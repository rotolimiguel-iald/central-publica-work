# -*- coding: utf-8 -*-
"""v1_ramo_b.py -- leitor do PRE-REGISTRO V1 do ramo B (ringdown), pinado por hash, mais as constantes e funcoes
que o V1 fixa. Nada aqui le dado de deformacao: so metadados (SNR, M_f,det, chi_f, k, N, delta_pred) que o V1 ja
carrega como "informacao cega", as constantes da Fase 6 e as formulas de Kerr/BCW copiadas VERBATIM de
poder_cego_ramo_b_v2.py (l.45-70 do original; o teste confere contra a tabela do V1).
Estatuto: codigo [REAL]; a hipotese do V1 e [ONTO]/[CONJECTURE] como o V1 diz.  Hash e beta SEMPRE lidos do disco/runtime.
"""
import ast
import hashlib
import json
import math
import os
import re

BS = chr(92)


def native(path):
    """C:/... -> /mnt/c/... quando roda no WSL (posix); inalterado no Windows."""
    p = path.replace(BS, "/")
    if os.name == "posix" and len(p) > 2 and p[1] == ":":
        return "/mnt/" + p[0].lower() + p[2:]
    if os.name == "nt" and p.startswith("/mnt/") and len(p) > 6 and p[6] == "/":
        return p[5].upper() + ":" + p[6:]
    return p


V1_DIR = "C:/IALD/Bancada_Um/investigacao/preregistro_ramo_b_05out"
V1_JSON = V1_DIR + "/PREREGISTRO_RAMO_B_RINGDOWN_V1.json"
V1_MD = V1_DIR + "/PREREGISTRO_RAMO_B_RINGDOWN_V1.md"
V1_HASHES = V1_DIR + "/V1_RAMO_B_HASHES.json"
# prefixo dado pela ORDEM do operador de 03/11/2026 (conferencia cruzada; o hash inteiro vem do disco)
V1_SHA16_DA_ORDEM = "86f98fcc124dd9ca"
FASE6_CR = "C:/IALD/Bancada_Um/investigacao/fase6_eco_radical_01out/preregistro_fase6.py"
UM_PY = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um.py"
CATALOGO = "C:/IALD/Bancada_Um/investigacao/fase6_eco_radical_01out/catalogo_v3.csv"
MANIFESTO_STRAIN = "C:/IALD/Bancada_Um/fontes_externas/gwosc_o4/GWOSC_O4_32S_V1.manifest.json"
STRAIN_RAIZ = "C:/IALD/Bancada_Um/fontes_externas/gwosc_o4"
MSUN = 1.98892e30  # o mesmo valor do poder_cego_ramo_b_v2.py (so para o controle C1)


class V1Error(RuntimeError):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(native(path), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def strict_json(raw):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                raise V1Error("chave JSON duplicada: " + k)
            d[k] = v
        return d

    def bad(v):
        raise V1Error("constante nao finita no JSON: " + v)

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def carregar_v1():
    """Le o V1 por hash (fail-closed). Devolve (v1_dict, info)."""
    hashes = strict_json(open(native(V1_HASHES), "rb").read())["arquivos"]
    info = {}
    for nome, caminho in (("PREREGISTRO_RAMO_B_RINGDOWN_V1.json", V1_JSON), ("PREREGISTRO_RAMO_B_RINGDOWN_V1.md", V1_MD)):
        esperado = hashes[nome]["sha256"]
        real = sha256_file(caminho)
        if real != esperado:
            raise V1Error("V1 difere do registro de hashes: " + nome)
        info[nome] = real
    if not info["PREREGISTRO_RAMO_B_RINGDOWN_V1.json"].startswith(V1_SHA16_DA_ORDEM):
        raise V1Error("V1 JSON nao confere com o sha16 da ordem do operador")
    v1 = strict_json(open(native(V1_JSON), "rb").read())
    return v1, info


def constantes_um_py():
    """alpha, G, C, H lidos do um.py por regex (nunca digitados). beta = alpha*sqrt(e) em runtime."""
    src = open(native(UM_PY), encoding="utf-8", errors="replace").read(2000000)

    def grab(nome):
        m = re.search(r"^" + nome + r"\s*=\s*([0-9.eE+-]+)", src, re.M)
        if not m:
            raise V1Error("constante ausente no um.py: " + nome)
        return float(m.group(1))

    alpha, G, C, H = (grab(n) for n in ("SEALED_CODATA_ALPHA", "G_NEWTON", "C_LIGHT", "H_PLANCK_EXACT"))
    hbar = H / (2 * math.pi)
    return dict(alpha=alpha, G=G, C=C, H=H, hbar=hbar, beta=alpha * math.sqrt(math.e),
                t_planck=math.sqrt(hbar * G / C ** 5), m_planck=math.sqrt(hbar * C / G))


def criterios_fase6():
    """min_eventos, z_excl, poder_min, sistematica_max_relativa: lidos de preregistro_fase6.py por AST."""
    src = open(native(FASE6_CR), encoding="utf-8").read()
    m = re.search(r'"criterios":\s*dict\((.*?)\),\s*\n', src)
    if not m:
        raise V1Error("criterios da Fase 6 nao encontrados")
    call = ast.parse("dict(" + m.group(1) + ")", mode="eval").body
    cr = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
    for k in ("min_eventos", "z_excl", "poder_min", "sistematica_max_relativa"):
        if k not in cr:
            raise V1Error("criterio ausente: " + k)
    return cr


# --- Berti-Cardoso-Will 2006, l=m=2, n=0 [KNOWN]; COPIA VERBATIM de poder_cego_ramo_b_v2.py (os mesmos do um.py:155704)
def bcw220(a):
    mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292
    q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990)
    return mw, q


