[REAL / INPUT / OPEN] CONTINUAÇÃO 026 — afinidade, limite global e estado fiel no Hilbert original

06/09/2026. O resultado central desta etapa é um critério exato para a convergência da preparação produto no espaço de Hilbert original. Sob esse critério, a bancada constrói um vetor unitário, cíclico e separante, cujo estado é fiel no fator original e tem todas as marginais do perfil de destino. Um exemplo muda todos os sítios e permanece nesse mesmo espaço.

A etapa 025 é PROGRESSO: seu auditor foi reexecutado nesta sessão e conferiu 675 hashes, sete módulos, 72 teoremas e uma definição impressa. A entrega 026 contém 8 módulos novos, 83 teoremas e 2 definições com axiomas impressos separadamente. A contagem inclui auxiliares e controles; não é contagem de novas descobertas matemáticas. A auditoria independente da gerência permanece pendente.

## Enunciado e hipóteses

[INPUT] P e Q são dois SiteProfile: em cada sítio binário n, o primeiro peso pertence estritamente a (0,1), e o segundo é seu complemento. Não se postula uma identificação prévia entre H(P) e H(Q). N=0 já contém um sítio.

Para os pesos de produto p_N=towerW(P,N), q_N=towerW(Q,N), definimos no H(P) original:

    F_N = diag sqrt(q_N / p_N)
    Ψ_N = π_P(F_N) Ω_P
    c_n = Σ_i sqrt(p_n(i)) sqrt(q_n(i))
    C_N = ∏_(n=0)^N c_n
    C   = inf_N C_N = lim_(N→∞) C_N.

[REAL] Cada filtro F_N é positivo definido e auto-adjunto, com inverso diag sqrt(p_N/q_N). O vetor Ψ_N tem norma um. Para a no andar L e N≥L,

    ⟨Ψ_N, π_P(a) Ψ_N⟩ = tState(Q,L,a).

A igualdade se refere ao mesmo observável π_P(a) no mesmo H(P), mesmo quando N cresce. Os enunciados estão em relative_filter_positive, relative_filter_reverse, profile_vector_norm e profile_state_marginal.

## O critério exato de convergência

[REAL] 0<c_n≤1, C_N>0, e a sequência C_N é decrescente. Para quaisquer L≤N,

    ⟨Ψ_L, Ψ_N⟩ = C_N/C_L
    ||Ψ_L−Ψ_N||² = 2(1−C_N/C_L).

A segunda igualdade é calculada a partir do produto interno efetivo do Hilbert; não é uma distância introduzida por definição. Daí:

    (Ψ_N é Cauchy) ⇔ (existe limite em norma de Ψ_N em H(P)) ⇔ C>0.

Suficiência: C_N≥C e C/C_L→1, portanto todas as distâncias na cauda são controladas por 2(1−C/C_L). Necessidade: uma cauda de Cauchy com distância menor que um obriga C_N>C_L/2 para um L fixo e todos N≥L; passando ao limite, C≥C_L/2>0.

Os teoremas principais são profile_vectors_overlap, profile_vectors_distance, profile_vectors_cauchy_iff e profile_vectors_limit_iff. Se C=0, profile_zero_affinity_no_limit recusa o limite em norma a qualquer vetor de H(P).

O quantificador negativo concerne à sequência Ψ_N especificada. Ele não foi substituído por uma afirmação sobre todos os possíveis estados normais com as mesmas marginais.

## O estado global e a prova de fidelidade

[REAL] Para C>0, globalProfileVector(P,Q,hpos) escolhe o limite cuja existência foi demonstrada. A escolha clássica não acrescenta uma hipótese de existência. Escrevendo Φ para esse vetor,

    ||Φ|| = 1
    ω_Φ(A) = ⟨Φ,AΦ⟩
    ω_Φ(π_P(a)) = tState(Q,L,a).

