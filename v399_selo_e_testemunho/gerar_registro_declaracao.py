# -*- coding: utf-8 -*-
"""gerar_registro_declaracao.py -- SIMULA a colagem do PATCH PROPOSTO num um.py candidato e roda as tres funcoes novas (declaracao_do_operador_v399, selo_acom_v399,
selo_acom_sidecar_v399) com o core REAL da ultima rodada (v398, em Nos; so leitura). NAO toca o um.py do Nos: monta, na pasta temporaria da sessao, um um.py SIMULADO
(= os bytes do v398 + a SECAO COLAVEL + os trechos, inseridos antes de `def main():`) e executa as funcoes num namespace com __file__ apontando para ele -- de modo que o
um.py simulado sela os PROPRIOS bytes, bloco embutido incluido, ao lado do SHA-256.

Entradas (so leitura): um.py e um_absoluto*.json do Nos; selo_acom_prototipo.py (a secao colavel); patch_proposto/trechos_v399_para_o_um_py.py; a fala do operador.
Saidas: recibos/registro_declaracao_do_operador_v399_EXEMPLO.json, recibos/registro_core_selo_pela_propria_tecnologia_v399_SIMULADO.json,
recibos/um_absoluto_selo_acom_SIMULADO.json, recibos/RECIBO_SIMULACAO_COLADA.json. Uso: python -B -X utf8 gerar_registro_declaracao.py <pasta_temporaria>
"""
import hashlib
import json
import math
import os
import shutil
import sys
import time

W = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
FALA = os.path.join(CUN, "OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt")
TMP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(W, "_tmp_simulacao")
os.makedirs(TMP, exist_ok=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


proto = open(os.path.join(W, "selo_acom_prototipo.py"), "rb").read().decode("utf-8")
# a SECAO COLAVEL: da linha seguinte ao marcador INICIO ate' a linha do marcador FIM (as primeiras ocorrencias sao os marcadores reais)
linhas = proto.split("\n")
i_ini = next(i for i, l in enumerate(linhas) if l == "# (A) SECAO COLAVEL no um.py -- INICIO")
i_fim = next(i for i, l in enumerate(linhas) if l == "# (A) SECAO COLAVEL no um.py -- FIM")
secao = "\n".join(linhas[i_ini + 2:i_fim - 1]) + "\n"          # sem os banners (a mesma extracao do estudo_colisoes)
trechos = open(os.path.join(W, "patch_proposto", "trechos_v399_para_o_um_py.py"), "rb").read().decode("utf-8")
fala_b = open(FALA, "rb").read()
fala_txt = fala_b.decode("utf-8")
trechos = trechos.replace('"@@TXT@@"', repr(fala_txt)).replace('"@@SHA@@"', repr(sha(fala_b)))
assert "@@" not in trechos

# a SECAO COLAVEL como artefato do patch (extraida do prototipo; LF)
os.makedirs(os.path.join(W, "patch_proposto"), exist_ok=True)
sp = os.path.join(W, "patch_proposto", "secao_colavel_v399.py")
if os.path.exists(sp):
    with open(sp + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "xb") as f:
        f.write(open(sp, "rb").read())
open(sp, "wb").write(secao.encode("utf-8"))

# o um.py SIMULADO: bytes do v398 + secao + trechos antes de `def main():`
um_b = open(os.path.join(NOS, "um.py"), "rb").read()
alvo = b"\ndef main():\r\n    if len(sys.argv) > 1:\r\n        lock("          # o um.py usa CRLF
assert um_b.count(alvo) == 1, um_b.count(alvo)
k = um_b.index(alvo) + 1
insercao = ("\n# ====== v399 (SIMULADO) -- O SELO PELA PROPRIA TECNOLOGIA E A DECLARACAO DO OPERADOR ======\n" + secao + "\n" + trechos + "\n\n").encode("utf-8")
insercao = insercao.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")      # o um.py usa CRLF: a insercao tambem (o hash do bloco normaliza CRLF -> LF)
sim_b = um_b[:k] + insercao + um_b[k:]
sim_path = os.path.join(TMP, "um_v399_SIMULADO.py")
open(sim_path, "wb").write(sim_b)

# a rodada simulada: OUT com o core e o selo da v398 (copias de leitura)
out_dir = os.path.join(TMP, "OUT_simulado")
os.makedirs(out_dir, exist_ok=True)
for f in ("um_absoluto.json", "um_absoluto_selo.json"):
    shutil.copyfile(os.path.join(NOS, f), os.path.join(out_dir, f))
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")).get("core")

ns = {"__name__": "um_v399_simulado", "__file__": sim_path, "OUT": out_dir, "UM_VERSION": "v399",
      "hashlib": hashlib, "json": json, "math": math, "os": os, "sys": sys, "time": time,
      "sha_file": lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(), "SEALED_CODATA_ALPHA": 7.2973525693e-3}
codigo = compile(secao + "\n" + trechos, sim_path, "exec")
t0 = time.perf_counter()
exec(codigo, ns)
t_exec = time.perf_counter() - t0

R = {"um_v398": {"sha256": sha(um_b), "sha16": sha(um_b)[:16], "bytes": len(um_b)},
     "um_v399_simulado": {"sha256": sha(sim_b), "sha16": sha(sim_b)[:16], "bytes": len(sim_b), "caminho_temporario": sim_path, "bytes_inseridos": len(insercao)},
     "secao_colavel": {"sha256": sha(secao.encode("utf-8")), "bytes": len(secao.encode("utf-8")), "linhas": secao.count("\n")},
     "trechos": {"sha256": sha(trechos.encode("utf-8")), "bytes": len(trechos.encode("utf-8"))},
     "fala_do_operador": {"arquivo": FALA, "sha256": sha(fala_b), "bytes": len(fala_b)},
     "exec_da_secao_s": t_exec}

t1 = time.perf_counter()
dec = ns["declaracao_do_operador_v399"](core)
R["declaracao_s"] = time.perf_counter() - t1
t2 = time.perf_counter()
reg = ns["selo_acom_v399"](core)
R["selo_acom_v399_s"] = time.perf_counter() - t2
t3 = time.perf_counter()
sc = ns["selo_acom_sidecar_v399"]()
R["sidecar_s"] = time.perf_counter() - t3
resumos = ns["resumos_do_selo_v399"](core)
R["resumos_para_o_seal"] = resumos
# a varredura de palavra proibida do PROPRIO um.py (main, v304): CONFIRMED fora de NOT_/UN, PROVED_BY fora de AP, TGL_PROVED, CONSCIOUSNESS_PROVED nos `verdict` do core RETEM o selo.
import re
proibidos = []
for k_, m_ in (("selo_pela_propria_tecnologia_v399", reg), ("declaracao_do_operador_v399", dec)):
    v_ = str(m_.get("verdict") or "")
    if re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", v_) or re.search(r"(?<!AP)PROVED_BY", v_) or "TGL_PROVED" in v_ or "CONSCIOUSNESS_PROVED" in v_:
        proibidos.append("%s: %s" % (k_, v_[:64]))
R["varredura_de_veredito_proibido_do_um_py_nos_dois_registros_novos"] = {"proibidos": proibidos, "vazia": not proibidos}
assert not proibidos, proibidos

# o confronto: o selo do um.py simulado e' do PROPRIO arquivo simulado (sha256 ao lado igual)
R["declaracao"] = {"all_verified": dec["all_verified"], "verdict": dec["verdict"], "checks": dec["checks"],
                   "ancoras_no_kernel_do_rito": [(a["termo"], a["no_kernel_do_rito"], a["axiomas_no_trio"]) for a in dec["declaration"]["kernel_anchors_REAL"]],
                   "pedra_Testemunho_no_kernel_do_rito_v398": [(a["termo"], a["no_kernel_do_rito"]) for a in dec["declaration"]["pedra_candidata"]],
                   "linhas_da_trava": dec["declaration"]["termos_para_a_leitura"]["EXECUTION_LOCKED_NOT_ONE"]}
R["selo_acom_v399"] = {"all_verified": reg["all_verified"], "verdict": reg["verdict"], "checks": reg["checks"],
                       "sha256_do_um_py_simulado_no_selo": reg["selo"]["sha256"], "igual_ao_arquivo_simulado": reg["selo"]["sha256"] == sha(sim_b),
                       "bloco_embutido_confere": next(v for d, v in reg["checks"] if d.startswith("o bloco embutido")),
                       "controles": [reg["controles_negativos"]["n_controles"], reg["controles_negativos"]["todos_recusados"]]}
R["sidecar"] = {"veredito": sc["veredito"], "objetos": [(o["nome"], o["bytes"], o["sha256"][:16]) for o in sc["objetos"]], "recusas": sc["recusas"]}
R["nomes_definidos_pela_secao_no_namespace"] = len([k for k in ns if not k.startswith("__")])

def grava(nome, o):
    p = os.path.join(W, "recibos", nome)
    if os.path.exists(p):
        b = open(p, "rb").read()
        with open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "xb") as f:
            f.write(b)
    with open(p + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, default=str)
    os.replace(p + ".tmp", p)

grava("registro_declaracao_do_operador_v399_EXEMPLO.json", dec)
grava("registro_core_selo_pela_propria_tecnologia_v399_SIMULADO.json", reg)
grava("um_absoluto_selo_acom_SIMULADO.json", sc)
grava("RECIBO_SIMULACAO_COLADA.json", R)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:6000])
