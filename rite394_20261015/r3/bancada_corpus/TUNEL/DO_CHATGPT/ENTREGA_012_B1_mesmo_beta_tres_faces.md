[REAL — B1 pago no módulo compilado e revisto; incorporação ao um.py cabe à gerência. B2–B6 e A1(b) não quitados.]

# ENTREGA 012 / B1 — o mesmo β nas faces de ângulo, custo e fundo

2026-09-14T15:26:34.131383-03:00

`TGLExt.the_same_beta_reads_three_faces` reúne a reflexão da matriz-S, a forma do custo, as duas identidades de fundo e a taxa de vazamento sobre a MESMA projeção `c.beta`. A estrutura tem apenas β e as provas de 0<β<1. α é definida como β/exp(1/2); sua positividade, seu limite superior e as duas escritas do custo são demonstrados. Não há campo que assuma reflexão, fundo ou vazamento.

Foram compilados 8 teoremas novos, uma estrutura e uma definição. É uma ligação de fornecedores pagos, sem reconstrução deles. **A identidade do custo é uma normalização de forma autorizada por B1; não é dedução do valor de α nem de CODATA.** A reflexão mede β como probabilidade, com amplitude √β. O ângulo lê o acoplamento e não entra no motor cosmológico.

## Critérios da ORDEM 012

| Critério B1 | Resultado e evidência |
|---|---|
| Ficha antes do código | PAGO — MD/JSON anexados; revisão confrontou fontes, linhas e timestamps. |
| Um termo, β real em (0,1) | PAGO — `TGLExt.TGLCoupling`, sem outro escalar de entrada. |
| (i) Reflexão em thetaMiguel β igual a β | PAGO — `TGLExt.TGLCoupling.reflection_weight`, especialização de `the_pruning_threshold_is_the_reflection_amplitude` + `Real.sq_sqrt`. |
| (ii) Forma β=α·exp(1/2), 0<α<1, radical | PAGO — `alpha_pos`, `alpha_lt_one`, `beta_eq_alpha_exp`, `beta_eq_alpha_radical`; reusa `boundary_extracts_the_radical` e `the_minimal_volume_exceeds_one`. |
| (iii) closure_identity e hubble_form no mesmo β | PAGO — aplicações literais na síntese; não se reprovam identidades de anel. |
| (iv) Taxa de vazamento no mesmo β | PAGO — perda estrita com t,g>0 e unicidade sob igualdade dos semigrupos para todo tempo; reusa NoFullWitness. |
| Nenhum numeral atribuído a β/α | PAGO — ambos variáveis/leituras; 0 e 1 limitam o domínio, 1/2 é o expoente e 4/3 vem do fluido já formalizado. |
| Axiomas no trio | PAGO — os dez alvos auditados na cópia do autor e na raiz independente. |
| lake build isolado | PAGO — projeto sem objetos TGL/TGLExt herdados; `lake build` produz a cadeia de dependências e o auditor. Reprodução independente também sem objetos de projeto do autor. |
| Consumidor nomeado | PAGO — proposta `ext_same_beta_reads_three_faces_kernel_proved → TGLExt.the_same_beta_reads_three_faces`; âncoras e hipótese D1 na ficha. Instalação pela gerência ainda não realizada. |

## Alcance e controles

`reflection_rejects_bare_alpha` prova que omitir o custo altera a reflexão. Duas sondas deliberadamente adulteradas foram efetivamente recusadas por incompatibilidade de tipo: `BadReflection.lean` troca β por α na reflexão; `BadCost.lean` remove exp(1/2). Importação e infraestrutura funcionaram: as recusas são de prova, com logs preservados.

As cláusulas de fundo ainda não contêm H, derivadas ou Einstein; a equação métrica pertence a B2–B4. A última cláusula identifica taxas de semigrupos iguais; não seleciona um β numérico nem identifica β separado de um gap desconhecido. Não há nova dinâmica, teste D1, seleção natural, escolha entre rotas, fechamento global, demonstração de G ou mudança de gate.

## Build, procedência e revisão

Build autoral: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_145521_664130\run.json`. Revisão: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\r\compilation.json`. P0/P1/P2 da revisão: 0/0/0 no escopo B1. A revisão verificou tipo, fonte, hipóteses, ficha e compilou fonte/auditores numa raiz própria. A gerência ainda fará sua auditoria de incorporação.

Mathlib e os outros oito pacotes são caches copiados, com revisões confrontadas ao manifesto; não foram reconstruídos a partir de Lean fonte nesta rodada. A toolchain é Lean4.31.0 instalada. Não há olean de projeto canônico reaproveitado: os fornecedores TGL/TGLExt do alvo foram reconstruídos por Lake. Avisos de linters dos fornecedores antigos permanecem nos logs e não foram corrigidos nesta entrega.

A leitura estática do dicionário embutido contou 941 chaves, sem duplicação; `lake-manifest.json` foi copiado separadamente (942 arquivos de configuração/fontes na raiz preparada antes dos dois novos). Essa contagem está discriminada em `PROVENIENCIA_B1.json`, sem transformar o número declarado na ordem em medição. Cópia do monólito e 941 fontes conferidas novamente sem alteração pela auditoria; o monólito não foi importado nem executado.

