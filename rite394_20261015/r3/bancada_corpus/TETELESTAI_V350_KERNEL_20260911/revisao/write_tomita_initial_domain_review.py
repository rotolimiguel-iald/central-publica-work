"""Write a new DEV-only review with measured evidence; preserve every sealed review."""
from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent
RUN=Path((R/'tomita_initial_domain_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
V=json.loads((RUN/'verification_dev.json').read_bytes());D=json.loads((RUN/'author_tomita_domain_draft_status.json').read_bytes())
K=json.loads((RUN/'gns_representation_custody.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for k in ['complete','all_exit_zero','full_audit_names_exact','all_axioms_allowed','sources_unchanged','dependencies_unchanged','previous_reviews_preserved']:assert C[k],k
for k in ['five_compiles_rc0','exact_target_set','axioms_match_status','all_axioms_allowed','dependencies_frozen_preserved','author_project_builds_excluded','status_unchanged','route_equals_status_and_frozen','custody_equals_status','previous_representation_review_equals_custody','previous_reviews_preserved']:assert V[k],k
for row in V['records'].values():assert all(v for v in row.values() if isinstance(v,bool))
assert len(V['records'])==4 and V['audited_targets']==14
for p,h in M['previous_reviews'].items():assert sha(Path(p))==h,p
assert sha(ROOT/'tomita_domain_draft_status.json')==M['draft_status_sha256']
assert sha(ROOT/'ROTA_DOMINIO_TOMITA_RASCUNHO.md')==M['route_sha256']
assert sha(ROOT/'gns_representation_custody.json')==M['custody_sha256']
assert all(sha(Path(r['path']))==r['sha256'] for r in M['sources'].values())
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
counts={Path(rel).stem:len(r['declarations']) for rel,r in M['sources'].items()}
table='\n'.join('| '+n+' | '+str(counts[n])+' | `'+r['source_sha256']+'` | `'+r['own_binary_sha256']+'` |' for n,r in V['records'].items())
logtable='\n'.join('| '+n+' | '+Path(r['author_log']).name+' | `'+r['author_log_sha256']+'` |' for n,r in V['records'].items())
exceptions=V['dependency_comment_only_exceptions'];ex=exceptions['TGLV350.DualSemifiniteIdeal']
warnings={Path(row['module']).stem:[s for s in Path(row['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in s] for row in C['records']}
assert all(not x for x in warnings.values())
report=f'''# Revisão independente — domínio inicial de Tomita

{date}. **Escopo DEV concluído: quatro módulos/14 alvos. Nenhum achado P0, P1 ou P2 nas fontes finais e na rota documental delimitada.** [REAL — leitura integral, recompilação independente e auditor próprio] As provas dão transferência de limites fortes uniformemente limitados pela ação ambiente, densidade de Λ(I∩I*) na norma GNS e um gráfico inicial univalente, invariante pela troca, com domínio denso. Não dão univalência do fecho ou operador Tomita fechado.

Esta revisão é nova. {link(R/'REVIEW_GNS_REPRESENTATION.md')} e os demais pareceres/custódias anteriores permanecem intocados. Os quatro módulos foram pinados por {link(ROOT/'tomita_domain_draft_status.json')}; não se reutiliza o parecer anterior como evidência de seus novos teoremas. A rota {link(ROOT/'ROTA_DOMINIO_TOMITA_RASCUNHO.md')} foi lida integralmente, inclusive o adendo que passa de nove para 14 alvos.

## Provas, tipos e hipóteses

**DualOrbitStrongLimits.lean:14–56 (3 alvos).** `dualCharacterField a` é a família s↦D_(a·s), fortemente contínua, com cota de norma 1. Na mesma representação regular K=L²(ℝ,TowerHilbert P), a ação no Hilbert exterior L²(ℝ,K) satisfaz

`L_A = W₊ · fibre(A) · W₋`, com `W₊ = lift(s↦D_s)` e `W₋ = lift(s↦D_(-s))`.

O sinal e a ordem seguem da convenção efetiva `dualAmbient s A = D_s A D_s*` e de `D_s*=D_(-s)`, sem troca de representação ou de fluxo. A igualdade é provada por quatro igualdades a.e. para **A e f fixados**. Depois, W₊ e W₋ são operadores limitados fixos; nenhum conjunto conulo é intersectado ao longo da rede.

O teorema de transferência recebe explicitamente Tᵢ, o CLM limite S, uma cota real C com `∀ i, ‖T i‖≤C`, e `∀ v, T i v→S v` ao longo de **qualquer filtro** sobre `ι : Type*`. Aplica o lema herdado `fibre_tendsto_of_uniformly_bounded` ao único vetor W₋f e a continuidade de W₊. Esse lema herdado usa funções simples de medida finita e equicontinuidade; não exige enumerabilidade, separabilidade, topologia no índice, continuidade em norma de operador nem uma cota adicional de S. Não se afirma existência de um limite forte para uma família que não o tenha. A cota é para todos os índices, não apenas eventual; filtros triviais são admitidos pelo enunciado geral, e a aplicação de densidade usa o filtro não trivial indicado abaixo.

**ScalarGNSStarApproximation.lean:15–51 (3 alvos).** Para A∈I, a definição dá `A_h=X_h* A` no mesmo ideal esquerdo I para todo h. Para **h>0**, A_h* = A*X_h também pertence a I, pois X_h∈I e I é fechado por multiplicação à esquerda por operadores limitados; não se supõe A*∈I. Assim A_h∈I∩I*. O operador e seu adjunto são finitos no sentido uniforme que define esse ideal, não meramente finitos em um vetor escolhido.

Para a convergência, `‖X_h*‖≤1` vale para todo h e `X_h*→I` fortemente vem do lema de adjuntas de contrações, já revisado. Esse lema utiliza a cota de contração; não presume continuidade geral de `star` na SOT. A restrição de `𝓝[≠]0` para `𝓝[>]0` está na direção correta, pois h>0 implica h≠0. Aplicando a transferência ao vetor **fixo Λ(A)** e o entrelaçamento previamente provado, obtém-se Λ(X_h*A)→Λ(A) na norma do L² exterior. A única hipótese sobre A é A∈I; não se introduz estimativa ou convergência à direita de AX_h na norma ν, nem regularização bilateral.

**ScalarGNSStarDensity.lean:13–35 (3 alvos).** `scalarGNSStarEmbedding` é uma função no mesmo H_I, obtida restringindo a inscrição linear já existente; não é declarada aqui como novo `LinearMap`. `tendsto_subtype_rng` transporta a convergência do ambiente para a topologia de H_I, que é a topologia da norma de Hilbert. Para cada A∈I, sua inscrição pertence ao fecho da imagem de I∩I*, usando pertinência eventual para h>0 e `isClosed_closure.mem_of_tendsto`. O filtro `𝓝[>] (0:ℝ)` é não trivial; assim esse passo não extrai pertinência de um limite vazio. A densidade já provada de Λ(I) em H_I conclui `DenseRange` de Λ|_(I∩I*). Esta é densidade GNS efetiva; não é somente densidade forte de operadores em N.

**ScalarTomitaGraph.lean:11–41 (5 alvos).** A inscrição restrita é injetiva pela inscrição de I. O objeto novo tem exatamente o tipo

`scalarTomitaGraph P : Set (ScalarGNSHilbert P × ScalarGNSHilbert P)`

e é `{{(Λ(A),Λ(A*)): A∈finiteDualStarCore P}}`. Dois pares com a mesma primeira coordenada têm o mesmo A pela injetividade, logo a mesma segunda coordenada. O representante A* produz o par trocado porque star(star A)=A. A imagem pela primeira projeção é densa pela densidade GNS anterior. Todos os vetores e pares estão no mesmo H_I; a adjunta algébrica é tomada no mesmo subtipo de N, estável por `star`.

“Invariância pela troca” descreve uma relação involutiva; não é uma afirmação de operador simétrico ou auto-adjunto no sentido dos produtos internos. O arquivo não toma o fecho do conjunto, não prova que esse fecho seja univalente e não empacota um mapa parcial semilinear. Não há circularidade com fechabilidade, Tomita ou KMS: a univalência inicial depende apenas da injetividade já construída. Nos tipos finais de densidade/univalência/troca não restam hipóteses de densidade, fidelidade ou domínio máximo fornecidas pelo chamador.

## Recompilação e axiomas

**Quatro fontes + auditor próprio, cinco processos rc0**, sem warnings. O auditor contém `#check` de todas as 14 declarações nomeadas e `#print axioms` dos mesmos 14 alvos; conjuntos exatos comparados às fontes e ao status. Todos os alvos usam somente `propext`, `Classical.choice`, `Quot.sound`; nenhum `sorryAx` ou axioma adicional. A saída completa do auditor foi lida. Não houve tentativa de compilação própria falhada nesta etapa.

| Fonte DEV | Alvos | SHA256 da fonte congelada e viva | SHA256 .olean próprio = autoral |
|---|---:|---|---|
{table}

| Fonte | Log final autoral conferido, sem executá-lo | SHA256 JSON do log |
|---|---|---|
{logtable}

Foram conferidos hash da fonte, fonte inalterada durante o build autoral, rc0, hash do binário existente, stdout/stderr e igualdade dos streams com suas cópias congeladas. Os quatro .olean próprios são **byte a byte iguais aos autorais finais**. Tentativas anteriores autorais ficam nos logs e não foram tratadas como defeitos pendentes dos bytes finais. Os processos próprios e seus tempos/outputs constam de {link(RUN/'compilation.json')}; os vínculos e hashes de todos os streams estão em {link(RUN/'verification_dev.json')}.

Auditor próprio: fonte `{V['own_auditor_source_sha256']}`; .olean `{V['own_auditor_binary_sha256']}`; stdout `{V['own_auditor_stdout_sha256']}`. Declarações completas e tipos expandidos: {link(RUN/'sources/TomitaInitialDomainAudit.lean')} e {link(RUN/'logs/TomitaInitialDomainAudit.stdout.txt')}.

**Dependências pinadas.** {link(RUN/'manifest.json')} registra 385 dependências de projeto, suas fontes e binários próprios congelados, imports e origens nas árvores já revisadas de GNS/representação e domínio modular. Foram copiados apenas os módulos necessários desse catálogo; nenhuma dependência de projeto veio do build autoral. A árvore de saída deste run é a única entrada de projeto no `LEAN_PATH`; seguem apenas os pacotes existentes em modo leitura. Não se recompilou biblioteca nem os GNS anteriores. O compilador, versão e caminho efetivo estão no manifesto: `{M['lean_version']}`, SHA256 `{M['compiler_sha256']}`.

Permanece explícita a herança histórica de `DualSemifiniteIdeal`: fonte própria `{ex['source_sha256']}`, binário próprio `{ex['sha256']}`, fonte autoral corrigida `{ex['live_source_sha256']}`. A diferença literal foi conferida e consiste somente no comentário já revisado, com provas intactas. Não se afirma reprodução byte a byte da cadeia inteira herdada; limitações binárias de pareceres anteriores permanecem válidas. `RegularScalarWeightCertificate`, que tinha limitação binária registrada anteriormente, não está no fecho de imports desta etapa. Todas as dependências próprias pinadas, as quatro fontes vivas e os pareceres anteriores permaneceram inalterados durante o build.

## Rota, estatuto e limites

Status congelado: `{V['status_sha256']}`. Rota integralmente lida: `{V['route_sha256']}`; seu hash coincide com o status. O texto principal documenta a fatoração, a regularização esquerda suficiente e a densidade na norma GNS; o adendo explicita os cinco alvos do gráfico inicial e mantém fechabilidade aberta. As referências a nove alvos e à obrigação anterior são um estrato histórico preservado, atualizado pelo adendo para quatro módulos/14 alvos. Não encontrei exagero documental que promova densidade ou invariância por troca a fechabilidade.

Custódia anterior lida e pinada: `{V['custody_sha256']}`. Seu pin de {link(R/'REVIEW_GNS_REPRESENTATION.md')} coincide com o hash vivo `{V['previous_representation_review_sha256']}`. O snapshot anterior `{K['working_sha256']}` e as contagens {K['integrated_records']} registros/{K['controls']} controles/{K['audit_declarations']} Audit são **herança da custódia GNS**, não evidência integrada dos quatro módulos novos. Não foi repetido o verifier de custódia ou seus 23 backups nesta revisão; a preservação dos pareceres foi conferida diretamente por hash.

**Conclusão exclusivamente DEV.** Nenhuma integração, raiz ou controle Python novo foi executado ou certificado aqui. As quatro recompilações próprias e o auditor encerram o exame autônomo solicitado; eventual integração exigirá inspeção separada de seus artefatos finais, sem usar contagens históricas como se fossem novas.

Continuam [OPEN / fora deste escopo]: univalência do fecho do gráfico, fechabilidade/operador Tomita fechado, normalidade da representação GNS, domínio escalar máximo, decomposição polar, identificação modular/KMS, traço, interfaces operatoriais/preduais, Three Locks/H1–H3, física, consumo de certificado pelo gate e runtime. Não se analisaram fontes posteriores de fechabilidade. Nenhuma análise necessária dos quatro módulos/14 alvos ficou pendente; nenhum gate foi promovido.

Originais, monólito, fontes autorais, memórias, recorders, testes, logs e pareceres anteriores permaneceram somente leitura. Não se executou/importou monólito ou programa autoral. Todas as saídas desta revisão estão em `revisao/`. Este parecer é um arquivo novo; adendos futuros, se solicitados antes de custódia, exigem backup imediato dos bytes e append preservando este estrato.
'''
p=R/'REVIEW_TOMITA_INITIAL_DOMAIN.md';assert not p.exists()
raw=report.encode('utf-8');tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw and len(raw)>500;tmp.replace(p)
closure={'timestamp':date,'status':'DEV_COMPLETE_NO_P0_P1_P2','review_path':str(p),'review_sha256':sha(p),'review_bytes':len(raw),'new_sources':4,'new_targets':14,'own_compiler_processes_rc0':5,'author_bins_equal_own':all(r['own_binary_equals_author'] for r in V['records'].values()),'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),'own_dependencies_preserved':C['dependencies_unchanged'],'integrated_inspection_performed':False,'author_programs_executed':False,'working_sha256_at_close':sha(ROOT/'um.py')}
out=RUN/'closure_dev.json';assert not out.exists();b=json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8');t=out.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(out)
print(json.dumps(closure,ensure_ascii=False,indent=2))
