# -*- coding: utf-8 -*-
"""congelar_oficial_opcao_c_03nov.py -- (1) regenera PINOS_D_V1.json OFICIAL com as pecas novas (arvore de codigo), o evento sintetico SYN_F41 e o runtime do WSL
(backup de bytes .bak_<ts> do arquivo anterior; nenhuma analise foi lancada com os pinos antigos); (2) confere strain (sha256 dos 20 HDF5) e sinteticos; (3) congela:
JOBS_D_V1.json + CONGELAMENTO_D.json (criacao exclusiva). NAO abre o relogio (isso e abrir_relogio_03nov.py) e NAO lanca nada."""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "codigo_D"))
import congelar_D as CG  # noqa: E402
import gerar_pinos_D as GP  # noqa: E402
import guard_D as G  # noqa: E402


def main():
    assert not G.RELOGIO.exists(), "relogio ja aberto: nao se regeram pinos depois"
    assert not G.JOBS.exists() and not G.CONGELAMENTO.exists(), "ja congelado"
    pinos, h = GP.montar(runtime_json=str(HERE / "runtime_wsl.json"), sinteticos_manifesto=str(HERE / "SINTETICO_F41_MANIFESTO.json"))
    print("PINOS_D_V1.json", h, "| sinteticos", list(pinos["sinteticos"]), "| arquivos de codigo", len(pinos["codigo"]))
    reg, dig = G.checked_registration(verificar_relogio=False)
    assert dig == h
    t = time.time()
    G.verificar_strain_bytes()
    print("strain: 20/20 sha256 iguais ao manifesto (%.1f s); sinteticos conferidos em checked_registration" % (time.time() - t))
    cong, hj, hc = CG.congelar()
    print("JOBS_D_V1.json", hj, "| jobs", len(cong["jobs"]))
    print("CONGELAMENTO_D.json", hc, "| limites", cong["limites"])


if __name__ == "__main__":
    main()
