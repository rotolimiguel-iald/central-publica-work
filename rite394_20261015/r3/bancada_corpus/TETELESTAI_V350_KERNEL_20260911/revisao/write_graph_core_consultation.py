from pathlib import Path
import datetime, hashlib, json, re, os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
now = datetime.datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
OUT = REV / ('consulta_graph_core_' + stamp)
OUT.mkdir()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_bytes())
mother = ROOT / 'right_vector_custody.json'
mv = load(ROOT / 'right_vector_custody_verification.json')
assert mv['custody_ok'] and mv['custody_sha256'] == sha(mother)
for p, h in load(mother)['review_sha256'].items():
    assert sha(p) == h, p
refs = {
 'TGLV350/ScalarWeightDomain.lean': ['scalarWeightLeftIdeal_left_mul'],
 'TGLV350/ScalarWeightAction.lean': ['scalarWeightGNSAction_intertwines', 'scalarWeightGNSEmbedding_injective', 'scalarWeightGNSEmbedding_denseRange'],
 'TGLV350/ScalarWeightStarCore.lean': ['scalarWeightStarCore', 'scalarWeightTomitaGraph'],
 'TGLV350/ScalarWeightTomitaIdentification.lean': ['scalarClosedTomita_graph_eq_weight', 'scalarClosedTomita_extends_weight_star'],
 'TGLV350/ScalarTomitaAdjoint.lean': ['scalarTomitaAdjoint_pairing', 'scalarTomitaAdjoint_isClosed', 'scalarTomitaAdjoint_gaussian_domain', 'scalarTomitaAdjoint_involutive'],
 'TGLV350/ScalarRightAdjointPair.lean': ['ScalarRightAdjointPair', 'scalarRightAdjointPair_maximal'],
 'TGLV350/ScalarPairedRightAlgebra.lean': ['scalarRightAdjointPair_add', 'scalarRightAdjointPair_star', 'scalarPairedRightAlgebra'],
 'TGLV350/ScalarRightPairVector.lean': ['scalarRightPairVector_of_pair', 'scalarRightPairVector_original_adjoint', 'scalarRightPairVector_denseRange'],
 'TGLV350/ScalarRightHilbertCore.lean': ['scalarRightPairGraph_closure_subset_original', 'scalarRightPairVector_products_dense'],
 'TGLV350/ScalarGaussianRightPairs.lean': ['scalarGaussianGNSMap_weightEmbedding', 'scalarGaussianRightAdjointPair'],
 'TGLV350/ScalarGaussianClosureTransport.lean': ['scalarGaussian_maps_graph_closure'],
 'TGLV350/ScalarGaussianGNSMap.lean': ['scalarGaussianGNSMap', 'scalarGaussianGNSMap_intertwines'],
 'TGLV350/ScalarGaussianImage.lean': ['scalarGaussianImage_eq_orbit', 'scalarGaussianVacuum_mem_image'],
 'TGLV350/ScalarGaussianUnitary.lean': ['scalarGaussianUnitary_intertwines', 'scalarGNSCyclicVector_separating'],
 'TGLV350/VectorTomitaClosability.lean': ['vectorTomita_closure_pairing'],
 'TGLV350/ScalarTomitaStandardSubspace.lean': ['scalarClosedTomita_fixed_decomposition'],
 'TGLExt/ClosedAntilinearStandardSubspace.lean': ['domain_fixed_decomposition', 'fixedRealSubmodule_closed'],
 'TGLV350/ReducingCommutantTransport.lean': ['reducing_projection_intertwines'],
 'TGLV350/ClosedAntilinearResolvent.lean': ['antilinearL2Graph'],
 'TGLV350/PositiveRootIntertwining.lean': ['positive_sqrt_intertwines'],
 'TGLV350/ReducingCommutantCompression.lean': ['reducingCommutant_gram_commutes', 'reducingBicommutant_orbit_bound'],
 'TGLV350/ReducingBicommutantLift.lean': ['reducingBicommutantLift_apply', 'reducingBicommutantLift_mem', 'reducingBicommutantLift_restrict', 'reducingBicommutant_has_preimage'],
}
pins = {}
for rel, names in refs.items():
    p = ROOT / 'kernel' / rel
    lines = p.read_text(encoding='utf-8').splitlines()
    found = {}
    for n in names:
        matches = [i for i, s in enumerate(lines, 1) if re.search(r'\b(?:theorem|def|structure)\s+' + re.escape(n) + r'\b', s)]
        assert len(matches) == 1, (rel, n, matches)
        found[n] = matches[0]
    pins[rel] = {'path': str(p), 'sha256': sha(p), 'declarations': found, 'mode': 'SOURCE_INSPECTION_NO_COMPILATION'}
    if rel.endswith('ReducingBicommutantLift.lean'):
        pins[rel]['mode'] = 'IN_PROGRESS_AUTHOR_SOURCE_INSPECTION_ONLY_NOT_CERTIFIED'

