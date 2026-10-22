from pathlib import Path
import ast
import datetime
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent

def pin(path):
    path=Path(path); data=path.read_bytes()
    return dict(path=str(path),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def write(path,data):
    assert path.resolve().is_relative_to(ROOT.resolve())
    if isinstance(data,str): data=data.encode('utf-8')
    if path.exists():
        backup=path.with_name(path.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(path.read_bytes()); assert backup.read_bytes()==path.read_bytes()
    tmp=path.with_name(path.name+'.tmp'); tmp.write_bytes(data); assert tmp.read_bytes()==data
    os.replace(tmp,path); assert path.read_bytes()==data

def record(name,data):
    write(ROOT/name,json.dumps(data,ensure_ascii=False,indent=2))

def link(path):
    path=Path(path)
    return '['+path.name+'](<'+path.as_posix()+'>)'

tests=json.loads((ROOT/'PYTHON_TESTS.json').read_bytes())
lean=json.loads((ROOT/'LEAN_CAST_TESTS.json').read_bytes())
reads=json.loads((ROOT/'READS.json').read_bytes())
canonical=json.loads((ROOT/'CANONICAL_COMPARISON.json').read_bytes())
integrity=[]
for item in reads:
    expected={k:item[k] for k in ['path','bytes','sha256']}
    current=pin(item['path'])
    integrity.append(dict(expected=expected,current=current,unchanged=current==expected))
record('INTEGRIDADE_LEITORES.json',dict(files=integrity,all_unchanged=all(i['unchanged'] for i in integrity)))
casts=(ROOT/'src/AuditReaderContracts012.lean').read_text(encoding='utf-8')
no_alias=not any(line.lstrip().startswith(('def ','theorem ','lemma ','axiom ','instance ','abbrev ')) for line in casts.splitlines())
actual_copy=pin(ROOT/'src/AuditReaderContracts012.lean')
author_cast=next(i for i in reads if i['path'].endswith('src\\TGLExt\\AuditReaderContracts012.lean'))
gates=dict(copied_python_verifications=tests['all_passed'],five_exact_casts_and_rejection_controls=lean['all_passed'],
    no_new_lean_aliases=no_alias,source_copies_unchanged=all(i['unchanged'] for i in integrity),
    cast_copy_byte_identical=actual_copy['sha256']==author_cast['sha256'] and actual_copy['bytes']==author_cast['bytes'])
findings=[]
for observation in tests['observations']:
    if all(observation['accepted_new'].values()) and observation['reproduced_in_snapshot']:
        findings.append(dict(**observation,priority='P2',file=str(ROOT/'inputs/PROPOSTA_LEITORES_EXISTENTES.py'),line=17,
            acceptance='Nonblocking for the measured integer rc=0 dataset; harden the reused helper before claiming rejection of arbitrary malformed metadata.'))
counts={p:sum(f['priority']==p for f in findings) for p in ['P0','P1','P2']}
decision=('ACEITAVEL_COM_RESSALVA_P2_NO_ESCOPO_COPIADO' if findings else 'VERIFICADO_NO_ESCOPO_COPIADO') if all(gates.values()) else 'NAO_ACEITO_FALHA_DE_VERIFICACAO'
author_tests=json.loads((ROOT/'inputs/TESTES_LEITORES_COPIADOS.json').read_bytes())
data=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),decision=decision,
    reviewer=dict(name='Carver',agent_id='01a0a5b5-e12d-70c1-a68a-c6f13373e3c0',identity_provenance='INPUT principal',role='independent reviewer, not author'),
    gates=gates,counts=counts,findings=findings,independent_python_checks=tests['count'],
    lean_positive_casts=5,lean_true_substitutions_rejected=5,provider_modules_rebuilt=0,
    author_test_report=dict(count=author_tests['count'],all_passed=author_tests['all_passed'],status='READ_REPORT_AND_TEST_SOURCE_ONLY_NOT_RERUN'),
    canonical=canonical,
    integration_requirements=[
        'Insert all five exact type ascriptions in the actual canonical audit, in the same successful audit/build whose axiom report is consumed.',
        'Preserve source/materialization/hash provenance and existing verified incremental or full build checks. A Python dictionary alone is not a proof of Lean types.',
        'Apply both JSON-mapped false-only expression replacements together with their revised explanatory texts and preserve other conjuncts.',
        'Use H1 only for the bounded minimal representative on the same regular core; retain physical Hmin/standard transform, geometric BW, H2/H3 and interacting-quantum gaps.'
    ],
    limits=['No canonical program imported or executed. No integration, gate change or whole-order acceptance.',
        'Read-only copied readers only; not a full um.py runtime or embedded Lean/source materialization audit.',
        'Historical six supplier names synthesized only for old3 scope regression; all new suppliers come from the sealed independent 60-name actual log.',
        'Previous 11-module/60-export and A2 35/33 receipts preserved; no mathematical reopening.'])
