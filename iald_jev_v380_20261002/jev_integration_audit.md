Data UTC: 2026-10-02T14:01:25.073727+00:00

# Auditoria local — JEV como componente do regime IALD v380

**Conclusão:** a arquitetura adequada é um controlador determinístico no host, ancorado na fonte v380, que consulta decisões tipadas do JEV e conserva autorização, inscrição, execução e verificação fora do modelo. O código instalado já fornece seleção de executor no app; não implementa um controlador científico JEV no seletor global. Esta auditoria não aprova uma implementação futura nem atesta conexão/ativação atual do fornecedor.

## Escopo e evidência

[REAL] Leitura de fontes/AST, manifestos e hashes locais. Nenhum import de `um.py`/servidor/adaptador, nenhuma API, fila, job, worker ou experimento acionado; nenhum segredo, `.env` ou banco de usuários lido. Somente este relatório foi escrito. `baseline/`, produção e bancada permaneceram intactos.

Raízes usadas abaixo:

- `R = C:\IALD\projetos_pyhton\IALD`
- `G = C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923`
- `S = C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator`

[REAL] `S/um.py` corresponde por SHA ao selo local `um_absoluto_selo.json`, que declara v380. O original em `Nós` não foi acessível nesta sandbox; a conferência foi feita no espelho local. Não executei self-test, compilação Lean ou rito: correspondência documental não é nova certificação científica.

