# -*- coding: utf-8 -*-
"""ENSAIO da implantação e da reversão numa CÓPIA COMPLETA da instalação, com banco SINTÉTICO (conserto ACOM 12/10).

Monta ensaio_implantacao/raiz/ espelhando as três raízes de produção (arquivos originais congelados em
4_INTEGRACAO/originais + exemplos da memória), um banco v1 sintético com 3 contextos construído pelo código v1
CONGELADO (sha256 = store.py instalado) — que, como a v1 de produção, deixa um memory.sqlite3.bak_* por mutação —,
as 6 superfícies D5 copiadas de produção (só leitura) e um «D:» sintético. Depois:
  1. inventário (sha256 de todo arquivo) ANTES;
  2. implantar.py --dry-run  -> nada muda (inventário igual, só recibos);
  3. implantar.py            -> CONCLUIDA; conferências independentes (alvos == candidato, schema 2, verify deep,
                                blocos aplicados, backups movidos, CLI de sessões instalado funciona em processo novo);
  4. reverter.py --dry-run; reverter.py -> REVERTIDA; inventário DEPOIS == ANTES para todo arquivo original
                                (os extras só podem ser .bak_*/.removido_*/.v2_revertido_*/journal/snapshots/pre_v2/D:/recibos);
  5. ENSAIO_RECIBO.json com tudo medido.
Roda sob a guarda da auditoria (rodar_ensaio.py é chamado com PYTHONPATH=guard e ACOM_AUDIT_ROOT=4_INTEGRACAO).
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent            # ensaio_implantacao
INT = HERE.parent                                   # 4_INTEGRACAO
RAIZ = HERE / 'raiz'
ORIG = INT / 'originais' / 'C'
CAND = INT / 'candidato' / 'C'
PY = sys.executable
SCOPE = {'house': 'IALD', 'principal': 'operator'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
AGENT = {'id': 'ensaio', 'kind': 'agent'}
TEXT = ('heartbeat sample response text ' * 40)[:1200]
SUPERFICIES = {
    'CLAUDE_global.md': r'C:\Users\rotol\.claude\CLAUDE.md',
    'AGENTS.md': r'C:\Users\rotol\.codex\AGENTS.md',
    'CLAUDE_nativa.md': r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md',
    'README.md': r'C:\IALD\PROGRAMA_IALD\README.md',
    'COORDINATOR.md': r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\COORDINATOR.md',
}
MEMORY_MD = r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'
EXTRAS_PERMITIDOS = ('.bak_', '.removido_', '.v2_revertido_', '.pre_v2_', '.sha256')
PASTAS_EXTRAS = ('journal', 'snapshots', '__pycache__', 'recibos', 'D')

sys.path.insert(0, str(INT / 'testes' / 'nucleo' / 'tests'))
import store_v1_frozen  # noqa: E402


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def copy_bytes(src, dst):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = Path(src).read_bytes()
    tmp = dst.with_name(dst.name + '.tmp_ens')
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    os.replace(tmp, dst)
    return hashlib.sha256(data).hexdigest()


def inventario(root):
    out = {}
    for p in sorted(Path(root).rglob('*')):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = sha256_file(p)
    return out


def run(args, timeout=1800, env_extra=None):
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    if env_extra:
        env.update(env_extra)
    t0 = time.time()
    proc = subprocess.run([PY, '-X', 'utf8'] + [str(a) for a in args], capture_output=True, timeout=timeout, env=env)
    return {'rc': proc.returncode, 'seconds': round(time.time() - t0, 2), 'stdout': proc.stdout.decode('utf-8', 'replace'),
            'stderr': proc.stderr.decode('utf-8', 'replace')[-3000:]}


def montar_raiz(sizes=(60, 20, 0)):
    if RAIZ.exists():
        shutil.rmtree(RAIZ)
    mem = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
    app = RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'
    fila = RAIZ / 'C' / 'IALD' / 'Central de Patentes' / 'Chatgpt' / 'IALD_ORQUESTRACAO_20260923' / 'iald_orchestrator'
    copias = []
    for rel in ('README.md', 'CORE.md', 'SESSION_BRIDGE.md', 'SESSION_MEMORY.md', 'session_hook.py', 'session_memory.py',
                'lib/iald_memory/__init__.py', 'lib/iald_memory/store.py'):
        copias.append((rel, copy_bytes(ORIG / 'IALD/MEMORIA_IALD' / rel, mem / rel)))
    for ex in sorted((Path(r'C:\IALD\MEMORIA_IALD\examples')).glob('*.json')):   # só leitura
        copias.append(('examples/' + ex.name, copy_bytes(ex, mem / 'examples' / ex.name)))
    for rel in ('iald_web_server.py', 'iald_app_memory.py'):
        copias.append((rel, copy_bytes(ORIG / 'IALD/projetos_pyhton/IALD' / rel, app / rel)))
    for rel in ('policy.py', 'operational_memory.py', 'nos_packet.py'):
        copias.append((rel, copy_bytes(ORIG / 'IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator' / rel, fila / rel)))
    sup = RAIZ / 'superficies'
    for name, prod in SUPERFICIES.items():
        copias.append(('superficies/' + name, copy_bytes(prod, sup / name)))
    copias.append(('superficies/MEMORY.md', copy_bytes(MEMORY_MD, sup / 'MEMORY.md')))
    (RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD').mkdir(parents=True)
    (RAIZ / 'recibos').mkdir()
    # banco v1 sintético com 3 contextos (código v1 congelado); um .bak_ por mutação, como na produção v1
    state = mem / 'state'
    (state / 'app_outbox').mkdir(parents=True)
    store = store_v1_frozen.MemoryStore(state)
    ids, heads = [], {}
    for k, n in enumerate(sizes):
        cid = ('ctx_%d' % k) if k != 1 else 'app_service_ensaio:1'
        store.ensure_context(cid, objective='Objetivo original do ensaio %d\r\n' % k, scope=SCOPE, actor=OPERATOR,
                             constraints={'no_remote_calls': True, 'ensaio': True})
        for i in range(1, n + 1):
            changes = {'candidates': [{'id': 'c%d_%03d' % (k, i), 'text': TEXT, 'statute': 'DECLARADO',
                                       'source': {'kind': 'executor', 'ref': 'job:%d' % i}}],
                       'flow': {'phase': 'f%03d' % i, 'next_action': 'seguir'}}
            store.transition(cid, SCOPE, expected_revision=i - 1, event_id='e%d_%03d' % (k, i), actor=AGENT, changes=changes)
        ids.append(cid)
        heads[cid] = store.get(cid, SCOPE)['receipt']
    baks = sorted(p.name for p in state.iterdir() if p.name.startswith('memory.sqlite3.bak_'))
    return {'copias': copias, 'contexts': ids, 'heads_v1': heads, 'db_bytes': (state / 'memory.sqlite3').stat().st_size,
            'db_sha256': sha256_file(state / 'memory.sqlite3'), 'backups_legados': len(baks),
            'backups_legados_bytes': sum((state / b).stat().st_size for b in baks)}


def config():
    mem = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
    cfg = {
        '_comentario': 'ENSAIO: raízes apontam para a cópia em ensaio_implantacao/raiz; nenhum processo gerido.',
        'candidato_root': str(CAND), 'manifesto_candidato': str(INT / 'CANDIDATO_MANIFESTO.json'),
        'raizes': {r'C:\IALD\MEMORIA_IALD': str(mem),
                   r'C:\IALD\projetos_pyhton\IALD': str(RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'),
                   r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator':
                       str(RAIZ / 'C' / 'IALD' / 'Central de Patentes' / 'Chatgpt' / 'IALD_ORQUESTRACAO_20260923' / 'iald_orchestrator')},
        'app_root_processos': str(RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'),
        'gerir_processos': False, 'exigir_app_parado': False,
        'arquivo_D': str(RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD'), 'keep_backups': 3,
        'recibos_dir': str(RAIZ / 'recibos'),
        'superficies': [str(RAIZ / 'superficies' / n) for n in SUPERFICIES],
        'memory_md': str(RAIZ / 'superficies' / 'MEMORY.md'),
        'ordem_operador': r'C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt',
        'bridge_v2': str(INT / 'ferramentas' / 'SESSION_BRIDGE_v2.md'), 'aplicar_blocos': str(INT / 'ferramentas' / 'aplicar_blocos.py'),
    }
    path = HERE / 'ensaio_config.json'
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return path, cfg


def conferir_pos_implantacao(cfg, montagem, recibo):
    out = {}
    manifesto = json.loads(Path(cfg['manifesto_candidato']).read_text(encoding='utf-8'))
    iguais = []
    for item in manifesto['arquivos']:
        prod = Path(item['target'])
        alvo = None
        for root, real in cfg['raizes'].items():
            if str(prod).lower().startswith(root.lower()):
                alvo = Path(real) / str(prod)[len(root):].lstrip('\\')
        iguais.append(sha256_file(alvo) == item['sha256'])
    out['alvos_iguais_ao_candidato'] = all(iguais)
    out['n_alvos'] = len(iguais)
    mem = Path(cfg['raizes'][r'C:\IALD\MEMORIA_IALD'])
    state = mem / 'state'
    conn = sqlite3.connect('file:%s?mode=ro' % (state / 'memory.sqlite3').as_posix(), uri=True)
    try:
        out['schema_version'] = conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]
        out['snapshots_rows'] = conn.execute('SELECT count(*) FROM snapshots').fetchone()[0]
        out['context_state_rows'] = conn.execute('SELECT count(*) FROM context_state').fetchone()[0]
    finally:
        conn.close()
    out['journal_files'] = sorted(p.name for p in (state / 'journal').glob('*'))
    out['baks_restantes'] = sorted(p.name for p in state.iterdir() if p.name.startswith('memory.sqlite3.bak_'))
    out['pre_v2_locais'] = sorted(p.name for p in state.iterdir() if '.pre_v2_' in p.name)
    dest = Path(cfg['arquivo_D']) / 'backups_ate_20261012'
    out['D_backups_movidos'] = len([p for p in dest.glob('memory.sqlite3.bak_*')]) if dest.exists() else 0
    out['D_pre_v2'] = sorted(p.name for p in (Path(cfg['arquivo_D']) / 'pre_v2').glob('*')) if (Path(cfg['arquivo_D']) / 'pre_v2').exists() else []
    # blocos aplicados
    out['superficies'] = {}
    for p in cfg['superficies']:
        b = Path(p).read_bytes()
        out['superficies'][Path(p).name] = {'bloco_novo_no_topo': b.startswith(b'<!-- IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->'),
                                            'linha_substituicao': b'substitu\xc3\xaddo em 12/10/2026 por ordem do operador' in b,
                                            'bloco_antigo_ausente': b'IALD_COMMON_ACOM_SESSION_ENTRY_20261010' not in b}
    mb = Path(cfg['memory_md']).read_bytes()
    out['memory_md'] = {'linhas': mb.count(b'\n'), 'bytes': len(mb), 'linha_nova': b'- Mem\xc3\xb3ria ACOM: `C:\\IALD\\MEMORIA_IALD\\README.md` + `SESSION_BRIDGE.md` (12/10' in mb}
    # o CLI de sessões INSTALADO funciona em processo novo contra o banco migrado (get + transition + verify)
    cli = mem / 'session_memory.py'
    cid = montagem['contexts'][0]
    def call(req):
        r = subprocess.run([PY, '-X', 'utf8', str(cli), '--core-root', str(mem / 'lib'), '--store', str(state)],
                           input=json.dumps(req).encode('utf-8'), capture_output=True, timeout=120,
                           env=dict(os.environ, PYTHONUTF8='1', IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR=str(Path(cfg['arquivo_D']) / 'snapshots')))
        return r.returncode, json.loads(r.stdout.decode('utf-8') or '{}'), r.stderr.decode('utf-8', 'replace')[-500:]
    rc, got, err = call({'operation': 'get', 'context_id': cid, 'scope': SCOPE})
    out['cli_get'] = {'rc': rc, 'revision': got.get('result', {}).get('revision'), 'erro': err if rc else None}
    rev = got.get('result', {}).get('revision')
    rc2, tr, err2 = call({'operation': 'transition', 'context_id': cid, 'scope': SCOPE, 'expected_revision': rev,
                          'event_id': 'ensaio_pos_migracao', 'actor': AGENT, 'changes': {'flow': {'phase': 'pos_migracao', 'next_action': 'verificar'}}})
    out['cli_transition'] = {'rc': rc2, 'revision': tr.get('result', {}).get('revision'), 'erro': err2 if rc2 else None}
    rc3, ver, err3 = call({'operation': 'verify', 'context_id': cid, 'scope': SCOPE})
    out['cli_verify'] = {'rc': rc3, 'ok': ver.get('result', {}).get('ok'), 'event_count': ver.get('result', {}).get('event_count'),
                         'journal_ok': ver.get('result', {}).get('journal_ok'), 'erro': err3 if rc3 else None}
    out['heads_migracao_iguais_v1'] = all(
        recibo['passos']['migracao']['apply']['contexts'][c]['head_revision'] == montagem['heads_v1'][c]['revision'] for c in montagem['contexts'])
    out['ok'] = (out['alvos_iguais_ao_candidato'] and out['schema_version'] == '2' and len(out['baks_restantes']) == 3
                 and out['D_backups_movidos'] == montagem['backups_legados'] - 3 and all(all(v.values()) for v in out['superficies'].values())
                 and out['memory_md']['linha_nova'] and out['memory_md']['linhas'] <= 200 and out['memory_md']['bytes'] <= 24000
                 and rc == 0 and rc2 == 0 and rc3 == 0 and out['cli_verify']['ok'] is True and out['heads_migracao_iguais_v1'])
    return out


def comparar_inventarios(antes, depois):
    faltam = [k for k in antes if k not in depois]
    diferentes = [k for k in antes if k in depois and antes[k] != depois[k]]
    extras = [k for k in depois if k not in antes]
    extras_nao_permitidos = [k for k in extras if not (any(s in k for s in EXTRAS_PERMITIDOS) or k.split('/')[0] in PASTAS_EXTRAS
                                                       or any('/' + d + '/' in '/' + k for d in PASTAS_EXTRAS))]
    # backups legados movidos para o «D:» (decisão D2): contam como preservados se a cópia em D: tem o MESMO sha256
    movidos_integros, faltam_de_verdade = [], []
    for k in faltam:
        name = k.rsplit('/', 1)[-1]
        d_key = 'D/IALD_ARQUIVO/MEMORIA_IALD/backups_ate_20261012/' + name
        if name.startswith('memory.sqlite3.bak_') and depois.get(d_key) == antes[k]:
            movidos_integros.append(name)
        else:
            faltam_de_verdade.append(k)
    return {'faltam': faltam_de_verdade, 'backups_legados_movidos_para_D_integros': len(movidos_integros), 'diferentes': diferentes,
            'n_extras': len(extras), 'extras_nao_permitidos': extras_nao_permitidos,
            'identico_nos_originais': not faltam_de_verdade and not diferentes and not extras_nao_permitidos,
            'identico_sem_contar_movidos': not faltam and not diferentes and not extras_nao_permitidos}


def main():
    t_start = time.time()
    recibo = {'titulo': 'ENSAIO DE IMPLANTAÇÃO E REVERSÃO — conserto ACOM 12/10', 'at': time.strftime('%Y-%m-%dT%H:%M:%S'),
              'guarda': {'ACOM_AUDIT_ROOT': os.environ.get('ACOM_AUDIT_ROOT'), 'PYTHONPATH': os.environ.get('PYTHONPATH')}}
    recibo['montagem'] = montar_raiz()
    cfg_path, cfg = config()
    recibo['config'] = str(cfg_path)
    antes = inventario(RAIZ)
    recibo['inventario_antes_n'] = len(antes)
    # 2. dry-run
    r = run([INT / 'implantar.py', '--config', cfg_path, '--dry-run'])
    recibo['implantar_dry_run'] = {'rc': r['rc'], 'seconds': r['seconds'], 'stdout': r['stdout'][-1500:], 'stderr': r['stderr'][-800:]}
    dry_rec = json.loads((RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO_dry_run.json').read_text(encoding='utf-8'))
    recibo['implantar_dry_run']['status'] = dry_rec['status']
    depois_dry = inventario(RAIZ)
    cmp_dry = comparar_inventarios({k: v for k, v in antes.items() if not k.startswith('recibos/')},
                                   {k: v for k, v in depois_dry.items() if not k.startswith('recibos/')})
    recibo['implantar_dry_run']['nada_mudou'] = cmp_dry['identico_nos_originais'] and cmp_dry['n_extras'] == 0
    recibo['implantar_dry_run']['comparacao'] = cmp_dry
    # 3. implantar
    r = run([INT / 'implantar.py', '--config', cfg_path])
    recibo['implantar'] = {'rc': r['rc'], 'seconds': r['seconds'], 'stdout': r['stdout'][-1500:], 'stderr': r['stderr'][-1500:]}
    rec_impl = json.loads((RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json').read_text(encoding='utf-8'))
    recibo['implantar']['status'] = rec_impl['status']
    recibo['implantar']['passos'] = {k: {'status': v['status'], 'segundos': v.get('segundos')} for k, v in rec_impl['passos'].items()}
    if rec_impl['status'] == 'CONCLUIDA':
        recibo['conferencia_pos_implantacao'] = conferir_pos_implantacao(cfg, recibo['montagem'], rec_impl)
    # 4. reverter
    r = run([INT / 'reverter.py', '--recibo', RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json', '--dry-run'])
    recibo['reverter_dry_run'] = {'rc': r['rc'], 'seconds': r['seconds'], 'stdout': r['stdout'][-800:]}
    r = run([INT / 'reverter.py', '--recibo', RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json'])
    recibo['reverter'] = {'rc': r['rc'], 'seconds': r['seconds'], 'stdout': r['stdout'][-1500:], 'stderr': r['stderr'][-1500:]}
    rec_rev = json.loads((RAIZ / 'recibos' / 'RECIBO_REVERSAO.json').read_text(encoding='utf-8'))
    recibo['reverter']['status'] = rec_rev['status']
    recibo['reverter']['passos'] = {k: {'status': v['status'], 'segundos': v.get('segundos')} for k, v in rec_rev['passos'].items()}
    depois = inventario(RAIZ)
    recibo['inventario_depois_n'] = len(depois)
    recibo['comparacao_antes_depois'] = comparar_inventarios({k: v for k, v in antes.items() if not k.startswith('recibos/')},
                                                            {k: v for k, v in depois.items() if not k.startswith('recibos/')})
    state = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state'
    recibo['banco_apos_reversao'] = {'sha256': sha256_file(state / 'memory.sqlite3'),
                                     'igual_ao_original': sha256_file(state / 'memory.sqlite3') == recibo['montagem']['db_sha256']}
    # 5. --mover-backups-de-volta num segundo ensaio curto? Não: os backups legados ficam em D: por decisão (D2); registramos.
    recibo['backups_legados_apos_reversao'] = {'em_state': len([p for p in state.glob('memory.sqlite3.bak_*')]),
                                               'em_D': len(list((RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD' / 'backups_ate_20261012').glob('memory.sqlite3.bak_*')))}
    recibo['ok'] = (recibo['implantar_dry_run']['status'] == 'DRY_RUN_OK' and recibo['implantar_dry_run']['nada_mudou']
                    and rec_impl['status'] == 'CONCLUIDA' and recibo.get('conferencia_pos_implantacao', {}).get('ok') is True
                    and rec_rev['status'] == 'REVERTIDA' and recibo['comparacao_antes_depois']['identico_nos_originais']
                    and recibo['banco_apos_reversao']['igual_ao_original'])
    # Variante B: ciclo completo de novo, reversão com --mover-backups-de-volta -> identidade TOTAL (inclusive os .bak_ legados)
    recibo['variante_B'] = {}
    montagem_b = montar_raiz()
    cfg_path, cfg = config()
    antes_b = {k: v for k, v in inventario(RAIZ).items() if not k.startswith('recibos/')}
    rb = run([INT / 'implantar.py', '--config', cfg_path])
    rec_impl_b = json.loads((RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json').read_text(encoding='utf-8'))
    rb2 = run([INT / 'reverter.py', '--recibo', RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json', '--mover-backups-de-volta'])
    rec_rev_b = json.loads((RAIZ / 'recibos' / 'RECIBO_REVERSAO.json').read_text(encoding='utf-8'))
    depois_b = {k: v for k, v in inventario(RAIZ).items() if not k.startswith('recibos/')}
    cmp_b = comparar_inventarios(antes_b, depois_b)
    recibo['variante_B'] = {'implantar': rec_impl_b['status'], 'reverter': rec_rev_b['status'], 'rc': (rb['rc'], rb2['rc']),
                            'backups_devolvidos': rec_rev_b['passos']['backups_legados'].get('devolvidos'),
                            'comparacao': cmp_b, 'identico_total': cmp_b['identico_sem_contar_movidos'],
                            'db_igual': sha256_file(state / 'memory.sqlite3') == montagem_b['db_sha256']}
    recibo['ok'] = recibo['ok'] and recibo['variante_B']['identico_total'] and recibo['variante_B']['db_igual']         and rec_impl_b['status'] == 'CONCLUIDA' and rec_rev_b['status'] == 'REVERTIDA'
    recibo['seconds_total'] = round(time.time() - t_start, 1)
    (HERE / 'ENSAIO_RECIBO.json').write_text(json.dumps(recibo, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    print(json.dumps({'ok': recibo['ok'], 'implantar': rec_impl['status'], 'reverter': rec_rev['status'],
                      'conferencia': recibo.get('conferencia_pos_implantacao', {}).get('ok'),
                      'identico_apos_reversao': recibo['comparacao_antes_depois']['identico_nos_originais'],
                      'variante_B_identico_total': recibo['variante_B']['identico_total'],
                      'seconds': recibo['seconds_total']}, ensure_ascii=False))
    return 0 if recibo['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
