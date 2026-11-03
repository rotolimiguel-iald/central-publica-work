# -*- coding: utf-8 -*-
"""Revisor terceiro v406: importa o CANDIDATO (sem executar o main) e testa, sobre o core do ensaio a seco (dry_v406/core_ensaio.json), que
_v406_certificado_habitado e fechamento_v406 sao fail-closed: nega UMA condicao por vez. Nao escreve nada fora desta pasta."""
import copy, hashlib, importlib.util, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v406_candidato.py")
m = importlib.util.module_from_spec(spec)
sys.modules["um_cand_rev"] = m
spec.loader.exec_module(m)
print("import ok", round(time.time() - t0, 1), "s;  UM_VERSION", m.UM_VERSION)
core0 = json.load(open(R + "dry_v406/core_ensaio.json", encoding="utf-8"))["core"]
kf0 = core0["kernel_formalization"]
C = m._V406_FECHO_CONTRACT
nome = C["ancora_certificado"]; rel = C["ancoras"][nome]["rel"]
print("ancora", nome, "rel", rel)
print("axioms da ancora:", kf0["axiom_report"].get(nome), "| src:", kf0["declaration_sources_v394"].get(nome), "| sha ok:", kf0["formal_files_sha256"].get(rel) == C["source_sha256"].get(rel))
H = m._v406_certificado_habitado
res = {}


def t(nome_, kf, esperado):
    r = H(kf); ok = (r is esperado) if isinstance(esperado, bool) else (r == esperado)
    res[nome_] = {"devolveu": r, "esperado": esperado, "ok": ok}
    print(("OK   " if ok else "FALHA"), nome_, "->", r)


t("base (habitado)", kf0, True)
k = copy.deepcopy(kf0); del k["axiom_report"][nome]; t("nome ausente do axiom_report", k, False)
k = copy.deepcopy(kf0); k["axiom_report"] = {}; t("axiom_report vazio", k, False)
k = copy.deepcopy(kf0); del k["axiom_report"]; t("axiom_report ausente", k, False)
for ax in (["propext", "sorryAx"], ["propext", "Classical.choice", "Quot.sound", "sorryAx"], ["Lean.ofReduceBool"], ["TGL.axioma_proprio"], ["propext", 5]):
    k = copy.deepcopy(kf0); k["axiom_report"][nome] = ax; t("fora do trio %r" % (ax,), k, False)
k = copy.deepcopy(kf0); k["axiom_report"][nome] = []; t("axiom list vazia (zero axiomas)", k, False)
k = copy.deepcopy(kf0); k["axiom_report"][nome] = "propext"; t("axiom nao-lista", k, False)
k = copy.deepcopy(kf0); k["declaration_sources_v394"][nome] = "TGLExt/F1Fecho394/PhysicalCanonicalNetCompleteR1.lean"; t("proveniencia errada (outro modulo)", k, False)
k = copy.deepcopy(kf0); del k["declaration_sources_v394"][nome]; t("proveniencia ausente", k, False)
k = copy.deepcopy(kf0); del k["declaration_sources_v394"]; t("declaration_sources_v394 ausente", k, False)
k = copy.deepcopy(kf0); k["formal_files_sha256"][rel] = "0" * 64; t("sha256 formal do rito errado", k, False)
k = copy.deepcopy(kf0); del k["formal_files_sha256"][rel]; t("sha256 formal do rito ausente", k, False)
k = copy.deepcopy(kf0); del k["formal_files_sha256"]; t("formal_files_sha256 ausente", k, False)
t("kf vazio", {}, False); t("kf None", None, False)
# sha embutido errado: altera o corpo embutido temporariamente
orig = m._EMBEDDED_KERNEL_FILES[rel]
m._EMBEDDED_KERNEL_FILES[rel] = orig + "\n-- adulterado"
t("fonte EMBUTIDA adulterada (hash difere do contrato)", kf0, False)
del m._EMBEDDED_KERNEL_FILES[rel]; t("fonte EMBUTIDA ausente", kf0, False)
m._EMBEDDED_KERNEL_FILES[rel] = orig; t("fonte restaurada", kf0, True)
# contrato
sv = m._V406_FECHO_CONTRACT
m._V406_FECHO_CONTRACT = {}; t("contrato ausente", kf0, False)
c2 = copy.deepcopy(sv); c2["source_sha256"][rel] = "0" * 64; m._V406_FECHO_CONTRACT = c2; t("sha do contrato errado", kf0, False)
c2 = copy.deepcopy(sv); del c2["ancora_certificado"]; m._V406_FECHO_CONTRACT = c2; t("contrato sem ancora_certificado", kf0, False)
m._V406_FECHO_CONTRACT = sv
# achado candidato: o auxiliar nao le all_verified/returncodes
k = copy.deepcopy(kf0); k["all_verified"] = False; k["build_returncode"] = 1; k["audit_returncode"] = 1
t("kernel all_verified False + rc 1 (R2: o auxiliar agora exige all_verified)", k, False)
k = copy.deepcopy(kf0); del k["all_verified"]; t("kernel sem all_verified", k, False)

