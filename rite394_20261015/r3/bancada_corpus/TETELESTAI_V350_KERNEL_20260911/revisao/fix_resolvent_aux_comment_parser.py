from pathlib import Path
import datetime,json
R=Path(__file__).resolve().parent;p=R/'run_resolvent_aux_review.py';raw=p.read_bytes()
backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));backup.write_bytes(raw);assert backup.read_bytes()==raw
code=raw.decode();old="for n in re.findall(r'^(?:noncomputable\\s+)?(?:def|theorem|abbrev|structure|instance)\\s+([\\w.]+)',txt,re.M)]"
new="for n in re.findall(r'^(?:noncomputable\\s+)?(?:def|theorem|abbrev|structure|instance)\\s+([\\w.]+)',re.sub(r'/\\-.*?\\-/|--[^\\n]*',lambda m: '\\n'*m[0].count('\\n'),txt,flags=re.S),re.M)]"
assert old in code
updated=code.replace(old,new).encode();tmp=p.with_suffix('.py.tmp');tmp.write_bytes(updated);assert tmp.read_bytes()==updated;tmp.replace(p)
failed=max(R.glob('resolvent_aux_independent_*'));note={'status':'REVIEWER_PREPARATION_FAILURE_BEFORE_LEAN','cause':'Declaration inventory matched the word structure at the start of a block-comment line. Parser now excludes comments. No author source changed; no Lean process was run in this failed preparation.','runner_backup':str(backup)}
q=failed/'preparation_failure.json';assert not q.exists();q.write_bytes(json.dumps(note,indent=2).encode())
