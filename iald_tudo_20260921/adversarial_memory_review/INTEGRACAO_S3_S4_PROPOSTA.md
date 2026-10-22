# Proposta S3/S4 — não integrada, aguarda revisão independente

Entregas: `haiku_s3_s4_proposal.py` (drop-in puro) e `test_haiku_s3_s4_proposal.py` (testes focais). Nenhum módulo existente, stage, ROOT ou memória foi modificado. O construtor não aprova esta proposta. S1/S2 continuam com o pai.

## Contrato do hash

`prepare_haiku_package.py` copia `count['native_tools_sha256']` para o manifesto. Em `count_native_reviewed_draft.py`, esse hash é calculado sobre `wire['tools']`, resultado de `converter_pedido`, com:

```python
hashlib.sha256(json.dumps(wire['tools'], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
```

UTF-8; separadores padrão com espaços; ordem do array preservada. NÃO é hash dos wrappers OpenAI `{type:'function',function:{...}}`. É hash dos objetos nativos `{name,...,input_schema:...}`, incluindo flags presentes nessa lista, como `eager_input_streaming`. O adaptador de contagem remove essa flag só na cópia destinada a count_tokens; conferir hash ANTES desse filtro. Não remover flags para fazer o hash coincidir.

O teste extrai por AST a expressão do builder sem importá-lo e compara sua execução com o serializer proposto, em schemas sintéticos com Unicode. Confere também os vínculos manifesto/recibo, incluindo orçamento e nomes. Os recibos locais não armazenam o conteúdo dos sete schemas: não foi recomputado o hash real das definições de ROOT (acesso proibido nesta tarefa). A conferência real abaixo é condição para a integração, não resultado alegado destes testes.

## S4 — montagem e envio

Importar no futuro stage, depois da revisão, `attach_openai_tools`, `CheckedAdapter`, `verify_native_tools`, `load_snapshot`, `status_response`, `HaikuUnavailable`. O arquivo novo não altera módulos existentes automaticamente.

1. Manter `permitidas` na ordem atual: kernel + fontes públicas + core indexado. Devem existir exatamente sete nomes únicos: os constantes em `PUBLIC_NAMES`. Preservar definições integrais; não reconstruir descrições ou parâmetros à mão.
2. Ao obter `haiku_package`, obter junto `snapshot` com `load_snapshot(diretorio_controlado_pelo_servidor, load_package)`. Essa função cruza orçamento e hashes com o retorno do loader e relê o manifesto para detectar alteração durante a leitura. Nenhum diretório vem do pedido HTTP.
3. Logo após montar `base` e ajustar `max_completion_tokens`, ANTES de `tokens_para_saldo`, aplicar:

```python
if haiku:
    base = attach_openai_tools(base, permitidas)
    if not usar_agente:
        base['tool_choice'] = 'none'
```

Assim, a ramificação direta também leva os sete schemas. `usar_agente` controla execução/chamadas, não existência dos schemas. A função preserva o payload original e `tool_choice`, recusa uma lista existente conflitante e nunca a sobrescreve silenciosamente.

4. Antes de count_tokens de pré-checagem financeira, converter pelo mesmo adaptador verificado:

```python
checked_adapter = CheckedAdapter(iald_motor_claude, snapshot)
wire = checked_adapter.converter_pedido(cfg, payload, prefixo=prompt_externo)
# Continuar a transformação Haiku de thinking/output_config existente.
# Não modificar wire['tools'] depois da verificação.
```

5. Na closure `enviar` Haiku, passar `checked_adapter` em vez de `iald_motor_claude` a `post_guarded`. É a conversão FINAL dentro do guard que precisa validar o hash. Verificar apenas uma amostra antes da reserva seria insuficiente. O proxy delega todos os demais atributos ao adaptador original; não constrói cliente nem chama API. Não alterar o caminho Sonnet/OpenAI.
6. Em TODAS as voltas do agente, inclusive na última/sem ferramentas permitidas, preservar os sete schemas. Onde o agente remove `tools` para impedir novas chamadas, trocar essa operação por `tool_choice='none'` mantendo a lista. Não usar `attach_openai_tools` para esconder uma alteração de lista já existente. O proxy recusa schemas ausentes/alterados na conversão final; o erro deve ser apresentado, sem fallback nem geração.
7. Em preflight, tratar `HaikuUnavailable` como indisponibilidade visível (JSON503 nas rotas JSON; aviso SSE explícito no chat), antes de reservar/gerar quando possível. No guard final, a exceção é ValueError e fecha o envio; se já houver reserva, sua liberação pertence ao fluxo financeiro do pai. Não mascarar a falha como sucesso. Registrar o identificador estável da falha (`native_tools_sha256_mismatch`, etc.) em diagnóstico interno sem conteúdo das ferramentas/credenciais.

