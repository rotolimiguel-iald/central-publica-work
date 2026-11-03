# -*- coding: utf-8 -*-
# regras (lote F) de derivar_encanamento_v406.py: o POS-RITO. ORIGEM v405 FINAL (a que rodou em 28/10). Mapa: 403 -> 405, 405 -> 406.
# ESTADO: a SUBIDA MECANICA das versoes + as correcoes de enumeracao que a subida perde (o rotulo v403 sai das listas de pastas irmas: aqui volta). O CONTEUDO da v406 (leitura, textos, harnesses, registro no mapa) e' adaptado por pos_rito\adaptar_pos_rito_v406.py (regras de contagem exata sobre a semente que este lote grava) e por textos_v406_novo.pysnip (escrito a mao). Nada daqui roda antes do rito. Escrito pela ferramenta Write.
_NOTA_POS_RITO = ("# [PREPARACAO v406, 02/11/2026 -- ESTADO] SUBIDA MECANICA da v405 FINAL (derivar_encanamento_v406.py, lote F); AINDA NAO adaptada ao conteudo da v406 nem exercitada por harness: a gerencia adapta e ensaia.\n"
                  "# NAO e' versao selada: a gerencia revisa antes do rito. Ver DERIVACAO_v406_NOTAS.md.\n")


def _tira_nota_antiga(t_):
    """o cabecalho [PREPARACAO v406, 01/11/2026 -- ESTADO] herdado da subida: sai, para a nota nova entrar."""
    import re as _re
    return _re.sub(r"# \[PREPARACAO v406, 01/11/2026 -- ESTADO\][^\n]*\n(# NAO e' versao selada[^\n]*\n)?", "", t_, count=1)


def _nota_py(t_):
    t_ = _tira_nota_antiga(t_)
    assert t_.startswith("# -*- coding: utf-8 -*-\n")
    return t_.replace("# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n" + _NOTA_POS_RITO, 1)


def _nota_sh(t_):
    t_ = _tira_nota_antiga(t_)
    assert t_.startswith("#!/bin/sh\n")
    return t_.replace("#!/bin/sh\n", "#!/bin/sh\n" + _NOTA_POS_RITO, 1)


_NOTA = (_nota_py, "nota do estado da preparacao no topo do arquivo", 1)
entrada("pos_rito/b3_recibo_v405.py", autoral=True, regras=[
    _NOTA,
    ("pina a v405, B12, deployment B12-v405-20261028-R1, e o Nos passou a v406; o rito grava a geracao B13 --", "pina a v405, B13, deployment B13-v405-20261028-R1, e o Nos passou a v406; o rito grava a geracao B14 --", 1),
])
entrada("pos_rito/superficies_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/fila_memoria_v405.py", autoral=True, regras=[])
entrada("pos_rito/montar_textos_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/fechar_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/textos_v405.py", dst="pos_rito/textos_v406.semente", autoral=True, regras=[])
entrada("pos_rito/registrar_mapa_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/leitura_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/harness_textos_ensaio_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/harness_fechar_sandbox_v405.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/gerar_x_custodia_v405.py", autoral=True, regras=[])
entrada("pos_rito/chain_pos_rito_v405.sh", autoral=True, regras=[(_nota_sh, "nota do estado da preparacao no topo do arquivo", 1)])
entrada("pos_rito/gerar_derivacao_pos_rito_v405.py", autoral=True, regras=[_NOTA])
