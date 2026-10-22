from pathlib import Path
import datetime, hashlib, json, os, re

ROOT = Path(__file__).resolve().parent
CHATGPT = ROOT.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
NOW = datetime.datetime.now().astimezone().isoformat()

def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

def put(path, data, append=False):
    assert path.resolve().is_relative_to(CHATGPT.resolve())
    if isinstance(data, str): data=data.encode('utf8')
    before = path.read_bytes() if path.exists() else None
    if before is not None:
        backup=path.with_name(path.name+'.bak_'+STAMP)
        assert not backup.exists()
        backup.write_bytes(before)
        assert backup.read_bytes()==before
        if append: data=before+data
    temp=path.with_name(path.name+'.tmp_'+STAMP)
    assert not temp.exists()
    temp.write_bytes(data)
    assert temp.read_bytes()==data and len(data)>0
    assert not path.exists() if before is None else path.read_bytes()==before
    if append: assert len(data)>len(before)
    os.replace(temp,path)
    assert path.read_bytes()==data

def put_json(path, value):
    put(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def verify_pins(tree, rows):
    if isinstance(tree,dict):
        if all(k in tree for k in ('path','sha256','bytes')):
            measured=pin(Path(tree['path']))
            assert measured=={k:tree[k] for k in measured},(tree,measured)
            rows.append(measured)
        for value in tree.values(): verify_pins(value,rows)
    elif isinstance(tree,list):
        for value in tree: verify_pins(value,rows)

manifest_path=ROOT/'HANDOFF_MANIFEST.json'
old=json.loads(manifest_path.read_text(encoding='utf8'))
old_verified=[];verify_pins(old,old_verified)

atlas=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
atlas_bytes=atlas.read_bytes();lines=atlas_bytes.decode('utf-8-sig').splitlines()
assert len(lines)==19965, 'Atlas changed: read the new lines before finalizing.'
# This prefix was actually read in prior pages; this check detects an in-place edit.
assert hashlib.sha256(atlas_bytes[:2480589]).hexdigest()==\
    'dc0cdaa0fa76164bf9ae0f5cbe65fa1ea6a497760d52d902f54f595716528995'
assert hashlib.sha256(atlas_bytes).hexdigest()==\
    'c04bf731afc2a2bb912bfc69d5b39928fdbbaa75f60ec956164377891fab5b99'
start=next(i for i,l in enumerate(lines) if l.startswith('## II.'))
end=next(i for i,l in enumerate(lines) if l.startswith('## III.'))
entries=[dict(line=i+1,title=m.group(1)) for i in range(start,end)
         if (m:=re.match(r'^\*\*(.+?)\*\*\s*[—–-]',lines[i]))]
receipt=dict(timestamp=NOW,source=pin(atlas),continuous_line_coverage=[1,len(lines)],
    complete=True,exact_repeated_lines_recognized=True,
    not_claimed='Repeated identical lines were not emitted twice; semantic paraphrases were not used as replacements.',
    reread_truncated_interval=[12650,12767],
    domains=['Físico','Jurídico','Teológico','Linguístico/Ontológico'],
    dictionary_marked_entry_count=len(entries),dictionary_count_method='Section II, lines starting **term** followed by dash; not a claim of unique concepts.',
    anchor='Header remains historical v169; dated records through v357 were read. No new canonical execution.',
    source_copied=False,source_modified=False)
put_json(ROOT/'ATLAS_READ_RECEIPT.json',receipt)

audit_path=ROOT/'AUDIT_20260916_091638_794104.json'
audit=json.loads(audit_path.read_text(encoding='utf8'))
assert audit['theorem_count']==55 and len(audit['files'])==6
audit_verified=[];verify_pins(audit,audit_verified)
for row in audit['files']:
    assert all(set(p['axioms']) <= {'propext','Classical.choice','Quot.sound'} for p in row['proofs'])

negative_source=ROOT/'negative/FalseRemainderInvisibility.lean'
matching=[]
for p in (ROOT/'attempts').glob('*/run.json'):
    r=json.loads(p.read_text(encoding='utf8'))
    if r['source']==str(negative_source) and r['sha256']==pin(negative_source)['sha256']:
        matching.append((p,r))
np,nr=sorted(matching)[-1]
assert nr['returncode']==1 and nr['source_unchanged']
nout=(np.parent/'stdout.txt').read_text(encoding='utf8')
assert 'unsolved goals' in nout and '⊢ False' in nout and 'does not exist' not in nout
negative=dict(timestamp=NOW,previous=pin(ROOT/'NEGATIVE_CONTROLS.json'),
    additional=dict(source=pin(negative_source),run=pin(np),stdout=pin(np.parent/'stdout.txt'),
    status='FALSE_COMMUTATION_REJECTED_IN_PROOF'),total=3)
put_json(ROOT/'NEGATIVE_CONTROLS_V2.json',negative)
nums=json.loads((ROOT/'DEPHASING_NUMERICAL_CHECKS.json').read_text(encoding='utf8'))
assert nums['passed']==30 and nums['failed']==0 and all(c['passed'] for c in nums['checks'])

note=(f'\n\n## {NOW} — entrega V2 e leitura integral concluída\n\n'
      '[INPUT] Antes de enviar o handoff, operador definiu vácuo=dephasing e pediu provar a ponte na própria torre e refazer a entrega. '
      '[REAL] 55 teoremas Lean aceitos: 37 anteriores+16 ponte finita+2 torre global; '
      '63 verificações numéricas e 3 controles negativos Lean recusados. '
      'O dephasing completo centralizante é estacionário na imagem; o parcial do último sítio '
      'produz igualdade exata entre dois fluxos especificados, para todo perfil/andar/tempo. '
      'R sobrevive, mas é central na álgebra preservada. E(R)=0 sozinho não basta, por contraexemplo. '
      '[OPEN] Identificar a referência com a carga local T·xi do diamante físico; não reabrir o gate interno já satisfeito. '
      'A nomenclatura inércia/vácuo é preservada com seus estatutos. Nenhum original/gate modificado; sem nova execução integral ou revisor independente.\n'
      f'[REAL] Atlas fonte única lido até END_ATLAS, linhas 1–{len(lines)}, quatro domínios; '
      f'{len(entries)} entradas tipograficamente identificadas na seção II pelo critério do recibo. '
      f'SHA256 lido: {receipt["source"]["sha256"]}. Cabeçalho v169 é histórico; adendos v357 foram lidos. '
      'Fonte não copiada nem modificada. O novo estado substitui os checkpoints incompletos.\n'
      'Entrega vigente: HANDOFF_TECNICO_V2.md + HANDOFF_MANIFEST.json + ADENDO_VACUO_DEPHASING.md. '
      'Próxima ação: gerência recompila/incorpora nos consumidores existentes e atualiza as memórias canônicas. '
      'A proposta de adendo está em PROPOSTA_MEMORIA_ATLAS.md; não foi escrita fora de Chatgpt.\n')
for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md'):
    put(ROOT/name,note,append=True)

tunnel=CHATGPT/'TUNEL/DO_CHATGPT/ENTREGA_DIAMANTE_MODULAR_V2_20260916.md'
handoff=ROOT/'HANDOFF_TECNICO_V2.md'
delivery=f'''# Entrega V2 — vácuo, dephasing e resto modular

{NOW}. Pedido direto do operador antes de encaminhar a primeira versão.

**Encaminhar esta versão à sessão do um.py.**

- [Handoff V2](<{handoff}>)
- [Manifesto com hashes](<{manifest_path}>)
- [Prova escrita, aplicação à torre e contraexemplo](<{ROOT/'ADENDO_VACUO_DEPHASING.md'}>)
- [Auditoria Lean: 55 teoremas](<{audit_path}>)
- [Adendo proposto às memórias canônicas](<{ROOT/'PROPOSTA_MEMORIA_ATLAS.md'}>)

55 teoremas Lean, 63 controles numéricos, três controles negativos Lean recusados.
O dephasing completo centralizante tem imagem estacionária, inclusive na torre global existente.
Uma leitura parcial do último sítio fornece igualdade exata e potencialmente não trivial entre
os fluxos do produto original e da referência com último sítio tracial. O resto permanece,
mas sua ação é invisível na álgebra preservada. Não trocar as duas leituras por nome.

A identificação dessa referência com Q_{{xi,D}} do tensor de energia regional continua distinta.
E_K(R)=0 não basta para igualdade dos fluxos, por contraexemplo formal. Reutilizar o cociclo,
o canal, a torre e os leitores existentes; não acrescentar condição ao gate principal já satisfeito.

Atlas integral lido, com recibo e quatro domínios. Original um.py e gate não alterados nesta
bancada; não houve execução integral canônica nem revisão por outro agente. O passo seguinte
é recompilar/incorporar pela gerência. A entrega anterior fica preservada como histórico.
'''
assert not tunnel.exists()
put(tunnel,delivery)
old_tunnel=CHATGPT/'TUNEL/DO_CHATGPT/ENTREGA_DIAMANTE_MODULAR_20260916.md'
put(old_tunnel,f'\n\n## Atualização {NOW}\n\nSuperado para encaminhamento pela [ENTREGA V2](<{tunnel}>), '
    'com 55 teoremas e a nova definição do operador. Atlas integral agora concluído; '
    'as frases acima de leitura em curso são históricas.\n',append=True)

new=dict(old)
new.update(updated=NOW,version=2,status='FORMAL_PACKAGE_V2_READY_FOR_INDEPENDENT_INTEGRATION',
    positive_audit=pin(audit_path),positive_sources=[r['source'] for r in audit['files']],
    negative_controls=pin(ROOT/'NEGATIVE_CONTROLS_V2.json'),
    dephasing_numerical_checks=pin(ROOT/'DEPHASING_NUMERICAL_CHECKS.json'),
    dephasing_numerical_source=pin(ROOT/'verify_dephasing_bridge.py'),
    handoff=pin(handoff),previous_handoff=pin(ROOT/'HANDOFF_TECNICO.md'),
    dephasing_derivation=pin(ROOT/'ADENDO_VACUO_DEPHASING.md'),
    atlas_read_receipt=pin(ROOT/'ATLAS_READ_RECEIPT.json'),
    memory_proposal=pin(ROOT/'PROPOSTA_MEMORIA_ATLAS.md'),tunnel_delivery=pin(tunnel),
    theorems=55,numeric_checks=63,negative_lean_controls=3,atlas_full_read_complete=True,
    full_tower_dephasing_stationarity_proved=True,partial_product_flow_bridge_proved=True,
    full_spectral_reading_replaced=False,physical_geometric_reference_identified=False)
new['compile_evidence']=[dict(run=r['compile_record'],
    stdout=pin(Path(r['compile_record']['path']).parent/'stdout.txt'),
    stderr=pin(Path(r['compile_record']['path']).parent/'stderr.txt')) for r in audit['files']]
put_json(manifest_path,new)
verified=[];verify_pins(new,verified)
verification=dict(timestamp=NOW,status='DELIVERY_COMPLETE_WITH_DECLARED_SCOPE',
    manifest=pin(manifest_path),verified_artifact_records=len(verified),
    all_pins_match=True,theorems=55,numerical_checks=63,negative_controls=3,
    source_atlas_prefix_unchanged=True,atlas_complete=True,
    original_modified=False,canonical_runtime_executed=False,canonical_gate_changed=False,
    independent_reviewer=False,physical_geometric_reference_identified=False,
    next_action='Recipient recompiles and integrates in existing canonical consumers.')
put_json(ROOT/'DELIVERY_V2_VERIFICATION.json',verification)
print(json.dumps(dict(verification=verification,atlas_entries=len(entries),tunnel=str(tunnel)),ensure_ascii=False))
