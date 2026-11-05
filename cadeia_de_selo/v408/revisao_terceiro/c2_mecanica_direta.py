# -*- coding: utf-8 -*-
"""Revisor v408 R1: chama v408_terminal_mechanics DIRETO (sem o pre-cheque _v408_formal) para ver que cada checagem c1..c16 falha por si so' quando a sua condicao e' negada."""
import copy, importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
core0 = json.load(open(R + "dry_v408/core_ensaio.json", encoding="utf-8"))["core"]
C = m._V408_TERMINAL_CONTRACT
beta0 = core0["beta"]
def fal(core, beta=beta0, C_=None):
    r = m.v408_terminal_mechanics(beta, core, C_ or C)
    return [c["id"] for c in r["checks"] if not c["ok"]]
print("base:", fal(core0))
res = {}
def t(nome, mut, quer, beta=beta0, Cmut=None):
    c = copy.deepcopy(core0); mut(c); C_ = None
    if Cmut: C_ = copy.deepcopy(C); Cmut(C_)
    f = fal(c, beta, C_); ok = all(q in f for q in quer); res[nome] = {"falhos": f, "quer": quer, "ok": ok}; print(("OK   " if ok else "FALHA"), nome, "->", f)
anc = list(C["ancoras"])[0]
t("c1: ancora fora do axiom_report", lambda c: c["kernel_formalization"]["axiom_report"].pop(anc), ["c1"])
t("c1: bandeira False", lambda c: c["kernel_formalization"].__setitem__(C["ancoras"][anc]["flag"], False), ["c1"])
t("c2: sha256 formal de um modulo errado", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/PIgualNP.lean", "0" * 64), ["c2"])
t("c13: escada limpa != esperada", lambda c: c["external_ladder"].__setitem__("n_theorems_clean", 12001), ["c13"])
t("c13: bandeira ausente", lambda c: c["kernel_formalization"].pop(C["flags"][3]), ["c13"])
t("c12: gate outro", lambda c: c["qg_closure"]["gate"].__setitem__("verdict", "X"), ["c12"])
t("c16: beta do core divergente", lambda c: c.__setitem__("beta", beta0 * 1.01), ["c16"])
t("c6/c7/c9/c16: beta fora de (0,1)", lambda c: None, ["c6", "c7", "c9", "c16"], beta=2.0)
t("c6/c7/c9/c16: beta None", lambda c: None, ["c6", "c7", "c9", "c16"], beta=None)
sv = m._V408_TERMINAL_TEXT; sd = list(sv["diz"]); sv["diz"] = sd + ["a TGL prova P = NP de Turing (Cook-Levin)"]
t("c14: texto com frase proibida", lambda c: None, ["c14"]); sv["diz"] = sd
sf = m._v392_fonte_bytes; m._v392_fonte_bytes = lambda k: (False, "X", b"")
t("c15: insumo purgado nao confere", lambda c: None, ["c15"]); m._v392_fonte_bytes = sf
t("c15: contrato diz integra pinada", lambda c: None, ["c15"], Cmut=lambda C_: C_["insumo_purgado"].__setitem__("integra_pinada", True))
print("c3,c4,c5,c8,c10,c11: aritmetica pura (exp(0), e^-1/2, f+(1-f), N*ln2, 2^(N+1), k_B*ln2): nao leem o core nem beta; base:", fal(core0))
n_f = sum(1 for v in res.values() if not v["ok"]); print("RESUMO", len(res), "casos;", n_f, "falhas")
json.dump(res, open(R + "revisao_terceiro/c2_mecanica_direta_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
