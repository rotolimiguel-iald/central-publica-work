# -*- coding: utf-8 -*-
"""gerar_sintetico_F41.py -- gera os dados SINTETICOS da qualificacao F4.1 (rodar no WSL /opt/lal_env): 600 s de ruido gaussiano colorido (PSD de projeto O4 do bilby) em H1 e L1,
no formato GWOSC que o strain_io.py le (strain/Strain, meta/GPSstart, mascaras de qualidade de 1 Hz), em ~/.iald_privado (fora do git e de work). Nenhum dado real.
Tambem escreve o MANIFESTO_SINTETICO (sha256 dos arquivos + a injecao so-RG com parametros do centro de D: GW241130_034908; SNR-alvo 14,0 = tipico de D).
Criacao exclusiva: nunca sobrescreve."""
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "codigo_D"))
import injecao_c2 as I  # noqa: E402
import v1_ramo_b as V  # noqa: E402

SAIDA = Path(V.native("C:/Users/rotol/.iald_privado/conjunto_D_20261029/sintetico"))
T0 = 1300000000
DURACAO = 600
FS = 4096
GPS_REF = T0 + 560.3          # "instante do evento" fictício: nada ha ali; a janela de ruido da injecao termina >= 76 s antes
EVENTO_MOLDE = "GW241130_034908"   # SNR 13,8; M_f,det 70; chi_eff 0,05: centro de D
SNR_ALVO = 14.0
SEMENTES = {"H1": 20261103, "L1": 20261104}


def gerar_hdf5(det, caminho):
    import bilby
    import h5py
    bilby.core.utils.random.seed(SEMENTES[det])
    np.random.seed(SEMENTES[det])
    ifo = bilby.gw.detector.get_empty_interferometer(det)
    ifo.set_strain_data_from_power_spectral_density(sampling_frequency=FS, duration=DURACAO, start_time=T0)
    x = np.asarray(ifo.strain_data.time_domain_strain, dtype=np.float64)
    assert len(x) == DURACAO * FS and np.isfinite(x).all()
    with h5py.File(caminho, "x") as h:
        d = h.create_dataset("strain/Strain", data=x)
        d.attrs["Xspacing"] = 1.0 / FS
        d.attrs["Xstart"] = float(T0)
        h.create_dataset("meta/GPSstart", data=np.int64(T0))
        h.create_dataset("meta/Duration", data=np.int64(DURACAO))
        h.create_dataset("quality/simple/DQShortnames", data=np.array([b"DATA", b"CBC_CAT1", b"CBC_CAT2", b"CBC_CAT3"]))
        h.create_dataset("quality/simple/DQmask", data=np.full(DURACAO, 15, dtype=np.uint32))
        h.create_dataset("quality/injections/InjShortnames", data=np.array([b"NO_CBC_HW_INJ", b"NO_BURST_HW_INJ", b"NO_DETCHAR_HW_INJ", b"NO_STOCH_HW_INJ"]))
        h.create_dataset("quality/injections/Injmask", data=np.full(DURACAO, 15, dtype=np.uint32))


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    cat = V.catalogo_d([EVENTO_MOLDE])[EVENTO_MOLDE]
    z = cat["z"]
    ex = I._extrinsecos("SYN_F41")
    start = math.floor(GPS_REF) - I.DESLOC_REAL - I.DESLOC_C2
    geocent = start + (GPS_REF - (math.floor(GPS_REF) - I.DESLOC_REAL))
    inj = {"mass_1": cat["m1_src"] * (1 + z), "mass_2": cat["m2_src"] * (1 + z), "chi_1": cat["chi_eff"], "chi_2": cat["chi_eff"], "luminosity_distance": I.dl_mpc(z),
           "theta_jn": ex["theta_jn"], "phase": ex["phase"], "ra": ex["ra"], "dec": ex["dec"], "psi": ex["psi"], "geocent_time": geocent,
           "dtau220": 0.0, "dtau440": 0.0, "domega220": 0.0, "domega440": 0.0}
    strain = {}
    for det in ("H1", "L1"):
        p = SAIDA / ("SYN_F41_%s_600s.hdf5" % det)
        gerar_hdf5(det, p)
        raw = p.read_bytes()
        strain[det] = {"hdf5": "C:/Users/rotol/.iald_privado/conjunto_D_20261029/sintetico/" + p.name, "hdf5_bytes": len(raw), "hdf5_sha256": hashlib.sha256(raw).hexdigest()}
    man = {"nome": "SYN_F41", "estatuto": "SINTETICO (ruido gaussiano da PSD de projeto O4 do bilby; nenhum dado real)", "gerado_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "GPS": GPS_REF, "gps_inicio_arquivo": T0, "duracao_arquivo_s": DURACAO, "segment_start_GPS": float(start), "snr_rede": SNR_ALVO,
           "molde": "centro de D: " + EVENTO_MOLDE + " (m_det = m_fonte*(1+z); chi1 = chi2 = chi_eff)", "sementes_ruido": SEMENTES,
           "injecao": inj, "strain": strain}
    raw = (json.dumps(man, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with open(HERE / "SINTETICO_F41_MANIFESTO.json", "xb") as f:
        f.write(raw)
    print("manifesto", hashlib.sha256(raw).hexdigest(), {d: s["hdf5_sha256"][:16] for d, s in strain.items()})


if __name__ == "__main__":
    main()
