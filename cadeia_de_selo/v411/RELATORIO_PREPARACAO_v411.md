# RELATÓRIO DA PREPARAÇÃO DA v411 (PRONTA)

> Gerado por `gerar_relatorio_v411.py` em 12/11/2026 23:46; tudo lido dos artefatos; o que não foi lido aparece como portão que não passa. Candidato: `1203b1f9202020d6`; base v410 `5d9497a721c3589e`; escada [12308, 12308]; bandeiras novas: 0; módulos novos: 0.

## Portões (30 de 30 passam; falta: nada)

| portão | estado |
|---|---|
| `topo_ratificado` | passa |
| `kernel` | passa |
| `candidato` | passa |
| `previoo_do_gerador` | passa |
| `registro_h0dn_offline_16` | passa |
| `quadro_e_secao_renderizados` | passa |
| `guarda_das_frases` | passa |
| `ast_v410_v411` | passa |
| `ensaio_a_seco` | passa |
| `registro_h0dn_no_ensaio_16` | passa |
| `guarda_da_conversa_d181` | passa |
| `conferidor_controle_negativo` | passa |
| `conferidor_caminho_positivo` | passa |
| `citacoes` | passa |
| `instalar_reverter_rito_estatico` | passa |
| `p00` | passa |
| `veto_kimi` | passa |
| `material_privado` | passa |
| `bn_pre_selo` | passa |
| `servico_estatico` | passa |
| `guardas_estaticas_bancada` | passa |
| `harness_textos` | passa |
| `harness_fechar` | passa |
| `cadeia_limpa_ate_o_relatorio` | passa |
| `purga_da_fala_reservada` | passa |
| `fala_excluida_fora_dos_artefatos` | passa |
| `varredura_fock_omega` | passa |
| `d135_sem_tmp_e_sem_copias_do_kernel_em_work` | passa |
| `orquestrador_sem_S7_e_sem_S10` | passa |
| `guarda_da_prosa` | passa |

## O teste, do registro

o teste pré-registrado da razão de Hubble local/fundo foi aberto uma vez, depois do commit público do pré-registro; sob o modelo de erros publicado o primário lê 6,11 contra o nulo e −0,61 contra K (ramo 4); ao lado, no mesmo item, as Cefeidas livres leem 4,38 (ramo 6); retrodição sem ajuste, com emenda posterior à guarda, teste não cego; provado é validade, não creditação; o gate não se move. Checagens do registro: 16 de 16 (16 esperadas); origem dos números: o core do ensaio a seco deste candidato (o registro h0dn_bg1_v411 recalculado no ponto de chamada real).

## Avisos

- a excecao ESTREITA da P18 (decisao (c) da gerencia, 12/11): uma funcao so', _v411_p18_sem_cabeca (a mesma no um.py e na cadeia: guarda_frases_v411.p18_sem_cabeca), retira APENAS a cabeca exata que a c7 monta do literal pre-registrado; controles: a exata sai = None; um caractere trocado e' recusado = None; a crua e' recusada = None; o portao de textos da G1 nao tem a R1 (medido pela custodia): a excecao fica so' na cadeia, e a NOTA do handoff diz isso em uma linha
- contratos de registro novos, FORA da escada de teoremas (D135; dizer no handoff): _V411_H0DN_CONTRACT
- as erratas AO LADO, em nome proprio da gerencia c1: E41: errata da gerência c1, em nome próprio: o docstring de `veredito_h0dn_v411` (módulo pinado) ainda põe a centragem dentro do primeiro portão; o código de `abrir` a trata como conferência interna (recusa de integridade). Vale o texto do pré-registro e o código; o módulo pinado não é tocado.; E42: errata da gerência c1, em nome próprio (A1 da revisão da v410): o colchete “[REAL o limiar de um pixel; INPUT/dicionário a leitura do operador]” ficou em duas linhas da v410 contra a regra do nome (D122, D123); lê-se “definição e nome do operador”. O texto selado da v410 não é reescrito; a errata vai ao lado.; E43: errata da gerência c1, em nome próprio (as seis aberturas da seção da Escala, no texto selado da v410): onde as seis aberturas identificam o operador contra a regra do nome (D122, D123), lê-se “por definição e nome do operador”; o texto selado da v410 não é reescrito e o artigo regenerado não diverge do registro selado; a errata vai ao lado.; E44: errata da gerência c1, em nome próprio (a seção “O teste pré-registrado da razão de Hubble com a rede de distâncias (H0DN × BG1)”, texto selado da v410 que o artigo da v411 traz igual): a seção descreve o estado da v410, de 09 a 11/11/2026. Onde ela diz “esta versão”, “nesta versão” e “hoje”, lê-se a v410. Onde diz que nenhum dado observado é lido, que o um.py não lê esse vetor e que a abertura é de versão futura, lê-se: assim era na v410; a versão futura é a v411, em que o vetor está embutido e o resultado é recalculado no rito. Onde trata o vetor fora do suporte como parede de montagem do dado, leia-se: é propriedade do modelo de erros publicado (o achado da gerência de 11/11 e a emenda, D162); não é erro de montagem. Onde condiciona a abertura a uma certificação prévia, às cegas, sob a covariância física, lê-se: a condição foi substituída em 11/11 pelo desenho ratificado (D159), com o primário no modelo de erros publicado e o portão de 90 % de poder de desenho; a certificação não existiu e o teste aberto não é cego (ressalvas 1, 4 e 6). E onde textos de versões anteriores (o parágrafo “O que não se declara”, da v392, e a cadeia de máquina do registro estatuto_da_prova_v391) dizem que β na natureza a 5σ aguarda instrumento, vale o ao lado da v411 no estatuto da prova. O texto selado não é reescrito; a errata vai ao lado.
- as traducoes EN (o titulo do quadro do topo e a frase EN ao lado do estatuto da prova) sao do construtor e ficam marcadas para a revisao de terceiro (decisao (e) da gerencia)
- a tolerancia do recalculo segue 1e-09; o medido no ensaio offline foi {"t": 0.0, "z_null": 0.0, "z_tgl": 0.0, "support_l2": 0.0, "D_s0": 0.0} (decisao (g) da gerencia)
- a contagem de arquivos da pasta da cadeia, para o handoff: 1184 (806 sem os backups; 378 backups), no momento deste relatorio
- as copias do kernel por rodada ficam FORA de work (D135): C:\t\k411c\arvore_simulada_h8, C:\t\k411c\arvore_simulada_h8, C:\t\k411c\dry_v411, C:\t\k411c\ensaio_topo_proposto, C:\t\k411c\falso_nos_v411, C:\t\k411c\final, C:\t\k411c\imp_1203b1f9202020d6, C:\t\k411c\imp_21e87eb3df5098f8, C:\t\k411c\imp_652eaa4f201682bc
- o orquestrador (orquestrador/pos_treino_v411.py) sem S7 e sem S10, MEDIDO no laco de passos = True; o fim da cadeia desta versao e' o HANDOFF; a custodia, o site e o X sao da sessao de custodia

