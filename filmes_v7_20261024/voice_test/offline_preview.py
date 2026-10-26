"""Local-only reference ASR, Qwen synthesis, measurements and output ASR.

Run after download_models.py and isolated package installation. All network
connections are refused before importing inference libraries or reading audio.
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import socket
import subprocess
import sys
import time
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent
for key, value in {
    'HF_HOME': str(ROOT / 'hf_home'), 'HF_HUB_CACHE': str(ROOT / 'hf_cache'),
    'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
    'HF_HUB_DISABLE_TELEMETRY': '1', 'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1',
    'HF_TOKEN': '', 'HUGGING_FACE_HUB_TOKEN': '',
    'HF_TOKEN_PATH': str(ROOT / 'unused_token'), 'CUDA_VISIBLE_DEVICES': '',
    'OMP_NUM_THREADS': '8', 'MKL_NUM_THREADS': '8',
    'NUMBA_CACHE_DIR': str(ROOT / 'numba_cache'),
}.items():
    os.environ[key] = value

BLOCKED = []
def deny(*args, **kwargs):
    BLOCKED.append('connection_refused')
    raise RuntimeError('OFFLINE_SOCKET_GUARD: network is forbidden')

def audit(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto', 'socket.sendmsg'):
        deny()

sys.addaudithook(audit)
socket.socket.connect = deny
socket.socket.connect_ex = deny
socket.socket.sendto = deny
socket.create_connection = deny
socket.getaddrinfo = deny
try:
    socket.create_connection(('127.0.0.1', 9))
except RuntimeError:
    pass
assert len(BLOCKED) == 1
BLOCKED.clear()

FFMPEG = pathlib.Path(r'C:\IALD\Central de Patentes\work\mimo26_upgrade_20261020\media_dependency\ffmpeg.exe')

def pin(path):
    path = pathlib.Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': str(path), 'sha256': digest, 'bytes': path.stat().st_size}

def save(name, data):
    dest = ROOT / name
    temp = dest.with_suffix(dest.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(dest)

def progress(stage, **extra):
    old = json.loads((ROOT / 'PROGRESS.json').read_text(encoding='utf-8'))
    old.update(updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               stage=stage, **extra)
    save('PROGRESS.json', old)
    print(json.dumps({'stage': stage, **extra}, ensure_ascii=False), flush=True)

def ffmpeg(args):
    result = subprocess.run([str(FFMPEG), '-nostdin', '-hide_banner', *args],
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    return result.stderr

def transcribe(model, path, language):
    import soundfile as sf
    import numpy as np
    from scipy.signal import resample_poly
    import math
    data, sr = sf.read(path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    if sr != 16000:
        factor = math.gcd(sr, 16000)
        data = resample_poly(data, 16000 // factor, sr // factor)
    result = model({'raw': np.asarray(data, dtype=np.float32), 'sampling_rate': 16000},
                   return_timestamps=True, generate_kwargs={'language': language, 'task': 'transcribe'})
    rows = [{'start': c['timestamp'][0] or 0, 'end': c['timestamp'][1] or len(data)/16000,
             'text': c['text'], 'avg_logprob': None, 'no_speech_prob': None}
            for c in result.get('chunks', [])]
    return {'text': result['text'].strip(),
            'language': language, 'segments': rows,
            'statute': 'AUTOMATIC_ASR_NOT_PERCEPTUALLY_VERIFIED'}

def make_asr(path):
    import torch
    from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
    model = AutoModelForSpeechSeq2Seq.from_pretrained(path, local_files_only=True,
                                                     torch_dtype=torch.float32)
    processor = AutoProcessor.from_pretrained(path, local_files_only=True)
    return pipeline('automatic-speech-recognition', model=model,
                    tokenizer=processor.tokenizer, feature_extractor=processor.feature_extractor,
                    device='cpu', chunk_length_s=30, batch_size=1)

def words(text):
    text = ''.join(c for c in unicodedata.normalize('NFKD', text.lower())
                   if not unicodedata.combining(c))
    return re.findall(r'\w+', text)

def wer(reference, hypothesis):
    a, b = words(reference), words(hypothesis)
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        new = [i]
        for j, y in enumerate(b, 1):
            new.append(min(new[-1] + 1, row[j] + 1, row[j-1] + (x != y)))
        row = new
    return row[-1] / max(len(a), 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=['reference', 'synthesize', 'validate', 'all'], default='all')
    parser.add_argument('--model', default='Qwen/Qwen3-TTS-12Hz-1.7B-Base')
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT.parent))
    import mission
    projection = mission.project()
    task = next(t for t in projection['projection']['active'] if t['id'] == 'VOICE_PREVIEW')
    assert task['lease']['owner'] == 'codex-video-audio'
    preflight = mission.call({'operation': 'check', **mission.current('codex-video-audio'),
                              'task_id': 'VOICE_PREVIEW', 'lease_id': task['lease']['id']})
    assert preflight['ready'], preflight
    save('OWN_PREFLIGHT.json', preflight)
    progress('PREFLIGHT_PASS', revision=preflight['receipt']['revision'],
             lease_id=task['lease']['id'], preflight_ready=True,
             pending=['Offline CPU reference/synthesis stage requested', 'Measure WAV and compare output ASR'])
    import numpy as np
    import soundfile as sf
    import torch
    torch.set_num_threads(8)
    torch.set_num_interop_threads(2)
    scripts = json.loads((ROOT / 'SCRIPTS.json').read_text(encoding='utf-8-sig'))
    source = pathlib.Path(scripts['source_audio'])
    assert pin(source)['sha256'] == scripts['source_sha256']
    downloads = json.loads((ROOT / 'MODEL_DOWNLOADS.json').read_text(encoding='utf-8'))
    paths = {m['repo']: m['path'] for m in downloads['models']}
    if args.stage in ('reference', 'validate', 'all'):
        asr = make_asr(paths['openai/whisper-small'])
    if args.stage in ('reference', 'all'):
        progress('REFERENCE_ASR_OFFLINE', last_result='Socket guard active; CPU only.')
        full = ROOT / 'reference_mono16.wav'
        if not full.exists():
            ffmpeg(['-i', str(source), '-map', '0:a:0', '-ac', '1', '-ar', '16000',
                    '-af', 'volume=0.7', '-c:a', 'pcm_s16le', str(full)])
        transcript = transcribe(asr, full, 'pt')
        save('REFERENCE_FULL_ASR.json', transcript)
        candidates = []
        rows = transcript['segments']
        for i in range(len(rows)):
            for j in range(i, len(rows)):
                span = rows[j]['end'] - rows[i]['start']
                if 10 <= span <= 14.5:
                    selected = rows[i:j+1]
                    score = -abs(span - 12)
                    text = ' '.join(s['text'].strip() for s in selected)
                    if len(words(text)) >= 15:
                        candidates.append((score, rows[i]['start'], rows[j]['end'], text))
        if candidates:
            _, start, end, _ = max(candidates)
        else:
            start, end = 5.0, 17.0
        start = max(0.0, start - 0.15)
        end += 0.15
        ref = ROOT / 'reference_clip.wav'
        assert not ref.exists(), 'Reference exists: reuse it with --stage synthesize'
        ffmpeg(['-ss', str(start), '-i', str(source), '-t', str(end-start),
                '-map', '0:a:0', '-ac', '1', '-ar', '24000', '-af', 'volume=0.7',
                '-c:a', 'pcm_s16le', str(ref)])
        exact = transcribe(asr, ref, 'pt')
        assert len(words(exact['text'])) >= 10
        save('REFERENCE.json', {'source': pin(source), 'clip': pin(ref), 'start': start,
                               'seconds': end-start, 'transcript': exact,
                               'selection': 'ASR segment boundaries near 12 seconds; no perceptual audition or confidence claim'})
        progress('REFERENCE_READY', last_result='Local ASR reference clip and transcript saved.')
        del asr
    if args.stage in ('synthesize', 'all'):
        from qwen_tts import Qwen3TTSModel
        reference = json.loads((ROOT / 'REFERENCE.json').read_text(encoding='utf-8'))
        assert pin(reference['clip']['path']) == reference['clip']
        progress('LOADING_QWEN_CPU', model=args.model, last_result='Loading local weights with socket guard.')
        started = time.monotonic()
        model = Qwen3TTSModel.from_pretrained(paths[args.model], device_map='cpu',
                    dtype=torch.float32, attn_implementation='sdpa', local_files_only=True, token=False)
        prompt = model.create_voice_clone_prompt(ref_audio=reference['clip']['path'],
                    ref_text=reference['transcript']['text'], x_vector_only_mode=False)
        for language, item in scripts['samples'].items():
            raw = ROOT / ('preview_' + language + '_raw.wav')
            if raw.exists():
                continue
            progress('SYNTHESIZING_' + language.upper(), last_result='Generating exact SCRIPTS.json text locally.')
            torch.manual_seed(73)
            t0 = time.monotonic()
            with torch.inference_mode():
                wavs, sr = model.generate_voice_clone(text=item['text'], language=item['language'],
                           voice_clone_prompt=prompt, max_new_tokens=1200)
            waveform = np.asarray(wavs[0], dtype=np.float32)
            assert np.isfinite(waveform).all() and len(waveform) > sr
            sf.write(raw, waveform, sr, subtype='FLOAT')
            save('GENERATION_' + language + '.json', {'model': args.model,
                 'model_path': paths[args.model], 'text': item['text'], 'scripts': pin(ROOT / 'SCRIPTS.json'),
                 'raw': pin(raw), 'sample_rate': sr, 'seconds': len(waveform)/sr,
                 'elapsed_seconds': time.monotonic()-t0, 'device': 'cpu', 'threads': 8,
                 'dtype': 'float32', 'ref_text': reference['transcript']['text'],
                 'reference': pin(ROOT / 'REFERENCE.json'), 'socket_blocked_attempts': len(BLOCKED)})
            progress('GENERATED_' + language.upper(), last_result='Raw WAV saved; awaiting loudness and ASR checks.')
        del model, prompt
    if args.stage in ('validate', 'all'):
        if args.stage == 'all':
            asr = make_asr(paths['openai/whisper-small'])
        results = []
        for language, item in scripts['samples'].items():
            raw = ROOT / ('preview_' + language + '_raw.wav')
            final = ROOT / ('preview_' + language + '.wav')
            progress('VALIDATING_' + language.upper(), last_result='Measuring local WAV and comparing automatic output ASR.')
            before = ffmpeg(['-i', str(raw), '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'])
            measurement = json.loads(before[before.rfind('{'):before.rfind('}')+1])
            filt = ('loudnorm=I=-16:TP=-2:LRA=11:linear=true:measured_I={input_i}:'
                    'measured_LRA={input_lra}:measured_TP={input_tp}:measured_thresh={input_thresh}:'
                    'offset={target_offset}').format(**measurement)
            if not final.exists():
                ffmpeg(['-i', str(raw), '-af', filt, '-ar', '24000', '-c:a', 'pcm_s24le', str(final)])
            after = ffmpeg(['-i', str(final), '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'])
            measured = json.loads(after[after.rfind('{'):after.rfind('}')+1])
            audio, sr = sf.read(final)
            peak = float(np.max(np.abs(audio)))
            transcript = transcribe(asr, final, language)
            error = wer(item['text'], transcript['text'])
            result = {'language': language, 'wav': pin(final), 'script_text': item['text'],
                      'asr': transcript, 'word_error_rate': error, 'seconds': len(audio)/sr,
                      'sample_rate': sr, 'sample_peak': peak, 'loudness': measured,
                      'no_clipping': peak < 1 and float(measured['input_tp']) < 0,
                      'automatic_text_similarity_pass': error <= 0.35,
                      'perceptually_auditioned': False}
            save('VALIDATION_' + language + '.json', result)
            results.append(result)
        passed = all(x['no_clipping'] and x['automatic_text_similarity_pass'] for x in results)
        manifest = {'status': 'TECHNICAL_PASS_AWAITING_HUMAN_LISTENING' if passed else 'NEEDS_REVIEW',
                    'source': pin(source), 'scripts': pin(ROOT / 'SCRIPTS.json'),
                    'reference': pin(ROOT / 'REFERENCE.json'), 'models': pin(ROOT / 'MODEL_DOWNLOADS.json'),
                    'environment': pin(ROOT / 'ENVIRONMENT.json'),
                    'asr_engine': 'openai/whisper-small via transformers, CPU float32',
                    'generation_receipts': [pin(ROOT / ('GENERATION_' + lang + '.json')) for lang in scripts['samples']],
                    'validation_script': pin(__file__),
                    'outputs': results, 'inference_network': {'HF_HUB_OFFLINE': True,
                    'TRANSFORMERS_OFFLINE': True, 'socket_guard': True, 'guard_selftest_passed': True,
                    'blocked_attempts': len(BLOCKED), 'voice_uploads': 0},
                    'films_modified': False, 'human_similarity_judgment': 'PENDING',
                    'limits': ['ASR is automated, not verified by listening.',
                               'No claim of perceptual speaker similarity or naturalness.',
                               'Socket guard is process-level, not an OS firewall. No inference service used.']}
        save('LOCAL_ONLY_MANIFEST.json', manifest)
        progress(manifest['status'], last_result='Two local WAVs and technical measurements ready.', pending=['Human listening and quality approval'])

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        progress('FAILED_LOCAL', last_result=type(exc).__name__ + ': ' + str(exc)[:600])
        raise
