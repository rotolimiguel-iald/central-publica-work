from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
OUT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
BASE=OUT/'maxwell_global'
WORK=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016')
FOCK=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\fock_construction')
M=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
REF=WORK/'FECHO_MISSION_REFERENCE.json'
ACTOR={'kind':'agent','id':'codex-r50-circular-field-transport'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p);b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str): yield o
        for v in o.values():yield from collect(v)
    elif isinstance(o,list):
        for v in o:yield from collect(v)
checked={}
def verify(o):
    for x in collect(o):
        key=(x['path'],x['sha256'].lower())
        if key in checked:continue
        a=pin(x['path']);assert a['sha256']==key[1],a
        if 'bytes' in x:assert a['bytes']==x['bytes'],a
        checked[key]=a
roots=[OUT/'orbital_rotation/attempts',OUT/'kms_strip/attempts']
def green(source,required=True):
    source=Path(source); matches=[]
    for root in roots:
        for src in root.glob('*/'+source.name):
            rp=src.parent/'RECEIPT.json'
            if not rp.exists():continue
            r=read(rp)
            if r.get('exit_code')!=0 or src.read_bytes()!=source.read_bytes():continue
            matches.append((src,rp,r))
    if not matches:
        assert not required,source
        return {'source':pin(source),'status':'DECLARADO_PENDING_BUILD'}
    src,rp,r=sorted(matches,key=lambda x:x[0].parent.name)[-1]
    verify(r)
    axp=src.parent/'AXIOMS.txt';ax=axp.read_text(encoding='utf-8')
    lists=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",ax)
    assert lists and 'sorryAx' not in ax and 'error:' not in ax
    assert all(set(v.strip() for v in s.split(','))<={'propext','Classical.choice','Quot.sound'} for _,s in lists)
    return {'source':pin(source),'status':'COMPILED_EXIT0_NOT_INDEPENDENTLY_REVIEWED_HERE',
      'receipt':pin(rp),'axioms':pin(axp),'seconds':r['seconds'],'exit_code':0,
      'axiom_declarations':[n for n,_ in lists],'only_standard_trio':True,'source_matches_attempt':True}
candidates=[BASE/'FockSegalUnitaryTransportR1.lean',BASE/'CircularPhysicalFieldTransportR1.lean',
    BASE/'AxisCompactCircularTransportR1.lean']
new=[]
for p in candidates:
    text=p.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',text,re.M)
    assert 'set_option maxHeartbeats 400000' in text
    assert 'set_option synthInstance.maxHeartbeats 500000' in text
    new.append({'source':pin(p),'imports':re.findall(r'^import (.+)$',text,re.M),
        'expected_print_count':len(re.findall(r'^#print axioms ',text,re.M)),
        'public_print_declarations':re.findall(r'^#print axioms (.+)$',text,re.M)})
supplier_paths=[BASE/'RegularCircularTransportR2.lean',OUT/'orbital_rotation/PhysicalSmearTranslationR2.lean',
    BASE/'UnitaryFourierRealStressR2.lean',BASE/'AxisCompactFockTranslationR2.lean']
suppliers=[green(p) for p in supplier_paths]
candidate_builds=[green(p,False) for p in candidates]
extra=[BASE/'WeakSegalDistributionR3.lean',BASE/'WickQuadraticFormR6.lean',
  BASE/'RegularCoherentTransportR1.lean',BASE/'PhysicalSchwartzMaxwellR1.lean',
  BASE/'RegularMaxwellFockDomainR5.lean',BASE/'AxisCompactProfileDensityR4.lean',
  BASE/'SmoothLinearMomentumCutoffR3.lean',BASE/'CompactFockBoostDerivativeR2.lean',
  OUT/'orbital_rotation/ScreenCircularBasisR2.lean',
  OUT/'maxwell_annihilation/ExponentialAnnihilationR2.lean',
  OUT/'maxwell_annihilation/CreationAndSegalR2.lean',OUT/'maxwell_annihilation/AnnihilationDomainR1.lean',
  FOCK/'BosonicFock.lean',FOCK/'BosonicFockGroupActions.lean',
  M/'Analysis/InnerProductSpace/LinearMap.lean',M/'Topology/Algebra/Support.lean',
  M/'Analysis/Normed/Operator/LinearIsometry.lean',
  BASE/'R49_MAXWELL_GAP_INVENTORY_R1.json']
if '--write' not in __import__('sys').argv:
    print(json.dumps({'candidates':new,'builds':[{'source':b['source']['path'],'status':b['status'],'seconds':b.get('seconds')} for b in candidate_builds],
      'suppliers':[{'source':b['source']['path'],'seconds':b['seconds']} for b in suppliers],
      'verified_pins':len(checked)},ensure_ascii=False))
    raise SystemExit(0)
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
 input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
