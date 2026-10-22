# -*- coding: utf-8 -*-
"""R2.1: ensaio de implantação+reversão numa CÓPIA SINTÉTICA (nunca produção), com os cenários K1–K6 da revisão R2
(8_REVISAO_R2/scripts/s5_ensaio.py, adaptado) e o passo 8 lento (P8), agora contra as ferramentas R2.1.

Ferramentas = implantar.py / reverter.py / implantacao_lib.py de 9_R2_1 (sha conferido no preparo) + aplicar_blocos.py e
SESSION_BRIDGE_v2.md de 4_INTEGRACAO/ferramentas. Candidato = candidato_r2_1 com a chave do web server REDIGIDA (mesmo
tamanho; o manifesto copiado recebe o sha recalculado só desse arquivo, nos dois lados). Banco v1 sintético
(store_v1_frozen), superfícies = cópias da integração, D: sintético, processos pelo backend SIMULADO (agendador,
supervisor e web reais em Python; o web simulado ganhou só um atraso opcional de saúde para o P8). Guarda da auditoria
ligada (ACOM_AUDIT_ROOT = 9_R2_1) + gancho de LENTIDÃO opcional em os.rename (para matar no meio).

  K1a mata o implantar no passo 4 (1º arquivo em backup_ok); o harness LÊ o recibo a cada 20 ms (o que no R2 abortava)
  K1b2 mata com o 8º arquivo (iald_web_server.py) em backup_ok
  K1c mata durante o passo 5 (aplicar_blocos.py órfão termina sozinho)
  K1d mata durante a migração --apply
  K2  falha no passo 4 (alvo preso); o operador roda o implantar DE NOVO: deve RECUSAR sem tocar; depois reverter
  K3  o stop script não derruba o app (só o simulador muda): a tarefa deve voltar habilitada e o recibo dizer a verdade
  K4  reverter com o web server preso: NÃO religa; solto o arquivo, o 2º reverter fecha e religa
  K5  mata o reverter no passo 2 e roda de novo
  K6  um leitor segura o recibo 2 s no meio do passo 4: a implantação deve CONCLUIR
  P8  a saúde do app demora mais que esperar_inicio_s: CONCLUIDA_AGUARDANDO_REINICIO, sem mandar reverter

    python -B s5_ensaio_r2_1.py [K1a K2 ...]
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

R21 = Path(__file__).resolve().parents[1]
SRC21 = R21.parent / '9_R2_1'
WORK = R21.parent
INT = WORK / '4_INTEGRACAO'
ENS = R21 / 'ensaio'
TOOLS = ENS / 'tools'
TOOLS_K3 = ENS / 'tools_k3'
SIMS = ENS / 'sim'
SIM_RUNS = ENS / 'sim_run'
CAND = ENS / 'cand' / 'C'
ORIG = ENS / 'orig' / 'C'
MAN = ENS / 'CANDIDATO_MANIFESTO_R2_1_redigido.json'
RAIZ = ENS / 'raiz'
GUARD_SLOW = ENS / 'guardslow'
PY = sys.executable
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,})')
SCOPE = {'house': 'IALD', 'principal': 'operator'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
AGENT = {'id': 'ensaio-r2-1', 'kind': 'agent'}
TEXT = ('heartbeat sample response text ' * 40)[:1200]
SUPERF = ['CLAUDE_global.md', 'AGENTS.md', 'CLAUDE_nativa.md', 'README.md', 'COORDINATOR.md']
sys.path.insert(0, str(R21 / 'suite_r21' / 'copia' / 'testes_r2' / 'nucleo' / 'tests'))
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


# --------------------------------------------------------------------------------------------- preparo
def preparar():
    if ENS.exists():
        shutil.rmtree(ENS)
    log = {}
    for n in ('implantar.py', 'reverter.py', 'implantacao_lib.py'):
        cpb(SRC21 / n, TOOLS / n)
        log[n] = sha(TOOLS / n)[:16]
        assert log[n] == sha(SRC21 / n)[:16]
    cpb(INT / 'ferramentas' / 'aplicar_blocos.py', TOOLS / 'ferramentas' / 'aplicar_blocos.py')
    cpb(INT / 'ferramentas' / 'SESSION_BRIDGE_v2.md', TOOLS / 'ferramentas' / 'SESSION_BRIDGE_v2.md')
    log['aplicar_blocos.py'] = sha(TOOLS / 'ferramentas' / 'aplicar_blocos.py')[:16]
    for n in ('implantar.py', 'reverter.py'):
        cpb(SRC21 / n, TOOLS_K3 / n)
    k3 = (SRC21 / 'implantacao_lib.py').read_bytes() + (
        b'\n\n# --- K3 (ensaio): ambiente em que o stop script nao derruba o app (so o simulador muda)\n'
        b'def _parar_script_sem_efeito(self):\n    return {"rc": 1, "nota": "K3: stop script sem efeito (simulado)"}\n'
        b'ProcessosSim.parar_script = _parar_script_sem_efeito\n')
    (TOOLS_K3 / 'implantacao_lib.py').write_bytes(k3)
    for f in (INT / 'ensaio_implantacao_r2' / 'sim').glob('*.py'):
        cpb(f, SIMS / f.name)
    # P8: o web simulado pode atrasar a saúde (tarefa.json: saude_atraso_s). Só o simulador muda.
    w = (SIMS / 'sim_web.py').read_text(encoding='utf-8')
    alvo = "(PIDS / ('saude_%d' % os.getpid())).write_text('200', encoding='utf-8')"
    assert w.count(alvo) == 1
    w = w.replace(alvo, "time.sleep(float(t.get('saude_atraso_s', 0) or 0))\n" + alvo)
    (SIMS / 'sim_web.py').write_text(w, encoding='utf-8')
    for root, _, files in os.walk(SRC21 / 'candidato_r2_1' / 'C'):
        for f in files:
            s = Path(root) / f
            cpb(s, CAND / s.relative_to(SRC21 / 'candidato_r2_1' / 'C'), red=f == 'iald_web_server.py')
    for root, _, files in os.walk(INT / 'originais' / 'C'):
        for f in files:
            s = Path(root) / f
            cpb(s, ORIG / s.relative_to(INT / 'originais' / 'C'), red=f == 'iald_web_server.py')
    man = json.loads((SRC21 / 'CANDIDATO_MANIFESTO_R2_1.json').read_text(encoding='utf-8'))
    for a in man['arquivos']:
        if a['target'].endswith('iald_web_server.py'):
            a['sha256'] = sha(CAND / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py')
    for o in man['originais']:
        if o['source'].endswith('iald_web_server.py'):
            o['sha256'] = sha(ORIG / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py')
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
    GUARD_SLOW.mkdir(parents=True, exist_ok=True)
    g = (R21 / 'suite_r21' / 'copia' / 'guard' / 'sitecustomize.py').as_posix()
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
    (R21 / 'guard_log').mkdir(exist_ok=True)
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
    for name in SUPERF + ['MEMORY.md']:
        cpb(R21 / 'suite_r21' / 'copia' / 'testes_r2' / 'blocos' / 'copias' / name, RAIZ / 'superficies' / name)
    (RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD').mkdir(parents=True)
    (RAIZ / 'recibos').mkdir()
    state = mem / 'state'
    (state / 'app_outbox').mkdir(parents=True)
    st = store_v1_frozen.MemoryStore(state)
    ids = []
    for k, n in enumerate(sizes):
        cid = 'ctx_%d' % k
        st.ensure_context(cid, objective='Objetivo do ensaio R2.1 %d\r\n' % k, scope=SCOPE, actor=OPERATOR,
                          constraints={'no_remote_calls': True})
        for i in range(1, n + 1):
            ch = {'candidates': [{'id': 'c%d_%04d' % (k, i), 'text': TEXT, 'statute': 'DECLARADO',
                                  'source': {'kind': 'executor', 'ref': 'job:%d' % i}}],
                  'flow': {'phase': 'f%04d' % i, 'next_action': 'seguir'}}
            st.transition(cid, SCOPE, expected_revision=i - 1, event_id='e%d_%04d' % (k, i), actor=AGENT, changes=ch)
        ids.append(cid)
    return {'contexts': ids, 'db_sha256': sha(state / 'memory.sqlite3')}


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
    estranhos = [k for k in extras if not any(x in k for x in EXTRA_OK) and not any(d in '/' + k for d in DIR_OK)]
    return {'identico_nos_originais': not falt and not dif, 'faltando': falt[:10], 'diferentes': dif[:10],
            'n_extras': len(extras), 'extras_estranhos': estranhos[:20]}


def config(sim_dir, nome, **extra):
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
    e.update(PYTHONPATH=str(GUARD_SLOW), ACOM_AUDIT_ROOT=str(R21), PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
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


def recibos_impl():
    return sorted(p for p in (RAIZ / 'recibos').glob('RECIBO_IMPLANTACAO_2*.json'))


def recibo_impl_ultimo():
    r = recibos_impl()
    return r[-1] if r else None


def recibo_rev_ultimo():
    r = sorted((RAIZ / 'recibos').glob('RECIBO_REVERSAO_2*.json'))
    return r[-1] if r else None


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
    def __init__(self, nome, tools=TOOLS, **tarefa_extra):
        sys.path.insert(0, str(tools))
        from implantacao_lib import ProcessosSim
        sys.path.pop(0)
        self.dir = SIM_RUNS / nome
        if self.dir.exists():
            shutil.rmtree(self.dir)
        (self.dir / 'pids').mkdir(parents=True)
        (self.dir / 'comandos').mkdir()
        t = {'nome': 'IALD Web Server (simulada)', 'enabled': True, 'restart_count': 3, 'restart_interval_s': 1.5,
             'scripts': str(SIMS), 'mem_root': str(RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD')}
        t.update(tarefa_extra)
        (self.dir / 'tarefa.json').write_text(json.dumps(t), encoding='utf-8')
        (self.dir / 'estado_agendador.json').write_text('{}', encoding='utf-8')
        self.ag = subprocess.Popen([PY, '-X', 'utf8', str(SIMS / 'sim_agendador.py'), str(self.dir)], env=env(),
                                   stdout=open(self.dir / 'saida_agendador.log', 'ab'), stderr=subprocess.STDOUT)
        self.b = ProcessosSim(self.dir)
        time.sleep(0.5)

    def subir(self, limite=30):
        self.b.tarefa_iniciar()
        t0 = time.time()
        while time.time() - t0 < limite:
            p = self.b.listar()
            if self.b.saude()[0] and len(p['web']) == 1 and len(p['supervisores']) == 1:
                return
            time.sleep(0.3)
        raise RuntimeError('sim nao subiu')

    def estado(self):
        p = self.b.listar()
        return {'tarefa_habilitada': self.b.tarefa_ler().get('habilitada'), 'sup': len(p['supervisores']),
                'web': [w.get('store_sha16') for w in p['web']], 'saude': self.b.saude()[0]}

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
    cfg = json.loads((ENS / 'config_base.json').read_text(encoding='utf-8'))
    out = {}
    for a in man['arquivos']:
        t = a['target']
        p = None
        for r, real in sorted(cfg['raizes'].items(), key=lambda kv: -len(kv[0])):
            if t.lower().startswith(r.lower() + '\\'):
                p = Path(real) / t[len(r):].lstrip('\\')
                break
        s = sha(p) if p.exists() else None
        out[t.rsplit('\\', 1)[-1]] = 'candidato' if s == a['sha256'] else 'original' if s == orig.get(t.lower()) else 'ausente' if s is None else 'outro'
    return out


def contar(est):
    c = {}
    for v in est.values():
        c[v] = c.get(v, 0) + 1
    return c


def schema():
    db = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state' / 'memory.sqlite3'
    if not db.exists():
        return None
    c = sqlite3.connect('file:%s?mode=ro' % db.as_posix(), uri=True)
    try:
        return c.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]
    finally:
        c.close()


def resumo_rec(rec):
    if not rec:
        return None
    sub = rec['passos'].get('substituir_arquivos', {})
    return {'status': rec['status'], 'mudancas_iniciadas': rec.get('mudancas_iniciadas'),
            'passos': {k: v['status'] for k, v in rec['passos'].items()},
            'fases': [a.get('fase') for a in sub.get('arquivos') or []], 'acao_requerida': rec.get('acao_requerida'),
            'apos_falha': rec.get('apos_falha')}


def implantar_e_matar(cfg_path, cond, slow=None, tools=TOOLS, extra_args=(), limite=240):
    p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(tools / 'implantar.py'), '--config', str(cfg_path)] + list(extra_args),
                         env=env(slow), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t0 = time.time()
    morto = False
    leituras = 0
    while time.time() - t0 < limite:
        if p.poll() is not None:
            break
        rp = recibo_impl_ultimo()
        rec = ler(rp) if rp else None
        leituras += 1
        if rec and cond(rec):
            p.kill()
            morto = True
            break
        time.sleep(0.02)
    p.wait(30)
    return {'morto': morto, 'rc': p.returncode, 'leituras_do_recibo': leituras, 'recibo': ler(recibo_impl_ultimo())}


def reverter(recibo=None, slow=None, tools=TOOLS, args=()):
    recibo = recibo or recibo_impl_ultimo()
    r = run([tools / 'reverter.py', '--recibo', recibo] + list(args), slow=slow)
    rr = ler(recibo_rev_ultimo())
    return {'rc': r['rc'], 'recibo_implantacao': Path(recibo).name, 'status': rr and rr['status'], 'falhas': rr and rr['falhas'],
            'app_religado': rr and rr.get('app_religado'), 'acao_requerida': rr and rr.get('acao_requerida'),
            'passos': rr and {k: (v['status'], (v.get('mensagem') or v.get('nota') or '')[:160]) for k, v in rr['passos'].items()}}


def com_sim(nome, fn, sizes=(12, 6, 0), tools=TOOLS, **tarefa_extra):
    mont = montar_raiz(sizes)
    sim = Sim(nome, tools, **tarefa_extra)
    try:
        sim.subir()
        cfg_path, cfg = config(sim.dir, nome)
        (ENS / 'config_base.json').write_text(json.dumps(cfg, ensure_ascii=False), encoding='utf-8')
        antes = inventario()
        out = fn(sim, cfg_path, cfg, mont, antes)
        out['estado_sim_final'] = sim.estado()
        out['comparacao_final'] = comparar(antes, inventario())
        db = RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state' / 'memory.sqlite3'
        out['banco_igual_ao_original'] = db.exists() and sha(db) == mont['db_sha256']
        out['lib_le_o_banco'] = lib_le(mont)
        out['schema_final'] = schema()
        out['tmp_orfaos_final'] = sorted(p.name for p in RAIZ.rglob('*.tmp_2*'))
        return out
    finally:
        sim.encerrar()


def slow_alvos(s=1.0, src='.tmp_'):
    return {'SLOW_RENAME_S': str(s), 'SLOW_RENAME_MARK': str(RAIZ / 'C'), 'SLOW_RENAME_SRC': src}


# ------------------------------------------------------------------------------------------------ cenários
def k1(nome, cond, slow, sizes=(12, 6, 0), espera_orfao=0):
    def fn(sim, cfg_path, cfg, mont, antes):
        r = implantar_e_matar(cfg_path, cond, slow=slow, extra_args=['--pular-mover-backups'])
        o = {'implantar': {'morto': r['morto'], 'rc': r['rc'], 'leituras_do_recibo': r['leituras_do_recibo'],
                           'recibo': resumo_rec(r['recibo'])}}
        o['tmp_orfaos'] = sorted(p.name for p in RAIZ.rglob('*.tmp_2*'))
        o['alvos_apos_morte'] = contar(alvos_estado())
        o['schema_apos_morte'] = schema()
        o['sim_apos_morte'] = sim.estado()
        if espera_orfao:
            time.sleep(espera_orfao)
        o['reverter'] = reverter()
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim(nome, fn, sizes)


def cen_K1a():
    return k1('K1a', lambda r: any(a.get('fase') == 'backup_ok' for a in (r['passos'].get('substituir_arquivos', {}).get('arquivos') or [])),
              slow_alvos(1.5))


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
        o = {'implantar': {'morto': morto, 'rc': p.returncode, 'recibo': resumo_rec(ler(recibo_impl_ultimo()))},
             'tmp_orfaos': sorted(x.name for x in RAIZ.rglob('*.tmp_2*')), 'alvos_apos_morte': contar(alvos_estado()),
             'schema_apos_morte': schema(), 'sim_apos_morte': sim.estado()}
        o['reverter'] = reverter()
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('K1b2', fn)


def cen_K1c():
    return k1('K1c', lambda r: 'aplicar_blocos' in r['passos'], slow_alvos(0.6), espera_orfao=6)


def cen_K1d():
    return k1('K1d', lambda r: 'migracao' in (r.get('mudancas_iniciadas') or []), None, sizes=(150, 50, 0))


def cen_K2():
    def fn(sim, cfg_path, cfg, mont, antes):
        man = json.loads(MAN.read_text(encoding='utf-8'))
        last = man['arquivos'][-1]['target']
        alvo = None
        for r, real in sorted(cfg['raizes'].items(), key=lambda kv: -len(kv[0])):
            if last.lower().startswith(r.lower() + '\\'):
                alvo = Path(real) / last[len(r):].lstrip('\\')
                break
        h = Prende(alvo)
        r1 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec1_p = recibo_impl_ultimo()
        rec1_bytes = rec1_p.read_bytes()
        h.soltar()
        o = {'implantar_1': {'rc': r1['rc'], 'recibo': rec1_p.name, 'resumo': resumo_rec(ler(rec1_p))},
             'alvos_apos_1': contar(alvos_estado()), 'sim_apos_1': sim.estado()}
        r2 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        recs = recibos_impl()
        rec2_p = recs[-1]
        rec2 = ler(rec2_p)
        o['implantar_2'] = {'rc': r2['rc'], 'recibo': rec2_p.name, 'status': rec2['status'],
                            'passos': {k: v['status'] for k, v in rec2['passos'].items()},
                            'acao_requerida': rec2.get('acao_requerida'),
                            'recibo_1_intocado': rec1_p.read_bytes() == rec1_bytes, 'n_recibos_implantacao': len(recs)}
        o['alvos_apos_2'] = contar(alvos_estado())
        o['sim_apos_2'] = sim.estado()
        o['reverter_com_o_recibo_indicado'] = reverter(recibo=rec1_p)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        o['schema_apos_reverter'] = schema()
        # depois de revertida, a trava não bloqueia mais (um dry-run conta: o passo T fica OK)
        r3 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--dry-run'])
        rec3 = ler(sorted((RAIZ / 'recibos').glob('RECIBO_IMPLANTACAO_dry_run_*.json'))[-1])
        o['dry_run_depois_de_revertida'] = {'rc': r3['rc'], 'status': rec3['status'],
                                            'trava': rec3['passos'].get('trava_recibo_anterior', {}).get('status')}
        return o
    return com_sim('K2', fn)


def cen_K3():
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg3 = dict(cfg, esperar_parada_s=5)
        p3 = ENS / 'config_K3.json'
        p3.write_text(json.dumps(cfg3, ensure_ascii=False, indent=1), encoding='utf-8')
        r = run([TOOLS_K3 / 'implantar.py', '--config', p3, '--pular-mover-backups'])
        rec = ler(recibo_impl_ultimo())
        time.sleep(3)
        af = rec.get('apos_falha') or {}
        return {'implantar': {'rc': r['rc'], 'status': rec['status'],
                              'tarefa_desabilitada_por_esta_execucao': rec['passos'].get('parar_app', {}).get('tarefa_desabilitada_por_esta_execucao'),
                              'apos_falha_nota': af.get('nota'), 'tarefa_reabilitada': af.get('tarefa_reabilitada'),
                              'estado_real': af.get('estado_real'), 'acao_sugerida': af.get('acao_sugerida')},
                'diz_nada_mudou': 'nada mudou' in json.dumps(af, ensure_ascii=False),
                'alvos': contar(alvos_estado()), 'sim_apos_falha': sim.estado()}
    return com_sim('K3', fn, tools=TOOLS_K3)


def cen_K4():
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}, 'sim_apos_implantar': sim.estado()}
        web = Path(cfg['raizes'][r'C:\IALD\projetos_pyhton\IALD']) / 'iald_web_server.py'
        h = Prende(web)
        o['reverter'] = reverter(recibo=rp)
        time.sleep(2)
        o['sim_apos_reverter_com_falha'] = sim.estado()
        o['alvos_apos_reverter_com_falha'] = contar(alvos_estado())
        o['schema_apos_reverter_com_falha'] = schema()
        h.soltar()
        o['reverter_de_novo'] = reverter(recibo=rp)
        o['alvos_apos_2o_reverter'] = contar(alvos_estado())
        o['sim_apos_2o_reverter'] = sim.estado()
        return o
    return com_sim('K4', fn)


def cen_K5():
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}}
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'reverter.py'), '--recibo', str(rp)],
                             env=env(slow_alvos(1.0, '.part')), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        t0, morto = time.time(), False
        while time.time() - t0 < 200 and p.poll() is None:
            rr_p = recibo_rev_ultimo()
            rr = ler(rr_p) if rr_p else None
            arqs = (rr or {}).get('passos', {}).get('restaurar_arquivos', {}).get('arquivos') or []
            if len(arqs) >= 6:
                p.kill()
                morto = True
                break
            time.sleep(0.02)
        p.wait(30)
        o['reverter_1_morto'] = morto
        o['alvos_apos_morte'] = contar(alvos_estado())
        o['sim_apos_morte'] = sim.estado()
        o['reverter_2'] = reverter(recibo=rp)
        o['alvos_apos_reverter_2'] = contar(alvos_estado())
        return o
    return com_sim('K5', fn)


def cen_K6():
    def fn(sim, cfg_path, cfg, mont, antes):
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(0.4)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        h = None
        t0 = time.time()
        while time.time() - t0 < 200 and p.poll() is None:
            rp = recibo_impl_ultimo()
            try:
                rec = json.loads(rp.read_text(encoding='utf-8')) if rp else None
            except (OSError, ValueError):
                rec = None
            if rec and len(rec['passos'].get('substituir_arquivos', {}).get('arquivos') or []) >= 5:
                h = Prende(rp)
                time.sleep(2.0)
                h.soltar()
                break
            time.sleep(0.25)
        out_s, err_s = p.communicate(timeout=300)
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        r21 = rec['passos'].get('substituir_arquivos', {})
        return {'implantar': {'rc': p.returncode, 'status': rec['status'], 'passos': {k: v['status'] for k, v in rec['passos'].items()},
                              'arquivos_substituidos': sum(a.get('fase') == 'substituido' for a in r21.get('arquivos') or [])},
                'leitor_segurou_2s': h is not None, 'alvos_apos': contar(alvos_estado()), 'sim_apos': sim.estado(),
                'reverter': reverter(recibo=rp), 'alvos_apos_reverter': contar(alvos_estado())}
    return com_sim('K6', fn)


def cen_P8():
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg8 = dict(cfg, esperar_inicio_s=3)
        p8 = ENS / 'config_P8.json'
        p8.write_text(json.dumps(cfg8, ensure_ascii=False, indent=1), encoding='utf-8')
        t = json.loads((sim.dir / 'tarefa.json').read_text(encoding='utf-8'))
        t['saude_atraso_s'] = 8                      # só o web relançado pela implantação demora 8 s para ficar saudável
        sim.b._escrever_tarefa(t)
        r = run([TOOLS / 'implantar.py', '--config', p8, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        o = {'implantar': {'rc': r['rc'], 'status': rec['status'], 'passos': {k: v['status'] for k, v in rec['passos'].items()},
                           'acao_requerida': rec.get('acao_requerida'), 'manda_reverter': 'reverter.py' in (rec.get('acao_requerida') or '')},
             'alvos': contar(alvos_estado()), 'sim_logo_apos': sim.estado()}
        time.sleep(10)
        o['sim_10s_depois'] = sim.estado()
        o['reverter_para_limpar_o_ensaio'] = reverter(recibo=rp)
        return o
    return com_sim('P8', fn)


def main(sel):
    out = {'at': datetime.now().isoformat(timespec='seconds'), 'preparo': preparar(), 'cenarios': {}}
    todos = {'K1a': cen_K1a, 'K1b2': cen_K1b2, 'K1c': cen_K1c, 'K1d': cen_K1d, 'K2': cen_K2, 'K3': cen_K3, 'K4': cen_K4,
             'K5': cen_K5, 'K6': cen_K6, 'P8': cen_P8}
    nome = 's5_ensaio_r2_1%s.json' % ('_' + '_'.join(sel) if sel else '')
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
        (R21 / 'runs' / nome).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        print(n, res['segundos'], flush=True)
    print('fim')



# =====================================================================================================================
# REVISOR c1 R2.1: cenarios em FORMA NOVA (acrescentados ao ensaio adaptado; mesmas ferramentas R2.1 copiadas byte a byte)
# =====================================================================================================================
import ctypes  # noqa: E402

TOOLS_K3B = ENS / 'tools_k3b'


def preparar_rev(log):
    """Variante K3b: o stop script nao derruba o app E o Enable-ScheduledTask falha (so o simulador muda).
    P8b: o web simulado pode morrer ao nascer (tarefa.json: web_morre_ao_nascer)."""
    for n in ('implantar.py', 'reverter.py'):
        cpb(SRC21 / n, TOOLS_K3B / n)
    k3b = (SRC21 / 'implantacao_lib.py').read_bytes() + (
        b'\n\n# --- K3b (revisor c1 R2.1): stop sem efeito + Enable falha (so o simulador muda)\n'
        b'def _parar_script_sem_efeito(self):\n    return {"rc": 1, "nota": "K3b: stop script sem efeito (simulado)"}\n'
        b'def _habilitar_falha(self):\n    raise ImplantacaoError("K3b: Enable-ScheduledTask falhou (simulado)")\n'
        b'ProcessosSim.parar_script = _parar_script_sem_efeito\nProcessosSim.tarefa_habilitar = _habilitar_falha\n')
    (TOOLS_K3B / 'implantacao_lib.py').write_bytes(k3b)
    w = (SIMS / 'sim_web.py').read_text(encoding='utf-8')
    alvo = "time.sleep(float(t.get('saude_atraso_s', 0) or 0))\n"
    assert w.count(alvo) == 1
    w = w.replace(alvo, "if t.get('web_morre_ao_nascer'):\n    raise SystemExit(7)\n" + alvo)
    (SIMS / 'sim_web.py').write_text(w, encoding='utf-8')
    log['tools_k3b_lib_sha16'] = sha(TOOLS_K3B / 'implantacao_lib.py')[:16]
    log['sim_web_sha16'] = sha(SIMS / 'sim_web.py')[:16]
    return log


class PrendeExclusivo:
    """Abre o arquivo SEM compartilhamento (share=0): ninguem le, escreve, renomeia ou apaga ate soltar."""
    def __init__(self, path):
        self.flag = ENS / ('soltaX_%d_%d' % (os.getpid(), int(time.time() * 1000)))
        self.ready = Path(str(self.flag) + '_pronto')
        code = ('import sys,time,os,ctypes\nfrom ctypes import wintypes\n'
                'k=ctypes.WinDLL("kernel32",use_last_error=True)\n'
                'k.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]\n'
                'k.CreateFileW.restype=wintypes.HANDLE\n'
                'h=k.CreateFileW(sys.argv[1],0x80000000,0,None,3,0,None)\n'
                'open(sys.argv[3],"w").write(str(ctypes.get_last_error()) if h in (None,0,(1<<64)-1) else "ok")\n'
                'while not os.path.exists(sys.argv[2]): time.sleep(0.05)\n'
                'k.CloseHandle(h)\n')
        self.p = subprocess.Popen([PY, '-c', code, str(path), str(self.flag), str(self.ready)], env=env())
        t0 = time.time()
        while not self.ready.exists() and time.time() - t0 < 10:
            time.sleep(0.02)
        self.estado = self.ready.read_text() if self.ready.exists() else None

    def soltar(self):
        self.flag.write_text('x')
        self.p.wait(10)


def alvo_de(cfg, target):
    for r, real in sorted(cfg['raizes'].items(), key=lambda kv: -len(kv[0])):
        if target.lower().startswith(r.lower() + '\\'):
            return Path(real) / target[len(r):].lstrip('\\')
    return None


def k2_variante(nome, mexer):
    """1a implantacao falha no passo 4 (ultimo alvo preso); o operador MEXE no recibo (renomeia / apaga / corrompe)
    e roda o implantar de novo. Mede o que a trava faz e onde o estado fica."""
    def fn(sim, cfg_path, cfg, mont, antes):
        man = json.loads(MAN.read_text(encoding='utf-8'))
        alvo = alvo_de(cfg, man['arquivos'][-1]['target'])
        h = Prende(alvo)
        r1 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec1_p = recibo_impl_ultimo()
        o = {'implantar_1': {'rc': r1['rc'], 'recibo': rec1_p.name, 'status': ler(rec1_p)['status']},
             'alvos_apos_1': contar(alvos_estado()), 'schema_apos_1': schema(), 'sim_apos_1': sim.estado()}
        h.soltar()
        o['mexida'] = mexer(rec1_p)
        r2 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        recs = recibos_impl()
        rec2_p = [p for p in recs if p != rec1_p][-1] if [p for p in recs if p != rec1_p] else None
        rec2 = ler(rec2_p) if rec2_p else None
        o['implantar_2'] = {'rc': r2['rc'], 'stdout': r2['stdout'][-700:], 'recibo': rec2_p and rec2_p.name,
                            'status': rec2 and rec2['status'],
                            'passos': rec2 and {k: v['status'] for k, v in rec2['passos'].items()},
                            'avisos_pre': rec2 and (rec2['passos'].get('pre_conferencias') or {}).get('avisos'),
                            'backup_integral': rec2 and (rec2['passos'].get('backup_integral') or {}).get('status')}
        o['alvos_apos_2'] = contar(alvos_estado())
        o['schema_apos_2'] = schema()
        o['sim_apos_2'] = sim.estado()
        # o operador segue a secao 4: reverter --config
        rc = run([TOOLS / 'reverter.py', '--config', cfg_path])
        rr = ler(recibo_rev_ultimo()) if recibo_rev_ultimo() else None
        o['reverter_config'] = {'rc': rc['rc'], 'stdout': rc['stdout'][-500:], 'stderr': rc['stderr'][-400:],
                                'status': rr and rr['status'], 'recibo_impl': rr and Path(rr['recibo_implantacao']).name,
                                'passos': rr and {k: v['status'] for k, v in rr['passos'].items()},
                                'app_religado': rr and rr.get('app_religado')}
        o['alvos_apos_reverter_config'] = contar(alvos_estado())
        o['schema_apos_reverter_config'] = schema()
        o['sim_apos_reverter_config'] = sim.estado()
        return o
    return com_sim(nome, fn)


def _renomear(p):
    novo = p.with_name(p.name + '.lido')
    os.replace(p, novo)
    return {'acao': 'renomeado', 'para': novo.name}


def _apagar(p):
    p.unlink()
    return {'acao': 'apagado'}


def _corromper(p):
    b = p.read_bytes()
    p.write_bytes(b[:len(b) // 2])
    return {'acao': 'truncado pela metade', 'bytes': len(b) // 2}


def cen_K2b():
    return k2_variante('K2b_renomeado', _renomear)


def cen_K2c():
    return k2_variante('K2c_apagado', _apagar)


def cen_K2d():
    return k2_variante('K2d_corrompido', _corromper)


def cen_K3b():
    """O stop script nao derruba o app E o Enable-ScheduledTask falha: o recibo deve dizer que a tarefa ficou
    desabilitada e o que fazer."""
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg3 = dict(cfg, esperar_parada_s=5)
        p3 = ENS / 'config_K3b.json'
        p3.write_text(json.dumps(cfg3, ensure_ascii=False, indent=1), encoding='utf-8')
        r = run([TOOLS_K3B / 'implantar.py', '--config', p3, '--pular-mover-backups'])
        rec = ler(recibo_impl_ultimo())
        af = rec.get('apos_falha') or {}
        time.sleep(2)
        return {'implantar': {'rc': r['rc'], 'stdout': r['stdout'][-600:], 'status': rec['status'], 'nota': af.get('nota'),
                              'tarefa_erro': af.get('tarefa_erro'), 'acao_sugerida': af.get('acao_sugerida'),
                              'acao_requerida': rec.get('acao_requerida')},
                'sim_apos_falha': sim.estado(), 'alvos': contar(alvos_estado())}
    return com_sim('K3b', fn, tools=TOOLS_K3B)


def cen_K3r():
    """Implantacao CONCLUIDA; depois o REVERTER encontra um stop script sem efeito (K3 do lado do reverter)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg3 = dict(cfg, esperar_parada_s=5)
        p3 = ENS / 'config_K3r.json'
        p3.write_text(json.dumps(cfg3, ensure_ascii=False, indent=1), encoding='utf-8')
        r = run([TOOLS / 'implantar.py', '--config', p3, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}, 'sim_apos_implantar': sim.estado()}
        rv = run([TOOLS_K3 / 'reverter.py', '--recibo', rp])
        rr = ler(recibo_rev_ultimo())
        o['reverter_k3'] = {'rc': rv['rc'], 'status': rr['status'], 'falhas': rr['falhas'], 'app_religado': rr.get('app_religado'),
                            'passos': {k: v['status'] for k, v in rr['passos'].items()}, 'acao_requerida': rr.get('acao_requerida'),
                            'diz_app_parado': 'fica parado' in (rr.get('acao_requerida') or '')}
        o['sim_apos_reverter_k3'] = sim.estado()
        o['alvos_apos_reverter_k3'] = contar(alvos_estado())
        o['reverter_normal'] = reverter(recibo=rp)
        o['alvos_apos_reverter_normal'] = contar(alvos_estado())
        return o
    return com_sim('K3r', fn)


