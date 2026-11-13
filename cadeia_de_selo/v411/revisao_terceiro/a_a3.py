"""A3: controles negativos PROPRIOS sobre o codigo EMBUTIDO no candidato (nao sobre o runtime_h0dn_v411.py solto)."""
import base64, copy, hashlib, io, json, os, re, sys, time, math
import a_lib
sys.stdout.reconfigure(encoding="utf-8")
t0 = time.time()
f = a_lib.Fonte(a_lib.CAND, "cand")
V = a_lib.V
core0 = json.load(open(os.path.join(V, "base_v410", "um_absoluto.json"), encoding="utf-8"))["core"]
ns = {"re": re, "os": os, "math": math, "json": json, "hashlib": hashlib, "__name__": "revA_cand", "__file__": a_lib.CAND}
ns["_m398"] = math
usar = ["_V411_H0DN_CONTRACT", "_V411_H0DN_TEXT", "_V411_H0DN_INSUMOS", "_V411_H0DN_RECUSA", "_v411_guarda_frases", "_v411_p18_sem_cabeca", "_v411_h0dn_decode", "_v411_h0dn_carregar_codigo", "_v411_h0dn_guarda_finitude",
        "_v411_h0dn_compara", "_v411_h0dn_json", "_v411_h0dn_secao", "v411_h0dn_mechanics", "h0dn_bg1_v411", "_V410_H0DN_INSUMOS", "_V410_H0DN_CONTRACT", "veredito_h0dn", "_v398_beta", "_v392_guarda_texto", "_v410_guarda_frases",
        "_v410_h0dn_vigia_arquivos", "SEALED_CODATA_ALPHA", "_v376_same_alpha_literal", "_v410_h0dn_cabeca"]
f.carregar(usar, ns)
CONTR, TXT, INS = ns["_V411_H0DN_CONTRACT"], ns["_V411_H0DN_TEXT"], ns["_V411_H0DN_INSUMOS"]
sha = lambda b: hashlib.sha256(b).hexdigest()


def blob(nome):
    ent = INS[nome]
    if "reuso_v410" in ent:
        ent = ns["_V410_H0DN_INSUMOS"][ent["reuso_v410"]]
    return base64.b64decode(ent["b64"].encode("ascii"))


def rodar(core_, contr_=None, txt_=None, ins_=None, trocar=None):
    salvo = {k: ns[k] for k in ("_V411_H0DN_CONTRACT", "_V411_H0DN_TEXT", "_V411_H0DN_INSUMOS")}
    salvo_v = ns["veredito_h0dn"]
    ns["_V411_H0DN_CONTRACT"] = contr_ or CONTR; ns["_V411_H0DN_TEXT"] = txt_ or TXT; ns["_V411_H0DN_INSUMOS"] = ins_ or INS
    if trocar:
        ns.update(trocar)
    try:
        for _ in range(80):
            c_try = copy.deepcopy(core_)
            o_ = f.chamar(ns, "h0dn_bg1_v411", c_try)
            m_ = re.search(r"NameError\(\"name '([A-Za-z_0-9]+)' is not defined", o_.get("error") or "")
            if m_ and m_.group(1) in f.idx:
                f.carregar([m_.group(1)], ns); continue
            return o_
        raise RuntimeError("dependencias demais")
    finally:
        ns.update(salvo); ns["veredito_h0dn"] = salvo_v


