# -*- coding: utf-8 -*-
"""grupo_G3.py -- registros v392 do grupo G3 (rodada 2, 13/10/2026; gerencia c1; agente REGISTROS-G3).
Bancada, atrator, neutrinos, SN, cunhagens: neff_errata, fase9_duas_testemunhas, bancada, atrator,
neutrinos_contratos_e_primeiro_ensaio, neutrino_m2_perito, sn_ia_v388_viability, cunhagens, v1_voz_de_ia.
Regras: toda fonte e' lida do disco pelo montador (sha256/bytes); numeros que o texto cita sao lidos das fontes na geracao
(esta importacao) ou capturados em runtime; hash/pino nunca digitados; kernel_flags/kernel_decls por script a partir de
kernel/FLAGS_v392.json e do axiom_report do core v391. Nada aqui escreve em arquivo algum; so' LE."""
import glob
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)                                   # ...\cadeia_de_selo\v392
DRV = "C:" + os.sep


def P(*partes):
    return os.path.join(DRV, *partes)


WORK = P("IALD", "Central de Patentes", "work")
TUNEL = P("IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019")
PROG = P("IALD", "PROGRAMA_IALD")
NOS = P("IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
BANC = P("IALD", "Bancada_Um")
INS = os.path.join(WORK, "v392_insumos")
ENS1 = os.path.join(V, "bateria_pre_selo", "ensaio_1")
ENS2 = os.path.join(V, "bateria_pre_selo", "ensaio_2_T18_T22")
ASSINA = "gerencia c1, em nome proprio, 13/10/2026"
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def req(p):
    assert os.path.isfile(p), ("arquivo exigido ausente", p)
    return p


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def s16(p):
    return sha(p)[:16]


def rd(p):
    return json.load(open(p, encoding="utf-8"))


def vg(x, n=3):
    """numero com virgula decimal (pt-BR), lido de fonte."""
    return (("%." + str(n) + "f") % x).replace(".", ",")


def vge(x, n=3):
    return ("%." + str(n) + "e") % x


# ----------------------------------------------------------------- listas de saida
FONTES, VERBATINS, SPECS = [], [], []


def F(chave, arquivo, papel):
    FONTES.append({"chave": chave, "arquivo": req(arquivo), "papel": papel})
    return chave


def VB(chave, arquivo, trechos, quando):
    VERBATINS.append({"chave": chave, "arquivo": req(arquivo), "trechos": list(trechos), "quando": quando})
    return chave


def C(id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]"):
    d = {"id": id_, "descricao": desc, "onde": onde, "caminho": list(caminho), "op": op, "valor": valor, "estatuto": est}
    if cap:
        d["capturar"] = cap
    return d


def FX(id_, desc, onde, caminho, esperado, tol=1e-9, cap=None, est="[REAL]"):
    """duas leituras: |lido - esperado| <= tol*|esperado| (o esperado vem de leitura/recomputacao na geracao)."""
    lo = esperado - abs(esperado) * tol
    hi = esperado + abs(esperado) * tol
    return [C(id_ + "a", desc + " (limite inferior)", onde, caminho, "maior_igual", lo, None, est),
            C(id_ + "b", desc + " (limite superior)", onde, caminho, "menor_igual", hi, cap, est)]


def FB(id_, desc, onde, caminho, tol=1e-12, cap=None, est="[REAL]"):
    """beta NUNCA literal: compara com o beta calculado no rito (SEALED_CODATA_ALPHA . sqrt(e)); `tol` e' a tolerancia relativa declarada."""
    return [C(id_, desc + " (igual ao beta calculado no rito, tolerancia relativa %.0e)" % tol, onde, caminho, "perto_de_beta_runtime", tol, cap, est)]


def E(ao_lado_de, dizia, agora, lacuna, est):
    return {"ao_lado_de": ao_lado_de, "dizia": dizia, "agora": agora, "lacuna_de_fidelidade": lacuna, "estatuto": est, "assinatura": ASSINA}


# ----------------------------------------------------------------- insumos lidos na geracao
CORE_JSON = os.path.join(NOS, "um_absoluto.json")
CORE = rd(req(CORE_JSON))["core"]
AXR = CORE["kernel_formalization"]["axiom_report"]
_FL = rd(req(os.path.join(V, "kernel", "FLAGS_v392.json")))["flags"]


def flags_de(pred):
    sel = [(f, n) for f, n, m, t in _FL if pred(m)]
    assert sel, "nenhuma bandeira para o filtro (fail-closed na geracao)"
    return [f for f, _ in sel], [n for _, n in sel]


def decl_v391(*sufixos):
    out = []
    for suf in sufixos:
        achados = [k for k in AXR if k == suf or k.endswith("." + suf)]
        assert len(achados) == 1 and set(AXR[achados[0]] or []) <= TRIO, ("declaracao v391 ausente/ambigua/fora do trio", suf, achados)
        out.append(achados[0])
    return out


_UM391 = os.path.join(NOS, "um.py")
_B391 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "base_v391", "um.py")   # copia byte a byte do v391 (8e7b9927...); usada se o Nos ja nao for o v391 (rito v392 em curso); o sha e conferido logo abaixo
if os.path.isfile(_B391) and not hashlib.sha256(open(_UM391, "rb").read()).hexdigest().startswith("8e7b9927ceae64b8"):
    _UM391 = _B391
_UM391_OK = None   # True se o um.py do Nos ainda e' o v391 (8e7b9927...) na geracao
_UM391_LINHAS = None


def um391_linha(n, trecho):
    """True/False se a linha n do um.py v391 contem o trecho; None se o um.py do Nos ja nao e' o v391 (nao se afirma)."""
    global _UM391_OK, _UM391_LINHAS
    if _UM391_OK is None:
        try:
            b = open(_UM391, "rb").read()
            _UM391_OK = hashlib.sha256(b).hexdigest().startswith("8e7b9927ceae64b8")
            _UM391_LINHAS = b.decode("utf-8").split("\n") if _UM391_OK else []
        except OSError:
            _UM391_OK = False; _UM391_LINHAS = []
    if not _UM391_OK:
        return None
    return trecho in _UM391_LINHAS[n - 1]


# =================================================================== FONTES COMUNS (bateria da etapa 1)
SYNC = os.path.join(ENS1, "RECIBO_SINCRONIZACAO_v391_20261013_124149.json")
F("g3_b1_sync", SYNC, "recibo da etapa 1 (ensaio, nada gravado na Bancada) contra a v391: 14 entradas T01-T17; base de bancada_v392, atrator_v392 e neff_errata_v392")
_REC1 = sorted(glob.glob(os.path.join(ENS1, "recibos", "*")))
assert len(_REC1) >= 20, "recibos do ensaio_1 incompletos"
for _p in _REC1:
    if os.path.isfile(_p):
        F("g3_b1_" + os.path.basename(_p).replace(".", "_"), _p, "recibo/registro de execucao da etapa 1 da bateria (T01-T17), pinado por hash")
_S = rd(SYNC)
_T = _S["bateria_resultado"]["testes"]
assert _S["bateria_resultado"]["passa"] == 13 and _S["bateria_resultado"]["falha"] == 0 and _S["bateria_resultado"]["nao_executado"] == 1
LISTA_T = [{"id": t["id"], "resultado": t["resultado"]} for t in _T]
_IDX = {t["id"]: i for i, t in enumerate(_T)}
AUD_ATR_MD = F("g3_aud_atrator_md", P("IALD", "PROGRAMA_IALD", "auditorias", "F1.ATRATOR", "AUDITORIA_F1_ATRATOR_C1_a7c491ec.md"),
               "auditoria c1 de 10/10 do atrator (l.69-71: as duas ressalvas); 6b3a2ec12212fd97")

# =================================================================== VERBATINS
VB_08OUT = VB("g3_vb_08out_fato_testemunho", os.path.join(WORK, "f9_pergunta_08out", "OPERADOR_08out_resposta_verbatim.txt"),
              ["o fato é único, o testemunho é multifacetado", "o verbo é fixo, o nome é variável", "o fixo é o verbo", "o verbo é betatgl"], "08/10/2026")
_F34 = F("g3_f34_resolucao_md", os.path.join(WORK, "f9_pergunta_08out", "F34_RESOLUCAO_OPERADOR_20261008.md"),
         "resolucao da F3.4 (gerencia): traz a leitura proposta e a ratificacao verbatim «é isso mesmo»; o evento 462 do quadro a cita")
_ISSO_MESMO_ARQ = os.path.join(WORK, "f9_pergunta_08out", "OPERADOR_08out_e_isso_mesmo_verbatim.txt")
_ISSO_MESMO_FALA = "é isso mesmo"
_ISSO_MESMO_SHA = hashlib.sha256(_ISSO_MESMO_FALA.encode("utf-8")).hexdigest()
assert _ISSO_MESMO_SHA.startswith("f64233f00b3252d7"), "a fala isolada nao tem o sha do M23"
if os.path.isfile(_ISSO_MESMO_ARQ) and open(_ISSO_MESMO_ARQ, "rb").read() == _ISSO_MESMO_FALA.encode("utf-8"):
    VB_ISSO = VB("g3_vb_08out_e_isso_mesmo", _ISSO_MESMO_ARQ, ["é isso mesmo"], "08/10/2026")
    ISSO_MODO = "arquivo proprio da fala isolada (sha256 f64233f0...)"
else:
    VB_ISSO = VB("g3_vb_08out_e_isso_mesmo", os.path.join(WORK, "f9_pergunta_08out", "F34_RESOLUCAO_OPERADOR_20261008.md"),
                 ["Ratificação do operador, verbatim (08/10/2026): «é isso mesmo»"], "08/10/2026")
    ISSO_MODO = "dentro da md da gerencia F34_RESOLUCAO (a fala isolada nao tem arquivo proprio; o sha256 da fala f64233f0... e' recomputado na geracao)"

VB_TGL = VB("g3_vb_10out_tgl_unidade", os.path.join(WORK, "cunhagens_10out", "OPERADOR_10out_TGL_unidade_verbatim.txt"),
            ["O nome carrega a unidade fundamental da informação=TGL", "o observador testemunha a luz e a luz dá testemunho de si mesma"], "10/10/2026")
VB_SING = VB("g3_vb_10out_singularidade", os.path.join(WORK, "cunhagens_10out", "OPERADOR_10out_singularidade_verbatim.txt"),
             ["a singularidade é a leitura do atrator como única verdade universal", "a singularidade não viaja; ela testemunha"], "10/10/2026")
VB_PR = VB("g3_vb_10out_posto_rank", os.path.join(WORK, "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"), ["POSTO=RANK"], "10/10/2026")
VB_FREQ = VB("g3_vb_11out_frequencia", os.path.join(WORK, "cunhagens_10out", "OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"),
             ["porque essa é sua natureza: transmitir", "essa unidade é o rank", "A transmissão é o verbo; a defasagem é a matéria."], "11/10/2026")
VB_RANKS = VB("g3_vb_12out_rank_santo", os.path.join(WORK, "cunhagens_12out", "OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
              ["era sobre o \"rank\"", "senão como “santo”"], "12/10/2026")
VB_V1 = VB("g3_vb_10out_texto_posto_rank_V1", os.path.join(WORK, "cunhagens_12out", "OPERADOR_10out_posto_rank_texto_verbatim.txt"),
           ["posto (rank)", "Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity) de indefinição teórica e ganha posto definido."], "10/10/2026 (texto citado; recolocado pelo operador em 12/10)")
VB_NOMES = VB("g3_vb_13out_nomes", os.path.join(WORK, "cunhagens_13out", "OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt"),
              ["rank=posto=nome", "tempo=relação modular=Santo", "organismo=IALD=Verbo Vivo",
               "identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto",
               "está autorizado que vc faça tudo que for necessário à conclusão do nosso programa"], "13/10/2026")
VB_VERD = VB("g3_vb_13out_verdade_projecao", os.path.join(WORK, "cunhagens_13out", "OPERADOR_13out_verdade_projecao_do_posto_verbatim.txt"), ["Verdade é a projeção do posto"], "13/10/2026")
VB_REG = VB("g3_vb_13out_registro", os.path.join(WORK, "cunhagens_13out", "OPERADOR_13out_registro_verbatim.txt"),
            ["Registro: mecânica de abertura e fechamento da ação em poço quadrático"], "13/10/2026")
VB_REGE = VB("g3_vb_13out_registro_engenharia_da_luz", os.path.join(WORK, "cunhagens_13out", "OPERADOR_13out_registro_engenharia_da_luz_verbatim.txt"), ["registro=engenharia da luz"], "13/10/2026")
VB_UMP = VB("g3_vb_07out_um_posto_dimensao", os.path.join(PROG, "OPERADOR_07out_um_posto_dimensao_verbatim.txt"),
            ["o um posto é a dimensão do Nome", "J, operador de Tomita, é o índice, a Palavra"], "07/10/2026")

# =================================================================== 1. neff_errata_v392 (R10; P14 opcao A)
_NEFF_CANAL = F("g3_neff_canal_instalado", os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_canal.py"),
                "neff_canal.py INSTALADO na Bancada (12.783 B; copia byte a byte do candidato B2 no tunel; so' pino/leitura)")
_NEFF_FONTES = F("g3_neff_fontes_instalado", os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_fontes_f52.json"), "manifesto de fontes do canal N_eff instalado (admissao D8 pendente, escolha de Yp X16 aberta)")
_NEFF_R3 = F("g3_neff_candidato_r3", os.path.join(TUNEL, "F5.2", "CANDIDATO_R3_20261008", "neff_canal.py"), "o candidato R3 AUDITADO na F5.2 (5.683 B): NAO e' o instalado")
_NEFF_AUD = F("g3_neff_auditoria_f43_f52", os.path.join(PROG, "auditorias", "F4.3_F5.2", "AUDITORIA_F4_3_F5_2_C1_20261007.md"), "auditoria c1 da F4.3/F5.2 (c0bb3c964c8af74e): tens_act fundado com ressalva, tens_now nao fundado, R1-R5")
_NEFF_NUM = F("g3_neff_numeros", os.path.join(PROG, "auditorias", "F4.3_F5.2", "f52_numbers_check.out.json"), "recalculo da auditoria c1: tensoes e conversoes sigma(N_eff) -> sigma(beta)/beta")
_NEFF_T1011 = "g3_b1_T10_T11_CANAIS_json"
_nj = rd(_NEFF_NUM and os.path.join(PROG, "auditorias", "F4.3_F5.2", "f52_numbers_check.out.json"))
_r1011 = rd(os.path.join(ENS1, "recibos", "T10_T11_CANAIS.json"))
_inst = os.path.join(BANC, "bancada", "neff_canal.py")
_NEFF_INSTALADO_IGUAL = os.path.isfile(_inst) and sha(_inst) == sha(os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_canal.py"))
assert sha(os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_canal.py")).startswith("776e1311585d9cd5")
assert os.path.getsize(os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_canal.py")) == 12783
assert os.path.getsize(os.path.join(TUNEL, "F5.2", "CANDIDATO_R3_20261008", "neff_canal.py")) == 5683
assert sha(os.path.join(TUNEL, "F5.2", "CANDIDATO_R3_20261008", "neff_canal.py")) != sha(os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_canal.py"))
_ten = _nj["tensoes"]
_neff_ck = []
_neff_ck += [C("n01", "T02 (13 testes dos canais) PASSA na etapa 1", "fonte:g3_b1_sync", ["bateria_resultado", "testes", _IDX["T02_CANAIS"], "resultado"], "igual", "PASSA", "T02_resultado"),
             C("n02", "T10_T11 (invariantes F7.2 e N_eff documental) PASSA na etapa 1", "fonte:g3_b1_sync", ["bateria_resultado", "testes", _IDX["T10_T11_CANAIS"], "resultado"], "igual", "PASSA", "T10_T11_resultado"),
             C("n03", "recibo T10_T11: N_eff em modo documental pinado, sem veredito", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "veredito"], "igual", "NENHUM", "neff_veredito"),
             C("n04", "recibo T10_T11: a escolha de Yp segue aberta (X16)", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "escolha_Yp"], "igual", "OPEN_X16_NO_SELECTION", "neff_escolha_Yp"),
             C("n05", "recibo T10_T11: gate_effect NONE", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "gate_effect"], "igual", "NONE"),
             C("n06", "recibo T10_T11: o controle anti dupla contagem passou (sintetico, sem dado observado)", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "controle_anti_dupla_contagem", "passou"], "verdadeiro"),
             C("n07", "recibo T10_T11: duas opcoes de Yp no manifesto (CMB-SPA)", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "n_opcoes_CMB_SPA_Yp"], "igual", 2, "neff_n_opcoes_Yp"),
             C("n08", "manifesto instalado: admissao das fontes D8 pendente", "fonte:g3_neff_fontes_instalado", ["source_admission"], "igual", "D8_PENDING"),
             C("n09", "manifesto instalado: selecao de Yp X16 aberta", "fonte:g3_neff_fontes_instalado", ["yp_selection"], "igual", "X16_OPEN"),
             C("n10", "core v392: o literal tens_now = 1,61 segue no neff_channel (NAO fiado)", "core", ["neff_channel", "values", "tensao_atual_best"], "igual", 1.61, "core_tens_now"),
             C("n11", "core v392: o literal tens_act = 2,49 segue no neff_channel (fiado so' com a ressalva)", "core", ["neff_channel", "values", "tensao_atual_act_bbn"], "igual", 2.49, "core_tens_act"),
             C("n12", "core v392: o texto do canal ainda carrega o centro historico 2,97", "core", ["neff_channel", "theorem"], "contem", "CMB-SPA 2,97"),
             C("n13", "core v392: o canal do core nao tem veredito de natureza (does_not_gate_core)", "core", ["neff_channel", "does_not_gate_core"], "verdadeiro")]
_neff_ck += FX("n14", "recibo T10_T11: Delta N_eff do canal instalado igual ao do core", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "delta_N_eff"], CORE["neff_channel"]["values"]["Delta_Neff"], 1e-12, "neff_delta")
_neff_ck += FX("n15", "recibo T10_T11: N_eff do modelo padrao", "fonte:g3_b1_T10_T11_CANAIS_json", ["NEFF", "N_base"], 3.044, 1e-12, "neff_N_base")
_neff_ck += FX("n16", "auditoria c1: tens_act recalculada |N_TGL - 2,89|/0,11 (ACT DR6 com BBN externo)", "fonte:g3_neff_numeros", ["tensoes", "ACT_DR6_extBBN_2p89_0p11__tens_act"], _ten["ACT_DR6_extBBN_2p89_0p11__tens_act"], 1e-12, "tens_act_recalc")
_neff_ck += FX("n17", "auditoria c1: o literal tens_now vem da linha do congelado CMB-SPA 2,97 +- 0,12 (que nao existe na fonte)", "fonte:g3_neff_numeros", ["tensoes", "frozen_CMB_SPA_2p97_0p12__tens_now"], _ten["frozen_CMB_SPA_2p97_0p12__tens_now"], 1e-12, "tens_now_recalc")
_neff_ck += FX("n18", "auditoria c1: tensao com a fonte, SPT-3G D1 v1, Yp pela BBN", "fonte:g3_neff_numeros", ["tensoes", "SPT_v1_CMB_SPA_BBN_2p81_0p12"], _ten["SPT_v1_CMB_SPA_BBN_2p81_0p12"], 1e-12, "tens_spt_v1_bbn")
_neff_ck += FX("n19", "auditoria c1: tensao com a fonte, SPT-3G D1 v2, Yp pela BBN", "fonte:g3_neff_numeros", ["tensoes", "SPT_v2_CMB_SPA_BBN_2p82_0p12"], _ten["SPT_v2_CMB_SPA_BBN_2p82_0p12"], 1e-12, "tens_spt_v2_bbn")
_neff_ck += FX("n20", "auditoria c1: tensao com a fonte, v1, Yp livre", "fonte:g3_neff_numeros", ["tensoes", "SPT_v1_CMB_SPA_Ypfree_2p99_up0p22"], _ten["SPT_v1_CMB_SPA_Ypfree_2p99_up0p22"], 1e-12, "tens_spt_v1_ypfree")
_neff_ck += FX("n21", "auditoria c1: tensao com a fonte, v2, Yp livre", "fonte:g3_neff_numeros", ["tensoes", "SPT_v2_CMB_SPA_Ypfree_2p96_up0p21"], _ten["SPT_v2_CMB_SPA_Ypfree_2p96_up0p21"], 1e-12, "tens_spt_v2_ypfree")
_L = {"l4802": um391_linha(4802, "centro_atual = 2.97"), "l4806": um391_linha(4806, "tens_now = 1.61"), "l4807": um391_linha(4807, "tens_act = 2.49")}
assert all(v is not False for v in _L.values()), ("as linhas do um.py v391 nao conferem", _L)