def kerr_kappa_hat(a):  # kappa em unidades de 1/M: sqrt(1-a^2) / (2 (1 + sqrt(1-a^2)))
    s = math.sqrt(1 - a * a)
    return s / (2 * (1 + s))


def k_kms(a):  # 2pi/kappa em unidades de GM/c^3 = 4 pi (1+s)/s
    return 2 * math.pi / kerr_kappa_hat(a)


def N_plain(a):
    mw, q = bcw220(a)
    return mw * q


def previsao_por_spin(a, beta):
    """delta_pred exato = -x/(1+x), x = beta*k*N  (M_X = M_f: M cancela). Devolve (delta, x, k, N)."""
    k = k_kms(a)
    N = N_plain(a)
    x = beta * k * N
    return -x / (1 + x), x, k, N


def tabela_eventos(v1):
    """A tabela 'informacao cega' do V1 por evento (SNR, M_f,det, chi_f, delta_pred): nenhum valor de deformacao."""
    rows = {r["evento"]: r for r in v1["spec"]["conjuntos"]["D"]["previsao_da_hipotese_por_evento_INFORMACAO_CEGA"]}
    return rows


def eventos_d10(v1):
    d = v1["spec"]["conjuntos"]["D"]
    ev = list(d["elegiveis_sem_hold"])
    if len(ev) != 10 or set(ev) & set(d["com_data_quality_hold"]):
        raise V1Error("D10 do V1 nao tem 10 eventos sem hold")
    return ev


def sigma_sys_familia(v1):
    f = v1["spec"]["sistematica"]["sigma_sys_familia_DECLARADO"]
    return [float(x) for x in f]


def catalogo_d(eventos):
    """GPS, massas de fonte, z, chi_eff, SNR do catalogo residente (metadados publicos GR; pinado no manifesto do strain)."""
    import csv
    man = strict_json(open(native(MANIFESTO_STRAIN), "rb").read())
    if man["catalog"]["sha256"] != sha256_file(CATALOGO):
        raise V1Error("catalogo difere do pino do manifesto")
    out = {}
    with open(native(CATALOGO), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["commonName"] in eventos:
                out[r["commonName"]] = dict(
                    GPS=float(r["GPS"]), m1_src=float(r["mass_1_source"]), m2_src=float(r["mass_2_source"]),
                    snr_rede=float(r["network_matched_filter_snr"]), chi_eff=float(r["chi_eff"]),
                    mf_src=float(r["final_mass_source"]), z=float(r["redshift"]), catalogo=r["catalog.shortName"])
    miss = set(eventos) - set(out)
    if miss:
        raise V1Error("eventos ausentes no catalogo: " + ",".join(sorted(miss)))
    return out


def strain_pins(eventos):
    """sha256/tamanho do HDF5 de cada (evento, detector) lidos do MANIFESTO (nao do disco); o guarda confere o disco."""
    man = strict_json(open(native(MANIFESTO_STRAIN), "rb").read())
    out = {}
    for s in man["series"]:
        if s["event"] in eventos and s.get("status") == "OK":
            out[(s["event"], s["det"])] = dict(hdf5=s["hdf5"], hdf5_bytes=s["hdf5_bytes"], hdf5_sha256=s["hdf5_sha256"])
    for e in eventos:
        for d in ("H1", "L1"):
            if (e, d) not in out:
                raise V1Error("strain ausente no manifesto: %s %s" % (e, d))
    return out
