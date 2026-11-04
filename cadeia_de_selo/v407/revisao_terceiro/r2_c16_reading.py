# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R2): (1) c16 de psion_canto_v407 varre o core por conjunto_d/teste_d_/ramo_b+resultado|veredito: base passa; chave de resultado do teste D no core reprova; (2) o campo fock_face.reading de testemunha_estatica_v396 ramifica pela chave lida."""
import copy, importlib.util, json, sys, time
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev3", R + "um_v407_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev3"] = m; spec.loader.exec_module(m)
print("import ok", round(time.time() - t0, 1), "s", m.UM_VERSION)
core0 = json.load(open(R + "dry_v407/core_ensaio.json", encoding="utf-8"))["core"]
F = m.psion_canto_v407
def c16(core):
    r = F(copy.deepcopy(core)); ch = {c["id"]: c["ok"] for c in r["mechanics"]["checks"]}
    return ch.get("c16"), r["all_verified"], r["verdict"][:60]
print("base:", c16(core0))
casos = [("chave top-level 'conjunto_d_resultado'", lambda c: c.__setitem__("conjunto_d_resultado", {"z": 1})),
         ("chave top-level 'teste_d_veredito'", lambda c: c.__setitem__("teste_d_veredito", "X")),
         ("chave top-level 'ramo_b_resultado'", lambda c: c.__setitem__("ramo_b_resultado", 1)),
         ("chave top-level 'ramo_b_veredito_v407'", lambda c: c.__setitem__("ramo_b_veredito_v407", 1)),
         ("chave top-level 'RAMO_B_RESULTADO' (maiusculas)", lambda c: c.__setitem__("RAMO_B_RESULTADO", 1)),
         ("chave top-level 'ramo_b_preregistration_v386' (existente na base, nao deve reprovar)", lambda c: c.__setitem__("ramo_b_preregistration_v386", c.get("ramo_b_preregistration_v386", {"a": 1}))),
         ("(limite) resultado ANINHADO: ramo_b_preregistration_v386.resultado", lambda c: c.__setitem__("ramo_b_preregistration_v386", {"resultado": 0.5})),
         ("(limite) resultado ANINHADO em chave nova sem o nome: 'outro'.'teste_d_resultado'", lambda c: c.__setitem__("outro", {"teste_d_resultado": 0.5})),
         ("(limite) valor com veredito de D: 'x': 'NOT_FALSIFIED_UNDERPOWERED'", lambda c: c.__setitem__("x", "NOT_FALSIFIED_UNDERPOWERED"))]
for nome, mut in casos:
    c = copy.deepcopy(core0); mut(c)
    try: print("%-95s -> c16=%s all_verified=%s" % (nome, *c16(c)[:2]))
    except Exception as e: print(nome, "EXCECAO", repr(e)[:150])
print("top-level keys do core do ensaio contendo conjunto_d / teste_d_ / ramo_b:", [k for k in core0 if any(s in k.lower() for s in ("conjunto_d", "teste_d_", "ramo_b"))])
# (2) reading
nome = m._V407_PSION_CONTRACT["ancora_lema"]
c = copy.deepcopy(core0); c.pop("testemunha_estatica_v396", None)
r = m.testemunha_estatica_v396(c); ff = r["fock_face"]
print("\n== com o lema lido: chave", ff["linked_to_the_corner_by_a_lemma"], "\nreading:", ff["reading"])
print("reading_v396:", ff.get("reading_v396"))
c = copy.deepcopy(core0); c.pop("testemunha_estatica_v396", None); c["kernel_formalization"]["axiom_report"].pop(nome)
r = m.testemunha_estatica_v396(c); ff = r["fock_face"]
print("\n== SEM o lema: chave", ff["linked_to_the_corner_by_a_lemma"], "\nreading:", ff["reading"])
# habitante fora (ramo _hab406t_ falso) + lema lido
c = copy.deepcopy(core0); c.pop("testemunha_estatica_v396", None)
for k in list(c["kernel_formalization"]["axiom_report"]):
    if "physicalFockCertificate" in k: c["kernel_formalization"]["axiom_report"].pop(k)
r = m.testemunha_estatica_v396(c); ff = r["fock_face"]
print("\n== sem physicalFockCertificate no axiom_report: chave", ff["linked_to_the_corner_by_a_lemma"], "\nreading:", ff["reading"][:420])
