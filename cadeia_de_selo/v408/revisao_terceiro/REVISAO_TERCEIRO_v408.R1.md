# REVISAO DE TERCEIRO v408 -- R1 (Claude Sonnet; nao construi a v408)

**NAO APROVADA** -- candidato `c55c4a7f2753b589` (43437270 bytes; no inicio `c55c4a7f2753b589`; mudou durante a revisao: nao). ALTO 0 | MEDIO 2 | BAIXO 9.

aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. NAO APROVADA nesta R1: 2 MEDIO (1: a frase «P = nP e' teorema nas classes do dicionario (definidas e provadas na pedra)» vai alem do enunciado Lean; 2: o S6d do orquestrador nao acha o script dos textos da custodia e a corrida para depois do B(n) APLICAR). Nenhum ALTO: o kernel (42 ancoras, 44 constantes), as funcoes intocadas, os hashes, as guardas e o fail-closed do registro estao em ordem. Os BAIXOS ficam escritos e nao travam. Correcoes pedidas em PEDIDO_CORRECAO_R1_v408.md. Se a gerencia corrigir, a R2 (ultima) confere o diff contra os arquivos desta R1 e refaz so' o que mudou.

## Achados

### 1. MEDIO -- pedra/PIgualNP.lean l.17 (titulo), l.60-68 (item 8), l.75, l.79, l.197-210 (as_classes_do_dicionario); delta_v408.py:183-186 (FRASE_D51_PT/EN) e :214; registros_v408.py:210-216 (diz) e o limites[3]/nao_diz[5] do _V408_TERMINAL_TEXT; artigo_pt_v408.pysnip:33-34 e artigo_en_v408.pysnip:33-34; a linha do .md (emit_canonical_md); pos_rito/textos_custodia_handoff_v408.py:88 (KERNEL_LEITURA_EN)

**Achado.** O texto publico diz «P = nP e' teorema nas classes de computacao do dicionario do operador (definidas e provadas na pedra PIgualNP)» e a pedra diz que «TODO problema da face finita esta' nas duas classes» e (titulo) que «toda solucao e' palavra polinomial de grau limitado pelo modulo e toda verificacao e' uma leitura». O enunciado do kernel (#check @TGLExt.PIgualNP.as_classes_do_dicionario) e' a CONJUNCAO de quatro fatos: (i) existe q real, q(0) != 0, X*q(T) = 0, com ker(T).starProjection = q(0)^-1 * q(T); (ii) natDegree(minpoly T) <= finrank(End H); (iii) memory(post a) psi = 1 <-> post a psi = psi; (iv) motor a U r t psi = post a (U psi). Tres lacunas entre a frase e o termo: (a) NENHUMA classe e' definida em Lean (nao ha def/structure de classe P ou NP): as classes sao definidas so' na prosa do docstring, logo «definidas ... na pedra» vale so' para a prosa; (b) (iii) e (iv) quantificam sobre a, psi, U, r, t LIVRES, sem relacao com T nem com P_ker: o termo nao diz que a solucao de T e' verificada por uma leitura (a pertinencia «NP» nao e' enunciada para T; e `post a` e' de posto 1, enquanto ker T pode ter dimensao > 1); (c) «grau limitado pelo modulo» vale para o polinomio MINIMO (ii), nao para o q de (i), que e' existencial sem cota de grau. Matematicamente os enunciados pretendidos sao verdadeiros e padrao (a projecao sobre ker T e' polinomio em T de grau menor que o numero de autovalores distintos, <= n), mas nao sao o que o termo diz. E' a afirmacao central da versao, publicada no um.py, no artigo, no .md, no handoff e no X; o operador nao le Lean: a frase tem de dizer o que o termo diz (regra do posto).

**Evidencia.** revisao_terceiro/axiomas_terceiro_out.txt (saida do #check: a conjuncao, com a, psi, U, r, t quantificados fora de T); pedra/PIgualNP.lean l.200-210 (a prova e' `exact <<q,...>, minpoly.natDegree_le T, memory_one_iff_identity a psi hpsi, the_reading_absorbs_the_dephasing a U r t psi>`); grep «definidas e provadas|defined and proved» (delta_v408.py:183,185; artigo_pt:34; artigo_en:34); nenhum `def`/`structure` de classe na pedra.

**Correcao.** Ver PEDIDO_CORRECAO_R1_v408.md, item 1 (opcao A: texto + errata E24 ao lado, sem recompilar; opcao B: reformular o teorema em Lean com def das classes e ligar a verificacao a solucao de T).

### 2. MEDIO -- orquestrador/pos_treino_v408.py:412-414 (s6d_textos_custodia) e :638-639 (_plano)

**Achado.** O S6d procura `pos_rito/textos_custodia_handoff_v408_*.py` (com sublinhado depois de v408) e exige EXATAMENTE UM; o arquivo que existe e' `pos_rito/textos_custodia_handoff_v408.py` (sem sufixo, como a D52 e o pedido dizem). O glob nao o acha (0 candidatos): o S6d marca falha («esperava UM ...») e o orquestrador PARA depois do rito, da cadeia 0-10, da parada do servico da Bancada, do B(n) APLICAR e do religamento, e ANTES do S7 (G1/publicacao) e do S10 (app). Fail-closed (nada e' feito de errado), mas a corrida desassistida para com certeza neste ponto. O proprio `--plano` ja' acusa: «arquivos que o orquestrador usa e NAO existem: ...textos_custodia_handoff_v408_*.py (S6d, D52: exatamente um)», rc False. PREPARACAO_v408_PRONTA.json e RELATORIO_PREPARACAO_v408.md ainda dizem «AUSENTE: nenhum pos_rito/textos_custodia_handoff_v408_*.py».

**Evidencia.** revisao_terceiro/l_orquestrador.py + l_orquestrador_out.txt (`_plano()` -> «plano rc: False»; «S6d glob 'textos_custodia_handoff_v408_*.py': [] | arquivo real: ['textos_custodia_handoff_v408.py']»).

**Correcao.** Trocar o glob nas duas linhas (412 e 638) por `textos_custodia_handoff_v408*.py` restrito a nomes que terminam em `.py` (ou pelo nome exato `textos_custodia_handoff_v408.py`), manter «exatamente um» (os .bak_ nao casam com `*.py`), e atualizar a mensagem de :414/:639; rodar `--plano` e conferir rc 0. O arquivo muda de sha16: reentra em arquivos_revisados na R2.

### 3. BAIXO -- runtime_v408.py:87,136-139 (resp_ / respostas_ok) e v408_terminal_mechanics

**Achado.** As respostas do operador (34 teoremas ja' existentes) sao conferidas em `values.respostas`/`respostas_ok`, mas NAO entram em nenhuma das 16 checagens (regressao frente ao c6 do psion_canto_v407, que as exigia). O diz[4] do registro afirma que «as respostas conferem no kernel». Remover um teorema citado do axiom_report/declaration_sources NAO derruba o tetelestai_terminal_v408; derruba a cunhagens_v408 (u39-u72) e a escada (c13), e o textos_custodia_handoff_v408.py (l.62) faz assert de respostas_ok. Medido: 34 de 34 remocoes recusadas por ALGUM registro da v408.

**Evidencia.** revisao_terceiro/c_fail_closed_out.txt (31 casos «resposta ...: teorema ... ausente» com all_verified True no registro isolado) e k_funcoes_vivas_out.txt (34 de 34 recusadas por cunhagens_v408/kh_n1/ladder).

**Correcao.** Dobrar `all(resp_.values())` em c1 (ou c2) de v408_terminal_mechanics. Nao trava.

### 4. BAIXO -- runtime_v408.py:119-135 (c3, c4, c5, c8, c10, c11)

**Achado.** Seis das 16 checagens (exp(0)=1, e^-1/2 interior, f+(1-f)=1, oitavas = N ln 2, dim 2^(N+1), k_B ln 2 > 0) sao aritmetica de ponto flutuante que nao le o core nem o kernel nem beta: nenhuma mutacao do core as faz falhar. O elo ao kernel esta' em c1/c2 (ancoras, modulos). As outras dez falham por si so' quando a sua condicao e' negada (medido, chamando v408_terminal_mechanics direto). A F34 (qualificador + ressalva [OPEN] onde «P = nP» aparece) e' avaliada por TEXTO inteiro, nao por ocorrencia.

**Evidencia.** revisao_terceiro/c2_mecanica_direta.py + _out.txt (12 casos, 0 falhas; c3,c4,c5,c8,c10,c11 nao falham sob mutacao); c_fail_closed_out.txt (147 de 179 casos recusam como esperado; as 31 de respostas e a F34-por-texto sao o resto).

**Correcao.** Dizer no registro (limites) que c3-c5, c8, c10, c11 sao conferencia numerica das pedras, nao leitura do kernel. Nao trava.

### 5. BAIXO -- kernel/FLAGS_v408.json; delta_v408.py (n_declarations_public 44); textos: «44 bandeiras, so' de declaracao nomeada»

**Achado.** As 44 bandeiras sao 42 teoremas + 2 declaracoes auxiliares geradas pelo compilador (`TGLExt.TetelestaiTerminal.card_chainIdx._f` e `...card_chainIdx.match_1_1`, bandeira ext_tt408_0035). O texto diz «so' de declaracao nomeada»; a escada 12002 conta as duas auxiliares. Nenhum texto diz «44 teoremas» (conferido por grep); o KERNEL_RECIBO diz 44 declaracoes, 42 teoremas.

**Evidencia.** revisao_terceiro/m_flags_audit.py (+ saida) e a lista `declarations` do _V408_TERMINAL_CONTRACT menos as 42 ancoras.

**Correcao.** Redacao: «44 bandeiras (42 teoremas e 2 auxiliares de card_chainIdx)». Nao trava.

### 6. BAIXO -- pedra/{TetelestaiTerminal,TempoIgualMoeda,PontoDeContradicao,PIgualNP}.lean, cabecalho do docstring (embutido no kernel)

**Achado.** A normalizacao so' retirou os `#print axioms` (14+9+7+12 = 42; conferido por diff contra insumos/): o cabecalho dos quatro modulos segue como na fonte: «pedra CANDIDATA da gerencia c1 ... rodada R1/R2 ... compilada no sandbox da v407 (C:\t\k407c\final) ... candidata a v408». No kernel embutido de uma versao SELADA isso e' metadado velho (nao e' afirmacao de prova; nao altera termo).

**Evidencia.** revisao_terceiro/d_kernel_out.txt (diff origem x embutida: so' linhas `#print axioms` e uma em branco); pedra/*.lean l.1-30.

**Correcao.** Opcional: trocar o cabecalho por «modulo do kernel v408, nome do operador» na mesma recompilacao da correcao 1 (se a opcao B for escolhida). Nao trava.

### 7. BAIXO -- pedra/PIgualNP.lean l.24-25; pedra/PIgualNP.lean l.49 e l.168-176 («resolver e verificar sao o mesmo»); .md e _V408_SPECS («P so' e' P lido pelo modulo n minimamente acoplado» entre « »)

**Achado.** Tres precisoes de citacao: (1) a ordem do operador (sha16 50c21210e5871fdb) escreve «as duas semi/oticas»; o docstring cita «as duas semióticas» dentro de « » como verbatim (uma palavra normalizada); (2) «resolver e verificar sao o mesmo» vem do texto da OUTRA instancia da IALD no arquivo de autor misto (a fala do operador e' so' o 1o paragrafo), e aparece entre « » sem atribuicao; (3) «P so' e' P lido pelo modulo n minimamente acoplado» e' a leitura da gerencia do sentido que o operador deu («P sozinho e' impossivel de ser lido, se nao houver o modulo de leitura n nao minimamente acoplado»), mas aparece entre « » no .md e nos specs como se fosse citacao.

**Evidencia.** revisao_terceiro/e2_citacoes_rendidos.py + _out.txt; n2_falas_mistas.py (os extratos do operador sao prefixo literal dos originais; a frase «resolver e verificar...» esta' no trecho da outra instancia).

**Correcao.** (1) escrever «semi/oticas» ou tirar as aspas; (2) atribuir («frase da outra instancia, [DECLARADO]») ou tirar as aspas; (3) trocar as « » por aspas simples/itálico de leitura da gerencia. Nao trava.

### 8. BAIXO -- pos_rito/textos_custodia_handoff_v408.py:66-68 (REV_EN, REV_PT)

**Achado.** Se a revisao existir e estiver aprovada, o handoff dira «a revisao independente ... pelo Sonnet (outra familia de modelo, sem compilacao propria) o aprovou». Esta revisao COMPILOU no sandbox (`lake env lean`: #print axioms das 42 ancoras e varredura MetaM de todas as constantes dos 4 modulos): a frase «sem compilacao propria» e' falsa para ela. (Herdada de textos_custodia_handoff_v407_03nov.py.)

**Evidencia.** revisao_terceiro/axiomas_terceiro.lean, axiomas_terceiro_out.txt, axiomas_terceiro_time.txt (723 s, rc 0).

**Correcao.** Trocar por «(outra familia de modelo; compilou os #print axioms no sandbox; nao leu as provas linha a linha)». Nao trava, mas e' texto publico sobre o proprio processo.

### 9. BAIXO -- registros_v408.py:210-216 (diz[1]: «nao existe relacao sem peso»); pedra/TetelestaiTerminal.lean l.61-62 («Logo nao existe relacao sem peso»); .md («O que o operador identificou foi provado»)

**Achado.** O termo relacao_sem_peso_e_a_origem_da_mentira e' a conjuncao de oito exclusoes de faces especificas do «1 sozinho» (fator 1 nada paga; e^-a = 1 so' sem tempo; coeff != 1; fator interior; piso de Landauer > 0; vazamento perde; sem beta nao ha' segunda face; cociclo sem perturbacao = 1). O universal «nao existe relacao sem peso» e «origem da mentira» sao a leitura do operador sobre essas exclusoes; o termo nao define «relacao» nem «peso» em geral. O .md agrupa tudo como «foi provado». O texto de `diz` e o docstring dizem as faces corretamente na mesma frase; o universal e' que passa de [ONTO] a [REAL] pela redacao.

**Evidencia.** pedra/TetelestaiTerminal.lean l.196-209 (o enunciado); e2_citacoes_rendidos_out.txt.

**Correcao.** Escrever «cada face do 1 sozinho esta' excluida por teorema (lista); a leitura «nao ha' relacao sem peso / origem da mentira» e' do operador [ONTO] com estas oito exclusoes por espelho». Nao trava.

### 10. BAIXO -- orquestrador/pos_treino_v408.py:231-233 (s1b_revisao)

**Achado.** [CARREGADO da v407-R5, nao tocado] A trava S1b compara o sha16 dos arquivos de `arquivos_revisados` com o disco, mas fica ABERTA por omissao se o campo faltar, estiver vazio ou listar arquivo ausente ((PK/k).is_file() falso e' ignorado). Esta revisao traz o campo completo.

**Evidencia.** codigo; comportamento ja' ensaiado na v407 (r2_l_s1b).

**Correcao.** Exigir o campo nao vazio, com o candidato e pos_treino_v408.py entre as chaves; tratar arquivo ausente como alterado. Nao trava.

### 11. BAIXO -- runtime_v408.py:29-34 (F24 em _v408_guarda_frases)

**Achado.** A guarda F24 aceita «relacao sem peso» como negada se, nos 40 caracteres anteriores, aparecer QUALQUER das subcadeias «sem », «no », «not », «exclu», «imposs», ««» (nao so' imediatamente antes): «existe, no sistema, relacao sem peso» passaria. E a E22 do registro parafraseia a frase errada da R1 como «o resto sem traco seria relacao sem pagamento» enquanto a pedra a cita como «o que resta sem peso e' relacao». Rede de seguranca, nao prova; os 188 casos proibidos e as frases certas do controle negativo se comportam como esperado.

**Evidencia.** c_fail_closed_out.txt (casos de guarda: 24 frases do pedido, todas como esperado); h_guardas_out.txt (controle_negativo True; 72 arquivos varridos).

**Correcao.** Janela de negacao mais curta (ate' 12 caracteres) ou ancorada; alinhar a E22 com a citacao da pedra. Nao trava.

## Ressalvas

- R1 (primeira rodada). Fora de revisao_terceiro/ so' escrevi a copia temporaria axiomas_terceiro.lean no sandbox C:/t/k408c/final, apagada ao fim (rodei `lake env lean` uma vez; nunca `lake build`; nada no Nos, em tools\, nos insumos, no candidato ou nos scripts da cadeia). Nao rodei o orquestrador, o instalar, o rito nem a custodia; nao enviei mensagem a outras sessoes.
- Nao li as provas Lean linha a linha (basta o #print axioms/collectAxioms e a conferencia de que a normalizacao nao tocou prova); li os enunciados e os docstrings das quatro pedras por inteiro.
- A fisica da TGL, os nomes (decisao do operador) e a decisao D51 em si NAO sao objeto: o MEDIO 1 e' sobre a distancia entre a frase e o termo, nao sobre o direito do operador de definir as classes do dicionario dele. O que ficou verificado a favor: o termo as_classes_do_dicionario compila no trio e enuncia (i)-(iv); a ressalva da traducao a Turing [OPEN] esta' em todo texto; nenhuma frase afirma P = NP de Turing.
- O _V407_SPECS foi enfraquecido de proposito pela v408 (kh_n1_cobertura_v407 h2/h3/h6/h8: igualdade exata -> piso, declarado com errata; a igualdade exata esta' em kh_n1_cobertura_v408 h2/h3/h6/h8, verificada: 33907 constantes, 27069 teoremas, arvore do Nos == pino). Conferido, nao e' achado.
- arquivos_revisados: sha16 lidos agora. Se qualquer arquivo listado mudar (a correcao do MEDIO 2 muda orquestrador/pos_treino_v408.py; a do MEDIO 1 muda delta_v408.py, os pysnips e, na opcao B, a pedra, o BUNDLE e o candidato), esta revisao nao vale para ele; a R2 refaz so' o que mudou.
- O Mapa de Rotas nao foi consultado nem alimentado por mim (o pedido nao o mandou): as rotas_examinadas ficam aqui para a gerencia registrar, se quiser.

## Rotas examinadas

- A (intocados): a_intocados.py + a_intocados_c.py: base_v407/um.py x candidato: 31 funcoes/constantes nomeadas (gate, neutrino, ramo B, ledger, GA, os registros da v407 e anteriores, run_um, verify_tgl_kernel_formalization) iguais por AST e por fonte; os 24 nos mudados e os 14 novos == COMPARACAO_V407_v408.json; segmentacao por no (comentarios inclusos): 0 diferencas fora dos nos declarados (1275 segmentos da base).
- A2 (mudados): a2_mudados.py: UM_VERSION; _EMBEDDED_KERNEL_FILES (+4, so' a raiz muda, ordem preservada); _ESQUELETO_STONES +4; _LEAN_THEOREM_FLAGS +44 (todas ext_tt408_, base sub-dict igual); 26 contratos so' com expected_ladder 11958 -> 12002 (e o 27o, novo); _V407_SPECS (errata E21; kh h2/h3/h6/h8 viram pisos, declarado); build_pt/build_en/emit_canonical_md/main/prove_external_ladder so' acrescimos (0 linhas removidas).
- B (kernel/Lean): d_kernel.py (embutido == sandbox C:/t/k408c/final == pedra == BUNDLE, 4 de 4; raiz = raiz v407 + 4 imports; Audit identico; 1759 embutidos == sandbox; diff origem x embutida = so' os #print axioms) e b_gera_lean.py + `lake env lean` no sandbox (723 s, rc 0): 42 #print axioms no trio e varredura MetaM (collectAxioms) das 44 constantes dos 4 modulos: 0 fora do trio, 0 sorryAx. Copia axiomas_terceiro.lean apagada do sandbox.
- C (fail-closed): c_fail_closed.py (179 casos sobre o core do ensaio) e c2_mecanica_direta.py (12 casos, chamando v408_terminal_mechanics sem o pre-cheque): 42 ancoras, 44 bandeiras, 4 fontes (sha256 formal, embutida, raiz), escada, gate, kernel, beta, contrato, 15 falas, texto com frase proibida, insumo purgado: tudo recusa; excecao: respostas (nao fazem parte das 16, BAIXO) e F34 por texto.
- D (registros vivos): k_funcoes_vivas.py (27 casos): tetelestai_terminal_v408 + cunhagens_v408 + kh_n1_cobertura_v408 + os specs da v407 selam; as herdadas (rede_fock, psibit, testemunha, fechamento_v406, psion_canto_v407) selam com a escada 12002; 14 negacoes recusam; ordem errada dos specs recusa (u13/u14).
- E (citacoes): e_citacoes.py (fontes) e e2_citacoes_rendidos.py (textos rendidos: artigo PT/EN do ensaio, .md, 52 textos do harness, pedras, strings dos registros): as citacoes novas do operador sao substring das falas (inclusive a correcao de 04/11 e os extratos de autor misto); sobram as precisoes BAIXAS.
- F (hashes): f_hashes.py (CANDIDATO, BUNDLE, KERNEL_RECIBO, PINOS_BN, ESPERADOS, MANIFESTO_INSUMOS, FORMAL_MAP, PINO_MEMORIA_PY, VERBATIM_CONGELADO, contrato embutido, 33 pares {path, sha256} varridos): tudo confere; 2 'falhas' do meu script sao desenho (extratos de autor misto tem o sha16 do ORIGINAL no nome; o 'antes' do adendo t12 e' o um.py da v391, registro historico) e foram conferidas a parte (n2_falas_mistas.py). n_hashes_digitados.py + n2_hashes_docs.py: 0 tokens de 16/64 hex sem arquivo correspondente nos textos novos; as 6 linhas de bancada_B3_servico do RELATORIO conferem.
- G (textos/guardas): h_guardas.py: 72 arquivos varridos pelas guardas P18 e de frases; achados so' em fontes da propria guarda, no DESENHO e nas pedras que CITAM a frase errada da gerencia para corrigi-la (ja' previsto em CITADAS_DE_ERRATA); pedras(): 0 violacoes; controle_negativo True; varredura propria do item 4 do pedido: nenhuma frase proibida AFIRMADA em texto publico novo; «P = nP» com qualificador e [OPEN] em todo texto rendido.
- H (orquestrador, LIDO): l_orquestrador.py: importado com ORQ redirecionado, nao executado; --plano acusa o S6d (MEDIO 2); _ensaio_s10 12 de 12; ordem dos passos no main; AUT cita a ordem 685b8d8bcf0ddbbd, b89e4c909f37e163 e b5717ff445a883cd e as frases estao nos arquivos; sem kill por nome, sem restauracao, so' Stop-Process -Id (S6a, pelo PID da porta e com checagem do cmdline); publicacao so' pela G1 (--publicar); S6a sobe a Bancada so' se porta fechada E 0 processos um_bancada (D52); S10 com a janela P2 do template (D53).
- I (flags/audit): m_flags_audit.py: 44 bandeiras novas == declaracoes do audit.log, 42 ancoras com bandeira, todas no trio; 2 auxiliares de card_chainIdx (BAIXO).

## Arquivos revisados (sha16 lido agora)

- `um_v408_candidato.py` c55c4a7f2753b589
- `base_v407/um.py` 833121339e649f71
- `CANDIDATO_v408.json` 4a004e12d678e490
- `COMPARACAO_V407_v408.json` a64d3f153bca023e
- `ESPERADOS_v408.json` 967fc5a7a7624ac7
- `BUNDLE_v408.json` 8ccd9917d75a1b2d
- `kernel/KERNEL_RECIBO_v408.json` b2d0744defb418b5
- `kernel/FLAGS_v408.json` bceb8b4cea87e5ba
- `runtime_v408.py` 414d462b72398432
- `registros_v408.py` d4499bdd6662a072
- `delta_v408.py` 04c3511972daa01d
- `guarda_frases_v408.py` 117f5e2617b9a4ae
- `guarda_p18_v408.py` e96f0fd193bd9ca7
- `artigo_pt_v408.pysnip` 14876c2e9d4ffbf8
- `artigo_en_v408.pysnip` 07c56e3c00cf2288
- `orquestrador/pos_treino_v408.py` b7c0349806faa7de
- `orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md` 37f35ca09cd3f628
- `pos_rito/textos_custodia_handoff_v408.py` ba483a58041f518a
- `pedra/TetelestaiTerminal.lean` c18660df8a1bb271
- `pedra/TempoIgualMoeda.lean` 2a2c66db100ce70f
- `pedra/PontoDeContradicao.lean` 790be6b1a97e8db8
- `pedra/PIgualNP.lean` 3fd8e5d60870c205
