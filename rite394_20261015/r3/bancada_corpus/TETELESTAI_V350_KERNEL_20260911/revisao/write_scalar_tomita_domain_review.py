"""Write the new DEV domain/energy review; never touch earlier reports."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_domain_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');V=load(RUN/'verification_dev.json');ST=load(RUN/'tomita_root_domain_draft_status.json')
assert C['complete'] and C['all_exit_zero'] and C['exact_25_targets']
assert V['all_axioms_trio'] and V['all_6_own_binaries_byte_equal_author']
def link(label,p,line=None):return '['+label+'](<' +Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
def src(name,line):return link(name+'.lean:'+str(line),ROOT/'kernel/TGLV350'/(name+'.lean'),line)
rows=[]
for rel,s in M['sources'].items():
    r=next(r for r in C['records'] if r['module']==rel)
    assert hf(s['path'])==hf(s['snapshot'])==s['sha256']
    rows.append('| '+link(Path(rel).stem,ROOT/'kernel'/rel)+' | '+str(len(r['axioms']))+' | `'+s['sha256']+'` | `'+r['output_sha256']+'` |')
times='\n'.join('| '+r['module']+' | 0 | '+str(r['seconds'])+' |' for r in C['records'])
logs='\n'.join('| '+n+' | '+link(Path(p['final_log']).name,RUN/'author_history'/Path(p['final_log']).name)+' | `'+p['stdout_sha256']+'` |' for n,p in ST['modules'].items())
artifactrows='\n'.join('| '+link(n,ROOT/n)+' | `'+hf(ROOT/n)+'` |' for n in ['tomita_root_domain_draft_status.json','RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md','tomita_root_custody.json','tomita_root_custody_verification.json'])
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão independente DEV — domínio e energia da raiz de Tomita

{now}. **[REAL — inspeção integral das seis fontes e recompilação própria] Nenhum achado P0–P2 no pacote final de seis módulos/25 alvos.** As provas estabelecem `D(B)=D(S)` e `‖Bx‖²=‖Sx‖²` para todo `x∈D(S)`, com `S=scalarClosedTomita P`, `A=scalarTomitaSquare P=S†S` e `B=scalarTomitaPositiveRoot P`, no mesmo `ScalarGNSHilbert P`. O exame DEV delimitado está concluído.

Manifesto efetivamente usado: {link('tomita_root_domain_draft_status.json',ROOT/'tomita_root_domain_draft_status.json')}. O homônimo histórico `tomita_domain_draft_status.json` descrevia o pacote antigo de aproximação GNS; foi reconhecido como tal, preservado e excluído dos pins desta nova revisão. Li integralmente o relatório novo e as seis fontes. Nenhum módulo posterior de antiunitariedade foi incluído.

**Conteúdo das provas e hipóteses conferidas.**

- {src('RealGraphCore',17)}, linhas 17–120: a restrição de `S` antilinear é somente real-linear; o gráfico é submódulo real de `WithLp 2 (H×H)`, com a mesma topologia produto e norma de gráfico. O argumento de densidade toma o complemento ortogonal **dentro do gráfico completo**, cuja completude vem do fechamento assumido. Para `w=(x,Sx)` ortogonal à imagem do core, aplica `hr` a `z=x`; a identidade fraca dá `⟨x,x⟩ℝ=0`, portanto `x=0` e `Sx=0`. A orientação em `real_inner_comm (F u) w` é correta. Não substitui densidade de gráfico por densidade em `H`, nem assume um inverso limitado de `S`. As sequências seguem da metrizabilidade do gráfico, sem hipótese de separabilidade.
- {src('ScalarTomitaGraphCore',16)}, linhas 16–66: `D(A)≤D(S)` vem do domínio real da composição. A família `u+Au=z` é a previamente provada por projeção no gráfico de **este** `S` e adjunto máximo; não é premissa nova sobre `P`. A identidade `⟨Au,x⟩ℂ=⟨Sx,Su⟩ℂ` é usada com parte real e simetria real para obter exatamente a orientação `⟨x,u⟩ℝ+⟨Sx,Su⟩ℝ=⟨x,z⟩ℝ`, contra todo `x∈D(S)`. Fechamento de `S` e o lema genérico dão core e aproximação nas duas coordenadas.
- {src('PartialSquareGraphCore',14)}, linhas 14–64: `he : partialOperatorSquare B=A` é hipótese explícita, mantida por `include he`; a igualdade inclui o domínio de duas aplicações. `partialSquare_pairing_all` usa os dois pontos do gráfico e simetria formal de `B` para parear contra **todo `D(B)`**, não apenas `D(A)`. O teorema genérico de core exige simetria, gráfico fechado e sobrejetividade de `I+A`; não afirma isso para um operador arbitrário sem essas hipóteses.
- {src('GraphCoreNormTransfer',18)}, linhas 18–61: a hipótese `hn` vale para todo vetor do submódulo comum `C`. Aplicá-la a `u_m−u_n` e usar a real-linearidade transfere a condição de Cauchy das imagens por `S` às imagens por `T`. A completude utilizada é a de `H`, não a do domínio de `T`. O fechamento do gráfico de `T` põe `(x,y)` no gráfico; continuidade da norma e unicidade de limites produzem a igualdade de normas. **Nenhuma igualdade `Sx=Tx` ou continuidade limitada dos operadores é pressuposta.**
- {src('ScalarTomitaRootGraphCore',14)}, linhas 14–55: a aplicação concreta fornece todas as hipóteses do core de `B` usando o quadrado exato, a simetria da raiz previamente construída, o seu gráfico fechado e a mesma sobrejetividade de `I+A`. Os testemunhos continuam no `H_I` original; os subtipos são reconciliados por igualdade de seus vetores ambientes.
- {src('ScalarTomitaRootDomain',14)}, linhas 14–73: a energia já provada em `D(A)` dá igualdade de **normas**, usando sua não negatividade. As duas aplicações de transferência fornecem ambas as inclusões; `le_antisymm` dá igualdade de submódulos, não apenas equivalência abstrata. O argumento de extensão é usado novamente para a norma no domínio inteiro, e o quadrado dessa igualdade dá a energia final. Os seis tipos finais impressos têm somente `P` e, quando pertinente, o vetor no domínio; não recebem igualdade de domínios, core, fechamento ou energia global como hipóteses residuais.

Os auxiliares genéricos usam `H : Type` com grupo normado, produto interno complexo e completude; não reivindico aqui uma generalização adicional a universos não presentes em seus tipos. As três instâncias locais (`realGraphHilbert`, `scalarGraphRealHilbert`, `squareGraphRealHilbert`) são exatamente `InnerProductSpace.complexToReal`. Não introduzem novo produto interno/norma independente; a estrutura complexa e as coerções reais do mesmo subobjeto são preservadas. Os 25 tipos completos com universos estão em {link('verification_dev.json',RUN/'verification_dev.json')} e no {link('stdout do auditor próprio',Path(C['records'][-1]['stdout']))}.

**Recompilação e proveniência.** Congelei as seis fontes, logs finais e histórico, e reutilizei {V['dependencies_count']} dependências do projeto a partir da árvore própria anterior {link('manifesto da revisão da raiz',Path(M['previous_run'])/'manifest.json')}, conferindo hashes de fonte/binário em cada origem e cópia. O novo `LEAN_PATH` contém somente o `build` desta revisão e oito caminhos de pacotes externos readonly; não contém o `build` autoral de projeto. Compilador herdado e conferido por hash: `{M['compiler_sha256']}`; {M['lean_version']}. Pacotes/base herdados não foram reconstruídos. O grafo de imports possui {V['project_import_graph_modules']} módulos (411 anteriores + 6 novos), é acíclico e nenhum import das dependências antigas aponta para estes seis novos, afastando circularidade de imports na construção.

| Execução própria | rc | Segundos |
|---|---|---|
{times}

As sete execuções (seis módulos e auditor `#check` com universos/`#print axioms` para os 25 nomes) passaram. Todos os alvos dependem somente de `propext`, `Classical.choice`, `Quot.sound`. Os seis `.olean` próprios são byte a byte iguais aos respectivos binários autorais finais. Fontes, dependências, stdout/stderr, compilador e pareceres anteriores permaneceram nos hashes pinados. Ausentes `sorry`, `axiom`, `unsafe`, `admit`, alterações de transparência/redutibilidade insegura nas seis fontes; as opções locais limitam-se a `autoImplicit`, linter e orçamento de heartbeats. Esta é recompilação **DEV própria**, sem recompilar raízes integradas ou executar scripts autorais/monólito.

| Módulo | Alvos | SHA256 fonte DEV | SHA256 `.olean` próprio = autoral final |
|---|---|---|---|
{chr(10).join(rows)}

| Módulo | Log autoral final aceito, copiado para revisão | SHA256 stdout final |
|---|---|---|
{logs}

**Histórico excluído da evidência aceita.** Foram encontrados {V['history_attempts']} registros autorais: seis rc0 finais pinados, um rc0 anterior de `GraphCoreNormTransfer` já substituído e cinco rc1. Os cinco rc1 correspondem exatamente às listas `failed_attempts` do manifesto: dois de `RealGraphCore` (colisão da instância real e orientação do pareamento), um de `ScalarTomitaGraphCore` (timeout), um de `PartialSquareGraphCore` (`he` não incluída no contexto e erros derivados) e um de `GraphCoreNormTransfer` (coerção na reescrita). Li seus streams; alguns imprimem `sorryAx`, e esses resultados não foram aceitos nem importados no build próprio. O rc0 antigo também não substitui o pin final. Fontes corrigidas e os 25 axiomas finais próprios resolvem os erros históricos; não são bugs pendentes. A preparação do runner próprio teve uma interrupção antes de Lean por nome incorreto da chave de contagem do antecedente, corrigida no script da revisão, sem alteração nas fontes.

**Documentação, custódia e alcance.** O relatório DEV descreve corretamente a norma de gráfico, Cauchy das diferenças, duas inclusões e igualdade de energia. Preserva a distinção entre o ideal de inscrição GNS e o domínio máximo do peso e não promove polar/KMS/traço. A mãe atual lida e pinada é `tomita_root_custody.json`; seu resultado autoral registra 130 pares binários e 34 backups. Neste DEV conferi o pin dessa custódia/verificação e os pareceres por ela pinados, sem reexecutar o verifier ou recertificar os 130 pares. O antecedente integrado continua `{V['working_sha256']}`; o original relido tem SHA `{V['original_sha256']}`. Os 25 novos alvos não constam do Audit integrado atual. Nenhuma integração destes seis módulos é certificada neste parecer.

| Artefato lido | SHA256 |
|---|---|
{artifactrows}

Evidências próprias: {link('manifest.json',RUN/'manifest.json')}, {link('compilation.json',RUN/'compilation.json')}, {link('verification_dev.json',RUN/'verification_dev.json')}, {link('author_history.json',RUN/'author_history.json')}; scripts {link('runner',REV/'run_scalar_tomita_domain_review.py')} e {link('verificação',REV/'verify_scalar_tomita_domain_review.py')}. Todos os hashes foram lidos de arquivos. Toda escrita ficou em `revisao/`; pareceres custodiados, fontes, memórias e monólito permaneceram intocados.

**[OPEN] Limites preservados.** A igualdade `D(B)=D(S)` e a energia nesse domínio estão provadas no pacote DEV; não afirmam domínio igual a todo `H_I`, operador limitado, invariância de `D(B)` por `B` ou gap. Não constroem o fator antiunitário polar, KMS, identificação com o domínio máximo do peso, traço, Three Locks, condições físicas ou consumo de certificado pelo gate. O estado integrado anterior e seus números são herança, não resultado novo desses módulos. Nenhuma análise matemática DEV necessária resta neste escopo; a conclusão não promove gate/QG/runtime.
'''
out=REV/'REVIEW_SCALAR_TOMITA_DOMAIN.md';assert not out.exists()
for p,h in M['previous_reviews'].items():assert hf(p)==h
raw=text.encode('utf-8');tmp=out.with_name(out.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);assert out.read_bytes()==raw
closure={'timestamp':now,'review_path':str(out),'review_sha256':hf(out),'bytes':len(raw),'lines':len(raw.splitlines()),
 'verification_sha256':hf(RUN/'verification_dev.json'),'compilation_sha256':hf(RUN/'compilation.json'),
 'no_P0_P1_P2_findings':True,'own_Lean_executions':7,'targets':25,'DEV_review_complete':True,'new_integration_reviewed':False}
q=RUN/'closure_dev.json';assert not q.exists();b=json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8');t=q.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(q)
print(json.dumps(closure,ensure_ascii=False,indent=2))