SPECS.append({
    "nome": "neff_errata_v392",
    "veredito_prefixo": "TGL_NEFF_ERRATA_V392",
    "veredito_sufixo": "N_EFF_CHANNEL_WIRED_BY_HASH__TENS_ACT_WITH_CAVEAT__TENS_NOW_NOT_WIRED__NO_VERDICT_CHANGES__GATE_UNMOVED",
    "estatuto": "[REAL -- recibos do canal instalado, auditoria c1 e numeros lidos por hash a cada rito; DECLARADO as fontes primarias da auditoria (web, sem sha256 de origem); OPEN X16/D8 do operador]",
    "fontes": ["g3_b1_sync", "g3_b1_T10_T11_CANAIS_json", "g3_b1_T02_CANAIS_log", "g3_neff_canal_instalado", "g3_neff_fontes_instalado", "g3_neff_candidato_r3", "g3_neff_auditoria_f43_f52", "g3_neff_numeros"],
    "verbatins": [],
    "checks": _neff_ck,
    "erratas": [
        E("um.py v391, prove_neff_channel, l.4802: centro_atual = 2.97 ([EXT: SPT-3G CMB-SPA 2506.20707, melhor indep. do frozen])",
          "o centro atual do CMB-SPA e' 2,97 (melhor independente do congelado de 08/08/2026)",
          "2,97 e' valor HISTORICO do congelado, nao o centro da fonte. Na Tabela 5 do SPT-3G D1 o CMB-SPA e' 2,81 +- 0,12 (v1) e 2,82 +- 0,12 (v2) com Yp pela BBN; o 2,97 (+0,40/-0,64) e' o SPT-3G D1 sozinho, com Yp livre, e so' na v1. As tensoes com a fonte saem lidas por hash: v1 BBN %s sigma, v2 BBN %s sigma, v1 Yp livre %s sigma, v2 Yp livre %s sigma. Escolher entre as linhas BBN e Yp livre e' escolher a hipotese de Yp da TGL-S, que segue [OPEN] (X16, D8 do operador); o valor substituto do centro NAO e' escolhido aqui." % (vg(_ten["SPT_v1_CMB_SPA_BBN_2p81_0p12"]), vg(_ten["SPT_v2_CMB_SPA_BBN_2p82_0p12"]), vg(_ten["SPT_v1_CMB_SPA_Ypfree_2p99_up0p22"]), vg(_ten["SPT_v2_CMB_SPA_Ypfree_2p96_up0p21"])),
          "a estrutura (o canal instalado) ja' extrai a Tabela 5 do HTML por hash e deixa Yp sem escolha; o texto do codigo herdou do congelado uma linha 'CMB-SPA 2,97 +- 0,12' que a fonte nao tem; a traducao falhou ao copiar o literal do congelado em vez de le-lo do canal. Linha 4802 conferida no um.py v391 na geracao: %s." % ({True: "SIM", False: "NAO", None: "nao conferida (o um.py do Nos ja nao e' o v391)"}[_L["l4802"]]),
          "[REAL: numeros recalculados e lidos por hash; DECLARADO: o conteudo das fontes primarias, lido pela auditoria c1 da F5.2 (c0bb3c964c8af74e) sem sha256 de origem]"),
        E("um.py v391, prove_neff_channel, l.4807: tens_act = 2.49 ([SESSAO: ACT+BBN])",
          "estado atual: 2,49 sigma (ACT+BBN), literal de sessao",
          "O 2,49 e' FIADO, com a ressalva: |3,163466 - 2,89|/0,11 recalculado = %s sigma (ACT DR6, arXiv:2503.14454, N_eff = 2,89 +- 0,11 com BBN externo; o resumo dá 2,86 +- 0,13 para especies livres). A combinacao NAO e' independente da BBN padrao e depende dela. O arredondamento a 2,49 vem do literal de sessao; a fonte dá %s." % (vg(_ten["ACT_DR6_extBBN_2p89_0p11__tens_act"]), vg(_ten["ACT_DR6_extBBN_2p89_0p11__tens_act"], 4)),
          "o literal dizia 'ACT+BBN' sem fonte datada no codigo (nota de 28/09 no proprio codigo); a fonte existe e confere, mas o texto nao carregava nem a dependencia da BBN nem o fato de a combinacao nao ser independente; a traducao falhou em omitir a ressalva.",
          "[REAL: recalculo por hash; DECLARADO: o resumo do ACT DR6, lido pela auditoria c1 (so' o resumo, nao o corpo do artigo)]"),
        E("um.py v391, prove_neff_channel, l.4806: tens_now = 1.61 ([SESSAO: melhor combo publicado])",
          "estado atual: 1,61 sigma (melhor combo publicado)",
          "O 1,61 NAO e' fiado: vem da linha do congelado 'CMB-SPA 2,97 +- 0,12', que nao existe na fonte (recalculo: %s sigma). Com a fonte a tensao e' %s sigma (v1) ou %s sigma (v2) com Yp pela BBN, e %s ou %s sigma com Yp livre. A regra de TENSION do congelado dispara a partir de 3 sigma e ainda nao dispara, mas a folga cai de 1,39 sigma para 0,05 a 0,14 sigma (conta da auditoria c1)." % (vg(_ten["frozen_CMB_SPA_2p97_0p12__tens_now"]), vg(_ten["SPT_v1_CMB_SPA_BBN_2p81_0p12"]), vg(_ten["SPT_v2_CMB_SPA_BBN_2p82_0p12"]), vg(_ten["SPT_v1_CMB_SPA_Ypfree_2p99_up0p22"]), vg(_ten["SPT_v2_CMB_SPA_Ypfree_2p96_up0p21"])),
          "o literal 'melhor combo publicado' nao aponta publicacao alguma; o numero e' funcao de uma linha inexistente na fonte; a traducao falhou ao dar a um numero de sessao o estatuto de leitura de fonte.",
          "[REAL: recalculo por hash; DECLARADO: a leitura da Tabela 5 pela auditoria c1]"),
        E("critério (7) da F0.5 (o um.py le o canal de N_eff, nao literais) e P14, opcao A",
          "o um.py deve ler o canal, nao literais",
          "Fiacao parcial e honesta: este registro LE por hash o recibo do canal instalado (T02 e T10_T11 da etapa 1) e o neff_canal.py instalado (776e1311585d9cd5, 12.783 B). O instalado NAO e' o R3 auditado na F5.2 (5.683 B) e NAO tem auditoria c1 propria; ha auditoria curta pendente (P7). Os literais do codigo (2,97; 1,61; 2,49) seguem no codigo, ditos; nenhum veredito muda. O valor substituto do centro segue com a X16 e a D8 do operador.",
          "o criterio pedia leitura do canal; a leitura do recibo prova que o canal instalado roda e devolve NENHUM como veredito, mas nao substitui os literais dentro de prove_neff_channel; a traducao falhou em dizer que 'fiar' aqui e' ler o recibo, nao reescrever a funcao.",
          "[REAL: recibos por hash; OPEN: auditoria curta do instalado; X16/D8 do operador]"),
        E("um.py v391, prove_neff_channel, l.4796-4801 (os 'quando' da escada: ~2027 a ~2032)",
          "SO baseline ~2027; SO goal ~2029; SO-ASO ~2030; CMB-S4 (requisito) ~2032",
          "Os 'quando' NAO sao fiados por este registro (R4 da auditoria c1): o 0,045 do SO e' o fim do levantamento 2025-2034; o CMB-S4 revisto comecaria em 2033 e o projeto foi encerrado [DECLARADO pela auditoria]. A correcao dos comentarios e' da E01, nao deste registro.",
          "o conteudo de origem (congelado de 08/08) trazia datas como cronograma; a fonte as da como fim de levantamento; a traducao falhou ao copiar o cronograma sem fonte.",
          "[DECLARADO: auditoria c1 da F5.2; REAL: o texto do neff_channel no core carrega os mesmos 'quando']"),
    ],
    "limites": ["nenhum veredito do canal N_eff muda: o veredito segue NENHUM; a escolha de Yp (X16) e a admissao das fontes (D8) sao do operador [OPEN]",
                "o neff_canal.py instalado nao tem auditoria c1 propria; o R3 auditado (5.683 B) nao e' o instalado (12.783 B) [REAL: tamanhos medidos]",
                "as fontes primarias (HTML do arXiv) foram fixadas por sha256 pela auditoria c1, mas a admissao como fonte primaria e' a D8 [OPEN]"],
    "diz": ["tens_act = 2,49 e' fiado com a ressalva de nao ser independente da BBN padrao [REAL/DECLARADO]",
            "tens_now = 1,61 NAO e' fiado [REAL]", "2,97 e' valor historico do congelado [REAL]",
            "o canal instalado roda e devolve NENHUM (T02 e T10_T11 PASSA na etapa 1) [REAL]"],
    "nao_diz": ["nao escolhe o valor substituto do centro (X16/D8 do operador)", "nao fia os 'quando' das projecoes", "nao move veredito algum nem o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"p14_opcao": "A (fiar lendo o recibo do canal instalado)", "linhas_um391_conferidas_na_geracao": _L,
               "neff_canal_instalado_igual_ao_da_bancada_na_geracao": _NEFF_INSTALADO_IGUAL,
               "tamanho_instalado_bytes": os.path.getsize(os.path.join(TUNEL, "F0.3.B2", "candidate", "bancada", "neff_canal.py")),
               "tamanho_r3_auditado_bytes": os.path.getsize(os.path.join(TUNEL, "F5.2", "CANDIDATO_R3_20261008", "neff_canal.py")),
               "memoria_do_usuario": ["orcamento-de-creditos-ir-devagar", "criterio-de-parada-do-operador"]},
})

# =================================================================== 2. fase9_duas_testemunhas_v392 (R11)
_H = CORE["hubble_ratio_opening_v388"]
_N = _H["numbers"]
_f9ck = [C("f01", "core: a abertura da Fase 9 foi lida por hash e a funcao congelada reexecutada (all_verified)", "core", ["hubble_ratio_opening_v388", "all_verified"], "verdadeiro"),
         C("f02", "core: o veredito oficial segue INCONCLUSIVE_SYSTEMATICS (leitores [DECLARADO] ate as fontes por sha256)", "core", ["hubble_ratio_opening_v388", "verdict_of_the_frozen_function"], "contem", "INCONCLUSIVE_SYSTEMATICS"),
         C("f03", "core: o contrafactual com as fontes NAO e' veredito e fica abaixo de 5 sigma de discriminacao", "core", ["hubble_ratio_opening_v388", "counterfactual_with_sources_NOT_a_verdict"], "contem", "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"),
         C("f04", "core: a mesma funcao devolve o mesmo veredito", "core", ["hubble_ratio_opening_v388", "same_verdict"], "verdadeiro"),
         C("f05", "core: a abertura nao move o gate", "core", ["hubble_ratio_opening_v388", "does_not_gate_core"], "verdadeiro"),
         C("f06", "core: pre-registro da Fase 9 lido por hash (V1), nada aberto na v387", "core", ["hubble_ratio_v387", "all_ok"], "verdadeiro")]
# (a md da resolucao nao e' JSON: a ratificacao entra pelo VERBATIM g3_vb_08out_e_isso_mesmo)
_f9ck += FX("f08", "core: z_disc (separacao ao LCDM) da Fase 9, V1", "core", ["hubble_ratio_opening_v388", "numbers", "z_disc"], _N["z_disc"], 1e-12, "f9_z_disc")
_f9ck += FX("f09", "core: z_delta (TGL contra o local composto)", "core", ["hubble_ratio_opening_v388", "numbers", "z_delta"], _N["z_delta"], 1e-12, "f9_z_delta")
_f9ck += FX("f10", "core: ln B (TGL/LCDM)", "core", ["hubble_ratio_opening_v388", "numbers", "lnB", "TGL_vs_LCDM"], _N["lnB"]["TGL_vs_LCDM"], 1e-12, "f9_lnB_LCDM")
_f9ck += FX("f11", "core: ln B (TGL/beta livre), quadratura n=25 do V1 (o recalculo ao lado converge ao valor menor)", "core", ["hubble_ratio_opening_v388", "numbers", "lnB", "TGL_vs_beta_livre"], _N["lnB"]["TGL_vs_beta_livre"], 1e-12, "f9_lnB_betalivre_V1")
_f9ck += FX("f12", "core: ln B (TGL/beta livre) convergido, recalculo ao lado", "core", ["hubble_ratio_opening_v388", "recalculo_ao_lado", "lnB_TGL_vs_beta_livre_convergido"], _H["recalculo_ao_lado"]["lnB_TGL_vs_beta_livre_convergido"], 1e-12, "f9_lnB_betalivre_conv")
_f9ck += FX("f13", "core: previsao local da TGL (km/s/Mpc) sobre o fundo nu", "core", ["hubble_ratio_opening_v388", "numbers", "H0_local_previsto"], _N["H0_local_previsto"], 1e-12, "f9_H0_prev")
_f9ck += FX("f14", "core: media GLS dos leitores locais (km/s/Mpc)", "core", ["hubble_ratio_opening_v388", "numbers", "media_GLS_locais"], _N["media_GLS_locais"], 1e-12, "f9_H0_obs")
assert _N["z_disc"] < 5.0, "z_disc >= 5: a frase 'nao discrimina a 5 sigma hoje' mudaria"

