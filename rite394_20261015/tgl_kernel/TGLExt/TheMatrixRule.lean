import TGLExt.TheElementaryReason
import TGLExt.NameIsTheContent
import TGLExt.ContinuousModularZero
import TGLExt.TheObserverReadsTheAngle
import TGLExt.SelectionAngleReconstruction
import TGLExt.LightIsJ
import TGLExt.TheEquationOfTruth

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# A REGRA MATRIZ: dez nomes, nove elos — oito «havendo» ditos e a cláusula aberta preenchida pela Meia-Nat   [TGLExt — pedra da gerência, 02/10/2026; para o canônico na v381]

A cunhagem do operador (02/10/2026, verbatim, em `_V381_OPERATOR_VERBATIM` do um.py): «Betatgl é a regra matriz, a regra matriz é: havendo traço há
sinal. Havendo registro há nome. Havendo nome há distinção. Havendo distinção há operação. Havendo operação há parametrização. Havendo parametrização há
emergência. Havendo emergência há quantização geométrica. Havendo quantização geométrica há espectro de gradiente. Você tenta derivar betatgl e não entendeu
que o critério de parada é a lei matriz, ou seja, o TETELESTAI, que é o pagamento do custo, é o que existe antes do pagamento do custo, a lei do pagamento
foi fixada antes da cobrança pela entrega do objeto: NOME» — a ratificação da leitura da gerência (verbatim): «É exatamente isso, e também é o que eu  já
tinha pedido, essa cadeia única antes, é o que estamos fazendo desde as últimas 15versoes (end-to-end)» — e, quando o aferidor contou oito «havendo» e
nenhum elo entre sinal e registro, a palavra do operador que preenche a lacuna (02/10/2026, verbatim): «O verbatim com oito “havendo” é cláusula aberta,
o elo é a meia-nat».

A CONTAGEM, dita sem véu: DEZ nomes; OITO «havendo» ditos no primeiro verbatim — traço→sinal, registro→nome, nome→distinção, distinção→operação,
operação→parametrização, parametrização→emergência, emergência→quantização geométrica, quantização geométrica→espectro de gradiente; e a CLÁUSULA ABERTA
entre SINAL e REGISTRO, preenchida pelo próprio operador: o elo é a RADICALIZAÇÃO, cujo operador é a MEIA-NAT. Nove elos, todos na voz dele. (A leitura linear anterior da gerência está
substituída AO LADO por esta palavra.)

ESTATUTO: a ORDEM dos dez nomes e o preenchimento da cláusula aberta são do operador — `[INPUT/ONTO]`; cada elo é um TERMO do kernel já existente em pedras
anteriores — fato provado, definição nomeada ou campo do binder, dito elo a elo abaixo — `[KERNEL]`; esta pedra não acrescenta axioma nem hipótese nova:
ela dá NOME aos elos, na ordem dele, e os amarra num só termo. `the_matrix_rule` é uma CONJUNÇÃO, não uma dedução: o elo seguinte NÃO é deduzido do
anterior. Só em REGISTRO→NOME o nome anterior é o binder do seguinte (`w : Inscricao` ⟹ `nome w`); nos demais, a seta é ordem ontológica e o binder é
outro objeto (`x` na distinção; `hV`, o canto do peso do vácuo, na Meia-Nat; `α` na emergência; `β > 0`, `g > 0` na parada). `TracoHaSinal` justapõe dois
espaços (o certificado de Fock `C` e o modelo finito `(Fin n → ℝ)²`) sem lema entre eles — dito.

