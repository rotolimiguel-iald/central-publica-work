memoria.py — construído e testado em cópia; nada ligado

# RESULTADO — `memoria.py`, o sistema da fila da memória (26/10/2026)

Agente Sonnet, a pedido da gerência c1, conforme `ROTEIRO_MEMORIA_INTELIGENTE_26out.md` e `memory\fila\README.md`. Medido em 26/10/2026 19:15; todo hash e todo número abaixo foi LIDO por script (régua nº 2). Python 3.14.3, stdlib só.

## 1. Entregas

| arquivo | linhas | bytes | sha16 |
|---|---|---|---|
| `memory\fila\memoria.py` | 1380 | 77.199 | `c4a29337063fb1a8` |
| `memory\fila\testes_memoria.py` | 934 | 55.663 | `0a0b87b33778f401` |
| `work\memoria_inteligente_26out\RESULTADO.md` | este arquivo | | |

Nada foi ligado: nenhuma tarefa agendada, nenhum hook, nenhuma escrita no `MEMORY.md`, em tópico, no pino, no livro ou em `depositos\` do diretório REAL. O real foi só lido (e o `__pycache__` que o meu `py_compile` criou na pasta `fila\` foi removido).

## 2. Testes — 29/29 passaram em 49 s

Comando: `C:\Python314\python.exe -X utf8 C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\testes_memoria.py` (rc 0 = tudo passou).
Cada teste recria `C:\t\mem_teste` do zero (tópicos e `MEMORY_2.md` copiados do real, SEM os `.bak_`; `MEMORY.md` sintético e determinístico; o `memoria.py` copiado) e roda o `memoria.py` DA CÓPIA com `MEMORIA_DIR` apontando para ela. Toda escrita do teste passa por `_seguro()`, que recusa caminho fora de `C:\t\mem_teste` (a guarda já barrou um deslize meu durante o desenvolvimento). O último teste confere que nenhum artefato do `memoria.py` apareceu no real.

| teste | o que prova | resultado |
|---|---|---|
| `test_01_help_em_portugues` | --help em português (geral e de cada comando) | ok |
| `test_02_verificar_passa` | verificar passa na cópia recém-pinada (todos os invariantes) | ok |
| `test_03_depositar_ok` | depositar OK: arquivo com frontmatter, id no formato, linha encadeada no livro, sha da fonte CALCULADO | ok |
| `test_04_depositar_recusa_conteudo_proibido` | depositar recusa (chave, senha, .env, iald_stack, psion, CPF, e-mail, «só entre nós», Escritório) sem ecoar o valor e sem gravar nada | ok |
| `test_05_depositar_valida_campos` | depositar valida quem, tipo, estatuto, alvo, texto e exclusão mútua --texto/--texto-arquivo | ok |
| `test_06_depositar_arquivo_com_espaco_e_acento` | depositar lê --texto-arquivo com espaço e acento no caminho, corpo UTF-8 preservado byte a byte, e '-' lê da entrada padrão | ok |
| `test_10_promover_sem_env_recusa` | promover/adiar/recusar/pinar sem MEMORIA_GERENCIA=claude-c1 (ou com outro valor) recusam e nada muda | ok |
| `test_11_promover_com_env_grava_topico_com_backup_e_repina` | promover com env: append datado AO LADO no tópico, backup de bytes, linha no índice, re-pino (sha+conteúdo), livro com quem | ok |
| `test_12_promover_estoura_195_linhas_recusa` | promover que estoura 195 linhas recusa e diz; nada é gravado; em 194 linhas a promoção cabe (fica em 195) | ok |
| `test_13_promover_estoura_24000_bytes_recusa` | promover que estoura 24 000 B recusa; o limite exato (24 000 B) ainda cabe | ok |
| `test_14_promover_para_topico_novo_e_para_indice` | promover novo:<slug> cria tópico com frontmatter válido; --para MEMORY.md exige --linha-indice e só insere a linha | ok |
| `test_15_adiar_recusar_e_estados` | adiar -> ainda promovível; recusar -> terminal; o depósito fica; o livro guarda quem e o motivo | ok |
| `test_16_promover_recusa_se_indice_diverge_do_pino` | promover só opera sobre um índice que bate com o pino; depois de `pinar` (ato da gerência) volta a operar | ok |
| `test_20_vigiar_ok` | vigiar com o índice igual ao pino: relatório OK, rc 0, nenhum arquivo novo | ok |
| `test_21_vigiar_detecta_linha_estranha_e_so_relata` | vigiar detecta a linha estranha (rc 4), grava VIGIA_<ts>.json com o diff, NÃO mexe no índice, e não repete o mesmo relatório | ok |
| `test_22_vigiar_enforcar_move_as_linhas_e_restaura` | vigiar --enforcar: linhas estranhas VERBATIM em depositos/estranho/<ts>_linhas_estranhas.md, versão estranha em .bak_estranho_<ts>, índice volta ao pino | ok |
| `test_23_enforcar_so_remocao_e_linha_sensivel` | --enforcar com só remoção restaura sem depósito; linha estranha sensível fica verbatim no depósito mas é OMITIDA dos relatórios | ok |
| `test_24_enforcar_sem_espelho_recusa` | --enforcar recusa se o pino não tem conteúdo guardado; nada é alterado; o vigiar simples ainda relata | ok |
| `test_25_enforcar_carencia_e_indice_ausente` | --carencia adia o enforcement de alteração recente; índice apagado é restaurado do espelho | ok |
| `test_30_hash_chain_detecta_adulteracao` | alterar, apagar ou trocar linha do livro quebra a cadeia: verificar/listar acusam; depósito editado também | ok |
| `test_31_verificar_acusa_regua_pino_tracos_e_topicos` | verificar acusa: índice acima da régua, pino divergente, sem MEMORY_2.md, tópico sem frontmatter | ok |
| `test_32_deposito_colocado_a_mao_e_recolhido` | arquivo colocado à mão (README, regra 5) aparece como NAO_REGISTRADO e é RECOLHIDO ao promover; dono errado e segredo são recusados | ok |
| `test_33_projetar` | projetar gera PROJECAO.md com os pendentes, por quem e há quanto tempo; sem mudança não reescreve | ok |
| `test_34_trava_ocupada_e_concorrencia` | duas escritas em paralelo não corrompem o livro (a trava serializa); trava velha de processo morto é retomada | ok |
| `test_35_compare_and_swap_nao_pisa_outro_escritor` | _escrever_atomico(antes=…) aborta se o arquivo mudou no meio do caminho (a gerência editando o índice à mão) e não grava nada | ok |
| `test_36_diretorio_errado_nao_semeia_pastas` | MEMORIA_DIR apontando para um lugar sem fila\ recusa e não cria nada | ok |
| `test_37_vigiar_nao_age_sobre_arquivo_em_mudanca` | com alguém escrevendo no MEMORY.md durante a leitura, o vigiar --enforcar recusa (INDICE_EM_MUDANCA) e não guarda nem restaura nada | ok |
| `test_38_livro_apagado_ou_encurtado_e_visto` | livro apagado ou encurtado em 2+ linhas é acusado (o backup mais recente tem de ser prefixo); o corte só da ÚLTIMA linha é limite conhecido | ok |
| `test_99_o_real_nao_foi_tocado` | nenhum artefato que o memoria.py produz (livro, trava, VIGIA_, PROJECAO, .bak_estranho_, depósitos do estranho) apareceu ou mudou no REAL | ok |

Os oito casos pedidos estão cobertos: depositar OK (03); depositar recusa chave, CPF e «só entre nós» (04); promover sem env recusa (10); promover com env grava tópico com backup e re-pina (11); promover que estoura 195 linhas recusa (12, mais 24 000 B em 13); vigiar detecta e, com `--enforcar`, move e restaura (21, 22); verificar passa (02); a cadeia de hash detecta adulteração (30: campo alterado, linha apagada, linhas trocadas, hash recalculado só na linha adulterada, linha cortada, depósito editado, depósito sumido).

**Os testes mordem?** Rodei 11 mutações do `memoria.py` (cadeia sem a checagem, promover sem exigir a variável, tetos 196/24 001, vigiar sem restaurar, filtro cego a «entre nós», backup sem copiar bytes, depósito editado ignorado, `--enforcar` sem espelho, CPF-11 nunca valida, livro apagado/encurtado ignorado) numa árvore descartável: 11 de 11 mortas pelo teste alvo, nenhuma sobreviveu (`scratchpad\mutantes.py`, não entregue; refazível sob pedido).

## 3. O que o `memoria.py` faz

Saída SEMPRE JSON em stdout; erro = JSON em stderr + rc diferente de 0. Códigos: **0** ok · **2** recusa/erro (fail-closed) · **3** `verificar` achou violação · **4** `vigiar` achou divergência do pino (mesmo quando `--enforcar` a reverteu: o JSON diz `restaurado: true`). `--help` em português em todos os comandos.

| operação | quem | efeito |
|---|---|---|
| `depositar --quem --tipo --estatuto --alvo [--fonte C[=SHA]]... (--texto-arquivo X \| --texto T) [--casa] [--slug]` | qualquer IA | `depositos\<quem>\<AAAAMMDD_HHMMSS>_<slug>.md` com frontmatter + linha no livro `fila.jsonl`; fonte com sha256 CALCULADO do arquivo; recusa conteúdo proibido (fail-closed, sem ecoar o valor) |
| `listar [--pendentes]` | qualquer | estados PENDENTE / PROMOVIDO / ADIADO / RECUSADO, integridade do arquivo, e os `NAO_REGISTRADO` |
| `promover ID --para (tópico.md \| MEMORY_2.md \| MEMORY.md \| novo:SLUG) [--linha-indice L] [--secao S] [--descricao D]` | só gerência | backup de bytes; append datado AO LADO; linha de índice; réguas ≤195 linhas e ≤24 000 B (estourou: recusa e não grava nada); re-pina (sha256 + conteúdo); marca no livro com quem |
| `adiar ID --motivo` / `recusar ID --motivo` | só gerência | marca no livro; o depósito fica |
| `pinar [--motivo]` | só gerência | pina o `MEMORY.md` atual (sha256 + espelho do conteúdo) |
| `vigiar [--enforcar] [--carencia S]` | tarefa agendada | igual ao pino: OK. Diferente: `VIGIA_<ts>.json` com o diff. Com `--enforcar`: linhas adicionadas VERBATIM em `depositos\estranho\<ts>_linhas_estranhas.md`, versão estranha em `MEMORY.md.bak_estranho_<ts>`, conteúdo pinado restaurado; recusa se o pino não tem espelho |
| `verificar` | qualquer | pino bate; ≤195 linhas e ≤24 000 B; regra dos dois arquivos; frontmatter de todos os tópicos; cadeia do livro; nenhum depósito editado ou sumido |
| `projetar` | gerência | `fila\PROJECAO.md` (pendentes, por autor, há quanto tempo); não reescreve se nada mudou |

Livro `fila.jsonl`: `{seq, ts, op, id, quem, estado, sha256_deposito, hash_anterior, hash}` (+ `detalhe` opcional), cadeia SHA-256 conferida por `verificar` (padrão do Mapa de Rotas). Regras duras cumpridas: nada de `open(p,'w')` em arquivo existente (backup de bytes `.bak_<AAAAMMDD_HHMMSS>` -> temporário -> conferir bytes -> `os.replace`; depósito novo por criação exclusiva); trava de arquivo com retomada de trava morta (10 min); ids `<quem>/<AAAAMMDD_HHMMSS>_<slug>`.

## 4. Decisões que a gerência precisa conhecer (além da tabela do roteiro)

1. **Nona operação, `pinar`.** Sem ela não há como pinar depois de uma edição direta do índice (o pós-rito, a compactação) nem como criar o espelho de um pino que não o tem. Exige a mesma variável e deixa linha no livro com o diff contra o pino anterior. Avisa se o pinado está acima da régua.
2. **`promover`, `adiar`, `recusar` e `pinar` exigem `MEMORIA_GERENCIA=claude-c1`** (grava `quem`). `promover` só opera se o `MEMORY.md` BATE com o pino: edição fora da promoção ainda não vigiada recusa com `PINO_DIVERGENTE` ("rode vigiar; se foi a gerência, pinar"). Assim uma promoção nunca abençoa linha estranha sem querer. **Consequência prática:** toda edição direta do índice pela gerência (inclusive o pós-rito da v402) deve terminar com `pinar`.
3. **Depósito colocado à mão** (regra 5 do README, já em uso pelo Codex): `listar` mostra `NAO_REGISTRADO`; `promover`/`adiar`/`recusar` o RECOLHEM antes (linha `recolher` no livro, com o sha256 do momento), passando pelas mesmas portas do `depositar` (frontmatter, dono da pasta = campo `quem`, varredura proibida). Enquanto não recolhido, o autor ainda pode editá-lo.
4. **Vigia e arquivo em mudança:** só age sobre divergência estável (duas leituras com 0,3 s de intervalo), reconfere antes de gravar e antes de restaurar (compare-and-swap); `--carencia S` (padrão 0, como no roteiro) adia o enforcement de alteração mais nova que S segundos. Mesma divergência não gera relatório repetido. Linha estranha com padrão sensível fica verbatim no depósito `estranho` (com `padroes_sensiveis:` no frontmatter) mas é OMITIDA dos relatórios JSON.
5. **Promover é tudo-ou-nada até onde dá:** monta e valida tudo (régua, seção, existência do tópico) antes de gravar; reconfere o índice e o tópico imediatamente antes da primeira escrita; escrita com compare-and-swap. Falha no meio diz o que já foi feito e onde estão os backups.
6. **Extras opcionais:** `--secao` (padrão "Estado corrente"; a linha entra ao fim da seção, o resto do índice fica byte a byte igual), `--descricao` (tópico novo), `MEMORIA_DIR` (outro diretório de memória; recusa se não existe e nunca cria a fila). Depósito até 65 536 B; detalhe grande fica em arquivo citado por `--fonte`.

## 5. Medido no estado REAL (só leitura), 26/10/2026 19:15

- `verificar` no real: rc 3; violações: PINO: o MEMORY.md (sha256 fb77245d785a1158…) difere do pino (d7525d5c5d1070b2…): rode `memoria.py vigiar`; se a alteração foi da gerência, `memoria.py pinar`. `MEMORY.md` real: 194 linhas, 23144 B. Livro `fila.jsonl` do real: 0 linha(s) (ainda não existe). Depósitos colocados à mão e ainda não recolhidos: 4.
- **Os depósitos reais do Codex passam nas portas:** [('codex-coordenadora', []), ('codex-coordenadora', []), ('codex-gerente-tgl', []), ('codex-video-v7', [])] (listas vazias = nenhum padrão proibido). Frontmatter, dono da pasta e fontes (existem e o sha confere) validados por script.
- **Ensaio numa cópia do estado real** (feito às ~19h, índice então com 194 linhas; a cópia foi apagada): `vigiar` apontou exatamente a linha que a gerência acrescentou depois do pino; `pinar` abençoou; dos quatro depósitos do Codex, UM coube (194 -> 195 linhas) e os outros três foram recusados por `REGUA_ESTOURADA` (196 linhas), sem gravar nada. Com o índice nessa altura, promover mais de um depósito exige compactação antes (ato da gerência, não da fila).
- **Calibragem do filtro fail-closed** sobre o texto da própria casa: 22 dos 237 tópicos existentes seriam recusados se fossem depósito (dotenv 12, casa_escritorio 9, email 6, iald_psion_state 5, iald_stack 5, so_entre_nos 2, cpf_formatado 1, cpf_11_digitos_valido 1); são menções legítimas de nomes confidenciais em memórias antigas, não vazamento — e confirma que o filtro é conservador. Falso positivo concreto achado: um número de 11 dígitos sem separador que, por acaso, fecha os dígitos verificadores de CPF (o tamanho em bytes do arquivo do KiDS, `17712469440`, é um deles); escrito como `17.712.469.440` passa. Achado lateral, sem valor ecoado: o filtro viu um número com cara de CPF em `escritorio-miguel.md` e um CPF formatado em `epct-protocolo-15.md` — conferir se é dado pessoal fora do lugar.

## 6. Limites declarados (a régua)

- `MEMORIA_GERENCIA` é **cerca de disciplina, não autenticação**: qualquer processo do usuário pode defini-la. A rede de segurança é o vigia (pino + espelho + restauração) e o livro encadeado.
- A cadeia de hash detecta alteração e remoção no MEIO do livro; `verificar` acusa também o livro apagado ou encurtado em 2+ linhas (o backup mais recente tem de ser prefixo do livro). **Não detecta o corte só da ÚLTIMA linha** (o livro vira exatamente o backup anterior; o depósito correspondente aparece como `NAO_REGISTRADO`) — teste 38 documenta o limite.
- O vigia cobre só o `MEMORY.md` (como no roteiro). `MEMORY_2.md` e tópicos não são vigiados; `verificar` só confere a existência do segundo e o frontmatter dos tópicos.
- O filtro de conteúdo é heurístico (lista em `PADROES_RECUSA`, no topo do arquivo, documentada); não substitui o `GUARD` da ACOM nem a revisão da gerência. «entre nós» também pega a casa "Nós" em "entre Nós e …" (escrever "a casa Nós").
- Não testado: carga prolongada, volume grande de depósitos (o `listar` relê e re-hasheia todos), Windows com antivírus segurando o arquivo além dos 2 s de tentativas do `os.replace`, e a tarefa agendada real (não criada). Os testes cobrem concorrência de 6 processos e a recusa de arquivo em mudança, não toda corrida possível.

## 7. Próximos passos sugeridos (todos da gerência; nada foi feito)

1. Revisor independente (Opus) lê `memoria.py` antes de ligar o vigia (item 3 do roteiro).
2. Com o `MEMORY.md` legítimo: `MEMORIA_GERENCIA=claude-c1 python memoria.py pinar --motivo "primeiro pino do sistema"` (cria também o espelho e a primeira linha do livro). No instante da medição o pino real já tinha espelho, mas divergia do índice (seção 5).
3. Tarefa agendada (item 7, modo sombra 48 h), ação: `C:\Python314\python.exe -X utf8 C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\memoria.py vigiar` a cada 30 min (o caminho não tem espaço). O Agendador não guarda o stdout; a evidência persistente é `VIGIA_<ts>.json` + a linha `vigiar` no livro (só quando há divergência). Item 8, depois do aceite: acrescentar `--enforcar --carencia 120`.
4. Trocar no `fila\README.md` a regra 5 ("enquanto memoria.py não existir") pelo comando `depositar`; exemplo para a ORDEM 026: `memoria.py depositar --quem fila-cientifica --tipo project --estatuto REAL --alvo MEMORY_2.md --fonte "<caminho>\DELIVERY_R1.json" --texto-arquivo "<caminho>\deposito.md"`.
5. O pós-rito da v402 termina com `memoria.py pinar --motivo "pós-rito v402"`, ou promove pelo `promover`.

## 8. ACOM

A inscrição da tarefa na memória ACOM foi tentada (`init` com o texto integral) e **recusada pelo guard**: `rules=psion_name,stack_name,dotenv_name`, `text_sha16=d05441d972a6625b`. O próprio texto da tarefa cita os nomes que a ferramenta deve recusar. Não inscrevi versão redigida (seria outro texto); trabalhei sem referência própria, e o prompt da gerência é a fonte.


---

## CORREÇÕES DA REVISÃO (26/10/2026, depois das 19h30) — AO LADO: as seções 1–8 acima ficam como entregues

A revisão independente (`work\memoria_inteligente_26out\revisao\REVISAO_MEMORIA.md`) deu **PODE_LIGAR_EM_SOMBRA** e exigiu as correções abaixo antes do
enforcement. **Vale para a versão instalada agora**; as seções 1–8 descrevem a versão entregue às 19h13 (`memoria.py` `c4a29337063fb1a8`, `testes_memoria.py`
`0a0b87b33778f401`), guardada em backup de bytes na mesma pasta (`memoria.py.bak_20261026_193418`, `testes_memoria.py.bak_20261026_193418`; deste arquivo: `RESULTADO.md.bak_20261026_193418`).

| arquivo | linhas | bytes | sha16 |
|---|---|---|---|
| `memory\fila\memoria.py` | 1519 | 87.642 | `7c4fc5853f41f1d3` |
| `memory\fila\testes_memoria.py` | 1153 | 70.399 | `460fc43cfef6e590` |

Os dois foram desenvolvidos numa árvore descartável (`C:\t\dev_memoria`), testados lá, e só então trocados em `memory\fila` de uma vez (temporário -> conferir bytes -> `os.replace`, depois de
conferir que o instalado ainda era o entregue). Nada foi escrito no `MEMORY.md`, nos tópicos, no pino, no espelho, no livro nem em `depositos\` do diretório real.

### O que mudou, item por item
- **M1 (obrigatória) — sem restauração automática.** `_escrever_atomico` não restaura mais do backup. Depois do `os.replace` só confere e relata: se outro escritor
  mudou o arquivo logo depois do nosso replace, o novo e a escrita alheia SOBREVIVEM, o estado anterior continua no `.bak_` e o erro (`INTEGRIDADE`) diz onde ele está e que NADA foi restaurado
  (a decisão é da gerência). Vale para todo arquivo que o programa reescreve (índice, tópicos, pino, espelho, livro, cabeça). Teste 39: dois escritores (hook no `os.replace`), um único replace, os dois conteúdos presentes.
- **C2 — `fila\CABECA.json {seq, hash, ts}`.** Gravada por `_acrescenta` DEPOIS do livro (backup -> temporário -> replace) e exigida por `verificar` (`checks.cabeca_do_livro`). Estados: `ok`;
  `atrasada` (o livro tem linhas além da cabeça — queda entre as duas gravações; só aviso, a próxima gravação cura); `ausente` (`CABECA_AUSENTE`: livro não vazio sem cabeça);
  `cortado` (`LIVRO_CORTADO`: o livro tem MENOS linhas que a cabeça — o corte da última linha, ou o livro apagado); `divergente`/`ilegivel` (`CABECA_DIVERGE`). **Não se cura em silêncio:**
  `depositar`, `listar`, `promover`, `adiar`, `recusar`, `projetar` e `vigiar --enforcar` leem o livro conferido (cadeia + cabeça) e RECUSAM com esses códigos antes de gravar qualquer coisa;
  o `vigiar` sem `--enforcar` continua relatando a divergência do índice (grava o `VIGIA_<ts>.json`, mas a linha do livro só se o livro estiver íntegro, e o relatório traz `livro_erro`).
  **Só o `pinar` (ato da gerência) adota um livro SEM cabeça** — a migração de um livro nascido antes da cabeça — e registra `cabeca_adotada` no livro; livro cortado/reescrito nem o `pinar` adota.
  O teste do backup-prefixo (38) fica como segunda linha de defesa e agora também vê o corte da última linha pela cabeça. Teste 40 cobre: corte da última linha, recusa de gravar em livro cortado,
  cabeça ausente + adoção pelo `pinar`, cabeça atrasada (aviso e cura), cabeça com hash errado e cabeça ilegível.
- **C3 — o filtro «entre nós».** `so_entre_nos`: «só/fica entre nós» e «só/fica entre a gente», em qualquer caixa. `entre_nos`: «entre nós» só com n minúsculo (ou tudo em maiúsculas); **«entre Nós» (a casa) PASSA**.
  Medido no teste 41: aceitos "sincronizar entre Nós e Haja_Luz", "Entre Nós, a casa do kernel…"; recusados "só entre nós", "SÓ ENTRE NÓS", "so entre nos", "fica entre nós", "só entre Nós", "fica entre a gente",
  "só entre a gente", "uma conversa entre nós dois", "Entre nós, sem registro", "ENTRE NÓS" (nenhuma frase é ecoada no erro).
- **C4 — `fila\PAUSA_VIGIA.json`.** Formato: `{"quem": "...", "ate": "2026-10-26T20:30:00-03:00", "motivo": "..."}` (`ate` em ISO — sem fuso vale hora local — ou epoch). Enquanto ATIVO, `vigiar --enforcar`
  só relata (`estado: DIVERGENTE_EM_PAUSA`, `enforcado: false`, relatório com a chave `pausa`): não guarda, não restaura, não cria depósito. Expirado: o enforcement age como sempre. **Na dúvida não restaura:**
  marcador ilegível conta como ativo; e nenhuma pausa vale mais de 4 h a contar da criação do arquivo (`limitada_pelo_teto`), para a pausa esquecida não desligar o vigia para sempre. `verificar` avisa que o
  arquivo existe. **O pós-rito da cadeia de selo deve** criar o marcador ANTES de escrever o `MEMORY.md` e removê-lo DEPOIS de `pinar` (o programa não cria nem remove o marcador). Teste 42 cobre
  pausa ativa, expirada, ilegível, esquecida (5 h) e ausente.
- **C5 — uma só conta de linhas.** `_medida` conta `b"\n"` (a conta do pós-rito e do `wc -l`), não `splitlines`: a última linha sem quebra não conta. Documentado em `_medida` e no cabeçalho do arquivo.
  Teto 195 e pino usam essa conta. Teste 43: 195 linhas visíveis com 194 quebras = 194; 195 quebras + cauda sem quebra = 195 (cabe; a conta antiga recusaria); 196 quebras recusa; `promover` usa a mesma conta.
- **M3 — `--carencia` padrão 1800 s** (era 0). O `--help` diz o padrão; `--carencia 0` age já. Os testes que querem agir na hora passam `--carencia 0`. Teste 44: sem o argumento, alteração recente -> `DIVERGENTE_EM_CARENCIA` com `espera_s`
  entre 1700 e 1800, nada tocado; com o arquivo "de 31 min atrás", restaura.

### Testes e mutação
- **35/35 passaram em 68 s**, rodando `testes_memoria.py` DA PASTA INSTALADA contra `C:\t\mem_teste` (o último teste confere que nenhum artefato do `memoria.py` apareceu no real): os 29 anteriores
  (três adaptados para `--carencia 0` — 22, 23, 37 —, o 38 e o 02 ajustados à cabeça, o 99 com a assinatura da cabeça e da pausa) mais **6 novos: 39 (M1), 40 (C2), 41 (C3), 42 (C4), 43 (C5), 44 (M3)**.
- **Mutação: 23 de 23 mutantes mortos pelo teste alvo, nenhum sobreviveu** (os 13 anteriores, com âncoras atualizadas, mais 10 das correções: restauração automática de volta, livro cortado aceita gravação, `verificar` sem exigir a cabeça,
  cabeça nunca gravada, `pinar` sem adotar, pausa ignorada, pausa sem teto, marcador ilegível inativo, `splitlines` de volta, carência padrão 0).

### O que muda para o sistema AO VIVO (medido, só leitura, depois da instalação)
- **O livro real (2 linhas, `vigiar` 19:16 e `pinar` 19:18) nasceu antes da cabeça.** `memoria.py verificar` no real devolve rc 3 com **uma** violação: `CABECA_AUSENTE`; as demais checagens passam (pino bate, 192 linhas / 22.938 B,
  tópicos íntegros). Enquanto a gerência não rodar `MEMORIA_GERENCIA=claude-c1 python memoria.py pinar` (que ADOTA o livro atual e grava a primeira `CABECA.json`), `depositar`, `listar`, `promover`, `adiar`, `recusar`,
  `projetar` e `vigiar --enforcar` recusam com `CABECA_AUSENTE`; o `vigiar` sem `--enforcar` segue relatando. Não adotei o livro por conta própria: é ato de atestação da gerência.
- O `PINO_MEMORY.json` existente continua válido (a chave `linhas` passa a ser contada por `b"\n"` nos próximos pinos; para arquivo terminado em quebra de linha é o mesmo número).
- O pós-rito (M2 estrutural) continua da gerência: escrever pelo `memoria.py` (item 9 do roteiro) ou tomar a pausa. A pausa só protege se o pós-rito a criar; sem ela, a defesa é a carência de 30 min, o compare-and-swap e a regra "toda edição direta termina em `pinar`".
- Resíduos declarados: o crescimento dos `.bak_` continua ilimitado por desenho (nunca apago backups); `CABECA.json` ganha um `.bak_` por acréscimo (pequeno); a cerca `MEMORIA_GERENCIA` continua sendo disciplina, não autenticação.
