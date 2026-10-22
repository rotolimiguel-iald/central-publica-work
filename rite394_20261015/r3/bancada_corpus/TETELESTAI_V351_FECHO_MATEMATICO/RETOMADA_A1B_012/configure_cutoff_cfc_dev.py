from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'dev_compile_sine_resolvent.py').read_text(encoding='utf8')
s=s.replace('REAPROVEITAMENTO_A1B_APROXIMANTES_SENO','REAPROVEITAMENTO_A1B_CFC_CORTES').replace('dev_sine_resolvent','dev_cutoff_cfc').replace('V351SineResolventApprox','V351InverseCutoffCFC')
p=R/'dev_compile_cutoff_cfc.py';assert not p.exists()
b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)

