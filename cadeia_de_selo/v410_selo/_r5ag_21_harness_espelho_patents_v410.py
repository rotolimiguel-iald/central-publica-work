# -*- coding: utf-8 -*-
"""_r5ag_21_harness_espelho_patents_v410.py -- R5: o delta_v410 passou a abrir, ao importar, o runner do ACOM Mirror (ACOM_MIRROR_RUNNER_ARQ = CENTRAL\\patents\\BR102026003428-2_ACOM_MIRROR\\runner\\one_acom_mirror.py; o pino sha256 e bytes, lido do arquivo por script, D100);
no sandbox do harness_fechar_sandbox_v410.py o CENTRAL da copia do delta e' o proprio sandbox, e o ESPELHO DA CASA so' copiava o que estava sob a pasta work (a casa real: Central de Patentes\\work): o runner nao era achado e o import do delta da copia quebrava (FileNotFoundError),
derrubando o fechar e o registrar_mapa de sandbox e fazendo os controles negativos do fechar dizerem 'NAO RECUSOU' por rc 1 de outra causa. O espelho passa a copiar tambem, na MESMA posicao relativa, os arquivos acessados sob Central de Patentes\\patents (copia de bytes, so' o que o import abriu, nunca sobrescreve);
o nome vai a lista do resumo como qualquer outro arquivo da casa (nao ha' nome vedado no caminho). Idempotente (a contagem exata falha na segunda vez); backup de bytes antes."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from _r5ag_lib_v410 import aplicar

aplicar("harness_fechar_sandbox_v410.py", [
    ('''    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):
        continue
    if _EXCL16 and sha(open(_p_a, "rb").read())[:16] in _EXCL16:''',
     '''    _PAT_REAL = os.path.join(os.path.dirname(_CEN_REAL), "patents")
    if _p_a.startswith(_PAT_REAL + os.sep) and os.path.isfile(_p_a):   # (R5, D100) o runner do ACOM Mirror (o pino do delta), sob Central\\patents: o CENTRAL do delta da copia e' o sandbox, entao vai a SB\\patents na mesma posicao relativa
        _dst_p = os.path.join(SB, "patents", os.path.relpath(_p_a, _PAT_REAL))
        if not os.path.exists(_dst_p):
            os.makedirs(os.path.dirname(_dst_p), exist_ok=True); shutil.copyfile(_p_a, _dst_p); _ESP_N += 1; _ESP_B += os.path.getsize(_dst_p)
            _ESP_LISTA.append(os.path.relpath(_p_a, os.path.dirname(_CEN_REAL)))
        continue
    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):
        continue
    if _EXCL16 and sha(open(_p_a, "rb").read())[:16] in _EXCL16:''', 1)], base=HERE)