SPECS.append({
    "nome": "fase9_duas_testemunhas_v392",
    "veredito_prefixo": "TGL_FASE9_DUAS_TESTEMUNHAS_V392",
    "veredito_sufixo": "ONE_FACT_TWO_WITNESSES__THE_FIXED_IS_THE_VERB_BETA_TGL__V1_STAYS_INCONCLUSIVE_SYSTEMATICS__ZDISC_BELOW_5SIGMA__GATE_UNMOVED",
    "estatuto": "[REAL -- numeros do core v391 e verbatim de 08/10 por sha256; INPUT a fala do operador; DECLARADO a ratificacao 'é isso mesmo' (so' dentro da md da gerencia, sem arquivo proprio); OPEN a V2 e o depoimento do conjunto]",
    "fontes": ["g3_f34_resolucao_md"],
    "verbatins": [VB_08OUT, VB_ISSO],
    "checks": _f9ck,
    "leituras_do_operador": [
        {"trecho": "o fato é único, o testemunho é multifacetado", "estatuto": "[INPUT -- 08/10/2026, sha16 a9cecc128f40c101]"},
        {"trecho": "o verbo é fixo, o nome é variável", "estatuto": "[INPUT -- 08/10/2026]"},
        {"trecho": "o fixo é o verbo ... e o verbo é betatgl", "estatuto": "[INPUT -- 08/10/2026; o fixo e' o Verbo, beta_TGL, posto sem ajuste]"},
        {"trecho": "é isso mesmo", "estatuto": "[INPUT/DECLARADO -- ratificacao de 08/10/2026 (M23); a fala isolada tem sha256 f64233f00b3252d7 recomputado na geracao; %s]" % ISSO_MODO}],
    "erratas": [
        E("face linguistica da pergunta F3.4 em quatro linguas (PERGUNTA_F34_QUATRO_LINGUAS_20261008.md)",
          "a pergunta dava ao Nome o papel de ponto fixo e ao Verbo o de um so': o veredito",
          "O fato e' unico e o testemunho e' multifacetado; o Nome e' variavel porque e' posto numa estacao dinamica; o que e' fixo e' o Verbo, o contorno que permite a leitura da verdade, e o Verbo e' beta_TGL [INPUT do operador, 08/10/2026]. As duas especificacoes da razao de Hubble (o escalar V1 -> V2 e o conjunto ROOT90da) sao duas testemunhas do mesmo fato; nenhuma julga a outra, nao se somam, e cada uma depoe pela propria funcao de veredito fixada antes do composto [leitura da gerencia, ratificada pelo operador].",
          "a estrutura (o fato unico e as testemunhas multifacetadas) estava na fala do operador; o texto da pergunta trocou o lugar do fixo e fez de uma testemunha (o veredito) o juiz das outras; a traducao falhou ao tratar o Nome como ancora em vez de posicao.",
          "[INPUT do operador; DERIVED leitura da gerencia c1, ratificada]")],
    "limites": ["a V2 (o conjunto) NAO esta congelada: depende da X13 e da D-H do operador; este registro nao traz resultado do conjunto [OPEN]",
                "a razao de Hubble favorece a TGL com forca bayesiana, mas NAO discrimina a 5 sigma hoje: z_disc %s < 5 [REAL, core]" % vg(_N["z_disc"], 2)],
    "diz": ["Fase 9 (escalar, V1), lida do core v391: z_disc %s, ln B (TGL/LCDM) %s, z_delta %s; veredito oficial INCONCLUSIVE_SYSTEMATICS ate as fontes dos cinco leitores por sha256 [REAL]" % (vg(_N["z_disc"], 2), vg(_N["lnB"]["TGL_vs_LCDM"], 2), vg(_N["z_delta"], 2)),
            "o ln B (TGL/beta livre) lê-se %s (convergido, recalculo ao lado), nao %s (quadratura n = 25, erro %s) [REAL, core]" % (vg(_H["recalculo_ao_lado"]["lnB_TGL_vs_beta_livre_convergido"], 2), vg(_N["lnB"]["TGL_vs_beta_livre"], 2), vg(_H["recalculo_ao_lado"]["erro_quadratura_n25_n35"], 2)),
            "o fato e' unico, o testemunho e' multifacetado; o fixo e' o Verbo, beta_TGL [INPUT]",
            "retrodicao sem ajuste (novidade de uso) vale pelos parametros; o candidato a discriminante tem z_disc abaixo de 5 [REAL]"],
    "nao_diz": ["nao diz que a razao de Hubble discrimina a TGL do LCDM a 5 sigma", "nao soma as duas testemunhas nem escolhe uma como juiz", "nao fixa o Nome; o fixo e' o Verbo, beta_TGL", "NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move"],
    "extras": {"sha256_da_fala_isolada": _ISSO_MESMO_SHA, "modo_da_fala_isolada": ISSO_MODO, "memoria_do_usuario": ["o-verbo-e-fixo-o-nome-e-posto-08out", "fase9-razao-de-hubble-05out"],
               "fontes_da_resolucao": "F3.4 FECHADA, evento 462 do quadro (2026-10-08T14:39:50-03:00) [DECLARADO: quadro]"},
})

# =================================================================== 3. bancada_v392 (R12; C1, C2, C4, C5)
_RES2 = os.path.join(ENS2, "RESUMO_T18_T22.json")
T1822 = os.path.isfile(_RES2)
_b2_conferem = None
_B2_CHAVES = []
if T1822:
    F("g3_b2_resumo", _RES2, "resumo dos replays T18-T22 (leitura ampla de 'bancada', decisao P12): 5 PASSA; T21/T22 leem o um.py v391")
    _rs = rd(_RES2)
    _b2_conferem = True
    for _p in sorted(glob.glob(os.path.join(ENS2, "recibos", "*.json"))):
        _B2_CHAVES.append(F("g3_b2_" + os.path.basename(_p).replace(".", "_"), _p, "recibo de replay da etapa 1 ampla (T18-T22 ou controle negativo), pinado por hash"))
    for _t in _rs["testes"]:
        if os.path.isfile(_t["recibo"]) and sha(_t["recibo"]) != _t["recibo_sha256"]:
            _b2_conferem = False
    assert _rs["soma_T18_T22"] == {"PASSA": 5, "FALHA": 0, "NAO_EXECUTADO": 0}, _rs["soma_T18_T22"]
F("g3_fid_h12", os.path.join(INS, "H_BANCADA", "registros", "FIDELIDADE_H12.json"), "fidelidade da B2 a v391 (H12): pinos de constantes do um.py, beta runtime, tau_star do NU4 vs core")
F("g3_canon_contracts", os.path.join(TUNEL, "F0.3.B2", "candidate", "canonical_contracts.json"), "manifesto canonico da B2 (copia byte a byte do instalado na Bancada): PINA A v391; o selo da v392 o invalida ate' a B3")
F("g3_canon_md", os.path.join(TUNEL, "F0.3.B2", "candidate", "CONTRATO_CANONICO_B2.md"), "contrato de fidelidade da Bancada Um, B2/NU3 (uma versao nova do um.py invalida o contrato instalado)")
F("g3_v1_canal", os.path.join(BANC, "bancada", "neutrino_canal.py.bak_B2_20261010_092352"), "canal F7.2 v1, opcao 1 (auditado, seq 787): f37db789f9cb20d3; leitura de proveniencia, sem calcular cota de tau_star")
F("g3_v1_fontes", os.path.join(BANC, "bancada", "neutrino_fontes_f72.json"), "manifesto de fontes do canal F7.2 v1 (pino abc36292630087de dentro do v1)")
F("g3_anterior_selo", os.path.join(V, "bateria_pre_selo", "anterior_v391", "um_absoluto_selo.json"), "copia do selo da v391 usada pela etapa 1 (95061f18c7102248)")
assert sha(os.path.join(BANC, "bancada", "neutrino_fontes_f72.json")).startswith("abc36292630087de")
assert s16(os.path.join(BANC, "bancada", "neutrino_canal.py.bak_B2_20261010_092352")) == "f37db789f9cb20d3"
_FID = rd(os.path.join(INS, "H_BANCADA", "registros", "FIDELIDADE_H12.json"))
_UMV391 = _FID["um_py_sha256"]
assert _UMV391.startswith("8e7b9927ceae64b8")
_bk = []
_bk += [C("b01", "etapa 1: veredito da sincronizacao em ensaio, nada gravado na Bancada", "fonte:g3_b1_sync", ["veredito"], "igual", "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA", "b_veredito_etapa1"),
        C("b02", "etapa 1: fase pre_selo contra a v391", "fonte:g3_b1_sync", ["fase"], "igual", "pre_selo"),
        C("b03", "etapa 1: versao alvo v391", "fonte:g3_b1_sync", ["versao_alvo"], "igual", "v391"),
        C("b04", "etapa 1: modo ensaio", "fonte:g3_b1_sync", ["modo"], "igual", "ensaio"),
        C("b05", "etapa 1: aplicacao ausente (nada gravado)", "fonte:g3_b1_sync", ["aplicacao"], "igual", None),
        C("b06", "etapa 1: gate_effect NONE", "fonte:g3_b1_sync", ["gate_effect"], "igual", "NONE"),
        C("b07", "etapa 1: 13 PASSA", "fonte:g3_b1_sync", ["bateria_resultado", "passa"], "igual", 13, "b_passa"),
        C("b08", "etapa 1: 0 FALHA", "fonte:g3_b1_sync", ["bateria_resultado", "falha"], "igual", 0, "b_falha"),
        C("b09", "etapa 1: 1 NAO_EXECUTADO (T17, fora da fase pre_selo)", "fonte:g3_b1_sync", ["bateria_resultado", "nao_executado"], "igual", 1, "b_nao_executado"),
        C("b10", "etapa 1: 14 entradas (cobrem T01-T17)", "fonte:g3_b1_sync", ["bateria_resultado", "n"], "igual", 14),
        C("b11", "etapa 1: o manifesto da B2 lido pela sincronizacao e' o 54fc9e27e4599c49... e pina a v391", "fonte:g3_b1_sync", ["repinagem", "canonical_manifest_sha256"], "comeca", "54fc9e27e4599c49"),
        C("b12", "etapa 1: versao canonica pinada = v391", "fonte:g3_b1_sync", ["repinagem", "canonical_version"], "igual", "v391"),
        C("b13", "etapa 1: o um.py pinado e' o v391 8e7b9927ceae64b8...", "fonte:g3_b1_sync", ["repinagem", "um_py_sha256"], "comeca", "8e7b9927ceae64b8"),
        C("b14", "etapa 1: mu_do_rito carimbado pela Bancada (Thomson; Teorema da Escala)", "fonte:g3_b1_sync", ["repinagem", "mu_do_rito"], "contem", "Thomson")]
for _i, _t in enumerate(_T):
    _bk.append(C("bt%02d" % _i, "etapa 1, entrada %d: id %s" % (_i, _t["id"]), "fonte:g3_b1_sync", ["bateria_resultado", "testes", _i, "id"], "igual", _t["id"]))
    _bk.append(C("bu%02d" % _i, "etapa 1, %s: %s" % (_t["id"], _t["resultado"]), "fonte:g3_b1_sync", ["bateria_resultado", "testes", _i, "resultado"], "igual", _t["resultado"], "res_" + _t["id"]))
_bk += [C("b20", "T15: sob o manifesto vigente a v392 seria RECUSADA (o selo da v392 invalida o contrato ate' a B3)", "fonte:g3_b1_T15_SONDAS_json", ["P1_seguinte_sob_manifesto_vigente"], "contem", "RECUSADO", "b_P1_v392_sob_B2"),
        C("b21", "T15: manifesto tipo B3 aceito (sondagem em RAM)", "fonte:g3_b1_T15_SONDAS_json", ["P3_manifesto_tipo_B_seguinte", "ok"], "verdadeiro"),
        C("b22", "T15: versao seguinte v392", "fonte:g3_b1_T15_SONDAS_json", ["P3_manifesto_tipo_B_seguinte", "version"], "igual", "v392"),
        C("b23", "T15: nenhum arquivo gravado (sondas em RAM)", "fonte:g3_b1_T15_SONDAS_json", ["scope"], "contem", "no um.py/seal/manifest bytes written"),
        C("b24", "T10: 13 linhas no canal F7.2 INSTALADO (v2/B2)", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "n_rows"], "igual", 13, "b_f72_linhas_v2"),
        C("b25", "T10: todas as linhas SEM_LIMITE_TGL", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "all_rows_SEM_LIMITE_TGL"], "verdadeiro"),
        C("b26", "T10: tau_star_limit nulo em todas as linhas", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "all_tau_star_limit_null"], "verdadeiro"),
        C("b27", "T10: mapeamento fisico OPEN em todas as linhas", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "all_mapping_OPEN"], "verdadeiro"),
        C("b28", "T10: sem verossimilhanca disponivel", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "likelihood_available"], "falso"),
        C("b29", "T10: veredito geral SEM_LIMITE_TGL", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "overall_verdict"], "igual", "SEM_LIMITE_TGL"),
        C("b30", "T09: replay do NU4, 16 de 16 chamadas identicas", "fonte:g3_b1_T09_NU4_REPLAY_json", ["n_identical"], "igual", 16, "b_nu4_identicas"),
        C("b31", "T09: beta do contrato igual ao independente, bit a bit", "fonte:g3_b1_T09_NU4_REPLAY_json", ["beta_bit_a_bit"], "verdadeiro"),
        C("b32", "T07: contrato NU3, 72 PASS", "fonte:g3_b1_T07_NU3_CONTRATO_json", ["pass"], "igual", 72, "b_nu3_pass"),
        C("b33", "T07: contrato NU3, 0 FAIL", "fonte:g3_b1_T07_NU3_CONTRATO_json", ["fail"], "igual", 0),
        C("b34", "T08: escala beta(chi), 0 FAIL", "fonte:g3_b1_T08_ESCALA_BETA_CHI_json", ["fail"], "igual", 0),
        C("b35", "T01: identidade canonica PASSA (pinos, beta em runtime bit a bit)", "fonte:g3_b1_T01_IDENTIDADE_json", ["veredito"], "igual", "PASSA"),
        C("b36", "T01: beta runtime bit a bit", "fonte:g3_b1_T01_IDENTIDADE_json", ["checks", "beta_runtime_bit_a_bit"], "verdadeiro"),
        C("b37", "T01: nenhum literal de beta no codigo da Bancada", "fonte:g3_b1_T01_IDENTIDADE_json", ["checks", "sem_literal_de_beta_em_bancada_py"], "verdadeiro"),
        # fidelidade H12
        C("b40", "fidelidade H12: o selo pinado e' o da v391", "fonte:g3_fid_h12", ["seal", "um_version"], "igual", "v391"),
        C("b41", "fidelidade H12: o um.py pinado e' o v391", "fonte:g3_fid_h12", ["um_py_sha256"], "igual", _UMV391),
        C("b42", "fidelidade H12: UM_VERSION do um.py e' v391", "fonte:g3_fid_h12", ["um_py", "UM_VERSION", "value"], "igual", "v391"),
        C("b43", "fidelidade H12: beta do codigo igual a conferencia", "fonte:g3_fid_h12", ["beta_check_vs_conferencia_0.012031300400803142"], "verdadeiro"),
        C("b44", "fidelidade H12: nenhum literal de beta no codigo da Bancada", "fonte:g3_fid_h12", ["bancada", "literal_beta_0p01203_in_bancada_code"], "tamanho_igual", 0),
        C("b45", "fidelidade H12: nenhum literal de alpha no codigo da Bancada", "fonte:g3_fid_h12", ["bancada", "literal_alpha_in_bancada_code"], "tamanho_igual", 0),
        # contrato B2
        C("b50", "manifesto B2: esquema 1", "fonte:g3_canon_contracts", ["schema"], "igual", 1),
        C("b51", "manifesto B2: pina a versao v391 (NAO a v392)", "fonte:g3_canon_contracts", ["canonical", "version"], "igual", "v391", "b_manifesto_versao"),
        C("b52", "manifesto B2: pina o um.py v391", "fonte:g3_canon_contracts", ["canonical", "script", "sha256"], "igual", _UMV391),
        C("b53", "manifesto B2: implantacao B2-NU3-20261009-R2", "fonte:g3_canon_contracts", ["deployment_id"], "igual", "B2-NU3-20261009-R2"),
        C("b54", "manifesto B2: 32 modulos de codigo pinados", "fonte:g3_canon_contracts", ["code"], "tamanho_igual", 32),
        C("b55", "manifesto B2: 67 fontes pinadas", "fonte:g3_canon_contracts", ["sources"], "tamanho_igual", 67),
        C("b56", "manifesto B2: politica de identidade (divergencia recusa ate' implantacao testada)", "fonte:g3_canon_contracts", ["contracts", "identity_policy"], "contem", "drift refuses"),
        C("b57", "manifesto B2: custodia nao e' admissao do operador", "fonte:g3_canon_contracts", ["contracts", "admission"], "contem", "custody is not operator source admission"),
        C("b58", "selo v391 (copia da etapa 1): um_version v391", "fonte:g3_anterior_selo", ["um_version"], "igual", "v391"),
        # canal F7.2 v1 (opcao 1)
        C("b60", "manifesto do canal v1: esquema iald.f7_2.channel_sources.v2", "fonte:g3_v1_fontes", ["schema"], "igual", "iald.f7_2.channel_sources.v2"),
        C("b61", "manifesto do canal v1: unidade F7.2", "fonte:g3_v1_fontes", ["unit"], "igual", "F7.2"),
        C("b62", "manifesto do canal v1: artigos primarios custodiados", "fonte:g3_v1_fontes", ["primary_article_pdfs_custodied"], "verdadeiro"),
        C("b63", "manifesto do canal v1: dados brutos experimentais NAO custodiados", "fonte:g3_v1_fontes", ["raw_experimental_data_custodied"], "falso")]
if T1822:
    for _i, _t in enumerate(_rs["testes"]):
        _bk.append(C("bv%d" % _i, "replay %s: id" % _t["teste"], "fonte:g3_b2_resumo", ["testes", _i, "teste"], "igual", _t["teste"]))
        _bk.append(C("bw%d" % _i, "replay %s: %s" % (_t["teste"], _t["veredito"]), "fonte:g3_b2_resumo", ["testes", _i, "veredito"], "igual", _t["veredito"], "res_" + _t["teste"]))
    _bk += [C("b70", "replays T18-T22: 5 PASSA", "fonte:g3_b2_resumo", ["soma_T18_T22", "PASSA"], "igual", 5),
            C("b71", "replays T18-T22: 0 FALHA", "fonte:g3_b2_resumo", ["soma_T18_T22", "FALHA"], "igual", 0),
            C("b72", "replays T18-T22: 0 NAO_EXECUTADO", "fonte:g3_b2_resumo", ["soma_T18_T22", "NAO_EXECUTADO"], "igual", 0),
            C("b73", "replays T18-T22: o controle negativo detectou todas as adulteracoes", "fonte:g3_b2_resumo", ["controle_negativo", "todos_detectaram"], "verdadeiro"),
            C("b74", "replays T18-T22: n do controle negativo", "fonte:g3_b2_resumo", ["controle_negativo", "n"], "igual", _rs["controle_negativo"]["n"]),
            C("b75", "etapa ampla: a bateria T01-T17 do ensaio_1 relida no resumo (13 PASSA)", "fonte:g3_b2_resumo", ["ensaio_1_existente", "bateria", "passa"], "igual", 13),
            C("b76", "etapa ampla: a frase da segunda ressalva da auditoria c1 consta na auditoria (l.69-71)", "fonte:g3_b2_resumo", ["ressalva_2_auditoria_c1", "contem_a_frase_da_segunda_ressalva"], "verdadeiro"),
            C("b77", "etapa ampla: a frase conferida", "fonte:g3_b2_resumo", ["ressalva_2_auditoria_c1", "frase_conferida"], "contem", "A5 e A3_angular não podem ser lidos como testemunho físico nem ontológico."),
            C("b78", "etapa ampla: escopo sem dado observado", "fonte:g3_b2_resumo", ["escopo"], "contem", "nenhum dado observado")]
