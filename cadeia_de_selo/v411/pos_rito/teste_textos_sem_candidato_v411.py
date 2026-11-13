# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-sonnet-posrito-L-v411, a servico do claude-construtor-v411] o teste de unidade dos textos da v411 SEM o core da v411 (que so' nasce no rito): monta um V e um core SINTETICOS a partir do registro offline do ensaio e exercita as funcoes de textos_v411.py
"""teste_textos_sem_candidato_v411.py -- exercita as funcoes de texto de textos_v411.py (handoff, linhagem, desenho, Atlas, core, Haja_Luz, topicos, aviso, verbete, remissivo, a secao do H0DN e o paragrafo do README) contra um CORE SINTETICO:
o core da v410 SELADA (base_v410/um_absoluto.json, so' leitura) com o registro `h0dn_bg1_v411` trocado pelo registro OFFLINE do ensaio (TESTE_H0DN_OFFLINE_v411_registro.json, o substituto do core enquanto o ensaio a seco nao existe) e os dois registros por spec da v411
como marcadores selados. O V e' montado a mao (chaves de leitura_v411.ler) com valores SINTETICOS que NAO sao da rodada (o hash do um.py, o conferidor e o sidecar sao de brinquedo; o que se testa e' a prosa e os numeros do registro). O que ele PROVA: (1) toda funcao de texto roda; (2) cada texto passa em
guarda_frases_v411.violacoes e na P18 (lista vazia); (3) os numeros que aparecem sao os do registro (o primario e as Cefeidas livres, formatados em PT); (4) a regra F67: um bloco com o Z do primario e SEM a linha das Cefeidas livres com o numero TEM de ser recusado pela guarda (controle negativo), e o bloco da moldura passa; (5) o paragrafo do README
passa em verificar_paragrafo_v411 e o numero adulterado e' recusado; (6) o cabecalho da linhagem casa com a RE_CAB da custodia (G1). O que ele NAO prova (sem o core real): a leitura da rodada (leitura_v411.ler), o ESPERADOS de verdade (so' as chaves do quadro, da v410), o sidecar e o selo reais, o quadro do paragrafo do README (o do Teste da Unica Palavra,
usa o core da v410, que e' o mesmo registro) e o stdout do rito. Nada e' escrito em lugar nenhum (sem --saida). uso: python -I -B -X utf8 teste_textos_sem_candidato_v411.py [--saida ARQ.json]   rc 0 = tudo passou."""
import copy, hashlib, json, os, re, sys, traceback
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, PK)
import delta_v411 as DL  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
from guarda_p18_v411 import violacoes as P18  # noqa: E402
import textos_v411 as T  # noqa: E402

R = {"etapas": {}, "falhas": []}
sha = lambda b: hashlib.sha256(b).hexdigest()


def etapa(nome, ok, **kw):
    R["etapas"][nome] = dict(ok=bool(ok), **kw)
    if not ok:
        R["falhas"].append(nome)
    print(("OK    " if ok else "FALHA ") + nome + ((" -- " + str(kw)[:300]) if (kw and not ok) else ""))


# ---- 1. o core sintetico, o ESPERADOS minimo (so' as chaves do quadro, da v410) e o V sintetico
OFF = json.load(open(os.path.join(PK, "TESTE_H0DN_OFFLINE_v411_registro.json"), encoding="utf-8"))
BASE_P = os.path.join(PK, "base_v410")
BASE = json.load(open(os.path.join(BASE_P, "um_absoluto.json"), encoding="utf-8"))["core"]
core = copy.deepcopy(BASE)
core[DL.FECHO_REGISTRO] = copy.deepcopy(OFF)
for n in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO):
    core[n] = {"all_verified": True, "verdict": "SINTETICO_" + n, "does_not_gate_core": True}
esp = json.load(open(os.path.join(os.path.dirname(PK), "v410", "ESPERADOS_v410.json"), encoding="utf-8"))
for k in list(esp):
    if k.startswith("vereditos_novos"):
        del esp[k]
esp["escada"] = [12308, 12308]; esp["escada_v410_e_v411"] = [12308, 12308]
esp["registros_funcao_v411"] = {"h0dn": {"nome": DL.FECHO_REGISTRO, "verdict": OFF["verdict"], "values": dict(OFF["values"]), "n_checks": 16}}   # (R1: a verificacao do paragrafo compara os values do core com os do ensaio a seco; o teste sem candidato os emula com os do registro offline)
T._CACHE["core"] = core; T._CACHE["esp"] = esp
T._bancada = lambda: {"de": "v410", "geracao": 19, "proxima": 20}   # (stub: le PINOS_BN_v411.json, que so' existe depois do pre-selo)
# a conferencia dos NOMES no um.py (T._conferir_nomes) roda contra o um.py do Nos, que ainda e' o da v410: os nomes da v411 (h0dn_bg1_v411 etc.) so' existem no um.py v411. Aqui se confere o que da' para conferir (os nomes que NAO sao da v411 existem no um.py v410 do Nos) e se pula o resto.
try:
    T._um_tem([n for n in T._NOMES_UM if "411" not in n]); _nomes_antigos_ok = True
except AssertionError as e_:   # noqa: BLE001
    _nomes_antigos_ok = str(e_)
