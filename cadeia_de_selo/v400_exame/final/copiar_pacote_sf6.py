# -*- coding: utf-8 -*-
"""copiar_pacote_sf6.py -- exame final v400 (c1, 24/10/2026): copia SO' LEITURA do pacote v400 para v400_exame\\final\\s6\\work\\cadeia_de_selo\\v400 (sem as pastas
de saida e de importacao nem os .bak), mais o que o conferidor e o harness do fechar leem fora do pacote pelo caminho relativo ao WK do delta (v399: delta, conferencias,
insumos, base_v398, os recibos do B(n); v398/v397: insumos e bancada_B3; as cunhagens; o esboco R3.5). Faz as copias de EXAME com os caminhos de escrita trocados para
pastas minhas e curtas: o sandbox do C15 do conferidor (antes C:\\t\\vb17) e o OUT/SB do harness do fechar. Nada fora de v400_exame\\final e' escrito."""
import fnmatch, hashlib, os, shutil, sys
W = r"C:\IALD\Central de Patentes\work"
V = os.path.join(W, "cadeia_de_selo", "v400")
F = os.path.join(W, "cadeia_de_selo", "v400_exame", "final")
S = os.path.join(F, "s6", "work")
D = os.path.join(S, "cadeia_de_selo", "v400")
IGN = ["imp_*", "sim_*", "conferidor_import_*", "harness_saida_v400", "falso_nos", "*.bak_*", "EXAME_PONTOS_*", "SIMULACAO_ARVORE_NOS_*", "__pycache__", "vb17_evidencia"]
ign = lambda d, names: [n for n in names if any(fnmatch.fnmatch(n, p) for p in IGN)]
if os.path.exists(D):
    sys.exit("ja existe: %s (nao sobrescrevo)" % D)
shutil.copytree(V, D, ignore=ign)
# v399: os arquivos de topo pequenos (delta, conferencias, pinos...) e as pastas que o delta/harness leem
V9 = os.path.join(W, "cadeia_de_selo", "v399"); D9 = os.path.join(S, "cadeia_de_selo", "v399"); os.makedirs(D9)
for f in os.listdir(V9):
    p = os.path.join(V9, f)
    if os.path.isfile(p) and os.path.getsize(p) < 5 * 2**20 and ".bak_" not in f:
        shutil.copy2(p, os.path.join(D9, f))
for sub in ("insumos", "base_v398", "bancada_B3_ensaio_20261024_162108", "bancada_B3_servico", "pos_rito"):
    if os.path.isdir(os.path.join(V9, sub)):
        shutil.copytree(os.path.join(V9, sub), os.path.join(D9, sub), ignore=shutil.ignore_patterns("harness_saida_v399", "*.bak_*", "__pycache__"))
os.makedirs(os.path.join(D9, "bateria_pre_selo", "ensaio_1"))
for f in os.listdir(os.path.join(V9, "bateria_pre_selo", "ensaio_1")):
    if f.startswith("RECIBO_SINCRONIZACAO_"):
        shutil.copy2(os.path.join(V9, "bateria_pre_selo", "ensaio_1", f), os.path.join(D9, "bateria_pre_selo", "ensaio_1", f))
for anterior in ("v397", "v398"):
    src = os.path.join(W, "cadeia_de_selo", anterior); dst = os.path.join(S, "cadeia_de_selo", anterior); os.makedirs(dst, exist_ok=True)
    for sub in ("insumos", "bancada_B3"):
        if os.path.exists(os.path.join(src, sub)):
            shutil.copytree(os.path.join(src, sub), os.path.join(dst, sub))
CU = os.path.join(S, "cunhagens_13out"); os.makedirs(CU)
for f in os.listdir(os.path.join(W, "cunhagens_13out")):
    if f.endswith(".txt"):
        shutil.copy2(os.path.join(W, "cunhagens_13out", f), os.path.join(CU, f))
shutil.copytree(os.path.join(W, "bancada_vinculo_12out", "R3_5"), os.path.join(S, "bancada_vinculo_12out", "R3_5"), ignore=shutil.ignore_patterns("_construcao", "evidencias", "__pycache__"))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
for f in ("um_v400_candidato.py", "conferir_rito_v400.py", "delta_v400.py", "ESPERADOS_v400.json", "pos_rito/fechar_v400.py", "pos_rito/textos_v400.py", "dry_v400/um.py", "teste_conferidor_positivo_v400.py"):
    print(f, h(os.path.join(D, f)) == h(os.path.join(V, f)), h(os.path.join(D, f)))
print("esboco na copia:", h(os.path.join(S, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")))
# as copias de EXAME (so os caminhos de escrita trocados)
t = open(os.path.join(D, "conferir_rito_v400.py"), encoding="utf-8").read()
a = '_sd = os.path.join("C:" + os.sep, "t", "vb17", "conf_%s" % umsha)'
assert t.count(a) == 1, "ancora do C15 mudou"
open(os.path.join(D, "conferir_rito_v400_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, '_sd = os.path.join(HERE, "vb_conf_exame", "conf_%s" % umsha)   # EXAME: o sandbox do C15 dentro da minha copia'))
t = open(os.path.join(D, "teste_conferidor_positivo_v400.py"), encoding="utf-8").read()
a = 'os.path.join(HERE, "conferir_rito_v400.py")'
assert t.count(a) == 1
open(os.path.join(D, "teste_conferidor_positivo_v400_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, 'os.path.join(HERE, "conferir_rito_v400_EXAME.py")'))
P = os.path.join(D, "pos_rito")
t = open(os.path.join(P, "harness_fechar_sandbox_v400.py"), encoding="utf-8").read()
a = 'OUT = os.path.join(HERE, "harness_saida_v400"); SB = os.path.join(OUT, "fechar_sandbox")'
assert t.count(a) == 1, "ancora do harness mudou"
b = 'OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v400_exame/final/hs6"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v400_exame/final/sb6"   # EXAME: caminho curto (MAX_PATH)'
open(os.path.join(P, "harness_fechar_sandbox_v400_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, b))
print("copias de EXAME escritas")
