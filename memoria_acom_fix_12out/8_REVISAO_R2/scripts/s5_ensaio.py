# -*- coding: utf-8 -*-
"""Revisor R2, item 2: ensaio ADVERSARIAL de implantacao+reversao numa COPIA SINTETICA (nunca producao).

Ferramentas = implantar.py / reverter.py / implantacao_lib.py / aplicar_blocos.py do R2 copiados BYTE A BYTE (sha conferido).
Candidato = candidato_r2 com a chave embutida do iald_web_server.py redigida (mesmo tamanho; o manifesto copiado recebe o
sha recalculado so dessa linha). Banco v1 sintetico (store_v1_frozen), superficies = copias da integracao, D: sintetico,
processos pelo backend SIMULADO do proprio R2 (agendador/supervisor/web reais em Python). Guarda da auditoria ligada
(ACOM_AUDIT_ROOT = 8_REVISAO_R2) + gancho de LENTIDAO opcional em os.rename (para matar no meio).

Cenarios novos (os do integrador A..F nao sao repetidos aqui):
  K1a mata o implantar (TerminateProcess) no passo 4 com o 1o arquivo em 'backup_ok' (tempario a meio da troca)
  K1b mata no passo 4 com o 8o arquivo em 'backup_ok'
  K1c mata durante o passo 5 (aplicar_blocos.py filho continua orfao)
  K1d mata durante a migracao --apply (filho migrar_para_delta.py continua orfao) e roda o reverter em seguida
  K2  falha no passo 4 (alvo preso) e o operador RODA O IMPLANTAR DE NOVO em vez do reverter; depois reverter
  K3  falha no passo 1 depois do Disable (o stop script nao derruba o app): a tarefa fica desabilitada?
  K4  reverter com um alvo preso (troca falha no meio): o reverter religa o app num estado misto?
  K5  mata o reverter no meio do passo 2 e roda o reverter de novo (idempotencia)
"""
import hashlib
import json
import os
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
WORK = REV.parent
INT = WORK / '4_INTEGRACAO'
ENS = REV / 'ensaio'
TOOLS = ENS / 'tools'
TOOLS_K3 = ENS / 'tools_k3'
SIMS = ENS / 'sim'
SIM_RUNS = ENS / 'sim_run'
CAND = ENS / 'cand' / 'C'
ORIG = ENS / 'orig' / 'C'
MAN = ENS / 'CANDIDATO_MANIFESTO_R2_redigido.json'
RAIZ = ENS / 'raiz'
GUARD_SLOW = ENS / 'guardslow'
PY = sys.executable
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,})')
SCOPE = {'house': 'IALD', 'principal': 'operator'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
AGENT = {'id': 'ensaio-r2', 'kind': 'agent'}
TEXT = ('heartbeat sample response text ' * 40)[:1200]
SUPERF = {'CLAUDE_global.md': 'CLAUDE_global.md', 'AGENTS.md': 'AGENTS.md', 'CLAUDE_nativa.md': 'CLAUDE_nativa.md',
          'README.md': 'README.md', 'COORDINATOR.md': 'COORDINATOR.md'}
R2_SHA16 = {'implantar.py': 'f2c9b3facc91500f', 'reverter.py': '7c12615545382ac7', 'implantacao_lib.py': '928118ee223976c3'}
sys.path.insert(0, str(REV / 'copia' / 'testes_r2' / 'nucleo' / 'tests'))
import store_v1_frozen  # noqa: E402


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def redact(b):
    return KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), b)


def cpb(src, dst, red=False):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    b = Path(src).read_bytes()
    dst.write_bytes(redact(b) if red else b)


