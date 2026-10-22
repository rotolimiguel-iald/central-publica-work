"""Prepare auditor93 v2 against its preserved historical base, without executing the auditor."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
SOURCE = BASE / "AUDITORIA_INTEGRACAO_93_20260909_203251_909834/audit_integration_93.py"
V1_PROVENANCE = SOURCE.parent / "PROVENIENCIA_ADAPTACAO.json"
COPY = BASE / "COPIA_INTEGRADA_20260909_203352_868028"

def rec(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def new(path, raw):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw

original = SOURCE.read_bytes()
text = original.decode("utf-8")
changes = []
def replace(old, updated):
    global text
    assert text.count(old) == 1, (old, text.count(old))
    text = text.replace(old, updated)
    changes.append({"from": old, "to": updated, "occurrences": 1})

replace('checks=[];inputs={}', '''checks=[];inputs={}
def observe_live_canonical(p):
 # Diagnostic only. This mutable path is never added to the immutable input ledger.
 p=Path(p)
 before=p.stat();raw=p.read_bytes();after=p.stat()
 return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
  "observed_utc":datetime.now(timezone.utc).isoformat(),
  "mtime_ns_before":before.st_mtime_ns,"mtime_ns_after":after.st_mtime_ns,
  "stable_during_capture":before.st_size==after.st_size==len(raw) and before.st_mtime_ns==after.st_mtime_ns,
  "role":"LIVE_DIAGNOSTIC_NOT_HISTORICAL_INTEGRATION_BASE"}
''')

replace('canonicalpath=Path(stages[0]["ir"]["source_um"]["path"])\ncanonical=remember(canonicalpath)\ncanon,cast,cbytes,csentinels=table(canonicalpath)',
'''historical_source_record=stages[0]["ir"]["source_um"]
canonicalpath=Path(historical_source_record["path"])
historical_snapshot_path=stages[0]["folder"]/"um_ORIGINAL_SNAPSHOT.py"
canonical=remember(historical_snapshot_path)
ck("historical_snapshot_record_exact",canonical==stages[0]["ir"]["original_copy"] and same(stages[0]["ir"]["original_copy"]))
ck("historical_source_bytes_hash_attested_by_snapshot",all(canonical[k]==historical_source_record[k] for k in ["bytes","sha256"]))
canon,cast,cbytes,csentinels=table(historical_snapshot_path)
current_canonical_start=observe_live_canonical(canonicalpath)''')

replace(' ck(label+":source_pin",same(ir["source_um"]))',
''' if number:
  ck(label+":source_pin",same(ir["source_um"]))
 else:
  ck(label+":historical_source_pin_from_snapshot",all(rec(sp)[k]==ir["source_um"][k] for k in ["bytes","sha256"]))''')

replace(' ck(label+":snapshot_bytes_exact",sp.read_bytes()==source.read_bytes())',
''' ck(label+":snapshot_recorded_path_exact",Path(ir["original_copy"]["path"]).resolve()==sp.resolve())
 if number:
  ck(label+":snapshot_bytes_exact",sp.read_bytes()==source.read_bytes())
 else:
  ck(label+":historical_snapshot_bytes_exact",sp.read_bytes()==historical_snapshot_path.read_bytes() and rec(sp)==canonical)''')

replace(' ck(label+":configured_source",cfg["source_um_sha256"]==rec(source)["sha256"] and Path(cfg["source_um"]).resolve()==source.resolve())',
''' if number:
  ck(label+":configured_source",cfg["source_um_sha256"]==rec(source)["sha256"] and Path(cfg["source_um"]).resolve()==source.resolve())
 else:
  ck(label+":configured_historical_source",cfg["source_um_sha256"]==ir["source_um"]["sha256"]==canonical["sha256"] and Path(cfg["source_um"]).resolve()==source.resolve())''')

replace('"source":remember(source),"snapshot":remember(sp)',
        '"source":remember(source) if number else dict(ir["source_um"]),"source_validation_mode":"FROZEN_PREDECESSOR_CURRENT_BYTES" if number else "HISTORICAL_RECORDED_PATH_HASH_AND_PRESERVED_SNAPSHOT","snapshot":remember(sp)')

replace('ck("no_new_full_names_collide_with_canonical",not collisions,collisions)',
        'ck("no_new_full_names_collide_with_historical_snapshot",not collisions,collisions)')

replace('ck("prepared_and_combined_present", prepared is not None and combined is not None)',
'''ck("prepared_and_combined_present", prepared is not None and combined is not None)
current_canonical=observe_live_canonical(canonicalpath)
live_diagnostic={"before":current_canonical_start,"after":current_canonical,
 "changed_during_audit":any(current_canonical_start[k]!=current_canonical[k] for k in ["bytes","sha256","mtime_ns_after"]),
 "differs_from_historical_source":any(current_canonical[k]!=historical_source_record[k] for k in ["bytes","sha256"]),
 "used_as_integration_base":False,
 "scope_note":"The live source may have advanced externally. Its difference is reported, never converted to a historical preservation PASS. All frozen predecessors retain strict pin and byte checks."}''')

replace('"canonical":canonical,"canonical_snapshot":stage_rows[0]["snapshot"],"current_canonical":canonical',
        '"canonical":canonical,"canonical_role":"HISTORICAL_SNAPSHOT_BASE","historical_source_record":historical_source_record,"canonical_snapshot":stage_rows[0]["snapshot"],"current_canonical":current_canonical,"current_canonical_diagnostic":live_diagnostic')

replace('"with_canonical":collisions', '"with_historical_canonical_snapshot":collisions')
replace('"limits":["Static integration audit; no runtime execution, seal or physical verdict."',
        '"limits":["The first integration source is verified against its preserved historical snapshot and recorded source path/hash; the live canonical is a separate diagnostic. This audit does not attest unchanged live canonical bytes or integration into its current version.","Static integration audit; no runtime execution, seal or physical verdict."')

replace('# Auditoria estática da integração93', '# Auditoria estática da integração93 — versão 2, base histórica')
replace('A genealogia foi percorrida: canônico → lote63 → delta9 → delta5 → delta6 → delta10.',
        'A genealogia foi percorrida: snapshot histórico do canônico → lote63 → delta9 → delta5 → delta6 → delta10.')
replace('AST e bytes fora da tabela de arquivos embutidos foram comparados em toda a cadeia.',
'''O estágio inicial usa o snapshot preservado, cujo tamanho e hash são conferidos contra os registros source_um e original_copy da época. O caminho do source_um vivo é apenas o endereço histórico registrado; seus bytes atuais não são usados como base.

AST e bytes fora da tabela de arquivos embutidos foram comparados em toda a cadeia, a partir desse snapshot histórico.''')
replace('O limite de auditoria permanece explícito: dependências externas transitivas não foram todas recompiladas ou integralmente hashadas.',
'''Diagnóstico separado do canônico vivo: {current_canonical['bytes']} bytes; SHA-256 {current_canonical['sha256']}. Difere do source_um histórico: {live_diagnostic['differs_from_historical_source']}. Mudou entre as duas observações desta auditoria: {live_diagnostic['changed_during_audit']}. As observações não são base da integração nem um teste de preservação da versão atual.

O limite de auditoria permanece explícito: dependências externas transitivas não foram todas recompiladas ou integralmente hashadas.''')

ast.parse(text)
# Read the actual lineage and enumerate non-Chatgpt references before freezing this adaptation.
stages=[];path=COPY/"INTEGRATION_RESULT.json"
while True:
    data=json.loads(path.read_bytes());stages.append((path,data))
    parent=data.get("predecessor_integration_result")
    if not parent:break
    assert rec(parent["path"])["sha256"]==parent["sha256"]
    path=Path(parent["path"])
stages.reverse()
first=stages[0][1]
snapshot=stages[0][0].parent/"um_ORIGINAL_SNAPSHOT.py"
snapshot_pin=rec(snapshot)
assert snapshot_pin==first["original_copy"]
assert all(snapshot_pin[k]==first["source_um"][k] for k in ["bytes","sha256"])
outside_leaf_sources=[m["source"]["path"] for _,stage in stages for m in stage["modules"] if not Path(m["source"]["path"]).resolve().is_relative_to(BASE)]
plan_path=BASE/"INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415/BUILD_SUCCESSOR_20260909_203414_443930/BUILD_PLAN.json"
plan=json.loads(plan_path.read_bytes())
outside_plan_sources=[r["path"] for r in plan["source_files"] if not Path(r["path"]).resolve().is_relative_to(BASE)]
assert not outside_leaf_sources and not outside_plan_sources
assert all(Path(stage["source_um"]["path"]).resolve().is_relative_to(BASE) for _,stage in stages[1:])
target=OUT/"audit_integration_93_v2.py"
new(target,text.encode("utf-8"))
provenance={"status":"PREPARED_NOT_EXECUTED","created_utc":datetime.now(timezone.utc).isoformat(),
 "source_v1":rec(SOURCE),"source_v1_provenance":rec(V1_PROVENANCE),"target_v2":rec(target),"adaptation_script":rec(__file__),
 "changes":changes,"historical_source_record":first["source_um"],"historical_snapshot":snapshot_pin,
 "lineage_integration_receipts":[rec(path) for path,_ in stages],"current_build_plan":rec(plan_path),
 "reference_review":{"only_live_source_path":first["source_um"]["path"],"all_later_predecessors_in_Chatgpt":True,
  "outside_Chatgpt_leaf_sources":outside_leaf_sources,"outside_Chatgpt_plan_source_files":outside_plan_sources,
  "unchanged_strict_checks":"Later predecessor source pins, byte-identical snapshots, modules, transpositions, receipts, source_files, compiled artifact presence and immutable input stability.",
  "transitive_scope_limit":"External dependency descriptors in prior build receipts are reported by those receipts; this auditor does not newly traverse or hash every external dependency."},
 "auditor_executed":False,"integration_executed":False,"lean_executed":False,"um_py_executed_or_imported":False,
 "physical_or_external_approval_attributed":False}
new(OUT/"PROVENIENCIA_CORRECAO_HISTORICA.json",(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
assert SOURCE.read_bytes()==original
print(json.dumps({"status":provenance["status"],"auditor":rec(target),"historical_snapshot":snapshot_pin,
 "changes":len(changes),"outside_leaf_sources":outside_leaf_sources,"outside_plan_sources":outside_plan_sources},ensure_ascii=False))
