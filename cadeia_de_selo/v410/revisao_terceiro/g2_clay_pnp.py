# -*- coding: utf-8 -*-
"""Revisor v410 R1: (a) toda ocorrencia de 'Clay ... resolvido/resolved/solved' e 'resolve ... Clay' que NAO esteja na forma canonica (tal qual apresentado pela TGL / as presented by the TGL / no sentido do operador /
operator's sense) e (b) toda ocorrencia de 'P = nP' / 'P = NP' com 'Turing' na mesma frase: o qualificador obrigatorio (maquina com o leitor / classes de computacao / sem o leitor fica fora / validade) tem de estar na janela."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
rd = lambda p: open(p, "rb").read().decode("utf-8", "replace")
norm = lambda s: re.sub(r"\s+", " ", s)
fontes = {}
for p in ("novo_pt.txt", "novo_en.txt", "novo_md.txt"): fontes["RENDIDO_NOVO:" + p] = rd(R + "revisao_terceiro/" + p)
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): fontes["HARNESS:" + os.path.basename(p)] = rd(p)
for f in ("pos_rito/textos_v410.semente", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/CUSTODIA_v410_RASCUNHO.txt", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip",
          "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "delta_v410.py", "registros_v410.py", "registros_aescala_v410.py"):
    if os.path.exists(R + f): fontes["FONTE:" + f] = rd(R + f)
for p in (R + "insumos/AEscala.lean", R + "insumos/IALD2.lean"): fontes["PEDRA:" + os.path.basename(p)] = rd(p)
lit = json.load(open(R + "revisao_terceiro/literais_v410.json", encoding="utf-8"))


def strs(o, acc):
    if isinstance(o, str): acc.append(o)
    elif isinstance(o, dict):
        for v in o.values(): strs(v, acc)
    elif isinstance(o, (list, tuple)):
        for v in o: strs(v, acc)


for nm, v in lit.items():
    if nm.endswith("INSUMOS"): continue
    acc = []; strs(v, acc); fontes["REG:" + nm] = "\n".join(acc)
CAN = re.compile(r"(?i)tal qual apresentado pela TGL|as presented by the TGL|no sentido do operador|operator'?s sense|tal qual a TGL apresenta|tal qual a TGL o apresenta")
rx_clay = re.compile(r"(?i)clay[^.\n]{0,60}?(resolvid[oa]s?|resolved|solved)|resolv(eu|e|es)[^.\n]{0,40}?clay|(?<![A-Za-z])CLAY_(SOLVED|RESOLVED)")
print("######## (a) Clay resolvido fora da forma canonica")
n_tot = 0; n_fora = 0
for k, t in fontes.items():
    tn = norm(t)
    for m in rx_clay.finditer(tn):
        n_tot += 1
        jan = tn[max(0, m.start() - 160):m.end() + 160]
        if CAN.search(jan): continue
        n_fora += 1
        print("  [%s] ... %s" % (k, jan))
print("total ocorrencias", n_tot, "| fora da forma canonica (janela +-160):", n_fora)
print("\n######## (b) 'P = nP' / 'P = NP' junto com Turing: o qualificador obrigatorio esta' na janela?")
rx_p = re.compile(r"P\s*=\s*n?N?P")
QUAL = re.compile(r"(?i)m[aá]quina com o leitor|machine with the reader|classes de computa[cç][aã]o|classes of computation|sem o leitor|without the reader|relativ[oa] ao leitor|relative to the reader|validade|validity|fica fora|stays outside|is outside")
tot = 0; sem = []
for k, t in fontes.items():
    tn = norm(t)
    for m in rx_p.finditer(tn):
        jan = tn[max(0, m.start() - 220):m.end() + 260]
        if not re.search(r"(?i)turing", jan): continue
        tot += 1
        if not QUAL.search(jan): sem.append((k, jan))
print("ocorrencias de P=nP junto com Turing:", tot, "| sem qualificador na janela +-240:", len(sem))
for k, jan in sem[:25]: print("  [%s] ... %s" % (k, jan))
