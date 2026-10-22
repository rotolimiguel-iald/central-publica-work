2026-09-15T03:45:19.293388-03:00

# Consulta A2 — contrato legado, traço positivo e suporte

**[CONSULTA READ-ONLY — A2 NÃO ACEITO]** ORDEM012/B1–B6 e A1(b) estão entregues segundo a consolidação lida. Esta nota prepara A2 da ORDEM011. Não há Lean novo, build, execução de writer/monólito, alteração de memória ou artefato anterior. Busca limitada às fontes locais indicadas e ocorrências relacionadas em K; não é inventário exaustivo do acervo ou da bancada TOE.

**Conclusão:** A1 não preenche literalmente ContinuousCoreData. Existe uma obrigação de compatibilidade de domínios e ciclicidade do campo legado, além das entradas concretas de suporte/split/gap de A2. As construções consultadas não fornecem essas entradas já instanciadas no mesmo core. A parede demonstrável abaixo refuta adaptações naturais específicas; NÃO demonstra impossibilidade de todo o contrato nem exige sua alteração.

## 1. O pedido exato

ORDEM011:113:

> ### A2 — H1 e os Three Locks no MESMO core (quita `qgf_unconditional_continuous_corner_proved` e `gpf_H1_internal_susy_relative_gap_discharged`)
Operadores dos Three Locks realizados nesse core (afiliação e domínios), a projeção do núcleo **P_F no core** com **0 < τ(P_F) < ∞** pelo traço de A1, e o gap
relativo para os operadores contínuos efetivos — usando `threeLocksFromSupport` onde as entradas forem de fato produzidas.
**Aceitação:** termo de `ThreeLocksCoreData` construído a partir dos dados de A1 (não recebidos como hipótese); identificação de P_F com a projeção espectral

TGL/ModularRealization.lean:68–83 exige `Core : Type` com `Ring`, `StarRing`, `Algebra ℂ`, embedding injetivo da cunha, ação dual e:

```text
canonicalTrace : Core -> ENNReal
trace_zero : canonicalTrace 0 = 0
trace_tracial : forall x y, canonicalTrace(x*y)=canonicalTrace(y*x)
trace_star : forall x, canonicalTrace(star x)=canonicalTrace x
trace_dual_scaling : canonicalTrace(theta_s x)=ofReal(exp(-s))*canonicalTrace x
```

A1 fornece `scalarInverseLimitTraceData.{u} P : RegularCoreTraceData.{u} P`, cujo value é literalmente `scalarInverseLimitWeight P : PositiveCoreInput P -> ENNReal`. Seu campo tracial é igualdade entre `positiveSquare a` e `positiveSquare (star a)`. O cone positivo não é um anel: não pode ser escolhido como `Core` mantendo as operações exigidas. Não há coerção que converta a igualdade quadrática na igualdade de valores em produtos arbitrários, que podem não ser positivos.

A ponte necessária, sem reformular contrato, seria uma função total F:N->ENNReal acompanhada dos quatro campos legados e de uma igualdade explícita F(X)=tau(X) para todo X positivo do MESMO core; W,D e o embedding requerido continuam precisando casar por tipo. Esse é um alvo de adaptação, não uma hipótese a inserir para declarar A2 construído. Mesmo a igualdade em todos positivos é uma condição de identificação do traço A1, não um campo novo que esta consulta acrescenta ao contrato antigo.

## 2. Parede exata dos atalhos — e seu limite

[DERIVED — cálculo matemático, não novo teorema Lean] Em M2, tome p=e11 e n=e12. Temos pn=n, np=0, n* n=e22 e |n|=e22. Para qualquer traço positivo fiel tau, tau(e22)>0 (finitude nem é necessária). Logo F(x)=tau(x*x) satisfaz F(pn)>0=F(np); F(x)=tau(|x|) falha igualmente. Ambas coincidem com tau nas projeções, mas isso não basta para `trace_tracial`. Assim não usar o mapa quadrático de A1 como `canonicalTrace` para quitar o campo legado.

A extensão linear usual de um traço positivo é complexa no ideal integrável; ela não é automaticamente uma função ENNReal em TODO o anel. Também não se pode declarar valor infinito fora do ideal e esperar ciclicidade: produtos com um fator projetor podem dar n e zero no exemplo acima, inclusive quando n não é integrável numa amplificação infinita.

