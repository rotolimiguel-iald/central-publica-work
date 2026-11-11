-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_037 (06/09/2026), transposta em 06/09/2026
-- Lote 035..037 (processo da ORDEM_008 cumprido pela bancada: zero instancias anonimas, lote compilado junto
--   num diretorio limpo). 035: DEFORMACOES OBSERVAVEIS e AREA DE FISHER — derivadas da conjugacao unitaria e
--   do estado, observaveis de Pauli por sitio na torre real, duas leituras independentes (jacobiano nao
--   degenerado), medicao conjunta efetiva (sitios distintos), probabilidades normalizadas e suas derivadas,
--   matriz de Fisher na origem, densidade de area de Fisher (4/9 como area de coordenadas). 036: AREA OPTICA e
--   LIBERDADE RADIATIVA — a area induzida dos campos de Jacobi da metrica 029 ligada a curvatura real
--   (A2(0) = -Ric(d,d); A4(0) = 2(tr K)^2 - 2 tr(K_TF^T K_TF)); germes de area distintos para shears
--   distintos. 037: QUARTA ORDEM, AREA e RELOGIO — limites entropicos e de area em 4a ordem; NEGATIVO
--   MEDIDO: o casamento adicional em 4a ordem com parametro comum fixo FALHA (delta4 >= (7/48) B > 0);
--   a reparametrizacao do relogio t + lambda t^3 cancela o defeito ate 4a ordem (controle do relogio relativo).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: X, Y, sitios e normalizacao sao INPUT; a familia optica
--   lorentziana e INPUT; identificacao da inscricao angular com area fisica, retorno estabilizador, ponte
--   regiao-algebra, escala, assinatura, dinamica gravitacional e H3 geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 14/14, 8/8 (via manifesto), 10/10; manifestos
--   1051/977; 3/3 auditores exit 0; recompilacao INDEPENDENTE 15/15, axiomas no trio; guarda de colisao;
--   enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.OpticalAreaFreedom
import Mathlib.Analysis.Calculus.Taylor

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace ChatgptAudit.Quartic037
open Filter Set ChatgptAudit.Optical036
open scoped Topology
noncomputable section

/- The fourth Taylor polynomial is evaluated from the already proved derivatives.
Taylor--Peano then controls the remainder. Only after that theorem is applied do
we divide on the punctured neighbourhood and transport the result to inducedArea. -/

theorem optical_jacobi_taylor_four (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (t : ℝ) :
    taylorWithinEval (opticalJacobiArea a c) 4 univ 0 t =
      1-(a+c)*t^2/2+(a^2+6*a*c+c^2)/24*t^4 := by
  norm_num [taylor_within_apply,Finset.sum_range_succ,iteratedDerivWithin_univ,
    iteratedDeriv_zero,optical_jacobi_area_zero,
    optical_jacobi_area_iterated_one_zero a c ha hc,
    optical_jacobi_area_iterated_two_zero a c ha hc,
    optical_jacobi_area_iterated_three_zero a c ha hc,
    optical_jacobi_area_iterated_four_zero a c ha hc]; ring

theorem optical_jacobi_taylor_remainder_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ =>
      (opticalJacobiArea a c t-
        (1-(a+c)*t^2/2+(a^2+6*a*c+c^2)/24*t^4))/t^4)
      (𝓝 0) (𝓝 0) := by
  have h := Real.taylor_tendsto (f := opticalJacobiArea a c)
    (x₀ := 0) (n := 4) (s := univ) convex_univ (mem_univ 0)
    (optical_jacobi_area_contDiff a c).contDiffOn
  simpa only [nhdsWithin_univ,sub_zero,optical_jacobi_taylor_four a c ha hc] using h

theorem optical_jacobi_area_quartic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (opticalJacobiArea a c t-1+(a+c)*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 ((a^2+6*a*c+c^2)/24)) := by
  have h0 := (optical_jacobi_taylor_remainder_limit a c ha hc).mono_left
    (show 𝓝[≠] (0 : ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)
  have hq := h0.add_const ((a^2+6*a*c+c^2)/24)
  have he :
      (fun t : ℝ => (opticalJacobiArea a c t-1+(a+c)*t^2/2)/t^4) =ᶠ[𝓝[≠] 0]
      (fun t : ℝ =>
        (opticalJacobiArea a c t-
          (1-(a+c)*t^2/2+(a^2+6*a*c+c^2)/24*t^4))/t^4+
            (a^2+6*a*c+c^2)/24) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have ht0 : t≠0 := ht
    field_simp [ht0]; ring
  exact (tendsto_congr' he).2 (by simpa only [zero_add] using hq)

/-- Effective fourth-order asymptotics of the geometric Jacobi screen area. -/
theorem geometric_jacobi_area_quartic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (geometricJacobiArea a c t-1+(a+c)*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 ((a^2+6*a*c+c^2)/24)) := by
  have he :
      (fun t : ℝ => (geometricJacobiArea a c t-1+(a+c)*t^2/2)/t^4) =ᶠ[𝓝[≠] 0]
      (fun t : ℝ => (opticalJacobiArea a c t-1+(a+c)*t^2/2)/t^4) := by
    filter_upwards [(geometric_jacobi_area_agrees_near_zero a c ha hc).filter_mono
      (show 𝓝[≠] (0 : ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)] with t ht
    rw [ht]
  exact (tendsto_congr' he).2 (optical_jacobi_area_quartic_limit a c ha hc)

theorem geometric_jacobi_area_rs_quartic_limit (r s : ℝ) (hs : |s|<r/2) :
    Tendsto (fun t : ℝ =>
      (geometricJacobiArea (r/2+s) (r/2-s) t-1+r*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 (r^2/12-s^2/6)) := by
  obtain ⟨ha,hc⟩ := optical_rs_positive_coefficients r s hs
  have hsum : r/2+s+(r/2-s)=r := by ring
  have hcoeff :
      ((r/2+s)^2+6*(r/2+s)*(r/2-s)+(r/2-s)^2)/24=r^2/12-s^2/6 := by ring
  simpa only [hsum,hcoeff] using
    geometric_jacobi_area_quartic_limit (r/2+s) (r/2-s) ha.le hc.le

#print axioms optical_jacobi_taylor_four
#print axioms optical_jacobi_taylor_remainder_limit
#print axioms optical_jacobi_area_quartic_limit
#print axioms geometric_jacobi_area_quartic_limit
#print axioms geometric_jacobi_area_rs_quartic_limit

end
end ChatgptAudit.Quartic037
