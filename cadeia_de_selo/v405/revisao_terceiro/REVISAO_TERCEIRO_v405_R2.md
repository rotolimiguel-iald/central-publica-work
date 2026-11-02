# Revisão de terceiro da v405, segunda rodada

Revisor independente; não construí nada disto. Candidato `eaefcd095abbaee7`, lido por script ao fechar, 2026-11-01T20:53:20. **Veredito: NÃO APROVADA: 1 ALTO, 4 MÉDIO, 11 BAIXO.** Os 13 achados da R1 estão fechados de verdade. Nenhuma prova cai, nenhum número está errado, o gate não foi tocado. O que resta é um homônimo no código novo e quatro etiquetas. R1 em `REVISAO_TERCEIRO_v405_R1.md` e `.json`.

## 1. Os 13 achados da R1, um a um

| # | sev | achado | estado | conferência |
|---|---|---|---|---|
| 1 | ALTO | O no-go se levanta | FECHADO | L121 reescrita; L10 e L27 corrigidas; no arquivo a frase só resta citada na errata, entre aspas. A docstring nova distingue absoluto e relativo. |
| 2 | ALTO | the_terminal_reads_one | FECHADO | Rebatizado the_omega_pole_reads_one, homônimo dito em pedra e artigo; fecho ganhou the_fixed_points_read_one_and_zero. Token do veredito trocado: zero THE_TERMINAL_READS_ONE. O nome velho só sobrevive na errata. |
| 3 | MÉDIO | Disco: E(t) definida | FECHADO | the_flow_is_the_canonical_law é HasDerivAt real, no trio; o texto diz «linear por definição» e «uma solução do fluxo»; dephasing como perda é entrada declarada. |
| 4 | MÉDIO | Disco: leitura como teorema | FECHADO | Stone, registro e artigo separam [REAL] Ω² sem cota de [ONTO] a inscrição. Resta só em LEITURA_V405, como leitura marcada. |
| 5 | MÉDIO | 4Mg² contra 6Mg² | FECHADO | A pedra diz 6Mg² com a energia total e guarda 4 ao lado; a E12 cita a pedra. |
| 6 | MÉDIO | frases residuais nas pedras | FECHADO | Títulos e docstrings corrigidos; a guarda agora varre as pedras e tem controle negativo. Sobra uma frase inofensiva, ver BAIXOS. |
| 7 | MÉDIO | quatro leituras como lista fechada | FECHADO | «numa lista que não é fechada», 14 itens, com meioTom, omegaSq, ½ω, a hipótese de área, b = 0, g e κ; zero «FOUR_READINGS». |
| 8 | MÉDIO | [KNOWN] na dispersão | FECHADO | [INPUT, Tratado §3] em artigo, registro e textos; [KNOWN] fica só no ponto zero. O mesmo vício sobrevive noutro ponto: novo achado 5. |
| 9 | MÉDIO | fóton sob [REAL] | FECHADO | Artigo, registro e pedra: álgebra da forma; b = 0 lido como fóton é [ONTO]; TGLCoupling exclui b = 0. |
| 10 | MÉDIO | Observador sem ressalva | FECHADO | Artigo e textos dizem modelo finito, rótulos, «medido» é campo do tipo, perda é não injetividade. |
| 11 | MÉDIO | o que permanece é o ponto zero | FECHADO | Marcado [ONTO]; «nenhum teorema liga os dois». |
| 12 | MÉDIO | citações não verbatim | FECHADO | 294 citações varridas nas pedras e nos textos: toda fala atribuída ao operador é substring exata. O que sobra são títulos, rótulos e citações de kernel, conferidas (lista em d_nao_verbatim.json). |
| 13 | MÉDIO | 16 posições | FECHADO | «quatro niveis e cinco posicoes», como o código conta. |

**BAIXOS da R1:** Fechados: cabeçalhos das pedras, comentário de Γ em p6, título da seção (agora parte da fala dele), L268 do Observador, «a única massa», etiquetas E12/Tetelestai/DECISÃO, parcela, tradução. Restam, por decisão: nomes com «derivad-» e checks tautológicos (BAIXOS 9 e 10).

## 2. O código novo [REAL, por script e compilação nesta pasta]

