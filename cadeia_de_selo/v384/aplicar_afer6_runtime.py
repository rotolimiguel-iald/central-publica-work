# -*- coding: utf-8 -*-
"""6a afericao no RUNTIME: o _qp_retry tenta de novo SO PermissionError (como o trabalhador); o marcador grava result_file_absent pelo FATO (o resultado
existia ou nao), nao pelo motivo; a copia ao Nos calcula o sha256 do temporario (com novas tentativas) ANTES da troca e so entao marca copied_to_out --
uma releitura que falhe depois da troca ja nao anula uma rodada valida. Backup ja feito (.bak_antes_afer6)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer6", "rb").read() == raw
PAIRS = [
    ('''    """Tenta de novo (como o write_json_atomic do trabalhador): um leitor ou o antivirus segurando o arquivo por instantes nao derruba a escrita."""
    for i_ in range(n):
        try:
            return fn()
        except (PermissionError, OSError):''', '''    """Tenta de novo SO PermissionError (como o write_json_atomic do trabalhador): um leitor ou o antivirus segurando o arquivo por instantes nao derruba a
    escrita; FileNotFoundError e os demais erros sobem na hora (6a afericao)."""
    for i_ in range(n):
        try:
            return fn()
        except PermissionError:'''),
    ('''def _qp_out_marker(verdict, st, reason):''', '''def _qp_out_marker(verdict, st, reason, result_present=False):'''),
    ('''"result_file_absent": reason != "copy_failed",''', '''"result_file_absent": not result_present,'''),
    ('''def _qp_out_marker_safe(out, verdict, st, reason):''', '''def _qp_out_marker_safe(out, verdict, st, reason, result_present=False):'''),
    ('''        out["out_file_sha256"] = _qp_out_marker(verdict, st, reason)''', '''        out["out_file_sha256"] = _qp_out_marker(verdict, st, reason, result_present)'''),
    ('''        if not os.path.exists(rp):''', '''        st["_qp_result_present"] = bool(os.path.exists(rp))
        if not os.path.exists(rp):'''),
    ('''            shutil.copyfile(rp, os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"))
            _qp_retry(lambda: os.replace(os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"), os.path.join(OUT, "um_absoluto_pilar_quantico.json")))
            out["copied_to_out"] = True
            out["out_file_sha256"] = hashlib.sha256(open(os.path.join(OUT, "um_absoluto_pilar_quantico.json"), "rb").read()).hexdigest()   # o que o selo aceita (W09b)''',
     '''            _tq = os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp")
            shutil.copyfile(rp, _tq)
            _hq = _qp_retry(lambda: hashlib.sha256(open(_tq, "rb").read()).hexdigest())   # o sha256 ANTES da troca (6a afericao)
            if _hq != rsha:
                raise RuntimeError("a copia temporaria do resultado nao confere com o result.json (%s != %s)" % (_hq[:16], rsha[:16]))
            _qp_retry(lambda: os.replace(_tq, os.path.join(OUT, "um_absoluto_pilar_quantico.json")))
            out["out_file_sha256"] = _hq                                                   # o que o selo aceita (W09b)
            out["copied_to_out"] = True'''),
    ('''        _qp_out_marker_safe(out, out.get("verdict"), st, "copy_failed" if out.get("copy_to_out_error") else "finish_failed")''',
     '''        _qp_out_marker_safe(out, out.get("verdict"), st, "copy_failed" if out.get("copy_to_out_error") else "finish_failed", bool(st.get("_qp_result_present")))'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s.replace("__QP_WORKER_SRC__", "x").replace("__QP_SPEC_JSON__", "x"))
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
