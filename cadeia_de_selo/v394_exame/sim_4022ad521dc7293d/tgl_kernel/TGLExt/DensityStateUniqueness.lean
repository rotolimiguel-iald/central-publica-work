-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_033 (06/09/2026), transposta em 06/09/2026
-- Lote 033: DENSIDADE CENTRALIZANTE, logaritmo e cociclo canonico — a algebra do centralizador de omega
--   definida sem o fluxo (fechada, soma, produto, exponencial); L, R, H e u no centralizador; densidade
--   positiva, auto-adjunta, invertivel, no fator e NORMALIZADA; logaritmo genuino e unico (CFC.log_exp);
--   potencia imaginaria limitada = cociclo, unitaria; estado da densidade e UNICIDADE da densidade no fator
--   (H, K no fator; sem supor positividade das concorrentes); controle da leitura angular (par no tempo;
--   estado de referencia invariante pelo cociclo). Estatuto [REAL / KNOWN / DERIVED / INPUT / OPEN]:
--   a identificacao de Connes e especializacao explicita de Hiai 9.4(2) [KNOWN/DERIVED], nao teorema novo
--   do kernel; Pedersen-Takesaki geral, area, retorno estabilizante e gravidade geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10; manifesto 265/265; auditor exit 0;
--   recompilacao INDEPENDENTE 3/3 apos a REGRA 3, axiomas no trio; guarda de colisao; enunciados lidos.
-- TRANSPOSICAO: cabecalho + prefixo TGLExt. + REGRA 3 (instancias LOCAIS anonimas nomeadas
--   inst_<Modulo>_<k>): Lean gerava o MESMO nome automatico (Density033.instNormedAlgebraRat...) em
--   CentralizerDensity e LikelihoodDensityLog e o ROOT nao os importa juntos; so o NOME da declaracao muda,
--   nenhuma prova. Os oleans da bancada traziam sufixos de arquivo que um compilador limpo nao gera
--   (ambiente da bancada com oleans reaproveitados) — ORDEM_008 pede instancias NOMEADAS daqui em diante.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.LikelihoodDensityLog
import TGLExt.CentralizerDensity

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace ChatgptAudit.Density033
open TGLExt ChatgptAudit ChatgptAudit.Cocycle030 ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

/-- A faithful vector state distinguishes all left densities in the factor. -/
theorem factor_density_state_unique {P : SiteProfile}
    {H K : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hH : H ∈ theFactorObject P) (hK : K ∈ theFactorObject P)
    (heq : ∀ A ∈ theFactorObject P, omegaState P (H*A)=omegaState P (K*A)) :
    H=K := by
  have hD : H-K ∈ theFactorObject P := (theFactorObject P).sub_mem hH hK
  have hDstar : star (H-K) ∈ theFactorObject P :=
    star_mem hD
  have hz : omegaState P ((H-K)*star (H-K))=0 := by
    rw [sub_mul,omegaState_sub,heq _ hDstar,sub_self]
  have hzstar : star (H-K)=0 := omega_definite hDstar (by
    simpa only [star_star] using hz)
  have hzero : H-K=0 := by
    simpa only [star_star,star_zero] using congrArg star hzstar
  exact sub_eq_zero.mp hzero

/-- The prepared state is represented by the left likelihood density. -/
theorem likelihood_density_state_left (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A ∈ theFactorObject thirdThermalReference) :
    amplitudeState b t A=omegaState thirdThermalReference (likelihoodDensity b t*A) := by
  have hR := likelihood_filter_mem_centralizer b t
  rw [likelihood_filter_state b t A]
  change omegaState thirdThermalReference
      (likelihoodFilter b t*A*likelihoodFilter b t)=
    omegaState thirdThermalReference (NormedSpace.exp (likelihoodGenerator b t)*A)
  calc
    omegaState thirdThermalReference (likelihoodFilter b t*A*likelihoodFilter b t)=
        omegaState thirdThermalReference (likelihoodFilter b t*(likelihoodFilter b t*A)) :=
      (hR.2 (likelihoodFilter b t*A)
        ((theFactorObject thirdThermalReference).mul_mem hR.1 hA)).symm
    _ = omegaState thirdThermalReference (NormedSpace.exp (likelihoodGenerator b t)*A) := by
      rw [←mul_assoc,likelihood_filter_square]

/-- Centralization also puts the likelihood density on the right. -/
theorem likelihood_density_state_right (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A ∈ theFactorObject thirdThermalReference) :
    amplitudeState b t A=omegaState thirdThermalReference (A*likelihoodDensity b t) := by
  have hR := likelihood_filter_mem_centralizer b t
  rw [likelihood_filter_state b t A]
  change omegaState thirdThermalReference
      (likelihoodFilter b t*A*likelihoodFilter b t)=
    omegaState thirdThermalReference (A*NormedSpace.exp (likelihoodGenerator b t))
  calc
    omegaState thirdThermalReference (likelihoodFilter b t*A*likelihoodFilter b t)=
        omegaState thirdThermalReference (likelihoodFilter b t*(A*likelihoodFilter b t)) := by
      rw [mul_assoc]
    _ = omegaState thirdThermalReference ((A*likelihoodFilter b t)*likelihoodFilter b t) :=
      hR.2 (A*likelihoodFilter b t)
        ((theFactorObject thirdThermalReference).mul_mem hA hR.1)
    _ = omegaState thirdThermalReference (A*NormedSpace.exp (likelihoodGenerator b t)) := by
      rw [mul_assoc,likelihood_filter_square]

/-- No other factor element represents the prepared state by left multiplication. -/
theorem likelihood_density_state_unique (b : SummableAmplitude) (t : ℝ)
    (H : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hH : H ∈ theFactorObject thirdThermalReference)
    (hstate : ∀ A ∈ theFactorObject thirdThermalReference,
      amplitudeState b t A=omegaState thirdThermalReference (H*A)) :
    H=likelihoodDensity b t := by
  apply factor_density_state_unique hH (likelihood_density_mem_factor b t)
  intro A hA
  exact (hstate A hA).symm.trans (likelihood_density_state_left b t A hA)

/-- A centralizing likelihood cocycle preserves the reference state on the factor. -/
theorem reference_state_cocycle_invariant (b : SummableAmplitude) (t s : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A ∈ theFactorObject thirdThermalReference) :
    omegaState thirdThermalReference
      (star (likelihoodCocycle b t s)*A*likelihoodCocycle b t s)=
        omegaState thirdThermalReference A := by
  have hU := likelihood_cocycle_mem_centralizer b t s
  have hUstar : star (likelihoodCocycle b t s)∈theFactorObject thirdThermalReference := by
    rw [likelihood_cocycle_star]
    exact likelihood_cocycle_mem_factor b t (-s)
  calc
    omegaState thirdThermalReference
        (star (likelihoodCocycle b t s)*A*likelihoodCocycle b t s)=
      omegaState thirdThermalReference
        (likelihoodCocycle b t s*(star (likelihoodCocycle b t s)*A)) :=
      (hU.2 (star (likelihoodCocycle b t s)*A)
        ((theFactorObject thirdThermalReference).mul_mem
          hUstar hA)).symm
    _ = omegaState thirdThermalReference A := by
      rw [←mul_assoc,likelihood_cocycle_star,likelihood_cocycle_inverse,one_mul]

#print axioms reference_state_cocycle_invariant
#print axioms factor_density_state_unique
#print axioms likelihood_density_state_left
#print axioms likelihood_density_state_right
#print axioms likelihood_density_state_unique

end
end ChatgptAudit.Density033
