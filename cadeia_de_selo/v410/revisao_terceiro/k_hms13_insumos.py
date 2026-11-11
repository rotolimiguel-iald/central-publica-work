# -*- coding: utf-8 -*-
"""Revisor v410 R1 (ponto 1 do pedido): os insumos EMBUTIDOS do recibo HMS/13 e do H0DN (base64 no candidato): (a) sha256/bytes batem com os pinos do contrato E com as copias em insumos/ (hms13_*, h0dn_*);
(b) inventario independente dos numeros dos JSON do HMS/13 por NOME DE CHAVE (nenhuma chave de dado observado: mu, distmod, m_b, z, vetor, y_obs, photometric center...); listas numericas (comprimentos 255 e 64);
(c) o npz embutido do H0DN e' o estimador congelado (nao o y_obs): so' sha256 e nomes de arrays (np.load com allow_pickle=False, SEM imprimir valores); (d) nenhuma referencia a y_obs.npz / C_fisica nos insumos embutidos como caminho de leitura.
NAO abre kimi\\y_obs.npz nem kimi\\C_fisica_258x258.npz (so' sha256 se o pedido o permitir, nao feito aqui)."""
import base64, hashlib, io, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
lit = json.load(open(R + "revisao_terceiro/literais_v410.json", encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
res = {}
for reg, ins_nm, con_nm in (("hms13", "_V410_HMS13_INSUMOS", "_V410_HMS13_CONTRACT"), ("h0dn", "_V410_H0DN_INSUMOS", "_V410_H0DN_CONTRACT")):
    ins = lit[ins_nm]; con = lit[con_nm]
    print("=====", reg, "insumos embutidos:", list(ins))
    pinos = con["insumos"]
    for nome, ent in ins.items():
        b = base64.b64decode(ent["b64"].encode("ascii"), validate=True)
        pino = pinos.get(nome)
        # copia em insumos/
        import glob, os
        cand = [p for p in glob.glob(R + "insumos/*") if os.path.basename(p) in (nome, "hms13_" + nome, "h0dn_" + nome)]
        cp = sha(open(cand[0], "rb").read()) if cand else None
        print("  %-48s bytes %7d sha16 %s | pino ok: %s | copia insumos/ %s: %s" % (nome, len(b), sha(b)[:16], pino and sha(b) == pino["sha256"] and len(b) == pino["bytes"], os.path.basename(cand[0]) if cand else None, cp == sha(b) if cp else None))
        res[(reg, nome)] = b
# (b) inventario numerico dos JSON do HMS/13
rx_perm = ("byte", "count", "line", "char", "n_", "_n", "num", "error", "err", "sigma", "component", "version", "page", "size", "total", "length")
chaves_num = {}
listas = []


def walk(o, cam, fonte):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, cam + "/" + str(k), fonte)
    elif isinstance(o, list):
        if o and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in o): listas.append((fonte, cam, len(o)))
        for i, v in enumerate(o): walk(v, cam + "[%d]" % i, fonte)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        k = cam.rsplit("/", 1)[-1]
        chaves_num.setdefault((fonte, re.sub(r"\[\d+\]", "[]", k)), 0)
        chaves_num[(fonte, re.sub(r"\[\d+\]", "[]", k))] += 1


for nome in ("MAPA_FONTES_E_COVARIANCIA_13.json", "MANIFEST_FONTES_PRIMARIAS.json", "VALIDACAO_FONTES_13.json"):
    walk(json.loads(res[("hms13", nome)].decode("utf-8")), "", nome[:12])
print("\nchaves com numero (fonte, chave): contagem")
for (f, k), n in sorted(chaves_num.items()): print("   ", f, k, n)
print("listas numericas:", listas)
SUSPEITAS = re.compile(r"(?i)(^|_)(mu|distmod|m_?b|zhd|zcmb|vetor|vector|y_?obs|photometr|centro|center|residual|h0|hubble_ratio|Z_)(_|$)")
sus = [(f, k) for (f, k) in chaves_num if SUSPEITAS.search(k)]
print("chaves numericas suspeitas (nomes de dado observado):", sus)
# texto do levantamento: linhas com muitos numeros
lev = res[("hms13", "LEVANTAMENTO_FONTES_PRIMARIAS_13.md")].decode("utf-8")
print("levantamento: linhas", lev.count("\n") + 1, "| linhas com >= 8 numeros:", sum(1 for l in lev.splitlines() if len(re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])", l)) >= 8))
# (d) referencias a y_obs / C_fisica nos embutidos
for (reg, nome), b in res.items():
    t = b.decode("utf-8", "replace") if not nome.endswith(".npz") else ""
    refs = re.findall(r"(?i)y_obs\.npz|C_fisica_258x258|kimi[\\/]", t)
    if refs: print("  referencias a nomes vedados em", reg, nome, ":", sorted(set(refs)))
# (c) o npz do H0DN: so' nomes e shapes
try:
    import numpy as np
    b = res[("h0dn", "h0dn_estimator_frozen.npz")] if ("h0dn", "h0dn_estimator_frozen.npz") in res else None
    k = [n for (r, n) in res if r == "h0dn" and n.endswith(".npz")]
    print("npz embutidos do H0DN:", k)
    for n in k:
        z = np.load(io.BytesIO(res[("h0dn", n)]), allow_pickle=False)
        print("  ", n, {a: tuple(z[a].shape) for a in z.files})
except Exception as e:
    print("npz:", repr(e)[:200])
