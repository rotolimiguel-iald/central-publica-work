"""Revisor sonnet-app-v407-revisor -- RODADA 2 (instalacao): D1, D2, D3, D4(a) e D6. Somente leitura.
ADAPTADO de check_d1_d4.py do revisor da v406 (-d): mesmas perguntas, numeros da v407; nao importa verify_installed.py; recalcula tudo dos bytes."""
import json, os, re, sys, time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2lib as L
L.install_guard()
W, R, REL, HERE = L.W, L.R, L.REL, L.HERE
sha_file, sha_bytes, norm, rd = L.sha_file, L.sha_bytes, L.norm, L.rd
PIN = '833121339e649f7171e2eccca1a19b3a1564aa306a787ed8cea76ded0fdf3475'
res = {'checks': {}, 'numbers': {}}
plan_raw = (W / 'install_plan.json').read_bytes()
plan_sha = sha_bytes(plan_raw)
plan = json.loads(plan_raw)
files = plan['files']
rf = rd(W / 'validation/review_final.json')
dep = rd(W / 'deployment.json')
fc = rd(W / 'validation/final_checks.json')
t_deploy_start = os.stat(W / 'deploy_stderr.txt').st_mtime   # o shell abre o redirecionamento imediatamente antes do python

# ------------------------------------------------------------------ D1
tools_now = {n: sha_file(W / n) for n in ('deploy_controlled.py', 'transaction.py', 'maintenance.py', 'verify_installed.py')}
tools_rec = {'deploy_controlled.py': rf['deploy_controlled_sha256'], 'transaction.py': rf['transaction_sha256'], 'maintenance.py': rf['maintenance_sha256'], 'verify_installed.py': rf['verify_installed_sha256']}
rf_now = sha_file(W / 'validation/review_final.json')
d1 = {'plan_sha256_recalculado': plan_sha, 'review_final.plan_sha256': rf['plan_sha256'], 'deployment.plan_sha256': dep['plan_sha256'], 'final_checks.plan_sha256': fc['plan_sha256'],
      'tools_recalculados': {k: v[:16] for k, v in tools_now.items()}, 'tools_gravados_no_review_final': {k: v[:16] for k, v in tools_rec.items()},
      'review_final.status': rf['status'], 'review_final.reviewer': rf['reviewer'], 'review_final.checks': len(rf['checks']), 'review_final_sha256_hoje': rf_now,
      'review_final_sha256_pinado_no_aceite_da_rodada_1': '33dd393f24d01f6f2ba7e82f7c20c3371c6eace4abd82f813b383a8f3542a815'}
d1['PASS'] = (plan_sha == rf['plan_sha256'] == dep['plan_sha256'] == fc['plan_sha256'] and all(tools_now[k] == tools_rec[k] for k in tools_now) and rf['status'] == 'PASS'
              and rf_now == d1['review_final_sha256_pinado_no_aceite_da_rodada_1'] and dep['status'] == 'INSTALLED_RESTART_REQUIRED')
res['checks']['D1'] = d1

# ------------------------------------------------------------------ D2
bad, missing, errs, src_bad, dep_bad = [], [], [], [], []
total_bytes = 0
t0 = time.time()
for it in files:
    dest = Path(it['destination'])
    try:
        if not dest.is_file():
            missing.append(str(dest)); continue
        h = sha_file(dest)
        total_bytes += dest.stat().st_size
        if h != it['sha256']:
            bad.append({'dest': str(dest), 'disk': h[:16], 'plano': it['sha256'][:16]})
        if dep['files'].get(str(dest)) != it['sha256']:
            dep_bad.append(str(dest))
        src = Path(it['source'])
        if not src.is_file():
            src_bad.append('AUSENTE:' + str(src))
        elif sha_file(src) != it['sha256']:
            src_bad.append(str(src))
    except Exception as e:
        errs.append({'dest': str(dest), 'err': repr(e)})
