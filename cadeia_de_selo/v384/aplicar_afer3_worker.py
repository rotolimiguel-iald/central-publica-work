# -*- coding: utf-8 -*-
"""As correcoes da 3a afericao no TRABALHADOR (o hash muda; a especificacao e as sondas de tempo e do motor sao refeitas depois):
ParentGone herda de BaseException (os except Exception das fases, das instancias e do D128 nao o engolem); a espera pela CPU em fatias, conferindo o pai;
o RK4 do D128 confere o pai; o filho da CPU recebe --parent-pid e confere o trabalhador; o del J, K volta ao bloco das conferencias; as docstrings do
gerador e do classificador; o modo zero tambem no D128; a escrita final do progresso com guarda; a CPU sem ponto comparavel ganha estado proprio;
n(c2) so como informacao; E8 = o autoteste do comparador; a contagem das estimativas nao finitas no T1. Backup de bytes antes; LF; ast."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pilar_quantico_worker.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert b"\r" not in raw
bak = os.path.join(HERE, "pilar_quantico_worker_auditado_3a_passada.py")
if not os.path.exists(bak):
    open(bak, "wb").write(raw)
assert open(bak, "rb").read() == raw, "o backup da 3a passada nao e' o estado corrente"
PAIRS = []
A = lambda old, new: PAIRS.append((old, new))

# 1. ParentGone fora do alcance dos except Exception
A('''class ParentGone(Exception):
    pass''', '''class ParentGone(BaseException):
    """O um.py morreu. Herda de BaseException (como KeyboardInterrupt): os except Exception das fases, das instancias e do D128 NAO o engolem;
    so o handler do main o pega e grava NOT_RUN__PARENT_GONE (3a afericão)."""
    pass''')
A('''    except SystemExit:
        raise
    except Exception as e:
        R["fatal"] = _err(e); R["trace"] = traceback.format_exc()[-3000:]''', '''    except SystemExit:
        raise
    except (Exception, ParentGone) as e:
        R["fatal"] = _err(e); R["trace"] = traceback.format_exc()[-3000:]''')
# 2. a espera pela CPU em fatias, conferindo o pai
A('''        prog.set(phase="cpuref_wait", force=True)
        try:
            child_rc = cpu_proc.wait(timeout=spec["cpuref"]["timeout_s"])
        except Exception:
            cpu_proc.kill(); child_rc = None''', '''        prog.set(phase="cpuref_wait", force=True)
        child_rc = None; t_w = time.time()
        while True:                                      # em fatias de 20 s: o pai e' conferido durante a espera (3a afericao)
            try:
                child_rc = cpu_proc.wait(timeout=20); break
            except subprocess.TimeoutExpired:
                prog.set(phase="cpuref_wait", force=True)      # levanta ParentGone se o um.py morreu
                if time.time() - t_w > spec["cpuref"]["timeout_s"]:
                    cpu_proc.kill(); child_rc = None; break''')
# 3. o filho da CPU confere o trabalhador
A('''        cpu_proc = subprocess.Popen([sys.executable, me, "--mode", "cpuref", "--spec", args.spec, "--spec-sha256", R["spec_sha256"], "--beta-hex", args.beta_hex,
                                     "--run-id", args.run_id, "--out", args.out], stdout=subprocess.DEVNULL, stderr=cpu_err, creationflags=_below_normal_flags())''',
  '''        cpu_proc = subprocess.Popen([sys.executable, me, "--mode", "cpuref", "--spec", args.spec, "--spec-sha256", R["spec_sha256"], "--beta-hex", args.beta_hex,
                                     "--run-id", args.run_id, "--parent-pid", str(os.getpid()), "--out", args.out],
                                    stdout=subprocess.DEVNULL, stderr=cpu_err, creationflags=_below_normal_flags())   # o filho confere o trabalhador (3a afericao)''')
A('''        if args.mode == "cpuref":
            run_cpuref(spec, beta, args.out, meta); return''', '''        if args.mode == "cpuref":
            run_cpuref(spec, beta, args.out, meta, parent_pid=args.parent_pid); return''')
A('''def run_cpuref(spec, beta, outdir, meta):
    import scipy.linalg as sl
    s2 = spec["T2"]; tol = spec["tolerances"]; op = spec["operators"]; out = {}
    t0 = time.time()
    for (d, nc, gi) in cpuref_items(spec):''', '''def run_cpuref(spec, beta, outdir, meta, parent_pid=None):
    import scipy.linalg as sl
    s2 = spec["T2"]; tol = spec["tolerances"]; op = spec["operators"]; out = {}
    t0 = time.time()
    for (d, nc, gi) in cpuref_items(spec):
        if not parent_alive(parent_pid):                # o trabalhador morreu (por exemplo, queda nativa): o filho nao fica orfao (3a afericao)
            raise ParentGone("o trabalhador %s nao vive mais" % parent_pid)''')
# 4. o RK4 do D128 confere o pai; o modo zero no D128
A('''        cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); out.update({k2: cl[k2] for k2 in ("status", "n0", "gap", "gap_rel", "scale", "max_re")})
        if cl["status"] != "DEGENERATE":
            prog.set(phase="D128", step="steady_state", force=True)''', '''        cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); out.update({k2: cl[k2] for k2 in ("status", "n0", "gap", "gap_rel", "scale", "max_re")})
        out["zero_mode_ok"] = bool(cl["n0"] >= 1)      # a IDENTIDADE do modo zero tambem em d = 128 (tr . S = 0 garante um zero; 3a afericao)
        if cl["status"] != "DEGENERATE":
            prog.set(phase="D128", step="steady_state", force=True)''')
A('''            for s in range(sd["rk4_steps"] + 1):
                Dn = []''', '''            for s in range(sd["rk4_steps"] + 1):
                if s % 50 == 0:
                    prog.set(phase="D128", step="spohn_rk4", rk4_step=s)   # confere o pai a cada 20 s no maximo (3a afericao)
                Dn = []''')
A('''    nv += sum(int(not (r.get("N2_unital_identity") or {}).get("identity_ok")) for dk, r in t3.items() if dk.startswith("d"))''',
  '''    nv += sum(int(not (r.get("N2_unital_identity") or {}).get("identity_ok")) for dk, r in t3.items() if dk.startswith("d"))
    nv += int(bool((R.get("D128") or {}).get("ran")) and (R.get("D128") or {}).get("zero_mode_ok") is False)   # o modo zero em d = 128''')
# 5. as docstrings e o del J, K
A('''        """L^ = log(Phi)/tau pelo logaritmo principal (Phi = V diag(lambda) V^-1); devolve a diagonal de L^ e duas conferencias do ramo:
        tau*||(L^ - L^dag)/2i|| < pi (o espectro de tau*L^ cabe na faixa principal) e o menor autovalor da Choi PROJETADA de L^ (Kossakowski >= 0:
        L^ e' um gerador de Lindblad legitimo; um logaritmo enrolado em geral nao e')."""''', '''        """L^ = log(Phi)/tau pelo logaritmo principal (Phi = V diag(lambda) V^-1); devolve a diagonal de L^ e:
        tau_antiherm_norm = tau*||(L^ - L^dag)/2i|| -- so INFORMACAO (mede a imagem numerica, nao certifica o ramo);
        ccp_min_rel = o menor autovalor da Choi PROJETADA de L^ relativo ao maior |autovalor| -- LEGITIMIDADE (Kossakowski >= 0: L^ e' um gerador de Lindblad);
        gen_rel_dev = ||L^ - S||_F/||S||_F, so quando o ARNES passa o gerador verdadeiro S_true (injecao; o estimador nunca o ve) -- o CERTIFICADO do
        ramo principal, a posteriori."""''')
A('''            info["ccp_min_rel"] = float(wk.min().item()) / mx if mx > 0 else 0.0
        if S_true is not None:
            # o certificado do ramo pelo ARNES (que conhece o gerador verdadeiro): o logaritmo principal reproduziu S?
            info["gen_rel_dev"] = float((t.linalg.vector_norm(Lh - S_true) / t.linalg.vector_norm(S_true)).item())
            del J, K''', '''            info["ccp_min_rel"] = float(wk.min().item()) / mx if mx > 0 else 0.0
            del J, K
        if S_true is not None:
            # o certificado do ramo pelo ARNES (que conhece o gerador verdadeiro): o logaritmo principal reproduziu S?
            info["gen_rel_dev"] = float((t.linalg.vector_norm(Lh - S_true) / t.linalg.vector_norm(S_true)).item())''')
A('''        # sigma = 0: o certificado a priori E a Choi projetada >= -tol (L^ e' Lindblad legitimo); sigma > 0: so o certificado -- a Choi projetada recebe o ruido
        # no seu nucleo enorme (autovalores ~ -sigma d/tau) e vira so informacao (achado 19 da 2a passada)''',
  '''        # sigma = 0: o certificado a posteriori (gen_rel_dev contra o S verdadeiro, que so o arnes conhece) E a Choi projetada >= -tol (L^ e' Lindblad legitimo);
        # sigma > 0: so o certificado -- a Choi projetada recebe o ruido no seu nucleo enorme (autovalores ~ -sigma d/tau) e vira so informacao (achado 1 da 2a passada)''')
A('''        """UNIQUE: exatamente um autovalor com |lambda| <= tol0_rel*escala e todos os outros com -Re lambda >= gap_rel*escala;
        DEGENERATE: dois ou mais no zero; AMBIGUOUS: o resto (um no zero, mas espectro periferico/proximo do eixo)."""''',
  '''        """UNIQUE: exatamente um autovalor com |lambda| <= tol0_rel*escala e todos os outros com -Re lambda >= gap_rel*escala;
        DEGENERATE: dois ou mais no zero; AMBIGUOUS: o resto -- um no zero com espectro proximo do eixo, OU nenhum no zero (n0 = 0), e este ultimo
        e' VIOLACAO da identidade do modo zero (identity_check e o D128), nunca so «ambiguo»."""''')
