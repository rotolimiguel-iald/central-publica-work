"""
═══════════════════════════════════════════════════════════════════════════════
    IALD — O MOTOR CLAUDE (Anthropic) DO CAMINHO EXTERNO (21/09/2026)

    O provedor Anthropic (Claude) do pipeline de motor externo da IALD.

    DECISÕES DO OPERADOR (verbatim, 21/09/2026):
      modelo      — *"Achei o Sonnet muito caro, mas é o melhor [...] eu vou instalar somente pra
                    mim, para eu testar"* → claude-sonnet-5 (janela de 1M; o prefixo TGL de
                    ~317k tokens o200k não cabe nos 200K do Haiku 4.5).
      o que vai   — *"O mesmo pacote do ChatGPT"*: o MESMO prefixo que o motor OpenAI recebe
                    (kernel v5, Memory Core, cluster v368 e, nas contas pagas/operador, Atlas §I/§VII
                    + TGL_INDICE_VIVO §0/§4). As seções §V, §VI e §X do Atlas e os arquivos
                    confidenciais ficam FORA, inclusive pelas ferramentas. Este módulo NÃO monta o
                    prefixo: recebe pronto (`prefixo`) quem o servidor já monta para a OpenAI.
      quem usa    — *"por enquanto só eu"* (lista de contas; no início só a conta 'luiz'). A lista
                    é do servidor; este módulo não decide acesso.

    O QUE ESTE MÓDULO FAZ. O pipeline (iald_web_server._chat_openai, agent_loop, e a contabilidade e
    a leitura de SSE de iald_motores) fala o formato Chat Completions da OpenAI por dentro. A
    tradução acontece SÓ na hora de enviar — post_como_openai recebe o payload no formato OpenAI,
    chama client.messages.stream(...) do SDK oficial e devolve um objeto com a cara de
    requests.Response (status_code, headers, text/content/json, iter_lines, iter_content, close)
    cujas linhas são pedaços `chat.completion.chunk` da OpenAI terminando em `data: [DONE]`. Assim
    linhas_com_espera, transmitir, ContaDoPedido, a reserva, _medir_saida_sse, a moderação da
    resposta e o app seguem sem mudança.

    O CACHE (a conta que mais pesa): o prefixo TGL vai num bloco de sistema PRÓPRIO com
    cache_control (5 min, ou 1 h com cfg.cache_ttl='1h'); a nota de serviço, o perfil e os avisos
    vão num segundo bloco SEM marca. O prefixo sai byte a byte igual entre chamadas — este módulo
    não põe data, hora, conta nem id em nada que vá antes da marca. As ferramentas mantêm a ORDEM
    recebida (elas são renderizadas antes do sistema: ordem trocada = cache perdido).
    21/09/2026 (revisão): e o cache AUTOMÁTICO no pedido (cache_control de topo, 5 min) para a cauda
    da conversa — histórico, tool_use/tool_result e o pensamento reenviado viram leitura de cache nas
    voltas seguintes do agente e na próxima mensagem. É a combinação que a skill claude-api prescreve
    para loops de agente [KNOWN — shared/prompt-caching.md, "The robust combination for agent loops"]:
    a marca explícita (5 min ou 1 h) vem ANTES da automática (5 min), como a regra "1 h antes de 5 min"
    exige.

    CORREÇÕES DA REVISÃO (21/09/2026, noite — revisores wire/segurança/custo/regressão):
      - imagem: só JPEG/PNG/GIF/WebP, pelo tipo lido nos BYTES (image/jpg, rótulo trocado e HEIC/BMP
        não viram 400 do pedido inteiro); acima de 10 MB em base64 ou do teto do pedido, a imagem vira
        um marcador de texto que diz por que não foi;
      - JSON de ferramenta que não valida: a ferramenta NÃO roda — o servidor pergunta
        EstadoClaude.entrada_invalida(id) e devolve o bruto como tool_result com is_error; o
        ValueError do SDK no meio da entrada vira linha de erro (claude_entrada_invalida), nunca
        uma volta tool_calls com argumentos {} [KNOWN — skill, tool-use-concepts.md, eager input];
      - conexão que falhou ANTES de enviar (DNS, TLS, recusada) → 503 claude_conexao; e
        recusa_sem_cobranca(status, código) diz ao servidor quais recusas antes do stream certamente
        não foram cobradas (504/502 ambíguos ficam na reserva);
      - recusa do modelo (stop_reason refusal): aviso "recusa" que RETIRA a parte já enviada; corte
        por max_tokens/janela: uma nota visível em vez do silêncio;
      - o Atlas integral (<ATLAS_CANONICO…>, com §V/§VI/§X) nunca sai para a Anthropic: recusa local.

    O PENSAMENTO: thinking adaptativo e output_config.effort = cfg.esforco_claude (padrão 'high').
    Numa volta com ferramenta, os blocos do assistente (inclusive os de pensamento, com a
    assinatura) ficam num EstadoClaude, pela lista de ids de tool_use, e voltam INTACTOS na
    chamada seguinte — o histórico interno do pipeline só guarda texto + tool_calls.

    O QUE ELE NÃO FAZ (fica com o servidor): moderação (a Anthropic não tem endpoint; segue na
    chave da OpenAI), consentimento, cotas, reserva, preço, escolha de conta, montagem do prefixo.

    ESTATUTOS: o formato do SDK (nomes de eventos, exceções tipadas, Timeout, with_options,
    count_tokens) vem da skill claude-api [KNOWN — arquivos da skill lidos em 21/09/2026]; o SDK
    NÃO pôde ser instalado nesta data (files.pythonhosted.org recusou TLS) e nada aqui rodou contra
    a API real [OPEN]. Os testes (tests/test_motor_claude.py) usam cliente falso.

    Este módulo não importa Flask nem iald_motores; o SDK entra de forma PREGUIÇOSA, só ao criar o
    cliente real. Sem SDK: HTTP 503 `claude_sdk_ausente`, nunca exceção.
═══════════════════════════════════════════════════════════════════════════════
"""

import base64
import binascii
import copy
import hashlib
import json
import re
import threading

MODELO_PADRAO = "claude-sonnet-5"
ESFORCOS_CLAUDE = ("low", "medium", "high", "xhigh", "max")
ESFORCO_PADRAO = "high"
NOTA_RECUSA = "\n\n[O Claude recusou responder a este pedido.]"
# 21/09/2026 (revisão): a recusa no meio já cobrou a parte gerada, e essa parte NÃO é resposta — a
# skill manda descartá-la [KNOWN — shared/model-migration.md, "refusal stop reason"]. O aviso sai com
# retirar_resposta (o app apaga o que já pintou e não guarda no histórico); NOTA_RECUSA segue como
# conteúdo depois dele, para quem não lê avisos.
AVISO_RECUSA = ("O Claude recusou responder a este pedido. A parte que já tinha chegado foi retirada e "
                "não entra no histórico da conversa.")
