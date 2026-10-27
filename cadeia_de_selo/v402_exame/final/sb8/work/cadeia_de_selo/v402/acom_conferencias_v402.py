# -*- coding: utf-8 -*-
"""acom_conferencias_v402.py -- as CONFERENCIAS da cadeia sobre a SECAO do selo pela propria tecnologia. A v402 NAO muda essa secao (o programa v401 selado a traz como esta; o bloco do operador e a adaptacao ficam byte a byte): este modulo apenas REEXPORTA, por caminho,
as conferencias da v401 (que reaproveitam as da v399): esboco_da_bancada, regexes_da_bancada, conferir_alfa_unico, conferir_secao, extrair_bloco, bloco_das_fontes, nomes_de_nivel_de_modulo, literais_de_beta e proveniencia. Importado por gerar_candidato_v402,
ensaio_a_seco_v402, p00_precondicoes_v402 e conferir_rito_v402. Nada daqui e' digitado de memoria: o esboco R3.5 da Bancada e' lido do arquivo pinado."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V401 = os.path.join(os.path.dirname(HERE), "v401")
_spec = importlib.util.spec_from_file_location("acom_conferencias_v401", os.path.join(V401, "acom_conferencias_v401.py"))
A0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A0)
globals().update({k: v for k, v in vars(A0).items() if not k.startswith("__")})
