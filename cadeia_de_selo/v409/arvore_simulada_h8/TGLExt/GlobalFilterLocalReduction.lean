-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_039 (06/09/2026), transposta em 06/09/2026
-- Lote 039..041 (ORDEM_008 cumprida: zero instancias anonimas; lote compilado junto em diretorio limpo).
--   039: CONE LOCAL E FILTRO — coordenadas de Herm2, produtos externos positivos singulares, rigidez
--   quadratica condicional, filtro e fase dos logaritmos locais (fatores, sinais, det, nao unitalidade),
--   reducao global ao bloco 0 (igualdade de operadores, compressao GNS). NAO pago: Delta^(it) como boost
--   sobre a tetrade (a obstrucao finita anterior segue). 040 (resposta a ORDEM_009): OBSTRUCAO PRECISA —
--   o fluxo modular do estado fixo nao percorre a curva de estados; o relogio de Fisher (lambda_F = 1/2 - 3k/16)
--   e toda inversa normalizada do relogio entropico (lambda_D = 1/2 - k/8) FALHAM no casamento quartico da
--   familia de um sitio (excedem lambda* = 1/2 - 9B2/(8 log2 B) - eta O/(2 log2 B)) embora preservem o
--   quadratico; o relogio afim da lambda = 0; a rede A(I) <= A(J) sse I <= J com representacao local fiel;
--   NEGATIVO: a area NAO e escalar so da algebra e do estado (dois protocolos de tangentes, duas densidades).
--   H3 (habitante) segue OPEN — o tipo canonico foi usado para PROVAR o negativo. 041: FLUXO DE CALOR efetivo
--   Q(t) = int_0^t -kappa u m A(u) du ligado por teorema a metrica/geodesica/waveMatter/Jacobi; a igualdade
--   FINITA exata Q = kappa eta (A-1)/(2 pi) FALHA (C/t^4 -> kappa eta (a^2+c^2)/(24 pi) > 0); a relacao
--   infinitesimal segue compativel. Estatuto [REAL / DERIVED / INPUT / OPEN]: familia especificada; area
--   fisica, EquilibriumScreenData compativel, materia/geometria/normalizacao e reconstrucao geral OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 16/16, 18/18, 8/8; 3/3 auditores exit 0;
--   recompilacao INDEPENDENTE 11/11, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.LikelihoodPreparedState
import TGLExt.LocalFilterLorentzAction
import TGLExt.ExpectationSlice
import TGLExt.ExpectationBounded

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Cone039
open Matrix Filter Topology TGLExt ChatgptAudit
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
  ChatgptAudit.Cocycle030 ChatgptAudit.Response028
open scoped Kronecker
noncomputable section

