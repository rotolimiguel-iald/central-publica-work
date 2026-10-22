# Revisão DEV — adjunto polar e transporte de gráficos

2026-09-13T02:56:11-03:00 — **ESTRATO PARCIAL: somente ScalarTomitaAdjointPolar, 1 módulo/10 alvos.**

[REAL — leitura integral, recompilação independente e auditor próprio] **Nenhum achado P0, P1 ou P2 neste primeiro módulo.** A consulta matemática anterior não foi usada como prova. O segundo módulo `ScalarRightConjugateGraph` e o manifesto conjunto aguardam aviso de fonte final; não foram congelados, lidos ou compilados nesta rodada. **Sem veredito ou marcador final do pacote.**

Escopo semântico conferido, em `kernel/TGLV350/ScalarTomitaAdjointPolar.lean`:

- **Linhas14–39:** `D(F) = J⁻¹ D(B)` em ambas as direções. A ida aplica `generic_adjoint_maximal` ao B auto-adjunto efetivo; a volta aplica a maximalidade do F já existente. O teste é em todo D(B)/D(S), usando as inclusões já provadas. Nenhuma hipótese de domínio total, inversa limitada ou novo adjunto é acrescentada.
- **Linhas41–69:** os subtipos transportam Jy ao domínio correto, e `F y = B(Jy)` decorre do pareamento na convenção local ⟨Sx,y⟩=⟨Fy,x⟩ e da densidade de D(S). B continua `scalarTomitaPositiveRoot P` e J continua `scalarTomitaPolarFactor P`.
- **Linhas71–106:** `F=JSJ` e `S=JFJ` conservam os domínios originais, com a involutividade efetivamente herdada de J. As igualdades entre entradas de subtipo identificam os mesmos vetores, sem trocar representações.
- **Linhas108–125:** J×J envia exatamente graph S sobre graph F, nos dois sentidos. A surjetividade é explícita pelo domínio conjugado. Este enunciado ainda não é o transporte do fecho do core direito, que pertence ao segundo módulo.

A dependência `TGLExt/GenericAntilinearAdjoint.lean` foi relida integralmente. `generic_adjoint_pairing` (linha114) usa o adjunto formal derivado de auto-adjunção; `generic_adjoint_maximal` (linha126) usa **o adjunto máximo Mathlib**, sua pertinência de domínio e `LinearPMap.isSelfAdjoint_def`. A prova genérica recebe involutividade de J, mas a aplicação concreta fornece `scalarTomitaPolarFactor_involutive P`, já provada. Não foi encontrada circularidade: a identidade nova F=BJ não é premissa dos resultados anteriores sobre S†S, B ou J. Os tipos impressos deixam somente P e os vetores/domínios indicados; não surge hipótese residual.

| Evidência | Resultado |
|---|---|
| Recompilação própria do módulo | rc0, 35.079 s, sem warnings |
| Auditor próprio `#check` com universos e `#print axioms` | rc0, 23.457 s, exatamente10 alvos, sem warnings |
| Binário | Próprio = autoral, byte a byte |
| Dependências de projeto | 425 congeladas a partir de árvores próprias; não recompiladas |
| Pacotes externos | Oito caminhos readonly; 10 pins diretos herdados e reconferidos |
| LEAN_PATH | Build desta árvore + pacotes externos; nenhum build de projeto autoral |

Proveniência das árvores próprias reutilizadas:

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\revisao\scalar_tomita_involution_independent_20260912_133836_401235` — manifesto `9dbb68de2dab5cfc89696f343595f5b87f8ccf6c812b2c1669b3352bfcb25fc3`, compilação `c25abecd8c3e2725c0f45482e8418a7467c9687c1a0eb88f49340bb66627acfd`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\revisao\right_graph_core_final_independent_20260913_021030_429982` — manifesto `a2f37294ae27d87fdc2c06f443796f28eba2de8c412c64f93010e8cf54c913ed`, compilação `78637e6e327307332c385a8a50e8aa5cafe5971b80f94faed69ec278e0cb6c94`.

`GenericAntilinearAdjoint` veio da árvore própria da involução polar; seu registro de compilação anterior foi herdado, não é uma nova recompilação nesta rodada. Os pins de dependências e companions, fontes/binários autorais, log final/streams e artefatos readonly foram reconferidos ao terminar.

Pins lidos nesta reprodução:

