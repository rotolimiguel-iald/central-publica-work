# -*- coding: utf-8 -*-
# ESPERA o fim do rito v386 SO POR LEITURA: nao roda nada do rito, nao mata processo, nao escreve nada (molde: espera_rito_v385.py).
# O rito v386 e' lancado pelo rito_v386.sh, que grava no fim RITO_RC=<rc> no stdout canonico (rodada_v386_stdout.txt), a 2a linha (o fim) em
# rito_horarios_v386.txt, e so DEPOIS restaura o servidor do modelo nativo e apaga o .rito_v386.pid (o trap do EXIT).
# A VIDA DO LANCADOR: lida como o PROPRIO lancador a le (rito_v386.sh, guarda da recusa 16): o PID do .rito_v386.pid (um PID do Git Bash) vive (kill -0) E
# /proc/<pid>/cmdline contem rito_v386 -- num sh do Git Bash, so leitura. Estados: AUSENTE (sem .pid), VIVO, MORTO (o .pid e' VELHO), '?' (ilegivel: conta como VIVO).
# Fim = (a) a linha RITO_RC=<rc> no stdout E (b) nenhum processo "python ... um.py" vivo (Get-CimInstance, so leitura; vigia fail-closed) E (c) o stdout parado
# por 2 leituras seguidas E (d) a 2a linha do horario OU o lancador fora (AUSENTE/MORTO). Depois, ate V386_ESPERA_RESTAURO_MAX_S (900 s), espera o lancador
# terminar a restauracao, para o log do lancador estar completo quando o conferidor o copiar; se nao terminar, AVISO visivel e segue.
# rc: 0 = terminou, RITO_RC=0 e a linha final do rito; 3 = acabou SEM a linha final ou com RITO_RC != 0 (rito nao limpo, inclusive SINAL_*);
# 4 = tempo esgotado (V386_ESPERA_MAX_S, padrao 7 h) -- «o rito ainda nao acabou»: nada foi feito; 5 = sem RITO_RC no stdout, nenhum um.py vivo e o
# lancador FORA (AUSENTE ou MORTO) -- nada foi feito.
# ENSAIO (so com o Nos SINTETICO): V386_ESPERA_SEM_VIGIA=1 desliga a vigia de processos (o rito real pode estar vivo ao lado); V386_ESPERA_LANCADOR_FINGE=VIVO|MORTO|AUSENTE
# finge o estado do lancador (para ensaiar «o rito ainda roda -> espera -> tempo esgotado -> para limpo»).
import os, sys, time, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
import leitura_v386 as L
AMB = A.ambiente()
NOS = AMB['nos']
STP = os.path.join(NOS, 'rodada_v386_stdout.txt')
PASSO = int(os.environ.get('V386_ESPERA_PASSO_S', '60')); MAX = int(os.environ.get('V386_ESPERA_MAX_S', str(7 * 3600)))
MAX_REST = int(os.environ.get('V386_ESPERA_RESTAURO_MAX_S', '900'))
PS = ("$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
      "Where-Object { $_.CommandLine -ne $null -and $_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'")
SH = shutil.which('sh') or shutil.which('bash') or r'C:\Program Files\Git\usr\bin\sh.exe'
VIDA = 'if kill -0 "$1" 2>/dev/null && grep -q rito_v386 "/proc/$1/cmdline" 2>/dev/null; then echo VIVO; else echo MORTO; fi'


def vivos():
    if AMB['sem_vigia']:
        return []          # SO no ensaio com o Nos SINTETICO: a vigia de processos e' desligada, dito
    try:
        r = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', PS], capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or r.stderr.strip() or 'VIGIA_OK' not in r.stdout:
            print('  [espera] AVISO: o vigia de processos falhou (rc %s; %r) -- sigo esperando' % (r.returncode, r.stderr[:200])); return ['?']
        return [x.strip() for x in r.stdout.split() if x.strip().isdigit()]
    except Exception as e:
        print('  [espera] AVISO: nao consegui ler a lista de processos: %r -- sigo esperando' % e); return ['?']


def lancador():
    """AUSENTE (sem .pid) | VIVO | MORTO (o .pid e' velho) | '?' (ilegivel -- conta como vivo). So leitura, como o proprio lancador confere."""
    if AMB['lancador_finge'] in ('VIVO', 'MORTO', 'AUSENTE'):
        return AMB['lancador_finge']   # ENSAIO: o estado fingido, dito no cabecalho
    pf = AMB['pidf']
    if not os.path.exists(pf):
        return 'AUSENTE'
    try:
        pid = open(pf, encoding='utf-8', errors='replace').read().strip()
    except OSError:
        return '?'
    if not pid.isdigit():
        return '?'
    try:
        r = subprocess.run([SH, '-c', VIDA, 'sh', pid], capture_output=True, text=True, timeout=30)
        o = r.stdout.strip()
        return o if o in ('VIVO', 'MORTO') else '?'
    except Exception:
        return '?'


