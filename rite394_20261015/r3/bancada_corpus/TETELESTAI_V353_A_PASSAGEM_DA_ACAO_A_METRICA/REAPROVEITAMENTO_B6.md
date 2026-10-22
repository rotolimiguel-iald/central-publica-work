[OPEN — ficha anterior aos artefatos B6]

# B6 — estatutos e importações explícitas

REUSAR e documentar: nenhum teorema novo; somente auditor de fornecedores existentes e propostas documentais tipadas.

## Tipo do produto
```text
B6 adds no mathematical assertion or axiom. Deliver typed JSON proposal:
 external_known_theorems: four entries with name,status,citation,exact_role,verified_url,
 source_read_scope,imported_into_witness=false;
 scope: H3 IMPORTED (conditional modus ponens), G/eta INPUT, H_nx INPUT,
 modified differential entropy INPUT, global Lemma3 OPEN, TGL-S/TGL-L OPEN;
 corrections: radius in Cai-Kim flux, variable-Phi derivative, density support for equality,
 nonzero total enthalpy for unique Phi_flux, explicit cosmological/integration constant;
 changes_gate=false, implements_runtime=false, chooses_route=false.
Audit existing fullnames by Lake: TheImportedEquilibrium logical providers, AreaScale calibration,
SectorFluid H_nx structure, HubbleHorizonInput, B4 derivative/support conditions.
No new theorem is needed for a bibliography or status table; importing a theorem as an implication
does not construct its horizon/equilibrium premise. The four literature sources do not prove Phi_TGL.
```

## Consumidores
```json
[
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 134757,
    "text": "EXTERNAL_KNOWN_THEOREMS = [",
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

### the_trio_is_a_pair
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:140 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem the_trio_is_a_pair {H1 H2 H3 P : Prop}
    (master : H1 ∧ H2 ∧ H3 → P) (imported : H2 → H3) :
    H1 ∧ H2 → P
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### the_pair_still_needs_its_hypotheses
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:149 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem the_pair_still_needs_its_hypotheses :
    ∃ H1 H2 P : Prop, (H1 ∧ H2 → P) ∧ ¬ P
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### discharge_by_import
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:129 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem discharge_by_import {H C : Prop} (h : H) (imported : H → C) : C
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### newtonPlanck_equivalence
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGL\AreaScale.lean:24 · SHA256 `7058ae26f99f44f2d81d0c51e39bf435359a94c410405e52da4c4a44834ce075`
```lean
theorem newtonPlanck_equivalence (kappa G : ℝ) (hk : 0 < kappa) (hG : 0 < G) :
    2 * Real.pi / (1 / (2 * kappa)) = 8 * Real.pi * G ↔ kappa = 2 * G
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### halfNat_over_two_faces_eq_quarter
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGL\AreaScale.lean:41 · SHA256 `7058ae26f99f44f2d81d0c51e39bf435359a94c410405e52da4c4a44834ce075`
```lean
theorem halfNat_over_two_faces_eq_quarter (G : ℝ) :
    (1 / 2) / (2 * G) = 1 / (4 * G)
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### SectorFluid
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean:20 · SHA256 `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3`
```lean
structure SectorFluid (ι : Type*) [Fintype ι] (I : Set ℝ) (H : ℝ → ℝ)
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### HubbleHorizonInput
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean:38 · SHA256 `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3`
```lean
structure HubbleHorizonInput (H : ℝ → ℝ) (t G Phi enthalpy : ℝ)
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### variable_entropy_derivative
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean:81 · SHA256 `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3`
```lean
theorem variable_entropy_derivative (A Phi : ℝ → ℝ) (t G : ℝ)
    (ha : DifferentiableAt ℝ A t) (hp : DifferentiableAt ℝ Phi t)
    (hg : G ≠ 0) (hz : Phi t ≠ 0) :
    HasDerivAt (fun u => A u/(4*G*Phi u))
      (deriv A t/(4*G*Phi t)-A t*deriv Phi t/(4*G*(Phi t)^2)) t
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### the_two_routes_equal_iff
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorRouteComparison.lean:106 · SHA256 `b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4`
```lean
theorem the_two_routes_equal_iff (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.correctedTotalRho c t+F.correctedTotalPressure c t =
      entropyFactor c (F.wEff t)*F.enthalpy t ↔
      ∃ commonW : ℝ, ∀ i, 0 < F.rho i t → F.w i = commonW
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### zero_flux_has_no_unique_factor
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorRouteComparison.lean:165 · SHA256 `b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4`
```lean
theorem zero_flux_has_no_unique_factor (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (he : F.enthalpy t = 0) :
    ¬ ∃! factor : ℝ, factor*F.enthalpy t =
      F.correctedTotalRho c t+F.correctedTotalPressure c t
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

## Buscas
```json
[
  {
    "timestamp": "2026-09-14T16:59:48.950118-03:00",
    "searches": [
      {
        "label": "01_kernel",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 11740,
        "stderr_bytes": 0
      },
      {
        "label": "02_notes",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
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
        "returncode": 0,
        "stdout_bytes": 17145,
        "stderr_bytes": 0
      },
      {
        "label": "03_deliveries",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT",
          "-g",
          "*.md"
        ],
        "returncode": 0,
        "stdout_bytes": 172,
        "stderr_bytes": 0
      },
      {
        "label": "03_workbenches",
        "command": [
          "rg",
          "-l",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
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
        "stdout_bytes": 223003,
        "stderr_bytes": 0
      },
      {
        "label": "04_tree",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3|Einstein|Clausius",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\inputs\\A_PROVA_DA_QG_TGL_arvore.md"
        ],
        "returncode": 0,
        "stdout_bytes": 5855,
        "stderr_bytes": 0
      },
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
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
          "the_trio_is_a_pair|invariance_does_not_fix_area|TGL-S",
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
    "timestamp": "2026-09-14T17:00:44.475206-03:00",
    "searches": [
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 373,
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
          "the_trio_is_a_pair|invariance_does_not_fix_area|TGL-S",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 0,
        "stdout_bytes": 11574,
        "stderr_bytes": 0
      }
    ]
  }
]
```

- Buscas por nomes/tipos e recortes, não varredura exaustiva de todo conteúdo.
- Gibbons–Hawking: metadados e resumo oficiais lidos; PDF oficial retornou 401. Não alegar leitura integral.
- Cai–Kim: seção2 lida em HTML primário, incluindo raio, fluxo, temperatura e conservação. Jacobson: texto primário lido sobre horizontes locais/hipóteses. Padmanabhan: resumo e trechos introdutórios primários lidos, papel contextual.
- Não alterar EXTERNAL_KNOWN_THEOREMS canônico: gerar proposta para gerência.
- Não derivar H3, G ou lei Phi por mera citação. B6 não encerra A1(b), que retoma após as entregas B1–B6.

2026-09-14T17:04:54.683217-03:00
