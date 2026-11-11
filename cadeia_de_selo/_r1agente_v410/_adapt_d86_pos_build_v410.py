# -*- coding: utf-8 -*-
"""_adapt_d86_pos_build_v410.py -- D86 (parte 2) no pos_build_kernel_v410.py: o bundle tem DOIS modulos (IALD2 e AEscala); as bandeiras saem em UMA serie POR MODULO (ext_iald2_410_NNNN, inalterada; ext_aescala_410_NNNN, nova), na ordem do bundle e, dentro da serie, por nome;
as ancoras conferidas sao as das duas pedras (delta_v410.ANCORAS e ANCORAS_AESCALA); o FLAGS_v410.json diz as contagens por origem e por grupo e os prefixos. Backup de bytes; trocas exatas; ast.parse; idempotente."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "pos_build_kernel_v410.py"); b0 = open(P, "rb").read(); t = b0.decode("utf-8")
if "FLAG_PREFIX_POR_MODULO" in t:
    print("pos_build_kernel_v410.py: a D86 ja' esta' aplicada"); raise SystemExit(0)
bk = P + ".bak_" + TS + "_d86"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:140]); t = t.replace(a, b)


troca("== o UNICO do delta (IALD2), sem repeticao\",", "== os DOIS do delta (IALD2 e AEscala, D86), sem repeticao\",")
troca("N_NOVOS == DL.N_BUNDLE == 1 and len(NEWMODS) == 1 and", "N_NOVOS == DL.N_BUNDLE == 2 and len(NEWMODS) == 2 and")
troca("    for n_, a_ in DL.ANCORAS.items():\n        if not (n_ in axm and set(axm[n_]) <= TRIO and srcm.get(n_) == a_[\"rel\"]):", "    for n_, a_ in list(DL.ANCORAS.items()) + list(DL.ANCORAS_AESCALA.items()):   # (D86) as ancoras das DUAS pedras\n        if not (n_ in axm and set(axm[n_]) <= TRIO and srcm.get(n_) == a_[\"rel\"]):")
troca("com proveniencia TGL_DECL_SOURCE == o modulo esperado\" % len(DL.ANCORAS), not anc_bad and len(DL.ANCORAS) == sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == DL.N_ANCORAS_ESPERADAS",
      "com proveniencia TGL_DECL_SOURCE == o modulo esperado\" % (len(DL.ANCORAS) + len(DL.ANCORAS_AESCALA)), not anc_bad and len(DL.ANCORAS) == sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == DL.N_ANCORAS_ESPERADAS and len(DL.ANCORAS_AESCALA) == DL.N_ANCORAS_AESCALA")
troca("    flags_v410 = []\n    i_ = 0\n    for rel in nov:   # `nov` esta' ordenada: (modulo, nome)\n        mod = rel[:-len(\".lean\")].replace(\"/\", \".\")\n        for n in nomeadas_por_rel[rel]:\n            i_ += 1; flags_v410.append([\"%s%04d\" % (DL.FLAG_PREFIX, i_), n, mod, DL.ORIGEM_DE_BANDEIRA])\n",
      "    flags_v410 = []\n    for rel in DL.BUNDLE_RELS:   # (D86) UMA serie POR MODULO, na ordem do bundle (IALD2, AEscala); dentro de cada serie, por nome (a da IALD2 nao muda)\n        mod = rel[:-len(\".lean\")].replace(\"/\", \".\"); i_ = 0\n        for n in nomeadas_por_rel[rel]:\n            i_ += 1; flags_v410.append([\"%s%04d\" % (DL.FLAG_PREFIX_POR_MODULO[rel], i_), n, mod, DL.ORIGEM_POR_MODULO[rel]])\n")
troca("for n_ in DL.ANCORAS}\n", "for n_ in list(DL.ANCORAS) + list(DL.ANCORAS_AESCALA)}\n")
troca("    n_por_modulo = {rel: len(nomeadas_por_rel[rel]) for rel in nov}\n",
      "    chk(\"(D86) as %d ancoras da AEscala tem bandeira da serie %s (a principal, a_escala, e as 6 de secao entre elas); as da IALD2 seguem na serie %s\" % (len(DL.ANCORAS_AESCALA), DL.FLAG_PREFIX_AESCALA, DL.FLAG_PREFIX),\n"
      "        all((chave_de.get(n_) or \"\").startswith(DL.FLAG_PREFIX_AESCALA) for n_ in DL.ANCORAS_AESCALA) and all(chave_de.get(n_) for n_ in DL.ANCORAS_PRINCIPAIS_AESCALA) and all((chave_de.get(n_) or DL.FLAG_PREFIX).startswith(DL.FLAG_PREFIX) for n_ in DL.ANCORAS), [n_ for n_ in DL.ANCORAS_AESCALA if not chave_de.get(n_)][:3])\n"
      "    n_por_modulo = {rel: len(nomeadas_por_rel[rel]) for rel in nov}\n")
troca("\"UMA serie de chaves %sNNNN, ordenada por (modulo, nome), para o(s) %d modulo(s) do bundle de TGLExt/ (decisao da gerencia c1, v410: bundle como a v409, de UM modulo; o numero e' MEDIDO do Audit desta geracao)\" % (DL.FLAG_PREFIX, N_NOVOS),",
      "\"UMA serie de chaves POR MODULO (%s), ordenada por nome, para os %d modulos do bundle de TGLExt/ (v410: IALD2, 06/11; AEscala, 09/11, D86; o numero e' MEDIDO do Audit desta geracao)\" % (\", \".join(p_ + \"NNNN\" for p_ in DL.FLAG_PREFIX_POR_MODULO.values()), N_NOVOS),")
troca("\"por_origem\": {DL.ORIGEM_DE_BANDEIRA: len(flags_v410)}, \"por_grupo_bandeiras\": {DL.GRUPO_BUNDLE: len(flags_v410)},",
      "\"por_origem\": {DL.ORIGEM_POR_MODULO[rel_]: len(nomeadas_por_rel[rel_]) for rel_ in DL.BUNDLE_RELS}, \"por_grupo_bandeiras\": {DL.GRUPO_POR_MODULO[rel_]: len(nomeadas_por_rel[rel_]) for rel_ in DL.BUNDLE_RELS}, \"prefixos\": dict(DL.FLAG_PREFIX_POR_MODULO),")
troca("(IALD2; linha Built)", "(IALD2 e AEscala; linha Built)")
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("pos_build_kernel_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| ok")
