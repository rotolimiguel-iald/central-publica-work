# -*- coding: utf-8 -*-
"""_r4ag_14_harness_tema_v410.py -- (a) o tema da fala de 10/11 sobre o teste sem poder preditivo, escrito sem o nome do executor (a D59 o reprova em texto que nao trata do H0DN: a lista das falas); (b) o harness dos textos conhece o pino da ORDEM 02 (sha256 do registro h0dn_bg1_v410, ordem_kimi_02) entre os hashes lidos."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

aplicar("pos_rito/textos_v410.py", [(
    '_TEMA_ESPECIAL = {"nomes_das_sete_pedras_e_tudo_derivado":',
    '_TEMA_ESPECIAL = {"teste_sem_poder_preditivo_nao_se_roda_comando_ao_kimi_o_que_falta": "o teste sem poder preditivo discriminante não se abre: a ordem ao executor sobre o que falta resolver (D96)",\n'
    '                  "nomes_das_sete_pedras_e_tudo_derivado":', 1)])
aplicar("pos_rito/harness_textos_ensaio_v410.py", [(
    '(_hd_h.get("ordem_kimi") or {}).get("sha256"), (_hd_h.get("leitura_dossie") or {}).get("sha256")] + [',
    '(_hd_h.get("ordem_kimi") or {}).get("sha256"), (_hd_h.get("ordem_kimi_02") or {}).get("sha256"), (_hd_h.get("leitura_dossie") or {}).get("sha256")] + [', 1)])
