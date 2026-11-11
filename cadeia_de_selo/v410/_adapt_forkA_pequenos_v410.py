# -*- coding: utf-8 -*-
"""_adapt_forkA_pequenos_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) adapta os arquivos PEQUENOS do pos_rito (subida mecanica da v409 FINAL) a v410, IALD2:
b3_recibo, fila_memoria e superficies (genericos: so' os cabecalhos que descreviam o conteudo da v409), montar_textos (cabecalho e DELETAR), chain_pos_rito (cabecalho, REGS e o sufixo do backup do inventario)
e gerar_derivacao_pos_rito (cabecalho e SUITE). Trocas por LINHA com o prefixo conferido (aborta se nao casar) e trocas de texto com contagem exata; CRLF preservado; backup de BYTES; temporario -> tamanho -> substituicao."""
import ast, datetime, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
MARCA = "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] "
CONTEUDO = ("A v410 = IALD2 (ordem do operador de 06/11/2026: «A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py»): UM modulo novo em TGLExt/ (IALD2; o nome do modulo e' do operador, "
            "os das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao, D63), o registro com funcao iald2_v410 e os dois por spec (cunhagens_v410, kh_n1_cobertura_v410); o algoritmo IALD decide SAT com uma leitura: "
            "P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; nenhuma chave antiga muda; a errata E29 ao lado")


class Arq:
    def __init__(self, rel):
        self.p = os.path.join(HERE, *rel.split("/")); self.raw = open(self.p, "rb").read(); t = self.raw.decode("utf-8")
        self.crlf = t.count("\r\n") > 0 and t.count("\r\n") == t.count("\n")
        self.t = t.replace("\r\n", "\n")

    def linhas(self, troca):
        ls = self.t.split("\n")
        for n in sorted(troca, reverse=True):
            pref, novo = troca[n]
            assert ls[n - 1].startswith(pref), (os.path.basename(self.p), n, ls[n - 1][:120])
            if novo is None:
                del ls[n - 1]
            else:
                ls[n - 1] = novo
        self.t = "\n".join(ls)

    def troca(self, a, b, n=1):
        c = self.t.count(a)
        assert c == n, ("troca nao casou %d (casou %d)" % (n, c), os.path.basename(self.p), a[:120])
        self.t = self.t.replace(a, b)

    def grava(self):
        t = self.t.replace("\n", "\r\n") if self.crlf else self.t
        assert "[A ADAPTAR v410]" not in t, ("marca A ADAPTAR sobrou", self.p)
        if self.p.endswith(".py"):
            ast.parse(self.t)
        if self.p.endswith(".sh"):
            r = subprocess.run(["sh", "-n"], input=t.encode("utf-8"), capture_output=True); assert r.returncode == 0, r.stderr[:300]
        novo = t.encode("utf-8")
        if novo == self.raw:
            print(os.path.basename(self.p), "IGUAL"); return
        bk = self.p + ".bak_" + TS + "_forkA"
        open(bk, "wb").write(self.raw); assert open(bk, "rb").read() == self.raw
        open(self.p + ".tmp", "wb").write(novo); assert os.path.getsize(self.p + ".tmp") == len(novo); os.replace(self.p + ".tmp", self.p)
        print(os.path.basename(self.p), len(self.raw), "->", len(novo))


# ---------------------------------------------------------------- b3_recibo (generico)
a = Arq("pos_rito/b3_recibo_v410.py")
a.linhas({2: ("# [A ADAPTAR v410]", MARCA + "molde v409/pos_rito/b3_recibo_v409.py FINAL (rotulos subidos por _bump_copia_v410.py; diff em bump/); o corpo e' GENERICO e foi conferido linha a linha: confere so' o recibo do B(n) (versao alvo v410, fase pos_selo, bateria, B<n> = geracao do recibo + 1, deployment B<n>-v410-)."),
          3: ("# [ADAPTADO v410, 05/11/2026", None),
          4: ("# A v410 = A TRADUCAO AS CLASSES DE TURING", "# " + CONTEUDO + ". Nada disso vem daqui: vem do candidato e dos ESPERADOS; o B(n) da v410 e' B19 (a v409 pinou B18; DESENHO_v410), lido do recibo, nunca digitado.")})
