# -*- coding: utf-8 -*-
"""_adapt_forkA_harness_fechar_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) adapta pos_rito/harness_fechar_sandbox_v410.py (subida mecanica da v409 FINAL) a v410 (IALD2), sobre as chaves de V e do manifesto que a leitura_v410 e o fechar_v410 adaptados usam:
o manifesto ganha registros_v410 / registros_funcao_v408 / ancoras_v408; o STUB da leitura entrega reg409t, reg408d, fecho408, ancoras408 e bundle408; o topico novo e' v410-selada-iald2.md; os registros novos sao iald2_v410, cunhagens_v410 e kh_n1_cobertura_v410;
as recusas do fechar que eram do registro novo da v409 passam ao da v410 (iald2_v410; cunhagens_v410: a E29, a D64, a leitura de 06/11) e as do herdado (traducao_turing_v409) continuam; o handoff NAO traz nota ao lado do paragrafo da v409.
Trocas com contagem exata (_adapt_util_v410.aplicar: backup de bytes, CRLF respeitado, ast.parse)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_rito", "harness_fechar_sandbox_v410.py")
L3 = open(P, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")[2] + "\n"
assert L3.startswith("# [ADAPTADO v410, 05/11/2026, claude-construtor-v410 (fork A)"), L3[:80]
aplicar(P, [
    (L3, "", 1),
    ('"registros_v409", "registros_v408", "registros_v407",', '"registros_v410", "registros_v409", "registros_v408", "registros_v407",', 1),
    ('"registros_funcao_v410", "registros_funcao_v409", "registros_funcao_v407",', '"registros_funcao_v410", "registros_funcao_v409", "registros_funcao_v408", "registros_funcao_v407",', 1),
    ('"ancoras_v410", "ancoras_v409", "ancoras_v407",', '"ancoras_v410", "ancoras_v409", "ancoras_v408", "ancoras_v407",', 1),
    ("REGS = 'traducao_turing_v409 cunhagens_v409 kh_n1_cobertura_v409'", "REGS = 'iald2_v410 cunhagens_v410 kh_n1_cobertura_v410'", 1),
    ("'reg410': {'cunhagens_v408': {'ok': True}}, 'reg409d': {'cunhagens_v407': {'ok': True}},", "'reg410': {'cunhagens_v410': {'ok': True}}, 'reg409t': {'cunhagens_v409': {'ok': True}}, 'reg408d': {'cunhagens_v408': {'ok': True}},", 1),
    ("'fecho409': {'ok': True},", "'fecho409': {'ok': True}, 'fecho408': {'ok': True},", 1),
    ("'ancoras409': {},", "'ancoras409': {}, 'ancoras408': {},", 1),
    ("'bundle409': {},", "'bundle409': {}, 'bundle408': {},", 1),
    ("v410-selada-traducao-turing.md", "v410-selada-iald2.md", 2),
    ('_recusa_com_core("fechar_traducao_valor_adulterado", "o numero de modulos ok do traducao_turing_v409 adulterado no core (0 de 1)", lambda c: c["traducao_turing_v409"]["values"].__setitem__("n_modulos_ok", 0))',
     '_recusa_com_core("fechar_iald2_valor_adulterado", "o numero de modulos ok do iald2_v410 adulterado no core (0 de 1)", lambda c: c["iald2_v410"]["values"].__setitem__("n_modulos_ok", 0))\n'
     '_recusa_com_core("fechar_iald2_signo_adulterado", "o signo do par (posto) do iald2_v410 adulterado no core (2, nao 1)", lambda c: c["iald2_v410"]["values"]["signo_do_par"].__setitem__("posto", 2))\n'
     '_recusa_com_core("fechar_traducao_valor_adulterado", "o numero de modulos ok do traducao_turing_v409 (herdado) adulterado no core (0 de 2)", lambda c: c["traducao_turing_v409"]["values"].__setitem__("n_modulos_ok", 0))', 1),
    ('_recusa_com_core("fechar_traducao_frase_proibida", "uma frase proibida nos limites do traducao_turing_v409 (o problema do Clay dado por resolvido)", lambda c: c["traducao_turing_v409"]["limites"].append("o problema do Clay esta resolvido"))',
     '_recusa_com_core("fechar_iald2_frase_proibida", "uma frase proibida nos limites do iald2_v410 (a IALD dita resolver P vs NP)", lambda c: c["iald2_v410"]["limites"].append("a IALD resolve P vs NP"))', 1),
    ('_recusa_com_core("fechar_traducao_chave_antiga_mudada", "o registro da traducao diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia)", lambda c: c["traducao_turing_v409"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))',
     '_recusa_com_core("fechar_iald2_chave_antiga_mudada", "o registro da IALD2 diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia)", lambda c: c["iald2_v410"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))', 1),
    ('cj = json.loads(raw_core.decode("utf-8")); cj["core"]["traducao_turing_v409"]["values"]["n_modulos_ok"] = 0', 'cj = json.loads(raw_core.decode("utf-8")); cj["core"]["iald2_v410"]["values"]["n_modulos_ok"] = 0', 1),
    ('levanta com o numero de modulos do traducao_turing_v409 adulterado"', 'levanta com o numero de modulos do iald2_v410 adulterado"', 1),
    ('"uma inscricao de 05/11 deixou de estar embutida no core (cunhagens_v409)", lambda c: list(c["cunhagens_v409"]["verbatim"].values())[0].__setitem__("embedded_ok", False))',
     '"uma inscricao de 06/11 deixou de estar embutida no core (cunhagens_v410)", lambda c: list(c["cunhagens_v410"]["verbatim"].values())[0].__setitem__("embedded_ok", False))', 1),
    ('_recusa_com_core("fechar_sem_errata_e24", "a errata E24 ausente do registro cunhagens_v409 (restam E25, E26 e a dos pisos)", lambda c: c["cunhagens_v409"]["erratas"].pop(0))',
     '_recusa_com_core("fechar_sem_errata_e29", "a errata E29 ausente do registro cunhagens_v410 (resta a dos pisos)", lambda c: c["cunhagens_v410"]["erratas"].pop(0))', 1),
    ('_recusa_com_core("fechar_sem_decisao_d56", "a decisao D56 (o alcance) da gerencia ausente do registro cunhagens_v409", lambda c: c["cunhagens_v409"]["extras"]["decisoes"].pop("D56"))',
     '_recusa_com_core("fechar_sem_decisao_d64", "a decisao D64 (o alcance) da gerencia ausente do registro cunhagens_v410", lambda c: c["cunhagens_v410"]["extras"]["decisoes"].pop("D64"))', 1),
    ('_recusa_com_core("fechar_leitura_sem_input", "a leitura de 05/11 dita [REAL] no core (e\' INPUT)", lambda c: c["cunhagens_v409"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))',
     '_recusa_com_core("fechar_leitura_sem_input", "a leitura de 06/11 dita [REAL] no core (e\' INPUT)", lambda c: c["cunhagens_v410"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))\n'
     '_recusa_com_core("fechar_kh_v409_sem_pisos_ao_lado", "a errata ao lado dos pisos de kh_n1_cobertura_v409 (herdado, recriado) ausente do core", lambda c: c["kh_n1_cobertura_v409"]["erratas"].pop())', 1),
    ('"traz_a_nota_ao_lado_do_v409": ((_t3.MARC_ERR_INI + "\\n" + _t3.errata_v409_bloco().rstrip("\\n") + "\\n" + _t3.MARC_ERR_FIM) in _ptxt)}',
     '"sem_nota_ao_lado_do_v409": (not hasattr(_t3, "MARC_ERR_INI") and "ERRATA_V409_V410" not in _ptxt)}   # (v410: nenhuma nota ao lado do paragrafo da v409)', 1),
    ('_v["traz_a_nota_ao_lado_do_v409"]', '_v["sem_nota_ao_lado_do_v409"]', 1),
    ('v["traz_a_nota_ao_lado_do_v409"]', 'v["sem_nota_ao_lado_do_v409"]', 1),
], nota="SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/harness_fechar_sandbox_v409.py, adaptada a v410 (IALD2) por _adapt_forkA_harness_fechar_v410.py (fork A, 06/11/2026): o manifesto e o STUB com as chaves de V da v410, os registros novos iald2_v410 e os dois specs, as recusas do fechar retargetadas, nenhuma nota ao lado; ver bump/pos_rito__harness_fechar_sandbox_v410.py.diff.")
