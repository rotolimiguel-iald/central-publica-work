[OPEN — ficha anterior a qualquer alteracao de codigo]

2026-09-15T15:40:04.637899+00:00

Escopo exclusivo: b,c,d,f,g,h. a,e pagos por main; nao refazer.

Item b — ADAPTAR
{
  "decision": "ADAPTAR",
  "consumer": "SectorFluid.H_nx; F.H_nx em sector_rescaling_preserves_continuity/weighted_continuity; tgl_first_friedmann_constant_w",
  "plan": "Renomear para H_sector_nonexchange e H_singlefluid_continuity; atualizar todos os consumidores no snapshot, gerar fecho reverso por imports e recompilar cada afetado."
}

Item c — REUSAR_E_TESTAR
{
  "decision": "REUSAR_E_TESTAR",
  "consumer": "Uma sonda por cada um dos sete modulos ja consumidores de regular_dual_weight_modular_implementation.",
  "plan": "Sete pares positivo/negativo: o positivo aplica o fornecedor original e compila; mudar apenas conclusao no negativo; requer Type mismatch sem erro de ambiente/sintaxe. Reexecutar as duas historicas."
}

Item d — REUSAR
{
  "decision": "REUSAR",
  "consumer": "antiunitaryConjugateRealHom e antiunitaryConjugate_complex_cfc em V351AntiunitaryResolventPhase; localBase_polar_commutes no fornecedor V350.",
  "plan": "Remover so as duas provas duplicadas no V351; importar TGLExt.V350LocalBasePolarCommutation. Preservar nomes/tipos do fornecedor. Conferir grafo total e recompilar fecho de dependentes."
}

Item f — NOVO_COROLARIO_POR_REUSO
{
  "decision": "NOVO_COROLARIO_POR_REUSO",
  "consumer": "Resposta ao adendo001 §5.4f; proposta ext_pb_tgl_friedmann_sector_additive_kernel_proved -> ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure_additive.",
  "type": "Para U aberto/preconexo, a suave positiva, I, F:SectorFluid, c:TGLCoupling, G>0, hI e H_null do stress corrigido: existe Lambda real tal que para todo x em U, (flrwHubble a (x0))^2=(8*pi*G/3)*F.correctedTotalRho c (x0)-Lambda/3. Sem hr:rho_total>0, sem he:entalpia>=0. correctedTotalRho e soma dos setores corrigidos; continuidade setorial permanece INPUT.",
  "plan": "Modulo novo SectorFriedmannAdditive importando SectorFriedmann; consumir flrw_friedmann_from_general_metric, sector_covariant_conservation e flrw_newton_coefficient. Nenhuma nova prova de geometria."
}

Item g — MEDIR
{
  "decision": "MEDIR",
  "consumer": "Ressalva B6 aceita pela gerencia",
  "plan": "Medir bytes/fontes/.olean/.trace nas duas raizes; comparar estruturas de traces, versao/compiler/options/imports quando disponiveis; recompilar os tres em raiz propria e registrar a que binario coincide. Nao inferir causa de serializacao so da igualdade de fonte."
}

Item h — DOCUMENTAR
{
  "decision": "DOCUMENTAR",
  "consumer": "Adendo001 §5.4h, 44 modulos incorporados",
  "plan": "Consultar 35 ENTREGAS A1 da retomada e B1-B6, comentarios/fontes e tentativas. Por modulo: limite observado, escopo global/local, evidencias de timeout com hash/linha, justificativa declarada, inferencia separada e lacuna. Nao afirmar que elevar limite foi necessario sem evidencia. Nao reduzir/trocar os limites neste saneamento."
}

