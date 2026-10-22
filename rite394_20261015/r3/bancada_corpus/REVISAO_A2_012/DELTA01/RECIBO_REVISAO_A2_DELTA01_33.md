# Recibo aditivo de revisão independente — A2 Delta01, lote 33

**[REAL — medido nesta revisão] DELTA01_VERIFICADO__33_PRESERVADOS__P2_01_QUITADO. P0=0; P1=0; P2=0 neste delta. P2-01: QUITADO.**

**Carver — agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`**, convocado pelo agente principal no escopo autorizado; revisor independente, não autor. Identidade fornecida pela principal [INPUT], registrada também no JSON. Nenhum outro usuário é apresentado como aprovador.

O recibo de 35 nomes permanece intacto em [RECIBO_REVISAO_A2.md](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/RECIBO_REVISAO_A2.md>), incluindo o P2 histórico. Este recibo acrescenta o resultado do delta de poda; não substitui nem reescreve a história. Escrita desta rodada exclusivamente em `C:\IALD\Central de Patentes\Chatgpt\REVISAO_A2_012\DELTA01`.

Foram removidas exatamente as declarações `scalarTrace_finite_positive_seed` e `scalarTrace_finite_projection_exists`, seus dois `#print axioms` nos módulos e os dois nomes no Audit ativo. A comparação com as cópias seladas de 35 nomes confirmou igualdade byte a byte após somente essas exclusões. Os seis outros V354 não mudaram. Os backups autorais correspondem aos bytes anteriores.

O conjunto público atual contém exatamente os 33 nomes anteriores menos os dois removidos. Os enunciados e corpos de prova restantes foram preservados, sem consumidor artificial. Os dois auxiliares gerais usados pela cadeia em e11 continuam presentes. Os módulos que os fornecem continuam necessários.

Diffs verificáveis: [V354FiniteTraceSupport.diff](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/diffs/V354FiniteTraceSupport.diff>), [V354SpectralThreshold.diff](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/diffs/V354SpectralThreshold.diff>) e [AuditA2RegularSupport.diff](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/diffs/AuditA2RegularSupport.diff>). Comparação e grafo: [DELTA_COMPARISON.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/DELTA_COMPARISON.json>).

