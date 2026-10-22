# -*- coding: utf-8 -*-
"""5a afericao no RUNTIME e no GERADOR DO CANDIDATO: o runtime grava out_file_sha256 = o sha256 do arquivo do pilar que ELE escreveu no Nos nesta rodada (o
resultado copiado ou o marcador); o marcador diz o motivo (e result_file_absent so quando nao ha resultado) e as escritas/remocoes tentam de novo (40 x 0,25 s,
como o trabalhador) e apagam o .tmp_qp na falha; o selo (W09b) so hasheia o arquivo do pilar se ele for o desta rodada -- senao grava NOT_THIS_RUN; o registro
do selo (W07) leva out_file_sha256 e out_file_remove_error. Backups ja feitos (.bak_antes_afer5)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer5", "rb").read() == raw
PAIRS = [
    ('''def _qp_out_marker(verdict, st):
    """O um_absoluto_pilar_quantico.json do Nos sem resultado DESTA rodada: um marcador desta rodada (troca atomica) -- o arquivo de uma rodada
    anterior nunca e' hasheado pelo selo como se fosse desta (3a afericao)."""
    p = os.path.join(OUT, "um_absoluto_pilar_quantico.json"); tmp = p + ".tmp_qp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"verdict": verdict, "result_file_absent": True, "run_id": st.get("run_id"), "key": st.get("key")}, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)''', '''def _qp_retry(fn, n=40, dt=0.25):
    """Tenta de novo (como o write_json_atomic do trabalhador): um leitor ou o antivirus segurando o arquivo por instantes nao derruba a escrita."""
    for i_ in range(n):
        try:
            return fn()
        except (PermissionError, OSError):
            if i_ == n - 1:
                raise
            time.sleep(dt)


