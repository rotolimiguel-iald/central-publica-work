# -*- coding: utf-8 -*-
"""Revisor v409 R3: varredura INDEPENDENTE (a minha, nao a do construtor) por «Fock» e por «Ω … uniforme» perto de OPEN/aberto/pendente/'ainda nao'/'por fazer'/'fica para'/v41x, em TODOS os textos que saem:
(A) fontes novos (artigos, registros, delta, runtime, guarda, pos_rito, handoff-textos) e os 52 textos rendidos do harness (README/site, Atlas, core memory, handoff, linhagem, topico, ...);
(B) a secao v409 do artigo PT/EN do ensaio, a linha v409 do .md canonico e as strings dos registros v409 do core do ensaio (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409); (C) os docs de preparacao (RELATORIO, PLANO).
Segmento = entre . ; | quebra de linha aspas « » e o ponto mediano. Isencao SO' para o historico declarado: E21, v407, deixou, dizia, ficava, podad/pruned (e a documentacao da propria guarda)."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
ruim = re.compile(r"(?-i:\bOPEN\b)|\bopen\b|\baberto\b|\baberta\b|\bpendente\b|\bpend[êe]ncia\b|\bpending\b|por\s+fazer|ainda\s+n(?:ã|a)o|not\s+yet|fica(?:m)?\s+para|left\s+for|\bremains\b|\bv41[0-9]\b", re.I)
isenta = ("e21", "v407", "deixou", "dizia", "ficava", "podad", "pruned")
def segs(t): return re.split(r"[.;|\n\"«»·]", t)
def varre(nome, t, saida, doc_guarda=False):
    for seg in segs(t):
        sl = seg.lower()
        tem_fock = "fock" in sl
        tem_ou = bool(re.search(r"(?:ω|omega)[^;]{0,90}uniform", sl))
        if not (tem_fock or tem_ou): continue
        if not ruim.search(seg): continue
        if any(x in sl for x in isenta): continue
        saida.setdefault(seg.strip()[:260], set()).add(nome)
A = {}
fontes = [R + f for f in ("artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "delta_v409.py", "pos_rito/textos_v409_novo.pysnip", "pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py", "pos_rito/CUSTODIA_v409_RASCUNHO.txt")]
for p in fontes: varre(os.path.relpath(p, R), open(p, encoding="utf-8", errors="replace").read(), A)
for p in sorted(glob.glob("C:/t/h409/harness_saida_v409/textos/*.txt")): varre("harness:" + os.path.basename(p), open(p, encoding="utf-8", errors="replace").read(), A)
B = {}
for lang in ("pt", "en"):
    t = open(R + "dry_v409/dry_v409_%s.txt" % lang, encoding="utf-8", errors="replace").read()
    i = t.index("== A tradu" if lang == "pt" else "== The translation to Turing"); j = t.index("== Tetelestai", i)
    varre("artigo_%s_secao_v409" % lang, t[i:j], B)
md = open(R + "dry_v409/um_absoluto_forma_canonica.md", encoding="utf-8", errors="replace").read()
k = md.index("Tradução às classes de Turing (v409"); varre("md_linha_v409", md[k:md.index("\n", k)], B)
core = json.load(open(R + "dry_v409/core_ensaio.json", encoding="utf-8"))["core"]
for reg in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"):
    varre("core:" + reg, json.dumps(core[reg], ensure_ascii=False), B)
C = {}
for f in ("RELATORIO_PREPARACAO_v409.md", "PLANO_v409.md"): varre(f, open(R + f, encoding="utf-8").read(), C)
tot = 0
for rot, D in (("A (fontes novos e textos rendidos)", A), ("B (secao v409 do artigo, .md, core)", B), ("C (RELATORIO/PLANO)", C)):
    print("==", rot, "| segmentos:", len(D)); tot += len(D)
    for s, fs in sorted(D.items(), key=lambda x: sorted(x[1])[0]): print("   -", sorted(fs)[:4], "|", s)
json.dump({"A": {k: sorted(v) for k, v in A.items()}, "B": {k: sorted(v) for k, v in B.items()}, "C": {k: sorted(v) for k, v in C.items()}}, open(R + "revisao_terceiro/t6_varredura_independente_r3_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
