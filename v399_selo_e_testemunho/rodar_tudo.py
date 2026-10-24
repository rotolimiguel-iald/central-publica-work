# -*- coding: utf-8 -*-
"""rodar_tudo.py -- a CADEIA do estudo, em ordem, com parada no primeiro erro (fail-closed): montar_prototipo -> estudo -> simulacao da colagem -> reprodutibilidade entre
interpretadores -> recibo da suite do operador -> RESULTADO.md -> registro do mapa (validado, sem registrar) -> inventario e invariantes.
Os processos criados aqui terminam sozinhos. Uso: python -B -X utf8 rodar_tudo.py <pasta_temporaria_da_simulacao>"""
import os
import subprocess
import sys
import time

W = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Python314\python.exe"
TMP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("TEMP", W), "sim_v399")
PASSOS = [
    ("consultar_mapa", [PY, "-I", "-B", "-X", "utf8", "consultar_mapa.py"]),
    ("montar_prototipo",[PY, "-I", "-B", "-X", "utf8", "montar_prototipo.py"]),
    ("estudo", [PY, "-B", "-X", "utf8", "selo_acom_prototipo.py", "estudo"]),
    ("simulacao_da_colagem", [PY, "-B", "-X", "utf8", "gerar_registro_declaracao.py", TMP]),
    ("reprodutibilidade", [PY, "-B", "-X", "utf8", "reprodutibilidade.py"]),
    ("recibo_testes_operador", [PY, "-I", "-B", "-X", "utf8", "recibo_testes_operador.py"]),
    ("resultado", [PY, "-I", "-B", "-X", "utf8", "gerar_resultado.py"]),
    ("registro_mapa", [PY, "-B", "-X", "utf8", "gerar_registro_mapa.py"]),
    ("varredura_textos", [PY, "-I", "-B", "-X", "utf8", "varredura_textos.py"]),
    ("inventario", [PY, "-I", "-B", "-X", "utf8", "inventario_final.py"]),
]
for nome, cmd in PASSOS:
    t0 = time.perf_counter()
    r = subprocess.run(cmd, cwd=W, capture_output=True, text=True, encoding="utf-8", timeout=1800)
    open(os.path.join(W, "saida_%s.txt" % nome), "w", encoding="utf-8", newline="\n").write(r.stdout + ("\n--- stderr ---\n" + r.stderr if r.stderr.strip() else ""))
    print("%-24s rc=%d %6.1fs" % (nome, r.returncode, time.perf_counter() - t0), flush=True)
    if r.returncode != 0:
        print(r.stdout[-1500:], r.stderr[-1500:])
        sys.exit(r.returncode)
print("CADEIA COMPLETA")
