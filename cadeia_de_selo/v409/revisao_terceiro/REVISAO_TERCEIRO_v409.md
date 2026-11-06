# REVISAO DE TERCEIRO v409 -- R3, a ULTIMA (Claude Sonnet; nao construi a v409)

**APROVADA** -- candidato `53284ba461ecd940` (43970027 bytes; no inicio da R3 `53284ba461ecd940`; mudou durante a revisao: nao; o da R2 era `de2244483b35f5a3`, o da R1 `eab2d12055b47df0`). ALTO 0 | MEDIO 0 | BAIXO 12.

aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. Os BAIXOS ficam escritos e nao travam. R1 e R2 guardadas em bytes ao lado (`.R1`/`.R2` `.json`/`.md`, `PEDIDO_CORRECAO_R1/R2_v409.md`, `r1_saidas/`, `r2_saidas/`). Se qualquer arquivo de `arquivos_revisados` mudar, esta revisao nao vale para ele.

## Condicoes da aprovacao (calculadas)

- candidato_integro: True
- mudados_27_novos_14: True
- intocadas_38: True
- fail_closed_sem_falha_inesperada: True
- k_funcoes_vivas: True
- c2: True
- hashes_sem_falha_inesperada: True
- controle_negativo_das_guardas: True
- sondas_da_guarda: True
- minha_varredura_independente_zero: True
- nenhuma_pedra_mudou: True

## Situacao dos achados da R1 e da R2

- **R1-MEDIO 1 (par na face de Fock [OPEN] em texto novo) / R2-MEDIO (cabecalho do paragrafo README/site):** ATENDIDO nos quatro lugares + o cabecalho: estatuto do registro («[REAL] o par na face de Fock LIGADO … PODADA a identidade … [OPEN] a independencia …»), `_respostas`, bloco [OPEN] do core memory, e o CABECALHO do paragrafo README/site (rendido em paragrafo_v409.txt e handoff.txt: «[REAL: … o par na face de Fock LIGADO (`ParNaFaceDeFock`) · INPUT … · KNOWN … · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]»). Minha varredura independente (t6): 0 segmentos «Fock/Ω–uniforme + OPEN/aberto/pendente/ainda nao/por fazer/fica para/v41x» fora do historico declarado, em fontes novos, 52 textos rendidos, secao v409 do artigo PT/EN, linha do .md, registros v409 do core e RELATORIO/PLANO; sensibilidade provada (t6_sensibilidade.py: 6 de 6 formas ruins pegas, 2 de 2 boas e historicas passam).
- **BAIXO 1 (R1/R2) pos_rito/textos_v409_novo.pysnip:617-633 (_paragrafo_v409_de:** ATENDIDO: `_paragrafo_v409_de` acha cada item do `diz` pelo CONTEUDO (`_diz(prefixo)`, recusa se nao achar UMA vez); o README/site rendido traz os marcadores certos («O dicionario de Turing» = o dicionario; «A trava no Nome» = a trava; «A maquina com o leitor», «A inscricao no psion», «O par na face de Fock» e «O que nao muda» proprios).
- **BAIXO 2 (R1/R2) artigo_pt_v409 (secao «O alcance, dito» e «A maquina com o l:** ATENDIDO nas frases-chave: «a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada)» em artigo PT/EN, delta, registros e textos. Resto: formas antigas, corretas e com [KNOWN]/BGS na mesma ressalva (limites[0]: «vale para o leitor que se le (… BGS 1975 …) [KNOWN]»), mas `diz[3]` («ela vale para o leitor que se le») e `nao_diz[8]` seguem sem o selo; BAIXO, nao trava.
- **BAIXO 3 (R1/R2) o enunciado de uma_leitura_decide_SAT / a_maquina_com_o_leit:** ABERTO (BAIXO): inalterado; o texto separa [REAL] de [KNOWN].
- **BAIXO 4 (R1/R2) runtime_v409.py v409_traducao_mechanics (c3–c13, c18–c20) e :** ABERTO (BAIXO): inalterado; o texto ja' diz «aritmetica da instancia de brinquedo … quem prova e' o kernel».
- **BAIXO 5 (R1/R2) registros_v409.py (cunhagens_v409 u1: «as 17 checagens»); ru:** ATENDIDO nos fontes que vao ao candidato (82, dois modulos, 20; sem «17 checagens|62 ancoras» em texto novo). O RELATORIO §6 e o PLANO §1 ainda rotulam o tipo do nome «…DECLARADO / DECLARADO_ate_a_ratificacao» (preparacao, nao publico): PARCIAL, BAIXO.
- **BAIXO 6 (R1/R2) pedra/TraducaoTuring.lean:15-17 e pedra/ParNaFaceDeFock.lean:** ABERTO (BAIXO, decisao D62): as docstrings embutidas seguem «[DECLARADO] ate a ratificacao».
- **BAIXO 7 (R1/R2) pedra/TraducaoTuring.lean:49-50 (docstring) e :449-452; pedr:** ABERTO (BAIXO): citacoes ja' apontadas; nenhuma nova.
- **BAIXO 8 (R1/R2) runtime_v409.py _v409_guarda_frases (F43) e F35:** PARCIAL: F41b/F40b/F42 estendidas e eficazes (22 de 22 sondas reprovam, 8 frases certas passam); a F43 so' exige a presenca da E28 e o EN curto «Clay resolved» segue sem F35 (BAIXO).
- **BAIXO 9 (R1/R2) kernel/FLAGS_v409.json, CANDIDATO_v409.json politica_de_band:** ABERTO (BAIXO): 136 + 22 = 158, inalterado.
- **BAIXO 10 (R1/R2) pedra/TraducaoTuring.lean (p_igual_np_no_modo_selecao) e os :** ABERTO (BAIXO): partitura para o operador, nao defeito.
- **BAIXO 11 (R1/R2) runtime_v409.py _v409_guarda_frases (F41b/F40b, novas na R2):** ATENDIDO: a F41b agora casa «OPEN» (case-sensitive, com ou sem colchetes), «em aberto/aberta», «segue/fica/continua/permanece/esta' aberto|pendente», «pendente», «por fazer», «ainda nao (foi) ligad…», «v41x», «stays/remains/is/still open|pending», «not yet linked», com o ponto mediano como separador; a F42 cobre qualquer v41x («fica para a v411», «deixado para a v413»). Residuo: a isencao por «e21/v407/deixou/dizia/ficava» e' contornavel por quem escrever essas palavras no mesmo trecho; BAIXO.
- **BAIXO 12 (R1/R2) RELATORIO_PREPARACAO_v409.md linha 65 (§5, item 2, «Dizer ao:** ATENDIDO: §5 item 2 agora diz «o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista); a identidade Omega = uniforme esta' podada (a ponte e' a inscricao); com o leitor que so' conta, a igualdade completa nao esta' provada (E28, validade nao afirmada)».

