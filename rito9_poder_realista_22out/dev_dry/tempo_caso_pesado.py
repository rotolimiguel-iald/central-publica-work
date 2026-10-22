"""Cronometra um caso PESADO fora das familias pre-registradas (K=4, S=13, G=1.8, flat, tau=900, f=0.85, ell=11)."""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "ferramentas"))
import nucleo_poder as N  # noqa: E402
import rodar_estudo as R  # noqa: E402

cfg = json.load(open(os.path.join(AQUI, "config_dry.json"), encoding="utf-8"))
num = cfg["numerica"]
um = N.ler_alpha_um(cfg["beta"]["um_py"])
beta = N.beta_de_alpha(um["alpha"])
g = N.perfil_burst(4, 13.0, 1.8, "flat", 1.0, 0.6)
caso = dict(case_id="DEV|pesado", familia="P2", perfil_id="dev", ell_km=11.0, K=4, S_ms=13.0, gamma_ms=1.8, amp="flat",
            tau_ms=900.0, f_tail=0.85, perfil=N.perfil_dict("P2", g, 0.85, 900.0, "dev"))
t0 = time.perf_counter()
row, scan = R.avaliar_caso((caso, beta, num))
print("segundos:", time.perf_counter() - t0)
for k in ("status", "erro", "n_celulas", "delta_rede", "kl_h1_h0_cap", "kl_h0_h1", "n_req", "c_n_em_n_req", "poder_em_n_req", "exata_todas", "fora_max", "monotono_ok"):
    print(k, row.get(k))
print("n avaliados:", len(scan), "max L:", max(r["L"] for r in scan))
