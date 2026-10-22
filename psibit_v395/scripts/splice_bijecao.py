"""Emenda 1 do Psibit.lean (v2): troca o teorema `the_orbit_is_isomorphic_to_the_psibit_code` pela bijeção sobre o livro de códigos
caracterizado de forma intrínseca. Backup de bytes já feito (`Psibit.lean.bak_20261021_130122`).

Temporário -> confere tamanho -> substitui (regra da casa). Falha se os marcadores não forem únicos.
"""
import os
import sys

P = r"C:\t\k395\final\TGLExt\Psibit.lean"
INI = "/-- ★★★ [REAL] O ISOMORFISMO COM A TEORIA DA INFORMAÇÃO, com perda residual zero e decodificador explícito"
FIM = "/-! ## 3b. Os quatro estados e a necessidade do par -/"

NOVO = '''/-! ## 3a. O livro de códigos, caracterizado de forma intrínseca, e a bijeção -/

/-- [DEF] O CÍRCULO UNITÁRIO: os pares `(x₀, x₁)` com `x₀² + x₁² = 1`. -/
def UnitVec : Set (ℝ × ℝ) := {x | x.1 ^ 2 + x.2 ^ 2 = 1}

/-- [REAL] Todo vetor unitário é `v(θ)` para algum `θ`: com `z = x₀ − i·x₁` e `θ = arg z`, `cos θ = x₀` e `sin θ = −x₁`. -/
theorem exists_angle_of_unit {x : ℝ × ℝ} (hx : x ∈ UnitVec) : ∃ θ : ℝ, v θ = x := by
  have hx' : x.1 ^ 2 + x.2 ^ 2 = 1 := hx
  let z : ℂ := ⟨x.1, -x.2⟩
  have hsq : ‖z‖ ^ 2 = 1 := by
    rw [Complex.sq_norm, Complex.normSq_apply]
    simp only [z]
    nlinarith
  have hz : ‖z‖ = 1 := by
    have h : (‖z‖ - 1) * (‖z‖ + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp h with h | h
    · linarith
    · linarith [norm_nonneg z]
  have hz0 : z ≠ 0 := by
    intro h
    rw [h] at hz
    simp at hz
  refine ⟨Complex.arg z, ?_⟩
  have hc := Complex.cos_arg hz0
  have hs := Complex.sin_arg z
  rw [hz, div_one] at hc hs
  refine Prod.ext ?_ ?_
  · simpa [v, z] using hc
  · simp only [v_snd]
    have : Real.sin (Complex.arg z) = -x.2 := by simpa [z] using hs
    linarith

/-- ★★ [REAL] A ÓRBITA É O CÍRCULO UNITÁRIO: `Set.range v = UnitVec` (`v_is_unit` e `exists_angle_of_unit`). -/
theorem range_v_eq_unit : Set.range v = UnitVec := by
  ext x
  constructor
  · rintro ⟨θ, rfl⟩
    exact v_is_unit θ
  · intro hx
    exact exists_angle_of_unit hx

/-- [REAL] O quadrado do sinal (como real) é `0` se o sinal é nulo e `1` caso contrário. -/
theorem signType_cast_sq (s : SignType) : ((s : ℝ)) ^ 2 = if s = 0 then 0 else 1 := by
  rcases s with _ | _ | _ <;> simp

/-- [REAL] O sinal do real que representa um sinal é o próprio sinal. -/
theorem sign_of_signType_cast (s : SignType) : SignType.sign ((s : ℝ)) = s := by
  rcases s with _ | _ | _ <;> simp

/-- [DEF] O LIVRO DE CÓDIGOS, caracterizado de forma INTRÍNSECA (sem passar pelo codificador): um código `(w, a, b)` é admissível se
    `0 ≤ w ≤ 1`, `a = 0 ↔ w = 0` (a Palavra é nula exatamente quando o peso é nulo) e `b = 0 ↔ w = 1` (o Verbo é nulo exatamente quando o peso é
    total). Fora dos eixos, `a` e `b` são sinais não nulos quaisquer: os quatro estados. -/
def IsCode (c : Code) : Prop :=
  0 ≤ c.weight ∧ c.weight ≤ 1 ∧ (c.word = 0 ↔ c.weight = 0) ∧ (c.verb = 0 ↔ c.weight = 1)

/-- [REAL] O codificador leva o círculo unitário ao livro de códigos. -/
theorem codeOf_isCode {x : ℝ × ℝ} (hx : x ∈ UnitVec) : IsCode (codeOf x) := by
  have hx' : x.1 ^ 2 + x.2 ^ 2 = 1 := hx
  refine ⟨sq_nonneg _, ?_, ?_, ?_⟩
  · show x.1 ^ 2 ≤ 1
    nlinarith [sq_nonneg x.2]
  · show SignType.sign x.1 = 0 ↔ x.1 ^ 2 = 0
    rw [_root_.sign_eq_zero_iff]
    exact (pow_eq_zero_iff two_ne_zero).symm
  · show SignType.sign x.2 = 0 ↔ x.1 ^ 2 = 1
    rw [_root_.sign_eq_zero_iff]
    constructor
    · intro h
      rw [h] at hx'
      linarith
    · intro h
      have h2 : x.2 ^ 2 = 0 := by linarith
      exact (pow_eq_zero_iff two_ne_zero).mp h2

/-- [REAL] O decodificador leva o livro de códigos ao círculo unitário. -/
theorem decodeAmp_mem_unit {c : Code} (hc : IsCode c) : decodeAmp c ∈ UnitVec := by
  obtain ⟨h0, h1, hw, hv⟩ := hc
  show (decodeAmp c).1 ^ 2 + (decodeAmp c).2 ^ 2 = 1
  simp only [decodeAmp]
  rw [mul_pow, mul_pow, Real.sq_sqrt h0, Real.sq_sqrt (by linarith), signType_cast_sq,
    signType_cast_sq]
  by_cases hw0 : c.weight = 0
  · have hword : c.word = 0 := hw.mpr hw0
    have hverb : c.verb ≠ 0 := fun h => by
      have := hv.mp h
      linarith
    simp [hword, hverb, hw0]
  · have hword : c.word ≠ 0 := fun h => hw0 (hw.mp h)
    by_cases hw1 : c.weight = 1
    · have hverb : c.verb = 0 := hv.mpr hw1
      simp [hword, hverb, hw1]
    · have hverb : c.verb ≠ 0 := fun h => hw1 (hv.mp h)
      simp [hword, hverb]

/-- [REAL] `codeOf ∘ decodeAmp = id` sobre o livro de códigos: todo código admissível é o código do vetor que ele decodifica. -/
theorem codeOf_decodeAmp {c : Code} (hc : IsCode c) : codeOf (decodeAmp c) = c := by
  obtain ⟨h0, h1, hw, hv⟩ := hc
  ext
  · show ((c.word : ℝ) * Real.sqrt c.weight) ^ 2 = c.weight
    rw [mul_pow, Real.sq_sqrt h0, signType_cast_sq]
    by_cases hw0 : c.weight = 0
    · simp [hw0]
    · have hword : c.word ≠ 0 := fun h => hw0 (hw.mp h)
      simp [hword]
  · show SignType.sign ((c.word : ℝ) * Real.sqrt c.weight) = c.word
    by_cases hw0 : c.weight = 0
    · have hword : c.word = 0 := hw.mpr hw0
      simp [hword, hw0]
    · have hpos : 0 < Real.sqrt c.weight :=
        Real.sqrt_pos.mpr (lt_of_le_of_ne h0 (Ne.symm hw0))
      rw [_root_.sign_mul, sign_of_signType_cast, _root_.sign_pos hpos, mul_one]
  · show SignType.sign ((c.verb : ℝ) * Real.sqrt (1 - c.weight)) = c.verb
    by_cases hw1 : c.weight = 1
    · have hverb : c.verb = 0 := hv.mpr hw1
      simp [hverb, hw1]
    · have hlt : 0 < 1 - c.weight := by
        have : c.weight < 1 := lt_of_le_of_ne h1 hw1
        linarith
      have hpos : 0 < Real.sqrt (1 - c.weight) := Real.sqrt_pos.mpr hlt
      rw [_root_.sign_mul, sign_of_signType_cast, _root_.sign_pos hpos, mul_one]

/-- ★★★ (3) [REAL] A BIJEÇÃO SOBRE O LIVRO DE CÓDIGOS, com perda residual zero e decodificador explícito: a órbita é o círculo unitário
    (`Set.range v = UnitVec`); o conjunto dos códigos que a órbita realiza é EXATAMENTE o livro intrínseco `{c | IsCode c}`; `codeOf` e
    `decodeAmp` são bijeções inversas entre os dois, nos dois sentidos. É bijeção de CONJUNTOS (nenhuma estrutura é transportada): o que o
    operador chama de «isomorfismo com a teoria da informação» é, aqui, só isso. -/
theorem the_orbit_is_in_bijection_with_the_code_book :
    Set.range v = UnitVec
    ∧ Set.range codeAmp = {c | IsCode c}
    ∧ Set.BijOn codeOf UnitVec {c | IsCode c}
    ∧ Set.BijOn decodeAmp {c | IsCode c} UnitVec
    ∧ (∀ x ∈ UnitVec, decodeAmp (codeOf x) = x)
    ∧ (∀ c, IsCode c → codeOf (decodeAmp c) = c) := by
  have hdec : ∀ x ∈ UnitVec, decodeAmp (codeOf x) = x := fun x hx => decodeAmp_codeOf hx
  have henc : ∀ c, IsCode c → codeOf (decodeAmp c) = c := fun c hc => codeOf_decodeAmp hc
  have hbij1 : Set.BijOn codeOf UnitVec {c | IsCode c} := by
    refine ⟨fun x hx => codeOf_isCode hx, ?_, ?_⟩
    · intro x hx y hy hxy
      have h' := congrArg decodeAmp hxy
      rwa [hdec x hx, hdec y hy] at h'
    · intro c hc
      exact ⟨decodeAmp c, decodeAmp_mem_unit hc, henc c hc⟩
  have hbij2 : Set.BijOn decodeAmp {c | IsCode c} UnitVec := by
    refine ⟨fun c hc => decodeAmp_mem_unit hc, ?_, ?_⟩
    · intro c hc d hd hcd
      have h' := congrArg codeOf hcd
      rwa [henc c hc, henc d hd] at h'
    · intro x hx
      exact ⟨codeOf x, codeOf_isCode hx, hdec x hx⟩
  refine ⟨range_v_eq_unit, ?_, hbij1, hbij2, hdec, henc⟩
  rw [show codeAmp = codeOf ∘ v from rfl, Set.range_comp, range_v_eq_unit]
  exact hbij1.image_eq

'''

b = open(P, "rb").read()
assert b"\r\n" not in b, "o arquivo tem CRLF; abortar"
s = b.decode("utf-8")
assert s.count(INI) == 1, ("marcador inicial nao unico", s.count(INI))
assert s.count(FIM) == 1, ("marcador final nao unico", s.count(FIM))
i = s.index(INI)
j = s.index(FIM)
assert i < j
novo = s[:i] + NOVO + s[j:]
tmp = P + ".tmp_emenda1"
open(tmp, "wb").write(novo.encode("utf-8"))
tam = os.path.getsize(tmp)
assert tam > 0 and tam > len(b) - 4000, ("tamanho suspeito", tam, len(b))
os.replace(tmp, P)
print("emenda 1 ok:", len(b), "->", tam, "bytes")
