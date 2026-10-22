from pathlib import Path
from datetime import datetime
import hashlib,json,os,re,traceback
R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
OLD=R.parent;OUT=R/'revisao';V=R/'v';BUILD=V/'.lake/build/lib/lean'
B=OLD.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def ck(p):assert pin(Path(p['path']))==p,p
def save(p,value,text=False):
    assert p.resolve().is_relative_to(OUT.resolve()) and not p.exists(),p
    b=value.encode('utf8') if text else (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    t=p.with_name(p.name+'.tmp_'+STAMP)
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;os.replace(t,p)
def norm(n):return re.sub(r'\.\{[^}]*\}','',n).strip()
def parse_axioms(text):
    result={}
    for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))",text,re.S):
        n=norm(m[1]);v=[] if m[3] else [norm(a) for a in m[2].split(',') if a.strip()]
        assert n not in result or result[n]==v
        result[n]=v
    return result
def main():
    ptr=load(OUT/'SNAPSHOT_POINTER.json');ck(ptr['snapshot']);A=Path(ptr['attempt']);snap=load(Path(ptr['snapshot']['path']))
    comp=load(A/'completion.json');assert comp['status']=='BUILD_RC0__REVIEW_PENDING'
    ck(comp['run']);run=load(A/'run.json');assert run['returncode']==0
    built_log=re.findall(r'^.*?\[\d+/\d+\] Built (\S+)',(A/'lake_stdout.txt').read_text(encoding='utf8'),re.M)
    non_project_built=[n for n in built_log if not n.startswith(('TGL.','TGLExt.')) and n not in ('TGL','TGLExt')]
    assert not non_project_built,non_project_built
    for p in run['streams']+run['executables']+snap['configs']+snap['documents']+snap['protected']+[snap['own_auditor'],snap['B6_receipt'],snap['cache_parent_compilation']]:ck(p)
    for s in snap['sources']:ck(s['original']);ck(s['copy'])
    for p in snap['original_v351']:ck(p['original']);ck(p['v353'])
    cache=load(A/'cache_provenance.json')
    for pkg in cache['packages']:ck(pkg['manifest'])
    namespace_check=load(A/'package_namespace_check.json');assert namespace_check['no_project_namespace_objects_in_inherited_packages']
    assert all(not p['project_namespace_objects'] for p in namespace_check['packages'])
    names=[t['name'] for t in snap['targets']];assert len(names)==len(set(names))==40
    owntrace=BUILD/'TGLExt/ReviewA1Orphans.trace';tr=load(owntrace);types={};axioms={}
    for e in tr['log']:
        assert e.get('level') not in ['warning','error'],e
        if e.get('level')!='info':continue
        msg=e['message']
        if 'depends on axioms:' in msg or 'does not depend on any axioms' in msg:axioms.update(parse_axioms(msg))
        else:
            msg=re.sub(r'^.*?\.lean:\d+:\d+:\s*','',msg,count=1)
            for n in names:
                if re.match(re.escape(n)+r'(?:\.\{[^}]*\})?(?:\s|$)',msg):
                    assert n not in types;types[n]=msg
    assert set(types)==set(axioms)==set(names)
    assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in axioms.values())
    author_cold=load(A/'author_cold_replay_read.json');assert author_cold['returncode']==0
    for p in [author_cold['run'],author_cold['stdout'],author_cold['stderr']]:ck(p)
    author_objects={x['module']:x for x in author_cold['objects']}
    for row in author_objects.values():
        for k in ['source','object','trace']:ck(row[k])
    objects=[];warnings=[];target_objects=[]
    for mod in [s['module'] for s in snap['sources']]+['TGLExt.ReviewA1Orphans']:
        p=BUILD/(mod.replace('.','/')+'.olean');tp=p.with_suffix('.trace');tt=load(tp)
        for e in tt['log']:
            assert e.get('level')!='error',e
            if e.get('level')=='warning':warnings.append(dict(module=mod,**e))
            if e.get('level')=='trace' and 'LEAN_PATH=' in e.get('message',''):
                paths=e['message'].split('LEAN_PATH=',1)[1].split(' c:',1)[0].split(';')
                assert all(Path(path).resolve().is_relative_to(V.resolve()) for path in paths),(mod,paths)
        row=dict(module=mod,own=pin(p),trace=pin(tp),target=mod in snap['modules'])
        if row['target']:
            expected={t['name'] for t in snap['targets'] if 'TGLExt.'+t['module']==mod}
            amap=parse_axioms('\n'.join(e['message'] for e in tt['log'] if e.get('level')=='info'))
            assert set(amap)==expected and all(amap[n]==axioms[n] for n in expected)
            old=OLD/'build'/p.relative_to(BUILD);baseline=B/'kernel/.lake/build/lib/lean'/p.relative_to(BUILD)
            row['old_author_object']=pin(old);row['v353_object']=pin(baseline) if baseline.is_file() else None
            row['v353_object_status']='AVAILABLE' if row['v353_object'] else 'FILE_NOT_FOUND_AT_LAKE_PATH'
            row['v353_object_path_checked']=str(baseline)
            row['equal_to_old_author']=row['own']['sha256']==row['old_author_object']['sha256']
            row['equal_to_v353']=row['own']['sha256']==row['v353_object']['sha256'] if row['v353_object'] else None
            fresh_author=author_objects[mod]
            coldax=parse_axioms('\n'.join(e['message'] for e in load(Path(fresh_author['trace']['path']))['log'] if e.get('level')=='info'))
            assert set(coldax)==expected and all(coldax[n]==axioms[n] for n in expected)
            row['author_cold_object']=fresh_author['object']
            row['equal_to_author_cold']=row['own']['sha256']==fresh_author['object']['sha256']
            target_objects.append(row)
        objects.append(row)
    target_warnings=[w for w in warnings if w['module'] in snap['modules']+['TGLExt.ReviewA1Orphans']]
    assert not target_warnings,target_warnings
    count=len([p for p in BUILD.rglob('*.olean') if p.relative_to(BUILD).parts[0] in ['TGL','TGLExt']])
    assert count==len(objects)==len(snap['sources'])+1
    fiche=load(R/'REAPROVEITAMENTO_RETORNO_A1B.json');targets=load(R/'ALVOS_RETORNO_A1B.json')
    assert targets==snap['targets']
    assert [sum(t['kind']==k for t in targets) for k in ['theorem','def']]==[36,4]
    flattened=[]
    for m in fiche['modules']:
        ck(m['original']);ck(m['v353']);flattened+=m['declarations']
        lines=Path(m['original']['path']).read_text(encoding='utf-8-sig').splitlines()
        for t in m['declarations']:
            ck(t['source']);assert t['name'].split('.')[-1] in lines[t['line']-1]
    assert flattened==targets
    for p in fiche['prior_fiches_and_searches']:ck(p)
    history=load(A/'historical_runs.json');accepted={};rejected=[]
    for h in history:
        ck(h['run']);rr=load(Path(h['run']['path']));assert rr['returncode']==h['returncode']
        for p in h['streams']:ck(p)
        for s in h['sources']:
            if s['snapshot']:ck(s['snapshot'])
            if h['returncode']==0 and s['matches_current']:
                stdout=next(p for p in h['streams'] if Path(p['path']).name=='stdout.txt')
                oldax=parse_axioms(Path(stdout['path']).read_text(encoding='utf-8-sig'))
                targetset={t['name'] for t in targets if t['module']==s['module']}
                assert set(oldax)==targetset and all(oldax[n]==axioms[n] for n in targetset)
                accepted[s['module']]=h
        if h['returncode']!=0:rejected.append(h)
    assert set(accepted)=={m.split('.')[-1] for m in snap['modules']}
    semantic=load(A/'semantic_inspection.json');assert not semantic['findings']
    principal=load(A/'principal_inspection_read.json')
    for p in principal['documents']:ck(p)
    assert len(principal['exact_16_names'])==16 and set(principal['exact_16_names'])<=set(names)
    principal_doc=load(Path(principal['documents'][0]['path']))
    assert principal_doc['reviewer']=='principal' and all(not principal_doc[k] for k in ['P0','P1','P2'])
    for m in principal_doc['modules']:
        ck(m['source']);assert m['source']['sha256']==next(x['original']['sha256'] for x in snap['sources'] if x['module']=='TGLExt.'+m['module'])
    for p in principal_doc['providers']:ck(p)
    # Prior authorship is not converted into personal reviewer independence.
    assert 'authored by this sidecar' in semantic['independence_limit']
    for p in semantic['source_pins']+semantic['interfaces']+[semantic['lacunas']]:ck(p)
    latest=dict(timestamp=datetime.now().astimezone().isoformat(),fiche=pin(R/'REAPROVEITAMENTO_RETORNO_A1B.json'),ficha_md=pin(R/'REAPROVEITAMENTO_RETORNO_A1B.md'),targets=pin(R/'ALVOS_RETORNO_A1B.json'),consumer=fiche['consumer'],source_and_provider_pins_checked=True,seven_current_sources_equal_v353=True,nineteen_current_sources_equal_v353=True,historical_accepted_same_source_runs=list(accepted.values()),historical_failed_runs_excluded=rejected,history=pin(A/'historical_runs.json'),semantic=pin(A/'semantic_inspection.json'),semantics=semantic['modules'],independence_limit=semantic['independence_limit'],remaining=semantic['remaining'],principal_inspection=pin(A/'principal_inspection_read.json'))
    save(A/'final_inspection.json',latest)
    binary_diffs=[dict(module=x['module'],own=x['own'],old=x['old_author_object'],v353=x['v353_object'],equal_to_old=x['equal_to_old_author'],equal_to_v353=x['equal_to_v353'],author_cold=x['author_cold_object'],equal_to_author_cold=x['equal_to_author_cold']) for x in target_objects if not x['equal_to_old_author'] or x['equal_to_v353'] is False or not x['equal_to_author_cold']]
    compilation=dict(timestamp=latest['timestamp'],status='INDEPENDENT_LAKE_A1_ORPHANS_RC0',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This standalone private Lake replay only',run=pin(A/'run.json'),author_cold_replay_read=pin(A/'author_cold_replay_read.json'),source_snapshot=ptr['snapshot'],targets={t['name']:dict(kind=t['kind'],module=t['module'],source=t['source'],line=t['line'],typecheck=types[t['name']],axioms=axioms[t['name']]) for t in targets},exact_target_count=40,existing_theorems=36,existing_definitions=4,new_theorems=0,all_axioms_allowed=True,all_target_typechecks_present=True,own_auditor=pin(owntrace),objects=objects,target_objects=target_objects,target_binary_differences=binary_diffs,source_project_object_count=count,v353_binary_comparison_unavailable=[x['module'] for x in target_objects if x['v353_object'] is None],project_objects_inherited=False,project_objects_copied_from_author=False,package_cache_inherited=True,cache_provenance=pin(A/'cache_provenance.json'),package_pins=cache['packages'],package_cache_not_rebuilt=True,non_project_built_log_entries=non_project_built,historical_v353_object_availability=pin(A/'historical_v353_object_availability.json'),package_namespace_check=pin(A/'package_namespace_check.json'),source_configs=snap['configs'],target_warnings=target_warnings,existing_supplier_warnings=warnings,protected_originals_unchanged=True,protected_pins=snap['protected'],historical_author_failed_attempts=len(rejected),historical_author_all_attempts_exit_zero=not rejected,independence_limit=semantic['independence_limit'])
    save(OUT/'compilation.json',compilation)
    review=dict(timestamp=latest['timestamp'],status='A1_ORPHANS_REPLAY_ACCEPTED__REVIEW_ROLES_SEPARATED__A1_B_OPEN',marker='A1_ORPHANS_REVIEW',P0=[],P1=[],P2=[],findings=[],observations=[semantic['independence_limit'],'Byte identity of binaries is reported, never forced or substituted for source/type/axiom validation.'],compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json'),final_inspection=pin(A/'final_inspection.json'),source_snapshot=ptr['snapshot'],target_binary_differences=binary_diffs,B6_receipt=snap['B6_receipt'],old_reports_and_V353_preserved=True,scope='Only the seven existing orphan modules and own #check/#print auditor. No new mathematics, target program, canonical changes or runtime.',regular_dual_weight_modular_implementation='OPEN',RegularCoreTraceData_inhabitant='NOT_PRODUCED',personal_authorship_independence_for_two_antiunitary_modules=False,five_scaling_review_status='ACCEPTED_NO_P0_P1_P2',two_antiunitary_review_status='PRINCIPAL_SEMANTIC_INSPECTION_PINNED__PRIVATE_REPLAY_RC0',principal_inspection=pin(A/'principal_inspection_read.json'))
    save(OUT/'REVIEW_A1_ORPHANS_FINAL.json',review)
    table='\n'.join('| '+m['name']+' | '+str(len(m['declarations']))+' | `'+m['original']['sha256']+'` | `'+next(o['own']['sha256'] for o in target_objects if o['module']=='TGLExt.'+m['name'])+'` |' for m in fiche['modules'])
    difftext='Nenhuma diferença nos sete objetos comparados.' if not binary_diffs else 'Diferenças de .olean medidas (sem forçar identidade): '+', '.join(x['module'] for x in binary_diffs)+'. Os pins de ambas as origens e os booleanos por comparação estão no JSON; nenhuma troca de objetos ou nova compilação foi usada para fazê-los coincidir.'
    md=f'''# A1 — revisão e reprodução dos sete módulos órfãos

{latest['timestamp']} · **A1_ORPHANS_REVIEW**

[REAL] **Reprodução computacional dos sete aceita; cinco módulos de escala revisados sem P0–P2 encontrados.** Os dois antiunitários recebem minha conferência/reprodução e inspeção semântica independente do principal, pinada separadamente; preserva-se a autoria anterior deste sidecar. Sete fontes existentes, **40 declarações = 36 teoremas + quatro definições**, zero novos teoremas. Lake próprio rc0, quarenta `#check` com universos e mapas de axiomas próprios completos, apenas subconjuntos de `propext`, `Classical.choice`, `Quot.sound`. **A1(b) permanece OPEN.**

**Ressalva de independência:** os dois módulos antiunitários tiveram autoria deste sidecar na manhã, conforme relatório histórico preservado. Esta rodada é independente em árvore, objetos e execução, com releitura adversarial; não constitui independência pessoal retrospectiva sobre a própria autoria. A auditoria histórica autoral não foi rebatizada como aprovação independente. A inspeção independente posterior do principal foi lida integralmente e seus 16 alvos/fontes conferidos: INSPECAO_PRINCIPAL_ANTIUNITARIOS.md/json. Ela não aponta P0–P2 e fica pinada separadamente. Assim se distinguem autoria anterior, nova reprodução e inspeção independente, sem atribuir a esta auto-releitura uma independência pessoal inexistente.

## Resultado matemático que foi conferido

1. **Entrelaçamento CFC:** a união compacta dos dois espectros permite indução para funções complexas contínuas. A etapa de conjugação usa auto-adjunção de ambos. Para U(T)R=RU(Q), T,Q são contrações positivas e ambos os extremos são injetivos. R é somente limitado, sem inversibilidade.
2. **Escala:** para r>0, D_r(x)=r+(1−r)x é positivo em [0,1]. F_r(x)=x/D_r(x), e_r(x)=r/D_r(x)²; as identidades de complemento, amortecimento e fase tratam as pontas separadamente. Não se supõe continuidade através de polos fora do espectro. A fase é **exp(+it log r)**.
3. **Cálculo funcional e cancelamento:** E_r=e_r(T) é unidade limitada por CFC, B_Q=B_T E_r e C_Q=exp(it log r) C_T E_r. A sobrejetividade de E_r dá densidade de Ran B_Q; a igualdade se estende por continuidade. **Não se inverte B_T=T(1−T)** nem o operador de entrelaçamento; não há gap novo.
4. **Aplicação concreta:** os dois resultados de transporte usam o MESMO `scalarTomitaResolvent`, `scalarTomitaImaginaryPower`, `ScalarGNSHilbert P`, `matrixUnitRightData` e `regularRightGNS`. Positividade, injetividades, r=localEigenvalue>0 e TR=RQ_r são descarregados por fornecedores reais. Os resultados valem para todos os vetores do Hilbert, sem uma premissa de domínio escondida.
5. **Antiunitariedade:** a conjugação é homomorfismo de *-álgebras **sobre ℝ**, conjugando escalares complexos. CFC real e decomposição real/imaginária provam `star(g_t(1−x))=g_t(x)`. Os dois sinais se cancelam: **JU_tJ⁻¹=U_t**, não U_−t. Na camada genérica J²=I não é hipótese necessária. A especialização consome o flip do **J polar original**, sem substituí-lo pelo J da torre ou por unidade gaussiana. A igualdade final é de operadores limitados complexos, além da igualdade pontual.

Esses são fornecedores efetivos para `regular_dual_weight_modular_implementation`, não sua conclusão inteira. Falta o consumo da ação à esquerda em toda a álgebra conforme o contrato; comutação/escala pela direita e invariância por J não são, isoladamente, KMS. Os sete não produzem gerador regular positivo h, perturbação pelo inverso, traço, nem habitante de `TGLV351.RegularCoreTraceData`.

## Fontes, ficha e histórico

`RECIBO_B6` e seus pins de entrega/manifesto foram conferidos **antes de escrever/preparar** esta reprodução. Ficha MD/JSON e ALVOS atuais foram lidos, seus tipos/linhas/pins confrontados com as sete fontes. Os **19 V351** coincidem com o snapshot V353, inclusive os sete. A retomada reutiliza fichas/buscas anteriores e não anuncia busca exaustiva nova.

Os {len(history)} registros históricos pertinentes foram lidos e pinados: {len(accepted)} rc0 com fonte final e **{len(rejected)} rc1 excluídos**, inclusive saídas parciais. Seus axiomas rc0 coincidem com os próprios. Isso é histórico autoral distinto do novo Lake; falhas de ambiente/elaboração não são prova matemática nem adulteração válida. Nenhum teste negativo extra foi criado para esta reprodução de fontes imutáveis.

## Reprodução isolada

Projeto `{V}`; saída `{OUT}`. Comando próprio: `lake build` dos sete módulos e `TGLExt.ReviewA1Orphans`. **{len(snap['sources'])} fontes de projeto** copiadas em bytes da árvore antiga por fecho de imports; **{count} objetos próprios** construídos incluindo o auditor. Nenhum .olean TGL/TGLExt autoral ou de V353 foi herdado. Toolchain Lean 4.31.0, configurações iguais às pinadas; LEAN_PATH verificado nas traces dentro de v.

Mathlib e oito pacotes auxiliares foram copiados **em bytes, sem hardlinks**, do cache privado anterior em V353/s. Cada arquivo foi lido, copiado e comparado, com manifestos próprios de SHA256. São **objetos de pacotes herdados**, não recompilação independente da biblioteca. O inventário dos 121.039 arquivos de pacotes não contém objetos TGL/TGLExt; a checagem está pinada em compilation.json. A raiz curta foi conferida antes da cópia; não houve escrita em V353. Relatórios/fontes antigos A1 e pins B1–B6 permaneceram inalterados.

Nenhum aviso nos sete módulos e no auditor próprio. Os **{len(warnings)} avisos de fornecedores existentes** permanecem nas traces/JSON e não foram suprimidos pela revisão. Total de jobs Lake inclui cache, não equivale a número de novas provas.

{difftext}

Os sete objetos autorais antigos em OLD/build e os sete da reprodução autoral nova em k foram lidos para comparação; o run autoral rc0 e seus streams/pins também foram conferidos. Seus quarenta axiomas coincidem com os próprios. Nenhum objeto autoral foi usado no meu build. Os sete caminhos .olean de V353/kernel/.lake/build/lib/lean não existem (FileNotFoundError/Windows 2, confirmado com leitura elevada); a igualdade com V353 refere-se às fontes, e a comparação binária indisponível fica como null, não como igualdade ou divergência. Nenhum objeto foi buscado ou copiado para preencher essa ausência.

## Pins finais e evidência

| Módulo existente | Declarações | SHA256 fonte | SHA256 .olean próprio |
|---|---:|---|---|
{table}

- [Parecer JSON](<{(OUT/'REVIEW_A1_ORPHANS_FINAL.json').as_posix()}>) — `{pin(OUT/'REVIEW_A1_ORPHANS_FINAL.json')['sha256']}`.
- [Compilação](<{(OUT/'compilation.json').as_posix()}>) — `{pin(OUT/'compilation.json')['sha256']}`.
- [Run próprio](<{(A/'run.json').as_posix()}>) — `{pin(A/'run.json')['sha256']}`.
- [Snapshot](<{(A/'source_snapshot.json').as_posix()}>), [inspeção final](<{(A/'final_inspection.json').as_posix()}>) e [cache](<{(A/'cache_provenance.json').as_posix()}>) e [inspeção separada do principal](<{(A/'principal_inspection_read.json').as_posix()}>) e [replay autoral relido](<{(A/'author_cold_replay_read.json').as_posix()}>).

**Execução deste escopo encerrada.** A reprodução está concluída; a inspeção semântica por agente distinto dos dois antiunitários provém do documento do principal, não desta auto-releitura. Sem novo teorema-alvo, monólito, integração, entrega pelo túnel, alteração de gate/memória ou início de módulo posterior. O aceite é da reprodução e do significado limitado desses fornecedores; não quita A1(b).
'''
    save(OUT/'REVIEW_A1_ORPHANS_FINAL.md',md,True)
    for p in snap['protected']:ck(p)
    print(json.dumps(dict(status=review['status'],P0=[],P1=[],P2=[],report=pin(OUT/'REVIEW_A1_ORPHANS_FINAL.md'),json=pin(OUT/'REVIEW_A1_ORPHANS_FINAL.json'),compilation=pin(OUT/'compilation.json')),ensure_ascii=False,indent=2))
if __name__=='__main__':
    try:main()
    except Exception:
        save(OUT/('finalizer_failure_'+STAMP+'.json'),dict(timestamp=datetime.now().astimezone().isoformat(),script=pin(Path(__file__)),error=traceback.format_exc()))
        raise
