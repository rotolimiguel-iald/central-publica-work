"""Bind the exact ladder guard to the actual program's external_ladder object."""
from diary_r1 import ROOT,new,pin
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
src=OUT/'runtime/time_runtime_v394_r2.py'
text=src.read_text(encoding='utf-8')
old="    clean=report.get('n_theorems_clean'); counted=report.get('n_theorems_expected')"
replacement="    ladder=core.get('external_ladder') or {}\n    clean=ladder.get('n_theorems_clean'); counted=ladder.get('n_theorems_expected')"
assert text.count(old)==1;text=text.replace(old,replacement)
dst=OUT/'runtime/time_runtime_v394_r3.py';new(dst,text)
new(OUT/'PREREGISTRO_INTEGRACAO_R3.json',{'previous':pin(OUT/'PREREGISTRO_INTEGRACAO_R2.json'),'R2':pin(src),'R3':pin(dst),
 'reason':'Actual v393 AST: ladder counts live in core.external_ladder. Its explicit7045flags differ from all7120flags. R2 would fail closed in actualprogram. Integration appends new flags to both the parser table and the actual ladder list.',
 'verification':'Run actual prove_external_ladder on fresh root Audit evidence, then actual consumer; prohibit a fabricated top-level ladder on kernel_formalization.',
 'unchanged':'Model, physical parameters, tolerances and scientific tests unchanged; prior sources preserved.'})
print(pin(dst))
