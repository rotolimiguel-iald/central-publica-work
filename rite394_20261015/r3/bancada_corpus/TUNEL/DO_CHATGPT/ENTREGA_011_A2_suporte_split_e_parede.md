[REAL — suporte, split, representante mínimo e canto construídos no core regular com o traço A1; OPEN — aceitação integral A2]

# A2 — o suporte finito já existe; a interface legada continua delimitada

Este marco constrói os objetos a partir de `SiteProfile P`, da representação regular e de `scalarInverseLimitTraceData P`. Nenhuma projeção finita, split ou testemunha completa é recebida como hipótese final. A contagem atual, após a poda P2-01, é de 33 declarações públicas em oito módulos. Os registros de 35 nomes pertencem ao lote anterior preservado.

## Critérios da ORDEM011 A2 e do adendo012

| Critério | Estado e fornecedor |
|---|---|
| Mesmo core regular e mesmo traço de A1 | PAGO: `regularCoreAlgebra P` e `scalarInverseLimitWeight P`; a tracialidade reutilizada é `scalarInverseLimitWeight_tracial` |
| Projeção não nula de traço positivo finito | PAGO: extração de minorante finito, corte por cálculo funcional e `scalarTrace_finite_subprojection_exists` |
| Duas faces ortogonais de traços iguais | PAGO: `scalarTrace_finite_equal_split`, pela relação a*a/aa* dentro do mesmo core |
| Suporte normalizado | PAGO: ação dual comum calibra τ(P_F)=1; não se redefine o traço. `scalarTrace_normalized_split_exists` e `regularFiniteSupport_trace` |
| Operador, domínio e afiliação | PAGO para o representante mínimo limitado H_min=1−P_F; grafo de domínio total, auto-adjunto, fechado e invariante sob o comutante |
| P_F é projeção espectral do zero | PAGO literalmente: `regularMinimalLock_spectral_zero` identifica a projeção ortogonal de ker(H_min) com P_F |
| Gap relativo | PAGO para H_min: ‖H_min x‖=‖x‖ no complemento ortogonal do núcleo. Não é gap global nem identificação com outro operador microscópico |
| Peso de Breuer do núcleo sem testemunha recebida | PAGO para H_min: `regularMinimalLock_breuer_kernel` dá τ_A1(projker H_min)=1, positivo e finito |
| Consumidor ContinuousCornerWitness | PAGO: `regularContinuousCorner`, com leitor concordante com A1 em TODOS os positivos; leituras normalizadas 1,½,½ |
| Termo exato de ThreeLocksCoreData a partir de A1 | NÃO PAGO: depende da interface total do traço em ContinuousCoreData, descrita abaixo |
| SusyRelativeData instanciado nesta realização | NÃO PAGO neste marco. Seu pacote reticular não foi substituído pelo modelo ENNReal, nem sua aceitação inferida apenas do nome do gap |
| FullWitness e bandeiras qgf/gpf/gpi | NÃO PAGO por este marco; nenhuma bandeira foi editada |

## Cadeia consumida

`A1 fiel + semifinito → minorante positivo finito → corte espectral → subprojeção sob e00 → par q, vq(vq)* → calibração dual → P_F e faces → H_min → núcleo, gap, grafo e canto`.

O sistema matricial de um sítio fornece e00 e v; isso não torna o Hilbert regular finito. A prova não toma a projeção de sítio, fixa pela ação dual, como se tivesse traço finito. Primeiro extrai uma subprojeção de traço finito, e só então constrói o split.

`CoreSupport` é reutilizado pelos lemas `hmin_selfadjoint`, `support_annihilates` e `support_maximal`. O construtor `threeLocksFromSupport` ainda exige o objeto `ContinuousCoreData` legado. A fonte `CoreSupport.lean` foi copiada sem alteração; os dez nomes auditados nela são fornecedores antigos, não dez teoremas novos deste marco.

## A parede exata do leitor

