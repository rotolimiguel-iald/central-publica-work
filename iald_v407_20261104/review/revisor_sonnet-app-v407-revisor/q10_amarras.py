"""Revisor sonnet-app-v407-revisor -- Q10 (amarras) e D4 reescrito executavel. Somente leitura no runtime e na release; testes do D4 em raiz de brinquedo dentro desta pasta.
Nao roda review_app.py aqui (isso e' o Q8, rodado uma unica vez a parte). Le o texto de deploy_controlled.py / review_app.py / transaction.py e compara bytes com a v406."""
import hashlib, json, os, re, shutil, sys, time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import d4_check as D

W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
W6 = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
chk, out = [], {}


def ck(name, ok, **info):
    chk.append({'name': name, 'pass': bool(ok), **info})


dc = (W / 'deploy_controlled.py').read_text('utf-8')
ra = (W / 'review/review_app.py').read_text('utf-8')
tx = (W / 'transaction.py').read_text('utf-8')
# --- Q10.1 amarras
ck('Q10.deploy_controlled_requires_transaction_sha256', "review['transaction_sha256']==digest((W/'transaction.py').read_bytes())" in dc)
ck('Q10.deploy_controlled_requires_maintenance_sha256', "review['maintenance_sha256']==digest((W/'maintenance.py').read_bytes())" in dc)
ck('Q10.deploy_controlled_requires_review_PASS_and_plan_sha', "review['status']=='PASS' and review['plan_sha256']==digest((W/'install_plan.json').read_bytes())" in dc and "assert task.check('deploy')['ready']" in dc)
ck('Q10.review_app_writes_transaction_and_maintenance_sha256', "'transaction_sha256':sha(B/'transaction.py')" in ra and "'maintenance_sha256':sha(B/'maintenance.py')" in ra and "'plan_sha256':sha(B/'install_plan.json')" in ra and "'deploy_controlled_sha256'" in ra and "'verify_installed_sha256'" in ra)
ck('Q10.apply_plan_requires_validation_and_review_plan_hash', "validation['plan_sha256'] != plan_sha256" in tx and "review['status'] != 'PASS' or review['plan_sha256'] != plan_sha256" in tx)
ck('Q10.review_app_refuses_builder_and_owner_as_reviewer', "assert REVIEWER not in (cfg.owner,cfg.builder)" in ra)
ck('Q10.review_app_writes_review_final_with_x_mode_so_runs_once', "open('x'" in ra and not (W / 'validation/review_final.json').exists(), exists_now=(W / 'validation/review_final.json').exists())
# bytes das ferramentas
tools = {}
for nm in ('maintenance.py', 'deploy_controlled.py', 'verify_installed.py', 'review/review_app.py', 'mission_step.py', 'verify_sources.py'):
    tools[nm] = {'equal_v406': (W / nm).read_bytes() == (W6 / nm).read_bytes(), 'sha16_v407': sha((W / nm).read_bytes())[:16]}
out['tools_vs_v406'] = tools
ck('Q10.maintenance_deploy_verify_review_app_bytes_equal_v406', all(tools[n]['equal_v406'] for n in ('maintenance.py', 'deploy_controlled.py', 'verify_installed.py', 'review/review_app.py')), **{k: v['equal_v406'] for k, v in tools.items()})
fc = rd(W / 'validation/final_checks.json')
ck('Q10.final_checks_plan_sha_equals_current_install_plan', fc['passed'] is True and fc['plan_sha256'] == sha((W / 'install_plan.json').read_bytes()) and fc['test_count'] == 11 and fc['production_mutations'] == 0 and fc['provider_calls_this_validation'] == 0, plan_sha16=sha((W / 'install_plan.json').read_bytes())[:16], tests=[t['status'] for t in fc['tests']])
# nenhuma versao velha cravada nas ferramentas de implantacao
stale = {nm: sorted(set(re.findall(r'\bv40[0-6]\b', (W / nm).read_text('utf-8')))) for nm in ('deploy_controlled.py', 'maintenance.py', 'verify_installed.py', 'review/review_app.py', 'verify_sources.py', 'mission_step.py')}
out['stale_version_literals_in_tools'] = stale
ck('Q10.no_stale_version_literal_in_deploy_tools', not any(stale.values()), stale=stale)
# estado da missao ainda nao tem deployment/restart/maintenance (nada instalado)
ck('Q10.nothing_installed_yet_no_deployment_restart_maintenance_files', not any((W / n).exists() for n in ('deployment.json', 'restart.json', 'maintenance.json', 'INSTALLED_VERIFICATION.json')))
ck('Q10.installed_runtime_is_still_v406', json.loads((R / 'iald_nucleo_fixo.json').read_bytes())['active_cluster']['release'] == 'v406')

