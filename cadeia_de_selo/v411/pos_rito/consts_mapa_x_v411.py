# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-sonnet-posrito-M-v411, a servico do claude-construtor-v411 e da gerencia c1] modulo NOVO, so' meu: as funcoes PURAS e as constantes que o registrar_mapa_v411.py e o gerar_x_custodia_v411.py compartilham
"""consts_mapa_x_v411.py -- (claude-sonnet-posrito-M-v411, 12/11/2026) os FATOS do registro h0dn_bg1_v411 do core, lidos e conferidos UMA vez e usados pelo registro do mapa de rotas e pelo texto curto do X.
Nada aqui e' digitado: todo numero, ramo, ato e ressalva e' LIDO do registro (chaves congeladas pelo construtor: topo `verdict`, `all_verified`, `opened_once`, `cabeca_do_teste`, `outcome`, `linha_ao_lado_cefeidas_livres`,
`ressalvas_secao8`, `o_que_o_teste_nao_decide`; `values.primario`, `values.cefeidas_livres`, `values.atos`); as chaves NAO congeladas (`values.lei_em_km_s_Mpc`, `values.K`, `values.esperado_pelos_agregados`,
`values.c6_max_dif`, `values.n_pinados_do_pre_voo_conferidos`) entram so' se existirem (campo ausente = clausula omitida, nunca inventada). A moldura e as obrigacoes vem de delta_v411 (DESENHO_v411 secao 4):
onde aparecer o Z do primario contra o nulo, a cabeca do teste ou «provado na natureza» ligado a este teste, no MESMO paragrafo/bloco: sob o modelo de erros publicado, a linha das Cefeidas livres com o numero dela,
validade (nao creditacao), retrodicao e nao cego (EN: under the published error model, free Cepheids, validity (not creditation), retrodiction, not blind).
Fail-closed: `fatos_h0dn` levanta AssertionError (mensagem visivel) em qualquer divergencia; nunca devolve fatos parciais."""
import datetime
import hashlib
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
for _p in (HERE, PK):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import delta_v411 as DL  # noqa: E402

CHAVES_TOPO = ("verdict", "all_verified", "opened_once", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide")
CHAVES_PRIMARIO = ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "cabeca_do_teste", "t", "modelo")
CHAVES_CEFEIDAS = ("z_null", "z_tgl", "D", "ramo", "outcome", "t", "modelo")
CHAVES_ATOS = ("commit_do_pre_registro", "push_do_pre_registro_utc", "inicio_da_abertura_utc", "fim_da_abertura_utc", "commit_do_resultado", "push_do_resultado_utc", "commit_do_pre_voo", "repositorio")
N_RESSALVAS = 7
N_NAO_DECIDE = 5
# o gatilho da obrigacao (F67 da guarda_frases_v411): onde o Z do primario contra o nulo, a cabeca do teste ou «provado na natureza» aparecem; o mesmo padrao serve a regra por CAMPO do registrar_mapa_v411
RX_GATILHO_F67 = r"Z\s+(?:do\s+prim[áa]rio\s+)?contra\s+o\s+nulo|\bprim[áa]rio\b[^\n]{0,160}?contra\s+o\s+nulo|prova(?:do|da)\s+na\s+natureza|PROVED_IN_NATURE|BETA_TGL_PRO"
_SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def pt(x_, nd_=2):
    """numero em PT: virgula decimal e o sinal menos de verdade (U+2212)."""
    return ("%.*f" % (nd_, float(x_))).replace(".", ",").replace("-", "−")


def en(x_, nd_=2):
    return "%.*f" % (nd_, float(x_))


def cient_pt(x_):
    m_, e_ = ("%.2e" % float(x_)).split("e")
    return "%s×10%s" % (m_.replace(".", ","), str(int(e_)).translate(_SUP))


def cient_en(x_):
    m_, e_ = ("%.2e" % float(x_)).split("e")
    return "%s×10%s" % (m_, str(int(e_)).translate(_SUP))


def _num(d_, k_, onde_):
    assert k_ in d_, "o registro h0dn_bg1_v411 nao traz %s.%s" % (onde_, k_)
    v_ = d_[k_]
    assert isinstance(v_, (int, float)) and not isinstance(v_, bool) and math.isfinite(float(v_)), "%s.%s nao e' um numero finito (%r)" % (onde_, k_, v_)
    return float(v_)


def _utc(s_):
    """instante ISO 8601 (com Z ou sem fuso => UTC)."""
    assert isinstance(s_, str) and s_, "instante ausente"
    x_ = datetime.datetime.fromisoformat(s_.replace("Z", "+00:00"))
    return x_ if x_.tzinfo else x_.replace(tzinfo=datetime.timezone.utc)


