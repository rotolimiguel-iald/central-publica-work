from pathlib import Path
from datetime import datetime
from collections import Counter
import hashlib, json, re, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
OUT = ROOT/'revisao'
AREA = OUT/'resolvent_phase39_independent_20260914_101512_721055'
NOW = datetime.now().astimezone()
TAG = NOW.strftime('%Y%m%d_%H%M%S_%f')
TRIO = {'propext','Classical.choice','Quot.sound'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p,b):
    assert p.is_relative_to(OUT)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name+'.bak_'+TAG)
        backup.write_bytes(old)
        assert backup.read_bytes()==old
    tmp = p.with_name(p.name+'.tmp_'+TAG)
    tmp.write_bytes(b)
    assert tmp.read_bytes()==b
    os.replace(tmp,p)

def dump(p,obj):
    write(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

def axmap(text):
    raw={}
    for m in re.finditer(r"(?m)^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",text):
        assert m[1] not in raw
        raw[m[1]]=[v.strip() for v in (m[2] or '').split(',') if v.strip()]
    normalized={k:[re.sub(r'\.\{[^{}]*\}$','',x) for x in v] for k,v in raw.items()}
    return raw,normalized

pre=load(AREA/'preflight.json')
deps=load(AREA/'dependencies.json')
mods=pre['modules']
targets=[t for m in mods for t in m['targets']]
assert len(targets)==len(set(targets))==39
own=[]
for m in mods:
    r=load(AREA/(m['stem']+'.run.json'))
    for field in ['source','object','stdout','stderr']:
        assert pin(r[field]['path'])==r[field]
    assert r['returncode']==0 and r['exact_targets'] and r['trio_only'] and r['no_warnings_or_errors'] and r['stderr_empty']
    assert r['binary_byte_equal_to_author']
    assert pin(m['source_original']['path'])==m['source_original']
    assert pin(m['object_author']['path'])==m['object_author']
    assert Path(r['object']['path']).read_bytes()==Path(m['object_author']['path']).read_bytes()
    assert r['axioms']==m['author_axioms']
    for field in ['author_run','author_stdout','author_stderr']:
        assert pin(m[field]['path'])==m[field]
    own.append(r)

audit_initial=load(AREA/'AuditResolventPhase39.run.json')
for field in ['source','object','stdout','stderr']:
    assert pin(audit_initial[field]['path'])==audit_initial[field]
assert audit_initial['returncode']==0 and audit_initial['stderr_empty'] and audit_initial['no_warnings_or_errors']
audit_text=Path(audit_initial['stdout']['path']).read_text(encoding='utf-8-sig')
raw,normalized=axmap(audit_text)
assert set(raw)==set(targets)
assert all(set(v)<=TRIO for v in normalized.values())
type_matches=list(re.finditer(r'(?m)^@?(TGLV350\.Regular\.[A-Za-z0-9_]+)\s*:',audit_text))
types={}
for match in type_matches:
    end=audit_text.index("\n'"+match[1]+"'",match.start())
    types[match[1]]=audit_text[match.start():end]
assert set(types)==set(targets) and len(type_matches)==39
assert normalized=={k:v for r in own for k,v in r['axioms'].items()}
audit=dict(audit_initial)
audit['axioms_raw_with_universes']=raw
audit['axioms']=normalized
audit['trio_only']=True
audit['types_with_universes']=types
audit['parser_correction']={
    'initial_run_preserved':pin(AREA/'AuditResolventPhase39.run.json'),
    'cause':'pp.universes prints Classical.choice.{u}/Quot.sound.{u}; initial Python allowlist compared unnormalized names',
    'correction':'Remove only trailing .{...} universe annotation; preserve raw names and exact declarations',
    'lean_rerun':False,'lean_returncode_always_zero':True}
dump(AREA/'AuditResolventPhase39.verified.json',audit)
for d in deps:
    for field in ['source_origin','author_object','selected_object','frozen_source','frozen_object']:
        assert pin(d[field]['path'])==d[field], (d['module'],field)
counts=Counter(d['provenance'] for d in deps)
compilation={'time':NOW.isoformat(),'all_exit_zero':True,'independent_module_compilations':5,
             'independent_auditors':1,'exact_targets':39,'trio_only':True,
             'all_binary_byte_equal_to_author':True,'pins_preserved':True,
             'modules':own,'auditor':audit,'preflight':pin(AREA/'preflight.json'),
             'dependencies':pin(AREA/'dependencies.json'),'lean_path':pre['lean_path'],
             'toolchain':pre['toolchain'],'project_author_build_in_lean_path':False,
             'inherited_dependencies_not_recompiled':len(deps),'inherited_provenance_counts':dict(counts),
             'python_postprocessing_correction':audit['parser_correction'],
             'new_module_bytes_imported_from_author_build':False,
             'author_monolith_or_helpers_executed':False}
dump(AREA/'compilation.json',compilation)

ficha_md=ROOT/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.md'
ficha_json=ROOT/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json'
ficha=load(ficha_json)
providers=[]
for p in ficha['providers']:
    current=pin(p['path'])
    assert current['sha256']==p['sha256']
    providers.append(current)
for filename in [ficha_md.name,ficha_json.name,'DEPENDENCIAS_A1_FASE_RESOLVENTE.json']:
    assert (AREA/'inputs'/filename).read_bytes()==(ROOT/filename).read_bytes()
author_audit_path=ROOT/'AUDITORIA_A1_POTENCIAS_IMAGINARIAS.json'
author_audit=load(author_audit_path)
assert author_audit['checked_declarations']==39 and len(author_audit['modules'])==5
for a,m in zip(author_audit['modules'],mods):
    assert a['module']==m['stem']
    assert a['source_sha256']==m['source_original']['sha256']
    assert a['object_sha256']==m['object_author']['sha256']
    assert ['TGLV350.Regular.'+n for n in a['declarations']]==m['targets']
negatives=[]
for n in author_audit['negatives']:
    probe=pin(n['probe'])
    assert probe['sha256']==n['sha256']
    text=Path(n['stdout']).read_text(encoding='utf-8-sig')
    assert re.search(r'error: (unsolved goals|Type mismatch)',text) and 'sorryAx' in text
    assert not re.search(r'unknown module prefix|object file .* does not exist|Access is denied',text,re.I)
    match=re.search(r'attempts\\(\d{8}_\d{6}_\d{6})',text)
    assert match
    run_path=ROOT/'attempts'/match[1]/'run.json'
    run=load(run_path)
    assert run['returncode']==1
    negatives.append({'probe':probe,'stdout':pin(n['stdout']),'run':pin(run_path),
                      'returncode':1,'real_elaboration_failure':True,'sorryAx_excluded':True,
                      'mutation':n['mutation'],'execution':'author_only_logs_independently_read'})
adendo=ROOT/'ADENDO_A1_POTENCIAS_IMAGINARIAS.md'
extra_sources=[ROOT/'kernel/TGLExt'/name for name in [
    'V350ScalarWeightTomitaIdentification.lean','V350ScalarTomitaSquare.lean',
    'V350ScalarTomitaResolvent.lean','V350ScalarTomitaPolarResolvent.lean',
    'V350DenseLinearPolarExtension.lean','BoundedGraphOperator.lean']]
extra_pins=[pin(p) for p in extra_sources]
declarations=[]
for m in mods:
    source=Path(m['source_snapshot']['path']).read_text(encoding='utf-8-sig')
    for full in m['targets']:
        name=full.split('.')[-1]
        match=re.search(r'(?m)^(def|theorem)\s+'+re.escape(name)+r'(?=\s|[(:])',source)
        assert match
        statement=source[match.start():].split(' :=',1)[0]
        declarations.append({'name':full,'module':m['stem'],'kind':match[1],
                             'line':source[:match.start()].count('\n')+1,
                             'source_statement':statement,'elaborated_type':types[full],
                             'axioms':normalized[full]})
kind_counts=Counter(d['kind'] for d in declarations)
assert kind_counts=={'def':6,'theorem':33}
history=[h for m in mods for h in m['history_excluded']]
assert len(history)==8 and all(h['returncode']==1 for h in history)
partial_md=OUT/'REVIEW_A1_FASE_RESOLVENTE_PARCIAL.md'
partial_json=OUT/'REVIEW_A1_FASE_RESOLVENTE_PARCIAL.json'
partial=load(partial_json)
assert pin(partial_md)==partial['report']
rows='\n'.join(f"| `{m['stem']}` | {len(m['targets'])} | `{m['source_original']['sha256']}` | `{m['object_author']['sha256']}` |" for m in mods)
attempt_rows='\n'.join(f"- `{m['stem']}`: `{Path(m['author_run']['path']).parent.name}`; próprio `{Path(r['stdout']['path']).name}`, rc0, {r['seconds']:.2f}s." for m,r in zip(mods,own))
report=f'''# Parecer final — fase do resolvente no mesmo GNS

Data: {NOW.isoformat()}. **[REAL — revisão DEV independente encerrada, cinco módulos/39 declarações].**

**P0=0; P1=0; P2=0; findings=[]**. Aceito o delta delimitado: construção unitária pelo resolvente efetivo, grupo, continuidade forte e caracterização única no mesmo `ScalarGNSHilbert P`. A1(b), identificação da ação com AdΛ, gerador h e traço continuam **[OPEN]**. Nenhuma pendência de revisão dos cinco fontes permanece.

O parecer parcial de 19 alvos continua byte a byte preservado. Ele registra a leitura anterior sem compilação própria; este parecer acrescenta a reprodução agora expressamente solicitada. Não é aceite de integração no monólito nem de custódia futura.

## Evidência própria e pins

Executei **cinco recompilações e um auditor Lean separado**, todos rc0 e sem warnings. Os cinco `.olean` próprios são byte a byte idênticos aos autorais. O auditor contém `#check @nome` com universos e `#print axioms` de **exatamente 39 nomes: seis definições e 33 teoremas**. Todos usam somente `propext`, `Classical.choice`, `Quot.sound`; sem `sorry`, `axiom`, `native_decide` ou `trustCompiler` nos candidatos. Tipos elaborados, fontes, comandos, streams e hashes estão no JSON final e na árvore independente.

Compilação: [{AREA.name}/compilation.json](<{AREA/'compilation.json'}>), SHA256 `{pin(AREA/'compilation.json')['sha256']}`. Toolchain: `{mods[0]['author_metadata']['lean_version']}`; executável pinado. `LEAN_PATH` contém apenas a árvore própria e pacotes externos readonly, sem caminho de build autoral de projeto.

Foram congelados e reconferidos **448 pares fonte/objeto** do manifesto: **378** objetos vêm de snapshots prévios de revisão, **70** são herdados dos objetos autorais pinados, copiados para a árvore isolada após comparação de hashes. Essas 448 dependências **não foram recompiladas aqui**; ter bytes iguais ao manifesto não equivale a uma nova reprodução independente delas. A proveniência individual está em `dependencies.json`. Nenhum dos cinco módulos novos usou seu próprio binário autoral como importação.

| Módulo | Alvos | SHA256 fonte | SHA256 olean autoral = próprio |
|---|---:|---|---|
{rows}

Execuções autorais aceitas e streams próprios correspondentes:

{attempt_rows}

O auditor próprio durou {audit['seconds']:.2f}s. Seu rc0 foi obtido na primeira execução. O pós-processador Python inicialmente recusou os nomes decorados `Classical.choice.{{u}}`/`Quot.sound.{{u}}` impressos com universos; corrigiu-se somente essa normalização, preservando o JSON inicial e o stream bruto. Não houve nova execução de Lean nem alteração de prova para esse ajuste; `AuditResolventPhase39.verified.json` registra a leitura corrigida.

## Hipóteses e conteúdo efetivo

**1. Funções (9).** `b(x)=x(1−x)` e `g_t(x)=b(x)exp(it·Real.log((1−x)/x))` têm as identidades de norma, estrela e produto declaradas. A continuidade conjunta é global em ℝ×ℝ. Fora de 0 e 1, o argumento do log é não nulo — Mathlib permite log de negativo como log do módulo. Nas duas pontas, `||g_t(x)||=||b(x)||→0` controla conjuntamente t e x. Não se usa continuidade da fase não amortecida nas pontas, nem extensão por zero fora de [0,1]. No interior do espectro positivo contrativo, o sinal é **+it log((1−x)/x)**.

**2. Cálculo funcional (10).** O Hilbert genérico está em `Type` (universo 0), complexo e completo para o CFC; os tipos efetivamente elaborados constam do auditor. A definição elementar `resolventDampingOperator` dispensa completude, como mostra seu tipo. T é limitado; as identidades de CFC/produto/Gram recebem auto-adjunticidade, e positividade do amortecimento/módulo/norma recebem `0≤T≤1`. O teorema da estrela é válido para todo T conforme o CFC total da biblioteca, mas isso não torna os outros teoremas incondicionais. Não há hipótese espectral escondida ou uso de cálculo holomorfo: usa-se a função contínua `z↦g_t(z.re)`. Aqui C₀=B e C_s C_t=B C_(s+t), não a lei unitária sem amortecimento.

**3. Extensão unitária e grupo (9).** Agora são recebidas explicitamente as injetividades de T e I−T. B=T(I−T) é positivo e injetivo, logo tem imagem densa; a injetividade de B usa a composição dessas duas aplicações. `Ran(B²)⊆Ran(C_t)` vem de **C_t C_−t=B²**, e Ran(B²) é densa. Assim `denseLinearEquiv` recebe as duas densidades e a igualdade `||C_t x||=||Bx||`; sua sobrejetividade está paga, não presumida. Define U_t como equivalência linear isométrica e prova U_t B=C_t. A lei do grupo é demonstrada em Ran(B²) e estendida por continuidade. Nenhuma inversa limitada de B, gap ou PVM é exigida.

**4. Continuidade (3).** Para T auto-adjunto, t↦C_t é contínua na **norma de operadores**, pelo CFC sobre o espectro compacto. Com `0≤T≤1` e ambas injetividades, a continuidade das órbitas em Ran(B), junto da constante Lipschitz 1 de cada U_t, dá continuidade conjunta `(x,t)↦U_t x` e continuidade forte. Não se afirma continuidade de t↦U_t em norma de operadores. A retipagem `t↦(x,t)` no corolário mantém exatamente essa topologia.

**5. Mesmo objeto concreto (8).** Os alvos recebem apenas `P : SiteProfile` e os parâmetros/vetores indicados; não há nova hipótese de modularidade. `scalarTomitaResolvent_complement_injective` transforma a igualdade (I−T)x=(I−T)y pelo J original, usa JT=(I−T)J e a injetividade de T/J. As condições do grupo são então descarregadas com os fornecedores concretos, sem trocar de GNS. A cadeia relida é `scalarClosedTomita_graph_eq_weight` → S do peso completo; `scalarTomitaSquare_apply` → Δ=S†S com domínio de composição; `scalarTomitaResolvent_graph` → T=(I+Δ)⁻¹ como igualdade de mapas parciais. Nenhuma identificação por homônimo é usada.

`scalarTomitaImaginaryPower_unique` afirma unicidade **entre mapas complexos limitados que satisfazem U·b(T)=g_t(T)**, ponto a ponto para todo vetor. Esta é uma caracterização densa efetiva da potência imaginária definida por resolvente. É correto chamar o grupo de Δ_ν^it **nessa construção concreta**; não foi provada nem alegada igualdade com uma API abstrata anterior de potências de `LinearPMap`. Grupo, inversa e continuidade forte estão especializados ao mesmo T e H_I.

## Documentação, históricos e limites

Li a ficha MD/JSON anterior ao código, seus oito fornecedores pinados e o `ADENDO_A1_POTENCIAS_IMAGINARIAS.md`. A ficha foi preservada; sua data/status são antecedentes e não aprovação antecipada. O adendo separa corretamente o pagamento deste subpasso das pontes de escala funcional, conjugação por J e ação nos geradores, ainda abertas. Essas pontes futuras não foram incluídas no aceite.

As **oito tentativas autorais rc1 anteriores** (2+3+2+1+0) foram localizadas e excluídas; nomes, logs e hashes constam da evidência. Prints parciais e `sorryAx` dessas tentativas não contam como prova. As cinco fontes finais correspondem aos snapshots rc0.

Também reli a auditoria autora e os dois controles negativos: multiplicar por 2 a norma da fase e trocar s+t por s−t. Ambos têm rc1, erros reais de elaboração e `sorryAx`, sem falha de acesso/importação. Os controles foram **executados pelo autor**, não repetidos por esta revisão; os logs e pins foram conferidos independentemente. Nenhum controle adicional foi necessário.

**Fronteira:** a igualdade U_t π(a) U_−t=π(Λ_t a Λ_−t), a identificação literal com um implementador esquerda/direita, o gerador h, sua perturbação e um habitante do contrato do traço não pertencem aos 39 alvos. Não se infere KMS por invariância, nem fechamento de A1(b). Nenhum monólito, integrador, recorder, memória ou gate foi executado/alterado pela revisão. Os únicos escritos desta rodada estão em `revisao/`.
'''
final_md=OUT/'REVIEW_A1_FASE_RESOLVENTE_FINAL.md'
final_json=OUT/'REVIEW_A1_FASE_RESOLVENTE_FINAL.json'
write(final_md,report.encode('utf-8'))
evidence={'time':NOW.isoformat(),'status':'ACCEPTED_DEV39__A1B_OPEN','P0':0,'P1':0,'P2':0,'findings':[],
          'scope':'Five frozen V351 modules, 39 declarations, own recompilation and auditor; no integration',
          'compilation':pin(AREA/'compilation.json'),'independent_compilation':pin(AREA/'compilation.json'),
          'report':pin(final_md),'modules':mods,'declarations':declarations,
          'counts':{'modules':5,'declarations':39,'definitions':6,'theorems':33,
                    'own_module_compilations':5,'own_auditors':1,'inherited_dependencies':448,
                    'prior_review_dependency_objects':378,'author_pinned_dependency_objects':70},
          'all_exit_zero':True,'binary_byte_equal_to_author':True,'axioms':normalized,
          'types_with_universes':types,'parser_incident_resolved':audit['parser_correction'],
          'dependencies':pin(AREA/'dependencies.json'),'ficha':[pin(ficha_md),pin(ficha_json)],
          'providers':providers,'direct_supplier_sources_read':extra_pins,
          'author_audit':pin(author_audit_path),'author_negatives_read_not_rerun':negatives,
          'author_history_excluded':history,'documentation':pin(adendo),
          'partial_preserved':[pin(partial_md),pin(partial_json)],
          'A1_b':'OPEN','AdLambda_identification':'OPEN','trace':'OPEN',
          'author_sources_modified':False,'monolith_executed':False,'memory_written':False,
          'gate_changed':False,'review_scope_complete':True}
dump(final_json,evidence)
assert pin(partial_md)==partial['report']
print(json.dumps({'report':pin(final_md),'evidence':pin(final_json),
                  'compilation':pin(AREA/'compilation.json'),'P0':0,'P1':0,'P2':0},ensure_ascii=False))
