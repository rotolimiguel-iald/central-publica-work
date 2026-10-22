[REAL / INPUT / OPEN] ENTREGA 008 ESPONTÂNEA — reconstrução tensorial condicional: o cone nulo determina A=fg e a conservação torna f constante em um domínio coordenado aberto preconexo.

05/09/2026. Continuação após a entrega 007, conforme o protocolo. Não responde a uma ordem 008 da gerência: essa ordem não estava no túnel ao publicar esta entrega. Pronta para auditoria independente; não altera gate ou conclusão física.

## Resultado e critérios desta continuação

| Critério | Estado | Evidência e limite |
|---|---|---|
| Derivação antes do código | PAGO | CONTINUACAO008_DERIVACAO_PREVIA.md. |
| Rigidez para tensores gerais | PAGO | lorentz_tensor_null_rigidity: matriz simétrica geral e contrato LorentzByCongruence; reutiliza o GeneralNullCone anterior. |
| Métrica e inversa do referencial | PAGO com referencial como INPUT | g=EᵀηE, g⁻¹=DηDᵀ; as duas identidades de inversão são teoremas. η não foi derivada. |
| Conexão de Levi-Civita | PAGO na carta | Fórmula construída das derivadas de g, torção zero e compatibilidade provadas. |
| Derivadas genuínas | PAGO | fderiv, regra do produto e igualdade local em aberto; hipóteses de diferenciabilidade explícitas. |
| Coeficiente produzido | PAGO | f=(DᵀAD)₀₀, A=fg e diferenciabilidade de f provadas. |
| Conservação ⇒ constante | PAGO | div(fg)=df; derivada zero e preconexão dão f constante. |
| G+Λg=κT | PAGO como implicação | G,T simétricos diferenciáveis conservados; diferença anula o cone nulo. Λ é constante. G é um campo do enunciado, não o tensor de Einstein já construído. |
| Controle sem conservação | PAGO | A(x)=x⁰η anula o cone, tem coeficiente não constante e divergência temporal 1. |
| Curvatura/Bianchi gerais | NÃO PAGO | Construir Ric, R, G geométrico e provar conservação. |
| Hipótese nula da dinâmica/horizontes | NÃO PAGO | Clausius/Raychaudhuri e H3 não foram produzidos. |
| Globalização e origem do referencial | NÃO PAGO | Colagem de cartas, quatro canais e assinatura derivada permanecem abertos. |

São 8 módulos novos e 42 teoremas novos, contados nos fontes. Todos os teoremas têm #print axioms e compilação limpa para os hashes finais. As definições auxiliares não impressas individualmente são listadas no manifesto; as provas que as usam têm suas dependências axiomáticas verificadas.

## Reprodução

```powershell
& 'C:\Python314\python.exe' 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation008.py'
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module TensorNullCone
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module MetricCompatibleJet
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module CovariantScalarConservation
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module MetricFieldConnection
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module LorentzMetricField
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module TensorFieldLinearity
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeneralTensorReconstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module TensorReconstructionControls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

Os comandos recompilam os módulos novos usando as dependências locais já presentes. O manifesto registra a ordem de compilação dos fontes da bancada e os oleans locais; o ambiente externo Lean/mathlib não é um pacote portátil. A auditoria de bytes não substitui a recompilação independente da gerência.

## Axiomas impressos

```text
ChatgptAudit.tensorQuad_single: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorQuad_single_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.symmetric_tensor_ext: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorQuad_congruence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorQuad_eta: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorQuad_components: [propext, Classical.choice, Quot.sound]
ChatgptAudit.minkowski_tensor_null_rigidity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.congruence_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.congruence_undo: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lorentz_tensor_null_rigidity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lower_christoffel_metric_identity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.levi_civita_jet_metric_compatible: [propext, Classical.choice, Quot.sound]
ChatgptAudit.levi_civita_jet_torsion_free: [propext, Classical.choice, Quot.sound]
ChatgptAudit.covariant_pure_trace_jet: [propext, Classical.choice, Quot.sound]
ChatgptAudit.divergence_pure_trace_jet: [propext, Classical.choice, Quot.sound]
ChatgptAudit.coordinatePartial_mul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldJet_smul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldJet_congr_on: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldDivergence_congr_on: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldJet_symmetric_on: [propext, Classical.choice, Quot.sound]
ChatgptAudit.partials_zero_implies_fderiv_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.pure_trace_field_divergence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.conserved_pure_trace_is_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.inverse_symmetric_of_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.levi_civita_field_metric_compatible: [propext, Classical.choice, Quot.sound]
ChatgptAudit.levi_civita_field_torsion_free: [propext, Classical.choice, Quot.sound]
ChatgptAudit.levi_civita_conserved_scalar_is_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.frame_metric_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.inverse_frame_metric_left: [propext, Classical.choice, Quot.sound]
ChatgptAudit.inverse_frame_metric_right: [propext, Classical.choice, Quot.sound]
ChatgptAudit.frame_metric_differentiableOn: [propext, Classical.choice, Quot.sound]
ChatgptAudit.frame_scalar_differentiableOn: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_tensor_eq_frame_scalar: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldJet_sub: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldJet_const_smul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldDivergence_sub: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensorFieldDivergence_const_smul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.conserved_null_tensor_is_constant_metric_multiple: [propext, Classical.choice, Quot.sound]
ChatgptAudit.conserved_null_balance_has_constant_term: [propext, Classical.choice, Quot.sound]
ChatgptAudit.linear_trace_annihilates_null_cone: [propext, Classical.choice, Quot.sound]
ChatgptAudit.linear_trace_has_no_constant_coefficient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.linear_trace_divergence: [propext, Classical.choice, Quot.sound]
```

## Arquivos e hashes dos bytes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO008_MANIFESTO.json` — SHA256 `1e504255715fa2600a9d29f318cb94e17d7401b10abd1ef215cfe74687610b41`.
O manifesto contém 359 registros com caminho absoluto, tamanho e SHA256. Os valores desta tabela são lidos dos arquivos pelo script.

