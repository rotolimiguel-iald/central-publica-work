# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v401.py: o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco) e a licao da v400 (guardas estaticas da Bancada). ORIGEM v400 (mapa 399 -> 400, 400 -> 401).
# A base mecanica sobe do v400; a logica NOVA da v401 (o registro falsidade_da_inercia_v401, os registros por spec v401, a pedra) entra como regras de contagem exata. Escrito pela ferramenta Write.

# ------------------------------------------------------------------------------------------- simular a arvore do Nos: mais o registro da falsidade (chamado no main logo depois da declaracao do operador) e os specs da v401
entrada("simular_arvore_do_nos_v400.py", autoral=True, regras=[
    ("um.selo_acom_v399(core); um.declaracao_do_operador_v399(core)   # (na fractalizacao", "um.selo_acom_v399(core); um.declaracao_do_operador_v399(core); um.falsidade_da_inercia_v401(core)   # (na fractalizacao", 1),
    ("um._v398_rodar_specs(core); um._v399_rodar_specs(core)   # (v397:", "um._v398_rodar_specs(core); um._v399_rodar_specs(core); um._v401_rodar_specs(core)   # (v397:", 1),
    ('for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399",', 'for k in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399",', 1),
])

# ------------------------------------------------------------------------------------------- exame dos pontos de chamada, ensaio a seco e as guardas estaticas: a base mecanica (as adicoes da v401 sao regras do lote D)
entrada("ensaio_a_seco_v400.py", autoral=True)
# as guardas estaticas: a LICAO da v400 mantida (o candidato passa a mesma leitura que o B(n) fara; o defeito real da v399 selada segue reproduzido como controle; mutantes recusados). Rotulos: o candidato e' v401 (o m6 usa v402 como alvo errado); a v399 selada
# vem da copia de bytes que a cadeia v400 guardou (v400\base_v399); o sandbox curto e' C:\t\vb18. com_bump=False: o mapa mecanico confundiria o v399 do DEFEITO (que fica) com o rotulo da cadeia.
entrada("guardas_estaticas_bancada_v400.py", autoral=True, com_bump=False, dst="guardas_estaticas_bancada_v401.py", regras=[
    sub_n(r'"v401"', '"v402"', 2, "alvo errado do mutante m6"),
    sub_n(r'v400', 'v401', 27, "rotulos do candidato e nomes da cadeia"),
    ("vb17", "vb18", 1),
    ('base_um = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read()', 'base_um = open(os.path.join(DL.V400, "base_v399", "um.py"), "rb").read()   # a v399 SELADA (o defeito real): copia de bytes guardada pela cadeia v400', 1),
    ("LICAO NOVA da v401 (a v399 passou", "LICAO da v400, MANTIDA na v401 (a v399 passou", 1),
])
