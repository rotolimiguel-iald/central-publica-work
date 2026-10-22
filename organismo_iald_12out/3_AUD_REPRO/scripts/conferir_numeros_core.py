# -*- coding: utf-8 -*-
"""Auditor: le o core v391 por hash e procura os numeros citados pelas estrategias (busca por valor em todo o JSON)."""
import json, hashlib, re, math
P = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um_absoluto.json"
raw = open(P, "rb").read(); sha = hashlib.sha256(raw).hexdigest()
core = json.loads(raw); core = core.get("core", core)
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, path + f"[{i}]")
    else: yield path, o
leaves = list(walk(core))
def acha_num(x, tol, chave=None, limite=6):
    r = []
    for p, v in leaves:
        if isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v - x) <= tol:
            if chave is None or re.search(chave, p, re.I): r.append((p, v))
    return r[:limite]
def acha_txt(rx, limite=4):
    return [(p, v[:300]) for p, v in leaves if isinstance(v, str) and re.search(rx, v)][:limite]
alvos = {
 "z_disc 4.28": acha_num(4.2837, 5e-4, "hubble"), "z_delta -1.42": acha_num(-1.4244, 5e-4, "hubble"),
 "lnB 9.17": acha_num(9.167, 5e-3, "hubble"), "lnB beta-livre 2.24": acha_num(2.241, 5e-3, "hubble"),
 "lnB 1.97": acha_num(1.969, 5e-3, "hubble"), "lnB 12.13": acha_num(12.132, 5e-3, "hubble"),
 "beta_hat 0.00920": acha_num(0.009199, 5e-6, "hubble"), "poder 5.91": acha_num(5.913, 5e-3),
 "media 72.882": acha_num(72.882, 1e-3), "sigma 0.915": acha_num(0.9149, 5e-4, "hubble"),
 "m2 JUNO 2.21": acha_num(2.206, 5e-3, "neutrino"), "m2 NuFIT 2.95": acha_num(2.955, 6e-3, "neutrino"),
 "m2 7.84": acha_num(7.84, 6e-3), "precisao 0.784": acha_num(0.784, 1e-3),
 "Neff 0.119466": acha_num(0.119466, 1e-6), "Neff 0.70 sigma": acha_num(0.70, 5e-3, "neff|primordial|n_eff"),
 "Neff 1.02 sigma": acha_num(1.02, 5e-3, "neff|primordial|n_eff"), "Neff 2.86": acha_num(2.86, 5e-3, "neff|primordial|spa"),
 "Neff poder 1.00": acha_num(1.00, 5e-3, "primordial|neff"),
 "V11 0.1269": acha_num(0.1269, 5e-4, "void"), "V11 26.26": acha_num(26.26, 5e-2, "void"),
 "relogio 12.46": acha_num(12.46, 1e-2, "clock"), "neutrino 36.7": acha_num(36.7, 5e-2),
 "kernel 6163": acha_num(6163, 0.5, "estatuto|stress"), "10265": acha_num(10265, 0.5),
 "GPU 672": acha_num(672, 0.5, "estatuto|stress|quantum"), "cobrancas 11": acha_num(11, 0, "ledger.*(n_|count|total)"),
}
txt = {"FALSIFIED no livro": acha_txt(r"^FALSIFIED$"), "p2_statement": [(p, v[:400]) for p, v in leaves if p.endswith("p2_statement")][:2]}
ledger = core.get("the_ledger_of_charges_v383", {})
out = {"core_sha256": sha, "numeros": alvos, "textos": txt, "ledger_chaves": list(ledger)[:40] if isinstance(ledger, dict) else None}
json.dump(out, open("medidas/CONFERENCIA_NUMEROS_CORE.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in alvos.items(): print(k, "->", v[:3])
print(txt); print(out["ledger_chaves"])