- Fonte: `7893d1356e10fac1c62b7282c4e1e3b16e534de924fa6cd81e314e140e76c248`.
- Binário autoral e próprio: `cf8fdd58193bbf4b278477cca0fe55a0f669692234a23f65914996a86f588992`.
- Log final `ScalarTomitaAdjointPolar_20260913_024356_420864.json`: `6b1bd710f6e5c0f5168766deaa65a8b26b6e71c626d4257296236461b2a7551c`.
- Stdout autoral final: `75c490fe595241d399f3c3b2a2c57cbeaf4bb649a817c354e8726541efc564cc`.
- Manifesto próprio: `a4ade1ad0ad1e27885b789f177a9f7416b38904c092a309beec605677896fecf`.
- Compilação própria: `2538a2b9ca5579d0b493bec92a32803228703591c25743cfa147822f9aeabb67`.

Histórico: **1 tentativa autoral rc1 excluída**, log `ScalarTomitaAdjointPolar_20260913_024247_552418.json`. O timeout de isDefEq/whnf gerou prints vazios e referências a constantes/provas inválidas; nenhum foi aceito como evidência. O log final rc0 e o auditor próprio imprimem somente o trio. Houve também uma falha própria **de preparação, antes de executar Lean**, por catálogo sem `ScalarTomitaPolarInvolution`; preservada em `adjoint_polar_first_independent_20260913_025247_090820/preparation_failure.json`. A resolução foi adicionar a origem própria já revisada da involução, sem binários autorais nem rebuild de dependências.

Os dez alvos conferidos:

- `TGLV350.Regular.scalarTomitaAdjoint_polar_domain_iff`.
- `TGLV350.Regular.scalarTomitaAdjointRootInput`.
- `TGLV350.Regular.scalarTomitaAdjoint_polar_value`.
- `TGLV350.Regular.scalarTomitaAdjoint_conjugate_domain_iff`.
- `TGLV350.Regular.scalarTomitaAdjointConjugateInput`.
- `TGLV350.Regular.scalarTomitaAdjoint_conjugate_value`.
- `TGLV350.Regular.scalarTomitaPolar_closed_domain_iff`.
- `TGLV350.Regular.scalarClosedTomitaConjugateInput`.
- `TGLV350.Regular.scalarClosedTomita_conjugate_value`.
- `TGLV350.Regular.scalarTomitaPolar_conjugates_closed_graph`.

[Manifesto e proveniência](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_first_independent_20260913_025326_236836/manifest.json>); [compilação própria completa](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_first_independent_20260913_025326_236836/compilation.json>); [tipos/universos/axiomas próprios](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_first_independent_20260913_025326_236836/logs/AdjointPolarFirstAudit.stdout.txt>); [histórico autoral preservado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_first_independent_20260913_025326_236836/author_history.json>).

[OPEN] Inclusão inversa dos comutantes, estimativa/reconstrução dos quadrados, KMS e traço não decorrem destas identidades de domínio/polar. Nenhum novo J, raiz, gate ou memória foi criado. Integração não revista neste estrato. Só há escritas em `revisao/`; fontes do autor, monólito, custódias e pareceres anteriores permanecem intactos. **Pendente somente para completar este pacote: segundo módulo final e manifesto conjunto.**


---

2026-09-13T03:03:46-03:00 — **ADJOINT_POLAR_GRAPH_DEV_REVIEW**

[REAL — revisão DEV cumulativa concluída] **Sem P0, P1 ou P2 nos dois módulos/17 alvos.** O estrato10 anterior está preservado. Nesta continuação foram recompilados somente `ScalarRightConjugateGraph` e o auditor cumulativo17, usando o primeiro módulo próprio já verde. Manifesto e relatório finais foram lidos integralmente e seus pins conferidos nos arquivos.

O segundo módulo foi examinado integralmente:

- **Linhas13–40:** três auxiliares privados genéricos tratam reversão de imagem por involução, composição de imagens/ranges e transporte de valor entre gráficos. No último, existência de pertinência ao domínio e igualdade de valor são recebidas separadamente e descarregadas pela aplicação concreta; diferenças entre provas de pertinência não alteram o vetor. Cobertura axiomática transitiva, sem axiom/sorry/unsafe novo.
- **Linhas44–70:** J×J é um **homeomorfismo** do produto H_I×H_I, com inversa igual a si mesmo. Sua continuidade vem do J antiunitário original. O gráfico de F é enviado exatamente ao de S pela igualdade anterior e involutividade; não se presume continuidade de S ou F.
- **Linhas73–99:** a inscrição a↦Jj(a) é corretamente **semilinear para starRingEnd ℂ**. Está no domínio do S original, e S(Jj(a))=Jj(a*) usa o F original e a estrela da mesma álgebra de pares, sem troca por torção modular ou alegação de identificação de álgebras.
- **Linhas103–123:** `Homeomorph.image_closure` justifica a troca entre imagem e fecho. O graph-core de F vem do teorema já provado, e a conclusão é **closure range(a↦(Jj(a),Jj(a*)))=graph S**. A igualdade é de gráficos inteiros, não apenas uma inclusão ou densidade Hilbert. Todos os objetos permanecem no mesmo H_I.

