# -*- coding: utf-8 -*-
r"""OS CONTRATOS QUE A GERENCIA DEVE AO KIMI, GERADOS POR SCRIPT (24/10/2026, sessao a7; nada digitado, todo campo lido do artefato).

Escreve em C:\IALD\Site\tgl\v3.0_bancada\central_extra\ (o montar_central_no_site.py copia essa pasta para o /central/ do site):
  organismo/index.html               copia byte a byte da fonte do Kimi (v3.0_bancada/organismo_publico/index.html); ausente = PARA
  organismo/ESTADO_DO_ORGANISMO.json o quadro do organismo SANEADO: mesmo esquema; nenhum caminho local (so o nome do arquivo);
                                     so os cinco campos por item; + publicado_em (ISO) e fonte; recusa se sobrar \Users\, rotol,
                                     token/senha/chave ou formato de credencial
  organismo/custodias.json           [{versao, pin16, selado_em, espelho_commit, central_commit, site_subida_em, publica_rodada,
                                     conferencia}], mais recente primeiro, para toda vNNN com pasta work/custodia_vNNN_*
  pensamentos/pensamentos.json       [{data, texto, url, fonte}] do LIVRO.jsonl + recibos da ORDEM 021 (so os de publicacao confirmada)
  arcos.json                         [{versao, data, pin16, en, pt}] (raiz; o montar NAO o copia ao site ate a gerencia decidir onde)
  MANIFESTO_CENTRAL_EXTRA.json       caminho, bytes e sha256 de cada saida (o montar tambem NAO o copia)
De onde vem cada campo (vale `null` quando o artefato nao existe; nunca se inventa):
  pin16        fatos_vNNN.json ou, na falta, CONFERENCIA_FINAL_vNNN.json (pin[:16]); os dois, se existirem, tem de concordar
  selado_em    fatos_vNNN.json (timestamp) > selo do cofre (vault/originals_copy/um_unificado_vNNN) > selo do espelho no commit da
               custodia (git show); so vale se o selo diz ser da versao (um_version) ou, sem esse campo, se a versao e a mais alta do commit
  commits      git log do espelho (the_boundary) e da Central: assunto que COMECA por `custodia(` e traz vNNN antes de ; / sementes / arco;
               havendo mais de um, vale o mais antigo (o da custodia; os de correcao vem depois)
  site_subida_em  1a subida do site com «SUBIDA VERIFICADA» cujo RELATORIO.md cita o manifesto manifesto_vNNN.json (hora do cabecalho)
  publica_rodada  `rodada <carimbo>: COMPLETA` em central_publica_vNNN*saida*.txt da pasta da custodia, se rodadas/<carimbo>.json ok
  conferencia  CONFERENCIA_FINAL_vNNN.json (ok/total)
  arcos        texto: o que o site mostra hoje (chaves art.c.cl.arcNNN do i18n.js, EN e PT); na falta, arco_vNNN_texto.json;
               pin16: arco_vNNN_texto.json (o pin16 do arquivo do v394 e do v394, nao do v393); data: a data do selo (ver selado_em)
Falha visivel: qualquer recusa PARA com rc 1 e NADA e gravado (o montar nao deve rodar com extras velhos).
Backup de bytes: o arquivo que vai mudar e copiado para work/central_publica_22out/central_extra_bak/<arq>.bak_<carimbo> (fora da
pasta de saida, que o montar copia). Escreve por temporario -> confere -> substitui. Registro local do que veio de onde:
work/central_publica_22out/central_extra_proveniencia.json (sem caminhos absolutos; so contagens e hashes curtos).
Limite conhecido da limpeza de caminhos: um caminho com espacos seguido de texto livre sem aspas pode levar junto as palavras do meio
(perde texto, nunca vaza caminho); o que sobrar de unidade/UNC/\Users\ derruba a geracao.
Uso: gerar_central_extra.py [--seco] [--saida PASTA] [--autoteste]"""
import argparse, hashlib, json, os, re, subprocess, sys, time, unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

W = Path(__file__).resolve().parent
CEN = Path(r"C:\IALD\Central de Patentes")
BANC = Path(r"C:\IALD\Site\tgl\v3.0_bancada")
SITE = Path(r"C:\IALD\Site\tgl\v3.0")
TB = Path(r"C:\IALD\Artigo\the_boundary")
SAIDA = BANC / "central_extra"
BAK = W / "central_extra_bak"
PROV = W / "central_extra_proveniencia.json"
ORG_HTML = BANC / "organismo_publico" / "index.html"
QUADRO = CEN / "organismo" / "ESTADO_DO_ORGANISMO.json"
LIVRO = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT" / "X_DIARIO" / "LIVRO.jsonl"
RECIBOS_X = CEN / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_021"
WORK = CEN / "work"
SUBIDAS = BANC / "subidas"
RODADAS = W / "rodadas"
REVISOES = BANC / "revisoes"
I18N = SITE / "i18n.js"
COFRE = CEN / "vault" / "originals_copy"
SELO_NO_ESPELHO = "Um (absoluto) \u2014 Grande Atrator/um_absoluto_selo.json"
FONTE_QUADRO = "tools/estado_do_organismo.py"
CINCO = ("superficie", "item", "esperado", "achado", "estado")
NAO_PUBLICA_NO_SITE = ("arcos.json", "MANIFESTO_CENTRAL_EXTRA.json")   # o montar le esta mesma decisao (ver montar_central_no_site.py)


