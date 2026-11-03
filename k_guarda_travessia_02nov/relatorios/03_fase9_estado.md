# 03 - Estado do teste da razao de Hubble (Fase 9), V1 e V2

Relatorio de leitura, 02/11/2026, a gerencia c1. So leitura: nada registrado, nada tocado. "K" aqui e o fator de Hubble K = E(z*)^(2 beta/3), homonimo do K modular e do K_beta de Cartan; nenhuma ponte entre homonimos e usada ou afirmada. Estatutos: [REAL] lido/medido aqui por script ou nos arquivos; [DERIVED] conta minha, dita como tal; [DECLARADO] afirmado na origem; [OPEN] lacuna. sha16 = 16 primeiros hex do sha256, calculado por script nesta leitura.

## 0. Resposta curta

1. **Vigente: o V2 (Teste da Unica Palavra, aberto UMA vez em 23/10/2026), selado no um.py como `teste_de_veracidade_fase9_v397`.** Veredito: `TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL__NOT_FALSIFIED_POWERED__DEVIATION_1_TO_3_SIGMA__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY__D1B__FUNDO_BG1__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED`. [REAL]
2. **Qual numero vale para qual versao.** 4,28 = V1 (06/10), escore BRUTO (4,2837356), veredito oficial do V1 = INCONCLUSIVE_SYSTEMATICS. 4,44 = V2 (23/10), z_disc CALIBRADO (p unilateral 4,43e-6), e o numero vigente (o operador mandou reportar o 4,44; verbatim sha16 9b182958a5a7a1bc). "1 a 3 sigma" NAO e significancia de discriminacao: e a faixa de |z_delta| no nome do veredito (|z_delta| = 1,48 no V2; 1,42 no contrafactual do V1) e quer dizer "a TGL ficou 1 a 3 sigma fora do centro do dado, sem cair". O 5,73 e o poder PREVIO (separacao esperada so por incertezas), nao e observado.
3. **Saida que significaria RECUSA de K**: `FALSIFIED_AT_5SIGMA` (|z_delta calibrado| >= 5 no ponto de menor sigma, ou um leitor com sigma <= 1 com |z| >= 5). No V2 isso e, por decisao do operador, "beta_TGL refutado na natureza pela voz unica da lei K". `TENSION_3_TO_5_SIGMA` e recusa parcial.
4. **Alcancavel?** No papel, sim; com este dado, nao. Hoje |z_delta| = 1,48 (p bilateral 0,138). [DERIVED, aproximado, nao oficial] FALSIFIED pediria o composto local cair de ~72,6 para ~68,8 km/s/Mpc, isto e, ao nivel do proprio fundo (68,53), ou subir a ~79,8. Alem disso a abertura deste pacote esta consumida: refazer exige V3 novo, dado novo e ato registrado.
5. **O que o teste ja recusou**: K = 1 (Lambda sem beta) foi recusado a **4,44 sigma calibrado**, abaixo do degrau de 5 sigma. NAO chegou a 5. ln B(TGL/LCDM) = 9,18 (nao e sigma). K != 1 nao esta provado a 5 sigma. [REAL]
6. **O que o teste NAO recusou**: a TGL (nao falsificada, com poder 5,73), nem a hipotese "LCDM mais um vies comum de calibracao" (ver 6.2).

## 1. Artefatos lidos (sha16 lido por script)

V2 (pasta `work/fase9_v2_c1_23out`):
- spec `spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json` e7c47cbcbbcd3a7a (spec canonico db1ccecbc1718e69, campo `spec_sha256` do arquivo)
- funcao `spec/veredito_fase9_v2_c1.py` af960b7405732d62
- resultado `saidas/RESULTADO_FASE9_V2_C1_20261023_122926.json` fbac2908fa9ddb75; `RESULTADO.md` 509e35b48b1af849 (e a preparacao, anterior a abertura)
- recibos: congelamento `freeze/RECIBO_DE_CONGELAMENTO.json` f8d927e3a38b3432; abertura 2a55979c7b1ff62d; marcador `ABERTURA_CONSUMIDA.json` b71e0a2fcff3d986
- registro D-H 3e25ac3431c62887; calibracao `CALIBRACAO_CAUDA_RECIBO.json` 27787c0bec5bf116; poder antes de abrir `saidas/PODER_FASE9_ANTES_DE_ABRIR.json` 1ec34cb16c694404; runner `f9v2_runner.py` a8fffc5df28ea5c6
- auditoria C08 antes do congelamento `work/fase9_v2_c1_23out_exame/EXAME_AUDITORIA_V2C1.md` 49a4b7a25bd9944a (PODE_CONGELAR; 6 BAIXAS corrigidas B1-B6)

