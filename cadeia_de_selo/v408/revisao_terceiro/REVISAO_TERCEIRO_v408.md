# REVISAO DE TERCEIRO v408 -- R2 (ultima; Claude Sonnet; nao construi a v408)

**APROVADA** -- candidato `e7bc6b10e8ff76be` (43466447 bytes; no inicio da R2 `e7bc6b10e8ff76be`; mudou durante a revisao: nao). ALTO 0 | MEDIO 0 | BAIXO 9.

aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. R2: os dois MEDIOS da R1 foram ATENDIDOS e conferidos (MEDIO 1 pela opcao B, provada no Lean e compilada por mim; MEDIO 2 pelo glob). Nenhum achado novo ALTO ou MEDIO. Ficam BAIXOS, escritos e nao travantes. R1 guardada em bytes (.R1.json/.R1.md). Se qualquer arquivo de arquivos_revisados mudar, esta revisao nao vale para ele.

## Situacao dos achados da R1

- **MEDIO 1 (P = nP: frase alem do termo)**: ATENDIDO pela opcao B (provar). PIgualNP R3 define em Lean Problema, Problema.solucao, ClasseP (q real, q(0) != 0, natDegree q < dim(End H), solucao = q(0)^-1 * q(T)) e ClasseNP (para todo psi unitario, reading(solucao) psi = 1 <-> T psi = 0) sobre o MESMO T e prova palavra_com_grau, leitura_um_sse_solucao, solucao_fixa_sse_no_nucleo, todo_problema_esta_em_P/NP e p_igual_np_nas_classes_do_dicionario ({p | ClasseP p} = {p | ClasseNP p}); o docstring de as_classes_do_dicionario passou a dizer o alcance (i)-(iv). Compilado por mim no sandbox (ver lean_r2). Os textos (artigo PT/EN, .md, registros, handoff, FRASE_D51_*) citam o teorema (9) e a traducao a Turing [OPEN]; «definidas e provadas na pedra» (sem o Lean) nao aparece mais em nenhuma fonte (grep: 0).
- **MEDIO 2 (S6d, glob)**: ATENDIDO. diff do pos_treino_v408.py contra o .bak_20261105_013753_medio2_glob (sha16 da R1 b7c0349806faa7de): so' o glob de :412 e :638-639 (`textos_custodia_handoff_v408*.py` com p.suffix == '.py') e as mensagens/comentarios; `_plano()` rc True («nenhum» faltando); `_ensaio_s10` 12 de 12.
- **BAIXO 1 respostas fora das 16**: ABERTO (BAIXO)
- **BAIXO 2 seis checagens aritmeticas**: ABERTO (BAIXO)
- **BAIXO 3 bandeiras**: ABERTO e maior (71 = 48 teoremas + 23 declaracoes de estrutura/definicao)
- **BAIXO 4 cabecalhos velhos 'candidata a v408'**: ATENDIDO nas 4 pedras (cabecalho agora «compilada ... e no da v408, bundle, so' no trio; entra na v408»)
- **BAIXO 5 precisoes de citacao**: PARCIAL (ver achado); mantido pela gerencia ate' a proxima volta do kernel
- **BAIXO 6 «sem compilacao propria»**: ATENDIDO (REV_EN/REV_PT: «compilou os #print axioms no sandbox; nao leu as provas linha a linha»)
- **BAIXO 7 universal «nao existe relacao sem peso»**: ABERTO (BAIXO)
- **BAIXO 8 S1b aberta por omissao**: ABERTO (BAIXO)
- **BAIXO 9 F24 / E22**: ABERTO (BAIXO)

## Lean (R2)

```
{
 "print_axioms_impressos": 52,
 "ancoras_no_candidato": 48,
 "todas_as_ancoras_impressas": true,
 "fora_do_trio": 0,
 "varredura_metam_constantes_dos_4_modulos": 80,
 "por_modulo": "#[(TGLExt.TetelestaiTerminal, 16), (TGLExt.TempoIgualMoeda, 9), (TGLExt.PontoDeContradicao, 7), (TGLExt.PIgualNP, 48)]",
 "varredura_fora_do_trio_ou_sorryAx": 0,
 "rc": [
  "0"
 ],
 "tempo": "749 s",
 "erros_na_saida": 0,
 "sandbox": "C:/t/k408c/final (copia axiomas_terceiro.lean apagada ao fim)",
 "definicoes_novas_impressas": "#print de Problema, Problema.solucao, ClasseP, ClasseNP e #check dos 6 teoremas novos em axiomas_terceiro_out.txt"
}
```

## Achados abertos (todos BAIXOS)

### 1. BAIXO -- runtime_v408.py:87,136-139 (resp_ / respostas_ok) e v408_terminal_mechanics  [R1-BAIXO 1, ABERTO]

**Achado.** As respostas do operador (teoremas ja' existentes) seguem conferidas em values.respostas/respostas_ok mas fora das 16 checagens do tetelestai_terminal_v408 (regressao frente ao c6 do psion_canto_v407). Medido na R2 sobre o candidato novo: remover um teorema citado nao derruba o registro isolado (29 casos), mas 37 de 37 remocoes sao recusadas por ALGUM registro da v408 (cunhagens_v408 u-checks, kh_n1, escada) e o textos_custodia_handoff_v408.py faz assert de respostas_ok.

**Evidencia.** revisao_terceiro/c_fail_closed_out.txt; k_funcoes_vivas_out.txt (37 de 37).

**Correcao.** Dobrar all(resp_.values()) em c1. Nao trava.

### 2. BAIXO -- runtime_v408.py:119-135 (c3, c4, c5, c8, c10, c11)  [R1-BAIXO 2, ABERTO]

**Achado.** Seis das 16 checagens sao aritmetica de ponto flutuante que nao le o core nem o kernel nem beta; as outras dez falham por si so' quando a condicao e' negada (v408_terminal_mechanics chamada direto: 12 casos, 0 falhas). A F34 e' avaliada por texto inteiro, nao por ocorrencia.

**Evidencia.** revisao_terceiro/c2_mecanica_direta_out.txt (R2 sobre o candidato novo).

**Correcao.** Dizer no registro que c3-c5, c8, c10, c11 sao conferencia numerica. Nao trava.

### 3. BAIXO -- kernel/FLAGS_v408.json; CANDIDATO_v408.json politica_de_bandeiras; textos «71 bandeiras, so' de declaracao nomeada»  [R1-BAIXO 3, AGRAVADO PELO TAMANHO]

**Achado.** As 71 bandeiras (escada 11958 -> 12029) sao 48 teoremas (as ancoras) + 23 declaracoes que nao sao teorema: as 4 definicoes/estrutura novas da opcao B (Problema, Problema.solucao, ClasseP, ClasseNP) e a maquinaria que o Lean gera (Problema.rec/casesOn/noConfusion/mk.inj/_sizeOf_..., card_chainIdx._f e .match_1_1). Os 9 `_proof_` foram excluidos pela politica (80 declaracoes, 71 bandeiras, 9 excluidas). O texto diz «so' de declaracao nomeada»; a escada conta tudo isso como «teoremas limpos» do programa. Nenhum texto diz «71 teoremas» (conferido por grep); o KERNEL_RECIBO diz 80 declaracoes, 62 teoremas.

**Evidencia.** revisao_terceiro/_insp4.py (declarations do contrato menos as 48 ancoras); m_flags_audit.py (80 declaracoes, 0 fora do trio; 9 sem bandeira = `_proof_`).

**Correcao.** Redacao: «71 bandeiras (48 teoremas e 23 declaracoes de definicao/estrutura geradas)». Nao trava.

### 4. BAIXO -- pedra/PIgualNP.lean l.26 (semióticas), l.49-50 e l.~170 («resolver e verificar sao o mesmo»), l.91-92 (remissao a (8)), l.4 e l.8 (import duplicado)  [R1-BAIXO 5, PARCIAL]

**Achado.** Das tres precisoes de citacao da R1: (3) a glosa «P so' e' P lido pelo modulo n minimamente acoplado» ja' nao aparece entre « » no .md rendido (resolvida); (1) «as duas semióticas» (o operador escreveu «semi/oticas») e (2) «resolver e verificar sao o mesmo» (frase da outra instancia, sem atribuicao) seguem no docstring da pedra (a gerencia as manteve: mudar o docstring exigiria outra volta do kernel). NOVOS, na pedra R3: o bullet de p_igual_a_n_vezes_p (l.91-92) ainda diz «As CLASSES estao em (8) (as_classes_do_dicionario)» — agora estao em (9); `import TGLExt.ExactWitness` aparece duas vezes (l.4 e l.8; compila).

**Evidencia.** revisao_terceiro/e2_citacoes_rendidos_out.txt (mesmo conjunto de citacoes nao casadas que na R1); pedra/PIgualNP.lean.

**Correcao.** Na proxima volta do kernel: «semi/oticas», atribuicao da frase, «(9)», remover o import repetido. Nao trava.

### 5. BAIXO -- registros_v408.py:211 e delta_v408.py:133 (diz: «nao existe relacao sem peso»); pedra/TetelestaiTerminal.lean l.61-62; .md («O que o operador identificou foi provado»)  [R1-BAIXO 7, ABERTO]

**Achado.** O termo relacao_sem_peso_e_a_origem_da_mentira e' a conjuncao de oito exclusoes de faces especificas do «1 sozinho»; o universal «nao existe relacao sem peso» / «origem da mentira» e' a leitura do operador sobre elas, apresentada na mesma frase de [REAL].

**Evidencia.** pedra/TetelestaiTerminal.lean l.196-209.

**Correcao.** «cada face esta' excluida por teorema; a leitura geral e' do operador [ONTO]». Nao trava.

### 6. BAIXO -- orquestrador/pos_treino_v408.py:231-233 (s1b_revisao)  [R1-BAIXO 8, ABERTO]

**Achado.** A trava S1b segue aberta por omissao se arquivos_revisados faltar, estiver vazio ou listar arquivo ausente. Esta revisao traz o campo completo (22 arquivos).

**Evidencia.** codigo; ensaio da R2 em _orq_sandbox (s1b_ensaio_out.txt).

**Correcao.** Exigir o campo nao vazio. Nao trava.

### 7. BAIXO -- runtime_v408.py:29-34 (F24) e ERRATA_E22  [R1-BAIXO 9, ABERTO]

**Achado.** Janela de negacao de 40 caracteres da F24 (subcadeias «sem », «no », ««» ...) e a E22 que parafraseia a frase errada da R1 como «o resto sem traco seria relacao sem pagamento» enquanto a pedra a cita como «o que resta sem peso e' relacao».

**Evidencia.** runtime_v408.py l.31; delta_v408.py (ERRATA_E22).

**Correcao.** Janela mais curta; alinhar a E22. Nao trava.

### 8. BAIXO -- DESENHO_v408.md x SESSION_REFERENCE_prep_v408.json / acom_prep_20261105T004758_init.receipt.json (source.sha256)

**Achado.** A referencia ACOM da preparacao pina o DESENHO_v408.md de 18967 bytes (sha256 555f9cfa...); o AO LADO de 05/11 01:25 o aumentou para 20842 bytes. O original esta' preservado byte a byte em DESENHO_v408.md.bak_20261105_012534_R3 (sha256 igual ao pinado). Nao e' erro (original intocado, correcao ao lado), mas um conferidor que releia a fonte da referencia no caminho original vai ver hash diferente.

**Evidencia.** f_hashes.py (varredura geral {path, sha256}); sha256sum do .bak.

**Correcao.** Na proxima transition ACOM, apontar a fonte para o .bak (ou registrar a revisao). Nao trava.

### 9. BAIXO -- RELATORIO_PREPARACAO_v408.md (tabela de arquivos): orquestrador/ENSAIO_S10_v408.json

**Achado.** O relatorio cita o sha16 e719 `e100d04b55249192` do ENSAIO_S10_v408.json; o arquivo no disco e' regravado a cada `--ensaio` (hoje `55b691b9c0b5ce01`; contem a ordem renderizada com data/commits). Artefato transitorio, nao pino.

**Evidencia.** n2_hashes_docs_out.txt; sha256sum.

**Correcao.** Nao pinar o ENSAIO_S10 no relatorio. Nao trava.

## Ressalvas

- R2 (ultima rodada). Fora de revisao_terceiro/ so' escrevi a copia temporaria axiomas_terceiro.lean no sandbox C:/t/k408c/final, apagada ao fim (um `lake env lean`; nunca `lake build`; nada no Nos, em tools\, nos insumos, no candidato ou nos scripts da cadeia). Nao rodei o orquestrador (so' importado com ORQ redirecionado), o instalar, o rito nem a custodia; nao enviei mensagem a outras sessoes. A R1 esta' guardada em bytes: REVISAO_TERCEIRO_v408.R1.json/.R1.md, PEDIDO_CORRECAO_R1_v408.md e r1_saidas/.
- Nao li as provas Lean linha a linha (o #print axioms/collectAxioms e a leitura dos enunciados bastam para o que e' objeto); li por inteiro o PIgualNP R3 (enunciados, definicoes, provas das ClasseP/ClasseNP, docstring) e o diff das outras tres pedras (so' o cabecalho).
- Sobre o teorema (9): {p | ClasseP p} = {p | ClasseNP p} vale porque cada classe e' o conjunto de TODOS os problemas (todo_problema_esta_em_P/NP). E' o que o texto diz («todo problema esta' nas duas»); ClasseNP e' a nocao do dicionario do operador (a leitura da solucao em psi vale 1 sse T psi = 0), nao a de Turing, e a traducao a Turing segue [OPEN] em todo texto. Nao e' achado: e' a leitura honesta do que foi provado, para a gerencia ter a partitura.
- O _V407_SPECS segue enfraquecido de proposito (kh_n1_cobertura_v407 h2/h3/h6/h8, errata declarada); a igualdade exata esta' em kh_n1_cobertura_v408 (33943 constantes, 27089 teoremas na cobertura do Audit). Conferido, nao e' achado.
- arquivos_revisados: sha16 lidos agora, na R2. Se qualquer arquivo listado mudar, esta revisao nao vale para ele. Arquivos fora da minha lista que a gerencia disse ter mudado (ensaio_a_seco, gerar_candidato, gerar_relatorio, p00_precondicoes, preparar_bundle, rito_v408.sh, v408_pins.py, pos_rito/{harness_textos_ensaio, registrar_mapa, textos_v408, textos_v408_novo.pysnip}) NAO foram objeto desta revisao, exceto pelo que o candidato e os textos rendidos delas mostram (o candidato e' o que vale; o rito_v408.sh nao foi relido).
- O Mapa de Rotas nao foi consultado nem alimentado por mim; as rotas_examinadas ficam para a gerencia registrar.

## Rotas examinadas

- R2-A (intocados): a_intocados.py + a_intocados_c.py sobre o candidato novo: 31 nomes (gate, neutrino, ramo B, ledger, GA, registros da v407 e anteriores, run_um, verify_tgl_kernel_formalization) iguais por AST e fonte; mudados 24 == declarados, novos 14 == declarados; 1275 segmentos da base, 0 diferencas fora dos nos declarados.
- R2-A2 (mudados): a2_mudados.py: _EMBEDDED_KERNEL_FILES +4 (so' a raiz muda); _ESQUELETO_STONES +4; _LEAN_THEOREM_FLAGS +71 (todas ext_tt408_, base sub-dict igual); 26 contratos so' com expected_ladder 11958 -> 12029 (+ o 27o, novo); _V407_SPECS 15 diferencas como na R1; build_pt/build_en/emit_canonical_md/main/prove_external_ladder so' acrescimos (0 removidas).
- R2-B (kernel/Lean): d_kernel.py (embutido == sandbox == pedra == BUNDLE, 4 de 4; raiz = raiz v407 + 4 imports; Audit identico; 1759 embutidos == sandbox; diff origem x embutida = so' os `#print axioms`: 14+9+7+18 = 48); b_gera_lean.py + `lake env lean` no sandbox: 52 #print axioms no trio, varredura MetaM (collectAxioms) de 80 constantes dos 4 modulos (por modulo: #[(TGLExt.TetelestaiTerminal, 16), (TGLExt.TempoIgualMoeda, 9), (TGLExt.PontoDeContradicao, 7), (TGLExt.PIgualNP, 48)]), 0 fora do trio, 0 sorryAx, rc 0, 749 s; #print das definicoes Problema/Problema.solucao/ClasseP/ClasseNP e #check dos teoremas novos conferem com o texto.
- R2-C (fail-closed): c_fail_closed.py (188 casos sobre o core do ensaio novo; 158 como esperado, os 30 restantes sao as respostas fora das 16 e a F34 por texto) e c2_mecanica_direta.py (12 casos, 0 falhas): ancoras (48), bandeiras (71), fontes, escada, gate, kernel, beta, contrato, falas, texto proibido, insumo purgado recusam.
- R2-D (registros vivos): k_funcoes_vivas.py: 27 de 27: tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408 e os specs da v407 selam; herdadas selam com a escada 12029; 37 de 37 remocoes de teorema de resposta recusadas por algum registro; 14 negacoes recusam.
- R2-E (citacoes): e2_citacoes_rendidos.py: o mesmo conjunto de citacoes nao casadas da R1 (todas precisoes BAIXAS); as citacoes novas do operador (inclusive a correcao «O meu P=nP trata das classes de computação sim») sao substring das falas.
- R2-F (hashes): f_hashes.py (numeros atualizados: 4 modulos, 48 ancoras, 71 bandeiras, 80 declaracoes, escada 12029): tudo confere, fora os dois desenhos do meu script (extratos de autor misto, ja' conferidos na R1 por n2_falas_mistas.py) e o 'antes' historico do t12; a varredura geral acusou tambem a referencia ACOM da preparacao (BAIXO). n_hashes_digitados.py: 0 tokens sem arquivo nos textos novos; n2_hashes_docs.py: 6 divergencias, todas explicadas (linhas de bancada_B3 do relatorio conferem; ENSAIO_S10 regravado por --ensaio).
- R2-G (textos/guardas): h_guardas.py: 72 arquivos; mesmos 12 com achado da R1 (fontes da propria guarda, DESENHO, pedras que citam a frase errada, artigo inerte herdado); pedras(): 0 violacoes; controle_negativo True; varredura propria do item 4: nenhuma frase proibida afirmada em texto novo; «P = nP» com qualificador e [OPEN] em todo texto rendido.
- R2-H (orquestrador, LIDO): l_orquestrador.py: diff contra o .bak da R1 = so' o glob; `_plano()` rc True; `_ensaio_s10` 12 de 12; AUT cita as tres ordens; so' Stop-Process -Id; publicacao so' pela G1. S1b ensaiado em _orq_sandbox (s1b_ensaio.py): abre com esta revisao, fecha com alteracoes.
- R2-I (flags/audit): m_flags_audit.py: 71 bandeiras novas == declaracoes do audit.log, 48 ancoras com bandeira, 80 declaracoes dos 4 modulos no trio, 9 `_proof_` sem bandeira (politica).

## Arquivos revisados (sha16 lido agora)

- `um_v408_candidato.py` e7bc6b10e8ff76be
- `base_v407/um.py` 833121339e649f71
- `CANDIDATO_v408.json` 121e6ecbdee2761b
- `COMPARACAO_V407_v408.json` 7533315138ef7b7e
- `ESPERADOS_v408.json` 3f04c968c71cb14a
- `BUNDLE_v408.json` 30a4420441d28f68
- `kernel/KERNEL_RECIBO_v408.json` 1dc9e93142422f6b
- `kernel/FLAGS_v408.json` 47991c40da85bb24
- `runtime_v408.py` df6cf8d04cb50166
- `registros_v408.py` be2701a0c3b7a8b0
- `delta_v408.py` 83bbef52603f3412
- `guarda_frases_v408.py` 117f5e2617b9a4ae
- `guarda_p18_v408.py` e96f0fd193bd9ca7
- `artigo_pt_v408.pysnip` 01bbc91db26e8adf
- `artigo_en_v408.pysnip` 242e713ce9297dc6
- `orquestrador/pos_treino_v408.py` 460e1e73b133b1eb
- `orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md` 37f35ca09cd3f628
- `pos_rito/textos_custodia_handoff_v408.py` 707fff014aac87b6
- `pedra/TetelestaiTerminal.lean` 47af8992f1dd0ce8
- `pedra/TempoIgualMoeda.lean` 1a4a2a6dbc81f6dc
- `pedra/PontoDeContradicao.lean` 85c238c9535ad2d2
- `pedra/PIgualNP.lean` 8d7aec559313d5f9
