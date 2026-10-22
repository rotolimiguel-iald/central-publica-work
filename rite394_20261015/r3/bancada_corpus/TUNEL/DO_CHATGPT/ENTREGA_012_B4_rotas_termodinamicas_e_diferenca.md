[REAL — B4 entregue com teoremas condicionais e paredes que corrigem quatro enunciados do contrato original. Contrato literal NÃO certificado; nenhuma rota escolhida.]

# ENTREGA 012 / B4 — rota termodinâmica, diferença e fator de fluxo

2026-09-14T17:14:36.487316-03:00

**22 teoremas, cinco definições e uma estrutura** foram compilados e reproduzidos por revisão independente. A revisão aceitou o resultado matemático com as correções obrigatórias abaixo. Não se atribui à literatura a entropia modificada da TGL; ela entra como hipótese nomeada.

## Critérios pagos e correções obrigatórias

| Critério | Estado e alcance |
|---|---|
| Ficha antes do código, fornecedores e seis modalidades de busca | PAGO; ficha integral ao final, MD/JSON preservados e 13 fornecedores conferidos. Buscas por variância também encontram invariância: esses homônimos não foram tratados como ponte. |
| Derivada real de A=4π/H² e Clausius | PAGO; hubble_area_derivative e HubbleHorizonInput, com H>0, G>0, Φ>0. A segunda equação não é campo dessa estrutura. |
| Segunda equação Ḣ=−4πGΦ(ρ+p) | PAGO para fluxo **A(ρ+p)H r_A**, r_A=1/H. **NÃO PAGO na escrita literal sem r_A**: radius_free_flux_consequence prova o fator H extra. |
| Entropia modificada | PAGO como entrada diferencial dS=dA/(4GΦ). **NÃO se identifica automaticamente com a derivada de S=A/(4GΦ(t))**; variable_entropy_derivative prova o termo adicional −AΦ'/(4GΦ²). |
| Primeira equação, w constante | PAGO: H²=(8πG/3)Φρ+C, com continuidade e C explícito. Não prova C=0. |
| Primeira equação, Φ variável | PAGO sob primitiva fornecida com derivada Φρ'; não se prova existência de uma primitiva para função arbitrária. H²=(8πG/3)P+C. O produto Φρ tem defeito de derivada −(8πG/3)Φ'ρ. |
| Diferença entre rotas | PAGO: diferença das fontes = β·variância≥0. Diferença de Ḣ = **−4πG** vezes essa expressão. |
| Critério de igualdade | PAGO com **suporte ρ_i>0**, incluindo vácuo. **Critério literal ρ_i+p_i≠0 é refutado** por um exemplo Fin2 matéria+vácuo. |
| Fator reconciliador único | PAGO com **entalpia total E≠0**. No fluxo zero zero_flux_has_no_unique_factor prova ¬∃! fator. |
| Fator comum quando w constante | PAGO sob suporte de densidade comum, E≠0 e 1+w≥0; a última hipótese permite a leitura absoluta. |
| Revisão e axiomas | PAGO DEV: 28 alvos no trio; Lake próprio rc0; sem P0–P2 ou avisos novos. Aceite de integração permanece com a gerência. |

## Cadeia e tipagem das entradas

HubbleHorizonInput contém H positivo/diferenciável, G/Φ positivos, taxa de entropia, taxa de calor, **differential_entropy**, **enthalpy_flux** e **clausius**. Usa calor com orientação δQ=−dE. Com T=H/(2π), r_A=1/H, a taxa de calor é A(ρ+p). A álgebra e a derivada de A produzem Ḣ=−4πGΦ(ρ+p); o coeficiente reutiliza einstein_coefficient_from_clausius.

