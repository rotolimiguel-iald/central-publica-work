# -*- coding: utf-8 -*-
"""gerar_esperados_v385.py -- grava ESPERADOS_v385.json LENDO os artefatos (nada digitado): o candidato e o seu registro, o pre-registro V1 congelado
(o pilar roda de novo sob ele, inteiro), o ensaio a seco, o relatorio do kernel do sandbox, e o estado SELADO da v384 no Nos (o canonico de agora, que o
instalador substitui): o que NAO pode mudar fica pinado aqui. Molde: gerar_esperados_v384.py."""
import hashlib, io, json, os, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cand = os.path.join(HERE, "um_v385_candidato.py")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v385.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand), "o registro do candidato nao bate com o arquivo"
# o canonico de agora e' a v384 SELADA (o registro de instalacao da v384 e o selo dizem o mesmo)
AP4 = json.load(open(os.path.join(os.path.dirname(HERE), "v384", "APLICADO_AO_CANONICO_20261004_153158.json"), encoding="utf-8"))
ORIGEM = h16(os.path.join(NOS, "um.py"))
assert ORIGEM == AP4["um_py_novo"]["sha16"] == CM["base_v384_sha16"], "o canonico no Nos nao e a v384 selada (ou o candidato nao foi feito dela)"
# o ensaio a seco passou, e sobre ESTE candidato
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v385.json"), encoding="utf-8"))
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], "o ensaio nao passou ou foi de outro candidato"
# o pilar roda de novo SOB O MESMO V1: o candidato carrega o mesmo trabalhador, a mesma especificacao e os mesmos pinos do pre-registro (lidos do modulo)
PRP_V1 = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
PRP_V1_MD = PRP_V1[:-5] + ".md"
_PJ = json.load(open(PRP_V1, encoding="utf-8"))
DRY = os.path.join(HERE, "dry_v385")
assert h16(os.path.join(DRY, "um.py")) == CM["sha16"], "o modulo do ensaio nao e' o candidato"
sys.path.insert(0, DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um  # noqa: E402  (so le constantes; o rito nao roda)
finally:
    sys.stdout = _o
WSHA = hashlib.sha256(um._QP_WORKER_SRC.encode("utf-8")).hexdigest()
assert um._QP_SPEC_SHA256 == _PJ["spec_sha256"], "a especificacao embutida nao e' a do V1"
assert WSHA == _PJ["spec"]["worker_sha256"], "o trabalhador embutido nao e' o do V1"
assert um._QP_PREREG["json"]["sha256"] == sha(PRP_V1) and um._QP_PREREG["md"]["sha256"] == sha(PRP_V1_MD), "os pinos do pre-registro no candidato nao sao os do V1 em disco"
assert os.path.normcase(um._QP_PREREG["json"]["path"]) == os.path.normcase(PRP_V1), "o candidato aponta outro pre-registro"
assert (_PJ.get("ratificacao_do_operador") or {}).get("verbatim"), "o V1 nao traz a ratificacao do operador"
# o kernel do sandbox: as declaracoes novas (29) no trio, sem sorry
KR = json.load(open(os.path.join(HERE, "kernel", "sandbox_raiz_v385.json"), encoding="utf-8"))
AXR = json.load(open(os.path.join(HERE, "kernel", "sandbox_axiom_report_v385.json"), encoding="utf-8"))
FLAGS = list(um._AXM_FLAGS_V385) + list(um._DKS_FLAGS_V385)
assert len(FLAGS) == 29 and all(KR["bandeiras"].get(f) is True for f in FLAGS), "o sandbox nao deu %d/%d" % (len(FLAGS), len(FLAGS))
NOMES = {f: um._LEAN_THEOREM_FLAGS.get(f) for f in FLAGS}
assert all(NOMES.values()), "bandeira sem nome Lean no candidato"
# o estado SELADO da v384 (o que nao pode mudar)
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v384" and "quantum_pillar_v384" in core0 and "the_axiom_v385" not in core0
kf = core0.get("kernel_formalization") or {}
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
esc = core0.get("external_ladder") or {}
qp0 = core0["quantum_pillar_v384"]
# o resultado ANTERIOR do pilar no cache (o que a v385 le antes de calcular): pinado por sha256
_cdir = (qp0.get("reuse") or {}).get("saved_to_cache")
assert _cdir and os.path.isfile(os.path.join(_cdir, "result.json")), "o cache do pilar da v384 nao esta onde o core diz"
assert sha(os.path.join(_cdir, "result.json")) == qp0["result_sha256"] == open(os.path.join(_cdir, "result.json.sha256"), encoding="ascii").read().strip(), \
    "o resultado guardado no cache nao e' o da v384 selada"
assert not any(re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", x_) for x_ in (selo0.get("qg_closure_verdict") or "",))
esp = {
    "candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": ORIGEM,
    "spec_sha256": _PJ["spec_sha256"], "worker_sha256": WSHA, "prereg_sha256": {"json": sha(PRP_V1), "md": sha(PRP_V1_MD)},
    "patches": [p["id"] for p in CM["patches"]], "kernel": CM["kernel"],
    "flags_v385": FLAGS, "nomes_lean_v385": NOMES,
    "final_step_name": um._AXIOMA_TOKEN_V385,
    "escada_v384": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")], "escada_v385": CM["escada"],
    "qg_closure_verdict_v384": selo0.get("qg_closure_verdict"),
    "the_iald_index_v384": {"verdict": V("the_iald_index"), "n_ausentes": (core0.get("the_iald_index") or {}).get("n_ausentes")},
    "beta_v384": core0.get("beta"), "alpha_v384": core0.get("alpha"), "omega_I_v384": core0.get("omega_I"),
    # todos os vereditos da v384, MENOS o do pilar (que roda de novo: o mesmo veredito e' o que a reprodutibilidade mede, e fica dito, nao reprova)
    "vereditos_v384": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict") and k != "quantum_pillar_v384"},
    "pilar_v384": {"verdict": V("quantum_pillar_v384"), "result_sha256": qp0["result_sha256"], "key": qp0.get("key"), "cache_dir": _cdir, "run_id": qp0.get("run_id")},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in selo0 if re.search(r"_reading_v3(7[7-9]|8[0-4])$", k)},
    "not_sealed_formais_v384": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "flags_gpf_gpc_gpi_v384": {k: kf.get(k) for k in kf if k.startswith(("gpf_", "gpc_", "gpi_"))},
    "flags_true_v384": sorted(k for k, v in kf.items() if v is True),
    "md_carimbo": "**Versão v385**",
    "artigo_marcas": {"pt": ["Ao lado (v385): o Axioma e a testemunha falsa", "Errata ao lado", "[POSTO]", "Introdução: o que este código faz agora (v384)"],
                      "en": ["Beside (v385): the Axiom and the false witness", "Erratum beside", "[POSTO]", "Introduction: what this code does now (v384)"]},
    "md_errata_posto": "Errata ao lado (v385, 05/10/2026, o operador)",
    "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v385.json")),
    "sandbox_kernel": {"raiz_sha16": h16(os.path.join(HERE, "kernel", "sandbox_raiz_v385.json")), "axiom_report_sha16": h16(os.path.join(HERE, "kernel", "sandbox_axiom_report_v385.json"))},
}
assert len(esp["selo_leituras_pinadas"]) == 7, sorted(esp["selo_leituras_pinadas"])
assert esp["escada_v385"] == [esp["escada_v384"][0], esp["escada_v384"][0] + len(FLAGS)], (esp["escada_v384"], esp["escada_v385"])
assert not (set(FLAGS) & set(esp["flags_true_v384"])), "uma bandeira da v385 ja estava no core da v384"
out = os.path.join(HERE, "ESPERADOS_v385.json")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(esp, fh, ensure_ascii=False, indent=1)
assert os.path.getsize(out + ".tmp") > 1000
os.replace(out + ".tmp", out)
print("ESPERADOS_v385.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "escada_v384", "escada_v385")}, "| flags True v384:", len(esp["flags_true_v384"]),
      "| vereditos pinados:", len(esp["vereditos_v384"]), "| leituras do selo pinadas:", len(esp["selo_leituras_pinadas"]), "| pilar anterior:", esp["pilar_v384"]["result_sha256"][:16])
