# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] REESCRITO do molde v410/comparar_v409_v410.py para uma versao SEM modulo novo: o kernel (embutidos, bandeiras, escada, ledger) IGUAL; nenhum C12 (a escada nao muda); os nos novos sao os do bloco de runtime da v411 (lidos do NOVOS_NOMES do gerador); os mexidos declarados sao a versao, o artigo PT/EN, o .md, o conversor TXT (A2), o spec da v410 (C13: pisos) e o main
"""comparar_v410_v411.py -- NADA DA v410 PERDIDO: compara, no a no (AST), a v410 SELADA (base_v410\\um.py) com o candidato v411 (ou, com V411_ENSAIO_TOPO_PROPOSTO=1, com o ARTEFATO DE ENSAIO do topo proposto, que NAO e' candidato):
todo no nomeado da v410 existe IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES, uma por no); nenhum no e' removido. Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1).
A v411 NAO tem modulo novo: _EMBEDDED_KERNEL_FILES, _LEAN_THEOREM_FLAGS, prove_external_ladder e _ESQUELETO_STONES ficam IGUAIS, e nenhum contrato que pina a escada muda (a escada e' a da v410). Os nos NOVOS sao exatamente os do
bloco de runtime da v411 (o registro com funcao h0dn_bg1_v411, o miolo _v411_*/_V411_*), LIDOS do NOVOS_NOMES do gerar_candidato_v411.py, nunca digitados. Os patches do manifesto (campo `patches`) sao mapeados aos nos que eles
mudam (PATCH_PARA_NOS): o conjunto de ids tem de ser IGUAL ao do manifesto e a uniao dos nos IGUAL aos nos mudados. O que nasceu na v410 (os quatro registros com funcao e o miolo _v410_*/_V410_*) segue IGUAL, salvo o
_V410_SPECS (C13: kh_n1_cobertura_v410 a pisos, mais a errata; veredito igual); idem o que nasceu na v409, v408, v407, v406 e v405 (iguais). Refinamentos por AST: o artigo PT/EN (o quadro antes do da v397, a remissao logo depois,
o topo e as duas trocas, a frase ao lado do estatuto e do coracao, a secao antes da da v410), o .md (o quadro e a linha), o conversor TXT (A2: uma linha antes da dissolucao das chaves) e o main (UMA instrucao, logo depois
do bloco do HMS/13 e antes de emit_figures; o selo ganha so' h0dn_bg1_v411 e registros_v411). Escreve COMPARACAO_V410_v411.json em DL.saida (no ensaio, fora de work\\, com a marca de ensaio).
uso: python -I -B -X utf8 comparar_v410_v411.py"""
import ast, copy, difflib, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(DL.CANDIDATO_ARQ, "rb").read().decode("utf-8"))
CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8"))
E_ANT, E_NOVA = CM["escada"]; NB = CM["n_bandeiras"]; NM = CM["kernel"]["modulos_novos"]
assert E_ANT == E_NOVA and NB == 0 and NM == 0, ("a v411 nao tem modulo nem bandeira nova (manifesto)", CM["escada"], NB, NM)
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
# os nos novos ESPERADOS: o NOVOS_NOMES do gerador (lido por AST do arquivo, nunca digitado) + os registros com funcao do delta
_G = ast.parse(open(os.path.join(HERE, "gerar_candidato_v411.py"), encoding="utf-8").read())
_nn = [n_ for n_ in _G.body if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == "NOVOS_NOMES" for t_ in n_.targets)]
assert len(_nn) == 1, "o NOVOS_NOMES do gerador nao foi achado uma vez"
NOVOS_ESPERADOS = set(ast.literal_eval(_nn[0].value)) | set(DL.REGISTROS_FUNCAO)
_ORDEM_MD = ast.literal_eval(repr(DL.MD_ROTULO_H0DN_V411))
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao %s -> %s" % (DL.BASE_VERSION, DL.UM_VERSION),
    "_V410_SPECS": "C13: kh_n1_cobertura_v410 h2/h3/h6 -> pisos e h8 -> tamanho minimo (a igualdade exata da v411 esta' em kh_n1_cobertura_v411), +1 errata; cunhagens_v410 nao muda; os vereditos nao mudam",
    "main": "N00/N02: UMA instrucao try/AVISO com a chamada do `h0dn_bg1_v411` e os registros por spec da v411 (`_v411_rodar_specs`), logo depois do bloco do h0dn_fontes_hms13_v410 e antes de emit_figures; o selo ganha `h0dn_bg1_v411` e `registros_v411`; nada do que existia muda",
    "build_pt": "W03/W03b/W06/W07/W08/W10/W11/W04: o quadro H0DN x BG1 antes do quadro da v397 (que fica) e a remissao logo depois dele; o paragrafo de apresentacao abre com o topo (5.1 b) e as duas trocas ditas (tambem no metodo); a frase ao lado do estatuto da prova e do coracao; a secao «O teste decisivo» antes da secao da v410",
    "build_en": "W03/W03b/W06/W07/W08/W10/W11/W05: the same in the EN article (the H0DN x BG1 box above the v397 box, the remission, the top text and the two stated swaps, the sentence beside the status of the proof and the heart, the section before the v410 one)",
    "emit_canonical_md": "W03_quadro_md/W09: o quadro H0DN x BG1 no topo do .md (antes do quadro da v397) e a linha «%s» antes da linha da IALD2 (v410)" % _ORDEM_MD,
    "_tex_to_txt": "W12 (A2 da revisao de terceiro da v410): uma linha que agrupa o expoente ^{X} de 2 ou mais caracteres como ^(X) antes de dissolver as chaves; nada mais no conversor muda",
}
# cada patch do manifesto -> os nos nomeados da base que ele muda (W02 so' ACRESCENTA nos novos: nenhum no da base)
PATCH_PARA_NOS = {"W01_versao": ["UM_VERSION"], "W03_quadro_md": ["emit_canonical_md"], "W09_md": ["emit_canonical_md"], "W12_a2_txt": ["_tex_to_txt"], "W02_runtime_v411": [],
                  "C13_specs_v410_pisos": ["_V410_SPECS"], "N00_main_h0dn_v411": ["main"], "N02_selo": ["main"]}
