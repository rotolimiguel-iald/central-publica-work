# -*- coding: utf-8 -*-
# regras (lote E2) de derivar_encanamento_v403.py: refazer (candidato, sandbox, arvore), regras de permissao (NAO executadas), regerar e o pino do memoria.py. ORIGEM v402. Escrito pela ferramenta Write; contagem exata; nada e' executado.

entrada("refazer_candidato_v402.sh", autoral=True, regras=[])
entrada("refazer_sandbox_v402_pos_selo.sh", autoral=True, regras=[])
entrada("refazer_arvore_v402_pos_selo.py", autoral=True, regras=[])

# regras_v403.py MUDA ~/.claude/settings.json: e' CLONE do molde, com a trava V403_REGRAS_AUTORIZADAS; esta preparacao NAO o executa (ordem da gerencia: nao rodar regras de permissao)
entrada("regras_v402.py", autoral=True, regras=[
    ("ESCRITO em 26/10/2026 pela preparacao da cadeia v403", "ESCRITO em 27/10/2026 pela preparacao da cadeia v403", 1),
])

entrada("regerar_v402.sh", autoral=True, regras=[
    ("refaz, NA ORDEM, tudo o que depende das TRES PEDRAS (Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_025\\PonteDaEscalaDual.lean, work\\pedras_v403\\QuedaSemGeometria.lean e EsperancaCondicional.lean)",
     "refaz, NA ORDEM, tudo o que depende das TRES PEDRAS (work\\cadeia_de_selo\\v403_kernel\\pedras\\Caminho.lean, Vida.lean e VerdadeAdendo.lean)", 1),
])

entrada("pino_memoria_py_v402.py", autoral=True, regras=[])
