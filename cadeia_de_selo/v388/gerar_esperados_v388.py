# -*- coding: utf-8 -*-
"""gerar_esperados_v388.py -- ESPERADOS_v388.json LIDOS dos artefatos (molde: gerar_esperados_v387.py): o estado SELADO da v387 pinado (todos os vereditos; os que
citam a escada 6137 MUDAM so por 6137 -> 6154, e isso e' dito); as 17 bandeiras novas; os vereditos v388 do ensaio; o pilar pela mesma chave."""
import hashlib, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v388.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, "um_v388_candidato.py"))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v387_sha16"] == "64c899f86d8d32e1"
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v388.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v387"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v387_sha16"], "escada": CM["escada"], "flags_v388": CM["flags"], "nomes_v388": CM["nomes"],
       "pedra_sha16": CM["kernel"]["new"]["TGLExt/TheCouplingRunsBoundedBelow.lean"], "fase9_files": CM["fase9"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v387": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")},
       "regra_da_mudanca_dita": "um veredito da v387 so pode mudar trocando '6137' por '6154' (a escada cresce 17); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_leituras": {k: selo0.get(k) for k in selo0 if re.search(r"_reading_v3(7[7-9]|8[0-6])$", k)},
       "selo_registros_v387": {k: selo0.get(k) for k in ("hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387")},
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v387": sorted(k for k, v in kf.items() if v is True),
       "vereditos_v388_do_ensaio": {k: ens["mainflow"][k]["verdict"] for k in ("beta_runs_bounded_below_v388", "hubble_ratio_opening_v388")},
       "artigo_marcas": {"pt": ["Ao lado (v388):", "TheCouplingRunsBoundedBelow", "Errata ao lado:", "A Fase 9 aberta.", "reexecutou", "Ao lado (v387)"],
                         "en": ["Beside (v388):", "TheCouplingRunsBoundedBelow", "Erratum beside:", "Phase 9 opened.", "re-executed", "Beside (v387)"]},
       "toc": {"pt": ["Ao lado (v388)", "Ao lado (v387)"], "en": ["Beside (v388)", "Beside (v387)"]},
       "md_carimbo": "**Versão v388**", "md_ao_lado": "Ao lado (v388, 06/10/2026)", "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v388.json"))}
assert len(esp["selo_leituras"]) == 9 and esp["escada"] == [6137, 6154] and not (set(esp["flags_v388"]) & set(esp["flags_true_v387"]))
out = os.path.join(HERE, "ESPERADOS_v388.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print("ESPERADOS_v388:", esp["candidato_sha16"], "| vereditos v387 pinados:", len(esp["vereditos_v387"]), "| flags True v387:", len(esp["flags_true_v387"]))
