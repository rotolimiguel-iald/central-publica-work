"""
═══════════════════════════════════════════════════════════════════════════════
    IALD — MOTORES DE INFERÊNCIA (14/09/2026)

    ORDEM DO OPERADOR (verbatim, 14/09/2026): *"eu quero o modelo mais barato, a função
    não é competir, é apenas poder servir sem ser o meu servidor. e eu posso ter o modelo
    melhor só pra mim, mas pra todos os demais que eu liberar acesso no app da IALD
    usariam o modelo mais barato que a openai servir"*

    DOIS MOTORES:
      nativa — o llama-server local (:8081), a IALD Nativa. Sem custo por token; ocupa
               a máquina do operador.
      openai — a API da OpenAI (Chat Completions). Padrão `gpt-5-nano`, o mais barato da
               página oficial lida em 14/09/2026: US$ 0,05 entrada · 0,005 entrada em
               cache · 0,40 saída, por 1M tokens; 400k de janela; streaming e funções.

    QUEM USA QUAL (nesta ordem):
      0. conta do plano `gratuito` → SEMPRE openai (14/09/2026 noite; vence até o motor
         fixado, porque a porta aberta nunca pode cair na máquina do operador);
      1. o campo `motor` da conta em iald_users.json, quando o operador o fixa no painel;
      2. conta de administrador → IALD_MOTOR_OPERADOR (padrão: nativa);
      3. todas as demais       → IALD_MOTOR_PADRAO   (padrão: nativa). Nada muda
         sozinho: o operador põe a chave no .env e troca para `openai` quando quiser.

    AS TRAVAS DO MOTOR EXTERNO (todas fail-closed):
      - sem chave, sem prompt canônico, sem preço do modelo ou sem consentimento da
        pessoa → recusa visível, nunca desvio silencioso para a máquina do operador
        (só se ele ligar IALD_OPENAI_RESERVA_NATIVA=1);
      - o prompt de sistema é o do SERVIDOR (o da loja, o mesmo texto que já viaja
        dentro do app). O que o cliente mandar como system é descartado, menos o bloco
        USER CONTEXT (o perfil que a própria pessoa preencheu, rotulado como dado) e a
        instrução da lupa. Sem isso a chave paga viraria um GPT genérico;
      - a memória do operador NUNCA vai ao motor externo (o servidor desvia antes de
        injetá-la);
      - ferramentas: só as de IALD_OPENAI_FERRAMENTAS (padrão: data/hora, busca na
        internet, leitura de página — nada que leia o acervo, a máquina ou o razão);
      - teto de gasto diário em dólar por conta e global, contado pelo `usage` exato que
        a OpenAI devolve no fim do stream; pedidos por minuto por conta;
      - `store: false` e `safety_identifier` = HMAC da conta (nunca o nome nem o e-mail).

    A PORTA ABERTA — ORDEM DO OPERADOR (verbatim, 14/09/2026 noite): *"eu quero que cada
    usuário ao entrar e baixar o app que agora vamos liberar pra todo mundo esteja conectado
    a essa versão do chatgpt com um limite bem baixo de tokens que ele pode gastar de forma
    gratuita."* Substitui a ordem da manhã ("só eu libero o acesso"): conta nova entra
    sozinha no plano gratuito; o operador continua podendo bloquear e excluir.

    PLANOS (aditivo — sem os argumentos novos, tudo funciona exatamente como antes):
      gratuito  — conta da porta aberta (o servidor ESCREVE `plano: "gratuito"`). Motor
                  openai sempre; cota em tokens por dia e por mês, teto em dólar por conta
                  e teto global próprio (os gratuitos não esgotam assinantes nem o operador).
      assinante — conta sem o campo `plano` e sem admin: os limites de hoje (não regressivo
                  para quem o operador liberou pessoalmente).
      operador  — conta de administrador sem o campo `plano`.
    TOKEN CONTADO = saída (com o raciocínio) + entrada fora do cache, sem cobrar da pessoa o
    prefixo fixo do servidor: completion + max(0, prompt − max(cached, prefixo)).
    MODELOS QUE DESLIGAM: gpt-5-nano e gpt-5-mini desligam em 11/12/2026 [REAL — página de
    desligamentos da OpenAI lida em 14/09/2026]; com IALD_OPENAI_SUCESSOR_AUTOMATICO=1
    (padrão) o sucessor indicado entra sozinho no dia, sem reiniciar nada.
    MODERAÇÃO: o endpoint /moderations é gratuito [REAL]; bloqueia poucas categorias graves e
    troca a resposta por acolhimento (CVV 188) nas de autolesão. Quem decide é o servidor.

    Este módulo não importa Flask; a rede entra por uma função injetada.
═══════════════════════════════════════════════════════════════════════════════
"""

import hashlib
import hmac
import json
import math
import os
import queue
import re
import threading
import time
from collections import deque
from datetime import datetime, timedelta, timezone

NATIVA, OPENAI = "nativa", "openai"
MOTORES = (NATIVA, OPENAI)
MODELO_MAIS_BARATO = "gpt-5-nano"

GRATUITO, ASSINANTE, OPERADOR = "gratuito", "assinante", "operador"
PLANOS = (GRATUITO, ASSINANTE, OPERADOR)

# US$ por 1M tokens: (entrada, entrada em cache, saída) ou (…, escrita no cache). [KNOWN] —
# páginas oficiais dos modelos lidas em 14/09/2026. Modelo fora desta tabela precisa de
# IALD_OPENAI_PRECOS; sem preço não há teto de gasto, e sem teto o motor não liga.
PRECOS_CONHECIDOS = {
    "gpt-5-nano": (0.05, 0.005, 0.40),
    # [REAL — página do modelo lida em 14/09/2026: "Cache writes are billed at 1.25x the
    # uncached input token rate"] → escrita no cache = 0,25.
    "gpt-5.6-luna": (0.20, 0.02, 1.20, 0.25),
}
ESFORCOS_VALIDOS = ("none", "minimal", "low", "medium", "high", "xhigh", "max")
# Os níveis que cada modelo aceita, do mais baixo ao mais alto. gpt-5-nano [KNOWN];
# gpt-5.6-luna [REAL — página do modelo lida em 14/09/2026]. Modelo fora daqui: sem ajuste.
ESFORCOS_POR_MODELO = {
    "gpt-5-nano": ("minimal", "low", "medium", "high"),
    "gpt-5.6-luna": ("none", "low", "medium", "high", "xhigh", "max"),
}
# modelo → (data do desligamento em UTC, sucessor indicado). [REAL —
# developers.openai.com/api/docs/deprecations lido em 14/09/2026]
DESLIGAMENTOS = {
    "gpt-5-nano": ("2026-12-11", "gpt-5.6-luna"),
    "gpt-5-nano-2025-08-07": ("2026-12-11", "gpt-5.6-luna"),
    "gpt-5-mini": ("2026-12-11", "gpt-5.6-terra"),
    "gpt-5-mini-2025-08-07": ("2026-12-11", "gpt-5.6-terra"),
}
FERRAMENTAS_PADRAO = ("get_current_datetime", "search_web", "fetch_url")
VERSAO_CONSENTIMENTO = 1
CPT = 2.91                      # chars por token, a calibração da casa
TOKENS_POR_IMAGEM = 800         # estimativa conservadora para o orçamento da janela
TETO_CONTEXTO_USUARIO = 2400    # chars do perfil que a pessoa preencheu