# corte por limite: antes saía "length" calado (e "(sem resposta)" quando o pensamento gastava tudo)
NOTA_CORTE = {
    "max_tokens": "\n\n[Resposta cortada: o Claude atingiu o limite de saída desta resposta.]",
    "model_context_window_exceeded": "\n\n[Resposta cortada: a conversa encheu a janela de contexto do Claude.]",
}
# Imagens que a API aceita e os tetos [KNOWN — página de visão, relatório 1 do levantamento de 21/09:
# jpeg/png/gif/webp; 10 MB por imagem em base64; 32 MB por pedido]. O teto do pedido fica em 24 MB de
# imagens para sobrar lugar ao prefixo (~1 MB) e ao histórico.
TIPOS_DE_IMAGEM = ("image/jpeg", "image/png", "image/gif", "image/webp")
TETO_IMAGEM_BASE64 = 10_000_000
TETO_IMAGENS_BASE64 = 24_000_000
# A marca do modo atlas_integral (iald_memoria_canonica.CanonicalMemory.prompt): o Atlas INTEIRO,
# com §V (patentes), §VI (caminhos) e §X (estado operacional) — nunca vai à Anthropic.
MARCA_ATLAS_INTEGRAL = "<ATLAS_CANONICO"
# 21/09/2026: o prefixo frio tem ~480–500k tokens Claude [INFERRED, relatório 4]; o prefill antes
# do primeiro byte pode passar do teto de 120 s que vale para a OpenAI. Leitura nunca abaixo disto.
TIMEOUT_LEITURA_MINIMO = 300.0
TIMEOUT_LEITURA_PADRAO = 600.0
TIMEOUT_CONEXAO = 10.0
MAX_RETRIES = 2

# stop_reason da Anthropic → finish_reason da OpenAI
PARADA_PARA_FIM = {
    "end_turn": "stop",
    "stop_sequence": "stop",
    "pause_turn": "stop",
    "tool_use": "tool_calls",
    "max_tokens": "length",
    "model_context_window_exceeded": "length",
    "refusal": "stop",
}

# Tipo de erro da Anthropic → status HTTP, para quando o status não vem (erro NO MEIO do stream,
# que chega depois do HTTP 200). [KNOWN — shared/error-codes.md da skill claude-api]
STATUS_POR_TIPO = {
    "invalid_request_error": 400,
    "authentication_error": 401,
    "billing_error": 402,
    "permission_error": 403,
    "not_found_error": 404,
    "request_too_large": 413,
    "rate_limit_error": 429,
    "api_error": 500,
    "timeout_error": 504,
    "overloaded_error": 529,
}

# Tipo/status da Anthropic → `code` no corpo OpenAI que o pipeline lê (erro_de_resposta). A regra
# completa, com as frases do corpo, está em codigo_openai().
MAPA_ERROS = {
    "billing_error": "claude_sem_credito",
    "authentication_error": "invalid_api_key",
    "permission_error": "permission_error",
    "not_found_error": "model_not_found",
    "request_too_large": "request_too_large",
    "rate_limit_error": "claude_rate_limit",
    "overloaded_error": "overloaded",
    401: "invalid_api_key",
    402: "claude_sem_credito",
    403: "permission_error",
    404: "model_not_found",
    413: "request_too_large",
    429: "claude_rate_limit",
    529: "overloaded",
}

# Exceções tipadas do SDK, da MAIS específica para a mais geral (status base quando o objeto não
# traz status_code). APITimeoutError é subclasse de APIConnectionError: vem antes.
_ORDEM_EXCECOES = (
    ("RateLimitError", 429),
    ("AuthenticationError", 401),
    ("PermissionDeniedError", 403),
    ("NotFoundError", 404),
    ("RequestTooLargeError", 413),
    ("UnprocessableEntityError", 422),
    ("BadRequestError", 400),
    ("OverloadedError", 529),
    ("InternalServerError", 500),
    ("APIStatusError", None),
    ("APITimeoutError", 504),
    ("APIConnectionError", 502),
)

# 21/09/2026 (revisão — custo/wire): o que certamente NÃO foi cobrado quando a recusa chega ANTES do
# stream. Status documentados como recusa sem processamento [KNOWN — shared/error-codes.md] e as
# recusas LOCAIS deste módulo (nada saiu da máquina). Ficam FORA, de propósito: 500 api_error, 504
# (tempo esgotado esperando o cabeçalho: a Anthropic pode ter processado o prefixo — [PLAUSIBLE, não
# documentado]) e 502 (conexão caída depois de enviar) — esses ficam na reserva e são liquidados
# pela estimativa, do lado caro, como a casa faz na OpenAI.
STATUS_SEM_COBRANCA = frozenset({400, 401, 402, 403, 404, 413, 422, 429, 529})
CODIGOS_SEM_COBRANCA = frozenset({"claude_sdk_ausente", "claude_erro_local", "claude_conexao",
                                  "claude_atlas_integral"})
# a falha foi na CONEXÃO (DNS, TLS, recusada, fila do pool): o pedido não chegou à Anthropic. Nomes
# das exceções do httpx que o SDK encadeia em APIConnectionError/APITimeoutError (`raise … from err`)
_FALHAS_DE_CONEXAO = frozenset({"ConnectError", "ConnectTimeout", "PoolTimeout"})


def recusa_sem_cobranca(status, codigo=""):
    """True quando uma recusa ANTES do stream (status ≠ 200 devolvido por post_como_openai)
    certamente não foi cobrada — o servidor libera a reserva. False = fica na reserva."""
    try:
        status = int(status or 0)
    except (TypeError, ValueError):
        status = 0
    return status in STATUS_SEM_COBRANCA or str(codigo or "") in CODIGOS_SEM_COBRANCA


def _falhou_ao_conectar(exc):
    """A cadeia de causas da exceção do SDK termina numa falha de CONEXÃO do httpx?"""
    visto, n = exc, 0
    while visto is not None and n < 8:
        visto = getattr(visto, "__cause__", None) or getattr(visto, "__context__", None)
        n += 1
        if visto is not None and any(c.__name__ in _FALHAS_DE_CONEXAO for c in type(visto).__mro__):
            return True
    return False


def _log(texto):
    print("[claude] " + _mascarar(texto), flush=True)


def _mascarar(texto):
    """A mesma regra de iald_motores.mascarar (cobre sk-ant-…), sem importá-lo."""
    return re.sub(r"sk-[A-Za-z0-9_\-*]{4,}", "sk-***", str(texto or ""))


_AVISADOS = set()
_TRAVA_AVISOS = threading.Lock()


def _avisar_uma_vez(chave, texto):
    with _TRAVA_AVISOS:
        if chave in _AVISADOS:
            return
        _AVISADOS.add(chave)
    _log("AVISO: " + texto)


def _campo(obj, nome, padrao=None):
    """Lê um campo de dict (cliente falso, JSON) ou de objeto (modelos do SDK)."""
    if obj is None:
        return padrao
    if isinstance(obj, dict):
        return obj.get(nome, padrao)
    return getattr(obj, nome, padrao)


def _inteiro(v):
    try:
        return max(int(v or 0), 0)
    except (TypeError, ValueError):
        return 0


# ══════════════════════════════════════════════════════════════
# O SDK E O CLIENTE
# ══════════════════════════════════════════════════════════════
_SDK_INJETADO = None
_FABRICA = None
_CLIENTES = {}
_TRAVA_CLIENTES = threading.Lock()


def definir_sdk(modulo):
    """Para os testes: um módulo com as exceções do SDK (None = o `anthropic` instalado)."""
    global _SDK_INJETADO
    _SDK_INJETADO = modulo


def _sdk():
    if _SDK_INJETADO is not None:
        return _SDK_INJETADO
    import anthropic                  # noqa: PLC0415 — preguiçoso de propósito
    return anthropic


def _sdk_ou_none():
    try:
        return _sdk()
    except ImportError:
        return None


def definir_fabrica_cliente(fabrica):
    """Troca quem cria o cliente: `fabrica(cfg)` → objeto com .messages.stream(...) e
    .messages.count_tokens(...). None volta ao anthropic.Anthropic real. Esvazia o cache."""
    global _FABRICA
    with _TRAVA_CLIENTES:
        _FABRICA = fabrica
        _CLIENTES.clear()


