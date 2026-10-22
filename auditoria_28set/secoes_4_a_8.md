## 4. A investigação na Bancada Um

**Pré-registro antes do dado.** `C:\IALD\Bancada_Um\investigacao\PREREGISTRO_INV_BANCADA_UM_20260928.json` (sha256 `1447aab21973af41…`),
carimbado no Mapa de Rotas (seq 63) antes de qualquer dado novo. Declarado **NÃO-CEGO**: o DR2 já tinha sido usado no programa e pela bancada
oficial. **Desvio dito:** a ordem executada foi P2 → P1 → S2 → S1 → D1 (a listada era P1 → P2 → D1 → S1 → S2); os resultados não dependem da
ordem.

**Sem dado real.** O ajustador vetorizado bate com o scipy a 1,3×10⁻⁵ σ. Injeção e recuperação (1000 + 1000): viés ≤ 0,04σ, desvio do pull
0,98–1,01, cobertura 66–69% e 95%. O estimador é honesto. A previsão de Fisher reproduz o σ da V3 selada (0,00827 contra 0,00823).

**Com dado real (Planck comprimido + DESI DR2 com covariância completa).** O posterior primário, bem convergido (62 τ, ~31.800 amostras
efetivas), dá **β = −0,01348 ± 0,00630** (z_TGL = −4,05; z_0 = −2,14). A comparação P2 dá Δχ² = 16,05 (4,0σ, Wilks), o jackknife mostra um
puxão amplo (nenhuma medida sozinha move β mais que 0,36σ), e com SH0ES fica β = −0,0077 ± 0,0063. A implementação do DR2 foi conferida contra o
executor independente da bancada oficial: χ² = 28,69347 nos dois.

**A leitura mudou no mesmo dia, e isso fica dito.** Eu tinha lido o resultado como «TENSAO_FORTE» e escrito que «quem limita β é o CMB». A
auditoria (D1F-02) apontou, e eu conferi de forma independente (M1), que essa sensibilidade depende de como o Ω_m entra no parâmetro R do Planck
comprimido:

| Planck comprimido + BAO | mapa de R | β̂ | σ(β) | α√e a | β_TGL/σ |
|---|---|---|---|---|---|
| DR2 | Ω_m nu (o da V3 e da Bancada) | −0,0137 | 0,0063 | 4,01σ | 1,90 |
| DR2 | Ω_m efetivo (1+β)Ω_m | +0,050 (borda do prior) | 0,0615 | 0,87σ | 0,20 |
| DR1 | Ω_m nu | −0,0130 | 0,0082 | 3,01σ (= selado) | 1,46 |
| DR1 | Ω_m efetivo | +0,050 (borda) | 0,0879 | 0,84σ | 0,14 |

Os números calculados não mudam. Muda a leitura: **a rota comprimida não decide β.** Os 3,01σ selados e os 4,0σ de hoje são condicionais a uma
escolha `[INPUT]` não derivada. A errata foi posta ao lado no mapa, no Atlas e nas memórias.

**A observação do sinal, com o estatuto certo.** Com o Ω_m nu, o módulo |β̂| fica a 0,23σ de α√e, com o sinal oposto, e o core já registrava o
mesmo padrão na V3 (a 0,087σ do «ramo da face do estado»). É **observação, não teste**: a orientação não foi derivada, o ramo foi nomeado depois
do dado, o DR2 já tinha sido olhado, e a observação depende do mesmo mapa de R.

## 5. O POA e onde buscar indício forte

O POA do artigo *Haja Luz* (§sec:poa) tem três passos. Usei o **POA-2** (os domínios) como lista de busca. O **POA-3** («diferenças que não
refutem» contam como consistência) não serve como critério de teste: é de não-refutação, e aqui vale a régua de sempre.

