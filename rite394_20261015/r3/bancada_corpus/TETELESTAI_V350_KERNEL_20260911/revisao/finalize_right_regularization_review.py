"""Record completed independent DEV review; writes only reviewer artifacts."""
from pathlib import Path
from collections import Counter
import datetime, hashlib, json, re

REV=Path(__file__).resolve().parent
ROOT=REV.parent
RUN=Path((REV/'right_regularization_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json')
D=load(RUN/'right_regularization_draft_status.json')
HS=load(RUN/'helper_static_inspection.json');H=load(RUN/'author_history.json')
P=load(RUN/'gaussian_polar_custody.json')
assert all(v is True for k,v in C.items() if k!='records')
assert len(C['records'])==3 and len(D['targets'])==19
assert not HS['new_findings'] and not D['integrated']

def put(p,raw):
    assert raw and p.resolve().is_relative_to(REV)
    if p.exists():
        before=p.read_bytes()
        backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(before)
        assert backup.read_bytes()==before
        assert raw.startswith(before), 'Existing review must remain an exact prefix'
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw
    temp.replace(p)
    assert p.read_bytes()==raw

author_pins=[]
for rel,s in M['sources'].items():
    assert hf(s['path'])==s['sha256'] and hf(s['snapshot'])==s['sha256']
    assert hf(s['author_log'])==s['author_log_sha256']
    ar=load(s['author_log']); assert ar['returncode']==ar['lean_returncode']==0
    assert ar['source_unchanged_during_compile'] and ar['output_exists']
    assert hf(s['author_binary'])==s['author_binary_sha256']==ar['output_sha256']
    assert hf(ar['stdout'])==s['author_stdout_sha256'] and hf(ar['stderr'])==s['author_stderr_sha256']
    author_pins.append({'module':rel,**s})
for r in C['records']:
    assert r['returncode']==0 and r['exact_targets'] and r['axioms_allowed']
    assert hf(r['command'][3])==r['source_sha256']
    assert hf(r['command'][2])==r['output_sha256']
    assert hf(r['stdout'])==r['stdout_sha256'] and hf(r['stderr'])==r['stderr_sha256']
aud=C['records'][-1]
audit_text=Path(aud['stdout']).read_text(encoding='utf-8')
checked=re.findall(r'^(TGLV350\.Regular\.\w+)\s',audit_text,re.M)
assert len(checked)==19 and set(checked)==set(D['targets'])==set(aud['axioms'])
assert all(set(v)=={'propext','Classical.choice','Quot.sound'} for v in aud['axioms'].values())
assert 'sorryAx' not in audit_text
assert all(hf(p)==pin for p,pin in P['surface_sha256'].items())
assert all(hf(ROOT/n)==pin for n,pin in M['artifact_pins'].items())
assert all(hf(p)==pin for p,pin in M['previous_reviews'].items())
assert hf(ROOT/'um.py')==M['working_sha256'] and hf(ROOT/'gate_extension.py')==M['gate_sha256']
counts=Counter(d['reviewer_origin'] for d in M['dependencies'].values())
assert len(M['dependencies'])==393 and all(Path(p).is_relative_to(REV) for p in counts)
source_lines={}
for rel,s in M['sources'].items():
    source_lines[rel]={}
    for i,line in enumerate(Path(s['snapshot']).read_text(encoding='utf-8').splitlines(),1):
        mat=re.match(r'(?:def|theorem)\s+(\w+)',line)
        if mat:source_lines[rel][mat[1]]=i
v={'timestamp':datetime.datetime.now().astimezone().isoformat(),
   'scope':'RIGHT_REGULARIZATION_DEV_REVIEW__TWO_MODULES_19_TARGETS',
   'result':'NO_P0_P1_P2_WITHIN_REVIEWED_SCOPE',
   'manifest_sha256':hf(RUN/'manifest.json'),'compilation_sha256':hf(RUN/'compilation.json'),
   'draft_sha256':hf(ROOT/'right_regularization_draft_status.json'),
   'report_sha256':hf(ROOT/'RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md'),
   'helper_static_inspection_sha256':hf(RUN/'helper_static_inspection.json'),
   'sources_and_final_author_evidence':author_pins,
   'own_records':C['records'],'checked_types_universes':checked,
   'source_declaration_lines':source_lines,'dependency_origins':dict(counts),
   'dependency_provenance_pins':M['origins'],'project_dependencies_copied_with_byte_pins':393,
   'author_project_build_in_lean_path':False,'external_packages_read_only':True,
   'compiler_sha256':M['compiler_sha256'],'lean_path':M['lean_path'],
   'historical_rc1_attempts':sum(r['returncode']!=0 for r in H),
   'historical_failed_outputs_excluded':True,
   'pre_lean_preparation_limit': 'The Gaussian-only catalog lacked ScalarWeightAction; setup stopped before Lean and was supplemented from the existing independent core_polar tree. Partial snapshot preserved.',
   'parent_custody_sha256':hf(ROOT/'gaussian_polar_custody.json'),
   'parent_memory_surfaces_rehashed_unchanged':34,
   'integration_reviewed':False,'author_helpers_executed_by_reviewer':False,
   'monolith_executed_or_imported':False,'new_findings':[],
   'no_further_DEV_analysis_required_for_this_scope':True}
put(RUN/'verification.json',json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))

