[REAL / INPUT / OPEN] CONTINUAÇÃO 029 — geometria curva, correspondência entrópica e liberdade residual

06/09/2026. Foi construída uma família explícita de métricas curvas, com matéria escalar conservada e os estados globais da entrega 028, para a qual a condição de correspondência entre entropia e área é demonstrada. Um parâmetro de curvatura permanece livre com a mesma fonte e a mesma família de estados.

A construção é uma solução dentro de um ansatz escolhido. Não é uma dinâmica microscópica que obrigue a natureza, ou todo modelo quântico, a realizar essa solução. A origem geral de H3 permanece aberta.

## Evidência e estado anterior

[REAL] O auditor da 028 foi executado novamente em modo somente leitura: PASS, 730 hashes, oito módulos, 112 teoremas, seis definições impressas. A última resposta ao operador foi esclarecimento de estado, sem nova demonstração, e foi classificada como NO PROGRESS para a meta. Esta etapa produz fontes, provas e controles novos; é PROGRESSO.

A inspeção final de 029 mediu seis módulos, 64 teoremas e 12 definições com axiomas impressos separadamente. As contagens incluem lemas auxiliares e controles. Todos os fontes finais têm compilação com exit 0, bytes estáveis, zero erros, zero avisos e zero sorryAx. As dependências axiomáticas impressas pertencem somente a propext, Classical.choice e Quot.sound. Dez tentativas rejeitadas foram preservadas, com logs e fontes recuperáveis pelos backups dos bytes. Auditoria independente da gerência pendente.

O túnel contém ordens 001–007. A entrega é espontânea, associada à continuação da ordem 007. O Atlas declara v317 com incorporação até a 023; isso não foi tratado como incorporação das entregas seguintes.

## A métrica e sua conexão

[INPUT] Trabalhamos na carta Coordinate4, com coordenadas (t,x,y,z), e adotamos a forma lorentziana eta4=diag(1,-1,-1,-1) já usada na bancada. Para a,c reais,

    k = (1,0,0,1)
    l = (1,0,0,-1)
    N = l⊗k
    H(t,x,y,z) = a x²+c y²
    E = I+(H/2)N
    D = I−(H/2)N.

[REAL] PlaneWaveSolder prova N²=0, ED=DE=I, suavidade e as identidades

    g = Eᵀ eta4 E = eta4+H k⊗k
    gInv = D eta4 Dᵀ = eta4−H l⊗l.

A métrica é construída pelo mesmo frameMetricField da cadeia anterior. A escolha da assinatura é uma entrada. Suavidade em todo R⁴ não é uma prova de completude geodésica, nem uma construção de variedade global a partir da álgebra quântica.

Para v=(0,a x,c y,0), a conexão calculada é

    Γ_i^r_j = l_r(k_j v_i+k_i v_j)+v_r k_i k_j.

[REAL] wave_metric_jet usa o fderiv real da função H. wave_levi_civita identifica exatamente essa expressão com frameLeviCivita E D; não se atribui o nome de conexão geométrica a um objeto independente. A conexão é suave e sem torção. Seu primeiro jato também é calculado por derivadas; o comutador das matrizes da conexão é zero nesta família, por prova algébrica.

## Curvatura e matéria

[REAL] Na convenção de Riemann do código, o cálculo resulta em

    Ric = (a+c) k⊗k
    scalarCurvature = 0
    G = Ric
    R¹_(0 1 0) = a
    R²_(0 2 0) = c.

As duas últimas expressões são coordinateCurvature Γ x 1 0 1 0 e coordinateCurvature Γ x 2 0 2 0. A ordem dos índices foi mantida explicitamente.

[REAL] O covetor w=k é nulo na métrica inversa, paralelo e fechado. wave_covector_potential demonstra que ele é o gradiente de t+z. Portanto satisfaz a equação de onda CovectorWaveOn. Para qualquer constante κ,

    T = κ [w⊗w−gInv(w,w)g/2] = κ k⊗k.

wave_matter_conserved prova a conservação desse tensor usando a Levi-Civita real. Não se usa apenas a conservação do símbolo linearizado. wave_matter_nonzero fornece o controle não nulo quando κ≠0. A fonte é escalar e clássica no lado geométrico; não classifica matéria quântica geral.

