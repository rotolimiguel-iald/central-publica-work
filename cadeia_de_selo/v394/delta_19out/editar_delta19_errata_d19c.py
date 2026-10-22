# -*- coding: utf-8 -*-
"""editar_delta19_errata_d19c.py -- DELTA 19/10 (rodada d19c): acrescenta a delta19_v394.py (a UNICA definicao do delta) as tres formas da frase de ERRATA AO LADO sobre a palavra «teoremas»
(a escada conta bandeiras: declaracoes nomeadas, teoremas e definicoes). Backup de BYTES antes (.bak_<STAMP>_c1d19c), temporario -> conferir tamanho -> substituir, idempotente."""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
ALVO = os.path.join(V, "delta19_v394.py")
raw = open(ALVO, "rb").read()
MARCA = b"ERRATA_TEOREMAS_PT"
if MARCA in raw:
    print("JA APLICADO (idempotente): delta19_v394.py ja tem ERRATA_TEOREMAS_PT"); sys.exit(0)
bloco = '''

# ---------------------------------------------------------------- a ERRATA AO LADO da palavra «teoremas» (gerencia c1, 19/10/2026, rodada d19c; ordem da gerencia): os modulos novos tem mais declaracoes que teoremas
# (teoremas E definicoes); a escada conta BANDEIRAS de declaracoes nomeadas, todas no trio. O rotulo «teoremas limpos: N/M» fica como REGISTRO DE MAQUINA (o pos-rito o le); nenhum numero digitado aqui:
# se um texto quiser dar T e D, gera-os por script do kernel (delta_vs_v393 de KH_N1) e cita a fonte.
ERRATA_TEOREMAS_PT = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_PT = r"a escada conta bandeiras --- declarações nomeadas, teoremas e definições --- com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_EN = r"the ladder counts flags --- named declarations, theorems and definitions --- with axioms in the trio; the label ``teoremas limpos'' (``clean theorems'') stays as a machine record"
'''
nov = raw + bloco.encode("utf-8")
stamp = time.strftime("%Y%m%d_%H%M%S")
bak = ALVO + ".bak_%s_c1d19c" % stamp
assert not os.path.exists(bak)
open(bak, "wb").write(raw)
assert open(bak, "rb").read() == raw
tmp = ALVO + ".tmp_c1d19c"
open(tmp, "wb").write(nov)
assert os.path.getsize(tmp) == len(nov) > len(raw)
os.replace(tmp, ALVO)
assert open(ALVO, "rb").read() == nov
print("OK: delta19_v394.py %d B -> %d B (sha16 %s -> %s); backup %s" % (len(raw), len(nov), hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(nov).hexdigest()[:16], os.path.basename(bak)))