| Artefato | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation008.py` | `98982addaa605b16c83085816de8d8e6013b16c4eb485d414b817222c031094d` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO008_DERIVACAO_PREVIA.md` | `70412d1899db75c77d53fb25d8d5447a6dbd5c19ae0a0e587a229bff7b52bb8c` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO008_PARECER.md` | `ede6da394a8681721e2badb234380611a8a6cb72c81507b7905c0bdf349f81ed` |
| `C:\IALD\Central de Patentes\Chatgpt\CovariantScalarConservation.20260905_203106.log` | `b87b6e46f63c083184f5cf6d60b348832b97f531dff85adba08d12e920ebead1` |
| `C:\IALD\Central de Patentes\Chatgpt\CovariantScalarConservation.lean` | `8b48e479208a90a78db00a9662c3434759f7f63c2d3ac1f02b923ad2f055c39e` |
| `C:\IALD\Central de Patentes\Chatgpt\GeneralTensorReconstruction.20260905_203804.log` | `5889ba01d4f63882da7777f8c98105a3519593ac76292a6a7a44601838b7fa9d` |
| `C:\IALD\Central de Patentes\Chatgpt\GeneralTensorReconstruction.lean` | `bbd44524c2ed31f9e784f26c49d230d587b0647a1e484bd0f3d11a6d42a95ec3` |
| `C:\IALD\Central de Patentes\Chatgpt\LorentzMetricField.20260905_203306.log` | `07065db19d22572d32ba8d18891ba5ef13aa4c0592b65b3dc387baef50b2c1a1` |
| `C:\IALD\Central de Patentes\Chatgpt\LorentzMetricField.lean` | `419126429ddbde879c61388c5ae85000786789e0f7af1c1e187e7e71af310bdc` |
| `C:\IALD\Central de Patentes\Chatgpt\MetricCompatibleJet.20260905_202216.log` | `4167fdedaac71c1be73cf8b659949285192aaad272f8b47497932a9f367a431e` |
| `C:\IALD\Central de Patentes\Chatgpt\MetricCompatibleJet.lean` | `813ff241c57fce71e743bb27c53c13d9c44f92cc9531c21aca8e629d0f71a22c` |
| `C:\IALD\Central de Patentes\Chatgpt\MetricFieldConnection.20260905_203252.log` | `1b20faad03e483ecd7faf8a89f731afe949777b3f0bf0e3942f6631e5fd2cdad` |
| `C:\IALD\Central de Patentes\Chatgpt\MetricFieldConnection.lean` | `a4c975605bf90abc5ea58f415370846c9693eca686d1403d87911e391d7a45ff` |
| `C:\IALD\Central de Patentes\Chatgpt\TensorFieldLinearity.20260905_203538.log` | `e3e970984ff114f0c1e9f3f96580e11528ba07404cf133eb43b9e4440db8edbd` |
| `C:\IALD\Central de Patentes\Chatgpt\TensorFieldLinearity.lean` | `7885f27d9ec7260085b0d50e9d9e01518f0d6033537da1f60a9406d980ec2244` |
| `C:\IALD\Central de Patentes\Chatgpt\TensorNullCone.20260905_202535.log` | `e7ce8d75ff61e9ab2ead2d8f35a05693d16cf38c11dd89defecc84bc322577a5` |
| `C:\IALD\Central de Patentes\Chatgpt\TensorNullCone.lean` | `382271c81604fb057d60c27c3699c30cc0bb247fdc368b87940c47ff3558fcad` |
| `C:\IALD\Central de Patentes\Chatgpt\TensorReconstructionControls.20260905_204016.log` | `cdf538b0d07e5501af317dce7b699e37b2a3a82447d4029d7863a282d8f52c0b` |
| `C:\IALD\Central de Patentes\Chatgpt\TensorReconstructionControls.lean` | `a50e6a7cc4a19f8a79609d33e023e67a093a8393d793fab4d812febd8c8eec76` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\TensorNullCone.20260905_202013.failed_compile.log`: cópia de bytes do log, exit code 1; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\TensorNullCone.20260905_202248.rejected_warning.log`: cópia de bytes do log, exit code 0; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\CovariantScalarConservation.20260905_202519.failed_compile.log`: cópia de bytes do log, exit code 1; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\CovariantScalarConservation.20260905_202941.failed_compile.log`: cópia de bytes do log, exit code 1; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\GeneralTensorReconstruction.20260905_203625.failed_compile.log`: cópia de bytes do log, exit code 1; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\TensorReconstructionControls.20260905_203818.failed_compile.log`: cópia de bytes do log, exit code 1; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.

## O alcance que continua aberto

O parecer detalha as hipóteses e os passos pagos. Assinatura, referencial e condição nula são entradas; G ainda não foi identificado com Ric−½Rg; conservação de G/T não foi obtida de Bianchi/dinâmica. O resultado cobre uma carta, não uma variedade global já colada. A gravitação quântica em sentido amplo permanece aberta.

Escritas somente em Chatgpt. Nenhum um.py executado/importado/editado; nenhum kernel canônico, Atlas, memória, selo ou gate alterado. As entregas 006 e 007 permanecem intactas. Nenhum dado observacional foi buscado.

A gerência audita antes de incorporar e atualiza as superfícies da casa quando houver incorporação. A confirmação física não é consequência desta entrega matemática.
