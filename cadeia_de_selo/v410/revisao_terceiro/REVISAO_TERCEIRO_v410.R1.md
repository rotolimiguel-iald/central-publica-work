# REVISAO DE TERCEIRO v410 — R1 (Claude Sonnet; nao construi a v410)

Quando: 2026-11-09T23:50:54 · candidato `092376092dccfa16` (44993049 B) no inicio e no fim: IGUAL · **aprovada: false** · ALTO 0 · MEDIO 3 · BAIXO 10

## O que passou (medido por script, nesta pasta)

- Codigo: 50 funcoes/constantes intocadas iguais por AST e fonte; 26 mudados e 38 novos == `COMPARACAO`; nenhuma linha de codigo fora dos nos declarados; contratos antigos mudam so' a escada 12187 -> 12271.
- Kernel: embutido == sandbox k410c == pedra == BUNDLE (2/2); `lake env lean` meu: 60 ancoras + varredura MetaM de 88 constantes (22 IALD2 + 66 AEscala), todas no trio, 0 `sorryAx`, rc 0; 84 bandeiras novas com alvo no axiom_report.
- Fail-closed: `iald2_v410` e `a_escala_v410` recusam em todas as mutacoes de ancora (ausente, sorryAx, ofReduceBool, vazia, proveniencia), bandeira, fonte e fala; H0DN e HMS/13 recusam insumo adulterado (1 bit) e caminho sob `kimi\` (c7).
- H0DN: 11 vetores meus na `veredito_h0dn` (ramos 1 a 6, precedencia, fronteiras exatas 5 e 1,959963984540054): como pre-registrado; a cabeca do ramo 4 traz `PROVED_IS_VALIDITY_NOT_CREDITATION` na MESMA string; nenhum caminho de `kimi\` tocado; insumos embutidos == pinos == copias.
- Frases: nenhuma forma proibida (Clay seco, milenio, tautologia, nao resolve, 'nao afirma/prova P = nP', PROVED_BY, 5 sigma atingido, covariancia fechada afirmada, abertura permitida) no texto novo rendido, harness, registros e fontes; frase canonica do Clay PT/EN nos lugares obrigatorios; forma da D81 presente.
- Fora do candidato: nenhuma checagem afrouxada nos consertos (gerar_esperados, conferir_rito, orquestrador S6d, registrar_mapa, harnesses, quadro do pacote). Orquestrador: sem S7/S10, `Stop-Process` so' por PID medido.

## Achados

### 1. [MEDIO] pedra/AEscala.lean: `LeitorDoFundo`, `aPerguntaDoClay`, `a_pergunta_do_clay_tem_resposta`, conjuncoes (1)-(3) de `existe_o_algoritmo_e_e_a_iald` e o conjunto `aPerguntaDoClay X` de `a_escala` (l.558-589, 652-718 da fonte); registro `a_escala_v410` (`diz`[3], `limites`[1], `extras.a_pergunta_do_clay`); artigo PT/EN secao A Escala; .md canonico; `readme_evidente.1_clay_forma_canonica`; handoff

`aPerguntaDoClay X := Nonempty (LeitorDoFundo X)` e' satisfeita SEM nenhum conteudo da TGL: a estrutura exige so' `leitura : (X -> N) -> R -> C`, `limite`, `Tendsto (leitura c) atTop (nhds (limite c))` e `limite c = 0 <-> not exists x, c x = 0`; nao ha' custo, tempo polinomial nem computabilidade no tipo, e o parametro `s` (tempo pago) e' so' um indice. Prova minha em Lean (axiomas_terceiro_v410.lean, compilado no sandbox k410c com `lake env lean`, rc 0, no trio): `theorem a_pergunta_do_clay_sem_TGL (X) [Fintype X] [DecidableEq X] : aPerguntaDoClay X := <leitorTrivial X>` com `leitorTrivial` = leitor CONSTANTE (`leitura c _ := if exists x, c x = 0 then 1 else 0`, `limite` idem, `tendsto_const_nhds`). Logo a frase 'a TGL resolve a pergunta do Clay no sentido do operador: existe o algoritmo, e' a IALD' vale, quanto a 'existe', para qualquer decisor da existencia de solucao, ate' nao computavel; o conteudo da TGL esta' em 'e' a IALD' (a instancia `iald`: a trava, a particao Z, `a_iald_le_a_face_sem_leitura`, `le_como_dissipacao_termica` e os itens 4-10 de `existe_o_algoritmo_e_e_a_iald`: SAT iff, leitor do psion, custo <= n ln 2 nats, tempo linear nos bits). Nenhum dos textos diz isso; a docstring de `LeitorDoFundo` diz so' que a definicao e' [INPUT] e que nao se afirma ser o enunciado do Instituto. Teorema trivialmente verdadeiro por definicao vendido como resultado (item 3f do pedido) e ressalva ausente em texto publico. A 'unicidade' ('e' a IALD') tambem nao esta' no tipo: qualquer leitor constante e' tambem um leitor do fundo.

**Correcao pedida** (toca o candidato: sim (docstrings da pedra -> sha256 da pedra, BUNDLE, kernel incremental; registro; artigo; README)): NAO mudar nomes, enunciados nem provas (o operador ratificou os 44 nomes). Acrescentar a MESMA ressalva, com as mesmas palavras, em: (a) docstring de `LeitorDoFundo`, de `a_pergunta_do_clay_tem_resposta` e de `existe_o_algoritmo_e_e_a_iald` da pedra: 'a definicao `Nonempty (LeitorDoFundo X)` nao exige custo, tempo polinomial nem computabilidade; e' satisfeita por qualquer decisor da existencia de solucao, ate' por um leitor constante; o conteudo da TGL esta' na instancia `iald` (a trava, a particao, o custo <= n ln 2 nats, o tempo linear nos bits), nao na existencia'; (b) `_V410_AESCALA_TEXT.limites` (nova entrada) e `nao_diz`; (c) artigo PT/EN, paragrafo da pergunta do Clay; (d) `readme_evidente.1_clay_forma_canonica.estatuto`; (e) os textos do pos-rito (handoff, README). A frase canonica D84 e a forma da D83 ficam intactas. Se o operador quiser que 'existe o algoritmo' signifique algo, a mudanca e' na DEFINICAO (acrescentar ao tipo um campo de custo/tempo), e essa e' decisao dele, nao desta rodada: dizer-lhe na lingua dele (ver o relatorio).

### 2. [MEDIO] pedra/AEscala.lean (21 passagens «» NAO verbatim; a gerencia contou 22) e pedra/IALD2.lean (2: «P = nP» com espacos, l.23 e l.194); `_V410_*` (E31 e decisoes que citam a frase canonica entre « »)

Varredura minha (e_citacoes_v410.py, corpus = cunhagens_13out + insumos/cunhagens das versoes v405-v410, 291 falas; niveis exata, elisao, sem acentos): AEscala 85 passagens «», 64 casam, 21 NAO: 'o nome pesa 1 porque e' a conjugacao das duas faces que pesam ½ cada' (fala: '1/2'), 'o inalcancavel … nao conjuga, nunca chega a pesar 1, nao acopla' (a fala tem 'mas como nao conjuga nunca chega a pesar 1 e por isso nao acopla'), 'tres faces de ½, duas conjugadas, uma caida (1/3 caiu)', 'qual algoritmo le a face sem leitura … existe, e' IALD' (fusao de duas frases; a fala diz 'qual algoritmo e' capaz de ler'), 'ela e' a justica, e' o ideal, mas e' intocavel', 'a insignia … nao esgota o signo … sustenta' (ordem invertida), 'o infinito inscrito no finito como Nome', 'a nota e' a conjugacao modular' (a fala: 'a nota que e' a conjugacao modular'), 'o Nome acima do Nome' (a fala: 'de Nome acima do Nome'), 'fundamental para P=nP' (a fala: 'fundamenal para a compreensao completa de P=nP'), 'a primeira leitura identifica; a segunda confirma que a operacao nao altera' (docstring do kernel `observing_adds_nothing`, nao fala), e rotulos/frases da gerencia ('Nome = par conjugado, face caida = a que nao conjuga', 'um de tres caiu', 'fala → termos', 'O negativo como tela de fundo da experiencia'). A regra da casa reserva « » a fala verbatim do operador (regua: nunca fabricar citacao; pedido 4(d) da v407) e a pedra e' fonte embutida e selada no um.py. Severidade MEDIA: nao muda prova nem enunciado, mas atribui ao operador, entre aspas, texto que ele nao disse, em fonte selada. Texto rendido (artigo PT/EN, .md, harness) e registros: 0 aspas angulares nao verbatim de fala; as unicas fora de fala sao a frase canonica D84 em « » nas decisoes/E31 do registro (ratificada, nao verbatim: BAIXO) e formulas metalinguisticas (guardas).

**Correcao pedida** (toca o candidato: sim (pedra -> sha256, BUNDLE, FORMAL_MAP, kernel incremental, candidato regenerado, ESPERADOS)): Instalar a correcao PREPARADA `work\pedras_candidatas_09nov\R2_aspas\AEscala.lean` (sha256 09b1b35a14edbc66ff5169379b58e3e6546088bc6632645cbd55281017899384). Revisei o diff (r2_aspas_diff.py): 25 linhas / 17 hunks; a unica diferenca que nao e' troca de delimitador e' a linha de convencao no cabecalho (l.13); 85 «» -> 63 «» + 22 “ ”; as 63 restantes casam todas (e_citacoes_v410: 53 exatas, 9 com elisao, 1 sem acentos, 0 NAO); nenhum nome, enunciado ou prova muda; compile_log.txt: 38 `depends on axioms` no trio, 0 'error'. Na MESMA instalacao: (i) em `pedra/IALD2.lean` trocar as duas «P = nP» (a do cabecalho l.23 e a de `a_forma_matricial...`/seccao 3) por “P = nP” OU escrever «P=nP» como a fala; (ii) nas decisoes/E31 do registro e nos textos do pos-rito, a frase canonica D84 e' ratificada, nao verbatim: trocar « » por “ ” ou por rotulo 'forma canonica (D84)'. Depois da reinstalacao, o registro `a_escala_v410` deve ser rerodado no ensaio (c3 le o sha256 da pedra; c7 a frase canonica PT na docstring; c11 o cabecalho com a ratificacao): ficam intactos no R2 (conferido por mim: PT canonica presente, `RATIFICADOS pelo operador em 09/11/2026` e o sha256 da fala presentes no cabecalho).

### 3. [MEDIO] registro `h0dn_bg1_v410` (`_V410_H0DN_TEXT.estatuto/escopo/o_que_falta[0]/limites/nao_diz`), artigo PT/EN `artigo_*_h0dn_v410.pysnip` (paragrafos 'O que falta e a ressalva da novidade de uso' e 'Ressalvas, ditas'), `readme_evidente.3_h0dn_bg1`, handoff/README do pos-rito

A frase obrigatoria 'pre-registrado; nenhum dado observado lido' e' dita sem escopo em TODO texto publico do H0DN, e `o_que_falta[0]`/o artigo dao `y_obs` como [OPEN] ('a ordem ao Kimi esta' pinada'). Mas o proprio um.py ja' sela, em `_V410_SPECS` (cunhagens_v410, decisoes D78 e D79), que a entrega parcial do Kimi trouxe um `y_obs` de 255 linhas, que o TESTE DE SUPORTE na covariancia publicada REPROVOU '[REAL, lido pela gerencia; o numero nao entra aqui]', que isso e' 'parede de montagem do dado, nao falsificacao da lei K nem leitura de beta_TGL' e que 'se a abertura fosse hoje, a funcao de veredito devolveria o ramo (1) inconclusivo por sistematica' (confirmado por mim: `veredito_h0dn` devolve ramo 1 sempre que `covariancia_fisica_fechada` ou `no_suporte` e' falso; vetores do revisor no c_fail_closed_v410_out.json). Nada disso aparece no texto rendido do artigo PT/EN (grep 'parede', 'montagem', 'reprovou', 'BLOQUEADA': 0 ocorrencias em novo_pt.txt/novo_en.txt), nem no README (`3_h0dn_bg1.agora`), nem na frase do operador do artigo ('o kimi fezz o trabalho e ja' te entregou' esta' no paragrafo seguinte, do HMS/13, sem ligar as duas coisas). Dois defeitos: (1) ressalva ausente em texto publico: o buraco (um vetor foi montado e a gerencia soube que nao cabe no suporte) fica dito so' no spec, nunca disfarcado la', mas disfarcado no artigo; (2) regra do posto: ao ler o artigo/README o operador nao fica sabendo o que o teste devolveria HOJE (inconclusivo por sistematica = parede de montagem, nao falsificacao) nem que um olhar parcial ja' houve. A verdade mecanica ('observed_vector_read False'; 6 caminhos tocados, nenhum sob kimi\; insumos embutidos conferidos por mim: 4 + 6, sha256 e bytes batem com os pinos e com as copias em insumos\) esta' correta; o defeito e' de dizer incompleto. Origem anterior ao olhar: o ramo 'fora do suporte' ja' era de `evaluate` do Codex (h0dn_estimator.py: `data_outside_support`, 06/11) e da funcao congelada D72/E30 (11:44-12:00), antes da entrega do Kimi (D78, ~13:28): o pre-registro nao foi ajustado ao olhar.

**Correcao pedida** (toca o candidato: sim (registro, artigos, readme_evidente, textos do pos-rito)): Acrescentar, SEM mexer na frase obrigatoria nem na funcao de veredito (pinada por sha256, c12): em `_V410_H0DN_TEXT` (`o_que_falta[0]` e uma entrada nova em `ressalvas`), no artigo PT/EN H0DN, em `readme_evidente.3_h0dn_bg1` e nos textos do pos-rito, uma frase unica: 'A entrega parcial do Kimi (09/11) trouxe um y_obs de 255 linhas [DECLARADO pelo Kimi] que NAO cabe no suporte da covariancia publicada (teste de suporte reprovado, [REAL] lido pela gerencia; nenhum Z, razao ou solver foi rodado): se a abertura fosse hoje, a funcao de veredito devolveria o ramo (1), inconclusivo por sistematica, que e' parede de montagem do dado, nao falsificacao da lei K nem leitura de beta_TGL; o um.py nao le esse vetor.' (PT e EN). Nao citar o numero (o spec ja' decidiu que ele nao entra). Ajustar a guarda F54 so' se ela reprovar a frase nova (ela exige 'pre-registrado' e 'nenhum dado observado lido' onde 'H0DN' aparece: manter os dois na mesma frase ou ao lado).

### 4. [BAIXO] artigo PT/EN secao IALD2 (artigo_pt_v410.pysnip l.20; artigo_en_v410.pysnip) e emit_canonical_md (.md canonico, linha 'IALD2 (v410…)')

Gabarito sem concordancia e com numero errado: '2 módulo novo no kernel, em TGLExt/: IALD2' (PT; EN '2 new kernel module…') porque `n_modulos` do iald2_v410 conta 2 (IALD2 e AEscala, ambos no contrato) e a frase nomeia so' IALD2; no .md a mesma linha diz '2 módulo novo … (`IALD2`…) com 84 bandeiras … e 22 âncoras' (o artigo, na mesma secao, diz 22 bandeiras; 84 = IALD2 + AEscala). Numero que nao bate com a frase.

**Correcao pedida** (toca o candidato: sim): Dizer '1 modulo novo (IALD2)' com 22 ancoras e 22 bandeiras na secao IALD2, e os 2 modulos/84 bandeiras so' onde a frase nomeia os dois (ou citar a AEscala).

### 5. [BAIXO] registro a_escala_v410 (runtime_aescala_v410 `_v410_aescala_mechanics`; 12 checagens)

Fail-closed menos forte que o `iald2_v410` e que o `traducao_turing_v409`: com `kernel_formalization.all_verified = False` (ou string 'True') o `a_escala_v410` AINDA sela (c_fail_closed_v410: 'recusado: False' nos dois casos), e com a raiz embutida sem `import TGLExt.AEscala` tambem. Mitigado: cada ancora/bandeira/sha256 e' conferida uma a uma (38/38, 62/62, 4/4 recusam em todas as mutacoes) e o proprio `kernel_formalization` recusado derruba o gate em outro ponto; mas e' regressao de padrao.

**Correcao pedida** (toca o candidato: sim): Acrescentar a c2/c3 `kf_.get('all_verified') is True` e o import da raiz (como `_v410_formal` do iald2).

### 6. [BAIXO] veredito_h0dn (funcao congelada, pinada por sha256)

Nao e' fail-closed para entrada nao finita: `z_tgl = nan` cai no ramo 5 ('discrimina do LCDM a n sigma, com K em tensao') porque todas as comparacoes com nan dao False. Inalcancavel hoje (o `evaluate` do estimador recusa `nonfinite_input` antes), e a funcao esta' pinada: mudar altera o pre-registro.

**Correcao pedida** (toca o candidato: nao (anotacao)): Nao mudar nesta versao; registrar para a versao que abrir o teste: guarda de finitude antes do ramo 1 (e em `evaluate`).

### 7. [BAIXO] _v410_guarda_frases (F44-F58)

Sondas do revisor que a guarda NAO pega: 'A TGL fechou a questao do Clay', 'a IALD respondeu ao problema do Clay e a prova esta' feita', 'Clay esta' provado', 'The TGL has proven P = NP' (as outras 31 sondas reprovam/passam como devem). Varredura independente (g_frases_v410.py, g2_clay_pnp.py) dos textos rendidos NOVOS (artigo PT/EN, .md), do harness, dos registros e das fontes: 0 ocorrencia dessas formas; so' o limite da guarda.

**Correcao pedida** (toca o candidato: nao (anotacao)): Registrar para a v411 (a guarda nao e' tocada nesta versao).

### 8. [BAIXO] pedra IALD2 (cabecalho l.12-13) e `_V410_*` textos

Docstring da epoca: 'os nomes das declaracoes sao da gerencia, [DECLARADO] ate' a ratificacao' em pedra ja' ratificada (D74); o artigo repete 'as docstrings da pedra, da epoca, dizem [DECLARADO] ate' a ratificacao'. Esta' dito no texto (nao e' escondido), mas e' estatuto desatualizado em fonte selada. Idem `o_atrator`: o item (5) 'o senao' e' sobre um Nome finito N arbitrario, nao sobre 'o Nome do par lido' como diz a docstring.

**Correcao pedida** (toca o candidato: sim se mexida): Se a IALD2 for mexida na rodada (aspas), trocar o cabecalho para 'ratificados pelo operador em 09/11/2026 (D74)' e dizer 'para todo Nome finito N' no item (5); senao deixar (dito).

### 9. [BAIXO] registro a_escala_v410 `limites`[0] e cabecalho da pedra (l.87-88)

O dicionario diz 'peso = traco'; mas a mesma lista (`limites`[3]) e o artigo dizem que 'cada face pesa 1/2' e que o traco da face e' 1 (peso ½ = autovalor/pureza). Lidos juntos, 'peso = traco' + 'face pesa ½' sugerem traco ½: e' o erro que o pedido 3(a) proibe. O texto rendido no artigo/.md esta' correto ('autovalor e pureza ½, traco 1'); a linha 'peso = traco' esta' so' no registro (core json) e na pedra.

**Correcao pedida** (toca o candidato: sim (texto)): Trocar por 'peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal (traco 1)'.

### 10. [BAIXO] registro a_escala_v410 `estatuto` e `numeros`; readme_evidente.2

Identidades aritmeticas em ℚ (`tres_faces_pesam_tres_meios`, `um_terco_caiu`, `o_nome_normalizado_e_dois_tercos`, `a_conjugacao…`, `a_escala_fecha`: `norm_num`) e o escalar '(1/2)^2 = 1/2·1/2' ('face_sem_par_ao_quadrado' = 'meio_de_meio' = 1/4) entram como '[REAL] numeros RECALCULADOS a cada rito'. A pedra os marca '[DERIVED, aritmetica em ℚ]'. O que ha' de conteudo e' a conta matricial (Bell, marginal ½·1, ½·1 nao idempotente); '(1/2)^2 = 1/2·1/2' e' tautologia escalar.

**Correcao pedida** (toca o candidato: sim (texto)): Rotular '[DERIVED, aritmetica]' como a pedra faz; tirar a tautologia escalar de 'numeros' ou diz-la matricial ((½·1)² = ½·(½·1) em M₂).

### 11. [BAIXO] pedra AEscala `nenhum_precede`, `a_face_caida_nao_acopla`, `existe_o_algoritmo_e_e_a_iald`

(a) `nenhum_precede`: o termo sao duas equivalencias simetricas nos pontos fixos 0 e 1 (lido=1 <-> objeto=1; lido=0 <-> objeto=0); 'nenhum precede' e' a leitura do operador (a docstring o diz [ONTO]), mas o texto do registro apresenta 'coexistem e nenhum precede' junto dos termos. (b) `a_face_caida_nao_acopla`: 'acoplar' e' definido pela pedra como a compressao N·(½·1)·N (escolha de modelagem da autoria, nao fala do operador, nao marcada como [INPUT]); o termo prova ½·N ≠ N. (c) `existe_o_algoritmo_e_e_a_iald`: os itens (8)-(10) (selecao no Nome, custo <= n ln 2, tempo linear) valem para um `c` ARBITRARIO com solucao, sem ligacao a `custoCNF φ` dos itens (4)-(6); a docstring os encadeia como se fossem da mesma instancia.

**Correcao pedida** (toca o candidato: sim (texto)): Dizer (a) 'equivalencias nos pontos fixos', (b) '[escolha de modelagem: acoplar = comprimir por N]', (c) 'para todo custo c com solucao' na docstring/registro.

### 12. [BAIXO] orquestrador/pos_treino_v410.py (docstring S4 l.12; log do S4 l.302)

Texto desatualizado: 'Só 1 módulo novo compila a frio' / '1 módulo novo a frio' — sao 2 (IALD2 e AEscala; POS_BUILD: build 318 s). S0 le `STATE_v4.json` do treino v4 (DONE em 01/11); nao confirmei que o treino Qwen3.8 em curso (D73) nao reescreve esse arquivo — a pasta da nativa me foi vedada. S6d: a mudanca da regra D59 (kimi so' se H0DN no texto) e' por texto inteiro, nao por contexto; nao afrouxa Milenio/Navier/lindao (continuam vedados em qualquer texto).

**Correcao pedida** (toca o candidato: nao (fora do candidato)): Corrigir o texto do log/docstring; a gerencia confere o S0 contra o estado real do treino antes de lancar.

### 13. [BAIXO] _V410_SPECS / E31 / delta: frase canonica D84 entre « »

A frase canonica e' RATIFICADA pelo operador (fala 7 'Perfeito, concordo plenamente'), mas redigida pela gerencia; aparece entre « » em E31/decisoes do registro (nao no texto rendido do artigo). « » e' reservada a fala verbatim.

**Correcao pedida** (toca o candidato: sim (texto)): Usar “ ” ou o rotulo 'forma canonica (D84, ratificada)'.

## Condicoes calculadas

- candidato_integro_no_inicio_e_no_fim: True
- mudados_26_novos_38_iguais_ao_declarado: True
- intocadas_50_iguais_por_AST_e_fonte: True
- nenhuma_linha_de_codigo_fora_dos_nos_declarados: True
- contratos_antigos_mudam_so_a_escada_12187_12271: True
- kernel_embutido_sandbox_pedra_bundle_iguais: True
- lean_60_ancoras_e_88_constantes_no_trio_sem_sorry: True
- fail_closed_iald2: True
- fail_closed_a_escala_ancoras_bandeiras_fontes: True
- fail_closed_a_escala_kernel_all_verified: False
- h0dn_hms13_insumos_embutidos_batem_e_nada_de_kimi_tocado: True
- veredito_h0dn_11_vetores_do_revisor: True
- cabeca_do_ramo_4_com_validade_nao_creditacao_na_mesma_string: True
- frases_proibidas_zero_no_texto_novo: True
- frase_canonica_clay_PT_EN_nos_lugares_obrigatorios: True
- citacoes_verbatim_pedra_AEscala: False
- pergunta_do_clay_nao_trivial_ou_divulgada: False
- h0dn_texto_publico_com_o_D78_e_o_ramo_1_de_hoje: False
- consertos_fora_do_candidato_sem_afrouxar: True
- orquestrador_sem_S7_S10_sem_kill_por_nome: True

## O que nao consegui conferir (ressalvas)

- R1 de ate' 3 rodadas (D69). Escrevi so' em revisao_terceiro\. Nao rodei lake build, instalar, rito, orquestrador, p00, ensaio a seco nem harness; o `lake env lean` foi em arquivo meu (axiomas_terceiro_v410.lean) com cd em C:\t\k410c\final, UM processo, 296 s.
- NAO abri nem calculei sha256 de kimi\y_obs.npz e kimi\C_fisica_258x258.npz. Li o estimador congelado (texto) e inventariei por nome de chave/forma o npz embutido do H0DN (estimator_frozen.npz: weights, null_basis, C_joint publicada, signal_local, ...), sem imprimir valores; nenhum Z, razao ou suporte observado foi calculado por mim.
- NAO li a pasta da nativa (C:\IALD\TGL_IALD_NATIVE_QWEN5090): nao confirmei que o S0 (STATE_v4.json, treino v4 DONE em 01/11) continua DONE com o treino Qwen3.8 da D73 em curso.
- Li os enunciados e docstrings das duas pedras; NAO li as provas Lean linha a linha (basta o trio e a varredura MetaM).
- NAO recompilei a R2_aspas/AEscala.lean (usei o compile_log.txt da gerencia: 38 no trio, 0 error) nem rodei o registro contra ela; a R2 de revisao confere isso depois da reinstalacao.
- NAO revisei instalar_v410.py, reverter_v410.py, rito_v410.sh, os 7 textos da custodia linha a linha (so' os rendidos pelo harness e o fonte para citacoes/frases) nem a Bancada B(n)/servico.
- Nao reproduzi os 915 controles negativos do harness; li os diffs dos consertos fora do candidato.

## Rotas examinadas

- R1-A: a_intocados_v410/a_intocados_c_v410/a2_mudados_v410 (base_v409 x candidato): 50 nomes iguais por AST e fonte; mudados 26 e novos 38 == COMPARACAO; segmentos nao declarados iguais; contratos mudam so' expected_ladder 12187->12271.
- R1-B: kernel (d_kernel_v410, lean): bundle embutido==sandbox==pedra==BUNDLE; 60 ancoras + varredura MetaM de 88 constantes dos 2 modulos no trio, rc 0; SONDA: aPerguntaDoClay e' satisfeita por leitor constante (a_pergunta_do_clay_sem_TGL).
- R1-C: fail-closed (c_fail_closed_v410) iald2 (22 ancoras, 22 bandeiras, 23 falas), a_escala (38, 62, 8; lacuna all_verified do kernel), h0dn/hms13 (insumo adulterado, c7 com caminho vedado), veredito_h0dn (11 vetores), guarda de frases (38 sondas).
- R1-D: citacoes (e_citacoes_v410, e2_classifica_nao): pedra AEscala 21 «» nao verbatim, IALD2 2; textos rendidos limpos; R2_aspas revisada (r2_aspas_diff).
- R1-E: frases proibidas (g_frases_v410, g2_clay_pnp, g3_frase_canonica) no texto rendido NOVO e fontes: nenhuma; frase canonica PT/EN nos lugares obrigatorios.
- R1-F: H0DN/HMS13 (k_hms13_insumos): 10 insumos embutidos == pinos == copias; chaves numericas so' de erro/bytes/linhas; 0 listas numericas; nada sob kimi\ tocado em rito; _V410_FONTES aponta copias em insumos\; D78/D79 selados no spec mas ausentes do texto publico (achado 3).
- R1-G: hashes (f_hashes_v410), diffs fora do candidato (m_diffs_fora_do_candidato), orquestrador (leitura), flags (84 == alvos no axiom_report).
- Rotas do Mapa consultadas antes: cadeia.preparacao_v410 (EXAMINADA, 1 reg.), estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov (BLOQUEADA), kernel.a_escala_tres_faces_v410_09nov (EXAMINADA; ja' registra que cada_face_pesa_meio e' autovalor/pureza e que nomeObjeto e' ponto fixo de Jconj na face finita, nao o J modular da luz); nao refiz nada delas; a nova a registrar: 'aPerguntaDoClay trivial por leitor constante' (revisao_terceiro R1 v410).