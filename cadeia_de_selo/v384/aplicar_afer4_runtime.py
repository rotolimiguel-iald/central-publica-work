# -*- coding: utf-8 -*-
"""4a afericao no RUNTIME: se o marcador desta rodada nao puder ser gravado, o arquivo do pilar no Nos e' REMOVIDO (o selo grava a ausencia: falha visivel);
se a copia do resultado ao Nos falhar, a cadeia de custodia nao fecha (CUSTODY_CHAIN_INCOMPLETE, all_verified False, nada ao cache); a volta do cache antigo
tem o erro registrado; e o registro do selo leva copied_to_out, copy_to_out_error, out_marker_error e out_file_removed (no gerador do candidato).
Backup ja feito (.bak_antes_afer4)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer4", "rb").read() == raw
PAIRS = [
    ('''    try:
        os.replace(tmp, cdir)
    except Exception:
        if old:                                          # a troca falhou: o cache antigo VOLTA ao lugar (3a afericao)
            try:
                os.replace(old, cdir)
            except Exception:
                pass
        shutil.rmtree(tmp, ignore_errors=True)
        raise''', '''    try:
        os.replace(tmp, cdir)
    except Exception as e1:
        e2 = None
        if old:                                          # a troca falhou: o cache antigo VOLTA ao lugar (3a afericao); se a volta falhar, isso fica dito (4a)
            try:
                os.replace(old, cdir)
            except Exception as e_r:
                e2 = e_r
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError("a troca do cache falhou: %r; a volta do antigo: %s" % (e1, ("FALHOU: %r (o antigo ficou em %s)" % (e2, old)) if e2 else ("ok" if old else "nao havia antigo")))'''),
    ('''    os.replace(tmp, p)


def _qp_summary(R):''', '''    os.replace(tmp, p)


def _qp_out_marker_safe(out, verdict, st):
    """O marcador desta rodada; se ele mesmo falhar, o arquivo do pilar no Nos e' REMOVIDO: o de outra rodada nunca fica (o selo grava a ausencia, falha
    visivel) -- 4a afericao."""
    try:
        _qp_out_marker(verdict, st)
    except Exception as e_:
        out["out_marker_error"] = repr(e_)
        try:
            os.remove(os.path.join(OUT, "um_absoluto_pilar_quantico.json"))
            out["out_file_removed"] = True
        except FileNotFoundError:
            out["out_file_removed"] = True
        except Exception as e2:
            out["out_file_remove_error"] = repr(e2)


def _qp_summary(R):'''),
    ('''            st["finished"] = True
            try:
                _qp_out_marker(out["verdict"], st)
            except Exception as e_:
                out["out_marker_error"] = repr(e_)
            return out''', '''            st["finished"] = True
            _qp_out_marker_safe(out, out["verdict"], st)
            return out'''),
    ('''            try:
                _qp_out_marker(out["verdict"], st)           # o arquivo de uma rodada anterior NAO fica no Nos (3a afericao)
            except Exception as e_:
                out["out_marker_error"] = repr(e_)''', '''            _qp_out_marker_safe(out, out["verdict"], st)   # o arquivo de uma rodada anterior NAO fica no Nos (3a e 4a afericoes)'''),
    ('''        except Exception as e_:
            out["copy_to_out_error"] = repr(e_)
        if reuse:''', '''        except Exception as e_:
            out["copy_to_out_error"] = repr(e_)
            # o resultado nao chegou ao Nos: a cadeia ate o selo NAO fecha (4a afericao) -- nada ao cache, all_verified False, dito no veredito
            ok_chain = False; out["custody_chain_ok"] = False; out["all_verified"] = False
            if "__RESULTS_VOID__" not in verdict and "__NOT_RUN__" not in verdict and "__CUSTODY_CHAIN_INCOMPLETE__" not in verdict:
                verdict = verdict.replace("__GATE_UNTOUCHED", "__CUSTODY_CHAIN_INCOMPLETE__GATE_UNTOUCHED"); out["verdict"] = verdict
        if reuse:'''),
    ('''    if not out.get("copied_to_out"):
        try:
            _qp_out_marker(out.get("verdict"), st)           # TODO caminho sem a copia desta rodada grava o marcador desta rodada (3a afericao)
        except Exception as e_:
            out["out_marker_error"] = repr(e_)
    return out''', '''    if not out.get("copied_to_out"):
        _qp_out_marker_safe(out, out.get("verdict"), st)   # TODO caminho sem a copia desta rodada: o marcador desta rodada, ou a remocao (3a e 4a afericoes)
    return out'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
assert "_qp_out_marker(out" not in s and s.count("_qp_out_marker_safe(") == 4
ast.parse(s.replace("__QP_WORKER_SRC__", "x").replace("__QP_SPEC_JSON__", "x"))
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok runtime", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
G = os.path.join(HERE, "gerar_candidato_v384.py"); g = open(G, "rb").read().decode("utf-8")
assert open(G + ".bak_antes_afer4", "rb").read().decode("utf-8") == g
old = '''"result_sha256", "details_sha256", "cpuref_sha256", "run_dir", "worker_sha256",'''
assert g.count(old) == 1
g = g.replace(old, '''"result_sha256", "details_sha256", "cpuref_sha256", "run_dir", "copied_to_out", "copy_to_out_error", "out_marker_error", "out_file_removed", "worker_sha256",''')
ast.parse(g); open(G + ".tmp", "wb").write(g.encode("utf-8")); os.replace(G + ".tmp", G); print("ok gerador W07")
