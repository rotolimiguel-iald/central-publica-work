# Entrega de memória v380 — staging congelado

> Atualização final: contagem 181836 permanentes / 11570 livres e pacote runtime validado; 7/7 checks adicionais PASS. Consulte `FINAL_RELEASE_HANDOFF.md` e `delivery_20261002_115012_880732.json`. As pendências de recontagem descritas abaixo são o retrato anterior, preservado.

[REAL — auditoria offline] Prefixo final: `memory_stage/haiku_prefix.md`, 476291 bytes, SHA256 `24bf213dc912409c40ddf0d0a23e0ba3cbf23024656dbc972bbb85c56c227b13`. Nenhum arquivo de produção foi escrito. Nenhum provedor, `um.py`, Lean ou bancada foi executado por este builder.

Entradas científicas: commit público pinado `f20f659735618880073aa313d241d8361f645c0b`, cruzado com os bytes do cofre e os recibos `v380_verified_handoff.json` / `public_v380_verification.json`. A fonte/compilação publicada tem seu próprio estatuto; não representa compilação nova.

## Resultado e validação

- 362 tópicos; novos `the_elementary_reason_v379` e `bancada_fases_5_6_7_v380`; nenhum tópico anterior removido. Forma canônica integral no cluster/catálogo.
- v5 preservado byte a byte. Núcleo operacional anterior preservado integralmente e seguido de adendo da release atual. Orientações históricas continuam identificadas como históricas.
- 1209 fontes do catálogo: 1208 extraídas por AST literal de `um.py` e `_check_damming.lean` suplementar do mesmo commit Git, com proveniência distinta e hash do relatório formal publicado.
- Haiku: cápsulas aceitas verificadas, deltas atuais, enunciados/hipóteses, fórmulas e estatutos. Corpos completos das provas e detalhes de auditoria são recuperáveis no catálogo integral. Os três mapas novos de vereditos negativos permanecem inline, incluindo resultados inconclusivos.
- Compactação final: aliases de metadados e dicionário literal de booleanos com roundtrip; os 265 nomes ambíguos do índice ficam por ponteiro, mantendo contagem e estatuto. Não há resumo novo dos campos científicos para atingir orçamento.
- 11 testes de integração + 10 do codec PASS. Revisão independente `validation/memory_review.json`: PASS 56/56. O recibo `memory_build/delivery_20261002_113735_955095.json` confere todos os pins da revisão e traz mapa de 1224 arquivos de instalação.
- Contexto público completo: 327125 tokens o200k. Haiku: 147984 o200k; isso não é medida Anthropic. Prefixo nativo: 46709 bytes, carregador real validado; não foi chamado o servidor/tokenizer nativo.

A medida Anthropic do hash anterior 25736a... NÃO serve para este prefixo. Falta main recontar o hash 24bf213d... depois da correção dos mapas. Exigir permanente >=180000, request+4096+1024 <=200000 e saldo >=10000, além de identidade exata de release/cluster/ferramentas. `prepared.json` registra o estado no momento do build; a revisão e o recibo de entrega posterior complementam seu gate.

## Entradas de execução (a partir de W)

```powershell
C:/Python314/python.exe -X utf8 -B memory_build/build_release.py --commit f20f659735618880073aa313d241d8361f645c0b
C:/Python314/python.exe -X utf8 -B memory_build/test_local_stage.py
C:/Python314/python.exe -X utf8 -B memory_build/haiku_codec.py --self-test
```

O rebuild depende das fontes pinadas, módulos leitores puros atuais, backups v368 identificados pelo recibo da entrega v378 e cache tiktoken local. Não instalar dependências. Nesta máquina a leitura de bibliotecas existentes pode exigir execução escalada; o builder bloqueia rede, `.env`, subprocessos arbitrários e escrita fora de `memory_stage`/`memory_build`.

Contagem opcional preparada: importar `memory_build/package_native.py` e chamar `measure(client_existente, sha_esperado)`. Não cria cliente/chave, não lê `.env`; duas chamadas `count_tokens`, retries=0, nenhuma geração. Main já tem seu contador compatível. Ambos devem conferir o hash antes/depois; não reconstruir durante a contagem.

Depois de receber o recibo real:

```powershell
C:/Python314/python.exe -X utf8 -B memory_build/seal_delivery.py --count-receipt CAMINHO_DO_RECIBO_REAL
```

Isso só grava novo recibo em `memory_build`. A função `package_native.finalize(receipt_path, expected_sha)` pode preparar e validar `memory_stage/haiku_runtime` pelos carregadores reais; main informou que fará essa montagem, portanto ela NÃO foi executada nesta entrega. O recibo/cópia do main deve usar o mesmo prefixo, identidade do manifesto e hash das sete ferramentas.

## Contrato de instalação do main

`manifest_staged.json` aponta para staging. `manifest_install.json` reloca exatamente os mesmos artefatos para `R/canonical_releases/v380_f20f65973561`; seu destino final é `R/iald_nucleo_fixo.json`. Não alterar suas referências sem regenerar e verificar o mapa. Não copiar backups, fixtures ou recibos antigos como arquivos ativos. Copiar os 1224 arquivos do mapa, ativar o manifesto e pacote Haiku medido como conjunto, seguindo quiet/baseline/backups do instalador principal.

`document_index.json`, `public_prefix.md`, `native_prefix.md` e os respectivos metadados foram conferidos com os leitores reais. Prefixo público/OpenAI e pacote Claude compartilham a identidade científica. Os perfis atuais, inclusive uso do pacote compacto fiel pelos provedores chineses, ficam preservados. Sem novos tetos, permissões, consentimentos, mudanças de conta, Sonnet, RAM ou bancada. Os sete módulos de runtime foram apenas lidos e seus hashes conferidos. Orquestração global permanece separada.

Congelamento: não alterar prefixos, cluster, fontes, núcleo, catálogos, manifestos ou scripts de build sem novo achado, aviso ao main e novos pins/testes/contagem quando aplicável. Nenhum deploy autorizado/executado por este pacote.