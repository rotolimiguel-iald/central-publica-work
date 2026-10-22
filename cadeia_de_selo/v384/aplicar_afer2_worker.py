# -*- coding: utf-8 -*-
"""As correcoes da 2a passada (workflow de 5 lentes, 48 achados sobreviventes) NO TRABALHADOR, por trocas com contagem conferida."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pilar_quantico_worker.py")
s = open(P, encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:120])
    s = s.replace(old, new)


# (a) write_json_atomic sempre com o .sha256 ao lado quando for o resultado (achado: saida precoce sem sha ganhava CUSTODY_CHAIN_INCOMPLETE)
rep('''class Progress:''', '''def write_result(path, obj):
    """O resultado (result.json ou cpuref*.json) com o seu .sha256 ao lado -- em TODA saida, inclusive recusa e falha fatal."""
    write_json_atomic(path, obj)
    b = open(path, "rb").read()
    with open(path + ".sha256.tmp", "w", encoding="ascii") as fh:
        fh.write(sha256_bytes(b))
    os.replace(path + ".sha256.tmp", path + ".sha256")


def parent_alive(pid):
    """O processo pai (o um.py) ainda vive? No Windows por OpenProcess/GetExitCodeProcess (os.kill la' MATARIA); fora dele, os.kill(pid, 0)."""
    if not pid:
        return True
    try:
        if os.name == "nt":
            import ctypes
            k = ctypes.windll.kernel32
            h = k.OpenProcess(0x1000, False, int(pid))      # PROCESS_QUERY_LIMITED_INFORMATION
            if not h:
                return False
            code = ctypes.c_ulong()
            ok = k.GetExitCodeProcess(h, ctypes.byref(code)); k.CloseHandle(h)
            return bool(ok) and code.value == 259          # STILL_ACTIVE
        os.kill(int(pid), 0)
        return True
    except Exception:
        return False


class ParentGone(Exception):
    pass


class Progress:''')
rep('''    def __init__(self, outdir, run_id=None):
        self.p = os.path.join(outdir, "progress.json") if outdir else None
        self.t0 = time.time(); self.last = 0.0; self.state = {"run_id": run_id}

    def set(self, force=False, **kw):
        self.state.update(kw)
        now = time.time()
        if self.p and (force or now - self.last >= 20.0):''', '''    def __init__(self, outdir, run_id=None, parent_pid=None):
        self.p = os.path.join(outdir, "progress.json") if outdir else None
        self.t0 = time.time(); self.last = 0.0; self.state = {"run_id": run_id}; self.parent_pid = parent_pid

    def set(self, force=False, **kw):
        self.state.update(kw)
        now = time.time()
        if self.p and (force or now - self.last >= 20.0):
            if not parent_alive(self.parent_pid):        # o um.py morreu: o trabalhador nao fica orfao na GPU (achado da 2a passada)
                raise ParentGone("o processo pai %s nao vive mais" % self.parent_pid)''')
# (b) a docstring do estimador (achado: a formula de beta^ estava errada no texto; o codigo estava certo)
rep('''parava em ~sqrt(eps)/curvatura -- achado 1 do aferidor). beta^ = lambda_1 |v|^2/gamma ... com |v| = exp(-intercepto)."""''',
    '''parava em ~sqrt(eps)/curvatura -- achado 1 do aferidor). beta^ = lambda_1/(gamma |v|^2) = lambda_1 e^{2c}/gamma, com |v| = e^{-c} (c = o intercepto)."""''')
# (c) identidade: espectro SEM autovalor nulo e' falha do motor (todo gerador que preserva o traco tem 0)
rep('''    v, c = [], []
    if rec.get("status") == "DEGENERATE":
        return v, c''', '''    v, c = [], []
    if rec.get("status") == "DEGENERATE":
        return v, c
    c.append("ZERO_MODE")
    if rec.get("n0", 1) == 0:
        v.append("ZERO_MODE")                            # tr . S = 0 garante um zero: nao acha-lo e' o motor errando, nao «ambiguo»''')
