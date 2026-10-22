[REAL — B5 pago como reescrita angular das equações condicionais B3/B4. Quatro teoremas; nenhum conteúdo dinâmico novo. Integração pela gerência.]

# ENTREGA 012 / B5 — o ângulo lê a métrica

2026-09-14T17:17:18.942151-03:00

Os quatro corolários unem a mesma variável beta de TGLCoupling, a reflexão da matriz-S e as equações já demonstradas em B3/B4. Não acrescentam um segundo parâmetro ou uma segunda lei de fundo.

## Critérios

| Critério B5 | Resultado |
|---|---|
| Ficha e aproveitamento anteriores ao código | PAGO; cinco fornecedores conferidos por hash/linha; buscas com falhas de leitura repetidas e corte histórico declarado. |
| Mesmo beta e mesma matriz-S | PAGO; coupling_eq_sin_sq compõe c.reflection_weight com normSq_reflection. Beta é sin²(thetaMiguel beta), não amplitude sin(theta). |
| Φ=1+sin²(thetaMiguel beta)|1+w| | PAGO; the_angle_reaches_the_metric reescreve entropyFactor. |
| Segunda equação angular | PAGO condicional; the_passage aplica B4 com o mesmo HubbleHorizonInput, mantendo suas entradas físicas e o sinal −4πG. |
| Primeira equação angular | PAGO condicional; the_angle_reads_sector_first aplica B3, mantendo H_nx, H_null e Λ existencial. |
| Regra dos dois regimes | PAGO; nenhum theta foi inserido em r_s, D_M, l_A ou H(z); runtime não foi tocado. Não há limite ou dinâmica angular nova. |
| Axiomas e reprodução | PAGO; quatro teoremas no trio, Lake autoral e próprio independente rc0, sem avisos novos. |
| Controles adversariais | PAGO; duas adulterações de conteúdo rejeitadas por Type mismatch. |
| Aceite | PAGO no escopo DEV B5, P0/P1/P2=0/0/0; integração não revisada. |

## Conclusões e hipóteses preservadas

```text
c.reflection_weight + normSq_reflection
 -> c.beta = sin(thetaMiguel c.beta)^2
 -> Φ = 1+sin(thetaMiguel c.beta)^2 |1+w|
 -> B4: H' = -4πG [1+sin²θ_M |1+w|](ρ+p)
 -> B3: existe Λ, H²=(8πG/3)ρ_tot[1+sin²θ_M |1+w_eff|]-Λ/3
```

As duas últimas linhas são aplicações separadas de teoremas anteriores, **não uma identificação entre as duas rotas que B4 distinguiu**. B4 mantém H>0, G>0, Φ>0, diferenciabilidade, fluxo com raio de horizonte, lei diferencial de entropia e Clausius. B3 mantém setores sem troca H_nx, w_i constantes, U aberto/preconexo, a suave/positivo, tempo em I, G>0, rhoTot>0 e entalpia≥0, além de H_null para o stress corrigido. O termo −Λ/3 não foi descartado.

O kernel usa beta variável; a forma geométrica não deriva o valor experimental de alpha. O ângulo lê o mesmo fator e não seleciona lei por ajuste ou por resultado cosmológico. Nenhum observável independente foi criado, nenhum fechamento global ou perturbativo foi provado.

## Reprodução e falhas preservadas

Run final autoral `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_170027_789047\run.json` rc0, fontes antes/depois idênticas. Na bancada `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA`, run_b5_lake.py invoca `lake build TGLExt.TheAngleReachesTheMetric TGLExt.AuditMetricAngle` na raiz kernel. AuditMetricAngle e sondas são executados por `lake env lean`; BadAngleAmplitude troca sin² por sin; BadAngleFactor remove o termo unitário. Ambos falham por Type mismatch, sem falha de import.

O revisor compilou `lake build TGLExt.TheAngleReachesTheMetric TGLExt.AuditMetricAngle TGLExt.ReviewMetricAngle` em s, run `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b5\independent_20260914_170847_217866\run.json`, rc0. Três novos objetos próprios; 117 objetos próprios anteriores preservados, 120 no total. Os dois objetos B5 são iguais aos autorais. Nenhum olean de projeto autoral foi copiado; Mathlib e oito pacotes auxiliares permanecem caches herdados/pinados, sem alegação de reconstrução destes.

