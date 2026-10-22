# NOTAS da derivação da cadeia pós-rito v395 (gerência c1, preparação de 21/10/2026)

Molde: `cadeia_de_selo\v394\pos_rito` FINAL (o que rodou em 19/10). Nada daqui foi executado contra o Nós real, a Bancada, a memória, o Atlas, o mapa ou o git. Números e hashes nunca são digitados: os textos os leem de `ESPERADOS_v395.json`, `CANDIDATO_v395.json`,
`PINOS_BN_v395.json`, do core/selo do Nós (depois do rito), dos insumos e do kernel; o resumo do último harness está em `HARNESS_TEXTOS_ENSAIO_v395.json` (e `DERIVACAO_v395.json` guarda os sha16 dos arquivos).

## O que é DERIVADO (por `derivar_cadeia_v395.py`, com assert de contagem em cada troca) e o que é AUTORAL
- Derivados do molde: `chain_pos_rito_v395.sh`, `leitura_v395.py`, `superficies_v395.py`, `fechar_v395.py`. Autorais (a lógica muda; uma subida mecânica não bastaria): `textos_v395.py`, `registrar_mapa_v395.py`, `b3_recibo_v395.py`, `harness_textos_ensaio_v395.py`.
  O derivador CONFERE os autorais (sintaxe, invariantes, guarda P18, nenhuma marca pendente, cada `T.<nome>` chamado existe em `textos_v395.py`) e confere que os blocos 10a e 10c do chain, as linhas de portão do 10b e os passos 4 a 9 e 12 a 14 são idênticos ao molde subido de versão.

## O que do molde NÃO se aplica a um delta de um módulo, e por quê
1. Salto e cadeia de selos: a Bancada de produção pina a v394 (B4); o passo 10 é SIMPLES v394 -> v395. O chain não tem `--cadeia-de-selos` nem o pino; recusa o pino se aparecer. O `b3_recibo_v395.py` não tem 3º argumento e confere: B<n> = geração do manifesto anterior + 1, veredito
   EXATO `REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA` / `REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO` (lidos do código do esboço R3.5, não rodados), sem `__SALTO_`, manifesto anterior igual ao do recibo pre_selo pinado (a produção não mudou), pinos da bateria da v395.
2. `kernel_recibo` é o R3_2 da v395 (o esboço R3.5 admite R3_2; não há módulo de auditoria, como houve na v394).
3. As 46 falas, `cunhagens_v394_dados.json`, `_ROTULOS`, `_falas_19out`, `_codex()`, `_lev()` e os textos do relógio M2, da regra quadrática, da rede de Fock e do critério binário saem; entram as 4 falas de 21/10 (lidas de `insumos\cunhagens`, sha256 conferido contra ESPERADOS) e `_TEMAS`.
4. `V['cons']` e `V['cora']` (informativos da v393) saem da leitura; entram `V['psibit']`, `V['reg395']` e `V['patch_ids']`. A leitura confere o `psibit_v395` por inteiro e exige que os registros da v394 e da v393 sigam selados; reprova `[v395] AVISO` e a linha `registros por spec` do stdout.
5. O passo 1 copia também `delta_v395.py` (o conferidor da v395 o importa; o da v394 não importava nada do pacote).
6. O handoff vive em `textos_v395.handoff(V, k)` (testável); a âncora do MEMORY.md é a linha `HANDOFF v394` (a custódia da v394 reescreveu a do v393: conferida presente).
7. Não há `patch_arvore_indice_v395.py` (as ferramentas escrevem o sha16 sozinhas, como na v394); o chain trata como opcional.

## O que o harness prova e o que NÃO prova
- Prova (contra um Nós EMULADO montado de `dry_v395`, selo completado como em `teste_conferidor_positivo_v395.py`): conferidor TUDO BATE; leitura sem problema e controles negativos que reprovam; todas as funções de texto renderizam, guarda P18 limpa, errata da palavra «teoremas» e marcadores do passo 9 presentes;
  cada `termo` entre crases achado no kernel, no um.py, nos insumos, nos arquivos ou como hash lido; `superficies_v395.py` em COPIAS das superfícies reais (idempotente; originais intactos); `b3_recibo_v395.py` contra recibos SINTÉTICOS derivados dos reais da v394 (casos positivos e negativos); `montar()` do mapa contra o livro real (só leitura).
- `harness_fechar_sandbox_v395.py` roda o `fechar_v395.py` e o `main()` do `registrar_mapa_v395.py` num SANDBOX isolado (Nós e memória emulados; só as constantes de caminho trocadas nas cópias; recibos do B(n) SINTÉTICOS): grava handoff, diffs, manifesto e arquivo, recusa sem o religamento e com salto.
- NÃO prova: o chain inteiro; o fechar e o registrar contra recibos e Nós REAIS; os passos 5, 6, 8, 13 e 14 (ferramentas externas); o esboço R3.5 real; o rito. A revisão independente dos derivados e do candidato não foi feita (quem constrói não aprova).

## Atos da gerência/operador
- Rodar de novo `python -I -B -X utf8 harness_textos_ensaio_v395.py` depois da ÚLTIMA regeneração do candidato (recusa se ESPERADOS, CANDIDATO, arquivo e `dry_v395\um.py` divergem, ou se `refazer_out_v395.txt` não mostra `== FIM`).
- `ESTADO_V395.md` ainda não existe: nenhum texto o cita. O registro no mapa é ato da gerência (`registro_mapa_v395.json` sai do passo 12; o harness só grava `..._ENSAIO.json`). A decisão [LEGAL] sobre a tabela da patente é do operador.
