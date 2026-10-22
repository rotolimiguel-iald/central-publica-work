from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
OUT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
BASE=OUT/'maxwell_global'
WORK=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016')
FOCK=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\fock_construction')
M=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
REF=WORK/'FECHO_MISSION_REFERENCE.json'
ACTOR={'kind':'agent','id':'codex-r51-wick-local-identification'}
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
candidates=[BASE/'RegularPointAnnihilationR2.lean',BASE/'LocalWickStressIdentificationR2.lean',
 BASE/'PointAnnihilationSmearingR2.lean']
new=[]
for f in candidates:
 t=f.read_text(encoding='utf-8')
 assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',t,re.M)
 assert 'set_option maxHeartbeats 400000' in t
 assert 'set_option synthInstance.maxHeartbeats 500000' in t
 new.append({'source':pin(f),'imports':re.findall(r'^import (.+)$',t,re.M),
 'expected_print_count':len(re.findall(r'^#print axioms ',t,re.M)),
 'public_print_declarations':re.findall(r'^#print axioms (.+)$',t,re.M)})
supplier_paths=[BASE/'CircularPhysicalFieldTransportR1.lean',BASE/'PhysicalSmearWavePairingR2.lean',
 BASE/'RegularFockPointStressR4.lean',BASE/'CalibratedFockStressDomainBridgeR1.lean',
 BASE/'RegularFockStressContinuityR4.lean']
suppliers=[green(f) for f in supplier_paths]
builds=[green(f,False) for f in candidates]
extra=[BASE/'RegularMaxwellFockDomainR5.lean',BASE/'WickQuadraticFormR6.lean',
 BASE/'CoherentPointMaxwellR1.lean',BASE/'CoherentPointStressR2.lean',
 BASE/'ProfileMaxwellLowerWaveR3.lean',BASE/'ProfileWaveFourierPairingR3.lean',
 BASE/'FiniteCoherentKernelR3.lean',BASE/'FiniteCoherentKernelCalculusR2.lean',
 BASE/'UnitaryFourierFockStressR1.lean',BASE/'MaxwellStressJetAlgebraR3.lean',
 BASE/'R49_MAXWELL_GAP_INVENTORY_R1.json',
 OUT/'maxwell_annihilation/AnnihilationDomainR1.lean',
 OUT/'maxwell_annihilation/ExponentialAnnihilationR2.lean',
 M/'LinearAlgebra/Finsupp/LinearCombination.lean',M/'Analysis/InnerProductSpace/Basic.lean',
 M/'MeasureTheory/Integral/Prod.lean',M/'MeasureTheory/Integral/Bochner/Basic.lean',
 M/'MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',
 M/'MeasureTheory/Function/L1Space/Integrable.lean']
for f in extra:pin(f)
summary={'sources':[x['source'] for x in new],'verified_pins':len(checked),
 'builds':[{'source':Path(b['source']['path']).name,'status':b['status'],'seconds':b.get('seconds')} for b in builds]}
if '--write' not in __import__('sys').argv:
 print(json.dumps(summary,ensure_ascii=False));raise SystemExit(0)
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
 input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
