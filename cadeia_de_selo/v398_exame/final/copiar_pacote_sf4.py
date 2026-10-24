# -*- coding: utf-8 -*-
"""copiar_pacote_sf4.py -- exame final v398 (c1, 23/10/2026): copia SO' LEITURA do pacote v398 para v398_exame\\sf4\\work\\cadeia_de_selo\\v398 (sem as pastas pesadas que
o fechar nao usa nem os .bak), mais o que o harness do fechar le fora do pacote (v397\\bancada_B3, as cunhagens de 22/10); cria a copia do harness com o sandbox num
caminho curto (v398_exame\\sb4, hs4). Nada fora de v398_exame e' escrito."""
import fnmatch, hashlib, os, shutil, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398"
E = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame"
D = os.path.join(E, "sf4", "work", "cadeia_de_selo", "v398")
IGN = ["bateria_pre_selo", "falso_nos", "imp_*", "sim_*", "arvore_simulada_h8", "harness_saida_v398", "*.bak_*", "EXAME_PONTOS_*", "SIMULACAO_ARVORE_NOS_*", "__pycache__", "dry_v398"]
def ign(d, names):
    return [n for n in names if any(fnmatch.fnmatch(n, p) for p in IGN)]
if os.path.exists(D):
    sys.exit("ja existe: %s (nao sobrescrevo)" % D)
shutil.copytree(V, D, ignore=ign)
# o dry_v398 so' com os .txt/.tex/.json/.md (o harness pode ler o core_ensaio.json e os txt)
os.makedirs(os.path.join(D, "dry_v398"), exist_ok=True)
for f in os.listdir(os.path.join(V, "dry_v398")):
    if f.endswith((".txt", ".tex", ".json", ".md")):
        shutil.copy2(os.path.join(V, "dry_v398", f), os.path.join(D, "dry_v398", f))
# o que o fechar/harness le fora do pacote
B3 = os.path.join(E, "sf4", "work", "cadeia_de_selo", "v397", "bancada_B3"); shutil.copytree(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397\bancada_B3", B3)
CU = os.path.join(E, "sf4", "work", "cunhagens_13out"); os.makedirs(CU, exist_ok=True)
for f in os.listdir(r"C:\IALD\Central de Patentes\work\cunhagens_13out"):
    if f.endswith(".txt"):
        shutil.copy2(os.path.join(r"C:\IALD\Central de Patentes\work\cunhagens_13out", f), os.path.join(CU, f))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
print("candidato na copia:", h(os.path.join(D, "um_v398_candidato.py")), "| original:", h(os.path.join(V, "um_v398_candidato.py")))
for f in ("pos_rito/textos_v398.py", "pos_rito/fechar_v398.py", "runtime_quadro_v397.py", "quadro_v397.py", "ESPERADOS_v398.json", "pos_rito/leitura_v398.py"):
    print(f, h(os.path.join(D, f)) == h(os.path.join(V, f)))
P = os.path.join(D, "pos_rito")
t = open(os.path.join(P, "harness_fechar_sandbox_v398.py"), encoding="utf-8").read()
a = 'OUT = os.path.join(HERE, "harness_saida_v398"); SB = os.path.join(OUT, "fechar_sandbox")'
assert t.count(a) == 1, "ancora do harness mudou"
b = 'OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v398_exame/hs4"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v398_exame/sb4"   # EXAME: caminho curto (MAX_PATH)'
open(os.path.join(P, "harness_fechar_sandbox_v398_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t.replace(a, b))
print("harness EXAME escrito")
