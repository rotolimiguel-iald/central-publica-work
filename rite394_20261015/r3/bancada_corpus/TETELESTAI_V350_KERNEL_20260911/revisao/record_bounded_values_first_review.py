"""Record only the first bounded-values review stratum; no author code execution."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/"bounded_dual_values_latest_run.txt").read_text(encoding="utf-8"))
M=json.loads((RUN/"manifest.json").read_bytes())
C=json.loads((RUN/"compilation.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert all(C[k] is True for k in ["complete","all_exit_zero","full_audit_names_exact","all_axioms_allowed","sources_unchanged","dependencies_unchanged","previous_reviews_preserved"])
assert len(M["declarations"])==len(C["records"][-1]["axioms"])==10
src=M["sources"]["TGLV350/BoundedDualValues.lean"]
assert sha(Path(src["path"]).read_bytes())==src["sha256"]
custody_raw=(ROOT/"semifinite_ideal_custody.json").read_bytes()
custody=json.loads(custody_raw)
previous=REVIEW/"REVIEW_REGULAR_SEMIFINITE_ROUTE.md"
assert sha(previous.read_bytes())==custody["review_sha256"]
with (RUN/"previous_semifinite_ideal_custody.json").open("xb") as f:f.write(custody_raw)
lines=Path(src["snapshot"]).read_text(encoding="utf-8").splitlines()
line_numbers={m.group(1):i+1 for i,l in enumerate(lines) if (m:=re.match(r'^theorem ([\w]+)',l))}
stamp=datetime.datetime.now().astimezone()
meanings={
"selfAdjoint_le_of_quadratic_le":"Ordem positiva determinada pelas leituras quadráticas de dois auto-adjuntos.",
"selfAdjoint_eq_of_quadratic_eq":"Igualdade pela antissimetria dessa ordem.",
"positive_le_scalar_of_quadratic_bound":"Cota quadrática real implica A ≤ C·I.",
"normalizedDualCut_le_of_uniform_bound":"q_A ≤ ofReal(C‖v‖²), C≥0, implica cada corte normalizado ≤ C·I.",
"exists_boundedDualCutLimit":"Constrói B≥0 em N, B≤C·I, limite forte e supremo ambiente dos cortes.",
"quadratic_le_of_operator_le":"A ordem operatorial implica ordem das partes reais quadráticas.",
"dualQuadraticIntegral_eq_boundedCutLimit":"Representa a integral estendida pela leitura do limite construído.",
"boundedDualValue_unique":"Unicidade entre representantes positivos que concordam em todos os vetores.",
"boundedDualValue_dual_fixed":"O representante positivo é fixado pela mesma ação dual.",
"exists_boundedDualValue_in_fixedCore":"Compõe as provas para obter o representante positivo em F, sem ht/hL como premissas."
}
table='\n'.join(f'| {line_numbers[n]} | `{n}` | {s} |' for n,s in meanings.items())
rec0,rec1=C["records"]
report=REVIEW/"REVIEW_BOUNDED_DUAL_VALUES.md"
assert not report.exists(), "Existing report requires a separate byte-preserving addendum, not replacement."
text=f'''# Revisão independente — valores duais limitados

## Estrato 1 — {stamp.isoformat(timespec="seconds")} — BoundedDualValues

**[REAL] Exame do primeiro módulo concluído, sem achados P0, P1 ou P2. Parecer conjunto ainda PENDENTE de `BoundedFiniteSquares` final e da integração deste novo lote.** Não se usa o parecer da etapa anterior como prova dos novos enunciados.

Escopo efetivamente examinado: as dez declarações de `kernel/TGLV350/BoundedDualValues.lean`, seus tipos elaborados, provas e composição, com leitura dirigida das dependências congeladas. O teorema final representa a forma dual uniformemente limitada por um operador positivo limitado da mesma álgebra fixa F. A cota **∀v, q_A(v) ≤ ofReal(C‖v‖²)**, com um único C≥0, e A≥0 pertencente a N são hipóteses explícitas. Este estrato não aplica ainda o resultado ao ideal da etapa anterior.

### Tipagem e pontos adversariais conferidos

O espaço é `RegularHilbert (TowerHilbert P) = Lp (TowerHilbert P) 2 (volume : Measure ℝ)`, na realização regular já construída. A, seus cortes e B são operadores contínuos complexos nesse mesmo espaço; N=`regularCoreAlgebra P` e F=`dualFixedCore P` usam o mesmo P. Não aparece troca de representação, projeção finita P_F, subespaço de suporte ou escolha de um domínio próprio para contornar vetores de valor infinito. A cota vale no Hilbert regular inteiro.

| Linha da fonte dev congelada | Declaração, namespace `TGLV350.Regular` | Conteúdo conferido |
|---|---|---|
{table}

**Ordem e positividade.** As primeiras provas usam positividade de B−A e simetria da parte real do produto interno; não confundem a convenção complexa de conjugação com uma forma bilinear real. A reconstrução da ordem/igualdade exige auto-adjunção explícita. `positive_le_scalar_of_quadratic_bound` não exige C≥0 isoladamente, pois sua própria cota é a premissa; o resultado aplicado aos cortes e os existenciais finais exigem hC. O escalar real C atua sobre o operador complexo por sua coerção usual, cuja auto-adjunção é verificada. Não se exige positividade estrita.

**Cortes e existência.** Os cortes são os efetivos `normalizedDualCut n A`, com o fator de Haar fixado anteriormente, não uma família substituta. Positividade, monotonicidade em n e a cota C·I fornecem uma cota de norma uniforme. `TGLExt.MonotoneOperatorLimit.monotone_operator_limit` (namespace declarado `ChatgptAudit.Expectation047`, linha 223 da dependência) constrói o limite forte e seu IsLUB ambiente. O índice é ℕ com `atTop`, dirigido e não vazio; a pertença a N usa o fechamento WOT via `vonNeumann_mem_of_strong_limit`, cujo filtro exige NeBot, aqui satisfeito. Não há circularidade por supremo interno nem limite forte assumido no existencial final. O IsLUB dá B≤C·I. Trata-se de convergência forte vetor a vetor, não de convergência na norma operatorial; a cota de norma tem apenas o papel de construir o limite.

**Integral estendida e domínio.** A igualdade q_A(v)=ofReal(Re⟨v,Bv⟩) combina a exaustão já provada por supremo dos cortes normalizados com a continuidade de `inner`, `Complex.re` e `ENNReal.ofReal`. As duas desigualdades são justificadas: cada leitura de corte é ≤ à de B pelo IsLUB, e o limite das leituras permanece ≤ ao supremo. O lema intermediário recebe ht/hL, mas a composição final os fornece, não os transfere para o usuário.

As duas ocorrências de `toReal` são legítimas e foram lidas: na cota dos cortes, o limite superior é `ofReal(C‖v‖²)≠⊤`, com não negatividade explícita dos dois argumentos reais; na unicidade, aplica-se `toReal` a uma igualdade entre dois valores `ofReal` finitos, e a positividade dos representantes permite recuperar as partes reais sem truncamento. Não há uso de `toReal` para apagar um q_A(v)=∞. A igualdade obtida mostra finitude para todos os vetores sob hbound; isso não equivale a provar semifinitude de um peso na álgebra. A unidade de integral infinita em vetores não nulos continua compatível: ela não satisfaz essa hipótese de cota.

**Unicidade e álgebra fixa.** `boundedDualValue_unique` compara dois operadores positivos com a mesma leitura em **todos** os vetores; não infere operador zero de um único vetor. A unicidade é um teorema separado, que compõe com o existencial, e não um campo `ExistsUnique` embutido no último enunciado. A invariância usa θ_s(B)=D_s B D_−s e lê sua forma em D_−s v, com o sinal negativo correto em `operatorQuadratic_conjugate`. A invariância vetorial da mesma q_A, já estabelecida, e a unicidade dão θ_s(B)=B. Junto com B∈N, `dualFixedCore_mem_iff` dá B∈F. A identificação usada é F=N∩{{D_s}}′; não se presume F=base original.

### Recompilação e auditoria próprias

Fonte final lida, congelada e recompilada: **{src['lines']} linhas**, SHA-256 **`{src['sha256']}`**. Log do autor confrontado com fonte e binário antes da recompilação: `{Path(src['author_log']).name}`, rc0, fonte inalterada. Esse log é evidência do autor, distinta dos dois processos abaixo.

Ambiente independente em [manifest.json](<{(RUN/'manifest.json').as_posix()}>): **{len(M['dependencies'])} dependências de projeto** com fontes e `.olean` copiados de snapshots anteriormente verificados, hashes conferidos antes/depois; nenhum pacote ou dependência foi recompilado. `LEAN_PATH` aponta primeiro para o build próprio e depois para bibliotecas de pacotes somente para leitura, excluindo os dois builds de projeto do autor. Saídas e TMP/TEMP estão dentro desta pasta de revisão.

Compilador: `{M['lean_version']}`; SHA-256 do executável lido `{M['compiler_sha256']}`.

| Processo executado pelo revisor | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
| BoundedDualValues.lean | rc0; 10 alvos | {rec0['seconds']} s | `{rec0['output_sha256']}` |
| BoundedDualValuesFullAudit.lean | rc0; #check e #print axioms dos 10 nomes exatos | {rec1['seconds']} s | `{rec1['output_sha256']}` |

O binário próprio do módulo coincide em hash com o binário dev do autor. Auditor próprio SHA de fonte `{rec1['source_sha256']}`. Todos os dez alvos dependem somente de `propext`, `Classical.choice`, `Quot.sound`; não há `sorryAx`, `trustCompiler` ou axioma customizado na auditoria transitiva desses alvos. O stdout do auditor foi lido para conferir as hipóteses elaboradas, além da contagem. [compilation.json](<{(RUN/'compilation.json').as_posix()}>) registra complete/all_exit_zero/exact names/axioms/sources/dependencies/reviews preservados, todos verdadeiros.

Histórico preservado: a tentativa inicial em `bounded_dual_values_independent_20260912_042044_591942` terminou rc1 por inacessibilidade do prefixo Mathlib no sandbox, antes de elaborar as provas. A execução seguinte concedeu leitura aos pacotes existentes e passou, sem alteração da fonte. Esse erro de ambiente não é um defeito pendente do módulo. Nenhum runtime, monólito, teste Python, recorder ou verifier do autor foi executado.

### Preservação e pendências deste parecer

`semifinite_ideal_custody.json` foi lido: timestamp `{custody['timestamp']}`, SHA `{sha(custody_raw)}`. O parecer anterior `REVIEW_REGULAR_SEMIFINITE_ROUTE.md` coincide com seu `review_sha256`: **`{sha(previous.read_bytes())}`**, e permanece intocado. Não reexecutei o verificador de custódia; o rc0/16 prefixos é informação do autor. Todos os demais pareceres anteriores também permaneceram com os hashes registrados no novo manifest. Escrita exclusivamente em `revisao/`; sem edição de fontes Lean, originais, monólito ou memórias. Este novo parecer nasce por escrita temporária verificada e substituição; adendos posteriores exigem backup imediato dos bytes e preservação integral do prefixo.

**Pendente para conclusão conjunta:** revisar/recompilar `BoundedFiniteSquares` final, cuja disponibilidade foi comunicada durante a redação deste estrato, auditar seus alvos e conferir a integração/minuta/evidências finais do lote quando disponibilizadas. Não atribuo a este novo incremento as contagens de compilações, testes ou Audit do pacote anterior, nem certifico integração ainda não inspecionada.

**[OPEN]** F=base, representação geral espectral/predual, peso operatorial padrão e suas obrigações de semifinitude, estado/gerador/perturbação e traço canônico, Three Locks/H1–H3, física, contrato ampliado e runtime integral. A representação agora provada para formas duais uniformemente limitadas é um avanço específico; não prova essas obrigações restantes nem altera flags. Nenhuma análise do primeiro módulo permanece pendente, mas a revisão conjunta permanece aberta.
'''
raw=text.encode('utf-8'); tmp=report.with_name(report.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and len(raw)>0
tmp.replace(report)
assert report.read_bytes()==raw
receipt={"timestamp":stamp.isoformat(),"report":str(report),"report_sha256":sha(raw),"report_bytes":len(raw),"first_module_review_complete":True,"joint_review_complete":False,"findings_P0_P1_P2":[],"independent_compilations_rc0":2,"exact_audited_targets":10,"source_sha256":src['sha256'],"previous_custodied_review_preserved":sha(previous.read_bytes())==custody['review_sha256']}
with (RUN/'first_review_receipt.json').open('xb') as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
