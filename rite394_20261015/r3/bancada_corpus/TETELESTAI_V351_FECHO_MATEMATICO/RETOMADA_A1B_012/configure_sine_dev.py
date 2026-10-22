from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'dev_compile_right_action_algebra.py').read_text(encoding='utf8')
s=s.replace('REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA','REAPROVEITAMENTO_A1B_APROXIMANTES_SENO').replace('dev_right_action_algebra','dev_sine_resolvent').replace('V351ScalarRightActionAlgebra','V351SineResolventApprox')
p=R/'dev_compile_sine_resolvent.py';assert not p.exists()
q=p.with_name(p.name+'.tmp');q.write_bytes(s.encode('utf8'));assert q.read_bytes()==s.encode('utf8');os.replace(q,p)

