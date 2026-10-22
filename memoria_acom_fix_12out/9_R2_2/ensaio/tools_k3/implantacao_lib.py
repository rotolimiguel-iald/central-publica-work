# -*- coding: utf-8 -*-
"""Biblioteca comum de implantar.py / reverter.py (conserto ACOM 12/10; R2 e R2.1 de 13/10). Só stdlib.

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

R2.1 (revisão independente R2 de 13/10, achados K2, K3, K4, K6 e passo 8):
  * K6 — toda troca (os.replace) e remoção de tempário tem nova tentativa curta e LIMITADA em PermissionError
    (WinError 5/32: um leitor — antivírus, indexador, um operador abrindo o recibo — segura o arquivo sem
    FILE_SHARE_DELETE). Os recibos esperam até 30 s; os demais arquivos até 10 s. Depois, a falha sobe como antes.
  * K2 — recibos com carimbo (nunca sobrescritos) e `recibos_pendentes`: a implantação real anterior que mudou algo
    e não tem RECIBO_REVERSAO REVERTIDA correspondente bloqueia uma nova implantação (e indica o recibo a reverter).
  * passo 8 — `ReinicioPendente`: o comando de início foi aceito e há processo do app vivo, mas a saúde não chegou no
    prazo. Não é falha da implantação; o recibo diz «aguardando reinício» e manda conferir, não reverter.
  * `estado_real` — o recibo descreve a tarefa e os processos LIDOS, nunca presumidos.

R2.2 (revisão independente R2.1 de 13/10, achados K4c, K4b, K3r e P8b):
  * K4c — `reversao_limpa`: a trava do implantar só aceita como revertida uma reversão REAL sem falhas e com
    status REVERTIDA* coerente (REVERTIDA exige app religado; REVERTIDA_SEM_RELIGAR é a escolha explícita do
    --sem-reiniciar, com a ação manual registrada). Um recibo de reversão REVERTIDA com `app_religado: false` (o
    status enganoso da R2.1) NÃO libera a trava.
  * P8b — `iniciar_app_gerido` observa os pids do app durante a espera (cada amostra: pids do filho web e do
    supervisor) e, quando a saúde não chega no prazo, classifica: LENTO_PROVAVEL (um só filho web, o mesmo pid
    em todas as amostras desde que apareceu) ou LACO_DE_QUEDA_PROVAVEL (o pid do filho web trocou, ou o filho
    sumiu e voltou, ou nunca ficou de pé com o supervisor vivo). A saída continua 3 por desenho; o recibo e a
    saída dizem como o operador distingue os dois casos e o que fazer.
  * `descrever_estado` — o estado LIDO em uma frase (tarefa, supervisores, filhos web, porta), para as ações.
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


class ReinicioPendente(ImplantacaoError):
    """R2.1 (passo 8): o início foi aceito e há processo do app vivo, mas a saúde não chegou no prazo."""


RETRY_ARQUIVO_S = 10.0     # R2.1: espera máxima de uma troca de arquivo de código/backup
RETRY_RECIBO_S = 30.0      # R2.1: espera máxima de uma troca de recibo (um leitor pode segurá-lo por segundos)


def com_nova_tentativa(fn, *args, limite_s=RETRY_ARQUIVO_S, registro=None):
    """R2.1 (K6): chama fn(*args); em PermissionError (WinError 5 acesso negado / 32 violação de compartilhamento)
    espera 20 ms, dobrando até 500 ms, por no máximo `limite_s` segundos; depois a exceção sobe (falha visível).
    `registro` (lista), se dado, recebe uma linha por nova tentativa."""
    t0 = time.monotonic()
    espera = 0.02
    while True:
        try:
            return fn(*args)
        except PermissionError as exc:
            if time.monotonic() - t0 >= limite_s:
                raise
            if registro is not None and len(registro) < 50:
                registro.append({'op': getattr(fn, '__name__', str(fn)), 'erro': repr(exc)[:160],
                                 'apos_s': round(time.monotonic() - t0, 3)})
            time.sleep(espera)
            espera = min(espera * 2, 0.5)


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


def write_bytes_atomic(dst, data, limite_s=RETRY_ARQUIVO_S):
    """tempário -> fsync -> conferência de bytes -> os.replace. Nunca open(dst, 'w') direto.

    R2: se a troca falhar (alvo somente-leitura, travado, sem permissão), o tempário — criado aqui e que nunca
    virou o arquivo — é removido e a exceção sobe com o nome do alvo; o alvo fica como estava.
    R2.1 (K6): a troca e a remoção do tempário têm nova tentativa curta e limitada em PermissionError.
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
        com_nova_tentativa(os.replace, tmp, dst, limite_s=limite_s)
    except BaseException:
        try:
            if tmp.exists():
                com_nova_tentativa(os.remove, tmp, limite_s=min(limite_s, 5.0))
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
        com_nova_tentativa(os.replace, tmp, dst.with_name(dst.name + '.mismatch'))
        raise ImplantacaoError('cópia divergente: %s' % dst)
    com_nova_tentativa(os.replace, tmp, dst)          # R2.1 (K6)
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
    com_nova_tentativa(os.replace, path, dest)        # R2.1 (K6)
    return dest