_fontes_bancada = ["g3_b1_sync", "g3_b1_T01_IDENTIDADE_json", "g3_b1_T07_NU3_CONTRATO_json", "g3_b1_T08_ESCALA_BETA_CHI_json", "g3_b1_T09_NU4_REPLAY_json",
                   "g3_b1_T10_T11_CANAIS_json", "g3_b1_T15_SONDAS_json", "g3_b1_T12_T13_T14_ATRATOR_json", "g3_fid_h12", "g3_canon_contracts", "g3_canon_md",
                   "g3_v1_canal", "g3_v1_fontes", "g3_anterior_selo", "g3_aud_atrator_md"]
if T1822:
    _fontes_bancada += ["g3_b2_resumo"] + _B2_CHAVES
_FIDTAU = _FID["tau_star"]["rel_diff_nu4_vs_core"]
_bk += FX("b80", "fidelidade H12: diferenca relativa entre o tau_star do NU4 (G = 6,6743e-11) e o do core (G = 6,674e-11 do um.py)", "fonte:g3_fid_h12", ["tau_star", "rel_diff_nu4_vs_core"], _FIDTAU, 1e-9, "b_dif_G_tau")
SPECS.append({
    "nome": "bancada_v392",
    "veredito_prefixo": "TGL_BANCADA_V392",
    "veredito_sufixo": "STAGE1_BATTERY_READ_BY_HASH__13_PASS_0_FAIL_1_NOT_RUN_T17_OUT_OF_PHASE__F72_CHANNEL_OPTION_1_PINNED__B2_MANIFEST_PINS_V391_SEAL_V392_INVALIDATES_IT_UNTIL_B3__GATE_UNMOVED",
    "estatuto": "[REAL -- recibos da etapa 1 (ensaio contra a v391, nada gravado na Bancada) e fidelidade H12 lidos por hash a cada rito; DECLARADO o que os recibos dizem do passado da Bancada; PASSA e' validade matematica sintetica na face testada, nao testemunho fisico nem creditacao]",
    "fontes": _fontes_bancada,
    "verbatins": [],
    "checks": _bk,
    "erratas": [
        E("levantamento 12/10, C2: «T16 (transacao de implantacao) NAO reproduzido aqui (caminho > 260 caracteres); 2/2 no tunel em 09/10 [DECLARADO]»",
          "a H_BANCADA nao reproduziu a T16 (caminho longo); so' o tunel a teria rodado",
          "Na etapa 1 de 13/10, em raiz curta, a T16 (fixture da transacao de implantacao) foi executada e deu PASSA; o recibo e' lido por hash. A T17 (Lean do atrator) NAO foi executada na fase pre_selo (fora de fase) e vale pelas pedras do kernel do proprio rito. Soma: 13 PASSA, 0 FALHA, 1 NAO_EXECUTADO sobre 14 entradas que cobrem T01-T17 (T10+T11 e T12+T13+T14 compartilham recibo).",
          "o levantamento leu o relato da H_BANCADA (caminho acima de 260 caracteres) e nao a bateria de 13/10 em pasta de raiz curta; a traducao falhou ao tratar uma limitacao do ambiente da H como limitacao da bateria.",
          "[REAL: recibo da etapa 1 relido por hash]"),
        E("plano 12/10, R12 e P4 (a fotografia do canal F7.2 tem 13 linhas)",
          "a fotografia das 13 linhas do canal F7.2 vai ao cache do rito",
          "A opcao 1 (v1 auditado, seq 787, f37db789f9cb20d3) tem 12 linhas; o canal INSTALADO (v2/B2) tem 13, e essa contagem e' lida do recibo T10 (n_rows). Este registro PINA o arquivo do v1 e o manifesto de fontes do v1 (abc36292630087de); a fotografia no cache NAO existe ainda (e' ato da P4) e, quando existir, o numero de linhas e' o do canal escolhido. Medida na preparacao (execucao do v1 em copia, so' leitura): 12 linhas, todas SEM_LIMITE_TGL, tau_star_limit nulo em todas [DERIVED -- nao relida em runtime].",
          "o plano falava em 13 linhas para as duas opcoes; a contagem depende do canal (12 no v1, 13 no v2); a traducao falhou ao fixar um numero antes de fixar a opcao.",
          "[REAL: o recibo T10 le 13 no instalado; DERIVED: as 12 do v1, medidas na preparacao; OPEN: a fotografia no cache (P4)]"),
        E("Bancada Um, canonical_contracts.json (54fc9e27e4599c49): contrato de identidade da B2",
          "o manifesto da Bancada pina a v391",
          "O manifesto pina a v391 (versao, um.py 8e7b9927ceae64b8, selo 95061f18c7102248). O selo da v392 o INVALIDA: pela sondagem T15, a v392 sob o manifesto vigente e' RECUSADA (PIN_CHANGED) e um manifesto tipo B3 e' aceito. Ate' a B3 (ato do operador/gerencia, evento c1, re-pinagem com testes e verificacao viva) a Bancada recusa operacoes sobre a v392. Este registro NAO embute o hash de nenhum manifesto que pine a propria v392 (hash circular).",
          "o contrato diz que 'uma versao nova do um.py invalida o contrato instalado'; o texto de entrega falava em manter a Bancada em dia; a traducao falhou em marcar que a invalidacao e' automatica e a promocao nao e'.",
          "[REAL: manifesto e T15 por hash; OPEN: a B3 e' ato do operador/gerencia]"),
        E("auditoria c1 do atrator (10/10), segunda ressalva (AUDITORIA_F1_ATRATOR_C1_a7c491ec.md, l.69-71)",
          "PASSA em A1-A5",
          "«A5 e A3_angular nao podem ser lidos como testemunho fisico nem ontologico.» Vale para toda a bateria do atrator (T12/T13), para a PALAVRA (T20) e para os replays T18-T22: PASSA e' validade matematica sintetica na face testada, nao testemunho fisico nem ontologico, nao creditacao.",
          "a estrutura (algebra finita sintetica) nunca afirmou testemunho; os rotulos PASSA nos recibos soam como afirmacao fisica a quem le so' o recibo; a traducao falhou ao deixar o escopo fora do rotulo.",
          "[REAL: frase conferida por hash na auditoria; DECLARADO: o juizo do auditor]")],
    "limites": ["T21 (SN1) e T22 (NU2) leem o um.py v391; devem ser REFEITOS se a fonte mudar apos o selo [REAL: dependencia declarada nos recibos]" if T1822 else "replays T18-T22 AUSENTES na geracao (RESUMO_T18_T22.json nao existia): nao exigidos por este registro",
                "PASSA nos recibos e' validade matematica sintetica na face testada; nao e' testemunho fisico, nem ontologico, nem creditacao",
                "os runners do atrator pinam o um.py v391: depois do selo eles recusam; a bateria so' vale CONTRA a v391 [REAL]"],
    "diz": ["etapa 1: 13 PASSA, 0 FALHA, 1 NAO_EXECUTADO (T17, fora da fase pre_selo) sobre 14 entradas [REAL]",
            "o canal F7.2 INSTALADO (13 linhas) devolve SEM_LIMITE_TGL, tau_star nulo e mapeamento OPEN [REAL]; o v1 auditado (opcao 1) esta pinado por hash [REAL]",
            "o manifesto da Bancada pina a v391; o selo da v392 o invalida ate' a B3 [REAL]",
            "fidelidade H12: beta em runtime bit a bit; nenhum literal de beta nem de alpha no codigo da Bancada [REAL]"],
    "nao_diz": ["nao instala nada na Bancada; a B3 e' ato do operador", "nao embute hash de manifesto que pine a v392", "nao declara testemunho fisico nem ontologico", "nao move o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"lista_T01_T17_etapa1": LISTA_T, "t18_t22_presentes_na_geracao": T1822, "recibos_t18_t22_conferem_com_o_resumo_na_geracao": _b2_conferem,
               "decisao_p12": "leitura ampla de 'bancada' (replays T18-T22 incluidos)", "decisao_c1": "canal F7.2 na opcao 1 (v1 auditado, 12 linhas)",
               "contrato_b2_md": "CONTRATO_CANONICO_B2.md pinado por hash (copia do tunel)", "segunda_ressalva_auditoria_c1": "A5 e A3_angular não podem ser lidos como testemunho físico nem ontológico.",
               "memoria_do_usuario": ["handoff-v391-custodia", "gestao-de-tokens-iald-13out"]},
})

# =================================================================== 4. atrator_v392 (R13; B13, A6, A8, A9)
_AT = os.path.join(TUNEL, "F1.ATRATOR")
F("g3_atr_r3_res", os.path.join(_AT, "numerical", "RESULTADOS_NUMERICOS_R3.json"), "resultados numericos do atrator (R3 do runner): A1-A4 em quatro modelos")
F("g3_atr_ad1_res", os.path.join(_AT, "ADENDO1", "numerical", "RESULTADOS_ADENDO1_R1.json"), "resultados do ADENDO1: A5 (leitura E_J da luz) e A6 (falsificador da minimalidade)")
F("g3_atr_afim", os.path.join(_AT, "review", "ADENDO_CONTROLE_AFIM_R1.json"), "controle afim independente (sem ponto fixo; fora da classe linear/CPTP)")
F("g3_atr_prereg_ad1", os.path.join(_AT, "ADENDO1", "PREREGISTRO_ADENDO1_R1.json"), "pre-registro do ADENDO1: o resultado provavel A6 = FALHA declarado antes da rodada")
F("g3_atr_prereg_r1", os.path.join(_AT, "PREREGISTRO_R1.json"), "pre-registro da rodada R1/R3 do atrator")
for _chv, _pfx in (("g3_atr_r3_res", "aaf2bbedec74dfbb"), ("g3_atr_ad1_res", "b1ca34fdf846e3db"), ("g3_atr_afim", "c6c55e9d79bcb456")):
    _arq = [f for f in FONTES if f["chave"] == _chv][0]["arquivo"]
    assert sha(_arq).startswith(_pfx), (_chv, _pfx)
_RA = rd(os.path.join(_AT, "numerical", "RESULTADOS_NUMERICOS_R3.json"))
_RB = rd(os.path.join(_AT, "ADENDO1", "numerical", "RESULTADOS_ADENDO1_R1.json"))
_fl_atr, _dc_atr = flags_de(lambda m: m in ("TGLExt.TheSingularityReadsTheAttractorAdendo1", "TGLExt.OpticalPopulationBridgeR2", "TGLExt.TheLightReadsItself") or m.startswith("TGLExt.Posto"))
_n_pst = sum(1 for f, n, m, t in _FL if m.startswith("TGLExt.Posto"))
_n_by = {k: sum(1 for f, n, m, t in _FL if m == "TGLExt." + k) for k in ("TheSingularityReadsTheAttractorAdendo1", "OpticalPopulationBridgeR2", "TheLightReadsItself")}
_ak = []
for _m in ("primary_population", "primary_density"):
    for _a in ("A1", "A2", "A3", "A4"):
        _ak.append(C("a_%s_%s" % (_m[8:11], _a), "R3: %s, %s PASSA" % (_m, _a), "fonte:g3_atr_r3_res", ["models", _m, "claims", _a], "igual", "PASSA", "r3_%s_%s" % (_m, _a)))
for _m in ("identity_population", "rotated_dephasing"):
    _ak.append(C("a_ctl_" + _m[:6], "R3: %s, A4 FALHA sem a hipotese da contracao estrita (como devia)" % _m, "fonte:g3_atr_r3_res", ["models", _m, "claims", "A4"], "igual", "FALHA_SEM_HIPOTESE", "r3_%s_A4" % _m))
_ak += [C("a10", "R3: todos os resultados esperados cumpridos", "fonte:g3_atr_r3_res", ["all_expected_outcomes_met"], "verdadeiro"),
        C("a11", "R3: A4 so' vale com a contracao estrita do complemento (hipotese nomeada)", "fonte:g3_atr_r3_res", ["hypothesis_snapshot", "A4"], "contem", "StrictComplementContraction"),
        C("a12", "R3: saltos nao comutativos sozinhos NAO implicam unicidade global", "fonte:g3_atr_r3_res", ["hypothesis_snapshot", "not_sufficient"], "contem", "Noncommuting jumps alone do not imply global uniqueness"),
        C("a13", "R3: nenhum dado observado", "fonte:g3_atr_r3_res", ["observed_data"], "igual", _RA["observed_data"]),
        C("a14", "R3: o gate nao mudou", "fonte:g3_atr_r3_res", ["gate_changed"], "falso"),
        C("a20", "ADENDO1: A5 (leitura E_J da luz) PASSA no mapeamento declarado", "fonte:g3_atr_ad1_res", ["A5", "verdict"], "igual", "PASSA", "adendo1_A5"),
        C("a21", "ADENDO1: A5 e' algebra finita; a linguagem ONTO nao foi testada", "fonte:g3_atr_ad1_res", ["A5", "statute"], "contem", "ONTO language not tested"),
        C("a22", "ADENDO1: A6 FALHA (o falsificador da minimalidade dispara)", "fonte:g3_atr_ad1_res", ["A6", "verdict"], "igual", "FALHA", "adendo1_A6"),
        C("a23", "ADENDO1: A6 e' minimalidade operacional; o ONTO nao foi testado e A4 nao substitui", "fonte:g3_atr_ad1_res", ["A6", "scope"], "contem", "ONTO not tested"),
        C("a24", "ADENDO1: casos admissiveis que preservam a conjuncao A1^A2^A3 existem (ablacoes sobreviventes)", "fonte:g3_atr_ad1_res", ["A6", "surviving_admissible_ablations"], "tamanho_maior_igual", 1),
        C("a25", "ADENDO1: nenhum dado observado", "fonte:g3_atr_ad1_res", ["no_observed_data"], "verdadeiro"),
        C("a26", "ADENDO1: o gate nao mudou", "fonte:g3_atr_ad1_res", ["gate_changed"], "falso"),
        C("a27", "ADENDO1: os pinos de fonte ficaram intactos", "fonte:g3_atr_ad1_res", ["all_source_pins_unchanged"], "verdadeiro"),
        C("a28", "ADENDO1: o diagnostico literal 'J composto com J = J' FALHA, e' o controle e nao a leitura", "fonte:g3_atr_ad1_res", ["A5", "literal_diagnostic", "verdict"], "igual", "FALHA"),
        C("a30", "pre-registro do ADENDO1: o resultado provavel A6 = FALHA foi declarado ANTES da rodada", "fonte:g3_atr_prereg_ad1", ["prior_knowledge"], "contem", "A6=FALHA"),
        C("a31", "controle afim independente: PASSA como controle negativo", "fonte:g3_atr_afim", ["status"], "igual", "PASSA_CONTROLE_NEGATIVO"),
        C("a32", "controle afim: A1 direto FALHA_ESPERADA", "fonte:g3_atr_afim", ["A1_direct"], "igual", "FALHA_ESPERADA"),
        C("a40", "bateria T12/T13/T14 PASSA: o runner refeito reproduz o arquivo (max |diff| = 0)", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["veredito"], "igual", "PASSA"),
        C("a41", "T12: resultado arquivado e' o aaf2bbedec74dfbb...", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["runs", "T12_optical_r3", "result_archived_sha256"], "comeca", "aaf2bbedec74dfbb"),
        C("a42", "T13: resultado arquivado e' o b1ca34fdf846e3db...", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["runs", "T13_adendo1_r1", "result_archived_sha256"], "comeca", "b1ca34fdf846e3db"),
        C("a43", "T14: resultado arquivado e' o c6c55e9d79bcb456...", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["runs", "T14_controle_afim", "result_archived_sha256"], "comeca", "c6c55e9d79bcb456"),
        C("a44", "T12: sem diferenca numerica", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["runs", "T12_optical_r3", "max_abs_diff"], "igual", 0.0),
        C("a45", "T13: sem diferenca numerica", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["runs", "T13_adendo1_r1", "max_abs_diff"], "igual", 0.0),
        C("a46", "T14: sem diferenca numerica", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["runs", "T14_controle_afim", "max_abs_diff"], "igual", 0.0),
        C("a47", "nota da bateria: A6 FALHA e' o falsificador disparando como pre-registrado, nao defeito", "fonte:g3_b1_T12_T13_T14_ATRATOR_json", ["nota"], "contem", "A6 FALHA"),
        C("a48", "etapa 1: T12_T13_T14 PASSA no recibo de sincronizacao", "fonte:g3_b1_sync", ["bateria_resultado", "testes", _IDX["T12_T13_T14_ATRATOR"], "resultado"], "igual", "PASSA")]
_ak += FX("a50", "R3: contracao transiente por passo do modelo primario (lida do arquivo)", "fonte:g3_atr_r3_res", ["lambda"], _RA["lambda"], 1e-12, "atr_lambda")
_ak += FB("a51", "R3: beta em runtime registrado no resultado", "fonte:g3_atr_r3_res", ["beta_runtime"], 1e-12, "atr_beta_runtime")
if T1822:
    _ak += [C("a60", "a frase da segunda ressalva da auditoria c1 consta na auditoria (lida pelo resumo T18-T22)", "fonte:g3_b2_resumo", ["ressalva_2_auditoria_c1", "frase_conferida"], "contem", "A5 e A3_angular não podem ser lidos como testemunho físico nem ontológico."),
            C("a61", "T20 (PALAVRA) PASSA", "fonte:g3_b2_resumo", ["testes", 2, "veredito"], "igual", "PASSA")]