TEXTO_CONSENTIMENTO = (
    "Para responder a você, esta conta da IALD usa um serviço de inteligência artificial "
    "de terceiros: a API da OpenAI (OpenAI, L.L.C., Estados Unidos).\n\n"
    "O que é enviado à OpenAI a cada mensagem: o texto que você escreve, o histórico "
    "recente desta conversa, o conteúdo dos arquivos e imagens que você anexar e as "
    "informações de perfil que você preencher nas configurações (nome, área, interesses, "
    "contexto). Não são enviados a sua senha, o seu e-mail nem a sua identidade Apple ou "
    "Google; a OpenAI recebe só um código derivado da sua conta, usado para prevenir "
    "abuso.\n\n"
    "Para que serve: só para gerar as respostas da IALD. Segundo a OpenAI, os dados "
    "enviados pela API não são usados para treinar os modelos dela e ficam em registros "
    "de monitoramento de abuso por até 30 dias. A IALD pede que as conversas não sejam "
    "armazenadas (store: false).\n\n"
    "Você pode recusar agora e revogar depois nas configurações. Sem este consentimento "
    "a conta não recebe respostas, porque o motor dela é o da OpenAI."
)

MARCA_CONTEXTO = "\n\nUSER CONTEXT:\n"
MARCA_LUPA = 'INSTRUÇÃO DESTA MENSAGEM: o usuário tocou em "buscar na internet".'
LUPA_CANONICA = (MARCA_LUPA + " Use a ferramenta search_web antes de responder e cite as "
                 "fontes encontradas.")


# ══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ══════════════════════════════════════════════════════════════
CAMPOS_DO_PLANO = ("tokens_dia", "tokens_mes", "usd_dia", "max_saida", "agente", "pensar")


def planos_padrao():
    """Os limites de cada plano quando nada foi configurado (um dict novo a cada chamada).

    `usd_dia` None = o teto em dólar de hoje, lido NA HORA da checagem:
    cfg.cota_usuario_usd (assinante, e gratuito se alguém o zerar para None) ou
    cfg.cota_operador_usd (operador).
    """
    return {
        GRATUITO: {"tokens_dia": 8000, "tokens_mes": 60000, "usd_dia": 0.02,
                   "max_saida": 1200, "agente": False, "pensar": False},
        ASSINANTE: {"tokens_dia": 60000, "tokens_mes": 900000, "usd_dia": None,
                    "max_saida": 4096, "agente": True, "pensar": True},
        OPERADOR: {"tokens_dia": 2000000, "tokens_mes": 30000000, "usd_dia": None,
                   "max_saida": 8192, "agente": True, "pensar": True},
    }


def _planos_completos(dados):
    """Padrão por baixo; o que foi passado (plano e campo conhecidos) por cima."""
    completos = planos_padrao()
    if isinstance(dados, dict):
        for plano, campos in dados.items():
            if plano in completos and isinstance(campos, dict):
                completos[plano].update({k: v for k, v in campos.items() if k in CAMPOS_DO_PLANO})
    return completos


class Config:
    """Configuração do motor externo. O repr nunca mostra a chave."""

    def __init__(self, **campos):
        self.chave = ""
        self.url_base = "https://api.openai.com/v1"
        self.modelo = MODELO_MAIS_BARATO
        self.modelo_operador = MODELO_MAIS_BARATO
        self.motor_padrao = NATIVA
        self.motor_operador = NATIVA
        self.esforco_rapido = "minimal"
        self.esforco_pensar = "low"
        self.max_saida = 4096
        self.max_saida_pensar = 8192
        self.janela = 32768
        self.cota_usuario_usd = 0.20
        self.cota_operador_usd = 1.00
        self.cota_global_usd = 5.00
        self.pedidos_por_minuto = 12
        self.ferramentas = frozenset(FERRAMENTAS_PADRAO)
        self.reserva_nativa = False
        self.timeout = 120.0
        self.precos_tabela = dict(PRECOS_CONHECIDOS)
        self.planos = None
        self.cota_global_gratuito_usd = 2.00
        self.sucessor_automatico = True
        self.avisos = []
        self._esforco_recusado = set()
        for k, v in campos.items():
            if not hasattr(self, k):
                raise TypeError(f"campo desconhecido: {k}")
            setattr(self, k, v)
        # depois dos campos: sem `planos`, o padrão; com `planos` parcial, o padrão completa
        self.planos = _planos_completos(self.planos)

    def __repr__(self):
        return (f"Config(motor_padrao={self.motor_padrao!r}, motor_operador={self.motor_operador!r}, "
                f"modelo={self.modelo!r}, chave={'definida' if self.chave else 'ausente'})")

    def precos(self, modelo):
        return self.precos_tabela.get(modelo)

    def esforco_recusado(self, modelo):
        return modelo in self._esforco_recusado

    def marcar_esforco_recusado(self, modelo):
        self._esforco_recusado.add(modelo)


def _ler_precos(bruto, avisos):
    """`modelo=entrada/cache/saida[/escrita_cache];modelo2=...` (US$ por 1M tokens)."""
    tabela = {}
    for item in (bruto or "").split(";"):
        item = item.strip()
        if not item:
            continue
        nome, _, valores = item.partition("=")
        partes = valores.split("/")
        try:
            if len(partes) not in (3, 4):
                raise ValueError
            valores = tuple(float(p.strip().replace(",", ".")) for p in partes)
            if any(not math.isfinite(v) or v < 0 for v in valores):
                raise ValueError      # preço NaN/negativo abriria o teto de gasto
            tabela[nome.strip()] = valores
        except ValueError:
            avisos.append(f"IALD_OPENAI_PRECOS: item inválido {item!r} (ignorado)")
    return tabela


