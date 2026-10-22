from pathlib import Path
from datetime import datetime
import hashlib,json,os,re

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=R/'revisao_b2';S=R/'s';STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def checkpin(p):
    assert pin(Path(p['path']))==p,p
def save(p,b):
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+STAMP)
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+STAMP)
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    os.replace(tmp,p)
def jsave(p,d):save(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def norm(s):return re.sub(r'\.\{[^}]*\}', '', s).strip()
def axioms(text):
    result={}
    for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))",text,re.S):
        name=norm(m.group(1));a=[] if m.group(3) else [norm(x) for x in m.group(2).split(',') if x.strip()]
        if name in result:assert result[name]==a,(name,result[name],a)
        result[name]=a
    return result

state=load(OUT/'state.json')
assert state['status']=='BUILDS_RC0__FINAL_AUDIT_PENDING',state
A=Path(state['attempt']);comp=load(A/'completion.json')
checkpin(comp['source_snapshot']);snap=load(Path(comp['source_snapshot']['path']))
targets=snap['targets'];assert len(targets)==32
for src in snap['sources']:checkpin(src['source']);checkpin(src['copy'])
for run in comp['runs']:
    checkpin(run['run']);rr=load(Path(run['run']['path']));assert rr['returncode']==0
    for stream in rr['streams']:checkpin(stream)
assert comp['protected_unchanged']
env=load(A/'environment_scope.json')
for p in env['protected_before']:checkpin(p)

build=S/'.lake'/'build'/'lib'/'lean'
trace_path=build/'TGLExt'/'ReviewFLRW.trace';trace=load(trace_path)
messages=[x['message'] for x in trace['log'] if x.get('level')=='info']
own_axioms={};typechecks={}
for message in messages:
    if 'depends on axioms:' in message or 'does not depend on any axioms' in message:
        own_axioms.update(axioms(message))
    else:
        text=re.sub(r'^.*?\.lean:\d+:\d+:\s*','',message,count=1)
        for target in targets:
            if re.match(re.escape(target)+r'(?:\.\{[^}]*\})?(?:\s|$)',text):
                assert target not in typechecks,target
                typechecks[target]=text
assert set(own_axioms)==set(targets),(set(targets)-set(own_axioms),set(own_axioms)-set(targets))
assert set(typechecks)==set(targets),(set(targets)-set(typechecks))
allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(ax)<=allowed for ax in own_axioms.values())
checks={t:dict(axioms=own_axioms[t],typecheck=typechecks[t]) for t in targets}

objects=[];warnings=[];new_warnings=[]
newmods={'FLRWGeometry','FLRWFieldEquations','AuditFLRW','ReviewFLRW'}
for obj in comp['project_objects']:
    checkpin(obj);p=Path(obj['path']);tr=p.with_suffix('.trace');td=load(tr)
    for log in td['log']:
        msg=log.get('message','')
        if log.get('level')=='trace' and 'LEAN_PATH=' in msg:
            paths=msg.split('LEAN_PATH=',1)[1].split(' c:',1)[0]
            assert str(R/'kernel'/'.lake') not in paths
            assert str(R/'r'/'.lake') not in paths
            assert 'TETELESTAI_V351' not in paths
        if log.get('level') in ['warning','error']:
            row=dict(module=p.stem,level=log['level'],message=msg)
            warnings.append(row)
            if p.stem in newmods:new_warnings.append(row)
    rel=p.relative_to(build);author=R/'kernel'/'.lake'/'build'/'lib'/'lean'/rel
    data=dict(own=obj,trace=pin(tr),author=None,equal_to_author=None)
    if author.exists():
        data['author']=pin(author);data['equal_to_author']=data['author']['sha256']==obj['sha256']
    objects.append(data)
assert not new_warnings,new_warnings
assert all(o['equal_to_author'] for o in objects if Path(o['own']['path']).stem in newmods-{'ReviewFLRW'})

