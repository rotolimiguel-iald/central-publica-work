2026-09-15T03:00:03.062577-03:00

[STATIC/DERIVED — consulta, não aceite34]

[STATIC] Não identifiquei falha matemática nos três privados do snapshot. root_quadratic_commutation usa somente R>=0 e Commute R A; não exige A positivo/auto-adjunto. bounded_root_form_balance recebe explicitamente 0<=T<=1, comutações com U/V e balanço limitado, e entrega igualdade complexa de formas. double_cut_form_supremum usa upper bounds p,q<=1, positividade de C,D, comutações cruzadas e limites fortes; passa ao limite um índice por vez em ENNReal. Não exige finitude, monotonicidade das famílias, cota uniforme de C/D ou produto ilimitado. As metades 0<=p e 0<=q não são usadas nessa prova; são hipóteses redundantes benignas, não motivo para alterar o candidato. O rc0/trio é relido do DEV autoral, não compilação própria nem aceite34.

[REAL — fornecedor direto] Para a:coreSubtype e ha:a in finiteDualStarCore P, forme Aa:finiteDualStarCore P com valor a. scalarStarCore_mem_closedTomitaDomain (P:=P) Aa e scalarClosedTomita_extends_star (P:=P) Aa fornecem exatamente o domínio e S x=Lambda(a*) para x=scalarGNSStarEmbedding P Aa. Não é necessário reusar toda a prova de fechamento do peso para este caso.

[REAL — identidade dos embeddings] scalarUniformToWeightStar P Aa inclui no núcleo pleno, scalarWeightStarEmbedding_uniform iguala seu embedding ao x antigo e scalarUniformToWeightStar_star compatibiliza a estrela. Alternativamente, Aa determina ai:finiteDualLeftIdeal P com prova Aa.property.1; scalarWeightGNSEmbedding_uniform P ai iguala o embedding de Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) ai ao embedding antigo. Isto fornece o A:scalarWeightLeftIdeal P exigido pela identidade do peso perturbado, sem assumir I=n_nu. Se o código já usa scalarWeightStarCore, scalarWeightStar_mem_closedTomitaDomain e scalarClosedTomita_extends_weight_star são a alternativa pronta.

[DERIVED/OPEN — forma do peso] Para epsilon>0, ponha s=hilbertPositiveSqrt(B_epsilon), b=⟨s,hb⟩ com a prova de pertença devolvida por scalarWeight_inverseCutoff_perturbed_norm, e L=pi(star b). O fornecedor dá nu(s* a*a s)=ofReal ||L(J^-1 Lambda a)||^2. Usando map_star/map_mul, IsSelfAdjoint.of_nonneg da raiz e CFC.sqrt_mul_sqrt_self no MESMO B_epsilon, obtenha star L * L=pi(B_epsilon). ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left dá a forma com (pi B)v na primeira posição; inner_re_symm troca para Re<v,pi B v>. A ponte RCLike.re_eq_complex_re já é usada em PerturbedWeightOrder. Por scalarTomitaPolarFactor_involutive, J^-1 v=J v. Assim a forma desejada é ENNReal.ofReal(Re<J Lambda a,pi(B_epsilon) J Lambda a>), não uma igualdade do peso com um número complexo. Não é preciso identificar pi(sqrt B) com sqrt(pi B) ou definir outra raiz. Este último adaptador de norma/forma não foi compilado nesta consulta.

[DERIVED/OPEN — ligação final] Domínio de S implica domínio da raiz por scalarClosedTomitaDomain_le_root, cujo domínio é range sqrt(T). Escolha u representando x; y=sqrt(1-T)u é o valor da raiz por bounded_graph_lift_apply. Há ainda um atalho de tipos: scalarTomita_sqrt_factor P u entrega diretamente S aplicado ao lift no domínio original = J y; scalarTomitaRootLift_coe e Subtype.ext ligam esse lift a x. Com S x=Lambda(a*), fica J Lambda(a*)=y usando a involução. A forma do peso para a dá o supremo em Jx; para a* dá o supremo em y. double_cut_form_supremum então tem o consumidor correto quando suas hipóteses concretas forem descarregadas. finiteDualStarCore não é aqui chamado núcleo analítico; nenhum domínio de produto ilimitado é acrescentado.

