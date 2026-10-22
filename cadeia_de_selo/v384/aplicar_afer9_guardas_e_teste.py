# -*- coding: utf-8 -*-
"""9a afericao: (9N16) o gerar_candidato, a fumaca, o gerar_esperados e o instalador RECUSAM rodar com -O/PYTHONOPTIMIZE (as guardas sao assert); (9N2) no
teste do congelamento, os casos F passam um trabalhador INEXISTENTE: com a guarda, o gerador recusa nela; sem ela, morreria ao abrir o trabalhador, antes de
qualquer gravacao -- o teste nao depende so da guarda que testa. Backups de BYTES .bak_antes_afer9 (feitos e conferidos aqui)."""
import ast, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
GUARDA = 'if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (9a afericao)\n    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")\n'


def bak(p):
    raw = open(p, "rb").read()
    if os.path.exists(p + ".bak_antes_afer9"):
        assert open(p + ".bak_antes_afer9", "rb").read() == raw, p
    else:
        open(p + ".bak_antes_afer9", "wb").write(raw); assert open(p + ".bak_antes_afer9", "rb").read() == raw
    return raw


for fn in ("gerar_candidato_v384.py", "fumaca_v384.py", "gerar_esperados_v384.py", "instalar_v384.py"):
    p = os.path.join(HERE, fn); s = bak(p).decode("utf-8")
    assert "sys.flags.optimize" not in s
    m = [x for x in re.finditer(r"(?m)^import [^\n]*\bsys\b[^\n]*\n", s)]
    assert len(m) >= 1, fn
    k = m[0].end()
    s = s[:k] + GUARDA + s[k:]
    ast.parse(s)
    b = s.encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p); assert open(p, "rb").read() == b
    print("ok", fn)
T = os.path.join(HERE, "teste_congelamento_v384.py"); s = bak(T).decode("utf-8")
old = '''    r = subprocess.run([sys.executable, gp, TW, TT, TM, HERE, "--escolha=B_REDUZIDO"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)'''
new = '''    # (9a afericao) um trabalhador INEXISTENTE: com a guarda, recusa nela; sem ela, o gerador morreria ao abrir o trabalhador, antes de qualquer gravacao
    r = subprocess.run([sys.executable, gp, os.path.join(HERE, "NAO_EXISTE_worker.py"), TT, TM, HERE, "--escolha=B_REDUZIDO"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)'''
assert s.count(old) == 1
s = s.replace(old, new); ast.parse(s)
b = s.encode("utf-8"); open(T + ".tmp", "wb").write(b); assert os.path.getsize(T + ".tmp") == len(b); os.replace(T + ".tmp", T); assert open(T, "rb").read() == b
print("ok teste F")
