"""GET-only public model download; never reads reference audio or credentials."""
import concurrent.futures
import hashlib
import json
import pathlib
import urllib.request
import sys

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / 'hf_cache'

def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)

def download(repo):
    info = get_json('https://huggingface.co/api/models/' + repo + '?blobs=true')
    revision = info['sha']
    target = CACHE / ('models--' + repo.replace('/', '--')) / 'snapshots' / revision
    target.mkdir(parents=True, exist_ok=True)
    records = []
    for item in info['siblings']:
        name = item['rfilename']
        if name == '.gitattributes':
            continue
        if repo.startswith('openai/') and not (name.endswith('.json') or name in ('model.safetensors', 'merges.txt', 'normalizer.json', 'README.md')):
            continue
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        url = 'https://huggingface.co/' + repo + '/resolve/' + revision + '/' + name
        expected = item.get('lfs', {}).get('sha256')
        if not dest.exists():
            print(json.dumps({'downloading': repo, 'file': name}), flush=True)
            partial = dest.with_suffix(dest.suffix + '.part')
            with urllib.request.urlopen(url, timeout=120) as response, partial.open('wb') as out:
                while block := response.read(4 * 1024 * 1024):
                    out.write(block)
            partial.replace(dest)
        digest = hashlib.file_digest(dest.open('rb'), 'sha256').hexdigest()
        if expected and digest != expected:
            raise RuntimeError('Model hash mismatch: ' + name)
        records.append({'path': str(dest), 'sha256': digest, 'bytes': dest.stat().st_size,
                        'expected_lfs_sha256': expected, 'url': url})
    return {'repo': repo, 'revision': revision, 'path': str(target), 'files': records}

if __name__ == '__main__':
    repos = sys.argv[1:] or ['Qwen/Qwen3-TTS-12Hz-1.7B-Base', 'Systran/faster-whisper-small']
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        models = list(pool.map(download, repos))
    old = ROOT / 'MODEL_DOWNLOADS.json'
    if old.exists():
        previous = json.loads(old.read_text())['models']
        models = [m for m in previous if m['repo'] not in repos] + models
    result = {'status': 'DOWNLOADED_HASH_VERIFIED', 'uploads': 0, 'models': models}
    (ROOT / 'MODEL_DOWNLOADS.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'models': [m['repo'] for m in models]}), flush=True)