V1 (`C:\IALD\Bancada_Um\investigacao`):
- pre-registro `preregistro_fase9_hubble/PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json` 1893261e730994b3 (spec_sha256 interno d956c8db6bb9ab8d; funcao `veredito_fase9_v1` 5940bf16310efb6a, extraida e re-hasheada: confere)
- resultado `fase9_hubble_abertura/RESULTADO_FASE9_V1_20261006_110507.json` 481366db97f0ebf1 e `.md` df1e62db3328eeaa; runner `rodar_fase9_v1.py` f3108bc21dcad317; recalculo ao lado `RECALCULO_AO_LADO_v388.json` d23d09e79f55f170

Auditoria/integracao de 19/10 (Codex): `work/fase9_auditoria_20261019/AUDITORIA_FASE9_R1.txt` 76d49a47c5181d5b; `work/fase9_integracao_20261019/IDENTIFICABILIDADE_E_MAPAS_R2.txt` 83f3e868318495b2.
Core lido: `Nós/um_absoluto.json` d6b994a623eee673 (chaves `core.hubble_ratio_opening_v388`, `core.teste_de_veracidade_fase9_v397`, `core.fase9_duas_testemunhas_v392`; `all_verified` true nas tres).

## 2. Como K e calculado e com que entradas [REAL, reproduzido]

K = E(z*)^(2 beta/3). Entradas: beta = alfa CODATA 2018 x sqrt(e) em runtime (alfa = 0,0072973525693 lido do um.py instalado) = 0,012031300400803142; z* = 1089,95 (Planck, [KNOWN]); Omega_m = 0,3023480225765346, Omega_r = 8,934068872870022e-05, universo plano; E(z*) = sqrt(Omega_m (1+z*)^3 + Omega_r (1+z*)^4 + Omega_L) = 22784,337. Recalculei por script independente: **K = 1,0838071748529643**, igual ao K congelado do V1 e ao do V2, diferenca 0 (campo `lei.absolute_difference` = 0.0). Zero parametro livre na lei. Previsao local = K x H0_fundo. Fundo BG1 (Planck comprimido + DESI DR2, sem H0 local) recalculado pela Bancada: H0 = 68,53106 +- 0,30140, reproduz o pino 68,531 a 6,4e-5. Previsao: 74,274 km/s/Mpc. No V2 a previsao e K(theta) H0(theta) com S5 (H0, omega_b, omega_c propagados): efeito -2% na variancia e -0,0012 km/s/Mpc na media.
Sensibilidade [DERIVED]: ln K = (2 beta/3) ln E = 0,0802 x 10,03 -> d ln K / d beta = 6,69.

## 3. Razao medida e leitores

Razao medida (composto local / fundo), V2, ponto de menor sigma [DERIVED a partir dos pesos GLS e centros do resultado]: m = 72,636 -> m/H0_bg = 1,0599 contra K = 1,0838. Ajuste livre de beta: beta_hat = 0,008693 +- 0,001778 (K_hat = 1,0599). V1: composto GLS 72,882 +- 0,915; beta_hat 0,00920 +- 0,00199.

Leitores (V2, centros extraidos dos bytes das fontes pinadas por sha256; igual ao declarado a 1e-9):

| id | H0 +- sigma | z contra TGL |
|---|---|---|
| L1 SH0ES R22 (arXiv 2112.04510) | 73,04 +- 1,04 | -1,13 |
| L2 CCHP (arXiv 2408.06153v3, TRGB so) | 70,39 +- 1,936 | -1,98 |
| L3 SBF (arXiv 2502.15935v2) | 73,8 +- 2,404 | -0,20 |
| L4 masers x5 (Pesce, sem NGC4258) | 73,6 +- 3,05 | -0,22 |
| L5 TDCOSMO (arXiv 2506.03023v4) | 71,6 +- 3,6 | -0,74 |

