# -*- coding: utf-8 -*-
# regras (lote F) de derivar_encanamento_v405.py: o POS-RITO. ORIGEM v404 FINAL (a que rodou em 28/10). Mapa: 403 -> 404, 404 -> 405.
# ESTADO: a SUBIDA MECANICA das versoes + as correcoes de enumeracao que a subida perde (o rotulo v403 sai das listas de pastas irmas: aqui volta). O CONTEUDO da v405 (leitura, textos, harnesses, registro no mapa) e' adaptado por pos_rito\adaptar_pos_rito_v405.py (regras de contagem exata sobre a semente que este lote grava) e por textos_v405_novo.pysnip (escrito a mao). Nada daqui roda antes do rito. Escrito pela ferramenta Write.
_NOTA_POS_RITO = ("# [PREPARACAO v405, 01/11/2026 -- ESTADO] derivado da v404 FINAL (derivar_encanamento_v405.py, lote F) e adaptado por adaptar_pos_rito_v405.py e textos_v405_novo.pysnip ao conteudo da v405; exercitado pelo harness_textos_ensaio_v405.py e pelo harness_fechar_sandbox_v405.py.\n"
                  "# NAO e' versao selada: a gerencia revisa antes do rito. Ver RELATORIO_PREPARACAO_v405.md.\n")


def _tira_nota_antiga(t_):
    """o cabecalho [PREPARACAO v405, 28/10/2026 -- ESTADO] herdado da subida: sai, para a nota nova entrar."""
    import re as _re
    return _re.sub(r"# \[PREPARACAO v405, 28/10/2026 -- ESTADO\][^\n]*\n(# NAO e' versao selada[^\n]*\n)?", "", t_, count=1)


def _nota_py(t_):
    t_ = _tira_nota_antiga(t_)
    assert t_.startswith("# -*- coding: utf-8 -*-\n")
    return t_.replace("# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n" + _NOTA_POS_RITO, 1)


def _nota_sh(t_):
    t_ = _tira_nota_antiga(t_)
    assert t_.startswith("#!/bin/sh\n")
    return t_.replace("#!/bin/sh\n", "#!/bin/sh\n" + _NOTA_POS_RITO, 1)


_NOTA = (_nota_py, "nota do estado da preparacao no topo do arquivo", 1)
entrada("pos_rito/b3_recibo_v404.py", autoral=True, regras=[
    _NOTA,
    ("pina a v404, B12, deployment B12-v404-20261028-R1, e o Nos passou a v405; o rito grava a geracao B13 --", "pina a v404, B13, deployment B13-v404-20261028-R1, e o Nos passou a v405; o rito grava a geracao B14 --", 1),
])
entrada("pos_rito/superficies_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/fila_memoria_v404.py", autoral=True, regras=[])
entrada("pos_rito/montar_textos_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/fechar_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/textos_v404.py", dst="pos_rito/textos_v405.semente", autoral=True, regras=[])
entrada("pos_rito/registrar_mapa_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/leitura_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/harness_textos_ensaio_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/harness_fechar_sandbox_v404.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/gerar_x_custodia_v404.py", autoral=True, regras=[])
entrada("pos_rito/chain_pos_rito_v404.sh", autoral=True, regras=[(_nota_sh, "nota do estado da preparacao no topo do arquivo", 1)])
entrada("pos_rito/gerar_derivacao_pos_rito_v404.py", autoral=True, regras=[_NOTA])