def write_json_atomic(path, payload, limite_s=RETRY_RECIBO_S):
    """Recibos e comandos: R2.1 (K6) — um leitor que segura o recibo por segundos não aborta mais a ferramenta."""
    write_bytes_atomic(path, (json.dumps(payload, ensure_ascii=False, indent=1, default=str) + '\n').encode('utf-8'),
                       limite_s=limite_s)


def ler_json_com_nova_tentativa(path, limite_s=RETRY_RECIBO_S):
    return com_nova_tentativa(lambda: json.loads(Path(path).read_text(encoding='utf-8')), limite_s=limite_s)


# ============================================================================ R2.1: recibos pendentes (K2)
STATUS_REVERTIDO = ('REVERTIDA', 'REVERTIDA_AGUARDANDO_REINICIO', 'REVERTIDA_SEM_RELIGAR')


def reversao_limpa(r):
    """R2.2 (K4c): um RECIBO_REVERSAO prova a reversão SÓ se for real (não dry-run), com status REVERTIDA*, sem
    falhas registradas, e — no status REVERTIDA — com o app religado (ou processos não geridos: `app_religado`
    None). A R2.1 podia gravar REVERTIDA com `app_religado: false` e um alvo fora do original: isso não libera."""
    if r.get('dry_run') or r.get('status') not in STATUS_REVERTIDO:
        return False
    if r.get('falhas'):
        return False
    if r.get('status') == 'REVERTIDA' and r.get('app_religado') is False:
        return False
    conf = r.get('conferencia_final')
    if isinstance(conf, dict) and conf.get('divergentes'):
        return False
    return True


def _impl_precisa_reverter(rec):
    """Uma implantação REAL precisa de reversão salvo se nada mudou: recusada, ou falhou sem mudança iniciada.
    EM_CURSO (morta no meio) e CONCLUIDA* precisam (estado desconhecido ou implantado)."""
    st = str(rec.get('status') or '')
    if st.startswith('RECUSADA'):
        return False
    if st.startswith('FALHOU_EM_') and not rec.get('mudancas_iniciadas'):
        return False
    return True


def recibos_pendentes(dirs, excluir=()):
    """R2.1 (K2): lista as implantações REAIS (não dry-run) que mudaram algo (ou cujo estado é desconhecido) e não
    têm RECIBO_REVERSAO real com status REVERTIDA* que as cite (por carimbo ou caminho). Recibo ilegível conta como
    pendente (fail-closed). Lê só JSON de recibo; nunca escreve."""
    impls, revertidos_stamp, revertidos_path, ilegiveis = [], set(), set(), []
    fora = {os.path.normcase(os.path.abspath(x)) for x in excluir}
    for d in dirs:
        d = Path(d)
        if not d.is_dir():
            continue
        for p in sorted(d.glob('RECIBO_REVERSAO*.json')):
            try:
                r = ler_json_com_nova_tentativa(p, limite_s=5.0)
            except (OSError, ValueError):
                continue                      # uma reversão ilegível não prova reversão
            if not reversao_limpa(r):         # R2.2 (K4c): só uma reversão LIMPA libera a trava
                continue
            if r.get('recibo_implantacao_stamp'):
                revertidos_stamp.add(r['recibo_implantacao_stamp'])
            if r.get('recibo_implantacao'):
                revertidos_path.add(os.path.normcase(os.path.abspath(r['recibo_implantacao'])))
        for p in sorted(d.glob('RECIBO_IMPLANTACAO*.json')):
            if os.path.normcase(os.path.abspath(p)) in fora:
                continue                      # o recibo da própria execução
            try:
                rec = ler_json_com_nova_tentativa(p, limite_s=5.0)
            except (OSError, ValueError) as exc:
                ilegiveis.append({'recibo': str(p), 'erro': repr(exc)[:200]})
                continue
            if rec.get('dry_run') or not _impl_precisa_reverter(rec):
                continue
            if rec.get('stamp') in revertidos_stamp or os.path.normcase(os.path.abspath(p)) in revertidos_path:
                continue
            impls.append({'recibo': str(p), 'stamp': rec.get('stamp'), 'status': rec.get('status'),
                          'mudancas_iniciadas': rec.get('mudancas_iniciadas'), 'iniciado_em': rec.get('iniciado_em')})
    return {'pendentes': impls, 'ilegiveis': ilegiveis}


