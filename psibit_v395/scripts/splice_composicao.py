"""Emenda 2 do Psibit.lean (v2): (a) seção 6 — pesos iguais (π/4 + kπ/2), «ponto fixo» como leitura [ONTO], entropia em todo θ de pesos iguais;
(b) seção 7 — composição INCONDICIONAL + face do psion CONDICIONAL em teorema à parte; (c) lista final de #print axioms.

Backup de bytes já feito. Temporário -> confere tamanho -> substitui. Falha se os marcadores não forem únicos.
"""
import os

P = r"C:\t\k395\final\TGLExt\Psibit.lean"

INI6 = "/-! ## 6. (6) O ponto fixo e o bit justo -/"
FIM6 = "/-! ## 6b. O colapso do psibit é um Um posto no sentido do kernel -/"
INI7 = "/-! ## 7. (7) A composição -/"

NOVO6 = '''/-! ## 6. (6) Os pesos iguais (a leitura «ponto fixo», [ONTO]) e o bit justo -/

/-- [REAL] PESOS TROCÁVEIS SOMAM A MEIA-NAT: se `cos²θ = sin²θ` então `cos²θ = 1/2` (por `observer_inverse_projection_halfnat`). -/
theorem balanced_weights_are_half {θ : ℝ} (h : Real.cos θ ^ 2 = Real.sin θ ^ 2) :
    Real.cos θ ^ 2 = 1 / 2 :=
  observer_inverse_projection_halfnat _ _ h (Real.cos_sq_add_sin_sq θ)

/-- [REAL] OS ÂNGULOS DE PESOS IGUAIS: `cos²θ = sin²θ` se e só se `θ = π/4 + kπ/2` para algum inteiro `k` (`cos 2θ = 0`). -/
theorem balanced_weights_iff {θ : ℝ} :
    Real.cos θ ^ 2 = Real.sin θ ^ 2 ↔ ∃ k : ℤ, θ = Real.pi / 4 + k * (Real.pi / 2) := by
  have h2 : Real.cos (2 * θ) = Real.cos θ ^ 2 - Real.sin θ ^ 2 := by
    rw [Real.cos_two_mul]
    nlinarith [Real.sin_sq_add_cos_sq θ]
  constructor
  · intro h
    have hc : Real.cos (2 * θ) = 0 := by rw [h2]; linarith
    obtain ⟨k, hk⟩ := Real.cos_eq_zero_iff.mp hc
    refine ⟨k, ?_⟩
    linarith
  · rintro ⟨k, hk⟩
    have hc : Real.cos (2 * θ) = 0 := Real.cos_eq_zero_iff.mpr ⟨k, by rw [hk]; ring⟩
    rw [h2] at hc
    linarith

/-- [REAL] `π/4` tem os pesos iguais: `cos²(π/4) = sin²(π/4)`. -/
theorem pi_div_four_weights_are_balanced :
    Real.cos (Real.pi / 4) ^ 2 = Real.sin (Real.pi / 4) ^ 2 := by
  rw [Real.cos_pi_div_four, Real.sin_pi_div_four]

/-- ★★ (6) [REAL] EM TODO θ DE PESOS IGUAIS (`π/4 + kπ/2`) O COLAPSO É `(1/2)•1`: os dois pesos valem ½. -/
theorem balanced_collapse_is_half {θ : ℝ} (h : Real.cos θ ^ 2 = Real.sin θ ^ 2) :
    diagExpect (rhoOut θ) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  have hcos : Real.cos θ ^ 2 = 1 / 2 := balanced_weights_are_half h
  have hsin : Real.sin θ ^ 2 = 1 / 2 := by
    have e := Real.sin_sq_add_cos_sq θ
    linarith
  have hc : ((Real.cos θ : ℝ) : ℂ) ^ 2 = 1 / 2 := by
    rw [← Complex.ofReal_pow, hcos]
    norm_num
  have hs : ((Real.sin θ : ℝ) : ℂ) ^ 2 = 1 / 2 := by
    rw [← Complex.ofReal_pow, hsin]
    norm_num
  rw [Posto.endpoint_eq, hc, hs]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- ★★ (6) [REAL; o NOME «ponto fixo» é [ONTO]] EM `θ = π/4` o colapso é `(1/2)•1`. A equação é [REAL]; ler `π/4` como «o ponto fixo» é
    leitura do operador: `π/4` não é ponto fixo de nenhuma aplicação em θ desta pedra, só representa os pesos iguais `x = 1 − x`. -/
theorem at_the_fixed_point_the_collapse_is_half :
    diagExpect (rhoOut (Real.pi / 4)) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  balanced_collapse_is_half pi_div_four_weights_are_balanced

/-- [REAL] O QUE É PONTO FIXO: `(1/2)•1` é fixado pelo colapso (`diagExpect`) e por TODA conjugação pela matriz-S,
    `S(θ)·X·S(θ)ᴴ = X` (unitariedade, `Smat_mul_conjTranspose`). Que este estado seja «o ponto fixo» sobre o qual o sistema flutua é [ONTO]. -/
theorem half_identity_is_a_fixed_point :
    diagExpect ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = (1 / 2 : ℂ) • 1
    ∧ ∀ θ : ℝ, Smat θ * ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) * (Smat θ)ᴴ
        = (1 / 2 : ℂ) • 1 := by
  refine ⟨?_, fun θ => ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [diagExpect]
  · rw [Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, Smat_mul_conjTranspose]

/-- [DEF] A entropia de Shannon (em nats) da distribuição dos RESULTADOS do colapso, `(cos²θ, 1 − cos²θ)`. Não é a entropia de
    nenhum canal físico: é a da distribuição de pesos da diagonal. -/
def collapseEntropy (θ : ℝ) : ℝ := Real.binEntropy (Real.cos θ ^ 2)

/-- ★★ (6) [REAL] EM TODO θ DE PESOS IGUAIS OS RESULTADOS DO COLAPSO SÃO O BIT JUSTO: `collapseEntropy θ = fairBitEntropy` (`= ln 2`, por
    `fair_bit_entropy_is_log_two`). -/
theorem collapseEntropy_at_balanced_weights {θ : ℝ} (h : Real.cos θ ^ 2 = Real.sin θ ^ 2) :
    collapseEntropy θ = ChatgptAudit.Collapse057.fairBitEntropy := by
  unfold collapseEntropy
  rw [balanced_weights_are_half h, ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two]
  have h2 : (1 / 2 : ℝ) = 2⁻¹ := by norm_num
  rw [h2]
  exact Real.binEntropy_two_inv

/-- ★★ (6) [REAL] Em `θ = π/4`: `collapseEntropy (π/4) = fairBitEntropy`. (Vale em todo `π/4 + kπ/2`: `collapseEntropy_at_balanced_weights`.) -/
theorem collapseEntropy_at_the_fixed_point :
    collapseEntropy (Real.pi / 4) = ChatgptAudit.Collapse057.fairBitEntropy :=
  collapseEntropy_at_balanced_weights pi_div_four_weights_are_balanced

/-- [REAL] NENHUM ÂNGULO EXCEDE O BIT JUSTO: `collapseEntropy θ ≤ fairBitEntropy`. (O limite da analogia, dito em
    `fair_bit_entropy_is_not_half_nat`: o bit justo é `ln 2`, não a meia-nat.) -/
theorem collapseEntropy_le_the_fair_bit (θ : ℝ) :
    collapseEntropy θ ≤ ChatgptAudit.Collapse057.fairBitEntropy := by
  rw [ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two]
  exact Real.binEntropy_le_log_two

'''

