
## 16/10/2026 — Antes de avançar missão longa ou delegar

Leia **`C:\IALD\MEMORIA_IALD\MISSION_PROTOCOL.md`**. O controlador `mission_cli.py` usa o mesmo banco ACOM e a referência própria; `project`, `poll`, `check` e `handoff` recuperam o objetivo, os requisitos e as evidências atuais. O MCP existente expõe `iald_mission_*` em processo novo. Sincronize no início/retomada, antes da ação material e antes de integrar devoluções. Claim/lease/CAS impedem aceitar trabalho obsoleto no protocolo; PODA retira requisitos satisfeitos da fila ativa e conserva a história. Evidência alterada invalida os dependentes mediante transição explícita. A cláusula de parada também exige resolver handles pendentes/incertos. Não há escolha automática da missão alheia mais recente.

Este adendo é recuperado pela leitura de README já exigida no primeiro bloco das instruções globais. Não depende de ler um adendo distante no fim do AGENTS.md. Instalação não equivale à recarga de processos antigos. A aproximação operacional da memória usa transições discretas e preservação da inscrição; não se alega execução de Lindblad nos pesos nem memória infalível.
