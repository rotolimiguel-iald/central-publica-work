"""Controlled promotion of the reviewed v408 staging. Run each step as a separate process."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import uuid

Q = Path(__file__).resolve().parent
P = Q.parent / "iald_v408_20261105"
R = Q / "promotion"
STAGED_REVIEW = P / "review/QUEUE_RECONSTRUCTION.json"
FINAL_REVIEW = P / "review/QUEUE_FINAL_PATHS.json"
AUTH = P / "F03_WRITE_V408.json"
STAGING = Q / "STAGING_R1.json"
UNIT = "F0.3.MEMORIA_CIENTIFICA_SYNC"
sys.dont_write_bytecode = True
sys.path.insert(0, str(Q.parent / "scientific_memory_sync_20261013"))
from scientific_memory_sync import ScientificMemorySync, cm, require_claim, utc_now


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    path = Path(path)
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")


def write_once(path, doc):
    raw = encoded(doc)
    if path.exists():
        require(path.read_bytes() == raw, "Conflicting evidence: " + str(path))
        return
    cm.save_json(path, doc, expected_old=None)


def inputs():
    summary = read(STAGING)
    for entry in summary["receipts"]:
        require(pin(entry["path"]) == entry, "Staging evidence changed")
    for entry in summary["inputs"]:
        require(pin(entry["path"]) == entry, "Preparation input changed: " + entry["path"])
    epoch = summary["epoch"]
    src = Q / "staging/releases" / epoch
    target = cm.RELEASES / epoch
    require(src.resolve(strict=True) == src and target.resolve() == target, "Redirected release")
    review = read(STAGED_REVIEW)
    comparisons = {"status": "PASS", "epoch": epoch, "generation": summary["generation"],
                   "manifest_sha256": pin(src/"manifest.json")["sha256"],
                   "index_sha256": pin(src/"index.sqlite3")["sha256"],
                   "complete_documents": summary["documents"], "chunks_verified": summary["chunks"]}
    require(all(review[k] == v for k, v in comparisons.items()), "Independent staging review differs")
    require(review["reviewer"] and review["reviewer"] != summary["builder"], "Reviewer required")
    return summary, src, target


def planned(summary, src, target):
    manifest = read(src / "manifest.json")
    root = target / "snapshots" / target.name
    manifest["snapshot_root"] = str(root)
    for doc in manifest["documents"]:
        doc["path"] = str(root / doc["name"])
    manifest_raw = encoded(manifest)
    prep = read(Q / ("PREPARATION_" + target.name + ".json"))
    dest_prep = copy.deepcopy(prep)
    dest_prep.update(status="REMAPPED_FROM_REVIEWED_STAGING", target=str(target),
                     baseline_active_pin=summary["initial_check"]["active_pin"],
                     manifest={"path": str(target/"manifest.json"), "bytes": len(manifest_raw),
                               "sha256": hashlib.sha256(manifest_raw).hexdigest()})
    files = {"index.sqlite3": summary["stage_index"]["sha256"]}
    for d in manifest["documents"]:
        files[str(Path(d["path"]).relative_to(target))] = d["sha256"]
    files[str((root/"SEALED_SNAPSHOT.json").relative_to(target))] = manifest["snapshot_manifest_sha256"]
    files["manifest.json"] = dest_prep["manifest"]["sha256"]
    plan = {"release": "v408", "generation": prep["generation"], "epoch": target.name,
            "baseline": dest_prep["baseline_active_pin"], "destination": str(target),
            "manifest": dest_prep["manifest"], "files": files, "staging": pin(STAGING),
            "stage_review": pin(STAGED_REVIEW), "promotion_cli": pin(__file__)}
    return manifest, dest_prep, plan


def production_precheck(sync, summary):
    expected = summary["initial_check"]
    require(sync.check() == expected, "Production baseline or sealed generation changed")
    sync.source_stable(read(Q / ("PREPARATION_" + summary["epoch"] + ".json")))


def authorization(plan):
    auth = read(AUTH)
    required = {"scope": "F0.3_v408_materialize_and_activate_after_final_review",
                "epoch": plan["epoch"], "generation": plan["generation"],
                "expected_active_sha256": plan["baseline"]["sha256"],
                "plan_sha256": pin(R/"PLAN.json")["sha256"],
                "parent_reference_sha256": pin(P/"SESSION_REFERENCE.json")["sha256"]}
    require(all(auth.get(k) == v for k, v in required.items()), "Authorization scope or pins differ")
    order = auth["operator_order"]
    p = Path(order["path"])
    require(p.resolve(strict=True) == p and p.parent == P and p.suffix.lower() == ".txt",
            "Operator order must be a local text artifact in the parent mission")
    require(p.stat().st_size and pin(p)["sha256"] == order["sha256"], "Order pin differs")
    # Human authority is checked by the parent, never inferred from the contents.
    return pin(AUTH)


def assert_tree(target, files):
    names = {str(p.relative_to(target)) for p in target.rglob("*") if p.is_file()}
    require(names == set(files), "Unexpected or missing files in release")
    for name, digest in files.items():
        path = target / name
        require(path.resolve(strict=True) == path and pin(path)["sha256"] == digest,
                "Release file pin differs: " + name)


def materialize(sync, summary, src, target, plan):
    require(os.name == "nt", "No-replace directory publication requires Windows")
    require_claim(UNIT, sync.member)
    auth = authorization(plan)
    production_precheck(sync, summary)
    if not target.exists():
        # Construct on the same volume in Q. Rename on Windows refuses existing
        # destinations; an interruption before publication leaves production alone.
        tmp = R / ("transfer_" + uuid.uuid4().hex)
        tmp.mkdir(exist_ok=False)
        for rel in plan["files"]:
            origin = R/"MANIFEST_FINAL.json" if rel == "manifest.json" else src/rel
            out = tmp / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origin, out)
        assert_tree(tmp, plan["files"])
        require_claim(UNIT, sync.member)
        require(authorization(plan) == auth, "Authorization changed")
        require(pin(cm.ACTIVE) == plan["baseline"], "CAS baseline changed before publication")
        tmp.rename(target)
    assert_tree(target, plan["files"])
    require(pin(cm.ACTIVE) == plan["baseline"], "Pointer moved during materialization")
    write_once(R/"MATERIALIZED.json", {"target": str(target), "manifest": pin(target/"manifest.json"),
                                      "active_before_activation": pin(cm.ACTIVE), "authorization": auth})


def verify_final(sync, summary, target, plan):
    production_precheck(sync, summary)
    assert_tree(target, plan["files"])
    result = sync.verify(target.name)
    baseline = read(Q/"VERIFY_STAGING.json")
    require(result == baseline, "Final verification differs from reviewed staging")
    return {"status": "PASS", "target": str(target), "generation": result["generation"],
            "documents": result["documents"], "chunks": result["chunks"],
            "manifest": pin(target/"manifest.json"), "index": pin(target/"index.sqlite3"),
            "full_check": result, "active_pre_cas": pin(cm.ACTIVE),
            "materialization": pin(R/"MATERIALIZED.json"), "plan": pin(R/"PLAN.json")}


def reviewed(plan, summary):
    rr = read(FINAL_REVIEW)
    require(rr["status"] == "PASS" and rr["generation"] == plan["generation"]
            and rr["manifest_sha256"] == plan["manifest"]["sha256"]
            and rr["verification_sha256"] == pin(R/"VERIFY_FINAL_PATHS.json")["sha256"]
            and rr["expected_active_sha256"] == plan["baseline"]["sha256"]
            and rr["reviewer"] and rr["reviewer"] != summary["builder"],
            "Independent final-paths review missing or mismatched")
    return pin(FINAL_REVIEW)


def complete(sync, summary, target, plan):
    ack = read(R/"ACTIVATION.json")
    pointer = read(cm.ACTIVE)
    require(ack["pointer"] == pointer and pointer["epoch"] == target.name
            and pointer["manifest_sha256"] == plan["manifest"]["sha256"], "Active identity differs")
    after = sync.check()
    require(after["status"] == "CURRENT" and after["sealed_generation"] == plan["generation"],
            "New process did not receive target")
    actual = sync.verify(target.name)
    require(actual == read(Q/"VERIFY_STAGING.json"), "Post-activation verification differs")
    papers = ["um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md"]
    query = " ".join(read(sync.report_path(target.name))["statute_record_names"])
    received = {}
    for mode, expected in actual["retrieval"].items():
        packet = cm.prepare(query, allowed_sources=papers, mode=mode, max_chars=24000)
        require(packet["receipt"] == expected and cm.digest(packet["prompt"].encode()) == expected["packet_sha256"],
                "Default production retrieval mismatch")
        received[mode] = {"generation": expected["generation"], "packet_sha256": expected["packet_sha256"]}
    old = read(Q/"BASELINE_PRODUCTION.json")["inventory"]
    for rel, digest in old["canonical_files"].items():
        if rel == cm.ACTIVE.name:
            continue
        require(pin(cm.ACTIVE.parent/rel)["sha256"] == digest, "Earlier canonical file changed")
    for rel, digest in old["queue_storage_bytes"].items():
        require(pin(cm.ACTIVE.parent.parent/rel)["sha256"] == digest, "Queue file changed: reconcile")
    require(any(pin(p)["sha256"] == plan["baseline"]["sha256"] for p in cm.ACTIVE.parent.glob("ACTIVE.json.bak_*")),
            "Byte-exact previous pointer backup missing")
    require(read(cm.ACTIVE) == pointer, "Pointer changed during final read")
    write_once(R/"RECEIVED_GENERATION.json", {"check": after, "received": received})
    files = [STAGING, STAGED_REVIEW, AUTH, FINAL_REVIEW, R/"PLAN.json", R/"MATERIALIZED.json",
             R/"VERIFY_FINAL_PATHS.json", R/"ACTIVATION.json", R/"RECEIVED_GENERATION.json"]
    delivery = {"release": "v408", "status": "ACTIVATED_VERIFIED_CURRENT_RECEIVED_GENERATION_CONFIRMED_NEW_PROCESS",
                "epoch": target.name, "generation": plan["generation"], "manifest": pin(target/"manifest.json"),
                "active_pointer": pin(cm.ACTIVE), "documents": actual["documents"], "chunks": actual["chunks"],
                "previous_releases_preserved": summary["production_observed"]["previous_releases"],
                "previous_manifests_unchanged": True, "receipts": {p.name:pin(p) for p in files}}
    write_once(Q/"DELIVERY_TECHNICAL_R1.json", delivery)


def run(op, member):
    summary, src, target = inputs()
    manifest, prep, plan = planned(summary, src, target)
    sync = ScientificMemorySync(work=R, member=member, unit=UNIT)
    if op == "plan":
        production_precheck(sync, summary)
        write_once(R/"MANIFEST_FINAL.json", manifest)
        write_once(sync.report_path(target.name), prep)
        write_once(R/"PLAN.json", plan)
        return
    require(read(R/"PLAN.json") == plan and read(R/"MANIFEST_FINAL.json") == manifest and
            read(sync.report_path(target.name)) == prep, "Remap plan changed")
    if op == "materialize":
        materialize(sync, summary, src, target, plan)
    elif op == "verify-final":
        write_once(R/"VERIFY_FINAL_PATHS.json", verify_final(sync, summary, target, plan))
    elif op == "activate":
        auth = authorization(plan)
        review = reviewed(plan, summary)
        require_claim(UNIT, member)
        # If the process stopped after CAS, use the exact-target branch of the API.
        active = read(cm.ACTIVE)
        if active.get("epoch") != target.name:
            require(verify_final(sync, summary, target, plan) == read(R/"VERIFY_FINAL_PATHS.json"),
                    "Reviewed final paths changed")
        else:
            require(active.get("manifest_sha256") == plan["manifest"]["sha256"], "Conflicting active target")
        require(authorization(plan) == auth and reviewed(plan, summary) == review, "Inputs changed")
        result = sync.activate(target.name)
        write_once(R/"ACTIVATION.json", {"pointer": result["pointer"], "review": review,
                                         "baseline": plan["baseline"], "authorization": auth})
    else:
        complete(sync, summary, target, plan)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("step", choices=("plan", "materialize", "verify-final", "activate", "receipt"))
    ap.add_argument("--member")
    args = ap.parse_args()
    if args.step in ("materialize", "activate") and not args.member:
        ap.error("--member must identify the current actual claimant")
    run(args.step, args.member or "read-only")
    print(args.step, "OK")
