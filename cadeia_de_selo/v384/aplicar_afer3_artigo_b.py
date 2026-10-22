# -*- coding: utf-8 -*-
"""Ajuste do trecho do artigo (PT/EN): a razao de nao ir ao cache composta EM CADA LINGUA a partir do codigo do runtime (not_cached_code), e o texto de
erro reduzido a caracteres seguros (o TXT nao fica com escapes crus). Backup ja feito em .bak_antes_afer3."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TX_OLD = r'''    _tx4 = lambda x_: "".join({"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "_": r"\_", "%": r"\%", "#": r"\#", "&": r"\&", "$": r"\$", "^": r"\^{}", "~": r"\~{}"}.get(c_, c_) for c_ in str(x_)[:200])'''
TX_NEW = r'''    _tx4 = lambda x_: "".join(c_ if (c_.isalnum() or c_ in " .,:;()'=<>/+-") else (r"\_" if c_ == "_" else "?") for c_ in str(x_)[:200])   # so caracteres seguros (PDF e TXT)
    _rz4 = _q4.get("reuse") or {}
    _ncc4 = str(_rz4.get("not_cached_code") or "")'''
PT_OLD = r'''                                                else ((r"; não foi guardado para reaproveitamento (" + _tx4((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) + r"). ")
                                                      if ((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) else r". "))'''
PT_NEW = r'''                                                else ((r"; não foi guardado para reaproveitamento ("
                                                       + ((r"o ponto $d=128$ não rodou nesta rodada, \texttt{" + _tx4(_ncc4.split(":", 1)[-1]) + r"}; o cache só guarda o resultado completo com ele") if _ncc4.startswith("D128_NOT_RAN")
                                                          else ((r"a gravação falhou: \texttt{" + _tx4(_rz4.get("cache_error")) + r"}") if _rz4.get("cache_error") else r"resultado não completo ou não conferido"))
                                                       + r"). ") if (_rz4.get("not_cached_because") or _rz4.get("cache_error")) else r". "))'''
EN_OLD = r'''                                                else ((r"; it was not stored for reuse (" + _tx4((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) + r"). ")
                                                      if ((_q4.get("reuse") or {}).get("not_cached_because") or (_q4.get("reuse") or {}).get("cache_error")) else r". "))'''
EN_NEW = r'''                                                else ((r"; it was not stored for reuse ("
                                                       + ((r"the $d=128$ point did not run in this run, \texttt{" + _tx4(_ncc4.split(":", 1)[-1]) + r"}; the cache keeps only a complete result with it") if _ncc4.startswith("D128_NOT_RAN")
                                                          else ((r"writing it failed: \texttt{" + _tx4(_rz4.get("cache_error")) + r"}") if _rz4.get("cache_error") else r"result not complete or not checked"))
                                                       + r"). ") if (_rz4.get("not_cached_because") or _rz4.get("cache_error")) else r". "))'''
for fn, pairs in (("artigo_pt_v384.pysnip", [(TX_OLD, TX_NEW), (PT_OLD, PT_NEW)]), ("artigo_en_v384.pysnip", [(TX_OLD, TX_NEW), (EN_OLD, EN_NEW)])):
    p = os.path.join(HERE, fn); s = open(p, "rb").read().decode("utf-8")
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:100])
        s = s.replace(old, new)
    b = s.encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("ok", fn)
