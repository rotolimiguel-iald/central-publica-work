from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
CAP=REV/'consulta_rvd56_cfc_20260913'
LIB=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
names=['HilbertProjectionBlocks','ComplexGraphProjection','ScalarRightMultiplicationGraph','ScalarRightProjectionPair','ScalarRightPairVector','ScalarRightHilbertCore','ScalarRightGraphCore','ScalarTomitaAdjointPolar','ScalarRightConjugateGraph','ScaledPositiveResolvent']
paths=[ROOT/'kernel/TGLV350'/(n+'.lean') for n in names]+[
 LIB/'Analysis/InnerProductSpace/LaxMilgram.lean',
 LIB/'Analysis/SpecialFunctions/ContinuousFunctionalCalculus/PosPart/Basic.lean',
 LIB/'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean',
 LIB/'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean',
 REV/'consulta_right_bounded_20260912_214127_316501/rieffel_van_daele_1977.pdf',
 ROOT/'adjoint_polar_graph_custody.json']
hf=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={str(p):hf(p) for p in paths}
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def atomic(p,raw):
 assert p.resolve().is_relative_to(REV)
 if p.exists():
  before=p.read_bytes();bk=p.with_name(p.name+'.bak_'+stamp)
  with bk.open('xb') as f:f.write(before)
  assert bk.read_bytes()==before
  raw=before+b'\n\n'+raw
 q=p.with_name(p.name+'.tmp_'+stamp)
 with q.open('xb') as f:f.write(raw)
 assert q.read_bytes()==raw;q.replace(p);assert p.read_bytes()==raw
