[REAL — B3 pago no escopo condicional declarado: conservação setorial ligada a B2. O caso sem Λ exige H_zero_cosmological. Incorporação pela gerência.]

# ENTREGA 012 / B3 — de H_nx à primeira equação de Friedmann

2026-09-14T17:03:46.660603-03:00

**14 teoremas, sete definições e a estrutura SectorFluid**, compilados e revistos independentemente. A conservação exigida pela camada Einstein é demonstrada a partir da não-troca setorial; o consumidor não a assume novamente. A conclusão geral conserva a constante cosmológica de B2.

## Critérios da ordem

| Critério B3 | Resultado |
|---|---|
| Ficha anterior ao código, seis buscas e fornecedores por tipo | PAGO; MD/JSON anexos, 14 locadores conferidos na revisão. Erros iniciais de acesso foram repetidos e registrados. |
| Setores finitos, rho_i≥0, w_i constante | PAGO; `SectorFluid`, w sem argumento temporal. |
| Não-troca nomeada | PAGO; campo `H_nx : HasDerivAt rho_i (-3H(1+w_i)rho_i)`. É INPUT, não conclusão microscópica. |
| Reescalonamento conserva a mesma continuidade | PAGO; `sector_rescaling_preserves_continuity`, depois `weighted_continuity`/`corrected_continuity`. |
| Soma corrigida e cancelamento do vácuo | PAGO; `corrected_closure`; o corolário de três setores invoca `closure_identity` e `hubble_form` existentes. |
| Mesmo beta de B1 | PAGO; `c : TGLCoupling`, uma única projeção c.beta em todos os fatores. |
| w_eff definido e leitura absoluta | PAGO; wEff=pTot/rhoTot; `effective_enthalpy` exige rhoTot>0 e enthalpy≥0. |
| Equação 00 sob B2 | PAGO com Λ existencial; `tgl_friedmann_from_sector_closure` aplica B2 e descarrega sua conservação. |
| Forma sem termo cosmológico | PAGO **condicionalmente** em `tgl_friedmann_zero_cosmological`; H_zero_cosmological é explícita. Não foi provado Λ=0. |
| Axiomas e reprodução isolada | PAGO; 22 alvos no trio, Lake autoral e Lake independente, sem objetos de projeto autorais copiados. |
| Revisão e negativos | PAGO no escopo DEV B3; P0/P1/P2=0/0/0; duas adulterações recusadas por Type mismatch. |

## Cadeia efetivamente consumida

```text
c:TGLCoupling (B1)
rhoT_i=(1+c.beta*(1+w_i))*rho_i
H_nx -> continuidade de rhoT_i -> continuidade do total corrigido
 -> sector_covariant_conservation (divergência da métrica B2)
 -> flrw_friedmann_from_general_metric (H_null permanece INPUT)
 -> existe Λ constante em U:
    H²=(8πG/3)*rhoTot*(1+c.beta*abs(1+wEff))-Λ/3
    H'=-4πG*(correctedTotalRho+correctedTotalPressure)
```

A identidade aditiva `rhoTtot=rhoTot+beta*enthalpy` vale sem sinal de entalpia. A reescrita absoluta requer rhoTot>0 e enthalpy≥0. Não se afirma positividade de cada densidade corrigida para w_i arbitrário; isso exigiria uma hipótese sobre seu fator. O suporte de densidades pode conter setores phantom nesta construção algébrica, desde que as hipóteses particulares de cada conclusão sejam satisfeitas.

U é aberto preconexo, a é suave/positiva nas coordenadas temporais de U, e esses tempos pertencem ao domínio I de H_nx. **H_null é o balanço nulo para o stress corrigido concreto**, não um teorema de realização física. G>0 e eta=1/(4G) continuam calibração INPUT. Não se divide por H. Não se declara existência de solução física não vazia. A convenção de B2 `G_tensor+Λg=κT` explica o sinal −Λ/3.

O corolário zero recebe a equação tensorial hE e H_zero_cosmological, não a própria conclusão escalar H². O resultado não autoriza eliminar a constante existencial em outro consumidor. A distinção entre rota total e setorial na segunda equação fica para B4; B3 não a resolve por escolha.

