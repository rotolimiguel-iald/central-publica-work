from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
O=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
T=O/'takesaki_fock'; A=O/'orbital_rotation/attempts'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'kind':'agent','id':'codex-r50-positive-cyclic-review'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
 p=Path(p);b=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def collect(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):yield x
  for v in x.values():yield from collect(v)
 elif isinstance(x,list):
  for v in x:yield from collect(v)
specs=[
 ('CanonicalFockActualInverseFinitenessR2.lean','20261016T201249_976567Z',4),
 ('CanonicalFockActualPositiveTracePackageR2.lean','20261016T201541_365276Z',6),
 ('CanonicalFockPositiveShiftTransportR2.lean','20261016T201551_615339Z',4)]
manifest_paths=[T/'CANONICAL_FOCK_ACTUAL_INVERSE_FINITENESS_CANDIDATE_R2.json',
 T/'CANONICAL_FOCK_ACTUAL_POSITIVE_TRACE_PACKAGE_CANDIDATE_R2.json',
 T/'CANONICAL_FOCK_POSITIVE_SHIFT_AND_CYCLIC_CANDIDATES_R2.json']
objects=[read(p) for p in manifest_paths]; builds=[]
for name,attempt,count in specs:
 source=T/name;d=A/attempt;r=read(d/'RECEIPT.json')
 objects.extend([r,read(d/'DEPENDENCY_CACHE.json')])
 assert r['exit_code']==0
 assert r['readonly_dependencies_unchanged'] and r['dependency_cache_unchanged']
 assert r['production_modified'] is False
 assert source.read_bytes()==(d/name).read_bytes()
 txt=source.read_text(encoding='utf-8')
 assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',txt,re.M)
 ax=(d/'AXIOMS.txt').read_text(encoding='utf-8')
 reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",ax)
 assert len(reports)==count and 'sorryAx' not in ax and 'error:' not in ax
 assert all(set(z.strip() for z in row.split(','))<={'propext','Classical.choice','Quot.sound'} for _,row in reports)
 op=next(x for x in r['artifacts'] if Path(x['path']).name==Path(name).with_suffix('.olean').name)
 assert pin(op['path'])==op
 builds.append({'source':pin(source),'receipt':pin(d/'RECEIPT.json'),
 'dependency_cache':pin(d/'DEPENDENCY_CACHE.json'),'olean':pin(op['path']),
 'axioms':pin(d/'AXIOMS.txt'),'exit_code':0,'seconds':r['seconds'],
 'declarations':[n for n,_ in reports],'only_standard_trio':True,
 'source_matches_attempt_bytes':True,'dependencies_and_cache_unchanged':True})
unique={}
for o in objects:
 for x in collect(o):unique[(str(Path(x['path']).resolve()).casefold(),x['sha256'].lower())]=x
nbytes=0;exts={}
for (_,sha),x in unique.items():
 a=pin(x['path']);assert a['sha256']==sha,a
 if 'bytes' in x:assert a['bytes']==x['bytes'],a
 nbytes+=a['bytes'];ext=Path(x['path']).suffix.lower();exts[ext]=exts.get(ext,0)+1
summary={'verdict':'PASS_COMPONENT_WITH_SCOPE','review_complete':True,'pins':len(unique),'bytes_hashed':nbytes,
 'pin_suffix_counts':exts,'builds':[{'name':Path(b['source']['path']).name,'attempt':Path(b['receipt']['path']).parent.name,
 'seconds':b['seconds'],'prints':len(b['declarations'])} for b in builds]}
if '--write' not in sys.argv:print(json.dumps(summary));raise SystemExit(0)
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
 input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
response=json.loads(run.stdout);assert response['ok'],response
p=response['result'];r7=next(x for x in p['projection']['active'] if x['id']=='R7')
assert r7['status']=='working'
supplier_paths=[
 T/'CanonicalFockRegularCoreR2.lean',T/'CanonicalFockDualWeightR3.lean',
 T/'CanonicalFockInverseSupremumR2.lean',T/'CanonicalFockInverseNormalR1.lean',
 T/'GeneralInverseOrderNormalR1.lean',T/'GeneralInverseFiniteApproximationR1.lean',
 T/'CanonicalFockGNSR5.lean',
 O/'gns_coefficient_tomita/CanonicalFockActualInverseAdditivityR2.lean',
 O/'gns_coefficient_tomita/CanonicalFockActualTracialExtensionR1.lean',
 K/'TGLExt/V354PolarIntertwining.lean',K/'TGLExt/V354TraceShiftEquivalence.lean',
 K/'TGLExt/V354CyclicTraceCompletion.lean',K/'TGLExt/V354TraceReaderWall.lean']
