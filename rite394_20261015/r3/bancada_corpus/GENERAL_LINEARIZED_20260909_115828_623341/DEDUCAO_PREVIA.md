# Dedução prévia — Ward clássico-linear para campos suaves gerais
Data: 09/09/2026. Pasta nova de bancada; nenhum original alterado.
Estatuto inicial: [DERIVED — dedução matemática a formalizar]. A compilação será medida depois.

## Objeto e lacuna
Reutilizar TGLExt.pd e TGLExt.linRicci, definidos em ContinuumShards.lean e ContinuumTT.lean.
O operador já aceita um campo arbitrário h_{μν}: R^4→R; os certificados posteriores aplicam
o Ward ao símbolo de uma onda plana. O novo alvo é o próprio operador diferencial para h geral.

Hipóteses: cada componente de h e cada componente do covetor ξ é ContDiff R ∞.
O fundo continua sendo a métrica plana diagonal etaDiag do modelo. Não se assume TT,
perfil de onda plana, soma finita de modos, equação de movimento ou comutação de derivadas.
A simetria de h é permitida, mas desnecessária para a identidade de gauge desse operador.

## Derivadas e regularidade
D_i f(x) = fderiv R f x (Pi.single i 1), exatamente o pd canônico.
Suavidade é preservada por D_i, somas finitas e multiplicação por constantes.
O teorema de simetria da segunda derivada da Mathlib, aplicado a f suave e a suas derivadas,
fornece D_i D_j f = D_j D_i f. Aplicá-lo novamente permite permutar derivadas terceiras.
As regras de derivação de somas serão usadas apenas depois de provar diferenciabilidade.

## Cancelamento de gauge
Defina (Kξ)_{μν} = D_μ ξ_ν + D_ν ξ_μ. A definição canônica é
R1(h)_{μν} = (1/2) Σ_a eta_a [D_a D_μ h_{aν} + D_a D_ν h_{aμ} - D_a² h_{μν}]
            - (1/2) D_μ D_ν [Σ_a eta_a h_{aa}].

Substituindo h=Kξ, para cada a o numerador restante é:
D_a D_μ D_a ξ_ν + D_a D_μ D_ν ξ_a
+ D_a D_ν D_a ξ_μ + D_a D_ν D_μ ξ_a
- D_a² D_μ ξ_ν - D_a² D_ν ξ_μ - 2 D_μ D_ν D_a ξ_a.
Schwarz cancela o primeiro com o quinto, o terceiro com o sexto;
os dois termos restantes somam 2 D_μ D_ν D_a ξ_a e cancelam o traço.
Logo R1(Kξ)=0, ponto a ponto. A linearidade, com regularidade provada, dá
R1(h+Kξ)=R1(h)+R1(Kξ)=R1(h).

## Alcance
O resultado supera a restrição de onda plana do Ward clássico-linear.
Não é quantização, cancelamento de anomalias interagentes, prova da ação Fierz–Pauli completa,
ausência de ghosts no setor geral, reconstrução de métrica curva geral ou resposta UV.
A divergência de Einstein/Bianchi será um complemento apenas se puder ser derivada
naturalmente da mesma API, mantendo o objeto e a regularidade explícitos.
