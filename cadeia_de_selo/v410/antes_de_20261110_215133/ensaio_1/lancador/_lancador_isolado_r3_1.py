# -*- coding: utf-8 -*-
# lancador do sincronizar_bancada.py R3.1 (A4): roda o script pinado com o site do usuario como CAMINHO
# (nenhum .pth, nenhum usercustomize executa); o filho ja roda com -E -P -s
import runpy
import sys


def _principal():
    site_usuario, script = sys.argv[1], sys.argv[2]
    sys.argv = [script] + sys.argv[3:]
    if site_usuario != '-':
        sys.path.append(site_usuario)
    runpy.run_path(script, run_name='__main__')


_principal()
