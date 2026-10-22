"""Pin verification and write the delimited DEV review, preserving any existing report bytes."""
from pathlib import Path
import datetime,hashlib,json,re
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_adjoint_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes());H=json.loads((RUN/'author_history.json').read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REV);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode())
def link(label,p,line=None):return f'[{label}](<{p.as_posix()}{":"+str(line) if line else ""}>)'
for k in ['complete','all_exit_zero','all_axioms_allowed','exact_23_targets','two_binaries_equal_author','sources_unchanged','dependencies_preserved','previous_reviews_preserved','um_unchanged']:assert C[k],k
source_checks={};graph={}
for rel,r in M['sources'].items():
    raw=Path(r['path']).read_bytes();txt=raw.decode();assert sha(raw)==r['sha256']
    graph[rel[:-5].replace('/','.')]=r['imports']
    lines={n:i for i,l in enumerate(txt.splitlines(),1) if (a:=re.match(r'^(?:def|theorem)\s+(\w+)',l)) for n in [a[1]]}
    forbidden=re.findall(r'^.*(?:\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]).*$',txt,re.M)
    assert not forbidden
    source_checks[rel]={'declaration_lines':lines,'local_instances':re.findall(r'^local instance.*$',txt,re.M),'options':re.findall(r'^set_option.*$',txt,re.M),'forbidden_tokens':forbidden}
    assert not source_checks[rel]['local_instances']
for n,r in M['dependencies'].items():
    raw=Path(r['frozen_source']).read_bytes();assert sha(raw)==r['source_sha256']
    assert sha(Path(r['frozen_binary']).read_bytes())==r['sha256']
    graph[n]=re.findall(r'^import\s+([\w.]+)',raw.decode(),re.M)
visiting=set();done=set()
def visit(n):
    if n not in graph:return
    assert n not in visiting,n
    if n in done:return
    visiting.add(n)
    for d in graph[n]:visit(d)
    visiting.remove(n);done.add(n)
for n in graph:visit(n)
new={'TGLV350.AntilinearAdjointGraph','TGLV350.ScalarTomitaAdjoint'}
assert all(not(new & set(ds)) for n,ds in graph.items() if n not in new)
for item in H:
    assert sha(Path(item['log']).read_bytes())==item['log_sha256']
    row=json.loads(Path(item['log']).read_bytes())
    for k in ['stdout','stderr']:assert sha(Path(row[k]).read_bytes())==item[k+'_sha256']
for rel,r in M['sources'].items():
    ar=json.loads(Path(r['author_log']).read_bytes());assert sha((ROOT/'build'/Path(rel).with_suffix('.olean')).read_bytes())==r['author_binary_sha256']
    own=next(x for x in C['records'] if x['module']==rel)
    assert own['axioms']==r['author_axioms']