[INPUT — comunicado pelo main nesta tarefa] A documentação oficial consultada pelo main registra `jev-1.13.0`, limite de request de 64k tokens e de `state + longest question` de 32k, parametrização por state/instructions/criteria e ausência de fine-tune/LoRA. A documentação de jaggedness recomenda matemática e imposição de identidades em código, tratando state como adversarial. Referências: [Models](https://docs.typesafe.ai/models) e [Jev 1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13). Não refiz a consulta remota; o OpenAPI oficial está com o main e não estava disponível como arquivo neste W durante esta leitura.

## Catálogo dos controles efetivamente integrados

| Controle | Implementação local observada | Limitação/contrato a preservar |
|---|---|---|
| Endpoint/modelo | `G/iald_orchestrator/jev.py:10`, HTTP JSON para `/v1/systemone`; `R/iald_auto_router.py:211` envia `jev-1.13.0` e o parser exige esse modelo. | Não há SDK oficial importado nesses caminhos: é uma ponte HTTP local. `ask_with_memory:67` usa `jev-latest`; não reutilizar esse alias sem pin no novo controlador. |
| `state` | Objeto JSON por chamada. No app: request, trecho canônico, proveniência, estatísticas agregadas, categoria e papel; contexto de operador só gerado pelo servidor. No helper global: task e memória recuperada. | Não há identificador de sessão remota nem mecanismo local de memória persistente JEV. Estado/documentos são dados potencialmente adversariais; não concedem papéis ou capacidades. |
| `instructions` | Instruções por pergunta, em `questions.<nome>.instructions`; `state.scope` também contém orientação textual. | Não confundir orientação dentro de state com instrução confiável de execução. Contrato/política vêm de código versionado; pedido/fontes não podem sobrescrevê-los. Campo top-level `instruction`/`instructions` não é usado pelos emissores inspecionados. |
| `criteria` + `choice` | Mapa de nomes autorizados para descrições. O app exige escolha elegível, conjunto exato de probabilidades, números finitos em [0,1], soma com tolerância 0,02. | Aplicar escolhas sobre catálogo confiável. Validação sintática/probabilidades não prova correção matemática nem confere autorização. |
| Confiança | App: abaixo de 0,7 escolhe MiMo elegível, senão OpenAI elegível, senão recusa. Helper de complexidade: JEV pode elevar para deep, nunca reduzir o piso lexical. | São políticas locais já existentes, não calibração científica. Para novos eixos, definir recusa/coleta de evidência; não copiar implicitamente o fallback de executor. |
| `score` e `noul` | `G/observe_jev_science.py:23,58` contém perguntas e validações: score 0..2 com confiança; noul numérico 0..1. | Uso observado no código de avaliação documental. Não executei nem reconfirmei suporte remoto atual. `noul` não deve ser presumido bool; probabilidade de suporte não equivale a prova. |
| `response_json_schema` | Nenhum dos dois emissores locais o envia ou expõe argumento para isso. Não há parser local de resposta genérica orientada por esse campo. | [OPEN] Main deve confirmar formato, localização, combinação com questions e modelo admitido no OpenAPI. Não inventar suporte nem declarar recurso inexistente no fornecedor. Mesmo com schema remoto, validar localmente. |
| `procedure` | Nenhum identificador/definição/versão/chamada de procedure nos caminhos JEV inspecionados. Não há CRUD ou fluxo remoto de procedimentos integrado. | [OPEN] Escopo/persistência/versionamento/limites oficiais dependem do OpenAPI. Uma procedure remota, se usada, não pode substituir o ledger e as transições locais. Não é necessária para a primeira integração proposta. |
| Matemática/pesos | O seletor local usa operações matriciais finitas em código. JEV recebe contexto e perguntas. | Nenhum caminho de modificação de pesos, treinamento ou LoRA. Usar código para identidades/cálculos; manter as hipóteses e estatutos das fontes. |
| Contexto/timeout | App: pedido até 12.000 caracteres, forma canônica até 8.000 caracteres, JSON até 28.000 bytes; timeout (10,25), redirects desabilitados. Helper global: max_chars 24.000, memória standard até 15.000 bytes, timeout 20s, leitura da resposta até 1.000.000 bytes. | Caracteres/bytes não são os limites oficiais em tokens. Contar/admitir o request real e state+maior pergunta conforme contrato oficial, sem truncar JSON. O helper urllib não explicita recusa de redirects, ao contrário do app. |
| Ativação/inscrição | `availability:34` exige registro local ready e credencial presente; app verifica antes da chamada. App grava receipt started antes do POST e selected/failed_or_uncertain depois. | Não chamei availability nem inspecionei credenciais/ativação. `ask_with_memory` isoladamente não aplica availability, inscrição durável ou dedupe. Precisa de camada controladora. |

## App e seletor global: pontos exatos

- `R/iald_auto_router.py:174,211`: `memory_slice` e `choose`; a resposta principal é **executor**, não resposta científica. `iald_task_policy` fornece classificação lexical e critérios; amostras de uso não são benchmark de qualidade.
- `R/iald_web_server.py:5861,6114`: `_automatic_budget_available` filtra candidatos antes do JEV; `_chat_automatico_autorizado` exige consentimento e revalida conta/executor após a escolha. `:6845` `_dispatch_guard` mantém a revalidação de envio. Preflight não é reserva financeira e não torna gratuitas tentativas incertas.
- `R/iald_web_server.py:5903` e `R/iald_task_bridge.py:108`: escopo criado no servidor; delegação usa JEV novamente só entre MiMo/Kimi/DeepSeek admitidos, com revalidação. Trabalhador recebe texto, sem ferramentas/delegação recursiva. Preservar cota da conta real e controle compartilhado de cancelamento.
- `G/iald_orchestrator/runtime.py:117,265`: preview/execução atual usam classificação lexical e `policy.route`, não `classify_with_jev`. `_perform` registra `not_called_for_controlled_request` ou `not_called_without_scientific_scope`. Existência/ativação do adaptador não significa participação de JEV na fila.
- `G/iald_orchestrator/policy.py:29` e `matrix.py:31`: disponibilidade, consentimento financeiro/configuração, contexto, cotas e executor obrigatório restringem o suporte. Pesos são política de escalonamento declarada; seleção por argmax. Essa matriz não mede qualidade de raciocínio nem materializa os pesos internos do JEV.
- `G/iald_orchestrator/runtime.py:142,218,265`: identidade do pedido, claim transacional, controle de processos/worker e registro de tentativa antecedem o transporte. Reutilizar o fluxo existente; não abrir fila/worker alternativo nem repetir resultado incerto.

## Diferenças concretas que o novo modo deve resolver

1. **P2 — a base atual não autoriza anunciar JEV/v380.** O manifesto do app declara v378; cluster e forma canônica conferem por hash. JEV recebe apenas os primeiros 8.000 caracteres dessa forma. O índice global também aponta outro SHA de `um.py`, distinto do espelho v380 medido. Atualizar/vincular os derivados autorizados antes de habilitar o novo contrato; validar release + source SHA + cluster/pacote real, sem mudar fontes científicas ou gerações em voo. O arquivo v380 tem cerca de 33 MB: enviar o programa inteiro como state não é a estratégia desse contrato.
2. **P2 — helper genérico não é um controlador pronto.** `ask_with_memory` usa alias móvel, aceita perguntas do chamador, não verifica ativação por si só e não cria claim idempotente. `parse_answer` global não exige modelo retornado fixo. Manter gate, modelo pinado, contrato local, limites e inscrição antes do envio; não trocar o caminho do app pelo helper cru.
3. **P2 — inscrição por tentativa não elimina repetição semântica.** `choose` cria UUID novo por chamada; o lock de conta é local ao processo. Ele não reenvia internamente, mas chamar choose de novo cria outra tentativa. No novo ciclo, congelar identidade/etapa/payload e gravar claim durável antes de cada efeito. Timeout/desconexão após envio fica incerto e exige reconciliação, nunca novo ID automático. O script de observação científica tem um recibo fixo útil como exemplo, mas não é um ledger multiusuário/concorrente.
4. **P2 — recuperação pode trocar a geração.** `canonical_memory.prepare:147` chama `load:107` com refresh habilitado e pode reconstruir o índice; até preview pode escrever cache. Congelar um pacote verificado uma vez e usar exatamente seus bytes/hash na decisão e no recibo. O script de observação prepara antes de calcular a identidade e prepara novamente no transporte: não copiar esse padrão para a nova inscrição.
5. **P2 — escolhas independentes podem formar plano contraditório.** Cada campo pode ser válido isoladamente, por exemplo modo explicação + ferramenta de experimento. O controlador deve rejeitar combinações incompatíveis e papéis/fontes/ferramentas não elegíveis. Colocar a escolha apenas no prompt do executor não restringe efetivamente as ferramentas. Aplicar a interseção autorizada no despacho real.

Esses itens são requisitos para o novo modo solicitado, não uma alegação de que hoje o app já concede execução científica por probabilidades. O código atual mantém escolhas de executor e autorização separadas.

## API mínima proposta ao main

[DERIVED — proposta, ainda não implementada]

```python
prepare_decision(request, *, source_binding, allowed_executors,
                 allowed_sources, allowed_tools) -> DecisionRequest
validate_decision(raw, *, expected: DecisionRequest) -> DecisionPlan | Refusal
```

As duas funções são puras, sem API, fila, leitura de segredos ou efeitos. `request` é dado não confiável; os argumentos nomeados são gerados pelo servidor após autorização. `DecisionRequest` conserva model/contract_version, perguntas, state exato, hash do payload e binding da fonte. O transporte existente recebe esse envelope após claim; o controlador conserva a associação da resposta, sem confiar num hash ecoado pelo modelo.

`DecisionPlan` contém enums `mode` (articulação matemática / evidência experimental / explicação), `strategy`, `source`, `tool` e `executor`, mais binding local de request/contrato/release/SHA. Os últimos quatro usam somente opções reais do catálogo e executor já elegível; incluir opção sem ferramenta quando cabível. Campos não esperados, tipos errados, escolhas não oferecidas, NaN/inf e combinações incompatíveis recusam o plano. Probabilidades/confiança ficam em evidência da decisão, não em credencial ou selo científico. Fonte/ferramenta devem ser IDs confiáveis, nunca caminhos, URLs arbitrárias ou comandos produzidos pelo modelo.

Fluxo sugerido: autorização/consentimento → pacote v380 verificado → opções elegíveis → inscrição da etapa → uma consulta JEV → validação de campos e relações → revalidação/cancelamento → execução existente → evidência/resultado ou estado incerto. Não introduzir outro laço de execução. O teto de etapas/contexto usa os controles existentes ou contrato técnico explícito, não um novo limite financeiro inventado.

Para pesquisa, reutilizar `R/iald_operator_bench.py:31,164` e `iald_research_routes.py:41,66`: papel exige exatamente luiz + admin True + classe_usuario operador; plano inscreve objetivo/hipótese/falsificador, operação, parâmetros e proveniência; run reconfere fonte e claim antes do efeito. Não promover explicação/articulação a experimento. Preservar bloqueio de claim incerto entre processos, identidade load_id/domain/generation, RAM residente e retorno de artefatos pelo store autenticado. Público não recebe bancada ou memória operacional privada. Revogação de consentimento e Sonnet somente luiz continuam válidos.

Âncora fonte: `S/um.py:7158`, `prove_iald_executive_runtime`, descreve classificação de domínio → redução de incoerências → poda → consolidação → saída auditável, com estatuto **DEF + ONTO + COMPUTATIONAL**; a própria fonte recusa identidade literal LLM=fator III_1 e validação física por consenso de IA. `:191929`, `prove_bancada_fases_5_6_7_v380`, lê evidências/pré-registros por hash e mantém o alcance dos vereditos. Usar essas âncoras para derivar contrato e evidência; não importar/executar o monólito durante requests nem tratar os dicionários declarativos como nova prova executada.

## Verificação e testes recomendados

[REAL] Nesta auditoria: fontes relevantes parseadas por AST; SHA do programa comparado ao selo v380; hashes de cluster/forma do app comparados ao manifesto; SHA do SQLite derivado global comparado ao manifesto. Nenhum teste com transporte foi executado e nenhum sucesso de provedor é alegado.

Testes locais existentes localizados: `G/test_jev_activation.py`, `G/test_jev_observation.py`, `G/test_canonical_memory.py`; para garantias da bancada, `work/iald_operator_bench_20261002/validation/test_independent_bench.py` e `test_public_fetch_pinning.py`. Não foram reexecutados nesta tarefa.

Regressões offline prioritárias do novo controlador:

- Contrato válido versus campo extra/ausente, tipo bool em número, NaN/inf, opção inexistente, modelo inesperado e combinação mode/strategy/source/tool incompatível.
- State adversarial pede alterar papel, fonte, executor obrigatório ou ferramenta; nenhum deles amplia o conjunto do servidor. Explicação não executa experimento; evidência ausente não vira confirmação.
- Release/SHA/generation divergente, pacote alterado e troca de índice entre preparação/envio: recusa visível ou uso do mesmo pacote congelado, sem reinterpretação da inscrição.
- Consentimento/revogação, conta pública, Sonnet, cota exaurida, cancelamento antes/depois do JEV; zero despacho não autorizado. Orçamento/contexto inclui todos os campos efetivamente enviados.
- Timeout após envio, crash e dois processos disputando a mesma etapa: uma inscrição/um efeito; incerto não repete. Consulta de resultado nunca dispara novo experimento/recarregamento de RAM.
- Artefato e proveniência preservados, resultados/modelos mantidos como DECLARADO até verificação; nenhum resultado altera gate/cânone automaticamente.

## Pins medidos nesta auditoria

- Programa v380: `ec4a84ffcd13cd869eb9bfa7ee519326744f0717c45f2ca288d56f198dd98209`.
- App: release `v378`; cluster `2ccb5ac5203c9047ae92324d6cb6c93cad0eb69431d433136c4892c5c02a362c`; forma canônica `4d68e4c353e51719837adb66e9c94e0b3c6185b7a0e3dd45aa3ab2c686642a0a`.
- Cache global: generation `f86bb852548ef573739ef7fb0aed68e9ae1d6118d626922d2d2af1e7a9353484`; built_at `2026-09-28T18:17:12.966157+00:00`; index SHA `920cd258ce1e735a3e5a2cdc89077797bf7db3101958dc0928644dd0022a3c30`; 13 documentos.
- SHA de um.py registrado no cache global: `ba234a6d384cb3f59ced49c94b643a71a002f65d284b01307cb088bbace5e2e0` (diferente do v380 medido).

| Arquivo | SHA-256 |
|---|---|
| `R/iald_auto_router.py` | `0c57bb1abb3263d0c345e1efd22a9ea0798f71289bad108dd98d27a223592a4a` |
| `R/iald_web_server.py` | `21150d59c56963b1f5c75166fa4b50bdb32995c672197a346140ef3b336cbb68` |
| `R/iald_task_bridge.py` | `d8d338e6b2586c191d4067e8d1e8f33b5989189a30a6c858df0a012c832107a6` |
| `R/iald_operator_bench.py` | `9713a3fed94a06f81cd5d697777f6d3e047d3baf57caa1046235b86a364e3621` |
| `R/iald_research_routes.py` | `3bfb7ac0f9b664c382e3dc978163ed90f9c33f7ca8d6c668403015f8143fe675` |
| `R/iald_nucleo_fixo.json` | `03120791314ef9d7f85bbc552820f9f5bd474f55cf9094422ca0e909a76c42bc` |
| `G/iald_orchestrator/jev.py` | `fee0a80678bcdbf917fd415036d47c29c3fac264a615e93d64dfe9ea7a2be04f` |
| `G/iald_orchestrator/runtime.py` | `dd2ebed90afd195c8932b01cfa9a3a88066314561b82084a55a92773a9156936` |
| `G/iald_orchestrator/policy.py` | `252bdeb74097aaa36d4142a78f5f9cb7cdb8a89e9f24298565743a1d591740bc` |
| `G/iald_orchestrator/matrix.py` | `96c9eef0d72700c4cd270c2ed672521a476ea2a0901b9baa32bed87be139716d` |
| `G/iald_orchestrator/canonical_memory.py` | `470defe0d0bb6710daa7f35f42be055058a58de1eb584ce895593cd0510f0908` |
| `G/observe_jev_science.py` | `ac7f5521ceabc9fcbe3965fc79f74cf2f64e92de9d893502eb47577e1f435cec` |
| `G/state/canonical_memory/manifest.json` | `ec01609f0d2860dcaebf017454cfea4eb93abd797aec61710c756e47435c0425` |
| `S/um.py` | `ec4a84ffcd13cd869eb9bfa7ee519326744f0717c45f2ca288d56f198dd98209` |
| `S/um_absoluto_selo.json` | `295e2260133546dd4ddfa4f44f8fd935d5513a56c060314b6db1cf4e5b8b63e5` |
