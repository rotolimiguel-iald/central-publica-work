"""Prepare a successor auditor from frozen93 v2; retain its historical-base correction."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re, sys

BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
SOURCE=BASE/"AUDITORIA_INTEGRACAO_93_V2_20260909_203946_6451878/audit_integration_93_v2.py"
REPORT=SOURCE.parent/"AUDITORIA_INTEGRACAO_93.json"
def rec(path):
 path=Path(path).resolve();raw=path.read_bytes()
 return {"path":path.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def new(path,raw):
 assert path.resolve().is_relative_to(BASE) and not path.exists()
 temp=path.with_name(path.name+".tmp")
 with temp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert temp.read_bytes()==raw;os.rename(temp,path);assert path.read_bytes()==raw

assert len(sys.argv)==2,"Pass the measured final INVENTARIO_N.json."
inventory_path=Path(sys.argv[1]).resolve()
inventory=json.loads(inventory_path.read_bytes());prior=json.loads(REPORT.read_bytes())
assert inventory["status"]=="PREPARED_STATIC_ONLY_NOT_CONFIRMED"
assert prior["status"]=="PASS_STATIC_INTEGRATION_SCOPE" and not prior["failed_checks"]
assert inventory["predecessor"]=={k:prior["counts"][k] for k in inventory["predecessor"]}
assert prior["canonical_role"]=="HISTORICAL_SNAPSHOT_BASE"
assert prior["current_canonical_diagnostic"]["used_as_integration_base"] is False
for module in inventory["modules"]:
 assert rec(module["source"]["path"])==module["source"]
 assert rec(module["build_result"]["path"])==module["build_result"]
plan=json.loads(Path(inventory["predecessor_build_plan"]["path"]).read_bytes())
assert rec(inventory["predecessor_build_plan"]["path"])==inventory["predecessor_build_plan"]
assert len(plan["aggregate_processes"])==3
old=inventory["predecessor"];delta=inventory["delta"];total=inventory["accumulated"]
n,t,d,instances,terms=(total[k] for k in ["modules","theorems","other_declarations","local_instances","total"])
dn=delta["modules"];processes=dn+len(plan["aggregate_processes"])
full_audit=inventory["full_theorem_audit_before"]+delta["theorems"]
stage_sizes=[s["counts"]["modules"] for s in prior["stages"]]+[dn]
embedded=[prior["stages"][0]["old_embedded"]]+[s["new_embedded"] for s in prior["stages"]]+[inventory["embedded_after_expected"]]
lean=[embedded[0]-(inventory["embedded_before"]-inventory["lean_embedded_before"])]+[s["new_lean"] for s in prior["stages"]]+[inventory["lean_embedded_after_expected"]]
assert sum(stage_sizes)==n
original=SOURCE.read_bytes();text=original.decode("utf-8");changes=[]
def replace(old_text,new_text):
 global text
 assert text.count(old_text)==1,(old_text,text.count(old_text))
 text=text.replace(old_text,new_text)
 changes.append({"from":old_text,"to":new_text,"occurrences":1})
def replace_line(prefix,new_line):
 matches=[line for line in text.splitlines() if line.startswith(prefix)]
 assert len(matches)==1,(prefix,len(matches))
 replace(matches[0],new_line)

replace(f'of {old["modules"]} integrated modules',f'of {n} integrated modules')
replace(f'Pass copy{old["modules"]} folder',f'Pass copy{n} folder')
replace_line('prior_auditor=BASE/', 'prior_auditor=BASE/'+repr(SOURCE.relative_to(BASE).as_posix()))
replace_line('expected_inventory=remember(', 'expected_inventory=remember(Path('+repr(inventory_path.as_posix())+'))')
replace_line('ck("expected_inventory_pin",', 'ck("expected_inventory_pin", expected_inventory == '+repr(rec(inventory_path))+')')
replace_line('ck("measured_stage_sizes",', 'ck("measured_stage_sizes",[len(s["ir"]["modules"]) for s in stages]=='+repr(stage_sizes)+')')
replace_line('ck("measured_accumulated_counts",', 'ck("measured_accumulated_counts",totals=='+repr(total)+')')
replace_line('ck("measured_delta_counts",', 'ck("measured_delta_counts",stage_rows[-1]["counts"]=='+repr(delta)+')')
replace_line('ck("measured_embedded_counts",', 'ck("measured_embedded_counts",[len(canon)]+[r["new_embedded"] for r in stage_rows]=='+repr(embedded)+')')
replace_line('ck("measured_lean_counts",', 'ck("measured_lean_counts",[sum(k.endswith(".lean") for k in canon)]+[r["new_lean"] for r in stage_rows]=='+repr(lean)+')')
for before,after in [
 (f'all_{old["modules"]}_sources_preserved_in_final',f'all_{n}_sources_preserved_in_final'),
 (f'no_duplicate_full_names_among{old["modules"]}',f'no_duplicate_full_names_among{n}'),
 (f'cumulative_{old["modules"]}_imports',f'cumulative_{n}_imports'),
 (f'cumulative_{old["theorems"]}_theorem_audits',f'cumulative_{t}_theorem_audits'),
 (f'plan_all{old["modules"]}_module_metadata',f'plan_all{n}_module_metadata'),
 (f'plan_all{old["total"]}_names',f'plan_all{terms}_names'),
 (f'prepared_sources_match_all{old["modules"]}',f'prepared_sources_match_all{n}'),
 (f'all{old["modules"]}_compiled_artifacts:',f'all{n}_compiled_artifacts:'),
 (f'"among{old["modules"]}":dups',f'"among{n}":dups')]:
 replace(before,after)
replace_line(' ck("dedicated_audit_all',f' ck("dedicated_audit_all{terms}",Counter(declarations)==Counter(d["name"] for d in alldecls) and len(declarations)=={terms})')
replace_line(' ck("plan_FullTGLAudit',f' ck("plan_FullTGLAudit{full_audit}_exact",len(fullrun)==1 and len(expected_full)=={full_audit} and fullrun[0]["expected_axiom_terms"]==expected_full)')
replace_line(' ck("dedicated_audit_12_instances",',f' ck("dedicated_audit_{instances}_instances",sum(d["kind"]=="instance" and d["local"] for d in alldecls)=={instances} and all(d["name"] in declarations for d in alldecls if d["kind"]=="instance" and d["local"]))')
replace_line(' ck("prepared_83_cache_10_new_3_aggregates",',f' ck("prepared_{old["modules"]}_cache_{dn}_new_3_aggregates",len(plan["cached_modules"])=={old["modules"]} and len(plan["runs"])=={processes} and [r["module"] for r in plan["runs"][:{dn}]]==stages[-1]["ir"]["transposed_module_order"])')
replace_line('  ck("combined_PASS_13_clean_exits",',f'  ck("combined_PASS_{processes}_clean_exits",cr["status"]=="PASS_TRANSPOSED_SCOPE" and len(cr["runs"])=={processes} and all(r["exit_code"]==0 and r["valid"] and r["warning_lines"]==0 for r in cr["runs"]))')
replace('"FullTGLAudit":5778,"NewModulesAudit":1638',f'"FullTGLAudit":{full_audit},"NewModulesAudit":{terms}')
for before,after in [("AUDITORIA_INTEGRACAO_93.json",f"AUDITORIA_INTEGRACAO_{n}.json"),
 ("RELATORIO_INTEGRACAO_93.md",f"RELATORIO_INTEGRACAO_{n}.md"),
 ("MANIFESTO_AUDITORIA_93.json",f"MANIFESTO_AUDITORIA_{n}.json")]:
 occurrences=text.count(before);assert occurrences>=1;text=text.replace(before,after)
 changes.append({"from":before,"to":after,"occurrences":occurrences})
replace('# Auditoria estática da integração93 — versão 2, base histórica',f'# Auditoria estática da integração{n} — base histórica preservada')
replace('snapshot histórico do canônico → lote63 → delta9 → delta5 → delta6 → delta10.',
 'snapshot histórico do canônico → '+' → '.join(('lote' if i==0 else 'delta')+str(count) for i,count in enumerate(stage_sizes))+'.')
replace('Dentro da tabela, entram 10 módulos',f'Dentro da tabela, entram {dn} módulos')

# The correction that separates historical evidence from the mutable live file is immutable.
original_text=original.decode("utf-8")
segments=[('def observe_live_canonical(p):','def rec(p):'),
 ('historical_source_record=','previous=canon;'),
 (' sp=folder/"um_ORIGINAL_SNAPSHOT.py"',' ck(label+":configuration_module_set"'),
 ('current_canonical=observe_live_canonical(canonicalpath)','for p,r in list(inputs.items()):')]
for start,stop in segments:
 original_part=original_text[original_text.index(start):original_text.index(stop,original_text.index(start))]
 target_part=text[text.index(start):text.index(stop,text.index(start))]
 assert target_part==original_part,('Historical correction changed',start)
assert 'table(canonicalpath)' not in text and 'remember(canonicalpath)' not in text
for required in ['prepared_receipt_required','combined_receipt_required','prepared_and_combined_present','HISTORICAL_SNAPSHOT_BASE','current_canonical_diagnostic']:
 assert required in text
ast.parse(text)
folder=BASE/(f"AUDITORIA_INTEGRACAO_{n}_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
folder.mkdir(exist_ok=False);target=folder/f"audit_integration_{n}.py";new(target,text.encode("utf-8"))
provenance={"status":"PREPARED_NOT_EXECUTED","created_utc":datetime.now(timezone.utc).isoformat(),
 "origin93_v2":rec(SOURCE),"origin_PASS":rec(REPORT),"target":rec(target),"inventory":rec(inventory_path),
 "adaptation_script":rec(__file__),"changes":changes,"measured_delta":delta,"measured_total":total,
 "stage_sizes":stage_sizes,"embedded_counts":embedded,"lean_counts":lean,"full_theorem_audit_expected":full_audit,
 "historical_correction_segments_unchanged":segments,"prepared_and_combined_receipts_required":True,
 "auditor_executed":False,"integrator_or_lean_executed":False,"um_py_executed_or_imported":False,"approval_attributed":False}
new(folder/"PROVENIENCIA_ADAPTACAO.json",(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
assert SOURCE.read_bytes()==original
print(json.dumps({"status":provenance["status"],"auditor":rec(target),"delta":delta,"total":total,
 "full_theorem_audit_expected":full_audit,"historical_base_correction_preserved":True},ensure_ascii=False))
