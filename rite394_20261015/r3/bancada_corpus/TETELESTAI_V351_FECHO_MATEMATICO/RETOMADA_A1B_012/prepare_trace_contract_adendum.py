from pathlib import Path
import datetime,hashlib,json,os,subprocess
R=Path(__file__).resolve().parent;K=R/'k'
stamp=datetime.datetime.now().astimezone().isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists() and b
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
fields={
 'value':'scalarInverseLimitWeight', 'zero':'scalarInverseLimitWeight_zero',
 'additive':'scalarInverseLimitWeight_add','homogeneous':'scalarInverseLimitWeight_scale',
 'monotone':'scalarInverseLimitWeight_mono','faithful':'scalarInverseLimitWeight_faithful',
 'normal':'scalarInverseLimitWeight_normal','semifinite':'scalarInverseLimitWeight_finite_minorants',
 'tracial':'scalarInverseLimitWeight_tracial [OPEN — candidate34]',
 'dual_scaling':'scalarInverseLimitWeight_dual'}
files=['V351RegularCoreTraceContract','V351InverseLimitWeight','V351InverseLimitFaithful',
 'V351InverseLimitFiniteMinorants','V351InverseLimitScaling','V351InverseLimitTracialExtension']
sources=[pin(K/'TGLExt'/f'{s}.lean') for s in files]
result=subprocess.run(['rg','-n','def .*TraceData|def .*CoreTrace|RegularCoreTraceData',str(K/'TGLExt'),'-g','*.lean','-g','!Audit*.lean'],capture_output=True)
assert result.returncode in (0,1)
description='[OPEN] Prévio à embalagem final: se a tracialidade34 for efetivamente compilada e auditada, preencher RegularCoreTraceData no mesmo arquivo, sem novo campo e sem novo teorema para cada lei. Todos os campos exceto tracial reutilizam fontes anteriores. O fornecedor dos minorantes exige explicitamente tracialidade: fornecer a prova34, nunca uma premissa não paga. Valor é literalmente scalarInverseLimitWeight; a definição não altera esse peso, sua normalização, seu core ou seu gerador. Busca local relida: outros TraceData são homônimos em álgebras distintas; o contrato concreto contém somente estrutura e obstruções a fornecedores errados. Não promover esta ficha, sucesso DEV ou mera presença de uma definição a aceite independente. Sem nova hipótese, sem renomear scalarDualWeight como traço, sem alteração do gate ou monólito.'
d=dict(timestamp=stamp,status='OPEN__PRE_CONTRACT_ASSEMBLY',description=description,fields=fields,sources=sources,search=dict(returncode=result.returncode,stdout=result.stdout.decode('utf8'),stderr=result.stderr.decode('utf8')),full_trace_constructed=False,gate_changed=False)
put(R/'ADENDO_PRE_EMBALAGEM_CONTRATO_TRACO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
text=stamp+'\n\n'+description+'\n\n'+ '\n'.join(f'- `{k}` ← `{v}`' for k,v in fields.items())+'\n\nBusca limitada:\n```\n'+d['search']['stdout']+'\n```\n'
put(R/'ADENDO_PRE_EMBALAGEM_CONTRATO_TRACO.md',text.encode('utf8'))
print(text)
