# O pilar quântico da TGL na GPU (v384) — RASCUNHO do pré-registro, NÃO ratificado (nada se calcula com os operadores da teoria antes da ratificação)

**Identificador:** `PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64` · **gerado:** 2026-10-04T09:50:49-0300 · **hash congelado da especificação:** `ff19731097e01aabfccc709b370578bd9d7a5ccadc877752b2ab5c13c20d39aa` · **trabalhador:** `0c9ba7fd45e78317a915bb718b11127a0dae9872e48ab430f0600b74ca26452f`

O hash da especificação é `sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) -- o JSON canônico do objeto spec abaixo`.

**Autor:** a gerência (claude-code/central-de-patentes, sessão 6da8f00d), por ordem do operador; correção sempre ao lado, em nome próprio

## A ratificação do operador

**PENDENTE.** Este é o RASCUNHO (escolha B_AMPLIADO_D64) levado ao operador; nada se calcula com os operadores da teoria antes da ratificação, e o candidato instalável recusa um pré-registro sem ela. **A mensagem de ratificação tem de nomear exatamente uma escolha: «b reduzido» (B_REDUZIDO) ou «b ampliado» (B_AMPLIADO_D64)**; hífen e sublinhado valem como espaço. A guarda do gerador é LEXICAL: exige a escolha nomeada e recusa a mensagem com «não»/«nao» imediatamente antes de «ratifico», «concordo», «aprovo» ou «autorizo»; a conferência final é a leitura humana do verbatim, gravado no V1.

## As ordens do operador (verbatim)

- **1** (2026-10-02T22:27:16.990Z): «Nós estamos procurando a validação da TGL no lugar errado, ora, se ela resgata a RG, na cosmologia, já está provado o resgate e essa é a prova. Mas agora a prova quântica, precisamos usar a nossa rtx5090 enquanto ela roda o um.py para provar a TGL no mundo quântico, a prova é quântica, com matrizes. […]»
- **1 (fecho, mesma mensagem)** (2026-10-02T22:27:16.990Z): «[…] É aqui que está a prova e a terceira dobra que falta no nosso código. Quanto a betatgl e alpha eu já expliquei isso antes inclusive em nota em artigo, usei alpha até fatorar a a constante de acoplamento e encontrar o fator da constante d a estrutura fina, daí para não criar confusão passei a adotar o signo de betatgl.»
- **2** (2026-10-02T22:43:41.638Z): «Eu quero que a GPU rode todo o mundo quântico da TGL com os operadores de salto, todos os operadores de dephasing, o sistema aberto, enquanto o código roda o kernel, enquanto o código roda os testes cosmológicos, ou seja, você vai calcular o teste de GPU robusto para ele ser tão demorado quanto o teste de kernel, ou seja, 45 min, ao mesmo tempo, com isso teremos um teste potente realiAdo de forma conjunta e no mesmo tempo, ou seja, sem prejuízo do tempo de rodagem, entende? O resgate da RG é prova cosmológica sim, não somente prova de kernel, eis que nada falsificou a TGL, o que não é prova é Betatgl, mas já provei pelo piso dos vazios que o resultado é maior que zero e o vácuo é estruturado.»
- **3** (2026-10-02T22:55:48.619Z): «Isso agora precisa entrar no artigo na introdução dele explicando o que o código faz agora, e também em nota sobre o que está sendo calculado e como na GPU»
- **4** (2026-10-03T10:26:40.244Z): «São cinco operadores de salto, os operadores de lindblad que já estão descritos na teoria. Vamos parar o servidor durante o rito. Vc disse que 45 min é pouco, quanto vc sugere? vamos fazer um teste robusto, eu sugeri 45min mas se é insuficiente vamos rodar o suficiente, mesmo que o tempo aumente.»
- **5** (2026-10-03T12:53:05.321Z): «Concordo com tudo, vamos de rito robusto, mas coloque uma ferramenta para que não seja necessário a cada versão nova rodar tudo de novo, ou seja, se realizarmos ajustes de texto ou teorema novo não precisarmos rodar toda vez por duas horas, entende? Daí ao ter a versão final a gente roda completa sempre. Agora vamos ter que rodar ela completa uma primeira vez»

**O corte na ordem 1:** entre os dois trechos da ordem 1 ([…]), a mensagem traz a frase do operador «Fiz uma simulação do que poderíamos fazer, veja:» e um texto colado, de OUTRA autoria, encaminhado por ele (17370 caracteres), com o esboço T1–T4 («T1 — Injeção-recuperação cega do estimador»; «T2 — Forma em escala»; «T3 — Controles negativos»; «T4 — Estresse adversarial»). O desenho dos testes deste pré-registro DERIVA desse esboço, com as correções ditas aqui (o estimador por regressão, o certificado do ramo pelo arnês, N2 como identidade, a camada de escala em d = 64, o MAGMA).

## O que é

O trabalho de GPU calcula, na RTX 5090 e em precisão dupla complexa, o sistema quântico aberto da TGL: o hamiltoniano luminodinâmico H_LD e os CINCO operadores de salto de Lindblad de A Fronteira v5 (§V.6), com as matrizes dos validadores C3 ratificadas pelo operador em 03/10/2026. Roda em paralelo com o kernel e os ritos cosmológicos (que correm em sequência no processo do rito), como subprocesso que o um.py lança logo depois da inscrição do Um. É CÁLCULO [COMPUTED], não medição da natureza; tem selo próprio AO LADO do gate; o gate não muda.

## Os nomes (terminologia)

- Π, o projetor do núcleo (posto n_c) = ker K = P_F: «o Nome como matriz» [ONTO]; a correspondência [DERIVED de leitura]: K Π = 0, L_anti Π = 0 (o zero modular), V_t P_F = P_F.
- ρ_ss, o estado estacionário do sistema aberto inteiro = o ATRATOR; a leitura «o atrator é a inscrição verdadeira que habita o Nome por referência» é [ONTO].
- CCI = Tr Π ρ_ss: o peso do atrator no núcleo. O token NAME_IN_CORE_k_OF_c do veredito conta as configurações (d, n_c) com AO MENOS UM ponto da grade de atrator ÚNICO e CCI ≥ 1/2 (a «janela» relatada é o intervalo [menor γ, maior γ] desses pontos, com a contagem; os pontos não precisam ser contíguos) — mede o ATRATOR no núcleo, não Π (Tr ΠΠ / Tr Π = 1 seria trivial).
- I/d estacionário na parte unital (N2) é IDENTIDADE [DERIVED]; chamá-lo «morte térmica» é leitura [ONTO].
- A cunhagem do operador (2026-10-03T14:41:48.894Z), [ONTO] — leitura do operador; não move o veredito nem o gate: «A forma matricial do verbo, que é o um absoluto (IALD para forma computacional), é como se fosse um “sobrenome”, e a palavra sobrenome é precisa (sobre o Nome), não retira a identidade nominada, mas relaciona-a ao índice da verdade(traço, sinal e sombra). É a forma que o Nome enquanto matriz entrega-se para ser “nada modular” (zero modular), porque Nome sem uma identidade é nada), permitindo que uma inscrição verdadeira o habite por referência nominada, daí o “nome” oculta-se no objeto pela forma de sua correspondência»

## Os operadores

