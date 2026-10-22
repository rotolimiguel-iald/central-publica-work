"""Append task evidence with byte backups and compare-before-replace."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')


def write_new(path, data):
    path = Path(path)
    if path.exists():
        raise RuntimeError('Receipt already exists: ' + path.name)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as handle:
        handle.write(data)
    assert temp.read_bytes() == data
    temp.replace(path)


def record(name, report, note, before_memory=None):
    memory = ROOT / 'CLAUDE.md'
    before = memory.read_bytes() if before_memory is None else before_memory
    now = datetime.now().astimezone()
    report = {'recorded_at': now.isoformat(), **report}
    target = WORK / name
    write_new(target, json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
    if memory.read_bytes() != before:
        raise RuntimeError('CLAUDE.md changed externally; receipt saved, append stopped.')
    suffix = now.strftime('%Y%m%d_%H%M%S_%f')
    backup = memory.with_name(memory.name + '.bak_' + suffix)
    write_new(backup, before)
    assert backup.read_bytes() == before
    newline = '\r\n' if b'\r\n' in before else '\n'
    appendix = (newline * 2 + '### ' + now.strftime('%d/%m/%Y %H:%M %z')
                + ' — Codex / ordem build 16 — ' + report['task'] + newline * 2
                + note + newline + 'Recibo: `work/iald_openai_motor_20260914/'
                + name + '`.' + newline)
    after = before + appendix.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    temp = memory.with_name(memory.name + '.tmp_' + suffix)
    write_new(temp, after)
    if memory.read_bytes() != before:
        raise RuntimeError('CLAUDE.md changed externally; append not applied.')
    temp.replace(memory)
    assert memory.read_bytes() == after and len(after) > len(before)
    return target
