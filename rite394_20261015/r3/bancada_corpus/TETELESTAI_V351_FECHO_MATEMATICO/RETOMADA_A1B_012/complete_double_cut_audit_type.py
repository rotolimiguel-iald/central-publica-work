from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists()
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
p=R/'AUDITORIA_BALANCO_DOS_CORTES_A1B.json';d=json.loads(p.read_text(encoding='utf8'))
assert d['all_axioms_allowed'] and d['negative_controls_rejected']
t=d['targets'][0];s=Path(t['source']['path']);assert pin(s)==t['source']
raw=s.read_text(encoding='utf8');start=raw.index('theorem scalarTomitaResolvent_double_cut_balance ')
end=raw.index(' := by',start)
full=raw[start:end]
assert 'Commute (scalarTomitaResolvent P) C ∧ Commute (scalarTomitaResolvent P) D ∧' in full
assert 'π (regularDomainCut P ε) * D' in full
old=t['statement'];t['statement']=full
d['metadata_correction']=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),previous_audit=pin(p),script=pin(Path(__file__)),reason='The previous extractor stopped at the first let := in the result. Full source type and compiler audit were already present; no Lean source or test result changed.',previous_truncated_statement=old,checks_rerun=False)
put(R/'AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
body='[REAL — correção documental ao lado]\n\nO extrator anterior parou no primeiro let := do resultado. O auditor Lean já imprimiu o enunciado inteiro e o código passou. Nenhuma fonte Lean, olean ou resultado de teste foi alterado ou reexecutado. A auditoria anterior é preservada, com seu pin; o consumidor deve usar AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json.\n\n```lean\n'+full+'\n```\n'
put(R/'ADENDO_TIPO_COMPLETO_BALANCO.md',body.encode('utf8'))
put(R/'ADENDO_TIPO_COMPLETO_BALANCO.json',json.dumps(dict(audit=pin(R/'AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json'),correction=d['metadata_correction']),ensure_ascii=False,indent=2).encode('utf8'))
print(full);print(json.dumps(pin(R/'AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json')))
