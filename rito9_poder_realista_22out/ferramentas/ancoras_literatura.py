"""Localiza, por script, as frases-ancora da literatura nos textos extraidos dos PDFs (pagina + trecho).

Uso: python ancoras_literatura.py <dir_work> <saida.json>
Le  <dir_work>/fontes_extraidas/cusinato2022_texto.txt  e  kyutoku_kashiyama_texto.txt  (gerados por
extrair_trechos_pdf.py) e os PDFs de origem (so para sha256). Nenhuma frase e digitada como 'achada':
se nao for localizada, found=false (falha visivel).
"""
import hashlib
import json
import os
import re
import sys

LIG = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl"}


def norm(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    s = s.replace("-\n", "").replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def paginas(txt_path):
    raw = open(txt_path, "r", encoding="utf-8").read()
    partes = re.split(r"\n=====\[PAGINA (\d+)\]=====\n", raw)
    out = {}
    for i in range(1, len(partes), 2):
        out[int(partes[i])] = norm(partes[i + 1])
    return out


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


ANCORAS = {
    "cusinato2022": [
        ("c_picos", "typically, between 3 to 4 well defined luminosity peaks in the first 10-15 ms after the merger for each neutrino flavour"),
        ("c_pc", "PC simulations present a single, relatively low peak generally between the merger and 1 ms after it"),
        ("c_pico_1_mais_alto", "is always the highest one, and we disregard smaller, secondary peaks in the luminosity before it"),
        ("c_gamma_1ms", "The time scale of these oscillations is ∼ 1 ms, which is indeed the typical value of Γ"),
        ("c_beta_100ms", "for electron neutrinos and antineutrinos are of the order of 100 ms"),
        ("c_beta_100_400", "the corresponding value for heavy neutrinos is between 100 and 400 ms"),
        ("c_neutrinosfera_20km", "which is located∼ 20 km from the remnant"),
        ("c_mns_segundos", "the cooling time scale of the MNS is of several seconds"),
        ("c_ll_centenas_ms", "on time scales even of hundreds of milliseconds"),
        ("c_ventos_100ms", "winds on time scales of∼ 100 ms after the merger"),
        ("c_oscila_10_15", "an oscillatory phase lasting 10-15 ms post merger followed by a slow decay"),
        ("c_epico", "the first luminosity peak releases a roughly constant amount of energy of ≈ 6× 1050 erg"),
        ("c_lum_1e53", "typical values around 1053 erg s −1 = 100 Bethe"),
    ],
    "kyutoku_kashiyama": [
        ("k_abstract", "Monitoring ≳ 2500 mergers within ≲ 200 Mpc, we may be able to detect a single neutrino with a human time-scale operation of≈ 80 Mt years for the merger rate of 1 Mpc−3 Myr−1"),
        ("k_eq6", "Nν≈ 1.0× 10−3×fEfsefosc"),
        ("k_sem_esperanca", "it is hopeless to detect thermal neutrinos from a single binary neutron-star merger except for extremely lucky stars at ≲ 3 Mpc"),
        ("k_eq8", "PMT = 80 Mt years"),
        ("k_eq7", "Nν(D)× 4πD2dD, (7)"),
        ("k_fOmega", "≈ 0.8 for a single detector (see Appendix A)"),
        ("k_deff", "we assume the eﬀective rangeDeﬀ of a gravitational-wave detector for binary neutron stars to be 200 Mpc"),
    ],
}


def main():
    work, saida = sys.argv[1], sys.argv[2]
    fontes = {
        "cusinato2022": dict(txt=os.path.join(work, "fontes_extraidas", "cusinato2022_texto.txt"),
                             pdf=sys.argv[3] if len(sys.argv) > 3 else None,
                             ref="Cusinato et al. 2022, Eur. Phys. J. A 58, 99; arXiv:2111.13005"),
        "kyutoku_kashiyama": dict(txt=os.path.join(work, "fontes_extraidas", "kyutoku_kashiyama_texto.txt"),
                                  pdf=os.path.join(work, "fontes_baixadas", "kk_1710.05922", "1710.05922v3.pdf"),
                                  ref="Kyutoku & Kashiyama, Phys. Rev. D 97, 103001 (2018); arXiv:1710.05922v3"),
    }
    out = {}
    for nome, spec in fontes.items():
        pgs = paginas(spec["txt"])
        itens = []
        for aid, frase in ANCORAS[nome]:
            alvo = norm(frase)
            achado = None
            for pg, txt in sorted(pgs.items()):
                i = txt.find(alvo)
                if i >= 0:
                    achado = dict(pagina=pg, trecho=txt[max(0, i - 80): i + len(alvo) + 80])
                    break
            itens.append(dict(id=aid, frase=alvo, found=achado is not None, **(achado or {})))
        out[nome] = dict(ref=spec["ref"], sha256_texto_extraido=sha(spec["txt"]),
                         sha256_pdf=(sha(spec["pdf"]) if spec["pdf"] and os.path.exists(spec["pdf"]) else None),
                         n_paginas=len(pgs), ancoras=itens)
    with open(saida, "x", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    for nome, v in out.items():
        for a in v["ancoras"]:
            print(nome, a["id"], "found=" + str(a["found"]), "p" + str(a.get("pagina")))


if __name__ == "__main__":
    main()