def _reverter_com_gatilho(rp, gatilho, acao, limite=240):
    """Roda o reverter e, quando o recibo de reversao satisfaz `gatilho`, executa `acao()` UMA vez."""
    antes = set(p.name for p in (RAIZ / 'recibos').glob('RECIBO_REVERSAO_2*.json'))
    p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'reverter.py'), '--recibo', str(rp)], env=env(),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t0, feito, res = time.time(), False, None
    while time.time() - t0 < limite and p.poll() is None:
        novos = [x for x in (RAIZ / 'recibos').glob('RECIBO_REVERSAO_2*.json') if x.name not in antes]
        if novos and not feito:
            try:
                rr = json.loads(novos[-1].read_text(encoding='utf-8'))
            except (OSError, ValueError):
                rr = None
            if rr and gatilho(rr):
                res = acao()
                feito = True
        time.sleep(0.01)
    out, err = p.communicate(timeout=300)
    rr = ler(recibo_rev_ultimo())
    return {'rc': p.returncode, 'acao_feita': feito, 'acao_res': res, 'stdout': out.decode('utf-8', 'replace')[-700:],
            'status': rr['status'], 'falhas': rr['falhas'], 'app_religado': rr.get('app_religado'),
            'passos': {k: (v['status'], (v.get('mensagem') or '')[:120]) for k, v in rr['passos'].items()},
            'acao_requerida': rr.get('acao_requerida')}


