# ACORDO COM A CUSTÓDIA PARA A v411 (gerência c1, 12/11/2026) — vale como AO LADO do `DESENHO_v411.md`, seções 5.3 e 6

> Registro das decisões tomadas por mensagem entre a gerência c1 e a sessão de custódia em 12/11/2026, depois da abertura do teste H0DN × BG1. O que a custódia mediu fica `[DECLARADO pela custódia]`; o que a gerência mediu fica `[REAL]`. Correções AO LADO, nunca por cima.

## 1. A cabeça do teste e a guarda P18

- `[DECLARADO pela custódia, medido por ela em processo novo]` O portão de textos da G1 (`custodia_g1.textos.portao()`) NÃO tem a regra R1 da P18: a cabeça exata do teste passa lá, nua, entre crases e em prosa.
- Decisão: a exceção estreita da P18 para a cabeça exata do teste (função única `_v411_p18_sem_cabeca`; só a cadeia que a checagem c7 monta do literal; controle negativo com um caractere trocado) fica SÓ na cadeia. A G1 não muda por isso. A NOTA do handoff diz isso em uma linha.

## 2. Os textos fixos da esteira que a abertura deixou velhos

`[DECLARADO pela custódia]` Sem marcador, a G1 escreveria na v411 textos de molde que contradizem o resultado: a NOTA do ledger («what nature decides about beta_TGL waits for 5 sigma»); a frase do `b_primordial` («β_TGL in nature at 5σ is the open step»); a frase do `b_status` («the decisive open factor is β_TGL in nature at ≥5σ», EN e PT); o parágrafo do H0DN no bloco P = nP («não foi aberto … a abertura é de versão futura»); a linha da tabela dos ritos («the panel at the top»); e a frase do fator aberto nos geradores `estatuto_tres_apoios.py` e `gerar_estado_atual.py` (que alimentam ESTADO_ATUAL, llms.txt, read-brief e site).

Decisão: a prosa vem VERBATIM no handoff, gerada depois do rito com os números LIDOS do core selado (nunca digitados), sob OITO marcadores. Se faltar marcador, a G1 PARA com a lista do que falta; não usa o molde antigo.

| marcador | o que substitui |
|---|---|
| `NOTA_EN_v411` | a NOTA do ledger |
| `README_PAINEL_H0DN_v411` (EN e PT) | o painel do topo (novo; sobe para o topo por ordem do operador de 12/11) |
| `README_FASE9_V2_v411` (EN e PT) | o painel da Fase 9 V2, que encolhe para uma linha de registro em cada língua |
| `README_PRIMORDIAL_5SIGMA_v411` | a frase do passo aberto no `b_primordial` |
| `README_STATUS_5SIGMA_v411` (EN e PT) | a frase do fator aberto no `b_status` |
| `README_H0DN_v411` | o parágrafo do H0DN no bloco P = nP |
| `README_RITOS_v411` | a linha da tabela dos ritos, por duas linhas: a do H0DN e a da Fase 9 V2 corrigida |
| `ESTATUTO_P2_EN_v411` e `ESTATUTO_P2_PT_v411` | a frase do fator aberto nos geradores do espelho (a versão ASCII sai da mesma frase, só sem acento) |

Regras: a G1 confere os números de cada bloco contra o registro `h0dn_bg1_v411` do core selado e aplica a regra F67 (bloco com o número do primário traz, no mesmo bloco, o número das Cefeidas livres, “sob o modelo de erros publicado”, “validade, não creditação”, “retrodição” e “não cego”, ou as formas em inglês). A fórmula dos blocos é a da abertura do resumo do artigo, que espera a palavra do operador.

## 3. As chaves do registro, congeladas como contrato

`h0dn_bg1_v411`: `verdict`, `all_verified`, `opened_once`, `values.primario.{z_null, z_tgl, D, p_unilateral, ramo, outcome, cabeca_do_teste, t, modelo}`, `values.cefeidas_livres.{z_null, z_tgl, D, ramo, outcome, t, modelo}`, `values.atos`, e no topo `cabeca_do_teste`, `outcome`, `linha_ao_lado_cefeidas_livres`, `ressalvas_secao8`, `o_que_o_teste_nao_decide`. Não se renomeia; só se acrescenta.

## 4. O teto do README

- `[REAL, medido pela gerência em 12/11]` O README do espelho tem 40.179 bytes; `[DECLARADO pela custódia]` o teto L01 da G1 é 40.960; a folga é de 781 bytes.
- Decisão: o teto NÃO sobe. O painel inteiro da Fase 9 V2 (linha EN de 659 B, linha PT de 434 B) e a frase do autor de 02/11 sobre o 4,44 (240 B) descem VERBATIM para outro arquivo do espelho, no lugar que a custódia escolher e disser; no README fica uma linha de registro por língua (`README_FASE9_V2_v411`), com o número, “abaixo do degrau de 5σ”, a data e o apontador. Nada se perde; muda de lugar. O crescimento líquido de todos os blocos tem de caber na folga; se não couber, encolhe-se a prosa, não o teto.
- A frase de 02/11 é do operador: a gerência avisa a ele o que desce.