text=r'''# Consulta — RVD5.6: inversão do bloco por parte positiva contínua

__DATE__. [DERIVED — argumento matemático proposto nesta consulta, não compilado nem revisado como DEV.] Leituras locais e conferência visual do PDF; zero execuções Lean, monólito ou helpers autorais; nenhuma escrita fora de revisao.

**Diagnóstico:** a etapa de inversão admite uma prova curta por CFC contínuo, com a cota exata A≥(1+‖ℓ(ξ)‖²)⁻¹I. Não precisa de PVM, projeções espectrais descontínuas ou limite ε→0. A ponte variacional deve, entretanto, produzir a identidade de teste ponderada explicitada abaixo. Não se obtém essa identidade apenas da existência Lax–Milgram.

**Convenções e leitura primária.** Conferi visualmente as páginas impressas211–213 (índices PDF25–27) da cópia local de [Rieffel–Van Daele, 1977, lema5.6](https://msp.org/pjm/1977/69-1/pjm-v69-n1-p17-s.pdf). A prova impressa elimina um intervalo espectral próximo de zero e depois exclui o núcleo. A forma real usada na seleção não precisa ser simétrica: a implementação adequada é Lax–Milgram. As equações e sua orientação foram lidas nas imagens, sem confiar no OCR. O argumento com parte positiva a seguir é uma substituição proposta aqui para a etapa de cortes espectrais.

Abaixo **A é o bloco superior esquerdo da projeção do gráfico**, não Δ=S†S. Escreva

    Gη = closure {(j(a), ℓ(a)η) : a∈E},
    P_G = [ A  B ; B*  D ],    ξ=j(a₀), a₀*=a₀,
    m=‖ℓ(a₀)‖,   c=1+m² ≥1.

No caso pretendido, E é a álgebra de pares direitos, j=scalarRightPairVector, ℓ(a)=a.val, fecho da estrela=F original, adjunto=S original e η∈Fix S. Não se muda o J. As relações abaixo são de operadores limitados, embora Gη inicialmente possa ser apenas uma relação fechada.

Da projeção ortogonal: 0≤A≤I, A=A*, BB*=A(I−A), BD=(I−A)B. Todos os blocos comutam com ℓ(E), pois Gη é redutor. Da simetria de multiplicação para η fixo pelo adjunto:

    B j(a)=Aℓ(a)η=ℓ(a)Aη,
    Bℓ(a)η=(I−A)j(a),
    B*ℓ(a)η=Dj(a).

**A é injetivo antes da estimativa, mas ainda não invertível:** Ax=0 implica ‖P_G(x,0)‖²=Re⟨x,Ax⟩=0. Logo (x,0)∈Gη⊥; a densidade de j(E) dá x=0. Não requer Gη ser gráfico de um operador limitado.

**A identidade que a seleção variacional deve fornecer.** Para e≥0, função contínua de A, defina

    ζ=eBB*η,       ζᵇ=B*eBη,
    K=e(I−A)B,    K*=B*e(I−A).

As relações dos blocos dão ℓ(a)ζ=Kj(a) e ℓ(a)ζᵇ=K*j(a). A ordem é **e(I−A)B**, não eB(I−A). Não se presume [A,B]=0, [e,B]=0 ou normalidade de B.

Com produto interno Lean conjugado-linear no primeiro argumento, a identidade de teste necessária é

    2 Re⟨ξ,ζᵇ⟩ = Re⟨η,ζᵇ⟩ + Re⟨ζ,η⟩.                 (V)

Ela decorre de Re λ=1 e da identidade complexa

    2⟨ξ,ζᵇ⟩=λ⟨η,ζᵇ⟩+conj(λ)⟨ζ,η⟩,

se o par estiver no gráfico do adjunto usado para separar as partes real/imaginária. Os dois termos à direita de (V) são reais não negativos, pois B*eB≥0 e eBB*=eA(I−A)≥0. Cauchy–Schwarz/2ab≤a²+b², aplicados com √e, cancelam Re⟨η,B*eBη⟩ e fornecem

    Re⟨η,eA(I−A)η⟩ ≤ ‖√e Bξ‖²
                        = ‖ℓ(a₀)√e Aη‖²
                        ≤ m² Re⟨η,eA²η⟩.                (E)

Aqui √e comuta com ℓ(a₀), porque A comuta; não foi comutado com B.

**Substituição econômica do corte espectral.** Tome, uma única vez,

    e = CFC.posPart (I−cA) = cfc(t↦max(1−ct,0),A).

Então e≥0, e comuta com A e ℓ(E), e a identidade contínua f(t)(1−ct)=f(t)² dá

    e(I−cA)=e².

De (E):

    0 ≥ Re⟨η,eA(I−cA)η⟩
      = Re⟨η,Ae²η⟩ = ‖√A eη‖² ≥0.

Consequentemente Aeη=0. Como A e=eA, vale eAη=0. Para todo a,

    eB j(a)=ℓ(a)eAη=0;

densidade de j(E) e continuidade dão **eB=0**. Usando BB*=A(I−A), obtemos A e(I−A)=0. A injetividade de A implica e(I−A)=0, portanto eA=e. Finalmente

    e²=e(I−cA)=(1−c)e≤0.

Como e²≥0, resulta e²=0 e e=0. A parte positiva nula implica I−cA≤0: **A≥c⁻¹I**. Este argumento inclui m=0/c=1 sem divisão por m ou c−1. Tudo é CFC contínuo/álgebra de operadores limitados; não se pede antecipadamente IsUnit A.

O último passo de implementação pode usar IsStrictlyPositive(c⁻¹I) mais A−c⁻¹I≥0; então IsStrictlyPositive.isUnit fornece a inversa limitada. Alternativamente, a cota inferior e auto-adjunção dão imagem fechada e densa. Defina R=A⁻¹B. Ele comuta com ℓ(E), satisfaz Rj(a)=ℓ(a)η e é simétrico sobre j(E); por densidade, R*=R. Assim também R*j(a)=ℓ(a)η: o multiplicador possui o adjunto pretendido, sem supor A⁻¹ anteriormente.

**Lacuna de aplicação ao Fix S que não deve desaparecer numa hipótese silenciosa.** Para usar a seleção somente em Fix S, é preciso provar ζ∈D(S) e Sζ=ζᵇ para esses testes (ou diretamente (V)). A partir do graph-core original de F, basta provar o pareamento

    ∀a∈E, ⟨j(a*),ζ⟩ = ⟨ζᵇ,j(a)⟩.                    (P)

A existência de K,K* com as duas leis de multiplicação acima, isoladamente, dá esse pareamento imediatamente **sobre produtos**: para a,b∈E,

    ⟨j(b*a*),ζ⟩ = ⟨j(a*),Kj(b)⟩
                 = ⟨K*j(a*),j(b)⟩ = ⟨ζᵇ,j(ab)⟩.

Não localizei aqui um lema que estenda isso a todos os a usando o graph-core de E². `scalarRightPairVector_products_dense` afirma só densidade Hilbert e explicitamente exclui essa conclusão de gráfico. O graph-core agora disponível é o de **E inteiro**, não automaticamente o de seus produtos. Por isso (P)/(V) deve ter prova concreta; esta consulta não declara sua descarga. Outra formulação usa o complemento simplético do fecho real dos quadrados, como na organização RVD, mas então é necessário ligar esse subespaço ao Fix S original, sem substituir J. Esse é um elo distinto da inversão de A, cujo argumento acima está completo sob (V).

**Interfaces verificadas e próximos lemas propostos (nomes novos, não existentes):**

| Existente | Uso / complemento necessário |
|---|---|
| `complexGraphClosure`, `complexGraphClosure_projection_commutes`, `complexGraphClosure_projection_rotated` | Relação fechada, comutação da projeção e vetor rodado; aplicar genericamente à álgebra E. |
| `hilbertBlockA/B/D`, `hilbertBlockB_adjoint`, `hilbertBlockA/B/D_commutes` | Mesmos blocos/comutação. Novos lemas explícitos devem extrair 0≤A≤I e as identidades de P²=P. |
| `hilbertBlockB_from_rotated`, `hilbertBlockBadjoint_from_fixed` | Duas equações já públicas; extrair também a coordenada superior de P(x,y)=(x,y) e a inferior de P(y,−x)=0. |
| `complexGraph_projection_inl_ne_zero` | Junto à energia da compressão, prova a injetividade de A. Positividade pontual não é cota uniforme. |
| `scalarRightPairVector_mul`, `scalarRightPairVector_inner_product`, `scalarRightPairGraph_closure_eq_original` | Produto, adjunto e graph-core F para a aplicação. `ScalarRightProjectionPair` existente está especializado ao ideal escalar original/F-fixo: não deve ser reutilizado por troca de nomes para E/S-fixo. |
| `IsCoercive.continuousLinearEquivOfBilin`, `…_apply` | Lax–Milgram real no subespaço fechado. Usar a inversa da equivalência para resolver o funcional; não a forma como novo produto interno. |
| `CFC.posPart_nonneg`, `CFC.posPart_sub_negPart`, `CFC.posPart_mul_negPart`, `CFC.posPart_eq_zero_iff`; `IsSelfAdjoint.commute_cfc` | Constroem e, a identidade e(I−cA)=e² e a passagem e=0⇒I≤cA. `cfc_mul`, `cfc_congr`, `cfc_nonneg` são a alternativa com max explícito. |
| `scaledResolventDenominator_positive`, `ring_inverse_commutes_of_unit` | Modelos locais já existentes para estrita positividade e comutação da inversa **depois** de IsUnit. |

Prioridade: (1) `graph_projection_block_relations`; (2) `positive_part_gap_from_weighted_graph_test`, recebendo (V)/(E) explicitamente e concluindo a cota c⁻¹I≤A; (3) prova concreta de `weighted_graph_pair_original_adjoint`/(P), seguida do teste variacional; (4) montagem R=A⁻¹B. Os itens2 e3 são separáveis, e o item2 não precisa de PVM nem de resultados modulares.

Dois alertas concretos: um operador diagonal Aₙ=(1+n²)⁻¹ é positivo, injetivo e bloco da projeção do gráfico de diag(n), mas não tem inversa limitada; logo a estimativa (V) não pode ser omitida. E Bλ(u,v)=Re(λ⟨u,v⟩) não é simétrico em geral, apesar de Bλ(u,u)=‖u‖². A coerção real preserva a norma, não cria simetria. [OPEN] Inversa global dos comutantes, Δ^it/KMS, traço e gate não são concluídos nesta consulta.

Pins das fontes consultadas, PDF local e imagens em `consulta_rvd56_cfc_20260913/consultation_pins.json`. Nenhuma fonte Lean ou memória foi editada; nenhum pacote foi compilado.
'''.replace('__DATE__',date)
p=REV/'CONSULTA_RVD56_BLOCO_INVERSIVEL_CFC.md'
atomic(p,text.encode())
meta={'timestamp':date,'mode':'READ_ONLY_MATHEMATICAL_CONSULTATION_NO_COMPILATION','source_pins':pins,'rendered_pdf_pages_zero_based':[25,26,27],
 'images':{str(p):hf(p) for p in CAP.glob('rvd-*.png')},'report':str(p),'report_sha256':hf(p),'new_Lean_executions':0,'author_programs_executed':False,
 'result':'Conditional algebraic proof of optimal block lower bound; weighted test/original-adjoint bridge explicitly outstanding'}
q=CAP/'consultation_pins.json';assert not q.exists();atomic(q,(json.dumps(meta,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'report':str(p),'sha256':hf(p),'pins':str(q)},ensure_ascii=False))