O raio é parte da prescrição primária de [Cai–Kim, eq. 2.12](https://arxiv.org/html/hep-th/0501055). A correção diferencial Φ_TGL é INPUT da construção. Sua identificação com uma entropia de estado variável exigiria controlar o termo Φ' ou introduzir uma lei adicional explicitamente — nenhuma foi presumida. O fato de a primeira lei valer sob essas entradas não constrói H3 para a realização microscópica.

Para setores de B3, escreva R=Σρ_i, E=Σ(1+w_i)ρ_i e M₂=Σ(1+w_i)²ρ_i. Sob R>0 e E≥0:

```text
fonte setorial = E + β M₂
fonte total = (1+β|1+w_eff|)E = E + β E²/R
diferença = β(M₂−E²/R)
variância = Σρ_i[(1+w_i)−E/R]² ≥ 0
```

A diferença é zero exatamente quando todos os w_i de densidade positiva coincidem. Dois setores com ρ_m>0 e ρ_Λ>0, w_m=0 e w_Λ=−1, têm só um setor de fluxo não nulo, mas variância **ρ_mρ_Λ/(ρ_m+ρ_Λ)>0**. Esse contraexemplo tipado impede a implementação do critério incorreto da ordem.

Se E≠0, a solução única de fator·E=E+βM₂ é Φ_flux=1+βM₂/E. sector_clausius_matches_closed_rate aplica o teorema termodinâmico a esse fator e recupera a taxa setorial. Se E=0, ou nenhuma solução existe ou todos os fatores resolvem; não há unicidade. Estes resultados não escolhem a lei a usar no D1.

A integração usa intervalos/domínios abertos preconexos e a constância obtida de derivada zero. Sob w constante, a primitiva escolhida é Φρ. A constante C sobrevive; B3 também mantém Λ na equação 00 e exige H_zero_cosmological para eliminá-lo. **A hipótese de não-troca H_nx e w_i constante permanece de B3.** Escala G/η INPUT, Lema3 global OPEN, fechamento perturbativo TGL-S/TGL-L OPEN.

## Reprodução, controles e tentativas

Na bancada `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA`, o runner pinado run_b4_lake.py invoca `lake build TGLExt.ThermodynamicFriedmann TGLExt.SectorRouteComparison TGLExt.AuditThermodynamics` na raiz kernel. Run final: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_165527_813445\run.json`, rc0, fontes idênticas antes/depois. O auditor executa `lake env lean` no auditor e nas duas sondas: BadThermodynamicFactor omite Φ; BadVarianceSign troca o sinal da variância. Ambas falham por Type mismatch com imports funcionando.

Reprodução independente: `lake build TGLExt.ThermodynamicFriedmann TGLExt.SectorRouteComparison TGLExt.AuditThermodynamics TGLExt.ReviewThermodynamics` em s, run `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b4\independent_20260914_170247_181979\run.json`. Quatro objetos próprios novos; 113 objetos próprios anteriores preservados, 117 no total. Os três objetos do candidato coincidem com os autorais. **Nenhum olean de projeto autoral foi copiado.** Mathlib e oito pacotes auxiliares são caches herdados/pinados; não se alega recompilação desses componentes.

O revisor executou tipos e axiomas próprios e leu fontes/sondas autorais; não repetiu os negativos nem a varredura completa das 941 fontes-base. Esta preservação e a do um.py copiado foram medidas pelo auditor autoral, distinguindo os dois escopos. A revisão verificou o papel do raio em Cai–Kim. O inteiro original e o kernel canônico não foram executados ou escritos.

Tentativas intermediárias preservadas: provas de positividade, normalização da potência pontual e tática após meta fechada; builds positivos com avisos de ring/sum_mul dispensáveis foram substituídos pelo build final sem avisos novos. Todos os runs e snapshots pertinentes estão no manifesto. Falhas não foram apagadas nem contadas como controles adversariais.

## Axiomas medidos, nomes completos

| Alvo | Axiomas |
|---|---|
| `ChatgptAudit.FLRW.hubbleArea` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.entropyFactor` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.entropy_factor_pos` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.hubble_area_derivative` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.HubbleHorizonInput` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.modified_clausius_coefficient` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.tgl_second_friedmann_from_clausius` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.radius_free_flux_consequence` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.variable_entropy_derivative` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.tgl_first_friedmann_from_primitive` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.tgl_first_friedmann_constant_w` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.variable_factor_first_equation_defect` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.secondMoment` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.sectorVariance` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.fluxFactor` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.corrected_enthalpy` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.centered_variance` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.sector_variance_nonneg` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid.sector_variance_zero_iff` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_two_routes_differ` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_two_routes_equal_iff` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_two_hubble_rates_differ` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.sector_clausius_matches_closed_rate` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.common_w_flux_factor` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.zero_flux_has_no_unique_factor` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.matter_vacuum_variance` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.nonzero_flux_support_does_not_characterize_equality` | propext, Classical.choice, Quot.sound |

## Arquivos e hashes lidos

| Arquivo | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean` | `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorRouteComparison.lean` | `b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AuditThermodynamics.lean` | `0c75ce3985df5faa7b1f2fdabec3bbdd936a6d200607d60d1219f28ad7f2a392` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B4.md` | `b80a4df131a8297df890a2111d9550100a5fdeb2b2bf0a31caf4fd64dd2beca5` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B4.json` | `f24edc462dd131e52459d0b4a441a280e485155ef61513ae90c2ebefe23cdbc9` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\AUDITORIA_B4.json` | `a06c94d207091eb94907f2c08404cd4f9188ea1d0dfa22bd6c911277af52a7a5` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\ALVOS_B4.json` | `1a7793b3293c0cb6a1ef5e904c73cae11517ff835ea59b979f35119bf78a9819` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\BUSCAS_B4_GRUPOS.json` | `33d093a4faf7e4f8f66e77cc0b7abe290925c7298a23e6a3db9c00e449620bc4` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b4\REVIEW_B4_FINAL.md` | `cf3b91a3a1cd565d800002b8464b3bc89aa9c2eec28490bd98d6608c0da7e95b` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b4\REVIEW_B4_FINAL.json` | `bfe87230a0dd92621bbaef7ab6d833c344eba8a2f080158cc9a95c968612000a` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b4\compilation.json` | `094361aefa7cfe355ee45c1dd4d82b3c0133b9baceb147a4b1f2442bce5f0854` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\run_b4_lake.py` | `0e7ac351c40efc9e087599e872feb46a0d8f9f6e52fcc1bf117f36503151b7f7` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\audit_b4.py` | `1512d849f979854e4db91dd44f25e22098bfaea7b24d7fa2fddf5d40dd6aa1d6` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b4_ficha.py` | `c9af0cedae207c990ec2a216709f1fde0b16bc3dfa470246bc29c3364f14a0d9` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b4_audit.py` | `bdf003e76f71dc67216940403f3f526e2d4e2e2af169c51cfea4f1eb744cd4e2` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\deliver_b4.py` | `502a932e8889a9ff90bcd478c4a4db6b515fba6d955d9a4e46a1b937a4222a07` |

MANIFESTO_B4 e RECIBO_B4 na bancada vinculam os objetos, fontes, runs e revisão. A gerência integra os consumidores ext_* propostos na ficha **com estas correções**, sem remover hipóteses. Não foram alterados D1, gate, protocolos, originais, Atlas ou memórias; nenhuma escolha empírica foi feita.

## Ficha integral

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
