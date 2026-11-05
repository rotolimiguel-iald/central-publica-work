"""Revisor sonnet-app-v407-revisor -- RODADA 2: extras de D3/D4/D5 sobre a ORDEM e o TEMPO das escritas (so' mtime e create_time; somente leitura).
Perguntas: (1) o plano foi escrito na ordem do plano, com o manifesto ativo POR ULTIMO? (2) cada backup e' anterior a escrita do seu destino? (3) o web novo so' nasceu depois da ultima escrita?
(4) quanto tempo o web ficou fora?"""
import json, os, sys
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2lib as L
L.install_guard()
import psutil
W, R, HERE = L.W, L.R, L.HERE
rd = L.rd
fmt = lambda t: datetime.fromtimestamp(t).strftime('%H:%M:%S.%f')[:-3]
plan, dep, rs = rd(W / 'install_plan.json'), rd(W / 'deployment.json'), rd(W / 'restart.json')
mt = [(i, os.stat(it['destination']).st_mtime) for i, it in enumerate(plan['files'])]
nondec = all(mt[i][1] <= mt[i + 1][1] for i in range(len(mt) - 1))
viol = [(i, fmt(mt[i][1]), fmt(mt[i + 1][1])) for i in range(len(mt) - 1) if mt[i][1] > mt[i + 1][1]]
man_i = len(plan['files']) - 1
bk = {}
for dest, b in dep['backups'].items():
    bm, dm = os.stat(b).st_mtime, os.stat(dest).st_mtime
    bk[dest.replace(str(R) + L.BS, '')] = {'backup_mtime': fmt(bm), 'destino_mtime': fmt(dm), 'backup_antes_do_destino': bm < dm}
last_write = max(m for _, m in mt)
new_ct = psutil.Process(rs['new_web_pid']).create_time()
t_mnt, t_rst = os.stat(W / 'maintenance.json').st_mtime, os.stat(W / 'restart.json').st_mtime
inst = datetime.fromisoformat(dep['installed_at']).timestamp()
out = {'ordem_de_escrita': {'mtimes_nao_decrescentes_na_ordem_do_plano': nondec, 'violacoes': viol[:5], 'primeiro': fmt(mt[0][1]), 'ultimo': fmt(mt[-1][1]), 'manifesto_e_o_ultimo_escrito_e_o_maximo': mt[man_i][1] == last_write,
                            'escrita_levou_s': round(last_write - mt[0][1], 2)},
       'backups': bk, 'backups_todos_antes_dos_destinos': all(v['backup_antes_do_destino'] for v in bk.values()),
       'tempo': {'ultima_escrita': fmt(last_write), 'installed_at': fmt(inst), 'web_novo_nasceu': fmt(new_ct), 'web_novo_nasceu_depois_da_ultima_escrita_s': round(new_ct - last_write, 2), 'janela_manutencao_s': round(t_rst - t_mnt, 2),
                 'v406_janela_s': 87},
       'deployment.json': {'accounts_modified_json': dep['accounts_modified'], 'bench_restarted_json': dep['bench_restarted'], 'client_files_changed_json': dep['client_files_changed'], 'tipo': [type(dep[k]).__name__ for k in ('accounts_modified', 'bench_restarted', 'client_files_changed')],
                           'errors': dep['scope_measurement']['errors'], 'bench_changed': dep['scope_measurement']['bench_changed'], 'state_changed': dep['scope_measurement']['state_changed'], 'client_changed': dep['scope_measurement']['client_changed'],
                           'plan_overlap': [dep['scope_measurement']['plan_overlap_before'], dep['scope_measurement']['plan_overlap_after']]}}
out['PASS'] = (nondec and out['ordem_de_escrita']['manifesto_e_o_ultimo_escrito_e_o_maximo'] and out['backups_todos_antes_dos_destinos'] and new_ct > last_write
               and all(t == 'bool' for t in out['deployment.json']['tipo']) and not out['deployment.json']['errors'] and not out['deployment.json']['bench_changed'])
(HERE / 'r2_extra_out.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('EXTRA', 'PASS' if out['PASS'] else 'FAIL')
print(json.dumps(out, ensure_ascii=False, indent=1)[:3500])