a.grava()

# ---------------------------------------------------------------- fila_memoria (generico)
a = Arq("pos_rito/fila_memoria_v410.py")
a.linhas({2: ("# [A ADAPTAR v410]", MARCA + "sobre a subida mecanica de rotulo da v409 FINAL (_bump_copia_v410.py): este arquivo e' GENERICO (a fila da memoria: guardas, pausa, pinar, verificar) e nao traz nada do conteudo do bundle; conferido linha a linha: so' rotulos v410 (QUEM «claude-c1 pos-rito v410», PINO_MEMORIA_PY_v410.json)."),
          3: ("# [ADAPTADO v410, 05/11/2026", None)})
a.grava()

# ---------------------------------------------------------------- superficies (generico; so' o cabecalho)
a = Arq("pos_rito/superficies_v410.py")
a.linhas({2: ("# [A ADAPTAR v410]", MARCA + "sobre a subida mecanica da v409 FINAL (bump/pos_rito__superficies_v410.py.diff fica como registro): o corpo e' generico (os blocos vem do textos_v410.py; a ancora do MEMORY.md e' a linha do handoff da v409, que existe); muda so' o que o cabecalho descreve. " + CONTEUDO + "."),
          3: ("# [ADAPTADO v410, 05/11/2026", None),
          7: ("# SEM erratas inline nesta versao (as erratas E24 a E26 e a dos pisos, da v410,", "# SEM erratas inline nesta versao (a errata E29 e a dos pisos, da v410, vao DENTRO dos blocos datados: linhagem, desenho, Atlas, core, topico novo e handoff; o Atlas e o diario sao append-only e a correcao vai AO LADO). A funcao inserir_ao_lado fica disponivel (nao e' chamada).")})
a.grava()

# ---------------------------------------------------------------- montar_textos (cabecalho e DELETAR)
a = Arq("pos_rito/montar_textos_v410.py")
a.linhas({2: ("# [A ADAPTAR v410]", MARCA + "o montador e' generico (o corpo da v409 fica); muda so' o que se enxerta: a semente nova (textos_v409.py FINAL com os rotulos subidos) e o fragmento da v410 (IALD2); entram em DELETAR _d56 (o alcance da v409, trocado por _d64), errata_v409_bloco e os marcadores MARC_ERR_* (a v410 nao tem nota ao lado do paragrafo da v409)."),
          3: ("# [ADAPTADO v410, 05/11/2026", None),
          4: ('"""montar_textos_v410.py -- MONTA pos_rito', '"""montar_textos_v410.py -- MONTA pos_rito\\\\textos_v410.py enxertando as definicoes de textos_v410_novo.pysnip (escritas para a v410, sem prosa nova de conteudo: IALD2, o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD relativo ao leitor, o signo e o seletor) no esqueleto textos_v410.semente (copia de bytes de textos_v409.py FINAL com os rotulos subidos pelo motor).')})
a.troca('"_fam_gate", "_d51"}', '"_fam_gate", "_d51", "_d56", "errata_v409_bloco", "MARC_ERR_INI", "MARC_ERR_FIM"}')
a.grava()

