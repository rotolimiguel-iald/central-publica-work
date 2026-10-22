from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b and b;os.replace(t,p)
specs=[('TGLExt/V350RegularTowerRepresentation.lean','regularUnitary'),('TGLExt/V350L2Translation.lean','shift_ae'),('TGLExt/V350StrongOperatorField.lean','operatorFieldLift'),('TGLExt/V350StrongOperatorField.lean','operatorFieldLift_ae'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_star'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_mul'),('.lake/packages/mathlib/Mathlib/Analysis/Fourier/LpSpace.lean','fourierTransformₗᵢ'),('TGLExt/V350FourierL1L2.lean','fourier_integral_ae_eq_L2'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_injective'),('TGLExt/V350CharacterLocality.lean','character_commutation_local_pairing'),('TGLExt/V350FixedCoreLocality.lean','character_commutation_measurableCut'),('TGLExt/V350ResolventGraph.lean','resolventGraphOperator')]
rows=[]
for rel,name in specs:
 p=K/rel;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|def) '+re.escape(name)+r'\b[\s\S]*?(?= :=| where)',s,re.M);assert m,name
 rows.append(dict(name=name,file=pin(p),line=s[:m.start()].count('\n')+1,statement=m[0]))
stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__NEXT_SUPPLIER_ROUTE_ONLY__NOT_A_COMPILED_THEOREM',consumer='regular_unitary_positive_generator, LACUNAS_A1.md:31',providers=rows,search_scope='Targeted local source/type inspection only; the six-mode formal reuse fiche is still required before a new Lean construction.',not_new_proof=True,full_trace_open=True)
put(R/'ROTA_GERADOR_REGULAR_A1B.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='''[OPEN — roteiro do próximo fornecedor; as identidades abaixo ainda não são um novo teorema Lean]

# A1(b): gerador positivo regular, sem reconstruir Fourier ou L²

'''+stamp+'''

O alvo restante é `regular_unitary_positive_generator` de LACUNAS_A1.md:31. O consumidor final é a perturbação de `scalarDualWeight` que deve habitar `TGLV351.RegularCoreTraceData`; o objeto vive no Hilbert REGULAR, não apenas na torre e não apenas no GNS do peso. Esta nota registra fornecedores localizados. Não autoriza saltar a ficha de seis modalidades antes do próximo delta Lean.

## Convenções e candidato a testar

No código existente, `(S_t f)(x)=f(x-t)`, `Λ_t=fibre(Δ_base^{it}) S_t`, e a Fourier usa `exp(-2π i x ξ)`. Ponha formalmente `(Wf)(x)=Δ_base^{ix}f(x)`. O cálculo pontual dá

```
W S_t W* f(x) = Δ_base^{ix} Δ_base^{-i(x-t)} f(x-t)
              = Δ_base^{it} f(x-t) = Λ_t f(x).
F S_t F* = multiplicação por exp(-2π i t ξ).
h = W F* M[exp(-2π ξ)] F W*.
```

Essas são identidades de planejamento a transportar para classes L², domínios e operadores da casa. A primeira demanda construir o campo unitário usando `operatorFieldLift`; a segunda demanda aplicar a identidade de translação Fourier na classe L², com extensão densa, reaproveitando `fourier_integral_ae_eq_L2` ou o fornecedor Schwartz. A Fourier isométrica em L² já está definida na mathlib; não se deve reconstruí-la.

Para reutilizar a maquinaria limitada de resolventes, o candidato é

```
g(ξ)=1/(1+exp(-2πξ)),   0<g(ξ)<1,
R = W F* M[g] F W*,
h = (1-R)/R, no domínio Ran(R).
```

`resolventGraphOperator` e o cálculo funcional das potências imaginárias já existem. A expressão quociente acima NÃO significa inversa limitada: R e 1-R podem ser injetivos sem gap. Precisam ser demonstradas a igualdade das potências com Λ_t, a afiliação ao MESMO N e a não singularidade. A afiliação pode ser abordada pela comutação com N′, usando os fornecedores de localidade dos caracteres; esta nota não afirma que essa passagem já foi paga.

## Sinal da ação dual

Com `C_s f(x)=exp(-isx)f(x)`, o campo W comuta pontualmente com C_s. Na Fourier, C_s desloca a função para `ξ+s/(2π)`. Logo o candidato a h transforma por `exp(-2π(ξ+s/(2π)))=exp(-s)exp(-2πξ)`. Essa conta confere o sinal exigido de θ_s(h). O domínio transformado e a igualdade de operadores não limitados ainda precisam de prova. Se L=log h, o deslocamento esperado é L−s; para K=−log h, K+s.

## O que isso não fecha

O traço continua sem habitante: falta construir a perturbação pelo inverso do gerador e provar fidelidade, normalidade, semifinitude por minorantes, aditividade, homogeneidade, tracialidade e escala. O peso dual existente é invariante pela ação dual; não pode ser renomeado como traço de peso −1. O novo teorema de ação no GNS (ainda em aceitação isolada) fornece uma ligação real, sem suprir esses campos por comentário.

## Fornecedores localizados, em bytes e tipos

'''
for q in rows:s+=f"`{q['file']['path']}:{q['line']}` — `{q['file']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
put(R/'ROTA_GERADOR_REGULAR_A1B.md',s.encode('utf8'));print(json.dumps(dict(providers=len(rows),new_theorems=0,status=d['status'])))
