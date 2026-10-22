# -*- coding: utf-8 -*-
"""editar_gerar_candidato.py -- DELTA 19/10: edita gerar_candidato_v394.py (backup de bytes ja' feito) para a INTEGRACAO FINAL: (1) a pedra do delta (190 modulos novos); (2) a politica de bandeiras (so' declaracao nomeada) lida de
FLAGS_v394.json; (3) os contratos do Codex seguem os do r8 (nao mais derivados das bandeiras); (4) o pino h8 = ARVORE SIMULADA do Nos; (5) C11: o token THEOREMS -> FLAGS; (6) saida em arquivo NOVO (DL.CANDIDATO). Cada troca tem assert de
unicidade. So' reescreve o gerar_candidato_v394.py (o resto da cadeia fica como esta')."""
import ast, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gerar_candidato_v394.py")
t = open(P, "rb").read().decode("utf-8")
assert "\r" not in t
n_edits = 0


def sub(old, new, count=1):
    global t, n_edits
    assert t.count(old) == count, ("troca", old[:90], t.count(old), count)
    t = t.replace(old, new); n_edits += 1


# ---- 1. imports e caminhos
sub("import registros_v394 as RG  # noqa: E402\n", "import registros_v394 as RG  # noqa: E402\nimport delta19_v394 as DL  # noqa: E402   (DELTA 19/10: a integracao final -- pedra do criterio binario, politica de bandeiras, nomes da geracao d19)\n")
sub('KD = os.path.join(HERE, "kernel"); KB = os.path.join(C, "t", "k394", "final")', 'KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX')
# ---- 2. os modulos novos: lidos da lista (189 do Codex + a pedra do delta)
sub('nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))["novos"]; assert len(nov) == 189\n',
    'nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))["novos"]; assert len(nov) == len(set(nov)) and DL.STONE_REL in nov, "a lista dos modulos novos tem de trazer a pedra do delta, sem repeticao"\n'
    'N_NOVOS = len(nov)   # LIDO da lista (189 do Codex + a pedra do delta de 19/10): nada digitado\n')
sub("    STONES_NEW[rel] = st\nfor k in (\"TGLExt.lean\", \"TGL/Audit.lean\"):\n",
    "    STONES_NEW[rel] = st\nassert STONES_NEW[DL.STONE_REL] == rd(DL.STONE_SRC), \"a pedra do sandbox difere da fonte autoral (delta_19out)\"\nfor k in (\"TGLExt.lean\", \"TGL/Audit.lean\"):\n")
sub("\"kernel embutido: +189 modulos Lean do Codex (tempo M2, RuleQuadraticResidual, 184 em F1Fecho394), do sandbox.\")",
    "\"kernel embutido: +%d modulos Lean (189 do Codex: tempo M2, RuleQuadraticResidual, 184 em F1Fecho394; e a pedra candidata do delta de 19/10), do sandbox.\" % N_NOVOS)")
sub('r8emb = ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", r8tree).value)\nassert final_emb == r8emb, "o kernel embutido da v394 difere do embutido no r8 do Codex"\n',
    'r8emb = ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", r8tree).value)\n'
    '# o esperado = o embutido do r8 do Codex + o DELTA de 19/10: a pedra, e a raiz/Audit com o import dela (delta19_v394.py define as linhas)\n'
    'exp_emb = dict(r8emb); exp_emb["TGLExt.lean"] = r8emb["TGLExt.lean"] + DL.ROOT_SUFFIX; exp_emb["TGL/Audit.lean"] = DL.AUDIT_PREFIX + r8emb["TGL/Audit.lean"]; exp_emb[DL.STONE_REL] = rd(DL.STONE_SRC)\n'
    'assert final_emb == exp_emb, "o kernel embutido da v394 difere do embutido no r8 do Codex + o delta de 19/10"\n')
