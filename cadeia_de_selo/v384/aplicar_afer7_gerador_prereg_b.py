# -*- coding: utf-8 -*-
"""Achado do TESTE do congelamento (gerencia, 04/10): o nome da copia permanente de cada evidencia era <papel>__<nome base> e, numa pasta funda, passava do limite
de 260 caracteres do Windows. Agora o nome e' <papel><extensao> (unico por papel; o nome de origem fica em «origem»); e a pasta temporaria e' apagada se a copia
falhar (nada sobra). Backup de bytes; ast."""
import ast, os, time
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_antes_teste_congelamento_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    ('''        _dst = os.path.join(HERE, "evidencias_PREREGISTRO_V1", _pp_ + "__" + os.path.basename(_p_))''',
     '''        _dst = os.path.join(HERE, "evidencias_PREREGISTRO_V1", _pp_ + os.path.splitext(_p_)[1])   # nome curto e unico por papel (o limite de 260 do Windows)'''),
    ('''        _tmpd = _dd + ".tmp_" + time.strftime("%Y%m%d_%H%M%S"); os.makedirs(_tmpd)
        for _src, _dst, _sh in _COPIAR:
            _t = os.path.join(_tmpd, os.path.basename(_dst)); shutil.copyfile(_src, _t)
            assert fsha(_t) == _sh, "a copia da evidencia nao confere: %s" % _t
        os.replace(_tmpd, _dd)''', '''        _tmpd = _dd + ".tmp_" + time.strftime("%Y%m%d_%H%M%S"); os.makedirs(_tmpd)
        try:
            for _src, _dst, _sh in _COPIAR:
                _t = os.path.join(_tmpd, os.path.basename(_dst)); shutil.copyfile(_src, _t)
                assert fsha(_t) == _sh, "a copia da evidencia nao confere: %s" % _t
            os.replace(_tmpd, _dd)
        except BaseException:
            shutil.rmtree(_tmpd, ignore_errors=True)   # nada sobra de uma copia que falhou
            raise'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:100])
    s = s.replace(old, new)
assert len(set(["x"])) == 1
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok", len(PAIRS))
