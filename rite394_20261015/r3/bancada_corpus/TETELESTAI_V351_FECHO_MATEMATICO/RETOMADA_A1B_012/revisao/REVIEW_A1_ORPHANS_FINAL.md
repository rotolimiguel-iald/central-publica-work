# A1 — revisão e reprodução dos sete módulos órfãos

2026-09-14T18:53:09.513088-03:00 · **A1_ORPHANS_REVIEW**

[REAL] **Reprodução computacional dos sete aceita; cinco módulos de escala revisados sem P0–P2 encontrados.** Os dois antiunitários recebem minha conferência/reprodução e inspeção semântica independente do principal, pinada separadamente; preserva-se a autoria anterior deste sidecar. Sete fontes existentes, **40 declarações = 36 teoremas + quatro definições**, zero novos teoremas. Lake próprio rc0, quarenta `#check` com universos e mapas de axiomas próprios completos, apenas subconjuntos de `propext`, `Classical.choice`, `Quot.sound`. **A1(b) permanece OPEN.**

**Ressalva de independência:** os dois módulos antiunitários tiveram autoria deste sidecar na manhã, conforme relatório histórico preservado. Esta rodada é independente em árvore, objetos e execução, com releitura adversarial; não constitui independência pessoal retrospectiva sobre a própria autoria. A auditoria histórica autoral não foi rebatizada como aprovação independente. A inspeção independente posterior do principal foi lida integralmente e seus 16 alvos/fontes conferidos: INSPECAO_PRINCIPAL_ANTIUNITARIOS.md/json. Ela não aponta P0–P2 e fica pinada separadamente. Assim se distinguem autoria anterior, nova reprodução e inspeção independente, sem atribuir a esta auto-releitura uma independência pessoal inexistente.

## Resultado matemático que foi conferido

1. **Entrelaçamento CFC:** a união compacta dos dois espectros permite indução para funções complexas contínuas. A etapa de conjugação usa auto-adjunção de ambos. Para U(T)R=RU(Q), T,Q são contrações positivas e ambos os extremos são injetivos. R é somente limitado, sem inversibilidade.
2. **Escala:** para r>0, D_r(x)=r+(1−r)x é positivo em [0,1]. F_r(x)=x/D_r(x), e_r(x)=r/D_r(x)²; as identidades de complemento, amortecimento e fase tratam as pontas separadamente. Não se supõe continuidade através de polos fora do espectro. A fase é **exp(+it log r)**.
3. **Cálculo funcional e cancelamento:** E_r=e_r(T) é unidade limitada por CFC, B_Q=B_T E_r e C_Q=exp(it log r) C_T E_r. A sobrejetividade de E_r dá densidade de Ran B_Q; a igualdade se estende por continuidade. **Não se inverte B_T=T(1−T)** nem o operador de entrelaçamento; não há gap novo.
4. **Aplicação concreta:** os dois resultados de transporte usam o MESMO `scalarTomitaResolvent`, `scalarTomitaImaginaryPower`, `ScalarGNSHilbert P`, `matrixUnitRightData` e `regularRightGNS`. Positividade, injetividades, r=localEigenvalue>0 e TR=RQ_r são descarregados por fornecedores reais. Os resultados valem para todos os vetores do Hilbert, sem uma premissa de domínio escondida.
5. **Antiunitariedade:** a conjugação é homomorfismo de *-álgebras **sobre ℝ**, conjugando escalares complexos. CFC real e decomposição real/imaginária provam `star(g_t(1−x))=g_t(x)`. Os dois sinais se cancelam: **JU_tJ⁻¹=U_t**, não U_−t. Na camada genérica J²=I não é hipótese necessária. A especialização consome o flip do **J polar original**, sem substituí-lo pelo J da torre ou por unidade gaussiana. A igualdade final é de operadores limitados complexos, além da igualdade pontual.

Esses são fornecedores efetivos para `regular_dual_weight_modular_implementation`, não sua conclusão inteira. Falta o consumo da ação à esquerda em toda a álgebra conforme o contrato; comutação/escala pela direita e invariância por J não são, isoladamente, KMS. Os sete não produzem gerador regular positivo h, perturbação pelo inverso, traço, nem habitante de `TGLV351.RegularCoreTraceData`.

## Fontes, ficha e histórico

`RECIBO_B6` e seus pins de entrega/manifesto foram conferidos **antes de escrever/preparar** esta reprodução. Ficha MD/JSON e ALVOS atuais foram lidos, seus tipos/linhas/pins confrontados com as sete fontes. Os **19 V351** coincidem com o snapshot V353, inclusive os sete. A retomada reutiliza fichas/buscas anteriores e não anuncia busca exaustiva nova.

Os 16 registros históricos pertinentes foram lidos e pinados: 7 rc0 com fonte final e **9 rc1 excluídos**, inclusive saídas parciais. Seus axiomas rc0 coincidem com os próprios. Isso é histórico autoral distinto do novo Lake; falhas de ambiente/elaboração não são prova matemática nem adulteração válida. Nenhum teste negativo extra foi criado para esta reprodução de fontes imutáveis.

## Reprodução isolada

