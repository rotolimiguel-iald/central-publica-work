# -*- coding: utf-8 -*-
"""sincronizar_bancada.py -- o elo B(n) da cadeia de selo: vincula a Bancada Um ao um.py selado.  REVISAO R2 (13/10/2026).

ESBOCO FUNCIONAL R2 do desenho da gerencia c1 (12/10/2026), por ordem do operador de 12/10 (verbatim em
work\\cunhagens_12out\\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt, sha256 lido por script no recibo).
A R1 (d9927a8fdc5cfc62) foi REPROVADA pela auditoria independente (AUDITORIA_VINCULO_BANCADA_C1.md, 13/10) com os achados A1-A13;
a R2 conserta um a um, cada conserto com teste negativo proprio (R2\\CONTROLES_NEGATIVOS_R2.json). A R1 fica como registro em
R2\\originais_R1\\. NAO ESTA INSTALADO. Roda em sandbox contra COPIAS da Bancada em raiz curta (T16). A instalacao na cadeia (passo
B(n)) e a primeira re-pinagem da producao (B3, depois do selo da v392) sao atos que o desenho reserva a gerencia e ao operador.

O que faz, nesta ordem, e tudo fail-closed (qualquer divergencia = recusa visivel, codigo 2; bateria reprovada = codigo 3):
  0. GUARDAS DE CAMINHO (A2, A5): a identidade de toda pasta e por os.path.samefile (st_dev+st_ino), depois de normalizar o prefixo
     \\\\?\\, o UNC local (\\\\127.0.0.1\\C$, \\\\localhost\\C$, \\\\<host>\\C$), juncao, nome 8.3 e caixa; UNC nao local e recusado.
     --saida so dentro das raizes permitidas (a pasta de trabalho da cadeia ou a raiz curta do sandbox) e nunca sob a producao,
     o Nos ou a propria --bancada.
  1. LE O SELO do Nos (um_absoluto_selo.json) e o um.py: a versao (UM_VERSION, linha UNICA na coluna 0 -- A11), o sha256 do um.py
     que o selo pina, a linha UNICA de ALPHA_FINE_CODATA_2018 (nenhuma reatribuicao, nem indentada -- A11) e beta = alpha*sqrt(e)
     EM RUNTIME (nunca literal), conferido contra o beta do core (um_absoluto.json) com tolerancia NOMEADA.
  2. VERIFICA O EVENTO c1 (A4) pela cadeia de hash do eventos.jsonl (anterior == hash do elo anterior; hash recalculado), exigindo
     tipo SINCRONIZACAO_BANCADA, quem claude-c1, e os campos nomeados por JSON (versao, bancada por identidade, um_py e selo por
     sha256, acao), sem texto que negue a gravacao, sem seq duplicado.
  3. LE O MANIFESTO VIGENTE da Bancada e o estado do contrato instalado; recusa --sandbox se o manifesto pinar o Nos real (A2);
     recusa re-pino com a mesma versao e hash diferente do um.py (SELO_PROGRAMA_DIVERGE -- A8) salvo --reparo-de-pino com evento
     que o diga; confere o recibo pre-selo por identidade (versao anterior, um.py antes pinado, mesma Bancada) e encadeia o seu
     hash no manifesto novo (A6).
  4. REGENERA O MANIFESTO (mesmos pinos de codigo e de fontes; pinos novos do um.py e do selo; geracao B(n); evento c1; contrato),
     recusando caminho com '..', absoluto ou fora da raiz em code[].path e copias[].para (A10).
  5. RE-PINA numa COPIA de ensaio e confere com o canonical.py instalado (ok, versao, sha, beta bit a bit).
  6. RODA A BATERIA pinada (A7: sha256 do BATERIA_VINCULO.json por --bateria-sha256 e sha256 canonico de cada teste; conjunto minimo
     obrigatorio em aplicar) a partir dos caminhos PINADOS em fontes[] (A3: {fonte:N}; sha256 conferido ANTES de cada teste; todo
     .py executado tem de ser fonte pinada ou copia conferida; {vinculo} e proibido). T17 le o recibo do build do kernel por hash,
     sem subprocesso (A1). Nenhum __pycache__ nasce na Bancada (A9: sys.dont_write_bytecode e PYTHONDONTWRITEBYTECODE).
  7. GRAVA O RECIBO; so em --modo aplicar, com evento verificado, servico parado e bateria passada, grava o manifesto novo na
     Bancada (backup de bytes, temporario -> conferir -> os.replace, reconferencia pelo canonical.py instalado, rollback se falhar).
Nada aqui le dado observado para veredito, nada move o gate, nada e leitura fisica. NOT_FALSIFIED nunca e creditacao.
"""
import sys
sys.dont_write_bytecode = True   # A9: nenhum .pyc nasce na Bancada alvo quando o canonical.py instalado e importado
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import os
import re
import socket
import subprocess
import time
from pathlib import Path
from unittest.mock import patch

if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (asserts sao guardas)")

REVISAO = "R2 (13/10/2026)"
AQUI = Path(__file__).resolve().parent
PRODUCAO = Path(r"C:\IALD\Bancada_Um")
NOS_PADRAO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TUNEL_PADRAO = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
EVENTOS_QUADRO = Path(r"C:\IALD\PROGRAMA_IALD\eventos.jsonl")
# A5: --saida so dentro destas raizes (a pasta de trabalho da cadeia; a raiz curta do sandbox por causa do limite de caminho, T16)
RAIZES_SAIDA = (Path(r"C:\IALD\Central de Patentes\work"), Path(r"C:\t"))
PORTA_BANCADA = 18777
EVENTO_TIPO = "SINCRONIZACAO_BANCADA"
EVENTO_AUTOR = "claude-c1"
# a MESMA regex do canonical.py instalado (l.73-74): coluna 0, sem indentacao
RE_VERSAO = re.compile(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', re.M)
RE_ALPHA = re.compile(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)', re.M)
# A11: unicidade da linha de coluna 0 (alpha e UM_VERSION) E nenhuma reatribuicao indentada (medido no um.py v391 8e7b9927: zero)
RE_ALPHA_LINHAS = re.compile(r'^ALPHA_FINE_CODATA_2018[ \t]*=(?!=)', re.M)
RE_VERSAO_LINHAS = re.compile(r'^UM_VERSION[ \t]*=(?!=)', re.M)
RE_ALPHA_INDENTADA = re.compile(r'^[ \t]+ALPHA_FINE_CODATA_2018[ \t]*=(?!=)', re.M)
RE_VERSAO_INDENTADA = re.compile(r'^[ \t]+UM_VERSION[ \t]*=(?!=)', re.M)
RE_GERACAO = re.compile(r'^B(\d+)-')
RE_SHA256 = re.compile(r'^[0-9a-f]{64}$')
# A4: texto que NEGA a gravacao (o evento autoriza; nao pode conter negacao, veto ou recusa em nenhum campo de texto)
RE_NEGACAO = re.compile(r"(?i)\b(n[aã]o|nunca|jamais|proib\w*|vet(a|o|ar|ado|ada)\b|recus\w*|cancel\w*|suspend\w*|revog\w*)\b")
ESPERADOS_POS_SELO = ("PIN_CHANGED", "CANONICAL_VERSION_CHANGED", "SEAL_PROGRAM_MISMATCH")
# a guarda da regua (a mesma do um.py e do iald.py), montada em pedacos para que o token nunca exista neste arquivo
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
BETA_TOLERANCIA_REL = 1e-11   # medido em 12/10 (H_BANCADA): |beta_core - beta_runtime|/beta = 5.43e-13; a tolerancia e nomeada, nao escondida
BATERIA_MINIMA = ("T01_IDENTIDADE", "T15_SONDAS")          # A7: sem estes dois nao ha bateria em aplicar
BATERIA_MINIMA_POS_SELO = ("T17_LEAN_KERNEL",)             # A7/A1: em aplicar pos_selo o kernel selado entra pelo recibo do build
HOSTS_LOCAIS = {"localhost", "127.0.0.1", "::1", ".", socket.gethostname().lower()}
try:
    HOSTS_LOCAIS.add(socket.getfqdn().lower())
except OSError:
    pass


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def agora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(p):
    b = Path(p).read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha256(b))


class Recusa(Exception):
    """Recusa fail-closed: o codigo e a primeira palavra; o resto e o motivo."""


# ---------------------------------------------------------------- 0. identidade de caminhos (A2, A5, A10)
def caminho_canonico(p):
    """Normaliza a FORMA do caminho antes de resolver: tira o prefixo \\\\?\\ (e \\\\?\\UNC\\, \\\\.\\), traduz UNC LOCAL (\\\\host\\X$\\...)
    para X:\\..., recusa UNC nao local; depois Path.resolve() (juncao, symlink, nome 8.3, '..', caixa do disco)."""
    s = os.fspath(p)
    if s.startswith("//"):
        s = "\\\\" + s[2:]
    if s.startswith("\\\\?\\UNC\\") or s.startswith("\\\\.\\UNC\\"):
        s = "\\\\" + s[8:]
    elif s.startswith("\\\\?\\") or s.startswith("\\\\.\\"):
        s = s[4:]
    m = re.match(r"^\\\\([^\\/]+)[\\/]([A-Za-z])\$(?:[\\/](.*))?$", s)
    if m:
        if m.group(1).lower() not in HOSTS_LOCAIS:
            raise Recusa("CAMINHO_UNC_NAO_LOCAL: " + s)
        s = m.group(2).upper() + ":\\" + (m.group(3) or "")
    if s.startswith("\\\\") or s.startswith("//"):
        raise Recusa("CAMINHO_UNC_NAO_ADMITIDO: " + s)
    return Path(s).resolve()


