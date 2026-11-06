# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] NADA DA v408 PERDIDO: os nos novos da v409 (traducao_turing_v409 e o miolo _v409_*), os mexidos declarados da v408 (C12, C13) e da v407 (C12, C14, C15: a D57d), os refinamentos da secao, da linha do md, do main e do selo
"""comparar_v408_v409.py -- NADA DA v408 PERDIDO: compara, no=a=no (AST), a v408 SELADA (base_v408\\um.py) com o candidato v409: todo no nomeado da v408 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito
(nenhum: a v409 nao remove nome algum). Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so' os da v409: o registro com funcao `traducao_turing_v409` e a mecanica dele (v409_traducao_mechanics, _v409_sat) (`v408_terminal_mechanics`, 16 checagens),
o miolo (`_v408_formal`, `_v408_guarda_frases`, a constante `_V408_KB_SI_J_PER_K`), o contrato, o texto, as fontes, as falas de 04/11, os registros por spec `cunhagens_v408` e `kh_n1_cobertura_v408` e o `_v408_rodar_specs`. A v409 e' um BUNDLE PEQUENO de quatro modulos de kernel em `TGLExt/`
(TraducaoTuring, UM modulo), nao um conjunto de funcoes de pedra: nao ha funcao de pedra nova. NENHUMA CHAVE ANTIGA MUDA: nao ha patch C19/C20; testemunha_estatica_v396, v406_fechamento_mechanics e todo o miolo da v408 ficam iguais.
ADAPTADO a v409 (04/11/2026, a partir do comparar_v406_v408.py): os patches do `CANDIDATO_v409.json` (campo `patches`) sao mapeados aos nos que eles mudam (PATCH_PARA_NOS): o conjunto de ids tem de ser IGUAL ao do candidato e a uniao dos nos tem de ser IGUAL ao conjunto dos nos mudados, nem um a mais nem um a menos.
Os 26 patches `C12_expected_ladder#i` (a escada 11958 -> 12001) sao mapeados AOS NOS pela contagem das entradas `expected_ladder` da BASE na ordem do corpo (derivada do AST, nunca digitada), e cada um desses nos e' conferido: com as constantes inteiras da escada antiga trocadas pela nova, o no da base e' IGUAL ao do candidato (so' a escada muda).
O que tem de ficar IGUAL (conferido): o gate (evaluate_quantum_gravity_closure e prove_qg_closure_gate), prove_neutrino_mass_gravitational, ramo_b_preregistration_v386 e ledger_errata_v386, prove_ga_mass_audit, prove_joint_coincidence_result_v3, GA_WINDOW_STATUS, o run_um, a funcao do kernel (verify_tgl_kernel_formalization),
os registros `fechamento_v406` e `psion_canto_v407` com os seus miolos, `rede_fock_v394`, `psibit_v395`, `testemunha_estatica_v396`, `v406_fechamento_mechanics`; so' os contratos que pinam a escada (C12: `_V406_FECHO_CONTRACT`, `_V407_PSION_CONTRACT` e os anteriores) e os specs `_V407_SPECS` (C13: cunhagens_v407 +errata E21; kh_n1_cobertura_v407 h2/h3/h6/h8 -> pisos +errata) mudam.
Refinamentos (alem do no=a=no): cada no mudado de forma ESTRUTURAL (raiz e modulos embutidos, bandeiras, ledger, ext_flags, versao, main, artigo, .md, selo) e' conferido por AST: o que a base tem esta' no candidato, e o que o candidato acrescenta e' so' o declarado.
Escreve COMPARACAO_V408_v409.json. Os numeros das explicacoes sao LIDOS de CANDIDATO_v409.json e de delta_v409, nunca digitados.
uso: python -I -B -X utf8 comparar_v408_v409.py"""
import ast, copy, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8"))
E_ANT, E_NOVA = CM["escada"]; NB = CM["n_bandeiras"]; NM = CM["kernel"]["modulos_novos"]
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPL_CONTRATO = "C12: expected_ladder %d -> %d" % (E_ANT, E_NOVA)
RAIZ_REL = "TGLExt.lean"   # a chave da raiz do kernel no dict dos modulos embutidos (o unico arquivo da base que o candidato muda)
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao %s -> %s" % (DL.BASE_VERSION, DL.UM_VERSION),
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean regenerada (+ %d import do modulo novo; o Audit nao muda) e +%d modulo Lean em TGLExt/ (TraducaoTuring); nenhum arquivo da base some e nenhum muda alem da raiz" % (NM, NM),
    "_LEAN_THEOREM_FLAGS": "V01: +%d bandeiras %s0001..%s%04d (so' declaracao nomeada)" % (NB, DL.FLAG_PREFIX, DL.FLAG_PREFIX, NB),
    "prove_external_ladder": "V02: a lista ext_flags ganha as %d bandeiras (a escada %d -> %d); nada mais no corpo da funcao muda" % (NB, E_ANT, E_NOVA),
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha os %d modulos do bundle (rotulo %s)" % (NM, DL.UM_VERSION),
    "_V394_FORMAL_CONTRACT": EXPL_CONTRATO, "_V394_QUADRATIC_CONTRACT": EXPL_CONTRATO, "_V394_NETWORK_CONTRACT": EXPL_CONTRATO, "_V395_PSIBIT_CONTRACT": EXPL_CONTRATO,
    "_V396_TESTEMUNHA_CONTRACT": EXPL_CONTRATO, "_V398_SONICO_CONTRACT": EXPL_CONTRATO, "_V398_AFINACAO_CONTRACT": EXPL_CONTRATO, "_V401_FALSIDADE_CONTRACT": EXPL_CONTRATO,
    "_V402_CONTRACTS": EXPL_CONTRATO + " nos tres contratos da v402 (ponte, queda, esperanca)", "_V403_CONTRACTS": EXPL_CONTRATO + " nos tres contratos de pedra da v403 (caminho, vida, adendo da verdade; o do gate fica None)",
    "_V404_CONTRACTS": EXPL_CONTRATO + " nos dois contratos de pedra da v404 (projecao, jo8v32; o da errata de F2b fica None)", "_V405_CONTRACTS": EXPL_CONTRATO + " nos oito contratos de pedra da v405",
    "_V406_FECHO_CONTRACT": EXPL_CONTRATO + " no contrato do fechamento_v406", "_V407_PSION_CONTRACT": EXPL_CONTRATO + " no contrato do psion_canto_v407", "_V408_TERMINAL_CONTRACT": EXPL_CONTRATO + " no contrato do tetelestai_terminal_v408 (o unico contrato nascido na v408)",
    "_V408_SPECS": "C13: cunhagens_v408 ganha a errata E26 AO LADO (nenhuma checagem muda) e kh_n1_cobertura_v408 h2/h3/h6 -> pisos e h8 -> tamanho minimo (a igualdade exata da v409 esta' em kh_n1_cobertura_v409); +1 errata em cada spec; os vereditos nao mudam",
    "_V407_SPECS": "C15: cunhagens_v407 ganha a errata da D57(d) AO LADO (o insumo do acervo repinado na copia purgada; nenhuma checagem muda); kh_n1_cobertura_v407 nao muda; o veredito nao muda",
    "_V407_FONTES": "C14: D57(d) -- so' a chave psion_no_acervo_do_imac_03nov muda: a copia PURGADA (a mesma que a v408 pinou) no lugar da integra, que fica citada so' por sha16",
    "main": "N00/N02: a chamada do `traducao_turing_v409` e dos registros por spec da v409 (logo depois do bloco do tetelestai_terminal_v408 e dos specs da v408, antes de emit_figures; try/AVISO) e as chaves novas do selo (traducao_turing_v409, registros_v409); nada do que existia muda",
    "build_pt": "W04: a secao «A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala» do artigo PT, antes da secao v408 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: the section «The translation to Turing's classes: the dictionary, the lock, the reader and the tape without scale» of the EN article, before the v408 section (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «Tradução às classes de Turing (v409, 05/11/2026)» no .md canonico, antes da linha da v408 (o quadro do topo NAO muda)",
}
# cada patch do CANDIDATO_v409.json -> os nos nomeados da base que ele muda (W02 so' ACRESCENTA nos novos: nenhum no da base). Os C12_expected_ladder#i entram abaixo, derivados do AST da base.
PATCH_PARA_NOS = {"W01_versao": ["UM_VERSION"], "K00_TGLExt.lean": ["_EMBEDDED_KERNEL_FILES"], "K01_modulos_novos": ["_EMBEDDED_KERNEL_FILES"], "V01_bandeiras": ["_LEAN_THEOREM_FLAGS"], "V02_escada": ["prove_external_ladder"], "V03_ledger": ["_ESQUELETO_STONES"],
                  "W09_md": ["emit_canonical_md"], "W04_artigo_PT": ["build_pt"], "W05_artigo_EN": ["build_en"], "W02_runtime_v409": [],
                  "C13_specs_v408_E26_e_pisos": ["_V408_SPECS"], "C14_V407_FONTES_acervo_purgado": ["_V407_FONTES"], "C15_specs_v407_errata_D57d": ["_V407_SPECS"], "N00_main_traducao_turing": ["main"], "N02_selo": ["main"]}
