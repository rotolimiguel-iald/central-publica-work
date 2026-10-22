from pathlib import Path
import json, hashlib, subprocess, sys

APP = Path(r'C:\IALD\projetos_pyhton\IALD')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
WORK = Path(__file__).resolve().parent
GIT = r'C:\Program Files\Git\cmd\git.exe'
def git(*args):
    return subprocess.check_output([GIT, '-C', str(REPO), *args])
def digest(raw): return hashlib.sha256(raw).hexdigest()
def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == raw, str(path)
    else:
        with path.open('xb') as f: f.write(raw)
    assert path.read_bytes() == raw

if __name__ == '__main__':
    commit = git('rev-parse','HEAD').decode().strip()
    tracked = git('ls-tree','-r','--name-only','-z',commit).decode().split('\0')
    chosen = [n for n in tracked if n.endswith(('um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','um_absoluto_forma_canonica.md'))]
    for name in chosen:
        raw = git('show',commit+':'+name)
        save(WORK/'inspect'/name, raw)
        print(name, len(raw), digest(raw))
        if name.endswith('um_absoluto.json'):
            data = json.loads(raw); old = json.loads(Path(json.loads((APP/'iald_nucleo_fixo.json').read_bytes())['published_evidence']['result']['path']).read_bytes())
            new = {k:v for k,v in data['core'].items() if k not in old['core']}
            save(WORK/'new_sections.json',json.dumps(new,ensure_ascii=False,indent=2).encode())
            print('New sections',[(k,len(json.dumps(v))) for k,v in new.items()])
        if name.endswith('um_absoluto_selo.json'):
            s=json.loads(raw)
            print('seal',s['um_version'],s['timestamp'],s['fail_closed_selftest'])
    save(WORK/'source_commit.txt',commit.encode())
    print('COMMIT',commit)
