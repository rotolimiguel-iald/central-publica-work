# -*- coding: utf-8 -*-
"""gerar_artefatos_03nov.py -- gera os artefatos oficiais da parametrizacao (pinos, desenho C2, poder de planejamento, proposta de jobs, escolhas do desenho).
Roda UMA vez depois que o codigo estiver final (os pinos amarram a arvore de codigo). Nao abre strain, nao lanca PE, nao abre o relogio.
Regra do backup imediato: arquivo existente => copia de bytes .bak_<ts> antes de tocar (os de criacao exclusiva falham se existirem).
"""
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "codigo_D"))
import gerar_jobs_D as J  # noqa: E402
import gerar_pinos_D as GP  # noqa: E402
import guard_D as G  # noqa: E402
import injecao_c2 as I  # noqa: E402
import poder_planejamento as PP  # noqa: E402
import v1_ramo_b as V  # noqa: E402

DQ = Path("C:/IALD/Central de Patentes/work/conjunto_D_20261029/smoke/dq_meta_D_v2.json")


def gravar(nome, obj, exclusivo=True):
    p = HERE / nome
    raw = (json.dumps(obj, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    if p.exists() and not exclusivo:
        p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(p.read_bytes())
    with open(p, "xb" if exclusivo else "wb") as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    G.SAIDAS.mkdir(parents=True, exist_ok=True)       # run_controlled faz out.mkdir() sem parents
    pinos, h_pinos = GP.montar(runtime_json=str(HERE / "runtime_wsl.json"))
    print("PINOS_D_V1.json", h_pinos)
    reg, dig = G.checked_registration(verificar_relogio=False)
    assert dig == h_pinos
    t = time.time()
    fbytes = G.verificar_strain_bytes()                # sha256 completo dos 20 HDF5 contra o MANIFESTO (so bytes)
    print("strain: 20/20 sha256 iguais ao manifesto em %.1f s" % (time.time() - t))
    dq = json.loads(DQ.read_text())
    desenho = {"fonte": "injecao_c2.desenho_c2", "dq_meta_sha256": V.sha256_file(str(DQ)), "pinos_sha256": h_pinos,
               "regras": {"janela": "[floor(GPS)-108-24k, +16 s): termina >= 76 s antes do evento real; GR e RB pareadas na mesma janela; k = replicas",
                          "parametros": "m_det = m_fonte*(1+z); chi_1 = chi_2 = chi_eff; extrinsecos por hash do evento; dtau220 = 0 (GR) ou delta_pred do V1 (RB)",
                          "SNR_alvo": "SNR de rede do catalogo (otimo de rede, IMR completo); distancia reescalada pelo injetor original",
                          "ruido": "off-source REAL do proprio evento, mesmos bytes do PSD; nada e lido aqui (desenho)"},
               "tamanhos": {t: I.desenho_c2(pinos, dq, t) for t in ("minima", "media", "ampla")}}
    h_des = gravar("DESENHO_C2_03nov.json", desenho)
    print("DESENHO_C2_03nov.json", h_des)
    out, raw = PP.gerar()
    with open(HERE / "PODER_RAMO_B_ANTES_DE_ABRIR.json", "xb") as f:
        f.write(raw)
    h_pod = hashlib.sha256(raw).hexdigest()
    print("PODER_RAMO_B_ANTES_DE_ABRIR.json (rascunho)", h_pod)
    amost = {"nlive": 512, "walks": 50, "maxcall": 3_000_000, "workers": 24}
    jobs = J.construir(reg, desenho["tamanhos"]["ampla"], amost, 8 * 3600)
    for nome, cfg in jobs.items():
        G.validate_job_D(reg, nome, cfg)
    J.validar_com_pe_runner(jobs)
    indice = {t: [x["id"] for x in desenho["tamanhos"][t]["injecoes"]] for t in ("minima", "media", "ampla")}
    prop = {"estagio": "PROPOSTA_NAO_CONGELADA__D2_AMOSTRADOR_E_PAREDE_SAEM_DA_MEDIDA_DE_F4_1",
            "aviso": "nlive/walks/maxcall/parede sao os valores do piloto da GW250114 (que NAO convergiu em maxcall); o congelamento os substitui pela medida de F4.1. "
                     "Nao e carregavel pelo guarda (load_jobs le JOBS_D_V1.json); o congelamento escolhe o subconjunto C2 por tamanho.",
            "pinos_sha256": h_pinos, "amostrador_proposto": amost, "parede_proposta_s": 8 * 3600,
            "validacao": "guard_D.validate_job_D e pe_runner.validate_config (original, copia RO) aprovam TODOS os jobs",
            "indice_C2_por_tamanho": indice, "jobs_cegos": [n for n in jobs if n.startswith("D_")], "jobs": jobs}
    h_jobs = gravar("JOBS_D_V1.PROPOSTA.json", prop)
    print("JOBS_D_V1.PROPOSTA.json", h_jobs, "| jobs", len(jobs))
    print("pinos: eventos", len(pinos["eventos"]), "| semente", pinos["semente"]["compromisso_sha256"][:16])


if __name__ == "__main__":
    main()
