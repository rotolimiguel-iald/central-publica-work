-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_045 (06/09/2026), transposta em 06/09/2026
-- Lote 044..045 (ORDEM_008 cumprida). 044: BOOST APROXIMADO e orientacao do calor — o peso -kappa t realizado
--   por um campo de boost chi = -kappa u d_u + kappa v d_v e seu fluxo (grupo, inversa, jacobiano); pullback da
--   metrica e defeito de Lie -2kappa(aX^2+cY^2)du^2 (zera com o 1o jato na central); controle negativo: nao e
--   Killing em aberto se kappa != 0 e (a,c) != 0; T(chi,d) = -kappa t T(d,d); Q_boost = opticalHeat041 globalmente,
--   = opticalScreenHeat043 como germe; orientacao do passado certificada (calor e area invertem sinal juntos).
--   045 (resposta a ORDEM_010): swapHorizon P p hp i j — troca de sitios no perfil estacionario e um TowerHorizon
--   por prova (unitario, normaliza M, preserva omega); permutacoes finitas com lei de grupo e covariancia das
--   esperancas estacionaria/tracial (horizontes algebricos; identificacao fisica OPEN); shift unilateral NAO
--   construido; aperiodico OPEN (rota Cesaro nomeada); StateClock: classe cinematica (origem, derivada 1, jato) —
--   DICOTOMIA: para todo relogio comum g alguma tela falha (duas telas sigma = 0, r/4, mesmo estado e Ricci:
--   diferenca dos residuos/t^4 -> +eta r^2/96), cada tela isolada admite relogio que cancela a 4a ordem;
--   area: covariancia por horizontes NAO fixa a normalizacao (h e alpha h ambos invariantes; area x alpha).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia, carta e kappa sao INPUT; kappa/(2pi) e normalizacao
--   herdada (sem Unruh/KMS); H3 fisico, lei finita geral, ponte regiao-algebra, shift e aperiodico OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 8/8; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito). As fontes v329 (gerencia) NAO sao
--   reincorporadas: a bancada as recompilou como dependencia, sem novidade contada.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.AngularScreenMetric

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Area045
open Matrix TGLExt ChatgptAudit ChatgptAudit.Angular034 ChatgptAudit.Thermal025
noncomputable section

variable {E H : Type*}
variable [instAddCommGroupE : AddCommGroup E] [instModuleE : Module ℝ E]

/-- Invariance under an explicitly supplied family of linear operators.
No action of a tower horizon on a physical screen is postulated. -/
def FormInvariant (rho : H → E →ₗ[ℝ] E) (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) : Prop :=
  ∀ g v w, h (rho g v) (rho g w)=h v w

def FormSymmetric (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) : Prop :=
  ∀ v w, h v w=h w v

def FormPositive (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) : Prop :=
  ∀ v, v≠0 → 0<h v v