- **Vacuidade de χ: descartada.** Provei no Lean do sandbox `revisor_chi_existe`: em todo `C : FockCertificate L` existe χ com ‖χ‖ = 1 e ⟪Ω, χ⟫ = 0, por `F_infinite`; só o trio (`r2_axiomas.lean`). `lock_no_angulo` não é vácuo DADO um certificado. O certificado em si o kernel não habita: achado 2.
- **`Acorde`, `modular`, `resolver`:** enunciados certos. `modular_nao_e_transposicao` e `mesmas_razoes_iff_transposicao` têm conteúdo real. `modular_comuta_com_transpor`, `resolver_modular` e `modular_sustenta` são o que dizem. `modular_mantem_a_escala` é consequência direta de sustentar, e a definição de escala está dita.
- **`E0_relativo_pinado` e `lerE0_e_a_tonica_modulada`:** definições ditas de outro modo, e o texto admite. Docstring de `E0_relativo_pinado`: «Segue da definição de `lerE0`». Artigo: «a definição de `lerE0` dita como razão». Registro: «nada mais». E₀ como tônica modulada é a leitura (11) da moldura. Sem achado.
- **`the_ratio_survives_the_rescaling`:** prova o que diz. A frase ao lado, «é a transposição», é BAIXO.
- **Seção O GAP:** as igualdades conferem; o nome `gap` é o achado 1.
- **Axiomas:** 22 teoremas novos e antigos, todos no trio. Zero `sorry` de código, zero `axiom`. Embutido, sandbox e `pedra/` têm o mesmo sha256 nas oito.

## 3. Disciplina de estatuto: as sete regras

| regra | estado |
|---|---|
| `tempoDoGap` como τ★ é [ONTO], a ratificar | CUMPRE em pedra, registro, artigos, moldura e parágrafo público |
| κ só como hipótese (24/08, conferida em `TheHorizonRate.lean` L13-15) | CUMPRE; ressalva BAIXA quanto a x7 |
| `U_E_NOT_DERIVED` fica; nada fixa u | CUMPRE |
| a ponte E_fluxo = E₀ não vale nesta leitura | CUMPRE, com o número |
| K não depende da inclinação | CUMPRE; conta conferida |
| as cinco notas são [OPEN] | CUMPRE |
| a escala é o que fica parado; `razao` não é escala | CUMPRE; o «tom» é outro assunto, achado 4 |

## 4. Achados abertos, ALTO e MÉDIO

### 1. [ALTO] pedra/PontoZeroDoPsion.lean: intro da seção O GAP (L156-158), def gap, o_gap_e_lido_do_angulo_de_miguel, the_gap_closes (L291); registro gap_v405 (registros_v405.py, gap_spec: diz, veredito); artigo PT/EN, parágrafo «O gap, ao lado»; pos_rito/textos_v405_novo.pysnip: _gap e o parágrafo do README/site

Homônimo: a mesma palavra para duas grandezas, na mesma seção. `o_lock_tem_gap_um` é o gap ESPECTRAL: H_min vale 0 no vácuo e 1 no ortogonal. Na unidade posta esse gap vale u = 1 eV. O texto segue: «Na unidade posta u, o gap é a energia retida, Δ = β·u». Δ não é gap: é o VALOR ESPERADO ⟨H_min⟩·u no estado a θ_M, que nem é autoestado; o gap espectral é 83,1 vezes Δ (1/β). Nenhum dos textos diz isso (grep por «valor esperado», «espectral» na seção: zero). E nenhum teorema liga as duas metades: `lock_no_angulo_de_miguel` é um produto interno em C.F, `o_gap_e_lido_do_angulo_de_miguel` é a identidade real sen²θ_M·u = β·u, e `the_gap_closes` não tem conjunto com H_min. Mesma classe do ALTO 2 da R1 (terminal), que a gerência corrigiu com rebatismo e aviso de homônimo. A fala do operador diz «gap com unidade»: a palavra é dele, e isso é leitura [ONTO], não [REAL].

**Proposta:** Dizer em pedra, registro, artigo PT/EN e parágrafo público: «[REAL] Δ = β·u é o valor esperado de H_min no estado inscrito no ângulo de Miguel, na unidade posta; o gap espectral do lock é 1, isto é, u; [ONTO] chamar Δ de gap é a leitura do operador». Acrescentar o teorema que falta, ligando o produto interno real a `gap c u` (u·⟨ψ_M, H_min ψ_M⟩ = gap c u). Preferível rebatizar a definição Lean (`gap` para algo como `retidoNoAngulo`); o nome da seção e do registro podem ficar, com o aviso. Prova nenhuma cai.

