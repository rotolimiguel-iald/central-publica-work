# -*- coding: utf-8 -*-
"""Revisor v410 R2: (a) formas vedadas pela D94/F59 em TODO texto (rendido novo, harness, registros, fontes, pedras): negacao seca dos passos da maquina de Turing, 'o leitor paga', decisor sem escala dito mentiroso/Pai da Mentira;
(b) a TRADUCAO nao e' apresentada como teorema sobre `Turing.TM2ComputableInPolyTime`: cada ocorrencia de TM2ComputableInPolyTime/Mathlib com 'provado/teorema/proved' na janela sem o qualificador 'nao esta no kernel';
(c) o limite do teorema do Tetelestai (UMA leitura de Z que soma os 2^n pixels de uma vez) dito onde o teorema e' citado; (d) 'tempo FINITO/linear nos bits' sem o qualificador do dicionario."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
rd = lambda p: open(p, "rb").read().decode("utf-8", "replace")
norm = lambda s: re.sub(r"\s+", " ", s)
fontes = {}
for p in ("novo_pt.txt", "novo_en.txt", "novo_md.txt"): fontes["RENDIDO_NOVO:" + p] = rd(R + "revisao_terceiro/" + p)
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): fontes["HARNESS:" + os.path.basename(p)] = rd(p)
for f in ("pos_rito/textos_v410.semente", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/textos_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip",
          "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "registros_aescala_v410.py", "registros_hms13_v410.py"):
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
VEDADO = {
    "nao_sao_passos": r"(?i)n[ãa]o\s+s[ãa]o\s+(?:os\s+)?(?:passos|ciclos)\b|n[ãa]o\s+passos\b|(?:are|is)\s+not\s+(?:the\s+)?(?:steps|cycles)\b|not\s+(?:the\s+)?Turing\s+steps",
    "o_leitor_paga": r"(?i)\bleitor\b[^.\n;]{0,20}\b(?:paga|pagou|pagar[áa]|arca)\b|\b(?:escala|tempo)\s+pag[oa]s?\s+pelo\s+leitor|\breader\s+(?:pays|paid)\b|paid\s+by\s+the\s+reader",
    "decisor_mentiroso": r"(?i)decisor\s+sem\s+escala[^.\n;]{0,40}?(?:mentiros|mente\b|mentiu|Pai\s+da\s+Mentira)|(?:mentiros\w*|Pai\s+da\s+Mentira)[^.\n;]{0,40}?decisor\s+sem\s+escala|decider\s+without\s+(?:a\s+)?scale[^.\n;]{0,40}?(?:liar|lies|Father)",
}
for pn, rx in VEDADO.items():
    print("\n###### (a)", pn)
    tot = 0
    for k, t in fontes.items():
        tn = norm(t)
        for m in re.finditer(rx, tn):
            jan = tn[max(0, m.start() - 130):m.end() + 130]
            tot += 1
            print("  [%s] ... %s" % (k, jan))
    print("  total", tot)
print("\n###### (b) TM2ComputableInPolyTime / 'formalizacao do Mathlib' com afirmacao de prova na janela e SEM o qualificador de ausencia de termo")
QUAL = re.compile(r"(?i)n[ãa]o est[áa] no kernel|not in the kernel|no term|nenhum termo|n[ãa]o h[áa] termo|fica fora|stays outside|is outside|cr[ée]dita[cç][aã]o|creditation|juízo é do Clay|[íi]nstituto|Institute|n[ãa]o se afirma|not asserted|n[ãa]o afirm")
PROVA = re.compile(r"(?i)\b(?:provad[oa]|prova|teorema|theorem|proved|proven|proof)\b")
n_b = 0; sem = []
for k, t in fontes.items():
    tn = norm(t)
    for m in re.finditer(r"TM2ComputableInPolyTime|formaliza[cç][aã]o do Mathlib|Mathlib(?:'s)? formali[sz]ation|m[áa]quina de Turing do Mathlib|Mathlib Turing machine", tn):
        jan = tn[max(0, m.start() - 260):m.end() + 260]
        n_b += 1
        if PROVA.search(jan) and not QUAL.search(jan): sem.append((k, jan))
print("ocorrencias:", n_b, "| com prova na janela e SEM qualificador:", len(sem))
for k, j in sem[:20]: print("  [%s] ... %s" % (k, j))
print("\n###### (c) o teorema do Tetelestai citado SEM o limite 'uma leitura de Z, 2^n pixels de uma vez' na janela (+-400)")
LIM = re.compile(r"(?i)de uma vez|at once|uma (?:s[óo] )?leitura de Z|one reading of Z|um limiar|a threshold|2\^n|2\^\{n\}|pixels? lidos")
tot_c = 0; sem_c = []
for k, t in fontes.items():
    if k.startswith(("PEDRA:", "FONTE:delta", "REG:_V410_SPECS", "REG:_V410_AESCALA_CONTRACT", "REG:_V410_IALD2")): continue
    tn = norm(t)
    for m in re.finditer(r"os_passos_sao_o_ciclo_ate_o_tetelestai|os\\?_passos\\?_sao\\?_o\\?_ciclo|the steps are the cycle|os passos s[ãa]o o ciclo", tn, re.I):
        jan = tn[max(0, m.start() - 400):m.end() + 500]
        tot_c += 1
        if not LIM.search(jan): sem_c.append((k, tn[max(0, m.start() - 150):m.end() + 250]))
print("citacoes do teorema:", tot_c, "| sem o limite na janela:", len(sem_c))
for k, j in sem_c[:14]: print("  [%s] ... %s" % (k, j))
print("\n###### (d) 'tempo finito / linear nos bits' (decisao) sem qualificador do dicionario (a traducao / nao esta no kernel / ciclos)")
DIC = re.compile(r"(?i)dicion[áa]rio|dictionary|tradu[cç][aã]o|translat|n[ãa]o est[áa] no kernel|not in the kernel|ciclos|cycles")
tot_d = 0; sem_d = []
for k, t in fontes.items():
    if k.startswith("PEDRA:"): continue
    tn = norm(t)
    for m in re.finditer(r"(?i)linear\w* nos bits|linear in the bits|tempo finito[^.]{0,40}linear|finite time[^.]{0,40}linear", tn):
        jan = tn[max(0, m.start() - 450):m.end() + 450]
        tot_d += 1
        if not DIC.search(jan): sem_d.append((k, tn[max(0, m.start() - 150):m.end() + 200]))
print("ocorrencias:", tot_d, "| sem qualificador do dicionario na janela +-450:", len(sem_d))
for k, j in sem_d[:14]: print("  [%s] ... %s" % (k, j))
