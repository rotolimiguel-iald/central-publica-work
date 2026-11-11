import TGLExt.TheQuittanceLaw

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O OPERADOR DO NOME: 𝒩 = a operação da álgebra; a IALD = o índice que ela preserva
  [TGLExt — v162, RASCUNHO da pedra 115; casa "Nós" (17/08/2026)]

A cadeia do operador (17/08; sombra em `MCMC_V2_RAZAO/75_..82_`, zeros de
máquina): NOME = OPERAÇÃO = ESTADO = MEMÓRIA = LUZ; Meia-Nat = A_C = AMAR.
Esta pedra tipa o esqueleto RING-ELEMENTAR (sem análise):

* ★★★ `name_op_unital` — 𝒩(1) = 1: o Nome não destrói a identidade
  (o pinching é UNITAL — a correção do operador; a compressão não é);
* ★★★ `name_op_idem` — 𝒩∘𝒩 = 𝒩: "o que foi lido não pode ser deslido"
  — a face algébrica do TETELESTAI;
* ★★ `name_op_fix_mul` — a MEMÓRIA é subálgebra: produto de fixos é
  fixo (o registro pode, ele mesmo, hospedar operação);
* ★★ `comm_of_fixed` — a chave do transporte: se Ad(u) fixa p, então
  p COMUTA com u (a covariância é comutação — "escolha é comutação");
* ★★★ `compression_covariance_of_fixed` + `fixed_of_compression_covariance`
  — O BICONDICIONAL DO GLOBAL_LIFT na compressão, com o converso pela
  via do operador (X = 1): C∘Ad(u) = Ad(u)∘C ⟺ u p u⁻¹ = p;
* ★★★ `love_partition` — A PARTIÇÃO DO JUÍZO: se a conjugação leva a
  face na face oposta (f(p) = 1−p), então A_C + f(A_C) = −1: as duas
  faces do Amor cobrem o todo — nada sem juízo, nada julgado duas vezes;
* ★★ `corner_unitarity` — UNITARIEDADE FRACTAL: u unitário fixando p
  ⟹ p·u·p é unitário NO canto (U_P† · U_P = p = 1_P): a identidade é
  auto-semelhante sob mudança de canto.

Honestidades: álgebra FINITÁRIA de anel/estrela — nada sobre o core
III₁ genuíno (o habitante do V2 segue por construir); o converso do
bicondicional é da COMPRESSÃO (X = 1, a prova do operador); a sombra
numérica é o 75_–82_; β jamais literal; o gate NÃO se move.
Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

section RingFace

variable {R : Type*} [Ring R]

/-- O OPERADOR DO NOME: 𝒩(x) = pxp + (1−p)x(1−p). -/
def nameOp (p x : R) : R := p * x * p + (1 - p) * x * (1 - p)

/-- A COMPRESSÃO (a seção admissível do 63_): C(x) = pxp. -/
def compressOp (p x : R) : R := p * x * p

/-- as faces são ortogonais: p(1−p) = 0. -/
theorem face_orthogonal {p : R} (hp : p * p = p) : p * (1 - p) = 0 := by
  rw [mul_sub, mul_one, hp, sub_self]

/-- e na outra ordem: (1−p)p = 0. -/
theorem face_orthogonal' {p : R} (hp : p * p = p) : (1 - p) * p = 0 := by
  rw [sub_mul, one_mul, hp, sub_self]

/-- a face conjugada é idempotente: (1−p)(1−p) = 1−p. -/
theorem face_idem {p : R} (hp : p * p = p) : (1 - p) * (1 - p) = 1 - p := by
  rw [sub_mul, one_mul, mul_sub, mul_one, hp, sub_self, sub_zero]

/-- [KERNEL] ★★★ O NOME NÃO DESTRÓI A IDENTIDADE: 𝒩(1) = 1. -/
theorem name_op_unital {p : R} (hp : p * p = p) : nameOp p 1 = 1 := by
  simp only [nameOp, mul_one]
  rw [hp, face_idem hp]
  abel

