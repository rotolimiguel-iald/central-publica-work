from pathlib import Path
import datetime, hashlib, json, re, sys

W = Path(__file__).resolve().parents[1]
# Reuse the local documentary checks, without rewriting the preparation receipt.
namespace = {'__file__': str(W/'review/prepare_deploy_review.py')}
source = (W/'review/prepare_deploy_review.py').read_text(encoding='utf-8')
exec(compile(source.split('failed = [c for c in checks')[0], str(W/'review/prepare_deploy_review.py'), 'exec'), namespace)
check, read, digest = (namespace[k] for k in ('check', 'read', 'digest'))
checks, evidence = namespace['checks'], namespace['evidence']
delivery = read('delivery.json')
ios = read('IOS_DISTRIBUTION.json')
matrix = read('AVAILABILITY_MATRIX.json')
memory = read('MEMORY_APPLIED.json')
admin = read('ADMIN_BUILD36_UPDATED.json')
submitted = read('DEPLOY_SUBMITTED.json')
check('delivery_plan_commit', delivery['plan_sha256'] == digest(W/'install_plan.json') and delivery['commit'] == ios['commit'] == namespace['push']['commit'])
check('availability_matrix', all(delivery[k] == v for k,v in matrix.items()))
check('ios_both_groups', ios['status'] == 'BOTH_GROUPS_VERIFIED' and ios['build'] == '4.1(36)' and ios['internal']['status'] == ios['external']['status'] == 'Em testes' and ios['internal']['testers'] == 1 and ios['external']['testers'] == 6 and ios['internal']['operator_participation_verified'])
for item in ios['sources']:
    check('ios_source:'+Path(item['path']).name, digest(item['path']) == item['sha256'])
    evidence[item['path']] = digest(item['path'])
cloud = (W/'IOS36_CLOUD_SUCCESS.txt').read_text(encoding='utf-8')
check('cloud_success_commit_documented', ios['commit'] in cloud and 'Processada com sucesso' in cloud and ios['cloud_build_id'] in cloud)
for name in ['IOS36_EQUIPE.txt', 'IOS36_PILOTO.txt']:
    text = (W/name).read_text(encoding='utf-8')
    row = re.search(r'row Compilação 4\.1 \(36\).*?(?=\n[^\n]*\brow |\Z)', text, re.S)
    check('group36_testing_row:'+name, row is not None and 'Em testes' in row.group() and ios['testflight_build_id'] in row.group())
operator = (W/'IOS36_OPERATOR.txt').read_text(encoding='utf-8')
check('operator_participation_and_old_install', 'IALD Equipe' in operator and 'Luiz Antonio Rotoli Miguel' in operator and re.search(r'Instalado 4\.1\s*\(\s*35\s*\)', operator))
check('explicit_limits', not delivery['physical_installation_verified'] and not ios['physical_installation_verified'] and delivery['google_play'] == 'NOT_PUBLISHED_THIS_DELIVERY' and delivery['provider_calls'] == 0 and 'not implemented' in delivery['compression'])
check('eight_memory_surfaces', len(memory['surfaces']) == 8 and memory['status'] == 'APPLIED_8_ADDITIVE_SURFACES')
appendices = []
for item in memory['surfaces']:
    old = Path(item['backup']).read_bytes(); current = Path(item['path']).read_bytes()
    check('memory_backup:'+item['path'], hashlib.sha256(old).hexdigest() == item['before_sha256'])
    check('memory_current:'+item['path'], hashlib.sha256(current).hexdigest() == item['after_sha256'])
    check('memory_append_only:'+item['path'], current.startswith(old) and len(current) > len(old))
    appendices.append(current[len(old):])
