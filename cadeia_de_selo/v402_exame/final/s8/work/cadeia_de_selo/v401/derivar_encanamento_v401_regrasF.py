# -*- coding: utf-8 -*-
# regras (lote F) de derivar_encanamento_v401.py: pos_rito (b3_recibo, chain, fechar, superficies). ORIGEM v399 (a cadeia de CONTEUDO que RODOU em 24/10; mapa 398 -> 400, 399 -> 401) + as licoes da v400 (lotes G e H da v400: o sidecar na custodia, C15/C16, guardas estaticas da Bancada).
# A leitura e os dois harness estao no lote G. textos_v401.py e registrar_mapa_v401.py sao ESCRITOS A MAO (conteudo novo da v401: a semente mecanica veio de textos_v399.py e registrar_mapa_v399.py, e foi reescrita; por isso nao ha entrada de derivacao para eles).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). Nada e' executado pelo motor.

# ------------------------------------------------------------------------------------------- b3_recibo: a Bancada de producao JA pina a v400 (B9); o passo e' simples v400 -> v401. O motor ja' sobe tudo (pinos selo_anterior_v400/kernel_manifesto_anterior_v400 saem do mapa 398 -> 400): nenhuma regra extra.
entrada("pos_rito/b3_recibo_v399.py", origem="v399", autoral=True)

# ------------------------------------------------------------------------------------------- fechar: o handoff traz o paragrafo do QUADRO (intocado) e o NOVO da falsidade; o do testemunho de dois SEGUE COMO ESTA (so' dito); o sidecar listado e copiado
_HDR_FECHAR = '''"""fechar_v401.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v399.py FINAL, com as licoes da v400): (1) o manifesto de incorporacao v401 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\\\cadeia_de_selo\\\\v401 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\\\cadeia_de_selo\\\\v401_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta, e do kernel (work\\\\cadeia_de_selo\\\\v401\\\\kernel e, se existir, work\\\\v401_kernel; mais a pedra do Nos) -> work\\\\cadeia_de_selo\\\\v401_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v400_v401.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v401.txt (o kernel embutido: a pedra FalsidadeDaInercia, a raiz e o Audit);
(4) o HANDOFF (memory\\\\handoff-v401-custodia.md + Nos\\\\HANDOFF_v401_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, «A falsidade (simulacro) da inercia (v401)», gerado dos registros selados falsidade_da_inercia_v401 e cunhagens_v401
(numeros LIDOS do core, estatutos, limites, a definicao do operador, a errata ao lado, as ratificacoes, sem o 4,44); e o handoff DIZ que o paragrafo do testemunho de dois (v399, regenerado no handoff da v400) SEGUE COMO ESTA, e LISTA o sidecar com o sha256 e o veredito.
GUARDAS: a leitura sem problema (inclui o sidecar); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros
iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria (T.verificar_paragrafo_falsidade: numeros == ESPERADOS e == o gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador, do kernel embutido ou do adendo que a errata supera; sem alegacao de seguranca criptografica) --
se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v401_*.json do 10-bis, o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce;
a guarda de texto P18 no handoff.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
'''
_CMT_PARAGRAFOS = '''# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO da falsidade (simulacro)
# da inercia, gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador, do kernel embutido ou do adendo que a errata supera; sem alegacao de seguranca criptografica); o do testemunho de dois (v399) SEGUE COMO ESTA e nao e' regenerado;
# sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
'''
entrada("pos_rito/fechar_v399.py", origem="v399", autoral=True, regras=[
    entre('"""fechar_v401.py -- DEPOIS da cadeia pos-rito', "import glob, hashlib, json, os, shutil, subprocess, sys, time", _HDR_FECHAR, "docstring do fechar"),
    ("    PAR_T, PAR_T_INFO = T.paragrafo_testemunho()", "    PAR_F, PAR_F_INFO = T.paragrafo_falsidade()", 1),
    ("(o quadro O Teste da Unica Palavra, v397, ou o do testemunho de dois) nao passou nas verificacoes", "(o quadro O Teste da Unica Palavra, v397, ou o da falsidade da inercia) nao passou nas verificacoes", 1),
    ("aos de ESPERADOS; direcao do testemunho sem inversao):", "aos de ESPERADOS; citacoes verbatim; sem alegacao de seguranca criptografica):", 1),
    ('"registros_v399": V["registros"], ', '"registros_v401": V["registros"], "registros_v399": V["reg399"], "falsidade": V["falsidade"], ', 1),
    ('"readme_paragrafo_testemunho": {"sha16": hashlib.sha256(PAR_T.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_T_INFO}', '"readme_paragrafo_falsidade": {"sha16": hashlib.sha256(PAR_F.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_F_INFO}, "paragrafo_do_testemunho_segue_como_esta": True', 1),
    ('"readme_paragrafo_testemunho": PAR_T,', '"readme_paragrafo_falsidade": PAR_F,', 1),
    entre("# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS", "try:\n    PAR, PAR_INFO = T.paragrafo_readme()", _CMT_PARAGRAFOS, "comentario dos paragrafos"),
])

