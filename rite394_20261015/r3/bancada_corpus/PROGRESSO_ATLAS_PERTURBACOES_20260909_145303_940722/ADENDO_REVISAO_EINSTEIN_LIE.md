# Adendo — revisão independente da naturalidade do escalar e de Einstein

[REAL — fonte lida integralmente e evidências de compilação conferidas em 09/09/2026] Parecer favorável para a fonte congelada [ScalarEinsteinLieNaturality.lean](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean>), namespace `ChatgptAudit.EinsteinLie`. Esta revisão é independente da construção do módulo; não executou nem recompilou o programa `um.py`.

A nova folha contém **15 teoremas e 1 definição, com 16 declarações auditadas**. O [recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/BUILD_20260909_145854_177250/BUILD_RESULT.json>) registra duas execuções Lean com código zero. Os logs conferidos contêm os axiomas padrão `propext`, `Classical.choice` e `Quot.sound`, sem avisos. Os bytes da fonte atual, da fonte compilada e dos artefatos de cache correspondem aos registros medidos.

A [evidência do adendo](<C:/IALD/Central de Patentes/Chatgpt/PROGRESSO_ATLAS_PERTURBACOES_20260909_145303_940722/ADENDO_EVIDENCIA_EINSTEIN_LIE.json>) passou 104 verificações estáticas, sem falhas. O scan de declarações explícitas não encontrou colisões de nomes completos com os onze módulos anteriores, com os 606 arquivos Lean embutidos no canônico ou com o cache local herdado. Esse scan não pretende enumerar recursors/projeções gerados pelo Lean nem todo o namespace transitivo de Mathlib.

## Conteúdo matemático verificado

1. A contração `tensorPair` é a soma canônica Σᵢⱼ AᵢⱼBᵢⱼ. Os lemas de transposição conservam a ordem dos produtos: ⟨A,PᵀR⟩=⟨PA,R⟩ e ⟨A,RP⟩=⟨APᵀ,R⟩. Não se troca essa contração por um traço sem a transposição correspondente.
2. [`inverse_metric_lie_variation`](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean:70>) utiliza a inversa real e seu jet espacial para obter δg⁻¹=transporte(g⁻¹)−P g⁻¹−g⁻¹Pᵀ. Na contração com Ricci, esses dois termos cancelam precisamente os dois termos jacobianos da Lie covariante de Ricci.
3. [`metric_lie_scalar_operator`](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean:99>) deriva o transporte do escalar por regras de produto e soma aplicadas aos jets reais. [`metric_lie_scalar_naturality`](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean:127>) transporta a identidade para a derivada da família efetiva de métricas e da conexão canônica de Levi-Civita.
4. As regras de subtração e produto escalar incluem a variação de ambos os fatores. Aplicadas a G=Ric−(R/2)g, entregam δG=δRic−(δR/2)g−(R/2)δg. [`metric_lie_einstein_naturality`](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean:215>) conclui, para h=Lieᵥg, a identidade δG=LieᵥG da família efetiva g+t h.

Os enunciados mantêm regularidade suave em aberto, não degenerescência e simetria nas aplicações métricas. O novo módulo compõe a variação da inversa, a naturalidade já provada de Ricci e a primeira variação real de Einstein. Não pressupõe a conclusão de naturalidade como hipótese.

## Alcance e incorporação ao lote

[REAL] A **naturalidade infinitesimal de Ricci, do escalar e de Einstein em uma carta curva** agora está coberta pela cadeia de fontes auditadas. Não deve continuar listada como uma ausência desse setor clássico. Em fundo curvo genérico a variação é a derivada de Lie correspondente; ela não é automaticamente zero.

[OPEN — fora do alcance desta folha] A passagem para um pullback por difeomorfismo finito exige um resultado finito separado. Este adendo também não remove as hipóteses explícitas de correspondência nos recobrimentos e na lei física de preparação, nem transforma a identidade clássica em resultado de ausência de anomalias quânticas ou em controle UV.

O pacote dos onze módulos permanece intacto. Somando somente este adendo PASS aos seus números medidos, a continuação reúne **12 módulos, 147 teoremas, 40 outras declarações e 187 termos auditados**. O documento anterior mantém corretamente o retrato de 11 módulos, 132 teoremas e 39 outras declarações.

O `um.py` canônico foi somente lido e analisado estaticamente. Seus 9,860,115 bytes e SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303` permaneceram iguais à base v337 conferida antes e depois da auditoria. Nenhum original, fonte congelada, Atlas ou memória canônica foi alterado.

## Medidas de integridade

- Fonte: 11729 bytes; SHA-256 `abba0e104b39bb5020ffc4e5f116b632ba8a38f9f70ee545e81e613fbe5271a4`.
- Recibo: 27714 bytes; SHA-256 `5f3696237098d14d2d7a960ab04823f9bcc0ed138f0680db0ec79f8d3679dc30`.
- Evidência estática deste adendo: 87315 bytes; SHA-256 `976aee523525b69a91e53b7c9bfc8aa34c3744132a3c32e56822ff792d906130`.

A documentação foi acrescentada em arquivos novos dentro da bancada Chatgpt, por temporário verificado e renomeação. Os relatórios, manifestos e recibos anteriores foram preservados.