[OPEN] Falta a instanciação concreta destes três privados e os adaptadores de embeddings/Gram/supremos. Nenhuma dessas pontes foi certificada por esta consulta. O snapshot não prova fulltrace, Q global ou gate. Não foi lida a fonte mutável K/V351QuadraticTrace.lean, nem houve compilação/escrita Lean.

Snapshot lido: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\dev_quadratic_trace\20260915_025534_427264\V351QuadraticTrace.lean; 4142 bytes; SHA256 695f6c7922cd04e8ef5e0a6f924e80017f24a7daf86208cc3d7ed6c77ae256f1.

Fornecedores relidos, com tipos/trechos exatos:

Domínio e estrela diretamente no núcleo uniforme — [V350ScalarClosedTomita.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarClosedTomita.lean:159>)

~~~lean
theorem scalarStarCore_mem_closedTomitaDomain (A : finiteDualStarCore P) :
    scalarGNSStarEmbedding P A ∈ scalarClosedTomitaDomain P :=
  ⟨scalarGNSStarEmbedding P (star A),subset_closure ⟨A,rfl⟩⟩

theorem scalarClosedTomita_extends_star (A : finiteDualStarCore P) :
    scalarClosedTomita P ⟨scalarGNSStarEmbedding P A,scalarStarCore_mem_closedTomitaDomain A⟩ =
      scalarGNSStarEmbedding P (star A) :=
  scalarTomitaGraph_closure_single_valued P (scalarGNSStarEmbedding P A) _ _
    (scalarClosedTomita_graph ⟨scalarGNSStarEmbedding P A,scalarStarCore_mem_closedTomitaDomain A⟩)
    (subset_closure ⟨A,rfl⟩)
~~~

Embedding uniforme concreto — [V350ScalarGNSStarDensity.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSStarDensity.lean:13>)

~~~lean
def scalarGNSStarEmbedding (P : SiteProfile) (A : finiteDualStarCore P) :
    ScalarGNSHilbert P := scalarGNSEmbedding P ⟨A.val,A.property.1⟩
~~~

Inclusão do núcleo uniforme no núcleo do peso e igualdade dos embeddings — [V350ScalarWeightStarCore.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightStarCore.lean:43>)

~~~lean
def scalarWeightStarEmbedding (P : SiteProfile) (A : scalarWeightStarCore P) : ScalarGNSHilbert P :=
  scalarWeightGNSEmbedding P ⟨A.val,A.property.1⟩

def scalarUniformToWeightStar (P : SiteProfile) (A : finiteDualStarCore P) : scalarWeightStarCore P :=
  ⟨A.val,HasFiniteDualSquare.scalar_finite P _ A.property.1,
    HasFiniteDualSquare.scalar_finite P _ A.property.2⟩

theorem scalarUniformToWeightStar_star (P : SiteProfile) (A : finiteDualStarCore P) :
    scalarUniformToWeightStar P (star A) = star (scalarUniformToWeightStar P A) := rfl

theorem scalarWeightStarEmbedding_uniform (P : SiteProfile) (A : finiteDualStarCore P) :
    scalarWeightStarEmbedding P (scalarUniformToWeightStar P A) = scalarGNSStarEmbedding P A :=
  scalarWeightGNSEmbedding_uniform P ⟨A.val,A.property.1⟩
~~~

Alternativa direta no núcleo pleno do peso — [V350ScalarWeightTomitaIdentification.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightTomitaIdentification.lean:65>)

~~~lean
theorem scalarWeightStar_mem_closedTomitaDomain (P : SiteProfile)
    (A : scalarWeightStarCore P) :
    scalarWeightStarEmbedding P A ∈ scalarClosedTomitaDomain P :=
  ⟨scalarWeightStarEmbedding P (star A),
    scalarWeightTomitaGraph_subset_closure_original P ⟨A,rfl⟩⟩