FUNCOES_QUE_NAO_PODEM_MUDAR = tuple(CM["gate_nao_se_move"]["funcoes_identicas_a_base"])   # lidas do candidato (o gerador conferiu); abaixo, a lista minima que a v408 ja exigia
FUNCOES_MINIMAS = ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS")
MAIS_QUE_NAO_PODEM_MUDAR = ("run_um", "verify_tgl_kernel_formalization", "fechamento_v406", "_v406_formal", "_v406_chaves", "_v406_certificado_habitado", "rede_fock_v394", "psibit_v395", "_V406_FECHO_TEXT", "v406_fechamento_mechanics", "testemunha_estatica_v396",
                            "psion_canto_v407", "_v407_formal", "_v407_chaves", "_v407_elo_lido", "v407_psion_mechanics", "_V407_PSION_TEXT", "_v407_guarda_frases", "_v407_rodar_specs", "_V407_VERBATINS2",
                            "tetelestai_terminal_v408", "_v408_formal", "v408_terminal_mechanics", "_V408_TERMINAL_TEXT", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K")   # (v409: nenhuma chave antiga muda; o miolo da v408 e o da v406 seguem como estao)
NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"v409_traducao_mechanics", "_v409_formal", "_v409_guarda_frases", "_v409_sat", "_V409_TRADUCAO_CONTRACT", "_V409_TRADUCAO_TEXT", "_V409_FONTES", "_V409_VERBATINS2", "_V409_RECUSA",
                                              "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO", "_V409_SPECS", "_v409_rodar_specs"}