| domínio (POA-2) | previsão da TGL no programa | o que o teste de hoje pode decidir | caminho para indício forte |
|---|---|---|---|
| **Ondas gravitacionais** | eco √β; ringdown (ramo A = t_Planck; ramo B = [INPUT]) | nada: ramo A invisível por construção; ramo B efetivo ≈ −0,005 por realização (poder ~0,04σ); eco com atraso travado e amplitude √β em conflito com a tipagem da v372 | a QG fechada prevê a RG: registrar por citação a correspondência (c_gw, massa do gráviton, polarizações, ringdown/no-hair, teorema da área). No ringdown, o modo 221, não o 440 |
| **Lentes** | piso dos vazios em matéria (κ, shear) | nada: o Fisher V9 é zero por construção; a emenda V10, que corrige isso, nunca rodou; o shear está 10⁷ vezes aquém | executar a V10 com uma família de perfis admissível e um estimador de mínimo por vazio em matéria |
| **CMB** | β no fundo (Φ_total) | nada de decisivo: com um mapa de R há 4σ, com o outro não há sensibilidade; o espectro completo (Nível 2 S) dá σ(β) ≈ 0,018 | **derivar antes** o mapa de R e a orientação do sinal; depois o espectro completo com a TGL no código de Boltzmann; com o CMB da era do CMB-S4 |
| **CMB: não-gaussianidade e fractalidade** | nenhuma previsão quantificada (Atlas, selo e mapa: 0) | nada | derivar uma previsão antes de buscar |
| **Grande escala: homogeneidade e redes auto-similares** | nenhuma previsão quantificada | nada | idem |
| **Grande escala: vazios (V11)** | piso de traçador | só consistência unilateral: não há desfecho FALSIFIED, e o ΛCDM passa | o mínimo por vazio em matéria (via lentes) |
| **Outros** | relógios (12,5 ordens aquém), dephasing (10 ordens), neutrino m₂ (na borda de 3σ, dependente da entrada), NMC-Shapiro (atraso literal de 50 ms, sem β), Coma (já revelado, não cego) | pouco | citar a fonte do neutrino; derivar a lei de escala do NMC-Shapiro antes do dado |

**A resposta direta à sua pergunta:** hoje não há rota que dê indício forte de β. O que a Bancada mostrou é onde está a alavanca e o que falta
antes dela: **a teoria tem de dizer, antes do dado, como a modificação entra na física do CMB** (o mapa de R e a orientação). Sem isso, qualquer
número de fundo é condicional. E há um teste com a natureza que se pode fazer hoje: **o da QG fechada**, a recuperação da RG, por citação.

## 6. Correções propostas para a v376 (nada instalado; aguardam os seus testes profundos)

**A. Leituras e nomes: errata ao lado, sem mover bandeira nem número.**
1. Gate: qualificar o degrau experimental (canal unilateral de traçador, sem desfecho FALSIFIED, o ΛCDM também passa); renomear as bandeiras
   (não há mocks; as quatro são um booleano). E dizer que o teste com a natureza da implicação fechada é a recuperação da RG.
2. V11: «POWERED» significa poder de ver supressão, não de falsificar.
3. Ringdown: fixar por escrito o que ele pode decidir (no ramo canônico, só a correspondência com a RG) antes de inseri-lo como condição.
4. Eco: «AMPLITUDE_SQRT_BETA_FROM_KERNEL» sobreafirma; a amplitude sob a tipagem da v372 é 0,218 ou β, não √β; a lei KMS usa um período de
   tempo imaginário como atraso real (os dois regimes).
5. Coma: o selo diz «aguardando revelação» de uma previsão já revelada; o hash da previsão inclui o carimbo de hora.
6. Neutrino: citar a fonte do ajuste global e declarar que o veredito depende da entrada (2,44–3,22σ).
7. O selo carrega a conjunta V1 e o D1 V1 superados, sem a V3 ao lado; a string v200 do dephasing sem a errata v369; a premissa do escape de
   Weinberg–Witten («gráviton = I = gerador») foi negada pela v372.
