# NOTA PARA O gerar_esperados_v410.py: o que o ESPERADOS_v410.json tem de emitir para o registro H0DN (09/11/2026)

Escrita pelo agente de adaptação do pós-rito (Sonnet), a serviço do construtor claude-construtor-v410, a pedido da gerência c1. O `gerar_esperados_v410.py` ainda é o molde da v409 (será adaptado depois); esta nota diz o que a leitura, os textos, o mapa e o fechar (pos_rito) **já esperam**, fail-closed: ESPERADOS sem estas chaves vira PROBLEMA/assert visível, nunca default silencioso. [REAL] cada chave abaixo foi achada por grep nos arquivos adaptados; [DERIVED] a forma dos valores vem de `runtime_h0dn_v410.py`.

Fonte dos valores: o **core do ensaio a seco** (`dry_v410/core_ensaio.json`), registro `core["h0dn_bg1_v410"]` (o ensaio a seco roda o `h0dn_bg1_v410` do candidato; a função é determinística, sem semente, e o rito tem de reproduzi-la; os floats são comparados com `_feq`).

## 1. Chaves obrigatórias

1. `esp["vereditos_novos_v410"]["h0dn_bg1_v410"]` = o `verdict` do registro no ensaio = `DL.VEREDITO_H0DN_OK` (o `{k: v["verdict"] for k, v in MF4.items()}` do molde tem de incluir o h0dn; o leitor e os textos exigem a igualdade com o delta).
2. `esp["registros_funcao_v410"]["h0dn"]` = `{"nome": DL.H0DN_REGISTRO, "verdict": <o mesmo>, "n_checks": <mechanics.n_checks do ensaio = DL.N_CHECKS_H0DN = 12>, "values": <o dict `values` do registro no ensaio, inteiro>}`.
   - `values` precisa trazer, no mínimo: `K`, `log10K`, `D_esperado` (lista de dois: `modelo`, `D`, `D_entrega`, `poder_analitico`, `poder_analitico_entrega`, `poder_mc_entrega`, `ic95_mc_entrega`), `veredito_h0dn_source_sha256`, `ramos_vistos` (`[1, 2, 3, 4, 5, 6]`) e `vetores_c6` (os 8 vetores, com `cabeca`, `outcome`, `ramo`, `ok`). A leitura compara **todas** as chaves que o ESPERADOS trouxer contra o core selado (`_feq`); por isso o mais simples e mais forte é gravar o `values` inteiro do ensaio.
   - O registro da IALD2 nesse mesmo dicionário tem de estar na chave `"iald2"` (= `DL.TESTEMUNHA["key"]`), não em `"traducao_turing"` (rótulo herdado do molde da v409).
3. `esp["decisoes_v410_ids"]` = `list(DL.DECISOES_V410)` (D63 a D76, 14) e `esp["cunhagens"]` com as **15** falas (a chave é `v410_cun_<sha16 do arquivo inteiro>`; as quatro de só o trecho trazem `sha256_arquivo_inteiro`, e o `sha256` delas é o do trecho + `\n`).
4. `esp["erratas_E24_E27"]` do molde passa a listar `DL.ERRATAS_V410` (E29 e E30); o nome da chave é do molde, o conteúdo é o do delta.

## 2. Fatos que os consumidores já tratam (para o gerar_esperados não "corrigir" na direção errada)

