# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): roda, sobre copias do core do ensaio, as funcoes VIVAS do candidato que mudaram ou sao novas:
_v409_rodar_specs (cunhagens_v409, kh_n1_cobertura_v409), _v408_rodar_specs e _v407_rodar_specs (cujos pisos mudaram), e as funcoes herdadas (tetelestai_terminal_v408, psion_canto_v407, fechamento_v406, rede_fock_v394,
psibit_v395, testemunha_estatica_v396) com o contrato da escada 12187. Confere que (1) os specs selam; (2) recusam quando devem (negacoes de uma condicao por vez); (3) as respostas do operador sao
exigidas por algum registro da v409 (cunhagens_v409 u51-u77 ou o traducao_turing_v409)."""
import copy, importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
spec = importlib.util.spec_from_file_location("um_cand_rev2", R + "um_v409_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev2"] = m; spec.loader.exec_module(m)
core0 = json.load(open(R + "dry_v409/core_ensaio.json", encoding="utf-8"))["core"]
C = m._V409_TRADUCAO_CONTRACT
res = {}
ESPEC = ("cunhagens_v409", "kh_n1_cobertura_v409", "cunhagens_v408", "kh_n1_cobertura_v408", "cunhagens_v407", "kh_n1_cobertura_v407", "traducao_turing_v409", "tetelestai_terminal_v408")


def rec(k, v, ok): res[k] = {"v": v, "ok": ok}; print(("OK   " if ok else "FALHA"), k, v if not ok else "")


def roda(c, ate_v409=True):
    """a ORDEM do main: v407 specs, v408 (registro + specs), v409 (registro + specs)."""
    for k_ in ESPEC: c.pop(k_, None)
    m._v407_rodar_specs(c)
    m.tetelestai_terminal_v408(c); m._v408_rodar_specs(c)
    m.traducao_turing_v409(c); m._v409_rodar_specs(c)


# 1. a base
c = copy.deepcopy(core0); roda(c)
for k_ in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "cunhagens_v407", "kh_n1_cobertura_v407"):
    rec("sela: %s" % k_, (c.get(k_) or {}).get("verdict", "")[:90], (c.get(k_) or {}).get("all_verified") is True)
for fn in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407"):
    c2 = copy.deepcopy(core0)
    if fn == "testemunha_estatica_v396": c2.pop(fn, None)
    try:
        rr = getattr(m, fn)(c2); rec("herdada %s sela com a escada 12187" % fn, rr.get("verdict", "")[:80], rr.get("all_verified") is True)
    except Exception as e:   # noqa: BLE001
        rec("herdada %s rodou" % fn, repr(e)[:200], False)
# o veredito do core do ensaio == o recalculado?
for k_ in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"):
    rec("veredito recalculado == o do core do ensaio: %s" % k_, [(c.get(k_) or {}).get("verdict", "")[:60], (core0.get(k_) or {}).get("verdict", "")[:60]], (c.get(k_) or {}).get("verdict") == (core0.get(k_) or {}).get("verdict"))
# 1b. controle: na ORDEM ERRADA (v409 antes dos v408/v407) a cunhagens_v409 recusa (u12-u17 leem os selos)
c = copy.deepcopy(core0)
for k_ in ESPEC: c.pop(k_, None)
m.traducao_turing_v409(c); m._v409_rodar_specs(c)
rec("controle: ordem errada (v409 antes dos registros v408/v407) => cunhagens_v409 recusa", (c.get("cunhagens_v409") or {}).get("verdict", "")[:90], (c.get("cunhagens_v409") or {}).get("all_verified") is False)


# 2. negacoes: uma condicao por vez
def neg(nome, mut, alvos, quer_recusa=True):
    c_ = copy.deepcopy(core0); mut(c_)
    try:
        roda(c_)
    except Exception as e:   # noqa: BLE001
        rec("negacao %s rodou" % nome, repr(e)[:200], False); return
    st = {a: (c_.get(a) or {}).get("all_verified") for a in alvos}
    ok_ = all(v is False for v in st.values()) if quer_recusa else all(v is True for v in st.values())
    rec("negacao %s => %s" % (nome, "recusa" if quer_recusa else "sela"), st, ok_)


# 2a. respostas do operador: remover o teorema do axiom_report => ALGUM registro da v409 recusa
n_rec = 0; tot = 0; passa = []
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        tot += 1
        c_ = copy.deepcopy(core0); c_["kernel_formalization"]["axiom_report"].pop(t_["completo"], None); roda(c_)
        if any((c_.get(a) or {}).get("all_verified") is False for a in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")): n_rec += 1
        else: passa.append((r_["id"], t_["curto"]))
rec("respostas: remover o teorema do axiom_report => ALGUM registro da v409 recusa (%d de %d)" % (n_rec, tot), passa[:6], n_rec == tot)
n_rec = 0; passa = []
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        c_ = copy.deepcopy(core0); c_["kernel_formalization"]["declaration_sources_v394"].pop(t_["completo"], None); roda(c_)
        if any((c_.get(a) or {}).get("all_verified") is False for a in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")): n_rec += 1
        else: passa.append((r_["id"], t_["curto"]))
rec("respostas: remover a PROVENIENCIA de cada teorema => ALGUM registro da v409 recusa (%d de %d)" % (n_rec, tot), passa[:6], n_rec == tot)
neg("gate com outro veredito", lambda c: c["qg_closure"]["gate"].__setitem__("verdict", "OUTRO"), ["traducao_turing_v409", "cunhagens_v409"])
neg("full_static_witness_exists True", lambda c: c["qg_closure"]["gate"].__setitem__("full_static_witness_exists", True), ["cunhagens_v409"])
neg("trivial_inhabitant_exists True", lambda c: c["witness_rigidity"].__setitem__("trivial_inhabitant_exists", True), ["cunhagens_v409"])
neg("chave do lema (v407) False", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False), ["cunhagens_v409"])
neg("rede_fock_v394 chave False", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False), ["cunhagens_v409"])
neg("neutrino com outro veredito", lambda c: c["neutrino_mass"].__setitem__("verdict", "OUTRO"), ["cunhagens_v409"])
neg("kernel: constante fora do trio", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("fora_do_trio", 1), ["kh_n1_cobertura_v409", "kh_n1_cobertura_v408"])
neg("formal_files_sha256 com arquivo extra", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Intruso.lean", "0" * 64), ["kh_n1_cobertura_v409"])
neg("formal_files_sha256: TraducaoTuring com hash errado", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/TraducaoTuring.lean", "0" * 64), ["traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"])
neg("formal_files_sha256: ParNaFaceDeFock com hash errado", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/ParNaFaceDeFock.lean", "1" * 64), ["traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"])
neg("proveniencia status nao ok", lambda c: c["kernel_formalization"].__setitem__("declaration_sources_status_v394", {"ok": False}), ["cunhagens_v409", "kh_n1_cobertura_v409"])
neg("cobertura de constantes diferente (34165)", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("decl", 34165), ["kh_n1_cobertura_v409"])
neg("cobertura de teoremas diferente (27270)", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("thm", 27270), ["kh_n1_cobertura_v409"])
neg("escada: limpos 12186", lambda c: c["external_ladder"].__setitem__("n_theorems_clean", 12186), ["traducao_turing_v409", "cunhagens_v409"])
neg("tetelestai_terminal_v408 nao selado (chave do core)", lambda c: c["kernel_formalization"].__setitem__("ext_tu409_0138", False), ["traducao_turing_v409", "cunhagens_v409"])
print("   chaves do axiom_coverage_v392:", sorted(core0["kernel_formalization"]["axiom_coverage_v392"].keys())[:20])
n_ok = sum(1 for v in res.values() if isinstance(v, dict) and v.get("ok") is True); n_f = sum(1 for v in res.values() if isinstance(v, dict) and v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
for k_, v_ in res.items():
    if v_.get("ok") is False: print("  FALHOU:", k_, v_["v"])
json.dump(res, open(R + "revisao_terceiro/k_funcoes_vivas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