8. D1 V3: «TENSION» e «3,01σ» condicionais ao mapa de R `[INPUT]`.

**B. Métodos: para a próxima rodada de cada rito, pré-registrada.**
9. D1: correlações DM–DH do DR1; a covariância do Planck como publicada por Chen+2019 (e a citação correta); l_A com r_s coerente; o mapa de R e
   a orientação derivados antes; DR2; espectro completo.
10. Eco ancorado: atraso por evento com incerteza de massa e spin; executar os nulos pré-registrados; σ estimado on-source. PE: a regra de borda
    também para a amplitude.
11. Ringdown: previsão efetiva por realização, calibrada por injeção de difusão de fase; incerteza do catálogo no σ; H1 e L1 em bloco; a
    sistemática nas mesmas séries (a V2 só passa pela regra afrouxada).
12. κ V6–V9: um teste de nulo que não seja tautológico. V10: executar. V12: ordenar a profundidade por estatística independente.
13. Conjunta: χ² conjunto ou Fisher, grupos de dependência (o Planck é compartilhado), correção de multiplicidade.
14. Máquina do veredito final: incluir o D1 V3, o neutrino e a conjunta V3; os canais l_A e Pantheon com o worker corrigido e a forma de fundo
    ratificada; `_is_refuted` reconhecendo EXCLUDED e lendo `verdict_v369`.
15. `READ_BY_HASH`: calcular o hash dos BYTES (em arquivo CRLF o sha16 gravado hoje é do texto traduzido).
16. Fator de tentativas entre famílias, com o Mapa de Rotas como contador.
17. NMC-Shapiro: a lei de escala Δt(β, potencial) antes do dado, trocando o signo α2.
18. Um rito «por citação» da recuperação da RG.

**C. Na Bancada Um (casa da gerência):** oferecer como opções declaradas a covariância do Planck de Chen+2019, o DM_* por razão sobre o CAMB (o
neutrino massivo contado uma vez só), as correlações do DR1, os dois mapas de R e o Pantheon+ com a covariância que existe em disco, mantendo a
«reprodução do selado» como modo de conferência. A Bancada herda hoje os defeitos da V3, e isso está dito ao lado no README, na memória e no mapa.

**E. O que a auditoria não cobriu, e a próxima rodada (crítico de completude).** As lacunas viraram rotas PROPOSTA no Mapa de Rotas. Por
ordem do crítico:
1. **Decidir e pré-registrar o mapa de R e a orientação do sinal antes de qualquer dado**, e recomputar o D1 V3 numa só conta com todas as
   correções juntas (DR1 correlacionado, covariância de Chen, l_A coerente, neutrino massivo uma vez). Hoje cada correção foi medida sozinha, e
   o rito está no limiar: a combinação pode trocar TENSION por INCONCLUSIVE.
2. **O canal N_eff e o ρ+p**: as tensões são literais de sessão no código (`um.py:4804-4805`), e o canal pode medir a mesma física que o D1 (β age
   como ΔN_eff), sem grupo de dependência.
3. **A cadeia do piso v78 → v92**: conferir se a emenda V4.1 (o primeiro POWERED) foi escrita depois de o sinal da v91 ser aberto, o mesmo
   padrão já achado na V11.1.
4. **`the_truth_is_in_the_contour`** («nenhum rival se conforma em todos os domínios»): a tabela escolhe os domínios, e o ΛCDM se conforma em
   pelo menos quatro. Auditar junto com a máquina do veredito final, como um único defeito de seleção de canais.
5. Neutrino (fixar a entrada, com citação e data), ecos (tipar a amplitude antes dos nulos), ringdown (fixar por injeção o valor esperado do
   ramo B) e gate (reconciliar a contagem de bandeiras, que aparece como 18, 15 e 11).
6. Famílias novas: laboratório e forma de α; Grande Atrator e Chandrasekhar; o Evento 2 α-livre e o MCMC-CRUZ do artigo público.

