from pathlib import Path
import datetime, hashlib, json, os, sys
root=Path(__file__).resolve().parent
chat=root.parent
out=chat/'TUNEL/DO_CHATGPT'
review=chat/'REVISAO_A2_012/TRACE_COMPLETION_012/COMPATIBILIDADE_7'
reader_report=Path(sys.argv[1]).resolve()
assert reader_report.is_relative_to(chat/'REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def checkpin(row):
    m=pin(Path(row['path']));assert m['sha256']==row['sha256'],row
    if 'bytes' in row:assert m['bytes']==row['bytes'],row
    return m
def put(p,b):
    assert p.is_relative_to(chat) and not p.exists() and b
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
    return pin(p)
rd=json.loads(reader_report.read_bytes())
assert rd['active_version']=='V2' and rd['all_passed'] is True and rd['checks']
assert set(rd['open_findings'])=={'P0','P1','P2'} and not any(rd['open_findings'].values())
assert rd['historical_observation']['status']=='CORRIGIDO_NA_V2'
checkpin(rd['active_candidate'])
v1_review=reader_report.parent.parent/'PARECER_LEITORES.json'
v1=json.loads(v1_review.read_bytes())
assert v1['gates'] and all(v1['gates'].values())
assert v1['counts']=={'P0':0,'P1':0,'P2':1}
assert [r['id'] for r in v1['findings']]==['P2-READERS-01']
math_review=json.loads((review/'AUDITORIA_FINAL_INDEPENDENTE.json').read_bytes())
assert math_review['gates'] and all(math_review['gates'].values())
assert not any(math_review['counts'].values())
inv=json.loads((root/'INTEGRACAO_A2_INVENTARIO.json').read_bytes())
for row in inv['source_order']:
    checkpin(row['source'])
    if 'reviewed_source' in row:checkpin(row['reviewed_source']);checkpin(row['reviewed_object'])
author=json.loads((root/'AUDITORIA_AUTORAL_FULL_LEGACY_012.json').read_bytes())
assert author['all_axioms_allowed'] and author['all_controls_semantic'] and author['exact_legacy_full_witness_constructed']
reader_tests=json.loads((root/'TESTES_LEITORES_COPIADOS_V2.json').read_bytes())
assert reader_tests['all_passed']
checkpin(reader_tests['proposal'])

selection=[root/n for n in [
 'ENTREGA_A2_FINAL_CORPO.md','ADENDO_ENTREGA_LEITORES_V2.md',
 'INTEGRACAO_A2_INVENTARIO.json','AUDIT_NAMES_FULL.json','AUDITORIA_AUTORAL_FULL_LEGACY_012.json',
 'REAPROVEITAMENTO.md','REAPROVEITAMENTO.json','ADENDO_FICHA_COMPATIBILIDADE.md',
 'PROVENIENCIA_POLAR.json','PROVENIENCIA_A2_DELTA01.json','PROVENIENCIA_CORE_SUPPORT.json',
 'PROVENIENCIA_SUSY_PARA_AUDIT_TIPOS.json','CANONICAL_READERS_PROVENANCE.json',
 'CANONICAL_READERS_SNAPSHOT.py','CANONICAL_CONSUMERS_BOUNDED.txt',
 'PROPOSTA_LEITORES_EXISTENTES_V2.py','PROPOSTA_LEITORES_EXISTENTES_V2.diff',
 'PROPOSTA_MAPA_CONSUMIDORES_V2.json','TESTES_LEITORES_COPIADOS_V2.json','test_reader_proposal_v2.py',
 'src/TGLExt/AuditFullLegacy012.lean','src/TGLExt/AuditReaderContracts012.lean',
 'src/TGLExt/BadReaderWitnessType012.lean','dev_lean.py',
 'attempts/20260915_143907_558559/RESULT.json','attempts/20260915_143907_558559/START.json',
 'attempts/20260915_143907_558559/stdout.txt',
 'attempts/20260915_144026_975759/RESULT.json','attempts/20260915_144026_975759/START.json',
 'attempts/20260915_144026_975759/stdout.txt']]
selection += [review/n for n in ['RECIBO_COMPATIBILIDADE_MONTAGEM_SUSY.md','AUDITORIA_FINAL_INDEPENDENTE.json','MANIFESTO_FINAL.json','INTEGRIDADE_FINAL.json','SELO_FINAL.json','FINAL_AUDIT.json']]
selection += [chat/'A2_SUSY_012'/n for n in ['RECIBO.json','ENTREGA.md','AUDITORIA.json','CONTROLES.json','FALHAS_E_LIMITES.md','FICHA_REAPROVEITAMENTO.md','FICHA_REAPROVEITAMENTO.json','MANIFESTO.json','SELOS.json']]
selection += [out/n for n in [
 'ENTREGA_011_A2_suporte_split_e_parede.md','ENTREGA_011_A2_suporte_split_e_parede_manifesto.json',
 'ENTREGA_012_B1_PRIME_quarta_face.md','ENTREGA_012_B1_PRIME_quarta_face_manifesto.json',
 'ENTREGA_012_ADENDO001_saneamentos.md','ENTREGA_012_ADENDO001_saneamentos_manifesto.json']]
# Include the complete final copied-reader receipt bundle, not its working source tree/cache.
selection += [p for p in reader_report.parent.iterdir() if p.is_file() and p.suffix in ('.md','.json') and '.bak_' not in p.name]
selection += [reader_report.parent.parent/n for n in ['PARECER_LEITORES.md','PARECER_LEITORES.json','MANIFESTO_LEITORES.json','SELO_LEITORES.json','LEAN_CAST_TESTS.json','PYTHON_TESTS.json','LEITORES_ATIVOS.json']]
selection += [Path(row['source']['path']) for row in inv['source_order']]
records=[]
for p in sorted(set(selection),key=str):records.append(pin(p))

stamp=datetime.datetime.now().astimezone().isoformat()
manifest={'timestamp':stamp,'status':'A2_MINIMAL_EXACT_CONTRACT_REVIEWED_DELIVERED_FOR_CANONICAL_INTEGRATION',
          'mathematical_review':pin(review/'AUDITORIA_FINAL_INDEPENDENTE.json'),
          'reader_review_v2':pin(reader_report),'counts':inv['counts'],
          'canonical_integration_done':False,'gate_changed':False,
          'source_order':inv['source_order'],'audit_names_explicit':inv['audit_names_explicit'],
          'additional_reviewed_exports':inv['additional_reviewed_exports'],
          'artifacts':records,
          'limits':['Minimal bounded representative 1-PF; old formal wedge supplier U=1.',
                    'No physical identification, sigma result or canonical run.',
                    'A1 and prior33 reused with separate accepted receipts; historical partial states preserved.']}
mp=out/'ENTREGA_011_A2_fecho_core_three_locks_susy_manifesto.json'
mpin=put(mp,json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf8'))
body=(root/'ENTREGA_A2_FINAL_CORPO.md').read_text(encoding='utf8')
body+='\n'+(root/'ADENDO_ENTREGA_LEITORES_V2.md').read_text(encoding='utf8')
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
body+='\n\n## Recibo de transmissão e referências diretas\n\n'
body+=f'Transmissão: {stamp}. Inventário conferido novamente: {len(records)} artefatos selecionados, mais as fontes e objetos da ordem de montagem. '
body+=f"A2 totaliza {inv['counts']['all_unique_A2_modules']} módulos matemáticos únicos: oito do lote33 preservado e onze desta conclusão. "
body+='A revisão dos leitores V2 quita P2-READERS-01 no delta; os pareceres V1 permanecem como histórico.\n\n'
important=[(mp,'Manifesto da entrega'),(root/'INTEGRACAO_A2_INVENTARIO.json','Ordem dos fontes, nomes auditados e tipos'),
 (review/'RECIBO_COMPATIBILIDADE_MONTAGEM_SUSY.md','Revisão matemática independente'),
 (reader_report.parent/'RECIBO_LEITORES_V2.md','Revisão independente dos leitores V2'),
 (root/'PROPOSTA_LEITORES_EXISTENTES_V2.py','Leitores existentes: cópia V2'),
 (root/'PROPOSTA_MAPA_CONSUMIDORES_V2.json','Mapa das bandeiras e das duas substituições'),
 (root/'src/TGLExt/AuditReaderContracts012.lean','Verificações de tipo para o auditor canônico'),
 (root/'src/TGLExt/V354RegularLegacyWitness.lean','Termos completos do contrato antigo'),
 (chat/'A2_SUSY_012/src/TGLExt/V354RegularSusy.lean','Instanciação SUSY concreta')]
for p,label in important:
    q=pin(p);body+='- '+link(p,label)+f" — SHA256 `{q['sha256']}`.\n"
body+='\nAs três entregas anteriores de A2 parcial, B1′ e saneamentos a–h estão vinculadas no manifesto; seus conteúdos e recibos não foram sobrescritos.\n'
dp=out/'ENTREGA_011_A2_fecho_core_three_locks_susy.md'
dpin=put(dp,body.encode('utf8'))
receipt={'timestamp':stamp,'handoff':dpin,'manifest':mpin,'reader_review':pin(reader_report),
         'goal_scope_delivered':['A2 exact legacy contract and concrete SUSY','B1 prime previously delivered','ADENDO001 a-h previously delivered'],
         'canonical_integration_pending_with_management':True,'gate_changed':False}
put(root/'RECIBO_TRANSMISSAO_A2_FINAL.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(receipt,ensure_ascii=False))
