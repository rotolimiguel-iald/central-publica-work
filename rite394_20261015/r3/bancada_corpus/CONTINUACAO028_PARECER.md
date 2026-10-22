[REAL / INPUT / OPEN] CONTINUAÇÃO 028 — resposta termodinâmica global e limite conjunto do corte

06/09/2026. Foi construída uma família de estados fiéis no Hilbert original, com perturbação em infinitos sítios e incrementos termodinâmicos finitos, sem depender de um corte fixo. Foi demonstrado o limite conjunto de corte e tempo para essa resposta. Em paralelo, o perfil harmônico anterior fornece um contraexemplo à inferência de finitude apenas a partir da equivalência unitária.

A etapa 027 é PROGRESSO: seu auditor foi novamente executado e verificou 724 hashes, oito módulos, 104 teoremas e 12 definições impressas. A etapa 028 reúne 8 módulos, 112 teoremas e 6 definições com axiomas impressos separadamente. As contagens incluem auxiliares e controles. A auditoria independente da gerência está pendente.

## O problema corrigido

[REAL] A 027 prova que C(P,Q)>0 fornece uma unitaria entre as representações e transporta o Tomita e os operadores modulares para o novo estado no mesmo Hilbert. Isso não implica que os incrementos termodinâmicos obtidos ao aumentar o corte sejam finitos.

Defina, nos pesos efetivos p_N=towerW(P,N), q_N=towerW(Q,N):

    D_N = Σ_i q_N(i)[log q_N(i)−log p_N(i)]
    K_N = Σ_i [q_N(i)−p_N(i)][−log p_N(i)]
    S_N = finiteEntropy(q_N)−finiteEntropy(p_N).

K_N é um incremento de expectativa de um observável local. Não é identificado ao operador −log Δ global.

[REAL] As quantidades satisfazem S_N=K_N−D_N. A aditividade dos produtos dá D_N e K_N como somas das respectivas contribuições dos sítios 0 a N. Usando log x≤x−1, foram provados, para pesos positivos normalizados,

    0 ≤ D(q||p) ≤ Σ_i (q_i−p_i)²/p_i.

Na referência binária p=(1/3,2/3),

    ΔK(q,p) = (q₀−1/3) log 2
    0 ≤ D(q||p) ≤ (9/2)(q₀−1/3)².

O sinal da primeira fórmula foi conferido: −log(1/3)+log(2/3)=log 2.

## O contraexemplo harmônico

[REAL] Para o perfil de 026,

    P.w(n)=1/3
    Q.w(n)=1/3+1/[12(n+1)],

a soma dos quadrados das diferenças é finita e a soma das diferenças é infinita. Logo

    D_N → D_finito
    K_N = log 2 Σ_(n≤N) 1/[12(n+1)] → +∞
    S_N = K_N−D_N → +∞.

As três conclusões foram verificadas em Lean. Também foram provadas a inexistência de limite real finito de K_N e de S_N e a falsidade da afirmação universal de que C>0 bastaria para tal limite.

Esse é o mesmo perfil cujo vetor, fidelidade, ciclicidade, separância, equivalência unitária e transporte modular foram construídos nas 026–027. Assim, a obstrução não resulta de uma falha de existência da representação. A entropia relativa de prefixo convergente também não garante que cada termo da identidade S_N=K_N−D_N tenha limite finito.

## Uma família com resposta finita

[INPUT] Fixe a referência P.w(n)=1/3. SummableAmplitude contém uma sequência b_n, as provas de 0≤b_n≤1/12 e a prova de sua somabilidade. Escreva

    B = Σ_n b_n
    B₂ = Σ_n b_n²
    h(t) = t²/(1+t²)
    Q_t.w(n) = 1/3−b_n h(t).

B₂ é finito, demonstradamente. Como 0≤h(t)<1, cada Q_t é um perfil positivo válido para todo t real. O sentido negativo foi escolhido para obter incremento modular negativo e acoplamento escalar positivo na convenção do calor das etapas anteriores. Essa escolha não foi derivada de uma dinâmica física.

[REAL] A soma dos quadrados das diferenças entre Q_t e P é finita; a estimativa de afinidade da 026 dá C(P,Q_t)>0 para todo t. Portanto há

    Φ_t ∈ H(P), ||Φ_t||=1
    ω_t(A)=⟨Φ_t,AΦ_t⟩
    ω_t(π_P(a))=tState(Q_t,N,a).

O estado é fiel no fator original. A unitaria da 027 envia Ω_(Q_t) a Φ_t. O pacote é válido para todo parâmetro real.

