# -*- coding: utf-8 -*-
"""medir_pinos.py -- todo hash citado em VINCULO_BANCADA_UMPY.md e lido do artefato AQUI, por script (regua n. 2: hash jamais de memoria).
Escreve PINOS_12out.json e PINOS_12out.md (a tabela que o desenho cita). Nao escreve fora de work\\bancada_vinculo_12out."""
import hashlib, json, datetime, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
CP = Path(r"C:\IALD\Central de Patentes")
O19 = CP / r"Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
BU = Path(r"C:\IALD\Bancada_Um")
EX = Path(r"C:\IALD\PROGRAMA_IALD\exame_12out")
ITENS = {
    "verbatim_operador_12out": CP / r"work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
    "um_py_v391": NOS / "um.py",
    "selo_v391": NOS / "um_absoluto_selo.json",
    "core_v391": NOS / "um_absoluto.json",
    "bancada_canonical_contracts_B2": BU / "canonical_contracts.json",
    "bancada_canonical_py": BU / "bancada" / "canonical.py",
    "bancada_CONTRATO_CANONICO_B2_md": BU / "CONTRATO_CANONICO_B2.md",
    "bancada_um_bancada_py": BU / "um_bancada.py",
    "bancada_mcp_um_py": BU / "mcp_um.py",
    "B2_DEPLOY_PLAN_R1": O19 / r"F0.3.B2\DEPLOY_PLAN_R1.json",
    "B2_DEPLOY_RECEIPT_R1": O19 / r"F0.3.B2\DEPLOY_RECEIPT_R1.json",
    "B2_build_manifest_py": O19 / r"F0.3.B2\build_manifest.py",
    "B2_deploy_candidate_py": O19 / r"F0.3.B2\deploy_candidate.py",
    "B2_restart_and_deploy_ps1": O19 / r"F0.3.B2\restart_and_deploy.ps1",
    "B2_RESTART_RECEIPT_R1": O19 / r"F0.3.B2\RESTART_RECEIPT_R1.json",
    "B2_verify_live_py": O19 / r"F0.3.B2\verify_live.py",
    "B2_verbatim_operador_09out": O19 / r"F0.3.B2\OPERADOR_ATUALIZACAO_VERBATIM_20261009.txt",
    "B2_verbatim_operador_10out": O19 / r"F0.3.B2\OPERADOR_CONTINUAR_20261010.txt",
    "relatorio_D_BANCADA": EX / r"D_BANCADA\RELATORIO_AUDITORIA_F0_3_B1_B2_C1.md",
    "relatorio_H_BANCADA": EX / r"H_BANCADA\RELATORIO_FRENTE_BANCADA_V392_12out.md",
    "H_BANCADA_BATERIA_FINAL_PROPOSTA_H12": EX / r"H_BANCADA\registros\BATERIA_FINAL_PROPOSTA_H12.json",
    "PLANO_V392_md": EX / r"J_SINTESE\PLANO_V392.md",
    "cadeia_v391_chain_pos_rito_sh": CP / r"work\v391_selo\chain_pos_rito_v391.sh",
    "cadeia_v391_fechar_py": CP / r"work\v391_selo\fechar_v391.py",
    "cadeia_v391_instalar_py": CP / r"work\cadeia_de_selo\v391\instalar_v391.py",
    "cadeia_v391_pins_py": CP / r"work\cadeia_de_selo\v391\v391_pins.py",
    "um_py_v380_registro_bancada_cache": NOS / "um.py",
    # os entregaveis deste desenho
    "vinculo_sincronizar_bancada_py": AQUI / "sincronizar_bancada.py",
    "vinculo_BATERIA_VINCULO_json": AQUI / "BATERIA_VINCULO.json",
    "vinculo_gerar_bateria_py": AQUI / "gerar_bateria.py",
    "vinculo_montar_sandbox_py": AQUI / "montar_sandbox.py",
    "vinculo_gerar_canais_mcp_py": AQUI / "gerar_canais_mcp.py",
    "vinculo_controles_negativos_py": AQUI / "controles_negativos.py",
    "vinculo_t01": AQUI / "bateria/t01_identidade.py",
    "vinculo_t06": AQUI / "bateria/t06_pantheon_rounding.py",
    "vinculo_t09": AQUI / "bateria/t09_nu4_replay.py",
    "vinculo_t10_t11": AQUI / "bateria/t10_t11_canais.py",
    "vinculo_t12_t14": AQUI / "bateria/t12_t14_atrator.py",
    "vinculo_t15": AQUI / "bateria/t15_sondas.py",
    "sandbox_SANDBOX_MANIFEST": AQUI / "sandbox/SANDBOX_MANIFEST.json",
    "sandbox_nos_sintetico_um_py": AQUI / "sandbox/nos_sintetico/um.py",
    "sandbox_nos_sintetico_selo": AQUI / "sandbox/nos_sintetico/um_absoluto_selo.json",
    "F0.6_unidade_json": AQUI / "F0.6_unidade.json",
    "PLANO_V392_paragrafo_B3_md": AQUI / "PLANO_V392_paragrafo_B3.md",
    "ATOS_DO_OPERADOR_md": AQUI / "ATOS_DO_OPERADOR.md",
}
# recibos produzidos pelo sandbox (os que existirem na hora da medida)
for extra in sorted(AQUI.glob("sandbox/saida_*/RECIBO_SINCRONIZACAO_*.json")) + sorted(AQUI.glob("sandbox/saida_*/MANIFESTO_CANDIDATO_B*.json")) \
        + sorted(AQUI.glob("sandbox/controles_negativos/CONTROLES_NEGATIVOS.json")) + sorted(AQUI.glob("sandbox/canais_gerados/*.py")) \
        + sorted(AQUI.glob("sandbox/canais_gerados/*.json")) + sorted(AQUI.glob("sandbox/bancada_copia/canonical_contracts.json*")) \
        + sorted(AQUI.glob("sandbox/bancada_copia/CONTRATO_CANONICO_B*.md")) + sorted(AQUI.glob("sandbox/saida_*/recibos/T*.json")):
    ITENS["sandbox_" + str(extra.relative_to(AQUI / "sandbox")).replace("\\", "/")] = extra
out = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "itens": {}}
for k, p in ITENS.items():
    p = Path(p)
    if not p.is_file():
        out["itens"][k] = {"path": str(p), "estado": "AUSENTE"}
        continue
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    out["itens"][k] = {"path": str(p), "sha256": h, "sha16": h[:16], "bytes": len(b)}
(AQUI / "PINOS_12out.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
linhas = ["| chave | arquivo | sha16 | bytes |", "|---|---|---|---|"]
for k, v in out["itens"].items():
    linhas.append("| `%s` | `%s` | `%s` | %s |" % (k, v["path"].replace("C:\\IALD\\Central de Patentes\\", "...\\"), v.get("sha16", "AUSENTE"), v.get("bytes", "")))
(AQUI / "PINOS_12out.md").write_text("# PINOS lidos por script em %s (medir_pinos.py)\n\n" % out["quando"] + "\n".join(linhas) + "\n", encoding="utf-8")
print("itens:", len(out["itens"]), "ausentes:", [k for k, v in out["itens"].items() if v.get("estado") == "AUSENTE"])