# 6. a escrita final do progresso com guarda (nao pode reescrever um resultado completo como fatal)
A('''        write_result(rp, R)
        prog.state["phase"] = "done"; write_json_atomic(prog.p, prog.state)''', '''        write_result(rp, R)
        try:                                             # a marca final do progresso NAO pode rebaixar um resultado completo (3a afericao)
            prog.state["phase"] = "done"; write_json_atomic(prog.p, prog.state)
        except Exception:
            pass''')
# 7. o comparador: a CPU sem ponto comparavel; n(c2) so como informacao (as chaves comparadas sao as do spec.cpuref.tol)
A('''        for k_, v_ in dd.items():
            maxd[k_] = max(maxd[k_], v_)
        if any(dd[k_] > tol[k_] for k_ in dd):
            bad.append((key, "TOL"))
    return {"compared": n, "near_threshold_not_compared": near, "disagreements": len(bad), "first_disagreements": bad[:10], "max_diffs": maxd, "meta_ok": meta_ok,
            "child_rc": child_rc, "ok": bool(n > near and not bad and meta_ok and child_rc == 0)}''', '''        for k_, v_ in dd.items():
            maxd[k_] = max(maxd[k_], v_)
        if any(dd[k_] > tol[k_] for k_ in dd if k_ in tol):     # so as chaves com tolerancia no spec decidem; n(c2) e' INFORMACAO (3a afericao)
            bad.append((key, "TOL"))
    return {"read": n, "compared": n - near, "near_threshold_not_compared": near, "not_comparable": bool(n > 0 and n == near), "disagreements": len(bad),
            "first_disagreements": bad[:10], "max_diffs": maxd, "informative_only": sorted(k_ for k_ in maxd if k_ not in tol), "meta_ok": meta_ok,
            "child_rc": child_rc, "ok": bool(n > near and not bad and meta_ok and child_rc == 0)}''')
