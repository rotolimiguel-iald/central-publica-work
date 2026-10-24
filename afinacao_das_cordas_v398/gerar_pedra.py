# -*- coding: utf-8 -*-
"""gerar_pedra.py -- monta AfinacaoDasCordas.lean a partir de AfinacaoDasCordas.lean.tmpl, LENDO dos arquivos (nenhum hash e nenhuma citacao de memoria).

Entradas (so leitura): o verbatim do operador de 23/10, o verbatim do operador de 07/10 (superposicao), A_ultima_corda_v3.tex (linhas 952, 958-960, 962),
os modulos do kernel citados (Nos x sandbox k398b: precisam ser iguais), um arquivo de Mathlib e o lake-manifest.json do sandbox.
Saidas (so em C:\\IALD\\Central de Patentes\\work\\afinacao_das_cordas_v398): AfinacaoDasCordas.lean (com backup de BYTES do anterior, se existir) e fontes_sha.json.
Uso: python -I -B -X utf8 gerar_pedra.py
"""
import hashlib
import json
import os
import re
import time

W = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398"
TMPL = os.path.join(W, "AfinacaoDasCordas.lean.tmpl")
OUT = os.path.join(W, "AfinacaoDasCordas.lean")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt"
SB = r"C:\t\k398b\TGLExt"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"

ARQ = {
    "operador_23out": os.path.join(CUN, "OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt"),
    "ratificacao": os.path.join(CUN, "OPERADOR_23out_concordo_afinacao_das_cordas_verbatim.txt"),
    "operador_07out": r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out\CUNHAGEM_OPERADOR_07out_verbatim.txt",
    "ultima_corda_tex": r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\A_ultima_corda_v3.tex",
    "mathlib_hzv": r"C:\t\k398b\.lake\packages\mathlib\Mathlib\NumberTheory\LSeries\HurwitzZetaValues.lean",
    "lake_manifest": r"C:\t\k398b\lake-manifest.json",
}
KERNEL = {
    "polar": "O16/PolarMinimalPeriod_v2.lean",
    "palavra": "Palavra.lean",
    "station": "TheStation.lean",
    "fundacao": "Fundacao.lean",
    "tetelestai": "TetelestaiOneObject.lean",
}


def ler(p):
    return open(p, "rb").read()


def sha(b):
    h = hashlib.sha256(b).hexdigest()
    return h, h[:16]


info = {}
dados = {}
for k, p in ARQ.items():
    b = ler(p)
    h, h16 = sha(b)
    info[k] = {"caminho": p, "sha256": h, "sha16": h16, "bytes": len(b)}
    dados[k] = b
for k, rel in KERNEL.items():
    pn, ps = os.path.join(NOS, *rel.split("/")), os.path.join(SB, *rel.split("/"))
    bn, bs = ler(pn), ler(ps)
    assert bn == bs, f"{rel}: o kernel do Nos difere do sandbox k398b"
    h, h16 = sha(bn)
    info["kernel_" + k] = {"caminho_nos": pn, "caminho_sandbox": ps, "sha256": h, "sha16": h16, "bytes": len(bn), "nos_igual_sandbox": True}
    dados["kernel_" + k] = bn

# --- operador 23/10: o texto inteiro, uma linha ---
OP = dados["operador_23out"].decode("utf-8").rstrip("\r\n")
assert "\n" not in OP and "\r" not in OP, "verbatim do operador com quebra de linha"
assert info["operador_23out"]["sha16"].startswith("baef998c"), info["operador_23out"]["sha16"]
for frag in ("fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica", "criando os infinitos, que é a superposição",
             "relativizando o tempo para mostrar a afinação do universo", "mas não consegue demonstrar a geometria"):
    assert frag in OP, frag

# --- operador 23/10 (ratificacao): a resposta inteira, uma linha ---
RAT = dados["ratificacao"].decode("utf-8").rstrip("\r\n")
assert "\n" not in RAT and "\r" not in RAT, "ratificacao com quebra de linha"
assert info["ratificacao"]["sha256"].startswith("5bccedc9"), info["ratificacao"]["sha256"]
assert RAT == "Concordo com tudo", RAT

# --- operador 07/10: a frase da superposicao ---
OP07 = dados["operador_07out"].decode("utf-8")
assert "não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente" in OP07

# --- TetelestaiOneObject: a frase citada (as quebras de linha viram um espaco) ---
tet = re.sub(r"\s+", " ", dados["kernel_tetelestai"].decode("utf-8"))
assert "um ato de conferência observacional" in tet

