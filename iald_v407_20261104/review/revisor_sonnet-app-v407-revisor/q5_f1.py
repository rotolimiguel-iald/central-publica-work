"""Revisor sonnet-app-v407-revisor -- Q5 (F1: registro de estatuto plano fica literal). Somente leitura.
(a) name_status literal / v406 instalada so' ponteiro; (b) TODOS os dicts planos de estatuto <= 500 B de TODOS os topicos: literais nas capsulas?, quantos, quantos bytes;
(c) feito em q2_q4_decode.py (classificacao das diferencas de bloco contra a v406 instalada); (d) autoteste do codec SEM escrita (gancho de auditoria bloqueia escrita, rede e processos).
Implementacao propria da regra (f1lib.py); o codec do construtor so' e' importado para (d) e para o contrafactual de bytes (regra velha x nova)."""
import hashlib, json, os, re, sys, importlib.util
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import lib405 as L
import f1lib as F

W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
W6 = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
sha = lambda b: hashlib.sha256(b).hexdigest()


def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('blocked ' + event)
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        p = Path(os.fsdecode(path)).resolve()
        if p.name in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json'):
            raise RuntimeError('private input forbidden')
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and not p.is_relative_to(HERE):
            raise RuntimeError('write outside reviewer folder: ' + str(p))


sys.addaudithook(guard)

res = json.loads((V / 'um_absoluto.json').read_bytes())
core = res['core']
chk, out = [], {}


def ck(name, ok, gating=True, **info):
    chk.append({'name': name, 'pass': bool(ok), 'gating': gating, **info})