def mesmo_no(a, b):
    """Identidade por st_dev+st_ino (os.path.samefile) quando os dois existem; senao, o caminho canonico sem caixa."""
    a, b = caminho_canonico(a), caminho_canonico(b)
    try:
        return os.path.samefile(a, b)
    except OSError:
        return os.path.normcase(str(a)) == os.path.normcase(str(b))


def dentro_de(filho, pai):
    """filho == pai ou filho esta sob pai, por caminho canonico (a existencia do filho nao e exigida)."""
    f, p = caminho_canonico(filho), caminho_canonico(pai)
    if mesmo_no(f, p):
        return True
    fs, ps = os.path.normcase(str(f)), os.path.normcase(str(p)).rstrip("\\")
    return fs.startswith(ps + "\\")


def relativo_seguro(rel, raiz):
    """A10: um caminho relativo do manifesto ou da bateria so pode descer dentro da raiz: sem '..', sem absoluto, sem drive, e o
    destino resolvido tem de ficar sob a raiz."""
    s = str(rel)
    p = Path(s.replace("/", "\\"))
    if p.is_absolute() or p.drive or p.anchor or ".." in p.parts or s.startswith(("\\", "/")) or ":" in s:
        raise Recusa("CAMINHO_RELATIVO_INVALIDO: %r" % s)
    dst = (Path(raiz) / p).resolve()
    if not dentro_de(dst, raiz):
        raise Recusa("CAMINHO_FORA_DA_RAIZ: %r" % s)
    return dst


def gravar_novo(p, data):
    """Grava arquivo NOVO (nunca sobrescreve): temporario -> conferir tamanho e bytes -> os.replace."""
    p = Path(p)
    if p.exists():
        raise Recusa("ARQUIVO_JA_EXISTE: " + str(p))
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp_sync")
    with tmp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.stat().st_size != len(data) or tmp.read_bytes() != data:
        tmp.unlink()
        raise Recusa("ESCRITA_CURTA: " + str(p))
    os.replace(tmp, p)
    if p.read_bytes() != data:
        raise Recusa("ESCRITA_DIVERGE: " + str(p))
    return p


def json_bytes(obj):
    s = json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False, default=str)
    if GUARDA.search(s):
        raise Recusa("PALAVRA_PROIBIDA_NA_SAIDA")
    return (s + "\n").encode("utf-8")