**Não concluo que o contrato legado seja impossível.** Ele não exige aditividade/linearidade em todo Core. Por exemplo, no caso matricial finito, x->|Tr(x)| é uma função ENNReal (via ofReal) cíclica, invariante por estrela e coincide com o traço nos positivos, embora não linear. Isso é ilustração de compatibilidade desses campos, não fornecedor da ação dual do core atual. O exemplo zero já está em V350CoreContractCounterexample, e o próprio arquivo prova que ele não fornece ThreeLocks com traço positivo. Portanto a lacuna é um adaptador legítimo ainda não localizado, não uma contradição deduzida do codomínio isoladamente.

## 3. Projeção finita e faces

[REAL — enunciados lidos] `scalarInverseLimitWeight_finite_contractions` devolve E_n em N, norm<=1, tau(E_n*E_n)<infinito e E_n->1 fortemente. Não devolve E_n^2=E_n. `scalarInverseLimitWeight_finite_minorants` entrega minorantes positivos finitos e agora recebe a tracialidade34 efetivamente paga. Não devolve automaticamente uma projeção espectral. `unitIntervalProjection_idempotent` é uma projeção no Hilbert regular; o resultado lido não inclui pertinência ao core nem traço A1 finito.

[DERIVED/OPEN — menor entrada útil] Extrair de um positivo finito não nulo uma projeção espectral de limiar q, com 0<q e c*q<=X para algum c>0, pagaria tau(q)<=tau(X)/c<infinito. A1 já paga a parte de ordem/fidelidade; falta um fornecedor concreto para essa extração no mesmo N, com pertinência e idempotência. Não reabrir a construção do peso. Semifinitude/fidelidade não tornam uma projeção arbitrária escolhida divisível em faces iguais; em particular uma projeção minimal não serve ao split exigido.

Uma possível economia, ainda DERIVED/OPEN: escolher a projeção finita e sob e11 de um sistema matricial já representado e usar uma parcial isometria v com v*v=e11 e vv*=e22. Então e e v e v* são ortogonais e têm o mesmo traço pela igualdade quadrática A1; q=e+v e v* tem traço positivo finito. **Não localizei nesta consulta a escolha dessa e com domínio/pertinência/traço já provados**, nem declaro preenchidos os dados matriciais correspondentes. Essa rota evita exigir um teorema global de divisibilidade de toda projeção, mas permanece candidato de aplicação, não fornecedor pronto.

A calibração para tau(q)=1 pode usar theta_(log tau(q).toReal), preservando as projeções e o split. O lema antigo `dual_calibration_exists` recebe um ThreeLocksCoreData pronto; chamá-lo para produzir o q necessário ao mesmo construtor seria circular. Reusar sua conta exp/log diretamente com `scalarInverseLimitWeight_dual` depois de obter q é a dependência correta.

[DERIVED — parede de escolha] Qualquer projeção não nula que seja FIXA pela ação dual não pode ter traço A1 positivo finito: tau(q)=exp(-1)*tau(q) força tau(q) em {0,infinito}; fidelidade exclui zero. Portanto usar uma projeção de uma subálgebra fixa só por ser matricial não paga PF. A aplicação a uma projeção concreta requer exibir que ela é fixa; não presumi isso de um nome.

## 4. Gap e projeção do zero: o que as assinaturas realmente dizem

`threeLocksFromSupport` recebe todo o suporte e split, incluindo tau(q)=1. Atribui H3Lt=1-q e prova aniquilação/maximalidade por álgebra. Isso é reutilizável depois de fornecer os dados, mas não produz o suporte. `ThreeLocksCoreData` não tem campo numérico de gap nem domínio de operador ilimitado; codifica transformada limitada e maximalidade. A2, além desse termo, exige identificação com os operadores contínuos efetivos e sua projeção espectral. Não substituir essa identificação pela escolha de um homônimo.

Para Hmin=1-q atuando no Hilbert, a decomposição por uma projeção ortogonal fornece ker(Hmin)=range(q) e Hmin é identidade no complemento: a estimativa de gap é elementar para ESSE representante. Ligá-lo a um operador Three Locks previamente especificado é uma obrigação separada; a consulta não inventa esse operador nem afirma que ele já coincide.

`SusyRelativeData` é reticular e recebe `free_gap_finite`, `gap_relative`, `diff_finite`, `ker_le_gap`, `ker_ne_bot`. `susy_relative_gives_breuer` é a implicação depois desses dados. O modelo `modelSusy` mora em ENNReal com peso identidade; não é uma instanciação no core de A1. A camada `SubadditiveTraceData` ainda pede subaditividade sobre sup reticular; aditividade de tau em positivos não constitui sozinha esse adaptador de projeções.