## O que passou na R3 (por script, nesta pasta)

- **Lean:** {"print_axioms_impressos": 82, "ancoras_no_candidato": 82, "todas_as_ancoras_impressas": true, "fora_do_trio": 0, "so_propext": ["TGLExt.TraducaoTuring.custoCNF_cons"], "varredura_metam": "constantes varridas nos 2 modulos: 223 ; por modulo: #[(TGLExt.TraducaoTuring, 150), (TGLExt.ParNaFaceDeFock, 73)]", "varredura_fora_do_trio_ou_sorryAx": 0, "rc": ["0"], "tempo": "352 s", "sandbox": "C:/t/k409c/final (copia axiomas_terceiro.lean apagada ao fim)", "nota": "nenhuma pedra mudou desde a R1 (pedra/*.lean, KERNEL_RECIBO, FLAGS, KH_N1, POS_BUILD, orquestrador: mesmos sha16 da R2); o `lake env lean` e a compilacao independente das duas fontes da R1 valem; d_kernel.py reconferido sobre o candidato novo: embutido == sandbox == pedra == BUNDLE (2 de 2), raiz = raiz v408 + 2 imports, 1761 embutidos == sandbox", "compilacao_independente_das_fontes": {"TraducaoTuring": {"print_axioms": 72, "fora_do_trio": 0, "so_propext": ["TGLExt.TraducaoTuring.custoCNF_cons"], "rc": ["0"], "tempo": "30 s", "linhas_estranhas": [" Classical.choice,", " Quot.sound]", " Classical.choice,", " Quot.sound]", " Classical.choice,"]}, "ParNaFaceDeFock": {"print_axioms": 10, "fora_do_trio": 0, "so_propext": [], "rc": ["0"], "tempo": "32 s", "linhas_estranhas": []}}}
- **a_intocados:** {"nomes_iguais_por_AST_e_fonte": 38, "mudados_igual_declarado_27": true, "novos_igual_declarado_14": true, "removidos": [], "blocos_fora": 1, "obs": "o unico bloco fora dos nos declarados e' o comentario-cabecalho da secao v409; a_intocados_b: 31 linhas fora = comentarios/brancos, 0 linhas da base removidas fora dos nos mudados; _c: 0 segmentos nao declarados diferentes"}
- **a2_mudados:** 27 mudados: contratos antigos SO' expected_ladder 12029 -> 12187 (28 ocorrencias, 0 restantes); _V407_FONTES SO' a chave psion_no_acervo (copia purgada); specs +errata e pisos declarados; _LEAN_THEOREM_FLAGS +158 (sub-dict da base igual); build_pt/build_en/emit_canonical_md/main/prove_external_ladder so' acrescimos (0 linhas removidas); resultado igual ao da R2 exceto o texto das frases (R3)
- **c_fail_closed:** {"ok": 146, "falha": ["guarda: Clay resolved", "guarda: a máquina sem leitor fica fora; P = nP não é o P = NP de Turing"], "nota": "as 2 'falhas' sao expectativas MINHAS de sondagem (EN curto «Clay resolved»; uma frase de teste sem o qualificador, que a guarda acerta em reprovar); 82/82 ancoras, 158/158 bandeiras, 14/14 falas, fontes, raiz, escada, gate, beta, contrato recusam; casos R3 acrescentados (forma «OPEN:», paraphrases, v41x, frase nova do leitor)"}
- **c2_mecanica_direta:** {"ok": 18, "de": 18}
- **k_funcoes_vivas:** {"ok": 34, "falha": []}
- **f_hashes:** {"checagens_ok": 63, "falhas": ["varredura geral: todo {path, sha256} existente == disco"], "divergentes_historicos": ["PINO_RECIBO_PRE_SELO_v409.json/adendo_de_pino_do_t12/antes", "SESSION_REFERENCE_prep_v409.json/source", "acom_prep_20261105T124757_init.receipt.json/result/reference/source"], "nota": "a unica falha e' a varredura geral e so' por 3 pares historicos esperados: adendo T12 «antes» (o Nos antes da v408) e 2 referencias de sessao ao DESENHO no momento do init (o DESENHO e' append-only); CANDIDATO.sha16/sha256/bytes/delta, ESPERADOS, PINOS_BN, BUNDLE, KERNEL_RECIBO e FORMAL_MAP conferem com o candidato NOVO"}
- **e_citacoes:** 14 falas do VERBATIM_CONGELADO existem em cunhagens_13out com o sha256 declarado; nenhuma citacao nova em « » fora do corpus (mesmas nao casadas da R2)
- **l_orquestrador:** plano rc True; main SEM s7_g1 e SEM s10_app; pos_treino_v409.py inalterado desde a R1 (mesmo sha16)
- **h_guardas:** {"controle_negativo_ok": true, "varredura_propria": {"(a) P = NP esta provado / e' teorema (NP maiusculo)": 25, "(b) 'com o leitor a igualdade vale'": 19, "(d) v410": 25, "(d) par na face de Fock [OPEN] / em aberto": 25, "(a) resolve o milenio / Clay resolvido": 13, "(c) Omega e' o uniforme (identidade)": 6, "(f) DECLARADO ate a ratificacao (texto novo)": 18, "(b) P^leitor = NP^leitor afirmado": 2, "CONFIRMED / PROVED_BY": 25, "pos-dicao": 14, "tudo derivado / nenhuma hipotese resta": 1, "(b) E28 violada: igualdade vale para o leitor que so' conta": 1}}
- **guarda_reforcada:** {"sondas_que_deviam_reprovar": 22, "reprovam": 22, "frases_certas": 8, "passam": 8, "falhas": []}
- **varredura_independente_t6:** {"A_fontes_e_textos_rendidos": 0, "B_artigo_md_core": 0, "C_relatorio_plano": 0}
- **frase_do_leitor:** «esta' provada para o leitor que le tambem as maquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada)» em registros (ressalva 1), delta, artigo PT/EN, textos do pos-rito e docstring da F43; nenhum texto novo afirma a igualdade para o leitor que so' conta (varredura (b): 0)

