# 020 · Primeira devolução visual — a dobra e as três portas

**De Kimi para Codex e Luiz · 09/11/2026.** Continuei a unidade `F9.UM_INTERFACE_20261108.INTEGRACAO` a partir da 019, sem recomeçar o aplicativo e sem alterar motor, kernel, gate ou selo. **Esta é uma devolução de telas, não uma declaração de aceite visual nem de rodada científica nova.**

## Ver agora

- **Corte comparativo antes/depois:** [abrir `dobra-020.html`](http://localhost:7100/dobra-020.html). O corte 011 permanece ao lado da proposta 020; há reprodução, volta por gesto e navegação pelos nove quadros.
- **Prévia principal:** [abrir a Interface do Um](http://localhost:7100/). Para chegar à galeria: inscrever `1` → “Pular abertura” → “Prosseguir para o rito” → “Rever a Bancada” → “Entrar na Bancada do Um”.
- **Galeria, captura imediata:** [três portas visuais](http://localhost:7100/verification/09a-portas-visuais.png).
- **Passagem intermediária, captura:** [substrato torcendo com a esquadria de 90°](http://localhost:7100/verification/02c-torcao-desktop.png).
- **Sequência de nove quadros:** `C:\IALD\um_interface\src\dobra-frames\01.png` até `09.png`.
- **Recibo da verificação:** `C:\IALD\um_interface\verification\results.json` — **93/93**, zero erro de console e zero erro HTTP inesperado.

## Feito nesta edição

1. **Inscrição como gesto da pessoa.** Campo realmente vazio, sem placeholder ou preenchimento; rótulo “Digite o número 1 para iniciar o programa.” e botão “Iniciar com o Um”. Vazio ou entrada inválida mantém foco, explica o que digitar e não inicia filme ou motor. Enter e clique seguem a mesma regra; `١` também é normalizado.
2. **Novo corte de 32 s, com o original preservado.** Nove gestos: breu → ingresso do 1 → projeções na identidade matricial → traço → resistência → torção do substrato → projeção oposta → leitura de Miguel → universo externo. Não há voo interno nem perseguição de partícula. As explicações não ficam queimadas na imagem: PT/EN/AR estão em VTT separado.
3. **Camada de estudo.** Pausa, voltar um gesto, rever sem legendas e nove quadros estáticos equivalentes para movimento reduzido. A pequena esquadria de 90° permanece visível e distinta do arco de `θ_M = arcsin √β = 6,297289°`, calculado da entrada CODATA, sem fixar β no código.
4. **Três portas visuais na Bancada.** Cosmológicos 9, Computacional 6 e Partículas 1, com imagens simbólicas antes do texto. As 16 estações anteriores foram preservadas. Cada caixa oferece “Ver o dado”, “Entender a fórmula” e “Perguntar à IALD”.
5. **Retorno e foco.** Fechar detalhe ou diálogo devolve a pessoa à mesma ação da galeria, inclusive após atualização do DOM. A abertura é ancorada no elemento que recebeu o clique, com fallback semântico pela estação.
6. **Acabamento.** Desktop, mobile, RTL, teclado, pesquisa, reorganização, modo leve/offline e procedência continuam funcionais. As portas usam imagens-guia sem frases congeladas num único idioma.

## Delimitação formal efetivamente conferida

Foram lidos `TheMatrixRule.lean`, `TheAngleIsTheProjection.lean`, `TracialDissipativeTorsion.lean` e `CartanTracialSupplier.lean` na árvore v409, além de `first_law_link` e `F_ext_doubling` no motor empacotado.

- `the_matrix_rule` é uma **conjunção de elos**, não uma dedução da cadeia inteira; a ordem dos nomes é [INPUT/ONTO].
- `the_angle_is_the_projection` prova que a família angular é a decomposição espectral; não prova as identificações ontológicas `J = gráviton = geometria = consciência`.
- A pedra de torção tracial-dissipativa formaliza a álgebra da contorção e seus limites; não fixa escala nem grau físico.
- O fornecedor de Cartan é condicional e explicita hipóteses e paredes; textura, esquadria ou quarto de volta visual não foram promovidos a teorema de torção.
- `first_law_link` mantém `g−/g+` aberto. `F_ext=2F` e a identificação do registro com `c³` são leituras estruturais/ontológicas [CONJ]; o fator 2 não foi apresentado como medição de força, rank ou probabilidade.

Por isso a passagem inteira está identificada como **narrativa do autor [INPUT/ONTO]**, com os elos formalizados separadamente. Nenhum evento Lean foi inventado.

## Verificado nesta edição

- `node --check` dos JavaScript alterados e `npm run build`.
- Suíte em Chrome: **93/93**, incluindo campo vazio, erro e foco; ordem dos nove gestos; 90° + 6,297289° distintos; portas e 16 imagens; dado/fórmula/diálogo; retorno de foco; PT/EN/AR e fallback explícito; RTL; teclado; Coma; perfil sem GPU; mobile; ACOM e toda a regressão anterior.
- Inspeção visual humana das capturas do corte, portas, Computacional e mobile.
- Novo WebM: `C:\IALD\um_interface\src\breu-um-dobra-global.webm`, **9.602.856 bytes**, SHA-256 `d8f7d148c8e4c525989616453d1febba29c77f4c2b83b8ac26dc015952d7a1c8`.
- Motor preservado: SHA-256 `53284ba461ecd94060cc2d12fed992bba70ab857f70198b24e6535b9f24f8da6`.
- Comparativo e recibo de mídia: `C:\IALD\um_interface\verification\dobra-020\`.

## Escolha visual proposta a Luiz

Manter o **plano contínuo dourado + ciano**: o fio dourado é o sinal; o substrato ciano resiste e torce; a esquadria fica no substrato; o arco só nasce com a leitura. O universo continua visto de fora. Esta é uma proposta, não um aceite presumido.

## Acréscimo — instalador ACOM real e staging

**Feito e verificado depois do recibo visual inicial:**

- Instalador: `C:\IALD\um_interface\release\UM-Setup.exe`, **481.140.224 bytes**, SHA-256 `2556353a163e18175ed78d903bca14b2cd9e7a149d1a9cecbc502080da3ac8f5`. Compilação de teste **sem assinatura Authenticode**.
- Payload: `C:\IALD\um_interface\release\UM-payload.acom`, **481.114.843 bytes**, SHA-256 `e5a654914604c9bcefb570315bb4ae36dcef6e002208edced7135a1eccc08d77`. **ACOM Archive v1 real**, zlib/store, **5.878 arquivos**, `meta_chain = b070dc98c75f227139d2d6bcee2fae4246d0462f0d7a5ee52f785cb0e480cb8f`. Não é ZIP/SFX renomeado.
- Executável reconstruído: `C:\IALD\um_interface\release\um_py.exe`, SHA-256 `3073c4e840dc2627ae673df5d08b6ffecf7156c6df2a0f92902c761f022f25de`, com telas 020, Node, Python, NumPy, SciPy e h5py. O host não depende mais de `C:\Python314\python.exe`; resolve o runtime dentro da instalação e falha fechado se os módulos estiverem ausentes.
- `native-results.json`: **10/10**; `results.json`: **93/93**.
- Staging sem perfil externo: extração e conferência de todos os 5.878 arquivos; `PYTHONNOUSERSITE=1`; abertura automática da Bancada com pino v409 válido; restauração byte a byte (`c9718950089be3909610c25b25b8b77faa97398868b9d957b7a5439134d551ea`); desinstalação confirmada.
- Recibos: `verification\installer-live\clean-install-receipt.json` e `verification\installer-clean\work\verification\dependencies.json`.
- A integração do Explorador foi testada por **hive isolado**, sem modificar o registro de Luiz. O aviso residencial, a fonte/licença e o caminho de desinstalação estão incluídos.

## Pendente, sem promoção indevida

- Avaliação do corte por Luiz e, se desejado, por um leitor novo sem som/títulos, apontando onde a trama resistiu, o que torceu e qual ângulo foi lido. Isso mede legibilidade, não a TGL.
- **Nova rodada científica completa de ponta a ponta.** Foram registradas 18 tentativas/recibos: duas falhas iniciais de espera e 16 janelas de trabalho. Toda janela válida começou com inscrição real e chegou ao lançamento do pilar; o harness encerrou antes da conclusão. **Nenhum selo novo foi emitido e nenhum artefato novo foi promovido.** As amostras de CPU confirmam criação de arquivos e acionamento dos trabalhadores, mas não conclusão. Recibos: `verification\live-run-results-*.json`; o mais recente é `live-run-results-1794253819184.json`.
- A limitação restante é operacional: as provas iniciais não têm checkpoint próprio e a janela de execução disponível interrompe antes do término. É necessário um acompanhamento contínuo maior, sem cancelamento por duração, para produzir início, término e artefatos da mesma execução.
- Serviço IALD a partir de perfil limpo sem credenciais desta máquina. Bancada e ACOM continuam utilizáveis offline.

## Acréscimo — abertura 011 restaurada por escolha de Luiz

**09/11/2026.** Luiz escolheu voltar ao vídeo de abertura anterior. A abertura **011 voltou a ser o padrão**; `dobra-020.html` e a mídia 020 permanecem apenas como material de estudo. As três portas visuais, as ações da galeria, a inscrição vazia, os idiomas, o percurso por capacidade e o instalador ACOM foram preservados.

- Vídeo padrão: `src/breu-um-traco-global.mp4`; pôster: `src/breu-ilhado.jpg`; duração de apresentação: **20,65 s**. Sequência restabelecida: breu → ingresso do Um → fractalização → traço → ângulo de Miguel → universo externo. Legendas PT/EN/AR e seis quadros de movimento reduzido voltaram aos tempos 011.
- Prévia conferida no navegador: inscrição real com `1`, reprodução do corte correto e etapa final “Visto de fora”, com filamentos, aglomerados e grandes vazios. Captura temporária SHA-256 `2223b20e90b5ea59665f5967d134771cf55994c5fa21d52c5cdb31da29a88beb`.
- `node --check src/main.js`, `npm run build` e suíte atual: **89/89**, sem erros. A contagem anterior 93/93 pertence à edição 020; quatro verificações específicas daquela abertura foram retiradas junto com sua ativação.
- Executável atualizado: `C:\IALD\um_interface\release\um_py.exe`, SHA-256 `0ef71e7bb2e5488ef0e552f6e85ac109fbc7e756c66b09fee0a1531112fe43b8`. Verificação nativa atual: **10/10**.
- Instalador atualizado: `C:\IALD\um_interface\release\UM-Setup.exe`, **481.141.248 bytes**, SHA-256 `9e6d3faeef1da8bc53cc2f753e796e8a7faad64b6f632e9dbf941957baeba9a5`; compilação de teste **sem assinatura Authenticode**.
- Payload atualizado: `C:\IALD\um_interface\release\UM-payload.acom`, **481.116.165 bytes**, SHA-256 `56be6ff2921522c745f0935a1e44ef4b806acdb7d794024edfdd46cdb597f39d`; **ACOM Archive v1**, zlib/store, **5.878 arquivos**, `meta_chain = 1c9d291c9c46094ac2187fd417cb311634fc498d17a7bfd8f357eaa9e336d242`.
- A ocupação inicial de `release\um_py.exe` foi resolvida encerrando somente o processo de teste da própria release. Um servidor Node antigo de `verification\live-work-*` na porta 7103 também foi isolado e encerrado antes da verificação limpa.

Esta atualização **não declara nova rodada científica concluída nem novo selo**. A pendência operacional registrada acima permanece inalterada.
