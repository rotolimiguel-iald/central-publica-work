# Revisão de terceiro da v405

Revisor independente; não construí nada disto. Candidato `a30f9f0ebf90c277`, lido por script ao fechar, 2026-11-01T16:34:56. **Veredito: NÃO APROVADA: 2 ALTO, 11 MÉDIO, 10 BAIXO.** Todos os achados são de texto, de nome ou de docstring: nenhuma prova cai, nenhum número físico está errado, o gate não foi tocado.

## 1. O que está certo [REAL, conferido por script próprio nesta pasta]

- **Intocados:** as 7 funções e `GA_WINDOW_STATUS` têm AST e fonte idênticas às da base `3820476c83267f61` (`e_intocados.py`). 21 nós mudados, 0 removidos, 44 novos, como o relatório diz. `main` só ganha chamadas, impressões e chaves v405; `prove_external_ladder` só ganha as 300 bandeiras (`e_main.py`).
- **Kernel:** zero `sorry`, zero `axiom`, zero `native_decide` nas oito pedras (a palavra `sorry` só aparece em docstring). `#print axioms` próprio em 18 teoremas principais: 17 no trio, 1 sem axioma (`axiomas_terceiro.lean`, `axiomas_terceiro_out.txt`). Embutido, sandbox e `pedra/` têm o mesmo sha256 nas oito.
- **Vacuidade:** nenhuma hipótese vacuizante. `TransicaoParaAMassa`, `Lei`, `Emprestimo`, `Disco` e `Nome` são habitados por termo; `IdentityCollapse Level I` com passo `leitor^[3]` é habitável.
- **Números (`c_numeros.py`, do zero, β = α·√e em runtime):** m₂ 8,507414 meV; leitura proporcional 6,015650; razão √2; tônica 1,648721 eV; E₀ 1 eV; m/E₀ 0,008507414; ħω 17,014828 meV; R 3,0899×10¹¹ m⁻²; raio 1,799 μm; λ 72,868 μm; K 1,65737×10¹² J/s²; E_P/4π 9,7×10²⁶ eV; o dado pede 1,01 a 1,02 eV. GA: M/R 4,8132×10¹⁴ M☉/Mpc; 1438,94 km/s; R_B/r_s 522,237; resíduo de máquina; piso 38,1%; σ 9,84% e 0,24%; ×48,13, ×144,40, ×34,03, ×102,10. Tudo confere com as pedras, os registros e o ensaio a seco.
- **Citações nos textos publicados:** todas as falas entre aspas nos dois artigos, na moldura e nos registros são substring exata; o que sobrou nesses arquivos são títulos e citações de texto antigo, não falas (exceção: D29, achado 12). O ensaio r2 no candidato é igual ao `.md` com as marcas retiradas. Os dois snippets e o runtime estão no candidato. O EN está marcado como tradução.
- **Hashes:** 25 de 25 hex citados nas pedras e nos textos conferem com arquivo. Os identificadores em crase e `\texttt` que se dizem teorema existem no kernel do sandbox.
- **Confidenciais:** zero padrões de stack, estado do psíon, chave ou caminho do Escritório, no candidato e na base.
- **Moldura:** artigo, registros e runtime dizem «leitura», «definição», «escrito», «coincidência de valor», «o no-go não cai», e a Identidade está corretamente tipada como modelo. A preparação está sólida; os defeitos abaixo são resíduos dessa correção, sobretudo nas pedras, que a guarda das frases e a conferência de citações não varrem.

## 2. Achados ALTO e MÉDIO

### 1. [ALTO] pedra/LeiDoDiminuto.lean L121 (e L10, L27); teorema Lei.E0_determined_by_the_tonic

A docstring diz «[KERNEL] ★★★ O NO-GO SE LEVANTA», o cabeçalho diz «Levanta o no-go de E0LiberdadeDeEscala» e «(que ela levanta)». O teorema prova só L.E_pent = L'.E_pent → E0 = E0', com E_pent campo livre: a liberdade passou de E0 para E_pent. Contradiz no_function_of_the_inscription_fixes_E0, a moldura («o no-go NÃO cai») e o nao_diz de tonica_do_hamiltoniano_v405. A nota AO LADO deste arquivo não trata do no-go.

