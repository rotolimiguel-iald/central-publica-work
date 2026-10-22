from pathlib import Path
from datetime import datetime
import hashlib, json, os, re

R = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT = R/'revisao_b6'; S = R/'s'; BUILD = S/'.lake/build/lib/lean'
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def load(p): return json.loads(p.read_bytes())
def ck(r): assert pin(Path(r['path'])) == r, r
def save(p, value, text=False):
    assert p.resolve().is_relative_to(OUT.resolve())
    b = value.encode('utf8') if text else (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf8')
    assert not p.exists(), ('Preserve existing result; write an explicit addendum', str(p))
    tmp = p.with_name(p.name+'.tmp_'+STAMP)
    with tmp.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == b
    os.replace(tmp, p)
def norm(x): return re.sub(r'\.\{[^}]*\}', '', x).strip()
def parse_axioms(text):
    out = {}
    for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))", text, re.S):
        n = norm(m.group(1))
        v = [] if m.group(3) else [norm(x) for x in m.group(2).split(',') if x.strip()]
        assert n not in out or out[n] == v
        out[n] = v
    return out

ptr = load(OUT/'B6_SNAPSHOT_POINTER.json'); ck(ptr['snapshot'])
A = Path(ptr['attempt']); snap = load(Path(ptr['snapshot']['path']))
completion = load(A/'completion.json'); assert completion['status'] == 'BUILD_RC0__REVIEW_PENDING'
ck(completion['run']); run = load(A/'run.json'); assert run['returncode'] == 0
for p in run['streams']+run['executables']+snap['protected_before']+snap['documents']+snap['source_configs']+[snap['own_auditor'], snap['inherited_B5_compilation']]: ck(p)
for x in snap['sources']: ck(x['source']); ck(x['copy'])
for x in snap['inherited_project_objects']: ck(x['object']); ck(x['trace'])
for x in snap['cache_inheritance']: ck(x['pins'])
targets = snap['targets']; assert len(targets) == len(set(targets)) == 10
tracepath = BUILD/'TGLExt/ReviewPassageScope.trace'; trace = load(tracepath)
ax = {}; types = {}
for entry in trace['log']:
    assert entry.get('level') not in ['error', 'warning'], entry
    if entry.get('level') != 'info': continue
    text = entry['message']
    if 'depends on axioms:' in text or 'does not depend on any axioms' in text:
        ax.update(parse_axioms(text))
    else:
        text = re.sub(r'^.*?\.lean:\d+:\d+:\s*', '', text, count=1)
        for t in targets:
            if re.match(re.escape(t)+r'(?:\.\{[^}]*\})?(?:\s|$)', text):
                assert t not in types; types[t] = text
assert set(ax) == set(types) == set(targets)
assert all(set(a) <= {'propext', 'Classical.choice', 'Quot.sound'} for a in ax.values())
assert sum(not a for a in ax.values()) == 3
author_copy_trace = BUILD/'TGLExt/AuditPassageScope.trace'
assert parse_axioms('\n'.join(e['message'] for e in load(author_copy_trace)['log'] if e.get('level') == 'info')) == ax

newmods = [x['module'] for x in snap['sources'] if x['new_source_copy']] + ['TGLExt.ReviewPassageScope']
objects = []; warnings = []
for mod in newmods:
    p = BUILD/(mod.replace('.', '/')+'.olean'); tp = p.with_suffix('.trace'); tr = load(tp)
    for e in tr['log']:
        assert e.get('level') != 'error', e
        if e.get('level') == 'warning': warnings.append(dict(module=mod, **e))
        if e.get('level') == 'trace' and 'LEAN_PATH=' in e.get('message', ''):
            search = e['message'].split('LEAN_PATH=', 1)[1].split(' c:', 1)[0]
            assert str(R/'kernel'/'.lake') not in search and 'V351' not in search
    ob = dict(module=mod, own=pin(p), trace=pin(tp), author=None, equal_to_author=None)
    if mod != 'TGLExt.ReviewPassageScope':
        ap = R/'kernel/.lake/build/lib/lean'/p.relative_to(BUILD)
        ob['author'] = pin(ap); ob['equal_to_author'] = ob['own']['sha256'] == ob['author']['sha256']
        assert ob['equal_to_author'], mod
    objects.append(ob)