d2 = {'arquivos_no_plano': len(files), 'ok_no_disco': len(files) - len(bad) - len(missing) - len(errs), 'n_divergentes': len(bad), 'divergentes': bad[:10], 'n_ausentes': len(missing), 'ausentes': missing[:10], 'n_erros': len(errs), 'erros': errs[:5],
      'bytes_totais_instalados': total_bytes, 'deployment.files_entradas': len(dep['files']), 'deployment.files_divergem_do_plano': len(dep_bad), 'staging_diverge_do_plano': len(src_bad), 'staging_exemplos': src_bad[:5], 'segundos': round(time.time() - t0, 1)}
d2['PASS'] = (len(files) == 1782 and not bad and not missing and not errs and len(dep['files']) == len(files) and not dep_bad and not src_bad)
res['checks']['D2'] = d2

# ------------------------------------------------------------------ D3
back = dep['backups']
base_items = [it for it in files if it.get('baseline')]
changed_items = [it for it in base_items if it['baseline'] != it['sha256']]
rows, ok3, stamps = [], True, set()
for it in changed_items:
    dest = it['destination']
    bp = back.get(dest)
    row = {'dest': dest.replace(str(R) + L.BS, ''), 'baseline_plano': it['baseline'][:16], 'novo_plano': it['sha256'][:16]}
    if not bp:
        row['backup'] = None; ok3 = False
    else:
        b = Path(bp)
        row['backup'] = b.name
        row['ao_lado'] = (norm(b.parent) == norm(Path(dest).parent)) and b.name.startswith(Path(dest).name + '.bak_')
        stamps.add(b.name.split('.bak_')[-1])
        if b.is_file():
            hb = sha_file(b)
            row['backup_igual_baseline'] = (hb == it['baseline'])
            row['backup_difere_do_novo'] = (hb != it['sha256'])
        else:
            row['backup_existe'] = False
        ok3 = ok3 and bool(row.get('ao_lado') and row.get('backup_igual_baseline') and row.get('backup_difere_do_novo'))
    rows.append(row)
extra_keys = [k for k in back if k not in {it['destination'] for it in changed_items}]
stamp = sorted(stamps)[0] if stamps else None
d3 = {'destinos_existentes_no_plano(baseline)': len(base_items), 'destinos_com_bytes_diferentes': len(changed_items), 'backups_no_deployment': len(back), 'carimbos': sorted(stamps), 'backups_sem_correspondente': extra_keys, 'linhas': rows,
      'mobile_backups_existe': (W / 'mobile_backups').exists(), 'rollback_new_files_existe': (W / 'rollback_new_files').exists()}
d3['PASS'] = (len(changed_items) == 7 and len(back) == 7 and ok3 and len(stamps) == 1 and not extra_keys and not d3['mobile_backups_existe'] and not d3['rollback_new_files_existe'])
res['checks']['D3'] = d3

# ------------------------------------------------------------------ D4(a): destinos por categoria, RUNTIME_BASELINE, .py de runtime
cats = {'release_v407': 0, 'core_packet_raiz': 0, 'haiku55': 0, 'haiku': 0, 'manifesto_ativo': 0, 'FORA': []}
for it in files:
    d = Path(it['destination']); n = norm(d)
    if n.startswith(norm(REL) + os.sep):
        cats['release_v407'] += 1
    elif n == norm(R / 'core_packet_v407_bound.txt'):
        cats['core_packet_raiz'] += 1
    elif norm(d.parent) == norm(R / '.iald_runtime' / 'haiku55'):
        cats['haiku55'] += 1
    elif norm(d.parent) == norm(R / '.iald_runtime' / 'haiku'):
        cats['haiku'] += 1
    elif n == norm(R / 'iald_nucleo_fixo.json'):
        cats['manifesto_ativo'] += 1
    else:
        cats['FORA'].append(str(d))
