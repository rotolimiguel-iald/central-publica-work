# -*- coding: utf-8 -*-
"""_fork_b_fechar_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) SO' ADAPTA (nao executa: e' ato da gerencia) fechar_preparacao_v411.py: a rota e' LIDA do registro que a abriu (registro_mapa_prep_v411_ABERTA.json
da gerencia, ou, na v411, registro_mapa_construtor_v411.json, do construtor: a rota cadeia.preparacao_v411); a prosa da anotacao e do deposito e' a da v411 (nenhum modulo novo; o teste H0DN x BG1 aberto, recalculado pelo
registro h0dn_bg1_v411; a moldura com as obrigacoes; as ressalvas; E41 a E43), montada do PRONTA e do delta; o revisor (Sonnet, D109); o slug de 12/11; RECUSA no ensaio do topo proposto e sem pronta = true.
uso: python -B -X utf8 _fork_b_fechar_v411.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _fork_b_lib_v411 as L  # noqa: E402

F = "fechar_preparacao_v411.py"
_d6 = L.linha(F, '"""fechar_preparacao_v411.py -- o fim da preparacao')
_d8 = L.linha(F, "FAIL-CLOSED ANTES de qualquer efeito:")
_res = L.linha(F, 'res = ("candidato %s (%s B, base v410 %s); pronta=%s; portoes que passaram: %s;')
_res2 = L.linha(F, '    J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], ", ".join(p_ok)')
_tit = L.linha(F, '         "titulo": "v411 preparada (IALD2 e AEscala, 06 a 09/11/2026): candidato %s; pronta=%s"')
_prox = L.linha(F, '         "proximo_passo": "revisao de terceiro (o Sonnet, D69')
_t41 = L.linha(F, 'txt = ("v411 (IALD2:')
_t42 = L.linha(F, '       "A moldura vale em todo texto:')
_t43 = L.linha(F, '       "As ressalvas vao ditas:')
_t44 = L.linha(F, '       "A Escala (validade no kernel;')
L.aplicar(F, [
    (_d6, '"""fechar_preparacao_v411.py -- o fim da preparacao, depois de gerar_relatorio_v411.py: (1) a ANOTACAO de fechamento da rota do Mapa de Rotas aberta pela preparacao (o rota_id e\' LIDO do registro que a abriu: '
          'registro_mapa_prep_v411_ABERTA.json, se a gerencia o gravou, ou registro_mapa_construtor_v411.json, o da abertura pelo construtor em 12/11: a rota cadeia.preparacao_v411),'),
    (_d8, "FAIL-CLOSED ANTES de qualquer efeito: exige PREPARACAO_v411_PRONTA.json com pronta = true (e nao o ensaio do topo proposto), a SESSION_REFERENCE_prep_v411.json (a inscricao ACOM da preparacao), o registro da abertura da rota e os artefatos que a anotacao cita; sem eles PARA sem efeito."),
    ('HERE = os.path.dirname(os.path.abspath(__file__))\nPR = os.path.join(HERE, "PREPARACAO_v411_PRONTA.json"); J = json.load(open(PR, encoding="utf-8"));',
     'HERE = os.path.dirname(os.path.abspath(__file__))\n'
     'if os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1":   # (v411) o ensaio do topo proposto depura a cadeia: nao e\' preparacao\n'
     '    raise SystemExit("RECUSO: modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1): nada vai ao Mapa, a fila nem a ACOM")\n'
     'import importlib.util as _ilu\n'
     '_sp_dl = _ilu.spec_from_file_location("delta_v411_fechar", os.path.join(HERE, "delta_v411.py")); DL = _ilu.module_from_spec(_sp_dl); _sp_dl.loader.exec_module(DL)   # (v411) a moldura e as listas, LIDAS do DESENHO pelo delta\n'
     'PR = os.path.join(HERE, "PREPARACAO_v411_PRONTA.json"); J = json.load(open(PR, encoding="utf-8"));'),
    ('    print("ja fechada para este PRONTA:", S); sys.exit(0)\n', '    print("ja fechada para este PRONTA:", S); sys.exit(0)\nassert J.get("pronta") is True and not J.get("ensaio_topo_proposto"), ("FAIL-CLOSED: a preparacao nao esta\' pronta", J.get("falta"))\n'),
    ('ABERTA_ = os.path.join(HERE, "registro_mapa_prep_v411_ABERTA.json")',
     'ABERTA_ = os.path.join(HERE, "registro_mapa_prep_v411_ABERTA.json")\nif not os.path.exists(ABERTA_):   # (v411) a rota da preparacao foi aberta pelo construtor, em 12/11, por este registro\n    ABERTA_ = os.path.join(HERE, "registro_mapa_construtor_v411.json")'),
    ('_ab0[0] if isinstance(_ab0, list) else _ab0   # (09/11: o registro ABERTO do Mapa da v411 e\' UM objeto; o da v410 era lista -- achado do revisor Sonnet)',
     '_ab0[0] if isinstance(_ab0, list) else _ab0   # (o registro da abertura e\' UM objeto; aceita-se a lista, como na v409)'),
    (_res, 'fpt = lambda x_: ("%.2f" % x_).replace(".", ",").replace("-", "\\u2212") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "n/d"\n'
           '_pri = (J.get("h0dn") or {}).get("primario") or {}; _cef = (J.get("h0dn") or {}).get("cefeidas_livres") or {}\n'
           'MOLDURA = DL.FRASE_MOLDURA_V411_PT % (fpt(_pri.get("z_null")), fpt(_pri.get("z_tgl")), _pri.get("ramo", "n/d"), fpt(_cef.get("z_null")), _cef.get("ramo", "n/d"))\n'
           'res = ("candidato %s (%s B, base v410 %s); pronta=%s; portoes que passaram: %s; que nao passaram: %s; kernel recibo %s (%s modulo novo: o kernel e\' o da v410); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas" % ('),
    (_tit, '         "titulo": "v411 preparada (o teste H0DN x BG1 aberto e recalculado no rito; nenhum modulo novo): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,'),
    (_prox, '         "proximo_passo": "revisao de terceiro (o Sonnet, D109: uma rodada de conserto e uma conferencia unica; quem constroi nao aprova); depois o orquestrador pos_treino_v411 instala, roda o rito e a cadeia ate\' o HANDOFF; a rota da versao selada sera a da v411",'),
    (_t41 + "\n" + _t42 + "\n" + _t43 + "\n" + _t44 + "\n",
     'txt = ("v411 (o teste decisivo: H0DN x BG1 aberto uma vez, depois do commit publico do pre-registro; a emenda e o resultado RECALCULADO no rito pelo registro %s, a partir dos bytes embutidos; nenhum modulo novo de kernel) '
     'preparada em 12/11/2026 por claude-construtor-v411 para a gerencia c1 (nada instalado; o rito nao rodou). " % DL.FECHO_REGISTRO + res + ".\\n\\n"\n'
     '       + "O teste, do registro (" + str((J.get("h0dn") or {}).get("origem_dos_numeros")) + "): " + MOLDURA + ". O que o teste nao decide: " + "; ".join(DL.NAO_DECIDE_RESUMO_PT) + ". As sete ressalvas: "\n'
     '       + "; ".join("%d %s" % (i_ + 1, r_) for i_, r_ in enumerate(DL.RESSALVAS_ROTULOS_PT)) + ". As erratas ao lado, em nome proprio da gerencia c1: " + ", ".join(DL.ERRATAS_IDS_V411)\n'
     '       + ". P = nP " + DL.D10.FRASE_QUALIFICADOR_PT + " (D64 e D84 da v410).\\n\\n"\n'),
    ('"--alvo", "novo:v411-preparada-06nov", "--casa", "Central de Patentes", "--slug", "v411-preparada-06nov",', '"--alvo", "novo:v411-preparada-12nov", "--casa", "Central de Patentes", "--slug", "v411-preparada-12nov",'),
], "so' adaptado (ato da gerencia, nao executado pelo construtor): a rota lida do registro da abertura (o da gerencia, ou o do construtor de 12/11); a prosa da v411 montada do PRONTA e do delta (nenhum modulo novo; o teste aberto e recalculado; a moldura; as ressalvas; E41 a E43); o revisor (D109); o slug de 12/11; RECUSA no ensaio e sem pronta = true")
