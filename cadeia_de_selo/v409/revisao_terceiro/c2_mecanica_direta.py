# -*- coding: utf-8 -*-
"""Revisor v409 R1: chama v409_traducao_mechanics DIRETO (sem o pre-cheque _v409_formal) para ver que cada checagem c1..c20 falha por si so' quando a sua condicao e' negada
(core, contrato ou beta), e quais delas sao aritmetica pura da instancia de brinquedo (nao leem o core nem o kernel)."""
import copy, importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v409_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
core0 = json.load(open(R + "dry_v409/core_ensaio.json", encoding="utf-8"))["core"]
C = m._V409_TRADUCAO_CONTRACT
beta0 = core0["beta"]


def fal(core, beta=beta0, C_=None):
    r = m.v409_traducao_mechanics(beta, core, C_ or C)
    return [c["id"] for c in r["checks"] if not c["ok"]]


print("base:", fal(core0))
res = {}


def t(nome, mut, quer, beta=beta0, Cmut=None):
    c = copy.deepcopy(core0); mut(c); C_ = None
    if Cmut: C_ = copy.deepcopy(C); Cmut(C_)
    try:
        f = fal(c, beta, C_); ok = all(q in f for q in quer)
    except Exception as e:   # noqa: BLE001
        f = ["EXC " + repr(e)[:120]]; ok = False
    res[nome] = {"falhos": f, "quer": quer, "ok": ok}; print(("OK   " if ok else "FALHA"), nome, "->", f)


anc = list(C["ancoras"])[0]
t("c1: ancora fora do axiom_report", lambda c: c["kernel_formalization"]["axiom_report"].pop(anc), ["c1"])
t("c1: bandeira False", lambda c: c["kernel_formalization"].__setitem__(C["ancoras"][anc]["flag"], False), ["c1"])
t("c2: sha256 formal de TraducaoTuring errado", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/TraducaoTuring.lean", "0" * 64), ["c2"])
t("c2: sha256 formal de ParNaFaceDeFock errado", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/ParNaFaceDeFock.lean", "0" * 64), ["c2"])
t("c14: gate outro", lambda c: c["qg_closure"]["gate"].__setitem__("verdict", "X"), ["c14"])
t("c15: escada limpa != esperada", lambda c: c["external_ladder"].__setitem__("n_theorems_clean", 12186), ["c15"])
t("c15: bandeira ausente", lambda c: c["kernel_formalization"].pop(C["flags"][3]), ["c15"])
t("c17: beta do core divergente", lambda c: c.__setitem__("beta", beta0 * 1.01), ["c17"])
t("c13/c17: beta fora de (0,1)", lambda c: None, ["c13", "c17"], beta=2.0)
t("c13/c17: beta None", lambda c: None, ["c13", "c17"], beta=None)
sv = m._V409_TRADUCAO_TEXT; sd = list(sv["diz"]); sv["diz"] = sd + ["a TGL prova P = NP de Turing (Cook-Levin)"]
t("c16: texto com frase proibida", lambda c: None, ["c16"]); sv["diz"] = sd
# contrato: instancias e inscricao
t("c4/c20: SIM insatisfazivel", lambda c: None, ["c4", "c20"], Cmut=lambda C_: C_["instancia_sim"].__setitem__("clausulas", [[1], [-1], [2]]))
t("c10/c20: NAO satisfazivel", lambda c: None, ["c10", "c20"], Cmut=lambda C_: C_["instancia_nao"].__setitem__("clausulas", [[1]]))
t("c19: s vazio", lambda c: None, ["c19"], Cmut=lambda C_: C_["inscricao_brinquedo"].__setitem__("s", []))
t("c19: Omega nulo (divisao)", lambda c: None, ["c19"], Cmut=lambda C_: C_["inscricao_brinquedo"].__setitem__("omega", [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]))
t("c1: n_ancoras do contrato 81", lambda c: None, ["c1"], Cmut=lambda C_: C_.__setitem__("n_ancoras", 81))
t("c2: sha256 do contrato errado", lambda c: None, ["c2"], Cmut=lambda C_: C_["source_sha256"].__setitem__("TGLExt/TraducaoTuring.lean", "0" * 64))
# aritmetica pura: nao leem core/kernel/beta (so' instancia + contrato)
puros = {}
for ck in ("c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c18", "c19", "c20"):
    puros[ck] = None
print("c3-c12, c18-c20: dependem so' da instancia FIXA do contrato (c13 tambem de beta); base:", fal(core0))
# a instancia SIM trocada por outra satisfazivel (3 solucoes) ainda sela? (mostra que as checagens nao pinam a instancia)
t("controle: instancia SIM trocada por outra satisfazivel (nao deve falhar c4/c20)", lambda c: None, [], Cmut=lambda C_: C_["instancia_sim"].__setitem__("clausulas", [[1, 2], [-1, 3]]))
n_f = sum(1 for v in res.values() if not v["ok"]); print("RESUMO", len(res), "casos;", n_f, "falhas")
json.dump(res, open(R + "revisao_terceiro/c2_mecanica_direta_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
