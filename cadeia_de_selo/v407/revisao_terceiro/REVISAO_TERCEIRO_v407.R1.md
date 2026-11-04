# Revisao de terceiro da v407 (R1)

Revisor independente (agente Claude Sonnet; nao construi a v407). Candidato `a5df4c573328465c`, lido do arquivo ao fechar, 2026-11-03T14:15:04. **Veredito: APROVADA -- 0 ALTO, 0 MEDIO, 9 BAIXO.** O candidato nao mudou durante a revisao (sha16 igual ao do inicio, mtime 13:28:02).

## 1. O que a R1 conferiu (resultado)

- **Candidato x base v406** (`a_intocados.py`, `a2_mudados.py`): 8 funcoes intocadas (gate, neutrino, ramo B, livro, GA) com AST e fonte identicas; 25 nomes mudados, 15 novos, 0 removidos (igual a COMPARACAO); `testemunha_estatica_v396` e `v406_fechamento_mechanics` mudaram so' no que o pedido diz, com texto antigo guardado (`reading_v396`, `elo_v407.reading_v396_v406`, c8 com «ate' a v406») e errata E18/E20 ao lado; `_V406_SPECS`: 17 diferencas, todas em u7 e h2/h3/h6/h8 mais as duas erratas; os 25 `'expected_ladder': 11860` viraram 11958 e so' eles.
- **Kernel** (`d_kernel.py`, `axiomas_terceiro.lean`): 9 modulos embutidos == sandbox == `pedra/` == BUNDLE (sha256); origem x normalizado diferem so' em cabecalho/namespace/`#print axioms`; raiz = raiz v406 + 9 imports; Audit identico; 1.746 herdados intactos. **Compilei eu** (`lake env lean`, um processo, 283 s): 76 ancoras + exemplo proprio no trio, 0 `sorryAx` (incluindo `the_psion_is_the_corner_on_both_faces`, `o_par_de_psions_e_o_graviton` e o lema instanciado no habitante).
- **Runtime/registros** (`c_fail_closed.py`: 159 casos, 0 falha; `k_funcoes_vivas.py`): as 16 checagens leem o core/kernel (c16 em parte declaratoria: BAIXO 5); `_v407_elo_lido` e `psion_canto_v407` sao fail-closed em cada elo; as 4 respostas do operador resolvem para teoremas que JA estavam no axiom_report da v406 (nao digitados); as 98 bandeiras apontam para declaracoes reais no trio e no modulo esperado.
- **Textos**: guardas P18 e v407 sobre 60 arquivos, sem frase proibida; todas as citacoes do operador nos textos rendidos (302) e no artigo PT (10/10) sao substring exata; ressalvas: as 11 inteiras no paragrafo do README, que renderizei e verifiquei (controle negativo reprova a ressalva cortada); a regra do 4,44 respeitada (sempre com p e a linha dos 5 sigma); erratas E18-E20 em nome proprio, ao lado.
- **Hashes** (`f_hashes.py`, `n_hashes_digitados.py`): 55 conferencias, 0 falha (CANDIDATO, ESPERADOS, PINOS_BN, MANIFESTO_INSUMOS, BUNDLE, FORMAL_MAP, KERNEL_RECIBO, PINO_MEMORIA_PY); 12 tokens hex digitados nos textos novos, todos prefixo de sha256 de arquivo real.
- **Orquestrador** (`l_orquestrador.py`): `--plano` e `--ensaio` a seco (ORQ redirecionado); S10 positivo + 8 negativos; ordem dos passos; AUT correta; sem matar processo por nome; publica so' pela G1; S1b fail-closed.

## 2. Leitura honesta (item 8 do pedido)

