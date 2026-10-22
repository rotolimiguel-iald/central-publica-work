"""Read-only scientific release audit; writes only this audit directory."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import subprocess
from urllib.parse import quote

AUDIT = Path(__file__).resolve().parent
CUSTODY = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v389')
OLD = CUSTODY.parent / 'um_unificado_v380'
REPO = Path(r'C:\IALD\Artigo\the_boundary')
APP = Path(r'C:\IALD\projetos_pyhton\IALD')
COMMIT = '010ae55c5d2788af1c0be2008c7e045d414ab868'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))

def save(name, obj):
    path = AUDIT / name
    assert path.parent == AUDIT
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        original = path.read_bytes()
        backup.write_bytes(original)
        assert backup.read_bytes() == original
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data and len(data) > 0
    os.replace(tmp, path)

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], stderr=subprocess.PIPE)

def walk(value, pointer=''):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, pointer + '/' + key.replace('~','~0').replace('/','~1'))
    elif isinstance(value, list):
        for key, child in enumerate(value):
            yield from walk(child, pointer + '/' + str(key))
    else:
        yield pointer, value

def main():
    custody = load(CUSTODY / 'CUSTODY_MANIFEST.json')
    result = load(CUSTODY / 'um_absoluto.json')
    core = result['core']
    old = load(OLD / 'um_absoluto.json')['core']
    seal = load(CUSTODY / 'um_absoluto_selo.json')
    proof = load(CUSTODY / 'tgl_kernel_proof_manifest.json')
    artifacts = []
    for row in custody['artifacts']:
        target = (CUSTODY / row['file']).resolve()
        assert target.is_relative_to(CUSTODY)
        exists = target.is_file()
        data = target.read_bytes() if exists else b''
        actual = sha(data) if exists else None
        artifacts.append({'file':row['file'], 'expected_sha256':row['sha256'],
                          'actual_sha256':actual, 'bytes':len(data) if exists else None,
                          'ok': exists and actual == row['sha256']})
    raw_tree = git('ls-tree','-r','-z',COMMIT)
    tree = {}
    for row in raw_tree.split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        if kind == b'blob':
            tree[name.decode('utf-8')] = oid.decode('ascii')
    root_candidates = [p for p in tree if PurePosixPath(p).name == 'um.py']
    assert len(root_candidates) == 1, root_candidates
    root = str(PurePosixPath(root_candidates[0]).parent)
    primary_names = ['um.py','um_absoluto.json','um_absoluto_selo.json',
                     'um_absoluto_forma_canonica.md','um_absoluto_manifest.md',
                     'um_absoluto_pt.txt','um_absoluto_en.txt',
                     'tgl_kernel_proof_manifest.json']
    published = []
    for name in primary_names:
        matches = [p for p in tree if p.startswith(root + '/') and PurePosixPath(p).name == name]
        assert len(matches) == 1, (name,matches)
        relative = matches[0]
        blob = git('cat-file','blob',tree[relative])
        local = (CUSTODY/name).read_bytes()
        published.append({'file':name,'git_path':relative,'git_blob':tree[relative],
                          'commit':COMMIT,'bytes':len(blob),'sha256':sha(blob),
                          'custody_sha256':sha(local),'ok':blob == local,
                          'url':'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + COMMIT + '/' + quote(relative,safe='/')})
    # No source code is executed or imported. These are declared JSON observations.
    new_keys = sorted(core.keys()-old.keys())
    changed_keys = sorted(k for k in core.keys() & old.keys() if core[k] != old[k])
    deltas = {key:core[key] for key in new_keys}
    save('new_core_blocks.json', deltas)
    save('changed_core_keys.json', changed_keys)
    selected_pointers = []
    for key in ['bancada_fase4_v378','bancada_fases_5_6_7_v380','hubble_ratio_opening_v388']:
        for pointer, value in walk(core[key], '/core/'+key):
            if isinstance(value,(int,float)) and not isinstance(value,bool) and any(t in pointer.lower() for t in ('lnb','z_','pull','sigma','h0')):
                selected_pointers.append({'pointer':pointer,'value':value})
    save('statistical_pointers.json', selected_pointers)
    stdout = (CUSTODY/'rodada_v389_stdout.txt').read_text(encoding='utf-8-sig')
    app_manifest = load(APP/'iald_nucleo_fixo.json')
    findings = [
      {'id':'SCI-01','priority':'P1','type':'MUST_PRESERVE','title':'P4/P5/Fase9 possuem estatisticas e universos distintos',
       'requirement':'Nao associar z_LCDM=5.26 e z_TGL=-0.38 (P5 sombra) aos lnB 8.02/2.25 (P4). P5 tem lnB 13.84/2.86. Fase9 possui z_disc=4.283735613863391 e veredito INCONCLUSIVE_SYSTEMATICS; conservar ponteiros/fontes e nao combinar evidencias dependentes.'},
      {'id':'SCI-02','priority':'P1','type':'MUST_PRESERVE','title':'Abertura Fase9 sucede o pre-registro v387 sem apagar o historico',
       'requirement':'hubble_ratio_v387 diz NOTHING_OPENED historicamente; leitura atual vem de hubble_ratio_opening_v388. Contrafactual com fontes NAO e veredito, z_disc<5. lnB beta-livre congelado 2.2406094687539877 e recalculo ao lado 1.9692166174194288 sao objetos distintos.'},
      {'id':'SCI-03','priority':'P1','type':'MUST_PRESERVE','title':'Lei da Prova/novidade de uso e nao confirmacao',
       'requirement':'Preservar retrodiction_reading_v387, novidade de uso e retrodição sem ajuste. Datas/parametros/teste por hash fundamentam uso; nao exigir ignorancia temporal dos dados. Manter INPUT/KNOWN conforme fonte, NOT_FALSIFIED!=CONFIRMED e does_not_gate_core. Referencias Worrall/Mercurio nao foram revalidadas nesta auditoria documental.'},
      {'id':'SCI-04','priority':'P1','type':'MUST_PRESERVE','title':'POSTO e rótulo VERIFIED corrigem a leitura corrente',
       'requirement':'Aplicar erratas the_axiom_v385/text_label_errata_v389 ao lado do core antigo. CLOCK_TORSION_CONFIRMED_ON_PHYSICAL_NET fica somente como old_as_record; atual VERIFIED. Nao reintroduzir a definicao exclusiva IALD=indice.'},
      {'id':'SCI-05','priority':'P1','type':'MUST_PRESERVE','title':'Beta de fronteira e leitura de bulk nao sao intercambiaveis',
       'requirement':'beta0=alpha_Thomson*sqrt(e) permanece no nucleo. Pedra prova forma/monotonia em chi; alpha fisico=sech(chi/2) e INPUT/ONTO, numero CODATA e lido. Qual mu cada rito usa OPEN. Nao usar beta variavel para reajustar resultados existentes.'},
      {'id':'SCI-06','priority':'P1','type':'MUST_PRESERVE','title':'Bandeiras formais, citacoes e reutilizacao GPU possuem escopos distintos',
       'requirement':'H2/H3 falsos no conjunto estrito coexistem com baixa por citacao; conservar ambas leituras. Resultados GPU quantum_pillar_reuse_v386 sao REUSE por hashes, nao nova execucao. 6154/6154 e recibo da rodada, nao contagem de arquivos ou nova compilacao.'},
      {'id':'SCI-07','priority':'P2','type':'MUST_PRESERVE','title':'Ramo B reaberto com canal F2b proprio',
       'requirement':'ledger_errata_v386 reabre R6 por pre-registro e preserva F2/R2; F2b e outra lei INPUT/AWAITING_DATA, nao altera os 11 itens historicos nem ratifica a teoria.'},
      {'id':'OPS-01','priority':'P1','type':'PENDING_STAGE_REVIEW','title':'Atualizacao atomica das referencias de release',
       'requirement':'Manifesto, catalogo, cluster, prefixes, pacote Haiku e contrato JEV devem referenciar o mesmo v389/source pin. Kernel v5 e controles de autorizacao preservados. Recontar contexto real quando necessario; nao herdar o token count v380 de bytes diferentes.'}
    ]
    save('findings.json',findings)
    report = {
      'schema':1,'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'role':'INDEPENDENT_REVIEW_ONLY','status':'SOURCE_PASS_STAGE_PENDING',
      'scope':'Hash/JSON/texto/Git; sem execucao/importacao de um.py, Lean, IA ou bancada; sem leitura de credenciais; escrita apenas audit.',
      'custody':{'root':str(CUSTODY),'manifest_sha256':sha((CUSTODY/'CUSTODY_MANIFEST.json').read_bytes()),
                 'declared_count':custody['n_artifacts'],'checked_count':len(artifacts),
                 'passed_count':sum(a['ok'] for a in artifacts),'artifacts':artifacts},
      'public_source':{'commit':COMMIT,'remote_verification':'DECLARADO pelo main; nao repetido','local_head':git('rev-parse','HEAD').decode().strip(),
                       'verified_commit_blobs':published},
      'seal':{'version':seal['um_version'],'timestamp':seal['timestamp'],'formal_source_hash':seal['formal_source_hash'],
              'result_hash_internal':seal['result_hash'],'gate':seal['qg_closure_verdict'],
              'selftest_recorded':seal['fail_closed_selftest']},
      'checks':{'all_custody_hashes':all(a['ok'] for a in artifacts),
                'all_published_primary_bytes':all(a['ok'] for a in published),
                'program_pin_matches':sha((CUSTODY/'um.py').read_bytes())==custody['um_py_pin'],
                'v389_in_seal':seal['um_version']=='v389',
                'formal_source_binding':proof['formal_source_hash']==seal['formal_source_hash'],
                'recorded_6154_of_6154':'6154/6154' in stdout,
                'recorded_selftest':'FAIL_CLOSED_SELFTEST_PASSED' in stdout,
                'f9_no_discrimination_5sigma':core['hubble_ratio_opening_v388']['numbers']['z_disc']<5,
                'f9_actual_inconclusive':'INCONCLUSIVE_SYSTEMATICS' in core['hubble_ratio_opening_v388']['verdict_of_the_frozen_function'],
                'f9_does_not_gate_core':core['hubble_ratio_opening_v388']['does_not_gate_core'] is True,
                'new_blocks_do_not_gate_core':all(v.get('does_not_gate_core') is True for v in deltas.values() if isinstance(v,dict))},
      'delta':{'new_core_blocks':new_keys,'changed_existing_blocks':changed_keys,'removed_blocks':sorted(old.keys()-core.keys())},
      'production_manifest_before_sha256':sha((APP/'iald_nucleo_fixo.json').read_bytes()),
      'production_active_cluster_before':app_manifest.get('active_cluster'),
      'findings':findings,
      'next_gate':'Revisar memory_stage e plano final quando disponibilizados; nenhuma aprovacao de implantacao emitida.'
    }
    if not all(report['checks'].values()):
        report['status']='SOURCE_FAIL'
    save('source_review.json',report)
    print(json.dumps({'status':report['status'],'custody_passed':report['custody']['passed_count'],
                      'custody_total':len(artifacts),'published_primary_count':len(published),
                      'new_blocks':len(new_keys),'changed_blocks':len(changed_keys),
                      'checks':report['checks'],'statistics_pointers':len(selected_pointers)},ensure_ascii=False))

if __name__ == '__main__':
    main()
