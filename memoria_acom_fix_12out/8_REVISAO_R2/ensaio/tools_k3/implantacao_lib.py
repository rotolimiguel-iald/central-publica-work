# -*- coding: utf-8 -*-
"""Biblioteca comum de implantar.py / reverter.py (conserto ACOM 12/10; R2 de 13/10). Só stdlib.

Regras: hash sempre lido do artefato; cópia de BYTES conferida (tempário -> fsync -> conferência -> os.replace);
backup de bytes antes de tocar qualquer arquivo existente; nada que exista antes é apagado (o que sai de lugar é
renomeado ou movido com sha256 conferido; só o tempário que a própria ferramenta criou e que nunca virou arquivo é
removido); recibo gravado a cada mudança; falha é visível.

R2 (achados bloqueantes da revisão de 13/10):
  * achado 1 — a escrita registra cada arquivo no recibo ANTES de tocá-lo (o reverter restaura o que foi tocado
    mesmo quando a implantação falhou no meio); o tempário de uma escrita que falhou é removido.
  * achado 3 — gestão de processos por um BACKEND (PowerShell em produção; simulado no ensaio), com a Tarefa
    Agendada «IALD Web Server» DESABILITADA antes de parar o supervisor (o RestartCount 3 / PT2M da tarefa não
    relança o app no meio dos passos), conferência de silêncio depois de parar e antes de cada passo que muda o
    banco ou os arquivos, e o reinício pela própria tarefa (Start-ScheduledTask: o processo nasce no Agendador,
    fora do job object do shell que rodou a ferramenta). Sem tarefa, o reinício usa Win32_Process.Create (WMI),
    também fora do job.
"""
from __future__ import annotations
import ctypes
import hashlib
import json
import os
import shutil
import signal
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