`concrete_breuer_corner_conditional` recebe auto-adjunção, `SpectralApproximationWitness`, kernel não trivial e inclusão do kernel em subespaço FINITO-DIMENSIONAL. A conclusão usa `semifiniteDimTrace` em submódulos, não tau=scalarInverseLimitWeight. Uma projeção tau-finita pode ter dimensão Hilbert infinita. Não transportar essa conclusão por homonímia nem cobrar dimensão finita desnecessariamente do core.

`SemifiniteSeed.matrix_trace_is_faithful_weight` trata matrizes reais finitas; `TheNonMinimalCoupling.the_split_is_inhabited` trata M2. São provas genéricas/concretas em outros tipos. Nenhuma é o consumidor A2 instanciado no mesmo N/traço. O resultado `split_forbids_minimality` explica por que um candidato de posto um sozinho não paga faces não nulas iguais.

## 5. Próximo passo mínimo e estatutos

1. **OPEN — fronteira de tipos:** nomear o adaptador de traço total exigido pelo legado e sua identificação com A1 nos positivos; não preencher com quadrados, módulo ou zero sem provar ciclicidade. Não propor alteração silenciosa do contrato.
2. **OPEN — dados consumíveis:** fornecedor de projeção não nula tau-finita no mesmo core, split ortogonal de traço igual e calibração; reusar A1 para ordem/fidelidade/tracialidade/escala.
3. **REAL genérico / OPEN concreto:** aplicar CoreSupport depois desses dados e provar a identificação espectral/domínios para o representante admitido por A2. Reusar os resultados genéricos de gap somente quando seus tipos forem realmente instanciados com tau e os operadores efetivos.

Nenhum aceite A2 nesta consulta. A consolidação mantém A2–A7 separados. ORDEM012 já entregue não é reaberta. Ausência no recorte lido não é ausência universal do acervo. As primeiras tentativas de localização CoreSupport/ModularRealization em TGLExt falharam e foram corrigidas para TGL; um padrão de glob Windows passado como caminho literal foi recusado e não foi contado como busca negativa de provas.

## Fontes, tipos e pins relidos

### 1. structure ContinuousCoreData

[ModularRealization.lean:68](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\ModularRealization.lean:68>) — 11569 bytes; SHA256 `17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348`.

```lean
structure ContinuousCoreData (W : TGLSpecificAQFTWitness) (D : WedgeModularData W) where
  Core : Type
  [instCoreRing : Ring Core]
  [instCoreStarRing : StarRing Core]
  [instCoreAlgebra : Algebra ℂ Core]
  embedding : D.wedgeAlgebra.toStarSubalgebra →⋆ₐ[ℂ] Core
  embedding_injective : Function.Injective embedding
  dualAction : ℝ → (Core ≃⋆ₐ[ℂ] Core)
  dualAction_zero : dualAction 0 = StarAlgEquiv.refl
  dualAction_add : ∀ s t : ℝ, dualAction (s + t) = (dualAction s).trans (dualAction t)
  canonicalTrace : Core → ENNReal
  trace_zero : canonicalTrace 0 = 0
  trace_tracial : ∀ x y : Core, canonicalTrace (x * y) = canonicalTrace (y * x)
  trace_star : ∀ x : Core, canonicalTrace (star x) = canonicalTrace x
  trace_dual_scaling : ∀ (s : ℝ) (x : Core),
    canonicalTrace ((dualAction s) x) = ENNReal.ofReal (Real.exp (-s)) * canonicalTrace x

```

### 2. structure ThreeLocksCoreData

[ModularRealization.lean:100](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\ModularRealization.lean:100>) — 11569 bytes; SHA256 `17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348`.

