from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'paired_blocks_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
V=load(RUN/'author_verification.json');C=load(RUN/'compilation.json');M=load(RUN/'build_manifest.json');S=load(RUN/'static_verification.json');H=load(RUN/'helper_static_inspection.json')
assert V['author_final_artifacts_validated'] and not V['complete']
assert C['complete'] and C['all_six_exit_zero'] and C['all_exact_targets'] and C['all_axioms_allowed'] and C['all_new_axioms_match_DEV'] and C['dependencies_preserved'] and C['external_direct_pins_preserved']
assert len(C['records'])==6 and not any(V[k] or H[k] for k in ['P0','P1','P2'])
for r in V['new_records']:
    mod=r['file'][:-5].replace('/','.');own=next(x for x in C['records'] if x['module']==mod)
    assert own['source_sha256']==r['source_sha256'] and own['output_sha256']==r['binary_sha256'],mod
    assert hf(own['command'][2])==own['output_sha256'] and hf(own['command'][3])==own['source_sha256']
    for k in ['stdout','stderr']:assert hf(own[k])==own[k+'_sha256']
    r['own_recompiled_binary_equal']=True;r['own_compile_seconds']=own['seconds']
newrows={r['file']:r for r in V['new_records']};V['records']=[newrows.get(r['file'],r) for r in V['records']]
assert C['records'][-1]['module']=='TGL.Audit' and C['records'][-1]['axioms']==load(RUN/'axioms.json')
for name,pin in V['artifact_pins'].items():assert hf(ROOT/name)==pin,name
assert hf(ROOT/'um.py')==V['working_sha256']
for r in V['records']:
    assert hf(ROOT/'kernel'/r['file'])==r['source_sha256'] and hf(ROOT/'build'/Path(r['file']).with_suffix('.olean'))==r['binary_sha256']
    for stream in ['stdout','stderr']:assert hf(r[stream+'_path'])==r[stream+'_sha256']
    assert hf(ROOT/'logs'/r['log_name'])==r['log_sha256']
for d in M['dependencies'].values():
    assert hf(d['source'])==hf(d['frozen_source'])==d['source_sha256']
    assert hf(d['origin_binary'])==hf(d['frozen_binary'])==d['binary_sha256']
    assert all(hf(p)==h for p,h in d['companions'].items())
