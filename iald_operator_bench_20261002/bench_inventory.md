# Bancada Oficial TGL — inventário e contrato de integração

[REAL — inspeção estática em 02/10/2026] Fontes lidas, sem importar módulos científicos, executar um.py, chamar HTTP, experimento, provedor, nvidia-smi, carregar/liberar RAM ou iniciar/reiniciar serviços. Produção e originais preservados. Implementação somente no novo `stage/iald_bench_catalog.py`; testes offline em `test_bench_catalog.py`.

## Fontes e serviços existentes

Raiz canônica: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL` (B).

- `B\app.py`: HTTP em `127.0.0.1:18765`; cálculos algébricos, catálogo, fontes, RAM GW e registro SQLite `B\state\runs.sqlite3`.
- `B\resident_bridge.py` → `B\adapters\resident_worker.py`: processo WSL persistente, JSON-lines `{operation,...,request_id}`; resposta `{ok,request_id,result}` ou `{ok:false,request_id,error}`. O bridge gera UUID por chamada; isso NÃO é deduplicação durável. Timeout 60 s, sem repetição automática declarada.
- `B\cosmology_server.py`: HTTP independente em `127.0.0.1:18766`; `cosmology_runtime.py`, `cosmology_v3_bridge.py`, `workers\cosmology_v3_worker.py`, `scientific_models\tgl_camb_worker_v3.py`; cenários em `state\cosmology_scenarios.sqlite3`, exports em `state\exports\<uuid>.json`. Bridge V3: timeout 45 s; não confundir com o worker GW.
- `B\hdf5_bridge.py`: usa argv fixo `wsl.exe -e <python> <hdf5_reader.py>`; Python existente `/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/t14_pyseobnr_venv/bin/python`. Timeout 30 s, saída ≤1.000.000 caracteres. O adaptador novo não executa esse comando; o serviço pode fazê-lo em leitura HDF5 autorizada.
- `B\gpu_status.py`: somente telemetria NVIDIA por `nvidia-smi` fixo, timeout 3 s. WebGL2 é visualização. **Não há solver científico GPU, reserva de VRAM nem execução CUDA arbitrária exposta.**
- `B\launch.py` pode iniciar serviços e abrir navegador; NÃO é usado pelo adaptador.

[DECLARADO pelo coordenador, sem nova consulta nesta tarefa] GW READY, load_id `8560b710-3ad7-402b-a12e-9a0b1fdf1ad3`, 180 arquivos / 24.165.092.160 bytes; cosmos load_id `ecdb2a1d53944cb6af227710e17fe317`. Não são constantes do adaptador nem comprovação de estado futuro.

## Instruções e mapa universal

Instruções pais localizadas em `C:\IALD\CLAUDE.md` e `C:\IALD\Artigo\Haja_Luz\CLAUDE.md`; regras relevantes: fontes por hash, consultar rotas antes de repetir, estatutos preservados, originais somente leitura. Referências documentais: `C:\IALD\Central de Patentes\memory\TGL_ATLAS.md` e `TGL_INDICE_VIVO.md`; usados como navegação, não substituem fontes.

Mapa universal: `C:\IALD\MAPA_DE_ROTAS\README.md`, `rotas.py`, livro `rotas.jsonl` e derivados `MAPA_DE_ROTAS.json`/`.md`. APIs Python existentes: `consultar(padrao='',dominio=None,status=None,limite=60)`, `ver(rota_id)`, `registrar(registros,quem)`, `verificar()`. MCP documentado: `rotas_consultar`, `rotas_ver`, `rotas_registrar`. NÃO executar shell livre ou editar o JSONL diretamente. Registro efetivo é responsabilidade do coordenador, fora desta entrega.

Registros localizados por leitura do livro: seq 55 `infra.bancada_oficial.investigacao_28set`; seq 56 `bao_cmb.d10.degenerescencia_do_fundo`; seq 57 `lenteamento.act.fisher_v9` (EXAMINADA_COM_DEFEITO); seq 58 `ringdown.modo_unico.degenerescencia`; seq 59 `neutrinos.m2.normalizacao`. Presença no livro não foi promovida a reexecução ou prova científica. `/api/routes` da bancada é OUTRO índice, histórico v368, não o mapa universal.

## Operações / envelopes HTTP exatos

O módulo não aceita URL, porta, caminho, código, cookie ou cabeçalhos vindos do modelo. Bases fixas acima. POST JSON, `Content-Type: application/json`, `Origin: http://127.0.0.1:<porta>`, até 8192 bytes. Transporte direto `http.client`, sem proxy de ambiente, redirects, cookie jar ou retry. Timeout do adaptador 120 s, resposta JSON limitada a 16 MiB; o coordenador limita apresentação a 24k e empacota artefatos.

