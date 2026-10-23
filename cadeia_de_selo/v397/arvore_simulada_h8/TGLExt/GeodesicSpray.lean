-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_015 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.TransportedScreenExistence

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen015
open Matrix Filter Topology Set
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

abbrev Phase4 := Coordinate4 × Coordinate4

def phaseDomain (U : Set Coordinate4) : Set Phase4 := {p | p.1∈U}

def sprayAcceleration (Gamma : ConnectionField4) (x v : Coordinate4) : Coordinate4 :=
  -((connectionAlong Gamma x v).mulVec v)

def geodesicSpray (Gamma : ConnectionField4) (p : Phase4) : Phase4 :=
  (p.2,sprayAcceleration Gamma p.1 p.2)

theorem phase_domain_open (U : Set Coordinate4) (hU : IsOpen U) :
    IsOpen (phaseDomain U) := hU.preimage continuous_fst

theorem geodesic_spray_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma) :
    ContDiffOn ℝ ∞ (geodesicSpray Gamma) (phaseDomain U) := by
  intro p hp
  apply ContDiffAt.contDiffWithinAt
  have hg (i a b : Fin 4) :
      ContDiffAt ℝ ∞ (fun q : Phase4 => Gamma q.1 i a b) p :=
    ((hG i a b p.1 hp).contDiffAt (hU.mem_nhds hp)).comp p contDiffAt_fst
  have hv (a : Fin 4) : ContDiffAt ℝ ∞ (fun q : Phase4 => q.2 a) p := by
    fun_prop
  apply ContDiffAt.prodMk contDiffAt_snd
  apply contDiffAt_pi.2
  intro a
  change ContDiffAt ℝ ∞ (fun q : Phase4 => sprayAcceleration Gamma q.1 q.2 a) p
  simp only [sprayAcceleration,connectionAlong,Matrix.mulVec,dotProduct,
    Pi.neg_apply,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Fin.sum_univ_four]
  have hL (b : Fin 4) : ContDiffAt ℝ ∞ (fun q : Phase4 =>
      q.2 0*Gamma q.1 0 a b+q.2 1*Gamma q.1 1 a b+
      q.2 2*Gamma q.1 2 a b+q.2 3*Gamma q.1 3 a b) p :=
    ((((hv 0).mul (hg 0 a b)).add ((hv 1).mul (hg 1 a b))).add
      ((hv 2).mul (hg 2 a b))).add ((hv 3).mul (hg 3 a b))
  exact (((((hL 0).mul (hv 0)).add ((hL 1).mul (hv 1))).add
    ((hL 2).mul (hv 2))).add ((hL 3).mul (hv 3))).neg

theorem geodesic_spray_c1 (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x v : Coordinate4) (hx : x∈U) :
    ContDiffAt ℝ 1 (geodesicSpray Gamma) (x,v) :=
  (((geodesic_spray_smooth U hU Gamma hG) (x,v) hx).contDiffAt
    ((phase_domain_open U hU).mem_nhds hx)).of_le (by simp)

theorem spray_position_component (Gamma : ConnectionField4) (p : Phase4) :
    (geodesicSpray Gamma p).1=p.2 := rfl

theorem spray_zero_velocity (Gamma : ConnectionField4) (x : Coordinate4) :
    geodesicSpray Gamma (x,0)=0 := by
  simp [geodesicSpray,sprayAcceleration]

theorem geodesic_energy_algebra (g L : Tensor4) (v : Coordinate4) :
    tensorPair g (-(L.mulVec v)) v+tensorPair (Lᵀ*g+g*L) v v+
      tensorPair g v (-(L.mulVec v))=0 := by
  simp only [tensorPair,Matrix.mulVec,dotProduct,Matrix.mul_apply,Matrix.transpose_apply,
    Matrix.add_apply,Pi.neg_apply,Fin.sum_univ_four]
  ring

theorem eventually_phase_rectangle (p : Phase4) (P : Phase4 × ℝ → Prop)
    (hP : ∀ᶠ z in 𝓝 (p,(0:ℝ)), P z) :
    ∃ radius > (0:ℝ), ∀ q∈Metric.ball p radius, ∀ t∈Ioo (-radius) radius, P (q,t) := by
  obtain ⟨radius,hr,hball⟩ := Metric.mem_nhds_iff.mp hP
  refine ⟨radius,hr,?_⟩
  intro q hq t ht
  apply hball
  rw [Metric.mem_ball,Prod.dist_eq]
  apply max_lt
  · exact hq
  · simpa only [Real.dist_eq,sub_zero,abs_lt,Set.mem_Ioo] using ht

#print axioms phase_domain_open
#print axioms geodesic_spray_smooth
#print axioms geodesic_spray_c1
#print axioms spray_position_component
#print axioms spray_zero_velocity
#print axioms geodesic_energy_algebra
#print axioms eventually_phase_rectangle
end
end ChatgptAudit.Screen015
