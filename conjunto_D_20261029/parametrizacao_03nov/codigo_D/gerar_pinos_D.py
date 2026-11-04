# -*- coding: utf-8 -*-
"""gerar_pinos_D.py -- gera PINOS_D_V1.json (o que o guard_D confere): tudo LIDO DO DISCO por script, nada de memoria.
Conteudo: sha256 do V1 (JSON+MD); os 10 eventos sem hold com GPS do catalogo, SNR, delta_pred e chi_f/M_f,det pinados pelo V1; strain (caminho+bytes+sha256 do MANIFESTO
O4); sha256 do catalogo e do manifesto; constantes da Fase 6 (lidas do arquivo); beta = alpha*sqrt(e) em runtime; arvore de codigo (.py de codigo_D) e copias somente-leitura;
compromisso da semente; runtime do WSL (de runtime_wsl.json).  Regra do backup imediato: se o arquivo de destino existe, copia de BYTES .bak_<AAAAMMDD_HHMMSS> antes.
"""
import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import blinding_D as B  # noqa: E402
import guard_D as G  # noqa: E402
import v1_ramo_b as V  # noqa: E402


def montar(destino=None, criar_semente=False, runtime_json=None, sinteticos_manifesto=None):
    destino = Path(destino) if destino else G.PINOS
    v1, info = V.carregar_v1()
    k = V.constantes_um_py()
    cr = V.criterios_fase6()
    d10 = V.eventos_d10(v1)
    tab = V.tabela_eventos(v1)
    cat = V.catalogo_d(d10)
    sp = V.strain_pins(d10)
    sem = Path(V.native(B.SEMENTE_PADRAO))
    if not sem.exists():
        if not criar_semente:
            raise RuntimeError("semente ausente (use criar_semente=True UMA vez)")
        commit = B.criar_semente(B.SEMENTE_PADRAO)
    else:
        commit = B.compromisso(B.SEMENTE_PADRAO)
    eventos = {}
    for ev in d10:
        c, t = cat[ev], tab[ev]
        if abs(c["snr_rede"] - t["SNR_rede_GWOSC"]) > 1e-9:
            raise RuntimeError("SNR do catalogo difere do V1: " + ev)
        eventos[ev] = {"GPS": c["GPS"], "segment_start_real": math.floor(c["GPS"]) - G.DESLOC_JANELA_REAL_S, "snr_rede": c["snr_rede"],
                       "delta_pred_pinado": t["delta_pred_exato"], "chi_f_pinado": t["chi_f_mediana_GR"], "mf_det_pinado": t["Mf_det_mediana_GR"],
                       "catalogo": {"m1_src": c["m1_src"], "m2_src": c["m2_src"], "z": c["z"], "chi_eff": c["chi_eff"], "mf_src": c["mf_src"], "catalogo": c["catalogo"]},
                       "strain": {det: sp[(ev, det)] for det in ("H1", "L1")}}
    rt = None
    if runtime_json:
        rt0 = json.loads(Path(runtime_json).read_text())
        rt = {"python": rt0["python"], "pacotes": {a: b for a, b in rt0["pacotes"].items() if b}, "arquivo_sha256": V.sha256_file(str(runtime_json))}
    sint = {}
    if sinteticos_manifesto:
        man = json.loads(Path(sinteticos_manifesto).read_text(encoding="utf-8"))
        sint[man["nome"]] = {"GPS": man["GPS"], "snr_rede": man["snr_rede"], "segment_start_GPS": man["segment_start_GPS"], "injecao": man["injecao"],
                             "strain": man["strain"], "estatuto": man["estatuto"], "manifesto_sha256": V.sha256_file(str(sinteticos_manifesto))}
    pinos = {
        "schema": "PINOS_D_V1__guard_D", "sinteticos": sint, "gerado_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "v1": {"json_sha256": info["PREREGISTRO_RAMO_B_RINGDOWN_V1.json"], "md_sha256": info["PREREGISTRO_RAMO_B_RINGDOWN_V1.md"], "sha16_da_ordem": V.V1_SHA16_DA_ORDEM},
        "eventos_d10": d10, "eventos_holds_FORA": list(v1["spec"]["conjuntos"]["D"]["com_data_quality_hold"]),
        "eventos_pendentes_FORA": list(v1["spec"]["conjuntos"]["D"]["pendentes_AWAITING_GR_METADATA"]),
        "eventos": eventos, "catalogo_sha256": V.sha256_file(V.CATALOGO), "manifesto_strain_sha256": V.sha256_file(V.MANIFESTO_STRAIN),
        "fase6_criterios": {x: cr[x] for x in ("min_eventos", "z_excl", "poder_min", "sistematica_max_relativa")},
        "fase6_arquivo_sha256": V.sha256_file(V.FASE6_CR),
        "beta_runtime": k["beta"], "um_py_sha256_informativo": V.sha256_file(V.UM_PY),
        "um_py_nota": "o V1 pina o um.py v385; aqui so alpha/G/C/H sao lidos por regex e beta = alpha*sqrt(e) e conferido contra o valor do V1 a 1e-15",
        "semente": {"caminho": B.SEMENTE_PADRAO, "compromisso_sha256": commit, "offset_half_range": B.ESCALA, "etiqueta_hmac": B.ETIQUETA},
        "codigo": G.arvore_de_codigo(), "copias_somente_leitura": G.copias_ro(), "runtime_esperado": rt,
        "regras": {"janela_real": "segment_start = floor(GPS) - 12; 16 s", "janela_C2": "termina >= 64 s antes do GPS (desenho: 76 s)", "psd_duration_s": 256,
                   "prior_distancia_Mpc": [100.0, 10000.0], "prior_tempo_s": G.PRIOR_TEMPO_S, "so_dtau220_livre": True},
    }
    raw = (json.dumps(pinos, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    if destino.exists():
        shutil.copyfile(destino, destino.with_name(destino.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")))
    tmp = destino.with_name(destino.name + ".tmp")
    tmp.write_bytes(raw)
    if tmp.stat().st_size != len(raw):
        raise OSError("gravacao incompleta")
    tmp.replace(destino)
    return pinos, hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--criar-semente", action="store_true")
    ap.add_argument("--runtime-json")
    a = ap.parse_args()
    pinos, h = montar(criar_semente=a.criar_semente, runtime_json=a.runtime_json)
    print("PINOS_D_V1.json sha256", h, "| eventos", len(pinos["eventos"]), "| compromisso da semente", pinos["semente"]["compromisso_sha256"][:16])