O estado é complexo-linear, positivo e normalizado. O kernel prova SeqWOTContinuous para esse funcional vetorial. Não foi formalizada aqui uma equivalência geral entre normalidade, predual e preservação de supremos por redes.

A fidelidade exige um argumento adicional; ela não foi inferida de um limite de estados fiéis. Para cada L, defina o operador limitado local

    G_L = π_P(diag sqrt(p_L/q_L)).

Usando as marginais do vetor limite e a fórmula das sobreposições, foram provados:

    ||G_L Φ|| = 1
    ⟨Ω_P,G_L Φ⟩ = C/C_L
    ||Ω_P−G_L Φ||² = 2(1−C/C_L)
    G_L Φ → Ω_P em norma.

Cada G_L é limitado; não se supõe uma cota uniforme para seus operadores nem um inverso global limitado. A ação direita da mesma diagonal coincide com G_L no vetor Φ, por comutação das diagonais finitas e passagem ao limite. Toda ação direita comuta com o fator original.

Assim, para A∈M(P), AΦ=0 implica A G_L Φ=0 para cada L; o limite dá AΩ_P=0. A separância canônica de Ω_P implica A=0. Portanto Φ é separante e ω_Φ é fiel no fator original. Teoremas: global_profile_right_left, global_profile_inverse_tendsto, global_profile_vector_separating e global_profile_state_faithful.

[REAL] A mesma recuperação prova ciclicidade. Ω_P está no fecho de M(P)Φ; aplicando cada operador local a essa aproximação, toda a órbita local de Ω_P está nesse fecho. A densidade da torre dá closure(M(P)Φ)=H(P). Esse corolário está em global_profile_vector_cyclic.

## Um exemplo que modifica infinitos sítios

[REAL] Foi demonstrada a condição suficiente

    Σ_n (1−c_n) < ∞  ⇒  C>0.

A prova controla a perda de produto na cauda pela soma das perdas dos sítios; não usa como axioma um teorema de produtos infinitos. A necessidade dessa condição escrita como série não é uma conclusão desta entrega.

Para pesos binários p,q∈(0,1), a estimativa formalizada é

    1−c(p,q) ≤ (p−q)² [1/(2p) + 1/(2(1−p))].

Em particular, para p=1/3, o fator da direita é 9/4. Isso permite o exemplo explícito:

    P.w(n) = 1/3
    Q.w(n) = 1/3 + 1/[12(n+1)].

gradualProfile prova que Q é um perfil válido. gradual_profile_changes_every_site prova Q.w(n)≠P.w(n) para todo n. As diferenças de primeira ordem não são somáveis; seus quadrados são somáveis. Esses dois fatos são demonstrados em gradual_profile_diff_not_summable e gradual_profile_square_summable.

Consequentemente, C>0 e há um estado fiel com marginais Q no H(P) original. gradual_state_not_reference prova que ele difere do estado original, usando um observável do andar zero; gradual_state_local fornece todos os valores locais. A ciclicidade segue do teorema geral. O exemplo é escolhido matematicamente, não selecionado por dinâmica física.

## Controles e ligação com a etapa térmica

[REAL] Se Q=P, C=1. Para P.w(n)=1/3 e Q.w(n)=1/2 constantes, a afinidade por sítio é estritamente menor que um, C_N=c^(N+1)→0 e a preparação não converge em norma. Os controles são profile_affinity_limit_self e stationary_changed_no_preparation_limit.

[REAL] A ligação com a família de 024/025 é explícita:

    profileVector(P, thermalProfile(P,s), N) = towerGibbsVector(P,N,s).

Logo thermal_preparation_limit_iff aplica o critério exato à preparação térmica já existente. Não se confunde igualdade de fórmulas semelhantes com igualdade entre os objetos: a identidade foi provada no kernel.

[KNOWN] Afinidades e estados produtos infinitos fazem parte da teoria clássica de [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf). O resultado geral do artigo tem hipóteses e noções próprias. Esta etapa verifica uma preparação concreta no kernel da casa; não reivindica a descoberta da teoria de Kakutani/Bures nem importa o artigo como axioma.

