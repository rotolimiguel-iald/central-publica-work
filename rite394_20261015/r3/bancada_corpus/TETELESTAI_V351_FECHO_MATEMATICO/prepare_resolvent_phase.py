from pathlib import Path
import hashlib,json,datetime,subprocess,re,os
R=Path(__file__).absolute().parent
K=R/'kernel/TGLExt'
O=R.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
 assert not p.exists(),p
 q=p.with_name(p.name+'.tmp'); q.write_bytes(b)
 assert q.read_bytes()==b and len(b)>0
 os.replace(q,p)
providers=[]
for name in ['V350ScalarWeightTomitaIdentification','V350ScalarTomitaResolvent','V350ScalarTomitaPolarResolvent','V350BoundedInjectivePolar','V350DenseLinearPolarExtension','V350MatrixUnitResolventScaling','V350PositiveRootIntertwining','ModularFlowLevel']:
 p=K/(name+'.lean'); lines=p.read_text(encoding='utf8').splitlines()
 providers.append(dict(path=str(p),sha256=sha(p),declarations=[dict(line=i+1,text=l) for i,l in enumerate(lines) if re.match(r'^(def|theorem|lemma) ',l)],decision='REUSAR'))
pattern='imaginaryPower|imaginary_power|resolventPhase|regular_dual_weight_modular|phase.*resolvent|resolvent.*phase'
cmd=['rg','-n',pattern,str(K),'-g','*.lean']
s=subprocess.run(cmd,capture_output=True)
assert s.returncode in [0,1]
put(R/'BUSCA_A1_FASE_RESOLVENTE.txt',s.stdout+b'\nEXIT '+str(s.returncode).encode()+b'\n')
record=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO',
 consumer='ORDEM_011 A1(b): modular implementation of the SAME scalarDualWeight, needed for perturbation by h^-1 to the faithful normal semifinite scaled trace on regularCoreAlgebra P. This bridge is not itself a trace contract inhabitant.',
 exact_target='T=scalarTomitaResolvent P=(I+S* S)^-1; b(x)=x(1-x); g_t(x)=b(x) exp(i t log((1-x)/x)). Construct U_t on ScalarGNSHilbert P with U_t b(T)=g_t(T), unitary group and strong continuity, then transport existing resolvent scaling to identify the modular action. No bounded inverse or spectral gap assumed.',
 decision='ADAPTAR bounded CFC and dense polar extension; NOVO damped imaginary phase and cancellation on dense range. Existing regular left/right groups do not identify imaginary powers of actual S* S; invariance is not KMS.',
 scope='A1 only; no repeated root construction or full abstract predual; no canonical edits; no experimental gate.',providers=providers,
 search=dict(command=cmd,returncode=s.returncode,path=str(R/'BUSCA_A1_FASE_RESOLVENTE.txt'),sha256=sha(R/'BUSCA_A1_FASE_RESOLVENTE.txt')),
 inherited_six_modalities={n:sha(R/n) for n in ['REAPROVEITAMENTO_A1.json','BUSCAS_A1.json','OUTRAS_BANCADAS_HASHES.json','ADENDO_REAPROVEITAMENTO_A1.json']})
put(R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json',json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.md',('''# A1 — potências imaginárias pelo resolvente do mesmo S* S

[OPEN — ficha anterior ao código]

Consumidor: A1(b), identificação modular do peso dual escalar, etapa necessária para perturbá-lo pelo gerador e obter o traço escalado. Este módulo não habita sozinho o contrato do traço.

Reusar o S do peso completo, seu resolvente positivo injetivo T, o transporte por J, a extensão polar densa e a relação de escala matricial já provada. Introduzir somente a fase amortecida g_t(x)=x(1−x) exp(it log((1−x)/x)) e a extensão unitária que ela determina na imagem densa de T(1−T).

O grupo regular à esquerda/direita já existe. Sua invariância não identifica as potências de S* S. A construção pretendida parte do resolvente efetivo; não recebe outro operador modular por hipótese. Grupo, continuidade e identificação com a conjugação regular serão obrigações separadas até compilação efetiva.

Fornecedores, linhas, hashes lidos e busca estão no JSON. As seis modalidades da ficha A1 são herdadas, sem repetir o acervo. Nenhum novo predual abstrato é exigido aqui. Nenhum gate é alterado.
'''+record['timestamp']+'\n').encode('utf8'))
# Copy only already validated inherited object dependencies needed for these imports.
seen=set(); deps=[]
def visit(m):
 if not m.startswith(('TGL.','TGLExt.')) or m in seen:return
 seen.add(m); rel=Path(*m.split('.')); src=R/'kernel'/rel.with_suffix('.lean'); old=O/rel.with_suffix('.lean')
 assert src.read_bytes()==old.read_bytes(),src
 for dep in re.findall(r'^import\s+(\S+)',src.read_text(encoding='utf8'),re.M):visit(dep)
 obj=O/'.lake/build/lib/lean'/rel.with_suffix('.olean'); dst=R/'build'/rel.with_suffix('.olean')
 if dst.exists():assert dst.read_bytes()==obj.read_bytes()
 else:put(dst,obj.read_bytes())
 deps.append(dict(module=m,source=str(src),source_sha256=sha(src),object=str(dst),object_sha256=sha(dst),origin=str(obj)))
for m in ['TGLExt.V350ScalarTomitaPolarResolvent','TGLExt.V350BoundedInjectivePolar','TGLExt.ModularFlowLevel','TGLExt.V350MatrixUnitResolventScaling']:visit(m)
put(R/'DEPENDENCIAS_A1_FASE_RESOLVENTE.json',json.dumps(deps,indent=2).encode())
print(json.dumps(dict(ficha=str(R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json'),dependencies=len(deps))))