Os pesos q_N(t) são lidos como valores reais de ω_t nos projetores diagonais locais. amplitude_read_modular_increment identifica K_N(t) com a diferença das expectativas efetivas do gerador local diagonal. amplitude_read_entropy_tendsto identifica o limite entrópico abaixo com as diferenças das entropias desses pesos lidos, não com uma nova quantidade sem ligação aos estados.

## Os limites globais

[REAL] Quando N→∞, para cada t fixo,

    K_N(t) → K(t) = −log 2 · B · h(t)
    D_N(t) → D(t) = Σ_n D(Q_t(n)||P(n))
    S_N(t) → S(t) = K(t)−D(t).

Os três limites são reais finitos. A soma que define D(t) tem sua convergência provada; não se usa o valor convencional de tsum em uma série divergente.

S(t) é o limite das diferenças de entropias finitas. Não se define subtraindo duas entropias infinitas e tratando o resultado como número real. Também não se identifica aqui D(t) ao funcional completo de entropia relativa de Araki.

A estimativa central, válida também para cada D_N, é

    0 ≤ D_N(t) ≤ D(t) ≤ (9/2) h(t)² B₂.

Os teoremas amplitude_modular_tendsto, amplitude_relative_tendsto e amplitude_entropy_tendsto provam os limites; amplitude_prefix_relative_bound fornece a cota uniforme.

## Limite temporal e limite conjunto

[INPUT] Para uma frequência real ℓ, considera-se Q_(ℓt). O parâmetro escolhido é h(ℓt), que chega a zero por valores não negativos mesmo quando t chega pelo passado.

[REAL] Para t≠0,

    h(ℓt)/t² = ℓ²/[1+(ℓt)²].

Além disso, para todo N e t,

    0 ≤ D_N(ℓt)/t² ≤ (9/2) ℓ⁴ t² B₂,

com a mesma cota para D(ℓt)/t². A fórmula inclui o valor convencional de divisão por zero em Lean; todos os limites de resposta não nula exigem explicitamente tempo eventualmente diferente de zero.

Consequentemente,

    K(ℓt)/t² → −ℓ² log 2 B
    S(ℓt)/t² → −ℓ² log 2 B
    D(ℓt)/t² → 0.

[REAL] A prova vai além de duas ordens separadas de limite. Para qualquer filtro e quaisquer funções N(ξ), t(ξ) tais que N(ξ)→∞, t(ξ)→0 e t(ξ)≠0 eventualmente,

    K_(N(ξ))(ℓt(ξ))/t(ξ)² → −ℓ² log 2 B
    S_(N(ξ))(ℓt(ξ))/t(ξ)² → −ℓ² log 2 B
    D_(N(ξ))(ℓt(ξ))/t(ξ)² → 0.

Não se impõe uma relação entre as velocidades de crescimento do corte e aproximação do tempo. amplitude_prefix_modular_joint e amplitude_prefix_entropy_joint contêm esses quantificadores; a estimativa do resto vale até sem exigir N→∞.

Esses são limites da resposta escalar lida dos estados. Não constituem, por si, prova de derivada segunda em norma de Φ_t ou de continuidade em norma da família de unitarias U_t.

## A ligação gravitacional e sua hipótese restante

[INPUT / REAL] Tome b constante em relação ao ponto geométrico x e defina o acoplamento

    κ = (log 2) B/π ≥ 0
    T = κ [w⊗w − gInv(w,w) g/2].

A conservação desse tensor reutiliza a prova anterior, sob covetor fechado e equação de onda. κ é uma normalização escolhida para o casamento com o calor; não é uma constante de Newton medida.

Em uma direção nula d, com ℓ=w(d),

    −ℓ² log 2 B = −π T(d,d).

[REAL] A resposta modular corresponde ao calor temporal construído a partir dessa fonte. A área é calculada independentemente, a partir da métrica e da tela geométrica. O coeficiente do seu defeito é

    lim_[t→0⁻] [S(ℓt)−η(A(t)−A(0))]/t²
      = −ℓ² log 2 B + η Ric(d,d)/2.

A anulação desse defeito equivale a

    η Ric(d,d) = 2π T(d,d).

Essa equivalência foi provada, não tomada como prova da lei de área. Sob a anulação para todas as telas locais, os coeficientes não nulos, solda suave inversível, covetor fechado, equação de onda e domínio aberto preconexo declarados no enunciado, foi verificado

    ∃ Λ constante: G + Λg = (2π/η)T.

