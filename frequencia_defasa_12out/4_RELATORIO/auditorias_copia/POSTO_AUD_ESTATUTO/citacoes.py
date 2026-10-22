# -*- coding: utf-8 -*-
# Confere as citacoes «...» atribuidas ao operador (V1-V4) nos artefatos da unidade:
# cada fragmento (separado por reticencias) tem de aparecer NA ORDEM nos bytes de algum V.
# Somente leitura; grava so na pasta do auditor.
import os, re, json, hashlib, unicodedata
AQUI = os.path.dirname(os.path.abspath(__file__))
CP = r"C:\IALD\Central de Patentes"
W = CP + r"\work\frequencia_defasa_12out"
V = {
 "V1": CP + r"\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
 "V2": CP + r"\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "V3": CP + r"\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
 "V4": CP + r"\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
}
TXT = {k: open(p, "rb").read().decode("utf-8") for k, p in V.items()}
def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("**", "").replace("*", "").replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()
NT = {k: norm(v) for k, v in TXT.items()}
ARQ = {
 "LEVANTAMENTO.md": W + r"\0_LEVANTAMENTO\LEVANTAMENTO.md",
 "PREREGISTRO.md": W + r"\1_PREREGISTRO\PREREGISTRO.md",
 "RESULTADO_OPTICO.json": W + r"\2_OPTICO\RESULTADO_OPTICO.json",
 "RESULTADO_KERNEL.json": W + r"\3_KERNEL\RESULTADO_KERNEL.json",
 "TheUnitIsTheRank.lean": W + r"\3_KERNEL\sandbox\TGLExt\TheUnitIsTheRank.lean",
}
def em_ordem(frags, alvo):
    pos = 0
    for f in frags:
        i = alvo.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return True
saida = {}
for nome, p in ARQ.items():
    s = open(p, "rb").read().decode("utf-8")
    if p.endswith(".json"):
        s = json.dumps(json.loads(s), ensure_ascii=False)
    quotes = re.findall(r"«([^«»]{3,600})»", s)
    res = []
    for q in quotes:
        qn = norm(q)
        frags = [norm(f) for f in re.split(r"…|\.\.\.", qn) if norm(f)]
        # sem distincao de caixa na primeira letra de cada fragmento
        hits = [k for k, t in NT.items() if em_ordem(frags, t)]
        hits_ci = [k for k, t in NT.items() if em_ordem([f.lower() for f in frags], t.lower())]
        cruza_frase = False
        if hits_ci and not hits:
            estado = "SO_COM_CAIXA_ALTERADA"
        elif hits:
            estado = "VERBATIM" if len(frags) == 1 else "VERBATIM_COM_RETICENCIAS"
        else:
            estado = "NAO_ENCONTRADA_NOS_V"
        res.append({"citacao": q, "estado": estado, "em": hits or hits_ci, "n_fragmentos": len(frags)})
    saida[nome] = res
resumo = {}
for nome, res in saida.items():
    c = {}
    for r in res:
        c[r["estado"]] = c.get(r["estado"], 0) + 1
    resumo[nome] = c
json.dump({"resumo": resumo, "detalhe": saida}, open(os.path.join(AQUI, "CITACOES_CONFERIDAS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(resumo, ensure_ascii=False, indent=1))
for nome, res in saida.items():
    for r in res:
        if r["estado"] != "VERBATIM" and r["estado"] != "VERBATIM_COM_RETICENCIAS":
            print(nome, "|", r["estado"], "|", r["citacao"][:200])