class Recusa(Exception):
    """Falha visivel: a geracao PARA e nada e gravado."""


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ───────────────────────── caminhos locais e coisas que nao saem ─────────────────────────
# um componente de caminho pode ter espacos («Central de Patentes»), mas nao atravessa para outro caminho de unidade (X:\ ou X:/)
_COMP = r"(?:(?![A-Za-z]:[\\/])[^\\/\"'|<>*?\r\n]){1,80}"
_FIM = r"(?:(?![A-Za-z]:[\\/])[^\\/\"'|<>*?\s])*"
RX_UNIDADE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]+(?:" + _COMP + r"[\\/]+)*" + _FIM)
RX_UNC = re.compile(r"(?<![A-Za-z0-9\\])\\\\+[A-Za-z0-9_.$-]+(?:\\+[^\\/\"'|<>*?\s]+)+")


def _ultimo(m, unidade):
    partes = [p for p in re.split(r"[\\/]+", m.group(0)) if p]
    if unidade:
        partes = partes[1:]          # tira «C:»
    return partes[-1] if partes else ""


def limpar_caminhos(s):
    """Troca todo caminho local (unidade Windows, X:/..., UNC) pelo nome do arquivo (ou da pasta) so. Devolve (texto, [(nome, sha12)])."""
    achados = []

    def troca(unidade):
        def f(m):
            n = _ultimo(m, unidade)
            achados.append((n, hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()[:12]))
            return n
        return f
    s = RX_UNIDADE.sub(troca(True), s)
    s = RX_UNC.sub(troca(False), s)
    return s, achados


RX_TOKEN = re.compile(r"(gh[posu]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|"
                      r"\bsk-[A-Za-z0-9]{32,}|\bhf_[A-Za-z0-9]{30,}|\bAKIA[0-9A-Z]{16}\b|\bAIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,}|"
                      r"-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,})")
# o que NENHUMA saida pode trazer (dado pessoal forte e credencial em formato de credencial)
RX_SENSIVEL = [
    ("formato de token/credencial", RX_TOKEN),
    ("CPF", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("e-mail pessoal", re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]++@(hotmail|gmail|icloud|outlook|yahoo|live|uol|bol|terra|msn|me|protonmail|"
                                  r"rmiguel\.adv)\.[a-z.]{2,6}", re.I)),
    ("telefone", re.compile(r"\+55\s?\(?\d{2}\)?\s?9?\d{4}-?\d{4}|\(\d{2}\)\s?9\d{4}-?\d{4}")),
]
# o que o QUADRO, alem disso, nao pode trazer (a ordem da gerencia: \Users\, rotol, token/senha/chave — grep simples)
RX_USERS = ("caminho de usuario (\\Users\\)", re.compile(r"[\\/]Users[\\/]", re.I))
RX_ROTOL = ("nome de usuario local (rotol)", re.compile(r"(?<![A-Za-z0-9])rotol(?![A-Za-z0-9])", re.I))   # «rotolimiguel» (X, GitHub) e identificador publico
RX_SEGREDO = ("token/senha/chave", re.compile(r"(?<![A-Za-z])(tokens?|senhas?|chaves?|passwords?|passwd|secrets?|api[_ -]?keys?)(?![A-Za-z])", re.I))
RX_DISCO = ("unidade de disco", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]"))
RX_REDE = ("caminho UNC", re.compile(r"(?<![A-Za-z0-9\\])\\\\[A-Za-z0-9_.$-]+\\"))
PROIBIDO_QUADRO = [RX_USERS, RX_ROTOL, RX_SEGREDO, RX_DISCO, RX_REDE]


def varrer(nome, texto, extra=()):
    for rotulo, rx in list(RX_SENSIVEL) + list(extra):
        if rx.search(texto):
            raise Recusa("%s traz %s" % (nome, rotulo))


# ───────────────────────── leitura ─────────────────────────
def ler_json(p, tentativas=2):
    """Le um JSON vivo (outro processo pode estar gravando): uma segunda tentativa antes de recusar."""
    if not p.is_file():
        raise Recusa("fonte ausente: %s" % p.name)
    for i in range(tentativas):
        try:
            return json.loads(p.read_bytes().decode("utf-8-sig"))
        except Exception as e:  # noqa: BLE001
            if i + 1 == tentativas:
                raise Recusa("JSON ilegivel em %s (%s)" % (p.name, e.__class__.__name__))
            time.sleep(1.5)


