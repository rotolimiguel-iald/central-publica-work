# -*- coding: utf-8 -*-
"""03/11/2026 02:0x, decisao da gerencia c1: o passo S6c_chain_10c_14 FALHOU no primeiro import de delta_v406.py (a funcao _bancada_pina_hoje so' aceitava a base v405; depois do APLICAR a Bancada pina B15-v406: defeito do delta, nao da cadeia).
Reparo: a funcao aceita a base OU esta versao (BANCADA_JA_APLICADA diz qual), errata ao lado no proprio delta; a cadeia 10c -> 14 foi rerodada inteira (chain_S6c_b_10c_14_out.txt): rc 0 (fechar: manifesto e handoff; mapa registrado; inventario; Nos vivo; rascunho do X).
Marca S6c_chain_10c_14 como ok=True no ESTADO.json, com a nota, para o orquestrador retomar em S7 (G1). Backup de bytes do ESTADO antes."""
import datetime, json, os, shutil
ORQ = os.path.dirname(os.path.abspath(__file__)); EST = os.path.join(ORQ, "ESTADO.json")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); shutil.copyfile(EST, EST + ".bak_" + ts)
e = json.load(open(EST, encoding="utf-8"))
s = e["passos"].get("S6c_chain_10c_14") or {}
assert s.get("ok") is False and s.get("rc") == 1, s
out = open(os.path.join(ORQ, "chain_S6c_b_10c_14_out.txt"), encoding="utf-8", errors="replace").read()
assert "== FIM" in out and "PARADA" not in out and "AGUARDA_OPERADOR" not in out, "a cadeia 10c-14 rerodada nao chegou ao FIM limpa"
e["passos"]["S6c_chain_10c_14"] = {"ok": True, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "rc": 0, "de": "10c", "ate": "14", "cauda": "",
                                   "decisao_da_gerencia": "a primeira rodada parou no import de delta_v406.py (_bancada_pina_hoje exigia a base v405; a Bancada ja pinava B15-v406 depois do 10b): defeito do delta, corrigido com errata ao lado (aceita base ou esta versao; BANCADA_JA_APLICADA); a cadeia 10c-14 foi rerodada inteira pela gerencia (chain_S6c_b_10c_14_out.txt, rc 0, FIM 02:03:09); marcado ok em 03/11/2026 02:0x para retomar em S7",
                                   "primeira_rodada": s}
tmp = EST + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=1)); os.replace(tmp, EST)
print("S6c marcado ok; backup", os.path.basename(EST + ".bak_" + ts))