## Reprodução e alcance da revisão

Na bancada `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA`:

```powershell
& 'C:\Python314\python.exe' -X utf8 -B '.\run_b3_lake.py' TGLExt.SectorFriedmann TGLExt.AuditSector
```

Run aceito `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_164047_491748\run.json`: rc0; snapshots finais conferidos. Auditoria em AUDITORIA_B3. Duas sondas em probes_B3 devem falhar sob `lake env lean`: BadSectorClosure troca +beta por −beta; BadSectorAbs troca a entalpia pelo negativo. Ambas efetivamente deram Type mismatch com imports funcionais.

A revisão independente executou `lake build TGLExt.TheSameBetaReadsThreeFaces TGLExt.SectorFluidClosure TGLExt.SectorFriedmann TGLExt.AuditSector TGLExt.ReviewSector` em s, rc0. Acrescentou 17 fornecedores B1 ainda ausentes e os quatro arquivos B3/auditor: 21 objetos novos, mantendo os 92 objetos próprios de B2 idênticos (113 no total). Nenhum olean autoral foi copiado. Os três objetos do candidato coincidem byte a byte. Mathlib/toolchain e oito outros pacotes são caches herdados, pinados; não se reivindica reconstrução independente desses componentes.

O revisor leu as sondas autorais e seus streams, mas não as reexecutou. A preservação de 941 fontes-base e um.py foi medida pelo auditor autoral, sem revarredura integral pelo revisor. Não houve aviso novo; dois avisos herdados de fornecedores B1 ficaram nos logs.

## Falhas preservadas

Tentativas autorais intermediárias falharam por instâncias de derivadas, simplificação de somas, namespace da inversa, limite de heartbeats e igualdade do vetor nulo. Os snapshots/logs permanecem. A criação inicial do runner falhou na citação de string do comando Python, antes de criar arquivo; foi refeita com entrada literal. Na revisão, a primeira geração do parecer usou `lambda` como nome de argumento Python e falhou antes de gravar o parecer; histórico preservado, sem efeito no build Lean. Nenhuma falha foi promovida a prova negativa.

## Axiomas medidos