MEXIDOS_DA_V408_DECLARADOS = {"_V408_TERMINAL_CONTRACT": "C12", "_V408_SPECS": "C13"}   # os UNICOS nos nascidos na v408 que a v409 muda
MEXIDOS_DA_V407_DECLARADOS = {"_V407_PSION_CONTRACT": "C12", "_V407_SPECS": "C15", "_V407_FONTES": "C14"}   # os UNICOS nos nascidos na v407 que a v409 muda (C14/C15: a D57d)
MEXIDOS_DA_V406_DECLARADOS = {"_V406_FECHO_CONTRACT": "C12"}                        # o UNICO no nascido na v406 que a v409 muda (so' a escada)


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


def todos(tree, nome):
    return [n for n in tree.body if nm(n) == nome]


da = {nm(n): n for n in A.body if nm(n)}; db = {nm(n): n for n in B.body if nm(n)}
mud = []
for k in da:
    if k not in db:
        continue
    la, lb = todos(A, k), todos(B, k)
    if [h(x) for x in la] != [h(x) for x in lb]:
        mud.append(k)
ig = [k for k in da if k in db and k not in mud]
rem = [k for k in da if k not in db]; nov = sorted(k for k in db if k not in da)
anon_a = [n for n in A.body if not nm(n)]; anon_b = [n for n in B.body if not nm(n)]
sa, sb = {}, {}
for n in anon_a:
    sa.setdefault(h(n), []).append(n)
for n in anon_b:
    sb.setdefault(h(n), []).append(n)
anon_perdidos = [n for k, v in sa.items() for n in v[len(sb.get(k, [])):] if len(sb.get(k, [])) < len(v)]
anon_novos = [n for k, v in sb.items() for n in v[len(sa.get(k, [])):] if len(sa.get(k, [])) < len(v)]
anon_novos_txt = [ast.unparse(n)[:160] for n in anon_novos]
# os nos anonimos novos esperados: so' os dois `update` que entregam as fontes e as falas da v409 ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V409_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V409_VERBATINS2)" in x for x in anon_novos_txt) == 1