```lean
structure ThreeLocksCoreData (W : TGLSpecificAQFTWitness) (D : WedgeModularData W)
    (C : ContinuousCoreData W D) where
  H3Lt : C.Core
  H3Lt_selfAdjoint : star H3Lt = H3Lt
  PF : C.Core
  PF_selfAdjoint : star PF = PF
  PF_idempotent : PF * PF = PF
  PF_locks : PF * H3Lt = 0
  PF_maximal : ∀ q : C.Core, star q = q → q * q = q → q * H3Lt = 0 → q * PF = q
  PF_nonzero : PF ≠ 0
  PF_trace_pos : 0 < C.canonicalTrace PF
  PF_trace_finite : C.canonicalTrace PF < ⊤
  Pplus : C.Core
  Pminus : C.Core
  Pplus_selfAdjoint : star Pplus = Pplus
  Pplus_idempotent : Pplus * Pplus = Pplus
  Pminus_selfAdjoint : star Pminus = Pminus
  Pminus_idempotent : Pminus * Pminus = Pminus
  split : Pplus + Pminus = PF
  orthogonal : Pplus * Pminus = 0
  trace_split_additive : C.canonicalTrace PF = C.canonicalTrace Pplus + C.canonicalTrace Pminus
  equal_face_trace : C.canonicalTrace Pplus = C.canonicalTrace Pminus

```

### 3. noncomputable def threeLocksFromSupport

[CoreSupport.lean:71](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\CoreSupport.lean:71>) — 6731 bytes; SHA256 `041fb863b07c3e0a167d5d0c8a522890d2da61586f41c27be2b06c46fac588e0`.

```lean
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
```

### 4. theorem support_maximal

[CoreSupport.lean:60](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\CoreSupport.lean:60>) — 6731 bytes; SHA256 `041fb863b07c3e0a167d5d0c8a522890d2da61586f41c27be2b06c46fac588e0`.

```lean
theorem support_maximal (q r : A) (hr : r * (1 - q) = 0) : r * q = r := by
  rw [mul_sub, mul_one, sub_eq_zero] at hr
  exact hr.symm
```

### 5. theorem dual_calibration_exists

[VerbInhabitant.lean:112](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\VerbInhabitant.lean:112>) — 6545 bytes; SHA256 `812a47f0e71a86f37368c918b0f704cccad9cda0e32c4aee64c5566e7808a5d7`.

```lean
theorem dual_calibration_exists {W : TGLSpecificAQFTWitness}
    {D : WedgeModularData W} (C : ContinuousCoreData W D)
    (T : ThreeLocksCoreData W D C) :
    ∃ s : ℝ, C.canonicalTrace ((C.dualAction s) T.PF) = 1 := by
  refine ⟨Real.log (C.canonicalTrace T.PF).toReal, ?_⟩
  rw [C.trace_dual_scaling]
  have hx0 : C.canonicalTrace T.PF ≠ 0 := T.PF_trace_pos.ne'
  have hxt : C.canonicalTrace T.PF ≠ ⊤ := T.PF_trace_finite.ne
  have hxr : 0 < (C.canonicalTrace T.PF).toReal := ENNReal.toReal_pos hx0 hxt
  rw [Real.exp_neg, Real.exp_log hxr]
  rw [ENNReal.ofReal_inv_of_pos hxr, ENNReal.ofReal_toReal hxt]
  exact ENNReal.inv_mul_cancel hx0 hxt

end TGL.VerbInhabitant
```

### 6. structure SubadditiveTraceData

[SusyRelativeGap.lean:59](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SusyRelativeGap.lean:59>) — 8700 bytes; SHA256 `3aa058b5c4f098e3218ffed0bc8271a28947b56af81750019e1360754873e7f2`.

```lean
structure SubadditiveTraceData (L : Type) [Lattice L] [BoundedOrder L]
    extends SemifiniteTraceData L where
  subadd : ∀ p q : L, tau (p ⊔ q) ≤ tau p + tau q

/-- [DATA — Q8.3, nível 4] o certificado SUSY-relativo: gap do livre
    τ-finito (fisicamente ⊥); gap do perturbado sob livre ⊔ diferença
    (Weyl relativo, face reticular); diferença τ-finita; kernel no gap. -/
structure SusyRelativeData (L : Type) [Lattice L] [BoundedOrder L]
    (T : SubadditiveTraceData L) where
  ker : L
  gapD : L
  gapD0 : L
  diff : L
  free_gap_finite : T.tau gapD0 < ⊤
  gap_relative : gapD ≤ gapD0 ⊔ diff
  diff_finite : T.tau diff < ⊤
  ker_le_gap : ker ≤ gapD
  ker_ne_bot : ker ≠ ⊥
```

### 7. theorem susy_relative_gives_breuer

[SusyRelativeGap.lean:103](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SusyRelativeGap.lean:103>) — 8700 bytes; SHA256 `3aa058b5c4f098e3218ffed0bc8271a28947b56af81750019e1360754873e7f2`.