/-- The weighted partial trace of a tensor product, with no commutativity assumption. -/
theorem weighted_slice_kronecker (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (c : Matrix (Fin 2) (Fin 2) ℂ) :
    weightedStepSlice P N (a ⊗ₖ c) =
      (∑ i : Fin 2, (siteW (P.w (N+1)) i : ℂ) * c i i) • a := by
  ext i j
  change (∑ r : Fin 2, (siteW (P.w (N+1)) r : ℂ) * (a i j * c r r)) =
    (∑ r : Fin 2, (siteW (P.w (N+1)) r : ℂ) * c r r) * a i j
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro r _
  ring

/-- Each added site has exactly unit weighted filter square. -/
theorem site_relative_filter_square_normalized (P Q : SiteProfile) (n : ℕ) :
    (∑ i : Fin 2, (siteW (P.w n) i : ℂ) *
      (relativeFilter (siteW (P.w n)) (siteW (Q.w n)) *
        relativeFilter (siteW (P.w n)) (siteW (Q.w n))) i i) = 1 := by
  have h := relative_filter_local_state (siteW (P.w n)) (siteW (Q.w n))
    (siteW_pos (P.pos n) (P.lt_one n))
    (fun i => (siteW_pos (Q.pos n) (Q.lt_one n) i).le)
    (1 : Matrix (Fin 2) (Fin 2) ℂ)
  simpa only [relative_filter_self_adjoint, mul_one, Matrix.one_apply_eq,
    ← Complex.ofReal_sum, siteW_sum, Complex.ofReal_one] using h

/-- An added product-state site disappears from the filtered sandwich under its weighted trace. -/
theorem weighted_slice_relative_filter_step (P Q : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    weightedStepSlice P N
      (relativeFilter (towerW P (N+1)) (towerW Q (N+1)) *
        towerStep a *
        relativeFilter (towerW P (N+1)) (towerW Q (N+1))) =
      relativeFilter (towerW P N) (towerW Q N) * a *
        relativeFilter (towerW P N) (towerW Q N) := by
  have hfilter :
      relativeFilter (towerW P (N+1)) (towerW Q (N+1)) =
        relativeFilter (towerW P N) (towerW Q N) ⊗ₖ
          relativeFilter (siteW (P.w (N+1))) (siteW (Q.w (N+1))) :=
    ChatgptAudit.Profile026.profile_filter_step P Q N
  simp only [hfilter, towerStep, ← Matrix.mul_kronecker_mul, mul_one]
  rw [weighted_slice_kronecker, site_relative_filter_square_normalized, one_smul]

/-- Exact finite-prefix reduction for an arbitrary, possibly non-Hermitian, local matrix. -/
theorem finite_filter_local_reduction (P Q : SiteProfile) (N : ℕ)
    (X : Matrix (Fin 2) (Fin 2) ℂ) :
    towerExpectation P 0
      (towerPi P (N := N)
        (relativeFilter (towerW P N) (towerW Q N) *
          tPush (Nat.zero_le N) X *
          relativeFilter (towerW P N) (towerW Q N))) =
      towerPi P (N := 0)
        (relativeFilter (towerW P 0) (towerW Q 0) * X *
          relativeFilter (towerW P 0) (towerW Q 0)) := by
  induction N with
  | zero =>
      simpa only [tPush_self] using
        (expectation_fixes (P := P) 0
          (relativeFilter (towerW P 0) (towerW Q 0) * X *
            relativeFilter (towerW P 0) (towerW Q 0)))
  | succ N ih =>
      rw [tPush_succ (Nat.zero_le N) (Nat.zero_le (N+1))]
      calc
        towerExpectation P 0
            (towerPi P (N := N+1)
              (relativeFilter (towerW P (N+1)) (towerW Q (N+1)) *
                towerStep (tPush (Nat.zero_le N) X) *
                relativeFilter (towerW P (N+1)) (towerW Q (N+1)))) =
            towerExpectation P 0
              (towerExpectation P N
                (towerPi P (N := N+1)
                  (relativeFilter (towerW P (N+1)) (towerW Q (N+1)) *
                    towerStep (tPush (Nat.zero_le N) X) *
                    relativeFilter (towerW P (N+1)) (towerW Q (N+1))))) := by
            rw [expectation_tower, min_eq_left (Nat.zero_le N)]
        _ = towerExpectation P 0
              (towerPi P (N := N)
                (relativeFilter (towerW P N) (towerW Q N) *
                  tPush (Nat.zero_le N) X *
                  relativeFilter (towerW P N) (towerW Q N))) := by
            rw [expectation_step_slice, weighted_slice_relative_filter_step]
        _ = _ := ih

/-- The same finite reduction stated directly for products of represented operators. -/
theorem finite_filter_operator_local_reduction (P Q : SiteProfile) (N : ℕ)
    (X : Matrix (Fin 2) (Fin 2) ℂ) :
    towerExpectation P 0
      (towerPi P (N := N) (relativeFilter (towerW P N) (towerW Q N)) *
        towerPi P (N := 0) X *
        towerPi P (N := N) (relativeFilter (towerW P N) (towerW Q N))) =
      towerPi P (N := 0)
        (relativeFilter (towerW P 0) (towerW Q 0) * X *
          relativeFilter (towerW P 0) (towerW Q 0)) := by
  simpa only [towerPi_mul, towerPi_compat] using
    finite_filter_local_reduction P Q N X

/-- The state-normalized local filter, with exactly the weights of the global likelihood family. -/
def localStateFilter (b : SummableAmplitude) (t : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  relativeFilter (towerW thirdThermalReference 0) (towerW (amplitudeProfile b t) 0)

theorem local_state_filter_weights (b : SummableAmplitude) (t : ℝ) :
    localStateFilter b t =
      relativeFilter (siteW (1/3)) (siteW (1/3 - b.value 0 * regularParameter t)) := rfl

/-- Reduction of the actual norm-limit likelihood filter to the entire local matrix algebra. -/
theorem global_filter_local_reduction (b : SummableAmplitude) (t : ℝ)
    (X : Matrix (Fin 2) (Fin 2) ℂ) :
    towerExpectation thirdThermalReference 0
      (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t) =
      towerPi thirdThermalReference (N := 0) (localStateFilter b t * X * localStateFilter b t) := by
  have hR : Tendsto
      (fun N : ℕ => towerPi thirdThermalReference (N := N)
        (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N)))
      atTop (𝓝 (likelihoodFilter b t)) := by
    simpa only [likelihood_prefix_filter] using likelihood_filter_prefix_limit b t
  have hprod : Tendsto
      (fun N : ℕ =>
        towerPi thirdThermalReference (N := N)
          (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N)) *
        towerPi thirdThermalReference (N := 0) X *
        towerPi thirdThermalReference (N := N)
          (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N)))
      atTop
      (𝓝 (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t)) :=
    (hR.mul tendsto_const_nhds).mul hR
  have he : Tendsto
      (fun N : ℕ => towerExpectation thirdThermalReference 0
        (towerPi thirdThermalReference (N := N)
            (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N)) *
          towerPi thirdThermalReference (N := 0) X *
          towerPi thirdThermalReference (N := N)
            (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N))))
      atTop
      (𝓝 (towerExpectation thirdThermalReference 0
        (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t))) :=
    (expectationCLM thirdThermalReference 0).continuous.continuousAt.tendsto.comp hprod
  have hconstant : Tendsto
      (fun _N : ℕ => towerPi thirdThermalReference (N := 0)
        (localStateFilter b t * X * localStateFilter b t))
      atTop
      (𝓝 (towerExpectation thirdThermalReference 0
        (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t))) := by
    simpa only [finite_filter_operator_local_reduction, localStateFilter] using he
  exact tendsto_nhds_unique hconstant tendsto_const_nhds