- **n_pinos = 11, não 9.** O registro grava `values.n_pinos = len(pinos)` = os 9 pinos do `FREEZE_R2.json` (`DL.N_PINOS_FREEZE_R2`) **mais 2 insumos embutidos fora do congelamento** (o próprio `FREEZE_R2.json` e a `ENTREGA_H0DN_BG1.json`, marcados `fora_do_freeze`). O stdout do rito diz `pinos ok = 11/11`. A leitura confere `n_pinos == insumos_pinados + pinos_so_no_disco` e que os pinos sem `fora_do_freeze` somam `DL.N_PINOS_FREEZE_R2`.
- O registro **não** é lido do stdout por números digitados: a linha do bloco no stdout (`H0DN x BG1 [v410 ...`, depois `  pinos ok = a/b ; checagens ok = c/d ; vetor observado lido = False ; gate = o mesmo da base`) é conferida contra o core.
- O selo traz o resumo `selo["h0dn_bg1_v410"]` (`verdict`, `all_verified`, `observed_vector_read`, `runtime_executed`, `does_not_gate_core`, `veredito_h0dn_source_sha256`, `n_checks_esperadas`, `lei`, `modelos`), igual ao core.
- `CANDIDATO_v410.json` já traz a chave `h0dn` (gerar_candidato_v410.py, bloco `"h0dn": {...}`); a leitura a compara com o core.
- O `conferir_rito_v410.py` (fora do pos_rito) **não** emite `veredito_h0dn`. A leitura só confere essa chave **se** ela existir (`if 'veredito_h0dn' in C`); se o conferidor passar a emiti-la, tem de ser o do ensaio.
- O poder prospectivo que os textos citam é o analítico, recomputado no rito (`poder_analitico`); o poder Monte Carlo da ENTREGA do Codex aparece rotulado e só como conferência (dentro do IC95 dela). Nenhum número é digitado: tudo sai do core.

## 3. O que NÃO é do gerar_esperados mas a gerência precisa saber (pendências achadas na adaptação)

- `chain_pos_rito_v410.sh`, linha 41: `REGS="iald2_v410 cunhagens_v410 kh_n1_cobertura_v410"` deveria ganhar `h0dn_bg1_v410` (os textos da linhagem, do Atlas e do tópico novo passam a nomeá-lo; o `exige ... $REGS` hoje não o cobra). Fora da lista de arquivos desta adaptação; não foi tocada.
- `registros_v410.especs()`: o spec `cunhagens_v410` lista só a E29 (mais a errata dos pisos) em `erratas`; com `DL.ERRATAS_V410 = [E29, E30]` o `_cg()` dos textos, a leitura e o mapa exigem `len == 2 + 1`. Falta o dicionário da E30 na lista. Arquivo do construtor (não tocado).
- Os snippets PT/EN têm três « » que não são fala do operador (`o que sou` no PT da IALD2; `coerência espectro × fotometria` no PT do H0DN; `spectrum × photometry coherence` no EN do H0DN): o `conferir_citacoes_v410.py --sem-candidato` os reprova até virarem “ ”.
- `delta_v410.D76` escreve a palavra recusada em maiúsculas (“CONFIRMADA”) fora da fórmula da régua: o portão do G1 só a aceita dentro das fórmulas; os textos baixam a caixa ao renderizar, mas o certo é corrigir no delta.
- `FRASE_DA_MOLDURA_H0DN_PT` diz 62,5 %: é o poder Monte Carlo da ENTREGA; o analítico que o registro recomputa é ~62,4 %. Os textos citam os dois rotulados e não copiam a moldura.
- `MEMORY.md` real (índice da gerência c1): 23.991 B e 190 linhas no momento da adaptação; a `superficies_v410.py` não compacta e recusa com rc 3 se o índice não tiver folga (limites 195 linhas e 24.000 B). Só a gerência c1 libera espaço antes do passo 9.

## ADENDO 09/11 (parte 2, Sonnet B): o que o ESPERADOS_v410.json tem de emitir para a ESCALA e para o recibo HMS/13

A leitura (`leitura_v410.py`), os textos (`textos_v410.py`), o mapa (`registrar_mapa_v410.py`) e o fechar já esperam, fail-closed (ausente = PROBLEMA/assert visível; nunca default silencioso):