# ---- 3. as bandeiras (politica so' declaracao nomeada), a escada e o ledger
sub('''r8_new = [(k, v) for k, v in r8_flags.items() if k not in old_flags]
assert sorted(r8_new) == sorted((k, n) for k, n, _ in FL), "as bandeiras novas do meu build != as do r8 (por chave e nome)"
FL_ORD = r8_new   # a ordem de insercao do Codex
''', '''r8_new = [(k, v) for k, v in r8_flags.items() if k not in old_flags]
r8_key_by_name = {v: k for k, v in r8_new}
for k_, n_, m_, o_ in FJ["flags"]:   # a POLITICA (decisao da gerencia, 19/10): so' declaracao NOMEADA; cada bandeira do Codex mantem a chave do Codex
    if o_ == "codex_nomeada":
        assert r8_key_by_name.get(n_) == k_ and DL.classe(n_) == "nomeada", ("bandeira do Codex com chave diferente do r8 ou auxiliar", k_, n_)
    elif o_ == "nomeada_sem_bandeira":
        assert n_ not in r8_key_by_name and k_.startswith(DL.PREFIXO_NOMEADA_SEM_BANDEIRA) and DL.classe(n_) == "nomeada", ("nomeada sem bandeira do Codex", k_, n_)
    else:
        assert o_ == "delta" and (k_, n_, m_) == (DL.FLAG_KEY, DL.THEOREM, DL.STONE_MOD), ("origem de bandeira desconhecida", k_, n_, o_)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v393"
FL_ORD = [(k, n) for k, n, _ in FL]   # a ordem do FLAGS_v394.json: as nomeadas do Codex na ordem de insercao dele, depois as nomeadas que ele nao marcou, depois a do delta
''')
sub('''edit(fb - 1, fb - 1, "    # v394 (19/10/2026): as pedras do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell): %d bandeiras" % len(FL_ORD) + CRLF + "".join('    "%s": "%s",%s' % (k, v, CRLF) for k, v in FL_ORD), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d." % len(FL_ORD))''',
    '''edit(fb - 1, fb - 1, "    # v394 (19/10/2026): as pedras do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell) e a pedra candidata do criterio binario de parada: %d bandeiras, SO' de declaracao NOMEADA (a pratica da v392/v393; %d do Codex, %d nomeadas que ele nao marcou, 1 do delta; as %d auxiliares geradas pelo compilador ficam fora)" % (len(FL_ORD), FJ["por_origem"]["codex_nomeada"], FJ["por_origem"]["nomeada_sem_bandeira"], FJ["excluidas_auxiliares"]["n"]) + CRLF + "".join('    "%s": "%s",%s' % (k, v, CRLF) for k, v in FL_ORD), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL_ORD))''')
sub('''assert r8lad[:len(old_lad)] == old_lad and sorted(r8lad[len(old_lad):]) == sorted(k for k, _ in FL_ORD) and len(r8lad) == len(old_lad) + len(FL_ORD)
''', '''assert r8lad[:len(old_lad)] == old_lad and {k for k, n, m, o in FJ["flags"] if o == "codex_nomeada"} <= set(r8lad[len(old_lad):]) and len(r8lad) == len(old_lad) + len(r8_new)
''')
sub('''edit(lbl, lbl, "        # v394: as pedras do Codex (%d)" % len(FL_ORD) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k in r8lad[len(old_lad):]), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL_ORD))''',
    '''edit(lbl, lbl, "        # v394: as pedras do Codex e a do delta de 19/10 (%d, so' declaracao nomeada)" % len(FL_ORD) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _ in FL_ORD), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL_ORD))''')
sub('''edit(sbl, sbl, "    # v394 (19/10/2026): as pedras do Codex" + CRLF + "".join('    ("v394", "%s", "%s", None, None),%s' % (t[1], t[2], CRLF) for t in r8_st[len(old_st):]), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % len(r8_st[len(old_st):]))
assert len(r8_st[len(old_st):]) == 189 and {t[2] for t in r8_st[len(old_st):]} == set(nov)''',
    '''st_novas = list(r8_st[len(old_st):]) + [("v394", DL.STONE_NAME, DL.STONE_REL, None, None)]   # as do Codex (189) + a pedra candidata do delta de 19/10
assert len(st_novas) == N_NOVOS and {t[2] for t in st_novas} == set(nov), "o ledger de pedras novas != a lista dos modulos novos"
edit(sbl, sbl, "    # v394 (19/10/2026): as pedras do Codex e a pedra candidata do criterio binario de parada (delta de 19/10)" + CRLF + "".join('    ("v394", "%s", "%s", None, None),%s' % (t[1], t[2], CRLF) for t in st_novas), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % len(st_novas))''')
sub("(19/10/2026): a CONSTANTE UNICA de versao -- a integracao do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell, indice qualificado) e as cunhagens de 14 a 19/10; v393 em 14/10",
    "(19/10/2026): a CONSTANTE UNICA de versao -- a integracao do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell, indice qualificado), as cunhagens de 14 a 19/10 e o criterio binario de parada (delta de 19/10); v393 em 14/10")
