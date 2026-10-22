from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'run_inverse_limit_faithful_replay.py').read_text(encoding='utf8')
s=s.replace("['V351InverseLimitFaithful.lean', 'AuditA1InverseLimitFaithful.lean']","['V351RegularCoreTraceContract.lean']")
s=s.replace('inverse_limit_faithful_attempts','existing_contract_dependency_attempts').replace('TGLExt.AuditA1InverseLimitFaithful','TGLExt.V351RegularCoreTraceContract')
p=R/'run_existing_contract_dependency.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
