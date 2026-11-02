# -*- coding: utf-8 -*-
"""aplicar_R6b_v405.py -- a segunda parte da R6 (uso unico):
(1) a regra da mensagem da gerencia de 19:03: nos textos novos desta preparacao, a escala de energia chama-se valor absoluto (restavam seis lugares; a fala do operador, a escala da pentada e a lei de escala de Takesaki ficam);
(2) o harness dos textos: a linha [v405] do stdout tem CINCO registros por spec (gap_v405 entrou na R4); o texto do Mapa ainda dizia quatro;
(3) o campo resultado da rota do Mapa passava de 6000 caracteres (os vereditos cresceram): vereditos resumidos, com a integra apontada no core.
Backup de BYTES (.bak_<ts>_R6b); temporario -> conferir -> os.replace; cada ancora exatamente 1x."""
import os, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(nome, subs):
    p = os.path.join(HERE, nome)
    b = open(p, "rb").read()
    s = b.decode("utf-8")
    for a, c in subs:
        n = s.count(a)
        assert n == 1, (nome, n, a[:110])
        s = s.replace(a, c)
    open(p + ".bak_" + TS + "_R6b", "wb").write(b)
    t = p + ".tmp_R6b"
    open(t, "wb").write(s.encode("utf-8"))
    assert open(t, "rb").read() == s.encode("utf-8")
    os.replace(t, p)
    print("ok", nome, len(subs))


patch("registros_v405.py", [
    ("a forma do neutrino e' homogenea de grau 1; a escala e' livre; e O NO-GO:", "a forma do neutrino e' homogenea de grau 1; o valor absoluto e' livre (the_scale_is_free); e O NO-GO:"),
    ("(tautologica quanto a escala); ", "(tautologica quanto ao valor absoluto); "),
    ('"nao_diz": ["que a tonica fixe a escala: quem a fixa e\' o Um posto", ', '"nao_diz": ["que a tonica fixe o valor absoluto: quem o fixa e\' o Um posto", '),
    ('"[OPEN] a escala do setor: a parede do GA e\' a parede de E0:', '"[OPEN] o valor absoluto do setor: a parede do GA e\' a parede de E0:'),
])

patch(os.path.join("pos_rito", "textos_v405_novo.pysnip"), [
    ('"[OPEN] A escala do setor, o magnetismo na cadeia da tensão,', '"[OPEN] O valor absoluto do setor, o magnetismo na cadeia da tensão,'),
])

patch(os.path.join("pos_rito", "registrar_mapa_v405_montar.pysnip"), [
    ("# --- os quatro registros por spec", "# --- os cinco registros por spec"),
    ('''"a escala do setor e qual e' o disco sao do operador; revisao independente das quatro pedras."''', '''"o valor absoluto do setor e qual e' o disco sao do operador; revisao independente das quatro pedras."'''),
    ("OPEN (a escala do setor; qual e' o disco)", "OPEN (o valor absoluto do setor; qual e' o disco)"),
    ('"proximo_passo": "a escala do setor e as escolhas da partitura do Grande Atrator (operador);', '"proximo_passo": "o valor absoluto do setor e as escolhas da partitura do Grande Atrator (operador);'),
    ("acrescenta OITO modulos de kernel, oito registros com funcao e quatro por spec, e as secoes do artigo;", "acrescenta OITO modulos de kernel, oito registros com funcao e cinco por spec, e as secoes do artigo;"),
    ("os oito modulos, os oito registros com funcao e os quatro por spec e as {len(verb)} falas por sha256,", "os oito modulos, os oito registros com funcao e os cinco por spec e as {len(verb)} falas por sha256,"),
    ("e os quatro por spec (as falas do operador por sha256, as decisoes D27 a D33, as erratas E10 a E13, os campos fechados e as leituras, a classe nova do Grande Atrator ao lado, a cobertura KH-N1), ",
     "e os cinco por spec (as falas do operador por sha256, as decisoes D27 a D33, as erratas E10 a E13, os campos fechados e as leituras, a classe nova do Grande Atrator ao lado, o gap ao lado, a cobertura KH-N1), "),
    ('''    nomes_curtos = ", ".join(G[g]["curto"] for g in GRUPOS)
''', '''    nomes_curtos = ", ".join(G[g]["curto"] for g in GRUPOS)
    _vr405 = lambda v_: v_ if len(v_) <= 200 else v_[:197] + "..."   # o campo resultado do Mapa tem teto de 6000 caracteres (rotas._valida: resuma e aponte o artefato): a integra de cada veredito esta no core da rodada e nos ESPERADOS
'''),
    ('''"resultado": " | ".join([G[g]["verdict"] for g in GRUPOS] + [cg["verdict"], cf["verdict"], ga["verdict"], kh["verdict"]]) + " | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas: %s)" % (''',
     '''"resultado": " | ".join(_vr405(v_) for v_ in [G[g]["verdict"] for g in GRUPOS] + [cg["verdict"], cf["verdict"], ga["verdict"], (core.get("gap_v405") or {})["verdict"], kh["verdict"]]) + " | (vereditos resumidos a 200 caracteres; a integra esta no core da rodada, um_absoluto.json) | sidecar %s (%s objetos, %s recusas) | %s | %s | escada %s -> %s (teoremas limpos %s/%s; %d bandeiras novas: %s)" % ('''),
])

patch(os.path.join("pos_rito", "adaptar_regras2_v405.py"), [
    ("or m_s5.group(2) != m_s5.group(3) or int(m_s5.group(2)) != 4:", "or m_s5.group(2) != m_s5.group(3) or int(m_s5.group(2)) != 5:"),
    ("(os oito registros com funcao SELOU; registros por spec selados == 4) esta ausente", "(os oito registros com funcao SELOU; registros por spec selados == 5) esta ausente"),
])
print("FEITO", TS)