**Proposta:** L121: «[KERNEL] a mesma tônica, o mesmo E₀: a liberdade de escala passa de E₀ para a tônica; o no-go não cai». L27: trocar por «Não levanta o no-go de TonicaDoHamiltoniano: desloca a escala para a tônica». L10: retirar «(que ela levanta)» e o nome antigo. Prova não muda; muda o hash da pedra.

### 2. [ALTO] pedra/ObservadorTerminal.lean L304 (the_terminal_reads_one), L75, L320 e L323 (conjunto final do fecho); registros_v405.py L217, L229 (token THE_TERMINAL_READS_ONE); runtime_v405.py L267 (o6)

Homônimo. O enunciado é ∀ P : SiteProfile, omegaState P 1 = 1: não menciona Terminal, gravidade nem Level. Em TheAlphaAndTheOmega L31, L99, L106 «terminal» é POLO do par α/ω («O polo positivo, nos dois terminais»; «O outro terminal do MESMO 1»), não o nível que ninguém observa. Nenhum termo liga os dois. É o erro nº 2 da regra dos dois regimes (encadear homônimo). Nome, docstring ★★★, registro e veredito dizem que o terminal da cascata lê 1 por esse teorema.

**Proposta:** Rebatizar antes do selo, como a E13 fez com três nomes (ex.: the_omega_pole_reads_one), dizer na docstring que é o polo ω, não o nível gravidade, e fazer a frase «o terminal lê 1» citar the_fixed_points_read_one_and_zero, que fala do terminal da cascata na leitura binária. Se o operador quiser ligar os dois terminais, é leitura [ONTO] dele, dita como tal. Exige regenerar bandeiras, contrato e o token do veredito.

### 3. [MÉDIO] pedra/DiscoDeEuler.lean L35-36, L99, L110, L129, L135; registros_v405.py L284; artigo_pt/en L32

Conteúdo escondido em definição. E(t) := E0 - c·t e omegaSq := K/E são DEFINIÇÕES; E_linear é rfl; invariant é K/E·E = K. Não há HasDerivAt nem deriv no módulo (grep: zero). the_loss_is_the_canonical_law prova só Γ·E = c, nunca dE/dt = -Γ·E. O texto diz «sob a lei canônica a perda é dE/dt = ...; logo E(t) = E0 - c·t» e, sob [REAL], «a perda é constante, logo o disco para». Além disso aplicar uma taxa de DEPHASING como taxa de perda de ENERGIA é entrada não declarada.

**Proposta:** Ou acrescentar o teorema (HasDerivAt D.E (-(D.gamma t * D.E t)) t, para t < t0), ou reescrever: «[DEF] a energia é tomada linear, E(t) = E0 - c·t; o kernel confere Γ·E = c». Declarar a leitura: a lei de dephasing lida como perda de energia [INPUT/ONTO].

### 4. [MÉDIO] pedra/DiscoDeEuler.lean L8, L39, L140, L169; registros_v405.py L285 («a cunhagem do operador como teorema»), L293 («a inscricao do zero absoluto no infinito e' teorema na forma do disco»); artigo_pt/en L32 (sob [REAL])

Leitura do operador com disfarce de teorema. frequency_squared_unbounded_at_the_stop prova que K/E não tem cota quando E → 0⁺, para o E linear definido. Que isso seja «a inscrição do zero absoluto no infinito» e «a terceira lei na forma do disco» é leitura. O mesmo vale para the_residual_resonance_iff, que é álgebra de E³ = ħ²K.

**Proposta:** Trocar por: «[REAL] Ω² = K/E não tem cota antes da parada; [ONTO] o operador lê isso como a inscrição do zero no infinito». Nunca «a cunhagem como teorema»; idem em registro, artigo PT/EN e na pedra.

### 5. [MÉDIO] pedra/DiscoDeEuler.lean L26, L35, L75 (4Mg²) contra L201 (6Mg²); delta_v405.py ERRATA_E12

