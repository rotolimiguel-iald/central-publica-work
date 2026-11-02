-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_056 ESPONTANEA (08/09/2026), transposta em 08/09/2026
-- Lote 055..056 (6 modulos; origem: ordem direta do operador a bancada para demonstrar no modelo completo).
--   055 — SELETOR RELATIVO NA TORRE INFINITA: com a preparacao ja existente geometricAmplitude (b_n = 2^-n/24)
--     e os pesos da torre, a leitura de verossimilhanca do cociclo SEPARA todas as configuracoes infinitas
--     quando t != 0 (contraste a(x) = log(1+3x/2) - log(1-3x) com 2a(x/2) < a(x): cada a_n domina toda a cauda;
--     codigo binario injetivo); a leitura coincide com os logaritmos dos pesos efetivos e com o gerador de
--     verossimilhanca do kernel (existing_global_generator_bound / density_normalized / cocycle_limit);
--     a densidade existente e o estado preparado. [DERIVED, analitico, NAO Lean]: A = C*(P_n), D = W*(P_n)
--     recuperados pelo cociclo; [DERIVED + KNOWN]: esperanca D no fator inteiro (Takesaki). D e comutativa,
--     M e o ambiente: W*(u) = D nao e W*(u) = M. Vale para geometricAmplitude e t != 0, nao para todo perfil.
--   056 — METRICAS DA TORRE E LIMITES DA RECONSTRUCAO: d_t(x,y) = |g_t(x) - g_t(y)| e metrica (t != 0) e a
--     escala e livre; Fisher radial F(r) = sum b_n^2/[q_n(1-q_n)] com 1/96 <= F <= 4/357 e F(0) = 1/96 (soma e
--     cotas Lean; identificacao probabilistica global analitica); entropia relativa/t^4 -> F(0)/2 = 1/192;
--     NEGATIVOS: a familia de um parametro tem Gram 2x2 de determinante ZERO (nao gera area por renomear
--     coordenadas); o gerador relativo como Dirac tem distancia de comutadores INFINITA entre configuracoes
--     distintas (comutador zero com as coordenadas); o gauge relativo exp(isP_n) preserva ambos os estados e o
--     cociclo (liberdade residual), e seu gerador NAO e central ([P_0, E_01] = E_01 != 0).
--   Estatuto: [REAL] o compilado; [DERIVED] reconstrucao da algebra diagonal, interpretacao global de Fisher,
--   4||xi_r||^2 = F(r), arcsin, distancia de Connes; [OPEN] geometria fisica 3+1, area-entropia geometrica,
--   calor fisico, acao gravitacional, Einstein-Cartan sem hipoteses. Nenhum nome ligado a H3/area/gate.
-- Auditoria da gerencia (sessao d554e796, 08/09/2026): hashes 10/10 + 13/13; 2/2 auditores da bancada exit 0;
--   sem revisao cientifica independente na bancada (declarado) — a gerencia leu os enunciados;
--   recompilacao INDEPENDENTE 6/6, axiomas no trio; guarda de colisao; fontes lidas das SUBPASTAS da entrega.
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SpectralMetricGeometry
import TGLExt.CentralizerPhaseOrbit
set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.Geometry056
open Filter Topology Set TGLExt ChatgptAudit.CocycleRealization
  ChatgptAudit.Response028 ChatgptAudit.Cocycle030 ChatgptAudit.Density033
  ChatgptAudit.Angular034 ChatgptAudit.Thermal025
noncomputable section

theorem site_commutes_existing_term (t : ℝ) (n k : ℕ) :
    Commute (siteZeroProjection thirdThermalReference n)
      (likelihoodTerm geometricAmplitude t k) := by
  unfold likelihoodTerm siteLikelihood
  exact ((site_zero_commute thirdThermalReference n k).smul_right _).add_right
    (((Commute.one_right _).sub_right
      (site_zero_commute thirdThermalReference n k)).smul_right _)

theorem site_commutes_existing_generator (t : ℝ) (n : ℕ) :
    Commute (siteZeroProjection thirdThermalReference n)
      (likelihoodGenerator geometricAmplitude t) :=
  Commute.tsum_right _ (fun k => site_commutes_existing_term t n k)

theorem coordinate_test_has_zero_commutator (t c : ℝ) (n : ℕ) :
    likelihoodGenerator geometricAmplitude t*((c:ℂ) • siteZeroProjection thirdThermalReference n) -
      ((c:ℂ) • siteZeroProjection thirdThermalReference n)*likelihoodGenerator geometricAmplitude t=0 :=
  sub_eq_zero.mpr ((site_commutes_existing_generator t n).symm.smul_right (c:ℂ)).eq