A('''    if not (R.get("cpuref_compare") or {}).get("ok"):
        return P + "CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED"''', '''    if not (R.get("cpuref_compare") or {}).get("ok"):
        if (R.get("cpuref_compare") or {}).get("not_comparable"):
            return P + "CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__GATE_UNTOUCHED"     # nenhum ponto longe do limiar: nao houve discordancia, nem conferencia
        return P + "CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED"''')
# 8. E8: o autoteste do comparador (entradas sinteticas; nenhum operador da teoria)
A('''    # E7 o PISO do estimador (achado 1 do aferidor): maximo <= criterio/10, inclusive com k quase iguais
    fl = estimator_floor(seed, crit_beta, crit_p)
    out.append(("E7_estimator_floor_below_one_tenth_of_the_criterion", fl["ok"], fl))''', '''    # E7 o PISO do estimador (achado 1 do aferidor): maximo <= criterio/10, inclusive com k quase iguais
    fl = estimator_floor(seed, crit_beta, crit_p)
    out.append(("E7_estimator_floor_below_one_tenth_of_the_criterion", fl["ok"], fl))
    # E8 o COMPARADOR da referencia na CPU, com linhas sinteticas (3a afericao): igual -> concorda; CCI fora da tolerancia -> discorda; so n(c2) diferente ->
    # concorda (informacao); tudo perto do limiar -> nao comparavel; marca da rodada errada -> recusa
    ct = cpu_tol or {"cci": 1e-9, "purity": 1e-9, "folds_n_c1": 1e-9, "gap_rel_rel": 1e-6, "choi_min": 1e-9, "min_gap_rel_for_compare": 1e-6}
    sp8 = {"cpuref": {"tol": ct}}; me8 = {"run_id": "e8", "spec_sha256": "x", "beta_hex": "0x1p-7", "worker_sha256": "w"}
    g8 = {"status": "UNIQUE", "gap_rel": 1e-3, "cci": 0.5, "purity": 0.4, "folds": [{"n": 2.9}, {"n": 2.1}], "choi_min": 0.0}
    c8 = {"status": "UNIQUE", "gap_rel": 1e-3, "cci": 0.5, "purity": 0.4, "folds_n_c1": 2.9, "folds_n_c2": 2.1, "choi_min": 0.0}
    cpu8 = lambda items, meta=me8: dict(meta, items=items)
    r_eq = compare_cpuref(sp8, {"a": g8, "b": g8}, cpu8({"a": c8, "b": c8}), me8, 0)
    r_cc = compare_cpuref(sp8, {"a": g8, "b": g8}, cpu8({"a": c8, "b": dict(c8, cci=0.5 + 1e-6)}), me8, 0)
    r_n2 = compare_cpuref(sp8, {"a": g8}, cpu8({"a": dict(c8, folds_n_c2=2.1 + 1e-5)}), me8, 0)
    r_nr = compare_cpuref(sp8, {"a": dict(g8, gap_rel=1e-8)}, cpu8({"a": dict(c8, gap_rel=1e-8)}), me8, 0)
    r_mt = compare_cpuref(sp8, {"a": g8}, cpu8({"a": c8}, dict(me8, run_id="outra")), me8, 0)
    ok = bool(r_eq["ok"] and r_eq["compared"] == 2 and not r_cc["ok"] and r_cc["disagreements"] == 1 and r_n2["ok"] and not r_nr["ok"] and r_nr["not_comparable"]
              and not r_mt["ok"])
    out.append(("E8_cpu_reference_comparator_selftest", ok, {"equal": r_eq["ok"], "cci_off": r_cc["ok"], "nc2_only_off": r_n2["ok"], "all_near_threshold_not_comparable": r_nr["not_comparable"],
                                                             "wrong_run_id": r_mt["ok"]}))''')
