# Domínios do mesmo Tomita e de seu adjunto — integração revisada

2026-09-12T16:29:40-03:00. [REAL — três módulos/17 alvos integrados e revisados]

Para os dados homogêneos construídos, inclusive cada unidade matricial local y:

    R_y D(S) ⊆ D(S),       S R_y x = π(y*) S x;
    π(y) D(S†) ⊆ D(S†),    S† π(y) z = R_y* S† z.

As igualdades valem nos domínios completos indicados, no mesmo GNS H_I e
para o mesmo operador fechado S e seu adjunto máximo. A primeira transporta
o gráfico do núcleo involutivo por um mapa contínuo de pares e passa ao fecho.
A segunda usa o pareamento para todo x∈D(S) e a definição máxima de S†.
S não é pressuposto limitado; D(S) não é identificado com a imagem algébrica.
O y* da primeira igualdade e o adjunto direito R_y* da segunda têm tipos
distintos. Para a instância local, R_y*=R_(ρy*ρ⁻¹), como provado antes.

Integração: 160 registros incrementais rc0,
90 controles aprovados, 6704 declarações
Audit e 862 arquivos embutidos. As dependências
anteriores foram reutilizadas com hashes conferidos. Revisões DEV e integrada
lidas. O corpo Python fora do embutido é igual ao estágio anterior.

[REAL — correção de metadados] Os campos globais de hash do Audit agora
apontam para os bytes do stdout corrente. Os valores herdados da v350 foram
preservados em historical_v350_audit_metadata. Dois controles verificam a
correspondência atual e a preservação histórica; o critério do gate não mudou.

O que falta para mover as seis obrigações maiores do gate:

| Obrigação | Parte já disponível | Resultado ainda exigido |
|---|---|---|
| Modular contínua | GNS do peso, S fechado, raiz e polar involutiva, novas relações nos domínios | Identificar o fluxo com (S†S)^it e demonstrar KMS global |
| Canto contínuo | Álgebra regular, ação dual e peso | Traço canônico, escala dual e canto finito Three Locks no mesmo modelo |
| H1 | Setor finito | Lacuna relativa SUSY além da face finita |
| H2 | Métrica refletida de Fisher | Dados suaves de posto quatro e identificação provenientes do mesmo estado/peso |
| H3 | Ponte condicional de Einstein e custos internos | Equilíbrio área-calor no mesmo horizonte físico, com fonte e limite exigidos |
| Testemunha completa | Contratos e resultados parciais | Interação quântica, BRST/QME, anomalias/escopo UV, composição e consumo efetivo |

As pontes de Einstein, Fisher e gauge geral linearizado já localizadas em
Chatgpt permanecem disponíveis com suas hipóteses. A tabela atual de consumo
tem três contratos anteriores; as novas obrigações exigirão seus próprios
termos e pontes de tipo exato compiladas, proveniência e consumo no certificado.
Mais declarações isoladas não bastam para mover essas flags.

[OPEN — próximo alvo preciso] Para y=e_ij e r=w_i/w_j, combinar os dois
entrelaçamentos exige identificar a instância torcida de y* com rR_y e
transportar o domínio composto D(S†S). O alvo é
R_yD(S†S)⊆D(S†S) e (S†S)R_yx=rR_y(S†S)x. Isso ainda não foi compilado.
Mesmo obtendo essa relação local, será necessário um argumento de domínio
e completude que identifique o fluxo inteiro; a relação local não o substitui.

[OPEN] KMS, identificação espectral completa, traço, hipóteses físicas e
runtime integral permanecem abertos. Nenhuma das seis flags foi promovida.
Gate legado preservado; original não executado/importado; objetivo ativo.

[Revisão DEV](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md>).
[Revisão integrada](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SCALAR_RIGHT_TOMITA_INTEGRATED.md>).
[Reaproveitamento em Chatgpt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md>).

Original relido `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia `f0f7c289ce2754e924f21af2de6204e950cc62cca95fee637c6ffbfbd1aad3a9`.
Mãe integrada `e0a1f3c0830bda9cd6f101814f5511c653da2d5667d269a3cfde17a954f88ca7`; mãe imediata de memória `ad5099094e1b8d73c414241b4ac920cfe824cb29686ea9c0711fe85c9caf0c99`.
Os manifestos DEV anteriores permanecem como registros datados.