/-- Decoding the conditional expectation gives a literal equality of two-by-two matrices. -/
theorem global_filter_local_matrix (b : SummableAmplitude) (t : ℝ)
    (X : Matrix (Fin 2) (Fin 2) ℂ) :
    expectationMatrix thirdThermalReference 0
      (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t) =
      localStateFilter b t * X * localStateFilter b t := by
  apply towerPi_injective thirdThermalReference 0
  change towerExpectation thirdThermalReference 0
      (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t) =
    towerPi thirdThermalReference (N := 0) (localStateFilter b t * X * localStateFilter b t)
  exact global_filter_local_reduction b t X

/-- On the local GNS subspace, compression of the filtered operator is this represented matrix. -/
theorem global_filter_local_compression (b : SummableAmplitude) (t : ℝ)
    (X : Matrix (Fin 2) (Fin 2) ℂ) {v : TowerHilbert thirdThermalReference}
    (hv : v ∈ levelSpace thirdThermalReference 0) :
    levelProject thirdThermalReference 0
      ((likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t) v) =
      towerPi thirdThermalReference (N := 0) (localStateFilter b t * X * localStateFilter b t) v := by
  have hA : likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t ∈
      theFactorObject thirdThermalReference :=
    (theFactorObject thirdThermalReference).mul_mem
      ((theFactorObject thirdThermalReference).mul_mem
        (likelihood_filter_mem_factor b t) (towerPi_mem_factor (P := thirdThermalReference) (N := 0) X))
      (likelihood_filter_mem_factor b t)
  have hc := expectation_compression (P := thirdThermalReference) 0
    (likelihoodFilter b t * towerPi thirdThermalReference (N := 0) X * likelihoodFilter b t) hA hv
  rw [global_filter_local_reduction] at hc
  exact hc.symm