| Alvo completo | Axiomas |
|---|---|
| `ChatgptAudit.FLRW.SectorFluid` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.totalRho` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.totalPressure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.enthalpy` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.wEff` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.correctedRho` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.correctedTotalRho` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.correctedTotalPressure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.enthalpy_eq` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.sector_rescaling_preserves_continuity` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.corrected_closure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.weighted_continuity` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.total_continuity` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.corrected_rho_deriv` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.corrected_pressure_differentiable` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.corrected_continuity` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.effective_enthalpy` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.multiplicative_closure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.three_sector_closure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.sector_covariant_conservation` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.tgl_friedmann_zero_cosmological` | propext, Classical.choice, Quot.sound |

## Arquivos principais

| Arquivo | SHA256 lido |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean` | `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFriedmann.lean` | `7c115dd6a8d71333d8811a6efbf7d46d4363e25d18b23f8c7e678e951c0b9dfa` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AuditSector.lean` | `4aa3174a76989847aed15152d1b7bf84e0b7808b7d6ab50728876bf3b17ddb65` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B3.md` | `82afc5993dc7e071318722e3a68120f19dd703445503e17a2fb6f70d36929988` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B3.json` | `ec48b145eb0f6504aa6da2e7cc7d1d142e58500dcaf5cecac3b929cd7c5e81e9` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\AUDITORIA_B3.json` | `8b35c067b9e2e1e38fdd8bd16af93d7efe103efd1fea6e2fbdfe13ba01a7918a` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\ALVOS_B3.json` | `28c7d5f0c94030164c3b72b49395be854bcd8aaf11b2d886a36b96f1c543a502` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\BUSCAS_B3_GRUPOS.json` | `f7fb3a713b3d1f904d4cb2289ae3d1b7378ff9bf485d8cdb5105422d4f5b0111` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b3\REVIEW_B3_FINAL.md` | `8ee5f96809d9fe93fb36ccee6998d1b68748a3c3d07f73bd98eca6443098a366` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b3\REVIEW_B3_FINAL.json` | `df0a2465e4821cd650d2cd783bc22b865ffd9091ccdd8632a576824bfb875ef7` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b3\compilation.json` | `588747431fef8fc6b0813956c2a50c0400e7df9bb76a816986115902f11daf9c` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\run_b3_lake.py` | `037aa4acef2d6dc5fa8000674e5eb351ab796e69182b51b8238d78cfe155d8a3` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\audit_b3.py` | `4a28babb5e6c7afe87dea729b3592ab9aaefc8bc705745238f1e6f6bf7b1d2e3` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b3_audit.py` | `17a6234adcb07aa010ce434afbd22a6525b106c8e07a63727da105e0144e9882` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\deliver_b3.py` | `5211eaea1d13c752e7755cfb42f7a4c2f675dfa6dea4e1d8d4ce322abed729d7` |

MANIFESTO_B3/RECIBO_B3 na bancada indexam entrega, fontes, objetos, runs, revisão e sondas. Consumidores propostos: ext_tgl_friedmann_from_sector_closure_kernel_proved, ext_sector_rescaling_preserves_continuity_kernel_proved e ext_sector_effective_equation_of_state_kernel_proved. Instalação no um.py e auditoria de integração são da gerência. D1, gate, originais, memórias, TGL-S/TGL-L e Lema3 global não foram alterados.

## Ficha integral preservada

[OPEN — ficha anterior ao código B3]

# B3 — conservação setorial e a equação 00

NOVO: tipagem SectorFluid e ponte entre conservação escalar setorial e FLRW já provado em B2. REUSAR soma/derivada Mathlib, TGLCoupling B1, toda geometria B2 e identidades de RhoPlusPClosure. Não refazer a camada Einstein.

## Tipo exato e hipóteses
```text
SectorFluid (iota : Type) [Fintype iota] (I : Set Real) (H : Real -> Real):
 rho : iota -> Real -> Real; w : iota -> Real (constant in time);
 rho_nonneg : forall i t in I, 0 <= rho i t;
 H_nx : forall i t in I, HasDerivAt (rho i) (-3*H t*(1+w i)*rho i t) t.
c : TGLExt.TGLCoupling from B1, with the same c.beta in every factor.
rhoT_i=(1+c.beta*(1+w_i))*rho_i; pT_i=w_i*rhoT_i.
The rescaled HasDerivAt equation follows from H_nx by constant multiplication.
rhoTot=sum rho_i; pTot=sum w_i*rho_i; enthalpy=sum(rho_i+w_i*rho_i).
rhoTtot=rhoTot+c.beta*enthalpy, and corrected total continuity holds.
wEff(t)=pTot(t)/rhoTot(t).
For rhoTot(t)>0 and enthalpy(t)>=0: rhoTot(t)*abs(1+wEff(t))=enthalpy(t).
Apply B2 to the actual FLRW stress of rhoTtot,pTtot on open preconnected U,
with smooth positive a, time coordinates in I, H=flrwHubble a and explicit H_null.
Conservation is proved from H_nx, not assumed separately.
At eta=1/(4*G), G>0, B2 yields exists Lambda and
 H^2=(8*pi*G/3)*rhoTot*(1+c.beta*abs(1+wEff))-Lambda/3.
The zero-constant specialization must have a named H_zero_cosmological:
 general Einstein equation with its Lambda and explicit Lambda=0.
