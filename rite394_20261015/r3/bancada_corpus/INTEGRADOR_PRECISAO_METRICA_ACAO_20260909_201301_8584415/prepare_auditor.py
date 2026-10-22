"""Derive a new static auditor from frozen auditor83 and measured successor inventory."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, sys

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
SOURCE = BASE / "AUDITORIA_INTEGRACAO_83_20260909/audit_integration_83.py"
PRIOR_REPORT = SOURCE.parent / "AUDITORIA_INTEGRACAO_83.json"

def record(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def new_file(path, raw):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw

def main():
    assert len(sys.argv) == 2, "Pass final measured INVENTARIO_91.json or INVENTARIO_92.json."
    inventory_path = Path(sys.argv[1]).resolve()
    inventory = json.loads(inventory_path.read_bytes())
    prior = json.loads(PRIOR_REPORT.read_bytes())
    assert inventory["status"] == "PREPARED_STATIC_ONLY_NOT_CONFIRMED"
    assert prior["status"] == "PASS_STATIC_INTEGRATION_SCOPE" and not prior["failed_checks"]
    assert inventory["predecessor"] == {k: prior["counts"][k] for k in inventory["predecessor"]}
    for module in inventory["modules"]:
        assert record(module["source"]["path"]) == module["source"]
        assert record(module["build_result"]["path"]) == module["build_result"]
    delta, total = inventory["delta"], inventory["accumulated"]
    n, t, d, i, all_terms = (total[k] for k in ["modules", "theorems", "other_declarations", "local_instances", "total"])
    dn, dt, dd, di, da = (delta[k] for k in ["modules", "theorems", "other_declarations", "local_instances", "total"])
    cached = inventory["predecessor"]["modules"]
    stage_sizes = [s["counts"]["modules"] for s in prior["stages"]] + [dn]
    assert sum(stage_sizes) == n
    embedded = [prior["stages"][0]["old_embedded"]] + [s["new_embedded"] for s in prior["stages"]] + [inventory["embedded_after_expected"]]
    lean = [embedded[0] - (inventory["embedded_before"] - inventory["lean_embedded_before"])] + [s["new_lean"] for s in prior["stages"]] + [inventory["lean_embedded_after_expected"]]
    full_audit = inventory["full_theorem_audit_before"] + dt
    original = SOURCE.read_bytes()
    text = original.decode("utf-8").replace("\r\n", "\n")
    changes = []
    def replace(old, new):
        nonlocal text
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
        changes.append({"from": old, "to": new, "occurrences": 1})
    replace("of 83 integrated modules", f"of {n} integrated modules")
    replace("Pass copy83 folder", f"Pass copy{n} folder")
    replace('prior_auditor=BASE/"AUDITORIA_INTEGRACAO_72_20260909_171311_522844/audit_integration_72.py"',
            'prior_auditor=BASE/"AUDITORIA_INTEGRACAO_83_20260909/audit_integration_83.py"')
    replace('remember(prior_auditor)', 'remember(prior_auditor)\nexpected_inventory=remember(Path(' + repr(inventory_path.as_posix()) + '))\nck("expected_inventory_pin", expected_inventory == ' + repr(record(inventory_path)) + ')')
    replace('ck("four_stages_63_9_5_6",[len(s["ir"]["modules"]) for s in stages]==[63,9,5,6])',
            'ck("measured_stage_sizes",[len(s["ir"]["modules"]) for s in stages]==' + repr(stage_sizes) + ')')
    replace('"all_83_sources_preserved_in_final"', f'"all_{n}_sources_preserved_in_final"')
    replace('ck("measured_83_1178_328_1506",totals=={"modules":83,"theorems":1178,"other_declarations":328,"local_instances":12,"total":1506})',
            'ck("measured_accumulated_counts",totals==' + repr(total) + ')')
    replace('ck("delta6_113_35_148",stage_rows[-1]["counts"]=={"modules":6,"theorems":113,"other_declarations":35,"local_instances":5,"total":148})',
            'ck("measured_delta_counts",stage_rows[-1]["counts"]==' + repr(delta) + ')')
    replace('ck("embedded_counts_606_669_678_683_689",[len(canon)]+[r["new_embedded"] for r in stage_rows]==[606,669,678,683,689])',
            'ck("measured_embedded_counts",[len(canon)]+[r["new_embedded"] for r in stage_rows]==' + repr(embedded) + ')')
    replace('ck("lean_counts_602_665_674_679_685",[sum(k.endswith(".lean") for k in canon)]+[r["new_lean"] for r in stage_rows]==[602,665,674,679,685])',
            'ck("measured_lean_counts",[sum(k.endswith(".lean") for k in canon)]+[r["new_lean"] for r in stage_rows]==' + repr(lean) + ')')
    for old, new in [("no_duplicate_full_names_among83", f"no_duplicate_full_names_among{n}"),
                     ("cumulative_83_imports", f"cumulative_{n}_imports"),
                     ("cumulative_1178_theorem_audits", f"cumulative_{t}_theorem_audits"),
                     ("plan_all83_module_metadata", f"plan_all{n}_module_metadata"),
                     ("plan_all1506_names", f"plan_all{all_terms}_names"),
                     ("prepared_sources_match_all83", f"prepared_sources_match_all{n}"),
                     ("all83_compiled_artifacts:", f"all{n}_compiled_artifacts:"),
                     ('"among83":dups', f'"among{n}":dups')]:
        replace(old, new)
    replace('prep_path=PREPARER/"RECIBO_PREPARACAO_SUCESSORA.json"',
            'prep_path=PREPARER/"RECIBO_PREPARACAO_SUCESSORA.json"\nck("prepared_receipt_required", prep_path.is_file())')
    replace('ck("dedicated_audit_all1506",Counter(declarations)==Counter(d["name"] for d in alldecls) and len(declarations)==1506)',
            f'ck("dedicated_audit_all{all_terms}",Counter(declarations)==Counter(d["name"] for d in alldecls) and len(declarations)=={all_terms})')
    replace('ck("plan_FullTGLAudit5670_exact",len(fullrun)==1 and len(expected_full)==5670 and fullrun[0]["expected_axiom_terms"]==expected_full)',
            f'ck("plan_FullTGLAudit{full_audit}_exact",len(fullrun)==1 and len(expected_full)=={full_audit} and fullrun[0]["expected_axiom_terms"]==expected_full)')
    replace('ck("dedicated_audit_twelve_instances",all(d["name"] in declarations for d in alldecls if d["kind"]=="instance" and d["local"]))',
            f'ck("dedicated_audit_{i}_instances",sum(d["kind"]=="instance" and d["local"] for d in alldecls)=={i} and all(d["name"] in declarations for d in alldecls if d["kind"]=="instance" and d["local"]))')
    replace('ck("prepared_77_cache_6_new_3_aggregates",len(plan["cached_modules"])==77 and len(plan["runs"])==9 and [r["module"] for r in plan["runs"][:6]]==stages[-1]["ir"]["transposed_module_order"])',
            f'ck("prepared_{cached}_cache_{dn}_new_3_aggregates",len(plan["cached_modules"])=={cached} and len(plan["runs"])=={dn + 3} and [r["module"] for r in plan["runs"][:{dn}]]==stages[-1]["ir"]["transposed_module_order"])')
    replace(' combined_path=build/"TRANSPOSED_RESULT.json"',
            ' combined_path=build/"TRANSPOSED_RESULT.json"\n ck("combined_receipt_required", combined_path.is_file())')
    replace('ck("combined_PASS_9_clean_exits",cr["status"]=="PASS_TRANSPOSED_SCOPE" and len(cr["runs"])==9 and all(r["exit_code"]==0 and r["valid"] and r["warning_lines"]==0 for r in cr["runs"]))',
            f'ck("combined_PASS_{dn + 3}_clean_exits",cr["status"]=="PASS_TRANSPOSED_SCOPE" and len(cr["runs"])=={dn + 3} and all(r["exit_code"]==0 and r["valid"] and r["warning_lines"]==0 for r in cr["runs"]))')
    replace('"FullTGLAudit":5670,"NewModulesAudit":1506', f'"FullTGLAudit":{full_audit},"NewModulesAudit":{all_terms}')
    replace('for p,r in list(inputs.items()):ck("stable:"+p,rec(p)==r)',
            'ck("prepared_and_combined_present", prepared is not None and combined is not None)\nfor p,r in list(inputs.items()):ck("stable:"+p,rec(p)==r)')
    # Report file names occur in several explicit output references; record their multiplicity.
    for old, new in [("AUDITORIA_INTEGRACAO_83.json", f"AUDITORIA_INTEGRACAO_{n}.json"),
                     ("RELATORIO_INTEGRACAO_83.md", f"RELATORIO_INTEGRACAO_{n}.md"),
                     ("MANIFESTO_AUDITORIA_83.json", f"MANIFESTO_AUDITORIA_{n}.json")]:
        occurrences = text.count(old)
        assert occurrences >= 1
        text = text.replace(old, new)
        changes.append({"from": old, "to": new, "occurrences": occurrences})
    replace("# Auditoria estática da integração83", f"# Auditoria estática da integração{n}")
    replace("canônico → lote63 → delta9 → delta5 → delta6.",
            "canônico → " + " → ".join(("lote" if index == 0 else "delta") + str(size) for index, size in enumerate(stage_sizes)) + ".")
    replace("Dentro da tabela, entram seis módulos", f"Dentro da tabela, entram {dn} módulos")
    ast.parse(text)
    folder = BASE / (f"AUDITORIA_INTEGRACAO_{n}_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(exist_ok=False)
    script = folder / f"audit_integration_{n}.py"
    new_file(script, text.encode("utf-8"))
    provenance = {"status": "PREPARED_NOT_EXECUTED", "created_utc": datetime.now(timezone.utc).isoformat(),
                  "source_auditor": record(SOURCE), "source_audit_PASS": record(PRIOR_REPORT),
                  "target_auditor": record(script), "inventory": record(inventory_path),
                  "adaptation_script": record(__file__), "changes": changes,
                  "measured_delta": delta, "measured_accumulated": total,
                  "measured_stage_sizes": stage_sizes, "embedded_counts": embedded, "lean_counts": lean,
                  "full_theorem_audit_expected": full_audit,
                  "additional_requirement": "Prepared and combined receipts must exist; absent evidence cannot yield PASS.",
                  "auditor_executed": False, "um_py_executed_or_imported": False,
                  "independent_reviewer_approval_attributed": False}
    new_file(folder / "PROVENIENCIA_ADAPTACAO.json", (json.dumps(provenance, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    assert SOURCE.read_bytes() == original
    print(json.dumps({"status": provenance["status"], "auditor": record(script),
                      "delta": delta, "accumulated": total, "full_theorem_audit_expected": full_audit}, ensure_ascii=False))

if __name__ == "__main__":
    main()