def carregar_canonical(bancada):
    """Importa o canonical.py INSTALADO naquela Bancada (nunca o de outra), com nome de modulo unico; sem bytecode (A9)."""
    assert sys.dont_write_bytecode, "A9: dont_write_bytecode tem de estar ligado antes de importar o canonical.py da Bancada"
    p = Path(bancada) / "bancada" / "canonical.py"
    if not p.is_file():
        raise Recusa("CANONICAL_PY_AUSENTE: " + str(p))
    nome = "canonical_instalado_" + sha256(p.read_bytes())[:12]
    spec = importlib.util.spec_from_file_location(nome, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod, pin(p)


# ---------------------------------------------------------------- 1. o selo e o um.py
def ler_nos(nos, versao):
    nos = caminho_canonico(nos)   # o manifesto pina caminhos ABSOLUTOS: um caminho relativo seria resolvido contra a raiz da Bancada (PIN_UNREADABLE)
    um_p, selo_p, core_p = nos / "um.py", nos / "um_absoluto_selo.json", nos / "um_absoluto.json"
    for p in (um_p, selo_p):
        if not p.is_file():
            raise Recusa("NOS_INCOMPLETO: " + str(p))
    raw = um_p.read_bytes()
    selo_raw = selo_p.read_bytes()
    try:
        selo = json.loads(selo_raw)
    except ValueError as exc:
        raise Recusa("SELO_ILEGIVEL: " + str(exc))
    if selo.get("um_version") != versao:
        raise Recusa("SELO_VERSAO_DIFERENTE: selo=%r alvo=%r" % (selo.get("um_version"), versao))
    pinado = (selo.get("sha256") or {}).get("um.py")
    if pinado != sha256(raw):
        raise Recusa("SELO_NAO_PINA_O_UM_PY_DO_DISCO: selo=%s disco=%s" % (str(pinado)[:16], sha256(raw)[:16]))
    texto = raw.decode("utf-8-sig")
    v, a = RE_VERSAO.search(texto), RE_ALPHA.search(texto)
    if v is None or a is None:
        raise Recusa("CANONICAL_DECLARATION_MISSING")
    if v.group(1) != versao:
        raise Recusa("UM_VERSION_DIFERENTE_DO_ALVO: %r" % v.group(1))
    # A11: UM_VERSION e ALPHA sao declaracoes UNICAS: uma linha na coluna 0 e nenhuma reatribuicao indentada.
    # O Python executaria a ULTIMA atribuicao; o canonical.py le a PRIMEIRA: a unica leitura segura e quando so ha uma.
    # Medido no um.py v391 (8e7b9927ceae64b8): 1 linha de cada na coluna 0, 0 indentadas -- a regra nao custa nada ao canonico.
    n_alpha = len(RE_ALPHA_LINHAS.findall(texto))
    if n_alpha != 1:
        raise Recusa("ALPHA_LINHA_NAO_UNICA: %d linhas nao indentadas" % n_alpha)
    n_alpha_ind = len(RE_ALPHA_INDENTADA.findall(texto))
    if n_alpha_ind:
        raise Recusa("ALPHA_REATRIBUIDA_INDENTADA: %d atribuicoes indentadas (o Python executaria a ultima; o contrato le a unica)" % n_alpha_ind)
    n_versao = len(RE_VERSAO_LINHAS.findall(texto))
    if n_versao != 1:
        raise Recusa("UM_VERSION_LINHA_NAO_UNICA: %d linhas nao indentadas" % n_versao)
    n_versao_ind = len(RE_VERSAO_INDENTADA.findall(texto))
    if n_versao_ind:
        raise Recusa("UM_VERSION_REATRIBUIDA_INDENTADA: %d atribuicoes indentadas" % n_versao_ind)
    alpha = float(a.group(1))
    if not (math.isfinite(alpha) and 0 < alpha < 1):
        raise Recusa("ALPHA_OUTSIDE_CONTRACT")
    linha_alpha = texto[:a.start()].count("\n") + 1
    beta = alpha * math.sqrt(math.e)          # EM RUNTIME, nunca literal
    if not core_p.is_file():
        raise Recusa("CORE_AUSENTE: " + str(core_p))
    core_raw = core_p.read_bytes()
    pin_core = (selo.get("sha256") or {}).get("um_absoluto.json")
    if pin_core is not None and pin_core != sha256(core_raw):
        raise Recusa("SELO_NAO_PINA_O_CORE_DO_DISCO")
    core = json.loads(core_raw).get("core") or {}
    beta_core = core.get("beta")
    if not isinstance(beta_core, (int, float)) or isinstance(beta_core, bool):
        raise Recusa("CORE_SEM_BETA")
    rel = abs(beta - float(beta_core)) / beta
    if rel > BETA_TOLERANCIA_REL:
        raise Recusa("BETA_CORE_DIVERGE_DO_RUNTIME: rel=%.3e" % rel)
    core_info = dict(path=str(core_p), bytes=len(core_raw), sha256=sha256(core_raw), beta_core=repr(float(beta_core)),
                     beta_rel_diff=rel, tolerancia_rel=BETA_TOLERANCIA_REL, qg_closure_verdict=core.get("qg_closure_verdict"))
    return dict(dir=str(nos), um_py=dict(path=str(um_p), bytes=len(raw), sha256=sha256(raw)),
                selo=dict(path=str(selo_p), bytes=len(selo_raw), sha256=sha256(selo_raw), um_version=selo.get("um_version"),
                          qg_closure_verdict=selo.get("qg_closure_verdict"),
                          tgl_kernel_proof_manifest_sha256=(selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")),
                core=core_info, UM_VERSION=v.group(1),
                alpha=dict(valor=alpha, linha=linha_alpha, n_linhas_nao_indentadas=n_alpha, n_reatribuicoes_indentadas=n_alpha_ind),
                um_version_linhas=dict(nao_indentadas=n_versao, indentadas=n_versao_ind),
                beta_runtime=repr(beta), _beta=beta, _raw=raw, _selo_raw=selo_raw)


# ---------------------------------------------------------------- 2. o evento c1 (A4)
def _hash_evento(e):
    return hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _textos(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from _textos(v)
    elif isinstance(o, list):
        for v in o:
            yield from _textos(v)


def verificar_evento(evento, versao, bancada, sandbox, nos_info, reparo=False, eventos_path=None):
    """A4: o evento que autoriza a gravacao e lido do livro de eventos pela CADEIA DE HASH (a mesma regra de iald.py verificar():
    anterior == hash do elo anterior e hash == sha256 do proprio elo sem o campo hash), do primeiro elo ate o evento citado; os
    campos sao conferidos por JSON, nao por substring; texto que negue a gravacao e recusado."""
    if evento is None or not str(evento).strip():
        raise Recusa("EVENTO_C1_AUSENTE: nenhuma gravacao na Bancada sem evento c1 nomeado")
    ev = str(evento).strip()
    eventos_path = Path(eventos_path) if eventos_path else EVENTOS_QUADRO
    if ev.startswith("SANDBOX:"):
        if not sandbox:
            raise Recusa("EVENTO_SANDBOX_FORA_DO_SANDBOX")
        return dict(evento=ev, verificado=False, nota="sandbox: evento literal, nao conferido no quadro")
    if not ev.isdigit():
        raise Recusa("EVENTO_C1_INVALIDO: %r (seq numerico de eventos.jsonl ou, so em --sandbox, SANDBOX:<texto>)" % ev)
    if not eventos_path.is_file():
        raise Recusa("EVENTOS_JSONL_AUSENTE: " + str(eventos_path))
    seq = int(ev)
    ant, achado, n, seqs = "0" * 64, None, 0, set()
    for linha in eventos_path.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        try:
            e = json.loads(linha)
        except ValueError as exc:
            raise Recusa("EVENTOS_JSONL_ILEGIVEL: linha %d: %s" % (n + 1, exc))
        n += 1
        if e.get("anterior") != ant or e.get("hash") != _hash_evento(e):
            raise Recusa("EVENTOS_CADEIA_QUEBRADA: no evento seq %r (elo %d)" % (e.get("seq"), n))
        ant = e["hash"]
        if e.get("seq") in seqs:
            raise Recusa("EVENTO_SEQ_DUPLICADO: %r" % e.get("seq"))
        seqs.add(e.get("seq"))
        if e.get("seq") == seq:
            achado = e
    if achado is None:
        raise Recusa("EVENTO_NAO_ENCONTRADO: seq %d (cadeia integra ate o elo %d)" % (seq, n))
    e = achado
    if e.get("quem") != EVENTO_AUTOR:
        raise Recusa("EVENTO_NAO_E_DA_C1: seq %d por %r" % (seq, e.get("quem")))
    if e.get("tipo") != EVENTO_TIPO:
        raise Recusa("EVENTO_TIPO_INVALIDO: seq %d tipo %r (exigido %s)" % (seq, e.get("tipo"), EVENTO_TIPO))
    d = e.get("dados")
    if not isinstance(d, dict):
        raise Recusa("EVENTO_SEM_DADOS_JSON: seq %d" % seq)
    for t in _textos(d):
        m = RE_NEGACAO.search(t)
        if m:
            raise Recusa("EVENTO_COM_NEGACAO: seq %d contem %r -- um evento que nega nao autoriza" % (seq, m.group(0)))
    if d.get("versao") != versao:
        raise Recusa("EVENTO_NAO_NOMEIA_A_VERSAO: seq %d versao=%r alvo=%r" % (seq, d.get("versao"), versao))
    if d.get("acao") != "sincronizacao":
        raise Recusa("EVENTO_NAO_NOMEIA_A_SINCRONIZACAO: seq %d acao=%r" % (seq, d.get("acao")))
    if not isinstance(d.get("bancada"), str) or not mesmo_no(d["bancada"], bancada):
        raise Recusa("EVENTO_NAO_NOMEIA_ESTA_BANCADA: seq %d bancada=%r alvo=%s" % (seq, d.get("bancada"), bancada))
    for campo, chave in (("um_py", "um_py"), ("selo", "selo")):
        val = d.get(campo)
        esperado = nos_info[chave]["sha256"]
        if not isinstance(val, str) or len(val) < 16 or not esperado.startswith(val.lower()):
            raise Recusa("EVENTO_NAO_NOMEIA_O_PROGRAMA: seq %d %s=%r nao e prefixo (>=16 hex) de %s" % (seq, campo, val, esperado[:16]))
    if reparo and d.get("reparo") is not True:
        raise Recusa("EVENTO_NAO_AUTORIZA_REPARO: seq %d sem dados.reparo=true" % seq)
    return dict(evento=seq, verificado=True, quando=e.get("quando"), tipo=e.get("tipo"), hash=e.get("hash"), anterior=e.get("anterior"),
                cadeia_conferida_ate=n, fonte=str(eventos_path), fonte_e_o_quadro=mesmo_no(eventos_path, EVENTOS_QUADRO) if EVENTOS_QUADRO.exists() else False,
                dados=dict(versao=d.get("versao"), bancada=d.get("bancada"), um_py=d.get("um_py"), selo=d.get("selo"), reparo=d.get("reparo"),
                           gravacoes=d.get("gravacoes"), unidade=d.get("unidade")))


# ---------------------------------------------------------------- 3. o manifesto vigente e o estado do contrato
def estado_anterior(bancada, canonical_mod):
    bancada = Path(bancada)
    man_p = bancada / "canonical_contracts.json"
    if not man_p.is_file():
        raise Recusa("MANIFESTO_AUSENTE: " + str(man_p))
    raw = man_p.read_bytes()
    man = json.loads(raw)
    if man.get("schema") != 1:
        raise Recusa("CANONICAL_SCHEMA_UNSUPPORTED")
    estado, recibo = "OK", None
    try:
        reg = canonical_mod.CanonicalRegistry(bancada)
        recibo = reg.check("pre_sincronizacao")
    except canonical_mod.CanonicalError as exc:
        estado = str(exc).split(":")[0]
    return dict(path=str(man_p), bytes=len(raw), sha256=sha256(raw), deployment_id=man.get("deployment_id"),
                version=(man.get("canonical") or {}).get("version"),
                um_py_pinado=((man.get("canonical") or {}).get("script") or {}).get("sha256"),
                script_path_pinado=((man.get("canonical") or {}).get("script") or {}).get("path"),
                seal_path_pinado=((man.get("canonical") or {}).get("seal") or {}).get("path"),
                n_code=len(man.get("code") or []), n_sources=len(man.get("sources") or []),
                estado_do_contrato_instalado=estado,
                recibo=({k: recibo[k] for k in ("ok", "canonical_version", "um_py_sha256", "beta_tgl", "deployment_id")} if recibo else None),
                _man=man, _raw=raw)


def sonda_pos_selo_em_ram(bancada, canonical_mod, anterior, nos_info):
    """Quando o Nos alvo NAO mora no caminho pinado (so em --sandbox): prova em RAM que, se os bytes do caminho pinado fossem os do
    Nos alvo (o que o selo faz em producao), o canonical.py INSTALADO recusaria. Nada e escrito."""
    script_p = Path(anterior["script_path_pinado"]).resolve()
    seal_p = Path(anterior["seal_path_pinado"]).resolve()
    orig = Path.read_bytes

    def leitor(path):
        p = Path(path).resolve()
        if p == script_p:
            return nos_info["_raw"]
        if p == seal_p:
            return nos_info["_selo_raw"]
        return orig(path)
    with patch.object(Path, "read_bytes", leitor):
        try:
            canonical_mod.CanonicalRegistry(Path(bancada))
            return dict(recusou=False, codigo="ACEITO (inesperado)")
        except canonical_mod.CanonicalError as exc:
            return dict(recusou=True, codigo=str(exc).split(":")[0])


def conferir_recibo_pre_selo(rp, anterior, bancada, ja_sincronizada=False):
    """A6: o recibo pre-selo e conferido por identidade, nao so por fase e veredito: a versao alvo dele e a versao ANTERIOR da
    Bancada (a que estava canonica antes do selo), o um.py que ele leu e o um.py antes pinado, a Bancada e a mesma por identidade.
    Se a Bancada JA pina a versao alvo (re-execucao idempotente), a referencia e a geracao anterior registrada no bloco
    sincronizacao.anterior do manifesto vigente (o B(n) que a gravou); sem esse bloco, nao ha referencia e a conferencia recusa."""
    ref_versao, ref_um_py = anterior["version"], anterior["um_py_pinado"]
    if ja_sincronizada:
        ant = ((anterior["_man"].get("sincronizacao") or {}).get("anterior") or {})
        ref_versao, ref_um_py = ant.get("version"), ant.get("um_py_pinado")
        if not ref_versao or not ref_um_py:
            raise Recusa("RECIBO_PRE_SELO_SEM_REFERENCIA: a Bancada ja pina a versao alvo e o manifesto nao registra a geracao anterior")
    rp = Path(rp)
    if not rp.is_file():
        raise Recusa("RECIBO_PRE_SELO_AUSENTE: " + str(rp))
    raw = rp.read_bytes()
    rj = json.loads(raw)
    bat = rj.get("bateria_resultado") or {}
    if rj.get("fase") != "pre_selo" or bat.get("veredito") != "BATERIA_PASSA":
        raise Recusa("RECIBO_PRE_SELO_INVALIDO: fase=%r bateria=%r" % (rj.get("fase"), bat.get("veredito")))
    if not str(rj.get("veredito") or "").startswith("JA_SINCRONIZADA__ENSAIO"):
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: veredito=%r (exigido JA_SINCRONIZADA__ENSAIO...)" % rj.get("veredito"))
    if rj.get("versao_alvo") != ref_versao:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: versao_alvo=%r != versao anterior da Bancada %r" % (rj.get("versao_alvo"), ref_versao))
    um_sha = ((rj.get("nos") or {}).get("um_py") or {}).get("sha256")
    if um_sha != ref_um_py:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: um.py do recibo %s != um.py antes pinado %s" % (str(um_sha)[:16], str(ref_um_py)[:16]))
    rdir = (rj.get("bancada") or {}).get("dir")
    if not isinstance(rdir, str) or not mesmo_no(rdir, bancada):
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: bancada do recibo %r nao e esta Bancada por identidade" % rdir)
    ids = {t.get("id"): t.get("resultado") for t in bat.get("testes") or []}
    for tid in BATERIA_MINIMA:
        if ids.get(tid) != "PASSA":
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: %s=%r na bateria pre-selo (exigido PASSA)" % (tid, ids.get(tid)))
    return dict(path=str(rp), sha256=sha256(raw), bytes=len(raw), versao=rj.get("versao_alvo"), veredito=rj.get("veredito"),
                um_py_sha256=um_sha, bancada_dir=rdir, bateria=dict(n=bat.get("n"), passa=bat.get("passa"), falha=bat.get("falha")))


# ---------------------------------------------------------------- 4. o manifesto regenerado
def contrato_md(n, versao, nos_info, anterior, evento, stamp, recibo_pre_selo):
    return ("# Contrato de fidelidade da Bancada Um -- B%d / %s (sincronizacao)\n\n"
            "[REAL] Gerado por sincronizar_bancada.py %s em %s UTC, no passo B(%d) da cadeia de selo da %s, sob o evento c1 %s.\n\n"
            "## Identidade pinada\n\n"
            "- um.py %s: sha256 %s (%d B), linha de alpha %d (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = %s.\n"
            "- selo: sha256 %s.\n"
            "- manifesto anterior: %s (sha256 %s).\n"
            "- recibo pre-selo (testes finais contra a versao anterior): sha256 %s.\n\n"
            "## A regra\n\n"
            "Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que\n"
            "o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa\n"
            "sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao\n"
            "com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1\n"
            "nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;\n"
            "nenhum rito move o gate.\n"
            % (n, versao, REVISAO, stamp, n, versao, evento, versao, nos_info["um_py"]["sha256"], nos_info["um_py"]["bytes"], nos_info["alpha"]["linha"],
               nos_info["beta_runtime"], nos_info["selo"]["sha256"], anterior["deployment_id"], anterior["sha256"],
               (recibo_pre_selo or {}).get("sha256") or "(ausente: so em --sandbox)")).encode("utf-8")


def regenerar(bancada, anterior, nos_info, versao, evento, script_sha, bateria_sha, modo, forcar, stamp, recibo_pre_selo, reparo):
    bancada = Path(bancada)
    man = anterior["_man"]
    m = RE_GERACAO.match(str(man.get("deployment_id") or ""))
    if not m:
        raise Recusa("DEPLOYMENT_ID_SEM_GERACAO: %r" % man.get("deployment_id"))
    n = int(m.group(1)) + 1
    code, sources = [], []
    for e in man["code"]:
        p = relativo_seguro(e["path"], bancada)          # A10: code[].path nunca sai da Bancada
        if not p.is_file():
            raise Recusa("PIN_UNREADABLE: " + str(p))
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("CODE_DRIFT_NAO_E_SINCRONIZACAO: " + e["path"])
        code.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b)))
    for e in man["sources"]:
        p = Path(e["path"])
        p = p if p.is_absolute() else relativo_seguro(e["path"], bancada)
        if not p.is_file():
            raise Recusa("PIN_UNREADABLE: " + str(p))
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("SOURCE_DRIFT_NAO_E_SINCRONIZACAO: " + e["path"])
        sources.append(dict(e, bytes=len(b), sha256=sha256(b)))
    rotulo = "CONTRATO_CANONICO_B%d.md" % n
    if any(c["path"] == rotulo for c in code):
        raise Recusa("CONTRATO_B%d_JA_PINADO" % n)
    md = contrato_md(n, versao, nos_info, anterior, evento, stamp, recibo_pre_selo)
    code.append(dict(path=rotulo, bytes=len(md), sha256=sha256(md)))
    code.sort(key=lambda c: c["path"])
    novo = dict(schema=1,
                deployment_id="B%d-%s-%s-R1" % (n, versao, stamp[:8]),
                created_utc=agora(),
                canonical=dict(version=versao,
                               script=dict(path=nos_info["um_py"]["path"], bytes=nos_info["um_py"]["bytes"], sha256=nos_info["um_py"]["sha256"]),
                               seal=dict(path=nos_info["selo"]["path"], bytes=nos_info["selo"]["bytes"], sha256=nos_info["selo"]["sha256"])),
                code=code, sources=sources,
                contracts=dict(man.get("contracts") or {},
                               sync_policy="B(n) a cada versao selada por sincronizar_bancada.py: pino velho recusa (PIN_CHANGED); evento c1 nomeado e "
                                           "verificado pela cadeia de hash; bateria pinada antes de gravar; mesma versao com outro hash = SELO_PROGRAMA_DIVERGE; "
                                           "codigo e fontes so mudam por implantacao B com plano proprio"),
                sincronizacao=dict(passo="B%d" % n, versao=versao, modo=modo, forcada=bool(forcar), reparo_de_pino=bool(reparo), revisao_do_esboco=REVISAO,
                                   anterior=dict(deployment_id=anterior["deployment_id"], manifest_sha256=anterior["sha256"],
                                                 version=anterior["version"], um_py_pinado=anterior["um_py_pinado"],
                                                 estado_do_contrato_instalado=anterior["estado_do_contrato_instalado"]),
                                   evento_c1=evento, selo_sha256=nos_info["selo"]["sha256"], um_py_sha256=nos_info["um_py"]["sha256"],
                                   core_sha256=nos_info["core"]["sha256"], alpha_linha=nos_info["alpha"]["linha"],
                                   beta_runtime=nos_info["beta_runtime"], beta_core=nos_info["core"]["beta_core"],
                                   recibo_pre_selo_sha256=(recibo_pre_selo or {}).get("sha256"),   # A6: o hash do recibo pre-selo fica encadeado no manifesto
                                   gerado_por=dict(script_sha256=script_sha, bateria_sha256=bateria_sha), quando_utc=agora(),
                                   scope="IDENTITY_RE_PIN_ONLY; NOT_A_PHYSICAL_READING", gate_effect="NONE"))
    return novo, md, rotulo, n


# ---------------------------------------------------------------- 5. a copia de ensaio (staging) e a re-pinagem
def montar_staging(bancada, man, raiz, novo_manifesto_bytes=None, contrato=None):
    """Copia byte a byte (conferindo os pinos do manifesto dado) o codigo e as fontes RELATIVAS da Bancada para raiz/candidate.
    A10: todo destino e conferido dentro de candidate (sem '..', sem absoluto)."""
    bancada, cand = Path(bancada), Path(raiz) / "candidate"
    if cand.exists():
        raise Recusa("STAGING_JA_EXISTE: " + str(cand))
    cand.mkdir(parents=True)
    copias = []
    for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
        src = relativo_seguro(e["path"], bancada)
        dst = relativo_seguro(e["path"], cand)
        if contrato is not None and e["path"] == contrato[0]:
            b = contrato[1]
        else:
            b = src.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("PIN_CHANGED_AO_COPIAR: " + e["path"])
        if dst.exists():
            # o mesmo arquivo pode estar pinado em code E em sources (B2: fontes_externas/F5.2/10_frozen_neff_v1.py): duplicata so com bytes iguais
            if dst.read_bytes() != b:
                raise Recusa("DUPLICATA_COM_BYTES_DIFERENTES: " + e["path"])
            copias.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b), duplicata_de_pino=True))
            continue
        gravar_novo(dst, b)
        copias.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b)))
    (cand / "estado").mkdir(exist_ok=True)
    man_bytes = novo_manifesto_bytes if novo_manifesto_bytes is not None else (bancada / "canonical_contracts.json").read_bytes()
    gravar_novo(cand / "canonical_contracts.json", man_bytes)
    return cand, copias