def _conferir_ok(rr):
    return (rr.get('passos', {}).get('conferir_alvos') or {}).get('status') == 'OK'


def cen_K4b():
    """K4 com o alvo travado SO na conferencia final (lock exclusivo depois de conferir_alvos OK)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}}
        man = json.loads(MAN.read_text(encoding='utf-8'))
        alvo = alvo_de(cfg, man['arquivos'][3]['target'])
        trava = {}

        def acao():
            trava['h'] = PrendeExclusivo(alvo)
            return {'alvo': alvo.name, 'lock': trava['h'].estado}
        o['reverter_1'] = _reverter_com_gatilho(rp, _conferir_ok, acao)
        o['sim_apos_reverter_1'] = sim.estado()
        o['alvos_apos_reverter_1'] = contar(alvos_estado()) if 'h' not in trava else 'alvo travado (nao legivel)'
        if 'h' in trava:
            trava['h'].soltar()
        o['alvos_apos_soltar'] = contar(alvos_estado())
        o['schema_apos_reverter_1'] = schema()
        o['trava_implantar_ve_pendente'] = _trava_ve(cfg_path)
        o['reverter_2'] = reverter(recibo=rp)
        o['alvos_apos_reverter_2'] = contar(alvos_estado())
        return o
    return com_sim('K4b', fn)


def cen_K4c():
    """K4 com um alvo MODIFICADO (bytes do candidato de volta) depois de conferir_alvos OK, antes de religar."""
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}}
        man = json.loads(MAN.read_text(encoding='utf-8'))
        item = man['arquivos'][3]
        alvo = alvo_de(cfg, item['target'])
        cand = CAND / Path(*Path(item['target']).parts[1:])

        def acao():
            alvo.write_bytes(cand.read_bytes())
            return {'alvo': alvo.name, 'escrito': 'bytes do candidato'}
        o['reverter_1'] = _reverter_com_gatilho(rp, _conferir_ok, acao)
        o['sim_apos_reverter_1'] = sim.estado()
        o['alvos_apos_reverter_1'] = contar(alvos_estado())
        o['trava_implantar_ve_pendente'] = _trava_ve(cfg_path)
        o['reverter_2'] = reverter(recibo=rp)
        o['alvos_apos_reverter_2'] = contar(alvos_estado())
        return o
    return com_sim('K4c', fn)


def _trava_ve(cfg_path):
    """A trava do implantar (recibos_pendentes, so leitura) ainda ve a implantacao como pendente?"""
    sys.path.insert(0, str(TOOLS))
    try:
        import implantacao_lib as L
        cfg = json.loads(Path(cfg_path).read_text(encoding='utf-8'))
        r = L.recibos_pendentes([cfg['recibos_dir']])
        return {'pendentes': [Path(p['recibo']).name for p in r['pendentes']], 'ilegiveis': len(r['ilegiveis'])}
    finally:
        sys.path.pop(0)


def cen_K6b():
    """Um leitor segura um ALVO (o 1o, CORE.md) por 2,5 s quando o passo 4 comeca (antivirus num .py recem-escrito)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        man = json.loads(MAN.read_text(encoding='utf-8'))
        alvo = alvo_de(cfg, man['arquivos'][0]['target'])
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(0.4)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        h = None
        t0 = time.time()
        while time.time() - t0 < 200 and p.poll() is None:
            rp = recibo_impl_ultimo()
            try:
                rec = json.loads(rp.read_text(encoding='utf-8')) if rp else None
            except (OSError, ValueError):
                rec = None
            if rec and 'substituir_arquivos' in rec['passos']:
                h = Prende(alvo)
                time.sleep(2.5)
                h.soltar()
                break
            time.sleep(0.01)
        out_s, err_s = p.communicate(timeout=300)
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        sub = rec['passos'].get('substituir_arquivos', {})
        o = {'implantar': {'rc': p.returncode, 'status': rec['status'],
                           'substituidos': sum(a.get('fase') == 'substituido' for a in sub.get('arquivos') or [])},
             'leitor_segurou_alvo': h is not None, 'alvos': contar(alvos_estado()), 'sim': sim.estado()}
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('K6b', fn)


