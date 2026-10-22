"""Local extracted logging functions only; no legacy mission imports or admission."""
import hashlib,json,os,re,subprocess,time,uuid
import datetime as dt
from pathlib import Path

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(path):
    return {'path': str(path), 'sha256': digest(path)}

def save(path, value):
    path = Path(path)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == data
    os.rename(temporary, path)

def safe_line(text):
    # Raw bytes are hashed in memory, never persisted. Sensitive-looking output
    # is omitted before UTF-8 custody, including multi-line private key content.
    if re.search(r'(?i)(password|passwd|storepass|keypass|authorization|bearer\s|token\s*[=:]|api[_-]?key|private key|keystore\.properties|\.jks\b|\.keystore\b)', text):
        return '[sensitive-looking build output omitted]\n', True
    if re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,})', text):
        return '[credential-shaped build output omitted]\n', True
    return text, False

def collect(command, *, cwd, env, label, attempt):
    log = attempt / (label + '.utf8.log')
    raw_hash = hashlib.sha256()
    raw_size = 0
    filtered = 0
    errors = []
    key_block = False
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, shell=False)
    save(attempt / (label + '.started.json'), {
        'pid': process.pid, 'command': command, 'cwd': str(cwd),
        'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'no_repeat': True})
    with log.open('xb') as output:
        for raw in iter(process.stdout.readline, b''):
            raw_hash.update(raw)
            raw_size += len(raw)
            text = raw.decode('utf-8', errors='replace')
            if '-----BEGIN ' in text and 'PRIVATE KEY-----' in text:
                key_block = True
            end_block = '-----END ' in text and 'PRIVATE KEY-----' in text
            if key_block:
                clean, omitted = '[private-key block omitted]\n', True
            else:
                clean, omitted = safe_line(text)
            if end_block:
                key_block = False
            filtered += int(omitted)
            output.write(clean.encode('utf-8'))
            output.flush()
            if re.search(r'(?i)(error|failure|exception|failed|what went wrong|sensitive-looking|omitted)', clean):
                errors.append(clean.rstrip()[:1200])
        os.fsync(output.fileno())
    code = process.wait()
    result = {'exit_code': code, 'seconds': time.monotonic() - started,
              'log': pin(log), 'raw_stream_sha256': raw_hash.hexdigest(),
              'raw_stream_bytes': raw_size, 'raw_stream_persisted': False,
              'filtered_lines': filtered, 'errors': errors[-40:]}
    save(attempt / (label + '.receipt.json'), result)
    return result