response=json.loads(run.stdout);assert response['ok'],response
p=response['result'];r8=next(x for x in p['projection']['active'] if x['id']=='R8')
assert r8['status']=='working'
report={
 'schema':'iald-lean-candidate/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'DECLARADO_PENDING_BUILD_AND_INDEPENDENT_REVIEW','author':ACTOR,
 'requirement':'R8','handle':'r51-wick-local-identification','requirement_satisfied':False,
 'mission_reference':pin(REF),'mission_receipt':p['receipt'],'projection_sha256':p['projection_sha256'],
 'criterion':r8['criterion'],'lease_observed':r8['lease'],
 'handoff':pin(OUT/'mission_resume_20261016/LIVE_HANDOFF_R8_20261016T202937_165515Z_f7b550eb_RECEIPT.json'),
 'sources':new,'existing_suppliers':suppliers,'root_builds_observed':builds,
 'direct_reuse':[pin(f) for f in extra],
 'supplier_receipt_pins_verified':len(checked),
 'supplier_receipt_bytes_verified':sum(x['bytes'] for x in checked.values()),
 'verification_scope':'Todos os pares path/sha256 dos recibos verdes observados e pinos diretos foram conferidos. O autor não compilou nem fez revisão independente de sua própria fonte.',
 'mathematics':[
 'regularDiagonal é um endomorfismo linear do regularFockDomain existente, calculado pelos coeficientes únicos já provados e seus vetores exponenciais. Não se constrói operador limitado de avaliação em H1/Fock.',
 'A escolha de autovalor inner f h coincide, por expansão finita e aniquilação exponencial existente, com a aniquilação original inclusive o domínio invariante. regularWick usa literalmente quatro termos de aniquilação; sua versão smeared coincide com WickForm.quadratic.',
 'physicalSmear_inner_wave descarrega o autovalor smeared, com contração 1/2 e dois sinais métricos para subir os índices. A amplitude real fixa é sqrt(unitaryFourierStressScale); seu quadrado é o fator Fourier (2*pi)^(-3).',
 'pointAnnihilation usa o autovalor normalizado lowerProfileWave no mesmo domínio regular. pointWick usa esses aniquiladores nos quatro termos, antes de qualquer menção ao tensor de perfil.',
 'A expansão coerente determina o núcleo bilocal contínuo; sua restrição x=y é avaliação de uma forma regular no domínio explícito. A contração Maxwell é provada igual a unitaryFourierPointStressForm, e então ao tensor calibrado preexistente.',
 'PointAnnihilationSmearingR2 constrói integrabilidade e igualdade de Bochner entre o aniquilador pontual integrado e o aniquilador físico normalizado. O lema genérico com integrabilidade como premissa é consumido por uma prova concreta usando o pareamento Fourier antigo e somas finitas.',
 'A igualdade circular conserva regularCircular nos dois estados; não se afirma invariância do tensor mantendo os vetores fixos.'
 ],
 'new_physical_premises':[],
 'scope_limits':[
 'Candidatas apenas: a identificação local só poderá ser afirmada após compilações e revisão independente das peças, incluindo a ligação efetiva de smearing.',
 'O objeto pontual é uma forma normalmente ordenada no domínio regular existente. Não se afirma campo pontual limitado, operador criação pontual definido em todo Fock, nem produto bruto de distribuições.',
 'A contrapartida circular transporta os estados pelo unitário já construído; physicalField antigo não é modificado.',
 'RemainingModularCoreInput A continua exigido pelo consumidor calibrado como antes; o trabalho não habita esse input nem escolhe relógio físico.',
 'R8 integral e sua integração geométrica permanecem abertos; sem aceite, promoção ao kernel ou mudança de gate.'
 ],
 'historical_failed_source':pin(BASE/'RegularPointAnnihilationR1.lean'),
 'historical_failure_receipt':pin(OUT/'orbital_rotation/attempts/20261016T203613_985553Z/RECEIPT.json'),
 'historical_failure_axioms':pin(OUT/'orbital_rotation/attempts/20261016T203613_985553Z/AXIOMS.txt'),
 'repair_scope':'R2 conserva enunciados: ordem das duas somas, coerção definicional, simplificação em etapas antes de abrir regularExponential, rfl do kernel, igualdade funcional por funext/congrArg.',
 'next_exact_obligation':'Compilar RegularPointAnnihilationR2, LocalWickStressIdentificationR2 e PointAnnihilationSmearingR2; auditar a composição real sem hipótese da igualdade desejada. Se houver erro, corrigir em fonte nova mantendo enunciados, medida, sinais, fator e limites.',
 'limits':{'maxHeartbeats':400000,'synthInstance.maxHeartbeats':500000},
 'original_sources_modified':False,'author_builds':0,'provider_calls':0,'production_changes':False,
 'mission_mutations':False,'script':pin(Path(__file__))
}
dest=BASE/'LOCAL_WICK_IDENTIFICATION_CANDIDATES_R51_R2.json'
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
assert not dest.exists();tmp=dest.with_name(dest.name+'.tmp_r51')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,dest);assert dest.read_bytes()==data
print(json.dumps({**summary,'manifest':pin(dest),'revision':p['receipt']['revision']},ensure_ascii=False))
