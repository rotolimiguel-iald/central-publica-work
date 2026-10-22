# Names only (os.walk + stat); never opens a file.
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'copia', 'MEMORIA_IALD', 'lib'))
from iald_memory import guard
pat = re.compile(r'(iald_psion_state|iald_stack_v\d|(^|[^a-z0-9])\.?env($|[.~_\-])|\.(key|pem)($|[~._\-]))', re.I)
hits = []
for root in [r'C:\IALD', r'D:\IALD', os.path.expanduser('~')]:
    for dp, dn, fn in os.walk(root):
        low = dp.lower()
        if 'escritorio' in guard.fold(low) or r'\.git' in low or 'node_modules' in low or r'\appdata' in low:
            dn[:] = []
            continue
        for n in fn:
            f = guard.fold(n)
            if ('iald_psion_state' in f or 'iald_stack_v' in f or re.search(r'(^|[^a-z0-9])env($|[.~_\-])', f) and f.startswith(('.env','env')) or f.endswith(('.env', '.env~', '.key~', '.pem~')) or re.search(r'\.(key|pem)[~]', f)):
                rule = guard.confidential_basename(n)
                if rule is None:
                    hits.append(os.path.join(dp, n))
json.dump(hits, open(os.path.join(HERE, 't2_names_not_caught.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(hits))
for h in hits[:60]: print(h)
