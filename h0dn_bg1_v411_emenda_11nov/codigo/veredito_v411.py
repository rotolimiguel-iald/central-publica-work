# -*- coding: utf-8 -*-
"""v411 -- funcao de veredito emendada do teste H0DN x BG1 (nenhum dado observado e' lido).
GERADO por gerar_modulos_v411.py a partir do texto-fonte de veredito_h0dn do um.py (v410); nao editar a mao.
sha256 do texto-fonte v410 (estilo inspect.getsource): e1513b25a36b85cb9eb41bb5db30ba4398a7362e5085b5ef58f381c525676de9
"""


def _v410_h0dn_cabeca(partes_):
    """v410 -- monta a cabeca de um ramo do veredito a partir das PARTES do contrato (a cabeca do ramo da leitura traz a palavra da prova com a validade na MESMA string, D57b/D76; o texto do um.py nunca a traz inteira)."""
    return "".join(partes_)


def veredito_h0dn_v411(z_null, z_tgl, D_esperado, portao_1_ok, ramos):
    """v411 (EMENDA de 11/11, derivada textualmente de veredito_h0dn da v410) -- a funcao de veredito do teste H0DN x BG1 (D72 + E30 + D76): a PRIMEIRA que casa decide. Devolve (cabeca, outcome, ramo).
    EMENDA: a assinatura troca (covariancia_fisica_fechada, no_suporte) por portao_1_ok; so' o ramo (1) muda; (2) a (6) ficam textualmente iguais.
    (1) INCONCLUSIVE_SYSTEMATICS se o primeiro portao do rito (reproducao do numero local publicado, centragem na referencia do fundo, impressao digital) falhar (portao_1_ok falso); (2) a lei K falsificada a 5 sigma a esta sensibilidade se |z_tgl| >= 5;
    (3) subpotente se o D esperado do modelo < 5; (4) a LEITURA do 5 sigma -- beta_TGL provado na natureza (validade, nao creditacao) a n sigma, n = floor(z_null) -- se z_null >= 5 e |z_tgl| <= 1,959963984540054;
    (5) discrimina do LCDM a n sigma com K em tensao de 2 a 5 sigma se z_null >= 5 e 1,96 < |z_tgl| < 5; (6) nao discriminado a sensibilidade disponivel, com a faixa do desvio |z_tgl|, se z_null < 5.
    A palavra do livro de cobrancas (TheLedgerOfCharges, imposta pelo tipo) vai em `outcome`, nunca na cabeca. O sha256 do texto-fonte desta funcao vai ao registro. Nenhum dado observado e' lido nesta versao."""
    import math as _m410
    L_ = float(ramos["limiar"]); C_ = float(ramos["compat_95"]); V_ = ramos["vereditos"]; suf_ = V_["sufixo"]
    zn_ = float(z_null); az_ = abs(float(z_tgl)); D_ = float(D_esperado)
    if not portao_1_ok:
        return V_["inconclusivo"] + suf_, "INCONCLUSIVE", 1
    if az_ >= L_:
        return V_["lei_falsificada"] + suf_, "FALSIFIED", 2
    if D_ < L_:
        return (V_["subpotente"] % ("%.2f" % D_).replace(".", "_")) + suf_, "INCONCLUSIVE", 3
    if zn_ >= L_ and az_ <= C_:
        return _v410_h0dn_cabeca(V_["leitura_partes"]) % int(_m410.floor(zn_)), "NOT_FALSIFIED", 4
    if zn_ >= L_:
        return (V_["tensao"] % int(_m410.floor(zn_))) + suf_, "NOT_FALSIFIED", 5
    faixa_ = V_["faixas"][0] if az_ <= 1.0 else (V_["faixas"][1] if az_ <= 3.0 else V_["faixas"][2])
    return (V_["nao_discriminado"] % faixa_) + suf_, "NOT_FALSIFIED", 6
