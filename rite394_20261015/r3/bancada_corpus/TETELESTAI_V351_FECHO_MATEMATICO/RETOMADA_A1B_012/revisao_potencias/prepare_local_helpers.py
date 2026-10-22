from pathlib import Path
import hashlib, json, os
R=Path(__file__).resolve().parent.parent
BASE=R/'revisao_grafo'
OUT=Path(__file__).resolve().parent
def fresh(p,b):
    assert p.resolve().is_relative_to(OUT.resolve()) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    os.replace(t,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
rows=[]
for name in ['build_delta.py','finish_delta.py','read_author_controls.py']:
    p=BASE/name;b=p.read_bytes();fresh(OUT/'helper_origins'/name,b);s=b.decode('utf8')
    if name=='build_delta.py':
        old="'calculo':('revisao_calculo',['V351ScalarMultiplierCalculus'],5,['REAPROVEITAMENTO_A1B_CALCULO_MULTIPLICADOR'])}"
        new="'calculo':('revisao_calculo',['V351ScalarMultiplierCalculus'],5,['REAPROVEITAMENTO_A1B_CALCULO_MULTIPLICADOR']),\n 'potencias':('revisao_potencias',['V351RegularImaginaryPowers'],4,['REAPROVEITAMENTO_A1B_POTENCIAS_REGULARES']),\n 'afiliacao':('revisao_afiliacao',['V351RegularGeneratorAffiliation'],3,['REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR'])}"
        assert s.count(old)==1;s=s.replace(old,new)
        old="'revisao_grafo','revisao_grafo_espectral']"
        assert s.count(old)==2;s=s.replace(old,"'revisao_grafo','revisao_grafo_espectral','revisao_calculo','revisao_potencias','revisao_afiliacao']")
    elif name=='finish_delta.py':
        old="'calculo':['dev_multiplier_calculus/20260914_192424_032053/run.json']}[key]"
        assert s.count(old)==1
        s=s.replace(old,"'calculo':['dev_multiplier_calculus/20260914_192424_032053/run.json'],\n  'potencias':['dev_regular_powers/20260914_193204_622512/run.json'],\n  'afiliacao':['dev_regular_affiliation/20260914_194034_466190/run.json']}[key]")
    else:
        old="'calculo':'AUDITORIA_CALCULO_MULTIPLICADOR_A1B.json'}"
        assert s.count(old)==1
        s=s.replace(old,"'calculo':'AUDITORIA_CALCULO_MULTIPLICADOR_A1B.json','potencias':'AUDITORIA_POTENCIAS_REGULARES_A1B.json','afiliacao':'AUDITORIA_AFILIACAO_REGULAR_A1B.json'}")
    fresh(OUT/name,s.encode('utf8'));rows.append(dict(parent=pin(p),snapshot=pin(OUT/'helper_origins'/name),local=pin(OUT/name)))
fresh(OUT/'helper_provenance.json',(json.dumps(dict(scope='Local additive configuration for powers and affiliation; prior helpers untouched',rows=rows),indent=2)+'\n').encode())