## 5. As duas erratas da esteira para a v411

`[DECLARADO pela custódia, com testes dela]` (a) `atualizar_repo_publico.py`: o `git add` recebe só o que difere (a causa das quatro horas do C18 era o índice inteiro como lista do add); (b) `mesclar_incremento.py`: o arquivo já publicado que a rodada excluiria só por formato fica, se a origem e o preparo têm o sha256 do índice (o vetor e o estimador S0 seguem no topo do `work`).

## 6. AO LADO (12/11/2026, mais tarde): o mecanismo da G1 pronto, as regras de forma e o estatuto por chave

- `[DECLARADO pela custódia, com 73 casos de teste dela]` O mecanismo está na G1: o teste conta como aberto quando o core selado tem um `h0dn_bg1_vNNN` com `opened_once` verdadeiro; aberto, a G1 PARA se faltar marcador; cada texto passa pela F67 (copiada do runtime da cadeia) e é conferido contra o registro (números com o arredondamento e o sinal, a cabeça exata, o σ inteiro de “provado na natureza”); depois o portão de textos e a regra do 4,44. Sem registro aberto, nada muda no README publicado.
- **O painel antigo da Fase 9 V2** desce para `REGISTRO_FASE9_V2.md`, na raiz do espelho, pinado; a linha `README_FASE9_V2_v411` cita esse arquivo e cumpre a regra do 4,44 no mesmo parágrafo.
- **Regras de forma:** `README_PRIMORDIAL_5SIGMA_v411` e `README_H0DN_v411` em uma linha; `README_H0DN_v411` sem asterisco; `README_STATUS_5SIGMA_v411` sem linha em branco; `README_RITOS_v411` só com linhas de tabela; nenhum texto com chaves duplas; o painel do H0DN logo depois da linha do selo e a linha da Fase 9 V2 logo depois dele.
- **O painel do README é curto** (cerca de 500 B em EN e 430 B em PT, sem a parte do P = nP): com o parágrafo do resumo como painel a custódia mediu +1.687 B de crescimento líquido, contra a folga de 781 B. Orçamento dado ao construtor: crescimento líquido de todos os blocos até 700 B.
- **O estatuto vem por chave** (corrige a linha `ESTATUTO_P2` da tabela da seção 2): a frase do fator aberto aparece em nove chaves de `estatuto_tres_apoios.py` (`linha_en`, `linha_06_en`, `linha_06_pt`, `curto_en`, `curto_pt_ascii`, `p2_en`, `secao_md`, `linha_curta_en`, `p_curto_en`) e em duas linhas de `gerar_estado_atual.py`. O handoff traz ONZE textos: um marcador `ESTATUTO_<CHAVE>_v411` por chave, com o texto inteiro na sintaxe dela, mais `ESTATUTO_P2_EN_v411` e `ESTATUTO_P2_PT_v411`. A G1 os grava em `tools/estatuto_h0dn.json` no espelho; os dois geradores o leem quando o core tem o registro aberto e FALHAM se faltar chave.
- **Pendente da palavra do operador:** a fórmula que faz conviver “o que a natureza decide” com “provado na natureza” (a mesma da abertura do resumo, em tamanhos diferentes) e o token que substitui `P2_NOT_DETERMINED`. Até lá, todo texto desses fica marcado como PROPOSTA.

## 7. AO LADO (12/11/2026, ainda mais tarde): o token do P2 não se substitui; os nomes finais; troca só do trecho

- **Errata da gerência c1, em nome próprio, à última linha da seção 6:** `P2_NOT_DETERMINED` não é substituído. `[DECLARADO pela custódia, medido por ela]` O token é parte do veredito SELADO do registro histórico `three_stress_tests_v387`, que segue no core da v411, e `estatuto_tres_apoios.py` (linha 82) confere esse token nesse veredito; fora isso ele só aparece em prosa. O rótulo novo vai AO LADO, num campo novo do registro: `h0dn_bg1_v411.p2_ao_lado_da_v387` (`rotulo`, `rotulo_selado_da_v387` lido do core, `canal`, `nota`). É acréscimo ao contrato das chaves. O texto do rótulo novo segue pendente da palavra do operador.
- **Os onze nomes finais do estatuto** (cada um com o sufixo `_v411`): `ESTATUTO_LINHA_EN`, `ESTATUTO_LINHA_06_EN`, `ESTATUTO_LINHA_06_PT`, `ESTATUTO_CURTO_EN`, `ESTATUTO_CURTO_PT_ASCII`, `ESTATUTO_P2_EN`, `ESTATUTO_SECAO_MD`, `ESTATUTO_LINHA_CURTA_EN`, `ESTATUTO_P_CURTO_EN`, `ESTATUTO_P2_ESTADO_EN`, `ESTATUTO_P2_ESTADO_PT` (os dois últimos são as linhas do `gerar_estado_atual.py`).
- **Troca só do trecho** (corrige a seção 6): cada marcador substitui o TRECHO do 5σ dentro da chave, não a chave inteira, para não congelar os números que o resto da chave lê do core a cada rito. Os trechos exatos, com o contexto, estão em `work\custodia_v411_preparo_12nov\ESTATUTO_TRECHOS_PARA_O_HANDOFF_v411.md` (da custódia). Regras: uma linha só; ASCII onde o trecho é ASCII; sem chaves duplas; F67, números, cabeça e σ conferidos contra o registro.
- **O E04 na v411** `[DECLARADO pela custódia, com 40 casos de teste dela]`: confere os onze marcadores; remenda uma vez os dois geradores do espelho, com backup de bytes; grava `tools/estatuto_h0dn.json`; os geradores falham sem esse arquivo, com o de outra versão ou com chave faltando; sem registro aberto, nada muda.