O auditor17 confirma os tipos sem premissas residuais além de P e dos elementos/domínios explícitos. O primeiro módulo preserva F=BJ=JSJ com D(F)=J⁻¹D(B)=J⁻¹D(S); o segundo compõe essa ponte com o graph-core anterior. Não há argumento circular ou nova raiz/J no pacote.

| Fonte | Alvos | SHA256 fonte final | SHA256 binário próprio = autoral |
|---|---:|---|---|
| ScalarTomitaAdjointPolar | 10 | `7893d1356e10fac1c62b7282c4e1e3b16e534de924fa6cd81e314e140e76c248` | `cf8fdd58193bbf4b278477cca0fe55a0f669692234a23f65914996a86f588992` |
| ScalarRightConjugateGraph | 7 | `e9472d822013d3b67d4b876a5d14d8dda9b76e50325e430ec8288380cdf3ed00` | `78e80054ab1ad99ee5d1b34ee2f1f138df4258a728ca6b57c844ae8035f8ab9d` |

Reprodução: primeiro módulo/auditor10 rc0 **35.079 s / 23.457 s**, já registrados; segundo módulo/auditor17 rc0 **175.126 s / 24.75 s**. Os dois binários coincidem byte a byte com os autorais. Os 17 prints próprios coincidem exatamente com o mapa do draft e dependem somente de `propext`, `Classical.choice`, `Quot.sound`. Não houve warning nos módulos próprios; os stderr estão vazios.

Árvore final com **452 dependências de projeto pinadas**, provenientes das árvores próprias da involução, do graph-core e do primeiro módulo desta etapa. Elas foram reutilizadas sem rebuild. O LEAN_PATH contém só o build próprio e oito caminhos de pacotes externos readonly; não contém build de projeto autoral. Pins de fontes/binários/companions e dez dependências externas diretas foram reconferidos pelo runner. A leitura dos binários do autor serviu apenas à comparação, nunca à resolução de imports.

Histórico excluído: **três rc1 autorais Lean** (uma do primeiro módulo, duas do segundo). Foram lidos e preservados os streams com timeout, erro de transporte de pertinência e prints com `sorryAx`/constantes inválidas; nenhum foi aceito. A falha inicial própria de catálogo, antes de Lean, permanece registrada no estrato anterior. [DECLARADO pelo autor] A primeira emissão do draft falhou por f-string antes de criar arquivos; essa execução não serve de evidência. Aqui foram consumidos apenas os arquivos finais existentes e os logs Lean finais pinados; o recorder de draft não foi executado pelo revisor.

Documentação: `RELATORIO_ADJUNTO_POLAR_GRAFOS_ORIGINAIS_DEV.md` distingue domínio inteiro, inscrição conjugado-linear, gráfico original e ausência de reconstrução do comutante. Suas afirmações matemáticas correspondem aos enunciados. O draft retém corretamente o estatuto de emissão com revisão/integração pendentes; não foi editado para produzir aprovação.

- Manifesto autoral final: `fdc14a4ebb72d8d8b76dfaa8c2940b311f2ac7a75b14073782ecba0951c5ca0a`.
- Relatório autoral final: `a84fd0080722279e51b8d7e57623b2c6c46158cd0661228e8142697aba442945`.
- Mãe `right_graph_core_custody.json`: `8490bf478251591c5779310dc7a0ce8401e25248332b2c829391a02e17504260`.
- Compilação própria final: `ec4c748a53230678d32ec0aa09d76a0c7f2bd0addb68b7b7db9a811a46625e87`.
- Verificação própria: `ea83e614b52065ec9bd350aa2b6e1792975d2f5e03fa4326c84c43078ac847a8`.

[Verificação cumulativa e pins](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_graph_final_independent_20260913_025725_898901/verification.json>); [compilação própria final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_graph_final_independent_20260913_025725_898901/compilation.json>); [manifesto próprio/dependências](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_graph_final_independent_20260913_025725_898901/manifest.json>); [17 tipos com universos e axiomas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/adjoint_polar_graph_final_independent_20260913_025725_898901/logs/AdjointPolarGraphFinalAudit.stdout.txt>).

[OPEN] O transporte de gráficos não prova JRJ∈π(N), uma estimativa de multiplicação dos quadrados ou a inclusão inversa. Também não identifica Δ^it/KMS, traço, Three Locks ou consumo físico/por gate. Não se afirma que a imagem algébrica de j seja todo domínio, nem I=nν. Esta conclusão é **DEV dos dois módulos/17 alvos**, sem revisão de integração, novos testes autorais ou runtime. Nenhum monólito/helper/recorder foi executado pelo revisor; originais, fontes autorais, memórias e pareceres anteriores não foram alterados. **Escopo DEV delimitado encerrado.**