O revisor leu fontes, ficha e controles autorais, executou sua própria auditoria de tipos/axiomas, mas não repetiu os negativos nem a varredura de 941 fontes-base e um.py. A preservação ampla foi medida pelo auditor autoral. Não houve falha de Lean ou aviso novo nas tentativas B5, nem na revisão. Falhas anteriores de acesso durante buscas foram registradas e repetidas; resultados negativos de busca não se confundem com falhas de leitura.

## Nomes completos e axiomas

| Alvo | Axiomas |
|---|---|
| `ChatgptAudit.FLRW.coupling_eq_sin_sq` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_angle_reaches_the_metric` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_passage` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_angle_reads_sector_first` | propext, Classical.choice, Quot.sound |

## Arquivos e hashes lidos

| Arquivo | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheAngleReachesTheMetric.lean` | `cba7dd9dc567e6a228ac5aaf5a31aa7062608642cc393d80d516bca15bf7ec5b` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AuditMetricAngle.lean` | `b6508066217a4ace3f079db07359131e4eedeeaea71f19da76b56fb7a0a4e96d` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B5.md` | `c0e797b85610f1103567fc9d52851f66c27b0e5cd1e17446b5ff3049da333938` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B5.json` | `3a8ae4aa0ab019283f6189cfb7f5737e573f2d0b2a56da20208af5eb6fbd5ac2` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\AUDITORIA_B5.json` | `0b6d4cd5bf0f978691042802d04dfa51eabea9be0d3760d78254685223beb5e9` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\ALVOS_B5.json` | `dd90eea69e5113421976a7f9711c3db0a1a82542596c2f4922880b52f1cfea59` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b5\REVIEW_B5_FINAL.md` | `b07e2c2adf94b7ed4734c1da113e6b1dc94836a81b9cf904652a7d5ab5b316b7` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b5\REVIEW_B5_FINAL.json` | `e1fa28eb6c81c7df5eb83687f0115f0f2e7ba32c1204131cddb66a16c3a9534c` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b5\compilation.json` | `7a7fc0a8740e717899720b72a6214c8c98c1ef5264def783439bcfa2cde9d1f1` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\run_b5_lake.py` | `390a1d7f100a13f04a06affb085552d6d3b6f0883b03264bb1ff50e00564fdf2` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\audit_b5.py` | `e537b4fde367d60e087a5d35841688a57fb7f9023791b4777cc688e9894d194e` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b5_ficha.py` | `f3c3dbe80816fa56978d6e7fdc580294ba1f7ff4f9aaf814f8b0a5397b1bcb44` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b5_audit.py` | `d36d2a3481f28ae02172e5f95ba1ea284756ca5b1cc094ddd61f45dc688f7918` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\deliver_b5.py` | `4c9c7d473d9c173c5a5f091c39c34c6467e5d528c7a240c9086db1291446fc20` |

MANIFESTO_B5 e RECIBO_B5 vinculam entrega, fontes, objetos, runs, controles e revisão. Os consumidores ext_* constam na ficha como propostas para a gerência. Nenhum gate, dado, protocolo, runtime, original, Atlas ou memória foi alterado.

## Ficha integral

[OPEN — ficha anterior ao código B5]

# B5 — leitura angular, sem conteúdo dinâmico novo

REUSAR B1/B3/B4: somente corolários por reescrita; B5 não acrescenta conteúdo dinâmico.

## Tipo
```text
c:TGLCoupling; theta=TGLExt.thetaMiguel c.beta, already defined.
coupling_eq_sin_sq: c.beta=(sin theta)^2 via actual reflection_weight and normSq_reflection.
the_angle_reaches_the_metric: entropyFactor c w=1+(sin theta)^2*abs(1+w).
the_passage: HubbleHorizonInput H t G (entropyFactor c w) E ->
 deriv H t=-4*pi*G*(1+(sin theta)^2*abs(1+w))*E.
the_angle_reads_sector_first: all B3 hypotheses unchanged (U open preconnected,
smooth positive a, finite H_nx sectors, totalrho>0, enthalpy>=0, G>0, H_null),
exists Lambda, H^2=(8*pi*G/3)*rho*(1+(sin theta)^2*abs(1+wEff))-Lambda/3.
No scalar, state, source, angle definition, differential law or horizon hypothesis added.
```

## Consumidores
```json
[
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
  }
]
```

## Fornecedores

### normSq_reflection
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SMatrix.lean:241 · SHA256 `14f7e717a4ef70204eeb825d989e6dcc3397c274f1c45a3820420ea6af12a3b7`
```lean
theorem normSq_reflection (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 1) = Real.sin θ ^ 2
```
REUSAR literalmente; corolário por reescrita

### reflection_weight
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheSameBetaReadsThreeFaces.lean:52 · SHA256 `2efd8b379f210111e0383d9c40e5fc72835f41cd94aad2dd70d645d66f400c16`
```lean
theorem reflection_weight (c : TGLCoupling) :
    Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta
