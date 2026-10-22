from pathlib import Path
import hashlib,json,os,re
from datetime import datetime
R=Path(__file__).resolve().parents[1];OUT=Path(__file__).parent;V=R/'v';OLD=R.parent/'kernel'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.resolve().is_relative_to(OUT.resolve()) and not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
requested=[
 ('TGLExt/V350ScalarRegularRightGNS.lean','regularRightGNS_intertwines'),
 ('TGLExt/V350ScalarRegularRightPolar.lean','scalarTomitaPolarFactor_regular_left'),
 ('TGLExt/V350ScalarGNSStrongContinuity.lean','scalarGNSRepresentation_tendsto_of_uniformly_bounded'),
 ('TGLExt/V350DualOrbitStrongLimits.lean','dualOrbit_tendsto_of_uniformly_bounded'),
 ('TGLExt/V350ScalarHomogeneousRightOrbit.lean','hasFiniteScalarSquare_iff_memLp'),
 ('TGLExt/V350ScalarCutVacuum.lean','scalarGNSCutMap_embedding_eq_action'),
 ('TGLExt/V350ScalarGNSCutMaps.lean','scalarGNSCutMap_joint_zero'),
 ('TGLExt/V350RegularNormality.lean','vonNeumann_mem_of_strong_limit'),
 ('TGLExt/V351RegularImaginaryPowers.lean','regularSpectralCoordinates_character'),
 ('TGLExt/V350StrongOperatorIntegral.lean','operatorIntegral'),
 ('TGLExt/V351ScalarMultiplierCalculus.lean','realScalarMultiplier_cfc_ae'),
 ('.lake/packages/mathlib/Mathlib/Topology/ContinuousMap/Weierstrass.lean','exists_polynomial_near_of_continuousOn')]
sources=[]
for rel,name in requested:
 p=V/rel;origin='own private source tree, read-only'
 if not p.is_file():p=OLD/rel;origin='OLD/kernel read-only fallback; no copy/object used'
 lines=p.read_text(encoding='utf-8-sig').splitlines()
 hits=[i+1 for i,l in enumerate(lines) if re.match(r'^(?:noncomputable )?(?:def|lemma|theorem) '+re.escape(name)+r'\b',l)]
 assert len(hits)==1,(name,hits)
 sources.append(dict(declaration=name,line=hits[0],source=pin(p),origin=origin))