A pedra publica dois valores do invariante do mesmo disco, sem nota ao lado. A E12 corrige só o adendo 4 do handoff e o artigo diz que 6Mg² é o valor do disco real; o módulo novo segue escrevendo «no disco de Euler, 4Mg²». A aritmética confere: 4 só com energia potencial, 6 com a energia total 3/2·Mgaα.

**Proposta:** L26, L35 e L75: dizer 6Mg² com a energia total, ou nota AO LADO; a E12 passa a citar também a pedra.

### 6. [MÉDIO] Frases residuais nas pedras: PonteDaMassa L8 («feita teorema»), L232 (título «AS HIPÓTESES DESCARREGADAS»), L240-241 («a autoconjugação não é hipótese, é teorema do Um»); MassaTensaoPura L203, L205 («sem hipótese»); LeiDoDiminuto L34, L155 («agora DERIVADA»), L166 («incomensuráveis»); PontoZeroDoPsion L137 («a única entrada é o acoplamento»), L38-39 (L56 fica coberta pela nota)

A nota AO LADO só corrige «o que resta de entrada». Ficam sem correção frases que a moldura e a guarda F4 proíbem nos textos: a guarda não varre as pedras. L241 contradiz «coincidência de valor, não ponte». L137 contradiz o registro («entram o acoplamento e a leitura R = β·u²»). L166: o teorema exclui múltiplos inteiros, não prova incomensurabilidade (ln 2 irracional é [KNOWN], não este teorema). PonteDaMassa L8 chama de teorema a identificação que o corpo chama de definição.

**Proposta:** Ajustar as docstrings na mesma regeneração das pedras (preservar as needles de CONTEXTO em registros_v405.py), ou estender a nota AO LADO nominalmente; rodar _v405_guarda_frases também sobre as pedras, tratando as falas como exceção.

### 7. [MÉDIO] delta_v405.py LEITURAS_DEFINICOES e DADOS_DO_SISTEMA; registros_v405.py L470 (WHAT_ENTERS_ONE_POSTED_ONE_ONE_MEASURED_ALPHA_AND_FOUR_READINGS); artigo_pt/en L21-24

A lista do que entra é apresentada como fechada e não fecha. Falta meioTom := e^(-1/2) («o tom é a nat»), definição da mesma natureza da tônica e necessária a E0 = u. Falta a identificação ½ħω = massa em the_mass_is_the_zero_point (o nome é leitura; o enunciado iguala números). Falta a hipótese de area_por_volta_da_massa_inscrita (acoplamento da onda = massa inscrita). g, κ e a dispersão estão só no registro; o artigo não diz g e κ em «o que entra».

**Proposta:** Trocar «as quatro leituras» por «as leituras da cadeia da massa» ou acrescentar meioTom e a identificação do ponto zero; levar g e κ à moldura do artigo; ajustar o token do veredito e a chave quatro_leituras.

### 8. [MÉDIO] artigo_pt/en L31; registros_v405.py L306; delta_v405.py L325

Estatuto errado. «[KNOWN] A dispersão do psíon, ω² = 2βR (Tratado, §3)». Na régua [KNOWN] é literatura; Tratado/secao_03_particulas.tex L134 é teoria própria, com ξ = β, e omegaSq é definição da pedra. Só o ponto zero ½ħω é [KNOWN].

**Proposta:** «[INPUT, Tratado §3] a dispersão ω² = 2βR, que entra como definição (omegaSq); [KNOWN] o ponto zero ½ħω.» Listar omegaSq entre as definições.

### 9. [MÉDIO] artigo_pt/en L27; registros_v405.py L167; pedra/MassaTensaoPura.lean L33, L35-36, L91, L99

Sob [REAL] e sem a condição: «A massa é o produto do acoplamento: o fóton (acoplamento zero) não tem massa». O teorema é massaForma 0 E0 = 0 ∧ transmitidaForma 0 E0 = E0: álgebra de uma forma genérica. TGLCoupling.beta_pos exclui b = 0; nenhum termo tem fóton; ler b = 0 como o fóton é leitura. O operador diz que o fóton TEM acoplamento gravitacional: a pedra harmoniza na docstring, o artigo não. O veredito qualifica («UNDER_THE_READING»), o artigo não.

