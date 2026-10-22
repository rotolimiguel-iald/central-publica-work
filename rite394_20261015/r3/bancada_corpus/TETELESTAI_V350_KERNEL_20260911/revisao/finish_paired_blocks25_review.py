from pathlib import Path
from collections import Counter
import datetime,hashlib,json,os,re
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'paired_blocks25_latest_run.txt').read_text())
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
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');hist=load(RUN/'author_history.json')
keys=['complete','all_exit_zero','exact_25_targets','all_axioms_allowed','all_axioms_match_author','new_binary_equal_author',
 'source_snapshot_preserved','readonly_artifacts_preserved','dependencies_preserved','external_direct_pins_preserved']
assert all(c[k] for k in keys) and len(c['records'])==2
assert all(hf(p)==h for p,h in m['readonly_pins'].items())
rel,d=next(iter(m['sources'].items()));r0,ra=c['records']
assert hf(d['path'])==hf(d['snapshot'])==d['sha256'] and hf(d['author_binary'])==hf(r0['command'][2])==d['author_binary_sha256']
for r in c['records']:
    assert hf(r['stdout'])==r['stdout_sha256'] and hf(r['stderr'])==r['stderr_sha256']
    assert not Path(r['stderr']).read_bytes()
at=Path(ra['stdout']).read_text(encoding='utf-8')
assert all(n in at for n in m['declarations']) and 'sorryAx' not in at
assert len(ra['axioms'])==25 and len(r0['axioms'])==12
origins=dict(Counter(v['immediate_own_origin'] for v in m['dependencies'].values()))
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
source=Path(d['snapshot']).read_text(encoding='utf-8')
priv=re.findall(r'^private theorem (\w+)',source,re.M)
assert len(priv)==5
checks={
 'centralizer_of_generated_algebra':'E is star-stable; double StarSubalgebra.centralizer is converted to ordinary centralizers and the triple-centralizer identity.',
 'range_hypothesis_discharged':'centralizerOfRange.hr is discharged by scalarGNSVonNeumann_coe P, for the same representation image.',
 'noncircularity':'Uses prior generated(E)=scalarGNSCommutant and actual-image VNA; does not assume inverse modular-conjugation inclusion.',
 'block_membership':'A,B,D commute with all E by diagonal projection commutation; E-centralizer is the same scalarGNSVonNeumann.',
 'positive_injective':'0<=A<=I and injectivity specialize the old generic results; DenseRange j is supplied by scalarRightPairVector_denseRange.',
 'products':'BB*=A(1-A), BD=(1-A)B; no AB=BA hypothesis.',
 'actions':'Bj(a)=A(a eta) and B*(a eta)=Dj(a) require eta in original D(S), S eta=eta; B(a eta)=(1-A)j(a) permits arbitrary eta.',
 'scope':'PARTIAL_DEV25: no acceptance of ScalarWeightedProjectionTest or integration.'}
save(RUN/'semantic_inspection.json',{'timestamp':stamp,'findings':[],'source_read_in_full':d['path'],
 'semantic_checks':checks,'private_helpers_transitive':priv,'own_dependency_origins':origins,
 'checks':{k:c[k] for k in keys},'new_declarations':m['new_declarations'],'all_25_declarations':m['declarations'],
 'author_history_excluded':[x for x in hist if x['returncode']!=0]})
failed=REV/'paired_blocks25_independent_20260913_065730_606754'
save(failed/'preparation_failure.json',{'recorded_at':stamp,'kind':'preparation_before_Lean',
 'observed_error':'AssertionError: TGLV350.ScalarGNSVonNeumann absent from narrower DEV13 dependency catalog',
 'Lean_started':False,'resolution':'Added only missing entries from own scalar_vna_final_independent_20260913_010417_138014 after hash checks; no author binary and no old-module recompilation.',
 'subsequent_successful_run':str(RUN),'raw_error_stream':False})