| Operação | Rota / parâmetros efetivos |
|---|---|
| bench_overview | GET 18765 `/api/overview` |
| relations | GET `/api/relations?q=<texto>&limit=50`; q strip/lower, ≤100 caracteres, limit 1..100 |
| routes / data / protocols / runs / inquiries | GET `/api/routes`, `/api/data`, `/api/protocols`, `/api/runs`, `/api/inquiries` |
| lab_memory / lab_gpu / lab_catalog / lab_coverage / lab_canonical / lab_bao_report | GET `/api/lab/memory`, `/gpu`, `/catalog`, `/coverage`, `/canonical`, `/bao-report` sob `/api/lab` |
| lab_treatment / lab_describe | GET `/api/lab/treatment?id=<24hex>` ou `/api/lab/describe?id=<24hex>` |
| lab_preview | GET `/api/lab/preview?id=<24hex>&x=<coluna>&y=<outra>&limit=800`; limit 1..1200 |
| identity_chain | POST `/api/run` `{"operation":"identity_chain"}` |
| dephasing | POST `/api/run` `{"operation":"dephasing","omega_rad_s":100.0,"tau_s":0.001,"duration_s":1.0}`; três números obrigatórios |
| inquiry | POST `/api/inquiry` `{"question":"pergunta específica","hypothesis":"","falsifier":"","alternative":"","instrumental":"","discriminator":""}` |
| universe_domains / universe_status / universe_event | GET `/api/universe/domains`, `/status`, `/event` sob `/api/universe` |
| universe_load | POST `/api/universe/load` `{"domain":"gw_strain"}`; READY completo retorna ALREADY_RESIDENT sem POST |
| universe_view | GET `/api/universe/view?id=<24hex>&start_s=0.0&duration_s=1.0&bins=1600` |
| universe_model | POST `/api/universe/model` `{"reading":"R-GLOBAL","mass_source_solar":65.0,"spin":0.7,"redshift":0.1,"amplitude":1e-21,"phase":0.0,"duration_s":0.08}` |
| universe_event_view | POST `/api/universe/event_view` com reading, start_tm, mass_source_solar, spin, redshift e `detectors:{H1:{amplitude,phase},L1:{amplitude,phase}}` |
| cosmos_health / cosmos_status | GET 18766 `/api/cosmology/health` ou `/api/cosmology/status` |
| cosmos_evaluate | POST `/api/cosmology/evaluate` com os sete campos cosmológicos abaixo |
| cosmos_scenarios / cosmos_scenario | GET `/api/cosmology/scenarios` ou `/api/cosmology/scenarios/<UUID4>` |
| cosmos_save_scenario | POST `/api/cosmology/scenarios` `{"label":"nome","parameters":{...sete campos...}}` |
| cosmos_export | POST `/api/cosmology/exports` `{"scenario_id":"<UUID4>"}` OU `{"reference_parameters":{...},"current_parameters":{...}}` |
| cosmos_get_export | GET `/api/cosmology/exports/<UUID4>` |

