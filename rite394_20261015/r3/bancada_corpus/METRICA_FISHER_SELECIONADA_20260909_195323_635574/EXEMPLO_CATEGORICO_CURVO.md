# Testemunha categórica: métrica curva sem métrica de entrada

[DERIVED — demonstração escrita. Não formalizada em Lean neste exemplo.]

Considere o aberto U de R⁴ definido por x₀,x₁,x₂,x₃>0 e x₀+x₁+x₂+x₃<1. Defina cinco probabilidades:

P₀=x₀, P₁=x₁, P₂=x₂, P₃=x₃, P₄=1−x₀−x₁−x₂−x₃.

A soma é 1 em todo R⁴, e todos os pesos são positivos em U. As funções são suaves. As primeiras quatro componentes do diferencial conjunto formam a identidade, logo o diferencial é injetivo. O relógio selecionado c=dP₀=dx₀ não se anula. Assim estes dados satisfazem, matematicamente, o contrato `SelectedProbabilityData (Fin 5) U`. Nenhum campo g foi usado para escolher os pesos.

O Fisher e sua inversa são, para a,b∈{0,1,2,3},

F_ab = δ_ab/x_a + 1/P₄,

(F⁻¹)_ab = δ_ab x_a − x_a x_b.

A multiplicação verifica a inversa porque Σ_{a<4}x_a=1−P₄. Portanto cᵀF⁻¹c=x₀(1−x₀)>0. O campo da folha é exatamente

g_ab = 2 δ_a0 δ_b0/[x₀(1−x₀)] − δ_ab/x_a − 1/P₄.

Para reconhecer sua curvatura, escreva q=P₀ e Q_a=P_a/(1−q), a=1,...,4. Então ΣQ_a=1 e todos Q_a>0. Expandindo a soma Σ dP_i²/P_i, os termos cruzados anulam-se por ΣdQ_a=0:

F = dq²/[q(1−q)] + (1−q) Σ_a dQ_a²/Q_a.

O covetor dq tem norma dual quadrada q(1−q), de modo que a leitura assinada dá

g = dq²/[q(1−q)] − (1−q) Σ_a dQ_a²/Q_a.

Ponha r=2 arcsin√q e z_a=√Q_a. Os z percorrem o octante positivo da esfera unitária S³, e ΣdQ_a²/Q_a=4Σdz_a²=4h_{S³}. Logo

g = dr² − a(r)² h_{S³},     a(r)=2 cos(r/2),     0<r<π.

Esta métrica não é plana. Em coordenadas espaciais locais, Γᴬ₀ᴮ=(a′/a)δᴬᴮ e Γᴬ₀₀=0. Com a convenção R^ρ_{σμν}=∂_μΓ^ρ_{νσ}−∂_νΓ^ρ_{μσ}+Γ^ρ_{μλ}Γ^λ_{νσ}−Γ^ρ_{νλ}Γ^λ_{μσ}, obtém-se Rᴬ₀ᴬ₀=−a″/a=1/4, sem somar A. A convenção oposta troca o sinal e preserva a não nulidade. Assim o protocolo categórico evita o controle plano dos quatro Bernoulli-produto.

[INPUT] Permanecem a família de preparações P(x), quatro parâmetros, o rótulo temporal 0 e a lei de leitura assinada. A demonstração não mostra que a natureza impõe esta lei, nem que toda métrica lorentziana pertence a esta família. Trocar o rótulo pode produzir outra métrica. A codificação de saída pelo registro angular não transforma os seus 16 parâmetros em cinco pesos experimentais idênticos.

[OPEN — correspondência de área] A curva afim P(x+tv) não ganha matching de área automaticamente. No interior deste simplex, dS=0 somente no ponto uniforme P_i=1/5: os quatro componentes de dS são log(P₄/P_a). Fora dele há direções nulas com dS(v)≠0, pois o cone nulo de uma forma lorentziana não degenerada gera o espaço tangente. Uma tela de equilíbrio tem A′(0)=0; portanto o erro entrópico de primeira ordem não pode ser o(t²) nessas direções. A métrica construída pode ser consumida por outros protocolos quadráticos, com suas condições de área ainda explícitas.
