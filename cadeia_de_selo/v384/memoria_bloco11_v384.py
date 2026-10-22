# -*- coding: utf-8 -*-
"""Acrescenta o bloco 11 (estado de 04/10, os rascunhos v13 apresentados ao operador) a memoria da v384. Numeros LIDOS dos artefatos. Backup de BYTES;
temporario -> tamanho -> substituir -> conferir."""
import hashlib, json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
V = os.path.join(HERE, "rascunho_prereg_v13")
RB = json.load(open(os.path.join(V, "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), encoding="utf-8"))
RA = json.load(open(os.path.join(V, "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"), encoding="utf-8"))
D = json.load(open(os.path.join(HERE, "disposicoes_afericoes_v384.json"), encoding="utf-8"))
GEN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json"), encoding="utf-8"))
B = """

<!-- estado_04out_v13_v384 -->
**11. Estado (04/10/2026, depois das aferições 9–11) — os rascunhos v13 APRESENTADOS ao operador; gerência, em nome próprio; números lidos por script:**
- **As aferições:** 9ª %s; 10ª (estreita) %s; 11ª (verificação das frases que mudaram, um verificador independente): tudo o que mudou confere, 4 defeitos BAIXO tratados. Nenhum ALTO/MÉDIO desde a 8ª.
- **Os rascunhos v13** (`scratchpad\\v384\\rascunho_prereg_v13\\`; registro em `registro_rascunhos_apresentados_v384.json`, que o rascunho NÃO cita por hash): B_REDUZIDO JSON `%s` (gerado_utc %s), especificação `%s`, %.1f min (%.1f com a margem); B_AMPLIADO_D64 JSON `%s` (gerado_utc %s), especificação `%s`, %.1f min (%.1f com a margem). Gerador `%s`; candidato de ENSAIO `%s`.
- **O CONGELAMENTO, depois da mensagem do operador** (que tem de vir DEPOIS do gerado_utc do rascunho e NOMEAR «b reduzido» ou «b ampliado», sem negação): `python "%s" <PK>\\pilar_quantico_worker.py <PK>\\teste_tempo_v9\\result.json <PK>\\teste_motor_v8\\result.json <PK> --escolha=<B_REDUZIDO|B_AMPLIADO_D64> --ratificacao-prefixo="<início verbatim da mensagem dele>" --rascunho=<PK>\\rascunho_prereg_v13\\PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_<escolha>.json` (PK = `C:\\Users\\rotol\\AppData\\Local\\Temp\\claude\\c--IALD-Central-de-Patentes\\6da8f00d-d44f-4888-a88d-fc9f73eead3d\\scratchpad\\v384`). ATENÇÃO: qualquer mudança no gerador ou nas disposições/AFERIDOR DEPOIS da apresentação muda o V1 e o congelamento recusa — então é preciso rascunho novo e nova mensagem do operador.
- **Lição (gerência):** uma condição de registro leu uma saída TRUNCADA e omitiu uma ressalva (errata ao lado); e o teste C2 falhou na v13 por limite do PRÓPRIO teste (a cópia do pacote sem a aferição 10, que ficou obrigatória). Registro pós-rascunho vai a arquivo que o rascunho não cita por hash (senão é circular).
""" % (
    "%d entradas %s, %d novos BAIXO" % (D["passada9"]["n_entradas"], json.dumps(D["passada9"]["entradas"]), D["passada9"]["novos"]),
    "%d entradas %s, %d novos BAIXO (%d tocavam o rascunho)" % (D["passada10"]["n_entradas"], json.dumps(D["passada10"]["entradas"]), D["passada10"]["novos"], D["passada10"]["tocam_o_rascunho"]),
    h(os.path.join(V, "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"))[:16], RB["gerado_utc"], RB["spec_sha256"][:16], RB["orcamento_estimado"]["total_min"], RB["orcamento_estimado"]["total_com_margem_min"],
    h(os.path.join(V, "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"))[:16], RA["gerado_utc"], RA["spec_sha256"][:16], RA["orcamento_estimado"]["total_min"], RA["orcamento_estimado"]["total_com_margem_min"],
    h(GEN)[:16], CM["sha16"], GEN)
raw = open(M, "rb").read(); assert b"estado_04out_v13_v384" not in raw
bak = M + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + B.encode("utf-8"); open(M + ".tmp", "wb").write(novo); assert os.path.getsize(M + ".tmp") == len(novo); os.replace(M + ".tmp", M)
assert open(M, "rb").read() == novo and len(novo) > len(raw)
print("memoria v384:", len(raw), "->", len(novo))
