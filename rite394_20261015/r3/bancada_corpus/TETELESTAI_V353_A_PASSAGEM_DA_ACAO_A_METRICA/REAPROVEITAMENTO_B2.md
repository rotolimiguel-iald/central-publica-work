[OPEN — ficha anterior ao código B2]

# B2 — FLRW na carta e nas definições geométricas da casa

NOVO: avaliação FLRW da maquinaria geral. REUSAR: reconstrução de Einstein, inversa, conexão, curvatura e divergência. A busca não achou fornecedor FLRW; o ansatz univariado antigo é outra métrica e não será renomeado.

## Tipo exigido
```text
a : Real -> Real; U : Set Coordinate4 open; for each x in U, ContDiffAt Real infinity a (x 0) and 0<a(x 0).
flrwMetric a x = diag(1,-a(x0)^2,-a(x0)^2,-a(x0)^2).
Use metricInverse(flrwMetric a), leviCivitaField of that same metric/inverse, coordinateRicci and geometricEinsteinTensor.
G00=3*(a'/a)^2; Gii=-(2*a*a''+(a')^2) for spatial i; off-diagonal G=0.
For null k, Ric(k,k)=2*((a'/a)^2-a''/a)*(k0)^2.
For T=diag(rho,p*a^2,p*a^2,p*a^2), scalar rho,p depend on x0 and are differentiable locally.
Instantiate metric_only_einstein_equation with connected U, null balance and divergence zero:
exists Lambda, G+Lambda*g=(2*pi/eta)*T, then H^2=(2*pi/(3*eta))*rho-Lambda/3
and H'=-(pi/eta)*(rho+p), equivalently a''/a=-(pi/(3*eta))*(rho+3*p)-Lambda/3.
Same divergence zero implies rho'+3*(a'/a)*(rho+p)=0.
With eta=1/(4*G_Newton) and G_Newton>0, coefficient 2*pi/(3*eta)=8*pi*G_Newton/3.
The formal Lambda sign follows G+Lambda*g=kappa*T in the existing layer; no identification with a physically named Lambda is assumed.
```

## Consumidores
[
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 128506,
    "text": "\"ext_v338_generalmetric_metric_only_einstein_equation_kernel_proved\": \"ChatgptAudit.GeneralMetric.metric_only_einstein_equation\",",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 128759,
    "text": "\"ext_v338_generalclausius_metric_einstein_from_screen_clausius_kernel_proved\": \"ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius\",",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 133228,
    "text": "\"ext_tm_einstein_coefficient_kernel_proved\": \"TGLExt.einstein_coefficient_from_clausius\",",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 133716,
    "text": "\"ext_rp_hubble_form_kernel_proved\": \"TGLExt.hubble_form\",",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  }
]

B3 tgl_friedmann_from_sector_closure consome equação 00; B4 compara a equação derivada de Clausius. Implementação do mapa pertence à gerência.

## Fornecedores e tipos lidos