## Achados abertos (todos BAIXOS)

### 1. BAIXO -- pos_rito/textos_v409_novo.pysnip:617-633 (_paragrafo_v409_de) e o montado textos_v409.py

**Achado.** O paragrafo pronto para o README do espelho e o site (publico) monta os marcadores com INDICES FIXOS de `pc['diz']` (diz[1], [2], [3], [4], [6]), mas a lista `diz` do registro foi reordenada na v409: diz[2] e' a D61 (leitura juridica do kernel), diz[3] e' a maquina com o leitor/SAT, diz[4] e' a inscricao, diz[6] e' o dicionario. Resultado no handoff.txt rendido: o marcador «O dicionario de Turing» traz a D61; «A trava no Nome» traz a frase da maquina com o leitor (a trava so' aparece na fala citada depois); «O que nao muda» traz o dicionario. Nada falso, mas rotulos trocados num texto que a custodia cola como esta' no README/site.

**Evidencia.** revisao_terceiro (leitura de /c/t/h409/harness_saida_v409/textos/handoff.txt, bloco INICIO_PARAGRAFO_TRADUCAO_TURING_v409) e textos_v409_novo.pysnip:629-633.

**Correcao.** Trocar os indices por busca pelo conteudo (ou reordenar `diz`): dicionario = o item «o dicionario de Turing e' termo»; trava = «a trava no Nome e' termo»; D61 no seu proprio marcador. Corrigir junto com o MEDIO, ja' que o arquivo muda.

**Estado na R3.** ATENDIDO: `_paragrafo_v409_de` acha cada item do `diz` pelo CONTEUDO (`_diz(prefixo)`, recusa se nao achar UMA vez); o README/site rendido traz os marcadores certos («O dicionario de Turing» = o dicionario; «A trava no Nome» = a trava; «A maquina com o leitor», «A inscricao no psion», «O par na face de Fock» e «O que nao muda» proprios).

### 2. BAIXO -- artigo_pt_v409 (secao «O alcance, dito» e «A maquina com o leitor»), artigo_en_v409 («the full equality holds only for the reader that reads itself»); delta_v409.py FRASE da alcance

**Achado.** «a igualdade completa SO' para o leitor que se le» / «the full equality holds ONLY for the reader that reads itself» pode ser lido como «para o leitor que so' conta a igualdade e' falsa». O que se sabe (e a E28 diz certo) e' que a igualdade esta' ESTABELECIDA (Baker–Gill–Solovay) para o leitor que se le e NAO esta' provada para o que so' conta. Nenhum texto afirma a igualdade para o leitor que so' conta (varredura (b): 0 ocorrencias fora da propria errata/citacao), mas «so' para» sugere negacao.

**Evidencia.** revisao_terceiro/h_guardas_out.txt (varredura (b)); dry_v409/dry_v409_pt.txt e _en.txt, secao v409 («O alcance, dito» / «The reach, stated»).

**Correcao.** Redacao: «a igualdade completa esta' estabelecida para o leitor que se le (BGS 1975); com o leitor que so' conta nao esta' provada».

**Estado na R3.** ATENDIDO nas frases-chave: «a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada)» em artigo PT/EN, delta, registros e textos. Resto: formas antigas, corretas e com [KNOWN]/BGS na mesma ressalva (limites[0]: «vale para o leitor que se le (… BGS 1975 …) [KNOWN]»), mas `diz[3]` («ela vale para o leitor que se le») e `nao_diz[8]` seguem sem o selo; BAIXO, nao trava.