O teorema é einstein_from_summable_area_matching. A hipótese harea permanece explícita. A identidade S=K−D e D/t²→0 permitem compor os casamentos de calor e área no resíduo de Clausius, mas não fornecem harea automaticamente.

## Controles

[REAL] O exemplo em infinitos sítios é

    b_n = (1/24)(1/2)^n
    B = 1/12
    B₂ = 1/432
    κ = log 2/(12π) > 0.

As duas somas foram calculadas em Lean. Para todo parâmetro não nulo, todos os sítios mudam e o estado global difere da referência. O limite conjunto é instanciado com o coeficiente −ℓ² log 2/12.

[REAL] Com amplitudes identicamente zero, Q_t=P, o estado é exatamente ω_P para todos os parâmetros e a resposta entrópica é zero.

[REAL] Em espaço plano, com covetor temporal constante e o exemplo geométrico não nulo, o tensor é suave e conservado, e a correspondência de calor vale. A correspondência de área falha para toda η, pois Ric=0 e T(d,d)=κ>0 na direção de controle. geometric_flat_area_not_matching usa a nova família global; não se limita a citar o controle finito de 024.

## Verificação

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| [RelativeEntropyProductBounds.lean](<C:/IALD/Central de Patentes/Chatgpt/RelativeEntropyProductBounds.lean>) | 10 | 0 |
| [ProfileEntropyLimits.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileEntropyLimits.lean>) | 15 | 0 |
| [HarmonicEnergyObstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/HarmonicEnergyObstruction.lean>) | 10 | 0 |
| [SummableProfileCurve.lean](<C:/IALD/Central de Patentes/Chatgpt/SummableProfileCurve.lean>) | 18 | 4 |
| [SummableStateThermodynamics.lean](<C:/IALD/Central de Patentes/Chatgpt/SummableStateThermodynamics.lean>) | 18 | 0 |
| [UniformQuadraticResponse.lean](<C:/IALD/Central de Patentes/Chatgpt/UniformQuadraticResponse.lean>) | 15 | 0 |
| [SummableGravityBridge.lean](<C:/IALD/Central de Patentes/Chatgpt/SummableGravityBridge.lean>) | 8 | 0 |
| [SummableGravityControls.lean](<C:/IALD/Central de Patentes/Chatgpt/SummableGravityControls.lean>) | 18 | 2 |

Todos os fontes finais têm exit 0, hash estável e zero erros, avisos ou sorryAx nas compilações finais. As dependências axiomáticas impressas pertencem apenas a propext, Classical.choice e Quot.sound. As 6 tentativas rejeitadas foram preservadas com seus logs e fontes recuperáveis nos backups exatos dos bytes. Definições auxiliares não impressas separadamente são identificadas no manifesto.

A custódia é conferida em modo somente leitura por:

    & 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation028.py'

A recompilação independente deve ocorrer em cópias, na ordem do manifesto. Os fontes locais e oleans TGL/TGLExt da bancada estão fixados por hashes; Lean 4.31.0 e mathlib externos são resolvidos pelo wrapper e não constituem um pacote integral portátil.

A entrega é C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_028_ESPONTANEA_resposta_global_e_limite_do_corte.md.

## Alcance e referências

[KNOWN] [Casini, Relative entropy and the Bekenstein bound](https://arxiv.org/abs/0804.2182) trata estados reduzidos e uma formulação do limite em espaço plano. [Jacobson, Entanglement Equilibrium and the Einstein Equation](https://arxiv.org/abs/1505.04753) relaciona Einstein a uma hipótese de equilíbrio, com resultado preciso de primeira ordem para campos conformes e condição adicional no caso não conforme. Esses artigos contextualizam a questão; nenhum resultado deles foi acrescentado como axioma Lean.

[OPEN] A finitude obtida vale para a classe somável e para os funcionais de prefixo especificados. A identificação completa com entropia de Araki, uma dinâmica física que selecione a curva, correlações, vínculo entre regiões e álgebras, lei microscópica de área, temperatura, unidades, origem da dimensão e assinatura permanecem abertos ou assumidos. A fonte construída é do tipo escalar e não classifica toda matéria quântica.

A etapa elimina a divergência de corte para uma família global não trivial e demonstra a resposta conjunta. Não resolve a origem microscópica de H3 nem a reconstrução gravitacional geral. O objetivo amplo permanece ativo e não alcançado.

Originais, um.py, kernel canônico, Atlas, memórias, diários, selos, gate e entregas anteriores permanecem intocados. Pelo protocolo do túnel, a gerência audita independentemente e incorpora.
