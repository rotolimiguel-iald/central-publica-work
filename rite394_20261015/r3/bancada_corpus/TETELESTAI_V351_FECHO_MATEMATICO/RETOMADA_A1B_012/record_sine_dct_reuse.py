from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists()
 q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
ps=[K/'TGLExt/V350ScalarWeightCompletion.lean',K/'TGLExt/V350FourierL1L2.lean',K/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',R/'revisao_consulta_acao_direita/CONSULTA_DCT_MULTIPLICADORES_L2.md',R/'revisao_consulta_acao_direita/CONSULTA_DCT_MULTIPLICADORES_L2.json']
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),decision='REUSAR_DCT_ADAPTAR_MULTIPLIER_L2',sources=[pin(p) for p in ps],consumer='regularSineResolvent strong-star convergence to the SAME regularSpectralResolvent',target='For a sequence of continuous g_n,g: R->R in [0,1] with pointwise g_n->g, realScalarMultiplier(g_n)u tends in the original vector L2 to realScalarMultiplier(g)u, for every u. Apply existing scalar dominated convergence to (g_n-g)^2 ||u||^2; dominant ||u||^2 is integrable by Lp.memLp. Use existing L2_integral_norm_sq then sqrt. This is a sequential adapter, not arbitrary-net DCT.')
put(R/'ADENDO_FICHA_SENO_DCT.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'ADENDO_FICHA_SENO_DCT.md',('[OPEN — adendo de aproveitamento anterior ao adaptador DCT]\n\n'+d['timestamp']+'\n\n'+d['target']+'\n\nFornecedores lidos, com pins no JSON: '+', '.join(str(p) for p in ps)+'\n').encode('utf8'))
d2=dict(title='Álgebra direita validada pelo autor; aproximantes explícitos em DEV',text='A auditoria autoral AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B passou, 10 teoremas e 2 definições; sonda de ordem b*c/c*b recusada por tipo. Revisão independente em andamento. DEV final da álgebra: dev_right_action_algebra/20260914_210039_263478 rc0; a tentativa 205915 rc1 foi corrigida por NNReal.coe_one. Há 12 entregas aceitas neste instante. A ficha dos aproximantes por seno foi escrita após sete buscas completas, com acervo de saída volumosa preservado; V351SineResolventApprox em primeiro DEV. Foi lida consulta DCT e registrado adendo antes de implementar o adaptador. A1(b)/traço continuam abertos, gate inalterado.',artifacts=['AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B.json','REAPROVEITAMENTO_A1B_APROXIMANTES_SENO.json','ADENDO_FICHA_SENO_DCT.json','dev_right_action_algebra/20260914_210039_263478/run.json'])
put(R/'status_sine_first_dev.json',json.dumps(d2,ensure_ascii=False,indent=2).encode('utf8'))