class ImplantacaoError(RuntimeError):
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def stamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def stat_info(path):
    p = Path(path)
    if not p.exists():
        return {'path': str(p), 'exists': False}
    st = p.stat()
    return {'path': str(p), 'exists': True, 'bytes': st.st_size,
            'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='milliseconds')}


def write_bytes_atomic(dst, data):
    """tempário -> fsync -> conferência de bytes -> os.replace. Nunca open(dst, 'w') direto.

    R2: se a troca falhar (alvo somente-leitura, travado, sem permissão), o tempário — criado aqui e que nunca
    virou o arquivo — é removido e a exceção sobe com o nome do alvo; o alvo fica como estava.
    """
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.tmp_' + stamp())
    try:
        with open(tmp, 'xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if tmp.read_bytes() != data:
            raise ImplantacaoError('tempário divergente: %s' % dst)
        os.replace(tmp, dst)
    except BaseException:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        raise
    if sha256_file(dst) != sha256_bytes(data):
        raise ImplantacaoError('conferência final divergente: %s' % dst)


def copy_file_verified(src, dst, chunk=1 << 22):
    """Cópia de bytes por blocos (arquivos grandes), fsync, sha256 da origem == sha256 do destino relido."""
    src, dst = Path(src), Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.part')
    h = hashlib.sha256()
    with open(src, 'rb') as fi, open(tmp, 'wb') as fo:
        for block in iter(lambda: fi.read(chunk), b''):
            h.update(block)
            fo.write(block)
        fo.flush()
        os.fsync(fo.fileno())
    digest = h.hexdigest()
    if sha256_file(tmp) != digest:
        os.replace(tmp, dst.with_name(dst.name + '.mismatch'))
        raise ImplantacaoError('cópia divergente: %s' % dst)
    os.replace(tmp, dst)
    return {'path': str(dst), 'bytes': dst.stat().st_size, 'sha256': digest}


def backup_bytes(target):
    """<arquivo>.bak_<stamp> na mesma pasta, por bytes, conferido. Devolve (caminho, sha256)."""
    target = Path(target)
    bak = target.with_name(target.name + '.bak_' + stamp())
    info = copy_file_verified(target, bak)
    return bak, info['sha256']


def mover_de_lado(path, sufixo):
    """Renomeia <path> -> <path>.<sufixo>_<stamp> (nunca apaga)."""
    path = Path(path)
    dest = path.with_name(path.name + '.' + sufixo + '_' + stamp())
    os.replace(path, dest)
    return dest


def write_json_atomic(path, payload):
    write_bytes_atomic(path, (json.dumps(payload, ensure_ascii=False, indent=1, default=str) + '\n').encode('utf-8'))


def run_python(args, cwd=None, timeout=3600, env=None):
    """Subprocesso Python (o mesmo interpretador), saída capturada; devolve dict com rc/stdout/stderr."""
    e = dict(os.environ)
    e.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    if env:
        e.update(env)
    t0 = time.time()
    proc = subprocess.run([sys.executable, '-X', 'utf8'] + [str(a) for a in args], cwd=cwd, env=e,
                          capture_output=True, timeout=timeout)
    return {'args': [str(a) for a in args], 'returncode': proc.returncode, 'seconds': round(time.time() - t0, 3),
            'stdout': proc.stdout.decode('utf-8', 'replace'), 'stderr': proc.stderr.decode('utf-8', 'replace')[-4000:]}


def run_powershell(script_text, timeout=180):
    """PowerShell 5.1 sem perfil; só usado pelo backend de produção."""
    t0 = time.time()
    proc = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-Command', script_text],
                          capture_output=True, timeout=timeout)
    return {'returncode': proc.returncode, 'seconds': round(time.time() - t0, 3),
            'stdout': proc.stdout.decode('utf-8', 'replace'), 'stderr': proc.stderr.decode('utf-8', 'replace')[-2000:]}


def _ps_quote(text):
    return "'" + str(text).replace("'", "''") + "'"


# =============================================================================== processos
class ProcessosPS:
    """Backend de PRODUÇÃO: Tarefa Agendada + stop/start_iald_web.ps1 + /login. Nunca usado nos ensaios."""

    nome = 'powershell'

    def __init__(self, app_root, tarefa=None, porta=8082):
        self.app_root = Path(app_root)
        self.tarefa = tarefa
        self.porta = int(porta)

    # ---- tarefa agendada
    def tarefa_ler(self):
        if not self.tarefa:
            return {'existe': False, 'nome': None, 'nota': 'nenhuma tarefa configurada'}
        ps = ("$t=Get-ScheduledTask -TaskName %s -ErrorAction SilentlyContinue | Select-Object -First 1;"
              "if(-not $t){'{\"existe\":false}'} else {"
              "@{existe=$true; nome=$t.TaskName; caminho=$t.TaskPath; estado=[string]$t.State;"
              "habilitada=([string]$t.State -ne 'Disabled'); restart_count=$t.Settings.RestartCount;"
              "restart_interval=[string]$t.Settings.RestartInterval; multiplas=[string]$t.Settings.MultipleInstances;"
              "acao=(($t.Actions | ForEach-Object { [string]$_.Execute + ' ' + [string]$_.Arguments }) -join ' | ')"
              "} | ConvertTo-Json -Compress }") % _ps_quote(self.tarefa)
        r = run_powershell(ps)
        if r['returncode'] != 0:
            raise ImplantacaoError('Get-ScheduledTask falhou: %s' % r['stderr'][-500:])
        try:
            data = json.loads(r['stdout'].strip() or '{}')
        except ValueError:
            raise ImplantacaoError('saída ilegível de Get-ScheduledTask: %r' % r['stdout'][-300:])
        data.setdefault('nome', self.tarefa)
        return data

    def _tarefa_cmd(self, cmdlet):
        info = self.tarefa_ler()
        if not info.get('existe'):
            raise ImplantacaoError('tarefa agendada ausente: %s' % self.tarefa)
        r = run_powershell('%s -TaskName %s -TaskPath %s -ErrorAction Stop | Out-Null; "ok"'
                           % (cmdlet, _ps_quote(info['nome']), _ps_quote(info.get('caminho') or '\\')))
        if r['returncode'] != 0 or 'ok' not in r['stdout']:
            raise ImplantacaoError('%s falhou: %s' % (cmdlet, r['stderr'][-500:]))
        return {'cmdlet': cmdlet, 'segundos': r['seconds']}

    def tarefa_desabilitar(self):
        return self._tarefa_cmd('Disable-ScheduledTask')

    def tarefa_habilitar(self):
        return self._tarefa_cmd('Enable-ScheduledTask')

    def tarefa_parar(self):
        return self._tarefa_cmd('Stop-ScheduledTask')

    def tarefa_iniciar(self):
        return self._tarefa_cmd('Start-ScheduledTask')

    # ---- processos
    def listar(self):
        web_pat = 'iald_web_server\\.py'
        ps = (
            "$w=@(Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Where-Object { $_.CommandLine -match '%s' } "
            "| Select-Object ProcessId,ParentProcessId,CreationDate);"
            "$s=@(Get-CimInstance Win32_Process -Filter \"name='powershell.exe'\" | Where-Object { $_.CommandLine -and $_.CommandLine -match 'start_iald_web\\.ps1' } "
            "| Select-Object ProcessId,ParentProcessId,CreationDate);"
            "$l=@(Get-NetTCPConnection -LocalPort %d -State Listen -ErrorAction SilentlyContinue | Select-Object OwningProcess);"
            "@{web=$w;supervisores=$s;listen=$l} | ConvertTo-Json -Depth 4 -Compress"
        ) % (web_pat, self.porta)
        r = run_powershell(ps)
        if r['returncode'] != 0:
            raise ImplantacaoError('listagem de processos falhou: %s' % r['stderr'][-500:])
        try:
            data = json.loads(r['stdout']) if r['stdout'].strip() else {}
        except ValueError:
            raise ImplantacaoError('listagem de processos ilegível: %r' % r['stdout'][-300:])
        for k in ('web', 'supervisores', 'listen'):
            v = data.get(k)
            data[k] = [] if v is None else [v] if isinstance(v, dict) else v
        return data

    def parar_script(self):
        script = self.app_root / 'stop_iald_web.ps1'
        if not script.exists():
            raise ImplantacaoError('stop_iald_web.ps1 não encontrado em %s' % self.app_root)
        r = run_powershell('& %s' % _ps_quote(script), timeout=120)
        return {'rc': r['returncode'], 'stdout': r['stdout'][-1500:], 'stderr': r['stderr'][-800:]}

    def iniciar_desacoplado(self):
        """Sem tarefa: Win32_Process.Create (o processo nasce no serviço WMI, fora do job object do chamador)."""
        script = self.app_root / 'start_iald_web.ps1'
        if not script.exists():
            raise ImplantacaoError('start_iald_web.ps1 não encontrado em %s' % self.app_root)
        cmd = 'powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "%s"' % script
        ps = ("$r=Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=%s; CurrentDirectory=%s};"
              "@{rv=[int]$r.ReturnValue; pid=[int]$r.ProcessId} | ConvertTo-Json -Compress") % (_ps_quote(cmd), _ps_quote(self.app_root))
        r = run_powershell(ps, timeout=60)
        try:
            data = json.loads(r['stdout'].strip())
        except ValueError:
            raise ImplantacaoError('Win32_Process.Create ilegível: %r %r' % (r['stdout'][-300:], r['stderr'][-300:]))
        if data.get('rv') != 0:
            raise ImplantacaoError('Win32_Process.Create devolveu %r' % data.get('rv'))
        return data

    def saude(self):
        try:
            import urllib.request
            with urllib.request.urlopen('http://127.0.0.1:%d/login' % self.porta, timeout=3) as resp:
                return resp.status == 200, resp.status
        except Exception as exc:  # noqa: BLE001 - registrado; quem chama tenta de novo
            return False, repr(exc)[:200]


def _pid_vivo(pid):
    """Windows: OpenProcess + GetExitCodeProcess (STILL_ACTIVE = 259). Nunca os.kill(pid, 0) (no Windows ele MATA)."""
    if os.name != 'nt':
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, int(pid))   # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    try:
        code = ctypes.c_ulong()
        if not k.GetExitCodeProcess(h, ctypes.byref(code)):
            return False
        return code.value == 259
    finally:
        k.CloseHandle(h)


