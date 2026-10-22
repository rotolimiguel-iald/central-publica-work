# Sucessor da cópia 93 — preparação sem confirmação

[REAL — leitura estática] A base desta preparação é `COPIA_INTEGRADA_20260909_203352_868028/um.py`. A compilação conjunta anterior está em `INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415/BUILD_SUCCESSOR_20260909_203414_443930/TRANSPOSED_RESULT.json`, com PASS. A auditoria anterior é a versão 2 de `AUDITORIA_INTEGRACAO_93_V2_20260909_203946_6451878`, também PASS. Seus pins foram lidos dos arquivos.

Os três utilitários `integrate_approved_copy.py`, `prepare_successor.py` e `run_successor.py` são cópias exatas dos utilitários anteriores. A proveniência está em `PROVENIENCIA_UTILITARIOS_93.json`. Nenhum deles foi executado nesta preparação.

`CONFIG_94_NAO_CONFIRMADA.json` contém apenas `SelectedProbabilitySigma`. `CONFIG_96_NAO_CONFIRMADA.json` contém também `SignedGibbsResponse` e `RenormalizedNegativeExpectation`. São snapshots novos com `root_confirmed:false`; a presença de recibos PASS não atribui aprovação semântica ou confirmação à tarefa principal.

O snapshot 96 tem delta de três módulos, 52 teoremas e 15 outras declarações; acumulado de 96 módulos, 1338 teoremas e 367 outras declarações, totalizando 1705 termos explícitos e 12 instâncias locais nomeadas. A folha `SignedGibbsCoverage` ainda depende do recibo final para gerar um snapshot 97 novo.

Para uma configuração confirmada em **arquivo novo**, as interfaces preservadas são:

1. `integrate_approved_copy.py CONFIG_CONFIRMADA_NOVA.json` — cria uma nova pasta de cópia.
2. `prepare_successor.py PASTA_DA_NOVA_COPIA BUILD_PLAN_ANTERIOR.json TRANSPOSED_RESULT_ANTERIOR.json` — os dois artefatos anteriores são os da sucessão 93 indicada no primeiro parágrafo.
3. `run_successor.py NOVO_BUILD_PLAN.json` — executa as folhas transpostas e agregadores.
4. Auditor correspondente ao snapshot, com argumentos `PASTA_DA_NOVA_COPIA PASTA_DESTA_PREPARACAO`, somente após PASS conjunto.

O preparador de configurações é `prepare_configuration_from93.py`. Aceita opcionalmente um JSON de referências extras, como `EXTRA_SOURCE_96.json`, e sempre cria inventário, configuração não confirmada e recibo novos.

O gerador válido de auditor é `prepare_auditor_from93_v2_fixed.py`. Ele recebe o inventário final e cria um auditor novo com proveniência. O arquivo sem o sufixo `_fixed` foi preservado após falhar visivelmente por tratar o inteiro `aggregate_processes` como lista; não gerou auditor ou pasta de saída. A correção exata está em `PROVENIENCIA_CORRECAO_GERADOR.json`.

A correção histórica da versão 2 foi mantida: no primeiro estágio, o auditor confere o snapshot original contra o tamanho/hash registrados na época. O canônico vivo é observado separadamente como diagnóstico e nunca usado como a base histórica. Etapas posteriores preservam as verificações estritas dos predecessores congelados. O gerador compara integralmente os quatro segmentos dessa correção e exige que preparação e resultado conjunto existam antes de um PASS.

Auditor 96 preparado, sem execução: `C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_INTEGRACAO_96_20260909_210653_224350/audit_integration_96.py`. Para ele, `FullTGLAudit` tem 5830 entradas e `NewModulesAudit` tem 1705. O snapshot 97, se criado, terá seu próprio auditor e suas contagens medidas.

[OPEN] Integração futura, compilação conjunta e auditoria futura não estão atestadas por estes arquivos de preparação. Não houve execução/importação de `um.py`, alteração de originais, novo selo ou mudança de gate nesta etapa.