No step silently discards the integration constant; no hypothesis is the desired Friedmann equation.
Three-sector corollary applies the existing closure_identity and hubble_form.
```

## Consumidores existentes
```json
[
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 4571,
    "text": "def prove_rho_plus_p_closure(ONE, parts):",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 133716,
    "text": "\"ext_rp_hubble_form_kernel_proved\": \"TGLExt.hubble_form\",",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 180955,
    "text": "def prove_d1_camb_protocol(ONE):",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 180969,
    "text": "\"hypothesis\": {\"background\": \"H^2 = (8 pi G/3) rho_tot [1 + beta |1 + w_eff(z)|]\", \"beta_theory\": \"alpha sqrt(e) em runtime\", \"approximation_DECLARED\": \"CAMB em LCDM; TGL analitica por cima; r_s deslocado por H_LCDM/H_TGL em z_* (nao --tight-rs)\"},",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  }
]
```

Propostos: ext_tgl_friedmann_from_sector_closure_kernel_proved, ext_sector_rescaling_preserves_continuity_kernel_proved, ext_sector_effective_equation_of_state_kernel_proved

## Fornecedores

### lambda_drops_out
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\RhoPlusPClosure.lean:47 · SHA256 `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6`
```lean
theorem lambda_drops_out (ρΛ : ℝ) : ρΛ + (-ρΛ) = 0
```
REUSAR diretamente

### closure_identity
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\RhoPlusPClosure.lean:52 · SHA256 `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6`
```lean
theorem closure_identity (β ρr ρm ρΛ : ℝ) :
    β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
      = β * ((4 / 3) * ρr + ρm)
```
REUSAR diretamente

### hubble_form
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\RhoPlusPClosure.lean:58 · SHA256 `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6`
```lean
theorem hubble_form (β ρr ρm ρΛ : ℝ) :
    (ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
      = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ
```
REUSAR diretamente

### TGLCoupling
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheSameBetaReadsThreeFaces.lean:22 · SHA256 `2efd8b379f210111e0383d9c40e5fc72835f41cd94aad2dd70d645d66f400c16`
```lean
structure TGLCoupling
```
REUSAR diretamente

### the_same_beta_reads_three_faces
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheSameBetaReadsThreeFaces.lean:76 · SHA256 `2efd8b379f210111e0383d9c40e5fc72835f41cd94aad2dd70d645d66f400c16`
```lean
theorem the_same_beta_reads_three_faces (c : TGLCoupling) (ρr ρm ρΛ : ℝ) :
    Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta
    ∧ (0 < c.alpha ∧ c.alpha < 1
      ∧ c.beta = c.alpha * Real.exp (1 / 2)
      ∧ c.beta = c.alpha * Real.sqrt (Real.exp 1))
    ∧ (c.beta * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
        = c.beta * ((4 / 3) * ρr + ρm))
    ∧ ((ρr + ρm + ρΛ) + c.beta * ((4 / 3) * ρr + ρm)
        = (1 + 4 * c.beta / 3) * ρr + (1 + c.beta) * ρm + ρΛ)
    ∧ (∀ t g : ℝ, 0 < t → 0 < g → Real.exp (-(t * c.beta * g)) < 1)
    ∧ (∀ b : ℝ, (∀ t : ℝ, Real.exp (-(t * b)) = Real.exp (-(t * c.beta)))
        → b = c.beta)
```
REUSAR diretamente

### flrwStress
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean:68 · SHA256 `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8`
```lean
def flrwStress (a rho pressure : ℝ → ℝ) : TensorField4
```
REUSAR diretamente

### flrw_stress_divergence
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean:109 · SHA256 `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8`
```lean
theorem flrw_stress_divergence (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (hz : a (x 0) ≠ 0) (ha : DifferentiableAt ℝ a (x 0))
    (hr : DifferentiableAt ℝ rho (x 0)) (hp : DifferentiableAt ℝ pressure (x 0)) :
    tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x =
      ![deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)),0,0,0]
