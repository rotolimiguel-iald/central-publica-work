[OPEN — ficha anterior ao código B4]

# B4 — termodinâmica explícita e diferença entre rotas

ADAPTAR dados termodinâmicos explícitos; NOVO o cálculo cosmológico e o teorema da diferença. As correções são teoremas de parede, não escolha de rota. Nenhuma nova camada Einstein.

## Tipo exato
```text
Natural units c=hbar=k_B=1; cpl:TGLCoupling; G>0, Phi>0, H>0.
Imported horizon data: radius=1/H, area=4*pi/H^2, temperature=H/(2*pi),
 qdot=area*(rho+p)*H*radius, sdot=Adot/(4*G*Phi), qdot=temperature*sdot.
Adot is the HasDerivAt derivative of 4*pi/(H(t)^2), not an assumed Einstein equation.
Then Hdot=-4*pi*G*Phi*(rho+p). Use the existing coefficient composition.
Literal errata flux without radius instead implies Hdot=-4*pi*G*Phi*H*(rho+p).
For constant w, Phi=1+cpl.beta*abs(1+w) is constant; continuity plus the derived
second equation yields HasDerivAt (H^2-(8*pi*G/3)*Phi*rho) 0 and an existential constant C
on an open connected time interval. H^2=(8*pi*G/3)*Phi*rho+C.
For variable Phi, use a primitive P(t) with P'=Phi*rho', yielding H^2=(8*pi*G/3)*P+C.
Derivative of H^2-(8*pi*G/3)*Phi*rho contains -(8*pi*G/3)*Phi'*rho;
derivative of S_BH/Phi contains -S_BH*Phi'/Phi^2 in addition to A'/(4G*Phi).
For finite sectors of B3 at t in I, R=sum rho_i>0, E=sum(1+w_i)*rho_i>=0,
 M2=sum(1+w_i)^2*rho_i, sectorEnthalpy=sum(1+beta*(1+w_i))*(rho_i+p_i):
 sectorEnthalpy-(1+beta*abs(1+wEff))*E=beta*(M2-E^2/R)>=0.
 M2-E^2/R=sum rho_i*((1+w_i)-E/R)^2;
 equality iff exists common w, forall i with rho_i>0, w_i=common w.
The criterion omitting vacuum sectors is false: positive matter plus vacuum is a typed counterexample.
Phi_flux=1+beta*M2/E is the unique scalar matching enthalpy-weighted closure if E!=0.
At E=0 uniqueness is not asserted; non-phantom sectors then have zero flux, allowing every factor.
For common w and E!=0, Phi_flux=1+beta*(1+w); equals 1+beta*abs(1+w) if 1+w>=0.
No route is selected and no empirical datum chooses an equation.
```

## Correções necessárias
- Fluxo: eq. (2.12) de Cai–Kim tem o fator raio aparente. A errata/ordem omitem esse raio e não produzem a segunda equação declarada. Serão provadas a consequência literal e a correção com raio.
- Entropia variável: S=A/(4G*Phi) não implica dS=dA/(4G*Phi) quando Phi varia. Tipar a lei diferencial como INPUT distinto, provar o termo ausente e o caso constante.
- Igualdade da variância: o suporte correto é rho_i>0, incluindo vácuo; o suporte rho_i+p_i!=0 pedido na ordem falha para matéria+vácuo. Provar contraexemplo e critério corrigido.
- Unicidade Phi_flux exige entalpia total diferente de zero. Sem isso a divisão não pode selecionar o fator.
- Constante cosmológica/integral permanece explícita, como em B2/B3. A primeira fórmula multiplicativa é a integração da rota setorial; não da rota total variável em geral.