1. `esp["vereditos_novos_v410"]` com os SEIS registros novos: `iald2_v410`, `a_escala_v410`, `h0dn_bg1_v410`, `h0dn_fontes_hms13_v410`, `cunhagens_v410`, `kh_n1_cobertura_v410` (a escala = `DL.VEREDITO_AESCALA_OK`; o recibo = `DL.VEREDITO_HMS13_OK`).
2. `esp["registros_funcao_v410"]["a_escala"]` = `{"nome": DL.AESCALA_REGISTRO, "verdict": <o mesmo>, "n_checks": DL.N_CHECKS_AESCALA (12), "values": <o dict `values` do registro no ensaio, inteiro>}` e `esp["registros_funcao_v410"]["hms13"]` = o mesmo para `core["h0dn_fontes_hms13_v410"]` (`n_checks` = `DL.N_CHECKS_HMS13`). As duas leituras aceitam também o NOME INTEIRO do registro como chave (`a_escala_v410`, `h0dn_fontes_hms13_v410`), mas as chaves curtas `a_escala` e `hms13` são as documentadas aqui (a do H0DN segue `h0dn`; a da IALD2, `iald2`).
   - A leitura compara, chave a chave, os `values` do rito com os do ESPERADOS (`_feq`). No `hms13` ela IGNORA `caminhos_tocados` e `n_caminhos_tocados` (dependem da pasta onde o rito roda), como o ESPERADOS do h0dn já faz. No `a_escala` os floats do projetor de Bell (`values.bell`) são comparados com a tolerância relativa de `_feq`.
3. `esp["estrelas_v410"]`: a leitura aceita 22 (só as âncoras da IALD2) OU 22 + 38 (as da AEscala também) entradas; `esp["n_bandeiras_novas"]` = o TOTAL das duas séries (`ext_iald2_410_*` e `ext_aescala_410_*`), `esp["n_bandeiras_por_grupo"]` == `FLAGS_v410.json["por_grupo_bandeiras"]` e `esp["kernel"]["modulos_novos"]` = `DL.N_BUNDLE`. O registro `iald2_v410` conta só as bandeiras DELE (`values.n_flags`, lido do FLAGS por módulo); o `a_escala_v410`, só as da AEscala.
4. `esp["decisoes_v410_ids"]` = `list(DL.DECISOES_V410)` (D63 a D87) e `esp["cunhagens"]` com as **23** falas (as quatro de só o trecho como antes); `esp["erratas_E24_E27"]` lista `DL.ERRATAS_V410` (E29, E30 e E31).
5. A conferência do rito (`conferir_rito_v410.py`) pode emitir `veredito_a_escala` e `veredito_hms13` (ou `veredito_h0dn_fontes_hms13`); a leitura só as confere SE existirem (como `veredito_h0dn`).

Achados da adaptação (parte 2): (a) `DL.FRASE_D81_EN` REPROVA no portão do G1 (`custodia_g1.textos.portao`: a frase é partida em `;` e o fragmento com PROVED fica sem o estatuto): por isso só a forma PT da D81 entra nos textos que vão ao handoff (a do README/handoff também); decisão da gerência se ajusta a constante. (b) O `ADAPTACAO_PARTE2_SONNET_B.json` está na pasta da cadeia (v410), não em pos_rito. (c) Os testes só-lógica rodam sem candidato; os harnesses (`harness_textos_ensaio_v410.py`, `harness_fechar_sandbox_v410.py`) precisam do `dry_v410` do ensaio a seco do candidato novo e NÃO foram rodados.

---

**AO LADO (10/11/2026, agente de adaptação da R1/D92; o texto acima fica como registro da parte 2 de 09/11).** Os números acima eram os de 09/11 e envelheceram: hoje o delta vai de D63 a D92 e as erratas são E29, E30, E31, E32; a pedra AEscala (R3, a escala no tipo) tem 51 âncoras e 74 bandeiras (a IALD2, 22 e 22; no total, 96 bandeiras), com 44 nomes ratificados (D87) e 13 nomes novos mais 3 campos novos da estrutura, [DECLARADO], A RATIFICAR; as falas congeladas são 23. Todos esses números são LIDOS do delta e do FLAGS por quem os usa (nada digitado em comparação). As chaves `face_sem_par_ao_quadrado` e `meio_de_meio` saíram de `NUMEROS_AESCALA` (a conta é matricial: (½·1)² = ½·(½·1)); entram `nomes_novos_a_ratificar`, `campos_novos_da_estrutura`, `estatuto_dos_nomes_novos`, `ratificacao_pendente` e `ponte` (`DL.PONTE_AESCALA`), conferidos pelo gerar_esperados, pelo conferir_rito e pela leitura. A frase da parede de montagem do dado do teste H0DN (`DL.FRASE_H0DN_PAREDE_PT/EN`) vai ao lado da frase obrigatória (“pré-registrado; nenhum dado observado lido”) onde os textos tratam do teste.