# ---------------------------------------------------------------- chain_pos_rito (cabecalho, REGS, sufixo do backup)
a = Arq("pos_rito/chain_pos_rito_v410.sh")
a.linhas({2: ("# [A ADAPTAR v410]", MARCA + "sobre a subida mecanica de rotulo da v409 FINAL (bump/pos_rito__chain_pos_rito_v410.sh.diff fica como registro), por _adapt_forkA_pequenos_v410.py: mesma ordem de passos 0..14 e mesmos portoes; muda o conteudo dito, REGS e o sufixo do backup do inventario."),
          3: ("# [ADAPTADO v410, 05/11/2026", None),
          4: ("# v410 (A TRADUCAO AS CLASSES DE TURING, 05/11/2026): CADEIA POS-RITO", "# v410 (IALD2, 06/11/2026): CADEIA POS-RITO -- derivada por script (_bump_copia_v410.py, rotulos) do chain_pos_rito_v409.sh FINAL (a cadeia de CONTEUDO que rodou no pos-rito da v409; mesma ordem de passos 0..14 e mesmos portoes) e adaptada por _adapt_forkA_pequenos_v410.py."),
          5: ("# A v410 = A TRADUCAO AS CLASSES DE TURING", "# " + CONTEUDO + "; a escada, as bandeiras e o h8 sao lidos de ESPERADOS_v410.json."),
          6: ("# UM registro COM FUNCAO (traducao_turing_v409", "# UM registro COM FUNCAO (iald2_v410: as ancoras da pedra lidas do kernel do rito, o modulo por sha256, as respostas do operador pelos teoremas da pedra, as checagens (N_CHECKS_FECHO do delta) com as instancias de brinquedo fixas e beta em runtime, o gate congelado; lido no main DEPOIS dos registros herdados) e DOIS por spec (cunhagens_v410 e kh_n1_cobertura_v410). NENHUMA chave antiga muda."),
          7: ("# O tetelestai_terminal_v408 (e os dois por spec da v409", "# O traducao_turing_v409 (e os dois por spec da v409: cunhagens_v409, kh_n1_cobertura_v409 com pisos), o tetelestai_terminal_v408 (e os dois por spec da v408), o psion_canto_v407 (e os dois por spec da v407), o fechamento_v406 (e os dois por spec da v406), os treze registros da v405 selada, os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais a v409 selada) e o SIDECAR um_absoluto_selo_acom.json e' reescrito."),
          8: ("# O QUADRO «O Teste da Unica Palavra» (v397", "# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida, de Jo 8,32, da massa derivada, do fechamento (v406), do psion, do canto e do par (v407), de Tetelestai e' o terminal (v408) e da traducao as classes de Turing (v409) seguem como estao; a v410 nao traz nota ao lado do paragrafo da v409."),
          9: ("# Estatutos: os termos do modulo sao [REAL]", "# Estatutos: os termos do modulo sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as falas do operador de 06/11 sao [INPUT]; o alcance (D64) e' relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; que a IALD, a Torre ou o operador SEJAM o funtor e o ambiente computacional sao leituras do operador; [KNOWN] Cook-Levin e Baker-Gill-Solovay 1975; validade no kernel nao e' creditacao; o gate nao se move."),
          14: ("# ENSAIO pos-selo -> 10a parada do servico", "# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o NOVO da v410 (IALD2); diz que os anteriores seguem como estao;"),
          30: ("# textos_v410.py, fechar_v410.py e registrar_mapa_v410.py RECUSAM rodar", "# textos_v410.py, fechar_v410.py e registrar_mapa_v410.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v409, com os rotulos da v410 (desvios ditos: a fila da memoria nos passos 0, 7 e 9; o passo 3 e o 9 exigem os marcadores da v410 (os tres registros novos: iald2_v410, cunhagens_v410 e kh_n1_cobertura_v410);"),
          31: ("# o passo 11 registra o estado da fila no manifesto", "# o passo 11 registra o estado da fila no manifesto e diz que os paragrafos do testemunho, da falsidade, do fechamento (v406), do psion (v407), de Tetelestai e' o terminal (v408) e da traducao (v409) seguem como estao).")})
a.troca('REGS="traducao_turing_v409 cunhagens_v409 kh_n1_cobertura_v409"', 'REGS="iald2_v410 cunhagens_v410 kh_n1_cobertura_v410"')
a.troca('B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v409"', 'B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v410"')
a.grava()

