"""Relatorio R2 da F1.TEMPO: sha256 e bytes de cada artefato citado (lidos do disco, nunca de memoria),
beta em runtime a partir dos bytes do um.py (l.95 e l.5557), e conferencia do FREEZE R1 e do FREEZE_R2.
Escreve SO em 4_RELATORIO_R2/saidas. Uso: python -I hashes_relatorio_r2.py"""
import hashlib, json, math, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
C = r"C:\IALD\Central de Patentes\work"
OUT = os.path.join(W, r"5_R2\4_RELATORIO_R2\saidas")
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest(), os.path.getsize(p)


ART = {
 "R1.FREEZE": W + r"\1_PREREGISTRO\FREEZE.json",
 "R1.PREREGISTRO.json": W + r"\1_PREREGISTRO\PREREGISTRO.json",
 "R1.PREREGISTRO.md": W + r"\1_PREREGISTRO\PREREGISTRO.md",
 "R1.RESULTADO_OPTICO": W + r"\2_OPTICO\RESULTADO_OPTICO.json",
 "R1.DIAGNOSTICO_T9c": W + r"\2_OPTICO\diagnostico\DIAGNOSTICO_T9c.json",
 "R1.RESULTADO_KERNEL": W + r"\3_KERNEL\RESULTADO_KERNEL.json",
 "R1.pedra.TheTimeHasNoRank.lean": W + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean",
 "R1.pedra.olean": W + r"\3_KERNEL\sandbox\TheTimeHasNoRank.olean",
 "R1.RELATORIO_FINAL_R1.md": W + r"\4_RELATORIO\R1_preservado\RELATORIO_FINAL_R1.md",
 "R1.registro_mapa_R1": W + r"\4_RELATORIO\R1_preservado\registro_mapa_F1.TEMPO_R1.json",
 "4_RELATORIO.RELATORIO_FINAL.md (redacao de 13/10 01:04, anterior as auditorias R2)": W + r"\4_RELATORIO\RELATORIO_FINAL.md",
 "4_RELATORIO.registro_mapa_F1.TEMPO.json (idem)": W + r"\4_RELATORIO\registro_mapa_F1.TEMPO.json",
 "4_RELATORIO.registro_rota_F1.TEMPO.json": W + r"\4_RELATORIO\registro_rota_F1.TEMPO.json",
 "ADENDO.ADENDO_R2.md": W + r"\5_R2\0_ADENDO\ADENDO_R2.md",
 "ADENDO.ADENDO_R2.json": W + r"\5_R2\0_ADENDO\ADENDO_R2.json",
 "ADENDO.FREEZE_R2.json": W + r"\5_R2\0_ADENDO\FREEZE_R2.json",
 "ADENDO.tolerancia_uniforme_r2.py": W + r"\5_R2\0_ADENDO\scripts\tolerancia_uniforme_r2.py",
 "ADENDO.TOLERANCIA_UNIFORME_R2.json": W + r"\5_R2\0_ADENDO\saidas\TOLERANCIA_UNIFORME_R2.json",
 "PEDRA.TheTimeIsNotAPost.lean": W + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean",
 "PEDRA.TheTimeIsNotAPost.olean": W + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.olean",
 "PEDRA.RESULTADO_PEDRA_R2.json": W + r"\5_R2\1_PEDRA\RESULTADO_PEDRA_R2.json",
 "PEDRA.MANIFESTO_1_PEDRA.json": W + r"\5_R2\1_PEDRA\MANIFESTO_1_PEDRA.json",
 "PEDRA.DIFF.patch": W + r"\5_R2\1_PEDRA\saidas\DIFF.patch",
 "PEDRA.TABELA_DECLARACOES_R2.md": W + r"\5_R2\1_PEDRA\saidas\TABELA_DECLARACOES_R2.md",
 "PEDRA.CONFERENCIA_ASPAS_PEDRA_R2.json": W + r"\5_R2\1_PEDRA\saidas\CONFERENCIA_ASPAS_PEDRA_R2.json",
 "PEDRA.AuditTiposR2.lean": W + r"\5_R2\1_PEDRA\sandbox\AuditTiposR2.lean",
 "PEDRA.T01_R2_TheTimeIsNotAPost.lean": W + r"\5_R2\1_PEDRA\tentativas\T01_R2_TheTimeIsNotAPost.lean",
 "PEDRA.R2_T02_saida.txt": W + r"\5_R2\1_PEDRA\logs\R2_T02_saida.txt",
 "PEDRA.LIMPEZA_RECIBO.json": W + r"\5_R2\1_PEDRA\saidas\LIMPEZA_RECIBO.json",
 "REENSAIO.RESULTADO_REENSAIO_R2.json": W + r"\5_R2\2_REENSAIO\RESULTADO_REENSAIO_R2.json",
 "REENSAIO.RECIBO_REENSAIO_R2.json": W + r"\5_R2\2_REENSAIO\RECIBO_REENSAIO_R2.json",
 "REENSAIO.reensaio_r2.py": W + r"\5_R2\2_REENSAIO\reensaio_r2.py",
 "REENSAIO.reensaio_r2.log": W + r"\5_R2\2_REENSAIO\reensaio_r2.log",
 "REENSAIO.T9c_float_E2_por_k.tsv": W + r"\5_R2\2_REENSAIO\T9c_float_E2_por_k.tsv",
 "REENSAIO.V4.RESULTADO_OPTICO.json": W + r"\5_R2\2_REENSAIO\2_OPTICO\RESULTADO_OPTICO.json",
 "REENSAIO.RECHECK_INDEPENDENTE_13out.json": W + r"\5_R2\2_REENSAIO\CONTINUACAO_13out\RECHECK_INDEPENDENTE_13out.json",
 "REENSAIO.RECIBO_CONTINUACAO_13out.json": W + r"\5_R2\2_REENSAIO\CONTINUACAO_13out\RECIBO_CONTINUACAO_13out.json",
 "AUD_REPRO.RELATORIO_AUD_REPRO_R2.md": W + r"\5_R2\3_AUD_REPRO\RELATORIO_AUD_REPRO_R2.md",
 "AUD_REPRO.RESULTADO_AUD_REPRO_R2.json": W + r"\5_R2\3_AUD_REPRO\RESULTADO_AUD_REPRO_R2.json",
 "AUD_REPRO.MANIFESTO_3_AUD_REPRO.json": W + r"\5_R2\3_AUD_REPRO\MANIFESTO_3_AUD_REPRO.json",
 "AUD_REPRO.sandbox.TheTimeIsNotAPost.olean (recompilado)": W + r"\5_R2\3_AUD_REPRO\sandbox\TheTimeIsNotAPost.olean",
 "AUD_REPRO.AuditTiposAud.lean": W + r"\5_R2\3_AUD_REPRO\sandbox\AuditTiposAud.lean",
 "AUD_REPRO.ProbesAud.lean": W + r"\5_R2\3_AUD_REPRO\sandbox\ProbesAud.lean",
 "AUD_REPRO.RECOMPUTO_INDEPENDENTE_AUD.json": W + r"\5_R2\3_AUD_REPRO\saidas\RECOMPUTO_INDEPENDENTE_AUD.json",
 "AUD_REPRO.COMPARACAO_REENSAIO_COPIA.json": W + r"\5_R2\3_AUD_REPRO\saidas\COMPARACAO_REENSAIO_COPIA.json",
 "AUD_ESTATUTO.RELATORIO_AUD_ESTATUTO_R2.md": W + r"\5_R2\3_AUD_ESTATUTO\RELATORIO_AUD_ESTATUTO_R2.md",
 "AUD_ESTATUTO.ACHADOS_AUD_ESTATUTO_R2.json": W + r"\5_R2\3_AUD_ESTATUTO\ACHADOS_AUD_ESTATUTO_R2.json",
 "AUD_ESTATUTO.MANIFESTO_3_AUD_ESTATUTO.json": W + r"\5_R2\3_AUD_ESTATUTO\MANIFESTO_3_AUD_ESTATUTO.json",
 "AUD_ESTATUTO.sandbox.TheTimeIsNotAPost.olean (recompilado)": W + r"\5_R2\3_AUD_ESTATUTO\sandbox\TheTimeIsNotAPost.olean",
 "AUD_ESTATUTO.AudEstatutoR2.lean": W + r"\5_R2\3_AUD_ESTATUTO\sandbox\AudEstatutoR2.lean",
 "AUD_ESTATUTO.RECOMPUTO_OTICO_AUDITOR.json": W + r"\5_R2\3_AUD_ESTATUTO\saidas\RECOMPUTO_OTICO_AUDITOR.json",
 "AUD_ESTATUTO.VARREDURA_PALAVRAS_R2_AUDITOR.json": W + r"\5_R2\3_AUD_ESTATUTO\saidas\VARREDURA_PALAVRAS_R2_AUDITOR.json",
 "VERBATIM.12out_rank_e_tempo_santo": C + r"\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "VERBATIM.12out_ordem_v392_quatro_linguas": C + r"\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
 "VERBATIM.10out_posto_rank": C + r"\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
 "VERBATIM.05out_VERBO": C + r"\cadeia_de_selo\v386\VERBO_operador_05out.txt",
 "VERBATIM.05out_RESPOSTAS": C + r"\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt",
 "VERBATIM.11out_frequencia_defasa_transmitir": C + r"\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
 "MEMORIA.pergunta-nas-quatro-linguas.md": r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\pergunta-nas-quatro-linguas.md",
 "um.py v391 (nao executado)": UMPY,
}
res = {}
for k, p in ART.items():
    if os.path.exists(p):
        h, n = sha(p)
        res[k] = {"arquivo": p, "sha256": h, "bytes": n,
                  "mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(p)))}
    else:
        res[k] = {"arquivo": p, "AUSENTE": True}


def conferir_freeze(fz, base):
    d = json.load(open(fz, encoding="utf-8"))
    out = {"n": 0, "ok": 0, "falhas": []}
    itens = []
    for key in ("adendo_json", "adendo_md", "preregistro_json", "preregistro_md"):
        if isinstance(d.get(key), dict) and "sha256" in d[key]:
            p = d[key].get("arquivo") or os.path.join(base, d[key].get("caminho", "").replace("/", "\\"))
            itens.append((p, d[key]["sha256"], d[key].get("bytes")))
    for a in d.get("anexos", []):
        p = a.get("arquivo") or os.path.join(base, a["caminho"].replace("/", "\\"))
        itens.append((p, a["sha256"], a.get("bytes")))
    for p, h, n in itens:
        out["n"] += 1
        if os.path.exists(p):
            hh, nn = sha(p)
            if hh == h and (n is None or nn == n):
                out["ok"] += 1
            else:
                out["falhas"].append({"arquivo": p, "esperado": h, "medido": hh})
        else:
            out["falhas"].append({"arquivo": p, "AUSENTE": True})
    out["sha256_do_freeze"] = sha(fz)[0]
    out["congelado_em_utc"] = d.get("congelado_em_utc")
    out["chaves_do_freeze"] = sorted(d.keys())
    return out


fr1 = conferir_freeze(ART["R1.FREEZE"], W + r"\1_PREREGISTRO")
fr2 = conferir_freeze(ART["ADENDO.FREEZE_R2.json"], W + r"\5_R2\0_ADENDO")

src = open(UMPY, "rb").read()
lines = src.split(b"\n")
l95 = lines[94].decode("utf-8", "replace")
l5557 = lines[5556].decode("utf-8", "replace")
m95 = re.search(r"SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", l95)
m5557 = re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l5557)
lit95, lit5557 = m95.group(1), m5557.group(1)
alpha = float(lit5557)
ONE = 1.0
beta = alpha * ONE * math.sqrt(math.e)
ini = next(i + 1 for i, l in enumerate(lines) if l.startswith(b"_NIVEL2_MCMC_FILES"))
beta_out = {
 "estatuto": "[DERIVED: lido nos bytes do um.py e calculado em runtime; nunca medido]",
 "um_py": {"arquivo": UMPY, "sha256": res["um.py v391 (nao executado)"]["sha256"],
           "bytes": res["um.py v391 (nao executado)"]["bytes"], "executado": False},
 "l95": l95.strip(), "l5557": l5557.strip(), "literal_l95": lit95, "literal_l5557": lit5557,
 "literais_iguais": lit95 == lit5557,
 "l5557_embutida_em": "_NIVEL2_MCMC_FILES (abre na l.%d)" % ini,
 "alpha": alpha, "ONE": ONE, "beta_eq_alpha_ONE_sqrt_e": beta, "beta_hex": beta.hex(), "beta_repr": repr(beta),
}
json.dump({"gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"), "artefatos": res, "freeze_R1": fr1, "freeze_R2": fr2},
          open(os.path.join(OUT, "HASHES_RELATORIO_R2.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(beta_out, open(os.path.join(OUT, "BETA_RUNTIME_RELATORIO_R2.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
for k, v in res.items():
    print("%-72s %s  %s" % (k, v.get("sha256", "AUSENTE")[:16], v.get("bytes", "")))
print("FREEZE R1:", json.dumps(fr1, ensure_ascii=False))
print("FREEZE R2:", json.dumps(fr2, ensure_ascii=False))
print("BETA:", json.dumps(beta_out, ensure_ascii=False))