for _lg, _fn, _sec in (("pt", "build_pt", "PT"), ("en", "build_en", "EN")):
    for _p in ("W06_topo_", "W07_troca1_", "W03_quadro_", "W03b_remissao_", "W10_estatuto_", "W08_troca2_", "W08_troca2_metodo_", "W11_coracao_", "W13_p2_v387_"):   # (v411, aditivo da gerencia de 12/11: W13, o P2 ao lado da v387)
        PATCH_PARA_NOS[_p + _lg] = [_fn]
    PATCH_PARA_NOS["W0%s_artigo_%s" % ("4" if _lg == "pt" else "5", _sec)] = [_fn]
FUNCOES_QUE_NAO_PODEM_MUDAR = tuple(CM["gate_nao_se_move"]["funcoes_identicas_a_base"])   # lidas do manifesto (o gerador conferiu)
FUNCOES_MINIMAS = ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS")
KERNEL_IGUAL = ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "prove_external_ladder", "_ESQUELETO_STONES")   # a v411 nao tem modulo novo: os quatro nos do kernel ficam IGUAIS
MAIS_QUE_NAO_PODEM_MUDAR = KERNEL_IGUAL + ("run_um", "verify_tgl_kernel_formalization", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409", "_V409_SPECS",
                                           "iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "_v410_rodar_specs", "_V410_NOMES_REGISTROS", "_V410_REGISTROS_FUNCAO", "_v397_quadro_tex", "_v397_quadro_md")
MEXIDOS_DECLARADOS_POR_VERSAO = {"v410": {"_V410_SPECS": "C13"}, "v409": {}, "v408": {}, "v407": {}, "v406": {}, "v405": {}}


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
    if [h(x) for x in todos(A, k)] != [h(x) for x in todos(B, k)]:
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
# os nos anonimos novos esperados: so' os dois `update` que entregam as fontes e as falas da v411 ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V411_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V411_VERBATINS2)" in x for x in anon_novos_txt) == 1


# ---- nenhum contrato que pina a escada muda (a escada da v411 e' a da v410): a contagem de {'expected_ladder': E} e' a mesma, e todo no que a tem fica IGUAL
def n_escada(n):
    return sum(1 for x in ast.walk(n) if isinstance(x, ast.Dict) for k_, v_ in zip(x.keys, x.values) if isinstance(k_, ast.Constant) and k_.value == "expected_ladder" and isinstance(v_, ast.Constant) and v_.value == E_ANT)


contratos_da_escada = sorted({nm(n) for n in A.body if nm(n) and n_escada(n)})
contratos_da_escada_iguais = {k_: (k_ not in mud) for k_ in contratos_da_escada}


def pares(d):
    assert isinstance(d, ast.Dict)
    return [(k.value if isinstance(k, ast.Constant) else ast.dump(k), v) for k, v in zip(d.keys, d.values)]


def dump_eq(x, y):
    return ast.dump(x) == ast.dump(y)


def r_versao():
    return {"base_v410": ast.literal_eval(da["UM_VERSION"].value) == DL.BASE_VERSION, "candidato_v411": ast.literal_eval(db["UM_VERSION"].value) == DL.UM_VERSION}


def r_kernel():
    return {k_: bool(k_ in da and k_ in db and k_ not in mud) for k_ in KERNEL_IGUAL}


def r_specs(var_="_V410_SPECS", esperado=None):
    a, b = da[var_].value.elts, db[var_].value.elts
    out = {"mesmo_numero_de_specs": len(a) == len(b)}
    for sa_, sb_ in zip(a, b):
        pa, pb = pares(sa_), pares(sb_); ad, bd = dict(pa), dict(pb)
        nome = ast.literal_eval(ad["nome"])
        dif = [k for k, v in pa if not dump_eq(v, bd[k])]
        ca, cb = ad["checks"].elts, bd["checks"].elts
        ids = lambda es: [ast.literal_eval(pares(e)[0][1]) for e in es]
        ch_dif = [ids(ca)[i] for i in range(min(len(ca), len(cb))) if not dump_eq(ca[i], cb[i])]
        ea, eb = ad["erratas"].elts, bd["erratas"].elts
        out[nome] = {"mesmas_chaves": [k for k, _ in pa] == [k for k, _ in pb], "chaves_que_mudam": sorted(dif), "checks_com_mesmos_ids": ids(ca) == ids(cb), "checks_que_mudam": ch_dif,
                     "erratas_a_base_e_prefixo": len(eb) == len(ea) + 1 and all(dump_eq(x, y) for x, y in zip(ea, eb)), "veredito_igual": dump_eq(ad["veredito_prefixo"], bd["veredito_prefixo"]) and dump_eq(ad["veredito_sufixo"], bd["veredito_sufixo"]), "identico": dump_eq(sa_, sb_)}
    if esperado is None:
        esperado = {DL.KH_ANTERIOR: (["h2", "h3", "h6", "h8"], ["checks", "erratas"])}
    out["ok"] = bool(out["mesmo_numero_de_specs"] and set(esperado) <= set(out) and all(out[n_]["mesmas_chaves"] and out[n_]["chaves_que_mudam"] == v_[1] and out[n_]["checks_com_mesmos_ids"] and out[n_]["checks_que_mudam"] == v_[0] and out[n_]["erratas_a_base_e_prefixo"] and out[n_]["veredito_igual"] for n_, v_ in esperado.items())
                     and all(v_["identico"] for n_, v_ in out.items() if isinstance(v_, dict) and n_ not in esperado))   # (o spec que nao esta' no esperado -- cunhagens_v410 -- fica IDENTICO)
    return out


def ops_de(nome):
    a, b = da[nome].body, db[nome].body
    sm = difflib.SequenceMatcher(None, [ast.dump(x) for x in a], [ast.dump(x) for x in b], autojunk=False)
    return a, b, [op for op in sm.get_opcodes() if op[0] != "equal"]


def novos_do_candidato(nome):
    """os indices (no corpo do candidato) das instrucoes que nao estao IGUAIS na base, e as instrucoes da base que sumiram (as trocadas)."""
    a, b, ops = ops_de(nome)
    idx_b = [j for op in ops for j in range(op[3], op[4])]; idx_a = [i for op in ops for i in range(op[1], op[2])]
    return a, b, ops, idx_b, idx_a


def _txt(x):
    return ast.unparse(x)


def r_artigo(nome, lg):
    a, b, ops, ib, ia = novos_do_candidato(nome)
    tb = {j: _txt(b[j]) for j in ib}; ta = {i: _txt(a[i]) for i in ia}
    acha = lambda s_: [j for j in ib if s_ in tb[j]]
    q_ = acha("_v411_quadro_tex(core.get('h0dn_bg1_v411'), '%s'" % lg); r_ = acha("_v411_remissao_tex('%s')" % lg)
    e_ = [j for j in acha("_v411_estatuto_tex(core, '%s')" % lg) if "'\\\\item '" not in tb[j]]; c_ = [j for j in acha("_v411_estatuto_tex(core, '%s')" % lg) if "'\\\\item '" in tb[j]]
    s_ = acha("_v411_secao_tex(core, '%s'" % lg); t_ = acha("_v411_topo_texto(core, '%s')" % lg)
    p2_ = acha("_v411_p2_ao_lado_tex(core, '%s')" % lg)   # (v411, aditivo de 12/11) o P2 ao lado da v387
    f1 = acha("_v411_efeitos_tex(core, '%s')" % lg); f2 = acha("_v411_efeitos_tex(core, '%s', 'metodo')" % lg)
    v397 = "_v397_quadro_tex(core.get('teste_de_veracidade_fase9_v397'), '%s')" % lg
    vizinho = lambda j, d_: _txt(b[j + d_]) if 0 <= j + d_ < len(b) else ""
    tx1 = ("lê a razão de Hubble pelo teste acima", "Remissão expressa (registro da v410)") if lg == "pt" else ("reads the Hubble ratio through the test above", "Express remission (v410 record)")
    tx0 = ("resolve a tensão de Hubble por", "existirem na natureza segue indeterminada", "existirem na natureza não está determinada") if lg == "pt" else ("resolves the Hubble tension by", "effects exist in nature remains undetermined", "effects exist in nature is not determined")
    est_ant = "O estatuto da prova (v391)" if lg == "pt" else "The status of the proof (v391)"
    cor_ant = "Nada disto credita a gravidade quântica na natureza" if lg == "pt" else "None of this credits quantum gravity in nature"
    novas_txt = "\n".join(tb.values()); velhas_txt = "\n".join(ta.values())
    return {"nada_removido_so_insercao_ou_troca": all(op[0] in ("insert", "replace") for op in ops) and len(b) == len(a) + 6,   # (v411: +6 -- o quadro, a remissao, o estatuto, o coracao, a secao e o P2 ao lado da v387)
            "o_p2_ao_lado_uma_vez_logo_antes_da_linha_do_veredito_da_v387": len(p2_) == 1 and "TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN" in vizinho(p2_[0], 1) and "_sec3s.append" in tb[p2_[0]],
            "o_quadro_uma_vez_logo_antes_do_quadro_da_v397": len(q_) == 1 and v397 in vizinho(q_[0], 1),
            "a_remissao_uma_vez_logo_depois_do_quadro_da_v397": len(r_) == 1 and v397 in vizinho(r_[0], -1),
            "a_frase_ao_lado_do_estatuto_logo_depois_dele": len(e_) == 1 and est_ant in vizinho(e_[0], -1),
            "a_remissao_no_coracao_logo_depois_do_item_pendente": len(c_) == 1 and cor_ant in vizinho(c_[0], -1),
            "a_secao_nova_uma_vez_logo_antes_da_da_v410": len(s_) == 1 and "iald2_v410" in vizinho(s_[0], 1),
            "o_topo_abre_o_paragrafo_de_apresentacao": len(t_) == 1, "a_troca_dos_efeitos_no_paragrafo_e_no_metodo": len(f1) == 1 and len(f2) == 1,
            "a_troca_da_remissao_da_tensao": all(x_ in novas_txt for x_ in tx1) and tx0[0] in velhas_txt and tx0[0] not in novas_txt,
            "as_duas_frases_antigas_dos_efeitos_sairam": all(x_ in velhas_txt and x_ not in novas_txt for x_ in tx0[1:]),
            "n_instrucoes_novas_ou_trocadas": len(ib), "n_da_base_trocadas": len(ia)}


def r_md():
    a, b, ops, ib, ia = novos_do_candidato("emit_canonical_md")
    ok1 = len(ops) == 2 and all(op[0] == "insert" and op[4] - op[3] == 1 for op in ops)
    tb = {j: _txt(b[j]) for j in ib}
    qj = [j for j in ib if "_v411_quadro_md(core.get('h0dn_bg1_v411')" in tb[j]]; lj = [j for j in ib if DL.MD_ROTULO_H0DN_V411 in tb[j] and "_v411_linha_md(core.get('h0dn_bg1_v411'))" in tb[j]]
    return {"duas_insercoes_de_uma_instrucao_e_nada_removido": ok1, "o_quadro_logo_antes_do_quadro_da_v397": len(qj) == 1 and qj[0] + 1 < len(b) and "_v397_quadro_md(" in _txt(b[qj[0] + 1]),
            "a_linha_do_h0dn_v411_logo_antes_da_da_iald2_v410": len(lj) == 1 and lj[0] + 1 < len(b) and "IALD2 (v410" in _txt(b[lj[0] + 1])}


def r_txt():
    a, b, ops, ib, ia = novos_do_candidato("_tex_to_txt")
    ok1 = len(ops) == 1 and ops[0][0] == "insert" and ops[0][4] - ops[0][3] == 1
    t_ = _txt(b[ib[0]]) if ok1 else ""
    return {"uma_linha_inserida_e_nada_removido": ok1, "e_o_agrupamento_do_expoente": "_re.sub(" in t_ and "'^(\\\\1)'" in t_, "logo_antes_da_dissolucao_das_chaves": ok1 and ".replace('{', '').replace('}', '')" in _txt(b[ib[0] + 1])}


def r_main():
    a, b, ops = ops_de("main")
    ins = [o for o in ops if o[0] == "insert"]; rep = [o for o in ops if o[0] == "replace"]
    ok_ins = len(ins) == 1 and ins[0][4] - ins[0][3] == 1 and ins[0][1] == ins[0][2]
    txt = _txt(b[ins[0][3]]) if ok_ins else ""
    anterior = _txt(a[ins[0][1] - 1]) if ok_ins else ""
    seguinte = _txt(a[ins[0][1]]) if ok_ins else ""
    sel = {}
    if len(rep) == 1 and rep[0][2] - rep[0][1] == 1 and rep[0][4] - rep[0][3] == 1:
        sa_, sb_ = a[rep[0][1]], b[rep[0][3]]
        eh_seal = lambda s: isinstance(s, ast.Assign) and len(s.targets) == 1 and isinstance(s.targets[0], ast.Name) and s.targets[0].id == "seal" and isinstance(s.value, ast.Dict)
        if eh_seal(sa_) and eh_seal(sb_):
            pa, pb = pares(sa_.value), pares(sb_.value); ad, bd = dict(pa), dict(pb)
            novas = [k for k, _ in pb if k not in ad]
            sel = {"e_o_dict_seal": True, "chaves_da_base_preservadas_na_ordem": [k for k, _ in pb if k in ad] == [k for k, _ in pa], "valores_da_base_iguais": all(dump_eq(v, bd[k]) for k, v in pa), "chaves_novas": novas}
    return {"uma_unica_instrucao_inserida": ok_ins, "a_instrucao_chama_o_h0dn_v411_e_depois_os_specs": "h0dn_bg1_v411(core)" in txt and "_v411_rodar_specs(core)" in txt and 0 <= txt.find("h0dn_bg1_v411(core)") < txt.find("_v411_rodar_specs(core)"),
            "logo_depois_do_bloco_do_hms13_v410": "h0dn_fontes_hms13_v410(core)" in anterior or "_v410_rodar_specs" in anterior, "logo_antes_do_emit_figures": "emit_figures" in seguinte,
            "um_unico_selo_trocado": bool(sel) and sel.get("e_o_dict_seal") is True, "selo": sel,
            "o_selo_so_ganha_as_duas_chaves_da_v411": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["h0dn_bg1_v411", "registros_v411"]),
            "n_operacoes_alem_disso": len(ops) - len(ins) - len(rep)}


