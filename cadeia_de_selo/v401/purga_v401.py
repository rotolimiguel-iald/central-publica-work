# -*- coding: utf-8 -*-
"""purga_v401.py -- SO LEITURA: conta, em toda a pasta v401 e no sandbox do kernel (C:\\t\\k401c), os arquivos que contem o texto da integra da fala de 25/10 retirada do trabalho
(a palavra de abertura do pedido de reserva e o hash da integra). Os padroes sao montados por concatenacao para este proprio arquivo NAO os conter. Grava purga_v401.json (so contagens e caminhos,
sem os padroes). Sai com rc 0 so' se ZERO ocorrencias.   uso: python -I -B -X utf8 purga_v401.py [--listar]"""
import json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PAT_A = ("entuasi" + "asmos").encode()          # a palavra de abertura da reserva (grafia da fala)
PAT_B = ("484ad9" + "82").encode()              # o prefixo do hash da integra
rx = re.compile(re.escape(PAT_A) + b"|" + re.escape(PAT_B), re.I)
raizes = [HERE, os.path.join("C:" + os.sep, "t", "k401c")]
res = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "raizes": {}}
total = 0
for r in raizes:
    achados, n = [], 0
    for d, ds, fs in os.walk(r):
        for f in fs:
            p = os.path.join(d, f); n += 1
            if f == "purga_v401.py" or f == "purga_v401.json":
                continue
            try:
                with open(p, "rb") as fh:
                    while True:
                        b = fh.read(8 << 20)
                        if not b:
                            break
                        if rx.search(b):
                            achados.append(p); break
                        if len(b) == (8 << 20):
                            fh.seek(-64, 1)   # sobreposicao: um padrao nao fica partido entre dois blocos
            except OSError as e:
                achados.append(p + "  [ERRO DE LEITURA: %s]" % e)
    res["raizes"][r] = {"arquivos_varridos": n, "com_ocorrencia": len(achados), "lista": achados}
    total += len(achados)
res["total_com_ocorrencia"] = total
p = os.path.join(HERE, "purga_v401.json")
open(p, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
for r, v in res["raizes"].items():
    print(r, "| varridos", v["arquivos_varridos"], "| com ocorrencia", v["com_ocorrencia"])
    if "--listar" in sys.argv:
        for x in v["lista"]:
            print("   ", x)
print("TOTAL com ocorrencia:", total)
sys.exit(0 if total == 0 else 1)
