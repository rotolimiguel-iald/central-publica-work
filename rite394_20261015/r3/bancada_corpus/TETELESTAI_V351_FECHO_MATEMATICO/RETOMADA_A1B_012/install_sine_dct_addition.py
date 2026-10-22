from pathlib import Path
import os
R=Path(__file__).resolve().parent
p=R/'k/TGLExt/V351SineResolventApprox.lean';s=p.read_text(encoding='utf8')
assert 'scalarMultiplier_sequence_tendsto' not in s
s=s.replace('    change cfc f M u x = _\n','')
a=s.index('#print axioms regularSineWindowCore')
s=s[:a]+(R/'sine_dct_addition.lean.part').read_text(encoding='utf8')+'\n'+s[a:]
s=s.replace('end\nend TGLV350.Regular',''.join('#print axioms '+n+'\n' for n in ['regularSineResolvent_nonneg','regularSineResolvent_norm_le','regularSineResolvent_tendsto','regularSpectralResolvent_right'])+'end\nend TGLV350.Regular')
q=p.with_name(p.name+'.tmp');b=s.encode('utf8');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)