### eta4
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\Solder4D.lean:61 · SHA256 `70f3c2aa3336b716a740a70c15759ffdaca612c7c69f975c0281a31e9bb2f35f`
```lean
def eta4 : Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### solder4_lorentzian
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\Solder4D.lean:93 · SHA256 `70f3c2aa3336b716a740a70c15759ffdaca612c7c69f975c0281a31e9bb2f35f`
```lean
theorem solder4_lorentzian {e : Matrix (Fin 4) (Fin 4) ℝ} (he : e.det ≠ 0) :
    (solderMetric4 e).det < 0
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### LorentzByCongruence
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\EmergenceTriad.lean:72 · SHA256 `3b7c6220060598fb4353dddefd71fb9064db3ce8a1e2cf891d0f2ae8c97c04e9`
```lean
def LorentzByCongruence (g : Matrix (Fin 4) (Fin 4) ℝ) : Prop
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### Coordinate4
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CovariantScalarConservation.lean:24 · SHA256 `69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c`
```lean
abbrev Coordinate4
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### TensorField4
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CovariantScalarConservation.lean:25 · SHA256 `69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c`
```lean
abbrev TensorField4
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### coordinatePartial
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CovariantScalarConservation.lean:27 · SHA256 `69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c`
```lean
def coordinatePartial (f : Coordinate4 → ℝ) (x : Coordinate4) (i : Fin 4) : ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### tensorFieldJet
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CovariantScalarConservation.lean:30 · SHA256 `69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c`
```lean
def tensorFieldJet (A : TensorField4) (x : Coordinate4) (i : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### tensorFieldDivergence
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CovariantScalarConservation.lean:33 · SHA256 `69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c`
```lean
def tensorFieldDivergence (gInv : TensorField4)
    (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (A : TensorField4) (x : Coordinate4) (j : Fin 4) : ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### tensorFieldJet_congr_on
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CovariantScalarConservation.lean:52 · SHA256 `69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c`
```lean
theorem tensorFieldJet_congr_on (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : Set.EqOn A B U) (x : Coordinate4) (hx : x∈U) :
    tensorFieldJet A x=tensorFieldJet B x
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### leviCivitaJet
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\MetricCompatibleJet.lean:34 · SHA256 `d20de372f56b28d5de7134d5e28a47d70b8a453c9da0a97cb729270e860463c7`
```lean
def leviCivitaJet (gInv : Matrix (Fin 4) (Fin 4) ℝ)
    (dg : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (i : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### leviCivitaField
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\MetricFieldConnection.lean:22 · SHA256 `f5134b7ed4a069fc1235c890174a4487566861ef676ccaa0f2e230bf4e26a832`
```lean
def leviCivitaField (g gInv : TensorField4) (x : Coordinate4) :
    Fin 4 → Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### levi_civita_field_metric_compatible
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\MetricFieldConnection.lean:34 · SHA256 `f5134b7ed4a069fc1235c890174a4487566861ef676ccaa0f2e230bf4e26a832`
```lean
theorem levi_civita_field_metric_compatible (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hleft : ∀ x∈U, gInv x*g x=1) (hright : ∀ x∈U, g x*gInv x=1) :
    ∀ x∈U, ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (leviCivitaField g gInv x) i=0
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### coordinateCurvature
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\CoordinateCurvature.lean:36 · SHA256 `8a3af4a1c80c18f4670377ab35ab6e661b724120a359a3150c9b68e30024e68a`
```lean
def coordinateCurvature (Gamma : ConnectionField4) (x : Coordinate4) (i j : Fin 4) :
    Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### coordinateRicci
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\MetricCurvatureSymmetries.lean:31 · SHA256 `6070daffdf63f24ee64157c11da8cbcf43765b6ce2c42069780a09b140064db7`
```lean
def coordinateRicci (Gamma : ConnectionField4) (x : Coordinate4) : Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### geometricEinsteinTensor
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\MetricCurvatureSymmetries.lean:37 · SHA256 `6070daffdf63f24ee64157c11da8cbcf43765b6ce2c42069780a09b140064db7`
```lean
def geometricEinsteinTensor (g gInv : TensorField4) (Gamma : ConnectionField4) (x : Coordinate4) :
    Matrix (Fin 4) (Fin 4) ℝ
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### metricInverse
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralMetricEinstein.lean:191 · SHA256 `5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c`
```lean
def metricInverse (g : TensorField4) : TensorField4
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### metric_inverse_unique
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralMetricEinstein.lean:42 · SHA256 `5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c`
```lean
theorem metric_inverse_unique (g leftInv rightInv : Tensor4)
    (hl : leftInv * g = 1) (hr : g * rightInv = 1) :
    leftInv = rightInv
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### constructed_metric_inverse_left
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralMetricEinstein.lean:235 · SHA256 `5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c`
```lean
theorem constructed_metric_inverse_left (g : TensorField4) (x : Coordinate4)
    (hg : LorentzByCongruence (g x)) : metricInverse g x * g x = 1
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### constructed_metric_inverse_right
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralMetricEinstein.lean:240 · SHA256 `5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c`
```lean
theorem constructed_metric_inverse_right (g : TensorField4) (x : Coordinate4)
    (hg : LorentzByCongruence (g x)) : g x * metricInverse g x = 1
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### metric_only_einstein_equation
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralMetricEinstein.lean:245 · SHA256 `5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c`
```lean
theorem metric_only_einstein_equation
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T : TensorField4) (coupling : ℝ)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (g x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField g (metricInverse g)) x -
        coupling • T x) v = 0)
    (hdT : ∀ x∈U, ∀ j,
      tensorFieldDivergence (metricInverse g)
        (leviCivitaField g (metricInverse g)) T x j = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
      cosmological • g x = coupling • T x
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### metric_einstein_from_screen_clausius
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\GeneralMetricClausius.lean:83 · SHA256 `d635b15c7197800ae26034bbf8d11ddc422a2dbf17633c743b603d3d66143109`
```lean
theorem metric_einstein_from_screen_clausius
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T : TensorField4) (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) T x j = 0)
    (screens : MetricScreenFamily U g)
    (rate eta : ℝ) (hrate : rate ≠ 0) (heta : eta ≠ 0)
    (hclausius : ∀ p (hp : p∈U) v (hv : v ≠ 0) (hn : tensorQuad (g p) v = 0),
      MetricScreenClausius (screens p hp v hv hn) T rate eta hU hg hT) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
      cosmological • g x = (2*Real.pi/eta) • T x
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### einstein_coefficient_from_clausius
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TriadMaster.lean:71 · SHA256 `64e0899e259693927b051493b8f20cc47885f183d02d79a8772e3b3d869863ae`
```lean
theorem einstein_coefficient_from_clausius (kappa a G : ℝ) (hG : G ≠ 0) :
    (kappa / (2 * Real.pi)) * (a / (4 * G)) = kappa * a / (8 * Real.pi * G)
```
REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.

### ansatzRicci00
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AnsatzEinstein.lean:57 · SHA256 `88ed36908dbc290f07574a0cf8e9a711220875ff79322ad89c21ce95f7dd436a`
```lean
def ansatzRicci00 (s : ℝ) : ℝ
```
NÃO USAR como FLRW: outro ansatz, Ricci definido à mão

### ansatzG00_zero
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AnsatzEinstein.lean:110 · SHA256 `88ed36908dbc290f07574a0cf8e9a711220875ff79322ad89c21ce95f7dd436a`
```lean
theorem ansatzG00_zero (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzG00 q s = 0
```
NÃO USAR como FLRW: outro ansatz, Ricci definido à mão

## Buscas
{
  "timestamp": "2026-09-14T15:06:33.880683-03:00",
  "searches": [
    {
      "label": "01_kernel",
      "command": [
        "rg",
        "-n",
        "FLRW|Friedmann|friedmann|flrw|scaleFactor|scale_factor",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
        "-g",
        "*.lean",
        "-g",
        "!**/.lake/**"
      ],
      "returncode": 0,
      "stdout_bytes": 416,
      "stderr_bytes": 0
    },
    {
      "label": "02_notes",
      "command": [
        "rg",
        "-n",
        "FLRW|Friedmann|friedmann|flrw|scaleFactor|scale_factor",
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
        "FLRW|Friedmann|friedmann|flrw|scaleFactor|scale_factor",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT",
        "-g",
        "*.md"
      ],
      "returncode": 1,
      "stdout_bytes": 0,
      "stderr_bytes": 0
    },
    {
      "label": "03_workbenches",
      "command": [
        "rg",
        "-l",
        "FLRW|Friedmann|friedmann|flrw|scaleFactor|scale_factor",
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
      "stdout_bytes": 127,
      "stderr_bytes": 0
    },
    {
      "label": "04_tree",
      "command": [
        "rg",
        "-n",
        "FLRW|Friedmann|friedmann|flrw|scaleFactor|scale_factor|Einstein|Clausius",
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
        "FLRW|Friedmann|friedmann|flrw|scaleFactor|scale_factor",
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
        "flrw_einstein|flrw_friedmann|leviCivitaField|coordinateRicci",
        "--max",
        "25",
        "--ctx",
        "120"
      ],
      "returncode": 0,
      "stdout_bytes": 84,
      "stderr_bytes": 0
    }
  ]
}

## Restrições e alcance
- A geometria é computada por definições gerais; componentes Ricci/Einstein não serão campos pressupostos.
- a é suave localmente sobre U, sem impor suavidade ou positividade fora da carta.
- A assinatura é eta4=(+---), conferida na inversa/congruência.
- Não escolher entre rotas cosmológicas, modificar D1 ou reabrir A1.
- B2 não introduz beta, nem parâmetro empírico. eta/G continuam INPUT.
- Módulos pretendidos: FLRWGeometry para componentes; FLRWFieldEquations para consumidor geral, Friedmann e conservação. Lemas auxiliares só se consumidos.
- Buscar.py não retornou ocorrências dos nomes/tipos consultados; é limitação do índice, não prova de ausência de toda a literatura.

2026-09-14T15:10:25.874366-03:00