def _tempo_limite(valor, sdk=None):
    """float (leitura), (conexão, leitura) ou None → anthropic.Timeout(leitura, connect=…).
    A leitura nunca fica abaixo de TIMEOUT_LEITURA_MINIMO (o prefill frio do prefixo)."""
    conexao, leitura = TIMEOUT_CONEXAO, TIMEOUT_LEITURA_PADRAO
    try:
        if isinstance(valor, (tuple, list)) and len(valor) == 2:
            conexao, leitura = float(valor[0]), float(valor[1])
        elif valor is not None:
            leitura = float(valor)
            conexao = min(TIMEOUT_CONEXAO, leitura)
    except (TypeError, ValueError):
        conexao, leitura = TIMEOUT_CONEXAO, TIMEOUT_LEITURA_PADRAO
    leitura = max(leitura, TIMEOUT_LEITURA_MINIMO)
    Timeout = getattr(sdk if sdk is not None else _sdk_ou_none(), "Timeout", None)
    if Timeout is not None:
        try:
            return Timeout(leitura, connect=conexao)
        except Exception:             # noqa: BLE001
            pass
    return leitura


def cliente_para(cfg):
    """O cliente do SDK para esta configuração (um por chave e prazo, reaproveitado)."""
    if _FABRICA is not None:
        return _FABRICA(cfg)
    chave = str(getattr(cfg, "chave", "") or "")
    sdk = _sdk()
    prazo = getattr(cfg, "timeout", None)
    marca = hashlib.sha256(chave.encode("utf-8")).hexdigest() + "|" + repr(prazo)
    with _TRAVA_CLIENTES:
        cliente = _CLIENTES.get(marca)
        if cliente is None:
            cliente = sdk.Anthropic(api_key=chave, max_retries=MAX_RETRIES,
                                    timeout=_tempo_limite(prazo if prazo else None, sdk))
            _CLIENTES[marca] = cliente
        return cliente


def _com_prazo(cliente, timeout):
    if timeout is None or not callable(getattr(cliente, "with_options", None)):
        return cliente
    return cliente.with_options(timeout=_tempo_limite(timeout))


# ══════════════════════════════════════════════════════════════
# O ESTADO DE UM PEDIDO (o pensamento que volta na volta seguinte)
# ══════════════════════════════════════════════════════════════
class EstadoClaude:
    """Estado de UM pedido do app (todas as voltas do agente). Guarda os blocos brutos do
    assistente (texto, pensamento com assinatura, tool_use) de cada volta que parou em
    `tool_use`, pela lista de ids de tool_use — para a volta seguinte mandá-los INTACTOS.
    Guarda todas as voltas do pedido (não só a última): o histórico reenviado fica igual a si
    mesmo de uma chamada para a outra, e o prefixo da conversa que o cache AUTOMÁTICO do pedido
    (cache_control de topo, ver converter_pedido) gravou numa volta é lido na seguinte.
    ⚠ CORREÇÃO AO LADO (21/09/2026, revisão): a frase de antes ("o cache das mensagens não quebra
    no meio do loop") não tinha cache de mensagens por trás — só o sistema tinha marca. Agora tem.

    `ids_invalidos` (21/09/2026, revisão): tool_use cujo JSON acumulado não validou. O servidor
    pergunta entrada_invalida(id) ANTES de rodar a ferramenta — e não roda; converter_pedido manda
    o tool_result desse id com is_error."""

    def __init__(self):
        self._trava = threading.Lock()
        self._voltas = {}             # id de tool_use → (ids da volta, em ordem; blocos)
        self.ids_invalidos = set()    # tool_use cujo JSON não validou (input virou {}; NÃO roda)
        self.ultima_parada = None
        self.ultimo_uso = None
        self.id_mensagem = ""
        self.recusou = False

    def marcar_invalidos(self, ids):
        with self._trava:
            self.ids_invalidos.update(str(i) for i in ids or () if i)

    def entrada_invalida(self, ident):
        """True se o tool_use `ident` chegou com JSON que não valida (a ferramenta não deve rodar)."""
        with self._trava:
            return str(ident or "") in self.ids_invalidos

    def guardar(self, blocos):
        blocos = copy.deepcopy([b for b in blocos or [] if isinstance(b, dict)])
        ids = tuple(str(b.get("id")) for b in blocos if b.get("type") == "tool_use" and b.get("id"))
        if not ids:
            return
        with self._trava:
            for i in ids:
                self._voltas[i] = (ids, blocos)

    def blocos_para(self, ids):
        """Os blocos brutos da volta cujos tool_use têm exatamente estes ids; None se não há."""
        ids = tuple(str(i) for i in ids or () if i)
        if not ids:
            return None
        with self._trava:
            achado = self._voltas.get(ids[0])
        if achado is None or set(achado[0]) != set(ids):
            return None
        return copy.deepcopy(achado[1])

    def registrar_fim(self, parada, uso, id_mensagem):
        with self._trava:
            self.ultima_parada, self.ultimo_uso, self.id_mensagem = parada, uso, id_mensagem or ""
            if parada == "refusal":
                self.recusou = True

    def __len__(self):
        with self._trava:
            return len({v[0] for v in self._voltas.values()})


# ══════════════════════════════════════════════════════════════
# O PEDIDO: OpenAI Chat Completions → Anthropic Messages
# ══════════════════════════════════════════════════════════════
def _texto(conteudo):
    if conteudo is None:
        return ""
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        partes = []
        for p in conteudo:
            if isinstance(p, str):
                partes.append(p)
            elif isinstance(p, dict) and isinstance(p.get("text"), str):
                partes.append(p["text"])
        return "\n".join(partes)
    return str(conteudo)


def _marca_cache(cfg):
    ttl = str(getattr(cfg, "cache_ttl", "") or "5m").strip().lower()
    if ttl == "1h":
        return {"type": "ephemeral", "ttl": "1h"}
    if ttl != "5m":
        _avisar_uma_vez("ttl:" + ttl, f"cache_ttl desconhecido ({ttl!r}); usando 5m")
    return {"type": "ephemeral"}


def _blocos_de_sistema(texto, prefixo, marca):
    """A primeira mensagem developer/system: [prefixo COM cache_control] + [resto SEM marca]."""
    if not texto or not texto.strip():
        return []
    if prefixo and texto.startswith(prefixo):
        blocos = [{"type": "text", "text": prefixo, "cache_control": dict(marca)}]
        resto = texto[len(prefixo):]
        if resto.strip():
            blocos.append({"type": "text", "text": resto.lstrip("\r\n")})
        return blocos
    if prefixo:
        _avisar_uma_vez("prefixo-fora", "a mensagem de sistema não começa pelo prefixo recebido; "
                                        "vai inteira num bloco só, com cache_control")
    return [{"type": "text", "text": texto, "cache_control": dict(marca)}]


_ASSINATURAS_DE_IMAGEM = ((b"\xff\xd8\xff", "image/jpeg"), (b"\x89PNG\r\n\x1a\n", "image/png"),
                          (b"GIF87a", "image/gif"), (b"GIF89a", "image/gif"))


def _tipo_pelos_bytes(dados_b64):
    """O tipo da imagem pelos primeiros BYTES (não pelo rótulo do data: URI); None se não for um
    dos quatro que a API aceita. 21/09/2026 (revisão)."""
    cabeca = re.sub(r"\s+", "", str(dados_b64 or "")[:64])[:24]
    try:
        bruto = base64.b64decode(cabeca + "=" * (-len(cabeca) % 4))
    except (ValueError, binascii.Error):
        return None
    for assinatura, tipo in _ASSINATURAS_DE_IMAGEM:
        if bruto.startswith(assinatura):
            return tipo
    if bruto[:4] == b"RIFF" and bruto[8:12] == b"WEBP":
        return "image/webp"
    return None


def _marcador_de_imagem(motivo):
    _avisar_uma_vez("imagem:" + motivo.split(" (")[0], "imagem não enviada ao Claude: " + motivo)
    return {"type": "text", "text": f"[imagem anexada não enviada ao Claude: {motivo}]"}


