# Revisão independente dos módulos de horizonte e polarizador — raiz053

[REAL — leitura integral das fontes e conferência dos registros de desenvolvimento]
Revisor: agente raiz. Autores: HorizonGNSImplementation por Newton; SymplecticPolarizer por Beauvoir. A raiz é autora da integração TowerStatePolarizer, cuja revisão matemática independente está em CONTINUACAO053_REVISAO_TORRE_NEWTON.md. Esta nota não é autoaprovação dessa integração.

## Horizonte

A identidade de pareamentos GNS usa omega_adT no produto A*B, com A,B no fator. A preservação de norma e distância segue dessa identidade. A definição no pré-espaço é feita por Quotient.lift e usa a compatibilidade real dos embeddings da torre para representantes de níveis distintos.

A imagem de um vetor local pelo horizonte não é presumida local: o contradomínio do mapa inicial já é o Hilbert completo. Completion.extension é aplicada a uma isometria demonstrada. Linearidade complexa, norma e inversas são verificadas por densidade no completamento.

O lema horizon_gns_map_apply_factor estende a fórmula a todo A∈M usando expectation_omega_limit e preservação da distância GNS da ação adT. Não supõe convergência em norma de operadores de toda a álgebra local para M. As inversas usam os horizontes h e h.inv e suas ações inversas sobre os elementos do fator.

O vetor Ω é fixado pelo implementador construído W_h. Nenhum passo o identifica com h.U. O mesmo realStateSubspace é o fecho do span real de AΩ, A autoadjunto em M; a ação preserva seus geradores e o fecho. A aplicação de h.inv paga sobrejetividade no setor real. Não encontrei falha material de enunciado ou hipótese oculta nessa construção.

## Polarizador

D é literalmente P_R(-i)P_R, com projeção ortogonal REAL. A identidade de dualidade tem o sinal correto porque Re(-i z)=Im z. A norma no máximo um resulta de duas projeções contrativas e da norma unitária de -i. A antissimetria é relativa ao produto interno real.

A unicidade por pareamentos e a caracterização do núcleo utilizam vetores do mesmo R; não se exige que R seja factorial nem se elimina seu radical por hipótese. A família de formas soma normas quadradas de D e D², com epsilon não negativo para positividade e identificação do núcleo com ker D.

A covariância exige isometria complexa W com x∈R↔Wx∈R. Primeiro demonstra covariância da projeção, depois de D e da forma. Isso não substitui W por uma ação abstrata não implementada. Na integração, W é o implementador GNS construído acima.

## Evidência e alcance

As fontes abaixo coincidem byte a byte com as cópias que passaram no marcador de desenvolvimento indicado. As etapas tinham exit0, passed=true, source_stable=true e inputs_stable=true. O marcador completo terminou PASS4/4, incluindo a integração dos três primeiros módulos. Esta nota não declara que os cinco módulos053 já passaram juntos.

| Fonte | Bytes | SHA256 lido | Censo do marcador |
|---|---:|---|---|
| [HorizonGNSImplementation.lean](<C:/IALD/Central de Patentes/Chatgpt/HorizonGNSImplementation.lean>) | 15089 | 870e4ec0f3330729a49ee5d4f4730fae523ac80cffb4b6bc0e265e17620ab087 | 28T/8D/1I/37 prints |
| [SymplecticPolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/SymplecticPolarizer.lean>) | 9193 | ef5c76b0d4451fa4a615b85c0c8567e503e052b9f91187e4fb58ffb5fa929eff | 19T/3D/0I/22 prints |

Marcador: [CONTINUACAO053_DEVELOPMENT_20260907_051929_205158.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_DEVELOPMENT_20260907_051929_205158.json>).

[OPEN] Seleção física de horizontes, localização lorentziana, escala dimensional de área e H3. Uma forma real bilinear no ambiente, uma classificação do radical em operadores SA do fator e uma identificação de área gravitacional são afirmações distintas.

Nenhum arquivo existente foi alterado por esta revisão. Somente esta nota nova foi escrita.

Emissão UTC: 2026-09-07T05:31:09.383728+00:00
