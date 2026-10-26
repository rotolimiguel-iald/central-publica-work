from pathlib import Path
import re
p=Path(__file__).resolve().parent/'TGLExt/PonteDaEscalaDual.lean'
s=p.read_text(encoding='utf-8').split('-- Explicit axiom reports')[0].rstrip()+'\n'
names=re.findall(r'^(?:def|abbrev|theorem)\s+(\w+)',s,re.M)
s+='\n-- Explicit axiom reports\n'+''.join('#print axioms TGLExt.PonteDaEscalaDual.'+n+'\n' for n in names)
p.write_text(s,encoding='utf-8')
print(len(names))
