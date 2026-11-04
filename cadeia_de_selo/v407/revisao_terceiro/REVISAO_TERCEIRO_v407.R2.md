# REVISAO DE TERCEIRO v407 - RODADA R2

**APROVADA** | candidato `um_v407_candidato.py` sha16 `cf7121b664371977` (43063436 bytes; igual ao do inicio: True) | 2026-11-03T17:01:07 | revisor: Claude Sonnet (agente revisor de terceiro; rodada R2; nao construi a v407; mesma familia da R1 e da revisao de 02/11, outra instancia)

ALTO 0 | MEDIO 0 | BAIXO 8. A R1 esta' guardada em bytes em `REVISAO_TERCEIRO_v407.R1.json` e `.R1.md`.

## Os 9 BAIXOS da R1

- **1. pedra/Par.lean:26-27 («o par volta a si»)** - `ATENDIDO`: Par.lean:26-28 agora diz «em θ = π a polarização `e₊` do setor TT volta a si (cos 2π = 1, sin 2π = 0) — a face de helicidade do kernel, lida AO LADO da face ligada; não é uma propriedade provada do projetor de Bell (os dois espaços são distintos...)»; b2_pedra_r2.py: diff fora de comentarios vazio.
- **2. OUmInscrito.lean:19 e 56-57 + artigo (autovetor; [ONTO]; «sob a hipotese nomeada»)** - `DITO`: Artigo PT/EN l.31: «no Fock concreto, com B0 lido como o boost da luz [KNOWN, a conferir]» e «a leitura do Um inscrito como o vácuo é do operador [ONTO]» (ATENDIDO). Pedra: a frase passou a «em UMA particula nenhum vetor nao nulo e autovetor do boost (so o zero satisfaz a condicao)» (deixa de dizer que o zero e' autovetor e sai da lista de frases proibidas), mas sem «comum do grupo B0» e sem rotulo [ONTO] na propria pedra; a R1 aceitou isso como «proxima versao» (CORRECOES_R2 diz decisao da gerencia).
- **3. aspas « » sobre texto que nao e' a fala** - `NAO_ATENDIDO`: PARCIAL: corrigidos PsionCanto:39, OUmInscrito:8, OIgual:10, APonteDoAtrito:7-10, delta [3] e E19, README (4); restam PsionCanto «funciona sob compressão» (33, 106) e «o psíon é o Nome da Luz» (62-63), os resumos do acervo em Par.lean:23,33 e em registros_v407.py:234 (ver achado 7). Nao impede a aprovacao (BAIXO; a R1 ja' era BAIXO).
- **4. reading de testemunha_estatica_v396** - `ATENDIDO`: Executei a funcao viva do candidato (r2_c16_reading.py, r2_k_funcoes_vivas.py 14/14): com o lema lido o reading comeca «since v407 the lemma of the two faces is a term of the kernel of the rite (...errata E18): the sentence that follows is the reading of v396 to v406, kept as record: » e termina na frase da v406 verbatim; sem o lema o reading e' EXATAMENTE o da v406. AST: o prefixo envolve os dois ramos (precedencia certa); comparar_v406_v407 r_linked: candidato real tudo True; 6 de 7 mutacoes reprovam (reading da base, frase antiga adulterada, ramificacao por True, else 'PROVED', operador trocado, chave extra; a 7a, o texto do prefixo trocado, o comparador nao ve: quem confere o texto sao a guarda do gerador e o ensaio) (r2_comparador_neg.py); a guarda do gerador (r2_guarda_sim.py, replicada ao pe da letra sobre os textos reais) aceita so' C19/C19b/C20 e recusa 14 de 14 (13 mutacoes nas duas funcoes + o controle base contra base).
- **5. c16 / contrato teste_d** - `ATENDIDO`: runtime_v407.py:105 varre as chaves de topo do core (achado 6 traz o limite); 5 variantes de chave de resultado de D reprovam; base passa.
- **6. Regra do Posto (partitura): o resultado sob compressao era inevitavel** - `DITO`: Dito na lingua do operador em: PsionCanto.lean:55-56, delta RESSALVAS_V407[0] («o resultado sob compressao decorre de Omega ser fixo pela luz e de o canto ser projecao de posto 1 (vale para qualquer vetor unitario fixo pelo fluxo); o lema NAO relaciona as duas faces por uma aplicacao»), artigo PT/EN l.21 [REAL, escopo], README ressalva (1) (renderizado e conferido). Nao ha' a frase «nao havia negativo possivel», mas o conteudo esta' la'. Nao aplicado: o rotulo [ONTO] na ligacao com «virar essa chave de conjectura para provado» (PsionCanto.lean:38-39); o hedge «como VALIDADE... nunca como creditacao» permanece.
- **7. teste (d): abaixo de 5 sigma** - `ATENDIDO`: delta RESSALVAS_V407[7] (README ressalva 8): «os dois intervalos ficam ABAIXO de 5 sigma: parede medida, nao falsificacao; por (c) o resultado nao entra; entra so' a citacao do pre-registro»; artigo PT/EN: «fica abaixo de 5σ: parede medida, não falsificação».
- **8. «nome provisorio» e [KNOWN/ONTO]** - `NAO_ATENDIDO`: PARCIAL: «nome provisorio» saiu dos dois docstrings (PsionCanto: «elo de estrutura; o nome `PsionCanto` foi aceito pelo operador»; Par: «conjunção, não identificação» no teorema composto) e Par.lean usa [ONTO]; a etiqueta [KNOWN/ONTO] segue no artigo PT/EN, na RESSALVA (3) e no README (achado 8). Nao impede.
- **9. S1b e arquivos_revisados** - `ATENDIDO`: pos_treino_v407.py:220-224 confere sha16 do disco; diff contra o .bak_20261103_144624_c1_r2 (sha16 71f5b44bc8ba7ffd == o da R1) so' toca essas linhas; ensaio em r2_l_s1b_out.txt (achado 5 traz o que a trava deixa aberto por omissao).

