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
import TGLExt.StaticDynamicMixture

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.StaticDynamicUnitary
open Matrix Filter Topology Set ChatgptAudit.Micro021 ChatgptAudit.JointUnitary
  ChatgptAudit.StaticDynamic ChatgptAudit.Unitary022
noncomputable section
variable {ι κ : Type} [Fintype ι] [Fintype κ]

def mixedLabelEquiv : (ι ⊕ (Fin 2 × κ)) ≃ (ι ⊕ (κ × Fin 2)) :=
  Equiv.sumCongr (Equiv.refl ι) (Equiv.prodComm (Fin 2) κ)

def mixedBlockFlow [DecidableEq ι] [DecidableEq κ]
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) (t : ℝ) :
    Matrix (ι ⊕ (Fin 2 × κ)) (ι ⊕ (Fin 2 × κ)) ℂ :=
  Matrix.fromBlocks 1 0 0 (jointBlockFlow C frequency (Real.sqrt 2*t))

theorem mixed_block_flow_unitary [DecidableEq ι] [DecidableEq κ]
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) (t : ℝ) :
    (mixedBlockFlow (ι := ι) C frequency t)ᴴ * mixedBlockFlow C frequency t = 1 ∧
      mixedBlockFlow (ι := ι) C frequency t * (mixedBlockFlow C frequency t)ᴴ = 1 := by
  have h := joint_block_flow_unitary C frequency (Real.sqrt 2*t)
  constructor
  · simp only [mixedBlockFlow, Matrix.fromBlocks_conjTranspose, Matrix.conjTranspose_one,
      Matrix.conjTranspose_zero, Matrix.fromBlocks_multiply, Matrix.one_mul, Matrix.mul_zero,
      Matrix.zero_mul, add_zero, zero_add, h.1, Matrix.fromBlocks_one]
  · simp only [mixedBlockFlow, Matrix.fromBlocks_conjTranspose, Matrix.conjTranspose_one,
      Matrix.conjTranspose_zero, Matrix.fromBlocks_multiply, Matrix.one_mul, Matrix.mul_zero,
      Matrix.zero_mul, add_zero, zero_add, h.2, Matrix.fromBlocks_one]

omit [Fintype ι] in
theorem mixed_block_flow_zero [DecidableEq ι] [DecidableEq κ]
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) :
    mixedBlockFlow (ι := ι) C frequency 0 = 1 := by
  simp only [mixedBlockFlow, jointBlockFlow, mul_zero, pair_flow_zero]
  have h : Matrix.blockDiagonal (fun _ : κ => (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1 :=
    Matrix.blockDiagonal_one
  rw [h]
  exact Matrix.fromBlocks_one

def mixedInitialAmplitude (q : ι → ℝ) (C : UnitaryLabelData κ) :
    ι ⊕ (Fin 2 × κ) → ℂ :=
  Sum.elim
    (fun i => (Real.sqrt (1/2 : ℝ) : ℂ) * (Real.sqrt (q i) : ℂ))
    (fun k => (Real.sqrt (1/2 : ℝ) : ℂ) * jointInitialAmplitude C k)

def mixedBlockAmplitude (q : ι → ℝ) (C : UnitaryLabelData κ)
    (frequency : κ → ℝ) (t : ℝ) : ι ⊕ (Fin 2 × κ) → ℂ :=
  Sum.elim
    (fun i => (Real.sqrt (1/2 : ℝ) : ℂ) * (Real.sqrt (q i) : ℂ))
    (fun k => (Real.sqrt (1/2 : ℝ) : ℂ) *
      jointBlockAmplitude C frequency (Real.sqrt 2*t) k)

theorem mixed_block_flow_prepares_amplitude [DecidableEq ι] [DecidableEq κ]
    (q : ι → ℝ) (C : UnitaryLabelData κ) (frequency : κ → ℝ) (t : ℝ) :
    mixedBlockFlow C frequency t *ᵥ mixedInitialAmplitude q C =
      mixedBlockAmplitude q C frequency t := by
  unfold mixedBlockFlow
  rw [Matrix.fromBlocks_mulVec]
  have hl : mixedInitialAmplitude q C ∘ Sum.inl =
      (fun i => (Real.sqrt (1/2 : ℝ) : ℂ) * (Real.sqrt (q i) : ℂ)) := rfl
  have hr : mixedInitialAmplitude q C ∘ Sum.inr =
      (Real.sqrt (1/2 : ℝ) : ℂ) • jointInitialAmplitude C := rfl
  rw [hl, hr, Matrix.one_mulVec, Matrix.zero_mulVec, add_zero,
    Matrix.zero_mulVec, zero_add, Matrix.mulVec_smul, joint_block_flow_prepares_amplitude]
  rfl

theorem mixed_block_amplitude_zero [DecidableEq ι] [DecidableEq κ]
    (q : ι → ℝ) (C : UnitaryLabelData κ) (frequency : κ → ℝ) :
    mixedBlockAmplitude q C frequency 0 = mixedInitialAmplitude q C := by
  have h := mixed_block_flow_prepares_amplitude q C frequency 0
  rw [mixed_block_flow_zero, Matrix.one_mulVec] at h
  exact h.symm

theorem sqrt_half_amplitude_weight (z : ℂ) :
    ((Real.sqrt (1/2 : ℝ) : ℂ)*z) * star ((Real.sqrt (1/2 : ℝ) : ℂ)*z) =
      ((1/2 : ℝ) : ℂ)*(z*star z) := by
  have hs : (Real.sqrt (1/2 : ℝ) : ℂ)^2 = ((1/2 : ℝ) : ℂ) := by
    exact_mod_cast Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1/2)
  calc
    _ = (Real.sqrt (1/2 : ℝ) : ℂ)^2*(z*star z) := by
      simp only [star_mul, Complex.star_def, Complex.conj_ofReal]
      ring
    _ = _ := by rw [hs]

theorem mixed_block_amplitude_weights
    (q : ι → ℝ) (hq : ∑ i, q i = 1) (hqp : ∀ i, 0 ≤ q i)
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) (t : ℝ)
    (k : ι ⊕ (Fin 2 × κ)) :
    mixedBlockAmplitude q C frequency t k * star (mixedBlockAmplitude q C frequency t k) =
      (((mixedCurve q hq (jointUnitaryCurve C frequency)).weights t
        (mixedLabelEquiv k)) : ℂ) := by
  cases k with
  | inl i =>
    have hs : (Real.sqrt (q i) : ℂ)^2 = (q i : ℂ) := by
      exact_mod_cast Real.sq_sqrt (hqp i)
    change ((Real.sqrt (1/2 : ℝ) : ℂ)*(Real.sqrt (q i) : ℂ)) *
      star ((Real.sqrt (1/2 : ℝ) : ℂ)*(Real.sqrt (q i) : ℂ)) =
        (((1/2 : ℝ)*q i : ℝ) : ℂ)
    rw [sqrt_half_amplitude_weight]
    simp only [Complex.star_def, Complex.conj_ofReal, ← pow_two, hs, Complex.ofReal_mul]
  | inr k =>
    change ((Real.sqrt (1/2 : ℝ) : ℂ)*jointBlockAmplitude C frequency (Real.sqrt 2*t) k) *
      star ((Real.sqrt (1/2 : ℝ) : ℂ)*jointBlockAmplitude C frequency (Real.sqrt 2*t) k) =
        (((1/2 : ℝ)*jointWeights C frequency (Real.sqrt 2*t) (k.2,k.1) : ℝ) : ℂ)
    rw [sqrt_half_amplitude_weight, joint_block_amplitude_weights]
    exact (Complex.ofReal_mul _ _).symm

