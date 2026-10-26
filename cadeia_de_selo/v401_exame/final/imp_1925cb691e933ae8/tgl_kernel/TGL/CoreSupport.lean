import Mathlib
import TGL.ModularRealization
import TGL.TransportData

set_option autoImplicit false

/-!
# O fechamento por separacao de tipos   [KERNEL]   (v32 -- derivacao do operador, auditada)

O ultimo erro era usar `P_F` para DOIS objetos: o SUPORTE que vive no core
(`q_F ∈ C_W`, desce, e' a unidade do canto) e o ESPELHO que vive na construcao
basica (`e_Nome ∈ ⟨R_F, e⟩`, NAO desce -- `jones_selector_not_descended` ja' o
provava). Ligados por transporte: `E₁(e_Nome) = β·q_F`.

O representante MINIMO da classe de kernel dos Three Locks e':

    H₃L^min = 1 − q_F      [q_F·H = 0 ; q_F e' a projecao MAXIMA que anula H]

Kernel-checked aqui:
  - a algebra do representante minimo (aniquilacao + maximalidade + auto-adjunto);
  - **`threeLocksFromSupport`**: DADO um suporte (projecao de traco 1 com faces de
    meio-traco), os Three Locks sao HABITAVEIS -- um CONSTRUTOR de termo. O gap do
    habitante pleno fica TIPADO como exatamente quatro entradas [KNOWN-COMPOSED]:
    testemunha-base W + dados modulares D + core C + suporte q_F (BW; Takesaki;
    II∞ hiperfinito difuso; indice de Jones ≥ 4 -- teoremas publicados, NAO
    formalizados na mathlib);
  - `realizationFromSupport`: o empacotamento ate' TGLModularRealization;
  - o PRINCIPIO DE GAUGE DO NOME [DEF/AX, do operador]: Nome-equivalencia de
    torres = mesmo indice e mesmo peso de Markov; os invariantes (peso, indice,
    defeito de transporte) sao funcoes de classe [KERNEL]. O fisico e' a CLASSE;
    o representante e' gauge.

Estatutos (fora do fechamento interno, cada um com nome):
  formalizacao Lean dos teoremas externos = certificacao formal [OPEN];
  escolha fisica localizada/covariante do representante = realizacao fisica
  [GAUGE, nao-matematico]; validacao experimental [INPUT futuro]; levantamento
  ao espaco-tempo curvo = extensao geometrica [OPEN].
  `full_TGL_witness_constructed` PERMANECE false ate' existir termo Lean pleno.
-/

namespace TGL.CoreSupport

open TGL.SpecificAQFT TGL.ModularRealization TGL.TransportData

section MinimalRepresentative

variable {A : Type} [Ring A] [StarRing A] [Algebra ℂ A]

/-- [KERNEL] O suporte aniquila o representante minimo: `q·(1−q) = 0`. -/
theorem support_annihilates (q : A) (hq2 : q * q = q) : q * (1 - q) = 0 := by
  rw [mul_sub, mul_one, hq2, sub_self]

/-- [KERNEL] O representante minimo e' auto-adjunto. -/
theorem hmin_selfadjoint (q : A) (hqs : star q = q) : star (1 - q : A) = 1 - q := by
  rw [star_sub, star_one, hqs]

/-- [KERNEL] MAXIMALIDADE: toda projecao que anula `1−q` esta' sob `q`
    (`r·(1−q)=0 ⟹ r·q = r`) -- `q` E' a projecao espectral do zero, na forma
    enunciavel. -/
theorem support_maximal (q r : A) (hr : r * (1 - q) = 0) : r * q = r := by
  rw [mul_sub, mul_one, sub_eq_zero] at hr
  exact hr.symm

end MinimalRepresentative

/-- [KERNEL — v32, o CONSTRUTOR do fechamento] Dado o core (DADOS) e um SUPORTE
    `q_F` (projecao nao-nula de traco 1, partida em duas faces ortogonais de
    traco igual), os Three Locks sao HABITAVEIS com o representante minimo
    `H₃L = 1 − q_F`. As hipoteses sao exatamente o que os teoremas EXTERNOS
    [KNOWN: BW + Takesaki + II∞ difuso] fornecem -- o gap esta' TIPADO. -/
noncomputable def threeLocksFromSupport {W : TGLSpecificAQFTWitness}
    {D : WedgeModularData W} (C : ContinuousCoreData W D)
    (q qp qm : C.Core)
    (hq2 : q * q = q) (hqs : star q = q) (hqne : q ≠ 0)
    (htr1 : C.canonicalTrace q = 1)
    (hp2 : qp * qp = qp) (hps : star qp = qp)
    (hm2 : qm * qm = qm) (hms : star qm = qm)
    (hsum : qp + qm = q) (horto : qp * qm = 0)
    (htradd : C.canonicalTrace q = C.canonicalTrace qp + C.canonicalTrace qm)
    (htreq : C.canonicalTrace qp = C.canonicalTrace qm) :
    ThreeLocksCoreData W D C where
  H3Lt := 1 - q
  H3Lt_selfAdjoint := hmin_selfadjoint q hqs
  PF := q
  PF_selfAdjoint := hqs
  PF_idempotent := hq2
  PF_locks := support_annihilates q hq2
  PF_maximal := fun r _ _ hr => support_maximal q r hr
  PF_nonzero := hqne
  PF_trace_pos := by rw [htr1]; exact zero_lt_one
  PF_trace_finite := by rw [htr1]; exact ENNReal.one_lt_top
  Pplus := qp
  Pminus := qm
  Pplus_selfAdjoint := hps
  Pplus_idempotent := hp2
  Pminus_selfAdjoint := hms
  Pminus_idempotent := hm2
  split := hsum
  orthogonal := horto
  trace_split_additive := htradd
  equal_face_trace := htreq

/-- [KERNEL] O empacotamento: com dimensao infinita + camadas + suporte, a
    REALIZACAO MODULAR e' habitavel. O habitante pleno reduz-se a QUATRO
    entradas [KNOWN-COMPOSED]: W, D, C, q_F. -/
noncomputable def realizationFromSupport {W : TGLSpecificAQFTWitness}
    (hinf : ¬ FiniteDimensional ℂ W.H)
    (D : WedgeModularData W) (C : ContinuousCoreData W D)
    (q qp qm : C.Core)
    (hq2 : q * q = q) (hqs : star q = q) (hqne : q ≠ 0)
    (htr1 : C.canonicalTrace q = 1)
    (hp2 : qp * qp = qp) (hps : star qp = qp)
    (hm2 : qm * qm = qm) (hms : star qm = qm)
    (hsum : qp + qm = q) (horto : qp * qm = 0)
    (htradd : C.canonicalTrace q = C.canonicalTrace qp + C.canonicalTrace qm)
    (htreq : C.canonicalTrace qp = C.canonicalTrace qm) :
    TGLModularRealization W where
  infiniteHilbert := hinf
  modular := D
  core := C
  threeLocks := threeLocksFromSupport C q qp qm hq2 hqs hqne htr1
    hp2 hps hm2 hms hsum horto htradd htreq

/-! ## O Principio de Gauge do Nome [DEF/AX do operador; invariantes KERNEL] -/

variable {N M Ext : Type}
  [Ring N] [StarRing N] [Algebra ℂ N]
  [Ring M] [StarRing M] [Algebra ℂ M]
  [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]

/-- [DEF/AX] Nome-equivalencia: mesmo peso de Markov e mesmo indice.
    O objeto fisico e' a CLASSE; o representante e' gauge. -/
def nameGaugeEquiv (T1 T2 : JonesTowerData N M Ext) : Prop :=
  T1.markovWeight = T2.markovWeight ∧ T1.indexVal = T2.indexVal

theorem nameGaugeEquiv_refl (T : JonesTowerData N M Ext) : nameGaugeEquiv T T :=
  ⟨rfl, rfl⟩

theorem nameGaugeEquiv_symm {T1 T2 : JonesTowerData N M Ext}
    (h : nameGaugeEquiv T1 T2) : nameGaugeEquiv T2 T1 :=
  ⟨h.1.symm, h.2.symm⟩

theorem nameGaugeEquiv_trans {T1 T2 T3 : JonesTowerData N M Ext}
    (h12 : nameGaugeEquiv T1 T2) (h23 : nameGaugeEquiv T2 T3) :
    nameGaugeEquiv T1 T3 :=
  ⟨h12.1.trans h23.1, h12.2.trans h23.2⟩

/-- [KERNEL] O DEFEITO DE TRANSPORTE e' invariante de gauge do Nome: torres
    Nome-equivalentes tem o mesmo defeito `β(1−β)·1`. O contraste e' fisico;
    o representante nao e'. -/
theorem transport_defect_gauge_invariant {T1 T2 : JonesTowerData N M Ext}
    (h : nameGaugeEquiv T1 T2) :
    transportDefect T1.upper T1.eJones = transportDefect T2.upper T2.eJones := by
  rw [transport_defect_of_jones, transport_defect_of_jones, h.1]

end TGL.CoreSupport
