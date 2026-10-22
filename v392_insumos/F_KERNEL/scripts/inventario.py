# -*- coding: utf-8 -*-
"""Monta INVENTARIO_V392_KERNEL.json a partir dos artefatos do sandbox (todo hash LIDO dos bytes; nada digitado)."""
import hashlib
import json
import os
import re
import time

F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"


def J(p):
    return json.load(open(os.path.join(F, p), encoding="utf-8"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


A = J("RESULTADO_A_sozinhas.json")["resultados"]
B = J("RESULTADO_B_modulos.json")
B0 = J("RESULTADO_B0_resolucao_raiz.json")["demo"]
BJ = J("RESULTADO_B_conjunto.json")["resultados"]
CP = J("RESULTADO_C_preparo.json")
CR = J("RESULTADO_C_raiz.json")
CD = J("RESULTADO_C_delta.json")
CC = J("RESULTADO_C_completa.json")
CX = J("RESULTADO_C_delta_x19.json")
KH1 = J("RESULTADO_KH_D1.json")
KH2 = J("RESULTADO_KH_D2.json")
KHF = json.load(open(os.path.join(F, "kh", "KH_N1_final.json"), encoding="utf-8"))
KHC = json.load(open(os.path.join(F, "kh", "D2_consolidado.json"), encoding="utf-8"))
K76 = J("RESULTADO_KH_formato_umpy_76.json")
KT = J("RESULTADO_KH_formato_umpy_total.json")
PP = {s["nome"]: s for s in J("RESULTADO_P_palavra.json")["sondas"]}
SS = {s["nome"]: s for s in J("RESULTADO_S_sondas_eq.json")["sondas"]}
EMB = J("embutido_vs_kernel.json")
OVV = J("ov_verificacao_inicial.json")
MEM = J("superficies_memoria.json")

padroes = {
    "FORMAL_DIR": r"^FORMAL_DIR = ", "_EMBEDDED_KERNEL_FILES_inicio": r"^_EMBEDDED_KERNEL_FILES = \{",
    "chave_TGLExt.lean": r'^    "TGLExt\.lean":', "chave_TGL/Audit.lean": r'^    "TGL/Audit\.lean":',
    "chave_TGLExt/Fundacao.lean": r"^    'TGLExt/Fundacao\.lean':", "def_materialize_embedded_kernel": r"^def materialize_embedded_kernel",
    "_LEAN_THEOREM_FLAGS": r"^_LEAN_THEOREM_FLAGS = \{", "bandeiras_v390_fnd": r"^    # v390 \(07/10/2026; a Fundacao",
    "_LEAN_FORBIDDEN_TOKENS": r"^_LEAN_FORBIDDEN_TOKENS", "def__lean_source_forbidden_tokens": r"^def _lean_source_forbidden_tokens",
    "def_verify_tgl_kernel_formalization": r"^def verify_tgl_kernel_formalization",
    "lake_build": r'build = run_process_checked\(\[lake, "build"\]', "lake_env_lean_audit": r'audit = run_process_checked\(\[lake, "env", "lean", "TGL/Audit.lean"\]',
    "blob": r"blob = \(build", "regex_depends": r"depends on axioms: \\\[\(\[\^\\\]\]\*\)\\\]\", blob",
    "escada_ext_flags": r"^    ext_flags = \[", "escada_v390": r"^        # v390: a Fundacao", "n_theorems_expected": r'"n_theorems_expected": len\(ext_flags\)',
    "_ESQUELETO_STONES": r"^_ESQUELETO_STONES = \[", "ledger_v390": r'^    \("v390", "Fundacao"', "_FND_FLAGS_V390": r"^_FND_FLAGS_V390",
    "_V390_PEDRA": r"^_V390_PEDRA", "def_fundacao_v390": r"^def fundacao_v390", "UM_VERSION": r"^UM_VERSION = ",
}
linhas = open(UM, "rb").read().decode("utf-8").split("\n")
lin = {}
for k, rx in padroes.items():
    lin[k] = [i + 1 for i, l in enumerate(linhas) if re.search(rx, l)][:3]
i0 = lin["_EMBEDDED_KERNEL_FILES_inicio"][0] - 1
j = i0 + 1
while linhas[j].rstrip("\r") != "}":
    j += 1
lin["_EMBEDDED_KERNEL_FILES_fim"] = [j + 1]
j = lin["escada_ext_flags"][0]
while linhas[j - 1].rstrip("\r") != "    ]":
    j += 1
lin["escada_ext_flags_fim"] = [j]

prov = B["proveniencia"]
mods_b = {r["nome"][2:]: r for r in B["resultados"]}
mapa_A = {"Palavra": "A01_palavra", "LiganteLeiCampoCurvo": "A02_ligante", "V351DualScalingBridge": "A04a_f12_ponte",
          "AgapeNonVacuity": "A04b_f12_agape", "TheSingularityReadsTheAttractor": "A05_atrator_r1",
          "OpticalPopulationBridgeR2": "A06_ponte_otica_r2", "TheSingularityReadsTheAttractorAdendo1": "A07_atrator_adendo1",
          "TheLightReadsItself": "A08_luz_le_a_si", "LightNetStandardWedgeDataBGL": "A09_x19_bgl",
          "LiganteLeiCampoCurvoTestemunha": "A03_ligante_S7S8_auditoria"}
Ad = {r["nome"]: r for r in A}
j1 = [r for r in BJ if r["nome"].endswith("J1_ConjuntoV392")][0]
j2 = [r for r in BJ if r["nome"].endswith("J2_ConjuntoV392ComX19")][0]
cands = []
for mod in ["Palavra", "LiganteLeiCampoCurvo", "LiganteLeiCampoCurvoTestemunha", "V351DualScalingBridge", "AgapeNonVacuity",
            "TheSingularityReadsTheAttractorAdendo1", "TheSingularityReadsTheAttractor", "OpticalPopulationBridgeR2",
            "TheLightReadsItself", "LightNetStandardWedgeDataBGL"]:
    a = Ad[mapa_A[mod]]
    b = mods_b[mod]
    src = open(prov[mod]["instalado_em_sandbox"], "rb").read().decode("utf-8")
    cands.append({
        "modulo_proposto": "TGLExt." + mod, "caminho_no_kernel": "TGLExt/%s.lean" % mod,
        "fonte_original": prov[mod]["fonte"], "fonte_original_sha256": prov[mod]["fonte_sha256"],
        "fonte_original_bytes": os.path.getsize(prov[mod]["fonte"]),
        "bytes_identicos_na_instalacao": prov[mod]["bytes_identicos"], "instalado_sha256": prov[mod]["instalado_sha256"],
        "derivacao": prov[mod].get("troca") or prov[mod].get("cabecalho_acrescentado"),
        "namespaces": sorted(set(re.findall(r"(?m)^namespace (\S+)", src))), "imports": re.findall(r"(?m)^import (\S+)", src),
        "sozinha": {"id": a["nome"], "rc": a["rc"], "fonte_sha256": a["fonte_sha256"], "n_print_axioms": a["n_axiomas"],
                    "fora_do_trio": a["fora_do_trio"], "sorry": a["sorry"], "tokens": a["tokens_proibidos_na_fonte"],
                    "n_avisos": a["n_avisos"], "avisos": [x.split("lean:")[-1] for x in a["avisos"]],
                    "olean_sha256": a.get("olean_sha256"), "olean_entregue_sha256": a.get("olean_entregue_sha256"),
                    "olean_identico_ao_entregue": a.get("olean_identico_ao_entregue"), "segundos": a["segundos"], "log_sha256": a["log_sha256"]},
        "instalado_sandbox": {"rc": b["rc"], "n_print_axioms": b["n_axiomas"], "fora_do_trio": b["fora_do_trio"],
                              "olean_sha256": b.get("olean_sha256"), "n_avisos": b["n_avisos"], "log_sha256": b["log_sha256"]},
        "conjunto_J1": j1["por_modulo"].get("TGLExt." + mod), "conjunto_J2": j2["por_modulo"].get("TGLExt." + mod),
    })
statement = Ad["A10_x19_statement"]
inv = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "execucao": "2a (a 1a perdeu os arquivos do sandbox na limpeza; numeros iguais)",
    "um_py_sha256": sha(UM), "um_py_bytes": os.path.getsize(UM), "um_py_linhas": lin,
    "kernel_embutido": {"entradas": EMB["n"], "iguais_ao_disco": sum(1 for v in EMB["entries"].values() if v["igual"]),
                        "linhas": [EMB["start_line"], EMB["end_line"]], "ultima_chave": EMB["keys_order"][-1],
                        "TGLExt.lean": EMB["entries"]["TGLExt.lean"], "TGL/Audit.lean": EMB["entries"]["TGL/Audit.lean"],
                        "TGLExt/Fundacao.lean": EMB["entries"]["TGLExt/Fundacao.lean"]},
    "sobreposicao_ov": OVV,
    "resolucao_da_raiz": [{"nome": r["nome"], "rc": r["rc"], "erros": r["erros"][:1]} for r in B0],
    "candidatas": cands,
    "x19_statement": {"rc": statement["rc"], "n_print_axioms": statement["n_axiomas"], "fonte_sha256": statement["fonte_sha256"],
                      "n_avisos": statement["n_avisos"]},
    "conjunto": [{k: r.get(k) for k in ("nome", "rc", "segundos", "cobertura_total", "por_modulo", "erros_texto", "log", "log_sha256", "fonte_sha256")} for r in BJ],
    "raiz_e_auditoria": {"raiz_v391_sha256": CP["raiz_v391_sha256"], "raiz_v392_sha256": CP["raiz_v392_sha256"],
                         "raiz_v392_bytes": CP["raiz_v392_bytes"], "raiz_acrescimo": CP["raiz_acrescimo"],
                         "raiz_compila": {"rc": CR["rc"], "olean_sha256": CR.get("olean_sha256"), "segundos": CR["segundos"]},
                         "audit_v391_sha256": CP["audit_v391_sha256"], "audit_v392_sha256": CP["audit_v392_sha256"],
                         "audit_v392_bytes": CP["audit_v392_bytes"], "audit_acrescimo_linhas": CP["audit_acrescimo_linhas"],
                         "delta": {"rc": CD["rc"], "lidos": CD["lidos_pela_regex_do_umpy"], "esperados": CD["esperados"],
                                   "faltam": CD["faltam"], "fora": CD["fora_do_trio_lidos"], "bandeiras": CD["bandeiras_que_acenderiam"]},
                         "completa": {k: CC.get(k) for k in ("rc", "segundos", "entradas_lidas", "axr_v391", "iguais_ao_v391", "n_novos",
                                                             "n_sumidos", "diferentes", "fora_do_trio", "sorryAx_ausente",
                                                             "trustCompiler_ausente", "sentinelas_amostra", "log_sha256")},
                         "x19_delta": {"rc": CX["rc"], "n": len(CX["declaracoes"]), "lidos": CX["lidos"], "faltam": CX["faltam"], "fora": CX["fora"]},
                         "bandeiras_propostas": CP["bandeiras_propostas"]},
    "kh_n1": {"D1": {k: KH1.get(k) for k in ("rc", "segundos", "linhas_novas", "linhas_0710", "identico_ao_0710_como_conjunto", "total",
                                             "distribuicao_0710", "log_sha256")},
              "D2_blocos": [{k: b.get(k) for k in ("bloco", "rc", "s", "n_cob", "total", "fonte_sha256", "log_sha256")} for b in KH2["blocos"]],
              "D2": {k: KHC.get(k) for k in ("n", "enumeradas", "faltam", "extras", "fora_do_trio", "distribuicao", "duplicadas_entre_blocos",
                                              "atribuidas_a_mais_de_um_modulo", "axr_v391", "em_ambos", "divergentes", "teoremas",
                                              "teoremas_no_axr", "teoremas_de_usuario", "teoremas_de_usuario_no_axr", "c73", "c73_teoremas",
                                              "c73_fora", "dist73_teoremas")},
              "final": KHF,
              "formato_umpy_76": {k: K76.get(k) for k in ("rc", "segundos", "lidos_pela_regex_do_umpy", "total", "fora", "fonte_sha256", "log_sha256")},
              "formato_umpy_total": {k: KT.get(k) for k in ("rc", "segundos", "lidos_pela_regex_do_umpy", "total", "fora", "fonte_sha256", "log_sha256")}},
    "sondas": {n: {"rc": s["rc"], "segundos": s["segundos"], "fonte_sha256": s["fonte_sha256"], "log_sha256": s["log_sha256"],
                   "axiomas": s.get("axiomas")} for n, s in list(PP.items()) + list(SS.items())},
    "superficies_memoria": MEM,
    "impressao_digital": {"antes": open(os.path.join(F, "fp_before.txt")).read().strip(),
                          "depois_lean": open(os.path.join(F, "fp_after_lean.txt")).read().strip()},
}
alvo = os.path.join(F, "INVENTARIO_V392_KERNEL.json")
if os.path.exists(alvo):
    os.replace(alvo, alvo + ".anterior_%s" % time.strftime("%H%M%S"))
open(alvo, "w", encoding="utf-8").write(json.dumps(inv, ensure_ascii=False, indent=1) + "\n")
print(alvo, sha(alvo)[:16])
print(json.dumps(lin, ensure_ascii=False))
