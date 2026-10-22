# Distribuir a IALD para um grupo de testes

Orientação conferida em 15/09/2026. Os links de convite da IALD ainda precisam ser gerados nas lojas; este documento não anuncia uma distribuição nova.

**iPhone e iPad — TestFlight externo**

1. No App Store Connect, abrir IALD → TestFlight → Testes externos e criar um grupo, por exemplo “IALD Piloto”. Pessoas que só vão testar entram como testadores externos; não precisam receber acesso administrativo ao App Store Connect.
2. Adicionar a compilação atualizada, preencher as informações do teste e enviar à análise beta. Uma compilação marcada “TestFlight Internal Only” não pode ser distribuída para esse grupo. A primeira compilação externa exige análise da Apple.
3. Após a aprovação, ativar um link público com limite de participantes ou convidar pessoas por e-mail. Para encaminhar em um grupo de WhatsApp, o link público é a opção mais simples; qualquer pessoa que receba o link poderá participar enquanto houver vagas.
4. Cada participante instala o TestFlight no iPhone/iPad, abre o convite e toca em Instalar. As próximas compilações são disponibilizadas pelo mesmo grupo.

Fonte: [Apple — convidar testadores externos](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers).

**Android — teste interno do Google Play**

1. Com a conta de desenvolvedor habilitada, abrir o aplicativo no Play Console → Testar e lançar → Teste → Teste interno.
2. Enviar o AAB assinado da versão atualizada e cadastrar os e-mails Google dos participantes, ou um Grupo do Google. O teste interno admite até 100 pessoas.
3. Publicar a versão nessa faixa de teste e copiar o link de participação. Cada pessoa abre o link usando a conta cadastrada, aceita participar e instala pela Play Store. O aplicativo não precisa aparecer na busca pública da loja.
4. Novas versões assinadas são enviadas à mesma faixa e chegam como atualização.

Fonte: [Google — configurar testes](https://support.google.com/googleplay/android-developer/answer/9845334?hl=pt-BR).

No último estado registrado deste trabalho, a abertura da conta Google da organização aguardava o D‑U‑N‑S. Não foi conferida uma conclusão posterior nesta etapa. Enquanto o cadastro não estiver habilitado, um APK assinado atualizado pode ser distribuído diretamente; a pessoa autoriza a instalação daquela origem no Android. Nesse caminho, a atualização também precisa ser entregue manualmente. Um AAB não é um instalador direto para o telefone.

**Acesso e versão da IALD**

Cada participante precisa da própria conta liberada na IALD. Instalar o aplicativo e ter permissão para usar a IALD são etapas distintas. Não compartilhar a senha do operador.

O núcleo fica no servidor e acompanha as chamadas encaminhadas ao motor OpenAI. As correções de interface e fórmulas foram sincronizadas nas fontes web/Android/iOS em 15/09, mas os binários anteriores não foram recompilados nesta etapa. Antes de enviar o convite como “versão atualizada”, gerar e distribuir a nova compilação.

Uma chamada real recebeu 324.211 tokens de entrada; os cabeçalhos da API informaram limite de 500.000 tokens por minuto. Portanto, começar com um grupo pequeno: chamadas simultâneas podem esperar a capacidade renovar. O servidor passou a repetir de forma limitada as recusas temporárias que informam tempo de espera. Essa correção não aumenta a capacidade contratada da API.

Mensagem sugerida para encaminhar depois que os links forem reais:

> Estou convidando você para testar a IALD. No iPhone/iPad, instale o TestFlight e abra o convite. No Android, abra o link de participação do Google Play com a conta cadastrada. Entre com sua própria conta da IALD. Teste conversa, pesquisa, fórmulas e alternância de modelos quando disponível; envie o aparelho, a versão e uma descrição de qualquer erro.