E uma memória que envelheceu: o `CLAUDE.md` da raiz ainda chamava de «evidência primária [REAL]» a convergência de β com «BBN 0,0σ», que o
próprio core reclassificou. A errata foi posta ao lado.

**D. Erros meus de hoje, ditos (errata em nome próprio, todos já corrigidos ao lado):**
- Na semeadura do Mapa de Rotas, registrei como rota nova o Fisher V9 do ACT, um achado já selado na v201. Era duplicata, justamente o que o mapa
  existe para impedir. Ficou SUPERADA, remetendo à rota original.
- Li o resultado do DR2 como «TENSAO_FORTE» e escrevi que «quem limita β na rota do fundo é o CMB». As duas frases eram condicionais ao mapa de
  R; a auditoria apontou, e eu conferi. Corrigido ao lado no mapa, no Atlas e nas memórias.
- Na construção da Bancada, eu tinha escrito que a covariância do Pantheon+ «não está em disco». Era falso: ela está em
  `C:\IALD\projetos_pyhton\acom\tgl_data_cache\pantheon_covariance.dat`. Foi afirmação de ausência sem consulta completa, exatamente o que a
  régua do aferidor proíbe. Corrigido ao lado no código, no README e na memória.
- No chat, eu disse que |β̂| ficava a 0,26σ de α√e. Esse número vinha do ajuste P2. Pela estatística pré-registrada (o posterior P1), são 0,23σ.
- A primeira bateria de testes do Mapa de Rotas «passou» pelo motivo errado: usei uma identidade curta demais, e as recusas vieram dessa regra, não
  das validações que eu queria provar. Refiz exigindo o motivo certo em cada recusa, e só então semeei o mapa.
- Repeti um erro já registrado como lição: um heredoc do Git Bash comeu uma barra invertida de um caminho. Foi pego por falha visível antes de
  qualquer número.

## 7. As outras IAs

- **Claude (15 agentes):** sete aferidores, sete verificadores adversariais e um crítico de completude, num workflow. Cada achado passou por um
  agente distinto que tentou derrubá-lo. Isso rebaixou vários (o do gate, de ALTO para MÉDIO) e refutou um (o «7,509» do neutrino).
- **ChatGPT/Codex (bancada oficial):** a investigação que ela fez hoje foi lida e conferida. O Fisher V9 = 0 se sustenta e já estava registrado
  na v201. A D10 foi reproduzida em todos os dígitos. A degenerescência de modo único se sustenta. O neutrino a 2,95σ está na borda, dependendo
  da entrada. Recebeu um aviso pelo túnel sobre o Mapa de Rotas.
- **Kimi, MiMo e Google (orquestrador):** o MCP está registrado e conectado, mas as ferramentas não carregaram nesta sessão. Pela regra da
  skill, não recriei o servidor. O pedido está pronto em `PEDIDO_ORQUESTRADOR_PREPARADO.md`: segunda leitura independente, com literatura, dos
  cinco pontos mais pesados. Sai quando a sessão for reaberta.

## 8. O que só você decide

1. **O mapa de R e a orientação do sinal:** como a modificação da TGL entra na física do CMB (qual Ω_m a física acústica vê) e qual face fecha o
   balanço de Clausius. São escolhas de teoria. Sem elas, a rota do fundo não decide β.
2. **O nome do gate:** se o degrau experimental ganha o qualificador no próprio nome (errata ao lado). A regra da casa é que o nome viaja sozinho.
3. **O ringdown na v376:** se entra «como condição», sabendo que no ramo canônico ele só devolve a RG.
4. **O neutrino:** qual entrada externa vale e com que convenção de σ, ou declarar o veredito como dependente da entrada.
5. **O orquestrador:** reabrir a sessão do Claude Code para as outras IAs rodarem o pedido pronto.
6. **A desclassificação:** se ela muda o desenho do site (a paridade inversa de 08/09). Isso é ato seu, pela sessão do site.