def ler_opcional(p):
    return ler_json(p) if p is not None and p.is_file() else None


def git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True)
    except OSError as e:
        raise Recusa("git indisponivel (%s)" % e.__class__.__name__)
    if r.returncode != 0:
        raise Recusa("git %s falhou em %s: %s" % (" ".join(args[:2]), repo.name, r.stderr.decode("utf-8", "replace").strip()[:160]))
    return r.stdout


RX_CUST = re.compile(r"custodia\(([^)]*)\)")


def versoes_do_assunto(dentro):
    """Versoes que a custodia SELA no assunto «custodia(v393+v394)»: o que vem depois de ; / sementes / arco / nao nao conta; v365-v367 e intervalo."""
    corte = re.split(r";|\bsementes\b|\barco\b|\bnao\b", dentro, maxsplit=1)[0]
    return [int(x) for x in re.findall(r"\bv(\d+)\b(?!\s*-\s*v?\d)", corte)]


def commits_de_custodia(repo):
    """Do mais antigo ao mais novo: [{hash, data, assunto, versoes}] dos commits cujo assunto COMECA por «custodia(»."""
    saida = git(repo, "log", "--format=%h%x1f%ci%x1f%s", "--grep=^custodia(").decode("utf-8", "replace")
    cs = []
    for ln in saida.splitlines():
        partes = ln.split("\x1f", 2)
        if len(partes) != 3:
            continue
        h, ci, s = partes
        m = RX_CUST.match(s)
        if not m:
            continue
        cs.append({"hash": h, "data": ci, "assunto": s, "versoes": versoes_do_assunto(m.group(1))})
    cs.reverse()
    return cs


def commit_de(cs, n):
    c = [x for x in cs if n in x["versoes"]]
    return (c[0], len(c)) if c else (None, 0)


def selo_no_commit(h):
    try:
        r = subprocess.run(["git", "-C", str(TB), "show", "%s:%s" % (h, SELO_NO_ESPELHO)], capture_output=True)
    except OSError:
        return None
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout.decode("utf-8-sig"))
    except Exception:  # noqa: BLE001
        return None


def selo_da_versao(n, pasta, tb_commits):
    """(timestamp, origem) do selo da versao n, ou (None, None). Nunca atribui o selo de outra versao."""
    v = "v%d" % n
    f = ler_opcional(pasta / ("fatos_%s.json" % v)) if pasta else None
    if f and f.get("versao") == v and f.get("timestamp"):
        return str(f["timestamp"]), "fatos_" + v
    s = ler_opcional(COFRE / ("um_unificado_%s" % v) / "um_absoluto_selo.json")
    if s and s.get("um_version") == v and s.get("timestamp"):
        return str(s["timestamp"]), "cofre"
    c, _ = commit_de(tb_commits, n)
    if c:
        s = selo_no_commit(c["hash"])
        if s and s.get("timestamp") and (s.get("um_version") == v or (s.get("um_version") is None and n == max(c["versoes"]))):
            return str(s["timestamp"]), "espelho@" + c["hash"]
    return None, None