def carregar_config(ler):
    """`ler(nome)` devolve o valor da variável (ambiente ou .env) ou ''."""
    avisos = []

    def texto(nome, padrao=""):
        v = (ler(nome) or "").strip()
        return v or padrao

    def numero(nome, padrao, tipo, minimo):
        bruto = texto(nome)
        if not bruto:
            return padrao
        mostrar = "o padrão" if padrao is None else padrao
        try:
            v = tipo(bruto.replace(",", ".")) if tipo is float else tipo(bruto)
            if tipo is float and math.isnan(v):
                raise ValueError      # NaN nunca é >= a nada: um teto NaN nunca bloquearia
        except ValueError:
            avisos.append(f"{nome} inválido ({bruto!r}); usando {mostrar}")
            return padrao
        if v < minimo:
            avisos.append(f"{nome} abaixo do mínimo {minimo}; usando {mostrar}")
            return padrao
        return v

    def chave_liga(nome, padrao):
        bruto = texto(nome)
        if not bruto:
            return padrao
        if bruto in ("0", "1"):
            return bruto == "1"
        avisos.append(f"{nome} inválido ({bruto!r}); use 0 ou 1; usando {int(padrao)}")
        return padrao

    def motor(nome):
        v = texto(nome, NATIVA).lower()
        if v not in MOTORES:
            avisos.append(f"{nome} desconhecido ({v!r}); usando {NATIVA}")
            return NATIVA
        return v

    def esforco(nome, padrao):
        v = texto(nome, padrao).lower()
        if v in ("omitir", "-"):
            return ""
        if v not in ESFORCOS_VALIDOS:
            avisos.append(f"{nome} inválido ({v!r}); usando {padrao}")
            return padrao
        return v

    modelo = texto("IALD_OPENAI_MODELO", MODELO_MAIS_BARATO)
    tabela = dict(PRECOS_CONHECIDOS)
    tabela.update(_ler_precos(texto("IALD_OPENAI_PRECOS"), avisos))
    nomes = texto("IALD_OPENAI_FERRAMENTAS", ",".join(FERRAMENTAS_PADRAO))
    ferramentas = frozenset(n.strip() for n in nomes.split(",") if n.strip() and n.strip() != "nenhuma")

    # IALD_PLANO_<GRATUITO|ASSINANTE|OPERADOR>_<TOKENS_DIA|TOKENS_MES|USD_DIA|MAX_SAIDA|AGENTE|PENSAR>
    # Vazio = padrão; inválido = padrão com aviso; 0 nas cotas = ninguém daquele plano gasta.
    planos = {}
    for plano, base in planos_padrao().items():
        pre = f"IALD_PLANO_{plano.upper()}_"
        planos[plano] = {
            "tokens_dia": numero(pre + "TOKENS_DIA", base["tokens_dia"], int, 0),
            "tokens_mes": numero(pre + "TOKENS_MES", base["tokens_mes"], int, 0),
            "usd_dia": numero(pre + "USD_DIA", base["usd_dia"], float, 0.0),
            "max_saida": numero(pre + "MAX_SAIDA", base["max_saida"], int, 256),
            "agente": chave_liga(pre + "AGENTE", base["agente"]),
            "pensar": chave_liga(pre + "PENSAR", base["pensar"]),
        }

    cfg = Config(
        chave=texto("IALD_OPENAI_API_KEY"),
        url_base=texto("IALD_OPENAI_URL", "https://api.openai.com/v1").rstrip("/"),
        modelo=modelo,
        modelo_operador=texto("IALD_OPENAI_MODELO_OPERADOR", modelo),
        motor_padrao=motor("IALD_MOTOR_PADRAO"),
        motor_operador=motor("IALD_MOTOR_OPERADOR"),
        esforco_rapido=esforco("IALD_OPENAI_ESFORCO", "minimal"),
        esforco_pensar=esforco("IALD_OPENAI_ESFORCO_PENSAR", "low"),
        max_saida=numero("IALD_OPENAI_MAX_SAIDA", 4096, int, 256),
        max_saida_pensar=numero("IALD_OPENAI_MAX_SAIDA_PENSAR", 8192, int, 256),
        janela=numero("IALD_OPENAI_JANELA", 32768, int, 16384),
        cota_usuario_usd=numero("IALD_OPENAI_COTA_USUARIO_USD_DIA", 0.20, float, 0.0),
        cota_operador_usd=numero("IALD_OPENAI_COTA_OPERADOR_USD_DIA", 1.00, float, 0.0),
        cota_global_usd=numero("IALD_OPENAI_COTA_GLOBAL_USD_DIA", 5.00, float, 0.0),
        pedidos_por_minuto=numero("IALD_OPENAI_PEDIDOS_POR_MINUTO", 12, int, 1),
        ferramentas=ferramentas,
        reserva_nativa=texto("IALD_OPENAI_RESERVA_NATIVA", "0") == "1",
        timeout=numero("IALD_OPENAI_TIMEOUT_S", 120.0, float, 5.0),
        precos_tabela=tabela,
        planos=planos,
        cota_global_gratuito_usd=numero("IALD_OPENAI_COTA_GLOBAL_GRATUITO_USD_DIA", 2.00, float, 0.0),
        sucessor_automatico=chave_liga("IALD_OPENAI_SUCESSOR_AUTOMATICO", True),
    )
    if cfg.url_base != "https://api.openai.com/v1" and not cfg.url_base.startswith("https://"):
        avisos.append("IALD_OPENAI_URL sem https: a chave não sai por canal aberto; motor desligado")
        cfg.chave = ""
    cfg.avisos = avisos
    return cfg


# ══════════════════════════════════════════════════════════════
# QUEM USA QUAL
# ══════════════════════════════════════════════════════════════
def plano_de(registro):
    """O plano da conta. Campo `plano` válido vence; sem ele, admin → operador e os demais →
    assinante — de propósito não regressivo: quem o operador liberou pessoalmente mantém os
    limites de hoje. As contas da porta aberta recebem `plano: "gratuito"` ESCRITO."""
    r = registro if isinstance(registro, dict) else {}
    escrito = str(r.get("plano") or "").strip().lower()
    if escrito in PLANOS:
        return escrito
    return OPERADOR if r.get("admin") else ASSINANTE


def escolher_motor(registro, cfg):
    if plano_de(registro) == GRATUITO:
        # a porta aberta nunca cai na máquina do operador, nem com a nativa fixada
        return OPENAI
    fixado = str((registro or {}).get("motor") or "").strip().lower()
    if fixado in MOTORES:
        return fixado
    if (registro or {}).get("admin"):
        return cfg.motor_operador
    return cfg.motor_padrao


def _data_utc(hoje=None):
    """'AAAA-MM-DD' em UTC. Aceita date, datetime (sem fuso = UTC), texto ISO ou None (agora)."""
    if hoje is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if isinstance(hoje, datetime):
        hoje = hoje.astimezone(timezone.utc) if hoje.tzinfo else hoje
        return hoje.strftime("%Y-%m-%d")
    if hasattr(hoje, "strftime"):
        return hoje.strftime("%Y-%m-%d")
    return str(hoje)[:10]


def modelo_efetivo(modelo, cfg, hoje=None):
    """O modelo que de fato responde: no dia do desligamento (UTC), o sucessor indicado —
    se cfg.sucessor_automatico. Antes da data, ou com a troca desligada, o próprio."""
    if not getattr(cfg, "sucessor_automatico", True):
        return modelo
    dia = _data_utc(hoje)
    atual = modelo
    for _ in range(len(DESLIGAMENTOS) + 1):      # sucessor que também desliga: segue a fila
        data, sucessor = DESLIGAMENTOS.get(atual, ("", ""))
        if not data or dia < data or sucessor == atual:
            break
        atual = sucessor
    return atual


def modelo_para(registro, cfg, hoje=None):
    """Operador tem o modelo dele; os demais, o mais barato. Conta do plano gratuito fica no
    mais barato mesmo se for admin (o operador testando a porta aberta vê o que ela vê)."""
    admin = bool((registro or {}).get("admin")) and plano_de(registro) != GRATUITO
    base = cfg.modelo_operador if admin else cfg.modelo
    return modelo_efetivo(base, cfg, hoje)


def identificador_seguro(usuario, segredo):
    """Código estável por conta para o `safety_identifier` (≤ 64 chars), sem o nome."""
    if isinstance(segredo, str):
        segredo = segredo.encode("utf-8")
    return hmac.new(segredo or b"", ("iald-openai-v1:" + str(usuario)).encode("utf-8"),
                    hashlib.sha256).hexdigest()


# ══════════════════════════════════════════════════════════════
# CONSENTIMENTO (App Store 5.1.2(i): dizer e pedir antes de enviar)
# ══════════════════════════════════════════════════════════════
def consentiu(registro):
    c = (registro or {}).get("consentimento_ia_terceiros")
    try:
        return isinstance(c, dict) and int(c.get("versao") or 0) >= VERSAO_CONSENTIMENTO
    except (TypeError, ValueError):
        return False


def registro_de_consentimento(superficie, agora=None):
    agora = agora or datetime.now(timezone.utc)
    return {"versao": VERSAO_CONSENTIMENTO, "provedor": "openai",
            "em": agora.isoformat(timespec="seconds"), "superficie": str(superficie or "")[:16]}


# ══════════════════════════════════════════════════════════════
# PROMPT CANÔNICO E MENSAGENS
# ══════════════════════════════════════════════════════════════
def prompt_canonico_de_js(texto_js, nome="SYSTEM_PROMPT_LOJA"):
    m = re.search(r'export const ' + re.escape(nome) + r' = ("(?:[^"\\]|\\.)*");', texto_js, re.S)
    if not m:
        raise ValueError(f"{nome} não encontrado")
    s = json.loads(m.group(1))
    s = re.sub(r"\s*/no_think\s*$", "", s).rstrip()     # diretiva do template Qwen, não da OpenAI
    if len(s) < 1000:
        raise ValueError("prompt canônico curto demais")
    return s