def estado_real(backend):
    """R2.1: a tarefa e os processos LIDOS agora (o recibo nunca presume o estado). Erros de leitura são registrados."""
    if backend is None:
        return {'gerido': False}
    out = {'lido_em': now_iso()}
    try:
        t = backend.tarefa_ler()
        out['tarefa'] = {k: t.get(k) for k in ('existe', 'nome', 'estado', 'habilitada')}
    except Exception as exc:  # noqa: BLE001 - registrado
        out['tarefa_erro'] = repr(exc)[:300]
    try:
        p = backend.listar()
        out['processos'] = {'supervisores': len(p['supervisores']), 'web': len(p['web']), 'escutando': len(p['listen'])}
    except Exception as exc:  # noqa: BLE001
        out['processos_erro'] = repr(exc)[:300]
    return out


def descrever_estado(er):
    """R2.2: o estado LIDO (saída de estado_real) em uma frase, para as ações do recibo. Nunca presume."""
    if not er or er.get('gerido') is False:
        return 'processos não geridos por esta ferramenta (nada lido)'
    partes = []
    t = er.get('tarefa')
    if t:
        partes.append('tarefa agendada %s (%s)' % ('HABILITADA' if t.get('habilitada') else 'DESABILITADA', t.get('estado')))
    elif er.get('tarefa_erro'):
        partes.append('tarefa agendada ILEGÍVEL (%s)' % er['tarefa_erro'][:120])
    p = er.get('processos')
    if p:
        partes.append('%d supervisor(es), %d filho(s) web, %d processo(s) escutando a porta'
                      % (p.get('supervisores', 0), p.get('web', 0), p.get('escutando', 0)))
        if p.get('web') and not p.get('supervisores'):
            partes.append('o app está VIVO SEM SUPERVISOR (ninguém o relança se cair)')
        elif not p.get('web') and not p.get('supervisores'):
            partes.append('o app está PARADO')
    elif er.get('processos_erro'):
        partes.append('processos ILEGÍVEIS (%s)' % er['processos_erro'][:120])
    return '; '.join(partes) + ' (lido em %s)' % er.get('lido_em')


def _pid_de(d):
    """pid de um item de listar(): 'pid' no simulador, 'ProcessId' no backend PowerShell."""
    if not isinstance(d, dict):
        return None
    return d.get('pid') if d.get('pid') is not None else d.get('ProcessId')


def diagnostico_reinicio(amostras, esperar_s):
    """R2.2 (P8b): classifica uma espera de saúde que não fechou, a partir das amostras de pids LIDAS.
    LENTO_PROVAVEL: um só filho web, o mesmo pid em todas as amostras desde que apareceu (e na última).
    LACO_DE_QUEDA_PROVAVEL: o pid do filho web trocou, ou o filho sumiu depois de aparecer, ou nunca apareceu
    com o supervisor vivo em todas as amostras. INDETERMINADO: amostras insuficientes."""
    webs = []
    sumiu_depois = False
    visto = False
    for a in amostras:
        w = a.get('web') or []
        if w:
            visto = True
        elif visto:
            sumiu_depois = True
        for pid in w:
            if pid not in webs:
                webs.append(pid)
    sups = []
    for a in amostras:
        for pid in a.get('sup') or []:
            if pid not in sups:
                sups.append(pid)
    ultimo = amostras[-1] if amostras else {}
    if len(amostras) < 2:
        leitura = 'INDETERMINADO'
    elif len(webs) == 1 and not sumiu_depois and (ultimo.get('web') or []) == webs:
        leitura = 'LENTO_PROVAVEL'
    elif len(webs) > 1 or sumiu_depois or (not webs and sups):
        leitura = 'LACO_DE_QUEDA_PROVAVEL'
    else:
        leitura = 'INDETERMINADO'
    return {'leitura': leitura, 'janela_s': esperar_s, 'amostras': len(amostras),
            'pids_web_distintos': len(webs), 'reinicios_do_filho_web_na_janela': max(len(webs) - 1, 0),
            'filho_web_sumiu_depois_de_aparecer': sumiu_depois, 'pids_supervisor_distintos': len(sups),
            'amostras_sem_filho_web': sum(1 for a in amostras if not a.get('web'))}