A v407 le do kernel o lema que mostra, nas duas faces, o mesmo molde («psion = vetor unitario cujo canto e' o projetor sobre ele; escalariza; pesa 1; a leitura de Jones devolve o canto») e compoe termos que o kernel ja tinha para o par ligado (CCI = 1/2, idempotente, traco 1, fase dobrada, canto 4x4). **Nao** identifica Omega com Phi+, **nao** prova o par na face de Fock, **nao** prova a ponte Bell-TT, **nao** move o gate (`qg_closure`, `neutrino_mass`, `witness_rigidity` do core do ensaio sao identicos ao da v406), nao acrescenta dado, nao deriva nada da natureza, nao roda teste novo. Nenhum texto sugere o contrario: nenhum ALTO. Duas leituras a manter: (i) o lema e' um molde repetido, nao uma aplicacao entre as faces, e o resultado «sob compressao» decorre de Omega ser fixo pela luz — o «teste da condicao» nao tinha negativo possivel (BAIXO 6); (ii) a chave `linked_to_the_corner_by_a_lemma` le True nesse sentido e so' nele.

## 3. BAIXOS (nao travam)

1. **[BAIXO] pedra/Par.lean:26-27 (cabecalho, lista "O que esta pedra PROVA").** A lista PROVA diz «em theta = pi o par volta a si (cos 2pi = 1, sin 2pi = 0)». O termo (the_pair_is_read_by_the_graviton, .2) prova que a polarizacao ePlus do setor TT (Fin 4, R) volta a si; o que volta nao e' o par de Bell (Fin 2 x Fin 2, C). O proprio cabecalho diz, em NAO afirma (l.35-38), que a leitura pelo graviton e' a face de helicidade JUSTAPOSTA a face ligada e que a conjuncao nao e' identificacao; a frase da lista de PROVA contradiz essa linha. As demais superficies (artigo PT/EN, paragrafo do README, DL.RESPOSTAS_DO_OPERADOR) dizem certo: «o retorno de fase e' a volta em theta = pi», sem «o par volta a si».
   - *Corrigir:* Na proxima versao do modulo: «e ePlus volta a si em theta = pi». Nao trava: o modulo esta' pinado por sha256 no bundle (mexer nele pede novo build do kernel); aceitar como esta' e registrar a ressalva, ou corrigir na v408.

2. **[BAIXO] pedra/OUmInscrito.lean:19 e 56-57 (APONTADO a gerencia em guarda_frases_v407.APONTADAS_A_GERENCIA); mais o artigo PT/EN (secao «As sete pedras», l.31 do pysnip).** Julgamento pedido: «em UMA particula, o unico autovetor do boost e o zero» e' VERDADEIRO no setor de 1 particula como enunciado de B0_no_eigen (nenhum f != 0 em H1 tem B0 s f = c(s) f com ‖c(s)‖ = 1 para todo s; compilei o #check: ∀ f, (∀ s, ∃ c, ‖c‖=1 ∧ B0 s f = c • f) → f = 0). Imprecisao de redacao: «autovetor do boost» e' autovetor COMUM do grupo {B0 s} (para um unico B0 0 = id todo vetor e' autovetor) e «o zero» nao e' autovetor por definicao. O aviso BASTA quanto ao escopo: o cabecalho (l.19-22) diz «em UMA particula», «valia so em uma particula» e que autovetores com fase nos setores n >= 1 NAO sao excluidos por este termo; o teorema do composto diz «vetor fixo». Restam dois reparos: (i) a revisao de 02/11 pediu rotular [ONTO] uma vez «Um inscrito = vacuo» e «o zero, o abstrato inominado» — nao aplicado (grep ONTO em OUmInscrito.lean: 0); (ii) o artigo diz «sob a hipotese nomeada» sem nomear hipotese alguma (a pedra diz «sem hipotese» no Fock concreto; a unica ressalva real e' a de B0 como boost «da luz», [KNOWN, a conferir] no docstring de B0 em TheImportedSecondQuantization.lean).
   - *Corrigir:* Artigo (barato, nao toca o kernel): trocar «sob a hipotese nomeada» por «no Fock concreto, com B0 lido como o boost da luz [KNOWN, a conferir]» e acrescentar «‘Um inscrito = vacuo’ e’ leitura do operador [ONTO]». Pedra: na proxima versao, «nenhum vetor nao nulo e’ autovetor comum do grupo B0 em H1».

3. **[BAIXO] pedra/PsionCanto.lean:39, 60-61, 104; pedra/OUmInscrito.lean:8-10; pedra/OIgual.lean:9; pedra/APonteDoAtrito.lean:7-10; delta_v407.py:260 (RESSALVAS_V407[3]) e :289 (ERRATA_E19); paragrafo do README, item (4) das ressalvas.** Aspas « » sobre texto que nao e' substring exata da fala. Operador: PsionCanto.lean:39 «vira a chave de conjectura para provado» (a fala e' «virar essa chave de conjectura para provado»); :60-61 «o psion e o Nome da Luz» (a cunhagem no kernel e' «ψ é o Nome da Luz», 16/09); :104 «funciona sob compressao» (a fala: «funcionar sob compressão»); OUmInscrito.lean:8-10 transliterado sem acentos E com pontuacao inserida (a fala de 02/11 nao tem ':' nem ';'); OIgual.lean:9 aspas curvas viram retas; APonteDoAtrito: sem acentos. Nao-operador: «psi+ psi- cancelado = vacuo» e «|G> como produto nao emaranhado» (E19, ressalva 4, README) sao resumos do levantamento do acervo [DECLARADO] — o acervo diz «Par cancelado», «ψ₊ψ₋ = Aniquilacao (vacuo)» e «posto de Schmidt 1 (nao emaranhado)». Todas as citacoes do operador nos TEXTOS (artigo PT: 10 de 10; textos rendidos: 302, 0 nao-substring de operador; paragrafo do README: verificar_paragrafo_v407 sem falhas) sao exatas.
   - *Corrigir:* Sem aspas quando for parafrase; com aspas so' o trecho exato (acento e pontuacao do original) ou dizer «transliterado, pontuacao da gerencia». Para E19/ressalva 4: tirar as « » dos dois resumos ou citar o trecho exato do acervo.

4. **[BAIXO] um_v407_candidato.py:247848 (testemunha_estatica_v396, campo fock_face.reading, ramo _hab406t_ verdadeiro); runtime/DL: errata E18.** A funcao testemunha_estatica_v396 so' mudou na chave (correto: diff de fonte so' nas linhas 40-42; texto antigo guardado em reading_v396 e em elo_v407.reading_v396_v406; errata E18/E20 ao lado). Mas o campo `reading` (nao rotulado como antigo) segue emitindo, no registro selado da v407, «...; no lemma identifies psion C with the psionCorner of this stone» ao lado de linked_to_the_corner_by_a_lemma = True e de elo_v407. A qualificacao «of this stone» (o modulo TestemunhaEstatica) mantem a frase literalmente verdadeira, e a E18 e o artigo («leia-se: era o estado da data») cobrem; ainda assim e' contradicao visivel dentro do mesmo dict (a mesma classe de lacuna que a E20 corrige nas checagens). Executei a funcao viva sobre o core do ensaio: chave True; sem o lema no kernel, chave False e elo_v407.lemma None (fail-closed).
   - *Corrigir:* Na proxima regeneracao: ramificar `reading` por _v407_elo_lido(kf_) (quando True, dizer que o lema esta' em TGLExt.PsionCanto e que a frase antiga e' a de v396-v406). Nao exige nova rodada de revisao so' por isto.

5. **[BAIXO] runtime_v407.py:105 (checagem c16 de psion_canto_v407) e _V407_PSION_CONTRACT.teste_d.** c16 («o teste (d) so' consta por CITACAO... nenhum resultado no um.py») le de fato o manifesto: fd_.get('sha256') == td_['manifesto_sha256'] contra a fonte EMBUTIDA (_V407_FONTES) — isso e' leitura. Mas `so_citado is True` e `resultado_no_um_py is None` sao literais do proprio contrato: a checagem passaria mesmo que um resultado do teste D fosse embutido em outro lugar do um.py. Autoafirmacao parcial (confirmado: mutar o contrato reprova; mutar o resto nao).
   - *Corrigir:* Descrever c16 como declaratoria (quanto aos dois booleanos), ou fazer a checagem varrer o core por qualquer chave/veredito de resultado do teste D e exigir ausencia.

6. **[BAIXO] artigo_pt_v407.pysnip (secoes «A condicao, lida sob compressao» e «O lema das duas faces»); delta_v407.py RESSALVAS_V407[0]; README paragrafo; pedra/PsionCanto.lean:37-39.** Regra do Posto (partitura): os textos dizem o que o lema NAO identifica (Omega != Phi+, face de Fock do par [OPEN], ponte Bell-TT, K(O)) e que nao e' teste com a natureza. Nao dizem, na lingua do operador, o que torna o resultado de «funcionar sob compressao» inevitavel: P·Δ^{it}·P = P e ⟨ψ,Δ^{it}ψ⟩ = 1 decorrem de o vacuo Ω ser fixo pelo fluxo modular (psion_is_fixed_by_the_light, ja' no kernel) e de qualquer projecao de posto 1 escalarizar qualquer operador; «o motor comprimido devolve o canto» vale para QUALQUER projetor (e·U·e = e); e o lema e' a conjuncao de duas instancias paralelas do mesmo molde, sem aplicacao entre as faces. Logo o «teste da condicao» nao tinha desfecho negativo possivel — o que a ressalva «elo de estrutura» sugere mas nao diz. A pedra ainda escreve que isso e' «o que, no kernel, vira a chave de conjectura para provado», leitura [ONTO] da fala dele sem rotulo (hedge presente: «como VALIDADE... nunca como creditacao»). Nao e' engano (nada e' induzido a negativo; nenhum texto afirma teste de natureza), mas e' a outra face da assimetria de leitura: um positivo que nao podia ser negativo.
   - *Corrigir:* Acrescentar uma linha a ressalva 1 e ao «nao_diz»: «o resultado sob compressao decorre de Ω ser fixo pela luz e de o canto ser projecao de posto 1; vale para qualquer vetor unitario fixo; o lema nao relaciona as duas faces por uma aplicacao, so' mostra o mesmo molde nas duas; nao havia negativo possivel». Rotular [ONTO] a ligacao com «virar essa chave de conjectura para provado».

7. **[BAIXO] delta_v407.py RESSALVAS_V407[7]; artigo PT/EN («O que fica fora, dito»); paragrafo do README, item (8).** O teste (d): a ressalva traz o poder de planejamento (3,7 a 3,9 sigma com 10 eventos; 2,1 a 3,2 sigma com a incerteza do vies) e a regra (c) do operador, mas nao junta as duas: ambos os intervalos estao ABAIXO de 5 sigma (parede medida, nao falsificacao, na PARTITURA_D_03nov.md), e pela (c) o teste so' entra com poder. Os numeros conferem com PARTITURA_D_03nov.md (linhas 6, 18, 20) e com PODER_RAMO_B_ANTES_DE_ABRIR.json, ambos pinados no MANIFESTO_PARAMETRIZACAO_03nov.json; o proprio PODER diz que o poder de planejamento e' < 5 sigma em todas as leituras e que o veredito seria NOT_FALSIFIED_UNDERPOWERED qualquer que seja o valor central. Os numeros ficam [DECLARADO] (calculo do agente da parametrizacao), como o texto diz.
   - *Corrigir:* Dizer na ressalva: «os dois intervalos ficam abaixo de 5 sigma: parede medida, nao falsificacao; por (c) o resultado nao entra; entra so' a citacao do pre-registro».

8. **[BAIXO] pedra/PsionCanto.lean:154 e pedra/Par.lean:78 (docstrings «nome provisorio»); pedra/Par.lean:38-39 e artigo PT/EN («[KNOWN/ONTO]» para a ponte Bell-TT).** Redacao: os dois docstrings chamam de «nome provisorio» o NOME DO TEOREMA (the_psion_is_the_corner_on_both_faces / o_par_de_psions_e_o_graviton) quando os nomes ratificados sao os dos modulos — leitura ambigua depois da ratificacao; e o teorema o_par_de_psions_e_o_graviton, pelo nome, le-se como identidade («o par de psions E o graviton») enquanto o corpo e' a conjuncao de a, a', a'', b (o docstring do modulo explica, o nome nao). A etiqueta [KNOWN/ONTO] para a ponte Bell-TT nao cita fonte [KNOWN].
   - *Corrigir:* Na proxima versao: tirar «nome provisorio» dos dois docstrings; manter o nome do teorema (e' ancora do contrato) mas repetir no docstring «conjuncao, nao identificacao»; trocar [KNOWN/ONTO] por [ONTO] ate' haver citacao.

9. **[BAIXO] orquestrador/pos_treino_v407.py:s1b_revisao (l.~200).** S1b exige aprovada is True e candidato_sha16 == sha16 do candidato em disco (testado: reprova aprovada False, aprovada 'true' string e sha16 de outro candidato; ficou esperando). Nao confere os hashes dos textos revisados: se um pysnip/runtime/delta mudar sem mudar o candidato (o candidato embute todos, entao em teoria muda; os textos de pos_rito NAO entram no candidato), a revisao seguiria 'valendo'. O pedido do proprio revisor diz que a revisao deixa de valer se algum mudar.
   - *Corrigir:* S1b comparar REVISAO['arquivos_revisados'] (sha16) com o disco para os arquivos de pos_rito e orquestrador, que nao entram no candidato.

## 4. Ressalvas (o que NAO examinei e outros avisos)

- R1 e' o escopo declarado: reli INTEIROS os nove .lean (docstrings e enunciados; as provas so' pelo #print axioms e pelo diff contra a origem), runtime_v407.py, registros_v407.py, delta_v407.py, o artigo PT (pysnip) e o paragrafo do README renderizado por mim; o EN so' por diff de estrutura e paridade com o PT (mesmas secoes, mesmos estatutos, mesmas contagens); NAO reli o EN frase a frase.
- NAO examinei: as provas Lean por dentro; o build do kernel (tomei o KERNEL_RECIBO + o audit.log e COMPILEI eu mesmo um arquivo com #print axioms das 76 ancoras + um exemplo proprio: 77 no trio, 0 sorryAx; o unico erro do meu arquivo foi um nome meu errado de B0_no_eigen no fim — conferi esse teorema no axiom_report do ensaio, trio); instalar_v407.py, reverter_v407.py, rito_v407.sh, chain_pos_rito_v407.sh, os scripts bateria_pre_selo/bancada_B3_servico, a G1 (custodiar.py), os gerenciadores de memoria/Atlas/handoff alem do que o harness rendeu (varri os textos rendidos por guardas e por citacoes, nao os li inteiros); a fisica; os PDFs; o rito (nao rodei); a correcao da custodia.
- Independencia: mesma familia de modelo (Sonnet) da revisao de 02/11 das tres pedras, outra instancia; a compilacao e' minha; os scripts a_*.py...n_*.py sao meus. O orquestrador foi lido e exercitado so' em --plano e --ensaio (com ORQ redirecionado para minha pasta: nada escrito fora de revisao_terceiro/).
- O candidato NAO mudou durante a revisao: sha16 a5df4c573328465c no inicio e no fim, mtime 13:28:02, 43.054.851 bytes. Em segundo plano a cadeia regravou ESPERADOS_v407.json (13:42), ensaio_a_seco_v407.json (13:42), PINOS_BN_v407.json (13:45) e PRECONDICOES_v407.json (13:45) com a mesma substancia; reexecutei f_hashes.py depois (todas as conferencias ok, ver f_hashes_out.txt).
- PRECONDICOES_v407.json esta' com ok False por UM pendente que e' da gerencia, nao desta revisao: o MEMORY.md real nao comporta a linha nova do handoff (185 linhas, 23.834 B; limite bytes+900 < 24.000); a superficie do pos-rito recusa com rc 3 e a gerencia decide o que sai do indice. Se S1 do orquestrador exigir PREPARACAO_v407_PRONTA.json com pronta == true, isto pode segurar o S1.
- A revisao de terceiro de 02/11 (tres pedras) e a minha (nove pedras, esta rodada) nao eliminam o rotulo [DECLARADO] dos textos publicos sobre o poder do teste D nem o das falas do acervo de 2025: ficam como estao ditos.
- As ressalvas (6) e (11) do README dizem que quatro das sete pedras de 02/11 «NAO tiveram revisao de terceiro ate' esta preparacao»: depois desta revisao (e se aprovada) a frase fica verdadeira so' como historia; a gerencia decide se atualiza o texto na superficie (nao e' defeito: a data esta' na frase).

## 5. Arquivos revisados (sha16 lidos ao fechar; se algum mudar, a revisao dele nao vale)

- `um_v407_candidato.py` a5df4c573328465c
- `CANDIDATO_v407.json` 2f349acf68d3d199
- `ESPERADOS_v407.json` 9014dd0a342a7e1e
- `PINOS_BN_v407.json` 3a0c5ba2d27b9309
- `BUNDLE_v407.json` eca69ad840df85b7
- `FORMAL_MAP_v407.json` a8d6968383d14083
- `MANIFESTO_INSUMOS_v407.json` a860850095012dfa
- `kernel/KERNEL_RECIBO_v407.json` da854cc2a3747a21
- `PINO_MEMORIA_PY_v407.json` 3c1ada3c6e4ede79
- `v407_pins.py` e0195fc9fb5e1c82
- `runtime_v407.py` c3517cb473cdf911
- `delta_v407.py` 08523b565ded2e28
- `registros_v407.py` 84449cac12c83e31
- `artigo_pt_v407.pysnip` 300c2c3bc5d1155f
- `artigo_en_v407.pysnip` 333a51acbd063e8e
- `guarda_frases_v407.py` 15a373c3a499fd2d
- `guarda_p18_v407.py` aad2f6704557f7b4
- `pos_rito/textos_v407.py` a21a7961b58b909a
- `pos_rito/textos_v407_novo.pysnip` 17e574b7ffa19d28
- `pos_rito/textos_custodia_handoff_v407_03nov.py` 7ed72c3682a066ca
- `orquestrador/pos_treino_v407.py` 71f5b44bc8ba7ffd
- `orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md` 2a0a1d616fcd17d6
- `base_v406/um.py` ddcb91930982d614
- `pedra/AChaveDaGuarda.lean` 135361a9105e11de
- `pedra/APonteDoAtrito.lean` f9b4872516e8fe5c
- `pedra/KEhATangente.lean` fe263ee12920e04f
- `pedra/LeituraPreservada.lean` aeab7e30d907f562
- `pedra/OGuarda.lean` d1362e297540b159
- `pedra/OIgual.lean` 91fa7896ea49b058
- `pedra/OUmInscrito.lean` 2a85f16fa6b9344d
- `pedra/Par.lean` 2835b54fe440c52f
- `pedra/PsionCanto.lean` f4a8e81c75dd1bb3

## 6. Fecho

`aprovada: true` para o candidato `a5df4c573328465c`. O orquestrador deve conferir que o sha16 do `um_v407_candidato.py` em disco e' este antes de instalar. Rodada R1 de ate' tres; os BAIXOS acima podem ser corrigidos nos textos baratos (artigo, ressalvas) sem nova rodada, ou ficar para a v408 (os que tocam as pedras pedem novo build do kernel).