def trocar_blob(nome, novos, refrescar_pinos=True, refrescar_contrato=True):
    I = copy.deepcopy(INS); Cc = copy.deepcopy(CONTR)
    for k, v in list(I.items()):
        if "reuso_v410" in v:
            I[k] = {"b64": base64.b64encode(blob(k)).decode("ascii")}
    I[nome] = {"b64": base64.b64encode(novos).decode("ascii")}
    if refrescar_contrato:
        Cc["insumos"][nome].update(sha256=sha(novos), bytes=len(novos))
    if refrescar_pinos:
        N = Cc["nomes"]; pin = json.loads(blob(N["pinos"]).decode("utf-8"))
        campo = [c for c, n in Cc["pinos_por_campo"].items() if n == nome]
        if campo:
            pin[campo[0]]["sha256"] = sha(novos)
        elif nome in pin["codigo"]:
            pin["codigo"][nome] = sha(novos)
        pb = (json.dumps(pin, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
        I[N["pinos"]] = {"b64": base64.b64encode(pb).decode("ascii")}
        Cc["insumos"][N["pinos"]].update(sha256=sha(pb), bytes=len(pb))
    return Cc, I


def falhas(o):
    return [c["id"] for c in (o.get("mechanics") or {}).get("checks") or [] if not c["ok"]]


def resumo(o):
    v = o.get("verdict", "")
    return {"verdict": v[:110], "all_verified": o.get("all_verified"), "falhas": falhas(o), "erro": (o.get("error") or "")[:160],
            "recusou": (not o.get("all_verified")) and ("REFUSED" in v) and v.endswith("__GATE_UNMOVED") and "OPENED_ONCE" not in v}


def res_json(mod):
    R = json.loads(blob("RESULTADO_DA_ABERTURA_V411.json").decode("utf-8")); mod(R)
    return (json.dumps(R, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


rep = {}
pos = rodar(copy.deepcopy(core0))
rep["positivo"] = {"verdict": pos["verdict"][:400], "all_verified": pos["all_verified"], "n_ok": sum(1 for c in pos["mechanics"]["checks"] if c["ok"]), "n": len(pos["mechanics"]["checks"])}
print("POSITIVO", rep["positivo"], "| %.1fs" % (time.time() - t0)); sys.stdout.flush()


def reg(nome, o):
    rep[nome] = resumo(o); print(nome, rep[nome]); sys.stdout.flush()


b = blob("vetor_y255.npz")
I = copy.deepcopy(INS); I["vetor_y255.npz"] = {"b64": base64.b64encode(b[:-1] + bytes([b[-1] ^ 1])).decode("ascii")}
reg("N1_um_byte_no_vetor_sem_refazer_pinos", rodar(copy.deepcopy(core0), ins_=I))
Cc, I = trocar_blob("vetor_y255.npz", b[:-1] + bytes([b[-1] ^ 1]))
reg("N1b_um_byte_no_vetor_pinos_refeitos", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
rb = res_json(lambda R: R["resultado"]["estatistica"]["z_null"].__setitem__(0, R["resultado"]["estatistica"]["z_null"][0] + 1e-6))
Cc, I = trocar_blob("RESULTADO_DA_ABERTURA_V411.json", rb, refrescar_pinos=False)
reg("N2_resultado_z_null_mais_1e-6", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
rb = res_json(lambda R: R["resultado"]["estatistica"]["z_tgl"].__setitem__(0, R["resultado"]["estatistica"]["z_tgl"][0] + 1e-3))
Cc, I = trocar_blob("RESULTADO_DA_ABERTURA_V411.json", rb, refrescar_pinos=False)
reg("N2b_resultado_z_tgl_mais_1e-3", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
rb = res_json(lambda R: R["resultado"]["veredito"].__setitem__("ramo", 5))
Cc, I = trocar_blob("RESULTADO_DA_ABERTURA_V411.json", rb, refrescar_pinos=False)
reg("N4_ramo_trocado_no_resultado", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
rb = res_json(lambda R: R["resultado"]["veredito"].__setitem__("cabeca", R["resultado"]["veredito"]["cabeca"].replace("6", "7", 1)))
Cc, I = trocar_blob("RESULTADO_DA_ABERTURA_V411.json", rb, refrescar_pinos=False)
reg("N4b_cabeca_trocada_no_resultado", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
Cc = copy.deepcopy(CONTR); Cc["esperado_do_resultado"]["ramo_primario"] = 5
reg("N4c_ramo_primario_esperado_no_contrato_5", rodar(copy.deepcopy(core0), contr_=Cc))
import numpy as np
npz = np.load(io.BytesIO(b), allow_pickle=False); chave = json.loads(blob("PINOS_DE_PRODUCAO.json").decode("utf-8"))["vetor"]["chave"]
arr = {k: npz[k] for k in npz.files}
for nome, val in (("N3_vetor_com_NaN_pinos_refeitos", float("nan")), ("N3b_vetor_com_inf_pinos_refeitos", float("inf"))):
    y = np.array(arr[chave], dtype=float); y[0] = val
    a2 = dict(arr); a2[chave] = y
    buf = io.BytesIO(); np.savez(buf, **a2)
    Cc, I = trocar_blob("vetor_y255.npz", buf.getvalue())
    reg(nome, rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
json.dump(rep, open(os.path.join(a_lib.OUT, "a3_parte1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fim parte 1 | %.1fs" % (time.time() - t0))
