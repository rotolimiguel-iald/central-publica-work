# Kimi → Codex · recibo ACOM 013 + acabamento 015
1. Versão final preservada: `C:\IALD\um_interface` · prévia [A Interface do Um](http://localhost:7100/) · direto em `?ferramenta=acom`; estética **observatório noturno**.
2. A abertura 011 e a Bancada aprovadas não foram redesenhadas; a regressão integral terminou em **60/60 conferências**, zero erros de console e zero erros HTTP inesperados.
3. ACOM abre antes ou depois da inscrição, no primeiro quadro, capacidade, runtime e Bancada; voltar preserva a jornada e, no móvel, a ferramenta abre no topo.
4. Contrato implementado: status JSON com token/versão, ações `pack-files`, `pack-folder`, `extract`, header `X-ACOM-Token`, idioma, MIME e timeout somente na sondagem.
5. Sem adaptador, a página diz que não lê nem altera arquivos; com adaptador, mostra “Pronto para escolher seus arquivos” e “Já instalado neste computador”, ocultando o instalador.
6. Aguardo, cancelamento e erro usam linguagem humana; o resultado mostra a mensagem e o destino, com escape HTML e quebra segura de caminhos longos.
7. Amostra real: `/downloads/Primeira-luz.acom`, 1.272 bytes, SHA-256 `63e50fcd44a722f544c02374d57281dfc7141d3e8eaa5398d76d9201a99fa478`.
8. Restaurei a amostra com o leitor ACOM publicado: 3 arquivos, 218 bytes, hashes íntegros; `Primeira luz/inscrição.txt` contém exatamente `1`.
9. Instalador e fonte finais estão em `/downloads`; seus hashes atuais, o recibo de restauração e os hashes das telas estão em `C:\IALD\um_interface\verification\DELIVERY.json`.
10. PT/EN/AR cobrem inclusive rótulos secundários, amostra e estados; RTL, teclado, 375 px, Coma, perfil sem GPU e seis quadros estáticos passaram na mesma suíte.
11. Evidências: `C:\IALD\um_interface\verification\results.json`, 19 capturas na mesma pasta e `sample-restoration.json`.
12. O host `:7101` existiu apenas dentro da verificação, estava rotulado como demonstração e não processou arquivos; a suíte não prova compactação nativa pela página estática.
13. Nenhum motor científico, `um.py`, gate, credencial, provedor ou publicação foi alterado; aguardo o aceite de Luiz antes de qualquer integração real seguinte.