REFINAMENTOS = {"UM_VERSION": r_versao(), "kernel_igual": r_kernel(), "_V410_SPECS": r_specs("_V410_SPECS"), "build_pt": r_artigo("build_pt", "pt"), "build_en": r_artigo("build_en", "en"), "emit_canonical_md": r_md(), "_tex_to_txt": r_txt(),
                "main": r_main(), "contratos_da_escada_iguais": contratos_da_escada_iguais}


def tudo_verdadeiro(x):
    if isinstance(x, dict):
        return all(tudo_verdadeiro(v) for k, v in x.items() if not k.startswith("n_") and k not in ("selo", "chaves_novas", "checks_que_mudam", "chaves_que_mudam"))
    if isinstance(x, bool):
        return x
    return True


REF_OK = {k: bool(tudo_verdadeiro(v)) for k, v in REFINAMENTOS.items()}
REF_OK["_V410_SPECS"] = bool(REFINAMENTOS["_V410_SPECS"]["ok"])
REF_OK["main"] = bool(all(v for k, v in REFINAMENTOS["main"].items() if k not in ("selo", "n_operacoes_alem_disso")) and REFINAMENTOS["main"]["n_operacoes_alem_disso"] == 0)
REF_OK["contratos_da_escada_iguais"] = bool(contratos_da_escada) and all(contratos_da_escada_iguais.values())
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
intactas = {f: bool(todos(A, f) and [h(x) for x in todos(A, f)] == [h(x) for x in todos(B, f)]) for f in sorted(set(FUNCOES_QUE_NAO_PODEM_MUDAR) | set(FUNCOES_MINIMAS) | set(MAIS_QUE_NAO_PODEM_MUDAR))}
HERDADOS = {}
for v_ in ("v410", "v409", "v408", "v407", "v406", "v405"):
    nascidos = sorted(k for k in da if k.startswith("_" + v_) or k.startswith(v_ + "_") or k.endswith("_" + v_) or k.startswith("_V%s_" % v_[1:]))
    HERDADOS[v_] = {"conferidos": len(nascidos), "mexidos": [k for k in nascidos if k in mud], "declarados": MEXIDOS_DECLARADOS_POR_VERSAO[v_]}