def link(path,label,line=None):
    return '['+label+'](<'+Path(path).as_posix()+((':'+str(line)) if line else '')+'>)'
def at(rel,name,label=None):
    return link(ROOT/'kernel'/rel,label or name,source_lines[rel][name])
s1='TGLV350/ScalarRightRegularization.lean';s2='TGLV350/ScalarCommutantRegularization.lean'
lines=[
 '# Revisão DEV — regularização direita do comutante',
 '',
 'RIGHT_REGULARIZATION_DEV_REVIEW',
 '',
 datetime.datetime.now().astimezone().isoformat(timespec='seconds')+'. **[REAL — revisão independente concluída] Nenhum achado P0, P1 ou P2 no escopo de duas fontes/19 alvos e cinco helpers.** Integração e registro de memórias permanecem pendentes.',
 '',
 '**Evidência própria.** Duas recompilações e um auditor com `#check`/`pp.universes` e `#print axioms` dos 19 nomes: todos rc0; somente `propext`, `Classical.choice`, `Quot.sound`. Os dois `.olean` produzidos são byte a byte iguais aos finais autorais. Não houve recompilação de dependências nem execução de scripts autorais, raízes ou monólito.',
 '',
 '| Fonte | Alvos | SHA256 da fonte congelada | Recompilação própria |',
 '|---|---:|---|---|',
]
for r in C['records'][:2]:
    s=M['sources'][r['module']]
    lines.append('| '+link(s['path'],Path(s['path']).name)+' | '+str(len(r['axioms']))+' | `'+s['sha256']+'` | rc0; '+str(r['seconds'])+' s; binário igual |')
lines += [
 '',
 'Auditor próprio: rc0 em '+str(aud['seconds'])+' s. '+link(RUN/'compilation.json','compilation.json')+' (`'+hf(RUN/'compilation.json')+'`); '+link(aud['stdout'],'tipos/universos e axiomas')+' (`'+aud['stdout_sha256']+'`); '+link(RUN/'verification.json','verification.json')+' (`'+hf(RUN/'verification.json')+'`).',
 '',
 '**Proveniência.** '+str(len(M['dependencies']))+' dependências de projeto copiadas com hashes de fonte/binário de árvores próprias anteriores, conforme '+link(RUN/'manifest.json','manifesto independente')+'. `LEAN_PATH` contém somente o build desta revisão e oito caminhos de pacotes externos somente leitura. Lean '+str(M['lean_version'])+'; executável SHA256 `'+M['compiler_sha256']+'`.',
 ]
for origin,n in counts.items():
    pin=M['origins'][origin]
    lines.append('- '+str(n)+' dependências de '+link(Path(origin)/'manifest.json',Path(origin).name)+'; manifesto `'+pin['manifest_sha256']+'`, compilação `'+pin['compilation_sha256']+'`.')