def _qp_out_marker(verdict, st, reason):
    """O um_absoluto_pilar_quantico.json do Nos sem o resultado DESTA rodada: um marcador desta rodada (troca atomica, com novas tentativas), com o MOTIVO;
    devolve o sha256 do que escreveu (3a e 5a afericoes)."""
    p = os.path.join(OUT, "um_absoluto_pilar_quantico.json"); tmp = p + ".tmp_qp"
    b = json.dumps({"verdict": verdict, "marker": True, "reason": reason, "result_file_absent": reason != "copy_failed", "run_id": st.get("run_id"), "key": st.get("key")},
                   ensure_ascii=False, indent=1).encode("utf-8")
    try:
        with open(tmp, "wb") as fh:
            fh.write(b)
        _qp_retry(lambda: os.replace(tmp, p))
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
    return hashlib.sha256(open(p, "rb").read()).hexdigest()'''),
    ('''def _qp_out_marker_safe(out, verdict, st):
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
            out["out_file_remove_error"] = repr(e2)''', '''def _qp_out_marker_safe(out, verdict, st, reason):
    """O marcador desta rodada; se ele mesmo falhar, o arquivo do pilar no Nos e' REMOVIDO (com novas tentativas). Se nem a remocao for possivel (outro
    processo segurando o arquivo), os erros ficam no registro do selo e o SELO grava NOT_THIS_RUN para esse arquivo (W09b: so o que o runtime escreveu
    nesta rodada, out_file_sha256, e' hasheado) -- 4a e 5a afericoes."""
    try:
        out["out_file_sha256"] = _qp_out_marker(verdict, st, reason)
    except Exception as e_:
        out["out_marker_error"] = repr(e_)
        try:
            _qp_retry(lambda: os.remove(os.path.join(OUT, "um_absoluto_pilar_quantico.json")))
            out["out_file_removed"] = True
        except FileNotFoundError:
            out["out_file_removed"] = True
        except Exception as e2:
            out["out_file_remove_error"] = repr(e2)'''),
    ('''            _qp_out_marker_safe(out, out["verdict"], st)
            return out''', '''            _qp_out_marker_safe(out, out["verdict"], st, "not_run")
            return out'''),
    ('''            _qp_out_marker_safe(out, out["verdict"], st)   # o arquivo de uma rodada anterior NAO fica no Nos (3a e 4a afericoes)''',
     '''            _qp_out_marker_safe(out, out["verdict"], st, "no_result_file")   # o arquivo de uma rodada anterior NAO fica no Nos (3a, 4a e 5a afericoes)'''),
    ('''            shutil.copyfile(rp, os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"))
            os.replace(os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"), os.path.join(OUT, "um_absoluto_pilar_quantico.json"))
            out["copied_to_out"] = True''', '''            shutil.copyfile(rp, os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"))
            _qp_retry(lambda: os.replace(os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"), os.path.join(OUT, "um_absoluto_pilar_quantico.json")))
            out["copied_to_out"] = True
            out["out_file_sha256"] = hashlib.sha256(open(os.path.join(OUT, "um_absoluto_pilar_quantico.json"), "rb").read()).hexdigest()   # o que o selo aceita (W09b)'''),
    ('''        _qp_out_marker_safe(out, out.get("verdict"), st)   # TODO caminho sem a copia desta rodada: o marcador desta rodada, ou a remocao (3a e 4a afericoes)''',
     '''        try:
            os.remove(os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"))   # a sobra de uma copia que falhou (5a afericao)
        except OSError:
            pass
        _qp_out_marker_safe(out, out.get("verdict"), st, "copy_failed" if out.get("copy_to_out_error") else "finish_failed")   # o marcador desta rodada, ou a remocao (3a-5a)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
assert s.count("_qp_out_marker_safe(") == 4 and "_qp_out_marker(verdict, st)" not in s
ast.parse(s.replace("__QP_WORKER_SRC__", "x").replace("__QP_SPEC_JSON__", "x"))
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok runtime", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
# o gerador do candidato: W07 com out_file_sha256 e out_file_remove_error; W09b: NOT_THIS_RUN
G = os.path.join(HERE, "gerar_candidato_v384.py"); g = open(G, "rb").read().decode("utf-8")
assert open(G + ".bak_antes_afer5", "rb").read().decode("utf-8") == g
GP = [
    ('''"copied_to_out", "copy_to_out_error", "out_marker_error", "out_file_removed", "worker_sha256",''',
     '''"copied_to_out", "copy_to_out_error", "out_marker_error", "out_file_removed", "out_file_remove_error", "out_file_sha256", "worker_sha256",'''),
    ('''A10 = '    t = t.replace("' + BS + BS + 'bTGL", "β_TGL").replace("' + BS + BS + 'Msun", "M_sol")' + CRLF''',
     '''A09b = '        json.dump(seal, open(os.path.join(OUT, "um_absoluto_selo.json"), "w", encoding="utf-8"), indent=2)' + CRLF
add("W09b_selo_so_o_pilar_desta_rodada", "G_SELO", A09b,
    '        # v384 (5a afericao): o arquivo do pilar so e' + "'" + ' hasheado se for o que o runtime escreveu NESTA rodada (out_file_sha256); senao, NOT_THIS_RUN' + CRLF
    + '        _pq_ = core.get("quantum_pillar_v384") or {}' + CRLF
    + '        if "quantum_pillar_v384" in core and seal["sha256"].get("um_absoluto_pilar_quantico.json") not in ("MISSING_THIS_RUN", _pq_.get("out_file_sha256")):' + CRLF
    + '            seal["sha256"]["um_absoluto_pilar_quantico.json"] = "NOT_THIS_RUN"' + CRLF + A09b,
    "selo: o arquivo do pilar so vale se for o desta rodada (NOT_THIS_RUN).")
A10 = '    t = t.replace("' + BS + BS + 'bTGL", "β_TGL").replace("' + BS + BS + 'Msun", "M_sol")' + CRLF'''),
]
for old, new in GP:
    c = g.count(old); assert c == 1, (c, old[:100])
    g = g.replace(old, new)
ast.parse(g); open(G + ".tmp", "wb").write(g.encode("utf-8")); os.replace(G + ".tmp", G); print("ok gerador W07/W09b")
