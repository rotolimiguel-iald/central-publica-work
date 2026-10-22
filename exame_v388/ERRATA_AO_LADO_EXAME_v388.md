# ERRATA AO LADO — EXAME_UM_PY_v388 (06/10/2026, em nome da gerência desta sessão)

O relatório `EXAME_UM_PY_v388.md` (sha16 `aedaeb09e32d4207`) e o `.json` (`b033831f6b62a6cc`) ficam como estão, como registro. Corrige-se AO LADO a **NOTA 2** (contagem de pedras da Parte C):

- **Onde se lê:** «o ledger tem 1015 caminhos únicos; … 166 fora do ledger (quase todos TGLExt/O16 …; + PPIndex, SMatrix)».
- **Leia-se [REAL — medido por `ast.literal_eval` do literal `_ESQUELETO_STONES` do um.py v388 `e64b00f4df75059b`]:** o ledger tem **1025** entradas, todas de 5 campos, com **1025 caminhos únicos**. A frase do artigo «1025 pedras em kernel Lean» estava CERTA. O kernel embutido tem 1181 `TGLExt/*.lean`; **156** ficam fora do ledger, **todos** em `TGLExt/O16` (importados da bancada pela ORDEM 016). Nenhuma entrada do ledger fica sem arquivo embutido.
- **Causa do erro:** a regex de linha (`^\s*\("v\d+", "\w+", "…"`) não pegou 10 entradas do ledger escritas em mais de uma linha, entre elas PPIndex e SMatrix. O número corrige a frase.
- **Consequência para a v389:** o item (6) da decisão da c1 («1025 pedras» → 1015) deixa de valer. A frase mantém o 1025, calculado em runtime, e ganha o recorte «+ 156 TGLExt/O16 fora do ledger», também calculado em runtime.
