"""Revisor sonnet-app-v407-revisor -- Q1 (identidade/fontes). Somente leitura. Sem rede (git local apenas). Nao importa haiku_codec / fit_*.
Adaptado de qa_files.py do revisor da v406 (parte Q1), com acrescimos: ref local origin/main, URL percent-encoded recomputada, Nos vivo, ORDEM_006 e ordem do operador por hash."""
import hashlib, json, re, subprocess, sys, urllib.parse
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
NOS = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
GIT = r'C:\IALD\Artigo\the_boundary'
A = W / 'app'
OUT = Path(__file__).parent
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
chk = []
out = {}


def ck(name, ok, **info):
    chk.append({'name': name, 'pass': bool(ok), **info})


def git(*args, binary=False):
    r = subprocess.run(['git', '-C', GIT, *args], capture_output=True)
    return (r.returncode, r.stdout if binary else r.stdout.decode('utf-8', 'replace').strip(), r.stderr.decode('utf-8', 'replace').strip()[:200])


rel_raw = (A / 'RELEASE.json').read_bytes()
rel = json.loads(rel_raw)
seal = rd(V / 'um_absoluto_selo.json')
pino = seal['sha256']['um.py']
ck('Q1.release_json_keys_exact', set(rel) == {'release', 'espelho_commit', 'um_py_sha256'} and rel['release'] == 'v407', release=rel['release'])
ck('Q1.seal_um_version_v407_selftest', seal.get('um_version') == 'v407' and seal.get('fail_closed_selftest') == 'FAIL_CLOSED_SELFTEST_PASSED', um_version=seal.get('um_version'), selftest=seal.get('fail_closed_selftest'))
ck('Q1.pino_equals_seal', rel['um_py_sha256'] == pino, pino16=pino[:16])
ck('Q1.pino_is_833121339e649f71_and_full', pino == '833121339e649f7171e2eccca1a19b3a1564aa306a787ed8cea76ded0fdf3475')
um_disk = sha((V / 'um.py').read_bytes())
ck('Q1.vault_um_py_sha_equals_pino', um_disk == pino, recomputed16=um_disk[:16], bytes=(V / 'um.py').stat().st_size)
commit = rel['espelho_commit']
ck('Q1.commit_is_bf9017157406afa6b4dc05c6a9d566129e6a6ee4', commit == 'bf9017157406afa6b4dc05c6a9d566129e6a6ee4')
rc, t, e = git('cat-file', '-t', commit)
ck('Q1.git_commit_exists', rc == 0 and t == 'commit', type=t, err=e)
rc, body, e = git('cat-file', '-p', commit)
out['git_commit_head_lines'] = body.splitlines()[:8]
ck('Q1.commit_message_mentions_v407', 'v407' in body)
rc, head, _ = git('rev-parse', 'HEAD')
rc1, orig, e1 = git('rev-parse', 'refs/remotes/origin/main')
rc2, _, _ = git('merge-base', '--is-ancestor', commit, 'HEAD')
rc3, _, _ = git('merge-base', '--is-ancestor', commit, 'refs/remotes/origin/main')
out['git_refs'] = {'HEAD': head, 'origin_main_local_ref': orig, 'pinned': commit}
ck('Q1.pinned_equals_local_HEAD_and_origin_main_ref', head == commit and orig == commit, head12=head[:12], origin12=orig[:12],
   note='ref local de origin/main: idade = ultimo fetch (sem rede nesta revisao); ls-remote NAO repetido')
ck('Q1.pinned_is_ancestor_of_HEAD_and_origin', rc2 == 0 and rc3 == 0)
rc, st, _ = git('status', '--porcelain', '--untracked-files=no')
out['git_tracked_changes_in_mirror_worktree'] = len(st.splitlines())

# --- blobs publicos do commit pinado
pgb = rd(A / 'PUBLIC_GIT_BINDING.json')
ck('Q1.public_binding_commit', pgb['commit'] == commit and pgb.get('local_git_object_bytes_only') is True and pgb.get('remote_http_checked') is False)
bad, urlbad = [], []
tree = {}
for pth, row in pgb['sources'].items():
    rc, blob, e = git('cat-file', 'blob', commit + ':' + pth, binary=True)
    if rc != 0 or sha(blob) != row['sha256'] or len(blob) != row['bytes']:
        bad.append((pth, rc, e))
    exp_url = 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + commit + '/' + urllib.parse.quote(pth)
    if row['url'] != exp_url:
        urlbad.append((pth, row['url'][-80:], exp_url[-80:]))
    tree[pth] = (rc == 0, len(blob), sha(blob)[:16])
