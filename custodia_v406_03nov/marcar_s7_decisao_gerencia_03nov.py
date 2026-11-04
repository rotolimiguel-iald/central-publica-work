# -*- coding: utf-8 -*-
"""03/11/2026 06:2x, gerencia c1: marca o S7 do orquestrador pos_treino_v406 como concluido POR DECISAO DA GERENCIA, no molde do S5 e do S6c (primeira_rodada preservada;
decisao dita por inteiro). O que a G1 fez (run v406_20261103_055852 e anteriores): 37 passos APLICADOS (cofre, kernel, runner v70, 16 dispositivos, FINAL, ledger, commit/push do
espelho a381c4d1 e da Central 42f3b0c9, site v406 no ar em duas subidas verificadas (03:10 e 06:09, a segunda com os 83 arquivos da Central publica), leitor de IA R1, ACOM t1/t2,
registro PUBLICADA e rota custodia.v406, Central publica 22/22 no quadro das 06:10, Nos vivo e TORRE_v406.json); `auditar` rc 0. C19 parou na classificacao do quadro: 7 DEFASADOS,
todos fora do alcance desta custodia: 2 da fila cientifica (ACTIVE.json v404 e DELIVERY v406: so o Codex, sem cota ate 04/11 06:37), 1 agregado da Torre e 4 itens dela (JEV v406:
nasce com a release do app, C21, decisao do operador; missao ACOM de 12/10 recusada pelo guarda de confidencialidade; CLAUDE.md de Haja_Luz 1.245.626 B e da Nativa 636.937 B acima do
teto de 262.144 B da Torre). C20 e C17C (t3) ficam abertos, como na v405. O executar devolveu 20 porque esses itens nao sao classificados como «do operador»; a leitura da gerencia e'
«custodia PUBLICADA; t3 aberto». Backup de bytes da ESTADO.json; temporario -> os.replace. Escrito pelo Write."""
import json, os, time
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v406\orquestrador\ESTADO.json")
TS = time.strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); d = json.loads(b.decode("utf-8")); s7 = d["passos"]["S7_g1"]
assert s7.get("ok") is False and s7.get("executar") == 20 and s7.get("auditar") == 0, s7
novo = {"ok": True, "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "planejar": 1, "executar": 20, "auditar": 0, "nota": "5 = só decisões do operador",
        "decisao_da_gerencia": ("custodia v406 PUBLICADA (espelho a381c4d1 = origin/main; Central 42f3b0c9 = origin/main; site v406 no ar: subidas verificadas 20261103_025919 e "
                                "20261103_055922, esta com os 83 arquivos da Central publica depois da reversao da 052210 pelo Range do hospedeiro, licoes 49 e 50; leitor de IA R1; "
                                "Central publica 22/22 no quadro das 06:10; conferencia final 13/13; ACOM t1/t2; rota custodia.v406; Nos vivo; TORRE_v406.json; auditar rc 0). "
                                "C19 parou na classificacao do quadro das 06:11: 7 DEFASADOS fora do alcance desta custodia (2 da fila cientifica: ACTIVE.json v404 e DELIVERY v406, so o "
                                "Codex, sem cota ate 04/11 06:37; Torre: JEV v406 nasce com a release do app (C21, decisao do operador), missao ACOM de 12/10 recusada pelo guarda, "
                                "CLAUDE.md de Haja_Luz e da Nativa acima do teto de 262.144 B). C20 e C17C (t3) ficam abertos, como na v405. Marcado ok pela gerencia c1 em 03/11/2026 "
                                "06:2x para o S9 escrever o relatorio; nada aqui move gate, selo ou cofre."),
        "pendentes_t3": ["C19 (quadro sem DEFASADO)", "C20 (ACTIVE.json/DELIVERY v406: Codex)", "C17C (ACOM t3)", "C21 (release do app v406: operador)"],
        "primeira_rodada": s7}
d["passos"]["S7_g1"] = novo
bak = P.with_name(P.name + ".bak_" + TS + "_c1_s7"); open(bak, "xb").write(b); assert bak.read_bytes() == b
out = json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8")
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(out); os.replace(tmp, P)
assert json.loads(P.read_text(encoding="utf-8"))["passos"]["S7_g1"]["ok"] is True
print("ESTADO.json: S7_g1 marcado ok pela gerencia; backup", bak.name)
