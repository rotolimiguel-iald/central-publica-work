import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
p = "pilar_quantico_worker.py"
s = open(p, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:80])
    s = s.replace(old, new)
# 1. identidades: PSD/SS_RES/SPOHN so em UNIQUE; NONRETURN
rep('''    v = []
    if rec.get("status") == "DEGENERATE":
        return v
    if "choi_min" in rec and rec["choi_min"] < -tol["cp"]:
        v.append("CP")
    if "tp_res" in rec and rec["tp_res"] > tol["tp"]:
        v.append("TP")
    if rec.get("ss_min_eig", 0.0) < -tol["psd"]:
        v.append("PSD")
    if rec.get("ss_res_rel", 0.0) > tol["ss_res"]:
        v.append("SS_RES")
    sp = rec.get("spohn")
    if sp and sp.get("status") == "OK" and sp.get("violations", 0) > 0:
        v.append("SPOHN")
    return v''',
'''    v = []
    if rec.get("status") == "DEGENERATE":
        return v
    if "choi_min" in rec and rec["choi_min"] < -tol["cp"]:
        v.append("CP")
    if "tp_res" in rec and rec["tp_res"] > tol["tp"]:
        v.append("TP")
    if "choi_min_inverse" in rec and rec["choi_min_inverse"] >= -tol["cp"]:
        v.append("NONRETURN")
    if rec.get("status") != "UNIQUE":
        return v          # PSD, residuo e Spohn so se cobram do atrator UNICO (gap ambiguo nao e' violacao de identidade)
    if rec.get("ss_min_eig", 0.0) < -tol["psd"]:
        v.append("PSD")
    if rec.get("ss_res_rel", 0.0) > tol["ss_res"]:
        v.append("SS_RES")
    sp = rec.get("spohn")
    if sp and sp.get("status") == "OK" and sp.get("violations", 0) > 0:
        v.append("SPOHN")
    return v''')
# 2. T1: so o nivel sem ruido decide
rep('''    t1 = R["T1"]; rec0 = all((s.get("sigma_0.0") or {}).get("pass_frac") == 1.0 for s in t1.values())
    rec8 = all(((s.get("sigma_1e-08") or {}).get("pass_frac") or 0.0) >= spec["T1"]["pass"]["1e-08"]["min_frac"] for s in t1.values())
    root = "RECOVERED" if (rec0 and rec8) else "NOT_RECOVERED"''',
'''    t1 = R["T1"]; rec0 = all((s.get("sigma_0.0") or {}).get("pass_frac") == 1.0 for s in t1.values())
    root = "RECOVERED" if rec0 else "NOT_RECOVERED"      # so o nivel SEM ruido decide; os niveis com ruido sao a curva de resolucao (relatada)''')
# 3. cpuref antes do D128; prazo do D128
rep('''            for ph in ("T3", "T2", "T1", "T4", "D128"):''', '''            for ph in ("T3", "T2", "T1", "T4"):''')
rep('''                    elif ph == "T4":
                        R["T4"] = run_T4(E, spec, prog, det)
                    else:
                        R["D128"] = run_D128(E, spec, beta, prog)''', '''                    else:
                        R["T4"] = run_T4(E, spec, prog, det)''')
rep('''        R["details_sha256"] = sha256_bytes(open(detp, "rb").read())
        R["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")''',
'''        R["details_sha256"] = sha256_bytes(open(detp, "rb").read())
        write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
        # o ponto d = 128 por ultimo, com prazo: se o prazo ja passou, NAO roda (dito no resultado, nunca escondido)
        t0 = time.time()
        if time.time() - prog.t0 <= spec["D128"]["start_deadline_s"]:
            R["D128"] = run_D128(E, spec, beta, prog)
        else:
            R["D128"] = {"ran": False, "error": "DEADLINE: o prazo de inicio (%d s) ja tinha passado" % spec["D128"]["start_deadline_s"]}
        R["phase_seconds"]["D128"] = round(time.time() - t0, 1)
        R["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")''')
ast.parse(s)
open(p + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s)
import os; os.replace(p + ".tmp", p); print("ok")
