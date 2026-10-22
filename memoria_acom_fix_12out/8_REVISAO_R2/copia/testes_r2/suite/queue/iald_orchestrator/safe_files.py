"""Atomic local writes with byte-exact immediate backups."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os


def replace_bytes(path, data):
    path = Path(path)
    if not data:
        raise ValueError('Empty replacement refused')
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_bytes() if path.exists() else None
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if old is not None:
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    assert (path.read_bytes() if path.exists() else None) == old
    os.replace(temp, path)
    assert path.read_bytes() == data


def save_json(path, value):
    replace_bytes(path, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))


def utc_now():
    return datetime.now(timezone.utc).isoformat()
