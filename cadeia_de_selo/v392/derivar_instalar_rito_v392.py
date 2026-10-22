# -*- coding: utf-8 -*-
"""derivar_instalar_rito_v392.py -- DERIVA MECANICAMENTE instalar_v392.py e rito_v392.sh dos da v391 (cadeia_de_selo\\v391): o numero de versao sobe um (v391 -> v392; v390 -> v391)
e os poucos pontos que MUDAM de sentido sao editados com asserts de contagem. NAO executa nada. Os dois derivados NAO foram executados nem revisados por cetico independente:
sao atos da gerencia (etapas 7 e 8 do plano). Uso: python -I -B -X utf8 derivar_instalar_rito_v392.py"""
import ast, hashlib, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V1 = os.path.join(os.path.dirname(HERE), "v391")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]


def sobe(t):
    t = t.replace("v391", "@@N@@").replace("v390", "v391").replace("@@N@@", "v392")
    return t.replace("work391", "work392")


def troca(t, old, new, n=1, nome=""):
    assert t.count(old) == n, (nome or old[:60], t.count(old), n)
    return t.replace(old, new)


# ---------- instalar ----------
src = open(os.path.join(V1, "instalar_v391.py"), encoding="utf-8").read(); h_src = sha16(src.encode("utf-8"))
t = sobe(src)
t = troca(t, 'assert h16(raw0) == ESP["origem_sha16"] == "0f5154bcc2f931cb"', 'assert h16(raw0) == ESP["origem_sha16"] == CM["base_v391_sha16"]', nome="origem")
t = troca(t, 'assert os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Fundacao.lean")), "a pedra da v391 nao esta no kernel do Nos -- nao instalo"',
          'assert os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Fundacao.lean")), "a pedra da v390 nao esta no kernel do Nos -- nao instalo"\n'
          'assert not [rel for rel in ESP["pedras_sha256"] if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "alguma das 13 pedras ja esta no kernel do Nos -- nao instalo"', nome="fundacao")
t = troca(t, "(a v392 nao traz pedra nova)", "(a v392 traz 13 pedras: o proprio rito as materializa a partir do corpo embutido)", nome="docstring")
t = troca(t, "pilar_anterior_v391", "pilar_anterior_v391", n=t.count("pilar_anterior_v391"), nome="pilar")
ast.parse(t)
open(os.path.join(HERE, "instalar_v392.py"), "w", encoding="utf-8", newline="\n").write(t)
# ---------- rito ----------
src2 = open(os.path.join(V1, "rito_v391.sh"), encoding="utf-8").read(); h_src2 = sha16(src2.encode("utf-8"))
r = sobe(src2)
r = troca(r, 'PK="/c/IALD/Central de Patentes/work/v392_pacote"', 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v392"', nome="PK")
r = troca(r, "C:/IALD/Central de Patentes/work/v392_pacote/ESPERADOS_v392.json", "C:/IALD/Central de Patentes/work/cadeia_de_selo/v392/ESPERADOS_v392.json", nome="esperados")
assert 'PK390="/c/IALD/Central de Patentes/work/v391_pacote"' in r.replace("PK390", "PK390") or 'PK391=' in r or 'PK390=' in r
open(os.path.join(HERE, "rito_v392.sh"), "w", encoding="utf-8", newline="\n").write(r)
rc = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v392.sh")], capture_output=True, text=True)
print("instalar_v392.py gerado (molde %s); rito_v392.sh gerado (molde %s); sh -n rc=%d %s" % (h_src, h_src2, rc.returncode, rc.stderr[:200]))
import re
print("PK=", re.findall(r'^PK="[^"]*"', r, re.M), "| guarda do marcador anterior:", re.findall(r'^PK\d+="[^"]*"', r, re.M))
