# Consulta — cortes do mesmo h por escala dual

[DERIVED — consulta, não novo Lean] A proposta do agente principal é correta para ε>0 e é mais econômica, nesta etapa, que reconstruir o corte por uma função racional no CFC. Fixe h=regularPositiveGenerator P, R=regularSpectralResolvent P, C_s=characterMultiplier s e θ_s=dualAmbient s. O delta7 prova hC_s=e^s C_sh em domínio completo, equivalentemente Ad(C_s)h=e^(−s)h.

Defina Bε=ε⁻¹ θ_(log ε)(R). Como θ preserva a álgebra N e 0≤R≤I, obtém-se Bε∈N e 0≤Bε≤ε⁻¹I; logo Bε é limitado, com norma ≤ε⁻¹. Não é preciso supor h com inversa limitada, gap ou domínio total, nem CompleteSpace do subtipo N. A positividade é a ordem usual dos operadores no Hilbert.

Prova exata de que este operador é (h+ε)⁻¹, sem usar esse nome como hipótese: dado u, ponha t=log ε e z=C_(-t)u. A equação já compilada do resolvente dá (Rz,z−Rz)∈graph(h). Transporte por C_t, usando exp(log ε)=ε, e divida AS DUAS componentes por ε. Resulta

    (Bεu, u−εBεu) ∈ graph(h).

Assim (h+ε)Bε=I, com Bεu no domínio efetivo. Para a recíproca, h+ε é injetivo: se hx+εx=0, a positividade de h dá 0≤Re⟨x,hx⟩=−ε‖x‖², portanto x=0. Essa unicidade implica Bε(hx+εx)=x para TODO x∈D(h). Paga-se a igualdade do grafo do inverso, não apenas uma identidade em um núcleo denso.

A composição da ação dual fornece diretamente

    θ_s(Bε)=ε⁻¹θ_(s+log ε)(R)=e^s B_(εe^s).

Os sinais estão coerentes: h escala por e^(−s), o inverso regularizado por e^s e o parâmetro por εe^s. A identidade exige ε>0; não se pode aplicar exp(log ε)=ε em ε=0. No código, dualAmbient_add usa StarAlgEquiv.trans, cuja ordem de avaliação deve ser respeitada; a soma real permite trocar s e log ε sem assumir comutação arbitrária de operadores.

[DERIVED — próximo consumidor] A família de cortes pode, portanto, ser construída agora usando apenas escala dual, ordem e o resolvente existente. Para compará-los, a equação dos inversos também dá Bε−Bδ=(δ−ε)BεBδ e comutação dos dois cortes; para 0<ε≤δ isso dá Bδ≤Bε. São lemas algébricos de resolvente ainda a formalizar, não novos objetos espectrais.

[OPEN — limite PT] Isto constrói os cortes limitados e sua escala. Não demonstra a ordem de ν(Bε^(1/2) A Bε^(1/2)) para todo A≥0 apenas pela ordem Bδ≤Bε: sanduíches não preservam essa comparação não comutativa. Continua necessária a lei específica de perturbação no centralizador (ou prova direta equivalente), a definição/limite do peso perturbado e a tracialidade. A raiz limitada, se usada, reaproveita a infraestrutura existente; não precisa ser reconstruída para provar o corte. Não se cobra novamente semifinitude de ν por minorantes positivos. A consulta anterior sobre PT permanece distinta e não foi editada.

[REAL — limites de execução] Somente leitura de fornecedores e escrita desta nota/JSON; nenhum novo Lean, build, objeto, memória ou alteração de parecer selado. Esta consulta não agrega alvos ao aceite separado da escala dual7.

Fornecedores relidos e pins medidos:

- `regularPositiveGenerator_dual_scaling` — [V351RegularGeneratorDualScaling.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularGeneratorDualScaling.lean:124>) — SHA256 `2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50`.
- `regularDualAction` — [V350RegularDualAction.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularDualAction.lean:76>) — SHA256 `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`.
- `dualAmbient_add` — [V350RegularDualAction.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularDualAction.lean:30>) — SHA256 `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`.
- `regularDualAction_apply` — [V350RegularDualAction.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350RegularDualAction.lean:83>) — SHA256 `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`.
- `resolvent_graph_resolvent_equation` — [V350ResolventGraph.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V350ResolventGraph.lean:89>) — SHA256 `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`.
- `regularSpectralResolvent_nonneg` — [V351RegularPositiveGraph.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularPositiveGraph.lean:84>) — SHA256 `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`.
- `regularSpectralResolvent_le_one` — [V351RegularPositiveGraph.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularPositiveGraph.lean:89>) — SHA256 `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`.
- `regularSpectralResolvent_mem` — [V351RegularGeneratorAffiliation.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\TGLExt\V351RegularGeneratorAffiliation.lean:32>) — SHA256 `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`.

Data: 2026-09-14T20:11:14.163535-03:00.