doc = r'''# Consulta — núcleo de grafo do F original

Data: @DATE@. **[DERIVED — análise de prova, não teorema Lean novo]** Há uma rota concreta pelo grafo de multiplicação direita de um vetor fixo de F. Ela produz uma identidade positiva que elimina o complemento ortogonal dos vetores direitos auto-adjuntos. Não exige provar antes preservação por resolvente, identificar o J gaussiano ou obter π(N) fechada como VNA.

## 1. Objetos e fatos locais utilizados

Fixar H=H_I, π=`scalarGNSRepresentation P`, Λ=`scalarWeightGNSEmbedding P`, L=nν=`scalarWeightLeftIdeal P`, S=`scalarClosedTomita P` e F=`scalarTomitaAdjoint P`. Denotar por E a imagem de j=`scalarRightPairVector P`. O produto interno segue Lean: conjugado-linear na primeira variável.

**[REAL — enunciados lidos, compilação herdada]** L é ideal esquerdo, Λ é linear/injetiva e tem imagem densa em H; π(c)Λ(a)=Λ(ca). S estende Λ(a)↦Λ(a*) em L∩L*. F é o adjunto máximo desse mesmo S, fechado e involutivo. Todo par limitado satisfaz F j(R)=j(R*). O fecho do grafo em E já está contido em graph F. Não se altera nenhum desses objetos.

A hipótese recebida crucial para o passo novo é apenas η∈D(F), Fη=η. Não se recebe densidade na norma de grafo, fechamento de π(N), KMS ou identificação de ideais.

## 2. Ponte proposta: projeção do grafo linear de multiplicação direita

Para η∈Fix F, formar diretamente o subespaço complexo fechado

    Gη = closure { (Λ(a), π(a)η) : a∈L }  ⊂ H⊕₂H.

Em Lean, pode-se usar o fecho da imagem de um mapa linear definido em L. Assim não é necessário escolher antecipadamente um operador não limitado nem provar que seu domínio máximo foi encontrado. **Este grafo auxiliar é complexo-linear.** Não é o grafo antilinear de F, que é tratado sobre ℝ. Usar `WithLp 2 (H × H)` para a norma quadrática e a projeção ortogonal complexa.

### 2.1 A simetria necessária já vem do F original

Para a,b∈L, tanto a*b como b*a pertencem a L∩L*: isso usa duas aplicações da propriedade de ideal esquerdo. Aplicar o pareamento de F a x=Λ(a*b), com Sx=Λ(b*a), dá

    ⟨π(a)η, Λ(b)⟩ = ⟨η, Λ(a*b)⟩
                    = ⟨Λ(b*a), η⟩
                    = ⟨Λ(a), π(b)η⟩.

Logo `(π(a)η, −Λ(a)) ∈ Gη⊥`. A igualdade é complexa, não apenas de partes reais. Nenhuma continuidade de S/F foi presumida.

### 2.2 Blocos da projeção

Gη é invariante por diag(π(c),π(c)) para todo c∈N, pois ca∈L. O mesmo vale para c*, então Gη é redutor. A projeção ortogonal Pη comuta com essa ação diagonal. Escrever seus blocos como

    Pη = [ A  B  ]      Pη*=Pη=Pη²,
         [ B* D  ]      0≤A≤1, 0≤D≤1.

Todos os blocos comutam com π(N). A comutação da projeção pode reutilizar a ideia de `reducing_projection_intertwines`/`starProjection_commutes_of_invariant`, aplicada ao espaço somado. Não é necessária a hipótese de que π(N) já seja VNA.

Como Pη fixa `(Λ(a),π(a)η)` e anula `(π(a)η,−Λ(a))`, suas coordenadas dão, para TODO a∈L,

    B Λ(a)  = π(a) Aη,
    B*Λ(a)  = π(a) (1−D)η.

Portanto **B tem um `ScalarRightAdjointPair` concreto**, com vetores Aη e (1−D)η. Somar esse par ao seu adjunto, usando as operações existentes, fornece

    Rη = B+B*,          vη = (A+1−D)η,
    Rη*=Rη,             RηΛ(a)=π(a)vη,
    Fvη=vη,             j(Rη)=vη.

Aqui `j(Rη)` significa o elemento do subtipo da álgebra pareada, munido do par construído. Não se conclui que η já seja right-bounded, nem que o operador não limitado inicial tenha adjunto máximo conhecido.

### 2.3 Identidade que efetivamente resolve a densidade real

A ortogonalidade da projeção fornece

    Re⟨η,vη⟩ = ‖Pη(η,0)‖² + ‖(1−Pη)(0,η)‖².                (★)

Se η≠0, o primeiro termo não pode ser zero: Pη(η,0)=0 implicaria `(η,0)⊥Gη`, logo η⊥Λ(L), contrariando a densidade de Λ(L). Assim (★) é estritamente positiva para η≠0.

Este é o próximo lema concreto recomendado: **todo η não nulo fixo por F admite um par auto-adjunto explícito com Re⟨η,j(Rη)⟩>0**, obtido pelos blocos acima. Não é um campo de graph-core rebatizado: a construção do par e a identidade (★) são a prova que falta formalizar.

## 3. Da ponte ao grafo inteiro — sem trocar J

Seja E_sa={j(R): R pareado, R*=R}. É um subespaço real de Fix F. Se seu fecho fosse próprio em Fix F, a projeção real produziria η≠0 em Fix F ortogonal a E_sa. O par Rη construído na seção 2 contradiz essa ortogonalidade por (★). Portanto

    closure E_sa = Fix F.

Para z∈D(F), usar a decomposição do MESMO F involutivo:

    h=(z+Fz)/2,   k=(z−Fz)/(2i),   z=h+ik,   Fz=h−ik,
    h,k∈Fix F.

Aproximar h e k por j(Rn),j(Tn) com Rn,Tn auto-adjuntos. Então

    j(Rn+iTn) → z,        j((Rn+iTn)*)=j(Rn−iTn) → Fz.

Com a inclusão já provada, isso conclui a igualdade desejada dos FECHOS. A escolha de sequências para dois pontos de um espaço métrico não exige separabilidade global de H. A infraestrutura `ClosedAntilinearStandardSubspace.domain_fixed_decomposition` é genérica; deve ser especializada em F, pois o wrapper `scalarTomitaStandardSubspace` existente usa S.

**[OPEN — formalização]** Esta consulta não compilou esses passos. Sugestão de divisão: (i) simetria no domínio Λ(L) e subespaço gráfico redutor; (ii) blocos, par e identidade (★); (iii) densidade real e igualdade do grafo. Cada aplicação deve descarregar as hipóteses nas fontes atuais. Não é necessário construir Δ^it, KMS, uma nova conjugação ou inversa gaussiana para essa rota.

## 4. Avaliação das outras rotas e contraexemplos

**Família gaussiana fixa.** As fontes fornecem `(C*BΩg,C*B*Ωg) ∈ graph F` e densidade Hilbert da primeira coordenada. Não foi localizado um lema que faça essa família específica um core de F. A rota acima usa TODOS os pares admissíveis; não prova, por si só, que os pares C*BC sejam um core. A injetividade de C não dá uma estimativa inversa de norma de grafo.

**Pré-imagem gaussiana.** `scalarGaussian_maps_graph_closure` fornece somente uma inclusão. Para convertê-la em igualdade por pré-imagem, seria preciso mostrar que convergência das duas imagens por C permite aproximação simultânea das duas coordenadas originais. Injetividade/continuidade não permitem essa passagem. Além disso, o adjunto de uma composição fechada com C pode exigir fechamento e hipóteses de domínio. A identidade do adjunto auxiliar com o fecho de seu grafo de comutante também não pode ser usada sem prova.

**Resolvente.** O critério sugerido é suficiente: se R_F=(1+F†F)⁻¹ está construído e R_F(E)⊆E, então R_F e F R_F são limitados; a densidade de E leva R_F(E) ao fecho gráfico de Ran R_F, e Ran R_F é core de F. A variante pela projeção de graph F levando E×E a graph(F|E) também funciona. Porém não há, nas pontes consultadas, a preservação de E; comutação de certos geradores não a fornece. A projeção da seção 2 é de OUTRO grafo, Gη, e resolve o problema sem assumir essa preservação.

**Quadrados/RVD.** A pertença de JΛ(a*a) a E, com operador Jπ(a*a)J, seria uma ponte válida, mas exige a identidade vetorial de ação direita; apenas a pertença de Jπ(a*a)J ao comutante não basta. Rieffel–Van Daele 5.10 fornece a ponte vetorial na sua construção, e 5.12 a utiliza para a densidade real. A construção por blocos do lema 5.4 oferece a alternativa explorada aqui; a combinação `A+1−D` e o argumento (★) foram explicitados nesta consulta. Não se importou 5.13 como hipótese. [Fonte primária, §5](https://msp.org/pjm/1977/69-1/pjm-v69-n1-p17-s.pdf).

**Contraexemplo à inferência “denso e F-invariante ⇒ core”.** Em H=ℓ²⊕ℓ², seja N=diag(n), n≥1, e

    F(x,y)=(N conjugate(y), N⁻¹ conjugate(x)),  D(F)=ℓ²⊕D(N).

É uma involução antilinear fechada e densamente definida. A funcional de grafo

    L(x,y)=Σ x_n/n + Σ y_n

é contínua na norma de grafo, e L(Fz)=conjugate(Lz). D₀=ker L⊂D(F) é F-invariante e fechado na norma de grafo, mas próprio. Ainda assim é denso em H: corrigir L(z) por vetores na segunda coordenada, com m entradas 1/m em índices de m+1 a 2m, altera a norma de H por O(m⁻¹/²) e altera L por 1. Portanto F|D₀ é uma restrição fechada densa própria, não um core. Isso refuta a inferência topológica isolada; não pretende ser contramodelo da álgebra pareada concreta, cujas identidades adicionais são usadas na seção 2.

**K_h(I).** O alerta tracial está correto. Em L∞(0,1) agindo em L²(0,1), F é conjugação e os vetores right-bounded são L∞. A aproximação constante K_h=I não leva η(t)=t⁻¹/⁴∈L² a L∞. Logo aproximação forte da identidade não implica regularização de todo D(F) em E.

## 5. A outra obrigação: imagem π(N) como VNA

**[DERIVED — argumento válido, a formalizar]** A proposta do operador evita compactidade WOT e não depende do núcleo de grafo acima. Fixar M⊂B(E₀) VNA, K fechado redutor, Ω∈K separante para M, e m=M|K. Para B∈m″, usar a órbita densa M′Ω e definir

    T₀(DΩ)=D(BΩ),      D∈M′.

Para Q_D=P_KD*D|K, temos Q_D≥0 e Q_D∈m′. B comuta com Q_D e sua raiz positiva; assim

    ‖DBΩ‖²=⟨BΩ,Q_D BΩ⟩=‖√Q_D BΩ‖²
           ≤‖B‖²‖√Q_D Ω‖²=‖B‖²‖DΩ‖².

A estimativa prova simultaneamente boa definição e limitação de T₀. A órbita é um subespaço linear; estender por continuidade dá T̃∈B(E₀). Para D₀,D∈M′, a fórmula em D₀DΩ prova T̃D₀=D₀T̃. Logo T̃∈M″=M.

Como K reduz M, T̃P_K=P_KT̃. Para cada D∈M′, Q_D⁰=P_KD|K∈m′, então

    T̃(P_KDΩ)=P_KD(BΩ)=Q_D⁰ BΩ=B Q_D⁰Ω=B(P_KDΩ).

P_KM′Ω é denso em K, e portanto T̃|K=B. A inclusão m⊆m″ dá m=m″. Não se supõe Ω separante para m″, nem se estende B por zero para alegar comutação com todos os blocos de M′. Apenas a extensão em M′Ω possui a comutação necessária.

Na aplicação atual, tomar M=`dualOrbitVonNeumann (regularCoreAlgebra P)`, K=`scalarGaussianImage P` e Ω=Ωg. As fontes fornecem Ωg∈K e separação de M; `scalarGaussianUnitary_intertwines` transporta m para π(N) no mesmo H_I. `positive_sqrt_intertwines` ajuda a justificar a comutação com √Q_D. Nenhuma identidade J_vetor=J_peso é necessária.

**Atualização de fonte durante a consulta.** Foram lidos integralmente `ReducingCommutantCompression.lean` e a versão em compilação de `ReducingBicommutantLift.lean`. O primeiro realiza a cota pelo Gram C*C da coluna C=D∘incl, com hB quantificado sobre o comutante da imagem efetiva. O segundo usa `extendOfNorm`, descarrega seu bound e sua densidade nos lemas de aplicação, prova pertença por comutação em M′Ω e restringe pela órbita projetada. Não identifiquei circularidade matemática nessa composição. O rc0 do primeiro foi informado pelo autor; não houve recompilação própria. A versão lida do segundo é provisória para fins desta consulta e não foi certificada como módulo compilado. A futura aplicação gaussiana deverá instanciar hS, hB e hsep efetivamente.

## 6. Diagnóstico final e proveniência

Prioridade sugerida: formalizar a projeção complexa Gη e o par de blocos B, cuja identidade (★) dá a redução real do graph-core. A prova de imagem VNA é igualmente concreta e pode avançar independentemente. Nenhuma delas deve ser anunciada como nova prova Lean antes de recompilação/auditoria próprias.

Não foram executados Lean, integradores, recorders, testes autorais ou monólito nesta consulta. Nenhuma fonte, memória ou parecer custodiado foi alterado. Custódia atual lida: `right_vector_custody.json`, SHA `@MOTHER@`; sua verificação autoral foi lida, não repetida. Fonte primária consultada pela extração textual do PDF; a tentativa de captura de página falhou por cache, e não foi usada como evidência visual. As identidades da rota proposta foram verificadas algebraicamente acima com a convenção de Lean.

Pins e localização dos enunciados lidos: [consultation_pins.json](<@PINS@>). Os resultados antigos são herdados das revisões seladas; as propostas e o contraexemplo deste documento são análise matemática, não certificação de novos módulos. O objetivo global, KMS/fluxo modular/traço e flags permanecem fora desta consulta.
'''
doc = doc.replace('@DATE@', now.isoformat()).replace('@MOTHER@', sha(mother)).replace('@PINS@', (OUT/'consultation_pins.json').as_posix())
data = {'timestamp': now.isoformat(), 'mode': 'CONCEPTUAL_SOURCE_INSPECTION_NO_LEAN_EXECUTION',
        'custody_sha256': sha(mother), 'custody_verification_sha256': sha(ROOT/'right_vector_custody_verification.json'),
        'source_pins': pins, 'primary_source': 'https://msp.org/pjm/1977/69-1/pjm-v69-n1-p17-s.pdf',
        'web_text_read': True, 'web_pdf_screenshot_failed_cache_miss': True,
        'new_theorems_compiled': False, 'author_code_executed': False, 'memories_written': False}
def atomic(p, b):
    assert p.resolve().is_relative_to(REV)
    q=p.with_name(p.name+'.tmp_'+stamp)
    with q.open('xb') as f: f.write(b)
    assert q.read_bytes()==b and len(b)>0
    os.replace(q,p)
    assert p.read_bytes()==b
atomic(OUT/'consultation_pins.json',json.dumps(data,ensure_ascii=False,indent=2).encode())
p=REV/'CONSULTA_GRAPH_CORE_ORIGINAL_F.md'
if p.exists():
    before=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+stamp)
    with bak.open('xb') as f:f.write(before)
    assert bak.read_bytes()==before
    raw=before+b'\n\n'+doc.encode()
else:
    before=b'';raw=doc.encode()
atomic(p,raw)
assert p.read_bytes().startswith(before)
assert sha(mother)==data['custody_sha256']
for r in pins.values():assert sha(r['path'])==r['sha256']
for rp,h in load(mother)['review_sha256'].items():assert sha(rp)==h
print(json.dumps({'report':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'pins':str(OUT/'consultation_pins.json'),'Lean_executions':0},ensure_ascii=False))