# --- D4 reescrito: executavel? (1) sobre o estado ATUAL (pre-instalacao), (2) em raiz de brinquedo simulando a instalacao + perturbacoes
base = rd(W / 'app/RUNTIME_BASELINE.json')
plan = rd(W / 'install_plan.json')
intact_now = [Path(e['path']).is_file() and sha(Path(e['path']).read_bytes()) == e['sha256'] for e in base['files']]
man_dest = plan['files'][-1]['destination']
out['d4_live_pre_install'] = {'baseline_entries': len(base['files']), 'intact_now': sum(intact_now), 'manifest_is_in_baseline': any(os.path.normcase(e['path']) == os.path.normcase(man_dest) for e in base['files']),
                             'manifest_baseline16': next(e['sha256'] for e in base['files'] if os.path.normcase(e['path']) == os.path.normcase(man_dest))[:16], 'plan_manifest_baseline16': plan['files'][-1]['baseline'][:16], 'plan_manifest_new16': plan['files'][-1]['sha256'][:16],
                             'supervisor_logs_dir_exists': (R / 'logs').is_dir(), 'supervisor_log_names_now': sorted(p.name for p in (R / 'logs').iterdir())[-4:]}
ck('Q10.D4_live_pre_install_171_of_171_intact_and_manifest_baseline_equals_plan_baseline', sum(intact_now) == len(base['files']) == 171 and out['d4_live_pre_install']['manifest_baseline16'] == out['d4_live_pre_install']['plan_manifest_baseline16'], **out['d4_live_pre_install'])

TOY = HERE / 'toy_root_d4'


def build_toy():
    if TOY.exists():
        shutil.rmtree(TOY)
    (TOY / 'logs').mkdir(parents=True)
    (TOY / 'canonical_releases').mkdir()
    files = {'a.py': b'print(1)', 'b.json': b'{}', 'c.txt': b'c'}
    for n, b in files.items():
        (TOY / n).write_bytes(b)
    (TOY / 'iald_nucleo_fixo.json').write_bytes(b'MANIFEST-OLD')
    for p in TOY.rglob('*'):
        if p.is_file():
            os.utime(p, (1000, 1000))
    baseline = {'files': [{'path': str(TOY / n), 'sha256': sha(b), 'bytes': len(b)} for n, b in files.items()] + [{'path': str(TOY / 'iald_nucleo_fixo.json'), 'sha256': sha(b'MANIFEST-OLD'), 'bytes': 12}]}
    newfile = TOY / 'canonical_releases/v999/x.bin'
    plan_ = {'files': [{'source': 's', 'destination': str(newfile), 'sha256': sha(b'NEW'), 'baseline': None},
                       {'source': 's2', 'destination': str(TOY / 'iald_nucleo_fixo.json'), 'sha256': sha(b'MANIFEST-NEW'), 'baseline': sha(b'MANIFEST-OLD')}]}
    return baseline, plan_, newfile


