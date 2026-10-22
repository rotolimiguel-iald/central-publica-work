# Derivação prévia049 — infraestrutura de verificação
[INPUT — contrato da bancada; implementação ainda sem rodada final]

Todos os módulos deste lote são novos, com importação local fechada entre os fontes049 e dependências externas Mathlib/stdlib. Não há dependência de oleans históricos Chatgpt nem fallback ao kernel canônico. A matemática anterior motiva o alvo, mas não será falsamente contada como fonte recompilada neste lote.

O runner copiará bytes dos fontes para uma pasta exclusiva, validará declarações, prints e ausência de escapes de prova/linters desligados, ordenará dependências locais e compilará cada módulo seguido do importador conjunto. Os imports externos diretos e respectivos artefatos companheiros serão medidos, junto com executável/configurações da ferramenta; esta fronteira é declarada e não equivale a recompilar Mathlib nem medir toda sua dependência transitiva.

Um snapshot congelado de fontes originais, cópias, derivações, runner, ferramenta e dependências externas diretas será comparado antes/depois de cada compilação e da rodada. Logs, oleans, metadata, ordens de compilação e hash de todos artefatos próprios serão preservados. Desenvolvimento usa pasta e marcador novos, sem sobrescrever a evidência. O marcador final só nascerá após todas etapas passarem.

O auditor independente verificará contagens, provas sem sorryAx, apenas propext/Classical.choice/Quot.sound, caminhos autorizados e evidências por hash. A revisão matemática vinculará o hash do marcador final; o relatório final não amplia o alcance para Δ^it/BW/rede/H3. O manifesto sela arquivos próprios e evidências correspondentes, sem alterar originais, canônico, gate, Atlas ou índice.