```
REUSAR diretamente

### flrw_friedmann_first
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean:135 · SHA256 `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8`
```lean
theorem flrw_friedmann_first (U : Set Coordinate4) (hU : IsOpen U)
    (a rho pressure : ℝ → ℝ) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
    (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
    (coupling cosmological : ℝ)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x +
      cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
    (flrwHubble a (x 0))^2 = coupling/3*rho (x 0)-cosmological/3
```
REUSAR diretamente

### flrw_friedmann_from_general_metric
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean:192 · SHA256 `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8`
```lean
theorem flrw_friedmann_from_general_metric
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (a rho pressure : ℝ → ℝ) (eta : ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (hr : ∀ y∈U, DifferentiableAt ℝ rho (y 0))
    (hp : ∀ y∈U, DifferentiableAt ℝ pressure (y 0))
    (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
        (2*Real.pi/eta) • flrwStress a rho pressure x) v = 0)
    (H_conservation : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x j = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      (flrwHubble a (x 0))^2 = (2*Real.pi/eta)/3*rho (x 0)-cosmological/3 ∧
      deriv (flrwHubble a) (x 0) = -(2*Real.pi/eta)/2*(rho (x 0)+pressure (x 0)) ∧
      deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)) = 0
```
REUSAR diretamente

### flrw_newton_coefficient
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean:222 · SHA256 `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8`
```lean
theorem flrw_newton_coefficient (G : ℝ) (hG : 0 < G) :
    (2*Real.pi/(1/(4*G)))/3 = 8*Real.pi*G/3
```
REUSAR diretamente

### finite_covector_stress_conserved
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FiniteCoherentSources.lean:154 · SHA256 `4b71fe49ae505d3017a3c2d05395de95f6c64f9630ea27c56de8ed024d94416b`
```lean
theorem finite_covector_stress_conserved (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4) (w : J → CovectorField4)
    (weight coupling : J → ℝ) (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv)
    (hw : ∀ q, SmoothVectorOn U (w q))
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x ∈ U, (g x)ᵀ = g x)
    (hl : ∀ x ∈ U, gInv x * g x = 1) (hr : ∀ x ∈ U, g x * gInv x = 1)
    (ht : ∀ x ∈ U, ∀ i j k, Gamma x i k j = Gamma x j k i)
    (hclosed : ∀ q, ClosedCovectorOn U (w q))
    (hwave : ∀ q, CovectorWaveOn U gInv Gamma (w q)) :
    ∀ x ∈ U, ∀ j, tensorFieldDivergence gInv Gamma
      (finiteCovectorStressField g gInv w weight coupling) x j = 0
```
TIPO DIFERENTE: fonte covetorial/fluxo total, não a lei escalar com w constante

### general_source_heat_matching
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralSourceEinsteinBridge.lean:43 · SHA256 `d4055e0f95d6ed7b83456bbd837a3c77e354f191a248c7f1b65933fb0f4853e9`
```lean
theorem general_source_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4}
    {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4) (rate : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hTd : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U)
    (hLor : LorentzByCongruence (g x)) (hTs : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) direction = 0) :
    Tendsto (fun t => microscopicHeatError (calibrationSourceCurve g T x direction) rate
      (constructedHeat P T rate hU hg hTd) t / t^2) (𝓝[<] 0) (𝓝 0)