ck('Q1.public_sources_blobs_match_in_pinned_commit', not bad and len(pgb['sources']) == 10, n=len(pgb['sources']), bad=bad[:3])
ck('Q1.public_urls_pinned_and_percent_encoded_recomputed', not urlbad, bad=urlbad[:2])
# o commit pinado carrega os arquivos selados (blob == cofre)
rc, ls, _ = git('ls-tree', '-r', '--name-only', '-z', commit)
names = ls.split('\0')
vv = {}
for nm in ('um.py', 'um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_pt.txt', 'um_absoluto_forma_canonica.md', 'tgl_kernel_proof_manifest.json'):
    cand = [n for n in names if (n.endswith('/' + nm) or n == nm)]
    pref = [n for n in cand if n.startswith('Um (absoluto)')]
    row = {'candidates_in_tree': len(cand), 'candidates_under_Um_absoluto_folder': len(pref)}
    cand = sorted(pref or cand, key=len)   # o arquivo do nivel da pasta, nao copias arquivadas mais fundo
    if cand:
        rc, blob, e = git('cat-file', 'blob', commit + ':' + cand[0], binary=True)
        row.update(path_tail=cand[0][-70:], equals_vault=(rc == 0 and sha(blob) == sha((V / nm).read_bytes())))
    vv[nm] = row
out['vault_equals_git_blob'] = vv
ck('Q1.vault_sealed_files_equal_pinned_git_blobs', all(v.get('equals_vault') for v in vv.values()), detail={k: v.get('equals_vault') for k, v in vv.items()})

# --- manifesto de custodia: 36 artefatos recomputados
cm_path = V / 'CUSTODY_MANIFEST.json'
cm = rd(cm_path)
sv = rd(W / 'sources_verified.json')
ck('Q1.sources_verified_status', sv['status'] == 'CUSTODY_AND_SEAL_VERIFIED' and sv['release'] == 'v407' and sv['source_sha256'] == pino and sv['published']['pinned_commit'] == commit and sv['published']['release_ready'] is True and sv['published']['remote_checked'] is True,
   remote_main_declared=sv['published']['remote_main'][:12])
ck('Q1.custody_manifest_sha', sha(cm_path.read_bytes()) == sv['custody_manifest']['sha256'], sha16=sha(cm_path.read_bytes())[:16])
ck('Q1.custody_manifest_version_fields', cm['version'] == cm['um_version_no_selo'] == 'v407' and not cm['mismatches'] and cm['um_py_pin'] == pino, mismatches=cm['mismatches'])
bad_art, rows = [], []
for a in cm['artifacts']:
    b = (V / a['file']).read_bytes()
    rows.append((a['file'], len(b), sha(b)))
    if sha(b) != a['sha256']:
        bad_art.append(('manifest', a['file']))
svmap = {a['file']: a for a in sv['artifacts']}
for f, n, h in rows:
    s = svmap.get(f)
    if not s or s['sha256'] != h or s['bytes'] != n:
        bad_art.append(('sources_verified', f))
ck('Q1.artifacts_recomputed_equal_manifest_and_sources_verified', not bad_art and len(rows) == len(sv['artifacts']) == sv['artifact_count'] == 36, n=len(rows), bad=bad_art[:3], total_bytes=sum(n for _, n, _ in rows))
out['artifact_ids'] = [f for f, _, _ in rows][:40]
pm = rd(V / 'tgl_kernel_proof_manifest.json')
res = rd(V / 'um_absoluto.json')
ck('Q1.seal_proof_custody_formal_source_hash_equal', seal['formal_source_hash'] == pm['formal_source_hash'] == cm['formal_source_hash'] == sv['formal_source_hash'], fsh16=seal['formal_source_hash'][:16])
nform = len(pm['formal_files_sha256'])
ck('Q1.formal_files_equals_declared', nform == sv['kernel_counts_declared_in_custody']['formal_files'] == cm['kernel']['formal_files'], n=nform, declared=sv['kernel_counts_declared_in_custody'])
for name in ('um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json', 'um_absoluto_forma_canonica.md'):
    if sha((V / name).read_bytes()) != seal['sha256'][name]:
        ck('Q1.seal_sha_' + name, False)
ck('Q1.seal_sha_of_four_files', all(sha((V / n).read_bytes()) == seal['sha256'][n] for n in ('um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json', 'um_absoluto_forma_canonica.md')))
ck('Q1.gate_and_science_untouched_flags', sv.get('gate_modified') is False and sv.get('science_executed') is False)
ck('Q1.sealed_result_has_477_topics', len(res['core']) == 477, n=len(res['core']))

