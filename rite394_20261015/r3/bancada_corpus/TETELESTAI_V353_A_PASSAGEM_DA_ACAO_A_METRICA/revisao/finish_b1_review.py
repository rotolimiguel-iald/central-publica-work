from pathlib import Path
from datetime import datetime
import hashlib, json, re, os

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
REVIEW=ROOT/'revisao'
OWN=ROOT/'r'

def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def write(p,b):
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();back=p.with_name(p.name+'.bak_'+stamp);back.write_bytes(old);assert back.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p);assert p.read_bytes()==b

def writej(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))

run=json.loads((OWN/'run.json').read_bytes())
snapshot=json.loads((OWN/'snapshot.json').read_bytes())
remap=json.loads((REVIEW/'B1_BUILD_ROOT_REMAP.json').read_bytes())
def remapped(x):
    if isinstance(x,str):return x.replace(remap['source'],remap['destination'])
    if isinstance(x,list):return [remapped(v) for v in x]
    if isinstance(x,dict):return {k:remapped(v) for k,v in x.items()}
    return x
snapshot=remapped(snapshot)
writej(OWN/'snapshot_remapped.json',snapshot)
assert run['returncode']==0,run
streams='\n'.join(Path(p['path']).read_text(encoding='utf8',errors='strict') for p in run['streams'])
streams=re.sub(r'\x1b\[[0-9;]*[a-zA-Z]','',streams)
targets=snapshot['own_auditor']['targets']
axioms={}
pattern=r"'([^\r\n]+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
for match in re.finditer(pattern,streams):
    name,body=match.groups()
    name=re.sub(r'\.\{[^}]*\}','',name)
    if name not in targets:continue
    atoms=[] if body is None else [re.sub(r'\.\{[^}]*\}','',a.strip()) for a in body.split(',') if a.strip()]
    if name in axioms:assert set(axioms[name])==set(atoms),(name,axioms[name],atoms)
    axioms[name]=atoms
assert set(axioms)==set(targets),(set(targets)-set(axioms))
assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in axioms.values()),axioms
assert 'sorryAx' not in str(axioms)

copies=[]
for row in snapshot['sources']+snapshot['documents']:
    p=Path(row['source']);copy=Path(row['copy'])
    assert pin(p)['sha256']==row['sha256'],p
    assert pin(copy)['sha256']==row['sha256'],copy
    copies.append({'path':str(p),'unchanged':True})

ficha=json.loads((ROOT/'REAPROVEITAMENTO_B1.json').read_bytes())
providers=[]
for row in ficha['providers']:
    p=Path(row['path']);b=p.read_bytes();lines=b.decode('utf8').splitlines()
    ok=hashlib.sha256(b).hexdigest()==row['sha256'] and row['name'].split('.')[-1] in lines[row['line']-1]
    assert ok,row
    providers.append({'name':row['name'],'path':str(p),'line':row['line'],'sha256':row['sha256'],'verified':ok})
consumers=[]
for row in ficha['consumers']:
    p=Path(row['path']);b=p.read_bytes();lines=b.decode('utf8').splitlines()
    ok=hashlib.sha256(b).hexdigest()==row['sha256'] and row['text'] in lines[row['line']-1]
    assert ok,row
    consumers.append({'path':str(p),'line':row['line'],'sha256':row['sha256'],'verified':ok})

source=ROOT/'kernel'/'TGLExt'/'TheSameBetaReadsThreeFaces.lean'
code=source.read_text(encoding='utf8')
# Nested block-comment removal, preserving line numbers; candidate has no strings.
i=depth=0;clean=[]
while i<len(code):
    if code.startswith('/-',i):depth+=1;i+=2;continue
    if depth and code.startswith('-/',i):depth-=1;i+=2;continue
    if not depth and code.startswith('--',i):
        j=code.find('\n',i);i=len(code) if j<0 else j;continue
    if not depth or code[i]=='\n':clean.append(code[i])
    i+=1
assert depth==0
clean=''.join(clean)
forbidden=re.findall(r'\b(?:sorry|axiom|native_decide|trustCompiler|admit|unsafe)\b',clean)
assert not forbidden,forbidden
types_checked={name:bool(re.search(re.escape(name)+r'(?:\.\{[^}]*\})?\s*(?:\(|:)',streams)) for name in targets}
assert all(types_checked.values()),types_checked