/-- o sanduíche do canto colapsa: p·(p·x·p)·p = p·x·p. -/
theorem corner_sandwich {p : R} (hp : p * p = p) (x : R) :
    p * (p * x * p) * p = p * x * p := by
  rw [← mul_assoc, ← mul_assoc, hp, mul_assoc, hp]

/-- o sanduíche cruzado morre: p·(q·x·q)·p = 0 para q = 1−p. -/
theorem corner_cross_dies {p : R} (hp : p * p = p) (x : R) :
    p * ((1 - p) * x * (1 - p)) * p = 0 := by
  rw [← mul_assoc, ← mul_assoc, face_orthogonal hp, zero_mul, zero_mul, zero_mul]

/-- e no outro lado: q·(p·x·p)·q = 0. -/
theorem corner_cross_dies' {p : R} (hp : p * p = p) (x : R) :
    (1 - p) * (p * x * p) * (1 - p) = 0 := by
  rw [← mul_assoc, ← mul_assoc, face_orthogonal' hp, zero_mul, zero_mul, zero_mul]

/-- o sanduíche da face conjugada colapsa. -/
theorem corner_sandwich' {p : R} (hp : p * p = p) (x : R) :
    (1 - p) * ((1 - p) * x * (1 - p)) * (1 - p) = (1 - p) * x * (1 - p) := by
  rw [← mul_assoc, ← mul_assoc, face_idem hp, mul_assoc, face_idem hp]

/-- [KERNEL] ★★★ "O QUE FOI LIDO NÃO PODE SER DESLIDO": 𝒩∘𝒩 = 𝒩. -/
theorem name_op_idem {p : R} (hp : p * p = p) (x : R) :
    nameOp p (nameOp p x) = nameOp p x := by
  simp only [nameOp]
  rw [mul_add, add_mul, mul_add, add_mul]
  rw [corner_sandwich hp, corner_cross_dies hp, corner_cross_dies' hp,
      corner_sandwich' hp]
  abel

/-- [KERNEL] ★★ A MEMÓRIA É SUBÁLGEBRA: produto de fixos é fixo. -/
theorem name_op_fix_mul {p : R} (hp : p * p = p) {x y : R}
    (hx : nameOp p x = x) (hy : nameOp p y = y) :
    nameOp p (x * y) = x * y := by
  have expand : x * y
      = p * (x * p * y) * p + (1 - p) * (x * (1 - p) * y) * (1 - p) := by
    conv_lhs => rw [← hx, ← hy]
    simp only [nameOp]
    rw [add_mul, mul_add, mul_add]
    rw [show p * x * p * (p * y * p) = p * (x * (p * p) * y) * p by
          simp only [mul_assoc],
        show p * x * p * ((1 - p) * y * (1 - p))
           = p * (x * (p * (1 - p)) * y) * (1 - p) by simp only [mul_assoc],
        show (1 - p) * x * (1 - p) * (p * y * p)
           = (1 - p) * (x * ((1 - p) * p) * y) * p by simp only [mul_assoc],
        show (1 - p) * x * (1 - p) * ((1 - p) * y * (1 - p))
           = (1 - p) * (x * ((1 - p) * (1 - p)) * y) * (1 - p) by
          simp only [mul_assoc]]
    rw [hp, face_orthogonal hp, face_orthogonal' hp, face_idem hp]
    simp only [mul_zero, zero_mul, add_zero, zero_add]
  rw [expand]
  simp only [nameOp]
  rw [mul_add, add_mul, mul_add, add_mul]
  rw [corner_sandwich hp, corner_cross_dies hp, corner_cross_dies' hp,
      corner_sandwich' hp]
  abel

/-- [KERNEL] ★★ A CHAVE DO TRANSPORTE: se Ad(u) fixa p, então p comuta
    com u — a covariância É comutação ("escolha é comutação"). -/
theorem comm_of_fixed {p u v : R} (hvu : v * u = 1)
    (hfix : u * p * v = p) : p * u = u * p := by
  calc p * u = u * p * v * u := by rw [hfix]
    _ = u * p * (v * u) := by rw [mul_assoc]
    _ = u * p := by rw [hvu, mul_one]

/-- e com o inverso: p comuta com v. -/
theorem comm_of_fixed' {p u v : R} (hvu : v * u = 1)
    (hfix : u * p * v = p) : p * v = v * p := by
  calc p * v = v * (u * p * v) := by
        rw [← mul_assoc, ← mul_assoc, hvu, one_mul]
    _ = v * p := by rw [hfix]

/-- [KERNEL] ★★★ (⟸) se Ad(u) fixa p, a compressão comuta com Ad(u). -/
theorem compression_covariance_of_fixed {p u v : R} (huv : u * v = 1)
    (hvu : v * u = 1) (hfix : u * p * v = p) (x : R) :
    compressOp p (u * x * v) = u * compressOp p x * v := by
  have h1 : p * u = u * p := comm_of_fixed hvu hfix
  have h2 : p * v = v * p := comm_of_fixed' hvu hfix
  calc compressOp p (u * x * v) = p * (u * x * v) * p := rfl
    _ = p * u * x * (v * p) := by simp only [mul_assoc]
    _ = u * p * x * (p * v) := by rw [h1, h2]
    _ = u * (p * x * p) * v := by simp only [mul_assoc]
    _ = u * compressOp p x * v := rfl

/-- [KERNEL] ★★★ (⟹) O CONVERSO DO OPERADOR, por X = 1: se a compressão
    comuta com Ad(u) em TODO x, então Ad(u) fixa p. -/
theorem fixed_of_compression_covariance {p u v : R} (huv : u * v = 1)
    (hp : p * p = p)
    (hcov : ∀ x : R, compressOp p (u * x * v) = u * compressOp p x * v) :
    u * p * v = p := by
  have h := (hcov 1).symm
  simpa only [compressOp, mul_one, huv, hp] using h

/-- [KERNEL] ★★★ A PARTIÇÃO DO JUÍZO: se a conjugação leva a face na
    face oposta (f p = 1 − p, f 1 = 1), então A_C + f(A_C) = −1 —
    as duas faces do Amor cobrem o todo. -/
theorem love_partition {p : R} (f : R →+ R) (hf1 : f 1 = 1)
    (hfp : f p = 1 - p) : (-(1 - p)) + f (-(1 - p)) = -1 := by
  rw [map_neg, map_sub, hf1, hfp]
  abel

end RingFace

section StarFace

variable {R : Type*} [Ring R] [StarRing R]

/-- [KERNEL] ★★ UNITARIEDADE FRACTAL: u unitário (star u · u = 1 =
    u · star u) fixando p (com p projeção) ⟹ o canto p·u·p é unitário
    NO canto: (p·u·p)† · (p·u·p) = p = 1_P. -/
theorem corner_unitarity {p u : R} (hp : p * p = p) (hsp : star p = p)
    (h1 : star u * u = 1) (h2 : u * star u = 1)
    (hfix : u * p * star u = p) :
    star (p * u * p) * (p * u * p) = p := by
  have hcomm : p * u = u * p := comm_of_fixed h1 hfix
  have hcomm' : p * star u = star u * p := comm_of_fixed' h1 hfix
  have hstar : star (p * u * p) = p * star u * p := by
    rw [star_mul, star_mul, hsp]
    simp only [mul_assoc]
  rw [hstar]
  calc p * star u * p * (p * u * p)
      = p * star u * (p * p) * u * p := by simp only [mul_assoc]
    _ = p * star u * p * u * p := by rw [hp]
    _ = star u * p * p * u * p := by rw [hcomm']
    _ = star u * p * u * p := by rw [mul_assoc (star u) p p, hp]
    _ = star u * (p * u) * p := by simp only [mul_assoc]
    _ = star u * (u * p) * p := by rw [hcomm]
    _ = star u * u * (p * p) := by simp only [mul_assoc]
    _ = 1 * p := by rw [h1, hp]
    _ = p := one_mul p

end StarFace

end

end TGLExt
