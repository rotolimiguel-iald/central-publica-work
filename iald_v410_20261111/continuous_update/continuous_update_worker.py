"""Staged app updater state machine. No imports of scientific programs.

Integration supplies trusted adapter functions. This module alone never deploys.
One supervisor-owned process must hold the OS mutex for its entire lifetime.
"""
import hashlib
import json
import os
import re
from pathlib import Path
import time
import uuid


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def replace_bytes(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + uuid.uuid4().hex)
        with backup.open('xb') as stream:
            stream.write(old)
        if backup.read_bytes() != old:
            raise RuntimeError('Backup verification failed')
    tmp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with tmp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if tmp.read_bytes() != data:
        raise RuntimeError('Temporary verification failed')
    os.replace(tmp, path)
    if path.read_bytes() != data:
        raise RuntimeError('State verification failed')


class Worker:
    """Adapters are installed code, never commands taken from a candidate file.

    detect(): small sealed custody/publication descriptor or None.
    prepare(candidate, directory): immutable complete package manifest.
    verify_package(directory): verifies EVERY package file and returns manifest.
    active(): immutable identity dict, captured once per actual model call too.
    review(directory, package_sha): verifies authenticated distinct ACOM reviewer
        and final pins; returns True only for accepted requirement, not PASS text.
    authorize(candidate): verifies standing operator policy source hash/scope.
    quiet(): no admitted jobs/calls, then deployment rechecks while frozen.
    deploy(directory, expected_active): existing controlled CAS transaction;
        returns receipt; MUST independently recheck review/auth/pins/quiet/CAS.
    reconcile(directory): inspect durable transaction receipt, no execution;
        returns verified 'ACTIVE', 'ROLLED_BACK', or None (uncertain).
    """

    def __init__(self, root, adapter):
        self.root = Path(root)
        self.adapter = adapter
        self.state_path = self.root / 'status.json'

    def save(self, state):
        data = encode(state)
        if not self.state_path.exists() or self.state_path.read_bytes() != data:
            replace_bytes(self.state_path, data)
        return state

    def tick(self):
        old = json.loads(self.state_path.read_bytes()) if self.state_path.exists() else {}
        # Recovery precedes discovery: a newer seal never hides an uncertain deploy.
        if old.get('phase') in ('PREPARING', 'ACTIVATING'):
            if old['phase'] == 'ACTIVATING':
                result = self.adapter.reconcile(Path(old['directory']))
                if result == 'ACTIVE':
                    return self.save(dict(old, phase='ACTIVE', reason='Recovered verified receipt'))
                if result == 'ROLLED_BACK':
                    return self.save(dict(old, phase='BLOCKED', reason='Verified rollback; explicit reconciliation required'))
            return self.save(dict(old, phase='BLOCKED', reason='Interrupted operation; inspect durable artifacts', uncertain=True))
        if old.get('uncertain'):
            return old
        candidate = self.adapter.detect()
        if candidate is None:
            return self.save(dict(old, phase='BLOCKED', reason='No verified sealed custody/publication descriptor'))
        key = sha(encode(candidate))
        active = self.adapter.active()
        if candidate['identity'] == active:
            return self.save({'phase': 'CURRENT', 'candidate_key': key, 'active': active})
        directory = self.root / 'candidates' / key
        if old.get('candidate_key') == key and old.get('phase') == 'BLOCKED':
            return old  # Do not retry a failed candidate merely because a timer fired.
        state = {'phase': 'PREPARING', 'candidate_key': key, 'candidate': candidate,
                 'directory': str(directory), 'expected_active': active}
        if old.get('candidate_key') == key:
            state['expected_active'] = old['expected_active']
        if not directory.exists():
            self.save(state)  # Write intent BEFORE preparing, including before mkdir.
            directory.mkdir(parents=True, exist_ok=False)
            try:
                self.adapter.prepare(candidate, directory)
            except Exception as exc:
                return self.save(dict(state, phase='BLOCKED', reason=type(exc).__name__))
        try:
            package = self.adapter.verify_package(directory)
            package_sha = package['manifest_sha256']
            if not isinstance(package_sha, str) or not re.fullmatch('[0-9a-f]{64}', package_sha):
                raise ValueError('Missing measured immutable manifest pin')
            if package['identity'] != candidate['identity']:
                raise ValueError('Candidate/package mismatch')
            state.update(phase='REVIEW_PENDING', package_sha256=package_sha)
            self.save(state)
            if not self.adapter.review(directory, package_sha):
                return state
            if not self.adapter.authorize(candidate):
                return self.save(dict(state, phase='BLOCKED', reason='Standing authorization not verified'))
            if self.adapter.active() != state['expected_active']:
                return self.save(dict(state, phase='BLOCKED', reason='Active baseline changed'))
            if not self.adapter.quiet():
                return self.save(dict(state, reason='Waiting for admitted calls to finish'))
            state.update(phase='ACTIVATING')
            self.save(state)
            self.adapter.deploy(directory, state['expected_active'])
            if self.adapter.reconcile(directory) != 'ACTIVE':
                raise RuntimeError('Deployment lacks verified final receipt')
            loaded = self.adapter.active()
            if loaded != candidate['identity']:
                raise RuntimeError('Loaded identity differs from reviewed candidate')
            return self.save(dict(state, phase='ACTIVE', active=loaded))
        except Exception as exc:
            return self.save(dict(state, phase='BLOCKED', reason=type(exc).__name__,
                                  uncertain=state['phase'] == 'ACTIVATING'))

    def run(self, stop_event, interval=60):
        if interval < 60:
            raise ValueError('Minimum polling interval is 60 seconds')
        while not stop_event.is_set():
            try:
                self.tick()
            except Exception as exc:
                # Do not replace an unreadable/uncertain state or erase its intent.
                # Supervisor log contains error class only, never provider data.
                print('UPDATE_CHECK_BLOCKED ' + type(exc).__name__, flush=True)
            stop_event.wait(interval)