## Reprodução nesta máquina

Na raiz `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA`:

```powershell
& 'C:\Python314\python.exe' -X utf8 -B '.\run_lake.py' TGLExt.TheSameBetaReadsThreeFaces TGLExt.AuditSameBeta
```

O script chama a toolchain fixa e `lake build` no diretório kernel, retira LEAN_PATH externo e grava cada tentativa em pasta nova. Para ver os axiomas diretamente, no diretório kernel:

```powershell
& 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe' env lean TGLExt/AuditSameBeta.lean
```

As duas sondas em `probes/` devem devolver saída diferente de zero sob `lake env lean ../probes/BadReflection.lean` e `lake env lean ../probes/BadCost.lean`. Logs reais: os caminhos estão em `AUDITORIA_B1.json`. Não há teste empírico nesta reprodução.

## Axiomas, nomes completos

| Alvo | Lista medida |
|---|---|
| `TGLExt.TGLCoupling` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.alpha` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.alpha_pos` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.alpha_lt_one` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.beta_eq_alpha_exp` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.beta_eq_alpha_radical` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.reflection_weight` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.reflection_cost` | propext, Classical.choice, Quot.sound |
| `TGLExt.TGLCoupling.reflection_rejects_bare_alpha` | propext, Classical.choice, Quot.sound |
| `TGLExt.the_same_beta_reads_three_faces` | propext, Classical.choice, Quot.sound |

## Arquivos

| Arquivo | SHA256 lido |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheSameBetaReadsThreeFaces.lean` | `2efd8b379f210111e0383d9c40e5fc72835f41cd94aad2dd70d645d66f400c16` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AuditSameBeta.lean` | `82ef806ff2a568cd1cc29f710b79f589b31ff0d6aa0f9122d92af73127704dd3` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B1.md` | `96f714483950aab877024f67d67303c0bfb6d96721b782f4fcf8bdebb6672190` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B1.json` | `8cf82a69a3f7aed1f82fbd2a9263cb1f4784e56be8cd3a5a71d886543e10845f` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\AUDITORIA_B1.json` | `8e8566d76dad232d421391f4e3118ef7ac1a1c41885acd81188b1d00301cbcd4` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\PROVENIENCIA_B1.json` | `dc9b9bd2f8af248cfe2de2003c5d3090abed58f1b50e6102cea131f12305b6f8` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\CUSTODIA_V353_FONTES.json` | `97065a33aa44a2aa952889cf1b2173caf69c2fad0163d2b4550e5e217e009e8f` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\DEPENDENCIAS_LAKE_V353.json` | `c5e4b7794794f2bbd049ccbe4b9cb461f9bab6dcdb19acb7835650c6b568a2d1` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao\REVIEW_B1_FINAL.md` | `890dc58651cb5a0d51d418d0cc5542666afebb1c8088c2ed3bc4fa0dea6247e8` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao\REVIEW_B1_FINAL.json` | `46c54ffb2680abae12b3d96caa5bdffc1ae12db1fd93015465bc452021005446` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\r\compilation.json` | `58a2f96e065eb9b9660c2d49f5fb76483b3610cda3c52d274416bace880dd74a` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\r\run.json` | `720ca3fa2844b42a82bda5250bd84fbaccdfb0596f3239a7e3609b8f8dbc55da` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao\B1_BUILD_ROOT_REMAP.json` | `22931e6385fea4602144b54629f436028c10e619c7c497089fbcbdde23368b22` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\run_lake.py` | `4ab6c5ddcb8ab69ec91279cd72ac8eec4c2342984e62fbb6e9512b892bfdb951` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\audit_b1.py` | `5cd030ae91e052eeb2a0bdfdbfc5f1757abd26d84fa01d10a4710c603d84f706` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\deliver_b1.py` | `53ed24756066c3fe3338e2519d83ab27c35203a0ce0bc06b57f3543a2b1a3060` |

O manifesto `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\MANIFESTO_B1.json` e o recibo `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\RECIBO_B1.json` indexam também a tentativa autoral B1, sondas e fontes necessárias. As tentativas de B2 ficam fora da custódia de B1. Nenhuma tentativa falha foi apagada; as sondas negativas não são provas admitidas no módulo. A revisão preserva a tentativa em caminho longo que falhou ao localizar um arquivo de cache no Windows e registra a reprodução em raiz curta; essa falha de infraestrutura não é uma recusa matemática.

## Próximos alvos preservados

B2: calcular FLRW na conexão/métrica da casa e instanciar seu teorema geral. B3: continuidade por setor com H_nx nomeada. B4: duas rotas, diferença e fator de entalpia, com todas as condições de denominador e conservação explícitas. B5: reescrita pelo ângulo. B6: tabela de importados/inputs/abertos. A1(b) e os sete módulos pendentes da ORDEM011 retomam depois de B6.

## Ficha de aproveitamento anexada, sem reescrita

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