def texto_reinicio_pendente(diag, tarefa, porta, acao_se_laco):
    """R2.2 (P8b): a ação para a saída 3 — como distinguir app lento de laço de queda, e o que fazer.
    `acao_se_laco`: a frase do que fazer quando o laço de queda se confirma (no implantar, o comando de reversão)."""
    como = ('COMO DISTINGUIR: rode duas vezes, com 1 minuto entre elas, '
            'Get-CimInstance Win32_Process -Filter "name=\'python.exe\'" | Where-Object { $_.CommandLine -match '
            '\'iald_web_server\\.py\' } | Select-Object ProcessId,CreationDate ; e confira http://127.0.0.1:%s/login. '
            'APP LENTO (saudável atrasado): o MESMO ProcessId nas duas leituras, CreationDate antiga, e /login passa a '
            'responder 200: esperar e conferir de novo. LAÇO DE QUEDA: o ProcessId muda entre as leituras (ou some e '
            'volta), CreationDate sempre recente, /login nunca 200: o código novo não sobe.' % porta)
    if diag.get('leitura') == 'LACO_DE_QUEDA_PROVAVEL' and not diag.get('pids_web_distintos'):
        lido = ('LIDO NA JANELA: o supervisor ficou vivo em %d amostras em %ss e NENHUM filho web ficou de pé em nenhuma '
                'delas (o filho morre ao nascer): LAÇO DE QUEDA PROVÁVEL.' % (diag['amostras'], diag['janela_s']))
        fazer = 'O QUE FAZER: confirme com o COMO DISTINGUIR; confirmado o laço, NÃO espere: %s' % acao_se_laco
    elif diag.get('leitura') == 'LACO_DE_QUEDA_PROVAVEL':
        lido = ('LIDO NA JANELA: o filho web reiniciou %d vez(es) em %ss (%d pids distintos; sumiu depois de aparecer: %s): '
                'LAÇO DE QUEDA PROVÁVEL.' % (diag['reinicios_do_filho_web_na_janela'], diag['janela_s'],
                                              diag['pids_web_distintos'], 'sim' if diag['filho_web_sumiu_depois_de_aparecer'] else 'não'))
        fazer = 'O QUE FAZER: confirme com o COMO DISTINGUIR; confirmado o laço, NÃO espere: %s' % acao_se_laco
    elif diag.get('leitura') == 'LENTO_PROVAVEL':
        lido = ('LIDO NA JANELA: um só filho web, o mesmo pid em %d amostras em %ss: APP LENTO PROVÁVEL (saudável atrasado).'
                % (diag['amostras'], diag['janela_s']))
        # o caso lento NÃO traz o comando de reversão (invariante do passo 8 desde a R2.1: não mandar reverter)
        fazer = ('O QUE FAZER: NÃO reverter; confira em alguns minutos com o COMO DISTINGUIR. Só se em 10 minutos /login '
                 'ainda não responder 200 e o ProcessId estiver mudando, trate como laço de queda (RUNBOOK_OPERADOR, '
                 'seção da saída 3).')
    else:
        lido = 'LIDO NA JANELA: amostras insuficientes para distinguir (%s).' % json.dumps(diag, ensure_ascii=False)
        fazer = 'O QUE FAZER: não reverter às cegas; aplique o COMO DISTINGUIR. Laço de queda confirmado: %s' % acao_se_laco
    return ' '.join([lido, como, fazer, 'Tarefa: Get-ScheduledTask -TaskName \'%s\'.' % tarefa])


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


