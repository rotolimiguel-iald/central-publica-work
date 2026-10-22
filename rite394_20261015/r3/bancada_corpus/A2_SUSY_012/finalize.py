
from support import *
import collections, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
K=ROOT/'k'
TRIO={'propext','Classical.choice','Quot.sound'}
def readj(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def pin(p):
    p=Path(p)
    return dict(path=str(p),bytes=p.stat().st_size,sha256=digest(p))
names=readj(ROOT/'AUDIT_NAMES.json')
modules=['TGLExt.'+m for m in names['modules']]
all_runs=[]
for rp in sorted((ROOT/'attempts').glob('*/RESULT.json')):
    d=readj(rp)
    all_runs.append((rp.parent,d))
def current_run(module,rc):
    src=K/Path(*module.split('.')).with_suffix('.lean')
    for p,d in reversed(all_runs):
        if d['module']==module and d['returncode']==rc and d['source_sha256']==digest(src):
            assert d['source_unchanged'] and d.get('imports_unchanged',True)
            assert (p/src.name).read_bytes()==src.read_bytes()
            return p,d
    raise RuntimeError('No matching successful/current receipt: '+module)
def axiom_rows(path):
    pairs=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",Path(path).read_text(encoding='utf-8'))
    assert len({p[0] for p in pairs})==len(pairs)
    return [dict(name=n,axioms=[x.strip() for x in a.split(',')]) for n,a in pairs]
def bundle(module,rc):
    p,d=current_run(module,rc)
    st=readj(p/'START.json')
    for out in d['outputs']:
        assert digest(out['path'])==out['sha256'], out['path']
    return dict(module=module,returncode=rc,attempt=str(p),seconds=d['seconds'],
        source=pin(st['source']),source_unchanged=d['source_unchanged'],
        imports_unchanged=d.get('imports_unchanged','NAO_REGISTRADO_NESSA_TENTATIVA'),
        command=st['command'],cwd=str(K),dependency_paths=st['dependency_paths'],
        build_tool_sha256=st['lean_sha256'],result=pin(p/'RESULT.json'),
        stdout=pin(p/'stdout.txt'),stderr=pin(p/'stderr.txt'),objects=[pin(o['path']) for o in d['outputs']])
version=subprocess.run([str(BIN/'lean.exe'),'--version'],capture_output=True,check=True).stdout.decode().strip()
builds=[bundle(m,0) for m in modules]
for b in builds:
    src=Path(b['source']['path'])
    dst=ROOT/'src/TGLExt'/src.name
    atomic(dst,src.read_bytes())
    assert digest(dst)==b['source']['sha256']
    b['review_source']=pin(dst)
audit=bundle('TGLExt.AuditA2Susy',0)
ax=axiom_rows(audit['stdout']['path'])
assert [x['name'] for x in ax]==names['names']+names['suppliers']
assert all(set(x['axioms'])==TRIO for x in ax)
assert 'fun P => TGLExt.susy_relative_gives_breuer (TGLV354.regularSusyData P)' in Path(audit['stdout']['path']).read_text(encoding='utf-8')
probes={m:bundle('TGLExt.'+m,0) for m in ['ProbePolarSupports','ProbeRegularSusy']}
for v in probes.values():
    v['axioms']=axiom_rows(v['stdout']['path'])
    assert v['axioms'] and all(set(a['axioms'])==TRIO for a in v['axioms'])
mutations=[
 ('BadPolarIdentity','ProbePolarSupports','TGLV354.Probes.zero_initial_is_not_identity',
  'Troca o suporte inicial pelo operador identidade para T=0 em H=complexos.',
  'A refutacao compilada prova u(0)*u(0)=0 e diferente de 1; a recusa de um termo so nao seria suficiente.'),
 ('BadSusyDifference','ProbeRegularSusy','TGLV354.Probes.removing_difference_is_false',
  'Ablacao diff=bottom, mantendo os mesmos gapD=PF e gapD0=bottom.',
  'A desigualdade mutada forca PF=bottom, contradizendo a projecao A2 nao nula.'),
 ('BadSusyZeroTrace','ProbeRegularSusy','TGLV354.Probes.zero_kernel_trace_is_false',
  'Troca a leitura A1 do mesmo nucleo por zero.',
  'A positividade de tau(ker) pelo consumidor e a identificacao exata tau(ker)=1 refutam zero.')]
controls=[]
for bad,good,refutation,change,reason in mutations:
    b=bundle('TGLExt.'+bad,1)
    log=Path(b['stdout']['path']).read_text(encoding='utf-8')
    errors=re.findall(r': error(?:\([^)]*\))?: ([^\n]*)',log)
    assert errors==['Type mismatch'], (bad,errors)
    assert not b['objects']
    assert refutation in [x['name'] for x in probes[good]['axioms']]
    controls.append(dict(status='REAL_RECUSA_COM_REFUTACAO_FORMAL',mutation=change,
        semantic_reason=reason,bad=b,errors=errors,refutation=refutation,good=probes[good]))
for m in ['AuditA2Susy','ProbePolarSupports','ProbeRegularSusy']+[x[0] for x in mutations]:
    atomic(ROOT/'audit/TGLExt'/(m+'.lean'),(K/'TGLExt'/(m+'.lean')).read_bytes())
record(ROOT/'CONTROLES.json',dict(timestamp=stamp(),status='REAL',controls=controls,
    scope='Tres mutacoes especificas; cada negativa tem refutacao formal rc0/trio. Nao se infere falsidade apenas da rejeicao do mesmo termo.'))
# Baseline sources are measured again; original caches are not rebuilt or rewritten.
baseline=readj(ROOT/'COPIA_A1.json')
preservation=[]
for row in baseline['files']:
    local=Path(row['local'])
    rel=local.relative_to(K)
    if local.suffix=='.lean' and rel.parts[0] in ['TGL','TGLExt']:
        original_now=digest(row['source'])
        local_now=digest(local)
        preservation.append(dict(source=row['source'],local=str(local),original_at_copy=row['sha256'],
            original_now=original_now,local_now=local_now,
            original_unchanged=original_now==row['sha256'],copy_identical=local_now==row['sha256']))
for row in readj(ROOT/'COPIA_A2.json')['sources']:
    local=K/'TGLExt'/Path(row['path']).name
    original_now=digest(row['path']); local_now=digest(local)
    preservation.append(dict(source=row['path'],local=str(local),original_at_copy=row['sha256'],
        original_now=original_now,local_now=local_now,
        original_unchanged=original_now==row['sha256'],copy_identical=local_now==row['sha256']))
assert all(r['original_unchanged'] and r['copy_identical'] for r in preservation)
record(ROOT/'PRESERVACAO_FONTES.json',dict(timestamp=stamp(),status='REAL',source_count=len(preservation),
    scope='Fontes Lean TGL/TGLExt A1 copiadas e oito fontes A2; hashes comparados ao momento da copia. Nao constitui medicao de toda raiz externa.',
    baseline_copy_files=len(baseline['files']),sources=preservation))
# Record real failures separately from deliberate controls.
attempts=[]
for p,d in all_runs:
    log=(p/'stdout.txt').read_text(encoding='utf-8')+(p/'stderr.txt').read_text(encoding='utf-8')
    attempts.append(dict(attempt=str(p),module=d['module'],returncode=d['returncode'],
        source_sha256=d['source_sha256'],source_unchanged=d['source_unchanged'],
        current_source=d['source_sha256']==digest(K/Path(*d['module'].split('.')).with_suffix('.lean')),
        deliberate_negative=d['module'] in ['TGLExt.'+x[0] for x in mutations],
        errors=re.findall(r': error(?:\([^)]*\))?: ([^\n]*)',log),
        sorryAx_in_failed_diagnostic='sorryAx' in log,
        result=pin(p/'RESULT.json'),stdout=pin(p/'stdout.txt'),stderr=pin(p/'stderr.txt')))
counts=dict(collections.Counter(str(a['returncode']) for a in attempts))
record(ROOT/'TENTATIVAS.json',dict(timestamp=stamp(),counts_by_returncode=counts,attempts=attempts,
    interpretation='Tentativas rc1 de desenvolvimento nao sao provas nem controles semanticos, exceto os tres Bad* explicitamente pareados. Todos os logs permanecem.'))
# This is a source-token check in addition to the transitive axiom audit, not its substitute.
new_sources=[K/'TGLExt'/(m+'.lean') for m in names['modules']+['AuditA2Susy','ProbePolarSupports','ProbeRegularSusy']+[x[0] for x in mutations]]
forbidden=[]
for p in new_sources:
    for line_no,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if re.search(r'\b(?:axiom|sorry|native_decide|trustCompiler)\b',line):
            forbidden.append(dict(path=str(p),line=line_no,text=line))
assert not forbidden
record(ROOT/'AUDITORIA.json',dict(timestamp=stamp(),status='REAL_AUTORAL',lean_version=version,
    lean_binary=pin(BIN/'lean.exe'),new_declarations=len(names['names']),suppliers=len(names['suppliers']),
    axioms=ax,allowed_axioms=sorted(TRIO),all_exact_trio=True,builds=builds,audit=audit,
    source_token_check=dict(files=len(new_sources),forbidden_hits=forbidden),controls=pin(ROOT/'CONTROLES.json'),
    limits=['Cache A1 e objetos A2 reutilizados conforme recibos; nao foi feito rebuild integral da mathlib ou de PF/split/gap.',
      'A instancia BoundedOrder anonima e consumida nos termos auditados; nao contada como uma das 29 declaracoes nomeadas.',
      'O polar foi compilado antes da instrumentacao IMPORTS_BEFORE; esta tentativa tem source_unchanged, sem medicao temporal dos imports. O consumidor final foi compilado e auditado depois.']))
# Functional consumer graph: deliberately no use invented for the removed lemmas.
consumer_edges={
 'boundedAbsolute_norm':['boundedPolar_mul_absolute','boundedPolar_norm','boundedAbsolute_ker (private)'],
 'boundedPolar':['boundedPolar_mul_absolute','boundedPolar_star_mul','projection_join_comparison'],
 'boundedPolar_mul_absolute':['boundedPolar_mul_star','boundedPolar_commutes'],
 'boundedAbsolute_range':['boundedPolar_norm','boundedPolar_commutes','V354PolarIntertwining (consumo informado pelo operador)'],
 'boundedPolar_norm':['boundedPolar_apply_eq_zero_iff','boundedPolar_star_mul','boundedPolar_initial_support'],
 'boundedPolar_apply_eq_zero_iff':['boundedPolar_commutes','projection_join_comparison'],
 'boundedPolar_star_mul':['boundedPolar_mul_star','projection_join_comparison'],
 'boundedPolar_initial_support':['boundedPolar_mul_star'],
 'boundedPolar_mul_star':['projection_join_comparison'],
 'boundedPolar_commutes':['boundedPolar_mem'],
 'boundedPolar_mem':['projection_join_comparison'],
 'coreProjectionSpaces':['CoreProjection'],
 'CoreProjection':['CoreProjection.operator','coreProjectionTrace','regularSusyData'],
 'CoreProjection.operator':['coreProjectionTrace','projection_join_comparison'],
 'CoreProjection.operator_mem':['CoreProjection.positive','projection_join_comparison'],
 'CoreProjection.operator_le_iff':['coreProjectionTrace','projection_join_comparison'],
 'CoreProjection.ofOperator':['regularSupportProjection'],
 'CoreProjection.operator_ofOperator':['regularSupportProjection_operator (private)'],
 'CoreProjection.operator_bot':['regularSusyData','regularSusy_operator_identifications'],
 'CoreProjection.sup_apply_eq_zero':['projection_join_comparison'],
 'CoreProjection.positive':['coreProjectionTrace','coreProjectionTrace_subadd'],
 'coreProjectionTrace':['coreProjectionTrace_subadd','coreProjectionTraceSubadditive'],
 'projection_join_comparison':['coreProjectionTrace_subadd'],
 'coreProjectionTrace_subadd':['coreProjectionTraceSubadditive'],
 'coreProjectionTraceSubadditive':['regularSusyData','regularSusy_gives_breuer'],
 'regularSupportProjection':['regularSusyData','regularSusy_operator_identifications'],
 'regularSusyData':['regularSusy_gives_breuer','regularSusy_operator_identifications'],
 'regularSusy_gives_breuer':['saida exigida: consumidor TGLExt.susy_relative_gives_breuer instanciado'],
 'regularSusy_operator_identifications':['saida exigida: identificacoes concretas D=1-PF,D0=1 e gap A2']}
assert set(consumer_edges)=={n.removeprefix('TGLV354.') for n in names['names']}
record(ROOT/'REAPROVEITAMENTO_EFETIVO.json',dict(timestamp=stamp(),status='REAL_AUTORAL',
    initial_fiche=pin(ROOT/'FICHA_REAPROVEITAMENTO.json'),consumer_graph=consumer_edges,
    actual_reuse=[
      'V350PositiveRootIntertwining.positive_sqrt_intertwines: transporte da raiz no boundedPolar_commutes.',
      'Mathlib LinearMap.extendOfNorm e projecao ortogonal: construcao do polar, sem hipotese de existencia.',
      'Mathlib VonNeumannAlgebra.IsStarProjection.mem_iff: representacao de todas as projecoes de N.',
      'A1 scalarInverseLimitWeight: monotonicidade, fidelidade, aditividade e tracialidade quadratica no mesmo N.',
      'A2 regularFiniteSupport: PF efetivo, nao nulo, traco 1; suporte/split anteriores reutilizados por import.',
      'A2 regularMinimalLock_spectral_zero e regularMinimalLock_relative_gap: identificacoes e gap efetivos.',
      'TGLExt.susy_relative_gives_breuer: consumidor aplicado diretamente a regularSusyData.'],
    rejected_or_delimited=[
      'TheMasterFires: outro Hilbert/traco dimensao; nao e a ponte entregue.',
      'V354PositiveTraceReader e V354TraceReaderWall: lidos para delimitar a tarefa, nao importados pelos quatro novos modulos.',
      'V354SelfAdjointPowerKernel e V354RegularLegacyWitness do principal: informados pelo operador; nao importados nem auditados aqui.',
      'WitnessV3_infinite: informado como ja pago na mesma Torre; esta ponte nao exige rederivar dimensao.',
      'Traço total/cyclicTraceCandidate/ContinuousCoreData/ThreeLocks: fora da construcao local.'],
    removed_unused=['CoreProjection.operator_injective','CoreProjection.operator_top'],
    review_status='A construcao SUSY aguarda revisao independente; parecer polar lido nao substitui auditoria da gerencia.'))
limits='''# Falhas e limites — entrega autoral A2 SUSY 012

[REAL] Quatro módulos candidatos compilaram no Lean 4.31.0. A auditoria efetiva imprime somente propext, Classical.choice e Quot.sound para as 29 declarações novas nomeadas e cinco fornecedores. Os três controles adulterados retornam rc1 por incompatibilidade de tipos; sua falsidade específica também está provada em sondas rc0/trio. Comandos, hashes e logs constam nos JSONs desta pasta.

[REAL] O reticulado representa todas as projeções ortogonais em regularCoreAlgebra P, por subespaços fechados invariantes sob o comutante. operator_mem, operator_ofOperator e operator_le_iff fornecem pertinência, representação e identificação da ordem. A API construída tem Lattice e BoundedOrder, com supremo binário; não acrescenta uma instância CompleteLattice nem teorema sobre supremos arbitrários.

[REAL] O traço é exatamente scalarInverseLimitWeight P aplicado à mesma projeção positiva. A subaditividade vem de u=boundedPolar((1-Q)P), com u em N, u* u <= P e u u* = (P join Q)-Q, e da tracialidade quadrática de A1. Não recebe subaditividade, Kaplansky ou existência de polar como premissa. O nome legado SemifiniteTraceData pede tau, monotonicidade e fidelidade; esta entrega não atribui ao nome uma nova prova de normalidade ou aproximação semifinita.

[REAL] O representante é D=regularMinimalLock P=1-PF e D0=1. ker=gapD=diff=PF; gapD0=bottom. As projeções de núcleo e a diferença 1-D são identificadas concretamente; o gap normativo no complemento do núcleo vem de A2. Não se acrescentou uma API de janelas espectrais de Borel. tauA1(PF)=1 é a normalização já provada em A2.

[OPEN] Não há identificação de Hamiltoniano microscópico, H1 físico resolvido ou confirmação da natureza. A flag gpf_H1_internal_susy_relative_gap_discharged é apenas proposta para exame neste alcance matemático; não foi editada. O acesso de busca ao um.py canônico foi recusado pelo sistema (erro 5); a implementação corrente dessa flag não foi inspecionada. A proposta se ancora no contrato e na instrução do operador.

[INPUT] A bancada principal informou sucesso da compatibilidade positiva e da montagem de regularLegacyCore, além da correção de instância em ThreeLocks e do fornecedor witnessV3_infinite na mesma Torre. Essas fontes não foram copiadas/importadas para esta ponte nem auditadas aqui. O total trace e ThreeLocks ficam fora deste pacote.

[REAL] A cópia A1 contém os bytes e hashes descritos em COPIA_A1.json. Seis objetos A2 e CoreSupport foram reutilizados com recibos; não foi repetido o trabalho PF/split/gap nem um rebuild completo da base. PRESERVACAO_FONTES.json remede as fontes TGL/TGLExt A1 copiadas e as oito fontes A2, sem alegar medição de toda raiz externa. As cópias próprias são arquivos independentes, sem hardlinks. Backups locais foram mantidos por bytes. Atlas, memórias externas, túnel, A2 e canônico não receberam escrita desta tarefa.

[REAL] As tentativas anteriores não foram apagadas. Houve builds prematuros com cópia ainda incompleta (imports Mathlib/Aesop ausentes), falta local do objeto CoreSupport e erros de elaboração Lean em nomes, coerções, reescritas dependentes e álgebra não comutativa. A sonda positiva SUSY teve uma tentativa com nome bot_sup inexistente; corrigida para bot_sup_eq. TENTATIVAS.json separa esses erros dos controles deliberados. Algumas saídas rc1 imprimem sorryAx por declarações com erros: não são objetos aceitos, nem fonte com sorry, nem evidência positiva.

[REAL] Permanecem avisos de aliases deprecated (mul_apply/zero_apply) e um aviso de ext em sonda. Não são erros de compilação. Os módulos novos usam o orçamento padrão de heartbeats; não se alega mínimo empírico. O build do polar precedeu a instrumentação de hashes temporais dos imports; seu receipt mede fonte estável, sem afirmar imports_unchanged naquela tentativa. O restante final registra a estabilidade dos imports diretos.

[REAL] Falhas auxiliares de consulta/empacotamento: buscas amplas tiveram saídas truncadas e caminhos presumidos inexistentes; uma busca por arquivos atravessou pastas sem acesso. Não se declara ausência exaustiva de fornecedores. Houve erro de aspas numa tentativa de gerar finalize.py antes de qualquer execução desse script, seguido de arquivo não encontrado; houve também UnicodeEncodeError ao imprimir a ficha em cp1252, sem alterar a ficha. A versão corrigida do empacotamento foi executada após esses erros. Nenhum desses erros é apresentado como controle semântico.

[OPEN] Revisão independente e aceite da gerência pendentes. Os snapshots POLAR_SNAPSHOT_001/002 são recibos históricos imutáveis; a situação final de controles está em CONTROLES.json. Esta entrega é autoral, não aceite final nem atualização de gate.
'''
atomic(ROOT/'FALHAS_E_LIMITES.md',limits)
receipt=dict(timestamp=stamp(),status='ENTREGA_AUTORAL_PARA_REVISAO',exclusive_root=str(ROOT),
    paid=[dict(item='Polar limitado construido dentro de N',status='PAGO_AUTORAL',module=modules[0]),
          dict(item='Reticulado concreto e tauA1',status='PAGO_AUTORAL',module=modules[1]),
          dict(item='Comparacao de projecoes e subaditividade A1',status='PAGO_AUTORAL',module=modules[2]),
          dict(item='SusyRelativeData, consumidor Breuer e identificacoes',status='PAGO_AUTORAL',module=modules[3])],
    proposed_flag=dict(name='gpf_H1_internal_susy_relative_gap_discharged',status='PROPOSTA_SEM_EDICAO',
      scope='Representante limitado D=1-PF,D0=1, no mesmo regularCoreAlgebra P e tauA1; nao H1 fisico.'),
    candidate_sources=[b['review_source'] for b in builds],build_count=len(builds),returncodes=[b['returncode'] for b in builds],
    new_declarations=len(names['names']),audited_suppliers=len(names['suppliers']),all_exact_trio=True,
    semantic_controls=len(controls),negative_returncodes=[x['bad']['returncode'] for x in controls],
    independent_review='PENDENTE',mathematical_blocker_for_declared_scope=None,
    delivery_links={n:pin(ROOT/n) for n in ['FICHA_REAPROVEITAMENTO.md','FICHA_REAPROVEITAMENTO.json','AUDITORIA.json','CONTROLES.json','FALHAS_E_LIMITES.md','REAPROVEITAMENTO_EFETIVO.json','PRESERVACAO_FONTES.json','TENTATIVAS.json']})
record(ROOT/'RECIBO.json',receipt)
md=['# Entrega autoral — A2 SUSY 012','',
 '[REAL] Ponte construída no mesmo regularCoreAlgebra P e traço A1. Quatro módulos rc0 no Lean 4.31.0; 29 declarações novas e cinco fornecedores auditados, todos apenas no trio propext / Classical.choice / Quot.sound. Três mutações recusadas com refutações formais rc0/trio. Revisão independente pendente.','',
 'O polar fornece a comparação de projeções para provar subaditividade de tauA1. O reticulado contém todas as projeções de N, com pertinência e identificação de ordem concretas. regularSusyData usa PF de A2: D=1-PF, D0=1, ker=gapD=diff=PF e gapD0=bottom. regularSusy_gives_breuer aplica diretamente TGLExt.susy_relative_gives_breuer. As identificações de operadores e o gap já pago em A2 acompanham o certificado.','',
 '[OPEN] Proposta gpf_H1_internal_susy_relative_gap_discharged apenas para esse representante matemático. Nenhuma identificação microscópica ou física; nenhuma edição de flag, gate, A2, Atlas ou túnel. O traço total e ThreeLocks permanecem com a bancada principal.','',
 '## Fontes e objetos','', '| Módulo | Fonte SHA256 lido | Objeto SHA256 lido | rc |','|---|---|---|---|']
for b in builds:
    md.append('| '+b['module']+' | '+b['source']['sha256']+' | '+b['objects'][0]['sha256']+' | 0 |')
md += ['', 'Fontes pequenas para revisão em src/TGLExt; fontes compiladas em k/TGLExt. Bytes idênticos verificados. Sondas e auditoria em audit/TGLExt, com cópias compiladas em k/TGLExt. Os recibos de cada tentativa preservam snapshot, comando, saída e objeto.','',
 '## Comandos efetivamente executados','',
 'AUDITORIA.json guarda cada argv completo, cwd e todos os diretórios LEAN_PATH, além do SHA256 do compilador. run_lean.py reproduz a invocação em uma nova tentativa própria; não é necessário repetir os builds para ler esta entrega.','']
fence=chr(96)*3
for b in builds+[audit]+list(probes.values())+[x['bad'] for x in controls]:
    md += ['### '+b['module'],'',fence+'powershell',
      'Set-Location -LiteralPath '+"'"+str(ROOT)+"'",
      'python .\\run_lean.py '+b['module'],fence,'',
      'Resultado observado: rc'+str(b['returncode'])+'. Tentativa: '+b['attempt']+'.',
      'Invocação do Lean registrada: '+json.dumps(b['command'],ensure_ascii=False)+'.','']
md += ['## Recibos e limites','',
 '- RECIBO.json: estatuto, propostas e pins das evidências.',
 '- AUDITORIA.json e AUDIT_NAMES.json: builds e axiomas efetivamente lidos.',
 '- CONTROLES.json: alterações exatas, erros e teoremas que refutam as mutações.',
 '- FICHA_REAPROVEITAMENTO.md/json: ficha anterior ao código; adendos e REAPROVEITAMENTO_EFETIVO.json documentam decisões e consumidores.',
 '- COPIA_A1.json, COPIA_A2.json, REUSO_OBJETOS_A2.json e REUSO_CORE_SUPPORT.json: proveniência da base reutilizada.',
 '- PRESERVACAO_FONTES.json: '+str(len(preservation))+' fontes comparadas ao hash da cópia, todas preservadas.',
 '- TENTATIVAS.json e FALHAS_E_LIMITES.md: erros anteriores, alcance e limites.',
 '- MANIFESTO.json: inventário dos artefatos de revisão; SELOS.json: hashes lidos dos recibos principais.',
 '', 'Os saneamentos b,c,d,f,g,h e B1-prime pertencem às entregas anteriores; não foram reabertos por esta tarefa.']
atomic(ROOT/'ENTREGA.md','\n'.join(md)+'\n')
# Manifest covers all review evidence but delegates the large copied baseline to its manifest.
selected=[]
for current,dirs,files in os.walk(ROOT):
    p=Path(current)
    dirs[:]=[d for d in dirs if not (p==ROOT and d in ['k','tmp','__pycache__']) and d!='__pycache__']
    for f in files:
        q=p/f
        if p==ROOT and (f in ['MANIFESTO.json','SELOS.json','VERIFICACAO_FINAL.json'] or any(f.startswith(n+'.bak_') for n in ['MANIFESTO.json','SELOS.json','VERIFICACAO_FINAL.json'])):
            continue
        selected.append(q)
for p in new_sources:
    selected.append(p)
    selected.extend(p.parent.glob(p.name+'.bak_*'))
    obj=K/'.lake/build/lib/lean/TGLExt'/(p.stem+'.olean')
    selected.extend(obj.parent.glob(obj.name+'*'))
selected=sorted(set(selected))
record(ROOT/'MANIFESTO.json',dict(timestamp=stamp(),algorithm='SHA256',status='ARTEFATOS_AUTORAIS',
    scope='Todos os artefatos de revisao fora de k/tmp/__pycache__, mais novas fontes Lean, seus backups e objetos locais; baseline k delegado aos manifestos de copia/reuso. O proprio manifesto, selos, verificacao e backups desses tres ficam fora para evitar ciclo de hashes.',
    baseline_manifests=[pin(ROOT/n) for n in ['COPIA_A1.json','COPIA_A2.json','REUSO_OBJETOS_A2.json','REUSO_CORE_SUPPORT.json']],
    files=[pin(p) for p in selected]))
record(ROOT/'SELOS.json',dict(timestamp=stamp(),algorithm='SHA256',files=[pin(ROOT/n) for n in
    ['MANIFESTO.json','RECIBO.json','ENTREGA.md','AUDITORIA.json','CONTROLES.json','FICHA_REAPROVEITAMENTO.md','FICHA_REAPROVEITAMENTO.json','FALHAS_E_LIMITES.md']]))
manifest=readj(ROOT/'MANIFESTO.json')
mismatches=[r['path'] for r in manifest['files'] if digest(r['path'])!=r['sha256'] or Path(r['path']).stat().st_size!=r['bytes']]
seal_mismatches=[r['path'] for r in readj(ROOT/'SELOS.json')['files'] if digest(r['path'])!=r['sha256']]
assert not mismatches and not seal_mismatches
record(ROOT/'VERIFICACAO_FINAL.json',dict(timestamp=stamp(),manifest=pin(ROOT/'MANIFESTO.json'),seals=pin(ROOT/'SELOS.json'),
    entries_checked=len(manifest['files']),manifest_mismatches=mismatches,seal_mismatches=seal_mismatches,
    source_review_copies_identical=True,forbidden_source_hits=forbidden,builds_repeated_for_packaging=False))
print(json.dumps(dict(status='FINALIZADO',builds=len(builds),new_names=len(names['names']),suppliers=len(names['suppliers']),
    controls=len(controls),preserved_sources=len(preservation),manifest_entries=len(manifest['files']),attempt_counts=counts,
    main_pins=[pin(ROOT/n) for n in ['RECIBO.json','ENTREGA.md','MANIFESTO.json','AUDITORIA.json','FALHAS_E_LIMITES.md']]),ensure_ascii=False,indent=2))