## Consumidores
```json
[
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
  },
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

### HorizonEquilibriumData
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TriadMaster.lean:56 · SHA256 `64e0899e259693927b051493b8f20cc47885f183d02d79a8772e3b3d869863ae`
```lean
structure HorizonEquilibriumData
```
ADAPTAR dados explícitos; lei de área modificada não cabe no tipo de área original

### einstein_coefficient_from_clausius
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TriadMaster.lean:71 · SHA256 `64e0899e259693927b051493b8f20cc47885f183d02d79a8772e3b3d869863ae`
```lean
theorem einstein_coefficient_from_clausius (kappa a G : ℝ) (hG : G ≠ 0) :
    (kappa / (2 * Real.pi)) * (a / (4 * G)) = kappa * a / (8 * Real.pi * G)
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### horizon_clausius_composition
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TriadMaster.lean:79 · SHA256 `64e0899e259693927b051493b8f20cc47885f183d02d79a8772e3b3d869863ae`
```lean
theorem horizon_clausius_composition (kappa eta dA : ℝ) :
    (kappa / (2 * Real.pi)) * (eta * dA)
      = (kappa * eta / (2 * Real.pi)) * dA
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### EquilibriumInput
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:73 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
structure EquilibriumInput (A : Type) [Mul A] [One A]
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### discharge_by_import
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:129 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem discharge_by_import {H C : Prop} (h : H) (imported : H → C) : C
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### the_trio_is_a_pair
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:140 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem the_trio_is_a_pair {H1 H2 H3 P : Prop}
    (master : H1 ∧ H2 ∧ H3 → P) (imported : H2 → H3) :
    H1 ∧ H2 → P
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### enthalpy_eq
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean:43 · SHA256 `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3`
```lean
theorem enthalpy_eq (F : SectorFluid ι I H) (t : ℝ) :
    F.enthalpy t = F.totalRho t+F.totalPressure t
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### corrected_closure
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean:56 · SHA256 `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3`
```lean
theorem corrected_closure (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) :
    F.correctedTotalRho c t = F.totalRho t+c.beta*F.enthalpy t
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### effective_enthalpy
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean:105 · SHA256 `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3`
```lean
theorem effective_enthalpy (F : SectorFluid ι I H) (t : ℝ)
    (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.totalRho t*|1+F.wEff t| = F.enthalpy t
```
REUSAR tipos/implicações pertinentes; importação fica explícita

### multiplicative_closure
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean:115 · SHA256 `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3`
```lean
theorem multiplicative_closure (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.correctedTotalRho c t = F.totalRho t*(1+c.beta*|1+F.wEff t|)
```
REUSAR tipos/implicações pertinentes; importação fica explícita

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
REUSAR tipos/implicações pertinentes; importação fica explícita

### local_clausius_forces_ricci
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\LocalHorizonBalance.lean:74 · SHA256 `b3dcb033522681ba0aa1bb6b755370add8ba8741e632d5653a9ff2647957320a`
```lean
theorem local_clausius_forces_ricci (rate eta ricci : ℝ) (theta area matter : ℝ → ℝ)
    (hrate : rate≠0) (heta : eta≠0) (hA0 : area 0≠0)
    (htheta : HasDerivAt theta (-ricci) 0) (htheta0 : theta 0=0)
    (harea : ContinuousAt area 0) (hmatter : ContinuousAt matter 0)
    (hbalance : LocalClausiusPast rate eta theta area matter) :
    ricci=(2*Real.pi/eta)*matter 0
```
NÃO CASAR por nome: tela nula local, não horizonte FLRW

### IsOpen.exists_is_const_of_deriv_eq_zero
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\.lake\packages\mathlib\Mathlib\Analysis\Calculus\MeanValue.lean:761 · SHA256 `420a547519436730434abd02bdd5d5b667f27b8a0d266e84254cc631c77125cb`
```lean
theorem _root_.IsOpen.exists_is_const_of_deriv_eq_zero
    (hs : IsOpen s) (hs' : IsPreconnected s) (hf : DifferentiableOn 𝕜 f s)
    (hf' : s.EqOn (deriv f) 0) : ∃ a, ∀ x ∈ s, f x = a
```
REUSAR para integrar a diferença com derivada nula em intervalo aberto conexo

## Fontes externas e alcance
- [Cai & Kim (2005), JHEP 02 050](https://arxiv.org/html/hep-th/0501055): Raio aparente, fluxo com H*r_A, prescrição de temperatura e primeira lei; especialização plana r_A=1/H. Temperatura em horizonte dinâmico é prescrição da derivação, discutida após 2.21. `imported_into_witness:false`.
- [Jacobson (1995), PRL 75 1260](https://arxiv.org/abs/gr-qc/9504004): Termodinâmica local como motivação/importação; hipóteses locais adicionais não são provadas por um dado escalar FLRW. `imported_into_witness:false`.

## Buscas
```json
[
  {
    "timestamp": "2026-09-14T16:38:16.765566-03:00",
    "searches": [
      {
        "label": "01_kernel",
        "command": [
          "rg",
          "-n",
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 157066,
        "stderr_bytes": 0
      },
      {
        "label": "02_notes",
        "command": [
          "rg",
          "-n",
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius",
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
        "stdout_bytes": 3764,
        "stderr_bytes": 0
      },
      {
        "label": "03_deliveries",
        "command": [
          "rg",
          "-n",
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT",
          "-g",
          "*.md"
        ],
        "returncode": 0,
        "stdout_bytes": 28845,
        "stderr_bytes": 0
      },
      {
        "label": "03_workbenches",
        "command": [
          "rg",
          "-l",
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius",
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
        "stdout_bytes": 774528,
        "stderr_bytes": 0
      },
      {
        "label": "04_tree",
        "command": [
          "rg",
          "-n",
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius|Einstein|Clausius",
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
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius",
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
          "Cai.Kim|friedmann2_TGL|Phi_flux",
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
    "timestamp": "2026-09-14T16:39:19.423495-03:00",
    "searches": [
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius",
          "C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 254,
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
          "Cai.Kim|friedmann2_TGL|Phi_flux",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 0,
        "stdout_bytes": 4245,
        "stderr_bytes": 0
      }
    ]
  }
]
```

Pesquisa por nomes/tipos e leituras dos fornecedores pertinentes, não prova de ausência exaustiva. Regex variance também localiza invariance; esses homônimos não são fornecedores estatísticos.

Grupos: {"path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\BUSCAS_B4_GRUPOS.json", "sha256": "33d093a4faf7e4f8f66e77cc0b7abe290925c7298a23e6a3db9c00e449620bc4", "groups": 377, "files": 6205}

2026-09-14T16:43:22.535802-03:00
