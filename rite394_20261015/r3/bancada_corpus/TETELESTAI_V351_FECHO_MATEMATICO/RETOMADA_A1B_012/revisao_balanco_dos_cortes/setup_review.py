from pathlib import Path
import hashlib, json, os

R = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
OUT = R / 'revisao_balanco_dos_cortes'
PREV = R / 'revisao_implementador_modular'

def pin(p):
    b = p.read_bytes()
    return {'path':str(p), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}

def fresh(name, content):
    p = OUT / name
    assert not p.exists(), p
    b = content.encode('utf-8')
    t = p.with_name(p.name + '.tmp')
    with t.open('xb') as f:
        f.write(b)
    assert t.read_bytes() == b
    os.replace(t, p)

build = (PREV / 'build_delta.py').read_text(encoding='utf-8-sig')
config = "\nCONFIG['balanco_dos_cortes']=('revisao_balanco_dos_cortes',['V351ModularCutBalance'],1," + repr(json.loads((R/'delivery_configs/modular_cut_balance.json').read_bytes())['docs']) + ")\n"
build = build.replace('\ndef now():', config + '\ndef now():', 1)
build = build.replace("'revisao_vetores_fixos_modulares']:", "'revisao_vetores_fixos_modulares','revisao_implementador_modular']:")
old = "assert p.resolve().is_relative_to(V.resolve()) or any(p.resolve().is_relative_to((R/x[0]).resolve()) for x in CONFIG.values()),p"
new = "assert p.resolve().is_relative_to(V.resolve()) or p.resolve().is_relative_to((R/'revisao_balanco_dos_cortes').resolve()),p"
assert old in build
build = build.replace(old,new)
old = "nms=re.findall(r'^#print axioms\\s+(\\S+)',code,re.M)\n   if not nms:nms=re.findall(r'^(?:theorem|def)\\s+(\\S+)',code,re.M)"
new = "nms=re.findall(r'^(?:theorem|def)\\s+(\\S+)',code,re.M)"
assert old in build
build = build.replace(old,new)
fresh('build_delta.py',build)
helpers = (PREV/'review_helpers.py').read_text(encoding='utf-8-sig')
helpers = helpers.replace("OUT=R/'revisao_implementador_modular'", "OUT=R/'revisao_balanco_dos_cortes'")
helpers = helpers.replace('A1_MODULAR_IMPLEMENTATION_REVIEW_ACCEPTED__QUADRATIC_TRACE_OPEN', 'A1_MODULAR_CUT_BALANCE_REVIEW_ACCEPTED__QUADRATIC_TRACE_OPEN')
helpers = helpers.replace('REVIEW_A1_MODULAR_IMPLEMENTATION_FINAL','REVIEW_A1_MODULAR_CUT_BALANCE_FINAL')
fresh('review_helpers.py',helpers)
negative = (PREV/'negative_control.py').read_text(encoding='utf-8-sig').replace('BadModularImplementationRightSignChanged','BadModularCutBalanceComplementChanged')
fresh('negative_control.py',negative)
fresh('helper_provenance.json',json.dumps({'source_helpers':[pin(PREV/n) for n in ['build_delta.py','review_helpers.py','negative_control.py']], 'local_helpers':[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','negative_control.py']], 'changes':['New delta configuration and prior32 pin preservation','Writes restricted to V and current review folder','Public declarations selected independently of private print directives','Negative uses frozen complement-change probe'],'old_helpers_modified':False},ensure_ascii=False,indent=2)+'\n')
print('Prepared independent review helpers', OUT)