# ───────────────────────── organismo: o quadro saneado ─────────────────────────
def construir_quadro(agora_iso, antigo_bytes, prov):
    q = ler_json(QUADRO)
    if not isinstance(q, dict):
        raise Recusa("quadro: raiz nao e objeto")
    for k in ("medido_em", "selo", "resumo", "itens"):
        if k not in q:
            raise Recusa("quadro sem a chave %r" % k)
    if not isinstance(q["selo"], dict) or not all(k in q["selo"] for k in ("versao", "pin", "timestamp")):
        raise Recusa("quadro: selo sem versao/pin/timestamp")
    if not isinstance(q["itens"], list) or not q["itens"]:
        raise Recusa("quadro sem itens")
    itens, saneados, extras = [], [], Counter()
    for i, it in enumerate(q["itens"]):
        if not isinstance(it, dict):
            raise Recusa("quadro: item %d nao e objeto" % i)
        for k in it:
            if k not in CINCO:
                extras[k] += 1
        novo = {}
        for k in CINCO:
            if k not in it:
                raise Recusa("quadro: item %d sem o campo %r" % (i, k))
            v = it[k]
            if isinstance(v, (list, dict)) or v is None:
                raise Recusa("quadro: item %d campo %r nao e escalar" % (i, k))
            v, ach = limpar_caminhos(v if isinstance(v, str) else str(v))
            for nome, h12 in ach:
                saneados.append({"item": i, "campo": k, "para": nome, "original_sha12": h12})
            novo[k] = v
        itens.append(novo)
    resumo = dict(q["resumo"])
    conta = Counter(it["estado"] for it in itens)
    if {k: int(v) for k, v in resumo.items()} != dict(conta):
        raise Recusa("quadro: resumo %s nao confere com os itens %s" % (resumo, dict(conta)))
    base = {"medido_em": str(q["medido_em"]), "selo": {k: str(q["selo"][k]) for k in ("versao", "pin", "timestamp")}, "resumo": resumo, "itens": itens}
    publicado_em = agora_iso
    if antigo_bytes:        # o mesmo quadro nao e «republicado»: a hora de publicacao so muda quando o conteudo muda
        try:
            ant = json.loads(antigo_bytes.decode("utf-8-sig"))
            if all(ant.get(k) == base[k] for k in base) and ant.get("fonte") == FONTE_QUADRO and ant.get("publicado_em"):
                publicado_em = ant["publicado_em"]
        except Exception:  # noqa: BLE001
            pass
    doc = dict(base)
    doc["publicado_em"] = publicado_em
    doc["fonte"] = FONTE_QUADRO
    texto = json.dumps(doc, ensure_ascii=False, indent=1)
    # a recusa: o que sobrar depois da limpeza PARA — procurando campo a campo para dizer onde (nunca o valor)
    for rotulo, rx in PROIBIDO_QUADRO:
        if rx.search(texto):
            onde = [("item %d campo %s" % (i, k)) for i, it in enumerate(itens) for k in CINCO if rx.search(it[k])][:3]
            raise Recusa("quadro saneado ainda traz %s (%s)" % (rotulo, "; ".join(onde) or "fora dos itens"))
    varrer("quadro saneado", texto)
    prov["quadro"] = {"itens": len(itens), "campos_extras_removidos": dict(extras), "caminhos_saneados": len(saneados), "saneados": saneados,
                      "medido_em": doc["medido_em"], "selo_versao": doc["selo"]["versao"]}
    return (texto + "\n").encode("utf-8"), doc, len(saneados)


# ───────────────────────── organismo: as custodias ─────────────────────────
def pasta_da_custodia(n):
    c = sorted(p for p in WORK.glob("custodia_v%d_*" % n) if p.is_dir())
    return c[-1] if c else None