# ---- os 27 patches C12: a contagem das entradas {'expected_ladder': <escada antiga>} por no da BASE, na ordem do corpo (derivada do AST)
def n_escada(n):
    return sum(1 for x in ast.walk(n) if isinstance(x, ast.Dict) for k_, v_ in zip(x.keys, x.values) if isinstance(k_, ast.Constant) and k_.value == "expected_ladder" and isinstance(v_, ast.Constant) and v_.value == E_ANT)


ordem_c12 = []
for n in A.body:
    k_ = nm(n)
    if k_ and n_escada(n):
        ordem_c12 += [k_] * n_escada(n)
for i_, k_ in enumerate(ordem_c12, 1):
    PATCH_PARA_NOS["C12_expected_ladder#%d" % i_] = [k_]


def troca_escada(node):
    class T(ast.NodeTransformer):
        def visit_Constant(self, c):
            if isinstance(c.value, int) and not isinstance(c.value, bool) and c.value == E_ANT:
                return ast.copy_location(ast.Constant(E_NOVA), c)
            return c
    return T().visit(copy.deepcopy(node))


so_a_escada = {k_: bool(ast.dump(troca_escada(da[k_])) == ast.dump(db[k_])) for k_ in sorted(set(ordem_c12))}   # com a escada antiga trocada pela nova, o no da base e' IGUAL ao do candidato


# ---- refinamentos estruturais (por AST): o que a base tem esta' no candidato; o que o candidato acrescenta e' so' o declarado
def pares(d):
    assert isinstance(d, ast.Dict)
    return [(k.value if isinstance(k, ast.Constant) else ast.dump(k), v) for k, v in zip(d.keys, d.values)]


def dump_eq(x, y):
    return ast.dump(x) == ast.dump(y)


def mascara(fn, pred):
    """a funcao com o no que satisfaz `pred` trocado por um marcador; devolve (dump, [nos que satisfazem])."""
    achados = []
    c = copy.deepcopy(fn)

    class T(ast.NodeTransformer):
        def generic_visit(self, node):
            if pred(node):
                achados.append(node)
                return ast.copy_location(ast.Constant("<<MASCARA>>"), node)
            return super().generic_visit(node)
    c = T().visit(c)
    return ast.dump(c), achados


def r_versao():
    return ast.literal_eval(da["UM_VERSION"].value) == DL.BASE_VERSION and ast.literal_eval(db["UM_VERSION"].value) == DL.UM_VERSION


def r_embutidos():
    a, b = pares(da["_EMBEDDED_KERNEL_FILES"].value), pares(db["_EMBEDDED_KERNEL_FILES"].value)
    ka, kb, ad, bd = [k for k, _ in a], [k for k, _ in b], dict(a), dict(b)
    novas = [k for k in kb if k not in ad]
    mudadas = [k for k in ka if k in bd and not dump_eq(ad[k], bd[k])]
    raiz_a, raiz_b = ast.literal_eval(ad[RAIZ_REL]), ast.literal_eval(bd[RAIZ_REL])
    sufixo = DL.ROOT_SUFFIX.replace("\r\n", "\n")
    sha_novas = {k: hashlib.sha256(ast.literal_eval(bd[k]).encode("utf-8")).hexdigest() for k in novas}
    sha_ok = all(sha_novas.get(rel) == DL.BUNDLE_POR_REL[rel]["sha256"] == CM["kernel"]["bundle"][rel]["sha256"] for rel in DL.BUNDLE_RELS)
    return {"nenhum_arquivo_da_base_some": not [k for k in ka if k not in bd], "so_a_raiz_muda": mudadas == [RAIZ_REL], "ordem_da_base_preservada": [k for k in kb if k in ad] == ka,
            "novos_sao_exatamente_o_bundle": sorted(novas) == sorted(DL.BUNDLE_RELS) and len(novas) == NM, "raiz_nova_e_a_antiga_mais_os_imports": raiz_b.replace("\r\n", "\n") == raiz_a.replace("\r\n", "\n") + sufixo,
            "sha256_dos_novos_igual_ao_do_BUNDLE_e_ao_do_candidato": sha_ok, "raiz_sha16_antiga_igual_ao_candidato": hashlib.sha256(raiz_a.encode("utf-8")).hexdigest()[:16] == CM["kernel"]["raiz_v408_sha16"],
            "raiz_sha16_nova_igual_ao_candidato": hashlib.sha256(raiz_b.encode("utf-8")).hexdigest()[:16] == CM["kernel"]["raiz_sha16"]}


