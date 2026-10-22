# Núcleo IALD v357 — integração preparada

**Estado: validado localmente; ainda não ativado no aplicativo.**

A referência corrente é **v357**. A seção v334 do documento recebido permanece intacta
como retrato histórico. O programa da publicação é vinculado por SHA-256 à seleção v357;
uma troca de arquivo não passa silenciosamente por nova versão autorizada.

## Conteúdo e integridade

| Camada | Tratamento |
|---|---|
| IALD_Kernel_v5.txt | Integral em cada contexto preparado; original preservado |
| IALD_TGL_MEMORY_CORE_v1_20260915.md | Integral, cópia idêntica em bytes; original preservado |
| Lagrangiana, equação mestra, H≥0, Lindblad, fase, comutação | Mantidos no núcleo e complemento matemático |
| Cinco fontes Lean de H1/H2/H3 | Inteiras no contexto, com fonte e escopo |
| Sete documentos científicos | Inteiros no servidor; busca e leitura paginada com hash e URL |
| Atlas e kernel Lean completo | Ferramentas existentes preservadas; Atlas privado restrito |

As conciliações são explícitas, ao lado do conteúdo original: v334/v357; G_rot²=-I versus
G_proj²=G_proj; J antiunitário versus involuções auxiliares; Pi± versus C±; face hiperbólica
versus leitura angular; dephasing puro versus hipótese de estado fixo único; identidade
da interface versus capacidades reais do motor. Nenhuma inferência é ratificada
automaticamente como cânone.

## Medições e testes

- Contexto anterior preparado com v5: **446,916 tokens**.
- Novo contexto do operador: **46,627 tokens** — redução de **89.6%**.
- Contexto público: **40,349 tokens**, sem Atlas privado ou diário.
- Sete documentos reconstruídos integralmente por **283 páginas**, sem perda de texto.
- Oito consultas de conceitos localizaram trechos com posições e proveniência.
- **18 testes de integridade, isolamento e roteamento passaram**.
- **53 verificações das rotas de testadores passaram**. Duas expectativas antigas foram
  atualizadas para incluir exatamente search_tgl e fetch_tgl; a restrição do Atlas permaneceu.
- Sintaxe dos módulos preparada e conferida; hashes dos arquivos de produção continuam no baseline.

A redução acima é de contexto medido, não promessa de latência, qualidade ou custo faturado.
Esta implementação usa **busca lexical local** e as ferramentas existentes. Não foi criado
Vector Store remoto, Conversations API nem servidor MCP. Essas integrações podem ser feitas
depois sem substituir a fonte canônica.

## Ativação pendente

O teste externo e a ativação do v5 aguardam autorização específica de envio à
**api.openai.com**. A revisão automática anterior rejeitou a autorização genérica
“faça tudo” para o conteúdo integral do v5. O teste proposto usa v5 + novo MD + fontes
públicas, sem Atlas privado, com teto de **US$ 0,03** e preservando o limite global.

Após autorização: avaliar a resposta real, aplicar os arquivos com backups de bytes e
checagem de concorrência, executar a regressão obrigatória e reiniciar somente o web.
O modelo nativo, pesos, documentos científicos e arquivos originais não são alterados.
Nenhuma instalação móvel ou publicação nas lojas foi realizada nesta etapa.

Evidências: verification.json, free_staged_updated_expectations.log, test_indexed_core.py,
integration.diff e prepared.json, nesta pasta.


### 16/09/2026 08:19 -0300 — Núcleo v357 ATIVO; TestFlight aguarda etapa manual

<!-- IALD_INDEXED_CORE_V357_ACTIVE_20260916 -->

[INPUT — autorização expressa recebida] Operador: “Sim, autorizo esses arquivos para api.openai.com e o teste”, respondendo à pergunta que nomeou IALD_Kernel_v5.txt e IALD_TGL_MEMORY_CORE_v1_20260915.md, envio integral à api.openai.com, uso no app e teste até US$0,03. A interpretação anterior de “ative o app” foi recusada pela revisão automática antes de qualquer chamada; rejeição e nova resposta ficam preservadas em explicit_approval.json e backup. Não há bloqueio restante de autorização para esse payload.

