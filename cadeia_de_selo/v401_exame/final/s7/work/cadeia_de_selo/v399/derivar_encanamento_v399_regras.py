# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v399.py (exec no escopo dele: `entrada(src, dst=None, regras=[(antigo_depois_do_mapa, novo, contagem), ...], com_bump=True, autoral=False)`)
# O MAPA muda 397 -> 398 e 398 -> 399 em todo o texto, MENOS nos identificadores protegidos (nomes nascidos no um.py); as regras abaixo corrigem o que o mapa nao pode saber: conteudo especifico das pedras
# (Sonico e AfinacaoDasCordas -> Testemunho), o ponto de chamada novo (o selo pela propria tecnologia e a declaracao do operador, logo depois da afinacao das cordas, no main; o sidecar no fim de _unified_main),
# os rotulos que o mapa subiu e nao devia e B8 -> B9. Cada regra tem contagem exata; nada e' executado.
# AUTORAIS (a logica muda; uma subida mecanica nao basta): delta, registros, runtime, gerar_candidato, os .pysnip, copiar_insumos, copiar_base, copiar_pedras e o pos_rito; e, depois da subida mecanica
# abaixo (autoral=True: o derivador NAO sobrescreve o que ja' existe e difere), editados a mao: p00_precondicoes, ensaio_a_seco, conferir_rito, gerar_esperados, gerar_estado, gerar_registro_mapa_prep, conferir_citacoes, comparar e derivar_instalar_rito.
# ATENCAO (licao da v396): este arquivo e' escrito pela ferramenta Write, nunca por heredoc do Bash (o heredoc colapsa barras invertidas); os textos com barras usam string RAW (r'...').
import re


def entre(inicio, fim, novo, nome):
    """regra por FUNCAO: troca o trecho que comeca em `inicio` (unico no texto) e vai ate o comeco de `fim` (unico, depois de `inicio`) por `novo`; ASSERTA as duas ancoras."""
    def fn(t):
        assert t.count(inicio) == 1, ("ancora inicial nao unica", nome, inicio[:70], t.count(inicio))
        i = t.index(inicio)
        assert t.count(fim, i + len(inicio)) >= 1, ("ancora final ausente", nome, fim[:70])
        j = t.index(fim, i + len(inicio))
        return t[:i] + novo + t[j:]
    return (fn, nome, 1)


def sub_n(pat, rep, n, nome=None, flags=0):
    """regra por FUNCAO: re.subn(pat, rep) exigindo exatamente n casamentos."""
    def fn(t):
        t2, c = re.subn(pat, rep, t, flags=flags)
        assert c == n, ("regra sub_n casou %d (esperado %d)" % (c, n), pat[:80])
        return t2
    return (fn, nome or ("sub_n:" + pat[:50]), n)


# ------------------------------------------------------------------------------------------- guarda P18 (identica; so' o mapa e o nome)
entrada("guarda_p18_v398.py")

# ------------------------------------------------------------------------------------------- o QUADRO do Teste da Unica Palavra (v397): COPIAS que a cadeia v399 so' IMPORTA para conferir (o quadro nao se mexe; os nomes ficam)
entrada("runtime_quadro_v397.py", dst="runtime_quadro_v397.py", com_bump=False)
entrada("quadro_v397.py", dst="quadro_v397.py", com_bump=False, regras=[
    ("import delta_v398 as DL  # noqa: E402", "import delta_v399 as DL  # noqa: E402", 1),
    ("\"\"\"quadro_v397.py [copia na cadeia v398: so' o import do delta mudou; o quadro nao se mexe] -- o lado da CADEIA do quadro", "\"\"\"quadro_v397.py [copia na cadeia v399: so' o import do delta mudou; o quadro nao se mexe] -- o lado da CADEIA do quadro", 1),
])

