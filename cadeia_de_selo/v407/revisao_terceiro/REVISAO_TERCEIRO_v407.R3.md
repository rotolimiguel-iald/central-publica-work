# REVISAO DE TERCEIRO v407 - RODADA R3 (confinada ao diff)

**APROVADA** | candidato `um_v407_candidato.py` sha16 `62a31fb08a3b7b97` (43065104 bytes; igual ao do inicio: True) | 2026-11-03T17:33:37 | revisor: Claude Sonnet (agente revisor de terceiro; rodada R3; nao construi a v407; mesma familia da R1/R2 e da revisao de 02/11, outra instancia)

ALTO 0 | MEDIO 0 | BAIXO 5. R2 guardada em `REVISAO_TERCEIRO_v407.R2.json/.md`; R1 em `.R1.*`.

## Os BAIXOS da R2

- **R2-1. rito_v407.sh:22 (comentario de tempo)** - `ATENDIDO`: diff contra rito_v407.sh.bak_r3_tempo_*: so' a linha 22; «a medida do sandbox, 379 s + 245 s» -> «337 s + 271 s» e «Audit de 245 s» -> «Audit de 271 s» (== construir_marcas.txt: 337 s e 271 s); bash -n limpo; nenhum comando mudou.
- **R2-2. registros_v407.py:155 (NAO diz 11) x ressalva (6)** - `ATENDIDO`: Agora: «que as pedras tenham revisao de terceiro POR DENTRO das provas: em 02/11 o Sonnet reviu tres das sete (docstrings e enunciados); em 03/11 o revisor desta preparacao conferiu as nove por #print axioms, diff contra as origens e docstrings, nao as provas linha a linha». Coerente com a ressalva (6) no paragrafo renderizado por mim (paragrafo_renderizado_R3.txt, 11 de 11 ressalvas, verificar_paragrafo_v407 sem falhas). O escopo da revisao de 02/11 («docstrings e enunciados», sem rodar lean) confere com o cabecalho dela.
- **R2-3. «relidas inteiras» (delta RESSALVAS[4]; artigo PT/EN; README (6))** - `ATENDIDO`: delta, artigo PT e artigo EN: «conferidas ... (#print axioms no trio, diff contra as origens e docstrings; nao as provas linha a linha; 0 alto e 0 medio em todas as rodadas; ...)». Descreve com exatidao o meu escopo da R1/R2. Ressalva: «0 alto e 0 medio em todas as rodadas» e' verdadeira para R1 (0/0/9), R2 (0/0/8) e, se esta R3 for aprovada como esta' gravada, R3 (0/0/5); o texto sela uma afirmacao sobre esta rodada, entao so' vale com esta aprovacao.
- **R2-4. papeis dos recibos/saidas R1 (registros_v407.py:55-58)** - `ATENDIDO`: As quatro FONTES ganham «[registro R1: a fonte vigente e' a R2, recibo R2 abaixo]» (recibos) e «[registro R1: a saida vigente e' a R2, saida_lean_r3.txt / saida_lean_par_r2.txt]» (saidas): o nome saida_lean_r2.txt deixa de enganar. O candidato traz 4 ocorrencias de «registro R1».
- **R2-5. S1b fail-open por omissao (campo ausente/vazio, arquivo ausente, '..')** - `NAO_ATENDIDO`: pos_treino_v407.py inalterado desde a R2 (sha16 == o da R2); r3_l_s1b_out.txt repete os casos 7-10 (ABRE). Nao tratado pelo pedido da R3; fica escrito (BAIXO, nao impede).
- **R2-6. c16 so' varre chaves de topo** - `NAO_ATENDIDO`: runtime_v407.py inalterado desde a R2. Fica escrito (BAIXO, nao impede).
- **R2-7. aspas residuais nas pedras e nos resumos do acervo** - `DITO`: Pedras nao tocadas (sha16 das 9 == R2); o pedido da R3 diz que ficam para o caderno da v408. Segue em registros_v407.py:234 (ao_lado_de da E19, «psi+ psi- cancelado = vacuo» e «|G> como produto nao emaranhado»): registros_v407.py so' mudou nas linhas 55-58 e 155.
- **R2-8. [KNOWN/ONTO] da ponte Bell-TT** - `NAO_ATENDIDO`: PARCIAL: [ONTO] nas superficies pedidas (delta ressalva 3: «[ONTO] (sem citacao [KNOWN] ate' haver fonte)»; artigo PT/EN l.29 «[ONTO]»; textos_v407.py:1099 e textos_v407_novo.pysnip:230; README renderizado). Escapou o print do rito em gerar_candidato_v407.py:229 (achado 1).

## Achados que restam (todos BAIXO)

### 1. BAIXO - gerar_candidato_v407.py:229 (print do cabecalho «O PSION, O CANTO E O PAR [v407 ...]»; no candidato, linha 278879); stdout canonico do rito

A troca [KNOWN/ONTO] -> [ONTO] da ponte Bell-TT foi feita em delta (ressalva 3), artigo PT/EN, pos_rito/textos_v407.py e textos_v407_novo.pysnip, mas escapou UMA ocorrencia: o print do rito que abre o bloco do psion ainda diz «[OPEN] o par na face de Fock; [KNOWN/ONTO] a ponte Bell-TT». Esse texto vai para rodada_v407_stdout.txt (stdout do rito e' canonico) e fica selado com a etiqueta [KNOWN] sem citacao, o defeito que a R1/R2 apontaram. grep «KNOWN/ONTO» no candidato: 1 ocorrencia; nos arquivos-fonte da v407 (fora dos .bak e dos scripts r2_/correcoes): so' gerar_candidato_v407.py:229; nos 52 textos rendidos do harness: nenhuma.

*Evidencia:* grep -n KNOWN/ONTO um_v407_candidato.py -> 278879; grep -l em *.py *.pysnip pos_rito orquestrador pedra -> gerar_candidato_v407.py; harness textos: zero.

*Como corrigir:* Trocar por [ONTO] na linha 229 do gerador (muda o candidato: pede rodada nova) ou deixar dito. Nao trava: e' etiqueta de um print, a mesma ponte aparece como [ONTO] em todas as outras superficies.

### 2. BAIXO - pos_rito/textos_v407.py (bytes): fins de linha

O diff contra o .bak_r3_baixos e' exatamente o declarado ao nivel de TEXTO (1 linha: [KNOWN/ONTO] -> [ONTO]). Ao nivel de BYTES ha' uma mudanca nao declarada: o arquivo tinha 1088 CRLF e 46 LF isolados (as 10 primeiras linhas de comentario e 36 linhas em branco) e agora tem 1134 CRLF e 0 LF isolados (o patch normalizou os fins de linha). Sem efeito semantico (o import normaliza \n; ignorando o fim de linha so' 1 linha difere), mas e' a mudanca que o pedido nao listou.

*Evidencia:* contagem de b'\r\n' e b'\n' nos dois arquivos (113521 -> 113561 bytes); difflib sobre o texto normalizado: 2 linhas (-/+) = a linha 1099.

*Como corrigir:* Dizer no caderno (ja' esta' aqui). Nao trava.

### 3. BAIXO - [CARREGADO da R2, nao tocado nesta rodada] orquestrador/pos_treino_v407.py:s1b_revisao (l. 220-224)

A trava S1b agora compara o sha16 de cada arquivo de arquivos_revisados com o disco (ensaiada por mim em _orq_sandbox: com os 5 arquivos integros abre; com um arquivo de pos_rito alterado fecha; com o proprio pos_treino alterado fecha; aprovada 'true' string, sha16 de outro candidato e aprovada False fecham). Mas e' ABERTA por omissao em tres casos: (i) revisao sem o campo arquivos_revisados, (ii) arquivos_revisados vazio, (iii) arquivo listado que nao existe no disco ((PK / k).is_file() falso e' ignorado) ou caminho com '..'. O pedido da R2 chama o campo OBRIGATORIO; a trava nao o exige.

*Evidencia:* revisao_terceiro/r2_l_s1b.py e r2_l_s1b_out.txt, casos 7-10 (ABRE).

*Como corrigir:* Exigir arquivos_revisados nao vazio com o candidato e pos_treino_v407.py entre as chaves; tratar arquivo ausente como alterado (ruim), nao como ignorado; recusar chaves com '..'. Nao trava: a revisao desta rodada traz o campo completo.

### 4. BAIXO - [CARREGADO da R2, nao tocado nesta rodada] runtime_v407.py:105 (c16 de psion_canto_v407)

O c16 passou a varrer o core, como pedido: chave de TOPO contendo «conjunto_d», «teste_d_» ou «ramo_b» + («resultado»|«veredito») reprova (testei 5 variantes, inclusive maiusculas: c16 False e all_verified False; a chave existente ramo_b_preregistration_v386 nao reprova: base c16 True). O limite: so' chaves de topo. Um resultado do teste D ANINHADO (ex.: ramo_b_preregistration_v386.resultado) ou so' no valor (veredito NOT_FALSIFIED_UNDERPOWERED num campo qualquer) passa. Os dois booleanos do contrato (so_citado, resultado_no_um_py) continuam literais do proprio contrato.

*Evidencia:* revisao_terceiro/r2_c16_reading.py / r2_c16_reading_out.txt (casos (limite) aninhado e valor: c16 True).

*Como corrigir:* Descrever o c16 como «nenhuma chave de topo do core...» (a descricao diz «nenhuma chave do core») ou varrer recursivamente. Nao trava.

### 5. BAIXO - [CARREGADO da R2, nao tocado nesta rodada] RESIDUAL da R1 (aspas): pedra/PsionCanto.lean:33, 62-63, 106; pedra/Par.lean:23 e 33; registros_v407.py:234 (ao_lado_de da E19, selado no candidato, linha 221750)

Corrigidos (verificados contra os verbatims): PsionCanto.lean:39 («virar essa chave de conjectura para provado»), OUmInscrito.lean:8 (cunhagem de 02/11 verbatim com acento e sha16 25010b04c17e8ce1), OIgual.lean:10 (curvas, sha16 1c05c03070544839), APonteDoAtrito.lean:7-10 (verbatim, sha16 e36df7f1245c7f16), delta RESSALVAS_V407[3] e ERRATA_E19 (sem « » nos resumos do acervo, rotulados [DECLARADO]), paragrafo do README (4). NAO corrigidos: «funciona sob compressão» (a fala e' «funcionar sob compressão»), «o psíon é o Nome da Luz» (a cunhagem no kernel e' «ψ é o Nome da Luz»), e os dois resumos do acervo com « » em Par.lean («ψ₊ψ₋ cancelado = vácuo»; «|G⟩ como produto não emaranhado») e em registros_v407.py:234 («psi+ psi- cancelado = vacuo»; «|G> como produto nao emaranhado»), que o acervo nao traz assim (traz «par cancelado», «ψ₊ψ₋ = Aniquilação (vácuo)», «posto de Schmidt 1 (não emaranhado)»). O resumo entre « » parece citacao exata e e' do agente de leitura.

*Evidencia:* r2_e_citacoes_out.txt (NAO: PsionCanto «funciona sob compressão», «o psíon é o Nome da Luz»; Par «ψ₊ψ₋ cancelado = vácuo», «|G⟩ como produto não emaranhado»; registros «psi+ psi- cancelado = vacuo»); grep -F no candidato: «psi+ psi- cancelado = vacuo» (1) e «ψ₊ψ₋ cancelado = vácuo» (1) presentes; o segundo resumo de registros_v407.py:234 atravessa uma quebra de linha de string no candidato; PSION_NO_ACERVO_03nov.md.

*Como corrigir:* Sem « » nos resumos (como ja' se fez em delta/README); nas duas citacoes do operador, o trecho exato («funcionar sob compressão»; «ψ é o Nome da Luz») ou sem aspas. Nas pedras, so' na proxima versao do modulo; em registros_v407.py:234 exige regenerar o candidato, entao fica dito. Nao trava.

## Verificacoes

- A (diff == declarado): diff de cada arquivo contra o seu .bak_r3_*: delta_v407.py (2 linhas: 263 e 266), registros_v407.py (55-58 e 155), artigo_pt/en_v407.pysnip (29 e 32 cada), pos_rito/textos_v407.py (1 linha de texto, 1099; + normalizacao de fim de linha, achado 2), pos_rito/textos_v407_novo.pysnip (230), rito_v407.sh (22): exatamente o declarado. Os .bak tem o sha16 == o da R2 em arquivos_revisados nos 6 arquivos de R2 (rito_v407.sh nao estava na lista). compile() limpo em delta, registros e textos_v407.py; bash -n limpo.
- Dos 28 arquivos de arquivos_revisados da R2, mudaram 7: o candidato, registros, delta, os dois pysnips do artigo, pos_rito/textos_v407.py e textos_v407_novo.pysnip — todos com .bak_r3. As 9 pedras, BUNDLE, KERNEL_RECIBO, runtime, gerar_candidato, comparar, ensaio, preparar_bundle, as guardas e pos_treino_v407.py: sha16 IGUAIS aos da R2. kernel/POS_BUILD_v407.json (Built 9, Replayed 0), KERNEL_RECIBO e FLAGS: mtime 15:10, inalterados.
- B (candidato novo 62a31fb08a3b7b97, 43.065.104 B): r3_a_intocados.py: 8 funcoes intocadas AST+fonte iguais a base; 25 nomes mudados (= COMPARACAO_V406_v407.json ok: 1150 iguais, 25 mudados, 0 sem explicacao, 0 removidos), 15 novos; r3_a2_mudados.py: 25 'expected_ladder' 11860->11958; r3_d_kernel.py: 9 embutidos == sandbox == pedra == BUNDLE, raiz = raiz v406 + 9 imports, 1755 embutidos == sandbox; r3_f_hashes.py: 55 conferencias, falhas []; ensaio_a_seco_v407.json: TUDO PASSOU, sha16 do candidato novo, artigo PT/EN pdflatex rc 0/0 sem erros; PRECONDICOES: TODAS PASSARAM; refazer_out termina em RC_REFAZER=0 e fim_de_cadeia_out em RC_FIM=0. As frases antigas (relidas inteiras, re-read in full, ponte nao e termo [KNOWN/ONTO], NAO diz 11 antigo) NAO estao mais no candidato; as novas estao (grep -F).
- r3_h_paragrafo_e_guardas.py: README renderizado de novo (paragrafo_renderizado_R3.txt), verificar_paragrafo_v407 sem falhas, 11 de 11 ressalvas inteiras, controle negativo reprova; guardas sobre 60 arquivos: so' os dois achados de sempre (o texto das proprias regras); r3_e_citacoes: nenhuma citacao nova.
- D (S1b): r3_l_s1b.py (copia _orq_sandbox; ORQ/LOG/ESTADO redirecionados; nenhum main): com o candidato novo e arquivos_revisados integros ABRE; com um arquivo de pos_rito alterado FECHA; com o proprio pos_treino alterado FECHA; aprovada string, sha16 de outro candidato e aprovada False FECHAM; ensaio final com a REVISAO real da R3 em r3_s1b_real_out.txt.
- Mapa de Rotas: consultado na R2 («v407»); nada novo a consultar para um diff de texto; a gerencia registra.

## Ressalvas

- R3 e' confinada ao diff: nao repeti os 283 s de lake env lean nem os 159 casos fail-closed nem a guarda do gerador / comparador / c16 / reading da R2, porque gerar_candidato_v407.py, comparar_v406_v407.py, ensaio_a_seco_v407.py, runtime_v407.py e as pedras tem o mesmo sha16 da R2.
- NAO examinei: o EN frase a frase (so' as duas trocas, em paridade com o PT); instalar, reverter, o rito; os PDFs alem do que o ensaio da cadeia registra.
- Independencia: mesma familia de modelo (Sonnet) da R1/R2, outra instancia da mesma linha; nada foi escrito fora de revisao_terceiro/.
- arquivos_revisados: as MESMAS 28 chaves da R2, com os sha16 atuais; rito_v407.sh segue de fora (so' comentario). Se qualquer arquivo listado mudar, esta revisao nao vale para ele.

## Arquivos que mudaram desde a R2

- `artigo_en_v407.pysnip`
- `artigo_pt_v407.pysnip`
- `delta_v407.py`
- `pos_rito/textos_v407.py`
- `pos_rito/textos_v407_novo.pysnip`
- `registros_v407.py`
- `um_v407_candidato.py`

## arquivos_revisados (sha16, relativo a v407/)

- `um_v407_candidato.py`: `62a31fb08a3b7b97`
- `base_v406/um.py`: `ddcb91930982d614`
- `BUNDLE_v407.json`: `6121ff5a51334dc3`
- `kernel/KERNEL_RECIBO_v407.json`: `210ad396fc6494cf`
- `runtime_v407.py`: `bd623db2bf04c136`
- `registros_v407.py`: `016106f0ccc29019`
- `delta_v407.py`: `58f280bc19863cf3`
- `artigo_pt_v407.pysnip`: `a80f672d8f3c7ec7`
- `artigo_en_v407.pysnip`: `38203865cb7900d6`
- `gerar_candidato_v407.py`: `3afa2dea0b9c9032`
- `comparar_v406_v407.py`: `4651222591e4f708`
- `ensaio_a_seco_v407.py`: `46443cde4b6272b6`
- `preparar_bundle_v407_03nov.py`: `27947dc318ba0170`
- `guarda_frases_v407.py`: `15a373c3a499fd2d`
- `guarda_p18_v407.py`: `aad2f6704557f7b4`
- `pos_rito/textos_v407.py`: `12c37a2a1fc786bf`
- `pos_rito/textos_v407_novo.pysnip`: `3239e6431925eb4b`
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
