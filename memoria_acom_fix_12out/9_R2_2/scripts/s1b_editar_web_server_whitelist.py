# -*- coding: utf-8 -*-
"""R2.2, passo 1b: no agi_validate_path do candidato_r2_2, a função interna da whitelist passa a comparar caminhos sem
o prefixo estendido do Windows (o GetFinalPathNameByHandle devolve o caminho SEM o prefixo, e uma raiz pode tê-lo).
Mesma disciplina do passo 1: âncora exata (1 ocorrência), CRLF preservado, a chave nunca impressa, cópia redigida
regravada em runs/."""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
WEB = R22 / 'candidato_r2_2' / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')

OLD = r'''    def inside_whitelist(candidate):
        for root in ALLOWED_ROOTS:
            try:
                root_real = os.path.realpath(root)
                if os.path.commonpath([candidate.lower(), root_real.lower()]) == root_real.lower():
                    return True
            except Exception:
                continue
        return False
'''

NEW = r'''    def plain(p):
        # without the extended-path prefix: the final path of a handle never carries it, a root may
        p = str(p)
        ext = os.sep * 2 + '?' + os.sep
        if p.startswith(ext + 'UNC' + os.sep):
            return os.sep * 2 + p[len(ext) + 4:]
        return p[len(ext):] if p.startswith(ext) else p

    def inside_whitelist(candidate):
        for root in ALLOWED_ROOTS:
            try:
                root_real = plain(os.path.realpath(root)).lower()
                if os.path.commonpath([plain(candidate).lower(), root_real]) == root_real:
                    return True
            except Exception:
                continue
        return False
'''


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = WEB.read_bytes()
    out = {'antes_sha256': sha(raw)}
    text = raw.decode('utf-8')
    assert text.count('\r\n') == text.count('\n') == text.count('\r')
    t = text.replace('\r\n', '\n')
    out['ancora'] = t.count(OLD)
    if out['ancora'] != 1:
        raise SystemExit('âncora aparece %d vez(es): nada escrito' % out['ancora'])
    t = t.replace(OLD, NEW)
    novo = t.replace('\n', '\r\n').encode('utf-8')
    assert KEY.findall(novo) == KEY.findall(raw)
    compile(novo.decode('utf-8'), str(WEB), 'exec')
    tmp = WEB.with_name(WEB.name + '.tmp_r2_2b')
    with open(tmp, 'xb') as f:
        f.write(novo)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == novo
    os.replace(tmp, WEB)
    red = KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), novo)
    (R22 / 'runs' / 'iald_web_server_r2_2_redigido.py').write_bytes(red)
    out.update(depois_sha256=sha(novo), depois_bytes=len(novo), redigido_sha256=sha(red),
               redigida_sem_chave_original=all(k not in red for k in KEY.findall(novo)))
    (R22 / 'runs' / 's1b_editar_web_server_whitelist.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print(json.dumps(out))


if __name__ == '__main__':
    sys.exit(main())