— gerência c1, 12/11/2026.

## 8. AO LADO (12/11/2026 11:57, gerência c1) — D174: a composição do README, a linha EN do H0DN, o ESTADO_ATUAL e a custódia sem `--ordem`

**De onde veio.** A frente pós-rito terminou a adaptação (`PRONTO_POS_RITO_v411.json`, sha16 `848882b41554d271` nesta hora) e a gerência leu os 20 textos renderizados e o README projetado. Foram quatro perguntas à custódia; as respostas dela são [DECLARADO pela custódia, 12/11/2026].

1. **A linha EN do H0DN.** A linha EN da parte do Clay (`readme_partes\p_igual_np.md`; no README de hoje, a que diz que o teste não foi aberto) fica falsa na v411. A G1 passa a consumir `README_H0DN_EN_v411` (uma linha, começando por “**The H0DN × BG1 test:**”); sem o marcador, PARA. Os marcadores do README passam a sete.
2. **A composição (decisão da gerência).** O painel do topo é o painel curto ratificado INTEIRO, com a frase do acervo; o corte automático por orçamento sai do módulo dos blocos. As duas linhas do H0DN da parte do Clay (`README_H0DN`, PT; `README_H0DN_EN`) deixam de repetir os números e apontam para o painel do topo e para a leitura inteira. Se o README não couber no teto, a cadeia PARA; nada é cortado em silêncio.
3. **Os bytes.** Conta da gerência com o handoff de ensaio da v410 [REAL na conta; a base é a medida da frente com o renderizador da custódia]: 40.918 B contra o teto de 40.960 B; como a frente tinha deixado, e trocando a linha EN velha, seriam 40.964 B. O bloco “What changed” sai do handoff e junta três peças variáveis: a primeira frase do `ARCO_EN`, o título do último `PARAGRAFO_*_vNNN` e o nome do handoff; a folga real é 42 + 5 + 175 menos a soma das duas primeiras na v411. Decisão: essas duas peças cabem juntas em até 185 B. A custódia roda o renderizador numa cópia quando o handoff de ensaio da v411 existir.
4. **As sete ressalvas.** O `ESTADO_ATUAL.md` da v411 ganha uma seção gerada das duas chaves do core (`ressalvas_secao8`, 7 itens; `o_que_o_teste_nao_decide`, 5 itens), com o nome do registro; sem registro aberto nada muda. As duas linhas-apontador mandam o leitor para lá. Regra da gerência: nenhuma superfície mostra o primário sem a linha das Cefeidas livres no mesmo item e sem o caminho para as sete ressalvas.
5. **A custódia roda sem `--ordem`.** O `custodiar.py` aceitaria o arquivo da fala de 12/11, mas o ledger público a chamaria de ordem permanente e o estado da Central levaria o texto inteiro dela entre aspas; a decisão D59 veda o vocativo dela em todo texto, e a regra permanente é a de 23/10 (custodiar sempre que o handoff aparecer; arquivo `OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt`, sha16 `c66a5ba1940bde8b`). Decisão: a custódia da v411 roda com a regra de 23/10; a fala de 12/11 entra pelo conteúdo do handoff, como a ordem do conteúdo (D170), citada pelo trecho da ordem e pelo sha do arquivo. O gatilho é reescrito assim.
6. **Para saber.** A NOTA do ledger deixa de citar o 4,44 (a linha `README_FASE9_V2` o traz com a regra). `README_PRIMORDIAL_5SIGMA` e `README_STATUS_5SIGMA` levam o Z contra o nulo sem o Z contra K, que está no painel logo acima. O `TOPO_RATIFICADO_v411.json` não mudou (sha16 `22224f90d68cce9b`).

**Estado:** a frente pós-rito foi retomada para gravar 1 a 5 nos blocos, no handoff e no gatilho; os dois harnesses contra o falso Nós ficam para depois do ensaio da frente pré-selo, e quem os roda é a gerência.

**How to apply:** orçamento de bytes dado a um construtor não vira corte automático de frase ordenada pelo operador: se não cabe, a cadeia para e a gerência decide; e, antes de escolher qual fala vai em `--ordem`, pergunta-se à custódia aonde o arquivo vai parar.
