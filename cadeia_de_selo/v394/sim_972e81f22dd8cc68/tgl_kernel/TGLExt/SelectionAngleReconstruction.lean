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
import TGLExt.TheObserverReadsTheAngle
import TGLExt.TheVerbalCoupling

set_option autoImplicit false
set_option maxHeartbeats 400000

namespace ChatgptAudit.SelectionAngle
open Matrix Complex TGLExt
noncomputable section

/-- Complex phase read from the known nonzero entry of the selected face. -/
def phaseReading (A : Matrix (Fin 2) (Fin 2) ℂ) : ℂ :=
  2 * (projPlus * A) 0 0

/-- Decoder for the prescribed angular family with reciprocal phases. -/
def angularDecoder (z : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  z • projPlus + z⁻¹ • projMinus

theorem phase_reading_is_the_angular_phase (θ : ℝ) :
    phaseReading (angFamily θ) = Complex.exp ((θ : ℂ) * Complex.I) := by
  unfold phaseReading
  rw [the_observer_reads_the_angle]
  simp [Matrix.smul_apply, projPlus, genK]
  ring

theorem angular_family_reconstructed_from_one_selected_face (θ : ℝ) :
    angularDecoder (phaseReading (angFamily θ)) = angFamily θ := by
  rw [phase_reading_is_the_angular_phase]
  unfold angularDecoder
  rw [the_angle_is_the_projection]
  have hi : (Complex.exp ((θ : ℂ) * Complex.I))⁻¹ =
      Complex.exp (-(θ : ℂ) * Complex.I) := by
    rw [← Complex.exp_neg]
    congr 1
    ring
  rw [hi]

theorem one_selected_face_separates_angular_forms (θ φ : ℝ)
    (h : projPlus * angFamily θ = projPlus * angFamily φ) :
    angFamily θ = angFamily φ := by
  have hp : phaseReading (angFamily θ) = phaseReading (angFamily φ) := by
    unfold phaseReading
    rw [h]
  calc
    angFamily θ = angularDecoder (phaseReading (angFamily θ)) :=
      (angular_family_reconstructed_from_one_selected_face θ).symm
    _ = angularDecoder (phaseReading (angFamily φ)) := congrArg angularDecoder hp
    _ = angFamily φ := angular_family_reconstructed_from_one_selected_face φ

/-- Explicit bridge between the two separately named complex matrix families. -/
theorem angular_form_is_the_boundary_s_matrix (θ : ℝ) :
    angFamily θ = Smat θ := by
  rfl

theorem miguel_boundary_reconstructed_from_its_selected_face (β : ℝ) :
    angularDecoder (phaseReading (Smat (thetaMiguel β))) =
      Smat (thetaMiguel β) := by
  simpa only [angular_form_is_the_boundary_s_matrix] using
    angular_family_reconstructed_from_one_selected_face (thetaMiguel β)

/-- Selection is not injective on the ambient matrix space. -/
theorem ambient_selection_has_distinct_inputs :
    projPlus ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ) ∧
    projPlus * projPlus = projPlus * 1 := by
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    norm_num [projPlus, genK, Matrix.one_apply] at h00
  · rw [(spectral_projections_are_idempotent).1, Matrix.mul_one]

/-- A decoder on all inputs would force injectivity on those inputs. -/
theorem reconstruction_on_all_inputs_forces_injectivity
    {X Y : Type} (encode : X → Y) (decode : Y → X)
    (h : ∀ x, decode (encode x) = x) : Function.Injective encode := by
  intro x y hxy
  calc
    x = decode (encode x) := (h x).symm
    _ = decode (encode y) := congrArg decode hxy
    _ = y := h y

#print axioms phaseReading
#print axioms angularDecoder
#print axioms phase_reading_is_the_angular_phase
#print axioms angular_family_reconstructed_from_one_selected_face
#print axioms one_selected_face_separates_angular_forms
#print axioms angular_form_is_the_boundary_s_matrix
#print axioms miguel_boundary_reconstructed_from_its_selected_face
#print axioms ambient_selection_has_distinct_inputs
#print axioms reconstruction_on_all_inputs_forces_injectivity

end
end ChatgptAudit.SelectionAngle
