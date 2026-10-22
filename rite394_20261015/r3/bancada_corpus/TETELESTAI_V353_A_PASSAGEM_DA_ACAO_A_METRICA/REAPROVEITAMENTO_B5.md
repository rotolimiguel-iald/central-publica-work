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
