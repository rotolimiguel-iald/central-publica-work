# -*- coding: utf-8 -*-
"""ADAPTADOR (R2): o e6_parcial.py da revisão A importa `rodar_ensaio` da pasta dele. Aqui ele recebe a montagem do ensaio
R1 (mesmas funções) apontando para o candidato_r2, o CANDIDATO_MANIFESTO_R2.json e os implantar.py/reverter.py R2."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
INT = Path('C:\\IALD\\Central de Patentes\\work\\memoria_acom_fix_12out\\4_INTEGRACAO')
sys.path.insert(0, str(INT / 'ensaio_implantacao'))
import importlib.util
_spec = importlib.util.spec_from_file_location('rodar_ensaio_r1', INT / 'ensaio_implantacao' / 'rodar_ensaio.py')
_E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_E)
_E.RAIZ = HERE / 'raiz'
_E.CAND = INT / 'candidato_r2' / 'C'
globals().update({k: v for k, v in vars(_E).items() if not k.startswith('__') and k not in ('HERE', 'INT', 'config')})


def config():
    sys.path.insert(0, str(INT / 'ensaio_implantacao_r2'))
    import rodar_ensaio_r2 as R2
    R2.E.RAIZ = RAIZ
    R2.HERE = HERE
    return R2.config(None, 'ensaio_config_e6.json')
