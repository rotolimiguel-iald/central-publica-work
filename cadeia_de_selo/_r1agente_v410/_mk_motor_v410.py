# -*- coding: utf-8 -*-
"""_mk_motor_v410.py -- gera derivar_v410_motor.py a partir de derivar_v409_motor.py (mesmo motor; origem unica "v409"; mapa 408 -> 409 e 409 -> 410;
as LISTAS de versoes crescem, acrescentando o 409, nao se deslocam). Nao executa nada derivado. claude-construtor-v410, a servico da gerencia c1, 06/11/2026.
Molde: _mk_motor_v409.py. Escrito pela ferramenta Write."""
import ast, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v409", "derivar_v409_motor.py"), "rb").read().decode("utf-8")
t = src
L9 = "(399|400|401|402|403|404|405|406|407|408)"; L10 = "(399|400|401|402|403|404|405|406|407|408|409)"
assert t.count(L9) >= 4, t.count(L9)
assert t.count("399..409") >= 2, t.count("399..409")
assert t.count('padrao=r"39[9]|40[0123456789]"') == 1
t = t.replace(L9, "@L@").replace("399..409", "399..@10@").replace('padrao=r"39[9]|40[0123456789]"', 'padrao=r"39[9]|40[0123456789]|4@10@"')
t = re.sub(r"(?<![0-9])(407|408|409)(?![0-9])", lambda m: str(int(m.group(1)) + 1), t)
t = re.sub(r"2026110(4|5)(?![0-9])", lambda m: "2026110" + str(int(m.group(1)) + 1), t)
t = re.sub(r"\b0(4|5)/11/2026\b", lambda m: "0" + str(int(m.group(1)) + 1) + "/11/2026", t)
t = t.replace("@L@", L10).replace("4@10@", "410").replace("@10@", "410")
for esperado in ('ORIGENS = {"v409": os.path.join(CH, "v409")}', 'MAPAS = {"v409": {"408": "409", "409": "410"}}',
                 'NUM3 = re.compile(r"(?<![0-9])' + L10 + '(?![0-9])")', 'base_v409', 'padrao=r"39[9]|40[0123456789]|410"', 'origem="v409"', "399..410"):
    assert esperado in t, esperado
assert "@" + "L@" not in t and "@10@" not in t
ast.parse(t)
out = os.path.join(HERE, "derivar_v410_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v410_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t), hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