theorem scalarClosedTomita_extends_weight_star (P : SiteProfile)
    (A : scalarWeightStarCore P) :
    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P (star A) :=
  scalarTomitaGraph_closure_single_valued P (scalarWeightStarEmbedding P A) _ _
    (scalarClosedTomita_graph ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩)
    (scalarWeightTomitaGraph_subset_closure_original P ⟨A,rfl⟩)
~~~

Inclusão I em n_nu, sem igualdade de ideais — [V350ScalarWeightDomain.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightDomain.lean:43>)

~~~lean
def scalarWeightLeftIdeal (P : SiteProfile) :
    Submodule ℂ (regularCoreAlgebra P).toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare P A.val}
  zero_mem' := HasFiniteScalarSquare.zero P
  add_mem' := fun hA hB => HasFiniteScalarSquare.add P _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteScalarSquare.smul P c _ hA

theorem finiteDualLeftIdeal_le_scalarWeight (P : SiteProfile) :
    finiteDualLeftIdeal P ≤ scalarWeightLeftIdeal P :=
  fun A hA => HasFiniteDualSquare.scalar_finite P A.val hA
~~~

Embedding do peso pleno coincide com o antigo na inclusão — [V350ScalarWeightCompletion.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightCompletion.lean:90>)

~~~lean
def scalarWeightGNSEmbedding (P : SiteProfile) : scalarWeightLeftIdeal P →ₗ[ℂ] ScalarGNSHilbert P :=
  (scalarWeightLinear P).codRestrict (scalarGNSSubspace P) (scalarWeightOrbit_mem_original_GNS P)

theorem scalarWeightGNSEmbedding_uniform (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    scalarWeightGNSEmbedding P (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) A) =
      scalarGNSEmbedding P A := Subtype.ext (scalarWeightOrbit_uniform P A)
~~~

Norma de corte com raiz e J originais — [V351PerturbedWeightNorm.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean:37>)

~~~lean
theorem scalarWeight_inverseCutoff_perturbed_norm (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (A : scalarWeightLeftIdeal P) :
    ∃ hb : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      dualQuadraticIntegral
        (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) *
          (star A.val.val * A.val.val) *
          hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P) =
      ENNReal.ofReal (‖scalarGNSRepresentation P
        (star (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),hb⟩ :
          (regularCoreAlgebra P).toStarSubalgebra))
        ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))‖^2) := by
  obtain ⟨hb,hr⟩ := regularInverseGeneratorCutoff_sqrt_right P ε hε
  exact ⟨hb,scalarWeight_right_perturbed_norm P _ hr A⟩
~~~

Wrapper da raiz e conjugação antiunitária — [V350AntiunitaryPositiveConjugation.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:14>)

~~~lean
/-- Fix the canonical Hilbert-operator CFC instances before specializing H. -/
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H := CFC.sqrt T

theorem hilbertComplement_nonneg (T : H →L[ℂ] H) (h : T ≤ 1) : 0 ≤ 1-T :=
  sub_nonneg.mpr h

/-- Complex-linear conjugation by an antiunitary; U need not be involutive. -/
def antiunitaryConjugate (T : H →L[ℂ] H) : H →L[ℂ] H :=
  U.toLinearIsometry.toContinuousLinearMap.comp
    (T.comp U.symm.toLinearIsometry.toContinuousLinearMap)

theorem antiunitaryConjugate_apply (T : H →L[ℂ] H) (x : H) :
    antiunitaryConjugate U T x=U (T (U.symm x)) := rfl
~~~

Lift do grafo, S da raiz e involução original — [V350ScalarTomitaPolarInvolution.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPolarInvolution.lean:56>)

