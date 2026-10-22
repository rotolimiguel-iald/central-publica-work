"""Offline, single-file unified-diff merge against one pinned UTF-8 baseline.

Each --diff is independently validated against that baseline. Hunk context
counts as occupied space: even context-only overlap is conservatively refused.
No fuzzy matching, runtime access, retries, source edits or output overwrite.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


class Refusal(ValueError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_patch(raw, label, baseline):
    lines = raw.decode('utf-8-sig').replace('\r\n', '\n').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if len(lines) < 3 or not lines[0].startswith('--- ') or not lines[1].startswith('+++ '):
        raise Refusal(f'{label}: expected one unified file diff')
    hunks = []
    i = 2
    last_end = 0
    shift = 0
    while i < len(lines):
        m = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*', lines[i])
        if not m:
            raise Refusal(f'{label}:{i+1}: invalid hunk header')
        old, count, new, new_count = (int(m[1]), int(m[2] or 1), int(m[3]), int(m[4] or 1))
        start = old - 1 if count else old
        new_start = new - 1 if new_count else new
        if start < last_end or start < 0 or start + count > len(baseline) or new_start != start + shift:
            raise Refusal(f'{label}:{i+1}: invalid coordinates')
        i += 1
        before, after = [], []
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]
            if not line or line[0] not in ' +-':
                raise Refusal(f'{label}:{i+1}: unsupported patch syntax (including missing-final-newline markers)')
            if line[0] in ' -':
                before.append(line[1:])
            if line[0] in ' +':
                after.append(line[1:])
            i += 1
        if len(before) != count or len(after) != new_count or baseline[start:start+count] != before:
            raise Refusal(f'{label}: hunk at {old} does not exactly match baseline')
        hunks.append({'patch': label, 'start': start, 'end': start+count, 'after': after})
        last_end = start + count
        shift += new_count - count
    return hunks


def collides(a, b):
    # Insertions at either boundary are refused too: no implicit order choice.
    if a['start'] == a['end'] or b['start'] == b['end']:
        return max(a['start'], b['start']) <= min(a['end'], b['end'])
    return max(a['start'], b['start']) < min(a['end'], b['end'])


def merge(raw, expected_sha, patches):
    if sha(raw) != expected_sha.lower():
        raise Refusal('baseline SHA256 mismatch')
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    text = raw[len(bom):].decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    normalized = text.replace('\r\n', '\n')
    if '\r' in normalized or (newline == '\r\n' and '\n' in text.replace('\r\n', '')):
        raise Refusal('mixed/unsupported baseline newlines')
    if not normalized.endswith('\n'):
        raise Refusal('baseline must have final newline')
    baseline = normalized[:-1].split('\n')
    hunks = []
    for label, patch in patches:
        hunks.extend(parse_patch(patch, label, baseline))
    collisions = [{'left': a['patch'], 'right': b['patch'],
                   'left_range_0based': [a['start'], a['end']],
                   'right_range_0based': [b['start'], b['end']]}
                  for i, a in enumerate(hunks) for b in hunks[i+1:] if collides(a, b)]
    if collisions:
        raise Refusal(json.dumps({'collisions': collisions}, ensure_ascii=False))
    result = baseline[:]
    for h in sorted(hunks, key=lambda h: h['start'], reverse=True):
        result[h['start']:h['end']] = h['after']
    output = bom + (newline.join(result) + newline).encode('utf-8')
    return output, {'baseline_sha256': sha(raw), 'output_sha256': sha(output),
                    'newline': 'CRLF' if newline == '\r\n' else 'LF', 'hunks': len(hunks),
                    'patches': [{'path': name, 'sha256': sha(p)} for name, p in patches]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', required=True, type=Path)
    parser.add_argument('--baseline-sha256', required=True)
    parser.add_argument('--diff', required=True, action='append', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        if not args.output.resolve().is_relative_to(Path(__file__).resolve().parent):
            raise Refusal('output must remain inside this integration staging directory')
        if args.output.exists() or args.output.resolve() in [p.resolve() for p in [args.baseline, *args.diff]]:
            raise Refusal('output must be a new path distinct from every input')
        output, receipt = merge(args.baseline.read_bytes(), args.baseline_sha256,
                                [(str(p), p.read_bytes()) for p in args.diff])
        # Exclusive creation: concurrent writers cannot replace existing bytes.
        with args.output.open('xb') as f:
            f.write(output)
        if args.output.read_bytes() != output:
            raise Refusal('output readback mismatch')
        print(json.dumps({'status': 'MERGED_STAGING_ONLY', 'output': str(args.output), **receipt}))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({'status': 'REFUSED', 'error': str(error)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