Campos cosmológicos efetivos: `model_id="FLAT_MATTER_CPL_BACKGROUND",H0=67.4,omega_m=0.315,rd_mpc=147.09,w0=-1.0,wa=0.0,redshift=0.5`. Alternativas model_id: `TGL_V3_TOTAL_FIXED_BETA`, `V3_TOTAL_BETA_ZERO`; ambas exigem w0=-1 e wa=0. Faixas: H0 40..100; omega_m .1...5; rd 120..170; w0 -1.5..-.5; wa -1..1; z .001..3.

Queries de listas aceitam parâmetros LOCAIS `offset=0,page_size=50` (máximo 500), omitidos no HTTP. Retorno `{items,offset,page_size,total_available,next_offset,has_more,upstream_limit,metadata,coverage}`. Servidor já limita runs=40, inquiries=20, relations≤100, catalog≤3000; a paginação não recupera truncamentos prévios. A lista cosmológica não tem paginação HTTP; excesso do teto de resposta falha visivelmente.

## Classificação, normalização e proveniência

Contrato público: `catalog(section='overview')`, `normalize(operation,parameters)->dict`, `request(operation,parameters)->JSON`, `provenance(operation,params)->dict`, `writes(operation)->bool`.

`writes=True`: identity_chain, dephasing, inquiry, universe_load, universe_model, universe_event_view, cosmos_evaluate, cosmos_save_scenario, cosmos_export; conservadoramente também universe_event e cosmos_status, que podem inicializar caches internos. Toda computação passa por plano/run. Demais operações são inspeção, incluindo amostragem limitada. Nenhuma liberação RAM é exposta; `/api/universe/release` existe no servidor mas não integra a allowlist.

Normalização materializa defaults, números finitos canônicos (int/float equivalentes e -0/0), trims efetivos, campos desconhecidos recusados, UUID4 canônico e ID de catálogo 24hex. Para C6 lê apenas `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\REGISTRO_C6.json`: janelas registradas, massa/redshift de referência; reading e coeficientes H1/L1 sempre explícitos. Não cria registros nem chama API.

Proveniência calcula SHA256 real por bytes dos executores e insumos selecionados; não importa fontes, não chama status cosmológico, não inclui RSS/PID/elapsed/data_reads/data de coleta no fingerprint. GW usa GET status passivo, load_id/generation e hash da lista ordenada dos metadados estáveis/hashes dos arrays. Hash do strain não equivale a hash independente de todas as máscaras; source_sha256 pode ser null em fontes não fixadas. Arquivos selecionados por ID são revalidados na allowlist antes de hash integral, sem seguir symlinks/junctions. Hash integral de dado grande tem custo de I/O.

**Lacuna de API:** `/api/cosmology/status` inicializa o cache DESI se vazio. `/health` atual retorna apenas `{service:"tgl-cosmology-resident-v1",status:"RUNNING"}`. Portanto proveniência usa health sem efeitos + pins dos dados/executores; load_id fica desconhecido se health não o informar em `memory.load_id`. Para congelar geração RAM cosmológica rigorosamente, adicionar metadados passivos ao health; nunca fingir verificação com o ID informado na conversa. Hash em disco também não atesta código Python já importado pelo servidor; a implantação deve amarrar geração carregada.

Metadados mínimos do plano: operation, parâmetros normalizados, versão do adaptador, pins de executores, pins dos dados, load_id/generation e identidade de arrays quando pertinentes, estatuto/escopo, identidade autenticada do operador. `planned_at`/`dispatched_at` ficam no journal, fora do fingerprint. Comparar proveniência novamente ANTES de marcar DISPATCHING. A API não oferece precondição atômica de geração: operação externa concorrente entre consulta e dispatch é uma janela residual a registrar; conferir recibo final também.

Erros levantam `BenchError(code,message,uncertain)`, mensagem PT-BR sem conteúdo de exceção/segredo. Não há retorno falso de sucesso. Timeout, desconexão e resposta inválida após POST são incertos; jamais repetir automaticamente. Falta de serviço não aciona launch/restart. Carga READY completa preservada; LOADING/PARTIAL/RELEASING não são refeitos. Autorização de luiz/classe operador, orçamento, consentimentos, mutex global, journal e mapa universal pertencem ao integrador autenticado.

