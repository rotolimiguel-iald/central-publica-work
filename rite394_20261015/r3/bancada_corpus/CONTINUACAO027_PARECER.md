[REAL / INPUT / OPEN] CONTINUAÇÃO 027 — equivalência unitária e transporte modular com domínios

06/09/2026. Para dois perfis produto positivos P,Q cuja afinidade infinita é positiva, foi construída uma unitaria U:H(Q)→H(P) que envia a referência de Q ao vetor Φ preparado no Hilbert original de P. Ela entrelaça todos os observáveis locais e transporta o fator completo. O Tomita do novo estado, sua conjugação antiunitária, o operador positivo auto-adjunto JS, seu quadrado Δ e o grupo modular foram identificados nesse mesmo H(P), com os domínios explícitos.

A etapa 026 é PROGRESSO, reconferida nesta sessão: 705 hashes, oito módulos, 83 teoremas e duas definições impressas, PASS. Esta etapa tem 8 módulos, 104 teoremas e 12 definições com axiomas impressos separadamente. As contagens incluem auxiliares e controles; não contam descobertas matemáticas. A auditoria independente da gerência está pendente.

## Hipóteses e enunciado

[INPUT] P e Q são SiteProfile: cada sítio binário tem pesos estritamente positivos e soma um. Escrevendo p_n e q_n para esses pares de pesos,

    c_n = Σ_i sqrt(p_n(i)) sqrt(q_n(i))
    C_N = ∏_(n=0)^N c_n
    C = lim_N C_N > 0.

A positividade de C é antecedente desta construção. A 026 demonstrou que ela equivale à convergência em norma da preparação canônica

    Ψ_N = π_P(diag sqrt(towerW(Q,N)/towerW(P,N))) Ω_P.

Seu limite Φ tem norma um, é cíclico e separante para M(P), e satisfaz

    ⟨Φ,π_P(a)Φ⟩ = tState(Q,N,a).

A escolha clássica em globalProfileVector escolhe um limite cuja existência já foi provada. Não introduz existência por axioma adicional. Nenhuma identificação entre as duas representações foi tomada como hipótese.

## A unitaria construída

[REAL] No quociente GNS de Q, define-se

    u₀([a]_Q) = π_P(a) Φ.

A compatibilidade dos empurrões torna essa aplicação bem definida, inclusive quando os representantes estão em andares distintos. A igualdade das marginais dá

    ⟨u₀([a]_Q),u₀([b]_Q)⟩ = ⟨[a]_Q,[b]_Q⟩.

Foram provadas aditividade, linearidade complexa e preservação da norma. A aplicação se estende por continuidade ao completamento H(Q). A imagem da extensão isométrica é fechada. Ela contém todos os filtros inversos locais G_LΦ da 026 e, portanto, seu limite Ω_P. Sua invariância por cada π_P(a), junto da densidade da órbita local de Ω_P, prova que a imagem é H(P) inteiro.

O resultado é profileGNSUnitary, uma LinearIsometryEquiv:

    U Ω_Q = Φ
    U π_Q(a) x = π_P(a) U x    para todo x∈H(Q).

Teoremas centrais: profile_gns_pre_inner, profile_gns_surjective e profile_gns_unitary_intertwines. A sobrejetividade não foi inferida apenas da preservação do produto interno.

## O fator completo e o Tomita real

[REAL] A conjugação C_U(B)=UBU⁻¹ é um StarAlgEquiv de operadores limitados. Primeiro se prova o transporte de cada álgebra local. Depois, star_equiv_centralizer_transport é aplicado duas vezes à definição do fator como bicomutante:

    B∈M(Q) ⇔ C_U(B)∈M(P).

A nova aplicação de Tomita é ligada ao gráfico efetivo de todo M(P):

    G_Φ = {(BΦ,B*Φ): B∈M(P)}
    G_Φ = (U×U)(G_Q)
    closure(G_Φ) = (U×U)(closure(G_Q)).

A última igualdade usa o homeomorfismo U×U. O domínio transportado coincide exatamente com

    D(S_Φ) = {x: existe y com (x,y)∈closure(G_Φ)}.

Foram demonstrados unicidade de y, densidade do domínio, fechamento do gráfico e

    S_Φ(BΦ) = B*Φ    para todo B∈M(P).