text='''# Consulta — extensão da ação direita do grupo aos cortes

[DERIVED / OPEN] Consulta breve, sem novo Lean, compilação ou aceite de fonte em construção. O fechamento proposto recebe duas convergências distintas: A_i→A fortemente com cota uniforme e Λν(A_i)→v em norma. Deve usar filtro não trivial (`NeBot`) ao identificar limites; para o filtro ⊥ a conclusão de identificação do vetor seria falsa. Não se deduz a segunda convergência da primeira.

Fixe o J original e escreva ρ_r(b)=Jπ(b*)J. Esta expressão é complexamente linear em b, pois estrela e conjugação antiunitária conjugam os escalares duas vezes; é antirrepresentação: ρ_r(b)ρ_r(c)=ρ_r(cb). O fornecedor `scalarTomitaPolarFactor_regular_left`, junto de J²=I, já identifica ρ_r(λ_t) com `regularRightGNS P t`; `regularRightGNS_intertwines` vale para TODO a∈nν. A identidade passa às combinações lineares finitas dos λ_t e seus produtos. Aqui λ_t*=λ_(-t), e portanto a álgebra inicial é fechada por estrela.

O passo de fechamento útil é preciso: suponha b_i→b e b_i*→b* fortemente, com ‖b_i‖≤C, e que ab_i∈nν e Λν(ab_i)=ρ_r(b_i)Λν(a). Para cada a∈nν, os operadores ab_i têm cota ‖a‖C e convergem fortemente a ab. A continuidade forte limitada da MESMA π, aplicada a b_i*, mais continuidade de J, prova a convergência EM NORMA dos vetores direitos para ρ_r(b)Λν(a). Aplicar o novo fechamento produz ab∈nν e a identidade desejada. Logo ambas as hipóteses do fechamento estão efetivamente disponíveis; não é circularidade.

Forte simples não controla os adjuntos em geral. Para os aproximantes auto-adjuntos de um corte auto-adjunto, forte já basta; para toda a álgebra gerada, explicitar forte-* ou justificar o controle dos adjuntos dentro da álgebra abeliana. A norma de ρ_r(b_i) é controlada pela norma de b_i. A mesma passagem funciona para limites em norma de operadores, o que permite extensão a C*(R) depois de obter a ação direita de R.

[REAL — fornecedores e lacuna] `dualOrbit_factorization` e `dualOrbit_tendsto_of_uniformly_bounded` tratam filtros arbitrários sem cruzar uma família não enumerável de conjuntos conulos. Entretanto, o atual `scalarGNSCutMap_embedding_eq_action` tem entrada `finiteDualLeftIdeal`, não todo nν: estendê-lo ao domínio escalar completo é parte real do fechamento proposto. `hasFiniteScalarSquare_iff_memLp` e os cortes n dão a identificação global usando apenas união contável de eventos a.e., com o MESMO dualHaarFactor. Nenhum corte individual precisa ser injetivo.

Para concluir a identidade em TODO W*(λ_t), ainda falta fornecer aproximação forte-* uniformemente limitada pela álgebra inicial (ou resultado equivalente). Nos recortes lidos não localizei esse fornecedor pronto. Mathlib `Analysis/VonNeumannAlgebra/Basic` fornece a definição por bicomutante e registra a equivalência topológica como trabalho pendente; `vonNeumann_mem_of_strong_limit` só conserva um limite já dado. `generated_transport` transporta bicomutantes; não constrói redes aproximantes. Essas observações são delimitadas aos arquivos/buscas desta consulta, não ausência universal no acervo.

[DERIVED — rota menor para o consumidor imediato] Não é necessário pagar a geração de TODO W*(λ_t) para chegar a √Bε. Basta provar a ação direita de UM operador auto-adjunto R. Depois, álgebra/polinômios e fechamento em norma estendem a ação a C*(R). A raiz do corte é a função contínua em [0,1]

    fε(x)=sqrt(x/(1−x+εx)),     ε>0.

O denominador é ≥min(1,ε)>0. Weierstrass fornece aproximações polinomiais uniformes; o CFC já existente transfere-as aos operadores. A identificação fε(R)=√Bε deve ser escrita, usando o grafo bilateral do corte ou o multiplicador espectral: não decorre só do nome de fε. Isto evita toda uma API de geração forte limitada do von Neumann gerado. Também evita supor que θ_(log ε) transporta automaticamente a ação direita GNS.

Uma construção explícita possível para esse único R, ainda NÃO fornecida como lema pronto: nas coordenadas V, use q_n(ξ)=sigmoid(2πξ) exp(−ξ²/(n+1)²). São candidatos de Schwartz, 0≤q_n≤1, e convergem pontualmente ao símbolo de R; DCT dá convergência forte dos multiplicadores auto-adjuntos com cota 1. Para cada n, inversão de Fourier representa o multiplicador por integrais fortes de λ_t com coeficiente a_n=𝓕⁻q_n, integrável. O sinal corresponde a λ_t=V M_(exp(−2πitξ)) V⁻¹. Somas finitas/integral em vetores e o fechamento dão a ação direita de cada q_n; em seguida o limite n dá a de R. Para esta rota ainda é preciso pagar a classificação Schwartz, a identidade integral e os limites de somas com cotas. Não os trato como disponíveis apenas por apontar os fornecedores de Fourier.

Armadilha dessa alternativa: t↦λ_t é fortemente contínua, não necessariamente contínua ou Bochner-mensurável em norma de B(H). Usar integrais em vetores; `StrongIntegral.operatorIntegral` já segue esse desenho para intervalos finitos. As cotas de aproximação podem depender de n no primeiro limite; a segunda passagem usa a cota espectral 1. Não é necessário impor uma cota L¹ uniforme dos coeficientes de Fourier para todos n.

Próximas ligações mínimas: fechamento da inscrição com `NeBot`; estabilidade da identidade direita por limites fortes-* limitados; obtenção dessa identidade para R; passagem por CFC contínuo a √Bε. A ordem das avaliações perturbadas e a tracialidade seguem separadas. Não se exige I=nν, minorantes positivos de ν, outro J, predual abstrato ou novo GNS.

Fornecedores relidos, linhas e hashes:

'''
for row in sources:
 p=row['source'];text+=f"- `{row['declaration']}` — [{Path(p['path']).name}](<{p['path']}:{row['line']}>) — `{p['sha256']}`; {row['origin']}.\n"
text+='\nEscopo de busca: v/TGLExt e recortes Mathlib/VonNeumannAlgebra, Fourier de Schwartz, CFC e Weierstrass; dois arquivos de cortes ausentes em v foram lidos em OLD/kernel sem cópia. Uma consulta inicial usou nomes/caminhos inexistentes e outra expressão de busca foi inválida; foram corrigidos antes das conclusões. Nenhuma varredura do acervo externo inteiro.\n'
text+='\nData: '+datetime.now().astimezone().isoformat()+'.\n'
p=OUT/'CONSULTA_ACAO_DIREITA_CORTES.md';fresh(p,text.encode('utf8'))
data=dict(status='DERIVED_CONSULTATION__NO_NEW_LEAN__RIGHT_ACTION_BRIDGES_OPEN',note=pin(p),providers=sources,
 source_reads_only=True,new_theorems=0,builds_executed=0,prior_reports_modified=False,
 key_gap='Bounded strong-star generation, or just a bounded strong approximation of R with already proved right action',
 required_filter='NeBot for the proposed closed-embedding identification',
 trace_open=True)
fresh(OUT/'CONSULTA_ACAO_DIREITA_CORTES.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(note=pin(p),json=pin(OUT/'CONSULTA_ACAO_DIREITA_CORTES.json')),ensure_ascii=False))