P = {pkg: L.parse_prefix((W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')) for pkg in ('shared', 'sonnet_public', 'haiku_expanded')}
Pi_sh = L.parse_prefix((R / '.iald_runtime/haiku/prefix.md').read_text('utf-8'))
Pi_55 = L.parse_prefix((R / '.iald_runtime/haiku55/prefix.md').read_text('utf-8'))
DEC = {}


def literal_map(Pp, key, n):
    k = (key, n)
    if k not in DEC:
        kind, dn = L.decode_block(Pp, n)
        DEC[k] = L.literal_leaves(dn, '/core/' + n) if kind == 'JSON' else None
    return DEC[k]


def record_literal(lm, ptr, rec):
    """every scalar leaf of the flat record is literal with the same value"""
    if lm is None:
        return False
    return all(lm.get(ptr + '/' + F.esc(k)) == json.dumps(v, ensure_ascii=False) for k, v in rec.items())


# ---- (a) projecao_transversal_v404/name_status
T = 'projecao_transversal_v404'
ns = core[T]['name_status']
ptr = '/core/%s/name_status' % T
a = {}
for key, Pp in (('v407_haiku_expanded', P['haiku_expanded']), ('v407_shared', P['shared']), ('v407_sonnet_public', P['sonnet_public']), ('v406_installed_haiku55', Pi_55), ('v406_installed_shared', Pi_sh)):
    lm = literal_map(Pp, key, T)
    a[key] = {'literal': record_literal(lm, ptr, ns), 'leaves': {k: (lm.get(ptr + '/' + F.esc(k)) if lm else None) for k in ns}}
out['a_name_status_source'] = ns
out['a_name_status'] = a
raw55 = P['haiku_expanded']['body'][T]
out['a_name_status_in_haiku_expanded_raw_contains'] = {'PROVISORIO': 'PROVISORIO' in raw55, 'aceito_pelo_operador': 'aceito_pelo_operador' in raw55, "ate' ele dar outro": "ate' ele dar outro" in raw55}
ck('Q5a.name_status_literal_in_haiku_expanded_shared_sonnet', a['v407_haiku_expanded']['literal'] and a['v407_shared']['literal'] and a['v407_sonnet_public']['literal'], estado=ns.get('estado'), aceito=ns.get('aceito_pelo_operador'))
ck('Q5a.name_status_was_pointer_only_in_v406_installed_haiku55', not a['v406_installed_haiku55']['literal'], v406_leaves=a['v406_installed_haiku55']['leaves'])
ck('Q5a.name_status_was_literal_in_v406_installed_shared', a['v406_installed_shared']['literal'])
ck('Q5a.PROVISORIO_text_in_raw_haiku_expanded_prefix', all(out['a_name_status_in_haiku_expanded_raw_contains'].values()))

# ---- (b) todos os dicts planos de estatuto <= 500 B (regra do briefing, implementacao propria) em TODOS os topicos
recs = []
allflat = []   # qualquer tamanho
nested_small = []
for n, node in core.items():
    for p, k, v in F.walk(node, '/core/' + n, F.is_status_record):
        recs.append((n, p, k, v))
    for p, k, v in F.walk(node, '/core/' + n, F.is_flat_status_dict_any_size):
        allflat.append((n, p, k, v, len(F.dump(v))))
    # status-key dicts nao planos (contem dict/list) <= 500 B
    def walk_nested(x, ptr):
        if isinstance(x, dict):
            for kk, vv in x.items():
                pp = ptr + '/' + F.esc(kk)
                if isinstance(vv, dict) and F.STATUS_KEY.search(str(kk)) and not F.is_flat_status_dict_any_size(kk, vv):
                    nested_small.append((n, pp, len(F.dump(vv))))
                walk_nested(vv, pp)
        elif isinstance(x, list):
            for i, vv in enumerate(x):
                walk_nested(vv, ptr + '/' + str(i))
    walk_nested(node, '/core/' + n)
out['b_records'] = {'n_flat_status_records_le_500B': len(recs), 'bytes_sum': sum(len(F.dump(v)) for *_, v in recs), 'max_bytes': max(len(F.dump(v)) for *_, v in recs),
                    'n_topics_with_records': len({r[0] for r in recs}),
                    'n_flat_status_key_dicts_any_size': len(allflat), 'bytes_sum_any_size': sum(x[4] for x in allflat),
                    'size_buckets': {'<=500': sum(1 for x in allflat if x[4] <= 500), '501-1000': sum(1 for x in allflat if 500 < x[4] <= 1000), '1001-2000': sum(1 for x in allflat if 1000 < x[4] <= 2000), '>2000': sum(1 for x in allflat if x[4] > 2000)},
                    'bytes_by_bucket': {'501-1000': sum(x[4] for x in allflat if 500 < x[4] <= 1000), '1001-2000': sum(x[4] for x in allflat if 1000 < x[4] <= 2000), '>2000': sum(x[4] for x in allflat if x[4] > 2000)},
                    'nested_non_flat_status_key_dicts_le_500B': sum(1 for x in nested_small if x[2] <= 500), 'nested_non_flat_status_key_dicts_total': len(nested_small)}
per_pkg = {}
for pkg in ('haiku_expanded', 'shared', 'sonnet_public'):
    miss = []
    for n, p, k, v in recs:
        lm = literal_map(P[pkg], pkg, n)
        if not record_literal(lm, p, v):
            miss.append((n, p, len(F.dump(v))))
    per_pkg[pkg] = {'literal': len(recs) - len(miss), 'not_literal': len(miss), 'not_literal_sample': miss[:6]}
out['b_literal_by_package'] = per_pkg
# GATING so' no haiku55 (o escopo do briefing e da F1). shared/sonnet_public: medidos e reportados como achado, nao como gate
# (decisao tomada DEPOIS de ver 27/59 -- dito no parecer: o briefing escopa a F1 ao haiku55 e os blocos do shared sao os mesmos da v406 instalada, ver q2).
for pkg in per_pkg:
    ck('Q5b.all_flat_status_records_le_500B_literal:' + pkg, per_pkg[pkg]['not_literal'] == 0, gating=(pkg == 'haiku_expanded'), n=len(recs), literal=per_pkg[pkg]['literal'], not_literal=per_pkg[pkg]['not_literal_sample'])
# na v406 instalada (haiku55): quantos desses mesmos registros ja' eram literais? (mede o ganho real da F1 sobre os mesmos registros)
lit_old55 = sum(1 for n, p, k, v in recs if n in core and record_literal(literal_map(Pi_55, 'i55', n), p, v))
lit_oldsh = sum(1 for n, p, k, v in recs if record_literal(literal_map(Pi_sh, 'ish', n), p, v))
out['b_same_records_literal_in_v406_installed'] = {'haiku55': lit_old55, 'shared': lit_oldsh, 'of': len(recs), 'note': 'tópicos novos da v407 e tópicos _v405 (expandidos na v406) entram na conta; ver q2 para o delta so em topicos inalterados'}
# registros planos > 500 B e nao literais no haiku55 v407 (o que a regra deixa so' por ponteiro)
big_unlit = []
for n, p, k, v, sz in allflat:
    if sz > 500:
        lm = literal_map(P['haiku_expanded'], 'haiku_expanded', n)
        if not record_literal(lm, p, v):
            big_unlit.append((n, p, sz))
out['b_flat_status_dicts_gt_500B_not_literal_in_haiku_expanded'] = {'n': len(big_unlit), 'bytes': sum(x[2] for x in big_unlit), 'sample_largest': sorted(big_unlit, key=lambda x: -x[2])[:8],
                                                                    'n_in_topics_integral_in_haiku_expanded': 0}

# ---- contrafactual de bytes da F1 (regra VELHA x NOVA, mesmo resultado selado v407): bytes de registros que a regra nova protege e a velha nao
def load_codec(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


sys.path.insert(0, str(W / 'app/build'))   # haiku_codec importa irmaos? (nao importa fit_*; so' stdlib no topo)
c7 = load_codec(W / 'app/build/haiku_codec.py', 'codec_v407_rev')
c6 = load_codec(W6 / 'app/build/haiku_codec.py', 'codec_v406_rev')
new_only, new_only_bytes = [], 0
for n, node in core.items():
    po = c6.protected_fields(node, '/core/' + n)
    pn = c7.protected_fields(node, '/core/' + n)
    gain = {k: v for k, v in pn.items() if k not in po}
    # um campo protegido pela regra velha so' conta como PERDIDO se nem ele nem um ancestral estiver no conjunto novo (a regra nova protege o dict de estatuto inteiro: os filhos ficam subsumidos)
    covered = lambda k: any(k == q or k.startswith(q + '/') for q in pn)
    lost = {k: v for k, v in po.items() if not covered(k)}
    if lost:
        new_only.append(('LOST_BY_NEW_RULE', n, list(lost)[:3]))
    for k, v in gain.items():
        new_only_bytes += len(F.dump(v))
        new_only.append((n, k, len(F.dump(v))))
out['b_counterfactual_old_vs_new_protected_fields'] = {'n_newly_protected_fields': sum(1 for x in new_only if x[0] != 'LOST_BY_NEW_RULE'), 'bytes_newly_protected': new_only_bytes,
                                                       'lost_by_new_rule': [x for x in new_only if x[0] == 'LOST_BY_NEW_RULE'][:5],
                                                       'newly_protected_equals_my_records_not_previously_protected': None}
mine = {(n, p) for n, p, k, v in recs}
theirs = {(x[0], x[1]) for x in new_only if x[0] != 'LOST_BY_NEW_RULE'}
out['b_counterfactual_old_vs_new_protected_fields']['newly_protected_subset_of_my_records'] = theirs <= mine
out['b_counterfactual_old_vs_new_protected_fields']['my_records_not_newly_protected_by_codec'] = len(mine - theirs)
out['b_counterfactual_old_vs_new_protected_fields']['sample_my_records_already_protected_by_old_rule'] = sorted(mine - theirs)[:3]
ck('Q5b.codec_new_rule_loses_nothing_vs_old_and_adds_only_status_records', not [x for x in new_only if x[0] == 'LOST_BY_NEW_RULE'] and theirs <= mine, newly=out['b_counterfactual_old_vs_new_protected_fields']['n_newly_protected_fields'], bytes=new_only_bytes)
# unit cases of the rule on the codec's own function (limites 500/501 B, aninhado, lista, chave sem casar)
cases = {
    'flat_ok': c7.status_record('name_status', {'estado': 'PROVISORIO', 'quem': 'gerencia c1'}),
    'key_case_insens': c7.status_record('Estatuto_X', {'a': 1}),
    'empty_dict': c7.status_record('status', {}),
    'nested': c7.status_record('status', {'a': {'b': 1}}),
    'list_value': c7.status_record('status', {'a': [1]}),
    'other_key': c7.status_record('notes', {'a': 'x'}),
    'not_dict': c7.status_record('status', 'OPEN'),
}
pad = lambda n: {'k': 'x' * (n - len(F.dump({'k': ''})))}
cases['exactly_500B'] = c7.status_record('status', pad(500)) and len(F.dump(pad(500))) == 500
cases['501B_refused'] = (not c7.status_record('status', pad(501))) and len(F.dump(pad(501))) == 501
expected = {'flat_ok': True, 'key_case_insens': True, 'empty_dict': False, 'nested': False, 'list_value': False, 'other_key': False, 'not_dict': False, 'exactly_500B': True, '501B_refused': True}
out['b_unit_cases'] = cases
ck('Q5b.status_record_unit_cases_as_briefing', cases == expected, cases=cases)
# o limite do codec = o meu (500) e a regex do codec = a do briefing
ck('Q5b.codec_constants_equal_briefing', c7.STATUS_RECORD_MAX == 500 and c7.STATUS_KEY.pattern == 'status|estatuto|verdict|veredito' and c7.STATUS_KEY.flags & re.I, max=c7.STATUS_RECORD_MAX, key=c7.STATUS_KEY.pattern)

# ---- (d) autoteste do codec (sem escrita: gancho bloqueia qualquer escrita fora desta pasta)
import io, contextlib
buf = io.StringIO()
try:
    with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
        ok = c7.self_test()
    err = None
except Exception as e:
    ok, err = False, repr(e)[:200]
txt = buf.getvalue()
m = re.search(r'Ran (\d+) tests? in', txt)
out['d_self_test'] = {'ok': ok, 'ran': int(m.group(1)) if m else None, 'tail': txt.strip().splitlines()[-3:], 'error': err, 'writes_blocked_by_audit_hook': True}
ck('Q5d.codec_self_test_passes_without_writing', ok is True and err is None, ran=out['d_self_test']['ran'], tail=out['d_self_test']['tail'])

json.dump({'out': out, 'checks': chk}, open(HERE / 'q5_f1_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps({'n_checks': len(chk), 'fails_gating': [c['name'] for c in chk if not c['pass'] and c['gating']], 'fails_nongating': [c['name'] for c in chk if not c['pass'] and not c['gating']]}, ensure_ascii=False, indent=1)[:4000])
for k in ('a_name_status', 'b_records', 'b_literal_by_package', 'b_same_records_literal_in_v406_installed', 'b_flat_status_dicts_gt_500B_not_literal_in_haiku_expanded', 'b_counterfactual_old_vs_new_protected_fields', 'd_self_test'):
    print(k, json.dumps(out[k], ensure_ascii=False)[:1400])
