# -*- coding: utf-8 -*-
"""_mk_motor_v409.py -- gera derivar_v409_motor.py a partir de derivar_v408_motor.py (mesmo motor; origem unica "v408"; mapa 407 -> 408 e 408 -> 409;
as LISTAS de versoes crescem, acrescentando o 408, nao se deslocam). Nao executa nada derivado. claude-construtor-v409, a servico da gerencia c1, 05/11/2026.
Molde: _mk_motor_v408.py. Escrito pela ferramenta Write."""
import ast, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v408", "derivar_v408_motor.py"), "rb").read().decode("utf-8")
t = src
L8 = "(399|400|401|402|403|404|405|406|407)"; L9 = "(399|400|401|402|403|404|405|406|407|408)"
assert t.count(L8) >= 4, t.count(L8)
t = t.replace(L8, "@L@").replace("399..407", "399..408").replace("399..408", "399..409").replace("40[012345678]", "40[0123456789]")
t = re.sub(r"(?<![0-9])(406|407|408)(?![0-9])", lambda m: str(int(m.group(1)) + 1), t)
t = re.sub(r"2026110(3|4)(?![0-9])", lambda m: "2026110" + str(int(m.group(1)) + 1), t)
t = re.sub(r"\b0(3|4)/11/2026\b", lambda m: "0" + str(int(m.group(1)) + 1) + "/11/2026", t)
t = t.replace("@L@", L9)
for esperado in ('ORIGENS = {"v408": os.path.join(CH, "v408")}', 'MAPAS = {"v408": {"407": "408", "408": "409"}}',
                 'NUM3 = re.compile(r"(?<![0-9])' + L9 + '(?![0-9])")', 'base_v408', 'padrao=r"39[9]|40[0123456789]"', 'origem="v408"'):
    assert esperado in t, esperado
ast.parse(t)
out = os.path.join(HERE, "derivar_v409_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v409_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t), hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