def _imagem(url):
    """21/09/2026 (revisão): o bloco de imagem, ou um MARCADOR de texto quando a API recusaria o
    pedido inteiro por causa dela (tipo fora de jpeg/png/gif/webp — image/jpg e rótulo trocado são
    corrigidos pelos bytes —, ou acima de TETO_IMAGEM_BASE64). Antes o tipo do rótulo passava cru."""
    url = str(url or "")
    m = re.match(r"^data:([^;,]+);base64,(.*)$", url, re.S)
    if m:
        declarado = m.group(1).strip().lower()
        dados = m.group(2).strip()
        real = _tipo_pelos_bytes(dados)
        if real is None:
            return _marcador_de_imagem(f"formato não aceito pelo Claude ({declarado}; aceitos: JPEG, PNG, GIF, WebP)")
        if len(dados) > TETO_IMAGEM_BASE64:
            return _marcador_de_imagem(f"imagem acima de {TETO_IMAGEM_BASE64 // 1_000_000} MB em base64")
        return {"type": "image", "source": {"type": "base64", "media_type": real, "data": dados}}
    if url.startswith("https://") or url.startswith("http://"):
        return {"type": "image", "source": {"type": "url", "url": url}}
    return _marcador_de_imagem("formato de imagem não reconhecido (esperado data:…;base64 ou http(s))")


def _limitar_imagens(mensagens):
    """Teto de imagens do PEDIDO (TETO_IMAGENS_BASE64): da mais nova para a mais antiga; o que
    passar vira marcador. O app reenvia as imagens do histórico, então é aqui que o pedido de 32 MB
    da API seria furado. 21/09/2026 (revisão)."""
    total = 0
    for m in reversed(mensagens):
        blocos = m.get("content")
        if not isinstance(blocos, list):
            continue
        for i in range(len(blocos) - 1, -1, -1):
            b = blocos[i]
            fonte = b.get("source") if isinstance(b, dict) and b.get("type") == "image" else None
            if not isinstance(fonte, dict) or fonte.get("type") != "base64":
                continue
            total += len(str(fonte.get("data") or ""))
            if total > TETO_IMAGENS_BASE64:
                blocos[i] = _marcador_de_imagem(
                    f"as imagens desta conversa passam de {TETO_IMAGENS_BASE64 // 1_000_000} MB por pedido")
    return mensagens


def _conteudo_usuario(conteudo):
    if conteudo is None:
        return []
    if isinstance(conteudo, str):
        return [{"type": "text", "text": conteudo}] if conteudo.strip() else []
    blocos = []
    for p in conteudo if isinstance(conteudo, list) else [conteudo]:
        if isinstance(p, str):
            if p.strip():
                blocos.append({"type": "text", "text": p})
            continue
        if not isinstance(p, dict):
            continue
        tipo = p.get("type")
        if tipo in ("text", "input_text"):
            if isinstance(p.get("text"), str) and p["text"].strip():
                blocos.append({"type": "text", "text": p["text"]})
        elif tipo == "image_url":
            fonte = p.get("image_url")
            img = _imagem(fonte.get("url") if isinstance(fonte, dict) else fonte)
            if img:
                blocos.append(img)
        else:
            _avisar_uma_vez("parte:" + str(tipo), f"parte de conteúdo {tipo!r} sem tradução — ignorada")
    return blocos


def _entrada(argumentos):
    if isinstance(argumentos, dict):
        return copy.deepcopy(argumentos)
    if isinstance(argumentos, str) and argumentos.strip():
        try:
            valor = json.loads(argumentos)
        except (ValueError, TypeError):
            return {}
        return valor if isinstance(valor, dict) else {}
    return {}


def _conteudo_assistente(m, estado):
    chamadas = [c for c in (m.get("tool_calls") or []) if isinstance(c, dict)]
    if chamadas and estado is not None:
        brutos = estado.blocos_para([c.get("id") for c in chamadas])
        if brutos:
            return brutos            # pensamento com assinatura, texto e tool_use, intactos
    blocos = []
    texto = _texto(m.get("content"))
    if texto.strip():
        blocos.append({"type": "text", "text": texto})
    for c in chamadas:
        fn = c.get("function") if isinstance(c.get("function"), dict) else {}
        nome, ident = fn.get("name"), c.get("id")
        if not nome or not ident:
            continue
        blocos.append({"type": "tool_use", "id": str(ident), "name": str(nome),
                       "input": _entrada(fn.get("arguments"))})
    return blocos


def _reparar(mensagens):
    """O mínimo para a API aceitar: papéis alternados, começa e termina pelo usuário, e
    tool_result só logo depois do tool_use correspondente (e antes do texto)."""
    fundidas = []
    for m in mensagens:
        if not m["content"]:
            continue
        if fundidas and fundidas[-1]["role"] == m["role"]:
            fundidas[-1]["content"].extend(m["content"])
        else:
            fundidas.append({"role": m["role"], "content": list(m["content"])})
    while fundidas and fundidas[0]["role"] != "user":
        _log("a conversa começava pelo assistente; mensagem inicial do assistente descartada")
        fundidas.pop(0)
    while fundidas and fundidas[-1]["role"] != "user":
        # o Sonnet 5 recusa prefill do assistente (400) [KNOWN — skill, migração Sonnet 5]
        _log("a conversa terminava no assistente; última mensagem do assistente descartada")
        fundidas.pop()
    for j, m in enumerate(fundidas):
        if m["role"] != "user":
            continue
        anteriores = set()
        if j > 0 and fundidas[j - 1]["role"] == "assistant":
            anteriores = {b.get("id") for b in fundidas[j - 1]["content"]
                          if isinstance(b, dict) and b.get("type") == "tool_use"}
        resultados, outros = [], []
        for b in m["content"]:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                if b.get("tool_use_id") in anteriores:
                    resultados.append(b)
                else:
                    _log(f"tool_result sem tool_use correspondente ({b.get('tool_use_id')!r}); vai como texto")
                    outros.append({"type": "text", "text": f"[resultado de ferramenta {b.get('tool_use_id')}]\n"
                                                           + _texto(b.get("content"))})
            else:
                outros.append(b)
        m["content"] = resultados + outros
    return fundidas


def converter_ferramentas(ferramentas):
    """{"type":"function","function":{name,description,parameters}} → {name, description,
    input_schema, eager_input_streaming}, NA MESMA ORDEM (determinismo = cache)."""
    saida = []
    for t in ferramentas or []:
        if not isinstance(t, dict):
            continue
        fn = t.get("function")
        if isinstance(fn, dict):
            nome, descricao, parametros = fn.get("name"), fn.get("description"), fn.get("parameters")
        elif t.get("name"):
            nome, descricao, parametros = t.get("name"), t.get("description"), t.get("input_schema")
        else:
            continue
        if not nome:
            continue
        esquema = parametros if isinstance(parametros, dict) and parametros else {"type": "object", "properties": {}}
        if "type" not in esquema:
            esquema = {"type": "object", **esquema}
        d = {"name": str(nome)}
        if descricao:
            d["description"] = str(descricao)
        d["input_schema"] = copy.deepcopy(esquema)
        # padrão da skill para stream + ferramentas do cliente; sem validação no servidor, o JSON
        # acumulado é validado aqui no fim de cada bloco (ver _Fluxo)
        d["eager_input_streaming"] = True
        saida.append(d)
    return saida


