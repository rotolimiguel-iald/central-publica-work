# -*- coding: utf-8 -*-
"""consultar_mapa.py -- consulta o MAPA DE ROTAS (so leitura: `rotas.py consultar`) para os temas desta tarefa e grava mapa_consultas.json com a contagem, a cabeca da
cadeia e as rotas relevantes (id, status, titulo curto). NADA e' registrado. Uso: python -I -B -X utf8 consultar_mapa.py"""
import json
import os
import subprocess
import time

W = os.path.dirname(os.path.abspath(__file__))
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
TEMAS = ["acom crypto", "acom", "criptografia", "selo", "testemunho", "testemunha", "mirror", "dobra", "hash", "Palavra", "k398", "psibit", "token", "tetelestai", "declaracao do operador",
         "inscricao", "transporte"]
saida = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "consultas": {}}
cabeca = None
for t in TEMAS:
    r = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", ROTAS, "consultar", t, "--limite", "200"], capture_output=True, text=True, encoding="utf-8", timeout=120)
    if r.returncode != 0:
        # versao do rotas.py sem --limite: tenta sem
        r = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", ROTAS, "consultar", t], capture_output=True, text=True, encoding="utf-8", timeout=120)
    d = json.loads(r.stdout)
    cabeca = d.get("cabeca")
    saida["consultas"][t] = {"n": d.get("n"), "truncado": d.get("truncado"), "rotas_relevantes": [
        {"rota_id": x["rota_id"], "status": x["status"], "titulo": (x.get("titulo") or "")[:150]} for x in d.get("rotas", [])
        if any(k in (x["rota_id"] + " " + (x.get("titulo") or "")).lower() for k in ("acom", "testemunh", "selo", "psibit", "token", "criptograf", "mirror", "tetelestai", "declara", "transporte", "inscri"))][:12]}
saida["cabeca_da_cadeia_na_consulta"] = cabeca
saida["n_registros"] = d.get("n_registros")
saida["leitura"] = ("nenhuma rota examina o ACOM Mirror Crypto como selo do um.py (acom crypto: 0; criptografia: 0; testemunho: 0). As rotas vizinhas sao as pedras ja seladas "
                    "(psibit_v395, testemunha_estatica_v396, Token/teste da unica palavra v397, Sonico/Afinacao v398) e as custodias; nada foi refeito.")
p = os.path.join(W, "recibos", "mapa_consultas.json")
os.makedirs(os.path.dirname(p), exist_ok=True)
if os.path.exists(p):
    with open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "xb") as f:
        f.write(open(p, "rb").read())
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(saida, f, ensure_ascii=False, indent=1)
for t, v in saida["consultas"].items():
    print("%-26s n=%-4s relevantes: %s" % (t, v["n"], [x["rota_id"] for x in v["rotas_relevantes"]][:5]))
print("cabeca:", cabeca, "| registros:", saida["n_registros"])
