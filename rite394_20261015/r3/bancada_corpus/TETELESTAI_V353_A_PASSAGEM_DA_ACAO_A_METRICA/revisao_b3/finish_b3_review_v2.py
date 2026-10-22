from pathlib import Path
from datetime import datetime
import hashlib, json, os, re

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=R/'revisao_b3'; S=R/'s'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
BUILD=S/'.lake'/'build'/'lib'/'lean'
FINAL={'TGLExt.SectorFluidClosure','TGLExt.SectorFriedmann','TGLExt.AuditSector'}
ALLOWED={'propext','Classical.choice','Quot.sound'}

def pin(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def checkpin(rec):assert pin(Path(rec['path']))==rec,rec
def save(p,d,text=False):
    assert p.resolve().is_relative_to(OUT.resolve())
    b=d.encode('utf8') if text else (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    if p.exists():
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+STAMP)
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+STAMP)
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    os.replace(tmp,p)
def norm(s):return re.sub(r'\.\{[^}]*\}','',s).strip()
def axioms(text):
    result={}
    for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))",text,re.S):
        name=norm(m.group(1)); ax=[] if m.group(3) else [norm(x) for x in m.group(2).split(',') if x.strip()]
        assert name not in result or result[name]==ax,(name,'Conflicting axiom output')
        result[name]=ax
    return result

ptr=load(OUT/'B3_SNAPSHOT_POINTER.json');checkpin(ptr['snapshot'])
A=Path(ptr['attempt']);snap=load(Path(ptr['snapshot']['path']))
comp=load(A/'completion.json');assert comp['status']=='BUILD_RC0__SEMANTIC_AND_AXIOM_AUDIT_PENDING'
checkpin(comp['run']);run=load(A/'run.json');assert run['returncode']==0
for p in run['streams']+run['executables']:checkpin(p)
for p in snap['protected_before']+snap['documents']+snap['source_configs']+[snap['own_auditor'],snap['inherited_B2_compilation']]:checkpin(p)
for r in snap['sources']:checkpin(r['source']);checkpin(r['copy'])
for r in snap['inherited_project_objects']:checkpin(r['object']);checkpin(r['trace'])

targets=snap['targets'];assert len(targets)==len(set(targets))==22
tracepath=BUILD/'TGLExt'/'ReviewSector.trace';trace=load(tracepath)
ax={};types={}
for log in trace['log']:
    assert log.get('level') not in ['error','warning'],log
    if log.get('level')!='info':continue
    message=log['message']
    if 'depends on axioms:' in message or 'does not depend on any axioms' in message:
        parsed=axioms(message)
        for k,v in parsed.items():
            assert k not in ax or ax[k]==v
            ax[k]=v
    else:
        text=re.sub(r'^.*?\.lean:\d+:\d+:\s*','',message,count=1)
        for t in targets:
            if re.match(re.escape(t)+r'(?:\.\{[^}]*\})?(?:\s|$)',text):
                assert t not in types,t
                types[t]=text
assert set(ax)==set(targets),(set(targets)-set(ax),set(ax)-set(targets))
assert set(types)==set(targets),set(targets)-set(types)
assert all(set(v)<=ALLOWED for v in ax.values()),ax
checks={t:dict(typecheck=types[t],axioms=ax[t]) for t in targets}
author_trace=load(BUILD/'TGLExt'/'AuditSector.trace')
assert axioms('\n'.join(x['message'] for x in author_trace['log'] if x.get('level')=='info'))==ax

objects=[];warnings=[]
newmods=[r['module'] for r in snap['sources'] if r['new_source_copy']]+['TGLExt.ReviewSector']
for mod in newmods:
    p=BUILD/(mod.replace('.','/')+'.olean');tr=p.with_suffix('.trace');td=load(tr)
    assert p.exists()
    for log in td['log']:
        assert log.get('level')!='error',log
        if log.get('level')=='warning':warnings.append(dict(module=mod,message=log['message']))
        if log.get('level')=='trace' and 'LEAN_PATH=' in log.get('message',''):
            search=log['message'].split('LEAN_PATH=',1)[1].split(' c:',1)[0]
            assert str(R/'kernel'/'.lake') not in search and str(R/'r'/'.lake') not in search
            assert 'TETELESTAI_V351' not in search
    author=R/'kernel'/'.lake'/'build'/'lib'/'lean'/p.relative_to(BUILD)
    ob=dict(module=mod,own=pin(p),trace=pin(tr),author=None,equal_to_author=None)
    if author.exists():
        ob['author']=pin(author);ob['equal_to_author']=pin(p)['sha256']==ob['author']['sha256']
    objects.append(ob)
