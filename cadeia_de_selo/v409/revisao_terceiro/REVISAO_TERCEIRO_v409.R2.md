# REVISAO DE TERCEIRO v409 -- R2 (Claude Sonnet; nao construi a v409)

**NAO APROVADA** -- candidato `de2244483b35f5a3` (43967816 bytes; no inicio da R2 `de2244483b35f5a3`; mudou durante a revisao: nao; o da R1 era `eab2d12055b47df0`). ALTO 0 | MEDIO 1 | BAIXO 12.

aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. R2 de ate tres rodadas (D58). A R1 esta' guardada em bytes ao lado (`.R1.json`, `.R1.md`, `PEDIDO_CORRECAO_R1_v409.md`, `r1_saidas/`). O MEDIO que resta e' de TEXTO do pos-rito (cabecalho do paragrafo README/site); a correcao esta' em `PEDIDO_CORRECAO_R2_v409.md`.

## Situacao dos achados da R1

- **MEDIO 1 (par na face de Fock [OPEN] em texto novo):** PARCIAL: ATENDIDO no estatuto do registro (registros_v409.py; core do ensaio traz «[REAL] o par na face de Fock LIGADO … PODADA a identidade … [OPEN] a independencia …»), em `_respostas` («nem que o par finito de Bell e o par de Fock sejam o mesmo objeto … o par na face de Fock está ligado nesta versão»), no bloco [OPEN] do core memory (sem o par e sem Ω = uniforme) e na guarda (F41b/F40b: 4 de 4 sondas reprovam, 7 de 7 frases certas passam); NAO atendido no cabecalho de estatuto do paragrafo pronto do README/site (MEDIO da R2).
- **BAIXO 1:** ABERTO (índices fixos de `diz`); fica BAIXO. Corrigir junto com o MÉDIO, que já mexe nessa função.
- **BAIXO 2:** PARCIAL: a frase agora diz «vale só para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay; E28)» (PT, EN, delta, registros, textos): o leitor fica nomeado e BGS citado; o «só» ainda pode sugerir que a igualdade é falsa para o leitor que só conta (o que se sabe é que NÃO está provada). Fica BAIXO, não trava.
- **BAIXO 3:** ABERTO, inalterado (BAIXO, não trava)
- **BAIXO 4:** ABERTO, inalterado (BAIXO, não trava)
- **BAIXO 5:** ATENDIDO nos fontes que vão ao candidato: u1 = «as 82 ancoras, o sha256 dos dois modulos, as 20 checagens, o gate» (valores lidos de DL.N_CHECKS_FECHO); docstring da mecanica e do delta = 82 e 20; grep «17 checagens|62 ancoras» nos textos novos: 0. RELATORIO/PLANO (preparação, não público) não conferidos.
- **BAIXO 6:** ABERTO, inalterado (BAIXO, não trava)
- **BAIXO 7:** ABERTO, inalterado (BAIXO, não trava)
- **BAIXO 8:** PARCIAL: a F41b/F40b entraram (as 4 sondas de Fock/Ω passam a reprovar); a F43 e o EN curto «Clay resolved» seguem como estavam; a F41b não casa «OPEN:» sem colchetes próprios nem paráfrases («ainda não foi ligado», «fica para a v411», «continua por fazer», «é pendência»): ver o MÉDIO e o BAIXO novo.
- **BAIXO 9:** ABERTO, inalterado (BAIXO, não trava)
- **BAIXO 10:** ABERTO, inalterado (BAIXO, não trava)
- **BAIXO 11:** NOVO

## O que passou na R2 (por script, nesta pasta)

