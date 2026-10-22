"""Append the completed DEV scope; preserve the previous report byte for byte."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'tomita_square_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
V=load(RUN/'verification_dev.json');M=load(RUN/'manifest.json');C=load(RUN/'compilation.json')
runs=[Path(p) for p in V['runs']]
assert V['status']=='DEV_COMPLETE_NO_P0_P1_P2' and not V['necessary_DEV_analysis_remaining']
assert sha((ROOT/'tomita_square_draft_status.json').read_bytes())==V['draft_status_sha256']
assert sha((ROOT/'RELATORIO_ADJUNTO_QUADRADO_DEV.md').read_bytes())==V['author_report_sha256']
for s in V['sources'].values():assert sha(Path(s['path']).read_bytes())==s['sha256']
assert sha((ROOT/'um.py').read_bytes())==V['working_sha256']
P=REV/'REVIEW_SCALAR_TOMITA_ADJOINT.md';old=P.read_bytes()
assert sha(old)==V['original_review_sha256'] and len(old)==V['original_review_bytes']
marker='DEV_TOMITA_SQUARE_REVIEW'
assert marker.encode() not in old
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
backup=P.with_name(P.name+'.bak_'+stamp)
def link(label,p,line=None):return f'[{label}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
def src(name,line):return link(name+'.lean',ROOT/'kernel/TGLV350'/(name+'.lean'),line)
new_names=['AntilinearComposition','ClosedAntilinearResolvent','PositiveSurjectiveResolvent','ScalarTomitaSquare','ScalarTomitaSelfAdjoint']
ss=[V['sources']['TGLV350/'+n+'.lean'] for n in new_names]
rows='\n'.join(f"| {Path(s['path']).stem} | {len(s['declarations'])} | `{s['sha256']}` | `{s['author_binary_sha256']}` |" for s in ss)
logs='\n'.join(f"| {Path(s['author_log']).name} | `{s['author_log_sha256']}` |" for s in ss)
procs='\n'.join(f"| {r['module']} | {r['returncode']} | {r['seconds']} |" for r in V['records'] if Path(r['run'])!=runs[0])
aud=C['records'][-1]
text=f'''

## ADENDO DEV — composição S†S e auto-adjunticidade

<!-- {marker} -->

{date}. **[REAL — revisão DEV encerrada, sete módulos/53 alvos; nenhum achado P0, P1 ou P2.]** Este adendo incorpora os três auxiliares/12 alvos e os dois módulos concretos/18 alvos ao estrato anterior de dois módulos/23. As exclusões de S†S no texto anterior descrevem aquele escopo histórico; a composição e suas propriedades passam a ser conferidas aqui. O texto anterior permanece integralmente como prefixo de {len(old)} bytes, SHA `{sha(old)}`, com {link('backup imediato exato',backup)}.

**Resultado delimitado:** no mesmo `ScalarGNSHilbert P = H_I`, A é o `LinearPMap` complexo-linear **S†S**, com domínio exato **{{x∈D(S) : Sx∈D(S†)}}**. As provas fornecem sua simetria, positividade, sobrejetividade de I+A, domínio denso, auto-adjunticidade pelo adjunto máximo Mathlib, gráfico fechado e núcleo trivial. As hipóteses dos critérios genéricos são efetivamente demonstradas para esse A; não foram acrescentadas como premissas a P.

{src('AntilinearComposition',12)}: a preimagem exige a pertinência efetiva a D e a imagem por S em E. A inclusão no domínio original preserva o vetor por `rfl` (linhas 32–39); a restrição da imagem usa o testemunho de pertinência. A composição na linha 45 cancela duas conjugações escalares, produzindo um mapa parcial complexo-linear no domínio inteiro dessa preimagem. Não se omite o domínio da segunda aplicação nem se prolonga S ao ambiente.

{src('ClosedAntilinearResolvent',18)}: o gráfico é um submódulo **real** de `WithLp 2 (H×H)`, com a norma/produto interno de Hilbert do produto. O fechamento é transportado pela preimagem contínua de `ofLp` (linha 34). A única instância local nova é a canônica `InnerProductSpace.complexToReal` (linha 13); `CompleteSpace G` na linha 51 vem do fechamento do gráfico. Não há estrutura complexa fictícia no gráfico antilinear, nem completude postulada de um domínio não fechado.

{src('ClosedAntilinearResolvent',46)}: a projeção ortogonal real de (z,0) produz **x∈D** e `Re⟨z−x,u⟩=Re⟨Sx,Su⟩` para todo u∈D. O auxiliar exige H completo e gráfico fechado; não exige D denso nem S limitado. No teste em iu (linha 68), S(iu)=−iSu. Se a=⟨z−x,u⟩ e b=⟨Sx,Su⟩, a identidade real testada dá −Im(a)=Im(b). A conjugação de b, junto da parte real, fornece exatamente **⟨Su,Sx⟩=⟨z−x,u⟩**, com a orientação necessária ao adjunto antilinear. Esse é um teste legítimo porque D é submódulo complexo.

{src('PositiveSurjectiveResolvent',17)}: `hp` pede apenas **0≤Re⟨x,Tx⟩**; `hr` pede **∀z∈H, ∃x∈D(T), x+Tx=z**, sobrejetividade inteira. A densidade é deduzida: para v∈D(T)⊥, escrever v=x+Tx dá 0=‖x‖²+Re⟨x,Tx⟩, portanto x=0 e v=0. A completude permite passar do ortogonal trivial ao fecho total. A realidade completa do pareamento não é uma hipótese escondida desse lema de densidade; no critério de auto-adjunticidade a simetria é hipótese adicional explícita.

{src('PositiveSurjectiveResolvent',43)}: a prova obtém primeiro a densidade e só então usa `LinearPMap.adjoint_isFormalAdjoint`, evitando a alternativa degenerada da definição Mathlib do adjunto quando não há densidade. Para a∈D(T*), resolve x+Tx=a+T*a. Testa contra cada b∈H, também escrito u+Tu; o pareamento do adjunto e a simetria dão ⟨a,b⟩=⟨x,b⟩. Assim a=x e Tx=T*a, isto é, **todo o gráfico de T*** está no de T, incluindo o domínio. A inclusão oposta vem de `hs.le_adjoint hd`. `isSelfAdjoint_def` conclui T*=T como mapas parciais. Não se confunde simetria num domínio prescrito com auto-adjunticidade, e não se pressupõe T fechado para obter esse resultado.

{src('ScalarTomitaSquare',14)} especializa D, E e S literalmente nos objetos do primeiro estrato. `domain_iff` (linha 40) e `apply` (linha 45) são igualdades definicionais que explicitam o domínio e a aplicação S†(Sx). O pareamento da linha 50 vale para x∈D(A) e **todo y∈D(S)**: **⟨Ax,y⟩=⟨Sy,Sx⟩**. A simetria usa a conjugação correta dos produtos internos; a identidade quadrática é **Re⟨x,Ax⟩=‖Sx‖²** (linha 75), e o lema `positive` expressa sua não negatividade. Essa identidade, acompanhada da simetria provada, justifica a positividade do operador; não é apenas uma inferência a partir do nome do lema.

{src('ScalarTomitaSelfAdjoint',15)} fecha a passagem genérico→P: usa o fechamento **anterior de S** para obter x∈D(S) e o pareamento complexo da projeção. `scalarTomitaAdjoint_maximal P hx` fornece Sx∈D(S†) e S†Sx=z−x. O testemunho w da linha 22 está, portanto, no domínio exato de A. Isso prova I+A sobrejetivo sem pressupor densidade, fechamento ou auto-adjunticidade de A. Nas linhas 28–40, os critérios genéricos recebem a positividade, a sobrejetividade e a simetria já provadas para o **mesmo** A. O fechamento de A vem de `IsSelfAdjoint.isClosed` da Mathlib. Os tipos concretos impressos usam P, sem premissas residuais de resolução variacional ou auto-adjunticidade.

{src('ScalarTomitaSelfAdjoint',42)}: Sx=0 implica x=0 pela involução anterior de S no domínio invariante. Se Ax=0, a identidade quadrática dá ‖Sx‖²=0, logo x=0 (linha 52). A conclusão é núcleo trivial. **Não fornece gap espectral, cota inferior uniforme positiva ou inversa limitada de A.** Também não afirma D(A)=H_I ou limitação de A/S.

Os tipos genéricos foram impressos com universos explícitos: H está em `Type` nesta implementação, não em um universo arbitrário reivindicado por extensão verbal. A aplicação concreta usa as estruturas de Hilbert herdadas do mesmo H_I. O grafo congelado de {V['project_graph_modules']} módulos é acíclico, e nenhuma dependência anterior aos sete novos os importa. A prova gaussiana do primeiro estrato conserva sua proveniência: densidade do adjunto por T* e injetividade de T, sem inverter T, sem alterar Haar/medida e sem substituir I por n_ν.

### Recompilação própria e reconciliação de pins

| Fonte acrescentada | Alvos | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---:|---|---|
{rows}

| Processo próprio acrescentado | rc | Segundos |
|---|---:|---:|
{procs}

São **sete novos processos próprios rc0** neste adendo: três auxiliares e auditor/12, dois concretos e auditor cumulativo/53. Somados aos três processos do primeiro estrato, há **dez processos rc0: sete compilações de módulos e três auditores**. Os dois primeiros módulos não foram recompilados redundantemente na última árvore; seus binários próprios foram reutilizados, seus hashes foram relidos e todos os 53 tipos/axiomas foram auditados novamente em conjunto. **Os sete .olean próprios coincidem byte a byte com os sete finais autorais.**

O auditor final contém 53 `#check` com universos e 53 `#print axioms`, sem hipóteses acrescentadas. A cobertura coincide exatamente com o manifesto e as fontes; cada alvo depende somente de **propext, Classical.choice e Quot.sound**. Os 35 tipos dos auditores anteriores coincidem com os do auditor cumulativo, normalizando apenas espaços da impressão. Nenhum `axiom`, `sorry`, `admit`, `unsafe` ou alteração de redutibilidade/transparência foi encontrado no código das sete fontes. O auxiliar de instância real não é um alvo adicional contado; foi lido e fica incluído nas dependências transitivas dos teoremas auditados.

Evidências próprias: {link('compilação dos três auxiliares e auditor/12',runs[1]/'compilation.json')}; {link('compilação dos dois concretos e auditor/53',RUN/'compilation.json')}; {link('53 tipos e axiomas completos',aud['stdout'])}; {link('verificação final e comparação de tipos/pins',RUN/'verification_dev.json')}. Auditor final: fonte `{aud['source_sha256']}`, binário `{aud['output_sha256']}`, stdout `{aud['stdout_sha256']}`. O manifesto {link('da árvore final',RUN/'manifest.json')} pina {V['dependency_count']} dependências próprias de projeto, inclusive os cinco módulos já recompilados nas duas árvores precedentes. O auxiliar usou apenas uma dependência de projeto própria, `AntilinearAdjointGraph`; o restante veio dos oito pacotes externos somente leitura. **Nenhum build autoral de projeto integra o LEAN_PATH.**

O compilador é o mesmo já pinado no primeiro estrato, SHA `{M['compiler_sha256']}`. Pacotes e dependências anteriores não foram recompilados nem receberam nova certificação global; mantêm-se os limites de proveniência anteriores, inclusive a errata histórica exclusivamente de comentário de `DualSemifiniteIdeal`. Os fontes/binários congelados foram reconferidos. As referências locais primárias da Mathlib sobre `LinearPMap`, adjunto máximo, projeção, produto L² e restrição ℂ→ℝ estão copiadas e pinadas em `mathlib_references` da árvore final. A única falha de preparação própria ocorreu **antes de executar Lean**, por o inventário de declarações ler a palavra `structure` dentro de comentário; foi corrigido somente o parser do revisor. A tentativa e a correção permanecem preservadas em `revisao/resolvent_aux_independent_20260912_105904_319758/preparation_failure.json` e nos scripts/backups próprios. Não é falha da fonte final nem processo Lean rc1 omitido.

| Log autoral final acrescentado | SHA256 do JSON |
|---|---|
{logs}

Os três `author_history.json` das árvores próprias preservam **{V['history_attempts']} tentativas: {V['history_rc0']} rc0 finais e {V['history_rc1']} rc1 históricos**. Seus JSONs e streams foram relidos por hash. Os erros anteriores são de elaboração, instâncias/simplificação e limites de heartbeats; eventuais `sorryAx` nesses outputs fracassados não são aceitos como prova. A conclusão usa exclusivamente as fontes finais, seus sete logs rc0 coincidentes e a recompilação própria. Nenhum erro histórico foi apagado nem tratado como achado pendente sem correspondência na versão final.

### Documentação, preservação e alcance final

Lidos integralmente e conciliados: `tomita_square_draft_status.json`, SHA **`{V['draft_status_sha256']}`**, e `RELATORIO_ADJUNTO_QUADRADO_DEV.md`, SHA **`{V['author_report_sha256']}`**. O hash do relatório coincide com o pin do manifesto. O texto distingue domínio exato, mesmo H_I, passagem pelo gráfico real, auto-adjunticidade deduzida e núcleo trivial sem gap. **Nenhum P2 documental encontrado.**

Original relido `{V['original_sha256']}`; cópia relida `{V['working_sha256']}`, ambos coerentes com a custódia antecedente. **Esta é revisão DEV, sem exame de nova integração.** Os 118 registros/75 controles/6456 Audit mencionados no estrato anterior pertencem à custódia precedente; não se somam os sete/53 a essas contagens. Não executei novos testes autorais, raízes, monólito, integrador, recorder ou verifier. Todas as escritas ficaram em `revisao/`; os demais pareceres, fontes autorais, originais, logs e memórias foram preservados.

**[OPEN — fora deste resultado]** Raiz positiva e decomposição polar deste S†S no mesmo H_I, identificação modular do peso, ponte de domínio/núcleo envolvendo n_ν, KMS, traço e escala dual, Three Locks/H1–H3, física, certificado consumido pelo gate e runtime. Nada no pacote fornece gap ou altera essas flags. **Não resta análise DEV necessária dentro dos sete módulos/53 alvos; o escopo delimitado está encerrado.**
'''
raw=old+text.encode('utf-8')
assert raw.startswith(old) and len(raw)>len(old)
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old
temp=P.with_name(P.name+'.tmp_'+stamp)
with temp.open('xb') as f:f.write(raw)
assert temp.read_bytes()==raw
temp.replace(P)
assert P.read_bytes()==raw and P.read_bytes()[:len(old)]==backup.read_bytes()
for p,h in M['previous_reviews'].items():
    if Path(p)!=P:assert sha(Path(p).read_bytes())==h
closure={'timestamp':date,'status':'DEV_COMPLETE_NO_P0_P1_P2','marker':marker,
 'review_path':str(P),'review_sha256':sha(raw),'review_bytes':len(raw),'review_lines':len(raw.splitlines()),
 'backup':str(backup),'backup_sha256':sha(backup.read_bytes()),'original_prefix_exact':True,
 'cumulative_modules':7,'cumulative_targets':53,'cumulative_own_processes_rc0':10,
 'additional_own_processes_rc0':7,'all_7_bins_equal_author':True,'all_53_axioms_trio':True,
 'findings':[],'necessary_DEV_analysis_remaining':False,'new_integration_inspected':False,
 'working_sha256':V['working_sha256'],'verification_sha256':sha((RUN/'verification_dev.json').read_bytes())}
q=RUN/'closure_dev.json';assert not q.exists()
b=json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8');t=q.with_suffix('.tmp_'+stamp)
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(q)
print(json.dumps(closure,ensure_ascii=False,indent=2))
