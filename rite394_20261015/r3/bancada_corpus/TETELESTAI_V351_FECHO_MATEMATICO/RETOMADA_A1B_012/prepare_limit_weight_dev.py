from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'dev_compile_regulator_weight_order.py').read_text(encoding='utf8')
for a,b in [('regulator_weight_order','inverse_limit_weight'),('V351RegulatorWeightOrder','V351InverseLimitWeight'),('REAPROVEITAMENTO_A1B_ORDEM_REGULADORES','REAPROVEITAMENTO_A1B_LEIS_PESO_LIMITE')]:s=s.replace(a,b)
p=R/'dev_compile_inverse_limit_weight.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