```
REUSAR literalmente; corolário por reescrita

### entropyFactor
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean:21 · SHA256 `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3`
```lean
def entropyFactor (c : TGLCoupling) (w : ℝ) : ℝ
```
REUSAR literalmente; corolário por reescrita

### tgl_second_friedmann_from_clausius
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean:56 · SHA256 `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3`
```lean
theorem tgl_second_friedmann_from_clausius (H : ℝ → ℝ) (t G Phi enthalpy : ℝ)
    (D : HubbleHorizonInput H t G Phi enthalpy) :
    deriv H t = -4*Real.pi*G*Phi*enthalpy
```
REUSAR literalmente; corolário por reescrita

### tgl_friedmann_from_sector_closure
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFriedmann.lean:37 · SHA256 `7c115dd6a8d71333d8811a6efbf7d46d4363e25d18b23f8c7e678e951c0b9dfa`
```lean
theorem tgl_friedmann_from_sector_closure
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (I : Set ℝ) (a : ℝ → ℝ) (F : SectorFluid ι I (flrwHubble a))
    (c : TGLCoupling) (G : ℝ) (hG : 0 < G)
    (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) (hpos : ∀ x∈U, 0 < a (x 0))
    (hI : ∀ x∈U, x 0∈I)
    (hr : ∀ x∈U, 0 < F.totalRho (x 0))
    (he : ∀ x∈U, 0 ≤ F.enthalpy (x 0))
    (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
        (2*Real.pi/(1/(4*G))) •
          flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) v = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
        F.totalRho (x 0)*(1+c.beta*|1+F.wEff (x 0)|)-cosmological/3 ∧
      deriv (flrwHubble a) (x 0) = -4*Real.pi*G*
        (F.correctedTotalRho c (x 0)+F.correctedTotalPressure c (x 0)) ∧
      deriv (F.correctedTotalRho c) (x 0)+3*flrwHubble a (x 0)*
        (F.correctedTotalRho c (x 0)+F.correctedTotalPressure c (x 0)) = 0
```
REUSAR literalmente; corolário por reescrita

## Buscas
```json
[
  {
    "timestamp": "2026-09-14T16:56:04.987954-03:00",
    "searches": [
      {
        "label": "01_kernel",
        "command": [
          "rg",
          "-n",
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 2114,
        "stderr_bytes": 0
      },
      {
        "label": "02_notes",
        "command": [
          "rg",
          "-n",
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel",
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
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT",
          "-g",
          "*.md"
        ],
        "returncode": 0,
        "stdout_bytes": 2281,
        "stderr_bytes": 0
      },
      {
        "label": "03_workbenches",
        "command": [
          "rg",
          "-l",
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel",
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
        "stdout_bytes": 41523,
        "stderr_bytes": 0
      },
      {
        "label": "04_tree",
        "command": [
          "rg",
          "-n",
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel|Einstein|Clausius",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\inputs\\A_PROVA_DA_QG_TGL_arvore.md"
        ],
        "returncode": 0,
        "stdout_bytes": 7477,
        "stderr_bytes": 0
      },
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel",
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
          "the_angle_reaches_the_metric|sin_thetaMiguel|normSq_reflection",
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
    "timestamp": "2026-09-14T16:56:32.715309-03:00",
    "searches": [
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "the_angle_reaches_the_metric|the_passage|normSq_reflection|sin_thetaMiguel",
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
          "the_angle_reaches_the_metric|sin_thetaMiguel|normSq_reflection",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 0,
        "stdout_bytes": 12815,
        "stderr_bytes": 0
      }
    ]
  }
]
```

- Nenhum theta, seno, cosseno ou raiz de beta é inserido em r_s, D_M, l_A ou worker H(z). Código Lean apenas lê as equações já obtidas.
- A busca do índice do acervo tem corte declarado e majoritariamente registros de auditoria da matriz-S; não é prova de ausência exaustiva.
- B1/B2 selados, B3 compilado/auditado, B4 compilado e auditor em curso. Não modificar fornecedores por esta ficha.
- Λ, G e hipóteses de horizonte e não-troca conservam seus estatutos.

2026-09-14T16:58:03.305728-03:00
