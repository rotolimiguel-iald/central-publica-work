# -*- coding: utf-8 -*-
"""inventario_final.py -- inventario e INVARIANTES da entrega (so leitura + grava INVENTARIO.json na pasta de trabalho).

Invariantes conferidas por script: (1) o um.py do Nos segue c632fa261ce3f538 (so leitura); (2) o core e o selo da rodada em Nos nao mudaram desde a leitura do estudo;
(3) nada foi escrito nas pastas do operador (SkyGrid_Piloto, projetos_pyhton/acom, o .tex): nenhum arquivo com mtime de hoje; (4) o Testemunho.lean da pasta de trabalho e' identico ao
do sandbox C:\\t\\k399; (5) o robocopy (PID criado por mim) terminou; (6) o kernel do Nos nao tem Testemunho.lean; (7) o k398c nao foi tocado (maior mtime anterior a hoje).
Uso: python -I -B -X utf8 inventario_final.py"""
import hashlib
import json
import os
import subprocess
import time

W = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
HOJE = time.strftime("%Y-%m-%d")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def info(p):
    h = sha(p)
    return {"caminho": p, "bytes": os.path.getsize(p), "sha256": h, "sha16": h[:16]}


R = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "hoje": HOJE, "artefatos": {}, "invariantes": {}}
entregas = ["RESULTADO.md", "selo_acom_prototipo.py", "selo_acom_prototipo.py.tmpl", "montar_prototipo.py", "EMBUTIDO_MANIFESTO.json", "Testemunho.lean", "Testemunho.lean.tmpl",
            "gerar_testemunho.py", "conferir_cabecalho.py", "conferencia_cabecalho.json", "construir_axiomas.py", "AXIOMAS.json", "conferir_sandbox.py", "conferencia_sandbox.json",
            "fontes_sha.json", "lake_build_testemunho.log", "nomes_citados_saida.txt", "registro_mapa_v399_estudo.json", "gerar_registro_declaracao.py", "reprodutibilidade.py",
            "recibo_testes_operador.py", "consultar_mapa.py", "varredura_textos.py", "varredura_textos.json", "gerar_resultado.py", "RESULTADO.md.tmpl", "gerar_registro_mapa.py", "rodar_tudo.py", "inventario_final.py",
            os.path.join("patch_proposto", "PATCH_PROPOSTO_v399.md"), os.path.join("patch_proposto", "secao_colavel_v399.py"),
            os.path.join("patch_proposto", "trechos_v399_para_o_um_py.py")]
for f in entregas:
    p = os.path.join(W, f)
    if os.path.exists(p):
        R["artefatos"][f] = info(p)
    else:
        R["artefatos"][f] = {"ausente": True}
rec = os.path.join(W, "recibos")
for f in sorted(os.listdir(rec)):
    if ".bak_" in f or f.endswith(".tmp"):
        continue
    R["artefatos"][os.path.join("recibos", f)] = info(os.path.join(rec, f))

# (1) e (2)
um = info(os.path.join(NOS, "um.py"))
R["invariantes"]["um_py_do_nos_sha16"] = um["sha16"]
R["invariantes"]["um_py_do_nos_e_a_v398"] = um["sha16"] == "c632fa261ce3f538"
sc = json.load(open(os.path.join(rec, "um_absoluto_selo_acom.json"), encoding="utf-8"))
lido = {o["nome"]: o["sha256"] for o in sc["objetos"]}
agora = {n: sha(os.path.join(NOS, n)) for n in lido}
R["invariantes"]["core_selo_um_py_do_nos_iguais_aos_do_estudo"] = (lido == agora)
# (3) pastas do operador
def novos(raiz):
    out = []
    for r, ds, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(r, f)
            if time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(p))) == HOJE:
                out.append(p)
    return out
R["invariantes"]["arquivos_com_mtime_de_hoje_nas_pastas_do_operador"] = {
    "SkyGrid_Piloto": novos(r"C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto")[:10],
    "projetos_pyhton_acom_py": [p for p in novos(r"C:\IALD\projetos_pyhton\acom") if p.endswith((".py", ".pyc"))][:10],
    "tex_da_patente": novos(r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_Crypto_PI_INPI.tex") if os.path.isdir(r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_Crypto_PI_INPI.tex") else
                      ([r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_Crypto_PI_INPI.tex"] if time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_Crypto_PI_INPI.tex"))) == HOJE else [])}
# (4)
a, b = sha(os.path.join(W, "Testemunho.lean")), sha(r"C:\t\k399\final\TGLExt\Testemunho.lean")
R["invariantes"]["Testemunho_lean_trabalho_igual_ao_sandbox"] = (a == b)
# (6)
R["invariantes"]["kernel_do_nos_sem_Testemunho_lean"] = not os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Testemunho.lean"))
# (7) k398c intocado: maior mtime
mx = 0.0
for r, ds, fs in os.walk(r"C:\t\k398c\final\TGLExt"):
    for f in fs:
        mx = max(mx, os.path.getmtime(os.path.join(r, f)))
R["invariantes"]["k398c_TGLExt_maior_mtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mx))
R["invariantes"]["k398c_nao_tocado_hoje"] = time.strftime("%Y-%m-%d", time.localtime(mx)) != HOJE
# (5) processos: o robocopy que eu criei (PID 45448) nao esta mais rodando
r = subprocess.run(["tasklist", "/FI", "PID eq 45448"], capture_output=True, text=True, encoding="cp850", errors="replace")
R["invariantes"]["robocopy_pid_45448_encerrado"] = "robocopy" not in (r.stdout or "").lower()
R["todas_as_invariantes_ok"] = all([R["invariantes"]["um_py_do_nos_e_a_v398"], R["invariantes"]["core_selo_um_py_do_nos_iguais_aos_do_estudo"],
                                    not any(R["invariantes"]["arquivos_com_mtime_de_hoje_nas_pastas_do_operador"].values()), R["invariantes"]["Testemunho_lean_trabalho_igual_ao_sandbox"],
                                    R["invariantes"]["kernel_do_nos_sem_Testemunho_lean"], R["invariantes"]["k398c_nao_tocado_hoje"], R["invariantes"]["robocopy_pid_45448_encerrado"]])
with open(os.path.join(W, "INVENTARIO.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(json.dumps(R["invariantes"], ensure_ascii=False, indent=1))
print("todas as invariantes ok:", R["todas_as_invariantes_ok"])
for k, v in R["artefatos"].items():
    print("%-62s %s %s" % (k, v.get("sha16", "AUSENTE"), v.get("bytes", "")))
