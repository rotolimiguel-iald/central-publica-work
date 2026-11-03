# -*- coding: utf-8 -*-
"""rodar_por_entrada_v406.py -- roda CADA entrada de derivar_encanamento_v406.py separadamente (o driver para na primeira regra que nao casa; aqui cada entrada e' tentada e o resultado e' REGISTRADO): quais derivaram (so' o mapa, ou o mapa + as regras com contagem exata
que casaram) e quais abortaram, com a regra e a contagem. Nenhuma regra e' forcada: uma entrada que aborta nao grava nada (o motor so' grava depois de todas as regras e do ast.parse). Nao executa nenhum derivado.
Escreve DERIVACAO_ENCANAMENTO_v406_POR_ENTRADA.json (backup de BYTES do anterior). uso: python -I -B -X utf8 rodar_por_entrada_v406.py [--refazer]"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_encanamento_v406 as D  # noqa: E402
M = D.M
refazer = "--refazer" in sys.argv[1:]
res = []
for src, dst, regras, prot_extra, com_bump, autoral, origem in D.ENTRADAS:
    item = {"origem": src, "destino": dst, "n_regras": len(regras), "autoral_depois_da_subida": autoral}
    try:
        r = M.derivar(src, dst, regras, prot_extra, com_bump, refazer, origem=origem)
        item.update(resultado="PASSOU", estado=r["estado"], destino_sha256=r["destino_sha256"], origem_sha256=r["origem_sha256"])
    except SystemExit as e:
        item.update(resultado="ABORTOU", motivo=str(e.code)[:600])
    except (AssertionError, FileNotFoundError, ValueError, SyntaxError, KeyError, IndexError) as e:
        item.update(resultado="ABORTOU", motivo="%s: %s" % (type(e).__name__, str(e)[:600]))
    res.append(item)
    print("%-9s %-52s regras=%d %s" % (item["resultado"], dst, len(regras), item.get("estado", "") or item.get("motivo", "")[:140]))
out = os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v406_POR_ENTRADA.json")
txt = json.dumps({"contrato": "DERIVACAO_ENCANAMENTO_v406_POR_ENTRADA", "executado": False, "lotes_nao_carregados": D.LOTES_NAO_CARREGADOS, "entradas": res,
                  "passaram": sum(1 for x in res if x["resultado"] == "PASSOU"), "abortaram": sum(1 for x in res if x["resultado"] == "ABORTOU")}, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(out):
    open(out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(out, "rb").read())
open(out + ".tmp", "wb").write(txt); os.replace(out + ".tmp", out)
print("passaram", sum(1 for x in res if x["resultado"] == "PASSOU"), "abortaram", sum(1 for x in res if x["resultado"] == "ABORTOU"), "lotes nao carregados", len(D.LOTES_NAO_CARREGADOS))
