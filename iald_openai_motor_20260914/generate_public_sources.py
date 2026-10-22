"""Generate public navigation URLs from tracked paths and the canonical root door."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote, urlparse, unquote

WORK = Path(__file__).parent
REPO = Path('C:/IALD/Artigo/the_boundary')
STAGE = WORK / 'stage'
git = ['git', '-c', 'safe.directory=' + REPO.as_posix(), '-C', str(REPO)]
tracked = set(subprocess.check_output(git + ['ls-files', '-z']).decode('utf-8').split('\0')) - {''}
door_bytes = (REPO / 'PORTA.json').read_bytes()
door = json.loads(door_bytes)
remote = subprocess.check_output(git + ['remote', 'get-url', 'origin']).decode().strip().removesuffix('.git')
if remote != door['repo']:
    raise RuntimeError('Repository remote differs from the canonical door')
base = door['repo_raw_base']
if not base.startswith('https://raw.githubusercontent.com/') or not base.endswith('/'):
    raise RuntimeError('Unexpected public raw URL')
entries = [{'id': 'site', 'role': 'Página pública da TGL', 'url': door['site']},
           {'id': 'repository', 'role': 'Repositório público da TGL', 'url': remote}]
for path, role in [('llms.txt', 'Entrada das IAs e ordem de leitura'),
                   ('PORTA.json', 'Porta raiz: hierarquia e remissões'),
                   ('PORTA.md', 'Porta raiz em texto'), ('README.md', 'Apresentação do repositório'),
                   ('ESTADO_ATUAL.md', 'Estado publicado e limites declarados'),
                   ('read-brief.md', 'Guia curto de localização das respostas'),
                   ('TUNEL.json', 'Mapa plano dos arquivos públicos')]:
    if path not in tracked:
        raise RuntimeError('Untracked public entry: ' + path)
    entries.append({'id': path, 'role': role, 'path': path, 'url': base + quote(path, safe='/')})
for child in door['portas_abaixo']:
    if child.get('id') not in ('artigo_1', 'artigo_2', 'artigo_3'):
        continue
    for key, suffix, role in [('porta_json_url', 'door', 'Porta da pasta'),
                               ('canonico_url', 'source', 'Fonte canônica publicada')]:
        given_url = child[key]
        if not given_url.startswith(base):
            raise RuntimeError('Article outside the public repository')
        path = unquote(given_url[len(base):])
        if path not in tracked:
            raise RuntimeError('Article absent from tracked files: ' + path)
        entries.append({'id': child['id'] + '_' + suffix, 'role': child['titulo'] + ' — ' + role,
                        'path': path, 'url': base + quote(path, safe='/')})

record = {'format': 1, 'generated_at': datetime.now(timezone.utc).isoformat(),
          'source': 'git ls-files -z + canonical PORTA.json; URLs generated with urllib.parse.quote',
          'root_door_sha256': hashlib.sha256(door_bytes).hexdigest(),
          'repository': remote, 'site': door['site'], 'raw_base': base, 'entries': entries,
          'scope': 'PUBLIC_NAVIGATION_ONLY__NOT_A_CURRENT_PROOF_OR_COMPILATION_VERDICT'}
target = STAGE / 'iald_fontes_publicas.json'
payload = json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8')
if target.exists():
    backup = target.with_name(target.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    backup.write_bytes(target.read_bytes())
fd, path = tempfile.mkstemp(prefix='.' + target.name + '.', dir=target.parent)
os.close(fd)
temporary = Path(path)
temporary.write_bytes(payload)
if temporary.read_bytes() != payload:
    raise RuntimeError('Temporary output verification failed')
os.replace(temporary, target)
assert target.read_bytes() == payload
print(json.dumps({'status': 'GENERATED', 'entries': len(entries), 'path': str(target)}, ensure_ascii=False))