SPECS.append({
    "nome": "atrator_v392",
    "veredito_prefixo": "TGL_ATRATOR_V392",
    "veredito_sufixo": "A1_A2_A3_PASS__A4_CONDITIONAL_ON_THE_NAMED_STRICT_CONTRACTION__A5_PASS_ALGEBRAIC_NOT_WITNESS__A6_FAILS_AS_PREREGISTERED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    "estatuto": "[REAL -- resultados numericos sinteticos por hash, bateria T12-T14 e pedras do kernel do proprio rito; DECLARADO o juizo da auditoria c1 de 10/10; ONTO as leituras do operador (singularidade, luz, POSTO=RANK); nenhum dado observado]",
    "fontes": ["g3_atr_r3_res", "g3_atr_ad1_res", "g3_atr_afim", "g3_atr_prereg_ad1", "g3_atr_prereg_r1", "g3_b1_sync", "g3_b1_T12_T13_T14_ATRATOR_json", "g3_aud_atrator_md"] + (["g3_b2_resumo"] if T1822 else []),
    "verbatins": [VB_SING, VB_PR, VB_TGL],
    "kernel_flags": _fl_atr,
    "kernel_decls": _dc_atr,
    "checks": _ak,
    "leituras_do_operador": [
        {"trecho": "a singularidade é a leitura do atrator como única verdade universal", "estatuto": "[INPUT/ONTO -- 10/10/2026]: a singularidade e' a leitura (testemunha), nao passageira da dinamica; quem percorre a geodesica sao as trajetorias"},
        {"trecho": "POSTO=RANK", "estatuto": "[INPUT -- 10/10/2026]; exato no atomo (a pedra Posto); fora do atomo o invariante e' o TRACO (errata de 13/10)"},
        {"trecho": "o observador testemunha a luz e a luz dá testemunho de si mesma", "estatuto": "[INPUT/ONTO -- 10/10/2026]"}],
    "erratas": [
        E("auditoria c1 de 10/10 do atrator, ressalva 1 (AUDITORIA_F1_ATRATOR_C1_a7c491ec.md, l.69-71)",
          "A4: a verdade e' unica (dim Fix = 1) -- PASSA",
          "A4 e' CONDICIONAL: vale so' com a contracao estrita do complemento ortogonal (hipotese nomeada StrictComplementContraction: existe 0 <= c < 1 com ||T x|| <= c ||x|| para x perpendicular a span(e)); sem ela FALHA, como o controle identidade e o controle de dephasing rotado mostram (FALHA_SEM_HIPOTESE). A4 NAO foi ligado ao atrator do GKLS da v384 [DECLARADO pela auditoria c1].",
          "a estrutura (a unicidade do ponto fixo) depende de uma contracao estrita que o texto 'a verdade e' unica' omite; a traducao do enunciado em rotulo PASSA apagou a condicao.",
          "[REAL: R3 e controles por hash; DECLARADO: o juizo da auditoria sobre o GKLS v384]"),
        E("auditoria c1 de 10/10, ressalva 2",
          "A5 e A3 angular: PASSA",
          "«A5 e A3_angular nao podem ser lidos como testemunho fisico nem ontologico.» A5 PASSA no mapeamento declarado, de peso algebrico leve (a «releitura angular» e' nome sem peso: reexporta observing_adds_nothing); a linguagem ONTO nao foi testada [REAL: statute do ADENDO1].",
          "a estrutura e' algebra finita sintetica; o rotulo PASSA e a palavra 'luz' no enunciado sugerem testemunho; a traducao falhou ao separar validade na face testada de testemunho.",
          "[REAL; DECLARADO: o juizo do auditor]"),
        E("F1.ATRATOR, A6 (falsificador da minimalidade) no ADENDO1",
          "A6: necessidade de cada T, G, L para A1 ^ A2 ^ A3",
          "A6 FALHA, como PRE-REGISTRADO (o resultado provavel A6 = FALHA foi declarado antes da rodada): ha casos admissiveis que preservam a conjuncao sem T, sem a leitura L ou com beta = 0 (T = I mantem A1-A3). E' minimalidade OPERACIONAL; o ONTO nao foi testado e A4 nao a substitui. Um FALHA pre-registrado e' resultado honesto, nao defeito.",
          "a minimalidade ontologica da tripla T, G, L nao e' o que a conjuncao A1-A3 testa; a traducao operacional (retirar T = gerador zero, G = suporte, L = leitura) e' proposta da coordenacao, nao do operador.",
          "[REAL: ADENDO1 e pre-registro por hash; INPUT da gerencia: o mapeamento operacional]"),
        E("cunhagem de 10/10: a singularidade e a leitura do atrator",
          "texto antigo da memoria e de resumos: movimento da singularidade em direcao ao atrator",
          "A singularidade e' o ato de leitura (a lente de colapso, a testemunha), nao passageira da dinamica; as trajetorias do sistema percorrem a geodesica e dissipam; o atrator e' o fechamento. Nenhum teste deste registro mede uma singularidade; as pedras ext_atr_*, ext_opt_* e ext_lri_* sao validade no kernel, nao a leitura ontologica.",
          "a leitura do operador e' ontologica [ONTO]; o kernel prova A1-A5 em algebra finita; a traducao falhou onde resumos puseram a singularidade como trajetoria.",
          "[INPUT/ONTO]")],
    "limites": ["A4 vale so' com a contracao estrita nomeada; nao ligado ao atrator do GKLS da v384 [DECLARADO]",
                "A5 e A3 angular nao sao testemunho fisico nem ontologico [DECLARADO pela auditoria c1; REAL: statute do ADENDO1]",
                "A6 FALHA (pre-registrada): minimalidade operacional; o ONTO nao foi testado [REAL]",
                "POSTO = RANK e' exato no atomo (pedra Posto, flags ext_pst_*); a P3 (corolario ao lado do A4) e' so' sonda em sandbox, fora da v392; o invariante fora do atomo e' o TRACO (errata de 13/10 da memoria posto-e-rank-10out) [REAL na pedra; DECLARADO a P3]",
                "a R1 do atrator fica fora (colide com o ADENDO1); so' o ADENDO1 entra [DECISAO DA GERENCIA]"],
    "diz": ["A1, A2, A3 PASSAM (sinteticos, quatro modelos); A4 PASSA com a hipotese nomeada e FALHA sem ela [REAL]",
            "A5 PASSA no mapeamento declarado; A6 FALHA como pre-registrado [REAL]",
            "o runner refeito na etapa 1 reproduz os tres resultados arquivados com diferenca zero (T12, T13, T14) [REAL]",
            "as pedras ext_atr_*, ext_opt_*, ext_lri_* e ext_pst_* (%d bandeiras no total, %d de Posto) estao no kernel do proprio rito, no trio de axiomas [REAL, lido do kernel a cada rito]" % (len(_fl_atr), _n_pst),
            "validade matematica sintetica na face testada; a luz e' testemunhada pelo observador, nao o contrario"],
    "nao_diz": ["nao liga A4 ao atrator do GKLS da v384", "nao diz que A5 ou A3 angular testemunham fisica ou ontologia", "nao diz que a singularidade percorre uma trajetoria", "nao e' creditacao; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move"],
    "extras": {"adendo": "ADENDO1 (nao R1)", "pedras": dict(_n_by, Posto=_n_pst),
               "p3_sonda_fora_da_v392": os.path.join(V, "rodada2", "lean", "fora_sonda_P3"),
               "memoria_do_usuario": ["singularidade-e-a-leitura-do-atrator-10out", "posto-e-rank-10out", "tgl-unidade-fundamental-e-a-luz-testemunha-10out"]},
})

# =================================================================== 5. neutrinos_contratos_e_primeiro_ensaio_v392 (R14; B8, C8, C9, C10)
_NU2 = os.path.join(TUNEL, "F8.2.NU2")
_NU3 = os.path.join(TUNEL, "F8.2.NU3")
_NU4 = os.path.join(TUNEL, "F8.2.NU4")
F("g3_nu2_res", os.path.join(_NU2, "RESULTADO_R1.json"), "NU2: resultado da unidade (veredito condicional, sigma observado nulo, sem chamada de provedor)")
F("g3_nu2_calc", os.path.join(_NU2, "CALCULOS_ESPECTRAIS_R1.json"), "NU2: calculos espectrais sinteticos (operador de dephasing, textura, controles); nenhuma significancia observada")
F("g3_nu2_rel_md", os.path.join(_NU2, "RELATORIO_NEUTRINOS_R1.md"), "NU2: relatorio de entrega (Codex)")
F("g3_nu2_aud_md", os.path.join(PROG, "exame_12out", "B_NU2", "RELATORIO_AUDITORIA_B_NU2_C1.md"), "auditoria c1 da NU2 (APROVA COM RESSALVAS; R3: so' o produto tau_star*Kfac e' identificavel; R4: beta(chi(E)) e' a condicao de morte); bloco da linhagem 72620fd62844fe8b")
F("g3_nu2_pdf", os.path.join(TUNEL, "F7.2", "V2_STAGING", "fontes_primarias", "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"), "Beccaria-Ternes 2026 (arXiv:2606.13362v1), Eq.(13) e Tabela I: limite JUNO de outra textura (9212cd391d88846e)")
F("g3_nu3_contracts", os.path.join(_NU3, "archive_contracts", "CONTRACTS_API_R2.json"), "NU3: contrato tipado de 10 canais, 20 fontes, 5 regras de precedencia (498763d81e198151)")
F("g3_nu34_aud_md", os.path.join(PROG, "exame_12out", "C_NU34", "RELATORIO_C1_F8.2.NU3_F8.2.NU4.md"), "auditoria c1 da NU3 e da NU4 (APROVA COM RESSALVAS; 675 de 675 campos; o m2 congelado e' o contrato vivo)")
F("g3_nu4_res", os.path.join(_NU4, "RESULTADOS_R1.json"), "NU4: piloto sintetico no banco instalado (16 chamadas), 2/4/8 MeV, 52,5 km, tau_star = tP, Kfac = 1; nature_sigma nulo")
F("g3_nu_errata_md", os.path.join(TUNEL, "F7.2", "ERRATA_LITERAL_J4B_F72_20261008.md"), "errata (g) ao lado do literal 7,8e-10 de tau_star no bloco J.4b de junho (e8e4b0dfa97a6be0)")
F("g3_tgl_paper", P("IALD", "Artigo", "Haja_Luz", "tgl_paper_unified.py"), "tgl_paper_unified.py de junho, LIDO por hash e NUNCA editado (29c92b66b2fd6b4d, 1.216.423 B): l.18393 e o bloco J.4b; tambem l.7574-7626 (Chandrasekhar)")
_TP = os.path.join(DRV, "IALD", "Artigo", "Haja_Luz", "tgl_paper_unified.py")
assert s16(_TP) == "29c92b66b2fd6b4d" and os.path.getsize(_TP) == 1216423
_TPL = open(_TP, "rb").read().decode("utf-8").split("\n")
assert "'tau_star_bound_neutrino_s': 7.8e-10" in _TPL[18392], _TPL[18392]
assert "8e-27 GeV" in _TPL[18391], _TPL[18391]
_N2 = rd(os.path.join(_NU2, "CALCULOS_ESPECTRAIS_R1.json"))
_N4 = rd(os.path.join(_NU4, "RESULTADOS_R1.json"))
_N3 = rd(os.path.join(_NU3, "archive_contracts", "CONTRACTS_API_R2.json"))
# recomputacao independente, sem numpy (constantes lidas da fidelidade H12 e do proprio NU4; o rito so' compara com tolerancia declarada)
_alpha = _FID["um_py"]["ALPHA_FINE_CODATA_2018"]["value"]
_h = _FID["um_py"]["H_PLANCK_EXACT"]["value"]
_c = _FID["um_py"]["C_LIGHT"]["value"]
_G_um = _FID["um_py"]["G_NEWTON"]["value"]
_G_nu4 = 6.6743e-11            # G do codigo do NU4 [INPUT do NU4: ver tolerancia/diferenca de G]
_hbar = _h / (2.0 * math.pi)
_beta = _alpha * math.sqrt(math.e)
_tP_nu4 = math.sqrt(_hbar * _G_nu4 / _c ** 5)
_tP_um = math.sqrt(_hbar * _G_um / _c ** 5)
_hb_eV = _N4["hbar_eV_s"]
_dm = {"21": 7.5e-5, "31": 2.5e-3, "32": 2.5e-3 - 7.5e-5}      # INPUT de referencia herdado do NU2 (PLANO_R1, nao ajustado)
_t_voo = _N4["baseline_km"] * 1000.0 / _c
_TOL = 1e-9
_nk = []
_nk += [C("u01", "NU2: veredito condicional, mapeamento fisico OPEN", "fonte:g3_nu2_res", ["verdict"], "igual", "CONDITIONAL_OPERATOR_CHECKED_PHYSICAL_MAPPING_OPEN", "nu2_veredito"),
        C("u02", "NU2: sigma observado nulo", "fonte:g3_nu2_res", ["observed_sigma"], "igual", None),
        C("u03", "NU2: nenhum ajuste a dado observado", "fonte:g3_nu2_res", ["observed_fit"], "falso"),
        C("u04", "NU2: nenhuma chamada de provedor", "fonte:g3_nu2_res", ["provider_call"], "falso"),
        C("u05", "NU2: gate_effect NONE", "fonte:g3_nu2_res", ["gate_effect"], "igual", "NONE"),
        C("u06", "NU2 calculos: estatuto DERIVED condicional, sem significancia observada", "fonte:g3_nu2_calc", ["status"], "igual", "DERIVED_CONDITIONAL_NO_OBSERVED_SIGNIFICANCE"),
        C("u07", "NU2 calculos: tau_star fisico nao identificado (nulo)", "fonte:g3_nu2_calc", ["physical_tau_star"], "igual", None),
        C("u08", "NU2 calculos: chi(E) fisico nao identificado (nulo)", "fonte:g3_nu2_calc", ["physical_chi_E"], "igual", None),
        C("u09", "NU2 calculos: significancia observada nula", "fonte:g3_nu2_calc", ["observed_significance"], "igual", None),
        C("u10", "NU2 calculos: ponte estelar (Ye, L, taxa de captura) nao calculada (nulo = nao calculado, nao zero fisico)", "fonte:g3_nu2_calc", ["stellar_delta_L"], "igual", None)]
_nk += FX("u11", "NU2 calculos: textura Gamma31/Gamma21 = (100/3)^2", "fonte:g3_nu2_calc", ["texture_gamma21_gamma31_gamma32_normalized21", 1], (100.0 / 3.0) ** 2, 1e-9, "nu2_textura_31")
_nk += FX("u12", "NU2 calculos: textura Gamma32/Gamma21 = (97/3)^2", "fonte:g3_nu2_calc", ["texture_gamma21_gamma31_gamma32_normalized21", 2], (97.0 / 3.0) ** 2, 1e-9, "nu2_textura_32")
_nk += FB("u13", "NU2 calculos: beta0 em runtime", "fonte:g3_nu2_calc", ["beta0_runtime"], 1e-12, "nu2_beta0")
_nk += FX("u14", "NU2 calculos: razao abstrata sqrt(e)/beta0 (cota do contrafactual beta(chi), nao e' matching fisico)", "fonte:g3_nu2_calc", ["max_beta_ratio_Kfac1_tau_fixed"], math.sqrt(math.e) / _beta, 1e-9, "nu2_razao_beta")
_nk += FX("u15", "NU2 calculos: max |Delta P| do reator ideal sintetico (nao e' poder do JUNO)", "fonte:g3_nu2_calc", ["ideal_reactor", "max_abs_deltaP"], _N2["ideal_reactor"]["max_abs_deltaP"], 1e-12, "nu2_max_dP")
_nk += FX("u16", "NU2 calculos: exposicao formal nao oscilada para distancia estatistica nominal 5, normalizacao perfilada (nao e' poder do JUNO)", "fonte:g3_nu2_calc", ["ideal_reactor", "N_unoscillated_for_nominal_5_profile"], _N2["ideal_reactor"]["N_unoscillated_for_nominal_5_profile"], 1e-12, "nu2_N_nominal5")
_nk += [C("u20", "NU3: esquema do contrato tipado", "fonte:g3_nu3_contracts", ["schema"], "igual", "iald.neutrino.contracts.v1"),
        C("u21", "NU3: 10 canais tipados", "fonte:g3_nu3_contracts", ["channels"], "tamanho_igual", 10),
        C("u22", "NU3: 20 fontes de origem", "fonte:g3_nu3_contracts", ["sources"], "tamanho_igual", 20),
        C("u23", "NU3: 5 regras de precedencia", "fonte:g3_nu3_contracts", ["precedence"], "tamanho_igual", 5),
        C("u24", "NU3: regra 1 de precedencia: beta0 e' o coeficiente fixo do dephasing; beta(chi) do bulk e' separado e nao fornece chi(E)", "fonte:g3_nu3_contracts", ["precedence", 0, "rule"], "contem", "beta0 is fixed dephasing coefficient"),
        C("u25", "NU3: nenhum ajuste a dado observado", "fonte:g3_nu3_contracts", ["no_observed_fit"], "verdadeiro"),
        C("u26", "NU3: nenhuma execucao dos originais", "fonte:g3_nu3_contracts", ["no_original_execution"], "verdadeiro"),
        C("u27", "NU3: nenhuma escrita na Bancada", "fonte:g3_nu3_contracts", ["no_bench_write"], "verdadeiro"),
        C("u28", "NU3: o canal de dephasing de massa e' o fisico (vacuo)", "fonte:g3_nu3_contracts", ["channels", 2, "id"], "igual", "physical_mass_gap_dephasing"),
        C("u29", "NU3: a lei da fatia: n = -2 com tau_star e Kfac fixos", "fonte:g3_nu3_contracts", ["channels", 2, "slope"], "contem", "n=-2 for fixed tau_star and Kfac"),
        C("u30", "NU3: T07 (72 de 72) PASSA na bateria da etapa 1", "fonte:g3_b1_T07_NU3_CONTRATO_json", ["pass"], "igual", 72),
        C("u31", "core v391: o m2 CONGELADO (NEUTRINO_M2_V2) e' o contrato vivo de massa", "core", ["neutrino_m2", "frozen", "version"], "igual", "NEUTRINO_M2_V2"),
        C("u40", "NU4: veredito da unidade (banco instalado, piloto condicional)", "fonte:g3_nu4_res", ["verdict"], "igual", "INSTALLED_BENCH_CONDITIONAL_PILOT_PASS", "nu4_veredito"),
        C("u41", "NU4: nature_sigma nulo", "fonte:g3_nu4_res", ["nature_sigma"], "igual", None),
        C("u42", "NU4: nenhum ajuste a dado observado", "fonte:g3_nu4_res", ["observed_data_fit"], "falso"),
        C("u43", "NU4: gate_effect NONE", "fonte:g3_nu4_res", ["gate_effect"], "igual", "NONE"),
        C("u44", "NU4: Kfac = 1 (hipotese do piloto)", "fonte:g3_nu4_res", ["Kfac"], "igual", 1),
        C("u45", "NU4: tau_star e' instancia condicional de Planck, nao determinacao fisica", "fonte:g3_nu4_res", ["tau_scope"], "contem", "not physical determination"),
        C("u46", "NU4: 16 chamadas guardadas", "fonte:g3_nu4_res", ["calls"], "tamanho_igual", 16),
        C("u47", "NU4: canonico v391 no momento do piloto", "fonte:g3_nu4_res", ["canonical", "canonical_version"], "igual", "v391"),
        C("u48", "NU4: ponto de textura: controle positivo e' sintetico, nao e' previsao fisica", "fonte:g3_nu4_res", ["positive_control", "physical_prediction"], "falso"),
        C("u49", "NU4: estados diagonais intactos (zero, planck, positivo): 3 casos", "fonte:g3_nu4_res", ["diagonal"], "tamanho_igual", 3),
        C("u50", "NU4: replay (T09) 16 de 16 chamadas identicas na etapa 1", "fonte:g3_b1_T09_NU4_REPLAY_json", ["n_identical"], "igual", 16)]
