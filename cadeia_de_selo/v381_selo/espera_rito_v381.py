# -*- coding: utf-8 -*-
# ESPERA o fim do rito v381 SO POR LEITURA: nao roda nada do rito, nao mata processo, nao escreve fora de v381_selo.
# Fim = (a) nenhum processo "python ... um.py" vivo (lista de processos lida via Get-CimInstance, so leitura) E (b) o stdout parado por 2
# leituras seguidas E (c) a ultima linha nao-trailer do stdout e a linha final do rito ("[selo] colapso tipado: ...").
# rc: 0 = terminou com a linha final; 3 = o processo acabou SEM a linha final (rito nao limpo); 4 = tempo esgotado (V381_ESPERA_MAX_S).
import os, sys, time, subprocess, re
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v381 as L
NOS = os.environ.get('V381_NOS') or L.NOS_REAL
STP = os.path.join(NOS, 'rodada_v381_stdout.txt')
PASSO = int(os.environ.get('V381_ESPERA_PASSO_S', '60')); MAX = int(os.environ.get('V381_ESPERA_MAX_S', str(4 * 3600)))
PS = ("$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
      "Where-Object { $_.CommandLine -ne $null -and $_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'")   # v381 (aferidor B1/C2)


def vivos():
    try:
        r = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', PS], capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or r.stderr.strip() or 'VIGIA_OK' not in r.stdout:   # v381 (aferidor B1): vigia fail-closed -- falha de leitura conta como "vivo"
            print('  [espera] AVISO: o vigia de processos falhou (rc %s; %r) -- sigo esperando' % (r.returncode, r.stderr[:200])); return ['?']
        return [x.strip() for x in r.stdout.split() if x.strip().isdigit()]
    except Exception as e:           # falha de leitura e' falha visivel: conta como "vivo" (nao declara fim sem ver)
        print('  [espera] AVISO: nao consegui ler a lista de processos: %r -- sigo esperando' % e); return ['?']


def ultima():
    try:
        t = open(STP, encoding='utf-8', errors='replace').read()
    except OSError:
        return '', -1
    ls = [l for l in t.splitlines() if l.strip() and not L.TRAILER_RE.match(l.strip())]
    return (ls[-1] if ls else ''), os.path.getsize(STP)


t0 = time.time(); ant = None; parado = 0
while True:
    pids = vivos(); ul, tam = ultima()
    parado = parado + 1 if (tam == ant and tam >= 0) else 0; ant = tam
    print('  [espera %s] processos um.py vivos: %s | stdout %s B | parado %d | ultima: %s' % (time.strftime('%H:%M:%S'), pids or 'nenhum', tam, parado, ul[:90]), flush=True)
    if not pids and parado >= 1:
        if L.FINAL_RE.match(ul):
            print('FIM DO RITO LIDO: a linha final esta no stdout e nenhum processo um.py vive.'); sys.exit(0)
        print('O RITO ACABOU SEM A LINHA FINAL (ultima: %r) -- rito nao limpo.' % ul[:200]); sys.exit(3)
    if time.time() - t0 > MAX:
        print('TEMPO ESGOTADO (%d s) esperando o rito -- nada foi feito.' % MAX); sys.exit(4)
    time.sleep(PASSO)