def r_bandeiras():
    a, b = pares(da["_LEAN_THEOREM_FLAGS"].value), pares(db["_LEAN_THEOREM_FLAGS"].value)
    ka, kb, bd = [k for k, _ in a], [k for k, _ in b], dict(b)
    novas = kb[len(ka):]
    return {"a_base_e_prefixo_igual": kb[:len(ka)] == ka and all(dump_eq(v, bd[k]) for k, v in a), "n_novas": len(novas), "n_novas_igual_ao_candidato": len(novas) == NB, "todas_com_o_prefixo_da_v409": all(k.startswith(DL.FLAG_PREFIX) for k in novas), "sem_repeticao": len(set(kb)) == len(kb)}


def r_ledger():
    a, b = da["_ESQUELETO_STONES"].value.elts, db["_ESQUELETO_STONES"].value.elts
    novas = [ast.literal_eval(x) for x in b[len(a):]]
    return {"a_base_e_prefixo_igual": len(b) >= len(a) and all(dump_eq(x, y) for x, y in zip(a, b)), "n_novas": len(novas), "n_novas_igual_ao_bundle": len(novas) == NM,
            "as_novas_sao_o_bundle_na_ordem": [t[2] for t in novas] == list(DL.BUNDLE_RELS), "rotulo_da_versao": all(t[0] == DL.UM_VERSION for t in novas)}


def r_ext_flags():
    fa, fb = da["prove_external_ladder"], db["prove_external_ladder"]
    pred = lambda n: isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "ext_flags"
    ma, aa = mascara(fa, pred); mb, bb = mascara(fb, pred)
    la, lb = aa[0].value.elts, bb[0].value.elts
    novas = [ast.literal_eval(x) for x in lb[len(la):]]
    return {"resto_da_funcao_igual": ma == mb, "uma_atribuicao_ext_flags": len(aa) == len(bb) == 1, "a_lista_antiga_e_prefixo": all(dump_eq(x, y) for x, y in zip(la, lb)) and len(lb) >= len(la), "n_novas": len(novas), "n_novas_igual_ao_candidato": len(novas) == NB, "novas_com_o_prefixo_da_v409": all(x.startswith(DL.FLAG_PREFIX) for x in novas)}


def r_specs(var_="_V408_SPECS", esperado=None):
    a, b = da[var_].value.elts, db[var_].value.elts
    out = {"mesmo_numero_de_specs": len(a) == len(b)}
    for sa_, sb_ in zip(a, b):
        pa, pb = pares(sa_), pares(sb_); ad, bd = dict(pa), dict(pb)
        nome = ast.literal_eval(ad["nome"])
        chaves_iguais = [k for k, _ in pa] == [k for k, _ in pb]
        dif = [k for k, v in pa if not dump_eq(v, bd[k])]
        ca, cb = ad["checks"].elts, bd["checks"].elts
        ids = lambda es: [ast.literal_eval(pares(e)[0][1]) for e in es]
        ch_dif = [ids(ca)[i] for i in range(min(len(ca), len(cb))) if not dump_eq(ca[i], cb[i])]
        ea, eb = ad["erratas"].elts, bd["erratas"].elts
        out[nome] = {"mesmas_chaves": chaves_iguais, "chaves_que_mudam": sorted(dif), "checks_com_mesmos_ids": ids(ca) == ids(cb), "checks_que_mudam": ch_dif, "erratas_a_base_e_prefixo": len(eb) == len(ea) + 1 and all(dump_eq(x, y) for x, y in zip(ea, eb)), "identico": dump_eq(sa_, sb_)}
    if esperado is None:
        esperado = {"cunhagens_v408": ([], ["erratas"]), "kh_n1_cobertura_v408": (["h2", "h3", "h6", "h8"], ["checks", "erratas"])}
    out["ok"] = bool(out["mesmo_numero_de_specs"] and set(esperado) <= set(out) and all(out[n_]["mesmas_chaves"] and out[n_]["chaves_que_mudam"] == v_[1] and out[n_]["checks_com_mesmos_ids"] and out[n_]["checks_que_mudam"] == v_[0] and out[n_]["erratas_a_base_e_prefixo"] for n_, v_ in esperado.items())
                     and all(v_["identico"] for n_, v_ in out.items() if isinstance(v_, dict) and n_ not in esperado))   # (v409: o spec que nao esta' no esperado fica IDENTICO)
    return out