[REAL — ATIVO] Instalados núcleo operacional v357 + v5 integral + conciliações ao lado, cinco fontes Lean nucleares completas e estado publicado; sete documentos íntegros via search_tgl/fetch_tgl. Janela 480000 e .env preservados. Regra pública de contexto para plano gratuito evita enviar Atlas privado e diário. Não confundir esta busca lexical LOCAL com Vector Store remoto/MCP/Conversations API: esses serviços não foram criados. Originais científicos e download preservados; não houve treinamento de pesos ou movimento do gate.

[REAL — avaliação externa] Uma chamada autorizada ao gpt-5.6-luna com contexto público, v5 e novo MD: HTTP200, 40669 tokens de entrada, 804 de saída, fim stop, teto calculado US$0.01563735 (menor que US$0,03). Reconheceu autoria Luiz Antonio Rotoli Miguel, versão v357/v334 histórica, H_3L≥0/GKSL/dephasing, distinção Pi±/C± e G_rot/G_proj, aplicação the_master_fires e H1 contínua posterior, ratificação reservada ao operador e diferença entre contexto e treinamento. Avaliação específica de seis perguntas; não garantia de todas as respostas. Arquivo model_response_20260916_080011.json; nenhum Atlas privado enviado nesse teste.

[REAL — regressão e serviço] 33 suítes: os mesmos 24 resultados verdes e 9 vermelhos históricos, zero regressões. 18 testes específicos e 53 verificações de rotas já registrados. Atualizadas somente assinaturas de mocks e expectativas das duas ferramentas novas. Web reiniciado UMA vez: PID antigo74548, novo72056; supervisor47020 e nativa34128 preservados. Saúde local/pública200. Navegador autenticado mostrou Online e gpt-5.6-luna após recarga; app aberto novamente na aba17. A atualização de servidor vale para binário4.1(16) existente, sem novo build.

[REAL — revisão beta] Criada conta exclusiva iald_review_beta por autorização prévia expressa: plano gratuito, motorOpenAI, adminFalse, acesso_nativaFalse, cota própria, sem consentimento inventado. Senha aleatória apenas em C:\Users\rotol\.iald_keys\apple-beta\review-account.json, pasta restrita ao usuário e SYSTEM; nunca imprimir senha/token. Login real local200, modelo disponível, ferramentas search_tgl/fetch_tgl presentes, ferramentas do Atlas privado ausentes, bloqueio por consentimento confirmado SEM inferência externa. Os demais usuários foram preservados; backup de bytes no mesmo diretório.

[OPEN — TestFlight NÃO ENVIADO] Grupo externo IALD Piloto (a2f7c246-06e1-4f7c-8fcd-d0c2a79cc345), app6760655636, build4.1(16). Modal “Informações de teste” da aba10 ainda aberto, usuário iald_review_beta preenchido, início de sessão obrigatório marcado, senha vazia. Contato autorizado já preenchido. Tentativa de transferência por área de transferência entre abas não funcionou; campo mascarado não retornou valor à automação. Revisão automática REJEITOU criar formulário de senha visível; NÃO contornar nem imprimir credencial. Pergunta enviada ao usuário para preencher apenas Senha na Apple usando o arquivo local e responder “preenchi”; sem resposta neste registro. Dois servidores locais de transferência foram encerrados e a aba temporária fechada; variável de senha limpa. Depois do preenchimento manual, concluir próximos passos e enviar à revisão beta; não desmarcar login obrigatório. Não há link externo de TestFlight liberado, convite enviado, aprovação beta ou instalação física confirmada nesta etapa.

[OPEN — família] Mãe e esposa usam iPhone. Pedido assíncrono de nome/e-mail da conta Apple de cada uma ainda sem resposta. Não criar identidades Apple por e-mail sem autenticação válida, não compartilhar conta admin e não abrir cadastro irrestrito. Preparar convites externos após revisão beta; o operador quer encaminhar convites. AndroidAPK4.1(16) segue existente; GooglePlay continua pendente de cadastro/D-U-N-S.

Evidências: code_installed.json, additional_test_fixtures.json, suite_gate.json, runtime_live.json, review_account_created.json, review_login_verified.json, completion.json. O antigo REVISAO_NUCLEO_V357.md ganhou adendo de ativação; preservar a preparação como histórico.
