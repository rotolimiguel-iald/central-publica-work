# -*- coding: utf-8 -*-
"""_fix_citacoes_regra_g_v411.py -- (claude-construtor-v411, fork C, 12/11/2026; ORDEM da gerencia c1) no escopo POS-RITO do conferir_citacoes_v411.py, volta a regra (g) da v410 (conferir_citacoes_v410.py, linhas 106 a 162),
PORTADA: varre so' os arquivos de TEXTO do pos-rito da v411 (os cinco da v410 -- textos, registrar_mapa, fechar, leitura, superficies -- mais textos_custodia_handoff, blocos_custodia e o textos_v411_novo.pysnip; testes e
harnesses FORA, como na v410), com as regexes da v410 («...» e ``...'' de 8 a 700 caracteres), a limpeza da v410 (_limpa, lida do arquivo da v410 por AST, nao redigitada), o corpus LARGO (as falas OPERADOR_* das pastas de work
da v410 e as da v411, o Atlas, o um.py da base, o adendo da v410, as pedras da v410, o CLAUDE.md da casa) e a lista _ROTULOS da v410 (HERDADA: lida do arquivo da v410 por AST) mais os rotulos da v411 ACRESCENTADOS um a um,
cada um com o porque. Os mesmos saltos da v410: trecho limpo com menos de 12 caracteres, com _V410_/_V411_, com «+» (concatenacao que, em execucao, cerca um trecho VERBATIM do operador lido do arquivo por sha256: o
trecho e' conferido onde e' lido, nao no fonte) ou com «%s» (molde de formatacao). O escopo do um.py fica ESTRITO como esta'. O que sobrar e' RESIDUO: listado (arquivo, linha, citacao, se e' comentario ou texto), nunca
feito passar. Backup de BYTES antes; ancoras unicas; ast.parse. uso: python -B -X utf8 _fix_citacoes_regra_g_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_citacoes_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
PARES = [
    ('ARQS_POS_RITO = [os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "pos_rito", "*_v411*.py*")) if ".bak_" not in p_]   # (escopo b: a frente pos-rito; nao entra no candidato)\n'
     'ARQS = ["delta_v411.py", "registros_h0dn_v411.py", "registros_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py"] + [os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "pos_rito", "*_v411*.py*")) if ".bak_" not in p_]\n',
     '# (escopo b, ORDEM da gerencia c1 de 12/11: a regra (g) da v410, portada) so\' os arquivos de TEXTO do pos-rito; testes e harnesses ficam FORA da varredura, como na v410\n'
     'ARQS_POS_RITO = [os.path.join("pos_rito", n_) for n_ in ("textos_v411.py", "registrar_mapa_v411.py", "fechar_v411.py", "leitura_v411.py", "superficies_v411.py", "textos_custodia_handoff_v411.py", "blocos_custodia_v411.py", "textos_v411_novo.pysnip")]\n'
     'ARQS = ["delta_v411.py", "registros_h0dn_v411.py", "registros_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py"]   # (escopo a, o do um.py: ESTRITO, as falas da lista congelada e as ja\' seladas)\n'),
    ('out["nao_verbatim_do_um_py"] = [x_ for x_ in out["nao_verbatim"] if x_["arquivo"] not in ARQS_POS_RITO]\n'
     'out["nao_verbatim_do_pos_rito"] = [x_ for x_ in out["nao_verbatim"] if x_["arquivo"] in ARQS_POS_RITO]\n',
     '# ---- (escopo b) A REGRA (g) DA v410, PORTADA (ordem da gerencia c1, 12/11/2026): o corpus LARGO e os rotulos da cadeia\n'
     '_SRC410 = open(os.path.join(DL.V410, "conferir_citacoes_v410.py"), encoding="utf-8").read(); _TR410 = __import__("ast").parse(_SRC410)\n'
     '_NS410 = {"re": re}\n'
     'for _n410 in _TR410.body:   # (a normalizacao e a limpeza da v410, LIDAS do arquivo da v410, nao redigitadas)\n'
     '    if isinstance(_n410, __import__("ast").Assign) and getattr(_n410.targets[0], "id", None) in ("_norm", "_limpa"):\n'
     '        exec(compile(__import__("ast").get_source_segment(_SRC410, _n410), "<conferir_citacoes_v410>", "exec"), _NS410)\n'
     '_norm, _limpa = _NS410["_norm"], _NS410["_limpa"]\n'
     '_ROT410 = [__import__("ast").literal_eval(_n410.value) for _n410 in _TR410.body if isinstance(_n410, __import__("ast").Assign) and getattr(_n410.targets[0], "id", None) == "_ROTULOS" and isinstance(_n410.value, __import__("ast").Set)]\n'
     'assert len(_ROT410) == 1 and len(_ROT410[0]) > 100, "a lista _ROTULOS da v410 nao foi lida"\n'
     '# os rotulos da v411, ACRESCENTADOS um a um, cada um com o porque (titulo de secao, rotulo de linha, frase de regra da guarda, traducao seguida do original): nenhum e\' fala de ninguem\n'
     'ROTULOS_V411 = {\n'
     '}\n'
     '_ROTULOS = {x_.lower() for x_ in _ROT410[0]} | {x_.lower() for x_ in ROTULOS_V411}\n'
     '_DIRS410 = ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")\n'
     '_OPB = " || ".join(_norm(open(p_, encoding="utf-8", errors="replace").read()) for p_ in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in _DIRS410]\n'
     '                                                                                  + [glob.glob(os.path.join(DL.V410, "insumos", "cunhagens", "*OPERADOR_*.txt")), glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))\n'
     '_ATLAS = os.path.join(DL.CENTRAL, "memory", "TGL_ATLAS.md"); _ATL = re.sub(r"\\s+", " ", open(_ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(_ATLAS) else ""\n'
     '_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()\n'
     '_KERN = _norm(re.sub(r"\\s--\\s+", " ", _base.replace("**", "").replace("`", "").replace("\\\\n", " ")))\n'
     '_ADENDO = _norm(open(DL.D10.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))\n'
     '_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.D10.PEDRAS_V410 if os.path.exists(p_.get("src") or "")).replace("**", "").replace("`", ""))\n'
     '_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))\n'
     '_corpus_um = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())\n'
     '_corpus_ok = lambda fr: _corpus_um(fr) or (re.search("…|" + re.escape("[...]"), fr) is not None and all(_corpus_um(x_.strip(" .,;:")) for x_ in re.split("…|" + re.escape("[...]"), fr) if len(x_.strip(" .,;:")) >= 8))\n'
     '_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)\'\'")]\n'
     'out["nao_verbatim_do_um_py"] = list(out["nao_verbatim"])\n'
     'out["nao_verbatim_do_pos_rito"] = []; out["pos_rito_saltados"] = {"concatenacao_ou_molde": 0, "curtos_ou_nomes_de_constante": 0}; out["pos_rito_arquivos"] = {}\n'
     'for a_ in ARQS_POS_RITO:\n'
     '    p_ = os.path.join(HERE, a_)\n'
     '    if not os.path.exists(p_):\n'
     '        out["pos_rito_arquivos"][a_] = "ausente"; continue\n'
     '    t_ = open(p_, encoding="utf-8", errors="replace").read(); n_ok_ = n_tot_ = 0\n'
     '    for rx_ in _rxs:\n'
     '        for m_ in rx_.finditer(t_):\n'
     '            fr_ = _limpa(m_.group(1))\n'
     '            if "+" in fr_ or "%s" in fr_:   # (concatenacao que, em execucao, cerca um trecho VERBATIM lido do arquivo por sha256, ou molde de formatacao: conferido onde e\' lido; como na v410)\n'
     '                out["pos_rito_saltados"]["concatenacao_ou_molde"] += 1; continue\n'
     '            if len(fr_) < 12 or "_V410_" in fr_ or "_V411_" in fr_:\n'
     '                out["pos_rito_saltados"]["curtos_ou_nomes_de_constante"] += 1; continue\n'
     '            n_tot_ += 1\n'
     '            if _corpus_ok(fr_):\n'
     '                n_ok_ += 1; continue\n'
     '            lin_ = t_.count("\\n", 0, m_.start()) + 1; l_ = t_.splitlines()[lin_ - 1]\n'
     '            out["nao_verbatim_do_pos_rito"].append({"arquivo": a_, "linha": lin_, "citacao": fr_[:200], "onde": "comentario" if "#" in l_[:max(0, l_.find(m_.group(0)[:20]))] else "texto ou string do codigo"})\n'
     '    out["pos_rito_arquivos"][a_] = {"n_citacoes_conferidas": n_tot_, "n_no_corpus_ou_rotulo": n_ok_}\n'
     'out["regra_do_pos_rito"] = "a regra (g) da v410, portada (ordem da gerencia c1, 12/11): os arquivos de texto do pos-rito; regex de 8 a 700 caracteres; o corpus largo (falas, Atlas, um.py da base, adendo, pedras, CLAUDE.md); os rotulos da v410 herdados e os da v411 acrescentados com o porque"\n'
     'out["n_rotulos"] = {"v410": len(_ROT410[0]), "v411": len(ROTULOS_V411)}\n'
     'out["nao_verbatim"] = out["nao_verbatim_do_um_py"] + out["nao_verbatim_do_pos_rito"]\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_regra_g"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
