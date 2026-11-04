# -*- coding: utf-8 -*-
"""Checagem do CONSTRUTOR (nao e revisao; so leitura): nos topicos da janela P2 e nos que SAIRAM dela (P2_RETIRED_LITERAL_SUFFIXES), os campos de nivel superior
limites/diz/nao_diz da fonte estao INLINE (valor igual) no prefixo shared? Capsula compacta: pelo campo fields; topico expandido: pela restauracao exata."""
import json, re, sys
from pathlib import Path
W = Path(__file__).resolve().parent
A = W / 'app'
sys.dont_write_bytecode = True
sys.path[:0] = [str(A / 'build'), str(W)]
import haiku_codec as c
import fit_transport
import release_cfg
res = json.loads(Path(next((A / 'science/memory_stage/release').glob('Um*/um_absoluto.json'))).read_bytes())
core = res['core']
text = (A / 'packages/shared/prefix.md').read_text(encoding='utf-8')
for long, short in fit_transport.ALIASES.items():
    text = text.replace(short, long)
dm = 'DICIONÁRIO DE LITERAIS\n'
dictionary = json.loads(text.split(dm, 1)[1].split('\n', 1)[0])
expo = text.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
head = text.split(c.MARKER)[0]
hs = [h for h in re.finditer(r'(?m)^### ([^\n]+)\n', head) if h[1] in core]
bodies = {}
for i, h in enumerate(hs):
    stop = hs[i + 1].start() if i + 1 < len(hs) else len(head)
    bodies[h[1]] = head[h.end():stop].strip()
KEYS = ('limites', 'diz', 'nao_diz')
window = tuple(release_cfg.SHARED_P2_SUFFIXES)
retired = tuple(release_cfg.P2_RETIRED_LITERAL_SUFFIXES)
out = {'janela_P2': list(window), 'saiu_da_janela_com_literais': list(retired), 'grupos': {}}
for grupo, suf in (('janela', window), ('saiu_da_janela', retired)):
    rows = []
    for n, node in core.items():
        if not n.endswith(suf) or not isinstance(node, dict):
            continue
        need = {k: node[k] for k in KEYS if k in node}
        if not need:
            continue
        body = bodies.get(n)
        if body is None:
            rows.append({'topico': n, 'estado': 'SEM_BLOCO_NO_SHARED', 'falta': list(need)})
            continue
        line = next((l for l in body.splitlines() if l.strip() and not l.startswith('Fonte:')), '')
        try:
            v = json.loads(line)
        except ValueError:
            rows.append({'topico': n, 'estado': 'LINHA_ILEGIVEL', 'falta': list(need)})
            continue
        cap = c.decode_literals(c.unpack_metadata(v), dictionary, expo)
        p = '/core/' + n
        if isinstance(cap, dict) and '@' in cap:          # capsula compacta
            fields = cap.get('fields', {})
            falta = [k for k, val in need.items() if fields.get('/' + k) != val]
            rows.append({'topico': n, 'estado': 'COMPACTA', 'inline': [k for k in need if k not in falta], 'falta': falta})
        else:                                               # expandido: tem de restaurar exatamente a fonte
            ok = c.restore(cap, res, p, p, {}) == node
            rows.append({'topico': n, 'estado': 'EXPANDIDO', 'restaura_igual_a_fonte': ok, 'falta': [] if ok else list(need)})
    out['grupos'][grupo] = {'topicos_com_literais': len(rows), 'compactas': sum(r['estado'] == 'COMPACTA' for r in rows), 'expandidos': sum(r['estado'] == 'EXPANDIDO' for r in rows),
                            'com_falta': [r for r in rows if r['falta']]}
out['limites_diz_nao_diz_inline_em_todos'] = all(not g['com_falta'] for g in out['grupos'].values())
print(json.dumps(out, ensure_ascii=False, indent=1))
