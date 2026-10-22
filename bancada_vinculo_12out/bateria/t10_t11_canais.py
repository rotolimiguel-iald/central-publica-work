# -*- coding: utf-8 -*-
# T10_F72_INVARIANTES + T11_NEFF -- os canais F7.2 (v2 + alias) e N_eff (duas linhas de Yp, sem escolha; controle anti-dupla-contagem
# sintetico na CPU) rodados na COPIA com a identidade canonica do manifesto da copia. Documental/sintetico; sem limite TGL, sem verossimilhanca.
# Porte parametrizado de H_BANCADA\scripts\canais_f72_neff.py.
# uso: t10_t11_canais.py <candidate> <saida.json>
import datetime, hashlib, json, re, sys, time
from pathlib import Path
cand, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.dont_write_bytecode = True
sys.path.insert(0, str(cand))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def strip_paths(o):
    if isinstance(o, dict):
        return {k: strip_paths(v) for k, v in o.items() if k != "path"}
    if isinstance(o, list):
        return [strip_paths(x) for x in o]
    return o


def cj(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


PROIBIDO = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED|\\bconfirmad[oa]s?\\b", re.I)
from bancada import canonical, neutrino_canal_v2, neutrino_canal, neff_canal
assert Path(canonical.__file__).resolve().is_relative_to(cand)
res = dict(teste="T10_F72_INVARIANTES+T11_NEFF", quando=datetime.datetime.now().isoformat(timespec="seconds"))
v2 = neutrino_canal_v2.canal()
v1 = neutrino_canal.canal()
rows = v2["rows"]
f72 = {
    "overall_verdict": v2["overall_verdict"], "mode": v2["mode"], "served_contract": v2["served_contract"], "n_rows": len(rows),
    "all_rows_SEM_LIMITE_TGL": all(r["verdict"] == "SEM_LIMITE_TGL" for r in rows),
    "all_tau_star_limit_null": all(r["tau_star_limit_s"] is None for r in rows),
    "all_mapping_OPEN": all(r["operator_mapping_to_TGL"] == "OPEN" for r in rows),
    "likelihood_available": v2["likelihood_available"], "gate_effect": v2["gate_effect"],
    "legacy_rows_equal_v2": v1["rows"] == rows,
    "forbidden_word_in_output": bool(PROIBIDO.search(json.dumps(v2, ensure_ascii=False, default=str))),
    "rows_digest_sem_caminho_sha256": sha(cj(strip_paths(rows))),
    "canonical_version": v2["current_contract"]["canonical_version"], "um_py_sha256": v2["current_contract"]["um_py_sha256"],
    "canonical_manifest_sha256": v2["current_contract"]["canonical_manifest_sha256"], "beta_tgl": v2["current_contract"]["beta_tgl"],
}
res["F72"] = f72
n = neff_canal.canal()
neff = {"mode": n["mode"], "beta_runtime": n["beta_runtime"], "um_py_sha256": n["um_py_sha256"], "delta_N_eff": n["delta_N_eff"],
        "N_base": n["N_base"], "dN_eff_dbeta": n["dN_eff_dbeta"], "escolha_Yp": n["escolha_Yp"], "veredito": n["veredito"], "gate_effect": n["gate_effect"],
        "n_opcoes_CMB_SPA_Yp": len(n["opcoes_CMB_SPA_Yp"]), "obsolete_frozen_row_suppressed": n["obsolete_frozen_row_suppressed"]}
t = time.perf_counter()
ctrl = neff_canal.controle_anti_dupla_contagem(dispositivo="cpu")
neff["controle_anti_dupla_contagem"] = {k: ctrl[k] for k in ("passou", "razao_E_menos_1", "tolerancia", "mode", "observed_data_used")}
neff["controle_seconds"] = time.perf_counter() - t
res["NEFF"] = neff
t10 = f72["all_rows_SEM_LIMITE_TGL"] and f72["all_tau_star_limit_null"] and f72["all_mapping_OPEN"] and (f72["likelihood_available"] is False) \
    and f72["legacy_rows_equal_v2"] and not f72["forbidden_word_in_output"] and f72["gate_effect"] == "NONE"
t11 = neff["veredito"] == "NENHUM" and neff["escolha_Yp"] == "OPEN_X16_NO_SELECTION" and neff["n_opcoes_CMB_SPA_Yp"] == 2 \
    and neff["obsolete_frozen_row_suppressed"] is True and ctrl["passou"] is True and ctrl["observed_data_used"] is False
res["T10"] = "PASSA" if t10 else "FALHA"
res["T11"] = "PASSA" if t11 else "FALHA"
res["veredito"] = "PASSA" if (t10 and t11) else "FALHA"
with out.open("x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, allow_nan=False, default=str)
print(json.dumps({k: res[k] for k in ("veredito", "T10", "T11")}), json.dumps({"rows": f72["n_rows"], "digest": f72["rows_digest_sem_caminho_sha256"][:16],
      "neff_veredito": neff["veredito"], "controle": neff["controle_anti_dupla_contagem"]["razao_E_menos_1"]}, default=str))
sys.exit(0 if res["veredito"] == "PASSA" else 1)