## Correspondência histórica (não equivalência presumida)

`runs.operation=identity_chain|dephasing`: remover só `parameters.operation`, normalizar restantes. **runs.source_sha256 = SHA256 de `APP_ESTRUTURA_V368_20260919\estrutura_v368.json`.** Não é Atlas. `result.engine_sha256` = app.py; `result.atlas_sha256` = TGL_ATLAS.md. Os três pins devem corresponder; histórico incompleto permanece leitura, não dedupe de execução.

`inquiries` → inquiry, campos completos do result; `scenarios` → cosmos_save_scenario: label + evaluation.parameters + evaluation.model.id; exigir proveniência histórica compatível (engine/components/data hashes), não só label/modelo. `exports.kind=scenario|comparison` → cosmos_export com cenário ou ambos conjuntos; `resident_runs` → universe_load, sem reativação automática. Datas e números locais de linha/registro não substituem identidade de entrada/geração. Constante `HISTORICAL_MAPPING` documenta as correspondências.

## Limites científicos e testes seguros

GW: carga min(50% RAM disponível Windows,96 GiB), reserva adicional WSL de 2 GiB; somente arrays próprios NumPy imutáveis, não memmap/pinned. View bins16..4096. Model duration (0,100], massa1..1e10, spin[0,1), z≥0; C6 massa≤1e4, cinco janelas registradas e máscaras DQ/injeção. Um evento, calibração não marginalizada, parâmetros manuais: NÃO é ajuste C6, p-valor, sigma nem movimento de gate. Cosmos: 13 observações, covariância completa13x13, curvas121pontos; V3 é fundo condicional, não CMB completo. Protocolos históricos não têm replay conectado.

Testes offline previstos/implementados no arquivo próprio: import/catalog sem I/O; defaults omitidos=explícitos e normalização repetida; rejeição de tipos/bools/NaN/Infinity/rotas/paths/UUIDs/campos; envelopes exatos; origem loopback fixa sem proxy/cookies/redirect; erro e resposta perdida sem retry; paginação honesta; READY sem POST; carga parcial preservada; worker ausente sem iniciar; proveniência ignora RSS/tempo mas detecta geração/pins; hash real de fixtures; links/caminhos privados recusados. Resultados executados serão registrados no manifesto final. Nenhum teste de renderização, experimento físico ou chamada paga faz parte desta entrega.

## Adendo — carga RAM assíncrona (02/10/2026)

`universe_load` significa iniciar/observar carga, não concluir experimento. O POST pode retornar `LOADING` com `domain`, `load_id` UUID4, `generation` inteiro positivo, `loaded_files`, `total_files`, `errors` e demais metadados. O adaptador verifica que o domínio REAL do retorno é o `gw_strain` normalizado; preserva o status e acrescenta `requested_domain`, `dispatched=true`, `load_complete=false` enquanto não estiver READY completo. Recibo incompatível após POST levanta `BenchError(code=INVALID_LOAD_RECEIPT,uncertain=true)`; jamais repetir.

A geração aumenta no início da carga. O main fixa **load_id + generation do retorno do POST**, e não a geração anterior do plano. Faz apenas GET via `request('universe_status',{})` até `READY` do mesmo par, domínio idêntico, total_files>0, loaded_files==total_files e errors==[]. Só então conclui. `PARTIAL`/`FAILED` preservam recibo e erros: não são resposta normal nem autorização de reenvio. `RELEASING`/`IDLE` ou troca de identidade indicam interrupção/substituição, não conclusão. Falha de rede conserva o acompanhamento pendente/incerto sem novo POST. O adaptador não faz polling.

`ALREADY_RESIDENT` retorna sem POST, com `dispatched=false`, `load_complete=true`, domínio/identidade/contagens validados. Deve ser registrado como reutilização da residência existente, não nova carga. A consulta de status agora preserva `FAILED` como estado de domínio; outras rotas continuam recusando falha genérica. Nenhum estado real de RAM foi alterado nesta correção.
