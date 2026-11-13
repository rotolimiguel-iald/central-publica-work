# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411] conferido: o corpo da subida de rotulo esta certo para a v411 (reexporta por caminho as conferencias da v410; a v411 NAO muda a secao do selo pela propria tecnologia); ver bump/acom_conferencias_v411.py.diff
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] reexporta as conferencias da v409 por caminho (a v410 NAO muda a secao do selo pela propria tecnologia; o corpo da subida de rotulo esta certo; conferido no diff do bump); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (marca herdada da v410, com o rotulo da epoca: adaptado a v410 (06/11/2026, claude-construtor-v410, fork B): a v410 NAO muda a secao do selo pela propria tecnologia; o modulo reexporta, por caminho, as conferencias da v409.)
"""acom_conferencias_v411.py -- as CONFERENCIAS da cadeia sobre a SECAO do selo pela propria tecnologia. A v411 NAO muda essa secao (o programa v410 selado a traz como esta; o bloco do operador e a adaptacao ficam byte a byte): este modulo apenas REEXPORTA, por caminho,
as conferencias da v410 (que reaproveitam as da v399): esboco_da_bancada, regexes_da_bancada, conferir_alfa_unico, conferir_secao, extrair_bloco, bloco_das_fontes, nomes_de_nivel_de_modulo, literais_de_beta e proveniencia. Importado por gerar_candidato_v411,
ensaio_a_seco_v411, p00_precondicoes_v411 e conferir_rito_v411. Nada daqui e' digitado de memoria: o esboco R3.5 da Bancada e' lido do arquivo pinado."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V410 = os.path.join(os.path.dirname(HERE), "v410")
_spec = importlib.util.spec_from_file_location("acom_conferencias_v410", os.path.join(V410, "acom_conferencias_v410.py"))
A0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A0)
globals().update({k: v for k, v in vars(A0).items() if not k.startswith("__")})
