"""Find essential source fields absent verbatim from the draft; no source edits."""
import hashlib
import json
from pathlib import Path
import re

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
ESSENTIAL = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)


def main():
    manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
    entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
    source_raw = Path(entry['path']).read_bytes()
    if hashlib.sha256(source_raw).hexdigest() != entry['public_sha256']:
        raise ValueError('Source hash mismatch')
    candidate_raw = (WORK / 'haiku_candidate.md').read_bytes()
    receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
    digest = hashlib.sha256(candidate_raw).hexdigest()
    if digest != receipt['sha256']:
        raise ValueError('Candidate hash mismatch')
    candidate = candidate_raw.decode('utf-8')
    data = json.loads(source_raw)
    rows = []

    def visit(node, pointer):
        if isinstance(node, dict):
            for key, value in node.items():
                child = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
                if ESSENTIAL.search(key) and isinstance(value, str) and len(value) >= 40:
                    escaped = json.dumps(value, ensure_ascii=False)[1:-1]
                    present = value in candidate or escaped in candidate
                    rows.append({'pointer': child, 'chars': len(value), 'literal_present': present,
                                 'value_sha256': hashlib.sha256(value.encode()).hexdigest()})
                visit(value, child)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                visit(value, pointer + '/' + str(i))

    for topic in receipt['topics']:
        visit(data['core'][topic['id']], topic['pointer'])
    missing = [row for row in rows if not row['literal_present']]
    result = {'status': 'LEXICAL_COVERAGE_AUDIT_NOT_SEMANTIC_CERTIFICATION',
              'candidate_sha256': digest, 'source_sha256': entry['public_sha256'],
              'examined_essential_string_fields': len(rows), 'absent_verbatim': len(missing),
              'missing_fields': missing,
              'limitations': 'Literal presence does not prove correct attribution or understanding. Absence requires inspection before omission is accepted.'}
    target = WORK / ('haiku_essential_fields_' + digest[:12] + '.json')
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
    if target.exists() and target.read_bytes() != payload:
        raise ValueError('Existing audit differs')
    if not target.exists():
        with target.open('xb') as stream:
            stream.write(payload)
    print(json.dumps({**result, 'missing_fields': missing[:20]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