def conferir_repinagem(canonical_mod, raiz_bancada, nos_info, versao, operacao):
    reg = canonical_mod.CanonicalRegistry(Path(raiz_bancada))
    rc = reg.check(operacao)
    falhas = []
    if not rc.get("ok"):
        falhas.append("ok=false")
    if rc.get("canonical_version") != versao:
        falhas.append("versao %r" % rc.get("canonical_version"))
    if rc.get("um_py_sha256") != nos_info["um_py"]["sha256"]:
        falhas.append("um.py sha")
    if rc.get("seal_sha256") != nos_info["selo"]["sha256"]:
        falhas.append("selo sha")
    if rc.get("beta_tgl") != nos_info["_beta"]:
        falhas.append("beta nao e bit a bit igual: %r vs %r" % (rc.get("beta_tgl"), nos_info["_beta"]))
    if falhas:
        raise Recusa("REPINAGEM_DIVERGE: " + "; ".join(falhas))
    return {k: rc[k] for k in ("ok", "canonical_version", "um_py_sha256", "seal_sha256", "canonical_manifest_sha256", "alpha", "beta_tgl",
                               "deployment_id", "mu_do_rito", "scope", "gate_effect")}


# ---------------------------------------------------------------- 6. a bateria (A1, A3, A7)
def sha_teste(t):
    """sha256 canonico de UM teste da bateria (JSON ordenado), para o pino por teste (A7)."""
    return sha256(json.dumps(t, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def carregar_bateria(bateria_p, bateria_sha_esperado, modo, fase, sandbox):
    """A7: a bateria e pinada pelo sha256 do arquivo (--bateria-sha256, lido pela cadeia de vNNN_pins) e pelo sha256 canonico de
    cada teste (testes_sha256); em aplicar o conjunto minimo e obrigatorio; cada teste (salvo o do kernel) tem fontes pinadas."""
    raw = bateria_p.read_bytes()
    sha_arq = sha256(raw)
    if modo == "aplicar":
        if not bateria_sha_esperado:
            raise Recusa("BATERIA_SHA_AUSENTE: em --modo aplicar a cadeia passa --bateria-sha256 (lido de vNNN_pins)")
    if bateria_sha_esperado and bateria_sha_esperado.lower() != sha_arq:
        raise Recusa("BATERIA_SHA_DIVERGE: arquivo %s != esperado %s" % (sha_arq[:16], str(bateria_sha_esperado)[:16]))
    try:
        bateria = json.loads(raw)
    except ValueError as exc:
        raise Recusa("BATERIA_ILEGIVEL: " + str(exc))
    testes = bateria.get("testes")
    if not isinstance(testes, list) or not testes:
        raise Recusa("BATERIA_SEM_TESTES")
    pinos = bateria.get("testes_sha256")
    if not isinstance(pinos, dict):
        raise Recusa("BATERIA_SEM_PINOS_POR_TESTE: a bateria R2 traz testes_sha256 {id: sha256 canonico}")
    ids = []
    for t in testes:
        tid = t.get("id")
        if not tid or tid in ids:
            raise Recusa("BATERIA_TESTE_SEM_ID_OU_DUPLICADO: %r" % tid)
        ids.append(tid)
        if pinos.get(tid) != sha_teste(t):
            raise Recusa("BATERIA_TESTE_SHA_DIVERGE: %s (%s != %s)" % (tid, sha_teste(t)[:16], str(pinos.get(tid))[:16]))
        if (t.get("verificacao") or {}).get("tipo") != "kernel_recibo" and not t.get("fontes"):
            raise Recusa("BATERIA_TESTE_SEM_FONTE_PINADA: " + tid)
        if any("{vinculo}" in str(x) for x in (t.get("comando") or [])) or "{vinculo}" in str(t.get("cwd", "")):
            raise Recusa("MARCADOR_VINCULO_PROIBIDO: %s executa da pasta do esboco, nao da fonte pinada (A3)" % tid)
    if set(pinos) != set(ids):
        raise Recusa("BATERIA_PINOS_NAO_CORRESPONDEM_AOS_TESTES")
    if modo == "aplicar":
        exigidos = set(BATERIA_MINIMA) | (set(BATERIA_MINIMA_POS_SELO) if fase == "pos_selo" else set())
        faltam = sorted(exigidos - set(ids))
        if faltam:
            raise Recusa("BATERIA_MINIMA_AUSENTE: em aplicar faltam %s" % ", ".join(faltam))
    return bateria, raw, sha_arq


def copiar_testes(bateria, raiz):
    raiz = Path(raiz)
    feitas = []
    for c in bateria.get("copias", []):
        b = Path(c["de"]).read_bytes()
        if len(b) != c["bytes"] or sha256(b) != c["sha256"]:
            raise Recusa("FONTE_DA_BATERIA_ALTERADA: " + c["de"])
        dst = relativo_seguro(c["para"], raiz)          # A10: copias[].para nunca sai da raiz
        gravar_novo(dst, b)
        feitas.append(dict(de=c["de"], para=str(dst), sha256=c["sha256"], bytes=c["bytes"]))
    return feitas


RE_FONTE = re.compile(r"\{fonte:(\d+)\}")


def _subst(x, ctx, fontes=None):
    if isinstance(x, str):
        if fontes is not None:
            def _f(m):
                i = int(m.group(1))
                if i >= len(fontes):
                    raise Recusa("MARCADOR_FONTE_FORA_DA_LISTA: {fonte:%d}" % i)
                return fontes[i]["path"]
            x = RE_FONTE.sub(_f, x)
        for k, v in ctx.items():
            x = x.replace("{" + k + "}", str(v))
        return x
    if isinstance(x, list):
        return [_subst(i, ctx, fontes) for i in x]
    if isinstance(x, dict):
        return {k: _subst(v, ctx, fontes) for k, v in x.items()}
    return x


VOLATEIS_PADRAO = {"started_utc", "finished_utc", "elapsed_seconds", "environment", "began_utc", "ended_utc", "seconds", "created_utc",
                   "python", "platform", "numpy", "path", "source_snapshot_before", "source_snapshot_after"}


def _strip(o, vol):
    if isinstance(o, dict):
        return {k: _strip(v, vol) for k, v in o.items() if k not in vol}
    if isinstance(o, list):
        return [_strip(x, vol) for x in o]
    return o


def _diff(a, b, path="", acc=None):
    acc = acc if acc is not None else {"max_abs": 0.0, "mismatch": []}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                acc["mismatch"].append(path + "." + k + " (missing)")
                continue
            _diff(a[k], b[k], path + "." + k, acc)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc["mismatch"].append(path + " (len)")
            return acc
        for i, (x, y) in enumerate(zip(a, b)):
            _diff(x, y, path + "[%d]" % i, acc)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        d = abs(float(a) - float(b))
        acc["max_abs"] = max(acc["max_abs"], d)
        if d != 0.0:
            acc["mismatch"].append(path + " (num %.3e)" % d)
    elif a != b:
        acc["mismatch"].append(path + " (value)")
    return acc


def verificar(ver, saida_texto, exit_code, ctx):
    """Devolve (passa, detalhe) para as verificacoes que dependem de um subprocesso."""
    t = ver.get("tipo", "exit0")
    if exit_code != 0:
        return False, "exit=%d" % exit_code
    if t == "exit0":
        return True, "exit 0"
    if t == "stdout_regex":
        ok = re.search(ver["regex"], saida_texto) is not None
        return ok, ("regex %r %s" % (ver["regex"], "casou" if ok else "NAO casou"))
    if t == "json_igual":
        p = Path(_subst(ver["arquivo"], ctx))
        if not p.is_file():
            return False, "arquivo ausente: " + str(p)
        d = json.loads(p.read_bytes())
        for campo, valor in ver["campos"].items():
            v = d
            for parte in campo.split("."):
                v = v.get(parte) if isinstance(v, dict) else None
            if v != valor:
                return False, "%s=%r esperado %r" % (campo, v, valor)
        return True, "campos conferem: " + ", ".join("%s=%r" % kv for kv in ver["campos"].items())
    if t == "comparar_json":
        novo, arq = Path(_subst(ver["novo"], ctx)), Path(_subst(ver["arquivado"], ctx))
        if not novo.is_file() or not arq.is_file():
            return False, "arquivo ausente para comparar"
        vol = set(ver.get("volateis") or VOLATEIS_PADRAO)
        d = _diff(_strip(json.loads(novo.read_bytes()), vol), _strip(json.loads(arq.read_bytes()), vol))
        ok = len(d["mismatch"]) == 0
        return ok, "max_abs=%.3e mismatch=%d %s" % (d["max_abs"], len(d["mismatch"]), d["mismatch"][:5])
    return False, "tipo de verificacao desconhecido: " + t


def verificar_kernel_recibo(kp, versao, nos_info):
    """A1: T17 e lido do recibo do build do kernel da etapa 2 da cadeia, por hash, SEM subprocesso. Campos exigidos: versao == alvo,
    rc == 0, sorry == 0, build_full_log_sha256 (64 hex); se o recibo nomeia o caminho do log (build_full_log), o log tem de existir
    e bater com o sha; se nomeia um um_py_sha256 ou o tgl_kernel_proof_manifest_sha256, tem de bater com o Nos lido."""
    kp = Path(kp)
    if not kp.is_file():
        return False, "recibo do kernel ausente: " + str(kp), None
    raw = kp.read_bytes()
    pino = dict(path=str(kp), sha256=sha256(raw), bytes=len(raw))
    try:
        k = json.loads(raw)
    except ValueError as exc:
        return False, "recibo do kernel ilegivel: %s" % exc, pino
    if not isinstance(k, dict):
        return False, "recibo do kernel nao e um objeto JSON", pino
    faltas = [c for c in ("versao", "rc", "sorry", "build_full_log_sha256") if c not in k]
    if faltas:
        return False, "recibo do kernel sem os campos %s" % faltas, pino
    if k.get("versao") != versao:
        return False, "recibo do kernel e da versao %r, alvo %r" % (k.get("versao"), versao), pino
    if k.get("rc") != 0 or isinstance(k.get("rc"), bool):
        return False, "recibo do kernel: rc=%r (exigido 0)" % k.get("rc"), pino
    if k.get("sorry") != 0 or isinstance(k.get("sorry"), bool):
        return False, "recibo do kernel: sorry=%r (exigido 0)" % k.get("sorry"), pino
    log_sha = str(k.get("build_full_log_sha256") or "").lower()
    if not RE_SHA256.match(log_sha):
        return False, "recibo do kernel: build_full_log_sha256 nao e sha256", pino
    if k.get("build_full_log"):
        lp = Path(k["build_full_log"])
        if not lp.is_file():
            return False, "recibo do kernel nomeia build_full_log ausente: %s" % lp, pino
        if sha256(lp.read_bytes()) != log_sha:
            return False, "recibo do kernel: o log em disco nao bate com build_full_log_sha256", pino
    if k.get("um_py_sha256") and str(k["um_py_sha256"]).lower() != nos_info["um_py"]["sha256"]:
        return False, "recibo do kernel nomeia outro um.py (%s)" % str(k["um_py_sha256"])[:16], pino
    if k.get("tgl_kernel_proof_manifest_sha256") and nos_info["selo"].get("tgl_kernel_proof_manifest_sha256") and \
            str(k["tgl_kernel_proof_manifest_sha256"]).lower() != nos_info["selo"]["tgl_kernel_proof_manifest_sha256"]:
        return False, "recibo do kernel nomeia outro tgl_kernel_proof_manifest.json que o selo", pino
    return True, "recibo do kernel %s: versao=%s rc=0 sorry=0 log=%s" % (pino["sha256"][:16], versao, log_sha[:16]), pino


def _arquivo_executado_e_pinado(arg, fontes_ok, candidate, copias_dst):
    """A3: todo .py que o comando executa ou passa como script tem de ser (a) uma fonte pinada deste teste (mesmo arquivo por
    identidade) ou (b) um arquivo da copia de ensaio (candidate, conferido pino a pino) ou uma copia conferida da bateria."""
    p = Path(arg)
    if not p.is_absolute():
        return None   # argumento relativo ao cwd do teste: so admitido se o cwd e a raiz e o arquivo e copia conferida
    try:
        pc = caminho_canonico(p)
    except Recusa:
        return False
    for f in fontes_ok:
        if mesmo_no(pc, f["path"]):
            return True
    if dentro_de(pc, candidate):
        return True
    for d in copias_dst:
        if mesmo_no(pc, d):
            return True
    return False


def rodar_bateria(bateria, ctx, recibos_dir, modo, fase="pos_selo", sandbox=False, recibo_pre_selo=None, nos_info=None, copias_feitas=()):
    recibos_dir = Path(recibos_dir)
    recibos_dir.mkdir(parents=True, exist_ok=True)
    copias_dst = [c["para"] for c in copias_feitas]
    resultados = []
    for t in bateria["testes"]:
        tid = t["id"]
        rec = dict(id=tid, teste=t.get("teste"), sha256_do_teste=sha_teste(t), fases=t.get("fases", ["pre_selo", "pos_selo"]),
                   obrigatorio_em=t.get("obrigatorio_em", ["ensaio", "aplicar"]), fontes=[], inicio=agora())
        if fase not in rec["fases"]:
            # o teste pertence a outra fase (ex.: os runners do atrator pinam o um.py ANTERIOR e so rodam antes do selo):
            # na fase pos_selo ele e lido do recibo da fase pre_selo, por hash, nunca refeito
            if fase == "pos_selo" and "pre_selo" in rec["fases"]:
                det = "nao pertence a fase pos_selo; o resultado vale pelo recibo pre-selo %s" % ((recibo_pre_selo or {}).get("sha256") or "(ausente)")
            else:
                det = "nao pertence a fase %s (fases: %s)" % (fase, rec["fases"])
            rec.update(resultado="NAO_EXECUTADO", detalhe=det, fim=agora())
            resultados.append(rec)
            continue
        # A3: as fontes PINADAS sao conferidas por sha256 ANTES de executar; o comando executa a fonte pinada, nunca uma copia local
        fontes_ok = True
        for f in t.get("fontes", []):
            p = Path(f["path"])
            if not p.is_absolute():
                rec["fontes"].append(dict(f, estado="NAO_ABSOLUTA"))
                fontes_ok = False
                continue
            if not p.is_file():
                rec["fontes"].append(dict(f, estado="AUSENTE"))
                fontes_ok = False
                continue
            b = p.read_bytes()
            est = "OK" if (len(b) == f["bytes"] and sha256(b) == f["sha256"]) else "ALTERADA"
            fontes_ok = fontes_ok and est == "OK"
            rec["fontes"].append(dict(f, estado=est))
        if not fontes_ok:
            rec.update(resultado="FALHA", detalhe="fonte pinada ausente, nao absoluta ou alterada", fim=agora())
            resultados.append(rec)
            continue
        ver = t.get("verificacao", {"tipo": "exit0"})
        if ver.get("tipo") == "kernel_recibo":
            # A1: sem subprocesso; o recibo do build e lido por hash e conferido campo a campo
            kp = ctx.get("kernel_recibo")
            if not kp:
                exig = (modo in rec["obrigatorio_em"]) and not sandbox
                rec.update(resultado=("FALHA" if exig else "NAO_EXECUTADO"),
                           detalhe="sem --kernel-recibo (T17 e lido do recibo do build do kernel da etapa 2 da cadeia)" + ("; tolerado so em --sandbox" if sandbox else ""), fim=agora())
            else:
                passa, detalhe, pino = verificar_kernel_recibo(kp, ctx["versao"], nos_info)
                rec.update(kernel_recibo=pino, resultado=("PASSA" if passa else "FALHA"), detalhe=detalhe, comando=None, fim=agora())
            resultados.append(rec)
            continue
        fontes_pin = t.get("fontes", [])
        cmd = _subst(t["comando"], ctx, fontes_pin)
        cwd = _subst(t.get("cwd", "{raiz}"), ctx, fontes_pin)
        rec["comando"], rec["cwd"] = cmd, cwd
        nao_pinados = []
        for i, arg in enumerate(cmd):
            if i == 0 or not str(arg).lower().endswith(".py"):
                continue
            ok = _arquivo_executado_e_pinado(arg, fontes_pin, ctx["candidate"], copias_dst)
            if ok is False or (ok is None and not any(mesmo_no(Path(cwd) / arg, d) for d in copias_dst)):
                nao_pinados.append(arg)
        if nao_pinados:
            rec.update(resultado="FALHA", detalhe="COMANDO_EXECUTA_ARQUIVO_NAO_PINADO: %s" % nao_pinados, fim=agora())
            resultados.append(rec)
            continue
        t0 = time.perf_counter()
        try:
            r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=float(t.get("timeout_s", 900)), env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8"))
            exit_code, out = r.returncode, (r.stdout or "") + "\n--- STDERR ---\n" + (r.stderr or "")
        except subprocess.TimeoutExpired as exc:
            exit_code, out = -1, "TIMEOUT apos %.0f s\n%s\n%s" % (float(t.get("timeout_s", 900)), exc.stdout or "", exc.stderr or "")
        except OSError as exc:
            exit_code, out = -2, "FALHA AO LANCAR: %s" % exc
        rec["segundos"] = round(time.perf_counter() - t0, 3)
        log = recibos_dir / (tid + ".log")
        gravar_novo(log, ("COMMAND: %r\nCWD: %s\nEXIT: %d\n%s" % (cmd, cwd, exit_code, out)).encode("utf-8"))
        rec["log"] = dict(path=str(log), sha256=sha256(log.read_bytes()), bytes=log.stat().st_size)
        rec["exit"] = exit_code
        passa, detalhe = verificar(ver, out, exit_code, ctx)
        rec["detalhe"] = detalhe
        rec["resultado"] = "PASSA" if passa else "FALHA"
        if GUARDA.search(out.replace("NOT_CONF" + "IRMED", "").replace("UNCONF" + "IRMED", "")):
            rec["resultado"], rec["detalhe"] = "FALHA", "palavra proibida na saida do teste; " + detalhe
        rec["fim"] = agora()
        resultados.append(rec)
    n_passa = sum(1 for r in resultados if r["resultado"] == "PASSA")
    n_falha = sum(1 for r in resultados if r["resultado"] == "FALHA")
    n_nexec = sum(1 for r in resultados if r["resultado"] == "NAO_EXECUTADO")
    return dict(n=len(resultados), passa=n_passa, falha=n_falha, nao_executado=n_nexec, testes=resultados,
                veredito=("BATERIA_PASSA" if n_falha == 0 else "BATERIA_FALHOU"))


# ---------------------------------------------------------------- 7. servico, aplicacao
def servico_responde(porta=PORTA_BANCADA):
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect(("127.0.0.1", porta))
        return True
    except OSError:
        return False
    finally:
        s.close()


def aplicar_na_bancada(bancada, canonical_mod, novo_bytes, contrato, nos_info, versao, n, stamp):
    bancada = Path(bancada)
    man_p = bancada / "canonical_contracts.json"
    antes = man_p.read_bytes()
    bak = man_p.with_name(man_p.name + ".bak_B%d_%s" % (n, stamp))
    if bak.exists():
        raise Recusa("BACKUP_JA_EXISTE: " + str(bak))
    with bak.open("xb") as f:
        f.write(antes)
    if bak.read_bytes() != antes:
        raise Recusa("BACKUP_DIVERGE")
    contrato_p = relativo_seguro(contrato[0], bancada)
    gravar_novo(contrato_p, contrato[1])
    tmp = man_p.with_name(man_p.name + ".tmp_B%d" % n)
    with tmp.open("xb") as f:
        f.write(novo_bytes)
        f.flush()
        os.fsync(f.fileno())
    if tmp.read_bytes() != novo_bytes:
        tmp.unlink()
        raise Recusa("ESCRITA_CURTA_DO_MANIFESTO")
    if man_p.read_bytes() != antes:
        tmp.unlink()
        raise Recusa("MANIFESTO_MUDOU_ENTRE_LEITURA_E_TROCA")
    os.replace(tmp, man_p)
    try:
        if man_p.read_bytes() != novo_bytes:
            raise Recusa("MANIFESTO_DIVERGE_APOS_TROCA")
        pos = conferir_repinagem(canonical_mod, bancada, nos_info, versao, "pos_sincronizacao")
    except Exception as exc:
        # rollback: o manifesto anterior volta byte a byte; o contrato novo sai
        tmp2 = man_p.with_name(man_p.name + ".tmp_rollback_B%d" % n)
        with tmp2.open("xb") as f:
            f.write(antes)
        os.replace(tmp2, man_p)
        if contrato_p.exists():
            contrato_p.unlink()
        raise Recusa("APLICACAO_REVERTIDA: " + str(exc))
    return dict(manifesto=str(man_p), backup=str(bak), backup_sha256=sha256(antes), contrato=str(contrato_p), pos_conferencia=pos)


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="o elo B(n): sincroniza a Bancada Um com o um.py selado (esboco funcional %s)" % REVISAO)
    ap.add_argument("--nos", default=str(NOS_PADRAO))
    ap.add_argument("--bancada", required=True)
    ap.add_argument("--versao", required=True)
    ap.add_argument("--saida", required=True, help="pasta nova desta sincronizacao (recibos, staging); so sob as raizes permitidas (A5)")
    ap.add_argument("--bateria", required=True, help="BATERIA_VINCULO.json (R2: com testes_sha256 e {fonte:N})")
    ap.add_argument("--bateria-sha256", default=None, help="sha256 esperado do BATERIA_VINCULO.json (obrigatorio em aplicar; lido de vNNN_pins) -- A7")
    ap.add_argument("--tunel", default=str(TUNEL_PADRAO))
    ap.add_argument("--modo", choices=("ensaio", "aplicar"), default="ensaio")
    ap.add_argument("--evento", default=None, help="seq do evento c1 (tipo SINCRONIZACAO_BANCADA) que nomeia a gravacao; em sandbox, SANDBOX:<texto>")
    ap.add_argument("--eventos", default=None, help="SO em --sandbox: um livro de eventos alternativo (copia) para ensaiar a verificacao pela cadeia de hash")
    ap.add_argument("--producao", action="store_true", help="obrigatorio quando --bancada e a Bancada de producao (por identidade)")
    ap.add_argument("--sandbox", action="store_true", help="permite Nos fora do caminho pinado e evento SANDBOX:*; recusado se o manifesto pina o Nos real")
    ap.add_argument("--kernel-recibo", default=None, help="recibo do build do kernel da etapa 2 (T17) -- A1")
    ap.add_argument("--fase", choices=("pre_selo", "pos_selo"), default="pos_selo",
                    help="pre_selo = os testes finais contra a versao ainda canonica (etapa 1 da cadeia); pos_selo = o elo B(n) depois do selo")
    ap.add_argument("--recibo-pre-selo", default=None, help="na fase pos_selo: o RECIBO_SINCRONIZACAO da fase pre_selo (conferido por identidade -- A6; obrigatorio fora do sandbox)")
    ap.add_argument("--forcar-regeracao", action="store_true", help="regenera mesmo se a Bancada ja pina a versao alvo")
    ap.add_argument("--reparo-de-pino", action="store_true", help="A8: so em aplicar, com evento c1 que traga dados.reparo=true: admite mesma versao com outro hash do um.py")
    ap.add_argument("--sem-bateria", action="store_true", help="SO para controles negativos: pula a bateria (nunca em aplicar)")
    a = ap.parse_args(argv)

    stamp = time.strftime("%Y%m%d_%H%M%S")

    def recusa_sem_recibo(motivo):
        # antes de --saida ser admitida nada pode ser gravado: a recusa e so impressa (fail-closed, rc 2)
        print(json.dumps(dict(veredito="RECUSADA", recusa=motivo, recibo=None, nota="recusa anterior a admissao de --saida: nada gravado"), ensure_ascii=False))
        return 2

    # 0. guardas de caminho (A2, A5) -- antes de qualquer gravacao
    try:
        bancada = caminho_canonico(a.bancada)
        saida = caminho_canonico(a.saida)
        nos_dir = caminho_canonico(a.nos)
        if not bancada.is_dir():
            raise Recusa("BANCADA_INEXISTENTE: " + str(bancada))
        # A5: as recusas especificas (producao, Nos, a propria Bancada) antes da generica (raizes permitidas), para que o motivo seja nomeado
        if PRODUCAO.exists() and dentro_de(saida, PRODUCAO):
            raise Recusa("SAIDA_NA_PRODUCAO: " + str(saida))
        if NOS_PADRAO.exists() and dentro_de(saida, NOS_PADRAO):
            raise Recusa("SAIDA_NO_NOS: " + str(saida))
        if dentro_de(saida, bancada):
            raise Recusa("SAIDA_DENTRO_DA_BANCADA: " + str(saida))
        if nos_dir.exists() and dentro_de(saida, nos_dir):
            raise Recusa("SAIDA_NO_NOS: " + str(saida))
        if not any(dentro_de(saida, r) for r in RAIZES_SAIDA if r.exists()):
            raise Recusa("SAIDA_FORA_DAS_RAIZES_PERMITIDAS: %s (permitidas: %s)" % (saida, "; ".join(str(r) for r in RAIZES_SAIDA)))
        producao = mesmo_no(bancada, PRODUCAO) if PRODUCAO.exists() else False
        if producao and not a.producao:
            raise Recusa("PRODUCAO_SEM_FLAG: --bancada e a Bancada de producao (por identidade); exige --producao")
        if producao and a.sandbox:
            raise Recusa("SANDBOX_NA_PRODUCAO")
        if a.eventos and not a.sandbox:
            raise Recusa("EVENTOS_ALTERNATIVO_FORA_DO_SANDBOX")
    except Recusa as exc:
        return recusa_sem_recibo(str(exc))
    except Exception as exc:
        return recusa_sem_recibo("ERRO_NAO_PREVISTO_NAS_GUARDAS: %s: %s" % (type(exc).__name__, exc))

    saida.mkdir(parents=True, exist_ok=True)
    script_sha = sha256(Path(__file__).read_bytes())
    bateria_p = caminho_canonico(a.bateria)
    recibo = dict(esboco="sincronizar_bancada.py %s -- NAO INSTALADO; desenho da gerencia c1; roda em sandbox contra uma copia" % REVISAO,
                  script_sha256=script_sha, bateria=dict(path=str(bateria_p), sha256=None, sha256_esperado=a.bateria_sha256, versao=None),
                  inicio_utc=agora(), stamp=stamp, modo=a.modo, sandbox=bool(a.sandbox), producao=producao, python_dont_write_bytecode=bool(sys.dont_write_bytecode),
                  fase=a.fase, recibo_pre_selo=None, reparo_de_pino=bool(a.reparo_de_pino),
                  versao_alvo=a.versao, bancada=dict(dir=str(bancada), forma_dada=a.bancada), nos=None, manifesto_anterior=None, manifesto_novo=None,
                  bateria_resultado=None, aplicacao=None, veredito=None,
                  escopo="IDENTIDADE_E_TESTES_SINTETICOS; NENHUMA_LEITURA_FISICA; NOT_FALSIFIED nao e creditacao", gate_effect="NONE")

    def fechar(veredito, codigo=0, recusa=None):
        recibo["veredito"] = veredito
        recibo["recusa"] = recusa
        recibo["fim_utc"] = agora()
        nome = ("RECIBO_SINCRONIZACAO_%s_%s.json" if recusa is None else "RECUSA_SINCRONIZACAO_%s_%s.json") % (a.versao, stamp)
        p = gravar_novo(saida / nome, json_bytes(recibo))
        print(json.dumps(dict(veredito=veredito, recusa=recusa, recibo=str(p), recibo_sha256=sha256(p.read_bytes())), ensure_ascii=False))
        return codigo

    try:
        if producao and a.modo == "aplicar" and servico_responde():
            raise Recusa("SERVICO_NO_AR: quiesce e pare o um_bancada.py (ato com recibo) antes de aplicar; o manifesto em RAM nao recarrega")
        if a.modo == "aplicar" and a.sem_bateria:
            raise Recusa("APLICAR_SEM_BATERIA_PROIBIDO")
        if a.reparo_de_pino and a.modo != "aplicar":
            raise Recusa("REPARO_SO_EM_APLICAR: --reparo-de-pino exige --modo aplicar e evento c1 com dados.reparo=true")
        if a.modo == "aplicar" and a.fase != "pos_selo" and not a.reparo_de_pino:
            raise Recusa("APLICAR_SO_NA_FASE_POS_SELO: o elo B(n) grava depois do selo; antes dele so ensaio (salvo --reparo-de-pino nomeado em evento)")
        if a.fase == "pos_selo" and not a.recibo_pre_selo and a.modo == "aplicar" and not a.sandbox:
            raise Recusa("RECIBO_PRE_SELO_AUSENTE: o elo B(n) exige o recibo dos testes finais da fase pre_selo")
        if a.fase == "pre_selo" and a.recibo_pre_selo:
            raise Recusa("RECIBO_PRE_SELO_NA_FASE_PRE_SELO")
        # a bateria (A7): pinada antes de qualquer outra leitura
        bateria, bateria_raw, bateria_sha = carregar_bateria(bateria_p, a.bateria_sha256, a.modo, a.fase, a.sandbox)
        recibo["bateria"].update(sha256=bateria_sha, versao=bateria.get("versao_bateria"), n_testes=len(bateria["testes"]))
        # 1. o selo e o um.py (A11)
        nos_info = ler_nos(nos_dir, a.versao)
        recibo["nos"] = {k: v for k, v in nos_info.items() if not k.startswith("_")}
        # 2. o evento c1 (A4) -- em aplicar, verificado pela cadeia de hash; em ensaio, so anotado
        if a.modo == "aplicar":
            evento = verificar_evento(a.evento, a.versao, bancada, a.sandbox, nos_info, a.reparo_de_pino, a.eventos)
        else:
            evento = dict(evento=a.evento, verificado=False, nota="ensaio: nenhuma gravacao na Bancada") if a.evento else None
        recibo["evento_c1"] = evento
        # 3. o manifesto vigente (A2, A6, A8)
        canonical_mod, canonical_pin = carregar_canonical(bancada)
        recibo["bancada"]["canonical_py_instalado"] = canonical_pin
        anterior = estado_anterior(bancada, canonical_mod)
        recibo["manifesto_anterior"] = {k: v for k, v in anterior.items() if not k.startswith("_")}
        if not anterior["script_path_pinado"] or not anterior["seal_path_pinado"]:
            raise Recusa("MANIFESTO_SEM_PINO_DO_NOS")
        pina_nos_real = NOS_PADRAO.exists() and mesmo_no(Path(anterior["script_path_pinado"]).parent, NOS_PADRAO)
        recibo["manifesto_anterior"]["pina_o_nos_real"] = pina_nos_real
        if a.sandbox and pina_nos_real:
            raise Recusa("SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL: o sandbox so existe para copia cujo manifesto pina um Nos de ensaio")
        nos_pinado = mesmo_no(anterior["script_path_pinado"], nos_info["um_py"]["path"]) and mesmo_no(anterior["seal_path_pinado"], nos_info["selo"]["path"])
        recibo["manifesto_anterior"]["nos_alvo_e_o_pinado"] = nos_pinado
        if not nos_pinado and not a.sandbox:
            raise Recusa("NOS_DIFERENTE_DO_PINADO: o manifesto pina %s; o alvo e %s (so em --sandbox)" % (anterior["script_path_pinado"], nos_info["um_py"]["path"]))
        if anterior["estado_do_contrato_instalado"] not in ("OK",) + ESPERADOS_POS_SELO:
            raise Recusa("BANCADA_EM_ESTADO_DESCONHECIDO: " + anterior["estado_do_contrato_instalado"])
        # A8: a mesma versao com outro hash do um.py nao e sincronizacao -- e divergencia de selo/programa (ou corrupcao do manifesto)
        if anterior["version"] == a.versao and anterior["um_py_pinado"] != nos_info["um_py"]["sha256"]:
            if not a.reparo_de_pino:
                raise Recusa("SELO_PROGRAMA_DIVERGE: a Bancada pina %s %s e o Nos tem %s %s com a MESMA versao; nunca atualizar so o hash "
                             "(so --reparo-de-pino em aplicar com evento c1 dados.reparo=true)"
                             % (anterior["version"], str(anterior["um_py_pinado"])[:16], a.versao, nos_info["um_py"]["sha256"][:16]))
            recibo["reparo_de_pino_autorizado_por"] = (evento or {}).get("evento")
        ja_sincronizada = (anterior["estado_do_contrato_instalado"] == "OK" and anterior["version"] == a.versao
                           and anterior["um_py_pinado"] == nos_info["um_py"]["sha256"] and nos_pinado)
        if a.recibo_pre_selo:                             # A6
            recibo["recibo_pre_selo"] = conferir_recibo_pre_selo(a.recibo_pre_selo, anterior, bancada, ja_sincronizada)
        if not nos_pinado:
            recibo["sonda_pos_selo_em_ram"] = sonda_pos_selo_em_ram(bancada, canonical_mod, anterior, nos_info)
            if not recibo["sonda_pos_selo_em_ram"]["recusou"] or recibo["sonda_pos_selo_em_ram"]["codigo"] not in ESPERADOS_POS_SELO:
                raise Recusa("CANONICAL_INSTALADO_NAO_RECUSOU_PINO_VELHO: " + str(recibo["sonda_pos_selo_em_ram"]))
        elif anterior["estado_do_contrato_instalado"] in ESPERADOS_POS_SELO:
            recibo["pino_velho_recusado_pelo_instalado"] = anterior["estado_do_contrato_instalado"]
        # 4. regenerar (ou nao)
        raiz = saida / "raiz"
        if ja_sincronizada and not a.forcar_regeracao:
            recibo["manifesto_novo"] = None
            cand, copias = montar_staging(bancada, anterior["_man"], raiz)
            recibo["staging"] = dict(candidate=str(cand), n_copias=len(copias), manifesto="o vigente (ja sincronizada)")
            recibo["repinagem"] = conferir_repinagem(canonical_mod, cand, nos_info, a.versao, "ensaio_ja_sincronizada")
            veredito_base = "JA_SINCRONIZADA"
            novo_bytes = contrato = n = None
        else:
            novo, md, rotulo, n = regenerar(bancada, anterior, nos_info, a.versao, (evento or {}).get("evento"), script_sha, bateria_sha, a.modo,
                                            a.forcar_regeracao, stamp, recibo.get("recibo_pre_selo"), a.reparo_de_pino)
            novo_bytes = json_bytes(novo)
            contrato = (rotulo, md)
            gravar_novo(saida / ("MANIFESTO_CANDIDATO_B%d.json" % n), novo_bytes)
            gravar_novo(saida / rotulo, md)
            recibo["manifesto_novo"] = dict(deployment_id=novo["deployment_id"], sha256=sha256(novo_bytes), bytes=len(novo_bytes), n_code=len(novo["code"]),
                                            n_sources=len(novo["sources"]), contrato=rotulo, contrato_sha256=sha256(md), candidato=str(saida / ("MANIFESTO_CANDIDATO_B%d.json" % n)),
                                            recibo_pre_selo_sha256_encadeado=novo["sincronizacao"]["recibo_pre_selo_sha256"])
            cand, copias = montar_staging(bancada, novo, raiz, novo_bytes, contrato)
            recibo["staging"] = dict(candidate=str(cand), n_copias=len(copias), manifesto="o regenerado B%d" % n)
            recibo["repinagem"] = conferir_repinagem(canonical_mod, cand, nos_info, a.versao, "ensaio_repinagem_B%d" % n)
            veredito_base = "REPINADA_B%d" % n
        # 6. a bateria (contra a copia; A1, A3)
        if a.sem_bateria:
            recibo["bateria_resultado"] = dict(veredito="BATERIA_PULADA_SO_CONTROLE_NEGATIVO")
        else:
            copias_feitas = copiar_testes(bateria, raiz)
            recibo["copias_de_testes"] = copias_feitas
            ctx = dict(py=sys.executable, raiz=str(raiz), candidate=str(cand), nos=str(nos_dir), versao=a.versao,
                       recibos=str(saida / "recibos"), tunel=str(caminho_canonico(a.tunel)), saida=str(saida), rotulo="V" + stamp, kernel_recibo=a.kernel_recibo or "")
            recibo["bateria_resultado"] = rodar_bateria(bateria, ctx, saida / "recibos", a.modo, a.fase, a.sandbox, recibo.get("recibo_pre_selo"), nos_info, copias_feitas)
            if recibo["bateria_resultado"]["veredito"] != "BATERIA_PASSA":
                return fechar(veredito_base + "__BATERIA_FALHOU__NADA_GRAVADO_NA_BANCADA", 3)
            if a.modo == "aplicar":
                # em aplicar nenhum teste obrigatorio pode ficar por executar (salvo os de outra fase, lidos por hash do recibo pre-selo)
                pendentes = [r["id"] for r in recibo["bateria_resultado"]["testes"]
                             if r["resultado"] == "NAO_EXECUTADO" and a.modo in r["obrigatorio_em"] and a.fase in r["fases"]]
                if pendentes and not a.sandbox:
                    return fechar(veredito_base + "__BATERIA_INCOMPLETA__NADA_GRAVADO_NA_BANCADA: %s" % pendentes, 3)
                recibo["bateria_resultado"]["nao_executados_tolerados_em_sandbox"] = pendentes
        # 7. aplicar (so com evento verificado e bateria passada)
        if a.modo == "aplicar":
            if novo_bytes is None:
                recibo["aplicacao"] = dict(nota="ja sincronizada: nada a gravar")
                return fechar(veredito_base + "__NADA_A_GRAVAR", 0)
            recibo["aplicacao"] = aplicar_na_bancada(bancada, canonical_mod, novo_bytes, contrato, nos_info, a.versao, n, stamp)
            est = bancada / "estado" / "sincronizacao"
            est.mkdir(parents=True, exist_ok=True)
            recibo["aplicacao"]["copia_do_recibo"] = str(est / ("RECIBO_SINCRONIZACAO_%s_%s.json" % (a.versao, stamp)))
            recibo["veredito"] = veredito_base + "__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO"
            recibo["fim_utc"] = agora()
            gravar_novo(est / ("RECIBO_SINCRONIZACAO_%s_%s.json" % (a.versao, stamp)), json_bytes(recibo))
            return fechar(recibo["veredito"], 0)
        return fechar(veredito_base + "__ENSAIO__NADA_GRAVADO_NA_BANCADA", 0)
    except Recusa as exc:
        return fechar("RECUSADA", 2, str(exc))
    except Exception as exc:   # qualquer erro nao previsto tambem e recusa visivel, com recibo -- nunca traceback mudo nem "ok" falso
        return fechar("RECUSADA", 2, "ERRO_NAO_PREVISTO: %s: %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(main())
