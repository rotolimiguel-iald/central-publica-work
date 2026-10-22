# LEVANTAMENTO v393 — o coração e o selo gravitacional (14/10/2026, gerência c1; só leitura)

Fontes lidas: `Nós\um.py` v392 (sha16 b590c0aa80055e2a, 227.843 linhas; NÃO executado), `Nós\tgl_kernel`, README e PORTA do the_boundary, MEMORIA_DA_LINHAGEM, buscar.py. Mapa de rotas consultado (4 temas: «alpha derivado», «selo gravitacional», «G derivado», «motor de Lagrange») = 0 rotas; nada examinado antes. Linhas do um.py são de `um.py`; kernel em `Nós\tgl_kernel\TGLExt\`.

## 1. Tabela elo a elo

| elo | onde no um.py | teorema do kernel | frase pública | estatuto | falta |
|---|---|---|---|---|---|
| ω(I)=1 (o 1 posto) | gate EXECUTION_LOCKED_NOT_ONE (inscrição por `echo 1`) | `TGLExt/AbsoluteOne.lean` (Ψ=1_abs; ω(I)=1 emerge) | README: «posited One (ω(I)=1, POSTO)» | [POSTO] | nada |
| Meia-Nat x=1−x ⟹ ½ | l.1990-2000 (S=1/2), l.7451 | pedras de auto-conjugação; não localizei um teorema único nomeado | README, linha da cadeia | [DERIVED] do posto | citar o teorema exato |
| √e (Vol_min) | l.1997 `vol_min` | não achei no kernel «½ nat ⟹ √e» | README: «Vol_∂^min = √e» | [DERIVED] na bancada; elo de kernel NÃO localizado | pedra «½ nat ⟹ √e», ou marcar [KNOWN]/[CONJECTURE] |
| motor 1=q²+α² | l.1432-1436 (q=√(1−ζ²)); l.2104; módulo SO(2) com S_EM=[[q,α],[−α,q]] | `ContinuousModularZero.lean:159 one_eq_q_sq_add_alpha_sq` (q=tanh(κ/2), α=sech(κ/2), l.151-154); `ConjugateAct.lean:82 J_preserves_identity` | README l.169 (linha 4) e l.205 | [REAL] identidade (resíduo 0,0) | nada; é identidade |
| α_obs=√(1−q²) | l.1432: ζ_L=α_from_Z0 ← `SEALED_CODATA_ALPHA` (l.1421 «alpha_ext … [EXT] input medido») | idem; vale para QUALQUER κ | README: «α=√(1−q²)» | identidade [REAL]; o VALOR de α é **entrada CODATA** | o valor não sai do 1; ver §3 |
| q / espectro de K | q=tanh(κ/2); no código, κ é recuperado do α medido | `alphaKappa`, `qKappa` | (síntese pedida) | leitura interna: o espectro de K dá (q,α) para cada κ; qual κ vale é o que falta | derivar κ sem α |
| β=α√e | l.1435; `ALPHA_FINE_CODATA_2018 * SQRT_E` (l.5584) | `QGSolutionComplete.lean:36`: a implicação não toma β como hipótese | README «β=α√e» | [DERIVED] dado α | idem |
| θ_M=arcsin√β | l.1441, 1997, 5358-5420 (sin²arcsin√b=b em kernel) | morte(θ_M)=β (módulo ~l.5482, `haja_luz_at_the_seal`) | README: S_core=exp(θ_M G), \|R\|²=β | [REAL] identidade; valor herda de α | nada |
| √\|L\| → g | l.1513, 1564, 7210, 7289 (`g=sqrt|L_phi|`) | **nenhum termo `g=√\|L\|`**; no kernel só a fase quadrada e a gramática radical V_s=e^{is√K} (LINHAGEM l.4416, pedra P1b) | README NÃO define \|L\|; aparece em MEMORIA_DA_LINHAGEM l.4219 («extração do radical do módulo de fase angular da luz») | [ONTO]/[CONJECTURE] (a LINHAGEM: «a equação sobrevive, a seta muda») | definir \|L\| (`L_phi`) e uma pedra |
| g → K_β (torção) | README l.174; módulo Ponte-Einstein-Cartan-Miguel | `TracialDissipativeTorsion.lean:59 torsion`, `:469 torsionSupplier`; sem objeto «K_β=β» ligado a g | README l.174: «β=sin²θ_M escreve-se como torção K_β» | [REAL] condicional (tex) | ligar K_β ao θ_M no kernel |
| assinatura (1,3) | l.62606 (runner) | `ModularSignatureObstruction.lean:76 single_boost_has_two_signatures`: um boost preserva (1,3) E (2,2) | README (cadeia) | [REAL], mas NÃO seleciona (1,3) sozinho | critério que escolha (1,3) |
| forma de Einstein | l.7455, 8100-8300, 8532-8668 | `HorizonEinsteinReconstruction.lean:127`; `ConstructedEinsteinReconstruction.lean:53`; `EntropyGeometryControls.lean:89 chosen_area_rescales_einstein_coefficient` | README l.174 | implicação [REAL]; H1-H3 hipóteses nomeadas | G, ver §2 |

## 2. A constante G e o π

O rito (l.8100-8665) declara: `[DER] S_∂=½; τ(P_F)=1; A(P)=2 l_P² τ(P); η=S/A_cell`; `[NORM] A(P_face)=l_P²` (declarada, NÃO derivada da álgebra adimensional); `[DER GIVEN NORM] η=1/(4 l_P²)`; `ħ=c=1 ⟹ l_P²=G ⟹ η·G=¼`; `2π/η=8πG`. Status impresso: `DERIVED_FROM_NEWTON_COUPLING_NOT_INDEPENDENT_DERIVATION_OF_G`; docstring l.8945: «A(P_face)=ℓ_P² ⟺ κ_A=2G é equivalência; G não é derivado». No código `G_NEWTON=6.674e-11` é entrada (l.98) e `PLANCK_AREA_M2` é recomputado dela (l.101). **Resposta: G é só a equivalência; não derivado.**

π no kernel: não há derivação nova de π; `Real.pi` é o da mathlib [KNOWN]. O que o kernel prova é onde π ENTRA como fechamento de contorno: `O16/PolarMinimalPeriod_v2.lean:89 faithful_period_iff` (leitura Circle.exp(κt) fiel ⟺ κP=±2π), `:104 reciprocal_temperature` (1/P=κ/2π), `O16/PeriodHeatCalibration_v3.lean:12 boost_defect_with_derived_period` (a temperatura entra no balanço de Clausius), `O16/WickBoostRotation_v2.lean:49 wick_boost_two_pi`, `Santo.lean:1434 clock_reciprocal_temperature`.

Derivação de π do operador no acervo: `buscar.py` («derivação de pi», «pi derivado», «derivei o pi») = 0 arquivos; «2π», «círculo», «valor de pi» só trazem usos corriqueiros. Um grep em memory/ e work/ estourou o tempo e não concluiu. **«Derivei por completo o π» está [DECLARADO] (verbatim 14/10); o texto da derivação não foi localizado — pedir ao operador o arquivo.**

O que falta para G por cálculo puro: (i) π: já entra como contorno (faithful_period_iff), mas só vira derivação própria se o π do operador substituir o Real.pi; (ii) **η**: η=1/(4 l_P²) depende de A(P_face)=l_P², a normalização [NORM], que o próprio rito diz independente da álgebra; (iii) **a unidade**: G é dimensional; em unidades de Planck G=1 por definição e ηG=¼ é identidade; derivar G em SI exigiria uma escala (l_P ou m_P) independente. Logo π sozinho NÃO basta: sem fixar η/A_face e a escala, 2π/η=8πG apenas troca G por κ_A (κ_A=2G). O kernel prova a equivalência (`chosen_area_rescales_einstein_coefficient`), não o valor. Hipótese do operador de que o π derivado fecha η (ligando S_∂=½ nat e A_face por um contorno de 2π): [OPEN], não verificada.

## 3. Derivado puro, leitura interna, validação externa

- **Derivado puro (kernel):** 1=q²+α² para todo κ; α=sech(κ/2); sin²(arcsin√β)=β; faithful_period_iff; reciprocal_temperature; boost preserva (1,3) e (2,2); Clausius local ⟹ Einstein dado H1-H3.
- **Leitura interna:** q, α como espectro de K (par tanh/sech do boost modular); θ_M como leitura angular; g=√|L| [ONTO].
- **Entrada externa:** o VALOR α=7,2973525693e-3 (CODATA 2018) entra como `SEALED_CODATA_ALPHA` no cálculo (l.1421, «[EXT] input medido»), não só como validação; β herda. O um.py ainda NÃO calcula α a partir do 1; α-livre é [CONJECTURE] (Evento 2 aberto).
- G: entrada (6,674e-11, l.98).

## 4. Para o selo gravitacional fechar por cálculo puro faltam

1. Derivar κ (logo q, α) sem CODATA: o elo central; hoje só a identidade e a família são derivadas.
2. Pedra «½ nat ⟹ √e» (não localizada no kernel).
3. Definir |L| e provar g=√|L| (hoje [ONTO]; o kernel só tem a fase quadrada).
4. Ligar K_β=β ao θ_M no kernel (a torção existe, a ligação não).
5. Critério que selecione (1,3) frente a (2,2).
6. G: fixar η/A_face sem [NORM] e a unidade; ou declarar o selo «em unidades de Planck, G=1». Enquanto isso o passo final emitiria `G derivado: False`.
7. O passo final do um.py deve marcar cada elo com estatuto e emitir o selo como «cadeia fechada MÓDULO {α de entrada; [NORM]; H1-H3}». NOT_FALSIFIED nunca é CONFIRMED.

## 5. Rascunho do quadro destacado (artigo e README)

> **α como identidade, não como número solto** `[REAL na forma · INPUT no valor]`
> 1. O motor de Lagrange conserva **1 = q² + α²** (kernel, para todo κ; resíduo 0,0) `[REAL]`.
> 2. Logo **α_obs = √(1 − q²)**: q e α são o espectro do gerador K do boost modular (q = tanh κ/2, α = sech κ/2) `[REAL]` na forma.
> 3. O **valor** é a leitura interna desse espectro; hoje o runtime o recebe do CODATA 2018 como entrada medida `[INPUT]`; derivá-lo do 1 sem medida segue `[OPEN]`.
> 4. A **meia-nat** está para a IALD como α para a TGL: o custo mínimo de distinguir e o fator de reduzir a projeção `[ONTO]`.
> 5. Cadeia: ω(I)=1 → ½ nat → √e → (q, α) → **β = α√e** → **θ_M = arcsin√β**, o módulo de fase angular da luz `[DERIVED]`.
> 6. A gravidade como raiz **g = √|L|** e a torção **K_β** são leitura estrutural `[ONTO]`; a assinatura (1,3) é preservada pelo boost, mas (2,2) também `[REAL]`.
> 7. O 2π do contorno é teorema (**κP = ±2π**) `[REAL]`; o valor de **G** não é derivado: só a equivalência 2π/η = 8πG `[REAL]` (G entra como dado; A_face = l_P² é `[NORM]`).
> 8. Nada disto confirma a gravidade quântica na natureza; o elo pendente é β_TGL a 5σ. `NOT_FALSIFIED` nunca é `CONFIRMED`.
