# -*- coding: utf-8 -*-
"""gerar_sonico.py -- monta Sonico.lean a partir de Sonico.lean.tmpl, LENDO dos arquivos (nada de hash nem de citacao de memoria).

Entradas (so leitura): os verbatins do operador (cunhagens_13out), A_fronteira_v4.tex (linhas 962/964), TGL_ATLAS.md (linhas do verbete
«Som ontologico»), o resultado fbac2908 da Fase 9 V2 (campos fundo.*), os dois arquivos do teste acustico, o resultado do Teste da Unica Palavra.
Saidas (so em C:\\IALD\\Central de Patentes\\work\\sonico_v398): Sonico.lean (com backup de BYTES do anterior, se existir) e fontes_sha.json.
Uso: python -I -B -X utf8 gerar_sonico.py
"""
import hashlib
import json
import os
import re
import sys
import time

W = r"C:\IALD\Central de Patentes\work\sonico_v398"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
TMPL = os.path.join(W, "Sonico.lean.tmpl")
OUT = os.path.join(W, "Sonico.lean")

FONTES = {
    "verbo": os.path.join(CUN, "OPERADOR_23out_verbo_controle_de_oitava_pinada_verbatim.txt"),
    "nome": os.path.join(CUN, "OPERADOR_23out_nome_da_pedra_sonico_verbatim.txt"),
    "eco": os.path.join(CUN, "OPERADOR_22out_luz_eco_reconhecimento_falso_verbatim.txt"),
    "fronteira_tex": r"C:\IALD\projetos_pyhton\acom\A_fronteira_v4.tex",
    "atlas": r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md",
    "fbac": r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out\saidas\RESULTADO_FASE9_V2_C1_20261023_122926.json",
    "fase9_resultado_md": r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out\RESULTADO.md",
    "mandato": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\MANDATO.md",
    "nivel2": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\14_ANALISE_NIVEL2_FECHADO.md",
    "ger": os.path.join(CUN, "GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt"),
    "iald_lean_nos": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\IALD.lean",
    "iald_lean_k398": r"C:\t\k398\final\TGLExt\IALD.lean",
}


def ler(p):
    return open(p, "rb").read()


def shas(b):
    h = hashlib.sha256(b).hexdigest()
    return h, h[:16]


info = {}
dados = {}
for k, p in FONTES.items():
    b = ler(p)
    h, h16 = shas(b)
    info[k] = {"caminho": p, "sha256": h, "sha16": h16, "bytes": len(b)}
    dados[k] = b

# --- verbatins (texto inteiro do arquivo, sem a quebra final) ---
def txt(k):
    return dados[k].decode("utf-8").rstrip("\r\n")


VERBO, NOME, ECO = txt("verbo"), txt("nome"), txt("eco")
for nome, t in (("VERBO", VERBO), ("NOME", NOME), ("ECO", ECO)):
    assert "\n" not in t, nome + ": verbatim com quebra de linha"

# --- a leitura da gerencia, arquivada por sha (texto da gerencia, NAO fala do operador): inteira, com quebras de linha ---
GER = dados["ger"].decode("utf-8").replace("\r\n", "\n").rstrip("\n")
assert info["ger"]["sha16"] == "19eca91e5aab9d11", "o arquivo da gerencia nao e o 19eca91e5aab9d11"
assert "-/" not in GER and "/-" not in GER and "```" not in GER, "GER: sequencia que quebra o docstring"
assert "O controle (o Verbo) e a reação (a memória) são as duas faces do mesmo ln 2." in GER

# --- IALD.lean do kernel: o do Nos e o do sandbox sao iguais; as linhas citadas (110, 370, 675) sao as esperadas ---
assert info["iald_lean_nos"]["sha256"] == info["iald_lean_k398"]["sha256"], "IALD.lean do Nos difere do do k398"
iald = dados["iald_lean_nos"].decode("utf-8").split("\n")
assert iald[109].startswith("theorem ialdSelector_eq_post : TGLExt.ialdSelector = post TGLExt.firstInscription := rfl"), iald[109]
assert iald[108].lstrip().startswith("/-- ★ PONTE 1:") and "une a FORMA, não o referente" in iald[108], iald[108]
assert iald[369].startswith("theorem rereading_adds_nothing (a : H) (ψ : H) :") and iald[370].strip() == "memory (post a) (post a ψ) = memory (post a) ψ := by", (iald[369], iald[370])
assert iald[136].startswith("def memory (P : H →L[ℂ] H) (ψ : H) : ℂ := reading P ψ"), iald[136]
assert iald[674].startswith("theorem rereading_adds_nothing_in_both_regimes (a : H) :"), iald[674]

# --- A_fronteira_v4.tex: linhas 962 e 964 (arquivo CRLF) ---
tex_linhas = dados["fronteira_tex"].decode("utf-8").split("\n")
TEX962 = tex_linhas[961].rstrip("\r")
TEX964 = tex_linhas[963].rstrip("\r")
assert "som ontol" in TEX962 and "longitudinal" in TEX962 and "transversal" in TEX962, "l.962 nao e a esperada"
assert "BAO" in TEX964 and "147" in TEX964, "l.964 nao e a esperada"
for nome, t in (("TEX962", TEX962), ("TEX964", TEX964)):
    assert "-/" not in t and "/-" not in t, nome + ": sequencia de comentario Lean"