def simulate_install(plan_, newfile, t_install=5000):
    bak = TOY / 'iald_nucleo_fixo.json.bak_20261104_000000_000000'
    bak.write_bytes(b'MANIFEST-OLD')
    newfile.parent.mkdir(parents=True, exist_ok=True)
    newfile.write_bytes(b'NEW')
    (TOY / 'iald_nucleo_fixo.json').write_bytes(b'MANIFEST-NEW')
    (TOY / 'logs/web-server_x.log').write_bytes(b'restart')
    (TOY / 'logs/web-supervisor.log').write_bytes(b'sup')
    for p in (bak, newfile, TOY / 'iald_nucleo_fixo.json', TOY / 'logs/web-server_x.log', TOY / 'logs/web-supervisor.log'):
        os.utime(p, (t_install, t_install))
    return {'backups': {str(TOY / 'iald_nucleo_fixo.json'): str(bak)}, 'files': {}}


d4res = {}
baseline, plan_, newfile = build_toy()
dep = simulate_install(plan_, newfile)
r = D.d4(TOY, baseline, plan_, dep, 4000, 6000)
d4res['simulated_clean_install'] = {'PASS': r['PASS'], 'expected': r['expected_in_window']}
# perturbacoes: cada uma deve DERRUBAR o D4
def perturb(label, fn):
    b, p, nf = build_toy(); d = simulate_install(p, nf); fn(b, p, nf, d)
    rr = D.d4(TOY, b, p, d, 4000, 6000)
    d4res[label] = {'PASS': rr['PASS'], 'failed_checks': [k for k, v in rr['checks'].items() if not v['ok']]}
perturb('runtime_py_modified', lambda b, p, nf, d: ((TOY / 'a.py').write_bytes(b'print(2)'), os.utime(TOY / 'a.py', (5000, 5000))))
perturb('baseline_file_deleted', lambda b, p, nf, d: (TOY / 'b.json').unlink())
perturb('manifest_backup_missing', lambda b, p, nf, d: Path(list(d['backups'].values())[0]).unlink())
perturb('manifest_backup_wrong_bytes', lambda b, p, nf, d: Path(list(d['backups'].values())[0]).write_bytes(b'OTHER'))
perturb('manifest_new_hash_not_plan', lambda b, p, nf, d: (TOY / 'iald_nucleo_fixo.json').write_bytes(b'MANIFEST-WRONG'))
perturb('stray_file_in_window', lambda b, p, nf, d: ((TOY / 'iald_users.json').write_bytes(b'u'), os.utime(TOY / 'iald_users.json', (5000, 5000))))
perturb('stray_inside_logs_is_expected_not_stray', lambda b, p, nf, d: ((TOY / 'logs/new_extra.log').write_bytes(b'x'), os.utime(TOY / 'logs/new_extra.log', (5000, 5000))))
out['d4_toy'] = d4res
shutil.rmtree(TOY, ignore_errors=True)
ck('Q10.D4_rewritten_is_executable_clean_install_passes_and_each_perturbation_fails', d4res['simulated_clean_install']['PASS'] and all(not d4res[k]['PASS'] for k in ('runtime_py_modified', 'baseline_file_deleted', 'manifest_backup_missing', 'manifest_backup_wrong_bytes', 'manifest_new_hash_not_plan', 'stray_file_in_window'))
   and d4res['stray_inside_logs_is_expected_not_stray']['PASS'], d4=d4res)

# --- nota de fidelidade: o D4 reescrito depende de 3 evidencias que a v407 gravara em deployment.json: backups (dict destino->backup), files, scope_measurement
ck('Q10.transaction_report_contains_backups_files_and_scope_measurement_keys', all(k in tx for k in ("'backups':backups", "'files':{str(p):digest(v) for p,v in new.items()}", "'scope_measurement':scope['scope_measurement']")))
json.dump({'out': out, 'checks': chk}, open(HERE / 'q10_amarras_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps({'n_checks': len(chk), 'fails': [c for c in chk if not c['pass']]}, ensure_ascii=False, indent=1)[:3500])
print(json.dumps(out, ensure_ascii=False)[:3000])
