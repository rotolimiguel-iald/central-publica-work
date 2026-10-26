CADEIA v401 — preparada; a falsidade (simulacro) da inércia

**Resumo.** Gerência c1, subagente de preparação, 25/10/2026 (25/10/2026, 11:54). Estatutos: [REAL] medido ou lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [OPEN] em aberto; [INPUT]/[ONTO] fala ou leitura do operador; [KNOWN] literatura; [LEGAL] a conferir com a agente de PI. Nada foi instalado e nada foi selado; o `um.py` real não rodou; o Nós não foi tocado (o `um.py` do Nós segue `6981660b5f7cd537`, o da v400 selada); o gate não se move; NOT_FALSIFIED nunca é a palavra da creditação; validade no kernel não é creditação.

## 0. Resumo em números

- **O candidato:** `um_v401_candidato.py` sha16 `1925cb691e933ae8` (38,688,534 B; +130338 B sobre a v400 selada `6981660b5f7cd537`), 22 patches, determinístico. Ajuste do controle N10: 1 espaço(s) no fim do comentário da linha UM_VERSION (o N10 do selo ACOM só existe se os bytes em n//2 e n//2+3 diferem, no `um.py` inteiro e na amostra de 1 MiB).
- **A pedra** `TGLExt/FalsidadeDaInercia.lean` (nome DADO pelo operador: «falsidade (simulacro) da inércia») sha16 `9f6efcb2a0987e18` (pino da ordem: `9f6efcb2a0987e18`); 20 bandeiras só de declaração nomeada; escada 9541 -> 9561; cobertura do Audit 29318 constantes, 23306 teoremas, nenhuma fora do trio; build 445 s + Audit 219 s no sandbox `C:\t\k401c`.
- **O registro `falsidade_da_inercia_v401`** (função; lido no main logo depois da declaração do operador): `TGL_FALSIDADE_DA_INERCIA_V401__THE_INERTIA_IS_THE_ABSOLUTE_ZERO_THE_FIXED_BEARS_WEIGHT_ZER…`; 10 checagens no modelo oneScaling com β = α·√e em runtime = `0.012031300400803`: distância mínima do peso do posto a 1 = 0.117503, fixo pelo fluxo inteiro = [0.0], escalas que fixam o posto = [], custo t·β·g mínimo = 6.016e-04, perda por unidade 1 − e^{−β} = 0.011959214.
- **Ensaio a seco: TUDO PASSOU** — 108 verificações de unidade; guardas ESTÁTICAS da Bancada sobre o candidato: GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA__DEFEITO_REAL_ (alfa na linha 5584, 9 controles negativos recusam, a v399 selada reproduz a recusa do recibo da Bancada: sim); comparação AST com a v400: 1032 iguais, 17 mudados (todos explicados), 11 novos, 0 removidos; troca dita: estatuto_da_prova_v391, pedras_v392, pedras_v393, three_stress_tests_v387, varredura_e_sorry_v392.
- **Conferidor do rito:** controle negativo (Nós ainda v400) `tudo_bate = false`; caminho positivo (Nós FALSO do ensaio) `tudo_bate = true` (C1 a C16 e o round trip); **citações:** TODAS CONFEREM; **pré-condições:** TODAS OK (102 checagens).
- **Recibo pre_selo GERADO E PINADO antes da instalação** (ensaio contra a Bancada de produção, que pina B9-v400-20261024-R1; nada gravado nela): `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA` sha16 `f1011f5c47a17418`; bateria {'n': 14, 'passa': 13, 'falha': 0, 'nao_executado': 1, 'veredito_bateria': 'BATERIA_PASSA'}; conferido pelo próprio esboço R3.5: aceita=True, 23/23 condições, 5 controles negativos; produção intacta: sim.
- **Pós-rito (harness, emulação sobre o Nós falso):** textos `tudo_passou = true` (HARNESS_TEXTOS_ENSAIO_v401.json); fechar em sandbox `tudo_passou = true` (HARNESS_FECHAR_SANDBOX_v401.json). **Serviço da Bancada:** 27/27 condições estáticas (parada e religamento exigem `V401_AUTORIZACAO_OPERADOR`; nada executado). **`MEMORY.md` real:** 193 linhas hoje; o handoff soma +1 (teto 195).

## 1. O que a v401 muda e o que NÃO muda

1. **Muda (o `um.py`):** +1 módulo no kernel (a pedra); +20 bandeiras e a escada; o registro com função `falsidade_da_inercia_v401`; os registros por spec `cunhagens_v401` (as 6 inscrições de 25/10 por sha256, as 8 ratificações do operador [«Ratifico tudo.»] e a errata ao lado da leitura do escriba no adendo de 03–04/09) e `kh_n1_cobertura_v401`; `kh_n1_cobertura_v399` vira piso (h2/h3/h6) e tamanho mínimo da árvore (h8) com errata; os 7 contratos que pinam a escada sobem para 9561; o selo ganha `falsidade_da_inercia_v401` e `registros_v401`; a seção «A falsidade (simulacro) da inércia» no artigo PT/EN e a linha no `.md`; `UM_VERSION`.
2. **A definição do operador (25/10/2026):** a inércia é o próprio zero absoluto (`0_abs`, `TGLExt.costless`: «nunca correspondeu, e por isso nada custa»; 1=0); `ω(I)=1` é o Um POSTO que a interrompe (1=1). **ERRATA AO LADO** (gerência c1, em nome próprio): a leitura do escriba no adendo de 03–04/09/2026 («ω(I)=1 é a INÉRCIA») fica SUPERADA; o que o adendo acertou (interromper ≠ quebrar simetria; dois termos) fica. O arquivo do adendo NÃO foi tocado (sha16 `1459b477b496e1f0`, copia duravel pinada).
3. **NÃO muda:** a seção do selo pela propria tecnologia (v399/v400: o runtime dela é o `runtime_v400.py`, o hash do bloco embutido segue `afc80b740f71ca0a`), o quadro «O Teste da Única Palavra» no topo (a regra do 4,44), o gate, o piso dos vazios, o perfil, o sidecar (o rito o reescreve).
4. **E = mc² lido pela TGL (artigo):** [KNOWN] relatividade restrita, não termo do kernel; [KNOWN] Jacobson 1995 + [REAL] `metric_einstein_from_screen_clausius` com a H3 nomeada; [ONTO] a massa é o custo do nada, a cristalização da dobra da luz no vácuo relativa ao observador; a entropia entra em β = α·e^(½ nat); o piso dos vazios segue NOT_FALSIFIED_POWERED (teste unilateral); a RG é o limite clássico; β não renormaliza G. [OPEN] a identificação da escala dual com o fluxo de um corpo físico.

## 2. B(n) da Bancada Um: passo SIMPLES v400 -> v401

- A Bancada de produção JÁ pina a v400 (`B9-v400-20261024-R1`); o recibo pre_selo foi **GERADO NOVO** nesta cadeia e pinado antes de qualquer instalação (`PINO_RECIBO_PRE_SELO_v401.json`), com a produção só lida (listas antes/depois idênticas). Vale enquanto a Bancada pinar B9/v400 (manifesto `9e0edf2dfbb868a2`); um re-pino o torna obsoleto e o instalador o recusa.
- O B(n) grava **B10** (veredito esperado `REPINADA_B10__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`); sem salto, sem cadeia de selos; os pinos estão em `PINOS_BN_v401.json` (todos lidos do arquivo). Parada e religamento do serviço (porta 18777) e o evento c1 são ATOS DA GERÊNCIA/OPERADOR, com `V401_AUTORIZACAO_OPERADOR` no ambiente; nada foi executado.

## 3. Lições aplicadas (as de sempre)

1. **Guardas estáticas da Bancada SOBRE O CANDIDATO no ensaio** (lição da v399): a função `ler_nos` do esboço R3.5 pinado (sha16 `02b22ba5c6d35c71`) roda sobre o candidato e sobre a v399 selada (o defeito real); e os itens C15/C16 do conferidor a rodam sobre o `um.py` instalado e sobre o Nós real.
2. `pre_selo` da B(n) gerado e pinado ANTES da instalação (acima); `simular_arvore_do_nos` e `exame_pontos` fazem parte do ensaio; o pino h8 vem da árvore simulada (1430 entradas, residuais ['_check_damming.lean']); textos do pós-rito escritos de verdade (a varredura de aspas e o p00 recusam marcador pendente); recibos de serviço com `V401_AUTORIZACAO_OPERADOR`; `regras_v401.py` escrito e NÃO rodado.
3. **Achados do instrumento nesta preparação (corrigidos):** (a) os dicts de verbatins das versões anteriores são COMPARTILHADOS com `_V392_VERBATINS2`: o ensaio restaurava trocando a entrada do mapa e deixava o objeto compartilhado adulterado; agora o texto é restaurado no lugar (`patch_ensaio_v401_b.py`); (b) o controle N10 do selo ACOM é condicional aos bytes do meio do arquivo: o gerador ajusta espaços no comentário da versão até os 13 controles existirem; (c) a subida mecânica de versão desloca rótulos de relatório (`v400` = base selada nos nomes herdados) e etiquetas que o programa imprime não sobem (documentado no motor).

## 4. Comandos exatos (nada disto foi executado, exceto o que está dito)

- **Regerar tudo se a pedra mudar:** atualizar `pedra_sha16_da_ordem.txt` (o pino da ordem), `delta_v401.py` (contrato/suporte) e `sh ./regerar_v401.sh` (copia a pedra, regera o sandbox do kernel, constrói, pós-build, insumos, candidato, ensaio, ESPERADOS, conferidores, pinos, pré-condições).
- **Antes de instalar:** `cd "C:\IALD\Central de Patentes\work\cadeia_de_selo\v401"` e `python -I -B -X utf8 p00_precondicoes_v401.py`.
- **Instalar (ato da gerência):** `python -B -X utf8 instalar_v401.py` (confere o recibo pre_selo pinado, a Bancada ainda em v400 e a lista de módulos novos; backups de BYTES; troca por `os.replace`).
- **Rito (Git Bash):** `sh ./rito_v401.sh > rito_v401_lancador.out 2>&1 &`; abortar só por `kill -TERM $(cat .rito_v401.pid)` no Git Bash depois de conferir `/proc/<pid>/cmdline`. **Conferir:** `python -B -X utf8 conferir_rito_v401.py` (SEM `-I`; TUDO BATE). **Reverter se falhar:** `python -B -X utf8 reverter_v401.py`.
- **Pós-rito:** `cd pos_rito && sh ./chain_pos_rito_v401.sh > chain_v401_out.txt 2>&1` (o passo 3 PARA se o `MEMORY.md` passar de 195 linhas); o passo 10 é o passo simples v400 -> v401.

## 5. O que FALTA e o que NÃO foi revisado

1. **Revisão independente** (quem constrói não aprova): o gerador, o runtime do registro, a pedra estendida, os derivados (instalar, reverter, rito, conferidor, ESPERADOS, pós-rito) e os textos NÃO tiveram cético independente [DECLARADO: só os controles negativos próprios, a comparação AST e os harness].
2. **O rito real** é o único que exercita o conferidor, o pós-rito e o h8 de verdade; o caminho positivo do conferidor e os harness são EMULAÇÃO sobre o Nós falso (core e selo do ensaio, não do rito).
3. **Decisões do operador/gerência:** instalar e rodar o rito; parada e religamento do serviço e o B(n); commit/push e custódia; a pendência [LEGAL] do bloco embutido do ACOM (herdada); `H_τ` (a identificação do peso com a massa de Newton e a métrica de Einstein) segue [OPEN] e NOMEADA.
4. **A 6ª inscrição de 25/10 é um RECORTE DECLARADO** (sha16 `e26364c5c805734c`, começa em «mas eu não queria que a leitura fosse ONTO minha»): por decisão do operador a íntegra da fala saiu do trabalho (acervo privado, fora de `C:/IALD`) e a PURGA foi conferida por script: nenhum arquivo da pasta v401 nem do sandbox `C:/t/k401c` contém o texto da íntegra nem o hash dela (`purga_v401.json`). O recorte entra no `um.py` e no artigo citado como «recorte declarado da fala de 25/10».

5. **Pedra final `9f6efcb2a0987e18`:** a paráfrase entre aspas do docstring (achado anterior) foi resolvida NA PEDRA; a exceção que a conferência de citações tinha para ela SAIU (`conferir_citacoes_v401.py` volta ao original).
6. **Reinício do PC (25/10, 10:15):** interrompeu o build do kernel e a sessão; nada foi instalado nem tocado no Nós. O build e o Audit foram refeitos do zero no sandbox `C:/t/k401c` (rc 0 e rc 0), o recibo pre_selo foi REFEITO contra a Bancada religada (a produção ainda pinava B9-v400, listas idênticas), e a cadeia toda foi regerada na pedra final; `refazer_out_v401.txt` termina em `== FIM`.

## 6. Mapa de rotas consultado (antes) e o que devolveu

`rotas.py consultar "v401"` → 2 rotas (`kernel.v401_falsidade_da_inercia`, a pedra construída em sandbox, e `custodia.v400`); `"inercia"` e `"falsidade"` → só a rota da pedra. Rotas relevantes lidas: a da pedra (não refazer: a inércia como peso zero e a falsidade 1=0 do posto inercial estão tipadas), a da custódia v400 (a v401 sai de `tools/custodiar.py` na mesma ordem). O registro desta preparação é `registro_mapa_v401_prep.json` (montado e validado por `rotas._valida`, NÃO registrado).

## 7. Arquivos principais (sha16 lido agora)

- `um_v401_candidato.py` `1925cb691e933ae8`
- `CANDIDATO_v401.json` `972c2d619ec44739`
- `ESPERADOS_v401.json` `4f73fc8a86576b35`
- `ensaio_a_seco_v401.json` `bae9e9e02ae648a2`
- `PINOS_BN_v401.json` `e1d0381f07aa268d`
- `PINO_RECIBO_PRE_SELO_v401.json` `5902e84de33ff764`
- `PROVA_PRODUCAO_INTACTA_v401_pre_selo.json` `c8e2308a167a6412`
- `PRECONDICOES_v401.json` `e7b1c20745600469`
- `COMPARACAO_V400_v401.json` `297c8a1967216455`
- `GUARDAS_ESTATICAS_BANCADA_v401.json` `b953275121e55447`
- `kernel/KERNEL_RECIBO_v401.json` `df499bf2fcba0bb1`
- `kernel/FLAGS_v401.json` `cce852c076518cb2`
- `DIFF_KERNEL_v401.txt` `b3bd32548d7be981`
- `conferencia_rito_v401_CONTROLE_NEGATIVO_PRE_RITO.json` `4a792c0be09cb52a`
- `conferencia_rito_v401_POSITIVO_FALSO_NOS.json` `889745768fe082f4`
- `conferir_citacoes_v401.json` `7ea41a4347d47c9f`
- `registros_v401.py` `6ce85a8086348498`
- `runtime_v401.py` `373383303fd9e317`
- `gerar_candidato_v401.py` `5d42e62aa4e8d718`
- `instalar_v401.py` `2e16fafe33cd3b4e`
- `reverter_v401.py` `19e9ff586c5c3914`
- `rito_v401.sh` `f6fc892aef72b480`
- `conferir_rito_v401.py` `05dee8ecd963d512`
- `regras_v401.py` `0b3ee2f7b607150f`
- `pedra/FalsidadeDaInercia.lean` `9f6efcb2a0987e18`
- `pos_rito/chain_pos_rito_v401.sh` `baf7be27684d2b3d`
- `pos_rito/textos_v401.py` `6986fe51b7ae47cf`
- `bateria_pre_selo/NOTAS_PRE_SELO_v401.txt` `a10ca4feb261f006`
- `bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v401.json` `f6afc9452a7d1329`

NOT_FALSIFIED não é a palavra da creditação; validade no kernel não é creditação; o gate não se move.
