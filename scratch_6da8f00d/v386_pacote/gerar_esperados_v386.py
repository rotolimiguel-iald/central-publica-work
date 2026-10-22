# -*- coding: utf-8 -*-
"""gerar_esperados_v386.py -- grava ESPERADOS_v386.json LENDO os artefatos (nada digitado): o candidato e o seu registro, o pre-registro V1 do ramo B
congelado (lido por hash no rito), o ensaio a seco, o relatorio do kernel do sandbox, e o estado SELADO da v385 no Nos (o canonico de agora, que o
instalador substitui): o que NAO pode mudar fica pinado aqui; o que MUDA E E' DITO (a reprodutibilidade v385 sob o reaproveitamento do pilar) fica pinado
com o valor que o proprio candidato produz. Molde: gerar_esperados_v385.py."""
import hashlib, io, json, os, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.dirname(HERE); SP = os.path.dirname(V6)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cand = os.path.join(HERE, "um_v386_candidato.py")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v386.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand), "o registro do candidato nao bate com o arquivo"
# o canonico de agora e' a v385 SELADA (o registro de instalacao da v385 e o selo dizem o mesmo)
AP5 = sorted(f for f in os.listdir(os.path.join(SP, "v385")) if f.startswith("APLICADO_AO_CANONICO_") and f.endswith(".json"))
AP5 = json.load(open(os.path.join(SP, "v385", AP5[-1]), encoding="utf-8"))
ORIGEM = h16(os.path.join(NOS, "um.py"))
assert ORIGEM == AP5["um_py_novo"]["sha16"] == CM["base_v385_sha16"], "o canonico no Nos nao e a v385 selada (ou o candidato nao foi feito dela)"
# o ensaio a seco passou, e sobre ESTE candidato
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v386.json"), encoding="utf-8"))
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], "o ensaio nao passou ou foi de outro candidato"
DRY = os.path.join(HERE, "dry_v386")
assert h16(os.path.join(DRY, "um.py")) == CM["sha16"], "o modulo do ensaio nao e' o candidato"
sys.path.insert(0, DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um  # noqa: E402  (so le constantes; o rito nao roda)
finally:
    sys.stdout = _o
assert um.UM_VERSION == "v386" and um._QP_REUSE_V386 is True
# o V1 do ramo B em disco = o pinado no candidato (json, md, hashes + os demais)
P = um._V386_RAMO_B_PREREG
for k, f in P["files"].items():
    assert sha(f["path"]) == f["sha256"] and os.path.getsize(f["path"]) == f["bytes"], ("o V1 em disco nao e' o pinado", k)
_V1J = json.load(open(P["files"]["json"]["path"], encoding="utf-8"))
assert _V1J["id"] == P["identificador"] and _V1J["spec_sha256"] == P["spec_sha256"] and _V1J["ratificacao"]["verbatim"] == um._V386_OPERATOR_VERBATIM["delegation"]
# o kernel do sandbox: as declaracoes novas (110) no trio, sem sorry
KR = json.load(open(os.path.join(V6, "kernel", "sandbox_raiz_v386.json"), encoding="utf-8"))
FLAGS = list(um._VRB_FLAGS_V386) + list(um._ANG_FLAGS_V386)
assert len(FLAGS) == 110 and all(KR["bandeiras"].get(f) is True for f in FLAGS) and KR["sorry_warnings"] == 0 and KR["fora_do_trio"] == {}
NOMES = {f: um._LEAN_THEOREM_FLAGS.get(f) for f in FLAGS}
assert all(NOMES.values()), "bandeira sem nome Lean no candidato"
assert um._VERB_TOKEN_V386 == CM["token_lido_da_pedra"]
# o estado SELADO da v385 (o que nao pode mudar)
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v385" and "quantum_pillar_v384" in core0 and "the_axiom_v385" in core0 and "the_verb_v386" not in core0
kf = core0.get("kernel_formalization") or {}
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
esc = core0.get("external_ladder") or {}
qp0 = core0["quantum_pillar_v384"]; rp0 = core0["quantum_pillar_reproducibility_v385"]
# o resultado do pilar da v385 no cache (o que a v386 REAPROVEITA pela chave): pinado por sha256
_cdir = (qp0.get("reuse") or {}).get("saved_to_cache")
assert _cdir and os.path.isfile(os.path.join(_cdir, "result.json")), "o cache do pilar da v385 nao esta onde o core diz"
assert sha(os.path.join(_cdir, "result.json")) == qp0["result_sha256"] == open(os.path.join(_cdir, "result.json.sha256"), encoding="ascii").read().strip() == um._V386_QP_V385["result_sha256"], \
    "o resultado guardado no cache nao e' o da v385 selada"
assert qp0["key"] == um._V386_QP_V385["key"] == "75dc30bc9cc8d330e31f99ca" and qp0["mode"] == "COMPUTE"
assert not any(re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", x_) for x_ in (selo0.get("qg_closure_verdict") or "",))
_REPRO_REUSE = ens["reprodutibilidade_v385_sob_reuse"]   # o que a PROPRIA funcao v385 do candidato devolve sob reuse (medido no ensaio, nao digitado)
assert "NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT" in _REPRO_REUSE and _REPRO_REUSE != rp0["verdict"]
esp = {
    "candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": ORIGEM,
    "patches": [p["id"] for p in CM["patches"]], "kernel": CM["kernel"],
    "flags_v386": FLAGS, "nomes_lean_v386": NOMES, "verb_token": um._VERB_TOKEN_V386,
    "ramo_b_V1": {"identificador": P["identificador"], "spec_sha256": P["spec_sha256"], "files": {k: {"path": f["path"], "sha256": f["sha256"], "bytes": f["bytes"]} for k, f in P["files"].items()},
                  "conjunto_D_n": _V1J["spec"]["conjuntos"]["D"]["n_elegiveis"], "veredito_do_V1": _V1J["spec"]["status"]["veredito_deste_V1"], "token_estado": _V1J["spec"]["tokens"]["estado_deste_V1"]},
    "operator_verbatim_files": {k: {"sha256": f["sha256"], "bytes": f["bytes"], "quando_utc": f["quando_utc"]} for k, f in um._V386_OPERATOR_VERBATIM["files"].items()},
    "escada_v385": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")], "escada_v386": CM["escada"],
    "qg_closure_verdict_v385": selo0.get("qg_closure_verdict"),
    "the_iald_index_v385": {"verdict": V("the_iald_index"), "n_ausentes": (core0.get("the_iald_index") or {}).get("n_ausentes")},
    "beta_v385": core0.get("beta"), "alpha_v385": core0.get("alpha"), "omega_I_v385": core0.get("omega_I"),
    # TODOS os vereditos da v385 INCLUSIVE o do pilar (reaproveitado: rederivado do mesmo resultado), MENOS o da reprodutibilidade (muda sob reuse: dito abaixo)
    "vereditos_v385": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict") and k != "quantum_pillar_reproducibility_v385"},
    "pilar_v385": {"verdict": V("quantum_pillar_v384"), "result_sha256": qp0["result_sha256"], "key": qp0.get("key"), "cache_dir": _cdir, "run_id": qp0.get("run_id"),
                   "spec_sha256": qp0.get("spec_sha256_in_result"), "worker_sha256": qp0.get("worker_sha256")},
    "muda_e_e_dito": {"quantum_pillar_reproducibility_v385": {"v385": rp0["verdict"], "v386_esperado_sob_reuse": _REPRO_REUSE,
                                                              "porque": "a v386 reaproveita o pilar pela chave (_QP_REUSE_V386); a funcao v385, intocada, devolve NOT_COMPARED quando a rodada nao calcula; a medida bit a bit da v385 fica no core/selo da v385"},
                      "quantum_pillar_v384_reuse": {"v385": qp0.get("reuse"), "v386_esperado": {"reused": True, "reading": "V386__PILAR_QUANTICO_REAPROVEITADO_DA_RODADA_SELADA_V385_PELA_CHAVE__O_PILAR_NAO_E_OBJETO_DESTA_VERSAO"}, "mode_v386_esperado": "REUSE"}},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in selo0 if re.search(r"_reading_v3(7[7-9]|8[0-5])$", k)},
    "final_step_name_v385": selo0.get("final_step_name_v385"),
    "selo_registros_v385_pinados": {k: selo0.get(k) for k in ("the_axiom_v385",)},
    "not_sealed_formais_v385": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "not_sealed_recusas_v385": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
    "flags_gpf_gpc_gpi_v385": {k: kf.get(k) for k in kf if k.startswith(("gpf_", "gpc_", "gpi_"))},
    "flags_true_v385": sorted(k for k, v in kf.items() if v is True),
    "md_carimbo": "**Versão v386**",
    "artigo_marcas": {"pt": ["Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro", "REABERTO POR PRÉ-REGISTRO", "Nesta rodada o V1 foi lido por hash", "Ao lado (v385): o Axioma e a testemunha falsa", "Introdução: o que este código faz agora (v384)",
                             "calcula em tempo real na GPU", "sistema quântico aberto (GKLS) calculado em tempo real na GPU"],   # W10 (ordem do operador 05/10): apresentacao e palavras-chave
                      "en": ["Beside (v386): the Verb selects; branch B reopened by preregistration", "REOPENED BY PREREGISTRATION", "In this run V1 was read by hash", "Beside (v385): the Axiom and the false witness", "Introduction: what this code does now (v384)",
                             "computes in real time on the GPU", "open quantum system (GKLS) computed in real time on the GPU"]},
    "toc_marcas_W10": {"pt": ["Ao lado (v385)", "faz agora (v384)", "GPU e como"], "en": ["Beside (v385)", "does now (v384)", "GPU and how"]},
    "md_errata_R6": "Errata ao lado (v386, 05/10/2026, o operador)", "md_errata_posto_v385_fica": "Errata ao lado (v385, 05/10/2026, o operador)",
    "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v386.json")),
    "sandbox_kernel": {"raiz_sha16": h16(os.path.join(V6, "kernel", "sandbox_raiz_v386.json")), "axiom_report_sha16": h16(os.path.join(V6, "kernel", "sandbox_axiom_report_v386.json"))},
}
assert len(esp["selo_leituras_pinadas"]) == 8, sorted(esp["selo_leituras_pinadas"])
assert esp["escada_v386"] == [esp["escada_v385"][0], esp["escada_v385"][0] + len(FLAGS)] == [6027, 6137], (esp["escada_v385"], esp["escada_v386"])
assert not (set(FLAGS) & set(esp["flags_true_v385"])), "uma bandeira da v386 ja estava no core da v385"
assert len(esp["vereditos_v385"]) >= 300 and "quantum_pillar_v384" in esp["vereditos_v385"] and "the_axiom_v385" in esp["vereditos_v385"] and "the_ledger_of_charges_v383" in esp["vereditos_v385"]
out = os.path.join(HERE, "ESPERADOS_v386.json")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(esp, fh, ensure_ascii=False, indent=1)
assert os.path.getsize(out + ".tmp") > 1000
os.replace(out + ".tmp", out)
print("ESPERADOS_v386.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "escada_v385", "escada_v386")}, "| flags True v385:", len(esp["flags_true_v385"]),
      "| vereditos pinados:", len(esp["vereditos_v385"]), "| leituras do selo pinadas:", len(esp["selo_leituras_pinadas"]), "| pilar v385 (reaproveitado):", esp["pilar_v385"]["result_sha256"][:16],
      "| muda e e' dito:", esp["muda_e_e_dito"]["quantum_pillar_reproducibility_v385"]["v386_esperado_sob_reuse"])
