# -*- coding: utf-8 -*-
"""v411 (gerencia c1, 11/11/2026) -- o que os AGREGADOS PUBLICOS deixam prever, sem abrir vetor nenhum.
Entradas: o numero local que a colaboracao publica (README do codigo dela), o centro e o desvio do fundo congelado (BG1),
a lei K congelada e matrizes de DESENHO (rede, pesos congelados de 255 linhas, pesos do desenho de 242 linhas e das
ancoras unicas). NAO e' o resultado do rito: e' a conta que qualquer leitor faz com numeros publicos, mais o quanto cada
linha do teste pode se afastar da estimativa publicada, pelo modelo publicado. Grava artefatos/ESPERADO_PELOS_AGREGADOS.json."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "artefatos"
B = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
README = B / "network" / "upstream" / "h0_constrainer" / "README.md"
BG1 = B / "background" / "BG1.json"
REDE = B / "network" / "network.npz"
CONGELADO = B / "estimator_frozen.npz"
S0 = OUT / "estimador_s0_v411.npz"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    m = re.search(r"H0=([0-9.]+)\+/-([0-9.]+) km/s/Mpc \| Chi-squared=([0-9.]+) \| ndof=([0-9]+)", README.read_text(encoding="utf-8"))
    assert m, "linha de base nao achada no README"
    H0_pub, sig_pub = float(m.group(1)), float(m.group(2))
    bg = json.loads(BG1.read_text(encoding="utf-8"))
    H0_bg, logK, sig_bg = float(bg["H0"]), float(bg["logK"]), float(bg["sigma_H0"])
    with np.load(REDE, allow_pickle=False) as n:
        C = n["C"].copy()
    with np.load(CONGELADO, allow_pickle=False) as e:
        W255, sd255, sdt255 = e["weights"].copy(), e["sd_null"].copy(), e["sd_tgl"].copy()
    with np.load(S0, allow_pickle=False) as s:
        keep, W0, sd0, sdt0 = s["keep"].copy(), s["weights"].copy(), s["sd_null"].copy(), s["sd_tgl"].copy()
        anc = {str(a): (s["keep_" + str(a)].copy(), s["weights_" + str(a)].copy(), s["sd_null_" + str(a)].copy(),
                        s["sd_tgl_" + str(a)].copy()) for a in s["anchor_names"]}
    t_pub = float(np.log10(H0_pub) - np.log10(H0_bg))   # so' agregados publicos

    def pad(w, k):
        v = np.zeros(C.shape[0])
        v[k] = w
        return v

    w_ref = W255[0]   # a estimativa publicada e' w_ref . y
    out = {"o_que_e": "esperado pelos agregados publicos; NAO e' resultado do rito; nenhum vetor observado lido",
           "entradas": {"H0_publicado": H0_pub, "desvio_publicado": sig_pub, "H0_fundo": H0_bg, "desvio_fundo": sig_bg,
                        "logK": logK, "previsao_K_para_o_local": H0_bg * 10 ** logK},
           "pinos_das_entradas": {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in (README, BG1, REDE, CONGELADO, S0)},
           "t_dos_agregados": t_pub,
           "conta_linear": {"z_nulo": (H0_pub - H0_bg) / float(np.hypot(sig_pub, sig_bg)),
                            "z_K": (H0_pub - H0_bg * 10 ** logK) / float(np.hypot(sig_pub, sig_bg))},
           "rede_completa_255": {"z_nulo": t_pub / float(sd255[0]), "z_K": (t_pub - logK) / float(sdt255[0])},
           "linhas": {}}

    def linha(nome, w, sd_n, sd_t):
        d = w - w_ref
        sdd = float(np.sqrt(max(float(d @ C @ d), 0.0)))   # desvio de (estimativa da linha - estimativa publicada), pelo modelo publicado
        zc, zk, s = t_pub / sd_n, (t_pub - logK) / sd_t, sdd / sd_n
        out["linhas"][nome] = {"desvio_da_diferenca_para_a_publicada_em_desvios_da_linha": s, "z_nulo_esperado": zc,
                               "z_K_esperado": zk,
                               "prob_z_nulo_ge_5_dado_o_publicado": float(norm.sf((5 - zc) / s)) if s > 0 else float(zc >= 5),
                               "sd_null": sd_n, "D": logK / sd_n}

    linha("primario_publicado_13_fora", pad(W0[0], keep), float(sd0[0]), float(sdt0[0]))
    linha("cefeidas_livres_13_fora", pad(W0[1], keep), float(sd0[1]), float(sdt0[1]))
    for a, (k, w, sn, st) in anc.items():
        linha("ancora_unica_" + a + "_publicado", pad(w[0], k), float(sn[0]), float(st[0]))
    OUT.mkdir(exist_ok=True)
    dest = OUT / "ESPERADO_PELOS_AGREGADOS.json"
    raw = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(raw)
    assert tmp.stat().st_size == len(raw)
    tmp.replace(dest)
    print(json.dumps({k: (v if k != "linhas" else {n: {"z_nulo_esperado": x["z_nulo_esperado"], "prob": x["prob_z_nulo_ge_5_dado_o_publicado"]} for n, x in v.items()}) for k, v in out.items() if k != "pinos_das_entradas"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
