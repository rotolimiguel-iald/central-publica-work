"""Staging-only image boundary. No network, vault or scientific-memory edits."""
import base64
import binascii


def request_media(client):
    """Public router projection: latest prompt plus media kinds/counts, no URLs."""
    import re
    counts = {'image':0,'audio':0,'video':0}
    encoded_bytes = 0
    prompt = ''
    if not isinstance(client,list): raise ValueError('Invalid message list')
    for message in client:
        if not isinstance(message,dict): raise ValueError('Invalid message')
        if message.get('role') not in ('user','assistant'): continue
        content = message.get('content')
        texts=[]
        if isinstance(content,str): texts=[content]
        elif isinstance(content,list):
            for part in content:
                if not isinstance(part,dict): raise ValueError('Invalid part')
                kind=part.get('type')
                if kind=='text':
                    if not isinstance(part.get('text'),str): raise ValueError('Invalid text')
                    texts.append(part['text'])
                elif kind in ('image_url','input_audio','video_url'):
                    key={'image_url':'image','input_audio':'audio','video_url':'video'}[kind]
                    counts[key]+=1
                    field='data' if kind=='input_audio' else 'url'
                    obj=part.get(kind)
                    value=obj.get(field) if isinstance(obj,dict) else None
                    if not isinstance(value,str): raise ValueError('Invalid media')
                    encoded_bytes+=len(value.encode('utf-8'))
                else: raise ValueError('Unsupported part')
        else: raise ValueError('Invalid content')
        if message.get('role')=='user':
            prompt=re.sub(r'\[ARQUIVO:[^\n]*\][\s\S]*?\[FIM\]','', '\n'.join(texts)).strip()
    return dict(kinds=[key for key,value in counts.items() if value],prompt=prompt,counts=counts,encoded_bytes=encoded_bytes)


def metric_task(messages):
    """Classify the latest user text on the host; never accept client task labels."""
    import re
    from iald_task_policy import classify
    for message in reversed(messages):
        if isinstance(message, dict) and message.get('role') == 'user':
            content = message.get('content')
            text = content if isinstance(content,str) else '\n'.join(
                p['text'] for p in content if isinstance(p,dict) and p.get('type')=='text' and isinstance(p.get('text'),str)) if isinstance(content,list) else ''
            text = re.sub(r'\[ARQUIVO:[^\n]*\][\s\S]*?\[FIM\]', '', text)
            return classify(text)
    return classify('')


def transport_response_format(mode=None):
    """Opt-in JSON object only; not an assertion of JSON Schema enforcement."""
    if mode is None:
        return {}
    if mode != 'json_object':
        raise ValueError('Unsupported response format')
    return {'response_format': {'type': 'json_object'}}


def transport_tool_options(provider, offered, round_no, rounds):
    """MiMo ignores tool_choice=none: omit tool definitions in final round."""
    if not offered or (provider == 'mimo' and round_no == rounds - 1):
        return {}
    return dict(tools=offered, tool_choice='none' if round_no == rounds - 1 else 'auto')


def image_parts(parts, *, images_authorized=False, media_authorized=False):
    """Server authorization must follow versioned MiMo image consent.

    Uses the existing Claude attachment signature detector, injected only when
    called. Never calls its permissive URL/marker conversion.
    """
    if images_authorized is not True:
        raise ValueError('MiMo image consent required')
    if not isinstance(parts, list) or not 1 <= len(parts) <= 16:
        raise ValueError('Invalid attachment parts')
    from iald_motor_claude import _tipo_pelos_bytes
    result, count, total = [], 0, 0
    for part in parts:
        if not isinstance(part, dict):
            raise ValueError('Invalid attachment part')
        if part.get('type') in ('input_audio','video_url'):
            from iald_mimo_multimodal import media_part
            if any(p.get('type') in ('input_audio','video_url') for p in result):
                raise ValueError('One audio/video attachment per message')
            result.append(media_part(part,media_authorized=media_authorized))
            continue
        if part.get('type') == 'text' and set(part) == {'type', 'text'}:
            if not isinstance(part['text'], str):
                raise ValueError('Invalid attachment text')
            result.append(dict(part))
            continue
        if set(part) != {'type', 'image_url'} or part.get('type') != 'image_url':
            raise ValueError('Unsupported media part')
        image = part['image_url']
        if not isinstance(image, dict) or set(image) != {'url'}:
            raise ValueError('Invalid image object')
        url = image['url']
        if not isinstance(url, str) or not url.startswith('data:image/') or ';base64,' not in url:
            raise ValueError('Only inline images accepted')
        header, data = url.split(';base64,', 1)
        if len(data) > 10_666_668:
            raise ValueError('Image exceeds local attachment limit')
        try:
            raw = base64.b64decode(data, validate=True)
        except (ValueError, binascii.Error):
            raise ValueError('Invalid image base64') from None
        mime = _tipo_pelos_bytes(data)
        if not raw or mime is None or header != 'data:' + mime:
            raise ValueError('Image type mismatch or unsupported format')
        count += 1
        total += len(raw)
        if count > 3 or len(raw) > 8_000_000 or total > 24_000_000:
            raise ValueError('Image attachment budget exceeded')
        result.append({'type': 'image_url', 'image_url': {'url': url}})
    return result