def estado():
    try:
        t = open(STP, encoding='utf-8', errors='replace').read()
    except OSError:
        return '', -1, None
    ls = [l for l in t.splitlines() if l.strip()]
    rcs = [l.strip()[len('RITO_RC='):] for l in ls if l.strip().startswith('RITO_RC=')]
    nt = [l for l in ls if not L.TRAILER_RE.match(l.strip())]
    return (nt[-1] if nt else ''), os.path.getsize(STP), (rcs[-1] if rcs else None)


def horario_fim():
    try:
        return len(open(AMB['horarios'], encoding='utf-8').read().split()) >= 2
    except OSError:
        return False


print('[espera] Nos: %s%s%s | stdout: %s | horarios: %s | pid do lancador: %s | sh: %s' % (
    NOS, ' (SINTETICO; vigia de processos DESLIGADA)' if AMB['sem_vigia'] else '', (' (lancador FINGIDO: %s)' % AMB['lancador_finge']) if AMB['lancador_finge'] else '',
    STP, AMB['horarios'], AMB['pidf'], SH), flush=True)
t0 = time.time(); ant = None; parado = 0
while True:
    pids = vivos(); ul, tam, rc = estado(); hf = horario_fim(); la = lancador()
    parado = parado + 1 if (tam == ant and tam >= 0) else 0; ant = tam
    print('  [espera %s] um.py vivos: %s | stdout %s B | parado %d | RITO_RC %s | horario de fim %s | lancador %s | ultima: %s'
          % (time.strftime('%H:%M:%S'), pids or 'nenhum', tam, parado, rc, 'sim' if hf else 'nao', la, ul[:80]), flush=True)
    fora = la in ('AUSENTE', 'MORTO')
    if la == '?':
        print('  [espera] AVISO: a vida do lancador nao foi lida (.pid ilegivel ou sh indisponivel) -- conta como VIVO (fail-closed); sigo')
    if not pids and parado >= 1 and (rc is not None or fora):
        if rc is None:
            print('O LANCADOR ESTA FORA (%s: %s) E O STDOUT NAO TEM RITO_RC -- rito nao concluido pelo lancador (morte a forca?); nada foi feito.'
                  % (la, 'sem .rito_v386.pid' if la == 'AUSENTE' else '.rito_v386.pid VELHO: o processo nao vive ou nao e o lancador')); sys.exit(5)
        if rc != '0' or not L.FINAL_RE.match(ul):
            print('O RITO ACABOU NAO LIMPO: RITO_RC=%s; ultima linha: %r' % (rc, ul[:200])); sys.exit(3)
        if hf:
            break
        if fora:
            print('  [espera] AVISO VISIVEL: RITO_RC=0 e a linha final lidos, nenhum um.py vivo, o lancador FORA (%s) e o horario de fim NAO gravado -- o fim e\' tomado; '
                  'o horario vira informacao (a leitura usa a ultima modificacao do stdout, dito)' % la)
            break
        print('  [espera] AVISO: RITO_RC=0 lido, mas o horario de fim ainda nao esta gravado e o lancador esta vivo (%s) -- sigo' % la)
    if time.time() - t0 > MAX:
        print('TEMPO ESGOTADO (%d s) esperando o rito v386 -- O RITO AINDA NAO ACABOU (ou nao selou): nada foi feito.' % MAX); sys.exit(4)
    time.sleep(PASSO)
print('FIM DO RITO LIDO: RITO_RC=0, a linha final do rito, nenhum um.py vivo%s.' % (', o horario de fim gravado' if horario_fim() else ' (horario de fim AUSENTE, dito)'), flush=True)
t1 = time.time()
la = lancador()
while la in ('VIVO', '?') and time.time() - t1 < MAX_REST:
    print('  [espera %s] o lancador ainda restaura o servidor (lancador %s)' % (time.strftime('%H:%M:%S'), la), flush=True)
    time.sleep(min(PASSO, 30)); la = lancador()
if la in ('VIVO', '?'):
    print('AVISO VISIVEL: o lancador segue %s depois de %d s -- o log do lancador pode estar incompleto (no conferidor ele e\' so informacao); sigo.' % (la, MAX_REST))
elif la == 'MORTO':
    print('AVISO VISIVEL: o .rito_v386.pid ficou, mas o processo nao vive (pid VELHO: o trap do EXIT nao rodou) -- o log do lancador pode estar incompleto; sigo.')
else:
    print('o lancador terminou a restauracao (.rito_v386.pid ausente).')
sys.exit(0)
