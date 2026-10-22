# IALD — instalação Android e próximos envios

Estado verificado em 13/09/2026. Este documento descreve o fluxo de entrega; a fonte do aplicativo continua em `C:\IALD\projetos_pyhton\IALD\iald-app`.

## Instalar o Android agora, por USB

[REAL] `IALD-4.1-11.apk`, nesta pasta, é uma cópia verificada do APK release existente: aplicativo `br.ia.IALD`, versão 4.1, código 11, assinatura APK v2 válida, Android mínimo 7.0 (API 24). A instalação em aparelho ainda não foi confirmada.

1. Conecte o Android ao computador por USB e escolha **Transferência de arquivos** no telefone.
2. Copie `IALD-4.1-11.apk` para a pasta **Download** do telefone.
3. No Android, abra **Arquivos > Downloads** e toque no APK.
4. Se solicitado, permita que esse gerenciador de arquivos instale este aplicativo e conclua a instalação. Os nomes dos menus variam conforme o fabricante.
5. Abra **IALD** e teste entrada, resposta em streaming, teclado, anexos e saída/reentrada. Ao terminar, pode desativar novamente a permissão de instalar outros aplicativos.

O link local do Codex aponta para este computador; ele não é um endereço público de download no celular. O arquivo `.aab` é destinado ao Google Play e não substitui o APK neste procedimento.

## Google Play

[REAL] O cadastro empresarial permanece no campo obrigatório D-U-N-S. O perfil de pagamentos, a taxa e a conta de desenvolvedor ainda não foram concluídos. Não há link de instalação da Play Store neste momento.

[OPEN] A consulta/emissão gratuita na CIAL Dun & Bradstreet foi preparada, mas o envio da mensagem ao atendimento aguarda a autorização específica solicitada ao operador. Nenhum serviço pago foi contratado.

Após obter o número e concluir a verificação da conta: criar/conferir o aplicativo `br.ia.IALD`, configurar Play App Signing, enviar o AAB assinado para **Teste interno**, incluir o próprio operador e disponibilizar o link de participação. Não é necessário abrir um novo aplicativo para cada melhoria.

Antes do primeiro envio, conferir a estratégia de assinatura: a chave de upload usada nos AABs e a chave de assinatura dos APKs distribuídos pelo Google podem ser distintas. Se o Google usar outra chave de assinatura, a migração deste APK instalado por USB poderá exigir desinstalação. Preservar os dados necessários antes de fazer isso.

Referências: [teste interno do Google](https://support.google.com/googleplay/android-developer/answer/9845334?hl=pt-BR) e [D-U-N-S gratuito](https://support.google.com/googleplay/android-developer/answer/13634888?hl=pt-BR).

## Quando a sessão de melhorias terminar

1. Ler o handoff atual e o `git status` do aplicativo. Confirmar quais mudanças estão prontas; não publicar trabalho parcial da outra sessão.
2. A interface canônica fica em `C:\IALD\projetos_pyhton\IALD\app`. Executar `sincronizar_app.ps1 -ComSync` na pasta `iald-app`, conferir o resultado e comparar os arquivos de origem com `www` e os recursos das duas plataformas. `kernel_prompt.js` do pacote deve vir de `kernel_prompt_bundle.js`, conforme o mapa do script.
3. Rodar `npm run validate` e os testes pertinentes às alterações. Auditar o diff e a lista de arquivos antes de enviar. Servidor, `.env`, senhas e chaves privadas ficam fora do repositório.
4. Android: incrementar `versionCode` em `android/app/build.gradle` para um número superior ao maior já enviado. O pacote disponível hoje usa 11; reler o projeto e o Play Console antes de escolher o próximo. Manter `applicationId` e a configuração da chave de upload existente. Compilar `bundleRelease` e `assembleRelease` na pasta Android com o ambiente de compilação já configurado, verificar assinatura e metadados dos artefatos e enviar o novo AAB ao mesmo teste interno.
5. Apple: manter o app existente 6760655636 e o identificador `br.ia.IALD`. O Xcode Cloud está ativo para a branch `codex/mobile-release` do repositório privado `rotolimiguel-iald/iald-app`. Cada push nessa branch pode iniciar uma compilação assinada; realizar o push somente depois da sincronização e validação.
6. O Xcode Cloud atribui o número de compilação iOS. A versão disponível é 4.1 (13); o número Android é independente. Acompanhar a nova execução até processamento no TestFlight, resolver eventual declaração de criptografia com base no código real e adicionar a compilação ao grupo interno **IALD Equipe**. A pós-ação automática de distribuição ainda não está configurada.
7. Testar a atualização nos aparelhos e registrar versão, commit, resultado e pendências nos handoffs, com backup imediato de bytes antes de cada atualização de memória.

Melhorias apenas no servidor/modelo podem passar a valer sem reinstalação, conforme a API usada. Mudanças na interface embarcada ou nos plugins nativos precisam de novo pacote. As exigências de revisão pública — privacidade, exclusão de conta, denúncia de conteúdo e correspondência das ferramentas oferecidas — permanecem no handoff; a disponibilidade para teste não prova aprovação pública.