response=json.loads(run.stdout);assert response['ok'],response
p=response['result']
r8=next(x for x in p['projection']['active'] if x['id']=='R8')
report={
 'schema':'iald-lean-candidate/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'DECLARADO_PENDING_COMPLETE_BUILD_AND_INDEPENDENT_REVIEW','author':ACTOR,
 'requirement':'R8','handle':'r50-circular-field-transport','requirement_satisfied':False,
 'mission_reference':pin(REF),'mission_receipt':p['receipt'],'projection_sha256':p['projection_sha256'],
 'criterion':r8['criterion'],'lease_observed':r8['lease'],
 'handoff':pin(OUT/'mission_resume_20261016/LIVE_R50_HANDOFF_R8_20261016T195704_412427Z_efeee276_RECEIPT.json'),
 'sources':new,'existing_suppliers':suppliers,'root_builds_observed':candidate_builds,
 'direct_reuse':[pin(f) for f in extra],
 'supplier_receipt_pins_verified':len(checked),
 'supplier_receipt_bytes_verified':sum(x['bytes'] for x in checked.values()),
 'verification_scope':'Cada par path/sha256 embutido nos recibos verdes observados foi conferido, além dos pinos diretos. O autor não compilou. Recibos de dependências não foram recursivamente reabertos para auditoria científica.',
 'mathematics':[
  'O gamma existente transporta o domínio exponencial concreto por reindexação das sínteses finitas. Aniquilação é entrelaçada nessa síntese; criação é identificada por totalidade exponencial e preservação do produto interno.',
  'Segal é transportado por linearidade do mesmo gamma. A saída de criação/Segal não é declarada membro do domínio exponencial.',
  'circularSmearCLM é exatamente circularH1.symm composto com physicalSmearCLM; circularField é o Segal desse rótulo. A igualdade inclui gamma circularH1 no vetor e no domínio.',
  'regularFockDomain entra no domínio exponencial por inclusão provada. regularCircular e o inverso usam regularGamma existente, preservando norma; gamma circularH1 entrelaça U1/B0.',
  'A amplitude é sqrt(unitaryFourierStressScale), com quadrado igual ao fator já fixado ((2*pi)^3)^(-1). Não há parâmetro ajustável. physicalField antigo fica intacto; normalizedPhysicalField é sua amplitude real fixa.',
  'O Wick bilocal é transportado no domínio exponencial inteiro e, por inclusão, em todas as somas coerentes regulares. As duas funções teste e os vetores transformados permanecem explícitos.',
  'A mesma fibra circular leva representantes compactos suaves ao mesmo suporte com a mesma lacuna de eixo. Reindexação dos coeficientes únicos transporta AxisCompactFock e o próprio axisCompactFockDomain.'
 ],
 'new_mathematical_premises':[],
 'scope_limits':[
  'A identificação local de Wick no ponto coincidente com unitaryFourierPointStressForm não é provada nem assumida.',
  'Não se afirma que o tensor de perfil é invariante sob circularH1 mantendo os vetores fixos; os teoremas transportam os estados.',
  'A testemunha nova é somente de excitação não nula do campo normalizado; não substitui a testemunha de energia nem Regular completos já construídos.',
  'R8 integral, incluindo tensor/campo/rede/fonte geométrica, permanece aberto. A existência de RemainingModularCoreInput e a seleção de relógio físico não são produzidas.'
 ],
 'next_exact_obligation':'Identificar a restrição Wick local construída do normalizedPhysicalField (ou do normalizedCircularField com regularCircular nos estados) e a contração de Maxwell com unitaryFourierPointStressForm, usando unitaryFourierFieldAmplitude_sq; sem hipótese da igualdade almejada.',
 'limits':{'maxHeartbeats':400000,'synthInstance.maxHeartbeats':500000},
 'original_sources_modified':False,'author_builds':0,'provider_calls':0,'production_changes':False,
 'mission_mutations':False,'script':pin(Path(__file__))
}
dest=BASE/'CIRCULAR_FIELD_TRANSPORT_CANDIDATE_R50_R1.json'
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
assert not dest.exists()
tmp=dest.with_name(dest.name+'.tmp_r50')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,dest);assert dest.read_bytes()==data
print(json.dumps({'manifest':pin(dest),'sources':[x['source'] for x in new],
 'verified_pins':len(checked),'revision':p['receipt']['revision'],
 'builds':[{'name':Path(b['source']['path']).name,'status':b['status'],'seconds':b.get('seconds')} for b in candidate_builds]},ensure_ascii=False))

