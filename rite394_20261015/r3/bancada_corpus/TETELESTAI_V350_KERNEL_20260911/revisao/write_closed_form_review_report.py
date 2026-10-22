from pathlib import Path
import datetime
import hashlib
import json

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "closed_form_latest_run.txt").read_text(encoding="utf-8"))
M = json.loads((RUN / "manifest.json").read_bytes())
C = json.loads((RUN / "compilation.json").read_bytes())
FINAL = sorted(RUN.glob("final_integrated_*"))[-1]
F = json.loads((FINAL / "verification.json").read_bytes())
FAILED = json.loads((RUN / "author_failed_attempt/DualClosedForm_20260911_230623_951830.json").read_bytes())
REFERENCE = json.loads((RUN / "references/reference.json").read_bytes())
RECORDER = RUN / "documentation_snapshot/record_closed_form_progress.py"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def link(label, path, line=None):
    return "[" + label + "](<" + Path(path).as_posix() + ((":" + str(line)) if line else "") + ">)"

def ref(module, declaration):
    rel = "TGLV350/" + module + ".lean"
    lines = Path(M["sources"][rel]["snapshot"]).read_text(encoding="utf-8").splitlines()
    n = next(i+1 for i, s in enumerate(lines) if any(w+" "+declaration in s for w in ["def", "theorem", "structure"]))
    return link(module+".lean:"+str(n), ROOT / "kernel" / rel, n)

ql = lambda n: ref("DualQuadraticLaws", n)
cf = lambda n: ref("DualClosedForm", n)
assert C["all_exit_zero"] and C["full_audit_names_exact"] and C["all_axioms_allowed"]
assert F["all_exit_zero"] and F["all_hashes_match"] and F["um_matches_gate_report"]
rows=[]
for rel, row in M["sources"].items():
    record = next(r for r in C["records"] if r["module"] == rel)
    assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
    rows.append("| "+link(Path(rel).name, row["snapshot"])+" | "+str(row["lines"])+" | "+str(len(row["declarations"]))+" | "+str(record["returncode"])+" | `"+row["sha256"]+"` |")
introws=["| "+name+" | `"+row["integrated_sha256"]+"` |" for name,row in F["source_matches"].items()]
assert all(sha(Path(p).read_bytes()) == h for p,h in M["previous_reviews"].items())
recorder_raw=RECORDER.read_bytes()

