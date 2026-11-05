# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): roda, sobre copias do core do ensaio, as funcoes VIVAS do candidato que mudaram ou sao novas:
_v408_rodar_specs (cunhagens_v408, kh_n1_cobertura_v408), _v407_rodar_specs (cunhagens_v407 e kh_n1_cobertura_v407, cujos pisos mudaram), e as funcoes herdadas (psion_canto_v407, fechamento_v406, rede_fock_v394,
psibit_v395, testemunha_estatica_v396) com o contrato da escada 12002. Confere que (1) os specs selam; (2) recusam quando devem (negacoes de uma condicao por vez); (3) as respostas do operador sao
exigidas pela cunhagens_v408 (u39-u72), ja' que NAO entram nas 16 checagens do tetelestai_terminal_v408."""
import copy, importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("um_cand_rev2", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev2"] = m; spec.loader.exec_module(m)
core0 = json.load(open(R + "dry_v408/core_ensaio.json", encoding="utf-8"))["core"]
C = m._V408_TERMINAL_CONTRACT
res = {}


def rec(k, v, ok): res[k] = {"v": v, "ok": ok}; print(("OK   " if ok else "FALHA"), k, v if not ok else "")


def so_specs(c, v8=True, v7=True):
    for k_ in ("cunhagens_v408", "kh_n1_cobertura_v408"): c.pop(k_, None)
    for k_ in ("cunhagens_v407", "kh_n1_cobertura_v407"): c.pop(k_, None)


# 1. a base: o registro com funcao + specs v408 + specs v407 selam sobre o core do ensaio
c = copy.deepcopy(core0); so_specs(c)
r = m.tetelestai_terminal_v408(c); rec("tetelestai_terminal_v408 sela", r["verdict"][:80], r["all_verified"] is True)
n7 = m._v407_rodar_specs(c); n8 = m._v408_rodar_specs(c)   # ordem do main: os specs da v407 ANTES (cunhagens_v408 u13/u14 leem os selos deles)
for k_ in n8 + n7:
    rec("spec %s sela" % k_, (c.get(k_) or {}).get("verdict", "")[:90], (c.get(k_) or {}).get("all_verified") is True)
# as herdadas, recalculadas
for fn in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407"):
    c2 = copy.deepcopy(core0)
    if fn == "testemunha_estatica_v396": c2.pop(fn, None)
    try:
        rr = getattr(m, fn)(c2); rec("herdada %s sela com a escada 12002" % fn, rr.get("verdict", "")[:80], rr.get("all_verified") is True)
    except Exception as e:   # noqa: BLE001
        rec("herdada %s rodou" % fn, repr(e)[:200], False)


# 1b. controle: na ORDEM ERRADA (v408 antes da v407) a cunhagens_v408 recusa por u13/u14 (le o selo dos specs da v407)
c = copy.deepcopy(core0); so_specs(c); m.tetelestai_terminal_v408(c); m._v408_rodar_specs(c)
rec("controle: ordem errada (specs v408 antes dos v407) => cunhagens_v408 recusa", (c.get("cunhagens_v408") or {}).get("verdict", "")[:90], (c.get("cunhagens_v408") or {}).get("all_verified") is False)
# 2. negacoes: uma condicao por vez
def neg(nome, mut, alvos, quer_recusa=True):
    c_ = copy.deepcopy(core0); mut(c_); so_specs(c_)
    try:
        m._v407_rodar_specs(c_); m.tetelestai_terminal_v408(c_); m._v408_rodar_specs(c_)   # ordem do main
    except Exception as e:   # noqa: BLE001
        rec("negacao %s rodou" % nome, repr(e)[:200], False); return
    st = {a: (c_.get(a) or {}).get("all_verified") for a in alvos}
    ok_ = all(v is False for v in st.values()) if quer_recusa else all(v is True for v in st.values())
    rec("negacao %s => %s" % (nome, "recusa" if quer_recusa else "sela"), st, ok_)


# 2a. respostas do operador (u39-u72): remover UMA resposta de declaration_sources => cunhagens_v408 recusa (e quantas)
n_rec = 0; tot = 0; passa = []
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        tot += 1
        c_ = copy.deepcopy(core0); so_specs(c_); c_["kernel_formalization"]["declaration_sources_v394"].pop(t_["completo"], None)
        m._v407_rodar_specs(c_); m.tetelestai_terminal_v408(c_); m._v408_rodar_specs(c_)
        if (c_.get("cunhagens_v408") or {}).get("all_verified") is False: n_rec += 1
        else: passa.append((r_["id"], t_["curto"]))
rec("respostas: remover a PROVENIENCIA de cada teorema citado => cunhagens_v408 recusa (%d de %d)" % (n_rec, tot), passa[:6], n_rec == tot)
n_rec = 0; passa = []
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        c_ = copy.deepcopy(core0); so_specs(c_); c_["kernel_formalization"]["axiom_report"].pop(t_["completo"], None)
        m._v407_rodar_specs(c_); m.tetelestai_terminal_v408(c_); m._v408_rodar_specs(c_)
        if (c_.get("cunhagens_v408") or {}).get("all_verified") is False or (c_.get("tetelestai_terminal_v408") or {}).get("all_verified") is False or (c_.get("kh_n1_cobertura_v408") or {}).get("all_verified") is False: n_rec += 1
        else: passa.append((r_["id"], t_["curto"]))
rec("respostas: remover o teorema do axiom_report => ALGUM registro da v408 recusa (%d de %d)" % (n_rec, tot), passa[:6], n_rec == tot)
neg("gate com outro veredito", lambda c: c["qg_closure"]["gate"].__setitem__("verdict", "OUTRO"), ["tetelestai_terminal_v408", "cunhagens_v408"])
neg("full_static_witness_exists True", lambda c: c["qg_closure"]["gate"].__setitem__("full_static_witness_exists", True), ["cunhagens_v408"])
neg("trivial_inhabitant_exists True", lambda c: c["witness_rigidity"].__setitem__("trivial_inhabitant_exists", True), ["cunhagens_v408"])
neg("psion_canto_v407 nao selado", lambda c: c["psion_canto_v407"].__setitem__("all_verified", False), ["cunhagens_v408"])
neg("chave do lema (v407) False", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False), ["cunhagens_v408"])
neg("rede_fock_v394 chave False", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False), ["cunhagens_v408"])
neg("neutrino com outro veredito (core.neutrino_mass.verdict)", lambda c: c["neutrino_mass"].__setitem__("verdict", "OUTRO"), ["cunhagens_v408"])
neg("kernel: constante fora do trio", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("fora_do_trio", 1), ["kh_n1_cobertura_v408", "kh_n1_cobertura_v407"])
neg("formal_files_sha256 com arquivo extra", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Intruso.lean", "0" * 64), ["kh_n1_cobertura_v408"])
neg("formal_files_sha256: um arquivo com hash errado", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/PIgualNP.lean", "0" * 64), ["cunhagens_v408", "kh_n1_cobertura_v408"])
neg("fonte formal de um modulo novo mudou", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/TetelestaiTerminal.lean", "1" * 64), ["cunhagens_v408"])
neg("proveniencia status nao ok", lambda c: c["kernel_formalization"].__setitem__("declaration_sources_status_v394", {"ok": False}), ["cunhagens_v408", "kh_n1_cobertura_v408"])
neg("cobertura de constantes diferente (33906)", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("decl", 33906), ["kh_n1_cobertura_v408"])
neg("cobertura de teoremas diferente (27068)", lambda c: c["kernel_formalization"]["axiom_coverage_v392"].__setitem__("thm", 27068), ["kh_n1_cobertura_v408"])
print("   chaves do axiom_coverage_v392:", sorted(core0["kernel_formalization"]["axiom_coverage_v392"].keys())[:20])
n_ok = sum(1 for v in res.values() if isinstance(v, dict) and v.get("ok") is True); n_f = sum(1 for v in res.values() if isinstance(v, dict) and v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
for k_, v_ in res.items():
    if v_.get("ok") is False: print("  FALHOU:", k_, v_["v"])
json.dump(res, open(R + "revisao_terceiro/k_funcoes_vivas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