# --- No's vivo (copia de trabalho): ainda v407? bytes iguais ao cofre?
nos_seal = rd(NOS / 'um_absoluto_selo.json')
live = {'nos_um_version': nos_seal.get('um_version')}
if nos_seal.get('um_version') == 'v407':
    live['bytes_equal_vault'] = {n: ((NOS / n).read_bytes() == (V / n).read_bytes()) for n in ('um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_selo.json')}
out['nos_live'] = live
ck('Q1.nos_live_is_v407_and_equal_to_vault_or_moved_on', live['nos_um_version'] != 'v407' or all(live['bytes_equal_vault'].values()), **live)

# --- ordem do operador e ORDEM_006 por hash
op = Path(r'C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt')
opb = op.read_bytes()
ck('Q1.operator_order_sha16_b89e4c909f37e163', sha(opb)[:16] == 'b89e4c909f37e163', sha16=sha(opb)[:16])
ck('Q1.ORDEM_DO_OPERADOR_and_ORIGINAL_equal_verbatim', (W / 'ORDEM_DO_OPERADOR.txt').read_bytes() == opb and (W / 'ORIGINAL.txt').read_bytes() == opb)
o6 = Path(r'C:\IALD\TUNEL_CLAUDE_APP\ORDEM_006_release_v407_do_app.md')
out['ORDEM_006_sha16_now'] = sha(o6.read_bytes())[:16]
cs = rd(W / 'CUSTODIA_v407_ESTADO.json')
claimed16 = re.search(r'sha16 ([0-9a-f]{16})', cs['ordem_006']).group(1)
out['ORDEM_006_sha16_claimed'] = claimed16
ck('Q1.ORDEM_006_sha16_matches_claim', sha(o6.read_bytes())[:16] == claimed16, now=sha(o6.read_bytes())[:16], claimed=claimed16)

# --- estado da custodia (PUBLICADA segundo a ORDEM_006) x plano G1 x conferencia final
plan_p = Path(cs['plano_g1']['path'])
plan = rd(plan_p)
out['custodia_plan_sha16_recorded_by_builder'] = cs['plano_g1']['sha256'][:16]
out['custodia_plan_sha16_now'] = sha(plan_p.read_bytes())[:16]
out['custodia_plan_changed_since_builder_snapshot'] = sha(plan_p.read_bytes()) != cs['plano_g1']['sha256']
ck('Q1.custodia_plan_live_fields_monotone_vs_builder_snapshot', plan['versao'] == 'v407' and plan['corrente'] is True and plan['relacao_espelho'] == 'igual' and plan['completo'] is False and set(plan['pendentes']) <= set(cs['campos_do_plano']['pendentes']) and plan['contagem'].get('OPERADOR') == 1,
   plan_completo=plan['completo'], plan_pendentes_now=plan['pendentes'], builder_pendentes=cs['campos_do_plano']['pendentes'], plan_contagem_now=plan['contagem'], relacao=plan['relacao_espelho'], note='CUSTODIA_v407_ESTADO.json do construtor esta defasado (plano andou: 8 -> 2 pendentes); direcao correta; INFO')
cf_p = Path(cs['conferencia_final_da_custodia']['path'])
cf = rd(cf_p)
ck('Q1.conferencia_final_sha_and_ok', sha(cf_p.read_bytes()) == cs['conferencia_final_da_custodia']['sha256'] and cf.get('ok') == cf.get('total') == 13 and cf.get('versao') == 'v407' and cf.get('pin', '').startswith('833121339e649f71'),
   itens=cf.get('total'), cf_ok=cf.get('ok'), cf_items=[(i['item'], i['ok']) for i in cf['itens']][:13], sha16=sha(cf_p.read_bytes())[:16])
out['plan_pendentes_do_operador'] = plan.get('pendentes_do_operador')
out['plan_pendentes'] = plan.get('pendentes')
# detalhe dos itens pendentes do plano (para o parecer: o que ainda falta e de quem)
itens = plan.get('itens') or plan.get('items') or []
out['plan_item_keys_sample'] = list(itens[0].keys()) if itens and isinstance(itens, list) and isinstance(itens[0], dict) else (list(plan.keys())[:20])

json.dump({'out': out, 'checks': chk}, open(OUT / 'q1_sources_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps({'n_checks': len(chk), 'fails': [c for c in chk if not c['pass']]}, ensure_ascii=False, indent=1)[:3500])
print(json.dumps({k: out[k] for k in ('git_refs', 'git_tracked_changes_in_mirror_worktree', 'nos_live', 'vault_equals_git_blob', 'plan_pendentes', 'ORDEM_006_sha16_now', 'ORDEM_006_sha16_claimed')}, ensure_ascii=False, indent=1)[:3500])
