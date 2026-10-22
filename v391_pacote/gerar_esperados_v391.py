# -*- coding: utf-8 -*-
"""gerar_esperados_v391.py -- ESPERADOS_v391.json LIDOS dos artefatos (molde: gerar_esperados_v390.py): o estado SELADO da v390 pinado. Nenhum veredito da v390
pode mudar (nenhuma troca: a escada fica 6163; o registro da v389 le o sucessor do titulo e fica IDENTICO; a v390 fica IDENTICA). +1 chave: estatuto_da_prova_v391,
cujo veredito so difere do ensaio no carimbo do proprio hash (o do candidato == o instalado). O pilar pela mesma chave."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v391.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, "um_v391_candidato.py"))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v390_sha16"] == "0f5154bcc2f931cb"
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v391.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v390"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v390_sha16"], "escada": [6163, 6163], "verbatim": CM["verbatim"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v390": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}, "troca_dita": [],
       "regra_da_mudanca_dita": "nenhum veredito da v390 pode mudar; o registro da v389 le o sucessor do titulo e fica IDENTICO; qualquer mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v390": {k: selo0.get(k) for k in ("fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")},
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v390": sorted(k for k, v in kf.items() if v is True),
       "runtime_seals_v390": core0["runtime_of_the_one"]["seals"], "what_remains_v390": core0["tgl_closure"]["what_remains_named"],
       "veredito_v391_do_ensaio_sem_carimbo": re.sub(r"CERTIFIED_BY_SELF_HASH_[0-9a-f]{16}", "CERTIFIED_BY_SELF_HASH_<SHA16>", ens["mainflow"]["estatuto"]["verdict"]),
       "artigo_marcas": {"pt": ["O estatuto da prova (v391).", "O estatuto da prova: provada; a confirmação recusada é creditação, não validade", "Errata ao lado (v391): as frases de época",
                                "a confirmação que eu proibi é de creditação e não de validade", "A Fundação: a superposição é a passagem (a cláusula Ágape)"],
                         "en": ["The status of the proof (v391).", "The status of the proof: proved; the refused confirmation is accreditation, not validity", "Erratum beside (v391): the period sentences",
                                "a confirmação que eu proibi é de creditação e não de validade", "The Foundation: the superposition is the passage (the Agape clause)"]},
       "artigo_nao": {"pt": ["NÃO selou: o que segue é o enunciado", "não selado nesta rodada"], "en": ["did NOT seal: what follows is the statement", "not sealed in this run"]},
       "toc": {"pt": ["O estatuto da prova: provada", "v384 a v391", "A Fundação: a superposição é a passagem"], "en": ["The status of the proof: proved", "v384 to v391", "The Foundation: the superposition is the passage"]},
       "md_carimbo": "**Versão v391**", "md_estatuto": "O estatuto da prova (v391, 07/10/2026)", "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v391.json"))}
assert esp["veredito_v391_do_ensaio_sem_carimbo"].startswith("TGL_ESTATUTO_DA_PROVA_V391__PROVED_AS_LOGICAL_CLOSURE__") and esp["selo_registros_v390"]["fundacao_v390"]
out = os.path.join(HERE, "ESPERADOS_v391.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v391:", esp["candidato_sha16"], "| vereditos v390 pinados:", len(esp["vereditos_v390"]), "| flags True v390:", len(esp["flags_true_v390"]))