### 2. [MÉDIO] artigo PT/EN, «O gap, ao lado», [REAL]; registro gap_v405 (estatuto, diz); textos_v405_novo.pysnip _gap; pedra/PontoZeroDoPsion.lean L167-188

`o_lock_tem_gap_um`, `lock_no_angulo` e `lock_no_angulo_de_miguel` valem para todo C : FockCertificate L, e o kernel não exibe habitante desse tipo (Psibit.lean L102 e L124; `psibit_v395.conditional_psion_face.inhabitant_exhibited` = false). A casa marca isso como [CONDICIONAL]; aqui sai [REAL] sem a ressalva. A vacuidade de χ está descartada: ver seção 2. A do certificado segue dita em outro lugar, não aqui.

**Proposta:** «[REAL, condicional ao certificado de Fock, que o kernel não habita]». Melhor: enunciar os três lemas num espaço de Hilbert qualquer com Ω unitário; nada neles usa o certificado além disso.

### 3. [MÉDIO] artigo PT/EN, parágrafo «A inscrição e a medida»; textos_v405_novo.pysnip _gap; registro gap_v405 (limites, extras.inscricao_e_medida)

«[REAL] Como forma no kernel: zero_mode_weight_is_one (o peso 1 como integral de uma cauda, faces ½) e alpha_transport (gradiente negativo).» Dizer que esses teoremas são a forma da fala do operador é leitura da gerência, sob [REAL]. `alpha_transport` é sobre alphaKappa = sech(κ/2), com κ profundidade modular: homônimo tanto da α de estrutura fina quanto do κ relógio, num parágrafo sobre eletricidade. O sinal de α' = −(q/2)·α só é negativo em κ > 0, pois q é ímpar. `zero_mode_weight_is_one` é o peso L² de ½sech(κ/2) em toda a reta: «cauda» não está no teorema.

**Proposta:** «[REAL] os dois teoremas existem; [ONTO, da gerência] lê-los como a forma da fala do operador; homônimo: alphaKappa não é a α de estrutura fina nem κ é o relógio; o gradiente é negativo em κ > 0.»

### 4. [MÉDIO] artigo PT/EN, «A lei do diminuto», [REAL]: «a escala e o tom ficam (modular_mantem_a_escala...)»; textos_v405_novo.pysnip _lei; registros_v405.py L265; docstring de modular, «O tom do acorde não muda»

O kernel não tem termo para o tom: `Acorde` são cinco reais, e `modular_mantem_a_escala` fala só das razões entre notas sustentadas. «O tom fica» é fala do operador posta sob [REAL] e atribuída a um teorema que não o menciona. A nota principal, que seria o candidato natural a tom, é justamente o que muda.

**Proposta:** «[REAL] as notas sustentadas e as razões entre elas ficam; [INPUT] o tom fica, na fala dele: o kernel não tem termo para o tom.»

### 5. [MÉDIO] registros_v405.py L382 e L395 (ga_spec); textos_v405_novo.pysnip _ga

«[KNOWN] não discrimina da RG: na ordem linear M_TGL = M_RG (stealth)». Mesmo vício do achado 8 da R1: [KNOWN] é literatura, e stealth é resultado da própria teoria. Escapou da correção da R1, que tratou só da dispersão do psíon. O negativo em si não é contestado.

**Proposta:** Trocar por [DERIVED] ou [INPUT, teoria própria], conforme a origem no acervo.

## 5. Números (`r2_numeros.py`, do zero, α CODATA 2018, β = α·√e em runtime)

Tudo confere com o ensaio a seco até a última casa publicada: β 0,012031300400803; m₂ 8,507414 meV; Δ = 0,012031300 eV; τ = 83,1165 eV⁻¹ = 5,4708×10⁻¹⁴ s; Γ_B = 1,44752×10⁻⁴ eV (2,199×10¹¹ s⁻¹); ω_ψ = √2·Δ = 0,0170148 eV; Q = √2/β = 117,545; κ·τ = 2π, com κ = 1,1485×10¹⁴ s⁻¹ SE a hipótese valer; E_fluxo = 9,859×10⁵⁶ eV (log₁₀ 56,99), cerca de 10⁵⁷, não E₀; τ/t_P = 1,015×10³⁰; tônica Δ/α = √e; e^(3/2) = 4,48169; K 1,65737×10¹² J/s². Gap espectral do lock na unidade posta: 1 eV, 83,1 vezes Δ.