objects=[]
for module in ['TGLExt.TheSameBetaReadsThreeFaces','TGLExt.AuditSameBeta','TGLExt.ReviewSameBeta']:
    rel=Path(*module.split('.')).with_suffix('.olean');op=OWN/'.lake'/'build'/'lib'/'lean'/rel
    obj=pin(op);obj['module']=module
    ap=ROOT/'kernel'/'.lake'/'build'/'lib'/'lean'/rel
    obj['author_object']=pin(ap) if ap.exists() and module!='TGLExt.ReviewSameBeta' else None
    obj['author_object_equal']=obj['sha256']==obj['author_object']['sha256'] if obj['author_object'] else None
    objects.append(obj)
project_objects=list((OWN/'.lake'/'build'/'lib'/'lean').rglob('*.olean'))
fresh_project=[pin(p) for p in project_objects]
author_attempt=ROOT/'attempts'/'20260914_145521_664130'
author_run=pin(author_attempt/'run.json') if (author_attempt/'run.json').exists() else None
author_audit=json.loads((ROOT/'AUDITORIA_B1.json').read_bytes())
assert author_audit['source']['sha256']==pin(source)['sha256']
negative_records=[]
for c in author_audit['commands']:
    if c['label'] in ['BadReflection','BadCost']:
        assert c['returncode']==1
        stream=Path(c['stdout']).read_text(encoding='utf8')
        assert 'Type mismatch' in stream
        negative_records.append({'label':c['label'],'returncode':1,'source':pin(ROOT/'probes'/(c['label']+'.lean')),'stdout':pin(Path(c['stdout'])),'stderr':pin(Path(c['stderr'])),'scope':'author-run control, inspected only'})
assert len(negative_records)==2
times=[]
for p in [ROOT/'REAPROVEITAMENTO_B1.md',ROOT/'REAPROVEITAMENTO_B1.json',source,ROOT/'kernel'/'TGLExt'/'AuditSameBeta.lean']:
    times.append({'path':str(p),'mtime_ns':p.stat().st_mtime_ns,'birthtime_ns':p.stat().st_birthtime_ns})
assert max(x['mtime_ns'] for x in times[:2])<min(x['birthtime_ns'] for x in times[2:])
comp={'status':'INDEPENDENT_LAKE_RC0','run':pin(OWN/'run.json'),'original_snapshot':pin(OWN/'snapshot.json'),'snapshot':pin(OWN/'snapshot_remapped.json'),'remap':pin(REVIEW/'B1_BUILD_ROOT_REMAP.json'),'targets':targets,'axioms':axioms,'types_checked':types_checked,'all_accepted_builds_exit_zero':True,'all_attempts_exit_zero':False,'exact_targets':True,'axioms_allowed_only':True,'author_project_objects_copied':False,'new_objects':objects,'fresh_project_objects':fresh_project,'package_cache_reused':snapshot['packages'],'scope':'B1 via Lake; full author-supplied package cache copied, no author project objects','build_not_runtime':True,'failed_preparation_attempts':[pin(OWN/'attempt_01_path_length'/'run.json'),pin(OWN/'attempt_02_short_path'/'run.json')]}
writej(OWN/'compilation.json',comp)