Limites:
- Exclusivamente raiz nova; sem alteracao A2/a/e/Atlas/memorias/canonico/tunel/originais.
- A2_012/ERRATA inicialmente procurado no nivel errado; localizado sob TETELESTAI_V351_FECHO_MATEMATICO/A2_012. a/e apenas lidos como exclusao de escopo.
- Copias de arquivos e diretorios, sem hardlinks/junctions. Cache de pacotes e objetos nao afetados podem ser copiados; os afetados e fechos serao recompilados.
- Recusa semantica de aplicacao adulterada nao e automaticamente contraexemplo de todo enunciado alternativo.
- h: 34/44 e declaracao do adendo; contagem atual sera recalculada, nao forcada.
- g: gerencia ja recompilou; esta bancada nao atribui causa nao demonstrada.
- Sem axiomas novos, sorry, native_decide, trustCompiler. Revisao autoral apenas; sem incorporacao/gate.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean
SHA256 2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3; 5398 bytes; REUSAR_ADAPTAR
b: campo e dois consumidores F.H_nx; rename H_sector_nonexchange; hipoteses conservadas.
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
```
```text
66: theorem weighted_continuity (F : SectorFluid ι I H) (weights : ι → ℝ)
67:     (t : ℝ) (ht : t∈I) :
68:     HasDerivAt (fun u => ∑ i, weights i*F.rho i u)
69:       (-3*H t*((∑ i, weights i*F.rho i t)+(∑ i, F.w i*(weights i*F.rho i t)))) t := by
70:   have hs := HasDerivAt.fun_sum (u := Finset.univ)
71:     (fun i _ => (F.H_nx i t ht).const_mul (weights i))
72:   convert! hs using 1
73:   simp only [← Finset.sum_add_distrib, Finset.mul_sum]
74:   apply Finset.sum_congr rfl
75:   intro i _
76:   ring
77: 
78: theorem total_continuity (F : SectorFluid ι I H) (t : ℝ) (ht : t∈I) :
79:     deriv F.totalRho t+3*H t*(F.totalRho t+F.totalPressure t) = 0 := by
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFriedmann.lean
SHA256 7c115dd6a8d71333d8811a6efbf7d46d4363e25d18b23f8c7e678e951c0b9dfa; 4397 bytes; REUSAR_ADAPTAR
b/f: consumidor de continuidade; fornecedor sector_covariant_conservation. Corolario novo nao usa hr/he ou multiplicative_closure.
```text
1: import TGLExt.SectorFluidClosure
2: 
3: set_option autoImplicit false
4: set_option maxHeartbeats 2400000
5: 
6: /-!
7: # The conserved sector closure reaches the existing FLRW metric (Order 012, B3)
8: 
9: The null balance is an input. Conservation is obtained from H_nx, and the
10: Einstein/Friedmann provider of B2 is actually invoked. Its integration constant
11: is retained. The zero-constant specialization has H_zero_cosmological on its face.
12: -/
13: 
14: namespace ChatgptAudit.FLRW
15: 
16: open TGLExt ChatgptAudit.GeneralMetric
17: open scoped ContDiff
18: noncomputable section
19: 
20: variable {ι : Type*} [Fintype ι]
21: 
22: theorem sector_covariant_conservation (I : Set ℝ) (a : ℝ → ℝ)
23:     (F : SectorFluid ι I (flrwHubble a)) (c : TGLCoupling)
24:     (x : Coordinate4) (ht : x 0∈I) (hz : a (x 0) ≠ 0)
25:     (ha : DifferentiableAt ℝ a (x 0)) :
26:     tensorFieldDivergence (metricInverse (flrwMetric a))
27:       (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
28:       (flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c)) x = 0 := by
29:   rw [flrw_stress_divergence a _ _ x hz ha
30:     (F.corrected_rho_deriv c (x 0) ht).differentiableAt
31:     (F.corrected_pressure_differentiable c (x 0) ht),
32:     F.corrected_continuity c (x 0) ht]
33:   ext j
34:   fin_cases j <;> rfl
35: 
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
78:     (H_zero_cosmological : cosmological = 0)
79:     (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
80:       (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x+
81:       cosmological • flrwMetric a x = (2*Real.pi/(1/(4*G))) •
82:         flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) :
83:     (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
84:       F.totalRho (x 0)*(1+c.beta*|1+F.wEff (x 0)|) := by
85:   rw [flrw_friedmann_first U hU a _ _ ha hpos x hx _ _ hE,
86:     H_zero_cosmological, flrw_newton_coefficient G hG,
87:     F.multiplicative_closure c (x 0) hr he]
88:   ring
89: 
90: end
91: end ChatgptAudit.FLRW
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean
SHA256 aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3; 6095 bytes; REUSAR_ADAPTAR
b: H_singlefluid_continuity no lugar de H_nx do fluido unico; tgl_first_friedmann_constant_w e consumidores.
```text
90: theorem tgl_first_friedmann_from_primitive (I : Set ℝ) (hI : IsOpen I)
91:     (hconn : IsPreconnected I) (H rho pressure Phi primitive : ℝ → ℝ) (G : ℝ)
92:     (hh : ∀ t∈I, DifferentiableAt ℝ H t)
93:     (hprimitive : ∀ t∈I, HasDerivAt primitive (Phi t*deriv rho t) t)
94:     (hsecond : ∀ t∈I, deriv H t = -4*Real.pi*G*Phi t*(rho t+pressure t))
95:     (hcontinuity : ∀ t∈I, deriv rho t = -3*H t*(rho t+pressure t)) :
96:     ∃ C : ℝ, ∀ t∈I, (H t)^2 = (8*Real.pi*G/3)*primitive t+C := by
97:   have hd (t : ℝ) (ht : t∈I) :
98:       HasDerivAt (fun u => (H u)^2-(8*Real.pi*G/3)*primitive u) 0 t := by
99:     convert! ((hh t ht).hasDerivAt.pow 2).sub
100:       ((hprimitive t ht).const_mul (8*Real.pi*G/3)) using 1
101:     rw [hsecond t ht, hcontinuity t ht]
102:     ring
103:   obtain ⟨C,hC⟩ := hI.exists_is_const_of_deriv_eq_zero hconn
104:     (fun t ht => (hd t ht).differentiableAt.differentiableWithinAt)
105:     (fun t ht => (hd t ht).deriv)
106:   exact ⟨C, fun t ht => by linarith [hC t ht]⟩
107: 
108: theorem tgl_first_friedmann_constant_w (I : Set ℝ) (hI : IsOpen I)
109:     (hconn : IsPreconnected I) (H rho : ℝ → ℝ) (c : TGLCoupling) (G w : ℝ)
110:     (hr : ∀ t∈I, DifferentiableAt ℝ rho t)
111:     (D : ∀ t∈I, HubbleHorizonInput H t G (entropyFactor c w) (rho t+w*rho t))
112:     (H_nx : ∀ t∈I, deriv rho t = -3*H t*(rho t+w*rho t)) :
113:     ∃ C : ℝ, ∀ t∈I,
114:       (H t)^2 = (8*Real.pi*G/3)*entropyFactor c w*rho t+C := by
115:   obtain ⟨C,hC⟩ := tgl_first_friedmann_from_primitive I hI hconn H rho
116:     (fun t => w*rho t) (fun _ => entropyFactor c w)
117:     (fun t => entropyFactor c w*rho t) G
118:     (fun t ht => (D t ht).H_diff)
119:     (fun t ht => (hr t ht).hasDerivAt.const_mul _)
120:     (fun t ht => tgl_second_friedmann_from_clausius H t G _ _ (D t ht)) H_nx
121:   refine ⟨C, fun t ht => ?_⟩
122:   simpa [mul_assoc] using hC t ht
123: 
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean
SHA256 5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8; 12687 bytes; REUSAR_ADAPTAR
f: flrw_friedmann_first e flrw_friedmann_from_general_metric, com Lambda, H_null/H_conservation; flrw_newton_coefficient com G>0.
```text
135: theorem flrw_friedmann_first (U : Set Coordinate4) (hU : IsOpen U)
136:     (a rho pressure : ℝ → ℝ) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
137:     (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
138:     (coupling cosmological : ℝ)
139:     (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
140:       (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x +
141:       cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
142:     (flrwHubble a (x 0))^2 = coupling/3*rho (x 0)-cosmological/3 := by
143:   have h00 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) hE
144:   simp [flrw_einstein_tensor U hU a ha hpos x hx, flrwMetric, flrwStress] at h00
145:   linarith
146: 
```
```text
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
219:       (hr x hx) (hp x hx) (H_conservation x hx 0)
220: 
221: /-- The Newton coefficient uses the imported area calibration; G is not derived. -/
222: theorem flrw_newton_coefficient (G : ℝ) (hG : 0 < G) :
223:     (2*Real.pi/(1/(4*G)))/3 = 8*Real.pi*G/3 := by
224:   have he := congrArg (fun q : ℝ => q⁻¹)
225:     (einstein_coefficient_from_clausius 1 1 G hG.ne')
226:   have hc : 2*Real.pi/(1/(4*G)) = 8*Real.pi*G := by
227:     simpa [one_div, div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using he
228:   exact congrArg (fun q : ℝ => q/3) hc
229: 
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryIntertwining.lean
SHA256 789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5; 4499 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351ResolventImaginaryPowers
2: import TGLExt.V350PositiveRootIntertwining
3: 
4: set_option autoImplicit false
5: set_option linter.unusedSectionVars false
6: set_option maxHeartbeats 1500000
7: 
8: namespace TGLV350.Regular
9: open Filter
10: open scoped Topology
11: noncomputable section
12: variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
13: 
14: /-- Complex continuous functions of two selfadjoint operators transport a bounded intertwiner. -/
15: theorem complex_cfc_selfadjoint_intertwines (A B R : H →L[ℂ] H)
16:     (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (h : A*R=R*B)
17:     (f : ℂ → ℂ) (hf : Continuous f) : cfc f A * R = R * cfc f B := by
18:   let s : Set ℂ := spectrum ℂ A ∪ spectrum ℂ B
19:   have hs : IsCompact s := (spectrum.isCompact A).union (spectrum.isCompact B)
20:   haveI : CompactSpace s := isCompact_iff_compactSpace.mp hs
21:   have ha : spectrum ℂ A ⊆ s := Set.subset_union_left
22:   have hb : spectrum ℂ B ⊆ s := Set.subset_union_right
23:   have he (g : C(s,ℂ)) :
24:       cfcHomSuperset hA.isStarNormal ha g * R = R * cfcHomSuperset hB.isStarNormal hb g := by
25:     induction g using ContinuousMap.induction_on_of_compact with
26:     | const r =>
27:       change cfcHomSuperset hA.isStarNormal ha (algebraMap ℂ C(s,ℂ) r) * R =
28:         R * cfcHomSuperset hB.isStarNormal hb (algebraMap ℂ C(s,ℂ) r)
29:       rw [AlgHomClass.commutes,AlgHomClass.commutes]
30:       exact Algebra.commutes r R
31:     | id => simpa only [cfcHomSuperset_id] using h
32:     | star_id =>
33:       simpa only [map_star,cfcHomSuperset_id,hA.star_eq,hB.star_eq] using h
34:     | add g k hg hk => simp only [map_add,add_mul,mul_add,hg,hk]
35:     | mul g k hg hk =>
36:       simp only [map_mul]
37:       calc
38:         _ = cfcHomSuperset hA.isStarNormal ha g * (cfcHomSuperset hA.isStarNormal ha k * R) := mul_assoc _ _ _
39:         _ = cfcHomSuperset hA.isStarNormal ha g * (R * cfcHomSuperset hB.isStarNormal hb k) := by rw [hk]
40:         _ = (cfcHomSuperset hA.isStarNormal ha g * R) * cfcHomSuperset hB.isStarNormal hb k := (mul_assoc _ _ _).symm
41:         _ = _ := by rw [hg,mul_assoc]
42:     | frequently g hg =>
43:       exact (isClosed_eq ((cfcHomSuperset_continuous hA.isStarNormal ha).mul continuous_const)
44:         (continuous_const.mul (cfcHomSuperset_continuous hB.isStarNormal hb))).mem_of_frequently_of_tendsto
45:           hg tendsto_id
46:   have hh := he ⟨fun x : s => f x,hf.comp continuous_subtype_val⟩
47:   rw [cfcHomSuperset_apply,cfcHomSuperset_apply] at hh
48:   rw [cfc_apply f A hA.isStarNormal hf.continuousOn,cfc_apply f B hB.isStarNormal hf.continuousOn]
49:   convert hh using 2 <;> congr 1
50: 
51: theorem resolventDampingOperator_intertwines (T Q R : H →L[ℂ] H)
52:     (h : T*R=R*Q) : resolventDampingOperator T * R = R * resolventDampingOperator Q := by
53:   unfold resolventDampingOperator
54:   simp only [mul_sub,sub_mul,mul_one,mul_assoc,h]
55:   rw [← mul_assoc T R Q,h,mul_assoc]
56: 
57: theorem resolventPhaseOperator_intertwines (T Q R : H →L[ℂ] H)
58:     (hT : IsSelfAdjoint T) (hQ : IsSelfAdjoint Q) (h : T*R=R*Q) (t : ℝ) :
59:     resolventPhaseOperator T t * R = R * resolventPhaseOperator Q t :=
60:   complex_cfc_selfadjoint_intertwines T Q R hT hQ h
61:     (fun z : ℂ => resolventPhaseFunction t z.re)
62:     ((resolventPhaseFunction_continuous t).comp Complex.continuous_re)
63: 
64: theorem resolventImaginaryPower_intertwines (T Q R : H →L[ℂ] H)
65:     (hT : 0 ≤ T) (h1T : T ≤ 1) (hiT : Function.Injective T)
66:     (hjT : Function.Injective (1-T : H →L[ℂ] H))
67:     (hQ : 0 ≤ Q) (h1Q : Q ≤ 1) (hiQ : Function.Injective Q)
68:     (hjQ : Function.Injective (1-Q : H →L[ℂ] H)) (h : T*R=R*Q)
69:     (t : ℝ) (x : H) :
70:     resolventImaginaryPower T hT h1T hiT hjT t (R x) =
71:       R (resolventImaginaryPower Q hQ h1Q hiQ hjQ t x) := by
72:   refine (resolventDampingOperator_denseRange Q hQ h1Q hiQ hjQ).induction ?_
73:     (isClosed_eq (by fun_prop) (by fun_prop)) x
74:   rintro _ ⟨y,rfl⟩
75:   have hb := congrArg (fun A : H →L[ℂ] H => A y) (resolventDampingOperator_intertwines T Q R h)
76:   change resolventDampingOperator T (R y)=R (resolventDampingOperator Q y) at hb
77:   rw [← hb,resolventImaginaryPower_damping,resolventImaginaryPower_damping]
78:   exact congrArg (fun A : H →L[ℂ] H => A y)
79:     (resolventPhaseOperator_intertwines T Q R (IsSelfAdjoint.of_nonneg hT)
80:       (IsSelfAdjoint.of_nonneg hQ) h t)
81: 
82: #print axioms complex_cfc_selfadjoint_intertwines
83: #print axioms resolventDampingOperator_intertwines
84: #print axioms resolventPhaseOperator_intertwines
85: #print axioms resolventImaginaryPower_intertwines
86: end
87: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScaledResolventFunctions.lean
SHA256 1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb; 3150 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351ResolventPhaseFunctions
2: import TGLExt.ModularFlowAlgebra
3: 
4: set_option autoImplicit false
5: set_option maxHeartbeats 1000000
6: 
7: namespace TGLV350.Regular
8: open ChatgptAudit
9: noncomputable section
10: 
11: def scaledResolventCoordinate (r x : ℝ) : ℝ := x/(r+(1-r)*x)
12: def scaledResolventDampingFactor (r x : ℝ) : ℝ := r/(r+(1-r)*x)^2
13: 
14: theorem scaledResolventDenominator_scalar_pos (r : ℝ) (hr : 0<r) (x : ℝ)
15:     (hx : x ∈ Set.Icc (0 : ℝ) 1) : 0<r+(1-r)*x := by
16:   by_cases h : x=1
17:   · simp [h]
18:   · have hh : 0<r*(1-x) := mul_pos hr (sub_pos.mpr (lt_of_le_of_ne hx.2 h))
19:     nlinarith [hx.1]
20: 
21: theorem scaledResolventCoordinate_complement (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
22:     1-scaledResolventCoordinate r x = r*(1-x)/(r+(1-r)*x) := by
23:   unfold scaledResolventCoordinate
24:   apply (eq_div_iff hd).mpr
25:   rw [sub_mul,one_mul,div_mul_cancel₀ _ hd]
26:   ring
27: 
28: theorem scaledResolventCoordinate_ratio (r x : ℝ) (hx : x≠0) (hd : r+(1-r)*x ≠ 0) :
29:     (1-scaledResolventCoordinate r x)/scaledResolventCoordinate r x = r*((1-x)/x) := by
30:   rw [scaledResolventCoordinate_complement r x hd]
31:   unfold scaledResolventCoordinate
32:   field_simp [hd,hx]
33:   have hd' : r+x*(1-r)≠0 := by simpa only [mul_comm] using hd
34:   exact mul_div_cancel_right₀ _ hd'
35: 
36: theorem scaledResolventCoordinate_damping (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
37:     resolventDamping (scaledResolventCoordinate r x)=
38:       resolventDamping x * scaledResolventDampingFactor r x := by
39:   unfold resolventDamping
40:   rw [scaledResolventCoordinate_complement r x hd]
41:   unfold scaledResolventCoordinate scaledResolventDampingFactor
42:   simp only [div_eq_mul_inv,← inv_pow]
43:   ring
44: 
45: theorem scaledResolventCoordinate_phase (r : ℝ) (hr : 0<r) (t x : ℝ)
46:     (hd : r+(1-r)*x ≠ 0) :
47:     resolventPhaseFunction t (scaledResolventCoordinate r x)=
48:       modularPhase t (Real.log r) * resolventPhaseFunction t x *
49:         (scaledResolventDampingFactor r x : ℂ) := by
50:   by_cases hx : x=0
51:   · subst x
52:     simp [scaledResolventCoordinate,resolventPhaseFunction,resolventDamping]
53:   by_cases h1 : x=1
54:   · subst x
55:     simp [scaledResolventCoordinate,resolventPhaseFunction,resolventDamping]
56:   have hl : Real.log ((1-scaledResolventCoordinate r x)/scaledResolventCoordinate r x)=
57:       Real.log r + Real.log ((1-x)/x) := by
58:     rw [scaledResolventCoordinate_ratio r x hx hd,
59:       Real.log_mul hr.ne' (div_ne_zero (sub_ne_zero.mpr (Ne.symm h1)) hx)]
60:   have hp : modularPhase t (Real.log r + Real.log ((1-x)/x)) =
61:       modularPhase t (Real.log r)*modularPhase t (Real.log ((1-x)/x)) := by
62:     simpa only [add_sub_cancel_right,sub_zero] using
63:       (modularPhase_cocycle t (Real.log r+Real.log ((1-x)/x)) (Real.log ((1-x)/x)) 0).symm
64:   unfold resolventPhaseFunction
65:   rw [scaledResolventCoordinate_damping r x hd,hl,hp]
66:   push_cast
67:   ring
68: 
69: #print axioms scaledResolventCoordinate
70: #print axioms scaledResolventDampingFactor
71: #print axioms scaledResolventDenominator_scalar_pos
72: #print axioms scaledResolventCoordinate_complement
73: #print axioms scaledResolventCoordinate_ratio
74: #print axioms scaledResolventCoordinate_damping
75: #print axioms scaledResolventCoordinate_phase
76: end
77: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScaledResolventCalculus.lean
SHA256 89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32; 7436 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351ScaledResolventFunctions
2: import TGLExt.V351ResolventImaginaryIntertwining
3: import TGLExt.V350ScaledPositiveResolvent
4: 
5: set_option autoImplicit false
6: set_option linter.unusedSectionVars false
7: set_option maxHeartbeats 1500000
8: 
9: namespace TGLV350.Regular
10: open ChatgptAudit
11: noncomputable section
12: variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
13: 
14: theorem positive_contraction_spectrum_bounds (T : H →L[ℂ] H)
15:     (hT : 0 ≤ T) (h1 : T ≤ 1) {x : ℝ} (hx : x ∈ spectrum ℝ T) :
16:     x ∈ Set.Icc (0 : ℝ) 1 := by
17:   refine ⟨spectrum_nonneg_of_nonneg hT hx,?_⟩
18:   exact (le_algebraMap_iff_spectrum_le (IsSelfAdjoint.of_nonneg hT)).mp
19:     (by simpa only [map_one] using h1) x hx
20: 
21: theorem scaledResolventDenominator_real_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (r : ℝ) :
22:     cfc (fun x : ℝ => r+(1-r)*x) T = scaledResolventDenominator T r := by
23:   rw [cfc_const_add r (fun x : ℝ => (1-r)*x) T (by fun_prop) hT,
24:     cfc_const_mul_id (1-r) T hT,Algebra.algebraMap_eq_smul_one]
25:   rfl
26: 
27: theorem scaledResolventCoordinate_cfc (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
28:     (r : ℝ) (hr : 0<r) :
29:     cfc (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T = scaledPositiveResolvent T r := by
30:   rw [← cfc_real_eq_complex (scaledResolventCoordinate r) (IsSelfAdjoint.of_nonneg hT)]
31:   unfold scaledResolventCoordinate scaledPositiveResolvent
32:   rw [cfc_map_div (fun x : ℝ => x) (fun x : ℝ => r+(1-r)*x) T
33:       (fun x hx => (scaledResolventDenominator_scalar_pos r hr x
34:         (positive_contraction_spectrum_bounds T hT h1 hx)).ne')
35:       (by fun_prop) (by fun_prop) (IsSelfAdjoint.of_nonneg hT),
36:     cfc_id' ℝ T (IsSelfAdjoint.of_nonneg hT),
37:     scaledResolventDenominator_real_cfc T (IsSelfAdjoint.of_nonneg hT)]
38: 
39: theorem scaledResolventCoordinate_continuousOn_spectrum (T : H →L[ℂ] H)
40:     (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
41:     ContinuousOn (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) (spectrum ℂ T) := by
42:   intro z hz
43:   have hd : r+(1-r)*z.re ≠ 0 := (scaledResolventDenominator_scalar_pos r hr z.re
44:     (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne'
45:   apply ContinuousAt.continuousWithinAt
46:   unfold scaledResolventCoordinate
47:   fun_prop
48: 
49: theorem scaledResolventDampingFactor_continuousOn_spectrum (T : H →L[ℂ] H)
50:     (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
51:     ContinuousOn (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) (spectrum ℂ T) := by
52:   intro z hz
53:   have hd : r+(1-r)*z.re ≠ 0 := (scaledResolventDenominator_scalar_pos r hr z.re
54:     (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne'
55:   apply ContinuousAt.continuousWithinAt
56:   unfold scaledResolventDampingFactor
57:   have hd2 : (r+(1-r)*z.re)^2 ≠ 0 := pow_ne_zero 2 hd
58:   fun_prop
59: 
60: /-- The invertible bounded correction to the damping under positive scaling. -/
61: def scaledResolventDampingOperator (T : H →L[ℂ] H) (r : ℝ) : H →L[ℂ] H :=
62:   cfc (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) T
63: 
64: theorem scaledResolventDampingOperator_isUnit (T : H →L[ℂ] H)
65:     (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
66:     IsUnit (scaledResolventDampingOperator T r) := by
67:   apply (isUnit_cfc_iff _ T (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr)
68:     (IsSelfAdjoint.of_nonneg hT).isStarNormal).mpr
69:   intro z hz
70:   apply Complex.ofReal_ne_zero.mpr
71:   exact div_ne_zero hr.ne' (pow_ne_zero 2 (scaledResolventDenominator_scalar_pos r hr z.re
72:     (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne')
73: 
74: theorem scaledPositiveResolvent_damping (T : H →L[ℂ] H)
75:     (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
76:     resolventDampingOperator (scaledPositiveResolvent T r) =
77:       resolventDampingOperator T * scaledResolventDampingOperator T r := by
78:   rw [← resolventDampingOperator_cfc _ (IsSelfAdjoint.of_nonneg (scaledPositiveResolvent_nonneg T hT h1 r hr))]
79:   rw [← scaledResolventCoordinate_cfc T hT h1 r hr,← cfc_comp'
80:     (fun z : ℂ => (resolventDamping z.re : ℂ))
81:     (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T
82:     (by unfold resolventDamping; fun_prop)
83:     (scaledResolventCoordinate_continuousOn_spectrum T hT h1 r hr)
84:     (IsSelfAdjoint.of_nonneg hT).isStarNormal]
85:   simp only [Complex.ofReal_re]
86:   have he : cfc (fun z : ℂ => (resolventDamping (scaledResolventCoordinate r z.re) : ℂ)) T =
87:       cfc (fun z : ℂ => (resolventDamping z.re : ℂ)*(scaledResolventDampingFactor r z.re : ℂ)) T := by
88:     apply cfc_congr
89:     intro z hz
90:     dsimp only
91:     rw [scaledResolventCoordinate_damping r z.re (scaledResolventDenominator_scalar_pos r hr z.re
92:       (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne',Complex.ofReal_mul]
93:   rw [he,cfc_mul _ _ T (by unfold resolventDamping; fun_prop)
94:     (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr),
95:     resolventDampingOperator_cfc T (IsSelfAdjoint.of_nonneg hT)]
96:   rfl
97: 
98: theorem scaledPositiveResolvent_phase (T : H →L[ℂ] H)
99:     (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) (t : ℝ) :
100:     resolventPhaseOperator (scaledPositiveResolvent T r) t =
101:       modularPhase t (Real.log r) • (resolventPhaseOperator T t * scaledResolventDampingOperator T r) := by
102:   unfold resolventPhaseOperator
103:   rw [← scaledResolventCoordinate_cfc T hT h1 r hr,← cfc_comp'
104:     (fun z : ℂ => resolventPhaseFunction t z.re)
105:     (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T
106:     (((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn)
107:     (scaledResolventCoordinate_continuousOn_spectrum T hT h1 r hr)
108:     (IsSelfAdjoint.of_nonneg hT).isStarNormal]
109:   simp only [Complex.ofReal_re]
110:   have he : cfc (fun z : ℂ => resolventPhaseFunction t (scaledResolventCoordinate r z.re)) T =
111:       cfc (fun z : ℂ => modularPhase t (Real.log r) *
112:         (resolventPhaseFunction t z.re*(scaledResolventDampingFactor r z.re : ℂ))) T := by
113:     apply cfc_congr
114:     intro z hz
115:     dsimp only
116:     rw [scaledResolventCoordinate_phase r hr t z.re (scaledResolventDenominator_scalar_pos r hr z.re
117:       (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne',mul_assoc]
118:   rw [he,cfc_const_mul _ _ T (by
119:       exact (((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn.mul
120:         (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr))),
121:     cfc_mul (fun z : ℂ => resolventPhaseFunction t z.re)
122:       (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) T
123:       (((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn)
124:       (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr)]
125:   rfl
126: 
127: #print axioms positive_contraction_spectrum_bounds
128: #print axioms scaledResolventDenominator_real_cfc
129: #print axioms scaledResolventCoordinate_cfc
130: #print axioms scaledResolventCoordinate_continuousOn_spectrum
131: #print axioms scaledResolventDampingFactor_continuousOn_spectrum
132: #print axioms scaledResolventDampingOperator
133: #print axioms scaledResolventDampingOperator_isUnit
134: #print axioms scaledPositiveResolvent_damping
135: #print axioms scaledPositiveResolvent_phase
136: end
137: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ImaginaryPowerScaling.lean
SHA256 fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69; 2870 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351ScaledResolventCalculus
2: import TGLExt.V350ScaledRootGraphTransport
3: 
4: set_option autoImplicit false
5: set_option linter.unusedSectionVars false
6: set_option maxHeartbeats 1500000
7: 
8: namespace TGLV350.Regular
9: open ChatgptAudit
10: noncomputable section
11: variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
12: 
13: theorem scaledResolventDamping_denseRange (T : H →L[ℂ] H)
14:     (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
15:     (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r) :
16:     DenseRange (resolventDampingOperator (scaledPositiveResolvent T r)) := by
17:   have hd := resolventDampingOperator_denseRange T hT h1 hi hj
18:   apply hd.mono
19:   rintro _ ⟨x,rfl⟩
20:   obtain ⟨y,hy⟩ := unit_operator_surjective (scaledResolventDampingOperator T r)
21:     (scaledResolventDampingOperator_isUnit T hT h1 r hr) x
22:   refine ⟨y,?_⟩
23:   rw [scaledPositiveResolvent_damping T hT h1 r hr]
24:   change resolventDampingOperator T (scaledResolventDampingOperator T r y)=_
25:   rw [hy]
26: 
27: /-- Scaling of the same imaginary powers, with no inverse assumed for the intertwiner. -/
28: theorem resolventImaginaryPower_scaled_intertwining (T R : H →L[ℂ] H)
29:     (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
30:     (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r)
31:     (hR : T*R=R*scaledPositiveResolvent T r) (t : ℝ) (x : H) :
32:     resolventImaginaryPower T hT h1 hi hj t (R x)=
33:       modularPhase t (Real.log r) • R (resolventImaginaryPower T hT h1 hi hj t x) := by
34:   refine (scaledResolventDamping_denseRange T hT h1 hi hj r hr).induction ?_
35:     (isClosed_eq (by fun_prop) (by fun_prop)) x
36:   rintro _ ⟨y,rfl⟩
37:   have hb := congrArg (fun A : H →L[ℂ] H => A y)
38:     (resolventDampingOperator_intertwines T (scaledPositiveResolvent T r) R hR)
39:   change resolventDampingOperator T (R y)=R (resolventDampingOperator (scaledPositiveResolvent T r) y) at hb
40:   rw [← hb,resolventImaginaryPower_damping]
41:   have hc := congrArg (fun A : H →L[ℂ] H => A y)
42:     (resolventPhaseOperator_intertwines T (scaledPositiveResolvent T r) R
43:       (IsSelfAdjoint.of_nonneg hT) (IsSelfAdjoint.of_nonneg (scaledPositiveResolvent_nonneg T hT h1 r hr)) hR t)
44:   change resolventPhaseOperator T t (R y)=R (resolventPhaseOperator (scaledPositiveResolvent T r) t y) at hc
45:   rw [hc,scaledPositiveResolvent_phase T hT h1 r hr t,
46:     scaledPositiveResolvent_damping T hT h1 r hr]
47:   change R (modularPhase t (Real.log r) • resolventPhaseOperator T t (scaledResolventDampingOperator T r y)) =
48:     modularPhase t (Real.log r) • R
49:       (resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T (scaledResolventDampingOperator T r y)))
50:   rw [map_smul,resolventImaginaryPower_damping]
51: 
52: #print axioms scaledResolventDamping_denseRange
53: #print axioms resolventImaginaryPower_scaled_intertwining
54: end
55: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarImaginaryRightTransport.lean
SHA256 5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349; 2139 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351ImaginaryPowerScaling
2: import TGLExt.V351ScalarTomitaImaginaryPowers
3: import TGLExt.V350MatrixUnitResolventScaling
4: import TGLExt.V350ScalarRegularRightPolar
5: 
6: set_option autoImplicit false
7: set_option maxHeartbeats 1500000
8: 
9: namespace TGLV350.Regular
10: open TGLExt ChatgptAudit
11: noncomputable section
12: 
13: /-- The modular frequency is transported to the actual imaginary powers of S†S. -/
14: theorem matrixUnit_imaginaryPower_right_scaling (P : SiteProfile) (N : ℕ)
15:     (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
16:     scalarTomitaImaginaryPower P t (homogeneousRightGNS (matrixUnitRightData P N i j) x)=
17:       modularPhase t (Real.log (localEigenvalue P N i j)) •
18:         homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaImaginaryPower P t x) :=
19:   resolventImaginaryPower_scaled_intertwining (scalarTomitaResolvent P)
20:     (homogeneousRightGNS (matrixUnitRightData P N i j))
21:     (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
22:     (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
23:     (localEigenvalue P N i j) (localEigenvalue_pos (P := P) N i j)
24:     (matrixUnit_resolvent_right_scaling P N i j) t x
25: 
26: /-- The right regular group commutes with these same imaginary powers. -/
27: theorem scalarTomitaImaginaryPower_regular_right_commutes (P : SiteProfile) (s t : ℝ)
28:     (x : ScalarGNSHilbert P) :
29:     scalarTomitaImaginaryPower P t (regularRightGNS P s x)=
30:       regularRightGNS P s (scalarTomitaImaginaryPower P t x) :=
31:   resolventImaginaryPower_intertwines (scalarTomitaResolvent P) (scalarTomitaResolvent P)
32:     (regularRightGNS P s)
33:     (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
34:     (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
35:     (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
36:     (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
37:     (scalarTomitaResolvent_regular_right_commutes P s).eq t x
38: 
39: #print axioms matrixUnit_imaginaryPower_right_scaling
40: #print axioms scalarTomitaImaginaryPower_regular_right_commutes
41: end
42: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AntiunitaryResolventPhase.lean
SHA256 4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8; 9504 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351ResolventImaginaryContinuity
2: import TGLExt.V350AntiunitaryPositiveConjugation
3: import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Unique
4: 
5: set_option autoImplicit false
6: set_option linter.unusedSectionVars false
7: set_option maxHeartbeats 1500000
8: 
9: namespace TGLV350.Regular
10: open ChatgptAudit ChatgptAudit.Continuous050
11: noncomputable section
12: variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
13: 
14: theorem resolventPhaseFunction_reflection (t x : ℝ) :
15:     star (resolventPhaseFunction t (1-x)) = resolventPhaseFunction t x := by
16:   have hb : resolventDamping (1-x) = resolventDamping x := by
17:     unfold resolventDamping
18:     ring
19:   have hl : Real.log ((1-(1-x))/(1-x)) = -Real.log ((1-x)/x) := by
20:     rw [sub_sub_cancel, ← inv_div, Real.log_inv]
21:   rw [resolventPhaseFunction_star]
22:   unfold resolventPhaseFunction modularPhase
23:   rw [hb, hl]
24:   congr 2
25:   push_cast
26:   ring
27: 
28: theorem antiunitaryConjugate_star (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T : H →L[ℂ] H) :
29:     antiunitaryConjugate J (star T) = star (antiunitaryConjugate J T) := by
30:   change antiunitaryConjugate J T.adjoint = (antiunitaryConjugate J T).adjoint
31:   apply (ContinuousLinearMap.eq_adjoint_iff _ _).mpr
32:   intro x y
33:   calc
34:     inner ℂ (antiunitaryConjugate J T.adjoint x) y =
35:         star (inner ℂ (T.adjoint (J.symm x)) (J.symm y)) := by
36:       simpa only [antiunitaryConjugate_apply, J.apply_symm_apply] using
37:         antiunitary_inner_conj J (T.adjoint (J.symm x)) (J.symm y)
38:     _ = star (inner ℂ (J.symm x) (T (J.symm y))) :=
39:       congrArg star (T.adjoint_inner_left (J.symm y) (J.symm x))
40:     _ = inner ℂ x (antiunitaryConjugate J T y) := by
41:       simpa only [antiunitaryConjugate_apply, J.apply_symm_apply] using
42:         (antiunitary_inner_conj J (J.symm x) (T (J.symm y))).symm
43: 
44: theorem antiunitaryConjugate_add (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T V : H →L[ℂ] H) :
45:     antiunitaryConjugate J (T+V) = antiunitaryConjugate J T + antiunitaryConjugate J V := by
46:   ext x
47:   simp only [antiunitaryConjugate_apply, add_apply, map_add]
48: 
49: theorem antiunitaryConjugate_smul (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
50:     (c : ℂ) (T : H →L[ℂ] H) :
51:     antiunitaryConjugate J (c • T) = star c • antiunitaryConjugate J T := by
52:   ext x
53:   simp only [antiunitaryConjugate_apply, smul_apply, map_smulₛₗ,
54:     starRingEnd_apply]
55: 
56: /-- Antiunitary conjugation is a real, not complex, star algebra homomorphism. -/
57: def antiunitaryConjugateRealHom (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
58:     (H →L[ℂ] H) →⋆ₐ[ℝ] (H →L[ℂ] H) where
59:   toFun := antiunitaryConjugate J
60:   map_one' := by ext x; simp [antiunitaryConjugate_apply]
61:   map_mul' := antiunitaryConjugate_mul J
62:   map_zero' := by ext x; simp [antiunitaryConjugate_apply]
63:   map_add' := antiunitaryConjugate_add J
64:   commutes' := by
65:     intro r
66:     ext x
67:     simp [antiunitaryConjugate_apply, Algebra.algebraMap_eq_smul_one]
68:     calc
69:       J (r • J.symm x) = J ((r : ℂ) • J.symm x) :=
70:         congrArg J (RCLike.real_smul_eq_coe_smul (K := ℂ) r (J.symm x))
71:       _ = (r : ℂ) • x := by
72:         rw [map_smulₛₗ]
73:         rw [J.apply_symm_apply]
74:         exact congrArg (fun c : ℂ => c • x) (Complex.conj_ofReal r)
75:       _ = r • x := (RCLike.real_smul_eq_coe_smul (K := ℂ) r x).symm
76:   map_star' := antiunitaryConjugate_star J
77: 
78: theorem antiunitaryConjugate_continuous (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
79:     Continuous (antiunitaryConjugate J) := by
80:   have hc : Continuous (fun T : H →L[ℂ] H =>
81:       T.comp J.symm.toLinearIsometry.toContinuousLinearMap) :=
82:     continuous_id.clm_comp_const J.symm.toLinearIsometry.toContinuousLinearMap
83:   exact hc.const_clm_comp J.toLinearIsometry.toContinuousLinearMap
84: 
85: theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
86:     (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T) :=
87:   (antiunitaryConjugate_star J T).symm.trans (congrArg (antiunitaryConjugate J) hT.star_eq)
88: 
89: theorem antiunitaryConjugate_real_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
90:     (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℝ) (hf : Continuous f) :
91:     antiunitaryConjugate J (cfc f T) = cfc f (antiunitaryConjugate J T) :=
92:   (antiunitaryConjugateRealHom J).map_cfc f T hf.continuousOn
93:     (antiunitaryConjugate_continuous J) hT (antiunitaryConjugate_selfadjoint J T hT)
94: 
95: theorem complex_cfc_real_imaginary (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
96:     (f : ℝ → ℂ) (hf : Continuous f) :
97:     cfc (fun z : ℂ => f z.re) T =
98:       cfc (fun x : ℝ => (f x).re) T + Complex.I • cfc (fun x : ℝ => (f x).im) T := by
99:   have hr : Continuous (fun z : ℂ => (((f z.re).re : ℝ) : ℂ)) := by fun_prop
100:   have hi : Continuous (fun z : ℂ => (((f z.re).im : ℝ) : ℂ)) := by fun_prop
101:   calc
102:     _ = cfc (fun z : ℂ => (((f z.re).re : ℝ) : ℂ) + Complex.I * (((f z.re).im : ℝ) : ℂ)) T :=
103:       cfc_congr fun z _ => by simpa only [mul_comm] using (Complex.re_add_im (f z.re)).symm
104:     _ = cfc (fun z : ℂ => (((f z.re).re : ℝ) : ℂ)) T +
105:         Complex.I • cfc (fun z : ℂ => (((f z.re).im : ℝ) : ℂ)) T := by
106:       rw [cfc_add _ _ _ hr.continuousOn (by fun_prop), cfc_const_mul _ _ _ hi.continuousOn]
107:     _ = _ := by
108:       rw [← cfc_real_eq_complex (fun x : ℝ => (f x).re) hT,
109:         ← cfc_real_eq_complex (fun x : ℝ => (f x).im) hT]
110: 
111: theorem antiunitaryConjugate_complex_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
112:     (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℂ) (hf : Continuous f) :
113:     antiunitaryConjugate J (cfc (fun z : ℂ => f z.re) T) =
114:       cfc (fun z : ℂ => star (f z.re)) (antiunitaryConjugate J T) := by
115:   rw [complex_cfc_real_imaginary T hT f hf, antiunitaryConjugate_add,
116:     antiunitaryConjugate_smul,
117:     antiunitaryConjugate_real_cfc J T hT (fun x : ℝ => (f x).re) (Complex.continuous_re.comp hf),
118:     antiunitaryConjugate_real_cfc J T hT (fun x : ℝ => (f x).im) (Complex.continuous_im.comp hf)]
119:   rw [complex_cfc_real_imaginary _ (antiunitaryConjugate_selfadjoint J T hT)
120:     (fun x => star (f x)) hf.star]
121:   simp only [Complex.star_def, Complex.conj_re, Complex.conj_im, cfc_neg,
122:     Complex.conj_I, neg_smul, smul_neg]
123: 
124: theorem antiunitaryConjugate_resolventPhase (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
125:     (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
126:     (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) :
127:     antiunitaryConjugate J (resolventPhaseOperator T t) = resolventPhaseOperator T t := by
128:   unfold resolventPhaseOperator
129:   rw [antiunitaryConjugate_complex_cfc J T hT _ (resolventPhaseFunction_continuous t), hflip]
130:   have hc : Continuous (fun z : ℂ => star (resolventPhaseFunction t z.re)) :=
131:     ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).star
132:   have he := cfc_comp' (fun z : ℂ => star (resolventPhaseFunction t z.re))
133:     (fun z : ℂ => 1-z) T hc.continuousOn (by fun_prop) hT.isStarNormal
134:   have hg : cfc (fun z : ℂ => 1-z) T = 1-T := by
135:     rw [cfc_sub _ _ _ (by fun_prop) (by fun_prop),
136:       cfc_const (1 : ℂ) T hT.isStarNormal, cfc_id' ℂ T hT.isStarNormal, map_one]
137:   rw [hg] at he
138:   rw [← he]
139:   apply cfc_congr
140:   intro z _
141:   simpa only [Complex.sub_re, Complex.one_re] using resolventPhaseFunction_reflection t z.re
142: 
143: theorem antiunitaryConjugate_resolventDamping (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
144:     (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
145:     (hflip : antiunitaryConjugate J T = 1-T) :
146:     antiunitaryConjugate J (resolventDampingOperator T) = resolventDampingOperator T := by
147:   rw [← resolventPhaseOperator_zero T hT]
148:   exact antiunitaryConjugate_resolventPhase J T hT hflip 0
149: 
150: theorem resolventImaginaryPower_antiunitary (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
151:     (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
152:     (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))
153:     (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) (x : H) :
154:     J (resolventImaginaryPower T hT h1 hi hj t x) =
155:       resolventImaginaryPower T hT h1 hi hj t (J x) := by
156:   have hB (y : H) : J (resolventDampingOperator T y) = resolventDampingOperator T (J y) := by
157:     have h := congrArg (fun A : H →L[ℂ] H => A (J y))
158:       (antiunitaryConjugate_resolventDamping J T (IsSelfAdjoint.of_nonneg hT) hflip)
159:     simpa only [antiunitaryConjugate_apply, J.symm_apply_apply] using h
160:   have hC (y : H) : J (resolventPhaseOperator T t y) = resolventPhaseOperator T t (J y) := by
161:     have h := congrArg (fun A : H →L[ℂ] H => A (J y))
162:       (antiunitaryConjugate_resolventPhase J T (IsSelfAdjoint.of_nonneg hT) hflip t)
163:     simpa only [antiunitaryConjugate_apply, J.symm_apply_apply] using h
164:   refine (resolventDampingOperator_denseRange T hT h1 hi hj).induction ?_
165:     (isClosed_eq (by fun_prop) (by fun_prop)) x
166:   rintro _ ⟨y,rfl⟩
167:   rw [resolventImaginaryPower_damping, hB, resolventImaginaryPower_damping]
168:   exact hC y
169: 
170: #print axioms resolventPhaseFunction_reflection
171: #print axioms antiunitaryConjugate_star
172: #print axioms antiunitaryConjugate_add
173: #print axioms antiunitaryConjugate_smul
174: #print axioms antiunitaryConjugateRealHom
175: #print axioms antiunitaryConjugate_continuous
176: #print axioms antiunitaryConjugate_selfadjoint
177: #print axioms antiunitaryConjugate_real_cfc
178: #print axioms complex_cfc_real_imaginary
179: #print axioms antiunitaryConjugate_complex_cfc
180: #print axioms antiunitaryConjugate_resolventPhase
181: #print axioms antiunitaryConjugate_resolventDamping
182: #print axioms resolventImaginaryPower_antiunitary
183: end
184: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarTomitaImaginaryConjugation.lean
SHA256 981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d; 2000 bytes; REUSAR
c: sonda individual por modulo, comparando enunciado valido com adulteracao de coeficiente/sinal/lado. d somente no modulo duplicador, removendo add/smul e importando fornecedor existente.
```text
1: import TGLExt.V351AntiunitaryResolventPhase
2: import TGLExt.V351ScalarTomitaImaginaryPowers
3: import TGLExt.V350ScalarTomitaPolarInvolution
4: 
5: set_option autoImplicit false
6: set_option maxHeartbeats 1500000
7: 
8: namespace TGLV350.Regular
9: open TGLExt
10: noncomputable section
11: 
12: /-- The original polar antiunitary commutes with the original resolvent phase group.
13: This is not yet identification of the modular action with regular conjugation. -/
14: theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
15:     (x : ScalarGNSHilbert P) :
16:     scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
17:       scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x) :=
18:   resolventImaginaryPower_antiunitary (scalarTomitaPolarFactor P)
19:     (scalarTomitaResolvent P) (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
20:     (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
21:     (scalarTomitaPolar_conjugate_resolvent P) t x
22: 
23: theorem scalarTomitaImaginaryPower_polar_conjugate (P : SiteProfile) (t : ℝ)
24:     (x : ScalarGNSHilbert P) :
25:     scalarTomitaPolarFactor P
26:       (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
27:         scalarTomitaImaginaryPower P t x := by
28:   rw [scalarTomitaImaginaryPower_polar_commutes, LinearIsometryEquiv.apply_symm_apply]
29: 
30: /-- Equality of bounded complex-linear operators, not just a formal pairing. -/
31: theorem scalarTomitaImaginaryPower_polar_operator (P : SiteProfile) (t : ℝ) :
32:     antiunitaryConjugate (scalarTomitaPolarFactor P)
33:       (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap =
34:         (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap := by
35:   apply ContinuousLinearMap.ext
36:   intro x
37:   exact scalarTomitaImaginaryPower_polar_conjugate P t x
38: 
39: #print axioms scalarTomitaImaginaryPower_polar_commutes
40: #print axioms scalarTomitaImaginaryPower_polar_conjugate
41: #print axioms scalarTomitaImaginaryPower_polar_operator
42: end
43: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LocalBasePolarCommutation.lean
SHA256 6a81d480bf6997282bdd5734b99e8d50ac17e532ad390ae108866130b94046a4; 3903 bytes; REUSAR
d: fornecedor unico dos dois lemas com nomes completos TGLV350.Regular.antiunitaryConjugate_add e _smul.
```text
1: import TGLExt.V350MatrixUnitPolarCommutation
2: import TGLExt.ChainPrefix
3: import Mathlib.Data.Matrix.Basis
4: 
5: set_option autoImplicit false
6: set_option linter.unusedSectionVars false
7: set_option maxHeartbeats 1500000
8: 
9: namespace TGLV350.Regular
10: open TGLExt ChatgptAudit
11: noncomputable section
12: 
13: theorem antiunitaryConjugate_add {H : Type} [NormedAddCommGroup H]
14:     [InnerProductSpace ℂ H] [CompleteSpace H] (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
15:     (T V : H →L[ℂ] H) :
16:     antiunitaryConjugate U (T+V) = antiunitaryConjugate U T + antiunitaryConjugate U V := by
17:   ext x
18:   change U (T (U.symm x) + V (U.symm x)) = U (T (U.symm x)) + U (V (U.symm x))
19:   exact map_add U _ _
20: 
21: theorem antiunitaryConjugate_smul {H : Type} [NormedAddCommGroup H]
22:     [InnerProductSpace ℂ H] [CompleteSpace H] (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
23:     (c : ℂ) (T : H →L[ℂ] H) :
24:     antiunitaryConjugate U (c • T) = star c • antiunitaryConjugate U T := by
25:   ext x
26:   change U (c • T (U.symm x)) = star c • U (T (U.symm x))
27:   exact map_smulₛₗ U c _
28: 
29: def localBaseCore (P : SiteProfile) (N : ℕ) :
30:     Matrix (chainIdx N) (chainIdx N) ℂ →ₗ[ℂ] (regularCoreAlgebra P).toStarSubalgebra where
31:   toFun a := regularCoreEmbedding P ⟨towerPi P a,towerPi_mem_factor a⟩
32:   map_add' a b := by
33:     apply Subtype.ext
34:     change fibre (towerPi P (a+b)) = fibre (towerPi P a) + fibre (towerPi P b)
35:     rw [towerPi_add,fibre_add]
36:   map_smul' c a := by
37:     apply Subtype.ext
38:     change fibre (towerPi P (c • a)) = c • fibre (towerPi P a)
39:     rw [towerPi_smul,fibre_smul]
40: 
41: theorem matrix_linear_polar_commutes {H : Type} [NormedAddCommGroup H]
42:     [InnerProductSpace ℂ H] [CompleteSpace H] {m n : Type*}
43:     [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
44:     (U : H ≃ₛₗᵢ[starRingEnd ℂ] H) (F : Matrix m n ℂ →ₗ[ℂ] (H →L[ℂ] H))
45:     (B : H →L[ℂ] H)
46:     (hunit : ∀ i j, Commute (antiunitaryConjugate U (F (Matrix.single i j 1))) B)
47:     (a : Matrix m n ℂ) : Commute (antiunitaryConjugate U (F a)) B := by
48:   induction a using Matrix.induction_on' with
49:   | h_zero =>
50:       rw [map_zero]
51:       apply ContinuousLinearMap.ext
52:       intro z
53:       simp [antiunitaryConjugate_apply]
54:   | h_add a b ha hb =>
55:       rw [map_add,antiunitaryConjugate_add]
56:       exact ha.add_left hb
57:   | h_std_basis i j c =>
58:       have he : Matrix.single i j c = c • Matrix.single i j (1 : ℂ) := by
59:         simp only [Matrix.smul_single,smul_eq_mul,mul_one]
60:       have hF : F (Matrix.single i j c) = c • F (Matrix.single i j 1) := by
61:         rw [he]
62:         exact F.map_smul c _
63:       rw [hF,antiunitaryConjugate_smul U c]
64:       have hh := hunit i j
65:       apply ContinuousLinearMap.ext
66:       intro z
67:       have hv := congrArg (fun T : H →L[ℂ] H => T z) hh.eq
68:       change star c • (antiunitaryConjugate U (F (Matrix.single i j 1))) (B z) =
69:         B (star c • (antiunitaryConjugate U (F (Matrix.single i j 1))) z)
70:       rw [map_smul]
71:       exact congrArg (fun v : H => star c • v) hv
72: 
73: /-- The same polar conjugation now commutes with all represented elements
74: for every matrix at every finite level, including arbitrary complex coefficients. -/
75: theorem localBase_polar_commutes (P : SiteProfile) (N : ℕ)
76:     (a : Matrix (chainIdx N) (chainIdx N) ℂ) (B : (regularCoreAlgebra P).toStarSubalgebra) :
77:     Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
78:       (scalarGNSRepresentation P (localBaseCore P N a))) (scalarGNSRepresentation P B) :=
79:   matrix_linear_polar_commutes (scalarTomitaPolarFactor P)
80:     ((scalarGNSRepresentation P).toLinearMap.comp (localBaseCore P N))
81:     (scalarGNSRepresentation P B) (fun i j => matrixUnit_polar_generator_commutes P N i j B) a
82: 
83: #print axioms antiunitaryConjugate_add
84: #print axioms antiunitaryConjugate_smul
85: #print axioms localBaseCore
86: #print axioms matrix_linear_polar_commutes
87: #print axioms localBase_polar_commutes
88: end
89: end TGLV350.Regular
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\probes\BadAntiunitaryPhase.lean
SHA256 5fa9db02bcb2466098ac32d48986a0f3754af1527a7fe7b59a87508a1fd698da; 216 bytes; REUSAR
c: sonda real historica, a ser reexecutada; nao contar falha de sintaxe/ambiente.
```text
1: import TGLExt.V351AntiunitaryResolventPhase
2: 
3: open TGLV350.Regular
4: 
5: example (t x : ℝ) :
6:     star (resolventPhaseFunction t (1-x)) = 2 * resolventPhaseFunction t x := by
7:   exact resolventPhaseFunction_reflection t x
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\probes\BadImaginaryScaling.lean
SHA256 0ece33df00d8322025921d33760be246fa2478e636129426af7df04c928164c5; 641 bytes; REUSAR
c: sonda real historica, a ser reexecutada; nao contar falha de sintaxe/ambiente.
```text
1: import TGLExt.V351ImaginaryPowerScaling
2: set_option maxHeartbeats 1500000
3: 
4: open TGLV350.Regular ChatgptAudit
5: 
6: example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
7:     (T R : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
8:     (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r)
9:     (hR : T*R=R*scaledPositiveResolvent T r) (t : ℝ) (x : H) :
10:     resolventImaginaryPower T hT h1 hi hj t (R x)=
11:       modularPhase (-t) (Real.log r) • R (resolventImaginaryPower T hT h1 hi hj t x) := by
12:   exact resolventImaginaryPower_scaled_intertwining T R hT h1 hi hj r hr hR t x
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\audit_orphans\20260914_183919_829315\BadAntiunitaryPhase.stdout.txt
SHA256 e2701738b3dc9093c333e296eb5f4b7ff4f6ea060d1b7fd1b31f31f5ad2cbc51; 368 bytes; EVIDENCIA_HISTORICA
Duas sondas anteriormente executadas, nao sete.
```text
1: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\probes\BadAntiunitaryPhase.lean:7:2: error: Type mismatch
2:   resolventPhaseFunction_reflection t x
3: has type
4:   star (resolventPhaseFunction t (1 - x)) = resolventPhaseFunction t x
5: but is expected to have type
6:   star (resolventPhaseFunction t (1 - x)) = 2 * resolventPhaseFunction t x
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\audit_orphans\20260914_183919_829315\BadImaginaryScaling.stdout.txt
SHA256 d413e667ad92cbb1fae73c15007ef748a52379a2bfd7b93046d9ed99e9304cf2; 532 bytes; EVIDENCIA_HISTORICA
Duas sondas anteriormente executadas, nao sete.
```text
1: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\probes\BadImaginaryScaling.lean:12:2: error: Type mismatch
2:   resolventImaginaryPower_scaled_intertwining T R hT h1 hi hj r hr hR t x
3: has type
4:   (resolventImaginaryPower T hT h1 hi hj t) (R x) =
5:     modularPhase t (Real.log r) • R ((resolventImaginaryPower T hT h1 hi hj t) x)
6: but is expected to have type
7:   (resolventImaginaryPower T hT h1 hi hj t) (R x) =
8:     modularPhase (-t) (Real.log r) • R ((resolventImaginaryPower T hT h1 hi hj t) x)
```

Contagem preliminar de h: {"modules": 44, "with_explicit_maxHeartbeats": 39, "adendo_declared": 34}

G: inventario inicial lido em FICHA_SANEAMENTO.json.