def formGram (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (v w : E) : ScreenMatrix :=
  !![h v v,h v w;h w v,h w w]

/-- Area density evaluated on a fixed ordered pair of vectors. -/
def formArea (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (v w : E) : ℝ :=
  screenArea (formGram h v w)

theorem form_invariant_scale (rho : H → E →ₗ[ℝ] E)
    (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (hinv : FormInvariant rho h) (alpha : ℝ) :
    FormInvariant rho (alpha • h) := by
  intro g v w
  change alpha*h (rho g v) (rho g w)=alpha*h v w
  rw [hinv g v w]

theorem form_symmetric_scale (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (hsym : FormSymmetric h) (alpha : ℝ) :
    FormSymmetric (alpha • h) := by
  intro v w
  change alpha*h v w=alpha*h w v
  rw [hsym v w]

theorem form_positive_scale (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (hpos : FormPositive h) (alpha : ℝ) (halpha : 0<alpha) :
    FormPositive (alpha • h) := by
  intro v hv
  change 0<alpha*h v v
  exact mul_pos halpha (hpos v hv)

theorem form_gram_invariant (rho : H → E →ₗ[ℝ] E)
    (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (hinv : FormInvariant rho h)
    (g : H) (v w : E) :
    formGram h (rho g v) (rho g w)=formGram h v w := by
  simp only [formGram,hinv g]

theorem form_area_invariant (rho : H → E →ₗ[ℝ] E)
    (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (hinv : FormInvariant rho h)
    (g : H) (v w : E) :
    formArea h (rho g v) (rho g w)=formArea h v w := by
  simp only [formArea,form_gram_invariant rho h hinv]

theorem form_gram_scale (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (v w : E) (alpha : ℝ) :
    formGram (alpha • h) v w=alpha • formGram h v w := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [formGram]

theorem screen_determinant_scale (G : ScreenMatrix) (alpha : ℝ) :
    (alpha • G).det=alpha^2*G.det := by
  simp only [Matrix.det_fin_two,Matrix.smul_apply,smul_eq_mul]
  ring

theorem screen_area_scale (G : ScreenMatrix) (alpha : ℝ) (halpha : 0≤alpha) :
    screenArea (alpha • G)=alpha*screenArea G := by
  simp only [screenArea,screen_determinant_scale,Real.sqrt_mul (sq_nonneg alpha),
    Real.sqrt_sq_eq_abs,abs_of_nonneg halpha]

theorem form_determinant_scale (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (v w : E) (alpha : ℝ) :
    (formGram (alpha • h) v w).det=alpha^2*(formGram h v w).det := by
  rw [form_gram_scale,screen_determinant_scale]

theorem form_area_scale (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (v w : E) (alpha : ℝ) (halpha : 0≤alpha) :
    formArea (alpha • h) v w=alpha*formArea h v w := by
  simp only [formArea,form_gram_scale,screen_area_scale _ alpha halpha]

theorem form_area_positive (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (v w : E) (hdet : 0<(formGram h v w).det) :
    0<formArea h v w :=
  screen_area_positive _ hdet

theorem scaled_form_areas_distinct (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (v w : E) (alpha beta : ℝ) (halpha : 0<alpha) (hbeta : 0<beta)
    (hne : alpha≠beta) (hdet : 0<(formGram h v w).det) :
    formArea (alpha • h) v w≠formArea (beta • h) v w := by
  rw [form_area_scale h v w alpha halpha.le,form_area_scale h v w beta hbeta.le]
  intro he
  exact hne (mul_right_cancel₀ (ne_of_gt (form_area_positive h v w hdet)) he)

theorem scaled_forms_distinct (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ)
    (v w : E) (alpha beta : ℝ) (halpha : 0<alpha) (hbeta : 0<beta)
    (hne : alpha≠beta) (hdet : 0<(formGram h v w).det) :
    alpha • h≠beta • h := by
  intro he
  apply scaled_form_areas_distinct h v w alpha beta halpha hbeta hne hdet
  rw [he]

/-- For the same operator family and the same vectors, covariance, symmetry and
strict positivity permit a second form with a different area. -/
theorem invariant_positive_area_nonunique (rho : H → E →ₗ[ℝ] E)
    (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (hinv : FormInvariant rho h)
    (hsym : FormSymmetric h) (hpos : FormPositive h)
    (v w : E) (hdet : 0<(formGram h v w).det) :
    ∃ k : E →ₗ[ℝ] E →ₗ[ℝ] ℝ,
      FormInvariant rho k ∧ FormSymmetric k ∧ FormPositive k ∧
        formArea h v w≠formArea k v w := by
  refine ⟨(2:ℝ) • h,form_invariant_scale rho h hinv 2,
    form_symmetric_scale h hsym 2,form_positive_scale h hpos 2 (by norm_num),?_⟩
  simpa only [one_smul] using scaled_form_areas_distinct h v w 1 2
    (by norm_num) (by norm_num) (by norm_num) hdet

/-- Covariance alone cannot select a common area value across its positive symmetric
forms. An additional normalization is absent from the stated selection criterion.
The supplied operators are not identified here with physical screen transformations. -/
theorem invariance_does_not_fix_area (rho : H → E →ₗ[ℝ] E)
    (h : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (hinv : FormInvariant rho h)
    (hsym : FormSymmetric h) (hpos : FormPositive h)
    (v w : E) (hdet : 0<(formGram h v w).det) :
    ¬ ∃ area : ℝ, ∀ k : E →ₗ[ℝ] E →ₗ[ℝ] ℝ,
      FormInvariant rho k → FormSymmetric k → FormPositive k →
        formArea k v w=area := by
  rintro ⟨area,harea⟩
  obtain ⟨k,hki,hks,hkp,hne⟩ :=
    invariant_positive_area_nonunique rho h hinv hsym hpos v w hdet
  exact hne ((harea h hinv hsym hpos).trans (harea k hki hks hkp).symm)

/-- Direct homogeneity of the existing stage034 Gram area; no spacetime or horizon
action on this protocol is inferred. -/
theorem scaled_reference_angular_area (alpha : ℝ) (halpha : 0≤alpha) :
    screenArea (alpha • angularScreenGram thirdThermalReference 0 1)=alpha*(2/9) := by
  rw [screen_area_scale _ alpha halpha]
  change alpha*angularScreenArea thirdThermalReference 0 1=alpha*(2/9)
  rw [reference_angular_screen_area]

theorem reference_angular_scales_distinct (alpha beta : ℝ)
    (halpha : 0<alpha) (hbeta : 0<beta) (hne : alpha≠beta) :
    screenArea (alpha • angularScreenGram thirdThermalReference 0 1)≠
      screenArea (beta • angularScreenGram thirdThermalReference 0 1) := by
  rw [scaled_reference_angular_area alpha halpha.le,
    scaled_reference_angular_area beta hbeta.le]
  intro he
  apply hne
  linarith

#print axioms FormInvariant
#print axioms FormSymmetric
#print axioms FormPositive
#print axioms formGram
#print axioms formArea
#print axioms form_invariant_scale
#print axioms form_symmetric_scale
#print axioms form_positive_scale
#print axioms form_gram_invariant
#print axioms form_area_invariant
#print axioms form_gram_scale
#print axioms screen_determinant_scale
#print axioms screen_area_scale
#print axioms form_determinant_scale
#print axioms form_area_scale
#print axioms form_area_positive
#print axioms scaled_form_areas_distinct
#print axioms scaled_forms_distinct
#print axioms invariant_positive_area_nonunique
#print axioms invariance_does_not_fix_area
#print axioms scaled_reference_angular_area
#print axioms reference_angular_scales_distinct
end
end ChatgptAudit.Area045