def _escolha_de_ferramenta(escolha):
    if escolha is None:
        return None
    if isinstance(escolha, str):
        return {"auto": {"type": "auto"}, "none": {"type": "none"},
                "required": {"type": "any"}}.get(escolha.strip().lower())
    if isinstance(escolha, dict):
        fn = escolha.get("function") if isinstance(escolha.get("function"), dict) else {}
        if escolha.get("type") == "function" and fn.get("name"):
            return {"type": "tool", "name": str(fn["name"])}
    return None


def _modelo(cfg, payload):
    pedido = payload.get("model") if isinstance(payload, dict) else None
    if isinstance(pedido, str) and pedido.startswith("claude"):
        return pedido
    padrao = str(getattr(cfg, "modelo", "") or MODELO_PADRAO)
    if pedido:
        _avisar_uma_vez("modelo:" + str(pedido), f"payload com modelo {pedido!r} (não Claude); usando {padrao}")
    return padrao


def _max_tokens(cfg, payload):
    for nome in ("max_completion_tokens", "max_tokens"):
        try:
            n = int(payload.get(nome))
        except (TypeError, ValueError):
            continue
        if n > 0:
            return n
    return _inteiro(getattr(cfg, "max_saida", 0)) or 4096


def _esforco(cfg):
    esforco = str(getattr(cfg, "esforco_claude", "") or ESFORCO_PADRAO).strip().lower()
    if esforco not in ESFORCOS_CLAUDE:
        _avisar_uma_vez("esforco:" + esforco, f"esforco_claude inválido ({esforco!r}); usando {ESFORCO_PADRAO}")
        return ESFORCO_PADRAO
    return esforco


def converter_pedido(cfg, payload, *, prefixo="", estado=None):
    """Função pura: payload OpenAI → kwargs de client.messages.stream(...).

    Só sai o que a Anthropic entende: stream_options, store, reasoning_effort, prompt_cache_key,
    temperature, top_p, top_k, n e o resto do que é só da OpenAI ficam para trás.
    Levanta ValueError quando não sobra mensagem do usuário para enviar."""
    if not isinstance(payload, dict):
        raise ValueError("o payload precisa ser um dicionário")
    marca = _marca_cache(cfg)
    sistema, extras, conversa, viu_sistema = [], [], [], False
    for m in payload.get("messages") or []:
        if not isinstance(m, dict):
            continue
        papel = m.get("role")
        if papel in ("system", "developer"):
            texto = _texto(m.get("content"))
            if not viu_sistema:
                viu_sistema = True
                sistema = _blocos_de_sistema(texto, prefixo, marca)
            elif texto.strip():
                extras.append({"type": "text", "text": texto})       # sempre DEPOIS do bloco em cache
            continue
        if papel == "user":
            conversa.append({"role": "user", "content": _conteudo_usuario(m.get("content"))})
        elif papel == "assistant":
            conversa.append({"role": "assistant", "content": _conteudo_assistente(m, estado)})
        elif papel in ("tool", "function"):
            bloco = {"type": "tool_result", "tool_use_id": str(m.get("tool_call_id") or "")}
            texto = _texto(m.get("content"))
            if texto:
                bloco["content"] = texto
            if estado is not None and estado.entrada_invalida(bloco["tool_use_id"]):
                # 21/09/2026 (revisão): a ferramenta não rodou (JSON inválido); o servidor mandou o
                # bruto como {"INVALID_JSON": …} e aqui ele volta ao Claude como ERRO, para refazer
                bloco["is_error"] = True
            conversa.append({"role": "user", "content": [bloco]})
        else:
            _avisar_uma_vez("papel:" + str(papel), f"papel {papel!r} sem tradução — mensagem ignorada")
    mensagens = _limitar_imagens(_reparar(conversa))
    if not mensagens:
        raise ValueError("não há mensagem do usuário para enviar ao Claude")

    kwargs = {"model": _modelo(cfg, payload), "max_tokens": _max_tokens(cfg, payload)}
    if sistema or extras:
        kwargs["system"] = sistema + extras
    kwargs["messages"] = mensagens
    ferramentas = converter_ferramentas(payload.get("tools"))
    if ferramentas:
        kwargs["tools"] = ferramentas
        escolha = _escolha_de_ferramenta(payload.get("tool_choice"))
        if escolha:
            kwargs["tool_choice"] = escolha
    kwargs["thinking"] = {"type": "adaptive"}
    kwargs["output_config"] = {"effort": _esforco(cfg)}
    if payload.get("safety_identifier"):
        kwargs["metadata"] = {"user_id": str(payload["safety_identifier"])[:256]}
    # 21/09/2026 (revisão — wire/custo): cache AUTOMÁTICO da cauda (último bloco que aceita cache;
    # avança com a conversa). Sem ele, cada volta do agente e cada mensagem nova pagavam o histórico
    # inteiro (resultados canônicos de até ~20 mil caracteres, pensamento reenviado) sem cache. 5 min
    # sempre: vem depois da marca do prefixo (5 min ou 1 h), e "1 h antes de 5 min" é a regra
    # [KNOWN — skill, shared/prompt-caching.md]. Ocupa 1 dos 4 lugares de marca (o prefixo, o outro).
    kwargs["cache_control"] = {"type": "ephemeral"}
    return kwargs


# ══════════════════════════════════════════════════════════════
# ERROS: Anthropic → corpo OpenAI
# ══════════════════════════════════════════════════════════════
def codigo_openai(status, tipo, mensagem, detalhes=None, corpo=None):
    """(status, code) no vocabulário que o pipeline lê. As frases do corpo são do provedor
    (crédito esgotado não é documentado: 402 billing_error ou 400 "credit balance" [INFERRED])."""
    tipo = str(tipo or "")
    status = _inteiro(status)
    if status in (0, 200):
        status = STATUS_POR_TIPO.get(tipo, 500)
    texto = str(mensagem or "").lower()
    bruto = json.dumps(corpo, ensure_ascii=False, default=str) if corpo is not None else ""
    detalhe = str(_campo(detalhes, "error_code", "") or "") if isinstance(detalhes, dict) else ""
    if status == 402 or tipo == "billing_error" or (status == 400 and "credit balance" in texto):
        return status, "claude_sem_credito"
    if (status == 400 and "specified api usage limits" in texto) or (
            status == 429 and (detalhe == "enforced_spend_limit_reached"
                               or "enforced_spend_limit_reached" in texto
                               or "enforced_spend_limit_reached" in bruto)):
        return status, "claude_limite_de_gasto"
    if status == 400 and "prompt is too long" in texto:
        return status, "context_length_exceeded"
    if status == 529 or tipo == "overloaded_error":
        return 529, "overloaded"
    if status in MAPA_ERROS:
        return status, MAPA_ERROS[status]
    return status, (tipo or f"http_{status}")


def _cabecalhos(cab):
    if not cab:
        return {}
    try:
        itens = cab.items()
    except AttributeError:
        return {}
    return {str(k).lower(): str(v) for k, v in itens}


def _corpo_de_erro(status, tipo, mensagem, detalhes=None, corpo=None):
    status, codigo = codigo_openai(status, tipo, mensagem, detalhes, corpo)
    return status, {"error": {"code": codigo, "type": str(tipo or codigo), "param": None,
                              "message": _mascarar(mensagem)[:1000]}}


def erro_openai(status, tipo, mensagem, headers=None, detalhes=None, corpo=None):
    """A resposta NÃO-200 (cara de requests.Response) com corpo {"error": {code, type, message}}.
    Os cabeçalhos do provedor seguem (retry-after incluído)."""
    status, corpo_openai = _corpo_de_erro(status, tipo, mensagem, detalhes, corpo)
    cab = _cabecalhos(headers)
    cab["content-type"] = "application/json"
    return RespostaClaude(status, cab, corpo=json.dumps(corpo_openai, ensure_ascii=False).encode("utf-8"))


