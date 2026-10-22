# -*- coding: utf-8 -*-
# T09_NU4_REPLAY -- as 16 chamadas sinteticas do piloto F8.2.NU4 refeitas offline contra a COPIA, com a identidade canonica
# do manifesto da copia (um.py + selo do Nos alvo, lidos; codigo/fontes por hash). Sem HTTP, sem dado observado, sem sigma.
# Porte parametrizado de H_BANCADA\scripts\reproduzir_nu4.py. A comparacao e so de result (bit a bit).
# uso: t09_nu4_replay.py <candidate> <dir F8.2.NU4> <saida.json>
import datetime, hashlib, json, math, re, sys, time
from pathlib import Path
cand, NU4, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(cand))


def sha(b):
    return hashlib.sha256(b).hexdigest()


t0 = time.perf_counter()
from bancada import canonical, neutrino_contract
assert Path(canonical.__file__).resolve().is_relative_to(cand), canonical.__file__
reg = canonical.get_registry(cand)
rc = reg.check("T09_nu4_replay_inicio")
um_path = Path(reg.manifest["canonical"]["script"]["path"])
raw = um_path.read_bytes()
m = re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", raw, re.M)
beta_indep = float(m.group(1).decode()) * math.sqrt(math.e)
res = dict(teste="T09_NU4_REPLAY", quando=datetime.datetime.now().isoformat(timespec="seconds"), candidate=str(cand), um_py_do_manifesto=str(um_path),
           um_py_sha256=sha(raw), beta_independente=repr(beta_indep), beta_do_contrato=repr(rc["beta_tgl"]), beta_bit_a_bit=(rc["beta_tgl"] == beta_indep),
           canonical_version=rc["canonical_version"], deployment_id=rc["deployment_id"], calls=[])


def maxdiff(a, b, path=""):
    if isinstance(a, dict):
        assert set(a) == set(b), (path, set(a) ^ set(b))
        r = [maxdiff(a[k], b[k], path + "." + k) for k in a]
        return (max([x[0] for x in r] or [0.0]), max([x[1] for x in r] or [0.0]))
    if isinstance(a, list):
        assert len(a) == len(b), path
        r = [maxdiff(x, y, path + "[]") for x, y in zip(a, b)]
        return (max([x[0] for x in r] or [0.0]), max([x[1] for x in r] or [0.0]))
    if isinstance(a, (int, float)) and not isinstance(a, bool):
        d = abs(float(a) - float(b))
        s = max(abs(float(a)), abs(float(b)))
        return (d, d / s if s else 0.0)
    assert a == b, (path, a, b)
    return (0.0, 0.0)


for f in sorted(NU4.glob("CALL_*.json")):
    rec = json.loads(f.read_bytes())
    req, resp = rec["request"], rec["response"]
    got = neutrino_contract.simulate(req)
    da, dr = maxdiff(got["result"], resp["result"])
    res["calls"].append(dict(call=f.name, call_sha256=sha(f.read_bytes()), channel=req["channel"], identical=(got["result"] == resp["result"]),
                             max_abs_diff=da, max_rel_diff=dr, beta_tgl_same=(got["beta_tgl"] == resp["beta_tgl"]),
                             manifest_same_as_10out=(got["canonical"]["canonical_manifest_sha256"] == resp["canonical"]["canonical_manifest_sha256"]),
                             synthetic=got["synthetic"], nature_sigma=got["nature_sigma"], gate_effect=got["gate_effect"]))
rc2 = reg.check("T09_nu4_replay_fim")
res["manifesto_estavel"] = rc2["canonical_manifest_sha256"] == rc["canonical_manifest_sha256"]
res["n_calls"] = len(res["calls"])
res["n_identical"] = sum(c["identical"] for c in res["calls"])
res["todas_sinteticas_sem_sigma"] = all(c["synthetic"] and c["nature_sigma"] is None and c["gate_effect"] == "NONE" for c in res["calls"])
res["nota"] = "manifest_same_as_10out e informativo: muda a cada geracao B(n); o que tem de ser identico e o result"
res["veredito"] = "PASSA" if (res["n_calls"] == 16 and res["n_identical"] == 16 and res["beta_bit_a_bit"] and res["manifesto_estavel"] and res["todas_sinteticas_sem_sigma"]) else "FALHA"
res["seconds"] = time.perf_counter() - t0
res["scope"] = "SYNTHETIC_REPRODUCTION_OF_INSTALLED_PILOT; no observed data, no sigma, gate NONE"
with out.open("x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, allow_nan=False)
print(json.dumps({k: res[k] for k in ("veredito", "n_calls", "n_identical", "beta_bit_a_bit", "manifesto_estavel", "canonical_version", "seconds")}, ensure_ascii=False))
sys.exit(0 if res["veredito"] == "PASSA" else 1)
