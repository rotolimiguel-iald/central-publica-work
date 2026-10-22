from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
OUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
GNS = OUT/'gns_coefficient_tomita'
REF = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR = {'kind':'agent','id':'codex-r49-tracial-independent-review'}
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def jread(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str): yield o
        for v in o.values(): yield from collect(v)
    elif isinstance(o,list):
        for v in o: yield from collect(v)
parts = [
    ('CanonicalFockActualStarCoreTracialR1.lean','CANONICAL_FOCK_ACTUAL_STAR_CORE_TRACIAL_CANDIDATE_R1.json','20261016T194440_801316Z',4),
    ('CanonicalFockActualTracialExtensionR1.lean','CANONICAL_FOCK_ACTUAL_TRACIAL_EXTENSION_CANDIDATE_R1.json','20261016T194835_820345Z',2)]
unique={}; builds=[]; inputs=[]
for src,man,at,count in parts:
    attempt=OUT/'orbital_rotation/attempts'/at
    paths=[GNS/man,attempt/'RECEIPT.json',attempt/'DEPENDENCY_CACHE.json']
    inputs += paths
    objs=[jread(p) for p in paths]
    for o in objs:
        for x in collect(o):
            unique[(str(Path(x['path']).resolve()).casefold(),x['sha256'].lower())]=x
    manifest,receipt,cache=objs
    assert receipt['exit_code']==0
    assert receipt['readonly_dependencies_unchanged'] and receipt['dependency_cache_unchanged']
    assert receipt['production_modified'] is False
    assert (GNS/src).read_bytes()==(attempt/src).read_bytes()
    source=(GNS/src).read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',source,re.M)
    ax=(attempt/'AXIOMS.txt').read_text(encoding='utf-8')
    lists=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",ax)
    assert len(lists)==count and 'sorryAx' not in ax
    assert all(set(v.strip() for v in row.split(',')) <= {'propext','Classical.choice','Quot.sound'} for _,row in lists)
    builds.append({'source':pin(GNS/src),'manifest':pin(GNS/man),
      'source_author':manifest.get('actor',manifest.get('author')),
      'receipt':pin(attempt/'RECEIPT.json'),'dependency_cache':pin(attempt/'DEPENDENCY_CACHE.json'),
      'axioms_log':pin(attempt/'AXIOMS.txt'),'exit_code':0,'seconds':receipt['seconds'],
      'axiom_declarations':[n for n,_ in lists],'only_standard_trio':True,
      'source_matches_attempt_bytes':True,'dependencies_and_cache_unchanged_per_receipt':True})
fail=[]; checked_bytes=0
for x in unique.values():
    try:
        a=pin(x['path']); checked_bytes+=a['bytes']
        if a['sha256']!=x['sha256'].lower() or ('bytes' in x and a['bytes']!=x['bytes']):
            fail.append({'expected':x,'actual':a})
    except Exception as e: fail.append({'path':x['path'],'error':str(e)})
assert not fail,fail
selected=[]
names=['CanonicalFockGNSR5.lean','CanonicalFockRegularR2.lean','CanonicalFockActualRootCutFormsR2.lean',
       'CanonicalFockWeightPolarR5.lean','GeneralInverseFiniteApproximationR1.lean',
       'GeneralInverseStrongFatouR1.lean','CanonicalFockWeightInvarianceR4.lean',
       'GeneralInverseSupremumR3.lean','GeneralInverseCutoffWeightR3.lean','RegularFiniteStarCoreR2.lean']
seen=set()
for item in unique.values():
    p=Path(item['path'])
    if p.name in names and 'attempts' not in p.parts and 'dependency_cache' not in p.parts and str(p) not in seen:
        selected.append(pin(p));seen.add(str(p))
if '--write' not in __import__('sys').argv:
    print(json.dumps({'verification':'PASS','pins':len(unique),'bytes_hashed':checked_bytes,
     'builds':builds,'selected_dependency_sources':selected},ensure_ascii=False))
    raise SystemExit(0)
for filename in ['GeneralInverseStrongFatouR1.lean','GeneralInverseSupremumR3.lean',
                 'GeneralInverseCutoffWeightR3.lean','RegularFiniteStarCoreR2.lean']:
    selected.append(pin(OUT/'takesaki_fock'/filename))
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
    input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
