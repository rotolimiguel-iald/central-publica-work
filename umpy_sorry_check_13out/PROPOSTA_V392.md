# PROPOSTA para a v392: a detecção de sorry nos controles Lean da bancada

Gerência c1, investigador cético, 13/10/2026. **Texto de proposta. O um.py NÃO foi editado.** Base: um.py v391 `8e7b9927ceae64b8`; relatório em `RELATORIO_SORRY_CHECK.md` (nesta pasta).
Instalar, ou não, é decisão de quem sela a v392.

## Lugar exato

`prove_bench_lean_controls` (def na l.192886), dentro de `run_one`, **l.192945**:

```python
sem = [e for e in errs if e[0] > n_imp]; envbad = bool(enverr.search(out)); sorry = "declaration uses 'sorry'" in out
```

## Conserto A (mínimo, obrigatório): regex que aceita os dois formatos e lê o axioma

A regex deve ser compilada uma vez, ao lado de `enverr` (l.192915):

```python
sorry_re = re.compile(r"declaration uses [`'‘]sorry", re.I)
axdep_re = re.compile(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", re.S)
```

Na l.192945, a string fixa dá lugar a:

```python
sorry_msg = bool(sorry_re.search(out))                                            # Lean <= 4.x antigo (aspas) e 4.31 (crases)
ax_seen = {m.group(1): [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()] for m in axdep_re.finditer(out)}
sorry_ax = any("sorryAx" in v for v in ax_seen.values())                          # imune ao texto do aviso
bad_ax = sorted({a for v in ax_seen.values() for a in v if a not in ("propext", "Classical.choice", "Quot.sound")})
sorry = bool(sorry_msg or sorry_ax)
```

O critério do positivo passa a ser:

```python
ok = (pr.returncode == 0 and not errs and not sorry and not bad_ax) if kind == "POSITIVO" else (...inalterado...)
```

O registro por controle ganha os campos `"sorry_message": sorry_msg`, `"sorryAx_in_print_axioms": sorry_ax`, `"axioms_outside_trio": bad_ax` e `"print_axioms_read": len(ax_seen)`.

Por que funciona:

- A regex `[`'‘]` cobre o formato antigo (`'sorry'`) e o do Lean 4.31 (`` `sorry` ``). A fonte do 4.31, em `Lean/AddDecl.lean` l.75 e l.79, emite `m!"declaration uses `{s}`"`.
- `sorryAx` lido de `#print axioms` é a fonte de verdade que o kernel principal já usa (l.134846 e l.134864 em diante). Pega 42 dos 52 positivos de hoje, que já trazem `#print axioms`, mesmo que o texto do aviso mude de novo.
- `bad_ax` fecha também `Lean.trustCompiler`, `Lean.ofReduceBool` (native_decide) e axiomas próprios, como a l.134864 faz no kernel.

## Conserto B (preferível): decidir pelo axioma em todo positivo, não só nos 42

Para os 10 positivos sem `#print axioms` (IndependentAssemblyControls, IndependentCompatibilityControls, IndependentA2Controls, GoodAntiunitaryPhase, GoodDampingIntertwining, GoodImaginaryScaling, GoodPolarConjugation, GoodRightScaling, GoodScaledCoordinate, GoodScaledDamping), a v392 pode acrescentar ao **fonte transposto** (o `src` já reescrito na área temporária, sem tocar o corpus embutido nem o sha) um rodapé que leia o axioma de **toda** declaração do módulo. O molde é o `run_cmd` da rota `kernel.auditoria.cobertura_axiomas_73_modulos`, que o um.py já consegue ler («24002 de 24006 lidas pela regex do um.py», seq 1023):

```lean
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mod := env.header.mainModule
  for (n, _) in env.constants.map₂.toList do
    let axs ← liftCoreM (Lean.collectAxioms n)
    logInfo m!"'{n}' depends on axioms: {axs.toList}"
```

Com isso, `sorry_ax` e `bad_ax` passam a valer para os 52 positivos, por construção.
- ⚠ O rodapé muda o fonte compilado. O sha256 conferido continua sendo o do **corpus**, e a transposição deve ser **registrada** no campo `transposition`, como já se faz com `TGLV350. -> TGLExt.V350`.
- A forma exata do `run_cmd` tem de ser compilada no sandbox antes de entrar. **Não a compilei aqui** (regra desta tarefa) [OPEN].

## Conserto C (autoteste, sem rodar Lean novo): a fixture que o próprio um.py já carrega

O arquivo v361 embutido traz `TETELESTAI_V350_KERNEL_20260911/tests/probes/SorryTerm.stdout.txt` (sha256 conferido pelo índice). É a saída real do Lean da bancada para um `by sorry`:

```
...SorryTerm.lean:3:4: warning: declaration uses `sorry`
'V350ProbeSorryTerm.named' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
```

Proposta: um check fail-closed no fim de `prove_bench_lean_controls` que aplica a mesma decisão (`sorry_re` e `axdep_re`) a esses bytes e exige `sorry is True`. O check também é aplicado a uma variante da saída com aspas simples, igualmente com `sorry is True`. Se o detector voltar a ficar cego, o check acusa sem precisar compilar nada.
Texto do check: `("o detector de sorry reconhece a saida real do Lean da bancada (probe SorryTerm) nos dois formatos", fx_ok)`, entrando em `all_v`.

## Conserto D (opcional, o mesmo defeito em outro lugar)

A rota irmã `infra.bancada_um.sincronizacao_vnnn` (seq 1058, R3-A1 «RE_LOG_SORRY cego a crase») tem o mesmo defeito no script de sincronização da Bancada Um. A mesma regex vale lá. Fica fora do um.py e é decisão da frente da Bancada.

## O que NÃO muda

- O kernel principal, as 6163 pedras e o Audit não dependem da l.192945: decidem por `#print axioms` (l.134846, l.134864 em diante, l.142090).
- O gate, as flags e o selo não leem `bench_lean_controls` diretamente. Só a `kernel_condition` da coincidência conjunta V3 o lê (l.193196, l.193366), e ela hoje é True com `BOOLEAN_False`.
- Na v391 não houve falso positivo: 0 tokens de sorry no fonte dos 52 positivos (medido).

## Texto ao lado sugerido para o artigo da v392 (errata ao lado do parágrafo v362)

> Ao lado (v392): na v362–v391 o critério «sem sorry» dos controles positivos lia o aviso no formato antigo do Lean (aspas simples), e o Lean 4.31 o escreve com crases. A barreira estava cega, mas o defeito não teve efeito: nenhum dos 52 positivos tem `sorry` no fonte (medido em 13/10/2026). A partir da v392 a decisão lê os dois formatos e o `sorryAx` de `#print axioms`. O kernel nunca dependeu dessa linha.
