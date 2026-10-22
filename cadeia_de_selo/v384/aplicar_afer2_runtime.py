# -*- coding: utf-8 -*-
"""As correcoes da 2a passada NO MODULO DO um.py (v384_runtime.py), por trocas com contagem conferida."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
s = open(P, encoding="utf-8").read()
open(P + ".bak_antes_afer2", "w", encoding="utf-8", newline="").write(s)


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:120])
    s = s.replace(old, new)


# (1) encerrar a ARVORE do trabalhador (o neto da CPU junto) -- no prazo e no atexit
rep('''def _qp_cache_dir(key):''', '''def _qp_kill_tree(proc):
    """Encerra o trabalhador E o filho da CPU (no Windows, taskkill /T /F; fora, o grupo). Silencioso se ja saiu."""
    try:
        if proc is None or proc.poll() is not None:
            return
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, timeout=60)
        else:
            proc.kill()
        proc.wait(timeout=60)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


_QP_LIVE = {}


def _qp_atexit():
    """Se o um.py sair (excecao, interrupcao) com o trabalhador ainda vivo, a arvore e' encerrada: nada fica orfao na GPU (achado da 2a passada)."""
    st = _QP_LIVE.get("st")
    if st and not st.get("finished") and st.get("proc") is not None:
        _qp_kill_tree(st["proc"])


