# -*- coding: utf-8 -*-
"""injecao_c2.py -- DESENHO das injecoes C2 do V1 em ruido OFF-SOURCE REAL dos proprios eventos de D (so-RG e dtau220 = delta_pred_i do V1).

Reaproveita SEM EDITAR a copia somente-leitura de injection_design.py (sha256 pinado) de e2_code_v1_1_2: o modulo e carregado por importlib e DUAS referencias
sao trocadas em memoria: validate_truth_support (exige prior em forma de dicionario inclusive para os parametros FIXOS) por validate_truth_support_D, que aceita o
parametro fixo como escalar -- o "impedimento 2" da NOTA_CONJUNTO_D.md --, e a fonte pSEOB por um envoltorio de mesma assinatura que encaminha a grade de geracao
8192 Hz/4096 Hz -- o "impedimento 3". O resto (SNR-alvo por reescala de distancia, janela fora do intervalo protegido,
mesmos bytes de off-source, chegada do sinal fora da regiao do roll-off) e o codigo original, byte a byte.
Este modulo NAO abre strain: o desenho usa o catalogo (metadados GR publicos), o V1 e os metadados de qualidade ja medidos (dq_meta_D_v2.json).

ESCOLHAS DO DESENHO (ditas ANTES):
  - parametros no centro do posterior GR do CATALOGO: m_det = m_fonte*(1+z); chi_1 = chi_2 = chi_eff (alinhado); extrinsecos por hash do evento (deterministicos);
  - SNR-alvo = SNR de rede do catalogo (SNR otimo de rede; a base e o IMR completo, nao o ringdown);
  - janela de ruido: [floor(GPS) - 108 - 24k, +16 s): termina >= 76 s antes do evento real, longe do intervalo protegido; k = replicas; GR e RB PAREADAS na mesma janela;
  - o dtau220 injetado e 0 (so-RG) ou o delta_pred do V1 para aquele evento (o valor fixado por hash), nunca o do posterior.
"""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
COPIAS = BASE / "copias_somente_leitura"
sys.path.insert(0, str(CODE))
import v1_ramo_b as V  # noqa: E402

DESLOC_REAL = 12
DESLOC_C2 = 96
PASSO_REPLICA_S = 24
DURACAO = 16
H0, OM0 = 67.66, 0.30966        # Planck18 (so ponto de partida do D_L; a distancia e reescalada ao SNR-alvo)


def _u(evento, nome):
    d = hashlib.sha256((evento + ":" + nome).encode()).digest()
    return (int.from_bytes(d[:8], "big") + 0.5) / 2 ** 64


def dl_mpc(z, n=4000):
    """D_L (Mpc) em ΛCDM plano (H0, Om0 de Planck18) por integracao trapezoidal. Ponto de partida; nao e dado."""
    c = 299792.458
    f = lambda zz: 1.0 / math.sqrt(OM0 * (1 + zz) ** 3 + (1 - OM0))
    h = z / n
    s = 0.5 * (f(0) + f(z)) + sum(f(i * h) for i in range(1, n))
    return (1 + z) * c / H0 * s * h


def validate_truth_support_D(params, priors):
    """Como validate_truth_support do original, mas um parametro FIXO (escalar no prior) deve ser igual a verdade."""
    required = {"mass_1", "mass_2", "luminosity_distance", "chi_1", "chi_2", "theta_jn", "phase", "ra", "dec", "psi", "geocent_time",
                "dtau220", "dtau440", "domega220", "domega440"}
    if set(priors) != required | {"mass_ratio"} or not required <= set(params):
        raise ValueError("Complete registered recovery prior and injection truth required")
    if set(params) - required - {"mass_ratio"}:
        raise ValueError("Unknown injection truth coordinate")
    if params["mass_1"] <= 0 or params["mass_2"] <= 0:
        raise ValueError("Invalid injection mass")
    q = params["mass_2"] / params["mass_1"]
    if "mass_ratio" in params and params["mass_ratio"] != q:
        raise ValueError("Injection mass ratio inconsistent")
    for name in sorted(required | {"mass_ratio"}):
        v = q if name == "mass_ratio" else params[name]
        p = priors[name]
        if isinstance(p, (int, float)) and not isinstance(p, bool):       # parametro fixo
            if v != p:
                raise ValueError("Injection truth differs from fixed parameter: " + name)
            continue
        if p["kind"] not in ("Uniform", "Sine", "Cosine", "Constraint"):
            raise ValueError("Unsupported truth prior")
        if not math.isfinite(v) or not p["minimum"] <= v <= p["maximum"]:
            raise ValueError("Injection truth outside recovery prior: " + name)
    if q > 1:
        raise ValueError("Injection masses not ordered")
    return True