def _pid_criado_em(pid):
    """Hora de criação (epoch) do processo `pid`, ou None (Windows: GetProcessTimes)."""
    if os.name != 'nt':
        return None
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, int(pid))
    if not h:
        return None
    try:
        tempos = [ctypes.c_ulonglong() for _ in range(4)]
        if not k.GetProcessTimes(h, *[ctypes.byref(t) for t in tempos]):
            return None
        return tempos[0].value / 1e7 - 11644473600.0      # FILETIME (100 ns desde 1601) -> epoch
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
                # R2.1: pid reaproveitado pelo Windows não é o processo simulado (hora de criação diferente)
                criado = _pid_criado_em(d['pid'])
                if criado is not None and d.get('t') is not None and abs(criado - float(d['t'])) > 5.0:
                    continue
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
    amostras = []                  # R2.2 (P8b): os pids LIDOS em cada amostra da espera
    while time.time() - t0 < esperar_s:
        procs = backend.listar()
        ok, status = backend.saude()
        ultimo = {'procs': procs, 'saude': status}
        if len(amostras) < 600:
            amostras.append({'s': round(time.time() - t0, 1), 'web': [_pid_de(w) for w in procs['web']],
                             'sup': [_pid_de(s) for s in procs['supervisores']]})
        if ok and len(procs['supervisores']) == 1 and len(procs['web']) == 1:
            reg.update({'saude': status, 'depois': procs, 'ok': True, 'segundos': round(time.time() - t0, 1),
                        'tarefa_depois': backend.tarefa_ler()})
            salvar()
            return reg
        time.sleep(1.0)
    reg.update({'ok': False, 'ultimo': ultimo})
    salvar()
    # R2.1 (passo 8): o comando de início FOI aceito (senão teria levantado acima). Se há processo do app vivo,
    # é um reinício lento, não uma falha da implantação: quem chama decide (nunca mandar reverter por isso).
    vivos = bool(ultimo) and (ultimo['procs']['supervisores'] or ultimo['procs']['web'])
    reg['amostras_de_pids'] = amostras[-60:]
    reg['diagnostico_reinicio'] = diagnostico_reinicio(amostras, esperar_s)
    if vivos:
        reg['aguardando_reinicio'] = True
        salvar()
        exc = ReinicioPendente('o início foi aceito e há processo do app vivo, mas a saúde (1 supervisor + 1 web + '
                               '/login) não chegou em %ds; leitura das amostras: %s'
                               % (esperar_s, reg['diagnostico_reinicio']['leitura']))
        exc.diagnostico = reg['diagnostico_reinicio']
        raise exc
    raise ImplantacaoError('o app não ficou saudável (1 supervisor + 1 web + saúde) em %ds' % esperar_s)


def restaurar_tarefa(backend, desabilitada_por_esta_execucao, reg, salvar):
    """Só a TAREFA. R2.1 (K3): reabilita SE E SÓ SE foi esta execução que a desabilitou (registrado no recibo como
    `tarefa_desabilitada_por_esta_execucao`); uma tarefa que o operador desabilitou nunca é reabilitada aqui.
    Devolve True se a tarefa ficou habilitada por esta chamada (ou já estava), False se nada foi feito."""
    if not desabilitada_por_esta_execucao:
        reg['tarefa_reabilitada'] = {'nota': 'não reabilitada: esta execução não a desabilitou'}
        salvar()
        return False
    if backend.tarefa_ler().get('habilitada'):
        reg['tarefa_reabilitada'] = {'nota': 'já estava habilitada'}
        salvar()
        return True
    reg['tarefa_reabilitada'] = backend.tarefa_habilitar()
    salvar()
    depois = backend.tarefa_ler()
    reg['tarefa_depois_de_reabilitar'] = {k: depois.get(k) for k in ('estado', 'habilitada')}
    salvar()
    if not depois.get('habilitada'):
        raise ImplantacaoError('Enable-ScheduledTask não deixou a tarefa habilitada')
    return True


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


# --- K3 (ensaio): ambiente em que o stop script nao derruba o app (so o simulador muda)
def _parar_script_sem_efeito(self):
    return {"rc": 1, "nota": "K3: stop script sem efeito (simulado)"}
ProcessosSim.parar_script = _parar_script_sem_efeito
