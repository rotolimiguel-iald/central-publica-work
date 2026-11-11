"""Receipt and allowlist guards shared by publication candidates."""
import re
from pathlib import Path
from prepare_mobile import HERE, REPO, read, require, sha, report
from release_controls import APP, D, release_installed

FILES = {'www/iald.js','www/owner_office.js','ios/App/App/public/iald.js',
         'ios/App/App/public/owner_office.js','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle'}

def pin(path):
    return {'path':str(path),'sha256':sha(path.read_bytes())}

def receipt(item):
    path = Path(item['path']).resolve(strict=True)
    require(path.is_relative_to(HERE.parent), 'Receipt outside mission')
    require(sha(path.read_bytes())==item['sha256'], 'Receipt drift')
    return read(path)

def checked(phase):
    authorization = read(HERE/'PARENT_PUBLICATION_READY.json')
    require(authorization.get('parent')=='codex-app-scroll-01a094df' and
            authorization.get('status')=='PUBLICATION_AUTHORIZED' and
            phase in authorization.get('phases',[]), 'Parent phase authorization missing')
    require(authorization['plan_sha256']==sha((HERE/'PLAN.json').read_bytes()), 'Plan drift')
    # Pin the executable closure so a later edit requires a new parent review.
    scripts = {'publication_guards.py','publish_apk42.py','git_release42.py',
               'release_controls.py','prepare_mobile.py'}
    require(set(authorization['script_pins'])==scripts, 'Script pin allowlist mismatch')
    for name,digest in authorization['script_pins'].items():
        require(sha((HERE/name).read_bytes())==digest, 'Publication script changed')
    review = receipt(authorization['workflow_review'])
    require(review.get('status')=='PASS' and review.get('reviewer') and
            review.get('script_pins')==authorization['script_pins'], 'Workflow review missing')
    installed = release_installed()  # exact client review + actual installed bytes
    plan = read(HERE/'PLAN.json')
    require(set(plan['tracked_files'])==FILES and len(plan['tracked_files'])==6, 'Six-file allowlist mismatch')
    install = receipt(authorization['install'])
    require(install.get('status')=='PASS' and install.get('plan_sha256')==authorization['plan_sha256'] and
            install.get('installed')=={r['target']:r['new'] for r in plan['rows']}, 'Install receipt mismatch')
    audit = receipt(authorization['build'])
    require(Path(authorization['build']['path']).resolve()==(D/'AUDIT.json').resolve(), 'Unexpected build receipt')
    require(audit.get('status')=='PASS' and audit.get('versionCode')==42 and
            audit.get('signer_matches_previous') is True and audit.get('resources')==installed['assets'], 'Build audit mismatch')
    for kind,relative in [('apk','apk/release/app-release.apk'),('aab','bundle/release/app-release.aab')]:
        path = Path(audit[kind])
        expected = D/'build42/projects/app/outputs'/relative
        require(path==expected and path.resolve(strict=True)==path and sha(path.read_bytes())==audit[kind+'_sha256'], 'Build artifact drift')
    return plan,audit,authorization

def intent(name, value):
    path = D/(name+'_INTENT.json')
    require(not path.exists(), 'Existing intent: reconcile; never retry uncertain operation')
    # Exclusive creation prevents concurrent executions from passing an idempotent writer.
    import json,os
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    with path.open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    require(path.read_bytes()==data, 'Intent custody failed')

def scan(raw):
    # Fail visibly without printing candidate bytes. Review remains required.
    patterns = [rb'-----BEGIN [A-Z ]*PRIVATE KEY-----',
                rb'gh[pousr]_[A-Za-z0-9]{20,}',rb'AIza[A-Za-z0-9_-]{30,}',
                rb'sk-[A-Za-z0-9_-]{20,}',
                rb'(?i)(?:password|storepass|keypass|api[_-]?key|access[_-]?token)\s*[:=]\s*[\x22\x27][^\x22\x27]{8,}[\x22\x27]']
    require(not any(re.search(p,raw) for p in patterns), 'Possible confidential literal: stop for review; content not logged')
