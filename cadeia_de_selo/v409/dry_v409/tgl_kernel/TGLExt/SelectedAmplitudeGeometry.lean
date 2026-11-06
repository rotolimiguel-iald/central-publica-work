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
import TGLExt.StateClockObstruction
import TGLExt.TheSelectionIsTheBallast
import TGLExt.PlaneWaveReconstructionControls

set_option autoImplicit false
set_option maxHeartbeats 4000000
set_option maxRecDepth 4096

namespace ChatgptAudit.SelectedGeometry
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Response028 ChatgptAudit.Thermal025 ChatgptAudit.Clock040
  ChatgptAudit.Wave029 ChatgptAudit.Coherent023 ChatgptAudit.Flow019
  ChatgptAudit.Flow020 ChatgptAudit.Micro021 ChatgptAudit.Profile026
noncomputable section

/-- Probability read on the common reference Hilbert space. -/
def selectedSiteProbability (b : SummableAmplitude) (t : ℝ) (n : ℕ) : ℝ :=
  (amplitudeState b t (siteMark thirdThermalReference n)).re

theorem selected_site_probability_formula (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    selectedSiteProbability b t n = 1/3-b.value n*regularParameter t := by
  simp only [selectedSiteProbability, amplitude_state_site_mark, Complex.ofReal_re]

theorem selected_site_probability_bounds (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    0 < selectedSiteProbability b t n ∧ selectedSiteProbability b t n < 1 := by
  rw [selected_site_probability_formula]
  exact ⟨(amplitudeProfile b t).pos n, (amplitudeProfile b t).lt_one n⟩

def selectedSiteAngle (b : SummableAmplitude) (t : ℝ) (n : ℕ) : ℝ :=
  selectionAngle (selectedSiteProbability b t n)

theorem selected_angle_recovers_probability (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    Real.sin (selectedSiteAngle b t n)^2 = selectedSiteProbability b t n :=
  selection_angle_reflection (selected_site_probability_bounds b t n).1.le
    (selected_site_probability_bounds b t n).2.le

def recoveredSiteAmplitude (t : ℝ) (angles : ℕ → ℝ) (n : ℕ) : ℝ :=
  (1/3-Real.sin (angles n)^2)/regularParameter t

theorem selected_angle_recovers_amplitude (b : SummableAmplitude) (t : ℝ) (ht : t ≠ 0)
    (n : ℕ) : recoveredSiteAmplitude t (selectedSiteAngle b t) n = b.value n := by
  unfold recoveredSiteAmplitude
  rw [selected_angle_recovers_probability, selected_site_probability_formula]
  have hr : regularParameter t ≠ 0 := (regular_parameter_positive t ht).ne'
  field_simp
  ring

/-- Admissibility concerns the decoded amplitude, not a gravitational equation. -/
structure AngularAmplitudeRecord where
  preparation : ℝ
  preparation_ne_zero : preparation ≠ 0
  angles : ℕ → ℝ
  nonnegative : ∀ n, 0 ≤ recoveredSiteAmplitude preparation angles n
  bounded : ∀ n, recoveredSiteAmplitude preparation angles n ≤ 1/12
  summable : Summable (recoveredSiteAmplitude preparation angles)

def decodeAmplitude (R : AngularAmplitudeRecord) : SummableAmplitude where
  value := recoveredSiteAmplitude R.preparation R.angles
  nonnegative := R.nonnegative
  bound := R.bounded
  summable := R.summable

def encodeAmplitude (b : SummableAmplitude) (t : ℝ) (ht : t ≠ 0) : AngularAmplitudeRecord where
  preparation := t
  preparation_ne_zero := ht
  angles := selectedSiteAngle b t
  nonnegative := by
    intro n
    rw [selected_angle_recovers_amplitude b t ht]
    exact b.nonnegative n
  bounded := by
    intro n
    rw [selected_angle_recovers_amplitude b t ht]
    exact b.bound n
  summable := by
    have h : recoveredSiteAmplitude t (selectedSiteAngle b t) = b.value := by
      funext n
      exact selected_angle_recovers_amplitude b t ht n
    rw [h]
    exact b.summable

theorem decoded_amplitude_round_trip (b : SummableAmplitude) (t : ℝ) (ht : t ≠ 0) :
    decodeAmplitude (encodeAmplitude b t ht) = b := by
  have hv : (decodeAmplitude (encodeAmplitude b t ht)).value = b.value := by
    funext n
    exact selected_angle_recovers_amplitude b t ht n
  have hext : ∀ a c : SummableAmplitude, a.value = c.value → a = c := by
    rintro ⟨av, an, ab, asum⟩ ⟨cv, cn, cb, csum⟩ h
    cases h
    rfl
  exact hext _ _ hv

/-- Every admissible record is realized at the probability level, without fixing an angle branch. -/
theorem decoded_probability_realizes_record (R : AngularAmplitudeRecord) (n : ℕ) :
    selectedSiteProbability (decodeAmplitude R) R.preparation n = Real.sin (R.angles n)^2 := by
  rw [selected_site_probability_formula]
  change 1/3-((1/3-Real.sin (R.angles n)^2)/regularParameter R.preparation)*
    regularParameter R.preparation = _
  have hr : regularParameter R.preparation ≠ 0 :=
    (regular_parameter_positive R.preparation R.preparation_ne_zero).ne'
  field_simp
  ring

def recoveredMass (R : AngularAmplitudeRecord) : ℝ :=
  ∑' n, recoveredSiteAmplitude R.preparation R.angles n

theorem recovered_mass_is_amplitude_mass (R : AngularAmplitudeRecord) :
    recoveredMass R = amplitudeMass (decodeAmplitude R) := rfl

theorem recovered_mass_round_trip (b : SummableAmplitude) (t : ℝ) (ht : t ≠ 0) :
    recoveredMass (encodeAmplitude b t ht) = amplitudeMass b := by
  rw [recovered_mass_is_amplitude_mass, decoded_amplitude_round_trip]

theorem recovered_mass_prefix_converges (R : AngularAmplitudeRecord) :
    Tendsto (fun N => ∑ n ∈ Finset.range (N+1), recoveredSiteAmplitude R.preparation R.angles n)
      atTop (𝓝 (recoveredMass R)) :=
  amplitude_prefix_tendsto (decodeAmplitude R)

/-- eta and shear are explicit additional data in the fixed chart and frame. -/
def selectedWaveSolder (R : AngularAmplitudeRecord) (eta shear : ℝ) : TensorField4 :=
  matchedSolder (decodeAmplitude R) eta shear

def selectedWaveInverse (R : AngularAmplitudeRecord) (eta shear : ℝ) : TensorField4 :=
  matchedInverseSolder (decodeAmplitude R) eta shear

def selectedWaveMatter (R : AngularAmplitudeRecord) (eta shear : ℝ) : TensorField4 :=
  frameCovectorStress (selectedWaveSolder R eta shear) (selectedWaveInverse R eta shear)
    waveCovectorField (amplitudeCoupling (decodeAmplitude R))

theorem selected_source_is_read_mass (R : AngularAmplitudeRecord) :
    amplitudeCoupling (decodeAmplitude R) = Real.log 2*recoveredMass R/Real.pi := rfl

theorem selected_wave_reconstruction (b : SummableAmplitude) (t : ℝ) (ht : t ≠ 0)
    (eta shear : ℝ) :
    selectedWaveSolder (encodeAmplitude b t ht) eta shear = matchedSolder b eta shear ∧
    selectedWaveInverse (encodeAmplitude b t ht) eta shear = matchedInverseSolder b eta shear := by
  simp only [selectedWaveSolder, selectedWaveInverse, decoded_amplitude_round_trip, and_self]

theorem selected_wave_einstein (R : AngularAmplitudeRecord) (eta shear : ℝ) (heta : eta ≠ 0) :
    ∃ cosmological : ℝ, ∀ x ∈ (univ : Set Coordinate4),
      frameEinsteinTensor (selectedWaveSolder R eta shear) (selectedWaveInverse R eta shear) x +
        cosmological • frameMetricField (selectedWaveSolder R eta shear) x =
        (2*Real.pi/eta) • selectedWaveMatter R eta shear x :=
  matched_wave_einstein_from_area (decodeAmplitude R) eta shear heta

theorem selected_wave_area_matching (R : AngularAmplitudeRecord) (eta shear : ℝ)
    (heta : eta ≠ 0) (x d : Coordinate4) (hd : d ≠ 0)
    (hn : tensorQuad (frameMetricField (selectedWaveSolder R eta shear) x) d = 0) :
    let P := matchedScreen (decodeAmplitude R) eta shear x d hd hn
    Tendsto (fun t => amplitudeAreaDefect (decodeAmplitude R) (covectorRead waveCovector d) eta
      (inducedArea (frameMetricField (selectedWaveSolder R eta shear)) P.curve P.screen.vectors) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  matched_constructed_area (decodeAmplitude R) eta shear heta x d hd hn

theorem equal_read_mass_same_solder (R Q : AngularAmplitudeRecord) (eta shear : ℝ)
    (hm : recoveredMass R = recoveredMass Q) :
    selectedWaveSolder R eta shear = selectedWaveSolder Q eta shear := by
  have hc : amplitudeCoupling (decodeAmplitude R) = amplitudeCoupling (decodeAmplitude Q) := by
    rw [selected_source_is_read_mass, selected_source_is_read_mass, hm]
  unfold selectedWaveSolder matchedSolder matchedLeft matchedRight waveRicciScale
  rw [hc]

theorem omitted_shear_changes_curvature (R : AngularAmplitudeRecord) (eta s s' : ℝ)
    (hs : s ≠ s') (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (selectedWaveSolder R eta s)
      (selectedWaveInverse R eta s)) x 1 0 1 0 ≠
    coordinateCurvature (frameLeviCivita (selectedWaveSolder R eta s')
      (selectedWaveInverse R eta s')) x 1 0 1 0 :=
  matched_curvature_distinguishes (decodeAmplitude R) eta s s' hs x

/-- General criterion: only the target geometry, not the whole state, must descend. -/
theorem geometry_decoder_exists_iff {S R G : Type} (read : S → R) (geom : S → G) :
    (∃ decode : Set.range read → G,
      ∀ x, decode ⟨read x, ⟨x, rfl⟩⟩ = geom x) ↔
    (∀ x y, read x = read y → geom x = geom y) := by
  constructor
  · rintro ⟨decode, hd⟩ x y hxy
    have hs : (⟨read x, ⟨x, rfl⟩⟩ : Set.range read) = ⟨read y, ⟨y, rfl⟩⟩ :=
      Subtype.ext hxy
    rw [← hd x, ← hd y, hs]
  · intro hf
    classical
    let decode : Set.range read → G := fun r => geom (Classical.choose r.property)
    refine ⟨decode, ?_⟩
    intro x
    exact hf _ x (Classical.choose_spec (show ∃ y, read y = read x from ⟨x, rfl⟩))

/-- The decoder is unique on the image, with no assertion of effective or stable computation. -/
theorem geometry_decoder_unique {S R G : Type} (read : S → R) (geom : S → G)
    (d e : Set.range read → G)
    (hd : ∀ x, d ⟨read x, ⟨x, rfl⟩⟩ = geom x)
    (he : ∀ x, e ⟨read x, ⟨x, rfl⟩⟩ = geom x) : d = e := by
  funext r
  rcases r with ⟨r, x, rfl⟩
  exact (hd x).trans (he x).symm

#print axioms decoded_probability_realizes_record
#print axioms selected_wave_area_matching
#print axioms geometry_decoder_unique
#print axioms selectedSiteProbability
#print axioms selected_site_probability_formula
#print axioms selected_site_probability_bounds
#print axioms selectedSiteAngle
#print axioms selected_angle_recovers_probability
#print axioms recoveredSiteAmplitude
#print axioms selected_angle_recovers_amplitude
#print axioms AngularAmplitudeRecord
#print axioms decodeAmplitude
#print axioms encodeAmplitude
#print axioms decoded_amplitude_round_trip
#print axioms recoveredMass
#print axioms recovered_mass_is_amplitude_mass
#print axioms recovered_mass_round_trip
#print axioms recovered_mass_prefix_converges
#print axioms selectedWaveSolder
#print axioms selectedWaveInverse
#print axioms selectedWaveMatter
#print axioms selected_source_is_read_mass
#print axioms selected_wave_reconstruction
#print axioms selected_wave_einstein
#print axioms equal_read_mass_same_solder
#print axioms omitted_shear_changes_curvature
#print axioms geometry_decoder_exists_iff

end
end ChatgptAudit.SelectedGeometry
