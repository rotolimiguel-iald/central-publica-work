# Revisão independente da infraestrutura 053 — Newton

Estatuto: [REAL — leitura e verificações locais da infraestrutura]. Esta nota não é um selo, não declara BUILD_PASS do lote final e não substitui revisão matemática independente das novas provas.

## Objeto e procedimento

Foram lidos integralmente os trechos operacionais relevantes de `clean_continuation053.py` e `audit_continuation053.py`, comparados com as versões seladas 052. A sintaxe Python foi verificada por AST. Os hashes e tamanhos abaixo foram medidos diretamente dos bytes no momento desta emissão.

| Arquivo | Bytes | SHA256 |
|---|---:|---|
| clean_continuation053.py | 36534 | d5e989ffd5adc15618efd4bbc9c22d2f9b0184e14333730e6844799549e27e5b |
| audit_continuation053.py | 55392 | 1210bc9a310a7ba0b6e37332dfbffd109339e99d331b5c3a2fe25711f1e91d2d |

A correção posterior à primeira leitura foi conferida byte a byte contra os backups imediatos indicados abaixo. Em cada script, o arquivo atual é exatamente o backup após as duas substituições `PIN029_047_EXACT_BYTES → PIN029_052_EXACT_BYTES` e `pinned_in_manifest029_047 → pinned_in_manifest029_052`. Não houve alteração das guardas ou do algoritmo.

| Arquivo | Bytes | SHA256 |
|---|---:|---|
| clean_continuation053.py.bak_20260907_021651_157471 | 36534 | f7ce07e885a4bf3de7dd40bd4bf42fce6b1a7efa2b33b9a119add31d734a249b |
| audit_continuation053.py.bak_20260907_021651_157471 | 55392 | 6698f275eab318145b4d471562c4505829ebfd49f043bcf7ecefecc02d25f622 |

## Achados

1. **Cadeia histórica 052.** O runner inclui o manifesto052 e escolhe as fontes e os binários das quatro unidades a partir do diretório limpo registrado no marcador052; não utiliza os oleans homônimos da raiz como substitutos. O auditor reconstitui o conjunto e a ordem esperados, o namespace, a origem das fontes, os registros de compilação, o importador e a cobertura dos prints. Foi feita uma conferência independente por script somente de leitura: 4 fontes, 5 etapas, 94 teoremas, 17 definições, 0 instâncias e 27 evidências únicas, com bytes/hashes e crosslinks coerentes com o manifesto052. Isso verifica evidência histórica registrada; não recompila 052.

2. **Congelamento e escrita.** A infraestrutura exige derivação prévia geral, derivação de infraestrutura e derivações dos módulos selecionados. Todas as derivações053 e notas053 já existentes são capturadas no início. A união de custódia, fontes originais e copiadas, fronteira e importações externas diretas é congelada; há comparações antes/depois de cada compilação e no encerramento. Na sonda já concluída `CONTINUACAO053_DEVELOPMENT_20260907_051051_899427`, os sete documentos de derivação estavam presentes em snapshots idênticos antes/depois e continuavam com os mesmos bytes na leitura desta revisão. O runner cria diretórios exclusivos e usa temporário verificado antes da renomeação. Essa guarda atesta existência e estabilidade durante o build; não prova por si só a cronologia intelectual da derivação antes do código.

3. **Censo e saída Lean.** O censo reconhece declarações, estruturas e instâncias nomeadas separadamente, exige correspondência exata dos prints e recusa declarações não reconhecidas, duplicatas, instâncias anônimas, tokens proibidos e linters desligados. Apenas os axiomas `propext`, `Classical.choice` e `Quot.sound` são permitidos. O formato sem dependência de axiomas é aceito. Foram extraídas por AST somente as funções puras de análise dos dois scripts e exercitados, em memória, dez casos negativos por parser; todos foram recusados. Os controles cobriram print ausente, duplicado e extra; declaração privada não coberta, unsafe, instância anônima, declaração duplicada, sorry, linter desligado e #eval. Também foram conferidos o formato sem axiomas e a recusa de saída residual. Nenhum runner ou auditor integral foi acionado por esses controles.

4. **Ambiente e resolução.** O LEAN_PATH é limitado ao diretório novo, sua fronteira copiada e às bibliotecas externas declaradas. O auditor confere os caminhos resolvidos, incluindo junctions, a ordem topológica, a primeira resolução efetiva de cada importação e o vínculo entre fontes, logs, metadados e binários. Os inputs históricos sem proveniência individual de fonte são rotulados como leitura atual; nenhum vínculo geral fonte→olean é inventado. A fronteira transitiva externa de Mathlib/pacotes/toolchain permanece um limite explicitamente declarado, não uma recompilação exaustiva.

5. **Escopo científico.** Os campos do auditor mantêm a distinção entre formas no setor real autoadjunto e seu quociente algébrico por direções centralizantes, covariância por todos os TowerHorizon admitidos e densidades de Gram em pares fixos. A normalização comum de traço no primeiro par e a diferença de área no segundo par não são promovidas a área espacial ou total de uma órbita. O polarizador é um operador real limitado no Hilbert, sem pressupor que mapeie toda a álgebra de von Neumann em si. A escolha de horizonte/região físicos, escala dimensional, H3 e reconstrução gravitacional geral permanecem [OPEN]. A correspondência aqui conferida é entre o contrato documental e o objetivo053; a aprovação matemática dos módulos restantes depende de suas próprias revisões e da compilação final.

## Conclusão e limite desta revisão

O único achado na leitura inicial foi a nomenclatura legada de proveniência “029–047”; a correção estritamente nominal foi medida e confirmada. Não ficou identificada falha material nas guardas examinadas. O aceite desta infraestrutura permanece condicionado ao lote final real e à auditoria independente do seu marcador.

Nesta revisão não foram executados compilador, runner, auditor integral, --build-only ou --seal; não foi modificado arquivo existente. A única escrita é a criação exclusiva desta nota. A autoria de HorizonGNSImplementation pertence ao revisor Newton, portanto esta nota não constitui aprovação matemática independente desse módulo.

Emissão UTC: 2026-09-07T05:19:59.359444+00:00
