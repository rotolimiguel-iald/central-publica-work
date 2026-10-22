from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'square_resolvent_integrated_latest_run.txt').read_text().strip())
load=lambda p:json.loads(p.read_bytes())
hf=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
V=load(RUN/'verification.json');C=load(RUN/'compilation.json');M=load(RUN/'build_manifest.json');H=load(RUN/'helper_static_inspection.json');S=load(RUN/'static_verification.json')
assert V['complete'] and C['all_five_exit_zero'] and C['all_exact_targets'] and C['all_axioms_allowed'] and V['own_integrated_binaries_equal_author']
assert not any(V[p] for p in ['P0','P1','P2']) and not any(H[p] for p in ['P0','P1','P2'])
assert hf(REV/'REVIEW_SQUARE_RESOLVENT_DEV.md')==V['own_DEV_review_sha256']
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
table='\n'.join('| '+r['module']+' | '+str(r['returncode'])+' | '+str(r['seconds'])+' | '+str(r['distinct_axioms'])+' | igual |' for r in C['records'])
pins='\n\n'.join('**'+r['file']+'**\n\n- Fonte integrada: `'+r['source_sha256']+'`.\n- Binário próprio = autoral: `'+r['binary_sha256']+'`.' for r in V['new_records'] if r['file'].startswith('TGLExt/'))
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão integrada — resolventes, quadrados e teste do S original

{now} — **SQUARE_RESOLVENT_INTEGRATED_REVIEW**

**[REAL] Sem achados P0–P2 no delta integrado de três módulos/20 alvos.** Inspeção e cinco recompilações próprias concluídas, com a herança binária delimitada abaixo. O {link(REV/'REVIEW_SQUARE_RESOLVENT_DEV.md','parecer DEV20')} permanece byte a byte, SHA256 `{V['own_DEV_review_sha256']}`.

## Evidência própria e evidência autoral

As fontes integradas são exatamente os bytes DEV, com a única substituição `import TGLV350.` → `import TGLExt.V350`. Preservam os nomes, tipos e hipóteses conferidos no auditor DEV20. As raízes acrescentam somente os três imports e os 20 pedidos de axiomas; nenhuma declaração anterior foi retirada ou teve sua multiplicidade reduzida.

**[REAL — execução própria]** Executei Lean diretamente em árvore isolada de `revisao/`, sobre cópias dos três módulos integrados e das duas raízes. Todos os cinco binários resultantes são byte a byte iguais aos binários autorais finais.

| Módulo | rc | Segundos | Declarações impressas distintas | Binário |
|---|---:|---:|---:|---|
{table}

O Audit próprio contém exatamente **7106 declarações distintas**, todas com axiomas contidos em `propext`, `Classical.choice`, `Quot.sound`. Seu mapa coincide com o stream autoral corrente e com `axiom_report`; os **7086 alvos anteriores** permanecem iguais, e os **20 novos** coincidem com o manifesto e o auditor DEV próprio.

**Limitação de proveniência:** esta não foi uma reconstrução independente integral das dependências. A árvore congelou **897 módulos herdados**: 307 do cache próprio previamente pinado, 205 binários integrados da custódia mãe e 385 binários da base canônica, lidos e copiados sem alteração. Os 385 fontes adicionais conferem com o manifesto formal da base. Não havia cache próprio dos aliases integrados recentes `TGLExt.V350…`; não renomeei `.olean` DEV para simular essa proveniência. `LEAN_PATH` contém somente a árvore congelada e oito caminhos de pacotes externos readonly, sem caminho do build autoral. Fontes, binários herdados, companheiros e imports externos diretos permaneceram nos pins lidos. Pacotes e dependências antigas não foram recompilados. A correspondência fonte→binário herdada conserva, portanto, essa limitação.

**[REAL — inspeção de registros, sem reexecutar testes autorais]** Foram relidos os **216 pares fonte/binário**, os JSON de compilação e seus streams: **211 registros idênticos aos da mãe e cinco novos**, estes com fonte inalterada durante compilação. As dependências diretas dos cinco novos são anteriores aos outputs. Os **106/106 controles** do autor estão registrados como aprovados; preservam os 105 anteriores e acrescentam `rational_squares_and_original_adjoint_test_does_not_discharge_KMS_trace_or_physical_frontier`.

## Integração, fiação e custódia ainda não gravada

