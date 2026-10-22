# Capturas da v338: correspondência e ordem de gravação

09/09/2026. [REAL — leitura de fonte e comparação de bytes, sem execução do programa]. Esta nota acrescenta a investigação do mecanismo à discrepância registrada anteriormente; não altera os recibos anteriores nem o acervo canônico.

O [recibo do snapshot](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_V338_FECHAMENTO_20260909/RECEIPT_V338.json>) verifica que o hash do `um.py` e o hash do manifesto formal conferem com o selo da v338. A captura de auditoria confere com o manifesto; a captura de compilação não confere, embora as duas registrem saída zero. A compilação contém 178 linhas de aviso; a auditoria, zero. Não houve nova compilação canônica nesta tarefa.

O [recibo dos fontes formais](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_V338_FECHAMENTO_20260909/RECEIPT_FORMAL_SOURCES_V338.json>) mede 684/684 arquivos atuais iguais aos hashes do manifesto e 683/683 arquivos embutidos iguais, byte a byte, aos materializados. O agregado confere tanto com o manifesto quanto com o selo. As 1.358 declarações dos 77 módulos incorporados, incluindo 1.065 teoremas, constam do relatório registrado com axiomas restritos a `propext`, `Classical.choice` e `Quot.sound`. O arquivo adicional do conjunto formal é `_check_damming.lean`; não está na tabela embutida.

## Mecanismo identificado na fonte

1. [`_unified_main`](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:181426>) chama `main()` e depois `selftest_fail_closed()`.
2. A execução principal escreve o [manifesto formal](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:180872>) com os hashes guardados em `core["kernel_formalization"]`.
3. O [autoteste](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:130957>) chama o verificador duas vezes: com a adulteração de teste e depois da restauração. Os resultados dessas chamadas são locais ao autoteste.
4. Cada chamada do verificador [escreve novamente as duas capturas nos mesmos nomes](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:137082>). A gravação ocorre antes da análise de axiomas.
5. Ao terminar o autoteste, o programa acrescenta seu veredito ao selo. Essa etapa não substitui os hashes de compilação e auditoria do manifesto formal pelos resultados da chamada restaurada.

[DERIVED — análise do fluxo de controle] Essa ordem permite que o manifesto descreva a compilação principal e a captura disponível descreva a compilação restaurada do autoteste. O texto produzido por `lake build` pode diferir entre essas chamadas, mesmo com fontes finais iguais; a saída de `TGL/Audit.lean` pode permanecer idêntica. O mecanismo é consistente com a discrepância observada e com as datas dos arquivos. Uma identificação exclusiva de cada processo histórico exigiria capturas separadas por chamada; a leitura de código não substitui essa trilha.

## Encaminhamento concreto à sessão codificadora

Preservar capturas e metadados distintos para as etapas principal, autoteste adulterado e autoteste restaurado, com identificador de rodada, comando, código de saída, comprimento e hash. O manifesto principal deve apontar para sua própria captura imutável; o recibo do autoteste deve apontar para as duas capturas correspondentes. A gravação deve tornar falhas de escrita visíveis. O `except OSError: pass` atual pode ocultar falha ao persistir uma captura, embora o resultado em memória exista.

Ajustar a prova de rastreabilidade não requer alterar um enunciado Lean, elevar o gate ou repetir testes da natureza. Nenhum código canônico foi modificado nesta tarefa.

## Correção textual ainda presente

A fonte inglesa ainda contém a frase de que o espectro modular é puramente contínuo e não possui autovetores em [um.py](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:165573>). Ela precisa ser harmonizada com os resultados de autovetores e totalidade da construção já registrados no kernel. Esta é a mesma errata espectral documentada anteriormente, agora relocalizada na v338, e não uma nova refutação do modelo inteiro.
