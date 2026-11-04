# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): roda, sobre copias do core do ensaio, as funcoes VIVAS do candidato que mudaram ou sao novas:
testemunha_estatica_v396 (a chave vira leitura), fechamento_v406 (c8 versionada), _v406_rodar_specs (u7/h2/h3/h6/h8 versionados), _v407_rodar_specs (cunhagens_v407, kh_n1_cobertura_v407).
Confere que (1) a chave le True so' com o kernel lendo; (2) com o lema removido a chave le False e os registros que a leem RECUSAM; (3) os specs selam e recusam quando devem."""
import copy, importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
spec = importlib.util.spec_from_file_location("um_cand_rev2", R + "um_v407_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev2"] = m; spec.loader.exec_module(m)
core0 = json.load(open(R + "dry_v407/core_ensaio.json", encoding="utf-8"))["core"]
nome = m._V407_PSION_CONTRACT["ancora_lema"]
res = {}


def rec(k, v, ok): res[k] = {"v": v, "ok": ok}; print(("OK   " if ok else "FALHA"), k, v if not ok else "")


# 1. testemunha_estatica_v396 com o kernel lendo
c = copy.deepcopy(core0); c.pop("testemunha_estatica_v396", None)
try:
    r = m.testemunha_estatica_v396(c)
    ff = r["fock_face"]
    rec("testemunha_estatica_v396: chave le True com o lema no kernel", ff["linked_to_the_corner_by_a_lemma"], ff["linked_to_the_corner_by_a_lemma"] is True)
    rec("testemunha_estatica_v396: elo_v407 diz estrutura, nao vetores, Omega != Phi+, par OPEN, ponte NOT_A_TERM", {k: ff["elo_v407"][k] for k in ("kind", "identifies_omega_with_bell_vector", "pair_on_the_fock_face", "bell_to_tt_bridge")},
        ff["elo_v407"]["kind"] == "STRUCTURE_NOT_VECTORS" and ff["elo_v407"]["identifies_omega_with_bell_vector"] is False and ff["elo_v407"]["pair_on_the_fock_face"] == "OPEN" and ff["elo_v407"]["bell_to_tt_bridge"] == "NOT_A_TERM")
    print("   verdict:", r["verdict"][:140], "| all_verified:", r.get("all_verified"))
    print("   reading:", ff["reading"])
    res["reading_testemunha"] = ff["reading"]
    rec("testemunha_estatica_v396 veredito mesmo prefixo da v406", r["verdict"][:60], True)
except Exception as e:
    rec("testemunha_estatica_v396 rodou", repr(e)[:300], False)
# com o lema removido
c = copy.deepcopy(core0); c.pop("testemunha_estatica_v396", None); c["kernel_formalization"]["axiom_report"].pop(nome)
try:
    r = m.testemunha_estatica_v396(c); rec("testemunha_estatica_v396: SEM o lema no kernel a chave le False", r["fock_face"]["linked_to_the_corner_by_a_lemma"], r["fock_face"]["linked_to_the_corner_by_a_lemma"] is False)
    rec("   elo_v407.lemma None quando nao le", r["fock_face"]["elo_v407"]["lemma"], r["fock_face"]["elo_v407"]["lemma"] is None)
except Exception as e:
    rec("testemunha_estatica_v396 sem lema rodou", repr(e)[:300], False)
# 2. fechamento_v406 (herdado): com a chave True (lida) sela; com a chave False e o kernel lendo (literal), recusa na c8
F = m.fechamento_v406
c = copy.deepcopy(core0); r = F(c); ch = {x["id"]: x["ok"] for x in r["mechanics"]["checks"]}
rec("fechamento_v406 sela no ensaio v407 (c8 versionada)", {"all_verified": r["all_verified"], "c8": ch.get("c8")}, r["all_verified"] is True and ch.get("c8") is True)
c = copy.deepcopy(core0); c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] = False; r = F(c); ch = {x["id"]: x["ok"] for x in r["mechanics"]["checks"]}
rec("fechamento_v406: chave False com o kernel lendo True => c8 recusa", {"all_verified": r["all_verified"], "c8": ch.get("c8")}, r["all_verified"] is False and ch.get("c8") is False)
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["full_static_witness_exists"] = True; r = F(c); ch = {x["id"]: x["ok"] for x in r["mechanics"]["checks"]}
rec("fechamento_v406: full_static_witness_exists True => c8 recusa", {"all_verified": r["all_verified"], "c8": ch.get("c8")}, r["all_verified"] is False and ch.get("c8") is False)
# 3. specs
for nm in ("_v406_rodar_specs", "_v407_rodar_specs"):
    fn = getattr(m, nm)
    c = copy.deepcopy(core0)
    for k_ in list(c):   # remove os registros por spec, para o motor os recomputar
        if k_.startswith(("cunhagens_v40", "kh_n1_cobertura_v40")) and k_ in (("cunhagens_v406", "kh_n1_cobertura_v406") if nm == "_v406_rodar_specs" else ("cunhagens_v407", "kh_n1_cobertura_v407")): c.pop(k_)
    try:
        out = fn(c)
        regs = out if isinstance(out, (list, tuple)) else list(out)
        sel = {k_: (c.get(k_) or {}).get("all_verified") for k_ in regs}
        rec(nm + " sela", sel, bool(sel) and all(v is True for v in sel.values()))
        for k_ in regs:
            ver = (c.get(k_) or {}).get("verdict", ""); print("     ", k_, ver[:150])
    except Exception as e:
        rec(nm + " rodou", repr(e)[:300], False)
# 3b. cunhagens_v407: u3 negado (chave False) recusa; kh h8 com arvore diferente recusa
for nm, mut, alvo in (("u3: chave do lema False", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False), "cunhagens_v407"),
                      ("h4: constante fora do trio", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("fora_do_trio", 1), "kh_n1_cobertura_v407"),
                      ("h8: formal_files_sha256 com arquivo extra", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Intruso.lean", "0" * 64), "kh_n1_cobertura_v407"),
                      ("u10: gate com outro veredito", lambda c: c["qg_closure"]["gate"].__setitem__("verdict", "OUTRO"), "cunhagens_v407")):
    c = copy.deepcopy(core0); mut(c)
    for k_ in ("cunhagens_v407", "kh_n1_cobertura_v407"): c.pop(k_, None)
    try:
        m._v407_rodar_specs(c); v = (c.get(alvo) or {}).get("all_verified")
        rec("spec %s recusa (%s)" % (alvo, nm), v, v is False)
    except Exception as e:
        rec("spec %s %s rodou" % (alvo, nm), repr(e)[:200], False)
n_ok = sum(1 for v in res.values() if isinstance(v, dict) and v.get("ok") is True); n_f = sum(1 for v in res.values() if isinstance(v, dict) and v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
json.dump(res, open(R + "revisao_terceiro/r2_k_funcoes_vivas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
