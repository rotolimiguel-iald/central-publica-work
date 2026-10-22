import hashlib, json, os, sys
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
files = {
 "operador": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "prereg_json": W + r"\1_PREREGISTRO\PREREGISTRO.json",
 "prereg_md": W + r"\1_PREREGISTRO\PREREGISTRO.md",
 "freeze": W + r"\1_PREREGISTRO\FREEZE.json",
 "levantamento_md": W + r"\0_LEVANTAMENTO\LEVANTAMENTO.md",
 "definicoes": W + r"\0_LEVANTAMENTO\DEFINICOES.json",
 "res_opt_r1": W + r"\2_OPTICO\RESULTADO_OPTICO.json",
 "res_opt_r2": W + r"\2_OPTICO\rodada_2\RESULTADO_OPTICO.json",
 "run_opt_r2": W + r"\2_OPTICO\rodada_2\run_optico.py",
 "res_ker_r1": W + r"\3_KERNEL\RESULTADO_KERNEL.json",
 "res_ker_r2": W + r"\3_KERNEL\rodada_2\RESULTADO_KERNEL.json",
 "pedra_r2": W + r"\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.lean",
 "olean_r2": W + r"\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.olean",
 "pedra_r1": W + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean",
 "adendo_r2_json": W + r"\5_R2\0_ADENDO\ADENDO_R2.json",
 "adendo_r2_md": W + r"\5_R2\0_ADENDO\ADENDO_R2.md",
 "freeze_r2": W + r"\5_R2\0_ADENDO\FREEZE_R2.json",
 "relatorio_final_r1": W + r"\4_RELATORIO\RELATORIO_FINAL.md",
 "um_py": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
}
out = {}
for k, p in files.items():
    try:
        b = open(p, "rb").read()
        out[k] = {"path": p, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "crlf": b.count(b"\r\n")}
    except Exception as e:
        out[k] = {"path": p, "erro": repr(e)}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(k, v.get("bytes"), (v.get("sha256") or v.get("erro"))[:64], v.get("crlf"))
