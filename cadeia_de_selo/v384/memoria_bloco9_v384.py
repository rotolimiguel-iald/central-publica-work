# -*- coding: utf-8 -*-
"""Acrescenta o bloco 9 (03/10, tarde: a 3a e a 4a afericoes; a regra do marcador do servidor) a memoria v384-pilar-quantico-gpu-02out.md. Backup de BYTES antes;
temporario -> conferir -> substituir. Numeros LIDOS dos artefatos."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
D = json.load(open(os.path.join(HERE, "disposicoes_afericoes_v384.json"), encoding="utf-8"))
RB = json.load(open(os.path.join(HERE, "rascunho_prereg_v5", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), encoding="utf-8"))
RA = json.load(open(os.path.join(HERE, "rascunho_prereg_v5", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"), encoding="utf-8"))
CA = json.load(open(os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json"), encoding="utf-8"))
MARK = "<!-- estado_03out_afer34_v384 -->"
bloco = ("\n\n" + MARK + "\n"
         "**9. Estado (03/10/2026, tarde) e uma REGRA DE OPERAÇÃO — gerência, em nome próprio; números lidos por script:**\n"
         "- **REGRA (o marcador do servidor):** o lançador `rito_v384.sh` grava `scratchpad\\v384\\.servidor_parado_pelo_rito` (com `restaurar=0|1`) enquanto o servidor do modelo nativo "
         "está parado pelo rito. Se o lançador morrer à força e não houver rodada seguinte, **a gerência, ao abrir qualquer sessão da Central, confere esse marcador**: se existir com "
         "`restaurar=1`, religa a tarefa «IALD Llama Server» (`Start-ScheduledTask`) e só então apaga o marcador. O pré-registro da v384 cita esta regra.\n"
         "- **As aferições:** %s.\n"
         "- **Os rascunhos (v5):** B_REDUZIDO especificação `%s`, %s min de GPU (%s com margem); B_AMPLIADO_D64 (o antigo «A», renomeado: o «nível A» de 03/10 era o LEVE) "
         "especificação `%s`, %s min (%s com margem). A ratificação exige mensagem do operador POSTERIOR ao rascunho apresentado e que NOMEIE a escolha («b reduzido» ou «b ampliado»).\n"
         "- **O pacote:** trabalhador `%s` (E1..E8; o E8 é o comparador da referência na CPU); candidato de ENSAIO `%s` (%d patches); o candidato antigo `0dd43652` renomeado `*_PRE_AFER2`. "
         "A custódia da v384 leva a pasta da rodada (`Nós\\quantum_pillar\\run_<...>\\`, com `details.jsonl` e `cpuref.json` amarrados por hash no `result.json`).\n"
         "- **Lição (gerência):** ao gravar a 4ª passada, indexei por id e omiti entradas de id repetido em outra lente; a errata foi ao lado, no AFERIDOR e nas disposições.\n") % (
    D["texto_para_o_pre_registro"], RB["spec_sha256"][:16], RB["orcamento_estimado"]["total_min"], RB["orcamento_estimado"]["total_com_margem_min"],
    RA["spec_sha256"][:16], RA["orcamento_estimado"]["total_min"], RA["orcamento_estimado"]["total_com_margem_min"], RB["spec"]["worker_sha256"][:16], CA["sha16"], len(CA["patches"]))
raw = open(MEM, "rb").read()
assert MARK.encode("utf-8") not in raw, "o bloco 9 ja existe"
ts = time.strftime("%Y%m%d_%H%M%S"); bak = MEM + ".bak_" + ts
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
new = raw + bloco.encode("utf-8"); tmp = MEM + ".tmp_" + ts
open(tmp, "wb").write(new); assert os.path.getsize(tmp) == len(new) and open(tmp, "rb").read().startswith(raw)
os.replace(tmp, MEM); assert os.path.getsize(MEM) == len(new) > len(raw)
print("ok", len(raw), "->", len(new), "backup", os.path.basename(bak))
