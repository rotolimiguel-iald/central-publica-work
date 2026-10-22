# -*- coding: utf-8 -*-
"""gerar_esperados_v384.py -- grava ESPERADOS_v384.json LENDO os artefatos (nada digitado): o candidato e o seu registro, o pre-registro congelado, o ensaio
a seco, e o estado SELADO da v383 no Nos (o canonico de agora, que o instalador substitui): o que NAO pode mudar fica pinado aqui."""
import hashlib, json, os, sys
if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (9a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand = os.path.join(HERE, "um_v384_candidato.py")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v384.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand), "o registro do candidato nao bate com o arquivo"
# a guarda da ratificacao (3a afericao): candidato de ENSAIO ou sem a ratificacao do operador NAO passa daqui
PRP_V1 = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
assert CM.get("ensaio") is False, "o candidato e' de ENSAIO -- nao sigo"
_RAT = CM.get("ratificacao_do_operador") or {}
assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
assert (_RAT.get("transcrito") or {}).get("de_teste") is False, "a ratificacao do candidato veio de transcrito de TESTE (ou nao diz qual) -- nao sigo"   # 8a afericao
_PJ = json.load(open(PRP_V1, encoding="utf-8"))
assert hashlib.sha256(open(PRP_V1, "rb").read()).hexdigest() == (CM.get("prereg_sha256") or {}).get("json"), "o pre-registro do candidato nao e' o V1 do lugar permanente"
assert _PJ["spec_sha256"] == CM["spec_sha256"] and _PJ["spec"]["worker_sha256"] == CM["worker_sha256"] and (_PJ.get("ratificacao_do_operador") or {}).get("verbatim") == _RAT["verbatim"], \
    "o trabalhador, a especificacao ou a ratificacao do candidato nao sao os do pre-registro V1"
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v384.json"), encoding="utf-8"))
assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], "o ensaio nao passou ou foi de outro candidato"
AP3 = json.load(open(os.path.join(os.path.dirname(HERE), "v383", "APLICADO_AO_CANONICO_20261002_200400.json"), encoding="utf-8"))
ORIGEM = h16(os.path.join(NOS, "um.py")); assert ORIGEM == AP3["um_py_novo"]["sha16"] == CM["base_v383_sha16"], "o canonico no Nos nao e a v383 selada"
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v383" and "quantum_pillar_v384" not in core0
kf = core0.get("kernel_formalization") or {}
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
esc = core0.get("external_ladder") or {}
esp = {
    "candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": ORIGEM, "spec_sha256": CM["spec_sha256"], "worker_sha256": CM["worker_sha256"],
    "prereg_sha256": CM["prereg_sha256"], "patches": [p["id"] for p in CM["patches"]],
    "qg_closure_verdict_v383": selo0.get("qg_closure_verdict"),
    "the_iald_index_v383": {"verdict": V("the_iald_index"), "n_ausentes": (core0.get("the_iald_index") or {}).get("n_ausentes")},
    "beta_v383": core0.get("beta"), "alpha_v383": core0.get("alpha"), "omega_I_v383": core0.get("omega_I"),
    "escada_v383": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")],
    "vereditos_v383": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")},
    "selo_leituras_pinadas": {k: selo0.get(k) for k in selo0 if k.endswith(("_reading_v377", "_reading_v378", "_reading_v379", "_reading_v380", "_reading_v381", "_reading_v383"))},
    "not_sealed_formais_v383": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []),
    "flags_gpf_gpc_v383": {k: kf.get(k) for k in kf if k.startswith(("gpf_", "gpc_", "gpi_"))},
    "n_flags_true_v383": sum(1 for k, v in kf.items() if v is True),
    "md_carimbo": "**Versão v384**",
    "artigo_marcas": {"pt": ["Introdução: o que este código faz agora (v384)", "Nota: o que se calcula na GPU e como"],
                      "en": ["Introduction: what this code does now (v384)", "Note: what is computed on the GPU and how"]},
    "ensaio_sha16": hashlib.sha256(open(os.path.join(HERE, "ensaio_a_seco_v384.json"), "rb").read()).hexdigest()[:16],
}
assert len(esp["selo_leituras_pinadas"]) >= 5, esp["selo_leituras_pinadas"].keys()
out = os.path.join(HERE, "ESPERADOS_v384.json")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(esp, fh, ensure_ascii=False, indent=1)
os.replace(out + ".tmp", out)
print("ESPERADOS_v384.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "escada_v383", "n_flags_true_v383")}, "| vereditos pinados:", len(esp["vereditos_v383"]),
      "| leituras do selo pinadas:", len(esp["selo_leituras_pinadas"]))
