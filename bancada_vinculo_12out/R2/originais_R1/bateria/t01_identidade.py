# -*- coding: utf-8 -*-
# T01_IDENTIDADE -- os pinos do contrato canonico da COPIA (candidate) contra o Nos alvo, com beta em runtime bit a bit.
# Porte parametrizado de exame_12out\H_BANCADA\scripts\fidelidade.py (12/10). Le bytes; nunca importa nem roda o um.py.
# uso: t01_identidade.py <candidate> <nos> <versao> <saida.json>
import datetime, hashlib, json, math, re, sys
from pathlib import Path
cand, nos, versao, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4])
sys.dont_write_bytecode = True
sys.path.insert(0, str(cand))
from bancada import canonical  # o canonical.py INSTALADO na copia
assert Path(canonical.__file__).resolve().is_relative_to(cand), canonical.__file__


def sha(b):
    return hashlib.sha256(b).hexdigest()


raw = (nos / "um.py").read_bytes()
txt = raw.decode("utf-8-sig")
m = list(re.finditer(r"^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([^\r\n#]+)", txt, re.M))
v = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt, re.M)
falhas = []
if len(m) != 1:
    falhas.append("alpha: %d linhas nao indentadas" % len(m))
alpha = float(m[0].group(1).strip()) if m else float("nan")
beta = alpha * math.sqrt(math.e)
selo_raw = (nos / "um_absoluto_selo.json").read_bytes()
reg = canonical.get_registry(cand)
rc = reg.check("T01_identidade")
man = json.loads((cand / "canonical_contracts.json").read_bytes())
checks = {
    "registro_ok": rc["ok"] is True,
    "versao_do_contrato_e_a_alvo": rc["canonical_version"] == versao,
    "UM_VERSION_no_um_py_e_a_alvo": (v.group(1) if v else None) == versao,
    "um_py_sha256_e_o_do_nos": rc["um_py_sha256"] == sha(raw),
    "selo_sha256_e_o_do_nos": rc["seal_sha256"] == sha(selo_raw),
    "selo_pina_o_um_py": json.loads(selo_raw)["sha256"]["um.py"] == sha(raw),
    "beta_runtime_bit_a_bit": rc["beta_tgl"] == beta,
    "alpha_igual": rc["alpha"] == alpha,
    "manifesto_sha256_igual_ao_arquivo": rc["canonical_manifest_sha256"] == sha((cand / "canonical_contracts.json").read_bytes()),
    "n_code_pinados": len(man["code"]),
    "n_sources_pinados": len(man["sources"]),
    "mu_do_rito_presente": bool(rc.get("mu_do_rito")),
    "gate_effect_NONE": rc.get("gate_effect") == "NONE",
}
lit_beta = sorted(str(p.relative_to(cand)) for p in (cand / "bancada").glob("*.py") if re.search(r"0\.01203", p.read_text(encoding="utf-8")))
lit_alpha = sorted(str(p.relative_to(cand)) for p in (cand / "bancada").glob("*.py") if re.search(r"7\.2973525693|137\.035999", p.read_text(encoding="utf-8")))
checks["sem_literal_de_beta_em_bancada_py"] = lit_beta == []
checks["sem_literal_de_alpha_em_bancada_py"] = lit_alpha == []
for k, val in checks.items():
    if val is False:
        falhas.append(k)
res = dict(teste="T01_IDENTIDADE", quando=datetime.datetime.now().isoformat(timespec="seconds"), candidate=str(cand), nos=str(nos), versao=versao,
           um_py_sha256=sha(raw), um_py_bytes=len(raw), selo_sha256=sha(selo_raw), alpha=alpha, alpha_linha=(txt[:m[0].start()].count("\n") + 1 if m else None),
           beta_runtime=repr(beta), beta_do_contrato=repr(rc["beta_tgl"]), deployment_id=rc["deployment_id"], checks=checks,
           literais=dict(beta=lit_beta, alpha=lit_alpha), falhas=falhas, veredito=("PASSA" if not falhas else "FALHA"),
           scope="IDENTIDADE; NAO E LEITURA FISICA", gate_effect="NONE")
with out.open("x", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ("veredito", "deployment_id", "um_py_sha256", "beta_runtime", "falhas")}, ensure_ascii=False))
sys.exit(0 if not falhas else 1)
