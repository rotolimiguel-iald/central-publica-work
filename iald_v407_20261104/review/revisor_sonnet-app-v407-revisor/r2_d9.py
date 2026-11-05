"""Revisor sonnet-app-v407-revisor -- RODADA 2: D9 (parte desta rodada). Somente leitura.
(a) o rastro dos MEUS scripts da rodada (contadores do gancho de auditoria de cada saida); (b) a trilha do deploy: imports e destinos de rede do codigo de implantacao e texto das evidencias.
A parte dos CARREGADORES de producao (0 rede, 0 .env, provider_calls no INSTALLED_VERIFICATION.json) e' do D7/D9 da segunda mensagem: NAO e' feita aqui."""
import ast, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2lib as L
L.install_guard()
W, HERE = L.W, L.HERE
rd = L.rd
out = {'checks': {}}
# (a) rastro dos meus scripts
mine = {}
for n in ('r2_d1_d6_out.json', 'r2_d4_scope_out.json', 'r2_d5_out.json'):
    ge = rd(HERE / n)['guard_events']
    mine[n] = {k: (len(v) if isinstance(v, list) else v) for k, v in ge.items()}
tot = {k: sum(m[k] for m in mine.values()) for k in next(iter(mine.values()))}
out['rastro_dos_meus_scripts'] = {'por_script': mine, 'total': tot}
a_ok = (tot['socket_connect_blocked'] == 0 and tot['getaddrinfo_blocked'] == 0 and tot['subprocess_blocked'] == 0 and tot['os_system_blocked'] == 0 and tot['env_open_blocked'] == 0 and tot['secret_open_blocked'] == 0 and tot['write_outside_blocked'] == 0
        and tot['socket_connect_allowed'] == 1 and tot['getaddrinfo_allowed'] == 1)
out['checks']['a_rastro_dos_meus_scripts'] = {'PASS': a_ok, 'rede': 'so o GET permitido em 127.0.0.1:8082 (%d connect, %d getaddrinfo)' % (tot['socket_connect_allowed'], tot['getaddrinfo_allowed']), 'env_bloqueados': tot['env_open_blocked'], 'subprocessos': tot['subprocess_blocked']}
# (b) codigo de implantacao: imports e hosts
NET_MODS = {'socket', 'ssl', 'urllib', 'urllib.request', 'requests', 'httpx', 'aiohttp', 'anthropic', 'openai', 'ftplib', 'smtplib', 'websockets', 'http.server'}
code = {}
for n in ('deploy_controlled.py', 'transaction.py', 'maintenance.py', 'task.py', 'release_cfg.py'):
    t = ast.parse((W / n).read_text('utf-8'))
    imps = sorted({(a.name if isinstance(x, ast.Import) else x.module or '') for x in ast.walk(t) if isinstance(x, (ast.Import, ast.ImportFrom)) for a in (x.names if isinstance(x, ast.Import) else [ast.alias(name=x.module or '')])})
    hosts = []
    for x in ast.walk(t):
        if isinstance(x, ast.Call) and ((isinstance(x.func, ast.Attribute) and x.func.attr in ('HTTPConnection', 'HTTPSConnection')) or (isinstance(x.func, ast.Name) and x.func.id in ('HTTPConnection', 'HTTPSConnection'))):
            hosts.append((x.func.attr if isinstance(x.func, ast.Attribute) else x.func.id, x.args[0].value if x.args and isinstance(x.args[0], ast.Constant) else '<nao-constante>'))
    urls = re.findall(r'https?://[^\s\'"]+', (W / n).read_text('utf-8'))
    code[n] = {'imports': imps, 'imports_de_rede_ou_provedor': sorted(set(imps) & NET_MODS), 'http_client_hosts': hosts, 'urls_no_codigo': urls[:5]}
out['codigo'] = code
b_ok = (all(not v['imports_de_rede_ou_provedor'] for v in code.values()) and all(h[0] == 'HTTPConnection' and h[1] == '127.0.0.1' for v in code.values() for h in v['http_client_hosts']) and all(not v['urls_no_codigo'] for v in code.values()))
out['checks']['b_codigo_de_implantacao_sem_rede_externa_nem_provedor'] = {'PASS': b_ok, 'usa_http.client_so_para': sorted({(h[1]) for v in code.values() for h in v['http_client_hosts']}), 'subprocess_so_em_task.py': 'subprocess' in code['task.py']['imports'] and 'subprocess' not in code['transaction.py']['imports'] and 'subprocess' not in code['maintenance.py']['imports'] and 'subprocess' not in code['deploy_controlled.py']['imports']}
# (c) evidencias da instalacao: nenhuma pista de provedor/segredo
ev = {}
for n in ('deployment.json', 'maintenance.json', 'restart.json', 'deploy_stdout.txt', 'deploy_stderr.txt'):
    t = (W / n).read_text('utf-8')
    ev[n] = {'bytes': len(t.encode()), 'env': len(re.findall(r'\.env\b', t)), 'sk_key': len(re.findall(r'\bsk-[A-Za-z0-9_\-]{12,}', t)), 'provider_words': len(re.findall(r'(?i)provider|anthropic|openai|api[_-]?key|authorization|bearer|password|secret', t))}
out['evidencias'] = ev
out['checks']['c_evidencias_da_instalacao_sem_pista_de_provedor_ou_segredo'] = {'PASS': all(v['env'] == 0 and v['sk_key'] == 0 and v['provider_words'] == 0 for v in ev.values()), 'detalhe': ev}
out['provider_calls_na_instalacao'] = 'nao ha chamada a provedor no codigo (b) nem nas evidencias (c); o campo provider_calls do INSTALLED_VERIFICATION.json (carregadores) é do D7/D9 da segunda mensagem'
out['PASS'] = all(c['PASS'] for c in out['checks'].values())
(HERE / 'r2_d9_out.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('D9(parcial)', 'PASS' if out['PASS'] else 'FAIL')
print(json.dumps({k: out[k] for k in ('checks', 'rastro_dos_meus_scripts')}, ensure_ascii=False, indent=1)[:3500])
print(json.dumps({n: {k: v[k] for k in ('imports_de_rede_ou_provedor', 'http_client_hosts', 'urls_no_codigo')} for n, v in code.items()}, ensure_ascii=False))