rep('''IDENTITIES = ("CP", "TP", "NONRETURN", "PSD", "SS_RES", "SPOHN")''', '''IDENTITIES = ("ZERO_MODE", "CP", "TP", "NONRETURN", "PSD", "SS_RES", "SPOHN")''')
rep('''            if set(c) >= {"CP", "TP", "PSD", "SS_RES", "SPOHN"}:''', '''            if set(c) >= {"ZERO_MODE", "CP", "TP", "PSD", "SS_RES", "SPOHN"}:''')
# (d) o ramo do log: CERTIFICADO A PRIORI pelo gerador verdadeiro (o arnes conhece H e os saltos; o estimador nao) + Kossakowski como consistencia so em sigma = 0
rep('''    S = E.superop(E.T(H), [E.T(L) for L in Ls.values()])
    Phi = E.propagator(S, s1["tau"]); del S
    Cc = np.eye(d) - np.ones((d, d)) / d
    out = []''', '''    S = E.superop(E.T(H), [E.T(L) for L in Ls.values()])
    Phi = E.propagator(S, s1["tau"]); del S
    # o CERTIFICADO A PRIORI do ramo (o arnes, nao o estimador): |Im lambda(L)| <= (E_max - E_min) + 2 sum ||L_k||^2 (faixa numerica); se tau vezes isto < pi, o
    # logaritmo principal de Phi E' tau*L -- certificado, nao condicao necessaria (achado 20 da 2a passada)
    eH = np.linalg.eigvalsh((H + H.conj().T) / 2)
    bound = float(eH.max() - eH.min()) + 2.0 * sum(float(np.linalg.norm(L, 2)) ** 2 for L in Ls.values())
    apriori_ok = bool(s1["tau"] * bound < math.pi - s1["branch_margin"])
    Cc = np.eye(d) - np.ones((d, d)) / d
    out = []''')
rep('''        branch_ok = bool(inf["tau_antiherm_norm"] < math.pi - s1["branch_margin"] and inf["ccp_min_rel"] >= -tol["ccp_rel"])''',
    '''        # sigma = 0: o certificado a priori E a Choi projetada >= -tol (L^ e' Lindblad legitimo); sigma > 0: so o certificado -- a Choi projetada recebe o ruido
        # no seu nucleo enorme (autovalores ~ -sigma d/tau) e vira so informacao (achado 19 da 2a passada)
        branch_ok = bool(apriori_ok and (inf["ccp_min_rel"] >= -tol["ccp_rel"] if sigma == 0 else True))''')
rep('''                    "p_hat": fr["p_hat"], "misfit": fr["misfit"], "rank_ratio": fr["rank_ratio"], "branch_ok": branch_ok, **inf})''',
    '''                    "p_hat": fr["p_hat"], "misfit": fr["misfit"], "rank_ratio": fr["rank_ratio"], "branch_ok": branch_ok, "tau_apriori_bound": s1["tau"] * bound, **inf})''')
# (e) a referencia na CPU: comparacao numerica so onde as duas sao UNICAS com gap folgado (perto do limiar, duas bibliotecas corretas discordam; achado 8)
rep('''    for key, c in (cpu.get("items") or {}).items():
        g = gpu_rows.get(key)
        if g is None:
            bad.append((key, "GPU_ROW_MISSING")); continue
        n += 1
        if g["status"] != c["status"]:
            bad.append((key, "STATUS %s != %s" % (g["status"], c["status"]))); continue
        if c["status"] == "DEGENERATE":
            continue''', '''    gmin = tol["min_gap_rel_for_compare"]; near = 0
    for key, c in (cpu.get("items") or {}).items():
        g = gpu_rows.get(key)
        if g is None:
            bad.append((key, "GPU_ROW_MISSING")); continue
        n += 1
        if min(float(g.get("gap_rel") or 0.0), float(c.get("gap_rel") or 0.0)) < gmin:
            near += 1; continue                          # perto do limiar: relatado, nao comparado (o status pode virar entre bibliotecas corretas)
        if g["status"] != c["status"]:
            bad.append((key, "STATUS %s != %s" % (g["status"], c["status"]))); continue
        if c["status"] != "UNIQUE":
            continue''')
rep('''    return {"compared": n, "disagreements": len(bad), "first_disagreements": bad[:10], "max_diffs": maxd, "meta_ok": meta_ok, "child_rc": child_rc,
            "ok": bool(n > 0 and not bad and meta_ok and child_rc == 0)}''', '''    return {"compared": n, "near_threshold_not_compared": near, "disagreements": len(bad), "first_disagreements": bad[:10], "max_diffs": maxd, "meta_ok": meta_ok,
            "child_rc": child_rc, "ok": bool(n > near and not bad and meta_ok and child_rc == 0)}''')
