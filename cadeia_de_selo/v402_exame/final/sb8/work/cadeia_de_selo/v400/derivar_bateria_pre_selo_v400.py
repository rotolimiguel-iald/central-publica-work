# -*- coding: utf-8 -*-
"""derivar_bateria_pre_selo_v400.py -- deriva, SEM executar, os scripts do recibo pre_selo da v400 a partir dos da v399 (bateria_pre_selo\\). O recibo pre_selo da v400 e' o da CADEIA v399 (gerado e pinado ANTES da instalacao da v399,
em ensaio, sobre o um.py v398 que a Bancada de producao AINDA pina): o esboco R3.5 so' gera um pre_selo lendo o Nos pinado pela Bancada, e o Nos ja' e' a v399 (o esboco o recusa: ALPHA_LINHA_NAO_UNICA), de modo que nenhum recibo NOVO e' possivel
sem tocar no Nos; o recibo da v399 segue valido para o passo simples v398 -> v400 e e' RECONFERIDO aqui pela funcao do proprio esboco, contra a Bancada de producao lida agora. Regras com contagem exata (o motor ABORTA se nao casar).
uso: python -I -B -X utf8 derivar_bateria_pre_selo_v400.py [--refazer]"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v400_motor as M  # noqa: E402
from derivar_v400_motor import entre  # noqa: E402

_DOC_CONF = '''"""conferir_recibo_pre_selo_v400.py -- SO LEITURA. Confere o recibo pre_selo (o da cadeia v399: ensaio_1, gerado ANTES da instalacao da v399, sobre o um.py v398 que a Bancada de producao ainda pina) PELO MESMO CAMINHO que o B(n) pos_selo da v400 usara:
conferir_recibo_pre_selo(...) do esboco R3.5 contra a Bancada de PRODUCAO (estado_anterior, so leitura), com o sha do recibo pinado, o selo e o manifesto do kernel da v398
(--selo-anterior / --kernel-manifesto-anterior: as copias de bytes de v400/base_v398) e SEM cadeia de selos (o B(n) da v400 e' um PASSO SIMPLES v398 -> v400: o salto declarado R3.4 passaria pelo elo v399, que o esboco recusa).
ja_sincronizada=False: no B(n) o Nos sera a v400 e a Bancada ainda pinara a v398. Alem da funcao do esboco, repete por script cada condicao da regra (nome, observado, esperado)
e roda cinco controles negativos (recibo adulterado / pino errado), que a funcao do esboco tem de recusar. Esboco e bateria sao os PINADOS (path e sha256 lidos dos pinos da v399, conferidos
contra o disco). Nada e' escrito na producao nem no Nos; so' grava conferencia_pelo_esboco_v400.json ao lado e as copias adulteradas em C:\\\\t\\\\vb17\\\\ctl.
uso: python -I -B -X utf8 conferir_recibo_pre_selo_v400.py"""
'''

ENTRADAS = [
    ("bateria_pre_selo/conferir_recibo_pre_selo_v399.py", "bateria_pre_selo/conferir_recibo_pre_selo_v400.py", [
        entre('"""conferir_recibo_pre_selo_v399.py', "import sys\n\nsys.dont_write_bytecode = True", _DOC_CONF, "docstring"),
        ('V = os.path.dirname(HERE)                                   # ...\\cadeia_de_selo\\v399\nV8 = os.path.join(os.path.dirname(V), "v398")\nCTL = os.path.join("C:" + os.sep, "t", "vb16", "ctl")        # copias adulteradas (sandbox curto, apagado no fim)\n',
         'V = os.path.dirname(HERE)                                   # ...\\cadeia_de_selo\\v400\nV9 = os.path.join(os.path.dirname(V), "v399")               # a cadeia v399: o recibo pre_selo foi gerado ali, ANTES da instalacao da v399\nCTL = os.path.join("C:" + os.sep, "t", "vb17", "ctl")        # copias adulteradas (sandbox curto, apagado no fim)\n', 1),
        ('pbn = lj(os.path.join(V8, "PINOS_BN_v398.json"))\npbat = lj(os.path.join(V8, "bateria_pos_selo", "PINOS_BATERIA_v398.json"))\nESB, ESB_SHA = pbn["esboco_R3_5"]["path"], pbn["esboco_R3_5"]["sha256"]\nBAT, BAT_SHA = pbat["bateria"]["path"], pbat["bateria"]["sha256"]\n',
         'pbn = lj(os.path.join(V9, "PINOS_BN_v399.json"))      # os pinos da v399: o esboco R3.5 e a bateria do pre_selo (a da v398)\nESB, ESB_SHA = pbn["esboco_R3_5"]["path"], pbn["esboco_R3_5"]["sha256"]\nBAT, BAT_SHA = pbn["bateria_do_pre_selo"]["path"], pbn["bateria_do_pre_selo"]["sha256"]\n', 1),
        ('ENS = os.path.join(HERE, "ensaio_1")\n', 'ENS = os.path.join(V9, "bateria_pre_selo", "ensaio_1")\n', 1),
        ('open(os.path.join(HERE, "etapa1_stdout.txt"), encoding="utf-8")', 'open(os.path.join(V9, "bateria_pre_selo", "etapa1_stdout.txt"), encoding="utf-8")', 1),
        ('SELO_V397 = os.path.join(V8, "base_v397", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior: o controle negativo "selo anterior errado"\nKM_V397 = os.path.join(V8, "base_v397", "tgl_kernel_proof_manifest.json")\n',
         'SELO_V397 = os.path.join(V, "base_v399", "um_absoluto_selo.json")      # o selo da v399 (o que o Nos tem): o controle negativo "selo anterior errado" (o da Bancada e o da v398)\nKM_V397 = os.path.join(V, "base_v399", "tgl_kernel_proof_manifest.json")\n', 1),
        ('controle("selo_anterior_e_o_da_v397_nao_o_pinado"', 'controle("selo_anterior_e_o_da_v399_nao_o_pinado"', 1),
        ('"contrato": "CONFERENCIA_PELO_ESBOCO_RECIBO_PRE_SELO_v399"', '"contrato": "CONFERENCIA_PELO_ESBOCO_RECIBO_PRE_SELO_v400"', 1),
        ('"como": ("conferir_recibo_pre_selo do esboco R3.5 com ja_sincronizada=False (no B(n) da v399 o Nos sera a v399 e a Bancada ainda pinara a v398), sem cadeia de selos, "\n             "selo e manifesto do kernel anteriores = copias de bytes v399/base_v398; producao so lida"),',
         '"como": ("conferir_recibo_pre_selo do esboco R3.5 com ja_sincronizada=False (no B(n) da v400 o Nos sera a v400 e a Bancada ainda pinara a v398), sem cadeia de selos, "\n             "selo e manifesto do kernel anteriores = copias de bytes v400/base_v398; recibo = o da cadeia v399 (gerado antes da instalacao da v399); producao so lida"),', 1),
        ('B(n) da v399 torna o recibo obsoleto e a conferencia o recusa"', 'B(n) da v400 torna o recibo obsoleto e a conferencia o recusa"', 1),
        ('dest = os.path.join(HERE, "conferencia_pelo_esboco_v399.json")', 'dest = os.path.join(HERE, "conferencia_pelo_esboco_v400.json")', 1),
        # depois da instalacao da v399 o contrato instalado na Bancada (que pina a v398) reporta PIN_CHANGED: e' o estado ESPERADO do esboco para um Nos que passou adiante (ESPERADOS_POS_SELO), nao uma falha
        ('chk("estado_do_contrato_instalado_ok", ant["estado_do_contrato_instalado"] == "OK", ant["estado_do_contrato_instalado"], "OK")',
         'chk("estado_do_contrato_instalado_e_o_esperado_depois_da_instalacao_da_v399", ant["estado_do_contrato_instalado"] in (("OK",) + tuple(MOD.ESPERADOS_POS_SELO)), ant["estado_do_contrato_instalado"], "OK ou um de ESPERADOS_POS_SELO (PIN_CHANGED: o Nos passou a v399 e a Bancada ainda pina a v398)")', 1),
    ]),
    ("bateria_pre_selo/snap_producao_v399.py", "bateria_pre_selo/snap_producao_v400.py", []),
]


def main():
    refazer = "--refazer" in sys.argv[1:]
    for src, dst, regras in ENTRADAS:
        regras = [r for r in regras]
        r = M.derivar(src, dst, regras, com_bump=(src.endswith("snap_producao_v399.py")), refazer=refazer)
        print("%-52s %-12s %s regras=%d" % (dst, r["estado"][:12], r["destino_sha256"][:12], len(regras)))


if __name__ == "__main__":
    main()