```lean
theorem susy_relative_gives_breuer (S : SusyRelativeData L T) :
    0 < T.tau S.ker ∧ T.tau S.ker < ⊤ :=
  breuer_kernel_weight S.toBreuerGapData

```

### 8. def modelSusy

[SusyRelativeGap.lean:115](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SusyRelativeGap.lean:115>) — 8700 bytes; SHA256 `3aa058b5c4f098e3218ffed0bc8271a28947b56af81750019e1360754873e7f2`.

```lean
def modelSusy : SusyRelativeData ℝ≥0∞ idTraceSub where
  ker := 1
  gapD := 1
  gapD0 := ⊥
  diff := 1
  free_gap_finite := bot_lt_top
  gap_relative := le_sup_right
  diff_finite := ENNReal.one_lt_top
  ker_le_gap := le_rfl
  ker_ne_bot := one_ne_zero

/-- [KERNEL] ★ CONSISTÊNCIA do nível 4: o certificado não é vazio. -/
theorem susy_relative_package_consistent :
    Nonempty (SusyRelativeData ℝ≥0∞ idTraceSub) := ⟨modelSusy⟩
```

### 9. def SpectralApproximationWitness

[SpectralReduction.lean:149](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SpectralReduction.lean:149>) — 8677 bytes; SHA256 `5e52f59e86bb353f6315d6f68accd6687ad958597a87b554012ed1ca92e6dab9`.

```lean
def SpectralApproximationWitness (T : H →L[ℂ] H) : Prop :=
  ∃ p : ℕ → Polynomial ℂ, ∀ x,
    Filter.Tendsto (fun n => (Polynomial.aeval T (p n)) x)
      Filter.atTop (nhds ((T.ker).starProjection x))
```

### 10. theorem concrete_breuer_corner_conditional

[SpectralReduction.lean:168](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SpectralReduction.lean:168>) — 8677 bytes; SHA256 `5e52f59e86bb353f6315d6f68accd6687ad958597a87b554012ed1ca92e6dab9`.

```lean
theorem concrete_breuer_corner_conditional (hH : ¬FiniteDimensional ℂ H)
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T)
    (hW : SpectralApproximationWitness T)
    (gp : Submodule ℂ H) (hker : T.ker ≠ ⊥)
    (hle : T.ker ≤ gp) (hgp : FiniteDimensional ℂ gp) :
    ((T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer ∧
      (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer) ∧
      ((0 < (semifiniteDimTrace ℂ H).tau T.ker ∧
          (semifiniteDimTrace ℂ H).tau T.ker < ⊤) ∧
        (semifiniteDimTrace ℂ H).tau (T.ker)ᗮ = ⊤) := by
  have hframe := breuer_corner_full_algebraic_frame hH T hsa gp hker hle hgp
  exact ⟨⟨corner_in_algebra_of_approximation T hW, hframe.1.1⟩, hframe.2⟩
```

### 11. theorem matrix_trace_is_faithful_weight

[SemifiniteSeed.lean:115](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SemifiniteSeed.lean:115>) — 5422 bytes; SHA256 `9e91547595c6fdfa37c5d9b786bf3b1e5b774fa90fa4ff0a01a463a775e77dc5`.

```lean
theorem matrix_trace_is_faithful_weight :
    (∀ A : Matrix n n ℝ, A.PosSemidef → 0 ≤ A.trace) ∧
      (∀ A : Matrix n n ℝ, A.PosSemidef → (A.trace = 0 ↔ A = 0)) ∧
      (∀ A B : Matrix n n ℝ, (B - A).PosSemidef → A.trace ≤ B.trace) :=
  ⟨fun _ hA => hA.trace_nonneg, psd_trace_eq_zero_iff, trace_monotone_of_psd_sub⟩

```

### 12. theorem split_forbids_minimality

[TheNonMinimalCoupling.lean:97](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheNonMinimalCoupling.lean:97>) — 6920 bytes; SHA256 `03576ea2958ffc4c3802b332227dfc7ef2b52e538881e602bfc15e2a81a21cec`.

```lean
theorem split_forbids_minimality (e f g : Matrix n n ℂ)
    (hsplit : f + g = e) (horth : f * g = 0) (hf : f * f = f) (hgne : g ≠ 0) :
    f * e = f ∧ f ≠ e := by
  constructor
  · rw [← hsplit, mul_add, hf, horth, add_zero]
  · intro h
    apply hgne
    have hg2 : g = e - f := by rw [← hsplit]; abel
    rw [hg2, h, sub_self]
```

