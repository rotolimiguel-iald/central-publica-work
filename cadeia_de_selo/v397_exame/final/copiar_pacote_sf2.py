# -*- coding: utf-8 -*-
"""copiar_pacote_sf2.py -- exame final v397 (c1, 23/10/2026): copia SO' LEITURA do pacote v397 (candidato 388cc374) para v397_exame\\sf2\\work\\cadeia_de_selo\\v397,
sem as pastas pesadas que o fechar nao usa (bateria, falso_nos, imp_*, sim_*, arvore_simulada_h8, saidas do harness) nem os .bak; depois cria a copia do harness com o
sandbox num caminho curto (v397_exame\\sb2, hs2). Nada fora de v397_exame e' escrito."""
import fnmatch, hashlib, os, shutil, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397"
E = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397_exame"
D = os.path.join(E, "sf2", "work", "cadeia_de_selo", "v397")
IGN = ["bateria_pre_selo", "falso_nos", "imp_*", "sim_*", "arvore_simulada_h8", "harness_saida_v397", "*.bak_*", "EXAME_PONTOS_*", "SIMULACAO_ARVORE_NOS_*", "__pycache__"]
def ign(d, names):
    return [n for n in names if any(fnmatch.fnmatch(n, p) for p in IGN)]
if os.path.exists(D):
    sys.exit("ja existe: %s (nao sobrescrevo)" % D)
shutil.copytree(V, D, ignore=ign)
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
print("candidato na copia:", h(os.path.join(D, "um_v397_candidato.py")), "| original:", h(os.path.join(V, "um_v397_candidato.py")))
for f in ("pos_rito/textos_v397.py", "pos_rito/fechar_v397.py", "runtime_quadro_v397.py", "quadro_v397.py", "ESPERADOS_v397.json"):
    print(f, h(os.path.join(D, f)) == h(os.path.join(V, f)))
P = os.path.join(D, "pos_rito")
t = open(os.path.join(P, "harness_fechar_sandbox_v397.py"), encoding="utf-8").read()
a = 'OUT = os.path.join(HERE, "harness_saida_v397"); SB = os.path.join(OUT, "fechar_sandbox")'
assert t.count(a) == 1, "ancora do harness mudou"
b = 'OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v397_exame/hs2"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v397_exame/sb2"   # EXAME: caminho curto (MAX_PATH)'
open(os.path.join(P, "harness_fechar_sandbox_v397_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, b))
print("harness EXAME escrito")
