# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411-posrito, a servico da gerencia c1] os TEXTOS DA CUSTODIA que a abertura do H0DN x BG1 torna obrigatorios no HANDOFF da v411 (DESENHO_v411 5.3; aditivos 1 a 4 da gerencia, 12/11/2026)
# [AO LADO, 12/11/2026 tarde, mesmo autor] D174 da gerencia: o painel vai INTEIRO (sem corte por orcamento; conferido contra o render inteiro do arquivo); as duas linhas do H0DN da parte do Clay sao apontadores; README_H0DN_EN entra na lista da G1
# [AO LADO, 12/11/2026 11h, mesmo autor] aditivo 4: a FORMULA deixou de ser PROPOSTA: tudo sai de TOPO_RATIFICADO_v411.json (ratificado pelo operador; o painel curto e a frase de estado), cortado para caber em cada lugar; o acervo (as cobrancas do livro) entra so' com falsificadas == 0
"""blocos_custodia_v411.py -- monta, do core SELADO (os registros `h0dn_bg1_v411`, `teste_de_veracidade_fase9_v397`, `estatuto_da_prova_v391`, `kernel_formalization`, `cunhagens_v411`) e de UMA fonte de texto,
`TOPO_RATIFICADO_v411.json` (a formula RATIFICADA pelo operador em 12/11/2026, com o acrescimo do acervo que ele ordenou; a fonte unica dos tres tamanhos), os textos que a custodia (G1) le do HANDOFF da v411 entre
marcadores `<!-- INICIO_<ID>_v411 -->` ... `<!-- FIM_<ID>_v411 -->` e que substituem os moldes que diziam que beta_TGL na natureza a 5 sigma e' o passo aberto:

  NOTA_EN (a NOTA inteira do ledger, com a frase de estado EN); README_PAINEL_H0DN (o painel curto, EN e PT, `painel_readme_en/pt`); README_FASE9_V2 (a linha de registro da Fase 9 V2, EN e PT, com a regra do 4,44, que
  aponta REGISTRO_FASE9_V2.md); README_PRIMORDIAL_5SIGMA, README_STATUS_5SIGMA, README_H0DN e a linha do H0DN em README_RITOS (cortados da frase de estado, `estado_en/pt`); os onze do estatuto (ESTATUTO_<CHAVE>,
  cada um so' o TRECHO do 5 sigma da chave, na sintaxe dela, uma linha; ASCII onde o trecho e' ASCII); e, fora da lista da custodia, README_H0DN_EN (a linha EN da parte do Clay, que ainda diz que o teste nao foi
  aberto) e X_TEXTO.

Os NUMEROS entram pelos marcadores da chave `marcadores` do arquivo, cada um lido do core pela sua `fonte` (nunca digitados), com o arredondamento e o sinal que a G1 confere; marcador que sobre = PARAR. A frase
“nenhuma foi falsificada” so' sai com `estatuto_da_prova_v391.prova_2_ritos.falsificadas == 0` e a soma das categorias igual ao numero de cobrancas; senao PARAR. O rotulo do P2 e' a chave `rotulo_p2`; o token
selado `P2_NOT_DETERMINED` de `three_stress_tests_v387` fica, dito como registro. Cortes so' por pedacos do texto ratificado (sentencas e oracoes inteiras); se o README nao couber no orcamento, sai primeiro a frase do
acervo do painel curto (ela esta' na frase de estado), nunca um dos quatro obrigatorios da F67. `conferir()` roda as MESMAS conferencias da custodia e a guarda de frases da v411; nada aqui escreve."""
import ast
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
CEN_TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(PK))), "tools")   # ...\Central de Patentes\tools (so' leitura)
for _p in (PK, CEN_TOOLS):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from custodia_g1 import h0dn as H0DN, textos as TXG1  # noqa: E402   (so' leitura: as funcoes da custodia)
import guarda_frases_v411 as GF  # noqa: E402

VERSAO = "v411"
ANTERIOR = "v410"
REGISTRO = "h0dn_bg1_v411"
REGISTRO_FASE9 = "teste_de_veracidade_fase9_v397"
REGISTRO_ACERVO = "estatuto_da_prova_v391"
TOPO_ARQ = os.path.join(PK, "TOPO_RATIFICADO_v411.json")
REGISTRO_FASE9_V2_MD = "REGISTRO_FASE9_V2.md"   # o arquivo da raiz do espelho onde a custodia poe o painel inteiro da Fase 9 V2 (aditivo 2, B)
MARCADORES_CUSTODIA = tuple(H0DN.TODOS)
MARCADORES_EXTRAS = tuple(x for x in ("README_H0DN_EN", "X_TEXTO") if x not in MARCADORES_CUSTODIA)   # (D174: a G1 passou a consumir README_H0DN_EN; o que ela nao consome vai ao lado, dito)
UMA_LINHA = ("README_PRIMORDIAL_5SIGMA", "README_H0DN", "README_H0DN_EN") + tuple(H0DN.MARCADORES_ESTATUTO)
FRASE_DO_ACERVO = {"en": " Read with the whole record: ⟨N charges⟩ pre-registered charges, none falsified.", "pt": " Lido com o acervo: ⟨N cobranças⟩ cobranças pré-registradas, nenhuma falsificada."}   # (D174: o painel vai INTEIRO; a frase do acervo e' ordem do operador de 12/11 e o controle negativo confere que ela esta')
APONTADOR_EN = "`ESTADO_ATUAL.md`"   # (D174, B: a linha EN do H0DN aponta para a leitura inteira; a palavra “reservations” e' a da secao EN do artigo, quadro_v411.py)