T._CACHE["nomes_ok"] = True
# o quadro_v397.py do pacote (copia literal da v410) ainda importa delta_v410 (nao existe nesta pasta): o teste o carrega com o import trocado EM MEMORIA (o achado vai em PEDIDOS_ENTRE_FRENTES_v411.md: a copia do quadro tem de importar delta_v411)
import types
_srcq = open(os.path.join(PK, "quadro_v397.py"), encoding="utf-8").read()
_import_velho = "import delta_v410 as DL" in _srcq
_mq = types.ModuleType("quadro_v397__teste_L"); _mq.__file__ = os.path.join(PK, "quadro_v397.py")
exec(compile(_srcq.replace("import delta_v410 as DL", "import delta_v411 as DL"), _mq.__file__, "exec"), _mq.__dict__)
T._CACHE["qd"] = _mq
base_um = os.path.join(BASE_P, "um.py")
reg = lambda n, v: {"verdict": v, "ok": True}
V = {"data": "12/11/2026", "s16": "0123456789abcdef", "umb": os.path.getsize(base_um) + 4321, "base16": sha(open(base_um, "rb").read())[:16], "teor": "12308/12308", "escada_antes": 12308, "n_pedras": 0, "pedras": [], "rc": "0", "conf16": "fedcba9876543210", "conf_dm": "5/5", "conf_np": "30/30",
     "compl": "COMPLETA", "horarios": ["2026-11-12T12:00:00", "2026-11-12T14:00:00"], "selo_ts": "2026-11-12T14:00:00", "n18": 18, "n_patches": 5, "patches": "N00_main, N02_selo, W02_runtime_v411, C13_specs, K01_sem_modulos", "instalado_em": "2026-11-12 14:05:00",
     "troca_dita": [], "n_ver_mudaram": 0, "axiom_report_n": 34300, "kh": {"decl": 34300, "thm": 27381, "fora": 0, "nao_lidas": 0, "verdict": "SINTETICO"},
     "sidecar": {"ok": True, "sha256": "ab" * 32, "sha16": "ab" * 8, "bytes": 1234, "veredito": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED__SINTETICO", "esquema": "v399", "recusas": 0, "n_objetos": 3,
                 "objetos": {"um.py": {"bytes": 1, "sha256": "cd" * 32, "sha16": "cd" * 8}, "um_absoluto.json": {"bytes": 2, "sha256": "ef" * 32, "sha16": "ef" * 8}, "um_absoluto_selo.json": {"bytes": 3, "sha256": "01" * 32, "sha16": "01" * 8}}},
     "selo": {"bytes": 1, "perfil": "perfil_sintetico", "n_controles": 12}, "pilar": {"mode": "REUSE", "result16": "1" * 16}, "artigos": {"um_absoluto_pt.pdf": "a" * 16}, "servidor": "marcador de servidor parado ficou: None",
     "h_um_absoluto.json": "1" * 16, "h_um_absoluto_selo.json": "2" * 16, "h_um_absoluto_forma_canonica.md": "3" * 16, "h_um_absoluto_manifest.md": "4" * 16,
     "registros_novos": sorted([DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]),
     "reg411": {n: reg(n, core[n]["verdict"]) for n in (DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},
     "reg410_recriados": {n: dict(reg(n, (BASE.get(n) or {}).get("verdict")), sealed=True) for n in list(DL.REGISTROS_FUNCAO_V410) + ["cunhagens_v410", "kh_n1_cobertura_v410"]},
     "fecho": {"sealed": True, "ok": True, "verdict": OFF["verdict"]}}
etapa("nomes_nao_v411_de__NOMES_UM_existem_no_um_py_do_Nos_v410", _nomes_antigos_ok is True, erro=None if _nomes_antigos_ok is True else _nomes_antigos_ok)
etapa("v410_recriados_existem_no_core_base", all(n in BASE and BASE[n].get("all_verified") is True for n in V["reg410_recriados"]), n=len(V["reg410_recriados"]))

# ---- 2. os numeros do registro, independentes do T (formato PT a 2 casas)
p = OFF["values"]["primario"]; c = OFF["values"]["cefeidas_livres"]
f2 = lambda x: ("%.2f" % x).replace(".", ",").replace("-", "−")
NUM = {"zn": f2(p["z_null"]) + "σ", "zk": f2(p["z_tgl"]) + "σ", "cn": f2(c["z_null"]) + "σ", "ck": f2(c["z_tgl"]) + "σ", "D": f2(p["D"]), "ramo_p": "ramo %d" % p["ramo"], "ramo_c": "ramo %d" % c["ramo"]}
etapa("os_numeros_esperados_sao_os_do_registro", NUM["zn"] == "6,11σ" and NUM["cn"] == "4,38σ" and NUM["zk"] == "−0,61σ" and p["ramo"] == 4 and c["ramo"] == 6, **NUM)

# ---- 3. todos os textos rodam e passam nas guardas
textos = {}
def _raises(f):
    try:
        f()
    except AssertionError:
        return True
    return False


def roda(nome, f):
    try:
        t = f()
        textos[nome] = t
        return True
    except BaseException as e:   # noqa: BLE001
        etapa("roda_" + nome, False, erro=repr(e)[:300], tb=traceback.format_exc()[-400:])
        return False

QUADRO_STUB = "### O Teste da Única Palavra (v397, 23/10/2026) — parágrafo pronto (STUB do teste de unidade; o real vem de paragrafo_readme)\n\n> [stub do quadro: sem número]\n"
K = {"readme_paragrafo": QUADRO_STUB, "ap_nome": "RECIBO_SINCRONIZACAO_v411_SINTETICO.json", "ap_sha": "a" * 16, "ap_ver": "REPINADA_B20__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", "ap_evento": "evento-sintetico", "ap_bat": "BATERIA_PASSA", "par_sha": "b" * 16, "rel_sha": "c" * 16, "rel_man": "d" * 16}
par_ok = roda("paragrafo_v411", lambda: T.paragrafo_v411())
if par_ok:
    par, info = textos["paragrafo_v411"]; textos["paragrafo_v411"] = par; K["readme_paragrafo_v411"] = par
    etapa("paragrafo_v411_passa_na_verificacao_propria", T.verificar_paragrafo_v411(par, core, esp) == [], falhas=T.verificar_paragrafo_v411(par, core, esp)[:3])
FUNS = [("secao_h0dn", lambda: T.secao_h0dn(V)), ("resultado", lambda: T._resultado(V)), ("moldura", lambda: T._moldura(V)), ("ressalvas", lambda: T._ressalvas(V)), ("nao_decide", lambda: T._nao_decide(V)), ("estresses", lambda: T._estresses(V)), ("agregados", lambda: T._agregados(V)), ("origem", lambda: T._origem(V)),
        ("historia_emenda", lambda: T._historia_emenda(V)), ("atos", lambda: T._atos(V)), ("lei", lambda: T._lei(V)), ("erratas_e", lambda: T._erratas_e(V)), ("decisoes", lambda: T._decisoes(V)), ("ordem", lambda: T._ordem(V)), ("num", lambda: T._num(V)), ("cunhagens", lambda: T._cunhagens(V)),
        ("linhagem", lambda: T.linhagem(V)), ("desenho", lambda: T.desenho(V)), ("atlas", lambda: T.atlas(V)), ("core_memory", lambda: T.core_memory(V)), ("haja_luz", lambda: T.haja_luz(V)), ("topico_missao", lambda: T.topico_missao(V)), ("topico_central", lambda: T.topico_central(V)),
        ("topico_estatuto", lambda: T.topico_estatuto(V)), ("topico_novo", lambda: T.topico_novo(V)), ("aviso", lambda: T.aviso(V, "reivindicacao-sintetica")), ("arvore_linha", lambda: T.arvore_linha(V)), ("verbete", lambda: T.verbete(V)), ("remissivo", lambda: T.remissivo(V)),
        ("titulo_verbete", lambda: T.titulo_verbete(V)), ("marca_missao", lambda: T.marca_missao(V)), ("linha_handoff", lambda: T.linha_handoff(V)), ("linha_topico_novo", lambda: T.linha_topico_novo(V)), ("handoff", lambda: T.handoff(V, K))]
for nome, f in FUNS:
    roda(nome, f)
etapa("todas_as_funcoes_de_texto_rodam", all(n in textos for n, _ in FUNS) and par_ok, faltam=[n for n, _ in FUNS if n not in textos])
viol = {}
for nome, t in textos.items():
    v1 = GF.violacoes(t); v2 = P18(t); v3 = T.atribuicao_da_gerencia(t)
    if v1 or v2 or v3:
        viol[nome] = {"frases": [x[0] for x in v1][:3], "p18": [x[0] for x in v2][:3], "atribuicao": v3[:2]}
etapa("cada_texto_passa_em_guarda_frases_p18_e_atribuicao", not viol, violacoes=viol)
etapa("nenhum_token_proibido_nos_textos", not [(n, t_) for n, t in textos.items() for t_ in DL.TOKENS_PROIBIDOS_V411 if t_ in t], achados=[(n, t_) for n, t in textos.items() for t_ in DL.TOKENS_PROIBIDOS_V411 if t_ in t][:3])
etapa("nenhuma_marca_a_adaptar_nem_pendente", not [n for n, t in textos.items() if "A ADAPTAR" in t or "TEXTO_A_REESCREVER" in t])
etapa("nenhuma_frase_velha_do_h0dn_da_v410", not [n for n, t in textos.items() if DL.FRASE_H0DN_OBRIGATORIA_PT in t or DL.FRASE_H0DN_OBRIGATORIA_EN in t])
_E42 = DL.ERRATAS_V411[1]["texto"]   # (a errata E42 CITA o colchete que corrige, entre aspas: e' mencao, nao uso; sai antes de procurar)
_sem_e42 = lambda s: s.replace(_E42, " ")
etapa("nenhuma_identificacao_como_leitura_do_operador_fora_da_errata_E42_que_a_cita", not [n for n, t in textos.items() if re.search(r"(?i)leitura\s+do\s+operador|leitura\s+dele", _sem_e42(t))], achados=[n for n, t in textos.items() if re.search(r"(?i)leitura\s+do\s+operador|leitura\s+dele", _sem_e42(t))])
etapa("INFORMATIVO_o_quadro_v397_do_pacote_ainda_importa_delta_v410_ACHADO_PARA_O_CONSTRUTOR", True, import_velho=_import_velho, nota="achado, nao falha deste teste: a copia do quadro tem de importar delta_v411 (PEDIDOS_ENTRE_FRENTES_v411.md)")
etapa("a_cabeca_literal_nao_e_reproduzida", not [n for n, t in textos.items() if p["cabeca_do_teste"] in t])
etapa("beta_nunca_literal", not [n for n, t in textos.items() if re.search(r"(?<![0-9])0[.,]0120(?:3|31)\d*", t)])

# ---- 4. os numeros nos textos que trazem o resultado (as duas linhas juntas)
for nome in ("secao_h0dn", "resultado", "paragrafo_v411", "linhagem", "atlas", "handoff", "topico_novo", "core_memory"):
    t = textos.get(nome, "")
    falta = [k for k, v in NUM.items() if v not in t and not (k.startswith("ramo") and False)]
    etapa("numeros_do_registro_em_" + nome, not falta, faltam=falta)

# ---- 5. a regra F67 e o controle negativo
moldura = T._mf(V)
etapa("moldura_do_delta_traz_as_quatro_obrigacoes_e_passa", GF.violacoes(moldura) == [] and all(x in moldura for x in (DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_VALIDADE_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT)) and NUM["cn"] in moldura)
sem_cef = "No teste da razão de Hubble (H0DN × BG1), sob o modelo de erros publicado, o primário fica a %s contra o nulo; retrodição sem ajuste, teste não cego; validade, não creditação." % NUM["zn"]
r1 = [x[0] for x in GF.violacoes(sem_cef)]
etapa("controle_negativo_primario_sem_a_linha_das_cefeidas_livres_e_recusado", any(x.startswith("F67_") and "cefeidas_livres_com_o_numero" in x for x in r1), violacoes=r1)
sem_num = "No teste da razão de Hubble (H0DN × BG1), sob o modelo de erros publicado, o primário fica a %s contra o nulo; as Cefeidas livres também são lidas; retrodição sem ajuste, teste não cego; validade, não creditação." % NUM["zn"]
r2 = [x[0] for x in GF.violacoes(sem_num)]
etapa("controle_negativo_cefeidas_livres_sem_o_numero_e_recusado", any(x.startswith("F67_") and "cefeidas_livres_com_o_numero" in x for x in r2), violacoes=r2)
sem_modelo = "No teste da razão de Hubble (H0DN × BG1) o primário fica a %s contra o nulo; as Cefeidas livres leem %s; retrodição sem ajuste, teste não cego; validade, não creditação." % (NUM["zn"], NUM["cn"])
r3 = [x[0] for x in GF.violacoes(sem_modelo)]
etapa("controle_negativo_sem_o_modelo_de_erros_publicado_e_recusado", any(x.startswith("F67_") and "modelo_publicado" in x for x in r3), violacoes=r3)
sem_val = "No teste da razão de Hubble (H0DN × BG1), sob o modelo de erros publicado, o primário fica a %s contra o nulo; as Cefeidas livres leem %s; retrodição sem ajuste, teste não cego." % (NUM["zn"], NUM["cn"])
r4 = [x[0] for x in GF.violacoes(sem_val)]
etapa("controle_negativo_sem_validade_nao_creditacao_e_recusado", any(x.startswith("F67_") and "validade_nao_creditacao" in x for x in r4), violacoes=r4)
etapa("forma_certa_passa", GF.violacoes("No teste da razão de Hubble (H0DN × BG1), sob o modelo de erros publicado, o primário fica a %s contra o nulo; as Cefeidas livres leem %s; retrodição sem ajuste, teste não cego; validade, não creditação." % (NUM["zn"], NUM["cn"])) == [])

# ---- 6. o paragrafo do README: numero adulterado e frase removida sao recusados
if par_ok:
    par = textos["paragrafo_v411"]
    adult = par.replace(NUM["zn"], "6,99σ", 1)
    etapa("controle_negativo_paragrafo_com_o_z_adulterado_e_recusado", T.verificar_paragrafo_v411(adult, core, esp) != [])
    sem_ress = par.replace("As sete ressalvas, ditas", "As ressalvas", 1)
    etapa("controle_negativo_paragrafo_sem_as_sete_ressalvas_e_recusado", T.verificar_paragrafo_v411(sem_ress, core, esp) != [])
    etapa("paragrafo_nao_traz_o_4_44", not re.search(r"4[,.]44|z_disc", par))

# ---- 7. o conteudo da v411 esta nos textos e o da v410 nao e' dito como novo
dec = textos.get("decisoes", ""); er = textos.get("erratas_e", ""); ho = textos.get("handoff", "")
etapa("decisoes_e_erratas_do_delta_no_diario", all(k in textos.get("linhagem", "") for k in list(DL.DECISOES_V411) + list(DL.ERRATAS_IDS_V411)), decisoes=list(DL.DECISOES_V411))
etapa("as_sete_ressalvas_por_rotulo_no_handoff", all(r in ho for r in DL.RESSALVAS_ROTULOS_PT), faltam=[r for r in DL.RESSALVAS_ROTULOS_PT if r not in ho])
etapa("o_que_o_teste_nao_decide_no_handoff", all(re.sub(r"\s+", " ", x) in ho for x in OFF["o_que_o_teste_nao_decide"]))
etapa("handoff_nao_traz_os_blocos_da_custodia", not any(x in ho for x in ("NOTA_EN_v411", "README_FRENTE", "README_O_QUE_SAI", "ESTATUTO_P2_", "INICIO_NOTA_EN")))
etapa("handoff_diz_os_registros_da_v410_como_recriados", all(n in ho for n in DL.REGISTROS_FUNCAO_V410) and "RECRIADOS" in ho)
etapa("kernel_sem_modulo_novo_dito", "nenhum módulo novo" in textos.get("linhagem", "") and "nenhuma bandeira nova" in textos.get("linhagem", ""))
etapa("linhagem_sem_as_secoes_da_v410", not any(x in textos.get("linhagem", "") for x in ("### A escala", "recibo documental HMS/13 (D80)", "O teste pré-registrado da razão de Hubble (H0DN × BG1) (v411")))
etapa("secao_aescala_falha_a_vista", _raises(lambda: T.secao_aescala(V)))

# ---- 8. o cabecalho da linhagem casa com a RE_CAB da custodia (G1)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(PK))), "tools"))
    from custodia_g1 import nos as NOSMOD  # noqa: E402
    cab = textos["linhagem"].split("\n")[0]
    m = NOSMOD.RE_CAB.match(cab + "\n")
    etapa("cabecalho_da_linhagem_casa_com_a_RE_CAB_da_custodia", bool(m) and m.group("v") == "v411" and m.group("k") in ("0", "nenhum") and int(m.group("a")) == int(m.group("b")) == 12308, cabecalho=cab[:200], grupos=(m.groupdict() if m else None))
    mo = NOSMOD.RE_OQUEE.search(ho)
    etapa("o_que_e_do_handoff_casa_com_a_RE_OQUEE_da_custodia", bool(mo) and mo.group("v") == "v411" and mo.group("ant") == "v410", achou=bool(mo))
except Exception as e:   # noqa: BLE001
    etapa("custodia_g1_importavel_para_a_RE_CAB", False, erro=repr(e)[:200])

# ---- 8b. a LEITURA da rodada: as funcoes novas de leitura_v411.py (_ler_fecho_v411, _ler_recriados_v410, _ler_specs_v411) contra o mesmo core sintetico (o ler() inteiro precisa do Nos real e de ESPERADOS: fica sem teste aqui)
import leitura_v411 as LV
GATE = OFF["values"]["gate_verdict"]
ESPL = {"vereditos_novos_v411": {DL.FECHO_REGISTRO: OFF["verdict"], DL.CUNHAGENS_REGISTRO: "TGL_CUNHAGENS_V411__SINTETICO", DL.KH_REGISTRO: "TGL_KH_N1_COBERTURA_V411__SINTETICO"},
        "registros_funcao_v411": {"h0dn": {"nome": DL.FECHO_REGISTRO, "verdict": OFF["verdict"], "values": {k: OFF["values"][k] for k in LV.H0_VALUES_COMPARADOS if k in OFF["values"]}, "n_checks": 16}},
        "qg_closure_gate_verdict_v410": GATE, "escada": [12308, 12308], "escada_v410_e_v411": [12308, 12308], "vereditos_v410": {n: (BASE.get(n) or {}).get("verdict") for n in list(DL.REGISTROS_FUNCAO_V410) + ["cunhagens_v410", "kh_n1_cobertura_v410"]}, "troca_dita": []}
SELOL = {"qg_closure_verdict": GATE, DL.FECHO_REGISTRO: {k: OFF.get(k) for k in LV.H0_SELO_CHAVES}}


def stdout_de(r):
    pp = r["values"]["primario"]; cc = r["values"]["cefeidas_livres"]
    return ("H0DN x BG1 ABERTO [v411 -- D169, sintetico]\n  primario (modelo publicado): Z nulo = %s ; Z K = %s ; ramo %s  ||  Cefeidas livres (ao lado, no mesmo item): Z nulo = %s ; Z K = %s ; ramo %s  ||  checagens ok = 16/16 ; gate = o mesmo da base\n  >>> %s <<<\n"
            % (pp.get("z_null"), pp.get("z_tgl"), pp.get("ramo"), cc.get("z_null"), cc.get("z_tgl"), cc.get("ramo"), r["verdict"]))


BETA = OFF["values"]["beta"]
F0, P0 = LV._ler_fecho_v411({DL.FECHO_REGISTRO: OFF}, ESPL, {}, SELOL, stdout_de(OFF), DL, GF, P18, BETA)
etapa("leitura_fecho_v411_le_o_registro_offline_sem_problema", P0 == [] and F0["sealed"] is True and F0["n_checks"] == 16 and F0["duas_linhas_ok"] and F0["ressalvas_ok"] and F0["stdout_ok"] and F0["selo_ok"] and F0["guarda_ok"] and F0["gate_ok"] and F0["pinos_ok"], problemas=P0, flags={k: F0.get(k) for k in ("sealed", "mech_ok", "values_ok", "duas_linhas_ok", "ressalvas_ok", "stdout_ok", "selo_ok", "guarda_ok", "gate_ok", "pinos_ok", "emenda_ok")})
etapa("leitura_fecho_v411_chaves_de_V_fecho", all(k in F0 for k in ("primario", "cefeidas_livres", "atos", "ressalvas", "nao_decide", "lei_em_km_s_Mpc", "cabeca_do_teste", "outcome", "verdict", "n_insumos")) and F0["primario"]["z_null"] == p["z_null"] and F0["cefeidas_livres"]["ramo"] == 6 and len(F0["ressalvas"]) == 7 and len(F0["nao_decide"]) == 5)


def mutar(f):
    r = copy.deepcopy(OFF); f(r); return r


def neg(nome, f, st=None, esp=None):
    r = mutar(f)
    Fn, Pn = LV._ler_fecho_v411({DL.FECHO_REGISTRO: r}, esp or ESPL, {}, SELOL, st if st is not None else stdout_de(r), DL, GF, P18, BETA)
    etapa("leitura_fecho_v411_controle_negativo_" + nome, bool(Pn) and Fn["sealed"] is False, problemas=len(Pn))


neg("z_do_primario_adulterado", lambda r: r["values"]["primario"].__setitem__("z_null", r["values"]["primario"]["z_null"] + 0.5))
neg("nao_aberto_uma_vez", lambda r: r.__setitem__("opened_once", False))
neg("uma_ressalva_a_menos", lambda r: r["ressalvas_secao8"].pop())
neg("checagem_falsa", lambda r: r["mechanics"]["checks"][5].__setitem__("ok", False))
neg("linha_das_cefeidas_livres_sem_o_ramo", lambda r: r["values"]["cefeidas_livres"].pop("ramo"))
neg("z_nao_finito", lambda r: r["values"]["primario"].__setitem__("z_null", float("nan")))
neg("token_proibido_no_texto", lambda r: r["limites"].append("a TGL foi CONFIRMED pela natureza"))
neg("frase_velha_da_v410_no_texto", lambda r: r["limites"].append(DL.FRASE_H0DN_OBRIGATORIA_PT))
neg("beta_adulterado", lambda r: r["values"].__setitem__("beta", r["values"]["beta"] * 1.001))
Fn, Pn = LV._ler_fecho_v411({DL.FECHO_REGISTRO: OFF}, ESPL, {}, SELOL, stdout_de(OFF).replace(str(p["z_null"]), "6.0"), DL, GF, P18, BETA)
etapa("leitura_fecho_v411_controle_negativo_stdout_com_numero_diferente", bool(Pn) and Fn["stdout_ok"] is False)
Fn, Pn = LV._ler_fecho_v411({DL.FECHO_REGISTRO: OFF}, {k: v for k, v in ESPL.items() if k != "registros_funcao_v411"}, {}, SELOL, stdout_de(OFF), DL, GF, P18, BETA)
etapa("leitura_fecho_v411_controle_negativo_ESPERADOS_sem_o_ensaio_a_seco_do_h0dn_e_recusado", bool(Pn))
Fn, Pn = LV._ler_fecho_v411({DL.FECHO_REGISTRO: OFF}, ESPL, {}, {"qg_closure_verdict": GATE}, stdout_de(OFF), DL, GF, P18, BETA)
etapa("leitura_fecho_v411_controle_negativo_selo_sem_o_resumo", bool(Pn) and Fn["selo_ok"] is False)
# os registros da v410 recriados
Pr = []
base_rec = copy.deepcopy(BASE)
errata_pisos = {"ao_lado_de": "kh_n1_cobertura_v410 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)", "assinatura": DL.ASSINA, "dizia": "x", "agora": "y"}
base_rec.setdefault("kh_n1_cobertura_v410", {}).setdefault("erratas", []).append(errata_pisos)
rec = LV._ler_recriados_v410(base_rec, BASE, ESPL, Pr)
etapa("leitura_recriados_v410_seis_selados_com_a_errata_dos_pisos", Pr == [] and sorted(rec) == sorted(LV.REG_RECRIADOS_V410) and all(rec[k]["sealed"] for k in LV.REG_RECRIADOS_V410) and rec["kh_n1_cobertura_v410"]["errata_dos_pisos"] is True, problemas=Pr)
Pr2 = []; LV._ler_recriados_v410(BASE, BASE, ESPL, Pr2)
etapa("leitura_recriados_v410_controle_negativo_sem_a_errata_dos_pisos_e_recusado", len(Pr2) == 1 and "errata" in Pr2[0])
b2 = copy.deepcopy(base_rec); b2["iald2_v410"]["verdict"] = "OUTRO"; Pr3 = []; LV._ler_recriados_v410(b2, BASE, ESPL, Pr3)
etapa("leitura_recriados_v410_controle_negativo_veredito_diferente_da_v410_e_recusado", any("iald2_v410" in x for x in Pr3))
b3 = copy.deepcopy(base_rec); del b3["h0dn_fontes_hms13_v410"]; Pr4 = []; LV._ler_recriados_v410(b3, BASE, ESPL, Pr4)
etapa("leitura_recriados_v410_controle_negativo_registro_ausente_e_recusado", any("h0dn_fontes_hms13_v410" in x for x in Pr4))
# os dois por spec da v411
# (R1, D181) as falas entram CITADAS (data, sha256, papel, autor); sem texto, sem trecho, sem o nome do arquivo
_CIT = {"v411_cun_" + c["sha256"][:16]: {"sha256": c["sha256"], "quando": c["quando"], "papel": c["papel"], "autor": c["autor"]} for c in DL.FALAS_CITADAS_V411}
ESPL["cunhagens"] = dict(_CIT)
cu = {"all_verified": True, "does_not_gate_core": True, "verdict": ESPL["vereditos_novos_v411"][DL.CUNHAGENS_REGISTRO], "checks": [{"id": "u1", "ok": True}],
      "verbatim": {k_: dict(v_, citado_por_sha256=True, texto_transcrito=False) for k_, v_ in _CIT.items()},
      "erratas": [{"agora": e["texto"], "assinatura": DL.ASSINA, "ao_lado_de": e["ao_lado_de"]} for e in DL.ERRATAS_V411] + [{"agora": "a v411 nao acrescenta modulo", "assinatura": DL.ASSINA, "ao_lado_de": "kh_n1_cobertura_v410 (h2/h3/h6)"}],
      "extras": {"n_falas": DL.N_FALAS_V411, "autores": {k_: "operador" for k_ in _CIT}, "falas_citadas": [dict(v_, chave=k_) for k_, v_ in _CIT.items()], "decisoes": dict(DL.DECISOES_V411), "erratas_ids": list(DL.ERRATAS_IDS_V411), "ressalvas_rotulos": list(DL.RESSALVAS_ROTULOS_PT),
                 "textos_da_gerencia_citados": [{"nome": g["nome"], "sha256": g["sha256"]} for g in DL.TEXTOS_DA_GERENCIA_CITADOS], "assinatura_das_erratas": DL.ASSINA,
                 "alcance_de_p_igual_np": "P = nP " + DL.D10.FRASE_QUALIFICADOR_PT},
      "leituras_do_operador": [], "estatuto": "[REAL] sintetico", "limites": ["[REAL] sintetico"], "diz": ["sintetico"], "nao_diz": ["sintetico"], "scope": "sintetico"}
kh_r = {"all_verified": True, "does_not_gate_core": True, "verdict": ESPL["vereditos_novos_v411"][DL.KH_REGISTRO], "checks": [{"id": "h1", "ok": True}], "estatuto": "[REAL] sintetico", "limites": ["[REAL] sintetico"], "diz": ["s"], "nao_diz": ["s"], "scope": "s"}
core_s = {DL.CUNHAGENS_REGISTRO: cu, DL.KH_REGISTRO: kh_r, DL.FECHO_REGISTRO: OFF}
Ps = []; Vc, khok = LV._ler_specs_v411(core_s, ESPL, DL, GF, Ps)
etapa("leitura_specs_v411_cunhagens_e_kh_sinteticos_sem_problema", Ps == [] and Vc["ok"] and khok and Vc["n"] == DL.N_FALAS_V411 and Vc["n_erratas"] == len(DL.ERRATAS_V411) + 1 and Vc["n_decisoes"] == len(DL.DECISOES_V411), problemas=Ps, vc={k: Vc.get(k) for k in ("ok", "verbatim_ok", "erratas_ok", "decisoes_ok", "ressalvas_ok", "contagens_ok", "alcance_ok", "sem_leitura_ok", "moldura_ok")})
c2 = copy.deepcopy(core_s); c2[DL.CUNHAGENS_REGISTRO]["extras"]["decisoes"].pop("D170"); Ps2 = []; LV._ler_specs_v411(c2, ESPL, DL, GF, Ps2)
etapa("leitura_specs_v411_controle_negativo_decisao_a_menos_e_recusada", bool(Ps2))
c3 = copy.deepcopy(core_s); c3[DL.CUNHAGENS_REGISTRO]["erratas"].pop(1); Ps3 = []; LV._ler_specs_v411(c3, ESPL, DL, GF, Ps3)
etapa("leitura_specs_v411_controle_negativo_errata_a_menos_e_recusada", bool(Ps3))
c4 = copy.deepcopy(core_s); c4[DL.CUNHAGENS_REGISTRO]["leituras_do_operador"] = ["uma leitura"]; Ps4 = []; LV._ler_specs_v411(c4, ESPL, DL, GF, Ps4)
etapa("leitura_specs_v411_controle_negativo_leitura_do_operador_no_registro_novo_e_recusada", bool(Ps4))

# ---- 8c. o fechar e as superficies: o CODIGO das guardas do handoff (fechar_v411.py) e da guarda das superficies (superficies_v411.py) executado sobre os textos renderizados (os scripts inteiros escrevem no Nos e na memoria: nao rodam aqui)
_src_f = open(os.path.join(HERE, "fechar_v411.py"), encoding="utf-8").read()
_a = _src_f.index("# v411 (12/11, D169): o handoff DIZ o registro com funcao"); _b = _src_f.index("assert not _vt411"); _b = _src_f.index("\n", _b)
_guardas_fechar = _src_f[_a:_b]


def roda_guardas_fechar(doc_):
    ns_ = {"doc": doc_, "DLF": DL, "_hc": OFF}
    try:
        exec(compile(_guardas_fechar, "fechar_v411.guardas_do_handoff", "exec"), ns_)
        return True, ""
    except AssertionError as e_:
        return False, str(e_)[:200]


ok_f, msg_f = roda_guardas_fechar(ho)
etapa("guardas_do_handoff_do_fechar_passam_no_handoff_renderizado", ok_f, msg=msg_f)
etapa("controle_negativo_fechar_recusa_handoff_sem_uma_ressalva", roda_guardas_fechar(ho.replace(DL.RESSALVAS_ROTULOS_PT[3], "xxx"))[0] is False)
etapa("controle_negativo_fechar_recusa_handoff_com_a_frase_velha_da_v410", roda_guardas_fechar(ho + "\n" + DL.FRASE_H0DN_OBRIGATORIA_PT)[0] is False)
etapa("controle_negativo_fechar_recusa_handoff_sem_o_registro_novo", roda_guardas_fechar(ho.replace(DL.FECHO_REGISTRO, "xxx"))[0] is False)
etapa("controle_negativo_fechar_recusa_handoff_sem_o_que_o_teste_nao_decide", roda_guardas_fechar(ho.replace(OFF["o_que_o_teste_nao_decide"][2], "xxx"))[0] is False)
_src_s = open(os.path.join(HERE, "superficies_v411.py"), encoding="utf-8").read()
_a = _src_s.index("def h0dn_sem_obrigacao(texto):"); _b = _src_s.index("def guarda(texto, onde):")
_ns_s = {"re": re}
exec(compile(_src_s[_a:_b], "superficies_v411.guardas", "exec"), _ns_s)
etapa("superficies_guarda_da_frase_velha_do_h0dn_recusa_a_frase_da_v410", bool(_ns_s["h0dn_sem_obrigacao"]("O teste H0DN x BG1 esta " + DL.FRASE_H0DN_OBRIGATORIA_PT)) and _ns_s["h0dn_sem_obrigacao"]("O teste H0DN x BG1 foi aberto uma vez.") == [] and _ns_s["h0dn_sem_obrigacao"]("sem o assunto") == [])
etapa("superficies_guarda_nao_acusa_os_textos_da_v411", all(_ns_s["h0dn_sem_obrigacao"](t_) == [] and _ns_s["hms13_sem_obrigacao"](t_) == [] and _ns_s["clay_sem_forma"](t_) == [] for t_ in textos.values()), achados=[n_ for n_, t_ in textos.items() if _ns_s["h0dn_sem_obrigacao"](t_) or _ns_s["hms13_sem_obrigacao"](t_) or _ns_s["clay_sem_forma"](t_)])

# ---- 8d. as linhas do STDOUT que a leitura espera: as regexes (copiadas do codigo de leitura_v411.py, sem retoque) contra o stdout REAL do rito da v410 selada (Nos\rodada_v410_stdout.txt, so' leitura), que o main da v411 repete; e a linha [v411] contra uma linha sintetica
_nos_std = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(PK)))), "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "rodada_v410_stdout.txt")
if not os.path.isfile(_nos_std):
    _nos_std = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "rodada_v410_stdout.txt")
