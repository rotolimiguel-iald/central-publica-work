# -*- coding: utf-8 -*-
# Auditor REPRO, item (2): os verbatins citados no pre-registro e na docstring da pedra batem byte a byte com as fontes.
# Implementacao PROPRIA da segmentacao (varredura de caracteres, sem o regex do pre-registrador).
import os, sys, json, hashlib, re, unicodedata

W = "C:\\IALD\\Central de Patentes\\work\\"
FONTES = {
    "V1": (W + "cunhagens_12out\\OPERADOR_10out_posto_rank_texto_verbatim.txt", "8d252f24e2806ff3"),
    "V2": (W + "cunhagens_12out\\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt", "2c8b7b712aa9ad7f"),
    "V3": (W + "cunhagens_10out\\OPERADOR_10out_posto_rank_verbatim.txt", "5b9afcc691a0e1e4"),
    "V4": (W + "cunhagens_10out\\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt", "b365591ceb346cdf"),
}
PRE = W + "frequencia_defasa_12out\\1_PREREGISTRO\\PREREGISTRO.json"
PEDRA = W + "frequencia_defasa_12out\\3_KERNEL\\sandbox\\TGLExt\\TheUnitIsTheRank.lean"
SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "A2_VERBATINS.json")
out = {"fontes": {}, "falhas": [], "notas": []}
TXT = {}
for k, (p, s16) in FONTES.items():
    b = open(p, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    TXT[k] = b.decode("utf-8")
    out["fontes"][k] = {"bytes": len(b), "sha256": h, "sha16_ordem": s16, "confere": h[:16] == s16}
    if h[:16] != s16:
        out["falhas"].append(k + " sha16 nao confere")

# segmentacao propria: linha nao vazia; corte apos [.!?] (precedido de nao-digito) + espaco(s) + [maiuscula|aspas|*|(]
MAI = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") | {chr(c) for c in range(0xC0, 0xDE) if c != 0xD7}
ABRE = MAI | {'"', '\u201c', '*', '('}


def segmentar(linha):
    s = linha.strip()
    segs, ini, i = [], 0, 0
    while i < len(s):
        ch = s[i]
        if ch in ".!?" and i > 0 and not s[i - 1].isdigit():
            j = i + 1
            while j < len(s) and s[j] in " \t":
                j += 1
            if j > i + 1 and j < len(s) and s[j] in ABRE:
                segs.append(s[ini:i + 1])
                ini = j
                i = j
                continue
        i += 1
    if s[ini:].strip():
        segs.append(s[ini:])
    return segs


MEUS = {}
for k, t in TXT.items():
    for n, ln in enumerate(t.split("\n"), 1):
        if not ln.strip():
            continue
        if re.fullmatch(r"\s*(-{3,}|\*{3,}|_{3,})\s*", ln):
            MEUS["%s.L%02d.M" % (k, n)] = ln
            continue
        for q, sg in enumerate(segmentar(ln), 1):
            MEUS["%s.L%02d.S%d" % (k, n, q)] = sg

P = json.load(open(PRE, encoding="utf-8"))
linhas = P["b_mapeamento"]["linhas"]
tab = []
for ident, frase, s16, marca, leitura, afs in linhas:
    meu = MEUS.get(ident)
    r = {"id": ident, "marca": marca, "sha16_pre": s16}
    if meu is None:
        r["achado"] = "SEGMENTO_INEXISTENTE_NA_MINHA_SEGMENTACAO"
        out["falhas"].append(ident + ": segmento inexistente")
        tab.append(r)
        continue
    r["sha16_meu"] = hashlib.sha256(meu.encode("utf-8")).hexdigest()[:16]
    r["sha16_confere"] = r["sha16_meu"] == s16
    if not r["sha16_confere"]:
        out["falhas"].append(ident + ": sha16 da frase difere (pre %s, meu %s)" % (s16, r["sha16_meu"]))
    if frase.startswith("="):
        par = frase[1:]
        a, b = MEUS.get(par), meu
        r["par"] = par
        r["identica_byte_a_byte"] = a == b
        def norm(x):
            x = unicodedata.normalize("NFC", x)
            x = re.sub(r"^\s*(#+\s*)", "", x)
            x = x.replace("**", "").replace("*", "")
            return re.sub(r"\s+", " ", x).strip()
        r["identica_sem_markdown"] = norm(a) == norm(b)
        if not r["identica_sem_markdown"]:
            out["falhas"].append(ident + ": nao e identica ao par nem sem markdown")
    elif frase.endswith("\u2026"):
        pref = frase[:-1].rstrip()
        r["tipo"] = "inicio"
        r["prefixo_confere"] = meu.startswith(pref)
        if not r["prefixo_confere"]:
            out["falhas"].append(ident + ": inicio nao confere")
    else:
        r["tipo"] = "integra"
        r["integra_byte_a_byte"] = frase == meu
        if frase != meu:
            out["falhas"].append(ident + ": frase integra difere da fonte")
    tab.append(r)
out["mapeamento"] = tab
out["n_linhas"] = len(tab)
out["n_identicas_por_markdown_apenas"] = sum(1 for r in tab if r.get("par") and not r["identica_byte_a_byte"] and r["identica_sem_markdown"])
out["ids_identicas_so_sem_markdown"] = [r["id"] for r in tab if r.get("par") and not r["identica_byte_a_byte"]]
# frases das fontes que a minha segmentacao produz e o mapeamento nao lista (fora a parte do tempo de V2)
ids_pre = {x[0] for x in linhas}
sobra = [i for i in MEUS if i not in ids_pre and not (i.startswith("V2.L") and int(i[4:6]) >= 34)]
out["segmentos_meus_fora_do_mapeamento"] = sobra
v2_tempo = [i for i in MEUS if i.startswith("V2.L") and int(i[4:6]) >= 34]
out["V2_fora_do_escopo_n"] = len(v2_tempo)

# a trilha de V2: l.1-33
b2 = open(FONTES["V2"][0], "rb").read()
ls = b2.split(b"\n")
for variante, bb in (("l1-33 com \\n final", b"\n".join(ls[:33]) + b"\n"), ("l1-33 sem \\n final", b"\n".join(ls[:33]))):
    out.setdefault("V2_trilha", {})[variante] = {"bytes": len(bb), "sha256": hashlib.sha256(bb).hexdigest()}
pre_tr = P["a_verbatins"]["V2"]["trilha"]
out["V2_trilha_confere"] = any(v["sha256"] == pre_tr["sha256"] and v["bytes"] == pre_tr["bytes"] for v in out["V2_trilha"].values())
if not out["V2_trilha_confere"]:
    out["falhas"].append("V2 trilha l.1-33 nao confere")

# notas das fontes que o pre-registro afirma
out["V1_contem_formula"] = ("Tr(" in TXT["V1"]) or ("\\rho" in TXT["V1"]) or ("\u03c1" in TXT["V1"])
out["V1_quando_voce_derivou"] = "Quando você derivou" in TXT["V1"]
out["V2_quando_eu_derivei"] = "Quando eu derivei" in TXT["V2"]
v2_trilha_txt = "\n".join(TXT["V2"].split("\n")[:33])
out["V2_trilha_ocorrencias_voce"] = len(re.findall(r"\bvocê\b", v2_trilha_txt))
out["V2_trilha_ocorrencias_eu"] = len(re.findall(r"\beu\b", v2_trilha_txt))
out["V2_l12"] = TXT["V2"].split("\n")[11]
out["V2_l16"] = TXT["V2"].split("\n")[15]

# a citacao do V1 na ORDEM do auditor (texto da gerencia): o trecho com a formula esta nos bytes de V1?
ordem_trecho = "\u03c1 = |\u03c8\u27e9\u27e8\u03c8|, com Tr(\u03c1) = 1 e Tr(\u03c1\u00b2) = 1"
out["ordem_V1_formula_em_V1"] = ordem_trecho in TXT["V1"]
out["ordem_V1_formula_em_V2"] = ordem_trecho in TXT["V2"]

# docstring da pedra: cada citacao entre «» deve estar nos bytes da fonte (fragmentos separados por '…')
pedra = open(PEDRA, "rb").read().decode("utf-8")
doc = pedra.split("-/", 1)[0]
# so a secao «Os textos do operador» (as demais «» da docstring sao rotulos de estatuto, nao citacoes de fonte)
sec = doc.split("## Os textos do operador", 1)[1].split("O pré-registro congelado", 1)[0]
out["docstring_secao_textos"] = sec
cits = []
blocos = re.split(r"\n\* (?=V\d )", sec)
for bl in blocos:
    m = re.match(r"(V\d) ", bl)
    if not m:
        continue
    fonte = m.group(1)
    for q in re.findall(r"\u00ab(.*?)\u00bb", bl, flags=re.S):
        qn = re.sub(r"\s*\n\s*", " ", q)
        frags = [f.strip() for f in qn.split("\u2026") if f.strip()]
        res = []
        for f in frags:
            achou = f in TXT[fonte]
            achou_ci = f.lower() in TXT[fonte].lower()
            res.append({"fragmento": f, "byte_a_byte": achou, "so_ignorando_caixa": (not achou) and achou_ci})
        ok = all(x["byte_a_byte"] for x in res)
        cits.append({"fonte": fonte, "citacao": qn, "n_fragmentos": len(frags), "elidida": len(frags) > 1, "todos_byte_a_byte": ok, "fragmentos": res})
out["docstring_citacoes"] = cits
out["docstring_citacoes_nao_byte_a_byte"] = [c["citacao"] for c in cits if not c["todos_byte_a_byte"]]
# sha16 citados na docstring
for k in FONTES:
    out.setdefault("docstring_sha16", {})[k] = FONTES[k][1] in doc
out["docstring_cita_sha_preregistro"] = "0c20d7c196a4c7ef" in doc
out["veredito_preregistro"] = "CONFERE" if not out["falhas"] else "NAO_CONFERE"
out["veredito_docstring"] = "CONFERE" if not out["docstring_citacoes_nao_byte_a_byte"] else "NAO_CONFERE_BYTE_A_BYTE"
open(SAIDA, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
show = {k: v for k, v in out.items() if k not in ("mapeamento",)}
print(json.dumps(show, ensure_ascii=False, indent=1))