plan_rel = {norm(it['destination']) for it in files if norm(it['destination']).startswith(norm(REL) + os.sep)}
disk_rel = set()
for dp, dn, fn in os.walk(REL):
    for f in fn:
        disk_rel.add(norm(os.path.join(dp, f)))
extras_rel, faltam_rel = sorted(disk_rel - plan_rel), sorted(plan_rel - disk_rel)
tmp_left = []
for base in (R, R / '.iald_runtime' / 'haiku55', R / '.iald_runtime' / 'haiku'):
    tmp_left += [str(p) for p in base.glob('*.tmp_v380_*')]
for dp, dn, fn in os.walk(REL):
    tmp_left += [os.path.join(dp, f) for f in fn if '.tmp_v380_' in f]
rb = rd(W / 'app/RUNTIME_BASELINE.json')['files']
man_dest = norm(R / 'iald_nucleo_fixo.json')
rb_bad, rb_missing = [], []
man_entry = None
for e in rb:
    p = Path(e['path'])
    if norm(p) == man_dest:
        man_entry = e; continue
    if not p.is_file():
        rb_missing.append(str(p)); continue
    if sha_file(p) != e['sha256']:
        rb_bad.append(str(p))
last = files[-1]
bkp_man = back.get(last['destination'])
man_now = sha_file(R / 'iald_nucleo_fixo.json')
bak_sha = sha_file(bkp_man) if bkp_man and Path(bkp_man).is_file() else None
top_py_changed = []
for p in R.iterdir():
    try:
        if p.is_file() and p.suffix == '.py' and p.stat().st_mtime >= t_deploy_start:
            top_py_changed.append(p.name)
    except OSError:
        pass
d4a = {'categorias_dos_destinos': {k: (v if k != 'FORA' else len(v)) for k, v in cats.items()}, 'destinos_fora_do_escopo': cats['FORA'][:5],
       'extras_no_diretorio_da_release': len(extras_rel), 'extras_exemplos': extras_rel[:3], 'ausentes_no_diretorio_da_release': len(faltam_rel), 'restos_tmp_v380': tmp_left[:5],
       'RUNTIME_BASELINE_entradas': len(rb), 'RUNTIME_BASELINE_intactos_sem_o_manifesto': (len(rb) - 1) - len(rb_bad) - len(rb_missing), 'RUNTIME_BASELINE_divergentes': rb_bad[:5], 'RUNTIME_BASELINE_ausentes': rb_missing[:5],
       'manifesto': {'baseline_no_RUNTIME_BASELINE': man_entry['sha256'][:16] if man_entry else None, 'baseline_no_plano': last['baseline'][:16], 'backup_bytes_sha': (bak_sha or '')[:16], 'backup_igual_baseline': bak_sha == (man_entry or {}).get('sha256') == last['baseline'],
                     'novo_no_plano': last['sha256'][:16], 'novo_no_disco': man_now[:16], 'disco_igual_plano': man_now == last['sha256']},
       'py_na_raiz_modificados_desde_o_inicio_do_deploy': top_py_changed}
d4a['PASS'] = (not cats['FORA'] and cats['release_v407'] == 1774 and cats['core_packet_raiz'] == 1 and cats['haiku55'] == 3 and cats['haiku'] == 3 and cats['manifesto_ativo'] == 1
               and not extras_rel and not faltam_rel and not tmp_left and len(rb) == 171 and not rb_bad and not rb_missing and d4a['manifesto']['backup_igual_baseline'] and d4a['manifesto']['disco_igual_plano'] and not top_py_changed)
res['checks']['D4a'] = d4a

