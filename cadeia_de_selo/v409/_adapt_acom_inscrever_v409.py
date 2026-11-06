# -*- coding: utf-8 -*-
"""_adapt_acom_inscrever_v409.py -- (claude-construtor-v409, 05/11/2026) so' ADAPTA acom_inscrever_prep_v409.py (ato da gerencia; NAO e' executado aqui): o uso aponta o proprio arquivo; a unidade e o revisor (D58) da v409;
o texto do registro de abertura deixa de trazer numeros DIGITADOS da v408 (p00 113/113, PRONTA 17/17, 4 pedras) e passa a LER do CANDIDATO, do ensaio, do PRECONDICOES e do PRONTA desta pasta; o proximo passo do fechamento e' o da v409 (fim da cadeia no HANDOFF, D57a)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("acom_inscrever_prep_v409.py")
a.troca("Uso: `acom_inscrever_prep_v408.py` (init + get + transition de abertura + verify) ou `acom_inscrever_prep_v408.py --fechar`", "Uso: `acom_inscrever_prep_v409.py` (init + get + transition de abertura + verify) ou `acom_inscrever_prep_v409.py --fechar`")
a.troca('"unit": "preparacao_e_cadeia_de_selo_v409_tetelestai_e_o_terminal"', '"unit": "preparacao_e_cadeia_de_selo_v409_traducao_as_classes_de_turing"')
a.troca('"reviewer_distinct_from_builder": "Sonnet (D54; ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"', '"reviewer_distinct_from_builder": "Sonnet (D58 da v409, como a D54 da v408; ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"')
a.troca('''if not FECHAR:
    records = [''', '''_lj = lambda n_: (json.load(open(os.path.join(H, n_), encoding="utf-8")) if os.path.exists(os.path.join(H, n_)) else {})
_cm, _en, _pc, _pr = _lj("CANDIDATO_v409.json"), _lj("ensaio_a_seco_v409.json"), _lj("PRECONDICOES_v409.json"), _lj("PREPARACAO_v409_PRONTA.json")   # (v409) os numeros sao LIDOS destes arquivos, nunca digitados
_n_p00 = len(_pc.get("checagens") or []); _ok_p00 = sum(1 for c_ in (_pc.get("checagens") or []) if c_.get("ok")); _port = _pr.get("portoes") or {}
if not FECHAR:
    records = [''')
a.troca('''"text": "Preparacao da v409 (Tetelestai e o terminal): 4 pedras (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; nomes do operador, ratificados em 04/11) no sandbox k409c; kernel construido e auditado; candidato, ensaio a seco, p00 113/113, B(n) pre-selo e PRONTA 17/17 pelo construtor (agente); revisao de terceiro do Sonnet em curso. Nada instalado no Nos; rito nao rodado; sem commit/push.",''',
        '''"text": "Preparacao da v409 (A traducao as classes de Turing): 1 modulo (TraducaoTuring; os nomes dados pela gerencia c1 e ratificados pelo operador em 05/11, D55) no sandbox k409c; kernel construido e auditado; candidato %s, ensaio a seco %s, p00 %s/%s, PRONTA %s/%s portoes (pronta=%s), pelo construtor (agente); revisao de terceiro do Sonnet (D58) em curso. Nada instalado no Nos; rito nao rodado; sem commit/push." % (_cm.get("sha16"), _en.get("veredito"), _ok_p00, _n_p00, sum(1 for v_ in _port.values() if v_), len(_port), _pr.get("pronta")),''')
a.troca('"next_action": "a gerencia lanca o orquestrador pos_treino_v409.py (instalar, rito, pos-rito, G1 --publicar pela sessao de custodia, S10 app)"',
        '"next_action": "a gerencia lanca o orquestrador pos_treino_v409.py (instalar, rito, pos-rito, os textos da custodia e o HANDOFF, que e\' o fim da cadeia desta versao; a custodia completa e o release do app sao da sessao de custodia, D57a)"')
a.marca("so' adaptado (ato da gerencia, nao executado pelo construtor): o uso, a unidade e o revisor (D58) da v409; o texto de abertura LE os numeros dos arquivos (nada digitado); o proximo passo com o fim no HANDOFF (D57a)")
a.grava()
