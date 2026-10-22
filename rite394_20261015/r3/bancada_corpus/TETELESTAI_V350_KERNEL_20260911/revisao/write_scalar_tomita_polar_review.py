"""Write only the new polar DEV review and its own evidence closure."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_polar_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');V=load(RUN/'verification_dev.json');ST=load(RUN/'tomita_polar_draft_status.json')
assert all(v for k,v in C.items() if isinstance(v,bool))
assert C['exact_16_targets'] and V['all_3_own_binaries_byte_equal_author']
def link(label,p,line=None):return '['+label+'](<' +Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
def src(n,line):return link(n+'.lean:'+str(line),ROOT/'kernel/TGLV350'/(n+'.lean'),line)
rows=[];logs=[]
for rel,s in M['sources'].items():
    r=next(r for r in C['records'] if r['module']==rel);n=Path(rel).stem;p=ST['modules'][n]
    assert hf(s['path'])==hf(s['snapshot'])==s['sha256']
    rows.append('| '+link(n,ROOT/'kernel'/rel)+' | '+str(len(r['axioms']))+' | `'+s['sha256']+'` | `'+r['output_sha256']+'` |')
    logs.append('| '+n+' | '+link(Path(p['final_log']).name,RUN/'author_history'/Path(p['final_log']).name)+' | `'+p['stdout_sha256']+'` |')
times='\n'.join('| '+r['module']+' | 0 | '+str(r['seconds'])+' |' for r in C['records'])
pinfiles=['tomita_polar_draft_status.json','RELATORIO_FATOR_POLAR_TOMITA_DEV.md','tomita_root_custody.json','tomita_root_domain_draft_status.json']
artifactrows='\n'.join('| '+link(n,ROOT/n)+' | `'+hf(ROOT/n)+'` |' for n in pinfiles)
assert hf(ROOT/'tomita_polar_draft_status.json')==M['draft_status_sha256']
assert hf(ROOT/'RELATORIO_FATOR_POLAR_TOMITA_DEV.md')==M['report_sha256']
assert hf(REV/'REVIEW_SCALAR_TOMITA_DOMAIN.md')==ST['domain_review_sha256']
assert hf(ROOT/'tomita_root_domain_draft_status.json')==ST['domain_manifest_sha256']
assert hf(ROOT/'tomita_root_custody.json')==ST['parent_custody_sha256']
for p,h in M['previous_reviews'].items():assert hf(p)==h
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão independente DEV — fator antiunitário de Tomita

{now}. **[REAL — leitura integral das três fontes e recompilação própria] Nenhum achado P0–P2 nos três módulos/16 alvos finais.** O pacote constrói um antiunitário `U=scalarTomitaPolarFactor P` no mesmo `ScalarGNSHilbert P`, satisfazendo `U(Bx)=Sx` em todo `D(S)=D(B)`. A conclusão não inclui `U²=I`, conjugação modular `J`, KMS ou identificação com o peso. Revisão DEV concluída; integração não examinada.

Li integralmente o manifesto correto `tomita_polar_draft_status.json`, `RELATORIO_FATOR_POLAR_TOMITA_DEV.md` e as três fontes. O manifesto ancora a mãe `tomita_root_custody.json` e os pins do manifesto/parecer do domínio. Esses pins conferiram; os seis módulos/25 alvos anteriores foram reutilizados, sem recompilação ou modificação.

**Provas, tipos e hipóteses.**

- {src('PartialSelfadjointRange',13)}–37: o lema genérico exige explicitamente domínio denso, auto-adjunção com o adjunto Mathlib e núcleo trivial. Se `z` é ortogonal à imagem, a conjugação da igualdade zero fornece o pareamento correto `⟨0,x⟩=⟨z,Bx⟩`. `mem_adjoint_domain_of_exists` põe `z` no domínio máximo do adjunto; `adjoint_apply_eq` usa a hipótese de densidade para concluir `B†z=0`. A igualdade **de operadores parciais** `B†=B` transporta `(z,0)` entre grafos; núcleo zero dá `z=0`. O complemento ortogonal zero implica densidade da imagem. Não se utiliza somente simetria formal, nem o ramo convencional do adjunto de domínio não denso. Não se infere imagem sobrejetiva ou inverso limitado de `B`.
- {src('DenseAntilinearExtension',9)}–26: `f : E →ₛₗ[starRingEnd ℂ] H` é conjugado-linear, enquanto `e : E →ₗ[ℂ] H` é linear. Os tipos impressos preservam essa distinção. `include hd hn` mantém as hipóteses explícitas, e `hn` fornece a cota com constante 1 exigida por `LinearMap.extendOfNorm_eq`; não há recurso ao comportamento total da definição sem suas hipóteses. A extensão continua semilinear e contínua em `H`. A igualdade das normas passa da imagem densa de `e` para todo `H` pelo conjunto fechado de igualdade de funções contínuas. Não é exigida norma em `E`, nem inverso limitado de `e`.
- {src('DenseAntilinearExtension',28)}–45: a densidade de `f` é hipótese adicional **necessária nesta prova de sobrejetividade**, distinta da densidade de `e`. A imagem da isometria contém `Ran f`; é fechada porque a fonte `H` é completa. Logo coincide com `H`. `LinearIsometryEquiv.ofSurjective` produz efetivamente `H ≃ₛₗᵢ[starRingEnd ℂ] H`, e não apenas uma isometria em um subespaço.
- {src('ScalarTomitaPolarFactor',14)}–47: os três requisitos para `Ran B` densa vêm da raiz já construída. `scalarTomitaRootImage` é exatamente `S` composto com a inclusão `D(B)≤D(S)`. As inclusões ida/volta devolvem o mesmo subtipo por `Subtype.ext rfl`; a igualdade de normas anterior aplica-se ao mesmo vetor. Para `y∈D(S)`, escolhe-se `Sy∈D(S)=D(B)` e usa-se `S(Sy)=y`, provando `D(S)⊆Ran f`; como `D(S)` é denso, obtém-se a densidade requerida, sem assumir `Ran S=H`.
- {src('ScalarTomitaPolarFactor',49)}–64: a identidade da extensão em `Bx` é especializada por inclusão a **todo** `x∈D(S)`. O enunciado Lean é essa igualdade pontual com subtipos explícitos; junto à igualdade prévia dos domínios e à totalidade de `U`, justifica `S=UB` no domínio inteiro. Os nove tipos concretos recebem somente `P` e os vetores indicados, sem antiunitário, densidade de imagem, norma ou fatoração como premissas novas. O resultado não se transfere para outro peso/espaço/representação.

Conferi as APIs Mathlib `extendOfNorm`/`extendOfNorm_eq` e `mem_adjoint_domain_of_exists`/`adjoint_apply_eq` nas fontes readonly usadas pelo projeto; seus hashes estão em {link('verification_dev.json',RUN/'verification_dev.json')}. Os auxiliares usam `E,H : Type`, com as estruturas explicitadas; não reivindico generalização adicional de universos. Não há instâncias locais novas nas três fontes. Os 16 tipos completos, com universos, foram lidos no {link('auditor próprio',Path(C['records'][-1]['stdout']))} e estão transcritos na evidência própria.

**Recompilação independente e pins.** O snapshot reutiliza {V['dependencies_count']} dependências próprias: as 411 herdadas e os seis módulos da revisão de domínio. As fontes e binários foram relidos por hash tanto na origem própria quanto no novo congelamento. O grafo de {V['project_import_graph_modules']} módulos (417+3) é acíclico, sem import das dependências anteriores para estes novos módulos. O `LEAN_PATH` contém apenas o build desta revisão e oito diretórios de pacotes readonly; nenhum build autoral de projeto. Compilador pinado `{M['compiler_sha256']}`; {M['lean_version']}. Pacotes e base são herança conferida por pins, sem rebuild global.

| Execução própria | rc | Segundos |
|---|---|---|
{times}

As quatro execuções próprias passaram. Os três `.olean` são byte a byte iguais aos autorais finais; todas as 16 declarações usam exclusivamente `propext`, `Classical.choice` e `Quot.sound`, coincidindo entre cada módulo, o auditor próprio e o manifesto. Fontes, streams, dependências e pareceres anteriores permaneceram pinados. Ausentes `sorry`, `axiom`, `unsafe`, `admit` e alterações inseguras de transparência/redutibilidade nas três fontes; as únicas opções são de elaboração/linter/heartbeats. Não executei/importei scripts autorais ou monólito.

| Módulo | Alvos | SHA256 fonte DEV | SHA256 `.olean` próprio = autoral final |
|---|---|---|---|
{chr(10).join(rows)}

| Módulo | Log final aceito, preservado em revisão | SHA256 stdout autoral |
|---|---|---|
{chr(10).join(logs)}

**Histórico e documentação.** Os cinco registros encontrados são três rc0 finais e os dois rc1 pinados de `DenseAntilinearExtension`: o primeiro omitia `hd`/`hn` do contexto; o segundo deixava a reflexividade da desigualdade sem prova. Os streams rc1 imprimem `sorryAx`; foram lidos e preservados, mas excluídos integralmente da evidência aceita. A versão final inclui `hd hn` e `le_rfl`, com quatro recompilações próprias verdes. O relatório descreve corretamente antiunitariedade, fatoração e seus limites; não encontrei exagero documental ou hipótese residual.

| Artefato lido | SHA256 |
|---|---|
{artifactrows}

Parecer do domínio preservado: `{ST['domain_review_sha256']}`. A cópia integrada antecedente continua `{V['working_sha256']}` e o original relido `{V['original_sha256']}`. Os 16 alvos ainda não constam do Audit integrado atual; não conferi futura transposição/raízes/controles deste lote. A custódia anterior é mãe matemática/documental, sem nova execução do recorder/verifier nesta revisão.

Evidências: {link('manifest.json',RUN/'manifest.json')}, {link('compilation.json',RUN/'compilation.json')}, {link('verification_dev.json',RUN/'verification_dev.json')}, {link('author_history.json',RUN/'author_history.json')}; scripts próprios {link('runner',REV/'run_scalar_tomita_polar_review.py')} e {link('verificação',REV/'verify_scalar_tomita_polar_review.py')}. Toda escrita ficou em `revisao/`; nenhum parecer anterior, fonte, memória ou monólito foi alterado.

**[OPEN] Limites e encerramento.** O sentido de “fator antiunitário polar” é precisamente a equivalência conjugado-linear isométrica e a fatoração com a raiz positiva já construída no mesmo `H_I`. Este pacote não demonstra involução `U²=I`, identifica `U` com `J` modular, estabelece KMS/domínio máximo do peso/traço, nem implica gap, Three Locks, condições físicas ou consumo de certificado. A revisão DEV 3/16 está concluída sem P0–P2; nenhuma análise necessária resta neste escopo. Não promove gate, QG ou runtime, e não certifica a futura integração conjunta 9/41.
'''
out=REV/'REVIEW_SCALAR_TOMITA_POLAR.md';assert not out.exists();raw=text.encode('utf-8');tmp=out.with_name(out.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);assert out.read_bytes()==raw
closure={'timestamp':now,'review_path':str(out),'review_sha256':hf(out),'bytes':len(raw),'lines':len(raw.splitlines()),
 'verification_sha256':hf(RUN/'verification_dev.json'),'compilation_sha256':hf(RUN/'compilation.json'),
 'no_P0_P1_P2_findings':True,'own_Lean_executions':4,'targets':16,'DEV_review_complete':True,'new_integration_reviewed':False}
p=RUN/'closure_dev.json';assert not p.exists();b=json.dumps(closure,ensure_ascii=False,indent=2).encode();q=p.with_suffix('.tmp')
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b;q.replace(p)
print(json.dumps(closure,ensure_ascii=False,indent=2))
