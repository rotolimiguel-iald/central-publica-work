# -*- coding: utf-8 -*-
"""guardas_e_bn_v402.py -- exame final v402 (examinador final unico, 27/10/2026; molde: guardas_e_bn_v401.py). Chama as FUNCOES do esboco R3.5 pinado (nada copiado), em processo, SEM gravar fora desta pasta:
 (1) ler_nos(Nos REAL v400, "v400") passa (a Bancada o pina) e ler_nos(Nos REAL, "v401") recusa; (2) ler_nos(<Nos de ensaio MEU: o candidato v401 + core do Nos +
 manifesto do kernel v401 SINTETIZADO do manifesto v400 (ff + a pedra + raiz/Audit novos; axiom_report + as 22 constantes do meu audit) + selo que pina os tres>, "v401")
 passa, com controles negativos; (3) a producao, so lida (foto antes/depois): pina B9-v400?; (4) conferir_recibo_pre_selo(f1011f5c..., producao de agora, selo e manifesto
 da v400 da custodia); (5) T17 emulado com KERNEL_RECIBO_v401 + CRITERIOS_v401 sobre o meu Nos de ensaio (passo simples v400 -> v401); variante com uma declaracao a menos.
uso: python -I -B -X utf8 guardas_e_bn_v402.py  [v402: Nos real v401; candidato v402; manifesto sintetizado com as 3 pedras e as 146 constantes do meu audit; producao B10-v401; pre_selo 36aaf247; T17 v402]"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, os, shutil, copy, time, importlib.util
from pathlib import Path
HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work")
V401 = os.path.join(WK, "cadeia_de_selo", "v402")   # (nome herdado do molde: aqui e o pacote v402)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PROD = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
ESB = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
sha = lambda b: hashlib.sha256(b).hexdigest()
shaf = lambda p: sha(open(p, "rb").read())
PINOS = json.load(open(os.path.join(V401, "PINOS_BN_v402.json"), encoding="utf-8"))
assert shaf(ESB) == PINOS["esboco_R3_5"]["sha256"] and PINOS["esboco_R3_5"]["sha256"].startswith("02b22ba5c6d35c71"), "esboco diverge do pino"
spec = importlib.util.spec_from_file_location("esboco_r35_exame_bn402", ESB); MOD = importlib.util.module_from_spec(spec); spec.loader.exec_module(MOD)
R = {"esboco": {"sha16": shaf(ESB)[:16], "revisao": MOD.REVISAO}}


def foto(raiz):
    out = {}
    for d, _, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(d, f)
            try:
                st = os.stat(p); out[os.path.relpath(p, raiz)] = (st.st_size, st.st_mtime_ns, shaf(p) if st.st_size < 8 * 2**20 else None)
            except OSError as e:
                out[os.path.relpath(p, raiz)] = ("erro", str(e))
    return out


t0 = time.time(); foto_antes = foto(PROD)
# (1) o Nos REAL (v400)
for v in ("v401", "v402"):
    try:
        info = MOD.ler_nos(Path(NOS), v); R["ler_nos_nos_real_" + v] = {"passou": True, "um_py16": info["um_py"]["sha256"][:16], "alpha": info["alpha"], "beta_rel_diff": info["core"]["beta_rel_diff"], "kernel16": (info["kernel"] or {}).get("sha256", "")[:16]}
    except MOD.Recusa as e:
        R["ler_nos_nos_real_" + v] = {"passou": False, "recusa": str(e)}
# (2) o meu Nos de ensaio com o candidato e o manifesto SINTETIZADO
CAND = PINOS["candidato"]["path"]; cand = open(CAND, "rb").read(); assert sha(cand) == PINOS["candidato"]["sha256"]
seloA_raw = open(os.path.join(NOS, "um_absoluto_selo.json"), "rb").read(); seloA = json.loads(seloA_raw)
coreA_raw = open(os.path.join(NOS, "um_absoluto.json"), "rb").read()
kmanA = json.loads(open(os.path.join(NOS, "tgl_kernel_proof_manifest.json"), "rb").read())
assert seloA["sha256"]["um_absoluto.json"] == sha(coreA_raw)
KR = json.load(open(PINOS["kernel_recibo"]["path"], encoding="utf-8"))
nomes_audit = [l.split("\t")[2] for l in open(os.path.join(HERE, "auditoria_v402.log"), encoding="utf-8") if l.startswith("V402_AX\t")]
assert len(nomes_audit) == 146, len(nomes_audit)
kmanB = copy.deepcopy(kmanA)
ff = kmanB["formal_files_sha256"]
for _p, _m in zip(KR["pedras"], ("TGLExt/PonteDaEscalaDual.lean", "TGLExt/QuedaSemGeometria.lean", "TGLExt/EsperancaCondicional.lean")):
    ff[_m] = _p["sha256"]
ff["TGLExt.lean"] = KR["raiz"]["sha256_depois"]; ff["TGL/Audit.lean"] = KR["audit"]["sha256_depois"]
for n in nomes_audit:
    kmanB["axiom_report"][n] = ["propext", "Classical.choice", "Quot.sound"]
kmanB_raw = json.dumps(kmanB, ensure_ascii=False, indent=1).encode("utf-8")
R["manifesto_sintetizado"] = {"n_ff": len(ff), "n_axiom_report": len(kmanB["axiom_report"]), "impressao_antes_v401": MOD.impressao_formal(kmanA["formal_files_sha256"])[:16], "impressao_depois": MOD.impressao_formal(ff)[:16],
                              "antes_igual_ao_do_recibo_do_kernel": MOD.impressao_formal(kmanA["formal_files_sha256"]) == KR["nos_kernel_impressao"]["antes"], "sha16": sha(kmanB_raw)[:16]}


def montar(nome, um_bytes, versao="v402", core_raw=coreA_raw, kman_raw=kmanB_raw, mexe_selo=None):
    d = os.path.join(HERE, "nos_ensaio", nome)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    open(os.path.join(d, "um.py"), "wb").write(um_bytes); open(os.path.join(d, "um_absoluto.json"), "wb").write(core_raw); open(os.path.join(d, "tgl_kernel_proof_manifest.json"), "wb").write(kman_raw)
    s = copy.deepcopy(seloA); s["um_version"] = versao; s["sha256"]["um.py"] = sha(um_bytes); s["sha256"]["um_absoluto.json"] = sha(core_raw); s["sha256"]["tgl_kernel_proof_manifest.json"] = sha(kman_raw)
    if mexe_selo:
        mexe_selo(s)
    open(os.path.join(d, "um_absoluto_selo.json"), "wb").write(json.dumps(s, ensure_ascii=False, indent=1).encode("utf-8"))
    return d


def ler(nome, um_bytes, versao="v402", **kw):
    d = montar(nome, um_bytes, versao, **kw)
    try:
        info = MOD.ler_nos(Path(d), versao)
        return {"passou": True, "alpha": info["alpha"], "um_version_linhas": info["um_version_linhas"], "UM_VERSION": info["UM_VERSION"], "beta_runtime": info["beta_runtime"], "beta_rel_diff": info["core"]["beta_rel_diff"],
                "kernel_manifesto_sha16": (info["kernel"] or {}).get("sha256", "")[:16], "n_formal_files": (info["kernel"] or {}).get("n_formal_files"), "um_py_sha16": info["um_py"]["sha256"][:16]}, info
    except MOD.Recusa as e:
        return {"passou": False, "recusa": str(e)}, None


R["ler_nos_candidato_v402"], NOS_INFO = ler("candidato", cand)
core_obj = json.loads(coreA_raw)
def core_com_beta(f):
    c = copy.deepcopy(core_obj); c["core"]["beta"] = c["core"]["beta"] * f; return json.dumps(c, ensure_ascii=False).encode("utf-8")
L5584 = b"ALPHA_FINE_CODATA_2018 = 7.2973525693e-3\r\n"; assert cand.count(L5584) == 1
neg = {
    "alfa_segunda_linha_coluna_0": (lambda: ler("n1", cand + b"\r\nALPHA_FINE_CODATA_2018 = 0.0072973525693\r\n")[0], "ALPHA_LINHA_NAO_UNICA"),
    "alfa_reatribuido_indentado": (lambda: ler("n2", cand + b"\r\nif True:\r\n    ALPHA_FINE_CODATA_2018 = 0.0072973525693\r\n")[0], "ALPHA_REATRIBUIDA_INDENTADA"),
    "um_version_segunda_linha": (lambda: ler("n4", cand + b'\r\nUM_VERSION = "v402"\r\n')[0], "UM_VERSION_LINHA_NAO_UNICA"),
    "beta_do_core_1e-10": (lambda: ler("n5", cand, core_raw=core_com_beta(1 + 1e-10))[0], "BETA_CORE_DIVERGE_DO_RUNTIME"),
    "selo_de_outra_versao": (lambda: ler("n6", cand, mexe_selo=lambda s: s.__setitem__("um_version", "v401"))[0], "SELO_VERSAO_DIFERENTE"),
    "alfa_fora_do_contrato": (lambda: ler("n7", cand.replace(L5584, b"ALPHA_FINE_CODATA_2018 = 1.5\r\n", 1))[0], "ALPHA_OUTSIDE_CONTRACT"),
    "manifesto_do_kernel_nao_pinado": (lambda: ler("n8", cand, mexe_selo=lambda s: s["sha256"].__setitem__("tgl_kernel_proof_manifest.json", "0" * 64))[0], "SELO_NAO_PINA_O_MANIFESTO_DO_KERNEL_DO_DISCO"),
}
R["ler_nos_controles_negativos"] = {}
for k, (f, cod) in neg.items():
    r = f(); R["ler_nos_controles_negativos"][k] = {"recusa": r.get("recusa"), "esperado": cod, "ok": (not r["passou"]) and str(r.get("recusa")).startswith(cod)}
# (3) a producao, so lida
can_mod, can_pin = MOD.carregar_canonical(Path(PROD)); ant = MOD.estado_anterior(Path(PROD), can_mod)
rps_p = PINOS["recibo_pre_selo"]["path"]; rps_raw = open(rps_p, "rb").read(); rps = json.loads(rps_raw)
R["producao"] = {"manifesto_sha16": ant["sha256"][:16], "deployment_id": ant["deployment_id"], "version": ant["version"], "um_py_pinado16": str(ant["um_py_pinado"])[:16], "seal_sha_pinado16": str(ant["seal_sha_pinado"])[:16],
                 "estado_do_contrato_instalado": ant["estado_do_contrato_instalado"], "kernel_manifesto_registrado16": str((ant["_man"].get("sincronizacao") or {}).get("kernel_manifesto_sha256"))[:16],
                 "igual_ao_que_o_recibo_pre_selo_registrou": ant["sha256"] == (rps.get("manifesto_anterior") or {}).get("sha256"), "recibo_pre_selo_sha16": sha(rps_raw)[:16], "pinos_bn": PINOS["recibo_pre_selo"]["sha256"][:16],
                 "recibo_veredito": rps.get("veredito"), "recibo_versao_alvo": rps.get("versao_alvo"), "recibo_um_py16": ((rps.get("nos") or {}).get("um_py") or {}).get("sha256", "")[:16]}
# (4) o recibo pre_selo conferido pelo esboco contra a producao de AGORA
SELO_ANT = PINOS["selo_anterior_v401"]["path"]; KMAN_ANT = PINOS["kernel_manifesto_anterior_v401"]["path"]
assert shaf(SELO_ANT) == PINOS["selo_anterior_v401"]["sha256"] and shaf(KMAN_ANT) == PINOS["kernel_manifesto_anterior_v401"]["sha256"]
R["selo_anterior_v401_e_o_do_nos"] = shaf(SELO_ANT) == sha(seloA_raw)
try:
    RPS_INFO = MOD.conferir_recibo_pre_selo(rps_p, ant, Path(PROD), False, PINOS["recibo_pre_selo"]["sha256"], SELO_ANT, KMAN_ANT, None)
    R["conferir_recibo_pre_selo"] = {"passou": True, "versao": RPS_INFO["versao"], "veredito": RPS_INFO["veredito"], "um_py16": RPS_INFO["um_py_sha256"][:16], "selo16": str(RPS_INFO["selo_sha256"])[:16],
                                     "kernel_anterior": {k: v[:16] for k, v in RPS_INFO["kernel_anterior"].items()}, "salto": RPS_INFO["salto"], "bateria": RPS_INFO["bateria"]}
except MOD.Recusa as e:
    RPS_INFO = None; R["conferir_recibo_pre_selo"] = {"passou": False, "recusa": str(e)}
negp = {}
for nome, args in (("selo_anterior_e_o_da_v400", (rps_p, ant, Path(PROD), False, PINOS["recibo_pre_selo"]["sha256"], os.path.join(V401, "..", "v401", "base_v400", "um_absoluto_selo.json"), KMAN_ANT, None)),
                   ("pino_do_recibo_errado", (rps_p, ant, Path(PROD), False, "0" * 64, SELO_ANT, KMAN_ANT, None)),
                   ("como_se_ja_sincronizada", (rps_p, ant, Path(PROD), True, PINOS["recibo_pre_selo"]["sha256"], SELO_ANT, KMAN_ANT, None))):
    try:
        MOD.conferir_recibo_pre_selo(*args); negp[nome] = {"recusou": False}
    except MOD.Recusa as e:
        negp[nome] = {"recusou": True, "recusa": str(e)[:200]}
R["conferir_recibo_pre_selo_controles"] = negp
# (5) o T17 emulado
KRP = PINOS["kernel_recibo"]["path"]; CRI = PINOS["criterios"]["path"]
crit = MOD.carregar_criterios(CRI, PINOS["criterios"]["sha256"], "v402")
ok17, det17, _ = MOD.verificar_kernel_recibo(KRP, "v402", NOS_INFO, PINOS["kernel_recibo"]["sha256"], RPS_INFO, False, crit)
R["t17_passo_simples"] = {"passou": ok17, "detalhe": det17[:900]}


def variante(nome, mexe_recibo=None, mexe_crit=None):
    k = copy.deepcopy(KR); (mexe_recibo or (lambda k: None))(k)
    p = os.path.join(HERE, "nos_ensaio", "KERNEL_RECIBO_" + nome + ".json"); open(p, "wb").write(json.dumps(k, ensure_ascii=False).encode("utf-8"))
    c = copy.deepcopy(crit); (mexe_crit or (lambda c: None))(c)
    ok, det, _ = MOD.verificar_kernel_recibo(p, "v402", NOS_INFO, None, None, True, c)
    return {"passou": ok, "detalhe": det[:300]}


R["t17_variante_declaracao_a_menos"] = variante("decl_menos", lambda k: k["pedras"][0]["declaracoes"].pop())
R["t17_variante_criterio_esperado_errado"] = variante("crit_errado", None, lambda c: c["esperados"].__setitem__("j1_teoremas", 105))
R["t17_variante_sem_a_pedra_no_recibo"] = variante("sem_pedra", lambda k: k.__setitem__("pedras", []))
R["t17_variante_uma_pedra_a_menos"] = variante("uma_pedra_a_menos", lambda k: k["pedras"].pop())
R["t17_controle_sandbox"] = variante("sandbox", None, None)
foto_depois = foto(PROD)
dif = sorted(k for k in set(foto_antes) | set(foto_depois) if foto_antes.get(k) != foto_depois.get(k))
R["producao_inalterada_por_este_exame"] = {"n_arquivos": len(foto_depois), "diferencas": dif[:20], "ok": not dif}
R["tempo_s"] = round(time.time() - t0, 1)
R["veredito"] = {"nos_real_v401_passa": R["ler_nos_nos_real_v401"]["passou"], "nos_real_como_v402_recusa": not R["ler_nos_nos_real_v402"]["passou"],
                 "candidato_passa_ler_nos": R["ler_nos_candidato_v402"]["passou"] and R["ler_nos_candidato_v402"]["alpha"]["n_linhas_nao_indentadas"] == 1 and R["ler_nos_candidato_v402"]["alpha"]["n_reatribuicoes_indentadas"] == 0,
                 "controles_ler_nos_todos_recusam": all(v["ok"] for v in R["ler_nos_controles_negativos"].values()),
                 "bancada_pina_B10_v401": R["producao"]["deployment_id"] == "B10-v401-20261025-R1" and R["producao"]["version"] == "v401",
                 "manifesto_igual_ao_do_recibo_pre_selo": R["producao"]["igual_ao_que_o_recibo_pre_selo_registrou"], "pre_selo_aceito_pelo_esboco": R["conferir_recibo_pre_selo"]["passou"],
                 "pre_selo_controles_recusam": all(v["recusou"] for v in negp.values()), "t17_passo_simples_passa": ok17,
                 "t17_variantes_recusam": not R["t17_variante_declaracao_a_menos"]["passou"] and not R["t17_variante_criterio_esperado_errado"]["passou"] and not R["t17_variante_sem_a_pedra_no_recibo"]["passou"] and not R["t17_variante_uma_pedra_a_menos"]["passou"],
                 "producao_inalterada": R["producao_inalterada_por_este_exame"]["ok"]}
json.dump(R, open(os.path.join(HERE, "GUARDAS_E_BN_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R["veredito"], ensure_ascii=False, indent=1))
for k in ("ler_nos_nos_real_v401", "ler_nos_nos_real_v402", "ler_nos_candidato_v402", "manifesto_sintetizado", "producao", "conferir_recibo_pre_selo", "conferir_recibo_pre_selo_controles", "t17_passo_simples", "t17_variante_declaracao_a_menos", "t17_variante_criterio_esperado_errado", "t17_variante_sem_a_pedra_no_recibo", "t17_variante_uma_pedra_a_menos", "t17_controle_sandbox", "producao_inalterada_por_este_exame", "tempo_s"):
    print(k + ":", json.dumps(R[k], ensure_ascii=False, default=str)[:700])
