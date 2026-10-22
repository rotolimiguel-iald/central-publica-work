"""Atomic local writes with byte-exact immediate backups."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os


_UNSPECIFIED = object()


def replace_bytes(path, data, *, expected_old=_UNSPECIFIED):
    path = Path(path)
    if not data:
        raise ValueError('Empty replacement refused')
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_bytes() if path.exists() else None
    if expected_old is not _UNSPECIFIED and old != expected_old:
        raise ValueError('Replacement baseline changed; no overwrite')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if old is not None:
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    current = path.read_bytes() if path.exists() else None
    if expected_old is not _UNSPECIFIED and current != expected_old:
        raise ValueError('Replacement baseline changed before commit; no overwrite')
    assert current == old
    os.replace(temp, path)
    assert path.read_bytes() == data


def save_json(path, value, *, expected_old=_UNSPECIFIED):
    replace_bytes(path, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'), expected_old=expected_old)


def utc_now():
    return datetime.now(timezone.utc).isoformat()