Compilador medido: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`. Executável: `C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe`; 83456 bytes; SHA-256 `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`.

A remoção afeta transitivamente os oito V354. Todos os oito foram recompilados de fontes próprios com rc0, sem objetos V354 antigos no ambiente. Também compilaram com rc0 o Audit autoral copiado e o Audit independente que enumera todos os 33 nomes. São oito módulos matemáticos e dois auditores; não se conta o cache como compilação.

Ambos os auditores imprimiram os 33 nomes, sem ausentes, duplicados ou axiomas fora de `{propext, Classical.choice, Quot.sound}`. A fonte própria `RemovedNamesAbsent.lean` teve as duas consultas recusadas por nome desconhecido no ambiente recém-compilado. Essas recusas comprovam ausência das declarações; não são provas matemáticas nem falhas de importação.

Evidência completa de execução: [BUILD_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/BUILD_DELTA01.json>); axiomas e gates: [AUDITORIA_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/AUDITORIA_DELTA01.json>). Cada execução registra comando, raiz, fonte, objeto, rc, tempo e logs com SHA-256 e bytes.

CoreSupport não mudou: reutilizou-se o objeto compilado independentemente na revisão de 35 nomes, após conferir fonte e objeto. As dependências A1 aceitas e esse objeto totalizam 1367 hardlinks usados somente para leitura. Mathlib foi cache. Nenhum A1 ou CoreSupport foi recompilado nesta rodada, nenhum objeto emprestado foi sobrescrito. A integridade pós-build foi medida em [INTEGRIDADE_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/INTEGRIDADE_DELTA01.json>).

Os controles semânticos próprios da revisão de 35 nomes permanecem preservados e não foram alterados nem reexecutados. O delta não altera hipótese, enunciado ou prova restante; os testes desta rodada limitam-se à exclusão exata, recompilação dos dependentes, cobertura completa de axiomas e ausência efetiva dos nomes removidos.

O alcance matemático do recibo anterior permanece: suporte não nulo, traço A1 igual a um, split igual e ortogonal, projeção do kernel de 1−PF igual a PF, gap um no complemento do kernel e afiliação do representante mínimo. CCW usa o reader que coincide com A1 em todos os positivos; sua extensão por zero fora do cone continua não cíclica e não fornece o traço total legado.

**Não é aceite integral de A2/ORDEM011 nem do adendo.** O totalizador Core→ENNReal com as leis antigas permanece [OPEN]; ThreeLocksCoreData e FullWitness não estão certificados como construídos. W/D têm os fornecedores já documentados no recibo anterior. A principal informa [DECLARADO] que SusyRelativeData reticular ainda não foi instanciado no mesmo core; este delta não certifica essa realização e não a substitui por modelSusy ENNReal. Não houve integração canônica.

Os metadados abaixo são dos arquivos autorais efetivamente lidos e copiados; os caminhos das cópias e seus hashes constam do manifesto e do JSON. A aprovação deste delta é calculada dos gates, sem usar o resultado autoral como prova.

| Arquivo autoral lido | Bytes | SHA-256 |
|---|---:|---|
| [DELTA01_PODA.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/DELTA01_PODA.json>) | 3281 | `f47119ec2efacb17475450cdc3ae801282f793a7062b502d0eb34175b6a54ac9` |
| [AUDIT_NAMES_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/AUDIT_NAMES_DELTA01.json>) | 5375 | `83aefa5ef0fd4646d039801f4a9af423fe306f17be42ad2bc32a34365a46f9ec` |
| [V354FiniteTraceSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354FiniteTraceSupport.lean>) | 1897 | `7edd9fb4ef524e95b8c71d71bb7467512f9b89f7b04c21a5114686e894b1d323` |
| [V354SpectralThreshold.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354SpectralThreshold.lean>) | 6267 | `9c33191344d07e4947a6d78a23ca0fc17e6b75206c13c511219f3a7a3b65085d` |
| [V354RegularMatrixCorner.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354RegularMatrixCorner.lean>) | 2641 | `1f469df09c8ce12c58d7c8388dbedadb3fc9336a9c97757113693e7322e596f9` |
| [V354FiniteEqualSplit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354FiniteEqualSplit.lean>) | 3193 | `72876fa3cf13dbd947ab02f1f4bd378c8d0dc7b2ed9beb39d98d7bed8079552e` |
| [V354NormalizedSplit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354NormalizedSplit.lean>) | 2452 | `5e90a1c08de4dc4593e65d9b8dde4a4bd5a1e074b68f8be357d17d25bbebe91a` |
| [V354RegularSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354RegularSupport.lean>) | 6756 | `c80d99c73be4a676bcdc8cc21d476c249911d08f93fd914fda0d788019b1063e` |
| [V354PositiveTraceReader.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354PositiveTraceReader.lean>) | 4075 | `8133d88dcaf9ac3d58d739ecaf997312d7951be2c11fe1d08f21c8f90badf3ea` |
| [V354TraceReaderWall.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354TraceReaderWall.lean>) | 2630 | `7882c9df649971790dfa9545e802df5b2b4e31c8bc16d536cecfd4d64203efcc` |
| [AuditA2RegularSupport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/AuditA2RegularSupport.lean>) | 2010 | `c35005716ff0a7c1186671aea32503466a306f37ba86d7c02b301b8c8b9290b3` |


| Módulo recompilado nesta revisão | rc | Segundos |
|---|---:|---:|
| TGLExt.V354FiniteTraceSupport | 0 | 16.70 |
| TGLExt.V354SpectralThreshold | 0 | 30.58 |
| TGLExt.V354RegularMatrixCorner | 0 | 17.94 |
| TGLExt.V354FiniteEqualSplit | 0 | 19.19 |
| TGLExt.V354NormalizedSplit | 0 | 19.56 |
| TGLExt.V354RegularSupport | 0 | 18.33 |
| TGLExt.V354PositiveTraceReader | 0 | 17.98 |
| TGLExt.V354TraceReaderWall | 0 | 21.63 |


Recibo e selo de 35 nomes preservados: [RECIBO_REVISAO_A2.md](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/RECIBO_REVISAO_A2.md>) e [SELO_A2.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/SELO_A2.json>). Recibo de 33 nomes, evidência nova e cópias são indexados por [MANIFESTO_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/MANIFESTO_DELTA01.json>) e [SELO_DELTA01.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/DELTA01/SELO_DELTA01.json>).
