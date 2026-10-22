from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'checkpoint_status.py').read_text(encoding='utf8')
s=s.replace("record=dict(timestamp=stamp,input=pin(inp),status=data,", "full_trace=data.get('full_trace_constructed',False)\nif full_trace:\n    audit=json.loads((R/data['trace_audit']).read_text(encoding='utf8'))\n    review=json.loads((R/data['trace_review']).read_text(encoding='utf8'))\n    assert audit['full_trace_constructed'] and review['full_trace_constructed']\n    assert audit['all_axioms_allowed'] and review['mathematical_review_passed']\n    assert all(not review[k] for k in ['P0','P1','P2'])\nrecord=dict(timestamp=stamp,input=pin(inp),status=data,")
s=s.replace('full_trace_constructed=False,gate_changed=False','full_trace_constructed=full_trace,gate_changed=False')
s=s.replace("d.setdefault('append_only_checkpoints',[]).append(pin(p));put(jp", "d.setdefault('append_only_checkpoints',[]).append(pin(p));d['latest_validated_checkpoint']=pin(p);put(jp")
p=R/'checkpoint_status_v2.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print('Prepared checkpoint_status_v2.py; no memory changed.')