def cen_K6c():
    """Um leitor segura o RECIBO por 40 s (acima do limite de 30 s) no meio do passo 4."""
    def fn(sim, cfg_path, cfg, mont, antes):
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(0.4)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        h = None
        t0 = time.time()
        while time.time() - t0 < 200 and p.poll() is None:
            rp = recibo_impl_ultimo()
            try:
                rec = json.loads(rp.read_text(encoding='utf-8')) if rp else None
            except (OSError, ValueError):
                rec = None
            if rec and len(rec['passos'].get('substituir_arquivos', {}).get('arquivos') or []) >= 5:
                h = Prende(rp)
                time.sleep(40.0)
                h.soltar()
                break
            time.sleep(0.1)
        out_s, err_s = p.communicate(timeout=400)
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        sub = rec['passos'].get('substituir_arquivos', {})
        o = {'implantar': {'rc': p.returncode, 'stdout': out_s.decode('utf-8', 'replace')[-700:], 'status': rec['status'],
                           'passos': {k: v['status'] for k, v in rec['passos'].items()},
                           'fases': [a.get('fase') for a in sub.get('arquivos') or []],
                           'acao_requerida': rec.get('acao_requerida')},
             'leitor_segurou_40s': h is not None, 'alvos': contar(alvos_estado()), 'sim': sim.estado(),
             'tmp_orfaos': sorted(x.name for x in RAIZ.rglob('*.tmp_2*'))}
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('K6c', fn)


