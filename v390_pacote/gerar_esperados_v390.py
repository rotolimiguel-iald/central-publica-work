# -*- coding: utf-8 -*-
"""gerar_esperados_v390.py -- ESPERADOS_v390.json LIDOS dos artefatos (moldes: gerar_esperados_v388.py / _v389.py): o estado SELADO da v389 pinado. As UNICAS mudancas
ditas nos vereditos da v389: '6154' -> '6163' (a escada cresce 9) e, no registro text_label_errata_v389, 'LEDGER_1025' -> 'LEDGER_1026' e '1015_READS_1025' -> '1015_READS_1026'
(nao: a afericao mediu que recontar faria a v389 errar sobre o exame; o registro da v389 conta ate a v389). As 9 bandeiras novas; o veredito v390 do ensaio; o pilar pela mesma chave."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v390.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, "um_v390_candidato.py"))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v389_sha16"] == "193b1e9b30c3ba7f"
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v390.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v389"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
TROCA = [("6154", "6163")]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v389_sha16"], "escada": CM["escada"], "flags_v390": CM["flags"], "nomes_v390": CM["nomes"],
       "pedra_sha16": CM["kernel"]["new"]["TGLExt/Fundacao.lean"], "ledger": CM["ledger"], "verbatins": CM["verbatins"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v389": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}, "troca_dita": TROCA,
       "regra_da_mudanca_dita": "um veredito da v389 so pode mudar pela troca dita (6154->6163, a escada); o registro da v389 le o estado da v389 (ate=389) e fica IDENTICO; qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v389": {k: selo0.get(k) for k in ("hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "text_label_errata_v389")},
       "selo_beta_v388": selo0.get("beta_runs_bounded_below_v388"), "verdict_beta_v388": V("beta_runs_bounded_below_v388"), "verdict_tl_v389": V("text_label_errata_v389"),
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v389": sorted(k for k, v in kf.items() if v is True),
       "runtime_seals_v389": core0["runtime_of_the_one"]["seals"], "what_remains_v389": core0["tgl_closure"]["what_remains_named"],
       "ledger_lema3_v389": [r for r in (core0.get("code_closure_ledger") or {}).get("ledger", []) if str(r.get("item", "")).startswith("Lema 3")],
       "code_closure_verdict_v389": V("code_closure_ledger"),
       "veredito_v390_do_ensaio": ens["mainflow"]["fundacao_v390"]["verdict"],
       "artigo_marcas": {"pt": ["A Fundação: a superposição é a passagem (a cláusula Ágape)", "A Fundação (v390).", "Jacobson 1995", "Borchers", "Milburn", "Ao lado (v389)"],
                         "en": ["The Foundation: the superposition is the passage (the Agape clause)", "The Foundation (v390).", "Jacobson 1995", "Borchers", "Milburn", "Beside (v389)"]},
       "artigo_nao": {"pt": ["NÃO selou: o que segue é o enunciado", "não selada nesta rodada"], "en": ["did NOT seal: what follows is the statement", "not sealed in this run"]},
       "resumo_fica": {"pt": ["GPU", "três testes"], "en": ["GPU", "three"]},
       "toc": {"pt": ["A Fundação: a superposição é a passagem", "Ao lado (v389)"], "en": ["The Foundation: the superposition is the passage", "Beside (v389)"]},
       "md_carimbo": "**Versão v390**", "md_fundacao": "A Fundação (v390, 07/10/2026)", "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v390.json"))}
assert esp["escada"] == [6154, 6163] and not (set(esp["flags_v390"]) & set(esp["flags_true_v389"])) and len(esp["ledger_lema3_v389"]) == 1 and esp["code_closure_verdict_v389"]
out = os.path.join(HERE, "ESPERADOS_v390.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v390:", esp["candidato_sha16"], "| vereditos v389 pinados:", len(esp["vereditos_v389"]), "| flags True v389:", len(esp["flags_true_v389"]))