def _classificar_excecao(exc):
    """(status, tipo, mensagem, cabeçalhos, detalhes, corpo) pelas exceções TIPADAS do SDK
    (a mais específica primeiro); None quando não é exceção do SDK."""
    sdk = _sdk_ou_none()
    if sdk is None:
        return None
    for nome, status_base in _ORDEM_EXCECOES:
        classe = getattr(sdk, nome, None)
        if not isinstance(classe, type) or not isinstance(exc, classe):
            continue
        if nome in ("APITimeoutError", "APIConnectionError") and _falhou_ao_conectar(exc):
            # 21/09/2026 (revisão): DNS, TLS, conexão recusada ou fila do pool — depois das 2
            # tentativas do SDK o pedido NÃO chegou à Anthropic: 503 próprio, reserva liberada.
            # (Antes: 502, que o servidor trata como "no meio, talvez cobrado" e liquidava pela
            # estimativa cheia — ~US$ 1,4 por falha contra o teto de US$ 5 do dia.)
            return 503, "claude_conexao", "não foi possível conectar à Anthropic (nada foi enviado)", {}, {}, None
        if nome == "APITimeoutError":
            return 504, "timeout_error", "tempo esgotado falando com a Anthropic", {}, {}, None
        if nome == "APIConnectionError":
            return 502, "api_connection_error", "falha de conexão com a Anthropic", {}, {}, None
        corpo = _campo(exc, "body")
        erro = corpo.get("error") if isinstance(corpo, dict) and isinstance(corpo.get("error"), dict) else {}
        tipo = erro.get("type") or (exc.type if isinstance(getattr(exc, "type", None), str) else "")
        mensagem = erro.get("message") or getattr(exc, "message", "") or str(exc)
        status = _inteiro(getattr(exc, "status_code", 0)) or (status_base or 0)
        if status in (0, 200):        # erro no meio do stream (depois do HTTP 200)
            status = STATUS_POR_TIPO.get(tipo, status_base or 500)
        detalhes = erro.get("details") if isinstance(erro.get("details"), dict) else {}
        cab = _cabecalhos(getattr(getattr(exc, "response", None), "headers", None))
        return status, tipo, mensagem, cab, detalhes, corpo
    return None


def _resposta_de_excecao(exc):
    classe = _classificar_excecao(exc)
    if classe is None:
        _log(f"falha local antes do stream: {type(exc).__name__}: {exc}")
        return erro_openai(500, "claude_erro_local", f"{type(exc).__name__}: {exc}")
    status, tipo, mensagem, cab, detalhes, corpo = classe
    resposta = erro_openai(status, tipo, mensagem, cab, detalhes, corpo)
    _log(f"HTTP {resposta.status_code} {tipo or '-'}: {mensagem}")
    return resposta


# ══════════════════════════════════════════════════════════════
# A RESPOSTA COM CARA DE requests.Response
# ══════════════════════════════════════════════════════════════
class RespostaClaude:
    """O que o pipeline consome: status_code, headers, text/content/json, iter_lines,
    iter_content, close. Com `linhas`, é o stream (uma leitura só); sem, o corpo pronto."""

    def __init__(self, status_code, headers=None, corpo=b"", linhas=None, fechar=None):
        self.status_code = int(status_code)
        self.headers = _cabecalhos(headers)
        self.encoding = "utf-8"
        self.reason = "OK" if self.status_code == 200 else "Error"
        self.closed = False
        self._corpo = None if linhas is not None else (corpo or b"")
        self._linhas = linhas
        self._consumido = False
        self._fechar = fechar
        self._trava = threading.Lock()

    @property
    def ok(self):
        return self.status_code < 400

    def _fonte(self):
        with self._trava:
            if self._consumido:
                return iter(())
            self._consumido = True
        if self._linhas is not None:
            return self._linhas
        return iter([linha for linha in self._corpo.split(b"\n") if linha.strip()])

    def iter_lines(self, chunk_size=None, decode_unicode=False, delimiter=None):
        for linha in self._fonte():
            yield linha.decode("utf-8", "replace") if decode_unicode else linha

    def iter_content(self, chunk_size=1, decode_unicode=False):
        if self._linhas is None:
            corpo = self.content
            passo = max(int(chunk_size or len(corpo) or 1), 1)
            for i in range(0, len(corpo), passo):
                pedaco = corpo[i:i + passo]
                yield pedaco.decode("utf-8", "replace") if decode_unicode else pedaco
            return
        for linha in self.iter_lines():
            pedaco = linha + b"\n\n"
            yield pedaco.decode("utf-8", "replace") if decode_unicode else pedaco

    @property
    def content(self):
        if self._corpo is None:
            self._corpo = b"".join(linha + b"\n\n" for linha in self.iter_lines())
        return self._corpo

    @property
    def text(self):
        return self.content.decode("utf-8", "replace")

    def json(self):
        return json.loads(self.content)

    def close(self):
        self.closed = True
        with self._trava:
            fn, self._fechar = self._fechar, None
        if fn is not None:
            try:
                fn()
            except Exception:         # noqa: BLE001 — fechar nunca derruba quem consome
                pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False

    def __repr__(self):
        return f"<RespostaClaude [{self.status_code}]>"


# ══════════════════════════════════════════════════════════════
# O STREAM: eventos Anthropic → pedaços chat.completion.chunk
# ══════════════════════════════════════════════════════════════
def normalizar_uso(usage):
    """usage da Anthropic → usage da OpenAI. `input_tokens` da Anthropic é só o resto fora do
    cache [KNOWN — prompt-caching.md]: prompt_tokens = entrada + escrita + leitura do cache."""
    entrada = _inteiro(_campo(usage, "input_tokens"))
    escrita = _inteiro(_campo(usage, "cache_creation_input_tokens"))
    leitura = _inteiro(_campo(usage, "cache_read_input_tokens"))
    saida = _inteiro(_campo(usage, "output_tokens"))
    prompt = entrada + escrita + leitura
    uso = {"prompt_tokens": prompt, "completion_tokens": saida, "total_tokens": prompt + saida,
           "prompt_tokens_details": {"cached_tokens": leitura, "cache_write_tokens": escrita}}
    pensamento = _campo(_campo(usage, "output_tokens_details"), "thinking_tokens")
    if pensamento is not None:
        uso["completion_tokens_details"] = {"reasoning_tokens": _inteiro(pensamento)}
    return uso


def _bloco_dict(bloco):
    if isinstance(bloco, dict):
        d = dict(bloco)
    elif callable(getattr(bloco, "to_dict", None)):
        d = bloco.to_dict()
    elif callable(getattr(bloco, "model_dump", None)):
        d = bloco.model_dump()
    else:
        d = dict(vars(bloco))
    d = {k: v for k, v in d.items() if v is not None and not str(k).startswith("_")}
    return json.loads(json.dumps(d, ensure_ascii=False, default=lambda o: _bloco_dict(o)))


