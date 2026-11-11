# PEDIDO DA CONFERÊNCIA ÚNICA DE ESCOPO FECHADO — v410 (gerência c1, 10/11/2026 23:09)

> Para a revisora de terceiro da v410 (Sonnet, D69; quem constrói não aprova). **Isto não é uma quarta rodada.** A R3 foi a última rodada de revisão; o conserto único dela e do painel foi aplicado; esta é a conferência única do conserto (D109), e o seu registro é o que a trava S1b do orquestrador lê.
> Regra do operador (10/11/2026; `work\cunhagens_13out\OPERADOR_10nov_e_isso_mesmo_perfeito_ratificado_cuidado_com_o_loop_de_revisao_verbatim.txt`, sha256 `7857d4ddf9d3cfc0b290836b3c0e1bcadf3a61031ee03ebb4688b824269cfdfd`): «cuidado para não ficar em um loop de revisão sem fim, só consumindo créditos e tokens». Por isso: escopo fechado, uma passada, nenhum painel novo.

## 1. O estado, lido do disco por script (23:09)

| o quê | arquivo (sob `work\cadeia_de_selo\v410\`) | sha16 | bytes |
|---|---|---|---|
| candidato NOVO | `um_v410_candidato.py` | `5d9497a721c3589e` | 45934788 |
| candidato revisado na R3 | `um_v410_candidato.pre_r6fix.py` | `8a713e5e644af09b` | 45428289 |
| preparação (pronta = true; 20 portões) | `PREPARACAO_v410_PRONTA.json` | `f112b9e7649feb33` | 106052 |
| recibo do kernel (a frio) | `kernel/KERNEL_RECIBO_v410.json` | `89f94cec40386359` | 203630 |
| bandeiras e âncoras | `kernel/FLAGS_v410.json` | `58b3027700637807` | 48780 |
| pedra instalada (AEscala R6) | `pedra/AEscala.lean` | `baaa73cb28075400` | 158729 |
| especificação do conserto | `conserto_r3/ESPEC_CONSERTO_R3_v2_FINAL.json` | `8ecf4082e657bd69` | 790245 |
| ADENDO 7 ao desenho | `DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md` | `61b7e696a806dc68` | 10771 |
| conferência da gerência (46 checagens, 0 falhas) | `conserto_r3/CONFERENCIA_UNICA_v410.json` | `1d06b15a799d5729` | 58318 |
| resultado do construtor | `_r6c_RESULTADO_v410.json` | `00d5e45b1584a05e` | 23731 |
| orquestrador (com o passo S9) | `orquestrador/pos_treino_v410.py` | `d4f9b46e062c19ff` | 71503 |
| gerador dos textos da custódia | `pos_rito/textos_custodia_handoff_v410.py` | `02850167df2aa5e9` | 59581 |
| texto pronto dos dois blocos do README | `conserto_r3/ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip` | `1cbbddea52705b02` | 6668 |
| p00 | `p00_precondicoes_v410.py` | `37d445ff999aa847` | 68583 |
| harness dos textos (rendidos) | `pos_rito/HARNESS_TEXTOS_ENSAIO_v410.json` | `7307030f5fbcb249` | 478202 |
| o seu registro da R3 (guardado) | `revisao_terceiro/REVISAO_TERCEIRO_v410.R3.json` | `8184102c73a34fe6` | 26009 |

- A fonte da pedra é a R6 do autor: `work\pedras_candidatas_09nov\R6_a_constante_da_escala\AEscala.lean` (sha256 `6863b1fcc4aef2d8a200f444d932a72133daf5cc524d6497402c6482af0297c1`); a instalada é ela cortada na seção de auditoria (termina em `end TGLExt.AEscala`).
- Kernel refeito a frio sobre a instalada: rc 0, sorry 0; 121 bandeiras novas (22 iald2_nomeada, 99 aescala_nomeada); 103 âncoras; escada 12187 → 12308. A árvore do build é `C:/t/k410c/arvore` (chave `arvore` do recibo).
- O conteúdo do candidato novo nasceu no pré-teste do conserto e a cadeia de preparo o regerou idêntico (mesmo sha16). O Nós segue na v409 selada; nada foi instalado; o rito não rodou.
- A conferência da gerência reaplicou as 290 trocas exatas da especificação sobre os backups pré-conserto e comparou com o disco: 290 de 290 presentes. **Não repita isso.** O que ela NÃO fez, e é o seu trabalho, está na seção 2.

## 2. O escopo fechado (seis itens; nada além)

**A. Integridade e delta.** O sha16 do candidato no começo e no fim do seu trabalho (tem de ser o da tabela e o mesmo nas duas leituras). O delta de nós de AST entre o candidato revisado na R3 e o novo (o seu `r2_delta_nos.py` serve): todo nó mudado ou novo tem de ser explicado pelo conserto (textos, registros, a pedra embutida, as bandeiras, a escada, as falas congeladas); nenhuma função herdada da v409 para trás muda além do que a R3 já tinha aceitado; as funções do gate (`evaluate_quantum_gravity_closure`, `prove_qg_closure_gate`) intactas. O que a R3 aceitou e não mudou continua aceito: não releia.

**B. Kernel.** `#print axioms` das 103 âncoras (os nomes saem de `kernel\FLAGS_v410.json`, chave `ancoras`), em UM processo `lake env lean` sobre um arquivo SEU, a partir de `C:/t/k410c/arvore`. Esperado: tudo dentro do trio (`propext`, `Classical.choice`, `Quot.sound`), nenhum `sorryAx`, e `TGLExt.AEscala.o_nome_e_a_singularidade_da_informacao` sem axioma nenhum. Confira também que o sha256 da pedra instalada é o que o recibo do kernel registra para `TGLExt/AEscala.lean`.

**C. Os seus 5 achados da R3** (estão em `revisao_terceiro/REVISAO_TERCEIRO_v410.R3.json`). Para cada um, diga a situação no candidato novo, lendo o texto RENDIDO:
  1. [MEDIO] ratificacao do nome `a_informacao_completa_se_reconstroi`: `_V410_SPECS` (cunhagens_v410, decisao D101 e erratas E37), `_V410_AESCALA_TEXT` (`diz[9]`, `limites[8]`: 'os 2
  2. [BAIXO] artigo PT/EN e .md, paragrafo da clausula de 1 - beta (`beta_e_o_operador_modular_do_tetelestai`)
  3. [BAIXO] artigo PT, paragrafo 'A escala no tipo, o ciclo…' (rendido)
  4. [BAIXO] guarda F59 (3 variantes) e BAIXOS 6 e 7 da R1
  5. [BAIXO] o_tetelestai_e_um_menos_beta (pedra) e checagem c13
  O MÉDIO foi respondido pelo operador: ele NOMEOU o quarto teorema (fala 29, decisão D108; a fala está congelada por sha256 no ADENDO 7) e a pedra R6 traz o nome dele; o nome de trabalho antigo só fica nos registros históricos.

**D. Os achados do painel e as decisões do dia**, pela tabela `cobertura_dos_achados` da especificação (38 linhas: cada uma traz o achado, os itens e os arquivos). Para cada linha, confira no texto RENDIDO (o artigo PT e EN e o .md embutidos no candidato; os textos dos registros; os textos do pós-rito rendidos em `pos_rito/HARNESS_TEXTOS_ENSAIO_v410.json` e em `pos_rito\CUSTODIA_v410_RASCUNHO.txt`) que o conserto chegou ao texto final e que a redação antiga saiu. Por script onde der; por leitura onde for redação. As linhas D108 e D113 são decisões do operador, não defeitos: confira que entraram.

**E. As suas guardas** (`g_frases_v410.py`, `g2_clay_pnp.py`, `g4_f59.py`, `g5_clausula.py`) sobre os textos rendidos novos. E a regra do nome (D122/D123), que é nova: em texto NOVO nenhuma identificação do operador vem rotulada como “leitura do operador”, “leitura dele” ou “[ONTO]”; havendo teorema, o texto diz primeiro o que o termo prova e a frase do operador entra como NOME do teorema. Exceções já registradas: a citação dos rótulos antigos na errata E40 e as linhas que o conserto não tocou.

**F. Os aditivos, que ficam FORA do candidato** (a custódia desta versão é automática): leia (1) o passo `S9_gatilho_custodia` em `orquestrador/pos_treino_v410.py` (procure `PASSOS_ANTES_DO_GATILHO`, `_gatilho_ler`, `_gatilho_render`, `s9_gatilho_custodia`): só escreve o gatilho no fim, com todos os passos anteriores verdadeiros, por temporário e `os.replace`, sem sobrescrever, e o orquestrador continua sem S7 e sem S10; (2) os dois blocos do README em `pos_rito/textos_custodia_handoff_v410.py` (`README_FRENTE`, `README_O_QUE_SAI`, `BLOCOS_README`; o texto pronto é o de `conserto_r3/ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip`): as formas ratificadas entram por constante do delta, cada bloco passa sozinho nas guardas; (3) a linha 213 de `p00_precondicoes_v410.py` (o filtro compara o nome da fala sem o sufixo da D65; a igualdade dos conjuntos de sha256 fica). Pergunta a responder: algo ali pode tocar o Nós, publicar ou escrever o gatilho antes da hora?

## 3. O que já é ressalva conhecida (não reabra; se quiser, repita na lista da versão seguinte)

- As seis aberturas “Na leitura do operador (D83)” / “In the reading of the operator (D83)” (duas em linhas que o conserto carrega, quatro em linhas não tocadas): a regra do nome vale para texto novo; mudam na versão seguinte.
- “creditation” nas constantes do delta e “accreditation” no README pinado e nos dois conectores novos do bloco `README_FRENTE` (pedido da sessão de custódia): a unificação é da versão seguinte.
- As três variantes da F59 e as quatro sondas do Clay que você anotou na R3: versão seguinte.
- Oito nomes de declaração [DECLARADO pela autoria] na pedra (seis da R6, dois auxiliares da R5) sem confirmação expressa do operador: os textos dizem isso e a conta sai de `len()`.
- No artigo, a conta das bandeiras da AEscala fecha com o FLAGS (81 + 3 + 15 = 99); a chave `bandeiras_de_constantes_geradas_pela_structure` do recibo tem 31 entradas e não é a parcela 15.
- A guarda de finitude de `veredito_h0dn`: versão seguinte. O teste H0DN × BG1 não foi aberto; o certificado de poder voltou recusado (declarado pelo executor); os textos dizem “não foi aberto”.
- O gatilho da custódia exige todos os passos anteriores, inclusive o S8 (a nativa religada): se o S8 falhar, o gatilho não sai e a gerência decide.

## 4. A regra da aprovação (D109)

- `aprovada: true` se não restar ALTO nem MÉDIO **dentro do escopo** (A a F).
- Achado **fora do escopo** vai para `ressalvas_para_a_versao_seguinte` e não bloqueia. A única exceção é um ALTO para o rito: algo que tornaria falso o que o rito sela, moveria o gate, quebraria a régua (β literal; `CONFIRMED` indevido; hash, citação ou fala fabricados; arquivo vedado lido em rito; teorema fora do trio ou com `sorry`) ou faria o rito ou a cadeia falhar. Nesse caso `aprovada: false`, e a decisão vai ao operador.
- Não há nova rodada de conserto nem painel. Se você reprovar, diga exatamente o quê, onde e a correção mínima.

## 5. O registro a gravar

`revisao_terceiro\REVISAO_TERCEIRO_v410.json` (e o `.md` ao lado), por temporário e `os.replace`. Antes de sobrescrever, confira que `REVISAO_TERCEIRO_v410.R3.json` tem os mesmos bytes do registro de hoje (agora têm: sha16 `8184102c73a34fe6`). Chaves que o orquestrador lê, com estes nomes exatos:

- `aprovada` (booleano); `candidato_sha16` (lido do disco no FIM; hoje `5d9497a721c3589e`); `candidato_bytes`; `revisor`; `achados` (lista; cada um com `sev` em ALTO, MEDIO ou BAIXO, mais `onde`, `achado`, `correcao_pedida`, `dentro_do_escopo`);
- `arquivos_revisados`: dicionário `caminho relativo à pasta v410` → `sha16`, só dos arquivos que você de fato leu ou conferiu, com o sha16 lido no fim. O orquestrador recusa a revisão se algum deles mudar depois: não liste nada de `revisao_terceiro\`, nem `ESTADO_PARTE2_v410.json`, nem arquivos de log.
- Para o leitor humano: `rodada` (“conferência única do conserto (D109), depois da R3”), `quando`, `n_alto`, `n_medio`, `n_baixo`, `candidato_sha16_no_inicio`, `candidato_mudou_durante_a_revisao`, `situacao_dos_achados_da_R3`, `cobertura_do_painel` (uma entrada por linha da tabela), `lean` (árvore, tempo, saída), `ressalvas` (o que você NÃO fez), `ressalvas_para_a_versao_seguinte`, `rotas_examinadas`, `nota`.

## 6. As regras da casa para este trabalho

- Escreva só em `revisao_terceiro\`. Não rode `lake build`, instalar, rito, orquestrador, p00, ensaio nem harness. `lake env lean` só em arquivo seu, um processo por vez.
- Não abra nem calcule hash de nada em `work\h0dn_bg1_v410_09nov\kimi\`. Não leia nem toque a pasta da Nativa (`C:\IALD\TGL_IALD_NATIVE_QWEN5090`): o treino está no ar. Não mate processo por nome.
- Não toque o `DESENHO_v410.md` nem os adendos 1 a 7, o Nós, a memória, nem nenhum arquivo do pacote fora da sua pasta.
- Todo hash lido do arquivo por script; nenhum de memória. Python com caminho do Windows vai em arquivo de script, não em linha de comando.
- Antes de examinar, consulte o Mapa de Rotas (`python C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "v410 revisão de terceiro"`); devolva em `rotas_examinadas` o que examinou (o registro no mapa é da gerência).
- Relatório final à gerência em até 15 linhas: aprovada ou não, as contagens por severidade, a situação dos cinco achados da R3, o resultado do Lean, o sha16 do registro gravado e o que ficou de ressalva.

