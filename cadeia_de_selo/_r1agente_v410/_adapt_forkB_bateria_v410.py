# -*- coding: utf-8 -*-
"""_adapt_forkB_bateria_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) adapta a v410 os scripts da bateria pre-selo do B(n) (v410\\bateria_pre_selo). O que muda: o controle negativo «selo anterior errado»
usa o selo da versao ANTES da anterior -- na v410 e' a v408, guardada em v409\\base_v408 (a subida mecanica deixara `base_v407`, que e' a de duas versoes antes); o controle chama-se selo_anterior_e_o_da_v408_nao_o_pinado.
O resto a subida mecanica deixou certo e foi conferido linha a linha no diff do bump: o Nos de hoje e a Bancada pinam a v409 (--versao v409; RECIBO_SINCRONIZACAO_v409_* no ensaio), o esboco R3.5 e a bateria sao os pinados na v409
(v409\\PINOS_BN_v409.json e v409\\bateria_pos_selo\\PINOS_BATERIA_v409.json, que existem), o selo e o manifesto anteriores sao os de v410\\base_v409. Em cada arquivo a marca [A ADAPTAR v410] sai e a marca antiga (a da v409, subida) e' retirada.
Trocas de contagem exata; backup de bytes; CRLF respeitado."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_forkB_util_v410 import adaptar, linha, texto, NOTA_FORKB  # noqa: E402


def sem_marca_velha(rel):
    """a linha da marca antiga que o bump subiu ([ADAPTADO v410, 05/11/2026, ...]) sai inteira (a nova vai na marca [ADAPTADO v410, 06/11/2026])."""
    t = texto(rel)
    if "[ADAPTADO v410, 05/11/2026, claude-construtor-v410]" not in t:
        return []
    l_ = linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410]")
    return [(l_ + "\n", "", 1)]


B = "bateria_pre_selo/"
rel = B + "conferir_recibo_pre_selo_v410.py"
l4 = linha(rel, "# (nota herdada da adaptacao da v409 [fork C, 04/11/2026]")
l5 = linha(rel, "# (a subida mecanica deixara `base_v406`")
n4 = (l4.replace("(nota herdada da adaptacao da v409 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v410)",
                 "(nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)")
        .replace("na v410 e' a v407, guardada em v409\\base_v407", "na v410 e' a v408, guardada em v409\\base_v408"))
n5 = l5.replace("(a subida mecanica deixara `base_v406`, que a v409 nao guarda); o controle chama-se selo_anterior_e_o_da_v407_nao_o_pinado.", "(a subida mecanica deixara `base_v407`, duas versoes antes); o controle chama-se selo_anterior_e_o_da_v408_nao_o_pinado.")
assert n4 != l4 and n5 != l5
adaptar(rel, sem_marca_velha(rel) + [
    (l4, n4, 1), (l5, n5, 1),
    ('SELO_V407 = os.path.join(V14, "base_v407", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v407, guardada em v409\\base_v407): o controle negativo "selo anterior errado"',
     'SELO_V408 = os.path.join(V14, "base_v408", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v408, guardada em v409\\base_v408): o controle negativo "selo anterior errado"', 1),
    ('KM_V407 = os.path.join(V14, "base_v407", "tgl_kernel_proof_manifest.json")', 'KM_V408 = os.path.join(V14, "base_v408", "tgl_kernel_proof_manifest.json")', 1),
    ('assert os.path.isfile(SELO_V407) and os.path.isfile(KM_V407), "a base v407 (o selo da versao antes da anterior) nao esta em v409\\\\base_v407"',
     'assert os.path.isfile(SELO_V408) and os.path.isfile(KM_V408), "a base v408 (o selo da versao antes da anterior) nao esta em v409\\\\base_v408"', 1),
    ("ok, rec_t, _ = conferir(RP, RSHA, SELO_V407, KM_V407)", "ok, rec_t, _ = conferir(RP, RSHA, SELO_V408, KM_V408)", 1),
    ('controle("selo_anterior_e_o_da_v407_nao_o_pinado", "SELO_ANTERIOR_NAO_E_O_PINADO", ok, rec_t)', 'controle("selo_anterior_e_o_da_v408_nao_o_pinado", "SELO_ANTERIOR_NAO_E_O_PINADO", ok, rec_t)', 1),
], "controle «selo anterior errado» com a v408 (v409\\base_v408); o resto e' lido do recibo, dos pinos da v409 e da producao; " + NOTA_FORKB)

rel = B + "derivar_pre_selo_v410.py"
l8 = linha(rel, "as fontes (v409\\\\bateria_pre_selo) citam")
l9 = linha(rel, '(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v410, a v407')
adaptar(rel, sem_marca_velha(rel) + [
    (l8, l8.replace("onde a v410 precisa de `base_v407`", "onde a v410 precisa de `base_v408`"), 1),
    (l9, l9.replace("para a v410, a v407, guardada em v409\\\\base_v407", "para a v410, a v408, guardada em v409\\\\base_v408"), 1),
], "o derivador segue RECUSANDO de proposito (os cinco scripts da v410 nasceram da subida e foram adaptados); so' a base do controle mudou no texto (v409\\base_v408); " + NOTA_FORKB)

for rel, nota in ((B + "gerar_pino_recibo_pre_selo_v410.py", "le tudo do recibo do ensaio, do stdout, dos pinos (os da v409) e das fotografias; nada de bundle; os nomes e rotulos v410/v409 conferidos no diff do bump"),
                  (B + "limpar_sandbox_vb21.py", "apaga so' C:\\t\\vb21 depois de provar que nao ha juncao nem link; nao depende de versao"),
                  (B + "snap_producao_v410.py", "so' le a Bancada de producao e o Nos e fotografa; nao depende de versao"),
                  (B + "rodar_bn_pre_selo_v410.sh", "a ordem dos passos da v409; passos 8 e 9 chamam diff_e_pinos_v410 e p00_precondicoes_v410"),
                  (B + "rodar_ensaio_1_pre_selo_v410.sh", "o ensaio pre_selo contra o Nos v409 (canonico hoje), com o esboco e a bateria pinados na v409 (lidos dos pinos); --versao v409")):
    adaptar(rel, sem_marca_velha(rel), nota + "; " + NOTA_FORKB)
print("bateria: ok")
