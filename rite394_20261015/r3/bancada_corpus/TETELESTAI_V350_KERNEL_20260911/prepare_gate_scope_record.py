"""Prepare reviewable traceability and the corrected work contract, without edits to um.py."""
from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'AUDITORIA_REUSO_GATE_20260913'
gate = json.loads((OUT/'gate_evidence.json').read_bytes())
reuse = json.loads((OUT/'external_source_reuse.json').read_bytes())
now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def create(p, raw):
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and raw
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(raw)
    assert t.read_bytes()==raw
    t.replace(p)

rows=[]
for x in gate['entries']:
    p=Path(x['source']['file'])
    rows.append('| `'+x['flag']+'` | `'+x['declaration']+'` | '+
                '['+p.name+'](<'+p.as_posix()+':'+str(x['source']['line'])+'>) | True |')
text=f'''# Gate v350: conjunto existente e correção de escopo

{now}. [REAL — inspeção do código, fontes e Audit existentes; execução isolada do gate por AST]

**Para o gate principal existente, não falta outra derivação matemática.** As seis
entradas formais e as cinco entradas físicas já são verdadeiras na evidência da v350
e no Audit incremental atual. Seus onze termos estão nas fontes embutidas. A função
principal já alcança o último dos quatro vereditos que implementa, usando o feed
experimental anteriormente registrado. Não se executou um novo experimento ou o monólito.

O desvio de trabalho identificado: tratar a construção adicional do peso/S/J original,
KMS e outras extensões como se fossem entradas ainda falsas do gate principal.
Elas não são lidas por `evaluate_quantum_gravity_closure`. Também é incorreto continuar
produzindo lemas para tentar mudar automaticamente o literal `full_plan_complete=False`
da subdecisão adicionada em `gate_extension.py`: esse literal não é um teste desses lemas.

## Ligação já existente, verificada entrada por entrada

`fonte Lean embutida → termo no Audit → mapa _QG_*_FLAGS → qgc_/qgp_ → gate`.
Cada linha abaixo teve localização única, hash de fonte lido, presença no Audit e
axiomas limitados a propext/Classical.choice/Quot.sound conferidos. A evidência é a
compilação incremental custodiada anterior; não se apresenta esta leitura como uma
recompilação de toda a biblioteca.

| Entrada | Termo consumido | Fonte | Valor |
|---|---|---|---|
{chr(10).join(rows)}

[Função principal](<{(ROOT/'um.py').as_posix()}:{gate['gate_source_line']}>).
[Mapas de termos consumidos](<{(ROOT/'um.py').as_posix()}:133899>).
[Evidência, hashes e controles](<{(OUT/'gate_evidence.json').as_posix()}>).

Onze ablações individuais fizeram o nível correspondente falhar. As 256 combinações
das oito entradas qgf_/gpf_, adicionadas aos dicionários recebidos pelo avaliador,
mantiveram o veredito principal. Isso mede sua independência no código; não muda
essas flags nem transforma hipótese de um contrato em prova de outro.

O campo `full_static_witness_exists=False` também não é um trabalho pendente: é
resultado deliberadamente constante do avaliador. Não há um quinto degrau secreto
que uma nova função auxiliar possa acender.

Os certificados físicos conservam seus enunciados e o alcance declarado no código.
Por exemplo, `qgPhysicsCertificate_anomaly` prova invariância de gauge do símbolo
de Ricci clássico-linear. A consolidação não muda esse enunciado para outro alcance.

## Reaproveitamento da outra pasta

Foram lidos {reuse['files_read']:,} caminhos Lean externos a esta pasta de trabalho,
com {reuse['distinct_byte_hashes']:,} hashes de bytes distintos e zero falhas de leitura.
{reuse['matching_paths']:,} caminhos correspondem a
{len(reuse['matching_embedded_files'])} módulos já embutidos na cópia do um.py.
Esses caminhos incluem cópias e revisões: não são milhares de provas independentes.

A comparação normaliza apenas CRLF, espaços das extremidades e texto anterior ao
primeiro import. Não demonstra equivalência semântica de fontes diferentes.
Também não declara inexistência de outras provas no acervo. O resultado positivo
relevante é que há material extenso já incorporado; deve ser consultado antes de
qualquer reconstrução.

[Inventário e correspondências](<{(OUT/'external_source_reuse.json').as_posix()}>).
O único grupo de candidatos por nomes de cota/bloco encontrado foi
`plus_block_eigenvalue_lower_bound`: seu enunciado recebe a cota matricial como
hipótese. Isso não é a cota do novo S original, mas esse novo S tampouco é requisito
do gate principal. Não se retoma essa derivação para responder à pergunta atual.

## Escopo ativo por ordem do operador

[INPUT] “vc só está ligando tudo ao mesmo conjunto probatório que é o um.py”.
Trabalho atual: consolidação, reaproveitamento, rastreabilidade e ligação efetiva
entre as provas existentes e o contrato consumido. Não reiniciar uma tentativa de
resolver gravidade quântica do zero nem inventar obrigações adicionais ao contrato.

Antes de acrescentar qualquer função de prova, exigir simultaneamente: uma entrada
específica do contrato solicitado, sua assinatura exata, a busca por fornecedor no
acervo e uma incompatibilidade concreta que impeça apenas ligar o fornecedor.
Se a entrada já está provada e consumida, reutilizar. Uma reserva de fronteira ou
um diagnóstico literal não autoriza reabrir uma entrada já satisfeita.

As fontes novas de energia produzidas antes desta correção ficam em DEV preservado:
quatro módulos/19 alvos com rc0 autoral; revisão independente parcial de 14;
`ScalarProjectionGap.lean` apenas escrito, nunca compilado. Nenhum desses cinco
módulos foi integrado ou será retomado automaticamente. Seus logs recusados ficam
preservados. A cópia integrada e o original não foram alterados nesta auditoria.

Memória deve carregar primeiro o contrato ativo e este mapa, usando registros antigos
como história. As antigas listas de OPEN não são automaticamente a próxima tarefa.
Os estados adicionais de fronteira permanecem com seu estatuto registrado.

## Estado da integração preservada

Working SHA256 `{gate['working_sha256']}`.
Mãe custodiada `{gate['parent_custody_sha256']}`.
Veredito principal relido e reproduzido pela função isolada:
`{gate['gate_result']['verdict']}`.

Este relatório é uma auditoria da ligação existente e uma correção do processo de
trabalho. Nenhuma alteração do gate, publicação, novo selo canônico ou execução
integral do um.py foi feita. A revisão independente da auditoria é registrada no
manifesto final, quando concluída.
'''
create(OUT/'MAPA_GATE_E_REAPROVEITAMENTO.md',text.encode('utf-8'))
contract={
 'timestamp':now,'status':'ACTIVE_USER_SCOPE__EXISTING_PROOF_INTEGRATION',
 'operator_instruction':'vc só está ligando tudo ao mesmo conjunto probatório que é o um.py',
 'objective':'Consolidar e ligar o conjunto probatório já existente ao contrato efetivamente consumido pelo um.py.',
 'principal_gate_existing_entries_verified':11,'principal_gate_missing_proof_inputs':[],
 'principal_gate_terminal_verdict_already_reached':True,
 'preserve_actual_theorem_statements_and_scope':True,
 'do_not_resume_original_S_expansion_automatically':True,
 'new_proof_requires':['specific_requested_contract_entry','exact_required_type',
                       'existing_corpus_provider_search','concrete_incompatibility_preventing_reuse'],
 'suspended_development_modules':['WeightedVariationalEnergy','ScalarWeightedEnergy',
   'ProjectionGapLowerBound','ProjectionGapEnergy','ScalarProjectionGap'],
 'suspended_modules_integrated':False,
 'frontier_flags_not_automatically_principal_gate_blockers':True,
 'read_first':str(OUT/'MAPA_GATE_E_REAPROVEITAMENTO.md'),
 'working_sha256':gate['working_sha256'],
 'canonical_source_readonly':True,'full_physical_claim_not_changed_by_this_contract':True}
create(ROOT/'CONTRATO_ATIVO_GATE_V350.json',json.dumps(contract,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'report':str(OUT/'MAPA_GATE_E_REAPROVEITAMENTO.md'),
 'active_contract':str(ROOT/'CONTRATO_ATIVO_GATE_V350.json'),'memories_not_yet_modified':True}))
