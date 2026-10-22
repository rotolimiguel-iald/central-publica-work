# Consulta: semifinitude do peso e minorantes do traço

[DERIVED — verificação matemática escrita, sem formalização Lean nova]

A correção proposta pelo principal é válida. O contraexemplo abaixo impede exigir do peso não tracial ν a propriedade de minorantes que o contrato `RegularCoreTraceData.semifinite` exige do futuro traço τ. Nenhum contrato, fonte, relatório selado ou memória foi modificado. A consulta não aceita a existência de τ e não muda as revisões 40/5/6/3/15.

[KNOWN — fonte primária relida] Hiai, *Concise lectures on selected topics of von Neumann algebras*, Definição 7.1, p.63, identifica semifinitude com densidade fraca de Nφ, supremum das projeções de peso finito igual a 1, ou uma rede crescente de positivos de peso finito com supremum 1. Não afirma a fórmula de minorantes finitos abaixo de cada positivo. [PDF arXiv, v1](https://arxiv.org/pdf/2004.02383#page=63).

Considere H=ℓ²({1,2,…}) e φ(A)=Σₙ n²⟨eₙ,Aeₙ⟩, para A≥0. A soma de termos não negativos define um peso. É normal: para uma rede crescente Aᵢ↑A, cada soma finita é normal, e os dois supremos (rede e conjuntos finitos de índices) comutam. É fiel: φ(A)=0 implica A¹ᐟ²eₙ=0 para todo n e, pela densidade, A=0.

Denote por p_N a projeção nas primeiras N coordenadas. Para qualquer x limitado,

    φ((x p_N)* (x p_N)) = Σ_{n≤N} n² ‖x eₙ‖² < ∞.

Logo x p_N∈Nφ e x p_N→x fortemente. Isso prova a semifinitude relevante sem condição de minorantes em cada A.

Escolha c=(Σₙn⁻²)⁻¹ᐟ²>0 e ξₙ=c/n. Então ‖ξ‖=1 e φ(Pξ)=Σₙc²=∞. Se 0≤B≤Pξ, para y⊥ξ temos ⟨y,By⟩=0 e portanto B¹ᐟ²y=0. A positividade dá B=PξBPξ=bPξ, com 0≤b≤1. Para b>0 seu peso é infinito; b=0 tem peso zero. Assim

    sup{φ(B): 0≤B≤Pξ, φ(B)<∞}=0 ≠ φ(Pξ).

Para um traço normal semifinito τ a conclusão é diferente. Tome projeções eᵢ↑1 com τ(eᵢ)<∞ (rede, sem impor σ-finitude). Para A≥0 limitado, Bᵢ=A¹ᐟ²eᵢA¹ᐟ² satisfaz 0≤Bᵢ≤A, Bᵢ↑A e, por tracialidade aplicada a x=eᵢA¹ᐟ²,

    τ(Bᵢ)=τ(eᵢAeᵢ)≤‖A‖τ(eᵢ)<∞.

A normalidade fornece τ(A)=supᵢτ(Bᵢ), inclusive quando τ(A)=∞. É precisamente a tracialidade que torna este argumento utilizável; não se deve transportá-lo para φ sem essa hipótese.

[REAL — leitura de fonte, sem rebuild nesta consulta] Em `V351ScalarWeightSemifiniteness.lean:15`, `TGLV351.scalarWeight_square_finite_wot_closure` fornece a densidade fraca do domínio quadrado-finito concreto, consumindo `scalarDualWeight_square_finite_strong_density`. O nome `scalarWeightLeftIdeal_wotDense` da mensagem não foi localizado literalmente em k/TGLExt; não foi usado como pin de uma declaração. `V351RegularCoreTraceContract.lean:56` conserva a fórmula de minorantes no campo `semifinite`, ao lado do campo `tracial` na linha58. As hipóteses desses campos são distintas e a presente nota não produz um habitante da estrutura.

[OPEN] Construção/perturbação do traço de A1(b). Esta nota remove uma cobrança inadequada sobre ν; não fornece nem dispensa os campos do traço τ.

Data da leitura: 2026-09-14T19:04:07.591017-03:00

Pins lidos dos dois fontes:

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean` — SHA256 `f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceContract.lean` — SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`.
