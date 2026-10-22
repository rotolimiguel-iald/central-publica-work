# Memória operacional comum da IALD

[REAL — infraestrutura local] A mesma biblioteca atende app, JEV, fila e sessões. O estado único fica em `C:\IALD\MEMORIA_IALD\state`; cada tarefa tem identidade e escopo próprios. Memória comum não mistura usuários, casas ou tarefas. O chamador autentica o titular; a biblioteca verifica a partição recebida.

A primeira inscrição conserva os bytes originais. O estado q reúne fatos, decisões, evidências, pendências e candidatos com origem e estatuto. O fluxo p reúne fase, próxima ação e identificadores de execução. Toda alteração é transacional, com revisão esperada, evento idempotente, backup imediato e cadeia verificável. Correções ficam ao lado da inscrição e do registro anterior.

## Uso pelas sessões locais

Consulte `SESSION_MEMORY.md` para JSON e vínculo de sessão. O CLI instalado é `C:\Python314\python.exe -X utf8 C:\IALD\MEMORIA_IALD\session_memory.py`, com um JSON por stdin. Inscreva o comando autorizado integral em arquivo UTF-8, calcule o SHA-256 dos bytes e use init com actor.kind=agent, scope e request_id próprios. Preserve a referência devolvida e transmita seu caminho exato nos handoffs.

Antes de agir e depois de compactação, retomada ou troca de executor, use project com a referência própria. Ao concluir uma etapa material, registre q com fonte/estatuto e p com a próxima ação por transition. Não adote o contexto mais recente de outra tarefa. Falha ou conflito exige leitura e conciliação explícita; não autoriza repetir uma chamada remota incerta.

Objetivo, restrições, fluxo e todos os registros consolidados são obrigatórios na projeção. Candidatos opcionais podem ser omitidos, com IDs declarados e recuperação integral por get; nenhum registro é apagado. Se o obrigatório não cabe, a operação recusa com required_chars. Um resultado de modelo permanece candidate/DECLARADO até verificação pela autoridade apropriada.

## Integrações e evidência

`CORE.md` descreve o contrato Python, custos e limites. `SESSION_MEMORY.md` descreve o CLI e os hooks opcionais. Os recibos de implantação em `C:\IALD\Central de Patentes\work\iald_memoria_acom_20261010` determinam quais adaptadores já estão instalados. Presença desta biblioteca sozinha não demonstra que todos os processos a carregaram. MCPs científicos antigos continuam sem reinício, conforme decisão do operador; para a fila use o CLI absoluto em processo novo até recarga confirmada.

Hooks de Codex/Claude exigem vínculo e confiança próprios. Exemplos revisáveis não são hooks ativos. O protocolo explícito das sessões independe de afirmar consumo automático. Nunca alterar trust ou permissões para contornar aprovação.

A implementação é uma adaptação simbólica e auditável da ideia ACOM, baseada em inscrição, estado e fluxo. Não altera pesos ou KV-cache dos provedores, não garante eliminação de alucinações e tem custo de armazenamento, projeção e tokens. Backup e replay completos crescem com o acervo. Nenhum kernel, gate, selo ou original científico é alterado por esta infraestrutura.

## 16/10/2026 — Antes de avançar missão longa ou delegar

Leia **`C:\IALD\MEMORIA_IALD\MISSION_PROTOCOL.md`**. O controlador `mission_cli.py` usa o mesmo banco ACOM e a referência própria; `project`, `poll`, `check` e `handoff` recuperam o objetivo, os requisitos e as evidências atuais. O MCP existente expõe `iald_mission_*` em processo novo. Sincronize no início/retomada, antes da ação material e antes de integrar devoluções. Claim/lease/CAS impedem aceitar trabalho obsoleto no protocolo; PODA retira requisitos satisfeitos da fila ativa e conserva a história. Evidência alterada invalida os dependentes mediante transição explícita. A cláusula de parada também exige resolver handles pendentes/incertos. Não há escolha automática da missão alheia mais recente.

Este adendo é recuperado pela leitura de README já exigida no primeiro bloco das instruções globais. Não depende de ler um adendo distante no fim do AGENTS.md. Instalação não equivale à recarga de processos antigos. A aproximação operacional da memória usa transições discretas e preservação da inscrição; não se alega execução de Lindblad nos pesos nem memória infalível.
