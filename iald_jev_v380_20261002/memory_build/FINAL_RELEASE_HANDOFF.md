# Handoff final — memória v380 e checks de contexto/gasto

[REAL — verificações locais encerradas; implantação pertence ao main]

Release científica: **v380**. Prefixo, cluster, fontes, catálogos, manifestos e scripts do build continuam congelados após a correção revisada. Nenhuma chamada remota adicional, leitura de credencial/configuração secreta, acesso ao razão real ou escrita em produção nesta verificação.

## Pins finais

| Artefato | SHA256 |
|---|---|
| Programa custodiado | `ec4a84ffcd13cd869eb9bfa7ee519326744f0717c45f2ca288d56f198dd98209` |
| Cluster | `ef1678bcad68a6669b119ef4d2f54f8cb662021dc53b0ed84968c2c48f140824` |
| Haiku, 181836 tokens permanentes | `24bf213dc912409c40ddf0d0a23e0ba3cbf23024656dbc972bbb85c56c227b13` |
| Manifesto staged | `89a2f581293f1f947219f58a63e54e1ab3c7fa2a009b410c5a985251b55e2fe7` |
| Manifesto install | `95e3eb0ebaedf4d2e4a577585704568383b8cc568a204d504e5562db2e2c5223` |
| Pacote Haiku runtime/manifest.json | `1f148fa2cb3e7822130da4085512a9e842e7062fbbac101bae3888aadc9087b7` |

Contagem real obtida pelo main: `count_20261002_113914_901730.json`. Entrada de referência **183310**, saída reservada **4096**, margem **1024**, folga **11570** na janela **200000**. `load_package` + `snapshot_from_manifest` reais validaram offline o pacote final; nenhuma nova contagem foi chamada. Não transferir essa medida aos tokenizers de outros provedores.

A referência 183310/11570 pertence ao recibo do pacote; não é uma medição da nova diretiva de cada chamada. `routing_instruction` é conteúdo dinâmico posterior ao prefixo e entra no contador nativo por pedido. Nesta regressão, o contador falso acrescentou 37 tokens sintéticos para verificar o aumento da reserva; esse número NÃO é contagem Anthropic real. Prefixo e recibo originais permanecem intactos.

## Verificações concluídas

- **21 testes locais da memória** (11 integração + 10 codec), **56/56 da revisão independente**, **7/7 adicionais de orçamento/contexto**.
- 362 tópicos, v5 integral, núcleo anterior byte a byte com adendo atual, forma canônica integral e catálogo 1209/1209 fontes. Os 15 valores nos três mapas de vereditos novos estão inline no cluster/Haiku. Provas completas e detalhes referenciados continuam recuperáveis; contexto projetado não significa corpus inteiro inline nem instalação em pesos.
- [ATUALIZAÇÃO — revisão restrita de routing_instruction] A igualdade AST integral de `_chat_avaliacao`/`_chat_externo` registrada anteriormente é histórica. O main acrescentou o argumento keyword `routing_instruction=None` e, em cada função, um único append à nota/instrução quando `routing_instruction` está presente e `task_scope is None`. Removendo exatamente essas duas adições de cada AST, o corpo remanescente coincide com a base anterior: montagem, `check_window`, contagem e reservas posteriores não foram alterados. Esta revisão não aprova mudanças fora dessas duas funções.
- MiMo/DeepSeek/Kimi continuam recebendo o pacote Haiku verificado. MiMo/DeepSeek executam `check_window` sobre o corpo final em cada volta e reservam antes do HTTP; o Kimi verifica o JSON final encapsulado antes do cliente oficial. Nenhum prefixo foi truncado.
- O orçamento público de MiMo/DeepSeek reserva entrada sem cache pelo limite UTF-8 conservador + saída máxima. Recusa impede o HTTP; encerramento sem uso mantém a reserva inteira. A pré-seleção consulta exaustão com reservas ativas; a admissão definitiva continua sendo a reserva imediatamente anterior ao envio.
- Haiku usa a contagem nativa do pedido final e o grupo `haiku_public`; mantém margem de reserva financeira e de contexto. MiMo/DeepSeek usam seu razão/grupo existentes `mimo_public`, separado do Haiku. Isso preserva a política atual; não significa que esses gastos sejam um único grupo global.
- Nenhum teto novo para Luiz/MiMo/Kimi. Saldo e parâmetros financeiros reais não foram lidos: os testes usam cotas sintéticas e provam recusa/isolamento, sem declarar disponibilidade financeira da conta real.

