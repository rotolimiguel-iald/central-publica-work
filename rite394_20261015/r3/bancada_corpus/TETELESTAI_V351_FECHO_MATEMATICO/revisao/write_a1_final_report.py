from pathlib import Path
import datetime, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'revisao/a1_independent_20260914_081736_089694'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(p,label):return f'[{label}](<{p.as_posix()}>)'
c=json.loads((OUT/'compilation.json').read_text(encoding='utf-8'))
v=json.loads((OUT/'verification.json').read_text(encoding='utf-8'))
assert all(c[k] for k in ['all_exit_zero','exact_targets_and_allowed_axioms','module_binary_equals_author','author_source_dependencies_inputs_preserved'])
assert all(v['own_controls'].values())
assert sha(ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean')==v['source_sha256']
previous=ROOT/'revisao/REVIEW_A1_CONTRATO_PRELIMINAR.md'
previous_sha=sha(previous)
target=ROOT/'revisao/REVIEW_A1_CONTRATO_FINAL.md'
assert not target.exists()
text=f'''# A1 — parecer independente final do marco parcial

{datetime.datetime.now().astimezone().isoformat()}

**[REAL — recompilação e auditoria próprias] Nenhum achado P0–P2 pendente no candidato delimitado. Aceitos (a) e (c); (b) permanece NÃO PAGO. A1 e a ORDEM_011 não estão concluídas.** O {link(previous,'parecer preliminar')} permanece intacto; este documento atualiza somente o estatuto do candidato final e da evidência agora disponível.

| Critério A1 | Conclusão independente |
|---|---|
| **a — contrato forte e recusa do zero legado** | **PAGO_KERNEL neste módulo.** `RegularCoreTraceData` e `legacy_zero_trace_cannot_supply` foram conferidos e recompilados. Isto não altera automaticamente o contrato legado ou seus consumidores. |
| **b — habitante concreto para todo P, ou impossibilidade de existência** | **NÃO PAGO.** Nenhum habitante foi construído; nenhuma impossibilidade de existência foi provada. Recusar zero e recusar renomear ν como τ não paga esta alternativa. |
| **c — axiomas permitidos** | **PAGO_KERNEL_AUDIT neste módulo.** Onze declarações — quatro definições auxiliares, uma estrutura e seis teoremas — conferidas por `#check` com universos e `#print axioms` próprios; somente `propext`, `Classical.choice`, `Quot.sound`. |

**Matemática e tipos.** Referência: {link(ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean','fonte final')}, linhas 15–120.

- Linhas 15–28 e 43–60: valor ENNReal no **mesmo cone positivo do core regular**, ação dual existente, ordem de operadores, soma e escala NNReal; normalidade de supremos internos de redes positivas crescentes, dirigidas e não vazias, com universo de índices explícito. Não é apenas normalidade sequencial e não recebe convergência SOT como premissa. Semifinitude é a igualdade com o supremo de **todos** os minorantes positivos de valor finito; densidade de um ideal não a substitui por definição. A lei tracial compara τ(a*a) com τ(aa*), e o sinal dual é e⁻ˢ.
- Linhas 30–37 e 62–77: unidade não nula demonstrada pelo vácuo de norma 1; fidelidade recusa o valor zero mesmo após qualquer transporte do fornecedor legado. A combinação fidelidade/semifinitude também impede a degeneração “infinito em todo positivo não nulo”. Isto não demonstra inhabitância do contrato. Não se exige τ(1) finito.
- Linhas 80–108: o peso existente ν é dual-invariante e vale **exatamente 1** no quadrado da média de comprimento 1, no mesmo vácuo. Se fosse o valor de um T escalado, teríamos 1=e⁻¹. Prova válida de incompatibilidade desse fornecedor, sem conversão de infinito em real, sem alegar impossibilidade de construir outro traço.

**Evidência própria e herança.** {link(OUT/'compilation.json','compilation.json')} e {link(OUT/'verification.json','verification.json')}.

- Candidato recompilado **rc0**, sem warnings, em {c['module']['seconds']:.3f}s; `.olean` próprio **idêntico byte a byte** ao autoral. Auditor separado com onze tipos/universos, onze listas de axiomas e impressão dos campos da estrutura: **rc0**, sem warnings, em {c['auditor']['seconds']:.3f}s. As saídas brutas estão na mesma pasta.
- As **375 dependências de projeto** foram copiadas para a árvore própria após comparar fonte, objeto e objeto de origem com `DEPENDENCIAS_A1.json`; pins preservados ao terminar. São **binários herdados** da construção anterior do autor, não 375 recompilações independentes. O LEAN_PATH de projeto aponta apenas à cópia congelada em `revisao/`; bibliotecas externas foram usadas somente para leitura, conforme o run aceito. Não reconstruí Mathlib ou o corpus anterior.
- Histórico próprio preservado: uma checagem preparatória excessiva exigiu um diretório opcional `Cli`; outra tentativa usou dois diretórios para o mesmo prefixo `TGLExt`, causando sombreamento. Corrigida a preparação, o módulo passou. A primeira saída do auditor já era verde, mas o pós-processamento recusou sufixos de universos como `Classical.choice.{{u}}`; parser normalizado e auditor reexecutado com registro explícito de rc0. Nenhum desses incidentes foi imputado à prova ou apagado.

**Auditoria autoral e controle negativo.** Li {link(ROOT/'AUDITORIA_A1.json','AUDITORIA_A1.json')}, os streams e snapshots dos seis runs registrados e a versão final de {link(ROOT/'audit_a1.py','audit_a1.py')}.

- O run aceito é `20260914_081118_098129`, com fonte idêntica ao candidato. O rc0 anterior `080951_993951` pertence a outro pin e não foi usado como aceite final. Os rc1 `080121` (preparação) e `080332` (elaboração/sintaxe, com `sorryAx`) ficam excluídos.
- O probe `081310_479904` altera o valor 1 para 2; sua fonte/snapshot/hash foram conferidos. O Lean retorna rc1 por incompatibilidade do alvo no `change` e erro derivado, com `sorryAx` nas provas afetadas. A tentativa anterior `081233_145150` falhou pelo root e **não conta como recusa matemática**. Não recompilei o probe: esta evidência é autoral relida.
- Os **oito controles** autorais foram confrontados e reproduzidos em memória, extraindo por AST somente a função pura `check`, sem executar o escritor do script. Rc não zero, entrada ausente, axioma desconhecido, duplicação e a saída do falso valor são recusados. Todos coincidem com PASS. O parser autoral basta para os onze nomes e formato desta saída; não o certifico como parser universal de logs Lean.
- A alteração de reexecução preserva `AUDITORIA_A1.json` existente e destina novas emissões a `audits/audit_<data>.json` por temporário. Não executei esse escritor nem declarei novo registro autoral. O script não fornece por si um pin completo do binário final: a comparação independente acima fecha essa verificação **para este candidato**, sem certificar futuras execuções.

**Lacuna restante, sem expansão de escopo.** {link(ROOT/'LACUNAS_A1.md','LACUNAS_A1.md')} distingue corretamente ausência de fornecedor de impossibilidade. Falta um termo `RegularCoreTraceData P` para todo P, ligado à perturbação canônica do ν fixado e à ação do mesmo core; a lei de escala isolada não seleciona normalização. A rota descrita ainda precisa das identificações de peso/grupo modular, gerador afiliado e perturbação com suas leis de normalidade e semifinitude. É obrigação de existência/ligação, não razão para reprovar (a)/(c). O fecho do grafo do peso completo com o **S original** já é fornecido por `V350ScalarWeightTomitaIdentification.scalarClosedTomita_graph_eq_weight` (nome no namespace `TGLV350.Regular`); não é exigido novamente, nem se presume igualdade dos ideais algébricos. A futura adaptação ao consumidor legado do core/ThreeLocks permanece fora deste marco.

**Pins lidos por script:**

| Artefato | SHA-256 |
|---|---|
| Fonte final | `{v['source_sha256']}` |
| `.olean` autoral = próprio | `{v['binary_sha256']}` |
| `AUDITORIA_A1.json` | `{v['author_audit_sha256']}` |
| `audit_a1.py` final | `{v['author_audit_script_sha256']}` |
| `LACUNAS_A1.md` | `{v['pins']['LACUNAS_A1.md']}` |
| Compilação independente | `{sha(OUT/'compilation.json')}` |
| Verificação independente | `{sha(OUT/'verification.json')}` |
| Cópia `um.py` preservada | `{v['pins']['um.py']}` |

Somente `revisao/` recebeu saídas. Não houve implementação autoral, integração, execução/importação de `um.py`, promoção de gate, atualização de memórias/Atlas ou alteração de pareceres anteriores. Não há análise pendente deste candidato; **o marco parcial a/c está aceito e b continua aberto**.
'''
# Correct module-vs-namespace wording before publication.
text=text.replace('`V350ScalarWeightTomitaIdentification.scalarClosedTomita_graph_eq_weight` (nome no namespace `TGLV350.Regular`)','`TGLV350.Regular.scalarClosedTomita_graph_eq_weight`, em `V350ScalarWeightTomitaIdentification.lean`')
data=text.encode('utf-8');tmp=target.with_name(target.name+'.tmp')
tmp.write_bytes(data);assert tmp.stat().st_size==len(data);tmp.replace(target)
assert sha(previous)==previous_sha
print(json.dumps(dict(report=str(target),sha256=sha(target),bytes=len(data),previous_preserved=True),ensure_ascii=False))
