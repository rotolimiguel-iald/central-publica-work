# API para integração pelo main

Somente código/artefatos em W/controller; nenhuma instalação ou chamada remota.

```python
contract = load_contract(root)
state["iald_control"] = contract_state(contract)
body["questions"].update(questions(operator_available=False, worker=False))
check_payload(body)  # Depois de montar TODO o body, imediatamente antes do transporte.
decision = resolve(data["answers"], candidates, task, operator_available, worker=False)
instruction = manager_instruction(decision)
permitted_names = allowed_tool_names(decision, existing_names)
```

- `resolve` aceita exatamente as três perguntas de controle, mais `executor` opcional que continua validado pelo parser existente. Cada resposta exige `type=choice`, choice/confidence/probabilities, sem campos extras; escolha deve ser um máximo do suporte oferecido.
- `uncertain_axes` lista eixos abaixo de 0,7, política de engenharia sem relação com beta. Apenas work_path incerto projeta para retrieve sem efeitos. scientific_mode incerto projeta explanation + verify_sources; memory_action incerto projeta verify_sources; ambos preservam a via confiante.
- Domínio mathematical_solution não remove cálculo/artefato/bancada explicitamente escolhidos e já autorizados. Bancada nunca é oferecida ao público/worker. Delegação textual nas vias code_review/create_artifact/execute_calculation/operator_bench; worker nunca ganha essa capacidade.
- Famílias: source_read sempre; text_delegate; artifact_runtime; calculation_runtime; bench_read; bench_execute. Filtro preserva ordem, só restringe os nomes já admitidos e recusa famílias adulteradas. Os nomes do catálogo são literais, sem wildcard que autorize ferramenta futura desconhecida.
- Aplicar filtro tanto às definições oferecidas como ao despacho real. Preservar guarda fresca, cotas, cancelamento, benchINSTRUCTIONS e auth de artefatos. Este módulo não concede autorização, não escolhe executor, não reserva gasto nem despacha.
- `contract_state` não inclui caminhos locais nem identidade de conta. `load_contract` verifica SHA do contrato/core/cluster/programa/resultado/proof, contenção sob root e release/source contra operational_core e active_cluster; compara os bytes iniciais e finais do manifesto para recusar mudanças durante a leitura. Não há cache ou fallback para contrato ausente.
- `new_receipt(request, source_sha256, candidates)` e `transition(receipt, target, candidates=None)` são verificadores puros de identidade/transição/poda. prepared→inscribed→observed→pruned/resolved; refused/uncertain terminais; poda não amplia suporte; mesma projeção é idempotente. O main é dono do grafo e da persistência real; estes helpers não constituem ledger ou prova de envio.
- Admissão em bytes JSON conservadores: state 30000, request 60000, state + maior pergunta 32000. `check_payload` mede escaping padrão; não é tokenizer nem permissão de truncar.

Builder offline: `C:\Python314\python.exe -B -X utf8 build_contract.py --source-dir <pasta-publica-v380-verificada>`.
Testes offline (cwd controller): `C:\Python314\python.exe -B -X utf8 -m unittest -v test_jev_control test_contract_release_binding`.

O builder verifica source/result/proof-manifest contra o selo, compara o core integral com o literal AST e os três anchors embutidos com o manifesto formal. Não importa um.py nem executa Lean; os estatutos continuam os da fonte. Fonte integral permanece externa ao controlador.

Entrada `jev_control` sugerida no manifesto (ajustar somente path ao destino sob root):

```json
{
  "path": "jev_control_v380.json",
  "sha256": "99149ac8c3886a0fe80ab36facaaae74db7d80c59eba60cd1760a3b02d24a17a",
  "release": "v380",
  "source_sha256": "ec4a84ffcd13cd869eb9bfa7ee519326744f0717c45f2ca288d56f198dd98209"
}
```