# ---- 4. C11: o token THEOREMS -> FLAGS (a escada conta bandeiras de declaracoes nomeadas; nem toda e' teorema)
sub('''assert not GP.violacoes(json.dumps({"e392": k2s["erratas"][-1], "e393": k3["erratas"][-1]}, ensure_ascii=False)), "P18 nas erratas novas dos specs v392/v393"
edit(s2a, s2b, pprint.pformat(specs392, width=160, sort_dicts=False).replace("\\n", CRLF), "C10_kh_n1_v392_k5", "G_CODEX_FUNCOES", "_V392_SPECS: kh_n1_cobertura_v392 k5 (== 4) -> <= 4 (+ errata); o veredito nao muda.")
''', '''assert not GP.violacoes(json.dumps({"e392": k2s["erratas"][-1], "e393": k3["erratas"][-1]}, ensure_ascii=False)), "P18 nas erratas novas dos specs v392/v393"
edit(s2a, s2b, pprint.pformat(specs392, width=160, sort_dicts=False).replace("\\n", CRLF), "C10_kh_n1_v392_k5", "G_CODEX_FUNCOES", "_V392_SPECS: kh_n1_cobertura_v392 k5 (== 4) -> <= 4 (+ errata); o veredito nao muda.")
# C11 (DELTA 19/10, decisao da gerencia): onde o texto diz THEOREMS para um conjunto que inclui nao-teoremas, diz bandeiras (FLAGS). A escada externa conta bandeiras de declaracoes nomeadas; a errata esta em kh_n1_cobertura_v394.
replace_unique("KERNEL_%d_OF_%d_THEOREMS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__", "KERNEL_%d_OF_%d_FLAGS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__", "C11_estatuto_token_flags", "G_DELTA19", "estatuto_da_prova_v391: o token KERNEL_N_OF_N_THEOREMS passa a KERNEL_N_OF_N_FLAGS (a escada conta bandeiras de declaracoes nomeadas; troca dita, errata ao lado em kh_n1_cobertura_v394).")
''')
# ---- 5. os contratos do Codex: as listas do r8 (nao mais derivadas das bandeiras, que agora sao so' as nomeadas); a proveniencia vem do Audit desta geracao
sub('''g_net = [n for _, n, m in FL if m.startswith("TGLExt.F1Fecho394.")]
assert len(g_tempo) + len(g_quad) + len(g_net) == len(FL)
''', '''g_net = [n for _, n, m in FL if m.startswith("TGLExt.F1Fecho394.")]; g_delta = [n for _, n, m in FL if m == DL.STONE_MOD]
assert len(g_tempo) + len(g_quad) + len(g_net) + len(g_delta) == len(FL) and g_delta == [DL.THEOREM], "as bandeiras nao se repartem em tempo, quadratica, rede e o delta"
PROV = FJ["proveniencia_publicas"]   # nome -> arquivo da declaracao, emitido pelo compilador (TGL_DECL_SOURCE do Audit desta geracao)
''')
sub('assert sorted(formal["theorems"]) == sorted(g_tempo)\n', 'assert set(formal["theorems"]) <= {n for n, r in PROV.items() if r in TEMPO}, "teorema do contrato de tempo sem proveniencia nos modulos de tempo"\n')
sub('assert sorted(quad["theorems"]) == sorted(g_quad)\n', 'assert set(quad["theorems"]) <= {n for n, r in PROV.items() if r in QUADF}, "teorema do contrato quadratico sem proveniencia no modulo"\n')
sub('''dsrc = {n: rel_of(m) for _, n, m in FL if m.startswith("TGLExt.F1Fecho394.")}
net = {"declarations": sorted(g_net), "declaration_sources": {n: dsrc[n] for n in sorted(g_net)},''',
    '''net_decl = sorted(net0["declarations"]); assert all(n in PROV and PROV[n].startswith("TGLExt/F1Fecho394/") for n in net_decl), "declaracao do contrato de rede sem proveniencia no Audit desta geracao"
net = {"declarations": net_decl, "declaration_sources": {n: PROV[n] for n in net_decl},''')
# ---- 6. os specs: h8 = a arvore simulada do Nos; a politica entra nos limites
sub('''specs = RG.especs(FORMAL_MAP, khj, kflags, kdecls)
''', '''# o pino h8 (achado do exame final de 19/10): o hash formal do RITO e' o sha256_directory da pasta Nos\\tgl_kernel DEPOIS da materializacao = as fontes EMBUTIDAS do candidato + os arquivos que moram na pasta e nao estao embutidos
# e que a funcao conta (_check_damming.lean; ExtrairDeps.lean sai por exclusao NOMINAL da propria funcao, que nao se altera). A funcao e' a do PROPRIO um.py (v393 base, por ast): mesma regra, mesma exclusao.
NOSK = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
_ns_h8 = {"os": os, "hashlib": hashlib}
for _nm in ("sha_file", "sha256_directory"):
    exec(compile(ast.get_source_segment(T0, top(_nm)), "<um:%s>" % _nm, "exec"), _ns_h8)
SIMD = os.path.join(HERE, "delta_19out", "arvore_simulada_h8")
if os.path.isdir(SIMD):
    shutil.rmtree(SIMD)
for rel, c_ in final_emb.items():
    p_ = os.path.join(SIMD, *rel.split("/")); os.makedirs(os.path.dirname(p_), exist_ok=True); open(p_, "w", encoding="utf-8", newline="").write(c_)
H8_EXTRAS = []
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\\\", "/")
            if rel_ not in final_emb:
                H8_EXTRAS.append(rel_); d_ = os.path.join(SIMD, *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(dp_, nm_), d_)
H8 = _ns_h8["sha256_directory"](SIMD)["files"]
assert all(H8.get(k_) == v_ for k_, v_ in FORMAL_MAP.items()) and set(H8) - set(FORMAL_MAP) <= set(H8_EXTRAS), "o hash formal simulado difere do FORMAL_MAP nos embutidos"
POL = {"n_flags": FJ["n_flags"], "n_codex_nomeadas": FJ["por_origem"]["codex_nomeada"], "n_nomeadas_sem_bandeira": FJ["por_origem"]["nomeada_sem_bandeira"], "n_excluidas": FJ["excluidas_auxiliares"]["n"],
       "n_auxiliares": FJ["excluidas_auxiliares"]["n"] + FJ["publicas_sem_bandeira"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"]}
specs = RG.especs(FORMAL_MAP, khj, kflags, kdecls, H8, POL)
''')
sub("import ast, hashlib, json, os, pprint, re, sys, importlib.util\n", "import ast, hashlib, json, os, pprint, re, shutil, sys, importlib.util\n")
# ---- 7. a saida: arquivo NOVO; o manifesto ganha a politica, o h8 e o delta
sub('out = os.path.join(HERE, "um_v394_candidato.py")', 'out = os.path.join(HERE, DL.CANDIDATO)\nassert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V394_REGERAR") == "1", "o candidato novo ja existe e difere: o candidato em exame 4022ad521dc7293d NAO e\' este arquivo; defina V394_REGERAR=1 para regerar o d19"')
sub('"kernel": {"modulos_novos": 189, "raiz_sha16"', '"kernel": {"modulos_novos": N_NOVOS, "modulos_novos_do_codex": N_NOVOS - 1, "pedra_do_delta": {"path": DL.STONE_REL, "sha16": sha16(STONES_NEW[DL.STONE_REL].encode())}, "raiz_r8_sha16": sha16(r8emb["TGLExt.lean"].encode()), "audit_r8_sha16": sha16(r8emb["TGL/Audit.lean"].encode()), "raiz_sha16"')
sub('''json.dump(man, open(os.path.join(HERE, "CANDIDATO_v394.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1)''',
    '''man["politica_de_bandeiras"] = {**POL, "n_bandeiras_sem_o_delta": POL["n_flags"] - 1, "escada_antes_da_pedra_do_delta": E393 + POL["n_flags"] - 1, "fonte": "FLAGS_v394.json (pos_build_kernel_v394.py); numeros conferidos contra o EXAME_FINAL_V394.md"}
man["h8"] = {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": H8_EXTRAS, "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"]}
man["delta19"] = {"candidato_anterior_sha16": DL.CANDIDATO_ANTERIOR_SHA16, "candidato_anterior_mantido_como_registro": True, "token_estatuto": "THEOREMS -> FLAGS (C11)", "n_cunhagens": len(verb), "registros_novos": ["criterio_binario_de_parada_v394"]}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v394.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1)''')
ast.parse(t)
open(P + ".tmp", "wb").write(t.encode("utf-8")); os.replace(P + ".tmp", P)
print("gerar_candidato_v394.py: %d trocas; ast.parse ok; %d bytes" % (n_edits, len(t.encode("utf-8"))))
