# -*- coding: utf-8 -*-
"""Rodada 2 — confere, byte a byte, as citações em «» da pedra r2 contra os arquivos-fonte (V1–V4 e um.py, só leitura).
Para cada citação: (a) ela aparece na pedra entre «»; (b) cada fragmento (separado por « … ») aparece, na ordem, na
LINHA indicada do arquivo-fonte (texto UTF-8 dos bytes). Além disso, lista TODAS as citações «» da pedra que mencionam
V1–V4 ou o um.py no mesmo parágrafo e não estão nesta lista (para que nada fique sem conferência).
Grava SO em 3_KERNEL\\rodada2\\CITACOES_R2.json."""
import hashlib, json, os, re, sys

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEDRA = os.path.join(R2, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
F = {
    "V1": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
    "V2": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "V3": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
    "V4": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
    "um.py": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\um.py",
}
SHA16 = {"V1": "8d252f24e2806ff3", "V2": "2c8b7b712aa9ad7f", "V3": "5b9afcc691a0e1e4", "V4": "b365591ceb346cdf",
         "um.py": "8e7b9927ceae64b8"}
CIT = [
    ("V1", 2, "a transição entre uma hipótese difusa e um formalismo fechado é precisamente uma questão de posto (rank)"),
    ("V1", 6, "um estado puro … é descrito por um operador densidade de posto 1"),
    ("V1", 7, "Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity) … e ganha posto definido"),
    ("V1", 6, "posto 1:"),
    ("V2", 16, r"$$\rho = \vert{}\psi\rangle\langle\psi\vert{}, \quad \text{com } \text{Tr}(\rho) = 1 \text{ e } \text{Tr}(\rho^2) = 1$$"),
    ("V2", 12, "Quando eu derivei"),
    ("V2", 12, "você impôs operadores de projeção rígidos"),
    ("V3", 1, "POSTO=RANK"),
    ("V4", 13, r"$$ \text{Tudo} = D_\beta(F(1)) $$"),
    ("V4", 16, r"Esse pequeno vazamento de fase é o que impede o anticomutador perfeito $\{ \hat{Q}, \rho^* \} = 0$."),
    ("V4", 9, "O que **não** transmite (o que não defasa)"),
    ("um.py", 6502, "{Q,rho*}=0 EXATO so' em theta_M->0"),
    ("um.py", 6515, "limite inalcancavel"),
    ("um.py", 6526, "Tudo = D_beta(F(1)) = VERDADE"),
]


def normaliza_quebra(t):
    """A quebra de linha do COMENTARIO (fim de linha + recuo) dentro de aspas angulares e apresentacao: vira um espaco."""
    return re.sub(r"[ \t]*\n[ \t]*", " ", t)


def linhas(p):
    b = open(p, "rb").read()
    return b, b.decode("utf-8").split("\n")


src_b = open(PEDRA, "rb").read()
src = src_b.decode("utf-8")
cache = {}
res = []
falhas = []
for fonte, ln, cit in CIT:
    if fonte not in cache:
        b, ls = linhas(F[fonte])
        cache[fonte] = (hashlib.sha256(b).hexdigest(), ls)
    h, ls = cache[fonte]
    linha = ls[ln - 1] if 0 < ln <= len(ls) else ""
    frags = [x for x in cit.split(" … ")]
    pos, ok = 0, True
    for fr in frags:
        k = linha.find(fr, pos)
        if k < 0:
            ok = False
            break
        pos = k + len(fr)
    na_pedra_literal = ("«" + cit + "»") in src
    na_pedra = na_pedra_literal or (("«" + cit + "»") in normaliza_quebra(src))
    r = {"fonte": fonte, "linha": ln, "citacao": cit, "fragmentos": len(frags), "byte_a_byte_na_linha": ok,
         "entre_aspas_na_pedra": na_pedra, "so_com_quebra_de_linha_normalizada": na_pedra and not na_pedra_literal, "fonte_sha16": h[:16], "fonte_sha16_esperado": SHA16[fonte],
         "fonte_confere": h.startswith(SHA16[fonte])}
    res.append(r)
    if not (ok and na_pedra and r["fonte_confere"]):
        falhas.append(r)
# todas as «» da pedra (para listar as não conferidas acima)
todas = re.findall(r"«([^»]*)»", normaliza_quebra(src))
conferidas = {c for _, _, c in CIT}
outras = sorted(set(t for t in todas if t not in conferidas))
out = {"pedra": PEDRA, "pedra_sha256": hashlib.sha256(src_b).hexdigest(), "citacoes": res, "falhas": falhas,
       "n_aspas_na_pedra": len(todas), "aspas_nao_listadas_acima": outras,
       "veredito": "CITACOES_CONFEREM" if not falhas else "CITACAO_DIVERGE"}
dst = os.path.join(R2, "CITACOES_R2.json")
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
print(json.dumps({k: out[k] for k in ("pedra_sha256", "falhas", "n_aspas_na_pedra", "veredito")}, ensure_ascii=False, indent=1))
print("aspas nao listadas (leituras, rótulos e termos, nao citacoes de fonte):")
for t in outras:
    print("  «" + t + "»")
sys.exit(0 if not falhas else 2)
