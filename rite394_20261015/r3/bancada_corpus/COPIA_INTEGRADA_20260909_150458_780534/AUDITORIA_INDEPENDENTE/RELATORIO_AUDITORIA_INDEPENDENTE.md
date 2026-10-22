[REAL — auditoria estática independente] PASS_STATIC_INTEGRATION_SCOPE. Foram conferidos 618 critérios; 618 passaram. Nenhum um.py foi executado/importado, e nenhum build foi executado ou reiniciado por este auditor.

# Auditoria da cópia integrada

Data: 09/09/2026. Revisor: /root/selected_geometry_design. Escopo: snapshot, AST, bytes, fontes embutidas, transposição, nomes e auditorias.

## Resultados medidos

- O snapshot é igual em bytes ao um.py canônico lido nesta auditoria e coincide com o hash aprovado. A linhagem v337 é identificada pelos marcadores ext_v337, preservados; 337 é o maior marcador ext_vNNN fora da tabela.
- O AST e todos os bytes antes/depois do valor de _EMBEDDED_KERNEL_FILES são idênticos. Logo o código de flags, sentinelas, gate e execução fora dessa tabela foi preservado integralmente.
- A tabela passou de 606 para 651 ARQUIVOS embutidos. Destes, 602 para 647 são arquivos Lean; os outros quatro são configuração/README.
- As 45 fontes novas correspondem exatamente à CONFIG_APROVADA. Cada fonte e recibo anterior teve hash conferido; cada módulo consta em execução PASS individual aprovada e suas declarações aparecem nas auditorias prévias com axiomas permitidos.
- A única transformação nas novas fontes é acrescentar TGLExt. aos imports dos módulos locais aprovados. Não houve normalização de fim de linha: todos os originais novos já usavam LF. Namespaces, assinaturas e corpos de prova foram comparados por igualdade exata do texto fora das linhas de import.
- Os arquivos transpostos em disco são iguais em bytes às respectivas entradas embutidas.
- Entre os arquivos embutidos preexistentes, somente TGLExt.lean e TGL/Audit.lean receberam acréscimos. Seus prefixos originais foram preservados em bytes. Os acréscimos contêm apenas comentários, imports e comandos de auditoria esperados.
- Foram adicionados exatamente 45 imports e 653 entradas globais #print axioms, correspondentes aos 653 teoremas novos; há mais 200 definições/abreviações/estruturas. Os nomes novos são distintos, e nenhum dos 653 nomes repete uma entrada da auditoria antiga.
- A ordem dos módulos é uma permutação completa dos aprovados e respeita suas dependências locais.
- Todos os artefatos monitorados permaneceram com os mesmos hashes entre início e fim da verificação.

## Hashes lidos

Snapshot/canônico: e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303  
Cópia integrada: a64395bd507e2803dd06eafa652f43dbaf31a02471dfb3ae1a1d6af388dd62a0  
CONFIG_APROVADA: 6c64a9a68c863be3e61a8e45ccd1af6cb4c9451a952fc3e07c0fae98c4ecbc64  
INTEGRATION_RESULT: 316c1069ea244d0acfb2c21be48f23f74c42a5229719945e920b7400f71889e4  
JSON desta auditoria: 895fcff630232879c7f56d49d2a137e9132dc07dd6e9d5b847f51ccc40bd6cad

Evidência detalhada: [AUDITORIA_ESTATICA_INTEGRACAO.json](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_150458_780534/AUDITORIA_INDEPENDENTE/AUDITORIA_ESTATICA_INTEGRACAO.json>).

## Alcance e limites

Esta auditoria verifica preservação de fonte e transposição mecânica. Não realizou nova revisão semântica individual dos 653 teoremas; a igualdade dos enunciados e corpos com as fontes anteriormente aprovadas foi verificada. Não executou/importou um.py, não recompilou Lean e não refez a árvore transitiva de dependências.

A compilação conjunta de 48 processos é conduzida separadamente pelo agente raiz. Nenhum resultado dessa execução é certificado aqui; o recibo global ainda deve ser lido por quem a conduz. A preservação de flags/gate significa ausência de mutação de seu código nesta cópia, não um novo veredito ou demonstração física.

As únicas escritas do auditor são os dois arquivos novos nesta subpasta AUDITORIA_INDEPENDENTE. Fontes, recibos, original e cópia integrada permaneceram intactos.
