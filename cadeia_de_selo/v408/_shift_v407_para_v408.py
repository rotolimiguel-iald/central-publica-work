# -*- coding: utf-8 -*-
"""_shift_v407_para_v408.py -- gera _mk_motor_v408.py e _bump_copia_v408.py a partir dos de v407 por SUBIDA UNIFORME DE ROTULO
(405->406, 406->407, 407->408; B14->B15, B15->B16, B16->B17; datas 02/11->03/11, 03/11->04/11; classes de regex 40[...] e B1[...] e -2026110[..]),
mais um conserto explicito do texto do cabecalho (o corpo herdado e' o da v407). Nao executa nada; ast.parse das saidas; nao sobrescreve sem backup.
Gerencia c1, 04/11/2026. Escrito pela ferramenta Write."""
import ast, datetime, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); CH = os.path.dirname(HERE); V7 = os.path.join(CH, "v407")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def shift(t):
    # placeholders para subida simultanea
    t = re.sub(r"40\[012345678\]", "@C8@", t); t = re.sub(r"40\[01234567\]", "@C7@", t); t = re.sub(r"40\[0123456\]", "@C6@", t)
    t = t.replace("@C6@", "40[01234567]").replace("@C7@", "40[012345678]").replace("@C8@", "40[0123456789]")
    t = t.replace("B1[456]", "B1[567]").replace("-2026110[23]-R1", "-2026110[34]-R1")
    t = re.sub(r"(?<![0-9])(405|406|407)(?![0-9])", lambda m: str(int(m.group(1)) + 1), t)
    t = re.sub(r"(?<![0-9A-Za-z_])B(14|15|16)(?![0-9A-Za-z_])", lambda m: "B" + str(int(m.group(1)) + 1), t)
    t = re.sub(r"2026110(2|3)(?![0-9])", lambda m: "2026110" + str(int(m.group(1)) + 1), t)
    t = re.sub(r"\b0(2|3)/11/2026\b", lambda m: "0" + str(int(m.group(1)) + 1) + "/11/2026", t)
    return t

def grava(dst, texto):
    b = texto.encode("utf-8")
    if os.path.exists(dst):
        if open(dst, "rb").read() == b:
            return "igual"
        os.replace(dst, dst + ".bak_" + TS)
    open(dst + ".tmp", "wb").write(b); assert os.path.getsize(dst + ".tmp") == len(b); os.replace(dst + ".tmp", dst); return "gravado"

res = {}
for nome in ("_mk_motor_v407.py", "_bump_copia_v407.py"):
    src = open(os.path.join(V7, nome), "rb").read().decode("utf-8")
    novo = shift(src)
    if nome == "_bump_copia_v407.py":
        a = "(bundle de 301 modulos, fechamento_v407, quatro chaves)"
        assert a in novo, "cabecalho do bump nao casou"
        novo = novo.replace(a, "(bundle de 9 modulos, psion_canto_v407, a chave do lema lida do kernel)")
        assert 'DEP_VELHO = "B15-v406-20261103-R1"' in novo, "DEP_VELHO nao casou"
        assert 'MAPA_N = {"406": "407", "407": "408"}' in novo, "MAPA_N nao casou"
    ast.parse(novo)
    dst = os.path.join(HERE, nome.replace("v407", "v408"))
    res[nome] = (grava(dst, novo), hashlib.sha256(novo.encode("utf-8")).hexdigest()[:16], sum(1 for a, b in zip(src.split("\n"), novo.split("\n")) if a != b))
print(res)