def cen_P8b():
    """O web v2 morre ao nascer (o supervisor fica vivo relancando): o que o operador ve no passo 8."""
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg8 = dict(cfg, esperar_inicio_s=6)
        p8 = ENS / 'config_P8b.json'
        p8.write_text(json.dumps(cfg8, ensure_ascii=False, indent=1), encoding='utf-8')
        t = json.loads((sim.dir / 'tarefa.json').read_text(encoding='utf-8'))
        t['web_morre_ao_nascer'] = True
        sim.b._escrever_tarefa(t)
        r = run([TOOLS / 'implantar.py', '--config', p8, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        o = {'implantar': {'rc': r['rc'], 'status': rec['status'], 'passos': {k: v['status'] for k, v in rec['passos'].items()},
                           'acao_requerida': rec.get('acao_requerida')}, 'sim_logo_apos': sim.estado()}
        t['web_morre_ao_nascer'] = False
        sim.b._escrever_tarefa(t)
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('P8b', fn)


def main_rev(sel):
    out = {'at': datetime.now().isoformat(timespec='seconds'), 'preparo': preparar_rev(preparar()), 'cenarios': {}}
    todos = {'K2': cen_K2, 'K3': cen_K3, 'K4': cen_K4, 'K6': cen_K6, 'P8': cen_P8,
             'K2b': cen_K2b, 'K2c': cen_K2c, 'K2d': cen_K2d, 'K3b': cen_K3b, 'K3r': cen_K3r, 'K4b': cen_K4b, 'K4c': cen_K4c,
             'K6b': cen_K6b, 'K6c': cen_K6c, 'P8b': cen_P8b, 'CFG': lambda: cen_CFG()}
    nome = 's5_ensaio_rev%s.json' % ('_' + '_'.join(sel) if sel else '')
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
        (R21 / 'runs' / nome).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        print(n, res['segundos'], flush=True)
    print('fim')


def cen_CFG():
    """Os comandos da secao 4 na forma positiva: implantar (CONCLUIDA), reverter --config --dry-run, reverter --config
    (acha a unica pendente), reverter --config de novo (0 pendentes: recusa), implantar --dry-run (trava OK)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        o = {}
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--dry-run'])
        o['dry_run_antes'] = {'rc': r['rc'], 'stdout': r['stdout'][-300:]}
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        o['implantar'] = {'rc': r['rc'], 'status': ler(recibo_impl_ultimo())['status']}
        r = run([TOOLS / 'reverter.py', '--config', cfg_path, '--dry-run'])
        o['reverter_config_dry_run'] = {'rc': r['rc'], 'stdout': r['stdout'][-400:]}
        o['sim_apos_dry_run_reverter'] = sim.estado()
        r = run([TOOLS / 'reverter.py', '--config', cfg_path])
        rr = ler(recibo_rev_ultimo())
        o['reverter_config'] = {'rc': r['rc'], 'status': rr['status'], 'recibo_impl': Path(rr['recibo_implantacao']).name,
                                'app_religado': rr.get('app_religado')}
        o['alvos_apos'] = contar(alvos_estado())
        r = run([TOOLS / 'reverter.py', '--config', cfg_path])
        o['reverter_config_de_novo'] = {'rc': r['rc'], 'stderr_fim': r['stderr'][-220:]}
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--dry-run'])
        o['dry_run_depois'] = {'rc': r['rc'], 'stdout': r['stdout'][-200:]}
        return o
    return com_sim('CFG', fn)


if __name__ == '__main__':
    main_rev(sys.argv[1:])
