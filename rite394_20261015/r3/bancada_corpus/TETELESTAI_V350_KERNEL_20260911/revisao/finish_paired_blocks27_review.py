from pathlib import Path
from collections import Counter
import ast,datetime,hashlib,json,os,re
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'paired_blocks27_latest_run.txt').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def put(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+datetime.datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def link(label,p,line=None):return f'[{label}](<{Path(p).as_posix()}'+(f':{line}' if line else '')+'>)'
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');draft=load(m['draft_path'])
keys=['complete','all_exit_zero','exact_27_targets','all_axioms_allowed','all_axioms_match_author','new_binary_equal_author',
 'source_snapshot_preserved','readonly_artifacts_preserved','dependencies_preserved','external_direct_pins_preserved']
assert all(c[k] for k in keys) and len(c['records'])==2
assert all(hf(p)==h for p,h in m['readonly_pins'].items())
assert hf(m['draft_path'])==m['draft_sha256'] and len(draft['modules'])==4 and len(draft['targets'])==27
rel,d=next(iter(m['sources'].items()));r0,ra=c['records']
assert hf(d['path'])==hf(d['snapshot'])==d['sha256'] and hf(d['author_binary'])==hf(r0['command'][2])==d['author_binary_sha256']
for r in c['records']:
    assert hf(r['stdout'])==r['stdout_sha256'] and hf(r['stderr'])==r['stderr_sha256'] and not Path(r['stderr']).read_bytes()
assert ra['axioms']==draft['targets'] and len(ra['axioms'])==27 and len(r0['axioms'])==2
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
own_module_records=[]
for rr in [Path(m['previous_own_run']),Path(load(Path(m['previous_own_run'])/'manifest.json')['previous_own_run']),RUN]:
    cc=load(rr/'compilation.json')
    assert cc['complete'] and cc['all_exit_zero']
    own_module_records += [x for x in cc['records'] if x['module'].startswith('TGLV350/')]
assert len(own_module_records)==4
for name,md in draft['modules'].items():
    row=next(x for x in own_module_records if x['module']==f'TGLV350/{name}.lean')
    assert hf(row['command'][3])==md['source_sha256'] and hf(row['command'][2])==md['binary_sha256']
    assert hf(ROOT/'kernel/TGLV350'/(name+'.lean'))==md['source_sha256']
    assert hf(ROOT/'build/TGLV350'/(name+'.olean'))==md['binary_sha256']
sem={
 'same_objects':'eta belongs to original D(S), S eta=eta; same E,j,H_I and M=scalarGNSVonNeumann; no replacement of S/F/J.',
 'weighted_pair':'e in M, e*=e, eA=Ae are explicit; K=e(1-A)B, Y=eBB*, Z=B*eB. K j(a)=a Y eta and K* j(a)=a Z eta are proved for all a in E.',
 'domain':'scalarClosedTomita_of_boundedPairAction supplies Y eta in D(S) and S(Y eta)=Z eta, before the variational equation is applied.',
 'adjoint':'K*=B* e (1-A), using eA=Ae; no eB=Be or AB=BA.',
 'variational':'Re z>0 and x in D(F), F x=x; eta is exactly scalarPhaseVariational P z hz x. equationOfGraphPair only substitutes the established graph pair.',
 'equation':'2< x,Z eta > = z< eta,Z eta > + conjugate(z)< Y eta,eta >, complex inner-product convention preserved.',
 'limitations':'No positivity of e required for the graph theorem, and no positivity of Y/Z asserted here. No uniform positive lower bound for A, inverse inclusion, KMS or trace.'}
save(RUN/'semantic_inspection.json',{'timestamp':stamp,'scope':'FINAL_DEV27','findings':[],
 'source_read_in_full':d['path'],'checks':sem,'private_helpers_transitive':re.findall(r'^private theorem (\w+)',Path(d['snapshot']).read_text(encoding='utf-8'),re.M),
 'all_27_types_axioms':ra['stdout'],'four_own_module_records':own_module_records})
helpers={}
for p,h in m['document_pins'].items():
    assert hf(p)==h
    if p.endswith('.py'):
        tree=ast.parse(Path(p).read_bytes());helpers[Path(p).name]={'sha256':h,'ast_parse_ok':True,'executed_by_reviewer':False,
          'functions':[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]}
assert len(helpers)==4
save(RUN/'helper_static_inspection.json',{'timestamp':stamp,'findings':[], 'helpers':helpers,'document_pins':m['document_pins'],
 'review_mode':'full source read and static inspection only; no execution',
 'checks':{
  'draft':'4 named modules, 27 targets, current final log/source/binary pins and parent working hash; no memory writes.',
  'prepare':'--review-read, review marker and all four source/binary hashes required, parent artifact/surface pins, 749 to 776 targets; 4 import-list additions and one 7-declaration frontier group.',
  'recorder':'Requires DEV and integrated reviews, current build/test pins, normalized import transposition, raw current Audit SHA with historical metadata separate, six false flags and 34 parent surfaces.',
  'backup':'Immediate rb/wb-equivalent byte backups via read_bytes/open(xb), prefix assertion, temporary-file verification and replace per file; not an atomic transaction across all 34 files.',
  'verifier':'Rereads source/binary hashes and rc0/output_exists for all integrated records; checks parent/memory prefix/backups and custody artifacts.',
  'future_guide':'PROXIMA_ETAPA_COTA_BLOCOS and its pin JSON are OPEN/DERIVED, no new Lean targets. Re z=1 is explicitly required for the proposed future constant 1+m².',
  'execution_boundary':'Prepared scripts are not evidence of integration or completed custody; no new recorder/verifier/monolith execution performed by reviewer.'}})
for fr in sorted(REV.glob('paired_blocks27_independent_*')):
    if fr==RUN or (fr/'compilation.json').exists():continue
    save(fr/'preparation_failure.json',{'recorded_at':stamp,'before_Lean':True,
      'cause':'Previous narrow own dependency catalog omitted ScalarPhaseVariational or its separately inherited RealPhaseVariational.',
      'resolution':'Read and hash-checked both previous own phase-variational reviews; copied only missing pinned dependencies, no author build and no library recompile.',
      'successful_run':str(RUN),'is_raw_process_error_stream':False})
report=REV/'REVIEW_PAIRED_BLOCKS_DEV.md';prefix=report.read_bytes();assert sha(prefix)==m['previous_report_sha256']
lines=['','',f'PAIRED_BLOCKS_DEV_REVIEW — adendo FINAL DEV27 (4 módulos; 5+8+12+2) — {stamp}',
 '', '[REAL] **Revisão DEV27 concluída, sem achados P0–P2.** Os estratos13 e25 acima são preservados por backup imediato de bytes e append. Leitura integral das quatro fontes finais, hipóteses, manifesto, relatório e quatro helpers concluída. As quatro recompilações próprias foram feitas uma vez por módulo; esta última execução acrescenta apenas o módulo4 e o auditor27.',
 '', '| Módulo recompilado independentemente | Alvos | rc | Tempo |', '|---|---:|---:|---:|']
for name in draft['modules']:
    row=next(x for x in own_module_records if x['module']==f'TGLV350/{name}.lean')
    lines.append(f"| {name} | {len(row['axioms'])} | {row['returncode']} | {row['seconds']} s |")
lines += [f"| Auditor cumulativo27 | 27 | {ra['returncode']} | {ra['seconds']} s |",'',
 'Todos os quatro binários próprios coincidem byte a byte com os autorais. O auditor final imprime os 27 tipos com universos e os axiomas transitivos exatos: somente `propext`, `Classical.choice`, `Quot.sound`. Fontes/binários/streams foram preservados. Evidências finais: '+link('manifest.json',RUN/'manifest.json')+', '+link('compilation.json',RUN/'compilation.json')+', '+link('auditor27',ra['stdout'])+' e '+link('inspeção semântica',RUN/'semantic_inspection.json')+'.',
 '', 'Conferência adicional do módulo4:', '',
 '- '+link('scalarPairedProjection_weighted_graph',ROOT/'kernel'/rel,47)+': as hipóteses são η∈D(S), Sη=η, e∈M, e*=e e eA=Ae, para o S original e os mesmos blocos. K=e(I−A)B é um operador limitado construído. As duas ações Kj(a)=aYη e K*j(a)=aZη são provadas usando os blocos e Y,Z∈M=E′, com Y=eBB* e Z=B*eB. O lema anterior de teste fornece a pertinência real Yη∈D(S) e S(Yη)=Zη; essa pertinência não é uma premissa escondida.',
 '- '+link('Adjunto e ações',ROOT/'kernel'/rel,13)+': K*=B*e(I−A) usa precisamente eA=Ae. Não se move e através de B nem se assume AB=BA. As igualdades usam B j(a)=A(aη) e B(aη)=(I−A)j(a) na orientação necessária. e não precisa ser positivo para este resultado; não se deduz positividade de Y/Z só de e*=e.',
 '- '+link('Equação variacional',ROOT/'kernel'/rel,93)+': Re z>0, ξ∈D(F), Fξ=ξ e η é exatamente a solução `scalarPhaseVariational`. O helper `equationOfGraphPair` substitui o par já pertencente ao grafo na identidade válida para todo u∈D(S): 2⟨ξ,Zη⟩=z⟨η,Zη⟩+conj(z)⟨Yη,η⟩. Mantêm-se o fator2, a conjugação e a ordem dos produtos internos. Não há hipótese nova sobre P nem troca por um S/J auxiliar.',
 '', 'Pins finais cumulativos, lidos dos arquivos e confrontados às quatro reproduções:', '']
for name,md in draft['modules'].items():
    lines += [f"- `{name}`: fonte `{md['source_sha256']}`; binário `{md['binary_sha256']}`."]
lines += [f"- Manifesto DEV `{m['draft_sha256']}`; relatório DEV `{draft['report_sha256']}`.",
 f"- Log final do módulo4 `{Path(d['author_log']).name}`, SHA `{d['author_log_sha256']}`; stdout `{d['author_stdout_sha256']}`.",
 '', 'Proveniência: a última árvore contém '+str(len(m['dependencies']))+' dependências de projeto com pins de fonte/binário, copiadas das revisões próprias anteriores. Reutiliza DEV25 e as árvores `phase_variational_final_independent_20260913_034807_811147` / `phase_variational_independent_20260913_033307_003262` para a seleção concreta e a genérica. Estas duas dependências não faziam parte do recorte DEV25; as preparações que as detectaram ausentes pararam antes de Lean e foram preservadas. Nenhuma biblioteca ou módulo antigo foi recompilado; nenhum build autoral de projeto entrou no `LEAN_PATH`. Limitação herdada de pacotes externos readonly e a errata histórica de comentário permanecem explicitadas nos manifestos.',
 '', 'Histórico rejeitado: sete rc1 autorais no pacote (1+2+2+2), todos preservados e excluídos. No módulo4, `_065520_837842` falhou por campo `star_mem` inexistente e elaboração; `_065724_257592` por timeout. Seus prints vazios/sem axiomas após rc1 não foram aceitos. A versão final usa `toStarSubalgebra.star_mem\'` e `equationOfGraphPair`, mantendo os limites200000. Os cinco auxiliares privados deste módulo entram na auditoria transitiva.',
 '', 'Também se preservou e excluiu um rc1 do auditor próprio27: o arquivo de auditoria importava equivocadamente apenas o módulo3, portanto não encontrava os dois nomes do módulo4. A correção alterou somente o import em um novo auditor (`PairedBlocksAudit27Final`); o módulo4, já rc0, não foi recompilado. `compilation.json` conserva a tentativa recusada em `excluded_own_auditor_attempts` e seu estado anterior em backup.',
 '', 'Helpers e documentação: '+link('helper_static_inspection.json',RUN/'helper_static_inspection.json')+' contém os hashes e o exame dos quatro scripts inteiros. O preparador exige leitura declarada, marcador e os quatro pares de pins; planeja batch749→776 e um grupo de controle de fronteira. Recorder/verifier exigem a futura evidência integrada, distinguem Audit atual/histórico e verificam bytes/prefixos das34 superfícies. As trocas são atômicas por arquivo, não uma transação global. Esta inspeção não afirma execução desses helpers nem custódia nova.', '']
for p,h in m['document_pins'].items():
    if p.endswith('.py'):lines.append(f"- `{Path(p).name}`: `{h}`.")
lines += ['', 'O roteiro '+link('PROXIMA_ETAPA_COTA_BLOCOS.md',ROOT/'PROXIMA_ETAPA_COTA_BLOCOS.md')+' foi lido somente como proposta OPEN/DERIVED; não soma alvos nem constitui prova da estimativa futura. Ele distingue Re z>0 no DEV de Re z=1 para a constante sugerida c=1+m² e não presume eB=Be. A futura aplicação de CFC/pertença de e/estimativa ainda exige seus próprios termos Lean.',
 '', 'Durante a compilação, somente os dois arquivos do roteiro OPEN receberam adendos autorais, inclusive a alternativa por norma de diferença. As versões anteriores foram preservadas e os pins documentais atualizados em '+link('document_refreshes.json',RUN/'document_refreshes.json')+'. Isso não modificou as quatro fontes, helpers ou manifesto DEV, nem motivou nova recompilação matemática. As novas propostas não foram certificadas como Lean.',
 '', '[OPEN] Cota inferior positiva uniforme de A, inverso limitado, inclusão inversa pelo J original, identificação Δ^it/KMS, traço e consumo por certificados/runtime não são resultados deste pacote. [REAL] O DEV27 está encerrado sem análise necessária pendente. A integração e as novas memórias/custódias não foram executadas ou certificadas aqui; mãe Square20, cópia, gate e34 superfícies pré-registro permaneceram nos pins. Nenhuma fonte autoral, original ou parecer custodiado foi alterado.', '']
body='\n'.join(lines).encode();bak=report.with_name(report.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with bak.open('xb') as f:f.write(prefix)
assert bak.read_bytes()==prefix
tmp=report.with_name(report.name+'.tmp_'+datetime.datetime.now().strftime('%H%M%S_%f'))
with tmp.open('xb') as f:f.write(prefix+body)
assert tmp.read_bytes()==prefix+body;os.replace(tmp,report)
assert report.read_bytes().startswith(prefix) and report.stat().st_size==len(prefix)+len(body)
save(RUN/'report_pin.json',{'report':str(report),'sha256':hf(report),'bytes':report.stat().st_size,
 'preserved_prefix_bytes':len(prefix),'preserved_prefix_sha256':sha(prefix),'backup':str(bak),'backup_sha256':hf(bak),
 'timestamp':stamp,'scope':'FINAL_DEV27','marker':'PAIRED_BLOCKS_DEV_REVIEW','findings':[]})
print(json.dumps({'report':str(report),'sha256':hf(report),'bytes':report.stat().st_size,'preserved_prefix_bytes':len(prefix),'scope':'FINAL_DEV27','findings':[]}))