theorem existing_generator_has_unbounded_commutator_distance (t : ℝ)
    {u v : ℕ → Bool} (huv : u≠v) (R : ℝ) :
    ∃ (n : ℕ) (c : ℝ),
      ‖likelihoodGenerator geometricAmplitude t*((c:ℂ) • siteZeroProjection thirdThermalReference n) -
        ((c:ℂ) • siteZeroProjection thirdThermalReference n)*likelihoodGenerator geometricAmplitude t‖ ≤ 1 ∧
      R < |binaryCoordinateTest c n u-binaryCoordinateTest c n v| := by
  obtain ⟨n,c,hc⟩ := coordinate_separates_with_arbitrary_size huv R
  exact ⟨n,c,by rw [coordinate_test_has_zero_commutator]; norm_num,hc⟩

def relativeSiteGauge (n : ℕ) (s : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  boundedPhase thirdThermalReference (siteZeroProjection thirdThermalReference n) s

theorem relative_site_gauge_unitary (n : ℕ) (s : ℝ) :
    relativeSiteGauge n s∈unitary _ :=
  bounded_phase_unitary _ _ (site_zero_projection _ n).isSelfAdjoint s

theorem relative_site_gauge_centralizer (n : ℕ) (s : ℝ) :
    relativeSiteGauge n s∈omegaCentralizer thirdThermalReference :=
  bounded_phase_centralizer _ _ (site_zero_mem_centralizer _ n) s

theorem relative_site_gauge_commutes_generator (n : ℕ) (s t : ℝ) :
    Commute (relativeSiteGauge n s) (likelihoodGenerator geometricAmplitude t) :=
  ((site_commutes_existing_generator t n).smul_left ((s:ℂ)*Complex.I)).exp_left

theorem relative_site_gauge_commutes_density (n : ℕ) (s t : ℝ) :
    Commute (relativeSiteGauge n s) (likelihoodDensity geometricAmplitude t) :=
  (relative_site_gauge_commutes_generator n s t).exp_right

theorem relative_site_gauge_commutes_cocycle (n : ℕ) (s t z : ℝ) :
    Commute (relativeSiteGauge n s) (likelihoodCocycle geometricAmplitude t z) :=
  ((relative_site_gauge_commutes_generator n s t).smul_right ((z:ℂ)*Complex.I)).exp_right

theorem unitary_conjugation_fixes_commuting
    (U A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hu : U∈unitary _) (h : Commute U A) :
    star U*A*U=A := by
  rw [mul_assoc,h.symm.eq,←mul_assoc,(Unitary.mem_iff.mp hu).1,one_mul]

theorem relative_site_gauge_fixes_cocycle (n : ℕ) (s t z : ℝ) :
    star (relativeSiteGauge n s)*likelihoodCocycle geometricAmplitude t z*
      relativeSiteGauge n s=likelihoodCocycle geometricAmplitude t z :=
  unitary_conjugation_fixes_commuting _ _ (relative_site_gauge_unitary n s)
    (relative_site_gauge_commutes_cocycle n s t z)

theorem relative_site_gauge_fixes_site (n k : ℕ) (s : ℝ) :
    star (relativeSiteGauge n s)*siteZeroProjection thirdThermalReference k*
      relativeSiteGauge n s=siteZeroProjection thirdThermalReference k :=
  unitary_conjugation_fixes_commuting _ _ (relative_site_gauge_unitary n s)
    (((site_zero_commute thirdThermalReference n k).smul_left ((s:ℂ)*Complex.I)).exp_left)

theorem relative_site_gauge_preserves_reference (n : ℕ) (s : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) :
    omegaState thirdThermalReference (star (relativeSiteGauge n s)*A*relativeSiteGauge n s)=
      omegaState thirdThermalReference A :=
  centralizer_unitary_preserves_state _ _ (relative_site_gauge_centralizer n s)
    (relative_site_gauge_unitary n s) A hA

theorem relative_site_gauge_preserves_preparation (n : ℕ) (s t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) :
    amplitudeState geometricAmplitude t (star (relativeSiteGauge n s)*A*relativeSiteGauge n s)=
      amplitudeState geometricAmplitude t A := by
  have hU := (relative_site_gauge_centralizer n s).1
  have hH := likelihood_density_mem_factor geometricAmplitude t
  have hs : Commute (likelihoodDensity geometricAmplitude t) (star (relativeSiteGauge n s)) := by
    have h := congrArg star (relative_site_gauge_commutes_density n s t).eq
    change likelihoodDensity geometricAmplitude t*star (relativeSiteGauge n s)=
      star (relativeSiteGauge n s)*likelihoodDensity geometricAmplitude t
    simpa only [star_mul,(likelihood_density_selfadjoint geometricAmplitude t).star_eq] using h
  rw [likelihood_density_state_left _ _ _ (mul_mem (mul_mem (star_mem hU) hA) hU),
    likelihood_density_state_left _ _ A hA]
  have he : likelihoodDensity geometricAmplitude t*
      (star (relativeSiteGauge n s)*A*relativeSiteGauge n s)=
      star (relativeSiteGauge n s)*(likelihoodDensity geometricAmplitude t*A)*relativeSiteGauge n s := by
    calc
      _=(likelihoodDensity geometricAmplitude t*star (relativeSiteGauge n s))*A*
          relativeSiteGauge n s := by noncomm_ring
      _=(star (relativeSiteGauge n s)*likelihoodDensity geometricAmplitude t)*A*
          relativeSiteGauge n s := by rw [hs.eq]
      _=_ := by noncomm_ring
  rw [he]
  exact relative_site_gauge_preserves_reference n s _ (mul_mem hH hA)

def firstOffDiagonal :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  towerPi thirdThermalReference (N:=0) (Matrix.single (0:Fin 2) 1 (1:ℂ))

theorem first_off_diagonal_nonzero : firstOffDiagonal≠0 := by
  intro h
  have hz : towerPi thirdThermalReference (N:=0) (0:Matrix (Fin 2) (Fin 2) ℂ)=0 :=
    (towerPiLinear thirdThermalReference 0).map_zero
  have hm := (towerPi_injective thirdThermalReference 0) (h.trans hz.symm)
  have he := congrArg (fun a : Matrix (Fin 2) (Fin 2) ℂ => a 0 1) hm
  norm_num [Matrix.single_apply] at he

theorem first_projection_left_off_diagonal :
    siteZeroProjection thirdThermalReference 0*firstOffDiagonal=firstOffDiagonal := by
  change towerPi thirdThermalReference (N:=0) (Matrix.single (0:Fin 2) 0 (1:ℂ))*
    towerPi thirdThermalReference (N:=0) (Matrix.single (0:Fin 2) 1 (1:ℂ))=_
  rw [←towerPi_mul]
  congr 1
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mul_apply,Fin.sum_univ_two,Matrix.single_apply]

