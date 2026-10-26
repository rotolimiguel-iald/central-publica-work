# -*- coding: utf-8 -*-
"""guardas_e_bn_v400.py -- exame final v400 (c1, modelo forte, 24/10/2026). Chama as FUNCOES do esboco R3.5 pinado (nada copiado, nada reimplementado),
em processo e SEM gravar em lugar nenhum fora desta pasta:
 (1) ler_nos(Nos REAL v399, "v399") -- so le -- tem de recusar com a MESMA mensagem do recibo da Bancada;
 (2) ler_nos(<Nos de ensaio MEU com o candidato>, "v400") -- passa; o Nos de ensaio tem o candidato, o core e o manifesto do kernel da v399 (copias de bytes;
     o kernel da v400 e' o da v399 byte a byte) e um selo = o da v399 com um_version "v400" e o pino do candidato; + controles negativos meus;
 (3) a producao (so leitura; foto da arvore antes e depois): carregar_canonical + estado_anterior -- a Bancada ainda pina B8-v398?; o manifesto e' o mesmo
     que o recibo pre_selo registrou?;
 (4) conferir_recibo_pre_selo(o recibo reaproveitado 0b12bdb6..., a producao de agora, ja_sincronizada=False, selo e manifesto do kernel da v398 da custodia);
 (5) o T17 emulado: verificar_kernel_recibo(KERNEL_RECIBO_v400, "v400", nos_info do meu Nos de ensaio, pino, o recibo pre_selo conferido, sandbox=False,
     CRITERIOS_v400 pinado) -- o passo simples v398 -> v400; e a variante do salto (o ANTES = o kernel da v399) recusada;
 (6) a cadeia de selos tentada pela preparacao (v398 -> v399) recusada no elo v399.
uso: python -I -B -X utf8 guardas_e_bn_v400.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, os, shutil, copy, time, importlib.util
from pathlib import Path
HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work")
V400 = os.path.join(WK, "cadeia_de_selo", "v400"); V399 = os.path.join(WK, "cadeia_de_selo", "v399")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PROD = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
ESB = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
sha = lambda b: hashlib.sha256(b).hexdigest()
shaf = lambda p: sha(open(p, "rb").read())
PINOS = json.load(open(os.path.join(V400, "PINOS_BN_v400.json"), encoding="utf-8"))
assert shaf(ESB) == PINOS["esboco_R3_5"]["sha256"] and PINOS["esboco_R3_5"]["sha256"].startswith("02b22ba5c6d35c71"), "esboco diverge do pino"
spec = importlib.util.spec_from_file_location("esboco_r35_exame_bn", ESB); MOD = importlib.util.module_from_spec(spec); spec.loader.exec_module(MOD)
R = {"esboco": {"sha16": shaf(ESB)[:16], "revisao": MOD.REVISAO}}


def foto(raiz):
    """a arvore da producao: caminho relativo -> (bytes, mtime_ns, sha256 se < 8 MB)."""
    out = {}
    for d, _, fs in os.walk(raiz):
        if "__pycache__" in d.split(os.sep):
            pass
        for f in fs:
            p = os.path.join(d, f)
            try:
                st = os.stat(p)
                out[os.path.relpath(p, raiz)] = (st.st_size, st.st_mtime_ns, shaf(p) if st.st_size < 8 * 2**20 else None)
            except OSError as e:
                out[os.path.relpath(p, raiz)] = ("erro", str(e))
    return out


t0 = time.time()
foto_antes = foto(PROD)
# ------------------------------------------------------------------ (1) o Nos REAL (v399), so lido
rec_v399 = json.load(open(os.path.join(V399, "bancada_B3_ensaio_20261024_162108", "RECUSA_SINCRONIZACAO_v399_20261024_162108.json"), encoding="utf-8"))
try:
    MOD.ler_nos(Path(NOS), "v399"); R["ler_nos_nos_real_v399"] = {"passou": True}
except MOD.Recusa as e:
    R["ler_nos_nos_real_v399"] = {"passou": False, "recusa": str(e), "recusa_do_recibo_da_bancada": rec_v399.get("recusa"), "identica": str(e) == rec_v399.get("recusa"),
                                  "recibo": {"veredito": rec_v399.get("veredito"), "manifesto_anterior_sha16": ((rec_v399.get("manifesto_anterior") or {}).get("sha256") or "")[:16]}}
# ------------------------------------------------------------------ (2) o meu Nos de ensaio com o candidato
CAND = PINOS["candidato"]["path"]; cand = open(CAND, "rb").read(); assert sha(cand) == PINOS["candidato"]["sha256"]
selo399_raw = open(os.path.join(NOS, "um_absoluto_selo.json"), "rb").read(); selo399 = json.loads(selo399_raw)
core399_raw = open(os.path.join(NOS, "um_absoluto.json"), "rb").read()
kman399_raw = open(os.path.join(NOS, "tgl_kernel_proof_manifest.json"), "rb").read()
assert selo399["sha256"]["um_absoluto.json"] == sha(core399_raw) and selo399["sha256"]["tgl_kernel_proof_manifest.json"] == sha(kman399_raw), "o selo v399 do Nos nao pina o core/manifesto do Nos"


def montar(nome, um_bytes, versao="v400", core_raw=core399_raw, mexe_selo=None):
    d = os.path.join(HERE, "nos_ensaio", nome)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    open(os.path.join(d, "um.py"), "wb").write(um_bytes)
    open(os.path.join(d, "um_absoluto.json"), "wb").write(core_raw)
    open(os.path.join(d, "tgl_kernel_proof_manifest.json"), "wb").write(kman399_raw)
    s = copy.deepcopy(selo399); s["um_version"] = versao; s["sha256"]["um.py"] = sha(um_bytes); s["sha256"]["um_absoluto.json"] = sha(core_raw)
    if mexe_selo:
        mexe_selo(s)
    open(os.path.join(d, "um_absoluto_selo.json"), "wb").write(json.dumps(s, ensure_ascii=False, indent=1).encode("utf-8"))
    return d


def ler(nome, um_bytes, versao="v400", **kw):
    d = montar(nome, um_bytes, versao, **kw)
    try:
        info = MOD.ler_nos(Path(d), versao)
        return {"passou": True, "alpha": info["alpha"], "um_version_linhas": info["um_version_linhas"], "UM_VERSION": info["UM_VERSION"], "beta_runtime": info["beta_runtime"],
                "beta_rel_diff": info["core"]["beta_rel_diff"], "kernel_manifesto_sha16": (info["kernel"] or {}).get("sha256", "")[:16], "um_py_sha16": info["um_py"]["sha256"][:16]}, info
    except MOD.Recusa as e:
        return {"passou": False, "recusa": str(e)}, None


R["ler_nos_candidato_v400"], NOS_INFO = ler("candidato", cand)
core_obj = json.loads(core399_raw)
def core_com_beta(f):
    c = copy.deepcopy(core_obj); c["core"]["beta"] = c["core"]["beta"] * f
    return json.dumps(c, ensure_ascii=False).encode("utf-8")
L5584 = b"ALPHA_FINE_CODATA_2018 = 7.2973525693e-3\r\n"
assert cand.count(L5584) == 1
assert cand.count(b"\r\n\r\ndef _beta_runtime() -> float:") == 1, "ancora do controle n3"
neg = {
    "alfa_segunda_linha_coluna_0": (lambda: ler("n1", cand + b"\r\nALPHA_FINE_CODATA_2018 = 0.0072973525693\r\n")[0], "ALPHA_LINHA_NAO_UNICA"),
    "alfa_reatribuido_indentado": (lambda: ler("n2", cand + b"\r\nif True:\r\n    ALPHA_FINE_CODATA_2018 = 0.0072973525693\r\n")[0], "ALPHA_REATRIBUIDA_INDENTADA"),
    "a_redeclaracao_da_v399_reposta": (lambda: ler("n3", cand.replace(b"\r\n\r\ndef _beta_runtime() -> float:", b"\r\nALPHA_FINE_CODATA_2018 = 0.0072973525693     # a da v399\r\n\r\ndef _beta_runtime() -> float:", 1))[0], "ALPHA_LINHA_NAO_UNICA"),
    "um_version_segunda_linha": (lambda: ler("n4", cand + b'\r\nUM_VERSION = "v400"\r\n')[0], "UM_VERSION_LINHA_NAO_UNICA"),
    "beta_do_core_1e-10": (lambda: ler("n5", cand, core_raw=core_com_beta(1 + 1e-10))[0], "BETA_CORE_DIVERGE_DO_RUNTIME"),
    "selo_de_outra_versao": (lambda: ler("n6", cand, mexe_selo=lambda s: s.__setitem__("um_version", "v399"))[0], "SELO_VERSAO_DIFERENTE"),
    "alfa_fora_do_contrato": (lambda: ler("n7", cand.replace(L5584, b"ALPHA_FINE_CODATA_2018 = 1.5\r\n", 1))[0], "ALPHA_OUTSIDE_CONTRACT"),
}
R["ler_nos_controles_negativos"] = {}
for k, (f, cod) in neg.items():
    r = f(); R["ler_nos_controles_negativos"][k] = {"recusa": r.get("recusa"), "esperado": cod, "ok": (not r["passou"]) and str(r.get("recusa")).startswith(cod)}
assert any("a_redeclaracao_da_v399_reposta" == k for k in R["ler_nos_controles_negativos"])
# ------------------------------------------------------------------ (3) a producao, so lida
can_mod, can_pin = MOD.carregar_canonical(Path(PROD))
ant = MOD.estado_anterior(Path(PROD), can_mod)
rps_p = PINOS["recibo_pre_selo"]["path"]; rps_raw = open(rps_p, "rb").read(); rps = json.loads(rps_raw)
pino_pino = json.load(open(os.path.join(V400, "PINO_RECIBO_PRE_SELO_v400.json"), encoding="utf-8"))
R["producao"] = {"manifesto_sha16": ant["sha256"][:16], "deployment_id": ant["deployment_id"], "version": ant["version"], "um_py_pinado16": str(ant["um_py_pinado"])[:16],
                 "seal_sha_pinado16": str(ant["seal_sha_pinado"])[:16], "estado_do_contrato_instalado": ant["estado_do_contrato_instalado"],
                 "kernel_manifesto_registrado16": str((ant["_man"].get("sincronizacao") or {}).get("kernel_manifesto_sha256"))[:16],
                 "canonical_py16": can_pin["sha256"][:16],
                 "igual_ao_que_o_recibo_pre_selo_registrou": ant["sha256"] == (rps.get("manifesto_anterior") or {}).get("sha256"),
                 "igual_ao_que_o_recibo_da_recusa_v399_registrou": ant["sha256"] == (rec_v399.get("manifesto_anterior") or {}).get("sha256"),
                 "deployments_no_estado": sorted(os.listdir(os.path.join(PROD, "estado")))[-6:] if os.path.isdir(os.path.join(PROD, "estado")) else None}
# o pino do pino (PINO_RECIBO_PRE_SELO_v400.json) e o PINOS_BN: o mesmo recibo, por sha
R["pre_selo_pino"] = {"sha16_arquivo": sha(rps_raw)[:16], "pinos_bn": PINOS["recibo_pre_selo"]["sha256"][:16], "pino_do_pino_sha16": shaf(os.path.join(V400, "PINO_RECIBO_PRE_SELO_v400.json"))[:16],
                      "pino_do_pino_no_pinos_bn": PINOS["recibo_pre_selo"]["pino_do_pino"]["sha256"][:16],
                      "chaves_do_pino_do_pino": sorted(pino_pino.keys())[:30]}
# ------------------------------------------------------------------ (4) o recibo pre_selo reaproveitado, conferido pelo esboco contra a producao de AGORA
SELO_ANT = PINOS["selo_anterior_v398"]["path"]; KMAN_ANT = PINOS["kernel_manifesto_anterior_v398"]["path"]
assert shaf(SELO_ANT) == PINOS["selo_anterior_v398"]["sha256"] and shaf(KMAN_ANT) == PINOS["kernel_manifesto_anterior_v398"]["sha256"]
try:
    RPS_INFO = MOD.conferir_recibo_pre_selo(rps_p, ant, Path(PROD), False, PINOS["recibo_pre_selo"]["sha256"], SELO_ANT, KMAN_ANT, None)
    R["conferir_recibo_pre_selo"] = {"passou": True, "versao": RPS_INFO["versao"], "veredito": RPS_INFO["veredito"], "um_py16": RPS_INFO["um_py_sha256"][:16], "selo16": str(RPS_INFO["selo_sha256"])[:16],
                                     "kernel_anterior": {k: v[:16] for k, v in RPS_INFO["kernel_anterior"].items()}, "salto": RPS_INFO["salto"], "bateria": RPS_INFO["bateria"]}
except MOD.Recusa as e:
    RPS_INFO = None; R["conferir_recibo_pre_selo"] = {"passou": False, "recusa": str(e)}
# controles: o selo anterior trocado pelo da v399; o pino errado
negp = {}
for nome, args in (("selo_anterior_e_o_da_v399", (rps_p, ant, Path(PROD), False, PINOS["recibo_pre_selo"]["sha256"], os.path.join(NOS, "um_absoluto_selo.json"), KMAN_ANT, None)),
                   ("pino_do_recibo_errado", (rps_p, ant, Path(PROD), False, "0" * 64, SELO_ANT, KMAN_ANT, None)),
                   ("como_se_ja_sincronizada", (rps_p, ant, Path(PROD), True, PINOS["recibo_pre_selo"]["sha256"], SELO_ANT, KMAN_ANT, None))):
    try:
        MOD.conferir_recibo_pre_selo(*args); negp[nome] = {"recusou": False}
    except MOD.Recusa as e:
        negp[nome] = {"recusou": True, "recusa": str(e)[:200]}
R["conferir_recibo_pre_selo_controles"] = negp
# ------------------------------------------------------------------ (5) o T17 emulado (passo simples v398 -> v400) e a variante do salto
KR = PINOS["kernel_recibo"]["path"]; CRI = PINOS["criterios"]["path"]
crit = MOD.carregar_criterios(CRI, PINOS["criterios"]["sha256"], "v400")
ok17, det17, pino17 = MOD.verificar_kernel_recibo(KR, "v400", NOS_INFO, PINOS["kernel_recibo"]["sha256"], RPS_INFO, False, crit)
R["t17_passo_simples"] = {"passou": ok17, "detalhe": det17[:900]}
kr = json.load(open(KR, encoding="utf-8")); km399 = json.loads(kman399_raw); ff399 = km399["formal_files_sha256"]


def variante(nome, mexe):
    k = copy.deepcopy(kr); mexe(k)
    p = os.path.join(HERE, "nos_ensaio", "KERNEL_RECIBO_" + nome + ".json"); open(p, "wb").write(json.dumps(k, ensure_ascii=False).encode("utf-8"))
    ok, det, _ = MOD.verificar_kernel_recibo(p, "v400", NOS_INFO, None, None, True, crit)   # sandbox: sem pino e sem o cruzamento com o pre_selo (so' o diff formal)
    return {"passou": ok, "detalhe": det[:300]}


def salto_antes_v399(k, pedras):
    k["formal_files_antes"] = dict(ff399); k["raiz"]["sha256_antes"] = ff399["TGLExt.lean"]; k["audit"]["sha256_antes"] = ff399["TGL/Audit.lean"]
    imp = MOD.impressao_formal(ff399); k["nos_kernel_impressao"]["antes"] = imp; k["nos_kernel_impressao"]["depois"] = imp; k["pedras"] = pedras


R["t17_variante_salto_antes_v399_pedras_vazias"] = variante("salto_vazias", lambda k: salto_antes_v399(k, []))
R["t17_variante_salto_antes_v399_com_testemunho"] = variante("salto_testemunho", lambda k: salto_antes_v399(k, kr["pedras"]))
R["t17_controle_sandbox_passo_simples"] = variante("simples_sandbox", lambda k: None)
# ------------------------------------------------------------------ (6) a cadeia de selos tentada (v398 -> v399)
CAD = os.path.join(V400, "salto_r3_4", "CADEIA_DE_SELOS_v400_TENTATIVA.json")
try:
    MOD.carregar_cadeia_de_selos(CAD, shaf(CAD)); R["cadeia_v398_v399"] = {"aceita": True}
except MOD.Recusa as e:
    R["cadeia_v398_v399"] = {"aceita": False, "recusa": str(e)}
cj = json.load(open(CAD, encoding="utf-8"))
R["cadeia_v398_v399"]["elos"] = [{"versao": e.get("versao"), "um_py16": (e.get("um_py") or {}).get("sha256", "")[:16], "um_py_path": (e.get("um_py") or {}).get("path")} for e in cj.get("elos", [])]
# ------------------------------------------------------------------ a foto da producao depois
foto_depois = foto(PROD)
dif = sorted(k for k in set(foto_antes) | set(foto_depois) if foto_antes.get(k) != foto_depois.get(k))
R["producao_inalterada_por_este_exame"] = {"n_arquivos": len(foto_depois), "diferencas": dif[:20], "ok": not dif}
R["tempo_s"] = round(time.time() - t0, 1)
R["veredito"] = {
    "nos_real_v399_recusa_identica": R["ler_nos_nos_real_v399"].get("identica") is True,
    "candidato_passa_ler_nos": R["ler_nos_candidato_v400"]["passou"] and R["ler_nos_candidato_v400"]["alpha"]["n_linhas_nao_indentadas"] == 1 and R["ler_nos_candidato_v400"]["alpha"]["n_reatribuicoes_indentadas"] == 0,
    "controles_ler_nos_todos_recusam": all(v["ok"] for v in R["ler_nos_controles_negativos"].values()),
    "bancada_pina_B8_v398": R["producao"]["deployment_id"] == "B8-v398-20261024-R1" and R["producao"]["version"] == "v398",
    "manifesto_igual_ao_do_recibo_pre_selo": R["producao"]["igual_ao_que_o_recibo_pre_selo_registrou"],
    "pre_selo_aceito_pelo_esboco": R["conferir_recibo_pre_selo"]["passou"], "pre_selo_controles_recusam": all(v["recusou"] for v in negp.values()),
    "t17_passo_simples_passa": ok17, "t17_salto_recusa": not R["t17_variante_salto_antes_v399_pedras_vazias"]["passou"] and not R["t17_variante_salto_antes_v399_com_testemunho"]["passou"],
    "cadeia_v398_v399_recusada_no_elo_v399": (not R["cadeia_v398_v399"]["aceita"]) and "CADEIA_DE_SELOS_UM_PY_COM_DECLARACAO_NAO_UNICA" in R["cadeia_v398_v399"].get("recusa", ""),
    "producao_inalterada": R["producao_inalterada_por_este_exame"]["ok"]}
json.dump(R, open(os.path.join(HERE, "GUARDAS_E_BN_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R["veredito"], ensure_ascii=False, indent=1))
print("ler_nos real:", R["ler_nos_nos_real_v399"]); print("candidato:", R["ler_nos_candidato_v400"]); print("producao:", R["producao"])
print("pre_selo:", R["conferir_recibo_pre_selo"]); print("controles pre_selo:", negp)
print("T17 simples:", R["t17_passo_simples"]); print("T17 salto vazias:", R["t17_variante_salto_antes_v399_pedras_vazias"]); print("T17 salto testemunho:", R["t17_variante_salto_antes_v399_com_testemunho"])
print("T17 simples sandbox:", R["t17_controle_sandbox_passo_simples"]); print("cadeia:", R["cadeia_v398_v399"]); print("producao inalterada:", R["producao_inalterada_por_este_exame"]); print("tempo", R["tempo_s"])
