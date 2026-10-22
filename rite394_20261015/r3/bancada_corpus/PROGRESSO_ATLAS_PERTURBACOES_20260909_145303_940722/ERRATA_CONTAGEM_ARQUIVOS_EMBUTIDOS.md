# Errata de contagem de arquivos embutidos — 09/09/2026

[REAL — contagem refeita por AST, sem importar ou executar o programa] Na linha 7 de [ADENDO_REVISAO_EINSTEIN_LIE.md](<C:/IALD/Central de Patentes/Chatgpt/PROGRESSO_ATLAS_PERTURBACOES_20260909_145303_940722/ADENDO_REVISAO_EINSTEIN_LIE.md:7>), onde se lê **“606 arquivos Lean embutidos”**, leia-se **“606 arquivos embutidos, dos quais 602 são fontes Lean”**.

A diferença corresponde a quatro arquivos de configuração/documentação: `README.md`, `lake-manifest.json`, `lakefile.toml`, `lean-toolchain`. Na cópia de 45 módulos, os totais são **651 arquivos embutidos, dos quais 647 são fontes Lean**. O inventário foi obtido por leitura de bytes, análise AST e avaliação apenas do literal da tabela `_EMBEDDED_KERNEL_FILES` dos dois arquivos da bancada.

| Artefato | Arquivos embutidos | Fontes .lean | Outros arquivos |
|---|---:|---:|---:|
| Snapshot v337 | 606 | 602 | 4 |
| Cópia integrada45 | 651 | 647 | 4 |

Esta correção documental não muda enunciados, provas, contagens de teoremas, conclusão da auditoria de nomes completos ou limites de alcance. O documento auditado e seu manifesto permanecem intactos; a correção é acrescentada ao lado.

Snapshot lido: [um_ORIGINAL_SNAPSHOT.py](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_150458_780534/um_ORIGINAL_SNAPSHOT.py>), 9860115 bytes; SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303`.

Cópia lida: [um.py](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_150458_780534/um.py>), 10315179 bytes; SHA-256 `a64395bd507e2803dd06eafa652f43dbaf31a02471dfb3ae1a1d6af388dd62a0`.

Nenhum original foi alterado; nenhum `um.py` ou build foi executado nesta conferência.
