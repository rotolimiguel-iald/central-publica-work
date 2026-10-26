# -*- coding: utf-8 -*-
"""G1 (25/10/2026, gerência a7): a custódia CONJUNTA (v399 selada e recusada pela Bancada + v400 que a corrige; o espelho está na v398).
 1. kh e cunhagens: quando a versão corrente não traz `kh_n1_cobertura_vN`/`cunhagens_vN` (a v400 não mudou o kernel nem inscreveu nada),
    usar o registro MAIS NOVO entre (anterior, N] — o da v399 —, e dizer qual (`kh_registro`, `cunhagens.registro`).
 2. o cruzamento com o handoff: «anterior» do handoff (v399) ≠ maior cofre anterior (v398) passa a ser CONJUNTA reconhecida quando a versão
    intermediária está selada na cadeia (`work\\cadeia_de_selo\\vK`) e não tem cofre — então não é divergência: grava `conjunta: [vK, vN]`.
    O pino da intermediária não é comparado (não há cofre dela); continua comparado quando o anterior é o do cofre.
Trocas contadas; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\fatos.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
CR, LF = chr(13), chr(10)
NL = CR + LF if (CR + LF) in s else LF
if "def _mais_novo_entre" in s:
    raise SystemExit("já aplicado")
pares = [
    ('''    khc, kht = kh_de(core, v)
    khcB, khtB = kh_de(coreB, ant)
''', '''    khc, kht = kh_de(core, v)
    kh_reg = "kh_n1_cobertura_" + v
    if khc is None:                       # 25/10: custódia conjunta — o registro mais novo entre (anterior, v] (a v400 não mudou o kernel)
        kk = _mais_novo_entre(core, "kh_n1_cobertura_", ant, v)
        if kk:
            khc, kht = kh_de(core, kk[len("kh_n1_cobertura_"):])
            kh_reg = kk
    khcB, khtB = kh_de(coreB, ant)
'''),
    ('''        "cunhagens": ({"n": len((core.get("cunhagens_" + v) or {}).get("verbatim") or {}), "data": _data_das_inscricoes(core.get("cunhagens_" + v) or {})}
                      if isinstance(core.get("cunhagens_" + v), dict) else None),
''', '''        "cunhagens": _cunhagens_conjunta(core, ant, v),
        "kh_registro": kh_reg,
'''),
    ('''        if q.anterior != F["anterior"]:
            out["divergencias"].append("anterior: handoff diz %s, o maior cofre anterior é %s (custódia conjunta? conferir)" % (q.anterior, F["anterior"]))
''', '''        if q.anterior != F["anterior"]:
            # 25/10: CONJUNTA reconhecida — a intermediária está selada na cadeia e não tem cofre (a v399, recusada pela Bancada, corrigida pela v400)
            try:
                _ni, _na, _nv = int(q.anterior[1:]), int(F["anterior"][1:]), int(F["versao"][1:])
            except (TypeError, ValueError):
                _ni = _na = _nv = 0
            from pathlib import Path as _P
            _cs = _P(r"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo") / q.anterior
            _cofre = _P(r"C:\\IALD\\Central de Patentes\\vault\\originals_copy") / ("um_unificado_" + q.anterior)
            if _na < _ni < _nv and _cs.is_dir() and not _cofre.exists():
                out["conjunta"] = [q.anterior, F["versao"]]
            else:
                out["divergencias"].append("anterior: handoff diz %s, o maior cofre anterior é %s (custódia conjunta? conferir)" % (q.anterior, F["anterior"]))
'''),
    ('''def _fatos_do_handoff(''', '''def _mais_novo_entre(core, prefixo, ant, v):
    """A chave `prefixoVK` mais nova com ant < K <= v (custódia conjunta, 25/10/2026)."""
    try:
        a, b = int(ant[1:]), int(v[1:])
    except (TypeError, ValueError):
        return None
    ks = [k for k in core if k.startswith(prefixo) and k[len(prefixo):][:1] == "v" and k[len(prefixo) + 1:].isdigit()
          and a < int(k[len(prefixo) + 1:]) <= b and isinstance(core.get(k), dict)]
    return max(ks, key=lambda k: int(k[len(prefixo) + 1:])) if ks else None


def _cunhagens_conjunta(core, ant, v):
    k = "cunhagens_" + v if isinstance(core.get("cunhagens_" + v), dict) else _mais_novo_entre(core, "cunhagens_", ant, v)
    if not k:
        return None
    r = core.get(k) or {}
    return {"n": len(r.get("verbatim") or {}), "data": _data_das_inscricoes(r), "registro": k}


def _fatos_do_handoff('''),
]
for a, b in pares:
    a, b = a.replace(LF, NL), b.replace(LF, NL)
    n = s.count(a)
    assert n == 1, (a[:70], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("fatos.py: custódia conjunta (kh/cunhagens do registro mais novo entre anterior e N; anterior intermediário selado sem cofre) | %d -> %d" % (len(raw), P.stat().st_size))