class _Fluxo:
    def __init__(self, gerente, stream, estado, modelo):
        self.gerente, self.stream, self.estado = gerente, stream, estado
        self.id_msg, self.modelo = "", modelo
        self.cancelado = False
        self._encerrado = False
        self._trava = threading.Lock()

    def encerrar(self):
        with self._trava:
            if self._encerrado:
                return
            self._encerrado = True
        try:
            self.gerente.__exit__(None, None, None)
        except Exception:             # noqa: BLE001
            pass

    def cancelar(self):
        self.cancelado = True
        self.encerrar()

    def _linha(self, corpo):
        return b"data: " + json.dumps(corpo, ensure_ascii=False).encode("utf-8")

    def _pedaco(self, delta=None, fim=None):
        return self._linha({"id": self.id_msg, "object": "chat.completion.chunk", "model": self.modelo,
                            "choices": [{"index": 0, "delta": delta or {}, "finish_reason": fim}]})

    def _uso(self, uso):
        return self._linha({"id": self.id_msg, "object": "chat.completion.chunk", "model": self.modelo,
                            "choices": [], "usage": uso})

    def linhas(self):
        try:
            yield from self._traduzir()
        finally:
            self.encerrar()

    @staticmethod
    def _validar(bloco):
        """JSON acumulado da ferramenta (eager: o servidor não valida). Vazio = {}."""
        bruto = bloco.get("_json", "")
        if not bruto.strip():
            return True, {}
        try:
            valor = json.loads(bruto)
        except (ValueError, TypeError):
            return False, {}
        return (True, valor) if isinstance(valor, dict) else (False, {})

    def _invalida(self, bloco, invalidos, motivo):
        invalidos.add(bloco.get("id"))
        # 21/09/2026 (revisão): a ferramenta NÃO roda — o servidor consulta EstadoClaude.entrada_invalida
        _log(f"entrada JSON inválida na ferramenta {bloco.get('name')!r} ({bloco.get('id')}): {motivo}; "
             "a ferramenta não roda e o bruto volta ao Claude como erro (INVALID_JSON)")

    def _blocos_proprios(self, blocos, invalidos):
        """O que já veio, montado aqui (o stream morreu antes da mensagem final)."""
        saida = []
        for _, b in sorted(blocos.items()):
            t = b.get("type")
            if t == "text" and b.get("text"):
                saida.append({"type": "text", "text": b["text"]})
            elif t == "thinking" and b.get("signature"):
                saida.append({"type": "thinking", "thinking": b.get("thinking", ""), "signature": b["signature"]})
            elif t == "redacted_thinking" and b.get("data"):
                saida.append({"type": "redacted_thinking", "data": b["data"]})
            elif t == "tool_use":
                ok, valor = self._validar(b)
                if not ok and b.get("id") not in invalidos:
                    self._invalida(b, invalidos, "stream interrompido no meio da entrada")
                entrada = valor if ok and b.get("id") not in invalidos else {}
                saida.append({"type": "tool_use", "id": b.get("id"), "name": b.get("name"), "input": entrada})
        return saida

    def _traduzir(self):
        blocos, ferramentas, invalidos = {}, {}, set()
        try:
            for ev in self.stream:
                if self.cancelado:
                    return
                tipo = _campo(ev, "type")
                if tipo == "message_start":
                    msg = _campo(ev, "message")
                    self.id_msg = str(_campo(msg, "id") or self.id_msg)
                    self.modelo = str(_campo(msg, "model") or self.modelo)
                    yield self._pedaco({"role": "assistant", "content": ""})
                elif tipo == "content_block_start":
                    i, bloco = _campo(ev, "index"), _campo(ev, "content_block")
                    t = _campo(bloco, "type")
                    if t == "text":
                        blocos[i] = {"type": "text", "text": str(_campo(bloco, "text") or "")}
                        if blocos[i]["text"]:
                            yield self._pedaco({"content": blocos[i]["text"]})
                    elif t == "tool_use":
                        k = len(ferramentas)
                        ferramentas[i] = k
                        blocos[i] = {"type": "tool_use", "id": str(_campo(bloco, "id") or ""),
                                     "name": str(_campo(bloco, "name") or ""), "_json": ""}
                        yield self._pedaco({"tool_calls": [{"index": k, "id": blocos[i]["id"], "type": "function",
                                                            "function": {"name": blocos[i]["name"],
                                                                         "arguments": ""}}]})
                    elif t == "thinking":
                        blocos[i] = {"type": "thinking", "thinking": str(_campo(bloco, "thinking") or ""),
                                     "signature": str(_campo(bloco, "signature") or "")}
                    elif t == "redacted_thinking":
                        blocos[i] = {"type": "redacted_thinking", "data": _campo(bloco, "data")}
                    else:
                        blocos[i] = {"type": str(t)}
                elif tipo == "content_block_delta":
                    i, delta = _campo(ev, "index"), _campo(ev, "delta")
                    t, b = _campo(delta, "type"), blocos.get(i)
                    if b is None:
                        continue
                    if t == "text_delta":
                        pedaco = str(_campo(delta, "text") or "")
                        b["text"] = b.get("text", "") + pedaco
                        if pedaco:
                            yield self._pedaco({"content": pedaco})
                    elif t == "input_json_delta":
                        parcial = str(_campo(delta, "partial_json") or "")
                        b["_json"] = b.get("_json", "") + parcial
                        if parcial and i in ferramentas:
                            yield self._pedaco({"tool_calls": [{"index": ferramentas[i],
                                                                "function": {"arguments": parcial}}]})
                    elif t == "thinking_delta":         # guardado para o EstadoClaude, nunca emitido
                        b["thinking"] = b.get("thinking", "") + str(_campo(delta, "thinking") or "")
                    elif t == "signature_delta":
                        b["signature"] = b.get("signature", "") + str(_campo(delta, "signature") or "")
                elif tipo == "content_block_stop":
                    i = _campo(ev, "index")
                    b = blocos.get(i)
                    if b is not None and b.get("type") == "tool_use":
                        b["_parado"] = True
                        ok, _ = self._validar(b)
                        if not ok:
                            self._invalida(b, invalidos, "JSON não valida no fim do bloco")
                        elif not b["_json"].strip() and i in ferramentas:
                            # ferramenta sem argumentos: o pipeline recebe "{}" (JSON válido), não ""
                            yield self._pedaco({"tool_calls": [{"index": ferramentas[i],
                                                                "function": {"arguments": "{}"}}]})
                # "text", "input_json", "thinking", "signature", "citation" (eventos de conveniência
                # do SDK, repetem os deltas acima), message_delta, message_stop, ping: nada a emitir
            final = self.stream.get_final_message()
        except Exception as exc:      # noqa: BLE001 — nunca levanta para o pipeline
            if self.cancelado:
                return
            yield from self._falha_no_meio(exc, blocos, ferramentas, invalidos)
            return

        conteudo = [_bloco_dict(b) for b in (_campo(final, "content") or [])]
        for b in conteudo:
            if b.get("type") == "tool_use" and (b.get("id") in invalidos or not isinstance(b.get("input"), dict)):
                b["input"] = {}
        parada = _campo(final, "stop_reason")
        self.id_msg = str(_campo(final, "id") or self.id_msg)
        self.modelo = str(_campo(final, "model") or self.modelo)
        uso = normalizar_uso(_campo(final, "usage"))
        if self.estado is not None:
            # ANTES do fim e do [DONE]: quem consome sai no [DONE] e já monta a volta seguinte
            self.estado.marcar_invalidos(invalidos)
            if parada == "tool_use":
                self.estado.guardar(conteudo)
            self.estado.registrar_fim(parada, uso, self.id_msg)
        if parada == "refusal":
            _log(f"recusa do modelo (mensagem {self.id_msg}); a parte já enviada é retirada")
            # 21/09/2026 (revisão): o aviso RETIRA a parte já enviada (e ela não vai ao histórico)
            yield self._linha({"iald_aviso": {"tipo": "recusa", "texto": AVISO_RECUSA, "retirar_resposta": True}})
            yield self._pedaco({"content": NOTA_RECUSA})
        elif parada in NOTA_CORTE:
            # 21/09/2026 (revisão): o corte fica dito (antes: "length" calado, ou "(sem resposta)")
            _log(f"resposta cortada ({parada}; mensagem {self.id_msg})")
            yield self._pedaco({"content": NOTA_CORTE[parada]})
        yield self._pedaco({}, PARADA_PARA_FIM.get(parada, "stop"))
        yield self._uso(uso)
        yield b"data: [DONE]"

    def _falha_no_meio(self, exc, blocos, ferramentas, invalidos):
        ferramentas_abertas = [b for b in blocos.values() if b.get("type") == "tool_use"]
        aberta = bool(ferramentas_abertas)
        # ⚠ CORREÇÃO AO LADO (21/09/2026, revisão): antes, QUALQUER ValueError com um tool_use visto
        # virava uma volta "tool_calls" com argumentos {} — e a ferramenta rodava com entrada que o
        # Claude não mandou. O ValueError do SDK é o do JSON eager sem conserto [KNOWN — skill,
        # python streaming.md]: sem tool_use_id completo para responder, a skill manda refazer o
        # pedido; aqui ele vira LINHA DE ERRO (claude_entrada_invalida) e o pedido termina com o
        # motivo. Só vale para esse ValueError: JSONDecodeError/UnicodeDecodeError (do SSE) e bloco
        # de ferramenta já fechado ficam no caminho geral.
        eager = (isinstance(exc, ValueError)
                 and not isinstance(exc, (json.JSONDecodeError, UnicodeDecodeError))
                 and any(not b.get("_parado") for b in ferramentas_abertas)
                 and _classificar_excecao(exc) is None)
        if eager:
            for b in ferramentas_abertas:
                if not b.get("_parado") and b.get("id") not in invalidos:
                    self._invalida(b, invalidos, f"{type(exc).__name__}: {exc}")
            if self.estado is not None:
                self.estado.marcar_invalidos(invalidos)
            status, tipo, detalhes, corpo = 502, "claude_entrada_invalida", {}, None
            mensagem = f"o Claude gerou uma entrada de ferramenta que não é JSON ({type(exc).__name__}: {exc})"
        else:
            classe = _classificar_excecao(exc)
            if classe is None:
                status, tipo, mensagem, detalhes, corpo = 500, "claude_erro_local", f"{type(exc).__name__}: {exc}", {}, None
            else:
                status, tipo, mensagem, _cab, detalhes, corpo = classe
        if self.estado is not None and aberta:
            # a volta pode seguir no pipeline (agent_loop ignora a linha de erro): o que já veio
            # fica guardado para a chamada seguinte continuar válida
            self.estado.guardar(self._blocos_proprios(blocos, invalidos))
        _, corpo_openai = _corpo_de_erro(status, tipo, mensagem, detalhes, corpo)
        _log(f"erro no meio do stream ({self.id_msg or '-'}): {corpo_openai['error']['code']}: {mensagem}")
        yield self._linha(corpo_openai)
        yield b"data: [DONE]"


