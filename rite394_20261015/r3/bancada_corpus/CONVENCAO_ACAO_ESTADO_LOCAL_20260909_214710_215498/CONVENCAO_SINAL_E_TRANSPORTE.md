# Convenção da ação para transportar o estado ao representante probabilístico local

[DERIVED — conferência escrita de sinais; não compilada em Lean] As notas do bloco livre e da quantização ambiente usam ações com sinais globais opostos. Isso preserva as equações clássicas, mas inverte a Hessiana e a forma simplética. Para compor os resultados, a escolha explícita será a ação da quantização, puxada pelo mapa probabilístico. Nenhuma nota congelada é alterada.

## A identificação que deve ser usada

Na [prova do bloco livre, §5](<C:/IALD/Central de Patentes/Chatgpt/COARSE_GRAINING_VARIACIONAL_LIVRE_20260909_212902_6343960/PROVA_COARSE_GRAINING_LIVRE.md>), a ação restrita à esfera foi

\[
S_{old}=\int\mu_g\left[\frac{R-2\Lambda}{2\kappa}
-\frac C2\sum_a g^{-1}(d\phi_a,d\phi_a)\right],\qquad\sum_a\phi_a^2=1.
\]

A [ação ambiente da quantização, §1](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>) e as reduções S/V e TT adotam

\[
S_{phys}=\int\mu_g\left[-\frac{R-2\Lambda}{2\kappa}
+\frac c2\sum_a g^{-1}(d\phi_a,d\phi_a)\right],\qquad c>0.
\]

Identifique `C=c`, preserve a assinatura `+---`, a convenção de curvatura, a orientação temporal e os acoplamentos. Então

\[
\boxed{S_{phys}=-S_{old},\qquad
S_{P,phys}:=S_{phys}\circ\Phi=-S_{old}\circ\Phi.}
\]

Essa escolha é [INPUT/POSTULATE] da ação. Os coeficientes cinéticos positivos das reduções físicas pertencem a `S_phys`. O presente ajuste de notação não os deduz da normalização de probabilidades.

Se o multiplicador for explicitado, a nota antiga usa `−c λ_geom(φ²−1)/2`, com `Box φ=λ_geom φ`. A convenção da quantização usa `+λ_phys(φ²−1)/2`, com `−c Box φ+λ_phys φ=0`. A identificação é

\[
\lambda_{phys}=c\lambda_{geom},\qquad
\lambda_{geom}=-\sum_a g^{-1}(d\phi_a,d\phi_a).
\]

Portanto também a ação completa com multiplicador é a negativa da antiga depois dessa mudança de unidade do multiplicador. Na formulação intrínseca da esfera, ele já foi eliminado e nenhuma variável extra é acrescentada.

## O que muda e o que permanece

Com os termos de fronteira e as convenções de potencial casados,

\[
E_{phys}=-E_{old},\quad H_{phys}=-H_{old},\quad
\theta_{phys}=-\theta_{old},\quad
\omega_{phys}=-\omega_{old},\quad\Omega_{phys}=-\Omega_{old}.
\]

Já `Φ`, `A=DΦ`, o inverso explícito `R`, a identidade `AR=Id`, seu adjunto `R^*A^*=Id` e o espaço de soluções clássicas não mudam. O adjunto aqui é definido pelo mesmo pareamento de testes/densidades, não por uma energia cujo sinal foi trocado.

O [adendo linearizado](<C:/IALD/Central de Patentes/Chatgpt/ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751/ADENDO_LINEARIZADO_E_SIMPLÉTICO.md>) aplica-se integralmente a `S_phys`:

\[
B_{phys}=A^*H_{phys}A=-B_{old},\qquad
B_{phys}p=0\ \Longleftrightarrow\ H_{phys}Ap=0.
\]

Seu termo de integração por partes passa a ser

\[
J_{phys}^{\mu}=E_{phys,\alpha}\,b^{\alpha\mu}{}_i p^i=-J_{old}^{\mu}.
\]

Nas soluções linearizadas, segue a igualdade com sinais efetivamente correspondentes,

\[
\boxed{\omega_{P,phys}(p_1,p_2)
=\omega_{phys}(Ap_1,Ap_2),\qquad
\Omega_{P,phys}=A^*\Omega_{phys}.}
\]

A última expressão é o pullback de uma forma bilinear, não a composição de operadores de Jacobi. As condições de suporte, fluxo e carga de fronteira do adendo continuam necessárias. Não se identifica `Ω_old` com `Ω_phys`.

## Comutador e estado

Para um mesmo esquema de fixação de gauge cujo termo quadrático também mude de sinal, os operadores causais de `−H_gf` são os negativos dos de `H_gf`; a diferença retardado menos avançado também muda de sinal. Equivalentemente, o comutador dos observáveis e a forma CCR acompanham o sinal da ação quando a orientação causal é preservada.

Assim uma covariância que satisfaz `W−W^T=iℏσ_phys` não é declarada satisfazer o mesmo comutador com `σ_old=−σ_phys`. Sua transposta inverteria o comutador e a orientação de frequência; essa troca não é feita silenciosamente.

Para transportar o estado físico ambiente adotamos **`S_{P,phys}=S_phys∘Φ`** e o isomorfismo simplético do adendo com essas formas. Se o estado está estabelecido para a álgebra ambiente no domínio e nas condições correspondentes, sua composição com o isomorfismo das álgebras reduzidas é positiva: `ω_P(a* a)=ω_phys(I(a)* I(a))≥0`. É esse transporte que se usa; não uma identificação entre uma forma e sua negativa.

A construção probabilística e seu inverso continuam locais, numa carta positiva com Gram livre. Uma restrição de um estado construído em `I×S³` pode ser usada na álgebra local compatível; isso não transforma a carta de probabilidades numa parametrização global de `S³`, nem identifica automaticamente álgebras com outros grupos de gauge ou outras condições de contorno. Também não prova que flutuações quantizadas sejam operadores de probabilidade positivos para toda amplitude.

[DERIVED] A diferença de sinal foi explicitamente resolvida para a composição dos resultados. [OPEN] Nenhuma conclusão nova sobre quantização interagente, anomalias, limite UV ou positividade operatorial não linear resulta apenas dessa correção de convenção. Originais, fontes Lean e notas congeladas permanecem preservados.
