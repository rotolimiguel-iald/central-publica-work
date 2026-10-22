from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'dev_compile_all_positive_weight_order.py').read_text(encoding='utf8')
for a,b in [('all_positive_weight_order','regulator_weight_order'),('V351AllPositiveWeightOrder','V351RegulatorWeightOrder'),('REAPROVEITAMENTO_A1B_ORDEM_TODOS_POSITIVOS','REAPROVEITAMENTO_A1B_ORDEM_REGULADORES')]:s=s.replace(a,b)
p=R/'dev_compile_regulator_weight_order.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