## Payloads de referência medidos localmente

MiMo/DeepSeek: prefixo final + nota de serviço/diretiva sintética de roteamento + mensagem sintética + 14 ferramentas públicas/de tarefa. Kimi: esse prefixo com diretiva + mensagem e recuperação sintética de 24000 caracteres Unicode. A diretiva acrescentou 83 bytes ao JSON MiMo/DeepSeek e está incluída na reserva. Os montadores reais de OpenAI/Sonnet/Haiku também preservaram a diretiva, sem duplicá-la quando já há task_scope. Os números abaixo seguem exatamente a fórmula conservadora de `check_window` (bytes JSON + reserva de saída + 4096), não contagem nativa desses provedores. Novos históricos, perfis, instruções de bancada ou resultados de ferramentas exigem o mesmo check a cada pedido.

| Provedor | Entrada UTF-8 JSON | Reserva de saída | Folga conservadora | Reserva USD calculada pelo código de referência |
|---|---:|---:|---:|---:|
| mimo | 505345 | 131072 | 408063 | 0.333857715 |
| deepseek | 505362 | 393216 | 145902 | 0.623467800 |
| kimi | 585245 | 131072 | 328163 | assinatura; política preservada |

Os valores em USD são reservas conservadoras com as tarifas do código e saída máxima; não são faturas nem leitura de saldo. Orçamento inferior à reserva é recusado antes do transporte. O teste inicial teve uma configuração sintética incompleta para Haiku, corrigida no fixture; nenhum arquivo de runtime mudou.

## Recibos e integração

- Entrega READY e mapa de 1224 arquivos: `C:\IALD\Central de Patentes\work\iald_jev_v380_20261002\memory_build\delivery_20261002_115012_880732.json`; SHA256 `130087265017bd92c3b3abede92d19c303394ec51839079b7a5e42af8bbcd3e6`.
- Checks atuais 7/7, incluindo routing_instruction: `C:\IALD\Central de Patentes\work\iald_jev_v380_20261002\memory_build\provider_checks_20261002_120542_740846.json`; SHA256 `2d5834d512d7d6f8c4354fcedbafac1dc3c8463ada72cf5182c4e66721f3fdf6`. O recibo anterior permanece como história, sem representar o novo diff.
- Revisão independente 56/56: `C:\IALD\Central de Patentes\work\iald_jev_v380_20261002\validation\memory_review.json`; SHA256 `010c3a1c2e09a0204aa08c4aecb3159bced57884e00b7d5164841bfe50feac21`.
- Contagem nativa real do main: `C:\IALD\Central de Patentes\work\iald_jev_v380_20261002\count_20261002_113914_901730.json`; SHA256 `d974af5d7776b478acede790cfef08c10aa71b9d3c810b2923fc356a8ce703d2`.

O main já preparou `memory_stage/haiku_runtime`. Usar o mapa de instalação do recibo READY e `manifest_install.json`; o controller e sua integração são responsabilidade do main. O pacote não executa deploy nem altera contas/RAM. Não copiar backups/recibos antigos como ativos. Quiet, baseline, backups e validação ao vivo continuam no instalador principal.

Repetição autorizada somente offline: `C:/Python314/python.exe -X utf8 -B memory_build/test_provider_budget_context.py`. Não reexecutar o builder nem modificar bytes congelados sem novo achado e coordenação com o main. Orquestração global permanece separada.

## Congelamento após a revisão da diretiva

Servidor staged lido nesta regressão: SHA256 `00caa7a36f4447634005ab5c4a59bd4c7bbd40f7ddfb85e36e9a0f481261b4f7`. Teste atualizado: SHA256 `e9d49c349c69c090cd6c2cb95029f30980e29ccf0ea180c3d03386a451357187`. Nenhum arquivo de servidor, controller ou memória foi editado por esta revisão; somente teste, novo recibo e este handoff. Nada foi enviado a provedores.
