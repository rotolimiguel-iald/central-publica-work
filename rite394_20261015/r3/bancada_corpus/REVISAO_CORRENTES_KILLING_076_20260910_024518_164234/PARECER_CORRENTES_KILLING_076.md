# Parecer independente do levantamento BRST das correntes de Killing — 076

10/09/2026. [DERIVED — revisão escrita delimitada]. **Não identifiquei erro material na construção dos seis representantes de ghost3.** O sinal positivo do termo de antifield, a identidade de Noether e a orientação dos polinômios Grassmann fecham o cancelamento off-shell. Isto não afirma seis classes independentes nem uma classificação de H³.

Fonte lida integralmente, com linhas: [LEVANTAMENTO_BRST_CORRENTES_KILLING_076.md](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/LEVANTAMENTO_BRST_CORRENTES_KILLING_076.md>). Pin medido antes da escrita: **12057 bytes; SHA-256 532a93096eaf8cbe4aae9dfaeaa42b9bb3db05bb404eed63040981af604d1590**. Este parecer é separado da [revisão do setor K e da homotopia do alvo](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_MODULOS_EBAR_076_20260910_024011_189592/PARECER_MODULOS_EBAR_076.md>).

## 1. Ação, corrente e densidade

Conferi a ação(1) com a [convenção física067](<C:/IALD/Central de Patentes/Chatgpt/CONVENCAO_ACAO_ESTADO_LOCAL_20260909_214710_215498/CONVENCAO_SINAL_E_TRANSPORTE.md>) e a equação1 da [CME071](<C:/IALD/Central de Patentes/Chatgpt/CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910/CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md>): o termo sigma é +c_σ Q/2 na assinatura +---. Sua derivada de Euler intrínseca é

\[
 \mathcal E_i=-c_\sigma v_g h_{ij}\tau^j.
\]

Para X Killing, a variação rígida da densidade da ação é zero. O potencial de fronteira dessa variação é a corrente vetorial densitizada

\[
 \mathcal J_X^\mu=c_\sigma v_g h_{ij}X^i\nabla^\mu\phi^j.
\]

Portanto ∂_μ𝒥_X^μ=−𝔈_iX^i. A mesma identidade sai diretamente da divergência: a parcela com ∇_(iX_j) se anula e sobra c_σv_g h(X,τ). Não se empregou a equação Einstein nem κc_σ=4.

A fonte φ_i* e 𝔈_i são ambas densidades de peso1. O pareamento BV usa d⁴x φ_i*sφ^i, sem uma segunda multiplicação por v_g. Já j_X é vetor e 𝒥_X=v_gj_X é vetor densidade. Essa separação foi mantida em toda a prova. Se a fonte for trocada por φ̂*=φ*/v_g, a expressão inteira deve ser convertida, como a nota indica.

## 2. Sinal BV e identidade Grassmann

No bloco de fontes Σ=S+∫φ_i*c^μ∂_μφ^i, as duas fontes ímpares são ordenadas exatamente como nas linhas33–63. A derivada direita em φ* é −c·∂φ. A derivada em φ, par, dá

\[
 -\partial_\mu(\phi_i^*c^\mu)
 =+\partial_\mu(c^\mu\phi_i^*).
\]