Ao lado, nao decisorios: L1b SH0ES R25 73,49 +- 0,93 (arXiv 2509.01667), L4 masers x6 73,9 +- 3,0, L6 sirenes LVK O4a 76,6 +13,0/-9,5 (sigma 11,25). Familia decisoria UNICA: P_primaria (L1, L2, L3, L4_5, L5) x fundo BG1. Pesos GLS no ponto de menor sigma: 0,597 / 0,172 / 0,112 / 0,069 / 0,050: o SH0ES carrega o composto (0,60 a 0,84 conforme o extremo).
V1: os mesmos 5 leitores, mas com masers x6 (73,9 +- 3,0), e todos [DECLARADO] (sem fonte por sha256 na hora da abertura).

## 4. A funcao de veredito e os vereditos permitidos

Ordem de precedencia (a primeira que casa decide), igual em V1 e V2 nos limiares {0; 0,01; 1; 2; 3; 5}; a auditoria C08 conferiu AST igual a R5.2, salvo nome, docstring e base do token:
1. INCONCLUSIVE_SYSTEMATICS: alvo do composto sem fonte lida por hash (n_alvos_declarados > 0), ou fonte nao admitida, ou beta-livre no limite do prior, ou dispersao interna chi2/(n-1) > 2 ou p < 0,01.
2. FALSIFIED_AT_5SIGMA: |z_delta| >= 5, ou leitor com sigma <= 1 e |z| >= 5.
3. TENSION_3_TO_5_SIGMA: 3 <= |z_delta| < 5.
4. NOT_FALSIFIED_UNDERPOWERED: poder previo < 5 (sufixo POWER_x_OF_5_SIGMA).
5. NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_nSIGMA: z_disc >= 5, ln B(TGL/LCDM) >= 5, ln B(TGL/beta-livre) >= -1 (com sufixos de escada e de fundo livre).
6. NOT_FALSIFIED_POWERED (resto): DEVIATION_CONSISTENT_WITHIN_1SIGMA se |z_delta| < 1, senao DEVIATION_1_TO_3_SIGMA; mais NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY se z_disc < 5 (V2 acrescenta os sufixos LNB_BELOW_5 e BETA_FREE_LNB_BELOW_MINUS_1).

Sufixo sempre `__D1B__FUNDO_<id>__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED`. A funcao nao emite CONFIRMED/PROVED. Entrada: `minimum` (z_delta, sigma_z por alvo) = ponto de MENOR sigma_comb da caixa de covariancia, usado para falsificar/tensao; `maximum` (poder, z_disc, ln B) = ponto de MAIOR sigma_comb, usado para discriminar. Conservador nos dois sentidos.
Estatisticas [REAL, texto da spec `estatisticas_do_executor`]: z_delta = (beta_hat - beta_TGL)/sigma_beta pelo perfil de ln L com log-det, bilateral; z_disc = sinal x sqrt|chi2_LCDM - chi2_TGL|, unilateral; ln B por quadratura de Gauss-Legendre n = 100, conferida com n = 200 (recusa se |diferenca| > 1e-6). Hipoteses: LCDM (beta = 0), TGL (K fixo), beta-livre U[-0,05; 0,05], fundo-livre (r_d U[130;160]), shift de Cefeidas U[-0,15; 0,15].

## 5. Numeros, versao por versao