response=json.loads(run.stdout); assert response['ok'],response
p=response['result']
r7=next(r for r in p['projection']['active'] if r['id']=='R7')
assert r7['status']=='working'
report={
 'schema':'iald-independent-review/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'PASS_COMPONENT_WITH_SCOPE','requirement':'R7','requirement_satisfied':False,
 'reviewer':ACTOR,'handle':'r49-tracial-independent-review',
 'independence':'Revisor não construiu nenhuma das duas fontes tracionais. A autoria das fontes consta dos manifestos pinados; esta revisão é independente e limitada aos dois componentes.',
 'mission_reference':pin(REF),'mission_receipt':p['receipt'],'projection_sha256':p['projection_sha256'],
 'criterion':r7['criterion'],'lease_observed':r7['lease'],
 'handoff':pin(OUT/'mission_resume_20261016/LIVE_HANDOFF_R7_20261016T194932_861133Z_94e7fe00_RECEIPT.json'),
 'builds':builds,
 'pin_verification':{'unique_path_sha256_pairs':len(unique),'bytes_hashed':checked_bytes,'mismatches':0,
   'coverage':'Todos os pares path+sha256 recursivamente presentes nos dois manifestos candidatos, nos dois recibos de build e nos dois DEPENDENCY_CACHE.json; bytes e tamanhos conferidos. Não é recompilação.'},
 'semantic_checks':[
   {'location':'CanonicalFockActualStarCoreTracialR1.lean:24','check':'O core, fockFlow, M, vácuo, GNSHilbert e weightContext são os fornecedores existentes. Dicionários nativos são abreviados; não se introduz outro GNS nem representação.'},
   {'location':'CanonicalFockActualStarCoreTracialR1.lean:59','check':'O núcleo finito uniforme entra no ideal escalar pela inclusão já provada; uniform_embedding identifica o mesmo vetor GNS.'},
   {'location':'CanonicalFockActualStarCoreTracialR1.lean:69','check':'A entrada da raiz provém do domínio fechado do Tomita original. A equação J.symm(GNS(a*))=root(GNS(a)) é deduzida de extends_star e da fatoração polar original.'},
   {'location':'CanonicalFockActualStarCoreTracialR1.lean:114','check':'A igualdade no núcleo finito usa o mesmo inverseSupremum de todos os reguladores positivos, sua forma quadrática e actual_root_cut_supremum. A conjugação antiunitária é explicitamente convertida na parte real. Só exige pertinência ao finiteDualStarCore.'},
   {'location':'RegularFiniteStarCoreR2.lean:25','check':'finiteDualStarCore é a interseção do ideal de quadrado dual finito com seu adjunto. A unidade não é declarada finita. Os regularSandwich existentes aproximam todos os elementos do core.'},
   {'location':'GeneralInverseFiniteApproximationR1.lean:126','check':'A redução usa regularSandwich, limites fortes, Fatou e a cota de contração. A única premissa sobre o vetor é a invariância de vácuo, fornecida concretamente por fibre_boost_fixes_regularVacuum; a extensão não assume a identidade final.'},
   {'location':'CanonicalFockActualTracialExtensionR1.lean:56','check':'A lei final quantifica a:core.toStarSubalgebra e consome a lei no núcleo finito. Não recebe hipóteses tracial, polar, balance, regularidade, finitude, hbound nem qualquer igualdade a provar.'}
 ],
 'final_signature':"theorem F1Fecho.CanonicalFockActualTracialExtensionR1.inverseSupremum_tracial (a : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) : inverseSupremum fockFlow regularFockVacuum (star a.val * a.val) = inverseSupremum fockFlow regularFockVacuum (a.val * star a.val)",
 'zero_extension_wall':{
   'source':pin(KERNEL/'TGLExt/V354TraceReaderWall.lean'),
   'check':'A parede refuta a ciclicidade irrestrita do positiveTraceReader zero-estendido em produtos arbitrários. As duas fontes não invocam esse leitor nem declaram ciclicidade xy/yx; comparam os quadrados positivos a*a e aa* no mesmo inverseSupremum. Não ocorre o atalho vedado.'},
 'direct_suppliers':selected,
 'scope_limits':[
   'Prova da lei tracial de quadrados no core limitado representado, com valores ENNReal possivelmente infinitos. Não afirma que todos os valores, a unidade ou um dado elemento são finitos.',
   'Não constrói aqui o traço total, seminfinitude/PF, sua normalização ou o entrelaçamento Takesaki completo. Esses componentes continuam exigindo seus próprios termos e evidências.',
   'Não transfere esta lei para representações, pesos ou ações homônimas. R7 integral permanece aberto; nenhum aceite operacional ou gate é alterado.'
 ],
 'findings':[],
 'nonblocking_residue':['Cabeçalhos e manifestos preservam o estatuto histórico de candidato não compilado; os recibos EXIT0 pinados são a evidência posterior usada nesta revisão. Nenhuma alteração documental foi feita.'],
 'audit_rounds':1,'own_builds':0,'provider_calls':0,'production_writes':False,
 'mission_mutations':False,'review_script':pin(Path(__file__))
}
dest=OUT/'mission_review_20261016/R49_TRACIAL_INDEPENDENT_REVIEW_R1.json'
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=dest.with_suffix('.json.tmp_review_r49_tracial')
assert not dest.exists()
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data
os.rename(tmp,dest)
assert dest.read_bytes()==data
print(json.dumps({'review':pin(dest),'verdict':report['verdict'],'pins':len(unique),
 'revision':p['receipt']['revision'],'requirement_satisfied':False},ensure_ascii=False))