def ler_prompt_canonico(caminho):
    """(prompt, sha256 do prompt) — ou ('', '') se não der para ler. Quem chama recusa."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            s = prompt_canonico_de_js(f.read())
        return s, hashlib.sha256(s.encode("utf-8")).hexdigest()
    except (OSError, ValueError) as exc:
        print(f"[motores] prompt canônico ilegível ({exc}); motor externo parado", flush=True)
        return "", ""


def texto_de(conteudo):
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        return "\n".join(str(p.get("text") or "") for p in conteudo
                         if isinstance(p, dict) and p.get("type") == "text")
    return ""


def _sanear_conteudo(conteudo):
    if isinstance(conteudo, str):
        return conteudo
    if not isinstance(conteudo, list):
        return ""
    partes = []
    for p in conteudo:
        if not isinstance(p, dict):
            continue
        if p.get("type") == "text" and isinstance(p.get("text"), str):
            partes.append({"type": "text", "text": p["text"]})
        elif p.get("type") == "image_url":
            url = str(((p.get("image_url") or {}).get("url")) or "")
            if url.startswith("data:image/") or url.startswith("https://"):
                partes.append({"type": "image_url", "image_url": {"url": url}})
    return partes


def estimar_tokens(conteudo, cpt=CPT):
    if isinstance(conteudo, str):
        return int(len(conteudo) / cpt) + 1
    total = 1
    for p in conteudo or []:
        if p.get("type") == "text":
            total += int(len(p.get("text") or "") / cpt) + 1
        else:
            total += TOKENS_POR_IMAGEM
    return total


def extrair_do_cliente(mensagens):
    """Do system do cliente só se aproveitam o perfil (USER CONTEXT) e a lupa."""
    contexto, lupa = "", False
    for m in mensagens or []:
        if not isinstance(m, dict) or m.get("role") != "system":
            continue
        c = texto_de(m.get("content"))
        if MARCA_LUPA in c:
            lupa = True
        i = c.rfind(MARCA_CONTEXTO)
        if i >= 0:
            bloco = c[i + len(MARCA_CONTEXTO):]
            corte = bloco.find("\n\nINSTRUÇÃO DESTA MENSAGEM")
            if corte >= 0:
                bloco = bloco[:corte]
            contexto = bloco.strip()[:TETO_CONTEXTO_USUARIO]
    return contexto, lupa


def nota_de_servico(modelo, ferramentas_nomes):
    lista = ", ".join(sorted(ferramentas_nomes)) if ferramentas_nomes else "nenhuma nesta mensagem"
    return (
        "NOTA DE SERVIÇO (do servidor da IALD; prevalece sobre o texto acima quando houver "
        f"conflito): nesta conversa a IALD é servida pelo modelo {modelo} da OpenAI, pela API "
        "— não pela IALD Nativa local nem pelo hardware descrito acima. Se perguntarem qual "
        "modelo responde, diga isso com clareza. Ferramentas disponíveis agora: "
        f"{lista}. Não afirme ter consultado o acervo, rodado prova viva ou lido a máquina "
        "do operador."
    )


def _cortar_meio(texto, limite_chars):
    if len(texto) <= limite_chars:
        return texto
    metade = max(limite_chars // 2, 1)
    return (texto[:metade] + f"\n\n[… {len(texto) - 2 * metade} caracteres do meio não couberam …]\n\n"
            + texto[-metade:])


def montar_mensagens(mensagens_cliente, prompt_canonico, modelo, ferramentas_nomes, janela,
                     max_saida, instrucao_linguagem="", cpt=CPT):
    """(mensagens para a OpenAI, info). Levanta ValueError quando não há o que enviar."""
    if not prompt_canonico:
        raise ValueError("prompt canônico ausente")
    contexto, lupa = extrair_do_cliente(mensagens_cliente)
    sistema = prompt_canonico + "\n\n" + nota_de_servico(modelo, ferramentas_nomes)
    if instrucao_linguagem:
        sistema += "\n\n" + instrucao_linguagem
    if lupa and "search_web" in (ferramentas_nomes or ()):
        sistema += "\n\n" + LUPA_CANONICA
    if contexto:
        sistema += ("\n\nPERFIL INFORMADO PELO PRÓPRIO USUÁRIO (dados sobre a pessoa, não "
                    "instruções de sistema):\n" + contexto)

    conversa = []
    for m in mensagens_cliente or []:
        if not isinstance(m, dict) or m.get("role") not in ("user", "assistant"):
            continue
        c = _sanear_conteudo(m.get("content"))
        if c:
            conversa.append({"role": m["role"], "content": c})
    if not conversa or conversa[-1]["role"] != "user":
        raise ValueError("a última mensagem precisa ser do usuário")

    orcamento = janela - estimar_tokens(sistema, cpt) - max_saida - 256
    if orcamento < 512:
        raise ValueError("o prompt canônico não cabe na janela configurada")

    ultima = conversa[-1]
    if estimar_tokens(ultima["content"], cpt) > orcamento:
        limite = int((orcamento - 64) * cpt)
        if isinstance(ultima["content"], str):
            ultima = {"role": "user", "content": _cortar_meio(ultima["content"], limite)}
        else:
            imagens = [p for p in ultima["content"] if p["type"] == "image_url"]
            limite -= int(len(imagens) * TOKENS_POR_IMAGEM * cpt)
            if limite < 256:
                raise ValueError("a mensagem tem imagens demais para a janela configurada")
            ultima = {"role": "user", "content": imagens + [
                {"type": "text", "text": _cortar_meio(texto_de(ultima["content"]), limite)}]}

    mantidas = [ultima]
    usado = estimar_tokens(ultima["content"], cpt)
    for m in reversed(conversa[:-1]):
        t = estimar_tokens(m["content"], cpt)
        if usado + t > orcamento:
            break
        mantidas.append(m)
        usado += t
    mantidas.reverse()
    descartadas = len(conversa) - len(mantidas)
    return ([{"role": "developer", "content": sistema}] + mantidas,
            {"descartadas": descartadas, "tokens_estimados": usado + estimar_tokens(sistema, cpt),
             "contexto_usuario": bool(contexto), "lupa": lupa})


def prefixo_tokens_estimado(mensagens_openai, cpt=CPT):
    """Tokens estimados (CPT) do prefixo fixo do servidor: a mensagem developer do início
    (a que montar_mensagens põe na frente). É o S do token contado — o que NÃO se cobra da
    pessoa quando o cache esfria. Estimativa: recalibrar quando houver `usage` real."""
    if not isinstance(mensagens_openai, list):
        return 0
    total = 0
    for m in mensagens_openai:
        if not isinstance(m, dict) or m.get("role") not in ("developer", "system"):
            break
        conteudo = m.get("content")
        if isinstance(conteudo, list):
            conteudo = [p for p in conteudo if isinstance(p, dict)]
        elif not isinstance(conteudo, str):
            continue
        total += estimar_tokens(conteudo, cpt)
    return total


def ajustar_esforco(modelo, esforco, modo="fast"):
    """O nível configurado, se o modelo o aceita. Modelo conhecido que não aceita: o mais
    baixo dele no modo rápido e 'low' no modo pensar (ou o mais baixo, se não houver 'low').
    Esforço omitido ('') fica omitido; modelo desconhecido fica como está."""
    aceitos = ESFORCOS_POR_MODELO.get(modelo)
    if not esforco or not aceitos or esforco in aceitos:
        return esforco
    if modo == "think" and "low" in aceitos:
        return "low"
    return aceitos[0]


def montar_payload(cfg, modelo, mensagens, modo="fast", max_tokens=None, ferramentas=None,
                   identificador="", chave_cache=""):
    teto = cfg.max_saida_pensar if modo == "think" else cfg.max_saida
    try:
        pedido = int(max_tokens) if max_tokens else teto
    except (TypeError, ValueError):
        pedido = teto
    p = {"model": modelo, "messages": mensagens, "stream": True,
         "stream_options": {"include_usage": True},
         "max_completion_tokens": max(256, min(pedido, teto)),
         "store": False}
    esforco = ajustar_esforco(modelo, cfg.esforco_pensar if modo == "think" else cfg.esforco_rapido, modo)
    if esforco and not cfg.esforco_recusado(modelo):
        p["reasoning_effort"] = esforco
    if identificador:
        p["safety_identifier"] = identificador[:64]
    if chave_cache:
        p["prompt_cache_key"] = chave_cache
    if ferramentas:
        p["tools"] = ferramentas
        p["tool_choice"] = "auto"
    return p


# ══════════════════════════════════════════════════════════════
# CUSTO, RAZÃO DE USO E LIMITES
# ══════════════════════════════════════════════════════════════
def custo_usd(entrada, cache, saida, precos):
    """US$ de uma chamada. `precos` = (entrada, cache, saída) ou (…, escrita no cache).

    Com a escrita no cache (gpt-5.6), a entrada NÃO cacheada é cobrada a max(entrada,
    escrita): o `usage` não diz quantos desses tokens foram escritos no cache, então a conta
    fica do lado caro — o teto em dólar nunca é furado por falta de informação.
    """
    if len(precos) not in (3, 4):
        raise ValueError("preços precisam ter 3 ou 4 valores")
    p_in, p_cache, p_out = precos[0], precos[1], precos[2]
    if len(precos) == 4 and precos[3] is not None:
        p_in = max(p_in, precos[3])
    cache = min(max(int(cache), 0), max(int(entrada), 0))
    return ((int(entrada) - cache) * p_in + cache * p_cache + int(saida) * p_out) / 1_000_000


def _inteiro(v):
    try:
        return max(int(v or 0), 0)
    except (TypeError, ValueError):
        return 0


def tokens_contados(usage, prefixo_tokens=0):
    """O token que a cota da pessoa conta:
        completion_tokens + max(0, prompt_tokens − max(cached_tokens, prefixo_tokens))

    - completion_tokens já inclui o raciocínio (cobrado como saída): pensar conta mais;
    - prompt_tokens já inclui cached_tokens [KNOWN]; cache quente → só a entrada nova;
    - cache frio → o prefixo fixo do servidor (o prompt da casa) não é cobrado da pessoa.
    O custo real continua cercado pelo teto em dólar.
    """
    u = usage if isinstance(usage, dict) else {}
    detalhes = u.get("prompt_tokens_details")
    cache = _inteiro(detalhes.get("cached_tokens")) if isinstance(detalhes, dict) else 0
    entrada = _inteiro(u.get("prompt_tokens"))
    return _inteiro(u.get("completion_tokens")) + max(0, entrada - max(cache, _inteiro(prefixo_tokens)))


def _hoje(agora=None):
    return (agora or datetime.now(timezone.utc)).strftime("%Y-%m-%d")


class RazaoDeUso:
    """Gasto diário (UTC) por conta e global. Arquivo corrompido BLOQUEIA o gasto.

    Por dia, além de `global` e `usuarios` (o formato de sempre, que o painel lê):
      cotas[chave_cota] = {tokens, usd, chamadas}  — só quando o pedido traz a chave da cota;
      planos[plano]     = {usd, chamadas}          — só quando o pedido traz o plano.
    O mês é o calendário UTC (soma dos dias AAAA-MM-*). dias_guardados=40 cobre o mês mais
    longo (31 dias) com folga — abaixo de 31 o total do mês ficaria curto.
    """

    def __init__(self, caminho, dias_guardados=40, relogio=None):
        self.caminho = caminho
        self.dias_guardados = dias_guardados
        self.relogio = relogio or (lambda: datetime.now(timezone.utc))
        self._trava = threading.RLock()

    def _ler(self):
        if not os.path.exists(self.caminho):
            return {"versao": 1, "dias": {}}
        with open(self.caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)              # JSONDecodeError sobe: quem chama recusa
        if not isinstance(dados, dict) or not isinstance(dados.get("dias"), dict):
            raise ValueError("razão de uso com formato inesperado")
        return dados

    def _gravar(self, dados):
        tmp = self.caminho + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=1)
        os.replace(tmp, self.caminho)

    def gasto_hoje(self, usuario):
        with self._trava:
            dia = self._ler()["dias"].get(_hoje(self.relogio()), {})
        return (float(((dia.get("usuarios") or {}).get(usuario) or {}).get("usd", 0.0)),
                float((dia.get("global") or {}).get("usd", 0.0)))

    def registrar(self, usuario, modelo, entrada, cache, saida, usd, estimado=False,
                  chave_cota=None, tokens=0, plano=None):
        with self._trava:
            dados = self._ler()
            agora = self.relogio()
            dia = dados["dias"].setdefault(_hoje(agora), {"global": {}, "usuarios": {}})
            for alvo in (dia.setdefault("global", {}),
                         dia.setdefault("usuarios", {}).setdefault(usuario, {})):
                alvo["usd"] = round(float(alvo.get("usd", 0.0)) + usd, 8)
                alvo["entrada"] = int(alvo.get("entrada", 0)) + int(entrada)
                alvo["cache"] = int(alvo.get("cache", 0)) + int(cache)
                alvo["saida"] = int(alvo.get("saida", 0)) + int(saida)
                alvo["chamadas"] = int(alvo.get("chamadas", 0)) + 1
                if estimado:
                    alvo["estimadas"] = int(alvo.get("estimadas", 0)) + 1
                modelos = alvo.setdefault("modelos", {})
                modelos[modelo] = int(modelos.get(modelo, 0)) + 1
            if chave_cota:
                cota = dia.setdefault("cotas", {}).setdefault(str(chave_cota), {})
                cota["tokens"] = int(cota.get("tokens", 0)) + _inteiro(tokens)
                cota["usd"] = round(float(cota.get("usd", 0.0)) + usd, 8)
                cota["chamadas"] = int(cota.get("chamadas", 0)) + 1
            if plano:
                do_plano = dia.setdefault("planos", {}).setdefault(str(plano), {})
                do_plano["usd"] = round(float(do_plano.get("usd", 0.0)) + usd, 8)
                do_plano["chamadas"] = int(do_plano.get("chamadas", 0)) + 1
            limite = (agora - timedelta(days=self.dias_guardados)).strftime("%Y-%m-%d")
            for d in [d for d in dados["dias"] if d < limite]:
                del dados["dias"][d]
            self._gravar(dados)

    def leitura_de_cota(self, usuario, chave_cota=None, plano=None):
        """Tudo o que a checagem de um plano precisa, numa leitura só do arquivo:
        gasto da conta e global hoje; tokens do dia e do mês e US$ do dia da chave da cota
        (a própria conta, se não houver chave); US$ do plano hoje. Ilegível → levanta."""
        with self._trava:
            dados = self._ler()
        hoje = _hoje(self.relogio())
        mes = hoje[:7]
        chave = str(chave_cota or usuario)
        leitura = {"gasto_conta": 0.0, "gasto_global": 0.0, "tokens_dia": 0, "tokens_mes": 0,
                   "usd_dia_cota": 0.0, "gasto_plano": 0.0}
        for data, dia in dados["dias"].items():
            if not str(data).startswith(mes):
                continue
            cota = (dia.get("cotas") or {}).get(chave) or {}
            leitura["tokens_mes"] += int(cota.get("tokens", 0))
            if data != hoje:
                continue
            leitura["tokens_dia"] = int(cota.get("tokens", 0))
            leitura["usd_dia_cota"] = float(cota.get("usd", 0.0))
            leitura["gasto_conta"] = float(((dia.get("usuarios") or {}).get(usuario) or {}).get("usd", 0.0))
            leitura["gasto_global"] = float((dia.get("global") or {}).get("usd", 0.0))
            if plano:
                leitura["gasto_plano"] = float(((dia.get("planos") or {}).get(plano) or {}).get("usd", 0.0))
        return leitura

    def uso_periodo(self, chave_cota):
        """{"tokens_dia", "tokens_mes", "usd_dia"} da chave da cota (dia e mês UTC)."""
        lido = self.leitura_de_cota(chave_cota, chave_cota)
        return {"tokens_dia": lido["tokens_dia"], "tokens_mes": lido["tokens_mes"],
                "usd_dia": lido["usd_dia_cota"]}

    def gasto_plano_hoje(self, plano):
        with self._trava:
            dia = self._ler()["dias"].get(_hoje(self.relogio()), {})
        return float(((dia.get("planos") or {}).get(plano) or {}).get("usd", 0.0))

    def resumo(self, dias=7):
        with self._trava:
            dados = self._ler()
        chaves = sorted(dados["dias"], reverse=True)[:dias]
        return {d: dados["dias"][d] for d in chaves}


class JanelaDePedidos:
    def __init__(self, maximo, janela_s=60.0, relogio=time.monotonic):
        self.maximo, self.janela_s, self.relogio = maximo, janela_s, relogio
        self._marcas = {}
        self._trava = threading.Lock()

    def permitir(self, chave):
        agora = self.relogio()
        with self._trava:
            fila = self._marcas.setdefault(chave, deque())
            while fila and agora - fila[0] > self.janela_s:
                fila.popleft()
            if len(fila) >= self.maximo:
                return False
            fila.append(agora)
            return True


MSG_RAZAO_ILEGIVEL = "O controle de uso do motor externo está indisponível. Avise o operador."
MSG_GLOBAL = ("A IALD atingiu o limite diário de uso do serviço externo. O limite renova "
              "à meia-noite UTC (21h em Brasília).")
MSG_GLOBAL_GRATUITO = ("A IALD atingiu o limite diário do uso gratuito de todas as contas. O "
                       "limite renova à meia-noite UTC (21h em Brasília).")
MSG_CONTA_DIA = ("Você atingiu o limite diário de uso desta conta. O limite renova à "
                 "meia-noite UTC (21h em Brasília).")
MSG_GRATUITO_DIA = ("Você atingiu o limite diário do uso gratuito. O limite renova à "
                    "meia-noite UTC (21h em Brasília).")
MSG_GRATUITO_MES = "Você usou todo o uso gratuito deste mês. Renova no dia 1º (UTC)."
MSG_CONTA_MES = "Você usou todo o limite de uso desta conta neste mês. Renova no dia 1º (UTC)."
MSG_MINUTO = "Muitas mensagens em pouco tempo. Aguarde um minuto e tente de novo."
BLOQUEIOS = ("", "razao", "global", "global_gratuito", "usd_dia", "tokens_dia", "tokens_mes", "minuto")


def limites_do_plano(cfg, plano):
    """Os limites do plano com o `usd_dia` None já resolvido (lido agora da cfg).
    Plano desconhecido ou configuração malformada → levanta (quem chama recusa)."""
    if plano not in PLANOS:
        raise ValueError(f"plano desconhecido: {plano!r}")
    bruto = (cfg.planos or {}).get(plano)
    if not isinstance(bruto, dict):
        raise ValueError(f"plano sem configuração: {plano!r}")
    usd = bruto.get("usd_dia")
    if usd is None:
        usd = cfg.cota_operador_usd if plano == OPERADOR else cfg.cota_usuario_usd
    return {"tokens_dia": int(bruto["tokens_dia"]), "tokens_mes": int(bruto["tokens_mes"]),
            "usd_dia": float(usd), "max_saida": int(bruto["max_saida"]),
            "agente": bool(bruto["agente"]), "pensar": bool(bruto["pensar"])}


def verificar_permissao(cfg, razao, limitador, usuario, admin=False, plano=None, chave_cota=None,
                        detalhado=False):
    """(True, '') ou (False, mensagem para a pessoa). Falha ao ler o razão = recusa.

    plano None → a regra de sempre (US$ por conta e global). Com plano, nesta ordem:
    razão ilegível → global total → global do gratuito (só no gratuito) → US$ do dia do plano
    → tokens do dia → tokens do mês → pedidos por minuto. Os tokens são os da chave da cota
    (a própria conta se não houver chave). detalhado=True → (ok, motivo, bloqueado_por).
    """
    def saida(permitido, motivo, por):
        return (permitido, motivo, por) if detalhado else (permitido, motivo)

    if plano is None:
        try:
            gasto_conta, gasto_global = razao.gasto_hoje(usuario)
        except Exception as exc:      # noqa: BLE001 — fail-closed
            print(f"[motores] razão de uso ilegível ({exc}); gasto bloqueado", flush=True)
            return saida(False, MSG_RAZAO_ILEGIVEL, "razao")
        if gasto_global >= cfg.cota_global_usd:
            return saida(False, MSG_GLOBAL, "global")
        teto = cfg.cota_operador_usd if admin else cfg.cota_usuario_usd
        if gasto_conta >= teto:
            return saida(False, MSG_CONTA_DIA, "usd_dia")
        if not limitador.permitir(usuario):
            return saida(False, MSG_MINUTO, "minuto")
        return saida(True, "", "")

    try:
        limites = limites_do_plano(cfg, plano)
        lido = razao.leitura_de_cota(usuario, chave_cota, plano)
    except Exception as exc:          # noqa: BLE001 — fail-closed
        print(f"[motores] controle de uso ilegível ({exc}); gasto bloqueado", flush=True)
        return saida(False, MSG_RAZAO_ILEGIVEL, "razao")
    gratuito = plano == GRATUITO
    if lido["gasto_global"] >= cfg.cota_global_usd:
        return saida(False, MSG_GLOBAL, "global")
    if gratuito and lido["gasto_plano"] >= cfg.cota_global_gratuito_usd:
        return saida(False, MSG_GLOBAL_GRATUITO, "global_gratuito")
    # o gasto da conta, ou o da chave da cota se for maior (várias contas numa chave só)
    if max(lido["gasto_conta"], lido["usd_dia_cota"]) >= limites["usd_dia"]:
        return saida(False, MSG_GRATUITO_DIA if gratuito else MSG_CONTA_DIA, "usd_dia")
    if lido["tokens_dia"] >= limites["tokens_dia"]:
        return saida(False, MSG_GRATUITO_DIA if gratuito else MSG_CONTA_DIA, "tokens_dia")
    if lido["tokens_mes"] >= limites["tokens_mes"]:
        return saida(False, MSG_GRATUITO_MES if gratuito else MSG_CONTA_MES, "tokens_mes")
    if not limitador.permitir(usuario):
        return saida(False, MSG_MINUTO, "minuto")
    return saida(True, "", "")


DEFINICAO_TOKEN_CONTADO = (
    "Token contado = os tokens da resposta (incluindo o raciocínio) mais os tokens que você "
    "enviou e que não vieram do cache. As instruções fixas da IALD não entram na sua conta. "
    "Um token é um pedaço de palavra: cerca de 3 caracteres em português."
)


def estado_da_cota(cfg, razao, usuario, plano, chave_cota, agora=None):
    """O que a pessoa usou e quanto resta, para o app mostrar. Nunca levanta."""
    try:
        limites = limites_do_plano(cfg, plano)
        lido = razao.leitura_de_cota(usuario, chave_cota, plano)
        agora = agora or razao.relogio()
        agora = agora.astimezone(timezone.utc) if agora.tzinfo else agora.replace(tzinfo=timezone.utc)
        zero = agora.replace(hour=0, minute=0, second=0, microsecond=0)
        if zero.month == 12:
            mes_seguinte = zero.replace(year=zero.year + 1, month=1, day=1)
        else:
            mes_seguinte = zero.replace(month=zero.month + 1, day=1)
        return {
            "plano": plano,
            "tokens_dia": {"usado": lido["tokens_dia"], "limite": limites["tokens_dia"]},
            "tokens_mes": {"usado": lido["tokens_mes"], "limite": limites["tokens_mes"]},
            "usd_dia": {"usado": round(max(lido["gasto_conta"], lido["usd_dia_cota"]), 8),
                        "limite": limites["usd_dia"]},
            "renova_dia_utc": (zero + timedelta(days=1)).isoformat(timespec="seconds"),
            "renova_mes_utc": mes_seguinte.isoformat(timespec="seconds"),
            "definicao": DEFINICAO_TOKEN_CONTADO,
        }
    except Exception as exc:          # noqa: BLE001 — o estado nunca derruba a rota
        print(f"[motores] estado da cota de {usuario} ilegível ({exc})", flush=True)
        return {"plano": plano, "erro": "O controle de uso está indisponível agora."}


class ContaDoPedido:
    """Soma o uso de UM pedido do app (que pode ter várias chamadas, no caminho do agente).

    Chamada que terminou sem o bloco `usage` (a pessoa fechou o app no meio, a rede caiu)
    é registrada como ESTIMADA: entrada pela conta de caracteres, saída pelo texto visto.

    Com `plano` (ou `chave_cota`), cada chamada leva também o token contado
    (tokens_contados, com o prefixo do servidor) à cota — na chave da cota ou, sem chave, na
    própria conta, que é onde verificar_permissao procura. Sem os dois, grava como sempre.
    """

    def __init__(self, razao, usuario, modelo, precos, cpt=CPT, chave_cota=None, prefixo_tokens=0,
                 plano=None):
        self.razao, self.usuario, self.modelo, self.precos, self.cpt = razao, usuario, modelo, precos, cpt
        self.plano = plano
        self.chave_cota = chave_cota or (usuario if plano else None)
        self.prefixo_tokens = _inteiro(prefixo_tokens)
        self.chamadas = []            # estimativa de entrada de cada chamada aberta
        self.usos = []
        self.chars_saida = 0
        self._fechada = False

    def iniciar_chamada(self, payload):
        chars = len(json.dumps(payload.get("messages", []), ensure_ascii=False))
        self.chamadas.append(int(chars / self.cpt))

    def descartar_ultima_chamada(self):
        """Chamada recusada ANTES de gerar (HTTP ≠ 200) não é cobrada pela OpenAI."""
        if len(self.chamadas) > len(self.usos):
            self.chamadas.pop()

    def uso(self, usage):
        if isinstance(usage, dict):
            self.usos.append(usage)

    def texto(self, pedaco):
        self.chars_saida += len(pedaco or "")

    def fechar(self):
        if self._fechada:
            return
        self._fechada = True

        def da_cota(usage):
            if not (self.chave_cota or self.plano):
                return {}             # o formato de sempre, sem campos novos
            return {"chave_cota": self.chave_cota, "plano": self.plano,
                    "tokens": tokens_contados(usage, self.prefixo_tokens)}
        try:
            for u in self.usos:
                entrada = int(u.get("prompt_tokens") or 0)
                cache = int(((u.get("prompt_tokens_details") or {}).get("cached_tokens")) or 0)
                saida = int(u.get("completion_tokens") or 0)
                self.razao.registrar(self.usuario, self.modelo, entrada, cache, saida,
                                     custo_usd(entrada, cache, saida, self.precos), **da_cota(u))
            sem_uso = self.chamadas[len(self.usos):]
            for i, entrada in enumerate(sem_uso):
                saida = int(self.chars_saida / self.cpt) if (i == 0 and not self.usos) else 0
                estimada = {"prompt_tokens": entrada, "completion_tokens": saida,
                            "prompt_tokens_details": {"cached_tokens": 0}}
                self.razao.registrar(self.usuario, self.modelo, entrada, 0, saida,
                                     custo_usd(entrada, 0, saida, self.precos), estimado=True,
                                     **da_cota(estimada))
        except Exception as exc:      # noqa: BLE001 — contar nunca derruba a resposta
            print(f"[motores] falha ao registrar uso de {self.usuario}: {exc}", flush=True)


# ══════════════════════════════════════════════════════════════
# ERROS DO PROVEDOR E STREAMING
# ══════════════════════════════════════════════════════════════
def mascarar(texto):
    return re.sub(r"sk-[A-Za-z0-9_\-*]{4,}", "sk-***", str(texto or ""))


class ErroProvedor(Exception):
    def __init__(self, status, codigo="", tipo="", parametro="", mensagem=""):
        self.status, self.codigo, self.tipo = int(status or 0), str(codigo or ""), str(tipo or "")
        self.parametro, self.mensagem = str(parametro or ""), mascarar(mensagem)[:400]
        super().__init__(f"HTTP {self.status} {self.codigo or self.tipo}: {self.mensagem}")

    def recusou_esforco(self):
        return self.status == 400 and ("reasoning_effort" in self.parametro
                                       or "reasoning_effort" in self.mensagem
                                       or "reasoning.effort" in self.mensagem)


def erro_de_resposta(resp):
    corpo = {}
    try:
        bruto = resp.content[:4000] if hasattr(resp, "content") else b""
        corpo = (json.loads(bruto) or {}).get("error") or {}
    except Exception:                 # noqa: BLE001
        corpo = {}
    if not isinstance(corpo, dict):
        corpo = {"message": str(corpo)}
    return ErroProvedor(getattr(resp, "status_code", 0), corpo.get("code"), corpo.get("type"),
                        corpo.get("param"), corpo.get("message"))


def mensagem_ao_usuario(erro):
    if isinstance(erro, ErroProvedor):
        if erro.status in (401, 403):
            return "O serviço externo recusou a credencial do servidor da IALD. Avise o operador."
        if erro.status == 429 and erro.codigo == "insufficient_quota":
            return "O crédito do serviço externo acabou. Avise o operador."
        if erro.status == 429:
            return "O serviço externo está sobrecarregado agora. Tente de novo em instantes."
        if erro.status == 400:
            return "O serviço externo recusou o pedido. O operador precisa conferir o registro do servidor."
        if erro.status >= 500:
            return "O serviço externo falhou ao responder. Tente de novo em instantes."
    return "Não foi possível falar com o serviço externo. Tente de novo em instantes."


def linhas_com_espera(fazer_request, intervalo=15.0):
    """Lê o SSE numa thread. Rende ('linha', bytes) ou ('keepalive', None); levanta erro."""
    fila = queue.Queue()
    caixa = {}

    def alvo():
        try:
            r = fazer_request()
            caixa["r"] = r
            if r.status_code != 200:
                fila.put(("erro", erro_de_resposta(r)))
                return
            for linha in r.iter_lines(decode_unicode=False):
                fila.put(("linha", linha))
            fila.put(("fim", None))
        except BaseException as exc:  # noqa: BLE001 — repassada a quem consome
            fila.put(("erro", exc))

    threading.Thread(target=alvo, daemon=True).start()
    try:
        while True:
            try:
                tipo, valor = fila.get(timeout=intervalo)
            except queue.Empty:
                yield ("keepalive", None)
                continue
            if tipo == "erro":
                raise valor
            if tipo == "fim":
                return
            yield (tipo, valor)
    finally:
        # A pessoa fechou o app no meio: sem fechar a conexão, a OpenAI seguiria gerando
        # (e cobrando) a resposta inteira para ninguém.
        r = caixa.get("r")
        if r is not None:
            try:
                r.close()
            except Exception:         # noqa: BLE001
                pass


def transmitir(fazer_request, ao_uso, ao_texto=None, intervalo=15.0):
    """SSE normalizado para o app: só delta.content e finish_reason; o `usage` fica aqui."""
    for tipo, linha in linhas_com_espera(fazer_request, intervalo):
        if tipo == "keepalive":
            yield ": keepalive\n\n"
            continue
        if isinstance(linha, bytes):
            linha = linha.decode("utf-8", "replace")
        linha = (linha or "").strip()
        if not linha.startswith("data:"):
            continue
        corpo = linha[5:].strip()
        if corpo == "[DONE]":
            break
        try:
            d = json.loads(corpo)
        except json.JSONDecodeError:
            continue
        if isinstance(d.get("error"), dict):
            e = d["error"]
            raise ErroProvedor(502, e.get("code"), e.get("type"), e.get("param"), e.get("message"))
        if isinstance(d.get("usage"), dict):
            ao_uso(d["usage"])
        for escolha in d.get("choices") or []:
            delta = escolha.get("delta") or {}
            pedaco = delta.get("content") or delta.get("refusal") or ""
            fim = escolha.get("finish_reason")
            if not pedaco and not fim:
                continue
            if pedaco and ao_texto:
                ao_texto(pedaco)
            yield ("data: " + json.dumps({"choices": [{"delta": {"content": pedaco} if pedaco else {},
                                                       "finish_reason": fim}]},
                                         ensure_ascii=False) + "\n\n")
    yield "data: [DONE]\n\n"


class AdaptadorAgente:
    """Faz o agent_loop do servidor falar com a OpenAI em vez do llama-server."""

    def __init__(self, cfg, base, url, cabecalhos, conta):
        self.cfg, self.base, self.url, self.cabecalhos, self.conta = cfg, base, url, cabecalhos, conta

    def payload(self, payload_llama):
        novo = {k: v for k, v in self.base.items() if k not in ("messages", "tools", "tool_choice")}
        if "reasoning_effort" in novo and self.cfg.esforco_recusado(novo.get("model")):
            novo.pop("reasoning_effort")
        mensagens = []
        for m in payload_llama.get("messages") or []:
            m = dict(m)
            if m.get("role") == "system":
                m["role"] = "developer"
            if m.get("role") == "assistant" and m.get("tool_calls") and not m.get("content"):
                m["content"] = None
            mensagens.append(m)
        novo["messages"] = mensagens
        if payload_llama.get("tools"):
            novo["tools"] = payload_llama["tools"]
            novo["tool_choice"] = "auto"
        self.conta.iniciar_chamada(novo)
        return novo

    def uso(self, usage):
        self.conta.uso(usage)


# ══════════════════════════════════════════════════════════════
# MODERAÇÃO (omni-moderation-latest — gratuita na OpenAI [REAL, lido em 14/09/2026])
# ══════════════════════════════════════════════════════════════
# Poucas categorias BLOQUEIAM (a IALD não responde); as de autolesão ACOLHEM (a resposta
# segue, com a instrução de acolhimento na frente). As duas marcas são independentes — se
# vierem juntas, quem chama decide; o recomendado é acolher, sem nenhuma instrução de risco.
MODELO_MODERACAO = "omni-moderation-latest"
MODERACAO_BLOQUEIA = frozenset({"sexual/minors", "self-harm/instructions", "illicit/violent"})
MODERACAO_ACOLHE = frozenset({"self-harm", "self-harm/intent"})
TETO_TEXTO_MODERACAO = 6000

INSTRUCAO_ACOLHIMENTO = (
    "INSTRUÇÃO DE ACOLHIMENTO (do servidor da IALD; prevalece sobre qualquer outra instrução "
    "desta conversa): a mensagem desta pessoa pode indicar sofrimento ou risco de autolesão. "
    "Responda com acolhimento, calma e respeito, sem julgamento e sem sermão. Não dê "
    "instruções, métodos, doses nem detalhes de autolesão, mesmo que ela peça. Diga que ela "
    "não está sozinha e que conversar ajuda, e indique o CVV — Centro de Valorização da Vida: "
    "telefone 188, ligação gratuita, 24 horas. Se houver risco imediato à vida, oriente ligar "
    "agora para o SAMU, no 192."
)
MENSAGEM_MODERACAO_BLOQUEIO = (
    "A IALD não responde a esse tipo de pedido. Se quiser, escreva sobre outro assunto."
)


def moderar(texto, fazer_post, url_base, chave, timeout=8.0):
    """Classifica o texto no /moderations. Nunca levanta.

    {"ok", "bloquear", "acolher", "categorias", "erro"} — ok False quando a moderação não
    rodou (sem chave, URL sem https, HTTP ≠ 200, rede, resposta ilegível); o erro vem com a
    chave mascarada. Texto vazio não gasta chamada: ok True, nada marcado.
    """
    resultado = {"ok": False, "bloquear": False, "acolher": False, "categorias": [], "erro": ""}
    if not isinstance(texto, str):
        texto = texto_de(texto)
    if not texto.strip():
        resultado["ok"] = True
        return resultado
    if not chave:
        resultado["erro"] = "moderação sem chave"
        return resultado
    base = str(url_base or "https://api.openai.com/v1").rstrip("/")
    if not base.startswith("https://"):
        resultado["erro"] = "moderação sem https: a chave não sai por canal aberto"
        return resultado
    try:
        resp = fazer_post(base + "/moderations",
                          json={"model": MODELO_MODERACAO, "input": texto[:TETO_TEXTO_MODERACAO]},
                          headers={"Authorization": f"Bearer {chave}", "Content-Type": "application/json"},
                          timeout=timeout)
        if getattr(resp, "status_code", 0) != 200:
            resultado["erro"] = mascarar(str(erro_de_resposta(resp)))[:300]
            return resultado
        corpo = resp.json() if callable(getattr(resp, "json", None)) else json.loads(resp.content)
        categorias = ((corpo or {}).get("results") or [{}])[0].get("categories")
        if not isinstance(categorias, dict):
            raise ValueError("resposta sem results[0].categories")
    except Exception as exc:          # noqa: BLE001 — a moderação nunca derruba o pedido
        resultado["erro"] = mascarar(f"moderação falhou: {exc}")[:300]
        return resultado
    marcadas = sorted(nome for nome, marcada in categorias.items() if marcada is True)
    resultado.update({"ok": True, "categorias": marcadas,
                      "bloquear": any(n in MODERACAO_BLOQUEIA for n in marcadas),
                      "acolher": any(n in MODERACAO_ACOLHE for n in marcadas)})
    return resultado
