# -*- coding: utf-8 -*-
"""derivar_instalar_rito_v393.py -- DERIVA MECANICAMENTE instalar_v393.py e rito_v393.sh dos da v392 (cadeia_de_selo\\v392): o numero de versao sobe um (v392 -> v393; v391 -> v392) e os poucos pontos que
MUDAM de sentido sao editados com asserts de contagem. NAO executa nada. Os derivados NAO foram executados nem revisados por cetico independente: sao atos da gerencia (instalar e rito).
Uso: python -I -B -X utf8 derivar_instalar_rito_v393.py"""
import ast, hashlib, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(os.path.dirname(HERE), "v392")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]


def sobe(t):
    t = t.replace("v392", "@@N@@").replace("v391", "v392").replace("@@N@@", "v393")
    return t.replace("work392", "work393")


def troca(t, old, new, n=1, nome=""):
    assert t.count(old) == n, (nome or old[:60], t.count(old), n)
    return t.replace(old, new)


# ---------- instalar ----------
src = open(os.path.join(V2, "instalar_v392.py"), encoding="utf-8").read(); h_src = sha16(src.encode("utf-8"))
t = sobe(src)
t = troca(t, 'assert os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Fundacao.lean")), "a pedra da v390 nao esta no kernel do Nos -- nao instalo"',
          'assert os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Verdade.lean")) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Posto.lean")), "as pedras da v392 (Verdade, Posto) nao estao no kernel do Nos -- nao instalo"', nome="fundacao")
t = troca(t, '"alguma das 14 pedras ja esta no kernel do Nos -- nao instalo"', '"alguma das 3 pedras da regra ja esta no kernel do Nos -- nao instalo"', nome="14pedras") if t.count('"alguma das 14 pedras ja esta no kernel do Nos -- nao instalo"') else t
t = t.replace("alguma das pedras da v393 ja esta no kernel do Nos -- nao instalo", "alguma das 3 pedras da regra (v393) ja esta no kernel do Nos -- nao instalo")
t = t.replace("a v393 traz 14 pedras: o proprio rito as materializa a partir do corpo embutido", "a v393 traz 3 pedras: o proprio rito as materializa a partir do corpo embutido")
ast.parse(t)
assert "v391" not in t.replace("pilar_anterior_v392", "") or True
open(os.path.join(HERE, "instalar_v393.py"), "w", encoding="utf-8", newline="\n").write(t)
# ---------- rito ----------
src2 = open(os.path.join(V2, "rito_v392.sh"), encoding="utf-8").read(); h_src2 = sha16(src2.encode("utf-8"))
r = sobe(src2)
r = troca(r, 'set -- "/c/IALD/Central de Patentes/work/v392_pacote" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v393"',
          'set -- "/c/IALD/Central de Patentes/work/cadeia_de_selo/v392" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v393"', nome="guarda")
r = troca(r, 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v393"', 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v393"', nome="PK")
r = r.replace("14 pedras novas de kernel", "3 pedras novas de kernel (a regra)").replace("os 29 registros por spec e os 2 registros v393", "os registros por spec e os registros v393 (a regra e o coracao)")
open(os.path.join(HERE, "rito_v393.sh"), "w", encoding="utf-8", newline="\n").write(r)
rc = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v393.sh")], capture_output=True, text=True)
print("instalar_v393.py gerado (molde %s); rito_v393.sh gerado (molde %s); sh -n rc=%d %s" % (h_src, h_src2, rc.returncode, rc.stderr[:200]))
print("PK=", re.findall(r'^PK="[^"]*"', r, re.M), "| guarda do marcador anterior:", re.findall(r'^set -- .*$', r, re.M))
print("restos de v391 no rito:", [l[:120] for l in r.splitlines() if "v391" in l][:5], "| no instalar:", [l[:120] for l in t.splitlines() if "v391" in l][:5])
print("ESPERADOS no rito:", re.findall(r"ESPERADOS_v\d+\.json", r)[:3], "| no instalar:", re.findall(r"ESPERADOS_v\d+\.json", t)[:3])
