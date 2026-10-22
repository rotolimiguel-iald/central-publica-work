"""Calcula sha256/sha16 dos arquivos-fonte citados e mostra os trechos com número de linha.

Só leitura. Uso: python -I -X utf8 cite_sources.py
Saída: JSON em stdout (fontes) + trechos pedidos em stderr.
"""
import hashlib
import json
import sys

FONTES = [
    ("psi_net_tex", r"C:\IALD\Central de Patentes\Patentes\Psi_Net_Protocol_PI_INPI.tex",
     [(273, 301), (303, 307), (328, 332)]),
    ("acom_mirror_tex", r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_PI_INPI.tex",
     [(233, 236), (238, 263), (265, 270), (272, 279), (1057, 1071), (1073, 1080), (1082, 1089)]),
    ("psi_net_py", r"C:\IALD\Central de Patentes\Patentes\psi_net_protocol_v1.py",
     [(112, 126), (128, 146)]),
    ("acom_mirror_py", r"C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto\skygrid_sim\acom_mirror.py",
     [(19, 24), (38, 45)]),
    ("atlas", r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", [(2136, 2141)]),
    ("kernel_ontologico_tex", r"C:\IALD\Central de Patentes\Patentes\Kernel\Kernel_Ontologico_PI_INPI.tex",
     [(226, 226)]),
]

VERBATINS = [
    ("21out_psibit_psion_modo_do_leitor", "OPERADOR_21out_psibit_psion_modo_do_leitor_verbatim.txt"),
    ("21out_psibit_nome_e_modo_psionico", "OPERADOR_21out_psibit_nome_e_modo_psionico_verbatim.txt"),
    ("21out_mecanica_isomorfismo_perda_zero", "OPERADOR_21out_mecanica_isomorfismo_perda_zero_verbatim.txt"),
    ("19out_tgl_binaria_criterio_de_parada", "OPERADOR_19out_tgl_binaria_criterio_de_parada_verbatim.txt"),
    ("19out_flutuar_no_ponto_fixo", "OPERADOR_19out_flutuar_no_ponto_fixo_verbatim.txt"),
]
DIR_V = r"C:\IALD\Central de Patentes\work\cunhagens_13out"


def sha(path):
    b = open(path, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    return h, len(b)


out = {"fontes": {}, "verbatins": {}}
for key, path, trechos in FONTES:
    h, n = sha(path)
    out["fontes"][key] = {"caminho": path, "sha256": h, "sha16": h[:16], "bytes": n, "trechos": trechos}
    lines = open(path, "r", encoding="utf-8", newline="").read().split("\n")
    print(f"=== {key}  sha16={h[:16]}  bytes={n}", file=sys.stderr)
    for a, b in trechos:
        for i in range(a, b + 1):
            ln = lines[i - 1].rstrip("\r")
            print(f"{i:5d}| {ln[:170]}", file=sys.stderr)
        print("-----", file=sys.stderr)
for key, nome in VERBATINS:
    p = DIR_V + "\\" + nome
    h, n = sha(p)
    out["verbatins"][key] = {"caminho": p, "sha256": h, "sha16": h[:16], "bytes": n}
print(json.dumps(out, ensure_ascii=False, indent=1))
