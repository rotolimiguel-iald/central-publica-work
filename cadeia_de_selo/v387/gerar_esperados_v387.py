# -*- coding: utf-8 -*-
"""gerar_esperados_v387.py -- grava ESPERADOS_v387.json LENDO os artefatos (nada digitado): o candidato e o seu registro, os dois V1 da Bancada (lidos por
hash no rito), o ensaio a seco, e o estado SELADO da v386 no Nos (o canonico de agora, que o instalador substitui): o que NAO pode mudar fica pinado aqui --
TODOS os vereditos da v386 (o pilar segue reaproveitado pela MESMA chave; a reprodutibilidade v385 segue NOT_COMPARED); a escada (6137); as bandeiras; as 9
leituras do selo; os nao-selados. Molde: gerar_esperados_v386.py."""
import hashlib, io, json, os, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cand = os.path.join(HERE, "um_v387_candidato.py")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v387.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand), "o registro do candidato nao bate com o arquivo"
ORIGEM = h16(os.path.join(NOS, "um.py"))
assert ORIGEM == CM["base_v386_sha16"] == "e30aac4e0e1096b1", "o canonico no Nos nao e a v386 selada (ou o candidato nao foi feito dela)"
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v387.json"), encoding="utf-8"))
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], "o ensaio nao passou ou foi de outro candidato"
DRY = os.path.join(HERE, "dry_v387")
assert h16(os.path.join(DRY, "um.py")) == CM["sha16"], "o modulo do ensaio nao e' o candidato"
sys.path.insert(0, DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um  # noqa: E402  (so le constantes; o rito nao roda)
finally:
    sys.stdout = _o
assert um.UM_VERSION == "v387" and um._QP_REUSE_V386 is True
V1 = {}
for nome, P in (("fase9", um._V387_FASE9_V1), ("fase8", um._V387_FASE8_V1)):
    for k, f in P["files"].items():
        assert sha(f["path"]) == f["sha256"] and os.path.getsize(f["path"]) == f["bytes"], ("o V1 em disco nao e' o pinado", nome, k)
    V1[nome] = {"identificador": P["identificador"], "spec_sha256": P["spec_sha256"], "funcao_sha256": P["funcao_sha256"],
                "files": {k: {"path": f["path"], "sha256": f["sha256"], "bytes": f["bytes"]} for k, f in P["files"].items()}}
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v386" and "the_verb_v386" in core0 and "three_stress_tests_v387" not in core0
kf = core0.get("kernel_formalization") or {}
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
esc = core0.get("external_ladder") or {}
qp0 = core0["quantum_pillar_v384"]
assert qp0["mode"] == "REUSE" and (qp0.get("reuse") or {}).get("reused") is True and qp0["key"] == "75dc30bc9cc8d330e31f99ca"
_cdir = (qp0.get("reuse") or {}).get("cache_dir")
assert _cdir and sha(os.path.join(_cdir, "result.json")) == qp0["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado pela v386"
esp = {
    "candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": ORIGEM, "patches": [p["id"] for p in CM["patches"]],
    "V1": V1, "verbatins": CM["verbatins"],
    "escada": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")],
    "qg_closure_verdict_v386": selo0.get("qg_closure_verdict"),
    "the_iald_index_v386": {"verdict": V("the_iald_index"), "n_ausentes": (core0.get("the_iald_index") or {}).get("n_ausentes")},
    "beta_v386": core0.get("beta"), "alpha_v386": core0.get("alpha"), "omega_I_v386": core0.get("omega_I"),
    "vereditos_v386": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")},
    "pilar_v386": {"verdict": V("quantum_pillar_v384"), "result_sha256": qp0["result_sha256"], "key": qp0.get("key"), "cache_dir": _cdir, "reuse_reading": qp0["reuse"]["reading"]},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in selo0 if re.search(r"_reading_v3(7[7-9]|8[0-6])$", k)},
    "selo_registros_v386_pinados": {k: selo0.get(k) for k in ("the_verb_v386", "ledger_errata_v386", "ramo_b_preregistration_v386", "verb_typing_stone_name_v386", "the_axiom_v385")},
    "not_sealed_formais_v386": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "not_sealed_recusas_v386": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
    "flags_gpf_gpc_gpi_v386": {k: kf.get(k) for k in kf if k.startswith(("gpf_", "gpc_", "gpi_"))},
    "flags_true_v386": sorted(k for k, v in kf.items() if v is True),
    "registros_v387": ["three_stress_tests_v387", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387"],
    "vereditos_v387_do_ensaio": {k: ens["mainflow"][k]["verdict"] for k in ("three_stress_tests_v387", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387")},   # C3: pinados do ensaio (o rito recalcula sobre o mesmo core)
    "md_carimbo": "**Versão v387**", "md_ao_lado_v387": "Ao lado (v387, 06/10/2026)", "md_errata_v386_fica": "Errata ao lado (v386, 05/10/2026, o operador)",
    "artigo_marcas": {"pt": ["Os três testes de estresse, conjuntos", "Ao lado (v387): a razão de Hubble e a era da radiação pré-registradas", "Ao lado (v386): o Verbo seleciona",
                             "retrodição sem ajuste", "um só teste de estresse conjunto", "três testes de estresse conjuntos"],
                      "en": ["The three stress tests, taken together", "Beside (v387): the Hubble ratio and the radiation era preregistered", "Beside (v386): the Verb selects",
                             "retrodiction without adjustment", "one joint stress test", "three joint stress tests"]},
    "artigo_nao_deve": {"pt": ["pós-dição declarada; zero", "pós-dição não ajustada"], "en": ["declared postdiction; zero", "an unadjusted postdiction"]},
    "toc_marcas": {"pt": ["testes de estresse", "Ao lado (v387)", "Ao lado (v386)", "Ao lado (v385)"], "en": ["stress tests, taken together", "Beside (v387)", "Beside (v386)", "Beside (v385)"]},
    "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v387.json")),
}
assert len(esp["selo_leituras_pinadas"]) == 9, sorted(esp["selo_leituras_pinadas"])
assert esp["escada"] == [6137, 6137] and len(esp["vereditos_v386"]) >= 300
assert not any(re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", x_) for x_ in esp["vereditos_v386"].values())
out = os.path.join(HERE, "ESPERADOS_v387.json")
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1))
assert os.path.getsize(out + ".tmp") > 1000
os.replace(out + ".tmp", out)
print("ESPERADOS_v387.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "escada")}, "| vereditos pinados:", len(esp["vereditos_v386"]),
      "| leituras do selo:", len(esp["selo_leituras_pinadas"]), "| flags True:", len(esp["flags_true_v386"]), "| pilar:", esp["pilar_v386"]["result_sha256"][:16])