class ProcessosSim:
    """Backend do ENSAIO (R2, achado 3): modela a Tarefa Agendada (gatilho, RestartCount/RestartInterval,
    MultipleInstances IgnoreNew, Disabled), o supervisor com trava de instância única e o filho web, com processos
    Python REAIS sob a guarda (sem rede: a saúde é um arquivo, não a porta). Os programas estão em
    ensaio_implantacao_r2/sim/. Tudo fica em `sim_dir` (dentro de 4_INTEGRACAO)."""

    nome = 'simulado'

    def __init__(self, sim_dir):
        self.dir = Path(sim_dir)
        self.cmd_dir = self.dir / 'comandos'
        self.pids = self.dir / 'pids'
        self.scripts = Path(json.loads((self.dir / 'tarefa.json').read_text(encoding='utf-8'))['scripts'])

    def _tarefa(self):
        return json.loads((self.dir / 'tarefa.json').read_text(encoding='utf-8'))

    def _escrever_tarefa(self, data):
        # o agendador/supervisor/web simulados leem tarefa.json o tempo todo; no Windows a troca falha enquanto um
        # leitor o tem aberto: novas tentativas curtas (só no simulador)
        for tentativa in range(100):
            try:
                write_json_atomic(self.dir / 'tarefa.json', data)
                return
            except PermissionError:
                if tentativa == 99:
                    raise
                time.sleep(0.02)

    def _estado_agendador(self):
        p = self.dir / 'estado_agendador.json'
        for _ in range(20):
            try:
                return json.loads(p.read_text(encoding='utf-8'))
            except (OSError, ValueError):
                time.sleep(0.05)
        return {}

    def tarefa_ler(self):
        t = self._tarefa()
        est = self._estado_agendador()
        inst = est.get('instancia_pid')
        vivo = bool(inst) and _pid_vivo(inst)
        estado = 'Disabled' if not t['enabled'] else ('Running' if vivo else 'Ready')
        return {'existe': True, 'nome': t['nome'], 'caminho': '\\', 'estado': estado, 'habilitada': bool(t['enabled']),
                'restart_count': t['restart_count'], 'restart_interval': 'PT%gS' % t['restart_interval_s'],
                'multiplas': 'IgnoreNew', 'simulada': True}

    def _comando(self, op, esperar_s=15):
        self.cmd_dir.mkdir(parents=True, exist_ok=True)
        cid = '%s_%s' % (stamp(), op)
        write_json_atomic(self.cmd_dir / (cid + '.json'), {'op': op, 'id': cid})
        ack = self.cmd_dir / (cid + '.ack')
        t0 = time.time()
        while time.time() - t0 < esperar_s:
            if ack.exists():
                return json.loads(ack.read_text(encoding='utf-8'))
            time.sleep(0.05)
        raise ImplantacaoError('agendador simulado não respondeu ao comando %s' % op)

    def tarefa_desabilitar(self):
        t = self._tarefa()
        t['enabled'] = False
        self._escrever_tarefa(t)
        return {'cmdlet': 'Disable-ScheduledTask (simulado)'}

    def tarefa_habilitar(self):
        t = self._tarefa()
        t['enabled'] = True
        self._escrever_tarefa(t)
        return {'cmdlet': 'Enable-ScheduledTask (simulado)'}

    def tarefa_parar(self):
        return dict(self._comando('stop'), cmdlet='Stop-ScheduledTask (simulado)')

    def tarefa_iniciar(self):
        ack = self._comando('start')
        if ack.get('resultado') == 'recusado_desabilitada':
            raise ImplantacaoError('Start-ScheduledTask recusado: tarefa desabilitada (simulado)')
        return dict(ack, cmdlet='Start-ScheduledTask (simulado)')

    def _vivos(self, prefixo):
        out = []
        for p in sorted(self.pids.glob(prefixo + '_*.json')):
            try:
                d = json.loads(p.read_text(encoding='utf-8'))
            except (OSError, ValueError):
                continue
            if _pid_vivo(d['pid']):
                out.append(d)
        return out

    def listar(self):
        web = self._vivos('web')
        return {'web': web, 'supervisores': self._vivos('sup'), 'listen': [{'OwningProcess': w['pid']} for w in web]}

    def parar_script(self):
        """Mesma ordem do stop_iald_web.ps1: supervisores primeiro, depois o filho, depois órfãos."""
        mortos = []
        for s in self._vivos('sup'):
            os.kill(s['pid'], signal.SIGTERM)          # Windows: TerminateProcess (como Stop-Process -Force)
            mortos.append(('sup', s['pid']))
        time.sleep(0.8)
        for w in self._vivos('web'):
            os.kill(w['pid'], signal.SIGTERM)
            mortos.append(('web', w['pid']))
        time.sleep(0.3)
        return {'rc': 0, 'mortos': mortos}

    def iniciar_desacoplado(self):
        flags = getattr(subprocess, 'DETACHED_PROCESS', 0) | getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)
        p = subprocess.Popen([sys.executable, '-X', 'utf8', str(self.scripts / 'sim_supervisor.py'), str(self.dir), 'desacoplado'],
                             creationflags=flags, stdout=open(self.dir / 'saida_desacoplado.log', 'ab'), stderr=subprocess.STDOUT)
        return {'pid': p.pid}

    def saude(self):
        for w in self._vivos('web'):
            if (self.pids / ('saude_%d' % w['pid'])).exists():
                return True, 200
        return False, 'sem filho web saudável'