assert not any(w['module'] in ['TGLExt.AuditPassageScope', 'TGLExt.ReviewPassageScope'] for w in warnings)
allobjects = [p for p in BUILD.rglob('*.olean') if p.relative_to(BUILD).parts[0] in ['TGL','TGLExt']]
assert len(allobjects) == len(snap['inherited_project_objects']) + len(objects) == 141

aupath = R/'AUDITORIA_B6.json'; au = load(aupath)
for p in au['sources']+au['objects']+[au['positive_build'],au['proposal'],au['documentary_validation']]: ck(p)
arun = load(Path(au['positive_build']['path'])); assert arun['returncode'] == 0
for x in arun['snapshots']:
    assert pin(Path(x['path']))['sha256'] == x['sha256'] == pin(Path(x['snapshot']))['sha256']
assert au['axioms'] == ax
assert au['targets'] == load(R/'ALVOS_B6.json')
assert [sum(t['kind'] == k for t in au['targets']) for k in ['theorem','structure']] == [8,2]
assert au['new_theorems'] == 0 and au['new_negative_probes'] is False
commands = []
for c in au['commands']:
    for key in ['source','stdout','stderr']: ck(c[key])
    assert c['returncode'] == 0
    assert parse_axioms(Path(c['stdout']['path']).read_text(encoding='utf8')) == ax
    commands.append(dict(**c, scope='Author execution reread by source/streams; not rerun'))

fiche = load(R/'REAPROVEITAMENTO_B6.json'); providers = []
for pr in fiche['providers']:
    p = Path(pr['path']); assert pin(p)['sha256'] == pr['sha256']
    line = p.read_text(encoding='utf-8-sig').splitlines()[pr['line']-1]
    assert pr['name'] in line
    providers.append(dict(**pr, verified_file=pin(p), line_read=line))
