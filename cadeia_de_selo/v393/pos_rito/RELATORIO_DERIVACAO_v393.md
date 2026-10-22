# RELATORIO_DERIVACAO_v393 (gerencia c1, derivacao da cadeia pos-rito a partir da v392)

Gerado por derivar_cadeia_v393.py (sha16 de molde e derivados em DERIVACAO_v393.json). Nada foi executado contra o Nos (que tem a v392 b590c0aa80055e2a).

## Gerado
- Derivados por copia + subida de versao + edicoes com assert: leitura_v393.py, superficies_v393.py, fechar_v393.py, b3_recibo_v393.py, chain_pos_rito_v393.sh.
- Escritos a mao sobre o molde: textos_v393.py, registrar_mapa_v393.py (monta a rota umpy.v393.regra_e_coracao + 3 anotacoes; NAO registra).
- Protegidos da subida de versao (vizinhos da troca dita): varredura_e_sorry_v392, estatuto_da_prova_v391, fundacao_v390, three_stress_tests_v387.
- ensaio_sintetico_v393/: V falso + COPIAS dos alvos; provou append, idempotencia e compactacao do MEMORY.md (nao e' a cadeia).

## Mudancas de sentido
- leitura: fixos = pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393 + os de ESPERADOS[registros_v393]; escada antes = ESPERADOS[escada_v392_e_v393][0];
  verbatins = ESPERADOS[cunhagens]; novo bloco confere vereditos/numeros do consumidor, do coracao, das cunhagens e da cobertura KH-N1 contra o ensaio a seco (ESPERADOS), fail-closed.
- textos: prosa da regra e do coracao; errata ao lado SO do kh_n1_cobertura_v392 (dentro do bloco datado); a frase do operador citada e' conferida por sha256.
- superficies: sem erratas inline; MEMORY.md tem 200 linhas hoje (limite 195): compacta corridas de ganchos antigos (ja ponteiros) num ponteiro, linhas VERBATIM ao MEMORY_2.
- chain: mesmos passos 0..14 e portoes (PARADA rc 1; AGUARDA_OPERADOR rc 20 em 10a/10c; B(3) aplicar so com B3_AUTORIZADO=sim + EVENTO/EVENTO_HASH; guarda MEMORY.md <24000 B e <=195 linhas).
  b3_prepara reescrita para PINOS_BN_v393.json; sem pino recibo_pre_selo o passo 10 PARA em AGUARDA_OPERADOR; selo/manifesto do kernel anteriores caem em base_v392 (sem pino, hash lido na hora).

## Descartado do molde
- patch_arvore_indice_v392 (CR-08/CR-02), errata_claude_md_v392, nota_handoff, derivar_cadeia_v392. Passos 3/4 tornam-se opcionais (so' se existir patch_arvore_indice_v393.py);
  o passo 7 nao chama errata do CLAUDE.md da raiz. Consequencia: arvore_da_prova.py e atlas_indice.py rodam sem linha nova da v393 (os gerentes trazem v392 embutido).

## Nao validado sem o Nos v393
Execucao real de leitura/superficies/fechar/chain; o campo core (chaves de pedras_v393, regra_consumidor_v393, coracao..., axiom_coverage_v392 em kernel_formalization) foi lido do codigo do runtime, nao do core real;
conferidor, B(3), refazer_arvore e a arvore/indice com o selo v393.

## Riscos
1. Passo 9 exige o sha16 do v393 em A_PROVA_DA_QG_TGL_arvore.md e TGL_INDICE_VIVO.md; sem patch das ferramentas elas podem nao o gravar -> a cadeia para ali (decisao: escrever patch_arvore_indice_v393.py ou relaxar o exige).
2. Igualdades da leitura contra ESPERADOS (veredito, pontos, hash, cobertura): rodada real que difira do ensaio a seco reprova (intencional).
3. Compactacao do MEMORY.md move 14 linhas (verbatim) ao MEMORY_2; confira o ensaio do passo 3 antes do 7.
4. Esboco R3.3 (v392/vinculo) e bateria v392 reusados; conferir se a bateria cobre a v393 (nota do PINOS_BN).
