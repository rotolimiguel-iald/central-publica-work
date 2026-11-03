-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_006 (05/09/2026), transposta em 05/09/2026
-- A ESPERANCA DO CENTRALIZADOR: habitante LOCAL (pinching espectral de cada
--   andar entra no centralizador GLOBAL de omega; into/fixes/ortho; unico) e
--   habitante TRACIAL do contrato original (w=1/2: M_omega = M, E = id);
--   invariancia de sitios sob sigma_t para TODO t (caudas nunca comprimem
--   estritamente); ponte: todo habitante global RESTRINGE-SE ao pinching.
-- Auditoria da gerencia (sessao d554e796): hashes 14/14 + manifesto 408/408;
--   recompilacao independente 5/5 exit 0; 34/34 no trio
--   [propext, Classical.choice, Quot.sound]; zero sorry/warning.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports da
--   bancada; nada mais. Namespace ChatgptAudit = procedencia.
-- [OPEN] declarados pela bancada: habitante global NAO tracial (parede exata:
--   operador medio do periodo + comutacao da media com E_N); nao-ciclicidade
--   da cauda em Lean; translacao de energia positiva nao trivial.
-- NAO move gate; nao e fisica. NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.CentralizerLocal
import TGLExt.ChainPrefix

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem expectationMatrix_pi (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    expectationMatrix P N (towerPi P a) = a :=
  towerPi_injective P N (expectation_fixes N a)

theorem expectationMatrix_star (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) :
    expectationMatrix P N (star x) = (expectationMatrix P N x)ᴴ := by
  apply towerPi_injective P N
  change towerPi P (expectationMatrix P N (star x)) = towerPi P ((expectationMatrix P N x)ᴴ)
  rw [towerPi_star,← ContinuousLinearMap.star_eq_adjoint]
  exact expectation_star N x hx

theorem pinching_global_ortho (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : TowerHilbert P →L[ℂ] TowerHilbert P) (hb : b ∈ omegaCentralizer P) :
    omegaState P (star b * (towerPi P a - towerPi P (specExpect (towerW P N) a))) = 0 := by
  have hsub : towerPi P a - towerPi P (specExpect (towerW P N) a) =
      towerPi P (a-specExpect (towerW P N) a) := (map_sub (towerPiLinear P N) _ _).symm
  rw [hsub,state_local_right N _ (star b) (star_mem hb.1),expectationMatrix_star N b hb.1]
  exact pinching_state_ortho N a (expectationMatrix P N b)
    (expectation_of_centralizer_is_centralizer N b hb)

structure LocalCentralizerInput (P : SiteProfile) (N : ℕ) where
  E : Matrix (chainIdx N) (chainIdx N) ℂ → (TowerHilbert P →L[ℂ] TowerHilbert P)
  into : ∀ a, E a ∈ omegaCentralizer P
  fixes : ∀ a, towerPi P a ∈ omegaCentralizer P → E a = towerPi P a
  ortho : ∀ a, ∀ b ∈ omegaCentralizer P, omegaState P (star b*(towerPi P a-E a)) = 0

def localCentralizerInput (P : SiteProfile) (N : ℕ) : LocalCentralizerInput P N where
  E := fun a => towerPi P (specExpect (towerW P N) a)
  into := pinching_into_global_centralizer N
  fixes := fun a ha => by rw [pinching_fixes_global_local N a ha]
  ortho := pinching_global_ortho N

theorem local_input_is_spectral (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (localCentralizerInput P N).E a = towerPi P (specExpect (towerW P N) a) := rfl

theorem local_input_unique (N : ℕ) (F : LocalCentralizerInput P N)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : F.E a = (localCentralizerInput P N).E a := by
  let E := localCentralizerInput P N
  have hF := F.into a
  have hE := E.into a
  have hd : F.E a-E.E a ∈ omegaCentralizer P := by
    refine ⟨sub_mem hF.1 hE.1,?_⟩
    intro b hb
    rw [sub_mul,mul_sub,omegaState_sub,omegaState_sub,hF.2 b hb,hE.2 b hb]
  apply sub_eq_zero.mp
  apply omega_definite hd.1
  have hf := F.ortho a _ hd
  have he := E.ortho a _ hd
  have hid : F.E a-E.E a = (towerPi P a-E.E a)-(towerPi P a-F.E a) := by abel
  have hk := congrArg (fun z => omegaState P (star (F.E a-E.E a)*z)) hid
  have hr : omegaState P (star (F.E a-E.E a)*
      ((towerPi P a-E.E a)-(towerPi P a-F.E a))) = 0 := by
    rw [mul_sub,omegaState_sub,he,hf,sub_self]
  exact hk.trans hr

#print axioms expectationMatrix_pi
#print axioms expectationMatrix_star
#print axioms pinching_global_ortho
#print axioms localCentralizerInput
#print axioms local_input_is_spectral
#print axioms local_input_unique
end
end ChatgptAudit