A('''def engine_selftest(E, tol, crit_beta=1e-6, crit_p=1e-4, seed=20261003):''', '''def engine_selftest(E, tol, crit_beta=1e-6, crit_p=1e-4, seed=20261003, cpu_tol=None):''')
A('''        R["engine_selftest"] = engine_selftest(E, (spec or {}).get("tolerances", {}).get("engine", 1e-9), crit["beta_rel"], crit["p_abs"], (spec or {}).get("seed", 20261003))''',
  '''        R["engine_selftest"] = engine_selftest(E, (spec or {}).get("tolerances", {}).get("engine", 1e-9), crit["beta_rel"], crit["p_abs"], (spec or {}).get("seed", 20261003),
                                               (((spec or {}).get("cpuref") or {}).get("tol")))''')
# 9. o T1: quantas estimativas nao tiveram solucao finita, por nivel
A('''            "branch_ok_frac": float(np.mean(br)) if br.size else None, "pass_frac": ok_frac, "required_frac": (crit or {}).get("min_frac"),''',
  '''            "branch_ok_frac": float(np.mean(br)) if br.size else None, "pass_frac": ok_frac, "required_frac": (crit or {}).get("min_frac"),
            "n_nonfinite_beta": int(np.sum(~np.isfinite(be))) if be.size else 0,''')

for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
s = s.replace("afericão", "afericao")
ast.parse(s)
b = s.encode("utf-8"); assert b"\r" not in b
tmp = P + ".tmp"
open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, P)
print("ok", len(PAIRS), "trocas; sha16", hashlib.sha256(b).hexdigest()[:16], "(antes", hashlib.sha256(raw).hexdigest()[:16] + ")")
