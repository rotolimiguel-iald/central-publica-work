"""Generate masked synthetic H0DN/BG1 blocks and call only the frozen scorer.

Labels/seeds stay in CUSTODY_SECRET.json until the coordinator acknowledges
SCORES_COMMIT.json. No observed local centers are read.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import secrets
import subprocess
import sys
import tempfile
import time

import numpy as np
from scipy import linalg
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SCORER = BASE / "estimator.py"
ESTIMATOR = BASE / "estimator_frozen.npz"
FREEZE = BASE / "FREEZE.json"
COUNT = 100000
BATCH = 25000
SHIFT = 5.0

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def array_sha(array):
    arr = np.ascontiguousarray(array, dtype="<f8")
    return hashlib.sha256(arr.tobytes()).hexdigest()

def write_new(path, value):
    path = Path(path)
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")
    with path.open("xb") as out:
        out.write(raw)

def verify_freeze():
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    for row in freeze["files"]:
        if sha(row["path"]) != row["sha256"]:
            raise ValueError("frozen_input_changed:" + row["path"])
    return freeze

def geometry():
    with np.load(ESTIMATOR, allow_pickle=False) as src:
        est = {key: src[key] for key in src.files}
    with np.load(BASE / "network/network.npz", allow_pickle=False) as src:
        c = src["c_cepheid"].copy()
    C = est["C_joint"]
    values, vectors = linalg.eigh(C)
    tol = 64*np.finfo(float).eps*len(C)*values[-1]
    if values[0] < -tol:
        raise ValueError("joint_covariance_indefinite")
    positive = values > tol
    factor = vectors[:, positive] * np.sqrt(values[positive])
    if not np.allclose(factor@factor.T, C, atol=2e-12, rtol=2e-11):
        raise ValueError("joint_factorization_failed")
    dims = est["weights"].shape[1]
    directions = []
    for index, weights in enumerate(est["weights"]):
        response = np.concatenate([weights, -est["gradient_h"]])
        direction = factor.T @ response / est["sd_null"][index]
        if abs(direction@direction-1) > 2e-10:
            raise ValueError("importance_direction_not_unit")
        directions.append(direction)
    return est, c, factor, np.asarray(directions), dims

def make_secret():
    def key():
        return secrets.token_hex(8)
    seeds = {"ordinary_0":secrets.randbits(128), "ordinary_1":secrets.randbits(128),
             "importance_0":secrets.randbits(128), "importance_1":secrets.randbits(128)}
    cases = []
    for hypothesis in (0, 1):
        for fixed, random in [(0.,0.),(-.05,0.),(.05,0.),(0.,.01),(0.,.03),(0.,.05),(0.,.10)]:
            cases.append(dict(id=key(),kind="ordinary",hypothesis=hypothesis,
                              fixed_bias=fixed, random_sd=random,
                              seed_key=f"ordinary_{hypothesis}"))
    for index in (0, 1):
        cases.append(dict(id=key(),kind="importance",hypothesis=0,
                          model=index,fixed_bias=0.,random_sd=0.,seed_key=f"importance_{index}"))
    secrets.SystemRandom().shuffle(cases)
    return dict(seeds=seeds,cases=cases,count=COUNT,batch=BATCH,shift=SHIFT)

def generate():
    start = time.monotonic()
    verify_freeze()
    if (HERE/"CUSTODY_SECRET.json").exists() or (HERE/"SCORES_COMMIT.json").exists():
        raise FileExistsError("Custody already exists; recover without repeating generation")
    est, c, factor, directions, dims = geometry()
    secret = make_secret()
    write_new(HERE/"CUSTODY_SECRET.json",secret)
    write_new(HERE/"CUSTODY_COMMIT.json",dict(
        status="COMMITTED_BEFORE_SYNTHETIC_DRAWS",
        at=datetime.now(timezone.utc).isoformat(), freeze_path=str(FREEZE), freeze_sha256=sha(FREEZE),
        generator_sha256=sha(Path(__file__)), secret_sha256=sha(HERE/"CUSTODY_SECRET.json"),
        count_per_masked_case=COUNT, batch=BATCH, cases=len(secret["cases"]),
        reuse="Each hypothesis shares ordinary primitive errors across nuisance stress cases.",
        storage="Input arrays are ephemeral. Seeds, source pins and raw-array SHA256 recover every block.",
        independence="Independent trials within a case. Fits and stress scenarios are paired.",
        no_observed_local_data=True))
    scores = HERE/"scores"
    scores.mkdir(exist_ok=False)
    manifest = []
    with tempfile.TemporaryDirectory(prefix="masked_input_",dir=HERE) as temp:
        input_path = Path(temp)/"input.npz"
        for case_index, case in enumerate(secret["cases"]):
            rng = np.random.default_rng(secret["seeds"][case["seed_key"]])
            for first in range(0, COUNT, BATCH):
                number = min(BATCH, COUNT-first)
                z = rng.standard_normal((number,factor.shape[1]))
                epsilon = rng.standard_normal(number)
                if case["kind"] == "importance":
                    z += SHIFT*directions[case["model"]]
                joint = z@factor.T
                local = joint[:,:dims].copy()
                bg = joint[:,dims:].copy()
                local += case["hypothesis"]*est["signal_local"]
                local += (case["fixed_bias"]+case["random_sd"]*epsilon)[:,None]*c if case["random_sd"] else case["fixed_bias"]*c
                block_id = f"{case['id']}_{first:06d}"
                output_path = scores/(block_id+".npz")
                with input_path.open("wb") as handle:
                    np.savez(handle,local=local,background=bg)
                verify_freeze()
                completed = subprocess.run([sys.executable,"-B","-X","utf8",str(SCORER),
                    "--input",str(input_path),"--estimator",str(ESTIMATOR),"--output",str(output_path)],
                    cwd=temp, capture_output=True, text=True, encoding="utf-8")
                if completed.returncode:
                    raise RuntimeError("frozen_scorer_failed:"+block_id+":"+completed.stderr[-1500:])
                manifest.append(dict(id=block_id,case_id=case["id"],first=first,n=number,
                    local_shape=list(local.shape),background_shape=list(bg.shape),
                    local_raw_sha256=array_sha(local),background_raw_sha256=array_sha(bg),
                    score_path=str(output_path),score_sha256=sha(output_path),
                    scorer_stdout=completed.stdout.strip()))
            print(json.dumps({"masked_cases_scored":case_index+1,"total_cases":len(secret["cases"]),
                              "seconds":round(time.monotonic()-start,1)}),flush=True)
    write_new(HERE/"SCORES_MANIFEST.json",manifest)
    write_new(HERE/"SCORES_COMMIT.json",dict(
        status="SCORES_PINNED_LABELS_CLOSED",at=datetime.now(timezone.utc).isoformat(),
        freeze_sha256=sha(FREEZE),generator_sha256=sha(Path(__file__)),
        custody_commit_sha256=sha(HERE/"CUSTODY_COMMIT.json"),
        manifest_sha256=sha(HERE/"SCORES_MANIFEST.json"),
        blocks=len(manifest),cases=len(secret["cases"]),samples_scored=sum(row["n"] for row in manifest),
        elapsed_seconds=time.monotonic()-start,
        next_action="Coordinator acknowledges this receipt before unblinding."))
    print(json.dumps({"status":"SCORES_PINNED_LABELS_CLOSED","receipt_sha256":sha(HERE/"SCORES_COMMIT.json")}),flush=True)

def wilson(success, total):
    phat=success/total
    z=norm.ppf(.975)
    denominator=1+z*z/total
    center=(phat+z*z/(2*total))/denominator
    radius=z*math.sqrt(phat*(1-phat)/total+z*z/(4*total*total))/denominator
    return dict(success=int(success),total=int(total),estimate=phat,ci95=[center-radius,center+radius])

def unblind(acknowledgment):
    verify_freeze()
    ack=json.loads(Path(acknowledgment).read_text(encoding="utf-8"))
    if ack.get("scores_commit_sha256") != sha(HERE/"SCORES_COMMIT.json"):
        raise ValueError("acknowledgment_does_not_match_commit")
    commitment=json.loads((HERE/"CUSTODY_COMMIT.json").read_text())
    for name, expected in [("CUSTODY_SECRET.json",commitment["secret_sha256"]),
                           (Path(__file__).name,commitment["generator_sha256"])]:
        if sha(HERE/name)!=expected: raise ValueError("custody_changed:"+name)
    score_commit=json.loads((HERE/"SCORES_COMMIT.json").read_text())
    if sha(HERE/"SCORES_MANIFEST.json")!=score_commit["manifest_sha256"]:
        raise ValueError("manifest_changed")
    manifest=json.loads((HERE/"SCORES_MANIFEST.json").read_text())
    secret=json.loads((HERE/"CUSTODY_SECRET.json").read_text())
    est,c,factor,directions,dims=geometry()
    outputs=[]
    for case in secret["cases"]:
        blocks=sorted([row for row in manifest if row["case_id"]==case["id"]],key=lambda r:r["first"])
        array={k:[] for k in ("t","z_null","z_tgl","z_null_exact_bg")}
        for row in blocks:
            if sha(row["score_path"])!=row["score_sha256"]:raise ValueError("score_changed")
            with np.load(row["score_path"],allow_pickle=False) as score:
                for key in array: array[key].append(score[key])
        array={key:np.concatenate(parts) for key,parts in array.items()}
        record={**case,"models":[]}
        if case["kind"]=="ordinary":
            truth=case["hypothesis"]*float(est["logK"])
            for index,name in enumerate(est["model_names"]):
                z=array["z_null"][:,index]
                noise=(array["t"][:,index]-truth)/est["sd_null"][index]
                response=float(est["weights"][index]@c)
                true_scale=math.sqrt(est["sd_null"][index]**2+(response*case["random_sd"])**2)
                rec=dict(name=str(name),mean_t=float(array["t"][:,index].mean()),
                    sd_t=float(array["t"][:,index].std(ddof=1)),sd_nominal=float(est["sd_null"][index]),
                    sd_true_predicted=true_scale,bias_predicted=response*case["fixed_bias"],
                    mean_Z=float(z.mean()),prediction_mean_Z=(truth+response*case["fixed_bias"])/est["sd_null"][index],
                    rejection=wilson(np.sum(z>=5),COUNT),
                    power_exact_bg=wilson(np.sum(array["z_null_exact_bg"][:,index]>=5),COUNT),
                    coverage95=wilson(np.sum(np.abs(noise)<=norm.ppf(.975)),COUNT),
                    power_variance_recalibrated=wilson(np.sum(array["t"][:,index]>=5*true_scale),COUNT),
                    analytic_rejection=float(norm.sf((5*est["sd_null"][index]-truth-response*case["fixed_bias"])/true_scale)),
                    analytic_coverage95=float(norm.cdf((norm.ppf(.975)*est["sd_null"][index]-response*case["fixed_bias"])/true_scale)-
                                              norm.cdf((-norm.ppf(.975)*est["sd_null"][index]-response*case["fixed_bias"])/true_scale)))
                if case["hypothesis"]:
                    rec["TGL_compatibility_coverage95"]=wilson(np.sum(np.abs(array["z_tgl"][:,index])<=norm.ppf(.975)),COUNT)
                    rec["TGL_compatibility_mean"]=float(array["z_tgl"][:,index].mean())
                    rec["TGL_compatibility_sd"]=float(array["z_tgl"][:,index].std(ddof=1))
                record["models"].append(rec)
        else:
            rng=np.random.default_rng(secret["seeds"][case["seed_key"]])
            logweights=[]
            for row in blocks:
                z=rng.standard_normal((row["n"],factor.shape[1]))
                rng.standard_normal(row["n"])
                z+=SHIFT*directions[case["model"]]
                logweights.append(-SHIFT*(z@directions[case["model"]])+SHIFT**2/2)
            weights=np.exp(np.concatenate(logweights))
            index=case["model"]
            for key in ("z_null","z_null_exact_bg"):
                values=weights*(array[key][:,index]>=5)
                avg=float(values.mean());se=float(values.std(ddof=1)/math.sqrt(COUNT))
                record["models"].append(dict(name=str(est["model_names"][index]),score=key,
                    tail_estimate=avg,standard_error=se,relative_standard_error=se/avg,
                    weighted_positive_ess=float(values.sum()**2/(values@values)),
                    gaussian_reference=float(norm.sf(5)),
                    gaussian_reference_zscore=(avg-norm.sf(5))/se,
                    ci95_normal_mc=[max(0,avg-1.96*se),avg+1.96*se],
                    tilted_exceedances=int(np.sum(array[key][:,index]>=5)),
                    interpretation="Target-weighted tail; no unweighted tilted p-value."))
        outputs.append(record)
    result=dict(status="UNBLINDED_SYNTHETIC_RESULTS",at=datetime.now(timezone.utc).isoformat(),
        acknowledgment_sha256=sha(acknowledgment),scores_commit_sha256=sha(HERE/"SCORES_COMMIT.json"),
        outputs=outputs,gaussian_alpha=float(norm.sf(5)),no_observed_local_data=True,
        ordinary_zero_success_upper95=1-.05**(1/COUNT),
        coverage_target="t = local logH minus background logH at true parameter centers",
        background_exact_scope="Exact log10(H0+Gaussian fluctuation); nominal statistic scale remains frozen.",
        shared_trials="Stress scenarios share ordinary errors within a hypothesis. Both fitted models share samples.")
    write_new(HERE/"UNBLINDED_RESULTS.json",result)
    print(json.dumps({"status":result["status"],"path":str(HERE/"UNBLINDED_RESULTS.json"),"sha256":sha(HERE/"UNBLINDED_RESULTS.json")}),flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("operation",choices=["generate_score","unblind"])
    parser.add_argument("--acknowledgment",type=Path)
    parser.add_argument("--freeze",type=Path,default=FREEZE)
    args=parser.parse_args()
    FREEZE=args.freeze.resolve()
    if args.operation=="generate_score": generate()
    else:
        if args.acknowledgment is None:parser.error("--acknowledgment required")
        unblind(args.acknowledgment)

