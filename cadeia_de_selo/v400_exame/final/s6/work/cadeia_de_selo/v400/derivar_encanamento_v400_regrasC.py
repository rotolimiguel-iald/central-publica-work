# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v400.py: a conferencia das citacoes. Escrito pela ferramenta Write (as barras nao colapsam).
# O mapa subiu 398 -> 399 e 399 -> 400; o que ele nao sabe: os snippets do artigo que esta conferencia le para (e) sao os da v399 (a v400 so' traz a errata, sem fala citada); os rotulos de secoes antigas
# (v398, v399) sao os que o um.py emite; a pedra Testemunho nao esta na pasta da v400; os rotulos novos da errata («beta do runtime») sao rotulos da propria cadeia, nao falas.
entrada("conferir_citacoes_v399.py", autoral=True, regras=[
    # as constantes _V399_* vem do CANDIDATO (o bloco v399 dentro dele) -- o v400_pins.py e' esse bloco, extraido pelo gerador
    ('pins = open(os.path.join(HERE, "v400_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)', 'pins = open(os.path.join(HERE, "v400_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v399 como esta no CANDIDATO v400 (extraido por gerar_candidato_v400.py)', 1),
    # (e) os snippets que citam a declaracao sao os da v399 (a errata da v400 nao cita fala nenhuma)
    ('os.path.join(HERE, "artigo_%s_v400.pysnip" % lang)', 'os.path.join(DL.V399, "artigo_%s_v399.pysnip" % lang)', 1),
    # a pedra Testemunho nao esta na pasta da v400 (ela e' da v399)
    ('"pedra/Testemunho.lean", ', '', 2),
    # os artefatos NOVOS desta cadeia: tambem os snippets da errata
    ('arts = ["runtime_v400.py", "artigo_pt_v400.pysnip", "artigo_en_v400.pysnip", "registros_v400.py", "gerar_candidato_v400.py", "v400_pins.py"]',
     'arts = ["runtime_v400.py", "artigo_pt_v400.pysnip", "artigo_en_v400.pysnip", "registros_v400.py", "gerar_candidato_v400.py", "montar_runtime_v400.py", "v400_pins.py"]', 1),
    # rotulos de secoes ANTIGAS: sao os da v398 e v399 que o um.py emite (o mapa os subiu)
    ('"sonico e a afinacao das cordas (v399)"', '"sonico e a afinacao das cordas (v398)"', 1),
    ('"o testemunho de dois: o selo pela propria tecnologia (v400)"', '"o testemunho de dois: o selo pela propria tecnologia (v399)"', 1),
    # rotulos NOVOS da errata (nomes da checagem do registro; nao sao falas de ninguem)
    ('"nenhuma face sozinha da o um"}', '"nenhuma face sozinha da o um",\n            "beta do runtime", "β do runtime", "$\\\\beta$ do runtime", "$\\\\beta$ of the runtime", "errata ao lado (v400)"}', 1),
])

# ------------------------------------------------------------------------------------------- o diff do kernel e os pinos do B(n): escrito a mao para a v400 (diff_e_pinos_v400.py); nao derivado
