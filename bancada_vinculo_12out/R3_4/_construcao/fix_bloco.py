# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from pathlib import Path
P = Path("bloco_novos_r3_4.py.txt")
t = P.read_text(encoding="utf-8")
def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (t.count(old), old[:100])
    t = t.replace(old, new)
sub('("sha_em_maiuscula", _mut_sha_maiusculo if False else _mut_sha_maiusculo, "CADEIA_DE_SELOS_ARQUIVO_INVALIDO")', '("sha_em_maiuscula", _mut_sha_maiusculo, "CADEIA_DE_SELOS_ARQUIVO_INVALIDO")')
sub('("versao_repetida", _mut_versao_repetida, "CADEIA_DE_SELOS_NAO_CONSECUTIVA")', '("versao_do_elo_diferente_do_um_py_da_copia", _mut_versao_repetida, "CADEIA_DE_SELOS_UM_PY_DE_OUTRA_VERSAO")')
sub('NI_REAL := MOD.ler_nos(NOS_REAL, VR), VR)["conferidos_contra_o_nos_lido"], None)', '_ni_real, VR)["conferidos_contra_o_nos_lido"], None)')
sub('MOD.conferir_pinos_da_versao(_pv(mut_), NI_REAL, VR)', 'MOD.conferir_pinos_da_versao(_pv(mut_), _ni_real, VR)')
sub('MOD.conferir_pinos_da_versao(json.loads(BAT.read_bytes()), NI_REAL, VR)', 'MOD.conferir_pinos_da_versao(json.loads(BAT.read_bytes()), _ni_real, VR)')
sub('AUD_BASE = (arv_aud := (FX / "kernel_src_v393s" / "TGLExt" / "AuditoriaSinteticaC.lean").read_text(encoding="utf-8"))', 'AUD_BASE = (FX / "kernel_src_v393s" / "TGLExt" / "AuditoriaSinteticaC.lean").read_text(encoding="utf-8")')
P.write_text(t, encoding="utf-8", newline="")
print("ok")