~~~lean
def scalarTomitaRootLift (x : ScalarGNSHilbert P) : (scalarTomitaPositiveRoot P).domain :=
  boundedGraphLift (hilbertPositiveSqrt (scalarTomitaResolvent P)) (hilbertPositiveSqrt (1-scalarTomitaResolvent P))
    (positive_sqrt_injective _ (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P)) x

theorem scalarTomitaRootLift_coe (x : ScalarGNSHilbert P) :
    (scalarTomitaRootLift P x : ScalarGNSHilbert P)=hilbertPositiveSqrt (scalarTomitaResolvent P) x := rfl

theorem scalarTomita_sqrt_factor (x : ScalarGNSHilbert P) :
    scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
      (scalarTomitaRootLift P x)) =
        scalarTomitaPolarFactor P (hilbertPositiveSqrt (1-scalarTomitaResolvent P) x) :=
  (scalarTomitaPolarFactor_root P (scalarTomitaRootLift P x)).symm.trans
    (congrArg (scalarTomitaPolarFactor P) (bounded_graph_lift_apply _ _ _ x))

/-- Involution is proved from the original S, its resolvent and the positive root.
It is not inserted as a premise of the polar construction. -/
theorem scalarTomitaPolarFactor_involutive : Function.Involutive (scalarTomitaPolarFactor P) := by
~~~

Fatorização no domínio original — [V350ScalarTomitaPolarFactor.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPolarFactor.lean:49>)

~~~lean
theorem scalarTomitaPolarFactor_root (x : (scalarTomitaPositiveRoot P).domain) :
    scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P x)=scalarTomitaRootImage P x :=
  denseAntilinearEquiv_apply _ _ _ _ _ x

/-- Exact S=UB on the full domain D(S), with both maps on the same H_I. -/
theorem scalarTomitaPolarFactor_factorization (x : scalarClosedTomitaDomain P) :
    scalarTomitaPolarFactor P
      (scalarTomitaPositiveRoot P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x))=
        scalarClosedTomita P x :=
  scalarTomitaPolarFactor_root P (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x)
~~~

Identidade dos domínios S e raiz — [V350ScalarTomitaRootDomain.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaRootDomain.lean:30>)

~~~lean
theorem scalarClosedTomitaDomain_le_root :
    scalarClosedTomitaDomain P ≤ (scalarTomitaPositiveRoot P).domain :=
  graphCore_norm_domain_transfer (scalarClosedTomitaDomain P)
    (scalarTomitaPositiveRoot P).domain (scalarTomitaSquare P).domain
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
    (scalarTomitaSquareDomain_le P) (scalarTomitaSquareDomain_le_root P)
    (scalarTomitaSquare_graph_core P) (scalarTomitaRoot_real_graph_closed P)
    (scalarTomitaSquare_norm_match P)

theorem scalarTomitaRootDomain_le_closed :
    (scalarTomitaPositiveRoot P).domain ≤ scalarClosedTomitaDomain P :=
  graphCore_norm_domain_transfer (scalarTomitaPositiveRoot P).domain
    (scalarClosedTomitaDomain P) (scalarTomitaSquare P).domain
    ((scalarTomitaPositiveRoot P).toFun.restrictScalars ℝ)
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    (scalarTomitaSquareDomain_le_root P) (scalarTomitaSquareDomain_le P)
    (scalarTomitaSquare_root_graph_core P) (scalarClosedTomita_is_closed (P := P))
    (fun x => (scalarTomitaSquare_norm_match P x).symm)

/-- Exact equality on the original GNS space, not an unspecified equivalent model. -/
theorem scalarTomitaPositiveRoot_domain_eq :
    (scalarTomitaPositiveRoot P).domain = scalarClosedTomitaDomain P :=
  le_antisymm (scalarTomitaRootDomain_le_closed P) (scalarClosedTomitaDomain_le_root P)
~~~

Domínio exatamente range sqrt(T) — [V350ResolventSquareRoot.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:33>)

~~~lean
def resolventSquareRoot (R : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R) :
    H →ₗ.[ℂ] H := boundedGraphOperator (CFC.sqrt R) (CFC.sqrt (1-R))
      (positive_sqrt_injective R hR hi)

