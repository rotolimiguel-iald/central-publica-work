# -*- coding: utf-8 -*-
"""copiar_pacote_s7.py -- exame final v401 (c1, 25/10/2026): copia SO' LEITURA do pacote v401 para v401_exame\\final\\s7\\work\\cadeia_de_selo\\v401 (sem saidas,
importacoes nem .bak), mais o que o conferidor e o harness do fechar leem fora do pacote (v400 e v399: delta, conferencias, runtime, insumos, bases, recibos do B(n);
v398/v397: insumos e bancada_B3; as cunhagens; o esboco R3.5). Faz as copias de EXAME com os caminhos de escrita trocados para pastas minhas: o sandbox do C15 do
conferidor (antes C:\\t\\vb18) e o OUT/SB do harness do fechar. Nada fora de v401_exame\\final e' escrito."""
import fnmatch, hashlib, os, shutil, sys
W = r"C:\IALD\Central de Patentes\work"
V = os.path.join(W, "cadeia_de_selo", "v401")
F = os.path.join(W, "cadeia_de_selo", "v401_exame", "final")
S = os.path.join(F, "s7", "work")
D = os.path.join(S, "cadeia_de_selo", "v401")
IGN = ["imp_*", "sim_*", "conferidor_import_*", "harness_saida_v401", "falso_nos", "*.bak_*", "EXAME_PONTOS_*", "SIMULACAO_ARVORE_NOS_*", "__pycache__", "vb18_evidencia", "arvore_simulada_h8"]
ign = lambda d, names: [n for n in names if any(fnmatch.fnmatch(n, p) for p in IGN)]
if os.path.exists(D):
    sys.exit("ja existe: %s (nao sobrescrevo)" % D)
shutil.copytree(V, D, ignore=ign)
for vv, subs in (("v400", ("insumos", "base_v399", "bancada_B3", "bancada_B3_ensaio_20261024_211418", "bancada_B3_servico", "pos_rito", "kernel", "vinculo")),
                 ("v399", ("insumos", "base_v398", "pedra", "bancada_B3_ensaio_20261024_162108", "bancada_B3_servico"))):
    src = os.path.join(W, "cadeia_de_selo", vv); dst = os.path.join(S, "cadeia_de_selo", vv); os.makedirs(dst)
    for f in os.listdir(src):
        p = os.path.join(src, f)
        if os.path.isfile(p) and os.path.getsize(p) < 5 * 2**20 and ".bak_" not in f:
            shutil.copy2(p, os.path.join(dst, f))
    for sub in subs:
        if os.path.isdir(os.path.join(src, sub)):
            shutil.copytree(os.path.join(src, sub), os.path.join(dst, sub), ignore=shutil.ignore_patterns("harness_saida_*", "*.bak_*", "__pycache__"))
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
for f in ("um_v401_candidato.py", "conferir_rito_v401.py", "delta_v401.py", "ESPERADOS_v401.json", "pos_rito/fechar_v401.py", "pos_rito/textos_v401.py", "dry_v401/um.py", "teste_conferidor_positivo_v401.py"):
    print(f, h(os.path.join(D, f)) == h(os.path.join(V, f)), h(os.path.join(D, f)))
print("esboco na copia:", h(os.path.join(S, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")))
t = open(os.path.join(D, "conferir_rito_v401.py"), encoding="utf-8").read()
a = '_sd = os.path.join("C:" + os.sep, "t", "vb18", "conf_%s" % umsha)'
assert t.count(a) == 1, "ancora do C15 mudou"
open(os.path.join(D, "conferir_rito_v401_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, '_sd = os.path.join(HERE, "vb_conf_exame", "conf_%s" % umsha)'))
t = open(os.path.join(D, "teste_conferidor_positivo_v401.py"), encoding="utf-8").read()
a = 'os.path.join(HERE, "conferir_rito_v401.py")'
assert t.count(a) == 1
open(os.path.join(D, "teste_conferidor_positivo_v401_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, 'os.path.join(HERE, "conferir_rito_v401_EXAME.py")'))
P = os.path.join(D, "pos_rito")
t = open(os.path.join(P, "harness_fechar_sandbox_v401.py"), encoding="utf-8").read()
a = 'OUT = os.path.join(HERE, "harness_saida_v401"); SB = os.path.join(OUT, "fechar_sandbox")'
assert t.count(a) == 1, "ancora do harness mudou"
b = 'OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v401_exame/final/hs7"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v401_exame/final/sb7"   # EXAME: caminho curto (MAX_PATH)'
open(os.path.join(P, "harness_fechar_sandbox_v401_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, b))
print("copias de EXAME escritas")