- Cópia lida: `{V['working_sha256']}`; **918 embutidos**, batch **749**.
- Mãe `bidual_right_support_custody.json`: `{V['parent_custody_sha256']}`.
- Original canônico e cópia-base relidos somente por hash: `{V['original_sha256']}`.
- AST Python fora de `_EMBEDDED_KERNEL_FILES` idêntico à mãe; `gate_extension.py` idêntico. O avaliador legado usa `qgc_`, `qgp_` e feed; as seis flags maiores pertencem ao anexo `kernel_frontier`, sem se tornarem entradas diretas desse avaliador.
- O Audit corrente foi obtido pelo registro **{V['final_Audit_record']['log_name']}** → stdout bruto → mapa reanalisado. SHA256 do stream: `{V['final_Audit_record']['stdout_sha256']}`. Ambos os hashes globais atuais coincidem com esses bytes; `historical_v350_audit_metadata` conserva os valores históricos separados.
- As **34 superfícies de memória** permanecem nos hashes da mãe, relidos antes da conclusão. Recorders/verifier novos, relatório integrado autoral e nova custódia ainda não foram executados/gravados. A revisão não fez essas escritas.

Leitura estática integral dos helpers atuais: o preparador exige leitura do parecer e os três pins fonte/binário no DEV; o recorder confronta fontes/binários/rc0, pais, streams e 34 estados anteriores; o verifier relê todos os pares compilados e os backups/prefixos. Os appends previstos usam backup imediato de bytes na mesma pasta e temporário conferido antes de substituir cada arquivo. Isso é inspeção da lógica de gravação, não evidência de sua execução nem promessa de transação única das 34 superfícies.

O guia **PROXIMA_ETAPA_BLOCOS_GUIA_DE_TIPOS.md**, SHA256 `{H['guide']['sha256']}`, e seus links no recorder foram lidos na versão final. Mantém **OPEN/zero novos alvos**; distingue o gráfico de `E,j,Fix S` do antigo ideal/`Λ,Fix F`, exige cota inferior além de injetividade e preserva a ordem dos blocos. Não auditei nem promovi suas construções futuras.

## Alcance matemático preservado

O limite dos resolventes é forte e restrito ao fecho de `Ran A`; não prova gap ou convergência em norma de operador. As diferenças de quadrados aproximam vetores auto-adjuntos na mesma álgebra não unital, sem pôr sua unidade ou o resolvente nessa álgebra. O teste caracteriza o **S original**; a aplicação com `K` ainda recebe explicitamente **as duas ações de K e K***. Não constrói automaticamente o multiplicador limitado proposto pelos blocos.

Permanecem abertos a aplicação desse critério ao candidato, a estimativa inferior do bloco, a inclusão inversa pelo J original, identificação de `Δ^it`/KMS, traço e obrigações posteriores. O escopo legado `{V['scope']}` não identifica por homonímia seu J com o J original do peso. Seis flags maiores falsas, gate legado preservado, `full_plan_complete=false`; nenhuma execução/importação de monólito ou runtime integral. **Conclusão limitada ao pacote integrado20; nenhuma aprovação QG.**

## Artefatos reproduzíveis

- {link(RUN/'verification.json','Verificação final')} — SHA256 `{hf(RUN/'verification.json')}`.
- {link(RUN/'compilation.json','Cinco recompilações próprias e axiomas')} — SHA256 `{hf(RUN/'compilation.json')}`.
- {link(RUN/'build_manifest.json','Árvore, fontes e proveniência de cada dependência')} — SHA256 `{hf(RUN/'build_manifest.json')}`.
- {link(RUN/'helper_static_inspection.json','Inspeção estática dos helpers e guia')} — SHA256 `{hf(RUN/'helper_static_inspection.json')}`.
- {link(RUN/'axioms.json','Mapa Audit corrente reanalisado')}; {link(RUN/'base_source_provenance.json','Conferência dos fontes adicionais da base')}; logs próprios e cópias dos streams autorais na mesma pasta.

### Pins dos três módulos integrados

{pins}
'''
p=REV/'REVIEW_SQUARE_RESOLVENT_INTEGRATED.md';assert not p.exists(),'Existing preliminary report must be preserved by explicit byte backup and append'
b=text.encode();t=p.with_name(p.name+'.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
pin={'report':str(p),'sha256':hf(p),'bytes':len(b),'marker':'SQUARE_RESOLVENT_INTEGRATED_REVIEW','verification_sha256':hf(RUN/'verification.json')}
q=RUN/'review_pin.json';assert not q.exists();tmp=q.with_suffix('.json.tmp');raw=json.dumps(pin,indent=2).encode();tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(q)
print(json.dumps(pin))