## A correspondência com os estados reais

[INPUT / REAL] Reutiliza-se b:SummableAmplitude da 028:

    0 ≤ b_n ≤ 1/12,   B=Σ_n b_n < ∞,
    Q_t(n)=1/3−b_n t²/(1+t²),
    κ=amplitudeCoupling b=log(2) B/π.

Os vetores, estados fiéis, marginais e operadores modulares dessa família foram construídos nas 026–028. Aqui se usa amplitudeState, e não uma entropia definida a partir da área.

Para uma direção d, a frequência é ℓ=k(d). A resposta medida nos estados é

    lim S(ℓt)/t² = −log(2) B ℓ² = −π T(d,d).

[INPUT] Para η≠0, escolhemos

    r=2πκ/η,
    a=r/2+s,
    c=r/2−s,

com s real livre. Essa escolha é matchedLeft/matchedRight; ela fixa a soma dos coeficientes. Não é apresentada como uma lei dinâmica derivada do estado.

[REAL] O cálculo de Ricci implica η Ric(d,d)=2π T(d,d). Assim matched_wave_area demonstra

    lim_[t→0⁻] [S(ℓt)−η(A(t)−A(0))]/t² = 0

para toda EquilibriumScreenData da métrica, em qualquer ponto e direção nula. matchedScreen constrói efetivamente uma dessas telas por localEquilibriumScreen em cada direção nula não zero; matched_constructed_area aplica a prova a essa tela construída. Nenhuma hipótese harea é recebida por esses teoremas da família escolhida.

wave_heat_matching verifica a correspondência com o calor construído da fonte. matched_wave_einstein dá a identidade exata

    G=(2π/η)T,

com Λ=0. matched_wave_einstein_from_area instancia também o teorema geral da 028: sua hipótese harea é fornecida por matched_constructed_area, e não deixada para o chamador. Isso testa a composição inteira da cadeia anterior.

### O limite conjunto é de probabilidades lidas

[REAL] amplitudeReadWeights são expectativas dos projetores diagonais no estado global. wave_read_entropy_joint liga essas probabilidades ao limite da 028. O resultado mais forte, matched_read_area_joint, prova, para qualquer corte N(ξ)→∞ e tempo t(ξ)→0 pelo passado,

    [finiteEntropy(amplitudeReadWeights b (ℓ t(ξ)) N(ξ))
       −finiteEntropy(towerW referência N(ξ))
       −η(A(t(ξ))−A(0))] / t(ξ)² → 0.

Não é imposta relação entre a velocidade do corte e a do tempo. A identidade é sobre diferenças de entropias finitas e seus limites; não subtrai entropias infinitas. Ela não identifica o funcional diagonal ao funcional completo de Araki.

## Controles e informação que permanece livre

[REAL] Na origem, g=eta4 para todos os parâmetros. A direção de teste d=(1,1,0,0) é nula, não zero e satisfaz k(d)=1. wave_origin_area_iff demonstra a condição necessária e suficiente

    correspondência de área nessa tela ↔ η(a+c)=2πκ.

wave_wrong_trace_refused recusa coeficientes incompatíveis. zero_eta_nonzero_source_refused recusa η=0 com fonte não nula.

A condição η≠0 é essencial no teorema de área. A identidade algébrica matched_wave_einstein também é válida em η=0, pois a divisão em ℝ no Lean é total e o coeficiente fica zero. Essa instância degenerada não é usada como correspondência física; o controle de η=0 torna explícita essa distinção.

[REAL] Variar s mantém o tensor de Ricci e o tensor de matéria. A família amplitudeState b (ℓt) também permanece a mesma: s não entra em sua definição. As métricas coincidem na origem, mas

    R¹_(0 1 0)−R²_(0 2 0)=2s.

matched_curvature_distinguishes demonstra que s diferentes dão componentes diferentes no referencial especificado. state_alone_not_curvature_coordinate prova que não há uma função somente do estado fixado que devolva essa componente para todos os valores de s desta família.

Este é um resultado sobre a construção especificada e suas coordenadas. Não foi demonstrada uma classificação global por isometria, nem uma impossibilidade de reconstrução que disponha de dados geométricos ou de contorno adicionais.

