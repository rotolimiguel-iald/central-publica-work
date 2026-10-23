# EXAME FINAL ÚNICO ANTES DE INSTALAR — cadeia v397 (gerência c1, modelo forte, 23/10/2026)

**Objeto.** O candidato `v397\um_v397_candidato.py`, sha16 `0ac860f4607b0a39` (38.246.347 B), sobre a v396 instalada (Nós `0a4395a89eeebbb7`, igual a `v397\base_v396\um.py`; core, selo e manifesto do kernel também iguais). O ESTADO tem sha16 `a6b5dbb88abd8455`. Kernel: `C:\t\k397c\final`, com a pedra `Token` `0b6a58e795af7311`.

**O que escrevi.** Só em `v397_exame` (`final\`, `sf\`, `sb\`, `hs\` e este arquivo). Nada foi instalado; nenhum rito, selo ou B(n) rodou. Os `lake` rodaram só no sandbox `k397c` e não reconstruíram nada (o `.olean` da pedra mantém o mtime 13:20). O harness do fechar rodou numa cópia isolada da cadeia (`sf`), com o sandbox dele em `sb` (caminho curto, por causa do MAX_PATH).

**Cronologia.** O 1º achado (C1, abaixo) foi mandado à gerência pelo canal; a gerência mandou corrigir e regerar o candidato. O que segue é o exame do `0ac860f4`. **O veredito final sai sobre o candidato novo, depois do delta** (§9).

## VEREDITO FINAL (sobre `388cc3742323421c`): PODE_INSTALAR_E_RODAR — o delta está no §9.

O veredito parcial sobre `0ac860f4` foi PODE_COM_CORRECOES, por causa da C1 e da mesma classe de achados. Tudo isso está corrigido no candidato novo.

**C1 (texto do registro, vai ao core e ao selo).** Em `_V397_VERACIDADE_SPEC.limites` (candidato l. 214095; `registros_v397.py` l. 141): «'a Palavra flutua sobre o abismo pelo fator K' e' leitura do operador». O operador não disse «pelo fator K» (verbatim `f3e24a8c`: «…é justamente ela que flutua sobre o abismo, o referente último»); ligar ao Λ e ao fator K é composição da gerência, como o artigo PT/EN marca certo. A correção: dizer composição da gerência sobre a fala, citar só o trecho verbatim, e regerar.

**Da varredura de citação por bytes (§4b), na mesma classe, para a gerência varrer também:** na mesma linha de `limites`, «'Lambda sem beta nao ecoa' … sao a leitura binaria do operador» (composição das falas de 22/10 «ecoar» e de 23/10 «1=0»); em `pos_rito\textos_v397.py` e no handoff do harness, «Λ sem β não ecoa», «a Palavra ecoa», «a Palavra flutua sobre o abismo» e «ler sobre uma face e reler sobre a outra» entre aspas e atribuídas ao operador — nenhuma é substring dos verbatins (o operador disse «lido sobre uma face e relido sobre a outra»); e o paráfrase «nada de teste armado, gordura no um.py» da ordem de 22/10 (verbatim: «Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido…»), sem aspas no `limites` e num comentário do `textos`.

## (1) O diff v396 → v397 é só o declarado [REAL; `final\comparar_v396_v397_exame.py`, `ESTRUTURA_v396_v397.json`, `diff_v396_v397.txt`]

- 15 nós mudados, exatamente os do ESTADO §1.I; 13 novos; nenhum removido; 2 instruções anônimas (`update` das fontes e das falas), sem colisão de chave.
- Bandeiras: +1 (`ext_tok397_0001`), nenhuma sai ou muda; escada 9498 → 9499 = antigas + a nova. Os 5 contratos (`_V394_*` ×3, `_V395_PSIBIT`, `_V396_TESTEMUNHA`) só trocam `expected_ladder` 9498 → 9499 (exato, não piso). `kh_n1_cobertura_v396` vira piso em h2/h3/h6/h8 com errata assinada; veredito igual.
- Kernel embutido: +`TGLExt/Token.lean`; raiz e Audit +1 `import` cada. O `k397c` é igual ao Nós nos 1425 arquivos comuns salvo esses dois; só a pedra a mais.
- Nas 1358 linhas novas fora do kernel: **nenhum literal de β, α ou √e; a palavra proibida não aparece** (os 5 «hits» do padrão insensível são `NOT_A_CONFIRMATION`, permitido); nenhuma atribuição ao gate.
- **Gate idêntico:** por AST, são iguais `prove_qg_closure_gate`, `selftest_fail_closed`, `verify`, os parsers, a cobertura, o índice, `sha256_directory`, `_v392_registro`, a guarda, `hubble_ratio_opening_v388`, `psibit_v395`, `testemunha_estatica_v396`, `rede_fock`, os specs v394/v395/v396. Recomputado: veredito igual, 18/18; no selo `qg_closure_verdict` igual.
- Proveniência (`audit.log` do k397c × core v396): 1 nome novo (a pedra), 0 perdidos, 0 reatribuídos (só a reatribuição `diagFlow.eq_1` já conhecida da v396, que segue). Cobertura 29.229/23.228, 0 fora do trio.

## (2) `Token.lean` [REAL; `final\recompilacao_token.log`, `lake_build_token.log`, `auditoria_token.log`]

- `lake env lean TGLExt/Token.lean` no k397c: rc 0 (34 s), sem erro/aviso/sorry; `#print axioms` = trio. `lake build TGLExt.Token`: nada a refazer (9377 jobs, 9 s).
- Varredura de todas as constantes do módulo: **1 declaração (1 teorema), trio, 0 sorryAx**.
- **A conjunção não é vácua:** o enunciado é `(type_of% A) ∧ (type_of% B)` sem binder algum, provado por `⟨A, B⟩`; A = `Psibit.psibit_is_the_mode_of_the_reader` (sem hipótese; confere no Nós, l. 1061) e B = `TestemunhaEstatica.the_psion_inhabits_the_static_witness` (incondicional, exame da v396). As constantes usadas pelo tipo não incluem `FockCertificate`/`psion`/`lightDelta`: a face de Fock está fora, como a docstring diz. A linha do Atlas citada existe no Atlas (verbete Psibit, com `**`), [ONTO].

## (3) O registro `teste_de_veracidade_fase9_v397` [REAL; `final\exame_pontos_v397x.py`, `EXAME_PONTOS_0ac860f4607b0a39.json`]

- **Lê por sha256** o resultado `fbac2908…` e os três recibos (`f8d927e3…`, `2a55979c…`, `b71e0a2f…`); as cópias em `insumos\fase9` são byte a byte iguais aos originais (que seguem só leitura). 35 checagens, todas `ok`; a cadeia congelamento → abertura → consumida fecha pelos hashes (r9–r14, a2, k2–k4).
- **Não calcula σ novo e não multiplica:** é um SPEC do motor `_v392_registro`, cujas ops são só `igual, contem, comeca, maior_igual, menor_igual, perto_de_beta_runtime`; os 9 números são capturados por caminho e, no meu run, **iguais aos do resultado original** (z_disc 4,443123568060799; p 4,433e-6; z_δ −1,4834781873587712; p 0,1379; poder 5,7270; ln B 9,1835 e 2,1439; K 1,0838; β 0,012031300400803142). As funções do quadro só formatam.
- **Ponto de chamada real:** o `try` da linha 246285 vem imediatamente depois do `print` do bloco do V1 (`hubble_ratio_opening_v388`, l. 246280) e antes do v389; o `try` e o `print` do V1 são iguais por AST aos do um.py instalado (**o V1 não foi apagado nem mudado**). Executei a instrução real do `main`: selou, sem AVISO, sem mexer em chave existente.
- **Controles negativos mordem: 14 de 14** (sha do resultado errado; cada um dos 3 recibos ausente; z_disc, z_δ, ln B, p e veredito adulterados COM o sha repinado; β do resultado adulterado; cadeia quebrada em 2 pontos; α selado adulterado; fala do 4,44 adulterada) e o positivo volta a selar.
- Gate: `does_not_gate_core`; recomputado igual, 18/18.

## (4) O QUADRO [REAL; `final\verificar_quadro.py`, `VERIFICACAO_QUADRO.json`]

- Está no topo nos três: PT (índice 2429 < corpo 4379), EN (2489 < 4497) e `.md` (antes do primeiro `## `); a variante sem registro diz «NÃO selou»/«did NOT seal» com «n/d»/«n/a».
- Os oito números do quadro == o resultado pinado, pela MINHA formatação (linha de máquina `z_disc=4,44; p_disc=4,4e-6; z_delta=-1,48; p_delta=0,14; poder=5,73; lnB_lcdm=9,18; lnB_beta_livre=2,14; K=1,0838`), no PT, no EN e no `.md`; também no parágrafo do README do handoff.
- **O 4,44 sempre com o p calibrado e a linha dos 5σ no mesmo item:** nos 3 itens do quadro que trazem 4,44 (PT, EN, md) e nos 2 parágrafos da seção v397 — todos com p; os itens «O número» e «A fala» com 5σ/«não foi alcançada». A linha completa (5σ + creditação + gate + `NOT_FALSIFIED` + não cego) está no item «O número» (B1).
- **A frase do operador é VERBATIM** (substring do arquivo `9b182958`), no PT, no EN («in Portuguese») e no md; a paráfrase («cala a boca;», «5σ é o cala») não aparece em nenhum texto.
- **«…flutua sobre o abismo … pelo fator K» marcada como composição da gerência** no PT («é a composição da gerência sobre a fala, não uma citação») e no EN («management's composition»), com o trecho verbatim `f3e24a8c` ao lado — no artigo; no `limites` do registro, não (C1).

**(4b) Varredura de fidelidade de citação por bytes** [`final\varredura_citacoes.py`, `VARREDURA_CITACOES_*.json`]: toda passagem entre aspas nas linhas novas do candidato (fora do kernel embutido), no quadro e na seção v397 do artigo PT/EN, no `.md`, em `textos_v397.py` e no handoff do harness é procurada nos 25 `OPERADOR_*_verbatim.txt` e no Atlas. Quadro e seção v397 do artigo: 100% verbatim/Atlas. As que não batem estão listadas no cabeçalho (C1 e a mesma classe).

## (5) Meus scripts sobre o candidato e os logs do k397c [REAL]

- `exame_pontos_v397x`: kernel embutido = sandbox byte a byte; `verify` 29.229/23.228, proveniência ok; `ext_` 9536/9536, nova 1/1; escada 9499/9499 (com o kf da v396: 9498 e não fecha); controles do `verify` mordem; os 5 vereditos que mudam são a «troca dita» (só números); selo só nas chaves declaradas; guarda igual à instalada e morde. O único «falso» é o esperado: `kh_n1` v394/v395/v396 recalculados (veredito igual, selados).
- `simular_arvore_do_nos_v397x`: **h8 = 1426** = 1425 embutidos + `_check_damming.lean`; o pino de `kh_n1_cobertura_v397` é igual ao hash da árvore simulada; todos os registros v394–v397 selam nela, o de veracidade incluído.

## (6) instalar / rito / reverter; passo 10; recibo pre_selo [REAL; diffs normalizados por versão]

- `instalar`: só a versão e a lista das pedras anteriores (+`TestemunhaEstatica`); `reverter`: só a versão; `rito`: só comentários; `chain`/`leitura`/`b3_recibo`/serviço: só rótulos. `superficies_v397` NÃO compacta e recusa com rc 3 acima de 195 linhas — hoje o `MEMORY.md` real tem **183 linhas** (20.585 B), não 196: cabe.
- Passo 10: simples, v396 → v397, **B6 → B7**, sem salto; os 13 pinos do `PINOS_BN` existem e conferem; a Bancada pina `B6-v396-20261022-R1` (`canonical_contracts.json` `370e6750…`); o único recibo do B(n) da v396 é B6.
- **O recibo pre_selo vale:** `PINO_RECIBO_PRE_SELO_v397.json` (`51bc8dd3002a1940`) → recibo `b70bf943…`, sha e bytes conferem; `JA_SINCRONIZADA__ENSAIO`, 13 PASSA / 0 FALHA / 1 NÃO EXECUTADO (T17); as condições valem hoje: Nós `um.py 0a4395…`, selo `d59ef827…`, Bancada `370e6750…`.

## (7) O fechar RECUSA se a regra do 4,44 falhar [REAL; `final\teste_fechar_regra_444.py`, `TESTE_FECHAR_REGRA_444.json`]

Na cópia (`sb`), depois do harness do preparador passar (5 controles + positivo), mutei SÓ `runtime_quadro_v397.py` da cópia e rodei `fechar_v397.py`: (a) item do 4,44 sem a linha dos 5σ → rc 2, «FECHAR RECUSADO … linha com o 4,44 sem a linha dos 5σ»; (b) sem o p calibrado → rc 2; (c) frase do operador parafraseada → rc 2, «NAO e' a verbatim (parafrase)»; em nenhum caso nasceu handoff; restaurado o arquivo, fecha de novo (rc 0, handoff gravado).

## (8) Resíduos BAIXOS

- **B1.** Nos itens «A fala do operador» e «Origem» o 4,44 vem com p e 5σ/creditação, mas sem «gate»/«não cego» (só no item «O número»). A regra do ESTADO (p + 5σ no mesmo item) está cumprida; a versão estrita da ordem da gerência, só no item 1.
- **B2.** «Λ sem β não ecoa [leitura do operador]» no quadro e no artigo é composição das falas de 22/10 e 23/10, sem aspas; sugiro «[leitura composta das falas do operador de 22 e 23/10]».
- **B3.** A regra v315 citada no quadro é a lei do rito do neutrino (ESTADO §4.14), usada aqui como critério de autonomia; se a gerência preferir, nomear a origem.
- **B4.** Herdados: o temporário `v393_cadeia_*\cadeia_sintetica.bin` e o `RuntimeWarning` do código do Codex.

## (8b) Atualização da regra de fidelidade (gerência, 23/10, ~14:47)

O operador RATIFICOU a leitura do fator K («mas é pelo fator K mesmo», `OPERADOR_23out_ratifica_pelo_fator_K_verbatim.txt`, sha16 `782c7e77de7924fd`) e aceitou os adendos («eu aceito todos os seus adendos…», `OPERADOR_23out_aceito_os_adendos_iald_verbatim.txt`, sha16 `c0214c84c28b0746`). Forma admitida nos artefatos: «leitura ratificada pelo operador em 23/10 (sha16 782c7e77…) sobre a fala dele (sha16 f3e24a8c…)», com os limites do verbatim ditos; forma proibida: «o operador disse X» com X fora dos bytes. A varredura (4b) passou a classificar cada citação não encontrada nos bytes em «forma admitida / composição marcada» ou «forma proibida». O candidato intermediário `6459c2dbfdeed0ab` (regerado 14:41, antes da ratificação) já marcava as composições como da gerência; o delta A→B dele (`final\DELTA_A_B.json`) mudou só texto de atribuição (6 nós; kernel, bandeiras, contratos, checks, h8 = 1426, números do quadro e ESPERADOS iguais salvo sha/bytes/ensaio/parágrafo do README) — fica como ensaio da ferramenta; o candidato FINAL, com as 6 falas de 23/10 como inscrições, é o que recebe o veredito.

## (9) O delta `0ac860f4` → `388cc3742323421c` e o veredito final [REAL]

Evidências em `final\`: `DELTA_A_388cc374.json`, `EXAME_PONTOS_388cc3742323421c.json`, `SIMULACAO_ARVORE_NOS_388cc3742323421c.json`, `FIDELIDADE_FATOR_K_388cc3742323421c.json`, `VARREDURA_CITACOES_388cc3742323421c.json`, `VERIFICACAO_QUADRO_388cc374.json`, `TESTE_FECHAR_REGRA_444_388.json`, `RENDER_TEXTOS_388.json`. Snapshots de A: `final\um_v397_candidato_A.py`, `final\ESPERADOS_v397_candidato_A.json`, `sf\`.

**Identidade.** O candidato é `388cc3742323421c`, 38.251.824 B, hash lido por script; é igual ao dos ESPERADOS, do CANDIDATO e do PINOS_BN (14 pinos, todos conferem). O ESTADO é `a7d39ce3666c8d45`.

**Delta por AST: 9 nós mudados, 0 novos, 0 removidos.**
- `main`, `emit_canonical_md`, `build_pt`, `build_en`, `_v397_quadro_tex` e `_v397_quadro_md` mudam só em constantes de texto; esqueleto e números são iguais.
  - Em `main`, só o rótulo de um `print` muda («as quatro falas» → «as falas»). A regex da leitura do pós-rito casa esse rótulo no stdout real executado: 2 registros, 2 selados.
- `_V397_VERBATINS2` ganha duas inscrições: `782c7e77` (26 B) e `c0214c84` (187 B). Em cada uma, o sha256 do texto == o declarado == o do arquivo do operador; o texto é igual aos bytes do arquivo; os trechos são substrings. As quatro antigas estão iguais.
- `_V397_SPECS` e `_V397_VERACIDADE_SPEC`: checagens, fontes e veredito IGUAIS. Mudam só:
  - os textos (limites, diz, nao_diz, estatuto, leituras);
  - a lista das falas usadas (+`782c7e77` no registro de veracidade; +2 no de cunhagens);
  - `extras.cunhagens_embutidas`, de 4 para 6.

**O que não mudou.**
- Kernel embutido, bandeiras, esqueleto, os 5 contratos, `_V397_FONTES`, `_V397_FRASE_444`, `_V397_CHAVES_NUM` e os specs da v396.
- h8 = 1426, com o pino igual.
- Nos ESPERADOS mudam só o sha e os bytes do candidato, o ensaio, as 2 cunhagens novas e o parágrafo do README (os rótulos). Linhas de máquina, átomos e frase do quadro, vereditos dos registros, gate, escada 9499 e h8 são iguais.
- Strings: 45 novas e 27 removidas, sem a palavra proibida e sem literal de β, α ou √e.
- Scripts do pacote: só rótulos de «quatro» para «seis falas» e a lista das 6 falas. O `delta_v397` ganhou um assert de que a ratificação e o aceite são verbatim; o conferidor exige 6 falas com `embedded_ok` e sha == ESPERADOS. `instalar` e `reverter` estão iguais; no `rito` mudou só um comentário.

**Re-execuções sobre o candidato novo.**
- `exame_pontos`: igual ao do `0ac860f4`, salvo as linhas deslocadas (+39), o rótulo do `print` e `verbatim_ok` +782c7e77.
  - O V1 está na l. 246319, igual por AST; a veracidade, na 246324.
  - O registro de veracidade: 35 checagens, `all_verified`, o lido == o resultado original, não move o gate, P18 limpa, os 14 controles negativos mordem.
- `simular`: h8 1426 == o pino.
- O harness do fechar rodou na MINHA cópia do pacote novo (`sf2` → `sb2`): os 5 controles negativos e o positivo passam.
- O item 7 foi refeito: sem os 5σ, sem o p e com a frase parafraseada, o fechar devolve rc 2 e não escreve handoff; restaurado, devolve «FECHADO v397: 388cc3742323421c».

**Fidelidade de citação por bytes.** Corpus: os 27 verbatins mais o Atlas. Superfícies:
- as strings novas do candidato, tiradas pelo AST (os literais partidos voltam a ser uma frase);
- os 24 textos do pós-rito renderizados contra o Nós do sandbox: Atlas, CORE, linhagem, desenho, Haja_Luz, tópicos, aviso, verbete e handoff;
- o handoff do sandbox, o artigo PT/EN (`.txt` e `.tex`) e o `.md`.

Resultados:
- Forma proibida («o operador disse/said X»): **0**.
- Toda citação atribuída ao operador é substring dos bytes, ou é a linha do Atlas, ou é o nome do teste.
- Onde a leitura do fator K é dada como leitura, ela vem na forma admitida: ratificada, com `782c7e77` e `f3e24a8c`.
- 1=1, 1=0 e «ecoa» estão marcados como composição da gerência.
- A C1 e os demais achados da mesma classe estão corrigidos; a B2 também (o rótulo agora é composição).
- O quadro continua com os números == resultado, a regra do 4,44 e a frase verbatim, no PT, no EN, no `.md` e no parágrafo do README do meu sandbox.

**B5 (BAIXA, nova).** Há duas menções curtas da leitura ratificada no spec de veracidade:
- o `estatuto` cita `782c7e77`, mas não `f3e24a8c`;
- um item de `nao_diz` não traz os sha16.

Nenhuma é forma proibida, e o `limites` do mesmo registro traz a forma completa; uniformizar é opcional. Herdados da v396 (estão no Nós instalado): as citações da errata v385/v386 no `.md` e as da Bancada de 30/09 no artigo EN.

**VEREDITO FINAL: PODE_INSTALAR_E_RODAR** (`388cc3742323421c`).