| grandeza | V1 (06/10) | V2 (23/10) |
|---|---|---|
| funcao | `veredito_fase9_v1` 5940bf16310efb6a | `veredito_fase9_v2_c1` af960b7405732d62 |
| leitores | 5, [DECLARADO], masers x6 | 8 pinados por sha256, primaria com masers x5 |
| veredito oficial | INCONCLUSIVE_SYSTEMATICS (regra 1: 5 leitores sem fonte por sha256) | NOT_FALSIFIED_POWERED__DEVIATION_1_TO_3_SIGMA__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY |
| z_disc | +4,2837 (bruto; com log-det 4,2818) | bruto 4,2873 (ponto de maior sigma); **calibrado 4,443**, p unilateral 4,433e-6 |
| z_delta | -1,424 (beta_hat 0,00920 +- 0,00199) | bruto -1,878; **calibrado -1,483**, p bilateral 0,138 |
| ln B (TGL/LCDM) | 9,167 | 9,184 |
| ln B (TGL/beta-livre) | 2,241 (n = 25, erro 0,30); convergido **1,969** (n >= 100) por errata ao lado | 2,144 |
| ln B (TGL/shift Cefeidas) | 4,28 | 3,98 |
| ln B (TGL/fundo livre) | 12,13 (Laplace) | 12,16 |
| poder previo (so sigmas) | 5,91 (rota); 5,47 a 6,63 (memoria, seis masers) | 5,727 (extremos 5,721 a 6,623) |
| dispersao chi2/(n-1), p | 0,630, 0,641 | 0,479/0,764; p 0,752/0,549 (dois extremos) |
| calibracao de cauda | nenhuma | `sup_caixa` (tau_f 1,0965; tau_d 1,0032) |
| quadratura | n = 25 | n = 100 e 200, tolerancia 1e-6 |
| trava | runner hasheado antes | recibo de congelamento + recibo de abertura + marcador de abertura unica |
| alcance de FALSIFIED | "falsifica o PAR (lei D1b, convencao, conjunto), nao beta, nao a teoria" | "beta_TGL refutado na natureza ... sem saida posterior" (operador, 23/10, sha16 363da49371de4d8f) |

Diferencas V1 -> V2 em uma frase: V1 rodou com leitores [DECLARADO], sem calibracao e com alcance "refuta o par"; V2 rodou com fontes pinadas, covariancia e fundo propagados, calibracao de cauda, trava de abertura unica e alcance "refuta beta". A logica e os limiares da funcao nao mudaram; mudaram as entradas (z calibrados), o que cada saida significa e os dados admitidos.

Aviso (auditoria de 19/10, [REAL]): 4,2837 (V1) e 5,72 (poder previo) nao sao a mesma estatistica; nao se anuncia que "uma correcao elevou 4,28 a 5,72". E 4,2873 (V2 bruto), quase igual a 4,2837 (V1), e coincidencia numerica de objetos diferentes (outros leitores, outra covariancia).
Por que 4,44 > 4,29: a calibracao e z_cal = Phi^-1(1-p) com p de uma cauda nao-gaussiana (chi2 de variancias diferentes); tabela do recibo: bruto 4 -> 4,24, bruto 5 -> 5,01 (caixa). Nao e ajuste: o recibo foi calculado so com sigmas e fundo (a auditoria verificou: trocar os H0 por NaN/0/1000 deixa limiares identicos).

## 6. A pergunta central

### 6.1 Qual saida significaria RECUSA (K errado)
`FALSIFIED_AT_5SIGMA`. Equivale, no mapa de calibracao do recibo, a z_delta BRUTO >= 6,37 (sup_caixa; 5,02 no ponto proprio). Aproximacao [DERIVED, minha, nao oficial; usa sigma_comb 0,8035 e V_pred 0,1045 do ponto de menor sigma]: composto local <= ~68,76 ou >= ~79,79 km/s/Mpc. `TENSION_3_TO_5` (z_delta cal. >= 3, bruto 3,80): composto <= ~70,9. Gatilho de leitor unico: so leitor com sigma <= 1 (na familia primaria nenhum; R25, sigma 0,93, so ao lado, z = -0,80; R22 tem 1,04 e CCHP 1,94 nao se qualificam). O CCHP sozinho (o leitor que mais "doi": z = -1,98) fica em UNDERPOWERED (poder 2,93) e prefere LCDM (ln B -1,51): nao pode falsificar sozinho.