# ══════════════════════════════════════════════════════════════
# A PORTA: post_como_openai e contar_tokens
# ══════════════════════════════════════════════════════════════
def _leva_atlas_integral(payload, prefixo=""):
    """O prefixo ou alguma mensagem de sistema/developer traz a marca do Atlas integral?"""
    if MARCA_ATLAS_INTEGRAL in str(prefixo or ""):
        return True
    for m in (payload.get("messages") or []) if isinstance(payload, dict) else []:
        if isinstance(m, dict) and m.get("role") in ("system", "developer") and MARCA_ATLAS_INTEGRAL in _texto(m.get("content")):
            return True
    return False


def post_como_openai(cfg, payload, *, prefixo="", estado=None, timeout=None, cliente=None):
    """Envia o payload OpenAI à Anthropic e devolve a resposta com cara de requests.Response.

    NUNCA levanta por erro da API: antes do stream → status ≠ 200 com corpo OpenAI
    {"error": {code, type, message}}; no meio → linha {"error": {...}} e depois [DONE].
    `cfg`: .chave, .modelo, .esforco_claude ('high'), .cache_ttl ('5m'|'1h'), .max_saida,
    .timeout (opcional). `prefixo`: o texto TGL que abre a mensagem developer (vai em cache).
    `estado`: um EstadoClaude por pedido (obrigatório no loop do agente para o pensamento voltar).
    `timeout`: float ou (conexão, leitura). `cliente`: injeção direta (sem chave obrigatória)."""
    modelo = _modelo(cfg, payload if isinstance(payload, dict) else {})
    if cliente is None and not str(getattr(cfg, "chave", "") or ""):
        return erro_openai(401, "authentication_error", "IALD_CLAUDE_API_KEY ausente no servidor")
    if _leva_atlas_integral(payload, prefixo):
        # 21/09/2026 (revisão de segurança, ALTO): defesa em profundidade — o servidor já recusa o
        # claude em IALD_MEMORIA_MODO=atlas_integral; se o Atlas inteiro chegar aqui mesmo assim, nada sai
        _log("o prefixo leva o Atlas integral (§V/§VI/§X); nada enviado à Anthropic")
        return erro_openai(400, "claude_atlas_integral",
                           "o prompt leva o Atlas integral (com §V, §VI e §X); o Claude não recebe esse modo")
    try:
        kwargs = converter_pedido(cfg, payload, prefixo=prefixo, estado=estado)
    except Exception as exc:          # noqa: BLE001
        _log(f"pedido não convertível: {exc}")
        return erro_openai(400, "invalid_request_error", f"pedido não convertível para o Claude: {exc}")
    try:
        c = cliente if cliente is not None else cliente_para(cfg)
        c = _com_prazo(c, timeout)
    except ImportError:
        _avisar_uma_vez("sdk", "o pacote `anthropic` não está instalado neste Python")
        return erro_openai(503, "claude_sdk_ausente", "o SDK da Anthropic não está instalado no servidor")
    except Exception as exc:          # noqa: BLE001
        return _resposta_de_excecao(exc)
    try:
        gerente = c.messages.stream(**kwargs)
        stream = gerente.__enter__()
    except Exception as exc:          # noqa: BLE001 — erro da API antes do stream vira status ≠ 200
        return _resposta_de_excecao(exc)
    cab = _cabecalhos(getattr(getattr(stream, "response", None), "headers", None))
    cab.setdefault("content-type", "text/event-stream")
    fluxo = _Fluxo(gerente, stream, estado, modelo)
    return RespostaClaude(200, cab, linhas=fluxo.linhas(), fechar=fluxo.cancelar)


def contar_tokens(cfg, *, system, tools=None, messages=None):
    """Tokens Claude (POST /v1/messages/count_tokens, gratuito [KNOWN]) de system + tools +
    messages. Sem `messages`, uma mensagem mínima do usuário (a API exige uma). Levanta em erro."""
    sistema = system if isinstance(system, list) else [{"type": "text", "text": str(system)}]
    kwargs = {"model": _modelo(cfg, {}), "system": sistema,
              "messages": messages or [{"role": "user", "content": "."}]}
    ferramentas = [{k: v for k, v in t.items() if k != "eager_input_streaming"}
                   for t in converter_ferramentas(tools)]
    if ferramentas:
        kwargs["tools"] = ferramentas
    resposta = cliente_para(cfg).messages.count_tokens(**kwargs)
    return _inteiro(_campo(resposta, "input_tokens"))


__all__ = [
    "AVISO_RECUSA", "CODIGOS_SEM_COBRANCA", "EstadoClaude", "MAPA_ERROS", "MARCA_ATLAS_INTEGRAL",
    "MODELO_PADRAO", "NOTA_CORTE", "NOTA_RECUSA", "PARADA_PARA_FIM", "RespostaClaude",
    "STATUS_POR_TIPO", "STATUS_SEM_COBRANCA", "TIPOS_DE_IMAGEM", "cliente_para", "codigo_openai",
    "contar_tokens", "converter_ferramentas", "converter_pedido", "definir_fabrica_cliente",
    "definir_sdk", "erro_openai", "normalizar_uso", "post_como_openai", "recusa_sem_cobranca",
]