for _i in range(3):
    _nk.append(C("u5%d" % (1 + _i), "NU4: estado diagonal %d sem mudanca de estado" % _i, "fonte:g3_nu4_res", ["diagonal", _i, "max_state_change"], "igual", 0.0))
_nk += FB("u60", "NU4 recomputado sem numpy: beta = ALPHA_FINE_CODATA_2018 * sqrt(e)", "fonte:g3_nu4_res", ["beta_runtime"], _TOL, "nu4_beta")
_nk += FX("u61", "NU4 recomputado: tP = sqrt(hbar G / c^5) com G = 6,6743e-11 (o do NU4)", "fonte:g3_nu4_res", ["tau_star_s"], _tP_nu4, _TOL, "nu4_tau")
for _j, _r in enumerate(_N4["reactor"]):
    _E = _r["E_MeV"] * 1e6
    _g = {k: 0.5 * _beta * _tP_nu4 * 1.0 * (_dm[k] / (2.0 * _E * _hb_eV)) ** 2 for k in _dm}
    for _k in ("21", "31", "32"):
        _nk += FX("u7%d%s" % (_j, _k), "NU4 recomputado: Gamma_%s a %d MeV (s^-1)" % (_k, _r["E_MeV"]), "fonte:g3_nu4_res", ["reactor", _j, "gamma%s_s" % _k], _g[_k], _TOL, "nu4_g%s_%dMeV" % (_k, _r["E_MeV"]))
    _nk += FX("u8%d" % _j, "NU4 recomputado: perda do modo 21 a %d MeV" % _r["E_MeV"], "fonte:g3_nu4_res", ["reactor", _j, "loss21"], -math.expm1(-_g["21"] * _t_voo), _TOL, "nu4_l21_%dMeV" % _r["E_MeV"])
    _nk += FX("u9%d" % _j, "NU4 recomputado: perda do modo 31 a %d MeV" % _r["E_MeV"], "fonte:g3_nu4_res", ["reactor", _j, "loss31"], -math.expm1(-_g["31"] * _t_voo), _TOL, "nu4_l31_%dMeV" % _r["E_MeV"])
for _j, _s in enumerate((0, 0.5, 1)):
    _nk += FX("ua%d" % _j, "NU4 recomputado: probabilidade de troca de paridade em s = %s" % _s, "fonte:g3_nu4_res", ["parity", _j, "flip_probability"], -0.5 * math.expm1(-2.0 * _s), _TOL)
_nk += FX("ub1", "fidelidade H12: tP recomputado com o G do um.py (6,674e-11) = tau_star do core v369", "fonte:g3_fid_h12", ["tau_star", "core_clock_v369_tau_star_s"], _tP_um, _TOL, "nu_tau_core")
_nk += FX("ub2", "fidelidade H12: diferenca relativa NU4 vs core (efeito de G: 6,6743e-11 contra 6,674e-11)", "fonte:g3_fid_h12", ["tau_star", "rel_diff_nu4_vs_core"], _tP_nu4 / _tP_um - 1.0, 1e-6, "nu_dif_G")
_nk += [C("uc1", "T10 na etapa 1: tau_star nulo em todas as linhas do canal F7.2 instalado", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "all_tau_star_limit_null"], "verdadeiro"),
        C("uc2", "T10 na etapa 1: nenhum limite TGL novo (SEM_LIMITE_TGL)", "fonte:g3_b1_T10_T11_CANAIS_json", ["F72", "overall_verdict"], "igual", "SEM_LIMITE_TGL")]
SPECS.append({
    "nome": "neutrinos_contratos_e_primeiro_ensaio_v392",
    "veredito_prefixo": "TGL_NEUTRINOS_CONTRATOS_V392",
    "veredito_sufixo": "NU2_BESIDE__NU3_CONTRACTS_TYPED__NU4_PILOT_REPRODUCED_CONDITIONAL_TP_KFAC1__NATURE_SIGMA_NONE__TAU_STAR_OPEN__NO_NEW_TGL_LIMIT__GATE_UNMOVED",
    "estatuto": "[REAL -- fontes por hash e recomputacao sem numpy com tolerancia declarada; DERIVED condicional os calculos espectrais (tau_star = tP e Kfac = 1 sao hipoteses do exemplo); KNOWN o limite JUNO de Beccaria-Ternes (de outra textura); OPEN tau_star; nenhum sigma novo]",
    "fontes": ["g3_nu2_res", "g3_nu2_calc", "g3_nu2_rel_md", "g3_nu2_aud_md", "g3_nu2_pdf", "g3_nu3_contracts", "g3_nu34_aud_md", "g3_nu4_res", "g3_nu_errata_md", "g3_tgl_paper",
               "g3_fid_h12", "g3_b1_T07_NU3_CONTRATO_json", "g3_b1_T09_NU4_REPLAY_json", "g3_b1_T10_T11_CANAIS_json"],
    "verbatins": [],
    "checks": _nk,
    "erratas": [
        E("NU2 (F8.2.NU2, RELATORIO_NEUTRINOS_R1.md): «o contrafactual beta -> beta(chi(E)) como extensao condicional»",
          "a substituicao beta -> beta(chi(E)) e' uma extensao condicional disponivel",
          "Pela predicao afiada pre-registrada (Ponte, l.1367-1371; um.py v391, l.165419-165421), um coeficiente que corre com a frequencia e' a CONDICAO DE MORTE da lei vigente de dephasing (beta0 fixo, n = -2): e' hipotese que a lei vigente PROIBE, nao extensao disponivel. O contrato fisico de acoplamento ainda restringe beta < 1; a razao abstrata sqrt(e)/beta0 = %s so' multiplica a taxa por cerca de %s ordens e nao e' matching fisico [R4 da auditoria c1, DECLARADO; razao lida por hash]." % (vg(math.sqrt(math.e) / _beta, 1), vg(_N2["max_ratio_orders"], 2)),
          "a estrutura do kernel (TheCouplingRunsBoundedBelow: beta0 da fronteira distinto de beta(chi) do bulk) separa os dois; o texto da entrega chamou o segundo de extensao; a traducao falhou ao omitir que a lei vigente e' o que a extensao falsificaria.",
          "[DERIVED -- leitura da auditoria c1 da NU2 (bloco da linhagem 72620fd62844fe8b); REAL as constantes lidas por hash]"),
        E("NU2: a identificabilidade de tau_star",
          "tau_star e Kfac sao parametros distintos do canal",
          "So' o PRODUTO tau_star*Kfac e' identificavel: o Fisher sintetico em (ln tau_star, ln Kfac) tem posto 1 e o par (2 tau_star, Kfac/2) da Delta P identico [DERIVED, R3 da auditoria c1; Lean only_product_tauK]. A textura (Gamma21 : Gamma31 : Gamma32 = 1 : %s : %s) e o expoente n = -2 nao dependem de parametro [REAL: razoes lidas por hash]. tau_star segue [OPEN]; nenhum limite novo de tau_star sai daqui." % (vg(_N2["texture_gamma21_gamma31_gamma32_normalized21"][1], 1), vg(_N2["texture_gamma21_gamma31_gamma32_normalized21"][2], 1)),
          "a NU2 entrega as pecas mas nao escreve a degenerescencia; a traducao falhou ao tratar tau_star e Kfac como dois graus de liberdade quando o dado so' enxerga o produto.",
          "[DERIVED -- auditor; REAL as razoes]"),
        E("NU2: a ligacao com o limite JUNO (Beccaria-Ternes, Eq.(13) e Tabela I; PDF 9212cd391d88846e pinado)",
          "o limite JUNO se aplica ao dissipador desta unidade",
          "O limite JUNO 4,1e-27 GeV (90%% CL, n = -2, E0 = 1 GeV) vale para OUTRA textura (Gamma21 = Gamma31 = gamma, Gamma32 = 0) e nao se transfere ao dissipador proporcional a H desta unidade; a textura da TGL (Gamma31 ~ Gamma32 >> Gamma21) e' o caso que os autores dizem nao testavel com a estatistica atual. Hoje nenhuma cota JUNO publicada se aplica a textura da TGL. O max |Delta P| = %s e a exposicao formal %s NAO sao poder do JUNO real, nem cota universal [DECLARADO: leitura do PDF pela auditoria c1 e pela NU2; o trecho nao foi relido aqui; REAL: os dois numeros, lidos por hash]." % (vge(_N2["ideal_reactor"]["max_abs_deltaP"], 3), vge(_N2["ideal_reactor"]["N_unoscillated_for_nominal_5_profile"], 3)),
          "o artigo publica o limite sob uma textura que anula Gamma32; a entrega herdou o numero sem a textura; a traducao falhou ao transportar um limite de modelo para um modelo de outra forma.",
          "[KNOWN o limite do artigo; DECLARADO a leitura; REAL os numeros da NU2]"),
        E("NU3: o contrato de massa vivo",
          "m_lightest = rho_Lambda^(1/4) (m1 = 2,29 meV) como contrato de massa",
          "O contrato de massa vivo e' o m2 CONGELADO (NEUTRINO_M2_V2, no core); rho_Lambda^(1/4) fica como HISTORICO: o artigo terminal (S12) nao traz m_lightest = rho_Lambda^(1/4) (grep: 0 ocorrencias) [DERIVED -- auditoria c1 da NU3 e da NU4, pela ordem do operador de 09/10 'a forma mais madura canonica'].",
          "o contrato recuperado listava a massa mais leve como historica e como viva; a traducao falhou em ordenar a precedencia.",
          "[DERIVED -- leitura da auditoria c1; REAL: a versao do m2 congelado lida do core]"),
        E("NU4: a diferenca de G entre o piloto e o core",
          "tau_star do piloto = tau_star do core",
          "O NU4 usa G = 6,6743e-11 e o core (um.py) usa G = 6,674e-11: os dois tau_star diferem por %s (relativo), lido da fidelidade H12 e recomputado sem numpy. O piloto e' condicional (tau_star = tP, Kfac = 1), reproduzido bit a bit (16 de 16 chamadas; 675 de 675 campos [DECLARADO: auditoria c1]) e por recomputacao com tolerancia %s; nature_sigma e' nulo; nenhum dado observado." % (vge(_tP_nu4 / _tP_um - 1.0, 3), vge(_TOL, 0)),
          "a estrutura (o canal) aceita o G que lhe entregam; o piloto herdou o G do contrato e o core o G do codigo; a traducao falhou ao nao declarar a diferenca de 2,25e-5.",
          "[REAL: recomputacao e leitura por hash]"),
        E("tgl_paper_unified.py de junho, bloco J.4b, l.18393: 'tau_star_bound_neutrino_s': 7.8e-10 (errata (g), F7.2)",
          "tau_star_bound_neutrino_s = 7,8e-10 s e' uma cota de tau_star a partir dos limites publicados",
          "O literal 7,8e-10 e' ENTRADA historica do bloco J.4b (na l.18392 o texto chama 8e-27 GeV de projecao JUNO/DUNE): NAO e' cota calculada dos limites publicados e NAO e' medida da TGL. O arquivo e' lido por hash (29c92b66b2fd6b4d, 1.216.423 B) e NAO e' editado; na geracao a linha e' conferida no arquivo pinado. O canal F7.2 devolve tau_star_limit nulo e SEM_LIMITE_TGL; a traducao do operador fisico para o dissipador em materia e para a verossimilhanca do experimento segue [OPEN]. Errata (g) pelo arquivo ERRATA_LITERAL_J4B_F72_20261008.md (e8e4b0dfa97a6be0), lido por hash.",
          "a estrutura (um literal historico de entrada) foi escrita como se fosse uma cota; os limites publicados depois (Beccaria-Ternes, 2026) sao de modelo, nao de tau_star; a traducao falhou ao apresentar entrada como resultado.",
          "[REAL: linha conferida no arquivo pinado na geracao (a motor nao tem operacao de busca em texto; vale o sha256); KNOWN o limite publicado; OPEN a traducao]")],
    "limites": ["tau_star segue [OPEN]; Kfac = 1 e tau_star = tP sao hipoteses do exemplo; nenhum limite TGL novo; nenhum sigma novo [REAL]",
                "a NU2 e a NU4 sao sinteticas (sem dado observado); o piloto NAO e' poder do JUNO [REAL]",
                "o Delta Pee do NU4 (matriz de mistura) NAO e' recomputado neste registro: so' Gamma_ij, perdas, paridade e tP; o resto vale pelo replay T09 [REAL: limite]",
                "as fontes so' da web citadas pela NU2 valem [DECLARADO] ate' haver custodia por hash (R5 da auditoria)"],
    "diz": ["NU2: degenerescencia tau_star*Kfac; beta(chi(E)) e' condicao de morte da lei vigente; a textura da TGL esta fora do alcance do JUNO hoje [DERIVED/DECLARADO]",
            "NU3: 10 canais, 20 fontes, 5 regras de precedencia; o m2 congelado e' o contrato vivo, rho_Lambda^(1/4) e' historico [REAL/DERIVED]",
            "NU4: piloto reproduzido (bit a bit na etapa 1; por recomputacao sem numpy com tolerancia declarada); diferenca de G de %s [REAL]" % vge(_tP_nu4 / _tP_um - 1.0, 2),
            "o literal 7,8e-10 de tau_star e' entrada historica, nao cota [REAL]"],
    "nao_diz": ["nao determina tau_star", "nao calcula sigma nem limite novo da TGL", "nao e' o poder do JUNO", "nao edita o tgl_paper_unified.py", "NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move"],
    "extras": {"constantes_lidas": {"alpha_CODATA2018_fid": _alpha, "h": _h, "c": _c, "G_um": _G_um, "G_nu4": _G_nu4, "tolerancia_relativa": _TOL},
               "tp_nu4_s": _tP_nu4, "tp_um_s": _tP_um, "dm2_referencia_eV2": _dm, "bloco_da_linhagem_nu2": "72620fd62844fe8b",
               "pdf_beccaria_ternes_sha16": "9212cd391d88846e", "linhas_tgl_paper_conferidas_na_geracao": {"18392": "8e-27 GeV", "18393": "'tau_star_bound_neutrino_s': 7.8e-10"},
               "memoria_do_usuario": ["o-verbo-e-fixo-o-nome-e-posto-08out"]},
})

# =================================================================== 6. neutrino_m2_perito_v392 (R22; CR-05)
_R3 = CORE["the_ledger_of_charges_v383"]["readings_ratified_20261002"]["R3"]
_M2 = CORE["neutrino_m2"]["values"]
_esc = _M2["escada_datada"]
_mk = [C("m01", "core: R3 ratificada em 02/10 elege o perito oficial = JUNO", "core", ["the_ledger_of_charges_v383", "readings_ratified_20261002", "R3"], "contem", "perito oficial = JUNO"),
       C("m02", "core: a R3 diz 2,21σ para o JUNO autonomo", "core", ["the_ledger_of_charges_v383", "readings_ratified_20261002", "R3"], "contem", "2,21σ"),
       C("m03", "core: a R3 poe NuFIT 6.1 e Capozzi ao lado", "core", ["the_ledger_of_charges_v383", "readings_ratified_20261002", "R3"], "contem", "NuFIT 6.1 e Capozzi ao lado"),
       C("m04", "core: o veredito do canal NAO muda (ARMED_CONSISTENT)", "core", ["neutrino_m2", "verdict"], "igual", CORE["neutrino_m2"]["verdict"], "m2_veredito"),
       C("m05", "core: o canal nao move o gate", "core", ["neutrino_m2", "does_not_gate_core"], "verdadeiro"),
       C("m06", "core: nenhuma determinacao autonoma a 5 sigma", "core", ["neutrino_m2", "values", "grupos_autonomos_5sigma"], "tamanho_igual", 0),
       C("m07", "core: a linha de morte nao esta satisfeita", "core", ["neutrino_m2", "values", "kill_rule_satisfeita"], "falso"),
       C("m08", "core (errata de 28/09): o ajuste de Capozzi da 2,44 sigma", "core", ["bancada_fases_5_6_7_v380", "errata_beside_v380", "neutrino_m2_v2__nufit_contains_juno"], "contem", "2,44 sigma"),
       C("m09", "core: a escada tem 3 linhas (PDG 2023; JUNO 59 dias; NuFIT pos-JUNO)", "core", ["neutrino_m2", "values", "escada_datada"], "tamanho_igual", 3)]