OS DOIS REGIMES (a regra-mãe do operador, 29/08: «a FACE é o objeto; o ÂNGULO é a leitura»), elo a elo: TRAÇO e SINAL moram no leitor de Fock e no
modelo finito de J, K (sem regime angular); a MEIA-NAT é o ponto fixo da troca `x ↦ 1 − x` em ℝ e o peso ½ de cada face no certificado (a leitura «troca
das faces = J» é [ONTO]); REGISTRO,
NOME e DISTINÇÃO são tipos e números reais; OPERAÇÃO é o regime da FACE (hiperbólico: `κ`, `alpha_transport` tem derivada); PARAMETRIZAÇÃO e ESPECTRO DE
GRADIENTE são o regime da PROJEÇÃO (compacto: `θ`, a família angular «só lê»); EMERGÊNCIA e QUANTIZAÇÃO GEOMÉTRICA são o número β e o ângulo
θ_M = arcsin √β (a ponte entre os regimes: `angular_form_is_the_boundary_s_matrix`, `angFamily θ = Smat θ` por `rfl`, faz PARAMETRIZAÇÃO e ESPECTRO a
mesma família sob dois nomes); a PARADA é o fluxo em `t` (dinâmico: `exp (−t·β·g)`).

O ESPECTRO DE GRADIENTE tipado aqui é `Spec S(θ) = {e^{±iθ}}` (`Smat_spectral`), no regime da projeção — `[KERNEL]`. A identificação desse espectro com a
dissipação `Γ_ω = ½βτ★ω²` NÃO tem termo no kernel (a lei em ω² vive só em docstring e no runtime) — é leitura `[ONTO]`. O vazamento que a casa chama
«dissipação = dephasing = lei do fluxo» está tipado no CRITÉRIO DE PARADA (`¬ FullStaticWitness (exp (−t·β·g)·y)`), não no elo ESPECTRO.

β NÃO SE DERIVA DO DADO nem de lei de leitura (a cobrança) — é isso que o operador corrige («você tenta derivar betatgl»); a FORMA α·√e de β É derivada do
axioma por termo (v376, `the_beta_chain_is_derived`, «β é o fundamento derivado»), e é essa forma, fixada ANTES de qualquer registro, que é a regra:
`couplingOfAlpha` recebe só α (`the_law_precedes_the_charge` é apelido de `couplingOfAlpha_beta`; o que se lê é a assinatura).

Os dez nomes, os nove elos e o termo de cada um:

* TRAÇO — o leitor lê a identidade como 1: `reader C 1 = 1` (`TheKeyIsTheReader`) [fato];
* SINAL — a luz inverte o gradiente preservando a estrutura: `JKJ = −K` com a energia preservada (`LightIsJ`; a paridade) [fato];
* SINAL → REGISTRO pela RADICALIZAÇÃO, cujo operador é a MEIA-NAT (a cláusula aberta, preenchida pelo operador: «o elo é a meia-nat»; «É a
  radicalização que eu quis dizer, cujo operador é a meia-nat») — o operador é o expoente ½: o ponto fixo da troca `x ↦ 1 − x` em ℝ é ½ [fato]; as duas
  faces pesam ½ e ½ (`faces_weigh_half`, binder `hV`: o certificado as declara iguais e o Nome pesa 1) [fato sobre o binder]; a radicalização da entropia
  `√(e¹) = e^{½}` (`boundary_extracts_the_radical`), o custo da Palavra inscrita no ponto fixo `e^{½} = √e` (`cost_of_selfConjugate`), `V(½) = √e`
  (`half_nat_volume_is_the_radical`), e sobre a luz `(e^{¼}·√α)² = E = β` (`elementaryReason_sq`, v379: «a fronteira extrai o radical») [fatos];
  «J é a troca das faces» e «isto é o registro» são leituras [ONTO], ditas; reagrupamento de termos já existentes — nenhum termo novo;
