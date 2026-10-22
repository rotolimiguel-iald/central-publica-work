# -*- coding: utf-8 -*-
"""gerar_esperados_v389.py -- ESPERADOS_v389.json LIDOS dos artefatos (molde: gerar_esperados_v388.py): o estado SELADO da v388 pinado (todos os vereditos -- a v389
nao muda calculo nem escada, logo NENHUM veredito da v388 pode mudar); as bandeiras True da v388 identicas; o iii1_net_image igual salvo o rotulo; o veredito v389 do ensaio."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v389.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, "um_v389_candidato.py"))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v388_sha16"] == "e64b00f4df75059b"
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v389.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v388"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
im0 = core0["iii1_net_image"]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v388_sha16"], "escada": [6154, 6154], "ledger": CM["ledger"], "exame": CM["exame"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v388": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")},
       "regra_da_mudanca_dita": "a v389 nao muda calculo nem escada: NENHUM veredito da v388 pode mudar",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v388": {k: selo0.get(k) for k in ("beta_runs_bounded_below_v388", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387")},
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v388": sorted(k for k, v in kf.items() if v is True),
       "iii1_sem_rotulo": {k: v for k, v in im0.items() if k != "seals"}, "iii1_seals_v388": im0["seals"], "rotulo_novo": "CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET",
       "veredito_v389_do_ensaio": ens["mainflow"]["text_label_errata_v389"]["verdict"],
       "artigo_marcas": {"pt": ["Ao lado (v389):", "um único axioma POSTO", "nesta versão (a abertura está na v388, ao lado)", "caminhos únicos do ledger citável; mais 156", "Ao lado (v388)"],
                         "en": ["Beside (v389):", "a single posited axiom", "in this version (the opening is in v388, beside)", "unique paths of the citable ledger; plus 156", "Beside (v388)"]},
       "artigo_nao": {"pt": ["parte de um único postulado", "o único postulado. A Parte C", "faz agora (v384)", "Dado o axioma da fronteira mínima", "NÃO selou"],
                      "en": ["starts from a single postulate", "the single postulate. Part C", "does now (v384)", "Given the axiom of the minimal", "did NOT seal"]},
       "toc": {"pt": ["Ao lado (v389)", "Ao lado (v388)", "v389; a cada versão ao lado"], "en": ["Beside (v389)", "Beside (v388)", "v389; each version beside"]},
       "md_carimbo": "**Versão v389**", "md_ao_lado": "Ao lado (v389, 06/10/2026)", "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v389.json"))}
assert esp["ledger"] == [1025, 156, 156] and "CLOCK_TORSION_" + "CONF" + "IRMED_ON_PHYSICAL_NET" in esp["iii1_seals_v388"]
out = os.path.join(HERE, "ESPERADOS_v389.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v389:", esp["candidato_sha16"], "| vereditos v388 pinados:", len(esp["vereditos_v388"]), "| flags True v388:", len(esp["flags_true_v388"]))