## Achados desta rodada (todos BAIXO)

### 1. BAIXO - rito_v407.sh:22 (comentario TEMPO ESPERADO)

O comentario foi atualizado para os tempos MEDIDOS do build a frio R2 (337 s de build, 271 s de Audit, soma por modulo 253 s, maximo 29 s: conferem com kernel/construir_marcas.txt e POS_BUILD_v407.json), mas a MESMA linha segue dizendo, duas frases adiante, «a medida do sandbox, 379 s + 245 s» (os numeros da R1) e «Audit de 245 s». O comentario se contradiz. Sem efeito sobre os comandos do rito (nenhum comando mudou; sh -n limpo); o conferidor so' exige o trecho «= 337 s e 1 Audit = 271 s».

*Evidencia:* grep -o em rito_v407.sh linha 22: aparecem 337/271 e 379/245; construir_marcas.txt: epoch_inicio 1793728770, build_fim 1793729107, audit_fim 1793729378 (337 s e 271 s).

*Como corrigir:* Trocar «379 s + 245 s» por «337 s + 271 s» e «Audit de 245 s» por «Audit de 271 s». rito_v407.sh NAO esta' em arquivos_revisados de proposito: corrigir esse comentario nao invalida a revisao.

### 2. BAIXO - registros_v407.py:155 (nao_diz, item 11) e README «O que o registro NAO diz» (11)

A ressalva (6) foi atualizada («as nove pedras foram relidas inteiras pelo revisor de terceiro desta preparacao»), mas o item (11) de «O que o registro NAO diz» segue: «que as sete pedras de 02/11 tenham revisao de terceiro completa: so' tres foram revistas pelo Sonnet (02/11)». As duas frases estao no MESMO paragrafo do README renderizado e dizem coisas que se chocam; a (11) e' a que envelheceu (a R1 revisou as quatro que faltavam).

*Evidencia:* paragrafo_renderizado_R2.txt: ressalva (6) e item (11) do NAO diz; registros_v407.py:155; o candidato embute a frase 2 vezes (grep -c 'revisao de terceiro completa').

