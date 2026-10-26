# -*- coding: utf-8 -*-
"""copiar_pacote_sf5.py -- exame final v399 (c1, 24/10/2026): copia SO' LEITURA do pacote v399 para v399_exame\\sf5\\work\\cadeia_de_selo\\v399 (sem as pastas pesadas que o fechar
nao usa nem os .bak), mais o que o harness do fechar le fora do pacote (v398\\bancada_B3, v397\\insumos, v398\\insumos, as cunhagens); cria a copia do harness com o sandbox num
caminho curto (v399_exame\\sb5, hs5). Nada fora de v399_exame e' escrito."""
import fnmatch, hashlib, os, shutil, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399"
E = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399_exame"
D = os.path.join(E, "sf5", "work", "cadeia_de_selo", "v399")
IGN = ["bateria_pre_selo", "falso_nos", "imp_*", "sim_*", "arvore_simulada_h8", "harness_saida_v399", "*.bak_*", "EXAME_PONTOS_*", "SIMULACAO_ARVORE_NOS_*", "__pycache__", "conferidor_import_*"]
def ign(d, names):
    return [n for n in names if any(fnmatch.fnmatch(n, p) for p in IGN)]
if os.path.exists(D):
    sys.exit("ja existe: %s (nao sobrescrevo)" % D)
shutil.copytree(V, D, ignore=ign)
for anterior in ("v397", "v398"):
    src = os.path.join(r"C:\IALD\Central de Patentes\work\cadeia_de_selo", anterior)
    dst = os.path.join(E, "sf5", "work", "cadeia_de_selo", anterior); os.makedirs(dst, exist_ok=True)
    for sub in ("insumos", "bancada_B3"):
        if os.path.exists(os.path.join(src, sub)):
            shutil.copytree(os.path.join(src, sub), os.path.join(dst, sub))
CU = os.path.join(E, "sf5", "work", "cunhagens_13out"); os.makedirs(CU, exist_ok=True)
for f in os.listdir(r"C:\IALD\Central de Patentes\work\cunhagens_13out"):
    if f.endswith(".txt"):
        shutil.copy2(os.path.join(r"C:\IALD\Central de Patentes\work\cunhagens_13out", f), os.path.join(CU, f))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
print("candidato na copia:", h(os.path.join(D, "um_v399_candidato.py")), "| original:", h(os.path.join(V, "um_v399_candidato.py")))
for f in ("pos_rito/textos_v399.py", "pos_rito/fechar_v399.py", "runtime_quadro_v397.py", "quadro_v397.py", "ESPERADOS_v399.json", "pos_rito/leitura_v399.py", "dry_v399/um.py"):
    print(f, os.path.exists(os.path.join(D, f)) and h(os.path.join(D, f)) == h(os.path.join(V, f)))
P = os.path.join(D, "pos_rito")
t = open(os.path.join(P, "harness_fechar_sandbox_v399.py"), encoding="utf-8").read()
a = 'OUT = os.path.join(HERE, "harness_saida_v399"); SB = os.path.join(OUT, "fechar_sandbox")'
assert t.count(a) == 1, "ancora do harness mudou"
b = 'OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v399_exame/hs5"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v399_exame/sb5"   # EXAME: caminho curto (MAX_PATH)'
open(os.path.join(P, "harness_fechar_sandbox_v399_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, b))
print("harness EXAME escrito")