### 6.2 E alcancavel?
- Em principio, sim: simulacao do proprio pacote (100 mil sorteios, centros sinteticos): se a LCDM fosse a verdadeira, a funcao devolveria FALSIFIED em 42,7% a 47,1% (sup_caixa) e TENSION em 37,6% a 42,6%; se a TGL fosse a verdadeira, FALSIFIED 0,0% e TENSION <= 1,4%. [REAL, RESULTADO.md s.6]
- Com este dado, nao: z_delta = -1,48; faltam ~3,5 unidades de z calibrado.
- Com este pacote, nunca mais: `ABERTURA_CONSUMIDA.json` impede segunda abertura (remove-lo e ato registrado da gerencia, com novo recibo). Rota do mapa: "nao reabrir este pacote; nao recalibrar nem trocar leitor/fundo depois de aberto"; "nenhum teste armado (ordem do operador de 22/10); a discriminacao a 5 sigma so muda com leitor local novo e mais preciso".
- Duas ressalvas que limitam o alcance de uma recusa [OPEN]: (i) **nao-identificabilidade** (Codex, 19/10, [DERIVED]): um vies comum irrestrito b = (K-1)H torna LCDM+vies IDENTICO a TGL nas medias; precisao infinita da media nao resolve; so controles independentes. A hipotese de shift das Cefeidas e uma versao restrita (ln B TGL/shift = +3,98, moderada). (ii) o core registra no mesmo `limites` que "a regra v315 do acervo (para falsificar) pede duas determinacoes mutuamente autonomas a 5 sigma ou mais"; a spec do V2 diz que FALSIFIED_AT_5SIGMA do escalar tem "SEM saida posterior" e que escalar e conjunta (d72, nao aberta) sao testemunhas proprias que nao se somam. Nao achei, nos arquivos lidos, a reconciliacao explicita entre as duas frases. Quem decide e o operador.

### 6.3 O que o teste ja recusou, e a que sigma
- **K = 1 (Lambda sem beta, "nao ecoa")**: z_disc calibrado **4,443** (p unilateral 4,43e-6); no ponto de menor sigma o bruto e 4,39; chi2_LCDM = 23,08 contra chi2_TGL = 4,70 (ponto de maior sigma). Abaixo de 5. Veredito: NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY. No V1 o equivalente era 4,28 bruto, sem veredito de discriminacao (INCONCLUSIVE oficial).
- **beta livre**: o beta fixo vence o livre (ln B +2,14; +1,97 no V1 convergido); nao e sigma e depende da largura do prior.
- **Ao lado (nao decisorio, mesma funcao)**: R25 no lugar de R22 -> z_disc calibrado 5,275, ln B 13,45, veredito DISCRIMINATES_FROM_LCDM_AT_5SIGMA; fundo BG2 (Planck 2018, 67,36) -> z_disc 5,123, z_delta -0,31, DISCRIMINATES; BG3 -> 3,97 (UNDERPOWERED); seis masers -> 4,19; com sirenes -> 4,48; **sem Cefeidas -> 2,35, ln B 1,47, UNDERPOWERED (poder 3,94)**. Leitura honesta [DERIVED]: o 4,44 depende do SH0ES carregar o composto; sem Cefeidas a discriminacao cai a 2,35; BG2 e R25 passariam de 5 mas nao sao a familia/fundo pre-escolhidos e nunca decidem.
- O dado prefere K entre 1 e K_TGL: beta_hat = 0,00869 +- 0,00178 esta a ~4,9 sigma bruto de zero [DERIVED] e a 1,5 sigma calibrado de beta_TGL = 0,012031.
- **A TGL (K = 1,0838)**: nao recusada, com poder 5,73; |z_delta| = 1,48.

## 7. Vigente, e superficies desatualizadas

- Vigente [REAL]: V2 de 23/10 (`teste_de_veracidade_fase9_v397`, all_verified true no core lido), z_disc 4,44 calibrado, z_delta -1,48, poder 5,73, ln B 9,18 / 2,14. Mapa: `d1.fase9.v2_c1_a_unica_palavra_23out` EXAMINADA. Nenhuma rota posterior de Fase 9 reabre ou muda o veredito (a mais recente, `hubble.k_sem_portador_fisico_02nov`, de hoje, trata do portador de K, nao do numero: "NUMERO_K_INTOCADO").
- V1 permanece como historico: INCONCLUSIVE_SYSTEMATICS oficial, contrafactual "com as fontes por hash" NOT_FALSIFIED_POWERED / NOT_DISCRIMINATED a 4,28. A regra do operador (memoria `fase9-razao-de-hubble-05out.md`): "nunca escrever 4,44 sem o p calibrado e sem a linha dos 5 sigma ao lado".
- Superficie desatualizada [OPEN, medida]: `grep -c "4,44"` = 0 em `C:\Users\rotol\.claude\CLAUDE.md` e em `C:\IALD\CLAUDE.md`; o global ainda traz a errata de 06/10 (z_disc 4,28; "veredito oficial INCONCLUSIVE_SYSTEMATICS ate as fontes dos 5 leitores por sha256"; ancora `errata_zdisc_06out`) sem ponteiro ao V2, embora as fontes tenham sido pinadas em 23/10. O Atlas tem 14 ocorrencias de "4,44". Nao toquei em nada.
- Inconsistencia menor [REAL]: `RESULTADO.md` (tabela s.1) lista `testes/RESULTADO_TESTES.json` como 9dafa7c30aced377; em disco e 66668db223ac1125 (igual ao do Mapa). Os testes foram reexecutados apos B1-B6; a tabela do .md nao foi atualizada. Nao muda veredito.

