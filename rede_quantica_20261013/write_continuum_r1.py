"""Write the explicit continuum construction beside the immutable R2 contract."""
from pathlib import Path
import datetime as dt
import hashlib,json,os
ROOT=Path(r'C:\IALD\Central de Patentes')
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
def pin(p):
    b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(name,value):
    p=OUT/name;t=p.with_name(p.name+'.tmp')
    if p.exists():raise FileExistsError(p)
    b=(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;os.rename(t,p)
    return pin(p)
review=OUT/'review_continuum/REVIEW_R1.json'
assert review.exists()
checks=json.loads((OUT/'continuum/RESULTADO_WIGNER_R1.json').read_text(encoding='utf-8'))
assert checks['verdict']=='PASS'
text=r'''# F1.REDE — construção explícita da rede contínua de helicidades ±1

Autor: codex-gerente-tgl. Camada nova ao CONTRATO_REDE_R2.
**[DERIVED sobre KNOWN]** Construção analítica no espaço de uma partícula da casa.
A identificação física com o refinamento do MQC/Supercondutor continua [OPEN].
As peças Lean e os testes numéricos têm o alcance discriminado abaixo.

## 1. A órbita e sua medida

Use assinatura (+---), c=ℏ=1 e uma unidade de momento de referência p*=1.
Esta escolha de unidade não é um ajuste físico. No cone futuro sem massa:

    p(q,r) = (ρ cosh r, ρ sinh r, q₂, q₃), ρ=|q|>0.
    dμ(p) = d³p/p⁰ = d²q dr.
    H1 = L²(C⁺, dμ; C²).

A igualdade de medidas segue de ∂p¹/∂r=ρ cosh r=p⁰. É precisamente a
normalização orbital da casa; trocar por d³p/(2p⁰) exigiria a isometria constante
correspondente, não uma troca silenciosa. O conjunto q=0 é nulo. A carta orbital,
o peso e sua ponte com rapidez já existem no O16.

## 2. Seção explícita e helicidade

Seja k*=(1,0,0,1). Defina Rₓ(q) como a rotação no plano yz que leva e_z a q/ρ:
seu bloco yz é [[q₃/ρ,q₂/ρ],[-q₂/ρ,q₃/ρ]]. Então

    s(p) = Bₓ(r) Rₓ(q) B_z(log ρ),       s(p) k* = p.

O bloco acima corresponde a cosφ=q₃/ρ, sinφ=−q₂/ρ. Ele é contínuo fora do eixo;
não depende da escolha de um argumento angular. Complete a seção de modo Borel
no eixo: para p=(E,±E,0,0), use R_y(±π/2) B_z(log E). Esse complemento permite
escrever o cociclo globalmente; as identidades na carta usadas como operadores
L² continuam sendo identidades quase em toda parte.

Para Λ própria ortócrona, ponha

    c(Λ,p) = s(p)⁻¹ Λ s(Λ⁻¹p).
    D(c) = diag(ζ(c), conjugado(ζ(c))).

O elemento c fixa k*. ζ é a projeção homomorfa do pequeno grupo ISO(2) ao
caractere de SO(2); a parte de translações nulas age trivialmente. Em coordenadas
do referencial k*, ζ=c₁₁+i c₂₁. As duas componentes são as helicidades +1 e −1;
essa orientação dos rótulos é uma convenção explícita.

## 3. A representação completa

Para uma translação a e Λ própria ortócrona, defina

    [U(a,Λ)f](p) = exp(i a·p) D(c(Λ,p)) f(Λ⁻¹p).

Não há fator 2π nessa fase: ela coincide com phase/orbitPairing da fonte Lean.
Cancelando as seções intermediárias obtém-se

    c(Λ₁Λ₂,p) = c(Λ₁,p)c(Λ₂,Λ₁⁻¹p).

Como a medida é Lorentz-invariante e D é unitário, U preserva a norma. A relação
a·p+b·Λ₁⁻¹p=(a+Λ₁b)·p prova a lei de grupo semidireto. U(0,I)=I e a inversa
vem da própria lei de grupo, portanto a isometria é sobrejetiva. O espectro
conjunto das translações está no cone futuro: seus geradores são multiplicação
pelas coordenadas p, no domínio maximal correspondente.

A continuidade forte pode ser verificada primeiro para funções contínuas de
suporte compacto na órbita, afastado da origem. Fora dos eixos nulos, as seções
são contínuas, logo o integrando converge pontualmente quando (a,Λ)→(0,I).
Os suportes transformados ficam num compacto comum de medida finita, D tem
norma 1 e a fase tem módulo 1: convergência dominada dá a convergência L².
A densidade dessa classe e a unitariedade estendem o resultado a H1. A seção
global Borel fornece o operador nos conjuntos excepcionais sem mudar sua classe.
Esta é uma prova analítica; a formalização Lean do grupo inteiro permanece aberta.

## 4. Boost, reflexão e a conjugação correta

A seção satisfaz s(Bₓ(t)p)=Bₓ(t)s(p) fora do eixo. Logo c(Bₓ(t),p)=I e

    [U(0,Bₓ(t))f](q,r) = f(q,r−t) = [B0(t)f](q,r).

Se R=Rₓ(π)=diag(1,1,−1,−1), também s(Rp)=R s(p) e c(R,p)=I.
Defina Θ f(p)=swap(conjugado(f(p))), onde swap troca as duas helicidades.
Como swap·conjugado(D)·swap=D, Θ comuta com a ação de Lorentz e inverte as
translações. Assim

    J_W = U(0,R) Θ,
    [J_W f](q,r) = swap(conjugado(f(−q,r))),
    J_W²=I,
    J_W U(a,Λ) J_W = U(j_W a, j_W Λ j_W),
    j_W=−R=diag(−1,−1,+1,+1).

A fase global da extensão antiunitária foi fixada como +1. Outra fase mudaria a
fase do subespaço real correspondente; ela não pode ser deixada implícita ao
comparar com uma realização física. Aqui a convenção é a mesma da candidata
geométrica construída, e não um parâmetro ajustado a dados.

Conjugar as coordenadas mantendo q fixo daria inversão total das translações;
isso não implementa j_W. O controle negativo abaixo detecta exatamente esse erro.

## 5. Tomita e o primeiro subespaço padrão

Use o Fourier parcial da casa, com núcleo exp(−2πi rξ), e denote-o por Φ.
Então ΦB0(t)Φ⁻¹ multiplica por exp(−2πitξ). Para a cunha direita:

    σ(ξ)=4π²ξ,
    Δ_W = Φ⁻¹ M_exp(σ) Φ,
    T_W = Φ⁻¹ M_exp(σ/2) Φ ≥ 0,
    Δ_W^(it)=B0(−2πt),
    S_W = J_W T_W,
    K(W_R) = { f∈Dom(T_W) : S_W f=f }.

Os domínios são maximais: f pertence a Dom(T_W) sse exp(σ/2)Φf pertence a L²;
para Δ_W, substitua por exp(σ). O Fourier da conjugação introduz ξ→−ξ,
enquanto a parte transversal introduz q→−q e swap. Daí J_W Δ_W J_W=Δ_W⁻¹.
T_W é positivo e auto-adjunto, S_W é fechado, densamente definido e involutivo
no seu domínio. A decomposição real f=(f+S_Wf)/2+i(f−S_Wf)/(2i) no domínio
explica densidade e separação do subespaço padrão. Seu Tomita é S_W e
S_W†S_W=Δ_W, com igualdade de grafos e domínios, não apenas uma igualdade formal.

Fubini, Fourier, o candidato geométrico J, T positivo, os grafos e o habitante
`F1Rede.CanonicalWedge.spectralOutput` foram construídos no sandbox Lean desta unidade.
A recompilação independente e o inventário final estão no relatório de entrega.
A prova Lean ainda não identifica o J espectral com a fórmula geométrica em
rapidez por um teorema de Fourier da conjugação; a correspondência acima é
analítica. Tampouco a prova Lean implementa todas as outras cunhas de Poincaré.

## 6. As outras cunhas e as álgebras

Defina K(gW_R)=U(g)K(W_R). A construção de localização modular BGL torna essa
definição independente da escolha de g e fornece isotonia, covariância e dualidade
sob as hipóteses verificadas da representação positiva antiunitária. Para um
duplo cone O, tome K(O)=∩_{W⊇O}K(W); regiões gerais usam extensão local por
fecho do span real das regiões básicas contidas. No Fock bosônico Γ_s(H1),
defina A(O)={W(f):f∈K(O)}''. Esta é a rede livre de helicidades ±1 [KNOWN].
Os resultados de localização/segunda quantização são importados da literatura,
não novos teoremas Lean nem uma derivação de gravitação interagente.
[BGL, §§2–4 e observação3.6](https://arxiv.org/abs/math-ph/0203021).

## 7. O que foi medido e o que permanece aberto

O pré-registro e o código foram pinados antes da rodada sintética. Em 128 pontos,
foram conferidos seção, Lorentz, estabilizador, cociclo, lei de Poincaré, boost,
rotação π, J², ação de J nas translações/Lorentz e jacobiano da medida. A tolerância
absoluta foi 1e−9. O maior resíduo ficou abaixo de 1,57e−13; o erro máximo da
conjugação antiga sem reflexão transversal foi 0,99109, bem acima do mínimo
pré-registrado 1e−4. A rodada inicial nem iniciou porque o sandbox não acessou o
Python científico; a execução autorizada com esse runtime gerou o único resultado.
São controles finitos de sinais/convenções, sem substituir a prova global.

Esta rede livre tem construção matemática conhecida e aqui explicitada no gauge
compatível com B0. β não entra na cinemática de Wigner e não foi inserido por nome.
O dispositivo só se identifica com ela após construir um refinamento, um setor
físico e uma equivalência unitária que entrelace a representação inteira, a reflexão
e as sub-redes localizadas. Isso é RC1 do contrato e continua [OPEN].

Também continuam [OPEN] a realização simultânea dos certificados da TGL, o
stress tensor normalizado/domínios, sua conservação na realização, a identificação
com Maxwell e o antecedente físico H3 em todas as direções. A implicação geométrica
auditada da F2.3 é reutilizada; não se deduz H3 do estado ou deste dispositivo.
O contraexemplo T→−T é excluído pela positividade adicional RC2, agora provada
para a candidata da cunha. Nada nesta camada mede hardware, 5σ ou creditação.
'''
report=new('CONSTRUCAO_CONTINUA_R1.md',text)
sources=[OUT/'sources/BGL_2002_v2.pdf',review,OUT/'continuum/PREREGISTRO_WIGNER_R1.json',OUT/'continuum/RESULTADO_WIGNER_R1.json',OUT/'CONTRATO_REDE_R2.json',OUT/'fiber_conjugation/DELIVERY_GEOMETRIC_FIBER_R1.json',OUT/'fubini/DELIVERY_R1.json']
K=ROOT/'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt/O16'
sources.extend([K/'OrbitTranslationFaithfulness_v2.lean',K/'OrbitalRapidityMeasure_v4.lean',K/'OrbitalMeasureSupport_v2.lean'])
receipt=new('CONSTRUCAO_CONTINUA_R1.json',{'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'statute':'DERIVED_ON_KNOWN','report':report,'sources':[pin(p) for p in sources],'synthetic_checks':{'samples':checks['samples'],'max_residual':max(checks['max_residuals'].values()),'negative_control_gap':checks['negative_control_gap'],'verdict':checks['verdict']},'full_poincare_lean':'OPEN','device_refinement_equivalence':'OPEN','H3_from_state':'NOT_CLAIMED','generator':pin(Path(__file__))})
print(json.dumps(receipt,ensure_ascii=False))