### 13. theorem the_split_is_inhabited

[TheNonMinimalCoupling.lean:110](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheNonMinimalCoupling.lean:110>) — 6920 bytes; SHA256 `03576ea2958ffc4c3802b332227dfc7ef2b52e538881e602bfc15e2a81a21cec`.

```lean
theorem the_split_is_inhabited :
    ∃ e f g : Matrix (Fin 2) (Fin 2) ℂ,
      f + g = e ∧ f * g = 0 ∧ f * f = f ∧ g * g = g
      ∧ f ≠ 0 ∧ g ≠ 0 ∧ f ≠ e := by
  refine ⟨1, !![1, 0; 0, 0], !![0, 0; 0, 1], ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.one_apply]
  · ext i j; fin_cases i <;> fin_cases j <;>
```

### 14. structure RegularCoreTraceData

[V351RegularCoreTraceContract.lean:43](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceContract.lean:43>) — 5624 bytes; SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`.

```lean
structure RegularCoreTraceData (P : SiteProfile) where
  value : PositiveCoreInput P → ℝ≥0∞
  zero : value (PositiveCoreInput.zero P) = 0
  additive : ∀ A B, value (A.add B) = value A + value B
  homogeneous : ∀ (r : ℝ≥0) A, value (A.scale r) = (r : ℝ≥0∞) * value A
  monotone : ∀ A B, A ≤ B → value A ≤ value B
  faithful : ∀ A, value A = 0 ↔ A = PositiveCoreInput.zero P
  normal : ∀ {ι : Type u} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (_hmono : Monotone A) (hS : IsLUB (Set.range A) S),
    value ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, value ⟨(A i).val, (A i).property, hpos i⟩
  semifinite : ∀ A, value A =
    ⨆ (B : PositiveCoreInput P) (_ : B ≤ A) (_ : value B < ⊤), value B
  tracial : ∀ a, value (positiveSquare P a) = value (positiveSquare P (star a))
  dual_scaling : ∀ s A, value (positiveDual P s A) =
    ENNReal.ofReal (Real.exp (-s)) * value A

theorem RegularCoreTraceData.not_zero (P : SiteProfile)
    (T : RegularCoreTraceData.{u} P) : T.value ≠ fun _ => 0 := by
  intro h
  have hz : T.value (positiveUnit P) = 0 := congrFun h _
  exact positiveUnit_ne_zero P ((T.faithful _).mp hz)
```

### 15. def scalarInverseLimitTraceData

[V351RegularCoreTraceConstruction.lean:15](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceConstruction.lean:15>) — 1095 bytes; SHA256 `f741525cfa335d89221834fdb01e3f3c6b8efa435b107f0a355cc5679fe06b40`.

```lean
def scalarInverseLimitTraceData (P : SiteProfile) : RegularCoreTraceData.{u} P where
  value := scalarInverseLimitWeight P
  zero := scalarInverseLimitWeight_zero P
  additive := scalarInverseLimitWeight_add P
  homogeneous := scalarInverseLimitWeight_scale P
  monotone := scalarInverseLimitWeight_mono P
  faithful := scalarInverseLimitWeight_faithful P
  normal := scalarInverseLimitWeight_normal P
  semifinite := scalarInverseLimitWeight_finite_minorants P (scalarInverseLimitWeight_tracial P)
  tracial := scalarInverseLimitWeight_tracial P
  dual_scaling := scalarInverseLimitWeight_dual P

```

### 16. theorem scalarInverseLimitWeight_finite_contractions

[V351InverseLimitFiniteMinorants.lean:14](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitFiniteMinorants.lean:14>) — 6831 bytes; SHA256 `fca7ff37994a84ee7cc5707f66d670c6cf46dadf9500da10f4f06fa932cc296c`.

```lean
theorem scalarInverseLimitWeight_finite_contractions (P : SiteProfile) :
    ∃ E : ℕ → (regularCoreAlgebra P).toStarSubalgebra,
      (∀ n, ‖(E n).val‖ ≤ 1) ∧
      (∀ n, scalarInverseLimitWeight P (positiveSquare P (E n)) < ⊤) ∧
      (∀ v, Tendsto (fun n => (E n).val v) atTop (𝓝 v)) := by
