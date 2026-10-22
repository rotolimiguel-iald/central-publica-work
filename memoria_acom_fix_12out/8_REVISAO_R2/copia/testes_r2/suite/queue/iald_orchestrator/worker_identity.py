"""Fail closed before user-bound provider calls when the Windows worker token differs."""
import csv
import io
import json
import os
import subprocess

from .profiles import BASE

IDENTITY_RECEIPT = BASE / 'state/handoffs/worker_identity_expected.json'


def current_identity():
    if os.name != 'nt':
        raise RuntimeError('Worker identity preflight requires Windows.')
    output = subprocess.check_output(
        ['whoami', '/user', '/fo', 'csv', '/nh'],
        text=True, encoding='utf-8', timeout=10,
    )
    rows = list(csv.reader(io.StringIO(output)))
    if len(rows) != 1 or len(rows[0]) != 2:
        raise RuntimeError('Windows worker identity could not be measured.')
    user, sid = rows[0]
    if not user or not sid.startswith('S-'):
        raise RuntimeError('Windows worker identity is invalid.')
    return {'user': user, 'sid': sid, 'pid': os.getpid()}


def require_expected_identity():
    expected = json.loads(IDENTITY_RECEIPT.read_text(encoding='utf-8'))
    actual = current_identity()
    if (actual['user'].casefold(), actual['sid']) != (
        expected['user'].casefold(), expected['sid']
    ):
        raise RuntimeError(
            'Worker Windows identity differs from the validated credential owner; '
            'no provider execution may be dispatched.'
        )
    return actual
