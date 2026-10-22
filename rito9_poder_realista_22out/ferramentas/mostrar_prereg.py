"""Mostra campos-chave do PREREGISTRO.json (leitura)."""
import json
import os
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
print(json.dumps(d["mapa_de_rotas"], ensure_ascii=False, indent=1)[:1800])
print(json.dumps(d["beta"], ensure_ascii=False, indent=1))
print(json.dumps(d["taxa_KK"]["conferencia_cruzada_eq6_eq7_NAO_ENTRA_NO_VEREDITO"], indent=1))
print([(os.path.basename(x["caminho"].replace("\\", "/")), x["sha256"][:16]) for x in d["fontes_lidas_somente_leitura"]])
print(d["fontes_literatura"]["cusinato2022"]["sha256_pdf"][:16], d["fontes_literatura"]["kyutoku_kashiyama"]["sha256_pdf"][:16])