assert not [w for w in warnings if w['module'] in FINAL|{'TGLExt.ReviewSector'}]
assert all(o['equal_to_author'] for o in objects if o['module'] in FINAL)
prior=load(Path(snap['inherited_B2_compilation']['path']))
present=[p for p in BUILD.rglob('*.olean') if p.relative_to(BUILD).parts[0] in ['TGL','TGLExt']]
assert len(present)==len(prior['objects'])+len(objects)

au_path=R/'AUDITORIA_B3.json';au=load(au_path)
for p in au['sources']+au['objects']+[au['positive_build']]:checkpin(p)
arun=load(Path(au['positive_build']['path']));assert arun['returncode']==0
for src in arun['snapshots']:
    assert pin(Path(src['path']))['sha256']==src['sha256']==pin(Path(src['snapshot']))['sha256']
assert {t['name'] for t in au['targets']}==set(targets)
assert au['axioms']==ax
author_controls=[]
for command in au['commands']:
    for k in ['source','stdout','stderr']:checkpin(command[k])
    text=Path(command['stdout']['path']).read_text(encoding='utf8')
    if command['label']=='AuditSector':assert command['returncode']==0 and axioms(text)==ax
    else:
        assert command['returncode']!=0 and 'type mismatch' in text.lower()
        assert not any(s in text.lower() for s in ['unknown module','unknown identifier','unexpected token','unexpected identifier','object file'])
    author_controls.append(dict(**command,review_scope='Author execution; source and streams re-read and pinned, not re-executed'))

fiche=load(R/'REAPROVEITAMENTO_B3.json');provider_checks=[]
for pr in fiche['providers']:
    p=Path(pr['path']);assert pin(p)['sha256']==pr['sha256'],pr
    line=p.read_text(encoding='utf-8-sig').splitlines()[pr['line']-1]
    assert pr['name'] in line,(pr['name'],line)
    provider_checks.append(dict(**pr,line_read=line,checked_sha256=pin(p)['sha256']))
times=[]
for p in [R/'REAPROVEITAMENTO_B3.md',R/'REAPROVEITAMENTO_B3.json']+[Path(x['source']['path']) for x in snap['sources'] if x['module'] in FINAL]:
    st=p.stat();times.append(dict(file=pin(p),created_local=datetime.fromtimestamp(st.st_ctime).astimezone().isoformat(),modified_local=datetime.fromtimestamp(st.st_mtime).astimezone().isoformat()))
fiche_precedes=all((R/'REAPROVEITAMENTO_B3.json').stat().st_mtime<Path(x['source']['path']).stat().st_ctime for x in snap['sources'] if x['module'] in FINAL)
assert fiche_precedes
order=R.parent/'TUNEL'/'PARA_CHATGPT'/'ORDEM_012_a_passagem_da_acao_a_metrica.md'
orderlines=order.read_text(encoding='utf-8-sig').splitlines()
orderexcerpt='\n'.join(orderlines[116:124])
assert 'H_nx' in orderexcerpt and 'B3' in orderexcerpt

