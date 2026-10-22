# Ficha A2 — reaproveitamento antes de código

[REAL — leitura; construção A2 ainda OPEN.]

2026-09-15T12:14:24.806686-03:00

Consumidores: ThreeLocksCoreData e qgf_unconditional_continuous_corner_proved / gpf_H1_internal_susy_relative_gap_discharged, conforme ORDEM011 §3.A2. O adendo exige o MESMO regularCoreAlgebra P e o valor scalarInverseLimitTraceData. O objetivo integral não se reduz ao primeiro lema.

- REUSAR scalarInverseLimitTraceData: obter positivo finito não nulo sob qualquer positivo não nulo a partir do campo semifinite e faithful. Não reconstruir peso ou tracialidade.
- ADAPTAR IsStarProjection.mem_iff: projeção ortogonal do núcleo de A em N pertence a N por invariância sob comutante. O alvo é exatamente pertinência do futuro corte espectral A2.
- ADAPTAR CFC posPart/negPart: de X positivo finito não nulo extrair limiar epsilon>0 e q projetor não nulo com epsilon*q<=X. Usar ordem/homogeneidade/fidelidade A1 para traço positivo finito. Prova ainda a construir.
- ADAPTAR sistema matricial representado para obter faces iguais com tracialidade A1. Semicorte finito sob projeção matricial, não projeção dual-fixa tomada como finita.
- REUSAR CoreSupport quando suporte, faces e traço compatíveis forem produzidos; gap do representante 1-q não identifica outro operador por nome.
- OPEN contrato: ContinuousCoreData exige função total cíclica em Core->ENNReal; A1 fornece traço no cone. Não usar tau(x*x) como extensão cíclica, não alterar silenciosamente o contrato. Essa obrigação não desaparece com a existência da projeção.

## Buscas e limites

1. `ThreeLocks|threeLocks|finite.*projection|projection.*finite|RegularCoreTraceData|SpectralApproximationWitness` em kernel canônico e cópia K, nomes e enunciados: Contratos legados, CoreSupport, SusyRelativeGap, SpectralReduction/ExactWitness, traço A1. Resultados amplos tiveram stdout truncado; fornecedores relevantes foram abertos separadamente. Consulta não executou um.py.

2. `ThreeLocks|P_F|projection|gap|projeção` em notas 11–13/09, TRACO_PROXIMAS_OBRIGACOES, CONVENCOES_DO_TRACO, AUDITORIA_DAS_PENDENCIAS, MAPA_GATE_E_REAPROVEITAMENTO: CoreSupport já construía Hmin=1-q recebendo suporte. Não há ponte automática para traço A1 no cone. Estados OPEN históricos de A1 são superados pelo aceite34. DEV de pesos/grafos não fornece projeção A2 pelo nome.

3. `ThreeLocks|P_F|finite.*projection|projection.*finite|Spectral` em ENTREGA_0*.md e consulta_A2_CONTRATO anterior: Consulta anterior delimita suporte, split, gap, fronteira do traço total. ENTREGAs de A1 reutilizáveis não são ThreeLocks construídos. A ausência é relativa às buscas, não universal.

4. `Three Locks|H1|A2|core|traço` em A_PROVA_DA_QG_TGL_arvore.md canônico: Adendo v354 registra A1 concluído e falta A2. Antigo adendo v353 OPEN sobrevive historicamente; não reabrir A1. Não foram lidos resultados de natureza para mover gate.

5. `ThreeLocks|threeLocks|finite.*projection|projection.*finite|spectralProjection|spectral_projection|RegularCoreTraceData` em C:\IALD\Artigo\BANCADA_TOE\kernel_bancada, *.lean: Ocorrências em TheAngleIsTheProjection/CoFoundation/ObserverReadsTheAngle; projeções matriciais de outro tipo, não suporte finito do mesmo core.

6. `threeLocksFromSupport|scalarInverseLimitTraceData|proje[cç][aã]o.{0,35}tra[cç]o.{0,20}finit` em buscar.py --ctx 140 --max 22: Consulta rc0 truncou nos registros de julho. Refinamento --desde 2026-09-10 devolveu ZERO DOCUMENTOS INDEXADOS, não ausência de provas recentes. buscar.py omite erros de leitura de corpus; índice não constitui busca exaustiva confiável por si. Leitura recente feita diretamente nas fontes e pastas atuais.

mathlib. `exists.*StarProjection|starProjection|ker.*commut|posPart_sub_negPart` em Mathlib Analysis/VonNeumannAlgebra e ContinuousFunctionalCalculus: IsStarProjection.mem_iff fornece critério exato de pertinência; adaptar à projeção do núcleo. CFC.posPart/negPart e corte de limiar são candidatos para finitude; extrair projeção via invariância evita pedir antecipadamente SpectralApproximationWitness.

## Tipos e fornecedores lidos

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\ModularRealization.lean:68 — SHA256 17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348

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

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\ModularRealization.lean:100 — SHA256 17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348

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

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGL\CoreSupport.lean:71 — SHA256 041fb863b07c3e0a167d5d0c8a522890d2da61586f41c27be2b06c46fac588e0

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

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceContract.lean:43 — SHA256 3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0

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

```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceConstruction.lean:15 — SHA256 f741525cfa335d89221834fdb01e3f3c6b8efa435b107f0a355cc5679fe06b40

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

#print axioms scalarInverseLimitTraceData
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SusyRelativeGap.lean:66 — SHA256 3aa058b5c4f098e3218ffed0bc8271a28947b56af81750019e1360754873e7f2

```lean
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

variable {L : Type} [Lattice L] [BoundedOrder L] {T : SubadditiveTraceData L}

/- ═══════ 2. Nível 4 ⟹ nível 3 ⟹ (B3) ═══════ -/

```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:154 — SHA256 bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86

```lean
theorem IsStarProjection.mem_iff {e : H →L[ℂ] H} (he : IsStarProjection e)
    (S : VonNeumannAlgebra H) :
    e ∈ S ↔ ∀ y ∈ S.commutant, e.range ∈ Module.End.invtSubmodule y := by
  simp_rw [he.isIdempotentElem.mem_iff, he.isIdempotentElem.range_mem_invtSubmodule_iff,
    he.isIdempotentElem.ker_mem_invtSubmodule_iff, forall_and, and_iff_left_iff_imp, ← mul_def]
  intro h x hx
  simpa [he.isSelfAdjoint.star_eq] using! congr(star $(h _ (star_mem hx)))

```

Nenhum aceite A2. Cache Mathlib e objetos A1 já aceitos podem ser REUSADOS em DEV, com proveniência explícita; os objetos novos terão reprodução e revisão separadas antes de entrega. Nenhum build canônico/um.py/rito experimental autorizado nesta bancada.