def fatos_h0dn(hd):
    """Le e CONFERE o registro h0dn_bg1_v411 do core (as chaves congeladas) e devolve os FATOS, todos LIDOS (nada digitado). AssertionError em qualquer divergencia."""
    assert isinstance(hd, dict) and hd, "o registro %s esta' ausente do core" % DL.FECHO_REGISTRO
    faltam_ = [k_ for k_ in CHAVES_TOPO if k_ not in hd]
    assert not faltam_, "o registro h0dn_bg1_v411 nao traz as chaves congeladas %s" % faltam_
    assert hd.get("all_verified") is True and hd.get("opened_once") is True, "h0dn_bg1_v411 nao selou (all_verified) ou nao diz que foi aberto uma vez (opened_once)"
    assert hd.get("runtime_executed") is True and hd.get("does_not_gate_core") is True, "h0dn_bg1_v411: runtime_executed e does_not_gate_core tem de ser True (cosmologia nao move o gate)"
    v_ = hd.get("verdict")
    assert isinstance(v_, str) and v_.startswith(DL.VEREDITO_OK_PREFIXO) and v_.endswith(DL.VEREDITO_SUFIXO), "o veredito de maquina do h0dn_bg1_v411 nao tem o prefixo e o sufixo do contrato (recusa ou outro texto)"
    hv_ = hd.get("values") or {}
    pr_, cf_, lado_ = hv_.get("primario") or {}, hv_.get("cefeidas_livres") or {}, hd.get("linha_ao_lado_cefeidas_livres") or {}
    for k_ in CHAVES_PRIMARIO:
        assert k_ in pr_, "values.primario sem a chave %s" % k_
    for k_ in CHAVES_CEFEIDAS:
        assert k_ in cf_, "values.cefeidas_livres sem a chave %s" % k_
    zn_, zk_, d_, p_ = _num(pr_, "z_null", "primario"), _num(pr_, "z_tgl", "primario"), _num(pr_, "D", "primario"), _num(pr_, "p_unilateral", "primario")
    cn_, ck_, dc_ = _num(cf_, "z_null", "cefeidas_livres"), _num(cf_, "z_tgl", "cefeidas_livres"), _num(cf_, "D", "cefeidas_livres")
    rp_, rc_ = pr_["ramo"], cf_["ramo"]
    assert isinstance(rp_, int) and isinstance(rc_, int) and not isinstance(rp_, bool) and not isinstance(rc_, bool), "os ramos (primario, Cefeidas livres) tem de ser inteiros"
    assert pr_["modelo"] != cf_["modelo"], "o primario e as Cefeidas livres sao o MESMO modelo: a linha ao lado nao e' ao lado"
    for k_ in ("modelo", "z_null", "z_tgl", "D", "ramo", "outcome"):
        assert lado_.get(k_) == cf_.get(k_), "a linha ao lado (topo) difere de values.cefeidas_livres em %s" % k_
    assert hd["cabeca_do_teste"] == pr_["cabeca_do_teste"] and isinstance(hd["cabeca_do_teste"], str) and hd["cabeca_do_teste"], "a cabeca do teste do topo difere da de values.primario (ou esta' vazia)"
    assert hd["outcome"] == pr_["outcome"] == cf_["outcome"] and isinstance(hd["outcome"], str) and hd["outcome"], "o desfecho (a palavra do livro de cobrancas) difere entre o topo, o primario e as Cefeidas livres"
    n_ = int(math.floor(zn_))
    assert ("PRIMARY_UNDER_THE_PUBLISHED_MODEL_%dSIGMA_AGAINST_THE_NULL__" % n_) in v_, "o veredito de maquina nao diz o primario sob o modelo publicado a %dSIGMA contra o nulo" % n_
    assert ("__%s" % DL.PREFIXO_DA_FAIXA) in v_ and ("__BRANCH_%d__BESIDE_FREE_CEPHEIDS_" % rp_) in v_ and ("__BRANCH_%d__" % rc_) in v_.split("BESIDE_FREE_CEPHEIDS_", 1)[1], "o veredito de maquina nao traz a faixa (K_LAW_) e os dois ramos nas duas linhas"
    assert ("BELOW_5SIGMA" in v_) == (cn_ < 5.0), "o veredito de maquina diz a linha das Cefeidas livres abaixo/acima de 5 sigma de modo diferente do numero dela"
    assert ("__OUTCOME_%s__" % hd["outcome"]) in v_, "o veredito de maquina nao traz o desfecho lido do registro"
    ress_, nd_ = hd["ressalvas_secao8"], hd["o_que_o_teste_nao_decide"]
    assert isinstance(ress_, list) and len(ress_) == N_RESSALVAS and all(isinstance(x_, str) and x_.strip() for x_ in ress_), "as sete ressalvas (secao 8 do pre-registro) nao estao no registro"
    assert isinstance(nd_, list) and len(nd_) == N_NAO_DECIDE == len(DL.NAO_DECIDE_RESUMO_PT) and all(isinstance(x_, str) and x_.strip() for x_ in nd_), "o que o teste nao decide (secao 6) nao traz os cinco itens"
    at_ = hv_.get("atos") or {}
    for k_ in CHAVES_ATOS:
        assert isinstance(at_.get(k_), str) and at_[k_], "values.atos sem %s" % k_
    t1_, t2_, t2b_, t3_ = _utc(at_["push_do_pre_registro_utc"]), _utc(at_["inicio_da_abertura_utc"]), _utc(at_["fim_da_abertura_utc"]), _utc(at_["push_do_resultado_utc"])
    assert t1_ < t2_ <= t2b_ < t3_, "a ordem dos atos nao e' push do pre-registro < inicio da abertura < push do resultado"
    assert at_["commit_do_pre_voo"] == at_["commit_do_pre_registro"] and at_["commit_do_pre_registro"] != at_["commit_do_resultado"], "o commit do pre-voo nao e' o do pre-registro, ou o do resultado repete o do pre-registro"
    lei_ = hv_.get("lei_em_km_s_Mpc")
    agr_ = hv_.get("esperado_pelos_agregados")
    return {"verdict": v_, "cabeca": hd["cabeca_do_teste"], "cabeca_sha16": hashlib.sha256(hd["cabeca_do_teste"].encode("utf-8")).hexdigest()[:16], "outcome": hd["outcome"], "n_sigma": n_,
            "zn": zn_, "zk": zk_, "D": d_, "p": p_, "ramo_p": rp_, "modelo_p": pr_["modelo"], "cn": cn_, "ck": ck_, "Dc": dc_, "ramo_c": rc_, "modelo_c": cf_["modelo"],
            "zn_pt": pt(zn_), "zk_pt": pt(zk_), "cn_pt": pt(cn_), "ck_pt": pt(ck_), "zn_en": en(zn_), "zk_en": en(zk_), "cn_en": en(cn_), "ck_en": en(ck_),
            "zn4_pt": pt(zn_, 4), "zk4_pt": pt(zk_, 4), "cn4_pt": pt(cn_, 4), "ck4_pt": pt(ck_, 4), "D4_pt": pt(d_, 4), "Dc4_pt": pt(dc_, 4), "p_pt": cient_pt(p_), "p_en": cient_en(p_),
            "ressalvas": list(ress_), "nao_decide": list(nd_), "atos": dict(at_),
            "lei": dict(lei_) if isinstance(lei_, dict) and lei_ else None, "K": hv_.get("K") if isinstance(hv_.get("K"), (int, float)) and not isinstance(hv_.get("K"), bool) else None,
            "agregados": [dict(x_) for x_ in agr_] if isinstance(agr_, list) and agr_ and all(isinstance(x_, dict) for x_ in agr_) else None,
            "c6_max_dif": dict(hv_["c6_max_dif"]) if isinstance(hv_.get("c6_max_dif"), dict) else None, "n_pre_voo": hv_.get("n_pinados_do_pre_voo_conferidos") if isinstance(hv_.get("n_pinados_do_pre_voo_conferidos"), int) else None}


