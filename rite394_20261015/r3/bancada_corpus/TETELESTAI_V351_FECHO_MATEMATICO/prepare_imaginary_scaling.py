from pathlib import Path
import re,json,hashlib,datetime,subprocess,os
R=Path(__file__).absolute().parent; K=R/'kernel/TGLExt'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
 assert not p.exists(),p
 if isinstance(b,str):b=b.encode('utf8')
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b and b;os.replace(t,p)
providers=[]
for stem in ['V350PositiveRootIntertwining','V350ScaledPositiveResolvent','V350MatrixUnitResolventScaling','V350ScalarRegularRightPolar','V350ScalarGNSGeneratorTransport','V351ResolventPhaseFunctions','V351ResolventPhaseCalculus','V351ResolventImaginaryPowers','V351ScalarTomitaImaginaryPowers']:
 p=K/(stem+'.lean');s=p.read_text(encoding='utf8');decl=[]
 for m in re.finditer(r'^(?:def|lemma|theorem) (\w+)',s,re.M):
  rest=s[m.start():];end=rest.find(':=');assert end>=0
  decl.append(dict(name=m[1],line=s[:m.start()].count('\n')+1,statement=rest[:end].strip()))
 providers.append(dict(path=str(p),sha256=sha(p),section_variables=re.findall(r'^variable[^\n]*(?:\n  [^\n]*)*',s,re.M),declarations=decl,decision='REUSAR'))
searches=[]
for pattern in ['scaledPositiveResolvent.*cfc|cfc.*scaledPositiveResolvent|imaginaryPower.*scal|imaginary.*intertwin','^theorem.*cfc_intertwines|^theorem.*resolvent.*scaling|^theorem.*ImaginaryPower']:
 cmd=['rg','-n',pattern,str(K),'-g','*.lean'];q=subprocess.run(cmd,capture_output=True);assert q.returncode in [0,1]
 p=R/f'BUSCA_A1_ESCALA_IMAGINARIA_{len(searches)}.txt';new(p,q.stdout+b'\nEXIT '+str(q.returncode).encode())
 searches.append(dict(command=cmd,returncode=q.returncode,path=str(p),sha256=sha(p)))
prior=R/'MANIFESTO_A1_POTENCIAS_IMAGINARIAS.json';pd=json.loads(prior.read_bytes())
for f in pd['files']:assert sha(Path(f['path']))==f['sha256']
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO',previous_goal_turn='PROGRESS_39_DECLARATIONS_DELIVERED_REVALIDATED',
 consumer=dict(path=str(R/'LACUNAS_A1.md'),sha256=sha(R/'LACUNAS_A1.md'),name='regular_dual_weight_modular_implementation',line=25),
 exact_target='For positive injective contraction T with injective I-T, r>0, Q=T[rI+(1-r)T]^-1 and bounded R satisfying TR=RQ, prove U_t(T) R=exp(i t log r) R U_t(T). Specialize to scalarTomitaResolvent P and homogeneousRightGNS(matrixUnitRightData P N i j), r=localEigenvalue P N i j; also commute with the existing regular right group.',
 decision='ADAPTAR real_cfc_intertwines to complex continuous functions; REUSAR exact resolvent scaling and newly verified imaginary group; NOVO rational phase scaling on spectrum and dense cancellation. No new operator called modular by invariance alone.',
 providers=providers,searches=searches,prior_manifest=dict(path=str(prior),sha256=sha(prior),verified_files=len(pd['files'])),
 inherited_six_modalities={n:sha(R/n) for n in ['REAPROVEITAMENTO_A1.json','BUSCAS_A1.json','OUTRAS_BANCADAS_HASHES.json','ADENDO_REAPROVEITAMENTO_A1.json']},
 expected_open_after='Identification on all generators and whole algebra, positive h, inverse-generator trace. A1(b) remains open until actual contract inhabitant or typed impossibility.')
new(R/'REAPROVEITAMENTO_A1_ESCALA_IMAGINARIA.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
new(R/'REAPROVEITAMENTO_A1_ESCALA_IMAGINARIA.md','''[OPEN — ficha anterior ao código]

# A1 — transportar a escala existente às potências imaginárias

Consumidor: regular_dual_weight_modular_implementation, LACUNAS_A1.md, para identificar a ação de Δν^{it} sobre os geradores do MESMO core. O grupo do resolvente já foi construído e entregue; a igualdade TR=RQ_r já foi provada para a direita matricial.

Alvo: U_t R=exp(it log r) R U_t para Q_r=T[rI+(1−r)T]⁻¹, r>0, TR=RQ_r. Tipo genérico: T positivo contrativo, T e I−T injetivos, R limitado, sem supor R invertível. Especializar para todo SiteProfile P, N,i,j. Também transportar a comutação regular já existente.

Reusar o grupo, resolvente, denominador positivo, injetividades e CFC. Adaptar o entrelaçamento real existente ao CFC complexo. A ponte nova deve incluir o amortecimento: b(Q_r)=b(T)rD_r⁻²; não cancelar b(T) por uma inversa limitada. Fontes, enunciados completos, linhas, hashes, buscas e reconferência do marco anterior no JSON.

A prova da ação em toda a álgebra e a construção do traço ainda serão consumidores posteriores. Não tocar fontes entregues, monólito, gate ou resultados de natureza.
'''+data['timestamp']+'\n')
print(json.dumps(dict(status=data['status'],providers=len(providers),prior_files=len(pd['files']))))