_out_real = open(_nos_std, encoding="utf-8", errors="replace").read()
_src_l = open(os.path.join(HERE, "leitura_v411.py"), encoding="utf-8").read().split("\n")


def _regex_da_leitura(var):
    ls_ = [l_ for l_ in _src_l if l_.lstrip().startswith(var + " = re.search(")]
    assert len(ls_) == 1, (var, len(ls_))
    return ls_[0].strip()


def _acha(var, out_text, extra=None):
    ns_ = {"re": re, "out": out_text, "out_n_": out_text.replace("\r\n", "\n"), "REG_RECRIADOS_V410F": LV.REG_RECRIADOS_V410F, "REG_FUNCAO": LV.REG_FUNCAO}
    ns_.update(extra or {})
    exec(compile(_regex_da_leitura(var), "leitura_v411." + var, "exec"), ns_)
    return ns_[var]


for var, rot in (("m_s9t", "[v409] a traducao (herdada)"), ("m_s10", "[v410] os quatro registros com funcao da v410 (recriados)"), ("m_s6", "[v406]"), ("m_s7", "[v407]"), ("m_s8t", "[v408]"), ("m_t9_", "o bloco A TRADUCAO AS CLASSES DE TURING [v409 ...")):
    m_ = _acha(var, _out_real)
    etapa("stdout_real_da_v410_casa_com_a_regex_da_leitura_" + var, bool(m_), rotulo=rot)
