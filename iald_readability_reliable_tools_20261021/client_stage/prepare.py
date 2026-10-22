from pathlib import Path
import hashlib
import json
import re
import difflib

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
OUT = Path(__file__).resolve().parent
NAMES = ('iald.js', 'iald.css', 'index.html')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def replace_once(text, old, new):
    assert text.count(old) == 1, old[:100]
    return text.replace(old, new, 1)

originals = {name: (ROOT / 'app' / name).read_bytes() for name in NAMES}
for name, raw in originals.items():
    (OUT / 'origin').mkdir(exist_ok=True)
    target = OUT / 'origin' / name
    if target.exists():
        assert target.read_bytes() == raw, 'Origin changed; stop for reconciliation'
    else:
        target.write_bytes(raw)

js = originals['iald.js'].decode('utf-8')
js = re.sub(r"const MEDIA_LIMIT_TEXT = [^\n]+\n", '', js, count=1)
js = re.sub(r"  if \(midiaPermitida\('audio'\).*MEDIA_LIMIT_TEXT\)\);\r?\n", '', js, count=1)
assert 'MEDIA_LIMIT_TEXT' not in js
marker = 'let mediaDraftDatabase = null'
helpers = r'''const MEDIA_DISABLED_TEXT = 'Novos anexos de áudio e vídeo estão desativados. Use PDF, texto ou imagem. O histórico anterior foi preservado.';
// Selection, drop, paste and direct attachment submission share this policy.
function isNewAudioVideo(value) {
  if (!value) return false;
  const mime = String(value.mime || value.type || '').trim();
  return /^(audio|video)\//i.test(mime) ||
    /\.(wav|wave|mp3|mp2|flac|ogg|oga|opus|m4a|m4b|aac|aiff?|wma|amr|mid|midi|mp4|m4v|mov|avi|wmv|webm|mkv|mpeg|mpg|ogv|3gp|3g2|ts|mts|m2ts)$/i.test(String(value.name || '').trim()) ||
    !!value.localDraftId || !!value.media || ['audio', 'video'].includes(value.mediaKind || value.kind) ||
    ['input_audio', 'video_url', 'iald_media', 'iald_local_media'].includes(value.type) ||
    /^data:(audio|video)\//i.test(String(value.image || value.image_url?.url || ''));
}
function rejectNewAudioVideo(anexos) {
  if (anexos.some(isNewAudioVideo)) throw Error(MEDIA_DISABLED_TEXT);
}
'''
js = replace_once(js, marker, helpers + marker)
js = replace_once(js, 'async function lerMidiaLocal(f, tipo) {',
                  'async function lerMidiaLocal(f, tipo) {\n  throw Error(MEDIA_DISABLED_TEXT);')
js = replace_once(js, 'async function mediaUpload(anexo, owner, conversation) {',
                  'async function mediaUpload(anexo, owner, conversation) {\n  throw Error(MEDIA_DISABLED_TEXT);')
js = replace_once(js, 'async function mediaConsent(anexos, text, conversation) {',
                  'async function mediaConsent(anexos, text, conversation) {\n  rejectNewAudioVideo(anexos);')
js = replace_once(js, 'async function enviarTexto(texto, anexos) {',
                  'async function enviarTexto(texto, anexos) {\n  rejectNewAudioVideo(anexos);')
js = replace_once(js, "  return limitesDoPlano()?.[tipo] === true;", '  return false; // New audio/video selection is disabled, including advertised server capabilities.')
js = re.sub(r"  const extrasMidia = [^\n]+\n  if \(extrasMidia.length\)[^\n]+\n", '', js, count=1)
# Do not reselect persisted drafts. Keep their bytes and historical messages intact.
start = js.index('async function mediaRestoreDrafts(conversation) {')
end = js.index('\nasync function lerMidiaLocal', start)
js = js[:start] + '''async function mediaRestoreDrafts(conversation) {
  // Existing local drafts remain stored; they are not new selectable attachments.
  return;
}
''' + js[end:]
start = js.index('    const tipoMidia = ', js.index('async function receberArquivos'))
end = js.index('    if (ehImagem', start)
js = js[:start] + "    if (isNewAudioVideo(f)) { avisar(MEDIA_DISABLED_TEXT); continue; }\n\n" + js[end:]

