# -*- coding: utf-8 -*-
"""03/11/2026 15:2x, gerencia c1 (R2): o comparar_v406_v407.py recusou o candidato R2 por duas razoes, ambas do patch C19b (o campo fock_face.reading da testemunha ramifica pela chave lida):
(1) o id C19b_testemunha_reading_ramifica nao estava em PATCH_PARA_NOS; (2) o refinamento r_linked exigia que SO a chave do lema mudasse no dict fock_face. Aqui: o mapa ganha o C19b;
o refinamento passa a exigir que mudem EXATAMENTE a chave do lema e o reading, e que o reading novo seja `(<prefixo> if _v407_elo_lido(kf_) else "") + <reading antigo, verbatim>` (o antigo e'
o operando direito, igual no AST); a explicacao do no' diz o C19b. Backup de bytes; py_compile. Escrito pelo Write."""
import json, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
ARQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\comparar_v406_v407.py"
O1 = '"C19_testemunha_linked_vira_leitura": ["testemunha_estatica_v396"], "C20_fechamento_v406_c8": ["v406_fechamento_mechanics"],'
N1 = '"C19_testemunha_linked_vira_leitura": ["testemunha_estatica_v396"], "C19b_testemunha_reading_ramifica": ["testemunha_estatica_v396"], "C20_fechamento_v406_c8": ["v406_fechamento_mechanics"],'
O2 = ('"so_a_chave_do_lema_muda": mudam == ["linked_to_the_corner_by_a_lemma"],')
N2 = ('"so_a_chave_do_lema_e_o_reading_mudam": sorted(mudam) == sorted(["linked_to_the_corner_by_a_lemma", "reading"]),   # [R2, 03/11] C19 + C19b\n'
      '            "reading_novo_guarda_o_antigo_como_operando_direito": isinstance(bd["reading"], ast.BinOp) and isinstance(bd["reading"].op, ast.Add) and dump_eq(bd["reading"].right, ad["reading"]),\n'
      '            "reading_novo_ramifica_pela_chave_lida": isinstance(bd["reading"], ast.BinOp) and isinstance(bd["reading"].left, ast.IfExp) and ast.unparse(bd["reading"].left.test) == "_v407_elo_lido(kf_)" and isinstance(bd["reading"].left.orelse, ast.Constant) and bd["reading"].left.orelse.value == "",')
O3 = ('"testemunha_estatica_v396": "C19 (errata E18): fock_face.linked_to_the_corner_by_a_lemma deixa de ser o literal False e passa a LEITURA do kernel (`_v407_elo_lido(kf_)`), com o campo novo elo_v407; os demais campos e o veredito NAO mudam",')
N3 = ('"testemunha_estatica_v396": "C19 (errata E18): fock_face.linked_to_the_corner_by_a_lemma deixa de ser o literal False e passa a LEITURA do kernel (`_v407_elo_lido(kf_)`), com o campo novo elo_v407; '
      'C19b (R2, 03/11): fock_face.reading ramifica pela MESMA chave lida (prefixo «since v407 the lemma ... is a term» so\' quando o lema e\' lido) e guarda a frase antiga, verbatim, como operando direito; os demais campos e o veredito NAO mudam",')


def f(s):
    for o in (O1, O2, O3):
        assert s.count(o) == 1, ("nao esta UMA vez (%d): %s" % (s.count(o), o[:100]))
    return s.replace(O1, N1).replace(O2, N2).replace(O3, N3), ["PATCH_PARA_NOS + C19b", "r_linked: lema e reading; reading guarda o antigo", "explicacao do no'"]


print(json.dumps(patches.aplicar_em_arquivo(ARQ, f, "r2_c19b"), ensure_ascii=False)[:300])
