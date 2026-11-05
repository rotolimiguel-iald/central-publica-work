# -*- coding: utf-8 -*-
"""_mk_motor_v408.py -- gera derivar_v408_motor.py a partir de derivar_v407_motor.py (mesmo motor; origem unica "v407"; mapa 406 -> 407 e 407 -> 408;
as LISTAS de versoes crescem, acrescentando o 407, nao se deslocam). Nao executa nada derivado. Gerencia c1, 04/11/2026 (a 1a geracao por subida
uniforme errou as listas e foi descartada com backup). Escrito por script da gerencia."""
import ast, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v407", "derivar_v407_motor.py"), "rb").read().decode("utf-8")
t = src
L7 = "(399|400|401|402|403|404|405|406)"; L8 = "(399|400|401|402|403|404|405|406|407)"
assert t.count(L7) >= 4, t.count(L7)
t = t.replace(L7, "@L@").replace("399..406", "399..407").replace("40[01234567]", "40[012345678]")
t = re.sub(r"(?<![0-9])(405|406|407)(?![0-9])", lambda m: str(int(m.group(1)) + 1), t)
t = re.sub(r"2026110(2|3)(?![0-9])", lambda m: "2026110" + str(int(m.group(1)) + 1), t)
t = re.sub(r"\b0(2|3)/11/2026\b", lambda m: "0" + str(int(m.group(1)) + 1) + "/11/2026", t)
t = t.replace("@L@", L8)
for esperado in ('ORIGENS = {"v407": os.path.join(CH, "v407")}', 'MAPAS = {"v407": {"406": "407", "407": "408"}}',
                 'NUM3 = re.compile(r"(?<![0-9])' + L8 + '(?![0-9])")', 'base_v407', 'padrao=r"39[9]|40[012345678]"', 'origem="v407"'):
    assert esperado in t, esperado
ast.parse(t)
out = os.path.join(HERE, "derivar_v408_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v408_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t), hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