for p,h in S['surface_pins'].items():assert hf(p)==h,p
parent=load(RUN/'square_resolvent_custody.json')
assert all(hf(p)==h for p,h in parent['review_sha256'].items())
assert hf(REV/'REVIEW_PAIRED_BLOCKS_DEV.md')==S['own_DEV_review_sha256']
assert hf(load(ROOT/'environment.json')['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==V['original_sha256']
assert not any((ROOT/n).exists() for n in V['new_custody_report_verification_absent'])
V.update({'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FINAL_INTEGRATION_INSPECTION_WITH_SIX_OWN_COMPILATIONS_ON_EXPLICITLY_INHERITED_BINARY_DEPS','complete':True,'new_Lean_executions':6,'own_integrated_compilation_sha256':hf(RUN/'compilation.json'),'own_build_manifest_sha256':hf(RUN/'build_manifest.json'),'own_integrated_binaries_equal_author':True,'own_full_Audit_equals_author_stream':True,'dependency_provenance_counts':M['provenance_counts'],'binary_inheritance_limitation':C['limitation'],'author_artifacts_phase_sha256':hf(RUN/'author_verification.json')})
def save_new(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists(),p
    t=p.with_name(p.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
save_new(RUN/'verification.json',(json.dumps(V,ensure_ascii=False,indent=2)+'\n').encode())
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
table='\n'.join('| '+r['module']+' | '+str(r['returncode'])+' | '+str(r['seconds'])+' | '+str(r['distinct_axioms'])+' | igual |' for r in C['records'])
pins='\n'.join('| '+r['file']+' | `'+r['source_sha256']+'` | `'+r['binary_sha256']+'` |' for r in V['new_records'])
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão integrada — blocos de projeção e teste ponderado original

{stamp} — **PAIRED_BLOCKS_INTEGRATED_REVIEW**

**[REAL] Aprovado o delta integrado de quatro módulos/27 alvos, sem achados P0–P2.** As seis recompilações próprias e as conferências dos registros finais estão concluídas. O {link(REV/'REVIEW_PAIRED_BLOCKS_DEV.md','parecer DEV27')} permanece intacto, SHA256 `{V['own_DEV_review_sha256']}`. Não resta análise necessária dentro deste escopo.

As quatro fontes são transposições literais dos bytes DEV, com a única troca `import TGLV350.` → `import TGLExt.V350`. As hipóteses, os tipos, os universos e os nomes são herdados do auditor DEV27 conferido. As raízes acrescentam apenas os quatro imports e os 27 pedidos de axiomas; preservam as declarações anteriores e suas multiplicidades.

## Execução própria e herança binária

**[REAL — seis execuções Lean próprias]** Árvore isolada em `revisao/`, sem build autoral no `LEAN_PATH`, sem recompilar dependências antigas. Todos os seis binários resultantes são byte a byte iguais aos autorais finais.

| Módulo | rc | Segundos | Alvos impressos distintos | Binário próprio/autoral |
|---|---:|---:|---:|---|
{table}

O Audit próprio coincide integralmente com o mapa extraído do stream autoral corrente: **7133 declarações distintas**, todas com axiomas contidos em `propext`, `Classical.choice`, `Quot.sound`. As **7106 anteriores** permanecem com os mesmos axiomas; os **27 novos** coincidem exatamente com o manifesto e com o auditor DEV próprio.

**Limitação explícita de proveniência:** a reconstrução própria cobre os seis comandos acima, não a biblioteca inteira. As **900 dependências de projeto** foram copiadas da árvore própria anterior `square_resolvent_integrated_20260913_060615_561897`, com fontes/binários/pins conferidos: **307** vieram de caches próprios anteriores; **3** foram recompiladas independentemente no delta Square20; **205** têm origem em binários autorais integrados e custodiados; **385** têm origem na base canônica, sem reconstrução independente integral. Essas duas últimas categorias continuam herdadas, mesmo estando agora numa árvore própria. Não se renomearam binários DEV para fabricar aliases integrados. Os oito caminhos de pacotes externos ficaram readonly; compiler, imports externos diretos, fontes, binários e companheiros mantiveram os pins. A correspondência fonte→binário de dependências herdadas conserva essa limitação.

## Registros autorais conferidos por leitura

**[REAL — inspeção, sem reexecutar programas autorais]** Relidos os **220 pares fonte/binário**, seus logs JSON e streams: **214 registros idênticos aos da mãe e seis novos** (quatro módulos e duas raízes), com rc0 e fonte inalterada durante compilação. Os imports diretos dos seis novos têm outputs anteriores aos respectivos binários.

Os **107/107 controles** constam aprovados nos registros autorais. Os 106 anteriores foram preservados, com um novo grupo: `{V['added_controls'][0]}`. O grupo exige os sete alvos sentinela previstos e mantém a fronteira; a auditoria matemática completa aqui comparou os 27, não somente esses sete.

- Cópia atual: `{V['working_sha256']}`; **922 embutidos**, batch **776**.
- Mãe `square_resolvent_custody.json`: `{V['parent_custody_sha256']}`.
- Original e cópia-base relidos somente por hash: `{V['original_sha256']}`.
- Corpo Python fora de `_EMBEDDED_KERNEL_FILES` idêntico ao backup da mãe; `gate_extension.py` idêntico. As seis flags maiores permanecem falsas; gate legado preservado, `full_plan_complete=false`, nenhum runtime integral.
- Audit corrente: **{V['final_Audit_record']['log_name']}** → stdout bruto → mapa reanalisado. SHA256 do stream `{V['final_Audit_record']['stdout_sha256']}`; `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com esses bytes. Os valores históricos permanecem separados em `historical_v350_audit_metadata`.

## Helpers e estado anterior à gravação

Lidos integralmente e inspecionados estaticamente `prepare_paired_blocks_stage.py`, `record_paired_blocks_progress.py` e `verify_paired_blocks_custody.py`. O delta dos scripts altera somente a lista/batch de integração, os quatro módulos antes das raízes e o grupo de controle. O preparador exige leitura do DEV e seus quatro pares de pins; o recorder exige os dois pareceres, confere pai, fontes/binários/rc0, Audit corrente/histórico e 34 estados anteriores. O verifier relê os pares compilados e os backups/prefixos, além dos pins do relatório e artefatos.

As **34 memórias continuam byte a byte nos pins da mãe**, relidos antes de concluir. Recorder/verifier novos não foram executados por esta revisão; a nova custódia e o relatório autoral integrado ainda estão ausentes. Os backups/appends futuros são apenas lógica examinada: backup imediato de bytes na mesma pasta, verificação de prefixo e substituição atômica por arquivo; não uma transação atômica conjunta de 34 arquivos.

O texto do recorder distingue corretamente as seis flags qgf/gpf das entradas diretas do avaliador legado (`qgc_`, `qgp_`, feed), com `kernel_frontier` como anexo. Referências a roteiros seguintes permanecem OPEN; não houve nova análise matemática desses guias nem novos alvos atribuídos a eles.

## Alcance matemático mantido

No mesmo H_I, E e S original: o gráfico dos pares fornece os blocos A,B,D na álgebra efetiva M, com `0≤A≤I`, A injetivo, `BB*=A(I−A)` e `BD=(I−A)B`, sem supor `[A,B]=0`. A é bloco de projeção, não o operador modular Δ.

Para η fixo pelo S original e **e∈M, e*=e, [e,A]=0** explícitos, as duas ações de `K=e(I−A)B` são provadas; `Yη=eBB*η` pertence ao domínio original e `S(Yη)=B*eBη=Zη`. Para a seleção variacional e `Re z>0`, vale `2〈ξ,Zη〉=z〈η,Zη〉+conj(z)〈Yη,η〉`. Isso não pressupõe positividade de e nem a deduz, e não afirma comutação de e com B.

**[OPEN]** Cota inferior uniforme positiva de A/inverso limitado, escolha CFC que a produziria, inclusão inversa pelo J original, identificação de Δ^it/KMS, traço e obrigações posteriores. O scope legado `{V['scope']}` não identifica por homonímia seu J com o J original do peso. Sem promoção de gate, aprovação QG ou execução/importação de monólito. **Aceite limitado à integração DEV27.**

## Evidências e pins finais

- {link(RUN/'verification.json','Verificação final')} — `{hf(RUN/'verification.json')}`.
- {link(RUN/'compilation.json','Seis recompilações próprias')} — `{hf(RUN/'compilation.json')}`.
- {link(RUN/'build_manifest.json','Fontes, dependências e proveniência')} — `{hf(RUN/'build_manifest.json')}`.
- {link(RUN/'helper_static_inspection.json','Inspeção estática dos helpers')} — `{hf(RUN/'helper_static_inspection.json')}`.
- {link(RUN/'axioms.json','Audit atual reanalisado')}; {link(RUN/'author_verification.json','Conferência dos 220 registros autorais')}; streams próprios e cópias dos logs autorais na mesma árvore.

| Fonte | SHA256 fonte integrada | SHA256 binário próprio = autoral |
|---|---|---|
{pins}
'''
p=REV/'REVIEW_PAIRED_BLOCKS_INTEGRATED.md';raw=text.encode();prefix=0;backup=None
if p.exists():
    before=p.read_bytes();backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    save_new(backup,before);prefix=len(before);raw=before+b'\n\n'+raw
    tmp=p.with_name(p.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));save_new(tmp,raw)
    assert p.read_bytes()==before and tmp.read_bytes().startswith(before);tmp.replace(p)
else:save_new(p,raw)
assert p.read_bytes()==raw and hf(REV/'REVIEW_PAIRED_BLOCKS_DEV.md')==V['own_DEV_review_sha256']
pin={'report':str(p),'sha256':hf(p),'bytes':len(raw),'preserved_prefix_bytes':prefix,'backup':str(backup) if backup else None,'marker':'PAIRED_BLOCKS_INTEGRATED_REVIEW','verification_sha256':hf(RUN/'verification.json'),'scope':'FINAL_INTEGRATED_4_MODULES_27_TARGETS','findings':[]}
save_new(RUN/'review_pin.json',(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(pin,ensure_ascii=False))