def r_fontes407():
    """D57(d): no _V407_FONTES so' a chave do acervo muda, e para a copia purgada (o sha256 e os bytes da v408), com a integra so' por sha16."""
    fa_, fb_ = ast.literal_eval(da["_V407_FONTES"].value), ast.literal_eval(db["_V407_FONTES"].value)
    muda_ = sorted(k_ for k_ in fa_ if fa_[k_] != fb_.get(k_))
    e_ = fb_.get(DL.CHAVE_ACERVO_V407) or {}
    return {"mesmas_chaves": sorted(fa_) == sorted(fb_), "so_a_chave_do_acervo_muda": muda_ == [DL.CHAVE_ACERVO_V407], "a_nova_e_a_copia_purgada": e_.get("sha256") == DL.PURGADO_SHA256 and e_.get("arquivo") == DL.PURGADO_ARQ,
            "a_antiga_era_a_integra": (fa_.get(DL.CHAVE_ACERVO_V407) or {}).get("sha256") == DL.ORIGEM_PURGA_SHA256, "a_integra_so_por_sha16": DL.ORIGEM_PURGA_SHA16_DA_ORDEM in str(e_.get("papel")) and DL.ORIGEM_PURGA_SHA256 not in json.dumps(fb_)}


def insercoes(nome, esperadas):
    """diff por instrucao do corpo da funcao `nome`: a base e' subsequencia do candidato; `esperadas` = [(ponto,)...] verificado pelos chamadores."""
    import difflib
    a, b = da[nome].body, db[nome].body
    sm = difflib.SequenceMatcher(None, [ast.dump(x) for x in a], [ast.dump(x) for x in b], autojunk=False)
    return a, b, [op for op in sm.get_opcodes() if op[0] != "equal"]


def r_artigo(nome, secao, ancora_velha):
    a, b, ops = insercoes(nome, None)
    ok_um_insert = len(ops) == 1 and ops[0][0] == "insert" and ops[0][1] == ops[0][2]
    novas = b[ops[0][3]:ops[0][4]] if ok_um_insert else []
    txt = "\n".join(ast.unparse(x) for x in novas)
    seguinte = ast.unparse(a[ops[0][1]]) if ok_um_insert and ops[0][1] < len(a) else ""
    return {"um_unico_bloco_inserido_e_nada_removido": ok_um_insert, "n_instrucoes_inseridas": len(novas), "traz_a_secao_da_v409": secao in txt, "traz_o_registro_da_v409": "traducao_turing_v409" in txt, "a_instrucao_seguinte_e_a_da_v408": ancora_velha in seguinte}


def r_md():
    a, b, ops = insercoes("emit_canonical_md", None)
    ok1 = len(ops) == 1 and ops[0][0] == "insert" and ops[0][1] == ops[0][2] and ops[0][4] - ops[0][3] == 1
    txt = ast.unparse(b[ops[0][3]]) if ok1 else ""
    seguinte = ast.unparse(a[ops[0][1]]) if ok1 else ""
    return {"uma_linha_inserida_e_nada_removido": ok1, "traz_o_texto_da_v409": "Tradução às classes de Turing (v409" in txt, "a_linha_seguinte_e_a_da_v408": "(v408" in seguinte}