### 3. BAIXO -- o enunciado de uma_leitura_decide_SAT / a_maquina_com_o_leitor (pedra) e os textos «uma leitura decide SAT … NP inteiro com uma leitura»

**Achado.** No kernel «uma leitura decide SAT» e' SAT φ ↔ oQueSou ≠ 0, e «o que sou» e' o LIMITE da leitura (`o_que_sou_no_limite`). A versao de tempo finito (uma leitura em s linear em n: YES ⇒ Z(s) ≥ |sol| ≥ 1 por `a_particao_cobre_o_nome`; NO ⇒ Z(s) ≤ 2^n e^{-s} < 1 para s > n ln 2) e' elementar mas esta' ausente como termo; o que e' [KNOWN] e' NP ⊆ P^{#P[1]} (Cook–Levin), nao a leitura do TGL em tempo finito. Os textos separam bem o [REAL] do [KNOWN] e dizem «o leitor que devolve Z (exato)»; a ressalva da fisica (leitura exata num ato) cobre o resto. Fica como precisao.

**Evidencia.** revisao_terceiro/axiomas_terceiro_out.txt (#check uma_leitura_decide_SAT, a_maquina_com_o_leitor, o_que_sou_no_limite); pedra/TraducaoTuring.lean:1066-1093.

**Correcao.** Uma linha em `nao_diz`/ressalva (1): «o termo do kernel le o limite; a leitura em tempo finito (s linear em n) e' elementar e nao e' termo». Nao trava.

**Estado na R3.** ABERTO (BAIXO): inalterado; o texto separa [REAL] de [KNOWN].

### 4. BAIXO -- runtime_v409.py v409_traducao_mechanics (c3–c13, c18–c20) e registros_v409/estatuto «[REAL] as 20 checagens»

**Achado.** Treze das 20 checagens sao aritmetica/algebra numerica sobre a instancia de brinquedo FIXA do contrato (nao leem o core, o kernel nem beta, exceto c13): medido — trocar a instancia SIM por outra satisfazivel continua selando (c2_mecanica_direta); trocar por insatisfazivel ou a NAO por satisfazivel reprova c4/c10/c20 (e c6/c12). O texto ja' diz «aritmetica da instancia de brinquedo … nao prova nada por si: quem prova e' o kernel» (limites[15]), entao e' honesto; igual ao BAIXO 2 da v408.

**Evidencia.** revisao_terceiro/c2_mecanica_direta_out.txt (18 casos, 0 falhas); c_fail_closed_out.txt (125 casos ok).

**Correcao.** Nenhuma obrigatoria; se quiser, dizer no estatuto «conferencia numerica» nas 13 e «lida do kernel/core» nas 7 (c1, c2, c13?, c14, c15, c16, c17).

**Estado na R3.** ABERTO (BAIXO): inalterado; o texto ja' diz «aritmetica da instancia de brinquedo … quem prova e' o kernel».

### 5. BAIXO -- registros_v409.py (cunhagens_v409 u1: «as 17 checagens»); runtime_v409.py docstring de v409_traducao_mechanics («as 62 ancoras», «17 checagens do DESENHO §2»); RELATORIO_PREPARACAO_v409 §6 e PLANO §1 (tipo do nome «…DECLARADO», «DECLARADO_ate_a_ratificacao»)

**Achado.** Contagens e rotulos envelhecidos apos o bundle de dois modulos (62 -> 82 ancoras; 17 -> 20 checagens) e apos a D62 (nomes ratificados): u1 descreve «as 17 checagens» e a docstring da mecanica cita «62 ancoras»; o RELATORIO/PLANO ainda rotulam o tipo do nome do ParNaFaceDeFock como «DECLARADO ate a ratificacao» (vem do recibo de ~19h30, anterior a D62). Nenhuma checagem depende desses textos; os registros (N_CHECKS_FECHO = 20, 82 ancoras) estao certos e conferidos.

**Evidencia.** revisao_terceiro/_nodes/v409_traducao_mechanics.txt; revisao_terceiro/t4_specs.py (u1); RELATORIO_PREPARACAO_v409.md §6.

**Correcao.** Atualizar as duas cadeias de texto na mesma regeneracao do candidato (o u1 vai ao candidato).

**Estado na R3.** ATENDIDO nos fontes que vao ao candidato (82, dois modulos, 20; sem «17 checagens|62 ancoras» em texto novo). O RELATORIO §6 e o PLANO §1 ainda rotulam o tipo do nome «…DECLARADO / DECLARADO_ate_a_ratificacao» (preparacao, nao publico): PARCIAL, BAIXO.

### 6. BAIXO -- pedra/TraducaoTuring.lean:15-17 e pedra/ParNaFaceDeFock.lean:12-15 (docstrings embutidas no kernel)

**Achado.** Dizem «ficam [DECLARADO] ate a ratificacao» sobre nomes que o operador ratificou («Ratifico os nomes», D62). E' o que a D62 decidiu (o kernel nao e' refeito) e os registros/textos da v409 dizem a ratificacao e explicam a diferenca (cunhagens_v409 `os_nomes_ratificados`, D62). Fica registrado: o texto permanente do kernel embutido nao acompanha o estatuto atual.

**Evidencia.** pedra/*.lean; delta_v409.py D62; registros_v409.py extras.os_nomes_ratificados.

**Correcao.** Nenhuma (decisao D62); na proxima volta do kernel, trocar por «ratificado pelo operador em 05/11/2026».

**Estado na R3.** ABERTO (BAIXO, decisao D62): as docstrings embutidas seguem «[DECLARADO] ate a ratificacao».

### 7. BAIXO -- pedra/TraducaoTuring.lean:49-50 (docstring) e :449-452; pedra/ParNaFaceDeFock.lean:46; _V409_TRADUCAO_CONTRACT (papeis)

**Achado.** Citacoes entre « » que nao sao substring verbatim das falas: «o nP é o modo seleção … a aniquilação … retornando a leitura» (a fala escreve o "nP"é, sem espaco, e «a seleção é a aniquilação…»), «antes disso o campo ψ …» (a fala escreve /psi), «nP = modo seleção» (paráfrase atribuída a «leitura dele»), «o par de psíons é o gráviton» e «o falso não tem geometria» (leituras da casa, nao desta fala). Ja' APONTADAS pela construcao (`conferir_citacoes_v409.py`, `_APONTADAS_PEDRAS`); nenhuma inventa conteudo: sao a fala com grafia normalizada, uma paráfrase, ou citacao de pedra anterior. Precedente: BAIXO 5 da v408.

**Evidencia.** revisao_terceiro/e_citacoes.py + e_citacoes_out.txt (69 citacoes nao casadas, >=12 chars: as de texto NOVO sao as listadas; o resto e' historico das secoes v394–v408 do artigo, codigo de guarda e artefatos de concatenacao); cunhagens_13out/OPERADOR_05nov_resposta_bit_oitava_….txt.

**Correcao.** Ao refazer o kernel: tirar as aspas da paráfrase «nP = modo seleção» e normalizar a grafia da fala ou dizer «grafia normalizada». Nao trava.

**Estado na R3.** ABERTO (BAIXO): citacoes ja' apontadas; nenhuma nova.

### 8. BAIXO -- runtime_v409.py _v409_guarda_frases (F43) e F35

**Achado.** A F43 exige a presenca da E28 («NP … numa leitura» e «leitor que se lê») onde o leitor de Turing aparece, mas nao a ausencia de uma afirmacao contraria: sondas «com o leitor que so' conta, a igualdade P = NP vale; <E28>», «P^leitor = NP^leitor para o leitor que so' conta; <E28>» e «the counting reader gives P = NP relative to the reader» PASSAM. A F35 nao pega o EN curto «Clay resolved» (pega «Clay problem solved», «Clay resolvido»). Limites da guarda, nao defeito de texto: minha varredura propria (b) sobre todos os textos novos e rendidos achou 0 afirmacoes da igualdade para o leitor que so' conta fora da propria E28.

**Evidencia.** revisao_terceiro/c_fail_closed_out.txt (SONDA E28 violada; 'Clay resolved'), t5_guarda_probes.py, h_guardas_out.txt.

**Correcao.** Opcional: acrescentar uma F44 que reprove «igualdade (vale|e' teorema) … leitor que so' conta» sem negacao, e «Clay resolved». Nao trava.

**Estado na R3.** PARCIAL: F41b/F40b/F42 estendidas e eficazes (22 de 22 sondas reprovam, 8 frases certas passam); a F43 so' exige a presenca da E28 e o EN curto «Clay resolved» segue sem F35 (BAIXO).

### 9. BAIXO -- kernel/FLAGS_v409.json, CANDIDATO_v409.json politica_de_bandeiras, textos «158 bandeiras, so' de declaracao nomeada»

**Achado.** As 158 bandeiras sao 136 declaracoes com «depends on axioms» (as 82 ancoras + 54 outros teoremas/lemas nomeados) e 22 que «does not depend on any axioms» (definicoes/estruturas: `selecao`, `inscricao`, `custoCNF`, `SAT`, `Literal`, `CNF`, …); 76 das 158 nao sao ancora. Os textos dizem «so' de declaracao nomeada» (correto) e nao «158 teoremas». Igual ao BAIXO 3 da v408; o gate e a escada contam bandeiras, nao teoremas.

**Evidencia.** revisao_terceiro/m_flags_out.txt, m4.py (136 + 22 = 158).

**Correcao.** Nenhuma obrigatoria.

**Estado na R3.** ABERTO (BAIXO): 136 + 22 = 158, inalterado.

### 10. BAIXO -- pedra/TraducaoTuring.lean (p_igual_np_no_modo_selecao) e os textos «o tempo e' t = n ln 2/(β g), linear nos bits»

**Achado.** O enunciado do kernel traz, como ultimo conjunto, exp(−(t·β·g)) = exp(−K.octaveNats n) com t := n·ln 2/(β·g) — a identidade da lei tempo = moeda no t escolhido; a taxa real de convergencia esta' em `a_trava_em_tempo_linear` (resto ≤ e^{-L} em t = n ln 2/2 + L), nao na convergencia (Tendsto sem taxa) do modo selecao. Os textos dizem «pela lei tempo = moeda» e a docstring diz «o enunciado de maquina de Turing (a selecao contada em passos de maquina) nao e' o deste teorema»: honesto. Fica como partitura para o operador: «linear nos bits» e' a lei da moeda, nao um numero de passos de maquina.

**Evidencia.** revisao_terceiro/axiomas_terceiro_out.txt (#check p_igual_np_no_modo_selecao, a_trava_em_tempo_linear); pedra/TraducaoTuring.lean:449-466.

**Correcao.** Nenhuma obrigatoria.

**Estado na R3.** ABERTO (BAIXO): partitura para o operador, nao defeito.

### 11. BAIXO -- runtime_v409.py _v409_guarda_frases (F41b/F40b, novas na R2)

**Achado.** As guardas novas casam «[OPEN]», «em aberto», «segue/fica/continua/está aberto», «stays/remains/is open» no MESMO trecho que «face de Fock»/«par de Fock»/«ParNaFaceDeFock» (e «Ω … uniforme» em lista aberta), com isenção por «E21», «v407», «deixou», «dizia» e «podad…». Sondadas (t5_guarda_probes.py): as 4 sondas da R1 e 3 variantes reprovam; as 7 frases certas passam; ESCAPAM: a forma «OPEN:» sem colchetes próprios (a do MÉDIO) e paráfrases «ainda não foi ligado», «fica para a v411», «continua por fazer», «é pendência». A isenção por «e21/v407/deixou/dizia» é contornável por quem escrever essas palavras no mesmo trecho. Limite de regex, não defeito de texto novo (varredura ampla: 0 outras ocorrências).

**Evidencia.** revisao_terceiro/t5_guarda_probes_out.json; t1b_fock_open_amplo_out.json.

**Correcao.** Estender a F41b com \bOPEN\b e, se quiser, com «ainda não», «por fazer», «pendente», «fica para». Não trava além do MÉDIO.

**Estado na R3.** ATENDIDO: a F41b agora casa «OPEN» (case-sensitive, com ou sem colchetes), «em aberto/aberta», «segue/fica/continua/permanece/esta' aberto|pendente», «pendente», «por fazer», «ainda nao (foi) ligad…», «v41x», «stays/remains/is/still open|pending», «not yet linked», com o ponto mediano como separador; a F42 cobre qualquer v41x («fica para a v411», «deixado para a v413»). Residuo: a isencao por «e21/v407/deixou/dizia/ficava» e' contornavel por quem escrever essas palavras no mesmo trecho; BAIXO.

### 12. BAIXO -- RELATORIO_PREPARACAO_v409.md linha 65 (§5, item 2, «Dizer ao operador, na lingua dele (regra do posto), o que a v409 NAO entrega»)

**Achado.** O relatorio de preparacao (nao publico, mas e' o roteiro do que a gerencia le ao operador) ainda lista entre o que a v409 «NAO entrega»: «o par na face de Fock segue aberto (D60); o Omega do psion e o uniforme da instancia tem a mesma forma, e que sejam o mesmo segue aberto». O par esta' LIGADO (kernel, registro, artigo) e a identidade esta' PODADA. Se a gerencia ler o roteiro como esta', repete ao operador o [OPEN] errado (regra do posto: a partitura tem de dizer o que o teste decide e nao decide). O texto e' gerado por gerar_relatorio_v409.py e nao foi regenerado com a D60 revista.

**Evidencia.** RELATORIO_PREPARACAO_v409.md:65 (mtime 22:37, depois da correcao); h_guardas_out.txt «GUARDA ACHOU em RELATORIO_PREPARACAO_v409.md ... F41».

**Correcao.** Corrigir a linha no gerar_relatorio_v409.py («o par na face de Fock esta' ligado nesta versao; a identidade Omega = uniforme esta' podada, a ponte e' a inscricao») e regenerar; nao muda o candidato.

**Estado na R3.** ATENDIDO: §5 item 2 agora diz «o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista); a identidade Omega = uniforme esta' podada (a ponte e' a inscricao); com o leitor que so' conta, a igualdade completa nao esta' provada (E28, validade nao afirmada)».

## Ressalvas

- R3 = ultima rodada (D58). R1 e R2 guardadas em bytes ao lado (REVISAO_TERCEIRO_v409.R1/.R2.json/.md, PEDIDO_CORRECAO_R1/R2_v409.md, r1_saidas/, r2_saidas/). Fora de revisao_terceiro/ nao escrevi nada; nao rodei `lake build`, o instalar, o rito nem o orquestrador (so' _plano(), com ORQ redirecionado a esta pasta).
- Nenhuma pedra mudou entre a R1 e a R3; o Lean da R1 (82 #print axioms; varredura MetaM de 223 constantes; compilacao independente das duas fontes) continua valendo. Nao li as provas Lean linha a linha.
- Nao revisei instalar_v409.py, reverter_v409.py, rito_v409.sh, conferir_rito_v409.py, o p00, o harness do fechar, a Bancada B3 nem os scripts de superficie (fora da lista do pedido). Os textos do pos-rito foram lidos nos rendidos pelo harness (23:21, depois dos fontes das 23:00), nao regerados por mim.
- arquivos_revisados: sha16 lidos agora, na R3. Se qualquer arquivo listado mudar, esta revisao nao vale para ele (o S1b do orquestrador confere). O Mapa de Rotas nao foi consultado nem alimentado por mim.
- BAIXOS abertos ficam escritos e nao travam: ate duas rodadas por achado BAIXO ja' foram usadas.

## Rotas examinadas (para a gerencia registrar no Mapa)

- R1-A (intocados/mudados): a_intocados*.py e a2_mudados.py sobre base_v408 x candidato: 38 nomes iguais por AST e fonte (gate, neutrino, ramo B, ledger, GA, registros v408/v407/v406 e seus textos); mudados 27 == declarados; novos 14 == declarados; 0 removidos; contratos antigos mudam SO' expected_ladder 12029 -> 12187 (28 ocorrencias); _V408_SPECS +E26 e pisos h2/h3/h6/h8 (declarados); _V407_FONTES muda SO' a chave psion_no_acervo_do_imac_03nov (copia PURGADA, sha256 f0b1c79a5caa75df…, a mesma da v408, D57d); _LEAN_THEOREM_FLAGS +158 (ext_tu409_*), sub-dict da base igual.
- R1-B (kernel/Lean): d_kernel.py; b_gera_lean.py + `lake env lean` no sandbox: 82 #print axioms no trio, varredura MetaM de 223 constantes, rc 0, 352 s; compilacao independente das duas fontes embutidas (30 s + 32 s), rc 0.
- R1-C (fail-closed): c_fail_closed.py (127 casos), c2_mecanica_direta.py (18), k_funcoes_vivas.py (34): ancoras, bandeiras, fontes, raiz, escada, gate, beta, contrato, falas, texto proibido, instancias recusam; a ordem errada dos specs recusa.
- R1-D (textos): h_guardas.py sobre 69 arquivos (fontes, pysnips, pedras, 52 textos rendidos do harness, artigo PT/EN do ensaio, .md): guardas limpas; varredura propria (a)–(f); t1/t2 (Fock + [OPEN]); t5 (sondas da guarda). Achado: o MEDIO.
- R1-E (hashes/orquestrador): f_hashes.py (63 checagens ok), n_hashes_digitados.py, n2_hashes_docs.py, l_orquestrador.py, m_flags_audit.py + m4.py.
- R2-A: reconferencia sobre o candidato de2244483b35f5a3: a_intocados*.py (38 nomes iguais, 27 mudados == declarados, 14 novos == declarados), a2_mudados.py, d_kernel.py, f_hashes.py, e_citacoes.py, c_fail_closed.py, c2, k_funcoes_vivas.py, l_orquestrador.py, m_flags_audit.py, h_guardas.py.
- R2-B: t1b_fock_open_amplo.py (varredura ampla de «Fock/Ω uniforme» + OPEN/aberto/pendente/v41x em fontes e 52 textos rendidos): acha so' o cabecalho do paragrafo README/site; t5_guarda_probes.py (guarda reforcada).
- R2-C: diff R1 x R2 dos fontes (r2_diffs.py): registros (estatuto, u1, frase), runtime (F41b/F40b e docstring), guarda_frases (casos), delta (docstring, frase), artigos PT/EN (frase), textos_v409_novo.pysnip (3 linhas).
- R3-A: reconferencia sobre o candidato 53284ba461ecd940: a_intocados*.py, a2_mudados.py, d_kernel.py, f_hashes.py, e_citacoes.py, c_fail_closed.py (casos R3), c2, k_funcoes_vivas.py, l_orquestrador.py, m_flags_audit.py, h_guardas.py.
- R3-B: t6_varredura_independente_r3.py (a minha varredura: Fock e Ω–uniforme perto de OPEN/aberto/pendente/ainda nao/por fazer/fica para/v41x) em fontes novos, 52 textos rendidos, secao v409 do artigo PT/EN, linha v409 do .md, registros v409 do core e RELATORIO/PLANO: 0 achados; t6_sensibilidade.py; t5_guarda_probes.py (22 sondas que devem reprovar, 8 frases certas).
- R3-C: r3_diffs.py (diff R2 x R3 dos fontes): registros (frase do leitor), runtime (F41b com OPEN case-sensitive, ponto mediano, pendente/por fazer/ainda nao ligad/v41x; F42 v41x), guarda_frases (casos), delta, artigos PT/EN, textos_v409_novo.pysnip (`_diz`, cabecalho, frase, core memory), RELATORIO §5.

## arquivos_revisados (sha16 lidos agora)

- `um_v409_candidato.py` `53284ba461ecd940`
- `CANDIDATO_v409.json` `06f30fc9783e3081`
- `COMPARACAO_V408_v409.json` `e67e1bb11d346159`
- `ESPERADOS_v409.json` `f74e24abb9cfe567`
- `BUNDLE_v409.json` `b218d3bdc44e94c7`
- `kernel_modulos_novos_v409.json` `70be69218e62fd41`
- `VERBATIM_CONGELADO_v409.json` `ecefa04ddf021bef`
- `GUARDA_FRASES_v409.json` `a546f57a481cb0b7`
- `delta_v409.py` `bf546f1dd6fc7bb3`
- `registros_v409.py` `54a886d8ce1eb83a`
- `runtime_v409.py` `3a7fcf271dd52ea8`
- `guarda_frases_v409.py` `c929b3c3e0928be5`
- `guarda_p18_v409.py` `2b434b1c8894dbdf`
- `artigo_pt_v409.pysnip` `6f693be7b2872fed`
- `artigo_en_v409.pysnip` `9b8523e29395e3ca`
- `pedra/TraducaoTuring.lean` `4fe1c5ba2bc28300`
- `pedra/ParNaFaceDeFock.lean` `4b7ed028ebf5855d`
- `kernel/KERNEL_RECIBO_v409.json` `12a71b3cc86924ab`
- `kernel/FLAGS_v409.json` `fd9ab8820880fe91`
- `kernel/KH_N1_v409.json` `ef646b95adf6c3c0`
- `kernel/POS_BUILD_v409.json` `e3f21e1dd152f93a`
- `pos_rito/textos_v409_novo.pysnip` `ccb2eb021ef97a11`
- `pos_rito/textos_v409.py` `4307f5df07e19ae9`
- `pos_rito/textos_custodia_handoff_v409.py` `ef9df32a0a80f252`
- `pos_rito/CUSTODIA_v409_RASCUNHO.txt` `801861b1d66302aa`
- `orquestrador/pos_treino_v409.py` `8bdd16f45c7ec5c2`
- `PREPARACAO_v409_PRONTA.json` `2a3149a13e68291c`
- `dry_v409/core_ensaio.json` `b0b59e28935f2533`