/-- The boost of the local Hermitian block comes from the actual global filter,
    after the explicit determinant-normalizing scalar is applied to its conditional expectation. -/
theorem global_filter_local_boost (b : SummableAmplitude) (t tau x y z : ℝ) :
    let q := (amplitudeProfile b t).w 0
    let ell0 := Real.log q - Real.log (1/3)
    let ell1 := Real.log (1-q) - Real.log (1-(1/3))
    let c := Real.exp (-(ell0+ell1)/4)
    let chi := (ell0-ell1)/2
    (c : ℂ)^2 • towerExpectation thirdThermalReference 0
      (likelihoodFilter b t *
        towerPi thirdThermalReference (N := 0) (hermitianMatrix tau x y z) *
        likelihoodFilter b t) =
      towerPi thirdThermalReference (N := 0)
        (hermitianMatrix
          (Real.cosh chi*tau + Real.sinh chi*z) x y
          (Real.sinh chi*tau + Real.cosh chi*z)) := by
  let q := (amplitudeProfile b t).w 0
  let ell0 := Real.log q - Real.log (1/3)
  let ell1 := Real.log (1-q) - Real.log (1-(1/3))
  let c := Real.exp (-(ell0+ell1)/4)
  let chi := (ell0-ell1)/2
  change (c : ℂ)^2 • towerExpectation thirdThermalReference 0
      (likelihoodFilter b t *
        towerPi thirdThermalReference (N := 0) (hermitianMatrix tau x y z) *
        likelihoodFilter b t) =
    towerPi thirdThermalReference (N := 0)
      (hermitianMatrix
        (Real.cosh chi*tau + Real.sinh chi*z) x y
        (Real.sinh chi*tau + Real.cosh chi*z))
  have hfilter : normalizedLocalFilter ell0 ell1 =
      (c : ℂ) • localStateFilter b t := by
    exact normalized_local_filter_from_relative (1/3) q
      (by norm_num) (by norm_num)
      ((amplitudeProfile b t).pos 0) ((amplitudeProfile b t).lt_one 0)
  have hr : (localStateFilter b t)ᴴ = localStateFilter b t :=
    relative_filter_self_adjoint _ _
  have hscaled :
      (c : ℂ)^2 •
        (localStateFilter b t * hermitianMatrix tau x y z * localStateFilter b t) =
      hermitianMatrix
        (Real.cosh chi*tau + Real.sinh chi*z) x y
        (Real.sinh chi*tau + Real.cosh chi*z) := by
    simpa only [hfilter, Matrix.conjTranspose_smul, Complex.star_def,
      Complex.conj_ofReal, hr, smul_mul_assoc, mul_smul_comm, smul_smul, pow_two]
      using normalized_local_filter_boost ell0 ell1 tau x y z
  calc
    (c : ℂ)^2 • towerExpectation thirdThermalReference 0
        (likelihoodFilter b t *
          towerPi thirdThermalReference (N := 0) (hermitianMatrix tau x y z) *
          likelihoodFilter b t) =
        (c : ℂ)^2 • towerPi thirdThermalReference (N := 0)
          (localStateFilter b t * hermitianMatrix tau x y z * localStateFilter b t) := by
        rw [global_filter_local_reduction]
    _ = towerPi thirdThermalReference (N := 0)
          ((c : ℂ)^2 •
            (localStateFilter b t * hermitianMatrix tau x y z * localStateFilter b t)) :=
        (towerPi_smul (P := thirdThermalReference) (N := 0) ((c : ℂ)^2) _).symm
    _ = _ := congrArg (fun A : Matrix (Fin 2) (Fin 2) ℂ => towerPi thirdThermalReference (N := 0) A)
      hscaled

#print axioms weighted_slice_kronecker
#print axioms site_relative_filter_square_normalized
#print axioms weighted_slice_relative_filter_step
#print axioms finite_filter_local_reduction
#print axioms finite_filter_operator_local_reduction
#print axioms localStateFilter
#print axioms local_state_filter_weights
#print axioms global_filter_local_reduction
#print axioms global_filter_local_matrix
#print axioms global_filter_local_compression
#print axioms global_filter_local_boost

end
end ChatgptAudit.Cone039
