import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
ops = []
for ln in open(p, encoding='utf-8'):
    try:
        o = json.loads(ln)
    except Exception:
        continue
    ts = o.get('timestamp') or ''
    if not ts.startswith('2026-10-05'):
        continue
    if o.get('type') == 'user':
        cc = (o.get('message') or {}).get('content')
        t = cc if isinstance(cc, str) else ''.join(x.get('text', '') for x in (cc or []) if isinstance(x, dict) and x.get('type') == 'text')
        if t and '<task-notification>' not in t and not t.startswith('This session is being continued'):
            ops.append((ts, t))
    if o.get('type') == 'attachment' and (o.get('attachment') or {}).get('type') == 'queued_command':
        pr = o['attachment'].get('prompt')
        t = pr if isinstance(pr, str) else ''.join(x.get('text', '') for x in pr if isinstance(x, dict))
        ops.append((ts, t))
ops = [(ts, t) for ts, t in ops if len(t) < 12000 and not t.lstrip().startswith('VOCÊ É AFERIDOR')]
BS = chr(92)


def norm(s):
    s = re.sub(BS + 'texttt' + BS + '{([^}]*)' + BS + '}', lambda m: m.group(1), s)
    s = s.replace('`', '"').replace("'", '"').replace(BS, '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


OP = [(ts, norm(t)) for ts, t in ops]


def find(q):
    qn = norm(q)
    if not qn:
        return None
    qn2 = qn[0].lower() + qn[1:]
    for ts, t in OP:
        if qn in t or qn2 in t:
            return ts
    return None


base = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"
pt = open(base + r"\v385\artigo_pt_v385.pysnip", encoding='utf-8').read()
qs = re.findall(r"``(.*?)''", pt)
print("== ARTIGO PT: aspas ``...''")
for q in qs:
    r = find(q)
    print('  ', 'VERBATIM' if r else 'NAO-VERBATIM', r, '|', q[:120])
stone = open(base + r"\v376\kernel_src\TGLExt\TheAxiomAndTheFalseWitness.lean", encoding='utf-8').read()
qs = re.findall(r"«(.*?)»", stone, re.S)
print("== PEDRA: aspas «...» (cada pedaço entre reticências testado em separado)")
for q in qs:
    parts = [x.strip() for x in q.split('…') if x.strip()]
    res = [find(pp) for pp in parts]
    print('  ', 'VERBATIM' if all(res) else 'VERIFICAR', '|', q.replace('\n', ' ')[:110], '|', res)
print("n mensagens do operador em 05/10:", len(OP))
