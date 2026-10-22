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