css = originals['iald.css'].decode('utf-8')
for role in ('user', 'ai'):
    pattern = rf'(\.msg\[data-papel="{role}"\] \.msg-corpo \{{[^}}]*?)font-size: 16\.5px;'
    css, count = re.subn(pattern, r'\1font-size: 15.5px;', css, count=1)
    assert count == 1
# Compensate relative inline code/math for the 16.5 -> 15.5 prose reduction.
# Blocks have their own fixed size, and no root/viewport/text adjustment changes.
css = replace_once(css, 'font-size: .86em;', 'font-size: .915483871em; /* same inline-code size after prose reduction */')
css = replace_once(css, 'font-size: 1.04em;', 'font-size: 1.107096774em; /* same formula size after prose reduction */')
staged = {'iald.js': js.encode('utf-8'), 'iald.css': css.encode('utf-8'), 'index.html': originals['index.html']}
files = []
for name, raw in staged.items():
    (OUT / name).write_bytes(raw)
    diff = ''.join(difflib.unified_diff(originals[name].decode('utf-8').splitlines(True),
        raw.decode('utf-8').splitlines(True), fromfile='origin/'+name, tofile='staged/'+name))
    (OUT / (name + '.diff')).write_bytes(diff.encode('utf-8'))
    files.append({'file': name, 'source': str(ROOT/'app'/name), 'origin_sha256': sha(originals[name]),
                  'staged_sha256': sha(raw), 'changed': raw != originals[name]})
mirrors = []
for relative in ('app', 'iald-app/www', 'iald-app/ios/App/App/public',
                 'iald-app/android/app/src/main/assets/public',
                 'iald-app/android/app/build/intermediates/assets/release/mergeReleaseAssets/public'):
    directory = ROOT / relative
    mirrors.append({'directory': str(directory), 'exists': directory.exists(),
        'files': [{'name': name, 'exists': (directory/name).exists(),
                   'sha256': sha((directory/name).read_bytes()) if (directory/name).exists() else None,
                   'matches_runtime_origin': (directory/name).read_bytes() == originals[name] if (directory/name).exists() else None}
                  for name in NAMES]})
server = ROOT/'iald_web_server.py'
server_raw = server.read_bytes()
server_lines = server_raw.decode('utf-8').splitlines()
receipt = {'unit': 'F9.APP_READABILITY_RELIABLE_TOOLS_20261021', 'status': 'STAGED_NOT_INSTALLED',
    'files': files, 'mirrors': mirrors,
    'limits': {'client_total_attachments': 6, 'client_images': 3, 'image_bytes': 8000000,
               'pdf_bytes': 25000000, 'text_bytes': 2000000, 'displayed_token_estimate': 100000,
               'token_estimate_enforced_by_client': False, 'server_extract_bytes': 25*1024*1024,
               'server_extract_max_chars': 400000,
               'evidence': {'client_line': 2846, 'client_size_checks_lines': [3287,3295,3312],
                            'server_path': str(server), 'server_sha256': sha(server_raw),
                            'server_start_line': 8436, 'server_end_line': 8488,
                            'server_excerpt': '\n'.join(server_lines[8435:8488])}},
    'scope': 'Client source staging only; no provider, git, restart or installation.',
    'limitations': ['No device/browser visual validation or iOS Dynamic Type measurement; existing root/text-size-adjust and input rules preserved.',
                   'Client guards use declared MIME/extensions/attachment metadata, not content sniffing. Server must independently enforce policy.',
                   'Existing historical rendering/storage/recovery code remains. Old local media cannot be newly uploaded; attempting that path fails clearly without deleting history.',
                   'Server/account/model/request-context constraints can further reduce admission; no claim of universal 50 MB support.']}
(OUT/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'staged': files, 'mirrors': len(mirrors)},ensure_ascii=False))
