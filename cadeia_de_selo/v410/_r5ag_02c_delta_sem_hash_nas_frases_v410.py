# -*- coding: utf-8 -*-
"""_r5ag_02c_delta_sem_hash_nas_frases_v410.py -- R5: as frases do dispositivo e da ratificacao D101 (PT e EN) vao tambem ao handoff, ao README e ao Atlas, onde o portao do G1 recusa todo hash de 16 ou 64 hex que o handoff nao traga; por isso as frases NAO carregam hash
(o sha256 da fala 28 fica no contrato, em ratificacao_d101, e na D101 e na E37; o pino do runner, sha256 e bytes, fica no contrato e no registro): a forma continua UMA so', PT e EN, usada igual em todo lugar."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
T.append(('''pino citado por sha256, sha16 " + ACOM_MIRROR_RUNNER["sha256"][:16] + ", não embutido), as âncoras T12 a T15''', '''pino citado por sha256, não embutido), as âncoras T12 a T15''', 1))
T.append(('''pin cited by sha256, sha16 " + ACOM_MIRROR_RUNNER["sha256"][:16] + ", not embedded), the anchors T12 to T15''', '''pin cited by sha256, not embedded), the anchors T12 to T15''', 1))
T.append(('''(D101; fala por sha256 %s), pela regra dele''', '''(D101; a fala está no registro, por sha256), pela regra dele''', 1))
T.append(('''(D101; saying by sha256 %s), by his rule''', '''(D101; the saying is in the record, by sha256), by his rule''', 1))
T.append(('''len(CAMPOS_RATIFICADOS_D101_AESCALA), RATIFICACAO_D101_SHA256[:16] + "...", ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS)''', '''len(CAMPOS_RATIFICADOS_D101_AESCALA), ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS)''', 2))
aplicar("delta_v410.py", T)