# --- fechamento_v406 inteiro: base e negacoes
F = m.fechamento_v406


def f(nome_, core, quer_ok):
    c = copy.deepcopy(core)
    r = F(c)
    v = r["verdict"]; ok_ = v.startswith("TGL_FECHAMENTO_V406__THE_FOCK_CERTIFICATE_IS_INHABITED") and r["all_verified"] is True
    certo = (ok_ is quer_ok)
    res["fechamento: " + nome_] = {"verdict": v[:110], "all_verified": r["all_verified"], "esperado_ok": quer_ok, "ok": certo}
    print(("OK   " if certo else "FALHA"), "fechamento:", nome_, "->", v[:100], r["all_verified"], "| cert:", r.get("certificate_inhabited"))
    return r


r0 = f("base", core0, True)
print("   checks:", [(c_["id"], c_["ok"]) for c_ in r0["mechanics"]["checks"]], "n_ancoras_ok", r0["values"]["n_ancoras_ok"], "n_modulos_ok", r0["values"]["n_modulos_ok"])
c = copy.deepcopy(core0); del c["kernel_formalization"]["axiom_report"][nome]; f("ancora do certificado ausente", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][nome] = ["propext", "sorryAx"]; f("ancora do certificado com sorryAx", c, False)
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(anc, None); f("ancora ausente: " + anc.split(".")[-1], c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["declaration_sources_v394"][nome] = "x.lean"; f("proveniencia errada", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"][rel] = "1" * 64; f("sha256 formal errado do modulo do topo", c, False)
r_ = C["ancoras"]["TGL.ModularRealization.canonicalFullTGLWitness"]["rel"]
c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"][r_] = "1" * 64; f("sha256 formal errado da candidata", c, False)
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_clean"] = 11859; f("escada 11859", c, False)
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["verdict"] = "OUTRO"; f("gate com outro veredito", c, False)
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["full_static_witness_exists"] = True; f("full_static_witness_exists True", c, False)
c = copy.deepcopy(core0); c["witness_rigidity"]["trivial_inhabitant_exists"] = True; f("trivial_inhabitant_exists True", c, False)
c = copy.deepcopy(core0); c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] = True; f("lema de ligacao True", c, False)
c = copy.deepcopy(core0); c["psibit_v395"]["all_verified"] = False; f("psibit_v395 nao selado", c, False)
c = copy.deepcopy(core0); c["witness_layers"]["canonical_full_witness_term_constructed"] = False; f("witness_layers False", c, False)
c = copy.deepcopy(core0); c["rede_fock_v394"]["whole_certificate_inhabited"] = False; f("rede_fock chave False", c, False)
c = copy.deepcopy(core0); c["psibit_v395"]["conditional_psion_face"]["status"] = "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"; f("status antigo do psibit", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["all_verified"] = False; f("kernel all_verified False", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["declaration_sources_status_v394"] = {"ok": False}; f("proveniencia status nao ok", c, False)
c = copy.deepcopy(core0); c["beta"] = c["beta"] * 1.001; f("beta do core divergente", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"].pop(r_); f("hash formal da candidata ausente", c, False)
c = copy.deepcopy(core0); f2 = [x for x in C["flags"]][0]; c["kernel_formalization"][f2] = False; f("uma bandeira do bundle False", c, False)
# embutida adulterada -> fechamento recusa
m._EMBEDDED_KERNEL_FILES[rel] = orig + "\n-- adulterado"
f("fonte embutida do topo adulterada", core0, False)
m._EMBEDDED_KERNEL_FILES[rel] = orig
# guarda de frases: dado que _v406_guarda_frases pega
for frase, deve in (("a luz não tem autovetor nenhum", True), ("«a luz não tem autovetor nenhum»", False), ("K(O) ≠ ⊥ está provado", True), ("o certificado foi confirmado", True), ("o único autovetor da luz", True), ("o único vetor fixo da luz", False), ("tudo derivado", None)):
    g = m._v406_guarda_frases(frase)
    print("guarda:", repr(frase), "->", [x[0] for x in g])
n_ok = sum(1 for v in res.values() if v.get("ok") is True); n_f = sum(1 for v in res.values() if v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
json.dump(res, open(R + "revisao_terceiro/c_fail_closed_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