theorem mixed_block_amplitude_normalized
    (q : ι → ℝ) (hq : ∑ i, q i = 1) (hqp : ∀ i, 0 ≤ q i)
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) (t : ℝ) :
    ∑ k, mixedBlockAmplitude q C frequency t k * star (mixedBlockAmplitude q C frequency t k) =
      (1 : ℂ) := by
  calc
    _ = ∑ k, (((mixedCurve q hq (jointUnitaryCurve C frequency)).weights t k) : ℂ) := by
      exact Fintype.sum_equiv mixedLabelEquiv _ _
        (fun k => mixed_block_amplitude_weights q hq hqp C frequency t k)
    _ = 1 := by
      exact_mod_cast (mixedCurve q hq (jointUnitaryCurve C frequency)).trace_one t

theorem mixed_initial_amplitude_normalized [DecidableEq ι] [DecidableEq κ]
    (q : ι → ℝ) (hq : ∑ i, q i = 1) (hqp : ∀ i, 0 ≤ q i)
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) :
    ∑ k, mixedInitialAmplitude q C k * star (mixedInitialAmplitude q C k) = (1 : ℂ) := by
  rw [← mixed_block_amplitude_zero q C frequency]
  exact mixed_block_amplitude_normalized q hq hqp C frequency 0

theorem mixed_flow_diagonal_readout [DecidableEq ι] [DecidableEq κ]
    (q : ι → ℝ) (hq : ∑ i, q i = 1) (hqp : ∀ i, 0 ≤ q i)
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) (t : ℝ)
    (k : ι ⊕ (Fin 2 × κ)) :
    (mixedBlockFlow C frequency t *ᵥ mixedInitialAmplitude q C) k *
      star ((mixedBlockFlow C frequency t *ᵥ mixedInitialAmplitude q C) k) =
      (((mixedCurve q hq (jointUnitaryCurve C frequency)).weights t (mixedLabelEquiv k)) : ℂ) := by
  rw [mixed_block_flow_prepares_amplitude]
  exact mixed_block_amplitude_weights q hq hqp C frequency t k

#print axioms mixedLabelEquiv
#print axioms mixedBlockFlow
#print axioms mixed_block_flow_unitary
#print axioms mixed_block_flow_zero
#print axioms mixedInitialAmplitude
#print axioms mixedBlockAmplitude
#print axioms mixed_block_flow_prepares_amplitude
#print axioms mixed_block_amplitude_zero
#print axioms sqrt_half_amplitude_weight
#print axioms mixed_block_amplitude_weights
#print axioms mixed_block_amplitude_normalized
#print axioms mixed_initial_amplitude_normalized
#print axioms mixed_flow_diagonal_readout
end
end ChatgptAudit.StaticDynamicUnitary