O traço A1 tem domínio `PositiveCoreInput P` e satisfaz a tracialidade quadrática τ(a*a)=τ(aa*), além das outras leis de traço positivo. O contrato legado tem `canonicalTrace : Core → ENNReal` e pede τ(xy)=τ(yx) para produtos arbitrários.

O leitor usado por `ContinuousCornerWitness` devolve A1 no cone positivo e zero fora dele. Ele satisfaz o contrato específico do canto, que usa projeções e split. **`positiveTraceReader_not_cyclic` prova que esse leitor NÃO satisfaz a ciclicidade global exigida pelo contrato legado.** A prova usa, no mesmo core, um par X,Y com XY positivo não nulo e YX não positivo. Não é erro numérico nem mera falha de compilação.

Essa parede refuta essa extensão por zero. Não prova que toda extensão total compatível seja impossível. Tampouco autoriza trocar silenciosamente a lei antiga pela quadrática. As alternativas formais a auditar são construir a extensão compatível exigida pelo legado, ou corrigir explicitamente a interface para o cone positivo e verificar seus consumidores. Nenhuma dessas alternativas foi implementada neste marco. Receber a extensão como hipótese e anunciar A2 concluído seria apenas transferir a obrigação para uma premissa.

Os dados da cunha não precisam ser reconstruídos: `theSpecificAQFTWitness` já está em `WedgeNet.lean`, e `towerWedgeData` em `V350WedgeModularData.lean`, para `mixProfile`. A leitura atual da fonte declara dados modulares mínimos; isso não é identificação geométrica BW. A pendência do traço total não deve ser descrita como ausência geral de W/D.

## Revisão, poda e limites dos controles

Carver revisou independentemente o lote congelado de 35 nomes, além de dez fornecedores antigos de CoreSupport, com nove controles negativos próprios e auditoria dos termos consumidores. Encontrou P2-01: duas especializações à unidade, sem consumidor matemático. O delta01 removeu apenas essas duas declarações, seus prints e entradas do Audit. Nenhum uso artificial ou bandeira foi criado para conservá-las.

As 33 declarações restantes conservam seus corpos de prova. A recompilação autoral do delta passou nos oito módulos e no Audit geral. O recibo independente do delta, ligado no manifesto desta entrega, determina o estado final da poda. Resultados anteriores permanecem históricos e não são apresentados como uma nova execução.

Os cinco controles autorais alteravam traço, gap, projeção do núcleo, ciclicidade e leitura de face. Foram recusados pelo Lean. O classificador inicial não reconhecia `'change' tactic failed` no caso GapTwo: sua correção documental preservou o relatório original e o log; não houve repetição inventada do teste. Os controles próprios do revisor incluem a impossibilidade de promover o gap relativo a global e um contraexemplo contra inferir traços iguais apenas da ortogonalidade.

## Reprodução

