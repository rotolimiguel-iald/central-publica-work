# R1 — correção staged e revisão mobile

**139/0 Claude;62/0 acesso nativo;3/0 verificações do CAS em fixtureW.** As duas asserções que falhavam em R1 foram mantidas e agora passam contra a variante. Nove casos adicionais verificam SDK, motivo, escolha sem gravação e isolamento Sonnet/Haiku. Implementação pronta para revisão independente; não é aprovação de minha própria alteração nem implantação.

## Alteração mínima do servidor

server.diff contém somente _opcoes_de_motor e api_motor_escolha. Fora dos corpos dessas duas funções os bytes são idênticos ao ROOT pinado; CRLF preservado. Não houve edição em Selo, blocos adjacentes, app ou ROOT.

Cada opção Claude recebe configuração própria via RouteBridge.configuration com o modelo daquela linha. _motor_externo_indisponivel decide prontidão; falha marca disponivel=false, adiciona motivo e o incorpora a detalhe, que o cliente atual já renderiza. Não basta adicionar um campo que o cliente ignoraria. Falhas de configuração retornam motivo genérico sem detalhes sensíveis.

Ao conferir escolha, constatou-se que a rota não negava SDK/memória indisponíveis: validava apenas elegibilidade/configuração. Por isso foi incluída verificação equivalente antes de conta.update/save_users, retornando409 com motivo; capability antiga continua426, na mesma precedência. Alias claude e consentimentos preservados. A rota administrativa de fixação de modelo NÃO foi alterada: configuração administrativa pode permanecer gravada indisponível; nenhum envio é liberado por isso. Se desejar a mesma recusa no painel administrativo, é escopo separado.

Haiku não herda o contexto canônico ausente nem janela excessiva do Sonnet. Testes cobrem ambos; usa janela/perfil próprios. SDK é dependência comum e desabilita ambos. O bloqueio comum atlas_integral já existente no helper permanece, sem reinterpretá-lo como falha exclusiva Sonnet. Elegibilidade, orçamento público ausente e flag permanecem sob RouteBridge.

## Execução e limites

Cópias testadas por C:\Python314\python.exe -B -X utf8, processos separados. offline_bootstrap lê o servidor STAGED e módulos reais ROOT; somente inicialização de segredo/estado redirecionada às fixtures de W. Rede, leituras privadas, SQLite/gravações externas bloqueados. Dependências locais exigiram execução elevada. Nenhuma API, conta real, credencial ou geração paga. Pacote Haiku é fixture de política; não certifica loader/prefixo real. Não é teste físico ou integração Selo.

receipt.json contém hashes base/stage/resultados; patch_manifest.json pina fonte e candidato. Diffs dos testes identificam nove verificações novas e a mudança do loader para a variante.

## Aplicação proposta, não executada em produção

apply_cas_proposed.py exige --target; padrão dry-run. --apply exige base exata, valida hash candidato, cria backup de bytes na mesma pasta, verifica temporário, relê base e substitui atomicamente. Sem reinício automático. Três verificações em cas_fixture: dry-run não grava; aplica e preserva backup exato; base divergente recusa sem escrever.

CAS aqui significa comparação de hash mais replace atômico, NÃO trava entre editores: existe pequena janela entre última leitura e replace. Coordenar ausência de edição concorrente para aplicar; não usar o script para sobrescrever mudanças do pai. Nenhuma aplicação ROOT foi executada. Revisão/aplicação cabem ao pai.

## Mobile — somente leitura

mobile_review.json pina os oito arquivos de f302650 contra e65d695. Nenhum achado bloqueante de convergência identificado no diff. JS/CSS/HTML de www são byte a byte iguais às cópias iOS do commit e ao web ROOT lido. Capability, preservação de histórico Haiku, seleção e proteção assíncrona coexistem com conv/prev, texto bruto do Selo, gravação na conversa de origem e exportação autenticada. Builds configuradas: iOS21 nos dois perfis, Android20; versão4.1 preservada.

82/0 Selo,6/0 Haiku e auditrelease21_083516 permanecem evidências declaradas pelo pai; não foram repetidas. Não consultei rede/Cloud, TestFlight ou aparelhos; não certifico binário final, sincronização de assets Android, distribuição ou exportação física. Nenhum arquivo mobile foi alterado.