# ------------------------------------------------------------------------------------------------ a fonte: TOPO_RATIFICADO_v411.json
def ler_topo():
    if not os.path.exists(TOPO_ARQ):
        raise ValueError("TOPO_RATIFICADO_v411.json ausente: os textos da custodia saem SO' dele (aditivo 4)")
    b = open(TOPO_ARQ, "rb").read(); tj = json.loads(b.decode("utf-8"))
    for k in ("painel_readme_pt", "painel_readme_en", "estado_pt", "estado_en", "rotulo_p2", "marcadores", "regras"):
        if k not in tj:
            raise ValueError("TOPO_RATIFICADO_v411.json sem a chave %s" % k)
    return tj, {"arquivo": TOPO_ARQ, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


# ------------------------------------------------------------------------------------------------ os numeros (do core; o arredondamento e o sinal que a G1 confere)
def _f2(x, lg):
    s = "%.2f" % abs(float(x))
    if lg.startswith("pt"):
        s = s.replace(".", ",")
    if float(x) < 0:
        s = ("-" if lg.endswith("ascii") else "\u2212") + s
    return s


def _data_iso(s):
    m = re.match(r"(\d{4})-(\d\d)-(\d\d)", str(s or ""))
    if not m:
        raise ValueError("data ilegivel nos atos do registro: %r" % (s,))
    return m.group(1), m.group(2), m.group(3)


def numeros(core):
    """Tudo o que os textos citam, LIDO do core: o h0dn_bg1_v411 (pelo contrato da custodia), a Fase 9 V2, o acervo (estatuto_da_prova_v391.prova_2_ritos), com as recusas das regras do arquivo ratificado."""
    reg = core.get(REGISTRO)
    if not isinstance(reg, dict):
        raise ValueError("o core nao traz %s" % REGISTRO)
    V = H0DN.valores(reg)   # o contrato da custodia (ValueError se faltar ou divergir)
    p, cf, at = V["primario"], V["cefeidas_livres"], V["atos"]
    y, m, d = _data_iso(at.get("inicio_da_abertura_utc"))
    f9 = (core.get(REGISTRO_FASE9) or {}); L9 = f9.get("lido") or {}
    for k in ("z_disc_calibrado", "z_delta_calibrado", "lnB_lcdm"):
        if not isinstance(L9.get(k), (int, float)):
            raise ValueError("o registro %s nao traz lido.%s" % (REGISTRO_FASE9, k))
    d9 = None
    for fo in f9.get("fontes") or []:
        mm = re.search(r"(\d\d)/(\d\d)/(\d{4})", str(fo.get("papel") or "")) if fo.get("chave") == "f9v2_resultado" else None
        if mm:
            d9 = mm.groups()
    if not d9:
        raise ValueError("a data da abertura da Fase 9 V2 nao foi lida do registro %s (fontes/f9v2_resultado)" % REGISTRO_FASE9)
    p2r = (core.get(REGISTRO_ACERVO) or {}).get("prova_2_ritos") or {}
    led = p2r.get("ledger") or {}
    cats = ("NOT_FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING")
    if not (isinstance(p2r.get("n_cobrancas"), int) and isinstance(p2r.get("falsificadas"), int) and all(isinstance(led.get(c), int) for c in cats)):
        raise ValueError("o core nao traz %s.prova_2_ritos (n_cobrancas, falsificadas, ledger)" % REGISTRO_ACERVO)
    if p2r["falsificadas"] != 0 or led.get("FALSIFIED", 0) != 0:
        raise ValueError("PARAR: o livro tem cobranca falsificada (%s): a frase “nenhuma foi falsificada” nao sai" % p2r["falsificadas"])
    if sum(led[c] for c in cats) + p2r["falsificadas"] != p2r["n_cobrancas"]:
        raise ValueError("PARAR: as categorias do livro nao somam o numero de cobrancas")
    p2 = reg.get("p2_ao_lado_da_v387") if isinstance(reg.get("p2_ao_lado_da_v387"), dict) else None
    N = {"V": V, "reg": reg, "n": int(abs(float(p["z_null"]))), "ramo": p["ramo"], "ramo_c": cf["ramo"], "outcome": V["outcome"],
         "data_en": "%s-%s-%s" % (y, m, d), "data_pt": "%s/%s/%s" % (d, m, y),
         "c_pre": str(at.get("commit_do_pre_registro") or "")[:8], "c_res": str(at.get("commit_do_resultado") or "")[:8],
         "data9_en": "%s-%s-%s" % (d9[2], d9[1], d9[0]), "data9_pt": "%s/%s/%s" % d9, "p2": p2, "acervo": {"n": p2r["n_cobrancas"], "ledger": {c: led[c] for c in cats}}}
    if not (re.fullmatch(r"[0-9a-f]{8}", N["c_pre"]) and re.fullmatch(r"[0-9a-f]{8}", N["c_res"])):
        raise ValueError("os commits do pre-registro e do resultado nao foram lidos dos atos do registro")
    for lg in ("en", "pt"):
        N[lg] = {"zn": _f2(p["z_null"], lg), "zk": _f2(p["z_tgl"], lg), "zc": _f2(cf["z_null"], lg), "n": str(N["n"]),
                 "zd9": _f2(L9["z_disc_calibrado"], lg), "zdel9": _f2(L9["z_delta_calibrado"], lg), "lnb9": _f2(L9["lnB_lcdm"], lg)}
    # o valor de cada marcador do arquivo, pela fonte dele (o nome PT e o EN); a fonte dita no arquivo tem de nomear a chave que se le aqui
    val = {"⟨Z contra K⟩": ("h0dn_bg1_v411.values.primario.z_tgl", lambda lg: N[lg]["zk"]), "⟨Z contra o nulo⟩": ("h0dn_bg1_v411.values.primario.z_null", lambda lg: N[lg]["zn"]),
           "⟨n⟩": ("h0dn_bg1_v411.values.primario.z_null", lambda lg: N[lg]["n"]), "⟨Z das Cefeidas livres⟩": ("h0dn_bg1_v411.values.cefeidas_livres.z_null", lambda lg: N[lg]["zc"]),
           "⟨N cobranças⟩": ("prova_2_ritos.n_cobrancas", lambda lg: str(p2r["n_cobrancas"])), "⟨não falsificadas⟩": ("ledger.NOT_FALSIFIED", lambda lg: str(led["NOT_FALSIFIED"])),
           "⟨inconclusivas⟩": ("ledger.INCONCLUSIVE", lambda lg: str(led["INCONCLUSIVE"])), "⟨à espera de dado⟩": ("ledger.AWAITING", lambda lg: str(led["AWAITING"])),
           "⟨excluídas na leitura⟩": ("ledger.EXCLUDED_IN_READING", lambda lg: str(led["EXCLUDED_IN_READING"])), "⟨z_disc⟩": ("teste_de_veracidade_fase9_v397", lambda lg: N[lg]["zd9"]),
           "⟨z_delta⟩": ("teste_de_veracidade_fase9_v397", lambda lg: N[lg]["zdel9"]), "⟨lnB⟩": ("teste_de_veracidade_fase9_v397", lambda lg: N[lg]["lnb9"])}
    N["_val"] = val
    return N


def preencher(texto, lg, N, tj):
    """troca cada marcador do arquivo (o nome PT, ou o EN em `marcadores[...]["en"]`) pelo valor lido do core; marcador que sobre = ValueError."""
    t = str(texto)
    for mk_pt, spec in tj["marcadores"].items():
        if mk_pt not in N["_val"]:
            raise ValueError("marcador do arquivo sem leitor aqui: %s" % mk_pt)
        chave, f = N["_val"][mk_pt]
        if chave.split(".")[-1] not in str(spec.get("fonte")) and chave not in str(spec.get("fonte")):
            raise ValueError("a fonte do marcador %s no arquivo (%r) nao nomeia a chave que se le aqui (%s)" % (mk_pt, spec.get("fonte"), chave))
        for nome in (mk_pt, spec.get("en")):
            if nome:
                t = t.replace(nome, f(lg))
    if "⟨" in t or "⟩" in t:
        raise ValueError("PARAR: sobrou marcador no texto emitido: %r" % re.findall(r"⟨[^⟩]*⟩", t))
    return t


# ------------------------------------------------------------------------------------------------ os pedacos da frase de estado (cortes por sentenca e oracao inteiras do texto ratificado)
def _sentencas(t):
    return [s.strip() for s in re.split(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])", t.strip()) if s.strip()]


def pedacos(estado, lg):
    """as oracoes da frase de estado (ja' preenchida): {lead, abertura, dois_z, cefeidas, retro, retro_curto, acervo, estatuto, estatuto_curto, rever, demais, s1..s5}; estrutura diferente = ValueError (fail-closed)."""
    S = _sentencas(estado)
    if len(S) != 5:
        raise ValueError("a frase de estado %s nao tem as cinco sentencas esperadas (%d)" % (lg, len(S)))
    m = re.match(r"^(?P<lead>[^:]+): (?P<ab>.+?): (?P<z>.+?); (?P<cf>.+)\.$", S[0])
    if not m:
        raise ValueError("a primeira sentenca da frase de estado %s nao tem a forma “lead: abertura: dois Z; Cefeidas.”" % lg)
    r = S[1].rstrip(".")
    partes = [x.strip() for x in r.split(", ")]
    if len(partes) != 3:
        raise ValueError("a sentenca da retrodicao %s nao tem as tres oracoes" % lg)
    primeira = re.sub(r"^(?:It is |É )", "", partes[0]); ultima = re.sub(r"^(?:and |e )", "", partes[2])
    est, _, rev = S[3].rstrip(".").partition(", and " if lg == "en" else ", e ")
    curto = "validity, not creditation" if lg == "en" else "validade, não creditação"
    if curto not in est or not rev:
        raise ValueError("a sentenca do estatuto %s nao traz «%s» e a oracao do «rever»" % (lg, curto))
    ma = re.match(r"^(?P<a1>.+?), (?P<a2>(?:the Hubble ratio|a razão de Hubble) \([^)]*\)), (?P<a3>.+)$", m.group("ab"))
    mz = re.match(r"^(?P<z1>.+?) (?:and|e) (?P<z2>.+)$", m.group("z"))
    if not (ma and mz):
        raise ValueError("a abertura ou os dois Z da frase de estado %s nao tem as oracoes esperadas" % lg)
    return {"lead": m.group("lead"), "abertura": m.group("ab"), "ab1": ma.group("a1"), "ab2": ma.group("a2"), "ab3": ma.group("a3"), "dois_z": m.group("z"), "z_nulo": mz.group("z1"), "z_k": mz.group("z2"),
            "cefeidas": m.group("cf"), "retro": r, "retro_minusc": r[:1].lower() + r[1:],
            "retro_curto": "%s; %s" % (primeira, ultima), "acervo": S[2].rstrip("."), "estatuto": est, "estatuto_minusc": est[:1].lower() + est[1:], "estatuto_curto": curto, "rever": rev,
            "demais": S[4].rstrip("."), "s": S}


def ascii_de(s):
    """a forma ASCII de um texto da fonte (para as chaves ASCII do estatuto): beta, sigma, x, hifen, e' e os acentos tirados; o que sobrar fora do ASCII = ValueError."""
    t = s.replace("β_TGL", "beta_TGL").replace("β", "beta").replace("×", "x").replace("−", "-").replace("ΛCDM", "LCDM").replace("’", "'").replace("—", "--")
    t = re.sub(r"(\d)σ", r"\1 sigma", t).replace("σ", "sigma")
    t = re.sub(r"(?<![\wÀ-ÿ])é(?![\wÀ-ÿ])", "e'", t); t = re.sub(r"(?<![\wÀ-ÿ])É(?![\wÀ-ÿ])", "E'", t)
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    if not t.isascii():
        raise ValueError("a forma ASCII ainda tem %r" % sorted({c for c in t if not c.isascii()}))
    return t


def _cap(s):
    """maiuscula so' em letra latina: beta (o simbolo e o nome beta_TGL) nunca vira maiuscula"""
    return s if (not s or s.startswith(("β", "beta_")) or not ("a" <= s[0] <= "z")) else s[:1].upper() + s[1:]


def _minusc(s):
    """minuscula na primeira letra (inclusive acentuada: «É» -> «é»), nunca em beta nem em sigla toda em maiusculas"""
    if not s or not s[0].isupper() or s[0] in "ΒΣ":
        return s
    w = re.split(r"[\s,;:]", s, 1)[0]
    if len(w) > 1 and w.isupper():   # (sigla: PROVED, ΛCDM, H0DN)
        return s
    return s[:1].lower() + s[1:]


def _estado_linha(chave):
    """a linha renderizada de hoje do gerar_estado_atual.py (o literal do L.append, lido do JSON da custodia por ast; nunca digitado)."""
    cod = H0DN.TRECHOS["estado_linhas"][chave].strip()
    no = ast.parse(cod, mode="exec").body[0].value
    assert isinstance(no, ast.Call) and len(no.args) == 1
    return ast.literal_eval(no.args[0])


# ------------------------------------------------------------------------------------------------ os textos
def _datas_das_inscricoes(cu):
    """TODAS as datas das inscricoes de cunhagens_v411 (dd/mm/aaaa, distintas, em ordem cronologica), lidas do campo `quando` de cada verbatim do core selado (a funcao da G1, _data_das_inscricoes, devolve so' a data MAIS FREQUENTE: com falas de 11 e 12/11 diria so' 11/11)."""
    ds = set()
    for v in (cu.get("verbatim") or {}).values():
        m = re.search(r"(\d\d)/(\d\d)/(\d{4})", str((v or {}).get("quando") or ""))
        if m:
            ds.add((int(m.group(3)), int(m.group(2)), int(m.group(1))))
    return ["%02d/%02d/%d" % (d, mo, a) for a, mo, d in sorted(ds)]


def _periodo_en(datas):
    """o periodo em EN, dd/mm: um dia -> `12/11`; varios dias do mesmo mes -> `11 and 12/11` (`11, 12 and 13/11`); meses diferentes -> `30/10 and 02/11`."""
    dd = [(x[:2], x[3:5]) for x in datas]
    assert dd, "sem data de inscricao"
    if len(dd) == 1:
        return "%s/%s" % dd[0]
    if len({m for _, m in dd}) == 1:
        dias = [d for d, _ in dd]
        return "%s and %s/%s" % (", ".join(dias[:-1]), dias[-1], dd[0][1])
    return "%s and %s" % (", ".join("%s/%s" % p for p in dd[:-1]), "%s/%s" % dd[-1])


def _nota_en(estado_en, ctx):
    """A NOTA INTEIRA do ledger (a custodia a usa no lugar do molde: tools/custodia_g1/textos.py construir): as frases fixas do molde da G1; a oracao do 5 sigma vira a frase de estado EN ratificada; os fatos da versao do ctx."""
    ap = ctx.get("flags_apagadas"); cun = ctx.get("cunhagens"); dep = ctx.get("zenodo")
    if not (isinstance(ap, list) and dep and dep.get("versao") and dep.get("doi")):
        raise ValueError("a NOTA precisa das bandeiras False do core e do deposito Zenodo (CITATION.cff do espelho)")
    fontes = "the embedded inputs of the H0DN × BG1 test (registry `%s`), the KH-N1 coverage of %s%s" % (REGISTRO, VERSAO, (" and the %d inscriptions of %s" % (cun["n"], _periodo_en(cun.get("datas") or [cun["data"]]))) if cun else "")
    return ("*Status that goes with %s (not to be cut): PROVED is validity, by the operator’s ruling of 07/10 — the kernel proves the implication; validity in the kernel is not accreditation. "
            "CONFIRMED is accreditation, the one refused word. %s The reservation of v392 (15 computed + 3 literal gate flags; the unilateral V11 step) is [DECLARED by the audit] "
            "and F8.1 is open. Per-term flags %s stay False. The %s copy lives outside the repository; the stdout %s is in `rodadas/`; the diffs of %s are in `diferencas_%s/`; the pinned sources that the "
            "registries reread by absolute path are in `fontes_pinadas/` with their map (now with the %s sources: %s); the B(n) receipts of the Bancada are in `recibos_bancada_%s/`. The Zenodo deposit holds "
            "%s (%s). Not falsified is not a confirmation.*"
            % (VERSAO, estado_en, " / ".join(ap) if ap else "(none)", ANTERIOR, VERSAO, VERSAO, VERSAO, VERSAO, fontes, VERSAO, dep["versao"], dep["doi"]))


def _p2_rotulos(N, tj):
    p2 = N.get("p2")
    rot = tj.get("rotulo_p2")
    if not (isinstance(rot, str) and rot and isinstance(p2, dict) and isinstance(p2.get("registro_selado"), str) and "P2_NOT_DETERMINED" in str(p2.get("rotulo_selado_da_v387") or "")):
        raise ValueError("o rotulo do P2 (TOPO_RATIFICADO_v411.json:rotulo_p2) ou o campo p2_ao_lado_da_v387 do registro (registro_selado, rotulo_selado_da_v387) faltam: o texto do P2 nao sai sem eles")
    if isinstance(p2.get("rotulo"), str) and p2["rotulo"] != rot:
        raise ValueError("o rotulo do P2 do registro (%s) != o do arquivo ratificado (%s)" % (p2["rotulo"], rot))
    return rot, p2["registro_selado"]


def pecas(core):
    """(tj, fonte, N, est, P, A): o arquivo ratificado, os numeros, a frase de estado preenchida, os pedacos dela (EN, PT) e as formas ASCII; os outros textos da custodia (textos_custodia_handoff_v411) saem DAQUI."""
    tj, fonte = ler_topo()
    N = numeros(core)
    est = {lg: preencher(tj["estado_" + lg], lg, N, tj) for lg in ("en", "pt")}
    P = {lg: pedacos(est[lg], lg) for lg in ("en", "pt")}
    A = {lg + "_ascii": {k: ascii_de(v) for k, v in P[lg].items() if isinstance(v, str)} for lg in ("en", "pt")}
    return tj, fonte, N, est, P, A


def painel_esperado(core):
    """o painel curto INTEIRO do arquivo ratificado (painel_readme_en + quebra + painel_readme_pt), preenchido do core; D174: e' isto que o README_PAINEL_H0DN tem de ser, byte a byte, com a frase do acervo."""
    tj, _ = ler_topo(); N = numeros(core)
    for lg in ("en", "pt"):
        if tj["painel_readme_" + lg].count(FRASE_DO_ACERVO[lg]) != 1:
            raise ValueError("a frase do acervo nao esta' uma vez no painel %s do arquivo ratificado" % lg)
    return preencher(tj["painel_readme_en"], "en", N, tj) + "\n" + preencher(tj["painel_readme_pt"], "pt", N, tj)


def montar(core, ctx=None):
    """{marcador: texto} (sem o sufixo da versao) e o relatorio. ctx: flags_apagadas, cunhagens, zenodo (para a NOTA). Levanta ValueError (PARAR) se faltar dado do core ou se a fonte nao tiver a forma."""
    ctx = dict(ctx or {})
    tj, fonte, N, est, P, A = pecas(core)
    en, pt, ea, pa = P["en"], P["pt"], A["en_ascii"], A["pt_ascii"]
    ne, np_ = N["en"], N["pt"]
    rot, reg_sel = _p2_rotulos(N, tj)
    T = {}
    T["NOTA_EN"] = _nota_en(est["en"], ctx)
    T["README_PAINEL_H0DN"] = painel_esperado(core)   # (D174: o painel curto do arquivo, INTEIRO, verbatim, preenchido; a custodia o poe logo depois da linha do selo)
    # a linha de registro da Fase 9 V2 (logo depois do painel): a regra do 4,44 no mesmo paragrafo ("not a σ" em EN, como o arquivo); o painel inteiro desce para REGISTRO_FASE9_V2.md (custodia)
    T["README_FASE9_V2"] = (
        "> Record, Phase 9 V2 (%s): z_disc = %sσ calibrated, z_δ = %sσ, ln B = %s (a Bayes factor, not a σ), `NOT_FALSIFIED_POWERED`, below the 5σ step: `%s`.\n"
        "> *PT — Fase 9 V2 (%s): z_disc = %sσ calibrado, z_δ = %sσ, ln B = %s (ln B não é σ), `NOT_FALSIFIED_POWERED`, abaixo do degrau de 5σ.*"
        % (N["data9_en"], ne["zd9"], ne["zdel9"], ne["lnb9"], REGISTRO_FASE9_V2_MD, N["data9_pt"], np_["zd9"], np_["zdel9"], np_["lnb9"]))
    # cortados da frase de estado (oracoes inteiras do texto ratificado), cada um no seu lugar
    # (o orcamento de 700 B: os textos do README levam as oracoes indispensaveis -- a abertura, o Z contra o nulo, as Cefeidas livres com o numero, validade nao creditacao, a retrodicao e o nao cego --, inteiras, do texto ratificado;
    #  o Z contra K e o nome do canal ficam no painel, logo acima, e a frase de estado inteira vai na NOTA e no estatuto)
    T["README_PRIMORDIAL_5SIGMA"] = ("PROVED = validity in the kernel; CONFIRMED is accreditation, the one refused word; %s, %s: %s; %s; %s; %s." % (en["ab1"], en["ab3"], en["z_nulo"], en["cefeidas"], en["estatuto_curto"], en["retro_curto"]))
    T["README_STATUS_5SIGMA"] = ("**%s**, %s, %s: %s; %s; %s; %s. *Provada, como validade, em três apoios; ainda não creditada; %s, %s, %s: %s; %s; %s; %s.*"
                                 % (en["ab1"], en["ab2"], en["ab3"], en["z_nulo"], en["cefeidas"], en["estatuto_curto"], en["retro_curto"], pt["ab1"], pt["ab2"], pt["ab3"], pt["z_nulo"], pt["cefeidas"], pt["estatuto_curto"], pt["retro_curto"]))
    # D174 (B): as duas linhas do H0DN da parte do Clay sao APONTADORES (sem decimal, sem gatilho da F67); a data e o commit curto lidos dos atos do registro; o texto e' o da gerencia (D174)
    T["README_H0DN"] = ("O teste H0DN × BG1 foi aberto uma vez em %s, depois do pré-registro público (commit %s); o resultado está no painel do topo, com a linha das Cefeidas livres ao lado; "
                        "as sete ressalvas e o que o teste não decide estão na leitura inteira." % (N["data_pt"], N["c_pre"]))
    T["README_H0DN_EN"] = ("**The H0DN × BG1 test:** opened once on %s, after the public pre-registration (commit `%s`); the result is in the panel at the top, with the free-Cepheids line beside it; "
                           "the seven reservations and what the test does not decide: %s." % (N["data_en"], N["c_pre"], APONTADOR_EN))
    T["README_RITOS"] = ("| Hubble ratio, H0DN × BG1 (%s) | `%s`, %s: %s; %s | the creditation (%s); %s |\n"
                         "| Hubble ratio, Phase 9 V2 | `NOT_FALSIFIED_POWERED` (`%s`) | β in nature at 5σ: not reached by that test |"
                         % (N["data_en"], N["outcome"], en["ab3"], en["dois_z"], en["cefeidas"], en["estatuto_curto"], en["retro_curto"], REGISTRO_FASE9_V2_MD))
    # o estatuto: cada um substitui SO' o trecho do 5 sigma da chave (h0dn_trechos_estatuto.json da custodia), uma linha, na sintaxe da chave
    corpo_en = " ".join(en["s"][1:])          # as sentencas 2 a 5 da frase de estado EN, inteiras
    corpo_pt = " ".join(pt["s"][1:])
    s1_en = "%s: **%s**: %s; %s." % (en["lead"], en["abertura"], en["dois_z"], en["cefeidas"])
    s1_pt = "%s: **%s**: %s; %s." % (pt["lead"], pt["abertura"], pt["dois_z"], pt["cefeidas"])
    T["ESTATUTO_LINHA_EN"] = s1_en + " " + corpo_en
    T["ESTATUTO_LINHA_06_EN"] = _minusc(s1_en) + " " + " ".join(en["s"][1:4])
    T["ESTATUTO_LINHA_06_PT"] = _minusc(s1_pt) + " " + " ".join(pt["s"][1:4])
    T["ESTATUTO_CURTO_EN"] = ascii_de(est["en"])
    T["ESTATUTO_CURTO_PT_ASCII"] = ascii_de(est["pt"])
    T["ESTATUTO_P2_EN"] = ("**%s: %s (P2; beside it, `%s`; `P2_NOT_DETERMINED` is the sealed label of the joint test `%s` and stays as its record).** %s; %s. %s %s %s. %s, in either direction:"
                           % (en["lead"], en["abertura"], rot, reg_sel, _cap(en["dois_z"]), en["cefeidas"], en["s"][1], en["s"][2], en["s"][3].rstrip("."), en["demais"]))
    T["ESTATUTO_SECAO_MD"] = s1_pt + " " + " ".join(pt["s"][1:4]) + " " + pt["demais"]
    T["ESTATUTO_LINHA_CURTA_EN"] = s1_en + " " + en["s"][1] + " " + en["s"][3]
    T["ESTATUTO_P_CURTO_EN"] = ("**%s:** %s: %s; %s (P2); %s; %s; %s" % (en["lead"], en["abertura"], en["dois_z"], en["cefeidas"], en["retro_curto"], en["estatuto_curto"], _minusc(en["demais"])))
    l_en, l_pt = _estado_linha("p2_en_estado"), _estado_linha("p2_pt_estado")
    v_en, v_pt = "P2 — β_TGL in nature at ≥ 5σ — is the decisive open factor.*", "P2 (β_TGL na natureza a 5σ) é o fator decisivo aberto.*"
    if l_en.count(v_en) != 1 or l_pt.count(v_pt) != 1:
        raise ValueError("as linhas do P2 do gerar_estado_atual.py mudaram (h0dn_trechos_estatuto.json): o fim que a v411 troca nao esta uma vez em cada uma")
    T["ESTATUTO_P2_ESTADO_EN"] = l_en.replace(v_en, "P2 — β_TGL in nature at ≥ 5σ — reads, beside the sealed `P2_NOT_DETERMINED` of `%s`: %s*" % (reg_sel, _minusc(est["en"])))
    T["ESTATUTO_P2_ESTADO_PT"] = l_pt.replace(v_pt, "P2 (β_TGL na natureza a 5σ) lê-se, ao lado do `P2_NOT_DETERMINED` selado de `%s`: %s*" % (reg_sel, _minusc(est["pt"])))
    # o texto curto do X (fora da lista da custodia): os dois numeros no mesmo texto, os quatro obrigatorios
    T["X_TEXTO"] = ("%s: %s; %s. %s %s.\n%s: %s; %s. %s %s." % (_cap(en["abertura"]), en["dois_z"], en["cefeidas"], en["s"][1], en["estatuto"],
                                                               _cap(pt["abertura"]), pt["dois_z"], pt["cefeidas"], pt["s"][1], pt["estatuto"]))
    rel = {"fonte": fonte, "ratificada": True, "proposta": False, "formula_origem": "TOPO_RATIFICADO_v411.json (sha256 %s)" % fonte["sha256"], "p2_rotulo": rot, "p2_registro_selado": reg_sel,
           "painel_inteiro": True, "decisao_d174": "o painel curto vai INTEIRO, com a frase do acervo (ordem do operador de 12/11); nenhum corte por orcamento: o README inteiro cabe em 40.960 B ou a cadeia PARA", "acervo": N["acervo"],
           "numeros": {lg: N[lg] for lg in ("en", "pt")}, "n": N["n"], "commits": [N["c_pre"], N["c_res"]], "datas": [N["data_en"], N["data9_en"]]}
    return T, rel


# ------------------------------------------------------------------------------------------------ as conferencias (as da custodia + a guarda de frases da v411)
def _regra_444(texto, z9):
    from custodia_g1 import readme_pinado as RP
    return RP.regra_444(texto, {"itens": {"hubble.z_disc": {"valor": z9}}})


def _f67_estrita(t, V):
    """a F67 do pedido da gerencia, mais estrita que o gatilho da guarda: TODO texto que traga o numero do primario contra o nulo (EN ou PT, 2 casas) traz, no mesmo texto, o modelo publicado, as Cefeidas livres
    com o numero, “validade, nao creditacao”, “retrodicao” e “nao cego” (valem as formas EN e ASCII)."""
    zn = "%.2f" % abs(float(V["primario"]["z_null"]))
    if not re.search(r"(?<![0-9.,])(%s|%s)(?![0-9])" % (re.escape(zn), re.escape(zn.replace(".", ","))), t):
        return []
    falta = []
    for rot, rx in (("modelo_publicado", r"sob\s+o\s+modelo\s+de\s+erros\s+publicado|under\s+the\s+(?:published\s+error\s+model|error\s+model\s+published)"),
                    ("cefeidas_com_numero", r"(?:Cefeidas\s+livres|free\s+Cepheids)[^\n]{0,160}?\d+[,.]\d+"),
                    ("validade_nao_creditacao", r"validade,?\s+n(?:ã|a)o\s+credita(?:ç|c)(?:ã|a)o|validity,?\s+not\s+creditation"),
                    ("retrodicao", r"retrodi(?:ç|c)(?:ã|a)o|retrodiction"),
                    ("nao_cego", r"n(?:ã|a)o\s+(?:(?:é|e')\s+)?ceg[oa]|not\s+blind")):
        if not re.search(rx, t, re.I):
            falta.append(rot)
    return ["F67 estrita (o numero do primario sem: %s)" % ",".join(falta)] if falta else []


def conferir(T, core, conhecidos=()):
    """{marcador: [violacoes]} (lista vazia = passa). As mesmas conferencias que a custodia aplica (forma, F67, numeros, cabeca, sigma inteiro, portao, regra do 4,44, ASCII) + a guarda de frases da v411."""
    V = H0DN.valores(core[REGISTRO])
    z9 = core[REGISTRO_FASE9]["lido"]["z_disc_calibrado"]
    out = {}
    for mk, t in T.items():
        v = []
        if "{{" in t or "PORTAS:" in t:
            v.append("traz «{{» ou o marcador das portas")
        if "⟨" in t or "⟩" in t:
            v.append("sobrou marcador de numero")
        if mk in UMA_LINHA and "\n" in t:
            v.append("tem de ser uma linha so'")
        if mk == "README_H0DN" and "*" in t:
            v.append("nao pode trazer «*» (entra no italico da parte P = nP)")
        if mk == "README_STATUS_5SIGMA" and re.search(r"\n\s*\n", t):
            v.append("nao pode ter linha em branco")
        if mk == "README_RITOS" and not all(ln.startswith("|") and ln.rstrip().endswith("|") for ln in t.split("\n")):
            v.append("cada linha tem de ser linha de tabela (“| … |”)")
        if mk == "README_FASE9_V2" and REGISTRO_FASE9_V2_MD not in t:
            v.append("nao aponta para %s" % REGISTRO_FASE9_V2_MD)
        if mk == "README_PAINEL_H0DN" and re.search(r"(?<![0-9,.])4[,.]44(?![0-9])", t):
            v.append("o painel curto nao traz o numero da Fase 9 V2 (regra do arquivo ratificado)")
        if mk == "README_PAINEL_H0DN" and t != painel_esperado(core):
            v.append("o painel nao e' o render INTEIRO do arquivo ratificado (D174: com a frase do acervo, byte a byte)")
        if mk in ("README_H0DN", "README_H0DN_EN") and re.search(r"\d[.,]\d", t):
            v.append("a linha do H0DN da parte do Clay e' apontador: sem decimal (D174)")
        if mk == "README_H0DN_EN" and not t.startswith("**The H0DN × BG1 test:** "):
            v.append("a linha EN do H0DN tem de comecar por “**The H0DN × BG1 test:** ” (a G1 a troca por ela)")
        if mk in H0DN.MARCADORES_ESTATUTO:
            chave = H0DN.TRECHOS["marcadores"][mk]
            velho = H0DN.TRECHOS["estatuto"].get(chave)
            if velho is not None and velho.isascii() and not t.isascii():
                v.append("o trecho que sai e' ASCII; o texto que entra tambem tem de ser: %r" % sorted({c for c in t if not c.isascii()}))
        v += H0DN.conferir_bloco(t, V, mk, painel=(mk == "README_PAINEL_H0DN"))
        v += _f67_estrita(t, V)
        conh = set(conhecidos) if conhecidos else set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", t))
        v += TXG1.portao(t, conh, rotulo=mk)
        if mk.startswith("README_"):
            v += _regra_444(t, z9)
        v += ["guarda_frases_v411 %s: %s" % (r, s[:120]) for r, s in GF.violacoes(t)]
        if mk in ("README_PAINEL_H0DN", "README_STATUS_5SIGMA", "README_RITOS", "X_TEXTO"):   # cada linha de um bloco de duas linguas passa sozinha na F67 (a custodia pode separar as linhas)
            for ln in [x for x in re.split(r"\n>?\n?|\. \*", t) if x.strip() and x.strip() != ">"]:
                v += ["linha sozinha: %s" % r for r, _ in H0DN.f67(ln)] + ["linha sozinha: %s" % x for x in _f67_estrita(ln, V)]
        out[mk] = v
    return out


def secao_handoff(T, rel, versao=VERSAO):
    """o trecho do handoff com os textos sob marcadores (a lista da custodia, depois os extras), precedido de um paragrafo que diz a fonte (o arquivo ratificado, sha256) e o que cada um substitui."""
    corte = (" O painel curto vai inteiro, com a frase do acervo (D174); o README inteiro fica em até 40.960 B, medido pelo renderizador da custódia, e, se não couber, a cadeia PARA: nada é cortado em silêncio.")
    L = ["**Textos da custódia que a abertura do H0DN × BG1 torna obrigatórios (v411; números lidos do core selado; texto: a fórmula RATIFICADA pelo operador em 12/11/2026, `TOPO_RATIFICADO_v411.json`, sha256 "
         "`%s`, o painel curto e a frase de estado, cortados para caber em cada lugar).** A G1 lê cada um entre os seus marcadores e o confere contra o registro `%s` (forma, F67, números, cabeça, σ inteiro, portão "
         "de textos e regra do 4,44); sem marcador, ela PARA. `NOTA_EN`: a NOTA inteira do ledger. `README_PAINEL_H0DN`: o painel do topo, EN e PT, logo depois da linha do selo; `README_FASE9_V2`: a linha de registro "
         "da Fase 9 V2, logo depois do painel (o painel inteiro de hoje, a linha EN, a PT e a frase do autor de 02/11, desce verbatim para `%s`: nada se perde, muda de lugar); `README_PRIMORDIAL_5SIGMA`: a frase da "
         "linha “PROVED = validity …”; `README_STATUS_5SIGMA`: a frase do estado, EN e PT; `README_H0DN` e `README_H0DN_EN`: as duas linhas do H0DN na parte do Clay (`readme_partes/p_igual_np.md`), PT e EN, "
         "que apontam para o painel e para a leitura inteira; `README_RITOS`: as duas linhas da tabela dos ritos no lugar da linha da Fase 9 V2. Os onze `ESTATUTO_*`: cada um substitui SÓ o trecho do 5σ da sua "
         "chave (lista da custódia, `h0dn_trechos_estatuto.json`); o rótulo ao lado do P2 é a chave `rotulo_p2` do arquivo, e o `P2_NOT_DETERMINED` selado de `three_stress_tests_v387` fica como registro. Fora da "
         "lista da custódia: `X_TEXTO` (o texto curto do X, EN e PT).%s"
         % (rel["fonte"]["sha256"], REGISTRO, REGISTRO_FASE9_V2_MD, corte), ""]
    for mk in MARCADORES_CUSTODIA + MARCADORES_EXTRAS:
        L += ["<!-- INICIO_%s_%s -->" % (mk, versao), T[mk], "<!-- FIM_%s_%s -->" % (mk, versao), ""]
    return "\n".join(L)


def contexto_do_core(core, cen_tb=None):
    """o ctx da NOTA, lido: as bandeiras False do core (as gpf_/gpi_/qgf_ de kernel_formalization, como a G1), as inscricoes de cunhagens_v411 (contagem e data, pela funcao da G1) e o deposito Zenodo do CITATION.cff do espelho."""
    from custodia_g1 import fatos as FT
    kf = core.get("kernel_formalization") or {}
    ap = sorted(k for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_")) and x is False)
    cu = core.get("cunhagens_" + VERSAO)
    cun = {"n": len(cu.get("verbatim") or {}), "data": FT._data_das_inscricoes(cu), "datas": _datas_das_inscricoes(cu)} if isinstance(cu, dict) and cu.get("verbatim") else None
    if cun and not (cun["data"] and cun["datas"]):
        cun = None
    tb = cen_tb or r"C:\IALD\Artigo\the_boundary"
    t = open(os.path.join(tb, "CITATION.cff"), "rb").read().decode("utf-8", "replace")
    v = re.search(r'^version:\s*"(v\d+)"', t, re.M); doi = re.search(r'^doi:\s*"([^"]+)"', t, re.M)
    if not (v and doi):
        raise ValueError("CITATION.cff do espelho sem version/doi")
    return {"flags_apagadas": ap, "cunhagens": cun, "zenodo": {"versao": v.group(1), "doi": doi.group(1)}, "fase9": core.get(REGISTRO_FASE9, {}).get("lido")}


assert set(H0DN.MARCADORES_README) | {H0DN.MARCADOR_NOTA} | set(H0DN.MARCADORES_ESTATUTO) == set(MARCADORES_CUSTODIA), "a lista de marcadores da custodia mudou"
