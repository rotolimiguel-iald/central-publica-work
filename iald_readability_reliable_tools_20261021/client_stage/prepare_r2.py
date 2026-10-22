from pathlib import Path
import re
import json
import hashlib
import difflib

HERE = Path(__file__).resolve().parent
OUT = HERE / 'R2'
OUT.mkdir(exist_ok=True)
source = (HERE / 'iald.js').read_bytes().decode('utf-8')

def replace(old, new):
    global source
    assert source.count(old) == 1, old[:100]
    source = source.replace(old, new, 1)

def function(name, replacement):
    global source
    pattern = r'^(?:async )?function ' + name + r'\([^]*?^}'
    # Python has no JS [^] wildcard; DOTALL makes the bounded end explicit.
    pattern = r'^(?:async )?function ' + name + r'\(.*?^}'
    source, count = re.subn(pattern, lambda _: replacement, source, count=1, flags=re.M|re.S)
    assert count == 1

helper = r'''// Outbound-only metadata: never rewrite persisted history or send historical media bytes.
function historicalMediaContent(content) {
  if (!Array.isArray(content)) return content;
  return content.map(part => {
    if (!['input_audio', 'video_url', 'iald_media', 'iald_local_media'].includes(part?.type)) return part;
    const kind = part.type === 'input_audio' ? 'áudio' : part.type === 'video_url' ? 'vídeo'
      : part.kind === 'audio' ? 'áudio' : part.kind === 'video' ? 'vídeo' : 'áudio/vídeo';
    const metadata = { type: part.type };
    // Only bounded identifiers, never raw data/URLs or arbitrary descriptive text.
    for (const key of ['media_ref', 'localDraftId', 'sha256']) {
      if (typeof part[key] === 'string' && /^[a-zA-Z0-9_-]{1,128}$/.test(part[key])) metadata[key] = part[key];
    }
    if (Number.isSafeInteger(part.bytes) && part.bytes >= 0) metadata.bytes = part.bytes;
    return { type: 'text', text: '[anexo histórico ' + kind + ', análise indisponível nesta mensagem; metadados: '
      + JSON.stringify(metadata) + ']' };
  });
}
function outboundHistory(messages) {
  return messages.map((message, index) => {
    // The last user message is the current request, never a legacy exemption.
    if (index === messages.length - 1 && message.role === 'user' && Array.isArray(message.content)) {
      rejectNewAudioVideo(message.content);
      return { ...message };
    }
    return { ...message, content: historicalMediaContent(message.content) };
  });
}
'''
replace('function rejectNewAudioVideo(anexos) {', helper + 'function rejectNewAudioVideo(anexos) {')
replace('async function enviarTexto(texto, anexos) {\n  rejectNewAudioVideo(anexos);',
        'async function enviarTexto(texto, anexos) {\n  rejectNewAudioVideo(anexos);\n  if (Array.isArray(texto)) rejectNewAudioVideo(texto);')
start = source.index('  const hasMedia = ', source.index('async function enviarTexto'))
end = source.index('  let conteudo = texto;', start)
source = source[:start] + '  const hasMedia = false; // New media rejected above; history is projected only by montarEnvio.\n  const midias = [];\n' + source[end:]
replace('  for (const m of recortar(c.mensagens, sys)) {',
        '  for (const m of recortar(outboundHistory(c.mensagens), sys)) {')
source = re.sub(r"    if \(Array.isArray\(conteudo\).*Mídia local ainda[^\n]+\r?\n", '', source, count=1)
# Raw legacy bytes stay local and unchanged. Projection is performed only for outbound requests.
function('mediaRecoverLegacyHistory', '''async function mediaRecoverLegacyHistory(owner) {
  // Keep legacy inline/local/ref history byte-for-byte; no automatic migration/upload.
  return;
}''')
source = re.sub(r"    if \(p\?\.type === 'input_audio'.*Mídia antiga precisa[^\n]+\r?\n",
                '    // Inline legacy media is allowed in local persistence; outboundHistory removes its payload.\n', source, count=1)
assert 'hasMedia = anexos.some' not in source
for name in ('iald.js','iald.css','index.html'):
    raw = source.encode('utf-8') if name == 'iald.js' else (HERE/name).read_bytes()
    with (OUT/name).open('xb') as f: f.write(raw)
    original = (HERE/'origin'/name).read_bytes().decode('utf-8')
    (OUT/(name+'.diff')).write_bytes(''.join(difflib.unified_diff(original.splitlines(True),raw.decode('utf-8').splitlines(True),fromfile='origin/'+name,tofile='R2/'+name)).encode('utf-8'))
print('R2 prepared; R1 untouched')
