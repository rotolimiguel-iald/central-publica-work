# -*- coding: utf-8 -*-
"""_r6c_09_conferir_itens_v410.py -- o CONSERTO UNICO da v410: conferencia, SO' LEITURA, dos 290 itens de troca exata da ESPEC_CONSERTO_R3_v2_FINAL.json contra os arquivos COMO ESTAO AGORA (depois das instrucoes e das adaptacoes do construtor):
para cada item, o trecho novo esta' no arquivo ao menos o numero de vezes do item, e o trecho atual sumiu (salvo quando o novo o contem). Diz, item a item, o que as instrucoes ou as adaptacoes do construtor mexeram DEPOIS da aplicacao
(o trecho novo que deixou de aparecer inteiro), para a conferencia de escopo fechado da gerencia. Grava _r6c_ITENS_v410.json por temporario + os.replace.   uso: python -I -B -X utf8 _r6c_09_conferir_itens_v410.py"""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda rel: os.path.join(HERE, *rel.split("/"))
ESPEC = P("conserto_r3/ESPEC_CONSERTO_R3_v2_FINAL.json"); b = open(ESPEC, "rb").read(); assert hashlib.sha256(b).hexdigest() == "8ecf4082e657bd69887c52e0e7d8efbcdbfc85eb4d739679227c9b11f5c23f19"
D = json.loads(b.decode("utf-8")); tx = {}; faltam = []; atual_ficou = []; ok = 0
for it in D["itens"]:
    if it["tipo"] != "TROCA_EXATA":
        continue
    r = it["arquivo_rel"]
    if r not in tx:
        tx[r] = open(P(r), "rb").read().decode("utf-8").replace("\r\n", "\n")
    cn = tx[r].count(it["trecho_novo"]); ca = tx[r].count(it["trecho_atual"]); contem = it["trecho_atual"] in it["trecho_novo"]
    if cn < it["ocorrencias"]:
        faltam.append({"n": it["n"], "arquivo": r, "linha": it.get("linha"), "novo_no_arquivo": cn, "ocorrencias": it["ocorrencias"], "inicio_do_novo": it["trecho_novo"][:120]})
    elif ca and not contem:
        atual_ficou.append({"n": it["n"], "arquivo": r, "atual_no_arquivo": ca})
    else:
        ok += 1
out = {"contrato": "R6c_ITENS_v410", "quando": time.strftime("%d/%m/%Y %H:%M:%S"), "espec_sha256": hashlib.sha256(b).hexdigest(), "n_itens_de_troca": sum(1 for i in D["itens"] if i["tipo"] == "TROCA_EXATA"), "n_ok": ok,
       "trecho_novo_que_nao_esta_mais_inteiro": faltam, "trecho_atual_que_ficou": atual_ficou, "sha16_dos_arquivos": {r: hashlib.sha256(open(P(r), "rb").read()).hexdigest()[:16] for r in sorted(tx)}}
p = P("_r6c_ITENS_v410.json"); open(p + ".tmp", "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print("itens de troca:", out["n_itens_de_troca"], "| ok:", ok, "| trecho novo que nao esta' mais inteiro:", [(x["n"], x["arquivo"]) for x in faltam], "| trecho atual que ficou:", [(x["n"], x["arquivo"]) for x in atual_ficou])
