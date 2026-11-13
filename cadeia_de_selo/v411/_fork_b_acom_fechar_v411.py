# -*- coding: utf-8 -*-
"""_fork_b_acom_fechar_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) SO' ADAPTA (nao executa: sao atos da gerencia) acom_inscrever_prep_v411.py, fechar_preparacao_v411.py e depositar_construtor_v411.py a v411:
nenhum modulo novo, o teste H0DN x BG1 aberto (o registro h0dn_bg1_v411 recalcula o resultado), a moldura e os numeros LIDOS do PRONTA (que os le do core), a rota cadeia.preparacao_v411 (aberta pelo construtor em
registro_mapa_construtor_v411.json), o revisor (Sonnet, D109) e o fim no HANDOFF; os tres RECUSAM no modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1: o ensaio nao e' preparacao). uso: python -B -X utf8 _fork_b_acom_fechar_v411.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _fork_b_lib_v411 as L  # noqa: E402

RECUSA_ENSAIO = ('if os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1":   # (v411) o ensaio do topo proposto depura a cadeia: nao e\' preparacao; nada vai a memoria, a fila nem ao Mapa\n'
                 '    raise SystemExit("RECUSO: modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1): o artefato de ensaio nao e\' candidato; este ato e\' so\' da preparacao real")\n')

# ---- acom_inscrever_prep_v411.py (ato da gerencia: so' adaptado)
A = "acom_inscrever_prep_v411.py"
_txt = L.linha(A, '                "text": "Preparacao da v411 (IALD2)')
L.aplicar(A, [
    ('"""Memoria ACOM da PREPARACAO da v411 (gerencia c1, 06/11/2026; molde: acom_inscrever_prep_v410.py)', '"""Memoria ACOM da PREPARACAO da v411 (gerencia c1, 12/11/2026; molde: acom_inscrever_prep_v410.py; adaptado pelo fork B do claude-construtor-v411)'),
    ('FECHAR = "--fechar" in sys.argv\n', 'FECHAR = "--fechar" in sys.argv\n' + RECUSA_ENSAIO),
    ('"constraints": {"unit": "preparacao_e_cadeia_de_selo_v411_iald2",', '"constraints": {"unit": "preparacao_e_cadeia_de_selo_v411_h0dn_bg1_aberto", "no_new_kernel_module": True, "the_opening_is_once_the_executor_is_never_rerun": True,'),
    ('"reviewer_distinct_from_builder": "Sonnet (D69 da v411, como a D58 da v410; ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"}}, "init")',
     '"reviewer_distinct_from_builder": "Sonnet (D109 herdada; revisao de terceiro e\' da gerencia)"}}, "init")'),
    (_txt, '                "text": "Preparacao da v411 (o teste H0DN x BG1 aberto uma vez, depois do commit publico do pre-registro; o registro h0dn_bg1_v411 recalcula o resultado dos bytes embutidos): %s modulo novo de kernel (o kernel e\' o da v410); '
           '%s %s, ensaio a seco %s, p00 %s/%s, PRONTA %s/%s portoes (pronta=%s), pelo construtor (agente); revisao de terceiro do Sonnet (D109) a seguir. Nada instalado no Nos; rito nao rodado; sem commit/push." '
           '% (_pr.get("n_modulos_novos"), _pr.get("rotulo_do_artefato") or "candidato", _cm.get("sha16"), _en.get("veredito"), _ok_p00, _n_p00, sum(1 for v_ in _port.values() if v_), len(_port), _pr.get("pronta")),'),
    ('"sources": [S(OBJ), S(os.path.join(H, "BUNDLE_v411.json"))]}]', '"sources": [S(OBJ)] + ([S(os.path.join(H, "CANDIDATO_v411.json"))] if os.path.exists(os.path.join(H, "CANDIDATO_v411.json")) else [])}]'),
    ('"event_id": "prep-v411-aberta-06nov"', '"event_id": "prep-v411-aberta-12nov"'),
], "so' adaptado (ato da gerencia, nao executado pelo construtor): a unidade e as restricoes da inscricao da v411 (sem modulo novo; a abertura e' uma vez); o revisor (D109); o texto de abertura LE os numeros dos arquivos (nada digitado; sem bundle); RECUSA no ensaio do topo proposto")

# ---- fechar_preparacao_v411.py (ato da gerencia: so' adaptado)
F = "fechar_preparacao_v411.py"
_t = open(os.path.join(L.HERE, F), encoding="utf-8").read()
print("--- fechar: linhas com texto da v410 ---")
for i_, l_ in enumerate(_t.split("\n")):
    if any(x_ in l_ for x_ in ("IALD2", "AEscala", "06/11", "09/11", "bundle", "BUNDLE", "D69", "_ABERTA")):
        print(i_ + 1, l_[:220])
