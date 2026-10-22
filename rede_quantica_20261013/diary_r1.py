"""Append evidenced progress to the task diary; preserve bytes and immutable receipts."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(r'C:\IALD\Central de Patentes')
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
WORK = ROOT / 'work/rede_quantica_20261013'
DIARY = ROOT / 'memory/DIARIO_CONSTRUCAO_QG.md'
WHO = 'codex-gerente-tgl'
PY = r'C:\Python314\python.exe'
CLI = r'C:\IALD\PROGRAMA_IALD\iald.py'

def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def new(path, value):
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)
    return pin(path)

def claim():
    cp = subprocess.run([PY, '-B', '-X', 'utf8', CLI, 'ver', 'F1.REDE'], capture_output=True, text=True, encoding='utf-8', check=True)
    value = json.loads(cp.stdout)
    active = value['reivindicacao']
    assert active['quem'] == WHO
    assert dt.datetime.fromisoformat(active['vence_em']) > dt.datetime.now(dt.timezone.utc)
    assert 'DIARIO_CONSTRUCAO_QG.md' in active['nota']
    return active

def append_bytes(path, addition, marker):
    path = Path(path)
    old = path.read_bytes() if path.exists() else None
    if old is not None and marker.encode() in old:
        raise ValueError('Entry already present; recover receipt rather than repeat')
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    backup = None
    if old is not None:
        bak = path.with_name(path.name + '.bak_' + stamp)
        with bak.open('xb') as stream:
            stream.write(old)
            stream.flush()
            os.fsync(stream.fileno())
        assert bak.read_bytes() == old
        backup = pin(bak)
    raw = (old or b'') + addition.encode('utf-8')
    tmp = path.with_name(path.name + '.tmp_' + stamp)
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    if old is None:
        assert not path.exists()
        os.rename(tmp, path)
    else:
        assert path.read_bytes() == old, 'Concurrent memory change'
        os.replace(tmp, path)
    assert path.read_bytes() == raw and raw.startswith(old or b'')
    return {'surface': pin(path), 'backup': backup, 'append_bytes': len(addition.encode('utf-8')), 'append_only': True}

def main():
    entry_path = Path(sys.argv[1])
    entry = json.loads(entry_path.read_text(encoding='utf-8'))
    event = entry['id']
    if not event.replace('-', '').replace('_', '').isalnum():
        raise ValueError('Invalid event identifier')
    receipt = OUT / 'diary_events' / (event + '_RECEIPT.json')
    intent = OUT / 'diary_events' / (event + '_INTENT.json')
    if receipt.exists() or intent.exists():
        raise FileExistsError('Event already attempted; inspect its intent and diary')
    active = claim()
    sources = [pin(p) for p in entry['sources']]
    at = dt.datetime.now(dt.timezone.utc).isoformat()
    new(intent, {'entry': pin(entry_path), 'claim': active, 'sources': sources, 'started_utc': at})
    marker = 'qg_diary_' + event
    text = ''
    if not DIARY.exists():
        text = '# Diário da construção matemática da TGL / QG\n\n'
        text += 'Casa: Central de Patentes. Autor operacional: codex-gerente-tgl. Diário cronológico desta frente, com evidências; o Atlas continua sendo a fonte conceitual canônica.\n\n'
        text += 'Cada avanço material recebe data, unidade, estatuto, verificação, pendências e próxima ação. Entradas anteriores permanecem; correções são acrescentadas ao lado. Os recibos e retratos imutáveis ficam em F1.REDE/diary_events. O diário vivo pode crescer e não é usado como evidência imutável. Atualização ao concluir etapas, não agendamento autônomo.\n\n'
        text += 'Base de trabalho: v392 autorizada pelo operador. A ratificação e a implantação são conferidas por seus recibos próprios. Nenhuma conclusão empírica ou mudança de gate decorre deste diário.\n'
    text += f'\n\n## {entry["title"]}\n<!-- {marker} -->\n\n'
    text += f'Inscrito em UTC: {at}. Unidade: {entry.get("unit", "F1.REDE")}. Em nome de {WHO}. Reivindicação ativa conferida pelo quadro.\n\n'
    text += entry['body'].rstrip() + '\n\n### Evidências lidas nesta inscrição\n\n'
    for source in sources:
        text += f'- `{source["path"]}` — SHA256 `{source["sha256"]}`; {source["bytes"]} bytes.\n'
    result = append_bytes(DIARY, text, marker)
    snapshot = OUT / 'diary_events' / (event + '_DIARIO_SNAPSHOT.md')
    new(snapshot, DIARY.read_bytes().decode('utf-8'))
    surfaces = []
    if entry.get('link_surfaces'):
        note = f'\n\n### {entry["title"]} — diário e continuidade\n<!-- {marker} -->\nEm nome de {WHO}, sob reivindicação da F1.REDE. [REAL — registro] Diário cronológico em `{DIARY}`; evidência imutável em `{snapshot}`. {entry["surface_summary"]}\n'
        for path in [ROOT/'memory/TGL_ATLAS.md', ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']:
            surfaces.append(append_bytes(path, note, marker))
    new(receipt, {'unit': 'F1.REDE', 'author': WHO, 'at_utc': at, 'claim': active, 'entry': pin(entry_path), 'diary': result, 'snapshot': pin(snapshot), 'surfaces': surfaces, 'sources': sources})
    print(json.dumps({'ok': True, 'diary': str(DIARY), 'receipt': pin(receipt)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
