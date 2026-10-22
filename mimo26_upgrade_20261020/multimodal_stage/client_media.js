// Staging R3: local inline media only; server consent and validation authoritative.
function midiaPermitida(tipo) {
  return limitesDoPlano()?.[tipo] === true;
}

function extensoesMidia(tipo) {
  const caps = limitesDoPlano()?.media_capabilities;
  const values = tipo === 'audio' ? caps?.audio_formats : caps?.video_formats;
  return Array.isArray(values) ? values : [];
}

async function lerMidiaLocal(f, tipo) {
  if (!midiaPermitida(tipo)) throw new Error('Áudio/vídeo requer MiMo e consentimento atualizado.');
  if (f.size > 512000) throw new Error('Limite local de 512 KB por mídia. Mesmo abaixo dele, a conversa pode exceder o contexto; a memória TGL será preservada e o envio recusado.');
  const extension = f.name.split('.').pop().toLowerCase();
  if (!extensoesMidia(tipo).includes(extension)) throw new Error('Validação deste formato indisponível no servidor. WAV não requer decoder externo.');
  const mime = ({ wav:'audio/wav',mp3:'audio/mpeg',flac:'audio/flac',ogg:'audio/ogg',m4a:'audio/mp4',
    mp4:'video/mp4',mov:'video/quicktime',avi:'video/x-msvideo',wmv:'video/x-ms-wmv' })[f.name.split('.').pop().toLowerCase()];
  if (!mime || !mime.startsWith(tipo + '/')) throw new Error('Formato de mídia não permitido.');
  const local = URL.createObjectURL(f);
  try {
    const duration = await new Promise((resolve,reject) => {
      const player = document.createElement(tipo);
      const timer = setTimeout(() => { cleanup(); reject(new Error('Não foi possível conferir a duração.')); },5000);
      function cleanup() { clearTimeout(timer); player.onloadedmetadata=null; player.onerror=null; player.removeAttribute('src'); player.load(); }
      player.preload='metadata';
      player.onloadedmetadata=() => { const d=player.duration; cleanup(); resolve(d); };
      player.onerror=() => { cleanup(); reject(new Error('Formato não reconhecido neste aparelho.')); };
      player.src=local;
    });
    if (!Number.isFinite(duration) || duration<=0 || duration>(tipo==='audio'?30:10))
      throw new Error('Duração máxima: áudio 30 s; vídeo 10 s.');
    const data = await lerComo(new Blob([f],{type:mime}),'dataURL');
    return {name:f.name,media:data,mediaKind:tipo,kb:Math.round(f.size/1024),duration};
  } finally { URL.revokeObjectURL(local); }
}