## 6. Citações, hashes, intocados

- **Citações:** 294 varridas, agora também nas docstrings; toda fala atribuída ao operador é substring exata. Os quatro trechos novos conferem.
- **Hashes:** 28 de 28 hex citados conferem com arquivo. Termos citados existem no kernel; os ausentes do kernel são nomes declarados como externos (`half_nat_araki_hidden_hamiltonian`, que o texto diz não ser termo; o nome Kimi do `AcordeE0`) ou antigos da errata.
- **Intocados:** as 7 funções e `GA_WINDOW_STATUS` têm AST e fonte idênticas às da base `3820476c83267f61` (`e_intocados.py`). 21 nós mudados, 0 removidos, 46 novos. `main` só ganha chamadas, impressões e chaves v405; nenhuma atribuição a chave do gate ou do neutrino no bloco novo (`e_main.py`).
- **Confidenciais:** zero padrões no candidato; zero da fala excluída.

## 7. O que não tinha examinado na R1

- **`pos_rito/textos_v405_novo.pysnip`, lido de fato:** bom. Moldura, pedras, estatutos, erratas e limites acompanham o artigo, e cada número e citação passa por leitura e conferência. Herda os achados 1, 2, 3, 4 e 5, porque repete os mesmos parágrafos. O parágrafo público traz «o lock mínimo tem gap 1; no ângulo de Miguel lê β, e na unidade posta Δ = β·u», sob [REAL].
- **`instalar_v405.py`:** toca só 10 arquivos em backup de bytes conferido, o `um.py` por temporário e `os.replace`, a cópia do pilar para o pacote e o recibo. Aborta antes de tocar: canônico ≠ v404, candidato ≠ esperado (`ESPERADOS`, `CANDIDATO` e `PRONTA` batem com o candidato: conferido), recibo pré-selo inválido, Bancada mudou, processo vivo, pilar diferente, módulo novo já presente. Recusa -O. Correto.
- **`reverter_v405.py`:** confere todos os backups antes da primeira escrita; guarda o estado falho; restaura por temporário; pedras em quarentena, nunca apaga; confere a âncora v404. Correto, BAIXO quanto a -O.
- **`rito_v405.sh`:** confere o hash antes de rodar; recusa com outro lançador, sonda ilegível, servidor que não para, VRAM acima de 6000 MiB ou ilegível. Mata só por PID da própria árvore, ou trabalhador do pilar órfão pela linha de comando, nunca por nome de processo. Religa o servidor em toda saída. Grava `RITO_RC`. Nada apaga. Correto.
- **A trava:** `pos_treino_v405.py` só passa S1b com `aprovada` true e `candidato_sha16` igual ao candidato; caso contrário registra e espera. Este JSON a mantém fechada.

## 8. Entra e sai do código novo

| pedra | ENTRA como definição ou hipótese | SAI como teorema |
|---|---|---|
| LeiDoDiminuto (acorde) | `Acorde`, `transpor`, `razao`, `lerE0`, `modular`, `resolver`, `meioTom`; `h` em `um_tom_vira_terca_menor`; `CollapseCostLaw` [INPUT] | razões ⟺ transposição; modular não é transposição; comuta; sustenta; abre meio-tom; resolve; igualdades de valor com a face |
| PontoZeroDoPsion (gap) | `FockCertificate`, χ unitário ortogonal; `gap` := energia retida; `tempoDoGap` := 1/gap; `h` de κ; `omegaSq`, `pagamentoComoCurvatura` | lock 0 e 1; sen²θ; β em θ_M; √2/τ = ω_ψ ⟺ τ = 1/Δ; Q = √2/β; κ/2π = Δ sob `h` |
| TonicaDoHamiltoniano | `reescala` | m/E₀ invariante |
| DiscoDeEuler | E linear, Ω² = K/E, Γ como perda | `HasDerivAt` do fluxo |

A tabela completa das oito pedras segue na R1, e os recursos antigos não mudaram de enunciado, salvo o fecho do Observador.

## 9. BAIXOS

