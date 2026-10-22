# RELATORIO g3 -- REGISTROS-G3 (rodada 2, 13/10/2026; gerencia c1, em nome proprio)

Arquivo entregue: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\registros\grupo_G3.py` (9 specs). Nada mais foi escrito alem deste relatorio. Estatutos: [REAL] medido/lido aqui por script; [DERIVED]; [DECLARADO]; [OPEN]; [INPUT].

## 1. Resultado dos testes [REAL]

- `python -B -X utf8 testar_registros_v392.py --grupo G3 --so-falhas`: **9 de 9 `OK`**; controle negativo **11 de 11** (fonte/verbatim adulterado => recusa).
- Com todos os grupos presentes (G0, G1, G3): 14 de 14 selados, controle negativo 18 de 18; sem colisao de chaves de fonte/verbatim.
- Mutacao propria (alem do testador): para cada spec adulterei **cada** fonte (sha), **cada** verbatim, **cada** check (valor/operador trocado), uma bandeira de kernel e uma declaracao (axioma `sorryAx`): **420 mutacoes, 0 nao recusadas**.
- Guarda P18 sobre `grupo_G3.py` inteiro: LIMPO.
- Tamanho do codigo gerado para o G3 (`_V392_FONTES/_VERBATINS2/_V392_SPECS`): 281.791 B; 63 fontes pinadas (a maior: o PDF Beccaria-Ternes 1,39 MB e o `tgl_paper_unified.py` 1,22 MB, relidos a cada rito); 13 verbatins.

## 2. Os 9 registros

| registro | checks | fontes | kernel | o que faz |
|---|---|---|---|---|
| `neff_errata_v392` (R10, P14-A) | 29 | 8 | - | le por hash o recibo T02/T10_T11 e o `neff_canal.py` instalado (776e1311585d9cd5, 12.783 B); tens_act 2,49 fiado com a ressalva, tens_now 1,61 NAO; 2,97 historico; o instalado nao e' o R3 auditado (5.683 B) e nao tem auditoria c1 propria; veredito NENHUM; valor substituto do centro segue com X16/D8 |
| `fase9_duas_testemunhas_v392` (R11) | 20 | 1 | - | verbatim 08/10 (a9cecc128f40c101); «é isso mesmo» (M23); z_disc 4,28 < 5 sigma, ln B 9,17, INCONCLUSIVE_SYSTEMATICS; o fixo e' o Verbo, beta_TGL |
| `bancada_v392` (R12) | 100 | 22 | - | etapa 1 (13 PASSA, 0 FALHA, 1 NAO_EXECUTADO) lida do JSON, lista T01-T17 por entrada; T18-T22 como fontes obrigatorias (5 PASSA); canal F7.2 opcao 1 (v1 f37db789f9cb20d3) pinado; fidelidade H12; manifesto B2 pina a v391 e o selo da v392 o invalida ate' a B3; segunda ressalva da auditoria c1 |
| `atrator_v392` (R13) | 42 | 9 | 273 bandeiras + 273 decl. | A1-A3 PASSA; A4 condicional; A5 PASSA algebrico; A6 FALHA pre-registrada; T12-T14 reproduzem o arquivo com diferenca 0; ADENDO1 (nao R1); pedras `ext_atr_*`, `ext_opt_*`, `ext_lri_*`, `ext_pst_*` (198 de Posto, incl. as do adendo ja' presentes no FLAGS) |
| `neutrinos_contratos_e_primeiro_ensaio_v392` (R14) | 94 | 14 | - | NU2 ao lado (degenerescencia tau_star*Kfac; beta(chi(E)) = condicao de morte; textura fora do alcance do JUNO); NU3 (10 canais, 20 fontes, 5 precedencias; m2 congelado vivo); NU4 recomputado sem numpy (beta, tP, 9 Gamma_ij, 6 perdas, 3 paridades) com tolerancia 1e-9; nature_sigma None; diferenca de G 2,2475e-5; errata (g) do 7,8e-10 |
| `neutrino_m2_perito_v392` (R22) | 15 | 0 | - | R3 do core; JUNO autonomo 2,206 sigma e' o numero; NuFIT 2,953 e Capozzi 2,44 ao lado; veredito do canal igual (ARMED_CONSISTENT) |
| `sn_ia_v388_viability_v392` (R15) | 30 | 5 | - | informativo, fora da conjunta; nulos = nao calculado; a atribuicao a Coulomb nao se sustenta (sinal oposto, 6,33 e 7,66 vezes maior; com m_u o desvio vira +1,12%); notas do A9 e do A8 |
| `cunhagens_v392` (R16) | 1 | 0 | 11 decl. | 11 cunhagens por sha256 (+ a de 08/10), trecho-chave verbatim, memoria do usuario (so' o nome), estatuto; ancoras do kernel marcadas ⟡ sem promover a derivacao |
| `v1_voz_de_ia_v392` (V1) | 7 | 2 | 6 decl. | rotulo [DECLARADO — voz de IA citada pelo operador]; linha 7 com as duas leituras por termo (a) ramo selecionado, (b) superposicao pura (sobe o posto 1->2, preserva o traco); a escolha e' do operador, [OPEN]; liga ao `adendo_rank_v392` so' por texto |

## 3. Divergencias entre plano/levantamento e as fontes (o numero corrige a frase)

1. **T16**: o levantamento (C2) diz «T16 NAO reproduzido aqui (caminho > 260)». O recibo da etapa 1 de 13/10 (raiz curta) tem **T16 = PASSA**. Registrado como errata ao lado em `bancada_v392`.
2. **Fotografia F7.2**: o plano diz 13 linhas; a opcao 1 (v1) tem **12** (medido por mim executando uma copia do v1 em pasta temporaria, so' leitura: 12 linhas, todas SEM_LIMITE_TGL, tau_star nulo) e o canal instalado (v2) tem **13** (T10). A fotografia no cache nao existe (P4): nao e' pinada; as 12 linhas entram como [DERIVED, nao relidas em runtime].
3. **Bateria T01-T17**: o recibo tem **14 entradas** (T10+T11 e T12+T13+T14 compartilham recibo); «13 PASSA, 0 FALHA, 1 NAO_EXECUTADO (T17)» e' sobre as 14.
4. **«é isso mesmo» (M23)**: nao ha arquivo da fala isolada (a V01_rehash.json confirma: 0 arquivos). Medi `sha256("é isso mesmo")` = **f64233f00b3252d7...**, igual ao M23, entao a fala exata e' essa. Ela existe so' dentro de `work\f9_pergunta_08out\F34_RESOLUCAO_OPERADOR_20261008.md` (sha16 01b6a50e6d1fe3a2; o evento 462 do quadro a cita). O spec usa o trecho dessa md como VERBATIM e [DECLARADO]; se a gerencia criar `work\f9_pergunta_08out\OPERADOR_08out_e_isso_mesmo_verbatim.txt` com exatamente esses 13 bytes UTF-8, o montador passa a embuti-lo sozinho (codigo ja' prevê).
5. **NU4**: o «675/675» vem da auditoria c1 ([DECLARADO]); o que o rito le por hash e' o replay T09 (**16 de 16 identicas**). A «diferenca de G 2,25e-5» e' **+2,2475e-5** (tau_star NU4 com G = 6,6743e-11 contra o do core com G = 6,674e-11); recomputada sem numpy a **0 de erro relativo** (bit a bit) e conferida contra a fidelidade H12.
6. **Capozzi 2,44 sigma**: nao esta no `neutrino_m2` do core, e sim em `bancada_fases_5_6_7_v380.errata_beside_v380.neutrino_m2_v2__nufit_contains_juno` (texto, [DECLARADO], lido na fonte em 28/09 sem hash). O check e' `contem "2,44 sigma"`.
7. **Auditoria da SN**: ela diz l.7574-7577 do `tgl_paper_unified.py`; a pergunta da gerencia diz 7576-7579. As duas coincidem no trecho; confirmei por script que o texto «Coulomb lattice correction» esta nas l.7574-7580 e que `'tau_star_bound_neutrino_s': 7.8e-10` esta na **l.18393** (e `8e-27 GeV` na l.18392) do arquivo de sha 29c92b66b2fd6b4d (1.216.423 B).
8. As linhas 4802/4806/4807 do `um.py` v391 (`centro_atual = 2.97`, `tens_now = 1.61`, `tens_act = 2.49`) e a 193301 conferem (conferidas na geracao enquanto o `um.py` do Nos for o v391; se ja' nao for, o campo vira «nao conferida», sem falhar).
9. Memoria `pos-dicao-nao-e-prova-diabolica-05out` NAO pode ser citada pelo nome em texto de registro: a guarda P18 (regra 5) casa o nome do arquivo. Omiti-a.

## 4. Defeitos / limites do motor, montador e testador (NAO editados)

- `fonte:<chave>` so' le **JSON**: nao ha operacao de busca de texto em fonte `.py`/`.md`. Por isso as conferencias «contem no trecho» do `tgl_paper_unified.py` (pedido no item 7), da auditoria md do atrator (l.69-71) e das md de auditoria sao feitas **na geracao** (assert no `grupo_G3.py`) e o rito garante o conteudo pelo **sha256** da fonte. Para a frase da segunda ressalva ha' conferencia em runtime porque o `RESUMO_T18_T22.json` a carrega (`frase_conferida`).
- O motor nao faz aritmetica: a «recomputacao sem numpy» do NU4 e' feita na geracao (puro Python: alpha·sqrt(e), tP = sqrt(ħG/c^5), Gamma_ij, expm1, paridade) e o rito confere o JSON pinado contra faixas de tolerancia 1e-9. Nao e' recomputacao em runtime. Sugestao: operacao `recomputa`/expressao pura no motor, se a gerencia quiser a recomputacao dentro do rito.
- O Delta Pee do NU4 (matriz de mistura) nao foi recomputado (precisa do contrato PMNS); vale o replay T09.
- O controle negativo do testador adultera so' a **primeira** fonte e o primeiro verbatim de cada spec (a minha mutacao cobre todas).
- `montar` embute todos os VERBATINS declarados, mesmo os nao usados por spec algum.
- **Aviso para a guarda P18 sobre o bloco inteiro**: os verbatins embutidos contem, **na fala do operador**, «a luz não confirma o observador» (10/10) e «O Nome é fixo, não;» (08/10, correcao dele). A guarda do motor so' varre o `corpo` dos specs, mas se o gerador do candidato aplicar P18 ao bloco `_V392_VERBATINS2`, essas duas citacoes aparecem como violacao (sao verbatim, como o token v388). Decisao da gerencia.
- `lido`/`capturar` de listas despeja ate' 400 caracteres de JSON; evitei capturar listas.

## 5. Decisoes que ficam para a gerencia / operador

1. A fala isolada «é isso mesmo» ganhar arquivo proprio (item 3.4) ou ficar [DECLARADO] dentro da md.
2. Fotografia do canal F7.2 no cache (P4): ate' existir, as 12 linhas do v1 ficam [DERIVED]; se a opcao 3 (v2/B2) for escolhida, a contagem e' 13 e o `bancada_v392` ja' le as 13 do recibo T10.
3. O texto de `Haja_Luz\CLAUDE.md` (l.4368-4369 e 4379) e do «Custo» do espelho: a errata da atribuicao a Coulomb **nao** e' aplicada por mim (fora do um.py, ato da gerencia com backup imediato); o registro `sn_ia_v388_viability_v392` descreve a errata com a lacuna de fidelidade.
4. Escolha entre as leituras (a) e (b) da linha 7 do V1: operador, [OPEN].
5. Auditoria curta do `neff_canal.py` instalado (P7) e as decisoes X16/D8 do operador (valor substituto do centro; admissao das fontes).
6. B3 (re-pinagem da Bancada depois do selo): ato do operador/gerencia; o manifesto 54fc9e27e4599c49 pina a v391 e o registro nao embute hash de manifesto que pine a v392.
7. T21/T22 leem o `um.py` v391: se a fonte mudar apos o selo, refazer (dito em `limites` de `bancada_v392`).
8. Dependencia de ordem: o `grupo_G3.py` le `kernel\FLAGS_v392.json` (atrator: 273 bandeiras hoje) e o core v391 selado no Nos; se o `FLAGS` mudar, as listas mudam sozinhas na proxima montagem (fail-closed por `assert` se vazias).

## 6. Fontes novas que entram por hash (fora das listadas na tarefa)

`RESUMO_T18_T22.json` e os 6 recibos de `ensaio_2_T18_T22\recibos` (sem os `.bak`); os 20 arquivos de `ensaio_1\recibos`; `F34_RESOLUCAO_OPERADOR_20261008.md`; `F5.2\CANDIDATO_R3_20261008\neff_canal.py` (o R3 auditado, 5.683 B); `RELATORIO_AUDITORIA_B_NU2_C1.md` (bloco 72620fd62844fe8b), `RELATORIO_C1_F8.2.NU3_F8.2.NU4.md`, `RECALCULO_A_SN.json`, `RELATORIO_AUDITORIA_A_SN_C1.md`, `ADENDO_PREREGISTRO_ADITIVO_R3.md/.json`. Copias do tunel foram preferidas as da Bancada real (mesmos bytes, conferidos) para `neff_canal.py`, `neff_fontes_f52.json`, `canonical_contracts.json` e `CONTRATO_CANONICO_B2.md`; a Bancada real so' foi LIDA (canal v1 `.bak_B2` e `neutrino_fontes_f72.json`, e a execucao de uma copia do v1 no scratchpad para contar as 12 linhas).