- **Lean:** {"print_axioms_impressos": 82, "ancoras_no_candidato": 82, "todas_as_ancoras_impressas": true, "fora_do_trio": 0, "so_propext": ["TGLExt.TraducaoTuring.custoCNF_cons"], "varredura_metam": "constantes varridas nos 2 modulos: 223 ; por modulo: #[(TGLExt.TraducaoTuring, 150), (TGLExt.ParNaFaceDeFock, 73)]", "varredura_fora_do_trio_ou_sorryAx": 0, "rc": ["0"], "tempo": "352 s", "sandbox": "C:/t/k409c/final (copia axiomas_terceiro.lean apagada ao fim)", "nota": "nenhuma pedra mudou desde a R1 (pedra/*.lean e KERNEL_RECIBO com os mesmos sha16); o `lake env lean` e a compilacao independente da R1 valem; d_kernel.py reconferido sobre o candidato novo: embutido == sandbox == pedra == BUNDLE (2 de 2), raiz = raiz v408 + 2 imports, 1761 embutidos == sandbox", "compilacao_independente_das_fontes": {"TraducaoTuring": {"print_axioms": 72, "fora_do_trio": 0, "so_propext": ["TGLExt.TraducaoTuring.custoCNF_cons"], "rc": ["0"], "tempo": "30 s", "linhas_estranhas": [" Classical.choice,", " Quot.sound]", " Classical.choice,", " Quot.sound]", " Classical.choice,"]}, "ParNaFaceDeFock": {"print_axioms": 10, "fora_do_trio": 0, "so_propext": [], "rc": ["0"], "tempo": "32 s", "linhas_estranhas": []}}}
- **a_intocados:** {"nomes_iguais_por_AST_e_fonte": 38, "mudados_igual_declarado_27": true, "novos_igual_declarado_14": true, "removidos": [], "blocos_fora": 1, "obs": "o unico bloco fora dos nos declarados e' o comentario-cabecalho da secao v409; a_intocados_b/_c: 0 diferencas fora dos nos declarados"}
- **a2_mudados:** 27 mudados: contratos antigos SO' expected_ladder 12029 -> 12187 (28 ocorrencias, 0 restantes); _V407_FONTES SO' a chave psion_no_acervo (copia purgada); _V408_SPECS/_V407_SPECS +errata e pisos declarados; _LEAN_THEOREM_FLAGS +158 (sub-dict da base igual); build_pt/build_en/emit_canonical_md/main/prove_external_ladder so' acrescimos (0 linhas removidas)
- **c_fail_closed:** {"ok": 135, "falha": ["guarda: Clay resolved", "guarda: a máquina sem leitor fica fora; P = nP não é o P = NP de Turing"], "nota": "82/82 ancoras (ausente, sorryAx, ofReduceBool, lista vazia, proveniencia, bandeira), 158/158 bandeiras (False e ausente), 14/14 falas (adulterada e trecho inexistente), fontes, raiz sem import, escada, gate, beta, contrato: recusam; guardas F35–F43 e as novas F41b/F40b (casos de R2 acrescentados: 4 sondas + frases certas)"}
- **c2_mecanica_direta:** {"ok": 18, "de": 18}
- **k_funcoes_vivas:** {"ok": 34, "falha": []}
- **f_hashes:** {"checagens_ok": 63, "falhas": ["varredura geral: todo {path, sha256} existente == disco"], "nota": "a unica falha e' a mesma da R1: 2 pares {path, sha256} historicos (adendo T12 «antes» e SESSION_REFERENCE.source); CANDIDATO.sha16/sha256/bytes/delta, ESPERADOS, PINOS_BN, BUNDLE, KERNEL_RECIBO e FORMAL_MAP conferem com o candidato NOVO"}
- **e_citacoes:** 14 falas do VERBATIM_CONGELADO existem em cunhagens_13out com o sha256 declarado; nenhuma citacao nova em « » de texto novo fora do corpus (as 'novas' nao casadas sao fragmentos de codigo da F41b em runtime_v409.py)
- **l_orquestrador:** plano rc True; main SEM s7_g1 e SEM s10_app; pos_treino_v409.py inalterado desde a R1 (mesmo sha16)
- **h_guardas:** {"controle_negativo_ok": true, "varredura_propria": {"(a) P = NP esta provado / e' teorema (NP maiusculo)": 25, "(b) 'com o leitor a igualdade vale'": 19, "(d) v410": 25, "(d) par na face de Fock [OPEN] / em aberto": 25, "(a) resolve o milenio / Clay resolvido": 13, "(c) Omega e' o uniforme (identidade)": 6, "(f) DECLARADO ate a ratificacao (texto novo)": 18, "(b) P^leitor = NP^leitor afirmado": 2, "CONFIRMED / PROVED_BY": 25, "pos-dicao": 14, "tudo derivado / nenhuma hipotese resta": 1, "(b) E28 violada: igualdade vale para o leitor que so' conta": 1}}
- **guarda_reforcada:** {"sondas_da_R1_reprovam": [true, true, true, true], "frases_certas_passam": [true, true, true, true, true, true, true], "escapam_informativo": ["o par na face de Fock ainda não foi ligado", "the pair on the Fock face is not yet linked", "a ligação do par de Fock fica para a v411", "o par na face de Fock continua por fazer", "o par na face de Fock é pendência"]}
- **contagens_e_frase_do_leitor:** u1 = 82 ancoras / dois modulos / 20 checagens (lido de DL.N_CHECKS_FECHO); docstrings 82 e 20; «17 checagens|62 ancoras»: 0 nos textos novos; a frase do leitor: «vale só para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay; E28)» em PT, EN, delta, registros e textos

