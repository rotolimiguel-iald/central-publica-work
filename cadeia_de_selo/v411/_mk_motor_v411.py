# -*- coding: utf-8 -*-
"""_mk_motor_v411.py -- gera derivar_v411_motor.py a partir de derivar_v410_motor.py (mesmo motor; origem unica "v410"; mapa 409 -> 410 e 410 -> 411;
as LISTAS de versoes crescem, acrescentando o 410, nao se deslocam). Nao executa nada derivado. claude-construtor-v411, a servico da gerencia c1, 12/11/2026.
Molde: _mk_motor_v410.py. Escrito pela ferramenta Write."""
import ast, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v410", "derivar_v410_motor.py"), "rb").read().decode("utf-8")
t = src
L10 = "(399|400|401|402|403|404|405|406|407|408|409)"; L11 = "(399|400|401|402|403|404|405|406|407|408|409|410)"
assert t.count(L10) >= 4, t.count(L10)
assert t.count("399..410") >= 2, t.count("399..410")
assert t.count('padrao=r"39[9]|40[0123456789]|410"') == 1
t = t.replace(L10, "@L@").replace("399..410", "399..@11@").replace('padrao=r"39[9]|40[0123456789]|410"', 'padrao=r"39[9]|40[0123456789]|41[01]"')
t = re.sub(r"(?<![0-9])(408|409|410)(?![0-9])", lambda m: str(int(m.group(1)) + 1), t)
t = t.replace("@L@", L11).replace("@11@", "411")
for esperado in ('ORIGENS = {"v410": os.path.join(CH, "v410")}', 'MAPAS = {"v410": {"409": "410", "410": "411"}}',
                 'NUM3 = re.compile(r"(?<![0-9])' + L11 + '(?![0-9])")', 'base_v410', 'padrao=r"39[9]|40[0123456789]|41[01]"', 'origem="v410"', "399..411"):
    assert esperado in t, esperado
assert "@" + "L@" not in t and "@11@" not in t
ast.parse(t)
out = os.path.join(HERE, "derivar_v411_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v411_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t), hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
