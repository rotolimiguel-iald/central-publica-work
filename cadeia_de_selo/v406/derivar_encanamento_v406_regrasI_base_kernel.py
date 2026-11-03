# -*- coding: utf-8 -*-
# regras (lote I) de derivar_encanamento_v406.py: a BASE e o SANDBOX do kernel (copiar_base, preparar_kernel). ORIGEM v405. Mapa: 404 -> 405 (a base selada), 405 -> 406 (esta rodada).
# Lote NOVO da v406 (nao vem dos lotes da v405: la' estes dois scripts eram escritos a mao). Escrito pela ferramenta Write. Contagem exata; nada e' executado.
# copiar_k406c.sh e delta_v406.py (esqueleto de encanamento) sao ESCRITOS A MAO (a origem do sandbox e' o Nos v405 selado; a juncao .lake/packages segue apontando para a mathlib compilada de C:\t\k404c, nunca para o k405c).
import hashlib as _hl
_NOS_UM = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s", "um.py")
_SHA16_BASE_V405 = _hl.sha256(open(_NOS_UM, "rb").read()).hexdigest()[:16]     # LIDO do um.py do Nos (nada digitado): na v406 o Nos e' a v405 selada; copiar_base_v406.py ainda o confere contra o selo, o ESPERADOS_v405.json e a ordem
_BANNER_KERNEL = ("# [PREPARACAO v406, 02/11/2026 -- ESTADO] SUBIDA MECANICA de preparar_kernel_v405.py (derivar_encanamento_v406.py, lote I). So' o modo `copiar` esta' pronto para a v406 (usa DL.SANDBOX de delta_v406.py e copiar_k406c.sh).\n"
                  "# Os modos `gerar` e `conferir` trazem o corpo da v405 (OITO pedras, ROOT_SUFFIX, STONES...) e dependem do delta completo da v406 (o bundle de ~300 modulos), que a gerencia escreve: NAO os rode antes.\n")


def _banner_kernel(t_):
    assert t_.startswith("# -*- coding: utf-8 -*-\n")
    return t_.replace("# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n" + _BANNER_KERNEL, 1)


entrada("copiar_base_v405.py", autoral=True, regras=[
    ("(3820476c83267f61; o arquivo manda)", "(" + _SHA16_BASE_V405 + "; o arquivo manda)", 1),
    ("A Bancada de producao JA pina a v405 (B13): nao ha salto de versoes.", "A Bancada de producao JA pina a v405 (B14, B14-v405-20261102-R1 segundo a receita [DECLARADO]): nao ha salto de versoes.", 1),
])
entrada("preparar_kernel_v405.py", autoral=True, regras=[
    ("a juncao .lake/packages aponta para a copia da mathlib do k405c, so' leitura", "a juncao .lake/packages aponta para a copia da mathlib do k404c, so' leitura; o k405c NAO e' origem nem alvo", 1),
    (_banner_kernel, "banner do estado da preparacao no topo do arquivo", 1),
])
