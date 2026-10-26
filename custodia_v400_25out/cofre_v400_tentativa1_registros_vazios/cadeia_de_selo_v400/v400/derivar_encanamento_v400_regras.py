# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v400.py (exec no escopo dele: `entrada(src, dst=None, regras=[(antigo_depois_do_mapa, novo, contagem), ...], prot_extra=(), com_bump=True, autoral=False)`)
# O MAPA sobe 398 -> 399 e 399 -> 400 em todo o texto, menos nos nomes nascidos no um.py; as regras corrigem o que o mapa nao pode saber. Cada regra tem contagem exata; nada e' executado.
# ATENCAO (licao da v396): este arquivo e' escrito pela ferramenta Write, nunca por heredoc do Bash (o heredoc colapsa barras invertidas); os textos com barras usam string RAW (r'...').

# ------------------------------------------------------------------------------------------- a simulacao da arvore do Nos e o exame dos pontos de chamada (a logica e' a mesma; so' o mapa)
entrada("simular_arvore_do_nos_v399.py")
# A base da v400 e' a v399 SELADA: os registros da v399 (selo ACOM, declaracao do operador, cunhagens_v399, kh_n1_cobertura_v399) JA estao no core0. O fluxo do main os RECRIA no mesmo ponto; por isso, como o exame da v399 fez com os da v398,
# eles saem do core ANTES do instantaneo `antes` (senao o proprio recriar vira "chave existente mexida") e comparam-se depois com os do core0 (vereditos_que_mudaram_vs_core0); a conferencia de que so' mudou o que devia e' do ensaio a seco.
entrada("exame_pontos_v399.py", regras=[
    ('+ ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0',
     '+ ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) + ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0', 1),
])

# ------------------------------------------------------------------------------------------- o kernel: construir (so' o Audit, em C:\t\k400c\final, copia do kernel da v399; NENHUM modulo novo)
entrada("construir_kernel_v399.sh", regras=[
    # o comentario de abertura diz o que a v400 faz (o mapa subiu os numeros; o texto da v399 falava de pedra nova)
    sub_n(r"(?m)^# Constroi o kernel do SANDBOX da v400[^\n]*\n",
          "# Constroi o kernel do SANDBOX da v400 (C:\\t\\k400c\\final, COPIA de C:\\t\\k399c\\final; nunca o do Nos): a v400 NAO acrescenta modulo ao kernel (a raiz TGLExt e o Audit sao os da v399, byte a byte); a copia ja' traz tudo compilado em .lake/build.\n"
          "# Para o recibo do kernel ter as linhas `Built` da raiz (TGLExt) e do Audit (TGL.Audit) -- o que o T17 do B(n) exige -- este script apaga SO' os artefatos compilados desses dois modulos (ir/ e lib/lean/), o que obriga o lake a\n"
          "# recompila-los (~200 s cada); a pedra Testemunho e o resto ficam como estao (Replayed). Depois: `lake build` + `lake env lean TGL/Audit.lean`.\n", 1, "comentario de abertura"),
    ('cd "$K" || exit 9\n', 'cd "$K" || exit 9\nfor f in ir/TGL/Audit.c ir/TGL/Audit.c.hash ir/TGL/Audit.setup.json ir/TGLExt.c ir/TGLExt.c.hash ir/TGLExt.setup.json lib/lean/TGL/Audit.ilean lib/lean/TGL/Audit.ilean.hash lib/lean/TGL/Audit.olean lib/lean/TGL/Audit.olean.hash lib/lean/TGL/Audit.trace lib/lean/TGLExt.ilean lib/lean/TGLExt.ilean.hash lib/lean/TGLExt.olean lib/lean/TGLExt.olean.hash lib/lean/TGLExt.trace; do rm -f ".lake/build/$f"; done\n', 1),
])

# ------------------------------------------------------------------------------------------- pos-selo: a arvore so-fontes do recibo (refeita do Nos; sem build)
entrada("refazer_sandbox_v399_pos_selo.sh")
entrada("refazer_arvore_v399_pos_selo.py")

# ------------------------------------------------------------------------------------------- regras de permissao (ESCRITO, NAO rodado)
entrada("regras_v399.py")