NOVO7 = '''/-! ## 7. (7) A composição INCONDICIONAL e, à parte, a face do psion (CONDICIONAL) -/

/-- ★★★ (7) [REAL — conjunção INCONDICIONAL, sem dedução nova além das provas acima; NENHUM certificado é hipótese] O PSIBIT É O MODO DO LEITOR,
    no que o kernel entrega: (1) o Verbo é a derivada do Nome; (2) o estado é puro, de posto 1; (3) a leitura do par não perde (decodificador
    explícito, injetividade) e é bijeção sobre o livro de códigos; (4) a densidade é reconstruída exatamente do par (peso, paridade), o sinal
    global não se observa, e o livro das perdas (amplitude: nada; densidade: só o sinal global; colapso: exatamente a paridade); (5) o
    colapso não vê a paridade e a leitura completa a lembra fora dos eixos; o bit justo vale `ln 2`; (6) nos pesos iguais (`π/4 + kπ/2`) o
    colapso é `(1/2)•1` e a entropia dos resultados é o bit justo; o Nome é a leitura de Born do posto (`reading_post_is_born`); a bandeira da
    pedra v394 (`the_binary_reading_floats_at_the_fixed_point`); a meia-nat da projeção inversa do observador; e a travessia PAGA PERDA
    (`posto_paid_loss`, geral e no colapso do psibit), ao passo que a leitura do par NÃO perde — o separante (injetivo) e o separador
    (muitos-para-um) no mesmo objeto. A FACE DO PSION NÃO está aqui: é condicional ao certificado e vive em `the_psion_face_of_the_psibit`.
    A identidade `psibit = psion = modo do leitor` NÃO é um termo: é [INPUT/ONTO] do operador (ver o cabeçalho). -/
theorem psibit_is_the_mode_of_the_reader :
    (∀ θ : ℝ, rhoOut θ 0 1 = (((1 / 2 : ℝ) * deriv (fun t => Real.cos t ^ 2) θ : ℝ) : ℂ))
    ∧ (∀ θ : ℝ, rhoOut θ 0 1 ^ 2 = rhoOut θ 0 0 * rhoOut θ 1 1)
    ∧ (∀ θ : ℝ, (rhoOut θ).rank = 1 ∧ rhoOut θ * rhoOut θ = rhoOut θ)
    ∧ (∀ θ : ℝ, decodeAmp (codeAmp θ) = v θ)
    ∧ (∀ θ θ' : ℝ, codeAmp θ = codeAmp θ' → v θ = v θ')
    ∧ (type_of% the_orbit_is_in_bijection_with_the_code_book)
    ∧ (∀ θ : ℝ, rhoOut θ = decodeRho (rhoWeight θ) (rhoParity θ))
    ∧ (∀ θ : ℝ, rhoOut (θ + Real.pi) = rhoOut θ)
    ∧ (type_of% the_ledger_of_losses)
    ∧ (∀ θ : ℝ, diagExpect (rhoOut θ) = diagExpect (rhoOut (-θ)))
    ∧ (∀ θ : ℝ, Real.sin (2 * θ) ≠ 0 → rhoOut θ ≠ rhoOut (-θ))
    ∧ ChatgptAudit.Collapse057.fairBitEntropy = Real.log 2
    ∧ (∀ θ : ℝ, Real.cos θ ^ 2 = Real.sin θ ^ 2 →
        diagExpect (rhoOut θ) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
          ∧ collapseEntropy θ = ChatgptAudit.Collapse057.fairBitEntropy)
    ∧ diagExpect (rhoOut (Real.pi / 4)) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
    ∧ (∀ θ : ℝ, TheVerbSelectsTheAction.reading (TheVerbSelectsTheAction.post basis0) (stateVec θ)
        = ((rhoWeight θ : ℝ) : ℂ))
    ∧ (type_of% the_binary_reading_floats_at_the_fixed_point)
    ∧ (∀ ωP ωQ : ℝ, ωP = ωQ → ωP + ωQ = 1 → ωP = 1 / 2)
    ∧ (∀ {S I : Type} (P : UmPostoRelacao.UmPosto S I),
        ¬ ∃ R : S → S, Function.LeftInverse R P.crossing.step)
    ∧ (¬ ∃ R : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ,
        Function.LeftInverse R diagExpect) :=
  ⟨the_verb_is_the_derivative_of_the_name,
   the_state_is_pure,
   the_state_is_a_rank_one_projector,
   decodeAmp_codeAmp,
   fun θ θ' h => (codeAmp_eq_iff θ θ').1 h,
   the_orbit_is_in_bijection_with_the_code_book,
   rhoOut_eq_decodeRho,
   fun θ => (the_global_sign_is_not_observed θ).2.2.2.2.2,
   the_ledger_of_losses,
   collapse_forgets_the_parity,
   fun _ h => the_full_reading_remembers_the_parity h,
   ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two,
   fun _ h => ⟨balanced_collapse_is_half h, collapseEntropy_at_balanced_weights h⟩,
   at_the_fixed_point_the_collapse_is_half,
   the_name_is_the_born_reading_of_the_post,
   the_binary_reading_floats_at_the_fixed_point,
   observer_inverse_projection_halfnat,
   fun P => UmPostoRelacao.posto_paid_loss P,
   the_psibit_crossing_pays_loss⟩

/-- ★ [REAL — CONDICIONAL AO CERTIFICADO] A FACE DO PSION: para todo certificado `C : FockCertificate L`, o psion tem `⟨ψ, ψ⟩ = 1`
    (`inner_psion_psion`) e é fixado pela luz, `Δ^{it} ψ = ψ` para todo `t` (`psion_is_fixed_by_the_light`).
    ⚠ O KERNEL NÃO HABITA `FockCertificate`: `TheImportedSecondQuantization` (l.66–67, «NÃO-VACUIDADE») diz que nenhum habitante é exibido e que a
    não-vacuidade é ARGUMENTADA, não provada; só há o construtor, `TetelestaiOneObject.rescale` (que exige outro certificado) e os montadores da v394
    (`F1Fecho394/*Assembly*`), que partem de entradas restantes sem habitante exibido («not a claim that the remaining imported fields are
    inhabited»). Logo este enunciado é uma IMPLICAÇÃO sobre um tipo sem habitante conhecido: NÃO mostra que o psion exista; o contrato conjunto da
    rede segue aberto (v394). Por isso NÃO é parte de `psibit_is_the_mode_of_the_reader`, que é incondicional. NENHUM lema liga `psion C` a
    `codeAmp`: `psibit = psion = modo do leitor` é [INPUT/ONTO] do operador. -/
theorem the_psion_face_of_the_psibit :
    ∀ {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L),
      inner ℂ (ThePsionAndTheViscosity.psion C) (ThePsionAndTheViscosity.psion C) = 1
      ∧ (∀ t : ℝ, ImportedSQ.lightDelta C t (ThePsionAndTheViscosity.psion C)
          = ThePsionAndTheViscosity.psion C) :=
  fun C => ⟨ThePsionAndTheViscosity.inner_psion_psion C,
    ThePsionAndTheViscosity.psion_is_fixed_by_the_light C⟩

end

end TGLExt.Psibit

#print axioms TGLExt.Psibit.the_verb_is_the_derivative_of_the_name
#print axioms TGLExt.Psibit.the_state_is_pure
#print axioms TGLExt.Psibit.decodeAmp_codeAmp
#print axioms TGLExt.Psibit.codeAmp_injOn
#print axioms TGLExt.Psibit.the_orbit_is_in_bijection_with_the_code_book
#print axioms TGLExt.Psibit.the_pair_is_necessary_and_sufficient
#print axioms TGLExt.Psibit.rhoOut_eq_decodeRho
#print axioms TGLExt.Psibit.the_density_is_its_code
#print axioms TGLExt.Psibit.the_global_sign_is_not_observed
#print axioms TGLExt.Psibit.only_the_global_sign_is_lost
#print axioms TGLExt.Psibit.the_ledger_of_losses
#print axioms TGLExt.Psibit.collapse_forgets_the_parity
#print axioms TGLExt.Psibit.the_full_reading_remembers_the_parity
#print axioms TGLExt.Psibit.the_collapse_loses_exactly_the_parity
#print axioms TGLExt.Psibit.the_collapse_has_no_left_inverse_on_the_orbit
#print axioms TGLExt.Psibit.balanced_weights_iff
#print axioms TGLExt.Psibit.balanced_collapse_is_half
#print axioms TGLExt.Psibit.at_the_fixed_point_the_collapse_is_half
#print axioms TGLExt.Psibit.half_identity_is_a_fixed_point
#print axioms TGLExt.Psibit.collapseEntropy_at_balanced_weights
#print axioms TGLExt.Psibit.collapseEntropy_at_the_fixed_point
#print axioms TGLExt.Psibit.the_psibit_crossing_pays_loss
#print axioms TGLExt.Psibit.the_name_is_the_born_reading_of_the_post
#print axioms TGLExt.Psibit.psibit_is_the_mode_of_the_reader
#print axioms TGLExt.Psibit.the_psion_face_of_the_psibit
'''

b = open(P, "rb").read()
assert b"\r\n" not in b, "o arquivo tem CRLF; abortar"
s = b.decode("utf-8")
for m in (INI6, FIM6, INI7):
    assert s.count(m) == 1, ("marcador nao unico", m, s.count(m))
i6, f6, i7 = s.index(INI6), s.index(FIM6), s.index(INI7)
assert i6 < f6 < i7
novo = s[:i6] + NOVO6 + s[f6:i7] + NOVO7
tmp = P + ".tmp_emenda2"
open(tmp, "wb").write(novo.encode("utf-8"))
tam = os.path.getsize(tmp)
assert tam > 0 and tam > len(b) - 6000, ("tamanho suspeito", tam, len(b))
os.replace(tmp, P)
print("emenda 2 ok:", len(b), "->", tam, "bytes")