_m10 = _acha("m_s10", _out_real)
etapa("stdout_real_da_v410_linha_v410_diz_SELOU_nos_quatro_e_2_specs", bool(_m10) and [_m10.group(i) for i in range(1, 5)] == ["SELOU"] * 4 and _m10.group(5) == _m10.group(6) == "2")
_lin11 = "   [v411] o registro com funcao e os por spec da v411: h0dn_bg1_v411=SELOU | specs: 2 (selados 2)\n"
_m11 = _acha("m_s11", _out_real + _lin11)
etapa("linha_v411_sintetica_casa_com_a_regex_da_leitura_m_s11", bool(_m11) and _m11.group(1) == "SELOU" and _m11.group(2) == _m11.group(3) == "2")
etapa("linha_v411_ausente_do_stdout_real_da_v410_nao_casa_m_s11", _acha("m_s11", _out_real) is None)
_stdout_h = stdout_de(OFF)
_m_h = re.search(r'^H0DN x BG1 ABERTO \[v411[^\n]*\n  primario \(modelo publicado\): Z nulo = (\S+) ; Z K = (\S+) ; ramo (\S+)  \|\|  Cefeidas livres \(ao lado, no mesmo item\): Z nulo = (\S+) ; Z K = (\S+) ; ramo (\S+)  \|\|  checagens ok = (\d+)/(\d+) ; gate = ([^\n]*)\n  >>> (\S+) <<<$', _stdout_h, flags=re.M)
etapa("bloco_H0DN_ABERTO_sintetico_casa_com_o_formato_que_gerar_candidato_v411_imprime", bool(_m_h))
_gc = open(os.path.join(PK, "gerar_candidato_v411.py"), encoding="utf-8").read()
etapa("o_formato_do_print_do_candidato_tem_as_mesmas_particulas_que_a_regex", all(x in _gc for x in ("primario (modelo publicado): Z nulo = %%s ; Z K = %%s ; ramo %%s  ||  Cefeidas livres (ao lado, no mesmo item): Z nulo = %%s ; Z K = %%s ; ramo %%s  ||  checagens ok = %%s/%%s ; gate = %%s", "H0DN x BG1 ABERTO [v411", "[v411] o registro com funcao e os por spec da v411: %%s | specs: %%d (selados %%d)")))

# ---- 9. o fechamento (--dump PASTA grava cada texto renderizado, so' para a leitura humana; nada e' gravado sem a opcao)
if "--dump" in sys.argv:
    dd_ = sys.argv[sys.argv.index("--dump") + 1]; os.makedirs(dd_, exist_ok=True)
    for n_, t_ in textos.items():
        open(os.path.join(dd_, n_ + ".md"), "w", encoding="utf-8").write(t_ if isinstance(t_, str) else str(t_))
R["resumo"] = {"etapas": len(R["etapas"]), "falhas": len(R["falhas"]), "nao_provado_sem_o_core_real": ["leitura_v411.ler", "ESPERADOS_v411 real", "sidecar e selo reais", "paragrafo_readme (quadro v397) com o core da rodada", "o stdout do rito"]}
if "--saida" in sys.argv:
    out = sys.argv[sys.argv.index("--saida") + 1]
    open(out, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1))
    print("gravado:", out)
print("\nRESUMO:", json.dumps(R["resumo"], ensure_ascii=False))
sys.exit(1 if R["falhas"] else 0)