## Revisão

a revisao de terceiro (revisao_terceiro/REVISAO_TERCEIRO_v411.json, rodada conferência única do conserto da R1 (D109), revisor Sonnet 5.5 (agente de conferencia unica; NAO construiu a v411 nem fez o conserto da R1: quem constroi nao aprova)) APROVOU este candidato (1203b1f9202020d6): 0 ALTO, 0 MEDIO, 17 BAIXO; quem constroi nao aprovou: o revisor aprovou.

## Arquivos (sha16 lidos)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v411_candidato.py` | 46,828,680 | `1203b1f9202020d6` |
| `CANDIDATO_v411.json` | 17,067 | `6d0b3d152b30834a` |
| `ESPERADOS_v411.json` | 1,381,636 | `ebc42fbb9532d9eb` |
| `ensaio_a_seco_v411.json` | 648,904 | `982039c1845756fb` |
| `COMPARACAO_V410_v411.json` | 11,474 | `52efa1e3f43ac3c7` |
| `conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json` | 46,444 | `5650c446611e8fe8` |
| `conferencia_rito_v411_POSITIVO_FALSO_NOS.json` | 49,206 | `bf80ee67486ed444` |
| `conferir_citacoes_v411.json` | 3,651 | `01a500dc860281cd` |
| `DERIVACAO_v411.json` | 8,624 | `4511542d2dbaf931` |
| `PINOS_BN_v411.json` | 21,182 | `167db24cf08ce090` |
| `PINO_RECIBO_PRE_SELO_v411.json` | 6,215 | `91f2890cb0c32f0b` |
| `PROVA_PRODUCAO_INTACTA_v411_pre_selo.json` | 10,061 | `edcb343d7470bf28` |
| `PRECONDICOES_v411.json` | 8,098 | `50be8067b34c84ea` |
| `GUARDAS_ESTATICAS_BANCADA_v411.json` | 3,709 | `fd58b143e2d95b6d` |
| `VARREDURA_FOCK_OMEGA_v411.json` | 3,238 | `7c28ecd1ac1ab345` |
| `purga_v411.json` | 515 | `9aeba85eb0c4dbf7` |
| `bancada_B3_servico\CONFERENCIA_EXIGENCIAS_SERVICO_v411.json` | 10,587 | `48b8bcea04fc74de` |
| `bancada_B3_servico\controle_negativo\RESULTADO_CONTROLE_NEGATIVO_v411.json` | 15,120 | `33c33fa715198299` |
| `pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json` | 441,588 | `41350c73f74aae72` |
| `pos_rito\HARNESS_FECHAR_SANDBOX_v411.json` | 44,060 | `2979bbfdda34edc8` |
| `kernel\KERNEL_RECIBO_v411.json` | 2,565 | `65393b056e719c17` |
| `kernel\POS_BUILD_v411.json` | 1,454 | `0be4e13f54d71f28` |
| `TESTE_H0DN_OFFLINE_v411.json` | 10,664 | `131dd59ce00b116f` |
| `TESTE_QUADRO_v411.json` | 1,253 | `6073efc7f7bdbde8` |
| `GUARDA_FRASES_v411.json` | 11,639 | `6780845a24534ba8` |
| `PREVOO_GERADOR_v411.json` | 17,302 | `aed8e2ef1484150e` |
| `DESENHO_v411.md` | 41,846 | `e85ea69f0dbe11b9` |

## Pendências do p00 (atos da gerência, quando houver)

- nenhuma lida
