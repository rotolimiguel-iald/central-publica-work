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
import TGLExt.BoundedPerturbationCocycle

set_option autoImplicit false
set_option maxHeartbeats 900000
namespace ChatgptAudit.SpectatorCancellation
open TGLExt Filter Topology Set ChatgptAudit.UnitaryDuhamel ChatgptAudit.BoundedPerturbation
noncomputable section

local instance operatorRationalAlgebra (P : SiteProfile) :
    NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance operatorRationalTower (P : SiteProfile) :
    IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

theorem evolution_commuting_sum {P : SiteProfile} (H K : Operator P)
    (hHK : Commute H K) (t : ℝ) :
    evolution (H+K) t = evolution H t * evolution K t := by
  unfold evolution
  rw [smul_add, NormedSpace.exp_add_of_commute
    ((hHK.smul_left (((t : ℂ)*Complex.I))).smul_right (((t : ℂ)*Complex.I)))]

/-- A commuting spectator cancels from the relative evolution exactly. -/
theorem bounded_cocycle_spectator {P : SiteProfile} (H K V : Operator P)
    (hKH : Commute K H) (hKV : Commute K V) (t : ℝ) :
    boundedCocycle (H+K) V t = boundedCocycle H V t := by
  have hKVH : Commute (H+V) K := (hKH.add_right hKV).symm
  have he : evolution (H+K) (-t) = evolution K (-t) * evolution H (-t) := by
    rw [add_comm H K]
    exact evolution_commuting_sum K H hKH (-t)
  calc
    boundedCocycle (H+K) V t =
        (evolution (H+V) t * evolution K t) *
          (evolution K (-t) * evolution H (-t)) := by
      unfold boundedCocycle
      rw [show H+K+V = (H+V)+K by abel,
        evolution_commuting_sum (H+V) K hKVH t, he]
    _ = evolution (H+V) t * (evolution K t * evolution K (-t)) *
        evolution H (-t) := by simp only [mul_assoc]
    _ = boundedCocycle H V t := by
      rw [evolution_mul_neg, mul_one]
      rfl

theorem bounded_cocycle_background_extension {P : SiteProfile} (H G V : Operator P)
    (hGH : Commute (G-H) H) (hGV : Commute (G-H) V) (t : ℝ) :
    boundedCocycle G V t = boundedCocycle H V t := by
  have h := bounded_cocycle_spectator H (G-H) V hGH hGV t
  rw [show H + (G-H) = G by abel] at h
  exact h

/-- Only the spectator part of the background must commute with the old potential. -/
theorem varying_background_duhamel {P : SiteProfile} (H G V W : Operator P)
    (hG : IsSelfAdjoint G) (hV : IsSelfAdjoint V) (hW : IsSelfAdjoint W)
    (hGH : Commute (G-H) H) (hGV : Commute (G-H) V) (t : ℝ) :
    ‖boundedCocycle H V t - boundedCocycle G W t‖ ≤ ‖V-W‖ * |t| := by
  rw [← bounded_cocycle_background_extension H G V hGH hGV t]
  exact bounded_cocycle_perturbation_bound G V W hG hV hW t

theorem varying_background_bound_on_interval {P : SiteProfile} (H G V W : Operator P)
    (hG : IsSelfAdjoint G) (hV : IsSelfAdjoint V) (hW : IsSelfAdjoint W)
    (hGH : Commute (G-H) H) (hGV : Commute (G-H) V) (T t : ℝ) (ht : |t| ≤ T) :
    ‖boundedCocycle H V t - boundedCocycle G W t‖ ≤ ‖V-W‖ * T :=
  (varying_background_duhamel H G V W hG hV hW hGH hGV t).trans
    (mul_le_mul_of_nonneg_left ht (norm_nonneg _))

#print axioms operatorRationalAlgebra
#print axioms operatorRationalTower
#print axioms evolution_commuting_sum
#print axioms bounded_cocycle_spectator
#print axioms bounded_cocycle_background_extension
#print axioms varying_background_duhamel
#print axioms varying_background_bound_on_interval
end
end ChatgptAudit.SpectatorCancellation
