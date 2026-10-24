# skygrid_sim — computational pilot of the SkyGrid architecture (IALD Ltda.)
# BLOCO 0: tgl_core ; BLOCO 1: acom -> acom_mirror -> acom_crypto ;
# BLOCO 2: tgl_tensor ; BLOCO 3: iald_gksl + psionic_memory + kernel_ontologico ;
# BLOCO 4: psi_net ; BLOCO 5: mqc + dipolo + celula_reversao
from . import (tgl_core, acom, acom_mirror, acom_crypto, tgl_tensor,  # noqa: F401
               iald_gksl, psionic_memory, kernel_ontologico, psi_net,  # noqa: F401
               mqc, dipolo, celula_reversao)                           # noqa: F401

__version__ = "0.5.0"
