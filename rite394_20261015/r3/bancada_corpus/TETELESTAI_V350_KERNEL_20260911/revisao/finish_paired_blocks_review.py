from pathlib import Path
import datetime, hashlib, json, os, re

REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=Path((REV/'paired_blocks_latest_run.txt').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def put(p,b,append=False):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    old=b''
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    data=old+b if append else b
    tmp=p.with_name(p.name+'.tmp_'+datetime.datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:f.write(data)
    assert tmp.read_bytes()==data;os.replace(tmp,p)
    assert p.read_bytes()==data and (not append or p.read_bytes().startswith(old))
    return len(old)
def save(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def link(label,p,line=None):
    target=Path(p).as_posix()+(f':{line}' if line else '')
    return f'[{label}](<{target}>)'

m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');history=load(RUN/'author_history.json')
checks=['complete','all_exit_zero','exact_13_targets','all_axioms_allowed','all_axioms_match_author',
        'binary_equal_author','source_snapshot_preserved','readonly_artifacts_preserved',
        'dependencies_preserved','external_direct_pins_preserved']
assert all(c[k] for k in checks),{k:c[k] for k in checks}
assert len(c['records'])==3 and len(m['declarations'])==13
assert all(hf(p)==h for p,h in m['readonly_pins'].items())
for rel,d in m['sources'].items():
    assert hf(d['path'])==hf(d['snapshot'])==d['sha256']
    assert hf(d['author_binary'])==d['author_binary_sha256']
    rr=next(x for x in c['records'] if x['module']==rel)
    assert hf(rr['command'][2])==d['author_binary_sha256']
for row in c['records']:
    assert hf(row['stdout'])==row['stdout_sha256'] and hf(row['stderr'])==row['stderr_sha256']
    assert not Path(row['stderr']).read_bytes()
aud=c['records'][-1];at=Path(aud['stdout']).read_text(encoding='utf-8')
assert not re.search(r'\b(?:sorryAx|error:|failed|unknown constant)\b',at)
for name in m['declarations']:assert name in at
failed=[x for x in history if x['returncode']!=0];assert len(failed)==3
timestamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
stat={'timestamp':timestamp,'scope':'PARTIAL_DEV_2_MODULES_13_TARGETS','findings':[],
 'complete_for_two_frozen_modules':True,'later_modules_reviewed':False,'integrated_review':False,
 'files_read_in_full':list(m['sources']),
 'semantic_checks':[
  'Original H_I, right-pair algebra E and j; eta belongs to original D(S), S eta=eta only in the two symmetry/rotation statements.',
  'Core pairing follows from original F=S-adjoint and bidual graph characterization; no new abstract pairing hypothesis survives the concrete application.',
  'Graph invariant for a and star a; diagonal reduction yields commuting orthogonal projection; correct rotated vector (a eta,-j a).',
  'Block A and D are selfadjoint; positivity of A and 1-A uses the actual complex CLM order, including selfadjointness.',
  'Products B B* = A(1-A) and B D = (1-A)B follow from idempotence without assuming A B = B A.',
  'Injectivity requires DenseRange e and the actual closed complex graph; does not give a uniform positive lower bound.',
  'Generic Hilbert variables use Type (universe zero); no arbitrary-universe generalization claimed.'
 ],'private_items':{},'evidence_checks':{k:c[k] for k in checks},
 'manifest_sha256':hf(RUN/'manifest.json'),'compilation_sha256':hf(RUN/'compilation.json'),
 'author_failures_excluded':failed,'parent_custody_sha256':m['parent_custody_sha256']}
for rel,d in m['sources'].items():
    txt=Path(d['snapshot']).read_text(encoding='utf-8')
    stat['private_items'][rel]=re.findall(r'^private (?:theorem|def|instance) (\w+)',txt,re.M)
save(RUN/'semantic_inspection.json',stat)
failed_run=REV/'paired_graph_independent_20260913_063723_299120'
if failed_run.exists():
    save(failed_run/'preparation_failure.json',{
     'recorded_at':timestamp,'kind':'reviewer_preparation_failure_before_Lean',
     'observed_error':'AssertionError: TGLV350.DualSemifiniteIdeal; historical comment-erratum flag absent from inherited dependency entry',
     'Lean_started':False,'resolution':'Exact old/new comment byte replacement verified in the later run; inherited own source/binary retained.',
     'successful_run':str(RUN),'is_raw_process_stream':False})
dep=m['dependencies']['TGLV350.DualSemifiniteIdeal']
assert dep['exact_literal_replacement_verified']
save(RUN/'inherited_comment_erratum.json',{
 'module':'TGLV350.DualSemifiniteIdeal','old_source_sha256':dep['source_sha256'],
 'live_source_sha256':dep['live_source_sha256'],'own_binary_sha256':dep['sha256'],
 'old_comment':dep['frozen_old_comment'],'new_comment':dep['live_corrected_comment'],
 'exact_literal_replacement_verified':True,'no_recompile_of_dependency':True})

lines=[f'PAIRED_BLOCKS_DEV_REVIEW — estrato parcial DEV13 — {timestamp}',
 '', '[REAL] Revisão encerrada para as duas fontes congeladas e seus 13 alvos (5+8). **Nenhum achado P0–P2** no escopo examinado. Leitura integral, recompilação própria de ambos os módulos e auditor separado concluídos; isto não é aceite integrado nem conclusão do terceiro módulo em autoria.',
 '', 'A árvore e os resultados completos estão em '+link('manifest.json',RUN/'manifest.json')+', '+link('compilation.json',RUN/'compilation.json')+' e '+link('semantic_inspection.json',RUN/'semantic_inspection.json')+'. Os nomes, tipos com `pp.universes` e axiomas dos 13 alvos estão no '+link('stdout do auditor próprio',aud['stdout'])+'.',
 '', '| Recompilação própria | Alvos | rc | Tempo | .olean versus autor |',
 '|---|---:|---:|---:|---|']
for row in c['records']:
    name=Path(row['module']).name
    lines.append(f"| {name} | {len(row['axioms'])} | {row['returncode']} | {row['seconds']} s | "+('bytes idênticos' if row.get('binary_equals_author') else 'auditor próprio')+' |')
lines += ['', 'Todos os alvos impressos coincidem exatamente com os conjuntos 5+8 das fontes e com os mapas dos logs autorais finais. A auditoria transitiva usa somente `propext`, `Classical.choice` e `Quot.sound`; os auxiliares privados estão incluídos pela dependência dos teoremas. Não há `sorry`, `axiom`, `unsafe` nem alteração de redutibilidade nas novas fontes aceitas.',
 '', 'Conferência matemática:',
 '', '- '+link('ScalarPairedMultiplicationGraph.lean',ROOT/'kernel/TGLV350/ScalarPairedMultiplicationGraph.lean',103)+': o pareamento é obtido da bidualidade do S original, com η∈D(S) e Sη=η. A identificação F j(a)=j(a*) e a lei j(ab)=a j(b) são efetivamente aplicadas; não ficam como premissas abstratas residuais. A orientação dos dois produtos internos é correta.',
 '- '+link('Invariância e projeção',ROOT/'kernel/TGLV350/ScalarPairedMultiplicationGraph.lean',116)+': a ação diagonal preserva o fecho para a e a*, logo comuta com sua projeção ortogonal. Estes três enunciados valem para η arbitrário. A anulação da projeção em (aη,−j(a)) volta a exigir η fixo pelo mesmo S. E, j, H_I e a realização não são trocados.',
 '- '+link('HilbertProjectionOrder.lean',ROOT/'kernel/TGLV350/HilbertProjectionOrder.lean',14)+': A=A* e D=D* são os blocos de Π. A identidade Re⟨v,Av⟩=‖Π(v,0)‖² e Pitágoras provam 0≤A≤I na ordem complexa usual de operadores positivos, incluindo auto-adjunticidade. A aqui é um bloco limitado de Π, não Δ=S†S.',
 '- '+link('Identidades de produtos',ROOT/'kernel/TGLV350/HilbertProjectionOrder.lean',127)+': Π²=Π dá BB*=A(I−A) e BD=(I−A)B nessa ordem; não há permutação indevida de fatores nem hipótese [A,B]=0.',
 '- '+link('Injetividade',ROOT/'kernel/TGLV350/HilbertProjectionOrder.lean',154)+': `DenseRange e` força Π(v,0)≠0 para v≠0, e a energia de A elimina seu núcleo. Não exige continuidade de f, domínio total de um operador não limitado ou cota inferior uniforme. É um lema genérico para o fecho de range(e,f); a especialização adicional em autoria não faz parte destes 13 alvos.',
 '', 'Proveniência e pins lidos:', '']
for rel,d in m['sources'].items():
    lines += [f'- `{Path(rel).name}`:',f"  fonte `{d['sha256']}`; .olean autor/próprio `{d['author_binary_sha256']}`.",
              f"  Log final `{Path(d['author_log']).name}`; SHA `{d['author_log_sha256']}`; stdout `{d['author_stdout_sha256']}`."]
lines += ['', f"A mãe é `square_resolvent_custody.json`, SHA `{m['parent_custody_sha256']}`. Seus 34 pins de superfícies, os pareceres pinados, a cópia e `gate_extension.py` foram relidos e permaneceram iguais; não se refez a auditoria integrada da mãe.",
 '', f"Lean 4.31.0, executável SHA `{m['compiler_sha256']}`. As {len(m['dependencies'])} dependências de projeto foram copiadas da árvore própria `{Path(m['own_origin_runs'][0]).name}`, após releitura de seus pins, sem build autoral de projeto no `LEAN_PATH`. Apenas os dois módulos novos e o auditor foram compilados. Os oito caminhos de pacotes externos ficaram readonly; {len(m['external_direct_pins'])} pares externos diretos têm hashes relidos no manifesto. A biblioteca e as dependências antigas não foram reconstruídas nesta rodada.",
 '', 'A primeira preparação própria parou **antes de Lean**, porque o manifesto herdado não carregava o rótulo da antiga errata documental de `DualSemifiniteIdeal`. A comparação literal confirmou apenas aquele comentário; foram mantidos o fonte e o binário próprios antigos, correspondentes entre si. '+link('Evidência da errata herdada',RUN/'inherited_comment_erratum.json')+'. Não se tratou de falha matemática nem de nova recompilação dessa dependência.',
 '', 'Histórico autoral excluído: `ScalarPairedMultiplicationGraph_20260913_062819_485761` (rc1) e `HilbertProjectionOrder_20260913_063011_096580` / `_063255_938405` (rc1). Os streams e logs foram preservados em '+link('author_history.json',RUN/'author_history.json')+'. Impressões parciais verdes, `sorryAx` ou ausência aparente de axiomas nesses arquivos recusados não foram usadas como evidência. As versões finais e próprias passaram com `maxHeartbeats 200000`.',
 '', '[OPEN] Estes resultados não demonstram A≥cI com c>0, inversibilidade limitada de A, as futuras estimativas concretas dos blocos, inclusão inversa de comutantes, KMS ou traço. O parâmetro `S` do módulo genérico de ordem é um subespaço fechado de H×H, distinto do Tomita original empregado no primeiro módulo. A genericidade impressa é sobre `H E : Type`; não se reivindica ampliação de universos além dos tipos efetivos.',
 '', '[REAL] Escopo parcial13 completo, sem pendência de análise necessária destes dois módulos. Nenhuma integração, monólito, helper autoral ou recorder foi executado; nenhuma memória, fonte autoral, original ou parecer custodiado foi alterado. Não houve promoção de gate ou das seis flags. Ampliação futura exige fontes finais e pedido próprio.', '']
report=REV/'REVIEW_PAIRED_BLOCKS_DEV.md'
prefix=put(report,('\n\n'.join([])+'\n'.join(lines)).encode('utf-8'),append=report.exists())
save(RUN/'report_pin.json',{'report':str(report),'sha256':hf(report),'bytes':report.stat().st_size,
 'preserved_prefix_bytes':prefix,'timestamp':timestamp,'scope':'PARTIAL_DEV13','marker':'PAIRED_BLOCKS_DEV_REVIEW'})
print(json.dumps({'report':str(report),'sha256':hf(report),'bytes':report.stat().st_size,'findings':[],'scope':'PARTIAL_DEV13'}))
