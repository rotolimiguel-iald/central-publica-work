-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_032 (06/09/2026), transposta em 06/09/2026
-- Lote 031..032: o OPERADOR MODULAR RELATIVO com dominio e fecho — S^0_{psi|omega}(A Omega) = A* Psi,
--   grafico relativo fechado por homeomorfismo dos graficos algebricos, dominio denso, adjunto antilinear
--   maximal, congruencia limitada (auto-adjunta, positiva) e Delta_rel = S*S com dominio, fecho,
--   auto-adjunticidade e positividade; e a COMUTACAO MODULAR: separacao de frequencias reais, reconhecimento
--   do grafico de Delta por testes fracos, B limitado auto-adjunto comutando com o fluxo preserva o dominio
--   de Delta e comuta; o filtro e o inverso preservam o dominio; IGUALDADE dos dominios de Delta relativo e
--   de referencia e igualdade dos operadores parciais (Delta_rel = produto de verossimilhanca x Delta_omega
--   como LinearPMap), positivo, auto-adjunto, fechado. Estatuto [REAL / INPUT / OPEN]: familia comutante
--   especificada (referencia 1/3,2/3; b somavel); calculo funcional/potencias relativas, identificacao
--   Connes/Araki completa, area geometrica e reconstrucao geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 12/12 + 12/12; manifestos 254/259; 2/2
--   auditores exit 0; recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao estatica no ROOT;
--   enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ModularFlowSpectrum
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Commutation032
open ChatgptAudit
noncomputable section

theorem phase_frequency_separation (a b : ℝ) (c : ℂ) (hc : c≠0)
    (h : ∀ s : ℝ,
      Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c=
      Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) :
    a=b := by
  have hd (r : ℝ) :
      HasDerivAt
        (fun s : ℝ => Complex.exp ((s : ℂ)*Complex.I*(r : ℂ))*c)
        ((Complex.I*(r : ℂ))*c) 0 := by
    have hr :=
      (((((hasDerivAt_id (0 : ℝ)).ofReal_comp).mul_const Complex.I).mul_const
        (r : ℂ)).cexp).mul_const c
    simpa using hr
  have hf :
      (fun s : ℝ => Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c)=
      (fun s : ℝ => Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) :=
    funext h
  have ha := hd a
  rw [hf] at ha
  have hfreq := mul_right_cancel₀ hc (ha.unique (hd b))
  exact Complex.ofReal_injective
    (mul_left_cancel₀ Complex.I_ne_zero hfreq)

theorem modular_phase_exponential (s a : ℝ) :
    modularPhase s a=Complex.exp ((s : ℂ)*Complex.I*(a : ℂ)) := by
  unfold modularPhase
  congr 1
  push_cast
  ring

theorem modular_phase_frequency_separation (a b : ℝ) (c : ℂ) (hc : c≠0)
    (h : ∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) :
    a=b := by
  apply phase_frequency_separation a b c hc
  intro s
  simpa only [modular_phase_exponential] using h s

theorem phase_frequency_zero_or_equal (a b : ℝ) (c : ℂ)
    (h : ∀ s : ℝ,
      Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c=
      Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) :
    c=0 ∨ a=b := by
  by_cases hc : c=0
  · exact Or.inl hc
  · exact Or.inr (phase_frequency_separation a b c hc h)

theorem modular_phase_frequency_zero_or_equal (a b : ℝ) (c : ℂ)
    (h : ∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) :
    c=0 ∨ a=b := by
  by_cases hc : c=0
  · exact Or.inl hc
  · exact Or.inr (modular_phase_frequency_separation a b c hc h)

theorem modular_phase_frequency_iff (a b : ℝ) (c : ℂ) :
    (∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) ↔ c=0 ∨ a=b := by
  constructor
  · exact modular_phase_frequency_zero_or_equal a b c
  · rintro (rfl | rfl) s <;> simp

#print axioms phase_frequency_separation
#print axioms modular_phase_exponential
#print axioms modular_phase_frequency_separation
#print axioms phase_frequency_zero_or_equal
#print axioms modular_phase_frequency_zero_or_equal
#print axioms modular_phase_frequency_iff

end
end ChatgptAudit.Commutation032