# ------------------------------------------------------------------ D6: manifesto ativo
mf_raw = (R / 'iald_nucleo_fixo.json').read_bytes()
mf = json.loads(mf_raw)
stage_mf = Path(last['source'])
mi_sha = sha_file(W / 'app/science/memory_stage/manifest_install.json')
paths = []
def walk(o, trail=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'path' and isinstance(v, str):
                paths.append((trail, v, o.get('sha256')))
            else:
                walk(v, trail + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, trail + '[%d]' % i)
walk(mf)
fora, nao_existe, sha_div, ver = [], [], [], 0
for trail, pth, h in paths:
    pp = Path(pth)
    inside = norm(pp).startswith(norm(REL) + os.sep) or norm(pp) == norm(R / 'core_packet_v407_bound.txt')
    if not inside:
        fora.append({'trail': trail, 'path': pth})
    if not pp.is_file():
        nao_existe.append(pth)
    elif h and len(h) == 64:
        ver += 1
        if sha_file(pp) != h:
            sha_div.append(pth)
jev_path = Path(mf['jev_control']['path'])
d6 = {'ultimo_do_plano_e_o_manifesto': norm(last['destination']) == man_dest, 'indice_no_plano': files.index(last), 'total_plano': len(files),
      'sha_manifesto_no_disco': man_now, 'sha_manifest_install_staging': mi_sha, 'sha_no_plano': last['sha256'],
      'operational_core.current_release': mf['operational_core']['current_release'], 'operational_core.release_source_sha256_igual_pino': mf['operational_core']['release_source_sha256'] == PIN,
      'active_cluster.release': mf['active_cluster']['release'], 'active_cluster.commit': mf['active_cluster']['commit'], 'active_cluster.publication_pending': mf['active_cluster'].get('publication_pending'),
      'jev_control.release': mf['jev_control'].get('release'), 'jev_control.arquivo': jev_path.name, 'jev_control.sha256_igual_ao_arquivo_instalado': mf['jev_control']['sha256'] == sha_file(jev_path), 'jev_control.source_sha256_igual_pino': mf['jev_control'].get('source_sha256') == PIN,
      'campos_path_no_manifesto': len(paths), 'paths_fora_da_release_v407': fora[:5], 'n_paths_fora': len(fora), 'paths_inexistentes': nao_existe[:5], 'paths_com_sha_verificados': ver, 'paths_sha_divergentes': sha_div[:5],
      'caminhos_sob_canonical_releases_v407_bf9017157406_no_plano': len(plan_rel), 'arquivos_no_disco_sob_o_alvo': len(disk_rel), 'alvo': str(REL)}
d6['PASS'] = (d6['ultimo_do_plano_e_o_manifesto'] and d6['indice_no_plano'] == len(files) - 1 and mf['operational_core']['current_release'] == 'v407' and mf['active_cluster']['release'] == 'v407' and mf['jev_control'].get('release') == 'v407'
              and man_now == mi_sha == last['sha256'] and d6['operational_core.release_source_sha256_igual_pino'] and d6['jev_control.sha256_igual_ao_arquivo_instalado'] and d6['jev_control.source_sha256_igual_pino']
              and mf['active_cluster']['commit'] == 'bf9017157406afa6b4dc05c6a9d566129e6a6ee4' and not mf['active_cluster'].get('publication_pending') and not fora and not nao_existe and not sha_div
              and len(plan_rel) == len(disk_rel) == 1774)
res['checks']['D6'] = d6
res['hashes_das_evidencias'] = {n: sha_file(W / n) for n in ('deployment.json', 'maintenance.json', 'restart.json', 'deploy_stdout.txt', 'deploy_stderr.txt', 'install_plan.json')}
res['guard_events'] = {k: (v if not isinstance(v, list) else len(v)) for k, v in L.EVENTS.items()}
(L.HERE / 'r2_d1_d6_out.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
for k, v in res['checks'].items():
    slim = {kk: vv for kk, vv in v.items() if kk not in ('linhas',)}
    print(k, 'PASS' if v['PASS'] else 'FAIL', json.dumps(slim, ensure_ascii=False)[:1400])
print('guard', res['guard_events'])
