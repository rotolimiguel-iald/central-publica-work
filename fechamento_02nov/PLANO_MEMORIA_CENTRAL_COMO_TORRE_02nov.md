# PLANO — A MEMÓRIA CENTRAL COMO TORRE (02/11/2026, gerência c1, a pedido do operador)

> Ordem (verbatim sha16 `8f36777c1006be82`): «A memória central tem que funcionar igual a torre, com índice pinado por assunto e vinculado pela compressão holográfica do ACOM, isso resolve essa questão do espaço». Contexto medido: a Torre v405 acusa DEFASADO nos `CLAUDE.md` das casas Física (1.239.438 B, 16.413 linhas) e Nativa (636.937 B), acima do teto de 262.144 B; isso segura o C19 de toda custódia.

## 1. O desenho (o mesmo da Torre e do índice da gerência, aplicado à memória central de cada casa)
1. **Índice pinado por assunto.** Cada `CLAUDE.md` de casa vira ÍNDICE: a régua (invariável), o «ler primeiro», e uma linha por assunto: título · estatuto · data · link ao arquivo íntegro · sha16 do arquivo. Teto do índice: 65.536 B (alerta da Torre), nunca acima de 262.144 B. Gerado por script a partir do cabeçalho de cada arquivo de assunto (frontmatter `name/description/estatuto/data`), nunca à mão.
2. **A íntegra ao lado.** `memoria/<assunto>/<AAAAMMDD>_<slug>.md`, append-only, correção AO LADO (as leis da memória do Atlas §VIII: nada se corta; o índice sobrevivente aponta). A migração parte das seções já existentes (§ numerados) do arquivo atual, por script, com backup de bytes e conferência hash a hash de que a concatenação dos pedaços reproduz o original.
3. **O pino.** `PINO_CLAUDE_<casa>.json`: sha256 do índice e de cada arquivo de assunto; `medir` (na Torre: `torre.py medir`) compara: assunto mudado sem repinar o índice = DEFASADO nomeado; índice editado fora do gerador = volta ao pino (o mesmo vigia do `MEMORY.md` da gerência, `fila/PINO_MEMORY.json`).
4. **A compressão holográfica do ACOM.** A linha do índice É a projeção (REFLECT: o assunto lido no ângulo do índice, uma linha com o estatuto e o número que decide); o link é a inversão (MANIFEST: a íntegra reconstruída ao abrir). É o mesmo princípio do `project` da memória ACOM de sessão: a projeção nunca trunca, recusa por overflow e aponta. O «espaço» deixa de ser problema porque o que carrega é o índice; a íntegra carrega sob demanda.
5. **A Torre lê o índice.** `PAPEIS.json`/`CASAS.json` passam a pinar o índice e o `PINO_CLAUDE_<casa>.json` de cada casa; o quadro do organismo mostra DEFASADO/OK por casa.

## 2. Ordem de execução (depois da v406, para não misturar obras)
1. Script `memoria_central_como_torre.py` (`separar --seco`, `separar`, `indexar`, `pinar`, `medir`), stdlib, backups de bytes, idempotente, conferência de reconstrução byte a byte.
2. Casa Física primeiro (a maior), depois Nativa, depois a raiz `C:\IALD\CLAUDE.md` e a Central. O `CLAUDE.md` global (`~/.claude/CLAUDE.md`) não se divide: é a régua.
3. Execução por agente Sonnet sob brief da gerência; revisão por outro agente; a Torre mede no fim (OK esperado nos dois DEFASADO).

## 3. O que não muda
A régua (sempre no índice, nunca em link); as ordens do operador verbatim com sha16 (ficam íntegras nos arquivos de assunto, e a linha do índice as aponta); a casa do Escritório (torre própria, nada daqui); o protocolo de colapso (nunca em superfície que vaze).