def moldura_pt(F):
    """A moldura da v411 (DESENHO secao 4), com os CINCO obrigatorios e os dois numeros no mesmo trecho: delta_v411.FRASE_MOLDURA_V411_PT preenchida com os numeros LIDOS."""
    return DL.FRASE_MOLDURA_V411_PT % (F["zn_pt"], F["zk_pt"], F["ramo_p"], F["cn_pt"], F["ramo_c"])


def moldura_en(F):
    return DL.FRASE_MOLDURA_V411_EN % (F["zn_en"], F["zk_en"], F["ramo_p"], F["cn_en"], F["ramo_c"])


def cauda_pt(F):
    """As obrigacoes sozinhas (para um bloco que cite o resultado sem repetir a moldura inteira)."""
    return "%s; as %s leem %s (ramo %d); %s sem ajuste, com emenda posterior à guarda, teste %s; provado é %s" % (DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, F["cn_pt"], F["ramo_c"], DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT, DL.OBRIG_VALIDADE_PT)


def cauda_en(F):
    return "%s; the %s read %s (branch %d); %s without fit, with an amendment made after the guard, test %s; proved is %s" % (DL.OBRIG_MODELO_EN, DL.OBRIG_CEFEIDAS_EN, F["cn_en"], F["ramo_c"], DL.OBRIG_RETRO_EN, DL.OBRIG_NAO_CEGO_EN, DL.OBRIG_VALIDADE_EN)


def ressalvas_pt(F):
    return " | ".join("(%d) %s" % (i_ + 1, x_) for i_, x_ in enumerate(F["ressalvas"]))


def cap(s_):
    return s_[:1].upper() + s_[1:]