```
TIPO DIFERENTE: fonte covetorial/fluxo total, não a lei escalar com w constante

### HasDerivAt.fun_sum
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\.lake\packages\mathlib\Mathlib\Analysis\Calculus\Deriv\Add.lean:218 · SHA256 `0921f2e9832bcfe3bb5147964ed2eb8663da64eb8497a69f7b83d2e37ac6cf55`
```lean
theorem HasDerivAt.fun_sum (h : ∀ i ∈ u, HasDerivAt (A i) (A' i) x) :
    HasDerivAt (fun y ↦ ∑ i ∈ u, A i y) (∑ i ∈ u, A' i) x
```
REUSAR, especializando escalares reais e soma finita

### HasDerivAt.const_mul
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\.lake\packages\mathlib\Mathlib\Analysis\Calculus\Deriv\Mul.lean:357 · SHA256 `883a9a5747481fc83c88e6f7de8816a22915f3a328ec66c754d5264232cadbf1`
```lean
theorem HasDerivAt.const_mul (c : 𝔸) (hd : HasDerivAt d d' x) :
    HasDerivAt (fun y => c * d y) (c * d') x
```
REUSAR, especializando escalares reais e soma finita

## Seis buscas e repetição das leituras negadas
```json
[
  {
    "timestamp": "2026-09-14T16:24:29.305884-03:00",
    "searches": [
      {
        "label": "01_kernel",
        "command": [
          "rg",
          "-n",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 1874,
        "stderr_bytes": 0
      },
      {
        "label": "02_notes",
        "command": [
          "rg",
          "-n",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911",
          "-g",
          "*.md",
          "-g",
          "!*.bak*",
          "-g",
          "!**/r/**",
          "-g",
          "!**/revisao/**"
        ],
        "returncode": 1,
        "stdout_bytes": 0,
        "stderr_bytes": 0
      },
      {
        "label": "03_deliveries",
        "command": [
          "rg",
          "-n",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT",
          "-g",
          "*.md"
        ],
        "returncode": 0,
        "stdout_bytes": 3095,
        "stderr_bytes": 0
      },
      {
        "label": "03_workbenches",
        "command": [
          "rg",
          "-l",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity",
          "C:\\IALD\\Central de Patentes\\Chatgpt",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**",
          "-g",
          "!**/attempts/**",
          "-g",
          "!**/revisao/**",
          "-g",
          "!**/DEPENDENCIAS_CE*/**",
          "-g",
          "!*.bak*"
        ],
        "returncode": 0,
        "stdout_bytes": 50957,
        "stderr_bytes": 0
      },
      {
        "label": "04_tree",
        "command": [
          "rg",
          "-n",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity|Einstein|Clausius",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\inputs\\A_PROVA_DA_QG_TGL_arvore.md"
        ],
        "returncode": 0,
        "stdout_bytes": 7177,
        "stderr_bytes": 0
      },
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity",
          "C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 2,
        "stdout_bytes": 0,
        "stderr_bytes": 144
      },
      {
        "label": "06_acervo",
        "command": [
          "C:\\Python314\\python.exe",
          "-X",
          "utf8",
          "-B",
          "C:\\IALD\\INDICE_DO_ACERVO\\buscar.py",
          "H_nx|w_eff|rho.plus.p",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 2,
        "stdout_bytes": 0,
        "stderr_bytes": 112
      }
    ]
  },
  {
    "timestamp": "2026-09-14T16:26:29.471908-03:00",
    "searches": [
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity",
          "C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 1,
        "stdout_bytes": 0,
        "stderr_bytes": 0
      },
      {
        "label": "06_acervo",
        "command": [
          "C:\\Python314\\python.exe",
          "-X",
          "utf8",
          "-B",
          "C:\\IALD\\INDICE_DO_ACERVO\\buscar.py",
          "H_nx|w_eff|rho.plus.p",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 0,
        "stdout_bytes": 10595,
        "stderr_bytes": 0
      }
    ]
  }
]
```

Grupos por bytes: {"path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\BUSCAS_B3_GRUPOS.json", "sha256": "f7fb3a713b3d1f904d4cb2289ae3d1b7378ff9bf485d8cdb5105422d4f5b0111", "distinct_bytes": 24, "files": 413}

- As duas leituras inicialmente negadas foram refeitas com acesso autorizado; erro de acesso não foi contado como ausência.
- A busca no índice do acervo retornou 25 recortes históricos e corte explícito. Não prova ausência exaustiva; resultados empíricos ali mencionados não foram revalidados nem utilizados.
- Fornecedores covetoriais tratam outro tipo de fonte e não satisfazem H_nx por homonímia.
- B2 está compilado e auditado pelo autor; revisão independente em curso. Sua fonte permanece congelada.
- Λ existencial não é zero por definição; o enunciado geral a conserva e o corolário zero exige hipótese nomeada.
- ρ>0 e entalpia>=0 entram exatamente no uso de w_eff/valor absoluto; nenhuma divisão por zero é ocultada.
- Não supor que a rescalagem seja não negativa sem hipótese adicional sobre o fator.
- Não-troca setorial e w_i constante são hipóteses [INPUT]; TGL-S/TGL-L e Lema 3 continuam abertos.
- As entradas propostas e a V3/D1 são consumidor da gerência; este trabalho não edita runtime nem gate.

2026-09-14T16:33:39.655896-03:00