Portanto a fórmula S_Φ=US_QU⁻¹ foi identificada com o fecho do Tomita do novo vetor no fator original. Não se limitou a dar esse nome a um operador transportado.

## Adjunto completo, positividade e quadrado

[REAL] O módulo UnitaryPartialTransport trata operadores parciais lineares sobre Hilberts complexos. Para uma unitaria e e um operador T, o transporte T' tem

    D(T') = {x: e⁻¹x∈D(T)}
    T'x = e T e⁻¹x.

O kernel prova a correspondência exata dos grafos, densidade do domínio, fechamento e positividade. A prova de auto-adjunticidade inclui a inclusão inteira do gráfico de (T')* no de T'. A identidade fraca de adjunto é puxada para T, cuja auto-adjunticidade devolve pertencimento ao domínio original. A simetria fornece a outra inclusão. Isso prova (T')*=T', inclusive o domínio.

Aplicado aos operadores canônicos de Q:

    J_Φ = U J_Q U⁻¹
    A_Φ = U (J_Q S_Q) U⁻¹
    Δ_Φ = U Δ_Q U⁻¹.

J_Φ é uma equivalência antiunitária involutiva e fixa Φ. Foram provadas

    J_Φ S_Φ = A_Φ
    S_Φ = J_Φ A_Φ
    A_Φ*=A_Φ
    Re ⟨x,A_Φx⟩ ≥ 0    para todo x∈D(A_Φ).

Δ_Φ também é positivo e auto-adjunto. As duas afirmações de quadrado são separadamente verificadas:

    D(Δ_Φ) = {x∈D(A_Φ): A_Φx∈D(A_Φ)}
    Δ_Φx = A_Φ(A_Φx)    para todo x∈D(Δ_Φ).

Esse é o sentido preciso em que A_Φ realiza a raiz quadrada positiva de Δ_Φ nesta entrega. Não foi acrescentado um cálculo funcional abstrato geral para operadores não limitados, nem um novo teorema independente de unicidade de raízes.

As ações locais também foram transportadas:

    A_Φ π_P(a)Φ = π_P(towerDeltaHalfLevel(Q,N,a))Φ
    Δ_Φ π_P(a)Φ = π_P(towerDeltaLevel(Q,N,a))Φ.

Essas fórmulas incluem a prova de que os vetores pertencem aos respectivos domínios.

## Grupo modular e controle espectral

[REAL] Define-se V_Φ(t)=U V_Q(t) U⁻¹. O kernel verifica unitariedade, continuidade forte em t, lei de grupo, valor identidade em zero e V_Φ(t)Φ=Φ. A conjugação correspondente preserva M(P) e o estado vetorial ω_Φ.

Para cada observável local,

    V_Φ(t) π_P(a) V_Φ(t)⁻¹ = π_P(flowLevel(Q,t,N,a)).

Transportando os autovetores locais v_(N,i,j) de Q, obtém-se

    Δ_Φ Uv = λ Uv
    V_Φ(t) Uv = exp(i t log λ) Uv
    λ = towerW(Q,N,i)/towerW(Q,N,j) > 0.

profile_flow_spectral_unique prova que qualquer operador limitado que tenha essa ação na família total transportada coincide com V_Φ(t) em todo H(P). A totalidade e a unicidade do grupo espectral canônico são reutilizadas das provas anteriores.

## Controles exatos

[REAL] Para Q=P, os filtros são identidade e Ψ_N=Ω_P. A unicidade do limite dá Φ=Ω_P; a densidade prova U=identidade em todo H(P). Consequentemente a conjugação do fator, J e o grupo modular recuperam os objetos canônicos.

O exemplo não trivial é o perfil da 026:

    P.w(n) = 1/3
    Q.w(n) = 1/3 + 1/[12(n+1)].

A 026 demonstrou C(P,Q)>0, mudança em todos os sítios, diferenças não somáveis mas quadrados somáveis e estado diferente da referência. Aqui se prova Φ≠Ω_P e

    V_P(t)Ω_P ≠ Φ    para todo t real,

pois o fluxo modular antigo fixa Ω_P. Uma mudança de perfil não foi confundida com uma órbita desse fluxo.

No primeiro sítio, os valores exatos são

    λ_P(0,0,1) = 1/2
    λ_Q(0,0,1) = 5/7.

O novo Δ e o novo fluxo realizam respectivamente o fator 5/7 e a fase exp(i t log(5/7)) no autovetor transportado. Essas razões foram calculadas em Lean a partir das definições dos pesos.

## Evidência e reprodução

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| [ProfileGNSPre.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileGNSPre.lean>) | 7 | 2 |
| [ProfileGNSUnitary.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileGNSUnitary.lean>) | 15 | 2 |
| [ProfileFactorTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileFactorTransport.lean>) | 8 | 1 |
| [UnitaryPartialTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/UnitaryPartialTransport.lean>) | 13 | 1 |
| [ProfileTomitaTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileTomitaTransport.lean>) | 12 | 1 |
| [ProfileModularTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileModularTransport.lean>) | 19 | 3 |
| [ProfileFlowTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileFlowTransport.lean>) | 15 | 2 |
| [ProfileTransportControls.lean](<C:/IALD/Central de Patentes/Chatgpt/ProfileTransportControls.lean>) | 15 | 0 |

Cada fonte final tem compilação com exit 0, hash estável e zero erros, avisos ou sorryAx. Todas as dependências axiomáticas impressas pertencem a propext, Classical.choice e Quot.sound. Definições auxiliares não impressas separadamente estão identificadas no manifesto; elas não entram na contagem de definições impressas.

Foram preservadas 9 tentativas rejeitadas, com suas versões de fonte recuperáveis pelos backups exatos dos bytes. Uma delas é uma interrupção deliberada de ProfileFlowTransport após o processo exceder 15 GB de memória: o wrapper registrou exit -1 e fonte estável, mas nenhum log de saída existia. O arquivo desse registro começa com BENCH INTERRUPTION RECORD e declara expressamente ser uma nota da bancada, não saída do Lean. A prova foi reformulada por extensionalidade e a compilação seguinte passou com um limite menor de elaboração. As demais rejeições contêm a saída efetiva do compilador. Nenhuma tentativa rejeitada sustenta a conclusão.

O auditor desta etapa verifica, por padrão, apenas leitura:

    & 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation027.py'

A recompilação independente deve ocorrer em cópias e seguir a ordem de módulos do manifesto. Fontes locais e oleans TGL/TGLExt da bancada estão fixados por hashes; Lean 4.31.0 e mathlib externos são resolvidos pelo wrapper existente. O pacote não pretende incluir todas as dependências externas de modo portátil.

A entrega no túnel é C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_027_ESPONTANEA_transporte_unitario_e_modular.md. Ela inclui critérios, axiomas impressos, hashes lidos dos artefatos e as tentativas rejeitadas.

[KNOWN] A teoria de estados produtos e afinidades tem antecedentes clássicos, entre eles [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf). A entrega formaliza esta construção concreta; não reivindica a descoberta da teoria geral.

## O que permanece aberto

[OPEN] C>0 é suficiente para a equivalência unitária construída. Não foi demonstrada aqui sua necessidade para toda equivalência de representações, nem disjunção geral quando C=0. O estatuto de continuidade do estado herdado da 026 é SeqWOTContinuous; não se afirma uma formalização geral do predual ou de normalidade por todas as redes.

[INPUT / OPEN] P e Q continuam perfis produto fornecidos. A construção não seleciona uma fonte por dinâmica física, não produz correlações entre sítios, não constrói uma translação de energia positiva e não fornece nova inclusão modular meio-lateral.

[OPEN] Não se demonstraram regularidade temporal de um caminho de estados, resposta gravitacional global finita, lei de área, temperatura física ou casamento entre a matéria microscópica e o tensor de energia. Métrica lorentziana suave, dimensão, referencial, conservação e relação de Clausius permanecem antecedentes ou lacunas da reconstrução geométrica condicional. H3 e a reconstrução gravitacional geral não foram pagas por uma mudança de representação.

Originais, um.py, kernel canônico, Atlas, memórias, diários, selos e entregas anteriores permanecem intocados. A bancada não muda o gate. O objetivo amplo de gravidade quântica permanece aberto; auditoria independente e incorporação pertencem à gerência.