def _qp_cache_dir(key):''')
rep('''        proc = subprocess.Popen([sys.executable, mat["pilar_quantico_worker.py"]["path"], "--mode", "run", "--spec", mat["pilar_quantico_spec.json"]["path"],
                                 "--spec-sha256", _QP_SPEC_SHA256, "--beta-hex", bhex, "--run-id", run_id, "--out", run_dir],''',
    '''        proc = subprocess.Popen([sys.executable, mat["pilar_quantico_worker.py"]["path"], "--mode", "run", "--spec", mat["pilar_quantico_spec.json"]["path"],
                                 "--spec-sha256", _QP_SPEC_SHA256, "--beta-hex", bhex, "--run-id", run_id, "--parent-pid", str(os.getpid()), "--out", run_dir],''')
rep('''        st.update({"mode": "COMPUTE", "proc": proc, "run_dir": run_dir, "log": logf, "cache_dir": cdir, "run_id": run_id,''',
    '''        import atexit
        _QP_LIVE["st"] = st; atexit.register(_qp_atexit)
        st.update({"mode": "COMPUTE", "proc": proc, "run_dir": run_dir, "log": logf, "cache_dir": cdir, "run_id": run_id,''')
rep('''        if el > st["timeout_s"]:
            proc.kill(); proc.wait(); timed_out = True; rc = None; break''', '''        if el > st["timeout_s"]:
            _qp_kill_tree(proc); timed_out = True; rc = None; break''')
# (2) o cache: troca atomica (o antigo so sai depois de o novo estar no lugar)
rep('''    if os.path.isdir(cdir):
        shutil.rmtree(cdir)
    os.replace(tmp, cdir)
    return cdir''', '''    old = None
    if os.path.isdir(cdir):
        old = cdir + ".old_" + time.strftime("%Y%m%d_%H%M%S")
        os.replace(cdir, old)
    os.replace(tmp, cdir)
    if old:
        shutil.rmtree(old, ignore_errors=True)
    return cdir''')
# (3) o finish: a cadeia sem depender do pre-registro em disco (informativo), beta conferido contra o core, parcial com a causa, cache em try proprio,
#     so resultado COMPLETO com o D128 rodado; o resultado copiado ao Nos para o selo
rep('''        same_code = bool(R.get("spec_sha256") == _QP_SPEC_SHA256 and R.get("worker_sha256") == st["materialized"]["pilar_quantico_worker.py"]["sha256"] and all(pr_ok.values())
                         and (reuse or R.get("run_id") == st.get("run_id")))      # a marca da rodada: o resultado e' DESTA rodada (achado 7)''',
    '''        beta_ok = bool(st.get("beta_hex") and isinstance(core.get("beta"), float) and float(core["beta"]).hex() == st["beta_hex"] == R.get("beta_hex"))
        out["beta_matches_core"] = beta_ok
        # o pre-registro em disco e' INFORMATIVO (o um.py nao depende de um caminho local): a especificacao embutida, conferida pelo hash, e' o congelado
        same_code = bool(R.get("spec_sha256") == _QP_SPEC_SHA256 and R.get("worker_sha256") == st["materialized"]["pilar_quantico_worker.py"]["sha256"] and beta_ok
                         and (reuse or R.get("run_id") == st.get("run_id")))      # a marca da rodada: o resultado e' DESTA rodada (achado 7)''')
rep('''        if partial and same_code and der:
            # o trabalhador foi encerrado (prazo) depois das fases principais: o parcial e' resultado legitimo, mas PARCIAL -- dito, nunca gravado no cache
            verdict = verdict.replace("__GATE_UNTOUCHED", "__PARTIAL_RESULT_WORKER_STOPPED__GATE_UNTOUCHED")''',
    '''        if partial and same_code and der:
            # o parcial e' resultado legitimo, mas PARCIAL -- dito com a CAUSA (o prazo ou a morte do trabalhador), nunca gravado no cache
            _cause = "WORKER_STOPPED_BY_TIMEOUT" if out.get("timed_out") else ("WORKER_DIED_RC_%s" % out.get("worker_rc"))
            verdict = verdict.replace("__GATE_UNTOUCHED", "__PARTIAL_RESULT_%s__GATE_UNTOUCHED" % _cause)''')
rep('''        out["verdict"] = verdict
        out["custody_chain_ok"] = ok_chain
        out["summary"] = _qp_summary(R)
        out["all_verified"] = bool(ok_chain and "FIVE_JUMP_GKLS" in verdict)''', '''        out["verdict"] = verdict
        out["custody_chain_ok"] = ok_chain
        out["all_verified"] = bool(ok_chain and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"))
        try:
            out["summary"] = _qp_summary(R)
        except Exception as e_:
            out["summary"] = {}; out["summary_error"] = repr(e_)       # um passo acessorio nao rebaixa o veredito (achado da 2a passada)
        try:
            # o resultado no Nos, para o selo o hashear junto (achado 40)
            shutil.copyfile(rp, os.path.join(OUT, "um_absoluto_pilar_quantico.json"))
        except Exception as e_:
            out["copy_to_out_error"] = repr(e_)''')
rep('''            if ok_chain and not partial and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and "__PARTIAL_" not in verdict:
                out["reuse"]["saved_to_cache"] = _qp_save_cache(st, rp)      # so resultado COMPLETO vai ao cache; falha de ambiente nunca (achado 8)''',
    '''            if (ok_chain and not partial and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and "__PARTIAL_" not in verdict
                    and str((R.get("D128") or {}).get("status_code")) == "RAN"):
                try:
                    out["reuse"]["saved_to_cache"] = _qp_save_cache(st, rp)  # so resultado COMPLETO (com o D128 rodado) vai ao cache; falha de ambiente nunca
                except Exception as e_:
                    out["reuse"]["cache_error"] = repr(e_)                    # a falha do cache nao rebaixa o veredito (achado 3)
            else:
                out["reuse"]["not_cached_because"] = "resultado nao completo, nao conferido ou sem o D128"''')
rep('''        print("[v384] pilar quantico: %s" % verdict, flush=True)
    except Exception as e:''', '''        print("[v384] pilar quantico: %s" % verdict, flush=True)
        st["finished"] = True
    except Exception as e:''')
rep('''    except Exception as e:
        out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__FINISH_FAILED__GATE_UNTOUCHED", "all_verified": False, "error": repr(e)})
    return out''', '''    except Exception as e:
        out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__FINISH_FAILED__GATE_UNTOUCHED", "all_verified": False, "error": repr(e)})
        _qp_kill_tree(st.get("proc")); st["finished"] = True
    if not os.path.exists(os.path.join(OUT, "um_absoluto_pilar_quantico.json")) or out.get("copy_to_out_error"):
        try:
            with open(os.path.join(OUT, "um_absoluto_pilar_quantico.json"), "w", encoding="utf-8") as fh:
                json.dump({"verdict": out.get("verdict"), "result_file_absent": True}, fh, ensure_ascii=False, indent=1)
        except Exception:
            pass
    return out''')
# a recusa e o atalho de REUSE tambem marcam finished
rep('''        if st.get("refused"):
            out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__%s__GATE_UNTOUCHED" % re.sub(r"[^A-Z0-9_]", "_", st["refused"].split(":")[0].upper()),
                        "all_verified": False, "refused": st["refused"]})
            return out''', '''        if st.get("refused"):
            out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__%s__GATE_UNTOUCHED" % re.sub(r"[^A-Z0-9_]", "_", st["refused"].split(":")[0].upper()),
                        "all_verified": False, "refused": st["refused"]})
            st["finished"] = True
            try:
                with open(os.path.join(OUT, "um_absoluto_pilar_quantico.json"), "w", encoding="utf-8") as fh:
                    json.dump({"verdict": out["verdict"], "result_file_absent": True}, fh, ensure_ascii=False, indent=1)
            except Exception:
                pass
            return out''')
ast.parse(s.replace("__QP_WORKER_SRC__", "''").replace("__QP_SPEC_JSON__", "''"))
open(P + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(P + ".tmp", P); print("ok")