def carregar_injection_design():
    """Carrega a COPIA somente-leitura (sha256 conferido) e troca UMA funcao. Precisa de lal/bilby (WSL /opt/lal_env)."""
    pin = None
    arq = COPIAS / "injection_design.py"
    sha = hashlib.sha256(arq.read_bytes()).hexdigest()
    for linha in (BASE / "copias_somente_leitura.SHA256.txt").read_text().splitlines():
        h, nome = linha.split()
        if nome.lstrip("*") == "injection_design.py":
            pin = h
    if pin is None or sha != pin:
        raise RuntimeError("copia de injection_design.py difere do sha256 registrado")
    sys.path.insert(0, str(COPIAS))
    spec = importlib.util.spec_from_file_location("injection_design_ro", arq)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.validate_truth_support = validate_truth_support_D
    # "impedimento 3" da NOTA_CONJUNTO_D.md: o gerador do injetor original nao encaminha generation_sample_rate_hz/generation_maximum_frequency_hz,
    # que o pseob_source vigente EXIGE. Envolvemos a fonte com a MESMA assinatura (bilby infere os parametros pela assinatura) e fixamos 8192 Hz / 4096 Hz,
    # os valores da qualificacao R5 e dos jobs registrados. O corpo da fonte e o do original.
    orig = mod.pseob_frequency_domain

    def pseob_fd_com_geracao(frequency_array, mass_1, mass_2, luminosity_distance, chi_1, chi_2, theta_jn, phase,
                             dtau220, dtau440, domega220=0., domega440=0., geocent_time=None, **kwargs):
        kwargs.setdefault("generation_maximum_frequency_hz", 4096)
        kwargs.setdefault("generation_sample_rate_hz", 8192)
        return orig(frequency_array, mass_1, mass_2, luminosity_distance, chi_1, chi_2, theta_jn, phase,
                    dtau220, dtau440, domega220, domega440, geocent_time=geocent_time, **kwargs)

    mod.pseob_frequency_domain = pseob_fd_com_geracao
    return mod


def _janela_dentro_da_corrida(dq, evento, start_c2, gps_inicio_arquivo):
    """Janela [start_c2, start_c2+16) dentro da maior corrida limpa antes do evento, nos DOIS detectores (metadados ja medidos; nenhum strain)."""
    ok = {}
    for det in ("H1", "L1"):
        r = dq[evento + "_" + det]
        a = r["longest_run_start_idx"]
        b = a + r["longest_ok_run_before_event_s"]
        i0 = int(start_c2 - gps_inicio_arquivo)
        ok[det] = bool(a <= i0 and i0 + DURACAO <= b and (i0 - a) >= 0)
    return ok


def _extrinsecos(evento):
    return {"ra": 2 * math.pi * _u(evento, "ra"), "dec": math.asin(2 * _u(evento, "dec") - 1), "psi": math.pi * _u(evento, "psi"),
            "phase": 2 * math.pi * _u(evento, "phase"), "theta_jn": math.acos(1 - 2 * _u(evento, "theta_jn"))}


def escolher_eventos(snr_por_evento, m):
    ordem = sorted(snr_por_evento, key=lambda e: snr_por_evento[e])
    idx = sorted({round(i * (len(ordem) - 1) / (m - 1)) for i in range(m)}) if m > 1 else [0]
    return [ordem[i] for i in idx], ordem


def desenho_c2(pinos, dq, tamanho):
    """tamanho: 'minima' (10 PE: 5 eventos x {GR,RB}), 'media' (20 PE: 10 x 2), 'ampla' (50 PE: 25 por classe)."""
    snr = {e: pinos["eventos"][e]["snr_rede"] for e in pinos["eventos_d10"]}
    if tamanho == "minima":
        eventos, _ = escolher_eventos(snr, 5)
        reps = {e: 1 for e in eventos}
    elif tamanho == "media":
        eventos, _ = escolher_eventos(snr, 10)
        reps = {e: 1 for e in eventos}
    elif tamanho == "ampla":
        eventos, ordem = escolher_eventos(snr, 10)
        reps = {e: (3 if i % 2 == 0 else 2) for i, e in enumerate(ordem)}
    else:
        raise ValueError("tamanho desconhecido")
    lista = []
    for ev in eventos:
        e = pinos["eventos"][ev]
        gps = e["GPS"]
        gps_arq = int(e["strain"]["H1"]["hdf5"].rsplit("-", 2)[-2])
        # a grade: igual para H1/L1 (os arquivos de 4096 s do GWOSC comecam no mesmo GPS)
        cat = e["catalogo"]
        z = cat["z"]
        m1 = cat["m1_src"] * (1 + z)
        m2 = cat["m2_src"] * (1 + z)
        ex = _extrinsecos(ev)
        for k in range(reps[ev]):
            start = math.floor(gps) - DESLOC_REAL - DESLOC_C2 - PASSO_REPLICA_S * k
            dentro = _janela_dentro_da_corrida(dq, ev, start, gps_arq)
            if not all(dentro.values()):
                raise ValueError("janela C2 fora da corrida limpa: %s k=%d %s" % (ev, k, dentro))
            geocent = start + (gps - (math.floor(gps) - DESLOC_REAL))
            for classe in ("GR", "RB"):
                dt = 0.0 if classe == "GR" else e["delta_pred_pinado"]
                params = {"mass_1": m1, "mass_2": m2, "chi_1": cat["chi_eff"], "chi_2": cat["chi_eff"], "luminosity_distance": dl_mpc(z),
                          "theta_jn": ex["theta_jn"], "phase": ex["phase"], "ra": ex["ra"], "dec": ex["dec"], "psi": ex["psi"],
                          "geocent_time": geocent, "dtau220": dt, "dtau440": 0.0, "domega220": 0.0, "domega440": 0.0}
                lista.append({"id": "C2_%s_%s_r%d" % (ev, classe, k), "evento": ev, "classe": classe, "replica": k,
                              "segment_start_GPS": float(start), "duration_s": DURACAO, "janela_dentro_da_corrida_limpa": dentro,
                              "termina_antes_do_evento_s": float(gps - (start + DURACAO)), "target_network_optimal_SNR": e["snr_rede"],
                              "parameters": params, "family": "pSEOBNRv4HM_PA", "noise_kind": "REAL_OFFSOURCE"})
    n_classe = {c: sum(1 for x in lista if x["classe"] == c) for c in ("GR", "RB")}
    return {"tamanho": tamanho, "n_PE": len(lista), "n_por_classe": n_classe, "eventos": eventos, "injecoes": lista}