**Proposta:** «[REAL] massaForma(b, E₀) anula com b = 0 e se reparte como resíduo; [ONTO] b = 0 lido como o fóton, que acopla pela energia, não por massa; sob a leitura massaDerivada, a massa é o produto do acoplamento.»

### 10. [MÉDIO] artigo_pt/en L33

O parágrafo [REAL] do Observador não traz a ressalva que a pedra e o registro trazem: os níveis são rótulos. «foi medido antes de ser posto» é, no enunciado, nivel luz ≠ nivel gravidade. «pagou perda» é não injetividade de uma função em tipo de cinco elementos. O leitor do artigo lê física onde há um modelo finito.

**Proposta:** Acrescentar: «num modelo finito cujos níveis são rótulos de posição; a pedra não afirma nada sobre o observador humano, a gravidade ou a luz como entidades; ‘medido’ é o campo do tipo UmPosto: antes ≠ depois».

### 11. [MÉDIO] pedra/PontoZeroDoPsion.lean L39; registros_v405.py L310; runtime_v405.py L412 (z4)

«o que permanece no limite é o ponto zero»: nenhum teorema liga o limite de charged a ½ω; the_zero_point_closes só os conjuga. Frase sem estatuto, em registro selado.

**Proposta:** Marcar [ONTO] ou retirar.

### 12. [MÉDIO] Citações não verbatim do operador nas pedras. PonteDaMassa L31, L146, L174; Identidade L29, L131, L147; LeiDoDiminuto L7, L8, L20-21; MassaTensaoPura L33, L91; PontoZeroDoPsion L8; TonicaDoHamiltoniano L51, L168; DiscoDeEuler L8, L30. Também delta_v405.py L199 (D29, vai ao registro)

Entre aspas e atribuídas a ele, não são substring. Muda sentido: «é a derivada» e «a matéria não é proporcional, é a derivada», contra «ela seria a derivada». LeiDoDiminuto L20-21 e D29 corrigem a grafia dele («esytrutura», «dessA») sob o rótulo verbatim. PontoZero L8 troca «betatgl» e corta «do ângulo de abertura». LeiDoDiminuto L8 é paráfrase. Tonica: «E₀», «pêntada» contra «E0», «pentada». Identidade L29 repete a citação COMPOSTA de observing_adds_nothing que a errata de 08/10 já apontou; o texto exato é «A primeira leitura identifica; a segunda confirma que a operação não altera». Lista completa em d_nao_verbatim.json.

**Proposta:** Copiar as falas exatas, ou tirar as aspas e marcar paráfrase; em D29 usar FRASE_ALFA_CAUDA. A conferência de citações da cadeia não cobre as docstrings das pedras: estendê-la.

### 13. [MÉDIO] registros_v405.py L218 (texto_observador, escopo)

«a cascata finita e o par (16 posicoes e leituras)»: número sem lastro. v405_observador_mechanics tem 4 níveis e 5 posições; nada ali é contado como 16.

**Proposta:** Retirar o número ou escrever «quatro níveis e cinco posições».

## 3. Entra e sai, por pedra