```

### 17. theorem scalarInverseLimitWeight_finite_minorants

[V351InverseLimitFiniteMinorants.lean:84](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitFiniteMinorants.lean:84>) — 6831 bytes; SHA256 `fca7ff37994a84ee7cc5707f66d670c6cf46dadf9500da10f4f06fa932cc296c`.

```lean
theorem scalarInverseLimitWeight_finite_minorants (P : SiteProfile)
    (htr : ∀ a : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P a) =
        scalarInverseLimitWeight P (positiveSquare P (star a)))
    (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X =
      ⨆ (Y : PositiveCoreInput P) (_ : Y ≤ X)
        (_ : scalarInverseLimitWeight P Y < ⊤), scalarInverseLimitWeight P Y := by
```

### 18. theorem scalarInverseLimitWeight_dual

[V351InverseLimitScaling.lean:91](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitScaling.lean:91>) — 5377 bytes; SHA256 `2aa1344d9f0ebbf8b3b87b1354b9ec20e10f0fd8b842789e925819c0c2b097ab`.

```lean
theorem scalarInverseLimitWeight_dual (P : SiteProfile) (s : ℝ) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (TGLV351.positiveDual P s X) =
      ENNReal.ofReal (Real.exp (-s)) * scalarInverseLimitWeight P X := by
  change (⨆ n : ℕ, scalarInverseCutoffWeight P (1/((n : ℝ)+1))
```

### 19. theorem scalarInverseLimitWeight_faithful

[V351InverseLimitFaithful.lean:50](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitFaithful.lean:50>) — 2713 bytes; SHA256 `c8ea383ff05cfee0c3ae5b92e9fffee44c56b0f0c2224eef4cba81ecc398ff99`.

```lean
theorem scalarInverseLimitWeight_faithful (P : SiteProfile) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X = 0 ↔ X = PositiveCoreInput.zero P := by
  constructor
```

### 20. theorem unitIntervalProjection_idempotent

[V350UnitIntervalProjection.lean:71](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350UnitIntervalProjection.lean:71>) — 3880 bytes; SHA256 `60b0cf134b9db7b6fbd286dd2b039452a2f7420a2bf2ababbc5240568b6343b2`.

```lean
theorem unitIntervalProjection_idempotent :
    unitIntervalProjection (H := H) * unitIntervalProjection = unitIntervalProjection := by
```

### 21. legacy zero model; incompatibility with positive ThreeLocks

[V350CoreContractCounterexample.lean:12](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CoreContractCounterexample.lean:12>) — 1960 bytes; SHA256 `1aaa11d4c572c2ad3c0c80a54322247233b64e6e16e28710cd4ccc0d3524de0e`.

```lean
def zeroTraceLegacyCore (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (D : WedgeModularData W) : ContinuousCoreData W D where
  Core := D.wedgeAlgebra.toStarSubalgebra
  instCoreRing := inferInstance
  instCoreStarRing := inferInstance
  instCoreAlgebra := inferInstance
  embedding := StarAlgHom.id ℂ D.wedgeAlgebra.toStarSubalgebra
  embedding_injective := Function.injective_id
  dualAction := fun _ => StarAlgEquiv.refl
  dualAction_zero := rfl
  dualAction_add := fun _ _ => rfl
  canonicalTrace := fun _ => 0
  trace_zero := rfl
  trace_tracial := fun _ _ => rfl
  trace_star := fun _ => rfl
  trace_dual_scaling := by intro s x; simp

/-- The purported canonical trace may vanish on every element under the
legacy signature, even though the algebra embedding is injective. -/
theorem legacy_contract_accepts_zero_trace
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (D : WedgeModularData W) :
    ∃ C : ContinuousCoreData W D, ∀ x : C.Core, C.canonicalTrace x = 0 :=
  ⟨zeroTraceLegacyCore W D, fun _ => rfl⟩

/-- This countermodel cannot supply a positive-trace Three-Locks corner.
It diagnoses the core contract without claiming to bypass the full witness. -/
theorem zeroTraceLegacyCore_has_no_threeLocks
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (D : WedgeModularData W) :
    ¬ Nonempty (ThreeLocksCoreData W D (zeroTraceLegacyCore W D)) := by
  rintro ⟨T⟩
  exact (lt_irrefl (0 : ENNReal)) T.PF_trace_pos

```

A proveniência de objetos anteriores, quando encontrada, está no JSON; ela não é aceite A2. Nenhum build foi executado nesta consulta.
