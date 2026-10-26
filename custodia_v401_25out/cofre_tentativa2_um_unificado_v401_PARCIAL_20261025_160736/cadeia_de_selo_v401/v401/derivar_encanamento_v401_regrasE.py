# -*- coding: utf-8 -*-
# regras (lote E) de derivar_encanamento_v401.py: o CONFERIDOR do rito e o teste do caminho positivo. ORIGEM v399 (a cadeia de CONTEUDO: um modulo novo; mapa 398 -> 400, 399 -> 401) + as LICOES da v400, escolhidas hunk a hunk por aplica_hunks
# (as da correcao do alfa/beta: C3, C9, C13, C15 e C16; NAO as que a v400 fez por nao ter modulo). Escrito pela ferramenta Write.
from derivar_v401_motor import aplica_hunks  # noqa: E402

entrada("conferir_rito_v399.py", origem="v399", autoral=True, regras=[
    aplica_hunks("conferir_rito_v400.py", [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
])
entrada("teste_conferidor_positivo_v399.py", origem="v399", autoral=True)

# ------------------------------------------------------------------------------------------- instalar / reverter / rito (origem v399, a cadeia de CONTEUDO) + as licoes da v400 (o sidecar entra nos backups e na reversao; a pedra Testemunho ja' esta no kernel do Nos)
entrada("instalar_v399.py", origem="v399", autoral=True, regras=[aplica_hunks("instalar_v400.py", [4, 5])])
entrada("reverter_v399.py", origem="v399", autoral=True, regras=[aplica_hunks("reverter_v400.py", [0, 1])])
entrada("rito_v399.sh", origem="v399", autoral=True)

# ------------------------------------------------------------------------------------------- o diff do kernel e os pinos do B(n) (origem v399: o passo simples com UM modulo novo, a Bancada ja' pinando a versao anterior)
entrada("diff_e_pinos_v399.py", origem="v399", autoral=True)

# ------------------------------------------------------------------------------------------- as precondicoes (p00): origem v399 + a licao da v400 (as guardas estaticas da Bancada); o resto do p00 e' ajustado por patch_p00_v401.py
entrada("p00_precondicoes_v399.py", origem="v399", autoral=True, regras=[aplica_hunks("p00_precondicoes_v400.py", [1, 3])])

# ------------------------------------------------------------------------------------------- refazer (candidato, sandbox e arvore pos-selo), regras de permissao (escrito, NAO rodado)
entrada("refazer_candidato_v399.sh", origem="v399", autoral=True)
entrada("refazer_sandbox_v399_pos_selo.sh", origem="v399")
entrada("refazer_arvore_v399_pos_selo.py", origem="v399")
entrada("regras_v399.py", origem="v399")