herdados_ok = all(sorted(d_["mexidos"]) == sorted(d_["declarados"]) for d_ in HERDADOS.values())
ids_cand = sorted(p["id"] for p in CM["patches"]); ids_map = sorted(PATCH_PARA_NOS)
nos_dos_patches = sorted({n_ for v in PATCH_PARA_NOS.values() for n_ in v})
patches_ok = bool(ids_cand == ids_map and len(ids_cand) == CM["n_patches"] and nos_dos_patches == sorted(mud))
_sha_arq = hashlib.sha256(open(DL.CANDIDATO_ARQ, "rb").read()).hexdigest()[:16]
res = {"contrato": "COMPARACAO_V410_v411", **DL.MARCA_ENSAIO, "artefato": DL.ROTULO_DO_ARTEFATO, "nos_nomeados_v410": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "n_mudados": len(mud),
       "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS), "novos_nao_esperados": sorted(set(nov) - NOVOS_ESPERADOS), "esperados_ausentes": sorted(NOVOS_ESPERADOS - set(nov)),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_dois_anonimos_novos_sao_os_update_das_fontes_e_das_falas_v411": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar, "funcoes_intactas": intactas, "o_gate_nao_se_move_e_o_kernel_nao_muda": all(intactas.values()),
       "herdados": HERDADOS, "herdados_ok": herdados_ok, "contratos_da_escada": contratos_da_escada, "refinamentos": REFINAMENTOS, "refinamentos_ok": REF_OK,
       "patches": {"n_no_manifesto": CM["n_patches"], "n_mapeados": len(ids_map), "ids_so_no_manifesto": sorted(set(ids_cand) - set(ids_map)), "ids_so_no_mapa": sorted(set(ids_map) - set(ids_cand)),
                   "nos_mudados_sem_patch": sorted(set(mud) - set(nos_dos_patches)), "nos_de_patch_nao_mudados": sorted(set(nos_dos_patches) - set(mud)), "ok": patches_ok},
       "sha16": CM["sha16"], "sha16_do_arquivo": _sha_arq}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar and all(intactas.values()) and herdados_ok and patches_ok
                 and all(REF_OK.values()) and set(FUNCOES_MINIMAS) <= set(FUNCOES_QUE_NAO_PODEM_MUDAR) and _sha_arq == CM["sha16"])
_p = DL.saida("COMPARACAO_V410_v411.json")
open(_p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(_p + ".tmp", _p)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos_nao_esperados", "esperados_ausentes", "explicacao_sem_mudanca", "patches", "refinamentos_ok") else v)) for k, v in res.items() if k not in ("funcoes_intactas", "herdados", "refinamentos", "novos", "novos_esperados")}, ensure_ascii=False))
print("mudados:", sorted(mud)); print("herdados mexidos:", {k_: v_["mexidos"] for k_, v_ in HERDADOS.items()}); print("refinamentos com falha:", {k_: {kk: vv for kk, vv in (REFINAMENTOS[k_].items() if isinstance(REFINAMENTOS[k_], dict) else []) if vv is False} for k_, v_ in REF_OK.items() if not v_})
sys.exit(0 if res["ok"] else 1)
