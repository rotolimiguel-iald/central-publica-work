"""New synthetic coverage/PSD controls; no observed centers or likelihood."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import covariance_admission_r1 as c

HERE = Path(__file__).resolve().parent


def checks():
    fixture_path = HERE / "PLAN_R1.json"
    pin = {"path": str(fixture_path), "sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest()}
    ref = [{"source_id": "fixture", "line_start": 1, "line_end": 1}]
    ids = ["SYN_A", "SYN_B", "SYN_C"]
    catalog = {"schema": "F9_SYSTEMATICS_CATALOG_R1", "sources": {"fixture": pin},
               "families": {"synthetic": ids}, "covariance_unit": "synthetic_unit^2",
               "observable_maps": {i: {"status": "SYNTHETIC_MAP", "references": ref} for i in ids},
               "pairs": {"|".join([a, b]): {"components": {"shared": {
                   "status": "SYNTHETIC_INPUT", "interval": [-0.9, 0.9], "references": ref}}}
                   for i, a in enumerate(ids) for b in ids[i + 1:]}}
    request = {"mode": "SYNTHETIC_QUALIFICATION", "family": "synthetic", "reader_ids": ids,
               "unit": "synthetic_unit^2", "matrix": [[1, .2, .1], [.2, 1, -.1], [.1, -.1, 1]],
               "pairs": {"SYN_A|SYN_B": {"shared": .2}, "SYN_A|SYN_C": {"shared": .1},
                         "SYN_B|SYN_C": {"shared": -.1}}}
    records = []
    with tempfile.TemporaryDirectory(prefix="synthetic_r1_", dir=HERE) as td:
        def one(name, mutate=None, expected=None):
            cat, req = copy.deepcopy(catalog), copy.deepcopy(request)
            if mutate:
                mutate(cat, req)
            p = Path(td) / (name + ".json")
            raw = json.dumps(cat, allow_nan=False).encode()
            p.write_bytes(raw)
            try:
                value = c.admit_covariance(req, catalog_path=p, catalog_sha256=hashlib.sha256(raw).hexdigest())
            except c.AdmissionError as exc:
                assert expected and expected in str(exc), (name, str(exc), expected)
                records.append({"name": name, "passed": True, "refusal": str(exc)})
            else:
                assert expected is None, (name, "expected refusal", expected)
                assert value["physical_admission"] is False
                records.append({"name": name, "passed": True, "qualification": value})

        one("complete_explicit_synthetic_spd")
        one("missing_pair", lambda a,b:b["pairs"].pop("SYN_A|SYN_B"), "ALL_EXPLICIT_PAIRS")
        one("missing_component", lambda a,b:b["pairs"]["SYN_A|SYN_B"].clear(), "ALL_EXPLICIT_COMPONENTS")
        one("open_component_even_with_number", lambda a,b:a["pairs"]["SYN_A|SYN_B"]["components"]["shared"].update(status="OPEN"), "OPEN_COVERAGE")
        one("open_map", lambda a,b:a["observable_maps"]["SYN_A"].update(status="OPEN"), "OPEN_COVERAGE")
        one("duplicate_reader", lambda a,b:b["reader_ids"].__setitem__(1,"SYN_A"), "READER_ID")
        one("wrong_reader_order", lambda a,b:b["reader_ids"].reverse(), "READER_ID")
        one("wrong_units", lambda a,b:b.update(unit="km/s/Mpc"), "UNIT_MISMATCH")
        one("nonfinite", lambda a,b:b["matrix"][0].__setitem__(0,float("nan")), "NONFINITE")
        one("boolean", lambda a,b:b["matrix"][0].__setitem__(0,True), "BOOL")
        one("nonsymmetric", lambda a,b:b["matrix"][0].__setitem__(1,.3), "NONSYMMETRIC")
        one("component_mismatch", lambda a,b:b["pairs"]["SYN_A|SYN_B"].update(shared=.3), "DO_NOT_RECONSTRUCT")
        one("bound_violation", lambda a,b:b["pairs"]["SYN_A|SYN_B"].update(shared=1.1), "OUTSIDE_DECLARED_BOUND")
        def indefinite(a,b):
            b["matrix"]=[[1,-.8,-.8],[-.8,1,-.8],[-.8,-.8,1]]
            for v in b["pairs"].values():v["shared"]=-.8
        one("pairwise_bounds_do_not_imply_psd", indefinite, "positive definite")
        def singular(a,b):
            b["matrix"]=[[1,-.5,-.5],[-.5,1,-.5],[-.5,-.5,1]]
            for v in b["pairs"].values():v["shared"]=-.5
        one("singular_psd_refused_no_jitter", singular, "positive definite")
        def explicit_zero(a,b):
            b["matrix"]=[[1,0,0],[0,1,0],[0,0,1]]
            for v in b["pairs"].values():v["shared"]=0
            for v in a["pairs"].values():v["components"]["shared"].update(interval=[0,0],zero_reason="Synthetic independent variables fixed before tests")
        one("explicit_zero_with_reason", explicit_zero)
        def badzero(a,b):
            explicit_zero(a,b)
            a["pairs"]["SYN_A|SYN_B"]["components"]["shared"].pop("zero_reason")
        one("zero_without_reason", badzero, "ZERO_WITHOUT")
        one("physical_mode_refused", lambda a,b:b.update(mode="PHYSICAL"), "NOT_IMPLEMENTED")
        one("synthetic_cannot_be_conditional", lambda a,b:b.update(mode="CONDITIONAL_MATRIX_ONLY"), "MAP_NOT_QUALIFIED")
        one("wrong_source_hash", lambda a,b:a["sources"]["fixture"].update(sha256="0"*64), "PIN_MISMATCH")
        one("reference_unknown", lambda a,b:a["observable_maps"]["SYN_A"].update(references=[{"source_id":"absent","line_start":1,"line_end":1}]), "INVALID_DOCUMENTARY")
        one("huge_integer_refused", lambda a,b:b["matrix"][0].__setitem__(0,10**400), "NUMERIC_RANGE")
        def normalization_overflow(a,b):
            b["matrix"][0][0]=1e-308
            b["matrix"][1][1]=1e-308
            b["matrix"][0][1]=b["matrix"][1][0]=1e308
            b["pairs"]["SYN_A|SYN_B"]["shared"]=1e308
            a["pairs"]["SYN_A|SYN_B"]["components"]["shared"]["interval"]=[-1e308,1e308]
        one("normalization_overflow_visible", normalization_overflow, "NORMALIZATION_RANGE")
    # Documentary catalog must remain OPEN, regardless of a supplied numerical C.
    p = HERE / "DEPENDENCY_INVENTORY_R1.json"
    inv = c.load_catalog(p, hashlib.sha256(p.read_bytes()).hexdigest())
    missing = c.unresolved(inv, "P_primaria")
    assert any("SHARED_SN" in x for x in missing)
    assert any("PANTHEON_SHARED" in x for x in missing)
    assert any("HST_ANCHORS" in x for x in missing)
    assert sum(x.startswith("MAP:") for x in missing)==5
    records.append({"name":"actual_catalog_remains_open_no_matrix_built", "passed":True,"unresolved":missing})
    return {"checks": records, "passed": all(x["passed"] for x in records),
            "count": len(records), "R1_scientific_status": "OPEN", "observed_composite": False}
