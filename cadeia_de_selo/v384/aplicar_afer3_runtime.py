# -*- coding: utf-8 -*-
"""As correcoes da 3a afericao no RUNTIME: o um_absoluto_pilar_quantico.json de uma rodada anterior nunca sobrevive (um marcador DESTA rodada o
substitui no finish, e o resultado o substitui se houver); o cache restaura o antigo se a troca falhar; o resumo conta TODAS as identidades (o modo
zero entra) e leva, por d e sigma, quantas estimativas do T1 nao tiveram solucao finita e o maior erro; a razao de nao ir ao cache dita com a causa;
as citacoes dos achados da 2a passada corrigidas. Backup de bytes; LF; ast."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_antes_afer3"
if not os.path.exists(bak):
    open(bak, "wb").write(raw)
assert open(bak, "rb").read() == raw
PAIRS = []
A = lambda old, new: PAIRS.append((old, new))

A('''    old = None
    if os.path.isdir(cdir):
        old = cdir + ".old_" + time.strftime("%Y%m%d_%H%M%S")
        os.replace(cdir, old)
    os.replace(tmp, cdir)
    if old:
        shutil.rmtree(old, ignore_errors=True)
    return cdir''', '''    old = None
    if os.path.isdir(cdir):
        old = cdir + ".old_" + time.strftime("%Y%m%d_%H%M%S")
        os.replace(cdir, old)
    try:
        os.replace(tmp, cdir)
    except Exception:
        if old:                                          # a troca falhou: o cache antigo VOLTA ao lugar (3a afericao)
            try:
                os.replace(old, cdir)
            except Exception:
                pass
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    if old:
        shutil.rmtree(old, ignore_errors=True)
    return cdir


def _qp_out_marker(verdict, st):
    """O um_absoluto_pilar_quantico.json do Nos sem resultado DESTA rodada: um marcador desta rodada (troca atomica) -- o arquivo de uma rodada
    anterior nunca e' hasheado pelo selo como se fosse desta (3a afericao)."""
    p = os.path.join(OUT, "um_absoluto_pilar_quantico.json"); tmp = p + ".tmp_qp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"verdict": verdict, "result_file_absent": True, "run_id": st.get("run_id"), "key": st.get("key")}, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)''')
A('''                   "identities_checked": {k: sum((c.get("identities_checked") or {}).get(k, 0) for c in cf) for k in ("CP", "TP", "NONRETURN", "PSD", "SS_RES", "SPOHN")},''',
  '''                   "identities_checked": {k: sum((c.get("identities_checked") or {}).get(k, 0) for c in cf) for k in sorted({kk for c in cf for kk in (c.get("identities_checked") or {})})},''')
A('''                                 "median_abs_p_err": {k[6:]: (v[k] or {}).get("median_abs_p_err") for k in v if k.startswith("sigma_")}} for d, v in t1.items()}}''',
  '''                                 "median_abs_p_err": {k[6:]: (v[k] or {}).get("median_abs_p_err") for k in v if k.startswith("sigma_")},
                                 "max_beta_rel_err": {k[6:]: (v[k] or {}).get("max_beta_rel_err") for k in v if k.startswith("sigma_")},
                                 "n_nonfinite_beta": {k[6:]: (v[k] or {}).get("n_nonfinite_beta") for k in v if k.startswith("sigma_")}} for d, v in t1.items()}}''')
A('''            st["finished"] = True
            try:
                with open(os.path.join(OUT, "um_absoluto_pilar_quantico.json"), "w", encoding="utf-8") as fh:
                    json.dump({"verdict": out["verdict"], "result_file_absent": True}, fh, ensure_ascii=False, indent=1)
            except Exception:
                pass
            return out''', '''            st["finished"] = True
            try:
                _qp_out_marker(out["verdict"], st)
            except Exception as e_:
                out["out_marker_error"] = repr(e_)
            return out''')
A('''        if not os.path.exists(rp):
            out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__NO_RESULT_FILE__GATE_UNTOUCHED", "all_verified": False}); return out''',
  '''        if not os.path.exists(rp):
            out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__NO_RESULT_FILE__GATE_UNTOUCHED", "all_verified": False})
            try:
                _qp_out_marker(out["verdict"], st)           # o arquivo de uma rodada anterior NAO fica no Nos (3a afericao)
            except Exception as e_:
                out["out_marker_error"] = repr(e_)
            st["finished"] = True
            return out''')
A('''                         and (reuse or R.get("run_id") == st.get("run_id")))      # a marca da rodada: o resultado e' DESTA rodada (achado 7)''',
  '''                         and (reuse or R.get("run_id") == st.get("run_id")))      # a marca da rodada: o resultado e' DESTA rodada (achado 7 da 1a passada)''')
A('''            out["summary"] = {}; out["summary_error"] = repr(e_)       # um passo acessorio nao rebaixa o veredito (achado da 2a passada)
        try:
            # o resultado no Nos, para o selo o hashear junto (achado 40)
            shutil.copyfile(rp, os.path.join(OUT, "um_absoluto_pilar_quantico.json"))
        except Exception as e_:
            out["copy_to_out_error"] = repr(e_)''', '''            out["summary"] = {}; out["summary_error"] = repr(e_)       # um passo acessorio nao rebaixa o veredito (achado 33 da 2a passada)
        try:
            # o resultado no Nos, para o selo o hashear junto (achado 36 da 2a passada); troca atomica
            shutil.copyfile(rp, os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"))
            os.replace(os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"), os.path.join(OUT, "um_absoluto_pilar_quantico.json"))
            out["copied_to_out"] = True
        except Exception as e_:
            out["copy_to_out_error"] = repr(e_)''')
A('''                    out["reuse"]["cache_error"] = repr(e_)                    # a falha do cache nao rebaixa o veredito (achado 3)
            else:
                out["reuse"]["not_cached_because"] = "resultado nao completo, nao conferido ou sem o D128"''',
  '''                    out["reuse"]["cache_error"] = repr(e_)                    # a falha do cache nao rebaixa o veredito (achados 7 e 33 da 2a passada)
            else:
                _d128sc = str((R.get("D128") or {}).get("status_code"))
                out["reuse"]["not_cached_because"] = ("o D128 nao rodou nesta rodada (%s): o cache so guarda resultado completo com o D128" % _d128sc
                                                      if (ok_chain and not partial and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and _d128sc != "RAN")
                                                      else "resultado nao completo ou nao conferido")''')
A('''    if not os.path.exists(os.path.join(OUT, "um_absoluto_pilar_quantico.json")) or out.get("copy_to_out_error"):
        try:
            with open(os.path.join(OUT, "um_absoluto_pilar_quantico.json"), "w", encoding="utf-8") as fh:
                json.dump({"verdict": out.get("verdict"), "result_file_absent": True}, fh, ensure_ascii=False, indent=1)
        except Exception:
            pass
    return out''', '''    if not out.get("copied_to_out"):
        try:
            _qp_out_marker(out.get("verdict"), st)           # TODO caminho sem a copia desta rodada grava o marcador desta rodada (3a afericao)
        except Exception as e_:
            out["out_marker_error"] = repr(e_)
    return out''')
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s.replace("__QP_WORKER_SRC__", "x").replace("__QP_SPEC_JSON__", "x"))
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "trocas; sha16", hashlib.sha256(b).hexdigest()[:16])
