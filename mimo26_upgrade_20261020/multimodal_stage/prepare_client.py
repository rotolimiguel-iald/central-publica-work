from pathlib import Path
import difflib
import hashlib
import json
root=Path(__file__).parent
source=Path('C:/IALD/projetos_pyhton/IALD/app/iald.js')
raw=source.read_bytes()
original=raw.decode('utf-8')
text=original.replace('function desenharAnexos() {',(root/'client_media.js').read_text(encoding='utf-8')+'\nfunction desenharAnexos() {',1)
text=text.replace('    if (a.image) {', '''    if (a.media) {
      const player = el(a.mediaKind);
      player.controls = true; player.preload = 'metadata'; player.src = a.media;
      item.appendChild(player);
    } else if (a.image) {''',1)
text=text.replace(': a.image ? `${a.kb} KB`', ': (a.image || a.media) ? `${a.kb} KB`',1)
text=text.replace("  botao.dataset.semImagem = permitidas ? '' : '1';", "  const extrasMidia = ['audio','video'].flatMap(tipo => midiaPermitida(tipo) ? extensoesMidia(tipo).map(ext => '.'+ext) : []);\n  if (extrasMidia.length) campo.setAttribute('accept', campo.getAttribute('accept') + ',' + extrasMidia.join(','));\n  botao.dataset.semImagem = permitidas ? '' : '1';",1)
text=text.replace("    const ehPdf = /\\.pdf$/i.test(f.name);", """    const ehPdf = /\\.pdf$/i.test(f.name);
    const tipoMidia = /\\.(wav|mp3|flac|ogg|m4a)$/i.test(f.name) ? 'audio'
      : /\\.(mp4|mov|avi|wmv)$/i.test(f.name) ? 'video' : null;
    if (tipoMidia) {
      if (S.anexos.some(a => a.media)) { avisar('Uma mídia de áudio/vídeo por mensagem.'); continue; }
      try { S.anexos.push(await lerMidiaLocal(f,tipoMidia)); desenharAnexos(); }
      catch (e) { avisar(e.message); }
      continue;
    }
    if (/^(audio|video)\\//.test(f.type)) { avisar('Formato de mídia não integrado.'); continue; }""",1)
text=text.replace("  const arquivos = anexos.filter((a) => !a.image && a.content);", """  if (anexos.some(a => a.media && !midiaPermitida(a.mediaKind))) {
    avisar('Mídia indisponível: selecione MiMo e confira o consentimento.'); return;
  }
  const midias = anexos.filter(a => a.media).map(a => a.mediaKind === 'audio'
    ? {type:'input_audio',input_audio:{data:a.media}}
    : {type:'video_url',video_url:{url:a.media}});
  const arquivos = anexos.filter((a) => !a.image && !a.media && a.content);""",1)
text=text.replace('  if (imagens.length) {','  if (imagens.length || midias.length) {',1)
text=text.replace("    return (imgs ? `[${imgs} imagem(ns) anexada(s)]\\n` : '') + t;", "    const audios = conteudo.filter(p => p?.type === 'input_audio').length;\n    const videos = conteudo.filter(p => p?.type === 'video_url').length;\n    return (audios ? `[${audios} áudio(s) anexado(s)]\\n` : '') + (videos ? `[${videos} vídeo(s) anexado(s)]\\n` : '') + (imgs ? `[${imgs} imagem(ns) anexada(s)]\\n` : '') + t;",1)
text=text.replace("      .concat([{ type: 'text', text: conteudo }]);","      .concat(midias).concat([{ type: 'text', text: conteudo }]);",1)
# Keep history media intact even if capability later changes; server refuses visibly.
text=text.replace("    const conteudo = (semImagens && Array.isArray(m.content)) ? textoDe(m.content) : m.content;", "    const conteudo = m.content;",1)
assert text != original
(root/'app').mkdir(exist_ok=True)
(root/'app'/'iald.js').write_text(text,encoding='utf-8',newline='')
(root/'client.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='a/app/iald.js',tofile='b/app/iald.js')),encoding='utf-8')
(root/'client_receipt.json').write_text(json.dumps({'source_sha256':hashlib.sha256(raw).hexdigest(),'production_unchanged':source.read_bytes()==raw,'runtime_browser_tested':False}),encoding='utf-8')
