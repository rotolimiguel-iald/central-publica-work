from pathlib import Path
p=Path(r'C:/IALD/Central de Patentes/work/app_attachments_beta_wait_20261021/repair')
s=(p/'baseline/iald_app_providers.py').read_text(encoding='utf-8')
helper=r'''def admission_input_bound(payload):
    """ESTIMATED local admission, NOT measured MiMo tokens or a vendor guarantee.

    Text/science/tools stay byte-counted in full. Only validated typed inline
    images are counted separately: 16px patches WITHOUT merge discount + 20% + 1024/frame.
    Grounding: XiaomiMiMo/MiMo-V2.6-Pro-MOPD config processor patch_size=16,
    merge_size=2, image_min_pixels=8192, image_max_pixels=8388608. MOPD is
    open weights, NOT an API tokenizer contract. No input pixel cap/downscale
    is assumed: count original geometry even above the MOPD max.
    This deliberately loose engineering estimate must be reviewed against usage;
    it is not a tokenizer. Wire JSON and image bytes are NEVER transformed.
    """
    import io
    import warnings
    from PIL import Image
    image_tokens = 0

    def image(url):
        nonlocal image_tokens
        if not isinstance(url, str) or ';base64,' not in url:
            raise ValueError('Invalid inline image for admission')
        header, encoded = url.split(';base64,', 1)
        if header not in ('data:image/png', 'data:image/jpeg', 'data:image/gif', 'data:image/webp') or len(encoded) > 10666668:
            raise ValueError('Unsupported or oversized image for admission')
        try:
            raw = base64.b64decode(encoded, validate=True)
            if not 0 < len(raw) <= 8000000:
                raise ValueError('Image byte budget exceeded')
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(raw)) as im:
                    expected = {'PNG':'data:image/png', 'JPEG':'data:image/jpeg', 'GIF':'data:image/gif', 'WEBP':'data:image/webp'}
                    if expected.get(im.format) != header:
                        raise ValueError('Image signature/MIME mismatch')
                    im.verify()
                pixels, estimate, frames = 0, 0, 0
                with Image.open(io.BytesIO(raw)) as im:
                    while True:
                        width, height = im.size
                        pixels += width * height
                        frames += 1
                        if width <= 0 or height <= 0 or pixels > 25000000 or frames > 256:
                            raise ValueError('Image geometry/frame safety budget exceeded')
                        im.load()  # Refuse truncated/corrupt files, not just a plausible header.
                        estimate += max(32, ((width + 15)//16)*((height + 15)//16)) + 1024
                        try: im.seek(frames)
                        except EOFError: break
            image_tokens += (estimate * 120 + 99)//100
        except (ValueError, OSError, SyntaxError, binascii.Error, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
            raise ValueError('Image geometry or bytes could not be validated') from exc
        return ''

    # Traverse only the supported message content slot. Unknown fields remain
    # fully counted; never subtract arbitrary strings resembling media elsewhere.
    counted = dict(payload)
    if isinstance(payload.get('messages'), list):
        counted['messages'] = []
        for message in payload['messages']:
            if not isinstance(message, dict) or not isinstance(message.get('content'), list):
                counted['messages'].append(message)
                continue
            parts, count = [], 0
            for part in message['content']:
                if isinstance(part, dict) and part.get('type') == 'image_url':
                    if set(part) != {'type', 'image_url'} or not isinstance(part['image_url'], dict) or set(part['image_url']) != {'url'}:
                        raise ValueError('Invalid typed image shape')
                    count += 1
                    if count > 3 or message.get('role') != 'user':
                        raise ValueError('Invalid image count or role')
                    parts.append({'type':'image_url', 'image_url':{'url':image(part['image_url']['url'])}})
                else:
                    parts.append(part)
            counted['messages'].append({**message, 'content':parts})
    return len(json.dumps(counted, ensure_ascii=False, allow_nan=False).encode('utf-8')) + image_tokens


'''
s=s.replace('def output_budget(payload, maximum):',helper+'def output_budget(payload, maximum):',1)
s=s.replace("used = len(json.dumps(payload, ensure_ascii=False).encode('utf-8'))",'used = admission_input_bound(payload)')
# Pillow is imported lazily ONLY when typed images exist, preserving text-only dependency semantics.
s=s.replace('    from PIL import Image\n    image_tokens', '    image_tokens')
s=s.replace('        nonlocal image_tokens\n', '        nonlocal image_tokens\n        from PIL import Image\n',1)
(p/'stage/iald_app_providers.py').write_bytes(s.replace('\n','\r\n').encode())
# Retain explicit server admission refusal even when durable job is failed.
f=p/'stage/app/iald.js';j=f.read_text(encoding='utf-8');j=j.replace("      deliveryNotice = failure?.terminal ? {", "      deliveryNotice = failure?.terminal && aviso && aviso.tipo !== 'em_andamento'\n        ? { ...aviso, retirar_resposta: true } : failure?.terminal ? {",1)
j=j.replace('      await submit(record, scope, signal);', '''      try { await submit(record, scope, signal); }
      catch (error) {
        // Only a verified local intent with no attempt can mean not submitted.
        try {
          if (!error.detached && current(scope) && !record.id && !record.attempted &&
              read(scope.owner).some(r => r.request_id === record.request_id && r.attempted === false)) error.notSubmitted = true;
        } catch (_) { /* Unreadable intent is uncertainty, never permission to retry. */ }
        throw error;
      }''',1)
f.write_bytes(j.replace('\n','\r\n').encode())
print('backend stage and frontend refusal handling prepared')