def subida_do_site(n):
    """(carimbo, 'AAAA-MM-DD HH:MM:SS') da 1a subida VERIFICADA cujo relatorio cita manifesto_vN.json (ou MANIFESTO_SUBIDA_vN.json)."""
    alvos = {"manifesto_v%d.json" % n, "manifesto_subida_v%d.json" % n}
    if not SUBIDAS.is_dir():
        return None
    for d in sorted(SUBIDAS.iterdir()):
        if not (d.is_dir() and re.fullmatch(r"\d{8}_\d{6}", d.name)):
            continue
        rel = d / "RELATORIO.md"
        if not rel.is_file():
            continue
        with open(rel, "rb") as f:
            cab = f.read(2500).decode("utf-8", "replace")
        m = re.search(r"Manifesto:\s*`([^`]+)`", cab)
        if not m or re.split(r"[\\/]", m.group(1))[-1].lower() not in alvos:
            continue
        if "SUBIDA VERIFICADA" not in rel.read_text(encoding="utf-8", errors="replace"):
            continue
        h = re.search(r"\((\d\d)/(\d\d)/(\d{4}) (\d\d):(\d\d):(\d\d)\)", cab.splitlines()[0] if cab else "")
        if h:
            quando = "%s-%s-%s %s:%s:%s" % (h.group(3), h.group(2), h.group(1), h.group(4), h.group(5), h.group(6))
        else:
            quando = datetime.strptime(d.name, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        return d.name, quando
    return None


def rodada_da_custodia(pasta, n):
    if not pasta:
        return None
    for f in sorted(pasta.glob("central_publica_v%d*saida*.txt" % n)):
        ms = re.findall(r"rodada\s+(\d{8}_\d{6}):\s*COMPLETA", f.read_text(encoding="utf-8", errors="replace"))
        if ms:
            r = ler_opcional(RODADAS / (ms[-1] + ".json"))
            if r and r.get("ok") is True:
                return ms[-1]
    return None


def construir_custodias(tb, cen, prov):
    nums = sorted({int(m.group(1)) for p in WORK.iterdir() if p.is_dir() for m in [re.match(r"custodia_v(\d+)_", p.name)] if m}, reverse=True)
    out, plog = [], {}
    for n in nums:
        v = "v%d" % n
        pasta = pasta_da_custodia(n)
        fatos = ler_opcional(pasta / ("fatos_%s.json" % v)) if pasta else None
        conf = ler_opcional(pasta / ("CONFERENCIA_FINAL_%s.json" % v)) if pasta else None
        p_fatos = fatos.get("pin16") if fatos and fatos.get("versao") == v else None
        p_conf = conf["pin"][:16] if conf and isinstance(conf.get("pin"), str) else None
        if p_fatos and p_conf and p_fatos != p_conf:
            raise Recusa("custodia %s: pin16 de fatos (%s) e da conferencia final (%s) divergem" % (v, p_fatos, p_conf))
        pin16 = p_fatos or p_conf
        if pin16 is not None and not re.fullmatch(r"[0-9a-f]{16}", pin16):
            raise Recusa("custodia %s: pin16 malformado" % v)
        selado, origem_selo = selo_da_versao(n, pasta, tb)
        ct, nt = commit_de(tb, n)
        cc, nc = commit_de(cen, n)
        sub = subida_do_site(n)
        rod = rodada_da_custodia(pasta, n)
        confer = None
        if conf and isinstance(conf.get("ok"), int) and isinstance(conf.get("total"), int):
            confer = "%d/%d" % (conf["ok"], conf["total"])
        out.append({"versao": v, "pin16": pin16, "selado_em": selado, "espelho_commit": ct["hash"] if ct else None,
                    "central_commit": cc["hash"] if cc else None, "site_subida_em": sub[1] if sub else None,
                    "publica_rodada": rod, "conferencia": confer})
        plog[v] = {"pasta": pasta.name if pasta else None, "fatos": bool(fatos), "conferencia_final": bool(conf),
                   "pin16_de": ("fatos" if p_fatos else "conferencia_final" if p_conf else None), "selado_em_de": origem_selo,
                   "espelho_commits_candidatos": nt, "central_commits_candidatos": nc, "site_subida_carimbo": sub[0] if sub else None}
    prov["custodias"] = plog
    return out


# ───────────────────────── pensamentos ─────────────────────────
RX_URL_X = re.compile(r"https://(?:x|twitter)\.com/[A-Za-z0-9_]{1,30}/status/\d{5,25}")


def fonte_curta(f):
    t = unicodedata.normalize("NFKD", f or "").encode("ascii", "ignore").decode("ascii").lower()
    m = re.match(r"\s*([a-z]+)", t)
    return m.group(1) if m else None


def construir_pensamentos(prov):
    if not LIVRO.is_file():
        raise Recusa("fonte ausente: LIVRO.jsonl")
    por_data, linhas = {}, 0
    for i, ln in enumerate(LIVRO.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip():
            continue
        linhas += 1
        try:
            d = json.loads(ln)
        except Exception:  # noqa: BLE001
            raise Recusa("LIVRO.jsonl: linha %d nao e JSON" % i)
        if not (isinstance(d, dict) and isinstance(d.get("data"), str) and isinstance(d.get("texto"), str) and d["texto"].strip()):
            raise Recusa("LIVRO.jsonl: linha %d sem data/texto" % i)
        por_data[d["data"]] = d          # a ultima linha do dia vale
    out, fora, avisos = [], [], []
    for data, d in por_data.items():
        # o livro e os recibos guardam o sha256 do ARQUIVO do dia (X_DIARIO/<data>.md = texto + LF final); aceita-se tambem o do texto cru
        hs = {hashlib.sha256(d["texto"].encode("utf-8")).hexdigest(), hashlib.sha256((d["texto"] + "\n").encode("utf-8")).hexdigest()}
        if d.get("sha256") and d["sha256"] not in hs:
            raise Recusa("LIVRO.jsonl: sha256 do texto de %s nao confere" % data)
        rec = ler_opcional(RECIBOS_X / (data + ".json"))
        url, publicado = None, False
        if rec is not None:
            if rec.get("publicado") is True:
                if rec.get("texto_sha256") and rec["texto_sha256"] not in hs:
                    raise Recusa("recibo de %s: o texto publicado nao e o do livro (sha256)" % data)
                publicado, url = True, rec.get("url")
        elif d.get("publicado") is True:
            publicado, url = True, d.get("url")
            avisos.append("%s: sem recibo em ORDEM_021; valeu o registro do livro" % data)
        if not publicado:
            fora.append(data)
            continue
        if not (isinstance(url, str) and RX_URL_X.fullmatch(url)):
            raise Recusa("pensamento de %s publicado, mas a url nao e de uma publicacao no X" % data)
        out.append({"data": data, "texto": d["texto"], "url": url, "fonte": fonte_curta(d.get("fonte"))})
    out.sort(key=lambda x: x["data"], reverse=True)
    prov["pensamentos"] = {"linhas_no_livro": linhas, "dias": len(por_data), "publicados": len(out), "sem_publicacao_confirmada_fora": fora, "avisos": avisos}
    return out


# ───────────────────────── arcos ─────────────────────────
def lit_js(s, i):
    """Le o literal de string JS que abre em s[i] (aspas simples ou duplas); devolve (valor, indice_depois)."""
    q = s[i]
    if q not in "'\"":
        raise Recusa("i18n.js: literal esperado")
    j, out = i + 1, []
    while j < len(s):
        c = s[j]
        if c == "\\":
            n = s[j + 1]
            if n == "u":
                out.append(chr(int(s[j + 2:j + 6], 16))); j += 6; continue
            if n == "x":
                out.append(chr(int(s[j + 2:j + 4], 16))); j += 4; continue
            out.append({"n": "\n", "t": "\t", "r": "\r"}.get(n, n)); j += 2; continue
        if c == q:
            return "".join(out), j + 1
        out.append(c); j += 1
    raise Recusa("i18n.js: literal nao fechado")


def arcos_do_i18n():
    s = I18N.read_text(encoding="utf-8")
    blocos = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^\s{0,4}([a-z]{2})\s*:\s*\{\s*$", s)]
    if not blocos:
        raise Recusa("i18n.js: nenhum bloco de lingua encontrado")
    out = {"en": {}, "pt": {}}
    for m in re.finditer(r"'art\.c\.cl\.arc(\d+)'\s*:\s*'", s):
        lang = None
        for pos, l in blocos:
            if pos < m.start():
                lang = l
            else:
                break
        if lang not in out:
            continue
        txt, _ = lit_js(s, m.end() - 1)
        if m.group(1) in out[lang]:
            raise Recusa("i18n.js: chave arc%s duplicada em %s" % (m.group(1), lang))
        out[lang][m.group(1)] = txt
    return out


def arcos_dos_arquivos():
    """{n: {en, pt, pin16}} de revisoes/arco_vNNN_texto.json (o arquivo do v394 traz tambem o arco do v393, sem pin16 proprio)."""
    out = {}
    for p in sorted(REVISOES.glob("arco_v*_texto.json")):
        m = re.fullmatch(r"arco_v(\d+)_texto\.json", p.name)
        if not m:
            continue
        n = int(m.group(1))
        d = ler_json(p)
        pin = d.get("pin16") if isinstance(d.get("pin16"), str) and re.fullmatch(r"[0-9a-f]{16}", d["pin16"]) else None
        if isinstance(d.get("en"), str) and isinstance(d.get("pt"), str):
            out[n] = {"en": d["en"], "pt": d["pt"], "pin16": pin}
        for k in d:
            mm = re.fullmatch(r"en(\d+)", k)
            if mm and isinstance(d.get(k), str) and isinstance(d.get("pt" + mm.group(1)), str):
                outro = int(mm.group(1))
                out[outro] = {"en": d[k], "pt": d["pt" + mm.group(1)], "pin16": pin if outro == n else None}
    return out


def construir_arcos(tb, prov):
    live, arq = arcos_do_i18n(), arcos_dos_arquivos()
    nums = sorted({int(x) for x in live["en"]} | {int(x) for x in live["pt"]} | set(arq), reverse=True)
    out, divergem, so_i18n, so_arquivo, sem_data = [], [], [], [], []
    for n in nums:
        k = str(n)
        a = arq.get(n)
        no_site = k in live["en"] and k in live["pt"]
        en = live["en"].get(k) or (a["en"] if a else None)
        pt = live["pt"].get(k) or (a["pt"] if a else None)
        if not en or not pt:
            raise Recusa("arco v%d sem texto em EN e PT" % n)
        if a and no_site and (live["en"][k] != a["en"] or live["pt"][k] != a["pt"]):
            divergem.append("v%d" % n)
        if not a:
            so_i18n.append("v%d" % n)
        elif not no_site:
            so_arquivo.append("v%d" % n)
        ts, _ = selo_da_versao(n, pasta_da_custodia(n), tb)
        if ts is None:
            sem_data.append("v%d" % n)
        out.append({"versao": "v%d" % n, "data": ts[:10] if ts else None, "pin16": a["pin16"] if a else None, "en": en, "pt": pt})
    prov["arcos"] = {"n": len(out), "texto_do_site_difere_do_arquivo_(valeu_o_do_site)": divergem, "so_no_i18n_(pin16_null)": so_i18n,
                     "so_no_arquivo_(site_sem_a_chave)": so_arquivo, "sem_data": sem_data,
                     "pin16_null": [x["versao"] for x in out if x["pin16"] is None]}
    return out


# ───────────────────────── escrita ─────────────────────────
def gravar(alvo, dados, carimbo, rotulo, seco=False):
    """backup de bytes do que existe -> temporario -> confere -> substitui. Devolve o estado em palavras."""
    antigo = alvo.read_bytes() if alvo.is_file() else None
    if antigo == dados:
        return "inalterado"
    if seco:
        return "novo (seco)" if antigo is None else "mudaria (seco)"
    alvo.parent.mkdir(parents=True, exist_ok=True)
    nome_bak = None
    if antigo is not None:
        BAK.mkdir(parents=True, exist_ok=True)
        nome_bak = rotulo.replace("/", "__") + ".bak_" + carimbo
        (BAK / nome_bak).write_bytes(antigo)
        if (BAK / nome_bak).read_bytes() != antigo:
            raise Recusa("backup de %s nao confere" % rotulo)
    t = alvo.with_name(alvo.name + ".tmp")
    t.write_bytes(dados)
    if t.stat().st_size != len(dados) or sha(t.read_bytes()) != sha(dados):
        t.unlink()
        raise Recusa("temporario de %s nao confere" % rotulo)
    os.replace(t, alvo)
    if sha(alvo.read_bytes()) != sha(dados):
        raise Recusa("%s gravado nao confere" % rotulo)
    return "gravado" if antigo is None else "gravado (backup central_extra_bak/%s)" % nome_bak


def js(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def autoteste():
    ok = n = 0

    def t(nome, cond):
        nonlocal ok, n
        n += 1
        ok += bool(cond)
        print("  %s %s" % ("ok    " if cond else "FALHOU", nome))
    s, a = limpar_caminhos(r"C:\IALD\Central de Patentes\work\x\arquivo.json")
    t("caminho com espacos -> nome do arquivo", s == "arquivo.json" and len(a) == 1)
    s, a = limpar_caminhos("ver C:/IALD/Site/tgl/v3.0/index.html agora")
    t("C:/... no meio do texto", s == "ver index.html agora" and len(a) == 1)
    s, a = limpar_caminhos("301 https://teoriadagravitacaoluminodinamica.com/ e ['_prep_20261002_060917']")
    t("URL e lista nao sao caminho", a == [] and s.startswith("301 https://teoria"))
    s, a = limpar_caminhos("FileNotFoundError(2, 'x', 'C:\\\\IALD\\\\Central de Patentes\\\\a b\\\\z.txt') @ onde")
    t("repr com barras dobradas e aspas", s == "FileNotFoundError(2, 'x', 'z.txt') @ onde" and len(a) == 1)
    s, a = limpar_caminhos(r"pasta C:\IALD\Site\ e depois D:\x\y.bin")
    t("diretorio com barra final e dois caminhos", s == "pasta Site e depois y.bin" and len(a) == 2)
    s, a = limpar_caminhos(r"em \\servidor\pasta\arq.txt ok")
    t("UNC", s == "em arq.txt ok")
    s, a = limpar_caminhos(r"C:\Users\rotol\AppData\x.log;E:/a/b")
    t("duas unidades coladas: nada de unidade sobra", not RX_DISCO[1].search(s) and not RX_USERS[1].search(s) and not RX_ROTOL[1].search(s) and len(a) == 2)
    t("recusa: \\Users\\", RX_USERS[1].search("x\\Users\\y") is not None)
    t("recusa: rotol isolado", RX_ROTOL[1].search("usuario rotol aqui") is not None)
    t("rotolimiguel (identificador publico) passa", RX_ROTOL[1].search("https://x.com/rotolimiguel/status/1") is None)
    t("recusa: token/senha/chave", all(RX_SEGREDO[1].search(x) for x in ("o token", "a Senha", "chave pública", "API key")))
    t("tokenizer nao e token", RX_SEGREDO[1].search("tokenizer") is None)
    t("recusa: formato de token GitHub", RX_TOKEN.search("ghp_" + "a" * 36) is not None)
    # (os exemplos sao montados na hora: o texto deste arquivo vai ao espelho publico e nao pode trazer um CPF ou e-mail, nem de mentira)
    t("recusa: CPF", RX_SENSIVEL[1][1].search("123." + "456." + "789-" + "09") is not None)
    t("recusa: e-mail pessoal", RX_SENSIVEL[2][1].search("fulano" + "@" + "gmail.com") is not None)
    t("e-mail institucional passa", RX_SENSIVEL[2][1].search("contato@iald.ia.br") is None)
    t("versoes: custodia(v393+v394)", versoes_do_assunto("v393+v394") == [393, 394])
    t("versoes: sementes/arco/intervalo nao contam", versoes_do_assunto("v368 + sementes v365-v367; v360 nao se custodia") == [368]
      and versoes_do_assunto("v375 + arco v369-v374") == [375])
    t("fonte curta", [fonte_curta(x) for x in ("gerencia (Claude, sessao a7)", "nativa (guarda + aferidor)", "medida", "Gerência", None)]
      == ["gerencia", "nativa", "medida", "gerencia", None])
    t("url do X", RX_URL_X.fullmatch("https://x.com/rotolimiguel/status/2113729970568622147") is not None
      and RX_URL_X.fullmatch("javascript:alert(1)") is None and RX_URL_X.fullmatch("https://evil.example/status/123456") is None)
    t("literal JS", lit_js("'a\\'b\\u00e9'", 0)[0] == "a'b\u00e9")
    print("AUTOTESTE: %d/%d" % (ok, n))
    return 0 if ok == n else 1


def main():
    global SAIDA, BAK, PROV
    ap = argparse.ArgumentParser()
    ap.add_argument("--seco", action="store_true", help="calcula e valida tudo, nao grava nada")
    ap.add_argument("--saida", default=None, help="pasta de saida alternativa (ensaio)")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()
    if a.autoteste:
        return autoteste()
    if a.saida:
        SAIDA = Path(a.saida)
        BAK = SAIDA.parent / (SAIDA.name + "_bak")
        PROV = SAIDA.parent / (SAIDA.name + "_proveniencia.json")
    agora = datetime.now().astimezone()
    carimbo = agora.strftime("%Y%m%d_%H%M%S")
    agora_iso = agora.isoformat(timespec="seconds")
    prov = {"gerado_em": agora_iso, "gerador": "work/central_publica_22out/gerar_central_extra.py"}
    try:
        if not ORG_HTML.is_file() or ORG_HTML.stat().st_size == 0:
            raise Recusa("fonte do Kimi ausente ou vazia: v3.0_bancada/organismo_publico/index.html")
        html = ORG_HTML.read_bytes()
        varrer("organismo/index.html", html.decode("utf-8", "replace"), extra=[RX_USERS])
        ant = SAIDA / "organismo" / "ESTADO_DO_ORGANISMO.json"
        quadro, doc, n_san = construir_quadro(agora_iso, ant.read_bytes() if ant.is_file() else None, prov)
        tb, cen = commits_de_custodia(TB), commits_de_custodia(CEN)
        cust = construir_custodias(tb, cen, prov)
        pens = construir_pensamentos(prov)
        arcos = construir_arcos(tb, prov)
        saidas = {"organismo/index.html": html, "organismo/ESTADO_DO_ORGANISMO.json": quadro, "organismo/custodias.json": js(cust),
                  "pensamentos/pensamentos.json": js(pens), "arcos.json": js(arcos)}
        for rel, b in saidas.items():
            if rel.endswith(".json") and rel != "organismo/ESTADO_DO_ORGANISMO.json":
                varrer(rel, b.decode("utf-8"))
        itens_man = [{"caminho": rel, "bytes": len(b), "sha256": sha(b)} for rel, b in sorted(saidas.items())]
        gerado_em = agora_iso
        man_antigo = SAIDA / "MANIFESTO_CENTRAL_EXTRA.json"
        if man_antigo.is_file():        # manifesto do mesmo conteudo nao e «regerado»
            try:
                m0 = json.loads(man_antigo.read_bytes().decode("utf-8-sig"))
                if m0.get("saidas") == itens_man and m0.get("gerado_em"):
                    gerado_em = m0["gerado_em"]
            except Exception:  # noqa: BLE001
                pass
        saidas["MANIFESTO_CENTRAL_EXTRA.json"] = js({"gerado_em": gerado_em, "gerador": "work/central_publica_22out/gerar_central_extra.py",
                                                     "o_montar_nao_copia_ao_site": list(NAO_PUBLICA_NO_SITE), "saidas": itens_man})
        estados = {rel: gravar(SAIDA / rel, b, carimbo, rel, a.seco) for rel, b in saidas.items()}
        prov["saidas"] = {rel: {"bytes": len(b), "sha256_16": sha(b)[:16]} for rel, b in saidas.items()}
        if PROV.is_file():        # o registro so muda quando o conteudo muda: a hora de geracao antiga vale se o resto e igual
            try:
                p0 = json.loads(PROV.read_bytes().decode("utf-8-sig"))
                if p0.get("gerado_em") and {k: v for k, v in p0.items() if k != "gerado_em"} == {k: v for k, v in prov.items() if k != "gerado_em"}:
                    prov["gerado_em"] = p0["gerado_em"]
            except Exception:  # noqa: BLE001
                pass
        prov_estado = gravar(PROV, js(prov), carimbo, PROV.name, a.seco)
    except Recusa as e:
        msg = "RECUSA em central_extra (nada gravado): %s" % e
        print(msg, file=sys.stderr)
        print(msg)
        return 1
    for rel in sorted(saidas):
        print("  %-38s %9d B  %s  %s" % (rel, len(saidas[rel]), sha(saidas[rel])[:16], estados[rel]))
    print("  %-38s (proveniencia local, nao publicada) %s" % (PROV.name, prov_estado))
    idade = None
    try:
        idade = (agora.replace(tzinfo=None) - datetime.strptime(doc["medido_em"], "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600
    except Exception:  # noqa: BLE001
        pass
    print("central_extra%s: %d saidas, %.1f KB | quadro %d itens, %d caminho(s) saneado(s)%s | custodias %d | pensamentos %d | arcos %d" % (
        " (SECO)" if a.seco else "", len(saidas), sum(len(b) for b in saidas.values()) / 1024, len(doc["itens"]), n_san,
        (", medido ha %.1f h%s" % (idade, " — ACIMA de 6 h" if idade > 6 else "")) if idade is not None else "", len(cust), len(pens), len(arcos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