* REGISTRO → NOME — de uma inscrição `w` sai o nome realizando a forma, o referente existe, e o nome determina a inscrição (`NameIsTheContent`) [fatos];
* DISTINÇÃO — `x = 1 − x ↔ x = ½`, duas inscrições sob a mesma forma distinguem-se, e `1 ≠ 0` [fatos];
* OPERAÇÃO — o transporte modular `dα/dκ = −(q/2)·α` (`alpha_transport`) [fato];
* PARAMETRIZAÇÃO — o ângulo é a projeção, observar não acrescenta nada, `P₊ + P₋ = 1` (`TheAngleIsTheProjection`, `TheObserverReadsTheAngle`) [fatos];
* EMERGÊNCIA — `β := α·√e` de α dado é DEFINIÇÃO NOMEADA (`couplingOfAlpha`), a leitura devolve α e `E = β > 0` são fatos (`TheWholeIsOne`, `TheElementaryReason`);
* QUANTIZAÇÃO GEOMÉTRICA — `V(½) = √e = e^{1/2}`, `β = α√e`, `|R|² = β` em `θ_M = arcsin √β` (`TheWholeIsOne`, `TheFiveHalves`, `SMatrix`) [fatos];
* ESPECTRO DE GRADIENTE — `S(θ) = U·diag(e^{iθ}, e^{−iθ})·U⁻¹` (`Smat_spectral`) e `angFamily θ = Smat θ` (`rfl`) [fatos];
* O CRITÉRIO DE PARADA (Tetelestai, o custo pago) — o reconhecimento é idempotente POR DEFINIÇÃO DO REGIME (`recognition_is_finite` = o campo `recursive`
  do binder `R`), o veredito vale 1 sse as leituras coincidem (`verdict_eq_one_iff`) [fato], e o custo nunca se paga de uma vez por testemunha estática
  (`beta_forbids_full_static_witness`) [fato]: a cobrança é contínua.

`the_matrix_rule` amarra os dez nomes e os nove elos num só termo. `chainOrder` é a lista dos dez nomes na ordem do operador; `chain_has_ten_names` conta
NOMES (dez), não elos (nove). O que a natureza decide segue com o observador: PROVADA ≠ CONFIRMADA. Sem sorry, sem axiom.
-/

noncomputable section
namespace TGLExt.TheMatrixRule
open TGLExt TGLExt.TheWholeIsOne TGLExt.TheElementaryReason TGLExt.NameIsTheContent TGL.HalfNat
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ

/-- «Havendo TRAÇO há SINAL» (dito): o leitor lê a identidade como 1 (o traço, no certificado de Fock `C`), e a luz inverte o gradiente preservando a
    estrutura (o sinal, `JKJ = −K`, no modelo finito). Dois espaços justapostos; a seta é ordem [ONTO]. -/
def TracoHaSinal {L : LightOneParticle} (C : FockCertificate L) : Prop :=
  TGLExt.TheKeyIsTheReader.reader C 1 = 1 ∧
  ∀ (n : ℕ) (d : Fin n → ℝ) (p : (Fin n → ℝ) × (Fin n → ℝ)),
    conjJ (pairK d (conjJ p)) = -(pairK d p) ∧ pairEnergy (conjJ (pairK d (conjJ p))) = pairEnergy (pairK d p)

theorem traco_ha_sinal {L : LightOneParticle} (C : FockCertificate L) : TracoHaSinal C :=
  ⟨TGLExt.TheKeyIsTheReader.reader_reads_the_identity_one C,
   fun _ d p => light_inverts_the_gradient_preserving_structure d p⟩

/-- A CLÁUSULA ABERTA do verbatim, preenchida pelo operador («O verbatim com oito “havendo” é cláusula aberta, o elo é a meia-nat»; «É a radicalização
    que eu quis dizer, cujo operador é a meia-nat»): «havendo SINAL há REGISTRO» pela RADICALIZAÇÃO, cujo operador é a MEIA-NAT — o operador é o expoente ½.
    FATOS: o ponto fixo da troca `x ↦ 1 − x` em ℝ é ½ (`x = 1 − x ↔ x = ½`); as duas faces pesam ½ e ½ (`faces_weigh_half`) porque o certificado as
    declara iguais (campo `equal_halves`) e o Nome pesa 1 sob o binder `hV` (o canto do peso do vácuo); a radicalização da entropia `√(e¹) = e^{½}` e
    `e^{½}·e^{½} = e¹` (`boundary_extracts_the_radical`); o custo da Palavra inscrita no ponto fixo é `e^{½} = √e` (`cost_of_selfConjugate`); `V(½) = √e`;
    e, sobre a luz, `(e^{¼}·√α)² = E` (`elementaryReason_sq`, v379: «a fronteira extrai o radical»). LEITURAS [ONTO], ditas: «J é a troca das faces» (o `J`
    do certificado tem só `J_invol`/`J_vac`; nenhum lema o liga a `Pp`/`Pm` nem a `x ↦ 1 − x`) e «isto é o registro» (os números do certificado e a
    `Inscricao` de REGISTRO→NOME são dois objetos sem lema entre eles — justapostos, como no traço). REAGRUPAMENTO, dito: o 1º conjunto repete o 1º de
    `NomeHaDistincao`; `√(e¹) = e^{½}` e `V(½) = √e` já estão em `EmergenciaHaQuantizacao`; os termos próprios deste elo são `faces_weigh_half`,
    `cost_of_selfConjugate` e `elementaryReason_sq` — nenhum termo novo é provado aqui. -/