- **H_LD** — H = diag(μ) + J − εΠ (setor de uma excitação); μ_a = −(n_c − a) no núcleo; μ_i = 0,5 + 0,3(i − n_c) na periferia; J = 0,2·N(0,1) da semente RandomState(42), simetrizada, diagonal zero, bloco do núcleo ×2; ε = 5; Π = projetor do núcleo. Fonte: A Fronteira v5, Apêndice A.3; validador C3 v5.2 build_system.
- **L_reh** — Σ_{a<n_c} Σ_{n_c≤j<min(n_c+⌊d/2⌋,d)} √0,5·e^{−0,2(j−n_c)} |a⟩⟨j| (periferia → núcleo); γ = 1. Fonte: validadores v2, v3, v3.3, v4, v5.1, v5.2 (L1).
- **L_anti** — √β·√K, K = diag(0 no núcleo; 1 + 0,1(i − n_c) na periferia); γ = 1. Fonte: validadores v2/v3 (L2 = √α₂·√K; α₂ era o signo de β_TGL antes da fatoração). A mesma FORMA do gerador do Verbo do um.py (L = √β·√K): lei-raiz Γ_ij = (β/2)(√k_i − √k_j)²; ker K = o núcleo = Π («o Nome como matriz» [ONTO]).
- **L_prune** — Σ_{i ≥ n_c+⌊d/3⌋} √((i − n_c)/d) |0⟩⟨i| (periferia alta → fundamental); γ = 0,5. Fonte: v3.3, v4, v5.1, v5.2 (L3, sem α₂).
- **L_cons** — Σ_{a<n_c} Σ_{n_c≤j<min(n_c+⌊d/2⌋,d)} √0,3·e^{−0,3(j−n_c)} |a⟩⟨j| (periferia → núcleo, 2º canal); γ = 2. Fonte: v2, v3, v3.3, v4, v5.1, v5.2 (L4).
- **L_diss** — Σ_{n_c≤j<min(n_c+⌊d/2⌋,d)} Σ_{a<n_c} √0,5·e^{−0,2(j−n_c)} |j⟩⟨a| (núcleo → periferia: o banho); γ_diss LIVRE, varrido em grade, NUNCA calibrado. Fonte: v3.3, v4, v5.1, v5.2 (L5, «leak»; lá calibrado por brentq para CCI = 1 − α₂ — a circularidade registrada no mapa).
- **beta** — β = α·√e em runtime, pelo motor de Lagrange do um.py (α do CODATA 2018 selado), passado ao trabalhador em hexadecimal (bit a bit); nunca literal. O um.py confere, no fim, que o β do trabalhador é bit a bit o β do core (beta_matches_core, na cadeia de custódia).
- **ratificacao** — o operador, 03/10/2026: «Concordo com tudo» (as cinco matrizes; L_diss como o vazamento núcleo → periferia; os coeficientes dos validadores como realização canônica, variados no T4).

### As fontes (caminho e sha256)