def backend_de(cfg):
    if not cfg.get('gerir_processos'):
        return None
    kind = cfg.get('processos_backend', 'powershell')
    if kind == 'powershell':
        return ProcessosPS(cfg['app_root_processos'], cfg.get('tarefa_agendada'), cfg.get('porta', 8082))
    if kind == 'simulado':
        return ProcessosSim(cfg['sim_dir'])
    raise ImplantacaoError('processos_backend desconhecido: %r' % kind)


def _vazio(procs):
    return not procs['web'] and not procs['supervisores'] and not procs['listen']


def assegurar_parado(backend, onde):
    """Fail-closed: antes de um passo que muda banco ou arquivos, nenhum processo do app pode estar vivo."""
    procs = backend.listar()
    if not _vazio(procs):
        raise ImplantacaoError('app vivo antes de %s (relançado durante a janela?): %s' % (onde, json.dumps(procs, default=str)[:600]))
    return {'onde': onde, 'em': now_iso(), 'vazio': True}


def parar_app_gerido(backend, reg, salvar, esperar_s=60, quieto_s=5.0):
    """1) lê a tarefa e REGISTRA o estado antes; 2) DESABILITA a tarefa (sem relançamento por RestartCount nem por
    gatilho de logon) e confere; 3) Stop-ScheduledTask se a instância corre; 4) stop script; 5) espera tudo morrer;
    6) silêncio: depois de `quieto_s` segundos, nada pode ter renascido. Cada mudança é gravada no recibo na hora."""
    tarefa = backend.tarefa_ler()
    reg['tarefa_antes'] = tarefa
    reg['processos_antes'] = backend.listar()
    salvar()
    if tarefa.get('existe') and tarefa.get('habilitada'):
        reg['tarefa_desabilitar'] = backend.tarefa_desabilitar()
        reg['tarefa_desabilitada_por_esta_execucao'] = True
        salvar()
        depois = backend.tarefa_ler()
        reg['tarefa_depois_de_desabilitar'] = depois
        if depois.get('habilitada'):
            raise ImplantacaoError('a tarefa agendada continua habilitada depois de Disable-ScheduledTask')
    if tarefa.get('existe') and tarefa.get('estado') == 'Running':
        try:
            reg['tarefa_parar'] = backend.tarefa_parar()
        except Exception as exc:  # noqa: BLE001 - o stop script abaixo para o app de qualquer modo; registrado
            reg['tarefa_parar'] = {'erro': repr(exc)[:500], 'nota': 'seguimos com o stop script'}
        salvar()
    if not _vazio(backend.listar()):
        reg['stop_script'] = backend.parar_script()
        salvar()
    t0 = time.time()
    while True:
        procs = backend.listar()
        if _vazio(procs):
            break
        if time.time() - t0 > esperar_s:
            raise ImplantacaoError('o app não parou dentro do prazo: %s' % json.dumps(procs, default=str)[:600])
        time.sleep(1.0)
    reg['parado_em_s'] = round(time.time() - t0, 2)
    time.sleep(quieto_s)
    reg['silencio'] = assegurar_parado(backend, 'fim do parar_app (silêncio de %gs)' % quieto_s)
    reg['parado'] = True
    salvar()
    return reg


