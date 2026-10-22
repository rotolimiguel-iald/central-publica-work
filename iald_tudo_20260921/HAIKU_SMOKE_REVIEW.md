# Smoke Haiku — entrega offline para revisão

Estado: draft offline; execução paga NÃO validada nem autorizada. ROOT, contas, flags e memórias não foram alterados. Nenhuma rede/API, credencial, .env ou usuário real foi lido nesta execução.

## Arquivos e execução

- `haiku_smoke_review.py`: dry-run por padrão. `--execute` sempre recusa antes de importar módulos ROOT, inclusive combinado com `--prepare-wire`.
- `--prepare-wire`: montagem local com Config real sem credencial, assemble, CheckedAdapter e conversor instalados; valida pacote e hash nativo das sete ferramentas. Não instancia SDK, conta, razão ou guarda. Produz arquivos wire contendo memória pública; o recibo preflight.json contém somente hashes/metadados. Não enviar esses arquivos automaticamente.
- Preparação concluída em `haiku_smoke_preflight_20260922_191838_601528`: duas solicitações independentes, none, saída512, cache5m. A segunda NÃO é a segunda volta real: essa depende da resposta futura e exige nova contagem do payload final. Configuração sintética explícita não atesta configuração viva do servidor.
- `test_haiku_smoke_review.py`: 11 testes sintéticos passaram, incluindo oito threads disputando duas reservas, limites0.325/0.65, preservação de cotas, hold incerto e recusa CLI. Não são testes pagos nem validação integral de NativeAccount/SQLite/servidor.

## Hooks conferidos e limite do núcleo experimental

No ROOT atual existem load_users_estrito, _guarda_claude, _guarda_do_motor, require_admin e _haiku_tool_definitions. Linhas e hash lidos constam no parecer JSON. O núcleo experimental usa agora `_guarda_do_motor(motors.CLAUDE)`.

`run_in_server` permanece código não integrado e NÃO testado de ponta a ponta. A existência dos hooks não torna esse caminho pronto para gasto. Não criar endpoint genérico nem importar o servidor em processo separado para executá-lo. Não há endpoint novo, restart ou mudança de autenticação propostos nesta entrega.

## Concorrência e próximo caminho

RazaoDeUso usa RLock por objeto/processo, read-modify-write do JSON e temporário fixo. Um processo externo pode perder atualizações feitas em paralelo pelo iPhone. Nova trava ignorada pela produção, snapshot de quiescência, ledger separado ou recibo SQLite não satisfazem a exigência de MESMO razão. Por isso --execute continua bloqueado.

Caminho preferido pelo pai: preflight gratuito já realizado por ele e duas mensagens futuras pela sessão autenticada do app, após autorização específica. Não inventar login ou token. A UI usa o caminho real de conta/razão; porém esta entrega NÃO demonstra que a UI imponha saída512, none, máximo duas reservas e tetos0.325/0.65 do harness. Esses requisitos devem ser conferidos ou explicitamente revistos pelo operador antes de tratar o teste UI como equivalente. Não há gasto autorizado por este relatório.

[DECLARADO PELO PAI] Contagem instalada184906, permanente183135, saída4096, margem1024, restante9974, recibo installed_haiku_runtime_count_20260922_191637_790423.json. Não recontado aqui. O restante é26 tokens abaixo da meta10k; não anunciar reserva dinâmica10k satisfeita por essa medição. A preparação offline não altera o pacote nem o manifesto.

Recibos do núcleo experimental excluem prefixo/chaves/exceções brutas e separam custo medido de hold; ainda sujeitos à revisão independente. Os arquivos wire públicos são artefatos de preparação, não recibos financeiros. Nenhum resultado deste trabalho aprova execução paga, integração final ou ativação de produção.