Com sφ=−δ_RΣ/δφ* e sφ*=+δ_RΣ/δφ, resulta sφ*=𝔈+Lie_cφ*. Conferi a convenção em [Fröb, equações104,110 e140](https://arxiv.org/pdf/1803.10235v3). A equação140 aparece no contexto de operadores quadráticos da teoria livre, mas o sinal nos geradores é o da definição do antibracket; aqui só se usa essa identidade algébrica, sem importar o teorema quântico para um gerador não linear.

A definição η_μ=∂_Lη/∂c^μ, com η=c⁰c¹c²c³, dá η₀=c¹c²c³, η₁=−c⁰c²c³, η₂=c⁰c¹c³, η₃=−c⁰c¹c². Assim c^νη_μ=δ^ν_μη. A aplicação direta de sc=c·∂c fornece

\[
 s\eta=-\eta\,\partial_\nu c^\nu,\qquad
 s\eta_\mu=(\partial_\mu c^\nu)\eta_\nu
              -(\partial_\nu c^\nu)\eta_\mu.
\]

Para 𝒥 par de tipo vetor densidade, a parcela vetorial e o peso cancelam os respectivos termos de sη_μ. Sobra a igualdade de zeroformas, sem descartar uma divergência,

\[
 s(\mathcal J^\mu\eta_\mu)=(\partial_\mu\mathcal J^\mu)\eta.
\]

O antifield contraído K_X*=φ_i*X^i é ímpar. O sinal de Leibniz em sK_X* faz −φ_i*sX^i tornar-se +c^μ φ_i*∂_μX^i. Consequentemente sK_X*=𝔈·X+Lie_cK_X*. Ao multiplicar por η, o transporte contém cinco ghosts não derivados e se anula; o termo de peso cancela −K_X*sη. Segue s(K_X*η)=(𝔈·X)η.

As três identidades fecham precisamente

\[
 \alpha_X=\mathcal J_X^\mu\eta_\mu+(\phi_i^*X^i)\eta,
 \qquad
 s\alpha_X=(\partial_\mu\mathcal J_X^\mu+\mathcal E_iX^i)\eta=0.
\]

O sinal positivo no segundo termo depende da convenção de KT explicitada. A nota explica corretamente a mudança que seria necessária para um dicionário com KT oposta. A identificação com J_X(c,c,c)/3! também confere: i_(∂_μ)d⁴x tem o mesmo sinal (−1)^μ de η_μ, e não sobra fator4 ou24.

## 3. Os seis geradores são globais, e o antifield ambiente é tangente

A escolha X_AB(Y^C)=Y_Aδ_B^C−Y_Bδ_A^C é a rotação infinitesimal unitária no plano AB. Ela gera seis campos de Killing globais do alvo redondo. A corrente é c_σv_g(Y_A∇Y_B−Y_B∇Y_A), sem fator1/2 ou κ oculto.

A expressão P_A=φ_i*h^{ij}∂_jY_A é intrínseca apesar da escrita em coordenadas φ. Com o embedding isométrico Y:S³→R⁴,

\[
 Y^AP_A=0,\qquad
 P_A\,\delta Y^A=\phi_i^*\delta\phi^i,\qquad
 P_C X_{AB}(Y^C)=Y_AP_B-Y_BP_A.
\]

Na última igualdade, A,B são os dois rótulos fixos e C é o índice contraído. Portanto não há quatro antifields independentes ou multiplicador novo. O mapa do antifield continua de posto três em cada ponto.

O controle da tensão ambiente também está correto. De Y·Y=1 segue Y·□Y=−Q, logo □Y+QY é tangente. A derivada de Euler tangente é −c_σv_g(□Y+QY); o termo Q cancela no par antissimétrico e reproduz exatamente a identidade de Noether(17).

As expressões α_AB colam globalmente sobre S³. Elas formam uma família que transforma como Λ²R⁴ sob a simetria rígida do alvo. Naturalidade de espaço-tempo e covariância dessa família não significam que cada componente seja um escalar O(4) invariante.

## 4. Setor K e precisão sobre Rees

Os representantes usam apenas campos ativos, antifields mínimos, seus tensores covariantes e c não derivado. Para o termo de antifield contraído, b_N aniquila 𝔈·X; a parte de Lie fornece a derivada covariante de fundo do tipo densidade. Para 𝒥 vale o mesmo cálculo no tipo vetor densidade. As conexões cancelam no escalar completo α_X e C_N aniquila seus geradores. Assim E_Nα_AB=C_Nα_AB=0 no domínio MÉTRICO de074. Não se aplica esse resultado ao ghost Lorentz excluído pelo adendo de frames.

[DERIVED — precisão aditiva de transporte] A nota do levantamento está escrita em campos e fontes ativos. Para utilizá-la na [completação Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>), deve-se puxar também os antifields pelo lift cotangente, e não substituir apenas φ por Exp_(φ₀)(tξ). Escrevendo

\[
 f_t(\xi)=\operatorname{Exp}_{\phi_0}(t\xi),\quad
 A_t=t^{-1}D_\xi f_t,\quad
 \phi^*=t A_t^{-T}\xi^*,\quad c=tC,
\]

com as demais variáveis transportadas canonicamente, vale Ψ_t*ω=t²ω_can. Por isso S_t=t^−2(S∘Ψ_t) gera o BRST transportado e s_t(α_X∘Ψ_t)=(sα_X)∘Ψ_t=0.

A corrente pode ter valor de fundo não nulo: sua contribuição começa em t³ por causa dos três ghosts. O termo de antifield começa em t⁵ na expansão ordinária, com uma fonte normalizada e quatro ghosts. Esses termos de valências diferentes pertencem à mesma série ∏_E t^E P_E; não se exige que comecem na mesma ordem. Cada coeficiente é homogêneo no número de campos normalizados correspondente. Multiplicar a série completa por t^(2L−2) produz um elemento de R_L. As funções de g e da exponencial têm expansão finita em cada coeficiente, e o lift das fontes é pontual, preservando a ordem finita dos jatos.

Isso é transporte de uma identidade formal inteira. Não se afirma que cada coeficiente separado seja um ciclo do BRST completo s_t, que um truncamento sem margem preserve a identidade exata ou que a série seja uma corrente quântica de laço L. Em dimensões de engenharia, [𝒥]=3, [c]=−1 e [φ*]=4 dão peso zero aos dois termos de α, coerente com o transporte.

Uma mudança de gauge exige conjugação canônica da expressão inteira. A igualdade no setor K foi estabelecida antes dessa conjugação; não se reaplica K por mera inspeção parcial dos campos já gauge-fixados.

## 5. Parecer e limites

[DERIVED] Parecer favorável ao levantamento off-shell dos seis representantes e ao cálculo E_N=C_N=0. Não solicito correção material da fonte. A precisão Rees acima é uma composição aditiva com a regra já demonstrada em074, sem editar o adendo do autor.

[OPEN] Não foram demonstradas não trivialidade ou independência das seis classes, ausência de melhorias, exaustividade de H³, classificação de H⁴, os grupos residuais de Ē_N, uma corrente quântica renormalizada ou QME. “Seis” conta os pares de geradores escritos, não a dimensão de uma cohomologia.

[REAL — custódia] O recibo separado confere os pins do autor e mede as onze entradas locais antes/depois da gravação. Não houve CAS/Lean, execução/importação de um.py, mudança de originais, alteração de arquivos congelados ou reabertura da entrega075. Os checks documentais não são apresentados como substitutos da revisão matemática escrita.
