# -*- coding: utf-8 -*-
"""Checagem do CONSTRUTOR (nao e revisao; so leitura), versao r2. Corrige ao lado o check_literais_v406.py (que fica como esta, copiado):
o ramo EXPANDIDO dele restaurava o no inteiro e comparava com a fonte, mas o marcador de transporte '@B' (fit_transport) fica no no restaurado -> falso negativo em todos os topicos
expandidos (medido: o mesmo script na pasta da v406 dava 32 de 32 'com falta'; a v406 foi aceita porque o revisor recomputou por outro caminho).
Aqui compara-se so' o que o criterio pede: em cada topico da janela P2 e em cada topico que SAIU dela (P2_RETIRED_LITERAL_SUFFIXES), os campos de nivel superior
limites/diz/nao_diz da fonte estao INLINE e com valor IGUAL no prefixo, nos DOIS pacotes (shared e sonnet_public). Capsula compacta: pelo campo 'fields'; topico expandido: pelo valor direto."""
import json
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
A = W / 'app'
sys.dont_write_bytecode = True
sys.path[:0] = [str(A / 'build'), str(W)]
import haiku_codec as c
import fit_transport
import release_cfg

MISSING = object()
KEYS = ('limites', 'diz', 'nao_diz')
res = json.loads(Path(next((A / 'science/memory_stage/release').glob('Um*/um_absoluto.json'))).read_bytes())
core = res['core']
window = tuple(release_cfg.SHARED_P2_SUFFIXES)
retired = tuple(release_cfg.P2_RETIRED_LITERAL_SUFFIXES)
HEADERS = ('DICIONÁRIO DE LITERAIS\n', 'DICIONÁRIO DE INDICADORES LITERAIS\n', 'LITERAIS_COMPARTILHADOS\n')


def parse(prefix_path):
    text = Path(prefix_path).read_text(encoding='utf-8')
    for long, short in fit_transport.ALIASES.items():
        text = text.replace(short, long)
    dictionary, header = None, None
    for h in HEADERS:
        if h in text:
            try:
                dictionary = json.loads(text.split(h, 1)[1].split('\n', 1)[0])
                header = h.strip()
                break
            except ValueError:
                continue
    expo = text.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    head = text.split(c.MARKER)[0]
    hs = [m for m in re.finditer(r'(?m)^### ([^\n]+)\n', head) if m[1] in core]
    bodies = {}
    for i, m in enumerate(hs):
        stop = hs[i + 1].start() if i + 1 < len(hs) else len(head)
        bodies[m[1]] = head[m.end():stop].strip()
    return dictionary, header, expo, bodies


def inline(cap, key):
    if isinstance(cap, dict) and '@' in cap:
        return cap.get('fields', {}).get('/' + key, MISSING)
    v = cap.get(key, MISSING) if isinstance(cap, dict) else MISSING
    return MISSING if (isinstance(v, dict) and '@' in v) else v


out = {'janela_P2': list(window), 'saiu_da_janela_com_literais': list(retired), 'pacotes': {}}
for pkg in ('shared', 'sonnet_public'):
    dictionary, header, expo, bodies = parse(A / 'packages' / pkg / 'prefix.md')
    if dictionary is None:
        out['pacotes'][pkg] = {'erro': 'dicionario de literais nao encontrado', 'cabecalhos_tentados': list(HEADERS)}
        continue
    rec = {'cabecalho_do_dicionario': header, 'topicos_no_bloco': len(bodies), 'grupos': {}}
    for grupo, suf in (('janela', window), ('saiu_da_janela', retired)):
        rows, falhas = 0, []
        compactas = expandidos = 0
        for n, node in core.items():
            if not n.endswith(suf) or not isinstance(node, dict):
                continue
            need = {k: node[k] for k in KEYS if k in node}
            if not need:
                continue
            rows += 1
            body = bodies.get(n)
            if body is None:
                falhas.append({'topico': n, 'estado': 'SEM_BLOCO', 'falta': list(need)})
                continue
            line = next((l for l in body.splitlines() if l.strip() and not l.startswith('Fonte:')), '')
            try:
                cap = c.decode_literals(c.unpack_metadata(json.loads(line)), dictionary, expo)
            except Exception as e:
                falhas.append({'topico': n, 'estado': 'LINHA_ILEGIVEL', 'erro': type(e).__name__, 'falta': list(need)})
                continue
            if isinstance(cap, dict) and '@' in cap:
                compactas += 1
            else:
                expandidos += 1
            falta = [k for k, val in need.items() if inline(cap, k) != val]
            if falta:
                falhas.append({'topico': n, 'estado': 'COMPACTA' if (isinstance(cap, dict) and '@' in cap) else 'EXPANDIDO', 'falta': falta})
        rec['grupos'][grupo] = {'topicos_com_literais': rows, 'compactas': compactas, 'expandidos': expandidos, 'com_falta': falhas}
    out['pacotes'][pkg] = rec
out['limites_diz_nao_diz_inline_em_todos'] = all('erro' not in p and all(not g['com_falta'] for g in p['grupos'].values()) for p in out['pacotes'].values())
print(json.dumps(out, ensure_ascii=False, indent=1))
