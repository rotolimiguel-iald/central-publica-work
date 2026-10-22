"""Add one verified APK only. Default is preview; --publish is never implicit."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'android29_R2'))
from run_android29_R2 import pin, save, fresh_preflight, no_reparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--preflight', type=Path)
    args = parser.parse_args()
    plan_path = HERE / 'APK29_ADDITIVE_PUBLICATION_PLAN_R1.json'
    plan = json.loads(plan_path.read_bytes())
    for item in [plan['review'], plan['source'], plan['candidate'], plan['endpoint_source']['pin'], *plan['preserve_existing_apks']]:
        no_reparse(item['path'])
        if pin(item['path']) != item:
            raise RuntimeError('Pinned artifact changed; publication refused')
    review = json.loads(Path(plan['review']['path']).read_bytes())
    if review['status'] != 'PASS' or not all(review['checks'].values()):
        raise RuntimeError('Archive review is not PASS')
    dest = Path(plan['destination'])
    expected = Path('C:/IALD/projetos_pyhton/IALD/downloads/IALD-4.1-29.apk')
    if dest != expected:
        raise RuntimeError('Unexpected publication target')
    no_reparse(dest)
    if dest.exists() and pin(dest)['sha256'] != plan['source']['sha256']:
        raise RuntimeError('Different APK29 already exists; no overwrite allowed')
    for item in plan['preserve_existing_apks']:
        if pin(item['path']) != item: raise RuntimeError('Existing APK changed')
    if not args.publish:
        print(json.dumps({'mode': 'PLAN_ONLY', 'published': False, 'plan': pin(plan_path),
                          'destination_exists': dest.exists(), 'endpoint': plan['authenticated_url']}, ensure_ascii=False))
        return
    if not args.preflight:
        raise RuntimeError('Explicit publication requires a fresh deploy preflight')
    receipt_dir = HERE / 'publication_receipts' / dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    receipt_dir.mkdir(parents=True, exist_ok=False)
    preflight = fresh_preflight(args.preflight, receipt_dir)
    raw = Path(plan['source']['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != plan['source']['sha256']:
        raise RuntimeError('APK changed after preflight')
    if pin(plan['preserve_apk27']['path']) != plan['preserve_apk27']:
        raise RuntimeError('APK27 changed after preflight')
    intent = HERE / 'PUBLICATION_INTENT_R1.json'
    with intent.open('xb') as out:
        out.write(json.dumps({'plan':pin(plan_path),'receipt_directory':str(receipt_dir),'no_repeat':True}).encode()); out.flush(); os.fsync(out.fileno())
    save(receipt_dir / 'INTENT.json', {'plan': pin(plan_path), 'preflight': preflight,
                                      'destination': str(dest), 'overwrite': False})
    if not dest.exists():
        # Same C: volume; stage only in WORK, then atomically create the new name.
        staged = receipt_dir / ('APK29_' + uuid.uuid4().hex + '.tmp')
        with staged.open('xb') as output:
            output.write(raw)
            output.flush()
            os.fsync(output.fileno())
        if pin(staged)['sha256'] != plan['source']['sha256']:
            raise RuntimeError('Staged APK hash mismatch')
        no_reparse(dest.parent)
        os.rename(staged, dest)  # Windows refuses replacing a competing target.
        action = 'CREATED_NEW_FILE'
    else:
        action = 'ALREADY_IDENTICAL_NO_WRITE'
    if pin(dest)['sha256'] != plan['source']['sha256'] or any(pin(item['path']) != item for item in plan['preserve_existing_apks']):
        raise RuntimeError('Post-publication verification failed')
    receipt = receipt_dir / 'RESULT.json'
    save(receipt, {'action': action, 'destination': pin(dest), 'preserved_apk27': plan['preserve_apk27'],
                   'plan': pin(plan_path), 'review': plan['review'], 'preflight': preflight,
                   'endpoint': plan['authenticated_url'], 'http_verified': False,
                   'html_or_manifest_changed': False, 'device_installation_verified': False})
    print(json.dumps({'receipt': pin(receipt), 'action': action}, ensure_ascii=False))


if __name__ == '__main__':
    main()
