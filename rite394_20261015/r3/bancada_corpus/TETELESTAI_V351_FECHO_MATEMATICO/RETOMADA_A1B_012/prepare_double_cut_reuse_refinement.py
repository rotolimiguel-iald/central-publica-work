from pathlib import Path
import datetime, hashlib, json, os
R=Path(__file__).resolve().parent; K=R/'k'
def pin(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists()
    q=p.with_name(p.name+'.tmp'); q.write_bytes(b); assert q.read_bytes()==b; os.replace(q,p)
specs=[
 ('V350AntiunitaryPositiveConjugation.lean','theorem antiunitaryConjugate_nonneg'),
 ('V350ScalarRegularPolarCommutation.lean','theorem scalarTomitaPolar_regular_generator'),
 ('V351RegularImaginaryPowers.lean','theorem regularPositiveGenerator_imaginaryPower'),
 ('V351ResolventImaginaryPowers.lean','theorem resolventImaginaryPower_damping'),
 ('V351InverseGeneratorCutoff.lean','theorem regularInverseGeneratorCutoff_one'),
 ('V351RegularDomainCut.lean','theorem regularDomainCut_inverse_product'),
 ('V351RegularDomainCut.lean','theorem regularDomainCut_commutes')]
rows=[]
for name,needle in specs:
    p=K/'TGLExt'/name; lines=p.read_text(encoding='utf8').splitlines()
    indexes=[i for i,s in enumerate(lines) if s.startswith(needle+' ') or s.startswith(needle+' (')]
    assert len(indexes)==1,(name,needle,indexes)
    i=indexes[0]; rows.append(dict(source=pin(p),line=i+1,declaration=needle,excerpt='\n'.join(lines[i:i+8])))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__REUSE_REFINEMENT_BEFORE_NEXT_CONSUMERS',prior_search_fiche=pin(R/'REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES.json'),providers=rows)
body='''[OPEN] Refinamento de aproveitamento — fases concretas e cortes

Sem mudança de escopo nem novo modelo. Complementa a ficha de sete canais já registrada.

A conjugação antiunitária preserva positividade por lema anterior. A identidade J pi(lambda_t) J^-1 = R_-t já existe; não deve ser reprovada. Transportar somente a identidade amortecida das potências imaginárias regulares pela pi existente e conjugar com o J existente.

[DERIVED — plano algébrico, ainda não compilado] Para o balanço de cortes, aproveitar B_1=R e a identidade de resolventes. Ela dá A p_e=(1-A) C_e e B q_h=(1-B) D_h. Com as comutações correspondentes, multiplicar a diferença desejada por A B reduz ao balanço básico (1-T) A (1-B)=T (1-A) B. Cancelar A B por injetividade vetorial, nunca por inversa limitada ou separação espectral uniforme. Isso dispensa construir um novo cálculo espectral para cada regulador. As hipóteses de comutação têm de ser descarregadas nos objetos originais.

[OPEN] Cinco auxiliares privados passaram apenas DEV. A sexta aplicação concreta ainda está sob correção de elaboração; não há entrega33, compilação independente33 ou tracialidade. Nenhum gate alterado.
'''
body+='\n'+d['timestamp']+'\n'
for row in rows: body+='\n'+row['source']['path']+':'+str(row['line'])+'\n```lean\n'+row['excerpt']+'\n```\n'
put(R/'ADENDO_APROVEITAMENTO_FASES_E_CORTES.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'ADENDO_APROVEITAMENTO_FASES_E_CORTES.md',body.encode('utf8'))
print(json.dumps(d,ensure_ascii=False))