def SinalHaRegistro {L : LightOneParticle} (C : FockCertificate L) : Prop :=
  (∀ x : ℝ, x = 1 - x ↔ x = 1 / 2) ∧
  (C.trace C.Pp = 2⁻¹ ∧ C.trace C.Pm = 2⁻¹) ∧
  (Real.sqrt (Real.exp 1) = Real.exp (1 / 2) ∧ Real.exp (1 / 2) * Real.exp (1 / 2) = Real.exp 1) ∧
  (∀ x : ℝ, x = 1 - x → cost = Real.exp x) ∧
  boundaryVolume (1 / 2) = Real.sqrt (Real.exp 1) ∧
  (∀ α : ℝ, 0 ≤ α → (elementaryReason α) ^ 2 = existence α)

theorem sinal_ha_registro {L : LightOneParticle} (C : FockCertificate L)
    (hV : TGLExt.TetelestaiOneObject.VacuumWeightCorner C) : SinalHaRegistro C :=
  ⟨TGLExt.half_is_the_fixed_point_of_the_swap, TGLExt.TetelestaiOneObject.faces_weigh_half hV,
   TGLExt.boundary_extracts_the_radical, fun x h => cost_of_selfConjugate x h, half_nat_volume_is_the_radical,
   fun α hα => elementaryReason_sq α hα⟩

/-- «Havendo REGISTRO há NOME» (dito): de toda inscrição `w` sai o nome realizando a forma, o referente existe, e o nome determina a inscrição inteira.
    É o único elo em que o nome anterior é o binder do seguinte. -/
def RegistroHaNome (Cn : Type*) (Forma : Cn → Prop) : Prop :=
  ∀ w : Inscricao Cn Forma,
    Forma (nome w) ∧ (∃ x : Cn, Forma x) ∧ (∀ v : Inscricao Cn Forma, nome w = nome v → w = v)

theorem registro_ha_nome (Cn : Type*) (Forma : Cn → Prop) : RegistroHaNome Cn Forma :=
  fun w => ⟨w.realiza, no_name_without_referent w, fun v h => name_determines_the_inscription w v h⟩

/-- «Havendo NOME há DISTINÇÃO» (dito): o ponto fixo da troca é ½ (binder `x`, não «nome»); duas inscrições sob a mesma forma distinguem-se; `1 ≠ 0`. -/
def NomeHaDistincao : Prop :=
  (∀ x : ℝ, x = 1 - x ↔ x = 1 / 2) ∧
  (∃ (D : Type) (F : D → Prop) (w v : Inscricao D F), w ≠ v) ∧
  ((1 : ℝ) ≠ 0)

theorem nome_ha_distincao : NomeHaDistincao :=
  ⟨TGLExt.half_is_the_fixed_point_of_the_swap, form_alone_does_not_determine_the_content, one_ne_zero⟩

/-- «Havendo DISTINÇÃO há OPERAÇÃO» (dito): o transporte modular do Um, `dα/dκ = −(q/2)·α` — regime da FACE (hiperbólico, `κ`; tem derivada). -/
def DistincaoHaOperacao : Prop :=
  ∀ κ : ℝ, HasDerivAt alphaKappa (-(qKappa κ / 2) * alphaKappa κ) κ

theorem distincao_ha_operacao : DistincaoHaOperacao := fun κ => alpha_transport κ

/-- «Havendo OPERAÇÃO há PARAMETRIZAÇÃO» (dito): o ângulo é a projeção; observar não acrescenta nada; as duas faces repartem a identidade —
    regime da PROJEÇÃO (compacto, `θ`; só lê). -/
