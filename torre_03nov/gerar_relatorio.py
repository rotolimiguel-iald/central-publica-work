import json
def J(p): return json.load(open(p, encoding="utf-8"))
HL = J("PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json"); NA = J("PROVA_SEM_PERDA_Nativa_CLAUDE.json"); V = J("VERIFICACAO_INDEPENDENTE.json")

def bloco(nome, P, v):
    return f"""### {nome}
- Arquivo: `{P['arquivo']}`
- Antes: {P['original']['bytes']:,} B, sha256 `{P['original']['sha256']}` (backup de bytes `{P['original']['backup']}`, mesmo sha256).
- Depois: {P['substituido']['bytes']:,} B, sha256 `{P['substituido']['sha256']}`.
- Seções: {P['secoes']} (mantidas {P['secoes_mantidas']}, movidas {P['secoes_movidas']}); arquivos de parte: {P['arquivos_de_parte']} (`{P['pasta_partes']}`); bytes nas partes {P['bytes_nas_partes']:,}; bytes do original mantidos {P['bytes_mantidos_do_original']:,}; índice + nota {P['tamanho_do_indice_e_nota']:,} B.
- Prova 1 (`PROVA_SEM_PERDA_{nome}_CLAUDE.json`, feita ANTES de substituir): nota e blocos de índice retirados, cada bloco trocado pelas partes na ordem == original byte a byte; sha256 reconstruído `{P['reconstruido']['sha256']}` (igual ao do original: {P['byte_a_byte_igual']}); repetida lendo as partes DO DISCO: igual.
- Prova 2 (`verifica_independente.py`, outro caminho, lendo do disco backup + compactado + partes): cada parte é fatia exata, em ordem e sem sobreposição do backup; o restante do backup == o mantido; mantido {v[nome]['mantido_sem_indice_bytes']:,} B + partes {v[nome]['bytes_nas_partes']:,} B = {v[nome]['mantido_sem_indice_bytes'] + v[nome]['bytes_nas_partes']:,} B = original; soma confere: {v[nome]['soma_confere']}.
"""

