# -*- coding: utf-8 -*-
# regras (lote D3) de derivar_encanamento_v404.py: o diff e os pinos e a conferencia das citacoes. ORIGEM v403. Mapa: 402 -> 403, 403 -> 404.

entrada("diff_e_pinos_v403.py", autoral=True, regras=[
    ("o diff do kernel nao e' so' as tres pedras + a raiz (o Audit nao muda na v404)", "o diff do kernel nao e' so' as duas pedras + a raiz (o Audit nao muda na v404)", 1),
])

_DOC_CIT = '''"""conferir_citacoes_v404.py -- confere, por script, toda inscricao de 28/10/2026 que a v404 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): (a) cada texto embutido em _V404_VERBATINS2 e' IGUAL, byte a byte, ao arquivo
duravel da cadeia (insumos\\\\cunhagens) e o sha256 bate; (b) a fonte original (work\\\\cinco_sigma_fora_da_cosmologia_27out, projecao_transversal_28out e transicao_para_a_massa_28out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v404 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente
as nove inscricoes (todas falas do operador: nenhuma e' da gerencia); (e) as citacoes do operador dos .pysnip existem nos snippets e a fala correspondente esta VERBATIM nos textos do operador; (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE
da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out e as tres pastas de 27 e 28/10), no Atlas, no texto do kernel embutido na base (e os textos da v403 que as erratas citam),
no adendo de 03-04/09, nas fontes das duas pedras, no CLAUDE.md da casa (a regua de beta que a pedra do Nome cita) ou ser rotulo da propria cadeia. Sai 0 se tudo bate. Escrito a mao para a v404 (molde: conferir_citacoes_v403.py)."""
'''
entrada("conferir_citacoes_v403.py", autoral=True, regras=[
    entre('"""conferir_citacoes_v404.py', "import ast, glob, hashlib, json, os, re, sys", _DOC_CIT, "docstring do conferir_citacoes"),
    ('alvo = {"_V403_VERBATINS2", "_V403_SPECS", "_V403_CONTRACTS"}', 'alvo = {"_V404_VERBATINS2", "_V404_SPECS", "_V404_CONTRACTS"}', 1),
    ('V = ns["_V403_VERBATINS2"]; R = {', 'V = ns["_V404_VERBATINS2"]; R = {', 1),
    ("ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V404) == 2", "ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V404) == 9", 1),
    ('startswith("OPERADOR_27out_") for v in V.values()', 'startswith("OPERADOR_28out_") for v in V.values()', 1),
    ('R["nenhuma_e_da_gerencia_as_duas_sao_do_operador"]', 'R["nenhuma_e_da_gerencia_as_nove_sao_do_operador"]', 2),
    ('cg = [s for s in ns["_V403_SPECS"] if s["nome"] == "cunhagens_v403"][0]', 'cg = [s for s in ns["_V404_SPECS"] if s["nome"] == "cunhagens_v404"][0]', 1),
    ('R["leituras"]["cunhagens_v403: " + it["trecho"][:60]]', 'R["leituras"]["cunhagens_v404: " + it["trecho"][:60]]', 1),
    ('CIT_OP = ["a meu ver o nome é", DL.FRASE_CONCORDO]', 'CIT_OP = [DL.FRASE_JO8, DL.FRASE_CONCORDO404]', 1),
    ('_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in glob.glob(os.path.join(DL.WK, "cunhagens_13out", "*OPERADOR_*.txt")))',
     '_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out")], []))', 1),
    ('"caminho, verdade e vida (v404)", "caminho, verdade e vida", "way, truth and life"}',
     '"caminho, verdade e vida (v403)", "caminho, verdade e vida", "way, truth and life",\n'
     '            # v404: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)\n'
     '            "jo 8,32 e a projeção transversal da meia-nat", "jo 8,32 e a projecao transversal da meia-nat", "john 8:32 and the transverse projection of the half-nat", "jo 8,32 e a projeção transversal da meia-nat (v404)", "a transição para a massa", "a transicao para a massa", "o teste da única palavra"}', 1),
])
