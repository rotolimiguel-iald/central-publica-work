# -*- coding: utf-8 -*-
"""classificador_vs_fontes.py -- exame do delta v394, item A3: o classificador de auxiliares (delta19_v394.classe, ultimo componente) nao exclui
nenhuma declaracao ESCRITA A MAO nas fontes .lean dos modulos novos? E o contrario: alguma bandeira nova parece gerada pelo compilador?
So' le (audit.log da cadeia, fontes do sandbox, delta19_v394.py, FLAGS); escreve so' em v394_exame\\delta."""
import importlib.util, json, os, re, sys, collections
H = os.path.dirname(os.path.abspath(__file__))
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v394"
SB = r"C:\t\k394d\final"
spec = importlib.util.spec_from_file_location("delta19_v394", os.path.join(V, "delta19_v394.py")); d19 = importlib.util.module_from_spec(spec); spec.loader.exec_module(d19)
novos = json.load(open(os.path.join(V, "kernel_modulos_novos_v394.lista.json"), encoding="utf-8"))["novos"]
mods = {r[:-5].replace("/", "."): r for r in novos}
prov = {}
for line in open(os.path.join(V, "kernel", "audit.log"), encoding="utf-8", errors="replace"):
    if line.startswith("TGL_DECL_SOURCE\t"):
        _, n, m = line.rstrip("\n").split("\t")
        if m in mods: prov[n] = m
cls = {n: d19.classe(n) for n in prov}
aux = sorted(n for n, c in cls.items() if c != "nomeada")
# identificadores DECLARADOS a mao nas fontes (o ultimo componente do nome declarado), por modulo
KW = r"(?:theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque|axiom|example|irreducible_def|alias)"
decl_rx = re.compile(r"^[ \t]*(?:@\[[^\]]*\][ \t]*)*(?:(?:private|protected|noncomputable|partial|unsafe|nonrec|scoped|local)[ \t]+)*" + KW + r"[ \t]+([^\s:({\[⦃]+)", re.M)
campo_rx = re.compile(r"^[ \t]+([A-Za-z_][\w']*)[ \t]*:[^=]", re.M)
mao = collections.defaultdict(set); campos = collections.defaultdict(set)
for m, rel in mods.items():
    src = open(os.path.join(SB, *rel.split("/")), encoding="utf-8", errors="replace").read()
    for x in decl_rx.findall(src): mao[m].add(x.split(".")[-1].strip("«»"))
    for x in campo_rx.findall(src): campos[m].add(x)
conflito = [n for n in aux if n.split(".")[-1] in mao[prov[n]]]
conflito_campo = [n for n in aux if n.split(".")[-1] in campos[prov[n]]]
# a mesma checagem contra TODAS as fontes novas (um nome escrito a mao noutro modulo novo)
todos = set().union(*mao.values())
conflito_global = [n for n in aux if n.split(".")[-1] in todos]
# padroes de auxiliar procurados como TEXTO declarado nas fontes (qualquer modulo novo)
aux_rx = re.compile(r"\b(?:" + KW + r")[ \t]+[\w.'«»]*?(?:_proof_\d+|_simp_\d+|match_\d+|_sunfold|eq_\d+|eq_def|congr_simp)\b")
texto = []
for m, rel in mods.items():
    src = open(os.path.join(SB, *rel.split("/")), encoding="utf-8", errors="replace").read()
    for mm in aux_rx.finditer(src): texto.append("%s: %s" % (rel, mm.group(0)[:120]))
# o contrario: bandeiras novas (FLAGS) cujo ultimo componente comeca com '_' (forma de nome gerado)
F = json.load(open(os.path.join(V, "kernel", "FLAGS_v394.json"), encoding="utf-8"))
fl = F["flags"]; nomes_fl = [f[1] for f in fl]
sublinhado = sorted(n for n in nomes_fl if n.split(".")[-1].startswith("_"))
R = {"declaracoes_nos_modulos_novos": len(prov), "auxiliares": len(aux), "nomeadas": len(prov) - len(aux), "por_classe": dict(collections.Counter(cls.values())),
     "auxiliar_com_nome_escrito_a_mao_no_mesmo_modulo": conflito, "auxiliar_com_nome_de_campo_no_mesmo_modulo": conflito_campo,
     "auxiliar_com_nome_escrito_a_mao_em_algum_modulo_novo": conflito_global[:20], "n_conflito_global": len(conflito_global),
     "padrao_auxiliar_escrito_como_declaracao_nas_fontes": texto[:20],
     "bandeiras_novas": len(nomes_fl), "bandeiras_novas_com_ultimo_componente_iniciado_por_sublinhado": sublinhado[:30], "n_sublinhado": len(sublinhado)}
json.dump(R, open(os.path.join(H, "CLASSIFICADOR_VS_FONTES.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