def iniciar_app_gerido(backend, tarefa_antes, reg, salvar, esperar_s=120):
    """Volta ao estado de antes: se a tarefa existia HABILITADA, reabilita e inicia PELA tarefa (o processo nasce no
    Agendador). Se existia desabilitada pelo operador, continua desabilitada e o app sobe desacoplado (WMI). Espera a
    saúde e exige exatamente 1 supervisor e 1 filho web."""
    tarefa_antes = tarefa_antes or {}
    agora = backend.tarefa_ler()
    reg['tarefa_agora'] = agora
    if agora.get('existe') and tarefa_antes.get('habilitada'):
        if not agora.get('habilitada'):
            reg['tarefa_habilitar'] = backend.tarefa_habilitar()
            salvar()
        reg['iniciado_por'] = 'tarefa_agendada'
        try:
            reg['tarefa_iniciar'] = backend.tarefa_iniciar()
        except ImplantacaoError as exc:   # uma nova tentativa (a habilitação recém-feita pode não ter sido vista)
            reg['tarefa_iniciar_1a_tentativa'] = repr(exc)[:300]
            salvar()
            time.sleep(2.0)
            reg['tarefa_iniciar'] = backend.tarefa_iniciar()
    else:
        reg['iniciado_por'] = 'desacoplado'
        reg['iniciar_desacoplado'] = backend.iniciar_desacoplado()
    salvar()
    t0 = time.time()
    ultimo = None
    while time.time() - t0 < esperar_s:
        procs = backend.listar()
        ok, status = backend.saude()
        ultimo = {'procs': procs, 'saude': status}
        if ok and len(procs['supervisores']) == 1 and len(procs['web']) == 1:
            reg.update({'saude': status, 'depois': procs, 'ok': True, 'segundos': round(time.time() - t0, 1),
                        'tarefa_depois': backend.tarefa_ler()})
            salvar()
            return reg
        time.sleep(1.0)
    reg.update({'ok': False, 'ultimo': ultimo})
    salvar()
    raise ImplantacaoError('o app não ficou saudável (1 supervisor + 1 web + saúde) em %ds' % esperar_s)