semantic=dict(
    status='B3 source semantics reviewed in full; conditional theorem, no integration or empirical validation',
    order=dict(file=pin(order),lines='117-124',excerpt=orderexcerpt),
    same_beta='Every correction uses c.beta from the actual B1 TGLExt.TGLCoupling. No second parameter or numeric beta/alpha; alpha is not recalibrated.',
    sectors='SectorFluid quantifies a finite type (possibly empty), rho nonnegative on I, time-independent w_i and named HasDerivAt H_nx. H, I arbitrary here; H becomes flrwHubble a in the metric consumer.',
    rescaling='HasDerivAt.const_mul by the time-constant factor 1+c.beta*(1+w_i). No exchange law derived: H_nx is INPUT. No assertion each corrected density is nonnegative without a bound on its factor.',
    sums='weighted_continuity uses the finite HasDerivAt.fun_sum. Total and corrected conservation, rho differentiability and corrected pressure differentiability follow from this, not from a hidden conservation field.',
    closure='correctedTotalRho=totalRho+c.beta*enthalpy exactly; three_sector_closure invokes closure_identity and hubble_form with the same c.beta and leaves rhoL unchanged.',
    effective_reading='wEff=pTot/rhoTot; the absolute-value equality has explicit hr:rhoTot>0 and he:enthalpy>=0. Outside that domain the theorem makes no claim; no hidden zero-denominator division.',
    conservation='sector_covariant_conservation identifies the full divergence vector via actual B2 flrw_stress_divergence, HasDerivAt/H_nx and corrected_continuity, for the same metric and stress.',
    metric_consumer='tgl_friedmann_from_sector_closure directly invokes flrw_friedmann_from_general_metric. Its H_conservation is discharged by sector_covariant_conservation; H_null for corrected stress remains explicit.',
    other_hypotheses='U open and preconnected, smooth positive a on U, times in I, hr and he on U, G>0. No H nonzero assumption. Nonempty U not assumed: the universal conclusion is vacuous if U is empty, not an existence theorem for a physical solution.',
    cosmological_constant='The aggregate gives one existential real cosmological constant, with H²=(8piG/3)*rhoTot*(1+beta*abs(1+wEff))-Lambda/3. This is the inherited G+Lambda*g=kappa*T convention.',
    zero_corollary='tgl_friedmann_zero_cosmological has H_zero_cosmological:Lambda=0 and the full pointwise metric equation hE. It is a conditional specialization; it does not prove the integration constant vanishes.',
    newton='flrw_newton_coefficient and eta=1/(4G) instantiate the inherited normalization with G>0 INPUT, not a derivation or fit of G.',
    second_equation='Hprime=-4piG*(correctedTotalRho+correctedTotalPressure). No replacement by the total effective factor is made; the B4 comparison is outside scope.',
    nonvacuity='No inconsistent/conclusion premise found. The generic sector data allow constant vacuum-like sectors w=-1 with positive rho. With a constant positive scale factor H=0, H_nx is consistent and H_null permits a compensating Lambda; this is a semantic consistency check, not an additional Lean construction.',
    findings=[],
    limitations=['No B4 comparison or choice between routes','No global Lema 3','No TGL-S/TGL-L closure','No runtime/gate installation or new flag consumption verified','No full 941-source or um.py integrity scan; the author audit statement is retained as DECLARADO','Package caches/toolchain inherited, not independently rebuilt'])
save(A/'semantic_inspection.json',semantic)
save(A/'contract_and_fiche.json',dict(order=semantic['order'],providers=provider_checks,chronology=times,fiche_before_sources_by_filesystem_metadata=fiche_precedes,search_scope='Fiche searches read, not re-executed; no exhaustive absence claim',consumer_scope='Proposed um.py locators read in fiche only; no um.py inspection/execution'))

stamp=datetime.now().astimezone().isoformat()
compilation=dict(timestamp=stamp,status='INDEPENDENT_B3_LAKE_RC0',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,
    all_attempts_scope='This B3 snapshot/build only. Historical B2 preparation failures remain in the sealed B2 report.',
    run=pin(A/'run.json'),runs=[dict(label='B3_with_missing_B1_suppliers',run=pin(A/'run.json'),returncode=0)],
    source_snapshot=ptr['snapshot'],targets=checks,exact_target_count=22,theorems=14,definitions=7,structures=1,
    all_axioms_allowed=True,all_target_typechecks_present=True,auditor_trace=pin(tracepath),
    objects=objects,new_project_object_count=len(objects),private_project_object_count=len(present),
    newly_recompiled_B1_supplier_count=len([r for r in snap['sources'] if r['new_source_copy'] and r['module'] not in FINAL]),
    inherited_B2_compilation=snap['inherited_B2_compilation'],inherited_project_objects=snap['inherited_project_objects'],
    inherited_project_objects_unchanged=True,source_checks=comp['source_checks'],new_warnings=[],supplier_warnings=warnings,
    author_project_objects_copied=False,cache_inheritance=snap['cache_inheritance'],B1_B2_protected_unchanged=True,protected_pins=snap['protected_before'])
save(OUT/'compilation.json',compilation)
evidence=dict(timestamp=stamp,status='B3_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED',marker='B3_DEV_REVIEW',
    P0=[],P1=[],P2=[],findings=[],compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json'),
    semantic_inspection=pin(A/'semantic_inspection.json'),semantic=semantic,contract_and_fiche=pin(A/'contract_and_fiche.json'),
    source_snapshot=ptr['snapshot'],author_audit=pin(au_path),author_positive_build=au['positive_build'],author_commands=author_controls,
    author_baseline_941_preservation='DECLARADO in AUDITORIA_B3; no repeat of broad baseline/um.py scan',
    new_source_object_pins=[dict(source=next(r['source'] for r in snap['sources'] if r['module']==o['module']),**o) for o in objects if o['module'] in FINAL],
    inherited_B2_compilation=snap['inherited_B2_compilation'],B1_B2_protected_pins=snap['protected_before'],B1_B2_unchanged=True,
    scope='B3 only, 14 theorems + 7 definitions + 1 structure; 3 author files and own auditor. No B4, A1, um.py, data, Atlas, runtime or integration.')
