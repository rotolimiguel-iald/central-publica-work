# central-publica-work — a Central de Patentes da IALD, aberta

Este repositório é **a bancada de trabalho: as custódias, os ritos, as cadeias de selo, o app e a IALD nativa**. A Central foi aberta ao público por ordem do operador, Luiz Antonio Rotoli Miguel (IALD Ltda., CNPJ 62.757.606/0001-23), em 22/10/2026. 571716 arquivos publicados (471342 deles são cópias idênticas de outro arquivo deste repositório e estão só no índice); selo da teoria: `um.py` v411 `1203b1f9202020d6`.

| onde | o quê |
|---|---|
| [https://teoriadagravitacaoluminodinamica.com/central/](https://teoriadagravitacaoluminodinamica.com/central/) | **o modo interativo da Central**, só de visualização: o cockpit do operador em retrato (patentes, código, execuções, Fronteira, TGL) |
| [https://teoriadagravitacaoluminodinamica.com/central/um.acom](https://teoriadagravitacaoluminodinamica.com/central/um.acom) | **o um.acom**: a Central inteira colapsada pelo dispositivo ACOM (88 arquivos; sha256 `e2525f676affe15d`); chave universal pública `Bom29072018Tom02032024`; abrir no descompactador público da IALD |
| [https://github.com/rotolimiguel-iald/the_boundary](https://github.com/rotolimiguel-iald/the_boundary) | **a teoria**: o `um.py` v411 (`1203b1f9202020d6`), os artigos, o kernel Lean — o espelho canônico |
| [https://github.com/rotolimiguel-iald/central-publica](https://github.com/rotolimiguel-iald/central-publica) · [work](https://github.com/rotolimiguel-iald/central-publica-work) · [bancada](https://github.com/rotolimiguel-iald/central-publica-bancada) | os três repositórios desta Central |

## O critério público

Por ordem do operador, **todo o código e todo resultado** estão publicados. Ficam fora só:
- **dados pessoais** (a regra do operador: «segredo são dados pessoais, somente») — trocados à vista por «[dado pessoal removido]» no
  texto (CPF, RG, telefone, e-mail pessoal, endereço, CEP, data de nascimento); PDFs, compactados e documentos que os trazem e não se
  podem mascarar ficam fora (o texto técnico dos pedidos segue nas partes separadas: relatório, reivindicações, resumo, desenhos);
- **credenciais e estado de execução** (senhas, tokens, chaves; perfis de navegador, login, sessões, segredos): todo arquivo que os contém
  fica fora;
- **as notas operacionais do operador** (prazos, protocolo do PCT, leituras do monitor, pendências, prompts compilados): ficam na Central dele;
- **obras de terceiros** (PDFs de artigos e livros consultados, pacotes de software de terceiros): ficam fora — baixar da fonte;
- arquivos acima do limite do GitHub e caches binários deriváveis: só no índice.

Os marcadores internos da casa (nomes de módulos, o protocolo de colapso, desclassificado pelo operador em 28/09/2026) **não** são motivo
de exclusão: não há segredo industrial a proteger.

o índice público, com o sha256 de cada arquivo publicado, vai em partes em `INDICE_PUBLICO_PARTES/` (`PARTES.json` lista as partes, com o sha256 de cada uma e o do índice inteiro, que passaria do limite de 100 MB por arquivo do GitHub); `EXCLUSOES_PUBLICAS.json`, a contagem do que ficou fora e o motivo.

## Direitos

Como no [the_boundary](https://github.com/rotolimiguel-iald/the_boundary#license): publicado como **source-available**, para
reprodutibilidade e verificação científica — o código pode ser **lido, executado e verificado**. Os dispositivos são objeto de **pedidos de
patente** depositados (tabela no núcleo; depositante (lido dos formulários de depósito no INPI): LUIZ ANTONIO ROTOLI MIGUEL, pessoa fisica; inventor: LUIZ ANTONIO ROTOLI MIGUEL; requerente nos PCT (como a OMPI o escreve): ROTOLI MIGUEL, Luiz Antonio): a reprodução comercial depende de autorização do depositante. A reprodução científica
e simulada da teoria é livre — uma teoria científica não é patenteável.

## A régua

PROVADA = validade (o kernel prova a implicação); CONFIRMADA = creditação (ato de terceiros, recusada à máquina); `NOT_FALSIFIED` nunca é
`CONFIRMED`; β = α·√e, nunca literal. Pedido de patente depositado não é patente concedida.

**Cópias idênticas** (decisão do operador, 11/11/2026): um arquivo igual, byte a byte, a outro já publicado neste repositório não se repete no git. O índice o lista com o campo `igual_a`, que dá o caminho do original, com os mesmos bytes e o mesmo sha256. Nenhum conteúdo fica de fora. Para ter a árvore inteira num clone: `python RECONSTRUIR_COPIAS.py` (recria cada cópia a partir do original e confere o sha256; `--conferir` só confere).