# (f) a arvore: ramo proprio para a falha fatal (achado 5)
rep('''    P = "TGL_QUANTUM_PILLAR_V1__"
    if R.get("refused"):''', '''    P = "TGL_QUANTUM_PILLAR_V1__"
    if R.get("fatal"):
        return P + "NOT_RUN__WORKER_FATAL__GATE_UNTOUCHED"
    if R.get("refused"):''')
# (g) toda gravacao do resultado com o .sha256; a falha fatal e o pai morto encerram o filho da CPU
for old in ('''R["verdict"] = "TGL_QUANTUM_PILLAR_V1__NOT_RUN__MISSING_ARGUMENTS__GATE_UNTOUCHED"; write_json_atomic(rp, R); sys.exit(4)''',
            '''R["refused"] = "SPEC_HASH_MISMATCH"; R["verdict"] = derive_verdict(spec, R); write_json_atomic(rp, R); sys.exit(4)''',
            '''R["refused"] = "WORKER_HASH_MISMATCH"; R["verdict"] = derive_verdict(spec, R); write_json_atomic(rp, R); sys.exit(4)''',
            '''            write_json_atomic(rp, R); sys.exit(6)''',
            '''R["verdict"] = "TGL_QUANTUM_PILLAR_V1__ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED"; write_json_atomic(rp, R); sys.exit(5)''',
            '''R["verdict"] = "ENGINE_SELFTEST_PASSED"; write_json_atomic(rp, R); return''',
            '''R["timing"] = run_timing(E, args.out); write_json_atomic(rp, R); return'''):
    rep(old, old.replace("write_json_atomic(rp, R)", "write_result(rp, R)"))
rep('''        R["verdict"] = derive_verdict(spec, R)
        write_json_atomic(rp, R)
        b = open(rp, "rb").read()
        with open(rp + ".sha256", "w", encoding="ascii") as fh:
            fh.write(sha256_bytes(b))
        prog.set(phase="done", force=True)''', '''        R["verdict"] = derive_verdict(spec, R)
        write_result(rp, R)
        prog.state["phase"] = "done"; write_json_atomic(prog.p, prog.state)''')
rep('''    except Exception as e:
        R["fatal"] = _err(e); R["trace"] = traceback.format_exc()[-3000:]
        R["verdict"] = "TGL_QUANTUM_PILLAR_V1__NOT_RUN__WORKER_FATAL__GATE_UNTOUCHED"
        write_json_atomic(rp, R); sys.exit(1)''', '''    except Exception as e:
        R["fatal"] = _err(e); R["trace"] = traceback.format_exc()[-3000:]
        R["verdict"] = "TGL_QUANTUM_PILLAR_V1__NOT_RUN__" + ("PARENT_GONE" if isinstance(e, ParentGone) else "WORKER_FATAL") + "__GATE_UNTOUCHED"
        try:
            cpu_proc.kill()                              # o filho da CPU nao fica orfao (achado da 2a passada)
        except Exception:
            pass
        write_result(rp, R); sys.exit(1)''')
# o pid do pai: argumento novo; o Progress o vigia
rep('''ap.add_argument("--run-id"); ap.add_argument("--out", required=True)''', '''ap.add_argument("--run-id"); ap.add_argument("--parent-pid", type=int); ap.add_argument("--out", required=True)''')
rep('''    prog = Progress(args.out, args.run_id)''', '''    prog = Progress(args.out, args.run_id, args.parent_pid)
    cpu_proc = None''')
# o modo cpuref grava o seu resultado com sha256; o erro dele vai para cpuref_error.json (rp)
rep('''    write_json_atomic(os.path.join(outdir, "cpuref.json"), res)
    return res''', '''    write_result(os.path.join(outdir, "cpuref.json"), res)
    return res''')
# a falha fatal deriva pela arvore (ramo fatal): rederivacao igual
rep('''        R["verdict"] = "TGL_QUANTUM_PILLAR_V1__NOT_RUN__" + ("PARENT_GONE" if isinstance(e, ParentGone) else "WORKER_FATAL") + "__GATE_UNTOUCHED"''',
    '''        R["parent_gone"] = isinstance(e, ParentGone)
        R["verdict"] = derive_verdict(spec or {}, R)''')
rep('''    if R.get("fatal"):
        return P + "NOT_RUN__WORKER_FATAL__GATE_UNTOUCHED"''', '''    if R.get("fatal"):
        return P + "NOT_RUN__" + ("PARENT_GONE" if R.get("parent_gone") else "WORKER_FATAL") + "__GATE_UNTOUCHED"''')
ast.parse(s)
open(P + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(P + ".tmp", P); print("ok")
