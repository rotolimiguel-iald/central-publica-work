# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): importa o CANDIDATO (sem executar o main) e testa, sobre o core do ensaio a seco (dry_v407/core_ensaio.json), que
_v407_elo_lido e psion_canto_v407 sao fail-closed: nega UMA condicao por vez. Nao escreve nada fora desta pasta."""
import copy, hashlib, importlib.util, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v407_candidato.py")
m = importlib.util.module_from_spec(spec)
sys.modules["um_cand_rev"] = m
spec.loader.exec_module(m)
print("import ok", round(time.time() - t0, 1), "s;  UM_VERSION", m.UM_VERSION)
core0 = json.load(open(R + "dry_v407/core_ensaio.json", encoding="utf-8"))["core"]
kf0 = core0["kernel_formalization"]
C = m._V407_PSION_CONTRACT
nome = C["ancora_lema"]; rel = C["ancoras"][nome]["rel"]
print("ancora", nome, "rel", rel, "| axioms:", kf0["axiom_report"].get(nome), "| src:", kf0["declaration_sources_v394"].get(nome), "| sha ok:", kf0["formal_files_sha256"].get(rel) == C["source_sha256"].get(rel), "| all_verified:", kf0.get("all_verified"))
H = m._v407_elo_lido
res = {}


def t(nome_, kf, esperado):
    r = H(kf); ok = (r is esperado)
    res[nome_] = {"devolveu": r, "esperado": esperado, "ok": ok}
    print(("OK   " if ok else "FALHA"), nome_, "->", r)


t("base (lido)", kf0, True)
k = copy.deepcopy(kf0); del k["axiom_report"][nome]; t("nome ausente do axiom_report", k, False)
k = copy.deepcopy(kf0); k["axiom_report"] = {}; t("axiom_report vazio", k, False)
k = copy.deepcopy(kf0); del k["axiom_report"]; t("axiom_report ausente", k, False)
for ax in (["propext", "sorryAx"], ["propext", "Classical.choice", "Quot.sound", "sorryAx"], ["Lean.ofReduceBool"], ["TGL.axioma_proprio"], ["propext", 5]):
    k = copy.deepcopy(kf0); k["axiom_report"][nome] = ax; t("fora do trio %r" % (ax,), k, False)
k = copy.deepcopy(kf0); k["axiom_report"][nome] = []; t("axiom list vazia", k, False)
k = copy.deepcopy(kf0); k["axiom_report"][nome] = "propext"; t("axiom nao-lista", k, False)
k = copy.deepcopy(kf0); k["declaration_sources_v394"][nome] = "TGLExt/Par.lean"; t("proveniencia errada (outro modulo do bundle)", k, False)
k = copy.deepcopy(kf0); k["declaration_sources_v394"][nome] = "TGLExt/F1Fecho394/CanonicalFockModularCoreInputR1.lean"; t("proveniencia errada (modulo antigo)", k, False)
k = copy.deepcopy(kf0); del k["declaration_sources_v394"][nome]; t("proveniencia ausente", k, False)
k = copy.deepcopy(kf0); del k["declaration_sources_v394"]; t("declaration_sources_v394 ausente", k, False)
k = copy.deepcopy(kf0); k["formal_files_sha256"][rel] = "0" * 64; t("sha256 formal do rito errado", k, False)
k = copy.deepcopy(kf0); del k["formal_files_sha256"][rel]; t("sha256 formal do rito ausente", k, False)
k = copy.deepcopy(kf0); del k["formal_files_sha256"]; t("formal_files_sha256 ausente", k, False)
k = copy.deepcopy(kf0); k["all_verified"] = False; t("kernel all_verified False (kernel recusado)", k, False)
k = copy.deepcopy(kf0); del k["all_verified"]; t("kernel sem all_verified", k, False)
k = copy.deepcopy(kf0); k["all_verified"] = "True"; t("all_verified string 'True' (nao `is True`)", k, False)
t("kf vazio", {}, False); t("kf None", None, False)
orig = m._EMBEDDED_KERNEL_FILES[rel]
m._EMBEDDED_KERNEL_FILES[rel] = orig + "\n-- adulterado"
t("fonte EMBUTIDA adulterada (hash difere do contrato)", kf0, False)
del m._EMBEDDED_KERNEL_FILES[rel]; t("fonte EMBUTIDA ausente", kf0, False)
m._EMBEDDED_KERNEL_FILES[rel] = orig; t("fonte restaurada", kf0, True)
sv = m._V407_PSION_CONTRACT
m._V407_PSION_CONTRACT = {}; t("contrato ausente", kf0, False)
c2 = copy.deepcopy(sv); c2["source_sha256"][rel] = "0" * 64; m._V407_PSION_CONTRACT = c2; t("sha do contrato errado", kf0, False)
c2 = copy.deepcopy(sv); del c2["ancora_lema"]; m._V407_PSION_CONTRACT = c2; t("contrato sem ancora_lema", kf0, False)
c2 = copy.deepcopy(sv); c2["ancoras"].pop(nome); m._V407_PSION_CONTRACT = c2; t("contrato sem a ancora no dict ancoras", kf0, False)
m._V407_PSION_CONTRACT = sv
t("restaurado", kf0, True)

# --- psion_canto_v407 inteiro: base e negacoes
F = m.psion_canto_v407


def f(nome_, core, quer_ok):
    c = copy.deepcopy(core)
    try:
        r = F(c)
    except Exception as e:   # noqa: BLE001
        res["psion_canto: " + nome_] = {"excecao": repr(e)[:200], "esperado_ok": quer_ok, "ok": False}
        print("EXCECAO", nome_, repr(e)[:200]); return None
    v = r["verdict"]; ok_ = v.startswith("TGL_PSION_CANTO_V407__THE_LEMMA_THAT_LINKS_THE_TWO_FACES") and r["all_verified"] is True
    certo = (ok_ is quer_ok)
    res["psion_canto: " + nome_] = {"verdict": v[:110], "all_verified": r["all_verified"], "esperado_ok": quer_ok, "ok": certo}
    print(("OK   " if certo else "FALHA"), "psion_canto:", nome_, "->", v[:100], r["all_verified"])
    return r


r0 = f("base", core0, True)
print("   checks:", [(c_["id"], c_["ok"]) for c_ in r0["mechanics"]["checks"]], "n_ancoras_ok", r0["values"]["n_ancoras_ok"], "n_modulos_ok", r0["values"]["n_modulos_ok"], "n_flags_true", r0["values"]["n_flags_true"])
print("   keys:", r0["keys"])
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(anc, None); f("ancora ausente: " + anc.split(".")[-1], c, False)
for anc in (nome, C["ancora_par"]):
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = ["propext", "sorryAx"]; f("ancora com sorryAx: " + anc.split(".")[-1], c, False)
    c = copy.deepcopy(core0); c["kernel_formalization"]["declaration_sources_v394"][anc] = "x.lean"; f("proveniencia errada: " + anc.split(".")[-1], c, False)
    fl = C["ancoras"][anc]["flag"]; c = copy.deepcopy(core0); c["kernel_formalization"][fl] = False; f("bandeira False: " + anc.split(".")[-1], c, False)
for r_ in C["source_sha256"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"][r_] = "1" * 64; f("sha256 formal errado: " + r_.split("/")[-1], c, False)
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_clean"] = 11957; f("escada 11957", c, False)
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_expected"] = 11860; f("escada esperada 11860 (a da v406)", c, False)
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["verdict"] = "OUTRO"; f("gate com outro veredito", c, False)
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["full_static_witness_exists"] = True; f("full_static_witness_exists True", c, False)
c = copy.deepcopy(core0); c["witness_rigidity"]["trivial_inhabitant_exists"] = True; f("trivial_inhabitant_exists True", c, False)
c = copy.deepcopy(core0); c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] = False; f("chave do lema False (literal)", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["all_verified"] = False; f("kernel recusado mas chave True (literal)", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(nome); f("lema ausente do kernel mas chave True (literal)", c, False)
for reg in ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"):
    c = copy.deepcopy(core0); c[reg]["all_verified"] = False; f("%s nao selado" % reg, c, False)
c = copy.deepcopy(core0); c["rede_fock_v394"]["whole_certificate_inhabited"] = False; f("rede_fock chave False", c, False)
c = copy.deepcopy(core0); c["psibit_v395"]["conditional_psion_face"]["inhabitant_exhibited"] = False; f("psibit inhabitant False", c, False)
c = copy.deepcopy(core0); c["witness_layers"]["canonical_full_witness_term_constructed"] = False; f("witness_layers False", c, False)
c = copy.deepcopy(core0); c["beta"] = c["beta"] * 1.001; f("beta do core divergente", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["declaration_sources_status_v394"] = {"ok": False}; f("proveniencia status nao ok", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"].pop("TGLExt/Par.lean"); f("hash formal do Par ausente", c, False)
# respostas do operador: tira um teorema "que ja existia"
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(t_["completo"]); f("resposta %s: teorema %s ausente" % (r_["id"], t_["curto"]), c, False)
# raiz sem import
raiz0 = m._EMBEDDED_KERNEL_FILES["TGLExt.lean"]
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz0.replace("import TGLExt.OIgual\n", "").replace("import TGLExt.OIgual\r\n", "")
f("raiz embutida sem o import OIgual", core0, False)
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz0
# teste D
sv = m._V407_PSION_CONTRACT
c2 = copy.deepcopy(sv); c2["teste_d"]["resultado_no_um_py"] = 0.5; m._V407_PSION_CONTRACT = c2; f("teste D com resultado no um.py", core0, False)
c2 = copy.deepcopy(sv); c2["teste_d"]["so_citado"] = False; m._V407_PSION_CONTRACT = c2; f("teste D nao so citado", core0, False)
c2 = copy.deepcopy(sv); c2["teste_d"]["manifesto_sha256"] = "2" * 64; c2["teste_d"]["manifesto_sha16"] = "2" * 16; m._V407_PSION_CONTRACT = c2; f("teste D: manifesto sha != fonte embutida", core0, False)
m._V407_PSION_CONTRACT = sv
# fontes embutidas adulteradas
orig = m._EMBEDDED_KERNEL_FILES[rel]
m._EMBEDDED_KERNEL_FILES[rel] = orig + "\n-- adulterado"; f("fonte embutida do PsionCanto adulterada", core0, False)
m._EMBEDDED_KERNEL_FILES[rel] = orig
# falas do operador adulteradas
ver = m._V407_VERBATINS2
k0 = list(ver)[0]; sv_t = ver[k0]["text"]; ver[k0]["text"] = sv_t + " x"; f("fala do operador adulterada (sha256 difere)", core0, False); ver[k0]["text"] = sv_t
# guarda de frases
for frase, deve in (("o par na face de Fock está provado", True), ("Ω = Φ⁺", True), ("a luz não tem autovetor nenhum", True), ("PAIR_CONFIRMED", True), ("o elo é de estrutura, não de vetores", False), ("o par na face de Fock segue [OPEN]", False)):
    g = m._v407_guarda_frases(frase)
    print("guarda:", repr(frase), "->", [x[0] for x in g], "(esperado reprovar)" if deve else "(esperado passar)")
    res["guarda: " + frase] = {"reprovou": bool(g), "esperado": deve, "ok": bool(g) == deve}
n_ok = sum(1 for v in res.values() if v.get("ok") is True); n_f = sum(1 for v in res.values() if v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
json.dump(res, open(R + "revisao_terceiro/c_fail_closed_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
