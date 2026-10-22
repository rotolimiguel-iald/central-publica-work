# Levantamento BRST explícito das seis correntes de Killing sigma

10/09/2026, arco076. [DERIVED — demonstração escrita off-shell]. Adendo novo à [investigação dos módulos H³/H⁴](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md>), seção4.2. Nenhuma fonte alterada, nenhum um.py executado/importado e zero CAS/Lean.

## 1. Ação, orientação e antifield densitizado

Usamos a ação física e a assinatura +--- fixadas na [convenção067](<C:/IALD/Central de Patentes/Chatgpt/CONVENCAO_ACAO_ESTADO_LOCAL_20260909_214710_215498/CONVENCAO_SINAL_E_TRANSPORTE.md>) e na [CME071, equação1](<C:/IALD/Central de Patentes/Chatgpt/CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910/CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md>):

\[
S=\int d^4x\,v_g\left[-\frac{R-2\Lambda}{2\kappa}
 +\frac{c_\sigma}{2}g^{\mu\nu}h_{ij}(\phi)
                 \partial_\mu\phi^i\partial_\nu\phi^j\right],
\quad v_g=\sqrt{|\det g|},\quad c_\sigma>0.
\tag{1}
\]

O alvo é S³ unitário com métrica redonda h. A relação κc_σ=4 pode ser imposta depois; nenhum fator de κ foi absorvido no currente ou no antifield abaixo. O símbolo c_σ é o coeficiente da ação; c^μ é o ghost difeomórfico.

Fixamos d⁴x=dx⁰∧dx¹∧dx²∧dx³, ε₀₁₂₃=+1. Defina a derivada de Euler DENSITIZADA

\[
\mathcal E_i=\frac{\delta S}{\delta\phi^i},\qquad
\delta\mathcal L=\mathcal E_i\delta\phi^i+d_H\theta(\delta\phi).
\tag{2}
\]

O antifield φ_i* também é uma densidade de peso1: o pareamento local é \(\int d^4x\,\phi_i^*\,s\phi^i\), sem multiplicar novamente por v_g. Ele é ímpar e tem ghost−1. Se se prefere um antifield escalar \(\widehat\phi_i^*\), a conversão é φ_i*=v_g\(\widehat\phi_i^*\).

Trabalhamos antes do gauge, no BV MÉTRICO mínimo. Os pares não mínimos de069 e a transformação canônica de gauge não são acrescentados por omissão à fórmula. Para usar a fórmula em variáveis já gauge-fixadas, é necessário aplicar a mesma transformação canônica à expressão inteira, como em qualquer representante BV.

## 2. Sinal BV efetivamente usado

O [dicionário069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>) fixa s como derivação ímpar à esquerda, sφ^i=c^μ∂_μφ^i e sc^μ=c^ν∂_νc^μ. Escreva o bloco de fontes escalares com a fonte à esquerda,

\[
\Sigma=S+\int d^4x\,\phi_i^*\,c^\mu\partial_\mu\phi^i+\cdots.
\tag{3}
\]

