# -*- coding: utf-8 -*-
"""03/11/2026 01:5x, decisao da gerencia c1: o passo S5 do orquestrador (cadeia pos-rito 0 -> 10) FALHOU no passo 10 (B(n) ENSAIO pos-selo) por um unico teste, T17_LEAN_KERNEL: o kernel/lake_build.log em disco (sha16 91de25f9)
nao batia com o declarado no KERNEL_RECIBO_v406.json (47ddb1ca). Causa achada: a tarefa agendada IALD_build_k406c (criada ONCE com /ST 23:58 e disparada a mao as 19:56) DISPAROU DE NOVO as 23:58:00, rodou construir_kernel_v406.sh no sandbox
(build incremental sem nada a compilar; Audit identico) e reescreveu lake_build.log (o .sh guardou o original em lake_build.log.bak_20261102_235800). Reparo: o log original foi restaurado byte a byte (sha16 47ddb1ca, igual ao recibo e ao LOGS_COPIADOS),
o log da redisparada ficou ao lado (lake_build.log.rebuild_235800_sha91de25f9), a tarefa foi DESABILITADA, e o passo 10 foi rerodado sozinho (CHAIN_DE=10 CHAIN_ATE=10): BATERIA_PASSA, REPINADA_B15__ENSAIO__NADA_GRAVADO_NA_BANCADA.
Os passos 0 a 9 passaram na primeira rodada (01:41-01:43: conferidor TUDO BATE; superficies reais; memoria pinada) e NAO se repetem. Este script marca S5_cadeia_0_10 como ok=True no ESTADO.json, com esta nota, para o orquestrador retomar em S6.
Backup de bytes do ESTADO antes."""
import datetime, json, os, shutil
ORQ = os.path.dirname(os.path.abspath(__file__)); EST = os.path.join(ORQ, "ESTADO.json")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); shutil.copyfile(EST, EST + ".bak_" + ts)
e = json.load(open(EST, encoding="utf-8"))
s5 = e["passos"].get("S5_cadeia_0_10") or {}
assert s5.get("ok") is False and s5.get("rc") == 1, s5
out10 = open(os.path.join(ORQ, "chain_S5b_10_out.txt"), encoding="utf-8", errors="replace").read()
assert "BATERIA_PASSA" in out10 and "REPINADA_B15__ENSAIO__NADA_GRAVADO_NA_BANCADA" in out10 and "== FIM" in out10, "o passo 10 rerodado nao passou"
e["passos"]["S5_cadeia_0_10"] = {"ok": True, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "rc": 0, "de": 0, "ate": 10, "cauda": "",
                                "decisao_da_gerencia": "passos 0-9 passaram em 01:41-01:43 (chain_S5_cadeia_0_10_out.txt); o passo 10 falhou so' em T17_LEAN_KERNEL porque a tarefa ONCE IALD_build_k406c redisparou as 23:58 e reescreveu kernel/lake_build.log; log original restaurado do .bak_20261102_235800 (sha16 47ddb1ca == recibo), tarefa desabilitada, passo 10 rerodado sozinho (chain_S5b_10_out.txt): BATERIA_PASSA, REPINADA_B15__ENSAIO; marcado ok pela gerencia c1 em 03/11/2026 01:5x para retomar em S6",
                                "primeira_rodada": s5}
tmp = EST + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=1)); os.replace(tmp, EST)
print("S5 marcado ok; backup", os.path.basename(EST + ".bak_" + ts))
