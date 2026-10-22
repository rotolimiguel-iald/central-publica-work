"""Build only staging outputs from a byte-for-byte, read-only production snapshot."""
from pathlib import Path
import difflib
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD\app\iald.js')


def write(name, raw):
    target = HERE / name
    temporary = target.with_suffix(target.suffix + '.tmp')
    temporary.write_bytes(raw)
    if temporary.read_bytes() != raw:
        raise OSError('Staging verification failed')
    os.replace(temporary, target)


def build():
    baseline = HERE / 'iald.base.js'
    if not baseline.exists():
        write(baseline.name, SOURCE.read_bytes())
    original = baseline.read_bytes()
    text = original.decode('utf-8').replace('\r\n', '\n')
    base = text

    def replace(old, new):
        nonlocal text
        if text.count(old) != 1:
            raise RuntimeError(f'Anchor mismatch: {old[:90]!r}')
        text = text.replace(old, new)

    module = (HERE / 'artifact_access.js').read_text(encoding='utf-8').replace('export ', '')
    replace('const VERSAO =', '// ARTIFACT ACCESS MODULE BEGIN\n' + module + '\n// ARTIFACT ACCESS MODULE END\n\nconst VERSAO =')
    integration = """let artifactAccessUI = null;
function startArtifactAccessUI() {
  if (artifactAccessUI) return;
  artifactAccessUI = mountArtifactAccess({ document, window, request: fetchIALD,
    identity: () => ({ account: backgroundOwner, token: tokenApp() }),
    unsafeStyle: estiloPerigoso, initialSearch: location.search,
    onAuthLost: () => { desanexarRespostasBackground(true); avisar('Entre novamente para abrir o arquivo.'); },
  });
  artifactAccessUI.authenticated();
}

"""
    replace('const svg =', integration + 'const svg =')
    replace('function desanexarRespostasBackground(sair = false) {', 'function desanexarRespostasBackground(sair = false) {\n  if (sair) artifactAccessUI?.reset();')
    replace('  refreshNativeNotificationsUI();\n  return backgroundOwner;', '  refreshNativeNotificationsUI();\n  artifactAccessUI?.authenticated();\n  return backgroundOwner;')
    replace('  frag.appendChild(molde.content);\n  enfeitarCodigo(frag);', '  frag.appendChild(molde.content);\n  normalizeArtifactLinks(frag);\n  enfeitarCodigo(frag);')
    replace('function iniciar() {\n  aplicarTema', 'function iniciar() {\n  startArtifactAccessUI();\n  aplicarTema')
    # The existing sanitizer and formula handling remain unchanged.
    start, end = '// ── SANEAMENTO (início) ──', '// ── SANEAMENTO (fim) ──'
    assert base[base.index(start):base.index(end)] == text[text.index(start):text.index(end)]
    raw = text.encode('utf-8')
    write('iald.js', raw)
    write('client.patch', ''.join(difflib.unified_diff(base.splitlines(True), text.splitlines(True), fromfile='a/app/iald.js', tofile='b/app/iald.js')).encode('utf-8'))
    write('build_manifest.json', json.dumps({'source': str(SOURCE), 'source_sha256': hashlib.sha256(original).hexdigest(),
        'output_sha256': hashlib.sha256(raw).hexdigest(), 'deploy_files': ['app/iald.js'],
        'production_written': False, 'new_runtime_dependencies': []}, indent=2).encode('utf-8'))
    print(json.dumps({'staged': str(HERE / 'iald.js'), 'bytes': len(raw)}))


if __name__ == '__main__':
    build()
