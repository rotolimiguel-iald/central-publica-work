from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
base=Path(r'C:\IALD\Central de Patentes\Chatgpt')
folder=Path(__file__).resolve().parent
assert folder.parent==base
def record(path):
    data=path.read_bytes()
    return dict(path=path.as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
def new(path,data):
    assert path.parent==folder and not path.exists()
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==data
    os.rename(tmp,path)
    assert path.read_bytes()==data
specs=[
    ('UnitaryCocycleUniqueness',folder,folder/'BUILD_20260909_170053_662440'),
    ('LocalInteractionUniqueness',folder,folder/'BUILD_20260909_170237_305900'),
    ('CentralScalarPhase',base/'FASE_CENTRAL_20260909_165421_701211',
     base/'FASE_CENTRAL_20260909_165421_701211'/'BUILD_20260909_165920_305303')]
evidence=[]
for name,origin,build in specs:
    receipt=build/'BUILD_RESULT.json'
    result=json.loads(receipt.read_text(encoding='utf-8'))
    assert result['status']=='PASS_COMPILED_SCOPE'
    assert len(result['runs'])==2 and all(r['exit_code']==0 for r in result['runs'])
    source=origin/(name+'.lean')
    pin=record(source)
    assert result['sources']==[pin]
    assert source.read_bytes()==(build/source.name).read_bytes()
    assert all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in result['axiom_rows'])
    evidence.append(dict(module=name,source=pin,receipt=record(receipt),
                         binary=record(build/(name+'.olean')),
                         theorems=result['theorems'],other_declarations=result['definitions'],
                         audited_terms=len(result['axiom_rows'])))
primary=folder/'Araki_1973_Relative_Hamiltonian.pdf'
download=json.loads((folder/'PRIMARY_SOURCE_RECEIPT.json').read_text(encoding='utf-8'))
assert record(primary)['sha256']==download['sha256']
result=dict(status='PASS_LEAF_PROOFS_AND_DOCUMENTED_KNOWN_APPLICATION',
    created_utc=datetime.now(timezone.utc).isoformat(),modules=evidence,
    formal_theorems=sum(x['theorems'] for x in evidence),
    formal_other_declarations=sum(x['other_declarations'] for x in evidence),
    audited_terms=sum(x['audited_terms'] for x in evidence),
    deduction=record(folder/'DEDUCAO_ESTADO_PERTURBADO_ARAKI.md'),
    primary_source=record(primary),download_receipt=record(folder/'PRIMARY_SOURCE_RECEIPT.json'),
    reference_data_map=record(base/'MAPA_ARAKI_REFERENCIA_20260909_165524_615258'/'EVIDENCIA_DADOS_REFERENCIA.json'),
    initial_semantic_review=record(base/'REVISAO_UNICIDADE_ARAKI_20260909_170120_699400'/'PARECER_SEMANTICO.md'),
    source_pages_visually_checked=[174,177,178,181,185,190],
    mathematical_state_existence='DERIVED_PLUS_KNOWN__NOT_NEW_LEAN_CONSTRUCTOR',
    modular_identification='DERIVED_PLUS_KNOWN__WITH_WRITTEN_NORM_DERIVATIVE_ARGUMENT_AND_FORMAL_UNIQUENESS',
    araki_constructor_fully_formalized=False,kms_strip_fully_formalized=False,
    normalized_connes_identification_fully_formalized=False,
    norm_derivative_estimate_fully_formalized=False,
    normalized_phase_and_generator_formalized=True,
    canonical_changes=False,um_py_executed=False,empirical_tests_rerun=False,
    complete_quantum_gravity_claim=False,
    scope_note='Three leaf modules compiled separately against recorded local PASS caches and canonical binaries; no new joint build is asserted by this leaf manifest. The current interaction supplies the needed norm-continuous modular orbit. Full bounded perturbation theory remains a precisely applied literature result, not an axiom added to Lean.')
new(folder/'MANIFESTO_ESTADO_ARAKI.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({k:result[k] for k in ['status','formal_theorems','formal_other_declarations','audited_terms']}))