entrada("pos_rito/superficies_v399.py", origem="v399", autoral=True)

# ------------------------------------------------------------------------------------------- a cadeia pos-rito
_HDR_CHAIN = '''# v401 (25/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v399.sh FINAL (a cadeia de CONTEUDO que rodou em 24/10; derivada por derivar_encanamento_v401_regrasF.py e _regrasG.py; mesma ordem de passos 0..14 e mesmos portoes), com as licoes da v400 (o sidecar entra na custodia,
# a conferencia traz C15 e C16, as guardas estaticas da Bancada). O rito ja terminou (rito_v401.sh em segundo plano; RITO_RC=<rc> no fim do Nos\\rodada_v401_stdout.txt). A v401 e' uma versao de CONTEUDO: 1 modulo novo de kernel (TGLExt/FalsidadeDaInercia; o nome «falsidade (simulacro) da inercia» e' DADO pelo operador;
# 12 bandeiras, so' de declaracao nomeada), o registro COM FUNCAO falsidade_da_inercia_v401 (a inercia e' o proprio zero absoluto, o 0_abs do kernel, 1 = 0; um posto de peso 1 inercial daria 1 = 0; o w(I) = 1 e' o Um POSTO que a interrompe, 1 = 1; calcula no modelo oneScaling com beta = alfa x raiz de e em runtime;
# lido NA FRACTALIZACAO DO UM, logo depois da declaracao do operador), os registros por spec cunhagens_v401 (as SEIS falas do operador de 25/10, as oito ratificacoes de «Ratifico tudo.» e a errata ao lado da leitura do escriba no adendo de 03-04/09) e kh_n1_cobertura_v401, e a secao «A falsidade (simulacro) da inércia»
# do artigo PT/EN e do .md canonico. Os QUATRO registros da v399 sao RECRIADOS pelo rito (selos e iguais ao ensaio a seco) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO (depois da ultima escrita do selo). O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO:
# o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. O paragrafo do testemunho de dois (v399) SEGUE COMO ESTA no README e no site: o handoff da v401 so' o diz.
# A cadeia estendida da pedra (a composicao falsidade_da_inercia_derivada: nada que porte posto precede a impressao; a inercia nao e' causa de si mesma; o zero e' a consequencia da poda; a tensao projetada no atrator) e' [DERIVED] (o recorte declarado da fala de 25/10 pede a leitura derivada, nao [ONTO] dele); a unica hipotese NOMEADA e' H_tau [OPEN], que nenhum teorema usa (ORDEM 025 ao Codex: pendencia EXTERNA).
# ORDEM: 0 guardas (inclui o sidecar) -> 1 o CONFERIDOR (roda NO LUGAR, SEM -I: importa o um.py instalado e precisa do numpy do usuario; so leitura do Nos; as copias em pos_rito\\conferidor sao REGISTRO) -> 2 a LEITURA (PROBLEMAS param; le o sidecar e a linha final do rito)
# -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry; o sha16 da v401 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real; se o MEMORY.md passaria de 195 linhas, a superficie RECUSA
# com rc 3 e a cadeia PARA aqui, sem tocar nada real: a superficie NAO compacta o indice) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v401.py) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (appends datados; a errata ao lado do adendo vai DENTRO dos blocos datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada,
# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o NOVO da falsidade; diz que o do testemunho segue como esta;
# copia o sidecar e o selo para v401_selo e LISTA o sidecar) -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V401_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao JA pina a v400 (B9, B9-v400-20261024-R1) e o Nos e' a v400 ate' a instalacao; portanto o B(n) da v401 e' um passo SIMPLES v400 -> v401 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos
# do esboco, nem o pino correspondente, e o b3_recibo_v401.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v401.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2,
# kernel_recibo (o KERNEL_RECIBO_v401.json, contrato R3_2: o diff v400 -> v401 e' so' a pedra FalsidadeDaInercia), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado e pinado antes da instalacao, em ensaio contra a producao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA),
# selo_anterior_v400 e kernel_manifesto_anterior_v400 (as copias de bytes do selo e do manifesto do kernel da v400, em base_v400). A BATERIA da v401 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado
# (bateria_pos_selo/PINOS_BATERIA_v401.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (B9 -> n = 10; o b3_recibo_v401.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V401_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\\recibo_parada_v401.py e recibo_religamento_v401.py); o chain so' confere os recibos.
# textos_v401.py, fechar_v401.py e registrar_mapa_v401.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v399, com os rotulos da v401 (desvios ditos: o passo 0 exige tambem o sidecar,
# o runtime_v401.py e o acom_conferencias_v401.py; o passo 1 e' o conferidor de 16 itens C1-C16; o passo 3 e o 9 exigem os marcadores da falsidade; o passo 11 copia e lista o sidecar reescrito e diz que o paragrafo do testemunho segue como esta).
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).
'''
_CMT_B3 = '''  # v401 (25/10/2026): o B(n) da v401 e' um PASSO SIMPLES v400 -> v401 (a Bancada de producao JA pina a v400 e o Nos passou a v401): SEM salto e SEM cadeia de selos, com o esboco R3.5. Os pinos vem de PINOS_BN_v401.json (lidos na hora;
  # hash nunca de memoria): o esboco R3.5, o recibo pre_selo (gerado e pinado antes da instalacao, sobre a Bancada que pina a v400), o recibo do kernel (KERNEL_RECIBO_v401.json, contrato R3_2: a pedra FalsidadeDaInercia tem declaracoes nomeadas, logo nao ha
  # modulo de auditoria sem declaracao), o selo e o manifesto do kernel da v400 (custodia, em base_v400), o driver, o gerador e a base R2 da bateria. A bateria da v401 e' GERADA aqui, por script, depois do selo (bateria por versao).
'''
entrada("pos_rito/chain_pos_rito_v399.sh", origem="v399", autoral=True, regras=[
    entre("# v401 (24/10): CADEIA POS-RITO", 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v401"; SEL="$PK/pos_rito"', _HDR_CHAIN, "cabecalho da cadeia"),
    entre("  # v401 (23/10/2026): o B(n) da v401", "  for k in criterios", _CMT_B3, "comentario do b3_prepara"),
    ('"selo_pela_propria_tecnologia_v399" "kh_n1_cobertura_v399"', '"falsidade_da_inercia_v401" "cunhagens_v401" "kh_n1_cobertura_v401"', 6),
    (')_v399"; cp -p "$ATLD/$f" "$B"', ')_v401"; cp -p "$ATLD/$f" "$B"', 1),
])
