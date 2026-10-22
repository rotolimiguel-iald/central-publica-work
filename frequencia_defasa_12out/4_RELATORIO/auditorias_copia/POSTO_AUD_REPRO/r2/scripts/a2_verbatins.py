# -*- coding: utf-8 -*-
"""A2 -- auditor REPRO r2: os verbatins citados no pre-registro e na docstring da pedra batem byte a byte?

Implementacao PROPRIA (nao importa segmentar.py do pre-registrador):
  (1) hashes de V1..V4 contra os sha16 da ordem; recorte V2 l.1-33 (LF, sem LF final) contra 2852 B / aa132de8...;
  (2) segmentacao propria pela regra escrita no pre-registro (b_segmentacao), sha16 de cada frase, e confronto
      linha a linha com PREREGISTRO.json:b_mapeamento (texto integral, inicio, ou '=id');
  (3) toda citacao entre « » na pedra r2 (e no PREREGISTRO.md) procurada BYTE A BYTE em V1..V4 e no um.py
      (com ' … ' tratado como corte; as partes devem aparecer em ordem no MESMO arquivo).
"""
import hashlib, json, os, re, sys, unicodedata

W = r"C:\IALD\Central de Patentes\work"
FONTES = {
    "V1": os.path.join(W, r"cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt"),
    "V2": os.path.join(W, r"cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
    "V3": os.path.join(W, r"cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt"),
    "V4": os.path.join(W, r"cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"),
}
SHA16 = {"V1": "8d252f24e2806ff3", "V2": "2c8b7b712aa9ad7f", "V3": "5b9afcc691a0e1e4", "V4": "b365591ceb346cdf"}
UMPY = os.path.join(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um", "N\u00f3s", "um.py")
PRE = os.path.join(W, r"frequencia_defasa_12out\1_PREREGISTRO")
PEDRA = os.path.join(W, r"frequencia_defasa_12out\3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "A2_VERBATINS.json")

res = {}
B = {k: open(p, "rb").read() for k, p in FONTES.items()}
T = {k: b.decode("utf-8") for k, b in B.items()}
res["hashes"] = {k: {"bytes": len(B[k]), "sha256": hashlib.sha256(B[k]).hexdigest(),
                     "sha16_ordem": SHA16[k], "confere": hashlib.sha256(B[k]).hexdigest()[:16] == SHA16[k]}
                 for k in B}
lin2 = T["V2"].split("\n")
corte = "\n".join(lin2[:33]).encode("utf-8")
res["V2_l1_33"] = {"bytes": len(corte), "sha256": hashlib.sha256(corte).hexdigest(),
                   "l34_comeca_com_O_que_mais_me_fascina": lin2[33].startswith("O que mais me fascina"),
                   "confere_2852_aa132de8": len(corte) == 2852 and hashlib.sha256(corte).hexdigest().startswith("aa132de8c79f8e8b")}
res["formula_em_V1"] = ("Tr(" in T["V1"]) or ("\\rho" in T["V1"]) or ("\u03c1" in T["V1"])
res["formula_em_V2_l16"] = lin2[15].startswith("$$\\rho = \\vert{}\\psi\\rangle")


# (2) segmentacao propria
def seg_linha(s):
    s = s.strip()
    out, ini, i = [], 0, 0
    while i < len(s):
        ch = s[i]
        if ch in ".!?" and i > 0 and not s[i - 1].isdigit():
            j = i + 1
            if j < len(s) and s[j].isspace():
                k = j
                while k < len(s) and s[k].isspace():
                    k += 1
                if k < len(s) and (s[k].isupper() or s[k] in '"\u201c*('):
                    out.append(s[ini:i + 1])
                    ini = k
                    i = k
                    continue
        i += 1
    out.append(s[ini:])
    return [x for x in out if x.strip()]


meus = {}
for k, t in T.items():
    for n, ln in enumerate(t.split("\n"), 1):
        if not ln.strip():
            continue
        if re.fullmatch(r"\s*-{3,}\s*", ln):
            meus[f"{k}.L{n:02d}.M"] = ln
            continue
        for j, f in enumerate(seg_linha(ln), 1):
            meus[f"{k}.L{n:02d}.S{j}"] = f


def s16(x):
    return hashlib.sha256(x.encode("utf-8")).hexdigest()[:16]


def norm(s):  # a normalizacao que o pre-registro declara para '=id' (markdown fora)
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"^\s*(#+\s*|\*\s+)", "", s)
    s = s.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip()


pj = json.load(open(os.path.join(PRE, "PREREGISTRO.json"), encoding="utf-8"))
linhas = pj["b_mapeamento"]["linhas"]
ids_pre = [r[0] for r in linhas]
tabela, falhas = [], []
for rid, txt, h16, marca, leit, af in linhas:
    meu = meus.get(rid)
    item = {"id": rid, "marca": marca, "sha16_pre": h16, "sha16_meu": s16(meu) if meu is not None else None}
    if meu is None:
        item["status"] = "SEGMENTO_NAO_ACHADO_NA_MINHA_SEGMENTACAO"
    else:
        item["sha16_confere"] = (s16(meu) == h16)
        if txt.startswith("="):
            ref = txt[1:]
            refm = meus.get(ref)
            item["tipo"] = "IDENTIDADE_" + ref
            item["byte_identico_ao_ref"] = (meu == refm)
            item["identico_normalizado"] = (norm(meu) == norm(refm)) if refm is not None else None
            if not item["byte_identico_ao_ref"]:
                item["diferenca"] = {"V2": meu[:160], "ref": (refm or "")[:160]}
        elif txt.endswith(" \u2026"):
            item["tipo"] = "INICIO"
            item["prefixo_confere"] = meu.startswith(txt[:-2])
        else:
            item["tipo"] = "INTEGRA"
            item["integra_byte_a_byte"] = (meu == txt)
        ok = item["sha16_confere"] and item.get("prefixo_confere", True) and item.get("integra_byte_a_byte", True) \
            and (item.get("identico_normalizado", True) is not False)
        item["status"] = "CONFERE" if ok else "NAO_CONFERE"
    if item["status"] != "CONFERE":
        falhas.append(item)
    tabela.append(item)
trilha_meus = [k for k in meus if not (k.startswith("V2.L") and int(k[4:6]) >= 34)]
res["mapeamento"] = {"n_linhas_pre": len(linhas), "n_segmentos_meus_na_trilha": len(trilha_meus),
                     "meus_fora_do_pre": [k for k in trilha_meus if k not in ids_pre],
                     "pre_fora_dos_meus": [k for k in ids_pre if k not in meus],
                     "n_confere": sum(1 for x in tabela if x["status"] == "CONFERE"),
                     "falhas": falhas,
                     "identidades_so_normalizadas": [x["id"] for x in tabela if x.get("tipo", "").startswith("IDENTIDADE")
                                                     and not x.get("byte_identico_ao_ref")]}
res["V2_fora_do_escopo_n_frases"] = len([k for k in meus if k.startswith("V2.L") and int(k[4:6]) >= 34])

# (3) citacoes « » -- pedra r2 e PREREGISTRO.md
UM = open(UMPY, "rb").read()
FONTES_B = dict(B)
FONTES_B["um.py"] = UM


def procura(q):
    partes = [p.strip() for p in re.split(r"\s*\u2026\s*", q) if p.strip()]
    achados = []
    for nome, b in FONTES_B.items():
        pos, ok = 0, True
        for p in partes:
            j = b.find(p.encode("utf-8"), pos)
            if j < 0:
                ok = False
                break
            pos = j + len(p.encode("utf-8"))
        if ok:
            achados.append(nome)
    return partes, achados


def citacoes(arq):
    t = open(arq, encoding="utf-8").read()
    qs = re.findall(r"\u00ab(.*?)\u00bb", t, flags=re.S)
    out = []
    for q in qs:
        q1 = re.sub(r"\s*\n\s*", " ", q)  # quebra de linha da docstring vira espaco
        partes, ach = procura(q1)
        if not ach and q1 != q:
            partes, ach = procura(q)
        out.append({"citacao": q1[:220], "partes": len(partes), "achada_em": ach})
    return out


for nome, arq in (("pedra_r2", PEDRA), ("PREREGISTRO.md", os.path.join(PRE, "PREREGISTRO.md"))):
    c = citacoes(arq)
    res["citacoes_" + nome] = {"n": len(c), "n_achadas": sum(1 for x in c if x["achada_em"]),
                               "nao_achadas": [x for x in c if not x["achada_em"]],
                               "achadas": [x for x in c if x["achada_em"]]}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
resumo = {k: v for k, v in res.items() if not k.startswith("citacoes")}
resumo["mapeamento"] = {k: v for k, v in res["mapeamento"].items()}
print(json.dumps(resumo, ensure_ascii=False, indent=1)[:9000])
for nome in ("pedra_r2", "PREREGISTRO.md"):
    r = res["citacoes_" + nome]
    print("==", nome, "citacoes:", r["n"], "achadas:", r["n_achadas"])
    for x in r["nao_achadas"]:
        print("   NAO ACHADA:", x["citacao"][:200])