Dois controles separam situações que não devem ser confundidas:

- Com b=zeroAmplitude, Ric=0; se s≠0, a curvatura é não nula. O estado é o de referência pela 028 e a resposta entrópica é zero. Portanto a presente família admite vácuo curvo.
- Com b=geometricAmplitude da 028, κ>0. geometric_wave_matter_nonzero prova matéria não nula. Para η≠0 e s=0, geometric_wave_curved prova curvatura não nula. A correspondência de área já vale para esse caso pelos teoremas gerais da família.

## Arquivos e reprodução

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| [PlaneWaveSolder.lean](<C:/IALD/Central de Patentes/Chatgpt/PlaneWaveSolder.lean>) | 12 | 4 |
| [PlaneWaveConnection.lean](<C:/IALD/Central de Patentes/Chatgpt/PlaneWaveConnection.lean>) | 5 | 1 |
| [PlaneWaveCurvature.lean](<C:/IALD/Central de Patentes/Chatgpt/PlaneWaveCurvature.lean>) | 10 | 0 |
| [PlaneWaveMatter.lean](<C:/IALD/Central de Patentes/Chatgpt/PlaneWaveMatter.lean>) | 10 | 2 |
| [PlaneWaveEntropyMatching.lean](<C:/IALD/Central de Patentes/Chatgpt/PlaneWaveEntropyMatching.lean>) | 11 | 4 |
| [PlaneWaveReconstructionControls.lean](<C:/IALD/Central de Patentes/Chatgpt/PlaneWaveReconstructionControls.lean>) | 16 | 1 |

O auditor, depois de publicada a entrega, funciona em modo somente leitura:

    & 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation029.py'

Ele confere hashes, bytes, versões compiladas, logs finais, cobertura dos axiomas e conteúdo da entrega. Não substitui a recompilação independente nem a revisão matemática da gerência. A recompilação deve ser feita em cópias, na ordem do manifesto. Os fontes locais e os oleans TGL/TGLExt copiados estão fixados; Lean 4.31.0/mathlib externos são resolvidos pelo wrapper. Não é um pacote integral portátil.

Alguns logs contêm sugestões informativas de táticas; não são tratados como novos teoremas. Somente os fontes finais e seus logs sem erros/avisos/sorryAx sustentam a entrega. Tentativas rejeitadas não foram apagadas.

## Alcance e próximos requisitos

[KNOWN] Ondas planas e sua liberdade transversal são clássicas. [David Tong, General Relativity, seção 5.2.3](https://davidtong.org/teaching/general-relativity/grhtml/S5) apresenta a família de Brinkmann e a condição de traço nulo no vácuo. [Harte e Drivas, Caustics and wave propagation in curved spacetimes](https://link.aps.org/accepted/10.1103/PhysRevD.85.124039), seção II, apresenta a curvatura e Ricci de pp-waves. A forma acima usa a convenção de sinal da bancada, conferida por cálculo. Não se reivindica descoberta dessas soluções clássicas; nenhum resultado externo foi acrescentado como axioma Lean.

[OPEN] O que se pagou é existência de correspondência entrópica em uma família curva com matéria, junto com um controle preciso da liberdade que sobra. A área não foi derivada para uma dinâmica microscópica geral. A escolha do ansatz, η, dimensão, assinatura, covetor e curva de estados continua INPUT. Seleção dos parâmetros geométricos e de dados radiativos, correlações, vínculo região–álgebra, identificação de Araki, temperatura/unidades físicas e reconstrução de matéria quântica geral permanecem abertos.

O próximo requisito substantivo é uma regra de acoplamento e evolução que determine os dados geométricos a partir da estrutura quântica e de condições de contorno explicitadas. Ajustar o coeficiente para obter correspondência não prova essa regra. A liberdade exibida pela 029 impede tratar a correspondência de Ricci como uma seleção completa da geometria.

Originais, um.py, kernel canônico, Atlas, memórias, diários, selos, gate e entregas anteriores permanecem intocados. Auditoria independente e incorporação cabem à gerência pelo túnel. O objetivo amplo permanece ativo e não alcançado.