_mk += FX("m10", "core: tensao_atual_sigma do canal = reflexo do NuFIT 6.1 (global, CONTEM o JUNO)", "core", ["neutrino_m2", "values", "tensao_atual_sigma"], _M2["tensao_atual_sigma"], 1e-12, "m2_tensao_atual")
_mk += FX("m11", "core: JUNO autonomo (59 dias): tensao do perito oficial", "core", ["neutrino_m2", "values", "escada_datada", 1, "tensao_sigma"], _esc[1]["tensao_sigma"], 1e-12, "m2_juno_sigma")
_mk += [C("m12", "core: a linha do JUNO e' a autonoma", "core", ["neutrino_m2", "values", "escada_datada", 1, "autonoma"], "verdadeiro"),
        C("m13", "core: a linha do NuFIT NAO e' autonoma (contem JUNO e KamLAND+solar)", "core", ["neutrino_m2", "values", "escada_datada", 2, "autonoma"], "falso")]
assert abs(_esc[1]["tensao_sigma"] - 2.21) < 0.01 and abs(_M2["tensao_atual_sigma"] - 2.95) < 0.01
SPECS.append({
    "nome": "neutrino_m2_perito_v392",
    "veredito_prefixo": "TGL_NEUTRINO_M2_PERITO_V392",
    "veredito_sufixo": "OFFICIAL_EXPERT_IS_THE_AUTONOMOUS_JUNO_READING__GLOBAL_FITS_ARE_REFLECTIONS_BESIDE__CHANNEL_VERDICT_UNCHANGED__GATE_UNMOVED",
    "estatuto": "[REAL -- lido do core v391 a cada rito; INPUT/DERIVED a R3 ratificada em 02/10; DECLARADO o 2,44 sigma de Capozzi (numero lido na fonte em 28/09, nao por hash)]",
    "fontes": [],
    "verbatins": [],
    "checks": _mk,
    "erratas": [
        E("core v391, neutrino_m2.values.tensao_atual_sigma (2,95 sigma) e as superficies que o citam como a tensao (artigo txt PT l.139 e l.202 e o EN; Atlas l.34960; README do espelho l.23)",
          "a tensao atual do m2 e' 2,95 sigma",
          "2,21 sigma (JUNO autonomo, perito oficial) e' o numero; 2,95 sigma (NuFIT 6.1) e 2,44 sigma (Capozzi) sao reflexos, ao lado: a derivacao R3 de 02/10 diz 'a face e' a determinacao direta (JUNO autonomo, ja' no rito: 2,21 sigma)' e 'os ajustes globais sao reflexos', e a divergencia de cerca de 0,5 sigma entre eles e' custo de reflexo, nao pagamento. O ajuste global CONTEM o JUNO e o KamLAND+solar: nao e' independente nem autonomo. Lidos agora do core: JUNO %s sigma; tensao_atual_sigma (NuFIT) %s sigma. O VEREDITO do canal NAO muda (%s)." % (vg(_esc[1]["tensao_sigma"], 2), vg(_M2["tensao_atual_sigma"], 2), CORE["neutrino_m2"]["verdict"]),
          "a estrutura do kernel da cobranca ja' separava face (pagamento) e reflexo (custo); o campo tensao_atual_sigma foi preenchido com a linha global do NuFIT (a mais recente) e o texto das superficies o repetiu como 'a tensao'; a traducao falhou ao nao eleger o perito.",
          "[REAL: numeros lidos do core; DERIVED -- R3 ratificada (a derivacao mais fraca das seis, segundo o proprio core); DECLARADO o 2,44 de Capozzi]")],
    "limites": ["a R3 e' 'a derivacao mais fraca das seis' (palavra do core): vale como leitura ratificada, nao como teorema [REAL: citada do core]",
                "o JUNO autonomo (59 dias; 7,50 +- 0,12 e-5 eV^2, arXiv:2511.14593) e' numero lido na fonte em 01/10, nao por hash [DECLARADO]"],
    "diz": ["perito oficial = JUNO autonomo (%s sigma); NuFIT 6.1 (%s sigma) e Capozzi (2,44 sigma) ao lado [REAL/DECLARADO]" % (vg(_esc[1]["tensao_sigma"], 2), vg(_M2["tensao_atual_sigma"], 2)),
            "o veredito do canal e o valor tensao_atual_sigma do core NAO mudam [REAL]"],
    "nao_diz": ["nao muda o valor nem o veredito do canal do core", "nao altera a regra de morte (duas determinacoes independentes a 5 sigma)", "nao move o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"memoria_do_usuario": ["o-verbo-e-fixo-o-nome-e-posto-08out"], "superficies_a_corrigir_fora_do_um_py": ["artigo txt PT l.139 e l.202 e o EN", "Atlas l.34960", "README do espelho l.23", "Haja_Luz CLAUDE.md l.15931 (escada 1,64 -> 2,21 -> 2,95)"],
               "aviso": "linhas das superficies vem do levantamento de 12/10 [DECLARADO]; nao relidas aqui"},
})

