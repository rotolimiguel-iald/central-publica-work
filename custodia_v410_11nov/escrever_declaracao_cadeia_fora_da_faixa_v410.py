# -*- coding: utf-8 -*-
r"""A declaracao do exame da cadeia de selo da v410 fora de +-50% da anterior (C3 do G1, errata de 11/11/2026). Copia a contagem e o sha256
da lista do CANDIDATO que a propria G1 gravou (nada digitado) e registra o exame. Grava com open('xb')."""
import hashlib
import json
import time
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
CAND = CEN / "work" / "custodia_v410_11nov" / "C3_CADEIA_FORA_DA_FAIXA_v410_candidato.json"
DEC = CEN / "work" / "custodia_G1" / "decisoes" / "CADEIA_DE_SELO_FORA_DA_FAIXA_v410.json"
V04 = CEN / "work" / "cunhagens_13out" / "OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt"
V10 = CEN / "work" / "cunhagens_13out" / "OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"
s = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

c = json.loads(CAND.read_text(encoding="utf-8"))
assert c["versao"] == "v410"
h = hashlib.sha256("\n".join(sorted(c["lista"])).encode("utf-8")).hexdigest()
assert h == c["lista_sha256"] and len(c["lista"]) == c["arquivos_no_cofre"]
d = {
    "schema": "iald.custodia.cadeia_fora_da_faixa/v1",
    "versao": "v410",
    "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "por": "claude-site-custodia (sessao de custodia), em nome proprio; a custodia inteira e da sessao de custodia (ordem do operador de 04/11/2026) e a da v410 corre desassistida (ordem de 10/11/2026)",
    "verbatim_04nov": {"arquivo": str(V04), "sha16": s(V04)[:16]},
    "verbatim_10nov": {"arquivo": str(V10), "sha16": s(V10)[:16]},
    "candidato": {"arquivo": str(CAND), "sha16": s(CAND)[:16]},
    "arquivos_no_cofre": c["arquivos_no_cofre"],
    "lista_sha256": c["lista_sha256"],
    "anterior": {"versao": c["anterior"], "arquivos_no_cofre": c["arquivos_no_cofre_anterior"], "razao": c["razao"]},
    "por_pasta": c["por_pasta"],
    "exame": [
        "Nenhum diretorio de ensaio novo: as duas subpastas novas em relacao a v409 sao de registro: r1_agente_logs (13 arquivos, logs do agente da rodada R1) e conserto_r3 (8, o conserto da rodada R3).",
        "O crescimento esta nos arquivos de primeiro nivel (249 na v409, 634 na v410), com 573 padroes de nome distintos: rodadas R1 a R6, saidas de construcao, transicoes ACOM e decisoes D da cadeia; a v410 correu de 06/11 a 11/11, foi reaberta duas vezes e teve seis rodadas de revisao.",
        "Nomes de registro de teste sao fracao estavel em todas as versoes (no cofre: v407 116/662, v408 115/588, v409 86/697; v410 134/1174); os relatorios SIMULACAO_ARVORE_NOS_* e EXAME_PONTOS_* ja entravam na v408 (15) e na v409 (20).",
        "Serie do cofre: v400 340, v401 434, v402 404, v403 432, v404 451, v405 452, v406 451, v407 662, v408 588, v409 697, v410 1174.",
        "A regra de copia nao mudou (FORA_RE, .bak_, raiz/temp/__pycache__/.lake, > 5 MB ficam fora). A guarda nao afrouxa: esta declaracao vale so para a v410 e para esta lista exata (contagem e sha256).",
    ],
}
b = (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
with DEC.open("xb") as f:
    f.write(b)
print(DEC.name, hashlib.sha256(b).hexdigest()[:16], len(b), "B | lista", c["lista_sha256"][:16], c["arquivos_no_cofre"])