author_path=R/'AUDITORIA_B2.json';author=load(author_path)
checkpin(author['positive_build']);author_run=load(Path(author['positive_build']['path']))
assert author_run['returncode']==0
for c in author_run['snapshots']:
    assert pin(Path(c['path']))['sha256']==c['sha256']==pin(Path(c['snapshot']))['sha256']
for p in author['sources']+author['objects']:checkpin(p)
assert {t['name'] for t in author['targets']}==set(targets)
assert {k:sorted(v) for k,v in author['axioms'].items()}=={k:sorted(v) for k,v in own_axioms.items()}
author_commands=[]
for c in author['commands']:
    for key in ['source','stdout','stderr']:checkpin(c[key])
    text=Path(c['stdout']['path']).read_text(encoding='utf8')
    if c['label']=='AuditFLRW':
        assert c['returncode']==0
        assert axioms(text)==author['axioms']
    else:
        assert c['returncode']!=0 and 'type mismatch' in text.lower()
        assert not any(s in text.lower() for s in ['unknown module','unknown identifier','object file','unexpected token','unexpected identifier'])
    author_commands.append(dict(**c,review_scope='Author execution, source and raw streams re-read independently; not re-executed'))
historical_author=[]
for d in sorted((R/'audit_B2').iterdir()):
    if d.is_dir() and str(d)!=str(Path(author['commands'][0]['stdout']['path']).parent):
        for p in sorted(d.iterdir()):
            if p.is_file():historical_author.append(pin(p))

prep=OUT/'suppliers_20260914_161954_798949';ps=load(prep/'snapshot.json')
package_pins=[]
for pkg in ps['packages']:
    checkpin(pkg['pins']);rows=load(Path(pkg['pins']['path']))
    assert len(rows)==pkg['files']
    package_pins.append(pkg)
failed_run=load(prep/'run.json');assert failed_run['returncode']!=0
for p in failed_run['streams']:checkpin(p)
own_history=dict(preparation_encoding_failure=pin(OUT/'suppliers_20260914_153804_396136'/'preparation_failure.json') if (OUT/'suppliers_20260914_153804_396136'/'preparation_failure.json').exists() else [pin(p) for p in OUT.glob('suppliers_*/preparation_failure.json')],interrupted_preparation_snapshot=pin(OUT/'suppliers_20260914_153824_720287'/'source_snapshot.json'),git_ownership_refusal=pin(prep/'run.json'),resolution='Nine exact private safe.directory values provided in process environment; no global Git configuration changed.')
sem_path=Path(snap['attempt'])/'semantic_inspection.json';semantic=load(sem_path)
contract_path=OUT/'REVIEW_B2_PREPARACAO.json';contract=load(contract_path)
for p in contract['fiche']:checkpin(p)
for p in contract['providers']:
    assert pin(Path(p['path']))['sha256']==p['sha256']

compilation=dict(timestamp=datetime.now().astimezone().isoformat(),status='INDEPENDENT_B2_LAKE_RC0',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,runs=comp['runs'],source_snapshot=comp['source_snapshot'],targets=checks,exact_target_count=32,theorems=26,definitions=6,all_axioms_allowed=True,auditor_trace=pin(trace_path),objects=objects,new_warnings=new_warnings,inherited_warnings=warnings,cache_inheritance=package_pins,author_project_objects_copied=False,source_checks=comp['source_checks'],B1_protected_unchanged=True,history=own_history)
jsave(OUT/'compilation.json',compilation)
evidence=dict(timestamp=compilation['timestamp'],status='B2_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED',marker='B2_DEV_REVIEW',P0=[],P1=[],P2=[],findings=[],compilation=pin(OUT/'compilation.json'),semantic_inspection=pin(sem_path),semantic=semantic,contract_inspection=pin(contract_path),source_snapshot=comp['source_snapshot'],author_audit=pin(author_path),author_commands=author_commands,author_failed_syntax_attempts_excluded=historical_author,author_baseline_941_claim='Author audit states 941 base sources and um.py unchanged; no independent re-audit of those 941 files or um.py in this restricted turn.',new_source_object_pins=[o for o in objects if Path(o['own']['path']).stem in newmods],scope='B2 only: flat FLRW geometry and conditional Friedmann/conservation in original chart; no physical calibration derived; no B3-B6, A1, um.py, data, Atlas or integration.',B1_protected_pins=env['protected_before'],B1_unchanged=True)
jsave(OUT/'REVIEW_B2_FINAL.json',evidence)

