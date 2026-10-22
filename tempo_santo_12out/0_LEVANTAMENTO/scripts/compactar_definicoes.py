"""Gera a forma COMPACTA de DEFINICOES.json (somente leitura do JSON completo), para o retorno estruturado:
cada objeto com id, termo, linha no texto, classe, estatuto, reafirma, novo, riscos e as ancoras como 'arquivo:linha·sha16·estatuto'.
Uso: python -I compactar_definicoes.py <DEFINICOES.json> <saida_compacta.json>"""
import hashlib
import json
import os
import sys


def main(src, out):
    raw = open(src, "rb").read()
    d = json.loads(raw.decode("utf-8"))
    objs = []
    for o in d["objetos"]:
        objs.append(dict(id=o["id"], termo=o["termo"], linha_texto=o["texto_operador"]["linha"], classe=o.get("classe"),
                         estatuto=o.get("estatuto_global"), reafirma=o.get("reafirma"), novo=o.get("novo"),
                         riscos=o.get("riscos"), knownn=o.get("knownn"), consulta_ausencia=o.get("consulta_ausencia"),
                         ancoras=["%s:%s·%s·%s" % (os.path.basename(a["arquivo"]), a["linha"], a["sha16"], a["estatuto"])
                                  for a in o["ancoras"]]))
    m = d["medidas"]
    c = dict(arquivo_completo=os.path.abspath(src), sha256_completo=hashlib.sha256(raw).hexdigest(),
             unidade=d["unidade"], data=d["data"], texto_operador=d["texto_operador"],
             beta=m["beta"], kernel_impressao_iguais=m["kernel_impressao"]["iguais"], lean=m["lean"],
             audit_lean_sha16=d["audit_lean_sha16"], n_ancoras=d["n_ancoras"],
             ancoras_nao_achadas=d["ancoras_nao_achadas"], objetos=objs,
             n_teoremas=len(d["teoremas_existentes"]), riscos_ids=sorted(d["riscos"].keys()))
    s = json.dumps(c, ensure_ascii=False, separators=(",", ":"))
    with open(out, "w", encoding="utf-8") as fo:
        fo.write(s)
    print(len(s))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
