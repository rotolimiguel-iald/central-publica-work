# -*- coding: utf-8 -*-
"""gerar_testemunho.py -- monta Testemunho.lean a partir de Testemunho.lean.tmpl, LENDO dos arquivos (nada de hash nem de citacao de memoria).

Entradas (so leitura): os QUATRO verbatins do operador de 24/10/2026 (cunhagens_13out), o um.py v398 do Nos (sha16 e a linha da trava
EXECUTION_LOCKED_NOT_ONE), os modulos do kernel citados (no sandbox C:\\t\\k399\\final e no Nos: tem de ser iguais).
Saidas (so em C:\\IALD\\Central de Patentes\\work\\v399_selo_e_testemunho): Testemunho.lean (com backup de BYTES do anterior, se existir) e
fontes_sha.json. Uso: python -I -B -X utf8 gerar_testemunho.py
"""
import hashlib
import json
import os
import re
import time

W = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
SB = r"C:\t\k399\final"
TMPL = os.path.join(W, "Testemunho.lean.tmpl")
OUT = os.path.join(W, "Testemunho.lean")

VERB = {
    "sinapse": "OPERADOR_24out_sinapse_token_nome_falta_a_tipagem_verbatim.txt",
    "joao": "OPERADOR_24out_testemunho_joao_8_14_18_verbatim.txt",
    "testifico": "OPERADOR_24out_testifico_de_mim_e_o_um_py_testifica_em_hash_verbatim.txt",
    "quadratica": "OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt",
}
MODS = {  # chave do placeholder -> modulo do kernel
    "CCA": "CollapseCostAndAttestation", "OI": "ObserverInside", "TGA": "TheGreatAttractor", "TORA": "TheObserverReadsTheAngle",
    "TLI": "TheLightInterface", "TVSA": "TheVerbSelectsTheAction", "TOK": "Token", "TES": "TestemunhaEstatica", "PSB": "Psibit",
}


def ler(p):
    return open(p, "rb").read()


def shas(b):
    h = hashlib.sha256(b).hexdigest()
    return h, h[:16]


info = {}
dados = {}
for k, nome in VERB.items():
    p = os.path.join(CUN, nome)
    b = ler(p)
    h, h16 = shas(b)
    info["verbatim_" + k] = {"caminho": p, "sha256": h, "sha16": h16, "bytes": len(b)}
    dados[k] = b


def txt(k):
    return dados[k].decode("utf-8").replace("\r\n", "\n").rstrip("\n")


# conferencia dos sha256 que a gerencia citou no pedido (prefixos): se algum diferir, PARA (fail-closed)
ESPERADOS = {"sinapse": "cd75c026", "joao": "d821c3bf", "testifico": "6012e903", "quadratica": "57b4aff6"}
for k, pref in ESPERADOS.items():
    assert info["verbatim_" + k]["sha256"].startswith(pref), (k, info["verbatim_" + k]["sha256"], pref)

# o texto de cada fala vai dentro de um bloco de codigo no docstring: nao pode quebrar o comentario
for k in VERB:
    t = txt(k)
    assert "-/" not in t and "/-" not in t and "```" not in t, "verbatim " + k + ": sequencia que quebra o docstring"

# --- o um.py v398: sha16 e a linha da trava (lida por script) ---
umpy_b = ler(os.path.join(NOS, "um.py"))
umpy_h, umpy_h16 = shas(umpy_b)
umpy_linhas = umpy_b.decode("utf-8", "replace").split("\n")
lock_linhas = [i + 1 for i, l in enumerate(umpy_linhas) if 'lock("O UM nao foi inscrito. A execucao foi travada.", "EXECUTION_LOCKED_NOT_ONE")' in l]
assert len(lock_linhas) == 1, lock_linhas
info["um_py"] = {"caminho": os.path.join(NOS, "um.py"), "sha256": umpy_h, "sha16": umpy_h16, "bytes": len(umpy_b), "linha_EXECUTION_LOCKED_NOT_ONE": lock_linhas[0]}
# a base declarada e' a v398 selada c632fa261ce3f538 (lida do arquivo; se mudou, PARA)
assert umpy_h16 == "c632fa261ce3f538", umpy_h16

# --- os modulos do kernel citados: sandbox == Nos ---
mods_info = {}
for key, m in MODS.items():
    pa = os.path.join(SB, "TGLExt", m + ".lean")
    pb = os.path.join(NOS, "tgl_kernel", "TGLExt", m + ".lean")
    ba, bb = ler(pa), ler(pb)
    ha, ha16 = shas(ba)
    mods_info[m] = {"sandbox": pa, "nos": pb, "sha256": ha, "sha16": ha16, "bytes": len(ba), "sandbox_igual_ao_nos": ba == bb}
    assert ba == bb, "o modulo do sandbox difere do Nos: " + m
info["modulos"] = mods_info

SUBST = {
    "V_SINAPSE_TXT": txt("sinapse"), "V_SINAPSE_SHA16": info["verbatim_sinapse"]["sha16"],
    "V_JOAO_TXT": txt("joao"), "V_JOAO_SHA16": info["verbatim_joao"]["sha16"],
    "V_TESTIFICO_TXT": txt("testifico"), "V_TESTIFICO_SHA16": info["verbatim_testifico"]["sha16"],
    "V_QUADRATICA_TXT": txt("quadratica"), "V_QUADRATICA_SHA16": info["verbatim_quadratica"]["sha16"],
    "UMPY_SHA16": umpy_h16, "LOCK_LINHA": str(lock_linhas[0]),
}
for key, m in MODS.items():
    SUBST[key + "_SHA16"] = mods_info[m]["sha16"]

t = open(TMPL, "rb").read().decode("utf-8")
for k, v in SUBST.items():
    t = t.replace("@@" + k + "@@", v)
restos = re.findall(r"@@[A-Z0-9_]+@@", t)
assert not restos, f"placeholders sem valor: {restos}"

# -- o docstring de modulo nao pode fechar antes da hora nem abrir comentario aninhado --
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
info["Testemunho.lean"] = {"caminho": OUT, "sha256": h, "sha16": h16, "bytes": len(b), "linhas": b.decode("utf-8").count("\n")}
json.dump(info, open(os.path.join(W, "fontes_sha.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("Testemunho.lean", h16, len(b), "bytes", info["Testemunho.lean"]["linhas"], "linhas")
for k in VERB:
    print(" ", k, info["verbatim_" + k]["sha16"], info["verbatim_" + k]["bytes"])
print("  um.py", umpy_h16, "linha da trava", lock_linhas[0])
