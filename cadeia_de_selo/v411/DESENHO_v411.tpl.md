# DESENHO DA v411 — O TESTE DECISIVO: H0DN × BG1 ABERTO, A EMENDA E O RESULTADO RECALCULADO NO RITO; O TOPO DO RESUMO (gerência c1, 12/11/2026) — a preencher AO LADO conforme a cadeia andar

> A ORDEM que esta versão cumpre (verbatim em `C:\IALD\Central de Patentes\work\cunhagens_13out\`, texto e sha16 LIDOS do arquivo, nunca digitados):
> `{{NOME:ORDEM_ABRIR}}` (sha16 `{{F:ORDEM_ABRIR}}`): «{{V:ORDEM_ABRIR}}»
> `{{NOME:ORDEM_TOPO}}` (sha16 `{{F:ORDEM_TOPO}}`): «{{V:ORDEM_TOPO}}»
> Base: a v410 selada `{{BASE}}` (Nós; sha16 lido de `Nós\um.py`; `um_version` do selo = `{{BASE_VERSAO}}`), custodiada e publicada em 11/11 (D135).
> A divisão do trabalho: a gerência c1 faz o `um.py`; a custódia (commit, push, publicação, site, X) é da sessão de custódia. Esta versão termina no HANDOFF; o orquestrador NÃO publica.
> Moldura (uma frase): o teste pré-registrado da razão de Hubble local/fundo foi aberto uma vez, depois do commit público do pré-registro; sob o modelo de erros publicado o primário lê {{N:zn0_2}} contra o nulo e {{N:zt0_2}} contra K (ramo 4); ao lado, no mesmo item, as Cefeidas livres leem {{N:zn1_2}} (ramo 6); retrodição sem ajuste, com emenda posterior à guarda, teste não cego; provado é validade, não creditação; o gate não se move.

## 1. Pedras (kernel): NENHUM módulo novo

- O kernel da v411 é o da v410, byte a byte: escada {{BASE_ESCADA}} (lida do core da base), nenhuma bandeira nova, raiz `TGLExt.lean` igual. Sandbox `C:\t\k411c\final` copiado de `C:\t\k410c\final` (robocopy SEM /PURGE); nenhum bundle; build incremental (nada a compilar) e Audit só no sandbox, para medir que a escada e as declarações são as da v410.
- Ficam para a versão seguinte, à espera dos nomes do operador: as doze candidatas de 11/11 (`work\fecho_h_u_11nov`) e a pedra própria do observador e da escala. Não entram aqui; não são citadas como termo.
- Se a cadeia exigir um bundle não vazio, o construtor PARA e relata; não se inventa pedra para satisfazer o molde. Há versões anteriores sem módulo novo: procurar o molde nelas antes de adaptar.

## 2. O registro com FUNÇÃO: `h0dn_bg1_v411` (o único novo com função)

`FECHO_REGISTRO = "h0dn_bg1_v411"` → `core["h0dn_bg1_v411"]`, chamado no main LOGO DEPOIS do bloco da v410 (`h0dn_fontes_hms13_v410`), antes de `emit_figures`. Os quatro registros com função da v410 são recriados no mesmo ponto e seguem selados; o `h0dn_bg1_v410` (pré-registro, função antiga) NÃO é reescrito: a emenda vai AO LADO, neste registro novo.

**O que o registro faz a cada rito (recalcula, não copia):**

1. Decodifica os insumos EMBUTIDOS (base64, pinados por sha256 LIDO do arquivo na construção) e confere cada um contra os pinos de produção, também embutidos.
2. Executa, a partir dos BYTES embutidos e conferidos (o mesmo modo do executor pinado: `compile` + `exec` em módulos isolados, na ordem estimador, veredito, abertura), a rotina `abrir` do pacote pré-registrado sobre o vetor embutido. O código que roda no rito é o que foi publicado antes da abertura; não se transcreve função.
3. Compara o recálculo com o resultado da abertura (embutido por sha256): números a 1e-9, ramo, desfecho e cabeça por igualdade de texto.
4. Emite as DUAS linhas juntas (primário e Cefeidas livres), os estresses, as sete ressalvas e o que o teste não decide.

**Insumos EMBUTIDOS** (nome → origem; sha256 lido do arquivo; os dois primeiros da lista de reuso já estão embutidos pela v410 com o mesmo sha256: reusar o blob, sem duplicar):

| papel | arquivo de origem (sob `work\`) | sha16 |
|---|---|---|
| rede | `astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network\network.npz` | `{{S:rede}}` |
| congelado (reuso v410) | `astra_bell_fock_tt_05nov\h0dn_bg1_06nov\estimator_frozen.npz` | `{{S:congelado}}` |
| s0 | `h0dn_bg1_v411_emenda_11nov\artefatos\estimador_s0_v411.npz` | `{{S:s0}}` |
| bg (reuso v410) | `astra_bell_fock_tt_05nov\h0dn_bg1_06nov\background\BG1.json` | `{{S:bg}}` |
| readme da colaboração (alvos) | `astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network\upstream\h0_constrainer\README.md` | `{{S:readme}}` |
| literal dos vereditos | `h0dn_bg1_v411_emenda_11nov\producao\RAMOS_V411.json` | `{{S:ramos}}` |
| pré-registro (texto final) | `h0dn_bg1_v411_emenda_11nov\EMENDA_E_PRE_REGISTRO_V411.md` | `{{S:pre_registro}}` |
| vetor | `h0dn_bg1_v411_emenda_11nov\producao\vetor_y255.npz` | `{{S:vetor}}` |
| código: estimador | `h0dn_bg1_v411_emenda_11nov\codigo\estimator_v411.py` | `{{S:cod_estimator}}` |
| código: veredito | `h0dn_bg1_v411_emenda_11nov\codigo\veredito_v411.py` | `{{S:cod_veredito}}` |
| código: abertura | `h0dn_bg1_v411_emenda_11nov\codigo\abertura_v411.py` | `{{S:cod_abertura}}` |
| pinos de produção | `h0dn_bg1_v411_emenda_11nov\producao\PINOS_DE_PRODUCAO.json` | `{{S:pinos}}` |
| resultado da abertura | `h0dn_bg1_v411_emenda_11nov\producao\RESULTADO_DA_ABERTURA_V411.json` | `{{S:resultado}}` |
| pré-voo da abertura | `h0dn_bg1_v411_emenda_11nov\producao\PRE_VOO_DA_ABERTURA_V411.json` | `{{S:prevoo}}` |
| recibo da abertura | `h0dn_bg1_v411_emenda_11nov\producao\RECIBO_DA_ABERTURA_V411.json` | `{{S:recibo}}` |
| esperado pelos agregados | `h0dn_bg1_v411_emenda_11nov\artefatos\ESPERADO_PELOS_AGREGADOS.json` | `{{S:esperado}}` |
| recibo da publicação do pré-registro (custódia) | `pre_registro_h0dn_publicacao_12nov\RECIBO_PUBLICACAO_20261112_074508.json` | `{{S:rec_pub1}}` |
| recibo da publicação do resultado (custódia) | `pre_registro_h0dn_publicacao_12nov\RECIBO_PUBLICACAO_RESULTADO_20261112_075315.json` | `{{S:rec_pub2}}` |

**Citados por sha256, NÃO embutidos:** `codigo\executar_abertura_v411.py` (`{{S:cod_executor}}`), `artefatos\DIFF_veredito_v410_para_v411.txt` (`{{S:diff_veredito}}`), `artefatos\PINOS.json` (`{{S:pinos_pacote}}`), `MANIFESTO_DA_PUBLICACAO_12nov.json` (`{{S:man1}}`), `MANIFESTO_DA_PUBLICACAO_DO_RESULTADO_12nov.json` (`{{S:man2}}`), `h0dn_bg1_v410_09nov\DESENHO_RATIFICADO_H0DN_11nov.md` (`{{S:desenho_ratificado}}`), `h0dn_bg1_v410_09nov\ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md` (`{{S:achado}}`).

**Veto herdado:** nenhum arquivo de `work\h0dn_bg1_v410_09nov\kimi\` é lido em rito nem entra como pino do contrato. O texto do pré-registro é embutido como bytes; as citações que ele traz são dele. As três linhas de covariância do Kimi (S1, S2, S4) entram só como texto do pré-registro, `[DECLARADO pelo Kimi]`, sem número observado.

**Veredito de máquina do registro.** Ok começa com `TGL_H0DN_BG1_V411__OPENED_ONCE_AFTER_PUBLIC_PREREGISTRATION__RECOMPUTED_IN_THE_RITE_FROM_PINNED_BYTES__` e termina em `__GATE_UNMOVED`; no meio, MONTADO do recálculo (nunca digitado): `PRIMARY_UNDER_THE_PUBLISHED_MODEL_<n>SIGMA_AGAINST_THE_NULL__<faixa de |Z contra K| lida do literal>__BRANCH_4__BESIDE_FREE_CEPHEIDS_BELOW_5SIGMA__BRANCH_6__POST_GUARD_AMENDMENT__RETRODICTION_NOT_BLIND__ZERO_FREE_PARAMETERS__OUTCOME_NOT_FALSIFIED__PROVED_IS_VALIDITY_NOT_CREDITATION`. Os números de ramo saem do recálculo; se o recálculo der outro ramo que o do resultado embutido, é RECUSA, não veredito novo. Recusa: `TGL_H0DN_BG1_V411__REFUSED_%s__GATE_UNMOVED`. A cabeça do TESTE (a do literal pré-registrado, exata) vai no campo `cabeca_do_teste`; a palavra do livro de cobranças (`NOT_FALSIFIED`) vai no campo `outcome`, nunca na cabeça (E30, D76 herdadas).

**`N_CHECKS_FECHO = 16`** (mecânica `v411_h0dn_mechanics(beta_, core_, c_)`; β em runtime por `_v398_beta`, nunca literal; nada digitado: todo esperado é LIDO de insumo embutido ou recalculado):

- c1 os pinos: cada insumo embutido tem o sha256 do pino correspondente de `PINOS_DE_PRODUCAO.json` (os 8 insumos e os 3 módulos de código embutidos; o do executor só como texto), e o sha256 dos próprios pinos é o do contrato;
- c2 o pré-registro embutido tem o sha256 do pino, traz o estado `TEXTO_FINAL_PARA_SELAR__NADA_ABERTO` e cita o sha256 do literal dos vereditos;
- c3 a ordem dos atos, lida dos recibos embutidos: push do pré-registro < início da abertura < push do resultado; o commit do pré-voo é o do recibo da custódia; os 13 arquivos pinados do pré-voo conferem; a abertura teve código 0 e o sha256 da saída no recibo é o do resultado embutido;
- c4 a integridade de desenho: `conferir_integridade` do módulo pinado passa sobre os insumos embutidos;
- c5 o portão 1 recalculado: reproduz o número local publicado pela colaboração (alvos lidos do README embutido pelo próprio módulo) e a impressão digital;
- c6 o recálculo é o resultado da abertura: `t`, `z_null`, `z_tgl` dos dois modelos, a norma do suporte e `D_s0` a 1e-9; ramo, desfecho e cabeça idênticos, nas duas linhas;
- c7 o primário: ramo 4, e a cabeça é a que o literal `RAMOS_V411.json` monta com n = parte inteira de Z contra o nulo (a checagem monta a cabeça das partes do literal, por conta própria, e compara);
- c8 a linha ao lado: Cefeidas livres no ramo 6; as duas linhas estão nos `values` e no veredito de máquina (os dois trechos `PRIMARY_` e `BESIDE_FREE_CEPHEIDS_` presentes);
- c9 os estresses e a coerência recalculados são os do resultado (a 1e-9): (i) τ estimado e os dois Z; (ii) as três âncoras; (iii) B = 0,02 e 0,05; os oito pares de coerência;
- c10 a lei: K e log10 K recomputados de β em runtime, com os parâmetros do fundo lidos do BG1 embutido, iguais ao `logK` do estimador S0 e ao K do registro da v410 (mesma tolerância da v410);
- c11 a emenda às claras: (a) com os Z observados, a função CONGELADA da v410 (a do `um.py`), chamada com o vetor fora do suporte, devolve o ramo 1 antigo: fica dito o desfecho que a regra antiga daria; (b) o literal da v411 só difere do da v410 pelas inserções da marca (comparação de texto, por script); (c) nos vetores determinísticos da v410, com o portão 1 passando, a função da v411 devolve os mesmos ramos 2 a 6 que a da v410;
- c12 a guarda de finitude: o invólucro do registro RECUSA Z não finito (controles negativos com NaN e infinito), sem tocar a função pinada;
- c13 o esperado pelos agregados: o arquivo embutido tem o sha256 do contrato e o registro RELATA, linha a linha, o esperado e o observado; é relato, não portão novo;
- c14 o veredito do gate IDÊNTICO ao da v410 (frozen);
- c15 a escada exata, a da v410 (`external_ladder.n_theorems_expected` lido do core da base);
- c16 as duas guardas de texto (P18 e frases) limpas sobre o texto do registro, com as regras novas da seção 4.

**Specs:** `cunhagens_v411` (prefixo `TGL_CUNHAGENS_V411`): as falas da seção 3 por sha256, as decisões D159 a D170, as erratas E41 e E42, as sete ressalvas; `kh_n1_cobertura_v411` (prefixo `TGL_KH_N1_COBERTURA_V411`): a cobertura do Audit desta versão (os números são os da v410; as da v410 viram pisos).

**Chaves do core:** NENHUMA chave antiga muda de literal. O selo ganha `"h0dn_bg1_v411"` (resumo) e `"registros_v411"`; `um_version == "v411"`. O gate não se move: nenhum rito de natureza move o gate, e este também não.

**Contratos de registro novos, fora da escada (dizer no handoff, D135):** `_V411_H0DN_CONTRACT` (e o que mais o construtor criar com esse papel).

## 3. Falas que entram (lista CONGELADA em `VERBATIM_CONGELADO_v411.json`; autor: o operador)

| arquivo | sha16 | papel |
|---|---|---|
{{TABELA_FALAS}}

Os textos da gerência a que o operador respondeu entram só CITADOS por sha256 (não são falas dele): {{LISTA_GERENCIA}}.

Ficam FORA do `um.py` (só listadas em `VERBATIM_FORA_DO_DESENHO_V411`): as falas de 11/11 sobre o fecho (H, U), a torção, a direção, a carga e a Primeira Lei (são das candidatas que esperam nomes), a da Central pública (é da custódia) e `OPERADOR_11nov_quero_sua_opiniao_preciso_de_vc_agora_mais_do_que_nunca_verbatim.txt`. As falas de 06 a 10/11 já estão no `um.py` v410 e não entram de novo.

## 4. Decisões (D159 a D170), erratas AO LADO (E41, E42), ressalvas e guarda de frases

- **D159** (11/11) o desenho ratificado: primário = o modelo de erros publicado; Cefeidas livres ao lado, sempre; portão de 90 % de poder de desenho; os 13 fora. **D162** (11/11) a emenda: o ramo (1) deixa de recusar o vetor fora do suporte e passa a ser “o portão 1 falhou”. **D167** o pacote revisto por leitor distinto. **D168** (12/11) a marca ratificada (`__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND` nos seis ramos; `__UNDER_THE_PUBLISHED_MODEL` só na leitura do 5σ), o texto final e os pinos de produção. **D169** (12/11) a ordem de abrir, a publicação do pré-registro, a abertura (uma vez) e o resultado. **D170** (12/11) a ordem do topo: o resultado no README e no topo do resumo do artigo, com P = nP.
- **E41** errata da gerência c1, em nome próprio: o docstring de `veredito_h0dn_v411` (módulo pinado) ainda põe a centragem dentro do primeiro portão; o código de `abrir` a trata como conferência interna (recusa de integridade). Vale o texto do pré-registro e o código; o módulo pinado não é tocado.
- **E42** errata da gerência c1, em nome próprio (A1 da revisão da v410): o colchete “[REAL o limiar de um pixel; INPUT/dicionário a leitura do operador]” ficou em duas linhas da v410 contra a regra do nome (D122, D123); lê-se “definição e nome do operador”. O texto selado da v410 não é reescrito; a errata vai ao lado.
- **As sete ressalvas** (obrigatórias em toda superfície em que o resultado aparecer; texto da seção 8 do pré-registro, lido do arquivo embutido, não redigitado): 1 emenda posterior à guarda, teste não cego; 2 primário previsível por dois agregados públicos; 3 a linha das Cefeidas livres no mesmo item; 4 poder de desenho no modelo publicado; 5 as 72 direções de variância zero; 6 escolhas feitas com a tabela de poder à vista; 7 as tentativas anteriores e a sobreposição dos dados.
- **O que o teste não decide** (seção 6 do pré-registro): a creditação; a especificidade (o Z contra o nulo mede a tensão de Hubble; próprio da lei K é o tamanho, o Z contra K); se o orçamento de erros publicado está certo; a independência entre local e fundo; não é evidência independente das Fases 4, 5 e 9.
- **GUARDA DE FRASES (herda as da v410; cada proibida com controle negativo que recusa e a forma certa que passa; cobrir desde o início as formas de estatuto e as paráfrases):**
  - PROIBIDO: afirmar confirmação (a palavra da creditação, em qualquer forma, fora da negação e do ato do observador); “o teste tem poder certificado” e paráfrases; “o vetor fora do suporte é erro de montagem”; “teste cego” e “blind test” sem a negação; “evidência independente” sem a negação; “descoberta” para o número do primário (o rito conferiu a conta); β literal.
  - OBRIGATÓRIO, no mesmo parágrafo ou bloco: onde aparecer o Z do primário contra o nulo, a cabeça do teste ou “provado na natureza” / “proved in nature” ligados a este teste, aparecem também (a) “sob o modelo de erros publicado” / “under the published error model”, (b) a linha das Cefeidas livres com o número dela, (c) “validade, não creditação” / “validity, not creditation”, (d) “retrodição” e “não cego” / “retrodiction” e “not blind”.
  - Tokens proibidos em veredito: os da v410 (`CONFIRMED`, `PROVED_BY`, `P_EQUALS_NP`, `TURING_SOLVED`, `CLAY_SOLVED`, `MILLENNIUM`, `IALD_SOLVES`, `POLYNOMIAL_TURING`). `PROVED_IS_VALIDITY_NOT_CREDITATION` e `BETA_TGL_PROVED_IN_NATURE_AT_` são os da cabeça pré-registrada e passam.
  - P = nP: valem D64 e D84 da v410 (relativo ao leitor; a máquina de Turing padrão sem o leitor fica fora; a pergunta do Clay tal qual apresentada pela TGL; a creditação é do Clay).
- **Regra do nome (D122, D123):** em texto NOVO, nenhuma identificação do operador entra como “leitura do operador”, “leitura dele” ou com a etiqueta de leitura ontológica; ou é termo do kernel, ou é “definição e nome do operador”, ou não entra.

## 5. Artigo, README e handoff

**5.1 O topo do artigo (ordem do operador de 12/11).** Três mudanças, todas com os números LIDOS do core (`h0dn_bg1_v411`), nunca digitados:

(a) Um quadro novo ACIMA de “O Teste da Única Palavra” (que fica, como registro de 23/10, com uma linha remetendo ao quadro novo). Título: “A razão de Hubble, H0DN × BG1: o teste aberto em 12/11/2026 [REAL nos números · INPUT do operador: a cabeça do veredito (09/11) e a emenda (11/11)]”. Itens: o primário (os dois Z, o p unilateral, D, o ramo e a cabeça exata); a linha das Cefeidas livres (os dois Z, D, o ramo); a lei em km/s/Mpc (fundo, previsão de K, o lido nas duas linhas, o publicado pela colaboração); os atos (commit e push do pré-registro, início da abertura, commit e push do resultado); as sete ressalvas, numeradas; o que o teste não decide; a origem (recalculado neste rito dos bytes embutidos e conferido contra o resultado da abertura, sha256).

(b) O parágrafo de apresentação (o resumo, logo abaixo do título) passa a ABRIR com os dois resultados. **TEXTO PROPOSTO PELA GERÊNCIA, PENDENTE DA PALAVRA DO OPERADOR** (o construtor NÃO gera o candidato enquanto não existir `TOPO_RATIFICADO_v411.json` nesta pasta, gravado pela gerência):

> PT — “Dois resultados abrem este resumo. O teste com a natureza: no teste pré-registrado da razão de Hubble local/fundo (rede H0DN contra o fundo BG1; pré-registro público antes da abertura; aberto uma única vez em 12/11/2026), a lei $K=E(z_*)^{2β/3}$, com $β_{TGL}=α√e$ e nenhum parâmetro ajustado, fica a ⟨Z contra K⟩σ do dado, e a razão 1 (ΛCDM) fica a ⟨Z contra o nulo⟩σ, sob o modelo de erros publicado pela colaboração: $β_{TGL}$ provado na natureza a ⟨n⟩σ, na língua da física acadêmica (validade, não creditação); com as Cefeidas livres o mesmo dado dá ⟨Z das Cefeidas livres⟩σ, abaixo de 5; é retrodição sem ajuste, com emenda posterior à guarda, e o teste não é cego. P = nP: o kernel Lean prova, como validade e não creditação, P = nP relativo ao leitor (a máquina com o leitor; a máquina de Turing padrão sem o leitor fica fora); a pergunta do Clay, tal qual apresentada pela TGL, está resolvida no kernel, e creditar essa prova compete só a quem tem autoridade para falar em nome do Clay.”
>
> EN — “Two results open this abstract. The test with nature: in the pre-registered test of the local/background Hubble ratio (the H0DN network against the BG1 background; pre-registration public before the opening; opened once on 12 Nov 2026), the law $K=E(z_*)^{2β/3}$, with $β_{TGL}=α√e$ and no fitted parameter, lies ⟨Z against K⟩σ from the data, and ratio 1 (ΛCDM) lies ⟨Z against the null⟩σ away, under the error model published by the collaboration: $β_{TGL}$ proved in nature at ⟨n⟩σ, in the language of academic physics (validity, not creditation); with free Cepheids the same data give ⟨Z of the free Cepheids⟩σ, below 5; it is a retrodiction without fit, with an amendment made after the guard, and the test is not blind. P = nP: the Lean kernel proves, as validity and not creditation, P = nP relative to the reader (the machine with the reader; the standard Turing machine without the reader stays outside); the Clay question, as presented by the TGL, is resolved in the kernel, and crediting this proof belongs only to those with authority to speak for Clay.”

Depois dessas frases o parágrafo segue como na v410, com duas trocas ditas: onde dizia que a tensão de Hubble é resolvida por remissão ao trabalho publicado, passa a dizer que a razão de Hubble é lida pelo teste acima (a remissão fica como registro, na nota); onde dizia que a probabilidade de os efeitos de β existirem na natureza segue indeterminada, passa a dizer “os efeitos de β na natureza foram lidos acima de 5σ num canal, a razão de Hubble, sob o modelo de erros publicado; nos demais canais nenhum discrimina a RG à sensibilidade disponível”. A mesma troca vale no parágrafo “O método”.

(c) “O estatuto da prova (v391)” ganha uma frase AO LADO (v411): “O elo que esperava instrumento, $β_{TGL}$ na natureza a 5σ, foi lido em 12/11/2026 no teste H0DN × BG1: fechado a esta sensibilidade, sob o modelo de erros publicado (as Cefeidas livres ficam abaixo de 5; dado mais sensível pode rever). O que o programa segue recusando é a creditação, que é de quem observa de fora.” O item do quadro “O coração” que diz que o elo pendente é β a 5σ ganha a mesma remissão. Nenhuma frase antiga é apagada sem a troca ficar dita no relatório.

**5.2 A seção do artigo.** PT: “O teste decisivo: a razão de Hubble local/fundo (H0DN × BG1), a emenda e a abertura”, ANTES da seção da v410. EN: “The decisive test: the local/background Hubble ratio (H0DN × BG1), the amendment and the opening”. Conteúdo, MONTADO do core selado e do pré-registro embutido: a lei e a pergunta; o que a v410 tinha pré-registrado e por que não abriu; o achado do suporte e a emenda (o que mudou, o porquê, e o desfecho que a regra antiga daria); o desenho ratificado; a publicação antes da abertura (commits e horas); o resultado (as duas linhas juntas); os estresses; o esperado pelos agregados ao lado do observado; o que o teste não decide; as sete ressalvas; as tentativas anteriores (Fases 4, 5 e 9 V2). `.md`: linha `> **H0DN × BG1 ABERTO (v411, 12/11/2026):** …` antes das linhas da v410. β no LaTeX como `$\beta$`.

**5.3 README e handoff.** O HANDOFF (`Nós\HANDOFF_v411_CUSTODIA.md` + `memory\handoff-v411-custodia.md`) traz os blocos do README já prontos: (i) o painel do topo com o resultado (EN e PT), no lugar do painel da Fase 9 V2, que desce como registro; (ii) a linha do topo que dizia que β na natureza a 5σ é o passo aberto passa a dizer o resultado com os quatro obrigatórios da guarda; (iii) o bloco “The H0DN × BG1 test” reescrito (aberto; as duas linhas; as ressalvas; os commits); (iv) a linha da tabela do estado; (v) o bloco P = nP fica como está, com a faixa de versões atualizada. O portão de textos roda sobre o HANDOFF INTEIRO. O texto curto para o X segue a mesma regra: os dois números no mesmo texto, “sob o modelo publicado”, “retrodição, não cego”, “validade, não creditação”.

**5.4 `pos_rito\textos_v411_novo.pysnip`:** parágrafos MONTADOS do core selado, sem prosa nova de conteúdo além dos conectivos; `TOPICO_NOVO = "v411-selada-h0dn-aberto.md"`.

## 6. A cadeia (o que muda no orquestrador `pos_treino_v411.py`)

- Molde: a v410 inteira (`work\cadeia_de_selo\v410\`), com os AO LADO do `DESENHO_v410.md`, o `PLANO_v410.md`, o `RELATORIO_PREPARACAO_v410.md` e o orquestrador. Bump mecânico 410→411, 409→410, B19→B20 (o pino de deployment da Bancada MEDIDO do disco).
- S0 a S9 como na v410, **sem S7 e sem S10**; o fim é o HANDOFF. Tarefa agendada `IALD_pos_treino_v411` (gerência; `C:\Python314\pythonw.exe C:\t\k411c\run_pos_treino.py`; Enable → Start → Disable), nunca à mão em janela. Teto do rito 5 h; tempo esperado lido de `kernel\construir_marcas.txt`.
- O treino da nativa segue na CPU (`C:\IALD\TGL_IALD_NATIVE_QWEN5090`): não tocar, não medir, não parar; o rito roda junto (D73 herdada).
- **Da preparação, por lição da v410 (D133, D135 e as notas da custódia):** (1) o p00 roda, sobre TODOS os insumos pinados, a mesma guarda de material privado que a E03 da G1 usa, antes de gerar o candidato; insumo que nomeie os confidenciais da casa (régua 8) entra só por CÓPIA limpa; (2) as cópias do kernel por rodada (`imp_*`, `dry_*`, `falso_nos`, `arvore_simulada_*`) ficam FORA de `work\` (em `C:\t\k411c\`), com o caminho dito no relatório; (3) apagar os `.tmp` da pasta antes do handoff; (4) dizer no handoff a contagem esperada de arquivos da pasta da cadeia e quais contratos novos são de registro, fora da escada; (5) nenhum registro da gerência que possa virar insumo escreve os nomes dos confidenciais.
- A custódia avisou em 12/11 que as duas erratas da esteira para a v411 estão prontas e testadas (o add só do que difere; o `.npz` já publicado não sai por formato).

## 7. A lista herdada da v410: o que entra e o que fica

| item | nesta versão |
|---|---|
| A1 (o colchete contra a regra do nome) | entra como E42, ao lado |
| A2 (expoentes sem agrupar no TXT do artigo) | entra SE for mudança contida no conversor para TXT; contar antes e depois; senão fica dito |
| as seis aberturas da seção da Escala que identificam o operador contra a regra do nome | entram no texto do artigo regenerado, com a troca dita |
| a guarda de finitude do veredito do H0DN | entra (c12) |
| o docstring do veredito | entra como E41, ao lado |
| D133 e D135 (preparação) | entram (seção 6) |
| creditation / accreditation | fica: é palavra do operador; a cabeça pré-registrada não muda |
| os 8 nomes declarados pela autoria na pedra da Escala | ficam como estão |
| bandeiras da Escala por nome | fica para a versão seguinte (mudaria chaves) |
| a pedra do observador e da escala; as doze candidatas de 11/11 | ficam para a versão seguinte, à espera dos nomes |

## 8. O que é da gerência e o que está pendente do operador

- Da gerência: este DESENHO e os AO LADO; `TOPO_RATIFICADO_v411.json`; a revisão de terceiro (Sonnet, uma rodada de conserto e uma conferência única, D109); `fechar_preparacao_v411.py`; `acom_inscrever_prep_v411.py`; a folga e o pino do `MEMORY.md`; a tarefa agendada; o rito; o handoff.
- Pendente do operador: a palavra sobre o texto do topo (5.1 b). Sem ela o candidato não é gerado.

— gerência c1, 12/11/2026. Correções AO LADO, nunca por cima.