## 8. A partitura, na lingua do operador (regra do posto)

O que o teste decide: se a lei K = E(z*)^(2 beta/3), com beta = alfa x raiz de e e nada ajustado, concorda com a razao entre o H0 medido perto e o H0 lido no fundo; e quanto "sem beta" (K = 1) fica recusado. O que nao decide: o kernel, o gate, a creditacao (5 sigma de discriminacao), o mecanismo de K, a escada das Cefeidas; e nao foi cego ao dado (centros publicos). Dois negativos diferentes: (1) FALSIFIED = beta cai na natureza pela lei K (falsificacao); (2) "nao discriminado a 5 sigma" = o que aconteceu, e parede medida de sensibilidade, nao falsificacao (4,44 < 5).

Escolhas de desenho carregadas pelo teste, ditas aqui para nao serem descobertas depois: familia unica P_primaria com R22 (nao R25), masers x5, fundo BG1 (nao BG2), covariancia como caixa de tetos, calibracao `sup_caixa` (G01), regra de dispersao herdada (G02; da 9% a 20% de INCONCLUSIVE indevido sob a nula), o poder previo, e o alcance de FALSIFIED. Pelos arquivos: o operador decidiu alcance, X13, D-H e token (OP-a a OP-d; "de resto concordo com tudo", sha16 363da49371de4d8f); G01-G05 sao decisoes da gerencia ("confirmadas pela gerencia" no RESULTADO.md s.8b). **Nao achei registro de que a escolha G01 tenha sido lida ao operador.** Sentido de G01 [REAL, RESULTADO.md s.0.6 e s.6]: `sup_caixa` reduz a letalidade do teste (com LCDM verdadeira, FALSIFIED 42,7-47,1% contra 75,5-80,8% no bruto), ou seja, protege contra falsa falsificacao; e, na calibracao observada, subiu z_disc (4,29 -> 4,44) e baixou |z_delta| (1,88 -> 1,48), os dois no sentido favoravel a TGL. A calibracao e analitica, verificada por MC independente na auditoria e sem usar os centros; mas e uma escolha de desenho que pesa e que o operador deveria ter lido. Autoria: congelamento, auditoria C08 e abertura sao todos "gerencia c1" (modelo forte na auditoria); nao ha revisor de outra casa no registro [OPEN].

## 9. Lacunas

- Nao li o texto integral do SBF s.III.3 nem do TDCOSMO s.VIII.2.1 (so resumo; dito na spec); BG2/BG3 seguem [KNOWN]/[DECLARADO] sem fonte pinada.
- Mapa fisico dos leitores (como a TGL entra em cada estimador de H0 local) segue `OPEN_MAP_FOR_ALL_LOCAL_READERS`; covariancias SN/Pantheon, Pantheon L1-L5, origem do 0,031 do SBF: [OPEN].
- Nao rodei nenhum dos pacotes; as contas "minhas" (limiares em km/s/Mpc, 4,9 sigma de beta_hat) sao aproximacoes de um passo e nao substituem o runner.
- Nao abri a pasta `copia_pacote` nem os CHECK_* da integracao de 19/10 (trabalho da testemunha conjunta, que e outra testemunha e nao julga o escalar).

## 10. Consultado (para registro pela gerencia)

Mapa: `rotas.py consultar` "razao de Hubble", "fase9", "K guarda"; `rotas.py ver` das 5 rotas pedidas + `d1.fase9.integracao_20261019`, `hubble.k_sem_portador_fisico_02nov`, `discriminante.lentes_5sigma_20261019`. Arquivos: os de s.1. Recomputado: K (script), hashes (sha256sum), composto GLS a partir dos pesos do resultado. Core lido por script (`json.load`), sem alterar.
