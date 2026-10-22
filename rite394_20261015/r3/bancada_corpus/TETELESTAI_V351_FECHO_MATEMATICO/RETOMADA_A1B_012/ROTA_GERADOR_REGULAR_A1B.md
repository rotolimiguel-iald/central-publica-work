[OPEN — roteiro do próximo fornecedor; as identidades abaixo ainda não são um novo teorema Lean]

# A1(b): gerador positivo regular, sem reconstruir Fourier ou L²

2026-09-14T18:12:25.297959-03:00

O alvo restante é `regular_unitary_positive_generator` de LACUNAS_A1.md:31. O consumidor final é a perturbação de `scalarDualWeight` que deve habitar `TGLV351.RegularCoreTraceData`; o objeto vive no Hilbert REGULAR, não apenas na torre e não apenas no GNS do peso. Esta nota registra fornecedores localizados. Não autoriza saltar a ficha de seis modalidades antes do próximo delta Lean.

## Convenções e candidato a testar

No código existente, `(S_t f)(x)=f(x-t)`, `Λ_t=fibre(Δ_base^{it}) S_t`, e a Fourier usa `exp(-2π i x ξ)`. Ponha formalmente `(Wf)(x)=Δ_base^{ix}f(x)`. O cálculo pontual dá

```
W S_t W* f(x) = Δ_base^{ix} Δ_base^{-i(x-t)} f(x-t)
              = Δ_base^{it} f(x-t) = Λ_t f(x).
F S_t F* = multiplicação por exp(-2π i t ξ).
h = W F* M[exp(-2π ξ)] F W*.
```

Essas são identidades de planejamento a transportar para classes L², domínios e operadores da casa. A primeira demanda construir o campo unitário usando `operatorFieldLift`; a segunda demanda aplicar a identidade de translação Fourier na classe L², com extensão densa, reaproveitando `fourier_integral_ae_eq_L2` ou o fornecedor Schwartz. A Fourier isométrica em L² já está definida na mathlib; não se deve reconstruí-la.

Para reutilizar a maquinaria limitada de resolventes, o candidato é

```
g(ξ)=1/(1+exp(-2πξ)),   0<g(ξ)<1,
R = W F* M[g] F W*,
h = (1-R)/R, no domínio Ran(R).
```

`resolventGraphOperator` e o cálculo funcional das potências imaginárias já existem. A expressão quociente acima NÃO significa inversa limitada: R e 1-R podem ser injetivos sem gap. Precisam ser demonstradas a igualdade das potências com Λ_t, a afiliação ao MESMO N e a não singularidade. A afiliação pode ser abordada pela comutação com N′, usando os fornecedores de localidade dos caracteres; esta nota não afirma que essa passagem já foi paga.

## Sinal da ação dual

Com `C_s f(x)=exp(-isx)f(x)`, o campo W comuta pontualmente com C_s. Na Fourier, C_s desloca a função para `ξ+s/(2π)`. Logo o candidato a h transforma por `exp(-2π(ξ+s/(2π)))=exp(-s)exp(-2πξ)`. Essa conta confere o sinal exigido de θ_s(h). O domínio transformado e a igualdade de operadores não limitados ainda precisam de prova. Se L=log h, o deslocamento esperado é L−s; para K=−log h, K+s.

## O que isso não fecha

O traço continua sem habitante: falta construir a perturbação pelo inverso do gerador e provar fidelidade, normalidade, semifinitude por minorantes, aditividade, homogeneidade, tracialidade e escala. O peso dual existente é invariante pela ação dual; não pode ser renomeado como traço de peso −1. O novo teorema de ação no GNS (ainda em aceitação isolada) fornece uma ligação real, sem suprir esses campos por comentário.

## Fornecedores localizados, em bytes e tipos

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:16` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
def regularUnitary (P : SiteProfile) (t : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2Translation.lean:19` — `1fc45298e186caf37d2b04779e64f3e000e7384511bede3bdce57ab9b429b267`

```lean
theorem shift_ae (t : ℝ) (f : RegularHilbert H) :
    shift t f =ᵐ[volume] fun x : ℝ => f (x-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:64` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
def operatorFieldLift (F : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:57` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_star (F G : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:33` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\LpSpace.lean:50` — `82b647b1998edea8d60ac8f986fd5735d697044e586464a05d71d0a346522cfe`

```lean
def fourierTransformₗᵢ : (Lp (α
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FourierL1L2.lean:26` — `49c8e43b55cbd48b3a2c9f1bdfa01a31af9566e7a3cccbb4eed119fc1c750f13`

```lean
theorem fourier_integral_ae_eq_L2 (f : ℝ → H) (hf1 : Integrable f) (hf2 : MemLp f 2) :
    (𝓕 f) =ᵐ[volume] (𝓕 (hf2.toLp f) : Lp (α
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:45` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_injective (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (hpos : ∀ s, 0 < g s) :
    Function.Injective (realScalarMultiplier (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CharacterLocality.lean:40` — `7a5d2f1b70b3d61307045c4460034e3821976c8b30b02d5bcf165d157f33419a`

```lean
theorem character_commutation_local_pairing
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (f g : RegularHilbert H) :
    (fun x : ℝ => inner ℂ ((B.adjoint f) x) (g x)) =ᵐ[volume]
      (fun x : ℝ => inner ℂ (f x) ((B g) x))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FixedCoreLocality.lean:16` — `b5cb6a24e5cc2ca221741f9e8dbb4ccc2361b7a7729886d2ab80ed723b1984a8`

```lean
theorem character_commutation_measurableCut
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (S : Set ℝ) (hS : MeasurableSet S) :
    measurableCut S hS * B = B * measurableCut S hS
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:13` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
def resolventGraphOperator (R : H →L[ℂ] H) (hi : Function.Injective R) : H →ₗ.[ℂ] H
```

