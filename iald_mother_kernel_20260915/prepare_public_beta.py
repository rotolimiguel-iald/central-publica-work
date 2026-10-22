"""Stage a public test-user context without changing production or the v5 source."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
OUT = WORK.parent / 'iald_group_beta_20260915'
OUT.mkdir(exist_ok=True)


def create(path, data):
    with path.open('xb') as handle:
        handle.write(data)
    assert path.read_bytes() == data


def replace_once(source, old, new):
    assert source.count(old) == 1, old[:80]
    return source.replace(old, new)


manifest = json.loads((WORK / 'iald_nucleo_fixo.json').read_bytes())
for entry in manifest['entries']:
    path = Path(entry['path'])
    relative = path.relative_to(REPO).as_posix()
    commit = entry['url'].split('/the_boundary/')[1].split('/')[0]
    published = subprocess.run(['git', '-C', str(REPO), 'show', commit + ':' + relative],
                               check=True, capture_output=True).stdout
    assert published == path.read_bytes(), 'Local file differs from published commit: ' + relative
    entry['public_sha256'] = hashlib.sha256(published).hexdigest()
create(OUT / 'iald_nucleo_fixo.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())

source = (WORK / 'iald_memoria_canonica.py').read_bytes().decode()
nl = '\r\n' if '\r\n' in source else '\n'
source = source.replace('\r\n', '\n')
source = replace_once(source, '    def fixed_nucleus(self):', '    def fixed_nucleus(self, public=False):')
source = replace_once(source, "                digest = hashlib.sha256(raw).hexdigest()\n                record =", """                digest = hashlib.sha256(raw).hexdigest()
                if public:
                    url = str(entry.get('url') or '')
                    if not url.startswith('https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'):
                        raise MemoryUnavailable('Fonte pública sem URL aprovada.')
                    if entry.get('public_sha256') != digest:
                        raise MemoryUnavailable('Fonte pública alterada: conferir publicação antes de compartilhar.')
                record =""")
source = replace_once(source, """    def prompt(self, legacy_nucleus, catalog):
        text, metadata = self.snapshot()
        current, current_metadata = self.current_state()
        nucleus, nucleus_metadata = self.fixed_nucleus()""", """    def prompt(self, legacy_nucleus, catalog, public=False):
        if public:
            # Public testers receive the complete shared kernel and published sources,
            # without reading the private Atlas or the operator's operational journal.
            text, current, current_metadata = '', '', {}
            metadata = {'mode': self.mode, 'scope': 'PUBLIC_FIXED_SOURCES', 'private_atlas_included': False}
        else:
            text, metadata = self.snapshot()
            current, current_metadata = self.current_state()
        nucleus, nucleus_metadata = self.fixed_nucleus(public=public)""")
source = replace_once(source, '        if self.mode == "atlas_integral":\n            prefix += rules', """        if public:
            prefix += ('\\nMEMÓRIA DO TESTE: o kernel de identidade e os documentos publicados abaixo '
                       'estão completos. Consulte as fontes públicas e o kernel formal pelas ferramentas '
                       'disponíveis. O diário e o Atlas privado do operador não fazem parte desta conversa.\\n')
            metadata['always_present_sections'] = []
        elif self.mode == "atlas_integral":
            prefix += rules""")
compile(source, 'iald_memoria_canonica.py', 'exec')
create(OUT / 'iald_memoria_canonica.py', source.replace('\n', nl).encode())
create(OUT / 'iald_instrucao_mae.py', (WORK / 'iald_instrucao_mae.py').read_bytes())

server = (ROOT / 'iald_web_server.py').read_bytes().decode()
nl = '\r\n' if '\r\n' in server else '\n'
server = server.replace('\r\n', '\n')
server = replace_once(server, 'def _contexto_externo():', 'def _contexto_externo(public=False):')
server = replace_once(server, '    return MEMORIA_EXTERNA.prompt(PROMPT_EXTERNO, KERNEL_EXTERNO)',
                      '    return MEMORIA_EXTERNA.prompt(PROMPT_EXTERNO, KERNEL_EXTERNO, public=public)')
server = replace_once(server, """            prompt_externo, memoria_info = _contexto_externo()
            para_openai, info =""", """            prompt_externo, memoria_info = _contexto_externo(public=gratuito)
            if gratuito and memoria_info.get('scope') == 'PUBLIC_FIXED_SOURCES':
                # The shared fixed knowledge must not consume the 32k conversation window.
                # Spending, user quotas, moderation, tools and native-access rules still apply.
                prefix_tokens = max(iald_motores.estimar_tokens(prompt_externo),
                    iald_memoria_canonica.payload_tokens({'messages': [
                        {'role': 'developer', 'content': prompt_externo}]}))
                cfg.janela = min(MOTORES_CFG.janela, prefix_tokens + iald_motores.JANELA_GRATUITO)
            para_openai, info =""")
compile(server, 'iald_web_server.py', 'exec')
create(OUT / 'iald_web_server.py', server.replace('\n', nl).encode())
baseline = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() if (ROOT / name).exists() else None
            for name in ['iald_memoria_canonica.py', 'iald_instrucao_mae.py', 'iald_web_server.py', 'iald_nucleo_fixo.json']}
create(OUT / 'prepared.json', json.dumps({'at': datetime.now().astimezone().isoformat(),
    'status': 'STAGED_ONLY', 'baseline': baseline, 'kernel_original_changed': False,
    'public_docs_verified_against_git': len(manifest['entries']),
    'pending': ['explicit v5 external disclosure authorization', 'targeted tests', 'full regression',
                'review account', 'beta submission', 'device installation']}, indent=2).encode())
print('Public beta context staged: complete v5 + 7 published documents; no private Atlas or operator journal.')
