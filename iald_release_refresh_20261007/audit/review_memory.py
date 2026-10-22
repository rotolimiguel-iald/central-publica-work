"""Independent, offline, read-only review of the prepared scientific release."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import unquote, urlparse
import ast
import hashlib
import json
import os
import re

WORK = Path(__file__).resolve().parents[1]
STAGE = WORK / 'memory_stage'
APP = Path('C:/IALD/projetos_pyhton/IALD')
VAULT = Path('C:/IALD/Central de Patentes/vault/originals_copy')
MARKER = '## Exposição canônica integral: fórmulas e derivações'
inputs, checks, findings = {}, [], []
stats = Counter()
BOOLEAN_DICTIONARY = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    path = Path(path)
    raw = path.read_bytes()
    key = str(path)
    pin = {'sha256': sha(raw), 'bytes': len(raw)}
    if key in inputs:
        assert inputs[key] == pin, 'Input changed while reading: ' + key
    inputs[key] = pin
    return raw

def pairs(rows):
    out = {}
    for key, value in rows:
        assert key not in out, 'Duplicate JSON key: ' + key
        out[key] = value
    return out

def loads(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))

def load(path):
    return loads(read(path))

def same(a, b):
    return json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False)

def child(pointer, key):
    return pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')

def resolve(root, pointer):
    assert pointer == '' or pointer.startswith('/'), pointer
    for part in pointer.split('/')[1:]:
        assert not re.search('~(?![01])', part), pointer
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(root, list):
            assert re.fullmatch('0|[1-9][0-9]*', key), pointer
            root = root[int(key)]
        else:
            root = root[key]
    return root

def check(name, ok, evidence=None):
    checks.append({'name': name, 'passed': bool(ok), 'evidence': evidence})

def topics(text, names=None):
    body = text.split(MARKER, 1)[0]
    headers = list(re.finditer(r'(?m)^### ([^\n]+)\n', body))
    result = {}
    for i, h in enumerate(headers):
        name = h[1].split(' — ', 1)[0]
        if names is not None and name not in names:
            continue
        end = headers[i+1].start() if i+1 < len(headers) else len(body)
        block = body[h.end():end].split('\n## ', 1)[0].strip()
        assert name not in result, name
        result[name] = block
    return result

def reconstruct(node, source, topic, pointer, represented, partial=False):
    expected = resolve(source, pointer)
    if isinstance(node, dict):
        tags = [t for t in ('same_as', 'SOURCE_RELATIVE', 'DETAILS_IN_SOURCE', '@') if t in node]
        if tags:
            assert len(tags) == 1, pointer
            tag = tags[0]
            target = topic + node[tag] if tag in ('SOURCE_RELATIVE', '@') else node[tag]
            actual = resolve(source, target)
            assert same(actual, expected), 'Wrong reference target: ' + pointer
            if tag != 'same_as':
                assert target == pointer, 'Misplaced reference: ' + pointer
            stats['references_' + tag] += 1
            if 'items' in node:
                assert type(node['items']) is int and len(actual) == node['items'], pointer
            if 'true_fields' in node or 'false_fields' in node:
                assert all(type(x) is bool for x in actual.values()), pointer
                assert node['true_fields'] == sum(actual.values()), pointer
                assert node['false_fields'] == len(actual)-sum(actual.values()), pointer
            for suffix, value in node.get('fields', {}).items():
                assert same(resolve(actual, suffix), value), pointer + suffix
                represented[pointer + suffix] = value
            for key, value in node.get('semantic_fields', {}).items():
                reconstruct(value, source, topic, child(pointer, key), represented)
            for index, value in enumerate(node.get('first_records', [])):
                reconstruct(value, source, topic, child(pointer, index), represented)
            metadata = {tag, 'items', 'fields', 'semantic_fields', 'first_records', 'role', 'true_fields', 'false_fields'}
            for key, value in node.items():
                if key not in metadata:
                    reconstruct(value, source, topic, child(pointer, key), represented)
            return actual
        assert isinstance(expected, dict), pointer
        if partial:
            assert set(node) <= set(expected), pointer
        else:
            assert set(node) == set(expected), 'Field coverage: ' + pointer
        return {k: reconstruct(v, source, topic, child(pointer, k), represented, partial) for k, v in node.items()}
    if isinstance(node, list):
        assert isinstance(expected, list) and len(node) == len(expected), pointer
        return [reconstruct(v, source, topic, child(pointer, i), represented, partial) for i, v in enumerate(node)]
    assert same(node, expected), 'Literal changed: ' + pointer
    represented[pointer] = node
    return node

def decode(node, dictionary, exposition, source, topic=None):
    if isinstance(node, list):
        return [decode(x, dictionary, exposition, source, topic) for x in node]
    if not isinstance(node, dict):
        return node
    if set(node)=={'@upper'}:
        assert isinstance(node['@upper'],str)
        return node['@upper'].upper()
    if set(node)=={'@concat'}:
        assert isinstance(node['@concat'],list)
        parts=[decode(x,dictionary,exposition,source,topic) for x in node['@concat']]
        assert all(isinstance(x,str) for x in parts)
        return ''.join(parts)
    if set(node)=={'@enum'}:
        label=node['@enum']
        assert isinstance(label,str) and re.fullmatch('[a-z0-9 ]+',label)
        stats['lossless_enum_labels'] += 1
        return label.upper().replace(' ','_')
    aliases = {'@F':'@SOURCE_FIELDS','@I':'@SOURCE_ITEMS','@L':'@TGL_LITERAL','@Y':'@SUMMARY','@X':'@EXPOSITION'}
    expanded = {aliases.get(k,k):v for k,v in node.items()}
    assert len(expanded)==len(node), 'Conflicting metadata aliases'
    node = expanded
    if '@B' in node:
        flags = BOOLEAN_DICTIONARY[node.pop('@B')]
        assert all(type(v) is bool for v in flags.values()) and not set(flags)&set(node)
        node.update(flags)
        stats['literal_boolean_groups'] += 1
    if set(node) == {'@TGL_LITERAL'}:
        stats['haiku_literal_references'] += 1
        return decode(dictionary[node['@TGL_LITERAL']],dictionary,exposition,source,topic)
    if isinstance(node.get('@SUMMARY'),list):
        assert set(node)=={'@SUMMARY'}, 'Unexpected compact-summary metadata'
        parts=node['@SUMMARY']
        assert len(parts) in (3,4), 'Invalid compact summary'
        if len(parts)==3:
            assert topic in source['core'], 'Current topic required for compact summary'
            relative,start,size=parts;label=topic
        else:
            label,relative,start,size=parts
            assert topic is None or topic==label, 'Summary topic mismatch'
        assert isinstance(label,str) and label in source['core']
        assert isinstance(relative,str) and (relative=='' or relative.startswith('/'))
        assert type(start) is int and type(size) is int
        pointer='/core/'+label+relative
        resolve(source,pointer)
        node={'@SUMMARY':label,'source_pointer':pointer,'span':[start,size]}
        stats['compact_summary_expansions'] += 1
    if '@EXPOSITION' in node or '@SUMMARY' in node:
        start, size = node.get('span', node.get('@EXPOSITION'))
        assert type(start) is int and type(size) is int and 0 <= start < start+size <= len(exposition)
        text = exposition[start:start+size]
        if '@SUMMARY' in node:
            assert text.startswith('**Estatutos [' + node['@SUMMARY'] + ']**')
            stats['haiku_summary_references'] += 1
            # A documented summary is not equated to its literal source value.
            return resolve(source, node['source_pointer'])
        if 'starts_with' in node:
            assert text.startswith(decode(node['starts_with'],dictionary,exposition,source,topic))
        stats['haiku_exposition_references'] += 1
        return text
    out = {k: decode(v, dictionary, exposition, source, topic) for k, v in node.items()
           if k not in ('@SOURCE_FIELDS', '@SOURCE_ITEMS')}
    for tag in ('@SOURCE_FIELDS', '@SOURCE_ITEMS'):
        for key in node.get(tag, []):
            assert key not in out and '/' not in key and '~' not in key
            out[key] = {'@': '/' + key}
            if tag == '@SOURCE_ITEMS':
                out[key]['items'] = node[tag][key]
    return out

def important(value, pointer=''):
    out = {}
    if isinstance(value, dict):
        for key, item in value.items():
            if key == 'checks':
                continue
            p = child(pointer, key)
            if re.search('statut|status|scope|escopo|hypothes|hip[oó]tes|not_claimed|not_said|verdict|veredito', key, re.I):
                out[p] = item
            else:
                out.update(important(item, p))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            out.update(important(item, child(pointer, i)))
    return out

def covered(pointer, value, represented):
    if pointer in represented:
        return same(value, represented[pointer])
    for p, v in represented.items():
        if pointer.startswith(p + '/') and same(resolve(v, pointer[len(p):]), value):
            return True
    if isinstance(value, dict):
        return all(covered(child(pointer, k), v, represented) for k, v in value.items())
    if isinstance(value, list):
        return all(covered(child(pointer, k), v, represented) for k, v in enumerate(value))
    return False

# Independent reader derived from the finalized v389 reviewer, with compact
# summary validation added locally. No builder module is imported.

def audit():
    m = load(STAGE/'manifest_staged.json')
    prepared = load(STAGE/'prepared.json')
    source = load(Path(m['published_evidence']['result']['path']))
    baseline = load(APP/'iald_nucleo_fixo.json')
    old = load(baseline['published_evidence']['result']['path'])
    source_names = set(source['core'])
    check('version_source_identity', m['active_cluster']['release']=='v390' and prepared['source_sha256']==m['active_cluster']['release_source_sha256'])
    public = load(WORK/'public_v390_verification.json')
    check('public_receipt_bound_to_selected_commit', public['status']=='PASS' and public['requested_commit']==prepared['commit'])
    for name in ('program','seal','result','proof_manifest'):
        path = Path(m['published_evidence'][name]['path'])
        raw = read(path)
        pub = next(a for a in public['artifacts'] if a['name']==path.name)
        check('source_'+name, raw==read(VAULT/'um_unificado_v390'/path.name) and sha(raw)==pub['actual_sha256'])
    for rel, record in prepared['source_files'].items():
        raw = read(STAGE/'release'/rel)
        check('release_file:'+rel, sha(raw)==record['sha256'] and len(raw)==record['bytes'])
    for entry in m['entries']:
        parsed = urlparse(entry['url'])
        parts = parsed.path.split('/')
        check('document_entry:'+entry['id'], parsed.netloc=='raw.githubusercontent.com' and parts[3]==prepared['commit'] and
              unquote('/'.join(parts[4:]))==str(Path(entry['path']).relative_to(STAGE/'release')).replace('\\','/') and
              sha(read(entry['path']))==entry['public_sha256'])
    install = load(STAGE/'manifest_install.json')
    target = Path(prepared['install_target'])
    mapped = json.loads(json.dumps(m))
    for entry in mapped['entries']+[mapped['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:
        entry['path'] = str(target/Path(entry['path']).relative_to(STAGE))
    for key in ('mother_instruction','operational_core'):
        mapped[key]['path'] = str(target/Path(mapped[key]['path']).relative_to(STAGE))
    for key in ('path','kernel_bundle','kernel_verification'):
        mapped['active_cluster'][key] = str(target/Path(mapped['active_cluster'][key]).relative_to(STAGE))
    check('install_manifest_only_relocates_paths', same(install,mapped) and sha(read(STAGE/'manifest_install.json'))==prepared['install_manifest_sha256'])
    index = load(STAGE/'document_index.json')
    check('retrieval_index_source_pins', all(any(r['id']==e['id'] and r['sha256']==e['public_sha256'] and r['url']==e['url'] for r in index) for e in m['entries']))
    mother = read(m['mother_instruction']['path'])
    old_mother = read(baseline['mother_instruction']['path'])
    core = read(m['operational_core']['path'])
    old_core = read(baseline['operational_core']['path'])
    check('mother_v5_byte_identical', mother==old_mother and sha(mother)==m['mother_instruction']['sha256'])
    check('operational_core_prior_bytes_preserved', core.startswith(old_core) and sha(core)==m['operational_core']['sha256'], {'preserved_bytes':len(old_core),'append_bytes':len(core)-len(old_core)})
    cluster_raw = read(m['active_cluster']['path'])
    cluster = cluster_raw.decode('utf-8')
    check('cluster_pin', sha(cluster_raw)==m['active_cluster']['sha256'])
    canonical = next(e for e in m['entries'] if e['id']=='um_forma_canonica_integral')
    canonical_raw = read(canonical['path'])
    canonical_text = canonical_raw.decode('utf-8-sig').replace('\r\n','\n')
    if 'DICIONÁRIO DO CLUSTER\n' in cluster.split(MARKER,1)[0]:
        cluster_dictionary=loads(cluster.split('DICIONÁRIO DO CLUSTER\n',1)[1].split('\n',1)[0])
        assert all(isinstance(k,str) and isinstance(v,str) for k,v in cluster_dictionary.items())
        assert cluster.count('<EXPOSICAO_CANONICA>\n')==cluster.count('\n</EXPOSICAO_CANONICA>')==1
        cluster_exposition=cluster.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    else:
        cluster_dictionary={}
        cluster_exposition=cluster.rsplit('Fonte: ',1)[1].split('\n',1)[1]
    check('canonical_integral_in_cluster', cluster_exposition==canonical_text and canonical_raw==read(VAULT/'um_unificado_v390'/Path(canonical['path']).name))
    ct = topics(cluster)
    check('all_v390_core_sections_present', set(ct)==source_names and len(ct)==len(source['core']) and set(prepared['coverage'])==source_names)
    cluster_errors = []
    representations = {}
    for name, body in ct.items():
        pointer = child('/core', name)
        try:
            assert body.splitlines()[0]=='Fonte: resultado_publicado_integral '+pointer
            node = decode(loads(body.splitlines()[1]),cluster_dictionary,cluster_exposition,source,name)
            represented = {}
            restored = reconstruct(node, source, pointer, pointer, represented)
            assert same(restored,source['core'][name])
            representations[name]=represented
        except Exception as exc:
            cluster_errors.append({'topic':name,'error':str(exc),'type':type(exc).__name__})
    check('cluster_all_topics_reconstruct_exactly',not cluster_errors,cluster_errors)
    added = sorted(source_names-set(old['core']))
    changed = sorted(n for n in source_names & set(old['core']) if not same(source['core'][n],old['core'][n]))
    check('prepared_delta_vs_installed_v389', added==sorted(prepared['added_topics']) and changed==sorted(prepared['changed_topics']) and not set(old['core'])-source_names,{'added':added,'changed_count':len(changed)})
    deltas = {}
    for version in (389,):
        prior = load(VAULT/('um_unificado_v'+str(version))/'um_absoluto.json')
        pc = prior['core']
        deltas[str(version)+'_to_390']={'added':sorted(source_names-set(pc)),'removed':sorted(set(pc)-source_names),'changed':sorted(k for k in source_names&set(pc) if not same(source['core'][k],pc[k]))}
    check('v389_v390_deltas_reconstruct', not cluster_errors and all(not d['removed'] for d in deltas.values()), deltas)
    proof = load(m['published_evidence']['proof_manifest']['path'])
    km = load(STAGE/'kernel/kernel_manifest.json')
    records = {r['path']:r for r in km['files']}
    pins = proof['formal_files_sha256']
    missing = sorted(set(pins)-set(records))
    extra = sorted(set(records)-set(pins))
    mismatches = [name for name,r in records.items() if sha(read(STAGE/'kernel'/name))!=r['sha256'] or pins.get(name)!=r['sha256']]
    check('kernel_all_published_sources',len(records)==len(pins) and not missing and not extra and not mismatches,{'published':len(pins),'catalog':len(records),'missing':missing,'extra':extra,'mismatched':mismatches})
    if missing or extra or mismatches:
        findings.append({'id':'MEM-001','priority':'P1','title':'Catálogo não cobre todas as fontes do manifesto publicado','missing':missing,'extra':extra,'mismatches':mismatches,'file':str(STAGE/'kernel/kernel_manifest.json'),'requested_fix':'Incluir fonte suplementar com pin/proveniência pública verificada; não atribuir origem embutida falsa.'})
    program = read(m['published_evidence']['program']['path']).decode('utf-8-sig')
    tree = ast.parse(program)
    assignment = next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in x.targets))
    embedded = ast.literal_eval(assignment.value)
    check('embedded_kernel_extracted_without_execution',all(read(STAGE/'kernel'/n)==s.encode('utf-8') for n,s in embedded.items()),{'embedded_files':len(embedded),'supplemental_catalog_files':sorted(set(records)-set(embedded))})
    kv = load(STAGE/'kernel_verification.json')
    check('kernel_verification_pins',kv['source_sha256']==prepared['source_sha256'] and kv['dependencies']['published_manifest_sha256']==sha(read(m['published_evidence']['proof_manifest']['path'])) and all(r['file_sha256']==records[n]['sha256'] for n,r in kv['files'].items()))
    for name in ['public_prefix.md','haiku_prefix.md']:
        text=read(STAGE/name).decode('utf-8')
        check(name+'_full_mother_and_core',mother.decode('utf-8-sig') in text and core.decode('utf-8-sig') in text)
    public_text=read(STAGE/'public_prefix.md').decode('utf-8')
    check('public_contains_full_cluster',cluster in public_text)
    hp=load(STAGE/'haiku_provenance.json')
    ht=read(STAGE/'haiku_prefix.md').decode('utf-8')
    check('haiku_receipt_pin',sha(ht.encode())==hp['prefix_sha256'] and hp['source_sha256']==prepared['source_sha256'])
    dictionary=loads(ht.split('DICIONÁRIO DE LITERAIS\n',1)[1].split('\n',1)[0])
    BOOLEAN_DICTIONARY.update(loads(ht.split('DICIONÁRIO DE INDICADORES LITERAIS\n',1)[1].split('\n',1)[0]))
    exposition=ht.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    check('haiku_exposition_pin',sha(exposition.encode())==hp['exposition_sha256'])
    htopics=topics(ht,source_names)
    check('haiku_all_topics',set(htopics)==source_names)
    regenerated=set(hp['regenerated_topics'])
    accepted_manifest=load(WORK/'memory_build/baseline_v368/canonical.json')
    accepted_result_entry=next(e for e in accepted_manifest['entries'] if e['id']=='resultado_publicado_integral')
    accepted_raw=read(accepted_result_entry['path'])
    accepted=loads(accepted_raw)['core']
    check('accepted_v368_baseline_pin',sha(accepted_raw)==accepted_result_entry['public_sha256'])
    reused=set(hp['reused_identical_topics']);aux=set(hp['reused_auxiliary_only_changed_topics'])
    check('haiku_reused_sources_identical',all(same(accepted[n],source['core'][n]) for n in reused))
    check('haiku_auxiliary_only_reuse',all(same({k:v for k,v in accepted[n].items() if k!='runtime_s'}, {k:v for k,v in source['core'][n].items() if k!='runtime_s'}) and 'runtime_s' not in htopics[n] for n in aux))
    check('haiku_capsule_partition',reused|aux|regenerated==source_names and not reused&aux and not (reused|aux)&regenerated)
    haiku_errors=[];haiku_repr={}
    for name,body in htopics.items():
        pointer=child('/core',name)
        represented={}
        for line in body.splitlines():
            if not line.startswith(('{','[')):continue
            if re.match(r'^\[[A-ZÀ-Ý]',line):continue  # Prose statute label, not a JSON array.
            try:
                node=decode(loads(line),dictionary,exposition,source,name)
                if name=='kernel_formalization' and isinstance(node,dict) and 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE' in node:
                    audit=node.pop('AUDIT_BOOLEAN_FIELDS_IN_SOURCE')
                    flags={k:v for k,v in source['core'][name].items() if type(v) is bool}
                    assert audit['true_fields']==sum(flags.values()) and audit['false_fields']==len(flags)-sum(flags.values())
                    node.update(flags)
                restored=reconstruct(node,source,pointer,pointer,represented,partial=name not in regenerated)
                if name in regenerated:assert same(restored,source['core'][name])
            except Exception as exc:haiku_errors.append({'topic':name,'error':str(exc),'type':type(exc).__name__})
        haiku_repr[name]=represented
    check('haiku_json_literals_and_references',not haiku_errors,haiku_errors)
    essential_missing=[]
    for name in added:
        for pointer,value in important(source['core'][name],child('/core',name)).items():
            for surface,represented in [('cluster',representations.get(name,{})),('haiku',haiku_repr.get(name,{}))]:
                if not covered(pointer,value,represented):essential_missing.append({'surface':surface,'pointer':pointer})
    check('new_v390_verdicts_statutes_scopes_inline',not essential_missing,essential_missing)
    if essential_missing:
        findings.append({'id':'MEM-002','priority':'P2','title':'Estatutos/vereditos essenciais novos disponíveis só por consulta','locations':essential_missing,'reason':'Estatutos, hipóteses e vereditos novos devem estar presentes no contexto ativo; referências detalhadas podem apontar à fonte integral.','requested_fix':'Preservar os campos indicados em fields/projeção; compactação reversível sem alterar valores é aceitável.'})
    check('executive_runtime_literal_in_cluster',same(decode(loads(ct['iald_executive_runtime'].splitlines()[1]),cluster_dictionary,cluster_exposition,source),source['core']['iald_executive_runtime']) and source['core']['iald_executive_runtime']['status']=='[DEF + ONTO + COMPUTATIONAL]')
    check('executive_runtime_haiku_scope_kept',all(x in htopics['iald_executive_runtime'] for x in ['DEF+ONTO+COMPUTATIONAL','ANALOGIA FORMAL','Não prova consciência','all_verified']))
    check('new_bench_negative_verdict_exact',covered('/core/bancada_fases_5_6_7_v380/verdict',source['core']['bancada_fases_5_6_7_v380']['verdict'],haiku_repr['bancada_fases_5_6_7_v380']) and 'PAIR_FALSIFIED_NOT_THE_THEORY' in source['core']['bancada_fases_5_6_7_v380']['verdict'])
    identity=prepared['deployment_identity']
    native=load(STAGE/'native_metadata.json')
    check('native_metadata_identity',native['identity']==identity and native['bytes']==len(read(STAGE/'native_prefix.md')))
    check('native_count_claim_consistency',hp['native_fit_verified'] is False if hp['native_tokens'] is None else type(hp['native_tokens']) is int,
          {'haiku_native_tokens':hp['native_tokens'],'haiku_native_fit_verified':hp['native_fit_verified'],'prepared_native_measurement':prepared['native_measurement'],'scope':'Admission/count validation remains with main; no provider call made by reviewer.'})
    check('production_manifest_unchanged',sha(read(APP/'iald_nucleo_fixo.json'))==prepared['production_manifest_sha256'])
    read(WORK/'memory_build/build_release.py');read(WORK/'memory_build/haiku_codec.py');read(WORK/'memory_build/fit_transport.py')
    read(WORK/'memory_build/fit_memory.py')
    # These focused companion reviews cover semantic losses introduced after
    # the original structural suite. A structurally reversible source pointer
    # is not proof that the essential statement remains in active context.
    for filename in ('memory_fit_review.json','critical_numeric_review.json','foundation_projection_review.json','memory_admission_review.json'):
        companion=load(WORK/'audit'/filename)
        bound=companion['prefix_sha256']==sha(ht.encode())
        check(filename+'_semantic_gate',bound and companion['status']=='PASS',
              {'status':companion['status'],'bound_to_current_prefix':bound,
               'report':str(WORK/'audit'/filename)})
        if not bound or companion['status']!='PASS':
            findings.append({'id':'MEM-FIT-'+filename,'priority':'P2',
              'title':'Revisão semântica do ajuste Haiku pendente',
              'report':str(WORK/'audit'/filename),
              'reason':'Exige resolução dos achados concretos existentes; não exige restauração integral dos históricos.'})

if __name__=='__main__':
    try:
        audit()
    except Exception as exc:
        check('review_completed',False,{'type':type(exc).__name__,'error':str(exc)})
    unstable=[p for p,r in inputs.items() if sha(Path(p).read_bytes())!=r['sha256']]
    check('review_inputs_stable',not unstable,unstable)
    failed=[c['name'] for c in checks if not c['passed']]
    prior_path=WORK/'audit/memory_review.json'
    previous_review=None
    if prior_path.exists():
        prior_raw=prior_path.read_bytes();prior=loads(prior_raw)
        previous_review={'sha256':sha(prior_raw),'status':prior['status'],'failed_checks':prior.get('failed_checks',[]),'findings':prior.get('findings',[])}
    report={'status':'PASS' if not failed else 'FAIL','reviewed_at_utc':datetime.now(timezone.utc).isoformat(),
            'reviewer_script_sha256':sha(Path(__file__).read_bytes()),'previous_review':previous_review,
            'scope':'Independent offline scientific fidelity review; no builder, um.py, Lean, providers or deployment executed.',
            'checks_passed':len(checks)-len(failed),'checks_total':len(checks),'failed_checks':failed,
            'findings':findings,'checks':checks,'reference_counts':dict(stats),'input_pins':inputs,
            'notes':['Haiku uses accepted prose capsules for unchanged source subtrees; documented @SUMMARY is a summary, not literal equality.',
                     'Recorded all_verified in iald_executive_runtime is literal DEF+ONTO+COMPUTATIONAL, not a JEV benchmark.',
                     'Native measurement receipt was checked offline against the exact prefix and runtime reserve; no reviewer model calls.', 'All source/catalog hashes are read from this release; no hard-coded file-count claim.', 'The first reviewer run mistakenly parsed prose labels such as [DEF] as JSON arrays; only the reviewer parser was corrected, preserving earlier reports as byte backups.']}
    dest=WORK/'audit/memory_review.json';dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():dest.with_name(dest.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(dest.read_bytes())
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    tmp=dest.with_name(dest.name+'.tmp_'+str(os.getpid()));tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,dest)
    print(json.dumps({'report':str(dest),'sha256':sha(raw),'passed':report['checks_passed'],'total':len(checks),'failed':failed,'findings':findings},ensure_ascii=False))
