# -*- coding: utf-8 -*-
"""sha256 por script (bytes) de todo artefato citado no RELATORIO_FINAL (R2). Somente leitura."""
import hashlib, json, os, sys, time
BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
SP = (r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes"
      r"\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12")
ITENS = {
 "operador_12out": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "um_py_v391": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
 "memoria_tempo_santo": r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\tempo-santo-12out.md",
 "memoria_MEMORY_md": r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md",
 "R1_FREEZE": BASE + r"\1_PREREGISTRO\FREEZE.json",
 "R1_PREREGISTRO_json": BASE + r"\1_PREREGISTRO\PREREGISTRO.json",
 "R1_PREREGISTRO_md": BASE + r"\1_PREREGISTRO\PREREGISTRO.md",
 "R1_LEVANTAMENTO": BASE + r"\0_LEVANTAMENTO\LEVANTAMENTO.md",
 "R1_RESULTADO_OPTICO": BASE + r"\2_OPTICO\RESULTADO_OPTICO.json",
 "R1_run_optico": BASE + r"\2_OPTICO\run_optico.py",
 "R1_DIAGNOSTICO_T9c": BASE + r"\2_OPTICO\diagnostico\DIAGNOSTICO_T9c.json",
 "R1_RESULTADO_KERNEL": BASE + r"\3_KERNEL\RESULTADO_KERNEL.json",
 "R1_pedra_TheTimeHasNoRank": BASE + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean",
 "R1_pedra_olean": BASE + r"\3_KERNEL\sandbox\TheTimeHasNoRank.olean",
 "R1_RELATORIO_FINAL": BASE + r"\4_RELATORIO\RELATORIO_FINAL.md",
 "R1_registro_rota": BASE + r"\4_RELATORIO\registro_rota_F1.TEMPO.json",
 "R1_registro_mapa": BASE + r"\4_RELATORIO\registro_mapa_F1.TEMPO.json",
 "REPL_RESULTADO_OPTICO_rodada_2": BASE + r"\2_OPTICO\rodada_2\RESULTADO_OPTICO.json",
 "REPL_run_optico_rodada_2": BASE + r"\2_OPTICO\rodada_2\run_optico.py",
 "REPL_ACHADOS_rodada_2": BASE + r"\2_OPTICO\rodada_2\ACHADOS_FORA_DO_PREREGISTRO.json",
 "REPL_COMPARACAO_R1_R2": BASE + r"\2_OPTICO\rodada_2\COMPARACAO_R1_R2.json",
 "REPL_RECIBO_OPTICO_R2": BASE + r"\2_OPTICO\rodada_2\RECIBO_OPTICO_R2.json",
 "REPL_RESULTADO_KERNEL_rodada_2": BASE + r"\3_KERNEL\rodada_2\RESULTADO_KERNEL.json",
 "REPL_pedra_rodada_2": BASE + r"\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.lean",
 "REPL_pedra_rodada_2_olean": BASE + r"\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.olean",
 "REPL_ACHADOS_KERNEL_rodada_2": BASE + r"\3_KERNEL\rodada_2\ACHADOS_FORA_DO_PREREGISTRO.json",
 "R2_ADENDO_md": BASE + r"\5_R2\0_ADENDO\ADENDO_R2.md",
 "R2_ADENDO_json": BASE + r"\5_R2\0_ADENDO\ADENDO_R2.json",
 "R2_FREEZE_R2": BASE + r"\5_R2\0_ADENDO\FREEZE_R2.json",
 "R2_TOLERANCIA_UNIFORME": BASE + r"\5_R2\0_ADENDO\saidas\TOLERANCIA_UNIFORME_R2.json",
 "R2_tolerancia_uniforme_py": BASE + r"\5_R2\0_ADENDO\scripts\tolerancia_uniforme_r2.py",
 "R2_RESULTADO_PEDRA": BASE + r"\5_R2\1_PEDRA\RESULTADO_PEDRA_R2.json",
 "R2_MANIFESTO_1_PEDRA": BASE + r"\5_R2\1_PEDRA\MANIFESTO_1_PEDRA.json",
 "R2_pedra_TheTimeIsNotAPost": BASE + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean",
 "R2_pedra_olean": BASE + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.olean",
 "R2_pedra_T01": BASE + r"\5_R2\1_PEDRA\tentativas\T01_R2_TheTimeIsNotAPost.lean",
 "R2_ProbeE5": BASE + r"\5_R2\1_PEDRA\sandbox\ProbeE5.lean",
 "R2_AuditTiposR2": BASE + r"\5_R2\1_PEDRA\sandbox\AuditTiposR2.lean",
 "R2_TABELA_DECLARACOES_md": BASE + r"\5_R2\1_PEDRA\saidas\TABELA_DECLARACOES_R2.md",
 "R2_APLICACAO_E5": BASE + r"\5_R2\1_PEDRA\saidas\APLICACAO_E5.json",
 "R2_CONFERENCIA_ASPAS_PEDRA": BASE + r"\5_R2\1_PEDRA\saidas\CONFERENCIA_ASPAS_PEDRA_R2.json",
 "R2_LIMPEZA_RECIBO_PEDRA": BASE + r"\5_R2\1_PEDRA\saidas\LIMPEZA_RECIBO.json",
 "R2_R2_T02_recibo": BASE + r"\5_R2\1_PEDRA\logs\R2_T02_recibo.json",
 "R2_R2_T02_saida": BASE + r"\5_R2\1_PEDRA\logs\R2_T02_saida.txt",
 "R2_RESULTADO_REENSAIO": BASE + r"\5_R2\2_REENSAIO\RESULTADO_REENSAIO_R2.json",
 "R2_RECIBO_REENSAIO": BASE + r"\5_R2\2_REENSAIO\RECIBO_REENSAIO_R2.json",
 "R2_reensaio_py": BASE + r"\5_R2\2_REENSAIO\reensaio_r2.py",
 "R2_T9c_tsv": BASE + r"\5_R2\2_REENSAIO\T9c_float_E2_por_k.tsv",
 "R2_RECHECK_13out": BASE + r"\5_R2\2_REENSAIO\CONTINUACAO_13out\RECHECK_INDEPENDENTE_13out.json",
 "R2_RECIBO_CONTINUACAO_13out": BASE + r"\5_R2\2_REENSAIO\CONTINUACAO_13out\RECIBO_CONTINUACAO_13out.json",
 "R2_AUD_ESTATUTO_parcial_ASPAS": BASE + r"\5_R2\3_AUD_ESTATUTO\saidas\ASPAS_PEDRA_R2_AUDITOR.json",
 "R2_AUD_ESTATUTO_parcial_VARREDURA": BASE + r"\5_R2\3_AUD_ESTATUTO\saidas\VARREDURA_PALAVRAS_R2_AUDITOR.json",
 "audR_relatorio_md": SP + r"\TEMPO_AUD_REPRO\AUDITORIA_REPRO_TEMPO.md",
 "audR_AUD_COMPILE_PEDRA": SP + r"\TEMPO_AUD_REPRO\AUD_COMPILE_PEDRA.json",
 "audR_AUD_HASHES": SP + r"\TEMPO_AUD_REPRO\AUD_HASHES_ARTEFATOS.json",
 "audR_AUD_INDEPENDENTE": SP + r"\TEMPO_AUD_REPRO\AUD_INDEPENDENTE.json",
 "audE_MEDIDAS": SP + r"\TEMPO_AUD_ESTATUTO\MEDIDAS_AUD.json",
 "audE_HASHES_CITADOS": SP + r"\TEMPO_AUD_ESTATUTO\HASHES_CITADOS_AUD.json",
 "audE_VARREDURA": SP + r"\TEMPO_AUD_ESTATUTO\VARREDURA_PALAVRAS_AUD.json",
 "audE_ASPAS": SP + r"\TEMPO_AUD_ESTATUTO\ASPAS_PEDRA_AUD.json",
}
LONG = "\\\\?\\"
out = {"gerado_em_local": time.strftime("%Y-%m-%d %H:%M:%S"), "itens": {}}
for k, p in ITENS.items():
    try:
        b = open(LONG + p, "rb").read()
        st = os.stat(LONG + p)
        out["itens"][k] = {"caminho": p, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                           "mtime_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime))}
    except Exception as e:
        out["itens"][k] = {"caminho": p, "erro": repr(e)}
b = open(ITENS["operador_12out"], "rb").read()
i = b.find("O que mais me fascina".encode("utf-8"))
seg = b[i:]
out["operador_segunda_parte"] = {"offset_byte": i, "bytes": len(seg), "sha256": hashlib.sha256(seg).hexdigest(),
                                 "crlf": b.count(b"\r\n"),
                                 "ocorrencias_verbo_sem_caixa": b.decode("utf-8").lower().count("verbo")}
outp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "HASHES_RELATORIO_R2.json")
with open(outp + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(outp + ".tmp", outp)
sys.stdout.reconfigure(encoding="utf-8")
for k, v in out["itens"].items():
    print(k, (v.get("sha256") or v.get("erro"))[:16], v.get("bytes"), v.get("mtime_local"))
print("segunda_parte", out["operador_segunda_parte"])
