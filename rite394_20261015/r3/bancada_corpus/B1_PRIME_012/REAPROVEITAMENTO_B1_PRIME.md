[OPEN — ficha autoral ANTES do codigo B1 prime]

Data UTC: 2026-09-15T15:13:31.806595+00:00

NOVO somente contrato de operadores, EOM tipada, extensao de B1 e paredes; REUSAR B1 sem reprovar.

Consumidor PROPOSTO: ext_pb_same_beta_four_faces_kernel_proved -> TGLExt.the_same_beta_reads_four_faces. Nao instalado.

Tipo planejado (notacao descritiva):
```text
ActionCouplingData (X : Type u): boxOperator : (X -> Complex) ->_l[Real] (X -> Complex); mass : Real; xi : Real; scalarCurvature : X -> Real; K_boundary : (X -> Complex) ->_l[Real] (X -> Complex).
fieldOperator D Psi := D.boxOperator Psi - D.mass^2 smul Psi - D.xi smul (fun x => D.scalarCurvature x smul Psi x).
modularSource D c Psi := c.beta smul D.K_boundary Psi.
EOM D c Psi : Prop := fieldOperator D Psi = modularSource D c Psi.
the_same_beta_reads_four_faces (c:TGLCoupling) (D:ActionCouplingData X) (Psi:X->Complex) (hEOM:D.EOM c Psi) (rho_r rho_m rho_L:Real): todas as seis clausulas exatas de the_same_beta_reads_three_faces c rho_r rho_m rho_L, seguidas da EOM expandida com o MESMO c.beta.
Controles: coeficiente adulterado, sinal trocado, xi confundido com beta, termo conforme omitido, K trocado, ausencia de hEOM, unicidade sem fonte nao nula. Provar paredes semanticas e testar termos adulterados sintaticamente validos.
```

Copiar projeto e caches por bytes para raiz nova. Lake build com Lean4.31; sem hardlinks/junctions externos; fontes locais de dependencia TGL/TGLExt recompiladas; caches Mathlib/pacotes copiados, nao reconstruidos. Auditoria #print axioms com nomes completos e verificacao calculada de subconjunto de propext/Classical.choice/Quot.sound; controles por lake env lean com diagnostico semantico. Cada tentativa preservada.

Limites e hipoteses:
- EOM e INPUT nomeado: nao se deriva variacao de funcional de acao, nem existencia/regularidade de solucao fisica.
- K_boundary sera operador linear real importado sobre secoes X->Complex. Nao se afirma ser gerador Stone/Tomita, autoadjunto, afiliado ou nao limitado.
- xi e variavel independente: nao identificada com beta nem fixada em 1/6. Independencia de papel nao e prova de desigualdade numerica xi != beta.
- boxOperator e dado linear, nao construcao do dAlembertiano de uma metrica. scalarCurvature:X->Real e dado, nao computacao de Ricci.
- Unicidade de coeficiente so quando K_boundary(Psi) != 0. Campo nulo satisfaz a equacao linear; nao e certificado de realizacao. Exibir modelo algebrico nao nulo e parede sem premissa EOM.
- B1 preservado: alpha e leitura beta/exp(1/2), nao CODATA; fundo e algebra; vazamento exige gap positivo.
- Fontes canonicas de outra casa retornaram Acesso negado. Artigo A original nao foi lido: forma EOM provem do adendo efetivamente lido [INPUT/DECLARADO]. Nao certificar estado v354 pelo indice.
- Revisao desta bancada e autoral; exame independente e aceite final reservados ao operador. Sem edicao de um.py, D1, gate, B3, A2, Atlas, memorias preexistentes ou tunel.

CONSUMIDOR_EXISTENTE_NA_COPIA — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\um.py
SHA256 c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40; 12864360 bytes. Tipo casa exatamente: False.
Mapa _LEAN_THEOREM_FLAGS e leitura efetiva do relatorio de axiomas; copia historica da bancada, nao arquivo canonico atual.
```text
128077: _LEAN_THEOREM_FLAGS = {
128078:     "half_nat_kernel_proved": "TGL.HalfNat.halfNat_of_selfConjugate",
128079:     "area_scale_kernel_proved": "TGL.AreaScale.newtonPlanck_equivalence",
128080:     "finite_three_locks_kernel_proved": "TGL.FiniteThreeLocks.ker_H3L_eq_threeLocks",
128081:     "finite_corner_projection_kernel_proved": "TGL.FiniteThreeLocks.PF_isProjection",
128082:     "finite_corner_trace_kernel_proved": "TGL.FiniteThreeLocks.normalizedCornerTrace_PF",
```
```text
133714:     "ext_rp_lambda_drops_kernel_proved": "TGLExt.lambda_drops_out",
133715:     "ext_rp_closure_identity_kernel_proved": "TGLExt.closure_identity",
133716:     "ext_rp_hubble_form_kernel_proved": "TGLExt.hubble_form",
133717:     "ext_rp_w_bounds_kernel_proved": "TGLExt.w_bounds",
133718:     "ext_rp_background_kernel_proved": "TGLExt.the_background_closure",
```
```text
134484:     for flag, thm in _LEAN_THEOREM_FLAGS.items():
134485:         ax = axioms.get(thm)
134486:         res[flag] = bool(res["lake_build_ok"] and ax is not None
134487:                          and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
134488:                          and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))
134489:     # v99: leituras do certificado de fechamento (nomes futuros; ausencia => False)
```

REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheSameBetaReadsThreeFaces.lean
SHA256 2efd8b379f210111e0383d9c40e5fc72835f41cd94aad2dd70d645d66f400c16; 3838 bytes. Tipo casa exatamente: True.
TGLCoupling, dominio beta e todas as clausulas do teorema anterior: consumo direto no alvo.
```text
22: structure TGLCoupling where
23:   beta : ℝ
24:   beta_pos : 0 < beta
25:   beta_lt_one : beta < 1
26: 
27: namespace TGLCoupling
28: 
29: noncomputable section
30: 
31: /-- The cost-normalized reading; no independent alpha parameter is introduced. -/
32: def alpha (c : TGLCoupling) : ℝ := c.beta / Real.exp (1 / 2)
33: 
34: theorem alpha_pos (c : TGLCoupling) : 0 < c.alpha :=
35:   div_pos c.beta_pos (Real.exp_pos _)
36: 
37: theorem alpha_lt_one (c : TGLCoupling) : c.alpha < 1 := by
38:   unfold alpha
39:   apply (div_lt_one (Real.exp_pos _)).mpr
40:   exact c.beta_lt_one.trans the_minimal_volume_exceeds_one
41: 
42: theorem beta_eq_alpha_exp (c : TGLCoupling) :
43:     c.beta = c.alpha * Real.exp (1 / 2) := by
44:   exact (div_mul_cancel₀ c.beta (Real.exp_ne_zero _)).symm
45: 
46: theorem beta_eq_alpha_radical (c : TGLCoupling) :
47:     c.beta = c.alpha * Real.sqrt (Real.exp 1) := by
48:   rw [boundary_extracts_the_radical.1]
49:   exact c.beta_eq_alpha_exp
50: 
51: /-- The existing reflected amplitude, squared, reads precisely the same beta. -/
52: theorem reflection_weight (c : TGLCoupling) :
53:     Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta := by
54:   have h := (the_pruning_threshold_is_the_reflection_amplitude
55:     c.beta_pos.le c.beta_lt_one.le).1
56:   rwa [Real.sq_sqrt c.beta_pos.le] at h
57: 
58: /-- The same cost variable appears in the reflected weight without a new axiom. -/
59: theorem reflection_cost (c : TGLCoupling) :
60:     Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) =
61:       c.alpha * Real.sqrt (Real.exp 1) :=
62:   c.reflection_weight.trans c.beta_eq_alpha_radical
63: 
64: /-- Negative control: dropping the geometric cost changes the reflected weight. -/
65: theorem reflection_rejects_bare_alpha (c : TGLCoupling) :
66:     Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) ≠ c.alpha := by
67:   rw [c.reflection_weight, c.beta_eq_alpha_exp]
68:   have h := mul_lt_mul_of_pos_left the_minimal_volume_exceeds_one c.alpha_pos
69:   simpa only [mul_one] using ne_of_gt h
70: 
71: end
72: end TGLCoupling
73: 
74: /-- All clauses use the same projection c.beta. The background clauses are
75:     algebraic identities, not an imported or assumed Friedmann equation. -/
76: theorem the_same_beta_reads_three_faces (c : TGLCoupling) (ρr ρm ρΛ : ℝ) :
77:     Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta
78:     ∧ (0 < c.alpha ∧ c.alpha < 1
79:       ∧ c.beta = c.alpha * Real.exp (1 / 2)
80:       ∧ c.beta = c.alpha * Real.sqrt (Real.exp 1))
81:     ∧ (c.beta * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
82:         = c.beta * ((4 / 3) * ρr + ρm))
83:     ∧ ((ρr + ρm + ρΛ) + c.beta * ((4 / 3) * ρr + ρm)
84:         = (1 + 4 * c.beta / 3) * ρr + (1 + c.beta) * ρm + ρΛ)
85:     ∧ (∀ t g : ℝ, 0 < t → 0 < g → Real.exp (-(t * c.beta * g)) < 1)
86:     ∧ (∀ b : ℝ, (∀ t : ℝ, Real.exp (-(t * b)) = Real.exp (-(t * c.beta)))
87:         → b = c.beta) := by
88:   exact ⟨c.reflection_weight,
89:     ⟨c.alpha_pos, c.alpha_lt_one, c.beta_eq_alpha_exp, c.beta_eq_alpha_radical⟩,
90:     closure_identity c.beta ρr ρm ρΛ,
91:     hubble_form c.beta ρr ρm ρΛ,
92:     fun _ _ ht hg => leakage_strictly_loses ht c.beta_pos hg,
93:     fun _ h => leakage_rate_unique h⟩
94: 
95: end TGLExt
```

REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheVerbalCoupling.lean
SHA256 912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507; 11431 bytes. Tipo casa exatamente: False.
Consumo transitivo por B1; fornece amplitude com 0<=beta<=1. Nao fornece EOM.
```text
126: def thetaMiguel (β : ℝ) : ℝ := Real.arcsin (Real.sqrt β)
127: 
128: /-- **A FUNÇÃO DE ACOPLAMENTO VERBAL** da patente: `f(θ) = tanh((θ − θ_M)/Δθ)`. -/
129: def fVerbal (θ θM Δ : ℝ) : ℝ := Real.tanh ((θ - θM) / Δ)
130: 
131: /-- **O PISO DE HILBERT VERBAL**: o sinal mínimo exigido de cada frase, `β · S_max`. -/
132: def verbFloor (β Smax : ℝ) : ℝ := β * Smax
133: 
134: /-! ## B — o limiar de poda É a amplitude de reflexão -/
135: 
136: /-- [KERNEL] `sin(θ_Miguel β) = √β`. ⚠ **Elementar** — `Real.sin_arcsin` sobre
137:     `0 ≤ √β ≤ 1`. Está aqui só para servir à identificação seguinte, e o seu estatuto
138:     modesto fica dito. -/
139: theorem sin_thetaMiguel {β : ℝ} (h0 : 0 ≤ β) (h1 : β ≤ 1) :
140:     Real.sin (thetaMiguel β) = Real.sqrt β := by
141:   unfold thetaMiguel
142:   apply Real.sin_arcsin
143:   · linarith [Real.sqrt_nonneg β]
144:   · calc Real.sqrt β ≤ Real.sqrt 1 := Real.sqrt_le_sqrt h1
145:     _ = 1 := Real.sqrt_one
146: 
147: /-- [KERNEL] ★★★★★ **O LIMIAR DE PODA VERBAL É A AMPLITUDE DE REFLEXÃO DA FRONTEIRA.**
148: 
149:     Num enunciado só: em `θ = θ_Miguel`, a amplitude de reflexão da matriz-S vale `√β` — o
150:     mesmo número que a patente usa como limiar de poda (`g_ratio < √β ⟹ L_poda elimina`) —
151:     e ela fecha com a transmissão em 1.
152: 
153:     **Um só ângulo governa os dois domínios.** O que a patente chama de *vácuo verbal* é o
154:     que reflete menos que a amplitude da fronteira. -/
155: theorem the_pruning_threshold_is_the_reflection_amplitude {β : ℝ}
156:     (h0 : 0 ≤ β) (h1 : β ≤ 1) :
157:     Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 1)
158:         = Real.sqrt β ^ 2
159:     ∧ Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 1)
160:         + Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 0) = 1 := by
161:   refine ⟨?_, normSq_reflection_add_transmission _⟩
162:   rw [normSq_reflection, sin_thetaMiguel h0 h1]
163: 
164: /-! ## C — o acoplamento separa, e é aí que ele vale -/
165: 
```

REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\NoFullWitness.lean
SHA256 fde4ca999c40e6892d1958bee15a066786adb1363b8e3514f41eeb8b8909a654; 7250 bytes. Tipo casa exatamente: False.
Consumo transitivo por B1; t,beta,gap positivos e igualdade do semigrupo completo. Nao fornece operador de campo.
```text
66: theorem leakage_strictly_loses {t β g : ℝ} (ht : 0 < t) (hβ : 0 < β)
67:     (hg : 0 < g) : Real.exp (-(t * β * g)) < 1 := by
68:   have hneg : -(t * β * g) < 0 := by
69:     have := mul_pos (mul_pos ht hβ) hg
70:     linarith
71:   have h := Real.exp_lt_exp.mpr hneg
72:   rwa [Real.exp_zero] at h
73: 
74: /-- [KERNEL] ★ O FECHAMENTO PLENO EXIGE O PLANO: `e^{−tβg} = 1 ⟺ tβg = 0`
75:     — só na ausência total de contraste (ou de tempo, ou de β) o transporte
76:     fecha; a física observada (β > 0, gap > 0) mantém a passagem aberta. -/
77: theorem full_closure_iff_flat (t β g : ℝ) :
78:     Real.exp (-(t * β * g)) = 1 ↔ t * β * g = 0 := by
79:   constructor
80:   · intro h
81:     have h0 : Real.exp (-(t * β * g)) = Real.exp 0 := by
82:       rw [h, Real.exp_zero]
83:     have hinj := Real.exp_injective h0
84:     linarith
85:   · intro h
86:     rw [h, neg_zero, Real.exp_zero]
87: 
88: /-- [KERNEL] ★ O TEOREMA DO full_witness = False: β > 0 e contraste > 0
89:     PROÍBEM a testemunha estática plena — o transporte dissipativo não fixa
90:     tudo ("a testemunha não é full porque o Verbo continua"). -/
91: theorem beta_forbids_full_static_witness {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
92:     ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) := by
93:   intro hfull
94:   have h1 := hfull 1 1
95:   simp only [mul_one] at h1
96:   have hlt := leakage_strictly_loses one_pos hβ hg
97:   rw [h1] at hlt
```
```text
135: theorem leakage_rate_unique {b₁ b₂ : ℝ}
136:     (h : ∀ t : ℝ, Real.exp (-(t * b₁)) = Real.exp (-(t * b₂))) : b₁ = b₂ := by
137:   have h1 := Real.exp_injective (h 1)
138:   simp only [one_mul] at h1
139:   linarith
140: 
141: /-- [KERNEL] ★ A COMBINAÇÃO CANÔNICA: a testemunha canônica NÃO é plena
142:     (β > 0 proíbe o fechamento) E é Meia-Nat de fronteira (as duas faces
```

REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\RhoPlusPClosure.lean
SHA256 cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6; 4561 bytes. Tipo casa exatamente: False.
Consumo transitivo por B1; identidades algebricas para densidades livres, nao EOM ou Friedmann.
```text
47: theorem lambda_drops_out (ρΛ : ℝ) : ρΛ + (-ρΛ) = 0 := by ring
48: 
49: /-- [KERNEL] ★★★ A IDENTIDADE DO FECHAMENTO: com p_r = ρ_r/3, p_m = 0 e
50:     p_Λ = −ρ_Λ, a soma β·Σ(ρ_i+p_i) fecha EXATA em β[(4/3)ρ_r + ρ_m] —
51:     ρ_Λ cancela, para quaisquer densidades. -/
52: theorem closure_identity (β ρr ρm ρΛ : ℝ) :
53:     β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
54:       = β * ((4 / 3) * ρr + ρm) := by ring
55: 
56: /-- [KERNEL] ★★ A FORMA DO FUNDO: somar ρ_TGL ao total reescalona
57:     radiação e matéria e deixa Λ intacta — o ponto no plano (N_eff, ω_c). -/
58: theorem hubble_form (β ρr ρm ρΛ : ℝ) :
59:     (ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
60:       = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ := by ring
61: 
62: /-- [KERNEL] a equação de estado efetiva (face algébrica): w_T ∈ [0, 1/3],
```
```text
90: theorem the_background_closure (β ρr ρm ρΛ : ℝ) :
91:     (ρΛ + (-ρΛ) = 0)
92:     ∧ (β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
93:         = β * ((4 / 3) * ρr + ρm))
94:     ∧ ((ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
95:         = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ) :=
96:   ⟨lambda_drops_out ρΛ, closure_identity β ρr ρm ρΛ, hubble_form β ρr ρm ρΛ⟩
97: 
98: end
99: 
100: end TGLExt
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean
SHA256 6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0; 6817 bytes. Tipo casa exatamente: False.
EquilibriumInput.flow:A->A e kms algebrico. towerEquilibriumInput tem matriz de andar finito; nenhum gerador diferencial de seções. H->C exige H. Nao criar instancia inerte so por nome.
```text
73: structure EquilibriumInput (A : Type) [Mul A] [One A] where
74:   flow : A → A
75:   state : A → ℂ
76:   fixes_unit : flow 1 = 1
77:   kms : ∀ a b : A, state (a * b) = state (b * flow a)
78: 
79: /-! ## B — a ponte: a torre concreta fornece a entrada -/
80: 
81: /-- [KERNEL] ★★★ A TORRE FORNECE A ENTRADA: o fluxo modular de Tomita e o
82:     estado-produto do andar N formam um `EquilibriumInput`. Nada é
83:     postulado — as duas leis são os teoremas `towerFlow_id` e
84:     `tower_kms`, já em kernel. -/
85: def towerEquilibriumInput (l : ℝ) (hl : 0 < l) (N : ℕ) :
86:     EquilibriumInput (Matrix (chainIdx N) (chainIdx N) ℂ) where
87:   flow := towerFlow l N
88:   state := chainState l N
89:   fixes_unit := towerFlow_id l hl N
90:   kms := tower_kms l hl N
91: 
92: /-- [KERNEL] ★★★ A PONTE, INCONDICIONAL: em TODO andar da torre e para
93:     todo parâmetro positivo, a entrada existe e satisfaz as duas leis. É
```
```text
120:     implicação verdadeira cujo consequente é falso. Casar a FORMA da
121:     entrada não descarrega a hipótese; é preciso ter a hipótese. -/
122: theorem the_import_alone_concludes_nothing :
123:     ∃ H C : Prop, (H → C) ∧ ¬ C :=
124:   ⟨False, False, fun h => h, fun h => h⟩
125: 
126: /-- [KERNEL] A QUITAÇÃO POR IMPORTAÇÃO É MODUS PONENS: quem tem a hipótese
127:     disponível colhe o consequente sem pagar de novo o que já foi provado.
128:     Esta é a regra do operador, exata: não se paga duas vezes. -/
129: theorem discharge_by_import {H C : Prop} (h : H) (imported : H → C) : C :=
130:   imported h
131: 
132: /-- [KERNEL] ★★★★ O TRIO É UM PAR: dado o teorema mestre (H1∧H2∧H3 ⟹ P,
133:     já em kernel) e a implicação IMPORTADA (H2 → H3, de Jacobson 1995 com
134:     Bisognano–Wichmann, Unruh e Bekenstein–Hawking), a exigência
135:     reduz-se a H1∧H2 ⟹ P.
136: 
137:     O LUGAR (o horizonte de Rindler local, o boost) é a H2 quem dá; a
138:     TERMODINÂMICA sobre esse lugar já foi dada. Logo a dívida de kernel
139:     não é de três hipóteses nomeadas: é de DUAS. -/
140: theorem the_trio_is_a_pair {H1 H2 H3 P : Prop}
141:     (master : H1 ∧ H2 ∧ H3 → P) (imported : H2 → H3) :
142:     H1 ∧ H2 → P := by
143:   rintro ⟨h1, h2⟩
144:   exact master ⟨h1, h2, imported h2⟩
145: 
146: /-- [KERNEL] [HONESTIDADE] e a redução NÃO é gratuita: se a H2 não estiver
147:     disponível, o par não conclui — a mesma régua que vale para a dívida
148:     vale para a citação. -/
149: theorem the_pair_still_needs_its_hypotheses :
150:     ∃ H1 H2 P : Prop, (H1 ∧ H2 → P) ∧ ¬ P :=
151:   ⟨False, False, False, fun h => h.1, fun h => h⟩
152: 
153: end
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TowerModular.lean
SHA256 e3697a4f628eb1ae5211f004ac17d5867ccf60e705bb955d868229b118ee5550; 6315 bytes. Tipo casa exatamente: False.
towerFlow = conjugacao rho*a*rho_inv, sem parametro temporal no tipo. Nao igualar a K_boundary.
```text
97: 
98: /-- o fluxo modular de Tomita na torre: σ_N(a) = ρ_N · a · ρ_N⁻¹. -/
99: def towerFlow (l : ℝ) (N : ℕ)
100:     (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
101:     Matrix (chainIdx N) (chainIdx N) ℂ :=
102:   chainDensity l N * a * chainDensityInv l N
103: 
104: /-- [KERNEL] σ_N(1) = 1: o fluxo fixa a unidade. -/
105: theorem towerFlow_id (l : ℝ) (hl : 0 < l) (N : ℕ) :
106:     towerFlow l N 1 = 1 := by
107:   unfold towerFlow
108:   rw [mul_one, chainDensity_mul_inv l hl N]
109: 
110: /-- [KERNEL] ★★★ A CONDIÇÃO KMS NA TORRE: φ_N(ab) = φ_N(b·σ_N(a)) em TODO
111:     andar — a lei do estado de equilíbrio do fator SEM traço; o fluxo
112:     modular é a estrutura que substitui o traço morto (v129). -/
113: theorem tower_kms (l : ℝ) (hl : 0 < l) (N : ℕ)
114:     (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
115:     chainState l N (a * b) = chainState l N (b * towerFlow l N a) := by
116:   unfold chainState towerFlow
117:   have h1 : trace (chainDensity l N * (a * b))
118:       = trace (b * (chainDensity l N * a)) := by
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheDammingByExpansion.lean
SHA256 f139c3e660a93d79aafc1a629bec7347f4e63fc5310c470aa427cc76a8559025; 6058 bytes. Tipo casa exatamente: False.
the_form_does_not_fix_the_value recebe L,m,c nao nulos; alphaIdentity nao e TGLCoupling.alpha. Limite conceitual, sem ponte formal inventada.
```text
61: noncomputable section
62: 
63: /-- **O REQUISITO CENTRÍPETO**: a força que uma trajetória fechada exige, m·v²/r. -/
64: def centripetalRequirement (m v r : ℝ) : ℝ := m * v ^ 2 / r
65: 
66: /-- **A IDENTIDADE DE ALFA** da cadeia do operador: α := L/(m·c·r). -/
67: def alphaIdentity (L m c r : ℝ) : ℝ := L / (m * c * r)
68: 
69: /-- [KERNEL] o requisito lido no momento angular: v = L/(m·r) ⟹ F_c = L²/(m·r³). -/
70: theorem centripetal_from_angular {m L r : ℝ} (hm : m ≠ 0) (hr : r ≠ 0) :
71:     centripetalRequirement m (L / (m * r)) r = L ^ 2 / (m * r ^ 3) := by
72:   unfold centripetalRequirement
73:   field_simp
74: 
75: /-- [KERNEL] ★★★ **O REPRESAMENTO PAGA O REQUISITO.** Se o acoplamento equilibra a
76:     trajetória (e₂/r² = m·v²/r) e o momento angular é L = m·v·r, então
77:     e₂/(L·c) = v/c: o acoplamento em unidades de L·c É a velocidade da órbita em
78:     unidades de luz. A órbita fechada é luz represada; α é o nome da razão. -/
79: theorem the_damming_pays_the_requirement {e2 m v r c L : ℝ}
80:     (hm : m ≠ 0) (hv : v ≠ 0) (hr : r ≠ 0) (hc : c ≠ 0)
81:     (hL : L = m * v * r)
82:     (hbal : e2 / r ^ 2 = centripetalRequirement m v r) :
83:     e2 / (L * c) = v / c := by
84:   unfold centripetalRequirement at hbal
85:   have he2 : e2 = m * v ^ 2 * r := by
86:     have h := congrArg (fun x : ℝ => x * r ^ 2) hbal
87:     rw [div_mul_cancel₀ _ (pow_ne_zero 2 hr)] at h
88:     rw [h]
89:     field_simp
90:   subst hL
91:   rw [he2]
92:   field_simp
93: 
94: /-- [KERNEL] ★★ **AS TRÊS FACES DA IDENTIDADE**: L/(m·c·r) = (L/(m·r))/c = (L/(m·c))/r —
95:     o acoplamento, a velocidade em unidades de luz, e o comprimento de onda reduzido
96:     sobre o raio. Um objeto, três leituras, igualdade por álgebra. -/
97: theorem the_three_faces {L m c r : ℝ} (hm : m ≠ 0) (hc : c ≠ 0) (hr : r ≠ 0) :
98:     alphaIdentity L m c r = (L / (m * r)) / c
99:       ∧ alphaIdentity L m c r = (L / (m * c)) / r := by
100:   unfold alphaIdentity
101:   constructor
102:   · field_simp
103:   · field_simp
104: 
105: /-- [KERNEL] ★★★★★ **A FORMA NÃO FIXA O VALOR.** Para todo a ≠ 0 existe r ≠ 0 que
106:     realiza a identidade com valor a: a forma tem liberdade de UM parâmetro, e só a
107:     MEDIÇÃO a fecha. É o teorema que separa esta derivação da numerologia — e o que
108:     faz da distinção do operador ("a diferença não está na derivação, mas na
109:     medição") um par de teoremas em vez de uma frase. -/
110: theorem the_form_does_not_fix_the_value {L m c : ℝ}
111:     (hL : L ≠ 0) (hm : m ≠ 0) (hc : c ≠ 0) :
112:     ∀ a : ℝ, a ≠ 0 → ∃ r : ℝ, r ≠ 0 ∧ alphaIdentity L m c r = a := by
113:   intro a ha
114:   refine ⟨L / (m * c * a), ?_, ?_⟩
115:   · exact div_ne_zero hL (mul_ne_zero (mul_ne_zero hm hc) ha)
116:   · unfold alphaIdentity
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean
SHA256 5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8; 12687 bytes. Tipo casa exatamente: False.
B2: metric_only_einstein_equation consumido; U aberto/preconexo, a suave positivo, H_null e H_conservation. Equacao metrica, nao EOM Psi.
```text
167: theorem flrw_friedmann_second (U : Set Coordinate4) (hU : IsOpen U)
168:     (a rho pressure : ℝ → ℝ) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
169:     (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
170:     (coupling cosmological : ℝ)
171:     (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
172:       (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x +
173:       cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
174:     deriv (flrwHubble a) (x 0) = -coupling/2*(rho (x 0)+pressure (x 0)) := by
175:   have hz := (hpos x hx).ne'
176:   have hda : DifferentiableAt ℝ a (x 0) := (ha x hx).differentiableAt (by simp)
177:   have hdda : DifferentiableAt ℝ (deriv a) (x 0) :=
178:     ((ha x hx).derivWithin (m := ∞) (by simp)).differentiableAt (by simp)
179:   have hh : HasDerivAt (flrwHubble a)
180:       ((deriv (deriv a) (x 0)*a (x 0)-(deriv a (x 0))^2)/(a (x 0))^2) (x 0) := by
181:     simpa [flrwHubble, pow_two] using! hdda.hasDerivAt.div hda.hasDerivAt hz
182:   have h00 := flrw_friedmann_first U hU a rho pressure ha hpos x hx coupling cosmological hE
183:   have hacc := flrw_acceleration U hU a rho pressure ha hpos x hx coupling cosmological hE
184:   rw [hh.deriv]
185:   calc
186:     _ = deriv (deriv a) (x 0)/a (x 0)-(flrwHubble a (x 0))^2 := by
187:       unfold flrwHubble; field_simp
188:     _ = _ := by linarith
189: 
190: /-- Instantiates the existing general Einstein theorem, then reads the FLRW equations.
191: The null balance and covariant conservation remain explicit hypotheses. -/
192: theorem flrw_friedmann_from_general_metric
193:     (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
194:     (a rho pressure : ℝ → ℝ) (eta : ℝ)
195:     (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
196:     (hr : ∀ y∈U, DifferentiableAt ℝ rho (y 0))
197:     (hp : ∀ y∈U, DifferentiableAt ℝ pressure (y 0))
198:     (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
199:       tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
200:         (2*Real.pi/eta) • flrwStress a rho pressure x) v = 0)
201:     (H_conservation : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse (flrwMetric a))
202:       (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
203:       (flrwStress a rho pressure) x j = 0) :
204:     ∃ cosmological : ℝ, ∀ x∈U,
205:       (flrwHubble a (x 0))^2 = (2*Real.pi/eta)/3*rho (x 0)-cosmological/3 ∧
206:       deriv (flrwHubble a) (x 0) = -(2*Real.pi/eta)/2*(rho (x 0)+pressure (x 0)) ∧
207:       deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)) = 0 := by
208:   have hda : ∀ y∈U, DifferentiableAt ℝ a (y 0) :=
209:     fun y hy => (ha y hy).differentiableAt (by simp)
210:   obtain ⟨cosmological,hE⟩ := metric_only_einstein_equation U hU hconn
211:     (flrwMetric a) (flrwStress a rho pressure) (2*Real.pi/eta)
212:     (fun y hy => flrw_metric_lorentz a y (hpos y hy).ne') (flrw_metric_smooth U a ha)
213:     (flrw_stress_differentiable U a rho pressure hda hr hp)
214:     (fun x _ => flrw_stress_symmetric a rho pressure x) H_null H_conservation
215:   refine ⟨cosmological, fun x hx => ⟨?_,?_,?_⟩⟩
216:   · exact flrw_friedmann_first U hU a rho pressure ha hpos x hx _ _ (hE x hx)
217:   · exact flrw_friedmann_second U hU a rho pressure ha hpos x hx _ _ (hE x hx)
218:   · exact flrw_continuity a rho pressure x (hpos x hx).ne' (hda x hx)
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean
SHA256 2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3; 5398 bytes. Tipo casa exatamente: False.
B3: rho_i, w_i constantes, H_nx setorial explicita; continuidade nao produz K_boundary.
```text
20: structure SectorFluid (ι : Type*) [Fintype ι] (I : Set ℝ) (H : ℝ → ℝ) where
21:   rho : ι → ℝ → ℝ
22:   w : ι → ℝ
23:   rho_nonneg : ∀ i t, t ∈ I → 0 ≤ rho i t
24:   H_nx : ∀ i t, t ∈ I → HasDerivAt (rho i) (-3*H t*(1+w i)*rho i t) t
25: 
26: namespace SectorFluid
27: 
28: noncomputable section
29: 
30: variable {ι : Type*} [Fintype ι] {I : Set ℝ} {H : ℝ → ℝ}
31: 
32: def totalRho (F : SectorFluid ι I H) (t : ℝ) : ℝ := ∑ i, F.rho i t
33: def totalPressure (F : SectorFluid ι I H) (t : ℝ) : ℝ := ∑ i, F.w i*F.rho i t
34: def enthalpy (F : SectorFluid ι I H) (t : ℝ) : ℝ := ∑ i, (1+F.w i)*F.rho i t
35: def wEff (F : SectorFluid ι I H) (t : ℝ) : ℝ := F.totalPressure t/F.totalRho t
36: def correctedRho (F : SectorFluid ι I H) (c : TGLCoupling) (i : ι) (t : ℝ) : ℝ :=
37:   (1+c.beta*(1+F.w i))*F.rho i t
38: def correctedTotalRho (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) : ℝ :=
39:   ∑ i, F.correctedRho c i t
40: def correctedTotalPressure (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) : ℝ :=
41:   ∑ i, F.w i*F.correctedRho c i t
42: 
43: theorem enthalpy_eq (F : SectorFluid ι I H) (t : ℝ) :
44:     F.enthalpy t = F.totalRho t+F.totalPressure t := by
45:   simp [enthalpy, totalRho, totalPressure, add_mul, Finset.sum_add_distrib]
46: 
47: /-- Constant rescaling of the supplied non-exchange law, with the same w. -/
48: theorem sector_rescaling_preserves_continuity (F : SectorFluid ι I H)
49:     (c : TGLCoupling) (i : ι) (t : ℝ) (ht : t∈I) :
50:     HasDerivAt (F.correctedRho c i)
51:       (-3*H t*(1+F.w i)*F.correctedRho c i t) t := by
52:   convert! (F.H_nx i t ht).const_mul (1+c.beta*(1+F.w i)) using 1
53:   dsimp [correctedRho]
54:   ring
55: 
56: theorem corrected_closure (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) :
57:     F.correctedTotalRho c t = F.totalRho t+c.beta*F.enthalpy t := by
58:   unfold correctedTotalRho totalRho enthalpy
59:   simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
60:   apply Finset.sum_congr rfl
61:   intro i _
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFriedmann.lean
SHA256 7c115dd6a8d71333d8811a6efbf7d46d4363e25d18b23f8c7e678e951c0b9dfa; 4397 bytes. Tipo casa exatamente: False.
B3: G>0, H_null corrigido, totalRho>0, entalpia>=0; Lambda existencial; nao fornece EOM.
```text
36: /-- G is an area calibration; beta is the single datum of B1. -/
37: theorem tgl_friedmann_from_sector_closure
38:     (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
39:     (I : Set ℝ) (a : ℝ → ℝ) (F : SectorFluid ι I (flrwHubble a))
40:     (c : TGLCoupling) (G : ℝ) (hG : 0 < G)
41:     (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) (hpos : ∀ x∈U, 0 < a (x 0))
42:     (hI : ∀ x∈U, x 0∈I)
43:     (hr : ∀ x∈U, 0 < F.totalRho (x 0))
44:     (he : ∀ x∈U, 0 ≤ F.enthalpy (x 0))
45:     (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
46:       tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
47:         (2*Real.pi/(1/(4*G))) •
48:           flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) v = 0) :
49:     ∃ cosmological : ℝ, ∀ x∈U,
50:       (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
51:         F.totalRho (x 0)*(1+c.beta*|1+F.wEff (x 0)|)-cosmological/3 ∧
52:       deriv (flrwHubble a) (x 0) = -4*Real.pi*G*
53:         (F.correctedTotalRho c (x 0)+F.correctedTotalPressure c (x 0)) ∧
54:       deriv (F.correctedTotalRho c) (x 0)+3*flrwHubble a (x 0)*
55:         (F.correctedTotalRho c (x 0)+F.correctedTotalPressure c (x 0)) = 0 := by
56:   have hc := flrw_newton_coefficient G hG
57:   obtain ⟨cosmological, hF⟩ := flrw_friedmann_from_general_metric U hU hconn a
58:     (F.correctedTotalRho c) (F.correctedTotalPressure c) (1/(4*G)) ha hpos
59:     (fun x hx => (F.corrected_rho_deriv c (x 0) (hI x hx)).differentiableAt)
60:     (fun x hx => F.corrected_pressure_differentiable c (x 0) (hI x hx))
61:     H_null (fun x hx j => congrFun (sector_covariant_conservation I a F c x
62:       (hI x hx) (hpos x hx).ne' ((ha x hx).differentiableAt (by simp))) j)
63:   refine ⟨cosmological, fun x hx => ⟨?_,?_,(hF x hx).2.2⟩⟩
64:   · rw [(hF x hx).1, hc, F.multiplicative_closure c (x 0) (hr x hx) (he x hx)]
65:     ring
66:   · rw [(hF x hx).2.1]
67:     have hk : -(2*Real.pi/(1/(4*G)))/2 = -4*Real.pi*G := by linarith
68:     rw [hk]
69: 
70: /-- Specialization at an explicitly zero integration constant, using the full
71:     metric equation rather than assuming the desired scalar Friedmann law. -/
72: theorem tgl_friedmann_zero_cosmological
73:     (U : Set Coordinate4) (hU : IsOpen U) (I : Set ℝ) (a : ℝ → ℝ)
74:     (F : SectorFluid ι I (flrwHubble a)) (c : TGLCoupling) (G cosmological : ℝ)
75:     (hG : 0 < G) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
76:     (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
77:     (hr : 0 < F.totalRho (x 0)) (he : 0 ≤ F.enthalpy (x 0))
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean
SHA256 aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3; 6095 bytes. Tipo casa exatamente: False.
B4: HubbleHorizonInput com H,G,Phi positivos, derivada e fluxo com raio. Nao fornece operador de campo nem realiza H3.
```text
20: def hubbleArea (H : ℝ → ℝ) (t : ℝ) : ℝ := 4*Real.pi/(H t)^2
21: def entropyFactor (c : TGLCoupling) (w : ℝ) : ℝ := 1+c.beta*|1+w|
22: 
23: theorem entropy_factor_pos (c : TGLCoupling) (w : ℝ) : 0 < entropyFactor c w := by
24:   unfold entropyFactor
25:   have hb := mul_nonneg c.beta_pos.le (abs_nonneg (1+w))
26:   linarith
27: 
28: theorem hubble_area_derivative (H : ℝ → ℝ) (t : ℝ)
29:     (hh : DifferentiableAt ℝ H t) (hz : H t ≠ 0) :
30:     HasDerivAt (hubbleArea H) (-8*Real.pi*deriv H t/(H t)^3) t := by
31:   convert! (hasDerivAt_const t (4*Real.pi)).div (hh.hasDerivAt.pow 2) (pow_ne_zero _ hz) using 1
32:   simp only [Pi.pow_apply]
33:   field_simp
34:   ring
35: 
36: /-- Imported physical prescriptions, with the modified differential law named.
37:     The definitions of A, T and r_A are displayed directly in the fields. -/
38: structure HubbleHorizonInput (H : ℝ → ℝ) (t G Phi enthalpy : ℝ) where
39:   H_pos : 0 < H t
40:   G_pos : 0 < G
41:   Phi_pos : 0 < Phi
42:   H_diff : DifferentiableAt ℝ H t
43:   entropyRate : ℝ
44:   heatRate : ℝ
45:   differential_entropy : entropyRate = deriv (hubbleArea H) t/(4*G*Phi)
46:   enthalpy_flux : heatRate = hubbleArea H t*enthalpy*H t*(H t)⁻¹
47:   clausius : heatRate = (H t/(2*Real.pi))*entropyRate
48: 
49: /-- The old coefficient provider is consumed with the modified area differential. -/
50: theorem modified_clausius_coefficient (H dA G Phi : ℝ) (hg : G ≠ 0) :
51:     (H/(2*Real.pi))*(dA/(4*G*Phi)) = H*(dA/Phi)/(8*Real.pi*G) := by
52:   convert einstein_coefficient_from_clausius H (dA/Phi) G hg using 1
53:   congr 1
54:   ring
55: 
56: theorem tgl_second_friedmann_from_clausius (H : ℝ → ℝ) (t G Phi enthalpy : ℝ)
57:     (D : HubbleHorizonInput H t G Phi enthalpy) :
58:     deriv H t = -4*Real.pi*G*Phi*enthalpy := by
59:   have hh := D.H_pos.ne'
60:   have hg := D.G_pos.ne'
61:   have hp := D.Phi_pos.ne'
62:   have hc := D.clausius
63:   rw [D.enthalpy_flux, D.differential_entropy,
64:     modified_clausius_coefficient _ _ _ _ hg,
65:     (hubble_area_derivative H t D.H_diff hh).deriv] at hc
66:   dsimp [hubbleArea] at hc
67:   field_simp at hc
```

EXAMINADO_NAO_REUSAR — C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorRouteComparison.lean
SHA256 b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4; 8459 bytes. Tipo casa exatamente: False.
B4: diferenca beta*variancia; fator unico exige entalpia !=0. Nao escolhe rota nem produz EOM.
```text
91: theorem the_two_routes_differ (F : SectorFluid ι I H) (c : TGLCoupling)
92:     (t : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
93:     (F.correctedTotalRho c t+F.correctedTotalPressure c t)-
94:       entropyFactor c (F.wEff t)*F.enthalpy t = c.beta*F.sectorVariance t ∧
95:     0 ≤ c.beta*F.sectorVariance t := by
96:   have hw : |1+F.wEff t| = F.enthalpy t/F.totalRho t := by
97:     apply (eq_div_iff hr.ne').mpr
98:     nlinarith [F.effective_enthalpy t hr he]
99:   constructor
100:   · rw [F.corrected_enthalpy]
101:     unfold entropyFactor SectorFluid.sectorVariance
102:     rw [hw]
103:     ring
104:   · exact mul_nonneg c.beta_pos.le (F.sector_variance_nonneg t ht hr.ne')
105: 
106: theorem the_two_routes_equal_iff (F : SectorFluid ι I H) (c : TGLCoupling)
107:     (t : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
108:     F.correctedTotalRho c t+F.correctedTotalPressure c t =
109:       entropyFactor c (F.wEff t)*F.enthalpy t ↔
110:       ∃ commonW : ℝ, ∀ i, 0 < F.rho i t → F.w i = commonW := by
111:   rw [← F.sector_variance_zero_iff t ht hr.ne']
112:   have h := (the_two_routes_differ F c t ht hr he).1
113:   constructor
114:   · intro hz
115:     have hm : c.beta*F.sectorVariance t = 0 := by rw [hz] at h; linarith
```
```text
129: theorem the_entropy_factor_that_reproduces_the_sector_closure
130:     (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ)
131:     (he : F.enthalpy t ≠ 0) (factor : ℝ) :
132:     factor*F.enthalpy t = F.correctedTotalRho c t+F.correctedTotalPressure c t ↔
133:       factor = F.fluxFactor c t := by
134:   rw [F.corrected_enthalpy]
135:   unfold SectorFluid.fluxFactor
136:   field_simp
137: 
138: /-- The factor identity is consumed by the actual Clausius-to-Hdot theorem. -/
139: theorem sector_clausius_matches_closed_rate (F : SectorFluid ι I H)
140:     (c : TGLCoupling) (t G : ℝ) (he : F.enthalpy t ≠ 0)
```

Buscas: [{"patterns": ["ActionCouplingData", "the_same_beta_reads_four_faces", "K_boundary", "boxOperator"], "root": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel\\TGLExt", "returncode": 1, "stdout": "", "stderr": ""}]

Erros de leitura: AGENTS.md locais ausentes; acesso negado a casa Artigo; nomes tentativos FLRWMetric/TheTwoRoutesDiffer inexistentes, corrigidos pelo inventario. Sonda Python de inventario com escape literal errado falhou, repetida sem esse escape. Nenhuma falha foi contada como verificacao.