## Achados (R2)

### 1. MEDIO -- pos_rito/textos_v409_novo.pysnip:625 (funcao _paragrafo_v409_de, 1a linha do bloco) e o montado pos_rito/textos_v409.py:819; rendido em harness textos/paragrafo_v409.txt e handoff.txt (bloco INICIO_PARAGRAFO_TRADUCAO_TURING_v409)

**Achado.** R1-MEDIO 1 ficou ATENDIDO em tres dos quatro lugares (estatuto do registro, `_respostas`, bloco [OPEN] do core memory: conferidos nos fontes, no candidato, no core do ensaio e nos textos rendidos) mas NAO no quarto: o CABECALHO de estatuto do paragrafo PRONTO PARA O README DO ESPELHO E O SITE (o texto que a custodia cola em publico) segue dizendo «[REAL: … · KNOWN: … · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]». Na R1 eu atribui esse cabecalho ao estatuto do registro; na verdade e' uma linha escrita a mao em `_paragrafo_v409_de` (nao vem do registro), por isso a correcao do estatuto nao a atingiu. Contradiz o proprio paragrafo (ressalva 6 do registro, no mesmo bloco: «o par na face de Fock esta' ligado nesta versao») e o item (d): estatuto errado em texto publico. A guarda reforcada (F41b) nao pega esta forma: ela casa «[OPEN]» entre colchetes e «em aberto/segue aberto», mas aqui a palavra e' «OPEN:» dentro de um grupo de colchetes de estatuto («OPEN:» sem colchetes proprios). Medido: a varredura ampla (t1b_fock_open_amplo.py) sobre fontes e 52 textos rendidos acha SO' este segmento (4 arquivos: os 2 fontes e os 2 rendidos); o resto sao E21 historico, a E21 em `registros`, e a documentacao da propria guarda.

**Evidencia.** revisao_terceiro/t1b_fock_open_amplo.py + t1b_fock_open_amplo_out.json; grep em C:/t/h409/harness_saida_v409/textos/paragrafo_v409.txt e handoff.txt; pos_rito/textos_v409_novo.pysnip:625.