assert set(C['records'][-1]['axioms'])==set(M['declarations'])
audraw=Path(C['records'][-1]['stdout']).read_text(encoding='utf-8')
types=re.findall(r'^TGLV350\.Regular\.(\w+)(?:\s|\.\{)',audraw,re.M)
assert {'TGLV350.Regular.'+n for n in types}==set(M['declarations']) and len(types)==23
assert all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items())
custody=(ROOT/'closed_tomita_custody.json').read_bytes();assert sha(custody)==M['custody_sha256']
cfg=json.loads((ROOT/'environment.json').read_bytes());original=Path(cfg['original_source']);oh=sha(original.read_bytes());assert oh==json.loads(custody)['original_sha256']
pkg=Path(cfg['lean_path'][6]).parents[3]/'Mathlib'
refs={}
for rel in ['Analysis/InnerProductSpace/Adjoint.lean','Analysis/InnerProductSpace/Orthogonal.lean','Analysis/InnerProductSpace/Continuous.lean','Analysis/InnerProductSpace/Projection/Submodule.lean','LinearAlgebra/LinearPMap.lean']:
    p=pkg/rel;b=p.read_bytes();write(RUN/'mathlib_references'/rel,b);refs[rel]={'path':str(p),'sha256':sha(b)}
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'sources':source_checks,'project_import_graph_modules':len(graph),'acyclic':True,'no_old_dependency_imports_new_modules':True,'own_23_types_exact':True,'own_and_author_23_axioms_equal':True,'own_and_author_two_bins_equal':True,'all_history_logs_streams_preserved':True,'mathlib_references':refs,'original_sha256':oh,'working_sha256':sha((ROOT/'um.py').read_bytes()),'working_matches_previous_custody':sha((ROOT/'um.py').read_bytes())==json.loads(custody)['working_sha256'],'previous_reviews_preserved':True,'new_integration_inspected':False,'author_scripts_executed':False}
save(RUN/'verification_dev.json',result)
rows='\n'.join(f"| {Path(rel).stem} | {len(r['declarations'])} | `{r['sha256']}` | `{r['author_binary_sha256']}` |" for rel,r in M['sources'].items())
process='\n'.join(f"| {r['module']} | {r['returncode']} | {r['seconds']} |" for r in C['records'])
logs='\n'.join(f"| {Path(r['author_log']).name} | `{r['author_log_sha256']}` |" for r in M['sources'].values())
AG=ROOT/'kernel/TGLV350/AntilinearAdjointGraph.lean';ST=ROOT/'kernel/TGLV350/ScalarTomitaAdjoint.lean';aud=C['records'][-1]
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
report=f'''# Revisão independente DEV — adjunto antilinear de Tomita

{date}. **[REAL — dois módulos/23 alvos conferidos e recompilados; nenhum achado P0, P1 ou P2.]** Escopo: `AntilinearAdjointGraph` (11) e `ScalarTomitaAdjoint` (12), nas fontes finais congeladas. A composição S†S e módulos posteriores não foram lidos, compilados ou aprovados nesta revisão. Nenhuma integração nova foi examinada.

## Significado, hipóteses e composição das provas

{link('AntilinearAdjointGraph.lean',AG,13)} define a relação por **∀x∈D, ⟨Sx,y⟩=⟨z,x⟩** e o domínio por existência de tal z. Isso testa todo D, não somente o gráfico inicial ou algum subdomínio escolhido. A convenção complexa é linear na segunda entrada. Por isso o representante de cy é **conj(c)z**, exatamente o testemunho de `smul_mem'` (linha 25), e o mapa resultante é `LinearPMap (starRingEnd ℂ) H H`, antilinear. Não é um CLM em todo H nem um adjunto complexo-linear inadvertido.

{link('Escolha, unicidade e mapa',AG,32)}: `Classical.choose` escolhe um representante cuja existência consta da propriedade do subtipo; `choose_spec` fornece o pareamento. Essa escolha e a relação existem antes de hD, mas a unicidade e as leis do mapa usam explicitamente **hD : Dense D** (linhas 40–73). O `include hD` do lema de unicidade é efetivo no tipo impresso. A igualdade de produtos internos no conjunto denso implica igualdade dos representantes. Não se pressupõem continuidade, limitação ou fechabilidade de S na construção genérica, e não há afirmação de unicidade sem densidade.

{link('Maximalidade e fechamento',AG,80)}: qualquer par que satisfaz o pareamento fornece pertinência ao domínio e o valor escolhido igual ao representante proposto. `graph_eq` prova igualdade entre o gráfico efetivo do mapa parcial e toda a relação. Esta é interseção, sobre x∈D, de igualdades fechadas em H×H; Sx fica fixo em cada igualdade, dispensando continuidade de S. O que é fechado é **o gráfico**, não necessariamente D. Os tipos genéricos usam `H : Type` com `NormedAddCommGroup` e `InnerProductSpace ℂ`; não exigem `CompleteSpace H` e não reivindicam aqui generalização a `Type u` arbitrário.

{link('Aplicação ao mesmo objeto',ST,13)} especializa literalmente `scalarClosedTomitaDomain P` e `scalarClosedTomita P`, no `ScalarGNSHilbert P` anterior. A densidade do domínio de S é fornecida pelo teorema já construído. `domain_iff` explicita o quantificador sobre **todo D(S)**; `maximal` e `isClosed` herdam a relação exata. Os tipos auditados das conclusões de existência do mapa, fechamento, densidade e involução têm somente P como parâmetro estrutural: nenhuma premissa adicional de separação, densidade do adjunto, KMS ou inversibilidade foi acrescida a P. Não há instâncias locais novas nesses dois arquivos.

{link('Transporte do pareamento gaussiano',ST,45)} usa T=`scalarGaussianGNSMap P`: H_I→L²(ℝ,L²(ℝ,TowerHilbert P)), e o **adjunto limitado Mathlib T***. Para B∈ρ(N)' e x∈D(S), o par (Tx,TSx) pertence ao fecho do gráfico auxiliar pela prova anterior `scalarGaussian_maps_graph_closure`. A cadeia efetiva é

`⟨Sx,T*BΩg⟩ = ⟨TSx,BΩg⟩ = ⟨B*Ωg,Tx⟩ = ⟨T*B*Ωg,x⟩`.

As orientações de `adjoint_inner_right` e `adjoint_inner_left` foram confrontadas com a Mathlib. Assim T*BΩg pertence ao domínio máximo e tem representante T*B*Ωg (linha 64), sem inverter T. Ωg, T, a álgebra auxiliar e o gráfico transportado são os mesmos já revisados; não há substituição de peso, medida, fator Haar ou Hilbert por homônimo.

{link('Densidade de D(S†)',ST,75)} prova primeiro D(S†)⊥=0. Se v está no ortogonal, a pertinência acima dá `⟨T*BΩg,v⟩=0`, logo `⟨BΩg,Tv⟩=0` para todo B∈ρ(N)'. A órbita é densa pela separação de Ωg **para a imagem ρ(N)**; então Tv=0 e a injetividade gaussiana dá v=0. A equivalência Mathlib entre ortogonal trivial e fecho total usa a completude herdada de H_I. Não se pressupõe que T tenha inversa limitada, que sua imagem seja fechada/sobrejetiva, ou que Ωg seja separante para todo B(H). Não se usa interseção a.e. não enumerável. O grafo de imports de {len(graph)} módulos de projeto é acíclico, e nenhuma das {len(M['dependencies'])} dependências antigas importa estes dois novos módulos: não há circularidade introduzida na densidade ou na separação.

{link('Troca e involução',ST,93)} substitui x por Sx, legitimamente em D(S) por `scalarClosedTomita_maps_domain`, e usa S²x=x. Conjugar o pareamento fornece a relação trocada `(z,y)`. A maximalidade do domínio coloca S†y de volta em D(S†); a unicidade do representante prova `(S†)²y=y` (linhas 108–119). É involução no domínio invariante, não alegação de operador limitado definido em todo H_I. Nenhum J substituto é introduzido.

## Evidência própria e pins

| Fonte DEV | Alvos | SHA256 fonte lido | SHA256 .olean próprio = autor |
|---|---:|---|---|
{rows}

| Processo próprio | rc | Segundos |
|---|---:|---:|
{process}

**Três processos próprios rc0**, sem warnings ou stderr; 23 `#check` com universos e 23 `#print axioms`, cobertura exata dos alvos das fontes, sem pressupostos acrescentados pelo auditor. Todos usam apenas `propext`, `Classical.choice`, `Quot.sound`. Ambos os .olean coincidem byte a byte com os finais do autor. A leitura integral das fontes não encontrou `axiom`, `sorry`, `admit`, `unsafe`, atributo de redutibilidade ou mudança de transparência. As opções são somente `autoImplicit false`, desativação do linter de variáveis não usadas e `maxHeartbeats 1000000`.

Árvore: {link('manifest.json',RUN/'manifest.json')}; {len(M['dependencies'])} dependências de projeto próprias congeladas, herdadas do lote anterior, com fontes/binários e origem pinados; oito pacotes externos somente leitura. **Nenhum build autoral de projeto no LEAN_PATH**. Não recompilei esses pacotes/dependências nem renovei a certificação global deles; mantêm-se os limites da proveniência anterior e a errata histórica de comentário de `DualSemifiniteIdeal`. Compilador `{M['compiler_sha256']}`: {M['lean_version']}.

Resultados: {link('compilation.json',RUN/'compilation.json')}, {link('verification_dev.json',RUN/'verification_dev.json')}, {link('23 tipos e axiomas completos',Path(aud['stdout']))}. Auditor fonte `{aud['source_sha256']}`, binário `{aud['output_sha256']}`, stdout `{aud['stdout_sha256']}`. Referências Mathlib relevantes foram preservadas e pinadas no relatório de verificação.

| Log autoral final aceito | SHA256 do JSON |
|---|---|
{logs}

Os cinco logs JSON e seus streams foram lidos/preservados em {link('author_history.json',RUN/'author_history.json')}. Há três tentativas rc1: uma em `AntilinearAdjointGraph` (hD omitido do escopo do lema, metas excedentes/tipagem), duas em `ScalarTomitaAdjoint` (timeout de elaboração e simplificação da conjugação). Seus `sorryAx` são resíduos desses erros registrados, **não evidência aceita** e não achados pendentes das fontes finais. Só os dois logs finais rc0/fonte inalterada e as três execuções próprias finais sustentam esta conclusão; os 23 axiomas próprios coincidem com os finais autorais.

## Preservação e limites

Custódia antecessora lida e pinada: `closed_tomita_custody.json` SHA `{M['custody_sha256']}`; seu relatório de verificação, SHA `{M['custody_verification_sha256']}`, declara rc0/30 pares de backup e prefixo. Conferi seu pin e os hashes dos três pareceres vinculados; **não reexecutei o verifier nem uma auditoria integral dos 30 backups**. Original relido `{oh}`; cópia permanece `{result['working_sha256']}`. Os números 118 registros/75 controles/6456 Audit pertencem à custódia integrada anterior; os 23 DEV novos não foram somados a eles.

Foram preservados os hashes de todos os pareceres anteriores, inclusive `REVIEW_CLOSED_SCALAR_TOMITA.md`. Nenhuma fonte autoral, original, monólito, memória ou log foi alterado. Nenhum monólito, recorder, integrador ou teste autoral foi executado/importado. Todas as saídas estão em `revisao/`.

**Conclusão delimitada:** existe o adjunto antilinear máximo por pareamento de S no mesmo H_I; seu gráfico é fechado, seu domínio é denso, invariante e nele o adjunto é involutivo. Não são concluídos S†S, sua auto-adjunticidade/identificação modular, decomposição polar, KMS, igualdade I=n_ν, traço, Three Locks/H1–H3, promoção de gate ou runtime. **Nenhuma análise DEV necessária resta nestes dois módulos/23 alvos.**
'''
assert all('warning:' not in Path(r['stdout']).read_text(encoding='utf-8') and Path(r['stderr']).read_bytes()==b'' for r in C['records'])
p=REV/'REVIEW_SCALAR_TOMITA_ADJOINT.md'
raw=report.encode()
if p.exists():raw=p.read_bytes()+b'\n\n'+raw
write(p,raw)
save(RUN/'closure_dev.json',{'timestamp':date,'status':'DEV_COMPLETE_NO_P0_P1_P2','review_path':str(p),'review_sha256':sha(p.read_bytes()),'review_bytes':p.stat().st_size,'review_lines':len(p.read_bytes().splitlines()),'new_modules':2,'new_targets':23,'own_processes_rc0':3,'same_bins_as_author':True,'necessary_analysis_remaining':False,'findings':[],'working_sha256':result['working_sha256'],'new_integration_inspected':False})
print(json.dumps(json.loads((RUN/'closure_dev.json').read_bytes()),ensure_ascii=False,indent=2))
