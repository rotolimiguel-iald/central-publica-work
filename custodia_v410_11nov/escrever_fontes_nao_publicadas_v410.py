# -*- coding: utf-8 -*-
"""Decisao FONTES_NAO_PUBLICADAS_v410.json (molde da v408): a fonte pinada que fez a E03 parar fica FORA do espelho. Grava com open('xb')."""
import hashlib, json, time
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes")
DEC = CEN / "work" / "custodia_G1" / "decisoes" / "FONTES_NAO_PUBLICADAS_v410.json"
SRC = CEN / "work" / "cadeia_de_selo" / "v410" / "insumos" / "h0dn_LEITURA_DOSSIE_5SIGMA_09nov.json"
REGUA = Path(r"C:\Users\rotol\.claude\CLAUDE.md")
V04 = CEN / "work" / "cunhagens_13out" / "OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt"
V10 = CEN / "work" / "cunhagens_13out" / "OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"
ANT = CEN / "work" / "custodia_G1" / "decisoes" / "FONTES_NAO_PUBLICADAS_v408.json"
HO = CEN / "work" / "cadeia_de_selo" / "v410" / "ORDEM_HANDOFF_CUSTODIA_v410.md"
RUN = CEN / "work" / "custodia_G1" / "runs" / "v410_20261111_024356"
s256 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
regua = REGUA.read_text(encoding="utf-8")
assert "Confidenciais nunca saem" in regua
d = {
 "schema": "iald.custodia.fontes_nao_publicadas/v1",
 "versao": "v410",
 "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
 "por": "claude-site-custodia (sessao de custodia), em nome proprio, aplicando a ordem vigente do operador, como na v407 (gerencia c1) e na v408",
 "decisao_do_operador": {
  "verbatim": str(REGUA), "sha16": s256(REGUA)[:16],
  "o_que_diz": "A regua, item 8 (instrucoes globais do operador): os arquivos confidenciais da casa nunca saem, nem em commit, nem em publicacao (so existencia/mtime). Em 04/11/2026 o operador devolveu a custodia inteira a sessao de custodia (verbatim ao lado) e em 10/11/2026 ordenou a custodia desassistida da v410: deixar esta fonte fora do espelho e cumprimento da ordem vigente, nao decisao nova.",
  "verbatim_04nov": str(V04), "sha16_04nov": s256(V04)[:16],
  "verbatim_10nov": str(V10), "sha16_10nov": s256(V10)[:16],
  "decisao_anterior": {"arquivo": str(ANT), "sha16": s256(ANT)[:16]},
  "handoff_v410": {"arquivo": str(HO), "sha16": s256(HO)[:16]},
 },
 "arquivos": [{
  "arquivo": str(SRC), "sha256": s256(SRC),
  "motivo": "insumo pinado pelo um.py v410 (leitura do dossie H0DN de 09/11). A E03 da v410 parou nele (termo-guarda a mais; recibo %s): o campo de proveniencia que lista o que NAO foi lido de proposito nomeia dois arquivos confidenciais da casa. Nao ha copia purgada pinada; a fonte fica FORA do espelho e no cofre da Central. A gerencia c1 foi avisada para a v411 pinar uma copia sem esses nomes." % RUN,
 }],
 "nota": "a guarda nao afrouxa: a fonte nao entra; vale so para a v410 e para este sha256; mudou o arquivo, a decisao nao cobre",
}
b = (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
with DEC.open("xb") as f:
    f.write(b)
print(DEC.name, hashlib.sha256(b).hexdigest()[:16], len(b), "B | fonte sha16", s256(SRC)[:16])