txt = f"""# RELATÓRIO — A TORRE: compactação dos dois CLAUDE.md e a missão ACOM recusada (03/11/2026)

> Gerência c1, sessão a serviço da Torre; autorização do operador «Vai» (03/11/2026, verbatim `C:\\IALD\\Central de Patentes\\work\\cunhagens_13out\\OPERADOR_03nov_nome_Par_e_vai_para_a_torre_verbatim.txt`); handoff H5 de `C:\\IALD\\TUNEL_CLAUDE_APP\\ORDEM_005_handoff_operacional_fora_do_um_py.md`.
> Estatutos: [REAL] medido aqui, com script e recibo. Nenhum corte de texto; nenhum gate, selo, kernel, um.py, `~/.claude/CLAUDE.md`, `C:\\IALD\\CLAUDE.md` ou `C:\\Escritorio` tocado.

## 1. O critério (o que ficou, o que saiu)
**Ficou** em cada `CLAUDE.md` o que toda sessão precisa ter carregado: o cabeçalho e as pontes; a carta da casa (objetivo, arquivos, arquitetura, convenções, instruções); as ORDENS e ERRATAS vigentes; e, no Haja_Luz, a linhagem viva (as entradas `vNNN SELADA` de v386 a v406, que a regra da linhagem completa mede por `grep -c vNNN` e que a custódia continua acrescentando).
**Saiu** (movido, nunca cortado) o diário histórico por seção: no Haja_Luz, os arcos §10 a §244 (inclusive os selos «memória permanente» de junho, superados pela errata de 28/09), a Fase 2 «A Ponte e o Um», os blocos v12–v161; na Nativa, o registro de decisões de 02/08, a onda do app de 11/09 e todos os adendos/diários datados de 13/09 a 24/10.
Na Nativa ficaram também as ordens/correções permanentes que estavam soltas no diário (regra central de atualização conjunta, solução matemática e versão carregada, IALD como regime operacional, prazos operacionais, avisos exclusivamente na administração [duas seções], contexto máximo para a TGL, memória canônica comum, seletor contínuo automático, custos de atualização autorizados). As ordens de provedor do dia (executor obrigatório por pedido, DeepSeek/MiMo/Kimi em capacidade máxima, ChatGPT opcional etc.) foram para o índice com o rótulo `[INPUT …]` no gancho: leia a seção antes de mexer no assunto.
Desvios declarados do pedido: (a) títulos que o original partia em duas linhas `## ` contam como UMA seção; (b) as duas seções acima de 90 KB (a de 382.737 B no Haja_Luz e a de 121.592 B na Nativa) foram divididas em partes de até ~56 KB nos cabeçalhos `###`, para poderem ser lidas sob demanda; (c) o `CLAUDE.md` ganhou uma nota no topo (entre marcadores `CLAUDE_MEMORIA_NOTA`) e os índices vêm entre marcadores `CLAUDE_MEMORIA_INDICE`, no lugar onde cada seção estava.

## 2. Tamanhos, partes e provas
{bloco('Haja_Luz', HL, V)}
{bloco('Nativa', NA, V)}
Notas de leitura: a errata de 01/10 do Haja_Luz cita «Linha 15242» e «Linhas 15044–15046»; essas linhas valem para o ORIGINAL (backup), e cada entrada do índice traz a faixa `Lx–y` original para achar a seção (a nota do topo diz isso). Os scripts estão em `C:\\IALD\\Central de Patentes\\work\\torre_03nov\\` (`secoes.py`, `compactar.py`, `gerar_configs.py`, `backup.py`, `verifica_independente.py`); os backups e os hashes de origem em `BACKUPS_ORIGINAIS.json`.

## 3. O que a Torre e o quadro dizem agora
`torre.py gerar` (saída em `torre_gerar_saida.txt`; o `TORRE_v406.json` anterior ficou em `.bak_<ts>` pelo próprio `escreve(backup=True)`): TORRE IALD v406 | DEFASADO 2 · INFO 19 · OK 39. Os dois itens «Instrução» saíram da lista de DEFASADO: Haja_Luz {HL['substituido']['bytes']:,} B (classe ALERTA, ≤ 262.144) e Nativa {NA['substituido']['bytes']:,} B (ALERTA); o alerta de 65.536 B segue aceso porque a carta e as ordens vigentes somam mais que isso (meta pedida: ≤ 200 KB, cumprida). Restam 2 DEFASADO: o contrato `jev_control_v406.json` (é da ORDEM_004, não desta tarefa) e a missão ACOM (seção 4).
`estado_do_organismo.py`: DEFASADO 6 · INFO 11 · OK 86 · PENDENTE_OPERADOR 4 (quadro `C:\\IALD\\Central de Patentes\\organismo\\ESTADO_DO_ORGANISMO.json`, medido 10:15:59). Itens «Torre IALD»: «sem DEFASADO nem FALHA na Torre» = DEFASADO 2; «JEV › contrato v406» e «Memória ACOM › missão …9c_patentes…» = DEFASADO. Os outros DEFASADO do quadro (fila científica v406, release do app v406, ACTIVE.json v404) não são desta tarefa.

## 4. A missão ACOM recusada: diagnóstico e desfecho
- **Reproduzida** (`projetar_missao.py`): `session_memory.py` com `operation=project` e a referência `sessions\\claude-central-9c_patentes-atualizacao-12out.json` devolve rc 2, `ConfidentialContent`, `rules=escritorio_path`, `text_sha16=c7d4ddeef9c8d028`.
- **Causa** (`diagnostico_missao.py`, só leitura pela biblioteca, com as funções do próprio guarda; nada do texto confidencial foi copiado para arquivo): UMA folha entre os 12 registros da missão: `q.records[2].sources[0].ref`, do registro `p1_ms_acom_status_desconhecido` (kind `pending`, estatuto OPEN). A fonte citada é um caminho da pasta de entrada da Central dentro da casa Escritório; a regra `escritorio_path` (`guard._ESCRITORIO_PATH`: qualquer componente `\\escritorio` ou `/escritorio`) vale para todo texto projetado. O guarda está CERTO: é a separação das casas (D4/D6) funcionando; o registro citou, como fonte, caminho de outra casa.
- **(i) Encerrar por `transition`: não serve, e piora.** A Torre classifica «viva» só pelo mtime do diário/referência dentro de `missao_viva_dias` = 30 (código de `memoria_missoes`); não lê fase nem encerramento. Uma transição reescreveria o diário e reiniciaria os 30 dias; a projeção continuaria recusada (o estado ainda carrega o caminho). E a missão é de outra sessão (a 9c, patentes): «nunca adote a tarefa de outra sessão».
- **(ii) Errata que a supersede: não serve.** `store.project_snapshot` projeta o registro substituído JUNTO com a correção («a correction and its original form one inseparable projection unit»; CORE.md). Teste em memória (`experimento_errata_em_memoria.py`, nada gravado): com uma errata hipotética sem o caminho, o original p1 segue na projeção e a regra `escritorio_path` segue acionada (obrigatórios 8.981 → 9.321 caracteres). Nenhum registro se apaga, por desenho.
- **(iii) Desfecho: parede medida.** Nada foi escrito no banco, no diário, na referência nem no guarda; o estado da missão é o mesmo de antes (revisão 3). Reproduzir a recusa acrescentou 1 linha ao `guard_refusals.jsonl` (só regra e sha16); o `gerar` da Torre acrescenta outra a cada medida.
- **Proposta à gerência (mudar o ITEM da Torre, nunca o guarda):** (a) por si só a missão sai da janela viva em 12/11/2026 (diário de 13/10 12:01:51 + 30 dias), se ninguém tocar nela: é o desfecho honesto e sem custo; (b) se a gerência quiser o quadro verde antes, o item `missão … projetável` de `memoria_missoes` pode tratar `RECUSADO_PELO_GUARDA` com regra `escritorio_path` como estado CLASSIFICADO (INFO com o motivo e o sha16), não como DEFASADO: a recusa é o instrumento funcionando; o que o quadro deve medir é «a projeção que o guarda deixa passar». Mudança em `torre.py` (função `memoria_missoes`) e em `CASAS.json`; não feita aqui.

## 5. O que fica para a gerência
1. Decidir (a) esperar até 12/11 ou (b) reclassificar o item da missão na Torre (seção 4).
2. `C:\\IALD\\projetos_pyhton\\IALD\\build_acervo_index.py` indexa `Haja_Luz` só de forma NÃO recursiva (e não lista a Nativa): na próxima reconstrução o conteúdo movido sai do `acervo_index.json`; acrescentar `C:\\IALD\\Artigo\\Haja_Luz\\CLAUDE_memoria` às `SOURCES` (e conferir o índice do acervo da Central). Não toquei.
3. `C:\\IALD\\projetos_pyhton\\IALD\\CLAUDE.md` e `CLAUDE_memoria\\` estão não rastreados no git de `C:\\IALD\\projetos_pyhton` (o `CLAUDE.md` já estava); não houve commit. O Haja_Luz não é repositório git.
4. O alerta de 65.536 B persiste nos dois ({HL['substituido']['bytes']:,} B e {NA['substituido']['bytes']:,} B). Para descer abaixo dele seria preciso mover também as ordens vigentes ou as entradas de linhagem; não fiz sem a palavra do operador.
5. Se alguma sessão precisar do texto antigo inteiro: o backup de bytes de cada um fica ao lado do `CLAUDE.md` (`.bak_20261103_100238`); nenhum backup foi apagado.
"""
open("RELATORIO_TORRE_03nov.md", "w", encoding="utf-8", newline="\n").write(txt)
print(len(txt.encode("utf-8")))