report=REV/'REVIEW_PAIRED_BLOCKS_DEV.md';prefix=report.read_bytes()
assert sha(prefix)==m['previous_report_sha256']
lines=['','',f'PAIRED_BLOCKS_DEV_REVIEW — adendo parcial DEV25 (13+12) — {stamp}',
 '', '[REAL] Escopo ampliado para os três módulos/25 alvos. **Nenhum achado P0–P2**. O estrato DEV13 acima fica preservado integralmente; nesta ampliação foram recompilados somente `ScalarPairedProjectionBlocks.lean` e o auditor cumulativo25. O módulo4 permanece sem aceite.',
 '', '| Execução própria nova | Alvos | rc | Tempo |', '|---|---:|---:|---:|',
 f"| ScalarPairedProjectionBlocks.lean | 12 | {r0['returncode']} | {r0['seconds']} s |",
 f"| PairedBlocksAudit25.lean | 25 | {ra['returncode']} | {ra['seconds']} s |",'',
 'O novo `.olean` coincide byte a byte com o autoral. Os 25 `#check` com universos e os 25 `#print axioms` passaram, com conjuntos exatos e somente `propext`, `Classical.choice`, `Quot.sound`. Os cinco auxiliares privados são cobertos transitivamente. Evidências: '+link('manifesto próprio',RUN/'manifest.json')+', '+link('compilation.json',RUN/'compilation.json')+', '+link('tipos/axiomas do auditor25',ra['stdout'])+' e '+link('inspeção semântica',RUN/'semantic_inspection.json')+'.',
 '', 'Conferência do módulo3:', '',
 '- '+link('Centralizadores',ROOT/'kernel'/rel,14)+': a estabilidade por estrela de E legitima a conversão entre centralizador-* e centralizador ordinário. A geração de E dá o comutante da representação; o duplo centralizador da imagem já provada VNA retorna a própria imagem. `centralizerOfRange` recebe a igualdade de conjuntos de `scalarGNSVonNeumann_coe P`, efetivamente descarregada na '+link('aplicação concreta',ROOT/'kernel'/rel,30)+'. Não há premissa residual `hr`, fechamento presumido de π(N), nem uso da inclusão inversa com J.',
 '- '+link('Pertença dos blocos',ROOT/'kernel'/rel,53)+': A, B e D pertencem à mesma `scalarGNSVonNeumann P` porque comutam com todos os operadores de E. Isto vale para η arbitrário e reutiliza a redução diagonal do grafo. Não troca a representação por sua realização auxiliar gaussiana.',
 '- '+link('Ordem e injetividade',ROOT/'kernel'/rel,71)+': 0≤A≤I e injetividade são especializações dos lemas genéricos revisados; `scalarRightPairVector_denseRange P` fornece a hipótese de densidade. Não se infere A≥cI, c>0.',
 '- '+link('Produtos e ações',ROOT/'kernel'/rel,88)+': BB*=A(I−A), BD=(I−A)B; para η∈D(S), Sη=η, obtêm-se Bj(a)=A(aη) e B*(aη)=Dj(a). Já B(aη)=(I−A)j(a) usa apenas o par fixado pela projeção e vale para η arbitrário. As posições de B/B*, a rotação (aη,−j(a)) e a ordem dos fatores estão corretas; nenhum [A,B]=0 é pressuposto.',
 '', 'Pins medidos do novo módulo:', '',
 f"- Fonte `{d['sha256']}`; binário autoral/próprio `{d['author_binary_sha256']}`.",
 f"- Log `{Path(d['author_log']).name}`, SHA `{d['author_log_sha256']}`; stdout `{d['author_stdout_sha256']}`.",
 f"- Manifesto próprio `{hf(RUN/'manifest.json')}`; compilation.json `{hf(RUN/'compilation.json')}`.",
 '', f"Foram reutilizadas {len(m['dependencies'])} dependências de projeto com pins de fonte/binário relidos. Origem imediata: "+'; '.join(f"{v} de `{Path(k).name}`" for k,v in origins.items())+'. Nenhum build autoral no `LEAN_PATH`; os pacotes externos continuam readonly. A tentativa inicial de preparação parou antes de Lean por ausência de `ScalarGNSVonNeumann` no recorte DEV13; a árvore própria anterior de VNA supriu a dependência e sua cadeia já conferida. Não houve recompilação das dependências antigas. A errata histórica exclusivamente de comentário em `DualSemifiniteIdeal` permanece explicitada nos pins herdados.',
 '', 'Dois rc1 autorais foram relidos e integralmente excluídos: `_20260913_064038_773544` (coerções/timeout/cascata) e `_20260913_064256_464387` (timeout de elaboração do centralizador). Os prints com `sorryAx` dessas tentativas não são evidência. O final `_065106_761132` e a reprodução própria passaram com limites originais 200000. '+link('Histórico preservado',RUN/'author_history.json')+'.',
 '', '[REAL] Pai `square_resolvent_custody.json` e 34 superfícies pré-registro, cópia e gate permaneceram iguais aos pins. Nenhuma memória, fonte autoral, monólito, integração ou parecer custodiado foi escrito/executado. Este adendo é exclusivamente DEV25: não inclui compilação/aceite de `ScalarWeightedProjectionTest`, a equação variacional ponderada futura, integração, cota inferior positiva, inversa JMJ, KMS ou traço. Nenhuma análise necessária destes 25 alvos resta pendente.', '']
body='\n'.join(lines).encode();bak=report.with_name(report.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with bak.open('xb') as f:f.write(prefix)
assert bak.read_bytes()==prefix
tmp=report.with_name(report.name+'.tmp_'+datetime.datetime.now().strftime('%H%M%S_%f'))
with tmp.open('xb') as f:f.write(prefix+body)
assert tmp.read_bytes()==prefix+body;os.replace(tmp,report)
assert report.read_bytes().startswith(prefix) and report.stat().st_size==len(prefix)+len(body)
save(RUN/'report_pin.json',{'report':str(report),'sha256':hf(report),'bytes':report.stat().st_size,
 'preserved_prefix_bytes':len(prefix),'preserved_prefix_sha256':sha(prefix),'backup':str(bak),'backup_sha256':hf(bak),
 'timestamp':stamp,'scope':'PARTIAL_DEV25','marker':'PAIRED_BLOCKS_DEV_REVIEW'})
print(json.dumps({'report':str(report),'sha256':hf(report),'preserved_prefix_bytes':len(prefix),'backup':str(bak),'scope':'PARTIAL_DEV25','findings':[]}))
