# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] reexporta as conferencias da v408 por caminho (o corpo da subida de rotulo esta certo; conferido no diff do bump)
# adaptado a v409 (04/11/2026, claude-construtor-v409): a v409 NAO muda a secao do selo pela propria tecnologia; este modulo segue reexportando, por caminho, as conferencias da v408 (o diff do bump e' so' o rotulo e a marca).
"""acom_conferencias_v409.py -- as CONFERENCIAS da cadeia sobre a SECAO do selo pela propria tecnologia. A v409 NAO muda essa secao (o programa v408 selado a traz como esta; o bloco do operador e a adaptacao ficam byte a byte): este modulo apenas REEXPORTA, por caminho,
as conferencias da v408 (que reaproveitam as da v399): esboco_da_bancada, regexes_da_bancada, conferir_alfa_unico, conferir_secao, extrair_bloco, bloco_das_fontes, nomes_de_nivel_de_modulo, literais_de_beta e proveniencia. Importado por gerar_candidato_v409,
ensaio_a_seco_v409, p00_precondicoes_v409 e conferir_rito_v409. Nada daqui e' digitado de memoria: o esboco R3.5 da Bancada e' lido do arquivo pinado."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V408 = os.path.join(os.path.dirname(HERE), "v408")
_spec = importlib.util.spec_from_file_location("acom_conferencias_v408", os.path.join(V408, "acom_conferencias_v408.py"))
A0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A0)
globals().update({k: v for k, v in vars(A0).items() if not k.startswith("__")})