## Verificação e reprodução

Todos os fontes finais têm compilação com exit 0, fonte estável, zero erros, zero avisos e ausência de sorryAx. Cada teorema declarado possui #print axioms; as únicas dependências axiomáticas impressas são propext, Classical.choice e Quot.sound. Os hashes e as contagens são calculados dos arquivos pelo auditor.

Foram preservadas 8 tentativas rejeitadas, com cópias exatas dos logs e backups dos bytes de todos os fontes históricos compilados. Erros de elaboração e avisos não são contabilizados como provas finais.

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| [RelativeProfilePreparation.lean](<C:/IALD/Central de Patentes/Chatgpt/RelativeProfilePreparation.lean>) | 12 | 0 |
| [ProfileOverlapFactorization.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileOverlapFactorization.lean>) | 14 | 0 |
| [AffinityProducts.lean](<C:/IALD/Central de Patentes/Chatgpt/AffinityProducts.lean>) | 9 | 0 |
| [AffinityVectorCriterion.lean](<C:/IALD/Central de Patentes/Chatgpt/AffinityVectorCriterion.lean>) | 6 | 0 |
| [GlobalProfileState.lean](<C:/IALD/Central de Patentes/Chatgpt/GlobalProfileState.lean>) | 11 | 1 |
| [GlobalProfileFaithfulness.lean](<C:/IALD/Central de Patentes/Chatgpt/GlobalProfileFaithfulness.lean>) | 9 | 0 |
| [ProfileAffinityBound.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileAffinityBound.lean>) | 5 | 0 |
| [GlobalProfileControls.lean](<C:/IALD/Central de Patentes/Chatgpt/GlobalProfileControls.lean>) | 17 | 1 |

O comando somente leitura para conferir a custódia é:

    & 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation026.py'

O manifesto registra os caminhos absolutos, tamanhos, hashes, ordem de dependências, saídas de axiomas e todas as tentativas. A recompilação independente deve ocorrer em cópia, na ordem dos módulos acima, usando o mesmo Lean e dependências resolvidos por verify_stage.ps1. Os fontes locais e oleans copiados de TGL/TGLExt estão fixados; a distribuição externa de Lean/mathlib não constitui aqui um pacote integral portátil.

## A parede que permanece

[OPEN] Esta construção remove a dúvida sobre existência de uma realização fiel e cíclica no Hilbert original quando C>0. Ainda não constrói explicitamente uma unitária H(Q)→H(P) que entrelace as representações, nem transporta S, J, Δ e o fluxo modular do novo estado por essa unitária.

[OPEN] Não foram demonstrados classificação de todos os estados normais, disjunção ou quase-equivalência geral. O regime continua sendo produto; correlações físicas não foram construídas. A nova preparação tampouco fornece automaticamente uma curva temporal duas vezes diferenciável, entropia infinita finita ou resposta gravitacional global.

[INPUT / OPEN] H3, relação entropia-área, dimensão, assinatura, solda, temperatura, unidades e seleção da fonte continuam antecedentes ou lacunas. Os controles geométricos de 024/025 não são alterados: existência de um estado fiel não paga a equação de área nem transforma calor compatível em reconstrução gravitacional geral.

O próximo passo matemático concreto é construir o entrelaçamento das representações a partir da igualdade dos produtos internos locais e transportar os operadores modulares, com seus domínios. Depois disso, a regularidade de famílias globais e a relação geométrica ainda exigirão provas próprias.

A entrega 026 representa PROGRESSO no objetivo amplo, que permanece não alcançado. Escrita somente na bancada Chatgpt; originais, um.py, kernel canônico, Atlas, memórias, diários, gate e entregas anteriores intocados. Incorporação, atualização das superfícies canônicas e auditoria adversarial independente cabem à gerência.