report=f'''# Revisão independente — leis quadráticas e formas positivas fechadas

Data: 11/09/2026. Bancada exclusiva: `{ROOT}`.

**Parecer final delimitado [REAL]: as duas fontes Lean corrigidas e estabilizadas passaram na recompilação independente; nenhum defeito P0–P2 permanece identificado nessas provas.** Foram auditadas 23 declarações escritas e nove declarações geradas pelas estruturas, totalizando **32 alvos**, todos sem axiomas além de `propext`, `Classical.choice` e `Quot.sound`.

Há **um P2 documental** na versão inspecionada da minuta do recorder: a frase que atribui “exatamente essas leis” a `ClosedPositiveForm` inclui, por referência ao parágrafo precedente, uma lei entre operadores distintos que é provada separadamente para a família `dualQuadraticIntegral`. A precisão é detalhada abaixo. O erro de compilação da primeira versão de `DualClosedForm` foi corrigido pelo autor e a correção foi validada independentemente.

O conteúdo estabelecido é: leis de forma positiva estendida, semicontinuidade inferior, domínio finito vetorial como submódulo, subníveis fechados e invariância pelo comutante unitário da mesma álgebra. **Não se estabelece um operador auto-adjunto espectral, um cone ampliado construído em Lean, peso dual canônico, semifinitude, traço ou Three Locks.**

## 1. Achados priorizados e seu estado

### P1 histórico — erro de elaboração corrigido, não pendente

Na primeira tentativa do autor, {link('DualClosedForm.lean:105', ROOT/'kernel/TGLV350/DualClosedForm.lean',105)} usava `U.inner_map_map`, embora U tivesse o tipo de um elemento do subtipo `unitary`. O campo não era resolvido; houve exit 1 e o elaborador deixou `sorryAx` nas duas declarações dependentes. A tentativa falha está identificada pelo hash de fonte `{FAILED['sha256']}` e por {link('seu log original preservado', RUN/'author_failed_attempt/DualClosedForm_20260911_230623_951830.stdout.txt')}.

A versão corrigida usa `Unitary.inner_map_map U`. Foi congelada em bytes e recompilada nesta revisão com exit 0; o audit independente final não contém `sorryAx`. Não houve edição Lean pelo revisor. A primeira versão foi inspecionada antes da correção, mas **não foi copiada em bytes pelo revisor antes de ser substituída pelo autor**: a evidência preservada dessa tentativa consiste nos logs e no hash de fonte neles registrado. Não se apresenta essa tentativa como uma recompilação independente bem-sucedida.

### P2 documental — separar a estrutura de uma forma da lei da família de operadores

Localização: {link('record_closed_form_progress.py:129', ROOT/'record_closed_form_progress.py',129)}, na minuta do relatório ainda não executado. O parágrafo anterior enumera `q_A(c v)`, o paralelogramo e `q_(r A)=r q_A`; em seguida afirma que `ClosedPositiveForm` reúne exatamente essas leis. Contudo, {cf('ClosedPositiveForm')} tem uma única função `value : H → ENNReal`: seus campos são valor zero, homogeneidade **vetorial**, paralelogramo e semicontinuidade inferior. A homogeneidade em A vive em {ql('dualQuadraticIntegral_smul_operator')} e relaciona membros distintos da família, não sendo campo da estrutura.

Redação sugerida, sem alteração pelo revisor: **“`ClosedPositiveForm` reúne homogeneidade vetorial, paralelogramo, semicontinuidade inferior e q(0)=0; a homogeneidade em A foi provada separadamente para `dualQuadraticIntegral`.”** Isso preserva o resultado sem ampliar o contrato. O snapshot da minuta tem SHA-256 `{sha(recorder_raw)}` e está {link('preservado aqui', RECORDER)}.

No restante do texto matemático examinado da minuta, a distinção entre finitude vetorial e domínio de peso está correta: não exige densidade de `D(q_A)` para todo A positivo; reconhece que `D(q_I)={{0}}` não decide semifinitude de um peso futuro; separa invariância da forma de representação espectral e de identificação com a base. Por precisão bibliográfica, A.13 é definição, A.14 é lema e A.15 é teorema. Esta inspeção foi **estática**: o recorder não foi executado, importado ou autorizado por este parecer a escrever memórias. O seu mecanismo de gravação não foi objeto de auditoria operacional exaustiva.

## 2. `DualQuadraticLaws`: hipóteses, infinito e semicontinuidade

{ql('operatorQuadratic_smul')} e {ql('operatorQuadratic_parallelogram')} são identidades algébricas das avaliações reais de um CLM complexo. Valem para A arbitrário: a primeira usa o produto do escalar com seu conjugado, a segunda expande as duas parcelas sem hipóteses de positividade. A convenção de produto interno complexo foi respeitada.

{ql('dualQuadraticIntegrand_smul_vector')} e {ql('dualQuadraticIntegral_smul_vector')} transportam a homogeneidade vetorial para ENNReal. O fator é `ofReal (‖c‖²)`, que é não negativo e finito. As igualdades valem também para `c=0` e avaliações infinitas: a multiplicação de ENNReal usa `0 * ∞ = 0`, em acordo com a lei `q(0)=0` já existente. Não há divisão por c, exigência implícita `c≠0` ou cancelamento de infinito.

{ql('dualAmbient_real_smul')} identifica explicitamente a ação de um escalar real com a coerção complexa no mesmo operador. {ql('dualQuadraticIntegral_smul_operator')} exige **`r ≥ 0`**, embora não exija A positivo: a definição total com `ofReal` permite a multiplicação por um escalar real não negativo. Não se afirma homogeneidade para r negativo.

No paralelogramo em ENNReal, a hipótese A positivo é indispensável à prova escrita: {ql('dualQuadraticIntegrand_parallelogram')} usa `hA : 0 ≤ A` antes de cada aplicação de `ENNReal.ofReal_add`. {ql('dualQuadraticIntegral_parallelogram')} integra as funções mensuráveis e usa apenas somas e produtos distributivos; não subtrai infinitos nem conclui finitude de uma parcela a partir de igualdade entre dois infinitos. Assim, o fato de a definição de q ser total para A arbitrário não elimina `hA` das leis que a tornam forma positiva.

{ql('dualQuadraticIntegral_add_vector_le')} obtém

`q_A(v+w) ≤ 2 q_A(v) + 2 q_A(w)`

por ordem e adição em ENNReal. Essa desigualdade é suficiente para provar a estabilidade do domínio finito por soma no módulo seguinte, sem invocar Cauchy–Schwarz ou polarização ainda não construídas.

{ql('dualCutEvaluation_continuous')} demonstra continuidade da avaliação de **cada operador de corte limitado** em função do vetor, com o mesmo fator `(2π)⁻¹`. A prova reescreve o produto em ENNReal como `ofReal` de um produto real, evitando qualquer hipótese indevida de continuidade global da multiplicação em pontos `0·∞`.

{ql('dualQuadraticIntegral_lowerSemicontinuous')} exige A positivo, usa a igualdade já construída `q_A(v)=sup_n avaliação_do_corte_n(v)` e aplica semicontinuidade inferior do supremo de funções contínuas. Não pressupõe normalidade de um peso nem representação espectral da forma. A igualdade com os cortes, e não uma simples desigualdade inferior, é o que justifica a conclusão sobre q_A.

## 3. `DualClosedForm`: o que os tipos efetivamente contêm

{cf('ClosedPositiveForm')} define uma função não negativa estendida sobre todo H, valor zero, homogeneidade pelo módulo quadrado do escalar complexo, paralelogramo e semicontinuidade inferior. Não contém campos de densidade do domínio, operador auto-adjunto, medida espectral, predual ou traço. O nome `ClosedPositiveForm` designa essa apresentação por leis; uma equivalência Lean com outros tipos de forma fechada não foi construída neste incremento.

{cf('finiteDomain')} constrói de fato `Submodule ℂ H` com portador `{{v | Q.value v < ⊤}}`. Zero pertence por `map_zero`; a soma é finita pela desigualdade quadrática e por finitude de `2 q(v)+2 q(w)`; o produto escalar é finito porque `ofReal(‖c‖²)<∞`. A linearidade do domínio não é uma hipótese entregue ao construtor. {cf('mem_finiteDomain')} expõe o critério por igualdade definicional.

{cf('isClosed_sublevel')} prova `IsClosed {{v | Q.value v ≤ c}}` para cada c em ENNReal. **Isso não é `IsClosed D(q)`**: reunir todos os valores finitos não equivale a um único subnível finito, e a fonte não faz essa passagem. Tampouco contém um campo `Dense D(q)` ou uma identificação automática entre domínio finito e seu fecho.

{cf('dualClosedPositiveForm')} usa exatamente `dualQuadraticIntegral A`, com `hA : 0 ≤ A`. As leis são fornecidas pelas provas anteriores; nenhuma delas é substituída por um rótulo `Prop` sem conteúdo. O objeto vive em `RegularHilbert H`, o mesmo L² de Lebesgue utilizado pelos cortes.

Os extremos foram provados, e não postulados:

- {cf('dualClosedPositiveForm_one_domain')}: `D(q_I)=⊥`, isto é, somente o vetor zero. Para v não nulo usa `q_I(v)=∞`, incompatível com `q_I(v)<∞`.
- {cf('dualClosedPositiveForm_zero_domain')}: `D(q_0)=⊤`, pois q_0 é zero em todos os vetores.

Esses resultados não precisam de uma hipótese de Hilbert não trivial. Se o Hilbert for trivial, os submódulos ⊥ e ⊤ coincidem; não há contradição nos enunciados. Em espaço não trivial, o primeiro exemplo mostra por que não se pode exigir universalmente densidade do domínio vetorial em todo H.

## 4. Mesmo comutante, mesma álgebra e afiliação da forma

{cf('AffiliatedPositiveForm')} estende a forma por uma condição explícita: para **todo** unitário U que comuta com **todos** os B de N, `q(Uv)=q(v)` para todo vetor v. Não se limita a uma lista de geradores ou a unitários escolhidos do comutante. O campo descreve invariância da forma; seu tipo não contém um operador espectral afiliado.

{cf('dualQuadraticIntegral_commutant_invariant')} assume separadamente A positivo, A pertencente a `regularCoreAlgebra P`, U unitário e comutação com essa mesma álgebra. A prova usa a representação de q por supremo de cortes. Cada corte pertence à álgebra concreta; portanto U comuta com esse corte. Aplicar essa igualdade a v e usar `Unitary.inner_map_map U` preserva a avaliação de cada termo. A igualdade passa então ao supremo em ENNReal, sem pressupor finitude de q ou um vetor do domínio finito.

{cf('dualAffiliatedPositiveForm')} junta a forma construída e essa prova para **`AffiliatedPositiveForm (regularCoreAlgebra P)`**. As coerções e o Hilbert são os mesmos; não se introduz uma nova realização nem se troca a álgebra pelo modelo base. Em particular, invariância por N′ não é invariância automaticamente estabelecida pelo comutante, em geral maior, da imagem da base.

## 5. Fonte primária e compatibilidade conceitual — não teorema Lean adicional

[KNOWN — leitura visual] Na definição A.13, formas positivas admitem infinito e a convenção `0∞=0`. A.14 usa **`K=closure D(q)`**, com barra visível; A.15 relaciona semicontinuidade inferior à representação sobre K, sem exigir K=H. A restrição finita tem domínio D(q), denso em K; não se confunde D(q) com K. Conferi as páginas impressas 154–155 do PDF, após a captura web falhar. [Hiai, A.13–A.15](https://arxiv.org/pdf/2004.02383v1#page=154).

[DERIVED — rota compatível, ainda não formalizada] As leis construídas e a invariância pelo comutante são compatíveis com a rota de representação e afiliação do §8.1: construir K, a representação espectral e a eventual parte infinita em K⊥, então a avaliação sobre funcionais normais positivos. Isso forneceria uma ponte ao cone ampliado de N; chegar à imagem da base ainda requer identificar os pontos fixos da ação dual. Esta rota não autoriza declarar tais objetos já construídos em Lean. [Hiai, teorema 8.3 e sua prova](https://arxiv.org/pdf/2004.02383v1#page=69).

O PDF usado foi pinado por SHA-256 `{REFERENCE['sha256']}`. {link('Registro de URL e hash', RUN/'references/reference.json')}. A extração textual consultada omitia a barra sobre D(q); a leitura visual resolveu a ambiguidade. Nenhuma conclusão deste parecer assume que D(q) seja um subespaço fechado de H.

## 6. Domínio da forma versus domínio de um peso

`finiteDomain` é um submódulo de **vetores**: D(q_A) varia com um operador A fixado. Já as obrigações de semifinitude de um peso futuro concernem um domínio/ideal de **elementos da álgebra**, determinado pelos valores desse peso. A fonte não constrói esse peso nem seu ideal.

Logo, os teoremas `D(q_I)=⊥` e `D(q_0)=⊤` não decidem semifinitude. Não se deduz falta de semifinitude pela ausência de vetores não nulos com q_I finita, nem se deduz semifinitude por haver um submódulo vetorial construído. Também não se deduz que q_A tenha domínio finito denso em H para todo A positivo. Essa separação está correta na minuta, à parte o ajuste de escopo dos campos assinalado no P2.

## 7. Recompilação independente e preservação

Compilador: `{M['lean_version']}`. O manifesto registra seu hash, as dependências e o `LEAN_PATH` completo.

| Fonte recompilada | Linhas | Declarações escritas | Exit | SHA-256 da fonte |
| --- | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

Foram congeladas **{len(M['dependencies'])} dependências de projeto**, com fontes e binários identificados por hash. `DualClosedForm` foi recompilado contra o `DualQuadraticLaws` produzido pelo revisor, não contra seu `.olean` novo do pai. Os builds vivos do projeto pai e do projeto canônico não entram no `LEAN_PATH`; entram a árvore própria e os pacotes instalados em leitura.

**Base de confiança declarada:** o compilador e os pacotes, incluindo Mathlib, não foram reconstruídos nem integralmente duplicados nesta revisão. O congelamento por fonte/binário aqui declarado cobre os módulos de projeto. A reutilização dessas dependências não foi descrita como uma nova prova de cada módulo histórico.

Foram executados três processos Lean independentes: as duas fontes e `ClosedFormFullAudit.lean`. Os 32 nomes auditados são as 23 declarações escritas, mais construtores e projeções selecionados das duas estruturas. O conjunto impresso coincidiu com o esperado; todos os axiomas estão no trio permitido. Não foram realizados outros testes Lean de fronteiras abertas nesta etapa.

Evidência: {link('manifesto', RUN/'manifest.json')}, {link('comandos, exit codes e hashes dos binários próprios', RUN/'compilation.json')}, {link('tipos completos e axiomas impressos', RUN/'logs/ClosedFormFullAudit.stdout.txt')}. Os hashes das fontes permaneceram iguais durante a revisão e todos os pareceres anteriores identificados no manifesto foram preservados. A versão inicial falha permanece separada como evidência de erro do autor, não como binário aceito.

## 8. Snapshot integrado final — inspeção estática e hashes

**SHA-256 experimental conferido:** `{F['um_sha256']}`. Coincide com `integration.json` e `gate_tests.json`. O AST foi lido como dados; não se executou nem importou `um.py`.

| Fonte integrada | SHA-256 conferido |
| --- | --- |
{chr(10).join(introws)}

Os dois arquivos TGLExt coincidem com os snapshots recompilados, exceto pelos caminhos de importação; seus bytes também coincidem com as entradas do dicionário embutido. Foram encontrados {F['embedded_files']} fontes embutidos.

**Evidência do autor conferida por leitura e hashes:** {F['integrated_modules']}/{F['integrated_modules']} registros Lean com exit 0, hashes de fonte e `.olean` válidos, {F['gate_checks_count']}/{F['gate_checks_count']} controles Python marcados aprovados e {F['audit_distinct']} declarações distintas no Audit, sem axiomas além do trio. Esses totais **não são recompilações das raízes nem testes Python executados pelo revisor**: a execução independente foi a dos dois módulos e sua auditoria própria.

Em relação ao estrato 25/48/5.922, os 23 módulos anteriores conservaram os hashes de fonte e binário; as quatro novas compilações correspondem aos dois módulos e às duas raízes. Não houve remoção de fontes embutidos. Entre os antigos, somente `TGLExt.lean` e `TGL/Audit.lean` mudaram. O AST Python fora do dicionário embutido é idêntico ao backup de hash `{F['previous_um_sha256']}`; `gate_extension.py` é byte a byte igual ao desse estrato.

Foram inspecionados os controles novos `closed_form_affiliation_does_not_supply_canonical_trace` e `constructed_finite_domain_does_not_supply_semifinitude_or_three_locks`. Eles constam como aprovados no relatório do autor; a estrutura de forma não foi usada para quitar traço, canto, H1 ou testemunha total. A função legada não foi reexecutada nesta revisão e o runtime integral permanece pendente.

Evidência congelada: {link('verificação AST/hash e comparação entre estratos', FINAL/'verification.json')}, {link('compilações integradas do autor', FINAL/'integrated_compile.json')}, {link('controles do autor', FINAL/'gate_tests.json')} e {link('Audit extraído', FINAL/'axioms.json')}.

## 9. Limites finais e encerramento do escopo

[OPEN] Representação por operador auto-adjunto e resolução espectral; construção do cone ampliado e identificação com a base; peso dual canônico, seu domínio na álgebra e semifinitude; traço e sua lei de escala; Three Locks e conclusões físicas/QG. O fechamento matemático da revisão não promove essas pendências a teoremas Lean.

A inspeção delimitada dos enunciados, da composição, dos tipos, da fonte primária e do texto matemático da minuta foi concluída. A execução do recorder e a revisão operacional completa de suas gravações não fazem parte desta entrega. O ajuste documental P2 é uma recomendação ao autor e não foi aplicado pelo revisor. Este parecer não declara a documentação já corrigida.

Todas as gravações do revisor ficaram sob `revisao`: snapshots, scripts, logs, binários independentes, referência bibliográfica e este relatório. Fontes do autor, raízes, integração, monólito, originais e memórias do pai não foram alterados. Não há aprovação de QG, transposição ao canônico ou atribuição dos resultados às flags abertas.
'''

path=REVIEW/'REVIEW_DUAL_CLOSED_FORM.md'
raw=report.encode('utf-8')
backup=None
if path.exists():
    before=path.read_bytes()
    backup=path.with_name(path.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(before)
    assert backup.read_bytes()==before
temp=path.with_name(path.name+'.tmp')
temp.write_bytes(raw)
assert temp.read_bytes()==raw and temp.stat().st_size==len(raw)
temp.replace(path)
assert path.read_bytes()==raw
print(json.dumps({'report':str(path),'bytes':len(raw),'sha256':sha(raw),'backup':str(backup) if backup else None}))