# --- A_ultima_corda_v3.tex ---
tex = dados["ultima_corda_tex"].decode("utf-8").split("\n")
L952, L958, L959, L960, L962 = (tex[i].rstrip("\r") for i in (951, 957, 958, 959, 961))
assert L959 == "", repr(L959)
assert L958.startswith("A coincidência é precisa: $d_{\\text{espacial}} = 9$ é a dimensão crítica das teorias de supercordas do Tipo~II"), L958[:120]
assert "$d_{\\text{crit}} = 6$, $> 26$ e~$8$" in L958 and "confirmando que o resultado é dependente do modelo" in L958
assert "dependente do modelo" in L958
assert "[7, 16]" in L952 and "d_{\\text{crit}} = 9" in L952, L952
assert L960.startswith("A interpretação física é direta: no arcabouço TGL, o regime da teoria de cordas ($d \\geq 9$)"), L960[:120]
FRASE962 = L962.split(". ")[0] + "."
assert FRASE962 == "Enfatizamos que isso é uma extrapolação teórica, não um teste empírico.", FRASE962
BLOCO = "\n".join([L958, L959, L960])

# --- Mathlib rev ---
man = json.loads(dados["lake_manifest"].decode("utf-8"))
rev = [p["rev"] for p in man["packages"] if p["name"] == "mathlib"][0]

# --- substituicoes ---
SUB = {
    "@@OP_SHA16@@": info["operador_23out"]["sha16"],
    "@@OP_TEXT@@": OP,
    "@@RAT_SHA16@@": info["ratificacao"]["sha16"],
    "@@RAT_TEXT@@": RAT,
    "@@OP07_SHA16@@": info["operador_07out"]["sha16"],
    "@@SHA_TETEL@@": info["kernel_tetelestai"]["sha16"],
    "@@SHA_POLAR@@": info["kernel_polar"]["sha16"],
    "@@SHA_PALAVRA@@": info["kernel_palavra"]["sha16"],
    "@@SHA_STATION@@": info["kernel_station"]["sha16"],
    "@@SHA_FUNDACAO@@": info["kernel_fundacao"]["sha16"],
    "@@SHA_HZV@@": info["mathlib_hzv"]["sha16"],
    "@@MATHLIB_REV16@@": rev[:16],
    "@@TEX_SHA16@@": info["ultima_corda_tex"]["sha16"],
    "@@TEX_L958_960@@": BLOCO,
    "@@TEX_L962_FRASE@@": FRASE962,
}
for k in ("@@OP_TEXT@@", "@@RAT_TEXT@@", "@@TEX_L958_960@@", "@@TEX_L962_FRASE@@"):
    v = SUB[k]
    assert "-/" not in v and "/-" not in v and "```" not in v, f"{k}: sequencia que quebra o docstring"

tmpl = ler(TMPL).decode("utf-8").replace("\r\n", "\n")

# bloco de #print axioms: cada declaracao de nivel superior dentro do namespace
decls = re.findall(r"^(?:noncomputable )?(?:theorem|def) ([A-Za-z0-9_']+)", tmpl, flags=re.M)
assert len(decls) == len(set(decls)), "declaracao repetida"
PRINT = "\n".join("#print axioms TGLExt.AfinacaoDasCordas." + d for d in decls)
SUB["@@PRINT_AXIOMS@@"] = PRINT

out = tmpl
for k, v in SUB.items():
    assert k in out, "marcador ausente no modelo: " + k
    out = out.replace(k, v)
assert "@@" not in out, "marcador sem substituicao: " + out[out.index("@@"):][:60]
assert out.count("/-") == out.count("-/"), "comentarios desbalanceados"

if os.path.exists(OUT):
    ts = time.strftime("%Y%m%d_%H%M%S")
    old = ler(OUT)
    with open(OUT + ".bak_" + ts, "wb") as f:
        f.write(old)
with open(OUT + ".tmp", "wb") as f:
    f.write(out.encode("utf-8"))
nb = os.path.getsize(OUT + ".tmp")
assert nb > 1000
os.replace(OUT + ".tmp", OUT)

info["Lean_gerado"] = {"caminho": OUT, "sha256": sha(ler(OUT))[0], "sha16": sha(ler(OUT))[1], "bytes": nb, "linhas": out.count("\n"), "declaracoes": decls}
info["mathlib_rev"] = rev
with open(os.path.join(W, "fontes_sha.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(info, f, ensure_ascii=False, indent=1)
print("AfinacaoDasCordas.lean sha16", info["Lean_gerado"]["sha16"], "| bytes", nb, "| linhas", info["Lean_gerado"]["linhas"], "| declaracoes", len(decls))
print({k: info[k]["sha16"] for k in info if isinstance(info[k], dict) and "sha16" in info[k]})