report={
 'schema':'iald-independent-review/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'PASS_COMPONENT_WITH_SCOPE','review_complete':True,'review_scope':'Somente as três peças com EXIT0 e 14 declarações; CyclicTraceCompletionR2 excluída.','requirement':'R7','requirement_satisfied':False,
 'reviewer':ACTOR,'handle':'r50-positive-cyclic-review',
 'independence':'O revisor não construiu as três fontes R50 objeto deste parecer. Autores dos manifestos: codex-fock-r6-review e codex-mission-memory-review. A revisão não cria uma identidade de aprovação fictícia.',
 'mission_reference':pin(REF),'mission_receipt':p['receipt'],'projection_sha256':p['projection_sha256'],
 'criterion':r7['criterion'],'lease_observed':r7['lease'],
 'handoff':pin(O/'mission_resume_20261016/LIVE_HANDOFF_R7_20261016T201834_424034Z_68cc0834_RECEIPT.json'),
 'builds':builds,'candidate_manifests':[pin(x) for x in manifest_paths],
 'integrity':{'unique_path_sha256_pairs':len(unique),'bytes_hashed':nbytes,'pin_suffix_counts':exts,
 'mismatches':0,'coverage':'Todos os pares path/sha256 nos três manifestos R2, nos três recibos EXIT0 e nos três DEPENDENCY_CACHE.json; o terceiro manifesto também pina a candidata CyclicTraceCompletionR2, cuja integridade não equivale a compilação concluída. Inclui fontes, cópias, oleans e os artefatos de saída. Não é recompilação.'},
 'source_review':[
 {'source':'CanonicalFockActualInverseFinitenessR2.lean','lines':[116,125,181,194],
  'result':'O corte pertence à álgebra direita do polar original. A cota vem da ordem dos produtos dos cortes e da monotonicidade do peso perturbado no mesmo GNS. No ramo de peso dual infinito, o fator d^-1 é estritamente positivo; o ramo finito recebe a prova concreta. A lei de minorantes consome essa cota e a tracialidade R49, sem hreg/hbound/tracialidade finais.'},
 {'source':'CanonicalFockActualPositiveTracePackageR2.lean','lines':[65,80,90,110,124,130,147],
  'result':'Os dez campos do pacote positivo são preenchidos sem premissas de entrada. value é definitionally o inverseSupremum preexistente em PositiveInput. Normalidade é preservação de IsLUB interno para família crescente dirigida não vazia; positividade do supremo é derivada. Semifinitude é supremacia de minorantes positivos com valor finito. A testemunha satisfaz 0<value Y<top; value(1)=top também impede vacuidade.'},
 {'source':'CanonicalFockPositiveShiftTransportR2.lean','lines':[31,76,93,105],
  'result':'O lema genérico de transporte declara hquadratic e suporte, mas o consumidor concreto descarrega hquadratic por R49. positiveShift_value_compatible exige somente a relação ShiftRelated; usa o polar limitado do mesmo operador no mesmo core para obter transporte e suporte, sem postular essa identificação.'},

 ],
 'same_object_checks':[
 'core é RegularCovariantCore.core fockFlow M em L2(R; Fock), com fockFlow=Gamma(B0(-2*pi*t)); nenhum SiteProfile é substituído.',
 'PositiveInput é o subtipo dos operadores positivos pertencentes ao core original; value é o inverseSupremum do vácuo regular original.',
 'O GNS e o polar usados na finitude são os fornecedores escalares originais. As abreviações de instâncias não criam outro produto interno ou domínio.',
 'O pacote positivo e a compatibilidade de ShiftRelated usam a mesma ação dual e a mesma normalização; não há nova escolha de peso.'
 ],
 'zero_extension_check':'As três peças revistas não introduzem uma extensão total por zero fora do cone positivo. A lei quadrática e a compatibilidade de ShiftRelated são demonstradas sobre value em PositiveInput. V354TraceReaderWall permanece respeitado.',
 'pending_live_build':{
  'source':pin(T/'CanonicalFockCyclicTraceCompletionR2.lean'),
  'attempt':'20261016T201910_284165Z',
  'attempt_source':pin(A/'20261016T201910_284165Z/CanonicalFockCyclicTraceCompletionR2.lean'),
  'session_id':4097,
  'status':'pending_live_build',
  'authority':'Mensagem do coordenador: processo Lean ativo; não repetir.',
  'review_status':'EXCLUDED_FROM_FINAL_VERDICT',
  'semantic_reading_status':'DECLARADO',
  'semantic_reading':'A leitura da candidata usa supremo ENNReal de positivos ShiftRelated, pretendendo ciclicidade e concordância positiva; não declara um traço complexo linear. Sem promover a leitura a compilação verificada. Um adendo próprio deverá conferir o recibo terminal e os oito relatórios esperados.'
 },
 'scope_limits':[
 'actualPositiveTrace é um peso tracial normal, semifinito e fiel no cone positivo no alcance literal de seus campos.',
 'A compatibilidade positiva de ShiftRelated está incluída. A completação cíclica em todo o core está excluída deste veredito, pois seu build está pendente. Não se certifica um traço complexo linear total.',
 'A existência da testemunha positiva finita não certifica PF, a equivalência Fock-torre, a implementação modular completa ou o critério integral R7.',
 'Não houve promoção ao kernel de produção, mudança de gate nem transição de aceite.'
 ],
 'findings':[],
 'nonblocking_residue':['Comentários e manifestos preservam o estatuto histórico de candidato; os três recibos posteriores EXIT0 são a evidência de compilação usada nesta revisão.'],
 'suppliers':[pin(x) for x in supplier_paths],
 'own_builds':0,'provider_calls':0,'mission_mutations':False,'production_writes':False,
 'audit_rounds':1,'review_script':pin(Path(__file__))
}
dest=O/'mission_review_20261016/R50_POSITIVE_TRACE_REVIEW_R1.json'
assert not dest.exists()
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=dest.with_name(dest.name+'.tmp_r50_positive')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,dest);assert dest.read_bytes()==data
print(json.dumps({**summary,'review':pin(dest),'revision':p['receipt']['revision']},ensure_ascii=False))

