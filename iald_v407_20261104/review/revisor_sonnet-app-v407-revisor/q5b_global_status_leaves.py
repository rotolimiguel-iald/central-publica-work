"""Revisor sonnet-app-v407-revisor -- extra de Q5: folha de qualificador (status|statute|estatuto|verdict|veredit*) que fica SO' por ponteiro, em TODOS os topicos (nao so' janela/aposentados).
Regra do molde (qb_decode.py da v406): folhas cujo ultimo nome casa; ignora raizes 'unconditional', 'index_conditional', 'named_pending'. Compara v407 (cada pacote) com a v406 instalada sobre o selado de cada uma. Somente leitura."""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104'); W6 = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103'); R = Path(r'C:\IALD\projetos_pyhton\IALD')
V7 = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
core7 = json.loads((V7 / 'um_absoluto.json').read_bytes())['core']
m = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
core6 = json.loads(Path(m['published_evidence']['result']['path']).read_bytes())['core']
RX = re.compile(r'(?i)status|statute|estatuto|verdict|veredit\w*')
def pointer_only(Pp, core):
    rows = {}
    for n, src in core.items():
        k, dn = L.decode_block(Pp, n)
        if k != 'JSON':
            continue
        lps = set(L.literal_leaves(dn, '/core/' + n))
        for p, v in L.leaves(src, '/core/' + n):
            last = p.rsplit('/', 1)[-1]
            if re.fullmatch(RX.pattern, last):
                top = p.split('/')[3] if p.count('/') >= 3 else ''
                if top in ('unconditional', 'index_conditional', 'named_pending'):
                    continue
                if p not in lps and not any(q.startswith(p + '/') or p.startswith(q + '/') for q in lps):
                    rows[p] = v
    return rows
P7 = {k: L.parse_prefix((W / 'app/packages' / k / 'prefix.md').read_text('utf-8')) for k in ('shared', 'sonnet_public', 'haiku_expanded')}
P6 = {'shared': L.parse_prefix((R / '.iald_runtime/haiku/prefix.md').read_text('utf-8')), 'haiku_expanded': L.parse_prefix((R / '.iald_runtime/haiku55/prefix.md').read_text('utf-8')), 'sonnet_public': L.parse_prefix((W6 / 'app/packages/sonnet_public/prefix.md').read_text('utf-8'))}
out = {}
for pkg in P7:
    a = pointer_only(P7[pkg], core7); b = pointer_only(P6[pkg], core6)
    newly = sorted(set(a) - set(b)); fixed = sorted(set(b) - set(a))
    # dos 'newly' so' os de topicos de fonte inalterada contam como regressao (fonte alterada pode ter folhas novas)
    newly_unchanged = [p for p in newly if core7[p.split('/')[2]] == core6.get(p.split('/')[2])]
    out[pkg] = {'pointer_only_v407': len(a), 'pointer_only_v406_installed': len(b), 'newly_pointer_only': len(newly), 'newly_pointer_only_in_unchanged_source_topics': newly_unchanged[:6], 'n_newly_unchanged': len(newly_unchanged), 'no_longer_pointer_only': len(fixed), 'sample_v407': sorted(a)[:4], 'sample_newly': newly[:4]}
json.dump(out, open(HERE / 'q5b_global_status_leaves_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:3500])