- **pedra/LeiDoDiminuto.lean, um_tom_vira_terca_menor:** Título ★★★ «O SISTEMA OPERA EM TERÇAS»: o teorema vale para UMA nota, sob a hipótese h de ela estar um tom acima, e as cinco notas são [OPEN]. O artigo diz certo: «a aritmética 1 nat + ½ nat». Rebaixar o título.
- **pedra/TonicaDoHamiltoniano.lean L37, L103; artigo, Tônica:** «A reescala é a transposição do acorde» sob [REAL]: não há termo ligando `reescala` (TransicaoParaAMassa) a `transpor` (Acorde). É análogo, verdadeiro à mão. Dizer «corresponde a», ou acrescentar o teorema via Lei.
- **pedra/PontoZeroDoPsion.lean L265; runtime x6; artigo E10:** A pedra diz «terceira leitura do mesmo sen 45°»; a E10 e o parágrafo público dizem «duas leituras». É aritmética de 2Δ·sen45°. Alinhar.
- **pedra/PontoZeroDoPsion.lean o_relogio_do_gap; runtime x7:** Conferido contra TheHorizonRate.lean L13-15: κ entra como hipótese h, nada é busca; a regra é cumprida. Mas a conclusão expressa κ = 2π·β·u, e x7 grava esse número no `valor` do check, em tensão com «só aparece como hipótese» e com «não alvo de uma equação de inversão». Tirar o número do `valor` de x7; escrever «como antecedente».
- **pedra/PontoZeroDoPsion.lean L158, L291:** «Todos são Δ», «Tudo é o mesmo Δ»: com tempoDoGap := 1/gap e gap = β·u, várias estrelas são tautologia (½·2/(1/Δ) = Δ). A seção avisa «álgebra», mas ★★★ e «conecta» sugerem mais que isso. Aceitável; baixar as estrelas.
- **textos_v405_novo.pysnip: __HEADER__, topico_missao, remissivo; rito_v405.sh, cabeçalho:** Listas de registros sem `gap_v405`. Acrescentar.
- **reverter_v405.py:** Usa assert sem a guarda de -O que o instalar tem. Roda só por ato da gerência. Como no molde, não restaura os .tex e .pdf que o rito reescreve nem limpa .lake. Copiar a guarda; dizer o que não restaura.
- **instalar_v405.py:** Janela mínima: o recibo APLICADO só é gravado depois do os.replace; se a gravação falhar, o reverter não acha recibo. Os .bak_<ts> existem e o orquestrador para no rc. Aceitável; ou pré-gravar o recibo.
- **PonteDaMassa, MassaTensaoPura: transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto:** Persiste da R1: nomes com «derivad-»; as docstrings avisam. Decisão da gerência.
- **runtime_v405.py g1, x7, x10:** Persiste da R1: checks que comparam por construção. Aceitar.
- **textos_v405_novo.pysnip, desenho:** «O que segue do operador: ... a revisão independente»: ficará velho se a revisão aprovar. Ajustar.

## 10. O que não examinei

- NÃO EXAMINADO: as 364 bandeiras uma a uma; #print axioms próprio em 22 teoremas (todos no trio, mais a testemunha do revisor). Os demais pelo recibo [DECLARADO].
- NÃO EXAMINADO: leitura_v405, fechar, superfícies, chain, registrar_mapa, harnesses, orquestrador (só o ponto que lê este JSON), B(n).
- NÃO EXAMINADO: a fonte de Moffatt e o AcordeE0.lean do Kimi conferidos só por hash citado, não pelo conteúdo.
- NÃO EXAMINADO: o rito não foi rodado, como manda a regra; instalar, reverter e rito lidos, não exercitados.
- RESSALVA: os arquivos _R1 desta pasta guardam, numa ressalva, trecho da fala hoje excluída; a purga isenta a pasta do revisor, e nada dali vai ao candidato. Conferido: zero ocorrência no candidato. A gerência decide se os _R1 ficam em work.

Rotas lidas no Mapa: `kernel.ponte_da_massa_transversal.candidata_30out`, `kernel.emprestimo_da_massa.segunda_ponte_candidata_30out`, `kernel.identidade.candidata_01nov`, `kernel.observador_terminal.candidata_31out`, `massa.e0.conferencia_kimi_e_no_go_tipado_31out`, `alpha.derivacao.pergunta_do_operador_01nov`, `outro.grande_atrator_e_chandrasekhar`, `kernel.v405.preparacao_01nov`.