save(OUT/'REVIEW_B3_FINAL.json',evidence)
table='\n'.join('| '+o['module'].split('.')[-1]+' | `'+next(r['source']['sha256'] for r in snap['sources'] if r['module']==o['module'])+'` | `'+o['own']['sha256']+'` |' for o in objects if o['module'] in FINAL)
targetlist='\n'.join('- `'+t+'`' for t in targets)
md=f'''# B3 — revisão independente final

{stamp} · **B3_DEV_REVIEW**

[REAL] **Aceito no escopo B3. Nenhum P0, P1 ou P2 encontrado.** Os dois módulos e o auditor autoral foram lidos integralmente e reproduzidos por Lake na raiz curta `s`, com auditor próprio de tipos, universos e axiomas. **22 alvos: 14 teoremas, 7 definições e 1 estrutura**, todos restritos a `propext`, `Classical.choice`, `Quot.sound`. Nenhum aviso novo nos módulos B3 ou auditores.

## Reprodução e proveniência

Comando próprio: `lake build TGLExt.TheSameBetaReadsThreeFaces TGLExt.SectorFluidClosure TGLExt.SectorFriedmann TGLExt.AuditSector TGLExt.ReviewSector`, rc0, Lean 4.31.0. Raiz: `{S}`. Tentativa: `{A}`. Foram acrescentadas e recompiladas **{compilation['newly_recompiled_B1_supplier_count']} fontes da cadeia B1** que faltavam em `s`, as três fontes B3 e o auditor próprio: **{len(objects)} novos objetos**. Os **{len(snap['inherited_project_objects'])} objetos próprios herdados de B2**, suas traces e fontes permaneceram idênticos; total privado medido: {len(present)} objetos. Não foram copiados objetos autorais de TGL/TGLExt.

Mathlib e oito pacotes auxiliares são o cache privado já pinado/reutilizado em B1/B2; não houve reconstrução independente desses pacotes nem da toolchain. A proveniência integral e os mapas de hashes herdados estão ligados em `compilation.json`. O ambiente remove LEAN_PATH/LEAN_SRC_PATH externos; as traces novas não incluem o build autoral ou a raiz B1. As permissões `safe.directory` são apenas nove caminhos privados exatos no ambiente desse processo, sem alteração global. Nenhuma falha nesta tentativa B3; as falhas históricas de preparação B2 continuam preservadas no relatório selado B2.

As fontes novas e seus três objetos correspondentes coincidem byte a byte com o candidato autoral. Relatórios B1/B2, compilation/run B1, manifesto B1, manifesto/recibo B2 e todos os objetos B2 protegidos foram relidos após o build e não mudaram. Só houve acréscimos em `s` e escritas em `revisao_b3`.

## Significado, hipóteses e consumidor

`SectorFluid` contém setores finitos, `rho_nonneg`, `w : ι → ℝ` constante no tempo e **`H_nx` como campo HasDerivAt nomeado**. É uma hipótese de não troca; a prova não a deriva de física microscópica. A multiplicação por `1+c.beta*(1+w_i)` conserva a mesma equação por ser constante no tempo; somas e pressão diferenciável são construídas efetivamente. Não se afirma positividade de cada densidade corrigida para w arbitrário: isso exigiria controlar o respectivo fator. Este limite já consta da ficha.

`corrected_closure` prova a identidade aditiva, e `three_sector_closure` invoca os fornecedores `closure_identity`/`hubble_form`, com o mesmo `c.beta` da estrutura B1. `wEff` é definido como pressão total/densidade total. A leitura `rhoTot*|1+wEff|=enthalpy` usa exatamente **rhoTot>0 e enthalpy≥0**; não há promessa para denominador zero ou entalpia negativa. A identidade aditiva não precisa dessas restrições.

O consumidor `tgl_friedmann_from_sector_closure` **chama o teorema B2 `flrw_friedmann_from_general_metric`** para a métrica e o stress corrigido concretos. A hipótese de conservação desse fornecedor é descarregada por `sector_covariant_conservation`, que usa a divergência tensorial B2 e a continuidade demonstrada a partir de H_nx. **H_null continua INPUT explícito sobre o stress corrigido**, assim como U aberto/preconexo, escala a suave/positiva, tempos em I e G>0. Não há campo que pressuponha a conclusão escalar pretendida. U pode ser vazio: não se declara existência de uma solução física em domínio não vazio.

O resultado geral mantém uma única constante existencial Λ e a convenção herdada `G+Λg=κT`:

`H²=(8πG/3)·rhoTot·(1+beta·|1+wEff|)−Λ/3`;
`H′=−4πG·(correctedTotalRho+correctedTotalPressure)`.

O corolário sem Λ exige **`H_zero_cosmological : cosmological=0`** e a equação métrica tensorial hE explicitamente. É uma especialização condicional, não uma prova de Λ=0. A calibração eta=1/(4G) reutiliza `flrw_newton_coefficient`, mantendo G>0 como INPUT. Não se divide por H nem se exclui H=0. A comparação da segunda equação com a rota de fator sobre o total pertence a B4, não a este aceite.

[DERIVED — inspeção semântica] Não foi encontrada premissa contraditória ou conclusão disfarçada. Como checagem de consistência, setores constantes com w=-1, rho>0 e a constante têm H_nx compatível e o balanço nulo admite a constante Λ correspondente; nenhum novo teorema de existência foi compilado nessa revisão.

## Ficha e controles

Cláusula B3 da ORDEM 012, linhas 117–123, confrontada com os enunciados. A ficha coincide com as hipóteses e consumidores efetivos: {len(provider_checks)} locadores de fornecedores conferidos por hash e linha. Metadados locais medidos colocam a ficha antes das três fontes; são evidência de cronologia do filesystem, não selo externo de tempo. Buscas autorais e limites foram lidos, sem refazê-los ou alegar exaustividade. Os consumidores Python são apenas propostas citadas na ficha: não houve leitura/execução de um.py nem revisão de sua instalação.

`AUDITORIA_B3.json` e seus streams foram relidos e pinados. `BadSectorClosure` troca +beta por −beta; `BadSectorAbs` troca entalpia por seu negativo. Ambos terminam rc1 por **Type mismatch**, com imports reconhecidos, sem erro de sintaxe/ambiente. São controles **executados pelo autor**, não novas execuções minhas. As 22 saídas autorais coincidem com o auditor próprio. A preservação autoral de 941 fontes/um foi relida como [DECLARADO]; não se reabriu esse inventário. Foram preservados {len(warnings)} avisos dos fornecedores B1 recompilados, detalhados no JSON; nenhum é aviso B3.

## Pins e evidência

| Arquivo | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---|---|
{table}

- [Revisão JSON](<{(OUT/'REVIEW_B3_FINAL.json').as_posix()}>) — SHA256 `{pin(OUT/'REVIEW_B3_FINAL.json')['sha256']}`.
- [Compilação independente](<{(OUT/'compilation.json').as_posix()}>) — SHA256 `{pin(OUT/'compilation.json')['sha256']}`.
- [Run rc0](<{(A/'run.json').as_posix()}>) — SHA256 `{pin(A/'run.json')['sha256']}`.
- [Snapshot e dependências](<{(A/'snapshot.json').as_posix()}>) — SHA256 `{pin(A/'snapshot.json')['sha256']}`.
- [Inspeção semântica](<{(A/'semantic_inspection.json').as_posix()}>) e [ficha/contrato](<{(A/'contract_and_fiche.json').as_posix()}>).

## Alvos auditados

{targetlist}

**Escopo encerrado:** DEV B3, com a ligação condicional B1→conservação setorial→B2. Sem pendência de análise/recompilação deste delta. Não é aceite de integração, alteração de gate, B4–B6, TGL-S/TGL-L, fecho global ou confirmação empírica. Fontes autorais, B1/B2 selados, memórias e dados não foram alterados.
'''
save(OUT/'REVIEW_B3_FINAL.md',md,True)
print(json.dumps(dict(status=evidence['status'],P0=[],P1=[],P2=[],report=pin(OUT/'REVIEW_B3_FINAL.md'),json=pin(OUT/'REVIEW_B3_FINAL.json'),compilation=pin(OUT/'compilation.json'),new_objects=len(objects),inherited_objects=len(snap['inherited_project_objects']),warnings=len(warnings)),ensure_ascii=False,indent=2))
