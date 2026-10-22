from pathlib import Path
import datetime, hashlib, json, os, subprocess
R=Path(__file__).resolve().parent; K=R/'k'; CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True); t=p.with_name(p.name+'.tmp'); t.write_bytes(b); assert t.read_bytes()==b; os.replace(t,p)
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A=R/'search_double_cut_spectral'/stamp; A.mkdir(parents=True)
pattern='modular_phase_frequency_separation|phase_family_injective|gelfandTransform_isometry|doubleCut_balance'
queries=[('kernel',['rg','-n',pattern,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pattern,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pattern,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pattern,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pattern,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pattern,'--max','12','--ctx','100']),('others',['rg','-l',pattern,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/PhaseFrequencySeparation.lean',58,64),('TGLExt/V351ResolventPhaseFunctions.lean',14,18),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/GelfandDuality.lean',144,144),('.lake/packages/mathlib/Mathlib/Algebra/Star/Subalgebra.lean',588,590),('.lake/packages/mathlib/Mathlib/Topology/Algebra/StarSubalgebra.lean',137,141),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean',461,465),('TGLExt/V350ScalarRegularRightPolar.lean',14,17),('TGLExt/V350CorePolarInclusion.lean',52,56)]
providers=[]
for path,start,end in specs:
    p=K/path; ls=p.read_text(encoding='utf8').splitlines();providers.append(dict(source=pin(p),line=start,excerpt='\n'.join(ls[start-1:end]),decision='REUSAR'))
text='[OPEN — adendo anterior ao código do balanço espectral]\n\n'+datetime.datetime.now().astimezone().isoformat()+'\n\nDelta32 já aceito e entregue. O balanço limitado e Q permanecem abertos. Estratégia em exame: usar a álgebra comutativa fechada gerada pelos três resolventes originais, transportar as fases amortecidas por map_cfc e aplicar os caracteres. A separação das frequências JÁ ESTÁ em modular_phase_frequency_separation: não refazer sua derivada. A igualdade escalar deve valer após multiplicação pelos amortecimentos, cobrindo os extremos 0 e 1 sem cancelamento falso. Só depois se cancela o operador com imagem densa, quando esta estiver provada na representação original. A conversão para cortes gerais é racional; não se introduz h=Delta_nu nem se assume o balanço desejado. Fornecedores abaixo relidos integralmente ou no trecho do enunciado antes de editar Lean33. Ausência em buscas não é prova de ausência universal.\n\n'
for q in providers: text+=q['source']['path']+':'+str(q['line'])+'\n```lean\n'+q['excerpt']+'\n```\n\n'
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__BEFORE_CODE',providers=providers,searches=pin(A/'searches.json'),full_balance_proved=False)
put(R/'ADENDO_PRE_CODIGO_BALANCO_ESPECTRAL.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'));put(R/'ADENDO_PRE_CODIGO_BALANCO_ESPECTRAL.md',text.encode('utf8'))
print('DONE',A)