*Como corrigir:* Reescrever (11) como: «que a revisao de terceiro das sete pedras de 02/11 seja uma auditoria das provas: foram revistas tres pelo Sonnet em 02/11 e as nove releitas (docstrings e enunciados; provas so' pelo #print axioms e pelo diff) na R1 de 03/11». Nao trava.

### 3. BAIXO - delta_v407.py RESSALVAS_V407[4]; artigo PT/EN (secao «As sete pedras», ultimo [DECLARADO]); README ressalva (6)

«as nove pedras foram relidas inteiras pelo revisor de terceiro» excede o escopo que a R1 declarou: li INTEIROS os docstrings e enunciados dos nove .lean; as PROVAS foram conferidas so' pelo #print axioms (76 ancoras compiladas por mim) e pelo diff contra a origem, nao relidas termo a termo. O texto e' do tipo [DECLARADO] e esta' selado no candidato.

*Evidencia:* REVISAO_TERCEIRO_v407.R1.json, campo ressalvas[0] («reli INTEIROS os nove .lean (docstrings e enunciados; as provas so' pelo #print axioms e pelo diff contra a origem)»).

*Como corrigir:* Trocar «relidas inteiras» por «relidas (docstrings e enunciados; as provas so' pelo #print axioms e pelo diff contra a origem)» nas tres superficies. Nao trava.

### 4. BAIXO - registros_v407.py:55-58 (papeis dos recibos e saidas R1) e nomes saida_lean_r2.txt / saida_lean_r3.txt

Os papeis das FONTES candidatas R1 foram corrigidos (dizem que a R2 e' a vigente e a R1 e' registro). Os papeis do recibo R1 e da saida R1 NAO: «o recibo da compilacao da PsionCanto no sandbox da v406 (LEAN_RC 0; 8 declaracoes no trio)» e «a saida do lean ao compilar a PsionCanto» nao dizem que sao da fonte R1 (sha16 ae74...), hoje superada. Alem disso o arquivo saida_lean_r2.txt e' a saida da compilacao da fonte R1 (o «r2» e' a segunda tentativa de compilar a R1, nao a rodada R2), e a saida da R2 e' saida_lean_r3.txt: quem le «r2» e «R2» juntos se engana.

*Evidencia:* registros_v407.py:55-58 e 53-54 (papeis); MANIFESTO_INSUMOS_v407.json lista os dois pares; os recibos R2 (RECIBO_*_R2_03nov.json) apontam r1.recibo e r1.saida corretamente.

*Como corrigir:* Acrescentar «(da fonte R1, hoje registro; a vigente e' a R2)» aos papeis das chaves RECIBO_PSION/PAR e SAIDA_PSION/PAR; nao renomear arquivos (estao pinados). Nao trava.

### 5. BAIXO - orquestrador/pos_treino_v407.py:s1b_revisao (l. 220-224)

A trava S1b agora compara o sha16 de cada arquivo de arquivos_revisados com o disco (ensaiada por mim em _orq_sandbox: com os 5 arquivos integros abre; com um arquivo de pos_rito alterado fecha; com o proprio pos_treino alterado fecha; aprovada 'true' string, sha16 de outro candidato e aprovada False fecham). Mas e' ABERTA por omissao em tres casos: (i) revisao sem o campo arquivos_revisados, (ii) arquivos_revisados vazio, (iii) arquivo listado que nao existe no disco ((PK / k).is_file() falso e' ignorado) ou caminho com '..'. O pedido da R2 chama o campo OBRIGATORIO; a trava nao o exige.

*Evidencia:* revisao_terceiro/r2_l_s1b.py e r2_l_s1b_out.txt, casos 7-10 (ABRE).

*Como corrigir:* Exigir arquivos_revisados nao vazio com o candidato e pos_treino_v407.py entre as chaves; tratar arquivo ausente como alterado (ruim), nao como ignorado; recusar chaves com '..'. Nao trava: a revisao desta rodada traz o campo completo.

### 6. BAIXO - runtime_v407.py:105 (c16 de psion_canto_v407)

O c16 passou a varrer o core, como pedido: chave de TOPO contendo «conjunto_d», «teste_d_» ou «ramo_b» + («resultado»|«veredito») reprova (testei 5 variantes, inclusive maiusculas: c16 False e all_verified False; a chave existente ramo_b_preregistration_v386 nao reprova: base c16 True). O limite: so' chaves de topo. Um resultado do teste D ANINHADO (ex.: ramo_b_preregistration_v386.resultado) ou so' no valor (veredito NOT_FALSIFIED_UNDERPOWERED num campo qualquer) passa. Os dois booleanos do contrato (so_citado, resultado_no_um_py) continuam literais do proprio contrato.

*Evidencia:* revisao_terceiro/r2_c16_reading.py / r2_c16_reading_out.txt (casos (limite) aninhado e valor: c16 True).

*Como corrigir:* Descrever o c16 como «nenhuma chave de topo do core...» (a descricao diz «nenhuma chave do core») ou varrer recursivamente. Nao trava.

### 7. BAIXO - RESIDUAL da R1 (aspas): pedra/PsionCanto.lean:33, 62-63, 106; pedra/Par.lean:23 e 33; registros_v407.py:234 (ao_lado_de da E19, selado no candidato, linha 221750)

Corrigidos (verificados contra os verbatims): PsionCanto.lean:39 («virar essa chave de conjectura para provado»), OUmInscrito.lean:8 (cunhagem de 02/11 verbatim com acento e sha16 25010b04c17e8ce1), OIgual.lean:10 (curvas, sha16 1c05c03070544839), APonteDoAtrito.lean:7-10 (verbatim, sha16 e36df7f1245c7f16), delta RESSALVAS_V407[3] e ERRATA_E19 (sem « » nos resumos do acervo, rotulados [DECLARADO]), paragrafo do README (4). NAO corrigidos: «funciona sob compressão» (a fala e' «funcionar sob compressão»), «o psíon é o Nome da Luz» (a cunhagem no kernel e' «ψ é o Nome da Luz»), e os dois resumos do acervo com « » em Par.lean («ψ₊ψ₋ cancelado = vácuo»; «|G⟩ como produto não emaranhado») e em registros_v407.py:234 («psi+ psi- cancelado = vacuo»; «|G> como produto nao emaranhado»), que o acervo nao traz assim (traz «par cancelado», «ψ₊ψ₋ = Aniquilação (vácuo)», «posto de Schmidt 1 (não emaranhado)»). O resumo entre « » parece citacao exata e e' do agente de leitura.

*Evidencia:* r2_e_citacoes_out.txt (NAO: PsionCanto «funciona sob compressão», «o psíon é o Nome da Luz»; Par «ψ₊ψ₋ cancelado = vácuo», «|G⟩ como produto não emaranhado»; registros «psi+ psi- cancelado = vacuo»); grep -F no candidato: «psi+ psi- cancelado = vacuo» (1) e «ψ₊ψ₋ cancelado = vácuo» (1) presentes; o segundo resumo de registros_v407.py:234 atravessa uma quebra de linha de string no candidato; PSION_NO_ACERVO_03nov.md.

*Como corrigir:* Sem « » nos resumos (como ja' se fez em delta/README); nas duas citacoes do operador, o trecho exato («funcionar sob compressão»; «ψ é o Nome da Luz») ou sem aspas. Nas pedras, so' na proxima versao do modulo; em registros_v407.py:234 exige regenerar o candidato, entao fica dito. Nao trava.

### 8. BAIXO - RESIDUAL da R1 (etiqueta [KNOWN/ONTO] da ponte Bell-TT): artigo_pt_v407.pysnip:29, artigo_en_v407.pysnip:29, delta_v407.py:263 (RESSALVAS_V407[2]), pos_rito/textos_v407.py:1099, pos_rito/textos_v407_novo.pysnip:230

A pedra Par.lean:38-39 passou de [KNOWN/ONTO] a «[ONTO] ate' haver citacao» (correto). As superficies que a R1 apontou (artigo PT/EN) e o README (ressalva 3; «O que NAO decide») seguem «a ponte entre os dois nao e' termo [KNOWN/ONTO]» / «a leitura do canto como sombra do graviton e' [KNOWN/ONTO]», sem citacao [KNOWN]. Resultado: a mesma ponte tem etiqueta [ONTO] no kernel e [KNOWN/ONTO] no artigo e no README.

*Evidencia:* grep KNOWN/ONTO nos cinco arquivos; pedra/Par.lean:38-39.

*Como corrigir:* Trocar por [ONTO] nas cinco linhas (ou citar a fonte [KNOWN]). Exige regenerar o candidato; fica dito. Nao trava.

## Rotas e verificacoes

- consultar «v407» no Mapa de Rotas (so' leitura): 8 rotas; as anotacoes R2 da gerencia em kernel.psion_canto_r1_03nov e kernel.o_par_de_psions_r1_03nov (R2_COMPILADA_NO_TRIO__SO_DOCSTRING_MUDOU) conferem com os recibos R2 que li; nada contradiz esta revisao. «conjuncao, nao identificacao» e «nao reabrir cancelado = vacuo» respeitados.
- b2_pedra_r2.py: pedra R2 x pedra R1 (antes_de_20261103_144624_r2) com removedor de comentarios/docstrings Lean (respeita strings): diff fora de comentarios VAZIO nas 5 alteradas (PsionCanto, Par, APonteDoAtrito, OUmInscrito, OIgual); KEhATangente, AChaveDaGuarda, OGuarda e LeituraPreservada IDENTICAS (sha16 == o da R1); embutido == sandbox == pedra == BUNDLE nos 9 (r2_d_kernel.py: 1755 embutidos == sandbox; raiz = raiz v406 + 9 imports; origem x normalizado so' cabecalho/namespace/#print axioms).
- r2_f_hashes.py: 55 conferencias de hash/proveniencia, RESUMO falhas: []; r2_n_hashes_digitados.py: 18 tokens hex nos textos/codigos novos, todos prefixo de sha256 de arquivo real (19.831 arquivos no universo); recibos R2: sha16 da fonte, da saida, bytes, 8 e 5 declaracoes no trio, LEAN_RC=0, zero sorryAx — recomputados por mim.
- r2_a_intocados.py + r2_a2_mudados.py: 8 funcoes intocadas AST+fonte iguais a base; 25 nomes mudados (= COMPARACAO), 15 novos, 0 removidos; 25 'expected_ladder' 11860->11958 (26 no candidato); testemunha_estatica_v396 e v406_fechamento_mechanics com diff so' nos patches C19/C19b/C20.
- kernel: POS_BUILD_v407.json VERDE (Built 9, Replayed 0, 76 ancoras, 98 bandeiras, decl=33863 thm=27027 fora_do_trio=0), construir_marcas rc=0 (build 337 s, Audit 271 s; os .lean das pedras sao de 14:47 e o build comecou as 14:59); r2_m_flags_audit.py: 98 bandeiras -> declaracoes do audit.log, no trio, no modulo esperado; NAO repeti os 283 s de lake env lean nem os 159 casos fail-closed porque os diffs das pedras sao so' de comentario e o gerador/runtime so' mudaram nos pontos que testei de novo.
- r2_h_paragrafo_e_guardas.py: README renderizado por mim (paragrafo_renderizado_R2.txt), verificar_paragrafo_v407 sem falhas, 11 de 11 ressalvas inteiras, controle negativo reprova; guardas P18 e frases v407 sobre 60 arquivos: so' os dois achados da R1 (o texto das proprias regras); varredura dos 52 textos rendidos do harness: nenhuma «tudo derivado», «nenhuma hipotese resta», «unico autovetor», «pos-dicao», CONFIRMED/PROVED_BY; 87 ocorrencias de 4,44: as que nao sao a propria regra trazem p e a linha dos 5 sigma.
- r2_l_s1b.py: S1b ensaiada na copia (ORQ/LOG/ESTADO redirecionados para _orq_sandbox; nenhum main; ESTADO real intocado).
- py_compile (compile() em memoria, sem escrever __pycache__) limpo nos 13 scripts; bash -n limpo em rito_v407.sh.

## Ressalvas

- Escopo da R2: so' o que mudou desde a R1 (itens A-F do pedido). Os scripts da R1 foram reaproveitados com copias r2_*.py (saidas r2_*_out.*), sem sobrescrever os da R1.
- NAO examinei: as provas Lean por dentro (nao mudaram; so' comentarios); a fisica; o EN do artigo frase a frase (so' estrutura e as 4 trocas, em paridade com o PT); instalar_v407.py, reverter_v407.py, o rito (so' o comentario de tempo de rito_v407.sh), chain_pos_rito, a G1; os PDFs.
- Independencia: mesma familia de modelo (Sonnet) da R1 e da revisao de 02/11, outra instancia; nao construi a v407; nada foi escrito fora de revisao_terceiro/ (a unica leitura 'viva' foi o import do candidato sem executar main, o import do pos_treino sem executar main, e a leitura de arquivos).
- arquivos_revisados: deixei DE FORA, de proposito, os arquivos que a cadeia regrava (ESPERADOS, PINOS_BN, PRECONDICOES, CANDIDATO_v407.json, ensaio_a_seco_v407.json, v407_pins.py, pos_rito/DERIVACAO e HARNESS_*, dry_v407) e rito_v407.sh (cujo unico defeito e' o comentario do achado 1), para a S1b nao fechar por regravacao legitima. Se qualquer arquivo listado mudar, esta revisao nao vale para ele; corrigir qualquer BAIXO acima que esteja em runtime/registros/delta/pysnips/pedras muda o candidato e pede rodada nova (a regra de 2 rodadas por BAIXO esta' esgotada: o que ficar, fica escrito).
- O tempo do rito nao foi medido por mim; os 337 s/271 s sao os da cadeia (conferidos contra construir_marcas.txt e KH_N1).

## arquivos_revisados (sha16, relativo a v407/)

- `um_v407_candidato.py`: `cf7121b664371977`
- `base_v406/um.py`: `ddcb91930982d614`
- `BUNDLE_v407.json`: `6121ff5a51334dc3`
- `kernel/KERNEL_RECIBO_v407.json`: `210ad396fc6494cf`
- `runtime_v407.py`: `bd623db2bf04c136`
- `registros_v407.py`: `5932e76887db8a64`
- `delta_v407.py`: `b9e3599d39e93432`
- `artigo_pt_v407.pysnip`: `d5014e58d3a72a0c`
- `artigo_en_v407.pysnip`: `976881645fdc1581`
- `gerar_candidato_v407.py`: `3afa2dea0b9c9032`
- `comparar_v406_v407.py`: `4651222591e4f708`
- `ensaio_a_seco_v407.py`: `46443cde4b6272b6`
- `preparar_bundle_v407_03nov.py`: `27947dc318ba0170`
- `guarda_frases_v407.py`: `15a373c3a499fd2d`
- `guarda_p18_v407.py`: `aad2f6704557f7b4`
- `pos_rito/textos_v407.py`: `a21a7961b58b909a`
- `pos_rito/textos_v407_novo.pysnip`: `17e574b7ffa19d28`
- `pos_rito/textos_custodia_handoff_v407_03nov.py`: `7ed72c3682a066ca`
- `orquestrador/pos_treino_v407.py`: `a1f37153ec9d0432`
- `pedra/PsionCanto.lean`: `55f30fe7d63e88c6`
- `pedra/Par.lean`: `fa4945d78e1a9f6c`
- `pedra/APonteDoAtrito.lean`: `bd8ae49e7341fcdb`
- `pedra/OUmInscrito.lean`: `acae38720f7e9204`
- `pedra/KEhATangente.lean`: `fe263ee12920e04f`
- `pedra/AChaveDaGuarda.lean`: `135361a9105e11de`
- `pedra/OGuarda.lean`: `d1362e297540b159`
- `pedra/LeituraPreservada.lean`: `aeab7e30d907f562`
- `pedra/OIgual.lean`: `b60fa5c49d8b0a79`