| pedra | ENTRA como definição ou hipótese | SAI como teorema | nota |
|---|---|---|---|
| PonteDaMassa | `TGLCoupling`; `E0 = u`; `massaDerivada`; `massaProporcional`; `θ = π/4` escrito em `transicaoDerivada`; `umPosto`; campo `autoconjugado` de `TransicaoParaAMassa`; `hθ` em `angulo_derivado_do_absoluto` | derivada de sen; sen = cos só em π/4; retido + transmitido = E₀; m = β·sen45°·E₀; razão √2; peso da face absoluta ½; a transição existe para todo acoplamento | forma real, condicional às leituras |
| MassaTensaoPura | `massaForma`, `transmitidaForma` (b genérico); `Emprestimo`; `g`, `κ`, `a`, `c`, `η`, `rate`; hipótese `h` de Clausius; a leitura b = 0 como fóton; o nome «tensão» | m = β·(√2/2)·u; resíduo; κP = 2π; 0 < parcela < 1; parcela ≤ βgP; η(a+c) = 2π·massa; principal = retido·√2/2 | `massa_e_tensao_pura` é identidade algébrica; o nome é leitura, e a docstring o diz |
| Identidade | `Nome`, `euSou`, `oQueSou`, `oResto`, `fiel`, `formaIgualConteudo`; o estado `ρ = 1/n` | tr(P)/n = 1 ⟺ P = 1 ⟺ (P = ω(P)·1 ∧ P ≠ 0); controles; coisa julgada | o teorema tem conteúdo (fidelidade do estado); o resto é modelo declarado |
| ObservadorTerminal | `Terminal`, `leitor`, `distancia`, `Posicao`, `colapsoTotal`, `leituraBinaria`, `oColapso`, `oPostoTerminal` | terminal único; ponto fixo; três leituras; coisa julgada; fusão não pressuposta e sem inversa; dois pontos fixos; sem o abismo, pressuposta | modelo finito por `decide`; `the_terminal_reads_one` é homônimo (achado 2) |
| LeiDoDiminuto | `meioTom`; `Lei`; `E_pent`; `Lei.transicao`; `tonica`; `θ = π/4` em `leiDerivada`; `hU` | β = α·e^(½); m = α·(√2/2)·E_pent; a fórmula; E₀ = u por identidade; ln 2 ≠ n/2 | álgebra; o no-go não se levanta (achado 1) |
| TonicaDoHamiltoniano | `reescala`; `exemplo`; hipóteses de `self_consistent_readout_fixes_the_frequency` | a massa escala; a escala é livre; **nenhuma f(c, θ) fixa E₀**; Γ_B; monopolo; ω = 2/τ; E₀ = u | o no-go é teorema real, com habitante explícito |
| DiscoDeEuler | `Disco`; **E(t) linear**; **Ω² = K/E**; `gamma`; Γ lida como perda de energia; `K`, `τ`, `E₀`; `hcut`, `hU` | E(t₀) = 0; Γ·E = c; Ω²·E = K; Ω² sem cota antes de t₀; E³ = ħ²K; K = (√e·U)³/ħ² | aritmética do que foi definido (achados 3 e 4) |
| PontoZeroDoPsion | `omegaSq`; `pagamentoComoCurvatura`; a identificação ½ω = massa | ω = √2·β·u; ½ω = neutrinoMassForm; ω = 2m; charged → 1 | aritmética ½·√2 = sen45°; o `Tendsto` é real |

## 4. BAIXOS