theorem resolventSquareRoot_domain (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) :
    (resolventSquareRoot R hR hi).domain = (CFC.sqrt R).range := rfl

~~~

Valor no lift do grafo — [BoundedGraphOperator.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean:76>)

~~~lean
theorem bounded_graph_parameter_lift (A B : E →L[ℂ] E)
    (hAi : Function.Injective A) (h : E) :
    boundedGraphParameter A hAi (boundedGraphLift A B hAi h) = h := by
  apply hAi
  rw [bounded_graph_parameter_apply]
  rfl

theorem bounded_graph_lift_apply (A B : E →L[ℂ] E) (hAi : Function.Injective A) (h : E) :
    boundedGraphOperator A B hAi (boundedGraphLift A B hAi h) = B h := by
  rw [bounded_graph_apply, bounded_graph_parameter_lift]
~~~

Definição do peso cortado — [V351InverseLimitWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:13>)

~~~lean
/-- Evaluate the original dual weight after conjugation by the existing root.
The regulator is mathematical; no new physical parameter is introduced. -/
def scalarInverseCutoffWeight (P : SiteProfile) (ε : ℝ) (X : PositiveCoreInput P) : ℝ≥0∞ :=
  dualQuadraticIntegral
    (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) * X.val *
      hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P)
~~~

Supremo sequencial do MESMO peso — [V351InverseLimitWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:85>)

~~~lean
/-- Candidate inverse-generator perturbation, as a monotone supremum of
the actual cutoff weights. This definition alone does not assert a trace. -/
def scalarInverseLimitWeight (P : SiteProfile) (X : PositiveCoreInput P) : ℝ≥0∞ :=
  ⨆ n : ℕ, scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X
~~~

Exemplo privado de adaptação da identidade de norma; não fornecedor público — [V351PerturbedWeightOrder.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightOrder.lean:11>)

~~~lean
private theorem star_apply_norm_sq_mono {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B C : H →L[ℂ] H) (hbc : B*star B ≤ C*star C) (v : H) :
    ‖star B v‖^2 ≤ ‖star C v‖^2 := by
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (sub_nonneg.mpr hbc)
  have hv := hp.re_inner_nonneg_left v
  have hn (D : H →L[ℂ] H) :
      ‖star D v‖^2 = (inner ℂ ((D*star D) v) v).re := by
    have he := ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left
      (𝕜 := ℂ) (star D) v
    simpa only [RCLike.re_eq_complex_re,ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint,ContinuousLinearMap.mul_def] using he
  rw [hn B,hn C]
  simpa only [RCLike.re_eq_complex_re,sub_apply,inner_sub_left,Complex.sub_re,
    sub_nonneg] using hv
~~~

Identidade pública de norma do operador limitado — [Adjoint.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Adjoint.lean:143>)

~~~lean
theorem apply_norm_sq_eq_inner_adjoint_left (A : E →L[𝕜] F) (x : E) :
    ‖A x‖ ^ 2 = re ⟪(A† ∘L A) x, x⟫ := by
  have h : ⟪(A† ∘L A) x, x⟫ = ⟪A x, A x⟫ := by rw [← adjoint_inner_left]; rfl
  rw [h, ← inner_self_eq_norm_sq (𝕜 := 𝕜) _]

theorem apply_norm_eq_sqrt_inner_adjoint_left (A : E →L[𝕜] F) (x : E) :
    ‖A x‖ = √(re ⟪(A† ∘L A) x, x⟫) := by
  rw [← apply_norm_sq_eq_inner_adjoint_left, Real.sqrt_sq (norm_nonneg _)]
~~~

Troca da ordem dos vetores na parte real — [Basic.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Basic.lean:79>)

~~~lean
theorem inner_re_symm (x y : E) : re ⟪x, y⟫ = re ⟪y, x⟫ := by rw [← inner_conj_symm, conj_re]
~~~

