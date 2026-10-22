[REAL — B2 pago: FLRW compilado e revisto na maquinaria geométrica existente. Incorporação ao um.py permanece com a gerência.]

# ENTREGA 012 / B2 — FLRW na métrica da casa

2026-09-14T16:52:49.358362-03:00

Foram construídos **26 teoremas e seis definições** para a métrica espacialmente plana diag(1,−a²,−a²,−a²), assinatura (+---). A inversa é identificada com `metricInverse`; a conexão é a `leviCivitaField` dessa métrica; Ricci, Einstein e a divergência do fluido são calculados pelas definições gerais existentes.

O consumidor `ChatgptAudit.FLRW.flrw_friedmann_from_general_metric` aplica de fato `metric_only_einstein_equation`. Obtém uma constante Λ em U aberto preconexo e lê as equações FLRW. Nenhuma componente Ricci/Einstein ou equação de Friedmann foi colocada como campo de entrada dessa especialização.

## Critérios, um a um

| Critério B2 | Resultado |
|---|---|
| Ficha MD/JSON anterior ao código; fornecedores por tipo/linha/hash | PAGO; 24 localizadores conferidos pela revisão. Ficha integral anexa. |
| FLRW em Coordinate4/TensorField4, assinatura da casa | PAGO; `flrw_metric_lorentz`, `flrw_metric_inverse`, `flrw_connection`, `flrw_ricci`. |
| G00, Gii e componentes fora da diagonal | PAGO; `flrw_einstein_tensor` calcula matriz completa; leituras `flrw_einstein_00` e `flrw_einstein_spatial`. |
| Ricci no cone nulo | PAGO; `flrw_null_ricci`, para o mesmo g e a mesma conexão. |
| Primeira e segunda Friedmann, aceleração | PAGO; `flrw_friedmann_first`, `flrw_friedmann_second`, `flrw_acceleration`; hE é descarregada pelo consumidor geral. |
| Continuidade do fluido | PAGO; `flrw_stress_divergence` calcula as quatro componentes, `flrw_continuity` consome divergência temporal zero. |
| Instanciar Einstein/Clausius existente | PAGO; `flrw_friedmann_from_general_metric` aplica `metric_only_einstein_equation`, sem reconstruí-lo. |
| Coeficiente 8πG/3 | PAGO sob eta=1/(4G), G>0 [INPUT]; `flrw_newton_coefficient` usa `einstein_coefficient_from_clausius`. |
| Axiomas no trio | PAGO; 32 nomes, auditor autoral e auditor independente. |
| Lake em raiz isolada | PAGO; cadeia própria recompilada e segunda reprodução própria sem objetos de projeto autorais. |
| Revisão adversarial independente | PAGO no escopo B2; P0/P1/P2 = 0/0/0. Integração da gerência ainda não revisada. |

## Equações e hipóteses que permanecem

Com κ=2π/eta e convenção `G_tensor + Λ*g = κ*T`:

```text
H = a'/a
G00 = 3H²
Gii = -(2aa''+(a')²)  (i espacial)
Ric(k,k) = 2(H²-a''/a)(k0)²  se g(k,k)=0
H² = κρ/3 - Λ/3
a''/a = -κ(ρ+3p)/6 - Λ/3
H' = -κ(ρ+p)/2
ρ' + 3H(ρ+p) = 0
```

U é aberto e preconexo; a é suave e positiva nas coordenadas temporais de U. rho e pressão são diferenciáveis localmente. **H_null e H_conservation são hipóteses explícitas**. B2 não afirma que a torre ou a natureza as fornecem. Não se divide por H; H=0 não foi excluído. Lambda é existencial e não é automaticamente zero. A identificação com outra convenção física de Lambda exige explicitar o sinal. O teorema algébrico admite eta real com a divisão total de Lean; a leitura física de Newton usa G>0 e a calibração indicada.

Não há beta nesta etapa. B3 conecta setores conservados e o mesmo beta de B1 a estes fornecedores; B4 examina separadamente a importação termodinâmica. H3, G, o Lema3 global e o fechamento perturbativo não são quitados aqui. O monólito não foi executado/importado; não foram tocados gate, dados, workers, Atlas ou fontes canônicas.

## Reprodução, auditoria e procedência

Na bancada `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA`:

```powershell
& 'C:\Python314\python.exe' -X utf8 -B '.\run_b2_lake.py' TGLExt.FLRWFieldEquations TGLExt.AuditFLRW
```