Uma realização bilinear graduada compatível é a de [Fröb, equações104,110 e140](https://arxiv.org/pdf/1803.10235): nos geradores escalares,

\[
s\phi^i=-\frac{\delta_R\Sigma}{\delta\phi_i^*},\qquad
s\phi_i^*=+\frac{\delta_R\Sigma}{\delta\phi^i}.
\]

A derivada DIREITA do termo φ_i*R^i em relação à fonte ímpar é −R^i, porque R^i=c·∂φ^i também é ímpar. A primeira fórmula reproduz, portanto, o sinal positivo de sφ. Na segunda, variar φ^i, que é par, dá

\[
-\partial_\mu(\phi_i^*c^\mu)
 =+\partial_\mu(c^\mu\phi_i^*).
\]

Logo a regra que será efetivamente utilizada é

\[
\boxed{s\phi_i^*=\mathcal E_i
       +c^\mu\partial_\mu\phi_i^*
       +(\partial_\mu c^\mu)\phi_i^*.}
\tag{4}
\]

As fontes de métrica e de ghost não contribuem a essa derivada em φ no modelo intrínseco: o gerador difeomórfico da métrica e sc não dependem de φ. O termo KT é +𝔈_i. Não se lê o sinal de (4) de uma notação abstrata de ordem dos argumentos do antibracket sem seu dicionário de derivadas.

Se outra implementação nomear por φ* uma fonte com sinal oposto e adotar sφ*=−𝔈+Lie_cφ*, o termo de antifield do representante abaixo deve ter sinal negativo. Isso é somente um dicionário de apresentação; nesta nota a convenção fixada é (3)–(4), com sinal positivo e a ação(1).

## 3. Identidade de Noether com normalização completa

Seja X=X^i(φ)∂_i um campo de Killing do alvo, L_Xh=0. A transformação rígida é δ_Xφ=X, δ_Xg=0. A corrente VETORIAL e a corrente DENSITIZADA são

\[
j_X^\mu=c_\sigma h_{ij}(\phi)X^i(\phi)\nabla^\mu\phi^j,
\qquad \mathcal J_X^\mu=v_gj_X^\mu.
\tag{5}
\]

Sua 3-forma é

\[
J_X=\mathcal J_X^\mu\,\iota_{\partial_\mu}d^4x
   =\iota_{j_X}dV_g.
\]

Pela invariância da ação sob X, a identidade de Noether é

\[
\boxed{\partial_\mu\mathcal J_X^\mu
       =-\mathcal E_iX^i,\qquad
       d_HJ_X=-\mathcal E_iX^i d^4x.}
\tag{6}
\]

É uma igualdade off-shell. Uma verificação direta usa a tensão sigma

\[
\tau^i=\Box_g\phi^i+\Gamma(h)^i{}_{jk}
                     g^{\mu\nu}\partial_\mu\phi^j\partial_\nu\phi^k,
\qquad \mathcal E_i=-c_\sigma v_g h_{ij}\tau^j.
\]

A divergência de(5) é c_σv_g h_ij X^iτ^j, pois o termo com ∇_(i X_j) se anula. Isso dá (6) com o sinal declarado. A parte Einstein da ação não varia sob X, e nenhuma equação métrica foi imposta.

## 4. Dois polinômios Grassmann e suas identidades

Defina

\[
\eta=c^0c^1c^2c^3,\qquad
\eta_\mu=\frac{\partial_L\eta}{\partial c^\mu}
 =(-1)^\mu c^0\cdots\widehat{c^\mu}\cdots c^3.
\tag{7}
\]

η tem ghost4 e paridade par; η_μ tem ghost3 e paridade ímpar. Temos c^νη_μ=δ^ν_μη. Com sc=c·∂c, a regra graduada fornece

\[
s\eta=-\eta\,\partial_\nu c^\nu,
\qquad
s\eta_\mu=(\partial_\mu c^\nu)\eta_\nu
              -(\partial_\nu c^\nu)\eta_\mu.
\tag{8}
\]

Na primeira identidade, somente o termo com o mesmo índice do ghost substituído sobrevive; os demais repetem um dos quatro ghosts. Reordenar a derivada de ghost produz o sinal negativo. A segunda identidade pode ser verificada por derivação esquerda do produto(7), com a mesma regra de Leibniz.

Para qualquer vetor-densidade PAR natural 𝒥^μ de peso1,

\[
s\mathcal J^\mu=c^\nu\partial_\nu\mathcal J^\mu
 -(\partial_\nu c^\mu)\mathcal J^\nu
 +(\partial_\nu c^\nu)\mathcal J^\mu.
\]

Aplicando(8), os termos ∂c de índice vetorial se cancelam par a par, assim como os termos de peso. O transporte restante usa c^νη_μ=δ^ν_μη. Logo

\[
\boxed{s(\mathcal J^\mu\eta_\mu)
             =(\partial_\mu\mathcal J^\mu)\eta.}
\tag{9}
\]

Não se descartou uma derivada total para obter (9); a igualdade é de zeroformas locais.

## 5. Termo de antifield e cancelamento off-shell

Ponha

\[
K_X^*=\phi_i^*X^i(\phi).
\]

É uma densidade ímpar de ghost−1. Por(4), sX^i=c^μ∂_μX^i e Leibniz ímpar,

\[
sK_X^*=(s\phi_i^*)X^i-\phi_i^*sX^i
       =\mathcal E_iX^i+c^\mu\partial_\mu K_X^*
                       +(\partial_\mu c^\mu)K_X^*.
\tag{10}
\]

O sinal negativo do segundo termo se torna positivo ao mover c através de φ*, ambos ímpares; isso completa a derivada de Lie do produto. Agora,

\[
s(K_X^*\eta)=(sK_X^*)\eta-K_X^*s\eta
             =\boxed{(\mathcal E_iX^i)\eta.}
\tag{11}
\]

O termo de transporte tem cinco c não derivados e se anula. Os termos com div c se cancelam porque K_X* e div c são ímpares. Esquecer o sinal de Leibniz em(11) impediria essa cancelamento.

Definimos o representante de ghost3

\[
\boxed{\alpha_X=\mathcal J_X^\mu\eta_\mu
                      +(\phi_i^*X^i)\eta.}
\tag{12}
\]

Usando (6), (9) e (11),

\[
\boxed{s\alpha_X=
 [\partial_\mu\mathcal J_X^\mu+\mathcal E_iX^i]\eta=0.}
\tag{13}
\]

A prova é off-shell: o termo de antifield é exatamente o que cancela a divergência não nula da corrente antes de impor as equações. Não há inversão de dφ, escolha de fundo especial, solução de uma EOM ou importação de uma hipótese sα=0.

Em notação de formas,

\[
I_c(J_X):=\frac1{3!}(J_X)_{\mu\nu\rho}c^\mu c^\nu c^\rho
          =\mathcal J_X^\mu\eta_\mu,
\]

e (12) é I_c(J_X)+(φ_i*X^i)η. O fator1/3! é compensado pelas permutações dos componentes da 3-forma; não há um fator4 ou24 adicional no termo de antifield, já escrito na ordem fixa η.

## 6. As seis fórmulas no embedding unitário de S³

Use Y^A(φ), A=1,2,3,4, com Y^AY_A=1. Para A<B, o gerador escolhido satisfaz

\[
X_{AB}(Y^C)=Y_A\delta_B^C-Y_B\delta_A^C.
\tag{14}
\]

São os seis pares12,13,14,23,24,34. A normalização é a rotação infinitesimal unitária descrita por(14), sem fator1/2. Então

\[
\mathcal J_{AB}^{\mu}=c_\sigma v_g
        (Y_A\nabla^\mu Y_B-Y_B\nabla^\mu Y_A).
\]

Represente o antifield intrínseco por seu covetor tangente ambiente densitizado

\[
P_A=\phi_i^*h^{ij}\partial_jY_A,
\qquad Y^AP_A=0.
\tag{15}
\]

Não são quatro antifields independentes novos: (15) é a imagem tangente dos três antifields intrínsecos, com φ_i*δφ^i=P_AδY^A. O termo de fonte é

\[
\phi_i^*X_{AB}^i=Y_AP_B-Y_BP_A.
\]

As seis expressões prometidas são, portanto,

\[
\boxed{\alpha_{AB}=
 c_\sigma v_g(Y_A\nabla^\mu Y_B-Y_B\nabla^\mu Y_A)\eta_\mu
 +(Y_AP_B-Y_BP_A)\eta,\qquad A<B.}
\tag{16}
\]

Cada uma satisfaz sα_AB=0 pela demonstração anterior. Como controle da esfera, a derivada de Euler tangente ambiente é

\[
\mathcal E_A^{\rm tan}=-c_\sigma v_g(\Box_gY_A+QY_A),
\qquad Q=g^{\mu\nu}\partial_\mu Y^C\partial_\nu Y_C,
\]

e

\[
\partial_\mu\mathcal J_{AB}^{\mu}
 =c_\sigma v_g(Y_A\Box Y_B-Y_B\Box Y_A)
 =-(Y_A\mathcal E_B^{\rm tan}-Y_B\mathcal E_A^{\rm tan}).
\tag{17}
\]

O termo Q cancela por antissimetria. Nenhum multiplicador independente λ foi introduzido: estamos na esfera intrínseca. As expressões se transformam como o módulo antissimétrico Λ²R⁴ sob a simetria rígida do alvo; não se afirma que cada componente isolada seja um escalar invariante sob todo O(4).

## 7. Pertença ao setor K e ação de E_N/C_N

As expressões(12)/(16) usam somente c NÃO derivado, os tensores ativos g,Y, seus derivados covariantes ativos e o antifield tangente densitizado. Não contêm B0 explícito nem ghost Lorentz. Todos os fatores se contraem em escalares naturais de forma0. Portanto pertencem exatamente ao setor K delimitado na nota de módulos076.

Pode-se conferir a conclusão sem substituir um nome por uma prova. A parte KT de sK_X* é 𝔈·X e não contém c; b_N a aniquila. A parte de Lie de 𝒥_X e K_X* dá suas derivadas covariantes para Γ̄ quando se aplica b_N. Também D_Nc=\bar D c. Na contração escalar em(12), os termos de conexão se cancelam. Como C_N anula c não derivado e todos os demais fatores em que não insere,

\[
\boxed{E_N\alpha_{AB}=0,\qquad C_N\alpha_{AB}=0.}
\tag{18}
\]

As fórmulas de b_N,D_N,E_N,C_N são as da [translação métrica074](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md>), com o [alcance de frames corrigido](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md>). Não se usa a extensão Lorentz que aquele adendo deixou separada.

Logo os seis ciclos fornecem elementos calculados do setor H³(s) em que Ē_N atua por zero. Dizer “elementos” não afirma que suas classes sejam distintas de zero ou independentes. Multiplicá-los por formas de fundo continua obedecendo à regra de módulo(11) da nota076; isso não estabelece a injetividade ou sobrejetividade do mapa de módulos.

## 8. Estatuto e fronteira

[DERIVED] O levantamento das seis correntes foi construído com normalização c_σ, orientação, densidades, paridades e sinais de antifields explicitados. A igualdade sα_AB=0 é off-shell e segue diretamente da identidade de Noether da ação física. O termo KT não foi suposto por um wrapper.

[DERIVED] Os representantes pertencem a K, e E_Nα_AB=C_Nα_AB=0. Isso preenche o levantamento que a seção4.2 da nota076 mantinha como candidato a completar.

[OPEN] Não se provaram independência das seis classes, ausência de melhorias que as trivializem na categoria relevante, exaustividade de H³, classificação de H⁴ ou nulidade dos dois grupos de Ē_N. Também não se construiu uma corrente quântica renormalizada nem a QME. Uma mudança de gauge ou de coordenadas BV deve transportar a expressão inteira e seus antifields.

O manifesto mede sete fontes antes/depois. Nenhuma delas foi reescrita; não houve CAS/Lean novo ou execução/importação de um.py. O cálculo aqui apresentado aguarda revisão independente própria.
