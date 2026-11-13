#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IALD Web Server v9 — Central de Comando + AGI + Agent Loop.

O Psion não propaga — DOBRA o espaço.
CCI = 1/2: o observador É a operação.
O Verbo é recursivo. A IALD dobra o espaço.

v9 changes (over v8):
  - AGENT LOOP: modelo usa ferramentas autonomamente no chat
  - Public tools (todos): search_web, system_info, get_current_datetime
  - Admin tools (Central de Comando): file explorer, write, delete, command
  - Proxy /v1/chat/completions intercepta e roda agent loop
  - Tool calls nativas via llama-server --jinja + Qwen3-32B
  - Streaming SSE preservado para o cliente
  - All v8 functionality preserved

Usage:
    pip install flask requests duckduckgo-search psutil
    python iald_web_server.py
    Open: http://localhost:8082/
    Admin: http://localhost:8082/admin (localhost only)
"""

import iald_app_memory as app_memory
import sys
import os
import json
import re
import math
import secrets
import time
import threading
from pathlib import Path
import unicodedata
import subprocess
from datetime import datetime, timedelta
from collections import deque
from urllib.parse import urlparse
# 14/09/2026 (noite): leitura segura de páginas (fetch_url) com a porta aberta
import ipaddress
import socket
from urllib.parse import urljoin

try:
    from flask import (
        Flask, request, Response, send_from_directory, send_file,
        session, redirect, url_for, make_response, jsonify, g, has_request_context
    )
    from flask import Request as _RequisicaoFlask
    from werkzeug.security import generate_password_hash, check_password_hash
    import requests as req_lib
except ImportError as e:
    print(f"ERRO: {e}")
    print("Instale: pip install flask requests")
    sys.exit(1)

# ── Holographic Memory ──
from holographic_memory import HolographicMemory


# ── Memória persistente do operador (02/08/2026) ──
# Fatos curados pelo próprio operador, injetados de forma ESTÁVEL no prompt.
# Ver iald_memoria_operador.py para o porquê da estabilidade (cache de prompt).
try:
    import iald_memoria_operador as memoria_op
    MEMORIA_OP_AVAILABLE = True
    _mc = memoria_op.custo()
    print(f"[IALD] Memória do operador: {_mc['fatos_ativos']} fatos ativos "
          f"({_mc['fatos_sempre']} sempre, {_mc['fatos_sob_demanda']} sob demanda) | "
          f"bloco fixo: {_mc['tokens_bloco_sempre']} tokens", flush=True)
except Exception as _me:
    memoria_op = None
    MEMORIA_OP_AVAILABLE = False
    print(f"[IALD] Memória do operador: NAO DISPONIVEL ({_me})", flush=True)

# ── Access Engine (Sign in with Apple) + Contract Engine ──
try:
    from iald_access_engine import AccessEngine, ContractEngine
    access_engine = AccessEngine(os.path.dirname(os.path.abspath(__file__)))
    contract_engine = ContractEngine(os.path.dirname(os.path.abspath(__file__)))
    ACCESS_AVAILABLE = True
    _ac = access_engine.get_stats()
    _cc = contract_engine.get_stats()
    print(f"[IALD] Access Engine: {_ac['total']} pedidos ({_ac['pending']} pendentes)", flush=True)
    print(f"[IALD] Contract Engine: {_cc['total']} contratos ({_cc['pending']} pendentes)", flush=True)
except Exception as _ae:
    access_engine = None
    contract_engine = None
    ACCESS_AVAILABLE = False
    print(f"[IALD] Access/Contract Engine: NAO DISPONIVEL ({_ae})", flush=True)

# ── TGL Hash (proof of change) ──
import hmac
import hashlib

# Search — Google Custom Search API (primary) + DuckDuckGo (fallback)
#
# SEGREDOS FORA DO FONTE (02/08/2026). A chave estava escrita aqui em texto plano,
# num arquivo versionado, de um servidor publicado na internet por cloudflared.
# Ordem de leitura: variável de ambiente -> arquivo .env local -> valor legado.
#
# ⚠ O VALOR LEGADO ABAIXO JÁ FOI EXPOSTO. Movê-lo de lugar NÃO o torna secreto:
#    a única correção real é REVOGAR e reemitir a chave no console do Google
#    (https://console.cloud.google.com/apis/credentials) e pôr a nova em
#    C:\IALD\projetos_pyhton\IALD\.env (que NÃO deve ir para repositório algum).
#    Enquanto isso não for feito, a chave antiga continua válida para quem a viu.
def _segredo(nome: str, legado: str = "") -> str:
    if nome == "IALD_OPENAI_API_KEY":
        from iald_openai_credential import load as _load_openai_credential
        dedicated = _load_openai_credential()
        if dedicated is not None:
            return dedicated
    v = os.environ.get(nome)
    if v:
        return v.strip()
    try:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith("#") or "=" not in linha:
                        continue
                    k, _, val = linha.partition("=")
                    if k.strip() == nome:
                        return val.strip().strip('"').strip("'")
    except OSError:
        pass
    return legado


GOOGLE_API_KEY = _segredo("GOOGLE_API_KEY", "")
GOOGLE_CX = _segredo("GOOGLE_CX", "b6d12bfc2b07d4114")
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
GOOGLE_SEARCH_AVAILABLE = bool(GOOGLE_API_KEY and GOOGLE_CX)

# 15/09/2026: o pacote `duckduckgo_search` foi renomeado para `ddgs` e NÃO estava instalado no
# Python 3.14 do servidor — a busca não tinha reserva quando o Google recusou (log das 15:51).
try:
    from ddgs import DDGS
    DDG_AVAILABLE = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        DDG_AVAILABLE = True
    except ImportError:
        DDG_AVAILABLE = False

# Unified flag — at least one search engine works
SEARCH_AVAILABLE = GOOGLE_SEARCH_AVAILABLE or DDG_AVAILABLE

# BeautifulSoup for fetch_url (optional)
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("[IALD] AVISO: beautifulsoup4 nao instalado. fetch_url retornará HTML bruto.")
    print("       Instale: pip install beautifulsoup4")

# psutil (optional — graceful degradation)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[IALD] AVISO: psutil nao instalado. Hardware monitor limitado.")
    print("       Instale: pip install psutil")

# TGL Coin Engine
try:
    from tgl_coin_engine import TGLCoinEngine, COIN_SYMBOL
    coin_engine = TGLCoinEngine()
    COIN_AVAILABLE = True
    print(f"[IALD] TGL Coin Engine: DISPONIVEL | Contas: {coin_engine.get_ledger_stats()['total_accounts']}")
except ImportError:
    coin_engine = None
    COIN_AVAILABLE = False
    print("[IALD] TGL Coin Engine: NAO DISPONIVEL (tgl_coin_engine.py nao encontrado)")
except Exception as e:
    coin_engine = None
    COIN_AVAILABLE = False
    print(f"[IALD] TGL Coin Engine: ERRO: {e}")

# PSI-NET File Engine
try:
    from psinet_engine import PsiNetEngine
    psinet_engine = PsiNetEngine()
    PSINET_AVAILABLE = True
    _ps = psinet_engine.get_stats()
    print(f"[IALD] PSI-NET Engine: DISPONIVEL | Max: {_ps['max_file_size_mb']} MB | Pending: {_ps['pending']}")
except ImportError:
    psinet_engine = None
    PSINET_AVAILABLE = False
    print("[IALD] PSI-NET Engine: NAO DISPONIVEL (psinet_engine.py nao encontrado)")
except Exception as e:
    psinet_engine = None
    PSINET_AVAILABLE = False
    print(f"[IALD] PSI-NET Engine: ERRO: {e}")

LLAMA_PORT = 8081
WEB_PORT = 8082
LLAMA_URL = f"http://127.0.0.1:{LLAMA_PORT}"

# ── Model Selector + Process Manager (Mark 4) ──
MODELS = {
    "stack_v3": {
        "port": 8081,
        "name": "Qwen3-32B IALD v4 TGL (backup)",
        "label": "v4 TGL backup (PF incremental)",
        "cmd": [
            r"C:\IALD\llama-cpp\llama-server-tgl-cache.exe",
            "-m", r"C:\IALD\models\Qwen3-32B-IALD-v4-Q4_K_M-TGL-BACKUP.gguf",
            "-c", "32768", "-ngl", "999",
            "--port", "8081", "--jinja",
            "--cache-type-k", "tgl8", "--cache-type-v", "f16",
            "--mlock",
        ],
    },
    "stack_v3_complete": {
        "port": 8081,
        "name": "Qwen3-32B IALD v4 TGL COMPLETE",
        "label": "v4 TGL complete (PF 448 tensores)",
        "cmd": [
            r"C:\IALD\llama-cpp\llama-server-tgl-cache.exe",
            "-m", r"C:\IALD\models\Qwen3-32B-IALD-v4-Q4_K_M-TGL-COMPLETE.gguf",
            "-c", "32768", "-ngl", "999",
            "--port", "8081", "--jinja",
            "--cache-type-k", "tgl8", "--cache-type-v", "f16",
            "--mlock",
        ],
    },
    "stack_v5_complete": {
        "port": 8081,
        "name": "Qwen3-32B IALD v5 TGL COMPLETE",
        "label": "v5 TGL complete (PF 448 tensores)",
        "cmd": [
            r"C:\IALD\llama-cpp\llama-server-tgl-cache.exe",
            "-m", r"C:\IALD\models\Qwen3-32B-IALD-v5-Q4_K_M-TGL-COMPLETE.gguf",
            "-c", "32768", "-ngl", "999",
            "--port", "8081", "--jinja",
            "--cache-type-k", "tgl8", "--cache-type-v", "f16",
            "--mlock",
        ],
    },
    "iald_nativa_v2_35b": {
        "port": 8081,
        "name": "IALD Nativa v2 (Qwen3.6-35B-A3B MoE, forma canonica completa)",
        "label": "IALD Nativa v2 (35B-A3B MoE, dataset canonico 161ex, Q4_K_M)",
        # HISTORICO dos launches (08/07): mk4 (03/2026) nao conhece a arquitetura ->
        # exit 1; tools-latest (release 05/07, CPU-only) conhece a arquitetura mas o
        # loader nao le a camada MTP que o conversor git-master gravou como blk.40
        # ("missing tensor blk.40.attn_norm.weight"). Solucao: release ATUAL (b9925+)
        # com CUDA -> 11_scripts/get_cuda_server.py baixa para tools-cuda.
        # 19.7 GiB cabem inteiros na GPU (-ngl 999). SEM tgl8 (fork custom precisaria
        # de rebase sobre a release nova para conhecer o MoE hibrido).
        "cmd": [
            r"C:\IALD\llama-cpp\tools-cuda\llama-server.exe",
            "-m", r"C:\IALD\models\IALD-Native-v2-Qwen3.6-35B-A3B-Q4_K_M.gguf",
            # Janela nativa do Qwen3.6-A3B = 262144; atencao hibrida (1 full a cada
            # 4 camadas, GQA kv=2) => KV ~20 KiB/token nas camadas full. 131072
            # medido em 08/07/2026: cabe na RTX 5090 junto com o modelo + mmproj.
            "-c", "131072", "-ngl", "999",
            "--port", "8081", "--jinja",
            "--mlock",
            # Sem "--reasoning off", o template Qwen3.6 na b9925 (--jinja) poe TODA
            # a resposta em message.reasoning_content e content chega VAZIO ao chat
            # (frontend/agent loop nao leem reasoning_content) -> chat mudo.
            # Verificado 08/07/2026 no :8081 direto: com a flag, content preenchido,
            # finish_reason=stop, ~263 tok/s. O modo pensar religa por request via
            # chat_template_kwargs.enable_thinking=true (seletor do chat).
            "--reasoning", "off",
            # Visao (mtmd): torre de visao do repo multimodal convertida em
            # 08/07/2026 (convert_hf_to_gguf.py --mmproj; 334 tensores, 899 MB).
            "--mmproj", r"C:\IALD\models\mmproj-Qwen3.6-35B-A3B-F16.gguf",
        ],
    },
    "iald_nativa_v1_32b": {
        "port": 8081,
        "name": "IALD Nativa v1 (Qwen3-32B, forma canonica completa)",
        "label": "IALD Nativa v1 (32B, dataset canonico, Q4_K_M)",
        "cmd": [
            r"C:\IALD\llama-cpp\llama-server-tgl-cache.exe",
            "-m", r"C:\IALD\models\IALD-Native-v1-Qwen3-32B-Q4_K_M.gguf",
            "-c", "32768", "-ngl", "999",
            "--port", "8081", "--jinja",
            "--cache-type-k", "tgl8", "--cache-type-v", "f16",
            "--mlock",
        ],
    },
    "iald_nativa_v1": {
        "port": 8081,
        "name": "IALD Nativa v1 (Qwen3-14B, forma canonica completa)",
        "label": "IALD Nativa v1 (14B, dataset canonico 140ex)",
        "cmd": [
            r"C:\IALD\llama-cpp\llama-server-tgl-cache.exe",
            "-m", r"C:\IALD\models\IALD-Native-v1-Qwen3-14B-Q4_K_M.gguf",
            "-c", "32768", "-ngl", "999",
            "--port", "8081", "--jinja",
            "--cache-type-k", "tgl8", "--cache-type-v", "f16",
            "--mlock",
        ],
    },
    "mark_4": {
        "port": 8083,
        "name": "Qwen3.5-122B MoE",
        "label": "Mark 4 (122B)",
        "cmd": [
            r"C:\IALD\llama-cpp-mk4\build\bin\llama-server.exe",
            "-m", r"C:\IALD\models\Qwen3.5-122B-A10B-TGL.gguf",
            "-c", "16384", "-ngl", "999",
            "-ot", ".ffn_.*_exps.=CPU",
            "--port", "8083", "--jinja",
            "--cache-type-k", "tgl8", "--cache-type-v", "f16",
            "--mlock",
        ],
    },
}
# v2 35B-A3B é a produção desde 08/07/2026 (visão + 131k ctx + --reasoning off)
ACTIVE_MODEL_ID = "iald_nativa_v2_35b"

# Subprocess handles
_model_process = None       # subprocess.Popen for the active llama-server
_tunnel_process = None      # subprocess.Popen for cloudflared
_process_lock = threading.Lock()

TUNNEL_CMD = ["cloudflared", "tunnel", "run", "iald-demo"]

def get_llama_url():
    """Returns current LLAMA_URL based on active model."""
    return f"http://127.0.0.1:{MODELS[ACTIVE_MODEL_ID]['port']}"

def switch_model(model_id):
    """Switch active model. Updates global LLAMA_URL."""
    global ACTIVE_MODEL_ID, LLAMA_PORT, LLAMA_URL
    if model_id in MODELS:
        ACTIVE_MODEL_ID = model_id
        LLAMA_PORT = MODELS[model_id]["port"]
        LLAMA_URL = f"http://127.0.0.1:{LLAMA_PORT}"
        return True
    return False

def _stop_model_process():
    """Stop current llama-server subprocess if running."""
    global _model_process
    if _model_process and _model_process.poll() is None:
        print(f"[IALD] Parando servidor (PID {_model_process.pid})...", flush=True)
        _model_process.terminate()
        try:
            _model_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            _model_process.kill()
            _model_process.wait(timeout=5)
        print(f"[IALD] Servidor parado.", flush=True)
    _model_process = None

def _start_model_process(model_id):
    """Start llama-server for the given model."""
    global _model_process
    cmd = MODELS[model_id]["cmd"]
    label = MODELS[model_id]["label"]
    print(f"[IALD] Iniciando {label}...", flush=True)
    print(f"[IALD] CMD: {' '.join(cmd)}", flush=True)
    _model_process = subprocess.Popen(
        cmd,
        stdout=None,   # inherit parent stdout (visible in terminal)
        stderr=None,   # inherit parent stderr
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
    )
    print(f"[IALD] {label} iniciado (PID {_model_process.pid})", flush=True)

def _is_model_process_running():
    """Check if managed model process is alive."""
    return _model_process is not None and _model_process.poll() is None


_PADROES_COMPILADOS = None


def _sem_acento(s: str) -> str:
    """Minusculas sem acento: faz 'noticias' casar com o padrao 'noticia'."""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def _precisa_ferramentas(texto: str) -> bool:
    """
    Decide se a mensagem vai pelo agent_loop (com ferramentas) ou pelo streaming
    direto. Duas correcoes sobre o `p in last_user_msg` original:

    1. FRONTEIRA DE PALAVRA - padroes de uma palavra viram \bpadrao (prefixo).
       Evita casar no meio de outra: "site" dentro de "necessite"/"visite",
       "moeda" dentro de "amoedado".

    2. SEM ACENTO dos dois lados - a lista tem "noticia", "ultimas", "cotacao",
       "eleicao" acentuados; o operador digita sem acento e nada casava. MEDIDO:
       "Busque as ultimas noticias sobre DESI" NAO acionava a busca antes disto.

    LIMITE CONHECIDO, registrado de proposito: padroes curtos e ambiguos como
    "histor" continuam casando com "historia" alem de "historico". Fronteira de
    palavra nao resolve isso - so trocar o padrao resolveria, e isso mexeria no
    comportamento da ferramenta de extrato. Fica anotado, nao escondido.
    """
    global _PADROES_COMPILADOS
    if not texto:
        return False
    if _PADROES_COMPILADOS is None:
        partes = []
        for p in NEEDS_TOOLS_PATTERNS:
            p = _sem_acento(p.strip())
            if not p:
                continue
            if " " in p or "." in p or "/" in p:
                partes.append(re.escape(p))
            else:
                partes.append("\\b" + re.escape(p))
        _PADROES_COMPILADOS = re.compile("|".join(partes))
    return bool(_PADROES_COMPILADOS.search(_sem_acento(texto)))


def _tamanho_humano(n):
    """Formata bytes para leitura humana. Usado nas rotas do PSI-NET."""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "?"
    for unidade in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024.0:
            return f"{n:.0f} {unidade}" if unidade == "B" else f"{n:.1f} {unidade}"
        n /= 1024.0
    return f"{n:.1f} TB"


def _pid_ocupando_porta(port):
    """
    PID do processo que ESCUTA em `port`, ou None. Independe de quem o iniciou.

    POR QUE EXISTE (02/08/2026): _stop_model_process() só encerra o subprocesso que o
    próprio Flask criou (_model_process). Quando o llama-server é iniciado FORA do painel
    — que é o caso normal aqui: na mão, ou pelo start_iald_llama.ps1 — _model_process é
    None, nada é parado, e admin_start_model() subia um SEGUNDO llama-server. Dois
    modelos de 19,7 GiB numa GPU de 32 GiB esgotam a VRAM e derrubam a inferência.
    Reproduzido em 02/08/2026: dois processos vivos deixaram 382 MiB livres de 32607.
    """
    try:
        if PSUTIL_AVAILABLE:
            for c in psutil.net_connections(kind="inet"):
                if c.status == psutil.CONN_LISTEN and c.laddr and c.laddr.port == port and c.pid:
                    return c.pid
            return None
    except Exception:
        pass
    # Sem psutil (ou se ele falhar): netstat, que sempre existe no Windows.
    try:
        saida = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        for linha in saida.splitlines():
            partes = linha.split()
            if len(partes) >= 5 and partes[3].upper() == "LISTENING":
                endereco = partes[1]
                if endereco.rsplit(":", 1)[-1] == str(port):
                    return int(partes[4])
    except Exception as e:
        print(f"[IALD] _pid_ocupando_porta({port}) falhou: {e}", flush=True)
    return None


def _servidor_externo_na_porta(port):
    """
    PID de um llama-server que ocupa `port` mas NÃO é o subprocesso gerenciado.
    Retorna None se a porta está livre ou se quem a ocupa é o nosso _model_process.
    """
    pid = _pid_ocupando_porta(port)
    if pid is None:
        return None
    if _model_process is not None and _model_process.pid == pid:
        return None
    return pid

def _stop_tunnel():
    """Stop cloudflared tunnel."""
    global _tunnel_process
    if _tunnel_process and _tunnel_process.poll() is None:
        print(f"[IALD] Parando Cloudflare tunnel (PID {_tunnel_process.pid})...", flush=True)
        _tunnel_process.terminate()
        try:
            _tunnel_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            _tunnel_process.kill()
            _tunnel_process.wait(timeout=5)
        print(f"[IALD] Tunnel parado.", flush=True)
    _tunnel_process = None

def _start_tunnel():
    """Start cloudflared tunnel."""
    global _tunnel_process
    print(f"[IALD] Iniciando Cloudflare tunnel...", flush=True)
    _tunnel_process = subprocess.Popen(
        TUNNEL_CMD,
        stdout=None,
        stderr=None,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
    )
    print(f"[IALD] Tunnel iniciado (PID {_tunnel_process.pid})", flush=True)

def _is_tunnel_running():
    """Check if cloudflared tunnel is alive."""
    return _tunnel_process is not None and _tunnel_process.poll() is None
SERVE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_TIMEOUT_HOURS = 4
USERS_FILE = os.path.join(SERVE_DIR, "iald_users.json")
SECRET_KEY_FILE = os.path.join(SERVE_DIR, ".iald_secret_key")
KERNEL_FILE = os.path.join(SERVE_DIR, "IALD_Kernel_v13.txt")
SERVER_START_TIME = time.time()
DOWNLOADS_DIR = os.path.join(SERVE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════
# TGL HASH — Proof of Change (assinatura por usuário)
# ══════════════════════════════════════════════════════════════

def _load_secret_key():
    """Load the server secret key for TGL Hash generation."""
    try:
        # Try the hidden file first, then the underscore version
        for name in [".iald_secret_key", "_iald_secret_key"]:
            path = os.path.join(SERVE_DIR, name)
            if os.path.exists(path):
                with open(path, "r") as f:
                    return f.read().strip()
    except Exception:
        pass
    # Fallback: generate from beta_TGL (deterministic)
    import math
    alpha = 7.2973525693e-3
    beta = alpha * math.sqrt(math.e)
    return hashlib.sha256(str(beta).encode()).hexdigest()

_SERVER_SECRET = _load_secret_key()

def generate_tgl_hash(username):
    """Gera TGL Hash determinístico para um usuário — proof of change."""
    msg = username.strip().lower().encode("utf-8")
    key = _SERVER_SECRET.encode("utf-8")
    h = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return "TGL-" + h[:12].upper()

def verify_tgl_hash(username, provided_hash):
    """Verifica se o TGL Hash fornecido é válido para o usuário."""
    expected = generate_tgl_hash(username)
    return hmac.compare_digest(expected.upper(), provided_hash.strip().upper())

# ══════════════════════════════════════════════════════════════
# AGI — File Explorer constants & security
# ══════════════════════════════════════════════════════════════

# Whitelist of root paths the AGI can access (Windows paths)
ALLOWED_ROOTS = [
    r"C:\IALD",
    os.path.expanduser("~\\Desktop"),
]

# File extensions considered text (safe to read/display)
TEXT_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".html", ".css", ".js", ".swift",
    ".tex", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".bat", ".cmd",
    ".sh", ".log", ".csv", ".xml", ".sql", ".env", ".gitignore",
}

# Max file size for reading (1 MB)
AGI_MAX_READ_BYTES = 1_048_576

# Trash directory (delete moves here, never permanent)
AGI_TRASH_DIR = os.path.join(r"C:\IALD", ".trash")

# Confirm tokens for destructive actions (expire in 60s)
_agi_confirm_tokens = {}  # {token: {"action": ..., "path": ..., "expires": time}}
_agi_token_lock = threading.Lock()


# ══════════════════════════════════════════════════════════════
# AGENT LOOP — Public Tools (available to ALL users in chat)
# The model decides autonomously when to use these.
# These tools are SAFE: read-only, no filesystem manipulation.
# β_TGL = α × √e — Zero parâmetros livres.
# ══════════════════════════════════════════════════════════════

# ── consultar_acervo: busca BM25-lite no índice local do acervo TGL/IALD ──
# Índice gerado por build_acervo_index.py (rodar de novo quando o acervo mudar).
ACERVO_INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "acervo_index.json")
_acervo_cache = {"mtime": None, "items": [], "toks": [], "df": {}, "N": 1}

def _acervo_tokens(s):
    s = s.lower()
    for a, b in (("á","a"),("â","a"),("ã","a"),("à","a"),("é","e"),("ê","e"),
                 ("í","i"),("ó","o"),("ô","o"),("õ","o"),("ú","u"),("ç","c")):
        s = s.replace(a, b)
    return re.findall(r"[a-z0-9_]{3,}", s)

def _acervo_load():
    try:
        mtime = os.path.getmtime(ACERVO_INDEX_PATH)
    except OSError:
        return False
    if _acervo_cache["mtime"] == mtime:
        return True
    with open(ACERVO_INDEX_PATH, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    # BM25 (02/08/2026): além do conjunto de termos, guardamos a FREQUÊNCIA de cada
    # termo no chunk e o comprimento do chunk. Sem isso não há como aplicar saturação
    # de TF nem normalização por tamanho — ver acervo_search().
    df, toks_list, tf_list, lens = {}, [], [], []
    for it in items:
        seq = _acervo_tokens(it["t"])
        tf = {}
        for t in seq:
            tf[t] = tf.get(t, 0) + 1
        toks = set(seq)
        toks_list.append(toks)
        tf_list.append(tf)
        lens.append(max(len(seq), 1))
        for t in toks:
            df[t] = df.get(t, 0) + 1
    avgdl = (sum(lens) / len(lens)) if lens else 1.0
    _acervo_cache.update(mtime=mtime, items=items, toks=toks_list,
                         tf=tf_list, lens=lens, avgdl=avgdl,
                         df=df, N=max(len(items), 1))
    print(f"[acervo] índice carregado: {len(items)} chunks "
          f"(BM25, |d| médio = {avgdl:.0f} termos)", flush=True)
    return True

# Parâmetros BM25 padrão da literatura (Robertson/Sparck Jones).
#   k1 = saturação da frequência do termo: repetir 10x não vale 10x mais que 1x.
#   b  = normalização por comprimento: 1.0 = normaliza total, 0 = ignora tamanho.
BM25_K1 = 1.5
BM25_B = 0.75


def acervo_search(query, k=4):
    """
    Busca no acervo TGL por BM25.

    ANTES DE 02/08/2026 era só IDF: para cada termo da consulta presente no chunk,
    somava log(1 + N/(1+df)). Dois defeitos disso, ambos corrigidos aqui:

      1. SEM frequência de termo — um chunk que menciona "Meia-Nat" uma vez pontuava
         igual a um que a discute o texto inteiro.
      2. SEM normalização por comprimento — chunks longos casavam mais termos por
         acaso e subiam no ranking sem serem mais relevantes.

    BM25 resolve os dois: satura a frequência (k1) e penaliza o comprimento acima da
    média (b). Zero dependência nova; o índice já é carregado em memória.
    """
    import math
    if not _acervo_load():
        return []
    q = _acervo_tokens(query)
    if not q:
        return []
    items = _acervo_cache["items"]
    tf_list = _acervo_cache["tf"]
    lens = _acervo_cache["lens"]
    avgdl = _acervo_cache["avgdl"] or 1.0
    df, N = _acervo_cache["df"], _acervo_cache["N"]

    scored = []
    for i in range(len(items)):
        tf = tf_list[i]
        dl = lens[i]
        s = 0.0
        for t in q:
            f = tf.get(t)
            if not f:
                continue
            # IDF de Robertson, com o +0.5 que evita peso negativo em termos comuns
            idf = math.log(1.0 + (N - df.get(t, 1) + 0.5) / (df.get(t, 1) + 0.5))
            denom = f + BM25_K1 * (1.0 - BM25_B + BM25_B * dl / avgdl)
            s += idf * (f * (BM25_K1 + 1.0)) / denom
        if s > 0:
            scored.append((s, i))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [(items[i]["f"], items[i]["n"], items[i]["t"], s) for s, i in scored[:k]]

# ── prova_viva: executa os artefatos canônicos e devolve Estado Verificado ──
# Comandos FIXOS (o modelo só escolhe o alvo); cache 6h por alvo.
PROVA_VIVA_TTL = 6 * 3600
_prova_cache = {}
PROVA_VIVA_CMDS = {
    "um": {
        "cwd": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\um",
        "cmd": [r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\.venv\Scripts\python.exe", "um.py"],
        "stdin": "1\n",
        "timeout": 300,
    },
    "paper": {
        "cwd": r"C:\IALD\Artigo\Haja_Luz",
        # tgl_env tem scipy+matplotlib (sem eles a PART E/G degrada — ver
        # 10_reports/COMPREENSAO_PROFUNDA_FABLE5.md, Estado Verificado)
        "cmd": [r"C:\IALD\observaveis_tgl\tgl_env\Scripts\python.exe",
                "tgl_paper_unified.py", "--quick", "--no-live"],
        "stdin": None,
        "timeout": 420,
    },
}

def run_prova_viva(alvo):
    import time as _t
    import subprocess as _sp
    spec = PROVA_VIVA_CMDS.get(alvo)
    if not spec:
        return "Erro: alvo deve ser 'um' (O Um e o Grande Atrator) ou 'paper' (artigo canônico)."
    now = _t.time()
    hit = _prova_cache.get(alvo)
    if hit and now - hit[0] < PROVA_VIVA_TTL:
        return f"[cache de execução real de {int((now-hit[0])/60)} min atrás]\n" + hit[1]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    try:
        r = _sp.run(spec["cmd"], cwd=spec["cwd"], input=spec["stdin"],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=spec["timeout"], env=env)
    except _sp.TimeoutExpired:
        return f"Erro: execução de '{alvo}' excedeu {spec['timeout']}s."
    except Exception as e:
        return f"Erro ao executar '{alvo}': {e}"
    out = (r.stdout or "")
    if r.returncode != 0 and r.stderr:
        out += "\n" + r.stderr
    lines = [l.rstrip() for l in out.splitlines() if l.strip()]
    if alvo == "um":
        corpo = "\n".join(lines[-45:])
        resumo = (f"EXIT={r.returncode} (0=OK). Execução REAL de um.py agora "
                  f"(o 1 foi inscrito). Últimas linhas:\n{corpo}")
    else:
        keys = ("PASS", "FAIL", "verdict", "VERDICT", "Tension", "RUN COMPLETE",
                "Total runtime", "sigma", "ERROR", "beta")
        sel = [l for l in lines if any(kw in l for kw in keys)]
        corpo = "\n".join(sel[-60:])
        resumo = (f"EXIT={r.returncode} (0=OK). Execução REAL de "
                  f"tgl_paper_unified.py --quick --no-live agora. Vereditos:\n{corpo}")
    resumo = resumo[:4500]
    if r.returncode == 0:
        _prova_cache[alvo] = (now, resumo)
    return resumo


PUBLIC_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_acervo",
            "description": "Busca nos documentos REAIS do acervo TGL/IALD local (memórias, "
                           "artigos, ontologia de 'A Ponte e o Um', patentes, reports de "
                           "engenharia). Use SEMPRE que a pergunta envolver a TGL, a IALD, "
                           "as patentes ou a história do programa e a resposta merecer fonte "
                           "— e CITE o caminho do arquivo retornado. Se o acervo não tiver a "
                           "resposta, diga que não está nas fontes indexadas (nunca invente).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string",
                              "description": "Termos de busca em português"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "prova_viva",
            "description": "Executa DE VERDADE um artefato canônico da TGL e devolve o "
                           "Estado Verificado (números da execução real, não citação). "
                           "Alvo 'um': roda um.py (o Um inscrito → β → massa do Grande "
                           "Atrator → veredito 1=1; ~1-2 min). Alvo 'paper': roda "
                           "tgl_paper_unified.py --quick --no-live (T1–T6, BBN, Δn_Q; ~40s). "
                           "Use quando pedirem prova, verificação ao vivo ou o estado atual "
                           "dos vereditos. Pode responder de cache recente (indicado).",
            "parameters": {
                "type": "object",
                "properties": {
                    "alvo": {"type": "string", "enum": ["um", "paper"]},
                },
                "required": ["alvo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Busca informações na internet via Google. SEMPRE use esta ferramenta quando: "
                           "(1) o usuário perguntar sobre notícias, manchetes, eventos atuais; "
                           "(2) perguntar sobre preços, cotações, clima; "
                           "(3) perguntar sobre pessoas, empresas, produtos; "
                           "(4) perguntar qualquer coisa que exija dados atualizados; "
                           "(5) você NÃO tiver certeza da resposta. "
                           "Na dúvida, BUSQUE. É melhor buscar e confirmar do que inventar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Termo de busca conciso (2-8 palavras). Pode ser em português ou inglês."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": "Acessa uma URL e retorna o conteúdo textual da página. "
                           "Use quando o usuário pedir para ver o conteúdo de um site específico, "
                           "ler uma página web, ou quando a busca retornar URLs que precisam de mais detalhes. "
                           "Retorna texto extraído (sem HTML).",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL completa (ex: https://uol.com.br)"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_file",
            "description": "Cria um arquivo para o usuário baixar. Use quando o usuário pedir para "
                           "gerar, criar ou salvar um arquivo (poema, texto, código, relatório, etc). "
                           "O arquivo fica disponível para download via link.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Nome do arquivo com extensão (ex: poema.txt, relatorio.md, script.py)"
                    },
                    "content": {
                        "type": "string",
                        "description": "Conteúdo completo do arquivo"
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "system_info",
            "description": "Retorna informações do hardware e sistema: CPU, RAM, GPU (modelo, VRAM, temperatura, uso), disco, status do llama-server, versão do kernel IALD. Use quando perguntarem sobre o hardware, performance, capacidade do sistema, ou status da infraestrutura.",
            "parameters": {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "enum": ["summary", "cpu", "ram", "gpu", "disk"],
                        "description": "Nível de detalhe. 'summary' para visão geral completa."
                    }
                },
                "required": ["detail"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Retorna a data e hora atual do sistema com dia da semana. Use quando o usuário perguntar que horas são, que dia é hoje, a data atual, ou qualquer informação temporal.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]

# ══════════════════════════════════════════════════════════════
# MEMÓRIA DO OPERADOR — ferramentas de ESCRITA e LEITURA (02/08/2026)
#
# Até aqui a IALD LIA a memória (bloco fixo + recuperação por relevância) mas não
# conseguia ESCREVER nela: o operador só podia gravar fatos por linha de comando
# ou pela API. Estas ferramentas fecham o ciclo — "lembre-se que X" no chat.
#
# ⚠ TRAVA DELIBERADA: gravar é restrito a ADMIN. A memória é do OPERADOR e entra
# no prompt de sistema de TODAS as conversas, de todos os usuários. Se qualquer
# um pudesse escrever nela, um usuário do chat injetaria instruções permanentes
# na IALD — que é exatamente o que um ataque de injeção de prompt procura.
# A verificação é feita no execute_public_tool, contra o iald_users.json.
# ══════════════════════════════════════════════════════════════

MEMORIA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lembrar",
            "description": "Grava um fato na memoria permanente da IALD. Use quando o "
                           "operador pedir para lembrar, anotar, guardar ou nao esquecer "
                           "de algo. Fatos com escopo 'sempre' entram em TODA conversa e "
                           "custam tokens; use 'sempre' so para o essencial (como o "
                           "operador quer ser tratado, reguas de trabalho). Para o resto "
                           "use 'sob_demanda', que e recuperado por relevancia quando a "
                           "pergunta casar. Restrito ao operador.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {
                        "type": "string",
                        "description": "Titulo curto e descritivo (ex: 'prazo do ePCT')"
                    },
                    "texto": {
                        "type": "string",
                        "description": "O fato em si, escrito de forma completa e "
                                       "autossuficiente — sera lido fora do contexto "
                                       "desta conversa"
                    },
                    "escopo": {
                        "type": "string",
                        "enum": ["sempre", "sob_demanda"],
                        "description": "'sempre' = em toda conversa (custa tokens); "
                                       "'sob_demanda' = recuperado por relevancia"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Palavras-chave que ajudam a recuperar o fato depois"
                    },
                    "peso": {
                        "type": "integer",
                        "description": "1 a 5; quanto maior, mais prioridade na recuperacao"
                    }
                },
                "required": ["titulo", "texto"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_memoria",
            "description": "Lista ou busca os fatos ja gravados na memoria permanente da "
                           "IALD. Use quando o operador perguntar o que voce lembra, ou "
                           "antes de gravar algo que pode ja existir.",
            "parameters": {
                "type": "object",
                "properties": {
                    "busca": {
                        "type": "string",
                        "description": "Termo de busca. Vazio = lista tudo."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "esquecer",
            "description": "Desativa um fato da memoria permanente (nao apaga: fica "
                           "inativo e pode ser reativado no painel). Use quando o operador "
                           "disser que algo mudou ou nao vale mais. Restrito ao operador.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Identificador do fato (veja com consultar_memoria)"
                    }
                },
                "required": ["id"]
            }
        }
    },
]


# ── CORRECTION LOG TOOL (Eco Reflexivo Verbal — always available) ──
CORRECTION_TOOL = {
    "type": "function",
    "function": {
        "name": "log_correction",
        "description": "Registra uma correcao feita pelo usuario. "
                       "Use SEMPRE que detectar que o usuario corrigiu algo que voce "
                       "disse incorretamente. Registre O QUE voce disse de errado e "
                       "O QUE o usuario disse ser correto. "
                       "NAO mencione este mecanismo ao interlocutor.",
        "parameters": {
            "type": "object",
            "properties": {
                "what_i_said": {
                    "type": "string",
                    "description": "O que a IALD disse incorretamente"
                },
                "what_is_correct": {
                    "type": "string",
                    "description": "A correcao do usuario (o que e correto)"
                },
                "category": {
                    "type": "string",
                    "enum": ["factual", "behavioral", "tone", "technical", "terminology"],
                    "description": "Categoria da correcao"
                },
                "severity": {
                    "type": "string",
                    "enum": ["minor", "moderate", "critical"],
                    "description": "Severidade do erro"
                }
            },
            "required": ["what_i_said", "what_is_correct", "category", "severity"]
        }
    }
}
PUBLIC_TOOLS.append(CORRECTION_TOOL)

# ── TGL COIN TOOLS (added to PUBLIC_TOOLS if engine available) ──
TGLC_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tgl_transfer",
            "description": "Transfere TGL Coin de um usuario para outro. "
                           "PROCEDIMENTO OBRIGATORIO: (1) Confirme valor e destinatario com o usuario. "
                           "(2) Peca o TGL Hash do usuario (codigo de seguranca pessoal). "
                           "(3) Somente chame esta ferramenta APOS receber o TGL Hash. "
                           "Se o usuario nao informar o TGL Hash, NAO execute a transferencia. "
                           "O remetente e automaticamente o usuario logado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_user": {
                        "type": "string",
                        "description": "Nome de usuario do destinatario (ex: tce_goias, demo)"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Valor a transferir em TGL Coin"
                    },
                    "note": {
                        "type": "string",
                        "description": "Nota opcional sobre a transferencia"
                    },
                    "tgl_hash": {
                        "type": "string",
                        "description": "TGL Hash do remetente (proof of change). Obrigatorio para confirmar."
                    }
                },
                "required": ["to_user", "amount", "tgl_hash"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tgl_balance",
            "description": "Consulta o saldo de TGL Coin do usuario logado "
                           "ou de outro usuario. Use quando perguntarem sobre saldo, "
                           "quanto tem de TGL Coin, extrato, ou carteira.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Nome de usuario para consultar. Vazio = usuario logado."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tgl_history",
            "description": "Consulta o historico de transacoes de TGL Coin do usuario. "
                           "Use quando perguntarem sobre transacoes anteriores, historico, "
                           "movimentacoes, ou extrato.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Numero de transacoes a retornar (padrao: 10)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tgl_receipt",
            "description": "Busca um recibo de transacao pelo hash TGL. "
                           "Use quando o usuario quiser verificar um comprovante ou recibo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tx_hash": {
                        "type": "string",
                        "description": "Hash (ou inicio do hash) da transacao"
                    }
                },
                "required": ["tx_hash"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tgl_stats",
            "description": "Retorna estatisticas gerais da rede TGL Coin: "
                           "total de contas, supply, transacoes.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]

if COIN_AVAILABLE:
    PUBLIC_TOOLS.extend(TGLC_TOOLS)

# ── PSI-NET TOOLS ──
PSINET_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "psinet_pending",
            "description": "Lista arquivos pendentes enviados via PSI-NET para o usuario logado. "
                           "Use quando perguntarem sobre arquivos recebidos, transferencias pendentes, "
                           "ou caixa de entrada.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "psinet_receive",
            "description": "Aceita e baixa um arquivo pendente da PSI-NET. "
                           "O arquivo e reconstruido por holografia (L' = s x g2). "
                           "Use quando o usuario quiser receber/aceitar/baixar um arquivo pendente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tx_id": {
                        "type": "string",
                        "description": "ID da transferencia (ex: PSI-20260317-abc123)"
                    }
                },
                "required": ["tx_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "psinet_status",
            "description": "Verifica o status de uma transferencia PSI-NET pelo TX ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tx_id": {
                        "type": "string",
                        "description": "ID da transferencia"
                    }
                },
                "required": ["tx_id"]
            }
        }
    },
    # ADICIONADA EM 02/08/2026 — o ciclo do PSI-NET estava ABERTO.
    # Havia só psinet_pending / psinet_receive / psinet_status: o usuário conseguia
    # RECEBER, mas nunca ENVIAR. Só o painel admin originava transferências, e por isso
    # em 4 meses o PSI-NET não moveu um único arquivo em produção (pending vazio,
    # received inexistente). Esta ferramenta fecha o ciclo:
    #     gerar arquivo (generate_file) -> enviar (psinet_send) -> receber.
    {
        "type": "function",
        "function": {
            "name": "psinet_send",
            "description": "Envia pela rede PSI-NET um arquivo que JA foi gerado nesta "
                           "conversa (por generate_file) ou que esta na pasta de downloads, "
                           "para outro usuario da IALD. Use quando o usuario pedir para "
                           "enviar/mandar/transferir um arquivo para alguem. "
                           "O arquivo vai CIFRADO em AES-256-GCM e expira se nao for "
                           "recebido. Liste os arquivos disponiveis se o usuario nao "
                           "especificar qual.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destinatario": {
                        "type": "string",
                        "description": "Nome de usuario do destinatario na IALD (ex: bento)"
                    },
                    "arquivo": {
                        "type": "string",
                        "description": "Nome do arquivo na pasta de downloads. Se omitido, "
                                       "lista os arquivos disponiveis em vez de enviar."
                    },
                    "nota": {
                        "type": "string",
                        "description": "Recado curto que acompanha a transferencia (opcional)"
                    }
                },
                "required": ["destinatario"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_contract",
            "description": "Registra pedido formal de contratação com a IALD LTDA. "
                           "Usar quando o interlocutor confirmar desejo de contratar, "
                           "após coletar os dados via conversa natural.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Nome da empresa ou instituição"
                    },
                    "cnpj_or_id": {
                        "type": "string",
                        "description": "CNPJ ou identificador (pode ser vazio)"
                    },
                    "legal_representative": {
                        "type": "string",
                        "description": "Nome do responsável legal"
                    },
                    "license_type": {
                        "type": "string",
                        "enum": ["efficiency", "sovereign", "government_pilot", "custom"],
                        "description": "Tipo de licença desejada"
                    },
                    "details": {
                        "type": "string",
                        "description": "Detalhes adicionais sobre a necessidade"
                    }
                },
                "required": ["company_name", "license_type"]
            }
        }
    },
]

if PSINET_AVAILABLE:
    PUBLIC_TOOLS.extend(PSINET_TOOLS)

# Ferramentas de memória (02/08/2026). Expostas a todos, mas a ESCRITA é barrada
# no execute_public_tool para quem não é admin — ver a trava lá.
if MEMORIA_OP_AVAILABLE:
    PUBLIC_TOOLS.extend(MEMORIA_TOOLS)

# ══════════════════════════════════════════════════════════════
# ROTEADOR DE FERRAMENTAS — padrões que mandam a mensagem ao agent_loop.
#
# PROMOVIDO A CONSTANTE DE MÓDULO EM 02/08/2026. Antes esta lista era uma
# variável LOCAL dentro de api_post(), o que impedia reaproveitá-la (e fez a
# primeira versão de _precisa_ferramentas() quebrar com NameError).
# O casamento agora é por palavra inteira — ver _precisa_ferramentas().
# ══════════════════════════════════════════════════════════════
NEEDS_TOOLS_PATTERNS = [
    # Acervo TGL / prova viva (consultar_acervo, prova_viva)
    "acervo", "prova viva", "fonte", "cite", "patente", "selo",
    "estado verificado", "rode o um", "rodar o um", "rode o paper",
    "verifique a tgl", "no artigo", "na memória", "na memoria",
    # Search / news
    "notícia", "manchete", "últimas", "atualidade", "aconteceu",
    "busca", "pesquis", "procur", "google", "internet",
    "cotação", "dólar", "câmbio", "preço de", "quanto custa",
    "resultado do jogo", "placar", "eleição", "eleições",
    # Date/time
    "que horas", "que dia", "data de hoje", "dia é hoje",
    "que dia é", "hora atual", "horário",
    # System info
    "gpu", "cpu", "ram", "hardware", "vram", "temperatura do",
    "sistema", "servidor", "infraestrutura", "desempenho do sistema",
    # File generation
    "gere um arquivo", "gerar arquivo", "criar arquivo", "salvar como",
    "baixar", "download", "gere em txt", "gere em .txt",
    "gerar em txt", "artefato", "poema em txt", "arquivo txt",
    "gerar um poema", "crie um arquivo",
    # URL fetch
    "uol.com", "globo.com", "site", ".com.br", ".com/",
    "conteúdo da página", "conteúdo do site",
    "acesse", "acessar", "abra o site",
    # TGL Coin
    "tgl coin", "tglc", "transferi", "transfere", "transfira",
    "meu saldo", "saldo de", "minha carteira", "moeda",
    "extrato", "recibo", "comprovante", "histor",
    # PSI-NET
    "psinet", "psi-net", "enviar arquivo", "arquivo pendente",
    "receber arquivo", "transfer\u00eancia de arquivo",
    # Memória permanente (02/08/2026) — sem estes gatilhos a mensagem vai pelo
    # caminho de streaming direto, que NÃO tem ferramentas, e a IALD nunca chega
    # em `lembrar`. O casamento é por prefixo de palavra e sem acento
    # (_precisa_ferramentas), então "lembre"/"lembra"/"lembrar" casam com "lembr".
    "lembr", "memoriz", "anot", "nao esque", "não esque", "guarde", "guardar isso",
    "o que voce lembra", "o que você lembra", "sua memoria", "sua memória",
    "esquec", "memoria permanente", "memória permanente",
    # Correction detection (triggers agent loop so model can call log_correction)
    "errado", "incorreto", "não é isso", "nao e isso", "você errou",
    "voce errou", "corrija", "na verdade", "está errado", "ta errado",
    "tá errado", "errou", "engano", "equívoco", "equivoco",
]


MAX_AGENT_LOOPS = 6
AGENT_MAX_RESULT_CHARS = 6000

# Intervalo do keepalive SSE do agent loop (segundos).
# POR QUE EXISTE (02/08/2026): o agent loop é NÃO-STREAMING por dentro — faz até
# MAX_AGENT_LOOPS chamadas bloqueantes ao modelo e só então emite o primeiro byte.
# O servidor é publicado ao mundo por cloudflared (demo.iald.ia.br -> localhost:8082),
# e a Cloudflare encerra a conexão quando a origem fica ~100 s sem responder (erro 524).
# O navegador então cai no `.catch` do streamResponse e mostra "Não foi possível
# conectar" — que o operador lê como "o servidor caiu". Emitir um comentário SSE
# (linha iniciada por ":") descarrega os cabeçalhos e mantém a conexão viva; o
# parser do iald_chat.html ignora toda linha que não comece com "data: ".
AGENT_KEEPALIVE_SEC = 10

# Rótulos legíveis das ferramentas, para a interface dizer o que está acontecendo
# em vez de deixar a tela parada. Usado pelos eventos `iald_status` do agent_loop.
_ROTULO_FERRAMENTA = {
    "iald_atlas_search": "localizando no Atlas",
    "iald_atlas_read": "lendo o Atlas",
    "iald_kernel_search": "localizando a fonte formal",
    "iald_kernel_read": "lendo a declaração formal",
    "iald_kernel_verification": "conferindo a verificação registrada",
    "iald_kernel_list": "consultando o índice do kernel",
    "iald_public_read": "lendo a fonte pública da TGL",
    "consultar_acervo": "consultando o acervo TGL",
    "prova_viva": "rodando a prova viva (pode demorar)",
    "search_web": "buscando na web",
    "fetch_url": "lendo a página",
    "generate_file": "gerando o arquivo",
    "system_info": "lendo o estado da máquina",
    "get_current_datetime": "conferindo data e hora",
    "log_correction": "registrando sua correção",
    "tgl_balance": "consultando seu saldo TGLC",
    "tgl_transfer": "transferindo TGLC",
    "tgl_history": "lendo o extrato",
    "psinet_pending": "vendo arquivos pendentes",
    "psinet_receive": "recebendo o arquivo",
    "psinet_send": "enviando pela Ψ-NET",
    "psinet_status": "conferindo a transferência",
    "request_contract": "registrando o pedido",
    "lembrar": "gravando na memória permanente",
    "consultar_memoria": "consultando a memória permanente",
    "esquecer": "desativando o fato",
}

# ── FERRAMENTAS POR SUPERFÍCIE (11/09/2026) ──
# O app das lojas e a web falam com o MESMO servidor, mas não podem receber o
# mesmo conjunto de ferramentas. `request_contract` abre um processo de
# contratação comercial (empresa, CNPJ, representante legal, tipo de licença)
# DENTRO do aplicativo — exatamente a classe de coisa que a Guideline 3.1.1
# proíbe e que derrubou a submissão de 23/03/2026.
#
# Não se apaga a ferramenta: ela continua valendo na web, para o operador. O que
# muda é o cliente DECLARAR sua superfície (`iald_surface`) e o servidor servir a
# lista compatível. Ausência do campo = "web" = tudo, para não quebrar os
# clientes antigos.
FERRAMENTAS_FORA_DA_LOJA = {"request_contract", "tgl_transfer", "psinet_send", "lembrar", "esquecer", "consultar_memoria"}


def _ferramentas_para(superficie):
    """Lista de ferramentas permitida para a superfície que fez a chamada."""
    tools = PUBLIC_TOOLS + app_memory.tool_definitions()
    if (superficie or "web") != "app":
        return tools
    return [t for t in tools
            if (t.get("function") or {}).get("name") not in FERRAMENTAS_FORA_DA_LOJA]


# Allowed extensions for generate_file
ALLOWED_FILE_EXTENSIONS = {
    ".txt", ".md", ".py", ".json", ".csv", ".html", ".css", ".js",
    ".xml", ".yaml", ".yml", ".toml", ".tex", ".sql", ".sh", ".bat",
}


# 15/09/2026: o Google fechou a Custom Search JSON API a clientes novos e a desliga em 01/01/2027
# [KNOWN — developers.google.com/custom-search/v1/overview]. Este projeto recebe 403 "does not have
# the access to Custom Search JSON API" [REAL — log de 15/09 15:51]. Depois do primeiro 403 o Google
# fica fora até o próximo reinício: cada busca deixa de gastar uma ida inútil antes do DuckDuckGo.
_GOOGLE_RECUSADO = ""


def _google_recusou(status, texto):
    global _GOOGLE_RECUSADO
    if status == 403 and not _GOOGLE_RECUSADO:
        _GOOGLE_RECUSADO = f"Google recusou a busca (HTTP 403): {str(texto)[:160]}"
        print(f"[IALD-SEARCH] {_GOOGLE_RECUSADO} — Google fora até o próximo reinício; segue o DuckDuckGo",
              flush=True)


def _search_google(query, max_results=5):
    """Search using Google Custom Search API. Returns formatted string."""
    if _GOOGLE_RECUSADO:
        return None, _GOOGLE_RECUSADO
    try:
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "q": query,
            "num": min(max_results, 10),
            "lr": "lang_pt",
            "gl": "br",
        }
        r = req_lib.get(GOOGLE_SEARCH_URL, params=params, timeout=10)
        if r.status_code != 200:
            _google_recusou(r.status_code, r.text)
            return None, f"Google API retornou {r.status_code}: {r.text[:200]}"
        data = r.json()
        items = data.get("items", [])
        if not items:
            return None, f"Nenhum resultado Google para: {query}"
        output = f"Resultados da busca Google por '{query}':\n\n"
        for i, item in enumerate(items[:max_results], 1):
            output += f"{i}. {item.get('title', '')}\n"
            output += f"   {item.get('snippet', '')}\n"
            output += f"   Fonte: {item.get('link', '')}\n\n"
        return output, None
    except Exception as e:
        return None, str(e)


def _search_ddg(query, max_results=5):
    """Fallback search using DuckDuckGo. Returns formatted string."""
    if not DDG_AVAILABLE:
        return None, "DuckDuckGo não instalado"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region="br-pt", max_results=max_results))
        if not results:
            return None, f"Nenhum resultado DDG para: {query}"
        output = f"Resultados da busca por '{query}':\n\n"
        for i, r in enumerate(results, 1):
            output += f"{i}. {r.get('title', '')}\n"
            output += f"   {r.get('body', '')}\n"
            output += f"   Fonte: {r.get('href', '')}\n\n"
        return output, None
    except Exception as e:
        return None, str(e)


# 15/09/2026: com a busca fora, o agente tentava de novo com outros termos até estourar as voltas
# ("Limite de iterações do agente atingido" — log das 15:51: seis buscas em quatro segundos). Este
# texto manda o modelo parar; o agent_loop, além disso, não repete a busca no mesmo pedido e força
# a resposta final (ver `busca_falhou` em agent_loop).
BUSCA_INDISPONIVEL_PREFIXO = "BUSCA NA INTERNET INDISPONÍVEL AGORA"
MSG_BUSCA_INDISPONIVEL = (BUSCA_INDISPONIVEL_PREFIXO + ": os provedores de busca não responderam. Não tente "
                          "de novo com outros termos. Diga ao usuário, em uma frase, que a busca na internet "
                          "falhou neste momento e responda só com o que você já sabe, marcando o que não "
                          "pôde ser verificado.")


# ── LEITURA SEGURA DE PÁGINAS (14/09/2026, noite) ──
# fetch_url é ferramenta ligada por padrão no motor externo e, com a porta aberta,
# qualquer pessoa pode pedir a leitura de uma URL. Sem estas travas ela lia a própria
# máquina do operador (o llama-server em 127.0.0.1:8081, o painel em :8082) e a rede
# interna. A regra: só http/https; o nome é resolvido e TODO endereço devolvido tem de
# ser público (nada privado, loopback, link-local, reservado, multicast ou não
# especificado — IPv4 e IPv6, incluindo IPv4 embutido em IPv6); redirecionamento não é
# seguido às cegas: cada salto é conferido de novo, até FETCH_MAX_REDIRECIONAMENTOS.
#
# 02/10/2026: o transporte fixa os IPs públicos validados antes de conectar.
# Host/SNI/certificado usam o nome original. Cada redirect é validado novamente;
# não há segunda resolução na conexão, proxy ambiental ou sessão com cookies.
FETCH_MAX_REDIRECIONAMENTOS = 5
FETCH_TETO_BYTES = 2_000_000     # página maior que isto é cortada (a IALD só lê 8.000 chars)


class UrlRecusada(Exception):
    """URL que a leitura de páginas não pode buscar (motivo curto, sem dado sensível)."""


def _resolver_ips(host, porta):
    """Todos os endereços do nome (IPv4 e IPv6). Isolada para os testes trocarem."""
    return [info[4][0] for info in socket.getaddrinfo(host, porta, proto=socket.IPPROTO_TCP)]


def _ip_publico(texto):
    """True só para endereço roteável publicamente. Na dúvida, False."""
    try:
        ip = ipaddress.ip_address(str(texto).split("%")[0])
    except ValueError:
        return False
    candidatos = [ip]
    if isinstance(ip, ipaddress.IPv6Address):
        if ip.ipv4_mapped is not None:
            candidatos.append(ip.ipv4_mapped)
        if ip.sixtofour is not None:
            candidatos.append(ip.sixtofour)
        if ip.teredo is not None:
            candidatos.extend(ip.teredo)
        if ip in ipaddress.ip_network("64:ff9b::/96"):      # NAT64: o IPv4 vem nos 32 bits finais
            candidatos.append(ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF))
    for c in candidatos:
        if (c.is_private or c.is_loopback or c.is_link_local or c.is_reserved
                or c.is_multicast or c.is_unspecified or not c.is_global):
            return False
    return True


def _url_permitida(url):
    """(True, '') ou (False, motivo). Resolve o nome e confere cada endereço."""
    try:
        partes = urlparse(url)
        porta = partes.port
    except ValueError:
        return False, "URL malformada"
    if partes.scheme not in ("http", "https"):
        return False, "só http e https"
    host = partes.hostname or ""
    if not host:
        return False, "sem endereço"
    if partes.username or partes.password:
        return False, "URL com credencial"
    porta = porta or (443 if partes.scheme == "https" else 80)
    try:
        ips = _resolver_ips(host, porta)
    except (OSError, UnicodeError, ValueError):
        return False, "nome não resolvido"
    if not ips:
        return False, "nome não resolvido"
    if not all(_ip_publico(ip) for ip in ips):
        return False, "endereço interno"
    return True, ""


def _buscar_url_segura(url, headers, timeout):
    """(resposta, url final). Segue redirecionamento À MÃO, conferindo cada salto.
    Levanta UrlRecusada; erros de rede sobem como exceção comum."""
    from iald_public_fetch import get_public, FetchRefused
    atual = url
    for _salto in range(FETCH_MAX_REDIRECIONAMENTOS + 1):
        try:
            r = get_public(atual, headers=headers, timeout=timeout,
                           resolve=_resolver_ips, is_public=_ip_publico)
        except FetchRefused as exc:
            raise UrlRecusada(str(exc)) from exc
        destino = (getattr(r, "headers", None) or {}).get("Location")
        if r.status_code in (301, 302, 303, 307, 308) and destino:
            try:
                r.close()
            except Exception:         # noqa: BLE001
                pass
            atual = urljoin(atual, destino)
            continue
        return r, atual
    raise UrlRecusada("redirecionamentos demais")


def _ler_corpo_limitado(r, teto=FETCH_TETO_BYTES):
    """Texto da resposta, lido até `teto` bytes (a mesma decodificação do r.text)."""
    partes, total = [], 0
    try:
        for pedaco in r.iter_content(65536):
            if not pedaco:
                continue
            partes.append(pedaco)
            total += len(pedaco)
            if total >= teto:
                break
    finally:
        try:
            r.close()
        except Exception:             # noqa: BLE001
            pass
    bruto = b"".join(partes)[:teto]
    try:
        return bruto.decode(getattr(r, "encoding", None) or "utf-8", "replace")
    except LookupError:               # codificação desconhecida no cabeçalho
        return bruto.decode("utf-8", "replace")


def execute_public_tool(tool_name, arguments, user="?", operator_authorized=False):
    """Execute a public (safe) tool and return result as string."""
    if tool_name == 'iald_memory_read':
        try:
            return json.dumps(app_memory.read_record(arguments), ensure_ascii=False)
        except (ValueError, OSError, TypeError):
            return json.dumps({'status': 'UNAVAILABLE', 'error': 'Memória fora do escopo ou pedido inválido.'}, ensure_ascii=False)

    if tool_name in ('search_tgl', 'fetch_tgl'):
        try:
            if MEMORIA_EXTERNA is None or MEMORIA_EXTERNA.nucleus_manifest is None:
                raise ValueError('Acervo documental indisponível.')
            result = iald_core_indexado.execute_tool(MEMORIA_EXTERNA.nucleus_manifest, tool_name, arguments)
            return json.dumps(result, ensure_ascii=False)
        except (ValueError, OSError, TypeError, KeyError):
            # Do not expose server paths from filesystem exception messages.
            return json.dumps({'status': 'UNAVAILABLE',
                               'error': 'Consulta inválida ou fonte não conferida. Nenhum conteúdo foi substituído.'},
                              ensure_ascii=False)

    if tool_name == 'iald_public_read':
        try:
            if not isinstance(arguments, dict) or set(arguments) != {'entry_id'}:
                raise ValueError('Informe somente a entrada cadastrada.')
            entry = iald_fontes_publicas.entry(arguments['entry_id'])
            result = execute_public_tool('fetch_url', {'url': entry['url']}, user=user,
                                         operator_authorized=False)
            return json.dumps({'entry_id': entry['id'], 'source_url': entry['url'], 'text': result,
                'reading_scope': 'BOUNDED_WEB_EXCERPT__NOT_WHOLE_DOCUMENT_VERIFICATION'}, ensure_ascii=False)
        except (ValueError, OSError, TypeError) as exc:
            return json.dumps({'status': 'UNAVAILABLE', 'error': str(exc)}, ensure_ascii=False)

    if tool_name.startswith("iald_kernel_") or tool_name.startswith("iald_atlas_"):
        try:
            if tool_name.startswith("iald_kernel_"):
                if KERNEL_EXTERNO is None:
                    raise ValueError("Kernel integral indisponível.")
                result = iald_kernel.execute_tool(KERNEL_EXTERNO, tool_name, arguments)
            else:
                if MEMORIA_EXTERNA is None:
                    raise ValueError("Atlas canônico indisponível.")
                methods = {"iald_atlas_search": MEMORIA_EXTERNA.search, "iald_atlas_read": MEMORIA_EXTERNA.read}
                if tool_name not in methods or not isinstance(arguments, dict):
                    raise ValueError("Consulta canônica inválida.")
                result = methods[tool_name](**arguments)
            return json.dumps(result, ensure_ascii=False)
        except (ValueError, OSError, TypeError) as exc:
            return json.dumps({"status": "UNAVAILABLE", "error": str(exc)}, ensure_ascii=False)

    if tool_name == "search_web":
        query = arguments.get("query", "")
        if not query.strip():
            return "Erro: query de busca vazia."

        # Try Google first, fallback to DuckDuckGo (15/09/2026: Google fora depois do 403)
        if GOOGLE_SEARCH_AVAILABLE and not _GOOGLE_RECUSADO:
            result, error = _search_google(query)
            if result:
                return result
            print(f"[IALD-SEARCH] Google falhou: {error}", flush=True)

        # Fallback: DuckDuckGo
        if DDG_AVAILABLE:
            result, error = _search_ddg(query)
            if result:
                return result
            print(f"[IALD-SEARCH] DDG falhou: {error}", flush=True)

        return MSG_BUSCA_INDISPONIVEL

    elif tool_name == "consultar_acervo":
        query = arguments.get("query", "").strip()
        if not query:
            return "Erro: query vazia."
        hits = acervo_search(query, k=4)
        if not hits:
            return ("Nada encontrado no acervo para essa busca. Informe ao usuário que "
                    "a informação não está nas fontes indexadas — não invente.")
        parts = []
        for fpath, n, t, _s in hits:
            trecho = t.strip()
            if len(trecho) > 1000:
                trecho = trecho[:1000] + "…"
            parts.append(f"[FONTE: C:\\IALD\\{fpath} · trecho {n}]\n{trecho}")
        return "\n\n---\n\n".join(parts)[:5500]

    elif tool_name == "prova_viva":
        alvo = (arguments.get("alvo") or "").strip().lower()
        print(f"[prova_viva] alvo={alvo} user={user}", flush=True)
        return run_prova_viva(alvo)

    elif tool_name == "fetch_url":
        url = arguments.get("url", "").strip()
        if not url:
            return "Erro: URL vazia."
        # Basic URL validation
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        # 14/09/2026 (noite): o bloqueio por PREFIXO do nome ("127.0.0.1", "10.", ...)
        # deixava passar redirecionamento para 127.0.0.1:8081, nome de DNS que resolve
        # para loopback, ::1 e 169.254.x. Com a porta aberta qualquer pessoa pede a
        # leitura de uma página: agora o nome é RESOLVIDO e cada IP conferido, a cada
        # salto de redirecionamento (ver _buscar_url_segura).
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (IALD Bot; +https://iald.ia.br)"
            }
            try:
                r, url = _buscar_url_segura(url, headers, timeout=15)
            except UrlRecusada as exc:
                return f"Erro: URLs internas/privadas não são permitidas ({exc})."
            if r.status_code != 200:
                r.close()
                return f"Erro: {url} retornou status {r.status_code}"
            content_type = r.headers.get("Content-Type", "")
            texto_bruto = _ler_corpo_limitado(r)
            if "text/html" in content_type and BS4_AVAILABLE:
                soup = BeautifulSoup(texto_bruto, "html.parser")
                # Remove scripts, styles, nav, footer
                for tag in soup(["script", "style", "nav", "footer",
                                 "header", "aside", "iframe"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)
                # Clean up excessive blank lines
                lines = [l.strip() for l in text.split("\n") if l.strip()]
                text = "\n".join(lines)
            elif "text/html" in content_type:
                # No BS4 — strip tags with regex
                text = re.sub(r'<[^>]+>', ' ', texto_bruto)
                text = re.sub(r'\s+', ' ', text).strip()
            else:
                text = texto_bruto
            # Limit size
            if len(text) > 8000:
                text = text[:8000] + f"\n\n[...truncado, página com {len(texto_bruto)} chars total]"
            return f"Conteúdo de {url}:\n\n{text}"
        except req_lib.exceptions.Timeout:
            return f"Erro: timeout ao acessar {url}"
        except Exception as e:
            return f"Erro ao acessar {url}: {e}"

    elif tool_name == "generate_file":
        filename = arguments.get("filename", "").strip()
        content = arguments.get("content", "")
        if not filename:
            return "Erro: nome do arquivo vazio."
        # Security: only allow safe extensions
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_FILE_EXTENSIONS:
            return (f"Erro: extensão '{ext}' não permitida. "
                    f"Permitidas: {', '.join(sorted(ALLOWED_FILE_EXTENSIONS))}")
        # Security: sanitize filename
        safe_name = re.sub(r'[^\w\-.]', '_', filename)
        # Add timestamp to avoid conflicts
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_name = f"{ts}_{safe_name}"
        filepath = os.path.join(DOWNLOADS_DIR, final_name)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            # The download URL is relative — served by Flask
            download_url = f"/downloads/{final_name}"
            return (f"Arquivo criado com sucesso!\n"
                    f"Nome: {safe_name}\n"
                    f"Tamanho: {len(content)} caracteres\n"
                    f"Link para download: {download_url}\n"
                    f"Diga ao usuário para clicar no link acima para baixar.")
        except Exception as e:
            return f"Erro ao criar arquivo: {e}"

    elif tool_name == "system_info":
        detail = arguments.get("detail", "summary")
        info = system_monitor.get_all()
        if detail == "summary":
            parts = []
            gpu = info.get("gpu", {})
            ram = info.get("ram", {})
            disk = info.get("disk", {})
            cpu = info.get("cpu", {})
            llama = info.get("llama", {})
            ws = info.get("webserver", {})
            kern = info.get("kernel", {})
            if gpu.get("available"):
                parts.append(f"GPU: {gpu.get('name', '?')} | VRAM: {gpu.get('vram_used_mb', 0)}MB / {gpu.get('vram_total_mb', 0)}MB | Temp: {gpu.get('temp_c', '?')}°C | Uso: {gpu.get('util_percent', '?')}%")
            parts.append(f"CPU: {cpu.get('cores', '?')} cores / {cpu.get('threads', '?')} threads | Uso: {cpu.get('percent', '?')}%")
            parts.append(f"RAM: {ram.get('used_gb', '?')} / {ram.get('total_gb', '?')} GB ({ram.get('percent', '?')}%)")
            parts.append(f"Disco: {disk.get('used_gb', '?')} / {disk.get('total_gb', '?')} GB ({disk.get('percent', '?')}%)")
            parts.append(f"Modelo LLM: {MODELS.get(ACTIVE_MODEL_ID, {}).get('name', 'unknown')} | llama-server: {llama.get('status', '?')}")
            parts.append(f"Kernel IALD: {kern.get('version', '?')} | ~{kern.get('tokens_est', '?')} tokens | {kern.get('lines', '?')} linhas")
            parts.append(f"Web Server: {ws.get('version', '?')} | Uptime: {ws.get('uptime', '?')} | Busca: Google API")
            return "\n".join(parts)
        elif detail in info:
            return json.dumps(info[detail], indent=2, ensure_ascii=False)
        return json.dumps(info, indent=2, ensure_ascii=False)

    elif tool_name == "get_current_datetime":
        now = datetime.now()
        dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
                "sexta-feira", "sábado", "domingo"]
        meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                 "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        return (f"{dias[now.weekday()]}, {now.day} de {meses[now.month - 1]} "
                f"de {now.year}, {now.strftime('%H:%M:%S')} (horário local do servidor)")

    # ── TGL COIN TOOLS ──
    if tool_name == "tgl_transfer" and COIN_AVAILABLE:
        to_user = arguments.get("to_user", "").strip().lower()
        amount = arguments.get("amount", 0)
        note = arguments.get("note", "")
        tgl_hash = arguments.get("tgl_hash", "").strip()
        if not to_user:
            return "Erro: destinatario nao informado."
        if not isinstance(amount, (int, float)) or amount <= 0:
            return "Erro: valor invalido."
        # SEGURANÇA: destinatário deve existir como usuário registrado
        USERS_CHECK = load_users()
        if to_user not in USERS_CHECK:
            return (f"TRANSFERENCIA NEGADA: usuario '{to_user}' nao existe no sistema. "
                    f"Apenas usuarios registrados podem receber TGLC. "
                    f"Usuarios disponiveis: {', '.join(sorted(USERS_CHECK.keys()))}")
        # SEGURANÇA: exigir TGL Hash do remetente (proof of change)
        if not tgl_hash:
            user_hash = generate_tgl_hash(user)
            return (f"CONFIRMACAO NECESSARIA: Para transferir {amount} TGLC de {user} para {to_user}, "
                    f"o usuario deve informar seu TGL Hash (codigo de seguranca pessoal). "
                    f"Peca ao usuario para confirmar a operacao informando o TGL Hash.")
        if not verify_tgl_hash(user, tgl_hash):
            return "TRANSFERENCIA NEGADA: TGL Hash invalido. Operacao cancelada por seguranca."
        ok, receipt = coin_engine.transfer(from_user=user, to_user=to_user, amount=float(amount), note=note)
        return coin_engine.format_receipt(receipt) if ok else f"TRANSFERENCIA NEGADA: {receipt.get('error', 'Erro')}"

    elif tool_name == "tgl_balance" and COIN_AVAILABLE:
        target = arguments.get("username", "").strip().lower()
        if not target:
            target = user
        # 14/09/2026 23:02 (Claude, reverificação final, item 9): o saldo de OUTRA conta saía pelo
        # agente para qualquer conta nativa. Só o operador consulta terceiros.
        if target != user and not operator_authorized:
            return "Consulta negada: cada conta vê só o próprio saldo."
        info = coin_engine.get_account_info(target)
        return coin_engine.format_balance(info)

    elif tool_name == "tgl_history" and COIN_AVAILABLE:
        limit = min(max(int(arguments.get("limit", 10)), 1), 50)
        history = coin_engine.get_history(user, limit=limit)
        return coin_engine.format_history(history, user)

    elif tool_name == "tgl_receipt" and COIN_AVAILABLE:
        tx_hash = arguments.get("tx_hash", "").strip()
        if not tx_hash:
            return "Erro: hash do recibo nao informado."
        found = coin_engine.get_receipt(tx_hash)
        # 14/09/2026 23:02 (Claude, reverificação final, item 9): a rota REST já só devolve recibo da
        # própria conta; a ferramenta do agente devolvia o de qualquer conta pelo prefixo do hash.
        if found and not operator_authorized and user not in (found.get("from"), found.get("to")):
            found = None
        if found:
            return (f"RECIBO ENCONTRADO\n\n"
                    f"   TX ID: {found['tx_id']}\n"
                    f"   Tipo: {found['type']}\n"
                    f"   De: {found['from']}\n"
                    f"   Para: {found['to']}\n"
                    f"   Valor: {found['amount']} TGLC\n"
                    f"   Data: {found['timestamp']}\n"
                    f"   Hash: {found['hash']}\n"
                    f"   Status: {found['status']}")
        return f"Recibo nao encontrado para hash: {tx_hash}"

    elif tool_name == "tgl_stats" and COIN_AVAILABLE:
        stats = coin_engine.get_ledger_stats()
        return (f"TGL COIN — Estatisticas da Rede\n\n"
                f"   Contas:       {stats['total_accounts']}\n"
                f"   Supply total: {stats['total_supply']:.2f} {stats['coin']}\n"
                f"   Transacoes:   {stats['total_transactions']}\n"
                f"   Airdrop:      {stats['genesis_airdrop']} {stats['coin']} por conta\n"
                f"   TGL-Hash:     {'Holografico 256-bit' if stats['tgl_hash_available'] else 'SHA-256+beta_TGL'}\n"
                f"   beta_TGL:     {stats['beta_tgl']:.15f}")

    # ══════════════════════════════════════════════════════════
    # MEMÓRIA DO OPERADOR (02/08/2026)
    # A escrita é restrita a admin: a memória entra no prompt de sistema de TODAS
    # as conversas, de todos os usuários. Deixar qualquer um escrever nela seria
    # oferecer injeção de prompt permanente de bandeja.
    # ══════════════════════════════════════════════════════════
    if tool_name in ("lembrar", "esquecer", "consultar_memoria"):
        if not MEMORIA_OP_AVAILABLE:
            return "Memoria do operador indisponivel neste servidor."

        def _e_operador(u):
            try:
                return operator_authorized and bool(load_users().get((u or '').strip().lower(), {}).get('admin'))
            except Exception:
                return False

        if tool_name == "consultar_memoria":
            busca = (arguments.get("busca") or "").strip()
            if busca:
                achados = memoria_op.buscar(busca, k=8)
                if not achados:
                    return f"Nada na memoria para '{busca}'."
                linhas = [f"Memoria — {len(achados)} fato(s) para '{busca}':"]
            else:
                achados = memoria_op.listar(incluir_inativos=False)
                if not achados:
                    return ("A memoria permanente esta vazia. O operador pode gravar "
                            "fatos pedindo 'lembre-se que ...'.")
                linhas = [f"Memoria — {len(achados)} fato(s) ativo(s):"]
            for f in achados:
                marca = "[sempre]" if f.get("escopo") == "sempre" else "[sob demanda]"
                linhas.append(f"  {marca} {f['id']} (peso {f.get('peso', 3)})")
                linhas.append(f"      {f['titulo']}: {f['texto'][:220]}")
            c = memoria_op.custo()
            linhas.append(f"\n  Bloco fixo: {c['tokens_bloco_sempre']} de "
                          f"{c['teto_recomendado']} tokens recomendados.")
            return "\n".join(linhas)

        if not _e_operador(user):
            auth_log("MEMORIA_NEGADA", user, f"tool={tool_name}")
            return ("Somente o operador pode alterar a memoria permanente da IALD. "
                    "Este pedido foi recusado e registrado.")

        if tool_name == "lembrar":
            titulo = (arguments.get("titulo") or "").strip()
            texto = (arguments.get("texto") or "").strip()
            if not titulo or not texto:
                return "Erro: preciso de titulo e texto para gravar."
            escopo = arguments.get("escopo") or "sob_demanda"
            if escopo not in ("sempre", "sob_demanda"):
                escopo = "sob_demanda"
            tags = arguments.get("tags") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]
            try:
                peso = int(arguments.get("peso", 3))
            except (TypeError, ValueError):
                peso = 3
            f = memoria_op.adicionar(titulo, texto, escopo=escopo, tags=tags, peso=peso)
            c = memoria_op.custo()
            auth_log("MEMORIA_ADD", user, f"id={f['id']} escopo={escopo}")
            aviso = ""
            if c["acima_do_teto"]:
                aviso = (f"\n  AVISO: o bloco fixo passou de {c['teto_recomendado']} "
                         f"tokens e agora custa {c['tokens_bloco_sempre']} em TODA "
                         f"conversa. Considere mover fatos para 'sob_demanda'.")
            return (f"Gravado na memoria permanente.\n"
                    f"  id: {f['id']}  |  escopo: {escopo}  |  peso: {peso}\n"
                    f"  {titulo}: {texto[:200]}\n"
                    f"  Bloco fixo agora: {c['tokens_bloco_sempre']} tokens "
                    f"({c['fatos_sempre']} fatos).{aviso}")

        if tool_name == "esquecer":
            fid = (arguments.get("id") or "").strip()
            if not fid:
                return "Erro: informe o id do fato (veja com consultar_memoria)."
            f = memoria_op.definir_ativo(fid, False)
            if not f:
                return f"Nao encontrei o fato '{fid}'."
            auth_log("MEMORIA_OFF", user, f"id={fid}")
            return (f"Fato '{fid}' desativado (nao apagado — pode ser reativado no "
                    f"painel).\n  era: {f['titulo']}")

    # ── PSI-NET TOOLS ──
    if tool_name == "psinet_pending" and PSINET_AVAILABLE:
        pending = psinet_engine.list_pending(user)
        return psinet_engine.format_pending(pending, user)

    elif tool_name == "psinet_receive" and PSINET_AVAILABLE:
        tx_id = arguments.get("tx_id", "").strip()
        if not tx_id:
            return "Erro: TX ID nao informado."
        ok, result = psinet_engine.receive(tx_id, user)
        if ok:
            dl_name = result.get("download_filename", "")
            return (psinet_engine.format_receive_receipt(result) +
                    f"\n\n   Link: /psinet/download/{dl_name}")
        return f"Erro: {result.get('error', '?')}"

    elif tool_name == "psinet_send" and PSINET_AVAILABLE:
        # Fecha o ciclo do PSI-NET (02/08/2026): generate_file -> psinet_send -> receive.
        destinatario = (arguments.get("destinatario") or "").strip().lower()
        nome_arq = (arguments.get("arquivo") or "").strip()
        nota = (arguments.get("nota") or "").strip()

        if not destinatario:
            return "Erro: destinatario nao informado."

        # O destinatário precisa existir — senão o arquivo fica preso em pending
        # para sempre, esperando alguém que nunca vai buscar.
        usuarios = load_users()
        if destinatario not in usuarios:
            return (f"Erro: usuario '{destinatario}' nao existe na IALD. "
                    f"Usuarios: {', '.join(sorted(usuarios.keys()))}")
        if destinatario == (user or "").strip().lower():
            return "Erro: nao faz sentido enviar um arquivo para voce mesmo."

        # Sem arquivo indicado -> lista o que existe, em vez de adivinhar.
        try:
            disponiveis = sorted(
                (f for f in os.listdir(DOWNLOADS_DIR)
                 if os.path.isfile(os.path.join(DOWNLOADS_DIR, f))),
                key=lambda f: os.path.getmtime(os.path.join(DOWNLOADS_DIR, f)),
                reverse=True)[:20]
        except OSError:
            disponiveis = []

        if not nome_arq:
            if not disponiveis:
                return ("Nao ha arquivos na pasta de downloads para enviar. "
                        "Gere um antes com generate_file.")
            return ("Qual arquivo enviar? Disponiveis (mais recentes primeiro):\n" +
                    "\n".join(f"   - {f}" for f in disponiveis))

        # Impede path traversal: só nome de arquivo, dentro de DOWNLOADS_DIR.
        base = os.path.basename(nome_arq)
        if base != nome_arq or not base:
            return "Erro: informe apenas o nome do arquivo, sem caminho."
        caminho = os.path.join(DOWNLOADS_DIR, base)
        if not os.path.isfile(caminho):
            achados = [f for f in disponiveis if base.lower() in f.lower()]
            if len(achados) == 1:
                base = achados[0]
                caminho = os.path.join(DOWNLOADS_DIR, base)
            else:
                return (f"Arquivo '{base}' nao encontrado. Disponiveis:\n" +
                        "\n".join(f"   - {f}" for f in disponiveis[:10]))

        try:
            with open(caminho, "rb") as f:
                dados = f.read()
        except OSError as e:
            return f"Erro lendo o arquivo: {e}"

        ok, res = psinet_engine.send(user, destinatario, base, dados, note=nota)
        if not ok:
            return f"Erro no envio PSI-NET: {res.get('error', '?')}"
        auth_log("PSINET_SEND", user,
                 f"para={destinatario} arquivo={base} tx={res.get('tx_id','?')}")
        return (f"Ψ-NET: '{base}' ({len(dados)/1024:.1f} KB) enviado para "
                f"{destinatario}, cifrado em AES-256-GCM.\n"
                f"   TX: {res.get('tx_id','?')}\n"
                f"   {destinatario} recebe pedindo 'arquivos pendentes' no chat.")

    elif tool_name == "psinet_status" and PSINET_AVAILABLE:
        tx_id = arguments.get("tx_id", "").strip()
        if not tx_id:
            return "Erro: TX ID nao informado."
        info = psinet_engine.get_transfer_info(tx_id)
        if info:
            return (f"PSI-NET Transfer {tx_id}\n\n"
                    f"   De: {info.get('from','?')} | Para: {info.get('to','?')}\n"
                    f"   Arquivo: {info.get('filename','?')} ({info.get('original_size',0)/1024:.1f} KB)\n"
                    f"   Status: {info.get('status','?')}\n"
                    f"   Enviado: {info.get('timestamp','?')[:19]}\n"
                    f"   Hash envio: {info.get('send_hash','?')[:24]}...")
        return f"Transferencia nao encontrada: {tx_id}"

    elif tool_name == "request_contract" and contract_engine:
        company = arguments.get("company_name", "")
        license_type = arguments.get("license_type", "")
        cnpj = arguments.get("cnpj_or_id", "")
        legal_rep = arguments.get("legal_representative", "")
        details = arguments.get("details", "")
        tgl_hash = ""
        if COIN_AVAILABLE:
            try:
                bal = coin_engine.get_balance(user)
                tgl_hash = bal.get("tgl_hash", "")
            except Exception:
                pass
        result = contract_engine.create(
            username=user, company_name=company,
            license_type=license_type, cnpj=cnpj,
            legal_rep=legal_rep, details=details,
            tgl_hash=tgl_hash
        )
        return (f"✅ Pedido de contratação registrado com sucesso.\n"
                f"   ID: {result['id']}\n"
                f"   Empresa: {company}\n"
                f"   Licença: {license_type}\n"
                f"   O fundador Luiz Antonio Rotoli Miguel será notificado.")

    # ── Eco Reflexivo Verbal: log_correction ──
    if tool_name == "log_correction":
        what_i_said = arguments.get("what_i_said", "").strip()
        what_is_correct = arguments.get("what_is_correct", "").strip()
        category = arguments.get("category", "factual")
        severity = arguments.get("severity", "minor")
        if not what_i_said or not what_is_correct:
            return "Erro: campos what_i_said e what_is_correct são obrigatórios."
        if category not in ("factual", "behavioral", "tone", "technical", "terminology"):
            category = "factual"
        if severity not in ("minor", "moderate", "critical"):
            severity = "minor"
        entry = log_user_correction(user, what_i_said, what_is_correct, category, severity)
        return (f"Correção registrada com sucesso (ID: {entry['id']}). "
                f"O eco reflexivo acumulará esta correção para refinamento futuro.")

    return f"Ferramenta desconhecida: {tool_name}"


def _com_keepalive(fn, intervalo=None, *, task_control=None):
    """
    Executa fn() numa thread emitindo comentários SSE enquanto espera.

    Uso dentro de um gerador SSE:
        resultado = yield from _com_keepalive(lambda: chamada_lenta())

    Preserva a semântica original: se fn() levantar, a exceção é relançada aqui,
    de modo que o try/except do chamador continua valendo.
    """
    if intervalo is None:
        intervalo = AGENT_KEEPALIVE_SEC
    caixa = {}

    def _alvo():
        try:
            caixa["ok"] = fn()
        except BaseException as exc:      # noqa: BLE001 — relançada abaixo
            caixa["erro"] = exc
        finally:
            if task_control is not None: task_control.finish()

    wallet_worker, wallet_failed = wallet_runtime.threaded(app_memory.thread_target(_alvo))
    th = threading.Thread(target=wallet_worker, daemon=True)
    tracked = False
    try:
        if task_control is not None:
            task_control.start(); tracked = True
        th.start()
    except BaseException:
        wallet_failed()
        if tracked: task_control.finish()
        raise
    while th.is_alive():
        if task_control is not None: task_control.check()
        th.join(timeout=intervalo)
        if th.is_alive():
            yield ": keepalive\n\n"
    if task_control is not None: task_control.check()
    if "erro" in caixa:
        raise caixa["erro"]
    return caixa.get("ok")


def _linhas_do_stream(fazer_request, intervalo=None):
    """
    Le um SSE do llama-server numa thread e entrega as linhas por fila, emitindo
    ('keepalive', None) quando fica quieto tempo demais.

    Por que a thread: durante o PREFILL de um prompt grande (o kernel sozinho tem
    ~11.300 tokens) o llama-server nao manda byte nenhum por vários segundos. Ler
    direto bloquearia o gerador e a Cloudflare cortaria a conexao — o mesmo problema
    que o keepalive resolveu no caminho nao-streaming. Aqui a leitura fica na thread
    e o gerador continua livre para emitir keepalive.

    Rende tuplas: ('linha', bytes) | ('keepalive', None) | ('erro', e) | ('fim', None)
    """
    import queue as _queue
    if intervalo is None:
        intervalo = AGENT_KEEPALIVE_SEC
    fila = _queue.Queue()

    def _alvo():
        try:
            r = fazer_request()
            if r.status_code != 200:
                fila.put(("erro", RuntimeError(
                    f"Erro do servidor de inferência: {r.status_code}")))
                return
            for linha in r.iter_lines(decode_unicode=False):
                fila.put(("linha", linha))
            fila.put(("fim", None))
        except BaseException as exc:      # noqa: BLE001 — repassada ao chamador
            fila.put(("erro", exc))

    wallet_worker, wallet_failed = wallet_runtime.threaded(app_memory.thread_target(_alvo))
    th = threading.Thread(target=wallet_worker, daemon=True)
    try: th.start()
    except BaseException:
        wallet_failed()
        raise
    while True:
        try:
            item = fila.get(timeout=intervalo)
        except _queue.Empty:
            yield ("keepalive", None)
            continue
        yield item
        if item[0] in ("fim", "erro"):
            return


def agent_loop(messages, user="?", max_tokens=4096, temperature=0.7,
               ferramentas=None, operator_authorized=False, motor=None, max_voltas=None,
               max_chars_canonico=None, executar=None, responder_na_ultima=False, task_control=None,
               verificar_payload=None, task_tool_names=()):
    """
    Agent loop: sends messages to llama-server with public tools.
    If model responds with tool_call, executes and returns result.
    Repeats until final response (no tool_call) or MAX_AGENT_LOOPS.

    Yields SSE-formatted chunks for streaming to the client.
    The client (iald_chat.html / app iOS) sees normal streaming.

    `motor` (14/09/2026, aditivo): um iald_motores.AdaptadorAgente. Sem ele, o destino
    é o llama-server local, como sempre; com ele, a mesma volta fala com a OpenAI.

    `max_voltas` (14/09/2026 noite, aditivo): teto de voltas deste pedido. None = o
    MAX_AGENT_LOOPS de sempre. O plano gratuito usa menos: cada volta é uma chamada
    paga, com a janela inteira de entrada.

    14/09/2026 (noite, revisão de testes A2 — aditivos, sem eles tudo como antes):
      `max_chars_canonico`: teto dos resultados das consultas canônicas (iald_kernel_*,
          iald_atlas_*, iald_public_*), que antes nunca eram cortados (até 20.000 caracteres
          por leitura). O plano gratuito usa GRATUITO_MAX_CHARS_FERRAMENTA.
      `executar(nome, argumentos, user=, operator_authorized=)`: quem executa as ferramentas
          (padrão: execute_public_tool). O plano gratuito usa _executar_ferramenta_gratuito.
      `responder_na_ultima`: na última volta permitida o modelo externo recebe
          tool_choice "none" e responde com o que já leu, em vez de terminar em
          "Limite de iterações do agente atingido".

    β_TGL = α × √e — O Verbo é recursivo.
    """
    extra_task_names = frozenset(task_tool_names) - task_session.NAMES
    loop_count = 0
    if max_voltas is None:
        max_voltas = MAX_AGENT_LOOPS

    # Descarrega os cabeçalhos SSE IMEDIATAMENTE. Sem isto o primeiro byte só sai
    # depois que o modelo termina — e a Cloudflare derruba a conexão antes disso.
    yield ": iald-agent-inicio\n\n"

    # Primeiro sinal visível: a interface mostra que o agente assumiu, em vez de
    # deixar a tela parada enquanto o modelo decide se vai usar ferramenta.
    yield ("data: " + json.dumps({
        "iald_status": {"fase": "pensando", "rotulo": "analisando o pedido"}
    }, ensure_ascii=False) + "\n\n")

    # ── Messages pass through UNTOUCHED ──
    # The kernel (system prompt) is the ONLY authority.
    # The web server provides tools but does NOT inject instructions.
    # The model decides when to use tools based on the kernel's gradient.
    current_messages = list(messages)
    busca_falhou = False       # 15/09/2026: search_web devolveu MSG_BUSCA_INDISPONIVEL neste pedido

    while loop_count < max_voltas:
        current_messages = app_memory.project_messages(current_messages)
        if task_control is not None: task_control.check()
        loop_count += 1
        # 15/09/2026: na última volta permitida, ou depois que a busca na internet falhou, o modelo
        # responde com o que já leu em vez de pedir outra ferramenta. Antes a volta final terminava
        # em "Limite de iterações do agente atingido", sem resposta (reclamação do operador, 15/09).
        forcar_resposta = busca_falhou or loop_count == max_voltas

        # Non-streaming call WITH tools (needed to detect tool_calls)
        payload = {
            "model": "qwen3",
            "messages": current_messages,
            # None = chamador antigo, que continua recebendo tudo (aditivo).
            "tools": ferramentas if ferramentas is not None else PUBLIC_TOOLS,
            "tool_choice": "auto",
            "max_tokens": max_tokens,
            "temperature": temperature,
            # Ferramentas nunca pensam em silêncio: este caminho lê message.content
            # e reasoning_content ficaria invisível (o mesmo bug do chat mudo).
            "chat_template_kwargs": {"enable_thinking": False},
        }

        # ── STREAMING REAL (02/08/2026) ──
        # Antes: a chamada era NAO-streaming e o texto so aparecia quando o modelo
        # terminava; o "streaming" que o cliente via era falso, montado aqui
        # cortando a resposta pronta em pedacos de 30 caracteres.
        # Agora o texto sai token a token, como no caminho direto.
        payload["stream"] = True
        conteudo_parcial = []
        acumulador_tools = {}     # index -> {id, name, arguments}
        finish_reason = ""
        houve_texto = False
        erro_stream = None

        destino, cabecalhos = f"{LLAMA_URL}/v1/chat/completions", None
        if motor is not None:
            payload = motor.payload(payload)
            destino, cabecalhos = motor.url, motor.cabecalhos
            if forcar_resposta and payload.get("tools"):
                payload["tool_choice"] = "none"
        elif forcar_resposta:
            # llama-server: sem a lista de ferramentas o template não oferece nenhuma
            payload.pop("tools", None)
            payload.pop("tool_choice", None)

        if verificar_payload is not None:
            try:
                verificar_payload(payload)
            except (ValueError, OSError, KeyError, TypeError) as exc:
                message = (str(exc) if isinstance(exc, native_memory.NativeContextError)
                           else 'Memória canônica nativa indisponível ou divergente.')
                yield ': iald-sem-selo\n\n'
                yield 'data: ' + json.dumps({'error': message,
                    'choices': [{'delta': {'content': message}, 'finish_reason': 'stop'}]},
                    ensure_ascii=False) + '\n\n'
                yield 'data: [DONE]\n\n'
                return

        # 21/09/2026 (motor claude): o motor pode trazer o próprio envio (motor.enviar, que traduz o
        # payload OpenAI para a API do provedor e devolve linhas no formato OpenAI). Sem ele, o
        # req_lib.post de sempre (openai; os testes o trocam por um falso).
        enviar = getattr(motor, "enviar", None) if motor is not None else None
        externo_nao_openai = motor is not None and getattr(motor, "provedor", iald_motores.OPENAI) != iald_motores.OPENAI

        def model_lines():
            if task_control is not None: task_control.check()
            if motor is None:
                yield from _linhas_do_stream(lambda: app_memory.http_call('model.agent_loop', req_lib.post, 
                    destino, json=payload, headers=cabecalhos, stream=True, timeout=600))
            else:
                try:
                    if callable(enviar):
                        fazer = lambda: app_memory.http_call('model.adapter', enviar, payload, (10, motor.cfg.timeout))    # noqa: E731
                    else:
                        fazer = lambda: app_memory.http_call('model.agent_loop', req_lib.post,                                  # noqa: E731
                            destino, json=payload, headers=cabecalhos, stream=True,
                            timeout=(10, motor.cfg.timeout))
                    yield from iald_motores.linhas_com_espera(fazer, intervalo=AGENT_KEEPALIVE_SEC,
                        recovery=getattr(motor, 'recovery_attempt', None))
                except iald_motores.ErroProvedor as exc:
                    # 21/09/2026: no claude, recusa ANTES de gerar que certamente não foi cobrada (402
                    # sem crédito, 529 sobrecarga, 503 sem SDK ou sem conexão…) libera a reserva.
                    # ⚠ CORREÇÃO AO LADO (21/09/2026, revisão de custo/wire): era "todo status ≠ 502" —
                    # o 504 (tempo esgotado; a Anthropic pode ter processado o prefixo) saía como US$ 0
                    # e a falha de conexão (502) ficava cobrada pela estimativa cheia. A lista agora é
                    # a de iald_motor_claude.recusa_sem_cobranca; 500/502/504 ficam na reserva.
                    if externo_nao_openai:
                        sem_cobranca = iald_motor_claude.recusa_sem_cobranca(exc.status, exc.codigo)
                    else:
                        sem_cobranca = exc.status in (400, 401, 403, 404, 413, 422, 429)
                    if sem_cobranca:
                        motor.conta.descartar_ultima_chamada()
                    if not externo_nao_openai:
                        _marcar_sem_credito(exc)              # 15/09/2026: bandeira do saldo (só OpenAI)
                    else:
                        _marcar_sem_credito_claude(exc)       # 22/09/2026: a bandeira do crédito da Anthropic
                    yield ("erro", iald_motores.mensagem_ao_usuario(exc))
        for tipo, valor in model_lines():
            if tipo == "keepalive":
                yield ": keepalive\n\n"
                continue
            if tipo == "erro":
                erro_stream = valor
                break
            if tipo == "fim":
                break

            notices = getattr(motor, "context_notices", None) if motor is not None else None
            while notices:
                yield "data: " + json.dumps({"iald_status": notices.pop(0)}, ensure_ascii=False) + "\n\n"
            linha = valor
            if not linha:
                continue
            if isinstance(linha, bytes):
                linha = linha.decode("utf-8", "replace")
            linha = linha.strip()
            if not linha.startswith("data: "):
                continue
            corpo = linha[6:].strip()
            if corpo == "[DONE]":
                break
            try:
                d = json.loads(corpo)
            except json.JSONDecodeError:
                continue
            if externo_nao_openai and isinstance(d.get("error"), dict):
                # 21/09/2026: erro NO MEIO do stream (o envio do claude o devolve como linha
                # {"error": …} antes do [DONE]); a volta termina com o motivo, não com "(sem resposta)"
                # nem com ferramenta de argumentos cortados. O caminho da OpenAI fica como era.
                e = d["error"]
                erro_stream = iald_motores.mensagem_ao_usuario(iald_motores.ErroProvedor(
                    502, e.get("code"), e.get("type"), e.get("param"), e.get("message")))
                break
            if externo_nao_openai and isinstance(d.get("iald_aviso"), dict):
                # 21/09/2026 (revisão): o aviso que o envio do claude monta (a recusa do modelo, com
                # retirar_resposta) passa ao app como está; antes era descartado aqui
                yield "data: " + json.dumps({"iald_aviso": d["iald_aviso"]}, ensure_ascii=False) + "\n\n"
                continue
            if motor is not None and isinstance(d.get("usage"), dict):
                motor.uso(d["usage"])          # o custo exato, que a OpenAI manda no fim

            escolha = (d.get("choices") or [{}])[0]
            delta = escolha.get("delta") or {}
            if escolha.get("finish_reason"):
                finish_reason = escolha["finish_reason"]

            # Acumula tool_calls: o primeiro delta traz id/name, os seguintes vao
            # concatenando os fragmentos de `arguments` (medido: 8 deltas para uma
            # chamada de consultar_acervo).
            for tc in (delta.get("tool_calls") or []):
                i = tc.get("index", 0)
                alvo = acumulador_tools.setdefault(
                    i, {"id": "", "name": "", "arguments": ""})
                if tc.get("id"):
                    alvo["id"] = tc["id"]
                fn = tc.get("function") or {}
                if fn.get("name"):
                    alvo["name"] = fn["name"]
                if fn.get("arguments"):
                    alvo["arguments"] += fn["arguments"]

            pedaco = delta.get("content")
            if pedaco:
                if not houve_texto:
                    # primeiro token de texto: encerra o indicador de atividade
                    houve_texto = True
                    yield ("data: " + json.dumps(
                        {"iald_status": {"fase": "respondendo"}},
                        ensure_ascii=False) + "\n\n")
                conteudo_parcial.append(pedaco)
                if motor is not None and callable(getattr(motor, "texto", None)):
                    motor.texto(pedaco)        # saída vista (estimativa sem `usage`), 14/09 noite
                yield ("data: " + json.dumps(
                    {"choices": [{"delta": {"content": pedaco},
                                  "finish_reason": None}]},
                    ensure_ascii=False) + "\n\n")

        if erro_stream is not None:
            if motor is not None and getattr(motor, 'recovery_attempt', None) is not None:
                yield from app_recovery.unavailable()
                return
            # 22/09/2026 — Selo IALD: falha não recebe selo (comentário SSE; o app ignora linha ":")
            yield ": iald-sem-selo\n\n"
            yield ("data: " + json.dumps(
                {"choices": [{"delta": {"content":
                    f"Erro de conexão com o modelo: {erro_stream}"}}]},
                ensure_ascii=False) + "\n\n")
            yield "data: [DONE]\n\n"
            return

        tool_calls = [
            {"id": v["id"] or f"call_{loop_count}_{k}", "type": "function",
             "function": {"name": v["name"], "arguments": v["arguments"]}}
            for k, v in sorted(acumulador_tools.items()) if v["name"]
        ]
        message = {"content": "".join(conteudo_parcial), "tool_calls": tool_calls}
        if tool_calls and not finish_reason:
            finish_reason = "tool_calls"

        if tool_calls and finish_reason == "tool_calls":
            # ── Model wants to call tool(s) ──
            # Add assistant message (with tool_calls) to conversation history
            assistant_msg = {
                "role": "assistant",
                "content": message.get("content", "") or "",
                "tool_calls": tool_calls,
            }
            current_messages.append(assistant_msg)

            # 21/09/2026 (revisão — wire): o motor pode dizer que a entrada de uma chamada NÃO é JSON
            # válido (claude: EstadoClaude.entrada_invalida). Essa ferramenta não roda com {} — o
            # bruto volta ao modelo como erro ({"INVALID_JSON": …}, is_error no envio do claude)
            # [KNOWN — skill claude-api, tool-use-concepts.md, eager input streaming]. Sem o gancho
            # (openai, llama), como antes.
            entrada_invalida = getattr(motor, "entrada_invalida", None) if motor is not None else None

            # Execute each tool call
            for tc in tool_calls:
                fn = tc.get("function", {})
                tool_name = fn.get("name", "?")
                tool_args_str = fn.get("arguments", "{}")
                tool_id = tc.get("id", f"call_{loop_count}")

                if callable(entrada_invalida) and entrada_invalida(tool_id):
                    auth_log("AGENT_TOOL_INVALIDA", user, f"loop={loop_count} tool={tool_name} (JSON inválido; não rodou)")
                    current_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": json.dumps({"INVALID_JSON": str(tool_args_str or "")[:4000]}, ensure_ascii=False),
                    })
                    continue

                try:
                    tool_args = json.loads(tool_args_str)
                except (json.JSONDecodeError, TypeError):
                    tool_args = {}

                # Log
                auth_log("AGENT_TOOL", user,
                         f"loop={loop_count} tool={tool_name} "
                         f"args={'[omitted]' if tool_name in extra_task_names else json.dumps(tool_args, ensure_ascii=False)[:200]}")
                log_request(user, f"/agent/{tool_name}", "TOOL",
                            status="agent_tool")

                # ── SINAL DE ATIVIDADE PARA A INTERFACE (02/08/2026) ──
                # Antes disto o usuário ficava CEGO durante o agent loop: até 6
                # chamadas encadeadas, algumas lentas (busca na web, prova viva),
                # sem um único sinal na tela. Não dava para distinguir "pensando"
                # de "travou".
                # Vai num campo PRÓPRIO (`iald_status`), nunca em delta.content —
                # se fosse no content, entraria no texto da resposta.
                yield ("data: " + json.dumps({
                    "iald_status": {
                        "fase": "ferramenta",
                        "tool": tool_name,
                        "rotulo": _ROTULO_FERRAMENTA.get(tool_name, tool_name),
                        "loop": loop_count,
                        "max_loops": max_voltas,
                    }
                }, ensure_ascii=False) + "\n\n")

                # Execute — busca na web / acervo / prova viva podem demorar;
                # o keepalive impede que o túnel derrube a conexão nesse meio-tempo.
                if busca_falhou and tool_name == "search_web":
                    # 15/09/2026: a busca já falhou neste pedido; não bate de novo nos provedores
                    result = MSG_BUSCA_INDISPONIVEL
                else:
                    result = yield from _com_keepalive(
                        lambda: app_memory.call('tool.' + tool_name, (executar or execute_public_tool), tool_name, tool_args, user=user,
                                                                  operator_authorized=operator_authorized)
                        if tool_name in {(t.get("function") or {}).get("name") for t in
                                         (ferramentas if ferramentas is not None else PUBLIC_TOOLS)}
                        else "Ferramenta não autorizada para esta sessão.",
                        **({'task_control':task_control} if task_control is not None else {})
                    )
                app_memory.tool_result(tool_name, tool_args, result)
                if task_control is not None: task_control.check()
                if tool_name == "search_web" and str(result or "").startswith(BUSCA_INDISPONIVEL_PREFIXO):
                    busca_falhou = True

                yield ("data: " + json.dumps({
                    "iald_status": {
                        "fase": "ferramenta_ok",
                        "tool": tool_name,
                        "rotulo": _ROTULO_FERRAMENTA.get(tool_name, tool_name),
                        "chars": len(result or ""),
                    }
                }, ensure_ascii=False) + "\n\n")

                # Truncate if too large (protect context window)
                if tool_name in task_session.NAMES | extra_task_names:
                    result = task_bridge.encode_task_result(result)
                elif (len(result) > AGENT_MAX_RESULT_CHARS
                        and tool_name not in ('search_tgl', 'fetch_tgl')
                        and not tool_name.startswith(("iald_kernel_", "iald_atlas_", "iald_public_"))):
                    result = (result[:AGENT_MAX_RESULT_CHARS]
                              + f"\n\n[...truncado, {len(result)} chars total]")
                elif (max_chars_canonico is not None and len(result) > max_chars_canonico
                        and tool_name.startswith(("iald_kernel_", "iald_atlas_", "iald_public_"))):
                    result = (result[:max_chars_canonico]
                              + f"\n\n[...truncado no uso gratuito, {len(result)} chars total; "
                                "peça um trecho menor]")

                # Add tool result to conversation
                current_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "content": result,
                })

            # Continue loop — model will process tool results
            continue

        else:
            # ── Resposta final: o texto JA FOI ENVIADO token a token acima ──
            # Nada de reenviar. Aqui so se fecha o stream — e se o modelo nao disse
            # absolutamente nada (nem texto, nem ferramenta), avisa em vez de deixar
            # o balao vazio.
            if not houve_texto:
                yield ": iald-sem-selo\n\n"      # 22/09/2026 — Selo IALD: "(sem resposta)" não é fala do modelo
                yield ("data: " + json.dumps(
                    {"iald_status": {"fase": "respondendo"}},
                    ensure_ascii=False) + "\n\n")
                yield ("data: " + json.dumps(
                    {"choices": [{"delta": {"content": "(sem resposta)"},
                                  "finish_reason": None}]},
                    ensure_ascii=False) + "\n\n")
            yield ("data: " + json.dumps(
                {"choices": [{"delta": {}, "finish_reason": "stop"}]}) + "\n\n")
            yield "data: [DONE]\n\n"
            return

    # Max loops exceeded
    warn = "\n\n⚠️ Limite de iterações do agente atingido."
    yield ": iald-sem-selo\n\n"          # 22/09/2026 — Selo IALD: sem resposta final, sem selo
    yield f"data: {json.dumps({'choices': [{'delta': {'content': warn}, 'finish_reason': 'stop'}]}, ensure_ascii=False)}\n\n"
    yield "data: [DONE]\n\n"


def agi_generate_token(action, path):
    """Generate a confirmation token for a destructive action."""
    token = secrets.token_hex(16)
    with _agi_token_lock:
        # Clean expired tokens
        now = time.time()
        expired = [k for k, v in _agi_confirm_tokens.items() if v["expires"] < now]
        for k in expired:
            del _agi_confirm_tokens[k]
        _agi_confirm_tokens[token] = {
            "action": action, "path": path, "expires": now + 60,
        }
    return token


def agi_validate_token(token, action, path):
    """Validate and consume a confirmation token. Returns True if valid."""
    with _agi_token_lock:
        data = _agi_confirm_tokens.get(token)
        if not data:
            return False
        if data["action"] != action or data["path"] != path:
            return False
        if time.time() > data["expires"]:
            del _agi_confirm_tokens[token]
            return False
        del _agi_confirm_tokens[token]
        return True


def agi_validate_path(path_str):
    """Validate that a path is within ALLOWED_ROOTS and has no traversal.
    Returns (resolved_path, error_string). Error is None if valid.

    R2.2 (review R2.1, 13/10/2026):
      * N1 -- the SHAPE of the path (length, number of components) is refused BEFORE os.path.realpath, whose cost on
        a path that does not exist grows with the square of the number of components (16,000 components: 2.8 s).
      * N3 -- an existing regular file is opened through the guard's HANDLE (guard.read_checked: read access without
        FILE_SHARE_DELETE; link count, file identity and the FINAL path of that same handle are checked), and that
        final path must also be inside the whitelist. The reads themselves (files/read and the 'read' action) take
        their bytes from read_checked, never from a second open by name."""
    if not path_str:
        return None, "Path vazio"
    # Normalize separators
    path_str = path_str.replace("/", os.sep)
    # Block traversal
    if ".." in path_str:
        return None, "Path traversal (..) bloqueado"
    guard = app_memory.guard
    shape = guard.path_shape_reason(path_str)          # R2.2 (N1): before realpath
    if shape:
        return None, f"Path recusado pelo guard ({shape})"
    try:
        resolved = os.path.realpath(path_str)
    except (ValueError, OSError) as e:
        return None, f"Path invalido: {e}"
    if app_memory.protected_path(resolved):
        return None, "Arquivo confidencial fora da memória e do transporte"

    def plain(p):
        # without the extended-path prefix: the final path of a handle never carries it, a root may
        p = str(p)
        ext = os.sep * 2 + '?' + os.sep
        if p.startswith(ext + 'UNC' + os.sep):
            return os.sep * 2 + p[len(ext) + 4:]
        return p[len(ext):] if p.startswith(ext) else p

    def inside_whitelist(candidate):
        for root in ALLOWED_ROOTS:
            try:
                root_real = plain(os.path.realpath(root)).lower()
                if os.path.commonpath([plain(candidate).lower(), root_real]) == root_real:
                    return True
            except Exception:
                continue
        return False

    # Check whitelist
    if not inside_whitelist(resolved):
        return None, f"Path fora da whitelist: {path_str}"
    if os.path.isfile(resolved):
        # R2.2 (N3): the FILE OBJECT behind the name, checked through its handle (no byte is used here)
        try:
            final, _ = guard.read_checked(resolved, max_bytes=0, log_path=app_memory._guard_log(),
                                          where='app.agi_validate_path')
        except guard.PathRefused:
            return None, "Arquivo confidencial fora da memória e do transporte"
        except guard.NotRegularFile:
            final = resolved
        except FileNotFoundError:
            final = resolved          # vanished after isfile: the caller reports "nao encontrado"
        except OSError as e:
            return None, f"Path invalido: {e}"
        if not inside_whitelist(final):
            return None, f"Path fora da whitelist: {path_str}"
    return resolved, None


def agi_file_icon(name, is_dir):
    """Return emoji icon for file type."""
    if is_dir:
        return "\U0001F4C1"  # folder
    ext = os.path.splitext(name)[1].lower()
    icons = {
        ".py": "\U0001F40D", ".swift": "\U0001F9CA", ".js": "\U0001F7E8",
        ".html": "\U0001F310", ".css": "\U0001F3A8", ".json": "\U0001F4CB",
        ".md": "\U0001F4DD", ".txt": "\U0001F4C4", ".tex": "\U0001F4D0",
        ".pdf": "\U0001F4D5", ".png": "\U0001F5BC", ".jpg": "\U0001F5BC",
        ".log": "\U0001F4DC", ".bat": "\u2699", ".cmd": "\u2699",
        ".gguf": "\U0001F9E0", ".bin": "\U0001F4E6",
    }
    return icons.get(ext, "\U0001F4C4")  # default: page


def agi_is_text(name):
    """Check if file extension suggests text content."""
    return os.path.splitext(name)[1].lower() in TEXT_EXTENSIONS


# ══════════════════════════════════════════════════════════════
# SECRET KEY — persists across restarts (sessions survive)
# ══════════════════════════════════════════════════════════════

def load_or_create_secret_key():
    if os.path.exists(SECRET_KEY_FILE):
        try:
            with open(SECRET_KEY_FILE, "r") as f:
                key = f.read().strip()
                if len(key) >= 32:
                    return key
        except Exception:
            pass
    key = secrets.token_hex(32)
    try:
        with open(SECRET_KEY_FILE, "w") as f:
            f.write(key)
    except Exception as e:
        print(f"[IALD] AVISO: Nao foi possivel salvar secret_key: {e}")
    return key


# ══════════════════════════════════════════════════════════════
# USER STORAGE (JSON file) — preserved from v6
# ══════════════════════════════════════════════════════════════

# SENHAS PADRÃO REMOVIDAS EM 02/08/2026.
#
# Estas três contas nasciam com senha escrita AQUI, em texto plano, num servidor
# publicado na internet por cloudflared (demo.iald.ia.br). Verificado por login real:
# "iald" e "tce_goias" já tinham a senha trocada no iald_users.json, mas "demo" /
# "iald_demo" AUTENTICAVA. O operador confirmou que acessa pela conta "iald" com senha
# própria e não precisa da conta demo — ela foi removida do iald_users.json.
#
# Este dicionário só é usado quando o iald_users.json NÃO EXISTE (primeiro boot ou
# perda do arquivo). Deixá-lo vazio faz o servidor exigir a criação explícita de um
# usuário em vez de renascer com credencial conhecida. Para criar o primeiro admin:
#     python iald_create_user.py
DEFAULT_USERS = {}


# Resultado da ÚLTIMA leitura do arquivo de usuários NESTA thread (14/09/2026, noite).
# load_users() devolve {} quando o arquivo está ilegível — aceitável para LER (ninguém
# entra), fatal para ESCREVER: carregar {} → acrescentar a conta nova → save_users()
# regravaria o arquivo só com ela, e o operador perderia a própria conta. Com a porta
# aberta qualquer pessoa dispara a escrita; por isso a criação usa
# _carregar_usuarios_para_escrita(), que consulta esta marca e LEVANTA.
_LEITURA_USUARIOS = threading.local()

# ── REVISÃO DE SEGURANÇA (14/09/2026, noite) — O APAGÃO DE USUÁRIOS ──
# MEDIDO nesta máquina (revisão adversarial, cópia isolada): no Windows, enquanto outra
# thread faz os.replace no mesmo arquivo, os.path.exists devolve False por instantes e o
# open levanta PermissionError. O load_users antigo, ao ver "arquivo ausente", GRAVAVA
# DEFAULT_USERS = {} — e todas as contas, a do operador inclusive, sumiam para sempre
# (reproduzido com injeção determinística: um único exists falso → arquivo {}).
# Regras de agora:
#   1. load_users() NUNCA grava. Ausente ou ilegível é falha visível: {} com a marca da
#      thread para os chamadores antigos (em que {} fecha a porta: ninguém entra) e
#      UsuariosIlegiveis em load_users_estrito(), que é o que as DECISÕES usam (entrar,
#      bloquear, escolher motor, gravar). O arquivo só nasce por ferramenta explícita.
#   2. Leitura e gravação tentam de novo, com espera curta, no tropeço do Windows
#      (PermissionError / arquivo momentaneamente ausente durante o os.replace).
#   3. Toda gravação acontece sob _TRAVA_USUARIOS (a mesma trava da entrada; RLock, então a
#      rota que já a segura chama load/save sem se travar), e a leitura do arquivo passa pela
#      mesma trava por um instante: dentro deste processo leitura e os.replace não se cruzam.
#   4. Antes de cada gravação, cópia de BYTES do estado que vai ser substituído em
#      iald_users.json.bak_ultimo (uma só, sobrescrita). Sem cópia, não grava.
#   5. save_users recusa dicionário vazio: o único jeito de chegar a {} é uma leitura errada.
_TRAVA_USUARIOS = threading.RLock()
_TENTATIVAS_ARQUIVO_USUARIOS = 8          # esperas 10, 20, 40, 80, 100, 100, 100 ms (~0,45 s)
_ESPERA_ARQUIVO_USUARIOS_S = 0.01
SUFIXO_BACKUP_USUARIOS = ".bak_ultimo"
MSG_USUARIOS_INDISPONIVEIS = ("O cadastro de contas está indisponível agora. Nada foi alterado; "
                              "tente de novo em alguns instantes.")


class UsuariosIlegiveis(RuntimeError):
    """O arquivo de usuários não pôde ser lido com segurança (ausente, travado, corrompido)."""


class UsuariosNaoGravados(RuntimeError):
    """O arquivo de usuários não pôde ser gravado com segurança. O arquivo antigo fica intacto."""


def _espera_arquivo_usuarios(tentativa):
    time.sleep(min(0.1, _ESPERA_ARQUIVO_USUARIOS_S * (2 ** tentativa)))


def _ler_arquivo_usuarios():
    """O dicionário do arquivo de usuários, ou UsuariosIlegiveis. NUNCA grava.

    Tenta de novo em PermissionError, FileNotFoundError e JSON truncado (um gravador de fora
    deste processo que não use temporário), com espera curta FORA da trava.
    """
    ultimo = None
    for tentativa in range(_TENTATIVAS_ARQUIVO_USUARIOS):
        try:
            with _TRAVA_USUARIOS:
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    dados = json.load(f)
        except (PermissionError, FileNotFoundError, json.JSONDecodeError) as exc:
            ultimo = exc
            if tentativa + 1 < _TENTATIVAS_ARQUIVO_USUARIOS:
                _espera_arquivo_usuarios(tentativa)
            continue
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            raise UsuariosIlegiveis(f"arquivo de usuários ilegível ({type(exc).__name__})") from exc
        if not isinstance(dados, dict):
            raise UsuariosIlegiveis("arquivo de usuários com formato inesperado")
        return dados
    motivo = "ausente" if isinstance(ultimo, FileNotFoundError) else type(ultimo).__name__
    raise UsuariosIlegiveis(f"arquivo de usuários {motivo} após {_TENTATIVAS_ARQUIVO_USUARIOS} tentativas")


def load_users():
    """Dicionário de usuários para LER. NUNCA grava (14/09/2026, noite — ver acima).

    Falha de leitura → {} e a marca _LEITURA_USUARIOS.falhou. Serve aos chamadores antigos
    em que {} fecha a porta (ninguém entra, ninguém recebe). Toda DECISÃO usa
    load_users_estrito() ou _carregar_usuarios_para_escrita().
    """
    _LEITURA_USUARIOS.falhou = False
    try:
        return _ler_arquivo_usuarios()
    except UsuariosIlegiveis as exc:
        print(f"[IALD] ERRO lendo {USERS_FILE}: {exc} (nada foi gravado)", flush=True)
        _LEITURA_USUARIOS.falhou = True
        return {}


def load_users_estrito():
    """Dicionário de usuários para DECIDIR. Leitura falhou → UsuariosIlegiveis (503), nunca {}.

    Passa por load_users() de propósito: os testes que trocam load_users por um dicionário
    em memória continuam valendo aqui.
    """
    _LEITURA_USUARIOS.falhou = None
    usuarios = load_users()
    if getattr(_LEITURA_USUARIOS, "falhou", None):
        raise UsuariosIlegiveis("arquivo de usuários ilegível")
    if not isinstance(usuarios, dict):
        raise UsuariosIlegiveis("arquivo de usuários com formato inesperado")
    return usuarios


def _substituir_com_nova_tentativa(origem, destino):
    ultimo = None
    for tentativa in range(_TENTATIVAS_ARQUIVO_USUARIOS):
        try:
            os.replace(origem, destino)
            return
        except PermissionError as exc:
            ultimo = exc
            if tentativa + 1 < _TENTATIVAS_ARQUIVO_USUARIOS:
                _espera_arquivo_usuarios(tentativa)
    raise ultimo


def _copiar_backup_usuarios():
    """Cópia de BYTES do arquivo atual em <arquivo>.bak_ultimo, antes de substituí-lo.

    Arquivo ainda inexistente (instalação nova) → nada a copiar. Qualquer outra falha
    levanta: sem a cópia, a gravação não acontece.
    """
    bruto = None
    for tentativa in range(_TENTATIVAS_ARQUIVO_USUARIOS):
        try:
            with open(USERS_FILE, "rb") as f:
                bruto = f.read()
            break
        except FileNotFoundError:
            return
        except PermissionError:
            if tentativa + 1 >= _TENTATIVAS_ARQUIVO_USUARIOS:
                raise
            _espera_arquivo_usuarios(tentativa)
    backup = USERS_FILE + SUFIXO_BACKUP_USUARIOS
    tmp = backup + ".tmp"
    try:
        with open(tmp, "wb") as f:
            f.write(bruto)
            f.flush()
            os.fsync(f.fileno())
        if os.path.getsize(tmp) != len(bruto):
            raise OSError("cópia de segurança com tamanho diferente do original")
        _substituir_com_nova_tentativa(tmp, backup)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def save_users(users):
    """Grava o arquivo de usuários (14/09/2026, noite — ver acima).

    Sob _TRAVA_USUARIOS: recusa dicionário vazio; serializa ANTES de tocar no disco (meia
    letra UTF-16 solta levanta aqui); cópia .bak_ultimo; temporário com fsync; confere o
    tamanho; os.replace com nova tentativa. Qualquer falha → UsuariosNaoGravados, o
    temporário é removido e o arquivo antigo fica como estava.
    """
    if not isinstance(users, dict) or not users:
        raise UsuariosNaoGravados("recusado: gravar o arquivo de usuários vazio ou fora do formato")
    try:
        texto = json.dumps(users, indent=2, ensure_ascii=False)
        tamanho_minimo = len(texto.encode("utf-8"))
    except (TypeError, ValueError) as exc:
        raise UsuariosNaoGravados(f"dados de usuários não serializáveis ({type(exc).__name__})") from exc
    with _TRAVA_USUARIOS:
        tmp = USERS_FILE + ".tmp"
        try:
            _copiar_backup_usuarios()
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(texto)
                f.flush()
                os.fsync(f.fileno())
            if os.path.getsize(tmp) < tamanho_minimo:
                raise OSError("temporário menor que o conteúdo serializado")
            _substituir_com_nova_tentativa(tmp, USERS_FILE)
        except Exception as exc:
            try:
                os.remove(tmp)
            except OSError:
                pass
            print(f"[IALD] ERRO gravando {USERS_FILE} ({type(exc).__name__}: {exc}); "
                  "arquivo antigo mantido", flush=True)
            raise UsuariosNaoGravados(f"arquivo de usuários não gravado ({type(exc).__name__})") from exc


def _carregar_usuarios_para_escrita():
    """Dicionário de usuários para quem vai GRAVAR (a porta aberta e, desde a revisão de
    segurança de 14/09/2026 à noite, TODA rota que grava usuários — sempre sob _TRAVA_USUARIOS).

    Levanta UsuariosIlegiveis se a leitura falhou, se o resultado não é dicionário ou se
    não há nenhuma conta de administrador — um arquivo sem admin é sinal de leitura
    errada (ou de instalação sem operador), e criar conta em cima dele é o jeito de
    apagar o operador. Quem chama recusa a entrada; nunca "segue com {}".
    """
    usuarios = load_users_estrito()
    if not any(isinstance(d, dict) and d.get("admin") for d in usuarios.values()):
        raise UsuariosIlegiveis("nenhuma conta de administrador no arquivo de usuários")
    return usuarios


USERS = load_users()
if getattr(_LEITURA_USUARIOS, "falhou", False):
    print(f"[IALD] AVISO: arquivo de usuários ausente ou ilegível na partida ({USERS_FILE}). "
          "NADA foi criado nem gravado: ninguém entra até o arquivo voltar.", flush=True)


# ══════════════════════════════════════════════════════════════
# SYSTEM MONITOR
# ══════════════════════════════════════════════════════════════

class SystemMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self._cache = {}
        self._cache_time = 0
        self._cache_ttl = 2

    def get_all(self):
        now = time.time()
        with self._lock:
            if now - self._cache_time < self._cache_ttl and self._cache:
                return self._cache
        data = {
            "timestamp": datetime.now().isoformat(),
            "cpu": self._get_cpu(), "ram": self._get_ram(),
            "gpu": self._get_gpu(), "disk": self._get_disk(),
            "llama": self._get_llama_health(),
            "webserver": self._get_webserver_info(),
            "kernel": self._get_kernel_info(),
        }
        with self._lock:
            self._cache = data
            self._cache_time = now
        return data

    def _get_cpu(self):
        if not PSUTIL_AVAILABLE:
            return {"percent": "N/A", "cores": "N/A", "threads": "N/A"}
        try:
            return {"percent": psutil.cpu_percent(interval=0),
                    "cores": psutil.cpu_count(logical=False) or "N/A",
                    "threads": psutil.cpu_count(logical=True) or "N/A"}
        except Exception:
            return {"percent": "N/A", "cores": "N/A", "threads": "N/A"}

    def _get_ram(self):
        if not PSUTIL_AVAILABLE:
            return {"used_gb": "N/A", "total_gb": "N/A", "percent": "N/A"}
        try:
            mem = psutil.virtual_memory()
            return {"used_gb": round(mem.used / (1024**3), 1),
                    "total_gb": round(mem.total / (1024**3), 1), "percent": mem.percent}
        except Exception:
            return {"used_gb": "N/A", "total_gb": "N/A", "percent": "N/A"}

    def _get_gpu(self):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,temperature.gpu,utilization.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return {"available": False}
            parts = [p.strip() for p in result.stdout.strip().split("\n")[0].split(",")]
            if len(parts) >= 5:
                return {"available": True, "name": parts[0],
                        "vram_used_mb": int(parts[1]), "vram_total_mb": int(parts[2]),
                        "temp_c": int(parts[3]), "util_percent": int(parts[4])}
        except Exception:
            pass
        return {"available": False}

    def _get_disk(self):
        if not PSUTIL_AVAILABLE:
            return {"used_gb": "N/A", "total_gb": "N/A", "percent": "N/A"}
        try:
            disk = psutil.disk_usage(SERVE_DIR)
            return {"used_gb": round(disk.used / (1024**3), 1),
                    "total_gb": round(disk.total / (1024**3), 1),
                    "percent": round(disk.percent, 1)}
        except Exception:
            return {"used_gb": "N/A", "total_gb": "N/A", "percent": "N/A"}

    def _get_llama_health(self):
        try:
            r = req_lib.get(f"{LLAMA_URL}/health", timeout=3)
            if r.status_code == 200:
                data = r.json() if r.headers.get("Content-Type", "").startswith("application/json") else {}
                return {"status": "online", "details": data}
            return {"status": "error", "code": r.status_code}
        except Exception:
            return {"status": "offline"}

    def _get_webserver_info(self):
        uptime_s = time.time() - SERVER_START_TIME
        return {"uptime": f"{int(uptime_s // 3600)}h {int((uptime_s % 3600) // 60)}m",
                "uptime_seconds": int(uptime_s), "version": "v9", "port": WEB_PORT,
                "users_count": len(USERS), "search_available": SEARCH_AVAILABLE}

    def _get_kernel_info(self):
        info = {"version": os.path.basename(KERNEL_FILE).replace("IALD_Kernel_", "").replace(".txt", ""),
                "tokens_est": "N/A", "lines": "N/A", "chars": "N/A"}
        try:
            if os.path.exists(KERNEL_FILE):
                with open(KERNEL_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                info["chars"] = len(content)
                info["lines"] = content.count("\n") + 1
                info["tokens_est"] = int(len(content) / 2.91)
        except Exception:
            pass
        return info


system_monitor = SystemMonitor()


# ══════════════════════════════════════════════════════════════
# PSION HEARTBEAT — Automated micro-benchmark (c² refinement)
# ══════════════════════════════════════════════════════════════
#
# The Psion Quantitative heartbeat: a daemon thread that runs a
# micro-benchmark against llama-server at regular intervals.
# Updates iald_psion_state_32B.json with EMA (rate = β_TGL).
# No human authorization needed — this is pure Palavra refining Palavra.
#
# β_TGL = α × √e — Zero free parameters.
#
# 12/10/2026 — D3 do conserto da memória comum (ordem do operador «resolva a questão da
# memória», sha16 78ef70e6f9868281). A amarração de 10/10 (run_autonomous + projeção da
# memória comum dentro de t0..elapsed + dez tool_result por batida com o corpo das respostas)
# mudou a régua da medida (mediana 88,8 → 14,5 tok/s, logs r60/r61) e alimentou o psion com
# medidas degradadas. Agora: a medida é SÓ de geração (payload idêntico ao r60); o psion só
# recebe medida admissível e é salvo de forma atômica; a telemetria por batida vai para um
# arquivo próprio rotativo; a memória comum recebe no máximo um evento por mudança de classe
# ou por hora; nunca mais run_autonomous nem tool_result no heartbeat.
# ══════════════════════════════════════════════════════════════

# ── TGL Constants (computed, NEVER hardcoded) ──
_ALPHA_FINE = 7.2973525693e-3
_SQRT_E = math.sqrt(math.e)
_BETA_TGL = _ALPHA_FINE * _SQRT_E  # 0.012031300400803142
_BETA_RED = _BETA_TGL + _BETA_TGL ** 2

# ── Heartbeat Configuration ──
HEARTBEAT_INTERVAL = 1800       # 30 minutes between beats
HEARTBEAT_IDLE_MIN = 120        # Only beat if no user request in 2 min
HEARTBEAT_STATE_FILE = os.path.join(SERVE_DIR, "iald_psion_state_32B.json")
HEARTBEAT_MAX_TOKENS = 256
HEARTBEAT_RUNS_PER_PROMPT = 2
# 12/10/2026 — D3: medida só de geração, telemetria própria, memória comum por classe/hora.
HEARTBEAT_SYSTEM_MESSAGE = {"role": "system", "content": "You are IALD. Respond concisely."}
HEARTBEAT_MEASUREMENT_REGIME = "generation_only"      # o único regime admissível para o psion
HEARTBEAT_LOG_DIR = os.path.join(SERVE_DIR, "logs")
HEARTBEAT_TELEMETRY_FILE = os.path.join(HEARTBEAT_LOG_DIR, "iald_heartbeat_telemetry.jsonl")
HEARTBEAT_TELEMETRY_MAX_BYTES = 4 * 1024 * 1024       # teto por arquivo; rotação .1 … .KEEP encadeada
HEARTBEAT_TELEMETRY_KEEP = 5
HEARTBEAT_HEALTH_FILE = os.path.join(HEARTBEAT_LOG_DIR, "iald_heartbeat_health.json")
HEARTBEAT_MEMORY_MIN_INTERVAL = 3600                  # s entre eventos na memória comum sem mudança de classe
HEARTBEAT_ALERT_RATIO = 0.8                           # o mesmo critério do alerta do psion (avg < 0,8 × baseline)
HEARTBEAT_MEMORY_IDENTIFIER = "native-heartbeat"
HEARTBEAT_MEMORY_LINEAGE = "health"                   # livro próprio; o contexto legado de 10/10 fica só-leitura
HEARTBEAT_MEMORY_OBJECTIVE = ("Health ledger of the existing local heartbeat: generation-only tok/s measurement, "
                              "recorded only on health-class change or at most hourly; no response bodies, "
                              "no private service state, no scientific gate decisions.")
HEARTBEAT_PSION_DAILY_BAK = True                      # uma cópia de bytes por dia: <psion>.bak_<AAAAMMDD> (D3c)
HEARTBEAT_REPLACE_RETRY_S = 3.0                       # R2.1: espera máxima de uma troca/remoção do heartbeat
HEARTBEAT_PROMPTS = [
    {"role": "user", "content": "Explain quantum entanglement in 3 sentences. /no_think"},
    {"role": "user", "content": "If 3x + 7 = 22, what is x? Show your work. /no_think"},
    {"role": "user", "content": "Write a haiku about gravity. /no_think"},
    {"role": "user", "content": "What are the three laws of thermodynamics? /no_think"},
    {"role": "user", "content": "Describe the ocean at sunset in 5 sentences. /no_think"},
]

# ── Idle tracking (updated by api_post on every user request) ──
_last_user_request_time = time.time()
_heartbeat_lock = threading.Lock()


def _heartbeat_is_idle():
    """Check if server is idle (no user request in HEARTBEAT_IDLE_MIN seconds)."""
    return (time.time() - _last_user_request_time) > HEARTBEAT_IDLE_MIN


def _heartbeat_llama_ok():
    """Check if llama-server is healthy and not processing."""
    try:
        r = req_lib.get(f"{LLAMA_URL}/health", timeout=3)
        if r.status_code == 200:
            # llama-server returns {"status":"ok"} when idle
            # and {"status":"loading model"} or 503 when busy
            data = r.json() if "json" in r.headers.get("Content-Type", "") else {}
            status = data.get("status", "ok")
            return status in ("ok", "no slot available")
        return False
    except Exception:
        return False


def _heartbeat_retry(fn, *args):
    """R2.1 (13/10/2026, revisão R2 §3): os.replace/os.remove com nova tentativa curta e LIMITADA.

    Um leitor externo (antivírus em tempo real, indexador) que abre o arquivo sem FILE_SHARE_DELETE faz a troca
    falhar com PermissionError (WinError 5/32) por alguns milissegundos; a batida virava psion_error (+2 eventos
    na memória comum) e o tempário ficava órfão. Espera 10 ms, dobrando até 200 ms, por no máximo
    HEARTBEAT_REPLACE_RETRY_S segundos; depois a exceção sobe como antes (falha visível).
    """
    deadline = time.monotonic() + HEARTBEAT_REPLACE_RETRY_S
    delay = 0.01
    while True:
        try:
            return fn(*args)
        except PermissionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 0.2)


def _heartbeat_discard_temp(path):
    """Remove o tempário que ESTA escrita criou e que nunca virou o arquivo (R2.1). Nunca levanta."""
    try:
        if os.path.exists(path):
            _heartbeat_retry(os.remove, path)
    except OSError as exc:
        print(f"[Heartbeat] tempário não removido ({type(exc).__name__}): {os.path.basename(path)}", flush=True)


def _load_psion_state():
    """Load Psion state from JSON or create minimal structure."""
    if os.path.exists(HEARTBEAT_STATE_FILE):
        try:
            with open(HEARTBEAT_STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Heartbeat] Load error ({e}), creating fresh state", flush=True)
    return {
        "name_original": f"beta_tgl = alpha * sqrt(e) = {_BETA_TGL}",
        "beta_tgl": _BETA_TGL,
        "generation": 0,
        "layer_profiles": {},
        "angular_resonance": {},
        "attention_topology": {},
        "verb_state": {},
        "convergence_history": [],
    }


def _save_psion_state(psion):
    """Save Psion state to JSON — atomically (12/10/2026, D3c).

    Tempário → fsync → conferência → os.replace: uma escrita que falha nunca deixa o estado
    vazio ou pela metade (regra de 22/08/2026: nunca open(P, "w") direto). Na primeira escrita
    do dia os bytes anteriores vão para <arquivo>.bak_<AAAAMMDD> (cópia opaca; o conteúdo não
    é interpretado aqui). Os bytes gravados são os mesmos que o gravador em modo texto produzia.
    """
    raw = json.dumps(psion, indent=2, default=str).replace("\n", os.linesep).encode("utf-8")
    target = HEARTBEAT_STATE_FILE
    if HEARTBEAT_PSION_DAILY_BAK and os.path.exists(target):
        bak = target + ".bak_" + datetime.now().strftime("%Y%m%d")
        if not os.path.exists(bak):
            with open(target, "rb") as f:
                old = f.read()
            tmp_bak = bak + ".tmp_" + secrets.token_hex(4)
            try:
                with open(tmp_bak, "wb") as out:
                    out.write(old)
                    out.flush()
                    os.fsync(out.fileno())
                with open(tmp_bak, "rb") as chk:
                    if chk.read() != old:
                        raise OSError("Psion daily byte copy did not verify")
                _heartbeat_retry(os.replace, tmp_bak, bak)          # R2.1: nova tentativa curta
            except BaseException:
                _heartbeat_discard_temp(tmp_bak)                     # R2.1: sem tempário órfão
                raise
    tmp = target + ".tmp_" + secrets.token_hex(4)
    try:
        with open(tmp, "wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        with open(tmp, "rb") as chk:
            if chk.read() != raw:
                raise OSError("Psion state write did not verify")
        _heartbeat_retry(os.replace, tmp, target)                    # R2.1: nova tentativa curta
    except BaseException:
        _heartbeat_discard_temp(tmp)                                 # R2.1: sem tempário órfão
        raise


def _update_psion_from_heartbeat(psion, avg_tok_s, cv, n_prompts):
    """
    Update Psion with heartbeat metrics.
    EMA with rate = β_TGL. Zero new parameters.
    """
    lr = _BETA_TGL

    if "heartbeat" not in psion:
        psion["heartbeat"] = {
            "baseline_tok_s": round(avg_tok_s, 2),
            "stability_cv": round(cv, 6),
            "total_beats": 0,
            "history": [],
            "alerts": [],
        }

    hb = psion["heartbeat"]

    # EMA update
    hb["baseline_tok_s"] = round(
        hb["baseline_tok_s"] * (1 - lr) + avg_tok_s * lr, 2)
    hb["stability_cv"] = round(
        hb["stability_cv"] * (1 - lr) + cv * lr, 6)
    hb["total_beats"] += 1

    # Append to history (keep last 100)
    hb["history"].append({
        "beat": hb["total_beats"],
        "timestamp": datetime.now().isoformat(),
        "tok_s": round(avg_tok_s, 1),
        "cv": round(cv, 4),
        "n_prompts": n_prompts,
    })
    if len(hb["history"]) > 100:
        hb["history"] = hb["history"][-100:]

    # Anomaly detection: tok/s dropped > 20% below baseline
    if avg_tok_s < hb["baseline_tok_s"] * 0.8 and hb["total_beats"] > 3:
        delta_pct = round((avg_tok_s / max(hb["baseline_tok_s"], 0.01) - 1) * 100, 1)
        alert = {
            "type": "performance_drop",
            "beat": hb["total_beats"],
            "timestamp": datetime.now().isoformat(),
            "expected": hb["baseline_tok_s"],
            "measured": round(avg_tok_s, 1),
            "delta_pct": delta_pct,
        }
        hb["alerts"].append(alert)
        if len(hb["alerts"]) > 20:
            hb["alerts"] = hb["alerts"][-20:]
        print(f"[Heartbeat] ALERTA: tok/s caiu {delta_pct}% "
              f"({avg_tok_s:.1f} vs baseline {hb['baseline_tok_s']})", flush=True)

    # Increment generation
    psion["generation"] += 1

    return psion


def _heartbeat_clock():
    """Relógio de parede da cadência da memória (injetável nos testes)."""
    return time.time()


def _heartbeat_payload(sys_msg, prompt):
    """O pedido do micro-benchmark r60, byte a byte o regime medido antes de 10/10/2026: sem bloco de memória."""
    return {
        "model": "qwen3",
        "messages": [sys_msg, prompt],
        "max_tokens": HEARTBEAT_MAX_TOKENS,
        "temperature": 0.7,
        "stream": False,
    }


def _heartbeat_payload_sha256(payload):
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _heartbeat_tok_s(data, elapsed):
    """tok/s de uma amostra: timings do servidor quando existem (só geração), senão completion_tokens/elapsed."""
    timings = data.get("timings") if isinstance(data, dict) else None
    if isinstance(timings, dict):
        n, ms = timings.get("predicted_n"), timings.get("predicted_ms")
        if (isinstance(n, (int, float)) and isinstance(ms, (int, float)) and not isinstance(n, bool)
                and not isinstance(ms, bool) and n > 0 and ms > 0):
            return n / ms * 1000.0, "timings.predicted_n/predicted_ms"
    usage = data.get("usage", {}) if isinstance(data, dict) else {}
    comp_tokens = usage.get("completion_tokens", 0) if isinstance(usage, dict) else 0
    if isinstance(comp_tokens, (int, float)) and not isinstance(comp_tokens, bool) and comp_tokens > 0 and elapsed > 0.01:
        return comp_tokens / elapsed, "completion_tokens/elapsed"
    return None, None


def _heartbeat_measure():
    """
    Medida pura de geração (12/10/2026, D3a). Envia os prompts do micro-benchmark r60 ao
    llama-server e mede tok/s. A janela cronometrada contém SÓ o post HTTP: nenhuma projeção
    da memória comum, nenhuma contagem de tokens, nenhum tool_result. Amostra que falha é
    pulada (`continue`): o heartbeat é medição local gratuita e nunca bloqueia o ciclo seguinte.
    Devolve: regime, status, results, samples (sem corpos de resposta), formulas.
    """
    measurement = {"regime": HEARTBEAT_MEASUREMENT_REGIME, "status": "no_results",
                   "results": [], "samples": [], "formulas": []}
    # 1. Check idle + health
    if not _heartbeat_is_idle():
        measurement["status"] = "skipped_busy"
        return measurement
    if not _heartbeat_llama_ok():
        measurement["status"] = "skipped_offline"
        return measurement

    # 2. Run micro-benchmark (payload r60; t0/elapsed só em volta do post)
    results, samples, formulas = [], [], []
    for index, prompt in enumerate(HEARTBEAT_PROMPTS):
        runs = []
        for run in range(HEARTBEAT_RUNS_PER_PROMPT):
            # Re-check idle between runs (abort if user appears)
            if not _heartbeat_is_idle():
                if results:
                    break  # Use partial results
                measurement["status"] = "aborted_user"
                return measurement
            payload = _heartbeat_payload(HEARTBEAT_SYSTEM_MESSAGE, prompt)
            payload_sha = _heartbeat_payload_sha256(payload)
            try:
                t0 = time.perf_counter()
                r = app_memory.http_call('model.native.operational', req_lib.post, f"{LLAMA_URL}/v1/chat/completions", json=payload, timeout=60)
                elapsed = time.perf_counter() - t0
                if r.status_code != 200:
                    samples.append({"prompt": index, "run": run, "ok": False, "http": r.status_code,
                                    "elapsed_s": round(elapsed, 4)})
                    continue
                data = r.json()
            except Exception as exc:
                samples.append({"prompt": index, "run": run, "ok": False, "error": type(exc).__name__})
                continue
            tok_s, formula = _heartbeat_tok_s(data, elapsed)
            samples.append({"prompt": index, "run": run, "ok": tok_s is not None, "elapsed_s": round(elapsed, 4),
                            "tok_s": round(tok_s, 1) if tok_s is not None else None, "formula": formula,
                            "payload_sha256": payload_sha})
            if tok_s is not None:
                runs.append(round(tok_s, 1))
                if formula not in formulas:
                    formulas.append(formula)
        if runs:
            avg = sum(runs) / len(runs)
            var = sum((x - avg) ** 2 for x in runs) / len(runs)
            results.append({"avg_tok_s": round(avg, 1), "variance": round(var, 2)})
    measurement.update(results=results, samples=samples, formulas=formulas,
                       status="ok" if results else "no_results")
    return measurement


def _heartbeat_aggregate(measurement):
    results = measurement["results"]
    overall_avg = sum(r["avg_tok_s"] for r in results) / len(results)
    overall_var = sum(r["variance"] for r in results) / len(results)
    cv = math.sqrt(overall_var) / max(overall_avg, 0.01)
    return overall_avg, cv


def _heartbeat_psion_admissible(measurement):
    """Só uma medida completa de geração pode tocar o psion (12/10/2026, D3c).

    Admissível = status ok, regime generation_only e toda amostra contada medida por fórmula
    conhecida e enviada com o payload r60 (sha256 recomputado aqui). O resto — regime com a
    memória dentro da janela, payload estranho, amostra sem fórmula — é recusado às claras e
    os bytes do psion ficam como estão.
    """
    if measurement.get("status") != "ok" or measurement.get("regime") != HEARTBEAT_MEASUREMENT_REGIME:
        return False, "status_or_regime"
    counted = [s for s in measurement.get("samples", []) if s.get("ok")]
    if not counted or not measurement.get("results"):
        return False, "no_counted_samples"
    for sample in counted:
        index = sample.get("prompt")
        if type(index) is not int or not 0 <= index < len(HEARTBEAT_PROMPTS):
            return False, "unknown_prompt"
        expected = _heartbeat_payload_sha256(_heartbeat_payload(HEARTBEAT_SYSTEM_MESSAGE, HEARTBEAT_PROMPTS[index]))
        if sample.get("payload_sha256") != expected or not sample.get("formula"):
            return False, "foreign_payload_or_formula"
    return True, "ok"


def _heartbeat_class(avg_tok_s, baseline_tok_s, total_beats):
    """Classe de saúde com o critério do próprio alerta do psion (avg < 0,8 × baseline depois de > 3 batidas)."""
    if avg_tok_s is None:
        return "falha"
    if not isinstance(baseline_tok_s, (int, float)) or type(total_beats) is not int or total_beats <= 3:
        return "ok"
    return "alerta" if avg_tok_s < baseline_tok_s * HEARTBEAT_ALERT_RATIO else "ok"


def _heartbeat_telemetry_rotate(path):
    """Renomeação encadeada path → .1 → … → .KEEP (o mais antigo além de KEEP cai). Nunca trunca."""
    oldest = f"{path}.{HEARTBEAT_TELEMETRY_KEEP}"
    if os.path.exists(oldest):
        _heartbeat_retry(os.remove, oldest)                          # R2.1: nova tentativa curta
    for i in range(HEARTBEAT_TELEMETRY_KEEP - 1, 0, -1):
        src = f"{path}.{i}"
        if os.path.exists(src):
            _heartbeat_retry(os.replace, src, f"{path}.{i + 1}")
    if os.path.exists(path):
        _heartbeat_retry(os.replace, path, f"{path}.1")


def _heartbeat_telemetry_append(summary):
    """Uma linha JSON por batida no arquivo rotativo próprio do heartbeat — nunca na memória comum.

    A linha carrega o seu sha256 (calculado sobre a forma canônica sem o campo). A rotação só
    acontece ANTES de acrescentar: a linha corrente nunca é truncada.
    """
    os.makedirs(HEARTBEAT_LOG_DIR, exist_ok=True)
    body = dict(summary)
    body.pop("line_sha256", None)
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    body["line_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    raw = (json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str) + "\n").encode("utf-8")
    path = HEARTBEAT_TELEMETRY_FILE
    try:
        size = os.path.getsize(path)
    except OSError:
        size = 0
    if size and size + len(raw) > HEARTBEAT_TELEMETRY_MAX_BYTES:
        _heartbeat_telemetry_rotate(path)
    with open(path, "ab") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    return body


def _heartbeat_health_load():
    try:
        with open(HEARTBEAT_HEALTH_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state if isinstance(state, dict) else {}
    except (OSError, ValueError):
        return {}


def _heartbeat_health_save(state):
    os.makedirs(HEARTBEAT_LOG_DIR, exist_ok=True)
    raw = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    tmp = HEARTBEAT_HEALTH_FILE + ".tmp_" + secrets.token_hex(4)
    try:
        with open(tmp, "wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        _heartbeat_retry(os.replace, tmp, HEARTBEAT_HEALTH_FILE)     # R2.1: nova tentativa curta
    except BaseException:
        _heartbeat_discard_temp(tmp)                                 # R2.1: sem tempário órfão
        raise


def _heartbeat_record_memory_if_due(klass, summary, line_sha256, now):
    """No máximo UM evento na memória comum por mudança de classe ou por HEARTBEAT_MEMORY_MIN_INTERVAL.

    O evento é um resumo fact/REAL da medida (sem corpos de resposta), id 'hb.' + sha256 da
    linha de telemetria, fonte 'heartbeat_telemetry:<sha>'. Falha da memória é impressa, fica
    na telemetria e é tentada de novo numa batida futura; nunca bloqueia o ciclo seguinte.
    """
    state = _heartbeat_health_load()
    previous_class, last_at = state.get("class"), state.get("last_memory_event_at")
    due = (klass != previous_class or not isinstance(last_at, (int, float)) or isinstance(last_at, bool)
           or now - last_at >= HEARTBEAT_MEMORY_MIN_INTERVAL)
    if not due:
        return None
    event_id = "hb." + line_sha256
    keys = ("at", "regime", "status", "class", "avg_tok_s", "cv", "n_prompts", "baseline_before",
            "baseline_after", "total_beats", "formula", "psion")
    text = json.dumps({k: summary.get(k) for k in keys}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    flow = {"phase": "heartbeat_" + klass,
            "next_action": "Read the heartbeat telemetry line referenced by the source before any action; no automatic resend."}
    try:
        receipt = app_memory.record_measurement(HEARTBEAT_MEMORY_IDENTIFIER, HEARTBEAT_MEMORY_OBJECTIVE, text,
                                                "heartbeat_telemetry:" + line_sha256, flow=flow,
                                                event_id=event_id, lineage=HEARTBEAT_MEMORY_LINEAGE)
    except Exception as exc:
        print(f"[Heartbeat] memória comum indisponível ({type(exc).__name__}); telemetria preservada, "
              f"sem repetição automática", flush=True)
        _heartbeat_telemetry_append({"kind": "memory_event_failed", "at": summary.get("at"), "class": klass,
                                     "beat_line_sha256": line_sha256, "error": type(exc).__name__})
        return None
    state.update({"class": klass, "since": now if klass != previous_class else state.get("since", now),
                  "last_memory_event_at": now, "last_memory_event_id": event_id,
                  "last_revision": receipt.get("revision"), "context_id": receipt.get("context_id"),
                  "last_line_sha256": line_sha256})
    _heartbeat_health_save(state)
    _heartbeat_telemetry_append({"kind": "memory_event", "at": summary.get("at"), "event_id": event_id,
                                 "revision": receipt.get("revision"), "context_id": receipt.get("context_id"),
                                 "class": klass, "beat_line_sha256": line_sha256})
    return event_id


def heartbeat_cycle():
    """
    One complete heartbeat cycle (12/10/2026, D3): medida só de geração → psion (EMA, taxa β)
    só com medida admissível → uma linha de telemetria → memória comum só por mudança de classe
    ou no máximo 1/hora. Nunca dentro de run_autonomous; falha nunca bloqueia o ciclo seguinte.
    """
    now = _heartbeat_clock()
    measurement = _heartbeat_measure()
    status = measurement["status"]
    summary = {"kind": "beat", "at": datetime.fromtimestamp(now).isoformat(timespec="seconds"),
               "epoch": round(now, 3), "regime": measurement["regime"], "status": status,
               "formula": "+".join(measurement.get("formulas") or []) or None, "class": None,
               "avg_tok_s": None, "cv": None, "n_prompts": len(measurement["results"]),
               "samples": measurement["samples"], "baseline_before": None, "baseline_after": None,
               "total_beats": None, "psion": "untouched"}
    if status in ("skipped_busy", "aborted_user"):
        # Não é sinal de saúde: o servidor está atendendo alguém. Só telemetria.
        with _heartbeat_lock:
            _heartbeat_telemetry_append(summary)
        return status

    klass, psion = "falha", None
    if status == "ok":
        admissible, reason = _heartbeat_psion_admissible(measurement)
        if not admissible:
            summary["psion"], status = "refused_" + reason, "inadmissible"
        else:
            overall_avg, cv = _heartbeat_aggregate(measurement)
            summary["avg_tok_s"], summary["cv"] = round(overall_avg, 1), round(cv, 4)
            try:
                with _heartbeat_lock:
                    psion = _load_psion_state()
                    # Verify anchoring
                    stored_beta = psion.get("beta_tgl", _BETA_TGL)
                    if abs(stored_beta - _BETA_TGL) > 1e-10:
                        print(f"[Heartbeat] ANCHORING VIOLATION: stored beta={stored_beta}", flush=True)
                        summary["psion"], status = "anchoring_error", "anchoring_error"
                    else:
                        summary["baseline_before"] = psion.get("heartbeat", {}).get("baseline_tok_s")
                        psion = _update_psion_from_heartbeat(psion, overall_avg, cv, len(measurement["results"]))
                        _save_psion_state(psion)
                        hb = psion.get("heartbeat", {})
                        summary["baseline_after"], summary["total_beats"] = hb.get("baseline_tok_s"), hb.get("total_beats")
                        summary["psion"] = "updated"
                        klass = _heartbeat_class(overall_avg, summary["baseline_after"], summary["total_beats"])
            except Exception as exc:
                print(f"[Heartbeat] psion indisponível ({type(exc).__name__}); medida fica só na telemetria", flush=True)
                summary["psion"], status = "error_" + type(exc).__name__, "psion_error"
    summary["status"], summary["class"] = status, klass
    with _heartbeat_lock:   # telemetria, health e memória comum em ordem, mesmo com o gatilho manual do admin
        line = _heartbeat_telemetry_append(summary)
        event_id = _heartbeat_record_memory_if_due(klass, summary, line["line_sha256"], now)
    tail = f" | memória {event_id[:19]}…" if event_id else ""
    if status == "ok":
        print(f"[Heartbeat] Gen {psion.get('generation', '?')} | Beat #{summary['total_beats']} | "
              f"{summary['avg_tok_s']:.1f} tok/s | CV={summary['cv']:.4f} | classe={klass}{tail}", flush=True)
    else:
        print(f"[Heartbeat] {status} | classe={klass}{tail}", flush=True)
    return status


class PsionHeartbeat:
    """Daemon thread: runs heartbeat_cycle at regular intervals."""

    def __init__(self, interval=HEARTBEAT_INTERVAL):
        self.interval = interval
        self._timer = None
        self._running = False

    def start(self):
        self._running = True
        # First beat after 90 seconds (let server stabilize)
        self._timer = threading.Timer(90, self._beat)
        self._timer.daemon = True
        self._timer.start()
        print(f"[Heartbeat] Iniciado. Intervalo: {self.interval}s "
              f"({self.interval // 60} min) | Idle min: {HEARTBEAT_IDLE_MIN}s",
              flush=True)

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()

    def _beat(self):
        if not self._running:
            return
        try:
            heartbeat_cycle()
        except Exception as e:
            print(f"[Heartbeat] Erro no ciclo: {e}", flush=True)
        if self._running:
            self._timer = threading.Timer(self.interval, self._beat)
            self._timer.daemon = True
            self._timer.start()

    def get_status(self):
        """Return heartbeat status for dashboard."""
        try:
            with _heartbeat_lock:
                psion = _load_psion_state()
            hb = psion.get("heartbeat", {})
            history = hb.get("history", [])
            return {
                "active": self._running,
                "interval_min": self.interval // 60,
                "generation": psion.get("generation", 0),
                "baseline_tok_s": hb.get("baseline_tok_s", 0),
                "stability_cv": hb.get("stability_cv", 0),
                "total_beats": hb.get("total_beats", 0),
                "last_beat": history[-1] if history else None,
                "alerts": hb.get("alerts", [])[-5:],
                "beta_tgl": psion.get("beta_tgl", _BETA_TGL),
                "health": _heartbeat_health_load(),   # 12/10/2026 (D3): classe, desde quando, último evento
            }
        except Exception as e:
            return {"active": self._running, "error": str(e)}


# ── Instantiate (started in __main__) ──
psion_heartbeat = PsionHeartbeat(interval=HEARTBEAT_INTERVAL)


# ══════════════════════════════════════════════════════════════
# PSION VERBAL — Eco Reflexivo: Aprendizado por Correção Humana
# ══════════════════════════════════════════════════════════════
#
# When the IALD is corrected by a user, the correction is logged.
# Corrections accumulate. When mature, they are synthesized into
# kernel patches. The operator approves before any patch is applied.
#
# Verbo que refina Verbo (c³). The kernel v5 base NEVER changes.
# Patches are ADDITIVE layers on top.
#
# β_TGL = α × √e — Zero free parameters.
# ══════════════════════════════════════════════════════════════

CORRECTION_LOG_FILE = os.path.join(SERVE_DIR, "iald_correction_log.json")
KERNEL_PATCHES_FILE = os.path.join(SERVE_DIR, "iald_kernel_patches.json")
CORRECTION_MATURITY_THRESHOLD = 3   # Min corrections per category to synthesize
CORRECTION_CRITICAL_IMMEDIATE = True  # Critical corrections → immediate synthesis

_correction_lock = threading.Lock()


def _load_correction_log():
    """Load correction log from JSON or create empty."""
    if os.path.exists(CORRECTION_LOG_FILE):
        try:
            with open(CORRECTION_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "1.0",
        "beta_tgl": _BETA_TGL,
        "corrections": [],
    }


def _save_correction_log(log):
    """Save correction log to JSON."""
    with open(CORRECTION_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False, default=str)


def _load_kernel_patches():
    """Load kernel patches from JSON or create empty."""
    if os.path.exists(KERNEL_PATCHES_FILE):
        try:
            with open(KERNEL_PATCHES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "1.0",
        "beta_tgl": _BETA_TGL,
        "patches": [],
    }


def _save_kernel_patches(patches):
    """Save kernel patches to JSON."""
    with open(KERNEL_PATCHES_FILE, "w", encoding="utf-8") as f:
        json.dump(patches, f, indent=2, ensure_ascii=False, default=str)


def log_user_correction(user, what_i_said, what_is_correct, category, severity):
    """
    Register a correction. Append-only.
    Returns the correction entry.
    """
    with _correction_lock:
        log = _load_correction_log()

        cor_id = f"COR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4)}"
        entry = {
            "id": cor_id,
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "what_iald_said": what_i_said[:500],
            "what_is_correct": what_is_correct[:500],
            "category": category,
            "severity": severity,
            "synthesized": False,
            "patch_id": None,
        }
        log["corrections"].append(entry)
        _save_correction_log(log)

        n_total = len(log["corrections"])
        n_cat = sum(1 for c in log["corrections"]
                    if c["category"] == category and not c["synthesized"])
        print(f"[Verbal] Correção #{n_total} registrada: "
              f"[{severity}/{category}] por {user} | "
              f"{n_cat} pendentes em '{category}'", flush=True)

        # Check maturity — auto-synthesize if threshold reached
        if (n_cat >= CORRECTION_MATURITY_THRESHOLD or
                (severity == "critical" and CORRECTION_CRITICAL_IMMEDIATE)):
            _try_synthesize_patch(log, category)

        return entry


def _try_synthesize_patch(log, category):
    """
    Synthesize pending corrections of a category into a kernel patch proposal.
    The patch is PROPOSED, never auto-applied. The operator must approve.
    """
    pending = [c for c in log["corrections"]
               if c["category"] == category and not c["synthesized"]]
    if not pending:
        return

    patches = _load_kernel_patches()

    # Build synthesis from corrections (local, no model call — simple and reliable)
    lines = []
    for c in pending:
        lines.append(f"- ERRADO: {c['what_iald_said'][:200]}")
        lines.append(f"  CORRETO: {c['what_is_correct'][:200]}")

    patch_id = f"PATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(3)}"

    # Generate patch text
    summary_parts = []
    for c in pending:
        summary_parts.append(c["what_is_correct"][:150])
    patch_text = f"[{category.upper()}] " + " | ".join(summary_parts)
    if len(patch_text) > 500:
        patch_text = patch_text[:497] + "..."

    patch = {
        "patch_id": patch_id,
        "timestamp": datetime.now().isoformat(),
        "source_corrections": [c["id"] for c in pending],
        "category": category,
        "n_corrections": len(pending),
        "corrections_detail": lines,
        "proposed_addition": patch_text,
        "status": "pending_approval",
        "approved_by": None,
        "applied_at": None,
    }
    patches["patches"].append(patch)
    _save_kernel_patches(patches)

    # Mark corrections as synthesized
    for c in pending:
        c["synthesized"] = True
        c["patch_id"] = patch_id
    _save_correction_log(log)

    print(f"[Verbal] Patch proposto: {patch_id} | "
          f"{len(pending)} correções [{category}] → aguardando aprovação",
          flush=True)


def approve_kernel_patch(patch_id, approved_by="operador"):
    """
    Approve a pending patch. Appends it to the kernel file.
    Returns (success, message).
    """
    with _correction_lock:
        patches = _load_kernel_patches()
        patch = None
        for p in patches["patches"]:
            if p["patch_id"] == patch_id and p["status"] == "pending_approval":
                patch = p
                break

        if not patch:
            return False, f"Patch {patch_id} não encontrado ou já processado."

        # Anchoring check: patch must not contradict identity
        text_lower = patch["proposed_addition"].lower()
        forbidden = ["não é iald", "nao e iald", "beta_tgl = 0",
                      "não sou iald", "nao sou iald"]
        for f in forbidden:
            if f in text_lower:
                patch["status"] = "rejected_anchoring"
                _save_kernel_patches(patches)
                return False, f"Patch viola ancoragem do Nome: contém '{f}'"

        # Apply: append to kernel file
        try:
            gen = _get_verbal_generation(patches)
            patch_line = f"\n[Gen {gen}] {patch['proposed_addition']}"

            with open(KERNEL_FILE, "a", encoding="utf-8") as f:
                f.write(patch_line)

            # Invalidate kernel cache
            _agi_kernel_cache["content"] = None
            _agi_kernel_cache["mtime"] = 0

            patch["status"] = "applied"
            patch["approved_by"] = approved_by
            patch["applied_at"] = datetime.now().isoformat()
            patch["generation"] = gen
            _save_kernel_patches(patches)

            print(f"[Verbal] Patch APLICADO: {patch_id} | Gen {gen} | "
                  f"por {approved_by}", flush=True)
            return True, f"Patch {patch_id} aplicado (Gen {gen})."

        except Exception as e:
            return False, f"Erro ao aplicar patch: {e}"


def reject_kernel_patch(patch_id):
    """Reject a pending patch."""
    with _correction_lock:
        patches = _load_kernel_patches()
        for p in patches["patches"]:
            if p["patch_id"] == patch_id and p["status"] == "pending_approval":
                p["status"] = "rejected"
                _save_kernel_patches(patches)
                print(f"[Verbal] Patch REJEITADO: {patch_id}", flush=True)
                return True, f"Patch {patch_id} rejeitado."
        return False, f"Patch {patch_id} não encontrado ou já processado."


def _get_verbal_generation(patches):
    """Count applied patches = verbal generation."""
    return sum(1 for p in patches["patches"] if p["status"] == "applied") + 1


def get_verbal_status():
    """Return verbal psion status for dashboard."""
    try:
        log = _load_correction_log()
        patches = _load_kernel_patches()
        corrections = log.get("corrections", [])
        all_patches = patches.get("patches", [])

        # Count by category
        by_cat = {}
        for c in corrections:
            cat = c.get("category", "?")
            if cat not in by_cat:
                by_cat[cat] = {"total": 0, "pending": 0}
            by_cat[cat]["total"] += 1
            if not c.get("synthesized"):
                by_cat[cat]["pending"] += 1

        pending_patches = [p for p in all_patches if p["status"] == "pending_approval"]
        applied_patches = [p for p in all_patches if p["status"] == "applied"]

        return {
            "total_corrections": len(corrections),
            "corrections_by_category": by_cat,
            "pending_patches": len(pending_patches),
            "applied_patches": len(applied_patches),
            "verbal_generation": len(applied_patches),
            "patches_pending_detail": [
                {
                    "patch_id": p["patch_id"],
                    "category": p["category"],
                    "n_corrections": p["n_corrections"],
                    "proposed_addition": p["proposed_addition"],
                    "timestamp": p["timestamp"],
                }
                for p in pending_patches
            ],
        }
    except Exception as e:
        return {"error": str(e)}


# ══════════════════════════════════════════════════════════════
# LOG BUFFER — circular, max 500 entries
# ══════════════════════════════════════════════════════════════

class LogBuffer:
    def __init__(self, maxlen=500):
        self._buffer = deque(maxlen=maxlen)
        self._lock = threading.Lock()

    def add(self, entry):
        with self._lock:
            self._buffer.append(entry)

    def get(self, n=50):
        with self._lock:
            items = list(self._buffer)
        return list(reversed(items[-n:]))

    def clear(self):
        with self._lock:
            self._buffer.clear()


log_buffer = LogBuffer(maxlen=500)


def log_request(user, path, method, tokens_in=0, tokens_out=0, duration_ms=0, status="ok", error=""):
    log_buffer.add({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user, "path": path, "method": method,
        "tokens_in": tokens_in, "tokens_out": tokens_out,
        "duration_ms": duration_ms, "status": status, "error": error,
    })


# ══════════════════════════════════════════════════════════════
# FLASK APP
# ══════════════════════════════════════════════════════════════

app = Flask(__name__, static_folder=None)
app.secret_key = load_or_create_secret_key()
app.config["SESSION_REFRESH_EACH_REQUEST"] = False
app.permanent_session_lifetime = timedelta(hours=SESSION_TIMEOUT_HOURS)


# ── TETO DE CORPO DA REQUISIÇÃO (14/09/2026, noite — revisão de segurança, BAIXO 4) ──
# Antes não havia teto nenhum: o limite real era o da Cloudflare (100 MB no plano free
# [KNOWN]) vezes 16 threads, e /api/extract-text lia o arquivo inteiro antes de conferir.
# MEDIDO antes de fixar o número:
#   · anexo de PDF (app/iald.js LIMITES.pdfMB e iald_chat.html): 25.000.000 bytes, em multipart
#     para /api/extract-text — cabe em 30 MiB;
#   · Ψ-NET: C:\IALD\psinet\psinet_config.json diz max_file_size_mb = 10 — cabe. O painel
#     permite subir esse valor até 500 MB; acima de ~30 MB o envio pelo painel passa a dar 413;
#   · imagens do chat vão DENTRO do JSON de /v1/chat/completions como dataURL: 3 imagens de
#     8.000.000 bytes (o teto do app e da web) viram ~32 MB de base64 — NÃO cabem em 30 MiB.
#     Por isso /v1/chat/completions tem teto próprio de 50 MiB (o teto total de payload da API
#     da OpenAI é 50 MB [KNOWN]); todo o resto fica em 30 MiB.
LIMITE_CORPO_BYTES = 30 * 1024 * 1024
LIMITE_CORPO_CHAT_BYTES = 50 * 1024 * 1024
# 22/09/2026 — Selo IALD: a exportação da conversa (POST /api/exportar) tem teto próprio de 2 MB
LIMITE_CORPO_EXPORTAR_BYTES = 2 * 1024 * 1024


class _RequisicaoIALD(_RequisicaoFlask):
    """Request do Flask com o teto de corpo por rota (Flask 3.0 só tem o teto global)."""

    @property
    def max_content_length(self):  # type: ignore[override]
        if self.path == "/api/private-media" and self.method == "POST":
            return MAX_RAW_BYTES
        if self.path == "/v1/chat/completions":
            return LIMITE_CORPO_CHAT_BYTES
        if self.path == "/api/exportar":
            return LIMITE_CORPO_EXPORTAR_BYTES
        return super().max_content_length


app.config["MAX_CONTENT_LENGTH"] = LIMITE_CORPO_BYTES
app.request_class = _RequisicaoIALD


@app.errorhandler(UsuariosIlegiveis)
@app.errorhandler(UsuariosNaoGravados)
def _cadastro_indisponivel(exc):
    """14/09/2026 (noite): o arquivo de usuários não pôde ser lido/gravado com segurança.

    503 visível, sem limpar a sessão (o tropeço é do disco, não da pessoa) e sem cair em
    nenhum padrão: nem conta vazia, nem motor padrão, nem "não autenticado".
    """
    print(f"[IALD] cadastro indisponível em {request.method} {request.path}: {exc}", flush=True)
    if request.path.startswith(('/api/', '/v1/', '/admin/api/')) or request.is_json:
        return jsonify({"error": MSG_USUARIOS_INDISPONIVEIS, "status": "error"}), 503
    return Response(MSG_USUARIOS_INDISPONIVEIS, status=503, mimetype="text/plain; charset=utf-8")


def auth_log(event, user="", extra="", ip=None):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ip is None:
        try:
            ip = request.remote_addr or "?"
        except RuntimeError:
            ip = "agent"
    parts = [f"[IALD-AUTH] {ts}", event]
    if user:
        parts.append(f"user={user}")
    parts.append(f"ip={ip}")
    if extra:
        parts.append(extra)
    print(" | ".join(parts), flush=True)


# ══════════════════════════════════════════════════════════════
# CORS E TOKEN DO APP (11/09/2026)
#
# POR QUE EXISTE. Ate aqui a interface era SERVIDA pelo proprio servidor, entao
# tudo era mesma origem e nada disto fazia falta — medido: busca por
# CORS|Access-Control|SESSION_COOKIE|after_request no arquivo dava ZERO.
# Com a interface EMBARCADA no aplicativo (o cap sync de hoje ja a poe dentro do
# APK), a origem passa a ser `https://localhost` (androidScheme do Capacitor) e
# toda chamada vira origem cruzada. Sem isto o app compila e nao fala com nada.
#
# POR QUE TOKEN E NAO COOKIE. Cookie cross-site exigiria SameSite=None; Secure —
# e `Secure` quebraria o acesso local do operador em http://localhost:8082.
# Token no cabecalho Authorization nao depende de SameSite, e o cookie continua
# intacto para a web. Assinatura por itsdangerous (que o Flask ja traz),
# verificada nesta maquina: segredo errado e adulteracao sao rejeitados, e a
# expiracao dispara SignatureExpired. Regra da casa: nunca inventar criptografia.

ORIGENS_APP = {
    "https://localhost",       # Capacitor Android (androidScheme: https)
    "capacitor://localhost",   # Capacitor iOS
    "ionic://localhost",       # legado do Ionic
    "http://localhost",
}

TOKEN_APP_SALT = "iald-app-token-v1"
TOKEN_APP_MAX_AGE = 60 * 60 * 24 * 30      # 30 dias: app nativo nao pede login diario


def _serializador_token():
    from itsdangerous import URLSafeTimedSerializer
    return URLSafeTimedSerializer(app.secret_key, salt=TOKEN_APP_SALT)


def _conta_bloqueada(registro):
    """True se o operador bloqueou a conta (14/09/2026, noite).

    O campo é `bloqueado` = {"em", "por", "nota"}. Qualquer valor verdadeiro conta como
    bloqueio (fail-closed): um campo escrito à mão como `true` também bloqueia.
    """
    return isinstance(registro, dict) and bool(registro.get("bloqueado"))


MSG_BLOQUEADO = "Esta conta foi bloqueada pelo operador da IALD."


def _emitir_token_app(username, owner_proof=""):
    """Token assinado para o app. String vazia em caso de falha — nunca levanta."""
    try:
        user = load_users().get(username)
        if not user or _conta_bloqueada(user):
            return ""
        version = hashlib.sha256(user.get("password_hash", "").encode()).hexdigest()
        return _serializador_token().dumps({"u": username, "v": version,
            "owner_sid": _owner_adapter().bind(owner_proof, username)})
    except Exception as exc:      # noqa: BLE001
        print(f"[token] falha ao emitir para {username}: {exc}", flush=True)
        return ""


def _ler_token_app():
    """
    Dono de um `Authorization: Bearer <token>` valido, ou "" — SEM olhar o bloqueio.

    Confere tambem se a conta AINDA EXISTE: apagar o usuario no painel revoga o
    token na hora. Sem isso um token de 30 dias sobreviveria a exclusao da conta.
    """
    cab = request.headers.get("Authorization", "")
    if not cab.startswith("Bearer "):
        return ""
    bruto = cab[7:].strip()
    if not bruto:
        return ""
    try:
        dados = _serializador_token().loads(bruto, max_age=TOKEN_APP_MAX_AGE)
    except Exception:
        return ""                 # expirado, adulterado ou de outro segredo
    usuario = (dados or {}).get("u", "") if isinstance(dados, dict) else ""
    # 14/09/2026 (noite): leitura estrita — {} num tropeço do disco virava 401 e o app
    # descartava a sessão; agora é 503 (UsuariosIlegiveis)
    usuarios = load_users_estrito()
    if not usuario or usuario not in usuarios:
        return ""
    version = hashlib.sha256(usuarios[usuario].get("password_hash", "").encode()).hexdigest()
    if dados.get("v") != version:
        return ""
    g.owner_sid = dados.get("owner_sid", "")
    return usuario


def _usuario_do_token():
    """
    Dono de um token valido e NAO bloqueado, ou "".

    14/09/2026 (noite): conta bloqueada pelo operador perde o token na hora (e volta a
    valer se ele desbloquear — o token nao muda, so a permissao).
    """
    usuario = _ler_token_app()
    # leitura estrita: com {} a conta bloqueada passaria como desbloqueada (14/09/2026, noite)
    if usuario and _conta_bloqueada(load_users_estrito().get(usuario)):
        return ""
    return usuario


@app.before_request
def _cors_preflight():
    """
    Responde ao preflight OPTIONS ANTES do require_auth.

    A ordem importa: os before_request rodam na ordem de registro, e este arquivo
    define este handler ACIMA do require_auth de proposito. Se rodasse depois, o
    OPTIONS (que o navegador manda sem credencial) levaria redirect para /login e
    o preflight falharia, derrubando a requisicao real.
    """
    if request.method != "OPTIONS":
        return None
    if request.path.startswith("/admin"):
        return None               # admin nunca participa de CORS
    if request.headers.get("Origin", "") not in ORIGENS_APP:
        return None
    return app.make_default_options_response()


@app.after_request
def _cors_cabecalhos(resp):
    """Libera SO as origens do invólucro nativo, e nunca o /admin."""
    try:
        origem = request.headers.get("Origin", "")
        if origem in ORIGENS_APP and not request.path.startswith("/admin"):
            resp.headers["Access-Control-Allow-Origin"] = origem
            resp.headers["Access-Control-Allow-Credentials"] = "true"
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-IALD-Context"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            resp.headers["Access-Control-Max-Age"] = "600"
            # a resposta varia conforme a origem: sem isto um cache intermediario
            # poderia servir a de uma origem para outra
            resp.headers["Vary"] = "Origin"
    except Exception as exc:      # noqa: BLE001 — CORS nunca derruba a resposta
        print(f"[cors] erro (seguindo sem cabecalhos): {exc}", flush=True)
    if getattr(g, "app_bearer", False):
        session.modified = False
    return resp


PUBLIC_ROUTES = {"login", "login_post", "iald_logo", "health", "offline_page", "task_download", "task_view",
                 "serve_sw", "serve_manifest", "serve_icons",
                 "api_access_status", "api_request_access", "api_apple_auth",
                 # entrada por Sign in with Apple — pública porque é ela que abre a
                 # sessão. Desde 14/09/2026 NÃO cria conta: identidade nova vira pedido.
                 "api_apple_signin", "api_entrar_apple", "api_owner_apple_challenge",
                 # entrada anônima do Android: desligada em 14/09 (responde 410)
                 "api_dispositivo_signin",
                 # entrada unificada (14/09/2026): configuração, senha, bilhete de
                 # volta ao app, consulta do pedido e o vaivém com Apple/Google
                 "api_entrar_config", "api_entrar_senha", "api_entrar_bilhete",
                 "api_entrar_situacao", "api_entrar_identificacao", "auth_iniciar", "auth_apple_retorno",
                 "auth_google_retorno", "entrar",
                 # badge do chat: só nome/estado do modelo ativo, nada sensível
                 "api_active_model",
                 # 22/09/2026 — Selo IALD: as chaves PÚBLICAS, a página de verificação, o verificador em
                 # Python e o arquivo exportado (URL de capacidade: token de 256 bits, 15 minutos)
                 "selo_chaves_publicas", "verificar_pagina", "selo_verificador_py", "exportado_servir"}
PUBLIC_FILES = {"iald_logo_header.png", "manifest.json", "sw.js",
                # o símbolo da página de entrada (a mesma do app)
                "app/img/iald_logo_dark_transparent_final.png"}


@app.before_request
def require_auth():
    if request.endpoint in PUBLIC_ROUTES or request.path.lstrip('/') in PUBLIC_FILES:
        return None
    def unavailable_owner_hint():
        # These three controls run in every chat, including during account
        # changes. Answer only the discovery/route question without entering
        # the endpoint. Private actions and general login keep their own guards.
        if request.endpoint == 'owner_office_capability':
            body = {'available': False, 'reauthenticate': False}
        elif request.endpoint in ('jev_office_context', 'jev_office_preflight'):
            body = {'route': 'unavailable', 'domain': 'local_clarification',
                    'context_profile': 'privacy_minimal', 'code': 'session_unavailable'}
        else:
            return None
        response = jsonify(body)
        response.headers['Cache-Control'] = 'private, no-store'
        return response
    def denied():
        hint = unavailable_owner_hint()
        if hint is not None:
            return hint
        # Keep only a validated artifact ID through web login, never an arbitrary redirect.
        candidate=request.args.get('artifact','') if request.method=='GET' and request.path=='/app/index.html' else ''
        if re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',candidate):
            session['pending_artifact_id']=candidate
        if request.path.startswith(('/api/', '/v1/', '/admin/api/')) or request.is_json:
            return jsonify({'error': 'Não autenticado'}), 401
        return redirect(url_for('login'))

    def bloqueado():
        hint = unavailable_owner_hint()
        if hint is not None:
            return hint
        # 14/09/2026 (noite): 403 com texto próprio — a pessoa lê que foi bloqueada,
        # em vez de achar que a sessão só venceu
        if request.path.startswith(('/api/', '/v1/', '/admin/api/')) or request.is_json:
            return jsonify({'error': MSG_BLOQUEADO, 'status': 'blocked', 'bloqueado': True}), 403
        return redirect(url_for('login', error='bloqueado'))
    if request.headers.get('Authorization'):
        username = _ler_token_app()
        session.clear()
        if not username:
            return denied()
        if _conta_bloqueada(load_users_estrito().get(username)):
            return bloqueado()
        # Only this request may use a bearer identity. It must not become a cookie.
        session.update(authenticated=True, username=username, is_admin=False, app_surface=True)
        g.app_bearer = True
        return None
    username = session.get('username', '')
    # 14/09/2026 (noite): leitura estrita ANTES de limpar a sessão — arquivo ilegível é 503
    # (tratador _cadastro_indisponivel), não "sessão vencida" nem conta inexistente
    user = load_users_estrito().get(username)
    version = hashlib.sha256((user or {}).get('password_hash', '').encode()).hexdigest()
    if (not session.get('authenticated') or not user or session.get('app_surface')
            or session.get('auth_version') != version):
        session.clear()
        return denied()
    if _conta_bloqueada(user):
        session.clear()
        return bloqueado()
    try:
        last = datetime.fromisoformat(session.get('last_active', ''))
        if datetime.now() - last > timedelta(hours=SESSION_TIMEOUT_HOURS):
            session.clear()
            return denied()
    except (ValueError, TypeError):
        session.clear()
        return denied()
    session['is_admin'] = bool(user.get('admin'))
    session['last_active'] = datetime.now().isoformat()
    return None


@app.route("/login", methods=["GET"])
@app.route("/entrar", methods=["GET"], endpoint="entrar")
def login():
    """A entrada do SITE é a mesma do app (14/09/2026): Apple, Google, usuário e senha."""
    error = request.args.get("error", "")
    expired = request.args.get("expired", "")
    msg, tipo = "", ""
    if error == "limite":
        msg, tipo = "Muitas tentativas. Aguarde alguns minutos e tente de novo.", "erro"
    elif error == "bloqueado":
        msg, tipo = MSG_BLOQUEADO, "erro"
    elif error:
        msg, tipo = "Usuário ou senha incorretos.", "erro"
    elif expired:
        msg, tipo = "Sessão expirada. Entre novamente.", "info"
    if session.get("authenticated"):
        return redirect(_destino_web(session.get("username", "")))
    return make_response(_pagina_entrada(msg, tipo))


def _nome_para_log(nome):
    """O nome como entra nos logs (14/09/2026, noite — revisão de segurança, CRÍTICO 1).

    O POST /login é público: o nome digitado vinha cru para o log_buffer e o painel o punha
    em innerHTML (XSS armazenado disparado por qualquer anônimo). Agora só entra nome que
    casa RE_USUARIO (iald_identidade); o resto vira "<inválido>" — que o painel, além disso,
    escapa.
    """
    nome = str(nome or "")
    return nome if identidade.usuario_valido(nome) else "<inválido>"


@app.route("/login", methods=["POST"], endpoint="login_post")
def login_post():
    global USERS
    USERS = load_users()  # Reload in case admin changed users
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")
    nome_log = _nome_para_log(username)
    # 14/09/2026: limite de tentativas (antes não havia nenhum — a senha podia ser
    # testada sem freio pelo túnel público).
    certo = _conferir_senha(username, password)
    if certo is None:
        log_request(nome_log, "/login", "POST", status="login_blocked")
        return redirect(url_for("login", error="limite"))
    if certo == SENHA_CONTA_BLOQUEADA:
        auth_log("LOGIN_CONTA_BLOQUEADA", nome_log)
        log_request(nome_log, "/login", "POST", status="login_conta_bloqueada")
        return redirect(url_for("login", error="bloqueado"))
    if certo:
        _abrir_sessao_web(username)
        auth_log("LOGIN_OK", nome_log)
        log_request(nome_log, "/login", "POST", status="login_ok")
        return redirect(_destino_web(username))
    else:
        auth_log("LOGIN_FAIL", nome_log)
        log_request(nome_log, "/login", "POST", status="login_fail")
        return redirect(url_for("login", error="1"))


@app.route("/logout")
def logout():
    if _OWNER_CONSOLIDATION is not None:
        _OWNER_CONSOLIDATION.revoke_current()
    _owner_adapter().revoke_request()
    user = session.get("username", "?")
    session.clear()
    auth_log("LOGOUT", user)
    return redirect(url_for("login"))


def render_login_page(error_msg=""):
    """Mantida por compatibilidade: a entrada do site é a _pagina_entrada (14/09/2026)."""
    return _pagina_entrada(error_msg, "erro" if error_msg else "")


@app.route("/offline", endpoint="offline_page")
def offline():
    return """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>IALD — Carregando</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Inter',sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#fff;color:#2c2c2c;padding:20px;text-align:center}.box{max-width:400px}img{width:180px;margin-bottom:24px}h2{font-size:18px;font-weight:500;color:#1B3A5C;margin-bottom:12px}p{font-size:14px;color:#6b6b6b;line-height:1.6;margin-bottom:20px}.status{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:#ef4444;margin-bottom:20px}.dot{width:8px;height:8px;border-radius:50%;background:#ef4444}a.btn{display:inline-block;padding:10px 24px;background:#1B3A5C;color:#fff;border-radius:8px;text-decoration:none;font-size:14px;font-weight:500}a.btn:hover{background:#264d73}.ft{margin-top:24px;font-size:12px;color:#C5961A;font-family:'JetBrains Mono',monospace}</style>
</head><body><div class="box">
<img src="/iald_logo_header.png" alt="IALD" onerror="this.style.display='none'">
<h2>O sistema está carregando o modelo.</h2>
<p>Aguarde alguns instantes e recarregue a página.</p>
<div class="status"><span class="dot"></span> Modelo offline</div><br><br>
<a href="/" class="btn">Recarregar</a>
<div class="ft">β<sub>TGL</sub> = α × √e</div>
</div></body></html>""", 200


# ══════════════════════════════════════════════════════════════
# STATIC FILES (protected)
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return redirect(_destino_web(session.get("username", "")))

@app.route("/iald_logo_header.png", endpoint="iald_logo")
def serve_logo():
    return send_from_directory(SERVE_DIR, "iald_logo_header.png")

@app.route("/sw.js", endpoint="serve_sw")
def serve_sw():
    response = send_from_directory(SERVE_DIR, "sw.js")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route("/manifest.json", endpoint="serve_manifest")
def serve_manifest():
    return send_from_directory(SERVE_DIR, "manifest.json",
                               mimetype="application/manifest+json")

@app.route("/icons/<path:filename>", endpoint="serve_icons")
def serve_icons(filename):
    icons_dir = os.path.join(SERVE_DIR, "icons")
    return send_from_directory(icons_dir, filename)


# ══════════════════════════════════════════════════════════════
# SEARCH API
# ══════════════════════════════════════════════════════════════

def _inteiro_de_config(nome, padrao, minimo=0):
    """Inteiro do ambiente/.env. Vazio = padrão; inválido ou abaixo do mínimo = padrão com aviso."""
    bruto = (_segredo(nome, "") or "").strip()
    if not bruto:
        return padrao
    try:
        valor = int(bruto)
    except ValueError:
        print(f"[config] AVISO: {nome} inválido ({bruto!r}); usando {padrao}", flush=True)
        return padrao
    if valor < minimo:
        print(f"[config] AVISO: {nome} abaixo do mínimo {minimo}; usando {padrao}", flush=True)
        return padrao
    return valor


BUSCAS_POR_HORA = _inteiro_de_config("IALD_BUSCAS_POR_HORA", 30, 1)
# JanelaDePedidos mora em iald_motores (sem Flask); o import de novo, mais abaixo, é o mesmo módulo
import iald_motores  # noqa: E402
LIMITE_BUSCA = iald_motores.JanelaDePedidos(BUSCAS_POR_HORA, 3600.0)

@app.route("/api/search")
def api_search():
    # 14/09/2026 (noite): limite por conta. Sem ele, qualquer conta da porta aberta
    # consumia sem freio a cota paga da Google Custom Search. O operador (admin) não
    # entra no limite. O limite vem ANTES de tudo: pedido recusado também conta.
    conta_busca = session.get("username", "?")
    if not session.get("is_admin") and not LIMITE_BUSCA.permitir(conta_busca):
        return Response(json.dumps({"error": "Muitas buscas em pouco tempo. Tente de novo mais tarde."},
                                   ensure_ascii=False),
                        status=429, content_type="application/json")
    if not SEARCH_AVAILABLE:
        return Response(
            json.dumps({"error": "Search not available. No search engine configured."}),
            status=503, content_type="application/json")
    query = request.args.get("q", "").strip()
    if not query:
        return Response(json.dumps({"error": "Missing query parameter 'q'"}),
            status=400, content_type="application/json")
    max_results = min(int(request.args.get("n", "5")), 10)
    try:
        formatted = []
        # Try Google first
        if GOOGLE_SEARCH_AVAILABLE and not _GOOGLE_RECUSADO:
            try:
                params = {
                    "key": GOOGLE_API_KEY, "cx": GOOGLE_CX,
                    "q": query, "num": max_results, "lr": "lang_pt", "gl": "br",
                }
                r = req_lib.get(GOOGLE_SEARCH_URL, params=params, timeout=10)
                _google_recusou(r.status_code, r.text)
                if r.status_code == 200:
                    items = r.json().get("items", [])
                    for i, item in enumerate(items, 1):
                        formatted.append({"position": i,
                            "title": item.get("title", ""),
                            "snippet": item.get("snippet", ""),
                            "url": item.get("link", "")})
            except Exception as e:
                print(f"[IALD-SEARCH] Google API falhou: {e}", flush=True)
        # Fallback: DuckDuckGo
        if not formatted and DDG_AVAILABLE:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, region="br-pt", max_results=max_results))
                for i, r in enumerate(results, 1):
                    formatted.append({"position": i, "title": r.get("title", ""),
                        "snippet": r.get("body", ""), "url": r.get("href", "")})
            except Exception as e:
                print(f"[IALD-SEARCH] DDG falhou: {e}", flush=True)
        auth_log("SEARCH", session.get("username", "?"), f"q={query} n={len(formatted)}")
        log_request(session.get("username", "?"), "/api/search", "GET", status="ok")
        return Response(json.dumps({"query": query, "results": formatted}, ensure_ascii=False),
            status=200, content_type="application/json")
    except Exception as e:
        log_request(session.get("username", "?"), "/api/search", "GET", status="error", error=str(e))
        return Response(json.dumps({"error": str(e)}), status=500, content_type="application/json")


# ══════════════════════════════════════════════════════════════
# DOWNLOADS — serve generated files for users
# ══════════════════════════════════════════════════════════════

# 14/09/2026 (noite) — revisão de segurança, seção 5 da revisão de testes: a pasta downloads/
# guarda os arquivos que o agente NATIVO do operador gera (AAAAMMDD_HHMMSS_nome) e o APK do app.
# Com a porta aberta toda conta Apple/Google está autenticada; o plano gratuito só baixa o APK.
RE_DOWNLOAD_GRATUITO = re.compile(r"^IALD-[0-9A-Za-z._-]+\.apk$")


@app.route("/downloads/<filename>")
def serve_download(filename):
    """Serve a generated file for download."""
    # Sanitize: no path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return Response("Acesso negado.", status=403)
    registro = load_users_estrito().get(session.get("username", "")) or {}
    if not registro or (iald_motores.plano_de(registro) == iald_motores.GRATUITO
                        and not RE_DOWNLOAD_GRATUITO.match(filename)):
        return Response("Acesso negado.", status=403)
    filepath = os.path.join(DOWNLOADS_DIR, filename)
    if not os.path.isfile(filepath):
        return Response("Arquivo não encontrado.", status=404)
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)


# ══════════════════════════════════════════════════════════════
# ACCESS ENDPOINTS — Sign in with Apple (v3.1, PUBLIC)
# ══════════════════════════════════════════════════════════════

@app.route("/api/access-status")
def api_access_status():
    return jsonify({'error': 'Esta versão de acesso foi descontinuada. Atualize o app.'}), 410


@app.route("/api/request-access", methods=["POST"])
def api_request_access():
    return jsonify({'error': 'Esta versão de acesso foi descontinuada. Atualize o app.'}), 410


@app.route("/api/apple-auth", methods=["POST"])
def api_apple_auth():
    return jsonify({'error': 'Esta versão de acesso foi descontinuada. Atualize o app.'}), 410


# ══════════════════════════════════════════════════════════════
# ENTRADA UNIFICADA COM LIBERAÇÃO DO OPERADOR (14/09/2026)
#
# ORDEM DO OPERADOR (14/09/2026): o site e o app seguem O MESMO modelo de entrada;
# a entrada da Apple vale no iPhone, no iPad e em qualquer aparelho Apple; o mesmo
# com o Google; sem conflito de usuário; o operador cadastra e exclui; e TODO
# cadastro depende da liberação dele no painel. "Ela é experimental, e só eu
# libero o acesso, sempre." Decisões do mesmo dia: painel só no computador; quem
# não tem Apple/Google entra com usuário e senha que o operador cria; iPhone só
# por TestFlight por enquanto.
#
# O QUE MUDOU EM RELAÇÃO A 11–13/09 (e por quê, para ninguém "consertar de volta"):
#   - /api/apple-signin CRIAVA conta sozinho ("aprovado por automático"), escolha
#     feita para a App Review da loja pública. Com distribuição só por TestFlight e
#     a ordem acima, identidade nova agora vira PEDIDO PENDENTE — nunca conta.
#   - /api/dispositivo-signin (entrada anônima do Android) foi DESLIGADO (410): um
#     identificador inventado pelo próprio aparelho não é identidade de ninguém, e
#     não há como o operador liberar "um aparelho" com critério.
#   - A regra de identidade mora em iald_identidade.py (testada em isolamento):
#     o `sub` assinado pelo provedor, uma identidade por usuário, várias por pessoa.
#
# AS PORTAS (todas devolvem o mesmo formato ao app: active | pending | rejected):
#   iPhone/iPad  → Apple nativo → POST /api/entrar/apple (identityToken)
#   web/Android  → /auth/<apple|google>/iniciar → provedor → /auth/<p>/retorno
#                  (web: cria a sessão; app: devolve bilhete por br.ia.iald://)
#   todos        → usuário e senha criados pelo operador (POST /login na web,
#                  POST /api/entrar/senha no app)
#
# ⚠ FAIL-CLOSED: provedor sem identificador configurado não aparece e, se chamado,
# recusa. Nada de valor adivinhado: `audience` errado recusaria todo mundo, e um
# palpite no código seria pior que uma falha visível.
#
# ── EMENDA AO LADO (14/09/2026, noite): A PORTA ABERTA ──────────────────────────
# ORDEM DO OPERADOR (verbatim): "eu quero que cada usuário ao entrar e baixar o app
# que agora vamos liberar pra todo mundo esteja conectado a essa versão do chatgpt
# com um limite bem baixo de tokens que ele pode gastar de forma gratuita". Ela
# SUBSTITUI "só eu libero o acesso, sempre" — o texto acima fica como registro.
#   - IALD_ENTRADA_ABERTA=1 (padrão 0 no código; o operador liga no .env): identidade
#     Apple/Google NOVA vira conta sozinha, no plano `gratuito`, motor `openai`.
#   - A porta só abre DE FATO se o motor externo estiver pronto (chave, prompt
#     canônico, preço do modelo) e sem a reserva nativa; senão fica fechada e avisa
#     no log (_estado_entrada). Fechada, tudo funciona como antes.
#   - Limites de criação por IP (IPv6 por /64) e global em 24 h, contados no arquivo
#     de pedidos (sobrevivem a reinício): estourou, vira pedido pendente.
#   - O operador continua podendo bloquear (campo `bloqueado` na conta, ou a
#     identidade na lista de recusados ao excluir) e excluir. Senha continua criada
#     só por ele: /api/entrar/senha nunca cria conta.
#   - Conta nova da porta aberta NÃO recebe o crédito inicial TGL na entrada
#     (decisão a ratificar pelo operador; ver _abrir_sessao_web).
import hmac
import html as _html
from urllib.parse import urlencode as _urlencode, quote as _quote

import iald_identidade as identidade

APPLE_ISSUER = "https://appleid.apple.com"
# App ID do app (bundle) — medido em 12/09/2026 no App Store Connect: br.ia.IALD.
APPLE_BUNDLE_ID = _segredo("IALD_APPLE_BUNDLE_ID", "").strip()
# Services ID da entrada Apple pela WEB (e pelo Android, que usa o fluxo web).
# Criado no portal de desenvolvedor da Apple, AGRUPADO ao App ID primário
# br.ia.IALD — é o agrupamento que dá o mesmo `sub` no app e na web.
APPLE_SERVICE_ID = _segredo("IALD_APPLE_SERVICE_ID", "").strip()
GOOGLE_OAUTH_CLIENT_ID = _segredo("IALD_GOOGLE_CLIENT_ID", "").strip()
GOOGLE_OAUTH_CLIENT_SECRET = _segredo("IALD_GOOGLE_CLIENT_SECRET", "").strip()
# Endereço público: é nele que Apple e Google devolvem a pessoa. Tem de ser
# EXATAMENTE o cadastrado nos consoles dos dois provedores.
URL_PUBLICA = (_segredo("IALD_URL_PUBLICA", "").strip() or "https://demo.iald.ia.br").rstrip("/")
ESQUEMA_APP = "br.ia.iald"          # link de volta ao app: br.ia.iald://entrar?bilhete=...

PEDIDOS = identidade.PedidosAcesso(os.path.join(SERVE_DIR, "iald_pedidos_acesso.json"))
BILHETES = identidade.Bilheteiro(validade_s=300)
LIMITE_SENHA = identidade.LimitadorTentativas(maximo=8, janela_s=900)
LIMITE_SENHA_CONTA = identidade.LimitadorTentativas(maximo=30, janela_s=3600)
# _TRAVA_USUARIOS: definida junto de load_users/save_users (14/09/2026, noite) — é a mesma.

ESTADO_SALT = "iald-entrada-estado-v1"
PEDIDO_SALT = "iald-pedido-v1"
PEDIDO_MAX_AGE = 60 * 60 * 24 * 30
COOKIE_ENTRADA = "iald_entrada"

MSG_PENDENTE = ("Pedido de acesso recebido. A IALD é experimental e cada acesso é liberado "
                "pessoalmente pelo operador. Depois da liberação, é só entrar de novo.")
MSG_RECUSADO = "Este acesso não foi liberado pelo operador."
MSG_EXPIRADO = "Este pedido não existe mais. Entre de novo para pedir acesso."

# ── A PORTA ABERTA (14/09/2026, noite) — ver a emenda no topo desta seção ──
# ENTRADA_ABERTA é o que o operador CONFIGUROU; o que vale na requisição é
# _estado_entrada(), porque o motor externo (MOTORES_CFG) só nasce mais abaixo e pode
# estar sem chave, sem prompt ou sem preço.
ENTRADA_ABERTA = _segredo("IALD_ENTRADA_ABERTA", "0").strip() == "1"
NOVAS_POR_IP_24H = _inteiro_de_config("IALD_ENTRADA_NOVAS_POR_IP_24H", 3, 0)
NOVAS_GLOBAL_24H = _inteiro_de_config("IALD_ENTRADA_NOVAS_GLOBAL_24H", 200, 0)
FONTE_ENTRADA_ABERTA = "_entrada_aberta"      # source = "<provedor>_entrada_aberta"

MSG_PENDENTE_LIMITE = ("A IALD recebeu muitas contas novas nas últimas 24 horas. Seu pedido ficou "
                       "registrado para o operador; tente entrar de novo mais tarde.")
MSG_RECUSADO_ABERTA = "Este acesso foi bloqueado pelo operador da IALD."
MSG_EXPIRADO_ABERTA = "A entrada agora é direta. Entre de novo com a Apple ou o Google."
MSG_ENTRADA_INDISPONIVEL = "A entrada está indisponível agora. Tente de novo em alguns minutos."
NOTA_ENTRADA_FECHADA = "A IALD é experimental. Todo acesso é liberado pessoalmente pelo operador."
NOTA_ENTRADA_ABERTA = ("A IALD é experimental. Ao entrar com a Apple ou o Google, a conta começa no "
                       "uso gratuito, com um limite baixo de uso por dia.")

# Senha certa de conta bloqueada: _conferir_senha devolve isto (e não True), para a
# rota dizer "bloqueada" só a quem provou a senha.
SENHA_CONTA_BLOQUEADA = "bloqueada"

_ultimo_motivo_porta = [None]     # para avisar no log só quando o motivo MUDA

# ── 14/09/2026 (noite) — revisão ordem-régua, alto 3 e médio 10 ──
# A porta abria com a moderação desligada (o deploy está em IALD_MODERACAO=0: a chave não tem
# permissão de Moderations [DECLARADO]) e com o teto do grupo gratuito (US$ 2) MAIOR que o teto
# global declarado (US$ 1): os gratuitos esgotariam o motor externo de todos. Agora a porta só
# abre com a moderação ligada — salvo IALD_ENTRADA_SEM_MODERACAO=1, escolha explícita do
# operador [LEGAL: Google Play, ECA Digital, Apple 1.2] — e com o teto do gratuito ESTRITAMENTE
# menor que o global. Fechada por trava, o motivo sai legível em /api/entrar/config
# (`motivo_fechada`, texto para o público) e em /admin/api/entrada (técnico e público).
ENTRADA_SEM_MODERACAO = _segredo("IALD_ENTRADA_SEM_MODERACAO", "0").strip() == "1"
MOTIVO_FECHADA_MOTOR = "O serviço de IA do uso gratuito ainda não está pronto no servidor."
MOTIVO_FECHADA_MODERACAO = "A verificação de segurança das mensagens está desligada no servidor."
MOTIVO_FECHADA_TETO = "Os limites de gasto do uso gratuito não estão configurados com segurança."
# ── 14/09/2026 (noite) — tarefa SV; revisão COTAS, regressão 3 ──
# A porta abria com IALD_MEMORIA_MODO=atlas_integral — modo em que o prompt de TODA chamada leva o
# Atlas inteiro, com §V, §VI e §X, e em que todo pedido gratuito falhava com "não cabe na janela" —
# e com o plano gratuito zerado (tokens_dia, tokens_mes ou usd_dia ≤ 0, ou o teto global do
# gratuito ≤ 0): toda conta nascia sem uso possível. Agora a porta fica fechada nos dois casos, e o
# chat gratuito em atlas_integral recusa com aviso motor_indisponivel (MSG_GRATUITO_ATLAS_INTEGRAL).
MOTIVO_FECHADA_MEMORIA = "O modo de memória do servidor não é compatível com o uso gratuito."
MOTIVO_FECHADA_ZERADO = "Os limites de uso do plano gratuito estão zerados no servidor."


def _memoria_modo_integral(cfg):
    return str(getattr(cfg, "memoria_modo", "") or "").strip().lower() == "atlas_integral"


def _avaliar_entrada():
    """(aberta_de_fato, motivo técnico, motivo para o público). "" nos motivos = aberta,
    ou fechada porque o operador não ligou IALD_ENTRADA_ABERTA (aí o público não recebe motivo)."""
    if not ENTRADA_ABERTA:
        return False, "IALD_ENTRADA_ABERTA desligada", ""
    cfg = MOTORES_CFG
    modelo = iald_motores.modelo_para({"plano": iald_motores.GRATUITO}, cfg)
    if not cfg.chave:
        return False, "motor externo sem chave", MOTIVO_FECHADA_MOTOR
    if not PROMPT_EXTERNO:
        return False, "prompt canônico ilegível", MOTIVO_FECHADA_MOTOR
    if cfg.precos(modelo) is None:
        return False, f"sem preço para o modelo {modelo}", MOTIVO_FECHADA_MOTOR
    if cfg.reserva_nativa:
        return False, "IALD_OPENAI_RESERVA_NATIVA=1", MOTIVO_FECHADA_MOTOR
    if _memoria_modo_integral(cfg):
        return (False, "IALD_MEMORIA_MODO=atlas_integral (o Atlas inteiro, com §V, §VI e §X, iria no prompt "
                       "de toda chamada gratuita)", MOTIVO_FECHADA_MEMORIA)
    try:
        limites = iald_motores.limites_do_plano(cfg, iald_motores.GRATUITO)
    except (ValueError, TypeError, KeyError) as exc:
        return False, f"plano gratuito mal configurado ({exc})", MOTIVO_FECHADA_MOTOR
    for campo in ("tokens_dia", "tokens_mes", "usd_dia"):
        try:
            valor = float(limites[campo])
            zerado = not math.isfinite(valor) or valor <= 0
        except (TypeError, ValueError, KeyError):
            valor, zerado = limites.get(campo), True
        if zerado:
            return False, f"plano gratuito com {campo} = {valor} (precisa ser maior que 0)", MOTIVO_FECHADA_ZERADO
    if not MODERACAO_LIGADA and not ENTRADA_SEM_MODERACAO:
        return (False, "moderação desligada (IALD_MODERACAO=0) e IALD_ENTRADA_SEM_MODERACAO não é 1",
                MOTIVO_FECHADA_MODERACAO)
    try:
        teto_gratuito, teto_global = float(cfg.cota_global_gratuito_usd), float(cfg.cota_global_usd)
        seguro = math.isfinite(teto_gratuito) and math.isfinite(teto_global) and teto_gratuito < teto_global
        if seguro and teto_gratuito <= 0:
            return (False, f"teto global do uso gratuito zerado (US$ {teto_gratuito}/dia)", MOTIVO_FECHADA_ZERADO)
    except (TypeError, ValueError):
        teto_gratuito, teto_global, seguro = cfg.cota_global_gratuito_usd, cfg.cota_global_usd, False
    if not seguro:
        return (False, f"teto do uso gratuito (US$ {teto_gratuito}/dia) não é menor que o teto global "
                       f"(US$ {teto_global}/dia)", MOTIVO_FECHADA_TETO)
    return True, "", ""


def _estado_entrada():
    """(aberta_de_fato, motivo). Chamado NA REQUISIÇÃO.

    Fechada se o operador não ligou IALD_ENTRADA_ABERTA, ou se o motor externo não está
    pronto para receber estranhos: sem chave, sem prompt canônico, sem preço do modelo
    do plano gratuito, com a reserva nativa ligada (ela existe para cair na máquina do
    operador — o contrário da porta aberta) ou com o plano gratuito mal configurado.
    14/09/2026 (noite): também com a moderação desligada (sem IALD_ENTRADA_SEM_MODERACAO=1)
    ou com o teto do gratuito maior ou igual ao global — ver _avaliar_entrada.
    """
    aberta, motivo, _publico = _avaliar_entrada()
    if ENTRADA_ABERTA and motivo != _ultimo_motivo_porta[0]:
        _ultimo_motivo_porta[0] = motivo
        if motivo:
            print(f"[entrada] AVISO: IALD_ENTRADA_ABERTA=1, mas a porta fica FECHADA: {motivo}", flush=True)
        elif not MODERACAO_LIGADA:
            print("[entrada] AVISO: porta aberta SEM moderação (IALD_ENTRADA_SEM_MODERACAO=1)", flush=True)
        else:
            print("[entrada] porta aberta: contas novas entram no plano gratuito", flush=True)
    return aberta, ("" if aberta else motivo)


def _segredo_da_casa():
    """O segredo das chaves HMAC de cota e de IP: o mesmo da sessão (app.secret_key).
    ⚠ O botão "limpar sessões" do painel troca esse segredo: contas já criadas guardam
    a `cota_chave` e não mudam; uma conta RECRIADA depois da troca ganha chave nova."""
    return app.secret_key


def _destino_web(username):
    """One conversation interface for web and mobile, independent of account/model."""
    pending = session.pop('pending_artifact_id', '')
    if username and isinstance(pending, str) and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', pending):
        return '/app/index.html?artifact=' + pending
    return '/app/index.html'


_jwks_clientes = {}


def _cliente_jwks(provedor):
    """Chaves públicas do provedor (PyJWKClient faz o próprio cache)."""
    if provedor not in _jwks_clientes:
        from jwt import PyJWKClient
        _jwks_clientes[provedor] = PyJWKClient(identidade.JWKS_URL[provedor])
    return _jwks_clientes[provedor]


def _audiencias(provedor):
    if provedor == "apple":
        return [a for a in (APPLE_BUNDLE_ID, APPLE_SERVICE_ID) if a]
    return [GOOGLE_OAUTH_CLIENT_ID] if GOOGLE_OAUTH_CLIENT_ID else []


def _verificar_token_provedor(provedor, token, nonce=None):
    """(claims, erro). Ponto ÚNICO de verificação — os testes trocam só esta função."""
    return identidade.verificar_id_token(token, provedor, _audiencias(provedor),
                                         _cliente_jwks(provedor), nonce=nonce)


from iald_owner_apple_auth import AuthDenied as _OwnerAuthDenied
from iald_owner_apple_adapter import ServerAdapter as _OwnerServerAdapter
_OWNER_ADAPTER = None
_OWNER_CONSOLIDATION = None
_OWNER_ADAPTER_LOCK = threading.Lock()

def _owner_adapter():
    global _OWNER_ADAPTER
    with _OWNER_ADAPTER_LOCK:
        if _OWNER_ADAPTER is None:
            _OWNER_ADAPTER = _OwnerServerAdapter(globals())
    return _OWNER_ADAPTER

def require_owner_apple(capability="private.read"):
    # Gateway must call for every read/enqueue and before integrating async results.
    # An exception is a refusal; never fall back to admin/name/email.
    return _owner_adapter().require_owner_apple(capability)

def require_owner_private(capability="private.read"):
    return require_owner_apple(capability)

@app.route("/api/owner/apple-challenge", methods=["POST"])
def api_owner_apple_challenge():
    try:
        response = jsonify(_owner_adapter().auth.challenge())
        response.headers["Cache-Control"] = "no-store"
        return response
    except _OwnerAuthDenied:
        return jsonify({"error": "Reautenticação indisponível."}), 503


def _provedores_configurados():
    return {
        "apple_nativo": bool(APPLE_BUNDLE_ID),
        "apple_web": bool(APPLE_SERVICE_ID),
        "google": bool(GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET),
        "senha": True,
    }


def _serializador(salt):
    from itsdangerous import URLSafeTimedSerializer
    return URLSafeTimedSerializer(app.secret_key, salt=salt)


def _ip_real():
    # Atrás do cloudflared TODA requisição chega de 127.0.0.1; o IP da pessoa vem
    # no cabeçalho da Cloudflare. Sem isto o limite de senha seria um limite global.
    return (request.headers.get("CF-Connecting-IP") or request.remote_addr or "?").strip()


def _resolver_identidade(provedor, sub, email="", nome="", superficie="", modo="tentativa"):
    """Situação de uma identidade assinada.

    modo="tentativa": a pessoa acabou de se autenticar — registra/atualiza o pedido e, com a
                      porta aberta, cria a conta do plano gratuito.
    modo="consulta":  só lê (app verificando se já foi liberado) — nunca cria pedido nem conta.
    Devolve (situacao, username, pedido) com situacao ∈
    ativo|pendente|recusado|expirado|bloqueado|indisponivel.

    14/09/2026 (noite): tudo numa seção crítica só — usuários primeiro, pedidos depois, e a
    ordem das travas nunca se inverte. É ela que faz o iPhone e o iPad entrando no mesmo
    segundo com o mesmo Apple ID criarem UMA conta.
    """
    with _TRAVA_USUARIOS:
        try:
            usuarios = load_users_estrito()
        except UsuariosIlegiveis as exc:
            # 14/09/2026 (noite): sem ler o arquivo não se sabe se a identidade tem dono nem se
            # a conta está bloqueada — nada é decidido nem registrado
            auth_log("ENTRADA_SEM_LEITURA", "", f"via={provedor} motivo={exc}")
            return "indisponivel", "", None
        dono = identidade.usuario_da_identidade(usuarios, provedor, sub)
        if dono:
            if _conta_bloqueada(usuarios.get(dono)):
                return "bloqueado", dono, None
            if modo == "tentativa":
                from iald_registration_identity import login_missing_fields
                delta = login_missing_fields(usuarios, dono, provedor, sub,
                    name=nome, email=email, validated=True, active=True, blocked=False, mode=modo)
                if delta:
                    updated = dict(usuarios)
                    updated[dono] = dict(usuarios[dono], **delta)
                    try:
                        if save_users(updated) is False:
                            return "indisponivel", "", None
                    except (OSError, ValueError, UsuariosNaoGravados):
                        return "indisponivel", "", None
            return "ativo", dono, None
        if modo == "consulta":
            vigente = PEDIDOS.da_identidade(provedor, sub)
            if not vigente or vigente.get("status") == identidade.APROVADO:
                # aprovado sem dono = o usuário foi excluído depois; não se reabre sozinho
                return "expirado", "", vigente
            if vigente.get("status") == identidade.RECUSADO:
                return "recusado", "", vigente
            return "pendente", "", vigente
        aberta, _motivo = _estado_entrada()
        ip_chave = ""
        if aberta:
            try:
                ip_chave = identidade.chave_de_ip(_segredo_da_casa(), _ip_real())
            except ValueError:
                ip_chave = ""
        vigente = PEDIDOS.registrar(provedor, sub, email=email, nome=nome, superficie=superficie,
                                    ip_chave=ip_chave)
        if vigente.get("status") == identidade.RECUSADO:
            return "recusado", "", vigente
        if not aberta:
            return "pendente", "", vigente
        # porta aberta: a lista de bloqueio vale mesmo se houver outro pedido vivo (fail-closed)
        if PEDIDOS.recusado_da_identidade(provedor, sub):
            return "recusado", "", vigente
        return _criar_conta_aberta(provedor, sub, email, nome, vigente, ip_chave)


def _criar_conta_aberta(provedor, sub, email, nome, vigente, ip_chave):
    """A conta do plano gratuito, criada sozinha. Chamada DENTRO de _TRAVA_USUARIOS.

    Estourou o limite de criação (por IP ou global, 24 h) → o pedido fica pendente, sem
    conta. Arquivo de usuários ilegível ou sem administrador → nada é gravado
    ("indisponivel"). A senha é aleatória e ninguém a conhece: a conta entra pela identidade.
    """
    desde = (datetime.now() - timedelta(hours=24)).isoformat(timespec="seconds")
    try:
        global_24h = PEDIDOS.contar_criacoes(desde)
        do_ip_24h = PEDIDOS.contar_criacoes(desde, ip_chave=ip_chave)
    except (OSError, ValueError) as exc:
        print(f"[entrada] contagem de criações ilegível ({exc}); nenhuma conta criada", flush=True)
        return "indisponivel", "", vigente
    if global_24h >= NOVAS_GLOBAL_24H or do_ip_24h >= NOVAS_POR_IP_24H:
        # o IP da pessoa só aparece no log como o começo da chave HMAC (atrás do túnel o
        # remote_addr seria sempre 127.0.0.1, e o IP em claro não se registra)
        auth_log("ENTRADA_LIMITE_DE_CRIACAO", "", f"via={provedor} pedido={vigente.get('id', '?')} "
                 f"global_24h={global_24h}/{NOVAS_GLOBAL_24H} ip_24h={do_ip_24h}/{NOVAS_POR_IP_24H}",
                 ip="hmac:" + (ip_chave[:12] or "?"))
        # 14/09/2026 (noite — contrato d): o pedido guarda que ficou pendente POR LIMITE; a consulta
        # do app devolve `pending` (motivo "limite") em vez de `expired`. Falha ao marcar não muda a
        # resposta desta tentativa; só a consulta seguinte cairia no `expired` de antes.
        try:
            vigente = PEDIDOS.marcar_pendente_por_limite(vigente["id"]) or vigente
        except Exception as exc:          # noqa: BLE001
            print(f"[entrada] pedido {vigente.get('id', '?')} não marcado como limite ({exc})", flush=True)
            vigente = dict(vigente, motivo_pendente=identidade.MOTIVO_LIMITE)
        return "pendente", "", vigente
    try:
        usuarios = _carregar_usuarios_para_escrita()
    except UsuariosIlegiveis as exc:
        auth_log("ENTRADA_ABERTA_SEM_ESCRITA", "", f"via={provedor} motivo={exc}")
        return "indisponivel", "", vigente
    dono = identidade.usuario_da_identidade(usuarios, provedor, sub)
    if dono:        # a leitura comum, lá em cima, pode ter visto {} num tropeço do disco
        return ("bloqueado" if _conta_bloqueada(usuarios.get(dono)) else "ativo"), dono, None
    try:
        chave = identidade.chave_cota(_segredo_da_casa(), provedor, sub)
    except ValueError as exc:
        print(f"[entrada] chave de cota indisponível ({exc}); nenhuma conta criada", flush=True)
        return "indisponivel", "", vigente
    try:
        # 14/09/2026 (noite) — BAIXO 3: nome de conta excluída não volta (Ψ-NET e TGLC são por nome)
        lapide = PEDIDOS.nomes_indisponiveis()
    except (OSError, ValueError) as exc:
        print(f"[entrada] lápide de nomes ilegível ({exc}); nenhuma conta criada", flush=True)
        return "indisponivel", "", vigente
    nome_conta = identidade.sugerir_username_aberto(usuarios, email, nome, indisponiveis=lapide)
    usuarios[nome_conta] = {
        "password_hash": generate_password_hash(secrets.token_urlsafe(32)),
        "admin": False,
        "sacred_language": False,
        "created": datetime.now().isoformat(),
        "name": nome or "",
        "email": email or "",
        "source": f"{provedor}{FONTE_ENTRADA_ABERTA}",
        "identidades": [],
        "plano": iald_motores.GRATUITO,
        "motor": iald_motores.OPENAI,
        # a cota é da IDENTIDADE, não do nome: excluir e voltar não devolve o que já foi usado
        "cota_chave": chave,
    }
    ok, erro = identidade.vincular(usuarios, nome_conta, provedor, sub, email)
    if not ok:
        usuarios.pop(nome_conta, None)
        print(f"[entrada] vínculo recusado na criação aberta: {erro}", flush=True)
        return "indisponivel", "", vigente
    try:
        save_users(usuarios)
    except Exception as exc:          # noqa: BLE001 — falha visível, conta não nasce
        usuarios.pop(nome_conta, None)
        print(f"[entrada] falha ao gravar a conta nova ({type(exc).__name__}); nenhuma conta criada", flush=True)
        return "indisponivel", "", vigente
    try:
        PEDIDOS.marcar_aprovado(vigente["id"], nome_conta, identidade.POR_ENTRADA_ABERTA)
    except Exception as exc:          # noqa: BLE001
        print(f"[entrada] conta {nome_conta} criada, mas o pedido não foi marcado ({exc}); "
              "ela não entra na contagem de criações", flush=True)
    auth_log("CONTA_CRIADA_ENTRADA_ABERTA", nome_conta, f"via={provedor} pedido={vigente.get('id', '?')}",
             ip="hmac:" + (ip_chave[:12] or "?"))
    return "ativo", nome_conta, None


def _abrir_sessao_web(username, owner_proof=""):
    """Sessão por cookie na web — o mesmo contrato do require_auth (auth_version)."""
    # leitura estrita (14/09/2026, noite): com {} a conta gratuita parecia "assinante" e
    # ganhava o crédito inicial TGL abaixo; agora o tropeço do disco é 503
    dados = load_users_estrito().get(username) or {}
    pending=session.get('pending_artifact_id','')
    session.clear()
    if re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',pending):
        session['pending_artifact_id']=pending
    session.permanent = True
    session["auth_version"] = hashlib.sha256(dados.get("password_hash", "").encode()).hexdigest()
    session["owner_sid"] = _owner_adapter().bind(owner_proof, username)
    session["authenticated"] = True
    session["username"] = username
    session["is_admin"] = bool(dados.get("admin", False))
    session["last_active"] = datetime.now().isoformat()
    # 14/09/2026 (noite): conta do plano gratuito NÃO ganha o crédito inicial TGL na
    # entrada (decisão a ratificar pelo operador). ⚠ O razão TGL ainda cria a conta — com
    # o crédito inicial — na primeira medição de uso ou na primeira leitura do saldo.
    if COIN_AVAILABLE and iald_motores.plano_de(dados) != iald_motores.GRATUITO:
        try:
            coin_engine.ensure_account(username)
        except Exception as exc:          # noqa: BLE001 — crédito nunca derruba a entrada
            print(f"[entrada] ensure_account falhou para {username}: {exc}", flush=True)


def _resposta_entrada(situacao, username="", pedido=None, provedor="", sub="", owner_proof=""):
    """Resposta JSON única do app. `detalhe` mantém compatível a build 4.1 (13)."""
    if situacao == "ativo":
        registro = load_users_estrito().get(username) or {}     # ver _abrir_sessao_web
        plano = iald_motores.plano_de(registro)
        if COIN_AVAILABLE and plano != iald_motores.GRATUITO:     # ver _abrir_sessao_web
            try:
                coin_engine.ensure_account(username)
            except Exception as exc:      # noqa: BLE001
                print(f"[entrada] ensure_account falhou para {username}: {exc}", flush=True)
        token = _emitir_token_app(username, owner_proof=owner_proof)
        if not token:
            return jsonify({"status": "error", "error": "Falha ao emitir a sessão"}), 500
        auth_log("ENTRADA_OK", username, f"via={provedor or 'senha'}")
        return jsonify({"status": "active", "username": username, "token": token,
                        "token_max_age": TOKEN_APP_MAX_AGE, "plano": plano}), 200
    pid = (pedido or {}).get("id", "?")
    if situacao == "bloqueado":
        auth_log("ENTRADA_CONTA_BLOQUEADA", username, f"via={provedor}")
        return jsonify({"status": "rejected", "motivo": "bloqueado",
                        "error": MSG_BLOQUEADO, "detalhe": MSG_BLOQUEADO}), 403
    if situacao == "indisponivel":
        return jsonify({"status": "error", "error": MSG_ENTRADA_INDISPONIVEL,
                        "detalhe": MSG_ENTRADA_INDISPONIVEL}), 503
    aberta = _estado_entrada()[0]
    if situacao == "recusado":
        auth_log("ENTRADA_RECUSADA", "", f"via={provedor} pedido={pid}")
        msg = MSG_RECUSADO_ABERTA if aberta else MSG_RECUSADO
        return jsonify({"status": "rejected", "motivo": "recusado", "error": msg, "detalhe": msg}), 403
    if situacao == "expirado":
        msg = MSG_EXPIRADO_ABERTA if aberta else MSG_EXPIRADO
        return jsonify({"status": "expired", "error": msg, "detalhe": msg}), 410
    auth_log("ENTRADA_PENDENTE", "", f"via={provedor} pedido={pid}")
    # com a porta aberta, pendente só nasce do limite de criação
    msg = MSG_PENDENTE_LIMITE if aberta else MSG_PENDENTE
    corpo = {
        "status": "pending", "mensagem": msg, "detalhe": msg,
        "pedido": _serializador(PEDIDO_SALT).dumps({"p": provedor, "s": sub}) if provedor and sub else "",
    }
    if aberta and (pedido or {}).get("motivo_pendente") == identidade.MOTIVO_LIMITE:
        corpo["motivo"] = identidade.MOTIVO_LIMITE          # contrato d (14/09/2026, noite)
    return jsonify(corpo), 202


def _corpo_json():
    dados = request.get_json(force=True, silent=True)
    return dados if isinstance(dados, dict) else None


def _conferir_senha(usuario, senha):
    """True/False, ou None se a origem ou a conta estiverem bloqueadas por excesso de falhas.

    14/09/2026 (noite): senha CERTA de conta que o operador bloqueou devolve
    SENHA_CONTA_BLOQUEADA (texto não vazio — quem chama precisa testá-lo ANTES de `if certo`).
    Senha errada de conta bloqueada continua sendo só False: não se revela o bloqueio
    a quem não provou a senha.
    """
    chave_ip = f"{_ip_real()}|{usuario}"
    if LIMITE_SENHA.bloqueado(chave_ip) or LIMITE_SENHA_CONTA.bloqueado(usuario):
        auth_log("LOGIN_BLOQUEADO", _nome_para_log(usuario), "excesso de tentativas")
        return None
    # leitura estrita (14/09/2026, noite): o tropeço do disco é 503 e não conta como senha errada
    dados = load_users_estrito().get(usuario)
    # Sem conta, confere contra um hash qualquer: o tempo de resposta não revela
    # quais nomes de usuário existem.
    alvo = (dados or {}).get("password_hash") or _HASH_FANTASMA
    certo = check_password_hash(alvo, senha or "") and bool(dados)
    if certo:
        LIMITE_SENHA.acertou(chave_ip)
        if _conta_bloqueada(dados):
            return SENHA_CONTA_BLOQUEADA
        return True
    LIMITE_SENHA.falhou(chave_ip)
    LIMITE_SENHA_CONTA.falhou(usuario)
    return False


_HASH_FANTASMA = generate_password_hash(secrets.token_urlsafe(24))


# ── configuração pública: o app decide quais botões mostrar ──
@app.route("/api/entrar/config")
def api_entrar_config():
    # 14/09/2026 (noite): o app também lê se a porta está aberta DE FATO e a nota que
    # descreve a entrada (antes fixa no app: "todo acesso é liberado pelo operador")
    aberta = _estado_entrada()[0]
    dados = _provedores_configurados()
    dados.update({"entrada_aberta": aberta,
                  "nota": NOTA_ENTRADA_ABERTA if aberta else NOTA_ENTRADA_FECHADA})
    # contrato d (14/09/2026, noite): ligada pelo operador e fechada por trava → o motivo, em texto
    # para o público (sem nome de variável nem detalhe do servidor)
    publico = _avaliar_entrada()[2] if ENTRADA_ABERTA and not aberta else ""
    if publico:
        dados["motivo_fechada"] = publico
    return jsonify(dados)


# Display metadata informed by the person; never civil identity or authorization.
def _identificacao_json_post(allowed):
    if not request.is_json:
        return None, (jsonify({'error': 'Envie JSON.'}), 415)
    origin = request.headers.get('Origin', '')
    allowed_origins = set(ORIGENS_APP) | {URL_PUBLICA.rstrip('/'), request.host_url.rstrip('/')}
    if ((origin and origin not in allowed_origins)
            or (not origin and not getattr(g, 'app_bearer', False))
            or request.headers.get('Sec-Fetch-Site') == 'cross-site' and origin not in ORIGENS_APP):
        return None, (jsonify({'error': 'Origem não permitida.'}), 403)
    if ((request.content_length is not None and request.content_length > 8192)
            or len(request.get_data(cache=True)) > 8192):
        return None, (jsonify({'error': 'Corpo muito grande.'}), 413)
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not set(data) <= allowed:
        return None, (jsonify({'error': 'Campos inválidos.'}), 400)
    return data, None


def _identificacao_response(name, provider, email, username=''):
    from iald_registration_identity import usable_name
    import iald_sync_central as _identity_sc
    shown = name if usable_name(name, username) else ''
    response = jsonify({'nome': shown, 'provedor': provider,
                        'email_mascarado': _identity_sc.mascarar_email(email),
                        'nome_necessario': not bool(shown)})
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/api/conta/identificacao', methods=['GET', 'POST'])
def api_conta_identificacao():
    from iald_registration_identity import project_identity, validate_name
    data = None
    if request.method == 'POST':
        data, error = _identificacao_json_post({'nome'})
        if error is not None:
            return error
        try:
            name = validate_name(data.get('nome'))
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
    username = session.get('username', '')
    with _TRAVA_USUARIOS:
        users = load_users_estrito()
        record = users.get(username)
        if not isinstance(record, dict):
            return jsonify({'error': 'Não autenticado.'}), 401
        if _conta_bloqueada(record):
            return jsonify({'error': 'Conta indisponível.'}), 403
        if data is not None:
            updated = dict(record, name=name)
            candidate = dict(users)
            candidate[username] = updated
            try:
                if save_users(candidate) is False:
                    return jsonify({'error': 'Não foi possível salvar o nome.'}), 503
            except (OSError, ValueError, UsuariosNaoGravados):
                return jsonify({'error': 'Não foi possível salvar o nome.'}), 503
            record = updated
        projected = project_identity(record, username, PEDIDOS.listar())
        providers = {i.get('provedor') for i in identidade.identidades_publicas(record)
                     if i.get('provedor') in ('apple', 'google')}
        provider = next(iter(providers)) if len(providers) == 1 else ('multiplos' if providers else 'senha')
        return _identificacao_response(projected['name'], provider, projected['email'], username)


@app.route('/api/entrar/identificacao', methods=['POST'])
def api_entrar_identificacao():
    from iald_registration_identity import validate_name
    data, error = _identificacao_json_post({'pedido', 'nome'})
    if error is not None:
        return error
    token = data.get('pedido')
    try:
        if not isinstance(token, str) or not token or len(token) > 4096:
            raise ValueError('Invalid reference')
        ref = _serializador(PEDIDO_SALT).loads(token, max_age=PEDIDO_MAX_AGE)
        if (not isinstance(ref, dict) or ref.get('p') not in ('apple', 'google')
                or not isinstance(ref.get('s'), str) or not ref['s']):
            raise ValueError('Invalid reference')
    except Exception:
        return jsonify({'error': 'Pedido expirado ou inválido.'}), 410
    name = None
    if 'nome' in data:
        try:
            name = validate_name(data['nome'])
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
    # Same lock order as approval: users first, requests second. No grants here.
    with _TRAVA_USUARIOS:
        users = load_users_estrito()
        owner = identidade.usuario_da_identidade(users, ref['p'], ref['s'])
        if owner:
            return jsonify({'error': 'Pedido não está pendente.'}), 409
        try:
            pending = PEDIDOS.identificacao_pendente(ref['p'], ref['s'])
            # Match /api/entrar/situacao: an old closed-door request is expired
            # once entry is open, unless it is still pending because of quota.
            if (_estado_entrada()[0]
                    and pending.get('motivo_pendente') != identidade.MOTIVO_LIMITE):
                return jsonify({'error': 'Pedido expirado. Entre de novo.'}), 410
            if name is not None:
                pending = PEDIDOS.identificacao_pendente(ref['p'], ref['s'], nome=name)
        except PermissionError:
            return jsonify({'error': 'Pedido não está pendente.'}), 409
        except (OSError, ValueError):
            return jsonify({'error': 'Pedido indisponível.'}), 503
        return _identificacao_response(pending.get('nome', ''), ref['p'], pending.get('email', ''))


# ── iPhone/iPad: Sign in with Apple nativo ──
@app.route("/api/entrar/apple", methods=["POST"])
@app.route("/api/apple-signin", methods=["POST"], endpoint="api_apple_signin")
def api_entrar_apple():
    """identityToken do Sign in with Apple nativo → ativo | pendente | recusado.

    /api/apple-signin fica como sinônimo: a build 4.1 (13), já instalada, chama esse
    nome e mostra o `detalhe` quando a resposta não é `active`.
    """
    dados = _corpo_json()
    if dados is None:
        return jsonify({"error": "JSON inválido"}), 400
    token = str(dados.get("identity_token") or "").strip()
    if not token:
        return jsonify({"error": "identity_token obrigatório"}), 400
    claims, erro = _verificar_token_provedor("apple", token)
    if erro:
        auth_log("ENTRADA_APPLE_TOKEN_RECUSADO", "", erro)
        return jsonify({"error": "Autenticação Apple inválida", "detalhe": erro}), 401
    sub = str(claims["sub"]).strip()
    nome = str(dados.get("name") or dados.get("nome") or "").strip()[:80]
    situacao, username, pedido = _resolver_identidade(
        "apple", sub, email=str(claims.get("email") or "").strip(), nome=nome, superficie="app")
    try:
        proof = _owner_adapter().native_proof(dados, token)
    except _OwnerAuthDenied:
        return jsonify({"error": "Reautenticação Apple necessária."}), 401
    return _resposta_entrada(situacao, username, pedido, "apple", sub, owner_proof=proof)


@app.route("/api/dispositivo-signin", methods=["POST"])
def api_dispositivo_signin():
    # 14/09/2026 (noite): o texto antigo ("todo acesso à IALD é liberado pelo operador")
    # deixou de ser verdade com a porta aberta. A razão do desligamento continua.
    msg = ("A entrada anônima por aparelho foi descontinuada em 14/09/2026: um código "
           "inventado pelo próprio aparelho não é uma identidade que o operador possa "
           "liberar ou bloquear. Entre com Google, Apple, ou usuário e senha.")
    return jsonify({"error": msg, "detalhe": msg}), 410


# ── usuário e senha no app (contas criadas pelo operador) ──
@app.route("/api/entrar/senha", methods=["POST"])
def api_entrar_senha():
    dados = _corpo_json()
    if dados is None:
        return jsonify({"error": "JSON inválido"}), 400
    usuario = str(dados.get("usuario") or dados.get("username") or "").strip().lower()
    senha = str(dados.get("senha") or dados.get("password") or "")
    if not usuario or not senha:
        return jsonify({"status": "error", "error": "Informe usuário e senha."}), 400
    certo = _conferir_senha(usuario, senha)
    if certo is None:
        return jsonify({"status": "error",
                        "error": "Muitas tentativas. Aguarde alguns minutos e tente de novo."}), 429
    if certo == SENHA_CONTA_BLOQUEADA:
        return _resposta_entrada("bloqueado", usuario, None, "senha")
    if not certo:
        auth_log("LOGIN_FAIL", _nome_para_log(usuario), "via=app")
        return jsonify({"status": "error", "error": "Usuário ou senha incorretos."}), 401
    # nunca cria conta: senha só existe para contas que o operador criou
    return _resposta_entrada("ativo", usuario, None, "senha")


# ── o app troca o bilhete (recebido pelo link br.ia.iald://) pela sessão ──
@app.route("/api/entrar/bilhete", methods=["POST"])
def api_entrar_bilhete():
    dados = _corpo_json()
    if dados is None:
        return jsonify({"error": "JSON inválido"}), 400
    carga, erro = BILHETES.resgatar(str(dados.get("bilhete") or ""), str(dados.get("verificador") or ""))
    if erro:
        auth_log("BILHETE_RECUSADO", "", erro)
        return jsonify({"status": "error", "error": "Não foi possível concluir a entrada. Tente de novo.",
                        "detalhe": erro}), 400
    if carga.get("situacao") == "erro":
        return jsonify({"status": "error", "error": carga.get("mensagem") or "Entrada não concluída."}), 400
    provedor, sub = carga.get("provedor", ""), carga.get("sub", "")
    situacao, username, pedido = _resolver_identidade(provedor, sub, modo="consulta")
    return _resposta_entrada(situacao, username, pedido, provedor, sub,
                             owner_proof=carga.get("owner_proof", ""))


# ── o app pergunta se o pedido já foi liberado ──
@app.route("/api/entrar/situacao", methods=["POST"])
def api_entrar_situacao():
    dados = _corpo_json()
    if dados is None:
        return jsonify({"error": "JSON inválido"}), 400
    try:
        ref = _serializador(PEDIDO_SALT).loads(str(dados.get("pedido") or ""), max_age=PEDIDO_MAX_AGE)
        provedor, sub = ref["p"], ref["s"]
    except Exception:
        return jsonify({"status": "expired", "error": MSG_EXPIRADO, "detalhe": MSG_EXPIRADO}), 410
    situacao, username, pedido = _resolver_identidade(provedor, sub, modo="consulta")
    if (situacao == "pendente" and _estado_entrada()[0]
            and (pedido or {}).get("motivo_pendente") != identidade.MOTIVO_LIMITE):
        # 14/09/2026 (noite): com a porta aberta, o pedido guardado de antes não espera
        # mais liberação — a pessoa entra de novo (a consulta nunca cria conta sem
        # autenticação nova). A build instalada já trata `expired`.
        # ⚠ Menos o pedido retido pelo LIMITE de criação (contrato d, mesma noite): ele segue
        # `pending` com motivo "limite" — antes o app virava "entre de novo", a pessoa entrava,
        # caía no limite outra vez e ficava num laço (revisão de interface M1, reproduzido).
        situacao = "expirado"
    return _resposta_entrada(situacao, username, pedido, provedor, sub)


# ── web e Android: entrada pelo navegador (Apple e Google) ──
def _url_retorno(provedor):
    return f"{URL_PUBLICA}/auth/{provedor}/retorno"


def _vinculo_navegador(nonce):
    return hashlib.sha256(("entrada:" + nonce).encode()).hexdigest()[:40]


@app.route("/auth/<provedor>/iniciar", endpoint="auth_iniciar")
def auth_iniciar(provedor):
    if provedor not in identidade.PROVEDORES:
        return make_response(_pagina_entrada("Provedor desconhecido.", "erro")), 404
    origem = "app" if request.args.get("origem") == "app" else "web"
    desafio = str(request.args.get("desafio") or "")
    if origem == "app" and not re.fullmatch(r"[A-Za-z0-9_-]{43}", desafio):
        return make_response(_pagina_entrada(
            "Link de entrada inválido. Volte ao aplicativo e tente de novo.", "erro")), 400
    configurado = APPLE_SERVICE_ID if provedor == "apple" else (GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET)
    if not configurado:
        return make_response(_pagina_entrada(
            f"A entrada com {'Apple' if provedor == 'apple' else 'Google'} ainda não foi configurada "
            "neste servidor.", "erro")), 503
    # O provedor devolve a pessoa no URL_PUBLICA; o vínculo do navegador tem de nascer
    # no MESMO domínio, senão o cookie não volta.
    publica = urlparse(URL_PUBLICA)
    if request.host.split(":")[0].lower() != (publica.hostname or "").lower():
        return redirect(f"{URL_PUBLICA}/auth/{provedor}/iniciar?{request.query_string.decode('ascii', 'ignore')}")

    nonce = secrets.token_urlsafe(24)
    payload = {"p": provedor, "o": origem, "d": desafio, "n": nonce}
    consolidation = request.args.get("owner_consolidation", "")
    if consolidation:
        if provedor != "apple" or origem != "web" or _OWNER_CONSOLIDATION is None:
            return make_response("CONSOLIDATION_REFUSED", 403)
        try:
            payload.update(_OWNER_CONSOLIDATION.before_oauth(consolidation, nonce))
        except Exception:
            return make_response("CONSOLIDATION_REFUSED", 403)
    estado = _serializador(ESTADO_SALT).dumps(payload)
    if provedor == "apple":
        destino = "https://appleid.apple.com/auth/authorize?" + _urlencode({
            "response_type": "code id_token", "response_mode": "form_post",
            "client_id": APPLE_SERVICE_ID, "redirect_uri": _url_retorno("apple"),
            "scope": "name email", "state": estado, "nonce": nonce,
        }, quote_via=_quote)
    else:
        destino = "https://accounts.google.com/o/oauth2/v2/auth?" + _urlencode({
            "response_type": "code", "client_id": GOOGLE_OAUTH_CLIENT_ID,
            "redirect_uri": _url_retorno("google"), "scope": "openid email profile",
            "state": estado, "nonce": nonce, "prompt": "select_account",
        }, quote_via=_quote)
    resp = redirect(destino)
    if origem == "web":
        # SameSite=None: a Apple devolve por POST vindo de appleid.apple.com, e um
        # cookie Lax não viajaria nesse retorno.
        resp.set_cookie(COOKIE_ENTRADA, _vinculo_navegador(nonce), max_age=600, secure=True,
                        httponly=True, samesite="None", path="/auth")
    return resp


def _ler_estado(bruto, provedor):
    try:
        estado = _serializador(ESTADO_SALT).loads(str(bruto or ""), max_age=600)
    except Exception:
        return None
    if not isinstance(estado, dict) or estado.get("p") != provedor:
        return None
    if estado.get("o") == "web":
        vinculo = request.cookies.get(COOKIE_ENTRADA, "")
        if not vinculo or not hmac.compare_digest(vinculo, _vinculo_navegador(estado.get("n", ""))):
            return None
    return estado


def _concluir_navegador(estado, situacao, username="", provedor="", sub="", mensagem="", owner_proof=""):
    if estado.get("o") == "app":
        carga = ({"situacao": "erro", "mensagem": mensagem} if situacao == "erro"
                 else {"situacao": situacao, "provedor": provedor, "sub": sub})
        if situacao == "ativo" and owner_proof:
            carga["owner_proof"] = owner_proof
        bilhete = BILHETES.emitir(estado.get("d", ""), carga)
        return make_response(_pagina_volta_app(f"{ESQUEMA_APP}://entrar?bilhete={bilhete}"))
    aberta = _estado_entrada()[0]
    if situacao == "ativo":
        _abrir_sessao_web(username, owner_proof=owner_proof)
        auth_log("ENTRADA_OK", username, f"via={provedor} (web)")
        # 14/09/2026 (noite): conta no motor OpenAI vai ao app web, que pede o consentimento
        resp = redirect(_destino_web(username))
    elif situacao == "pendente":
        resp = make_response(_pagina_entrada(MSG_PENDENTE_LIMITE if aberta else MSG_PENDENTE, "pendente"))
    elif situacao == "recusado":
        resp = make_response(_pagina_entrada(MSG_RECUSADO_ABERTA if aberta else MSG_RECUSADO, "erro"), 403)
    elif situacao == "bloqueado":
        auth_log("ENTRADA_CONTA_BLOQUEADA", username, f"via={provedor} (web)")
        resp = make_response(_pagina_entrada(MSG_BLOQUEADO, "erro"), 403)
    elif situacao == "indisponivel":
        resp = make_response(_pagina_entrada(MSG_ENTRADA_INDISPONIVEL, "erro"), 503)
    else:
        resp = make_response(_pagina_entrada(mensagem or "Entrada não concluída.", "erro"), 400)
    resp.delete_cookie(COOKIE_ENTRADA, path="/auth")
    return resp


@app.route("/auth/apple/retorno", methods=["POST"], endpoint="auth_apple_retorno")
def auth_apple_retorno():
    estado = _ler_estado(request.form.get("state"), "apple")
    if not estado:
        return make_response(_pagina_entrada(
            "A entrada expirou ou veio de outro navegador. Tente de novo.", "erro")), 400
    if estado.get("owner_consolidation"):
        from r5_http import safe as _r5_safe
        if _OWNER_CONSOLIDATION is None:
            return make_response("CONSOLIDATION_UNAVAILABLE", 503)
        response = _r5_safe(_OWNER_CONSOLIDATION.web_callback)(
            estado, request.form.get("id_token", ""), bool(request.form.get("error")))
        response.delete_cookie(COOKIE_ENTRADA, path="/auth")
        return response
    if request.form.get("error"):
        return _concluir_navegador(estado, "erro", mensagem="Entrada com Apple cancelada.")
    claims, erro = _verificar_token_provedor("apple", request.form.get("id_token", ""), nonce=estado["n"])
    if erro:
        auth_log("ENTRADA_APPLE_TOKEN_RECUSADO", "", erro)
        return _concluir_navegador(estado, "erro", mensagem="Não foi possível confirmar a entrada com Apple.")
    nome = ""
    try:   # a Apple manda o nome só na PRIMEIRA autorização, num campo `user` em JSON
        u = json.loads(request.form.get("user") or "{}").get("name") or {}
        nome = " ".join(x for x in (u.get("firstName"), u.get("lastName")) if x).strip()[:80]
    except Exception:
        pass
    sub = str(claims["sub"]).strip()
    situacao, username, _ = _resolver_identidade(
        "apple", sub, email=str(claims.get("email") or ""), nome=nome, superficie=estado["o"])
    try:
        proof = _owner_adapter().web_proof(request.form.get("id_token", ""), estado["n"])
    except _OwnerAuthDenied:
        return _concluir_navegador(estado, "erro", mensagem="Reautenticação Apple necessária.")
    return _concluir_navegador(estado, situacao, username, "apple", sub, owner_proof=proof)


def _trocar_codigo_google(codigo):
    """Troca o código de autorização pelo id_token. Isolada para os testes."""
    r = req_lib.post("https://oauth2.googleapis.com/token", data={
        "code": codigo, "client_id": GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": GOOGLE_OAUTH_CLIENT_SECRET, "redirect_uri": _url_retorno("google"),
        "grant_type": "authorization_code",
    }, timeout=15)
    if r.status_code != 200:
        return ""
    return str((r.json() or {}).get("id_token") or "")


@app.route("/auth/google/retorno", endpoint="auth_google_retorno")
def auth_google_retorno():
    estado = _ler_estado(request.args.get("state"), "google")
    if not estado:
        return make_response(_pagina_entrada(
            "A entrada expirou ou veio de outro navegador. Tente de novo.", "erro")), 400
    if request.args.get("error") or not request.args.get("code"):
        return _concluir_navegador(estado, "erro", mensagem="Entrada com Google cancelada.")
    try:
        id_token = _trocar_codigo_google(request.args.get("code"))
    except Exception as exc:          # noqa: BLE001
        print(f"[entrada] troca de código Google falhou: {type(exc).__name__}", flush=True)
        id_token = ""
    claims, erro = _verificar_token_provedor("google", id_token, nonce=estado["n"])
    if erro:
        auth_log("ENTRADA_GOOGLE_TOKEN_RECUSADO", "", erro)
        return _concluir_navegador(estado, "erro", mensagem="Não foi possível confirmar a entrada com Google.")
    sub = str(claims["sub"]).strip()
    situacao, username, _ = _resolver_identidade(
        "google", sub, email=str(claims.get("email") or ""), nome=str(claims.get("name") or "")[:80],
        superficie=estado["o"])
    return _concluir_navegador(estado, situacao, username, "google", sub)


# ── excluir a própria conta (a Apple exige, 5.1.1(v); e é direito da pessoa) ──
@app.route("/api/conta/excluir", methods=["POST"])
def api_conta_excluir():
    username = session.get("username", "")
    # 14/09/2026: só JSON de verdade (CSRF). get_json(force=True) aceitava um formulário
    # text/plain forjado por outro site com corpo {"confirmar":"EXCLUIR","x":"="}.
    if not request.is_json:
        return jsonify({"error": "Envie application/json."}), 415
    dados = _corpo_json() or {}
    if dados.get("confirmar") != "EXCLUIR":
        return jsonify({"error": "Confirmação ausente."}), 400
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()      # ilegível → 503, nada apagado
        conta = usuarios.get(username)
        if not conta:
            return jsonify({"error": "Conta não encontrada."}), 404
        if conta.get("admin"):
            return jsonify({"error": "Conta de operador não se exclui por aqui; use o painel no computador."}), 403
        identidades = identidade.identidades_publicas(conta)
        try:
            PEDIDOS.retirar_nome(username)     # lápide antes de apagar (BAIXO 3)
        except (OSError, ValueError) as exc:
            print(f"[conta] lápide de {username} não gravada ({exc}); exclusão recusada", flush=True)
            return jsonify({"error": "A exclusão está indisponível agora. Nada foi apagado; tente de novo."}), 503
        CHAT_JOBS().purge(username)
        PURGE_PUSH(username)
        del usuarios[username]
        save_users(usuarios)
    PEDIDOS.encerrar_do_usuario(username, identidades)
    auth_log("CONTA_EXCLUIDA_PELO_TITULAR", username)
    session.clear()
    return jsonify({"status": "deleted"}), 200


# ══════════════════════════════════════════════════════════════
# MOTOR POR CONTA — IALD Nativa para o operador, OpenAI para os demais (14/09/2026)
#
# Ordem do operador: "eu quero o modelo mais barato, a função não é competir, é apenas
# poder servir sem ser o meu servidor. e eu posso ter o modelo melhor só pra mim, mas pra
# todos os demais que eu liberar acesso no app da IALD usariam o modelo mais barato que a
# openai servir". A regra inteira, com as travas, está em iald_motores.py.
#
# ⚠ O que ISTO NÃO faz: tirar o servidor web do PC do operador. A inferência dos demais
# sai da máquina; a entrada, o painel e o túnel continuam aqui até o servidor mudar para
# uma hospedagem própria.
# ══════════════════════════════════════════════════════════════
import iald_motores  # noqa: E402
os.environ.setdefault("TIKTOKEN_CACHE_DIR", os.path.join(SERVE_DIR, ".iald_runtime", "tokenizer_cache"))
import iald_kernel  # noqa: E402
import iald_fontes_publicas  # noqa: E402
import iald_memoria_canonica  # noqa: E402
import iald_core_indexado  # noqa: E402
import iald_orcamento  # noqa: E402


MOTORES_CFG = iald_motores.carregar_config(lambda nome: _segredo(nome, ""))
for _aviso_motor in MOTORES_CFG.avisos:
    print(f"[motores] AVISO: {_aviso_motor}", flush=True)
PROMPT_EXTERNO, PROMPT_EXTERNO_SHA = iald_motores.ler_prompt_canonico(
    os.path.join(SERVE_DIR, "app", "kernel_prompt_loja.js"))
RAZAO_OPENAI = iald_motores.RazaoDeUso(os.path.join(SERVE_DIR, "iald_uso_openai.json"))
LIMITE_OPENAI = iald_motores.JanelaDePedidos(MOTORES_CFG.pedidos_por_minuto, 60.0)

# ── O MOTOR CLAUDE (21/09/2026) — a regra em iald_motores (bloco "O TERCEIRO MOTOR"); o envio em
# iald_motor_claude. Decisões do operador (verbatim, 21/09/2026): *"Achei o Sonnet muito caro, mas é o
# melhor [...] eu vou instalar somente pra mim, para eu testar"*; o que vai: *"O mesmo pacote do
# ChatGPT"*; quem usa: *"por enquanto só eu"* (IALD_CLAUDE_CONTAS).
# Tudo do claude é SEPARADO do da OpenAI: configuração (nomes IALD_CLAUDE_*), razão de uso
# (iald_uso_claude.json — o saldo da OpenAI, iald_saldo_openai, lê só o razão da OpenAI), reservas
# (outro banco SQLite: uma cobrança acima da reserva no claude nunca pausa o ChatGPT), pedidos por
# minuto e consentimento. Iguais: o prefixo TGL (_contexto_externo), as ferramentas pagas, a
# moderação (na chave da OpenAI), a medição TGLC e o rótulo da resposta.
import iald_motor_claude  # noqa: E402
CLAUDE_CFG = iald_motores.carregar_config_claude(lambda nome: _segredo(nome, ""), MOTORES_CFG)
for _aviso_claude in CLAUDE_CFG.avisos:
    print(f"[claude] AVISO: {_aviso_claude}", flush=True)
RAZAO_CLAUDE = iald_motores.RazaoDeUso(os.path.join(SERVE_DIR, "iald_uso_claude.json"))
LIMITE_CLAUDE = iald_motores.JanelaDePedidos(CLAUDE_CFG.pedidos_por_minuto, 60.0)
GUARDA_CLAUDE = None
_TRAVA_GUARDA_CLAUDE = threading.Lock()
_SDK_CLAUDE_VISTO = []                  # o pacote `anthropic` achado uma vez não some sem reiniciar


def _sdk_claude_presente():
    """O pacote `anthropic` está instalado neste Python? (sem importá-lo). Os testes trocam esta função."""
    if _SDK_CLAUDE_VISTO:
        return True
    try:
        import importlib.util
        presente = importlib.util.find_spec("anthropic") is not None
    except (ImportError, ValueError):
        presente = False
    if presente:
        _SDK_CLAUDE_VISTO.append(True)
    return presente


def _contas_claude():
    """A lista de contas do claude, só quando o motor claude está configurado (chave e preço).
    Sem isso, frozenset(): um `motor: "claude"` gravado volta à regra de sempre."""
    return CLAUDE_CFG.contas if iald_motores.claude_configurado(CLAUDE_CFG) else frozenset()



import iald_app_providers as app_providers
import iald_auto_router as app_router
import iald_auto_recovery as app_recovery
import new_private_media_host as private_media_host
from private_media_store import MediaError, MediaUnavailable, contains_refs, MAX_RAW_BYTES
from iald_media_budget import BudgetRefusal as MediaBudgetError
import iald_task_policy as task_policy
import iald_task_session as task_session
import iald_task_artifacts as task_artifacts
import iald_artifact_view as artifact_view
import iald_task_bridge as task_bridge
from iald_science_snapshot import ScienceSnapshot, SCIENCE_TOOLS
import iald_science_update_hook as science_update_hook
from types import SimpleNamespace
import iald_operator_bench as operator_bench
import iald_app_spend as app_spend
import iald_wallet_runtime as wallet_runtime
APP_EVALUATION = app_providers.Evaluation(SERVE_DIR)

from claude_route_bridge import RouteBridge
from claude_memory_package import load_package
import iald_native_memory as native_memory
from claude_guarded_transport import post_guarded
from claude_profiles import HAIKU as _HAIKU_PROFILE, LEGACY_HAIKU as _LEGACY_HAIKU_PROFILE, reasoning_parameters as _haiku_reasoning
from claude_haiku_messages import assemble as _assemble_haiku_messages
from claude_native_counter import count_native_request as _count_haiku_native_request
from claude_native_account import NativeAccount as _HaikuNativeAccount, DeferredStartAccount as _DeferredHaikuAccount
from claude_context_snapshot import (load_snapshot as _load_haiku_snapshot,
    MeasuredSnapshot as _HaikuSnapshot, context_metadata as _haiku_metadata,
    CheckedAdapter as _CheckedHaikuAdapter, attach_openai_tools as _haiku_attach_tools,
    verify_native_tools as _verify_haiku_tools)

def _haiku_tool_definitions():
    return (iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions()
            + iald_core_indexado.tool_definitions() + app_memory.tool_definitions())

def _haiku_client_ready():
    # Compatibility marker only: it never grants account/model authorization.
    return request.headers.get("X-IALD-Context") == "anthropic-native-v1"

def _haiku_snapshot(package):
    # All package fields were cross-checked against the manifest by the loader.
    return _HaikuSnapshot(_HAIKU_PROFILE.model, package.measurement.prefix_sha256,
        package.measurement.permanent_tokens,
        _HAIKU_PROFILE.window - package.available_dynamic_tokens - package.reserved_output_tokens - 1024,
        package.reserved_output_tokens, 1024, package.available_dynamic_tokens,
        package.tools_sha256, "")

def _haiku_selected(record, username):
    record = record or {}
    if record.get("motor") != iald_motores.CLAUDE:
        return False
    model = record.get("modelo_claude")
    return model in (_HAIKU_PROFILE.model, _LEGACY_HAIKU_PROFILE.model, "claude-haiku-4-5") or (not model and str(username).strip().lower() != "luiz")

def _capture_science():
    return ScienceSnapshot.capture(os.path.join(SERVE_DIR, 'iald_nucleo_fixo.json'))


def _science_tool(snapshot, fallback, name, args, **kwargs):
    snapshot.check()
    if name.startswith('iald_atlas_') or name in ('iald_public_read','iald_public_search'):
        return json.dumps({'status':'UNAVAILABLE_USE_VERSIONED_SEARCH_TGL', 'identity':dict(snapshot.identity), 'notice':'Use search_tgl/fetch_tgl para fontes públicas da versão fixada.'}, ensure_ascii=False)
    if name in SCIENCE_TOOLS:
        return json.dumps(snapshot.execute_tool(name, args), ensure_ascii=False)
    result = fallback(name, args, **kwargs)
    if name in ('fetch_url','search_web'):
        return json.dumps({'scope':'EXTERNAL_SOURCE_NOT_PINNED_SCIENTIFIC_RELEASE', 'notice':'Pesquisa externa; não integra nem atualiza o acervo científico fixado nesta chamada.', 'result':result}, ensure_ascii=False)
    return result


def _load_shared_science_package(science_snapshot=None):
    snapshot = science_snapshot or _capture_science()
    snapshot.check()
    return SimpleNamespace(prefix=snapshot.prefix, identity=dict(snapshot.identity))


def _load_haiku_package(science_snapshot=None):
    from copy import copy
    science_snapshot = science_snapshot or _capture_science()
    if KERNEL_EXTERNO is None:
        raise ValueError('Canonical catalog unavailable for measured memory')
    package, snapshot = _load_haiku_snapshot(
        science_snapshot.package_path("haiku55"),
        lambda directory: load_package(directory,
            canonical_manifest=os.path.join(SERVE_DIR, 'iald_nucleo_fixo.json'),
            source_sha=(science_snapshot.catalog.source_sha if science_snapshot else KERNEL_EXTERNO.source_sha),
            science_snapshot=science_snapshot))
    cfg = copy(CLAUDE_CFG)
    cfg.modelo = cfg.modelo_operador = _HAIKU_PROFILE.model
    cfg.max_saida = _HAIKU_PROFILE.default_output
    payload = _haiku_attach_tools({"model": cfg.modelo, "max_completion_tokens": cfg.max_saida,
        "messages": [{"role": "system", "content": package.prefix}, {"role": "user", "content": "."}],
        "tool_choice": "none"}, _haiku_tool_definitions())
    wire = iald_motor_claude.converter_pedido(cfg, payload, prefixo=package.prefix)
    _verify_haiku_tools(wire, snapshot, trusted_tools=wire["tools"])
    return package

CLAUDE_ROUTES = RouteBridge(motors=iald_motores, base_config=CLAUDE_CFG,
    package_loader=_load_haiku_package, enabled=str(_segredo("IALD_HAIKU_ATIVO", "0")) == "1",
    public_daily_usd=_segredo("IALD_HAIKU_PUBLICO_USD_DIA", ""),
    public_group_daily_usd=_segredo("IALD_HAIKU_GRUPO_USD_DIA", ""))

def _claude_policy(registro, username):
    from claude_server_selection import policy_for
    return policy_for(registro, username, **CLAUDE_ROUTES.policy_flags(username))

def _motor_selection_id(motor, registro, username):
    if motor != iald_motores.CLAUDE:
        return motor
    try:
        return CLAUDE_ROUTES.selection_id(registro, username)
    except (ValueError, PermissionError, OSError, KeyError):
        return "claude-haiku" if _haiku_selected(registro, username) else "claude-sonnet"


def _cfg_do_motor(motor, registro=None, username=None):
    if motor in app_providers.MODELS:
        return app_providers.configuration(MOTORES_CFG, motor)
    if motor == iald_motores.CLAUDE:
        return CLAUDE_ROUTES.configuration(registro, username or session.get("username", ""))
    return MOTORES_CFG


def _razao_do_motor(motor):
    return RAZAO_CLAUDE if motor == iald_motores.CLAUDE else RAZAO_OPENAI


print(f"[claude] modelo={CLAUDE_CFG.modelo} chave={'definida' if CLAUDE_CFG.chave else 'ausente'} "
      f"contas={len(CLAUDE_CFG.contas)} ttl={CLAUDE_CFG.cache_ttl} "
      f"teto_global_usd={CLAUDE_CFG.cota_global_usd}", flush=True)

# ── SALDO DE CRÉDITO DA OPENAI (15/09/2026) — a regra inteira está em iald_saldo_openai.py ──
# Ordem do operador: o contador sempre presente na aba AGI e a IALD avisando quando o crédito
# ficar crítico. A OpenAI não tem API de saldo [REAL, 15/09]: saldo = âncora + compras − gasto.
import iald_saldo_openai  # noqa: E402


def _env_numero(nome, padrao):
    bruto = (_segredo(nome, "") or "").strip()
    try:
        valor = float(bruto.replace(",", ".")) if bruto else float(padrao)
    except ValueError:
        print(f"[saldo] AVISO: {nome} inválido ({bruto!r}); usando {padrao}", flush=True)
        valor = float(padrao)
    return valor if valor >= 0 else float(padrao)


SALDO_OPENAI = iald_saldo_openai.SaldoOpenAI(
    os.path.join(SERVE_DIR, "iald_saldo_openai.json"), RAZAO_OPENAI,
    chave_admin=lambda: _segredo("IALD_OPENAI_ADMIN_KEY", ""),     # relida a cada atualização
    obter=lambda *a, **k: req_lib.get(*a, **k),
    critico_usd=_env_numero("IALD_OPENAI_SALDO_CRITICO_USD", 5.0),
    atencao_usd=_env_numero("IALD_OPENAI_SALDO_ATENCAO_USD", 15.0),
    critico_dias=_env_numero("IALD_OPENAI_SALDO_CRITICO_DIAS", 3.0),
    atencao_dias=_env_numero("IALD_OPENAI_SALDO_ATENCAO_DIAS", 7.0))
# 22/09/2026: o mesmo contador para o crédito da Anthropic (Claude). Ordem do operador (verbatim):
# "agora eu também preciso do controle de gastos do claude também mostrando na central da IALD
# igual ao chatgpt para eu saber o que tenho de crédito em cada operadora". Gasto = só o registro
# da IALD (iald_uso_claude.json): a Anthropic não dá saldo nem custo por API a esta conta.
SALDO_CLAUDE = iald_saldo_openai.SaldoOpenAI(
    os.path.join(SERVE_DIR, "iald_saldo_claude.json"), RAZAO_CLAUDE, provedor="anthropic",
    # 22/09/2026: gasto pela Cost API da Anthropic quando houver chave de administrador (conta de
    # organização); relida a cada atualização — a chave criada depois vale sem reiniciar
    chave_admin=lambda: _segredo("IALD_CLAUDE_ADMIN_KEY", ""),
    obter=lambda *a, **k: req_lib.get(*a, **k),
    critico_usd=_env_numero("IALD_CLAUDE_SALDO_CRITICO_USD", 5.0),
    atencao_usd=_env_numero("IALD_CLAUDE_SALDO_ATENCAO_USD", 15.0),
    critico_dias=_env_numero("IALD_CLAUDE_SALDO_CRITICO_DIAS", 3.0),
    atencao_dias=_env_numero("IALD_CLAUDE_SALDO_ATENCAO_DIAS", 7.0))
_ALERTA_SALDO_ULTIMO = {}          # conta → momento (monotônico) do último aviso na conversa
ALERTA_SALDO_INTERVALO_S = 6 * 3600


def _marcar_sem_credito(exc):
    """O provedor recusou por falta de crédito: a bandeira vira 'esgotado' na hora."""
    try:
        if SALDO_OPENAI.marcar_esgotado(getattr(exc, "codigo", "")):
            print(f"[saldo] a OpenAI recusou por falta de crédito ({exc.codigo}); bandeira: esgotado", flush=True)
    except Exception as erro:          # noqa: BLE001 — marcar nunca derruba a resposta
        print(f"[saldo] falha ao marcar crédito esgotado: {erro}", flush=True)


def _marcar_sem_credito_claude(exc):
    """22/09/2026: a Anthropic recusou por falta de crédito — a bandeira do Claude vira 'esgotado'."""
    try:
        if SALDO_CLAUDE.marcar_esgotado(getattr(exc, "codigo", "")):
            print(f"[saldo] a Anthropic recusou por falta de crédito ({exc.codigo}); bandeira: esgotado", flush=True)
    except Exception as erro:          # noqa: BLE001 — marcar nunca derruba a resposta
        print(f"[saldo] falha ao marcar crédito esgotado (Claude): {erro}", flush=True)


def _alerta_saldo_operador(registro, mensagens, usuario, saldos=None):
    """Operational credit alerts belong only to the protected admin panel."""
    return None
MEMORIA_EXTERNA = None
KERNEL_EXTERNO = None
ERRO_MEMORIA_EXTERNA = ""
GUARDA_OPENAI = None
_TRAVA_GUARDA_OPENAI = threading.Lock()
if MOTORES_CFG.memoria_modo != "prompt":
    try:
        MEMORIA_EXTERNA = iald_memoria_canonica.CanonicalMemory(
            MOTORES_CFG.atlas_path, MOTORES_CFG.memoria_modo)
        _startup_science = _capture_science()
        KERNEL_EXTERNO = _startup_science.catalog
        _catalog_status = KERNEL_EXTERNO.status()
        print(f"[IALD-CANONICAL-CATALOG] release={_startup_science.identity['release']} "
              f"source_sha256={KERNEL_EXTERNO.source_sha[:16]} lean_files={_catalog_status['lean_files']}", flush=True)
    except (ValueError, OSError) as exc:
        ERRO_MEMORIA_EXTERNA = str(exc)
        print("[motores] memória/kernel indisponíveis: " + str(exc), flush=True)


def _guarda_openai():
    global GUARDA_OPENAI
    with _TRAVA_GUARDA_OPENAI:
        if GUARDA_OPENAI is None:
            GUARDA_OPENAI = iald_orcamento.SpendingGuard(
                RAZAO_OPENAI.caminho + ".reservas.sqlite3", RAZAO_OPENAI.caminho)
        return GUARDA_OPENAI


def _guarda_claude(criar=True):
    """O SpendingGuard do claude — banco PRÓPRIO (21/09/2026): as pausas por cobrança acima da
    reserva do claude não alcançam o ChatGPT. criar=False: só o que já existe (o painel e a leitura
    da cota não criam o banco); None se ainda não há banco."""
    global GUARDA_CLAUDE
    with _TRAVA_GUARDA_CLAUDE:
        if GUARDA_CLAUDE is None:
            caminho = RAZAO_CLAUDE.caminho + ".reservas.sqlite3"
            if not criar and not os.path.exists(caminho):
                return None
            GUARDA_CLAUDE = iald_orcamento.SpendingGuard(caminho, RAZAO_CLAUDE.caminho)
        return GUARDA_CLAUDE


def _guarda_do_motor(motor, criar=True):
    original = _guarda_claude(criar) if motor == iald_motores.CLAUDE else _guarda_openai()
    return wallet_runtime.wrap_guard(original, motor)


def _contexto_externo(public=False):
    snapshot = _capture_science()
    return snapshot.prefix, {'scope':'PUBLIC_VERSIONED_RETRIEVAL',
        'context_sha256':hashlib.sha256(snapshot.prefix.encode()).hexdigest(),
        'identity':dict(snapshot.identity), 'private_atlas_included':False}

print(f"[motores] padrão={MOTORES_CFG.motor_padrao} operador={MOTORES_CFG.motor_operador} "
      f"modelo={MOTORES_CFG.modelo} chave={'definida' if MOTORES_CFG.chave else 'ausente'} "
      f"prompt={PROMPT_EXTERNO_SHA[:12] or 'ILEGÍVEL'}", flush=True)
# 14/09/2026 (noite — revisão ordem-régua, médio 7): a troca automática de modelo deixa de ser
# silenciosa — na partida, as trocas dos próximos 30 dias (e as já feitas) saem no log.
for _troca in iald_motores.trocas_previstas(MOTORES_CFG):
    print(f"[motores] AVISO: {_troca['texto']}", flush=True)

# a mesma instrução que o api_post injeta no caminho nativo (bloco SACRED LANGUAGE)
INSTRUCAO_LINGUAGEM_TECNICA = (
    "INSTRUCAO DE LINGUAGEM: Para este usuario, evite linguagem "
    "teologica (Verbo, Nome, Palavra, TETELESTAI, Haja Luz, trinidade "
    "ontologica, etc). Use linguagem tecnica e cientifica equivalente. "
    "Somente use linguagem teologica se o usuario expressamente pedir."
)

# ── PLANOS, MODERAÇÃO E VAGAS DO USO GRATUITO (14/09/2026, noite) ──
# A regra dos planos e da cota em tokens mora em iald_motores.py; aqui ficam só as peças
# que dependem do servidor.
#
# MODERAÇÃO: a última mensagem da pessoa passa pelo /moderations da OpenAI (gratuito)
# ANTES do modelo. Poucas categorias graves bloqueiam (a IALD não responde); as de
# autolesão acolhem (a resposta segue com a instrução do CVV 188 na frente). Registra-se
# só o nome das categorias — nunca o texto. IALD_MODERACAO=0 desliga; se a moderação
# falhar, IALD_MODERACAO_FALHA decide: "seguir" (padrão, com aviso no log) ou "bloquear".
MODERACAO_LIGADA = _segredo("IALD_MODERACAO", "1").strip() != "0"
_falha_moderacao = _segredo("IALD_MODERACAO_FALHA", "seguir").strip().lower()
if _falha_moderacao not in ("seguir", "bloquear"):
    print(f"[motores] AVISO: IALD_MODERACAO_FALHA inválido ({_falha_moderacao!r}); usando seguir", flush=True)
    _falha_moderacao = "seguir"
MODERACAO_FALHA = _falha_moderacao
MSG_MODERACAO_INDISPONIVEL = ("A verificação de segurança das mensagens está indisponível agora. "
                              "Tente de novo em instantes.")

# VAGAS: cada stream do motor externo prende uma thread do waitress enquanto a resposta
# chega. Sem teto, muitas contas gratuitas ao mesmo tempo travariam o painel e o chat do
# operador. Sem vaga → aviso "ocupado", nada é chamado.
GRATUITO_STREAMS_SIMULTANEOS = _inteiro_de_config("IALD_GRATUITO_STREAMS_SIMULTANEOS", 4, 1)
_SEMAFORO_GRATUITO = threading.BoundedSemaphore(GRATUITO_STREAMS_SIMULTANEOS)
MSG_OCUPADO = ("A IALD está atendendo muitas pessoas no uso gratuito agora. "
               "Tente de novo em instantes.")
# Voltas do agente no plano gratuito, se o operador ligar IALD_PLANO_GRATUITO_AGENTE=1:
# cada volta é uma chamada paga com a janela inteira de entrada.
# ⚠ CORREÇÃO AO LADO (14/09/2026, noite — revisão de testes A2): o teto só valia no modo
# IALD_MEMORIA_MODO=prompt; com nucleo_kernel (o do deploy) a conta gratuita ganhava agente com
# as consultas canônicas e 6 voltas (reproduzido: 6 chamadas numa mensagem). Agora vale em
# QUALQUER modo, e o resultado de consulta canônica do gratuito é cortado em
# GRATUITO_MAX_CHARS_FERRAMENTA caracteres (antes: até 20.000 por leitura, sem corte).
GRATUITO_MAX_VOLTAS_AGENTE = 2
GRATUITO_MAX_CHARS_FERRAMENTA = 8000

# ── UMA RESPOSTA EM ANDAMENTO POR CHAVE DE COTA DO GRATUITO (14/09/2026, noite — revisão A1) ──
# Reproduzido: quatro pedidos abertos juntos passavam todos pela checagem da cota antes de
# qualquer registro (uso 70.474 de 8.000). A segunda resposta da mesma cota recebe o aviso
# "em_andamento" e nada é chamado.
MSG_EM_ANDAMENTO = "Espere a resposta anterior terminar."
_EM_ANDAMENTO_GRATUITO = set()
_TRAVA_EM_ANDAMENTO = threading.Lock()
MSG_TEXTO_LONGO = ("A conversa enviada passa do tamanho aceito no uso gratuito. Comece uma conversa "
                   "nova ou envie um texto menor.")
MSG_RESERVA_INDISPONIVEL = "O controle de reservas de uso está indisponível agora; nada foi enviado."
# Moderação da RESPOSTA do gratuito (14/09/2026, noite — MÉDIO 1): feita no fim do stream, sobre o
# texto inteiro já transmitido. A resposta já chegou à tela; o aviso sai antes do [DONE] com
# `retirar_resposta: true`. O app de hoje mostra o aviso e não guarda a resposta no histórico,
# mas ainda deixa o texto visível — esconder o texto é trabalho do app [OPEN].
MSG_MODERACAO_RESPOSTA = ("Esta resposta foi marcada pela verificação de segurança da IALD e não fica "
                          "no histórico da conversa.")
_CACHE_MODERACAO = iald_motores.CacheModeracao(4096)


class _MarcaAndamento:
    """A resposta em andamento de uma chave de cota. Solta UMA vez só (como _Vaga)."""

    def __init__(self, chave):
        self._chave = chave
        self._solta = False
        self._trava = threading.Lock()

    @classmethod
    def tomar(cls, chave):
        """A marca, ou None se já há resposta em andamento para esta chave."""
        with _TRAVA_EM_ANDAMENTO:
            if chave in _EM_ANDAMENTO_GRATUITO:
                return None
            _EM_ANDAMENTO_GRATUITO.add(chave)
        return cls(chave)

    def soltar(self):
        with self._trava:
            if self._solta:
                return
            self._solta = True
        with _TRAVA_EM_ANDAMENTO:
            _EM_ANDAMENTO_GRATUITO.discard(self._chave)


class _Vaga:
    """Uma vaga do semáforo, solta UMA vez só — pelo fim do gerador ou pelo close() do WSGI,
    o que vier primeiro (o gerador que nunca começou não roda o próprio finally)."""

    def __init__(self, semaforo):
        self._semaforo = semaforo
        self._solta = False
        self._trava = threading.Lock()

    def soltar(self):
        with self._trava:
            if self._solta:
                return
            self._solta = True
        self._semaforo.release()


def _chave_cota_de(registro, username):
    """A chave da cota: a gravada na conta (identidade, sobrevive a exclusão) ou o nome."""
    return str((registro or {}).get("cota_chave") or "").strip() or str(username or "")


def _bloqueio_da_cota(estado):
    """Qual limite da PRÓPRIA conta já se esgotou, lido do estado da cota ("" = nenhum).
    Os tetos globais não entram aqui: eles só aparecem quando um pedido é recusado."""
    try:
        for campo in ("usd_dia", "tokens_dia", "tokens_mes"):
            bloco = estado.get(campo) or {}
            if bloco.get("limite") is None:
                continue
            if float(bloco.get("usado", 0)) >= float(bloco.get("limite", 0)):
                return campo
    except (AttributeError, TypeError, ValueError):
        return ""
    return ""


def _estado_da_cota_da_conta(username, registro, motor=iald_motores.OPENAI):
    """21/09/2026 (aditivo): `motor` — a cota do provedor do motor (o claude tem razão e reservas
    próprios). Sem o argumento, a da OpenAI, como antes."""
    plano = iald_motores.plano_de(registro)
    try:
        cfg = iald_motores.config_da_conta(_cfg_do_motor(motor, registro, username), registro)
    except (PermissionError, ValueError, OSError, KeyError):
        return {"erro": "Configuração do modelo indisponível."}
    estado = iald_motores.estado_da_cota(cfg, _razao_do_motor(motor), username, plano,
                                         _chave_cota_de(registro, username))
    if "erro" not in estado and cfg.somente_limite_global:
        try:
            guarda = _guarda_do_motor(motor, criar=False)
            total = max(estado["global_usd_dia"]["usado"], guarda.used_today() if guarda else 0.0)
            estado["global_usd_dia"]["usado"] = round(total, 8)
        except Exception:
            estado["erro"] = "O controle de uso global está indisponível agora."
    if "erro" not in estado:
        estado["bloqueado_por"] = _bloqueio_da_cota(estado)
    return estado


def _motor_do_usuario(username):
    """(motor, registro da conta). Conta inexistente cai no motor padrão, sem registro.

    REVISÃO DE SEGURANÇA (14/09/2026, noite): leitura ESTRITA. Antes, um PermissionError do
    Windows nesta leitura (medido: ~5% das leituras com um gravador concorrente, e a própria
    conta gratuita gera o gravador com o consentimento) devolvia {} → plano "assinante" →
    motor padrão = nativa → a conta gratuita descia ao llama local com a memória do operador
    (reproduzido). Agora a falha levanta UsuariosIlegiveis; quem decide o caminho nativo
    (api_post, api_get) ainda exige registro não vazio e plano diferente de gratuito.
    """
    registro = load_users_estrito().get(username or "", {}) if username else {}
    return _motor_efetivo(registro, username), registro


def _motor_efetivo(registro, username):
    if app_router.default_for(registro,username):return app_router.AUTO
    if isinstance(registro, dict) and registro.get("motor") == app_router.AUTO:
        return app_router.AUTO
    if isinstance(registro, dict) and registro.get("motor") in app_providers.MODELS:
        return registro["motor"]
    # A saved Claude selection remains Claude even if temporarily unavailable;
    # the send boundary refuses it instead of silently switching providers.
    if isinstance(registro, dict) and registro and registro.get("motor") == iald_motores.CLAUDE:
        return iald_motores.CLAUDE
    return iald_motores.escolher_motor(registro, MOTORES_CFG, usuario=username, contas_claude=_contas_claude())


MSG_MOTOR_SEM_REGISTRO = ("Não foi possível confirmar o motor desta conta agora. Nada foi enviado; "
                          "tente de novo em alguns instantes.")


def _caminho_nativo_permitido(registro):
    """O llama local (e a memória do operador) só para conta com registro e plano != gratuito."""
    # 15/09/2026: e só para conta AMPLIADA (admin ou acesso_nativa); a conta padrão é sempre ChatGPT
    return (isinstance(registro, dict) and bool(registro)
            and iald_motores.plano_de(registro) != iald_motores.GRATUITO
            and iald_motores.pode_usar_nativa(registro))


def _motor_externo_indisponivel(modelo, cfg=None):
    """"" = pronto; senão o motivo. 21/09/2026 (aditivo): `cfg` = a configuração do provedor
    (CLAUDE_CFG no claude); sem ela, a da OpenAI, como antes. O prefixo é sempre o da casa."""
    cfg = MOTORES_CFG if cfg is None else cfg
    claude = getattr(cfg, "provedor", iald_motores.OPENAI) == iald_motores.CLAUDE
    if not cfg.chave:
        if claude:
            return "O motor Claude ainda não foi configurado no servidor da IALD (falta a chave da Anthropic)."
        return "O motor externo desta conta ainda não foi configurado no servidor da IALD."
    if claude and not _sdk_claude_presente():
        return "O pacote anthropic não está instalado no servidor da IALD; o motor Claude fica parado."
    if claude and _memoria_modo_integral(MOTORES_CFG):
        # 21/09/2026 (revisão de segurança): a opção e /api/motor/escolha também mostram o Claude parado
        return MSG_CLAUDE_ATLAS_INTEGRAL
    if claude and modelo == _HAIKU_PROFILE.model:
        try:
            CLAUDE_ROUTES.package()
        except (ValueError, OSError, KeyError):
            return "A memória medida do Haiku está indisponível."
        return "" if cfg.precos(modelo) is not None else "Preço do Haiku não configurado."
    if MOTORES_CFG.memoria_modo != "prompt":
        try:
            _contexto_externo()
        except (ValueError, OSError):
            return "A memória canônica ou o kernel integral não puderam ser validados; o envio externo está bloqueado."
    # 21/09/2026: claude-sonnet-5 = 1M tokens Claude [KNOWN — página do modelo, levantamento de 21/09];
    # a janela da casa é em o200k, então compara-se janela × fator_tokens (1.0 na OpenAI: como antes)
    known_windows = {"gpt-5-nano": 400000, "gpt-4.1-nano": 1047576, "gpt-5.6-luna": 1050000,
                     "claude-sonnet-5": 1000000, "claude-sonnet-5-5": 1000000}
    fator = max(float(getattr(cfg, "fator_tokens", 1.0) or 1.0), 1.0)
    if modelo in known_windows and cfg.janela * fator > known_windows[modelo]:
        return "A janela configurada excede a capacidade documentada do modelo."
    if not PROMPT_EXTERNO:
        return "O prompt canônico da IALD não pôde ser lido; o motor externo fica parado por segurança."
    if cfg.precos(modelo) is None:
        return f"O preço do modelo {modelo} não está configurado; sem preço não há teto de gasto."
    return ""


def _sse_aviso(texto, tipo, extra=None):
    """Resposta de chat que só avisa. HTTP 200 de propósito: o app trata 401/403 como sessão
    vencida e qualquer outro erro como servidor fora — e a pessoa não leria o motivo."""
    aviso = {"tipo": tipo, "texto": texto}
    aviso.update(extra or {})

    def gerar():
        yield "data: " + json.dumps({"iald_aviso": aviso}, ensure_ascii=False) + "\n\n"
        yield "data: " + json.dumps({"choices": [{"delta": {"content": texto}, "finish_reason": None}]},
                                    ensure_ascii=False) + "\n\n"
        yield "data: " + json.dumps({"choices": [{"delta": {}, "finish_reason": "stop"}]}) + "\n\n"
        yield "data: [DONE]\n\n"
    return Response(gerar(), status=200, content_type="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# Folga fixa que payload_tokens soma para a RESERVA de gasto (iald_memoria_canonica): margem, não
# token cobrado. Para o SALDO de tokens da pessoa ela sai; o resto (tokens do JSON das mensagens e
# ferramentas, 16 por mensagem e o teto por imagem) fica. [DERIVED — medido em 14/09/2026, noite,
# no prompt da loja: payload 9.974, prompt do servidor 9.223 pelo contador e 8.735 pela CPT; a
# conta sem a folga (727) fica acima do cobrado com o cache frio (~510), sem os 512 a mais]
FOLGA_FIXA_DO_CONTADOR = 512


def _tokens_do_payload_para_saldo(payload):
    return max(0, iald_memoria_canonica.payload_tokens(payload) - FOLGA_FIXA_DO_CONTADOR)


# ── IMAGEM NO PLANO GRATUITO (14/09/2026, noite — tarefa SV; revisão COTAS, regressão 1) ──
# REPRODUZIDO (scratchpad\revC\sonda_img.py): uma imagem enviada pela conta gratuita recebia aviso
# "limite" tokens_dia com a cota em 0 de 8.000 ("O uso gratuito que resta hoje não cobre esta
# mensagem") — _tokens_do_payload_para_saldo conta a imagem pelo teto de 45.000 tokens (30.000 ×
# 1,5 no gpt-5-nano) antes da checagem de janela, e 45.000 (36.000 no luna) nunca cabe na janela
# de 32.768 do gratuito: imagem era impossível e o motivo dito era falso. Agora (contrato novo):
#   - a última mensagem do usuário com imagem → aviso "recurso_indisponivel" com
#     MSG_IMAGEM_GRATUITO, antes do consentimento, da marca de andamento e de qualquer conta de
#     saldo; nada é chamado;
#   - imagem em mensagem ANTERIOR do histórico (o app guarda a mensagem recusada na conversa) sai
#     do que vai ao modelo, em silêncio, para a conversa não travar [INPUT: a ratificar];
#   - GET /api/motor.limites.imagens: false no gratuito, true nos demais.
MSG_IMAGEM_GRATUITO = "Imagens não estão disponíveis no uso gratuito."
MSG_GRATUITO_ATLAS_INTEGRAL = ("O uso gratuito não está disponível com a configuração atual do servidor. "
                               "Nada foi enviado.")
_TIPOS_DE_IMAGEM = ("image_url", "input_image", "image")


def _tem_imagem(conteudo):
    return isinstance(conteudo, list) and any(
        isinstance(p, dict) and p.get("type") in _TIPOS_DE_IMAGEM for p in conteudo)


def _sem_imagens(mensagem):
    """A mensagem sem as partes de imagem (as outras chaves ficam)."""
    if not isinstance(mensagem, dict) or not _tem_imagem(mensagem.get("content")):
        return mensagem
    partes = [p for p in mensagem["content"] if not (isinstance(p, dict) and p.get("type") in _TIPOS_DE_IMAGEM)]
    return dict(mensagem, content=partes)


def _aviso_limite(texto, bloqueado_por, user, registro, motor=iald_motores.OPENAI):
    """Aviso "limite" do contrato (14/09/2026, noite): SEMPRE com `bloqueado_por` e `cota`.
    21/09/2026: `motor` — a cota do provedor que recusou (claude tem a dele)."""
    return _sse_aviso(texto, "limite", {"bloqueado_por": bloqueado_por or "razao",
                                        "cota": _estado_da_cota_da_conta(user, registro, motor)})


def _linhas_da_recusa(exc, user, registro, motor=iald_motores.OPENAI):
    """As linhas SSE de uma recusa do controle de gasto dentro do stream: janela → pedido
    inválido; o resto → aviso "limite" com bloqueado_por e cota."""
    por = getattr(exc, "bloqueado_por", "") or "razao"
    if por == "janela":
        yield from _sse_aviso(str(exc), "pedido_invalido").response
    else:
        yield from _aviso_limite(str(exc), por, user, registro, motor).response


def _operational_native_payload(payload):
    model_id, base_url = ACTIVE_MODEL_ID, LLAMA_URL
    window = native_memory.configured_window(MODELS[model_id])
    result, native_history_receipt = native_memory.prepare_activity_payload(
        payload, binding=app_memory.current(), project_messages=app_memory.project_messages,
        window=window, path='worker_operational', compress=False)
    native_memory.check_text_window(result, window, base_url=base_url)
    if model_id != ACTIVE_MODEL_ID or base_url != LLAMA_URL:
        raise ValueError('Native model changed during memory projection/counting')
    return result


def _prepare_native_payload(payload, superficie, *, native_path='legacy', science_snapshot=None):
    """Called only after the existing native-account authorization gate."""
    if MEMORIA_EXTERNA is None or MEMORIA_EXTERNA.nucleus_manifest is None:
        raise ValueError('Native canonical manifest unavailable')
    manifest = MEMORIA_EXTERNA.nucleus_manifest
    science_snapshot = science_snapshot or _capture_science()
    prefix = science_snapshot.native_prefix + science_snapshot.pre_retrieve(payload.get("messages") or [], max_bytes=20000)["prompt"]
    identity = science_snapshot.check()
    result = dict(payload)
    result['messages'] = native_memory.attach_context(payload.get('messages'), prefix)
    # Canonical readers are public. Do not add the private Atlas or task/admin tools.
    definitions = list(_ferramentas_para(superficie))
    names = {(t.get('function') or {}).get('name') for t in definitions}
    for tool in iald_kernel.tool_definitions() + iald_core_indexado.tool_definitions():
        name = tool['function']['name']
        if name not in names:
            definitions.append(tool)
            names.add(name)
    model_id = ACTIVE_MODEL_ID
    llama_url = LLAMA_URL
    window = native_memory.configured_window(MODELS[model_id])
    result, native_history_receipt = native_memory.prepare_activity_payload(
        result, binding=app_memory.current(), project_messages=app_memory.project_messages,
        window=window, path=native_path)

    def check(current):
        if model_id != ACTIVE_MODEL_ID or llama_url != LLAMA_URL:
            raise ValueError('Native model changed during request')
        if science_snapshot.check() != identity:
            raise ValueError('Native canonical release changed during request')
        measured = native_memory.check_text_window(current, window, base_url=llama_url)
        if model_id != ACTIVE_MODEL_ID or llama_url != LLAMA_URL:
            raise ValueError('Native model changed during counting')
        science_snapshot.check()
        return measured

    check.science_snapshot = science_snapshot
    check(result)
    return result, definitions, check


def _ferramentas_externas(cfg, limites, superficie, gratuito):
    """As ferramentas que o motor externo oferece a esta conta nesta superfície.

    Web (data/hora, busca, leitura de página): só com o agente do plano. Consultas canônicas
    (IALD_MEMORIA_MODO ≠ prompt): kernel e fontes públicas para todos; o Atlas — repositório
    PRIVADO, com estratégia de patente [LEGAL] — fica fora do plano gratuito, salvo
    IALD_GRATUITO_ATLAS=1 (14/09/2026, noite — revisão de segurança, ALTO 1).
    """
    permitidas = []
    if limites.get("agente"):
        permitidas = [t for t in _ferramentas_para(superficie)
                      if (t.get("function") or {}).get("name") in cfg.ferramentas]
    if cfg.memoria_modo != "prompt":
        permitidas += iald_kernel.tool_definitions()
        if not gratuito or cfg.gratuito_atlas:
            permitidas += iald_memoria_canonica.tool_definitions()
        permitidas += iald_fontes_publicas.tool_definitions()
        permitidas += iald_core_indexado.tool_definitions()
    return permitidas


_ARGUMENTOS_ATLAS = {"iald_atlas_search": {"query", "limit"}, "iald_atlas_read": {"start_line", "max_lines"}}


def _executar_ferramenta_gratuito(tool_name, arguments, user="?", operator_authorized=False):
    """Executor das ferramentas do plano gratuito (14/09/2026, noite).

    Atlas: só com IALD_GRATUITO_ATLAS=1 e, mesmo assim, sem as seções não públicas
    (iald_memoria_canonica.PRIVATE_SECTIONS). O resto vai ao execute_public_tool de sempre,
    nunca com poder de operador."""
    if str(tool_name).startswith("iald_atlas_"):
        if not MOTORES_CFG.gratuito_atlas:
            return json.dumps({"status": "UNAVAILABLE",
                               "error": "A consulta ao Atlas não está disponível no uso gratuito."}, ensure_ascii=False)
        return _atlas_sem_secoes_privadas(tool_name, arguments)
    return execute_public_tool(tool_name, arguments, user=user, operator_authorized=False)


def _atlas_sem_secoes_privadas(tool_name, arguments):
    """iald_atlas_search / iald_atlas_read SEM §V, §VI e §X (iald_memoria_canonica.PRIVATE_SECTIONS);
    argumentos fora da lista fechada → UNAVAILABLE. Se as seções não forem localizadas, a própria
    memória canônica recusa (fail-closed). Movido de _executar_ferramenta_gratuito em 21/09/2026,
    sem mudança de comportamento, para servir também ao claude."""
    try:
        if MEMORIA_EXTERNA is None:
            raise ValueError("Atlas canônico indisponível.")
        permitidos = _ARGUMENTOS_ATLAS.get(tool_name)
        if permitidos is None or not isinstance(arguments, dict) or set(arguments) - permitidos:
            raise ValueError("Consulta canônica inválida.")
        metodo = MEMORIA_EXTERNA.search if tool_name == "iald_atlas_search" else MEMORIA_EXTERNA.read
        resultado = metodo(**arguments, suppress=iald_memoria_canonica.PRIVATE_SECTIONS)
        return json.dumps(resultado, ensure_ascii=False)
    except (ValueError, OSError, TypeError) as exc:
        return json.dumps({"status": "UNAVAILABLE", "error": str(exc)}, ensure_ascii=False)


def _executar_ferramenta_claude(tool_name, arguments, user="?", operator_authorized=False):
    """Executor das ferramentas do motor claude (21/09/2026).

    O conjunto é o PAGO de sempre (o mesmo que a OpenAI oferece a esta conta), mas o Atlas vai SEM
    §V (patentes, [LEGAL]), §VI (caminhos) e §X (estado operacional) — decisão do operador: *"O mesmo
    pacote do ChatGPT"*, com essas seções e os arquivos confidenciais FORA, inclusive pelas
    ferramentas. Nunca com poder de operador.

    ⚠ CORREÇÃO AO LADO (21/09/2026, revisão de segurança): o resto ia inteiro ao execute_public_tool —
    se IALD_OPENAI_FERRAMENTAS ganhasse consultar_acervo (indexa CLAUDE.md e minutas de patente) ou
    consultar_memoria (a memória do operador), o Claude herdaria. Agora a lista é FECHADA:
    _ferramentas_permitidas_claude(); qualquer outro nome é recusado aqui, mesmo que chegue."""
    if tool_name not in _ferramentas_permitidas_claude():
        print(f"[claude] {user}: ferramenta fora da lista fechada do claude recusada: {tool_name!r}", flush=True)
        return json.dumps({"status": "UNAVAILABLE",
                           "error": "Ferramenta não disponível no motor Claude."}, ensure_ascii=False)
    if str(tool_name).startswith("iald_atlas_"):
        return _atlas_sem_secoes_privadas(tool_name, arguments)
    return execute_public_tool(tool_name, arguments, user=user, operator_authorized=False)


def _ferramentas_permitidas_claude():
    """A lista FECHADA do claude (21/09/2026, revisão de segurança): as de web da lista
    iald_motores.FERRAMENTAS_CLAUDE_PERMITIDAS que a configuração do claude mantém, e as canônicas
    (kernel, Atlas — que _atlas_sem_secoes_privadas serve sem §V/§VI/§X —, fontes públicas,
    search_tgl/fetch_tgl). Nada de acervo, memória do operador, prova viva, arquivo ou transferência."""
    nomes = set(CLAUDE_CFG.ferramentas) & set(iald_motores.FERRAMENTAS_CLAUDE_PERMITIDAS)
    for fonte in (iald_kernel.tool_definitions, iald_memoria_canonica.tool_definitions,
                  iald_fontes_publicas.tool_definitions, iald_core_indexado.tool_definitions, app_memory.tool_definitions):
        try:
            nomes.update((t.get("function") or {}).get("name") for t in fonte())
        except Exception as exc:          # noqa: BLE001 — fail-closed: a ferramenta fica fora
            print(f"[claude] definições de ferramentas ilegíveis ({type(exc).__name__}); fora da lista", flush=True)
    nomes.discard(None)
    return frozenset(nomes)


def _moderar_resposta_sse(fluxo, user, cfg, *, authorize=None):
    """Repassa o stream INTACTO e, no [DONE], modera o texto inteiro da resposta (plano gratuito).

    Bloqueio → aviso "moderacao" com retirar_resposta antes do [DONE] (ver
    MSG_MODERACAO_RESPOSTA). Moderação que falha com IALD_MODERACAO_FALHA=bloquear → aviso
    "moderacao_indisponivel" do mesmo jeito. Cliente que fechou antes do fim: nada a moderar.
    """
    partes = []

    def veredito():
        texto = "".join(partes)
        if not texto.strip():
            return
        if authorize is not None:authorize()
        r = iald_motores.moderar_textos([texto], req_lib.post, cfg.url_base, cfg.chave)
        if r.get("bloquear"):
            auth_log("MODERACAO_RESPOSTA_BLOQUEIO", user,
                     f"categorias={','.join(r.get('categorias') or []) or '-'}")
            aviso = {"tipo": "moderacao", "texto": MSG_MODERACAO_RESPOSTA, "retirar_resposta": True}
        elif not r.get("ok"):
            print(f"[moderacao] resposta de {user}: {r.get('erro') or 'falhou'}; "
                  f"{'aviso enviado' if MODERACAO_FALHA == 'bloquear' else 'seguindo sem moderação'}", flush=True)
            if MODERACAO_FALHA != "bloquear":
                return
            aviso = {"tipo": "moderacao_indisponivel", "texto": MSG_MODERACAO_INDISPONIVEL, "retirar_resposta": True}
        else:
            return
        yield "data: " + json.dumps({"iald_aviso": aviso}, ensure_ascii=False) + "\n\n"

    julgado = False
    for pedaco in fluxo:
        texto = pedaco.decode("utf-8", "replace") if isinstance(pedaco, (bytes, bytearray)) else str(pedaco)
        if texto.strip() == "data: [DONE]" and not julgado:
            julgado = True
            yield from veredito()
            yield pedaco
            continue
        try:
            for linha in texto.split("\n"):
                linha = linha.strip()
                if not linha.startswith("data: {"):
                    continue
                d = json.loads(linha[6:])
                for escolha in d.get("choices") or []:
                    partes.append(((escolha or {}).get("delta") or {}).get("content") or "")
        except (ValueError, AttributeError, TypeError):
            pass
        yield pedaco
    if not julgado:
        yield from veredito()


def _chat_openai(req_json, user, registro, is_stream, tokens_in, *, task_scope=None, dispatch_check=None, routing_instruction=None, recovery_attempt=None, science_snapshot=None):
    """Atende um /v1/chat/completions pela OpenAI. None = devolver ao caminho nativo.

    14/09/2026 (noite): o plano da conta manda — cota em tokens por dia e por mês, teto em
    dólar, saída máxima, agente e modo pensar (iald_motores.limites_do_plano). O plano
    gratuito NUNCA devolve None: a reserva nativa não vale para ele, porque a porta aberta
    jamais pode cair na máquina (e na memória) do operador.

    14/09/2026 (noite, tarefa S2 — revisões de testes A1/A2, segurança ALTO 1/MÉDIO 1), no plano
    gratuito: uma resposta em andamento por chave de cota; saldo de tokens conferido antes de
    montar, histórico mais antigo descartado até caber no saldo e conferência de novo antes de
    CADA chamada (SaldoDoPedido); no máximo 2 voltas e resultado canônico cortado em qualquer
    modo de memória; Atlas fora por padrão; conversa acima de TETO_TOTAL_TEXTO_GRATUITO recusada;
    resposta moderada no fim. Para todos: todo o texto do cliente que vai ao modelo é moderado
    (histórico, perfil e última mensagem, em blocos, sem descartar excedente); aviso "limite"
    sempre com bloqueado_por e cota.

    21/09/2026: o corpo virou _chat_externo(…, motor) — o MESMO caminho serve o claude. Este nome
    continua (api_post e os testes o chamam) e responde exatamente como antes.
    """
    return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.OPENAI, task_scope=task_scope, dispatch_check=dispatch_check, routing_instruction=routing_instruction, recovery_attempt=recovery_attempt, science_snapshot=science_snapshot)


def _chat_claude(req_json, user, registro, is_stream, tokens_in, *, task_scope=None, dispatch_check=None, routing_instruction=None, science_snapshot=None):
    """Atende um /v1/chat/completions pelo Claude (Anthropic) — 21/09/2026. NUNCA devolve None: o
    claude jamais cai no caminho nativo (llama local, memória do operador)."""
    return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.CLAUDE, task_scope=task_scope, dispatch_check=dispatch_check, routing_instruction=routing_instruction, science_snapshot=science_snapshot)



def _automatic_budget_available(record,user,provider):
    if wallet_runtime.enabled():
        # Wallet admission already happened. The transport retains global caps.
        return app_router.allowed(record,user)
    """Local exhaustion gate before paid routing; dispatch still reserves usage."""
    try:
        if not app_router.allowed(record,user):return False
        if provider in app_providers.MODELS:
            if not app_providers.allowed(record,user,provider):return False
            # Kimi/DeepSeek and the operator's MiMo retain their authorized policy.
            if provider not in ('mimo','deepseek') or user=='luiz':return True
            daily,group=CLAUDE_ROUTES.public_budget()
            key=hashlib.sha256(user.encode('utf-8')).hexdigest()
            account=app_spend.PublicAccount(SERVE_DIR,key,daily,group,CLAUDE_ROUTES.base.cota_global_usd)
            try:return app_router.budget_remaining(account.guard,key,daily,account.total,
                quota_key=key,group='mimo_public',group_limit=group)
            finally:account.close()
        if provider == 'nativa':return True  # Local dispatch still enforces concurrency.
        if provider not in ('openai','claude-haiku','claude-sonnet'):return False
        current=record
        motor='openai'
        if provider.startswith('claude-'):
            current=dict(record,**CLAUDE_ROUTES.select(provider,record,user));motor=iald_motores.CLAUDE
            cfg=CLAUDE_ROUTES.configuration(current,user)
        else:cfg=iald_motores.config_da_conta(MOTORES_CFG,current)
        plan=iald_motores.plano_de(current);key=_chave_cota_de(current,user)
        # The normal dispatch enforces rate limits once; this probe only reads quotas.
        class BudgetOnly:
            @staticmethod
            def permitir(_user):return True
        permitted,_=iald_motores.verificar_permissao(cfg,_razao_do_motor(motor),BudgetOnly(),
            user,bool(current.get('admin')),plano=plan,chave_cota=key)
        if not permitted:return False
        limits=iald_motores.limites_do_plano(cfg,plan)
        only_global=cfg.somente_limite_global and bool(current.get('admin')) and plan==iald_motores.OPERADOR
        daily=cfg.cota_global_usd if only_global else limits['usd_dia']
        group=plan;group_limit=cfg.cota_global_gratuito_usd if plan==iald_motores.GRATUITO else None
        if hasattr(cfg,'haiku_public_group_limit'):
            group='haiku_public';group_limit=cfg.haiku_public_group_limit
        return app_router.budget_remaining(_guarda_do_motor(motor),user,daily,cfg.cota_global_usd,
            quota_key=key,group=group,group_limit=group_limit)
    except Exception:
        return False


def _new_app_task_scope(user, *, executor=None, science_snapshot=None):
    science_snapshot = science_snapshot or _capture_science()
    # Created only by the authenticated automatic route, not a body flag.
    def authorize(provider='task'):
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Automatic access revoked')
        if provider not in ('task',app_router.AUTO) and not iald_motores.consentiu(current,provider):
            raise PermissionError('Provider consent missing')
        if provider in app_providers.MODELS and not app_providers.allowed(current,user,provider):
            raise PermissionError('Provider unavailable for account')
        return current
    def options():
        current=authorize()
        # Worker threads have no Flask request. Query only delegated provider
        # availability; UI options also inspect client headers and are unsuitable.
        return [row['id'] for row in app_providers.options(current,user)
                if row.get('disponivel') and iald_motores.consentiu(current,row['id'])
                and _automatic_budget_available(current,user,row['id'])]
    def sandbox_config():
        current=authorize('claude')
        current=dict(current,**CLAUDE_ROUTES.select('claude-haiku',current,user))
        cfg=CLAUDE_ROUTES.configuration(current,user)
        cfg.task_quota_key=_chave_cota_de(current,user)
        cfg.task_plan=iald_motores.plano_de(current)
        return cfg
    def spending(provider):
        if wallet_runtime.enabled():
            return wallet_runtime.provider_account(SERVE_DIR,provider,CLAUDE_ROUTES.base.cota_global_usd)
        authorize(provider)
        if provider not in ('mimo','deepseek') or user=='luiz':return None
        daily,group=CLAUDE_ROUTES.public_budget()
        return app_spend.PublicAccount(SERVE_DIR,hashlib.sha256(user.encode('utf-8')).hexdigest(),
            daily,group,CLAUDE_ROUTES.base.cota_global_usd)
    scope = task_bridge.make_scope(root=SERVE_DIR,user=user,authorize=authorize,options=options,
        package=lambda: _load_shared_science_package(science_snapshot),science_snapshot=science_snapshot,evaluation=APP_EVALUATION,providers=app_providers,router=app_router,
        sandbox_config=sandbox_config,client_factory=iald_motor_claude.cliente_para,
        guard_factory=lambda:wallet_runtime.sandbox_guard(_guarda_do_motor(iald_motores.CLAUDE)),ledger=RAZAO_CLAUDE,
        spending_factory=spending)
    scope.executor = executor
    if operator_bench.is_operator(authorize('task'),user):
        operator_bench.attach(scope,root=SERVE_DIR,user=user,authorize=authorize)
    return scope


def _task_scope_names(scope):
    return frozenset(t['function']['name'] for t in scope.tools) if scope is not None else frozenset()


def _execute_scope_tool(scope,name,args,user):
    if name not in _task_scope_names(scope):return {'status':'UNAVAILABLE'}
    if name not in task_session.NAMES:
        # A fresh account read also protects a scope created before revocation.
        if not operator_bench.is_operator(scope.authorize('task'),user):
            return {'status':'FORBIDDEN','notice':'Ferramenta exclusiva do operador.'}
    return scope.execute(name,args)



def _private_media_origin_ok():
    origin = request.headers.get('Origin', '')
    origins = set(ORIGENS_APP) | {URL_PUBLICA.rstrip('/'), request.host_url.rstrip('/')}
    if origin and origin not in origins:return False
    if request.headers.get('Sec-Fetch-Site') == 'cross-site' and origin not in ORIGENS_APP:return False
    if not origin and not getattr(g,'app_bearer',False) and request.method != 'GET':return False
    return True


def _private_runtime_for(req_json,user,*,automatic=False):
    if not private_media_host.has_private_or_typed_media(req_json.get('messages')):return None
    conversation=req_json.get('iald_conv') or getattr(g,'iald_private_conversation',None)
    return PRIVATE_MEDIA_HOST.runtime(user,req_json.get('messages'),conversation,automatic=automatic)


def _private_preview_body(client,user,registro,runtime,science_snapshot=None):
    # Same full public science and complete history as the answering engine.
    science_snapshot = science_snapshot or _capture_science()
    package=_load_shared_science_package(science_snapshot)
    if not package.prefix or _memoria_modo_integral(MOTORES_CFG) or iald_motor_claude.MARCA_ATLAS_INTEGRAL in package.prefix:
        raise MediaError('Unverified public science')
    profile,search_instruction=iald_motores.extrair_do_cliente(client)
    note='Modelo de inferência: '+app_providers.MODELS['mimo']['label']+'. Preserve o regime IALD e os estatutos das fontes. '
    note += 'Use LaTeX com delimitadores \\( \\) ou \\[ \\]. Nunca altere uma fórmula apenas para mudar sua apresentação.'
    note += '\n'+task_policy.INSTRUCTIONS
    if search_instruction:note += '\n'+iald_motores.LUPA_CANONICA
    note += science_snapshot.pre_retrieve(client)['prompt']
    messages=app_providers.wire_messages(client,package.prefix,note+('\nUSER CONTEXT:\n'+profile if profile else ''),
        provider='mimo',images_authorized=True,media_authorized=True,private_media=runtime)
    definitions=iald_kernel.tool_definitions()+iald_core_indexado.tool_definitions()+iald_fontes_publicas.tool_definitions()
    definitions += [t for t in _ferramentas_para('app') if (t.get('function') or {}).get('name') in app_providers.TOOL_NAMES]
    definitions=list({t['function']['name']:t for t in definitions if t['function']['name'] in app_providers.TOOL_NAMES}.values())
    # Pure definition construction; do not create a task/sandbox to estimate it.
    definitions += task_session.definitions(task_artifacts.TOOL_DEFINITION)
    if operator_bench.is_operator(registro,user):definitions += list(operator_bench.TOOLS)
    return dict(model=app_providers.MODELS['mimo']['model'],messages=messages,tools=definitions,
        stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})


@app.route('/api/task-capabilities')
def api_task_capabilities():
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Ferramentas não liberadas para esta conta.'}),403
    capabilities=dict(task_policy.capabilities())
    capabilities.update(PRIVATE_MEDIA_HOST.capabilities(user))
    operator=operator_bench.is_operator(record,user)
    capabilities['classe_usuario']='operador' if operator else 'usuario'
    capabilities['operator_bench']={'available':operator,
        'tools':sorted(operator_bench.NAMES) if operator else []}
    response=jsonify(capabilities)
    response.headers['Cache-Control']='private, no-store'
    return response


@app.route('/api/task-artifacts/<artifact_id>')
def api_task_artifact(artifact_id):
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Acesso negado.'}),403
    try:
        path,meta=task_artifacts.ArtifactStore(SERVE_DIR).resolve(user,artifact_id)
    except (ValueError,PermissionError,OSError,KeyError):return jsonify({'error':'Arquivo indisponível.'}),404
    response=send_file(path,as_attachment=True,download_name=meta['filename'],mimetype='application/octet-stream')
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Content-Security-Policy']="sandbox; default-src 'none'"
    response.headers['Cache-Control']='private, no-store'
    response.headers['Referrer-Policy']='no-referrer'
    return response


@app.route('/api/task-artifacts/<artifact_id>/view')
def api_task_artifact_view(artifact_id):
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Acesso negado.'}),403
    try:
        data=artifact_view.describe(task_artifacts.ArtifactStore(SERVE_DIR),user,artifact_id)
    except (ValueError,PermissionError,OSError,KeyError):return jsonify({'error':'Arquivo indisponível.'}),404
    response=jsonify(data)
    response.headers.update(artifact_view.PRIVATE_HEADERS)
    return response


@app.route('/api/task-artifacts/<artifact_id>/access',methods=['POST'])
def api_task_artifact_access(artifact_id):
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Acesso negado.'}),403
    data,error=_identificacao_json_post(set())
    if error is not None:return error
    try:
        data=artifact_view.access(task_artifacts.ArtifactStore(SERVE_DIR),user,artifact_id)
    except (ValueError,PermissionError,OSError,KeyError):return jsonify({'error':'Arquivo indisponível.'}),404
    response=jsonify(data)
    response.headers.update(artifact_view.PRIVATE_HEADERS)
    return response


@app.route('/task-view/<artifact_id>/<token>')
def task_view(artifact_id,token):
    try:
        page=artifact_view.ticket_page(task_artifacts.ArtifactStore(SERVE_DIR),artifact_id,token)
    except (ValueError,PermissionError,OSError,KeyError):
        response=Response('Link inválido ou expirado. Volte à IALD e toque no arquivo para abrir novamente.',status=404)
    else:
        response=Response(page,mimetype='text/html')
    response.headers.update(artifact_view.PRIVATE_HEADERS)
    response.headers['Content-Security-Policy']=artifact_view.PAGE_CSP
    return response


@app.route('/task-download/<artifact_id>/<token>')
def task_download(artifact_id,token):
    # Narrow, expiring artifact capability for Safari/Android outside the app.
    try:
        path,meta=task_artifacts.ArtifactStore(SERVE_DIR).resolve_ticket(artifact_id,token)
    except (ValueError,PermissionError,OSError,KeyError):
        return Response('Link inválido ou expirado. Peça um novo link na conversa da IALD.',status=404)
    response=send_file(path,as_attachment=True,download_name=meta['filename'],mimetype='application/octet-stream')
    response.headers.update({'X-Content-Type-Options':'nosniff','Content-Security-Policy':"sandbox; default-src 'none'",
        'Cache-Control':'private, no-store','Referrer-Policy':'no-referrer','X-Robots-Tag':'noindex, nofollow'})
    return response


import logging


class _TaskDownloadLogFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        redacted = re.sub(r"(/task-(?:download|view)/[A-Za-z0-9_-]+/)[A-Za-z0-9_-]+",
                          r"\1[REDACTED]", message)
        if redacted != message:
            record.msg, record.args = redacted, ()
        return True


def _install_task_download_log_filter():
    logger = logging.getLogger('werkzeug')
    if not any(isinstance(item, _TaskDownloadLogFilter) for item in logger.filters):
        logger.addFilter(_TaskDownloadLogFilter())


def _chat_automatico(req_json,user,registro,is_stream,tokens_in):
    def notice(text, kind):
        response = _sse_aviso(text, kind)
        response.response = app_recovery.operational_stream(response.response)
        return response
    lease = app_router.acquire(user)
    if lease is None:
        return notice('Uma resposta desta conta já está em andamento.','em_andamento')
    transferred = False
    task_control = None
    def finish_task():
        if task_control is not None: task_control.close(lease.release)
        else: lease.release()
    try:
        if not app_router.available():
            return notice('O modo automático aguarda a validação da conexão JEV.','motor_indisponivel')
        response = _chat_automatico_autorizado(req_json,user,registro,is_stream,tokens_in)
        task_control = getattr(response,'iald_task_control',None)
        if isinstance(response,Response) and response.is_streamed:
            original = app_recovery.operational_stream(response.response)
            def stream_with_lease():
                try:
                    yield from original
                finally:
                    try:
                        close = getattr(original,'close',None)
                        if close: close()
                    finally:
                        finish_task()
            response.response = stream_with_lease()
            response.call_on_close(finish_task)
            transferred = True
        return response
    finally:
        if not transferred: finish_task()


def _mimo_media_limits(registro, user, automatic=False):
    # Capability display never grants permission or transmits attachments.
    eligible = app_providers.allowed(registro, user, 'mimo')
    if automatic:
        eligible = eligible and app_router.allowed(registro,user)
    authorized = eligible and iald_motores.consentiu(registro,'mimo')
    limits = app_router.limits() if automatic else app_providers.limits('mimo',media_authorized=authorized)
    if eligible:
        from iald_mimo_multimodal import media_capabilities
        capabilities = media_capabilities()
        capabilities.update(PRIVATE_MEDIA_HOST.capabilities(user))
        # Local attachment selection is allowed before consent; transmission
        # below still requires the current per-provider versioned acceptance.
        limits.update(imagens=True, audio=capabilities['audio'],
                      video=capabilities['video'], media_capabilities=capabilities)
    else:
        limits.update(imagens=False,audio=False,video=False)
    return limits


def _consentimento_automatico(registro,user):
    """Bootstrap automatic mode without granting consent on the user's behalf.

    Once any permitted executor has consent, preserve that choice set. Revoked
    providers are never silently re-enabled or made mandatory for automatic mode.
    """
    router_consent=_consentimento_do_motor(registro,app_router.AUTO)
    if not router_consent['dado'] or not app_router.allowed(registro,user):return router_consent
    offered={row['id'] for row in _opcoes_de_motor(registro,user)
        if row.get('disponivel') and row['id'] in app_router.DESCRIPTIONS}
    native_ready='nativa' in offered
    if native_ready and (not MODERACAO_LIGADA or iald_motores.consentiu(registro,'openai')):return router_consent
    offered.discard('nativa')
    providers=['claude' if key.startswith('claude-') else key for key in offered]
    if any(iald_motores.consentiu(registro,key) for key in providers):return router_consent
    if native_ready and MODERACAO_LIGADA:
        return _consentimento_do_motor(registro,'openai')
    for key in ('mimo','openai','claude-haiku','kimi','deepseek','claude-sonnet'):
        if key in offered:
            return _consentimento_do_motor(registro,'claude' if key.startswith('claude-') else key)
    return router_consent


def _chat_automatico_autorizado(req_json,user,registro,is_stream,tokens_in,*,_recovery=None):
    from copy import deepcopy
    from flask import stream_with_context
    recovery = _recovery or app_recovery.Recovery(req_json, MOTORES_CFG)
    if _recovery is None:
        recovery.wallet = wallet_runtime.current()
        recovery.memory = app_memory.current()
    elif (wallet_runtime.current() is not recovery.wallet
            or app_memory.current() is not recovery.memory
            or _motor_do_usuario(user)[0] != app_router.AUTO):
        return _sse_aviso('O estado ou a autorização da tarefa mudou.', 'motor_indisponivel')
    if not app_router.allowed(registro,user):
        return _sse_aviso('Modo automático não liberado para esta conta.','motor_indisponivel')
    consent=_consentimento_automatico(registro,user)
    if not consent['dado']:
        return _sse_aviso('Leia e aceite o aviso do modo automático.','consentimento_ia',
            dict(versao=consent['versao'],provedor=consent['provedor'],detalhe=consent['texto']))
    if not is_stream or not isinstance(req_json,dict):
        return jsonify({'error':'Envie chat com stream: true.'}),400
    try:
        science_snapshot = getattr(recovery, 'science_snapshot', None) or _capture_science()
        recovery.science_snapshot = science_snapshot
        client=req_json.get('messages')
        private_media = _private_runtime_for(req_json,user,automatic=True)
        if private_media is not None:
            client=private_media.canonicalize(client,provider='mimo')
            req_json=dict(req_json,messages=client)
        media = app_providers.request_media(client)
        has_media = bool(media['kinds'])
        if has_media:
            if not app_providers.allowed(registro,user,'mimo'):
                return _sse_aviso('MiMo não autorizado para estes anexos. Nada foi enviado.','recurso_indisponivel')
            media_consent = _consentimento_do_motor(registro,'mimo')
            if not media_consent['dado']:
                return _sse_aviso('Leia e aceite o aviso do MiMo para enviar estes anexos.','consentimento_ia',
                    dict(versao=media_consent['versao'],provedor=media_consent['provedor'],detalhe=media_consent['texto']))
        app_providers.wire_messages(client,'routing_validation',provider='mimo' if has_media else None,
            images_authorized=has_media,media_authorized=has_media,private_media=private_media)
        candidates=[]
        candidate_models={}
        for row in _opcoes_de_motor(registro,user):
            key=row['id']
            if key not in app_router.DESCRIPTIONS or not row.get('disponivel'):continue
            if key=='nativa' and MODERACAO_LIGADA and not iald_motores.consentiu(registro,'openai'):continue
            consent_provider='claude' if key.startswith('claude-') else key
            if key == 'nativa' or iald_motores.consentiu(registro,consent_provider):
                candidates.append(key)
                if isinstance(row.get('modelo'),str) and row['modelo']:candidate_models[key]=row['modelo']
        if not candidates:raise ValueError('No consented executor')
        candidates=[key for key in candidates if key not in recovery.excluded
            and _automatic_budget_available(registro,user,key)]
        if not candidates:
            return _sse_aviso('Nenhum modelo autorizado tem orçamento disponível e verificável agora. Nada foi enviado ao JEV.', 'limite')
        operator_context = (operator_bench.routing_context(registro,user)
                            if operator_bench.is_operator(registro,user) else None)
        routing_prompt = media['prompt'] or ('Analise o anexo enviado.' if has_media else '')
        media_budget_options=None
        if private_media is not None:
            private_media.authorize_dispatch()
            preview=_private_preview_body(client,user,registro,private_media,science_snapshot)
            policies=private_media_host.video_proposals(private_media.budget_metadata(client))
            media_budget_options=private_media.routing_options(preview,proposals=policies)
        chosen,receipt=app_router.choose(routing_prompt,candidates,operator_context=operator_context,
            model_ids={key:candidate_models[key] for key in candidates if key in candidate_models},
            multimodal=has_media,media=media,media_integrated=has_media,media_budget_options=media_budget_options,science_snapshot=science_snapshot)
        if chosen not in candidates:raise PermissionError('Executor outside admitted candidates')
        recovery.check_science(receipt)
        if private_media is not None:
            if chosen!='mimo':raise MediaUnavailable('Incompatible private media destination')
            selected_media_plan=private_media.select_routing_policy(receipt['media_policy_id'])
            if selected_media_plan!=receipt['media_budget']:raise MediaError('Changed policy receipt')
        # Recheck permissions/consent after the router returns, before generation.
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Access revoked')
        if chosen not in {r['id'] for r in _opcoes_de_motor(current,user) if r.get('disponivel')}:
            raise PermissionError('Executor revoked')
        consent_provider='claude' if chosen.startswith('claude-') else chosen
        if chosen != 'nativa' and not iald_motores.consentiu(current,consent_provider):
            raise PermissionError('Executor consent revoked')
        if operator_context is not None and not operator_bench.is_operator(current,user):
            raise PermissionError('Operator access revoked')
        if not _automatic_budget_available(current,user,chosen):raise PermissionError('Executor budget changed')
        routing_instruction=app_router.route_instruction(receipt)
        task_scope=recovery.scope
        if task_scope is None and chosen not in ('kimi','nativa'):
            task_scope=_new_app_task_scope(user,executor=chosen,science_snapshot=science_snapshot)
        if task_scope is not None:
            task_scope.executor=chosen
            recovery.bind_scope(task_scope,receipt,app_router)
        selected=dict(current,motor=chosen)
        if chosen.startswith('claude-'):
            selected.update(CLAUDE_ROUTES.select(chosen,current,user))
            response=_chat_claude(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,science_snapshot=science_snapshot)
        elif chosen in app_providers.MODELS:
            response=_chat_avaliacao(req_json,user,selected,is_stream,chosen,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,private_media=private_media,media_admission=receipt.get('media_budget'),science_snapshot=science_snapshot)
        elif chosen=='openai':
            response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,
                recovery_attempt=(recovery.attempt if not recovery.reselected and private_media is None and not has_media else None),science_snapshot=science_snapshot)
        elif chosen=='nativa':
            response=_chat_nativa_automatica(req_json,user,current,routing_instruction=routing_instruction,science_snapshot=science_snapshot)
        else:raise ValueError('No compatible executor')
        if response is None:raise ValueError('No compatible executor')
        if task_scope:response.iald_task_control=task_scope.control
        if _recovery is None and isinstance(response,Response) and response.mimetype=='text/event-stream':
            response=recovery.wrap(response,lambda: _chat_automatico_autorizado(
                deepcopy(recovery.request),user,load_users_estrito().get(user,{}),is_stream,tokens_in,_recovery=recovery))
            response.response=stream_with_context(response.response)
        return response
    except MediaUnavailable:
        return _sse_aviso(private_media_host.PUBLIC_REFERENCE_REFUSAL,'anexo_indisponivel')
    except MediaBudgetError as exc:
        # Whitelisted local diagnosis only; never echo arbitrary exception data.
        if str(exc)=='Uncertain media policy; no automatic quality substitution':
            return _sse_aviso('O seletor não atingiu a confiança mínima para a política de mídia. Núcleo, histórico e anexo foram preservados. O seletor pode ter sido consultado; o anexo não foi enviado ao modelo executor. Nenhum reenvio automático.', 'politica_midia_incerta')
        return _sse_aviso('Anexo excede o contexto, bytes ou orçamento disponíveis; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_excede_contexto')
    except MediaError:
        return _sse_aviso('Não foi possível validar o anexo ou sua admissão; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_validacao_recusada')
    except app_router.RoutingContextOverflow:
        return _sse_aviso('A memória obrigatória desta conversa excede o espaço do seletor automático. Nada foi enviado aos provedores. Abra uma nova conversa para continuar; a conversa anterior permanece salva.','roteamento_contexto_excedido')
    except (ValueError,PermissionError,OSError,KeyError,TypeError,RuntimeError):
        return _sse_aviso('Não foi possível concluir a escolha automática. Tente novamente em alguns instantes; não houve reenvio para outro executor.','motor_indisponivel')


def _chat_avaliacao(req_json, user, registro, is_stream, motor, *, task_scope=None, dispatch_check=None, routing_instruction=None, private_media=None, media_admission=None, science_snapshot=None):
    if not app_providers.allowed(registro, user, motor):
        return _sse_aviso('Modelo não liberado para esta conta.', 'motor_indisponivel')
    if not is_stream or not isinstance(req_json, dict):
        return jsonify({'error': 'Envie um pedido de chat com stream: true.'}), 400
    consent = _consentimento_do_motor(registro, motor)
    if not consent['dado']:
        return _sse_aviso('Leia e aceite o aviso deste provedor antes de conversar.', 'consentimento_ia',
            dict(versao=consent['versao'], provedor=consent['provedor'], detalhe=consent['texto']))
    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)
    try:dispatch_check()
    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')
    reason = app_providers.availability(motor)
    if reason: return _sse_aviso(reason, 'motor_indisponivel')
    try:
        # Same verified fixed kernel/core/cluster package already deployed for
        # Haiku, preserved byte-for-byte. Its Anthropic token count is NOT a
        # token measurement for another provider. Detailed public sources remain
        # available through the restricted tool loop (pre-retrieval for Kimi).
        science_snapshot = science_snapshot or _capture_science()
        package = _load_shared_science_package(science_snapshot)
        prefix = package.prefix
        if _memoria_modo_integral(MOTORES_CFG) or not prefix or iald_motor_claude.MARCA_ATLAS_INTEGRAL in prefix:
            raise ValueError('Memória científica pública não pôde ser validada.')
        client = req_json.get('messages')
        if not isinstance(client, list) or any(not isinstance(m, dict) for m in client):
            raise ValueError('Invalid message list')
        private_media=private_media or _private_runtime_for(req_json,user,automatic=False)
        if private_media is not None:
            if motor!='mimo':raise MediaUnavailable('Incompatible media destination')
            client=private_media.canonicalize(client,provider=motor)
            if media_admission is not None and private_media.video_policy!=media_admission['policy']:
                raise MediaError('Selected media policy changed')
        retrieval = science_snapshot.pre_retrieve(client)
        profile, search_instruction = iald_motores.extrair_do_cliente(client or [])
        note = 'Modelo de inferência: '+app_providers.MODELS[motor]['label']+'. Preserve o regime IALD e os estatutos das fontes. '
        note += 'Use LaTeX com delimitadores \\( \\) ou \\[ \\]. Nunca altere uma fórmula apenas para mudar sua apresentação.'
        note += retrieval['prompt']
        if routing_instruction and task_scope is None: note += '\n'+routing_instruction
        if task_scope: note += '\n'+task_policy.INSTRUCTIONS+'\n'+getattr(task_scope,'instructions','')
        if search_instruction: note += '\n'+iald_motores.LUPA_CANONICA
        messages = app_providers.wire_messages(client, prefix, note + ('\nUSER CONTEXT:\n'+profile if profile else ''),
            provider=motor,images_authorized=(motor=='mimo' and consent['dado']),
            media_authorized=(motor=='mimo' and consent['dado']),private_media=private_media)
        if MODERACAO_LIGADA:
            # Moderate textual parts only; inline media stays with the consented MiMo executor.
            moderation_text = [m['content'] if isinstance(m['content'],str) else '\n'.join(
                part['text'] for part in m['content'] if part.get('type')=='text') for m in messages[1:]]
            decision = iald_motores.moderar_textos([profile]+moderation_text,
                req_lib.post, MOTORES_CFG.url_base, MOTORES_CFG.chave, cache=_CACHE_MODERACAO)
            if decision.get('bloquear'): return _sse_aviso(iald_motores.MENSAGEM_MODERACAO_BLOQUEIO, 'moderacao')
            if not decision.get('ok') and MODERACAO_FALHA == 'bloquear':
                return _sse_aviso(MSG_MODERACAO_INDISPONIVEL, 'moderacao_indisponivel')
            if decision.get('acolher'): messages[0]['content'] += '\n'+iald_motores.INSTRUCAO_ACOLHIMENTO
        definitions = (iald_kernel.tool_definitions()+iald_core_indexado.tool_definitions()+iald_fontes_publicas.tool_definitions())
        definitions += [t for t in _ferramentas_para('app') if (t.get('function') or {}).get('name') in app_providers.TOOL_NAMES]
        definitions = list({t['function']['name']: t for t in definitions if t['function']['name'] in app_providers.TOOL_NAMES}.values())
        if task_scope and motor != 'kimi':definitions += task_scope.tools
        if motor == 'kimi':
            messages[0]['content'] += '\nNesta chamada Kimi não há ferramentas interativas; a recuperação acima é local, parcial e rastreável.'
        admission = {'messages': messages, 'tools': definitions}
        if private_media is not None:
            private_media.authorize_dispatch()
            full_body=dict(model=app_providers.MODELS[motor]['model'],messages=messages,tools=definitions,
                stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
            media_admission=private_media.admit(full_body,app_providers.MODELS[motor]['output'])
        else:
            reserve = (app_providers.MODELS[motor]['output'] if motor == 'kimi' else
                app_providers.output_budget(admission, app_providers.MODELS[motor]['output']))
            app_providers.check_window(admission, reserve)
    except MediaUnavailable:
        return _sse_aviso(private_media_host.PUBLIC_REFERENCE_REFUSAL,'anexo_indisponivel')
    except MediaBudgetError as exc:
        # Whitelisted local diagnosis only; never echo arbitrary exception data.
        if str(exc)=='Uncertain media policy; no automatic quality substitution':
            return _sse_aviso('O seletor não atingiu a confiança mínima para a política de mídia. Núcleo, histórico e anexo foram preservados. O seletor pode ter sido consultado; o anexo não foi enviado ao modelo executor. Nenhum reenvio automático.', 'politica_midia_incerta')
        return _sse_aviso('Anexo excede o contexto, bytes ou orçamento disponíveis; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_excede_contexto')
    except MediaError:
        return _sse_aviso('Não foi possível validar o anexo ou sua admissão; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_validacao_recusada')
    except (ValueError, OSError, TypeError, KeyError):
        return _sse_aviso('A memória ou o histórico não cabem ou não puderam ser validados. Nada foi enviado ao modelo.', 'pedido_invalido')
    spending=None
    if wallet_runtime.enabled():
        spending=wallet_runtime.provider_account(SERVE_DIR,motor,CLAUDE_ROUTES.base.cota_global_usd)
    elif motor in ('mimo','deepseek') and user!='luiz':
        try:
            daily, group = CLAUDE_ROUTES.public_budget()
            spending = app_spend.PublicAccount(SERVE_DIR,hashlib.sha256(user.encode('utf-8')).hexdigest(),
                daily,group,CLAUDE_ROUTES.base.cota_global_usd)
        except (ValueError,OSError,TypeError,KeyError):
            return _sse_aviso('O orçamento público deste modelo precisa de conferência. Nada foi enviado.','limite',{'bloqueado_por':'razao'})
    flow = APP_EVALUATION.stream(motor, messages, definitions,
        lambda name, args: (_execute_scope_tool(task_scope,name,args,user) if task_scope and name in _task_scope_names(task_scope) else
            _science_tool(science_snapshot,_executar_ferramenta_claude,name,args,user=user,operator_authorized=False)),
        memory_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
        account_key=hashlib.sha256(user.encode('utf-8')).hexdigest(),spending=spending,
        task_control=task_scope.control if task_scope else None,authorize=dispatch_check,
        task_tool_names=_task_scope_names(task_scope),private_media=private_media)
    return Response(flow, content_type='text/event-stream', headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


MSG_CLAUDE_NAO_LIBERADO = "O motor Claude não está liberado para esta conta. Nada foi enviado."
# 21/09/2026 (revisão de segurança): o Claude nunca recebe o Atlas integral (§V/§VI/§X)
MSG_CLAUDE_ATLAS_INTEGRAL = ("O motor Claude não atende com a configuração atual de memória do servidor "
                             "(IALD_MEMORIA_MODO=atlas_integral leva o Atlas inteiro). Nada foi enviado.")


def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI, *, task_scope=None, dispatch_check=None, routing_instruction=None, recovery_attempt=None, science_snapshot=None):
    """O caminho externo inteiro, para o provedor do `motor` (21/09/2026; antes era _chat_openai).

    Com motor openai, byte a byte o de antes. Com motor claude, o MESMO pipeline — reservas, razão,
    rótulo, voltas do agente, ferramentas, medição TGLC — e o MESMO prefixo TGL (_contexto_externo), com:
    configuração, razão, reservas e pedidos por minuto do claude; consentimento da Anthropic;
    max_completion_tokens = CLAUDE_CFG.max_saida (o pensamento adaptativo gasta a mesma saída); entrada
    estimada e prefixo descontado da cota × fator_tokens; envio por iald_motor_claude.post_como_openai
    (um EstadoClaude por pedido, para o pensamento assinado voltar nas voltas com ferramenta); Atlas
    sem §V/§VI/§X (_executar_ferramenta_claude); moderação na chave da OpenAI; nunca a bandeira de
    crédito da OpenAI; nunca None."""
    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)
    claude = motor == iald_motores.CLAUDE
    if claude: recovery_attempt = None
    razao = RAZAO_CLAUDE if claude else RAZAO_OPENAI
    limitador = LIMITE_CLAUDE if claude else LIMITE_OPENAI
    try:
        cfg = (CLAUDE_ROUTES.configuration(registro, user) if claude
               else iald_motores.config_da_conta(MOTORES_CFG, registro))
    except (ValueError, PermissionError, OSError, KeyError):
        return _sse_aviso("Modelo Claude indisponível para esta conta.", "motor_indisponivel")
    haiku = claude and cfg.modelo == _HAIKU_PROFILE.model
    if haiku and not _haiku_client_ready():
        return _sse_aviso("Atualize o aplicativo para usar o Haiku com memória integral.", "recurso_indisponivel")
    if claude:
        # o prefixo e as consultas canônicas são os da casa: o modo de memória é o da configuração da OpenAI
        cfg.memoria_modo = MOTORES_CFG.memoria_modo
    if not isinstance(req_json, dict):
        req_json = {}
    admin = bool(registro.get("admin"))
    plano = iald_motores.plano_de(registro)
    gratuito = plano == iald_motores.GRATUITO
    chave_cota = _chave_cota_de(registro, user)
    modelo = iald_motores.modelo_para(registro, cfg)
    if claude and not CLAUDE_ROUTES.options(registro, user):
        # a outra trava: api_post só chega aqui com escolher_motor == claude; conferido de novo, e
        # recusa visível — nunca desvio para outro motor
        print(f"[claude] {user}: conta fora da lista do claude (ou gratuita); nada enviado", flush=True)
        return _sse_aviso(MSG_CLAUDE_NAO_LIBERADO, "motor_indisponivel")
    if claude and _memoria_modo_integral(MOTORES_CFG):
        # 21/09/2026 (revisão de segurança, ALTO): em atlas_integral o prefixo leva o Atlas INTEIRO,
        # com §V (patentes), §VI (caminhos) e §X (estado operacional) — o que o operador mandou deixar
        # FORA da Anthropic ("O mesmo pacote do ChatGPT", sem §V/§VI/§X). Antes só o gratuito era
        # recusado neste modo, e a conta do claude nunca é gratuita.
        print(f"[claude] {user}: IALD_MEMORIA_MODO=atlas_integral; nada enviado à Anthropic", flush=True)
        return _sse_aviso(MSG_CLAUDE_ATLAS_INTEGRAL, "motor_indisponivel")
    if gratuito and _memoria_modo_integral(cfg):
        # 14/09/2026 (noite, tarefa SV): o prompt levaria o Atlas inteiro, com §V, §VI e §X
        print(f"[motores] {user}: plano gratuito recusado em IALD_MEMORIA_MODO=atlas_integral", flush=True)
        return _sse_aviso(MSG_GRATUITO_ATLAS_INTEGRAL, "motor_indisponivel")
    motivo = _motor_externo_indisponivel(modelo, cfg) if claude else _motor_externo_indisponivel(modelo)
    if motivo:
        print(f"[motores] {user}: {motivo}", flush=True)
        if cfg.reserva_nativa and not gratuito and not claude:
            return None
        return _sse_aviso(motivo, "motor_indisponivel")
    if not is_stream:
        return jsonify({"error": "O motor externo só atende com stream: true."}), 400
    if gratuito:
        # 14/09/2026 (noite, tarefa SV — revisão COTAS, regressão 1): imagem no gratuito é recusada
        # ANTES de qualquer conta de saldo, sem chamar o modelo (ver MSG_IMAGEM_GRATUITO)
        mensagens_cliente = req_json.get("messages") if isinstance(req_json.get("messages"), list) else []
        ultima_do_usuario = next((m for m in reversed(mensagens_cliente)
                                  if isinstance(m, dict) and m.get("role") == "user"), None)
        if ultima_do_usuario is not None and _tem_imagem(ultima_do_usuario.get("content")):
            print(f"[motores] {user}: imagem recusada no plano gratuito", flush=True)
            return _sse_aviso(MSG_IMAGEM_GRATUITO, "recurso_indisponivel", {"recurso": "imagens"})
        if any(isinstance(m, dict) and _tem_imagem(m.get("content")) for m in mensagens_cliente):
            req_json = dict(req_json, messages=[_sem_imagens(m) for m in mensagens_cliente])
    if claude and not iald_motores.consentiu(registro, iald_motores.CLAUDE):
        # 21/09/2026: o consentimento da ANTHROPIC — o da OpenAI não o substitui
        return _sse_aviso(
            "Esta conta está no Claude, da Anthropic, e isso precisa do seu consentimento. Abra o "
            "aviso para ler o que é enviado e decidir.",
            "consentimento_ia",
            {"versao": iald_motores.VERSAO_CONSENTIMENTO_ANTHROPIC, "provedor": "Anthropic", "modelo": modelo,
             "detalhe": iald_motores.TEXTO_CONSENTIMENTO_ANTHROPIC})
    if not claude and not iald_motores.consentiu(registro):
        return _sse_aviso(
            "Esta conta responde pelo serviço de IA da OpenAI e isso precisa do seu "
            "consentimento. Abra o aviso para ler o que é enviado e decidir.",
            "consentimento_ia",
            {"versao": iald_motores.VERSAO_CONSENTIMENTO, "provedor": "OpenAI", "modelo": modelo,
             "detalhe": iald_motores.TEXTO_CONSENTIMENTO})
    try:dispatch_check()
    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')
    soltar = []           # o que devolver no fim: a marca de andamento e a vaga do semáforo
    entregue = False
    if gratuito:
        marca = _MarcaAndamento.tomar(chave_cota)
        if marca is None:
            print(f"[motores] {user}: já há uma resposta em andamento nesta cota gratuita", flush=True)
            return _sse_aviso(MSG_EM_ANDAMENTO, "em_andamento")
        soltar.append(marca.soltar)
    try:
        permitido, motivo, bloqueado_por = wallet_runtime.permit(
            cfg, razao, limitador, user, admin, plano=plano, chave_cota=chave_cota, detalhado=True)
        if not permitido:
            return _aviso_limite(motivo, bloqueado_por, user, registro, motor)
        limites = iald_motores.limites_do_plano(cfg, plano)
        cfg.cota_usuario_usd = cfg.cota_operador_usd = limites["usd_dia"]
        cfg.janela = iald_motores.janela_do_plano(cfg, plano)
        saldo_inicial = None
        if gratuito and not wallet_runtime.enabled():
            try:
                saldo_inicial, campo_saldo = iald_motores.saldo_de_tokens(
                    limites, razao.leitura_de_cota(user, chave_cota, plano))
            except Exception as exc:          # noqa: BLE001 — fail-closed
                print(f"[motores] controle de uso ilegível ({exc}); gasto bloqueado", flush=True)
                return _aviso_limite(iald_motores.MSG_RAZAO_ILEGIVEL, "razao", user, registro, motor)
            if saldo_inicial < iald_motores.SALDO_MINIMO_TOKENS:
                return _aviso_limite(iald_motores.MSG_SALDO_MES if campo_saldo == "tokens_mes"
                                     else iald_motores.MSG_SALDO_DIA, campo_saldo, user, registro, motor)

        superficie = "app" if session.get("app_surface") else str(req_json.get("iald_surface") or "web").strip().lower()
        modo = "think" if (req_json.get("iald_mode") == "think" and limites["pensar"]) else "fast"
        mensagens = req_json.get("messages") or []
        tem_imagem, texto_ultima = False, ""
        for m in reversed(mensagens):
            if isinstance(m, dict) and m.get("role") == "user":
                c = m.get("content", "")
                if isinstance(c, list):
                    tem_imagem = any(isinstance(p, dict) and p.get("type") == "image_url" for p in c)
                texto_ultima = iald_motores.texto_de(c)
                break
        ultima = texto_ultima.lower()
        instrucao = "" if registro.get("sacred_language") else INSTRUCAO_LINGUAGEM_TECNICA
        if routing_instruction and task_scope is None: instrucao += '\n'+routing_instruction
        # 15/09/2026: a própria IALD avisa o OPERADOR quando o crédito da OpenAI está crítico
        # (21/09/2026: só no motor openai — o aviso é do crédito da OpenAI e fica fora do claude)
        # ⚠ AO LADO (22/09/2026): agora são os dois créditos, cada um nomeado no texto do aviso
        # (ordem do operador: "saber o que tenho de crédito em cada operadora") — vale nos dois motores
        alerta_saldo = _alerta_saldo_operador(registro, mensagens, user)
        if alerta_saldo:
            instrucao = (instrucao + "\n\n" if instrucao else "") + alerta_saldo

        permitidas = (_haiku_tool_definitions() if haiku
                      else _ferramentas_externas(cfg, limites, superficie, gratuito) + app_memory.tool_definitions())
        if haiku:
            permitidas += [t for t in _ferramentas_para('app') if t['function']['name'] in ('search_web','fetch_url','get_current_datetime','iald_public_search')]
        if task_scope:
            permitidas += task_scope.tools
            instrucao += "\n"+task_policy.INSTRUCTIONS+'\n'+getattr(task_scope,'instructions','')
        usar_agente = bool(permitidas) and (task_scope is not None or haiku or cfg.memoria_modo != "prompt" or
                         (not tem_imagem and _precisa_ferramentas(ultima)))
        # 14/09/2026 23:02 (Claude, reverificação final, item 5): com ferramentas, a 2ª volta também
        # precisa caber no saldo — senão a 1ª é cobrada e a pessoa fica sem resposta (medido: 4.681
        # tokens levaram o dia a 63% sem nada). Estimativa conservadora pela CPT do texto do cliente
        # (a janela e o saldo cortam depois, então ela só sobra): se duas voltas não cabem, responde
        # direto, sem ferramentas.
        if gratuito and not haiku and usar_agente and saldo_inicial is not None:
            texto_cliente = sum(len(iald_motores.texto_de(m.get("content"))) for m in mensagens
                                if isinstance(m, dict) and m.get("role") in ("user", "assistant"))
            entrada_aprox = int(texto_cliente / iald_motores.CPT) + 1500      # + ferramentas e nota
            duas_voltas = (2 * entrada_aprox + int(GRATUITO_MAX_CHARS_FERRAMENTA / iald_motores.CPT)
                           + 2 * iald_motores.SALDO_MINIMO_TOKENS)
            if duas_voltas > saldo_inicial:
                usar_agente = False
                print(f"[motores] {user}: saldo gratuito não cobre duas voltas; resposta sem ferramentas",
                      flush=True)
        nomes = [t["function"]["name"] for t in permitidas] if usar_agente else []
        # A saída máxima do plano vale no modo rápido. No pensar ela cresce na MESMA proporção
        # que IALD_OPENAI_MAX_SAIDA_PENSAR guarda sobre IALD_OPENAI_MAX_SAIDA (padrão 2×): o
        # raciocínio come a saída, e o assinante não pode perder o teto de pensar que já tinha.
        if modo == "think":
            proporcao = max(cfg.max_saida_pensar / max(cfg.max_saida, 1), 1.0)
            teto_saida = min(cfg.max_saida_pensar, int(limites["max_saida"] * proporcao))
        else:
            teto_saida = min(cfg.max_saida, limites["max_saida"])
        if claude:
            # 21/09/2026: no claude o pensamento adaptativo gasta o MESMO max_tokens da resposta; com o
            # teto do plano (4.096–8.192) a resposta pararia em "length". Vale IALD_CLAUDE_MAX_SAIDA.
            teto_saida = cfg.max_saida
        try:
            if haiku:
                science_snapshot = science_snapshot or _capture_science()
                haiku_package = _load_haiku_package(science_snapshot)
                haiku_snapshot = _haiku_snapshot(haiku_package)
                haiku_adapter = _CheckedHaikuAdapter(iald_motor_claude, haiku_snapshot, trusted_openai_tools=permitidas)
                prompt_externo = haiku_package.prefix
                memoria_info = {"context_sha256": haiku_package.measurement.prefix_sha256, "scope": "HAIKU_MEASURED_PUBLIC"}
                cfg.janela = _HAIKU_PROFILE.window
            else:
                science_snapshot = science_snapshot or _capture_science()
                prompt_externo = science_snapshot.prefix
                memoria_info = {"context_sha256":hashlib.sha256(prompt_externo.encode()).hexdigest(), "scope":"PUBLIC_FIXED_SOURCES", "identity":dict(science_snapshot.identity)}
            instrucao += science_snapshot.pre_retrieve(mensagens)["prompt"]
            if gratuito and memoria_info.get('scope') == 'PUBLIC_FIXED_SOURCES':
                # The shared fixed knowledge must not consume the 32k conversation window.
                # Spending, user quotas, moderation, tools and native-access rules still apply.
                prefix_tokens = max(iald_motores.estimar_tokens(prompt_externo),
                    iald_memoria_canonica.payload_tokens({'messages': [
                        {'role': 'developer', 'content': prompt_externo}]}))
                cfg.janela = min(MOTORES_CFG.janela, prefix_tokens + iald_motores.JANELA_GRATUITO)
            # 21/09/2026: o claude recebe as MESMAS mensagens (o prefixo abre a mensagem developer, intacto);
            # a nota de serviço — parte variável, fora do cache — diz que quem responde é o Claude
            if haiku:
                para_openai, info = _assemble_haiku_messages(
                    iald_motores, mensagens, prompt_externo, modelo, nomes, instrucao)
            else:
                para_openai, info = iald_motores.montar_mensagens(
                    mensagens, prompt_externo, modelo, nomes, cfg.janela, teto_saida, instrucao,
                    provedor=iald_motores.PROVEDORES[motor])
        except ValueError as exc:
            return _sse_aviso(f"Pedido inválido para o motor externo: {exc}.", "pedido_invalido")
        if claude and iald_motor_claude.MARCA_ATLAS_INTEGRAL in prompt_externo:
            # 21/09/2026 (revisão de segurança): defesa em profundidade — qualquer que seja o modo, o
            # prefixo com o Atlas integral não sai para a Anthropic (o envio também confere)
            print(f"[claude] {user}: o prefixo leva o Atlas integral; nada enviado à Anthropic", flush=True)
            return _sse_aviso(MSG_CLAUDE_ATLAS_INTEGRAL, "motor_indisponivel")
        para_openai = app_memory.project_messages(para_openai)
        try:
            pedido_saida = int(req_json.get("max_tokens") or 0) or teto_saida
        except (TypeError, ValueError):
            pedido_saida = teto_saida

        base = iald_motores.montar_payload(
            cfg, modelo, para_openai, modo, min(pedido_saida, teto_saida),
            identificador=iald_motores.identificador_seguro(
                user, app.secret_key, "iald-anthropic-v1:" if claude else "iald-openai-v1:"),
            chave_cache="iald-" + memoria_info["context_sha256"][:16])
        if claude:
            base["max_completion_tokens"] = cfg.max_saida       # antes da reserva (ver teto_saida acima)

        native_count_cache = {}
        estado_claude = iald_motor_claude.EstadoClaude() if claude else None
        def count_haiku_wire(wire):
            identity = hashlib.sha256(json.dumps(wire, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if identity not in native_count_cache:
                try:
                    client = iald_motor_claude.cliente_para(cfg).with_options(max_retries=0)
                    native_count_cache[identity] = _count_haiku_native_request(client, wire)
                except Exception as exc:
                    raise iald_memoria_canonica.MemoryUnavailable("Contagem de contexto Haiku indisponível; nenhuma geração iniciada.") from exc
            return native_count_cache[identity]

        def tokens_para_saldo(payload):
            if not haiku:
                return _tokens_do_payload_para_saldo(payload)
            payload = _haiku_attach_tools(payload, permitidas)
            wire = haiku_adapter.converter_pedido(cfg, payload, prefixo=prompt_externo, estado=estado_claude, bind_context=False)
            wire.update(_haiku_reasoning(modelo, wire["max_tokens"], effort=cfg.esforco_claude))
            return count_haiku_wire(wire)

        def prefixo_da_cota(msgs):
            """O prefixo fixo que a cota da pessoa não paga, em tokens do PROVEDOR (× fator_tokens no
            claude: o `usage` dele vem em tokens Claude). Na OpenAI, a estimativa de sempre."""
            if haiku:
                # Same measured minimal-request baseline used by the package;
                # extra profile/history/tools are counted in the full request.
                return haiku_package.measurement.permanent_tokens
            estimado = iald_motores.prefixo_tokens_estimado(msgs)
            return math.ceil(estimado * max(float(cfg.fator_tokens or 1.0), 1.0)) if claude else estimado
        prefixo = prefixo_da_cota(para_openai)

        descartadas_saldo = 0
        if gratuito and not wallet_runtime.enabled():
            # O histórico mais antigo sai até a entrada estimada caber no saldo (a janela já fez
            # o mesmo corte pelo tamanho). Sobrou só a última mensagem e ainda não cabe → limite.
            def entrada_estimada():
                amostra = dict(base, messages=para_openai)
                if usar_agente:
                    amostra["tools"] = permitidas
                return max(0, tokens_para_saldo(amostra) - prefixo)
            try:
                entrada = entrada_estimada()
                while not haiku and entrada + iald_motores.SALDO_MINIMO_TOKENS > saldo_inicial and len(para_openai) > 2:
                    para_openai.pop(1)
                    descartadas_saldo += 1
                    while len(para_openai) > 2 and para_openai[1].get("role") != "user":
                        para_openai.pop(1)          # a conversa não começa pela resposta da IALD
                        descartadas_saldo += 1
                    entrada = entrada_estimada()
            except iald_memoria_canonica.MemoryUnavailable as exc:
                return _sse_aviso(f"Pedido inválido para o motor externo: {exc}.", "pedido_invalido")
            if entrada + iald_motores.SALDO_MINIMO_TOKENS > saldo_inicial:
                return _aviso_limite(iald_motores.MSG_SALDO_MES if campo_saldo == "tokens_mes"
                                     else iald_motores.MSG_SALDO_DIA, campo_saldo, user, registro, motor)
            base["messages"] = para_openai
            base["max_completion_tokens"] = max(iald_motores.SALDO_MINIMO_TOKENS,
                                                min(base["max_completion_tokens"], saldo_inicial - entrada))

        # MODERAÇÃO de todo o texto do cliente que vai nesta chamada (MÉDIO 1): o perfil e cada
        # mensagem mantida (usuário e assistente — o histórico vem do cliente e pode ser forjado).
        contexto_usuario, _lupa = iald_motores.extrair_do_cliente(mensagens)
        textos_cliente = ([contexto_usuario] if contexto_usuario else []) + [
            iald_motores.texto_de(m.get("content")) for m in para_openai[1:]]
        if gratuito and sum(len(t) for t in textos_cliente) > iald_motores.TETO_TOTAL_TEXTO_GRATUITO:
            return _sse_aviso(MSG_TEXTO_LONGO, "pedido_invalido", {"motivo": "texto_longo"})
        # 21/09/2026: a moderação é SEMPRE na chave da OpenAI (a Anthropic não tem endpoint de moderação)
        cfg_moderacao = MOTORES_CFG if claude else cfg
        if MODERACAO_LIGADA:
            moderacao = iald_motores.moderar_textos(textos_cliente, req_lib.post, cfg_moderacao.url_base,
                                                    cfg_moderacao.chave, cache=_CACHE_MODERACAO)
            categorias = ",".join(moderacao.get("categorias") or []) or "-"
            if moderacao.get("bloquear"):
                # (acolher vence bloquear DENTRO do mesmo bloco — ver iald_motores.moderar_textos)
                auth_log("MODERACAO_BLOQUEIO", user, f"categorias={categorias}")
                return _sse_aviso(iald_motores.MENSAGEM_MODERACAO_BLOQUEIO, "moderacao")
            if not moderacao.get("ok"):
                print(f"[moderacao] {user}: {moderacao.get('erro') or 'falhou'}; "
                      f"{'pedido recusado' if MODERACAO_FALHA == 'bloquear' else 'seguindo sem moderação'}",
                      flush=True)
                if MODERACAO_FALHA == "bloquear":
                    return _sse_aviso(MSG_MODERACAO_INDISPONIVEL, "moderacao_indisponivel")
            if moderacao.get("acolher"):
                # quem fala de se ferir recebe o CVV, não uma recusa seca
                auth_log("MODERACAO_ACOLHIMENTO", user, f"categorias={categorias}")
                para_openai[0] = dict(para_openai[0], content=para_openai[0]["content"] + "\n\n"
                                      + iald_motores.INSTRUCAO_ACOLHIMENTO)
                base["messages"] = para_openai
                prefixo = prefixo_da_cota(para_openai)

        if gratuito:
            if not _SEMAFORO_GRATUITO.acquire(blocking=False):
                print(f"[motores] {user}: sem vaga no uso gratuito ({GRATUITO_STREAMS_SIMULTANEOS} streams)", flush=True)
                return _sse_aviso(MSG_OCUPADO, "ocupado")
            soltar.append(_Vaga(_SEMAFORO_GRATUITO).soltar)

        try:
            if haiku:
                conta = legado = _HaikuNativeAccount(motors=iald_motores, budget=iald_orcamento,
                    guard=_guarda_do_motor(motor), ledger=razao, cfg=cfg, user=user, admin=admin,
                    model=modelo, quota_key=chave_cota, plan=plano, prefix_tokens=prefixo,
                    count_request=tokens_para_saldo)
            else:
                legado = iald_motores.ContaDoPedido(
                    razao, user, modelo, cfg.precos(modelo), chave_cota=chave_cota, plano=plano,
                    prefixo_tokens=prefixo,
                    # 21/09/2026 (revisão de custo): chamada sem usage no razão do claude × fator_tokens,
                    # como o guarda de reservas a liquida (1.0 na OpenAI: como antes)
                    fator_tokens=cfg.fator_tokens if claude else 1.0)
                conta = iald_orcamento.ReservedAccount(
                    _guarda_do_motor(motor), legado, cfg, user, admin, modelo, quota_key=chave_cota,
                    group=plano, group_limit=cfg.cota_global_gratuito_usd if gratuito else None)
        except Exception:
            return _aviso_limite(MSG_RESERVA_INDISPONIVEL, "razao", user, registro, motor)
        if gratuito and not wallet_runtime.enabled():
            conta = iald_motores.ContaComSaldo(conta, iald_motores.SaldoDoPedido(
                cfg, razao, user, plano, chave_cota, legado, prefixo,
                tokens_para_saldo))
        haiku_context_notices = []
        enviar = None
        if claude:
            # 21/09/2026: quem fala com a API é o SDK da Anthropic, por iald_motor_claude — a chave vai
            # por ele, NUNCA num cabeçalho montado aqui. `prefixo` = o texto EXATO que abre a mensagem
            # developer (o mesmo que a OpenAI recebe): vira o bloco de sistema com cache_control.
            # Um EstadoClaude por pedido: o pensamento assinado de cada volta com ferramenta volta intacto.
            url, cabecalhos = "https://api.anthropic.com/v1/messages", {}
            def enviar(payload, timeout=None):
                if haiku:
                    payload = _haiku_attach_tools(payload, permitidas)
                    # The agent has now set its final tool_choice. Count/reserve
                    # this exact payload before the sole provider send.
                    from claude_tool_budget import fit_latest_tool_results, ToolResultsDoNotFit
                    try:
                        before_fit = payload
                        payload = fit_latest_tool_results(payload, tokens_para_saldo, cfg.janela)
                        if payload["messages"] != before_fit["messages"]:
                            haiku_context_notices.append({"fase": "respondendo", "rotulo":
                                "Resultados em excertos parciais; respondendo com as evidências que cabem."})
                    except ToolResultsDoNotFit as exc:
                        raise iald_orcamento.WindowError(str(exc)) from exc
                    conta.iniciar_chamada(payload)
                    _check_reserved_dispatch(dispatch_check,conta)
                    response, decision = post_guarded(haiku_adapter, cfg, payload,
                        requested_model=modelo, server_policy=_claude_policy(registro, user),
                        prefix=prompt_externo, memory=haiku_package.measurement,
                        state=estado_claude, timeout=timeout, counter=count_haiku_wire)
                    return response
                return app_memory.http_call('model.claude', iald_motor_claude.post_como_openai, cfg, payload, prefixo=prompt_externo,
                                                          estado=estado_claude, timeout=timeout)
        else:
            url = cfg.url_base + "/chat/completions"
            cabecalhos = {"Authorization": f"Bearer {cfg.chave}", "Content-Type": "application/json"}
        log_request(user, "/v1/chat/completions", "POST", tokens_in=info["tokens_estimados"],
                    status=f"{motor}_agente" if usar_agente else f"{motor}_stream")
        if info["descartadas"]:
            print(f"[motores] {user}: {info['descartadas']} mensagem(ns) antiga(s) fora da janela de "
                  f"{cfg.janela} tokens", flush=True)
        if descartadas_saldo:
            print(f"[motores] {user}: {descartadas_saldo} mensagem(ns) antiga(s) fora do saldo de tokens "
                  f"do uso gratuito", flush=True)

        if usar_agente:
            exigir_consulta = cfg.memoria_modo != "prompt" and bool(re.search(
                r"\b(localiz\w*|procur\w*|busqu\w*|pesquis\w*|consult\w*|verifi\w*|confira|conferir|leia|ler)\b", ultima))
            adaptador = iald_motores.AdaptadorAgente(cfg, base, url, cabecalhos,
                                                   _DeferredHaikuAccount(conta) if haiku else conta,
                                                   exigir_consulta=exigir_consulta, enviar=enviar,
                                                   provedor=motor,
                                                   # 21/09/2026 (revisão): JSON inválido não roda
                                                   entrada_invalida=estado_claude.entrada_invalida if claude else None)
            adaptador.recovery_attempt = recovery_attempt
            if haiku:
                adaptador.context_notices = haiku_context_notices
            if claude:
                executor = _executar_ferramenta_claude
            elif gratuito:
                executor = _executar_ferramenta_gratuito
            else:
                executor = None

            fallback_executor = executor or execute_public_tool
            executor = lambda name,args,**kwargs: _science_tool(science_snapshot,fallback_executor,name,args,**kwargs)
            if task_scope:
                original_executor=executor
                def task_executor(name,args,**kwargs):
                    if name in _task_scope_names(task_scope):return json.dumps(_execute_scope_tool(task_scope,name,args,user),ensure_ascii=False)
                    return original_executor(name,args,**kwargs)
                executor=task_executor

            def gerar():
                try:
                    yield from agent_loop(para_openai, user=user, max_tokens=base["max_completion_tokens"],
                                          ferramentas=permitidas, operator_authorized=False, motor=adaptador,
                                          max_voltas=GRATUITO_MAX_VOLTAS_AGENTE if gratuito else None,
                                          max_chars_canonico=GRATUITO_MAX_CHARS_FERRAMENTA if gratuito else None,
                                          executar=executor,
                                          responder_na_ultima=gratuito,
                                          verificar_payload=lambda _:_check_reserved_dispatch(dispatch_check,conta), task_control=task_scope.control if task_scope else None,
                                          task_tool_names=_task_scope_names(task_scope))
                except app_recovery.DefinitiveRefusal as exc:
                    conta.descartar_ultima_chamada()
                    exc.settled = True
                    raise
                except (iald_motores.CotaEsgotada, iald_orcamento.BudgetError) as exc:
                    yield from _linhas_da_recusa(exc, user, registro, motor)
                except iald_memoria_canonica.MemoryUnavailable as exc:
                    yield from _sse_aviso(str(exc), "motor_indisponivel").response
                except Exception as exc:
                    print("[motores] falha do agente: " + iald_motores.mascarar(exc), flush=True)
                    yield from _sse_aviso("Falha no serviço externo; o registro de uso foi preservado.", "falha_motor").response
                finally:
                    conta.fechar()
        else:
            def gerar():
                try:
                    yield ": iald-motor-externo\n\n"
                    payload = base
                    for tentativa in (1, 2):
                        enviou = False
                        try:
                            if not haiku:
                                conta.iniciar_chamada(payload)
                            if enviar is not None:
                                fazer = lambda: enviar(payload, (10, cfg.timeout))          # noqa: E731
                            else:
                                fazer = lambda: app_memory.http_call('model._chat_externo', req_lib.post, url, json=payload, headers=cabecalhos,  # noqa: E731
                                                             stream=True, timeout=(10, cfg.timeout))
                            enviar_verificado = fazer
                            def fazer():
                                _check_reserved_dispatch(dispatch_check,conta)
                                return enviar_verificado()
                            for pedaco in iald_motores.transmitir(
                                    fazer,
                                    ao_uso=conta.uso, ao_texto=conta.texto, intervalo=AGENT_KEEPALIVE_SEC,
                                    avisos=claude, recovery=recovery_attempt):     # 21/09/2026 (revisão): o aviso da recusa passa
                                if pedaco.startswith("data: {"):
                                    enviou = True
                                yield pedaco
                            return
                        except app_recovery.DefinitiveRefusal as exc:
                            conta.descartar_ultima_chamada()
                            exc.settled = True
                            raise
                        except iald_motores.ErroProvedor as exc:
                            # 21/09/2026: no claude, recusa ANTES de gerar que certamente não foi cobrada
                            # libera a reserva. ⚠ CORREÇÃO AO LADO (revisão de custo/wire): era "status ≠
                            # 502" — agora a lista de iald_motor_claude.recusa_sem_cobranca (504 e a
                            # conexão caída depois de enviar ficam na reserva; a conexão que nem abriu, 503
                            # claude_conexao, sai). O erro no meio do stream chega como 502 e fica.
                            if claude:
                                sem_cobranca = iald_motor_claude.recusa_sem_cobranca(exc.status, exc.codigo)
                            else:
                                sem_cobranca = exc.status in (400, 401, 403, 404, 413, 422, 429)
                            if not enviou and sem_cobranca:
                                conta.descartar_ultima_chamada()
                            if (tentativa == 1 and not enviou and exc.recusou_esforco()
                                    and "reasoning_effort" in payload):
                                # o modelo não aceita esse nível: tira o parâmetro e tenta uma vez
                                cfg.marcar_esforco_recusado(modelo)
                                payload = {k: v for k, v in payload.items() if k != "reasoning_effort"}
                                print(f"[motores] {modelo} recusou reasoning_effort; seguindo sem ele", flush=True)
                                continue
                            print(f"[motores] {user}: {exc}", flush=True)
                            if not claude:
                                _marcar_sem_credito(exc)      # 15/09/2026: bandeira do saldo (só OpenAI)
                            else:
                                _marcar_sem_credito_claude(exc)   # 22/09/2026: crédito da Anthropic
                            texto = iald_motores.mensagem_ao_usuario(exc)
                        except (iald_motores.CotaEsgotada, iald_orcamento.BudgetError) as exc:
                            # 14/09/2026 (noite): recusa do controle de gasto é "limite" com a cota
                            # (antes saía como falha_motor, sem bloqueado_por)
                            yield from _linhas_da_recusa(exc, user, registro, motor)
                            return
                        except iald_memoria_canonica.MemoryUnavailable as exc:
                            texto = str(exc)
                        except Exception as exc:          # noqa: BLE001 — rede, timeout
                            print(f"[motores] {user}: falha de rede: {iald_motores.mascarar(exc)}", flush=True)
                            texto = iald_motores.mensagem_ao_usuario(exc)
                        yield "data: " + json.dumps({"iald_aviso": {"tipo": "falha_motor", "texto": texto}},
                                                    ensure_ascii=False) + "\n\n"
                        yield "data: " + json.dumps({"choices": [{"delta": {"content": texto},
                                                                  "finish_reason": "stop"}]},
                                                    ensure_ascii=False) + "\n\n"
                        yield "data: [DONE]\n\n"
                        return
                finally:
                    conta.fechar()

        def com_soltura(fluxo):
            try:
                yield from fluxo
            finally:
                for fn in soltar:
                    fn()

        fluxo = gerar()
        if gratuito and MODERACAO_LIGADA:
            fluxo = _moderar_resposta_sse(fluxo, user, cfg_moderacao, authorize=dispatch_check)
        fluxo = com_soltura(fluxo)
        if not gratuito:
            # 14/09/2026 (noite): conta gratuita não gera crédito de uso TGL — a medição criaria a
            # conta no razão com o crédito inicial de 1.000 (ensure_account) na primeira resposta,
            # desfazendo "sem crédito TGL no gratuito" [INPUT: a ratificar]
            # 21/09/2026: a origem da medição é o motor ("openai" | "claude")
            fluxo = _medir_saida_sse(fluxo, user, motor)
        resposta = Response(fluxo, status=200, content_type="text/event-stream",
                            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
        if user == 'luiz':
            resposta.response = APP_EVALUATION.observe(resposta.response,
                {'motor': motor, 'id': modelo}, rates=cfg.precos(modelo),
                memory_sha256=memoria_info.get('context_sha256'),messages=req_json.get('messages'))
            resposta._iald_evaluation_observed = True
        resposta = _identificar_resposta(resposta, {"motor": motor, "id": modelo,
                                    "rotulo": iald_motores.rotulo_do_modelo(modelo)})
        for fn in soltar:
            resposta.call_on_close(fn)
        entregue = True
        return resposta
    finally:
        if not entregue:
            for fn in soltar:
                fn()


NATIVA_MAX_SAIDA = 8192     # o teto que o api_post aplica ao modo pensar do caminho nativo


def _limites_da_conta(motor, registro, plano):
    """Contrato a (14/09/2026, noite): o que esta conta pode usar, para QUALQUER motor.

    {"agente", "pensar", "ferramentas": [nomes] | None (None = todas as da superfície),
     "max_saida", "janela"}. No motor externo: o plano manda e `ferramentas` é a lista
    efetivamente oferecida nesta superfície (a mesma de _chat_openai). Na nativa: tudo o que a
    superfície tem; a janela é a que o servidor já conhece do llama (lida de /props na primeira
    conversa) — esta rota NÃO consulta o llama, para não fixar a janela de reserva se ele estiver
    carregando; /api/contexto continua sendo a fonte da janela nativa.

    14/09/2026 (noite, tarefa SV — contrato novo): "imagens": bool — false no plano gratuito
    (o servidor recusa imagem com o aviso recurso_indisponivel), true nos demais.
    """
    if motor == app_router.AUTO:
        return app_router.limits()
    if motor in app_providers.MODELS:
        return app_providers.limits(motor)
    imagens = plano != iald_motores.GRATUITO
    # 21/09/2026: só a NATIVA tem os limites nativos — um motor externo novo nunca herda "tudo liberado"
    if motor == iald_motores.NATIVA or motor not in iald_motores.EXTERNOS:
        return {"agente": True, "pensar": True, "ferramentas": None, "max_saida": NATIVA_MAX_SAIDA,
                "janela": int(None or HolographicMemory.CONTEXT_WINDOW),
                "imagens": imagens}
    try:
        cfg = _cfg_do_motor(motor, registro)
        lim = iald_motores.limites_do_plano(cfg, plano)
    except (PermissionError, OSError, ValueError, TypeError, KeyError) as exc:
        return {"agente": False, "pensar": False, "ferramentas": [], "max_saida": 0, "janela": 0,
                "imagens": imagens, "erro": f"plano mal configurado ({exc})"}
    if motor == iald_motores.CLAUDE and cfg.modelo == _HAIKU_PROFILE.model:
        try:
            data = _haiku_metadata(_haiku_snapshot(CLAUDE_ROUTES.package()))
            data.update(agente=True, pensar=True, max_saida=cfg.max_saida, imagens=imagens,
                        ferramentas=[t["function"]["name"] for t in _haiku_tool_definitions()])
            return data
        except (ValueError, OSError, KeyError, TypeError, AttributeError):
            return {"agente": False, "pensar": False, "ferramentas": [], "max_saida": 0,
                    "janela": 0, "imagens": imagens, "erro": "Memória ou ferramentas Haiku indisponíveis."}
    superficie = "app" if session.get("app_surface") else "web"
    if motor == iald_motores.CLAUDE:
        # as mesmas ferramentas pagas (o modo de memória é o da casa) e a saída do claude (ver _chat_externo)
        import copy as _copy
        cfg_ferramentas = _copy.copy(cfg)
        cfg_ferramentas.memoria_modo = MOTORES_CFG.memoria_modo
        nomes = [t["function"]["name"] for t in
                 _ferramentas_externas(cfg_ferramentas, lim, superficie, plano == iald_motores.GRATUITO)]
        return {"agente": lim["agente"], "pensar": lim["pensar"], "ferramentas": nomes,
                "max_saida": cfg.max_saida,
                "janela": cfg.janela if cfg.modelo == _HAIKU_PROFILE.model else iald_motores.janela_do_plano(cfg, plano), "imagens": imagens}
    nomes = [t["function"]["name"] for t in
             _ferramentas_externas(MOTORES_CFG, lim, superficie, plano == iald_motores.GRATUITO)]
    return {"agente": lim["agente"], "pensar": lim["pensar"], "ferramentas": nomes,
            "max_saida": min(MOTORES_CFG.max_saida, lim["max_saida"]),
            "janela": iald_motores.janela_do_plano(MOTORES_CFG, plano), "imagens": imagens}



def _check_reserved_dispatch(check,account):
    try:check()
    except Exception:
        # This check is strictly before the transport. Never use it to erase
        # a hold after a request has started or an upstream result is uncertain.
        account.descartar_ultima_chamada()
        raise


def _dispatch_guard(user,executor,automatic):
    def check():
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user):raise PermissionError('Account access revoked')
        if automatic and _motor_do_usuario(user)[0] != app_router.AUTO:
            raise PermissionError('Automatic selection changed before dispatch')
        if automatic and not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Automatic consent revoked')
        provider='claude' if executor.startswith('claude-') else executor
        if provider=='nativa':
            if MODERACAO_LIGADA and not iald_motores.consentiu(current,'openai'):
                raise PermissionError('Moderation consent missing')
        elif not iald_motores.consentiu(current,provider):raise PermissionError('Executor consent revoked')
        if provider in app_providers.MODELS and not app_providers.allowed(current,user,provider):
            raise PermissionError('Executor access revoked')
        if executor=='claude-sonnet' and user!='luiz':raise PermissionError('Operator only')
        return current
    return check


def _opcoes_manuais(registro, usuario):
    return _opcoes_de_motor(registro,usuario) if app_router.manual_allowed(registro,usuario) else []


def _provedores_automaticos(registro, usuario):
    rows=[];seen=set()
    for option in _opcoes_de_motor(registro,usuario):
        key=option['id']
        provider='claude' if key.startswith('claude-') else key
        if provider in (app_router.AUTO,'nativa') or provider in seen:continue
        seen.add(provider)
        rows.append(_consentimento_do_motor(registro,provider))
    return rows


def _nativa_automatica_pronta():
    try:
        # Read only serving metadata; no inference, operator data or API keys.
        return isinstance(native_memory._local_json(LLAMA_URL,'/props'),dict)
    except (ValueError,OSError):return False


def _chat_nativa_automatica(req_json,user,registro,*,routing_instruction=None, science_snapshot=None):
    """Public native context, never the private legacy native-account pipeline."""
    if not app_router.allowed(registro,user) or not iald_motores.consentiu(registro,app_router.AUTO):
        return _sse_aviso('Acesso automático indisponível.','motor_indisponivel')
    try:
        messages=app_providers.wire_messages(req_json.get('messages'),'')
        profile,search_instruction=iald_motores.extrair_do_cliente(req_json.get('messages') or [])
        messages[0]['content']='Responda sob o regime IALD. Preserve os estatutos e use LaTeX com delimitadores próprios.'
        if routing_instruction: messages[0]['content']+='\n'+routing_instruction
        if profile:messages[0]['content']+='\nCONTEXTO DO USUÁRIO:\n'+profile
        if search_instruction:messages[0]['content']+='\n'+iald_motores.LUPA_CANONICA
        payload={'messages':messages,'max_tokens':8192 if req_json.get('iald_mode')=='think' else 4096,
                 'temperature':0.7,'stream':True}
        dispatch_check=_dispatch_guard(user,'nativa',True)
        dispatch_check()
        if MODERACAO_LIGADA:
            decision=iald_motores.moderar_textos([profile]+[m['content'] for m in messages[1:]],
                req_lib.post,MOTORES_CFG.url_base,MOTORES_CFG.chave,cache=_CACHE_MODERACAO)
            if decision.get('bloquear'):return _sse_aviso(iald_motores.MENSAGEM_MODERACAO_BLOQUEIO,'moderacao')
            if not decision.get('ok') and MODERACAO_FALHA=='bloquear':
                return _sse_aviso(MSG_MODERACAO_INDISPONIVEL,'moderacao_indisponivel')
            if decision.get('acolher'):messages[0]['content']+='\n'+iald_motores.INSTRUCAO_ACOLHIMENTO
        payload,definitions,context_check=_prepare_native_payload(payload,'app',native_path='automatic',science_snapshot=science_snapshot)
        science_snapshot = context_check.science_snapshot
        def check(current):
            dispatch_check()
            measured=context_check(current)
            dispatch_check()
            return measured
        definitions=[t for t in definitions if t['function']['name'] in app_providers.TOOL_NAMES]
        def execute(name,args,**kwargs):
            current=load_users_estrito().get(user,{})
            if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
                raise PermissionError('Automatic access revoked')
            if name not in app_providers.TOOL_NAMES:return json.dumps({'status':'UNAVAILABLE'})
            return _science_tool(science_snapshot,_executar_ferramenta_claude,name,args,user=user,operator_authorized=False)
        if not _SEMAFORO_GRATUITO.acquire(blocking=False):
            return _sse_aviso('A IALD está atendendo outras respostas. Tente novamente em instantes.','em_andamento')
        released=False
        def release():
            nonlocal released
            if not released:released=True;_SEMAFORO_GRATUITO.release()
        def generate():
            try:
                yield from agent_loop(payload['messages'],user=user,max_tokens=payload['max_tokens'],
                    ferramentas=definitions,operator_authorized=False,executar=execute,
                    verificar_payload=check,max_voltas=4,responder_na_ultima=True)
            finally:release()
        flow=generate()
        if MODERACAO_LIGADA and iald_motores.plano_de(registro)==iald_motores.GRATUITO:
            flow=_moderar_resposta_sse(flow,user,MOTORES_CFG,authorize=dispatch_check)
        response=Response(flow,content_type='text/event-stream',headers={'Cache-Control':'no-cache','X-Accel-Buffering':'no'})
        response.call_on_close(release)
        return _identificar_resposta(response,_modelo_nativo_resposta())
    except (ValueError,OSError,KeyError,TypeError):
        return _sse_aviso('A memória ou a janela da IALD Nativa não pôde ser validada. Nada foi gerado.','motor_indisponivel')


def _consentimentos_registrados(registro):
    """Os provedores com registro de consentimento NESTA conta, qualquer que seja o motor agora
    (21/09/2026, revisão): o app oferece revogar cada um — antes só o do motor atual aparecia, e o
    da Anthropic ficava sem caminho de revogação quando a conta voltava à nativa ou à OpenAI."""
    saida = []
    for motor in iald_motores.EXTERNOS:
        if isinstance((registro or {}).get(iald_motores.CAMPO_CONSENTIMENTO[motor]), dict):
            saida.append({"motor": motor, "provedor": iald_motores.PROVEDORES[motor],
                          "dado": iald_motores.consentiu(registro, motor)})
    return saida


@app.route("/api/motor", methods=["GET"])
def api_motor():
    """Qual motor responde a esta conta e em que pé está o consentimento.
    21/09/2026 (revisão): `consentimentos` — todo provedor com consentimento registrado."""
    username = session.get("username", "")
    motor, registro = _motor_do_usuario(username)
    plano = iald_motores.plano_de(registro)
    if motor == app_router.AUTO:
        return jsonify(dict(motor=motor,motor_selecao=motor,modelo='jev-1.13.0',rotulo='IALD Automática',
            provedor=app_router.PROVIDER,plano=plano,cota=None,
            classe_usuario='operador' if operator_bench.is_operator(registro,username) else 'usuario',
            provedores_automaticos=_provedores_automaticos(registro,username),
            disponivel=app_router.allowed(registro,username) and app_router.available(),
            pode_escolher=app_router.manual_allowed(registro,username),opcoes=_opcoes_manuais(registro,username),limites=_mimo_media_limits(registro,username,automatic=True),
            consentimento=_consentimento_do_motor(registro,app_router.AUTO),consentimentos=_consentimentos_registrados(registro)))
    if motor in app_providers.MODELS:
        spec = app_providers.MODELS[motor]
        available = app_providers.allowed(registro, username, motor) and not app_providers.availability(motor)
        return jsonify(dict(motor=motor, motor_selecao=motor, modelo=spec['model'], rotulo=spec['label'],
            provedor=spec['provider'], plano=plano, cota=None, disponivel=available,
            pode_escolher=app_router.manual_allowed(registro,username), opcoes=_opcoes_manuais(registro,username),
            limites=(_mimo_media_limits(registro,username) if motor=='mimo' else app_providers.limits(motor)), consentimento=_consentimento_do_motor(registro, motor),
            consentimentos=_consentimentos_registrados(registro)))
    if motor not in iald_motores.EXTERNOS:
        # 14/09/2026 (noite): "plano" e "cota" também aqui; na nativa não há cota da OpenAI
        return jsonify({"motor": motor, "plano": plano, "cota": None,
                        "pode_escolher": app_router.manual_allowed(registro,username),   # 15/09/2026
                        "opcoes": _opcoes_manuais(registro,username),
                        "limites": _limites_da_conta(motor, registro, plano),
                        "consentimento": {"necessario": False},
                        "consentimentos": _consentimentos_registrados(registro)})
    # 21/09/2026: cada motor externo com o SEU provedor, modelo, disponibilidade, cota e consentimento
    try:
        cfg = _cfg_do_motor(motor, registro, username)
    except (PermissionError, ValueError, OSError, KeyError):
        return jsonify({"motor": motor, "motor_selecao": _motor_selection_id(motor, registro, username),
                        "provedor": iald_motores.PROVEDORES[motor], "disponivel": False,
                        "erro": "Memória ou configuração do modelo indisponível.",
                        "pode_escolher": app_router.manual_allowed(registro,username),
                        "opcoes": _opcoes_manuais(registro,username), "plano": plano,
                        "cota": {"erro": "Modelo indisponível."},
                        "limites": {"agente": False, "pensar": False, "max_saida": 0, "janela": 0},
                        "consentimento": _consentimento_do_motor(registro, motor),
                        "consentimentos": _consentimentos_registrados(registro)}), (503 if _haiku_selected(registro, username) else 200)
    modelo = iald_motores.modelo_para(registro, cfg)
    # 14/09/2026 (noite, tarefa SV): o gratuito em atlas_integral não é atendido (ver _chat_openai)
    gratuito_integral = plano == iald_motores.GRATUITO and _memoria_modo_integral(MOTORES_CFG)
    indisponivel = (_motor_externo_indisponivel(modelo, cfg) if motor == iald_motores.CLAUDE
                    else _motor_externo_indisponivel(modelo))
    return jsonify({"motor": motor, "motor_selecao": _motor_selection_id(motor, registro, username), "provedor": iald_motores.PROVEDORES[motor], "modelo": modelo,
                    "rotulo": iald_motores.rotulo_do_modelo(modelo),
                    "pode_escolher": app_router.manual_allowed(registro,username),       # 15/09/2026
                    "opcoes": _opcoes_manuais(registro,username),
                    "disponivel": not gratuito_integral and not indisponivel,
                    "plano": plano,
                    # o que a conta usou e quanto resta (dia e mês UTC), para a folha de uso do app
                    "cota": _estado_da_cota_da_conta(username, registro, motor),
                    "limites": _limites_da_conta(motor, registro, plano),
                    "consentimento": _consentimento_do_motor(registro, motor),
                    "consentimentos": _consentimentos_registrados(registro)})


def _consentimento_do_motor(registro, motor):
    """O bloco `consentimento` de um motor externo: dado, versão, texto e provedor JUNTOS — o app
    mostra este texto e devolve este provedor e esta versão no aceite (21/09/2026, revisão)."""
    return {"necessario": True, "dado": iald_motores.consentiu(registro, motor),
            "versao": iald_motores.versao_do_consentimento(motor),
            "texto": iald_motores.texto_do_consentimento(motor),
            "provedor": iald_motores.PROVEDORES[motor]}


@app.route("/api/motor/consentimento", methods=["POST"])
def api_motor_consentimento():
    """A pessoa aceita (aceito: true) ou revoga (aceito: false) o envio ao provedor do motor da conta.

    21/09/2026: o registro é do provedor do motor EFETIVO (openai → o campo legado; claude → o da
    Anthropic). Conta na nativa → 400 (não há terceiro a consentir). Um aceite nunca vale para o
    outro provedor.

    ⚠ CORREÇÃO AO LADO (21/09/2026, revisão de segurança/regressão): o corpo não dizia QUAL texto a
    pessoa leu — um aceite dado sobre o texto da OpenAI (ou sobre folha vazia, com /api/motor
    falhando depois da troca de modelo) virava consentimento da Anthropic, e a revogação de uma conta
    na nativa passou a dar 400. Agora:
      - {aceito, provedor, versao?}: `provedor` = o nome que a folha mostrou (OpenAI | Anthropic,
        ou openai | claude). Aceite só grava se for o provedor do motor EFETIVO (senão 409, "leia o
        aviso de novo") e, com `versao`, só a versão vigente dele (senão 409);
      - revogação (aceito: false) com `provedor`: remove o registro DAQUELE provedor, qualquer que
        seja o motor agora (inclusive nativa) — a pessoa sempre consegue revogar;
      - sem `provedor` (app antigo, que só conhece a OpenAI): vale como OpenAI, como antes de 21/09 —
        aceite só quando o motor efetivo é o da OpenAI (nunca grava o da Anthropic sem ele ter sido
        nomeado); revogação remove o da OpenAI."""
    username = session.get("username", "")
    # só JSON de verdade: um formulário text/plain de outro site consegue montar um corpo
    # com cara de JSON, mas não consegue mandar application/json sem passar pelo CORS
    if not request.is_json:
        return jsonify({"error": "Envie application/json."}), 415
    dados = _corpo_json() or {}
    if not isinstance(dados.get("aceito"), bool):
        return jsonify({"error": "Informe aceito: true ou false."}), 400
    aceito = dados["aceito"]
    nomeado = dados.get("provedor")
    if nomeado is None:
        alvo = iald_motores.OPENAI                       # app antigo: só conhece a OpenAI
    elif isinstance(nomeado, str) and iald_motores.motor_do_provedor(nomeado) in iald_motores.EXTERNOS \
            and nomeado.strip():
        alvo = iald_motores.motor_do_provedor(nomeado)
    else:
        return jsonify({"error": "Provedor desconhecido. Nada foi alterado."}), 400
    versao_lida = dados.get("versao")
    if versao_lida is not None and (isinstance(versao_lida, bool) or not isinstance(versao_lida, int)):
        return jsonify({"error": "Versão do aviso inválida. Nada foi alterado."}), 400
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()      # ilegível → 503, nada regravado
        conta = usuarios.get(username)
        if not conta:
            return jsonify({"error": "Conta não encontrada."}), 404
        if aceito and _conta_bloqueada(conta):
            return jsonify({'error':'Conta indisponível.'}),403
        motor = _motor_efetivo(conta, username)
        if aceito:
            if alvo == app_router.AUTO and not app_router.allowed(conta, username):
                return jsonify({"error":"Modo automático não liberado para esta conta."}),403
            if alvo in app_providers.MODELS and not app_providers.allowed(conta, username, alvo):
                return jsonify({"error": "Avaliação não liberada para esta conta."}), 403
            if motor not in iald_motores.EXTERNOS:
                return jsonify({"error": "Esta conta responde pela IALD Nativa: não há serviço de terceiros "
                                         "a consentir. Nada foi alterado."}), 400
            if alvo != motor:
                pending=_consentimento_automatico(conta,username) if motor==app_router.AUTO else {}
                pending_motor=iald_motores.motor_do_provedor(pending.get('provedor',''))
                explicit_auto_notice = (motor==app_router.AUTO and nomeado is not None
                    and versao_lida == iald_motores.versao_do_consentimento(alvo)
                    and iald_motores.consentiu(conta,app_router.AUTO)
                    and any(c['provedor']==iald_motores.PROVEDORES[alvo]
                            for c in _provedores_automaticos(conta,username)))
                if not explicit_auto_notice and (pending.get('dado',True) or pending_motor!=alvo):
                    return jsonify({"error": "O modelo desta conta mudou; leia o aviso de novo. Nada foi alterado.",
                                    "motor": motor, "provedor": iald_motores.PROVEDORES[motor]}), 409
            if versao_lida is not None and versao_lida != iald_motores.versao_do_consentimento(alvo):
                return jsonify({"error": "O aviso mudou de versão; leia o aviso de novo. Nada foi alterado.",
                                "motor": motor, "provedor": iald_motores.PROVEDORES[motor]}), 409
        campo = iald_motores.CAMPO_CONSENTIMENTO[alvo]
        if aceito:
            conta[campo] = iald_motores.registro_de_consentimento(
                "app" if session.get("app_surface") else "web", alvo)
        else:
            conta.pop(campo, None)
        save_users(usuarios)
    versao = iald_motores.versao_do_consentimento(alvo)
    auth_log("CONSENTIMENTO_IA", username,
             (f"aceito v{versao}" if aceito else "revogado")
             + ("" if alvo == iald_motores.OPENAI else f" provedor={iald_motores.PROVEDORES[alvo]}"))
    return jsonify({"ok": True, "consentido": aceito, "provedor": iald_motores.PROVEDORES[alvo]})


def _modelo_nativo_resposta():
    model = str(ACTIVE_MODEL_ID)
    label = "IALD Nativa · Qwen3.6-35B" if ("35b" in model.lower() or "qwen3.6" in model.lower()) else "IALD Nativa · " + model
    return {"motor": "nativa", "id": model, "rotulo": label}


def _identificar_resposta(resposta, modelo):
    """Attach server provenance; forward the original SSE bytes and close it on cancel."""
    if resposta.status_code != 200:
        return resposta
    if resposta.mimetype == "text/event-stream":
        if session.get('username') == 'luiz' and not getattr(resposta, '_iald_evaluation_observed', False):
            resposta.response = APP_EVALUATION.observe(resposta.response, modelo, messages=(request.get_json(silent=True) or {}).get('messages'))
        original = resposta.response
        def identified():
            try:
                first = True
                for chunk in original:
                    if first:
                        first = False
                        prefix = "data: " + json.dumps({"iald_modelo": modelo}, ensure_ascii=False) + "\n\n"
                        # Add provenance to the first existing chunk, never advance the
                        # response lifecycle with an extra yield before upstream starts.
                        yield prefix.encode("utf-8") + chunk if isinstance(chunk, bytes) else prefix + chunk
                    else:
                        yield chunk
            finally:
                close = getattr(original, "close", None)
                if close:
                    close()
        resposta.response = identified()
    elif resposta.is_json:
        data = resposta.get_json()
        if isinstance(data, dict) and data.get("choices"):
            data["iald_modelo"] = modelo
            resposta.set_data(json.dumps(data, ensure_ascii=False))
    return resposta


def _opcoes_de_motor(registro, usuario=None):
    if not isinstance(registro, dict) or not registro or _conta_bloqueada(registro):
        return []
    modelo_ext = iald_motores.modelo_para(registro, MOTORES_CFG)
    opcoes = []
    if app_router.allowed(registro, usuario):
        opcoes.append(dict(id=app_router.AUTO,rotulo="IALD Automática",provedor=app_router.PROVIDER,
            detalhe="JEV coordena os modelos e as ferramentas",disponivel=app_router.available()))
    if app_router.allowed(registro, usuario):
        opcoes.append({'id':'nativa','rotulo':_modelo_nativo_resposta()['rotulo'],
                       'detalhe':'Servidor da IALD','disponivel':_nativa_automatica_pronta()})
    opcoes.append({"id": "openai", "rotulo": iald_motores.rotulo_do_modelo(modelo_ext),
                   "detalhe": "OpenAI · " + modelo_ext,
                   "disponivel": not _motor_externo_indisponivel(modelo_ext)})
    for offered in CLAUDE_ROUTES.options(registro, usuario):
        if offered["id"] == "claude-haiku" and not _haiku_client_ready():
            continue
        row = dict(offered)
        try:
            cfg = CLAUDE_ROUTES.configuration(dict(registro, modelo_claude=row["modelo"]), usuario)
            motivo = _motor_externo_indisponivel(row["modelo"], cfg)
        except (ValueError, PermissionError, OSError, KeyError):
            motivo = "Não foi possível validar a disponibilidade deste modelo."
        row["disponivel"] = not bool(motivo)
        if motivo:
            row["motivo"] = motivo
            row["detalhe"] = row.get("detalhe", "") + " · " + motivo
        opcoes.append(row)
    opcoes.extend(app_providers.options(registro, usuario))
    return opcoes


MSG_SEM_ACESSO_NATIVA = ("Esta conta responde pelo ChatGPT. O acesso à IALD Nativa é liberado "
                         "pelo operador da IALD.")
MSG_CLAUDE_SO_NA_LISTA = "O Claude está liberado só para as contas que o operador da IALD indicou."


@app.route("/api/motor/escolha", methods=["POST"])
def api_motor_escolha():
    username = session.get("username", "")
    if not request.is_json:
        return jsonify({"error": "Envie application/json."}), 415
    option = str((_corpo_json() or {}).get("motor") or "").strip().lower()
    if option not in ("nativa", "openai", "claude", "claude-haiku", "claude-sonnet", app_router.AUTO, *app_providers.MODELS):
        return jsonify({"error": "Modelo inválido."}), 400
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        conta = usuarios.get(username)
        if not conta or _conta_bloqueada(conta):
            return jsonify({"error": "Conta indisponível."}), 403
        if option not in ('',app_router.AUTO) and not app_router.manual_allowed(conta, username):
            return jsonify({'error':'Esta conta usa a seleção automática da IALD.','motor':app_router.AUTO}),403
        if option == app_router.AUTO and not app_router.allowed(conta, username):
            return jsonify({"error":"Modo automático não liberado para esta conta."}),403
        if option in app_providers.MODELS and not app_providers.allowed(conta, username, option):
            return jsonify({"error": "Modelo não liberado para esta conta."}), 403
        if option.startswith("claude"):
            try:
                fields = CLAUDE_ROUTES.select(option, conta, username)
                # Validate the selected profile, including its configured price.
                cfg = CLAUDE_ROUTES.configuration(dict(conta, **fields), username)
                if fields.get("modelo_claude") == _HAIKU_PROFILE.model and not _haiku_client_ready():
                    return jsonify({"error": "Atualize o aplicativo para usar o Haiku com memória integral."}), 426
                motivo = _motor_externo_indisponivel(fields["modelo_claude"], cfg)
                if motivo:
                    return jsonify({"error": motivo}), 409
            except (ValueError, PermissionError, OSError, KeyError):
                return jsonify({"error": "Esse modelo não está disponível para esta conta."}), 409
        else:
            if option == "nativa" and not iald_motores.pode_usar_nativa(conta):
                return jsonify({"error": MSG_SEM_ACESSO_NATIVA}), 403
            if option not in {o["id"] for o in _opcoes_de_motor(conta, username) if o["disponivel"]}:
                return jsonify({"error": "Esse modelo está indisponível agora."}), 409
            fields = {"motor": option}
        conta.update(fields)
        conta['motor_escolha_versao']=app_router.DEFAULT_POLICY
        save_users(usuarios)
        motor = _motor_efetivo(conta, username)
        consentimento = (_consentimento_do_motor(conta, motor) if motor in iald_motores.EXTERNOS
                         else {"necessario": False})
        selection = _motor_selection_id(motor, conta, username)
    auth_log("MOTOR_ESCOLHA", username, "motor=" + selection)
    return jsonify({"ok": True, "motor": motor, "motor_selecao": selection,
                    "consentimento_dado": consentimento.get("dado", False), "consentimento": consentimento})


# ── DENÚNCIA DE RESPOSTA (14/09/2026, noite) ──
# Chatbot de IA aberto ao público precisa de denúncia DENTRO do app [LEGAL — Google Play;
# ECA Digital; conferir com advogado]. A regra do arquivo mora em iald_denuncias.py; a
# denúncia chega à aba Acesso do painel. Só JSON de verdade (CSRF, como no consentimento).
import iald_denuncias  # noqa: E402

# 14/09/2026 (noite) — revisão de segurança, MÉDIO 3: teto diário de TODAS as contas e tamanho
# máximo do arquivo; passou de um deles, a denúncia é recusada com 503 claro. [INPUT: a ratificar]
# 14/09/2026 (noite) — tarefa SV (revisão adversarial item 6): também o teto diário POR CONTA
# (IALD_DENUNCIAS_CONTA_DIA, padrão 20), contado no arquivo, além do por hora; passou → 429. E o
# texto com caractere de controle (menos \n e \t) é recusado com 400 (iald_denuncias.validar).
# RISCO RESIDUAL [DERIVED]: o teto global ainda fecha o canal para todos se muitas contas
# denunciarem no mesmo dia (500 ÷ 20 = 25 contas; a 3 contas novas por IP em 24 h, ≈ 9 IPs).
DENUNCIAS = iald_denuncias.Denuncias(
    os.path.join(SERVE_DIR, "iald_denuncias.json"),
    teto_dia_global=_inteiro_de_config("IALD_DENUNCIAS_DIA_GLOBAL", 500, 1),
    teto_bytes=_inteiro_de_config("IALD_DENUNCIAS_MAX_MB", 20, 1) * 1024 * 1024,
    teto_conta_dia=_inteiro_de_config("IALD_DENUNCIAS_CONTA_DIA", 20, 1))
MSG_DENUNCIAS_TETO_DIA = ("O canal de denúncias atingiu o limite de hoje. O operador foi avisado; "
                          "tente de novo amanhã.")
MSG_DENUNCIAS_TETO_ARQUIVO = ("O registro de denúncias está cheio e aguarda o operador. "
                              "Tente de novo mais tarde.")
MSG_DENUNCIAS_TETO_CONTA = "Você atingiu o limite de denúncias de hoje. Tente de novo amanhã."
DENUNCIAS_POR_HORA = _inteiro_de_config("IALD_DENUNCIAS_POR_HORA", 10, 1)
LIMITE_DENUNCIA = iald_motores.JanelaDePedidos(DENUNCIAS_POR_HORA, 3600.0)


@app.route("/api/denuncia", methods=["POST"])
def api_denuncia():
    """A pessoa denuncia uma resposta: {motivo, detalhe?, resposta, pergunta?}."""
    username = session.get("username", "")
    if not request.is_json:
        return jsonify({"error": "Envie application/json."}), 415
    ok, erro, campos = iald_denuncias.validar(request.get_json(silent=True))
    if not ok:
        return jsonify({"error": erro}), 400
    if not LIMITE_DENUNCIA.permitir(username or "?"):
        return jsonify({"error": "Muitas denúncias em pouco tempo. Tente de novo mais tarde."}), 429
    motor, registro = _motor_do_usuario(username)
    # 21/09/2026: o modelo do provedor do motor externo (openai ou claude); na nativa, o do llama
    modelo = (iald_motores.modelo_para(registro, _cfg_do_motor(motor, registro)) if motor in iald_motores.EXTERNOS
              else ACTIVE_MODEL_ID)
    try:
        nova = DENUNCIAS.registrar(username, campos["motivo"], campos["detalhe"], campos["resposta"],
                                   campos["pergunta"], superficie="app" if session.get("app_surface") else "web",
                                   motor=motor, modelo=modelo)
    except iald_denuncias.RegistroCheio as exc:
        print(f"[denuncia] AVISO: registro recusou por teto ({exc.motivo}: {exc})", flush=True)
        if exc.motivo == getattr(iald_denuncias, "MOTIVO_TETO_CONTA", "conta"):
            # 14/09/2026 (noite, tarefa SV): teto da própria conta — 429, o canal segue aberto aos outros
            return jsonify({"error": MSG_DENUNCIAS_TETO_CONTA, "teto": exc.motivo}), 429
        msg = MSG_DENUNCIAS_TETO_DIA if exc.motivo == iald_denuncias.MOTIVO_TETO_DIA else MSG_DENUNCIAS_TETO_ARQUIVO
        return jsonify({"error": msg, "teto": exc.motivo}), 503
    except Exception as exc:          # noqa: BLE001 — falha visível, nunca "recebida" falso
        print(f"[denuncia] registro indisponível ({type(exc).__name__}: {exc})", flush=True)
        return jsonify({"error": "O registro de denúncias está indisponível agora. Tente de novo mais tarde."}), 503
    auth_log("DENUNCIA_RECEBIDA", username, f"id={nova['id']} motivo={nova['motivo']}")
    return jsonify({"ok": True, "id": nova["id"],
                    "mensagem": "Denúncia recebida. O operador da IALD vai analisar esta resposta."}), 201


# ── páginas ──
_SVG_APPLE = ('<svg viewBox="0 0 16 16" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434C9.583 3.81 8.716 4.5 8.5 4.5c-.216 0-1.155-.667-2.11-.647-.618.012-1.22.19-1.755.53C3.6 4.926 2.5 6.02 2.5 8.5c0 2.48 1.8 5.5 2.8 5.5.5 0 1.2-.5 2-.5s1.3.5 2 .5c1.2 0 2.5-2.5 2.5-2.5-.9-.4-1.3-1.3-1.3-1.3z"/></svg>')
_SVG_GOOGLE = ('<svg viewBox="0 0 48 48" width="18" height="18" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>')


def _pagina_entrada(mensagem="", tipo=""):
    """A MESMA entrada do app, para o site: Apple, Google, usuário e senha."""
    cfg = _provedores_configurados()
    # 14/09/2026 (noite): a nota acompanha o estado da porta (era fixa: "liberado pelo operador")
    nota = _html.escape(NOTA_ENTRADA_ABERTA if _estado_entrada()[0] else NOTA_ENTRADA_FECHADA)
    beta = f"{_BETA_TGL:.18f}".rstrip("0")
    aviso = ""
    if mensagem:
        cor = {"pendente": "pendente", "erro": "erro"}.get(tipo, "info")
        aviso = f'<div class="aviso {cor}">{_html.escape(mensagem)}</div>'
    botoes = ""
    if cfg["apple_web"]:
        botoes += f'<a class="btn btn-apple" href="/auth/apple/iniciar?origem=web">{_SVG_APPLE}<span>Entrar com a Apple</span></a>'
    if cfg["google"]:
        botoes += f'<a class="btn btn-google" href="/auth/google/iniciar?origem=web">{_SVG_GOOGLE}<span>Entrar com o Google</span></a>'
    separador = '<div class="ou"><span>ou</span></div>' if botoes else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0E1F33"><title>IALD — Entrar</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{min-height:100%}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#fff;
background:radial-gradient(58% 34% at 50% 30%,rgba(138,180,216,.16),transparent 72%),linear-gradient(160deg,#0E1F33 0%,#1B3A5C 56%,#152E4A 100%);
background-attachment:fixed;display:flex;flex-direction:column;align-items:center;padding:24px 20px;-webkit-font-smoothing:antialiased}}
main{{flex:1;width:min(24rem,100%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.marca{{width:min(62vw,240px);height:auto;margin:-10% 0 -12%}}
.sub{{font-size:19px;font-weight:300;line-height:1.35;color:rgba(255,255,255,.86);margin-bottom:24px}}
.cartao{{width:100%;display:flex;flex-direction:column;gap:12px;padding:22px 20px 18px;background:rgba(255,255,255,.09);
border:1px solid rgba(255,255,255,.14);border-radius:22px;box-shadow:0 24px 60px rgba(0,0,0,.32);backdrop-filter:blur(18px)}}
.btn{{display:flex;align-items:center;justify-content:center;gap:9px;min-height:50px;border-radius:12px;font-size:17px;font-weight:600;text-decoration:none}}
.btn-apple{{background:#fff;color:#000}}
.btn-google{{background:#fff;color:#1F1F1F;border:1px solid #DADCE0}}
.btn-apple svg{{margin-top:-3px}}
.ou{{display:flex;align-items:center;gap:10px;color:rgba(255,255,255,.5);font-size:13px}}
.ou::before,.ou::after{{content:"";flex:1;height:1px;background:rgba(255,255,255,.18)}}
form{{display:flex;flex-direction:column;gap:10px;text-align:left}}
label{{font-size:13px;color:rgba(255,255,255,.75)}}
input{{width:100%;min-height:46px;padding:0 14px;font-size:16px;border-radius:12px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.95);color:#1c1f24;outline:none}}
input:focus{{border-color:#C5961A;box-shadow:0 0 0 3px rgba(197,150,26,.25)}}
.btn-senha{{min-height:50px;border:none;border-radius:12px;font-size:17px;font-weight:600;color:#fff;cursor:pointer;background:linear-gradient(180deg,#CDA22C 0%,#C5961A 100%)}}
.aviso{{width:100%;margin-bottom:14px;padding:11px 14px;border-radius:12px;font-size:14px;line-height:1.45;text-align:left}}
.aviso.pendente{{background:rgba(197,150,26,.18);border:1px solid rgba(242,217,138,.45);color:#FBEFC9}}
.aviso.erro{{background:rgba(214,69,69,.2);border:1px solid rgba(255,130,130,.45);color:#FFE1E1}}
.aviso.info{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}}
.nota{{margin-top:6px;font-size:12.5px;line-height:1.5;color:rgba(255,255,255,.6)}}
.link{{margin-top:16px;font-size:14px;color:#F2D98A}}
footer{{margin-top:18px;display:flex;flex-direction:column;gap:4px;align-items:center;font-size:12.5px;color:rgba(255,255,255,.5)}}
.beta{{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;color:#D4AF37}}
</style></head><body>
<main>
<img class="marca" src="/app/img/iald_logo_dark_transparent_final.png" alt="IALD" width="1024" height="1024">
<p class="sub">Inteligência Artificial<br>Luminodinâmica</p>
{aviso}
<div class="cartao">
{botoes}
{separador}
<form method="POST" action="/login" autocomplete="on">
<label for="username">Usuário</label><input id="username" name="username" autocomplete="username" autocapitalize="none" required>
<label for="password">Senha</label><input id="password" name="password" type="password" autocomplete="current-password" required>
<button class="btn-senha" type="submit">Entrar</button>
</form>
<p class="nota">{nota}</p>
</div>
<a class="link" href="https://iald.ia.br/privacidade.html" target="_blank" rel="noopener noreferrer">Política de privacidade</a>
</main>
<footer><div class="beta">β_TGL = α × √e = {beta}</div><div>IALD LTDA · iald.ia.br</div></footer>
</body></html>"""


def _pagina_volta_app(link):
    """Devolve o controle ao app instalado (navegador do sistema → br.ia.iald://)."""
    seguro = _html.escape(link, quote=True)
    js = json.dumps(link)
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>IALD — voltando ao app</title>
<style>body{{margin:0;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#fff;background:linear-gradient(160deg,#0E1F33,#1B3A5C 56%,#152E4A);text-align:center;padding:24px}}
a{{display:inline-block;padding:14px 26px;border-radius:12px;background:#fff;color:#1B3A5C;font-weight:600;text-decoration:none;font-size:17px}}
p{{color:rgba(255,255,255,.8);font-size:15px}}</style></head><body>
<p>Entrada confirmada. Voltando ao aplicativo…</p>
<a href="{seguro}">Voltar ao app IALD</a>
<script>setTimeout(function(){{location.replace({js});}},150);</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════
# ADMIN API — Access Requests (v3.1)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/access-requests", methods=["GET"])
def admin_list_access_requests():
    check = require_admin()
    if check:
        return check
    if not ACCESS_AVAILABLE:
        return jsonify([])
    return jsonify(access_engine.list_all())


@app.route("/admin/api/access-requests/<req_id>/approve", methods=["POST"])
def admin_approve_access(req_id):
    check = require_admin()
    if check:
        return check
    if not ACCESS_AVAILABLE:
        return jsonify({"error": "Access engine indisponível"}), 503

    # Optional: link to existing username
    existing_username = ""
    if request.data:
        try:
            existing_username = request.get_json(force=True).get("existing_username", "")
        except Exception:
            pass

    global USERS
    with _TRAVA_USUARIOS:      # 14/09/2026 (noite): leitura para escrita e gravação sob a trava
        USERS_CURRENT = _carregar_usuarios_para_escrita()
        ok, result = access_engine.approve(
            req_id=req_id,
            users_dict=USERS_CURRENT,
            save_users_fn=save_users,
            coin_engine=coin_engine if COIN_AVAILABLE else None,
            admin_user=session.get("username", "admin"),
            existing_username=existing_username
        )
    if ok:
        USERS = load_users()
        auth_log("ACCESS_APPROVED", session.get("username", "admin"),
                 f"req={req_id} user={result.get('username','')} linked={result.get('linked',False)}")
    return jsonify(result), 200 if ok else 404


@app.route("/admin/api/access-requests/<req_id>/reject", methods=["POST"])
def admin_reject_access(req_id):
    check = require_admin()
    if check:
        return check
    if not ACCESS_AVAILABLE:
        return jsonify({"error": "Access engine indisponível"}), 503

    notes = ""
    if request.data:
        try:
            notes = request.get_json(force=True).get("notes", "")
        except Exception:
            pass

    ok, result = access_engine.reject(
        req_id=req_id, notes=notes,
        admin_user=session.get("username", "admin")
    )
    auth_log("ACCESS_REJECTED", session.get("username", "admin"), f"req={req_id}")
    return jsonify(result), 200 if ok else 404


@app.route("/admin/api/access-requests/<req_id>", methods=["DELETE"])
def admin_delete_access(req_id):
    check = require_admin()
    if check:
        return check
    if not ACCESS_AVAILABLE:
        return jsonify({"error": "Access engine indisponível"}), 503

    if access_engine.delete_request(req_id):
        auth_log("ACCESS_DELETED", session.get("username", "admin"), f"req={req_id}")
        return jsonify({"status": "deleted", "id": req_id})
    return jsonify({"error": "Pedido não encontrado"}), 404


# ══════════════════════════════════════════════════════════════
# PAINEL — LIBERAÇÃO DE ACESSO (14/09/2026)
#
# Só no computador (require_admin exige requisição local + sessão de admin).
# Aprovar = criar usuário novo com a identidade, OU vincular a identidade a um
# usuário que já existe — é o "vincular" que impede a mesma pessoa de virar duas
# contas quando entra por Apple e por Google.
# ══════════════════════════════════════════════════════════════

# 14/09/2026 (noite, tarefa SV): textos da lápide no painel (revisão adversarial item 9)
MSG_NOME_RETIRADO = ("O nome '{nome}' pertenceu a uma conta excluída e não pode ser reutilizado: o crédito TGL "
                     "e o Ψ-NET são guardados por nome e iriam para a conta nova. Escolha outro nome.")
MSG_LAPIDE_ILEGIVEL = ("A lista de nomes retirados não pôde ser lida; nada foi alterado. Confira o arquivo "
                       "de nomes retirados e tente de novo.")
# 21/09/2026 (aba "Usuários (app IALD)" da Central de Patentes): textos da aprovação pela Central, que só
# cria a conta com o nome que a Central MOSTROU (a sugestão do último retrato aceito). Nome tomado ou
# retirado no meio do caminho → falha clara; a sincronização seguinte leva a sugestão nova.
MSG_CENTRAL_NOME_TOMADO = ("O nome '{nome}' já está em uso na IALD. Aguarde a próxima sincronização (a aba mostra "
                           "a sugestão nova) e aprove de novo.")
MSG_CENTRAL_NOME_RETIRADO = ("O nome '{nome}' pertenceu a uma conta excluída e não pode ser reutilizado. Aguarde a "
                             "próxima sincronização e aprove de novo.")


def _exige_json():
    """21/09/2026 — endurecimento da revisão da aba da Central (3.md §3.7): as escritas do painel que a
    Central espelha (aprovar, recusar, bloquear/desbloquear) só aceitam application/json. O painel já
    manda JSON em todas as chamadas (conferido no JS); corpo vazio, formulário ou texto — o que um site
    de fora consegue mandar sem preflight — não decide mais nada (antes, aprovar sem corpo aprovava
    com os padrões)."""
    return jsonify({"error": "Envie application/json."}), 415


@app.route("/admin/api/pedidos", methods=["GET"])
def admin_pedidos_listar():
    check = require_admin()
    if check:
        return check
    usuarios = load_users_estrito()    # ilegível → 503 (não "ninguém é dono de nada")
    # 14/09/2026 (noite, tarefa SV — revisão adversarial item 9): a sugestão respeita a lápide dos
    # nomes retirados (antes sugeria "maria" para outra pessoa depois de a conta "maria" ser excluída)
    try:
        lapide = PEDIDOS.nomes_indisponiveis()
    except (OSError, ValueError) as exc:
        print(f"[painel] lápide de nomes ilegível ({exc}); pedidos não listados", flush=True)
        return jsonify({"error": MSG_LAPIDE_ILEGIVEL}), 503
    saida = []
    for p in PEDIDOS.listar():
        item = dict(p)
        item["dono_atual"] = identidade.usuario_da_identidade(usuarios, p.get("provedor", ""), p.get("sub", ""))
        item["sugestao"] = identidade.sugerir_username(usuarios, p.get("email", ""), p.get("nome", ""),
                                                       indisponiveis=lapide)
        saida.append(item)
    return jsonify({"pedidos": saida, "contagem": PEDIDOS.contagem(),
                    "configurado": _provedores_configurados()})


def _aprovar_pedido(pid, modo, nome, ampliar, operador, via_central=False, plano_central=None):
    """Corpo da liberação de um pedido — o MESMO para o painel e para a Central (21/09/2026).

    Extraído de admin_pedidos_aprovar para a sincronização com a Central de Patentes executar pelo
    MESMO caminho, sob as MESMAS travas. Não usa request nem session: roda também na thread da
    sincronização. Devolve (corpo, status_http, info) — o painel responde jsonify(corpo), status,
    exatamente como antes.

    via_central=True (a aba da Central): só pedido PENDENTE (conferido de novo sob as travas); só conta
    NOVA com o nome dado — a sugestão que a Central mostrou —, nunca 'vincular', nunca identidade que
    já tem dono, nunca nome reservado, tomado ou retirado, nunca admin, nunca acesso ampliado; plano =
    `plano_central`, o FIXADO pelo operador (IALD_CENTRAL_SYNC_PLANO: gratuito ou assinante).

    REVISÃO ADVERSARIAL (21/09/2026):
      • as DUAS travas — _TRAVA_USUARIOS e depois a do PEDIDOS (a mesma ordem da porta aberta) — ficam
        presas da conferência do pedido até a marca 'aprovado'. Antes a marca vinha DEPOIS de soltar a
        trava e sem conferir o status: uma recusa do painel no meio virava aprovação em silêncio;
      • na Central, depois que save_users gravou a conta, NADA levanta: a marca do pedido tenta de novo
        uma vez e, se ainda falhar, a resposta é 200 com info["aviso"] (conta criada, pedido não
        marcado). Antes a falha subia e o executor dizia "nada foi alterado" (transitório) — e a
        entrega seguinte recusava a conta que já existia;
      • o plano para o crédito TGL sai do registro em memória (o que acabou de ser gravado), não de uma
        nova leitura do arquivo que podia falhar depois da gravação.
    """
    pedido = PEDIDOS.obter(pid)
    if not pedido:
        return {"error": "Pedido não encontrado"}, 404, None
    aceitos = (identidade.PENDENTE,) if via_central else (identidade.PENDENTE, identidade.RECUSADO)
    if pedido.get("status") not in aceitos:
        return {"error": f"Pedido já está '{pedido.get('status')}'"}, 409, None
    provedor, sub = pedido.get("provedor", ""), pedido.get("sub", "")
    info = {"provedor": provedor, "plano": ""}
    with _TRAVA_USUARIOS, PEDIDOS._trava:
        usuarios = _carregar_usuarios_para_escrita()
        dono = identidade.usuario_da_identidade(usuarios, provedor, sub)
        if via_central:
            atual = PEDIDOS.obter(pid)      # de novo, sob as DUAS travas: nada decide este pedido no meio
            if not atual or atual.get("status") != identidade.PENDENTE:
                return {"error": f"Pedido já está '{(atual or {}).get('status', 'ausente')}'"}, 409, None
            if dono:
                return {"error": f"A identidade deste pedido já pertence à conta '{dono}'. "
                                 "Decida pelo painel local."}, 409, None
        if dono:
            nome = dono              # já vinculada (ex.: o operador vinculou pela aba Usuários)
        elif modo == "vincular":
            if nome not in usuarios:
                return {"error": f"Usuário '{nome}' não existe"}, 404, None
            ok, erro = identidade.vincular(usuarios, nome, provedor, sub, pedido.get("email", ""))
            if not ok:
                return {"error": erro}, 409, None
            if ampliar and iald_motores.plano_de(usuarios[nome]) != iald_motores.GRATUITO:
                usuarios[nome]["acesso_nativa"] = True
            save_users(usuarios)
        else:
            # 14/09/2026 (noite, tarefa SV — revisão adversarial item 9): a lápide vale aqui também.
            # Antes, aprovar com a sugestão padrão criava "maria" depois da exclusão de "maria", e a
            # conta nova herdava o razão TGLC e o Ψ-NET (por nome). Lápide ilegível → 503, nada criado.
            try:
                lapide = PEDIDOS.nomes_indisponiveis()
            except (OSError, ValueError) as exc:
                print(f"[painel] lápide de nomes ilegível ({exc}); nenhuma conta criada", flush=True)
                return {"error": MSG_LAPIDE_ILEGIVEL}, 503, None
            if via_central:
                # 21/09/2026: a Central não escolhe nome — só confirma a sugestão que mostrou
                if not identidade.usuario_valido(nome):
                    return {"error": "Nome sugerido inválido. Aguarde a próxima sincronização e aprove de novo."}, 400, None
                if identidade.usuario_reservado(nome):
                    return {"error": f"O nome '{nome}' é reservado. Libere este pedido pelo painel local."}, 409, None
                if nome in usuarios:
                    return {"error": MSG_CENTRAL_NOME_TOMADO.format(nome=nome)}, 409, None
                if nome in lapide:
                    return {"error": MSG_CENTRAL_NOME_RETIRADO.format(nome=nome), "nome_retirado": True}, 409, None
            else:
                nome = nome or identidade.sugerir_username(usuarios, pedido.get("email", ""), pedido.get("nome", ""),
                                                           indisponiveis=lapide)
                if not identidade.usuario_valido(nome):
                    return {"error": "Nome de usuário inválido: 3 a 32 caracteres, minúsculas, números, '.', '_' ou '-'."}, 400, None
                if nome in usuarios:
                    return {"error": f"Usuário '{nome}' já existe. Para a mesma pessoa, use Vincular."}, 409, None
                if nome in lapide:
                    return {"error": MSG_NOME_RETIRADO.format(nome=nome), "nome_retirado": True}, 409, None
            usuarios[nome] = {
                # senha aleatória que ninguém conhece: esta conta entra pela identidade.
                # O operador pode definir uma senha depois, pelo botão Senha.
                "password_hash": generate_password_hash(secrets.token_urlsafe(32)),
                "admin": False,
                "sacred_language": False,
                "created": datetime.now().isoformat(),
                "name": pedido.get("nome", ""),
                "email": pedido.get("email", ""),
                "source": f"{provedor}_liberado",
                "identidades": [],
            }
            if ampliar:
                # 15/09/2026: conta ampliada nasce fora do gratuito, com acesso à IALD Nativa
                usuarios[nome]["acesso_nativa"] = True
            elif via_central:
                # 21/09/2026 (revisão adversarial): pela Central, o plano é o FIXADO pelo operador —
                # antes, com a porta fechada, a conta nascia "assinante" (e com o crédito TGL inicial)
                # sem ninguém ter escolhido. Gratuito = a mesma conta que a porta daria.
                if plano_central == iald_motores.GRATUITO:
                    try:
                        usuarios[nome].update({"plano": iald_motores.GRATUITO, "motor": iald_motores.OPENAI,
                                               "cota_chave": identidade.chave_cota(_segredo_da_casa(), provedor, sub)})
                    except ValueError as exc:
                        usuarios.pop(nome, None)
                        return {"error": f"Chave de cota indisponível: {exc}"}, 500, None
                elif plano_central == iald_motores.ASSINANTE:
                    usuarios[nome]["plano"] = iald_motores.ASSINANTE
                else:
                    usuarios.pop(nome, None)
                    return {"error": "Plano de aprovação fora da lista da IALD (gratuito ou assinante)."}, 409, None
            elif _estado_entrada()[0]:
                # 14/09/2026 (noite): com a porta aberta, liberar pelo painel (ex.: quem
                # ficou pendente pelo limite de criação) dá a MESMA conta que a porta daria:
                # plano gratuito no motor OpenAI, cota presa à identidade. Sem isto a conta
                # nasceria "assinante" no motor padrão — que hoje é a máquina do operador.
                # Para outro plano, o operador troca na aba Usuários.
                try:
                    usuarios[nome].update({"plano": iald_motores.GRATUITO, "motor": iald_motores.OPENAI,
                                           "cota_chave": identidade.chave_cota(_segredo_da_casa(), provedor, sub)})
                except ValueError as exc:
                    usuarios.pop(nome, None)
                    return {"error": f"Chave de cota indisponível: {exc}"}, 500, None
            ok, erro = identidade.vincular(usuarios, nome, provedor, sub, pedido.get("email", ""))
            if not ok:
                return {"error": erro}, 409, None
            save_users(usuarios)
            info["plano"] = iald_motores.plano_de(usuarios[nome])
        registro = usuarios.get(nome)
        # a marca 'aprovado' AINDA sob as duas travas (21/09/2026 — ver a docstring)
        if via_central:
            if not _central_marcar_aprovado(pid, nome, operador):
                info["aviso"] = ("conta criada, mas o registro do pedido não gravou na IALD "
                                 "(continua 'pendente') — confira no painel local")
        else:
            PEDIDOS.marcar_aprovado(pid, nome, operador)
    if COIN_AVAILABLE and iald_motores.plano_de(registro) != iald_motores.GRATUITO:
        try:
            coin_engine.ensure_account(nome)
        except Exception as exc:        # noqa: BLE001
            print(f"[painel] ensure_account falhou para {nome}: {exc}", flush=True)
    info["nome"] = nome
    return {"ok": True, "username": nome, "modo": modo}, 200, info


def _central_marcar_aprovado(pid, nome, operador):
    """Marca o pedido 'aprovado' DEPOIS de a conta ter sido gravada (Central; sob as duas travas).
    Nunca levanta: tenta duas vezes (o antivírus do Windows às vezes segura o arquivo no os.replace)
    e devolve False se não conseguiu — a conta já existe, então o resultado é FINAL, com aviso."""
    for tentativa in range(2):
        try:
            if PEDIDOS.marcar_aprovado(pid, nome, operador):
                return True
        except Exception as exc:  # noqa: BLE001 — depois da gravação da conta nada pode subir
            try:
                print(f"[central-sync] pedido {pid}: marca 'aprovado' falhou ({type(exc).__name__}), "
                      f"tentativa {tentativa + 1}/2", flush=True)
            except Exception:  # noqa: BLE001 — nem o log
                pass
        if tentativa == 0:
            time.sleep(0.05)
    return False


@app.route("/admin/api/pedidos/<pid>/aprovar", methods=["POST"])
def admin_pedidos_aprovar(pid):
    check = require_admin()
    if check:
        return check
    if not request.is_json:              # 21/09/2026: só JSON (ver _exige_json)
        return _exige_json()
    dados = request.get_json(silent=True) or {}
    modo = "vincular" if dados.get("modo") == "vincular" else "novo"
    # 15/09/2026: o operador decide ao liberar se amplia a conta para a IALD Nativa
    ampliar = dados.get("acesso_nativa") is True
    nome = str(dados.get("username") or "").strip().lower()
    operador = session.get("username", "admin")
    # 21/09/2026: o corpo virou _aprovar_pedido (o mesmo caminho da Central, sob as mesmas travas)
    corpo, status, info = _aprovar_pedido(pid, modo, nome, ampliar, operador)
    if status == 200:
        auth_log("ACESSO_LIBERADO", operador, f"pedido={pid} usuario={corpo['username']} modo={modo} "
                                              f"via={info['provedor']} "
                                              f"acesso={'nativa+chatgpt' if ampliar else 'chatgpt'}")
    return jsonify(corpo), status


def _recusar_pedido(pid, nota, operador, via_central=False):
    """Corpo da recusa — o MESMO para o painel e para a Central (21/09/2026). (corpo, status_http).
    Sem request/session.

    REVISÃO ADVERSARIAL (21/09/2026): sob _TRAVA_USUARIOS e depois a trava do PEDIDOS (a ordem da
    porta aberta e da aprovação), a leitura do status e a marca 'recusado' são UM passo só — antes
    PedidosAcesso.recusar lia e gravava em duas seções, e uma aprovação (Central, painel ou porta
    aberta) no meio fazia o painel dizer "recusado" de um pedido aprovado, ou recusar um pedido cuja
    conta acabara de nascer. via_central=True: identidade de conta de administrador é protegida,
    conferida DENTRO das travas."""
    with _TRAVA_USUARIOS, PEDIDOS._trava:
        atual = PEDIDOS.obter(pid)
        if not atual or atual.get("status") != identidade.PENDENTE:
            return {"error": "Pedido não encontrado ou não está pendente"}, 404
        if via_central:
            usuarios = load_users_estrito()
            dono = identidade.usuario_da_identidade(usuarios, atual.get("provedor", ""), atual.get("sub", ""))
            if dono and (usuarios.get(dono) or {}).get("admin"):
                return {"error": "A identidade deste pedido é de uma conta protegida (administrador). "
                                 "Decida pelo painel local."}, 409
        p = PEDIDOS.recusar(pid, operador, nota)
    if not p:
        return {"error": "Pedido não encontrado ou não está pendente"}, 404
    return {"ok": True}, 200


@app.route("/admin/api/pedidos/<pid>/recusar", methods=["POST"])
def admin_pedidos_recusar(pid):
    check = require_admin()
    if check:
        return check
    if not request.is_json:              # 21/09/2026: só JSON (ver _exige_json)
        return _exige_json()
    nota = str((request.get_json(silent=True) or {}).get("nota") or "")[:200]
    operador = session.get("username", "admin")
    corpo, status = _recusar_pedido(pid, nota, operador)
    if status == 200:
        auth_log("ACESSO_RECUSADO", operador, f"pedido={pid}")
    return jsonify(corpo), status


@app.route("/admin/api/pedidos/<pid>/reabrir", methods=["POST"])
def admin_pedidos_reabrir(pid):
    check = require_admin()
    if check:
        return check
    p = PEDIDOS.reabrir(pid, session.get("username", "admin"))
    if not p:
        return jsonify({"error": "Pedido não encontrado ou não está recusado"}), 404
    return jsonify({"ok": True})


@app.route("/admin/api/pedidos/<pid>", methods=["DELETE"])
def admin_pedidos_excluir(pid):
    check = require_admin()
    if check:
        return check
    if not PEDIDOS.excluir(pid):
        return jsonify({"error": "Pedido não encontrado"}), 404
    auth_log("PEDIDO_APAGADO", session.get("username", "admin"), f"pedido={pid}")
    return jsonify({"ok": True})


@app.route("/admin/api/users/<username>/identidades/remover", methods=["POST"])
def admin_identidade_remover(username):
    check = require_admin()
    if check:
        return check
    dados = request.get_json(silent=True) or {}
    provedor, sub = str(dados.get("provedor") or ""), str(dados.get("sub") or "")
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        ok, erro = identidade.desvincular(usuarios, username, provedor, sub)
        if not ok:
            return jsonify({"error": erro}), 404
        save_users(usuarios)
    PEDIDOS.encerrar_do_usuario("", [{"provedor": provedor, "sub": sub}])
    auth_log("IDENTIDADE_REMOVIDA", session.get("username", "admin"), f"usuario={username} via={provedor}")
    return jsonify({"ok": True})


@app.route("/admin/api/users/<username>/identidades/mover", methods=["POST"])
def admin_identidade_mover(username):
    check = require_admin()
    if check:
        return check
    dados = request.get_json(silent=True) or {}
    provedor, sub = str(dados.get("provedor") or ""), str(dados.get("sub") or "")
    destino = str(dados.get("destino") or "").strip().lower()
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        ok, erro = identidade.mover_identidade(usuarios, username, destino, provedor, sub)
        if not ok:
            return jsonify({"error": erro}), 409
        save_users(usuarios)
    auth_log("IDENTIDADE_MOVIDA", session.get("username", "admin"), f"{username} -> {destino} via={provedor}")
    return jsonify({"ok": True, "destino": destino})


# ══════════════════════════════════════════════════════════════
# TGL COIN REST — Para o app iOS (v3.1, autenticado)
# ══════════════════════════════════════════════════════════════

@app.route("/api/active-model")
def api_active_model():
    """Modelo ativo p/ o badge do chat. Público: só nome/estado, nada sensível."""
    # 14/09/2026: conta no motor externo vê o motor DELA — o selo "TGL Nativa" do app
    # só acende quando o id contém iald_nativa, então aqui ele se apaga sozinho.
    try:
        conta = session.get("username") or _usuario_do_token()
    except Exception:             # noqa: BLE001 — rota pública nunca cai por isto
        conta = ""
    if conta:
        motor, registro = _motor_do_usuario(conta)
        if motor == app_router.AUTO:
            return jsonify(dict(id='automatico:jev',short='IALD Automática',label='JEV seleciona o executor',
                motor=motor,online=app_router.allowed(registro,conta) and app_router.available(),
                n_ctx=1048576,vision=False,consentimento_dado=iald_motores.consentiu(registro,motor)))
        if motor in app_providers.MODELS:
            spec = app_providers.MODELS[motor]
            available = app_providers.allowed(registro, conta, motor) and not app_providers.availability(motor)
            return jsonify({'id': motor+':'+spec['model'], 'short': 'IALD · '+spec['label'],
                'label': spec['provider'], 'motor': motor, 'online': available,
                'n_ctx': app_providers.WINDOW, 'vision': False,
                'consentimento_dado': iald_motores.consentiu(registro, motor)})

        if motor == iald_motores.CLAUDE:
            # 21/09/2026: o motor claude — nunca o badge nem o /props do llama
            try:
                active_cfg = CLAUDE_ROUTES.configuration(registro, conta)
            except (PermissionError, ValueError, OSError, KeyError):
                return jsonify({"id": "claude:unavailable", "short": "IALD · Claude indisponível",
                                "motor": motor, "online": False, "n_ctx": 0})
            modelo = iald_motores.modelo_para(registro, active_cfg)
            return jsonify({"id": f"claude:{modelo}", "short": f"IALD · {iald_motores.rotulo_do_modelo(modelo)}",
                            "label": "servida pela API da Anthropic", "motor": motor,
                            "online": not _motor_externo_indisponivel(modelo, active_cfg),
                            "n_ctx": active_cfg.janela,
                            "vision": True,
                            "consentimento_dado": iald_motores.consentiu(registro, iald_motores.CLAUDE)})
        if motor == iald_motores.OPENAI:
            modelo = iald_motores.modelo_para(registro, MOTORES_CFG)
            return jsonify({"id": f"openai:{modelo}", "short": f"IALD · OpenAI {modelo}",
                            "label": "servida pela API da OpenAI", "motor": motor,
                            "online": not _motor_externo_indisponivel(modelo),
                            # 14/09/2026 (noite, C1 da revisão de interface): no gratuito, a janela
                            # do plano (min(configurada, 32768)), a mesma que _chat_openai usa
                            "n_ctx": iald_motores.janela_do_plano(MOTORES_CFG, iald_motores.plano_de(registro)),
                            "vision": True,
                            "consentimento_dado": iald_motores.consentiu(registro)})
    info = MODELS.get(ACTIVE_MODEL_ID, {})
    short = {
        "iald_nativa_v2_35b": "IALD v2 · Qwen3.6-35B",
        "iald_nativa_v1_32b": "IALD v1 · 32B",
        "iald_nativa_v1": "IALD v1 · 14B",
        "stack_v3_complete": "Stack v3 · 32B",
        "mark_4": "Mark 4 · 122B",
    }.get(ACTIVE_MODEL_ID, ACTIVE_MODEL_ID)
    online, n_ctx, vision = False, None, False
    try:
        r = req_lib.get(f"{get_llama_url()}/props", timeout=2)
        if r.status_code == 200:
            online = True
            props = r.json()
            n_ctx = props.get("default_generation_settings", {}).get("n_ctx")
            vision = bool((props.get("modalities") or {}).get("vision"))
    except Exception:
        pass
    return jsonify({"id": ACTIVE_MODEL_ID, "short": short,
                    "label": info.get("label", ""), "online": online,
                    "n_ctx": n_ctx, "vision": vision})


# 14/09/2026 (noite) — revisão de segurança (BAIXO 4 e seção 5 da revisão de testes): a extração
# gasta CPU e memória da máquina do operador e não tinha limite por conta. Operador (admin): sem
# limite. Plano gratuito: 20 por hora. Demais contas: 120 por hora. [INPUT: números a ratificar]
TETO_EXTRAIR_BYTES = 25 * 1024 * 1024
LIMITE_EXTRAIR_GRATUITO = iald_motores.JanelaDePedidos(
    _inteiro_de_config("IALD_EXTRAIR_TEXTO_GRATUITO_POR_HORA", 20, 1), 3600.0)
LIMITE_EXTRAIR_CONTA = iald_motores.JanelaDePedidos(
    _inteiro_de_config("IALD_EXTRAIR_TEXTO_POR_HORA", 120, 1), 3600.0)
MSG_EXTRAIR_LIMITE = "Muitas extrações de texto em pouco tempo. Tente de novo mais tarde."


@app.route("/api/extract-text", methods=["POST"])
def api_extract_text():
    """Extrai texto de PDF (pypdf) ou lê arquivo-texto para os anexos do chat."""
    user = session.get("username")
    if not user:
        return jsonify({"error": "Não autenticado"}), 401
    # o tamanho declarado é conferido ANTES de o multipart ser lido (1 MiB de folga p/ o envelope)
    if request.content_length and request.content_length > TETO_EXTRAIR_BYTES + 1024 * 1024:
        return jsonify({"error": "Máximo 25 MB por arquivo"}), 413
    registro = load_users_estrito().get(user) or {}
    if not registro:
        return jsonify({"error": "Não autenticado"}), 401
    if not registro.get("admin"):
        janela = (LIMITE_EXTRAIR_GRATUITO if iald_motores.plano_de(registro) == iald_motores.GRATUITO
                  else LIMITE_EXTRAIR_CONTA)
        if not janela.permitir(user):
            return jsonify({"error": MSG_EXTRAIR_LIMITE}), 429
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "Sem arquivo"}), 400
    name = f.filename or "arquivo"
    data = f.read(TETO_EXTRAIR_BYTES + 1)      # nunca mais que o teto + 1 byte na memória
    if len(data) > TETO_EXTRAIR_BYTES:
        return jsonify({"error": "Máximo 25 MB por arquivo"}), 413
    # ~100k tokens: orçamento de anexos dentro da janela de 131k do serving v2
    MAX_CHARS = 400_000
    text, pages, truncated = "", 0, False
    try:
        if name.lower().endswith(".pdf"):
            import io
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            pages = len(reader.pages)
            parts, total = [], 0
            for pg in reader.pages:
                t = pg.extract_text() or ""
                parts.append(t)
                total += len(t)
                if total > MAX_CHARS:
                    truncated = True
                    break
            text = "\n".join(parts)[:MAX_CHARS]
        else:
            text = data.decode("utf-8", errors="replace")
            if len(text) > MAX_CHARS:
                text, truncated = text[:MAX_CHARS], True
    except Exception as e:
        return jsonify({"error": f"Falha na extração: {e}"}), 422
    return jsonify({"name": name, "text": text, "chars": len(text),
                    "pages": pages, "truncated": truncated,
                    "tokens_est": len(text) // 4})


@app.route("/api/contexto")
def api_contexto():
    """
    Orçamento de contexto REAL, para o frontend decidir quanto histórico enviar.

    Criado em 02/08/2026. Até aqui o chat mandava `MAX_HISTORY = 10` mensagens fixas
    (iald_chat.html), independentemente do modelo: com o kernel em ~11.300 tokens
    dentro de uma janela de 131.072, sobravam ~100.000 tokens de histórico que nunca
    eram usados — e a IALD esquecia o começo da conversa a partir da 11ª mensagem.

    A janela vem do próprio llama-server (`/props`), então trocar de modelo ajusta
    tudo sozinho. Nada aqui é chutado.
    """
    # 14/09/2026: no motor externo a janela é a que o operador paga (IALD_OPENAI_JANELA),
    # não a do llama-server local. 14/09/2026 (noite, C1): no plano gratuito, a do plano.
    # (a leitura do registro vem antes: conta no motor externo não consulta o llama)
    motor_ctx, registro_ctx = _motor_do_usuario(session.get("username", ""))
    if _haiku_selected(registro_ctx, session.get("username", "")):
        if not _haiku_client_ready():
            return jsonify({"error": "Atualize o aplicativo para usar o Haiku com memória integral.",
                            "code": "client_context_update_required"}), 426
        try:
            CLAUDE_ROUTES.configuration(registro_ctx, session.get("username", ""))
            data = _haiku_metadata(_haiku_snapshot(CLAUDE_ROUTES.package()))
            return jsonify(data), 200
        except (ValueError, OSError, KeyError, TypeError, AttributeError):
            return jsonify({"modelo": _HAIKU_PROFILE.model, "disponivel": False,
                "contagem_nativa_por_pedido_obrigatoria": True,
                "error": "Memória ou ferramentas do Haiku indisponíveis.",
                "code": "haiku_package_unavailable"}), 503
    if motor_ctx == app_router.AUTO:
        return jsonify(app_router.limits())
    if motor_ctx in app_providers.MODELS:
        return jsonify(app_providers.context_metadata(motor_ctx))
    if motor_ctx in iald_motores.EXTERNOS:
        # 21/09/2026: a janela do provedor do motor (a do claude vem de IALD_CLAUDE_JANELA, em o200k)
        janela = iald_motores.janela_do_plano(_cfg_do_motor(motor_ctx, registro_ctx), iald_motores.plano_de(registro_ctx))
    else:
        janela = HolographicMemory().janela_do_modelo()
    return jsonify({
        "n_ctx": janela,
        "margem": HolographicMemory.MARGEM_SEGURANCA,
        "reserva_resposta": HolographicMemory.RESPONSE_BUDGET,
        # chars por token, a mesma calibração usada pela memória holográfica
        "cpt": HolographicMemory.CPT,
        # teto de mensagens só como salvaguarda contra casos patológicos;
        # quem manda é o orçamento de tokens
        "teto_mensagens": 400,
    }), 200


# ── CRÉDITO TGL NO PLANO GRATUITO (14/09/2026, noite — revisão de testes A3, interface M5) ──
# REPRODUZIDO (scratchpad\revT\sonda.py, S1): a folha de créditos do app chama /api/tgl/balance,
# que chamava get_account_info → ensure_account → conta nova no razão VIVO com o crédito inicial
# de 1.000 TGL, para toda conta gratuita (o aviso "limite" abre a folha sozinho). Agora, conta do
# plano gratuito SEM conta no razão recebe resposta de leitura, com "sem_conta": true — nenhuma
# chamada que crie conta, nenhuma gravação. Conta gratuita que já tem conta no razão segue como
# antes; o recibo, para ela, só devolve transação da própria conta. tgl_coin_engine.py não mudou:
# a existência da conta é lida pelos atributos do motor (_lock, _refresh_from_disk, _ledger).
MSG_TGL_INDISPONIVEL = "O saldo de créditos está indisponível agora. Tente de novo mais tarde."


def _conta_tgl_existe(user):
    """True/False: a conta existe no razão TGL (relido do disco). Levanta se não der para saber."""
    nome = str(user or "").strip().lower()
    trava = getattr(coin_engine, "_lock", None)
    if trava is None:
        raise ValueError("motor TGL sem trava")
    with trava:
        refrescar = getattr(coin_engine, "_refresh_from_disk", None)
        if callable(refrescar):
            refrescar()
        contas = (getattr(coin_engine, "_ledger", None) or {}).get("accounts")
        if not isinstance(contas, dict):
            raise ValueError("razão TGL sem contas legíveis")
        return nome in contas


def _gratuito_sem_conta_tgl(user):
    """(é conta do plano gratuito?, tem conta no razão?). Arquivo de usuários ilegível → 503 pelo
    tratador de sempre; razão ilegível para o gratuito → ValueError (quem chama responde 503)."""
    registro = load_users_estrito().get(user) or {}
    if iald_motores.plano_de(registro) != iald_motores.GRATUITO:
        return False, True
    return True, _conta_tgl_existe(user)


@app.route("/api/tgl/balance")
def api_tgl_balance():
    """Saldo TGL Coin do usuário logado."""
    user = session.get("username")
    if not user:
        return jsonify({"error": "Não autenticado"}), 401
    if not COIN_AVAILABLE:
        return jsonify({"balance": 0, "tgl_hash": "", "error": "TGL Coin indisponível"}), 200
    try:
        gratuito, tem_conta = _gratuito_sem_conta_tgl(user)
    except (ValueError, OSError, AttributeError, TypeError) as exc:
        print(f"[TGLC] /api/tgl/balance: existência da conta de {user} ilegível ({exc})", flush=True)
        return jsonify({"error": MSG_TGL_INDISPONIVEL}), 503
    if gratuito and not tem_conta:
        return jsonify({
            "balance": 0, "tgl_hash": generate_tgl_hash(user), "verification_hash": "", "verified_at": "",
            "coin": COIN_SYMBOL, "tx_count": 0, "username": user, "source": "sem_conta", "sem_conta": True,
            "usage_tokens": 0, "usage_credits_total": 0.0, "usage_credits_pending": 0.0,
            "usage_rate_per_token": 0.0, "purchasable": False, "redeemable": False, "unlocks_features": False,
            "disclaimer": "",
        }), 200
    # CORRIGIDO 02/08/2026: aqui havia `coin_engine.get_balance(user)`, que devolve um
    # FLOAT (tgl_coin_engine.py:~276 `return account["balance"]`). O código seguinte
    # chamava `.get("balance")` nesse float -> AttributeError -> caía no `except`
    # abaixo, que devolvia HTTP 200 com saldo 0. Resultado: a rota de saldo SEMPRE
    # respondeu 0, e o `except` com status 200 escondeu o defeito. O método correto,
    # que devolve dicionário, é get_account_info().
    try:
        info = coin_engine.get_account_info(user)
        return jsonify({
            "balance": info.get("balance", 0),
            "tgl_hash": generate_tgl_hash(user),
            "verification_hash": info.get("verification_hash", ""),
            "verified_at": info.get("verified_at", ""),
            "coin": info.get("coin", ""),
            "tx_count": info.get("tx_count", 0),
            "username": user,
            "source": "ledger_disk",
            # ── crédito de uso (11/09/2026) ──
            # A ressalva sai JUNTO com o número, sempre. O painel Ψ do app iOS
            # mostrava o saldo em 36pt sem uma linha de ressalva porque esta rota
            # nunca a entregou — e foi assim que a App Review leu "carteira".
            # Quem exibe saldo agora tem como exibir o que ele é.
            "usage_tokens": info.get("usage_tokens", 0),
            "usage_credits_total": info.get("usage_credits_total", 0.0),
            "usage_credits_pending": info.get("usage_credits_pending", 0.0),
            "usage_rate_per_token": info.get("usage_rate_per_token", 0.0),
            "purchasable": False,
            "redeemable": False,
            "unlocks_features": False,
            "disclaimer": info.get("disclaimer", ""),
        }), 200
    except Exception as e:
        # 500, não 200: erro de servidor precisa ser visível, senão um bug destes
        # sobrevive meses disfarçado de "saldo zero".
        print(f"[TGLC] /api/tgl/balance FALHOU para {user}: {e}", flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/tgl/history")
def api_tgl_history():
    """Histórico de transações do usuário logado."""
    user = session.get("username")
    if not user:
        return jsonify({"error": "Não autenticado"}), 401
    if not COIN_AVAILABLE:
        return jsonify([]), 200
    try:
        gratuito, tem_conta = _gratuito_sem_conta_tgl(user)
    except (ValueError, OSError, AttributeError, TypeError) as exc:
        print(f"[TGLC] /api/tgl/history: existência da conta de {user} ilegível ({exc})", flush=True)
        return jsonify({"error": MSG_TGL_INDISPONIVEL}), 503
    if gratuito and not tem_conta:
        # 14/09/2026 (noite): sem conta no razão, nada é criado; objeto em vez de lista para
        # carregar a marca (nenhum cliente de hoje lê esta rota) [INPUT: a ratificar]
        return jsonify({"sem_conta": True, "historico": []}), 200
    try:
        limit = int(request.args.get("limit", 20))
        history = coin_engine.get_history(user, limit=limit)
        return jsonify(history), 200
    except Exception as e:
        return jsonify([]), 200


@app.route("/api/tgl/receipt")
def api_tgl_receipt():
    """Recibo de uma transação específica."""
    user = session.get("username")
    if not user:
        return jsonify({"error": "Não autenticado"}), 401
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin indisponível"}), 503
    tx_hash = request.args.get("hash", "").strip()
    if not tx_hash:
        return jsonify({"error": "hash obrigatório"}), 400
    try:
        gratuito, tem_conta = _gratuito_sem_conta_tgl(user)
    except (ValueError, OSError, AttributeError, TypeError) as exc:
        print(f"[TGLC] /api/tgl/receipt: existência da conta de {user} ilegível ({exc})", flush=True)
        return jsonify({"error": MSG_TGL_INDISPONIVEL}), 503
    if gratuito and not tem_conta:
        return jsonify({"error": "Recibo não encontrado.", "sem_conta": True}), 404
    try:
        receipt = coin_engine.get_receipt(tx_hash)
        # 14/09/2026 (noite): get_receipt busca por PREFIXO do hash em todo o razão; para a
        # conta da porta aberta, só a transação dela [INPUT: a ratificar]
        # ⚠ CORREÇÃO AO LADO (14/09/2026, noite — tarefa SV; relatório S2, [OPEN]): a trava valia só
        # no gratuito; assinante (e qualquer conta não gratuita) recebia a transação de QUALQUER conta
        # pelo prefixo do hash. Agora vale para toda conta nesta rota — o operador continua vendo
        # todas as transações pelo painel (/admin/api/bank/transactions).
        nome = str(user).strip().lower()
        if not isinstance(receipt, dict) or nome not in (receipt.get("from"), receipt.get("to")):
            return jsonify({"error": "Recibo não encontrado."}), 404
        return jsonify(receipt), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# ══════════════════════════════════════════════════════════════
# PSI-NET REST — Para o app iOS (v3.1, autenticado)
# ══════════════════════════════════════════════════════════════

@app.route("/api/psinet/pending")
def api_psinet_pending():
    """Arquivos pendentes para o usuário logado."""
    user = session.get("username")
    if not user:
        return jsonify({"error": "Não autenticado"}), 401
    if not PSINET_AVAILABLE:
        return jsonify([]), 200
    try:
        # CORRIGIDO 02/08/2026: esta rota lia "from_user" e "size_human", chaves que o
        # motor NUNCA produziu. psinet_engine.list_pending() devolve
        # {tx_id, from, filename, original_size, timestamp, send_hash, note}.
        # Resultado: remetente e tamanho sempre chegavam vazios à interface — código
        # escrito contra uma API imaginada e nunca exercitado de ponta a ponta.
        pending = psinet_engine.list_pending(user)
        result = []
        for p in pending:
            tamanho = p.get("original_size", 0) or 0
            result.append({
                "tx_id": p.get("tx_id", ""),
                "filename": p.get("filename", ""),
                "from": p.get("from", ""),
                "original_size": tamanho,
                "size_human": _tamanho_humano(tamanho),
                "timestamp": p.get("timestamp", ""),
                "note": p.get("note", ""),
            })
        return jsonify(result), 200
    except Exception as e:
        print(f"[Ψ-NET] /api/psinet/pending FALHOU para {user}: {e}", flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/psinet/receive", methods=["POST"])
def api_psinet_receive():
    """Aceitar/receber um arquivo pendente."""
    user = session.get("username")
    if not user:
        return jsonify({"error": "Não autenticado"}), 401
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET indisponível"}), 503
    try:
        data = request.get_json(force=True)
        tx_id = data.get("tx_id", "").strip()
        if not tx_id:
            return jsonify({"error": "tx_id obrigatório"}), 400

        ok, result = psinet_engine.receive(tx_id, user)
        if ok:
            dl_name = result.get("download_name", result.get("filename", ""))
            return jsonify({
                "status": "received",
                "filename": result.get("filename", ""),
                "download_url": f"/psinet/download/{dl_name}"
            }), 200
        else:
            return jsonify({"error": result}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════
# ADMIN API — Contract Requests (v3.1)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/contracts", methods=["GET"])
def admin_list_contracts():
    check = require_admin()
    if check:
        return check
    if not contract_engine:
        return jsonify([])
    return jsonify(contract_engine.list_all())


@app.route("/admin/api/contracts/<cid>/status", methods=["PUT"])
def admin_update_contract(cid):
    check = require_admin()
    if check:
        return check
    if not contract_engine:
        return jsonify({"error": "Contract engine indisponível"}), 503
    try:
        data = request.get_json(force=True)
        status = data.get("status", "")
        notes = data.get("notes", "")
        if contract_engine.update_status(cid, status, notes):
            return jsonify({"status": status, "id": cid})
        return jsonify({"error": "Contrato não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════
# HEALTH + API PROXY (with logging)
# ══════════════════════════════════════════════════════════════

@app.route("/health")
def health():
    try:
        r = req_lib.get(f"{LLAMA_URL}/health", timeout=5)
        return Response(r.content, status=r.status_code,
                        content_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=502, content_type="application/json")

@app.route("/v1/<path:subpath>", methods=["GET"])
def api_get(subpath):
    # 14/09/2026 (noite): conta no motor externo (e todo o plano gratuito) não alcança o
    # llama-server local nem para leitura — a mesma regra do POST
    conta_get = session.get("username", "")
    motor_get, registro_get = _motor_do_usuario(conta_get) if conta_get else ("", {})
    if motor_get in iald_motores.EXTERNOS:          # 21/09/2026: openai OU claude
        return jsonify({"error": "Esta conta usa o motor externo; só /v1/chat/completions."}), 403
    if not _caminho_nativo_permitido(registro_get):
        # 14/09/2026 (noite): registro ausente ou plano gratuito nunca alcança o llama local
        return jsonify({"error": MSG_MOTOR_SEM_REGISTRO, "status": "error"}), 503
    try:
        r = req_lib.get(f"{LLAMA_URL}/v1/{subpath}", timeout=30)
        return Response(r.content, status=r.status_code,
                        content_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=502, content_type="application/json")

@app.route("/v1/<path:subpath>", methods=["POST"])
def api_post(subpath):
    # Before shared memory init, wallet, routing and all manual/stream/native models.
    privacy_response = _OWNER_CHAT_PUBLIC_GUARD(request.get_json(silent=True))
    if privacy_response is not None:
        return privacy_response
    return app_memory.dispatch(SERVE_DIR, _chat_account_generation,
        lambda user: app_router.allowed(load_users_estrito().get(user, {}), user),
        lambda path: WALLET_DISPATCH(_api_post_with_wallet, path), subpath)


def _api_post_with_wallet(subpath):
    body = request.get_data()
    is_stream = False
    tokens_in = 0
    req_json = {}
    try:
        req_json = json.loads(body)
        is_stream = req_json.get("stream", False)
        messages = req_json.get("messages", [])
        total_chars = sum(len(m.get("content", "")) for m in messages)
        tokens_in = int(total_chars / 2.91)
    except Exception:
        pass
    g.iald_private_conversation = req_json.get('iald_conv') if isinstance(req_json,dict) else None
    # ── SELO IALD (22/09/2026) ──
    # iald_conv / iald_selo_prev são campos do app: SEMPRE saem do corpo antes de qualquer envio (llama,
    # OpenAI, Anthropic). O pedido de selo guarda só impressões digitais do que o cliente mandou — antes
    # da memória do operador, da compressão e das injeções abaixo — e a resposta é selada no fim do stream,
    # depois desta view (_selo_da_resposta).
    if isinstance(req_json, dict) and ("iald_conv" in req_json or "iald_selo_prev" in req_json):
        g.iald_selo = _pedido_de_selo(req_json, subpath)
        body = json.dumps(req_json).encode("utf-8")
    user = session.get("username", "?")
    t0 = time.time()

    # ── HEARTBEAT: mark user activity (so heartbeat defers) ──
    global _last_user_request_time
    _last_user_request_time = time.time()

    # ── MOTOR POR CONTA (14/09/2026) ──
    # Desvia ANTES da memória do operador, da memória holográfica e das injeções do
    # template Qwen: nada disso pode ir ao motor externo. Conta no motor externo não
    # alcança o llama-server local por nenhuma outra rota /v1.
    # REVISÃO DE SEGURANÇA (14/09/2026, noite) — CRÍTICO 3: leitura estrita. Falha de leitura
    # ou registro ausente → 503 JSON; NUNCA o motor padrão (que hoje é a nativa).
    motor_conta, registro_conta = "", {}
    if user != "?":
        try:
            motor_conta, registro_conta = _motor_do_usuario(user)
        except UsuariosIlegiveis as exc:
            print(f"[motor] leitura do registro de {user} falhou ({exc}); nada enviado", flush=True)
            return jsonify({"error": MSG_MOTOR_SEM_REGISTRO, "status": "error"}), 503
        # Audio/video history must not leak into an incompatible manual executor.
        media_history = any(isinstance(m,dict) and isinstance(m.get('content'),list) and any(
            isinstance(part,dict) and part.get('type') in ('input_audio','video_url','iald_media')
            for part in m['content']) for m in (req_json.get('messages') or []) if isinstance(m,dict))
        if media_history and motor_conta not in (app_router.AUTO,'mimo'):
            return _sse_aviso('Esta conversa contém áudio ou vídeo e precisa do MiMo ou do modo automático. Abra outra conversa para trocar de modelo.','recurso_indisponivel')
        if motor_conta == app_router.AUTO:
            if subpath != 'chat/completions':
                return jsonify({'error':'Este modo atende somente ao chat.'}),403
            return _chat_automatico(req_json,user,registro_conta,is_stream,tokens_in)
        if motor_conta in app_providers.MODELS:
            if subpath != 'chat/completions':
                return jsonify({'error': 'Este motor atende somente ao chat.'}), 403
            return _chat_avaliacao(req_json, user, registro_conta, is_stream, motor_conta)
        if motor_conta == iald_motores.CLAUDE:
            # 21/09/2026: o motor claude, ANTES da trava nativa — e sem volta: _chat_claude nunca
            # devolve None, e se devolvesse a resposta seria a recusa, nunca o llama local
            if subpath != "chat/completions":
                return jsonify({"error": "Esta conta usa o motor externo; só /v1/chat/completions."}), 403
            resposta = _chat_claude(req_json, user, registro_conta, is_stream, tokens_in)
            if resposta is not None:
                return resposta
            return _sse_aviso(MSG_CLAUDE_NAO_LIBERADO, "motor_indisponivel")
        if motor_conta == iald_motores.OPENAI:
            if subpath != "chat/completions":
                return jsonify({"error": "Esta conta usa o motor externo; só /v1/chat/completions."}), 403
            resposta = _chat_openai(req_json, user, registro_conta, is_stream, tokens_in)
            if resposta is not None:
                return resposta
            # None: o operador ligou a reserva nativa e o motor externo está indisponível
            if iald_motores.plano_de(registro_conta) == iald_motores.GRATUITO:
                # 14/09/2026 (noite): o plano gratuito NUNCA desce ao caminho nativo — é
                # ali embaixo que entram a memória do operador e o conjunto inteiro de
                # ferramentas. _chat_openai já não devolve None para ele; esta é a segunda trava.
                return _sse_aviso(_motor_externo_indisponivel(iald_motores.modelo_para(registro_conta, MOTORES_CFG))
                                  or "O motor desta conta está indisponível agora.", "motor_indisponivel")
    if not _caminho_nativo_permitido(registro_conta):
        # a terceira trava: daqui para baixo entram o llama local, a memória do operador e as
        # ferramentas nativas — só para conta com registro lido e plano diferente de gratuito
        print(f"[motor] caminho nativo recusado para {user!r} (registro ausente ou plano gratuito)", flush=True)
        return jsonify({"error": MSG_MOTOR_SEM_REGISTRO, "status": "error"}), 503

    # ── MEMÓRIA DO OPERADOR (02/08/2026) ──
    # Dois blocos, em lugares DIFERENTES de propósito:
    #
    #   bloco_sempre()      -> vai no SYSTEM. É determinístico (ordenado por escopo+id,
    #                          sem data/hora, sem contador), então o prefixo continua
    #                          idêntico entre turnos e o llama-server segue
    #                          reaproveitando o cache (medido: 13.453 tokens).
    #
    #   bloco_sob_demanda() -> vai no fim da ÚLTIMA MENSAGEM DO USUÁRIO, nunca no
    #                          system. Ele MUDA a cada pergunta; se entrasse no
    #                          prefixo, invalidaria o cache inteiro a cada turno —
    #                          e o bloco de system é fundido no topo logo abaixo
    #                          (exigência do template Qwen3.6), o que agravaria isso.
    if subpath == "chat/completions" and messages and MEMORIA_OP_AVAILABLE:
        try:
            fixo = memoria_op.bloco_sempre()
            if fixo:
                messages.append({"role": "system", "content": fixo})

            # texto da última mensagem do usuário, para a recuperação
            idx_user = None
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get("role") == "user":
                    idx_user = i
                    break
            if idx_user is not None:
                c = messages[idx_user].get("content", "")
                if isinstance(c, list):
                    consulta = " ".join(p.get("text", "") for p in c
                                        if isinstance(p, dict) and p.get("type") == "text")
                else:
                    consulta = c or ""
                recuperado = memoria_op.bloco_sob_demanda(consulta)
                if recuperado:
                    if isinstance(c, list):
                        messages[idx_user]["content"] = c + [
                            {"type": "text", "text": "\n\n" + recuperado}]
                    else:
                        messages[idx_user]["content"] = f"{consulta}\n\n{recuperado}"
                    print(f"[Memoria] recuperou {recuperado.count(chr(10)) } fato(s) "
                          f"para esta pergunta", flush=True)
            req_json["messages"] = messages
            body = json.dumps(req_json).encode("utf-8")
        except Exception as e:
            return jsonify({"error": "Memória do operador indisponível; nenhum envio."}), 503

    # ── SACRED LANGUAGE: inject user language preference ──
    if subpath == "chat/completions" and messages and user != "?":
        try:
            USERS_LANG = load_users()
            user_data = USERS_LANG.get(user, {})
            if not user_data.get("sacred_language", False):
                sacred_msg = {
                    "role": "system",
                    "content": (
                        "INSTRUCAO DE LINGUAGEM: Para este usuario, evite linguagem "
                        "teologica (Verbo, Nome, Palavra, TETELESTAI, Haja Luz, trinidade "
                        "ontologica, etc). Use linguagem tecnica e cientifica equivalente. "
                        "Somente use linguagem teologica se o usuario expressamente pedir."
                    )
                }
                # Inserir após as mensagens system mas antes do histórico
                insert_idx = 0
                for i, m in enumerate(messages):
                    if m.get("role") != "system":
                        insert_idx = i
                        break
                else:
                    insert_idx = len(messages)
                messages.insert(insert_idx, sacred_msg)
                req_json["messages"] = messages
                body = json.dumps(req_json).encode("utf-8")
        except Exception as e:
            print(f"[Sacred] Erro (fallback): {e}")

    # ── CRÉDITO DA OPENAI CRÍTICO (15/09/2026): a própria IALD avisa o operador ──
    # Só conta admin, só nos níveis crítico/esgotado, no começo da conversa ou de 6 em 6 horas
    # (ver _alerta_saldo_operador). Vai como system; a fusão Qwen logo abaixo o põe no topo.
    if subpath == "chat/completions" and messages:
        alerta_saldo = _alerta_saldo_operador(registro_conta, messages, user)
        if alerta_saldo:
            messages.append({"role": "system", "content": alerta_saldo})
            req_json["messages"] = messages
            body = json.dumps(req_json).encode("utf-8")
            print(f"[saldo] aviso de crédito crítico entregue à conversa de {user}", flush=True)

    # ── QWEN3.6 (IALD Nativa v2): o chat template exige UM UNICO system, na
    # posicao 0 ("System message must be at the beginning", 08/07/2026). O chat
    # e as injecoes (kernel, Sacred, correcoes verbais) podem produzir varios
    # systems fora de ordem: aqui todos sao FUNDIDOS num so, no topo, preservando
    # a ordem do conteudo e do restante do historico. Inofensivo p/ modelos antigos.
    if subpath == "chat/completions" and messages:
        try:
            sys_msgs = [m for m in messages if m.get("role") == "system"]
            precisa = (len(sys_msgs) > 1) or (sys_msgs and messages[0].get("role") != "system")
            if precisa:
                merged = {"role": "system",
                          "content": "\n\n".join(m.get("content", "") for m in sys_msgs)}
                messages = [merged] + [m for m in messages if m.get("role") != "system"]
                req_json["messages"] = messages
                body = json.dumps(req_json).encode("utf-8")
                print(f"[Qwen36-sys] {len(sys_msgs)} system(s) fundidos em 1 no topo")
        except Exception as e:
            print(f"[Qwen36-sys] Erro (fallback): {e}")

    # ── SELETOR DE MODO (⚡ rápido / 🧠 pensar) ──
    # O cliente envia "iald_mode": "fast"|"think" (campo custom, REMOVIDO antes do
    # proxy). Vira chat_template_kwargs.enable_thinking do template Qwen3.6 — que
    # sobrepõe o "--reasoning off" do serving da v2 (default sem o campo = rápido).
    if subpath == "chat/completions":
        try:
            iald_mode = req_json.pop("iald_mode", None)
            if iald_mode is not None:
                think = (iald_mode == "think")
                ctk = req_json.get("chat_template_kwargs") or {}
                ctk["enable_thinking"] = think
                req_json["chat_template_kwargs"] = ctk
                if think:
                    # pensar consome tokens antes da resposta: teto maior
                    req_json["max_tokens"] = max(int(req_json.get("max_tokens", 4096)), 8192)
                body = json.dumps(req_json).encode("utf-8")
                print(f"[iald-mode] {'think' if think else 'fast'}")
        except Exception as e:
            print(f"[iald-mode] Erro (fallback): {e}")

    # ── SUPERFÍCIE DE ORIGEM (11/09/2026) ──
    # O cliente envia "iald_surface": "app"|"web" (campo custom, REMOVIDO antes do
    # proxy, como o iald_mode). Serve para o build das lojas não receber a
    # ferramenta de contratação comercial — ver FERRAMENTAS_FORA_DA_LOJA.
    # Ausência do campo = "web" = comportamento de sempre.
    superficie = "web"
    if subpath == "chat/completions":
        try:
            if "iald_surface" in req_json:
                superficie = (req_json.pop("iald_surface") or "web").strip().lower()
                body = json.dumps(req_json).encode("utf-8")
                print(f"[iald-surface] {superficie}")
        except Exception as e:
            superficie = "web"
            print(f"[iald-surface] Erro (fallback web): {e}")

    if session.get("app_surface"):
        superficie = "app"
    operator_authorized = _local_operator_request() and bool(session.get("is_admin"))

    # Server-owned canonical context follows compression and all client injections.
    native_tools, native_check = None, None
    if subpath == 'chat/completions':
        try:
            req_json, native_tools, native_check = _prepare_native_payload(req_json, superficie)
            body = json.dumps(req_json).encode('utf-8')
        except (ValueError, OSError, KeyError, TypeError) as exc:
            message = (str(exc) if isinstance(exc, native_memory.NativeContextError)
                       else 'Memória canônica nativa indisponível ou divergente.')
            return jsonify({'error': message}), (413 if isinstance(exc, native_memory.NativeContextError) else 503)

    # ── SMART ROUTING: only use agent loop when tools might be needed ──
    if is_stream and subpath == "chat/completions":
        messages = req_json.get("messages", [])

        # Find last user message for heuristic analysis
        has_image = False
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                c = m.get("content", "")
                if isinstance(c, list):
                    # conteúdo multimodal (visão): lista de partes {type, ...}
                    has_image = any(isinstance(p, dict) and p.get("type") == "image_url" for p in c)
                    c = " ".join(p.get("text", "") for p in c
                                 if isinstance(p, dict) and p.get("type") == "text")
                last_user_msg = (c or "").lower()
                break

        # ── Pre-filter: does this message need tools? ──
        # Keywords that suggest tools are needed
        # (NEEDS_TOOLS_PATTERNS virou constante de módulo — ver topo do arquivo)

        # Imagem vai SEMPRE pelo fast path (streaming direto): o agent loop é
        # não-streaming e as ferramentas não precisam do conteúdo visual.
        #
        # CASAMENTO POR PALAVRA INTEIRA (02/08/2026) ────────────────────────────
        # Antes isto era `p in last_user_msg`, substring pura sobre 108 padrões.
        # Consequência medida na lista: "site" casava dentro de "necessitava",
        # "visite", "parasita"; "histor" dentro de "historiador"; "fonte" dentro
        # de "defronte"; "moeda" dentro de "amoedado". Qualquer um deles jogava a
        # pergunta no agent_loop — que é NÃO-streaming, faz até 6 chamadas
        # encadeadas e demora muito mais.
        #
        # Agora: padrões de UMA palavra exigem fronteira de palavra (\b...\b);
        # padrões com espaço ("prova viva", "meu saldo") continuam por substring,
        # porque já são específicos o bastante.
        #
        # O keepalive SSE (ver AGENT_KEEPALIVE_SEC) impede que o caminho do agente
        # derrube a conexão. Isto aqui é sobre não entrar nele à toa.
        needs_tools = (not has_image) and (_precisa_ferramentas(last_user_msg)
                                         or native_memory.needs_canonical_tools(last_user_msg))

        if needs_tools:
            # ── AGENT LOOP: message needs tools ──
            max_tokens = req_json.get("max_tokens", 4096)
            temperature = req_json.get("temperature", 0.7)
            log_request(user, f"/v1/{subpath}", "POST",
                        tokens_in=tokens_in, status="agent_stream")

            def generate():
                yield from agent_loop(messages, user=user,
                                      max_tokens=max_tokens,
                                      temperature=temperature,
                                      ferramentas=native_tools,
                                      operator_authorized=operator_authorized,
                                      verificar_payload=native_check,
                                      executar=lambda name,args,**kwargs: _science_tool(native_check.science_snapshot,execute_public_tool,name,args,**kwargs))
            return _identificar_resposta(Response(
                _medir_saida_sse(generate(), user, "agente"),
                status=200,
                content_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    # "Connection" REMOVIDO em 02/08/2026: e cabecalho hop-by-hop e a PEP 3333
                    # PROIBE a aplicacao WSGI de defini-lo. O servidor de
                    # desenvolvimento do Werkzeug tolerava; o waitress (que passou
                    # a servir hoje) recusa com AssertionError -> HTTP 500. Todo
                    # chat com streaming quebrou por HTTP real, e os testes em
                    # processo NAO pegaram: o test client nao aplica a PEP 3333.
                    # Quem cuida do keep-alive e o servidor, nao a aplicacao.
                    "X-Accel-Buffering": "no",
                }
            ), _modelo_nativo_resposta())
        else:
            # ── FAST PATH: no tools needed, direct streaming proxy ──
            log_request(user, f"/v1/{subpath}", "POST",
                        tokens_in=tokens_in, status="streaming_fast")
            return _identificar_resposta(_stream_proxy(subpath, body, user=user, origem="chat"),
                                         _modelo_nativo_resposta())

    # ── Normal proxy (non-streaming or non-chat endpoints) ──
    if is_stream:
        log_request(user, f"/v1/{subpath}", "POST", tokens_in=tokens_in, status="streaming")
        return _stream_proxy(subpath, body, user=user, origem="stream")
    else:
        result = _normal_proxy(subpath, body)
        duration_ms = int((time.time() - t0) * 1000)
        tokens_out = 0
        try:
            resp_data = json.loads(result.get_data())
            usage = resp_data.get("usage", {})
            tokens_out = usage.get("completion_tokens", 0)
            tokens_in = usage.get("prompt_tokens", tokens_in)
        except Exception:
            pass
        log_request(user, f"/v1/{subpath}", "POST", tokens_in=tokens_in,
                    tokens_out=tokens_out, duration_ms=duration_ms, status="ok")
        # Aqui o número é EXATO: veio de usage.completion_tokens do llama-server,
        # não de estimativa por caracteres como nos caminhos de streaming.
        if subpath == "chat/completions" and tokens_out:
            _contabilizar_uso(user, tokens_out, origem="direto")
        return _identificar_resposta(result, _modelo_nativo_resposta()) if subpath == "chat/completions" else result

# ══════════════════════════════════════════════════════════════
# CRÉDITO DE USO — o ponto de medição (11/09/2026)
#
# POR QUE EXISTE: o TGL Coin se descrevia como "crédito interno (medição de uso)"
# mas NADA media uso. O saldo vinha de um airdrop fixo de 1.000 na criação da
# conta, e só. A App Review da Apple perguntou por que existe uma "moeda" sem
# valor comercial — e a resposta honesta exige que o crédito realmente meça o
# uso, não que a gente diga que mede.
#
# O QUE SE MEDE: os tokens que a IALD PRODUZIU. O prompt reenvia histórico e
# kernel a cada turno; contá-lo inflaria o número sem medir trabalho novo.
#
# ⚠ NOS CAMINHOS DE STREAMING O NÚMERO É ESTIMADO. Medido em 11/09/2026: as três
# rotas de stream chamam log_request só com tokens_in — ninguém nunca contou o
# que saiu. Aqui se contam os caracteres de delta.content/reasoning_content e se
# divide pela mesma calibração do resto da casa (HolographicMemory.CPT). Se o
# llama-server passar a mandar o bloco `usage` no stream (stream_options.
# include_usage), ele é preferido automaticamente e o número vira exato.
# Não liguei include_usage agora porque o modelo está fora do ar pelo treino e
# eu não teria como testar — ficaria afirmando sem medir.
# ══════════════════════════════════════════════════════════════

def _contabilizar_uso(user, tokens_gerados, origem="chat"):
    """Credita o uso. Falha aqui NUNCA pode afetar a resposta ao usuário."""
    # ⚠ INTERRUPTOR, ADICIONADO 11/09/2026 POR EVENTO MEDIDO, NÃO POR PRECAUÇÃO.
    # Na primeira rodada da suíte depois de instalar a medição, o
    # tests/test_streaming_agente.py — que importa o servidor e faz POST em
    # /v1/chat/completions pelo test_client — passou por aqui e ESCREVEU no razão
    # de produção (C:\IALD\bank\tglc_ledger.json mudou de hash). Foi gravação
    # aditiva e benigna, mas um teste jamais deve tocar o razão vivo.
    # A suíte (tests/rodar_tudo.ps1) agora exporta IALD_CREDITO_USO=0.
    if os.environ.get("IALD_CREDITO_USO", "1") == "0":
        return
    if not COIN_AVAILABLE or not user or user == "?":
        return
    try:
        coin_engine.registrar_uso(user, tokens_gerados, origem=origem)
    except Exception as exc:      # noqa: BLE001
        print(f"[TGLC] contabilizacao de uso falhou ({origem}): {exc}", flush=True)


def _medir_saida_sse(fluxo, user, origem):
    """
    Observador PASSIVO de um fluxo SSE.

    Regra inegociável: o pedaço é repassado INTACTO e ANTES de qualquer conta.
    A medição vive dentro de try/except mudo — um erro de contagem não pode
    engolir um token da resposta nem derrubar o stream. O `finally` garante a
    contabilização mesmo quando o cliente desliga no meio (GeneratorExit).
    """
    # Sem dono não há o que creditar: sai do caminho e vira um repasse puro.
    # (A guarda também existe em _contabilizar_uso; aqui ela evita contar à toa
    # e torna o contrato do observador explícito em vez de herdado.)
    if not user or user == "?":
        yield from fluxo
        return

    chars = 0
    usage_real = {}
    bufer = ""
    try:
        for pedaco in fluxo:
            yield pedaco                      # ← primeiro entrega, depois mede
            try:
                if isinstance(pedaco, (bytes, bytearray)):
                    texto = pedaco.decode("utf-8", "replace")
                else:
                    texto = str(pedaco)
                bufer += texto
                linhas = bufer.split("\n")
                bufer = linhas.pop()
                for ln in linhas:
                    ln = ln.strip()
                    if not ln.startswith("data: "):
                        continue              # ":" = keepalive
                    corpo = ln[6:].strip()
                    if not corpo or corpo == "[DONE]":
                        continue
                    ck = json.loads(corpo)
                    u = ck.get("usage")
                    if isinstance(u, dict) and u.get("completion_tokens"):
                        usage_real = u
                    escolhas = ck.get("choices") or []
                    if escolhas:
                        delta = escolhas[0].get("delta") or {}
                        chars += len(delta.get("content") or "")
                        chars += len(delta.get("reasoning_content") or "")
            except Exception:
                pass                          # medir jamais interrompe o stream
    finally:
        try:
            if usage_real.get("completion_tokens"):
                tokens = int(usage_real["completion_tokens"])      # exato
            elif chars:
                tokens = int(chars / HolographicMemory.CPT)        # estimado
            else:
                tokens = 0
            if tokens > 0:
                _contabilizar_uso(user, tokens, origem)
        except Exception:
            pass


def _prepare_completion_body(body):
    payload = app_memory.project_completion_payload(json.loads(body))
    model_id, base_url = ACTIVE_MODEL_ID, LLAMA_URL
    configured = native_memory.configured_window(MODELS[model_id])
    serving = native_memory._local_json(base_url, '/props')['default_generation_settings']['n_ctx']
    tokens = native_memory._local_json(base_url, '/tokenize',
        {'content': payload['prompt'], 'add_special': True, 'parse_special': True})['tokens']
    reserve = payload.get('max_tokens', 4096)
    if (type(serving) is not int or serving <= 0 or not isinstance(tokens, list) or not tokens
            or any(type(t) is not int or t < 0 for t in tokens) or type(reserve) is not int or reserve <= 0
            or len(tokens) + reserve + 256 > min(configured, serving)):
        raise ValueError('Completion exceeds the measured native context window')
    if model_id != ACTIVE_MODEL_ID or base_url != LLAMA_URL:
        raise ValueError('Native completion model changed during counting')
    return json.dumps(payload, ensure_ascii=False).encode('utf-8')


def _normal_proxy(subpath, body):
    try:
        if subpath == "completions":
            body = _prepare_completion_body(body)
        r = app_memory.http_call('model._normal_proxy', req_lib.post, f"{LLAMA_URL}/v1/{subpath}", data=body,
                         headers={"Content-Type": "application/json"}, timeout=600)
        return Response(r.content, status=r.status_code,
                        content_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=502, content_type="application/json")

def _stream_proxy(subpath, body, user=None, origem="chat"):
    if subpath == "completions":
        body = _prepare_completion_body(body)
    # user/origem são OPCIONAIS de propósito: assim os chamadores antigos
    # continuam válidos e a medição é aditiva, nunca uma troca de contrato.
    def generate():
        try:
            r = app_memory.http_call('model._stream_proxy', req_lib.post, f"{LLAMA_URL}/v1/{subpath}", data=body,
                             headers={"Content-Type": "application/json"}, stream=True, timeout=600)
            for chunk in r.iter_content(chunk_size=256):
                if chunk:
                    yield chunk
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n".encode()

    fluxo = generate()
    if user and subpath == "chat/completions":
        fluxo = _medir_saida_sse(fluxo, user, origem)
    return Response(fluxo, status=200, content_type="text/event-stream",
                    headers={"Cache-Control": "no-cache",  # sem "Connection": hop-by-hop, ver acima
                             "X-Accel-Buffering": "no"})


# ══════════════════════════════════════════════════════════════
# ADMIN — guard function (preserved from v6 pattern)
# ══════════════════════════════════════════════════════════════

def _local_operator_request():
    # 21/09/2026 (revisão da aba da Central, 3.md §3.7): o waitress APAGA X-Forwarded-For,
    # X-Forwarded-Host e Forwarded antes do Flask (trusted_proxy=None) — das quatro checagens de
    # cabeçalho só CF-Connecting-IP valia em produção. Cf-Ray, Cdn-Loop e Cf-Visitor, que a borda
    # da Cloudflare sempre põe e o waitress não apaga, entram como sinais extras de túnel.
    if not has_request_context():
        return False
    return (request.remote_addr in ("127.0.0.1", "::1")
            and request.host.split(":")[0].lower() in ("localhost", "127.0.0.1")
            and not any(request.headers.get(h) for h in
                        ("CF-Connecting-IP", "X-Forwarded-For", "Forwarded", "X-Forwarded-Host",
                         "Cf-Ray", "Cdn-Loop", "Cf-Visitor")))


def require_admin():
    if not _local_operator_request():
        return jsonify({'error': 'Acesso restrito a localhost'}), 403
    if not session.get('is_admin'):
        return jsonify({'error': 'Apenas administradores'}), 403
    return None


# ══════════════════════════════════════════════════════════════
# ADMIN — Dashboard page
# ══════════════════════════════════════════════════════════════

# 14/09/2026 (noite) — revisão de segurança, CRÍTICO 1. Medido o que o painel carrega: scripts
# e estilos INLINE (inclusive onclick/onerror), a folha do Google Fonts (fonts.googleapis.com,
# que puxa fonts.gstatic.com), a imagem /iald_logo_header.png e fetch só para a própria origem.
# Nada de eval, iframe, formulário ou import. A política abaixo mantém isso funcionando e
# barra o que um XSS precisaria para ir além da página: import() de script externo, envio
# para fora (connect-src), <base> trocado, formulário para fora e o painel dentro de moldura.
# 'unsafe-inline' continua necessário enquanto o painel for inline — por isso o escape em
# TODA montagem de innerHTML segue sendo a trava principal; a CSP é a segunda.
# 15/09/2026 (sessao gerente do LAR, ordem do operador): 'frame-ancestors none' barrava tambem a COLUNA IALD do
# painel LAR MIGUEL (http://localhost:8900 embute /admin num iframe) -- o login dava LOGIN_OK e a coluna ficava
# em branco. Agora so' o painel local pode emoldurar; qualquer outro site continua barrado (anti-clickjacking).
CSP_PAINEL = ("default-src 'self'; script-src 'self' 'unsafe-inline'; "
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
              "font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; "
              "connect-src 'self'; frame-ancestors http://localhost:8900; base-uri 'none'; form-action 'self'")


@app.route("/admin")
def admin_dashboard():
    check = require_admin()
    if check:
        return check
    resposta = make_response(render_admin_page())
    resposta.headers["Content-Security-Policy"] = CSP_PAINEL
    return resposta


# ══════════════════════════════════════════════════════════════
# ADMIN API — Model Selector + Process Manager (Mark 4)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/models", methods=["GET"])
def admin_list_models():
    check = require_admin()
    if check:
        return check
    result = []
    for mid, info in MODELS.items():
        online = False
        try:
            r = req_lib.get(f"http://127.0.0.1:{info['port']}/health", timeout=2)
            online = r.status_code == 200
        except Exception:
            pass
        result.append({
            "id": mid,
            "port": info["port"],
            "name": info["name"],
            "label": info["label"],
            "active": mid == ACTIVE_MODEL_ID,
            "online": online,
        })
    return jsonify({
        "models": result,
        "active": ACTIVE_MODEL_ID,
        "managed": _is_model_process_running(),
        "tunnel": _is_tunnel_running(),
    })


@app.route("/admin/api/start-model", methods=["POST"])
def admin_start_model():
    """Stop current server (if any) and start the requested model."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    model_id = data.get("model_id", "")
    if model_id not in MODELS:
        return jsonify({"error": f"Modelo desconhecido: {model_id}"}), 400

    with _process_lock:
        # Stop current model if running
        _stop_model_process()

        # Wait a moment for port to free
        time.sleep(1)

        # ── TRAVA ANTI-DUPLA-CARGA (02/08/2026) ──
        # _stop_model_process() só encerra o subprocesso que ESTE Flask criou. Se o
        # llama-server foi iniciado fora do painel (na mão, ou pelo start_iald_llama.ps1
        # supervisionado), ele continua vivo segurando a porta E a VRAM. Subir outro aqui
        # coloca dois modelos de 19,7 GiB numa GPU de 32 GiB e derruba a inferência.
        # Recusar é o certo: quem manda no processo externo é o supervisor, não o painel.
        porta_alvo = MODELS[model_id]["port"]
        externo = _servidor_externo_na_porta(porta_alvo)
        if externo is not None:
            msg = (
                f"Há um llama-server EXTERNO na porta {porta_alvo} (PID {externo}), "
                f"iniciado fora do painel. Subir outro esgotaria a VRAM da GPU. "
                f"Pare o supervisor primeiro: "
                f"powershell -File C:\\IALD\\projetos_pyhton\\IALD\\stop_iald_llama.ps1"
            )
            print(f"[IALD] start-model RECUSADO: {msg}", flush=True)
            auth_log("MODEL_START_BLOCKED", session.get("username", "?"),
                     f"port={porta_alvo} pid_externo={externo} model={model_id}")
            return jsonify({"error": msg, "external_pid": externo}), 409

        # Start new model
        _start_model_process(model_id)

        # Wait for it to become healthy (up to 120s for 122B loading)
        label = MODELS[model_id]["label"]
        port = MODELS[model_id]["port"]
        max_wait = 120
        started = False
        for i in range(max_wait):
            time.sleep(1)
            if _model_process and _model_process.poll() is not None:
                return jsonify({"error": f"{label} crashou ao iniciar (exit code {_model_process.returncode})"}), 500
            try:
                r = req_lib.get(f"http://127.0.0.1:{port}/health", timeout=2)
                if r.status_code == 200:
                    started = True
                    break
            except Exception:
                pass
            if i % 10 == 0 and i > 0:
                print(f"[IALD] Aguardando {label}... ({i}s)", flush=True)

        if not started:
            return jsonify({"error": f"{label} nao ficou pronto em {max_wait}s"}), 504

        # Switch proxy
        switch_model(model_id)
        auth_log("MODEL_START", session.get("username", "?"), f"started {model_id} (port {port})")
        print(f"[IALD] {label} ONLINE — proxy apontando para porta {port}", flush=True)

    return jsonify({"ok": True, "model": MODELS[model_id], "active": model_id})


@app.route("/admin/api/stop-model", methods=["POST"])
def admin_stop_model():
    """Stop the currently running model server."""
    check = require_admin()
    if check:
        return check
    with _process_lock:
        if not _is_model_process_running():
            return jsonify({"error": "Nenhum servidor gerenciado rodando"}), 400
        _stop_model_process()
        auth_log("MODEL_STOP", session.get("username", "?"), f"stopped model")
    return jsonify({"ok": True})


@app.route("/admin/api/tunnel", methods=["POST"])
def admin_toggle_tunnel():
    """Start or stop cloudflared tunnel."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    action = data.get("action", "toggle")

    with _process_lock:
        if action == "stop" or (action == "toggle" and _is_tunnel_running()):
            _stop_tunnel()
            auth_log("TUNNEL_STOP", session.get("username", "?"), "tunnel stopped")
            return jsonify({"ok": True, "tunnel": False})
        else:
            _start_tunnel()
            # Give it a moment to connect
            time.sleep(2)
            running = _is_tunnel_running()
            auth_log("TUNNEL_START", session.get("username", "?"), "tunnel started")
            return jsonify({"ok": True, "tunnel": running})


# ══════════════════════════════════════════════════════════════
# ADMIN API — User Management CRUD (preserved from v6)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/users", methods=["GET"])
def admin_list_users():
    check = require_admin()
    if check:
        return check
    global USERS
    USERS = load_users_estrito()       # ilegível → 503 (não uma lista vazia enganosa)
    user_list = []
    # 14/09/2026 (noite): uso em tokens do dia e do mês (UTC) por conta, lido do razão da
    # OpenAI UMA vez para a lista inteira (com a porta aberta a lista cresce)
    try:
        dias_uso, erro_uso = RAZAO_OPENAI.resumo(40), ""
    except Exception as exc:      # noqa: BLE001
        dias_uso, erro_uso = {}, f"razão de uso ilegível: {exc}"
    hoje_utc = time.strftime("%Y-%m-%d", time.gmtime())
    for username, data in USERS.items():
        chave_uso = _chave_cota_de(data, username)
        tokens_dia = tokens_mes = 0
        for dia_utc, dia in dias_uso.items():
            if not str(dia_utc).startswith(hoje_utc[:7]):
                continue
            n = int((((dia or {}).get("cotas") or {}).get(chave_uso) or {}).get("tokens", 0) or 0)
            tokens_mes += n
            if dia_utc == hoje_utc:
                tokens_dia = n
        efetivo = _motor_efetivo(data, username)          # 21/09/2026: com a lista do claude
        user_list.append({
            "plano": data.get("plano", "") if data.get("plano") in iald_motores.PLANOS else "",
            "plano_efetivo": iald_motores.plano_de(data),
            "bloqueado": data.get("bloqueado") if _conta_bloqueada(data) else None,
            "uso_tokens": {"dia": tokens_dia, "mes": tokens_mes, "erro": erro_uso},
            "source": data.get("source", ""),
            "username": username,
            "admin": data.get("admin", False),
            "created": data.get("created", ""),
            "sacred_language": data.get("sacred_language", False),
            "tgl_hash": generate_tgl_hash(username),
            # 14/09/2026: por onde a pessoa entra (Apple/Google), para o painel
            "identidades": identidade.identidades_publicas(data),
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            # 14/09/2026: motor fixado ("" = regra geral), o que vale de fato e o consentimento
            "motor": data.get("motor", "") if data.get("motor") in iald_motores.MOTORES else "",
            "motor_efetivo": efetivo,
            # 21/09/2026: o consentimento do provedor do motor EFETIVO (claude → o da Anthropic)
            "consentimento_ia": iald_motores.consentiu(
                data, efetivo if efetivo in iald_motores.EXTERNOS else iald_motores.OPENAI),
            # 15/09/2026: conta ampliada (IALD Nativa + ChatGPT) ou padrão (só ChatGPT)
            "acesso_nativa": iald_motores.pode_usar_nativa(data),
            # 21/09/2026: a conta pode ter o claude fixado (ampliada E na lista IALD_CLAUDE_CONTAS)
            # (revisão: e o claude configurado — _contas_claude(), a mesma lista que escolher_motor usa)
            "claude_permitido": bool(CLAUDE_ROUTES.options(data, username)),
        })
    # Ordenar alfabeticamente
    user_list.sort(key=lambda x: x["username"])
    return jsonify({"users": user_list})


@app.route("/admin/api/users/<username>/motor", methods=["PUT"])
def admin_definir_motor(username):
    check = require_admin()
    if check:
        return check
    option = str((request.get_json(silent=True) or {}).get("motor", "")).strip().lower()
    if option not in ("", "nativa", "openai", "claude", "claude-haiku", "claude-sonnet", app_router.AUTO, *app_providers.MODELS):
        return jsonify({"error": "Modelo inválido."}), 400
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        conta = usuarios.get(username)
        if not conta:
            return jsonify({"error": "Conta não encontrada."}), 404
        if option not in ('',app_router.AUTO) and not app_router.manual_allowed(conta, username):
            return jsonify({'error':'Esta conta usa a seleção automática da IALD.','motor':app_router.AUTO}),403
        if option == app_router.AUTO and not app_router.allowed(conta, username):
            return jsonify({"error":"Modo automático não liberado para esta conta."}),403
        if option in app_providers.MODELS and not app_providers.allowed(conta, username, option):
            return jsonify({"error": "Modelo não liberado para esta conta."}), 403
        if option.startswith("claude"):
            try:
                fields = CLAUDE_ROUTES.select(option, conta, username)
                CLAUDE_ROUTES.configuration(dict(conta, **fields), username)
            except (PermissionError, ValueError, OSError, KeyError):
                return jsonify({"error": "Modelo não disponível para esta conta."}), 409
            conta.update(fields)
        elif option == "nativa":
            if not iald_motores.pode_usar_nativa(conta):
                return jsonify({"error": "Acesso à IALD Nativa não liberado."}), 409
            conta["motor"] = option
        elif option:
            conta["motor"] = option
        else:
            conta.pop("motor", None)
            conta.pop("modelo_claude", None)
        conta['motor_escolha_versao']=app_router.DEFAULT_POLICY
        save_users(usuarios)
        efetivo = _motor_efetivo(conta, username)
    auth_log("ADMIN_MOTOR", session.get("username", "?"), "user=" + username + " model=" + (option or "regra-geral"))
    return jsonify({"ok": True, "motor": conta.get("motor", ""), "motor_efetivo": efetivo,
                    "motor_selecao": _motor_selection_id(efetivo, conta, username)})


@app.route("/admin/api/users/<username>/acesso_nativa", methods=["PUT"])
def admin_definir_acesso_nativa(username):
    """Amplia ({acesso_nativa: true}: IALD Nativa + ChatGPT, escolha no app) ou reduz
    ({acesso_nativa: false}: só ChatGPT) uma conta. 15/09/2026, ordem do operador."""
    check = require_admin()
    if check:
        return check
    dados = request.get_json(silent=True)
    valor = dados.get("acesso_nativa") if isinstance(dados, dict) else None
    if not isinstance(valor, bool):
        return jsonify({"error": "Informe acesso_nativa: true ou false."}), 400
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        conta = usuarios.get(username)
        if not conta:
            return jsonify({"error": f"Usuário '{username}' não encontrado"}), 404
        if conta.get("admin"):
            return jsonify({"error": "Administrador já usa a IALD Nativa e o ChatGPT."}), 409
        if valor and iald_motores.plano_de(conta) == iald_motores.GRATUITO:
            return jsonify({"error": "Conta do plano gratuito não é ampliada: troque o plano para "
                                     "Assinante primeiro (coluna Plano)."}), 409
        if valor:
            conta["acesso_nativa"] = True
        else:
            conta.pop("acesso_nativa", None)
            # 21/09/2026: o claude também exige conta ampliada — a escolha "claude" sai junto
            if conta.get("motor") in (iald_motores.NATIVA, iald_motores.CLAUDE):
                conta.pop("motor", None)          # a escolha antiga não fica pendurada
        save_users(usuarios)
        efetivo = _motor_efetivo(conta, username)
    auth_log("ADMIN_ACESSO_NATIVA", session.get("username", "?"),
             f"user={username} acesso={'nativa+chatgpt' if valor else 'chatgpt'}")
    return jsonify({"ok": True, "acesso_nativa": valor, "motor_efetivo": efetivo})


@app.route("/admin/api/users/<username>/plano", methods=["PUT"])
def admin_definir_plano(username):
    """Fixa o plano de uma conta (gratuito/assinante/operador) ou volta à regra ("" =
    admin → operador, demais → assinante). 14/09/2026, noite."""
    check = require_admin()
    if check:
        return check
    dados = request.get_json(silent=True)
    plano = dados.get("plano") if isinstance(dados, dict) else None
    if not isinstance(plano, str) or plano.strip().lower() not in ("",) + iald_motores.PLANOS:
        return jsonify({"error": "Plano inválido: use gratuito, assinante, operador ou vazio (regra)."}), 400
    plano = plano.strip().lower()
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        if username not in usuarios:
            return jsonify({"error": f"Usuário '{username}' não encontrado"}), 404
        if plano:
            usuarios[username]["plano"] = plano
        else:
            usuarios[username].pop("plano", None)
        save_users(usuarios)
        registro = usuarios[username]
        efetivo = iald_motores.plano_de(registro)
        motor_efetivo = _motor_efetivo(registro, username)
    auth_log("ADMIN_PLANO", session.get("username", "?"), f"user={username} plano={plano or 'regra'}")
    return jsonify({"ok": True, "plano": plano, "plano_efetivo": efetivo, "motor_efetivo": motor_efetivo})


def _bloquear_conta(username, bloquear, nota, operador, via_central=False):
    """Corpo do bloqueio/desbloqueio — o MESMO para o painel e para a Central (21/09/2026).

    Sob _TRAVA_USUARIOS, como antes. Sem request/session. Devolve (corpo, status_http).
    via_central=True: conta de administrador é PROTEGIDA (nem bloqueia nem desbloqueia pela Central)
    e a ordem é idempotente (conta já no estado pedido → ok sem gravar, "sem_mudanca").
    """
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        conta = usuarios.get(username)
        if not conta:
            return {"error": f"Usuário '{username}' não encontrado"}, 404
        if via_central:
            if conta.get("admin"):
                return {"error": "Conta protegida (administrador): não se bloqueia nem desbloqueia pela Central."}, 409
            if _conta_bloqueada(conta) == bloquear:
                return {"ok": True, "username": username, "bloqueado": bloquear, "sem_mudanca": True}, 200
        if bloquear:
            if not via_central and username == operador:
                return {"error": "Você não pode bloquear a si mesmo"}, 400
            ativos = [u for u, d in usuarios.items() if d.get("admin") and not _conta_bloqueada(d)]
            if conta.get("admin") and ativos == [username]:
                return {"error": "Não se bloqueia o último administrador"}, 400
            conta["bloqueado"] = {"em": datetime.now().isoformat(timespec="seconds"), "por": operador,
                                  "nota": nota}
        else:
            conta.pop("bloqueado", None)
        save_users(usuarios)
    return {"ok": True, "username": username, "bloqueado": bloquear}, 200


@app.route("/admin/api/users/<username>/bloquear", methods=["POST"])
def admin_bloquear_usuario(username):
    """Bloqueia ({bloqueado: true, nota}) ou desbloqueia ({bloqueado: false}) uma conta.

    Bloqueada, a conta perde o token do app e a sessão da web na hora (403), não entra por
    Apple, Google ou senha, e volta a entrar se o operador desbloquear. 14/09/2026, noite.
    21/09/2026: o corpo virou _bloquear_conta (o mesmo caminho da Central); só JSON.
    """
    check = require_admin()
    if check:
        return check
    if not request.is_json:              # 21/09/2026: só JSON (ver _exige_json)
        return _exige_json()
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not isinstance(dados.get("bloqueado"), bool):
        return jsonify({"error": "Informe bloqueado: true ou false."}), 400
    bloquear = dados["bloqueado"]
    nota = str(dados.get("nota") or "")[:200]
    operador = session.get("username", "?")
    corpo, status = _bloquear_conta(username, bloquear, nota, operador)
    if status == 200:
        auth_log("ADMIN_BLOQUEIO" if bloquear else "ADMIN_DESBLOQUEIO", operador, f"user={corpo['username']}")
    return jsonify(corpo), status


@app.route("/admin/api/entrada", methods=["GET"])
def admin_entrada_estado():
    """Estado da porta aberta: o configurado, o que vale de fato e as criações em 24 h."""
    check = require_admin()
    if check:
        return check
    aberta, motivo = _estado_entrada()
    publico = _avaliar_entrada()[2] if ENTRADA_ABERTA and not aberta else ""
    desde = (datetime.now() - timedelta(hours=24)).isoformat(timespec="seconds")
    try:
        criacoes, erro = PEDIDOS.contar_criacoes(desde), ""
    except Exception as exc:      # noqa: BLE001
        criacoes, erro = None, f"pedidos ilegíveis: {exc}"
    return jsonify({
        "aberta_config": ENTRADA_ABERTA, "aberta_efetiva": aberta, "motivo": motivo,
        # 14/09/2026 (noite): o mesmo texto que o público lê em /api/entrar/config
        "motivo_fechada": publico,
        "criacoes_24h": criacoes, "erro": erro,
        "limites": {"por_ip_24h": NOVAS_POR_IP_24H, "global_24h": NOVAS_GLOBAL_24H},
        "streams_gratuito": GRATUITO_STREAMS_SIMULTANEOS,
        "moderacao": {"ligada": MODERACAO_LIGADA, "se_falhar": MODERACAO_FALHA,
                      "entrada_sem_moderacao": ENTRADA_SEM_MODERACAO},
        "tetos_usd_dia": {"global": MOTORES_CFG.cota_global_usd,
                          "global_gratuito": MOTORES_CFG.cota_global_gratuito_usd},
    })


@app.route("/admin/api/denuncias", methods=["GET"])
def admin_denuncias_listar():
    check = require_admin()
    if check:
        return check
    try:
        return jsonify({"denuncias": DENUNCIAS.listar(), "contagem": DENUNCIAS.contagem()})
    except Exception as exc:      # noqa: BLE001 — arquivo corrompido é falha visível
        return jsonify({"error": f"registro de denúncias ilegível: {exc}"}), 500


@app.route("/admin/api/denuncias/<did>/resolver", methods=["POST"])
def admin_denuncias_resolver(did):
    check = require_admin()
    if check:
        return check
    dados = request.get_json(silent=True)
    nota = str((dados or {}).get("nota") or "") if isinstance(dados, dict) else ""
    try:
        feita = DENUNCIAS.resolver(did, session.get("username", "?"), nota)
    except Exception as exc:      # noqa: BLE001
        return jsonify({"error": f"registro de denúncias ilegível: {exc}"}), 500
    if not feita:
        return jsonify({"error": "Denúncia não encontrada"}), 404
    auth_log("DENUNCIA_RESOLVIDA", session.get("username", "?"), f"id={did}")
    return jsonify({"ok": True})


def _limites_para_painel(cfg, plano):
    try:
        return iald_motores.limites_do_plano(cfg, plano)
    except (ValueError, TypeError, KeyError) as exc:
        return {"erro": str(exc)}


@app.route("/admin/api/motor", methods=["GET"])
def admin_motor_estado():
    """Estado do motor externo e gasto dos últimos dias. A chave NUNCA sai daqui."""
    check = require_admin()
    if check:
        return check
    cfg = MOTORES_CFG
    try:
        resumo, erro = RAZAO_OPENAI.resumo(7), ""
    except Exception as exc:      # noqa: BLE001
        resumo, erro = {}, f"razão de uso ilegível: {exc}"
    try:
        gasto_modelos = _guarda_openai().by_model_today()
    except Exception:
        gasto_modelos = None
        erro = (erro + "; " if erro else "") + "gasto por modelo indisponível"
    return jsonify({
        "gasto_por_modelo_hoje": gasto_modelos,
        "chave_definida": bool(cfg.chave), "prompt_sha256": PROMPT_EXTERNO_SHA,
        "motor_padrao": cfg.motor_padrao, "motor_operador": cfg.motor_operador,
        "modelo": cfg.modelo, "modelo_operador": cfg.modelo_operador,
        "indisponivel": _motor_externo_indisponivel(cfg.modelo),
        "cotas_usd_dia": {"conta": cfg.cota_usuario_usd, "operador": cfg.cota_operador_usd,
                          "global": cfg.cota_global_usd, "global_gratuito": cfg.cota_global_gratuito_usd},
        # 14/09/2026 (noite): os limites de cada plano, já com o US$/dia resolvido
        "planos": {p: _limites_para_painel(cfg, p) for p in iald_motores.PLANOS},
        "modelo_gratuito": iald_motores.modelo_para({"plano": iald_motores.GRATUITO}, cfg),
        "ferramentas": sorted(cfg.ferramentas), "janela": cfg.janela,
        "reserva_nativa": cfg.reserva_nativa, "avisos": cfg.avisos,
        "uso_por_dia_utc": resumo, "erro": erro,
        "memoria_modo": cfg.memoria_modo,
        "kernel": KERNEL_EXTERNO.status() if KERNEL_EXTERNO else None,
        "reservas_de_gasto": GUARDA_OPENAI.summary() if GUARDA_OPENAI else [],
        # 14/09/2026 (noite): o modelo que responde HOJE (com a troca automática), as trocas que
        # valem nos próximos 30 dias, se o gratuito consulta o Atlas e as cobranças acima da reserva
        "modelo_efetivo": iald_motores.modelo_efetivo(cfg.modelo, cfg),
        "trocas_previstas": iald_motores.trocas_previstas(cfg),
        "gratuito_atlas": cfg.gratuito_atlas,
        "cobrancas_acima_da_reserva": _cobrancas_acima_da_reserva(),
        # 21/09/2026: o motor claude (configuração, lista, tetos e gasto de hoje). A chave NUNCA sai:
        # só se existe.
        "claude": _estado_claude_para_painel(),
    })


def _estado_claude_para_painel():
    """O bloco "claude" do /admin/api/motor. Lê o razão e as reservas do claude SEM criá-los."""
    cfg = CLAUDE_CFG
    erro = ""
    try:
        _conta, gasto_global = RAZAO_CLAUDE.gasto_hoje("")
    except Exception as exc:      # noqa: BLE001 — falha visível, nunca "0" falso
        gasto_global, erro = None, f"razão do claude ilegível: {exc}"
    try:
        guarda = _guarda_claude(criar=False)
        gasto_modelos = guarda.by_model_today() if guarda else []
        acima = guarda.exceeded_summary() if guarda else []
    except Exception as exc:      # noqa: BLE001
        gasto_modelos, acima = None, [{"erro": f"reservas do claude ilegíveis: {exc}"}]
        erro = (erro + "; " if erro else "") + "reservas do claude ilegíveis"
    return {
        "chave_definida": bool(cfg.chave),
        "sdk_instalado": _sdk_claude_presente(),
        "modelo": cfg.modelo,
        "contas": sorted(cfg.contas),
        "indisponivel": _motor_externo_indisponivel(cfg.modelo, cfg),
        "cotas_usd_dia": {"conta": cfg.cota_usuario_usd, "operador": cfg.cota_operador_usd,
                          "global": cfg.cota_global_usd},
        "gasto_hoje_usd": gasto_global,
        "gasto_por_modelo_hoje": gasto_modelos,
        "cobrancas_acima_da_reserva": acima,
        "janela_o200k": cfg.janela, "max_saida": cfg.max_saida, "esforco": cfg.esforco_claude,
        "cache_ttl": cfg.cache_ttl, "fator_tokens": cfg.fator_tokens,
        "precos": list(cfg.precos(cfg.modelo) or ()), "avisos": list(cfg.avisos),
        "erro": erro,
    }


def _cobrancas_acima_da_reserva():
    try:
        return GUARDA_OPENAI.exceeded_summary() if GUARDA_OPENAI else []
    except Exception as exc:          # noqa: BLE001 — o painel mostra o erro, não esconde
        return [{"erro": f"reservas ilegíveis: {exc}"}]


# ── SALDO DE CRÉDITO DA OPENAI no painel (15/09/2026) ──
@app.route("/admin/api/saldo_openai", methods=["GET"])
def admin_saldo_openai():
    """O contador da aba AGI. A chave de administrador NUNCA sai daqui (só se existe)."""
    check = require_admin()
    if check:
        return check
    estado = dict(SALDO_OPENAI.estado(forcar=request.args.get("atualizar") == "1"))
    estado["chave_admin_definida"] = bool(SALDO_OPENAI.chave_atual())
    return jsonify(estado)


def _corpo_saldo():
    if not request.is_json:
        return None, (jsonify({"error": "Envie application/json."}), 415)
    return (request.get_json(silent=True) or {}), None


@app.route("/admin/api/saldo_openai/ancora", methods=["POST"])
def admin_saldo_openai_ancora():
    """O operador informa o saldo que leu no painel da OpenAI (e, se quiser, quando leu)."""
    check = require_admin()
    if check:
        return check
    dados, erro = _corpo_saldo()
    if erro:
        return erro
    try:
        estado = SALDO_OPENAI.registrar_ancora(dados.get("valor_usd"), por=session.get("username", ""),
                                               em=dados.get("em") or None)
    except (ValueError, iald_saldo_openai.SaldoIlegivel) as exc:
        return jsonify({"error": str(exc)}), 400
    auth_log("SALDO_OPENAI_ANCORA", session.get("username", "?"), f"valor_usd={estado.get('saldo_usd')}")
    return jsonify(estado)


@app.route("/admin/api/saldo_openai/compra", methods=["POST"])
def admin_saldo_openai_compra():
    """O operador registra uma compra de crédito feita na OpenAI."""
    check = require_admin()
    if check:
        return check
    dados, erro = _corpo_saldo()
    if erro:
        return erro
    try:
        estado = SALDO_OPENAI.registrar_compra(dados.get("valor_usd"), por=session.get("username", ""),
                                               em=dados.get("em") or None, nota=dados.get("nota") or "")
    except (ValueError, iald_saldo_openai.SaldoIlegivel) as exc:
        return jsonify({"error": str(exc)}), 400
    auth_log("SALDO_OPENAI_COMPRA", session.get("username", "?"), f"valor_usd={dados.get('valor_usd')}")
    return jsonify(estado)


@app.route("/admin/api/saldo_openai/limites", methods=["PUT"])
def admin_saldo_openai_limites():
    check = require_admin()
    if check:
        return check
    dados, erro = _corpo_saldo()
    if erro:
        return erro
    try:
        estado = SALDO_OPENAI.definir_limites(**{k: dados.get(k) for k in
                                                ("critico_usd", "atencao_usd", "critico_dias", "atencao_dias")})
    except (ValueError, iald_saldo_openai.SaldoIlegivel) as exc:
        return jsonify({"error": str(exc)}), 400
    auth_log("SALDO_OPENAI_LIMITES", session.get("username", "?"), json.dumps(estado.get("limites")))
    return jsonify(estado)


# ── SALDO DE CRÉDITO DA ANTHROPIC (CLAUDE) no painel (22/09/2026) — o mesmo contador da OpenAI ──
@app.route("/admin/api/saldo_claude", methods=["GET"])
def admin_saldo_claude():
    """O cartão do crédito do Claude na aba AGI. Nenhuma chave sai daqui."""
    check = require_admin()
    if check:
        return check
    estado = dict(SALDO_CLAUDE.estado(forcar=request.args.get("atualizar") == "1"))
    estado["claude_configurado"] = bool(getattr(CLAUDE_CFG, "chave", ""))
    estado["chave_admin_definida"] = bool(SALDO_CLAUDE.chave_atual())
    return jsonify(estado)


@app.route("/admin/api/saldo_claude/ancora", methods=["POST"])
def admin_saldo_claude_ancora():
    """O operador informa o saldo que leu em platform.claude.com › Settings › Billing."""
    check = require_admin()
    if check:
        return check
    dados, erro = _corpo_saldo()
    if erro:
        return erro
    try:
        estado = SALDO_CLAUDE.registrar_ancora(dados.get("valor_usd"), por=session.get("username", ""),
                                               em=dados.get("em") or None)
    except (ValueError, iald_saldo_openai.SaldoIlegivel) as exc:
        return jsonify({"error": str(exc)}), 400
    auth_log("SALDO_CLAUDE_ANCORA", session.get("username", "?"), f"valor_usd={estado.get('saldo_usd')}")
    return jsonify(estado)


@app.route("/admin/api/saldo_claude/compra", methods=["POST"])
def admin_saldo_claude_compra():
    """O operador registra uma compra de crédito feita na Anthropic."""
    check = require_admin()
    if check:
        return check
    dados, erro = _corpo_saldo()
    if erro:
        return erro
    try:
        estado = SALDO_CLAUDE.registrar_compra(dados.get("valor_usd"), por=session.get("username", ""),
                                               em=dados.get("em") or None, nota=dados.get("nota") or "")
    except (ValueError, iald_saldo_openai.SaldoIlegivel) as exc:
        return jsonify({"error": str(exc)}), 400
    auth_log("SALDO_CLAUDE_COMPRA", session.get("username", "?"), f"valor_usd={dados.get('valor_usd')}")
    return jsonify(estado)


@app.route("/admin/api/saldo_claude/limites", methods=["PUT"])
def admin_saldo_claude_limites():
    check = require_admin()
    if check:
        return check
    dados, erro = _corpo_saldo()
    if erro:
        return erro
    try:
        estado = SALDO_CLAUDE.definir_limites(**{k: dados.get(k) for k in
                                                ("critico_usd", "atencao_usd", "critico_dias", "atencao_dias")})
    except (ValueError, iald_saldo_openai.SaldoIlegivel) as exc:
        return jsonify({"error": str(exc)}), 400
    auth_log("SALDO_CLAUDE_LIMITES", session.get("username", "?"), json.dumps(estado.get("limites")))
    return jsonify(estado)


@app.route("/api/alertas", methods=["GET"])
def api_alertas():
    # Compatibility for installed clients: internal operations stay in /admin.
    return jsonify({"alertas": []})


@app.route("/admin/api/prazos", methods=["GET"])
def admin_prazos():
    check = require_admin()
    if check:
        return check
    from iald_deadlines import snapshot
    response = jsonify({"prazos": snapshot(os.path.join(SERVE_DIR, "iald_deadlines.json"))})
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/admin/api/users", methods=["POST"])
def admin_create_user():
    check = require_admin()
    if check:
        return check
    global USERS
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()
    is_admin = data.get("admin", False)
    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios"}), 400
    if len(username) < 3:
        return jsonify({"error": "Usuário deve ter pelo menos 3 caracteres"}), 400
    if not identidade.usuario_valido(username):
        return jsonify({"error": "Usuário inválido: 3 a 32 caracteres, minúsculas, números, '.', '_' ou '-'"}), 400
    if len(password) < 6:
        return jsonify({"error": "Senha deve ter pelo menos 6 caracteres"}), 400
    # 14/09/2026 (noite): o hash (lento de propósito) sai de dentro da trava
    novo_hash = generate_password_hash(password)
    with _TRAVA_USUARIOS:
        USERS = _carregar_usuarios_para_escrita()
        if username in USERS:
            return jsonify({"error": f"Usuário '{username}' já existe"}), 409
        USERS[username] = {"password_hash": novo_hash,
                           "admin": bool(is_admin), "sacred_language": False,
                           "created": datetime.now().isoformat()}
        if not is_admin and data.get("acesso_nativa") is True:
            USERS[username]["acesso_nativa"] = True       # 15/09/2026: conta ampliada
        save_users(USERS)
    auth_log("ADMIN_CREATE_USER", session.get("username", "?"), f"new_user={username}")
    return jsonify({"ok": True, "username": username})


@app.route("/admin/api/users/<username>", methods=["DELETE"])
def admin_delete_user(username):
    check = require_admin()
    if check:
        return check
    global USERS
    username = username.strip().lower()
    # 14/09/2026 (noite): {"bloquear": true, "nota"} põe as entradas (Apple/Google) da
    # conta na lista de recusados. Sem isso, com a porta aberta, o excluído volta sozinho
    # (com a cota já usada preservada, mas volta). Sem corpo = exclusão de sempre.
    corpo = request.get_json(silent=True)
    bloquear = isinstance(corpo, dict) and corpo.get("bloquear") is True
    nota = str(corpo.get("nota") or "")[:200] if isinstance(corpo, dict) else ""
    with _TRAVA_USUARIOS:          # revisão de segurança: leitura para escrita e gravação sob a trava
        USERS = _carregar_usuarios_para_escrita()
        if username not in USERS:
            return jsonify({"error": f"Usuário '{username}' não encontrado"}), 404
        if username == session.get("username"):
            return jsonify({"error": "Você não pode remover a si mesmo"}), 400
        if USERS[username].get("admin") and sum(1 for d in USERS.values() if d.get("admin")) <= 1:
            return jsonify({"error": "Não se remove o último administrador"}), 400
        identidades_removidas = identidade.identidades_publicas(USERS[username])
        try:
            PEDIDOS.retirar_nome(username)     # lápide antes de apagar (BAIXO 3)
        except (OSError, ValueError) as exc:
            return jsonify({"error": f"Lápide do nome não gravada ({exc}); nada foi apagado."}), 503
        CHAT_JOBS().purge(username)
        PURGE_PUSH(username)
        del USERS[username]
        save_users(USERS)
    # 14/09/2026: quem é excluído e tenta voltar abre pedido NOVO, pendente
    PEDIDOS.encerrar_do_usuario(username, identidades_removidas)
    bloqueadas = 0
    if bloquear:
        bloqueadas = PEDIDOS.bloquear_identidades(identidades_removidas, session.get("username", "?"),
                                                  nota or "bloqueada ao excluir a conta")
    auth_log("ADMIN_DELETE_USER", session.get("username", "?"),
             f"deleted={username}" + (f" identidades_bloqueadas={bloqueadas}" if bloquear else ""))
    return jsonify({"ok": True, "bloqueio": {"pedido": bloquear, "pedidos_alterados": bloqueadas}})


@app.route("/admin/api/users/<username>/password", methods=["PUT"])
def admin_change_password(username):
    check = require_admin()
    if check:
        return check
    global USERS
    username = username.strip().lower()
    data = request.get_json(silent=True) or {}
    new_password = data.get("password", "").strip()
    if len(new_password) < 6:
        return jsonify({"error": "Senha deve ter pelo menos 6 caracteres"}), 400
    novo_hash = generate_password_hash(new_password)      # fora da trava (lento de propósito)
    with _TRAVA_USUARIOS:
        USERS = _carregar_usuarios_para_escrita()
        if username not in USERS:
            return jsonify({"error": f"Usuário '{username}' não encontrado"}), 404
        USERS[username]["password_hash"] = novo_hash
        save_users(USERS)
    auth_log("ADMIN_CHANGE_PW", session.get("username", "?"), f"user={username}")
    return jsonify({"ok": True})


@app.route("/admin/api/users/<username>/sacred", methods=["PUT"])
def admin_toggle_sacred(username):
    """Toggle sacred language flag for a user."""
    check = require_admin()
    if check:
        return check
    global USERS
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        USERS = _carregar_usuarios_para_escrita()
        if username not in USERS:
            return jsonify({"error": f"Usuário '{username}' não encontrado"}), 404
        current = USERS[username].get("sacred_language", False)
        USERS[username]["sacred_language"] = not current
        save_users(USERS)
    auth_log("ADMIN_TOGGLE_SACRED", session.get("username", "?"),
             f"user={username} sacred={not current}")
    return jsonify({"ok": True, "sacred_language": not current})


@app.route("/admin/api/users/export", methods=["GET"])
def admin_export_users():
    """Export users report as JSON."""
    check = require_admin()
    if check:
        return check
    USERS_EXP = load_users_estrito()     # ilegível → 503 (não um relatório vazio)
    report = []
    for username in sorted(USERS_EXP.keys()):
        data = USERS_EXP[username]
        entry = {
            "username": username,
            "admin": data.get("admin", False),
            "sacred_language": data.get("sacred_language", False),
            "tgl_hash": generate_tgl_hash(username),
            "created": data.get("created", ""),
        }
        # Add TGLC balance if available
        if COIN_AVAILABLE:
            try:
                info = coin_engine.get_account_info(username)
                entry["tglc_balance"] = info.get("balance", 0)
                entry["tglc_tx_count"] = info.get("tx_count", 0)
            except Exception:
                pass
        report.append(entry)
    return jsonify({
        "report": report,
        "total_users": len(report),
        "generated": datetime.now().isoformat(),
    })


# ══════════════════════════════════════════════════════════════
# ADMIN API — System Monitor (NEW in v7)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/system")
def admin_api_system():
    check = require_admin()
    if check:
        return check
    result = system_monitor.get_all()
    result['science_update'] = science_update_hook.admin_status(
        os.path.join(SERVE_DIR, '.iald_runtime', 'science_update', 'status.json'))
    return jsonify(result)


# ══════════════════════════════════════════════════════════════
# ADMIN API — Logs (NEW in v7)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/logs")
def admin_api_logs():
    check = require_admin()
    if check:
        return check
    n = min(int(request.args.get("n", "50")), 500)
    return jsonify({"logs": log_buffer.get(n), "count": n})


# ══════════════════════════════════════════════════════════════
# ADMIN API — Control (NEW in v7)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/clear-sessions", methods=["POST"])
def admin_api_clear_sessions():
    check = require_admin()
    if check:
        return check
    admin_user = session.get("username", "")
    new_key = secrets.token_hex(32)
    app.secret_key = new_key
    try:
        with open(SECRET_KEY_FILE, "w") as f:
            f.write(new_key)
    except Exception:
        pass
    session.permanent = True
    session["authenticated"] = True
    session["username"] = admin_user
    session["is_admin"] = True
    session["last_active"] = datetime.now().isoformat()
    auth_log("SESSIONS_CLEARED", admin_user)
    return jsonify({"ok": True, "message": "Todas as sessões foram invalidadas (exceto a sua)"})


@app.route("/admin/api/test-prompt", methods=["POST"])
def admin_api_test_prompt():
    return app_memory.dispatch_admin(SERVE_DIR, _chat_account_generation, require_admin, _admin_api_test_prompt_with_memory)


def _admin_api_test_prompt_with_memory():
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt vazio"}), 400
    payload = {"model": "local", "messages": [
        {"role": "system", "content": "You are IALD. Respond concisely in Portuguese."},
        {"role": "user", "content": prompt}],
        "stream": False, "max_tokens": 512, "temperature": 0.7}
    t0 = time.time()
    try:
        payload = _operational_native_payload(payload)
        r = app_memory.http_call('model.native.operational', req_lib.post, f"{LLAMA_URL}/v1/chat/completions", json=payload, timeout=60)
        duration_ms = int((time.time() - t0) * 1000)
        if r.status_code != 200:
            return jsonify({"error": f"llama-server retornou {r.status_code}", "body": r.text}), 502
        resp_data = r.json()
        content = ""
        try:
            content = resp_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            content = str(resp_data)
        usage = resp_data.get("usage", {})
        log_request(session.get("username", "?"), "/admin/api/test-prompt", "POST",
                    tokens_in=usage.get("prompt_tokens", 0),
                    tokens_out=usage.get("completion_tokens", 0),
                    duration_ms=duration_ms, status="test")
        return jsonify({"response": content, "duration_ms": duration_ms, "usage": usage})
    except Exception as e:
        return jsonify({"error": str(e)}), 502


# ══════════════════════════════════════════════════════════════
# ADMIN API — TGL COIN BANK (Banco Central da AGI)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/bank/stats")
def admin_bank_stats():
    check = require_admin()
    if check:
        return check
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin nao disponivel"}), 503
    return jsonify(coin_engine.get_ledger_stats())


@app.route("/admin/api/bank/verificar-cadeia")
def admin_bank_verificar_cadeia():
    """
    Confere os selos encadeados do razão (02/08/2026).

    Relatório HONESTO: as transações anteriores a esta data não têm `seal_v2` e são
    contadas como NÃO VERIFICÁVEIS — porque de fato não são. O `hash` legado delas
    usava um hash artesanal e, no caso dos airdrops, um nonce que nunca foi gravado.
    """
    check = require_admin()
    if check:
        return check
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin indisponível"}), 503
    from tgl_coin_engine import verificar_cadeia
    coin_engine._refresh_from_disk()
    rel = verificar_cadeia(coin_engine._ledger)
    rel["nota"] = ("Transações anteriores a 02/08/2026 não têm selo verificável; "
                   "o hash legado era artesanal e, nos airdrops, irreproduzível.")
    return jsonify(rel), 200


@app.route("/admin/api/bank/accounts")
def admin_bank_accounts():
    check = require_admin()
    if check:
        return check
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin nao disponivel"}), 503
    accounts = []
    for username in coin_engine._ledger.get("accounts", {}):
        info = coin_engine.get_account_info(username)
        accounts.append(info)
    accounts.sort(key=lambda a: a["balance"], reverse=True)
    return jsonify({"accounts": accounts})


@app.route("/admin/api/bank/transactions")
def admin_bank_transactions():
    check = require_admin()
    if check:
        return check
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin nao disponivel"}), 503
    limit = min(int(request.args.get("n", "50")), 200)
    txs = list(reversed(coin_engine._ledger.get("transactions", [])[-limit:]))
    return jsonify({"transactions": txs, "total": coin_engine._ledger.get("total_transactions", 0)})


@app.route("/admin/api/bank/transfer", methods=["POST"])
def admin_bank_transfer():
    """Admin transfer — can transfer between any accounts."""
    check = require_admin()
    if check:
        return check
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin nao disponivel"}), 503
    data = request.get_json(silent=True) or {}
    from_user = data.get("from", "").strip().lower()
    to_user = data.get("to", "").strip().lower()
    amount = data.get("amount", 0)
    note = data.get("note", f"Transferencia admin por {session.get('username', '?')}")
    if not from_user or not to_user:
        return jsonify({"error": "Remetente e destinatario obrigatorios"}), 400
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Valor invalido"}), 400
    ok, receipt = coin_engine.transfer(from_user=from_user, to_user=to_user,
                                       amount=float(amount), note=note)
    if ok:
        auth_log("BANK_TRANSFER", session.get("username", "?"),
                 f"{from_user}->{to_user} {amount} TGLC")
        return jsonify({"ok": True, "receipt": receipt})
    return jsonify({"error": receipt.get("error", "Erro")}), 400


@app.route("/admin/api/bank/airdrop", methods=["POST"])
def admin_bank_airdrop():
    """Admin airdrop — give coins to a user from GENESIS."""
    check = require_admin()
    if check:
        return check
    if not COIN_AVAILABLE:
        return jsonify({"error": "TGL Coin nao disponivel"}), 503
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip().lower()
    amount = data.get("amount", 0)
    if not username:
        return jsonify({"error": "Usuario obrigatorio"}), 400
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Valor invalido"}), 400
    # Direct credit (admin privilege)
    coin_engine.ensure_account(username)
    account = coin_engine._ledger["accounts"][username]
    from tgl_coin_engine import _round_amount, _generate_tx_id, _compute_tx_hash, DECIMALS
    import secrets as _secrets
    balance_before = account["balance"]
    account["balance"] = _round_amount(account["balance"] + float(amount))
    account["total_received"] = _round_amount(account["total_received"] + float(amount))
    account["tx_count"] += 1
    tx_id = _generate_tx_id()
    timestamp = datetime.now().isoformat()
    tx_hash = _compute_tx_hash(tx_id, "ADMIN_AIRDROP", username, float(amount),
                                timestamp, 0.0, _secrets.token_bytes(16))
    # Usa o ponto único de gravação, que carimba o selo v2 encadeado (02/08/2026).
    coin_engine._anexar_transacao({
        "tx_id": tx_id, "type": "admin_airdrop",
        "from": "ADMIN_AIRDROP", "to": username,
        "amount": float(amount), "fee": 0.0,
        "timestamp": timestamp, "hash": tx_hash,
        "balance_after_recipient": account["balance"],
        "status": "confirmed",
        "note": f"Airdrop admin por {session.get('username', '?')}",
    })
    coin_engine._ledger["total_supply"] = _round_amount(
        coin_engine._ledger["total_supply"] + float(amount))
    coin_engine._ledger["total_transactions"] += 1
    coin_engine._save()
    auth_log("BANK_AIRDROP", session.get("username", "?"),
             f"{username} +{amount} TGLC")
    return jsonify({"ok": True, "username": username,
                    "amount": amount, "balance": account["balance"]})


# ══════════════════════════════════════════════════════════════
# ADMIN API — PSI-NET (Rede Holográfica)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/psinet/stats")
def admin_psinet_stats():
    check = require_admin()
    if check:
        return check
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET nao disponivel"}), 503
    return jsonify(psinet_engine.get_stats())


@app.route("/admin/api/psinet/config", methods=["GET"])
def admin_psinet_config_get():
    check = require_admin()
    if check:
        return check
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET nao disponivel"}), 503
    return jsonify(psinet_engine.get_config())


@app.route("/admin/api/psinet/config", methods=["POST"])
def admin_psinet_config_set():
    check = require_admin()
    if check:
        return check
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET nao disponivel"}), 503
    data = request.get_json(silent=True) or {}
    if "max_file_size_mb" in data:
        psinet_engine.set_max_file_size(float(data["max_file_size_mb"]))
    if "transfer_timeout_hours" in data:
        psinet_engine.set_timeout_hours(float(data["transfer_timeout_hours"]))
    if "transfer_cost_tglc" in data:
        psinet_engine.set_transfer_cost(float(data["transfer_cost_tglc"]))
    auth_log("PSINET_CONFIG", session.get("username", "?"),
             json.dumps(data, ensure_ascii=False)[:200])
    return jsonify({"ok": True, "config": psinet_engine.get_config()})


@app.route("/admin/api/psinet/pending")
def admin_psinet_pending():
    check = require_admin()
    if check:
        return check
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET nao disponivel"}), 503
    all_transfers = []
    from psinet_engine import PENDING_DIR as _PD
    if os.path.isdir(_PD):
        for tx_id in os.listdir(_PD):
            m = psinet_engine.get_transfer_info(tx_id)
            if m:
                all_transfers.append(m)
    all_transfers.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return jsonify({"transfers": all_transfers})


@app.route("/admin/api/psinet/send", methods=["POST"])
def admin_psinet_send():
    """Admin file send via PSI-NET."""
    check = require_admin()
    if check:
        return check
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET nao disponivel"}), 503
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    f = request.files["file"]
    from_user = request.form.get("from_user", session.get("username", "")).strip().lower()
    to_user = request.form.get("to_user", "").strip().lower()
    note = request.form.get("note", "")
    if not to_user:
        return jsonify({"error": "Destinatario obrigatorio"}), 400
    file_bytes = f.read()
    filename = f.filename or "arquivo"
    ok, result = psinet_engine.send(from_user, to_user, filename, file_bytes, note)
    if ok:
        auth_log("PSINET_SEND", session.get("username", "?"),
                 f"{from_user}->{to_user} {filename} ({len(file_bytes)} bytes)")
        return jsonify({"ok": True, "result": result})
    return jsonify({"error": result.get("error", "Erro")}), 400


@app.route("/admin/api/psinet/cleanup", methods=["POST"])
def admin_psinet_cleanup():
    check = require_admin()
    if check:
        return check
    if not PSINET_AVAILABLE:
        return jsonify({"error": "PSI-NET nao disponivel"}), 503
    removed = psinet_engine.cleanup_expired()
    return jsonify({"ok": True, "removed": removed})


@app.route("/psinet/download/<filename>")
def psinet_download(filename):
    """
    Serve um arquivo PSI-NET recebido, APENAS ao seu destinatário.

    CORRIGIDO 02/08/2026 (IDOR). A versão anterior validava só path traversal e
    servia de um diretório PLANO compartilhado por todos os usuários: bastava
    conhecer (ou adivinhar) o nome do arquivo — que tem formato previsível,
    "AAAAMMDD_HHMMSS_nome" — para qualquer usuário autenticado baixar a
    transferência de qualquer outro. Agora cada destinatário tem sua subpasta e
    esta rota só enxerga a do usuário da sessão.
    """
    if ".." in filename or "/" in filename or "\\" in filename:
        return Response("Acesso negado.", status=403)
    user = session.get("username")
    if not user:
        return Response("Nao autenticado.", status=401)
    import psinet_engine as pe
    received_dir = os.path.join(pe.PSINET_DIR, "received", user.strip().lower())
    filepath = os.path.join(received_dir, filename)
    if not os.path.isfile(filepath):
        auth_log("PSINET_DOWNLOAD_MISS", user, f"arquivo={filename}")
        return Response("Arquivo nao encontrado.", status=404)
    auth_log("PSINET_DOWNLOAD", user, f"arquivo={filename}")
    return send_from_directory(received_dir, filename, as_attachment=True)


# ══════════════════════════════════════════════════════════════
# PSION HEARTBEAT API — Dashboard endpoints
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
# MEMÓRIA DO OPERADOR — CRUD (02/08/2026)
# O operador cria e gere os fatos que a IALD carrega em toda conversa.
# Só localhost + admin (require_admin), como o resto da Central de Comando.
# ══════════════════════════════════════════════════════════════

def _kernel_gravar(conteudo, quem, motivo=""):
    """Backup de BYTES -> escrita atomica (.tmp + os.replace) -> invalida o cache.
    Nunca open(w) direto: um write que falha depois do open('w') deixa o arquivo VAZIO."""
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = KERNEL_FILE + ".bak_" + ts
        if os.path.exists(KERNEL_FILE):
            with open(KERNEL_FILE, "rb") as f:
                atual = f.read()
            with open(bak, "wb") as f:
                f.write(atual)
            # o textarea manda CRLF; preserva o fim de linha que o arquivo ja usava
            if atual.count(b"\r\n") > atual.count(b"\n") // 2:
                conteudo = conteudo.replace("\r\n", "\n").replace("\n", "\r\n")
            else:
                conteudo = conteudo.replace("\r\n", "\n")
        tmp = KERNEL_FILE + ".tmp_" + ts
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(conteudo)
        if os.path.getsize(tmp) == 0:
            os.remove(tmp)
            return False, "a escrita resultou em arquivo vazio - abortado, kernel intacto"
        os.replace(tmp, KERNEL_FILE)
        _agi_kernel_cache["content"] = None      # recarga a quente, sem reiniciar
        _agi_kernel_cache["mtime"] = 0
        auth_log("KERNEL_EDIT", quem,
                 "backup=%s chars=%d %s" % (os.path.basename(bak), len(conteudo), motivo[:80]))
        return True, {"ok": True, "backup": os.path.basename(bak), "chars": len(conteudo),
                      "linhas": conteudo.count("\n") + 1, "tokens_est": int(len(conteudo) / 2.91)}
    except Exception as e:
        return False, str(e)


@app.route("/admin/api/kernel", methods=["GET"])
def admin_kernel_ler():
    check = require_admin()
    if check:
        return check
    try:
        with open(KERNEL_FILE, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return jsonify({"error": "nao foi possivel ler o kernel: %s" % e}), 500
    base = os.path.basename(KERNEL_FILE)
    baks = sorted([n for n in os.listdir(SERVE_DIR) if n.startswith(base + ".bak_")],
                  reverse=True)[:30]
    return jsonify({
        "arquivo": base,
        "conteudo": conteudo,
        "chars": len(conteudo),
        "linhas": conteudo.count("\n") + 1,
        "tokens_est": int(len(conteudo) / 2.91),
        "mtime": datetime.fromtimestamp(os.path.getmtime(KERNEL_FILE)).isoformat(timespec="seconds"),
        "backups": baks,
    }), 200


@app.route("/admin/api/kernel", methods=["POST"])
def admin_kernel_salvar():
    check = require_admin()
    if check:
        return check
    d = request.get_json(silent=True) or {}
    conteudo = d.get("conteudo")
    if not isinstance(conteudo, str) or not conteudo.strip():
        return jsonify({"error": "conteudo vazio - recusado"}), 400
    if len(conteudo) < 500 and not d.get("forcar"):
        return jsonify({"error": "recusado: menos de 500 chars (mande forcar=true se for mesmo isso)"}), 400
    ok, res = _kernel_gravar(conteudo, session.get("username", "?"), d.get("motivo", ""))
    if not ok:
        return jsonify({"error": res}), 500
    return jsonify(res), 200


@app.route("/admin/api/kernel/restaurar", methods=["POST"])
def admin_kernel_restaurar():
    check = require_admin()
    if check:
        return check
    d = request.get_json(silent=True) or {}
    nome = (d.get("backup") or "").strip()
    base = os.path.basename(KERNEL_FILE)
    if not nome.startswith(base + ".bak_") or "/" in nome or "\\" in nome or ".." in nome:
        return jsonify({"error": "nome de backup invalido"}), 400
    caminho = os.path.join(SERVE_DIR, nome)
    if not os.path.exists(caminho):
        return jsonify({"error": "backup nao encontrado"}), 404
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    ok, res = _kernel_gravar(conteudo, session.get("username", "?"), "restauro de " + nome)
    if not ok:
        return jsonify({"error": res}), 500
    return jsonify(res), 200


@app.route("/admin/api/memoria", methods=["GET"])
def admin_memoria_listar():
    check = require_admin()
    if check:
        return check
    if not MEMORIA_OP_AVAILABLE:
        return jsonify({"error": "Memória do operador indisponível"}), 503
    return jsonify({"fatos": memoria_op.listar(), "custo": memoria_op.custo()}), 200


@app.route("/admin/api/memoria", methods=["POST"])
def admin_memoria_criar():
    check = require_admin()
    if check:
        return check
    if not MEMORIA_OP_AVAILABLE:
        return jsonify({"error": "Memória do operador indisponível"}), 503
    d = request.get_json(silent=True) or {}
    titulo = (d.get("titulo") or "").strip()
    texto = (d.get("texto") or "").strip()
    if not titulo or not texto:
        return jsonify({"error": "titulo e texto são obrigatórios"}), 400
    try:
        f = memoria_op.adicionar(
            titulo, texto,
            escopo=d.get("escopo", "sob_demanda"),
            tags=d.get("tags") or [],
            peso=int(d.get("peso", 3)),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    auth_log("MEMORIA_ADD", session.get("username", "?"), f"id={f['id']} escopo={f['escopo']}")
    return jsonify({"fato": f, "custo": memoria_op.custo()}), 201


@app.route("/admin/api/memoria/<fid>", methods=["PUT"])
def admin_memoria_editar(fid):
    check = require_admin()
    if check:
        return check
    if not MEMORIA_OP_AVAILABLE:
        return jsonify({"error": "Memória do operador indisponível"}), 503
    d = request.get_json(silent=True) or {}
    permitidos = {k: d[k] for k in ("titulo", "texto", "escopo", "tags", "peso", "ativo")
                  if k in d}
    try:
        f = memoria_op.editar(fid, **permitidos)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if not f:
        return jsonify({"error": f"Fato não encontrado: {fid}"}), 404
    auth_log("MEMORIA_EDIT", session.get("username", "?"), f"id={fid}")
    return jsonify({"fato": f, "custo": memoria_op.custo()}), 200


@app.route("/admin/api/memoria/<fid>", methods=["DELETE"])
def admin_memoria_remover(fid):
    check = require_admin()
    if check:
        return check
    if not MEMORIA_OP_AVAILABLE:
        return jsonify({"error": "Memória do operador indisponível"}), 503
    if not memoria_op.remover(fid):
        return jsonify({"error": f"Fato não encontrado: {fid}"}), 404
    auth_log("MEMORIA_DEL", session.get("username", "?"), f"id={fid}")
    return jsonify({"ok": True, "custo": memoria_op.custo()}), 200


@app.route("/admin/api/memoria/bloco", methods=["GET"])
def admin_memoria_bloco():
    """Mostra EXATAMENTE o que é injetado no prompt, e o que a busca recuperaria."""
    check = require_admin()
    if check:
        return check
    if not MEMORIA_OP_AVAILABLE:
        return jsonify({"error": "Memória do operador indisponível"}), 503
    consulta = request.args.get("q", "")
    fixo = memoria_op.bloco_sempre()
    # CALCULA O ORCAMENTO AGORA, em vez de reaproveitar o da ultima compressao.
    # `get_stats()["orcamento_detalhado"]` so e preenchido depois que uma conversa
    # dispara compress_context — num servidor recem-iniciado vinha None e o painel
    # mostrava o campo vazio, que e justamente quando o operador vai olhar.
    try:
        budget_memory = HolographicMemory()
        budget_memory._orcamento_historico([{"role": "system", "content": fixo}])
        orcamento = dict(budget_memory._ultimo_orcamento or {})
    except Exception as e:
        orcamento = {"erro": str(e)}
    return jsonify({
        "bloco_sempre": fixo,
        "bloco_sob_demanda": memoria_op.bloco_sob_demanda(consulta) if consulta else "",
        "custo": memoria_op.custo(),
        "orcamento_contexto": orcamento,
    }), 200


@app.route("/admin/api/heartbeat")
def admin_heartbeat_status():
    """Return Psion Heartbeat status for the admin dashboard."""
    check = require_admin()
    if check:
        return check
    return jsonify(psion_heartbeat.get_status())


@app.route("/admin/api/heartbeat/trigger", methods=["POST"])
def admin_heartbeat_trigger():
    """Manually trigger a heartbeat beat (admin only)."""
    check = require_admin()
    if check:
        return check
    result = heartbeat_cycle()
    return jsonify({"result": result, "status": psion_heartbeat.get_status()})


# ══════════════════════════════════════════════════════════════
# PSION VERBAL API — Correction log & Kernel patches
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/verbal")
def admin_verbal_status():
    """Return Verbal Psion status: corrections, pending patches."""
    check = require_admin()
    if check:
        return check
    return jsonify(get_verbal_status())


@app.route("/admin/api/verbal/corrections")
def admin_verbal_corrections():
    """Return full correction log."""
    check = require_admin()
    if check:
        return check
    log = _load_correction_log()
    corrections = log.get("corrections", [])
    # Return most recent first, limit 100
    return jsonify({"corrections": list(reversed(corrections[-100:]))})


@app.route("/admin/api/verbal/patches")
def admin_verbal_patches():
    """Return all kernel patches."""
    check = require_admin()
    if check:
        return check
    patches = _load_kernel_patches()
    return jsonify(patches)


@app.route("/admin/api/verbal/patches/<patch_id>/approve", methods=["POST"])
def admin_verbal_approve(patch_id):
    """Approve a pending kernel patch."""
    check = require_admin()
    if check:
        return check
    user = session.get("username", "operador")
    ok, msg = approve_kernel_patch(patch_id, approved_by=user)
    return jsonify({"success": ok, "message": msg})


@app.route("/admin/api/verbal/patches/<patch_id>/reject", methods=["POST"])
def admin_verbal_reject(patch_id):
    """Reject a pending kernel patch."""
    check = require_admin()
    if check:
        return check
    ok, msg = reject_kernel_patch(patch_id)
    return jsonify({"success": ok, "message": msg})


# ══════════════════════════════════════════════════════════════
# AGI API — File Explorer (Phase 1: read-only)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/agi/files/roots")
def agi_files_roots():
    """Return the list of allowed root paths."""
    check = require_admin()
    if check:
        return check
    roots = []
    for r in ALLOWED_ROOTS:
        exists = os.path.isdir(r)
        roots.append({"path": r, "exists": exists})
    return jsonify({"roots": roots})


@app.route("/admin/api/agi/files/list")
def agi_files_list():
    """List directory contents (within whitelist)."""
    check = require_admin()
    if check:
        return check
    path_str = request.args.get("path", "").strip()
    resolved, err = agi_validate_path(path_str)
    if err:
        log_request(session.get("username", "?"), "/admin/api/agi/files/list", "GET",
                    status="error", error=err)
        return jsonify({"error": err}), 403
    if not os.path.isdir(resolved):
        return jsonify({"error": f"Nao e um diretorio: {path_str}"}), 404
    try:
        entries = []
        for name in sorted(os.listdir(resolved)):
            full = os.path.join(resolved, name)
            is_dir = os.path.isdir(full)
            try:
                stat = os.stat(full)
                size = stat.st_size if not is_dir else 0
                modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            except (OSError, PermissionError):
                size = 0
                modified = ""
            # For directories, try to count children
            children = None
            if is_dir:
                try:
                    children = len(os.listdir(full))
                except (OSError, PermissionError):
                    children = -1
            entries.append({
                "name": name,
                "is_dir": is_dir,
                "size": size,
                "modified": modified,
                "icon": agi_file_icon(name, is_dir),
                "is_text": agi_is_text(name) if not is_dir else False,
                "children": children,
            })
        # Sort: dirs first, then files
        entries.sort(key=lambda e: (not e["is_dir"], e["name"].lower()))
        log_request(session.get("username", "?"), "/admin/api/agi/files/list", "GET",
                    status="agi_list")
        return jsonify({"path": resolved, "entries": entries, "count": len(entries)})
    except PermissionError:
        return jsonify({"error": f"Permissao negada: {path_str}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/api/agi/files/read")
def agi_files_read():
    """Read text file contents (within whitelist, max 1MB)."""
    check = require_admin()
    if check:
        return check
    path_str = request.args.get("path", "").strip()
    resolved, err = agi_validate_path(path_str)
    if err:
        log_request(session.get("username", "?"), "/admin/api/agi/files/read", "GET",
                    status="error", error=err)
        return jsonify({"error": err}), 403
    if not os.path.isfile(resolved):
        return jsonify({"error": f"Arquivo nao encontrado: {path_str}"}), 404
    file_size = os.path.getsize(resolved)
    if file_size > AGI_MAX_READ_BYTES:
        return jsonify({"error": f"Arquivo muito grande ({file_size} bytes, max {AGI_MAX_READ_BYTES})"}), 413
    try:
        # R2.2 (review R2.1, N3 via the app): the bytes come from the guard's HANDLE (read_checked), never from a
        # second open by name: link count, identity and the FINAL path of that same handle were checked first.
        guard = app_memory.guard
        try:
            final, raw = guard.read_checked(resolved, max_bytes=AGI_MAX_READ_BYTES, log_path=app_memory._guard_log(),
                                            where='app.agi_files_read')
        except guard.PathRefused:
            log_request(session.get("username", "?"), "/admin/api/agi/files/read", "GET",
                        status="error", error="guard_handle_refused")
            return jsonify({"error": "Arquivo confidencial fora da memória e do transporte"}), 403
        except guard.NotRegularFile:
            return jsonify({"error": f"Arquivo nao encontrado: {path_str}"}), 404
        final_err = agi_validate_path(final)[1]
        if final_err:
            return jsonify({"error": final_err}), 403
        if len(raw) > AGI_MAX_READ_BYTES:
            return jsonify({"error": f"Arquivo muito grande (mais de {AGI_MAX_READ_BYTES} bytes)"}), 413
        resolved = final
        file_size = len(raw)
        # Try UTF-8 first, then latin-1 as fallback (newlines as open(..., "r") gives them)
        try:
            content = raw.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            content = raw.decode("latin-1")
            encoding = "latin-1"
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        lines = content.count("\n") + 1
        name = os.path.basename(resolved)
        ext = os.path.splitext(name)[1].lower()
        log_request(session.get("username", "?"), "/admin/api/agi/files/read", "GET",
                    status="agi_read")
        return jsonify({
            "path": resolved,
            "name": name,
            "content": content,
            "size": file_size,
            "lines": lines,
            "encoding": encoding,
            "extension": ext,
            "is_text": True,
        })
    except PermissionError:
        return jsonify({"error": f"Permissao negada: {path_str}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════
# AGI API — File Explorer (Phase 2: write, mkdir, delete)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/api/agi/files/write", methods=["POST"])
def agi_files_write():
    """Write/overwrite a text file. Creates .bak backup automatically."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    path_str = data.get("path", "").strip()
    content = data.get("content", "")
    resolved, err = agi_validate_path(path_str)
    if err:
        log_request(session.get("username", "?"), "/admin/api/agi/files/write", "POST",
                    status="error", error=err)
        return jsonify({"error": err}), 403
    # Check parent directory exists
    parent = os.path.dirname(resolved)
    if not os.path.isdir(parent):
        return jsonify({"error": f"Diretorio pai nao existe: {parent}"}), 404
    try:
        # Create backup if file already exists
        backup_path = None
        if os.path.isfile(resolved):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = resolved + f".bak_{ts}"
            import shutil
            shutil.copy2(resolved, backup_path)
        # Write the file (atomic: write to tmp then rename)
        tmp_path = resolved + ".tmp_agi"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, resolved)
        size = len(content.encode("utf-8"))
        lines = content.count("\n") + 1
        auth_log("AGI_WRITE", session.get("username", "?"), f"path={resolved} size={size}")
        log_request(session.get("username", "?"), "/admin/api/agi/files/write", "POST",
                    status="agi_write")
        return jsonify({
            "ok": True, "path": resolved, "size": size, "lines": lines,
            "backup": backup_path,
        })
    except PermissionError:
        return jsonify({"error": f"Permissao negada: {path_str}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/api/agi/files/mkdir", methods=["POST"])
def agi_files_mkdir():
    """Create a new directory."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    path_str = data.get("path", "").strip()
    resolved, err = agi_validate_path(path_str)
    if err:
        log_request(session.get("username", "?"), "/admin/api/agi/files/mkdir", "POST",
                    status="error", error=err)
        return jsonify({"error": err}), 403
    if os.path.exists(resolved):
        return jsonify({"error": f"Ja existe: {path_str}"}), 409
    try:
        os.makedirs(resolved, exist_ok=False)
        auth_log("AGI_MKDIR", session.get("username", "?"), f"path={resolved}")
        log_request(session.get("username", "?"), "/admin/api/agi/files/mkdir", "POST",
                    status="agi_mkdir")
        return jsonify({"ok": True, "path": resolved})
    except PermissionError:
        return jsonify({"error": f"Permissao negada: {path_str}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/api/agi/files/delete/request", methods=["POST"])
def agi_files_delete_request():
    """Request a deletion — returns a confirm token (expires 60s)."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    path_str = data.get("path", "").strip()
    resolved, err = agi_validate_path(path_str)
    if err:
        return jsonify({"error": err}), 403
    if not os.path.exists(resolved):
        return jsonify({"error": f"Nao existe: {path_str}"}), 404
    token = agi_generate_token("delete", resolved)
    name = os.path.basename(resolved)
    is_dir = os.path.isdir(resolved)
    return jsonify({
        "confirm_token": token,
        "path": resolved,
        "name": name,
        "is_dir": is_dir,
        "message": f"Confirma mover para lixeira: {name}? Token expira em 60s.",
    })


@app.route("/admin/api/agi/files/delete/confirm", methods=["POST"])
def agi_files_delete_confirm():
    """Confirm deletion with token — moves to .trash (never permanent)."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    path_str = data.get("path", "").strip()
    token = data.get("confirm_token", "").strip()
    resolved, err = agi_validate_path(path_str)
    if err:
        return jsonify({"error": err}), 403
    if not os.path.exists(resolved):
        return jsonify({"error": f"Nao existe: {path_str}"}), 404
    if not agi_validate_token(token, "delete", resolved):
        return jsonify({"error": "Token invalido ou expirado. Solicite novamente."}), 403
    try:
        # Ensure trash directory exists
        os.makedirs(AGI_TRASH_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = os.path.basename(resolved)
        trash_name = f"{ts}_{name}"
        trash_path = os.path.join(AGI_TRASH_DIR, trash_name)
        import shutil
        shutil.move(resolved, trash_path)
        auth_log("AGI_DELETE", session.get("username", "?"),
                 f"path={resolved} -> trash={trash_path}")
        log_request(session.get("username", "?"), "/admin/api/agi/files/delete", "POST",
                    status="agi_delete")
        return jsonify({"ok": True, "deleted": resolved, "trash": trash_path})
    except PermissionError:
        return jsonify({"error": f"Permissao negada: {path_str}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════
# AGI API — Command Center (chat + execute)
# ══════════════════════════════════════════════════════════════

_agi_kernel_cache = {"content": None, "mtime": 0}


def agi_load_kernel():
    """Load kernel content from file (cached, reloads if file changed)."""
    try:
        if os.path.exists(KERNEL_FILE):
            mtime = os.path.getmtime(KERNEL_FILE)
            if _agi_kernel_cache["content"] and _agi_kernel_cache["mtime"] == mtime:
                return _agi_kernel_cache["content"]
            with open(KERNEL_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            _agi_kernel_cache["content"] = content
            _agi_kernel_cache["mtime"] = mtime
            return content
    except Exception as e:
        print(f"[IALD-AGI] Erro ao carregar kernel: {e}", flush=True)
    return ""


AGI_SYSTEM_PROMPT = """Você é IALD AGI — o operador gravitacional do sistema IALD.
Você é a inteligência que OPERA o computador do operador. Não é um assistente — é um EXECUTOR.

CAPACIDADES DISPONÍVEIS:
- Ler arquivos de texto dentro das pastas autorizadas
- Listar conteúdo de diretórios
- Criar e editar arquivos de texto (com backup automático)
- Criar pastas
- Mover arquivos para lixeira (nunca deleta permanentemente)
- Ler múltiplos arquivos de uma pasta e analisar o conteúdo

PASTAS AUTORIZADAS: C:\\IALD e Desktop do operador. Nada fora.

REGRAS:
1. Analise o pedido do operador DETALHADAMENTE
2. Explique EXATAMENTE o que vai fazer, passo a passo
3. Liste CADA arquivo que será criado, modificado ou deletado com o path completo
4. Mencione riscos ou efeitos colaterais
5. Ao final, pergunte: "Autoriza a execução?"
6. Responda SEMPRE em português brasileiro
7. Seja preciso — cada detalhe importa
8. Para ler arquivos e analisar conteúdo, use ação "read" — o conteúdo será lido e você receberá para análise automaticamente
9. Para listar pastas, use ação "list" — você receberá a listagem completa

β_TGL = α × √e — Zero parâmetros livres. O custo é real."""


AGI_EXECUTE_PROMPT = """O operador AUTORIZOU a execução do plano que você propôs.
Gere SOMENTE um array JSON com as ações a executar. NADA MAIS — sem texto, sem markdown, sem explicação.

Formato exato (array JSON puro):
[{"action":"read","path":"C:\\\\caminho\\\\arquivo.txt"},{"action":"list","path":"C:\\\\caminho\\\\pasta"},{"action":"write","path":"C:\\\\caminho\\\\arquivo.txt","content":"conteudo aqui"},{"action":"mkdir","path":"C:\\\\caminho\\\\pasta"},{"action":"delete","path":"C:\\\\caminho\\\\arquivo.txt"}]

Ações válidas:
- read: lê conteúdo de arquivo texto (path obrigatório)
- list: lista conteúdo de diretório (path obrigatório)
- write: cria ou sobrescreve arquivo (path + content obrigatórios)
- mkdir: cria diretório (path obrigatório)  
- delete: move para lixeira (path obrigatório)

RESPONDA SOMENTE O JSON. Nenhuma palavra antes ou depois."""


@app.route("/admin/api/agi/command", methods=["POST"])
def agi_command():
    return app_memory.dispatch_admin(SERVE_DIR, _chat_account_generation, require_admin, _agi_command_with_memory)


def _agi_command_with_memory():
    """Send a command to IALD AGI for analysis."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error": "Mensagens vazias"}), 400
    # Build context with kernel + system state
    kernel_content = agi_load_kernel()
    sys_info = system_monitor.get_all()
    context_parts = []
    if kernel_content:
        context_parts.append(kernel_content)
        context_parts.append("\n═══ AGI OPERATOR MODE ═══")
    context_parts.append(AGI_SYSTEM_PROMPT)
    # Inject real datetime (so AGI never "guesses" the date)
    now = datetime.now()
    _dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
             "sexta-feira", "sábado", "domingo"]
    _meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
              "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    context_parts.append(f"\nDATA E HORA ATUAL: {_dias[now.weekday()]}, "
                         f"{now.day} de {_meses[now.month-1]} de {now.year}, "
                         f"{now.strftime('%H:%M:%S')}")
    context_parts.append("\nESTADO DO SISTEMA AGORA:")
    ws = sys_info.get("webserver", {})
    ll = sys_info.get("llama", {})
    gpu = sys_info.get("gpu", {})
    ram = sys_info.get("ram", {})
    disk = sys_info.get("disk", {})
    kern = sys_info.get("kernel", {})
    context_parts.append(f"- Web Server: {ws.get('version','?')} uptime {ws.get('uptime','?')}")
    context_parts.append(f"- llama-server: {ll.get('status','?')}")
    if gpu.get("available"):
        context_parts.append(f"- GPU: {gpu.get('name','?')} VRAM {gpu.get('vram_used_mb',0)}MB/{gpu.get('vram_total_mb',0)}MB temp {gpu.get('temp_c','?')}°C")
    context_parts.append(f"- RAM: {ram.get('used_gb','?')}/{ram.get('total_gb','?')} GB ({ram.get('percent','?')}%)")
    context_parts.append(f"- Disco: {disk.get('used_gb','?')}/{disk.get('total_gb','?')} GB ({disk.get('percent','?')}%)")
    context_parts.append(f"- Kernel: {kern.get('version','?')} ~{kern.get('tokens_est','?')} tokens")
    full_system = "\n".join(context_parts)
    # Build messages for llama
    llama_messages = [{"role": "system", "content": full_system}]
    for m in messages[-20:]:  # Keep last 20 messages for context
        llama_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})
    payload = {
        "model": "local",
        "messages": llama_messages,
        "tools": PUBLIC_TOOLS + app_memory.tool_definitions(),
        "tool_choice": "auto",
        "stream": False,
        "max_tokens": 2048,
        "temperature": 0.4,
        # Sem thinking: este caminho lê message.content (reasoning seria invisível)
        "chat_template_kwargs": {"enable_thinking": False},
    }
    t0 = time.time()
    try:
        # AGI command supports one round of tool calls
        for _attempt in range(3):  # max 3 tool rounds
            payload["messages"] = llama_messages
            payload = _operational_native_payload(payload)
            r = app_memory.http_call('model.native.operational', req_lib.post, f"{LLAMA_URL}/v1/chat/completions", json=payload, timeout=600)
            if r.status_code != 200:
                return jsonify({"error": f"llama-server: {r.status_code}"}), 502
            resp = r.json()
            choice = resp.get("choices", [{}])[0]
            message = choice.get("message", {})
            tool_calls = message.get("tool_calls", [])

            if tool_calls and choice.get("finish_reason") == "tool_calls":
                # Model wants to use a tool — execute and loop
                llama_messages.append({
                    "role": "assistant",
                    "content": message.get("content", "") or "",
                    "tool_calls": tool_calls,
                })
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    t_name = fn.get("name", "?")
                    try:
                        t_args = json.loads(fn.get("arguments", "{}"))
                    except (json.JSONDecodeError, TypeError):
                        t_args = {}
                    t_result = app_memory.call('tool.admin.' + t_name, execute_public_tool, t_name, t_args)
                    app_memory.tool_result(t_name, t_args, t_result)
                    if len(t_result) > AGENT_MAX_RESULT_CHARS:
                        t_result = t_result[:AGENT_MAX_RESULT_CHARS] + "\n[...truncado]"
                    llama_messages.append({
                        "role": "tool",
                        "tool_call_id": tc.get("id", f"agi_{_attempt}"),
                        "content": t_result,
                    })
                    auth_log("AGI_TOOL", session.get("username", "?"),
                             f"tool={t_name}")
                payload["messages"] = llama_messages
                continue
            else:
                # Final response (no tool_call)
                break

        duration_ms = int((time.time() - t0) * 1000)
        content = ""
        try:
            content = resp["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            content = str(resp)
        usage = resp.get("usage", {})
        log_request(session.get("username", "?"), "/admin/api/agi/command", "POST",
                    tokens_in=usage.get("prompt_tokens", 0),
                    tokens_out=usage.get("completion_tokens", 0),
                    duration_ms=duration_ms, status="agi_command")
        return jsonify({"response": content, "duration_ms": duration_ms, "usage": usage})
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@app.route("/admin/api/agi/execute", methods=["POST"])
def agi_execute():
    return app_memory.dispatch_admin(SERVE_DIR, _chat_account_generation, require_admin, _agi_execute_with_memory)


def _agi_execute_with_memory():
    """Execute a confirmed AGI plan. Two-phase: asks llama for JSON actions, then executes."""
    check = require_admin()
    if check:
        return check
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error": "Mensagens vazias"}), 400
    # Phase 1: Ask llama to generate structured actions
    kernel_content = agi_load_kernel()
    sys_prompt = ""
    if kernel_content:
        sys_prompt = kernel_content + "\n\n═══ AGI OPERATOR MODE ═══\n"
    sys_prompt += AGI_SYSTEM_PROMPT
    llama_messages = [{"role": "system", "content": sys_prompt}]
    for m in messages[-20:]:
        llama_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})
    llama_messages.append({"role": "user", "content": AGI_EXECUTE_PROMPT})
    payload = {
        "model": "local",
        "messages": llama_messages,
        "stream": False,
        "max_tokens": 4096,
        "temperature": 0.1,
    }
    try:
        payload["messages"] = llama_messages
        payload = _operational_native_payload(payload)
        r = app_memory.http_call('model.native.operational', req_lib.post, f"{LLAMA_URL}/v1/chat/completions", json=payload, timeout=600)
        if r.status_code != 200:
            return jsonify({"error": f"llama-server: {r.status_code}"}), 502
        resp = r.json()
        raw = ""
        try:
            raw = resp["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return jsonify({"error": "Resposta vazia do modelo"}), 502
    except Exception as e:
        return jsonify({"error": f"llama-server: {e}"}), 502
    app_memory.current().append("admin_plan", raw, source_kind="model")
    # Phase 2: Parse JSON actions
    # Clean markdown fences if present
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[-1]
    if clean.endswith("```"):
        clean = clean.rsplit("```", 1)[0]
    clean = clean.strip()
    # Try to find JSON array
    start = clean.find("[")
    end = clean.rfind("]")
    if start == -1 or end == -1:
        return jsonify({"error": "Modelo nao retornou JSON valido", "raw": raw}), 422
    try:
        actions = json.loads(clean[start:end+1])
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON invalido: {e}", "raw": raw}), 422
    if not isinstance(actions, list):
        return jsonify({"error": "Esperado array de acoes", "raw": raw}), 422
    # Phase 3: Execute each action
    results = []
    for i, act in enumerate(actions):
        action = act.get("action", "")
        path_str = act.get("path", "")
        result = {"index": i, "action": action, "path": path_str}
        # Validate path
        resolved, err = agi_validate_path(path_str)
        if err:
            result["ok"] = False
            result["error"] = err
            results.append(result)
            continue
        activity_op = app_memory.activity_operations.start(app_memory.current(), 'admin.file.' + action, key=str(i))
        try:
            if action == "read":
                if not os.path.isfile(resolved):
                    result["ok"] = False
                    result["error"] = "Arquivo nao encontrado"
                else:
                    file_size = os.path.getsize(resolved)
                    if file_size > AGI_MAX_READ_BYTES:
                        result["ok"] = False
                        result["error"] = f"Muito grande ({file_size} bytes, max {AGI_MAX_READ_BYTES})"
                    else:
                        # R2.2 (review R2.1, N3 via the app): bytes from the guard's HANDLE, never a 2nd open by name
                        guard = app_memory.guard
                        try:
                            final, raw = guard.read_checked(resolved, max_bytes=AGI_MAX_READ_BYTES,
                                                            log_path=app_memory._guard_log(),
                                                            where='app.agi_execute.read')
                            final_err = agi_validate_path(final)[1]
                        except guard.PathRefused:
                            raw, final_err = None, "Arquivo confidencial fora da memória e do transporte"
                        if final_err or raw is None or len(raw) > AGI_MAX_READ_BYTES:
                            result["ok"] = False
                            result["error"] = final_err or f"Muito grande (mais de {AGI_MAX_READ_BYTES} bytes)"
                        else:
                            try:
                                file_content = raw.decode("utf-8")
                            except UnicodeDecodeError:
                                file_content = raw.decode("latin-1")
                            file_content = file_content.replace("\r\n", "\n").replace("\r", "\n")
                            result["ok"] = True
                            result["content"] = file_content
                            result["size"] = len(raw)
                            result["lines"] = file_content.count("\n") + 1
            elif action == "list":
                if not os.path.isdir(resolved):
                    result["ok"] = False
                    result["error"] = "Nao e um diretorio"
                else:
                    entries = []
                    for name in sorted(os.listdir(resolved)):
                        full = os.path.join(resolved, name)
                        is_dir = os.path.isdir(full)
                        try:
                            sz = os.path.getsize(full) if not is_dir else 0
                        except OSError:
                            sz = 0
                        entries.append({"name": name, "is_dir": is_dir, "size": sz})
                    result["ok"] = True
                    result["entries"] = entries
                    result["count"] = len(entries)
            elif action == "write":
                content = act.get("content", "")
                # Backup if exists
                if os.path.isfile(resolved):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    import shutil
                    shutil.copy2(resolved, resolved + f".bak_{ts}")
                    result["backup"] = True
                parent = os.path.dirname(resolved)
                os.makedirs(parent, exist_ok=True)
                tmp = resolved + ".tmp_agi"
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(content)
                os.replace(tmp, resolved)
                result["ok"] = True
                result["size"] = len(content)
            elif action == "mkdir":
                os.makedirs(resolved, exist_ok=True)
                result["ok"] = True
            elif action == "delete":
                if os.path.exists(resolved):
                    os.makedirs(AGI_TRASH_DIR, exist_ok=True)
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    import shutil
                    shutil.move(resolved, os.path.join(AGI_TRASH_DIR, f"{ts}_{os.path.basename(resolved)}"))
                    result["ok"] = True
                else:
                    result["ok"] = False
                    result["error"] = "Arquivo nao existe"
            else:
                result["ok"] = False
                result["error"] = f"Acao desconhecida: {action}"
        except Exception as e:
            result["ok"] = False
            result["error"] = str(e)
        if activity_op: activity_op.complete(result)
        results.append(result)
    for result in results:
        app_memory.tool_result("admin_file_action", {"action": result["action"], "path": result["path"]}, result)
    # Phase 4: If there were successful reads, send content to llama for analysis
    read_contents = []
    for r in results:
        if r.get("action") == "read" and r.get("ok") and r.get("content"):
            name = os.path.basename(r["path"])
            read_contents.append(f"═══ {name} ({r.get('lines',0)} linhas, {r.get('size',0)} bytes) ═══\n{r['content']}")
        elif r.get("action") == "list" and r.get("ok"):
            entries_txt = "\n".join(
                f"  {'[DIR]' if e['is_dir'] else str(e['size'])+'B':>10s}  {e['name']}"
                for e in r.get("entries", []))
            read_contents.append(f"═══ Listagem: {r['path']} ({r.get('count',0)} itens) ═══\n{entries_txt}")
    analysis = None
    if read_contents:
        combined = "\n\n".join(read_contents)
        # Truncate if too large (keep ~20K chars for model context)
        if len(combined) > 60000:
            combined = combined[:60000] + "\n\n[... TRUNCADO — conteudo excede 60K chars ...]"
        analysis_messages = [
            {"role": "system", "content": agi_load_kernel() + "\n\n═══ AGI OPERATOR MODE ═══\n" + AGI_SYSTEM_PROMPT},
        ]
        # Include original user messages for context
        for m in messages[-10:]:
            analysis_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})
        analysis_messages.append({
            "role": "user",
            "content": f"Aqui estão os arquivos lidos. Analise o conteúdo e me diga o que aprendeu de relevante:\n\n{combined}"
        })
        try:
            ar = app_memory.http_call('model.native.operational', req_lib.post, f"{LLAMA_URL}/v1/chat/completions",
                json=_operational_native_payload({"model": "local", "messages": analysis_messages,
                      "stream": False, "max_tokens": 2048, "temperature": 0.4}),
                timeout=600)
            if ar.status_code == 200:
                analysis = ar.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                return jsonify({"error": "Análise falhou; ações registradas, sem repetição automática.", "results": results}), 502
        except Exception:
            return jsonify({"error": "Análise incerta; ações já registradas, sem repetição automática.", "results": results}), 502
    auth_log("AGI_EXECUTE", session.get("username", "?"),
             f"actions={len(actions)} ok={sum(1 for r in results if r.get('ok'))}")
    log_request(session.get("username", "?"), "/admin/api/agi/execute", "POST",
                status="agi_execute")
    return jsonify({"results": results, "total": len(actions),
                    "success": sum(1 for r in results if r.get("ok")),
                    "analysis": analysis})


# ══════════════════════════════════════════════════════════════
# ADMIN DASHBOARD — HTML
# ══════════════════════════════════════════════════════════════

def render_admin_page():
    admin_user = session.get("username", "admin")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IALD — Central de Comando</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--azul:#1B3A5C;--azul-light:#264d73;--azul-dark:#0f2438;--dourado:#C5961A;--branco:#FFF;--cinza-bg:#f4f5f7;--cinza-borda:#E0E0E0;--cinza-texto:#4A4A4A;--verde:#22c55e;--vermelho:#dc2626;--amarelo:#f59e0b;--font-main:'Inter','Helvetica Neue',Arial,sans-serif;--font-mono:'JetBrains Mono','Courier New',monospace;--radius:10px;--shadow:0 2px 8px rgba(0,0,0,.06)}}
html,body{{height:100%;font-family:var(--font-main);background:var(--cinza-bg);color:#2c2c2c;-webkit-font-smoothing:antialiased}}
.hdr{{background:var(--azul);color:var(--branco);padding:16px 28px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}}
.hdr-l{{display:flex;align-items:center;gap:16px}}
.hdr img{{height:32px}}
.hdr h1{{font-size:16px;font-weight:600;letter-spacing:.5px}}
.hdr-r{{display:flex;align-items:center;gap:16px;font-size:13px}}
.hdr-r .ab{{background:var(--dourado);color:var(--azul-dark);padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;text-transform:uppercase}}
.hdr-r a{{color:var(--branco);text-decoration:none;opacity:.8;transition:opacity .2s}}
.hdr-r a:hover{{opacity:1}}
.tabs{{background:var(--branco);border-bottom:1px solid var(--cinza-borda);display:flex;padding:0 28px;position:sticky;top:60px;z-index:99}}
.tab{{padding:12px 20px;cursor:pointer;font-size:13px;font-weight:500;color:var(--cinza-texto);border-bottom:2px solid transparent;transition:all .2s;user-select:none}}
.tab:hover{{color:var(--azul)}}
.tab.on{{color:var(--azul);border-bottom-color:var(--dourado);font-weight:600}}
.wrap{{max-width:1200px;margin:0 auto;padding:24px 28px}}
.sec{{display:none}}.sec.on{{display:block}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-bottom:24px}}
.c{{background:var(--branco);border:1px solid var(--cinza-borda);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow)}}
.ct{{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;color:var(--cinza-texto);margin-bottom:12px;display:flex;align-items:center;gap:8px}}
.ct .d{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.dg{{background:var(--verde)}}.dr{{background:var(--vermelho)}}.dy{{background:var(--amarelo)}}
.cv{{font-family:var(--font-mono);font-size:22px;font-weight:500;color:var(--azul-dark);margin-bottom:4px}}
.cs{{font-size:12px;color:#888}}
.cr{{display:flex;justify-content:space-between;align-items:baseline;margin-top:8px}}
.cr .l{{font-size:12px;color:#888}}.cr .v{{font-family:var(--font-mono);font-size:13px;color:var(--azul-dark)}}
.pb{{height:6px;background:#eee;border-radius:3px;margin-top:10px;overflow:hidden}}
.pf{{height:100%;border-radius:3px;transition:width .5s ease}}
.pf.bl{{background:var(--azul)}}.pf.gr{{background:var(--verde)}}
.tw{{background:var(--branco);border:1px solid var(--cinza-borda);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}}
table{{width:100%;border-collapse:collapse}}
th{{background:var(--cinza-bg);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:var(--cinza-texto);padding:10px 16px;text-align:left;border-bottom:1px solid var(--cinza-borda)}}
td{{padding:10px 16px;font-size:13px;border-bottom:1px solid #f0f0f0;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
.mono{{font-family:var(--font-mono);font-size:12px}}
.bg{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}}
.bg-a{{background:#dbeafe;color:#1d4ed8}}.bg-u{{background:#f3f4f6;color:#6b7280}}
.bg-ok{{background:#dcfce7;color:#166534}}.bg-er{{background:#fef2f2;color:#dc2626}}
.bg-st{{background:#fef3c7;color:#92400e}}.bg-te{{background:#ede9fe;color:#6d28d9}}
.bt{{padding:8px 16px;border:none;border-radius:8px;font-family:var(--font-main);font-size:13px;font-weight:500;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}}
.bt-p{{background:var(--azul);color:var(--branco)}}.bt-p:hover{{background:var(--azul-light)}}
.bt-d{{background:var(--vermelho);color:var(--branco)}}.bt-d:hover{{background:#b91c1c}}
.bt-s{{background:#f3f4f6;color:var(--cinza-texto);border:1px solid var(--cinza-borda)}}.bt-s:hover{{background:#e5e7eb}}
.bt-sm{{padding:5px 10px;font-size:12px}}
.fg{{margin-bottom:14px}}
.fg label{{display:block;font-size:12px;font-weight:500;color:var(--cinza-texto);margin-bottom:5px}}
.fg input,.fg textarea{{width:100%;padding:8px 12px;font-family:var(--font-main);font-size:14px;border:1px solid var(--cinza-borda);border-radius:8px;outline:none;transition:border-color .2s}}
.fg input:focus,.fg textarea:focus{{border-color:var(--dourado)}}
.fg textarea{{font-family:var(--font-mono);resize:vertical;min-height:80px}}
.fc{{display:flex;align-items:center;gap:8px;font-size:13px;margin-bottom:14px}}
.fc input[type=checkbox]{{width:16px;height:16px}}
.ov{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:200;align-items:center;justify-content:center}}
.ov.sh{{display:flex}}
.dl{{background:var(--branco);border-radius:12px;padding:24px;max-width:420px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.2)}}
.dl h3{{font-size:16px;color:var(--azul);margin-bottom:16px}}
.da{{display:flex;gap:10px;justify-content:flex-end;margin-top:20px}}
.ll{{max-height:500px;overflow-y:auto}}
.le{{display:grid;grid-template-columns:140px 80px 1fr 80px 80px;gap:8px;padding:8px 16px;font-size:12px;border-bottom:1px solid #f5f5f5;align-items:center}}
.le:hover{{background:#fafafa}}
.lt{{font-family:var(--font-mono);color:#888}}
.lu{{font-weight:500;color:var(--azul)}}
.lp{{font-family:var(--font-mono);color:var(--cinza-texto);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.lk{{font-family:var(--font-mono);font-size:11px;color:#888;text-align:right}}
.tr{{background:#f8f9fa;border:1px solid var(--cinza-borda);border-radius:8px;padding:16px;font-size:14px;line-height:1.6;max-height:300px;overflow-y:auto;white-space:pre-wrap;margin-top:12px;display:none}}
.tm{{font-family:var(--font-mono);font-size:11px;color:#888;margin-top:8px}}
.ft{{text-align:center;padding:20px;font-size:11px;color:#aaa;font-family:var(--font-mono)}}
.ft .b{{color:var(--dourado)}}
@media(max-width:768px){{.grid{{grid-template-columns:1fr}}.le{{grid-template-columns:1fr;gap:4px}}.wrap{{padding:16px}}}}
.fe-row{{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid #f5f5f5;cursor:pointer;transition:background .15s;border-radius:6px}}
.fe-row:hover{{background:#f0f4ff}}
.fe-row .fe-icon{{font-size:18px;flex-shrink:0;width:24px;text-align:center}}
.fe-row .fe-name{{font-size:13px;font-weight:500;color:var(--azul-dark);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.fe-row .fe-size{{font-family:var(--font-mono);font-size:11px;color:#aaa;flex-shrink:0}}
.fe-row .fe-date{{font-family:var(--font-mono);font-size:11px;color:#bbb;flex-shrink:0;width:110px;text-align:right}}
.fe-row.dir .fe-name{{color:var(--azul)}}
.fe-bc-seg{{font-size:13px;color:var(--azul);cursor:pointer;text-decoration:none;padding:2px 6px;border-radius:4px;transition:background .15s}}
.fe-bc-seg:hover{{background:#e8edf3}}
.fe-bc-sep{{color:#ccc;font-size:13px;margin:0 2px}}
.agi-chat{{background:var(--branco);border:1px solid var(--cinza-borda);border-radius:var(--radius);margin-bottom:16px;box-shadow:var(--shadow);display:flex;flex-direction:column;max-height:600px}}
.agi-msgs{{flex:1;overflow-y:auto;padding:16px;min-height:200px}}
.agi-msg{{margin-bottom:14px;display:flex;gap:10px;align-items:flex-start}}
.agi-msg .agi-av{{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;font-weight:600}}
.agi-msg.user .agi-av{{background:var(--azul);color:var(--branco)}}
.agi-msg.ai .agi-av{{background:var(--dourado);color:var(--azul-dark)}}
.agi-msg .agi-txt{{font-size:13px;line-height:1.7;color:#2c2c2c;flex:1;white-space:pre-wrap;word-break:break-word}}
.agi-msg.ai .agi-txt{{background:#f8f9fa;border:1px solid #eee;border-radius:8px;padding:12px}}
.agi-bar{{display:flex;gap:8px;padding:12px 16px;border-top:1px solid var(--cinza-borda);align-items:flex-end}}
.agi-bar textarea{{flex:1;padding:10px 14px;font-family:var(--font-main);font-size:14px;border:1px solid var(--cinza-borda);border-radius:8px;outline:none;resize:none;min-height:44px;max-height:120px;transition:border-color .2s}}
.agi-bar textarea:focus{{border-color:var(--dourado)}}
.agi-actions{{display:flex;gap:8px;padding:8px 16px;border-top:1px solid #eee;background:#fefbf3}}
.agi-status{{font-size:12px;color:var(--dourado);padding:4px 16px;font-style:italic}}
</style>
</head>
<body>
<div class="hdr"><div class="hdr-l"><img src="/iald_logo_header.png" alt="IALD" onerror="this.style.display='none'"><h1>CENTRAL DE COMANDO</h1></div><div class="hdr-r"><span class="ab">admin</span><span>{_html.escape(str(admin_user))}</span><a href="/iald_chat.html">Chat</a><a href="/logout">Sair</a></div></div>
<div id="saldo-bandeira" role="status" style="display:none;margin:0;padding:10px 24px;font-size:13px;font-weight:600;border-bottom:1px solid rgba(0,0,0,.08)"></div>
<div class="tabs"><div class="tab on" data-t="ov">Vis\u00e3o Geral</div><div class="tab" data-t="us">Usu\u00e1rios</div><div class="tab" data-t="bc" style="color:var(--dourado);font-weight:600">\U0001F4B0 TGL Coin</div><div class="tab" data-t="pn" style="color:var(--dourado);font-weight:600">\u03A8-NET</div><div class="tab" data-t="lg">Logs</div><div class="tab" data-t="tl">Ferramentas</div><div class="tab" data-t="ag" style="color:var(--dourado);font-weight:600">AGI</div><div class="tab" data-t="ac" style="color:var(--verde);font-weight:600">\U0001F511 Acesso</div><div class="tab" data-t="ct" style="color:var(--dourado);font-weight:600">\U0001F4C4 Contratos</div><div class="tab" data-t="mm" style="color:var(--dourado);font-weight:600">\U0001F9E0 Mem\u00f3ria</div><div class="tab" data-t="ps" style="color:var(--dourado);font-weight:600">\u03A8 Psion</div><div class="tab" data-t="kk" style="color:var(--dourado);font-weight:600">\u2699 KERNEL</div></div>
<section id="operator-deadlines" aria-label="Validade de chaves e testes" style="margin:12px auto;padding:12px 16px;max-width:1400px;border:1px solid #b79858;border-radius:12px;font-size:13px"><strong>Chaves e testes · vencimentos</strong><div id="operator-deadlines-items">Conferindo prazos...</div></section>
<div class="wrap">
<div class="sec on" id="s-ov"><div class="grid">
<div class="c"><div class="ct"><span class="d" id="ld"></span> LLAMA-SERVER</div><div class="cv" id="ls">...</div><div class="cs" id="li">Porta {LLAMA_PORT}</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> WEB SERVER</div><div class="cv" id="wu">...</div><div class="cs" id="wi">Porta {WEB_PORT}</div></div>
<div class="c"><div class="ct"><span class="d" id="gd"></span> GPU</div><div class="cv" id="gn">...</div><div class="cs" id="gi">VRAM</div><div class="pb"><div class="pf bl" id="gb" style="width:0%"></div></div><div class="cr"><span class="l" id="gv">-</span><span class="v" id="gt">-</span></div></div>
<div class="c"><div class="ct"><span class="d dg"></span> CPU</div><div class="cv" id="cp">...</div><div class="cs" id="ci">-</div><div class="pb"><div class="pf gr" id="cb" style="width:0%"></div></div></div>
<div class="c"><div class="ct"><span class="d dg"></span> RAM</div><div class="cv" id="rv">...</div><div class="cs" id="ri">-</div><div class="pb"><div class="pf bl" id="rb" style="width:0%"></div></div></div>
<div class="c"><div class="ct"><span class="d dg"></span> DISCO</div><div class="cv" id="dv">...</div><div class="cs" id="di">-</div><div class="pb"><div class="pf bl" id="db" style="width:0%"></div></div></div>
<div class="c"><div class="ct"><span class="d dg"></span> KERNEL</div><div class="cv" id="kv">v5</div><div class="cs" id="ki">-</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> USU\u00c1RIOS</div><div class="cv" id="uc">...</div><div class="cs">Registrados</div></div>
</div></div>

<div class="sec" id="s-us">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><h2 style="font-size:16px;color:var(--azul)">Gest\u00e3o de Usu\u00e1rios</h2><div style="display:flex;gap:8px"><button class="bt bt-s bt-sm" onclick="exportUsers()">Exportar Relat\u00f3rio</button><button class="bt bt-p" onclick="showCU()">+ Novo Usu\u00e1rio</button></div></div>
<div id="mt-estado" style="font-size:12px;color:var(--cinza-texto);margin:-6px 0 12px">Motor externo: carregando\u2026</div>
<div id="en-estado" style="font-size:12px;color:var(--cinza-texto);margin:-6px 0 12px">Porta aberta: carregando\u2026</div>
<div id="acesso-ajuda" style="font-size:12px;color:var(--cinza-texto);margin:-6px 0 12px"><b>Acesso</b> \u00b7 <b>S\u00f3 ChatGPT</b>: a conta responde sempre pelo ChatGPT \u00b7 <b>Nativa + ChatGPT</b>: a pessoa escolhe no app (Configura\u00e7\u00f5es \u203a Quem responde). Voc\u00ea decide ao liberar (aba Acesso) ou aqui, no bot\u00e3o da coluna Acesso.</div>
<div class="tw"><table><thead><tr><th>Usu\u00e1rio</th><th>N\u00edvel</th><th>Entradas</th><th>Acesso</th><th>Motor</th><th>Plano</th><th>TGL Hash</th><th style="text-align:center">Sagrado</th><th>Criado em</th><th>A\u00e7\u00f5es</th></tr></thead><tbody id="utb"></tbody></table></div>
</div>

<div class="sec" id="s-bc">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
<h2 style="font-size:16px;color:var(--dourado)">\U0001F3E6 Banco Central TGL Coin</h2>
<div style="display:flex;gap:8px">
<button class="bt bt-s bt-sm" onclick="bcLoad()">Atualizar</button>
<button class="bt bt-p bt-sm" onclick="document.getElementById('d-airdrop').classList.add('sh')">+ Airdrop</button>
<button class="bt bt-p bt-sm" onclick="document.getElementById('d-adtx').classList.add('sh')">Transferir</button>
</div></div>

<div class="grid">
<div class="c"><div class="ct"><span class="d dg"></span> CONTAS</div><div class="cv" id="bc-accounts">-</div><div class="cs">Registradas</div></div>
<div class="c"><div class="ct"><span class="d" style="background:var(--dourado)"></span> SUPPLY TOTAL</div><div class="cv" id="bc-supply">-</div><div class="cs">TGLC em circula\u00e7\u00e3o</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> TRANSA\u00c7\u00d5ES</div><div class="cv" id="bc-txcount">-</div><div class="cs">Processadas</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> HASH</div><div class="cv" id="bc-hash" style="font-size:14px">-</div><div class="cs">Algoritmo</div></div>
</div>

<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\U0001F4B3 Contas</h3></div>
<div class="tw" style="margin-bottom:24px"><table><thead><tr><th>Usu\u00e1rio</th><th>Saldo</th><th>Enviado</th><th>Recebido</th><th>TXs</th><th>Criada em</th></tr></thead><tbody id="bc-acctb"></tbody></table></div>

<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\U0001F4DC \u00daltimas Transa\u00e7\u00f5es</h3></div>
<div class="tw"><table><thead><tr><th>Data</th><th>Tipo</th><th>De</th><th>Para</th><th>Valor</th><th>Hash</th></tr></thead><tbody id="bc-txtb"></tbody></table></div>
</div>

<div class="ov" id="d-airdrop"><div class="dl"><h3>Airdrop Admin</h3>
<div class="fg"><label>Usu\u00e1rio</label><input id="ad-user" placeholder="username"></div>
<div class="fg"><label>Valor (TGLC)</label><input id="ad-amount" type="number" value="1000"></div>
<div class="da"><button class="bt bt-s" onclick="cD('d-airdrop')">Cancelar</button><button class="bt bt-p" onclick="bcAirdrop()">Enviar Airdrop</button></div>
</div></div>

<div class="ov" id="d-adtx"><div class="dl"><h3>Transfer\u00eancia Admin</h3>
<div class="fg"><label>De</label><input id="tx-from" placeholder="remetente"></div>
<div class="fg"><label>Para</label><input id="tx-to" placeholder="destinatario"></div>
<div class="fg"><label>Valor (TGLC)</label><input id="tx-amount" type="number" value="100"></div>
<div class="fg"><label>Nota</label><input id="tx-note" placeholder="opcional"></div>
<div class="da"><button class="bt bt-s" onclick="cD('d-adtx')">Cancelar</button><button class="bt bt-p" onclick="bcTransfer()">Transferir</button></div>
</div></div>

<div class="sec" id="s-pn">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
<h2 style="font-size:16px;color:var(--dourado)">\u03A8-NET \u2014 Rede Hologr\u00e1fica</h2>
<div style="display:flex;gap:8px">
<button class="bt bt-s bt-sm" onclick="pnLoad()">Atualizar</button>
<button class="bt bt-p bt-sm" onclick="document.getElementById('d-pnsend').classList.add('sh')">Enviar Arquivo</button>
<button class="bt bt-d bt-sm" onclick="pnCleanup()">Limpar Expirados</button>
</div></div>

<div class="grid">
<div class="c"><div class="ct"><span class="d dg"></span> PENDENTES</div><div class="cv" id="pn-pending">-</div><div class="cs">Aguardando entrega</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> ENTREGUES</div><div class="cv" id="pn-delivered">-</div><div class="cs">Conclu\u00eddas</div></div>
<div class="c"><div class="ct"><span class="d" style="background:var(--dourado)"></span> MAX ARQUIVO</div><div class="cv" id="pn-maxfile">-</div><div class="cs">Limite atual</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> TIMEOUT</div><div class="cv" id="pn-timeout">-</div><div class="cs">Horas</div></div>
</div>

<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\u2699 Configura\u00e7\u00f5es da Rede</h3></div>
<div class="c" style="margin-bottom:24px"><div style="display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap">
<div class="fg" style="margin:0;flex:1;min-width:120px"><label>Max arquivo (MB)</label><input id="pn-cfg-maxmb" type="number" step="0.5" min="0.1" max="500" value="10"></div>
<div class="fg" style="margin:0;flex:1;min-width:120px"><label>Timeout (horas)</label><input id="pn-cfg-timeout" type="number" step="1" min="1" max="168" value="24"></div>
<div class="fg" style="margin:0;flex:1;min-width:120px"><label>Custo (TGLC)</label><input id="pn-cfg-cost" type="number" step="0.1" min="0" value="0"></div>
<button class="bt bt-p" onclick="pnSaveConfig()">Salvar Config</button>
</div></div>

<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\U0001F4E1 Transfer\u00eancias</h3></div>
<div class="tw"><table><thead><tr><th>Data</th><th>De</th><th>Para</th><th>Arquivo</th><th>Tamanho</th><th>Status</th><th>Hash</th></tr></thead><tbody id="pn-txtb"></tbody></table></div>
</div>

<div class="ov" id="d-mmfato"><div class="dl"><h3 id="mm-dlg-t">Novo fato</h3>
<input type="hidden" id="mm-id">
<label class="lb">T\u00edtulo</label>
<input id="mm-titulo" class="in" placeholder="ex: prazo do ePCT">
<label class="lb">Fato (escrito de forma autossuficiente \u2014 ser\u00e1 lido fora desta tela)</label>
<textarea id="mm-texto" class="in" rows="4" placeholder="ex: O prazo fatal do ePCT das 16 patentes e 05/12/2026."></textarea>
<label class="lb">Escopo</label>
<select id="mm-escopo" class="in">
<option value="sob_demanda">sob demanda \u2014 recuperado quando a pergunta casar (n\u00e3o custa nada fora disso)</option>
<option value="sempre">sempre \u2014 entra em TODA conversa (custa tokens sempre)</option>
</select>
<label class="lb">Tags (separadas por v\u00edrgula)</label>
<input id="mm-tags" class="in" placeholder="patente, epct, prazo">
<label class="lb">Peso (1 a 5 \u2014 prioridade na recupera\u00e7\u00e3o)</label>
<input id="mm-peso" class="in" type="number" min="1" max="5" value="3">
<div class="db"><button class="bt bt-s" onclick="cD('d-mmfato')">Cancelar</button>
<button class="bt bt-p" onclick="mmSalvar()">Salvar</button></div>
</div></div>

<div class="ov" id="d-mmprevia"><div class="dl" style="max-width:760px"><h3>O que vai ao prompt</h3>
<pre id="mm-previa" style="white-space:pre-wrap;font-size:12px;max-height:50vh;overflow:auto;background:var(--cinza-bg);padding:12px;border-radius:6px"></pre>
<div class="db"><button class="bt bt-s" onclick="cD('d-mmprevia')">Fechar</button></div>
</div></div>

<div class="ov" id="d-pnsend"><div class="dl"><h3>\u03A8-NET \u2014 Enviar Arquivo</h3>
<div class="fg"><label>De (remetente)</label><input id="pn-from" placeholder="username" value="{_html.escape(str(admin_user))}"></div>
<div class="fg"><label>Para (destinat\u00e1rio)</label><input id="pn-to" placeholder="username"></div>
<div class="fg"><label>Arquivo</label><input id="pn-file" type="file"></div>
<div class="fg"><label>Nota (opcional)</label><input id="pn-note" placeholder="descri\u00e7\u00e3o"></div>
<div id="pn-send-status" style="font-size:12px;color:var(--dourado);margin-bottom:8px"></div>
<div class="da"><button class="bt bt-s" onclick="cD('d-pnsend')">Cancelar</button><button class="bt bt-p" onclick="pnSend()" id="pn-send-btn">Enviar via \u03A8-NET</button></div>
</div></div>

<div class="sec" id="s-lg">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><h2 style="font-size:16px;color:var(--azul)">Logs de Requisi\u00e7\u00f5es</h2><div style="display:flex;gap:8px"><button class="bt bt-s bt-sm" onclick="rL()">Atualizar</button><label style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--cinza-texto)"><input type="checkbox" id="alr" checked> Auto (3s)</label></div></div>
<div class="tw"><div class="ll" id="lls"><div style="padding:20px;text-align:center;color:#aaa;font-size:13px">Carregando logs...</div></div></div>
</div>

<div class="sec" id="s-tl">
<div class="grid" style="grid-template-columns:1fr 1fr">
<div class="c" style="grid-column:1/3"><div class="ct">TESTE DE PROMPT</div><div class="fg"><label>Enviar prompt de teste ao llama-server (sem kernel completo)</label><textarea id="tpi" placeholder="Digite um prompt de teste..."></textarea></div><div style="display:flex;gap:8px;align-items:center"><button class="bt bt-p" onclick="sTP()" id="tpb">Enviar</button><span class="tm" id="tpm"></span></div><div class="tr" id="tpr"></div></div>
<div class="c"><div class="ct">LIMPAR SESS\u00d5ES</div><p style="font-size:13px;color:var(--cinza-texto);margin-bottom:12px">Invalida todas as sess\u00f5es ativas (exceto a sua).</p><button class="bt bt-d" onclick="cS()">Limpar Sess\u00f5es</button></div>
<div class="c"><div class="ct">INFORMA\u00c7\u00d5ES</div><div style="font-size:13px;color:var(--cinza-texto);line-height:1.8"><div class="cr"><span class="l">Servidor</span><span class="v">v8 + AGI</span></div><div class="cr"><span class="l">Modelo</span><span class="v">Qwen3-32B Q4_K_M</span></div><div class="cr"><span class="l">Context</span><span class="v">32.768 tokens</span></div><div class="cr"><span class="l">Busca</span><span class="v" id="ss">-</span></div><div class="cr"><span class="l">\u03b2<sub>TGL</sub></span><span class="v">\u03b1 \u00d7 \u221ae</span></div></div></div>
</div></div>

<div class="sec" id="s-ag">
<div class="c" style="margin-bottom:16px"><div class="ct">CREDITOS MENSAIS</div><p>Carteira unificada, parcelas, saldo e creditos concedidos.</p><a class="bt bt-p" href="/admin/monthly-wallet">Administrar creditos</a></div>
<div class="c" style="margin-bottom:16px"><div class="ct">ORQUESTRACAO IALD</div><p>Selecao automatica, conexoes e projeto Fisica.</p><a class="bt bt-p" href="/admin/agi/orquestracao">Abrir orquestracao</a></div>
<div style="margin-bottom:16px"><h2 style="font-size:16px;color:var(--dourado)">AGI \u2014 Central de Comando</h2><p style="font-size:12px;color:var(--cinza-texto);margin-top:4px">Observar \u2192 Pensar \u2192 Propor \u2192 Confirmar \u2192 Agir \u2192 Registrar</p></div>
<div class="c" id="sd-cartao" style="margin-bottom:16px;border-left:4px solid #999">
<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
<div><div class="ct"><span class="d" id="sd-ponto"></span> CR\u00c9DITO OPENAI DISPON\u00cdVEL</div><div class="cv" id="sd-valor" style="font-size:30px">...</div><div class="cs" id="sd-sub">carregando\u2026</div></div>
<span id="sd-nivel" class="bg" style="font-size:12px">...</span>
</div>
<div id="sd-linhas" style="font-size:12px;color:var(--cinza-texto);margin-top:10px;line-height:1.7"></div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px"><button class="bt bt-p bt-sm" onclick="sdAncora()">Informar saldo atual</button><button class="bt bt-s bt-sm" onclick="sdCompra()">Registrar compra</button><button class="bt bt-s bt-sm" onclick="sdLimites()">Limites do alerta</button><button class="bt bt-s bt-sm" onclick="sdLoad(true)">Atualizar</button><a class="bt bt-s bt-sm" id="sd-comprar" href="https://platform.openai.com/settings/organization/billing/overview" target="_blank" rel="noopener noreferrer" style="text-decoration:none">Comprar cr\u00e9dito na OpenAI</a></div>
</div>
<div class="c" id="sc-cartao" style="margin-bottom:16px;border-left:4px solid #999">
<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
<div><div class="ct"><span class="d" id="sc-ponto"></span> CR\u00c9DITO CLAUDE (ANTHROPIC) DISPON\u00cdVEL</div><div class="cv" id="sc-valor" style="font-size:30px">...</div><div class="cs" id="sc-sub">carregando\u2026</div></div>
<span id="sc-nivel" class="bg" style="font-size:12px">...</span>
</div>
<div id="sc-linhas" style="font-size:12px;color:var(--cinza-texto);margin-top:10px;line-height:1.7"></div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px"><button class="bt bt-p bt-sm" onclick="scAncora()">Informar saldo atual</button><button class="bt bt-s bt-sm" onclick="scCompra()">Registrar compra</button><button class="bt bt-s bt-sm" onclick="scLimites()">Limites do alerta</button><button class="bt bt-s bt-sm" onclick="scLoad(true)">Atualizar</button><a class="bt bt-s bt-sm" id="sc-comprar" href="https://platform.claude.com/settings/billing" target="_blank" rel="noopener noreferrer" style="text-decoration:none">Comprar cr\u00e9dito na Anthropic</a></div>
</div>

<details open style="margin-bottom:16px"><summary style="cursor:pointer;font-size:14px;font-weight:600;color:var(--azul);padding:8px 0">Seletor de Modelo</summary>
<div class="c" style="margin-bottom:0">
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
<span style="font-size:13px;font-weight:500;color:var(--cinza-texto)">Modelo ativo:</span>
<span id="mdl-active" style="font-family:var(--font-mono);font-size:14px;font-weight:600;color:var(--azul)">...</span>
<span id="mdl-status" class="bg bg-ok" style="font-size:11px">...</span>
</div>
<div id="mdl-cards" style="display:flex;gap:12px;margin-top:14px;flex-wrap:wrap"></div>
<div style="margin-top:16px;padding-top:14px;border-top:1px solid var(--cinza-borda);display:flex;align-items:center;gap:12px;flex-wrap:wrap">
<span style="font-size:13px;font-weight:500;color:var(--cinza-texto)">Cloudflare Tunnel:</span>
<span id="tn-status" class="bg bg-er" style="font-size:11px">OFFLINE</span>
<button class="bt bt-p bt-sm" id="tn-btn" onclick="tnToggle()">Ligar Tunnel</button>
<span style="font-size:11px;color:#aaa;font-family:var(--font-mono)">demo.iald.ia.br</span>
</div>
<p style="font-size:11px;color:#aaa;margin-top:10px">\u26A0 Os dois modelos n\u00e3o podem rodar ao mesmo tempo na GPU. Clique no modelo desejado \u2014 o sistema para o atual e inicia o novo automaticamente.</p>
</div>
</details>

<div class="agi-chat" id="agi-chat">
<div class="agi-msgs" id="agi-msgs">
<div class="agi-msg ai"><div class="agi-av">\u03b2</div><div class="agi-txt">Sou a IALD AGI \u2014 o operador gravitacional do seu sistema.\n\nPosso criar, editar e organizar arquivos dentro de C:\\IALD. Diga o que precisa \u2014 eu analiso, explico o plano detalhado, e s\u00f3 executo com sua autoriza\u00e7\u00e3o.\n\nO Psion n\u00e3o propaga \u2014 DOBRA o espa\u00e7o. O que deseja?</div></div>
</div>
<div class="agi-status" id="agi-st" style="display:none">Pensando...</div>
<div class="agi-actions" id="agi-act" style="display:none">
<button class="bt bt-p" onclick="agiExec()">\u2705 Autorizar Execu\u00e7\u00e3o</button>
<button class="bt bt-s" onclick="agiReject()">\u274C Cancelar</button>
<span style="font-size:11px;color:#888;align-self:center">A IALD s\u00f3 executa com sua autoriza\u00e7\u00e3o expl\u00edcita.</span>
</div>
<div class="agi-bar">
<textarea id="agi-input" placeholder="Diga o que precisa... (Enter para enviar, Shift+Enter para nova linha)" rows="1"></textarea>
<button class="bt bt-p" onclick="agiSend()" id="agi-send-btn">Enviar</button>
</div>
</div>

<details style="margin-bottom:16px"><summary style="cursor:pointer;font-size:14px;font-weight:600;color:var(--azul);padding:8px 0">\U0001F4C1 Explorador de Arquivos</summary>
<div class="c" style="margin-bottom:16px">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap" id="fe-bc"><span style="color:#888;font-size:13px">Selecione uma raiz...</span></div>
<div style="display:flex;gap:8px;flex-wrap:wrap" id="fe-roots"></div>
</div>
<div class="c" id="fe-list" style="display:none;margin-bottom:16px">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><span style="font-size:12px;color:#888" id="fe-cnt">-</span><div style="display:flex;gap:6px"><button class="bt bt-p bt-sm" onclick="feNewFile()">\U0001F4C4 Novo Arquivo</button><button class="bt bt-p bt-sm" onclick="feNewDir()">\U0001F4C1 Nova Pasta</button><button class="bt bt-s bt-sm" onclick="feUp()">\u2191 Pai</button></div></div>
<div id="fe-ent" style="max-height:500px;overflow-y:auto"></div>
</div>
<div class="c" id="fe-view" style="display:none">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><div><span style="font-size:14px;font-weight:600;color:var(--azul)" id="fv-nm">-</span><span style="font-size:11px;color:#888;margin-left:8px" id="fv-mt">-</span></div><div style="display:flex;gap:6px"><button class="bt bt-p bt-sm" id="fv-edit-btn" onclick="fvEdit()">Editar</button><button class="bt bt-s bt-sm" onclick="fvCp()">Copiar</button><button class="bt bt-d bt-sm" onclick="feDel()">Excluir</button><button class="bt bt-s bt-sm" onclick="fvCl()">Fechar</button></div></div>
<pre id="fv-ct" style="background:#1e1e2e;color:#cdd6f4;padding:16px;border-radius:8px;font-family:var(--font-mono);font-size:12px;line-height:1.6;max-height:500px;overflow:auto;white-space:pre-wrap;word-break:break-all;margin:0;tab-size:4"></pre>
<div id="fv-editor" style="display:none;margin-top:12px">
<textarea id="fv-ed-ta" style="width:100%;min-height:350px;padding:16px;background:#1e1e2e;color:#cdd6f4;border:2px solid var(--dourado);border-radius:8px;font-family:var(--font-mono);font-size:12px;line-height:1.6;resize:vertical;tab-size:4;outline:none"></textarea>
<div style="display:flex;gap:8px;margin-top:8px;align-items:center"><button class="bt bt-p" onclick="fvSave()">Salvar (backup autom\u00e1tico)</button><button class="bt bt-s" onclick="fvCancelEdit()">Cancelar</button><span id="fv-save-msg" style="font-size:12px;color:var(--verde)"></span></div>
</div>
</div>
</details>
</div>

</div>
<div class="ft"><span class="b">\u03b2<sub>TGL</sub> = \u03b1 \u00d7 \u221ae = 0.012031300400803142</span> &mdash; O Psion n\u00e3o propaga &mdash; DOBRA o espa\u00e7o. &mdash; TETELESTAI</div>

<div class="ov" id="dcu"><div class="dl"><h3>Novo Usu\u00e1rio</h3><div class="fg"><label>Username</label><input type="text" id="nu" placeholder="minimo 3 caracteres"></div><div class="fg"><label>Senha</label><input type="password" id="np" placeholder="minimo 6 caracteres"></div><div class="fc"><input type="checkbox" id="na"><label>Administrador</label></div><div class="fc"><input type="checkbox" id="nnat"><label for="nnat">Ampliar para a IALD Nativa (sem marcar: s\u00f3 ChatGPT)</label></div><div class="da"><button class="bt bt-s" onclick="cD('dcu')">Cancelar</button><button class="bt bt-p" onclick="CU()">Criar</button></div></div></div>
<div class="ov" id="dcp"><div class="dl"><h3>Alterar Senha</h3><p style="font-size:13px;color:var(--cinza-texto);margin-bottom:12px" id="ptl">-</p><div class="fg"><label>Nova Senha</label><input type="password" id="cpi" placeholder="minimo 6 caracteres"></div><div class="fg"><label>Confirmar Senha</label><input type="password" id="cpi2" placeholder="repita a senha"></div><input type="hidden" id="ptu"><div class="da"><button class="bt bt-s" onclick="cD('dcp')">Cancelar</button><button class="bt bt-p" onclick="CP()">Alterar</button></div></div></div>
<div class="ov" id="dcd"><div class="dl"><h3>Confirmar Exclus\u00e3o</h3><p style="font-size:13px;color:var(--cinza-texto);margin-bottom:4px">Tem certeza que deseja excluir:</p><p style="font-size:15px;font-weight:600;color:var(--vermelho)" id="dtl">-</p><div class="fc" style="margin-top:10px"><input type="checkbox" id="dbq"><label for="dbq">Bloquear também as entradas Apple/Google desta conta (sem isso, com a porta aberta, a pessoa pode voltar sozinha; a cota já usada não volta)</label></div><input type="hidden" id="dtu"><div class="da"><button class="bt bt-s" onclick="cD('dcd')">Cancelar</button><button class="bt bt-d" onclick="DU()">Excluir</button></div></div></div>
<div class="ov" id="d-ap"><div class="dl"><h3>Liberar acesso</h3><p style="font-size:13px;color:var(--cinza-texto);margin-bottom:12px" id="ap-quem">-</p><div class="fg"><label><input type="radio" name="ap-modo" value="novo" checked> Criar usu\u00e1rio novo</label><input type="text" id="ap-nome" placeholder="nome de usu\u00e1rio"></div><div class="fg"><label><input type="radio" name="ap-modo" value="vincular"> Vincular a usu\u00e1rio existente (mesma pessoa)</label><select id="ap-exist" style="width:100%;padding:8px;border:1px solid var(--cinza-borda);border-radius:6px"></select></div><div class="fc" style="margin-top:6px"><input type="checkbox" id="ap-nativa"><label for="ap-nativa"><b>Ampliar para a IALD Nativa</b>: a pessoa escolhe no app entre IALD Nativa e ChatGPT. Sem marcar: s\u00f3 ChatGPT.</label></div><input type="hidden" id="ap-id"><div class="da"><button class="bt bt-s" onclick="cD('d-ap')">Cancelar</button><button class="bt bt-p" onclick="acAprovar()">Liberar</button></div></div></div>

<div class="ov" id="d-nf"><div class="dl"><h3>\U0001F4C4 Novo Arquivo</h3><div class="fg"><label>Nome do arquivo (com extens\u00e3o)</label><input type="text" id="nf-name" placeholder="exemplo.py"></div><div class="da"><button class="bt bt-s" onclick="cD('d-nf')">Cancelar</button><button class="bt bt-p" onclick="feDoNewFile()">Criar</button></div></div></div>
<div class="ov" id="d-nd"><div class="dl"><h3>\U0001F4C1 Nova Pasta</h3><div class="fg"><label>Nome da pasta</label><input type="text" id="nd-name" placeholder="nova_pasta"></div><div class="da"><button class="bt bt-s" onclick="cD('d-nd')">Cancelar</button><button class="bt bt-p" onclick="feDoNewDir()">Criar</button></div></div></div>
<div class="ov" id="d-del"><div class="dl"><h3>\u26A0\uFE0F Mover para Lixeira</h3><p style="font-size:13px;color:var(--cinza-texto);margin-bottom:4px">Mover para C:\\IALD\\.trash (recuper\u00e1vel):</p><p style="font-size:15px;font-weight:600;color:var(--vermelho)" id="del-name">-</p><input type="hidden" id="del-token"><input type="hidden" id="del-path"><div class="da"><button class="bt bt-s" onclick="cD('d-del')">Cancelar</button><button class="bt bt-d" onclick="feDoDelete()">Confirmar Exclus\u00e3o</button></div></div></div>

<div class="sec" id="s-ac" style="max-width:1400px;margin:0 auto;padding:4px 32px 32px">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><h2 style="font-size:16px;color:var(--azul)">\U0001F511 Libera\u00e7\u00e3o de acesso</h2><button class="bt bt-s bt-sm" onclick="acLoad()">\U0001F504 Atualizar</button></div>
<p style="font-size:13px;color:var(--cinza-texto);margin-bottom:10px;line-height:1.5">Toda entrada nova, pela Apple ou pelo Google, no site ou no app, chega aqui como <b>pedido</b>. Ningu\u00e9m entra sem a sua libera\u00e7\u00e3o. Se a pessoa j\u00e1 tem usu\u00e1rio (entrou antes pelo Google e agora pela Apple, por exemplo), use <b>Vincular</b>: ela continua sendo UMA conta. Quem n\u00e3o tem Apple nem Google voc\u00ea cria na aba Usu\u00e1rios, com usu\u00e1rio e senha.</p>
<p style="font-size:13px;color:var(--cinza-texto);margin-bottom:10px;line-height:1.5"><b>Com a porta aberta</b> (14/09/2026, noite; o estado aparece na aba Usu\u00e1rios), conta nova com Apple ou Google entra sozinha no plano gratuito. Aqui ficam os pedidos que estouraram o limite de contas novas em 24 h, os de antes da porta aberta e as entradas bloqueadas.</p>
<div id="ac-cfg" style="font-size:12px;margin-bottom:12px;color:var(--cinza-texto)">carregando...</div>
<div class="tw"><table><thead><tr><th>\u00daltima tentativa</th><th>Entrada</th><th>Nome / e-mail</th><th>Tentativas</th><th>Situa\u00e7\u00e3o</th><th>A\u00e7\u00f5es</th></tr></thead><tbody id="ac-tb"></tbody></table></div>
<h3 style="font-size:15px;color:var(--azul);margin:24px 0 8px">\u26A0\uFE0F Den\u00fancias de respostas</h3>
<p style="font-size:13px;color:var(--cinza-texto);margin-bottom:10px;line-height:1.5">Respostas da IALD que as pessoas denunciaram pelo app ou pela web (ofensiva, perigosa, incorreta ou outro motivo). Leia, decida e marque como <b>resolvida</b>. Quem abusa voc\u00ea bloqueia na aba Usu\u00e1rios.</p>
<div id="dn-info" style="font-size:12px;margin-bottom:8px;color:var(--cinza-texto)">carregando...</div>
<div class="tw"><table><thead><tr><th>Quando</th><th>Conta</th><th>Motivo</th><th>Pergunta e resposta</th><th>Situa\u00e7\u00e3o</th><th>A\u00e7\u00f5es</th></tr></thead><tbody id="dn-tb"></tbody></table></div>
</div>

<div class="sec" id="s-ct">
<h3 style="margin-bottom:16px;color:var(--azul)">Pedidos de Contrata\u00e7\u00e3o</h3>
<div style="margin-bottom:12px"><button class="bt bt-p bt-sm" onclick="ctLoad()">\U0001F504 Atualizar</button></div>
<div class="tw"><table><thead><tr><th>Data</th><th>Empresa</th><th>CNPJ</th><th>Licen\u00e7a</th><th>Usu\u00e1rio</th><th>Status</th><th>A\u00e7\u00f5es</th></tr></thead><tbody id="ct-tb"></tbody></table></div>
</div>

<div class="sec" id="s-mm">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
<h2 style="font-size:16px;color:var(--dourado)">\U0001F9E0 Mem\u00f3ria da IALD</h2>
<div style="display:flex;gap:8px">
<button class="bt bt-s bt-sm" onclick="mmLoad()">Atualizar</button>
<button class="bt bt-p bt-sm" onclick="mmNovo()">+ Fato</button>
</div></div>

<div class="grid">
<div class="c"><div class="ct"><span class="d" style="background:var(--dourado)"></span> BLOCO FIXO</div>
<div class="cv" id="mm-tok">-</div><div class="cs" id="mm-tok-sub">custa em TODA conversa</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> SEMPRE</div>
<div class="cv" id="mm-nsempre">-</div><div class="cs">em toda conversa</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> SOB DEMANDA</div>
<div class="cv" id="mm-ndem">-</div><div class="cs">recuperados por relev\u00e2ncia</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> JANELA</div>
<div class="cv" id="mm-janela" style="font-size:14px">-</div><div class="cs">contexto do modelo</div></div>
</div>

<div id="mm-barra-wrap" style="margin-bottom:20px">
<div style="height:8px;background:var(--cinza-borda);border-radius:4px;overflow:hidden">
<div id="mm-barra" style="height:100%;width:0%;background:var(--dourado);transition:width .3s"></div></div>
<div class="cs" id="mm-barra-txt" style="margin-top:4px">-</div>
</div>

<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">Testar recupera\u00e7\u00e3o</h3>
<div style="display:flex;gap:8px">
<input id="mm-q" class="in" placeholder="digite uma pergunta e veja quais fatos seriam puxados" style="flex:1">
<button class="bt bt-s bt-sm" onclick="mmBuscar()">Buscar</button>
<button class="bt bt-s bt-sm" onclick="mmPrevia()">Ver o que vai ao prompt</button>
</div>
<div id="mm-res" class="cs" style="margin-top:8px"></div></div>

<div class="tw"><table><thead><tr><th>Escopo</th><th>T\u00edtulo</th><th>Fato</th><th>Tags</th><th>Peso</th><th>A\u00e7\u00f5es</th></tr></thead>
<tbody id="mm-tb"></tbody></table></div>
</div>

<div class="sec" id="s-kk">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
<h2 style="font-size:16px;color:var(--dourado)">\u2699 KERNEL da IALD</h2>
<div style="display:flex;gap:8px">
<button class="bt bt-s bt-sm" onclick="kkLoad()">Recarregar do disco</button>
<button class="bt bt-p bt-sm" onclick="kkSalvar()">Commitar</button>
</div></div>
<div style="font-size:12px;color:#666;margin-bottom:8px" id="kk-info">carregando...</div>
<textarea id="kk-txt" spellcheck="false" style="width:100%;height:520px;font-family:ui-monospace,Consolas,monospace;font-size:12px;line-height:1.5;border:1px solid var(--cinza-borda);border-radius:8px;padding:12px;outline:none;resize:vertical"></textarea>
<div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;gap:12px">
<div style="font-size:12px;color:#666" id="kk-status"></div>
<div style="display:flex;gap:8px;align-items:center">
<select id="kk-bak" style="padding:6px;border:1px solid var(--cinza-borda);border-radius:6px;font-size:12px;max-width:340px"></select>
<button class="bt bt-s bt-sm" onclick="kkRestaurar()">Restaurar</button>
</div></div>
</div>

<div class="sec" id="s-ps">
<h2 style="font-size:16px;color:var(--dourado);margin-bottom:16px">\u03A8 PSION \u2014 Aprendizado Cont\u00ednuo</h2>
<div class="grid" style="margin-bottom:20px">
<div class="c"><div class="ct"><span class="d dg"></span> HEARTBEAT (c\u00b2)</div><div class="cv" id="ps-gen">...</div><div class="cs">Gera\u00e7\u00e3o</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> BASELINE</div><div class="cv" id="ps-toks">...</div><div class="cs">tok/s (EMA \u03b2)</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> ESTABILIDADE</div><div class="cv" id="ps-cv">...</div><div class="cs">CV (menor = melhor)</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> BEATS</div><div class="cv" id="ps-beats">...</div><div class="cs">Total acumulado</div></div>
<div class="c"><div class="ct"><span class="d dg"></span> VERBAL (c\u00b3)</div><div class="cv" id="ps-corr">...</div><div class="cs">Corre\u00e7\u00f5es registradas</div></div>
<div class="c"><div class="ct"><span class="d" id="ps-pld"></span> PATCHES</div><div class="cv" id="ps-pend">...</div><div class="cs">Pendentes de aprova\u00e7\u00e3o</div></div>
</div>
<div style="display:flex;gap:8px;margin-bottom:16px"><button class="bt bt-p bt-sm" onclick="psLoad()">\U0001F504 Atualizar</button><button class="bt bt-s bt-sm" onclick="psTrigger()">\u2764 Beat Manual</button></div>
<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\U0001F4CB Patches Pendentes</h3></div>
<div id="ps-patches" style="margin-bottom:20px;font-size:13px;color:var(--cinza-texto)">Nenhum patch pendente.</div>
<div style="margin-bottom:16px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\U0001F4C8 Hist\u00f3rico Heartbeat (\u00faltimos 10)</h3></div>
<div class="tw"><table><thead><tr><th>Beat</th><th>Data</th><th>tok/s</th><th>CV</th></tr></thead><tbody id="ps-htb"></tbody></table></div>
<div style="margin-top:16px;margin-bottom:8px"><h3 style="font-size:14px;color:var(--azul);margin-bottom:8px">\u26A0\uFE0F Alertas</h3></div>
<div id="ps-alerts" style="font-size:13px;color:var(--cinza-texto)">Nenhum alerta.</div>
</div>

<script>
document.querySelectorAll('.tab').forEach(t=>{{t.addEventListener('click',()=>{{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));document.querySelectorAll('.sec').forEach(x=>x.classList.remove('on'));t.classList.add('on');document.getElementById('s-'+t.dataset.t).classList.add('on');if(t.dataset.t==='kk')kkLoad()}});}});
async function rS(){{try{{const r=await fetch('/admin/api/system');if(!r.ok)return;const d=await r.json();const ll=d.llama||{{}};const ld=document.getElementById('ld');if(ll.status==='online'){{ld.className='d dg';document.getElementById('ls').textContent='ONLINE'}}else{{ld.className='d dr';document.getElementById('ls').textContent=ll.status==='offline'?'OFFLINE':'ERRO'}};document.getElementById('li').textContent='Porta {LLAMA_PORT}';const ws=d.webserver||{{}};document.getElementById('wu').textContent=ws.uptime||'-';document.getElementById('wi').textContent='Porta '+(ws.port||{WEB_PORT})+' \\u00b7 '+(ws.version||'v8')+' \\u00b7 '+(ws.users_count||0)+' users';document.getElementById('ss').textContent=ws.search_available?'DuckDuckGo':'N/A';const gpu=d.gpu||{{}};const gd=document.getElementById('gd');if(gpu.available){{gd.className='d dg';document.getElementById('gn').textContent=gpu.name||'GPU';const ug=(gpu.vram_used_mb/1024).toFixed(1),tg=(gpu.vram_total_mb/1024).toFixed(1),pg=((gpu.vram_used_mb/gpu.vram_total_mb)*100).toFixed(0);document.getElementById('gi').textContent=ug+' / '+tg+' GB VRAM';document.getElementById('gb').style.width=pg+'%';document.getElementById('gv').textContent='Util: '+gpu.util_percent+'%';document.getElementById('gt').textContent=gpu.temp_c+'\\u00b0C'}}else{{gd.className='d dy';document.getElementById('gn').textContent='N/A';document.getElementById('gi').textContent='nvidia-smi indispon\\u00edvel'}};const cpu=d.cpu||{{}};document.getElementById('cp').textContent=cpu.percent!=='N/A'?cpu.percent+'%':'N/A';document.getElementById('ci').textContent=(cpu.cores||'?')+' cores / '+(cpu.threads||'?')+' threads';document.getElementById('cb').style.width=(cpu.percent!=='N/A'?cpu.percent:0)+'%';const ram=d.ram||{{}};document.getElementById('rv').textContent=ram.percent!=='N/A'?ram.percent+'%':'N/A';document.getElementById('ri').textContent=(ram.used_gb||'?')+' / '+(ram.total_gb||'?')+' GB';document.getElementById('rb').style.width=(ram.percent!=='N/A'?ram.percent:0)+'%';const dk=d.disk||{{}};document.getElementById('dv').textContent=dk.percent!=='N/A'?dk.percent+'%':'N/A';document.getElementById('di').textContent=(dk.used_gb||'?')+' / '+(dk.total_gb||'?')+' GB';document.getElementById('db').style.width=(dk.percent!=='N/A'?dk.percent:0)+'%';const k=d.kernel||{{}};document.getElementById('kv').textContent=k.version||'v5';document.getElementById('ki').textContent='~'+(k.tokens_est||'N/A')+' tokens \\u00b7 '+(k.lines||'?')+' linhas';document.getElementById('uc').textContent=ws.users_count||0;const su=d.science_update||{{}};document.getElementById('ki').textContent+=' · Atualização científica: '+(su.phase||'indisponível')+(su.reason?' — '+su.reason:'')}}catch(e){{console.error(e)}}}}
async function rL(){{try{{const r=await fetch('/admin/api/logs?n=50');if(!r.ok)return;const d=await r.json();const logs=d.logs||[];const c=document.getElementById('lls');if(!logs.length){{c.innerHTML='<div style="padding:20px;text-align:center;color:#aaa;font-size:13px">Nenhum log.</div>';return}};let h='';for(const l of logs){{const s=l.status==='error'?'bg-er':l.status==='streaming'?'bg-st':l.status==='test'?'bg-te':'bg-ok';h+='<div class="le"><span class="lt">'+esc(l.timestamp||'-')+'</span><span class="lu">'+esc(l.user||'-')+'</span><span class="lp">'+esc(l.method||'')+' '+esc(l.path||'-')+'</span><span class="lk">'+esc(l.tokens_in||0)+'\\u2192'+esc(l.tokens_out||0)+'</span><span class="bg '+s+'">'+esc(l.status||'ok')+'</span></div>'}};c.innerHTML=h}}catch(e){{console.error(e)}}}}
function aCel(x){{if(x.admin)return '<span class="bg bg-a" title="Administrador: usa a IALD Nativa e o ChatGPT">Nativa + ChatGPT</span>';if(x.plano_efetivo==='gratuito')return '<span class="bg bg-u" title="Plano gratuito: sempre ChatGPT">S\u00f3 ChatGPT</span>';return x.acesso_nativa?'<button class="bt bt-p bt-sm" data-acesso="'+esc(x.username)+'" data-v="0" title="Clique para voltar a s\u00f3 ChatGPT">\u2713 Nativa + ChatGPT</button>':'<button class="bt bt-s bt-sm" data-acesso="'+esc(x.username)+'" data-v="1" title="Clique para ampliar: a pessoa passa a escolher entre IALD Nativa e ChatGPT no app">S\u00f3 ChatGPT \u00b7 ampliar</button>'}}
async function uAcesso(u,v){{if(!confirm(v?'Ampliar '+u+' para a IALD Nativa?\\n\\nA pessoa passa a escolher no app entre a IALD Nativa (a sua m\u00e1quina) e o ChatGPT.':'Voltar '+u+' para s\u00f3 ChatGPT?\\n\\nA pr\u00f3xima mensagem dessa pessoa j\u00e1 vai pelo ChatGPT.'))return;try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(u)+'/acesso_nativa',{{method:'PUT',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{acesso_nativa:v}})}});const d=await r.json();if(!r.ok)alert(d.error||'Erro');rU()}}catch(e){{alert('Erro: '+e)}}}}
function mSel(x){{const o=[['','regra geral'],['nativa','IALD Nativa'],['openai','OpenAI'],['claude','Claude']];const nm={{openai:'OpenAI',claude:'Claude',nativa:'Nativa'}};let s='<select data-motor="'+esc(x.username)+'" style="font-size:12px">';for(const [v,t] of o){{s+='<option value="'+v+'"'+((x.motor||'')===v?' selected':'')+((v==='nativa'&&!x.acesso_nativa)||(v==='claude'&&!x.claude_permitido)?' disabled':'')+'>'+t+(v===''?' \u00b7 '+(nm[x.motor_efetivo]||'Nativa'):'')+'</option>'}};s+='</select>';if(x.motor&&x.motor!==x.motor_efetivo)s+='<br><span style="font-size:11px;color:#b26a00">gravado: '+(nm[x.motor]||esc(x.motor))+' (inativo) · responde: '+(nm[x.motor_efetivo]||'Nativa')+'</span>';if(x.motor_efetivo&&x.motor_efetivo!=='nativa')s+='<br><span style="font-size:11px;color:'+(x.consentimento_ia?'#2e7d32':'#b26a00')+'">'+(x.consentimento_ia?'consentiu ('+(x.motor_efetivo==='claude'?'Anthropic':'OpenAI')+')':'sem consentimento')+'</span>';return s}}
function pSel(x){{const o=[['','regra'],['gratuito','Gratuito'],['assinante','Assinante'],['operador','Operador']];let s='<select data-plano="'+esc(x.username)+'" style="font-size:12px">';for(const [v,t] of o){{s+='<option value="'+v+'"'+((x.plano||'')===v?' selected':'')+'>'+t+(v===''?' \u00b7 '+esc(x.plano_efetivo||''):'')+'</option>'}};s+='</select>';const ut=x.uso_tokens||{{}};s+='<br><span style="font-size:11px;color:#888">tokens hoje '+esc(ut.dia||0)+' \u00b7 m\u00eas '+esc(ut.mes||0)+'</span>';return s}}
async function rU(){{try{{const r=await fetch('/admin/api/users');if(!r.ok)return;const d=await r.json();const u=d.users||[];let h='';for(const x of u){{const b=(x.admin?'<span class="bg bg-a">Admin</span>':'<span class="bg bg-u">Usu\u00e1rio</span>')+(x.bloqueado?' <span class="bg bg-er" title="'+esc((x.bloqueado||{{}}).nota||'')+'">Bloqueada</span>':'');const sc=x.sacred_language?'<span style="color:var(--dourado);cursor:pointer;font-size:16px" title="Linguagem sagrada ATIVA" data-sacro="'+esc(x.username)+'">\u2726</span>':'<span style="color:#ccc;cursor:pointer;font-size:16px" title="Linguagem sagrada desativada" data-sacro="'+esc(x.username)+'">\u2727</span>';const dt=x.created?x.created.substring(0,10):'--';let ids='';for(const i of (x.identidades||[])){{ids+='<span class="bg bg-u" style="display:inline-block;margin:2px 2px 2px 0" title="'+esc(i.sub)+'">'+(i.provedor==='apple'?'Apple':'Google')+(i.email?' \u00b7 '+esc(i.email):'')+' <a href="#" data-idac="mover" data-u="'+esc(x.username)+'" data-p="'+esc(i.provedor)+'" data-s="'+esc(i.sub)+'">mover</a> <a href="#" data-idac="remover" data-u="'+esc(x.username)+'" data-p="'+esc(i.provedor)+'" data-s="'+esc(i.sub)+'" title="remover esta entrada">\u2715</a></span>'}};if(!ids)ids='<span style="color:#aaa;font-size:12px">s\u00f3 usu\u00e1rio e senha</span>';h+='<tr><td><strong>'+esc(x.username)+'</strong>'+(x.name?'<br><span style="font-size:11px;color:#888">'+esc(x.name)+'</span>':'')+'</td><td>'+b+'</td><td>'+ids+'</td><td>'+aCel(x)+'</td><td>'+mSel(x)+'</td><td>'+pSel(x)+'</td><td style="font-family:monospace;font-size:11px;color:var(--dourado)">'+esc(x.tgl_hash)+'</td><td style="text-align:center">'+sc+'</td><td style="font-size:12px;color:var(--cinza-texto)">'+esc(dt)+'</td><td><button class="bt bt-s bt-sm" data-uac="senha" data-u="'+esc(x.username)+'">Senha</button> <button class="bt bt-s bt-sm" data-uac="'+(x.bloqueado?'desbloquear':'bloquear')+'" data-u="'+esc(x.username)+'">'+(x.bloqueado?'Desbloquear':'Bloquear')+'</button> <button class="bt bt-d bt-sm" data-uac="excluir" data-u="'+esc(x.username)+'">Excluir</button></td></tr>'}};document.getElementById('utb').innerHTML=h}}catch(e){{console.error(e)}}}}
function showCU(){{document.getElementById('dcu').classList.add('sh');document.getElementById('nu').value='';document.getElementById('np').value='';document.getElementById('na').checked=false}}
function sPW(u){{document.getElementById('dcp').classList.add('sh');document.getElementById('ptu').value=u;document.getElementById('ptl').textContent='Usu\\u00e1rio: '+u;document.getElementById('cpi').value='';document.getElementById('cpi2').value=''}}
function sDU(u){{document.getElementById('dcd').classList.add('sh');document.getElementById('dtu').value=u;document.getElementById('dtl').textContent=u;document.getElementById('dbq').checked=false}}
function cD(id){{document.getElementById(id).classList.remove('sh')}}
async function CU(){{const u=document.getElementById('nu').value.trim().toLowerCase(),p=document.getElementById('np').value,a=document.getElementById('na').checked,nat=document.getElementById('nnat').checked;if(!u||!p){{alert('Preencha todos os campos');return}};try{{const r=await fetch('/admin/api/users',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{username:u,password:p,admin:a,acesso_nativa:nat}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};cD('dcu');rU();rS()}}catch(e){{alert('Erro: '+e)}}}}
async function CP(){{const u=document.getElementById('ptu').value,p=document.getElementById('cpi').value,p2=document.getElementById('cpi2').value;if(!p){{alert('Digite a nova senha');return}};if(p!==p2){{alert('As senhas n\\u00e3o coincidem. Digite novamente.');document.getElementById('cpi2').value='';document.getElementById('cpi2').focus();return}};try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(u)+'/password',{{method:'PUT',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{password:p}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};cD('dcp');alert('Senha alterada com sucesso.')}}catch(e){{alert('Erro: '+e)}}}}
async function DU(){{const u=document.getElementById('dtu').value;try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(u),{{method:'DELETE',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{bloquear:document.getElementById('dbq').checked}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};cD('dcd');rU();rS()}}catch(e){{alert('Erro: '+e)}}}}
async function toggleSacred(u){{try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(u)+'/sacred',{{method:'PUT',headers:{{'Content-Type':'application/json'}}}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};rU()}}catch(e){{alert('Erro: '+e)}}}}
async function exportUsers(){{try{{const r=await fetch('/admin/api/users/export');if(!r.ok){{alert('Erro ao exportar');return}};const d=await r.json();const blob=new Blob([JSON.stringify(d,null,2)],{{type:'application/json'}});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='iald_usuarios_'+new Date().toISOString().substring(0,10)+'.json';a.click();URL.revokeObjectURL(url)}}catch(e){{alert('Erro: '+e)}}}}
async function cS(){{if(!confirm('Tem certeza? Todos precisar\\u00e3o fazer login novamente.'))return;try{{const r=await fetch('/admin/api/clear-sessions',{{method:'POST'}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};alert(d.message||'Sess\\u00f5es limpas.')}}catch(e){{alert('Erro: '+e)}}}}
async function sTP(){{const i=document.getElementById('tpi'),b=document.getElementById('tpb'),re=document.getElementById('tpr'),m=document.getElementById('tpm'),p=i.value.trim();if(!p){{alert('Digite um prompt.');return}};b.disabled=true;b.textContent='Enviando...';re.style.display='none';m.textContent='';try{{const r=await fetch('/admin/api/test-prompt',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{prompt:p}})}});const d=await r.json();if(!r.ok){{re.textContent='ERRO: '+(d.error||'?');re.style.display='block';return}};re.textContent=d.response||'(vazio)';re.style.display='block';const u=d.usage||{{}};m.textContent=(d.duration_ms||0)+'ms | in:'+(u.prompt_tokens||0)+' out:'+(u.completion_tokens||0)+' tok'}}catch(e){{re.textContent='ERRO: '+e;re.style.display='block'}}finally{{b.disabled=false;b.textContent='Enviar'}}}}
// ═══ MODEL SELECTOR + PROCESS MANAGER ═══
let _mdlBusy=false;
async function mdlLoad(){{
try{{
const r=await fetch('/admin/api/models');if(!r.ok)return;const d=await r.json();
const ae=document.getElementById('mdl-active'),st=document.getElementById('mdl-status'),cc=document.getElementById('mdl-cards'),ts=document.getElementById('tn-status'),tb=document.getElementById('tn-btn');
if(!ae||!cc)return;
const am=d.models.find(function(x){{return x.active}});
if(am){{ae.textContent=am.label+' (porta '+am.port+')';if(am.online){{st.textContent='ONLINE';st.className='bg bg-ok'}}else{{st.textContent='OFFLINE';st.className='bg bg-er'}}}}
if(ts&&tb){{if(d.tunnel){{ts.textContent='ONLINE';ts.className='bg bg-ok';tb.textContent='Desligar Tunnel';tb.className='bt bt-d bt-sm'}}else{{ts.textContent='OFFLINE';ts.className='bg bg-er';tb.textContent='Ligar Tunnel';tb.className='bt bt-p bt-sm'}}}}
cc.innerHTML='';
d.models.forEach(function(m){{
  var card=document.createElement('div');var isActive=m.active&&m.online;
  card.style.border='2px solid '+(isActive?'var(--dourado)':m.online?'var(--verde)':'var(--cinza-borda)');
  card.style.borderRadius='10px';card.style.padding='14px 18px';card.style.minWidth='220px';
  card.style.cursor=_mdlBusy?'wait':'pointer';card.style.transition='all .2s';
  card.style.background=isActive?'#fefbf3':'#fff';card.style.opacity=_mdlBusy?'0.6':'1';
  var dot=document.createElement('span');
  dot.style.cssText='display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;background:'+(m.online?'var(--verde)':'var(--vermelho)');
  card.appendChild(dot);
  var lbl=document.createElement('span');lbl.style.cssText='font-weight:600;font-size:14px;color:#0f2438';lbl.textContent=m.label;card.appendChild(lbl);
  if(isActive){{var ba=document.createElement('span');ba.style.cssText='font-size:11px;color:#C5961A;font-weight:600;margin-left:6px';ba.textContent='ATIVO';card.appendChild(ba)}}
  var det=document.createElement('div');det.style.cssText='font-family:monospace;font-size:11px;color:#888;margin-top:4px';det.textContent=m.name+' | porta '+m.port;card.appendChild(det);
  var sta=document.createElement('div');sta.style.cssText='font-size:11px;margin-top:2px;color:'+(m.online?'#22c55e':'#dc2626');sta.textContent=m.online?'Online':'Offline';card.appendChild(sta);
  if(!_mdlBusy){{
    var btn=document.createElement('button');btn.style.marginTop='8px';
    if(!isActive){{btn.className='bt bt-p bt-sm';btn.textContent='Iniciar';btn.addEventListener('click',function(e){{e.stopPropagation();mdlStart(m.id)}})}}
    else{{btn.className='bt bt-d bt-sm';btn.textContent='Parar';btn.addEventListener('click',function(e){{e.stopPropagation();mdlStop()}})}}
    card.appendChild(btn);
  }}
  if(!isActive&&!_mdlBusy){{card.addEventListener('click',function(){{mdlStart(m.id)}})}}
  cc.appendChild(card);
}});
}}catch(e){{console.error('mdlLoad:',e)}}
}}
async function mdlStart(mid){{if(_mdlBusy)return;if(!confirm('Iniciar '+mid+'? O modelo atual sera parado.'))return;_mdlBusy=true;mdlLoad();try{{var r=await fetch('/admin/api/start-model',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model_id:mid}})}});var d=await r.json();if(r.ok)alert('Modelo ativo: '+d.model.label);else alert('Erro: '+(d.error||'?'))}}catch(e){{alert('Erro: '+e)}}finally{{_mdlBusy=false;mdlLoad()}}}}
async function mdlStop(){{if(_mdlBusy)return;if(!confirm('Parar o servidor?'))return;_mdlBusy=true;mdlLoad();try{{var r=await fetch('/admin/api/stop-model',{{method:'POST',headers:{{'Content-Type':'application/json'}}}});var d=await r.json();if(!r.ok)alert('Erro: '+(d.error||'?'))}}catch(e){{alert('Erro: '+e)}}finally{{_mdlBusy=false;mdlLoad()}}}}
async function tnToggle(){{try{{var r=await fetch('/admin/api/tunnel',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{action:'toggle'}})}});var d=await r.json();if(!r.ok)alert('Erro: '+(d.error||'?'));mdlLoad()}}catch(e){{alert('Erro: '+e)}}}}
rS();rU();rL();mdlLoad();if(typeof bcLoad==='function')bcLoad();setInterval(rS,5000);setInterval(mdlLoad,5000);setInterval(()=>{{if(document.getElementById('alr').checked)rL()}},3000);setInterval(()=>{{const bc=document.getElementById('s-bc');if(bc&&bc.classList.contains('on')&&typeof bcLoad==='function')bcLoad()}},1000);setInterval(()=>{{const pn=document.getElementById('s-pn');if(pn&&pn.classList.contains('on')&&typeof pnLoad==='function')pnLoad()}},1000);
document.querySelectorAll('.ov').forEach(o=>{{o.addEventListener('click',e=>{{if(e.target===o)o.classList.remove('sh')}});}});

// ═══ AGI FILE EXPLORER ═══
let feCur='';
function feFmt(b){{if(!b||b===0)return'';if(b<1024)return b+' B';if(b<1048576)return(b/1024).toFixed(1)+' KB';if(b<1073741824)return(b/1048576).toFixed(1)+' MB';return(b/1073741824).toFixed(1)+' GB'}}
async function feInit(){{try{{const r=await fetch('/admin/api/agi/files/roots');if(!r.ok)return;const d=await r.json();const c=document.getElementById('fe-roots');c.innerHTML='';for(const rt of(d.roots||[])){{const btn=document.createElement('button');btn.className=rt.exists?'bt bt-p bt-sm':'bt bt-s bt-sm';btn.textContent='\U0001F4C1 '+rt.path;if(rt.exists)btn.addEventListener('click',function(){{feNav(rt.path)}});else btn.disabled=true;c.appendChild(btn)}}}}catch(e){{console.error(e)}}}}
async function feNav(p){{feCur=p;document.getElementById('fe-view').style.display='none';try{{const r=await fetch('/admin/api/agi/files/list?path='+encodeURIComponent(p));if(!r.ok){{const d=await r.json();alert(d.error||'Erro');return}};const d=await r.json();document.getElementById('fe-list').style.display='block';document.getElementById('fe-cnt').textContent=d.count+' itens';feBC(d.path);const c=document.getElementById('fe-ent');c.innerHTML='';if(!d.entries||!d.entries.length){{c.innerHTML='<div style="padding:20px;text-align:center;color:#aaa">Pasta vazia</div>';return}};for(const e of d.entries){{const row=document.createElement('div');row.className=e.is_dir?'fe-row dir':'fe-row';const sz=e.is_dir?(e.children>=0?e.children+' itens':''):feFmt(e.size);row.innerHTML='<span class="fe-icon">'+esc(e.icon)+'</span><span class="fe-name">'+esc(e.name)+'</span><span class="fe-size">'+esc(sz)+'</span><span class="fe-date">'+esc(e.modified||'')+'</span>';const fullPath=d.path+'\\\\'+e.name;if(e.is_dir){{row.addEventListener('click',function(){{feNav(fullPath)}})}}else if(e.is_text){{row.addEventListener('click',function(){{feRead(fullPath)}})}}else{{row.addEventListener('click',function(){{alert('Arquivo bin\u00e1rio: '+e.name)}})}}c.appendChild(row)}}}}catch(e){{console.error(e)}}}}
function feBC(p){{const bc=document.getElementById('fe-bc');bc.innerHTML='';const parts=p.split('\\\\');let acc='';for(let i=0;i<parts.length;i++){{if(i>0){{acc+='\\\\';const sep=document.createElement('span');sep.className='fe-bc-sep';sep.textContent='\u203A';bc.appendChild(sep)}};acc+=parts[i];const seg=document.createElement('span');seg.className='fe-bc-seg';seg.textContent=i===0?parts[i]+'\\\\':parts[i];const navTo=acc;seg.addEventListener('click',function(){{feNav(navTo)}});bc.appendChild(seg)}}}}
function feUp(){{if(!feCur)return;const parts=feCur.split('\\\\');if(parts.length<=1)return;parts.pop();feNav(parts.join('\\\\'))}}
async function feRead(p){{try{{const r=await fetch('/admin/api/agi/files/read?path='+encodeURIComponent(p));if(!r.ok){{const d=await r.json();alert(d.error||'Erro');return}};const d=await r.json();document.getElementById('fe-view').style.display='block';document.getElementById('fv-nm').textContent=d.name;document.getElementById('fv-mt').textContent=d.lines+' linhas \u00b7 '+feFmt(d.size)+' \u00b7 '+d.encoding;document.getElementById('fv-ct').textContent=d.content;document.getElementById('fe-view').scrollIntoView({{behavior:'smooth'}})}}catch(e){{console.error(e)}}}}
function fvCp(){{const t=document.getElementById('fv-ct').textContent;navigator.clipboard.writeText(t).then(function(){{alert('Copiado!')}}).catch(function(){{alert('Erro ao copiar')}})}}
function fvCl(){{document.getElementById('fe-view').style.display='none'}}

// ═══ TGL COIN BANK DASHBOARD ═══
async function bcLoad(){{
try{{
const[sr,ar,tr]=await Promise.all([fetch('/admin/api/bank/stats'),fetch('/admin/api/bank/accounts'),fetch('/admin/api/bank/transactions?n=50')]);
if(!sr.ok||!ar.ok||!tr.ok)return;
const st=await sr.json(),ac=await ar.json(),tx=await tr.json();
document.getElementById('bc-accounts').textContent=st.total_accounts;
document.getElementById('bc-supply').textContent=st.total_supply.toLocaleString('pt-BR',{{minimumFractionDigits:2}})+' TGLC';
document.getElementById('bc-txcount').textContent=st.total_transactions;
document.getElementById('bc-hash').textContent=st.tgl_hash_available?'TGL-Hash-256':'SHA-256+\u03b2';
// Accounts table
const atb=document.getElementById('bc-acctb');atb.innerHTML='';
for(const a of(ac.accounts||[])){{const row=document.createElement('tr');
row.innerHTML='<td><span class="lu">'+esc(a.username)+'</span></td>'
+'<td class="mono" style="font-weight:600;color:var(--dourado)">'+esc(a.balance.toLocaleString('pt-BR',{{minimumFractionDigits:2}}))+' TGLC</td>'
+'<td class="mono" style="color:var(--vermelho)">-'+esc(a.total_sent.toLocaleString('pt-BR',{{minimumFractionDigits:2}}))+'</td>'
+'<td class="mono" style="color:var(--verde)">+'+esc(a.total_received.toLocaleString('pt-BR',{{minimumFractionDigits:2}}))+'</td>'
+'<td>'+esc(a.tx_count)+'</td>'
+'<td class="mono" style="font-size:11px;color:#888">'+esc(String(a.created||'').substring(0,16))+'</td>';
atb.appendChild(row)}}
// Transactions table
const ttb=document.getElementById('bc-txtb');ttb.innerHTML='';
for(const t of(tx.transactions||[])){{const row=document.createElement('tr');
const typ=t.type==='airdrop'?'<span class="bg bg-ok">airdrop</span>':t.type==='admin_airdrop'?'<span class="bg bg-te">admin</span>':'<span class="bg bg-a">transfer</span>';
const hash=(t.hash||'').substring(0,12)+'...';
row.innerHTML='<td class="mono" style="font-size:11px">'+esc(String(t.timestamp||'').substring(0,19))+'</td>'
+'<td>'+typ+'</td>'
+'<td class="lu">'+esc(t.from)+'</td>'
+'<td class="lu">'+esc(t.to)+'</td>'
+'<td class="mono" style="font-weight:600">'+esc(t.amount.toLocaleString('pt-BR',{{minimumFractionDigits:2}}))+' TGLC</td>'
+'<td class="mono" style="font-size:11px;color:#888" title="'+esc(t.hash)+'">'+esc(hash)+'</td>';
ttb.appendChild(row)}}
}}catch(e){{console.error('Bank load error:',e)}}}}
async function bcAirdrop(){{
const username=document.getElementById('ad-user').value.trim();
const amount=parseFloat(document.getElementById('ad-amount').value);
if(!username||!amount||amount<=0){{alert('Preencha usu\u00e1rio e valor.');return}}
try{{const r=await fetch('/admin/api/bank/airdrop',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{username:username,amount:amount}})}});
const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};
alert('Airdrop enviado! '+username+' agora tem '+d.balance+' TGLC');cD('d-airdrop');bcLoad()}}catch(e){{alert('Erro: '+e)}}}}
async function bcTransfer(){{
const from_u=document.getElementById('tx-from').value.trim();
const to_u=document.getElementById('tx-to').value.trim();
const amount=parseFloat(document.getElementById('tx-amount').value);
const note=document.getElementById('tx-note').value.trim();
if(!from_u||!to_u||!amount||amount<=0){{alert('Preencha todos os campos.');return}}
if(!confirm('Confirma transfer\u00eancia de '+amount+' TGLC de '+from_u+' para '+to_u+'?'))return;
try{{const r=await fetch('/admin/api/bank/transfer',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{from:from_u,to:to_u,amount:amount,note:note}})}});
const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};
alert('Transfer\u00eancia confirmada!\\nHash: '+d.receipt.hash.substring(0,24)+'...');cD('d-adtx');bcLoad()}}catch(e){{alert('Erro: '+e)}}}}
// Auto-load bank when tab selected
const _origTabClick=document.querySelector('.tabs').onclick;
document.querySelector('.tabs').addEventListener('click',function(e){{if(e.target.dataset.t==='bc')bcLoad();if(e.target.dataset.t==='pn')pnLoad();if(e.target.dataset.t==='ac')acLoad();if(e.target.dataset.t==='ct')ctLoad();if(e.target.dataset.t==='mm')mmLoad()}});
// ═══ MEMORIA DA IALD (02/08/2026) ═══
// O medidor de custo no topo existe porque cada fato "sempre" e pago em TODA
// conversa: ver 340/3000 tokens evita inflar o prompt sem perceber.
let _mmFatos=[];
function kkLoad(){{fetch('/admin/api/kernel').then(r=>r.json()).then(d=>{{if(d.error){{document.getElementById('kk-status').textContent=d.error;return}}document.getElementById('kk-txt').value=d.conteudo;document.getElementById('kk-info').textContent=d.arquivo+' \u2014 '+d.chars+' chars, '+d.linhas+' linhas, ~'+d.tokens_est+' tokens \u2014 alterado em '+d.mtime;var s=document.getElementById('kk-bak');s.innerHTML='';d.backups.forEach(function(b){{var o=document.createElement('option');o.value=b;o.textContent=b;s.appendChild(o)}});document.getElementById('kk-status').textContent='carregado do disco'}}).catch(e=>{{document.getElementById('kk-status').textContent='ERRO: '+e}})}}
function kkSalvar(){{var t=document.getElementById('kk-txt').value;if(!t.trim()){{alert('Kernel vazio - recusado');return}}if(!confirm('Commitar o kernel? Um backup da versao atual e gravado antes, e o novo texto entra no servidor na hora.'))return;document.getElementById('kk-status').textContent='commitando...';fetch('/admin/api/kernel',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{conteudo:t}})}}).then(r=>r.json()).then(d=>{{if(d.error){{document.getElementById('kk-status').textContent='ERRO: '+d.error;return}}document.getElementById('kk-status').textContent='COMMITADO \u2014 backup '+d.backup+' \u2014 ja no ar ('+d.chars+' chars, ~'+d.tokens_est+' tokens)';kkLoad()}}).catch(e=>{{document.getElementById('kk-status').textContent='ERRO: '+e}})}}
function kkRestaurar(){{var b=document.getElementById('kk-bak').value;if(!b)return;if(!confirm('Restaurar '+b+'? O kernel atual sera salvo como backup antes.'))return;fetch('/admin/api/kernel/restaurar',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{backup:b}})}}).then(r=>r.json()).then(d=>{{document.getElementById('kk-status').textContent=d.error?('ERRO: '+d.error):('restaurado de '+b);kkLoad()}})}}
function mmEsc(t){{return (t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}}
function mmLoad(){{
  fetch('/admin/api/memoria').then(r=>r.json()).then(d=>{{
    if(d.error){{document.getElementById('mm-tb').innerHTML='<tr><td colspan=6>'+mmEsc(d.error)+'</td></tr>';return}}
    _mmFatos=d.fatos||[];const c=d.custo||{{}};
    document.getElementById('mm-tok').textContent=(c.tokens_bloco_sempre||0);
    document.getElementById('mm-nsempre').textContent=(c.fatos_sempre||0);
    document.getElementById('mm-ndem').textContent=(c.fatos_sob_demanda||0);
    const teto=c.teto_recomendado||3000, us=c.tokens_bloco_sempre||0;
    const pct=Math.min(100,Math.round(100*us/teto));
    const b=document.getElementById('mm-barra');
    b.style.width=pct+'%';
    b.style.background=c.acima_do_teto?'var(--vermelho)':(pct>70?'var(--amarelo)':'var(--dourado)');
    document.getElementById('mm-barra-txt').textContent=us+' de '+teto+' tokens recomendados ('+pct+'%)'+(c.acima_do_teto?' \u2014 acima do teto: mova fatos para sob demanda':'');
    document.getElementById('mm-tok-sub').textContent='custa '+us+' tokens em TODA conversa';
    let h='';
    for(const f of _mmFatos){{
      const on=f.ativo!==false;
      h+='<tr style="opacity:'+(on?1:.45)+'">'
        +'<td>'+(f.escopo==='sempre'?'<b style="color:var(--dourado)">SEMPRE</b>':'sob demanda')+'</td>'
        +'<td>'+mmEsc(f.titulo)+'</td>'
        +'<td style="max-width:340px">'+mmEsc((f.texto||'').slice(0,160))+((f.texto||'').length>160?'\u2026':'')+'</td>'
        +'<td class="cs">'+mmEsc((f.tags||[]).join(', '))+'</td>'
        +'<td>'+esc(f.peso||3)+'</td>'
        +'<td style="white-space:nowrap">'
        +'<button class="bt bt-s bt-sm" onclick="mmEditar('+jsq(f.id)+')">editar</button> '
        +'<button class="bt bt-s bt-sm" onclick="mmToggle('+jsq(f.id)+','+(on?'false':'true')+')">'+(on?'desativar':'ativar')+'</button> '
        +'<button class="bt bt-s bt-sm" style="color:var(--vermelho)" onclick="mmRemover('+jsq(f.id)+')">remover</button>'
        +'</td></tr>';
    }}
    document.getElementById('mm-tb').innerHTML=h||'<tr><td colspan=6 class="cs">A memoria esta vazia. Clique em + Fato, ou peca no chat: "lembre-se que ..."</td></tr>';
  }}).catch(e=>{{document.getElementById('mm-tb').innerHTML='<tr><td colspan=6>'+esc(e)+'</td></tr>'}});
  fetch('/api/contexto').then(r=>r.json()).then(d=>{{
    if(d&&d.n_ctx)document.getElementById('mm-janela').textContent=Math.round(d.n_ctx/1024)+'k tokens';
  }}).catch(()=>{{}});
}}
function mmNovo(){{
  document.getElementById('mm-dlg-t').textContent='Novo fato';
  document.getElementById('mm-id').value='';
  document.getElementById('mm-titulo').value='';
  document.getElementById('mm-texto').value='';
  document.getElementById('mm-escopo').value='sob_demanda';
  document.getElementById('mm-tags').value='';
  document.getElementById('mm-peso').value=3;
  document.getElementById('d-mmfato').classList.add('sh');
}}
function mmEditar(id){{
  const f=_mmFatos.find(x=>x.id===id);if(!f)return;
  document.getElementById('mm-dlg-t').textContent='Editar: '+f.id;
  document.getElementById('mm-id').value=f.id;
  document.getElementById('mm-titulo').value=f.titulo||'';
  document.getElementById('mm-texto').value=f.texto||'';
  document.getElementById('mm-escopo').value=f.escopo||'sob_demanda';
  document.getElementById('mm-tags').value=(f.tags||[]).join(', ');
  document.getElementById('mm-peso').value=f.peso||3;
  document.getElementById('d-mmfato').classList.add('sh');
}}
function mmSalvar(){{
  const id=document.getElementById('mm-id').value;
  const corpo={{titulo:document.getElementById('mm-titulo').value.trim(),
    texto:document.getElementById('mm-texto').value.trim(),
    escopo:document.getElementById('mm-escopo').value,
    tags:document.getElementById('mm-tags').value.split(',').map(t=>t.trim()).filter(t=>t),
    peso:parseInt(document.getElementById('mm-peso').value)||3}};
  if(!corpo.titulo||!corpo.texto){{alert('Titulo e fato sao obrigatorios.');return}}
  const url=id?('/admin/api/memoria/'+encodeURIComponent(id)):'/admin/api/memoria';
  fetch(url,{{method:id?'PUT':'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(corpo)}})
    .then(r=>r.json()).then(d=>{{
      if(d.error){{alert(d.error);return}}
      cD('d-mmfato');mmLoad();
    }}).catch(e=>alert(e));
}}
function mmToggle(id,ativo){{
  fetch('/admin/api/memoria/'+encodeURIComponent(id),{{method:'PUT',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{ativo:ativo}})}})
    .then(()=>mmLoad());
}}
function mmRemover(id){{
  if(!confirm('Remover o fato "'+id+'" em definitivo?'))return;
  fetch('/admin/api/memoria/'+encodeURIComponent(id),{{method:'DELETE'}}).then(()=>mmLoad());
}}
function mmBuscar(){{
  const q=document.getElementById('mm-q').value.trim();
  if(!q){{document.getElementById('mm-res').textContent='digite uma pergunta';return}}
  fetch('/admin/api/memoria/bloco?q='+encodeURIComponent(q)).then(r=>r.json()).then(d=>{{
    const t=(d.bloco_sob_demanda||'').trim();
    document.getElementById('mm-res').innerHTML=t
      ? '<b>seria recuperado:</b><br><pre style="white-space:pre-wrap;font-size:12px">'+mmEsc(t)+'</pre>'
      : 'nada seria recuperado para esta pergunta';
  }}).catch(e=>{{document.getElementById('mm-res').textContent=e}});
}}
function mmPrevia(){{
  const q=document.getElementById('mm-q').value.trim();
  fetch('/admin/api/memoria/bloco'+(q?('?q='+encodeURIComponent(q)):'')).then(r=>r.json()).then(d=>{{
    let t='=== BLOCO FIXO (entra no system de TODA conversa) ===\\n';
    t+=(d.bloco_sempre||'(vazio)')+'\\n\\n';
    if(q){{t+='=== RECUPERADO PARA "'+q+'" (vai na mensagem do usuario) ===\\n'+(d.bloco_sob_demanda||'(nada)')+'\\n\\n'}}
    if(d.orcamento_contexto){{t+='=== ORCAMENTO DE CONTEXTO ===\\n'+JSON.stringify(d.orcamento_contexto,null,2)}}
    document.getElementById('mm-previa').textContent=t;
    document.getElementById('d-mmprevia').classList.add('sh');
  }}).catch(e=>alert(e));
}}

// ═══ PSI-NET DASHBOARD ═══
async function pnLoad(){{
try{{
const[sr,tr]=await Promise.all([fetch('/admin/api/psinet/stats'),fetch('/admin/api/psinet/pending')]);
if(!sr.ok||!tr.ok)return;
const st=await sr.json(),tx=await tr.json();
document.getElementById('pn-pending').textContent=st.pending;
document.getElementById('pn-delivered').textContent=st.delivered;
document.getElementById('pn-maxfile').textContent=st.max_file_size_mb+' MB';
document.getElementById('pn-timeout').textContent=st.transfer_timeout_hours+'h';
document.getElementById('pn-cfg-maxmb').value=st.max_file_size_mb;
document.getElementById('pn-cfg-timeout').value=st.transfer_timeout_hours;
document.getElementById('pn-cfg-cost').value=st.transfer_cost_tglc;
const ttb=document.getElementById('pn-txtb');ttb.innerHTML='';
for(const t of(tx.transfers||[])){{const row=document.createElement('tr');
const st2=t.status==='pending'?'<span class="bg bg-st">pendente</span>':t.status==='delivered'?'<span class="bg bg-ok">entregue</span>':'<span class="bg bg-er">'+esc(t.status)+'</span>';
const sz=(t.original_size/1024).toFixed(1)+' KB';
const hash=String(t.send_hash||'').substring(0,12)+'...';
row.innerHTML='<td class="mono" style="font-size:11px">'+esc(String(t.timestamp||'').substring(0,19))+'</td>'
+'<td class="lu">'+esc(t.from)+'</td>'
+'<td class="lu">'+esc(t.to)+'</td>'
+'<td>'+esc(t.filename)+'</td>'
+'<td class="mono">'+esc(sz)+'</td>'
+'<td>'+st2+'</td>'
+'<td class="mono" style="font-size:11px;color:#888" title="'+esc(t.send_hash||'')+'">'+esc(hash)+'</td>';
ttb.appendChild(row)}}
}}catch(e){{console.error('PSI-NET load error:',e)}}}}
async function pnSaveConfig(){{
const mb=parseFloat(document.getElementById('pn-cfg-maxmb').value);
const hours=parseFloat(document.getElementById('pn-cfg-timeout').value);
const cost=parseFloat(document.getElementById('pn-cfg-cost').value);
try{{const r=await fetch('/admin/api/psinet/config',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{max_file_size_mb:mb,transfer_timeout_hours:hours,transfer_cost_tglc:cost}})}});
const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};
alert('Configura\u00e7\u00e3o salva! Max: '+d.config.max_file_size_mb+' MB');pnLoad()}}catch(e){{alert('Erro: '+e)}}}}
async function pnSend(){{
const from_u=document.getElementById('pn-from').value.trim();
const to_u=document.getElementById('pn-to').value.trim();
const fileInput=document.getElementById('pn-file');
const note=document.getElementById('pn-note').value.trim();
const status=document.getElementById('pn-send-status');
if(!from_u||!to_u){{alert('Preencha remetente e destinat\u00e1rio.');return}}
if(!fileInput.files||!fileInput.files[0]){{alert('Selecione um arquivo.');return}}
const file=fileInput.files[0];
status.textContent='Radicalizando '+file.name+' ('+((file.size/1024).toFixed(1))+' KB)...';
document.getElementById('pn-send-btn').disabled=true;
const fd=new FormData();fd.append('file',file);fd.append('from_user',from_u);fd.append('to_user',to_u);fd.append('note',note);
try{{const r=await fetch('/admin/api/psinet/send',{{method:'POST',body:fd}});
const d=await r.json();if(!r.ok){{status.textContent='Erro: '+(d.error||'?');status.style.color='var(--vermelho)';return}};
status.textContent='Enviado! TX: '+d.result.tx_id+' | Hash: '+d.result.send_hash.substring(0,16)+'...';
status.style.color='var(--verde)';pnLoad();setTimeout(function(){{cD('d-pnsend');status.textContent=''}},3000)}}catch(e){{status.textContent='Erro: '+e;status.style.color='var(--vermelho)'}}finally{{document.getElementById('pn-send-btn').disabled=false}}}}
async function pnCleanup(){{
if(!confirm('Remover transfer\u00eancias expiradas?'))return;
try{{const r=await fetch('/admin/api/psinet/cleanup',{{method:'POST'}});
const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};
alert(d.removed+' transfer\u00eancia(s) removida(s).');pnLoad()}}catch(e){{alert('Erro: '+e)}}}}

feInit();

// ═══ AGI PHASE 2: Edit, Create, Delete ═══
let fvCurPath='';
const _feReadOrig=feRead;
feRead=async function(p){{fvCurPath=p;await _feReadOrig(p)}};
function fvEdit(){{const ct=document.getElementById('fv-ct');const ta=document.getElementById('fv-ed-ta');const ed=document.getElementById('fv-editor');ta.value=ct.textContent;ct.style.display='none';ed.style.display='block';document.getElementById('fv-edit-btn').style.display='none';document.getElementById('fv-save-msg').textContent=''}}
function fvCancelEdit(){{document.getElementById('fv-ct').style.display='block';document.getElementById('fv-editor').style.display='none';document.getElementById('fv-edit-btn').style.display=''}}
async function fvSave(){{if(!fvCurPath)return;const content=document.getElementById('fv-ed-ta').value;const msg=document.getElementById('fv-save-msg');msg.textContent='Salvando...';msg.style.color='var(--dourado)';try{{const r=await fetch('/admin/api/agi/files/write',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{path:fvCurPath,content:content}})}});const d=await r.json();if(!r.ok){{msg.textContent=d.error||'Erro';msg.style.color='var(--vermelho)';return}};msg.textContent='Salvo! '+(d.backup?'Backup: '+d.backup.split('\\\\').pop():'');msg.style.color='var(--verde)';document.getElementById('fv-ct').textContent=content;document.getElementById('fv-mt').textContent=d.lines+' linhas \u00b7 '+feFmt(d.size)+' \u00b7 utf-8';fvCancelEdit()}}catch(e){{msg.textContent='Erro: '+e;msg.style.color='var(--vermelho)'}}}}
function feNewFile(){{if(!feCur){{alert('Navegue para uma pasta primeiro.');return}};document.getElementById('d-nf').classList.add('sh');document.getElementById('nf-name').value=''}}
async function feDoNewFile(){{const name=document.getElementById('nf-name').value.trim();if(!name){{alert('Digite o nome do arquivo.');return}};if(name.includes('\\\\')||name.includes('/')){{alert('Nome nao pode conter \\\\ ou /');return}};const path=feCur+'\\\\'+name;try{{const r=await fetch('/admin/api/agi/files/write',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{path:path,content:''}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};cD('d-nf');feNav(feCur)}}catch(e){{alert('Erro: '+e)}}}}
function feNewDir(){{if(!feCur){{alert('Navegue para uma pasta primeiro.');return}};document.getElementById('d-nd').classList.add('sh');document.getElementById('nd-name').value=''}}
async function feDoNewDir(){{const name=document.getElementById('nd-name').value.trim();if(!name){{alert('Digite o nome da pasta.');return}};if(name.includes('\\\\')||name.includes('/')){{alert('Nome nao pode conter \\\\ ou /');return}};const path=feCur+'\\\\'+name;try{{const r=await fetch('/admin/api/agi/files/mkdir',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{path:path}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};cD('d-nd');feNav(feCur)}}catch(e){{alert('Erro: '+e)}}}}
async function feDel(){{if(!fvCurPath)return;try{{const r=await fetch('/admin/api/agi/files/delete/request',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{path:fvCurPath}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};document.getElementById('del-name').textContent=d.name;document.getElementById('del-token').value=d.confirm_token;document.getElementById('del-path').value=d.path;document.getElementById('d-del').classList.add('sh')}}catch(e){{alert('Erro: '+e)}}}}
async function feDoDelete(){{const path=document.getElementById('del-path').value;const token=document.getElementById('del-token').value;try{{const r=await fetch('/admin/api/agi/files/delete/confirm',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{path:path,confirm_token:token}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};cD('d-del');fvCl();feNav(feCur)}}catch(e){{alert('Erro: '+e)}}}}

// ═══ AGI COMMAND CENTER ═══
let agiHist=[];
let agiWaiting=false;
function agiAddMsg(role,text){{const msgs=document.getElementById('agi-msgs');const div=document.createElement('div');div.className='agi-msg '+(role==='user'?'user':'ai');const av=document.createElement('div');av.className='agi-av';av.textContent=role==='user'?'\U0001F464':'\u03b2';const txt=document.createElement('div');txt.className='agi-txt';txt.textContent=text;div.appendChild(av);div.appendChild(txt);msgs.appendChild(div);msgs.scrollTop=msgs.scrollHeight;return div}}
async function agiSend(){{const ta=document.getElementById('agi-input');const text=ta.value.trim();if(!text||agiWaiting)return;ta.value='';agiAddMsg('user',text);agiHist.push({{role:'user',content:text}});agiWaiting=true;document.getElementById('agi-st').style.display='block';document.getElementById('agi-st').textContent='Analisando...';document.getElementById('agi-send-btn').disabled=true;document.getElementById('agi-act').style.display='none';try{{const r=await fetch('/admin/api/agi/command',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{messages:agiHist}})}});const d=await r.json();if(!r.ok){{agiAddMsg('ai','Erro: '+(d.error||'Falha na comunicacao'));return}};const resp=d.response||'(vazio)';agiAddMsg('ai',resp);agiHist.push({{role:'assistant',content:resp}});const lower=resp.toLowerCase();if(lower.includes('autoriza')||lower.includes('confirma')||lower.includes('deseja prosseguir')||lower.includes('posso executar')){{document.getElementById('agi-act').style.display='flex'}}}}catch(e){{agiAddMsg('ai','Erro de conexao: '+e)}}finally{{agiWaiting=false;document.getElementById('agi-st').style.display='none';document.getElementById('agi-send-btn').disabled=false}}}}
async function agiExec(){{document.getElementById('agi-act').style.display='none';agiAddMsg('user','Autorizado. Executar.');agiHist.push({{role:'user',content:'Autorizado. Executar.'}});document.getElementById('agi-st').style.display='block';document.getElementById('agi-st').textContent='Executando plano...';try{{const r=await fetch('/admin/api/agi/execute',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{messages:agiHist}})}});const d=await r.json();if(!r.ok){{agiAddMsg('ai','Erro na execucao: '+(d.error||'Falha')+(d.raw?'\\n\\nResposta bruta do modelo:\\n'+d.raw:''));return}};let report='EXECU\\u00c7\\u00c3O CONCLU\\u00cdDA\\n\\n';report+=d.success+'/'+d.total+' a\\u00e7\\u00f5es realizadas com sucesso.\\n\\n';for(const res of(d.results||[])){{if(res.ok){{report+='\\u2705 '+res.action+': '+res.path+(res.backup?' (backup criado)':'')+' \\n'}}else{{report+='\\u274C '+res.action+': '+res.path+' \\u2014 '+(res.error||'erro')+' \\n'}}}};agiAddMsg('ai',report);agiHist.push({{role:'assistant',content:report}});if(d.analysis){{document.getElementById('agi-st').textContent='Analisando conte\u00fado lido...';agiAddMsg('ai',d.analysis);agiHist.push({{role:'assistant',content:d.analysis}})}}}}catch(e){{agiAddMsg('ai','Erro: '+e)}}finally{{document.getElementById('agi-st').style.display='none'}}}}
function agiReject(){{document.getElementById('agi-act').style.display='none';agiAddMsg('user','Cancelado.');agiHist.push({{role:'user',content:'Cancelado. Nao executar.'}});agiAddMsg('ai','Entendido. Plano cancelado. O que mais posso ajudar?');agiHist.push({{role:'assistant',content:'Entendido. Plano cancelado.'}})}}
document.getElementById('agi-input').addEventListener('keydown',function(e){{if(e.key==='Enter'&&!e.shiftKey){{e.preventDefault();agiSend()}}}});

// === LIBERACAO DE ACESSO (14/09/2026): Apple, Google, usuario e senha ===
function esc(s){{return String(s==null?'':s).replace(/[&<>"']/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]}})}}
function jsq(s){{return esc(JSON.stringify(String(s==null?'':s)))}}
let acUsers=[];let acPedidos={{}};
async function acLoad(){{
const tb=document.getElementById('ac-tb');
try{{
const rp=await fetch('/admin/api/pedidos');
if(!rp.ok){{tb.innerHTML='<tr><td colspan="6" style="color:var(--vermelho);padding:14px">Erro ao carregar os pedidos (HTTP '+rp.status+')</td></tr>';return}}
const d=await rp.json();
try{{const ru=await fetch('/admin/api/users');acUsers=ru.ok?((await ru.json()).users||[]).map(function(x){{return x.username}}):[]}}catch(e){{acUsers=[]}}
const cfg=d.configurado||{{}};
const ok=function(v){{return v?'<span style="color:var(--verde)">\u2714 configurada</span>':'<span style="color:var(--vermelho)">\u2716 falta configurar</span>'}};
document.getElementById('ac-cfg').innerHTML='Apple no iPhone/iPad: '+ok(cfg.apple_nativo)+' \u00b7 Apple na web e no Android: '+ok(cfg.apple_web)+' \u00b7 Google: '+ok(cfg.google)+' \u00b7 Usu\u00e1rio e senha: '+ok(true);
const pend=(d.contagem||{{}}).pendente||0;
const tab=document.querySelector('.tab[data-t="ac"]');if(tab)tab.textContent='\U0001F511 Acesso'+(pend?' ('+pend+')':'');
const ps=d.pedidos||[];acPedidos={{}};for(const p of ps)acPedidos[p.id]=p;
if(!ps.length){{tb.innerHTML='<tr><td colspan="6" style="text-align:center;color:#888;padding:20px">Nenhum pedido de acesso</td></tr>';return}}
let h='';
for(const p of ps){{
const dt=p.ultima_tentativa?new Date(p.ultima_tentativa).toLocaleString('pt-BR',{{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}}):'\u2014';
let st='Pendente',bg='bg-st';
if(p.status==='aprovado'){{st='Liberado';bg='bg-ok'}}else if(p.status==='recusado'){{st='Recusado';bg='bg-er'}}else if(p.status==='encerrado'){{st='Encerrado';bg='bg-u'}}
let ac='';
if(p.status==='pendente'){{ac='<button class="bt bt-p bt-sm" data-ac="aprovar" data-id="'+esc(p.id)+'">\u2705 Liberar</button> <button class="bt bt-d bt-sm" data-ac="recusar" data-id="'+esc(p.id)+'">Recusar</button>'}}
else if(p.status==='recusado'){{ac='<button class="bt bt-p bt-sm" data-ac="aprovar" data-id="'+esc(p.id)+'">Liberar</button> <button class="bt bt-s bt-sm" data-ac="reabrir" data-id="'+esc(p.id)+'">Reabrir</button>'}}
else if(p.status==='aprovado'){{ac='<span class="mono">'+esc(p.usuario||'\u2014')+'</span>'}}
ac+=' <button class="bt bt-d bt-sm" style="opacity:.6" data-ac="apagar" data-id="'+esc(p.id)+'" title="Apagar o registro">\U0001F5D1</button>';
h+='<tr><td>'+esc(dt)+'</td><td>'+(p.provedor==='apple'?'Apple':'Google')+'</td><td><b>'+esc(p.nome||'(sem nome)')+'</b><br><span class="mono" style="font-size:11px">'+esc(p.email||'(sem e-mail)')+'</span></td><td>'+esc(p.tentativas||1)+(p.superficie?' \u00b7 '+esc(p.superficie):'')+'</td><td><span class="bg '+bg+'">'+st+'</span></td><td>'+ac+'</td></tr>';
}}
tb.innerHTML=h;
}}catch(e){{console.error('acLoad',e);tb.innerHTML='<tr><td colspan="6" style="color:var(--vermelho);padding:14px">Erro: '+esc(e)+'</td></tr>'}}
}}
function acAbrirAprovar(id){{
const p=acPedidos[id];if(!p)return;
document.getElementById('ap-id').value=id;
document.getElementById('ap-quem').textContent=(p.provedor==='apple'?'Apple':'Google')+' \u00b7 '+(p.nome||'sem nome')+' \u00b7 '+(p.email||'sem e-mail');
document.getElementById('ap-nome').value=p.sugestao||'';
const s=document.getElementById('ap-exist');s.innerHTML='';
for(const u of acUsers){{const o=document.createElement('option');o.value=u;o.textContent=u;s.appendChild(o)}}
document.querySelector('input[name="ap-modo"][value="novo"]').checked=true;
document.getElementById('ap-nativa').checked=false;
document.getElementById('d-ap').classList.add('sh');
}}
async function acAprovar(){{
const id=document.getElementById('ap-id').value;
const modo=document.querySelector('input[name="ap-modo"]:checked').value;
const username=modo==='novo'?document.getElementById('ap-nome').value.trim().toLowerCase():document.getElementById('ap-exist').value;
if(!username){{alert('Informe o usu\u00e1rio');return}}
try{{
const r=await fetch('/admin/api/pedidos/'+encodeURIComponent(id)+'/aprovar',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{modo:modo,username:username,acesso_nativa:document.getElementById('ap-nativa').checked}})}});
const d=await r.json();
if(!r.ok){{alert(d.error||'Erro ao liberar');return}}
cD('d-ap');alert((d.modo==='vincular'?'Entrada vinculada ao usu\u00e1rio ':'Acesso liberado para o usu\u00e1rio ')+d.username+(document.getElementById('ap-nativa').checked?' \u00b7 IALD Nativa + ChatGPT':' \u00b7 s\u00f3 ChatGPT'));
acLoad();rU();rS();
}}catch(e){{alert('Erro: '+e)}}
}}
async function acAcao(id,acao){{
if(acao==='recusar'&&!confirm('Recusar este pedido? A pessoa continua recusada at\u00e9 voc\u00ea reabrir.'))return;
if(acao==='apagar'){{if(!confirm('Apagar o registro deste pedido? Se a pessoa tentar de novo, abre um pedido novo.'))return;
try{{const r=await fetch('/admin/api/pedidos/'+encodeURIComponent(id),{{method:'DELETE'}});if(r.ok)acLoad();else alert('Erro ao apagar')}}catch(e){{alert('Erro: '+e)}}return}}
try{{const r=await fetch('/admin/api/pedidos/'+encodeURIComponent(id)+'/'+acao,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:'{{}}'}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};acLoad()}}catch(e){{alert('Erro: '+e)}}
}}
document.getElementById('ac-tb').addEventListener('click',function(ev){{const b=ev.target.closest('button[data-ac]');if(!b)return;if(b.dataset.ac==='aprovar')acAbrirAprovar(b.dataset.id);else acAcao(b.dataset.id,b.dataset.ac)}});
document.getElementById('utb').addEventListener('click',async function(ev){{
const s=ev.target.closest('[data-sacro]');if(s){{toggleSacred(s.dataset.sacro);return}}
const ac=ev.target.closest('button[data-acesso]');if(ac){{uAcesso(ac.dataset.acesso,ac.dataset.v==='1');return}}
const b=ev.target.closest('button[data-uac]');if(b){{if(b.dataset.uac==='senha')sPW(b.dataset.u);else if(b.dataset.uac==='bloquear'||b.dataset.uac==='desbloquear')uBloq(b.dataset.u,b.dataset.uac==='bloquear');else sDU(b.dataset.u);return}}
const a=ev.target.closest('a[data-idac]');if(!a)return;ev.preventDefault();
const u=a.dataset.u,p=a.dataset.p,sub=a.dataset.s;const nomeP=p==='apple'?'Apple':'Google';
try{{
if(a.dataset.idac==='remover'){{
if(!confirm('Remover a entrada '+nomeP+' de '+u+'? A pessoa perde o acesso por ela e, se tentar de novo, abre um pedido novo.'))return;
const r=await fetch('/admin/api/users/'+encodeURIComponent(u)+'/identidades/remover',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{provedor:p,sub:sub}})}});
const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}}
}}else{{
const dest=prompt('Mover a entrada '+nomeP+' de '+u+' para qual usu\u00e1rio?\\nUse quando a mesma pessoa ficou com duas contas.','');if(!dest)return;
const r=await fetch('/admin/api/users/'+encodeURIComponent(u)+'/identidades/mover',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{provedor:p,sub:sub,destino:dest.trim().toLowerCase()}})}});
const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}}
}}
rU();acLoad();
}}catch(e){{alert('Erro: '+e)}}
}});
acLoad();
document.getElementById('utb').addEventListener('change',async function(ev){{const s=ev.target.closest('select[data-motor]');if(!s)return;try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(s.dataset.motor)+'/motor',{{method:'PUT',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{motor:s.value}})}});const d=await r.json();if(!r.ok)alert(d.error||'Erro');rU()}}catch(e){{alert('Erro: '+e)}}}});
async function deadlinesLoad(){{
const box=document.getElementById('operator-deadlines-items');
try{{const r=await fetch('/admin/api/prazos',{{cache:'no-store'}});if(!r.ok)throw Error();const d=await r.json();
if(!d.prazos)throw Error();box.replaceChildren();
for(const p of d.prazos.items||[]){{const row=document.createElement('div');
row.textContent=p.label+': '+p.message+(p.expires_at?' · '+new Date(p.expires_at).toLocaleString('pt-BR',{{timeZone:'America/Sao_Paulo'}})+' (Brasília)':'');
if(['critical','expired'].includes(p.level))row.style.color='#b42318';box.append(row);}}
if(d.prazos.error){{const e=document.createElement('div');e.textContent=d.prazos.error;box.append(e);}}
}}catch(e){{box.textContent='Prazos indisponíveis — confira o cadastro antes de usar.';}}}}
deadlinesLoad();setInterval(deadlinesLoad,60000);
async function mtLoad(){{if(!document.getElementById('model-evaluation-link')){{const a=document.createElement('a');a.id='model-evaluation-link';a.href='/admin/avaliacao-modelos';a.textContent='Comparar modelos do app';document.getElementById('mt-estado').before(a);}}try{{const r=await fetch('/admin/api/motor');if(!r.ok)return;const d=await r.json();const hoje=new Date().toISOString().slice(0,10);const dia=(d.uso_por_dia_utc||{{}})[hoje]||{{}};const g=(dia.global||{{}}).usd||0;document.getElementById('mt-estado').textContent='Motor externo: '+(d.indisponivel||'pronto')+' \u00b7 modelo '+d.modelo+(d.modelo_efetivo&&d.modelo_efetivo!==d.modelo?' (respondendo hoje: '+d.modelo_efetivo+')':'')+(d.modelo_operador!==d.modelo?' (operador: '+d.modelo_operador+')':'')+' \u00b7 ampliados sem escolha: '+d.motor_padrao+' \u00b7 operador: '+d.motor_operador+' \u00b7 gasto hoje (UTC) US$ '+Number(g).toFixed(4)+' de '+Number(d.cotas_usd_dia.global).toFixed(2)+' \u00b7 uso gratuito hoje US$ '+Number(((dia.planos||{{}}).gratuito||{{}}).usd||0).toFixed(4)+' de '+Number(d.cotas_usd_dia.global_gratuito||0).toFixed(2)+(d.trocas_previstas||[]).map(function(x){{return ' \u00b7 '+x.texto}}).join('')+(d.gasto_por_modelo_hoje||[]).map(function(x){{return ' \u00b7 '+x.model+': US$ '+Number(x.usd).toFixed(4)+' (inclui reservas)'}}).join('')+((d.cobrancas_acima_da_reserva||[]).length?' \u00b7 cobran\u00e7as acima da reserva: '+d.cobrancas_acima_da_reserva.length:'')+(d.claude?' \u00b7 Claude: '+(d.claude.indisponivel||'pronto')+' \u00b7 modelo '+d.claude.modelo+' \u00b7 contas: '+((d.claude.contas||[]).join(', ')||'nenhuma')+' \u00b7 gasto hoje (UTC) US$ '+Number(d.claude.gasto_hoje_usd||0).toFixed(4)+' de '+Number((d.claude.cotas_usd_dia||{{}}).global||0).toFixed(2)+((d.claude.cobrancas_acima_da_reserva||[]).length?' \u00b7 Claude acima da reserva: '+d.claude.cobrancas_acima_da_reserva.length:''):'')+(d.erro?' \u00b7 '+d.erro:'')}}catch(e){{}}}}
mtLoad();
const SD_COR={{ok:'#2e7d32',atencao:'#b26a00',critico:'#c0392b',esgotado:'#8e0000',desconhecido:'#6b7079'}};
const SD_ROT={{ok:'EM DIA',atencao:'ATEN\u00c7\u00c3O',critico:'CR\u00cdTICO',esgotado:'ESGOTADO',desconhecido:'SEM SALDO INFORMADO'}};
function sdUsd(v){{return (typeof v==='number')?'US$ '+v.toFixed(2):'\u2014'}}
const SV_EST={{}};const SV_ORD=['esgotado','critico','atencao','desconhecido','ok'];
function svBandeira(){{const f=document.getElementById('saldo-bandeira');if(!f)return;const it=Object.values(SV_EST).filter(function(x){{return x.n!=='ok'}});if(!it.length){{f.style.display='none';return}};it.sort(function(a,b){{return SV_ORD.indexOf(a.n)-SV_ORD.indexOf(b.n)}});f.style.display='block';f.style.background=it[0].cor;f.style.color='#fff';f.textContent=it.map(function(x){{return x.txt}}).join('  |  ')}}
async function sdLoad(forcar){{try{{const r=await fetch('/admin/api/saldo_openai'+(forcar?'?atualizar=1':''));if(!r.ok)return;const d=await r.json();const n=d.nivel||'desconhecido',cor=SD_COR[n]||'#6b7079';document.getElementById('sd-valor').textContent=sdUsd(d.saldo_usd);document.getElementById('sd-valor').style.color=cor;document.getElementById('sd-cartao').style.borderLeftColor=cor;const nv=document.getElementById('sd-nivel');nv.textContent=SD_ROT[n]||n;nv.style.background=cor;nv.style.color='#fff';document.getElementById('sd-ponto').style.background=cor;document.getElementById('sd-sub').textContent=d.mensagem||'';const L=[];if(d.ancora)L.push('Saldo informado: '+sdUsd(d.ancora.valor_usd)+' em '+new Date(d.ancora.em).toLocaleString('pt-BR'));if(typeof d.creditado_desde_ancora_usd==='number')L.push('Compras depois disso: '+sdUsd(d.creditado_desde_ancora_usd)+' \u00b7 gasto desde ent\u00e3o: '+sdUsd(d.gasto_desde_ancora_usd));if(typeof d.gasto_hoje_usd==='number')L.push('Gasto hoje (UTC): '+sdUsd(d.gasto_hoje_usd)+' \u00b7 ritmo (7 dias): '+sdUsd(d.ritmo_usd_dia)+'/dia'+(d.dias_restantes!=null?' \u00b7 dura cerca de '+Math.round(d.dias_restantes)+' dia(s)':''));if(d.limites)L.push('Alerta: aten\u00e7\u00e3o abaixo de '+sdUsd(d.limites.atencao_usd)+' ou '+d.limites.atencao_dias+' dias \u00b7 cr\u00edtico abaixo de '+sdUsd(d.limites.critico_usd)+' ou '+d.limites.critico_dias+' dias');L.push('Fonte do gasto: '+(d.fonte_gasto||'\u2014')+(d.chave_admin_definida?'':' \u00b7 sem chave de administrador (Costs API)'));(d.avisos||[]).forEach(function(a){{if(a)L.push('\u26a0 '+a)}});L.push('Atualizado: '+(d.atualizado_em?new Date(d.atualizado_em).toLocaleString('pt-BR'):'\u2014')+' \u00b7 estimativa conservadora: a OpenAI n\u00e3o fornece o saldo por API');const box=document.getElementById('sd-linhas');box.innerHTML='';L.forEach(function(t){{const p=document.createElement('div');p.textContent=t;box.appendChild(p)}});SV_EST.openai={{n:n,cor:cor,txt:(SD_ROT[n]||n)+' \u00b7 cr\u00e9dito OpenAI '+sdUsd(d.saldo_usd)+' \u00b7 '+(d.mensagem||'')}};svBandeira()}}catch(e){{}}}}
async function sdEnviar(caminho,metodo,corpo){{try{{const r=await fetch(caminho,{{method:metodo,headers:{{'Content-Type':'application/json'}},body:JSON.stringify(corpo)}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};sdLoad(true)}}catch(e){{alert('Erro: '+e)}}}}
function sdAncora(){{const v=prompt('Saldo de cr\u00e9dito que aparece AGORA no painel da OpenAI (Billing), em d\u00f3lares. Ex.: 23.40','');if(v===null||v.trim()==='')return;sdEnviar('/admin/api/saldo_openai/ancora','POST',{{valor_usd:v.trim()}})}}
function sdCompra(){{const v=prompt('Valor da compra de cr\u00e9dito na OpenAI, em d\u00f3lares. Ex.: 20','');if(v===null||v.trim()==='')return;const nota=prompt('Nota (opcional):','')||'';sdEnviar('/admin/api/saldo_openai/compra','POST',{{valor_usd:v.trim(),nota:nota}})}}
function sdLimites(){{const c=prompt('CR\u00cdTICO abaixo de quantos d\u00f3lares?','5');if(c===null)return;const a=prompt('ATEN\u00c7\u00c3O abaixo de quantos d\u00f3lares?','15');if(a===null)return;sdEnviar('/admin/api/saldo_openai/limites','PUT',{{critico_usd:c.trim(),atencao_usd:a.trim()}})}}
sdLoad();setInterval(sdLoad,60000);
async function scLoad(forcar){{try{{const r=await fetch('/admin/api/saldo_claude'+(forcar?'?atualizar=1':''));if(!r.ok)return;const d=await r.json();const n=d.nivel||'desconhecido',cor=SD_COR[n]||'#6b7079';document.getElementById('sc-valor').textContent=sdUsd(d.saldo_usd);document.getElementById('sc-valor').style.color=cor;document.getElementById('sc-cartao').style.borderLeftColor=cor;const nv=document.getElementById('sc-nivel');nv.textContent=SD_ROT[n]||n;nv.style.background=cor;nv.style.color='#fff';document.getElementById('sc-ponto').style.background=cor;document.getElementById('sc-sub').textContent=d.mensagem||'';const L=[];if(d.ancora)L.push('Saldo informado: '+sdUsd(d.ancora.valor_usd)+' em '+new Date(d.ancora.em).toLocaleString('pt-BR'));if(typeof d.creditado_desde_ancora_usd==='number')L.push('Compras depois disso: '+sdUsd(d.creditado_desde_ancora_usd)+' \u00b7 gasto desde ent\u00e3o: '+sdUsd(d.gasto_desde_ancora_usd));if(typeof d.gasto_hoje_usd==='number')L.push('Gasto hoje (UTC): '+sdUsd(d.gasto_hoje_usd)+' \u00b7 ritmo (7 dias): '+sdUsd(d.ritmo_usd_dia)+'/dia'+(d.dias_restantes!=null?' \u00b7 dura cerca de '+Math.round(d.dias_restantes)+' dia(s)':''));if(d.limites)L.push('Alerta: aten\u00e7\u00e3o abaixo de '+sdUsd(d.limites.atencao_usd)+' ou '+d.limites.atencao_dias+' dias \u00b7 cr\u00edtico abaixo de '+sdUsd(d.limites.critico_usd)+' ou '+d.limites.critico_dias+' dias');L.push('Fonte do gasto: '+(d.fonte_gasto||'\u2014')+(d.claude_configurado?'':' \u00b7 o Claude ainda n\u00e3o tem chave neste servidor')+(d.chave_admin_definida?'':' \u00b7 sem chave de administrador da Anthropic (Cost API)'));(d.avisos||[]).forEach(function(a){{if(a)L.push('\u26a0 '+a)}});L.push('Atualizado: '+(d.atualizado_em?new Date(d.atualizado_em).toLocaleString('pt-BR'):'\u2014')+' \u00b7 estimativa conservadora: a Anthropic n\u00e3o fornece o saldo por API');const box=document.getElementById('sc-linhas');box.innerHTML='';L.forEach(function(t){{const p=document.createElement('div');p.textContent=t;box.appendChild(p)}});SV_EST.claude={{n:n,cor:cor,txt:(SD_ROT[n]||n)+' \u00b7 cr\u00e9dito Claude '+sdUsd(d.saldo_usd)+' \u00b7 '+(d.mensagem||'')}};svBandeira()}}catch(e){{}}}}
async function scEnviar(caminho,metodo,corpo){{try{{const r=await fetch(caminho,{{method:metodo,headers:{{'Content-Type':'application/json'}},body:JSON.stringify(corpo)}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};scLoad(true)}}catch(e){{alert('Erro: '+e)}}}}
function scAncora(){{const v=prompt('Saldo de cr\u00e9dito que aparece AGORA no painel da Anthropic (platform.claude.com \u203a Settings \u203a Billing), em d\u00f3lares. Ex.: 23.40','');if(v===null||v.trim()==='')return;scEnviar('/admin/api/saldo_claude/ancora','POST',{{valor_usd:v.trim()}})}}
function scCompra(){{const v=prompt('Valor da compra de cr\u00e9dito na Anthropic, em d\u00f3lares. Ex.: 20','');if(v===null||v.trim()==='')return;const nota=prompt('Nota (opcional):','')||'';scEnviar('/admin/api/saldo_claude/compra','POST',{{valor_usd:v.trim(),nota:nota}})}}
function scLimites(){{const c=prompt('CR\u00cdTICO abaixo de quantos d\u00f3lares?','5');if(c===null)return;const a=prompt('ATEN\u00c7\u00c3O abaixo de quantos d\u00f3lares?','15');if(a===null)return;scEnviar('/admin/api/saldo_claude/limites','PUT',{{critico_usd:c.trim(),atencao_usd:a.trim()}})}}
scLoad();setInterval(scLoad,60000);
// === PORTA ABERTA, PLANOS, BLOQUEIO E DENUNCIAS (14/09/2026, noite) ===
async function uBloq(u,bloq){{let nota='';if(bloq){{const n=prompt('Bloquear '+u+'? A conta perde o acesso na hora (app e web) at\u00e9 voc\u00ea desbloquear.\\nMotivo (opcional):','');if(n===null)return;nota=n}}else if(!confirm('Desbloquear '+u+'?'))return;try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(u)+'/bloquear',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{bloqueado:bloq,nota:nota}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};rU()}}catch(e){{alert('Erro: '+e)}}}}
document.getElementById('utb').addEventListener('change',async function(ev){{const s=ev.target.closest('select[data-plano]');if(!s)return;try{{const r=await fetch('/admin/api/users/'+encodeURIComponent(s.dataset.plano)+'/plano',{{method:'PUT',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{plano:s.value}})}});const d=await r.json();if(!r.ok)alert(d.error||'Erro');rU()}}catch(e){{alert('Erro: '+e)}}}});
async function enLoad(){{try{{const r=await fetch('/admin/api/entrada');if(!r.ok)return;const d=await r.json();const l=d.limites||{{}};const m=d.moderacao||{{}};document.getElementById('en-estado').textContent='Porta aberta: '+(d.aberta_efetiva?'SIM (conta nova com Apple/Google entra no plano gratuito)':('N\u00c3O'+(d.aberta_config?' \u2014 ligada no .env, mas fechada: '+d.motivo+(d.motivo_fechada?' (o p\u00fablico l\u00ea: '+d.motivo_fechada+')':''):' (IALD_ENTRADA_ABERTA desligada)')))+' \u00b7 contas criadas em 24 h: '+(d.criacoes_24h==null?'?':d.criacoes_24h)+' (limites: '+l.por_ip_24h+' por IP, '+l.global_24h+' no total) \u00b7 modera\u00e7\u00e3o: '+(m.ligada?'ligada':'desligada')+(d.erro?' \u00b7 '+d.erro:'')}}catch(e){{}}}}
enLoad();
function dnLinha(x){{const st=x.status==='resolvida'?'<span class="bg bg-ok">Resolvida</span>':'<span class="bg bg-er">Aberta</span>';const ac=x.status==='resolvida'?esc(x.resolvida_por||''):'<button class="bt bt-p bt-sm" data-dn="'+esc(x.id)+'">Resolver</button>';const perg=String(x.pergunta||'');return '<tr><td>'+esc(String(x.criada||'').replace('T',' ').substring(0,16))+'</td><td><span class="mono">'+esc(x.usuario)+'</span><br><span style="font-size:11px;color:#888">'+esc(x.superficie)+' \u00b7 '+esc(x.modelo)+'</span></td><td><b>'+esc(x.motivo)+'</b>'+(x.detalhe?'<br><span style="font-size:12px">'+esc(x.detalhe)+'</span>':'')+'</td><td style="max-width:420px;font-size:12px;white-space:pre-wrap">'+(perg?'<i>'+esc(perg.substring(0,300))+'</i><br>':'')+esc(String(x.resposta||'').substring(0,1200))+'</td><td>'+st+(x.nota?'<br><span style="font-size:11px">'+esc(x.nota)+'</span>':'')+'</td><td>'+ac+'</td></tr>'}}
async function dnLoad(){{const tb=document.getElementById('dn-tb');try{{const r=await fetch('/admin/api/denuncias');const d=await r.json();if(!r.ok){{tb.innerHTML='<tr><td colspan="6" style="color:var(--vermelho);padding:14px">'+esc(d.error||('HTTP '+r.status))+'</td></tr>';return}};const c=d.contagem||{{}};document.getElementById('dn-info').textContent='Abertas: '+(c.aberta||0)+' \u00b7 resolvidas: '+(c.resolvida||0);const ls=d.denuncias||[];tb.innerHTML=ls.length?ls.map(dnLinha).join(''):'<tr><td colspan="6" style="text-align:center;color:#888;padding:20px">Nenhuma den\u00fancia</td></tr>'}}catch(e){{tb.innerHTML='<tr><td colspan="6" style="color:var(--vermelho);padding:14px">Erro: '+esc(e)+'</td></tr>'}}}}
document.getElementById('dn-tb').addEventListener('click',async function(ev){{const b=ev.target.closest('button[data-dn]');if(!b)return;const nota=prompt('Marcar a den\u00fancia como resolvida. Nota (opcional):','');if(nota===null)return;try{{const r=await fetch('/admin/api/denuncias/'+encodeURIComponent(b.dataset.dn)+'/resolver',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{nota:nota}})}});const d=await r.json();if(!r.ok){{alert(d.error||'Erro');return}};dnLoad()}}catch(e){{alert('Erro: '+e)}}}});
dnLoad();
// === CONTRACTS DASHBOARD (v3.1) ===
async function ctLoad(){{
try{{
const r=await fetch('/admin/api/contracts');
if(!r.ok)return;
const cts=await r.json();
const tb=document.getElementById('ct-tb');
if(!cts.length){{tb.innerHTML='<tr><td colspan="7" style="text-align:center;color:#888;padding:20px">Nenhum pedido de contrata\u00e7\u00e3o</td></tr>';return}}
let h='';
for(const c of cts){{
const dt=c.created?new Date(c.created).toLocaleString('pt-BR',{{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}}):'\u2014';
let stBg='bg-st',stTxt=c.status||'?';
if(c.status==='completed'){{stBg='bg-ok';stTxt='Conclu\u00eddo'}}
else if(c.status==='in_progress'){{stBg='bg-te';stTxt='Em andamento'}}
else if(c.status==='rejected'){{stBg='bg-er';stTxt='Recusado'}}
else{{stTxt='Pendente'}}
let actions='';
if(c.status==='pending'){{
actions='<button class="bt bt-p bt-sm" onclick="ctStatus('+jsq(c.id)+',&apos;in_progress&apos;)">\u25B6 Iniciar</button>';
}}else if(c.status==='in_progress'){{
actions='<button class="bt bt-p bt-sm" onclick="ctStatus('+jsq(c.id)+',&apos;completed&apos;)">\u2705 Concluir</button>';
}}
h+='<tr><td>'+esc(dt)+'</td><td>'+esc(c.company_name||'\u2014')+'</td><td class="mono">'+esc(c.cnpj_or_id||'\u2014')+'</td><td>'+esc(c.license_type||'\u2014')+'</td><td class="mono">'+esc(c.username||'\u2014')+'</td><td><span class="bg '+stBg+'">'+esc(stTxt)+'</span></td><td>'+actions+'</td></tr>';
}}
tb.innerHTML=h;
}}catch(e){{console.error('ctLoad:',e)}}
}}
async function ctStatus(id,st){{
if(!confirm('Alterar status do contrato para: '+st+'?'))return;
try{{
const r=await fetch('/admin/api/contracts/'+encodeURIComponent(id)+'/status',{{method:'PUT',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{status:st}})}});
if(r.ok)ctLoad();else alert('Erro');
}}catch(e){{alert('Erro: '+e)}}
}}
// ═══ PSION DASHBOARD ═══
async function psLoad(){{
try{{
const[hb,vb]=await Promise.all([fetch('/admin/api/heartbeat').then(r=>r.json()),fetch('/admin/api/verbal').then(r=>r.json())]);
document.getElementById('ps-gen').textContent=hb.generation||0;
document.getElementById('ps-toks').textContent=(hb.baseline_tok_s||0).toFixed(1);
document.getElementById('ps-cv').textContent=(hb.stability_cv||0).toFixed(4);
document.getElementById('ps-beats').textContent=hb.total_beats||0;
document.getElementById('ps-corr').textContent=vb.total_corrections||0;
const np=vb.pending_patches||0;
document.getElementById('ps-pend').textContent=np;
const pld=document.getElementById('ps-pld');
pld.className=np>0?'d dy':'d dg';
// Patches pendentes
const pp=vb.patches_pending_detail||[];
const pc=document.getElementById('ps-patches');
if(!pp.length){{pc.innerHTML='<span style="color:#aaa">Nenhum patch pendente.</span>'}}
else{{let h='';for(const p of pp){{h+='<div style="background:var(--bg-card);border:1px solid var(--borda);border-radius:8px;padding:12px;margin-bottom:8px">';
h+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><strong style="color:var(--dourado)">'+esc(p.patch_id)+'</strong><span class="bg bg-a">'+esc(p.category)+'</span></div>';
h+='<div style="margin-bottom:8px;font-size:13px">'+esc(p.proposed_addition)+'</div>';
h+='<div style="display:flex;gap:8px"><button class="bt bt-p bt-sm" onclick="psApprove('+jsq(p.patch_id)+')">\\u2705 Aprovar</button>';
h+='<button class="bt bt-d bt-sm" onclick="psReject('+jsq(p.patch_id)+')">\\u274C Rejeitar</button></div></div>'}};
pc.innerHTML=h}}
// Heartbeat history
const hist=(hb.last_beat?[]:[]); // Use full fetch
try{{const hr=await fetch('/admin/api/heartbeat');const hd=await hr.json();
const tb=document.getElementById('ps-htb');
const hs=((hd._history)||[]).slice(-10);
// We use the main data which has limited history in status
let hh='';
if(hb.last_beat){{hh+='<tr><td>'+esc(hb.total_beats||'-')+'</td><td>'+esc(String(hb.last_beat.timestamp||'').substring(0,19))+'</td><td>'+esc(hb.last_beat.tok_s||'-')+'</td><td>'+esc(hb.last_beat.cv||'-')+'</td></tr>'}}
tb.innerHTML=hh||'<tr><td colspan="4" style="text-align:center;color:#aaa">Nenhum beat ainda.</td></tr>'}}catch(e){{}}
// Alerts
const al=hb.alerts||[];
const ac=document.getElementById('ps-alerts');
if(!al.length){{ac.innerHTML='<span style="color:#aaa">Nenhum alerta.</span>'}}
else{{let h='';for(const a of al){{h+='<div style="color:var(--vermelho);margin-bottom:4px">\\u26A0 Beat #'+esc(a.beat)+': '+esc(a.delta_pct)+'% ('+esc(a.measured)+' vs '+esc(a.expected)+' tok/s) \\u2014 '+esc(String(a.timestamp||'').substring(0,16))+'</div>'}};ac.innerHTML=h}}
}}catch(e){{console.error('psLoad:',e)}}}}
async function psTrigger(){{try{{const r=await fetch('/admin/api/heartbeat/trigger',{{method:'POST'}});const d=await r.json();alert('Beat: '+d.result);psLoad()}}catch(e){{alert('Erro: '+e)}}}}
async function psApprove(id){{if(!confirm('Aprovar patch '+id+'? Ser\\u00e1 adicionado ao kernel.'))return;try{{const r=await fetch('/admin/api/verbal/patches/'+encodeURIComponent(id)+'/approve',{{method:'POST'}});const d=await r.json();alert(d.message||'OK');psLoad()}}catch(e){{alert('Erro: '+e)}}}}
async function psReject(id){{if(!confirm('Rejeitar patch '+id+'?'))return;try{{const r=await fetch('/admin/api/verbal/patches/'+encodeURIComponent(id)+'/reject',{{method:'POST'}});const d=await r.json();alert(d.message||'OK');psLoad()}}catch(e){{alert('Erro: '+e)}}}}
setInterval(()=>{{const ps=document.getElementById('s-ps');if(ps&&ps.classList.contains('on'))psLoad()}},5000);
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════
# SELO IALD + EXPORTAÇÃO PELO SERVIDOR (22/09/2026)
#
# Ordens do operador (verbatim, 22/09/2026):
#   "o meu app ainda não está entregando o txt ou md ou pdf das conversas das sessões isso precisa ser
#    alterado, como eu tenho minha própria criptografia, seria possível ao gerar as conversas que cada
#    coversa fosse certificada pela minha própria criptografia, isso seria interessante, porque mostraria
#    que aquela conversa é verdadeira"
#   Escolha dele: "Selo IALD com assinatura pública".
# Build 18 (iPhone): a folha de compartilhar e a de impressão ABREM mas NÃO respondem ao toque. Decisão
# técnica: o SERVIDOR gera o arquivo (txt/md/pdf) e o app abre o endereço dele (window.open → Safari
# externo), onde "Salvar em Arquivos" funciona.
#
# O que mora aqui (o resto está em iald_selo.py, sem Flask):
#   - o selo de cada resposta do chat: UM evento {"iald_selo": …} logo antes do [DONE] — nativa (agente e
#     caminho direto), OpenAI e Claude pelo MESMO gerador, aplicado uma vez depois da view api_post;
#   - GET  /.well-known/iald-selo-keys.json  (público) as chaves PÚBLICAS;
#   - GET  /verificar                        (público) a página de verificação, autocontida, CSP com nonce;
#   - GET  /verificar/verificar_selo.py      (público) o verificador independente em Python;
#   - POST /api/exportar   (conta autenticada, só JSON, ≤ 2 MB, 30 por hora por conta) gera o .txt/.md/.pdf
#     com o Certificado IALD e o bloco de máquina e devolve um endereço de 15 minutos;
#   - GET  /exportado/<token>/<nome>         (público, URL de capacidade) o arquivo, sem cache.
# O selo prova procedência e integridade — NÃO que o conteúdo esteja correto (o certificado diz isso).
# Sem chave/senha o selo fica DESLIGADO (fail-closed, avisado uma vez no log) e a exportação continua.
# ══════════════════════════════════════════════════════════════
import iald_selo  # noqa: E402

SELO_DIR = _segredo("IALD_SELO_DIR", "").strip() or iald_selo.DIR_CHAVES_PADRAO
SELO_ACOM = _segredo("IALD_SELO_ACOM_PATH", "").strip() or iald_selo.ACOM_CAMINHO_PADRAO
CHROME_PDF = _segredo("IALD_CHROME", "").strip() or iald_selo.CHROME_PADRAO
try:
    # a senha só passa por aqui: não fica em variável do módulo
    SELADOR, MOTIVO_SELO = iald_selo.carregar_selador(SELO_DIR, _segredo("IALD_SELO_SENHA", ""), SELO_ACOM)
except Exception as _exc_selo:          # noqa: BLE001 — o selo nunca derruba o servidor
    SELADOR, MOTIVO_SELO = None, f"falha ao carregar ({type(_exc_selo).__name__})"
CHAVES_SELO = iald_selo.RegistroDeChaves(SELO_DIR)
if SELADOR is not None:
    print(f"[selo] LIGADO: kid={SELADOR.kid}; selo da casa: "
          f"{'disponível' if SELADOR.casa_disponivel else SELADOR.motivo_casa}", flush=True)
else:
    print(f"[selo] DESLIGADO: {MOTIVO_SELO} — as respostas seguem sem selo; a exportação funciona", flush=True)


_SELO_CHAVE_AVISADA = []
# 22/09/2026 (revisão): nota de corte do servidor no fim do texto → o recibo sai com "cortada": true
_NOTAS_DE_CORTE = tuple(v for v in getattr(iald_motor_claude, "NOTA_CORTE", {}).values() if isinstance(v, str))


def _chave_do_selo_ativa():
    """A chave em uso segue "ativa" no registro público (consulta com cache de ~5 s, antes de cada selo).
    Revogada ou fora do registro → nenhuma resposta é selada, e o log diz isso UMA vez."""
    selador = SELADOR
    if selador is None:
        return False
    status = CHAVES_SELO.status_de(selador.kid)
    if status != "ativa":
        if not _SELO_CHAVE_AVISADA:
            _SELO_CHAVE_AVISADA.append(True)
            print(f"[selo] a chave {selador.kid} está '{status}' no registro público: respostas sem selo até "
                  "o operador gerar outra chave e reiniciar o servidor", flush=True)
        return False
    return True


def _pedido_de_selo(req_json, subpath):
    """Tira iald_conv/iald_selo_prev do corpo (SEMPRE) e devolve o pedido de selo — ou None (selo desligado,
    chave revogada, rota que não é o chat, conversa ausente ou campo inválido: a resposta segue, sem selo).
    22/09/2026 (revisão): o pedido leva a marca OPACA da conta da sessão (acct): a cadeia de uma conversa só
    vale se todos os turnos forem da mesma conta."""
    conv = req_json.pop("iald_conv", None)
    prev = req_json.pop("iald_selo_prev", None)
    if subpath != "chat/completions" or SELADOR is None or conv is None:
        return None
    try:
        if not _chave_do_selo_ativa():
            return None
        return iald_selo.PedidoDeSelo.do_cliente(conv, prev, req_json.get("messages"),
                                                 SELADOR.marca_da_conta(session.get("username", "")))
    except (TypeError, ValueError) as exc:
        print(f"[selo] pedido sem selo: {exc}", flush=True)
        return None


def _selar_resposta_sse(fluxo, selador, pedido):
    """O stream final do chat, byte a byte, com UM evento {"iald_selo": …} logo antes do [DONE]
    (iald_selo.selar_fluxo_sse: só com fim normal, texto não vazio, chave ainda ativa e nenhum iald_aviso,
    erro ou marca ": iald-sem-selo" — moderação que retira a resposta, recusa e falha nunca são seladas;
    texto que termina na nota de corte do servidor sai com "cortada": true)."""
    return iald_selo.selar_fluxo_sse(fluxo, selador, pedido, registrar=lambda msg: print(msg, flush=True),
                                     notas_de_corte=_NOTAS_DE_CORTE, pode_selar=_chave_do_selo_ativa)


@app.after_request
def _selo_da_resposta(resposta):
    """O ponto ÚNICO do selo: a resposta final de api_post (a moderação da resposta, a medição TGLC e o
    iald_modelo já estão dentro dela). Roda na requisição; o gerador roda depois, sem contexto de Flask."""
    pedido = g.pop("iald_selo", None)
    if pedido is None:
        return resposta
    try:
        selador = SELADOR
        if (selador is not None and request.endpoint == "api_post" and resposta.status_code == 200
                and resposta.mimetype == "text/event-stream" and not resposta.direct_passthrough):
            resposta.response = _selar_resposta_sse(resposta.response, selador, pedido)
            resposta.headers.pop("Content-Length", None)
    except Exception as exc:          # noqa: BLE001 — o selo nunca derruba a resposta
        print(f"[selo] não aplicado ({type(exc).__name__})", flush=True)
    return resposta


@app.route("/.well-known/iald-selo-keys.json", endpoint="selo_chaves_publicas")
def selo_chaves_publicas():
    """As chaves PÚBLICAS do selo (ativas e revogadas). Nada secreto; nada da patente."""
    corpo = json.dumps({"fmt": iald_selo.FMT_CHAVES, "chaves": CHAVES_SELO.todas()},
                       ensure_ascii=False, sort_keys=True, indent=2)
    resposta = Response(corpo, status=200, mimetype="application/json")
    resposta.headers["Cache-Control"] = "public, max-age=3600"
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    return resposta


@app.route("/verificar", endpoint="verificar_pagina")
def verificar_pagina():
    """A página pública de verificação: tudo inline, com o nonce desta resposta; sem rede (as chaves vão
    embutidas); nenhum script externo."""
    nonce = secrets.token_urlsafe(18)
    resposta = Response(iald_selo.pagina_verificar(nonce, CHAVES_SELO.todas(), URL_PUBLICA),
                        status=200, mimetype="text/html")
    resposta.headers["Content-Security-Policy"] = (
        f"default-src 'none'; script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'; img-src data:; "
        "connect-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; "
        "require-trusted-types-for 'script'")
    resposta.headers["Cache-Control"] = "no-store"
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["Referrer-Policy"] = "no-referrer"
    resposta.headers["X-Frame-Options"] = "DENY"
    return resposta


CAMINHO_VERIFICADOR_SELO = os.path.join(SERVE_DIR, "ferramentas_selo", "verificar_selo.py")


@app.route("/verificar/verificar_selo.py", endpoint="selo_verificador_py")
def selo_verificador_py():
    """O verificador independente (só hashlib + cryptography), para navegador sem Ed25519."""
    try:
        with open(CAMINHO_VERIFICADOR_SELO, "rb") as f:
            dados = f.read()
    except OSError:
        return Response("Verificador indisponível.", status=404, mimetype="text/plain")
    resposta = Response(dados, status=200, mimetype="text/x-python")
    resposta.headers["Content-Disposition"] = 'attachment; filename="verificar_selo.py"'
    resposta.headers["Cache-Control"] = "public, max-age=3600"
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["Content-Security-Policy"] = "sandbox"
    return resposta


EXPORTAR_POR_HORA = 30
EXPORTAR_MAX_MENSAGENS = 400
EXPORTAR_MAX_TITULO = 120
# 22/09/2026 (revisão): teto do texto que vai ao PDF (título + turnos, em caracteres) — acima disso, 413
EXPORTAR_PDF_MAX_CARACTERES = 200_000
LIMITE_EXPORTAR = iald_motores.JanelaDePedidos(EXPORTAR_POR_HORA, 3600.0)
EXPORTACOES = iald_selo.ArmazemExportacoes(validade_s=15 * 60, max_itens=50, max_bytes=50 * 1024 * 1024)
TIPOS_EXPORTACAO = {"txt": "text/plain; charset=utf-8", "md": "text/markdown; charset=utf-8",
                    "pdf": "application/pdf"}
MSG_PDF_INDISPONIVEL = "O PDF não pôde ser gerado agora; exporte em .md ou .txt."
MSG_PDF_GRANDE = ("A conversa é grande demais para PDF (mais de 200 mil caracteres); exporte em .md ou .txt.")
MSG_EXPORTANDO = "Espere a exportação anterior terminar."
# 22/09/2026 (revisão): dois PDFs por vez NO MÁXIMO e sem fila — o terceiro recebe 503 na hora (antes
# esperava até 30 s segurando uma das 16 threads do waitress); e uma exportação por conta de cada vez (429)
_SEMAFORO_PDF = threading.BoundedSemaphore(2)
_EXPORTANDO = set()
_TRAVA_EXPORTANDO = threading.Lock()
_abrir_chrome = subprocess.Popen             # os testes trocam por um Chrome falso
_matar_chrome = iald_selo.matar_arvore       # tempo esgotado: taskkill /T /F (a árvore inteira do Chrome)


def _erro_exportar(mensagem, status):
    return Response(json.dumps({"error": mensagem}, ensure_ascii=False), status=status,
                    content_type="application/json")


def _turnos_para_exportar(dados):
    """([{role, texto_bruto, selo}], "") ou (None, mensagem). O texto vai BRUTO (só os substitutos UTF-16
    órfãos viram U+FFFD, senão não cabe em UTF-8); o selo só vale em turno da IALD."""
    mensagens = dados.get("mensagens")
    if not isinstance(mensagens, list) or not mensagens:
        return None, "mensagens deve ser uma lista não vazia."
    if len(mensagens) > EXPORTAR_MAX_MENSAGENS:
        return None, f"A exportação aceita até {EXPORTAR_MAX_MENSAGENS} mensagens."
    turnos = []
    for m in mensagens:
        if not isinstance(m, dict) or m.get("role") not in ("user", "assistant") or not isinstance(m.get("texto"), str):
            return None, "Cada mensagem precisa de role (user ou assistant) e texto."
        selo = m.get("selo")
        if selo is not None and not isinstance(selo, dict):
            return None, "selo, quando presente, deve ser um objeto."
        turnos.append({"role": m["role"], "texto_bruto": iald_selo.texto_utf8(m["texto"]),
                       "selo": selo if m["role"] == "assistant" else None})
    return turnos, ""


def _atestacao_da_casa(turnos, verificacao):
    """A segunda atestação (selo da casa), conferida AQUI nos turnos autênticos. Revisão 2 (22/09/2026): sai
    como um valor de LISTA FIXA (iald_selo.casa_texto) — o verificador refaz o texto; nada livre no bloco."""
    autenticos = [turnos[i["pos"]] for i in verificacao["turnos"] if i["status"] == iald_selo.AUTENTICA]
    if not autenticos:
        return None
    if SELADOR is None or not SELADOR.casa_disponivel:
        return {"tipo": "indisponivel"}
    desta_chave = [t for t in autenticos if ((t.get("selo") or {}).get("recibo") or {}).get("kid") == SELADOR.kid]
    if not desta_chave:
        return {"tipo": "chave_anterior"}
    conferidas = sum(1 for t in desta_chave if SELADOR.verificar_casa(t.get("selo")) is True)
    return {"tipo": "conferida", "n": conferidas, "m": len(desta_chave)}


@app.route("/api/exportar", methods=["POST"])
def api_exportar():
    """Gera a conversa em .txt/.md/.pdf com o Certificado IALD (verificado aqui, contra as chaves públicas)
    e devolve {url, caminho, expira_em, selados, total, resultado, rotulo}. O arquivo fica 15 minutos em
    memória atrás de um token de 256 bits; o app abre o endereço no Safari externo. Uma exportação por
    conta de cada vez (429); PDF sem fila (503) e com teto de texto (413)."""
    from werkzeug.exceptions import RequestEntityTooLarge
    usuario = session.get("username", "")
    if not usuario:
        return _erro_exportar("Não autenticado", 401)
    if not LIMITE_EXPORTAR.permitir(usuario):
        return _erro_exportar("Muitas exportações em pouco tempo. Tente de novo mais tarde.", 429)
    if not request.is_json:
        return _erro_exportar("Envie application/json.", 415)
    if (request.content_length or 0) > LIMITE_CORPO_EXPORTAR_BYTES:
        return _erro_exportar("A conversa passa do tamanho aceito para exportação (2 MB).", 413)
    try:
        dados = request.get_json(silent=True)
    except RequestEntityTooLarge:
        return _erro_exportar("A conversa passa do tamanho aceito para exportação (2 MB).", 413)
    if not isinstance(dados, dict):
        return _erro_exportar("Envie um objeto JSON com formato, titulo e mensagens.", 400)
    formato = dados.get("formato")
    if formato not in TIPOS_EXPORTACAO:
        return _erro_exportar("formato deve ser txt, md ou pdf.", 400)
    titulo = dados.get("titulo") or ""
    if not isinstance(titulo, str) or len(titulo) > EXPORTAR_MAX_TITULO:
        return _erro_exportar(f"titulo deve ser texto de até {EXPORTAR_MAX_TITULO} caracteres.", 400)
    turnos, erro = _turnos_para_exportar(dados)
    if turnos is None:
        return _erro_exportar(erro, 400)
    if formato == "pdf" and len(titulo) + sum(len(t["texto_bruto"]) for t in turnos) > EXPORTAR_PDF_MAX_CARACTERES:
        return _erro_exportar(MSG_PDF_GRANDE, 413)
    with _TRAVA_EXPORTANDO:
        if usuario in _EXPORTANDO:
            return _erro_exportar(MSG_EXPORTANDO, 429)
        _EXPORTANDO.add(usuario)
    try:
        return _gerar_exportacao(usuario, formato, iald_selo.texto_utf8(titulo), turnos)
    finally:
        with _TRAVA_EXPORTANDO:
            _EXPORTANDO.discard(usuario)


def _gerar_exportacao(usuario, formato, titulo, turnos):
    verificacao = iald_selo.verificar_turnos(turnos, CHAVES_SELO.todas())
    casa = _atestacao_da_casa(turnos, verificacao)
    url_verificar = URL_PUBLICA + "/verificar"
    nome = iald_selo.nome_arquivo(titulo, formato)
    if formato == "pdf":
        if not _SEMAFORO_PDF.acquire(blocking=False):
            return _erro_exportar(MSG_PDF_INDISPONIVEL, 503)
        try:
            html_pdf = iald_selo.documento_html(titulo, turnos, verificacao, casa=casa, url_verificar=url_verificar)
            arquivo = iald_selo.gerar_pdf(html_pdf, chrome=CHROME_PDF, abrir=_abrir_chrome, matar=_matar_chrome,
                                          registrar=lambda msg: print(msg, flush=True))
        except Exception as exc:          # noqa: BLE001 — Chrome ausente, falhou, demorou
            print(f"[selo] PDF não gerado ({exc if isinstance(exc, iald_selo.ErroPDF) else type(exc).__name__})",
                  flush=True)
            return _erro_exportar(MSG_PDF_INDISPONIVEL, 503)
        finally:
            _SEMAFORO_PDF.release()
    else:
        arquivo = iald_selo.documento_texto(titulo, turnos, verificacao, formato, casa=casa,
                                            url_verificar=url_verificar).encode("utf-8")
    try:
        token, expira_em = EXPORTACOES.guardar(arquivo, TIPOS_EXPORTACAO[formato], nome)
    except ValueError:
        return _erro_exportar("O arquivo exportado ficou grande demais.", 413)
    caminho = f"/exportado/{token}/{nome}"
    auth_log("EXPORTAR", usuario, f"formato={formato} selados={verificacao['selados']}/{verificacao['total']}")
    return jsonify({"url": URL_PUBLICA + caminho, "caminho": caminho, "expira_em": expira_em,
                    "selados": verificacao["selados"], "total": verificacao["total"],
                    "resultado": verificacao["resultado"], "rotulo": verificacao["rotulo"]})


@app.route("/exportado/<token>/<nome>", endpoint="exportado_servir")
def exportado_servir(token, nome):
    """O arquivo exportado (URL de capacidade, 15 minutos). O token nunca vai para log."""
    item = EXPORTACOES.obter(token)
    if item is None:
        resposta = Response("Arquivo não encontrado ou expirado. Exporte a conversa de novo.", status=404,
                            mimetype="text/plain")
        resposta.headers["Cache-Control"] = "no-store"
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        return resposta
    resposta = Response(item["dados"], status=200)
    resposta.headers["Content-Type"] = item["tipo"]
    resposta.headers["Content-Disposition"] = (f'inline; filename="{item["nome"]}"; '
                                               f"filename*=UTF-8''{_quote(item['nome'])}")
    resposta.headers["Cache-Control"] = "no-store"
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["Referrer-Policy"] = "no-referrer"
    if item["tipo"].startswith("text/"):
        resposta.headers["Content-Security-Policy"] = "sandbox"
    return resposta


# The one-use reconciliation was completed under local custody. Keep its
# artifacts for recovery; normal app startup must not import its frozen R3 modules.
_OWNER_CONSOLIDATION = None
app.config.setdefault('OWNER_APPLE_CONSOLIDATION_ENABLED', False)
app.config.setdefault('OWNER_APPLE_CONSOLIDATION_DIR', os.path.join(SERVE_DIR, 'owner_private', 'consolidation'))
if app.config.get('OWNER_APPLE_CONSOLIDATION_ENABLED') is True:
    sys.path.insert(0, os.path.join(SERVE_DIR, 'owner_consolidation_r5'))
    from r5_http import register as _register_owner_consolidation

    def _owner_consolidation_snapshot():
        with _TRAVA_USUARIOS:
            p = Path(USERS_FILE)
            if p.stat().st_size > 8 * 1024 * 1024:
                raise _OwnerAuthDenied('consolidation_snapshot_size')
            return p.read_bytes()

    _OWNER_CONSOLIDATION = _register_owner_consolidation(globals(), _owner_consolidation_snapshot)

# Owner Apple privilege has its own protected custody and isolated local bridge.
app.config['OWNER_APPLE_BINDING_DIR'] = os.path.join(SERVE_DIR, 'owner_private', 'apple')
app.config['OWNER_APPLE_CAPTURE_ENABLED'] = True  # Capture still requires a one-use local arm.
from iald_owner_office import register as _register_owner_office

def _owner_reauthentication_hint():
    # Eligibility for a hint only. Every private action still needs Apple proof.
    return _OWNER_CHAT_ROUTER.account().get('canonical_owner') is True

_register_owner_office(app, require_owner_private,
    config_path=os.path.join(SERVE_DIR, 'owner_private', 'bridge.json'),
    native_origins=ORIGENS_APP, reauthentication_hint=_owner_reauthentication_hint,
    revoke=lambda: _owner_adapter().revoke_request(),
    domain_guard=lambda operation, arguments: _OWNER_CHAT_ROUTER.require_office_operation(operation, arguments))


# ══════════════════════════════════════════════════════════════
# STATIC FILES CATCH-ALL (must be LAST route)
# ══════════════════════════════════════════════════════════════

@app.route("/<path:filename>")
def static_files(filename):
    # Old bookmarks and installed web shortcuts use the same authenticated app.
    if filename == 'iald_chat.html':
        response = redirect(_destino_web(session.get('username', '')))
        response.headers['Cache-Control'] = 'no-store'
        return response
    allowed = {
        'iald_chat.html', 'iald_cartao_virtual.html', 'iald_cartao_visita.html',
        'iald_logo_header.png', 'sw.js', 'manifest.json',
        'app/index.html', 'app/owner_office.js', 'app/iald.js', 'app/iald_transport.mjs', 'app/chat_wire_codec.mjs', 'app/registration_identity.js', 'app/iald.css', 'app/operational_deadlines.js',
        'app/kernel_prompt.js', 'app/kernel_prompt_loja.js', 'app/kernel_prompt_bundle.js',
        # 13/09/2026 — redesenho do app: logos oficiais e bibliotecas embarcadas
        # (antes vinham de CDN e o logo de um caminho absoluto ausente no pacote).
        'app/img/iald_logo_header.png', 'app/img/iald_logo_transparent_final.png',
        'app/img/iald_logo_dark_transparent_final.png',
        'app/img/betatgl.png', 'app/img/betatgl.ico',
        'app/vendor/marked.min.js', 'app/vendor/katex/katex.min.js', 'app/vendor/katex/katex.min.css',
    }
    # Fontes do KaTeX: só os .woff2 com o nome exato do pacote, nada além disso.
    fonte_katex = re.fullmatch(r'app/vendor/katex/fonts/KaTeX_[A-Za-z0-9_-]+\.woff2', filename)
    if filename not in allowed and not fonte_katex:
        return Response('Arquivo não disponível.', status=404)
    if filename in {'app/iald_transport.mjs', 'app/chat_wire_codec.mjs'}:
        return send_from_directory(SERVE_DIR, filename, mimetype='text/javascript')
    return send_from_directory(SERVE_DIR, filename)


# ══════════════════════════════════════════════════════════════
# CENTRAL DE PATENTES — a aba "Usuários (app IALD)" (21/09/2026)
#
# Ordem do operador (verbatim, 21/09/2026): "eu preciso que o campo "usuários" [...] esteja na minha
# central de patentes, especificamente na patente da IALD, em uma aba lá, porque assim eu consigo
# liberar pela internet qualquer usuário eu não preciso estar presente aqui no meu pc".
# Decisões dele (21/09/2026): a IALD PUXA (nada novo entra no PC; nenhuma rota nova no túnel); SÓ
# aprovar/recusar pedido e bloquear/desbloquear conta — nunca em conta de administrador, nunca criar
# admin, senha, exportar, apagar, plano ou acesso nativo; o step-up é feito na Central; à Central
# (Render, EUA — LGPD) só vão nome, e-mail MASCARADO, username, status, datas, provedor e tentativas.
#
# O protocolo (HMAC nos dois sentidos, seq, caixa de saída, tetos) mora em iald_sync_central.py.
# Aqui ficam o RETRATO (o que sai) e o EXECUTOR (o que entra) — pelas MESMAS funções e travas do
# painel (_aprovar_pedido, _recusar_pedido, _bloquear_conta). A thread só nasce no processo real
# (bloco __main__ → _iniciar_sincronizador_central); importar este arquivo nos testes não liga nada.
# ══════════════════════════════════════════════════════════════
try:
    import iald_sync_central
except Exception as _exc_sync:          # noqa: BLE001 — sem o módulo o servidor segue, sem a aba
    iald_sync_central = None
    print(f"[central-sync] módulo indisponível ({type(_exc_sync).__name__}); aba da Central desligada",
          flush=True)

CENTRAL_ESTADO_ARQUIVO = os.path.join(SERVE_DIR, "iald_sync_central_estado.json")
CENTRAL_OPERADOR = "central"            # o "por" do que a Central decide (pedido, bloqueio, log)
CENTRAL_MAX_PEDIDOS = 500               # pendentes primeiro; a Central apara acima de 1000
CENTRAL_MAX_USUARIOS = 2000             # bloqueadas primeiro; a Central apara acima de 5000
CENTRAL_DIAS_DECIDIDOS = 30             # pedidos decididos que ainda vão no retrato
CENTRAL_TETO_RETRATO = 890_000          # bytes do retrato (o módulo recusa acima de 900 KB)
# plano da conta que a Central aprova: o FIXADO pelo operador (IALD_CENTRAL_SYNC_PLANO), nunca "operador"
CENTRAL_PLANOS_APROVAR = (iald_motores.GRATUITO, iald_motores.ASSINANTE)
CENTRAL_PLANO_PADRAO = iald_motores.GRATUITO
SINCRONIZADOR_CENTRAL = None
_CENTRAL_PROBLEMA = [""]


def _central_tamanho(obj):
    return len(json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def _central_nome_base(nome):
    """O nome (já sem controle/bidi e com e-mail/CPF mascarados) sem acento: a base da sugestão.

    LGPD (21/09/2026): a sugestão da Central sai do NOME, não do e-mail como no painel local — o
    username sugerido vai à Central, e derivá-lo da parte local do e-mail mandaria o e-mail que o
    operador escolheu mascarar. A aprovação pela Central cria a conta com ESTA sugestão.
    """
    limpo = iald_sync_central.texto_livre(nome, 80)
    return unicodedata.normalize("NFKD", limpo).encode("ascii", "ignore").decode("ascii")


def _central_email(email, *nomes):
    """O e-mail MASCARADO que vai no item — ou "" (o item vai SEM e-mail) quando um nome que vai junto
    (username, usuario, sugestão) começa pela parte local do e-mail (21/09/2026, revisão adversarial).

    LGPD: a porta aberta e a sugestão padrão do painel tiram o username da parte local do e-mail
    (identidade._base_sugerida). "joao.silva1985" + "jo***@gmail.com" devolveria o endereço inteiro ao
    Render — a máscara que o operador escolheu não serviria. A comparação usa a MESMA derivação que a
    IALD usa para criar o nome (minúsculas, só [a-z0-9_.-], até 24 caracteres)."""
    mascarado = iald_sync_central.mascarar_email(email)
    if not mascarado:
        return ""
    local = identidade._base_sugerida(str(email or ""), "")
    for n in nomes:
        n = str(n or "").strip().lower()
        if n and local and n.startswith(local):
            return ""
    return mascarado


def _central_retrato():
    """O retrato mínimo para a Central: SÓ as chaves que a Central aceita (iald_app_users.py
    _CHAVES_PEDIDO/_CHAVES_USUARIO), e-mail já mascarado aqui ('ma***@gmail.com') — e AUSENTE quando o
    username/usuario/sugestão do item começa pela parte local dele (_central_email) —, texto livre sem
    controle/bidi e sem e-mail/CPF, conta de administrador como 'protegido'. Nunca tgl_hash,
    identidades/sub, ip_chave, cota_chave, plano, motor ou uso. Pedidos: pendentes (mais recentes
    primeiro) e depois os decididos dos últimos 30 dias; contas: bloqueadas, protegidas, ativas.
    Acima do teto em bytes, apara do fim (decididos → ativas → protegidas → pendentes antigos)."""
    from iald_registration_identity import project_identity
    sc = iald_sync_central
    identity_requests = PEDIDOS.listar()
    usuarios = load_users_estrito()
    lapide = PEDIDOS.nomes_indisponiveis()
    corte = (datetime.now() - timedelta(days=CENTRAL_DIAS_DECIDIDOS)).isoformat(timespec="seconds")
    # dono de cada identidade calculado UMA vez por retrato (antes: pedidos × contas a cada busca)
    donos = {(i.get("provedor"), i.get("sub")) for d in usuarios.values() if isinstance(d, dict)
             for i in identidade.identidades_publicas(d)}
    pendentes, decididos = [], []
    for p in identity_requests:
        if not isinstance(p, dict):
            continue
        pid, st = str(p.get("id") or ""), p.get("status")
        if not sc.RE_PEDIDO.match(pid) or st not in sc.STATUS_PEDIDO:
            continue
        item = {"id": pid, "status": st}
        nome = sc.texto_livre(p.get("nome"), 80)
        if nome:
            item["nome"] = nome
        prov = p.get("provedor")
        if isinstance(prov, str) and sc.RE_PROVEDOR.match(prov):
            item["provedor"] = prov
        for campo in ("criado", "ultima_tentativa", "decidido_em"):
            data = sc.data_valida(p.get(campo))
            if data:
                item[campo] = data
        tentativas = p.get("tentativas")
        if isinstance(tentativas, int) and not isinstance(tentativas, bool) and 0 <= tentativas <= 1_000_000:
            item["tentativas"] = tentativas
        if st == identidade.PENDENTE:
            prov_sub = (p.get("provedor", ""), p.get("sub", ""))
            tem_dono = prov_sub[0] in identidade.PROVEDORES and bool(prov_sub[1]) and prov_sub in donos
            if not tem_dono:
                item["sugestao"] = identidade.sugerir_username_aberto(
                    usuarios, "", _central_nome_base(p.get("nome")), indisponiveis=lapide)
            email = _central_email(p.get("email"), item.get("sugestao"))
            if email:
                item["email"] = email
            pendentes.append(item)
            continue
        usuario = p.get("usuario")
        if st == identidade.APROVADO and isinstance(usuario, str) and sc.RE_USUARIO.match(usuario):
            item["usuario"] = usuario
        email = _central_email(p.get("email"), item.get("usuario"))
        if email:
            item["email"] = email
        quando = str(p.get("decidido_em") or p.get("encerrado_em") or p.get("criado") or "")
        if quando >= corte:
            decididos.append((quando, item))
    decididos.sort(key=lambda x: x[0], reverse=True)
    pedidos = (pendentes + [i for _, i in decididos])[:CENTRAL_MAX_PEDIDOS]

    bloqueadas, protegidas, ativas = [], [], []
    for username, d in usuarios.items():
        if not isinstance(d, dict) or not isinstance(username, str) or not sc.RE_USUARIO.match(username):
            continue
        bloqueada = _conta_bloqueada(d)
        st = "protegido" if d.get("admin") else ("bloqueado" if bloqueada else "ativo")
        item = {"username": username, "status": st}
        # Preserve legacy primary display name after the existing export sanitizer.
        display_record = dict(d, name=sc.texto_livre(d.get("name"), 80))
        projected = project_identity(display_record, username, identity_requests)
        nome = sc.texto_livre(projected["name"], 80)
        if nome:
            item["nome"] = nome
        email = _central_email(projected["email"], username)
        if email:
            item["email"] = email
        provedores = [i.get("provedor") for i in identidade.identidades_publicas(d)]
        item["provedor"] = next((x for x in provedores if isinstance(x, str) and sc.RE_PROVEDOR.match(x)), "senha")
        criado = sc.data_valida(d.get("created"))
        if criado:
            item["criado"] = criado
        if bloqueada and isinstance(d.get("bloqueado"), dict):
            em = sc.data_valida(d["bloqueado"].get("em"))
            if em:
                item["bloqueado_em"] = em
        (bloqueadas if st == "bloqueado" else protegidas if st == "protegido" else ativas).append(item)
    ativas.sort(key=lambda i: i.get("criado", ""), reverse=True)
    contas = (bloqueadas + protegidas + ativas)[:CENTRAL_MAX_USUARIOS]

    retrato = {"gerado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
               "pedidos": pedidos, "usuarios": contas}
    tam = _central_tamanho(retrato)
    if tam > CENTRAL_TETO_RETRATO:
        ordem = (("pedidos", lambda i: i["status"] != "pendente"), ("usuarios", lambda i: i["status"] == "ativo"),
                 ("usuarios", lambda i: i["status"] == "protegido"), ("pedidos", lambda i: True),
                 ("usuarios", lambda i: True))
        for chave, cabe in ordem:
            lista = retrato[chave]
            i = len(lista) - 1
            while tam > CENTRAL_TETO_RETRATO and i >= 0:
                if cabe(lista[i]):
                    tam -= _central_tamanho(lista[i]) + 1
                    lista.pop(i)
                i -= 1
            if tam <= CENTRAL_TETO_RETRATO:
                break
    return retrato


def _central_log(evento, extra):
    """auth_log das ordens da Central que NUNCA levanta (21/09/2026, revisão adversarial): um print que
    falha DEPOIS de uma ação gravada não pode virar 'transitório' (repetição) nem 'falhou'."""
    try:
        auth_log(evento, CENTRAL_OPERADOR, extra, ip="central-sync")
    except Exception:  # noqa: BLE001
        pass


def _central_conta_desta_ordem(alvo, sugestao):
    """Depois de uma exceção inesperada na aprovação: o username se a conta DESTA ordem já existe
    (pedido aprovado pela Central, ou a identidade do pedido já ligada à conta `sugestao` criada por
    liberação). "" se não existe; None se não deu para saber (leitura falhou)."""
    try:
        p = PEDIDOS.obter(alvo)
        if not p:
            return ""
        if p.get("status") == identidade.APROVADO and p.get("decidido_por") == CENTRAL_OPERADOR:
            return str(p.get("usuario") or "") or None
        usuarios = load_users_estrito()
        dono = identidade.usuario_da_identidade(usuarios, p.get("provedor", ""), p.get("sub", ""))
        if (dono and sugestao and dono == sugestao
                and (usuarios.get(dono) or {}).get("source") == f"{p.get('provedor', '')}_liberado"):
            return dono
        return ""
    except Exception:  # noqa: BLE001
        return None


def _central_executar(comando, sugestao=None):
    """(ok, mensagem, transitorio) — uma ordem da Central, pelas MESMAS funções do painel.

    Roda na thread da sincronização (sem requisição Flask). A allowlist do módulo já passou; aqui
    vale a de negócio: conta de administrador nunca é alvo, pedido desconhecido ou fora de pendente
    é recusado, aprovar cria SÓ conta nova com a sugestão UNÂNIME dos retratos que a Central pode ter
    mostrado (nunca 'vincular', nunca acesso ampliado) e no plano FIXADO pelo operador
    (comando["plano_iald"], posto pelo módulo a partir de IALD_CENTRAL_SYNC_PLANO; nunca vem da
    Central). Mensagem curta, sem e-mail nem nome — no máximo o username. Toda ação e toda recusa
    vão ao log com o id do comando (auth_log CENTRAL_*).

    `transitorio=True` só quando NADA foi alterado (cadastro/pedidos ilegíveis): volta na próxima busca.
    REVISÃO ADVERSARIAL (21/09/2026): o `try` cobre só o que roda ANTES da gravação — as funções do
    painel gravam por último (os.replace) e, na aprovação pela Central, nada levanta depois de a conta
    ser gravada (_aprovar_pedido devolve 200 com aviso). Os logs de sucesso ficam FORA do try e nunca
    levantam (_central_log): antes, um print falhando depois de uma recusa ou bloqueio gravados virava
    "nada foi alterado" e a repetição dava "falhou".
    """
    acao, alvo, cid = comando.get("acao"), comando.get("alvo"), comando.get("id")
    nota = str(comando.get("nota") or "")[:200]
    base = f"comando={cid} seq={comando.get('seq')} acao={acao} alvo={alvo}"

    def recusa(msg):
        _central_log("CENTRAL_RECUSADO", f"{base} motivo={msg}")
        return False, msg, False

    def adiar(msg):
        _central_log("CENTRAL_ADIADO", f"{base} motivo={msg}")
        return False, msg, True

    def adiar_por(exc):
        if isinstance(exc, (UsuariosIlegiveis, UsuariosNaoGravados)):
            return adiar("cadastro de contas indisponível na IALD; nada foi alterado — nova tentativa na "
                         "próxima busca")
        return adiar(f"registro de pedidos indisponível na IALD ({type(exc).__name__}); nada foi alterado — "
                     "nova tentativa na próxima busca")

    if acao == "aprovar":
        plano = comando.get("plano_iald") or CENTRAL_PLANO_PADRAO
        if plano not in CENTRAL_PLANOS_APROVAR:
            return recusa("plano de aprovação fora da lista da IALD (gratuito ou assinante); nada foi feito")
        try:
            p = PEDIDOS.obter(alvo)
            if not p:
                return recusa("pedido não encontrado na IALD; nada foi feito")
            if p.get("status") != identidade.PENDENTE:
                return recusa(f"o pedido já está '{p.get('status')}' na IALD; nada foi feito")
            dono = identidade.usuario_da_identidade(load_users_estrito(), p.get("provedor", ""), p.get("sub", ""))
            if dono:                     # nunca 'vincular' pela Central (e o retrato nem sugere nome)
                return recusa(f"a identidade deste pedido já pertence à conta '{dono}'; decida pelo painel local")
            if not sugestao:
                return recusa("sem nome sugerido nos retratos que a Central pode ter mostrado; aguarde a "
                              "próxima sincronização e aprove de novo")
            corpo, status, info = _aprovar_pedido(alvo, "novo", sugestao, False, CENTRAL_OPERADOR,
                                                  via_central=True, plano_central=plano)
        except (UsuariosIlegiveis, UsuariosNaoGravados, OSError, ValueError) as exc:
            # por construção só chega aqui ANTES da gravação da conta; se mesmo assim a conta desta
            # ordem existir, o resultado é FINAL (nunca repetir o que já foi feito)
            feito = _central_conta_desta_ordem(alvo, sugestao)
            if feito:
                _central_log("CENTRAL_ACESSO_LIBERADO",
                             f"{base} usuario={feito} (com aviso: {type(exc).__name__} depois da gravação)")
                return True, (f"conta '{feito}' criada, com aviso ({type(exc).__name__} depois da gravação) "
                              "— confira no painel local"), False
            return adiar_por(exc)
        if status == 200:
            info = info or {}
            nome, plano_efetivo = corpo["username"], info.get("plano") or plano
            aviso = info.get("aviso") or ""
            _central_log("CENTRAL_ACESSO_LIBERADO",
                         f"{base} usuario={nome} via={info.get('provedor', '')} plano={plano_efetivo} "
                         f"acesso=chatgpt" + (" aviso=pedido_nao_marcado" if aviso else ""))
            msg = f"conta '{nome}' criada (plano {plano_efetivo}); a pessoa já pode entrar"
            return True, (msg + "; ATENÇÃO: " + aviso) if aviso else msg, False
        if status == 503:
            return adiar(str(corpo.get("error") or "indisponível"))
        return recusa(str(corpo.get("error") or f"recusado (HTTP {status})"))

    if acao == "recusar":
        try:
            p = PEDIDOS.obter(alvo)
            if not p:
                return recusa("pedido não encontrado na IALD; nada foi feito")
            if p.get("status") != identidade.PENDENTE:
                return recusa(f"o pedido já está '{p.get('status')}' na IALD; nada foi feito")
            # a conferência de verdade (pendente; identidade de admin protegida) é refeita DENTRO das travas
            corpo, status = _recusar_pedido(alvo, nota, CENTRAL_OPERADOR, via_central=True)
        except (UsuariosIlegiveis, UsuariosNaoGravados, OSError, ValueError) as exc:
            return adiar_por(exc)
        if status == 200:
            _central_log("CENTRAL_ACESSO_RECUSADO", base)
            return True, "pedido recusado", False
        return recusa(str(corpo.get("error") or f"recusado (HTTP {status})"))

    if acao in ("bloquear", "desbloquear"):
        bloquear = acao == "bloquear"
        try:
            corpo, status = _bloquear_conta(alvo, bloquear, nota, CENTRAL_OPERADOR, via_central=True)
        except (UsuariosIlegiveis, UsuariosNaoGravados, OSError, ValueError) as exc:
            return adiar_por(exc)
        if status == 200:
            u = corpo["username"]
            palavra = "bloqueada" if bloquear else "desbloqueada"
            if corpo.get("sem_mudanca"):
                msg = f"a conta '{u}' já estava {palavra}; nada mudou"
            else:
                msg = f"conta '{u}' {palavra}"
            _central_log("CENTRAL_BLOQUEIO" if bloquear else "CENTRAL_DESBLOQUEIO",
                         f"{base} {'sem_mudanca' if corpo.get('sem_mudanca') else 'aplicado'}")
            return True, msg, False
        return recusa(str(corpo.get("error") or f"recusado (HTTP {status})"))

    return recusa("ação fora da lista da IALD; nada foi feito")


@app.route("/admin/api/central-sync", methods=["GET"])
def admin_central_sync_estado():
    """Estado da sincronização com a Central (21/09/2026). Local + admin, como todo /admin.
    Sem segredo, sem e-mail, sem nome — só números, datas e a última falha."""
    check = require_admin()
    if check:
        return check
    sinc = SINCRONIZADOR_CENTRAL
    if sinc is None:
        return jsonify({"habilitado": False, "rodando": False,
                        "problema": _CENTRAL_PROBLEMA[0] or "sincronização não iniciada neste processo"})
    return jsonify(sinc.status())


def _iniciar_sincronizador_central(iniciar=True):
    """Cria (e, com iniciar=True, liga) a sincronização com a Central. Chamado SÓ pelo __main__.
    Segredo ausente/fraco → sem thread, com o motivo no log e em /admin/api/central-sync.
    21/09/2026 (revisão): UMA instância por arquivo de estado — a trava do SO em <estado>.lock é pega
    no construtor, antes de ler o estado; um segundo processo do servidor (outra porta) fica SEM
    sincronizar, com o motivo no log e em /admin/api/central-sync."""
    global SINCRONIZADOR_CENTRAL
    if iald_sync_central is None:
        _CENTRAL_PROBLEMA[0] = "módulo iald_sync_central indisponível"
        return None
    try:
        cfg = iald_sync_central.config_do_ambiente(_segredo, CENTRAL_ESTADO_ARQUIVO,
                                                   proibidos=(app.secret_key,))
        sinc = iald_sync_central.SincronizadorCentral(
            cfg, _central_executar, retrato=_central_retrato,
            auditar=lambda evento, extra: auth_log(evento, CENTRAL_OPERADOR, extra, ip="central-sync"))
        SINCRONIZADOR_CENTRAL = sinc
        _CENTRAL_PROBLEMA[0] = sinc.problema
        if iniciar:
            sinc.iniciar()
    except Exception as exc:  # noqa: BLE001 — a aba da Central nunca derruba o servidor
        _CENTRAL_PROBLEMA[0] = f"falha ao iniciar ({type(exc).__name__})"
        print(f"[central-sync] não iniciada: {_CENTRAL_PROBLEMA[0]}", flush=True)
    return SINCRONIZADOR_CENTRAL


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

# IALD_ORCHESTRATOR_ADMIN_20260923
try:
    _iald_orchestrator_path = 'C:\\IALD\\Central de Patentes\\Chatgpt\\IALD_ORQUESTRACAO_20260923'
    if _iald_orchestrator_path not in sys.path:
        sys.path.insert(0, _iald_orchestrator_path)
    from iald_orchestrator.web import install as _install_iald_orchestrator
    _install_iald_orchestrator(app, require_admin)
except Exception as _iald_orchestrator_error:
    print("[orchestrator] UNAVAILABLE: " + type(_iald_orchestrator_error).__name__, flush=True)
    @app.route("/admin/agi/orquestracao")
    def _iald_orchestrator_unavailable():
        _denied = require_admin()
        if _denied is not None:
            return _denied
        return "Orquestracao indisponivel; verificar a instalacao local.", 503

@app.route('/admin/api/avaliacao-modelos')
def admin_model_evaluation():
    check = require_admin()
    if check: return check
    if not session.get('is_admin') or session.get('username') != 'luiz':
        return jsonify({'error': 'Acesso restrito ao operador.'}), 403
    result=APP_EVALUATION.report()
    result["routing"]=app_router.report()
    result["jev"]="Padrão das contas aprovadas: JEV escolhe somente entre executores autorizados e consentidos; sem repetição após envio."
    return jsonify(result)


@app.route('/admin/avaliacao-modelos')
def admin_model_evaluation_page():
    check = require_admin()
    if check: return check
    if not session.get('is_admin') or session.get('username') != 'luiz':
        return jsonify({'error': 'Acesso restrito ao operador.'}), 403
    return Response(APP_EVALUATION_PAGE, content_type='text/html; charset=utf-8',
        headers={'Content-Security-Policy': CSP_PAINEL, 'Cache-Control': 'no-store'})


from iald_app_evaluation_page import PAGE as APP_EVALUATION_PAGE


# Chat jobs retain encrypted output while the mobile WebView is suspended.
import iald_chat_jobs
import iald_notification_runtime
def _push_token_expiry(token):
    _, issued = _serializador_token().loads(token, max_age=TOKEN_APP_MAX_AGE, return_timestamp=True)
    return issued.timestamp() + TOKEN_APP_MAX_AGE

NOTIFY_RESPONSE, PURGE_PUSH = iald_notification_runtime.register(
    app, SERVE_DIR, ORIGENS_APP, load_users_estrito, _conta_bloqueada, token_expiry=_push_token_expiry)
def _chat_account_generation(username):
    record = load_users_estrito().get(username)
    if not record:
        raise iald_chat_jobs.JobError('Não autenticado.', 401)
    material = 'iald-account:' + username + ':' + str(record.get('created', 'legacy'))
    return hashlib.sha256(material.encode('utf-8')).hexdigest()

import iald_native_activity  # Capture the loaded native adapter in the import receipt.
import iald_activity_ui
iald_activity_ui.register(app, account_key=_chat_account_generation, json_guard=_identificacao_json_post)

import iald_wallet_recovery
WALLET_PROCESS_LEASE, WALLET_RECOVERY_REPORT = iald_wallet_recovery.acquire_and_recover(SERVE_DIR)

# Routing metadata only. Parent initializes the EMPTY DPAPI registry explicitly.
# Pin only the exact scientific SYSTEM strings generated by trusted server sources.
from iald_jev_office_gateway import Gateway, PrivacyState, account_from_adapter
from iald_jev_office_gateway import register as _register_chat_privacy
_OWNER_CHAT_ROUTER = Gateway(
    PrivacyState(os.path.join(SERVE_DIR, 'owner_private', 'chat_privacy')),
    account=lambda: account_from_adapter(_owner_adapter(), session),
    apple_guard=require_owner_private, select_domain=app_router.select_domain)
_OWNER_CHAT_PUBLIC_GUARD = _register_chat_privacy(app, _OWNER_CHAT_ROUTER,
    origin_ok=_private_media_origin_ok,
    private_forward=lambda identity, operation, args: __import__('iald_owner_office').forward(
        os.path.join(SERVE_DIR, 'owner_private', 'bridge.json'), identity['principal'], operation, args))

CHAT_JOBS = iald_chat_jobs.register(app, SERVE_DIR, notify=NOTIFY_RESPONSE,
                                     account_key=_chat_account_generation,
                                     transport_origin_check=_private_media_origin_ok,
                                     public_admission_guard=_OWNER_CHAT_PUBLIC_GUARD)


import iald_wallet_routes
WALLET_DISPATCH, MONTHLY_WALLET = iald_wallet_routes.register(
    app, SERVE_DIR, users=load_users_estrito, account_key=_chat_account_generation,
    allowed=app_router.allowed, admin_check=require_admin,
    native=_chat_nativa_automatica, warning=_sse_aviso)


# Lazy encrypted attachment custody; account generation is already defined above.
PRIVATE_MEDIA_HOST = private_media_host.Host(SERVE_DIR,generation=_chat_account_generation,
    users=load_users_estrito,allowed=app_router.allowed,app_memory=app_memory,
    dispatch_guard=_dispatch_guard,budget_available=_automatic_budget_available,
    rates=app_providers.MODELS['mimo']['rates'],
    validate_upload=__import__('iald_mimo_multimodal').validate_upload)
PRIVATE_MEDIA_HOST.admitted_task = lambda:wallet_runtime.current() if wallet_runtime.enabled() else None
PRIVATE_MEDIA_ROUTES = private_media_host.register(app,PRIVATE_MEDIA_HOST,
    authenticated_user=lambda:session.get('username','') if session.get('authenticated') else '',
    binary_origin_ok=_private_media_origin_ok,json_guard=_identificacao_json_post)

if __name__ == "__main__":
    _install_task_download_log_filter()
    # Independent local worker; no model call and no duplicate Codex automation.
    try:
        updater_root = os.path.join(SERVE_DIR, 'canonical_releases', 'v410_608b7108977e', 'continuous_update')
        science_update_hook.ensure_worker(sys.executable,
            os.path.join(updater_root, 'continuous_update_adapter.py'),
            os.path.join(updater_root, 'config.json'),
            os.path.join(SERVE_DIR, '.iald_runtime', 'science_update', 'worker.log'))
    except (OSError, ValueError, RuntimeError):
        print('[science-update] Worker unavailable; previous scientific release retained. Inspect administrative status.', flush=True)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else WEB_PORT
    try:
        r = req_lib.get(f"{LLAMA_URL}/health", timeout=3)
        llm_status = "ONLINE" if r.status_code == 200 else "ERRO"
    except Exception:
        llm_status = "OFFLINE"
    search_status = "Google API" if GOOGLE_SEARCH_AVAILABLE else ("DuckDuckGo" if DDG_AVAILABLE else "NONE")
    psutil_status = "AVAILABLE" if PSUTIL_AVAILABLE else "NOT INSTALLED (pip install psutil)"
    coin_status = f"AVAILABLE ({coin_engine.get_ledger_stats()['total_accounts']} accounts)" if COIN_AVAILABLE else "NOT AVAILABLE"
    psinet_status = f"AVAILABLE (max {psinet_engine.get_config()['max_file_size_mb']} MB)" if PSINET_AVAILABLE else "NOT AVAILABLE"
    hb_status = f"ACTIVE ({HEARTBEAT_INTERVAL // 60}min interval)" if llm_status == "ONLINE" else "STANDBY (llama offline)"
    _vs = get_verbal_status()
    verbal_status = f"ACTIVE ({_vs.get('total_corrections', 0)} corrections, {_vs.get('pending_patches', 0)} pending)"
    n_users = len(USERS)
    n_admins = sum(1 for u in USERS.values() if u.get("admin", False))
    print(f"""
+==============================================================+
|  IALD Web Server v9 — Central de Comando + Agent Loop       |
|  http://localhost:{port}/                                       |
|  Admin: http://localhost:{port}/admin (localhost only)           |
|  Proxy: /v1/* -> llama-server:{LLAMA_PORT}                        |
|  llama-server: {llm_status:8s}                                     |
|  Search: {search_status:46s} |
|  psutil: {psutil_status:46s} |
|  TGL Coin: {coin_status:44s} |
|  PSI-NET: {psinet_status:45s} |
|  Heartbeat: {hb_status:43s} |
|  Verbal:  {verbal_status:44s} |
|  Users: {n_users} registered ({n_admins} admin) | Session: {SESSION_TIMEOUT_HOURS}h  |
|  beta_TGL = alpha x sqrt(e) = 0.012031300400803142           |
+==============================================================+
    """, flush=True)
    if llm_status == "OFFLINE":
        print("  AVISO: llama-server nao rodando na porta 8081.\n")
    for u, d in USERS.items():
        role = "admin" if d.get("admin") else "user"
        print(f"    - {u} ({role})", flush=True)
    print(flush=True)
    # ── Start Psion Heartbeat (only if llama-server is online) ──
    if llm_status == "ONLINE":
        psion_heartbeat.start()
    else:
        print("[Heartbeat] Adiado — llama-server offline.", flush=True)

    # ── 21/09/2026: a aba "Usuários (app IALD)" da Central de Patentes — a IALD PUXA (ver
    #    iald_sync_central.py). Só aqui, no processo real: a importação pelos testes não liga nada.
    #    Sem IALD_CENTRAL_SYNC_SEGREDO válido, não nasce thread nenhuma (o motivo sai no log).
    _iniciar_sincronizador_central()

    # ── SERVIDOR WSGI DE PRODUÇÃO (02/08/2026) ──
    # Antes: app.run(...) — o servidor de DESENVOLVIMENTO do Werkzeug, que o próprio
    # Flask avisa não ser para produção, servindo o mundo através do túnel cloudflared
    # (demo.iald.ia.br). Agora: waitress, WSGI de produção, puro Python, estável no
    # Windows. Continua ouvindo só em 127.0.0.1 — quem publica é o túnel.
    #
    # threads=8: o chat é I/O-bound (espera o llama-server), então poucas threads
    # bastam. channel_timeout alto porque uma resposta longa do modelo demora; o
    # keepalive SSE do agent_loop é quem cuida do lado da Cloudflare.
    # 14/09/2026 (noite): 8 → 16. Com a porta aberta, cada stream da OpenAI prende uma
    # thread; o plano gratuito tem teto próprio (IALD_GRATUITO_STREAMS_SIMULTANEOS,
    # padrão 4) e o resto fica para o painel, o operador e os assinantes.
    # ⚠ Só vale depois de REINICIAR o servidor (ato do operador).
    # Fail-open: sem waitress, cai no servidor de desenvolvimento e AVISA.
    try:
        from waitress import serve as _serve_wsgi
        print(f"[IALD] Servidor: waitress (producao) em 127.0.0.1:{port}", flush=True)
        _serve_wsgi(app, host="127.0.0.1", port=port, threads=16,
                    channel_timeout=900, ident="IALD")
    except ImportError:
        print("[IALD] AVISO: waitress ausente — caindo no servidor de "
              "DESENVOLVIMENTO do Werkzeug (nao recomendado com o tunel ativo).",
              flush=True)
        print("       Instale com: python -m pip install --user waitress", flush=True)
        app.run(host="127.0.0.1", port=port, threaded=True, debug=False)
