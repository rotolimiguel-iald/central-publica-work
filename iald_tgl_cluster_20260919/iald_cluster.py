"""Always-present, integrity-checked topic memory derived from a pinned release."""
import hashlib
import json
from pathlib import Path
import re


def active_cluster(manifest, source_sha):
    config = json.loads(Path(manifest).read_bytes()).get('active_cluster')
    if config is None:
        return '', {}
    if config.get('release_source_sha256') != source_sha:
        raise ValueError('Cluster e kernel pertencem a versões diferentes.')
    if not re.fullmatch(r'v[0-9]+', str(config.get('release',''))) or not re.fullmatch(r'[0-9a-f]{40}',str(config.get('commit',''))):
        raise ValueError('Cluster sem proveniência fixada.')
    path = Path(config['path'])
    if not path.is_absolute() or path.suffix != '.md':
        raise ValueError('Caminho de cluster inválido.')
    raw = path.read_bytes()
    if not 0 < len(raw) <= 4000000 or hashlib.sha256(raw).hexdigest() != config['sha256']:
        raise ValueError('Cluster alterado ou indisponível; não será omitido silenciosamente.')
    text = raw.decode('utf-8')
    if text.count('\n### ') < config['core_sections']:
        raise ValueError('Cobertura do cluster inconsistente.')
    return ('\n<CLUSTER_TGL_ATIVO>\n'+text+'\n</CLUSTER_TGL_ATIVO>\n',
            {'active_cluster':{k:v for k,v in config.items() if k not in ('path','kernel_bundle','kernel_verification')},
             'cluster_always_present':True})