rows='\n'.join('| `'+name+'` | '+(', '.join(axioms[name]) or 'nenhum')+' |' for name in targets)
object_rows='\n'.join('| `'+x['module']+'` | `'+x['sha256']+'` | '+('sim' if x['author_object_equal'] else 'não comparável' if x['author_object_equal'] is None else 'diverge')+' |' for x in objects)
stamp=datetime.now().astimezone().isoformat()
md=f'''# Revisão independente B1 — o mesmo β nas três faces

[REAL — leitura e reprodução própria por Lake] {stamp}

**B1_DEV_REVIEW — sem P0, P1 ou P2 constatado no escopo.** O candidato cumpre o B1 da ORDEM_012 como composição formal das leituras do mesmo β. O aceite é do módulo, de seu auditor e da ficha; não é incorporação ao monólito, mudança de gate ou prova da equação métrica.

## Resultado e hipóteses

Li integralmente `TheSameBetaReadsThreeFaces.lean` e `TGLExt/AuditSameBeta.lean`, a ficha MD/JSON e os fornecedores pertinentes. O primeiro tem 10 alvos auditados: uma estrutura, uma definição e oito teoremas. A estrutura contém apenas β real e `0<β<1` (linhas 22–25). Nenhuma das conclusões de reflexão, fundo ou vazamento é campo assumido. Não há atribuição de numeral a β ou α; 0/1 são limites, 1/2 o expoente do custo, e 4/3 é o coeficiente setorial herdado.

* **α é forma, não valor** (32–49): α=β/exp(1/2). Positividade e α<1 são provadas; o fator radical vem de `boundary_extracts_the_radical`. Isso não deduz CODATA. A possibilidade matemática de β no intervalo aberto assegura que a estrutura não é contraditória; a identidade de custo é a normalização expressamente autorizada em B1.
* **Reflexão efetiva** (52–69): usa a componente 1 de `Smat(thetaMiguel β)·e1`, especializa a prova existente e reduz `(sqrt β)^2` a β. A probabilidade é β, a amplitude é √β. `reflection_cost` liga ao mesmo α; `reflection_rejects_bare_alpha` prova que retirar o custo muda o valor.
* **Síntese** (76–93): todas as cláusulas usam `c.beta`. `closure_identity` e `hubble_form` são aplicadas literalmente, sem nova hipótese sobre densidades. Continuam identidades de anel, sem H, métrica ou conservação dinâmica.
* **Taxa** (85–93): perda estrita recebe t>0 e g>0. A última cláusula compara `exp(−tb)` a `exp(−tβ)` para todos os tempos; essa é a hipótese de identificabilidade do fornecedor. Não afirma unicidade de β apenas por 0<β<1 nem confunde taxa com produto βg de gap desconhecido.

## Ficha e consumidor

Conferi os 13 fornecedores e os seis locadores de consumidores por hash e linha. Os timestamps lidos corroboram ficha MD/JSON anterior aos dois fontes; isso é evidência de ordem de criação local, não prova de toda a história autoral. O tipo da síntese coincide com a ficha, inclusive a distinção entre proposições de igualdade e nomes de provas usados como abreviação no texto.

`ext_same_beta_reads_three_faces_kernel_proved → TGLExt.the_same_beta_reads_three_faces` está identificado como **consumidor proposto**, não já instalado. O consumidor posterior `prove_d1_camb_protocol.hypothesis.background` depende de B2–B5; B1 não paga Friedmann. A ficha registra explicitamente a contagem local 941 versus 942 declarada na ordem, sem equipará-las. Não ampliei esta revisão para inventário ou execução integral.

## Reprodução própria e limites da proveniência

Raiz: `{OWN}`. Executei `lake build TGLExt.TheSameBetaReadsThreeFaces TGLExt.AuditSameBeta TGLExt.ReviewSameBeta` com Lean 4.31.0 e `LEAN_PATH`/`LEAN_SRC_PATH` retirados do ambiente. **rc0 próprio**. O módulo novo e ambos os auditores foram recompilados nesta raiz; o auditor próprio contém `#check` e `#print axioms` dos dez alvos, com universos impressos.

Copiei fontes e configuração Lake em bytes. **Nenhum objeto TGL/TGLExt do autor foi copiado**: os {len(fresh_project)} objetos de projeto presentes ao final foram produzidos pelo build próprio, seguindo os imports. Reutilizei por cópia independente o cache de Mathlib e oito outros pacotes da árvore autoral `.lake/packages`, com revisão Git confrontada ao manifesto e hashes de todos os arquivos copiados. Este cache não foi reconstruído independentemente: esse é o limite herdado. Não há links graváveis de volta à árvore do autor. A toolchain também é a instalação existente, pinada no `run.json`.

Não executei `um.py`, integrador, testes autorais nem recorder. Minha primeira leitura procurou o auditor na raiz do kernel e recebeu arquivo ausente; localizei-o em `TGLExt/AuditSameBeta.lean`. Foi correção do meu localizador, sem atribuir falha à fonte. A cópia serial inicial do cache foi interrompida deliberadamente antes de qualquer Lean próprio, por lentidão, e retomada em paralelo sobre os arquivos preservados, verificando seus bytes. Os dois preparadores e o estado inicial permanecem na revisão. Nenhum processo autoral foi interrompido.

Duas tentativas Lake próprias anteriores deram rc1 de preparação por MAX_PATH: o arquivo `IntegralRepresentation.olean.server.hash`, em caminho de 260 caracteres, existia e foi lido pelo prefixo longo Windows. O alias 8.3 voltou a ser expandido por Lake e não resolveu. Com autorização expressa do usuário, movi a árvore privada inteira de `revisao/b1_20260914_145853` para `ROOT/r`, após verificar ambos os destinos absolutos dentro de V353; o caminho problemático caiu para 235 caracteres. Registros e streams rc1 foram preservados byte a byte em `attempt_01_path_length` e `attempt_02_short_path`. `B1_BUILD_ROOT_REMAP.json` registra o remapeamento; o snapshot original não foi reescrito. Essas tentativas não são recusa matemática do B1.

| Alvo | Axiomas medidos no auditor próprio |
|---|---|
{rows}

Li separadamente `AUDITORIA_B1.json`, os dois fontes de controle e seus streams. `BadReflection` e `BadCost` foram executados pelo autor e retornaram rc1 por **Type mismatch**: β não foi aceito como α, e β=α·exp(1/2) não foi aceito como β=α. São controles autorais inspecionados, não novas execuções minhas. A desigualdade correspondente também está no teorema positivo `reflection_rejects_bare_alpha`, auditado por mim.

## Pins e evidências

Fonte nova: `{pin(source)['sha256']}`. Auditor autoral: `{pin(ROOT/'kernel'/'TGLExt'/'AuditSameBeta.lean')['sha256']}`. Ficha MD: `{pin(ROOT/'REAPROVEITAMENTO_B1.md')['sha256']}`; JSON: `{pin(ROOT/'REAPROVEITAMENTO_B1.json')['sha256']}`.

| Objeto próprio | SHA-256 | Igual ao objeto autoral disponível |
|---|---|---|
{object_rows}

Evidência central: `{OWN/'compilation.json'}` — SHA-256 `{pin(OWN/'compilation.json')['sha256']}`. Logs brutos, configuração, cópias, manifestos de cache e timestamps estão na mesma raiz. Tipos completos estão nos streams; os dez relatórios de axiomas não contêm `sorryAx` nem axiomas fora de propext/Classical.choice/Quot.sound. A varredura do código novo, excluindo comentários, não encontrou `sorry`, `axiom`, `native_decide`, `trustCompiler`, `admit` ou `unsafe`.

Fontes, ficha e fornecedores foram relidos ao término e permanecem iguais aos snapshots. A1 ficou suspenso; escritas apenas em `V353/revisao` e na raiz privada `V353/r`, esta autorizada posteriormente para contornar MAX_PATH. A conclusão não presume integração nem os alvos B2–B6, e não reclama condições matemáticas adicionais de outras rotas.
'''
report=REVIEW/'REVIEW_B1_FINAL.md'
write(report,md.encode('utf8'))
e={'timestamp':stamp,'status':'B1_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED','P0':[],'P1':[],'P2':[],'findings':[],'scope':'B1 module+author auditor+own types/axioms+reuse ficha','compilation':pin(OWN/'compilation.json'),'report':pin(report),'source':pin(source),'author_auditor':pin(ROOT/'kernel'/'TGLExt'/'AuditSameBeta.lean'),'ficha':[pin(ROOT/'REAPROVEITAMENTO_B1.md'),pin(ROOT/'REAPROVEITAMENTO_B1.json')],'providers':providers,'consumer_locators':consumers,'proposed_consumer':ficha['proposed_consumer'],'timestamps':times,'before_code_timestamp_check':True,'source_snapshot_checks':copies,'forbidden_tokens':forbidden,'alpha_is_form_not_value':True,'no_numeric_assignment_to_beta_or_alpha':True,'author_attempt_metadata_read':author_run,'axioms':axioms,'own_objects':objects,'inherited_limit':'Mathlib and package cache copied and hashed, not independently rebuilt; no author TGL/TGLExt objects used.','not_done':['runtime','integration','B2-B6','A1','gate mutation','additional empirical/physical validation']}
e['author_negative_controls_inspected']=negative_records
e['author_audit_pin']=pin(ROOT/'AUDITORIA_B1.json')
e['warnings_from_accepted_stream']=re.findall(r'^warning:.*$',streams,re.M)
e['warnings_in_new_modules']=[w for w in e['warnings_from_accepted_stream'] if any(n in w for n in ['TheSameBetaReadsThreeFaces.lean','AuditSameBeta.lean','ReviewSameBeta.lean'])]
writej(REVIEW/'REVIEW_B1_FINAL.json',e)
print(json.dumps({'report':pin(report),'evidence':pin(REVIEW/'REVIEW_B1_FINAL.json'),'compilation':pin(OWN/'compilation.json'),'P0':[],'P1':[],'P2':[]},ensure_ascii=False))
