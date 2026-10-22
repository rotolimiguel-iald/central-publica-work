# Revisão da raiz: setor K, homotopia do alvo e correntes076

10/09/2026. [DERIVED — revisão escrita]. Li integralmente a nota de módulos, o adendo de correntes e os dois pareceres de Herschel. Parecer favorável aos enunciados delimitados, sem promover a lista de representantes a uma classificação dos módulos completos.

No setor K, aplicar b_N à derivada de Lie equivale à derivada covariante de B0 em cada fator. Incluem-se pesos de densidade. A conexão cancela nas contrações escalares; C_N aniquila c não derivado e os demais fatores. As partes KT e seus prolongamentos não contêm ghosts. O parecer independente explicita também o antifield do ghost c*, que é covetor densidade e possui transporte de Lie mais o termo de Noether sem ghosts. Portanto E_N=C_N=0 está demonstrado nesse setor; não se estende por nome a ∇̄c.

A família A_L=ρ_L c⁰c¹c²c³ é s-fechada pelo cancelamento da divergência e pela ausência de cinco ghosts não derivados independentes. Isso constrói ciclos; não afirma classes não nulas.

A homotopia do volume do alvo usa F_u=Exp_(φ0)(utξ), V_u=sF_u e W_u=∂uF_u. Cartan dá ∂u[Ω(V,V,V)/6]=s[Ω(W,V,V)/2]. A extremidade u=0 desaparece porque sφ0=0, mesmo quando d_Hφ0≠0. Assim τ3=sK2 na classe formal declarada. O termo inicial K2=t³Ω(φ0)ξ(s_tξ)²/6 tem a normalização correta. A avaliação ξ=0 não é mapa de complexos para o BRST ativo; não apaga seu derivado.

A construção é intrínseca sobre φ0*TS³, natural e finita em jatos por coeficiente. Não define uma primitiva global de de Rham do volume de S³. O fator topológico global GL⁺4 e os polinômios CE de Lorentz também não são identificados automaticamente com classes formais. A condição de classe e a curvatura no diferencial permanecem necessárias.

Para as correntes de Killing, conferi diretamente ∂μ𝒥_X^μ=−𝔈_iX^i, com 𝔈_i=−cσ√|g| h_ij τ^j. A derivada de Euler e o antifield são densitizados uma única vez. Com η=c⁰c¹c²c³ e η_μ=∂_Lη/∂c^μ, as identidades
s(𝒥^μη_μ)=(∂μ𝒥^μ)η e s[(φ*·X)η]=(𝔈·X)η
produzem sα_X=0 para α_X=𝒥^μη_μ+(φ*·X)η. O segundo sinal é positivo na convenção efetiva sφ*=+𝔈+Lie_cφ*. Os dois sinais ímpares, na variação de φ*X e na multiplicação por η, são necessários.

A escrita ambiente usa P_A=φ_i*h^{ij}∂jY_A tangente, com Y·P=0; não acrescenta um quarto antifield livre. Os seis geradores AB são campos de Killing globais e as expressões formam o módulo Λ²R⁴ do alvo. Cada componente não é, por si, um escalar O(4) invariante. Também não se provou dim H³=6.

A precisão Rees do parecer independente é consumida: a expansão deve transportar antifields pelo lift cotangente completo, φ*=tA_t^-T ξ*, além de φ=Exp_(φ0)(tξ). A identidade s_t(α∘Ψ_t)=0 vale para a série inteira. O termo de corrente pode começar em t³ e o de antifield em t⁵; graus distintos não impedem que a série pertença à mesma completação. Isso não faz cada coeficiente isolado um ciclo de s_t.

[OPEN] A geração e as relações de H³/H⁴, os dois canais de Ebar_N, a primitiva admissível da anomalia e a carga/QME não foram concluídas. A nova transgressão característica da raiz tem sua revisão própria pendente; não é aprovada por este parecer. Zero CAS/Lean e nenhuma fonte alterada.