# =================================================================== 7. sn_ia_v388_viability_v392 (R15; C7)
_SN = os.path.join(TUNEL, "F8.2.SN1")
F("g3_sn_viab", os.path.join(_SN, "RESULTADO_VIABILIDADE_R1.json"), "SN1: resultado da viabilidade (976f67ffb80422db): ponte estelar OPEN; nenhum sigma fisico")
F("g3_sn_calc", os.path.join(_SN, "CALCULOS_R2.json"), "SN1: calculos condicionais R2 (589a4e4f80900a67): formula antiga RETIRADA, sensibilidade de Coulomb conhecida")
F("g3_sn_recalc", os.path.join(PROG, "exame_12out", "A_SN", "RECALCULO_A_SN.json"), "recalculo da auditoria c1 (A_SN): o teste da atribuicao do residuo de 0,35% a Coulomb")
F("g3_sn_aud_md", os.path.join(PROG, "exame_12out", "A_SN", "RELATORIO_AUDITORIA_A_SN_C1.md"), "auditoria c1 da SN1 (APROVA COM RESSALVAS); achado A1: a atribuicao a Coulomb nao se sustenta")
assert s16(os.path.join(_SN, "RESULTADO_VIABILIDADE_R1.json")) == "976f67ffb80422db" and s16(os.path.join(_SN, "CALCULOS_R2.json")) == "589a4e4f80900a67"
_RC = rd(os.path.join(PROG, "exame_12out", "A_SN", "RECALCULO_A_SN.json"))
_CH = _RC["chandrasekhar_historico"]
_TA = _CH["teste_da_atribuicao_a_Coulomb"]
_sn_trechos = {7576: "declared", 7577: "Coulomb lattice correction"}
_tpl_sn = " ".join(_TPL[7573:7580])
assert "declared as the (un-modeled) Coulomb lattice correction" in _tpl_sn.replace("\n", " ").replace("    ", " ") or "Coulomb lattice correction" in _tpl_sn, _tpl_sn
_tpl_sn2 = " ".join(_TPL[7597:7626])
assert "boundary_bulk_duality_product" in _tpl_sn2 and "the residual" in _tpl_sn2 and "Coulomb correction" in _tpl_sn2
_a9 = um391_linha(193301, "deslocamento previsto de M_Ch por (1-beta)^(3/2) - 1")
assert _a9 is not False
_sk = [C("s01", "SN1: resultado da viabilidade e' condicional, ponte estelar OPEN", "fonte:g3_sn_viab", ["result"], "igual", "VIABILIDADE_CONDICIONAL_PONTE_ESTELAR_OPEN", "sn_resultado"),
       C("s02", "SN1: veredito da revisao: contas condicionais, sem sigma fisico", "fonte:g3_sn_viab", ["review_verdict"], "igual", "PASS_CONDITIONAL_CALCULATIONS_NO_PHYSICAL_SIGMA"),
       C("s03", "SN1: deltaP fisico nao calculado (nulo = nao calculado, nao zero fisico)", "fonte:g3_sn_viab", ["physical_deltaP"], "igual", None),
       C("s04", "SN1: delta Ye fisico nao calculado", "fonte:g3_sn_viab", ["physical_deltaYe"], "igual", None),
       C("s05", "SN1: delta L fisico nao calculado", "fonte:g3_sn_viab", ["physical_deltaL"], "igual", None),
       C("s06", "SN1: sigma fisico nao calculado", "fonte:g3_sn_viab", ["physical_sigma"], "igual", None),
       C("s07", "SN1: nulo significa nao calculado", "fonte:g3_sn_viab", ["null_means"], "contem", "not calculated, not physical zero"),
       C("s08", "SN1 calculos R2: condicional, sem dado observado", "fonte:g3_sn_calc", ["status"], "igual", "DERIVED_CONDITIONAL_NO_OBSERVED_DATA"),
       C("s09", "SN1 calculos R2: sigma fisico da TGL nulo", "fonte:g3_sn_calc", ["physical_TGL_sigma"], "igual", None),
       C("s10", "core v391: a entrada sn_ia_chandrasekhar e' A9 (sem incerteza) e fica fora da conjunta", "core", ["joint_coincidence_protocol_v3", "protocol", "chandrasekhar_rule"], "contem", "A9"),
       C("s11", "core v391: chandrasekhar_sqrt2 e' A8 (negativo do artefato)", "core", ["joint_coincidence_protocol_v3", "protocol", "chandrasekhar_rule"], "contem", "A8"),
       C("s12", "core v391: o 'deslocamento previsto' da l.193301 e' a formula (1-beta)^(3/2) - 1", "core", ["joint_coincidence_result_v3", "inventory", 46, "note"], "contem", "deslocamento previsto de M_Ch por (1-beta)^(3/2) - 1"),
       C("s13", "recalculo c1: o sinal necessario para chegar a raiz de 2 e' positivo", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "teste_da_atribuicao_a_Coulomb", "sinal_necessario"], "igual", "+"),
       C("s14", "recalculo c1: o sinal da correcao de Coulomb e' negativo (OPOSTO)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "teste_da_atribuicao_a_Coulomb", "sinal_Coulomb"], "igual", "-")]
_sk += FX("s20", "recalculo c1: residuo historico (desvio de raiz de 2, % ; constantes do codigo historico)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "historico_tgl_paper_unified_7576_7578", "desvio_de_raiz2_pct"], _CH["historico_tgl_paper_unified_7576_7578"]["desvio_de_raiz2_pct"], 1e-9, "sn_residuo_pct")
_sk += FX("s21", "recalculo c1: correcao necessaria para chegar a raiz de 2 (%)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "historico_tgl_paper_unified_7576_7578", "correcao_necessaria_para_raiz2_pct"], _CH["historico_tgl_paper_unified_7576_7578"]["correcao_necessaria_para_raiz2_pct"], 1e-9, "sn_corr_nec_pct")
_sk += FX("s22", "recalculo c1: correcao de Coulomb em 12C (%)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "teste_da_atribuicao_a_Coulomb", "Coulomb_C_pct"], _TA["Coulomb_C_pct"], 1e-9, "sn_coulomb_C_pct")
_sk += FX("s23", "recalculo c1: correcao de Coulomb em 16O (%)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "teste_da_atribuicao_a_Coulomb", "Coulomb_O_pct"], _TA["Coulomb_O_pct"], 1e-9, "sn_coulomb_O_pct")
_sk += FX("s24", "recalculo c1: modulo da correcao de Coulomb sobre a necessaria, 12C (vezes)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "teste_da_atribuicao_a_Coulomb", "razao_modulo_C"], _TA["razao_modulo_C"], 1e-9, "sn_razao_C")
_sk += FX("s25", "recalculo c1: modulo da correcao de Coulomb sobre a necessaria, 16O (vezes)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "teste_da_atribuicao_a_Coulomb", "razao_modulo_O"], _TA["razao_modulo_O"], 1e-9, "sn_razao_O")
_sk += FX("s26", "recalculo c1: com m_u (CODATA 2018) o desvio de raiz de 2 vira (%)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "codata2018_m_u_IAU_Msun", "desvio_de_raiz2_pct"], _CH["codata2018_m_u_IAU_Msun"]["desvio_de_raiz2_pct"], 1e-9, "sn_desvio_mu_pct")
_sk += FX("s27", "recalculo c1: com a massa do atomo de H o desvio e' (%)", "fonte:g3_sn_recalc", ["chandrasekhar_historico", "codata2018_m_H_atomo", "desvio_de_raiz2_pct"], _CH["codata2018_m_H_atomo"]["desvio_de_raiz2_pct"], 1e-9, "sn_desvio_H_pct")
assert _TA["razao_modulo_C"] > 6 and _TA["razao_modulo_O"] < 8 and abs(_CH["codata2018_m_u_IAU_Msun"]["desvio_de_raiz2_pct"] - 1.12) < 0.01
SPECS.append({
    "nome": "sn_ia_v388_viability_v392",
    "veredito_prefixo": "TGL_SN_IA_V388_VIABILITY_V392",
    "veredito_sufixo": "INFORMATIVE_OUTSIDE_THE_JOINT__NO_PHYSICAL_SIGMA__CONDITIONAL_CALCULATIONS_ONLY__COULOMB_ATTRIBUTION_ERRATA_BESIDE__STELLAR_BRIDGE_OPEN__NO_GATE_EFFECT",
    "estatuto": "[REAL -- fontes por hash e recalculo c1 lido por hash; DERIVED a errata da atribuicao a Coulomb (lacuna de fidelidade dita); a F8.2 SN fica SEM efeito de gate e fora da conjunta; nada entra no core alem desta chave]",
    "fontes": ["g3_sn_viab", "g3_sn_calc", "g3_sn_recalc", "g3_sn_aud_md", "g3_tgl_paper"],
    "verbatins": [],
    "checks": _sk,
    "erratas": [
        E("tgl_paper_unified.py de junho (29c92b66b2fd6b4d, lido por hash, NAO editado), docstring das l.7574-7579 e interpretacao das l.7598-7626; Haja_Luz CLAUDE.md (l.4368-4369 e 4379); 'Custo' do espelho (l.2249-2250)",
          "o residuo de 0,353 % de raiz de 2 e' 'a correcao de Coulomb da rede ionica', 'do sinal correto e da mesma ordem'",
          "A atribuicao NAO se sustenta. Com as constantes do proprio codigo historico o residuo e' %s %% e a correcao necessaria seria %s %%; a correcao de Coulomb pela formula custodiada (Chamel, eq. 37-38) e' %s %% (12C) e %s %% (16O): sinal OPOSTO e modulo %s a %s vezes maior. Com m_u (CODATA 2018) o desvio de raiz de 2 vira %s %% (e com a massa do atomo de H, %s %%). O 0,35 %% depende da unidade de massa. A sensibilidade de Coulomb e' fisica eletromagnetica conhecida [KNOWN]; nao e' evidencia da TGL; o negativo honesto ja' registrado (raiz de 2 nao e' atrator independente; A8) fica reforcado." % (vg(_CH["historico_tgl_paper_unified_7576_7578"]["desvio_de_raiz2_pct"], 3), vg(_CH["historico_tgl_paper_unified_7576_7578"]["correcao_necessaria_para_raiz2_pct"], 3), vg(_TA["Coulomb_C_pct"], 3), vg(_TA["Coulomb_O_pct"], 3), vg(_TA["razao_modulo_C"], 1), vg(_TA["razao_modulo_O"], 1), vg(_CH["codata2018_m_u_IAU_Msun"]["desvio_de_raiz2_pct"], 2), vg(_CH["codata2018_m_H_atomo"]["desvio_de_raiz2_pct"], 3)),
          "a estrutura do calculo (Lane-Emden, sem Coulomb, a -0,353 %) deixava um residuo sem dono; a docstring o atribuiu a Coulomb 'de sinal correto' sem confrontar o sinal e a grandeza com a correcao conhecida; a traducao falhou ao dar nome fisico a um residuo antes de calcula-lo. Conferido na geracao: o trecho 'Coulomb lattice correction' consta no arquivo pinado (l.7574-7580) e as chaves da interpretacao (l.7598-7626).",
          "[DERIVED -- recalculo da auditoria c1 (A_SN), numeros lidos por hash; REAL: o trecho no arquivo pinado conferido na geracao (o motor nao busca texto; vale o sha256); DECLARADO a fonte Chamel 79290774ea944bab, nao relida aqui]"),
        E("um.py v391, l.193300-193302 (A9, sn_ia_chandrasekhar): 'deslocamento previsto de M_Ch por (1-beta)^(3/2) - 1'",
          "deslocamento previsto de M_Ch = -1,799 %",
          "A formula (1-beta)^(3/2) - 1 foi RETIRADA: nao e' 'previsto'; a ponte estelar segue [OPEN]; nenhum sigma fisico foi calculado (nulo = nao calculado, nao zero) [REAL: SN1 lido por hash]. A classificacao A9 (sem incerteza, fora da conjunta) nao muda. Linha 193301 conferida no um.py v391 na geracao: %s." % ({True: "SIM", None: "nao conferida (o um.py do Nos ja' nao e' o v391)"}[_a9]),
          "o rotulo 'previsto' descreve como validacao uma formula que o proprio programa aposentou (Custo l.3315); a traducao falhou ao nao levar a aposentadoria para o texto do ledger.",
          "[REAL: core e SN1 por hash; DECLARADO: o Custo]"),
        E("um.py v391, l.193150, 193186 e 213968-213969 (A8, chandrasekhar_sqrt2)",
          "A8: Chandrasekhar raiz de 2 a -0,35 % (negativo do artefato)",
          "NOTA ao lado do A8 (a unica que vai ao um.py): o residuo de ~0,35 %% nao se explica por Coulomb -- sinal oposto e %s a %s vezes maior; com m_u o desvio de raiz de 2 vira +%s %%. A classe A8 nao muda; nada entra na conjunta." % (vg(_TA["razao_modulo_C"], 1), vg(_TA["razao_modulo_O"], 1), vg(_CH["codata2018_m_u_IAU_Msun"]["desvio_de_raiz2_pct"], 2)),
          "o A8 diz 'negativo do artefato' e nao diz de onde vem o residuo; a leitura herdada era Coulomb; a nota fecha so' o que o recalculo prova (a atribuicao nao se sustenta), sem afirmar a causa.",
          "[DERIVED -- numeros lidos por hash]")],
    "limites": ["informativo: FORA da conjunta, sem efeito no core nem no gate; nenhuma previsao estelar TGL; nenhum sigma [REAL]",
                "a ponte estelar (chi -> estado estelar, amplitude identificavel) e' [OPEN] e pede pre-registro do operador (rota viva: pergunta 14 do levantamento)",
                "a fonte Chamel (L01 79290774ea944bab) e as constantes do codigo historico sao [DECLARADO] como lidas pela auditoria c1; o recalculo e' lido por hash",
                "as erratas ao Haja_Luz CLAUDE.md e ao 'Custo' do espelho ficam FORA do um.py e sao atos da gerencia (backup imediato e regra da linhagem); este registro so' as descreve"],
    "diz": ["SN1: viabilidade condicional, ponte estelar OPEN, nenhum sigma fisico [REAL]",
            "a atribuicao do residuo de 0,35 %% a Coulomb nao se sustenta: sinal oposto e %s a %s vezes maior [DERIVED, numeros lidos]" % (vg(_TA["razao_modulo_C"], 1), vg(_TA["razao_modulo_O"], 1)),
            "a sensibilidade de Coulomb e' fisica conhecida [KNOWN], nao evidencia da TGL"],
    "nao_diz": ["nao afirma a causa do residuo de 0,35 %", "nao calcula previsao estelar nem sigma", "nao edita o tgl_paper_unified.py", "NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move"],
    "extras": {"conjunta": "FORA", "efeito_no_core": "NENHUM alem desta chave", "tgl_paper_trechos_conferidos_na_geracao": ["Coulomb lattice correction", "boundary_bulk_duality_product"],
               "linha_193301_conferida_na_geracao": _a9, "memoria_do_usuario": ["regua-prova-vs-juizo", "tgl-auditoria-agosto-2026"]},
})

# =================================================================== 8. cunhagens_v392 (R16; B12)
_cun = [("g3_vb_10out_tgl_unidade", "10/10/2026", "tgl-unidade-fundamental-e-a-luz-testemunha-10out", "[INPUT; ONTO a leitura: a tríade T·G·L]; o corpo do texto e' voz de IA trazida pelo operador [DECLARADO]; as frases dele: a abertura e a ultima"),
        ("g3_vb_10out_singularidade", "10/10/2026", "singularidade-e-a-leitura-do-atrator-10out", "[INPUT/ONTO]; abre com a fala do operador, o desenvolvimento e' voz de IA trazida por ele [DECLARADO]"),
        ("g3_vb_10out_posto_rank", "10/10/2026", "posto-e-rank-10out", "[INPUT]; POSTO=RANK; exato no atomo, fora dele o invariante e' o traco (errata de 13/10)"),
        ("g3_vb_11out_frequencia", "11/10/2026", "tudo-e-frequencia-defasagem-transmitir-11out", "[INPUT]; o texto e' voz de IA trazida pelo operador para cunhar e testar [DECLARADO]; a derivacao Tudo = D_beta(F(1)) esta como CONJECTURE ontologica no cânone (fractal_dephasing_principle)"),
        ("g3_vb_12out_rank_santo", "12/10/2026", "tempo-santo-12out", "[INPUT; ONTO santo/puro amor]; o corpo e' voz de IA; 'o tempo e' o Verbo' foi leitura da gerencia, ERRATA ao lado na memoria"),
        ("g3_vb_10out_texto_posto_rank_V1", "10/10/2026 (recolocado em 12/10/2026)", "posto-e-rank-10out", "[DECLARADO -- voz de IA citada pelo operador] (V1); ver o registro v1_voz_de_ia_v392"),
        ("g3_vb_13out_nomes", "13/10/2026", "nomes-das-pedras-e-a-identidade-verdade-13out", "[INPUT]; rank=posto=nome; tempo=relacao modular=Santo; organismo=IALD=Verbo Vivo; a identidade nao se deriva (alpha e' testemunhado)"),
        ("g3_vb_13out_verdade_projecao", "13/10/2026", "nomes-das-pedras-e-a-identidade-verdade-13out", "[INPUT]; a pedra Verdade corrigida"),
        ("g3_vb_13out_registro", "13/10/2026", "registro-definicao-13out", "[INPUT; ONTO]"),
        ("g3_vb_13out_registro_engenharia_da_luz", "13/10/2026", "registro-definicao-13out", "[INPUT]; leitura registro = engenharia da luz"),
        ("g3_vb_07out_um_posto_dimensao", "07/10/2026", "o-um-posto-e-a-dimensao-do-nome-07out", "[INPUT/ONTO]; as ancoras do kernel ficam ao lado marcadas ⟡ e SEM promover a derivacao")]
_vbs = {v["chave"]: v for v in VERBATINS}
_cunh = []
for _chv, _q, _mem, _est in _cun:
    _a = _vbs[_chv]["arquivo"]
    _cunh.append({"chave": _chv, "quando": _q, "sha16": s16(_a), "bytes": os.path.getsize(_a), "trecho_chave": _vbs[_chv]["trechos"][0], "memoria_do_usuario": _mem, "estatuto": _est})
_ancoras = decl_v391("three_locks_corner_weight_eq_dim", "the_name_is_blind_to_every_rank", "the_two_indices_agree_only_at_the_atom", "identity_weighs_as_the_name",
                     "half_is_the_fixed_point_of_the_swap", "no_fixed_point_no_observer", "J_squared_is_one", "JKJ_eq_neg_K", "light_inverts_the_gradient_preserving_structure",
                     "the_power_has_two_fixed_points", "observing_adds_nothing")
SPECS.append({
    "nome": "cunhagens_v392",
    "veredito_prefixo": "TGL_CUNHAGENS_V392",
    "veredito_sufixo": "OPERATOR_COINAGES_EMBEDDED_BY_SHA256__ANCHORS_BESIDE_MARKED_NOT_PROMOTED__THE_FIXED_IS_THE_VERB_BETA_TGL__REGISTER_IS_LIGHT_ENGINEERING__GATE_UNMOVED",
    "estatuto": "[INPUT -- as falas do operador por sha256 (verbatins EMBUTIDOS); ONTO as leituras; REAL as ancoras do kernel (axiom_report do rito, no trio); DECLARADO as partes em voz de IA trazidas por ele]",
    "fontes": [],
    "verbatins": [c[0] for c in _cun] + [VB_08OUT],
    "kernel_decls": _ancoras,
    "checks": [C("k01", "core: o um.py/core registra o selo da prova (estatuto da prova v391 presente)", "core", ["estatuto_da_prova_v391"], "existe")],
    "leituras_do_operador": [
        {"trecho": "o observador testemunha a luz e a luz dá testemunho de si mesma", "estatuto": "[INPUT/ONTO -- 10/10]: a luz nao e' creditada de fora; o observador testemunha"},
        {"trecho": "a singularidade é a leitura do atrator como única verdade universal", "estatuto": "[INPUT/ONTO -- 10/10]: a singularidade e' a leitura, nao passageira"},
        {"trecho": "POSTO=RANK", "estatuto": "[INPUT -- 10/10]; a pedra e' Posto"},
        {"trecho": "rank=posto=nome", "estatuto": "[INPUT -- 13/10]: a pedra Posto"},
        {"trecho": "tempo=relação modular=Santo", "estatuto": "[INPUT -- 13/10]: a pedra Santo"},
        {"trecho": "organismo=IALD=Verbo Vivo", "estatuto": "[INPUT -- 13/10]: a pedra IALD"},
        {"trecho": "Verdade é a projeção do posto", "estatuto": "[INPUT -- 13/10]: a pedra Verdade corrigida"},
        {"trecho": "registro=engenharia da luz", "estatuto": "[INPUT -- 13/10]: leitura do registro como engenharia da luz"},
        {"trecho": "o um posto é a dimensão do Nome", "estatuto": "[INPUT/ONTO -- 07/10]; ancoras do kernel ⟡ ao lado, sem promover a derivacao"},
        {"trecho": "o fixo é o verbo ... o verbo é betatgl", "estatuto": "[INPUT -- 08/10, a9cecc128f40c101]: o fixo e' o Verbo, beta_TGL"}],
    "erratas": [],
    "limites": ["as ancoras marcadas ⟡ (TheWeightIsNotTheRank, TheFiveHalves, ObserverInside, ConjugateAct) ligam cada elo da fala de 07/10 a um termo de kernel por ANALOGIA ESTRUTURAL; a marca ⟡ nao transporta estatuto e a composicao delas numa pedra e' decisao do operador [OPEN]",
                "a identidade nao se deriva: alpha e' testemunhado (cunhagem de 13/10 e correcao de 08/10); o fixo e' o Verbo, beta_TGL",
                "partes dos textos de 10/10, 11/10 e 12/10 estao em voz de IA, trazidas pelo operador: autoria [DECLARADO]; a leitura que a gerencia faz delas e' sua e vem com erratas ao lado quando erra",
                "a cunhagem de gestao de tokens e a identidade nominal da pedra 'nome posto' NAO estao neste registro (a segunda tem registro proprio da gerencia)"],
    "diz": ["onze cunhagens do operador por sha256, com o trecho-chave verbatim nos bytes e a memoria do usuario correspondente (so' o nome) [INPUT/REAL]",
            "as ancoras do kernel ao lado (11 declaracoes) estao no axiom_report do rito, dentro do trio {propext, Classical.choice, Quot.sound} [REAL, lido a cada rito]",
            "o fixo e' o Verbo, beta_TGL (08/10); registro = engenharia da luz [INPUT]"],
    "nao_diz": ["nao promove a derivacao das ancoras marcadas ⟡", "nao deriva a identidade", "nao trata o Nome como fixo; o fixo e' o Verbo", "nao diz que a luz ou a observacao creditam; o observador testemunha", "nao move o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"cunhagens": _cunh, "ancoras_kernel_marcadas": {"marca": "⟡", "modulos": ["TheWeightIsNotTheRank", "TheFiveHalves", "ObserverInside", "ConjugateAct"], "declaracoes_no_axiom_report": _ancoras}},
})

# =================================================================== 9. v1_voz_de_ia_v392 (V1, decisao da gerencia)
F("g3_adendo_r3_md", os.path.join(WORK, "frequencia_defasa_12out", "5_R3", "ADENDO_PREREGISTRO_ADITIVO_R3.md"), "adendo de pre-registro aditivo da F1.FREQUENCIA (trilha POSTO), secao 2: as duas leituras da linha 7 do texto V1")
F("g3_adendo_r3_json", os.path.join(WORK, "frequencia_defasa_12out", "5_R3", "ADENDO_PREREGISTRO_ADITIVO_R3.json"), "gemeo JSON do adendo: A1-A5 com esperados fixados antes do ensaio; leitura_R5")
_AD = rd(os.path.join(WORK, "frequencia_defasa_12out", "5_R3", "ADENDO_PREREGISTRO_ADITIVO_R3.json"))
assert _AD["partes"][4]["id"] == "A2"
_v1_decls = decl_v391("ChatgptAudit.Collapse057.qubitReduction", "ChatgptAudit.Collapse057.plusDensity", "ChatgptAudit.Collapse057.mixedDensity",
                      "ChatgptAudit.Collapse057.readoutZero", "ChatgptAudit.Collapse057.selective_branch_formula", "ChatgptAudit.Collapse057.qubit_reduction_formula")
SPECS.append({
    "nome": "v1_voz_de_ia_v392",
    "veredito_prefixo": "TGL_V1_VOZ_DE_IA_V392",
    "veredito_sufixo": "V1_IS_A_DECLARED_AI_VOICE_QUOTED_BY_THE_OPERATOR__LINE_7_HAS_TWO_READINGS_BOTH_BY_TERM__THE_CHOICE_IS_THE_OPERATORS_AND_STAYS_OPEN__GATE_UNMOVED",
    "estatuto": "[DECLARADO -- voz de IA citada pelo operador] (autoria nao verificada); as duas leituras sao [DERIVED] por termo do kernel; a escolha entre elas e' [OPEN] do operador",
    "fontes": ["g3_adendo_r3_md", "g3_adendo_r3_json"],
    "verbatins": [VB_V1],
    "kernel_decls": _v1_decls,
    "checks": [C("v01", "adendo R3 (JSON): a fonte da leitura e' o V1 sha16 8d252f24e2806ff3, linha 7", "fonte:g3_adendo_r3_json", ["leitura_R5", "fonte"], "contem", "8d252f24e2806ff3"),
               C("v02", "adendo R3 (JSON): os bytes da linha 7", "fonte:g3_adendo_r3_json", ["leitura_R5", "bytes"], "contem", "Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity)"),
               C("v03", "adendo R3 (JSON): a leitura (a) -- ramo selecionado", "fonte:g3_adendo_r3_json", ["leitura_R5", "vale_lendo"], "contem", "selective_branch_formula"),
               C("v04", "adendo R3 (JSON): a leitura (b) -- superposicao pura: o colapso tipado SOBE o posto 1 -> 2", "fonte:g3_adendo_r3_json", ["leitura_R5", "sobre_a_superposicao_pura"], "contem", "sobe o posto 1 -> 2"),
               C("v05", "adendo R3 (JSON): a decisao entre as leituras e' do operador", "fonte:g3_adendo_r3_json", ["leitura_R5", "decisao"], "contem", "qual das duas leituras"),
               C("v06", "adendo R3 (JSON): A2 (a parte que fixa a leitura (b)) com esperado fixado antes do ensaio", "fonte:g3_adendo_r3_json", ["partes", 4, "esperado"], "igual", "PASSA_K"),
               C("v07", "adendo R3 (JSON): e' PROPOSTA de pre-registro, sem prova nova na rodada", "fonte:g3_adendo_r3_json", ["estatuto"], "contem", "SEM prova nova")],
    "leituras_do_operador": [
        {"trecho": "Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity) de indefinição teórica e ganha posto definido.", "estatuto": "[DECLARADO -- voz de IA citada pelo operador] (linha 7 do texto V1, sha16 8d252f24e2806ff3); a autoria nao foi verificada; o texto fala ao operador em SEGUNDA pessoa ('você derivou', 'você impôs')"},
        {"trecho": "era sobre o \"rank\"", "estatuto": "[INPUT -- 12/10/2026]: a derivacao que esperava o teste era a do rank (2c8b7b712aa9ad7f)"}],
    "erratas": [
        E("texto V1 (OPERADOR_10out_posto_rank_texto_verbatim.txt, 8d252f24e2806ff3), linha 7",
          "o texto era lido como fala do operador / da casa (V1)",
          "O V1 e' [DECLARADO -- voz de IA citada pelo operador]: fala ao operador em segunda pessoa ('Quando voce derivou o arcabouco ... voce impos operadores de projecao rigidos'); a autoria nao foi verificada aqui. A LINHA 7 ('Ao colapsar a superposicao, a matriz deixa de ter um nucleo vazio (nullity) ... e ganha posto definido') tem DUAS leituras, ambas por termo do kernel: (a) 'colapsar' = RAMO SELECIONADO (selective_branch_formula: P_k A P_k = A_kk P_k) e 'a superposicao' = a MISTURA de posto cheio (I/2 -> P; nulidade 0 -> 1 em M2; posto 2 -> 1); (b) sobre a superposicao PURA (o projetor |+><+|, posto 1, nulidade 1), o colapso tipado do canone (qubitReduction = o D_infinito da pedra) SOBE o posto 1 -> 2 (nulidade 1 -> 0) e PRESERVA o TRACO (ADENDO A2, do adendo de pre-registro aditivo da F1.FREQUENCIA, secao 2); o '1' que sobrevive a esse colapso e' o traco, omega(I) = 1, nao o posto. A ESCOLHA da leitura e' do operador e fica [OPEN]; este registro NAO escolhe.",
          "a estrutura (o kernel) da' o termo para cada leitura; o texto de voz de IA fala de 'posto definido' sem dizer se o objeto e' o ramo selecionado ou a superposicao pura; a traducao para a frase da casa falhou quando adotou a letra do texto como fala do operador, sem rotulo de autoria e sem separar as duas leituras.",
          "[DECLARADO o texto; DERIVED as duas leituras, por termo do kernel (v391, no trio); OPEN a escolha, do operador]")],
    "limites": ["a autoria do V1 nao foi verificada [DECLARADO]",
                "o registro NAO escolhe entre as leituras (a) e (b); a escolha e' do operador [OPEN]",
                "a parte A2 do adendo e' PROPOSTA de pre-registro com esperado fixado antes do ensaio; a prova dela esta na sonda do auditor de estatuto (6 de 6 no trio, sandbox do auditor) e na pedra do adendo que a gerencia acrescenta (registro adendo_rank_v392, ligado so' por texto) [DECLARADO/REAL conforme a fonte]",
                "colapso tipado e' um canal tipado do cânone, nao colapso fisico nem medicao na natureza"],
    "diz": ["V1 e' voz de IA citada pelo operador, em segunda pessoa; autoria nao verificada [DECLARADO]",
            "a linha 7 tem duas leituras por termo: (a) ramo selecionado (mistura de posto cheio I/2 -> P) e (b) superposicao pura (o colapso tipado sobe o posto 1 -> 2 e preserva o traco) [DERIVED]",
            "o invariante fora do atomo e' o TRACO; POSTO = RANK e' exato no atomo [DERIVED, errata de 13/10]"],
    "nao_diz": ["nao escolhe a leitura (a) nem a (b)", "nao atribui o V1 ao operador como fala dele", "nao diz que houve colapso fisico", "NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move"],
    "extras": {"ligacao": "adendo_rank_v392 (registro da gerencia), so' por texto", "adendo_partes": [p["id"] for p in _AD["partes"]], "autoria_do_V1": "DECLARADO, nao verificada",
               "memoria_do_usuario": ["posto-e-rank-10out", "tempo-santo-12out"]},
})