check('same_factual_appendix_eight_surfaces', len(set(appendices)) == 1 and b'IALD_READABILITY_RELIABLE_TOOLS_20261021' in appendices[0])
appendix = appendices[0].decode('utf-8')
check('memory_claims_scoped', 'não implantada' in appendix and 'Não reduz tokens após descompactação nem demonstra ganho de latência' in appendix and 'não é instalação física' in appendix and 'GooglePlay não publicado' in appendix)
admin_path = Path(r'C:\IALD\projetos_pyhton\IALD\iald_deadlines.json')
before_raw = Path(admin['backup']).read_bytes(); after_raw = admin_path.read_bytes()
check('admin_backup_current_source_pins', hashlib.sha256(before_raw).hexdigest() == admin['before_sha256'] and hashlib.sha256(after_raw).hexdigest() == admin['after_sha256'] and digest(W/'IOS_DISTRIBUTION.json') == admin['source_sha256'])
before, after = json.loads(before_raw), json.loads(after_raw)
keys = ['testflight_internal','testflight_external']
for key in keys:
    check('admin_subtree:'+key, after['items'][key]['build'] == '4.1 (36)' and after['items'][key]['status'] == 'Em testes' and after['items'][key]['source_reference']['sha256'] == digest(W/'IOS_DISTRIBUTION.json'))
    after['items'][key] = before['items'][key]
check('admin_other_semantics_preserved', after == before)
def outside_subtrees(raw):
    text = raw.decode('utf-8'); spans = []
    for key in keys:
        start = re.search(r'"'+key+r'"\s*:\s*', text).end()
        _, length = json.JSONDecoder().raw_decode(text[start:]); spans.append((start,start+length))
    for start,end in sorted(spans,reverse=True): text = text[:start]+'<ADMIN_SUBTREE>'+text[end:]
    return text.encode('utf-8')
check('admin_other_bytes_preserved', outside_subtrees(before_raw) == outside_subtrees(after_raw))
sys.path.insert(0,str(W)); import task
projection = task.project()
deploy = next(t for t in projection['projection']['active'] if t['id'] == 'deploy')
check('real_distinct_submission', deploy['status'] == 'review_pending' and deploy['submitted_by'] == 'codex-app-01a094df')
for item in deploy['evidence']:
    check('submitted_evidence:'+Path(item['path']).name, digest(item['path']) == item['sha256'])
failed = [c for c in checks if not c['passed']]
report = dict(status='BLOCK' if failed else 'PASS', reviewer='codex-readability-reviewer', scope='FINAL_DEPLOY_DOCUMENTARY_REVIEW', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), plan_sha256=digest(W/'install_plan.json'), delivery_sha256=digest(W/'delivery.json'), checks=checks, findings=failed, evidence=[dict(path=p,sha256=h) for p,h in evidence.items()], submission_revision=projection['receipt']['revision'], availability=matrix, limits=['Revisão documental e de integridade local; UI, assinatura, rede e testes existentes não reproduzidos.', 'Nenhuma inferência de causalidade ou ganho de compressão; proposta não implementada.', 'Google Play não publicado; instalação física não verificada; Apple observava build35 instalada no operador.', 'Aceite operacional separado abaixo; nenhum gate científico ou quadro alterado.'], deployment_accepted=False, new_tests=0, provider_calls=0)
def save(path, value):
    raw = json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    if path.exists():
        old = path.read_bytes(); backup = path.with_name(path.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')); backup.write_bytes(old); assert backup.read_bytes() == old
    tmp = path.with_suffix('.json.tmp'); tmp.write_bytes(raw); assert tmp.read_bytes() == raw; tmp.replace(path)
report['reviewer_check_correction'] = 'Comparações corrigidas para o estado real review_pending e o texto nem demonstra ganho de latência. BLOCK intermediário preservado em backup; nenhuma alteração na entrega.'
out = W/'review/FINAL_REVIEW.json'; save(out, report)
print(json.dumps(dict(status=report['status'],checks=len(checks),failed=failed,report=str(out)),ensure_ascii=False),flush=True)
if failed: raise SystemExit(2)
# Recheck the reviewed evidence immediately before the independent CAS acceptance.
assert all(digest(p) == h for p,h in evidence.items())
result = task.act('accept', actor='codex-readability-reviewer', task_id='deploy', event_id='readability-independent-deploy-accept-final-r1', review_evidence=[dict(path=str(out),sha256=digest(out))])
save(W/'review/DEPLOY_ACCEPTED.json', result)
print(json.dumps(dict(receipt=result.get('receipt'),task=result.get('task'),artifact=str(W/'review/DEPLOY_ACCEPTED.json')),ensure_ascii=False))