proposal = load(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json')
valid = load(R/'VALIDACAO_DOCUMENTAL_B6.json'); ck(valid['proposal'])
entries = proposal['external_known_theorems']; assert len(entries) == 4
for e in entries:
    assert {'name','status','citation','exact_role','verified_url','source_read_scope','imported_into_witness'} <= set(e)
    assert e['imported_into_witness'] is False and e['status'] == 'KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED'
    assert all(isinstance(e[k],str) and e[k] for k in ['name','citation','exact_role','verified_url','source_read_scope'])
assert len(proposal['scope']) == 11
expected = ['IMPORTED','INPUT','INPUT','INPUT','REAL','REAL','INPUT','OPEN','OPEN','INPUT','REAL']
assert [x['status'] for x in proposal['scope']] == expected
for key in ['changes_gate','implements_runtime','chooses_route']:
    assert proposal[key] is False and valid[key] is False
assert valid['entries'] == 4 and valid['all_imported_into_witness_false'] and valid['all_statuses_typed']
scope_notes = [
    'IMPORTED is explicitly conditional: master and imported:H2->H3 must be supplied. No horizon premise constructed by modus ponens.',
    'AreaScale is a conditional algebraic calibration, not a numerical derivation of G. The unrestricted division identity at G=0 carries no physical calibration.',
    'SectorFluid keeps H_nx as HasDerivAt input and w depending only on sector; aggregation consumes these assumptions.',
    'HubbleHorizonInput.differential_entropy is a separate prescription. The derivative of A/(4G Phi(t)) retains the Phi-prime term.',
    'Conditional B4 comparison requires positive total density and nonnegative total enthalpy; no route selection.',
    'Phi_flux uniqueness requires nonzero total enthalpy. Zero total flux has no unique factor.',
    'INPUT here refers to choosing the zero integration constant. The general existential Lambda/C result is proved and retained, not assumed to vanish.',
    'Global Lemma 3 remains OPEN; no local-to-global identification claimed.',
    'TGL-S/TGL-L perturbative choice remains OPEN. Background H_nx does not settle it.',
    'TGLCoupling has beta in (0,1); alpha=beta/exp(1/2) is a form, not a measured or derived numeral.',
    'The angle corollary rewrites sin squared thetaMiguel(beta)=beta; it adds no dynamic law or independent observable.'
]
scope_checked = [dict(**row, review=note) for row,note in zip(proposal['scope'],scope_notes)]
prior_maps = {}
for stage in ['b3','b4','b5']:
    comp = load(R/('revisao_'+stage)/'compilation.json'); prior_maps.update(comp['targets'])
for n in proposal['correction_providers']: assert n in prior_maps, n
for i in [4,5,6,10]: assert proposal['scope'][i]['provider'] in prior_maps
source_audit = (R/'kernel/TGLExt/AuditPassageScope.lean').read_text(encoding='utf-8-sig')
assert len(re.findall(r'^#check\s+',source_audit,re.M)) == 10
assert len(re.findall(r'^#print axioms\s+',source_audit,re.M)) == 10
order = Path(fiche['order']['path']); assert pin(order)['sha256'] == fiche['order']['sha256']
olines = order.read_text(encoding='utf-8-sig').splitlines()
oi = next(i for i,l in enumerate(olines) if l.startswith('### B6'))
chronology = []
for p in [R/'REAPROVEITAMENTO_B6.md',R/'REAPROVEITAMENTO_B6.json',R/'kernel/TGLExt/AuditPassageScope.lean',R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json']:
    st=p.stat(); chronology.append(dict(file=pin(p),created_local=datetime.fromtimestamp(st.st_ctime).astimezone().isoformat(),modified_local=datetime.fromtimestamp(st.st_mtime).astimezone().isoformat()))
assert (R/'REAPROVEITAMENTO_B6.json').stat().st_mtime < (R/'kernel/TGLExt/AuditPassageScope.lean').stat().st_ctime
um_pin = pin(R/'um.py'); assert all(um_pin['sha256'] == c['sha256'] for c in fiche['consumers'])
documentary = dict(timestamp=datetime.now().astimezone().isoformat(),order=pin(order),B6_lines=[oi+1,oi+5],B6_excerpt='\n'.join(olines[oi:oi+5]),fiche=[pin(R/'REAPROVEITAMENTO_B6.md'),pin(R/'REAPROVEITAMENTO_B6.json')],providers=providers,proposal=pin(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json'),validation=pin(R/'VALIDACAO_DOCUMENTAL_B6.json'),four_entries_schema_passed=True,eleven_scope_rows=scope_checked,correction_providers_in_own_prior_audits=proposal['correction_providers'],chronology=chronology,fiche_precedes_auditor_by_local_metadata=True,copied_um_matches_fiche=um_pin,integration_performed=False,findings=[])
save(A/'documentary_inspection.json',documentary)
references = dict(timestamp=datetime.now().astimezone().isoformat(),method='Limited primary HTML reading with web tool; no PDF download or exhaustive literature review',entries=[
    dict(url=entries[0]['verified_url'],scope='Primary HTML, local equilibrium/area/Unruh temperature hypotheses and equations (1)-(6).',conclusion='The relation is conditional on local horizon premises; neither G calibration nor Phi_TGL is supplied by this citation.'),
    dict(url=entries[1]['verified_url'],scope='Inherited own B4 primary HTML section 2 reading and pinned contract_and_fiche evidence.',evidence=pin(R/'revisao_b4/independent_20260914_170247_181979/contract_and_fiche.json'),conclusion='Heat convention -dE/dt; radius factor H*r_A retained, flat expanding horizon r_A=1/H. Dynamical temperature prescription remains explicit.'),
    dict(url=entries[2]['verified_url'],scope='Primary HTML abstract and initial introduction; no full-paper review.',conclusion='Contextual review, not a supplier of Phi or route selection.'),
    dict(url=entries[3]['verified_url'],scope='Official APS metadata and abstract read independently; PDF not accessed. Historical author PDF401 not reproduced or erased.',conclusion='Cosmological event horizons in the considered positive-cosmological-constant setting; not a general dynamical-FLRW theorem.')],imported_into_witness=[False]*4,findings=[])
save(A/'reference_inspection.json',references)

stamp = datetime.now().astimezone().isoformat()
compilation = dict(timestamp=stamp,status='INDEPENDENT_B6_LAKE_RC0',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This B6 private Lake run only; prior failures remain in prior manifests',run=pin(A/'run.json'),runs=[dict(label='B6',run=pin(A/'run.json'),returncode=0)],source_snapshot=ptr['snapshot'],targets={t:dict(typecheck=types[t],axioms=ax[t]) for t in targets},exact_target_count=10,existing_theorems=8,existing_structures=2,new_theorems=0,new_definitions=0,all_axioms_allowed=True,empty_axiom_targets=[t for t in targets if not ax[t]],all_target_typechecks_present=True,auditor_trace=pin(tracepath),objects=objects,new_project_object_count=len(objects),private_project_object_count=len(allobjects),inherited_B5_compilation=snap['inherited_B5_compilation'],inherited_project_objects=snap['inherited_project_objects'],inherited_project_objects_unchanged=True,new_B6_auditor_warnings=[],existing_supplier_warnings=warnings,author_project_objects_copied=False,cache_inheritance=snap['cache_inheritance'],cache_manifest_pins_rechecked=True,package_cache_not_rebuilt_or_fully_rehashed_this_turn=True,prior_protected_unchanged=True,protected_pins=snap['protected_before'])
save(OUT/'compilation.json',compilation)
evidence = dict(timestamp=stamp,status='B6_DOCUMENTARY_REVIEW_ACCEPTED__PROPOSAL_NOT_INSTALLED',marker='B6_SCOPE_REVIEW',P0=[],P1=[],P2=[],findings=[],compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json'),source_snapshot=ptr['snapshot'],documentary_inspection=pin(A/'documentary_inspection.json'),reference_inspection=pin(A/'reference_inspection.json'),author_audit=pin(aupath),author_positive_build=au['positive_build'],author_commands=commands,baseline_941_preservation='DECLARADO in author audit; no repeated broad source scan',copied_um_matches_fiche=um_pin,protected_prior_reports=snap['protected_before'],prior_unchanged=True,scope='B6 documentary proposal, four external references and eleven statuses; own audit of ten existing declarations. No new theorem, runtime, gate mutation, D1, route choice or A1 work.')
save(OUT/'REVIEW_B6_FINAL.json',evidence)
audob=next(x for x in objects if x['module']=='TGLExt.AuditPassageScope')
audsource=next(x['source'] for x in snap['sources'] if x['module']=='TGLExt.AuditPassageScope')
status_table='\n'.join('| '+str(i+1)+' | '+r['item']+' | '+r['status']+' | '+r['condition']+' |' for i,r in enumerate(scope_checked))
warnmods=sorted(set(w['module'] for w in warnings))
md=f'''# B6 — revisão independente documental final

{stamp} · **B6_SCOPE_REVIEW**

[REAL] **Aceito no escopo B6, sem P0, P1 ou P2.** Ficha MD/JSON, proposta, validação, auditor e tipos dos fornecedores conferidos. A reprodução Lake própria terminou rc0 e auditou **dez declarações EXISTENTES: oito teoremas e duas estruturas; zero teoremas novos**. A proposta permanece documental, **não instalada no witness ou no runtime**.

## Tipos e alcance

`the_trio_is_a_pair` recebe `master : H1 ∧ H2 ∧ H3 → P` e `imported : H2 → H3`; `discharge_by_import` aplica uma implicação já fornecida. Nenhum deles constrói a premissa física H3. `the_pair_still_needs_its_hypotheses` preserva justamente a insuficiência da implicação desacompanhada das hipóteses. Os três não dependem de axiomas; os outros sete usam somente **propext, Classical.choice, Quot.sound**, com universos normalizados no parser próprio. “all_trio” foi interpretado como subconjunto permitido, não como presença obrigatória dos três.

`AreaScale` fornece identidades de normalização, sem medir/derivar G. A identidade total de divisão, inclusive sua elaboração em G=0, não constitui calibração física; a interpretação usa G>0. As estruturas `SectorFluid` e `HubbleHorizonInput` mantêm H_nx e a lei diferencial de entropia como campos de entrada. A derivada do quociente contém Phi′. A igualdade das rotas usa suporte de **densidade positiva**, incluindo vácuo quando aplicável, e a unicidade do fator de fluxo exige entalpia total não nula.

## Onze estatutos conferidos

| # | Item | Estatuto | Condição mantida |
|---|---|---|---|
{status_table}

No item “constante de integração”, INPUT refere-se à **escolha do caso zero**; não apaga a existência de Λ/C no resultado geral. Os itens REAL são teoremas condicionais já reproduzidos em B3–B5, não ratificação experimental. As quatro correções explícitas de B4 e a recusa de seu contrato literal continuam preservadas.

## Referências e integração

As quatro entradas têm `KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED`, papel delimitado e **imported_into_witness:false**. Schema e onze linhas foram checados independentemente contra os arquivos atuais, sem usar o booleano da validação como substituto da leitura.

- [Jacobson 1995]({entries[0]['verified_url']}): HTML primário lido nas hipóteses e derivação local; o argumento exige equilíbrio, proporcionalidade área/entropia, temperatura e balanço. A citação não fornece H3 da realização nem Phi_TGL.
- [Cai–Kim 2005]({entries[1]['verified_url']}): herança explícita da leitura primária própria de B4, seção 2; calor −dE, fator **H r_A**, e prescrição de temperatura no horizonte aparente. Não se restaura o fluxo literal sem raio.
- [Padmanabhan 2010]({entries[2]['verified_url']}): resumo e início da introdução relidos; referência de enquadramento, sem alegar leitura integral ou fornecedor de Phi/G.
- [Gibbons–Hawking 1977]({entries[3]['verified_url']}): metadados e resumo APS relidos; horizonte de eventos cosmológico no regime considerado. O PDF não foi lido nesta revisão. A limitação autoral histórica HTTP401 permanece explícita; não se atribui ao artigo uma prova geral de FLRW dinâmico.

A cláusula B6 da ORDEM 012 (linhas {oi+1}–{oi+5}) é atendida como **proposta** para gerência. `changes_gate`, `implements_runtime` e `chooses_route` são false. Não se revisou/instalou toda a lista antiga EXTERNAL_KNOWN_THEOREMS, nem se alterou D1, A1, campos de gate, código canônico ou memórias.

## Reprodução e proveniência

Raiz curta `{S}`. Comando próprio: `lake build TGLExt.AuditPassageScope TGLExt.ReviewPassageScope`, Lean 4.31.0. Auditor autoral copiado byte a byte, mais auditor independente de `#check` com universos e `#print axioms`. Os **{len(objects)-2} fornecedores existentes faltantes** foram reconstruídos de fontes copiadas, sem objetos autorais. Com os dois auditores, **{len(objects)} novos objetos privados**, somados aos **120 próprios anteriores preservados**, dão **{len(allobjects)}**. Os {len(objects)-1} objetos com equivalente autoral coincidem byte a byte, inclusive AuditPassageScope.

Nenhum aviso nos dois auditores B6. Foram preservados **{len(warnings)} avisos de fornecedores existentes** ({', '.join(warnmods)}), ligados às traces no JSON. O total de jobs mostrado por Lake inclui reuso; não é contagem de novas provas. Fontes e objetos/traces previamente pinados B1–B5 e relatórios/compilations protegidos foram revalidados sem alteração.

Mathlib e oito pacotes auxiliares vêm do cache privado cuja cópia/pins foram registrados em B1/B2 e herdados até B5. Nesta rodada se reconferiram os manifestos e configuração/toolchain; **não se reconstruiu nem se rehashou integralmente o cache**. LEAN_PATH do build usa o projeto privado e pacotes; nenhum objeto TGL/TGLExt autoral foi copiado. Não se executou monólito ou auditor autoral.

Auditoria autoral e seus streams rc0 foram relidos e coincidem com os dez resultados próprios. Não foram criados novos negativos: B6 não acrescenta asserção matemática. A preservação ampla das 941 fontes continua [DECLARADO] no auditor autoral, sem nova varredura. O hash da cópia ROOT/um.py foi lido e coincide com a ficha. A cronologia local coloca a ficha antes do auditor; não é selo externo de tempo.

## Pins e saída

- Auditor fonte: `{audsource['sha256']}`.
- Auditor .olean próprio = autor: `{audob['own']['sha256']}`.
- Proposta documental: `{pin(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json')['sha256']}`.
- [Revisão JSON](<{(OUT/'REVIEW_B6_FINAL.json').as_posix()}>) — `{pin(OUT/'REVIEW_B6_FINAL.json')['sha256']}`.
- [Compilação própria](<{(OUT/'compilation.json').as_posix()}>) — `{pin(OUT/'compilation.json')['sha256']}`.
- [Run rc0](<{(A/'run.json').as_posix()}>) — `{pin(A/'run.json')['sha256']}`.
- [Snapshot](<{(A/'snapshot.json').as_posix()}>), [tabela/ficha](<{(A/'documentary_inspection.json').as_posix()}>) e [referências](<{(A/'reference_inspection.json').as_posix()}>).

**B6 concluído no escopo solicitado.** Não resta build, negativo ou pesquisa deste delta. Esta revisão não é entrega pelo túnel, instalação da proposta ou nova custódia. Nenhum alvo posterior foi iniciado.
'''
save(OUT/'REVIEW_B6_FINAL.md',md,True)
for x in snap['protected_before']: ck(x)
print(json.dumps(dict(status=evidence['status'],P0=[],P1=[],P2=[],report=pin(OUT/'REVIEW_B6_FINAL.md'),json=pin(OUT/'REVIEW_B6_FINAL.json'),compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json')),ensure_ascii=False,indent=2))