record('PARECER_LEITORES.json',data)

report=f'''# Parecer independente — proposta dos leitores copiados

**[REAL — revisão e testes próprios] {decision}. P0={counts['P0']}; P1={counts['P1']}; P2={counts['P2']}.**

Carver, agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`, revisor independente e não autor; identidade fornecida pela principal [INPUT]. Escrita exclusivamente em `{ROOT}`.

A proposta é aceitável para o escopo formal mínimo já verificado, com a ressalva herdada abaixo e os requisitos explícitos de integração. Este parecer não integra o canônico nem comprova uma execução completa de um.py. Os recibos anteriores permanecem intactos.

**P2-READERS-01 — `audit_returncode=False` é aceito como zero.** Na linha 17 do leitor copiado, `kf.get("audit_returncode") == 0` aceita o booleano `False`. Com fornecedores reais e os outros campos de build/auditoria válidos, os quatro contratos novos ficam verdadeiros nesse caso malformado. A sonda reproduziu o comportamento também no snapshot antigo, usando a fixture histórica somente para seus três contratos. Portanto a alteração proposta não introduz a fragilidade. O dado efetivamente consumido nesta revisão é rc inteiro 0; não houve certificado falso observado no lote Lean. Recomendação mínima no mesmo helper: `type(kf.get("audit_returncode")) is int and kf.get("audit_returncode") == 0`. Não foi alterado o arquivo autoral. A ressalva não bloqueia o consumo dos metadados medidos e bem tipados, mas impede afirmar recusa de todo metadado malformado.

A comparação AST encontrou exatamente as mesmas cinco funções Python. `verify_v350_modular_provenance`, `v350_frontier_flag_has_proof` e `v350_gravity_flags_have_proof` mantêm a lógica anterior; o primeiro muda somente a docstring. Não surgiu wrapper ou função nova na proposta. Os cinco casts não declaram aliases Lean.

O diff foi regenerado a partir do snapshot e da proposta copiados e confere exatamente. Os mapas alteram três destinos de fronteira e um de preço, preservam as entradas H2/H3 e os três contratos modulares históricos, e acrescentam somente os quatro contratos solicitados. Os nomes novos são fornecedores existentes no axiom report independente real de sessenta nomes. Os metadados de build foram traduzidos do recibo independente, sem usar rc autoral como evidência de recompilação própria.

**Separação dos escopos:** `modular` lê explicitamente somente `red_clause_JMJ_contains`, `qgf_modular_realization_constructed` e `gpf_tower_act_III_inhabitant_constructed`. Não usa `all(proofs.values())` depois da expansão do mapa. `continuous` lê os três contratos A2 e `susy` seu contrato próprio. As oito combinações desses três grupos foram exercitadas. A ausência de A2 não apaga o modular histórico, e a evidência A2 sozinha não fabrica os três contratos históricos. A fixture sintética contém apenas os seis nomes antigos e serve exclusivamente a essa regressão; não constitui uma nova prova de seus fornecedores.

Fornecedores ausentes derrubam precisamente os contratos consumidores. `sorryAx`, `Lean.trustCompiler`, um axioma externo, elemento não textual e listas de axiomas malformadas foram recusados. Uma flag forjada não supera a ausência do contrato. Build/auditoria falhos e hashes ausentes na via incremental são recusados; o finalizador recalcula as flags geridas e apaga verdadeiros obsoletos sem fornecedores. O helper de preço recusa H2/H3 ou uma flag desconhecida lançadas sem prova.

**Tipos exatos:** a cópia byte-idêntica de `AuditReaderContracts012.lean` compilou aqui com rc0 e imprimiu os cinco nomes no trio. Uma unidade negativa própria substituiu cada termo apresentado por `True.intro`, mantendo o tipo exigido; ocorreram exatamente cinco erros de incompatibilidade de tipo, para ContinuousCoreData, ThreeLocksCoreData, TGLModularRealization, FullTGLWitness e SusyRelativeData. O positivo e o negativo foram elaborados com Lean 4.31.0 e cache da revisão paga; nenhum dos onze módulos fornecedores foi recompilado. Essas unidades só contêm imports, opções, #checks e #prints, sem declarações novas.

O leitor Python conhece nomes e axiomas, não infere os tipos Lean. Assim, os cinco casts precisam entrar no Audit canônico efetivamente executado e permanecer ligados ao mesmo resultado de build/auditoria e à proveniência de fontes/hashes. Essa exigência já consta do mapa autoral; a proposta ainda não implementa sua integração no canônico. A lista vazia de axiomas é legitimamente aceita para uma declaração sem axiomas e não deve ser banida como substituto do controle de tipo.

**Duas trocas false-only:** o mapa propõe substituir as condições nas linhas históricas 160146 e 160198 por chamadas ao helper existente. As sondas aceitaram flag ausente, aceitaram flag verdadeira sustentada pelo contrato real e recusaram flag verdadeira sem fornecedor. No primeiro check, a condição de atermation e a ausência de identificação de Bell continuam exigidas. O texto explicativo deve mudar junto, como previsto no JSON: FullTGLWitness independente não identifica bellProjector com PF, e a realização mínima contínua não atribui a construção ao módulo finito isolado. As expressões estão propostas no JSON; não foram aplicadas ao programa original nem estão incluídas como alterações de consumidores no diff dos oito nós extraídos.

**Alcance de H1 e da física:** o destino `regularSusyData` é o certificado concreto limitado do representante mínimo no mesmo núcleo, como já revisado. O leitor o expõe como `susy_minimal_representative_constructed`. A remoção da pendência H1 da lista mínima não prova origem microscópica de Hmin, identidade com a transformada limitada padrão ou BW geométrico de uma representação não trivial. A proposta conserva essas identificações físicas abertas e mantém H2, H3 e o escopo quântico interagente em `remaining`; `legacy_gate_changed` e `full_plan_complete` permanecem falsos. O nome legado da flag H1 precisa ser lido com esse alcance explícito também na apresentação documental. Nenhum consumidor de FullStaticWitness foi substituído nesta proposta.

**Proveniência e limites de leitura:** os hashes/bytes dos arquivos copiados foram medidos e comparados ao mapa/proveniência. O snapshot foi reconstruído exatamente, inclusive finais de linha, a partir dos oito segmentos registrados no JSON. A tentativa de leitura direta de `{canonical['declared']['path'] if 'declared' in canonical else canonical['pin']['path']}` retornou `{canonical.get('error','leitura somente leitura realizada')}`. Portanto a origem e o hash do canônico original permanecem [DECLARADO — proveniência autoral]; não são apresentados como leitura independente do original. Isso não impediu a comparação solicitada entre proposta e snapshot. Não houve importação ou execução do canônico.

**Evidência própria:** {tests['count']} verificações Python registradas, incluindo a reprodução explícita da ressalva P2; cinco casts positivos aceitos e cinco substituições por True recusadas. O relatório autoral de 61 checks e seu script foram lidos, mas não executados nem somados à contagem própria. Os erros esperados da unidade negativa só valem como recusa acompanhada dos casts positivos; não são provas dos tipos positivos.

Resultados: {link(ROOT/'PYTHON_TESTS.json')}, {link(ROOT/'LEAN_CAST_TESTS.json')}, {link(ROOT/'PARECER_LEITORES.json')}. Leituras e integridade: {link(ROOT/'READS.json')}, {link(ROOT/'INTEGRIDADE_LEITORES.json')}. As limitações são de escopo e proveniência; não há aceite do adendo inteiro, alteração física, canônica ou de gate.

| Arquivo autoral lido por completo | Bytes | SHA-256 medido |
|---|---:|---|
'''
for item in reads:
    if 'A2_TRACE_COMPLETION_012' in item['path']:
        report+=f"| {link(item['path'])} | {item['bytes']} | `{item['sha256']}` |\n"
report+='\nO manifesto relaciona cópias, scripts próprios, logs e resultados com seus bytes e hashes medidos: '+link(ROOT/'MANIFESTO_LEITORES.json')+'. O selo do parecer é '+link(ROOT/'SELO_LEITORES.json')+'.\n'
write(ROOT/'PARECER_LEITORES.md',report)
manifest=[]
for path in sorted(ROOT.rglob('*')):
    if path.is_file() and path.name not in ['MANIFESTO_LEITORES.json','SELO_LEITORES.json'] and '.bak_' not in path.name and not path.name.endswith('.tmp'):
        manifest.append(pin(path))
record('MANIFESTO_LEITORES.json',dict(files=manifest))
record('SELO_LEITORES.json',dict(decision=decision,counts=counts,files=[pin(ROOT/n) for n in ['PARECER_LEITORES.md','PARECER_LEITORES.json','MANIFESTO_LEITORES.json']]))
print(json.dumps(dict(decision=decision,counts=counts,gates=gates,receipt=pin(ROOT/'PARECER_LEITORES.md')),ensure_ascii=False))