`tool_choice='none'` (OpenAI) e `{'type':'none'}` (nativo) são aceitos pelos helpers. Eles não transformam o choice, tarefa do conversor existente. A integração deve conferir que esse conversor preserva os schemas ao converter `none`; se os retirar, o proxy recusará visivelmente. Não se afirmou ter testado essa conversão real nesta tarefa sem ROOT.

## S3 — contexto e limites/status

Usar um callback autorizado `load_checked_snapshot()` que:

1. Resolve a conta e configuração por `CLAUDE_ROUTES.configuration`, sem aceitar flags/modelo enviados pelo cliente.
2. Obtém pacote+snapshot com `load_snapshot`.
3. Monta as sete definições atuais em um payload de referência com `model=cfg.modelo`, `max_completion_tokens=4096`, sistema `package.prefix`, usuário `'.'` e `tool_choice='none'`; aplica `attach_openai_tools`.
4. Converte esse payload via `CheckedAdapter(...).converter_pedido(..., prefixo=package.prefix)`; somente conversão local, SEM count_tokens, SDK ou envio. A verificação do hash abrange o array nativo produzido. Retorna o snapshot.

Em `/api/contexto`, desviar o Haiku selecionado ANTES de `janela_do_plano` (que impõe32768 ao gratuito). Reconhecer a seleção gravada mesmo se o pacote estiver fora do ar; não tentar construir a configuração fora do tratamento de indisponibilidade. Para seleção Claude legada sem `modelo_claude`, conservar a resolução já definida: Luiz→Sonnet; demais→Haiku. Sessão/conta bloqueada continuam sob a autorização existente.

```python
if selected_is_haiku:
    return status_response(load_checked_snapshot, jsonify)
# Demais motores: preservar implementação existente.
```

O helper retorna `(jsonify(...), 503)` em falha de arquivo/pacote/configuração/hash e não expõe caminhos da exceção. O sucesso fornece `n_ctx=janela=200000`, unidade Anthropic, memória e orçamento lidos do manifesto. Para o manifesto conferido: memória183135, requisição de referência184609, resposta4096, margem1024, reserva dinâmica de referência10271. A referência inclui mensagem mínima na medição permanente; perfil/nota/histórico/tool results atuais não são medidos aqui. `saldo_conversa_atual_tokens=None` é intencional. Nenhum status chama count_tokens.

Para `_limites_da_conta` e `/api/motor`, usar o MESMO callback/snapshot, por exemplo `status_response(load_checked_snapshot, lambda d:d, limits=True)`. Se o status for503, propagar JSON503 no endpoint que o contém: não inserir uma tupla como valor de `limites` nem publicar `disponivel:true`. Em sucesso, mesclar os campos devolvidos aos limites Haiku existentes; preservar cotas/autorizações de execução e imagens. `pensar=False` reflete thinking desativado; sete schemas presentes não concedem execução de ferramentas ao usuário nem elevam privilégios. Se o pai mantiver `agente` restrito pelo plano, preservar esse campo.

O helper não afirma conversão de caracteres para tokens Anthropic: `cpt=None`. O consumidor de `/api/contexto` precisa tratar isso explicitamente e não fazer aritmética/divisão com `None`; usar contagem nativa no envio como autoridade. Não substituir o saldo dinâmico medido por200k para estimar história no cliente. Este ajuste do consumidor é uma dependência de integração visível, não foi aplicado nesta proposta.

Na rota de status/admin, adicionar bloco por perfil Haiku com `status_response(..., limits=True)`, incluindo indisponibilidade e hashes; manter o bloco Sonnet/base rotulado como tal. Não substituir totais de gasto/reservas por orçamento de contexto. Preservar `require_admin`, autenticação e consentimento. O callback de status administrativo deve resolver o perfil autorizado correspondente, não inferir que o modelo base é o escolhido por toda conta.

## Validação e limites

Executar `python -B -X utf8 test_haiku_s3_s4_proposal.py` dentro desta pasta. Somente biblioteca padrão, sockets bloqueados; não importa builders nem servidor. Os10 testes cobrem serializer exato, cadeia de recibo, metadata, limites, JSON503, tipagem/orçamento, sete schemas comnone, deriva de schema/ordem/flags, distinção OpenAI/nativo e proxy de conversão final. Não repetem o teste completo do pai.

Esta entrega é construção para revisão independente, não aprovação de integração, preços, produção, semântica da memória, contagem Anthropic nova ou comportamento do conversor ROOT. O pai deve incorporar os pontos acima ao seu stage e testar suas rotas/voltas reais; S1/S2 não foram tocados.
