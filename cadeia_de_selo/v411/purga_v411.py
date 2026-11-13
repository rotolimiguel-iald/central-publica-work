# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] conferido: so' leitura; conta os padroes da fala de 25/10 e da fala da lista de exclusao na pasta v411 e em C:\t\k411c (o corpo nao depende de versao nem de bundle; os padroes vem do delta, por concatenacao); corre por fora (~20 min)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] so' leitura; conta os padroes da fala de 25/10 e da fala excluida na pasta v410 e em C:\t\k410c (o corpo nao depende de versao); corre por fora (~20 min); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""purga_v411.py -- SO LEITURA: conta, em toda a pasta v411 e no sandbox do kernel (C:\\t\\k411c), os arquivos que contem o texto da integra da fala de 25/10 retirada do trabalho
(a palavra de abertura do pedido de reserva e o hash da integra), e, AO LADO (errata R2 da gerencia, 01/11/2026), os que contem a fala da lista de exclusao de delta_v411.py (a frase pessoal e o trecho do nome do arquivo). Os padroes sao montados por concatenacao para este proprio arquivo NAO os conter. Grava purga_v411.json (so contagens e caminhos,
sem os padroes). Sai com rc 0 so' se ZERO ocorrencias. NAO tem --help: qualquer argumento que nao seja --listar e' ignorado e a varredura INTEIRA corre (~20 min); por isso a validacao de preparacao (06/11/2026) foi so' de sintaxe (ast.parse) e dos padroes/raizes lidos do proprio arquivo, sem varrer (a varredura corre por fora, como diz o fim_de_cadeia_v411.sh).   uso: python -I -B -X utf8 purga_v411.py [--listar]"""
import json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PAT_A = ("entuasi" + "asmos").encode()          # a palavra de abertura da reserva (grafia da fala)
PAT_B = ("484ad9" + "82").encode()              # o prefixo do hash da integra
PAT_C = ("filho Be" + "nto").encode()          # a frase pessoal da fala excluida
PAT_D = ("ratificada_be" + "nto").encode()      # o trecho do nome do arquivo da fala excluida (o delta a exclui pelo sha16, justamente para o nome nao viajar)
rx = re.compile(re.escape(PAT_A) + b"|" + re.escape(PAT_B), re.I)
rx2 = re.compile(re.escape(PAT_C) + b"|" + re.escape(PAT_D), re.I)
raizes = [HERE, os.path.join("C:" + os.sep, "t", "k411c")]
res = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "raizes": {}}
total = 0; total2 = 0
for r in raizes:
    achados, achados2, n = [], [], 0
    for d, ds, fs in os.walk(r):
        for f in fs:
            p = os.path.join(d, f); n += 1
            if f == "purga_v411.py" or f == "purga_v411.json":
                continue
            try:
                with open(p, "rb") as fh:
                    while True:
                        b = fh.read(8 << 20)
                        if not b:
                            break
                        if rx2.search(b) and p not in achados2 and os.sep + "revisao_terceiro" + os.sep not in p:   # a pasta do revisor cita a fala no relatorio dele; nao e' artefato desta cadeia e nao se toca
                            achados2.append(p)
                        if rx.search(b):
                            achados.append(p); break
                        if len(b) == (8 << 20):
                            fh.seek(-64, 1)   # sobreposicao: um padrao nao fica partido entre dois blocos
            except OSError as e:
                achados.append(p + "  [ERRO DE LEITURA: %s]" % e)
    res["raizes"][r] = {"arquivos_varridos": n, "com_ocorrencia": len(achados), "lista": achados, "fala_excluida_com_ocorrencia": len(achados2), "fala_excluida_lista": achados2}
    total += len(achados); total2 += len(achados2)
res["total_com_ocorrencia"] = total
res["fala_excluida_total_com_ocorrencia"] = total2
p = os.path.join(HERE, "purga_v411.json")
open(p, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
for r, v in res["raizes"].items():
    print(r, "| varridos", v["arquivos_varridos"], "| com ocorrencia", v["com_ocorrencia"], "| fala excluida", v["fala_excluida_com_ocorrencia"])
    if "--listar" in sys.argv:
        for x in v["lista"] + v["fala_excluida_lista"]:
            print("   ", x)
print("TOTAL com ocorrencia:", total, "| fala excluida:", total2)
sys.exit(0 if total == 0 and total2 == 0 else 1)