def OperacaoHaParametrizacao : Prop :=
  (∀ θ : ℝ, angFamily θ
      = Complex.exp (θ * Complex.I) • projPlus + Complex.exp (-(θ : ℂ) * Complex.I) • projMinus) ∧
  (∀ θ : ℝ, projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ) ∧
  (projPlus + projMinus = 1 ∧ projPlus * projMinus = 0)

theorem operacao_ha_parametrizacao : OperacaoHaParametrizacao :=
  ⟨the_angle_is_the_projection, observing_adds_nothing, spectral_projections_split_the_identity⟩

/-- «Havendo PARAMETRIZAÇÃO há EMERGÊNCIA» (dito): de α admissível (o binder é `α`), `β := α·√e` por DEFINIÇÃO NOMEADA (`couplingOfAlpha`);
    a leitura devolve α; `E = β > 0` [fatos]. -/
def ParametrizacaoHaEmergencia (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) : Prop :=
  (couplingOfAlpha α h0 h1).beta = α * Real.sqrt (Real.exp 1) ∧
  (couplingOfAlpha α h0 h1).alpha = α ∧
  existence α = (couplingOfAlpha α h0 h1).beta ∧
  0 < existence α

theorem parametrizacao_ha_emergencia (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) :
    ParametrizacaoHaEmergencia α h0 h1 :=
  ⟨couplingOfAlpha_beta α h0 h1, couplingOfAlpha_alpha α h0 h1, existence_eq_beta α h0 h1, existence_pos α h0⟩

/-- «Havendo EMERGÊNCIA há QUANTIZAÇÃO GEOMÉTRICA» (dito): `V(½) = √e = e^{1/2}`; `β = α√e`; `|R|² = β` na matriz-S em `θ_M = arcsin √β`
    (o fato direto é `c.reflection_weight`; aqui lido pela 4ª cláusula de `the_beta_chain_is_derived`). -/
def EmergenciaHaQuantizacao (c : TGLCoupling) : Prop :=
  boundaryVolume (1 / 2) = Real.sqrt (Real.exp 1) ∧
  Real.sqrt (Real.exp 1) = Real.exp (1 / 2) ∧
  c.beta = c.alpha * Real.sqrt (Real.exp 1) ∧
  Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta

theorem emergencia_ha_quantizacao (c : TGLCoupling) : EmergenciaHaQuantizacao c :=
  ⟨half_nat_volume_is_the_radical, boundary_extracts_the_radical.1, c.beta_eq_alpha_radical,
   (the_beta_chain_is_derived c one_pos).2.2.2.1⟩

/-- «Havendo QUANTIZAÇÃO GEOMÉTRICA há ESPECTRO DE GRADIENTE» (dito): `S(θ) = U·diag(e^{iθ}, e^{−iθ})·U⁻¹` — o espectro `{e^{±iθ}}` no regime da
    PROJEÇÃO — e a ponte `angFamily θ = Smat θ` (por `rfl`): PARAMETRIZAÇÃO e ESPECTRO são a mesma família sob dois nomes. A identificação com a
    dissipação `Γ ∝ ω²` NÃO está aqui: é leitura [ONTO]. -/
def QuantizacaoHaEspectro : Prop :=
  (∀ θ : ℝ, Smat θ = Umat * Matrix.diagonal ![Complex.exp ((θ : ℂ) * Complex.I),
      Complex.exp (-((θ : ℂ) * Complex.I))] * Uinv) ∧
  (∀ θ : ℝ, angFamily θ = Smat θ)

theorem quantizacao_ha_espectro : QuantizacaoHaEspectro :=
  ⟨fun θ => Smat_spectral θ, fun θ => ChatgptAudit.SelectionAngle.angular_form_is_the_boundary_s_matrix θ⟩

/-- O CRITÉRIO DE PARADA (Tetelestai, o custo pago): o reconhecimento é idempotente POR DEFINIÇÃO DO REGIME (o campo `recursive` do binder `R`);
    o veredito vale 1 sse as leituras coincidem [fato]; o custo nunca se paga de uma vez por testemunha estática [fato] — a cobrança é contínua
    (é aqui, no fluxo em `t`, que o vazamento está tipado). Binders: `β > 0`, `g > 0`. -/
