[OPEN — ficha de aproveitamento escrita antes do código B1]

# B1 — o mesmo beta nas faces de ângulo, custo e fundo

O único dado escalar é beta em (0,1). Alpha é definida como beta/exp(1/2), sem escolha de valor. A relação do custo é uma identidade desta normalização, não a dedução de CODATA. O teorema de reflexão existente será especializado e sqrt(beta)^2 reduzido a beta. Os dois teoremas de fundo e as propriedades da taxa serão aplicados literalmente ao mesmo campo.

Consumidor proposto: `ext_same_beta_reads_three_faces_kernel_proved → TGLExt.the_same_beta_reads_three_faces` no mapa já existente. Âncoras atuais e linhas verificadas constam abaixo. A hipótese `background` do protocolo D1 é consumidor posterior via B2–B5: B1 paga a identidade do acoplamento, não a equação de Friedmann. A gerência fará a incorporação.

Decisão: ADAPTAR fornecedores; NOVO apenas o termo compartilhado e as pontes necessárias. Não há reconstrução dos fornecedores. Nenhum valor numérico beta/alpha, inferência física ou mudança de gate.

## Tipo exigido
```text
structure TGLExt.TGLCoupling: beta : Real; beta_pos : 0 < beta; beta_lt_one : beta < 1.
def TGLCoupling.alpha c := c.beta / Real.exp (1/2).
the_same_beta_reads_three_faces (c : TGLCoupling) (rho_r rho_m rho_Lambda : Real):
 normSq(Smat(thetaMiguel c.beta).mulVec e1 1)=c.beta AND
 (0<c.alpha AND c.alpha<1 AND c.beta=c.alpha*exp(1/2) AND c.beta=c.alpha*sqrt(exp 1)) AND
 closure_identity(c.beta,rho_r,rho_m,rho_Lambda) AND hubble_form(c.beta,rho_r,rho_m,rho_Lambda) AND
 (forall t gap, 0<t -> 0<gap -> exp(-(t*c.beta*gap))<1) AND
 (forall b, (forall t, exp(-(t*b))=exp(-(t*c.beta))) -> b=c.beta).
The references to closure_identity and hubble_form above abbreviate their full equality propositions, recorded verbatim in providers, not proof objects used as propositions.
```

## Consumidores verificados
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py:133180 — `"ext_nfw_rate_unique_kernel_proved": "TGLExt.leakage_rate_unique",`
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py:133716 — `"ext_rp_hubble_form_kernel_proved": "TGLExt.hubble_form",`
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py:133738 — `"ext_fh_boundary_radical_kernel_proved": "TGLExt.boundary_extracts_the_radical",`
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py:133864 — `"ext_vc_pruning_is_reflection_kernel_proved": "TGLExt.the_pruning_threshold_is_the_reflection_amplitude",`
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py:180955 — `def prove_d1_camb_protocol(ONE):`
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py:180969 — `"hypothesis": {"background": "H^2 = (8 pi G/3) rho_tot [1 + beta |1 + w_eff(z)|]", "beta_theory": "alpha sqrt(e) em runtime", "approximation_DECLARED": "CAMB em LCDM; TGL analitica por cima; r_s deslocado por H_LCDM/H_TGL em z_* (nao --tight-rs)"},`

## Fornecedores lidos

### TGLExt.thetaMiguel
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheVerbalCoupling.lean:126 · SHA256 `912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507`

```lean
def thetaMiguel (β : ℝ) : ℝ
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.sin_thetaMiguel
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheVerbalCoupling.lean:139 · SHA256 `912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507`

```lean
theorem sin_thetaMiguel {β : ℝ} (h0 : 0 ≤ β) (h1 : β ≤ 1) :
    Real.sin (thetaMiguel β) = Real.sqrt β
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.the_pruning_threshold_is_the_reflection_amplitude
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheVerbalCoupling.lean:155 · SHA256 `912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507`

```lean
theorem the_pruning_threshold_is_the_reflection_amplitude {β : ℝ}
    (h0 : 0 ≤ β) (h1 : β ≤ 1) :
    Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 1)
        = Real.sqrt β ^ 2
    ∧ Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 1)
        + Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 0) = 1
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.normSq_reflection
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\SMatrix.lean:241 · SHA256 `14f7e717a4ef70204eeb825d989e6dcc3397c274f1c45a3820420ea6af12a3b7`

```lean
theorem normSq_reflection (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 1) = Real.sin θ ^ 2
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.normSq_reflection_add_transmission
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\SMatrix.lean:254 · SHA256 `14f7e717a4ef70204eeb825d989e6dcc3397c274f1c45a3820420ea6af12a3b7`

```lean
theorem normSq_reflection_add_transmission (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 1)
      + Complex.normSq ((Smat θ).mulVec e1 0) = 1
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.boundary_extracts_the_radical
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheFiveHalves.lean:84 · SHA256 `456c66269b72d30fa10e38c427ec3194d985b46e04809233f2c42fe82495d7d1`

```lean
theorem boundary_extracts_the_radical :
    Real.sqrt (Real.exp 1) = Real.exp (1 / 2)
    ∧ Real.exp (1 / 2) * Real.exp (1 / 2) = Real.exp 1
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.the_minimal_volume_exceeds_one
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheGeometricCostOfAbsoluteZero.lean:52 · SHA256 `299ef10c96770aac933c3b65a5eef375684f32b12764824c8cb6622b05dbb61b`