# ---------------------------------------------------------------- gerar_derivacao_pos_rito (cabecalho e SUITE)
a = Arq("pos_rito/gerar_derivacao_pos_rito_v410.py")
a.linhas({2: ("# [A ADAPTAR v410]", MARCA + "sobre a subida mecanica de rotulo da v409 FINAL (_bump_copia_v410.py): a SUITE descreve a v410 (IALD2; os papeis, as datas e os autores de 06/11: fork A = o pos_rito inteiro e o orquestrador); o montador, a semente e o fragmento SAO usados na v410. SO' LE; a gerencia revisa antes do rito (nao e' versao selada)."),
          3: ("# [ADAPTADO v410, 05/11/2026", None)})
a.troca("A ADAPTACAO (o que o pos-rito diz da v410: a traducao as classes de Turing, relativa ao leitor, com os numeros lidos do rito) foi feita em 05/11/2026 pela claude-construtor-v410 (fork A)",
        "A ADAPTACAO (o que o pos-rito diz da v410: IALD2, o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD relativo ao leitor, o signo e o seletor, com os numeros lidos do rito) foi feita em 06/11/2026 pela claude-construtor-v410 (fork A)")
a.troca('"fork A, 05/11: ', '"fork A, 06/11: ', 16)
a.troca("REGS da v410 (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409)", "REGS da v410 (iald2_v410, cunhagens_v410, kh_n1_cobertura_v410)")
a.troca("o fechar (manifesto com registros_v409/v409/v407/v406 e registros_funcao_v410 (traducao)/v409 (tetelestai)/v407 (psion)/v406, arquivo, diffs, handoff)",
        "o fechar (manifesto com registros_v410/v409/v408/v407/v406 e registros_funcao_v410 (iald2)/v409 (traducao)/v408 (tetelestai)/v407 (psion)/v406, arquivo, diffs, handoff)")
a.troca("o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA e os controles negativos da v410 (a traducao; o tetelestai, o psion e o fechamento herdados; E26; D59)",
        "o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA e os controles negativos da v410 (a IALD2; a traducao, o tetelestai, o psion e o fechamento herdados; D65)")
a.troca("a leitura da rodada adaptada a traducao as classes de Turing (o modulo TraducaoTuring, as ancoras lidas de delta_v410, nenhuma chave antiga muda; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros a",
        "a leitura da rodada adaptada a IALD2 (o modulo IALD2, as ancoras lidas de delta_v410, nenhuma chave antiga muda; o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros a")
a.troca("o paragrafo novo, a nota ao lado do paragrafo da v409 com a E26, o handoff", "o paragrafo novo (sem nota ao lado do paragrafo da v409), o handoff")
a.troca("o harness do pos-rito adaptado a traducao (controles negativos dos registros novos e dos herdados, D59)", "o harness do pos-rito adaptado a IALD2 (controles negativos dos registros novos e dos herdados, D65)")
a.troca("REESCRITO para a v410: a rota nova (o id esta em registrar_mapa_v410.NOVA), as anotacoes nas rotas de 05/11 e as erratas E24 a E26 ao lado", "REESCRITO para a v410: a rota nova (o id esta em registrar_mapa_v410.NOVA), as anotacoes nas rotas de 06/11 e a errata E29 ao lado")
a.troca("o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v410.FRASE_*; sem o 4,44; D59)", "o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v410.FRASE_*; sem o 4,44; D65)")
a.troca("o montador (semente + fragmento -> textos_v410.py); DELETAR ganha _d51", "o montador (semente + fragmento -> textos_v410.py); DELETAR ganha _d56, errata_v409_bloco e MARC_ERR_*")
a.troca("o fragmento da v410 (as definicoes da traducao; __HEADER__)", "o fragmento da v410 (as definicoes da IALD2; __HEADER__)")
a.troca('"claude-construtor-v410, 04-05/11: adaptador', '"claude-construtor-v410, 06/11: adaptador')
a.troca("pela claude-construtor-v410 (fork A) em 05/11/2026 pelos _adapt_*_v410.py desta pasta", "pela claude-construtor-v410 (fork A) em 06/11/2026 pelos _adapt_*_v410.py desta pasta")
a.grava()