def r_main():
    a, b, ops = insercoes("main", None)
    ins = [o for o in ops if o[0] == "insert"]; rep = [o for o in ops if o[0] == "replace"]
    ok_ins = len(ins) == 1 and ins[0][4] - ins[0][3] == 1 and ins[0][1] == ins[0][2]
    txt = ast.unparse(b[ins[0][3]]) if ok_ins else ""
    anterior = ast.unparse(a[ins[0][1] - 1]) if ok_ins else ""
    seguinte = ast.unparse(a[ins[0][1]]) if ok_ins else ""
    sel = {}
    if len(rep) == 1 and rep[0][2] - rep[0][1] == 1 and rep[0][4] - rep[0][3] == 1:
        sa_, sb_ = a[rep[0][1]], b[rep[0][3]]
        eh_seal = lambda s: isinstance(s, ast.Assign) and len(s.targets) == 1 and isinstance(s.targets[0], ast.Name) and s.targets[0].id == "seal" and isinstance(s.value, ast.Dict)
        if eh_seal(sa_) and eh_seal(sb_):
            pa, pb = pares(sa_.value), pares(sb_.value); ad, bd = dict(pa), dict(pb)
            novas = [k for k, _ in pb if k not in ad]
            sel = {"e_o_dict_seal": True, "chaves_da_base_preservadas_na_ordem": [k for k, _ in pb if k in ad] == [k for k, _ in pa], "valores_da_base_iguais": all(dump_eq(v, bd[k]) for k, v in pa), "chaves_novas": novas}
    return {"um_unico_bloco_inserido": ok_ins, "o_bloco_chama_traducao_turing_v409_e_os_specs": "traducao_turing_v409(core)" in txt and "_v409_rodar_specs(core)" in txt, "logo_depois_do_bloco_da_v408": "_v408_rodar_specs" in anterior or "tetelestai_terminal_v408" in anterior,
            "logo_antes_do_emit_figures": "emit_figures" in seguinte, "um_unico_selo_trocado": bool(sel) and sel.get("e_o_dict_seal") is True, "selo": sel, "o_selo_so_ganha_as_duas_chaves_da_v409": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["traducao_turing_v409", "registros_v409"]), "n_operacoes_alem_disso": len(ops) - len(ins) - len(rep)}


REFINAMENTOS = {"UM_VERSION": r_versao(), "_EMBEDDED_KERNEL_FILES": r_embutidos(), "_LEAN_THEOREM_FLAGS": r_bandeiras(), "_ESQUELETO_STONES": r_ledger(), "prove_external_ladder": r_ext_flags(), "_V408_SPECS": r_specs("_V408_SPECS"),
                "_V407_SPECS": r_specs("_V407_SPECS", {"cunhagens_v407": ([], ["erratas"])}), "_V407_FONTES": r_fontes407(),
                "build_pt": r_artigo("build_pt", "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala", "_rg408"), "build_en": r_artigo("build_en", "The translation to Turing's classes: the dictionary, the lock, the reader and the tape without scale", "_rg408"), "emit_canonical_md": r_md(), "main": r_main(), "contratos_da_escada_so_a_escada_muda": so_a_escada}


def tudo_verdadeiro(x):
    if isinstance(x, dict):
        return all(tudo_verdadeiro(v) for k, v in x.items() if not k.startswith("n_") and k not in ("selo", "chaves_novas", "ids_que_mudam", "checks_que_mudam", "chaves_que_mudam"))
    if isinstance(x, bool):
        return x
    return True


REF_OK = {k: bool(tudo_verdadeiro(v)) for k, v in REFINAMENTOS.items()}
REF_OK["_V408_SPECS"] = bool(REFINAMENTOS["_V408_SPECS"]["ok"])
REF_OK["_V407_SPECS"] = bool(REFINAMENTOS["_V407_SPECS"]["ok"])
REF_OK["main"] = bool(all(v for k, v in REFINAMENTOS["main"].items() if k not in ("selo", "n_operacoes_alem_disso")) and REFINAMENTOS["main"]["n_operacoes_alem_disso"] == 0)
REF_OK["contratos_da_escada_so_a_escada_muda"] = bool(so_a_escada) and all(so_a_escada.values())

sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
intactas = {f: bool(todos(A, f) and [h(x) for x in todos(A, f)] == [h(x) for x in todos(B, f)]) for f in sorted(set(FUNCOES_QUE_NAO_PODEM_MUDAR) | set(FUNCOES_MINIMAS) | set(MAIS_QUE_NAO_PODEM_MUDAR))}
# TODO no que NASCEU na v408 (registro com funcao, miolo `_v408_*`, constantes `_V408_*`, a mecanica) segue IGUAL, salvo os dois declarados (C12 no contrato, C13 nos specs); idem o que nasceu na v406 (salvo C12 no contrato) e na v405 (salvo os contratos)
herdados_v408 = sorted(k for k in da if k.startswith("_v408") or k.startswith("v408_") or k.endswith("_v408") or k.startswith("_V408_"))
v408_mexidos = [k for k in herdados_v408 if k in mud]
herdados_v407 = sorted(k for k in da if k.startswith("_v407") or k.startswith("v407_") or k.endswith("_v407") or k.startswith("_V407_"))
v407_mexidos = [k for k in herdados_v407 if k in mud]
herdados_v406 = sorted(k for k in da if (k.startswith("_v406") or k.startswith("v406_") or k.endswith("_v406") or k.startswith("_V406_")))
v406_mexidos = [k for k in herdados_v406 if k in mud]
herdados_v405 = sorted(k for k in da if (k.startswith("_v405") or k.startswith("v405_") or k.endswith("_v405") or k.startswith("_V405_")) and k not in ("_V405_CONTRACTS", "_V405_SPECS"))
v405_mexidos = [k for k in herdados_v405 if k in mud]
# os patches do candidato == os patches mapeados; a uniao dos nos == os nos mudados
ids_cand = sorted(p["id"] for p in CM["patches"]); ids_map = sorted(PATCH_PARA_NOS)
nos_dos_patches = sorted({n_ for v in PATCH_PARA_NOS.values() for n_ in v})
patches_ok = bool(ids_cand == ids_map and len(ids_cand) == CM["n_patches"] and nos_dos_patches == sorted(mud))
res = {"nos_nomeados_v408": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "n_mudados": len(mud), "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_dois_anonimos_novos_sao_os_update_das_fontes_e_das_falas_v409": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar, "funcoes_intactas": intactas, "o_gate_nao_se_move_e_a_v386_nao_e_reescrita": all(intactas.values()),
       "herdados_da_v408_conferidos": len(herdados_v408), "herdados_da_v408_mexidos": v408_mexidos, "herdados_da_v408_mexidos_declarados": MEXIDOS_DA_V408_DECLARADOS, "herdados_da_v407_conferidos": len(herdados_v407), "herdados_da_v407_mexidos": v407_mexidos, "herdados_da_v407_mexidos_declarados": MEXIDOS_DA_V407_DECLARADOS, "herdados_da_v406_conferidos": len(herdados_v406), "herdados_da_v406_mexidos": v406_mexidos, "herdados_da_v406_mexidos_declarados": MEXIDOS_DA_V406_DECLARADOS,
       "herdados_da_v405_conferidos": len(herdados_v405), "herdados_da_v405_mexidos": v405_mexidos,
       "refinamentos": REFINAMENTOS, "refinamentos_ok": REF_OK,
       "patches": {"n_no_candidato": CM["n_patches"], "n_mapeados": len(ids_map), "n_C12": len(ordem_c12), "ordem_C12_derivada_do_AST": ordem_c12, "ids_so_no_candidato": sorted(set(ids_cand) - set(ids_map)), "ids_so_no_mapa": sorted(set(ids_map) - set(ids_cand)), "nos_mudados_sem_patch": sorted(set(mud) - set(nos_dos_patches)), "nos_de_patch_nao_mudados": sorted(set(nos_dos_patches) - set(mud)), "ok": patches_ok},
       "candidato_sha16": CM["sha16"]}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar and all(intactas.values()) and sorted(v408_mexidos) == sorted(MEXIDOS_DA_V408_DECLARADOS) and sorted(v407_mexidos) == sorted(MEXIDOS_DA_V407_DECLARADOS) and sorted(v406_mexidos) == sorted(MEXIDOS_DA_V406_DECLARADOS) and not v405_mexidos and patches_ok
                 and all(REF_OK.values()) and set(FUNCOES_MINIMAS) <= set(FUNCOES_QUE_NAO_PODEM_MUDAR) and hashlib.sha256(open(os.path.join(HERE, DL.CANDIDATO), "rb").read()).hexdigest()[:16] == CM["sha16"])
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V408_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos", "explicacao_sem_mudanca", "funcoes_intactas", "herdados_da_v408_mexidos", "herdados_da_v407_mexidos", "herdados_da_v406_mexidos", "herdados_da_v405_mexidos", "patches", "refinamentos_ok") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