O manifesto liga cada fonte aos registros de compilação, aos objetos e aos logs. Reprodução DEV atual, usando somente os objetos de dependências já aceitos como cache, sem reexecutar preparadores:

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012'
$a2Modules = @('V354FiniteTraceSupport','V354SpectralThreshold','V354RegularMatrixCorner','V354FiniteEqualSplit','V354NormalizedSplit','V354RegularSupport','V354PositiveTraceReader','V354TraceReaderWall','AuditA2RegularSupport')
foreach ($a2Module in $a2Modules) {
    & 'C:\Python314\python.exe' -X utf8 -B .\dev_lean.py $a2Module
    if ($LASTEXITCODE -ne 0) { throw "Falha em $a2Module" }
}
```

`dev_lean.py` preserva fonte, comando, executável, stdout/stderr e rc em uma nova pasta de tentativa. Ele recusa sobrepor um módulo emprestado da base A1. Isso não substitui a raiz independente do revisor, cujos comandos também constam dos recibos. Lean é 4.31.0; Mathlib/pacotes externos são caches, não reconstrução integral nesta sessão. Os 33 nomes novos imprimem somente propext/Classical.choice/Quot.sound ou subconjunto. O aumento local de maxHeartbeats em SpectralThreshold responde a timeout de elaboração documentado; não é axioma nem resultado matemático.

## Preservação e incorporação

As tentativas falhas continuam em `attempts`; os cinco controles em `author_controls`; o lote35 e seus hashes nos recibos autorais e independentes originais; os backups imediatos em bytes junto às fontes alteradas. A ficha anterior ao código, `REAPROVEITAMENTO_A2.md/json`, é anexa por referência no manifesto.

Este é um marco parcial utilizável, com a parede tipada junto. A2 integral permanece OPEN. A construção não modifica `um.py`, D1, Atlas, memórias canônicas, selo ou kernel canônico. A gerência recebe os arquivos para auditoria e eventual incorporação; nenhum resultado cosmológico é usado para suprir um campo matemático.


## Recibo final do delta e arquivos

[REAL] Revisão independente do delta concluída: P0=0, P1=0, P2=0 neste delta; P2-01 quitado. Oito módulos matemáticos e dois auditores recompilados na raiz própria do revisor; os 33 nomes foram impressos por ambos os auditores. Isso não altera os itens NÃO PAGO da tabela.

- [V354FiniteTraceSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354FiniteTraceSupport.lean>) — 2 theorem, 0 def; SHA256 `7edd9fb4ef524e95b8c71d71bb7467512f9b89f7b04c21a5114686e894b1d323`.
- [V354SpectralThreshold.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354SpectralThreshold.lean>) — 2 theorem, 0 def; SHA256 `9c33191344d07e4947a6d78a23ca0fc17e6b75206c13c511219f3a7a3b65085d`.
- [V354RegularMatrixCorner.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354RegularMatrixCorner.lean>) — 1 theorem, 0 def; SHA256 `1f469df09c8ce12c58d7c8388dbedadb3fc9336a9c97757113693e7322e596f9`.
- [V354FiniteEqualSplit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354FiniteEqualSplit.lean>) — 2 theorem, 0 def; SHA256 `72876fa3cf13dbd947ab02f1f4bd378c8d0dc7b2ed9beb39d98d7bed8079552e`.
- [V354NormalizedSplit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354NormalizedSplit.lean>) — 2 theorem, 0 def; SHA256 `5e90a1c08de4dc4593e65d9b8dde4a4bd5a1e074b68f8be357d17d25bbebe91a`.
- [V354RegularSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354RegularSupport.lean>) — 14 theorem, 4 def; SHA256 `c80d99c73be4a676bcdc8cc21d476c249911d08f93fd914fda0d788019b1063e`.
- [V354PositiveTraceReader.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354PositiveTraceReader.lean>) — 3 theorem, 2 def; SHA256 `8133d88dcaf9ac3d58d739ecaf997312d7951be2c11fe1d08f21c8f90badf3ea`.
- [V354TraceReaderWall.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354TraceReaderWall.lean>) — 1 theorem, 0 def; SHA256 `7882c9df649971790dfa9545e802df5b2b4e31c8bc16d536cecfd4d64203efcc`.
- [REAPROVEITAMENTO_A2.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/REAPROVEITAMENTO_A2.md>) — SHA256 `55f8d295d8cfaabe255b97d481cea95440ead7d62d1dcdcd21fc22138cb87242`.
- [REAPROVEITAMENTO_A2.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/REAPROVEITAMENTO_A2.json>) — SHA256 `58decf1f0a88a183832f02e6e3a21c68b7e8ee2837e3e1aa6afa15339ec79eca`.
- [AUDIT_NAMES_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/AUDIT_NAMES_DELTA01.json>) — SHA256 `83aefa5ef0fd4646d039801f4a9af423fe306f17be42ad2bc32a34365a46f9ec`.
- [DELTA01_PODA.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/DELTA01_PODA.json>) — SHA256 `f47119ec2efacb17475450cdc3ae801282f793a7062b502d0eb34175b6a54ac9`.
- [RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/delta01_build/RESULT.json>) — SHA256 `b765360fa163428ae63df8db56a2c9daeef0e4b7d78221cd875e384006e5a381`.
- [AUDITORIA_A2_AUTORAL.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/AUDITORIA_A2_AUTORAL.json>) — SHA256 `c0406ff958a4f2e985e0e30fb109e87b9b092cf3f5a2cef8716f40343a25c696`.
- [SEMANTIC_RECLASSIFICATION.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/author_controls/20260915_125804_093873/SEMANTIC_RECLASSIFICATION.json>) — SHA256 `a9b73370d9dea826e21a28ae9ef3fbb18b32e2b31796ebf5419dc6613aafc836`.
- [PROVENIENCIA_CORE_SUPPORT.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/PROVENIENCIA_CORE_SUPPORT.json>) — SHA256 `c827ff7cd24387d18fdbc67045082aeb87bf65ed18b85e46fd63b25b18bf4dee`.
- [CoreSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGL/CoreSupport.lean>) — SHA256 `041fb863b07c3e0a167d5d0c8a522890d2da61586f41c27be2b06c46fac588e0`.
- [AuditA2RegularSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/AuditA2RegularSupport.lean>) — SHA256 `c35005716ff0a7c1186671aea32503466a306f37ba86d7c02b301b8c8b9290b3`.
- [dev_lean.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/dev_lean.py>) — SHA256 `6f36230af97a7321cd57a06fe3ec4c07d3590956b2cde8e688a7bc7a75a311de`.
- [ENTREGA_A2_CORPO.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/ENTREGA_A2_CORPO.md>) — SHA256 `798eaf0b49e1081ca9b5703f57cc04b28a97668f19031674f21bbd92156fb266`.
- [RECIBO_REVISAO_A2.md](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/RECIBO_REVISAO_A2.md>) — SHA256 `bc7f667cfe96f5380cc95e08e72fd8d94bc91aa6e048e109b3aacabe17c17dd4`.
- [AUDITORIA_A2_INDEPENDENTE.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/AUDITORIA_A2_INDEPENDENTE.json>) — SHA256 `8c5b419325b82a97a2d1ff2d658368cc159d8487a1032c4056a7edb768557206`.
- [SELO_A2.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/SELO_A2.json>) — SHA256 `07151fcf279899d7fbd2db955af6cfabcf290ed4974bf374076711e7df1312a9`.
- [RECIBO_REVISAO_A2_DELTA01_33.md](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/RECIBO_REVISAO_A2_DELTA01_33.md>) — SHA256 `c9cb0f6507ae7c1d5bac7c79983e5638844ddd1aeb0cc2383033ded4afae5985`.
- [AUDITORIA_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/AUDITORIA_DELTA01.json>) — SHA256 `c4091f3ef88044544bf01a9d4c1724990570d3589b19b305ec4974b44150ddb5`.
- [BUILD_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/BUILD_DELTA01.json>) — SHA256 `c044a30f8b457ce5b150a554cc41aa8d33e6adc944a672172673a755c7a9ae50`.
- [DELTA_COMPARISON.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/DELTA_COMPARISON.json>) — SHA256 `143ba089268b20830349e3a9f064a19699df23a4a80198d008bca95e9c32529f`.
- [INTEGRIDADE_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/INTEGRIDADE_DELTA01.json>) — SHA256 `ba8e1ef3dc612c9b6681cf6c41776a38d26fccd4356c58d598dacab17e9ff319`.
- [MANIFESTO_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/MANIFESTO_DELTA01.json>) — SHA256 `f469ae0fc3d2be1bbab21e3382f64ac6171faeddf477d69567a5f4100f8c8815`.
- [SELO_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/SELO_DELTA01.json>) — SHA256 `94ed880a9811c304b2f44d38560d2e9f6047a616c782a9595477e0b0ce1018ab`.

Manifesto: [ENTREGA_011_A2_suporte_split_e_parede_manifesto.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_011_A2_suporte_split_e_parede_manifesto.json>) — SHA256 `64cceabb76ef6359efd5ec3a338855a387f1c087b63204c65ab850411a0903b5`.