```lean
theorem the_minimal_volume_exceeds_one : (1 : ℝ) < Real.exp (1 / 2)
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.closure_identity
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\RhoPlusPClosure.lean:52 · SHA256 `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6`

```lean
theorem closure_identity (β ρr ρm ρΛ : ℝ) :
    β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
      = β * ((4 / 3) * ρr + ρm)
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.hubble_form
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\RhoPlusPClosure.lean:58 · SHA256 `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6`

```lean
theorem hubble_form (β ρr ρm ρΛ : ℝ) :
    (ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
      = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.the_background_closure
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\RhoPlusPClosure.lean:90 · SHA256 `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6`

```lean
theorem the_background_closure (β ρr ρm ρΛ : ℝ) :
    (ρΛ + (-ρΛ) = 0)
    ∧ (β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
        = β * ((4 / 3) * ρr + ρm))
    ∧ ((ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
        = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ)
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.leakage_strictly_loses
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\NoFullWitness.lean:66 · SHA256 `fde4ca999c40e6892d1958bee15a066786adb1363b8e3514f41eeb8b8909a654`

```lean
theorem leakage_strictly_loses {t β g : ℝ} (ht : 0 < t) (hβ : 0 < β)
    (hg : 0 < g) : Real.exp (-(t * β * g)) < 1
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.beta_forbids_full_static_witness
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\NoFullWitness.lean:91 · SHA256 `fde4ca999c40e6892d1958bee15a066786adb1363b8e3514f41eeb8b8909a654`

```lean
theorem beta_forbids_full_static_witness {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x)
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

### TGLExt.leakage_rate_unique
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\NoFullWitness.lean:135 · SHA256 `fde4ca999c40e6892d1958bee15a066786adb1363b8e3514f41eeb8b8909a654`

```lean
theorem leakage_rate_unique {b₁ b₂ : ℝ}
    (h : ∀ t : ℝ, Real.exp (-(t * b₁)) = Real.exp (-(t * b₂))) : b₁ = b₂
```

EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2). Decisão: REUSAR/ADAPTAR, sem reprovar fornecedor.

## Buscas e limites
{
  "timestamp": "2026-09-14T14:52:36.247163-03:00",
  "searches": [
    {
      "label": "01_kernel",
      "command": [
        "rg",
        "-n",
        "the_same_beta_reads_three_faces|TGLCoupling|closure_identity|hubble_form|boundary_extracts_the_radical|leakage_rate_unique|sin_thetaMiguel",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
        "-g",
        "*.lean"
      ],
      "returncode": 0,
      "stdout_bytes": 3781,
      "stderr_bytes": 0
    },
    {
      "label": "02_notes",
      "command": [
        "rg",
        "-n",
        "the_same_beta_reads_three_faces|TGLCoupling|closure_identity|hubble_form|boundary_extracts_the_radical|leakage_rate_unique|sin_thetaMiguel",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911",
        "-g",
        "*.md",
        "-g",
        "!*.bak*",
        "-g",
        "!r/**",
        "-g",
        "!revisao/**"
      ],
      "returncode": 0,
      "stdout_bytes": 4698,
      "stderr_bytes": 0
    },
    {
      "label": "03_deliveries",
      "command": [
        "rg",
        "-n",
        "the_same_beta_reads_three_faces|TGLCoupling|closure_identity|hubble_form|boundary_extracts_the_radical|leakage_rate_unique|sin_thetaMiguel",
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
        "the_same_beta_reads_three_faces|TGLCoupling|closure_identity|hubble_form|boundary_extracts_the_radical|leakage_rate_unique|sin_thetaMiguel",
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
      "stdout_bytes": 80703,
      "stderr_bytes": 0
    },
    {
      "label": "04_tree",
      "command": [
        "rg",
        "-n",
        "^## 6|^### 6|RhoPlusP|ângulo|Friedmann",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\inputs\\A_PROVA_DA_QG_TGL_arvore.md"
      ],
      "returncode": 0,
      "stdout_bytes": 1120,
      "stderr_bytes": 0
    },
    {
      "label": "05_toe",
      "command": [
        "rg",
        "-n",
        "the_same_beta_reads_three_faces|TGLCoupling|closure_identity|hubble_form|boundary_extracts_the_radical|leakage_rate_unique|sin_thetaMiguel",
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
        "the_same_beta_reads_three_faces|TGLCoupling|sin_thetaMiguel|boundary_extracts_the_radical",
        "--max",
        "35",
        "--ctx",
        "150"
      ],
      "returncode": 0,
      "stdout_bytes": 19236,
      "stderr_bytes": 0
    }
  ]
}

- Definir alpha pelo custo é normalização de forma, não derivação do valor CODATA.
- Sem numeral atribuído a beta ou alpha; 0 e 1 são limites do domínio.
- Sem hipótese sin²θ=beta adicionada: é conclusão do fornecedor aplicado.
- Nenhum gate modificado.
- 941 entradas distintas lidas no dicionário embutido; ordem declara942. Números não equiparados silenciosamente.
- Pesquisa do acervo tem corte --max35; não demonstra exaustão das ocorrências. Busca canônica por tipo e nome é a prova de reaproveitamento local.

2026-09-14T14:53:59.863890-03:00