newsource=[x for x in snap['sources'] if x['module'] in ['TGLExt.FLRWGeometry','TGLExt.FLRWFieldEquations','TGLExt.AuditFLRW']]
table='\n'.join('| '+x['module'].split('.')[-1]+' | `'+x['source']['sha256']+'` | `'+next(o['own']['sha256'] for o in objects if Path(o['own']['path']).stem==x['module'].split('.')[-1])+'` |' for x in newsource)
targetlist='\n'.join('- `'+t+'`' for t in targets)
warningtext='\n'.join('- '+w['message'].replace('\n',' ') for w in warnings) or 'Nenhum aviso.'
md=f'''# B2 — revisão independente final

{compilation['timestamp']} · **B2_DEV_REVIEW**

[REAL] **Aceito no escopo B2. P0: nenhum; P1: nenhum; P2: nenhum.** Fontes integrais, ficha e cláusula B2 da ORDEM 012 lidas. Reprodução própria por Lake, seguida de auditor próprio com `#check`, universos e `#print axioms`: **32 declarações = 26 teoremas + 6 definições**, todas limitadas a `propext`, `Classical.choice`, `Quot.sound`. Nenhum aviso novo. Não há aceite de integração, B3–B6, nova calibração física ou alteração de gate.

## Reprodução e proveniência

Raiz própria curta: `{S}`. Primeiro `lake build TGLExt.GeneralMetricEinstein`; depois `lake build TGLExt.FLRWGeometry TGLExt.FLRWFieldEquations TGLExt.AuditFLRW TGLExt.ReviewFLRW`. Os dois comandos finais terminaram rc0. Mesma Lean 4.31.0, com binários/toolchain pinados nos runs. `{len(comp['project_objects'])}` objetos TGL/TGLExt produzidos nesta raiz, incluindo o auditor próprio; nenhum objeto de projeto autoral ou de B1 foi copiado. As 88 fontes transitivas iniciais e as três fontes B2 foram copiadas em bytes e conferidas; o auditor próprio é a quarta fonte do delta.

Mathlib e oito pacotes auxiliares vieram do cache privado de B1 em `R/r/.lake/packages`, copiados com leitura/verificação dos hashes de cada arquivo e revisão Git igual ao manifesto. Este cache é **herdado**, não recompilação independente de Mathlib/toolchain. LEAN_PATH/LEAN_SRC_PATH externos removidos; as traces mostram somente bibliotecas da raiz privada e pacotes privados. Os objetos dos dois módulos novos e AuditFLRW são byte a byte iguais aos autorais. B1/R/r, seus relatórios, compilation/run e manifesto permanecem intocados e os pins protegidos foram relidos.

Falhas próprias preservadas: erro de encoding do preparador (`utf8-sig`, corrigido para `utf-8-sig` em arquivo novo); preparação interrompida antes de Lake, retomada verificando as cópias; recusa Git por propriedade de diretório do cache criado sob conta sandbox. Esta última foi resolvida por nove `safe.directory` exatos apenas no ambiente do processo, sem configuração global. Nenhuma dessas falhas é refutação matemática. Por isso `all_accepted_builds_exit_zero=true` e `all_attempts_exit_zero=false`.

## Hipóteses e consumidor real

`flrwMetric` é diag(1,-a²,-a²,-a²), na assinatura (+---). `flrw_metric_inverse` identifica a inversa diagonal com `metricInverse`; `flrw_connection` calcula a Levi-Civita dessa mesma métrica. `flrw_ricci` transporta a igualdade local da conexão aos jets em U aberto antes de avaliar a curvatura. As hipóteses hG/hJ do auxiliar algébrico são descarregadas. Nenhuma componente Ricci/Einstein foi pressuposta como campo.

`flrw_einstein_tensor` fornece a matriz inteira, incluindo componentes fora da diagonal nulas; as leituras 00/espaciais e a identidade de Ricci nulo usam esse mesmo objeto. `flrw_stress_divergence` calcula os quatro componentes de divergência do fluido; a continuidade é condicional à componente temporal nula. Há diferenciabilidade local de rho e pressão e suavidade local de a, não hipóteses globais fora de U.

As leituras `flrw_friedmann_first`, `flrw_acceleration` e `flrw_friedmann_second` têm hE tensorial explícita. Isso não é circularidade na entrega: `flrw_friedmann_from_general_metric` **obtém** hE de `metric_only_einstein_equation`, fornecendo Lorentz/suavidade/regularidade/simetria concretas e preservando **H_null e H_conservation como hipóteses nomeadas**. Abertura e preconexidade de U são explícitas; Lambda é uma única constante existencial em U. Não se afirma conservação, balanço nulo ou realização física incondicionais.

O sinal segue `G+Lambda*g=coupling*T`: `H²=coupling*rho/3-Lambda/3`, `a''/a=-coupling*(rho+3p)/6-Lambda/3` e `H'=-coupling*(rho+p)/2`. Não há divisão por H, portanto H=0 não é excluído. Nenhuma identificação automática com uma Lambda física de outra convenção. Eta é real arbitrário no teorema algébrico, com a divisão total de Lean; a leitura de Newton usa G>0 e eta=1/(4G) como INPUT. `flrw_newton_coefficient` consome `einstein_coefficient_from_clausius`, sem derivar essa calibração nem fixar beta.

Ficha: 24 locadores em 11 arquivos conferidos por hash/linha. A proposta coincide com a maquinaria solicitada; Ansätze antigos não foram renomeados como FLRW. As quatro entradas `ext_flrw_*` são consumidores propostos, não instalação revisada. Não houve leitura/execução de um.py, dados ou Atlas nesta rodada; a afirmação autoral de preservação de 941 fontes/um foi somente relida em AUDITORIA_B2.

## Evidência autora e controles negativos

Run final autoral `{author['positive_build']['path']}` rc0 e snapshots iguais aos três pins próprios. AUDITORIA_B2, seu auditor de 32 alvos e streams das duas sondas foram relidos e pinados; nenhum desses scripts foi executado por esta revisão. A rodada válida rejeita por **Type mismatch** a troca 3→4 em G00 e a troca do sinal de Lambda, com imports funcionais. A rodada anterior FAILED_SYNTAX, com erro lexical em `a(y0)`, é preservada e **excluída** como controle matemático. Não foram ampliados controles.

## Pins do candidato congelado

| Arquivo | SHA256 fonte | SHA256 objeto próprio = autor |
|---|---|---|
{table}

## Avisos herdados

{warningtext}

## Alvos conferidos

{targetlist}

Os enunciados completos impressos pelo auditor, axiomas por alvo, fontes/objetos, traces, runs, pacotes e histórico estão em [compilation.json](<{OUT/'compilation.json'}>) SHA256 `{pin(OUT/'compilation.json')['sha256']}`. Evidência desta revisão: [REVIEW_B2_FINAL.json](<{OUT/'REVIEW_B2_FINAL.json'}>) SHA256 `{pin(OUT/'REVIEW_B2_FINAL.json')['sha256']}`. Fontes e relatórios B1 preservados; nenhuma pendência de revisão B2 dentro deste escopo.
'''
save(OUT/'REVIEW_B2_FINAL.md',md.encode('utf8'))
print(json.dumps(dict(report=pin(OUT/'REVIEW_B2_FINAL.md'),evidence=pin(OUT/'REVIEW_B2_FINAL.json'),compilation=pin(OUT/'compilation.json'),targets=len(targets),objects=len(objects),new_warnings=new_warnings,all_new_objects_equal=True),ensure_ascii=False,indent=2))
