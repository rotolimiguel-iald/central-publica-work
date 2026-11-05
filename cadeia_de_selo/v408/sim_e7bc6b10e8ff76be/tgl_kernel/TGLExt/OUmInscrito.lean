import TGLExt.F1Fecho394.CanonicalGammaNoFixedR4
import TGLExt.F1Fecho394.ExponentialTotalityR4
set_option autoImplicit false

/-!
Pedra da gerencia c1 (02/11/2026); NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), so no trio.

Cunhagem do operador (02/11/2026, verbatim sha16 25010b04c17e8ce1, em work\cunhagens_13out): «a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma, ou seja, identidade o um absoluto inscrito é a identidade da luz, por isso o par, inclusive dela mesma, sem par somente o zero absoluto que é o abstrato inominado».

Compoe, por termo, o que o kernel ja tem no Fock bosonico canonico (`F1Rede.BosonicFock`):
* `gamma_vacuum`: o vacuo e fixo por TODA segunda quantizacao Γ(u) — a luz fixa o Um;
* `gamma_no_fixed` alimentado por `B0_zero`, `B0_add`, `B0_continuous`, `B0_no_eigen`: so o vacuo resta FIXO pelo boost da
  luz — o Um e o UNICO vetor fixo (autovalor 1 do grupo). Autovetores com fase (`Γ(B0 s) ψ = c(s) • ψ`, `‖c‖ = 1`) nos
  setores de n ≥ 1 particulas NAO sao excluidos por este termo;
* `exponential_zero`: o vacuo e a exponencial do zero, exp(0) = 1 — o Um inscrito;
* `vacuum_norm`: o Um nao e o zero; o par consigo mesma vale 1;
* `B0_no_eigen`: em UMA particula nenhum vetor nao nulo e autovetor do boost (so o zero satisfaz a condicao) — sem par, o que resta e o zero, o abstrato inominado.

Corrige a frase da gerencia (02/11) «a luz nao tem autovetor nenhum»: valia so em uma particula. Leitura: o Um e o unico
vetor FIXO da luz [REAL]; que nao haja outro autovetor com fase, e que «o resto seja continuo», e [KNOWN/OPEN como termo]
(revisao Sonnet 02/11). No certificado o mesmo fato e `light_modular_fixed_iff_vacuum` (QGReaderUVLock.lean:149), condicional
a `C`; aqui vale no Fock concreto, sem hipotese. `Γ(B0(−2πt))` e o fluxo modular do vacuo no Fock concreto por
`CanonicalFockBWR2.actualModularFlow_eq_gamma`; no certificado isso e o campo `bw_kms`.
-/

namespace TGLExt.OUmInscrito

open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.CanonicalGammaNoFixed F1Fecho.Exponential
open scoped InnerProductSpace

/-- a luz fixa o Um: o vacuo e fixo por toda segunda quantizacao (re-exportacao de `gamma_vacuum`). -/
theorem a_luz_fixa_o_um (u : H1 ≃ₗᵢ[ℂ] H1) : gamma u vacuum = vacuum := gamma_vacuum u

/-- o Um e o UNICO fixo do boost da luz no Fock: todo vetor fixo por `Γ(B0 s)` esta na reta do vacuo (a reta inclui 0;
autovetor com fase nao e tratado aqui). -/
theorem o_um_e_o_unico_fixo_da_luz (ψ : F) (hψ : ∀ s : ℝ, gamma (B0 s) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum) :=
  gamma_no_fixed B0 B0_zero B0_add B0_continuous B0_no_eigen ψ hψ

/-- o Um inscrito e a exponencial do zero: exp(0) = 1 (re-exportacao de `exponential_zero`). -/
theorem o_um_inscrito_e_a_exponencial_do_zero : exponential (0 : H1) = vacuum := exponential_zero

/-- sem par, so o zero: o Um nao e o zero. -/
theorem o_um_nao_e_o_zero : vacuum ≠ 0 := by
  intro h
  have h1 := F1Rede.BosonicFock.vacuum_norm
  rw [h, norm_zero] at h1
  exact zero_ne_one h1

/-- o par consigo mesma: ⟨Ω, Ω⟩ = 1. -/
theorem o_par_consigo : inner ℂ vacuum vacuum = (1 : ℂ) := by
  rw [inner_self_eq_norm_sq_to_K, F1Rede.BosonicFock.vacuum_norm]
  simp

/-- em uma particula, sem par: nenhum vetor nao nulo e autovetor do boost; so o zero satisfaz a condicao — o abstrato inominado (apelido de `B0_no_eigen`, PAGO
pela bancada). -/
theorem na_particula_so_o_zero (f : H1) (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ B0 s f = c • f) : f = 0 :=
  B0_no_eigen f h

/-- ★ composto: a luz tem um vetor fixo, a inscricao do Um, e so ele. -/
theorem a_luz_tem_autovetor_o_um_inscrito :
    (∀ u : H1 ≃ₗᵢ[ℂ] H1, gamma u vacuum = vacuum) ∧
    (∀ ψ : F, (∀ s : ℝ, gamma (B0 s) ψ = ψ) → ψ ∈ (ℂ ∙ vacuum)) ∧
    exponential (0 : H1) = vacuum ∧ vacuum ≠ 0 :=
  ⟨a_luz_fixa_o_um, o_um_e_o_unico_fixo_da_luz, o_um_inscrito_e_a_exponencial_do_zero, o_um_nao_e_o_zero⟩

end TGLExt.OUmInscrito