lines += [
 '',
 'O catálogo gaussiano sozinho não incluía `ScalarWeightAction`; a preparação parou antes de iniciar Lean e foi completada pela árvore própria `core_polar`, com pins compatíveis. O snapshot parcial foi preservado. Não se introduziu build de projeto do autor no `LEAN_PATH`.',
 '',
 '**Enunciados e composição conferidos.**',
 '',
 '- '+at(s1,'scalarWeightRightRegularization_norm_le')+': a cota usa o mesmo peso/vetor e o mesmo fator Haar herdados de `ScalarWeightAction`/`ScalarRightAverage`. A passagem por `toReal` ocorre depois de reescrever ambos os lados como `ofReal ‖Λ(a)‖²`; a finitude do majorante é explícita. `extendOfNorm` recebe densidade e cota, não fica apenas como definição total sem suas condições.',
 '- '+at(s1,'scalarRightRegularization_commutes')+' e '+at(s1,'scalarRightRegularization_tendsto')+': associatividade no ideal completo `nν` e igualdade em sua imagem densa dão comutação com toda `π(N)`. A cota 1 e a equicontinuidade estendem a convergência das inscrições a todo o **mesmo** `H_I`. Trata-se de convergência forte em `h→0`, `h≠0`, sem afirmação de convergência na norma de operadores.',
 '- '+at(s1,'scalarRegularizationVector')+' e '+at(s1,'scalarRightRegularization_vector')+': `η_h` é inscrita via o ideal uniforme para `h>0`, depois identificada à inscrição completa. A igualdade é `R_hΛν(a)=π(a)η_h` para todo `a∈nν`; não usa `Λν(1)` nem supõe `I=nν`.',
 '- '+at(s2,'ScalarRightBounded')+' e '+at(s2,'scalarRightBounded_commutant_mem')+': a definição exige somente `∃η, ∀a∈nν, RΛν(a)=π(a)η`. A comutação e a condição do centralizador também para `star a` são demonstradas por densidade/representação estrela. Nenhum vetor adjunto é embutido nessa definição.',
 '- '+at(s2,'scalarCommutantRegularization_rightBounded')+' e '+at(s2,'scalarCommutant_rightBounded_approximation')+': o produto é `T * R_h`, com vetor `Tη_h`, cota `‖T‖` e limite forte `T`; a pertinência right-bounded vale eventualmente em `𝓝[>]0`. A orientação usa `Tπ(a)=π(a)T`; não troca a ordem de `T` e `R_h` nem presume continuidade SOT do adjunto.',
 '- '+at(s2,'scalarCommutant_mem_of_rightBounded')+': `Q : VonNeumannAlgebra H_I` e `hQ : ∀R, ScalarRightBounded P R → R∈Q` continuam **premissas explícitas**. O fechamento WOT herdado recebe o limite forte e a instância `NeBot` de `𝓝[>]0`; não há vacuidade por filtro vazio. '+at(s2,'scalarCommutant_mem_generated_rightBounded')+' descarrega `hQ` apenas na álgebra gerada pelo conjunto de todos esses multiplicadores. Não a identifica com a imagem polar.',
 '',
 '**Manifesto, tentativas e documentação.** Lidos integralmente o manifesto autoral, o relatório DEV e os dois módulos. Os logs finais aceitos são `_214636_263993` e `_215017_718191`; fonte, binário, log, stdout e stderr foram relidos e confrontados com os pins. As quatro tentativas autorais rc1, seus streams e backups de fonte estão preservados em '+link(RUN/'author_history.json','author_history.json')+' e excluídos da evidência positiva; seus prints incompletos ou com `sorryAx` não contam. Manifesto autoral SHA256 `'+hf(ROOT/'right_regularization_draft_status.json')+'`; relatório DEV `'+hf(ROOT/'RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md')+'`.',
 '',
 '**Helpers: somente inspeção estática.** Os cinco foram lidos integralmente e parseados por AST; pins em '+link(RUN/'helper_static_inspection.json','helper_static_inspection.json')+' (`'+hf(RUN/'helper_static_inspection.json')+'`). A projeção textual em memória confirma batch 525→544, somente dois módulos antes das raízes e um grupo de controle novo; preserva a lógica corrente/histórica dos hashes Audit. Recorder/verifier planejam releitura de fontes/binários, mãe gaussiana, 34 backups imediatos de bytes, prefixos preservados e substituição por temporário. `--review-read` e marcadores são precondições documentais, não prova automática de aprovação. Os textos mantêm a premissa `hQ`, a ausência de vetor adjunto/algebra-full e a distinção das seis flags maiores versus entradas do gate legado. Nenhum desses helpers foi executado por esta revisão; a gravação futura não está certificada aqui.',
 '',
 '**Limites.** [REAL — leitura/pins] Mãe `gaussian_polar_custody.json` SHA256 `'+hf(ROOT/'gaussian_polar_custody.json')+'`; cópia `'+M['working_sha256']+'` inalterada, assim como gate, 34 memórias e pareceres gaussianos. As contagens 189/97/6882 pertencem à mãe e não a este DEV. [OPEN] Reconstrução como `Jπ(b)J` com o J original, álgebra direita completa/vetor adjunto, fechamento da imagem `π(N)`, inclusão polar inversa, identificação `Δ^it`/KMS, traço e consumo tipado/gate/runtime. São limites declarados, não defeitos destas provas.',
 '',
 '**Encerramento:** nenhuma análise DEV necessária resta neste pacote 2/19 e nos cinco helpers lidos. A conclusão é delimitada a esses bytes e não aguarda nem antecipa integração futura.',
 '']
report=REV/'REVIEW_RIGHT_REGULARIZATION_DEV.md'
assert not report.exists(), 'Do not overwrite or silently amend an existing review'
put(report,'\n'.join(lines).encode('utf-8'))
print(json.dumps({'report':str(report),'sha256':hf(report),'lines':len(report.read_bytes().splitlines()),
    'findings':[],'own_compilations':3,'targets':19,'verification_sha256':hf(RUN/'verification.json'),
    'dependency_origins':dict(counts)},ensure_ascii=False))
