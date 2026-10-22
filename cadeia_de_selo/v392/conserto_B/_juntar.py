import os
f = "testar_rodape_B.py"
b = open(f, "rb").read().decode("utf-8")
i = b.index("def run_one(")
head = b[:i]
a = 'deps = [c for c in todos if c[5]]\nsel_ctrl = [by[n] for n in SEL + [CTRL_POS_COM_PRINT] + CTRL_NEG]\nrodar = deps + [c for c in sel_ctrl if c not in deps]\n'
c = 'deps = [c for c in todos if c[5]]\nsel_ctrl = [c for c in todos if c[3] == "POSITIVO"] + [by[n] for n in CTRL_NEG]   # TODOS os positivos (o patch vale para todos) + 2 negativos de controle\n'
assert head.count(a) == 1
head = head.replace(a, c)
nova = open("_parte_nova.txt", "rb").read().decode("utf-8")
open(f + ".tmp", "wb").write((head + nova).encode("utf-8")); os.replace(f + ".tmp", f)
