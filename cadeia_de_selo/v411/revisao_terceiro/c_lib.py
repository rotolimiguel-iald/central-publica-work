import hashlib, json, os, sys, io
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
RT = os.path.join(V, "revisao_terceiro")
W = r"C:\t\k411c\revisao_C"
def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:16]
def rd(p, enc="utf-8"):
    with open(p, "rb") as f:
        return f.read().decode(enc)
def lines(p):
    return rd(p).split("\n")

ESTADO = RT + r"\ESTADO_REVISAO_v411.C.json"
def estado_load():
    if os.path.exists(ESTADO):
        return json.load(open(ESTADO, encoding="utf-8"))
    return {"escopo": "C", "revisor": "Sonnet 5.5 (agente de revisao de terceiro; nao construiu a v411)", "candidato_sha16_no_inicio": "21e87eb3df5098f8", "itens": {}, "achados": [], "conferencias": {}, "nao_verificado": []}
def estado_save(e):
    tmp = ESTADO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(e, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ESTADO)
def estado_item(item, feito, conf=None, achados=None, nao_verif=None):
    e = estado_load()
    e["itens"][item] = feito
    if conf: e["conferencias"][item] = conf
    for a in (achados or []):
        e["achados"] = [x for x in e["achados"] if x["id"] != a["id"]] + [a]
    for n in (nao_verif or []):
        if n not in e["nao_verificado"]: e["nao_verificado"].append(n)
    estado_save(e)
