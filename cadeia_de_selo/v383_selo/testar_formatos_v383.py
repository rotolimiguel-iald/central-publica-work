# -*- coding: utf-8 -*-
"""So leitura: exercita, com um dicionario de teste, os textos da v383, o corpo e a linha do handoff, e as frases formatadas do registro e das superficies."""
import re, ast, importlib.util, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
L = open("leitura_v383.py", encoding="utf-8").read()
keys = set(re.findall(r"V\[['\"]([A-Za-z0-9_]+)['\"]\]\s*=", L)) | {"nos", "aplicado_json", "the_ledger_of_charges_v383", "the_ledger_of_charges_reading_v383"}
V = {k: "<%s>" % k for k in keys}
V.update(umb=33146483, pedras={"TheLedgerOfCharges": {"sha16": "5ee9", "n_print": 19}, "ThePsionAndTheViscosity": {"sha16": "0a4e", "n_print": 13}}, tentativas=[],
         n_loc=19, n_psv=13, kf_on=32, kf_n=32, data="02/10/2026", n_ledger=11, rot_n=9, rot_exc=5, rot_inc=4, pr_label="V1.4")
spec = importlib.util.spec_from_file_location("textos_v383", "textos_v383.py"); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
bad = []
for fn in ("core_txt", "rodada_txt", "linhagem", "desenho", "atlas", "topico_missao", "topico_central", "topico_regra", "topico_regimes", "arvore_linha", "verbete", "remissivo", "topico_suspensao"):
    out = getattr(T, fn)(V)
    left = [x for x in re.findall(r"\{[A-Za-z_0-9]+\}", out) if x != "{it}"]
    if left or "onze" in out or " nove pares" in out:
        bad.append((fn, left[:3]))
print("textos:", "OK" if not bad else bad)
H = open("handoff_v383.py", encoding="utf-8").read()
m = re.search(r'corpo = \(""".*?"""\s*%\s*dict\(V, umb=format\(V\["umb"\], ","\)\)\)', H, re.S)
corpo = eval(m.group(0)[len("corpo = "):], {"V": V, "format": format})
sobra = re.findall(r"%\([a-z_0-9]+\)s", corpo)
cam = [x for x in ("cadeia_de_selo" + os.sep + "v383" + os.sep + "AFERIDOR_v383.txt", "cadeia_de_selo" + os.sep + "v382" + os.sep + "AFERIDOR_v382.txt") if x in corpo]
m2 = re.search(r'linha = \((".*?" % \(V\["data"\]\[:5\], V\["n_ledger"\], V\["rot_n"\], V\["pr_label"\], V\["s16"\]\))\)', H, re.S)
linha = eval(m2.group(1), {"V": V})
print("handoff:", len(corpo), "chars | sobrando:", sobra, "| caminhos do arquivo:", cam, "| nove/onze digitados:", ("onze" in corpo) or (" nove pares" in corpo))
print("   linha:", linha)
R = open("registrar_resultado_v383.py", encoding="utf-8").read()
t1 = re.search(r'titulo=("v383 SELADA: o livro de cobrancas.*?" % \(V\["n_loc"\], V\["n_psv"\], V\["kf_on"\], V\["kf_n"\], V\["n_ledger"\], V\["rot_n"\]\))', R, re.S)
print("registrar titulo:", eval(t1.group(1), {"V": V})[:230])
t2 = re.search(r'nao_refazer=("nenhum lado e cego.*?" % \(V\["rot_n"\], V\["rot_exc"\], V\["rot_inc"\]\))', R, re.S)
print("registrar nao_refazer:", eval(t2.group(1), {"V": V})[:230])
S = open("superficies_v383.py", encoding="utf-8").read()
t3 = re.search(r"('%s %s %s \(O LIVRO DE COBRANÇAS tipado.*?' % \(MARCA, V\['teor'\], V\['compl'\], V\['n_ledger'\], V\['rot_n'\], V\['pr_label'\]\))", S, re.S)
print("superficies:", eval(t3.group(1), {"V": V, "MARCA": "<MARCA>"})[:220])
for f in ("textos_v383.py", "handoff_v383.py", "registrar_resultado_v383.py", "patch_arvore_indice_v383.py", "superficies_v383.py", "espera_rito_v383.py", "arquivar_v383.py", "leitura_v383.py", "manifesto_v383.py"):
    ast.parse(open(f, encoding="utf-8").read())
print("todos compilam; marcas 382 restantes:", [f for f in ("superficies_v383.py", "patch_arvore_indice_v383.py", "handoff_v383.py", "chain_pos_rito_v383.sh") if re.search(r"_(sup|p|handoff|i)382", open(f, encoding="utf-8").read())])