Projeto `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v`; saída `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao`. Comando próprio: `lake build` dos sete módulos e `TGLExt.ReviewA1Orphans`. **469 fontes de projeto** copiadas em bytes da árvore antiga por fecho de imports; **470 objetos próprios** construídos incluindo o auditor. Nenhum .olean TGL/TGLExt autoral ou de V353 foi herdado. Toolchain Lean 4.31.0, configurações iguais às pinadas; LEAN_PATH verificado nas traces dentro de v.

Mathlib e oito pacotes auxiliares foram copiados **em bytes, sem hardlinks**, do cache privado anterior em V353/s. Cada arquivo foi lido, copiado e comparado, com manifestos próprios de SHA256. São **objetos de pacotes herdados**, não recompilação independente da biblioteca. O inventário dos 121.039 arquivos de pacotes não contém objetos TGL/TGLExt; a checagem está pinada em compilation.json. A raiz curta foi conferida antes da cópia; não houve escrita em V353. Relatórios/fontes antigos A1 e pins B1–B6 permaneceram inalterados.

Nenhum aviso nos sete módulos e no auditor próprio. Os **178 avisos de fornecedores existentes** permanecem nas traces/JSON e não foram suprimidos pela revisão. Total de jobs Lake inclui cache, não equivale a número de novas provas.

Diferenças de .olean medidas (sem forçar identidade): TGLExt.V351ResolventImaginaryIntertwining, TGLExt.V351ScaledResolventFunctions, TGLExt.V351ScaledResolventCalculus, TGLExt.V351ImaginaryPowerScaling, TGLExt.V351ScalarImaginaryRightTransport, TGLExt.V351AntiunitaryResolventPhase, TGLExt.V351ScalarTomitaImaginaryConjugation. Os pins de ambas as origens e os booleanos por comparação estão no JSON; nenhuma troca de objetos ou nova compilação foi usada para fazê-los coincidir.

Os sete objetos autorais antigos em OLD/build e os sete da reprodução autoral nova em k foram lidos para comparação; o run autoral rc0 e seus streams/pins também foram conferidos. Seus quarenta axiomas coincidem com os próprios. Nenhum objeto autoral foi usado no meu build. Os sete caminhos .olean de V353/kernel/.lake/build/lib/lean não existem (FileNotFoundError/Windows 2, confirmado com leitura elevada); a igualdade com V353 refere-se às fontes, e a comparação binária indisponível fica como null, não como igualdade ou divergência. Nenhum objeto foi buscado ou copiado para preencher essa ausência.

## Pins finais e evidência

| Módulo existente | Declarações | SHA256 fonte | SHA256 .olean próprio |
|---|---:|---|---|
| V351ResolventImaginaryIntertwining | 4 | `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5` | `22b5b4b8921934abd4decf15ac29777e87ba61192153a97d836b6a40b3de4c85` |
| V351ScaledResolventFunctions | 7 | `1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb` | `1c97ae11718afcf3a737f9ae252bc7b484d18000442293cdda8ed50afb404956` |
| V351ScaledResolventCalculus | 9 | `89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32` | `6a1c8d78ac795b7725d09e3f550660e2e68ffcbaececc41692e473fe30847866` |
| V351ImaginaryPowerScaling | 2 | `fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69` | `86f7045252bbcb0d28b87074362c4d08f158db72791ac4b67ea2a4e4142a7be5` |
| V351ScalarImaginaryRightTransport | 2 | `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349` | `2edd544ed663d54c1b16a4db7776dde48f103e228e6fc4dfd5ba8df4684a0037` |
| V351AntiunitaryResolventPhase | 13 | `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8` | `f2788c22f86fec05bb06db0c0ef2ae3f52b33c151be11fdc356641660312b973` |
| V351ScalarTomitaImaginaryConjugation | 3 | `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d` | `e251343e535ffd4a374d2bff1e1dece2746c11ae372cec141ae5c79e1c8c183a` |

- [Parecer JSON](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/REVIEW_A1_ORPHANS_FINAL.json>) — `6be3a9c9c11a5254eb150c4b2160c035719ddbcf691f12ee29141f18ffb87c55`.
- [Compilação](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/compilation.json>) — `2c0b7e73520a255c0b4d8055b9339b4f0765c00d9eafcd7fa5309d2f9031b3a5`.
- [Run próprio](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/run.json>) — `1ca860d7d399dda0a5476acb9d2307a92a195092cab75453c3a8e6409ab3062b`.
- [Snapshot](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/source_snapshot.json>), [inspeção final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/final_inspection.json>) e [cache](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/cache_provenance.json>) e [inspeção separada do principal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/principal_inspection_read.json>) e [replay autoral relido](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/author_cold_replay_read.json>).

**Execução deste escopo encerrada.** A reprodução está concluída; a inspeção semântica por agente distinto dos dois antiunitários provém do documento do principal, não desta auto-releitura. Sem novo teorema-alvo, monólito, integração, entrega pelo túnel, alteração de gate/memória ou início de módulo posterior. O aceite é da reprodução e do significado limitado desses fornecedores; não quita A1(b).