def restaurar_tarefa(backend, tarefa_antes, reg, salvar):
    """Só a TAREFA: reabilita se estava habilitada antes (usado quando nada mudou e o reinício falha)."""
    if tarefa_antes and tarefa_antes.get('existe') and tarefa_antes.get('habilitada'):
        if not backend.tarefa_ler().get('habilitada'):
            reg['tarefa_reabilitada'] = backend.tarefa_habilitar()
            salvar()


# ================================================================================ banco
def sqlite_schema_version(db_path):
    conn = sqlite3.connect('file:%s?mode=ro' % Path(db_path).as_posix(), uri=True, timeout=30)
    try:
        row = conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        contexts = conn.execute('SELECT count(*) FROM contexts').fetchone()[0] if 'contexts' in tables else None
        events = conn.execute('SELECT count(*) FROM events').fetchone()[0] if 'events' in tables else None
        jm = conn.execute('PRAGMA journal_mode').fetchone()[0]
        return {'schema_version': row[0] if row else None, 'tables': tables, 'contexts': contexts, 'events': events,
                'journal_mode': jm}
    finally:
        conn.close()


def sqlite_writer_probe(db_path, timeout_s=30):
    """BEGIN IMMEDIATE e ROLLBACK: prova que ninguém segura escrita no banco (fail-closed se ocupado)."""
    conn = sqlite3.connect(str(db_path), timeout=timeout_s, isolation_level=None)
    try:
        conn.execute('PRAGMA busy_timeout=%d' % (timeout_s * 1000))
        conn.execute('BEGIN IMMEDIATE')
        conn.execute('ROLLBACK')
        return True
    finally:
        conn.close()


def disk_free(path):
    p = Path(path)
    while not p.exists() and p.parent != p:
        p = p.parent
    if not p.exists():
        return None
    return shutil.disk_usage(str(p)).free


def mapear(caminho_producao, raizes):
    """Traduz um caminho de produção para o alvo real pelo mapa de raízes (produção = identidade)."""
    norm = str(caminho_producao)
    for prod_root, real_root in sorted(raizes.items(), key=lambda kv: -len(kv[0])):
        if norm.lower().startswith(prod_root.lower().rstrip('\\') + '\\') or norm.lower() == prod_root.lower():
            rest = norm[len(prod_root.rstrip('\\')):].lstrip('\\')
            return Path(real_root) / rest if rest else Path(real_root)
    raise ImplantacaoError('caminho fora das raízes mapeadas: %s' % norm)


# --- K3 (revisor R2): ambiente em que o stop script nao derruba o app (so o simulador muda)
def _parar_script_sem_efeito(self):
    return {"rc": 1, "nota": "K3: stop script sem efeito (simulado)"}
ProcessosSim.parar_script = _parar_script_sem_efeito