# ------------------------------------------------------------------------------------------- refazer_* (sandbox, arvore pos-selo, candidato) e o build do kernel
entrada("refazer_arvore_v398_pos_selo.py", regras=[
    ("Escrito em 23/10/2026 (NAO executado na preparacao). Molde: refazer_arvore_v398_pos_selo.py.", "Escrito em 24/10/2026 (NAO executado na preparacao). Molde: refazer_arvore_v398_pos_selo.py.", 1),
])
entrada("refazer_sandbox_v398.sh", regras=[
    ("e sem as pedras compiladas em .lake/build, entao o build COMPILA AS PEDRAS A FRIO, como o rito)", "e sem a pedra compilada em .lake/build, entao o build COMPILA A PEDRA A FRIO, como o rito)", 1),
    ("acrescenta as pedras Sonico e AfinacaoDasCordas e GERA a raiz e o Audit", "acrescenta a pedra Testemunho e GERA a raiz e o Audit", 1),
])
entrada("refazer_sandbox_v398_pos_selo.sh")
entrada("refazer_candidato_v398.sh", regras=[
    ("(runtime_pedras_v399.py, registros_v399.py, artigo_*_v399.pysnip, gerar_candidato_v399.py)", "(runtime_v399.py [montado por montar_runtime_v399.py], registros_v399.py, artigo_*_v399.pysnip, gerar_candidato_v399.py)", 1),
    ('PY="python -I -B -X utf8"\n', 'PY="python -I -B -X utf8"\nPYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele\n', 1),
    ('echo "== 1. gerar_candidato_v399.py $(date +%T)"; $PY gerar_candidato_v399.py', 'echo "== 0. montar_runtime_v399.py (o codigo novo do um.py, montado dos insumos aprovados do estudo) $(date +%T)"; $PY montar_runtime_v399.py | tail -3\necho "== 1. gerar_candidato_v399.py $(date +%T)"; $PY gerar_candidato_v399.py', 1),
    ("$PY conferir_rito_v399.py _CONTROLE_NEGATIVO_PRE_RITO", "$PYN conferir_rito_v399.py _CONTROLE_NEGATIVO_PRE_RITO", 1),
    ("$PY teste_conferidor_positivo_v399.py | tail -1", "$PYN teste_conferidor_positivo_v399.py | tail -1", 1),
])
entrada("construir_kernel_v398.sh", regras=[
    (r"(C:\t\k399c\final; nunca o do Nos nem C:\t\k399b): um `lake build` INCREMENTAL (a v398 e as duas pedras novas ja' estao compiladas em .lake/build, cada pedra isolada; muda a raiz TGLExt e o Audit)",
     r"(C:\t\k399c\final; nunca o do Nos nem C:\t\k399): um `lake build` INCREMENTAL (a v398 e a pedra nova, Testemunho, ja' estao compiladas em .lake/build, a pedra isolada; muda a raiz TGLExt e o Audit)", 1),
])

# ------------------------------------------------------------------------------------------- diff_e_pinos / instalar / reverter / regras / teste do conferidor
entrada("diff_e_pinos_v398.py", regras=[
    ("o diff do kernel nao e' so' as duas pedras + raiz + Audit", "o diff do kernel nao e' so' a pedra + raiz + Audit", 1),
    ("os vereditos esperados do passo simples (REPINADA_B8__...)", "os vereditos esperados do passo simples (REPINADA_B9__...)", 1),
])
entrada("instalar_v398.py", regras=[
    ("escrito em 23/10/2026, NAO executado na preparacao). Molde: instalar_v398.py.", "escrito em 24/10/2026, NAO executado na preparacao). Molde: instalar_v398.py.", 1),
    ("(a v399 traz DOIS modulos novos de kernel, o numero lido de kernel_modulos_novos_v399.json: o proprio rito os materializa a partir do corpo embutido)",
     "(a v399 traz UM modulo novo de kernel, Testemunho [nome provisorio]; o numero e' lido de kernel_modulos_novos_v399.json: o proprio rito o materializa a partir do corpo embutido)", 1),
    ("(o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica e Token) JA estao no kernel do Nos (a base instalada e' a v398 selada); (b) os modulos novos da v399 (Sonico e AfinacaoDasCordas) NAO estao la ainda.",
     "(o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica, Token, Sonico e AfinacaoDasCordas) JA estao no kernel do Nos (a base instalada e' a v398 selada); (b) o modulo novo da v399 (Testemunho) NAO esta la ainda.", 1),
    ('"Psibit", "TestemunhaEstatica", "Token")', '"Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas")', 1),
])
entrada("reverter_v398.py", regras=[
    ("escrito em 23/10/2026, NAO executado na preparacao). Le o ULTIMO", "escrito em 24/10/2026, NAO executado na preparacao). Le o ULTIMO", 1),
])
entrada("regras_v398.py", regras=[
    ("ESCRITO em 23/10/2026 pela preparacao da cadeia v399", "ESCRITO em 24/10/2026 pela preparacao da cadeia v399", 1),
    # o conferidor da v399 IMPORTA o um.py instalado (que importa o numpy do usuario): roda SEM -I (o -I esconderia o numpy); a regra de permissao tem de casar o comando exato
    ("python -I -B -X utf8 conferir_rito_v399.py:*", "python -B -X utf8 conferir_rito_v399.py:*", 1),
])
entrada("teste_conferidor_positivo_v398.py", autoral=True)   # escrito a mao na v399: monta o sidecar e o stdout do Nos falso com a funcao do proprio candidato

