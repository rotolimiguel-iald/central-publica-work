"""Preserve preregistered R1 and write R2 for the concrete review findings."""
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
src=OUT/'runtime/time_runtime_v394.py'
text=src.read_text(encoding='utf-8')
old='    return phase_lift/(2*omega)'
new_text='''    result = (phase_lift/omega)*0.5 if phase_lift <= omega else (phase_lift*0.5)/omega
    import math
    if not math.isfinite(result) or (phase_lift > 0 and result <= 0):
        raise ValueError('phase clock overflow or underflow')
    return result'''
assert text.count(old)==1
text=text.replace(old,new_text)
old="    formal=bool(required) and report.get('all_verified') is True"
new_text="""    expected=_V394_FORMAL_CONTRACT['expected_ladder']
    clean=report.get('n_theorems_clean'); counted=report.get('n_theorems_expected')
    exact_ladder=(type(expected) is int and type(clean) is int and type(counted) is int
                  and clean == counted == expected)
    formal=bool(required) and report.get('all_verified') is True and exact_ladder"""
assert text.count(old)==1;text=text.replace(old,new_text)
text=text.replace("per[theorem]=isinstance(values,list) and set(values)<=trio", "per[theorem]=isinstance(values,list) and all(isinstance(x,str) for x in values) and set(values)<=trio")
text=text.replace("'formal_theorems':per,", "'exact_ladder':exact_ladder,'formal_theorems':per,")
needle="    # Controls test genuine failures, independent of the main verdict."
assert text.count(needle)==1
text=text.replace(needle,"    close('clock_phase:overflow_avoided',_v394_clock_phase(1e308,1e308),.5)\n"+needle)
needle="    refused('negative_input:zero_coherence'"
where=text.index(needle)
text=text[:where]+"    refused('clock_phase:unrepresentable',lambda:_v394_clock_phase(1.,5e-324))\n    refused('clock_phase:underflow',lambda:_v394_clock_phase(5e-324,1e308))\n"+text[where:]
dst=OUT/'runtime/time_runtime_v394_r2.py'
new(dst,text)
new(OUT/'PREREGISTRO_INTEGRACAO_R2.json',{'prior':pin(OUT/'PREREGISTRO_INTEGRACAO_R1.json'),'R1_source':pin(src),'R2_source':pin(dst),
    'reason':'Independent review: phase clock overflow/underflow and unconsumed exact ladder guard. No tolerance relaxed or scientific model changed.',
    'new_controls':['phase=omega=1e308 -> time0.5','unrepresentable time refused','positive time underflow refused','n_clean=n_expected=contract expected exact nonboolean integers required'],
    'scope':'R1 remains immutable; all previous tests and tolerances inherited; explicit physical identity only in stated M2 model.'})
print(pin(dst))