# ---------------------------------------------------------------------------------------------- preparo
def preparar():
    if ENS.exists():
        shutil.rmtree(ENS)
    log = {}
    for n in ('implantar.py', 'reverter.py', 'implantacao_lib.py'):
        cpb(INT / n, TOOLS / n)
        log[n] = sha(TOOLS / n)[:16]
        assert log[n] == R2_SHA16[n], ('ferramenta divergente do R2', n)
    cpb(INT / 'ferramentas' / 'aplicar_blocos.py', TOOLS / 'ferramentas' / 'aplicar_blocos.py')
    cpb(INT / 'ferramentas' / 'SESSION_BRIDGE_v2.md', TOOLS / 'ferramentas' / 'SESSION_BRIDGE_v2.md')
    log['aplicar_blocos.py'] = sha(TOOLS / 'ferramentas' / 'aplicar_blocos.py')[:16]
    # variante K3: o MESMO codigo + um remendo no SIMULADOR (o stop script nao derruba o app)
    for n in ('implantar.py', 'reverter.py'):
        cpb(INT / n, TOOLS_K3 / n)
    k3 = (INT / 'implantacao_lib.py').read_bytes() + (
        b'\n\n# --- K3 (revisor R2): ambiente em que o stop script nao derruba o app (so o simulador muda)\n'
        b'def _parar_script_sem_efeito(self):\n    return {"rc": 1, "nota": "K3: stop script sem efeito (simulado)"}\n'
        b'ProcessosSim.parar_script = _parar_script_sem_efeito\n')
    (TOOLS_K3 / 'implantacao_lib.py').write_bytes(k3)
    for f in (INT / 'ensaio_implantacao_r2' / 'sim').glob('*.py'):
        cpb(f, SIMS / f.name)
    for root, _, files in os.walk(INT / 'candidato_r2' / 'C'):
        for f in files:
            s = Path(root) / f
            cpb(s, CAND / s.relative_to(INT / 'candidato_r2' / 'C'), red=f == 'iald_web_server.py')
    for root, _, files in os.walk(INT / 'originais' / 'C'):
        for f in files:
            s = Path(root) / f
            cpb(s, ORIG / s.relative_to(INT / 'originais' / 'C'), red=f == 'iald_web_server.py')
    man = json.loads((INT / 'CANDIDATO_MANIFESTO_R2.json').read_text(encoding='utf-8'))
    for a in man['arquivos']:
        if a['target'].endswith('iald_web_server.py'):
            a['sha256'] = sha(CAND / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py')
    for o in man['originais']:
        if o['source'].endswith('iald_web_server.py'):
            o['sha256'] = sha(ORIG / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py')
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
    # sitecustomize: a guarda da auditoria (exec do arquivo da copia) + lentidao opcional em os.rename
    GUARD_SLOW.mkdir(parents=True, exist_ok=True)
    g = (REV / 'copia' / 'guard' / 'sitecustomize.py').as_posix()
    (GUARD_SLOW / 'sitecustomize.py').write_text(
        'import os, sys, time\n'
        'exec(compile(open(%r, encoding="utf-8").read(), %r, "exec"))\n'
        '_SLOW = float(os.environ.get("SLOW_RENAME_S", "0") or 0)\n'
        '_MARK = os.environ.get("SLOW_RENAME_MARK", "")\n'
        '_SRC = os.environ.get("SLOW_RENAME_SRC", ".tmp_")\n'
        'def _slowhook(ev, args):\n'
        '    if ev == "os.rename" and _SLOW and _MARK:\n'
        '        try:\n'
        '            s, d = os.fsdecode(args[0]), os.fsdecode(args[1])\n'
        '        except Exception:\n'
        '            return\n'
        '        if _MARK.lower() in d.lower() and _SRC in s:\n'
        '            time.sleep(_SLOW)\n'
        'sys.addaudithook(_slowhook)\n' % (g, g), encoding='utf-8')
    return log


def montar_raiz(sizes=(12, 6, 0)):
    if RAIZ.exists():
        shutil.rmtree(RAIZ)
    mem = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
    app = RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'
    fila = RAIZ / 'C' / 'IALD' / 'Central de Patentes' / 'Chatgpt' / 'IALD_ORQUESTRACAO_20260923' / 'iald_orchestrator'
    for rel in ('README.md', 'CORE.md', 'SESSION_BRIDGE.md', 'SESSION_MEMORY.md', 'session_hook.py', 'session_memory.py',
                'lib/iald_memory/__init__.py', 'lib/iald_memory/store.py'):
        cpb(ORIG / 'IALD' / 'MEMORIA_IALD' / rel, mem / rel)
    for rel in ('iald_web_server.py', 'iald_app_memory.py'):
        cpb(ORIG / 'IALD' / 'projetos_pyhton' / 'IALD' / rel, app / rel)
    for rel in ('policy.py', 'operational_memory.py', 'nos_packet.py'):
        cpb(ORIG / 'IALD' / 'Central de Patentes' / 'Chatgpt' / 'IALD_ORQUESTRACAO_20260923' / 'iald_orchestrator' / rel, fila / rel)
    for name, src in SUPERF.items():
        cpb(INT / 'testes_r2' / 'blocos' / 'copias' / src, RAIZ / 'superficies' / name)
    cpb(INT / 'testes_r2' / 'blocos' / 'copias' / 'MEMORY.md', RAIZ / 'superficies' / 'MEMORY.md')
    (RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD').mkdir(parents=True)
    (RAIZ / 'recibos').mkdir()
    state = mem / 'state'
    (state / 'app_outbox').mkdir(parents=True)
    st = store_v1_frozen.MemoryStore(state)
    ids = []
    for k, n in enumerate(sizes):
        cid = 'ctx_%d' % k
        st.ensure_context(cid, objective='Objetivo do ensaio R2 %d\r\n' % k, scope=SCOPE, actor=OPERATOR,
                          constraints={'no_remote_calls': True})
        for i in range(1, n + 1):
            ch = {'candidates': [{'id': 'c%d_%04d' % (k, i), 'text': TEXT, 'statute': 'DECLARADO',
                                  'source': {'kind': 'executor', 'ref': 'job:%d' % i}}],
                  'flow': {'phase': 'f%04d' % i, 'next_action': 'seguir'}}
            st.transition(cid, SCOPE, expected_revision=i - 1, event_id='e%d_%04d' % (k, i), actor=AGENT, changes=ch)
        ids.append(cid)
    return {'contexts': ids, 'db_sha256': sha(state / 'memory.sqlite3'), 'db_bytes': (state / 'memory.sqlite3').stat().st_size,
            'baks': len([p for p in state.iterdir() if p.name.startswith('memory.sqlite3.bak_')])}


def inventario():
    out = {}
    for p in sorted(RAIZ.rglob('*')):
        if p.is_file():
            rel = p.relative_to(RAIZ).as_posix()
            if not rel.startswith('recibos/'):
                out[rel] = sha(p)
    return out


EXTRA_OK = ('.bak_', '.removido_', '.v2_revertido_', '.pre_v2_', '.sha256')
DIR_OK = ('/journal/', '/snapshots/', '/__pycache__', 'D/')


def comparar(antes, depois):
    falt = [k for k in antes if k not in depois]
    dif = [k for k in antes if k in depois and antes[k] != depois[k]]
    extras = [k for k in depois if k not in antes]
    extras_estranhos = [k for k in extras if not any(x in k for x in EXTRA_OK) and not any(d in '/' + k for d in DIR_OK)]
    return {'identico_nos_originais': not falt and not dif, 'faltando': falt[:10], 'diferentes': dif[:10],
            'n_extras': len(extras), 'extras_estranhos': extras_estranhos[:20]}


def config(sim_dir, nome, tools=TOOLS, **extra):
    mem = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
    cfg = {'candidato_root': str(CAND), 'manifesto_candidato': str(MAN),
           'raizes': {r'C:\IALD\MEMORIA_IALD': str(mem),
                      r'C:\IALD\projetos_pyhton\IALD': str(RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'),
                      r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator':
                          str(RAIZ / 'C' / 'IALD' / 'Central de Patentes' / 'Chatgpt' / 'IALD_ORQUESTRACAO_20260923' / 'iald_orchestrator')},
           'app_root_processos': str(RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'),
           'gerir_processos': True, 'processos_backend': 'simulado', 'sim_dir': str(sim_dir),
           'tarefa_agendada': 'IALD Web Server (simulada)', 'silencio_s': 2.0, 'esperar_parada_s': 15, 'esperar_inicio_s': 40,
           'arquivo_D': str(RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD'), 'keep_backups': 3, 'recibos_dir': str(RAIZ / 'recibos'),
           'superficies': [str(RAIZ / 'superficies' / n) for n in SUPERF], 'memory_md': str(RAIZ / 'superficies' / 'MEMORY.md'),
           'ordem_operador': r'C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt',
           'bridge_v2': str(TOOLS / 'ferramentas' / 'SESSION_BRIDGE_v2.md'), 'aplicar_blocos': str(TOOLS / 'ferramentas' / 'aplicar_blocos.py')}
    cfg.update(extra)
    p = ENS / ('config_%s.json' % nome)
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding='utf-8')
    return p, cfg


def env(slow=None):
    e = dict(os.environ)
    e.update(PYTHONPATH=str(GUARD_SLOW), ACOM_AUDIT_ROOT=str(REV), PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
             PYTHONDONTWRITEBYTECODE='1', IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR=str(RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD' / 'snapshots'))
    for k in ('SLOW_RENAME_S', 'SLOW_RENAME_MARK', 'SLOW_RENAME_SRC'):
        e.pop(k, None)
    if slow:
        e.update(slow)
    return e


def run(args, slow=None, timeout=900):
    p = subprocess.run([PY, '-B', '-X', 'utf8'] + [str(a) for a in args], capture_output=True, timeout=timeout, env=env(slow))
    return {'rc': p.returncode, 'stdout': p.stdout.decode('utf-8', 'replace')[-1500:], 'stderr': p.stderr.decode('utf-8', 'replace')[-1500:]}


def ler(p):
    for _ in range(50):
        try:
            return json.loads(Path(p).read_text(encoding='utf-8'))
        except (OSError, ValueError):
            time.sleep(0.05)
    return None


def _pid_vivo(pid):
    import ctypes
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    try:
        c = ctypes.c_ulong()
        return bool(k.GetExitCodeProcess(h, ctypes.byref(c))) and c.value == 259
    finally:
        k.CloseHandle(h)


class Sim:
    def __init__(self, nome, tools=TOOLS):
        sys.path.insert(0, str(tools))
        from implantacao_lib import ProcessosSim
        sys.path.pop(0)
        self.dir = SIM_RUNS / nome
        if self.dir.exists():
            shutil.rmtree(self.dir)
        (self.dir / 'pids').mkdir(parents=True)
        (self.dir / 'comandos').mkdir()
        (self.dir / 'tarefa.json').write_text(json.dumps({'nome': 'IALD Web Server (simulada)', 'enabled': True, 'restart_count': 3,
                                                          'restart_interval_s': 1.5, 'scripts': str(SIMS),
                                                          'mem_root': str(RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD')}), encoding='utf-8')
        (self.dir / 'estado_agendador.json').write_text('{}', encoding='utf-8')
        self.ag = subprocess.Popen([PY, '-X', 'utf8', str(SIMS / 'sim_agendador.py'), str(self.dir)], env=env(),
                                   stdout=open(self.dir / 'saida_agendador.log', 'ab'), stderr=subprocess.STDOUT)
        self.b = ProcessosSim(self.dir)
        time.sleep(0.5)

    def subir(self):
        self.b.tarefa_iniciar()
        t0 = time.time()
        while time.time() - t0 < 30:
            p = self.b.listar()
            if self.b.saude()[0] and len(p['web']) == 1 and len(p['supervisores']) == 1:
                return
            time.sleep(0.3)
        raise RuntimeError('sim nao subiu')

    def estado(self):
        p = self.b.listar()
        return {'tarefa_habilitada': self.b.tarefa_ler().get('habilitada'), 'sup': len(p['supervisores']),
                'web': [w.get('store_sha16') for w in p['web']]}

    def encerrar(self):
        try:
            self.b._comando('exit', esperar_s=5)
        except Exception:  # noqa: BLE001
            pass
        if self.ag.poll() is None:
            self.ag.terminate()
        for f in (self.dir / 'pids').glob('*.json'):
            try:
                pid = json.loads(f.read_text(encoding='utf-8'))['pid']
                if _pid_vivo(pid):
                    os.kill(pid, signal.SIGTERM)
            except (OSError, ValueError, KeyError):
                pass
        time.sleep(0.5)


class Prende:
    def __init__(self, path):
        self.flag = ENS / ('solta_%d_%d' % (os.getpid(), int(time.time() * 1000)))
        self.ready = Path(str(self.flag) + '_pronto')
        code = ('import sys,time,os\nf=open(sys.argv[1],"rb")\nopen(sys.argv[3],"w").close()\n'
                'while not os.path.exists(sys.argv[2]): time.sleep(0.1)\nf.close()\n')
        self.p = subprocess.Popen([PY, '-c', code, str(path), str(self.flag), str(self.ready)], env=env())
        t0 = time.time()
        while not self.ready.exists() and time.time() - t0 < 10:
            time.sleep(0.05)

    def soltar(self):
        self.flag.write_text('x')
        self.p.wait(10)


def lib_le(mont):
    mem = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
    p = subprocess.run([PY, '-B', '-X', 'utf8', '-c',
                        'import sys; sys.path.insert(0, sys.argv[1]); from iald_memory import MemoryStore; '
                        'print(MemoryStore(sys.argv[2]).get(sys.argv[3], {"house":"IALD","principal":"operator"})["revision"])',
                        str(mem / 'lib'), str(mem / 'state'), mont['contexts'][0]], capture_output=True, env=env())
    return {'rc': p.returncode, 'err': p.stderr.decode('utf-8', 'replace')[-240:] if p.returncode else None}


def alvos_estado():
    man = json.loads(MAN.read_text(encoding='utf-8'))
    orig = {o['source'].lower(): o['sha256'] for o in man['originais']}
    _, cfg = None, json.loads((ENS / 'config_base.json').read_text(encoding='utf-8')) if (ENS / 'config_base.json').exists() else None
    out = {}
    for a in man['arquivos']:
        t = a['target']
        for r, real in cfg['raizes'].items():
            if t.lower().startswith(r.lower()):
                p = Path(real) / t[len(r):].lstrip('\\')
        s = sha(p) if p.exists() else None
        out[t.rsplit('\\', 1)[-1]] = 'candidato' if s == a['sha256'] else 'original' if s == orig.get(t.lower()) else 'ausente' if s is None else 'outro'
    return out


def schema():
    db = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state' / 'memory.sqlite3'
    if not db.exists():
        return None
    c = sqlite3.connect('file:%s?mode=ro' % db.as_posix(), uri=True)
    try:
        return c.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]
    finally:
        c.close()


def implantar_e_matar(cfg_path, cond, slow=None, tools=TOOLS, extra_args=(), limite=240):
    rec_p = RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json'
    p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(tools / 'implantar.py'), '--config', str(cfg_path)] + list(extra_args),
                         env=env(slow), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t0 = time.time()
    morto = False
    while time.time() - t0 < limite:
        if p.poll() is not None:
            break
        rec = ler(rec_p) if rec_p.exists() else None
        if rec and cond(rec):
            p.kill()
            morto = True
            break
        time.sleep(0.02)
    p.wait(30)
    return {'morto': morto, 'rc': p.returncode, 'recibo': ler(rec_p)}


def reverter(slow=None, tools=TOOLS, args=()):
    r = run([tools / 'reverter.py', '--recibo', RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json'] + list(args), slow=slow)
    rr = ler(RAIZ / 'recibos' / 'RECIBO_REVERSAO.json')
    return {'rc': r['rc'], 'status': rr and rr['status'], 'falhas': rr and rr['falhas'],
            'passos': rr and {k: (v['status'], (v.get('mensagem') or v.get('nota') or '')[:160]) for k, v in rr['passos'].items()}}


def resumo_rec(rec):
    if not rec:
        return None
    sub = rec['passos'].get('substituir_arquivos', {})
    return {'status': rec['status'], 'mudancas_iniciadas': rec.get('mudancas_iniciadas'),
            'passos': {k: v['status'] for k, v in rec['passos'].items()},
            'fases': [a.get('fase') for a in sub.get('arquivos') or []], 'apos_falha': rec.get('apos_falha')}


# ---------------------------------------------------------------------------------------------- cenarios
def com_sim(nome, fn, sizes=(12, 6, 0), tools=TOOLS):
    mont = montar_raiz(sizes)
    sim = Sim(nome, tools)
    try:
        sim.subir()
        cfg_path, cfg = config(sim.dir, nome)
        (ENS / 'config_base.json').write_text(json.dumps(cfg, ensure_ascii=False), encoding='utf-8')
        antes = inventario()
        out = fn(sim, cfg_path, cfg, mont, antes)
        out['estado_sim_final'] = sim.estado()
        out['comparacao_final'] = comparar(antes, inventario())
        out['banco_igual_ao_original'] = sha(RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state' / 'memory.sqlite3') == mont['db_sha256'] \
            if (RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state' / 'memory.sqlite3').exists() else False
        out['lib_le_o_banco'] = lib_le(mont)
        out['schema_final'] = schema()
        return out
    finally:
        sim.encerrar()


SLOW_ALVO = None


def slow_alvos(s=1.0, src='.tmp_'):
    return {'SLOW_RENAME_S': str(s), 'SLOW_RENAME_MARK': str(RAIZ / 'C'), 'SLOW_RENAME_SRC': src}


def k1(nome, cond, slow, sizes=(12, 6, 0), espera_orfao=0):
    def fn(sim, cfg_path, cfg, mont, antes):
        r = implantar_e_matar(cfg_path, cond, slow=slow, extra_args=['--pular-mover-backups'])
        o = {'implantar': {'morto': r['morto'], 'rc': r['rc'], 'recibo': resumo_rec(r['recibo'])}}
        o['tmp_orfaos'] = sorted(p.name for p in RAIZ.rglob('*.tmp_2*'))
        o['alvos_apos_morte'] = alvos_estado()
        o['schema_apos_morte'] = schema()
        o['sim_apos_morte'] = sim.estado()
        if espera_orfao:
            time.sleep(espera_orfao)
        o['reverter'] = reverter()
        o['alvos_apos_reverter'] = alvos_estado()
        o['tmp_orfaos_apos_reverter'] = sorted(p.name for p in RAIZ.rglob('*.tmp_2*'))
        return o
    return com_sim(nome, fn, sizes)


def cen_K1a():
    return k1('K1a', lambda r: any(a.get('fase') == 'backup_ok' for a in (r['passos'].get('substituir_arquivos', {}).get('arquivos') or [])),
              slow_alvos(1.5))


def cen_K1b():
    def c(r):
        a = r['passos'].get('substituir_arquivos', {}).get('arquivos') or []
        return len(a) >= 8 and a[-1].get('fase') == 'backup_ok'
    return k1('K1b', c, slow_alvos(1.0))


def cen_K1c():
    return k1('K1c', lambda r: 'aplicar_blocos' in r['passos'], slow_alvos(0.6), espera_orfao=6)


def cen_K1d():
    return k1('K1d', lambda r: 'migracao' in (r.get('mudancas_iniciadas') or []), None, sizes=(150, 50, 0))


def cen_K2():
    def fn(sim, cfg_path, cfg, mont, antes):
        man = json.loads(MAN.read_text(encoding='utf-8'))
        last = man['arquivos'][-1]['target']
        for r, real in cfg['raizes'].items():
            if last.lower().startswith(r.lower()):
                alvo = Path(real) / last[len(r):].lstrip('\\')
        h = Prende(alvo)
        r1 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec1 = ler(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        shutil.copyfile(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json', ENS / 'K2_recibo_1a_execucao.json')
        h.soltar()
        o = {'implantar_1': {'rc': r1['rc'], 'recibo': resumo_rec(rec1)}}
        r2 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec2 = ler(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        o['implantar_2'] = {'rc': r2['rc'], 'recibo': resumo_rec(rec2),
                            'avisos': rec2['passos']['pre_conferencias'].get('avisos'),
                            'backup_integral': rec2['passos'].get('backup_integral', {}).get('status'),
                            'recibo_1_sobrescrito': rec2.get('stamp') != rec1.get('stamp')}
        o['sim_apos_2'] = sim.estado()
        o['reverter_com_recibo_2'] = reverter()
        o['alvos_apos_reverter'] = alvos_estado()
        o['schema_apos_reverter'] = schema()
        return o
    return com_sim('K2', fn)


def cen_K3():
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg3 = dict(cfg, esperar_parada_s=5)
        p3 = ENS / 'config_K3.json'
        p3.write_text(json.dumps(cfg3, ensure_ascii=False, indent=1), encoding='utf-8')
        r = run([TOOLS_K3 / 'implantar.py', '--config', p3, '--pular-mover-backups'])
        rec = ler(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        time.sleep(3)
        return {'implantar': {'rc': r['rc'], 'recibo': resumo_rec(rec),
                              'tarefa_desabilitada_por_esta_execucao': rec['passos'].get('parar_app', {}).get('tarefa_desabilitada_por_esta_execucao')},
                'sim_apos_falha': sim.estado()}
    return com_sim('K3', fn, tools=TOOLS_K3)


def cen_K4():
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec = ler(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        o = {'implantar': {'rc': r['rc'], 'status': rec['status']}, 'sim_apos_implantar': sim.estado()}
        web = Path(cfg['raizes'][r'C:\IALD\projetos_pyhton\IALD']) / 'iald_web_server.py'
        h = Prende(web)
        o['reverter'] = reverter()
        time.sleep(1)
        o['sim_apos_reverter_com_falha'] = sim.estado()
        o['alvos_apos_reverter'] = alvos_estado()
        o['schema_apos_reverter'] = schema()
        o['lib_mista_le_o_banco'] = lib_le(mont)
        h.soltar()
        o['reverter_de_novo'] = reverter()
        o['alvos_apos_2o_reverter'] = alvos_estado()
        return o
    return com_sim('K4', fn)


def cen_K5():
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        o = {'implantar': {'rc': r['rc'], 'status': ler(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')['status']}}
        rr_p = RAIZ / 'recibos' / 'RECIBO_REVERSAO.json'
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'reverter.py'), '--recibo', str(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')],
                             env=env(slow_alvos(1.0, '.part')), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        t0, morto = time.time(), False
        while time.time() - t0 < 200 and p.poll() is None:
            rr = ler(rr_p) if rr_p.exists() else None
            arqs = (rr or {}).get('passos', {}).get('restaurar_arquivos', {}).get('arquivos') or []
            if len(arqs) >= 6:
                p.kill()
                morto = True
                break
            time.sleep(0.02)
        p.wait(30)
        o['reverter_1_morto'] = morto
        o['alvos_apos_morte'] = alvos_estado()
        o['sim_apos_morte'] = sim.estado()
        o['reverter_2'] = reverter()
        o['alvos_apos_reverter_2'] = alvos_estado()
        return o
    return com_sim('K5', fn)


def main(sel):
    out = {'at': datetime.now().isoformat(timespec='seconds'), 'preparo': preparar(), 'cenarios': {}}
    todos = {'K1a': cen_K1a, 'K1b': cen_K1b, 'K1c': cen_K1c, 'K1d': cen_K1d, 'K2': cen_K2, 'K3': cen_K3, 'K4': cen_K4, 'K5': cen_K5, 'K6': lambda: cen_K6(), 'K1b2': lambda: cen_K1b2()}
    for n, fn in todos.items():
        if sel and n not in sel:
            continue
        t = time.time()
        try:
            res = fn()
        except Exception:  # noqa: BLE001
            res = {'excecao': traceback.format_exc()[-2500:]}
        res['segundos'] = round(time.time() - t, 1)
        out['cenarios'][n] = res
        (REV / 'runs' / ('s5_ensaio%s.json' % ('_' + '_'.join(sel) if sel else ''))).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        print(n, res['segundos'], flush=True)
    print('fim')



# ---- K6 (acrescentado depois do K1b): um LEITOR segura o RECIBO aberto por 2 s no meio do passo 4
def cen_K6():
    def fn(sim, cfg_path, cfg, mont, antes):
        rec_p = RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json'
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(0.4)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        h = None
        t0 = time.time()
        while time.time() - t0 < 200 and p.poll() is None:
            try:
                rec = json.loads(rec_p.read_text(encoding='utf-8')) if rec_p.exists() else None
            except (OSError, ValueError):
                rec = None
            if rec and len(rec['passos'].get('substituir_arquivos', {}).get('arquivos') or []) >= 5:
                h = Prende(rec_p)
                time.sleep(2.0)
                h.soltar()
                break
            time.sleep(0.25)
        out_s, err_s = p.communicate(timeout=300)
        rec = ler(rec_p)
        sub = rec['passos'].get('substituir_arquivos', {})
        o = {'implantar': {'rc': p.returncode, 'stdout': out_s.decode('utf-8', 'replace')[-600:], 'recibo': resumo_rec(rec),
                           'mensagens': {k: v.get('mensagem') for k, v in rec['passos'].items() if v.get('status') == 'FALHOU'}},
             'leitor_segurou': h is not None, 'alvos_apos_falha': alvos_estado(), 'sim_apos_falha': sim.estado()}
        o['reverter'] = reverter()
        o['alvos_apos_reverter'] = alvos_estado()
        return o
    return com_sim('K6', fn)

# ---- K1b2: como K1b, mas sem ler o recibo durante a execucao (condicao pelos arquivos: .bak_ e .tmp_ do 8o alvo)
def cen_K1b2():
    def fn(sim, cfg_path, cfg, mont, antes):
        web_dir = Path(cfg['raizes'][r'C:\IALD\projetos_pyhton\IALD'])
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(1.5)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        t0, morto = time.time(), False
        while time.time() - t0 < 200 and p.poll() is None:
            if list(web_dir.glob('iald_web_server.py.bak_*')) and list(web_dir.glob('iald_web_server.py.tmp_*')):
                p.kill()
                morto = True
                break
            time.sleep(0.05)
        p.wait(30)
        rec = ler(RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        o = {'implantar': {'morto': morto, 'rc': p.returncode, 'recibo': resumo_rec(rec)},
             'tmp_orfaos': sorted(x.name for x in RAIZ.rglob('*.tmp_2*')), 'alvos_apos_morte': alvos_estado(),
             'schema_apos_morte': schema(), 'sim_apos_morte': sim.estado()}
        o['reverter'] = reverter()
        o['alvos_apos_reverter'] = alvos_estado()
        o['tmp_orfaos_apos_reverter'] = sorted(x.name for x in RAIZ.rglob('*.tmp_2*'))
        return o
    return com_sim('K1b2', fn)



if __name__ == '__main__':
    main(sys.argv[1:])