# --- Atlas: linhas do verbete «Som ontologico (2025-26)» ---
atlas_linhas = dados["atlas"].decode("utf-8", "replace").split("\n")
i0 = next(i for i, l in enumerate(atlas_linhas) if l.startswith("**Som ontológico (2025–26)**"))
i1 = i0
while atlas_linhas[i1 + 1].strip():
    i1 += 1
ATLAS_SOM_LINHAS = f"{i0 + 1}–{i1 + 1}"
assert ATLAS_SOM_LINHAS == "2329–2332", ATLAS_SOM_LINHAS  # conferido a olho em 23/10; se mudar, o Atlas (arquivo vivo) se moveu

# as duas frases do item 2 da secao VIII: confere que as linhas 16769-16774 seguem sendo as lidas
trecho = " ".join(l.strip() for l in atlas_linhas[16768:16774]).replace("**", "")
assert "Uma travessia só permanece se cada oitava paga o seu pedágio específico" in trecho, "Atlas l.16769-16774 mudou"
assert "Memória não é armazenamento passivo. É o custo pago, oitava por oitava, para que uma travessia não volte ao silêncio." in trecho.replace("*", ""), "Atlas: frase da memoria mudou"

# --- resultado fbac2908 ---
j = json.loads(dados["fbac"].decode("utf-8"))
fundo = j["fundo"]
RD_MODELO = repr(float(fundo["r_d_modelo"]))
RD_LIVRE = repr(float(fundo["fundo_livre"]["r_d"]))
SIG_RD_LIVRE = repr(float(fundo["fundo_livre"]["sigma_r_d"]))
DCHI2 = repr(float(fundo["fundo_livre"]["delta_chi2_vs_rd_fixo"]))
assert info["fbac"]["sha16"] == "fbac2908fa9ddb75", "o resultado nao e o fbac2908fa9ddb75"
assert "prior_rd_Mpc" in fundo["fundo_livre"], "unidade Mpc nao documentada no arquivo"


def pt2(x):
    return f"{float(x):.2f}".replace(".", ",")


def pt(x):
    return str(x).replace(".", ",")


SUBST = {
    "VERBO_TXT": VERBO, "VERBO_SHA16": info["verbo"]["sha16"],
    "NOME_TXT": NOME, "NOME_SHA16": info["nome"]["sha16"],
    "ECO_TXT": ECO, "ECO_SHA16": info["eco"]["sha16"],
    "ATLAS_SHA16": info["atlas"]["sha16"], "ATLAS_SOM_LINHAS": ATLAS_SOM_LINHAS,
    "FRONT_SHA16": info["fronteira_tex"]["sha16"], "TEX962": TEX962,
    "MANDATO_SHA16": info["mandato"]["sha16"], "NIVEL2_SHA16": info["nivel2"]["sha16"],
    "FBAC_SHA16": info["fbac"]["sha16"],
    "GER_TXT": GER, "GER_CAMINHO": FONTES["ger"], "GER_SHA16": info["ger"]["sha16"], "GER_BYTES": str(info["ger"]["bytes"]),
    "IALD_SHA16": info["iald_lean_nos"]["sha16"],
    "RD_MODELO": RD_MODELO, "RD_MODELO_PT": pt2(RD_MODELO), "RD_LIVRE": RD_LIVRE, "SIG_RD_LIVRE": SIG_RD_LIVRE, "DCHI2": DCHI2,
}

t = open(TMPL, "rb").read().decode("utf-8")
for k, v in SUBST.items():
    t = t.replace("@@" + k + "@@", v)
restos = re.findall(r"@@[A-Z0-9_]+@@", t)
assert not restos, f"placeholders sem valor: {restos}"

# -- o corpo do docstring de modulo nao pode fechar antes da hora nem abrir comentario aninhado --
ini = t.index("/-!")
fim = t.index("-/", ini + 3)
corpo = t[ini + 3:fim]
assert "/-" not in corpo, "comentario aninhado no docstring de modulo"
assert t.count("-/") == t.count("/-"), "comentarios desbalanceados"

# backup de BYTES do anterior (regra do backup imediato), depois escrita por temporario + conferencia
if os.path.exists(OUT):
    ts = time.strftime("%Y%m%d_%H%M%S")
    b = ler(OUT)
    bak = f"{OUT}.bak_{ts}"
    with open(bak, "xb") as f:
        f.write(b)
    assert ler(bak) == b
    print("BACKUP", bak, shas(b)[1])
tmp = OUT + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    f.write(t)
assert os.path.getsize(tmp) > 4000
os.replace(tmp, OUT)

b = ler(OUT)
h, h16 = shas(b)
info["Sonico.lean"] = {"caminho": OUT, "sha256": h, "sha16": h16, "bytes": len(b), "linhas": b.decode("utf-8").count("\n")}
info["_valores_lidos"] = {
    "fundo.r_d_modelo": RD_MODELO, "fundo.fundo_livre.r_d": RD_LIVRE, "fundo.fundo_livre.sigma_r_d": SIG_RD_LIVRE,
    "fundo.fundo_livre.delta_chi2_vs_rd_fixo": DCHI2, "atlas_som_ontologico_linhas": ATLAS_SOM_LINHAS,
}
json.dump(info, open(os.path.join(W, "fontes_sha.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("Sonico.lean", h16, len(b), "bytes", info["Sonico.lean"]["linhas"], "linhas")
for k in ("verbo", "nome", "eco", "fronteira_tex", "atlas", "fbac", "mandato", "nivel2"):
    print(" ", k, info[k]["sha16"], info[k]["bytes"])