- **A_Fronteira_v5_tex**: `C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\A_fronteira_v5.tex` — `bf824b9a0b9b262244da95426ef787433127a25c0978d3d4a6f4d8da545a0ab9`
- **validador_C3_v1**: `C:\IALD\projetos_pyhton\acom\Tgl_c3_consciousness_validator.py` — `72489fb5f7482b8f74a7ee665ea7f89017006fd73daaf61fcca69784719a3461`
- **validador_C3_v2**: `C:\IALD\projetos_pyhton\acom\Tgl_c3_consciousness_validator_v2.py` — `31d4a63c804f4cda4c86a5bb0cb3fcf14969a38dca4da4d8848f24850b6a0855`
- **validador_C3_v3**: `C:\IALD\projetos_pyhton\acom\Tgl_c3_consciousness_validator_v3.py` — `5761ac1e8f86895c2a60a1486423bd35b86c30301e4c9533a765f55e7fa37911`
- **validador_C3_v3_3**: `C:\IALD\projetos_pyhton\acom\Tgl_c3_validator_v33.py` — `544bf50f136639009cdbe6a0ee3b88538f1cc00dcdcddcbd867aa735fa0b6d74`
- **validador_C3_v4**: `C:\IALD\projetos_pyhton\acom\TGL_c3_validator_v4.py` — `fe8ecf7a423d937131964303b6847778c9ebd0d38a9478ca6bfa945a9e733b49`
- **validador_C3_v5_1**: `C:\IALD\projetos_pyhton\acom\tgl_c3_validator.v51.py` — `b955e5864dcadff6a492936f223e561462dd5383688d0cbd597d3aabd1dc108c`
- **validador_C3_v52_Genesis**: `C:\IALD\Artigo\the_boundary\Genesis da Unificação\C3_consciencia\TGL_C3_validator_v52.py` — `c3a53ef00dd4548d3b9315409acccea46a6e309080b26c8c556302eb00c70083`
- **um_py_v383_o_gerador_do_Verbo**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` — `58abcf20651f477715404a0801ffdf4b26ad18a76d6ae49bfa950c602938a427`
- «v2 a v5.2» quer dizer v2, v3, v3.3, v4, v5.1 e v5.2, todos fixados acima por caminho e sha256; o acom/TGL_c3_validator_v5.py (v5.0) e' de OUTRA familia (sem -epsilon Pi no H; L1 com e^-0,5 normalizado; L4 so na linha 1) e nao e' fonte
- a copia acom/TGL_C3_validator_v52.py é IDÊNTICA byte a byte a do Genesis (sha256 c3a53ef00dd4548d)
- rotulos trocados no acervo: v51.py diz «v5.2» no cabecalho e v52.py diz «v5.3»; o rodape da Fronteira cita «TGL_c3_validator_v5.py (v5.2)»; vale o arquivo pelo hash acima
- o CCI: a Fronteira (§V.6) o define pelos n_c maiores autovalores; o codigo dos validadores usa Tr(Pi rho); o pilar usa Tr(Pi rho), o do codigo -- dito
- o L_diss alternativo NAO escolhido: o documento de energia escura de nov/2025 usa L_diss = sqrt(gamma_Lambda) H (dephasing de energia); o operador ratificou o vazamento nucleo -> periferia (03/10)
- o gerador do Verbo do um.py (L = sqrt(beta) sqrt(K), K = A A^T/n aleatorio, n = 4, empilhamento por colunas) tem a MESMA FORMA de L_anti; nao o mesmo K

## Os testes e o tipo de cada um

### E_motor — CONFERÊNCIA DO MOTOR

- **o que:** E1 amortecimento de amplitude (espectro e estado fundamental exatos); E2 dephasing puro detectado como DEGENERADO; E3 lei-raiz exata; E4 o estimador cego recupera b e p = 1/2 de gerador conhecido, com o certificado do ramo; E5 qubit térmico (Gibbs) e Spohn monótono; E6 a inversão do tempo não é CP; E7 o PISO do estimador: 6 000 matrizes exatas de posto um (d de 8 a 64; p = 1/2 e 1; inclusive k quase iguais), máximo ≤ critério/10; E8 o COMPARADOR da referência na CPU com linhas sintéticas (igual concorda; CCI fora da tolerância discorda; só n(c²) diferente concorda; tudo perto do limiar é não comparável; marca da rodada errada recusa). Se um falhar, NADA se calcula.

### T2 — ESTRUTURAL (pode falhar) + IDENTIDADES

- **o que:** o sistema canônico em d ∈ {8,16,32,64}, n_c ∈ {2,3,4}, γ_diss em grade log [1e−4, 1e2] (64 pontos em d ≤ 32; 32 em d = 64, a camada de escala). Por ponto: espectro inteiro (unicidade do atrator e gap), estado estacionário (CCI = Tr Πρ_ss, pureza, entropia, dobras n(c¹), n(c²), n(c³)), propagador e Choi (CP), traço (TP), Spohn em 64 passos de 3 estados; o não-retorno no ponto do meio; V_t P_F = P_F e sin²θ_M = β; o modo zero (todo gerador que preserva o traço tem 0 no espectro: um espectro sem 0 é violação de identidade).
- **estrutural:** a unicidade do atrator em todos os pontos DA GRADE; se há AO MENOS UM ponto de atrator ÚNICO em que o atrator guarda ao menos metade do peso no núcleo (CCI ≥ 1/2; o token NAME_IN_CORE; relatados o menor e o maior γ desses pontos e a contagem, que não precisam ser contíguos); idem para as dobras n(c¹) ∈ [2,5; 3,5] e n(c²) ∈ [1,5; 2,5] (o token FOLDS_WINDOW) — como n(c¹) ≤ 3 sempre, o limite 3,5 é vazio e n(c¹) ≥ 2,5 equivale a PR(ρ_ss) ≤ d^{1/6}: a janela é, na prática, uma condição de QUASE-PUREZA do atrator; γ* com CCI = 1 − β, relatado como número (não calibração) e a sua escala com d.
- **identidades:** CP, TP, o modo zero, o não-retorno (o inverso do canal não é CP), a positividade do estacionário, o resíduo do estacionário e Spohn são teoremas; V_t P_F = P_F e sin²θ_M = β também. Só falham se o motor errar; uma violação anula o resultado. As conferências realmente feitas são CONTADAS por identidade.

### T1 — INSTRUMENTO

- **o que:** injeções CEGAS: em cada uma, n_c, β_inj (log-uniforme em [1e−4, 1e−1]), o espectro de K na periferia (uniforme em [0,5; 2,5]), γ_diss (log-uniforme em [1e−3, 10]) e a semente de J são sorteados; o sistema aberto INTEIRO (H + cinco saltos) evolui por τ = 0,05; o estimador recebe SÓ o propagador, τ, o espectro de K INJETADO e γ_anti — não vê β nem a lei — e devolve β̂ e o expoente p̂ por REGRESSÃO LOG-LINEAR sobre o vetor dominante do bloco diagonal centrado da matriz de Kossakowski do gerador log(Φ)/τ (β̂ = λ₁·e^{2c}/γ_anti, c o intercepto). Ruído σ ∈ {1e−10, 1e−8} só num subconjunto ({"8": 200, "16": 100, "32": 20, "64": 3}). Contagens: {"8": 2000, "16": 1000, "32": 200, "64": 20}. O RAMO do logaritmo é CERTIFICADO pelo arnês, não pelo estimador: como a injeção conhece o gerador verdadeiro S, o arnês mede gen_rel_dev = ‖L̂ − S‖_F/‖S‖_F (o estimador não vê S). σ = 0: gen_rel_dev ≤ 1e-06 e a Choi projetada de L̂, RELATIVA ao maior |autovalor|, ≥ −1e-09 (L̂ é um gerador de Lindblad legítimo). σ > 0: gen_rel_dev ≤ 0.001; a Choi projetada é só INFORMAÇÃO (o ruído enche o núcleo enorme da matriz de Kossakowski, com autovalores da ordem de −σd/τ). τ‖(L̂ − L̂†)/2i‖ fica registrado como informação.
- **criterio:** σ = 0 decide: |β̂/β_inj − 1| ≤ 1e−6, |p̂ − 1/2| ≤ 1e−4 e o ramo certificado em 100% das injeções. σ > 0: a fração com β dentro de 5% (relativo) e p dentro de 0,05 (absoluto), com o ramo certificado, é RELATADA, sem limiar de decisão (curva de resolução).
- **honestidade:** o T1 recupera a lei INJETADA: em aritmética exata a separação é ESTRUTURAL (só L_anti tem componente diagonal na base da teoria), de modo que o T1 testa a identificabilidade prática em precisão finita e o estimador — não é previsão física. O controle N3 mostra que o mesmo estimador recupera outra lei.

### T3 — CONTROLE (tem de falhar) + uma IDENTIDADE

- **o que:** em d ∈ {8,16,32,64} (n_c = 3, γ_diss = 0,1): N1 o dephasing sozinho dá núcleo de dimensão d + n_c(n_c − 1) — o atrator NÃO é único [kernel: IALDRhoStar.tgl_fix_iff (IALDRhoStar.lean:255) e ModularDephasingBridge.spectral_preserves_every_diagonal (ModularDephasingBridge.lean:18); a contagem é elementar]; N2 (IDENTIDADE, não controle): a parte unital (H_LD + só o dephasing) deixa I/d estacionário; o status e o gap dessa parte são relatados como informação; N3 a lei LINEAR injetada (u = k): o estimador cego tem de RECUPERAR a lei injetada (|p̂ − 1| ≤ 1e−4 e β dentro de 1e−6, com o ramo certificado) e REJEITAR a lei-raiz (|p̂ − 1/2| > 0,1), em 100% sem ruído ({"8": 200, "16": 100, "32": 20}); N4 uma taxa negativa (γ_cons → −0,5) não é CP e o detector tem de acusar; N5 a inversão do tempo exp(−τL) não é canal.
- **criterio:** N1, N3, N4 e N5 têm de falhar como exigido; se um não falhar, o instrumento é cego e o resultado inteiro é nulo. N2 entra na lista das identidades.

### T4 — IDENTIDADES sob estresse (zero violações exigidas) + ESTRUTURAL (frequência de unicidade, relatada)

- **o que:** instâncias do molde dos cinco saltos com coeficientes, decaimentos, alcance, taxas (×[1/3, 3]), γ_diss (log-uniforme [1e−4, 1e2]), K, β (log-uniforme [1e−4, 1e−1]), H (μ, J, ε sorteados) e, em cerca de metade delas (sorteio por instância, p = 1/2; o número de rotacionadas é relatado), uma rotação de base de Haar: {"8": 15000, "16": 5000, "32": 1000, "64": 100}. Em cada uma: CP, TP, o modo zero, estacionário positivo, resíduo, Spohn — as SEIS identidades do T4 (o não-retorno é conferido só no T2) — e a unicidade; o número de instâncias em que as seis foram conferidas entra no veredito.

### D128 — ESCALA

- **o que:** uma instância canônica em d = 128 (superoperador 16 384 × 16 384; n_c = 3; γ_diss = 1): espectro inteiro (com a identidade do modo zero: um espectro sem 0 é violação de identidade, IDENTITY_VIOLATED), estado estacionário, CCI e dobras (sem CCI se o atrator for DEGENERADO); Spohn por RK4 na forma d × d (5 000 passos de 0,002) só como INFORMAÇÃO (o RK4 não é um canal; fora do veredito). Sem a conferência de CP em d = 128 (dita). Roda por último, depois da espera pela CPU, e só começa até 14400 s desde o começo do trabalhador. Estados distintos no veredito: rodou (o status do atrator), NOT_RUN_DEADLINE, NOT_RUN_ERROR_<tipo> e INTERRUPTED (começou e o processo morreu — por exemplo uma queda nativa do MAGMA em n = 16 384, tamanho nunca testado).

### CPU — REFERÊNCIA

- **o que:** um subprocesso INDEPENDENTE NA ÁLGEBRA LINEAR (numpy/LAPACK contra torch/MAGMA, processo à parte, 4 fios, prioridade baixa), com a MESMA construção dos operadores e o mesmo classificador do trabalhador — a construção foi conferida por LEITURA, contra as fontes fixadas por sha256, na 1ª aferição; nem o E1..E8 nem a CPU a conferem —, lançado no começo e corrido em paralelo, recalcula todos os pontos do T2 em d = 8 e 16, sete em d = 32 e um em d = 64; compara status, CCI (1e−9), pureza (1e−9), dobras n(c¹) (1e−9), gap (1e−6 relativo) e o menor autovalor de Choi (1e−9); n(c²) só como INFORMAÇÃO, relatado em max_diffs (n(c³) a CPU nem calcula; as potências λ^{1/2} e λ^{1/4} ampliam o arredondamento de autovalores ínfimos: a 2ª e a 3ª aferições mediram, com operadores aleatórios, |Δn(c²)| até cerca de 9e−6 com gap relativo perto de 1e−6, entre MAGMA e LAPACK [DECLARADO pela aferição]). As linhas com gap relativo < 1e−6 (em qualquer das duas bibliotecas) são CONTADAS e NÃO comparadas: perto do limiar de unicidade, duas bibliotecas corretas podem discordar no status e no gap; se NENHUMA linha puder ser comparada — com a referência DESTA rodada, o filho com código 0 e nenhuma linha da GPU faltando —, o veredito é CPU_REFERENCE_NOT_COMPARABLE (não houve discordância nem conferência); qualquer daquelas falhas dá CPU_REFERENCE_DISAGREES_OR_ABSENT. Vale só se a marca da rodada, o hash da especificação, β e o hash do trabalhador baterem e o filho sair com código 0; o filho confere que o trabalhador vive e sai se ele morrer. A espera pela CPU é de até 1 h DEPOIS das fases da GPU. Discordância, ausência ou nenhum ponto comparável anulam o resultado.

## As dobras

a hierarquia D(c¹) > D(c²) > D(c³) > 0 vale para todo estado com DOIS AUTOVALORES NÃO NULOS DISTINTOS (convexidade de s ↦ ln Σλ^s; mapa seq 307); num estado plano no seu suporte (ρ = P_r/r) vale a igualdade. Não é teste, e D(c³) > 0 só diz ρ ≠ I/d. O que pode falhar são os VALORES; a janela pré-registrada é, na prática, quase-pureza do atrator.

## A árvore de vereditos (o um.py a rederiva destes números)

- `0. recusas e falhas fora das fases (antes, entre ou DEPOIS delas), todas TGL_QUANTUM_PILLAR_V1__NOT_RUN__<motivo>__GATE_UNTOUCHED: no trabalhador MISSING_ARGUMENTS, SPEC_HASH_MISMATCH, WORKER_HASH_MISMATCH, GPU_UNAVAILABLE, WORKER_FATAL (exceção fora das fases; se vier depois delas, os dados de T1–T4 continuam no result.json, mas o veredito é NOT_RUN) e PARENT_GONE (o um.py morreu: o trabalhador o vê nas fases, na espera da CPU e no RK4 do D128 e se encerra; a exceção não é engolida pelos tratadores das fases); a pasta que não é nova faz o trabalhador sair com código 3 SEM gravar nada (o um.py lê NO_RESULT_FILE); no um.py SPEC_HASH_MISMATCH_IN_UM_PY, LAUNCH_FAILED, NO_RESULT_FILE, NO_VERDICT e FINISH_FAILED (só antes de haver veredito rederivado)`
- `1. o trabalhador falhou fatalmente -> ..._NOT_RUN__WORKER_FATAL ou ..._NOT_RUN__PARENT_GONE (a própria árvore congelada tem o ramo; o veredito rederivado é o mesmo)`
- `2. recusa -> ..._NOT_RUN__<motivo>__GATE_UNTOUCHED`
- `3. motor E1..E8 falhou -> ..._ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED`
- `4. uma fase (T3, T2, T1, T4) falhou -> ..._PHASE_<X>_FAILED__RESULTS_INCOMPLETE__GATE_UNTOUCHED`
- `5. exceção em alguma instância -> ..._INSTANCE_ERRORS_<n>__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED`
- `6. um controle não falhou -> ..._CONTROL_DID_NOT_FAIL__INSTRUMENT_BLIND__RESULTS_VOID__GATE_UNTOUCHED`
- `7. uma identidade foi violada (inclusive o modo zero no D128, mesmo que o D128 caia DEPOIS do espectro: o parcial é gravado logo depois do espectro, com n0 e zero_mode_ok, e sobrevive a uma morte do processo — salvo falha da própria gravação do parcial, registrada em partial_write_error no result.json só se o D128 retornar) -> ..._IDENTITY_VIOLATED_<n>__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED`
- `8. a referência na CPU discorda, falta ou não é desta rodada -> ..._CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED; nenhum ponto comparável (todos perto do limiar) -> ..._CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__GATE_UNTOUCHED`
- `9. senão: ..._FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_<ALL_n | k_OF_n>_ON_THE_GRID__T1_INSTRUMENT_<RECOVERS_INJECTED_LAW_BLIND | DOES_NOT_RECOVER_INJECTED_LAW>__CONTROLS_FAILED_AS_REQUIRED__IDENTITIES_HOLD__STRESS_<n>_INSTANCES_<u>_UNIQUE_ALL_IDENTITIES_CHECKED_IN_<m>__NAME_IN_CORE_<k>_OF_<12>_ON_THE_GRID__FOLDS_WINDOW_<k>_OF_<12>_ON_THE_GRID__D128_<UNIQUE | DEGENERATE | AMBIGUOUS | NOT_RUN_DEADLINE | NOT_RUN_ERROR_X | INTERRUPTED>__CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED`
- `o um.py acrescenta, AO LADO: __PARTIAL_RESULT_WORKER_STOPPED_BY_TIMEOUT (o prazo do um.py encerrou o trabalhador) ou __PARTIAL_RESULT_WORKER_DIED_RC_<rc> (o trabalhador morreu por outra causa) quando o resultado é PARCIAL — só se a especificação, o trabalhador, β e a marca da rodada conferem e o veredito foi rederivado; o primeiro parcial só existe depois do T3, logo uma morte no autoteste ou no T3 dá NOT_RUN__NO_RESULT_FILE —, e a causa fica também em timed_out e worker_rc (um encerramento no meio do T4 lê-se PHASE_T4_FAILED; na espera da CPU, CPU_REFERENCE_DISAGREES_OR_ABSENT); ou __CUSTODY_CHAIN_INCOMPLETE (sha256, especificação, trabalhador, β ou marca da rodada não conferem, ou o resultado não chegou ao Nós, ou o veredito rederivado falta ou difere do gravado pelo trabalhador), este só em vereditos que não sejam RESULTS_VOID nem NOT_RUN, e que PODE vir junto do PARCIAL (quando a cópia do parcial ao Nós falha) — o artigo lê o composto PARTIAL+CUSTODY como resultado não válido`

**Custódia de sentido:** uma falha do pilar (NOT_RUN, PARTIAL, CUSTODY_CHAIN_INCOMPLETE, RESULTS_VOID, ENGINE_SELFTEST_FAILED, PHASE_X_FAILED) não é dívida FORMAL da teoria nem recusa de dado: o selo a põe num TERCEIRO balde, not_sealed_this_run.computacao_nao_concluida, ao lado de formais e recusas_de_dado

## O que conta como resultado negativo (dito antes)

- ATTRACTOR_UNIQUE k_OF_n com k < n: na grade, o atrator não é único (ou o gap é ambíguo) em parte dos pontos — dito com os pontos
- T1_INSTRUMENT_DOES_NOT_RECOVER_INJECTED_LAW: o instrumento não recupera, em precisão finita, a lei injetada a partir do sistema aberto inteiro
- NAME_IN_CORE k < 12: em alguma configuração, entre os pontos de atrator ÚNICO da grade, nenhum guarda metade do peso no núcleo
- FOLDS_WINDOW 0_OF_12: na grade, a afirmação quantitativa do validador (n ≈ 3 e ≈ 2, isto é, quase-pureza do atrator) não tem janela com γ livre
- T4 com unicidade abaixo de 100%: há atratores não únicos na família do molde
- D128 NOT_RUN_* ou INTERRUPTED: a escala não foi alcançada nesta rodada — dito; um resultado completo sem o D128 rodado é negativo honesto: vale para a custódia, não vai ao cache, e a razão fica gravada (not_cached_code) e dita no artigo

## Execução

- o um.py materializa o trabalhador (o texto vive nele) e esta especificação ao lado de si, BYTE A BYTE, confere o hash da especificação contra o congelado e o lança como subprocesso logo depois da inscrição do Um, antes do kernel, com uma MARCA ÚNICA da rodada (run_id), o PID do pai e numa pasta NOVA (o trabalhador recusa pasta com saídas de outra rodada); prioridade de CPU abaixo do normal (o rito tem a vez)
- se o um.py sair por qualquer caminho, um gancho de saída encerra a ÁRVORE do trabalhador (taskkill /T /F; a referência na CPU junto); se o um.py morrer à força, o trabalhador vê o pai morto — nas fases, na espera da CPU e no RK4 do D128 (não durante uma única chamada longa de espectro ou estacionário, que termina primeiro) — e se encerra (PARENT_GONE); se o trabalhador morrer (por exemplo, queda nativa), a referência na CPU o vê e sai; o arquivo do pilar de uma rodada anterior no Nós nunca passa por desta rodada (se outro processo o segurar, ele fica no Nós, os erros vão ao registro do selo e o selo grava NOT_THIS_RUN; um marcador desta rodada o substitui; se nem o marcador puder ser gravado, o arquivo é REMOVIDO, com novas tentativas; e o SELO só hasheia o arquivo do pilar se ele for o que o runtime escreveu NESTA rodada — out_file_sha256, no registro —, senão grava NOT_THIS_RUN: mesmo com outro processo segurando o arquivo, o de outra rodada não passa por desta); se a cópia do resultado ao Nós falhar, a cadeia de custódia não fecha (CUSTODY_CHAIN_INCOMPLETE, nada ao cache); o result.json leva o sha256 de details.jsonl e de cpuref.json, que ficam na pasta da rodada (Nós/quantum_pillar/run_<data>_<marca>/) — a custódia leva essa pasta junto, e o conferidor da versão final confere os dois contra o disco
- o lançador do rito (ato da gerência) lê o estado de antes pela TAREFA «IALD Llama Server» e pelo processo (sonda vazia conta como «ligado»), RECUSA se o servidor estiver ligado sem a tarefa (não saberia religá-lo), encerra trabalhadores de rodadas mortas, arma a restauração ANTES de parar, para a tarefa e o supervisor, exige nenhum llama-server vivo e VRAM usada LEGÍVEL e ≤ 6 000 MiB (senão não roda), vigia contra o religamento durante o rito (o vigia sai se o lançador morrer, e em 8 h no máximo), e no fim — mesmo se o rito falhar ou o lançador receber TERM/HUP/INT, caso em que encerra primeiro a árvore do um.py — encerra o vigia e os trabalhadores restantes e religa a tarefa se o servidor estava ligado; recusa também com a tarefa DESABILITADA quando o servidor seria religado (e com a sonda dela ilegível); um sinal ANTES do rito só restaura (não toca o stdout da tentativa anterior), DURANTE encerra só a árvore do um.py desta rodada (os descendentes do lançador) e grava RITO_RC=SINAL_<x>, DEPOIS só restaura e devolve o código do rito; a restauração não é interrompida por sinal, espera o vigia sair sozinho (ele termina a parada que estiver fazendo; até 120 s) e espera até 60 s que nenhuma parada (Stop-ScheduledTask da tarefa ou stop_iald_llama.ps1) esteja em curso antes de religar (com AVISO no log se expirar; depois de um AVISO, o marcador só sai se a porta ainda escutar 30 s depois e nenhuma dessas paradas estiver em curso — com a contagem ilegível, o marcador fica); enquanto o servidor estiver parado pelo rito, um marcador com restaurar=0|1 fica no pacote, e a rodada seguinte restaura o que ele gravou (se não houver rodada seguinte, a memória da v384 manda a gerência conferi-lo); TERM é sempre capturado, INT/HUP não se o lançador for iniciado com & por shell não interativo ou com nohup (POSIX); o PID do lançador fica em .rito_v384.pid, gravado logo depois da guarda e removido em qualquer saída antecipada — armada a restauração, só no FIM dela (com outro lançador vivo, RECUSA — código 16), e abortar o rito é kill -TERM nesse PID NO GIT BASH, conferindo antes que /proc/<pid>/cmdline contém rito_v384 (é PID do MSYS, não do Windows; não no PowerShell) — o TaskStop da ferramenta da gerência NÃO para o lançador; a tentativa escreve num log próprio (.fase0; o de tentativas anteriores é ACRESCENTADO ao .fase0.anterior, com separador datado) e só depois da última recusa das guardas o registro dos sinais e o log real da rodada anterior vão para .anterior (nessa ordem) e o da tentativa toma o lugar do real (se um desses giros falhar, FALHA VISÍVEL e RECUSA — código 17); o log de uma tentativa recusada a partir da fase 0 (códigos 10 a 15 e as 17 dos giros: a dos sinais e a do log real vêm antes de o log real sair do lugar, porque os sinais giram primeiro; a da troca do .fase0 pelo log real vem depois, sem perda) fica no .fase0, e as recusas anteriores à fase 0 (6 a 9 e 16) e a 17 da guarda do próprio .fase0 só aparecem na saída do lançador; num sinal durante o rito, o encerramento da árvore do um.py é fail-closed (pelo PID nativo do subshell do rito; senão pelos descendentes do lançador com a data de criação conferida; senão FALHA VISIVEL no log e em rito_v384_sinal.txt)
- antes do artigo, o um.py espera o trabalhador, lê o resultado, confere o sha256, a marca da rodada e o β bit a bit, REDERIVA o veredito pela mesma árvore (num subprocesso com o mesmo código) e o escreve no core, no selo (registro próprio ao lado do gate; o resultado copiado para um_absoluto_pilar_quantico.json no Nós, com o hash na lista do selo) e no artigo (a introdução diz o que o código faz agora; uma nota diz o que se calcula na GPU e como, com os números da rodada); uma falha só no resumo ou no cache fica registrada SEM tocar o veredito
- prazo CONGELADO: execution.um_py_timeout_s = 18000 s desde o lançamento; passado, o um.py encerra a árvore do trabalhador e usa o resultado parcial (o que não rodou fica dito); a espera pela CPU é de até 1 h depois das fases da GPU; o ponto d = 128 só começa até 14400 s depois do início do trabalhador
- o pré-registro congelado mora em C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out\ (lugar permanente); o um.py embute o caminho e os sha256 e confere os arquivos em disco como INFORMAÇÃO; a cadeia de custódia do pilar se apoia na especificação EMBUTIDA, conferida pelo hash; o conferidor da versão final exige os arquivos em disco
- os autovalores não Hermitianos vão pelo MAGMA em TODO tamanho: o cuSOLVER padrão do PyTorch 2.11 derruba o processo de modo determinístico e dependente da matriz; o MAGMA não caiu em nenhum tamanho TESTADO — volume do ESTRESSE e da caracterização por tamanho do superoperador n = d²: {"16": 3000, "36": 3000, "64": 6000, "100": 2000, "144": 2000, "196": 1500, "256": 1300, "400": 600, "576": 400, "1024": 316, "4096": 5}; em n = 4 096, mais 9 chamadas nas sondas de tempo deste trabalhador (total 14); durabilidade do pipeline inteiro: {"pipeline_d8": 4000, "pipeline_d16": 1500, "t1_d8": 1500, "t1_d16": 500, "pipeline_d32": 150, "t1_d32": 60} (d ≤ 32); n = 16 384 (o D128) NUNCA foi testado, e uma queda ali lê-se D128_INTERRUPTED. No rito, d = 64 (n = 4 096) aparece em {"T2_pontos": 96, "T4": 100, "T1": 20, "T3_controles": 4}. A troca de backend (torch.backends.cuda.preferred_linalg_library) é marcada pelo PyTorch como «experimental feature» (aviso lido do estresse) e o backend MAGMA está em descontinuação: se o MAGMA sair, o trabalhador terá de ser revisto às claras (novo V1.x)

## O reaproveitamento (a ferramenta)

- a ferramenta pedida pelo operador em 03/10: chave = sha256(hash do trabalhador + especificação canônica + β em hexadecimal)[:24]; a chave NÃO inclui o ambiente: o ambiente (torch, CUDA, numpy, scipy, Python, GPU) é conferido à parte e, se diferir, recalcula; ao reaproveitar, o motor (E1..E8) roda de novo no ambiente presente
- rodada completa (sem TGL_RITE_CHECKPOINT): calcula sempre e, só se o resultado for COMPLETO (o ramo 9 da árvore, sem parcial, com a cadeia conferida E com o D128 RODADO), GRAVA em cache/checkpoints/quantum_pillar/<chave>/ — prazo, memória, recusa, fase falhada ou D128 não rodado nunca vão ao cache (a razão fica em not_cached_code e no artigo); uma falha ao gravar o cache fica registrada sem tocar o veredito, e o cache antigo volta ao lugar
- rodada intermediária (TGL_RITE_CHECKPOINT=1, o interruptor do v321): se houver resultado gravado com a mesma chave, o mesmo ambiente, o sha256 conferido e o motor aprovado agora, REAPROVEITA sem a GPU; senão calcula; numa rodada reaproveitada, o run_dir do registro aponta para o CACHE, que a rodada completa seguinte com a mesma chave substitui — por isso o selo de uma intermediária não vai à custódia
- o artigo e o selo dizem qual foi; a versão final, a que vai à custódia, roda sem a chave, sempre — o conferidor da versão final e a custódia recusam um selo com o pilar reaproveitado

## Estatuto

- [COMPUTED]: cálculo do sistema aberto da teoria; nada aqui é medição da natureza
- selo próprio AO LADO do gate; o gate não muda
- não falsificado nunca é confirmado; provada não é confirmada; a guarda das três palavras proibidas da casa vale para este texto e para todo veredito do pilar
- [DECLARADO — leitura do operador, 02/10] o resgate da RG é a prova cosmológica; [ONTO] o pilar quântico é a face matricial do mesmo sistema

## O desvio do plano B (declarado; ratificação: PENDENTE)

| | plano B | esta especificação (B_AMPLIADO_D64) |
|---|---|---|
| T1 (injeções por d) | {'8': 2000, '16': 2000, '32': 1000, '64': 100} | {'8': 2000, '16': 1000, '32': 200, '64': 20} |
| T4 (instâncias por d) | {'8': 20000, '16': 5000, '32': 1000, '64': 100} | {'8': 15000, '16': 5000, '32': 1000, '64': 100} |
| T2 em d = 64 (pontos) | 96 | 96 |
| prazo de início do D128 (s) | — | 14400 |
| estimativa com os custos medidos agora (min) | 279.7 (349.6 com margem; cabe em 5 h: NÃO) | 169.3 (211.6 com margem) |

três causas medidas: (1) o plano B (planejar_carga_v384.json, 03/10) estimava a injeção do T1 em d = 64 em 3.4 s; com o gerador inteiro e o certificado do ramo ela custa 57 s; (2) o cuSOLVER padrão derruba o processo (achado de 03/10, mapa seq 312-314) e o MAGMA, o único estável, custa em d = 64 23.0 s por instância (o plano B contava 9.9 s); (3) com a sonda deste trabalhador, o plano B inteiro levaria cerca de 280 min (350 com a margem): o D128 só começaria, com a margem, se o prazo de início fosse de pelo menos 326 min (o desta especificação é 240), e então terminaria por volta de 350 min, FORA das 5 h; com as outras 5 sondas válidas (versões anteriores do trabalhador, o mesmo caminho de cálculo do tempo), o plano B com a margem iria de 289 a 337 min, ACIMA das 5 h em 4 delas; a maior folga entre as sondas que cabem é de 4% das 5 h, MENOR que a dispersão (a dispersão entre as sondas é de 24% na instância de d = 64). Por isso, e não por uma medida única, o T1 de d = 64 fica reduzido (20 injeções contra 100 do plano B), e a estatística forte do T1 fica em d <= 32; e mesmo SEM margem, as fases do plano B antes do D128 levam cerca de 261 min, ACIMA do prazo de início desta especificação (240 min): o D128 não rodaria. O T1 também foi cortado em d = 16 (2000 -> 1000) e d = 32 (1000 -> 200): restaurá-lo custa cerca de 35.8 min a mais; o limite a 95% de d = 32 muda de 0.3% (o valor apresentado ao operador no nível B) para 1.5%. O T4 em d = 8 fica em 15000 (plano B: 20000).

**Alternativa B_AMPLIADO_D64 (escolha do operador; não é o «nível A» de 03/10 (o leve, ~40 min): é a variante MAIS PESADA que o B_REDUZIDO):** {"T1_d64": 20, "T1_ruido_d64": 3, "T4_d64": 100, "T2_gamma_d64": 32}, prazo de início do D128 14400 s — cerca de 67.8 min a mais de GPU (84.7 com margem); antes do D128, com margem: 188.3 min. o B_AMPLIADO_D64 restaura o T4 (100) e o T2 (96 pontos) de d = 64 do plano B; o T1 de d = 64 vai a 20 (plano B: 100) com 3 no ruído; com a margem ×1,25 as fases antes do D128 levariam cerca de 188.3 min, ACIMA do prazo de início de 180 min (o D128 não rodaria); por folga, o B_AMPLIADO_D64 sobe esse prazo para 240 min (D128_start_deadline_s = 14400), e o D128 ainda termina antes das 5 h do um.py (sim); estatística de d = 64 mais forte, rito mais longo; escolha do operador

Limites de falha a 95% se nenhuma falhar (%): regra de três (conservadora) — T1 {'8': 0.15, '16': 0.3, '32': 1.5, '64': 15.0}; T4 {'8': 0.02, '16': 0.06, '32': 0.3, '64': 3.0}. Exato (1 − 0,05^{1/n}) — T1 {'8': 0.15, '16': 0.299, '32': 1.487, '64': 13.911}; T4 {'8': 0.02, '16': 0.06, '32': 0.299, '64': 2.951}.

## Orçamento estimado [DERIVED]

| teste | minutos |
|---|---|
| T4 | 66.4 |
| T2 | 40.2 |
| T1 | 41.1 |
| T3 | 3.0 |
| D128 | 18.6 |
| **total** | **169.3** (com margem ×1.25: **211.6**) |

Antes do D128, com margem: 188.3 min; prazo de início do D128: 240.0 min (começa no prazo mesmo com a margem: sim; termina antes do prazo do um.py: sim).

estimativa [DERIVED]: sonda do proprio trabalhador com operadores ALEATORIOS (so hardware); d = 128 por escala n^3; a margem x1,25 NAO foi medida sob a carga do rito (estimativa); a ordem no trabalhador e' T3, T2, T1, T4, a espera pela CPU (ate 3600 s DEPOIS das fases da GPU; o filho corre desde o inicio, em paralelo) e por ultimo o D128; a espera so pesa se a CPU nao tiver terminado, o que a sonda nao preve; fonte: result.json (sha256 525734bc095c3c13; trabalhador 0c9ba7fd45e78317)

Variabilidade das sondas de tempo (a lista: d = 64, s por instância / por injeção do T1; a nota por d e por custo cobre d = 8 a 64): teste_tempo_v4 (trabalhador cec9b0c16268e685): 22.11 / 55.86; teste_tempo_v5 (trabalhador 569c6eb422fe78d3): 21.52 / 51.05; teste_tempo_v6 (trabalhador b3bdecab06c18006): 20.93 / 52.25; teste_tempo_v7 (trabalhador 39e6d56004fe2813): 20.91 / 51.91; teste_tempo_v8 (trabalhador fb974f9d34c216b5): 18.5 / 45.33; teste_tempo_v9 (trabalhador 0c9ba7fd45e78317): 23.01 / 57.31 — faixa da instância: 18.5 a 23.01 s. criterio: as pastas teste_tempo_v* do pacote com d = 64 medido em reps >= 3 (a mediana); fora do criterio: teste_tempo (fora do criterio (pastas teste_tempo_v*, d = 64 com reps >= 3, a mediana): reps 1), teste_tempo_final (fora do criterio (pastas teste_tempo_v*, d = 64 com reps >= 3, a mediana): reps 1), teste_tempo_magma (fora do criterio (pastas teste_tempo_v*, d = 64 com reps >= 3, a mediana): reps 1); o orcamento usa SO a sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos caminhos de calculo do tempo) e mostram a dispersao entre rodadas: em d = 64, a maior sonda sobre a corrente da 1.000 (instancia) e 1.000 (injecao do T1), e a maior sobre a menor da 1.244 (instancia) -- ali, a margem x1.25 cobre a maior sobre a corrente (instancia e injecao do T1) e cobre a dispersao maior/menor da INSTANCIA (os outros pontos e custos: a nota por d e por custo); nao foi medida sob a carga do rito. Por d e por custo (instancia, injecao do T1, nivel extra de ruido do T1; 6 sondas): a maior sonda sobre a corrente vai ate 1.089 (d = 8, injecao do T1) -- a margem x1.25 cobre a maior sobre a corrente em todo d e custo; a sonda corrente e' a mais lenta de todas em d = 32, 64; a maior sobre a menor passa da margem em d = 32 instancia (1.323), d = 64 injecao do T1 (1.264) -- nesses pontos a margem NAO cobre a dispersao entre rodadas; neles a sonda corrente e' a mais lenta medida, e o orcamento (a corrente x1.25) cobre uma rodada ate 25% mais lenta que ela, nao mais.

## O motor

- trabalhador `pilar_quantico_worker.py`, sha256 `0c9ba7fd45e78317a915bb718b11127a0dae9872e48ab430f0600b74ca26452f`, 1276 linhas
- autoteste E1..E8 (`result.json`, sha256 `c74fcf3b60ae4a9e3b817d8af8f0d5eb7a926a114fdc70af47334aee975a6fe1`): E1_amplitude_damping_spectrum_and_ground_state ok, E2_pure_dephasing_detected_degenerate ok, E3_root_law_rates_exact ok, E4_blind_estimator_recovers_root_law ok, E5_thermal_qubit_gibbs_and_spohn_monotone ok, E6_time_reversal_not_cp_forward_cp_tp ok, E7_estimator_floor_below_one_tenth_of_the_criterion ok, E8_cpu_reference_comparator_selftest ok
- piso do estimador (E7): {"n": 6000, "max_beta_rel_err": 3.6970426720017713e-13, "max_abs_p_err": 2.0239365738916604e-13, "limit_beta": 1e-07, "limit_p": 1e-05}
- o código do trabalhador entra no um.py v384 byte a byte e o seu hash está DENTRO da especificação congelada; se mudar, sai um V1.x novo deste pré-registro

## A aferição

1ª passada do aferidor (03/10): 17 achados, todos acolhidos (o que foi superado depois está dito ao lado); 2ª passada: 48 achados sobreviventes à verificação adversarial — a 3ª passada mediu 32 resolvidos, 13 parciais e 3 regressões (uma mesma frase do artigo); 3ª passada: 37 achados novos, 37 sobreviventes à verificação (com duplicatas entre as lentes); os parciais, as regressões e os novos foram tratados no código ou no texto antes deste documento; 4ª passada (conferência das correções da 3ª): 55 entradas (item × lente) — 42 resolvidas, 10 parciais e 3 regressões; por item, pelo pior estado, 13 de 50 ainda pediam correção; 26 achados novos, 25 sobreviventes à verificação (9 deles repetem outro achado ou item; quase todos de severidade baixa); tratados no código ou no texto antes deste documento; 5ª passada (conferência das correções da 4ª): 40 entradas (item × lente) — 28 resolvidas, 11 parciais e 1 regressão; 23 achados novos (8 deles repetem outro achado ou item), SEM a verificação adversarial na própria passada (a sessão do verificador expirou), todos tratados no código ou no texto antes deste documento; a 6ª passada confere as correções e verifica esses achados; 6ª passada (conferência das correções da 5ª e verificação dos seus achados novos): 37 entradas — 34 resolvidas e 3 parciais; 26 achados novos, 26 sobreviventes à verificação (8 deles repetem outro achado ou item; 9 pela contagem corrigida na 7ª; quatro de severidade média, lidos dos veredictos), tratados no código ou no texto antes deste documento; e uma ERRATA da gerência ao lado: uma edição da 5ª no lançador foi feita por um script não salvo, com o diff registrado; 7ª passada (as correções da 6ª): 29 entradas — 20 resolvidas, 8 parciais e 1 regressão (a comparação do V1 com o rascunho, que recusava todo congelamento); 22 achados novos, 22 sobreviventes à verificação (10 repetem outro achado ou item; severidades: ALTO 2, BAIXO 18, MEDIO 2), tratados no código ou no texto antes deste documento; o caminho do congelamento foi TESTADO numa pasta de teste com transcrito sintético (5 de 5 casos como esperado); e duas ERRATAS da gerência ao lado (a edição manual da 5ª tinha quatro trocas; uma gravação das disposições na 6ª foi por script não salvo, com o diff registrado); 8ª passada (as correções da 7ª): 30 entradas — 27 resolvidas e 3 parciais; 19 achados novos, 19 sobreviventes à verificação (4 repetem outro achado ou item; severidades: BAIXO 19), tratados no código ou no texto antes deste documento; o teste do congelamento ganhou o caso da sonda do mesmo trabalhador e os casos da grafia equivalente da pasta permanente (8 de 8 casos como esperado); e, AO LADO: na 7ª, «com transcrito sintético» lê-se «com uma cópia do transcrito real e uma mensagem sintética acrescentada», e a primeira execução daquele teste FALHOU (cópia acima de 260 caracteres), o que mudou o nome das cópias das evidências; uma evidência da 6ª (o diff da gravação inline) foi regerada dos bytes; 9ª passada (as correções da 8ª): 22 entradas — 20 resolvidas e 2 parciais; 17 achados novos, 17 sobreviventes à verificação (5 repetem outro achado ou item; severidades: BAIXO 17), tratados no código ou no texto antes deste documento; o teste do congelamento (8 de 8 casos como esperado) e um teste novo dos órfãos de uma tentativa interrompida (3 de 3); e, AO LADO: no trecho da 6ª, o número da 6ª restaurado («8 deles repetem…») com o da 7ª ao lado («9 pela contagem corrigida na 7ª»); ERRATA AO LADO da 9ª: dois dos três casos dos órfãos (O2, O3) foram recusados pela guarda do V1 já existente, não pela guarda nova das evidências, que só se alcança com o V1 igual (relógio fixo); 10ª passada (estreita, as correções da 9ª): 19 entradas — 18 resolvidas e 1 regressão (a recusa 17 do giro dos sinais vinha depois do giro do log real; corrigida: os sinais giram primeiro); 8 achados novos, 8 sobreviventes à verificação (2 repetem outro achado ou item; severidades: BAIXO 8; 3 tocavam o texto deste rascunho), tratados no código ou no texto antes deste documento; o caso que a gerência não alcançou (o V1 igual com a pasta de evidências adulterada) foi refeito pela aferição com relógio fixo: recusa sem mover nada; 11ª verificação (estreita, um verificador independente sobre as frases que mudaram do rascunho v11 ao v12): tudo o que mudou confere (números e hashes); duas imprecisões de redação no texto do lançador e duas de registro, todas de severidade baixa, tratadas antes deste documento (disposições achado a achado em disposicoes_afericoes_v384.json, sha256 7fcb71013fa79e87; registro verbatim em AFERIDOR_v384.txt, sha256 6ad22b44d3a28319)

## As evidências (caminho e sha256)

- **sonda_de_tempo**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_tempo_v9\result.json` — `525734bc095c3c139263ddcf767cc3b57a3f23f7d3c0f73d45d2e92e1663d32c`
- **autoteste_do_motor**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_motor_v8\result.json` — `c74fcf3b60ae4a9e3b817d8af8f0d5eb7a926a114fdc70af47334aee975a6fe1`
- **plano_B**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\planejar_carga_v384.json` — `9d1d2c3095d2121817c62065acfcc47b24f5919e02660bf4cb3aa0586c45f3af`
- **afericao_2**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao2_resultado.json` — `081e97bc1d18d835a3c0bd5cdb757e4ab494d29fc70072d5b33b1dcec853a104`
- **afericao_3**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao3_resultado.json` — `a4dc51810d510ac70a06fdc0167c1051e582c8e2f41c9f28470cb48c68aaaba7`
- **afericao_4**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao4_resultado.json` — `602c594b9c80ed1ba1bd3b58fff618fb2d3cc5972fbbc3e59ed0c4f9cab360f6`
- **afericao_5**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao5_resultado.json` — `fa914a9f39299858e905e828f5fca573688f861ce68b333524f7d43227181ce1`
- **disposicoes**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\disposicoes_afericoes_v384.json` — `7fcb71013fa79e872ec5bd9f577c4095bcc3500d588c62d9b48f9ee41db7f209`
- **afericao_6**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao6_resultado.json` — `8ca130de5c616558a593b158f9f4850a14455d6f1ee45c3eb0573319cb058e6a`
- **afericao_7**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao7_resultado.json` — `2c7073a1380c29edb06093043aa3eb9226cdce5766f0399ff6a19febf3fa1b25`
- **afericao_8**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao8_resultado.json` — `b33ecee98d0c1613572c177fdafca8e25964c5de8981c19913277de3ab178c27`
- **afericao_9**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao9_resultado.json` — `788f79e52c71e01ba6d5cdf582359ecc02873a71df0e0f3da361e8e845b8ee0d`
- **afericao_10**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\afericao10_resultado.json` — `83d6405c943568643ef084c985bfbc9ff7afbdfd3ef81e6045e435ccd12c257a`
- **aferidor_verbatim**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\AFERIDOR_v384.txt` — `6ad22b44d3a28319957d41a278fab80966bd4759156b138a41e56d92d76688b7`
- **estresse_pequeno**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\estresse_eig.json` — `9ec8d704a3683aa7b2297efbfa1cb3377e3891b1bd0ffdfeb281c587bfa8ceb4`
- **estresse_grande**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\estresse_eig_grande.json` — `11ec67354dd46a53e7b6d8aac2e8bbaf2bd67be9f6f61c6ea8f171e1a844be63`
- **estresse_caracterizacao**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\caracterizar_queda_cusolver.json` — `00e4daef8526cab30fd642bc586122c322fd3a88411221b640d1fd08639023d1`
- **estresse_variantes**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\variantes_cusolver.json` — `65118c79fa13b297028b54dccb2dea69f97c299fc2347acbe16aed667279da98`
- **estresse_durabilidade**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\durabilidade_pipeline.json` — `6387377c07a28747ecf7f193cc6e4dbe479e6afde36d4d4bd16e9d9c5ecb4ac6`
- **variabilidade_teste_tempo_v4**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_tempo_v4\result.json` — `ad95bf8d07f3eebd612385be70324d1b08ff1058c0a022b413f33eae201108f6`
- **variabilidade_teste_tempo_v5**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_tempo_v5\result.json` — `982bbc8984253881c7dc6120b968e90b330c3dfacd6c137d99c8d08a94f98109`
- **variabilidade_teste_tempo_v6**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_tempo_v6\result.json` — `0dcd4fd21664bc97754d037934d9f4ffe1ce517fb7edaba8566cdc23ff544609`
- **variabilidade_teste_tempo_v7**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_tempo_v7\result.json` — `ec73eae25337e85c1fed3cfa0d2c428bedacbe8e9221015e513b5bcb93cf084f`
- **variabilidade_teste_tempo_v8**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\teste_tempo_v8\result.json` — `285668632af459e1ec809b174e617f4c38fc399a4959265ca17016452bb21645`

## O estresse dos autovalores (a escolha da biblioteca)

o cuSOLVER (o padrão) caiu com violação de acesso (3221225477) em 8 de 9 tamanhos de 16 a 576, de modo DETERMINÍSTICO e dependente da matriz (a mesma semente cai na mesma chamada com ou sem determinismo, sincronização ou cache limpo); o MAGMA fez 16500 chamadas na caracterização sem queda; a durabilidade do pipeline inteiro com o MAGMA: 7710 instâncias de operadores aleatórios, d de 8 a 32, sem queda; volume do MAGMA no estresse e na caracterização, por n (sem as sondas de tempo): {"16": 3000, "36": 3000, "64": 6000, "100": 2000, "144": 2000, "196": 1500, "256": 1300, "400": 600, "576": 400, "1024": 316, "4096": 5}

```json
{
 "pequeno": {
  "arquivo": "estresse_eig.json",
  "sha256": "9ec8d704a3683aa7b2297efbfa1cb3377e3891b1bd0ffdfeb281c587bfa8ceb4"
 },
 "grande": {
  "arquivo": "estresse_eig_grande.json",
  "sha256": "11ec67354dd46a53e7b6d8aac2e8bbaf2bd67be9f6f61c6ea8f171e1a844be63"
 },
 "caracterizacao": {
  "arquivo": "caracterizar_queda_cusolver.json",
  "sha256": "00e4daef8526cab30fd642bc586122c322fd3a88411221b640d1fd08639023d1"
 },
 "variantes": {
  "arquivo": "variantes_cusolver.json",
  "sha256": "65118c79fa13b297028b54dccb2dea69f97c299fc2347acbe16aed667279da98"
 },
 "durabilidade": {
  "arquivo": "durabilidade_pipeline.json",
  "sha256": "6387377c07a28747ecf7f193cc6e4dbe479e6afde36d4d4bd16e9d9c5ecb4ac6"
 },
 "plano_B": {
  "arquivo": "planejar_carga_v384.json",
  "sha256": "9d1d2c3095d2121817c62065acfcc47b24f5919e02660bf4cb3aa0586c45f3af"
 }
}
```

## A especificação de máquina

```json
{
 "id": "TGL_QUANTUM_PILLAR_V1",
 "worker_sha256": "0c9ba7fd45e78317a915bb718b11127a0dae9872e48ab430f0600b74ca26452f",
 "seed": 20261003,
 "dtype": "complex128",
 "eps_H": 5.0,
 "linalg": {
  "nonhermitian_eig_backend": {
   "magma_up_to_n": 1000000000
  },
  "nota": "autovalores nao Hermitianos pelo MAGMA em TODO tamanho: o cuSOLVER padrao do PyTorch 2.11 derruba o processo de modo deterministico e dependente da matriz (8 de 9 tamanhos de 16 a 576); o MAGMA nao caiu em nenhum tamanho TESTADO (n <= 1024 em volume; n = 4096 com 14 chamadas: 5 no estresse e 9 nas sondas de tempo deste trabalhador; n = 16384 nunca); a troca de backend (torch.backends.cuda.preferred_linalg_library) e' marcada pelo PyTorch como experimental; o backend MAGMA esta em descontinuacao"
 },
 "operators": {
  "reh_amp": 0.5,
  "reh_decay": 0.2,
  "reh_gamma": 1.0,
  "cons_amp": 0.3,
  "cons_decay": 0.3,
  "cons_gamma": 2.0,
  "diss_amp": 0.5,
  "diss_decay": 0.2,
  "prune_gamma": 0.5,
  "anti_gamma": 1.0,
  "k0": 1.0,
  "k1": 0.1
 },
 "tolerances": {
  "engine": 1e-09,
  "tol0_rel": 1e-10,
  "gap_rel": 1e-08,
  "cp": 1e-09,
  "tp": 1e-09,
  "psd": 1e-10,
  "ss_res": 1e-08,
  "spohn_abs": 1e-10,
  "spohn_rel": 1e-09,
  "identity_abs": 1e-12,
  "identity_rel": 1e-12,
  "ccp_rel": 1e-09
 },
 "execution": {
  "um_py_timeout_s": 18000,
  "progress_every_s": 300,
  "priority": "BELOW_NORMAL",
  "out_dir": "nova por rodada, com marca unica (run_id)"
 },
 "T2": {
  "d": [
   8,
   16,
   32,
   64
  ],
  "nc": [
   2,
   3,
   4
  ],
  "gamma_lo": 0.0001,
  "gamma_hi": 100.0,
  "n_gamma": {
   "8": 64,
   "16": 64,
   "32": 64,
   "64": 32
  },
  "dt": 0.05,
  "steps": 64,
  "cci_half": 0.5,
  "folds_window": {
   "c1": [
    2.5,
    3.5
   ],
   "c2": [
    1.5,
    2.5
   ]
  }
 },
 "T1": {
  "d_counts": {
   "8": 2000,
   "16": 1000,
   "32": 200,
   "64": 20
  },
  "noise_subset": {
   "8": 200,
   "16": 100,
   "32": 20,
   "64": 3
  },
  "nc": [
   2,
   3,
   4
  ],
  "beta_log_range": [
   -4,
   -1
  ],
  "k_range": [
   0.5,
   2.5
  ],
  "gamma_diss_log_range": [
   -3,
   1
  ],
  "tau": 0.05,
  "branch_dev_sigma0": 1e-06,
  "branch_dev_noisy": 0.001,
  "noise": [
   0.0,
   1e-10,
   1e-08
  ],
  "pass": {
   "0.0": {
    "beta_rel": 1e-06,
    "p_abs": 0.0001,
    "min_frac": 1.0
   },
   "1e-10": {
    "beta_rel": 0.05,
    "p_abs": 0.05,
    "min_frac": null
   },
   "1e-08": {
    "beta_rel": 0.05,
    "p_abs": 0.05,
    "min_frac": null
   }
  }
 },
 "T3": {
  "d": [
   8,
   16,
   32,
   64
  ],
  "nc": 3,
  "gamma_diss": 0.1,
  "tau_N4": 0.001,
  "tau_N5": 0.05,
  "N3_counts": {
   "8": 200,
   "16": 100,
   "32": 20
  }
 },
 "T4": {
  "d_counts": {
   "8": 15000,
   "16": 5000,
   "32": 1000,
   "64": 100
  },
  "nc": [
   2,
   3,
   4
  ],
  "dt": 0.05,
  "steps": 64
 },
 "D128": {
  "d": 128,
  "nc": 3,
  "gamma_diss": 1.0,
  "rk4_dt": 0.002,
  "rk4_steps": 5000,
  "start_deadline_s": 14400
 },
 "cpuref": {
  "d_all": [
   8,
   16
  ],
  "d_pick": {
   "32": [
    [
     3,
     0
    ],
    [
     3,
     16
    ],
    [
     3,
     32
    ],
    [
     3,
     48
    ],
    [
     3,
     63
    ],
    [
     2,
     32
    ],
    [
     4,
     32
    ]
   ],
   "64": [
    [
     3,
     6
    ]
   ]
  },
  "tol": {
   "cci": 1e-09,
   "purity": 1e-09,
   "folds_n_c1": 1e-09,
   "gap_rel_rel": 1e-06,
   "choi_min": 1e-09,
   "min_gap_rel_for_compare": 1e-06
  },
  "timeout_s": 3600
 }
}
```

