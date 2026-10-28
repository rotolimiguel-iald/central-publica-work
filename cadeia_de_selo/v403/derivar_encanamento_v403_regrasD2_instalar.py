# -*- coding: utf-8 -*-
# regras (lote D2) de derivar_encanamento_v403.py: instalar, reverter, rito e a conferencia deles (as TRES pedras: N = 3). ORIGEM v402. Escrito pela ferramenta Write; cada regra tem contagem exata; nada e' executado.
# O que a v403 muda aqui: (a) a base instalada e' a v402 SELADA, cujo kernel JA traz PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional (entram em _PEDRAS_ANTERIORES); os modulos NOVOS sao Caminho, Vida e VerdadeAdendo (lidos de kernel_modulos_novos_v403.json);
# (b) o tempo esperado do rito sai das marcas da construcao de 27/10/2026 (kernel/construir_marcas.txt), lidas na derivacao; (c) o Audit nao muda, mas o instalador segue guardando os 9 backups (o reverter restaura os 9).

_re_d2 = __import__("re")

_HDR_RITO = r'''# O RITO v403 (ato da gerencia c1, preparado em 27/10/2026): roda o um.py v403 instalado no Nos -- 3 modulos novos de kernel (TGLExt/Caminho, TGLExt/Vida e TGLExt/VerdadeAdendo: os nomes do operador, 27/10/2026; o numero e' lido de kernel_modulos_novos_v403.json) materializados a partir do corpo embutido, kernel e Audit
# construidos pelo proprio um.py, os QUATRO registros com FUNCAO caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 (chamados no main logo depois da esperanca condicional da v402; o ultimo e' a F8.1: as tres bandeiras literais do gate passam a calculadas e a letra do veredito nao muda), os registros por spec novos do core v403 (cunhagens_v403, com as duas falas de 27/10,
# as decisoes D17 a D22, os tres nomes e as erratas E5 e E6; kh_n1_cobertura_v403) e os registros da v399, da v401 e da v402 RECRIADOS (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399, kh_n1_cobertura_v399, falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401, ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402), o SIDECAR um_absoluto_selo_acom.json (depois da ultima escrita do selo). O QUADRO do Teste da Unica Palavra segue no topo.
# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v402); TGL_RITE_CHECKPOINT DESLIGADO. Molde: o rito da v402 (herdeiro do rito_v399.sh com as afericoes dele, a cadeia de CONTEUDO que rodou em 24/10), trocados os nomes, o pacote (a propria pasta da cadeia v403) e a
# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v403_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA.
'''


def _tempo_rito(t):
    """regra por FUNCAO (lote D2): o paragrafo «TEMPO ESPERADO» e' recomposto com os numeros LIDOS de kernel/construir_marcas.txt (build e Audit do sandbox k403c); nada digitado."""
    ini = "# TEMPO ESPERADO (v403, parametro lido de kernel/construir_marcas.txt)"
    assert t.count(ini) == 1, ("ancora do paragrafo de tempo nao unica", t.count(ini))
    i = t.index(ini); j = t.index("\n", i)
    mm = {k_: int(v_) for k_, v_ in _re_d2.findall(r"^(epoch_\w+)=(\d+)$", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), _re_d2.M)}
    b_ = mm["epoch_build_fim"] - mm["epoch_inicio"]; a_ = mm["epoch_audit_fim"] - mm["epoch_build_fim"]; p_ = b_ + a_
    novo = ("# TEMPO ESPERADO (v403, parametro lido de kernel/construir_marcas.txt): no sandbox k403c, 1 lake build INCREMENTAL (a v402 selada, com as tres pedras da v402, ja' esta compilada em .lake/build; as tres pedras novas, Caminho, Vida e VerdadeAdendo, compilam agora; muda a raiz TGLExt; o Audit nao muda) = %d s e 1 Audit = %d s (%d s por passagem); "
            "o rito faz 3 passagens de build + Audit (ordem de grandeza %.2f min so' de lake, fora o resto do um.py; no Nos o primeiro build compila as tres pedras a frio [dado herdado da v402: a ponte do Codex mediu 399,65 s sozinha na maquina dela e 158 s na do revisor]). "
            "O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato." % (b_, a_, p_, 3 * p_ / 60.0))
    return t[:i] + novo + t[j:]


entrada("instalar_v402.py", autoral=True, regras=[
    ("escrito em 26/10/2026, NAO executado na preparacao). Molde: instalar_v402.py.", "escrito em 27/10/2026, NAO executado na preparacao). Molde: instalar_v402.py.", 1),
    ("(a v403 traz TRES modulos novos de kernel, PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional [nomes provisorios; o primeiro e' o do Codex, ORDEM 025]; o numero e' lido",
     "(a v403 traz TRES modulos novos de kernel, Caminho, Vida e VerdadeAdendo [os nomes do operador, 27/10/2026]; o numero e' lido", 1),
    ("TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas e FalsidadeDaInercia) JA estao no kernel do Nos (a base instalada e' a v402 selada); (b) os tres modulos novos da v403 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) NAO estao la ainda.",
     "TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas, FalsidadeDaInercia, PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional) JA estao no kernel do Nos (a base instalada e' a v402 selada); (b) os tres modulos novos da v403 (Caminho, Vida, VerdadeAdendo) NAO estao la ainda.", 1),
    ('"Testemunho", "FalsidadeDaInercia")', '"Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")', 1),
])

entrada("reverter_v402.py", autoral=True, regras=[
    ("escrito em 26/10/2026, NAO executado na preparacao).", "escrito em 27/10/2026, NAO executado na preparacao).", 1),
])

entrada("rito_v402.sh", autoral=True, regras=[
    entre("# O RITO v403 (ato da gerencia c1, preparado em 26/10/2026)", "# O SERVIDOR DO MODELO NATIVO", _HDR_RITO, "cabecalho do rito"),
    (_tempo_rito, "paragrafo de tempo esperado (lido das marcas)", 1),
])

entrada("conferir_instalar_rito_v402.py", autoral=True, regras=[
    ('"base_v402_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", \'"version") == "v402"\']',
     '"base_v402_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho, Vida e VerdadeAdendo", \'"version") == "v402"\']', 1),
    ('"Testemunho [nome provisorio]"])', '"Testemunho [nome provisorio]", "[nomes provisorios; o primeiro e\' o do Codex, ORDEM 025]"])', 1),
    ('/c/IALD/Central de Patentes/work/cadeia_de_selo/v403", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional"],', '/c/IALD/Central de Patentes/work/cadeia_de_selo/v403", "TGLExt/Caminho", "TGLExt/Vida", "TGLExt/VerdadeAdendo"],', 1),
    ('"TGLExt/Testemunho, nome PROVISORIO"])', '"TGLExt/Testemunho, nome PROVISORIO", "do Codex, ORDEM 025"])', 1),
])