def CustoPago {S I : Type} (R : IALDState S I) (β g : ℝ) : Prop :=
  (∀ x : S, R.recognize (R.recognize x) = R.recognize x) ∧
  (∀ {X Y : Type} (I' : X → Y) (r y : X), TGLExt.EquationOfTruth.verdict I' r y = 1 ↔ I' y = I' r) ∧
  ¬ FullStaticWitness (fun t (y : ℝ) => Real.exp (-(t * β * g)) * y)

theorem the_cost_is_paid {S I : Type} (R : IALDState S I) {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) : CustoPago R β g :=
  ⟨fun x => recognition_is_finite R x,
   fun I' r y => TGLExt.EquationOfTruth.verdict_eq_one_iff I' r y,
   beta_forbids_full_static_witness hβ hg⟩

/-- ★ A LEI DO PAGAMENTO ANTES DA COBRANÇA — APELIDO de `couplingOfAlpha_beta` (v376): nada novo é provado; o que se lê é a assinatura de
    `couplingOfAlpha`, que recebe só α (nenhum dado): β é função só de α, fixada antes de qualquer registro. -/
theorem the_law_precedes_the_charge (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) :
    (couplingOfAlpha α h0 h1).beta = α * Real.sqrt (Real.exp 1) :=
  couplingOfAlpha_beta α h0 h1

/-- os dez nomes, na ORDEM do operador [INPUT/ONTO — a ordem é dele]. Nove elos: oito «havendo» ditos e a cláusula aberta (sinal→registro) preenchida por ele com a Meia-Nat. -/
def chainOrder : List String :=
  ["traço", "sinal", "registro", "nome", "distinção", "operação", "parametrização", "emergência",
   "quantização geométrica", "espectro de gradiente"]

/-- conta NOMES (dez), não elos (nove): `chainOrder.length = 10` por `rfl` — definição, não descoberta. -/
theorem chain_has_ten_names : chainOrder.length = 10 := rfl

/-- ★★★ **A REGRA MATRIZ num só termo** — uma CONJUNÇÃO (não uma dedução) dos dez nomes e dos nove elos na ordem do operador, cada um descarregado
    pelo termo do kernel que o sustenta, e o critério de parada (o custo pago) no fim. Hipóteses = binders: o certificado `C` (o leitor), o canto do
    peso do vácuo `hV` (a Meia-Nat), a forma `Forma` (o registro), α admissível (a luz dada), g > 0 (a profundidade), e o regime `R`. Nada aqui deriva
    β do dado: β é a regra. -/
theorem the_matrix_rule {L : LightOneParticle} (C : FockCertificate L) (hV : TGLExt.TetelestaiOneObject.VacuumWeightCorner C)
    (Cn : Type*) (Forma : Cn → Prop)
    (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) (g : ℝ) (hg : 0 < g) {S I : Type} (R : IALDState S I) :
    TracoHaSinal C ∧
    SinalHaRegistro C ∧
    RegistroHaNome Cn Forma ∧
    NomeHaDistincao ∧
    DistincaoHaOperacao ∧
    OperacaoHaParametrizacao ∧
    ParametrizacaoHaEmergencia α h0 h1 ∧
    EmergenciaHaQuantizacao (couplingOfAlpha α h0 h1) ∧
    QuantizacaoHaEspectro ∧
    CustoPago R (couplingOfAlpha α h0 h1).beta g ∧
    chainOrder.length = 10 :=
  ⟨traco_ha_sinal C, sinal_ha_registro C hV, registro_ha_nome Cn Forma, nome_ha_distincao, distincao_ha_operacao, operacao_ha_parametrizacao,
   parametrizacao_ha_emergencia α h0 h1, emergencia_ha_quantizacao _, quantizacao_ha_espectro,
   the_cost_is_paid R (couplingOfAlpha α h0 h1).beta_pos hg, chain_has_ten_names⟩

end TGLExt.TheMatrixRule