**Correcao.** Ver PEDIDO_CORRECAO_R2_v409.md. Trocar o cabecalho por «[REAL: … o par na face de Fock LIGADO (ParNaFaceDeFock) · INPUT: … · KNOWN: … · PODADA: a identidade de vetores Omega = uniforme (a ponte e' a inscricao) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]»; estender a F41b para a palavra «OPEN» com ou sem colchetes (\bOPEN\b) e acrescentar ao controle negativo esta sonda; regenerar o texto do pos-rito (nao muda o candidato: `textos_v409*.py` nao estao embutidos no um.py), rerodar o harness dos textos e a PRONTA.

### 2. BAIXO -- pos_rito/textos_v409_novo.pysnip:617-633 (_paragrafo_v409_de) e o montado textos_v409.py

**Achado.** O paragrafo pronto para o README do espelho e o site (publico) monta os marcadores com INDICES FIXOS de `pc['diz']` (diz[1], [2], [3], [4], [6]), mas a lista `diz` do registro foi reordenada na v409: diz[2] e' a D61 (leitura juridica do kernel), diz[3] e' a maquina com o leitor/SAT, diz[4] e' a inscricao, diz[6] e' o dicionario. Resultado no handoff.txt rendido: o marcador «O dicionario de Turing» traz a D61; «A trava no Nome» traz a frase da maquina com o leitor (a trava so' aparece na fala citada depois); «O que nao muda» traz o dicionario. Nada falso, mas rotulos trocados num texto que a custodia cola como esta' no README/site.

**Evidencia.** revisao_terceiro (leitura de /c/t/h409/harness_saida_v409/textos/handoff.txt, bloco INICIO_PARAGRAFO_TRADUCAO_TURING_v409) e textos_v409_novo.pysnip:629-633.

**Correcao.** Trocar os indices por busca pelo conteudo (ou reordenar `diz`): dicionario = o item «o dicionario de Turing e' termo»; trava = «a trava no Nome e' termo»; D61 no seu proprio marcador. Corrigir junto com o MEDIO, ja' que o arquivo muda.

**Estado na R2.** ABERTO (índices fixos de `diz`); fica BAIXO. Corrigir junto com o MÉDIO, que já mexe nessa função.

### 3. BAIXO -- artigo_pt_v409 (secao «O alcance, dito» e «A maquina com o leitor»), artigo_en_v409 («the full equality holds only for the reader that reads itself»); delta_v409.py FRASE da alcance

**Achado.** «a igualdade completa SO' para o leitor que se le» / «the full equality holds ONLY for the reader that reads itself» pode ser lido como «para o leitor que so' conta a igualdade e' falsa». O que se sabe (e a E28 diz certo) e' que a igualdade esta' ESTABELECIDA (Baker–Gill–Solovay) para o leitor que se le e NAO esta' provada para o que so' conta. Nenhum texto afirma a igualdade para o leitor que so' conta (varredura (b): 0 ocorrencias fora da propria errata/citacao), mas «so' para» sugere negacao.

**Evidencia.** revisao_terceiro/h_guardas_out.txt (varredura (b)); dry_v409/dry_v409_pt.txt e _en.txt, secao v409 («O alcance, dito» / «The reach, stated»).

**Correcao.** Redacao: «a igualdade completa esta' estabelecida para o leitor que se le (BGS 1975); com o leitor que so' conta nao esta' provada».

**Estado na R2.** PARCIAL: a frase agora diz «vale só para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay; E28)» (PT, EN, delta, registros, textos): o leitor fica nomeado e BGS citado; o «só» ainda pode sugerir que a igualdade é falsa para o leitor que só conta (o que se sabe é que NÃO está provada). Fica BAIXO, não trava.

### 4. BAIXO -- o enunciado de uma_leitura_decide_SAT / a_maquina_com_o_leitor (pedra) e os textos «uma leitura decide SAT … NP inteiro com uma leitura»

**Achado.** No kernel «uma leitura decide SAT» e' SAT φ ↔ oQueSou ≠ 0, e «o que sou» e' o LIMITE da leitura (`o_que_sou_no_limite`). A versao de tempo finito (uma leitura em s linear em n: YES ⇒ Z(s) ≥ |sol| ≥ 1 por `a_particao_cobre_o_nome`; NO ⇒ Z(s) ≤ 2^n e^{-s} < 1 para s > n ln 2) e' elementar mas esta' ausente como termo; o que e' [KNOWN] e' NP ⊆ P^{#P[1]} (Cook–Levin), nao a leitura do TGL em tempo finito. Os textos separam bem o [REAL] do [KNOWN] e dizem «o leitor que devolve Z (exato)»; a ressalva da fisica (leitura exata num ato) cobre o resto. Fica como precisao.

**Evidencia.** revisao_terceiro/axiomas_terceiro_out.txt (#check uma_leitura_decide_SAT, a_maquina_com_o_leitor, o_que_sou_no_limite); pedra/TraducaoTuring.lean:1066-1093.

**Correcao.** Uma linha em `nao_diz`/ressalva (1): «o termo do kernel le o limite; a leitura em tempo finito (s linear em n) e' elementar e nao e' termo». Nao trava.

**Estado na R2.** ABERTO, inalterado (BAIXO, não trava)

### 5. BAIXO -- runtime_v409.py v409_traducao_mechanics (c3–c13, c18–c20) e registros_v409/estatuto «[REAL] as 20 checagens»

**Achado.** Treze das 20 checagens sao aritmetica/algebra numerica sobre a instancia de brinquedo FIXA do contrato (nao leem o core, o kernel nem beta, exceto c13): medido — trocar a instancia SIM por outra satisfazivel continua selando (c2_mecanica_direta); trocar por insatisfazivel ou a NAO por satisfazivel reprova c4/c10/c20 (e c6/c12). O texto ja' diz «aritmetica da instancia de brinquedo … nao prova nada por si: quem prova e' o kernel» (limites[15]), entao e' honesto; igual ao BAIXO 2 da v408.

**Evidencia.** revisao_terceiro/c2_mecanica_direta_out.txt (18 casos, 0 falhas); c_fail_closed_out.txt (125 casos ok).

**Correcao.** Nenhuma obrigatoria; se quiser, dizer no estatuto «conferencia numerica» nas 13 e «lida do kernel/core» nas 7 (c1, c2, c13?, c14, c15, c16, c17).

**Estado na R2.** ABERTO, inalterado (BAIXO, não trava)

### 6. BAIXO -- registros_v409.py (cunhagens_v409 u1: «as 17 checagens»); runtime_v409.py docstring de v409_traducao_mechanics («as 62 ancoras», «17 checagens do DESENHO §2»); RELATORIO_PREPARACAO_v409 §6 e PLANO §1 (tipo do nome «…DECLARADO», «DECLARADO_ate_a_ratificacao»)

**Achado.** Contagens e rotulos envelhecidos apos o bundle de dois modulos (62 -> 82 ancoras; 17 -> 20 checagens) e apos a D62 (nomes ratificados): u1 descreve «as 17 checagens» e a docstring da mecanica cita «62 ancoras»; o RELATORIO/PLANO ainda rotulam o tipo do nome do ParNaFaceDeFock como «DECLARADO ate a ratificacao» (vem do recibo de ~19h30, anterior a D62). Nenhuma checagem depende desses textos; os registros (N_CHECKS_FECHO = 20, 82 ancoras) estao certos e conferidos.

**Evidencia.** revisao_terceiro/_nodes/v409_traducao_mechanics.txt; revisao_terceiro/t4_specs.py (u1); RELATORIO_PREPARACAO_v409.md §6.

**Correcao.** Atualizar as duas cadeias de texto na mesma regeneracao do candidato (o u1 vai ao candidato).

**Estado na R2.** ATENDIDO nos fontes que vão ao candidato: u1 = «as 82 ancoras, o sha256 dos dois modulos, as 20 checagens, o gate» (valores lidos de DL.N_CHECKS_FECHO); docstring da mecanica e do delta = 82 e 20; grep «17 checagens|62 ancoras» nos textos novos: 0. RELATORIO/PLANO (preparação, não público) não conferidos.

### 7. BAIXO -- pedra/TraducaoTuring.lean:15-17 e pedra/ParNaFaceDeFock.lean:12-15 (docstrings embutidas no kernel)

**Achado.** Dizem «ficam [DECLARADO] ate a ratificacao» sobre nomes que o operador ratificou («Ratifico os nomes», D62). E' o que a D62 decidiu (o kernel nao e' refeito) e os registros/textos da v409 dizem a ratificacao e explicam a diferenca (cunhagens_v409 `os_nomes_ratificados`, D62). Fica registrado: o texto permanente do kernel embutido nao acompanha o estatuto atual.

**Evidencia.** pedra/*.lean; delta_v409.py D62; registros_v409.py extras.os_nomes_ratificados.

**Correcao.** Nenhuma (decisao D62); na proxima volta do kernel, trocar por «ratificado pelo operador em 05/11/2026».

**Estado na R2.** ABERTO, inalterado (BAIXO, não trava)

### 8. BAIXO -- pedra/TraducaoTuring.lean:49-50 (docstring) e :449-452; pedra/ParNaFaceDeFock.lean:46; _V409_TRADUCAO_CONTRACT (papeis)

**Achado.** Citacoes entre « » que nao sao substring verbatim das falas: «o nP é o modo seleção … a aniquilação … retornando a leitura» (a fala escreve o "nP"é, sem espaco, e «a seleção é a aniquilação…»), «antes disso o campo ψ …» (a fala escreve /psi), «nP = modo seleção» (paráfrase atribuída a «leitura dele»), «o par de psíons é o gráviton» e «o falso não tem geometria» (leituras da casa, nao desta fala). Ja' APONTADAS pela construcao (`conferir_citacoes_v409.py`, `_APONTADAS_PEDRAS`); nenhuma inventa conteudo: sao a fala com grafia normalizada, uma paráfrase, ou citacao de pedra anterior. Precedente: BAIXO 5 da v408.

**Evidencia.** revisao_terceiro/e_citacoes.py + e_citacoes_out.txt (69 citacoes nao casadas, >=12 chars: as de texto NOVO sao as listadas; o resto e' historico das secoes v394–v408 do artigo, codigo de guarda e artefatos de concatenacao); cunhagens_13out/OPERADOR_05nov_resposta_bit_oitava_….txt.

**Correcao.** Ao refazer o kernel: tirar as aspas da paráfrase «nP = modo seleção» e normalizar a grafia da fala ou dizer «grafia normalizada». Nao trava.

**Estado na R2.** ABERTO, inalterado (BAIXO, não trava)

### 9. BAIXO -- runtime_v409.py _v409_guarda_frases (F43) e F35

**Achado.** A F43 exige a presenca da E28 («NP … numa leitura» e «leitor que se lê») onde o leitor de Turing aparece, mas nao a ausencia de uma afirmacao contraria: sondas «com o leitor que so' conta, a igualdade P = NP vale; <E28>», «P^leitor = NP^leitor para o leitor que so' conta; <E28>» e «the counting reader gives P = NP relative to the reader» PASSAM. A F35 nao pega o EN curto «Clay resolved» (pega «Clay problem solved», «Clay resolvido»). Limites da guarda, nao defeito de texto: minha varredura propria (b) sobre todos os textos novos e rendidos achou 0 afirmacoes da igualdade para o leitor que so' conta fora da propria E28.

**Evidencia.** revisao_terceiro/c_fail_closed_out.txt (SONDA E28 violada; 'Clay resolved'), t5_guarda_probes.py, h_guardas_out.txt.

**Correcao.** Opcional: acrescentar uma F44 que reprove «igualdade (vale|e' teorema) … leitor que so' conta» sem negacao, e «Clay resolved». Nao trava.

**Estado na R2.** PARCIAL: a F41b/F40b entraram (as 4 sondas de Fock/Ω passam a reprovar); a F43 e o EN curto «Clay resolved» seguem como estavam; a F41b não casa «OPEN:» sem colchetes próprios nem paráfrases («ainda não foi ligado», «fica para a v411», «continua por fazer», «é pendência»): ver o MÉDIO e o BAIXO novo.

### 10. BAIXO -- kernel/FLAGS_v409.json, CANDIDATO_v409.json politica_de_bandeiras, textos «158 bandeiras, so' de declaracao nomeada»

**Achado.** As 158 bandeiras sao 136 declaracoes com «depends on axioms» (as 82 ancoras + 54 outros teoremas/lemas nomeados) e 22 que «does not depend on any axioms» (definicoes/estruturas: `selecao`, `inscricao`, `custoCNF`, `SAT`, `Literal`, `CNF`, …); 76 das 158 nao sao ancora. Os textos dizem «so' de declaracao nomeada» (correto) e nao «158 teoremas». Igual ao BAIXO 3 da v408; o gate e a escada contam bandeiras, nao teoremas.

**Evidencia.** revisao_terceiro/m_flags_out.txt, m4.py (136 + 22 = 158).

**Correcao.** Nenhuma obrigatoria.

**Estado na R2.** ABERTO, inalterado (BAIXO, não trava)

### 11. BAIXO -- pedra/TraducaoTuring.lean (p_igual_np_no_modo_selecao) e os textos «o tempo e' t = n ln 2/(β g), linear nos bits»

**Achado.** O enunciado do kernel traz, como ultimo conjunto, exp(−(t·β·g)) = exp(−K.octaveNats n) com t := n·ln 2/(β·g) — a identidade da lei tempo = moeda no t escolhido; a taxa real de convergencia esta' em `a_trava_em_tempo_linear` (resto ≤ e^{-L} em t = n ln 2/2 + L), nao na convergencia (Tendsto sem taxa) do modo selecao. Os textos dizem «pela lei tempo = moeda» e a docstring diz «o enunciado de maquina de Turing (a selecao contada em passos de maquina) nao e' o deste teorema»: honesto. Fica como partitura para o operador: «linear nos bits» e' a lei da moeda, nao um numero de passos de maquina.

**Evidencia.** revisao_terceiro/axiomas_terceiro_out.txt (#check p_igual_np_no_modo_selecao, a_trava_em_tempo_linear); pedra/TraducaoTuring.lean:449-466.

**Correcao.** Nenhuma obrigatoria.

**Estado na R2.** ABERTO, inalterado (BAIXO, não trava)

### 12. BAIXO -- runtime_v409.py _v409_guarda_frases (F41b/F40b, novas na R2)

**Achado.** As guardas novas casam «[OPEN]», «em aberto», «segue/fica/continua/está aberto», «stays/remains/is open» no MESMO trecho que «face de Fock»/«par de Fock»/«ParNaFaceDeFock» (e «Ω … uniforme» em lista aberta), com isenção por «E21», «v407», «deixou», «dizia» e «podad…». Sondadas (t5_guarda_probes.py): as 4 sondas da R1 e 3 variantes reprovam; as 7 frases certas passam; ESCAPAM: a forma «OPEN:» sem colchetes próprios (a do MÉDIO) e paráfrases «ainda não foi ligado», «fica para a v411», «continua por fazer», «é pendência». A isenção por «e21/v407/deixou/dizia» é contornável por quem escrever essas palavras no mesmo trecho. Limite de regex, não defeito de texto novo (varredura ampla: 0 outras ocorrências).

**Evidencia.** revisao_terceiro/t5_guarda_probes_out.json; t1b_fock_open_amplo_out.json.

**Correcao.** Estender a F41b com \bOPEN\b e, se quiser, com «ainda não», «por fazer», «pendente», «fica para». Não trava além do MÉDIO.

**Estado na R2.** NOVO

### 13. BAIXO -- RELATORIO_PREPARACAO_v409.md linha 65 (§5, item 2, «Dizer ao operador, na lingua dele (regra do posto), o que a v409 NAO entrega»)

**Achado.** O relatorio de preparacao (nao publico, mas e' o roteiro do que a gerencia le ao operador) ainda lista entre o que a v409 «NAO entrega»: «o par na face de Fock segue aberto (D60); o Omega do psion e o uniforme da instancia tem a mesma forma, e que sejam o mesmo segue aberto». O par esta' LIGADO (kernel, registro, artigo) e a identidade esta' PODADA. Se a gerencia ler o roteiro como esta', repete ao operador o [OPEN] errado (regra do posto: a partitura tem de dizer o que o teste decide e nao decide). O texto e' gerado por gerar_relatorio_v409.py e nao foi regenerado com a D60 revista.

**Evidencia.** RELATORIO_PREPARACAO_v409.md:65 (mtime 22:37, depois da correcao); h_guardas_out.txt «GUARDA ACHOU em RELATORIO_PREPARACAO_v409.md ... F41».

**Correcao.** Corrigir a linha no gerar_relatorio_v409.py («o par na face de Fock esta' ligado nesta versao; a identidade Omega = uniforme esta' podada, a ponte e' a inscricao») e regenerar; nao muda o candidato.

**Estado na R2.** NOVO (ja' presente na R1, nao anotado por mim)

## Ressalvas

- R2 de ate tres rodadas (D58). A R1 esta' guardada em bytes: REVISAO_TERCEIRO_v409.R1.json/.R1.md, PEDIDO_CORRECAO_R1_v409.md e r1_saidas/. Fora de revisao_terceiro/ nao escrevi nada; nao rodei `lake build`, o instalar, o rito nem o orquestrador (so' _plano(), com ORQ redirecionado a esta pasta).
- Nenhuma pedra mudou entre a R1 e a R2 (sha16 de pedra/*.lean e do KERNEL_RECIBO identicos), entao o Lean da R1 (82 #print axioms, varredura de 223 constantes, compilacao independente das duas fontes) continua valendo; reconferi por d_kernel.py contra o candidato novo.
- O MEDIO da R2 e' de TEXTO do pos-rito (textos_v409*.py NAO sao embutidos no um.py): corrigi-lo nao muda o candidato (de2244483b35f5a3); muda pos_rito/textos_v409_novo.pysnip, o montado textos_v409.py, o harness e a PRONTA. Se a gerencia estender tambem a F41b em runtime_v409.py, o candidato muda e a R3 refaz as conferencias (os scripts desta pasta rodam sem edicao).
- arquivos_revisados: sha16 lidos agora, na R2. Se qualquer arquivo listado mudar, esta revisao nao vale para ele. O Mapa de Rotas nao foi consultado nem alimentado por mim.

## Rotas examinadas (para a gerencia registrar no Mapa)

- R1-A (intocados/mudados): a_intocados*.py e a2_mudados.py sobre base_v408 x candidato: 38 nomes iguais por AST e fonte (gate, neutrino, ramo B, ledger, GA, registros v408/v407/v406 e seus textos); mudados 27 == declarados; novos 14 == declarados; 0 removidos; contratos antigos mudam SO' expected_ladder 12029 -> 12187 (28 ocorrencias); _V408_SPECS +E26 e pisos h2/h3/h6/h8 (declarados); _V407_FONTES muda SO' a chave psion_no_acervo_do_imac_03nov (copia PURGADA, sha256 f0b1c79a5caa75df…, a mesma da v408, D57d); _LEAN_THEOREM_FLAGS +158 (ext_tu409_*), sub-dict da base igual.
- R1-B (kernel/Lean): d_kernel.py; b_gera_lean.py + `lake env lean` no sandbox: 82 #print axioms no trio, varredura MetaM de 223 constantes, rc 0, 352 s; compilacao independente das duas fontes embutidas (30 s + 32 s), rc 0.
- R1-C (fail-closed): c_fail_closed.py (127 casos), c2_mecanica_direta.py (18), k_funcoes_vivas.py (34): ancoras, bandeiras, fontes, raiz, escada, gate, beta, contrato, falas, texto proibido, instancias recusam; a ordem errada dos specs recusa.
- R1-D (textos): h_guardas.py sobre 69 arquivos (fontes, pysnips, pedras, 52 textos rendidos do harness, artigo PT/EN do ensaio, .md): guardas limpas; varredura propria (a)–(f); t1/t2 (Fock + [OPEN]); t5 (sondas da guarda). Achado: o MEDIO.
- R1-E (hashes/orquestrador): f_hashes.py (63 checagens ok), n_hashes_digitados.py, n2_hashes_docs.py, l_orquestrador.py, m_flags_audit.py + m4.py.
- R2-A: reconferencia sobre o candidato de2244483b35f5a3: a_intocados*.py (38 nomes iguais, 27 mudados == declarados, 14 novos == declarados), a2_mudados.py, d_kernel.py, f_hashes.py, e_citacoes.py, c_fail_closed.py, c2, k_funcoes_vivas.py, l_orquestrador.py, m_flags_audit.py, h_guardas.py.
- R2-B: t1b_fock_open_amplo.py (varredura ampla de «Fock/Ω uniforme» + OPEN/aberto/pendente/v41x em fontes e 52 textos rendidos): acha so' o cabecalho do paragrafo README/site; t5_guarda_probes.py (guarda reforcada).
- R2-C: diff R1 x R2 dos fontes (r2_diffs.py): registros (estatuto, u1, frase), runtime (F41b/F40b e docstring), guarda_frases (casos), delta (docstring, frase), artigos PT/EN (frase), textos_v409_novo.pysnip (3 linhas).

## arquivos_revisados (sha16 lidos agora)

- `um_v409_candidato.py` `de2244483b35f5a3`
- `CANDIDATO_v409.json` `4104ea63e1cd601b`
- `COMPARACAO_V408_v409.json` `dc9b6afbd6e981d2`
- `ESPERADOS_v409.json` `5dc1ae7985600ec3`
- `BUNDLE_v409.json` `b218d3bdc44e94c7`
- `kernel_modulos_novos_v409.json` `70be69218e62fd41`
- `VERBATIM_CONGELADO_v409.json` `ecefa04ddf021bef`
- `GUARDA_FRASES_v409.json` `b8280faf5eb35a19`
- `delta_v409.py` `70a49fc5563fc065`
- `registros_v409.py` `e673b74136a014a9`
- `runtime_v409.py` `b2a5b6ee94d2fa92`
- `guarda_frases_v409.py` `16a75b86bf652e92`
- `guarda_p18_v409.py` `2b434b1c8894dbdf`
- `artigo_pt_v409.pysnip` `03fd66151913d135`
- `artigo_en_v409.pysnip` `8388a9d51c5eec4b`
- `pedra/TraducaoTuring.lean` `4fe1c5ba2bc28300`
- `pedra/ParNaFaceDeFock.lean` `4b7ed028ebf5855d`
- `kernel/KERNEL_RECIBO_v409.json` `12a71b3cc86924ab`
- `kernel/FLAGS_v409.json` `fd9ab8820880fe91`
- `kernel/KH_N1_v409.json` `ef646b95adf6c3c0`
- `kernel/POS_BUILD_v409.json` `e3f21e1dd152f93a`
- `pos_rito/textos_v409_novo.pysnip` `2654c81f1b646198`
- `pos_rito/textos_v409.py` `5abdb0be2b7ecacc`
- `pos_rito/textos_custodia_handoff_v409.py` `ef9df32a0a80f252`
- `pos_rito/CUSTODIA_v409_RASCUNHO.txt` `dbebb398de4cbf68`
- `orquestrador/pos_treino_v409.py` `8bdd16f45c7ec5c2`
- `PREPARACAO_v409_PRONTA.json` `7f37aa1195e2786b`
- `dry_v409/core_ensaio.json` `786cc04af38b0690`
