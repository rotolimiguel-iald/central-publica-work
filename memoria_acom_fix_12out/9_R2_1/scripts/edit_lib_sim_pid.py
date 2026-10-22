# -*- coding: utf-8 -*-
"""R2.1 (achado do próprio ensaio K4): o backend SIMULADO reconhecia um pid reaproveitado pelo Windows como o supervisor
morto (os arquivos pids/*.json ficam; o pid volta a existir noutro processo). Agora confere também a hora de criação
do processo contra a hora registrada pelo simulado. Só ProcessosSim muda; o backend de produção (PowerShell) lista por
linha de comando e não usa pid guardado."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'implantacao_lib.py'
s = P.read_bytes().decode('utf-8')


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)


sub('''class ProcessosSim:''', '''def _pid_criado_em(pid):
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


class ProcessosSim:''')

sub('''            if _pid_vivo(d['pid']):
                out.append(d)
        return out''', '''            if _pid_vivo(d['pid']):
                # R2.1: pid reaproveitado pelo Windows não é o processo simulado (hora de criação diferente)
                criado = _pid_criado_em(d['pid'])
                if criado is not None and d.get('t') is not None and abs(criado - float(d['t'])) > 5.0:
                    continue
                out.append(d)
        return out''')
P.write_bytes(s.encode('utf-8'))
print('ok')