O runner chama Lake4.31.0 na raiz kernel, remove LEAN_PATH/LEAN_SRC_PATH externos e preserva snapshots dos três arquivos FLRW em nova pasta. Run autoral aceito: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_162109_507348\run.json`; rc0, fontes inalteradas durante a execução.

Reprodução independente em `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\s`: primeiro `lake build TGLExt.GeneralMetricEinstein`; depois `lake build TGLExt.FLRWGeometry TGLExt.FLRWFieldEquations TGLExt.AuditFLRW TGLExt.ReviewFLRW`. Ambos rc0; 92 objetos de projeto construídos na raiz própria. Os três objetos novos coincidem byte a byte com os autorais. Os nove pacotes, incluindo Mathlib, são caches copiados e pinados; **não** houve reconstrução independente de Mathlib/toolchain. 59 avisos herdados de fornecedores, nenhum novo nos arquivos B2. O auditor próprio imprimiu tipos, universos e axiomas.

As duas sondas válidas (`probes_B2`) rejeitam por Type mismatch a troca 3→4 em G00 e a troca de sinal de Λ. Imports funcionam. A revisão leu os streams dessas sondas, sem afirmar reexecução delas. O autor relê os 941 arquivos-base e a cópia do um.py; a revisão não repetiu essa auditoria integral de preservação, e diz isso expressamente.

## Tentativas falhas preservadas

Compilações intermediárias falharam em especializações de derivadas/instâncias, avaliação de componentes e simplificação algébrica; não foram apagadas. A primeira rodada de sondas tinha erro lexical e foi **excluída** como controle matemático; os arquivos FAILED_SYNTAX e logs estão preservados ao lado da rodada corrigida. Preparação independente teve erro de encoding, interrupção e recusa Git por propriedade de diretório; retomada em cópia conferida, com safe.directory apenas no ambiente do processo. Por isso todas as compilações **aceitas** têm rc0, mas nem toda tentativa teve rc0.

O manifesto lista cada tentativa B2 selecionada por comando e seus hashes. Os primeiros runners nem sempre copiavam dependências editadas; não se reivindica snapshot completo de cada tentativa falha. A execução final aceita e a reprodução independente pinam os três arquivos finais integralmente.

## Axiomas por nome completo

| Alvo | Axiomas medidos |
|---|---|
| `ChatgptAudit.FLRW.flrwMetric` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrwInverse` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrwHubble` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_metric_lorentz` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_inverse_left` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_inverse_right` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_metric_inverse` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.coordinatePartial_time_function` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_metric_smooth` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_inverse_smooth` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_metric_jet` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrwConnectionForm` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrwConnection` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_connection` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_connection_form_jet` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_connection_form_ricci` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_ricci` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_einstein_tensor` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_einstein_00` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_einstein_spatial` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_null_ricci` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrwStress` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_stress_symmetric` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_stress_differentiable` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_stress_jet` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_stress_divergence` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_continuity` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_friedmann_first` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_acceleration` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_friedmann_second` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_friedmann_from_general_metric` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.flrw_newton_coefficient` | propext, Classical.choice, Quot.sound |

## Arquivos principais

| Arquivo | SHA256 lido |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWGeometry.lean` | `47aea5aebebd8611edab566724ce562508908dc86b96db7194dff2592bac9e92` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\FLRWFieldEquations.lean` | `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AuditFLRW.lean` | `db1f1b0f494bca195511cbb7316e8d504760b3508301674bfbee81113e990730` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B2.md` | `033433f7cfeed64f67bc1ae33cd505ac1db2f0f52f57fb5623afba0adf5c3f0d` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B2.json` | `a96139f9b8a4906c64040e464a8b7e28e0fb292aba93c61311d37b9b9d6ed8e4` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\AUDITORIA_B2.json` | `b34ac3c993f086261a421bf945625e9783c9029f8238edc99ac0ef7eda9ed4fc` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\ALVOS_B2.json` | `97455f1df343361ff01c8c1ecf1c18607b0e3c298f00e0d1c0fef29f744bcae7` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b2\REVIEW_B2_FINAL.md` | `beb3f1ed40f2b1c5911501a1cb948d21f5b21df6216c4e4450e65c7c7b747b21` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b2\REVIEW_B2_FINAL.json` | `5a7cdc4999b103315fd1266bc1b5e3be503ed842b3841612b578fd093320deac` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b2\compilation.json` | `7b7bb4682c3e7cfda77b1eb26bdf92860c820300f4bf5ddc51368fd8de2f9a5d` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\run_b2_lake.py` | `85fad57b20551c190a0d4e36c72b72b483a07cfbdcdd04491d3ba41c91b4687d` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\audit_b2.py` | `554145c34b85ce74534a9171455e6110ed630304d1ea4cfed91f004aac7013c3` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b2_audit.py` | `9dbc592d7171ef3a74d4e8dbe3d2f14134766b9cdb8b639666b57ac107f3339a` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\deliver_b2.py` | `4fe543033922847de273bcca45f3add06b8d4511a047111350452f4d91f33adb` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\CUSTODIA_V353_FONTES.json` | `97065a33aa44a2aa952889cf1b2173caf69c2fad0163d2b4550e5e217e009e8f` |

`MANIFESTO_B2.json` indexa também streams, objetos, revisões, runs e sondas. `RECIBO_B2.json` pina entrega e manifesto. Ambos ficam na bancada; a entrega fica na via de volta do túnel. Nenhuma entrada ext_* foi instalada no um.py: essa ação pertence à gerência, com a própria auditoria de integração.

## Ficha integral, preservada

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