theorem first_projection_right_off_diagonal :
    firstOffDiagonal*siteZeroProjection thirdThermalReference 0=0 := by
  change towerPi thirdThermalReference (N:=0) (Matrix.single (0:Fin 2) 1 (1:ℂ))*
    towerPi thirdThermalReference (N:=0) (Matrix.single (0:Fin 2) 0 (1:ℂ))=_
  rw [←towerPi_mul]
  have hm : (Matrix.single (0:Fin 2) (1:Fin 2) (1:ℂ))*
      (Matrix.single (0:Fin 2) (0:Fin 2) (1:ℂ))=0 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [Matrix.mul_apply,Fin.sum_univ_two,Matrix.single_apply]
  rw [hm]
  exact (towerPiLinear thirdThermalReference 0).map_zero

theorem gauge_generator_changes_quantum_observable :
    siteZeroProjection thirdThermalReference 0*firstOffDiagonal -
      firstOffDiagonal*siteZeroProjection thirdThermalReference 0=firstOffDiagonal := by
  rw [first_projection_left_off_diagonal,first_projection_right_off_diagonal,sub_zero]

theorem gauge_generator_is_not_central :
    ¬Commute (siteZeroProjection thirdThermalReference 0) firstOffDiagonal := by
  intro h
  have he := sub_eq_zero.mpr h.eq
  rw [gauge_generator_changes_quantum_observable] at he
  exact first_off_diagonal_nonzero he

#print axioms site_commutes_existing_term
#print axioms site_commutes_existing_generator
#print axioms coordinate_test_has_zero_commutator
#print axioms existing_generator_has_unbounded_commutator_distance
#print axioms relativeSiteGauge
#print axioms relative_site_gauge_unitary
#print axioms relative_site_gauge_centralizer
#print axioms relative_site_gauge_commutes_generator
#print axioms relative_site_gauge_commutes_density
#print axioms relative_site_gauge_commutes_cocycle
#print axioms unitary_conjugation_fixes_commuting
#print axioms relative_site_gauge_fixes_cocycle
#print axioms relative_site_gauge_fixes_site
#print axioms relative_site_gauge_preserves_reference
#print axioms relative_site_gauge_preserves_preparation
#print axioms firstOffDiagonal
#print axioms first_off_diagonal_nonzero
#print axioms first_projection_left_off_diagonal
#print axioms first_projection_right_off_diagonal
#print axioms gauge_generator_changes_quantum_observable
#print axioms gauge_generator_is_not_central

end
end ChatgptAudit.Geometry056