# ------------------------------------------------------------------------------------------- o kernel (preparar, pos_build): a logica e' a mesma (laco sobre DL.STONES); so' o texto de uma pedra
entrada("preparar_kernel_v398.py", regras=[
    entre('"""preparar_kernel_v399.py', 'import ast, hashlib, json, os, subprocess, sys',
          r'''"""preparar_kernel_v399.py -- monta o SANDBOX do kernel da v399 em C:\\t\\k399c\\final (nunca toca o Nos nem C:\\t\\k399).
Parte de C:\\t\\k399\\final (um projeto lake: o kernel da v398 compilado em .lake/build + a pedra nova, Testemunho, compilada ISOLADA; sem a pasta probe\\ nem os .bak_), e GERA (nao copia) a raiz TGLExt.lean
e o TGL/Audit.lean a partir dos da v398 embutida: raiz = v398 + o import da pedra; Audit = o import no topo + o Audit da v398. A pedra e' a fonte da ORDEM (v399\\pedra\\Testemunho.lean, copia de bytes da de
work\\v399_selo_e_testemunho; o sha16 e' LIDO na hora da geracao e conferido contra o que a ordem da gerencia deu), copiada para o sandbox quando difere. Molde: preparar_kernel_v398.py.
uso: python -I -B -X utf8 preparar_kernel_v399.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = pedra + raiz + Audit; conferir = so' verifica e escreve kernel_modulos_novos_v399.json)"""
''', "docstring (uma pedra)"),
    ('"*.bak_*", "Sonico*.bak_*", "AfinacaoDasCordas*.bak_*", "TGLExt.lean.bak_*",', '"*.bak_*", "Testemunho*.bak_*", "TGLExt.lean.bak_*",', 1),
    ("# le as duas pedras do disco e confere o sha16 da ordem", "# le a pedra do disco e confere o sha16 da ordem", 1),
    ("# a raiz e o Audit de partida do sandbox (copia de k399b)", "# a raiz e o Audit de partida do sandbox (copia de k399/final)", 1),
])
entrada("pos_build_kernel_v398.py", regras=[
    ("linha Built/Replayed das DUAS pedras (Sonico, AfinacaoDasCordas), da raiz", "linha Built/Replayed da pedra (Testemunho), da raiz", 1),
    ("uma serie de chaves por pedra: ext_son398_NNNN e ext_afi398_NNNN)", "uma serie de chaves por pedra: ext_tmn399_NNNN)", 1),
    ("as unicas pedras do recibo sao Sonico e AfinacaoDasCordas, nao a LightNetStandardWedgeDataBGL", "a unica pedra do recibo e' a Testemunho, nao a LightNetStandardWedgeDataBGL", 1),
    ("tem de ser so' as duas pedras, na ordem do delta", "tem de ser so' a pedra Testemunho, na ordem do delta", 1),
    ("linha Built/Replayed dos modulos novos (Sonico, AfinacaoDasCordas), da raiz", "linha Built/Replayed do modulo novo (Testemunho), da raiz", 1),
    ("(Replayed = a pedra ja' estava compilada em .lake/build do k399b;", "(Replayed = a pedra ja' estava compilada em .lake/build do k399/final;", 1),
    ("(as pedras podem ja' estar compiladas em C:/t/k399b, cada uma isolada;", "(a pedra pode ja' estar compilada em C:/t/k399/final, isolada;", 1),
    ("x19='nao': o recibo v399 lista so' as pedras NOVAS Sonico e AfinacaoDasCordas e a LightNetStandardWedgeDataBGL.lean", "x19='nao': o recibo v399 lista so' a pedra NOVA Testemunho e a LightNetStandardWedgeDataBGL.lean", 1),
    ("gerado por pos_build_kernel_v399.py (preparacao, 23/10/2026);", "gerado por pos_build_kernel_v399.py (preparacao, 24/10/2026);", 1),
    ("(decisao da gerencia c1, 23/10/2026; a regra e' a da v394 a v398,", "(decisao da gerencia c1, mantida na ordem da v399 de 24/10/2026: bandeiras so' nomeadas; a regra e' a da v394 a v398,", 1),
])
