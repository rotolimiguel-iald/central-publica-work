-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.LikelihoodCocycleControls

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.UnitaryDuhamel
open TGLExt Filter Topology Set NormedSpace
noncomputable section

local instance operatorRationalAlgebra (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance operatorRationalTower (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

abbrev Operator (P : SiteProfile) := TowerHilbert P →L[ℂ] TowerHilbert P

def evolution {P : SiteProfile} (A : Operator P) (t : ℝ) : Operator P :=
  NormedSpace.exp (((t : ℂ) * Complex.I) • A)

theorem evolution_zero {P : SiteProfile} (A : Operator P) : evolution A 0 = 1 := by
  simp [evolution]

theorem evolution_unitary {P : SiteProfile} (A : Operator P)
    (hA : IsSelfAdjoint A) (t : ℝ) : evolution A t ∈ unitary _ :=
  NormedSpace.exp_mem_unitary_of_mem_skewAdjoint
    (hA.smul_mem_skewAdjoint
      (by simp : star ((t : ℂ)*Complex.I) = -((t : ℂ)*Complex.I)))

theorem evolution_add {P : SiteProfile} (A : Operator P) (s t : ℝ) :
    evolution A (s+t) = evolution A s * evolution A t := by
  have h : Commute (((s : ℂ)*Complex.I) • A) (((t : ℂ)*Complex.I) • A) :=
    ((Commute.refl A).smul_left _).smul_right _
  unfold evolution
  rw [← NormedSpace.exp_add_of_commute h, ← add_smul]
  congr 2
  push_cast
  ring

theorem evolution_neg_mul {P : SiteProfile} (A : Operator P) (t : ℝ) :
    evolution A (-t) * evolution A t = 1 := by
  rw [← evolution_add, neg_add_cancel, evolution_zero]

theorem evolution_mul_neg {P : SiteProfile} (A : Operator P) (t : ℝ) :
    evolution A t * evolution A (-t) = 1 := by
  rw [← evolution_add, add_neg_cancel, evolution_zero]

theorem evolution_star {P : SiteProfile} (A : Operator P)
    (hA : IsSelfAdjoint A) (t : ℝ) : star (evolution A t) = evolution A (-t) := by
  simp only [evolution, NormedSpace.star_exp, star_smul, hA.star_eq,
    star_mul, Complex.star_def, Complex.conj_ofReal, Complex.conj_I,
    Complex.ofReal_neg, neg_mul]
  congr 1
  congr 1
  ring

theorem evolution_continuous {P : SiteProfile} (A : Operator P) :
    Continuous (evolution A) := by
  unfold evolution
  fun_prop

theorem evolution_derivative_right {P : SiteProfile} (A : Operator P) (t : ℝ) :
    HasDerivAt (evolution A) (evolution A t * (Complex.I • A)) t := by
  have h := hasDerivAt_exp_smul_const (Complex.I • A) t
  have he : (fun r : ℝ => NormedSpace.exp (r • (Complex.I • A))) = evolution A := by
    funext r
    rw [← smul_assoc, Complex.real_smul]
    rfl
  rw [he, congrFun he t] at h
  exact h

theorem evolution_derivative_left {P : SiteProfile} (A : Operator P) (t : ℝ) :
    HasDerivAt (evolution A) ((Complex.I • A) * evolution A t) t := by
  have h := hasDerivAt_exp_smul_const' (Complex.I • A) t
  have he : (fun r : ℝ => NormedSpace.exp (r • (Complex.I • A))) = evolution A := by
    funext r
    rw [← smul_assoc, Complex.real_smul]
    rfl
  rw [he, congrFun he t] at h
  exact h

def interpolation {P : SiteProfile} (A B : Operator P) (t r : ℝ) : Operator P :=
  evolution A r * evolution B (t-r)

theorem interpolation_derivative {P : SiteProfile} (A B : Operator P) (t r : ℝ) :
    HasDerivAt (interpolation A B t)
      (evolution A r * (Complex.I • (A-B)) * evolution B (t-r)) r := by
  have hc : HasDerivAt (fun z : ℝ => t-z) (0-1 : ℝ) r :=
    (hasDerivAt_const r t).sub (hasDerivAt_id r)
  have hd := (evolution_derivative_left B (t-r)).scomp r hc
  have hp := (evolution_derivative_right A r).mul hd
  convert! hp using 1
  simp only [Function.comp_apply, zero_sub, neg_smul, one_smul, smul_sub,
    mul_neg, mul_sub, sub_mul]
  noncomm_ring

theorem interpolation_derivative_norm {P : SiteProfile} (A B : Operator P)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (t r : ℝ) :
    ‖evolution A r * (Complex.I • (A-B)) * evolution B (t-r)‖ = ‖A-B‖ := by
  rw [CStarRing.norm_mul_mem_unitary _ (evolution_unitary B hB (t-r)),
    CStarRing.norm_mem_unitary_mul _ (evolution_unitary A hA r),
    norm_smul, Complex.norm_I, one_mul]

/-- The estimate has no commutation hypothesis and no exponential norm loss. -/
theorem unitary_duhamel_bound {P : SiteProfile} (A B : Operator P)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (t : ℝ) :
    ‖evolution A t - evolution B t‖ ≤ ‖A-B‖ * |t| := by
  have hd (r : ℝ) (_ : r ∈ (Set.univ : Set ℝ)) :=
    (interpolation_derivative A B t r).hasDerivWithinAt (s := Set.univ)
  have hn (r : ℝ) (_ : r ∈ (Set.univ : Set ℝ)) :
      ‖evolution A r * (Complex.I • (A-B)) * evolution B (t-r)‖ ≤ ‖A-B‖ :=
    le_of_eq (interpolation_derivative_norm A B hA hB t r)
  have h := Convex.norm_image_sub_le_of_norm_hasDerivWithin_le hd hn
    (convex_univ : Convex ℝ (Set.univ : Set ℝ)) (Set.mem_univ (0 : ℝ)) (Set.mem_univ t)
  simpa only [interpolation, evolution_zero, sub_self, sub_zero, one_mul, mul_one,
    Real.norm_eq_abs] using h

#print axioms operatorRationalAlgebra
#print axioms operatorRationalTower
#print axioms Operator
#print axioms evolution
#print axioms evolution_zero
#print axioms evolution_unitary
#print axioms evolution_add
#print axioms evolution_neg_mul
#print axioms evolution_mul_neg
#print axioms evolution_star
#print axioms evolution_continuous
#print axioms evolution_derivative_right
#print axioms evolution_derivative_left
#print axioms interpolation
#print axioms interpolation_derivative
#print axioms interpolation_derivative_norm
#print axioms unitary_duhamel_bound
end
end ChatgptAudit.UnitaryDuhamel
