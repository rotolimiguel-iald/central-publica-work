# -*- coding: utf-8 -*-
"""gerar_jobs_D.py -- monta os JOBS de PE do conjunto D (cegos e C2) a partir dos PINOS. Gera PROPOSTA (nao congelada): os campos do amostrador (D2: nlive, walks,
maxcall, parede) sao argumentos e so se fixam no CONGELAMENTO, depois da medida de F4.1. Valida cada job com o guard_D.validate_job_D E com o validate_config do
pe_runner.py ORIGINAL (copia somente-leitura, carregado com guard_D no lugar do registration_guard). Nao lanca nada.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import guard_D as G  # noqa: E402
import v1_ramo_b as V  # noqa: E402

COSMO = {"remnant_fit": "LAL_SEOBNRv4_aligned_NR_fit", "cosmology_name": "Planck18_external_INPUT",
         "cosmology_source_path": "/opt/lal_env/lib/python3.12/site-packages/astropy/cosmology/data/Planck18.ecsv",
         "cosmology_parameters": {"H0_km_s_Mpc": 67.66, "Om0": 0.30966, "Tcmb0_K": 2.7255, "Neff": 3.046, "m_nu_eV": [0.0, 0.0, 0.06], "Ob0": 0.04897}}
JOB_REGISTRADO = "C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1_1_3.json"


def _cosmo_input():
    """O bloco remnant_conversion_INPUT: o mesmo do job registrado da GW250114 (path e sha256 do Planck18.ecsv do runtime pinado)."""
    j = json.loads(Path(V.native(JOB_REGISTRADO)).read_text(encoding="utf-8"))["pe_jobs"]["GW250114_PILOT_V2_S220"]["remnant_conversion_INPUT"]
    c = dict(COSMO)
    c["cosmology_source_sha256"] = j["cosmology_source_sha256"]
    if j["cosmology_parameters"] != c["cosmology_parameters"] or j["cosmology_source_path"] != c["cosmology_source_path"]:
        raise RuntimeError("bloco de cosmologia difere do registrado")
    return c


def _semente(nome):
    return int.from_bytes(hashlib.sha256(("RAMOB_V1_D_SAMPLER:" + nome).encode()).digest()[:4], "big") % (2 ** 31 - 1)


def _base(reg, ev, nome, amostrador, wall):
    e = G._entrada(reg, ev)
    dados = {}
    for det in ("H1", "L1"):
        s = e["strain"][det]
        dados[det] = {"onsource_path": s["hdf5"], "onsource_sha256": s["hdf5_sha256"], "offsource_path": s["hdf5"], "offsource_sha256": s["hdf5_sha256"]}
    return {"event": ev, "variant": "registered_fixed_deformation_variant", "privacy_mode": "procedural_same_host",
            "fixed_deformation_parameters": {"dtau440": 0.0, "domega220": 0.0, "domega440": 0.0},
            "remnant_conversion_INPUT": _cosmo_input(), "output_directory_name": nome, "label": nome, "event_GPS": e["GPS"],
            "duration_s": G.DURACAO_S, "sample_rate_hz": 4096, "minimum_frequency_hz": 20.0, "maximum_frequency_hz": 1024.0, "reference_frequency_hz": 20.0,
            "psd_duration_s": 256, "psd_segment_s": 8, "offsource_exclusion_s": 16.0, "onsource_roll_off_s": 0.2,
            "quality_required": ["DATA", "CBC_CAT1", "CBC_CAT2", "CBC_CAT3"],
            "injection_flags_required": ["NO_CBC_HW_INJ", "NO_BURST_HW_INJ", "NO_DETCHAR_HW_INJ", "NO_STOCH_HW_INJ"],
            "detectors": ["H1", "L1"], "data": dados, "wall_budget_seconds": wall,
            "sampler": {"seed": _semente(nome), "workers": amostrador["workers"], "nlive": amostrador["nlive"], "dlogz": 0.1, "walks": amostrador["walks"],
                        "maxcall": amostrador["maxcall"], "minimum_posterior_samples": 1000, "minimum_effective_samples": 100},
            "prior_scope": "INPUT broad priors (D1: d_L ate 10 000 Mpc); so dtau220 livre; GR higher modes remain",
            "generation_sample_rate_hz": 8192, "generation_maximum_frequency_hz": 4096}


def job_cego(reg, ev, amostrador, wall):
    nome = "D_" + ev
    cfg = _base(reg, ev, nome, amostrador, wall)
    cfg.update(mode="blind_test", segment_start_GPS=float(reg["eventos"][ev]["segment_start_real"]), priors=G.priors_do_evento(reg, ev))
    return nome, cfg


def job_c2(reg, inj, amostrador, wall):
    ev = inj["evento"]
    nome = inj["id"]
    cfg = _base(reg, ev, nome, amostrador, wall)
    cfg.update(mode="calibration", segment_start_GPS=float(inj["segment_start_GPS"]),
               priors=G.priors_do_evento(reg, ev, inj["parameters"]["geocent_time"]),
               injection={"family": inj["family"], "noise_kind": inj["noise_kind"], "target_network_optimal_SNR": inj["target_network_optimal_SNR"],
                          "parameters": inj["parameters"]})
    return nome, cfg


def job_sintetico(reg, nome, amostrador, wall):
    """F4.1: injecao so-RG (dtau220 = 0) em ruido SINTETICO gaussiano com SNR tipico de D; mesmo caminho de codigo dos jobs reais (guarda -> controlador -> PE)."""
    ev = "SYN_F41"
    s = reg["sinteticos"][ev]
    cfg = _base(reg, ev, nome, amostrador, wall)
    cfg.update(mode="calibration", segment_start_GPS=float(s["segment_start_GPS"]), priors=G.priors_do_evento(reg, ev, s["injecao"]["geocent_time"]),
               injection={"family": "pSEOBNRv4HM_PA", "noise_kind": "REAL_OFFSOURCE", "target_network_optimal_SNR": s["snr_rede"], "parameters": dict(s["injecao"])})
    cfg["prior_scope"] = "F4.1 SINTETICO (rotulo noise_kind exigido pelo injetor); " + cfg["prior_scope"]
    return nome, cfg


def job_repeticao(reg, nome_primario, cfg_primario, fator_maxcall, wall):
    """D5: a repeticao e um job PRE-REGISTRADO no congelamento (maxcall x fator, nova semente do amostrador), disparado so por bandeira de convergencia."""
    nome = nome_primario + "_R1"
    cfg = json.loads(json.dumps(cfg_primario))
    cfg["output_directory_name"] = nome
    cfg["label"] = nome
    cfg["sampler"]["maxcall"] = int(cfg["sampler"]["maxcall"] * fator_maxcall)
    cfg["sampler"]["seed"] = _semente(nome)
    cfg["wall_budget_seconds"] = wall
    return nome, cfg


def validar_com_pe_runner(cfgs):
    """validate_config do pe_runner ORIGINAL (copia RO), com guard_D no lugar do registration_guard. So estrutura; nao inicia ciencia."""
    sys.modules["registration_guard"] = G
    arq = BASE / "copias_somente_leitura" / "pe_runner.py"
    sys.path.insert(0, str(BASE / "copias_somente_leitura"))
    spec = importlib.util.spec_from_file_location("pe_runner_ro", arq)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for nome, cfg in cfgs.items():
        mod.validate_config(cfg)
    return True


def construir(reg, desenho_c2=None, amostrador=None, wall=8 * 3600):
    amostrador = amostrador or {"nlive": 512, "walks": 50, "maxcall": 3_000_000, "workers": 24}
    jobs = dict(job_cego(reg, ev, amostrador, wall) for ev in reg["eventos_d10"])
    if desenho_c2:
        for inj in desenho_c2["injecoes"]:
            n, c = job_c2(reg, inj, amostrador, wall)
            jobs[n] = c
    return jobs
