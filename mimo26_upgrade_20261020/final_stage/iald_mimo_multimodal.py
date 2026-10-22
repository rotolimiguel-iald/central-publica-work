"""Inline media boundary. Local probe only; never fetch remote media."""
import base64
import binascii
import hashlib
import io
import json
import math
import subprocess
import tempfile
from pathlib import Path
import wave

MAX_BYTES = 512_000  # Explicit conservative app budget, not vendor maximum.
MAX_AUDIO_SECONDS = 30
MAX_VIDEO_SECONDS = 10
VENDOR = Path(__file__).resolve().parent / 'vendor' / 'ffmpeg'


def _expected_decoder_hash():
    """Manifest schema: {\"files\": {\"ffprobe.exe\": \"64 lowercase hex\"}}."""
    manifest = VENDOR / 'manifest.json'
    if manifest.stat().st_size > 65536:
        raise ValueError('Decoder manifest exceeds limit')
    data = json.loads(manifest.read_text(encoding='utf-8'))
    files = data.get('files')
    pin = files.get('ffprobe.exe') if isinstance(files,dict) else None
    if not isinstance(pin,str) or len(pin)!=64 or any(c not in '0123456789abcdef' for c in pin):
        raise ValueError('Decoder manifest hash invalid')
    return pin


def _copy_verified_decoder(destination=None):
    """Hash the same bytes copied to a private execution snapshot; no PATH fallback."""
    expected = _expected_decoder_hash()
    digest = hashlib.sha256()
    with (VENDOR / 'ffprobe.exe').open('rb') as source:
        if destination is None:
            for block in iter(lambda: source.read(1024*1024),b''): digest.update(block)
        else:
            with Path(destination).open('xb') as target:
                for block in iter(lambda: source.read(1024*1024),b''):
                    digest.update(block); target.write(block)
    if digest.hexdigest() != expected:
        raise ValueError('Decoder integrity mismatch; nothing sent')
    return expected


def decoder_capabilities():
    """Host readiness only, never consent. Recheck on every actual invocation."""
    try:
        _copy_verified_decoder()
        ready, reason = True, 'verified'
    except (OSError,ValueError,TypeError,AttributeError):
        ready, reason = False, 'decoder_missing_or_unverified'
    return dict(wav=True, decoder_ready=ready, reason=reason,
        audio_extensions=['wav','mp3','flac','ogg','m4a'] if ready else ['wav'],
        video_extensions=['mp4','mov','avi','wmv'] if ready else [],
        max_bytes=MAX_BYTES, max_audio_seconds=MAX_AUDIO_SECONDS, max_video_seconds=MAX_VIDEO_SECONDS)


def media_capabilities():
    """Public capability shape: no filesystem paths, executable names or hashes."""
    state = decoder_capabilities()
    return dict(audio=True, video=state['decoder_ready'],
        audio_formats=state['audio_extensions'], video_formats=state['video_extensions'],
        max_media_bytes=MAX_BYTES, max_audio_seconds=MAX_AUDIO_SECONDS,
        max_video_seconds=MAX_VIDEO_SECONDS, max_media_per_message=1)


def probe_media(raw, kind):
    if kind == 'audio/wav':
        with wave.open(io.BytesIO(raw)) as w:
            return {'duration': w.getnframes()/w.getframerate(), 'types': ['audio']}
    with tempfile.TemporaryDirectory(prefix='iald_media_') as directory:
        executable = Path(directory)/'ffprobe.exe'
        try:
            _copy_verified_decoder(executable)
        except (OSError,ValueError,TypeError,AttributeError):
            raise ValueError('Local media validation unavailable or unverified; nothing sent') from None
        path = Path(directory)/'input.bin'
        path.write_bytes(raw)
        process = subprocess.run([str(executable), '-v', 'error', '-protocol_whitelist', 'file',
            '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', str(path)],
            capture_output=True, timeout=5, check=True, creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        info = json.loads(process.stdout)
    return {'duration': float(info['format']['duration']),
            'types': [s['codec_type'] for s in info.get('streams',[])]}


def media_part(part, *, media_authorized=False, probe=probe_media):
    if media_authorized is not True:
        raise ValueError('MiMo media consent required')
    if not isinstance(part,dict) or part.get('type') not in ('input_audio','video_url'):
        raise ValueError('Unsupported media')
    kind = part['type']
    if set(part) != {'type',kind} or not isinstance(part[kind],dict):
        raise ValueError('Invalid media object')
    field = 'data' if kind == 'input_audio' else 'url'
    if set(part[kind]) != {field}: raise ValueError('Invalid media fields')
    url = part[kind][field]
    if not isinstance(url,str) or ';base64,' not in url: raise ValueError('Inline media required')
    header, encoded = url.split(';base64,',1)
    if len(encoded) > 4*((MAX_BYTES+2)//3): raise ValueError('Media byte budget exceeded')
    try: raw = base64.b64decode(encoded,validate=True)
    except (ValueError,binascii.Error): raise ValueError('Invalid media base64') from None
    mime = header.removeprefix('data:')
    valid = {
        'audio/wav':raw[:4]==b'RIFF' and raw[8:12]==b'WAVE',
        'audio/mpeg':raw.startswith(b'ID3') or len(raw)>1 and raw[0]==255 and raw[1]&224==224,
        'audio/flac':raw.startswith(b'fLaC'), 'audio/ogg':raw.startswith(b'OggS'),
        'audio/mp4':raw[4:8]==b'ftyp', 'video/mp4':raw[4:8]==b'ftyp',
        'video/quicktime':raw[4:8]==b'ftyp',
        'video/x-msvideo':raw[:4]==b'RIFF' and raw[8:12]==b'AVI ',
        'video/x-ms-wmv':raw.startswith(bytes.fromhex('3026b2758e66cf11a6d900aa0062ce6c')),
    }
    expected = 'audio' if kind=='input_audio' else 'video'
    if not header.startswith('data:') or not mime.startswith(expected+'/') or not valid.get(mime) or not 0<len(raw)<=MAX_BYTES:
        raise ValueError('Media MIME/signature mismatch')
    info = probe(raw,mime)
    duration = info['duration']
    ceiling = MAX_AUDIO_SECONDS if expected=='audio' else MAX_VIDEO_SECONDS
    if isinstance(duration,bool) or not isinstance(duration,(int,float)) or not math.isfinite(duration) or not 0<duration<=ceiling:
        raise ValueError('Media duration exceeded or unknown')
    if expected not in info['types'] or expected=='audio' and 'video' in info['types']:
        raise ValueError('Media stream mismatch')
    return {'type':kind,kind:{field:url}}