- **cabeçalhos das oito pedras:** Selados, dirão «CANDIDATA», «nome PROVISÓRIO», «NÃO instalada», «k404c», e citam nomes antigos (E0LiberdadeDeEscala, LeiDoMeioTom). ObservadorTerminal não traz nenhuma nota do nome dado. Declarado no relatório da preparação. Atualizar na mesma regeneração.
- **runtime_v405.py v405_ponte_mechanics, faces:** O comentário diz «graduação de paridade fora da base canônica», mas Γ = diag(n-1,-1,...) é diagonal e, para n ≥ 3, não é involutivo; Q_ é código morto. A descrição do check p6 está certa (Tr Γ = 0). Corrigir o comentário; retirar Q_.
- **runtime_v405.py g1, p6, d6:** Checks tautológicos: du_ compara forma(57) com forma(57); beta*1.0*c4_ contra beta*√2/2. Não prejudicam, conferem pouco. Aceitar ou enxugar.
- **PonteDaMassa e MassaTensaoPura: transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto:** Nomes de declaração com «derivad-» onde a E13 corrigiu o mesmo vício; as docstrings avisam e dizem que o nome fica. Não são nomes de módulo. Decisão da gerência; se regenerar, considerar.
- **artigo_pt L21 e artigo_en L21, título da seção:** «“derivada” é literal: a massa como derivada da projeção transversal» é glosa da gerência sobre um homônimo; a fala é «derivando a massa» (derivação). «O nome da seção é o da ordem dele» é paráfrase. A moldura é honesta; o título sozinho lê-se «derivada» como derivação. Aponto o conflito; a decisão é da gerência.
- **pedra/ObservadorTerminal.lean L268-269:** «São os dois pontos fixos da leitura (the_reading_has_two_fixed_points)»: aquele teorema é sobre √x em [0, ∞); aqui é colapsoTotal. Mesma contagem, objetos distintos. Trocar «São» por «Fazem par com», com [ONTO].
- **registros_v405.py L144:** «a unica massa que o programa deriva de beta» sob [REAL]: choca com a moldura e com a forma do GA, também função de β. «a única massa cuja forma o programa escreve a partir de β e de u».
- **artigo_pt/en: E12, Tetelestai, Grande Atrator:** E12 fica sob o [REAL] do parágrafo, e o registro diz [KNOWN/DECLARADO]. «Tetelestai» é nome do operador dentro de frase [REAL]. «[DECISÃO, por ordem do operador]» omite «da gerência»: a classe A13 foi escolha da gerência (D33). Ajuste de etiqueta.
- **pedra/MassaTensaoPura.lean parcela_nunca_quita; runtime t4:** «nem em volta nenhuma finita»: o teorema é de uma volta. Vale por the_charge_never_completes em t qualquer, mas não está dito assim. Citar o teorema do kernel.
- **A_IDENTIDADE_traducao_en_da_gerencia.txt:** «not as a sum» para «não como conta»; o mesmo parágrafo usa «calculation» para «cálculo». «not as a calculation».

## 5. O que não examinei

- NÃO EXAMINADO: pos_rito (textos_v405_novo.pysnip só por varredura de frases; leitura, fechar, superfícies, chain, harnesses não lidos).
- NÃO EXAMINADO: instalar, reverter, rito_v405.sh, conferir_rito, B(n), bancada_B3_servico, orquestrador: fora do pedido; não os rodei.
- NÃO EXAMINADO: as 300 bandeiras uma a uma. #print axioms próprio em 18 teoremas (17 no trio; without_the_abyss_no_posto_reads_so sem axioma algum; saída em axiomas_terceiro_out.txt); as demais pelo Audit declarado no recibo [DECLARADO].
- NÃO EXAMINADO: a citação de Moffatt (Nature 404, 833, 2000) e o E = 3/2·Mgaα conferidos de memória [KNOWN], sem abrir a fonte.
- RESSALVA, decisão da gerência: o glob embute no um.py público a fala OPERADOR_30out_leitura3 («meu [dado pessoal removido]»), que nenhuma pedra usa. «Bento» já está na base como nome de teste, mas a frase é nova e pessoal. Não é confidencial pela régua nº 8; aponto para ele ler antes.

## 6. Custo de corrigir

Corrigir as pedras muda o hash de quase todas. Nenhuma prova cai. Os dois ALTO tocam docstring e um nome de teorema, e o Disco ganha um teorema se a gerência escolher essa via. Isso refaz, pela cadeia existente, pino, kernel incremental, candidato, ensaio a seco, p00 e os harnesses: o caminho que a própria errata de 13:33 já percorreu. Preservar as needles de `CONTEXTO` em `registros_v405.py`.

Rotas lidas no Mapa antes do exame: `kernel.emprestimo_da_massa.segunda_ponte_candidata_30out`, `kernel.ponte_da_massa_transversal.candidata_30out`, `kernel.identidade_que_e_quem_cartas_do_circulo_30out`, `kernel.identidade.candidata_01nov`, `kernel.observador_terminal.candidata_31out`, `massa.e0.conferencia_kimi_e_no_go_tipado_31out`, `alpha.derivacao.pergunta_do_operador_01nov`, `outro.grande_atrator_e_chandrasekhar`, `kernel.v405.preparacao_01nov`, `memoria.forma_madura_da_tgl_01nov`.
