from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
BASE=R.parent/'RETOMADA_A1B_012'
K=BASE/'k'
stamp=datetime.datetime.now().astimezone().isoformat()
suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put_new(p,b):
 assert p.is_relative_to(R) and not p.exists()
 q=p.with_name(p.name+'.tmp_'+suffix)
 with q.open('xb') as f:f.write(b)
 assert q.read_bytes()==b;os.replace(q,p)
review=BASE/'revisao_tracialidade_quadratica/REVIEW_A1_QUADRATIC_TRACE_FINAL.json'
rd=json.loads(review.read_text(encoding='utf8'))
assert rd['mathematical_review_passed'] and rd['full_trace_constructed']
assert not any(rd[k] for k in ('P0','P1','P2'))
suppliers=[
 ('Contrato habitado','TGLExt/V351RegularCoreTraceConstruction.lean','def scalarInverseLimitTraceData'),
 ('Tracialidade','TGLExt/V351QuadraticTrace.lean','theorem scalarInverseLimitWeight_tracial'),
 ('Implementação modular','TGLExt/V351ModularImplementation.lean','theorem scalarTomitaImaginaryPower_eq_regular_implementation'),
 ('Grafo espectral','TGLExt/V351RegularSpectralGraph.lean','theorem regularPositiveGenerator_graph_iff'),
 ('Afiliação do grafo','TGLExt/V351RegularGeneratorAffiliation.lean','theorem regularPositiveGenerator_commutant_graph'),
]
rows=[]
for role,file,needle in suppliers:
 p=K/file;lines=p.read_text(encoding='utf8').splitlines()
 line=next(i+1 for i,s in enumerate(lines) if needle in s)
 rows.append(dict(role=role,line=line,declaration=needle,**pin(p)))
text='\n\n## Errata ao lado — '+stamp+' — A1(b) concluído; quatro pontes e rota efetiva\n\n'
text+='[REAL — auditorias e fontes relidas] A frase inicial «Um termo desse contrato ainda não foi produzido» e o NÃO PAGO de A1(b) descrevem o estado histórico de 14/09. Estão superados: scalarInverseLimitTraceData P habita RegularCoreTraceData P para todo SiteProfile, com o MESMO scalarInverseLimitWeight. A revisão final A1_QUADRATIC_TRACE_REVIEW_ACCEPTED__REGULAR_TRACE_CONSTRUCTED está aceita, sem P0/P1/P2. Nenhum build foi repetido para esta correção documental.\n\n'
text+='1. A ponte geral regular_scalar_weight_is_dual_weight não foi provada pela rota final. A construção partiu de nu=scalarDualWeight e seus dados concretos de GNS/normalidade/fidelidade/semifinitude. A ponte geral ao cone estendido abstrato foi DISPENSADA pela rota, não declarada paga por nome.\n'
text+='2. A implementação modular foi paga por scalarTomitaImaginaryPower_eq_regular_implementation e seus fornecedores; não recebeu o nome proposto na lista inicial. Identificação de implementadores e ação no core são os resultados concretos, preservando seus espaços.\n'
text+='3. O gerador positivo, domínio/afiliação e potências imaginárias foram construídos por transporte direto do grafo espectral, com regularPositiveGenerator_graph_iff. Não foi a rota genérica por unicidade do gerador e Weyl anunciada inicialmente. h não foi identificado com Delta_nu.\n'
text+='4. O conteúdo necessário à perturbação pelo inverso foi pago por cortes do mesmo h, seus limites positivos e scalarInverseLimitWeight_tracial. O contrato reúne zero, aditividade, homogeneidade, ordem, fidelidade, normalidade, semifinitude, tracialidade e escala dual. Não se afirma um teorema geral abstrato de Pedersen–Takesaki além desta realização.\n\n'
text+='[ESTADO] A1(a),(b),(c) concluídos no alcance das entregas aceitas. A2 é distinto: suporte finito, divisão em faces, identificação espectral/domínios/gap no mesmo core e compatibilidade do contrato legado. A existência do traço não quita essas entradas por si.\n\n'
text+='[NAMESPACE — resposta §5.4a] Os módulos V351 continuam em TGLV350.Regular porque estendem os mesmos objetos regularCoreAlgebra, regularDualAction, scalarDualWeight e o GNS construídos naquela namespace. V351 no nome do arquivo identifica a etapa de construção, não uma segunda álgebra. Mudar namespace não cria uma realização nova; duplicar os objetos seria contraproducente. O contrato RegularCoreTraceData nasceu em TGLV351 e é consumido explicitamente pelo construtor em TGLV350.Regular. Essa diferença é tipada por import/open e tipo de retorno, nunca por equivalência presumida de nomes.\n\n'
for row in rows:
 text+=f"- {row['role']}: `{row['path']}:{row['line']}`, SHA256 `{row['sha256']}`.\n"
text+='\nParecer: '+str(review)+'.\n'
target=R.parent/'LACUNAS_A1.md'
old=target.read_bytes()
assert b'Errata ao lado' not in old, 'Errata já existe; não repetir escritor'
backup=target.with_name(target.name+'.bak_'+suffix)
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old
new=old+text.encode('utf8')
temp=target.with_name(target.name+'.tmp_'+suffix)
with temp.open('xb') as f:f.write(new)
assert temp.read_bytes()==new and len(new)>len(old)
os.replace(temp,target)
assert target.read_bytes().startswith(old) and target.read_bytes()==new
record=dict(timestamp=stamp,before=pin(backup),after=pin(target),review=pin(review),sources=rows,
 backup_is_exact_bytes=True,append_only=True,requirements_paid=['5.4a','5.4e'],gate_changed=False)
put_new(R/'ERRATA_LACUNAS_A1_REGISTRO.json',json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(record,ensure_ascii=False))
