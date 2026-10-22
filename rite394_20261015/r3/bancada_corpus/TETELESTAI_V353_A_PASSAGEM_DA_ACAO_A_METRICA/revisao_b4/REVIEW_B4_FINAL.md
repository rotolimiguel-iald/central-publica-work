# B4 — revisão independente final

2026-09-14T17:07:19.253408-03:00 · **B4_DEV_REVIEW**

[REAL] **Candidato DEV aceito nos enunciados corrigidos e explicitamente condicionais; nenhum P0–P2 no candidato.** Reprodução Lake própria rc0, **28 alvos = 22 teoremas + 5 definições + 1 estrutura**, tipos/universos e axiomas conferidos. Apenas `propext`, `Classical.choice`, `Quot.sound`; nenhum aviso novo. **Não se certifica a redação literal incorreta da ordem:** as quatro correções abaixo são parte obrigatória do alcance, não detalhes a omitir na entrega.

## O que a prova corrige

1. **Fluxo:** a entrada usa `A·(rho+p)·H·r_A`, com `r_A=H⁻¹`. `radius_free_flux_consequence` demonstra que retirar o raio deixa um fator H extra no resultado. Conferi a presença do raio em Cai–Kim (2.12), a especialização plana (2.3) e a prescrição de temperatura (2.13); os autores discutem a limitação do horizonte dinâmico após (2.21). `heatRate` tem a orientação do calor deltaQ=-dE. A lei modificada de entropia é INPUT próprio, não resultado desse artigo. [Fonte primária](https://arxiv.org/html/hep-th/0501055).
2. **Entropia variável:** `variable_entropy_derivative` prova o termo adicional `−A·Phi′/(4G·Phi²)`. A entrada `differential_entropy` é a lei diferencial `Sdot=Adot/(4G Phi)`, distinta de derivar o quociente variável. Não se declara esta última passagem automática.
3. **Igualdade entre rotas:** o critério correto usa **rho_i>0, inclusive vácuo**, e não somente `(1+w_i)rho_i≠0`. Há contraexemplo Lean em Fin 2: matéria e vácuo positivos satisfazem o critério original de fluxo, mas têm variância `rhoM*rhoL/(rhoM+rhoL)>0`. A cláusula literal de igualdade da ordem é refutada; `sector_variance_zero_iff`/`the_two_routes_equal_iff` provam a versão corrigida.
4. **Unicidade:** `Phi_flux` seleciona um único fator apenas para entalpia total E≠0. `zero_flux_has_no_unique_factor` prova que E=0 nunca dá unicidade: pode haver nenhum fator ou todos. A leitura por divisão total de Lean não é usada como seleção física no caso zero.

Esses negativos são resultados explícitos do pacote. O aceite não deve ser convertido em afirmação de que as quatro formulações literais originais foram provadas.

## Hipóteses e uso dos fornecedores

`HubbleHorizonInput` explicita H>0, G>0, Phi>0, diferenciabilidade de H e os três vínculos entre fluxo, taxa de entropia e Clausius. Não contém a conclusão Friedmann ou Hdot como campo. `hubble_area_derivative` calcula a derivada real de `4pi/H²`; `modified_clausius_coefficient` consome o fornecedor existente. A consequência é **Hdot=−4piG·Phi·(rho+p)**. Não é construção global de horizonte ou descarga de H3; a validade física das prescrições permanece importada/condicional.

`tgl_first_friedmann_from_primitive` usa uma **primitiva efetivamente fornecida por HasDerivAt**, prova derivada zero de `H²−(8piG/3)primitive` e obtém uma constante C em I aberto/preconexo. Não prova existência de primitivas para funções arbitrárias. `tgl_first_friedmann_constant_w` fornece a primitiva `Phi*rho` quando w é constante, conserva C e usa a segunda equação obtida do dado de horizonte mais continuidade `H_nx` nomeada. `variable_factor_first_equation_defect` calcula exatamente o defeito `−(8piG/3)Phi′rho`; não afirma que todo Phi variável produz defeito não nulo nem apaga exceções.

Nos setores finitos, a variância é identificada com uma soma de quadrados ponderados por rho_i≥0. A fórmula centrada pede rhoTot≠0; a comparação com o valor absoluto pede rhoTot>0 e E≥0. A diferença de **fontes** é beta·variância≥0; `the_two_hubble_rates_differ` mantém o prefator **−4piG**, portanto para G>0 o sinal da diferença de Hdot é o oposto. Esse sinal não foi invertido por nomenclatura.

`sector_clausius_matches_closed_rate` efetivamente aplica a equação de Clausius com Phi_flux e a identidade de entalpia corrigida. `common_w_flux_factor` exige E≠0 e 1+w≥0 para coincidir com `1+beta*|1+w|`. A primeira equação setorial permanece a B3 já revista; não se supõe que duas leis diferentes de Hdot descrevam automaticamente a mesma solução. **Nenhuma rota é escolhida.**

## Reprodução e custódia privada

Raiz curta `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\s`, tentativa `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b4\independent_20260914_170247_181979`. Comando: `lake build TGLExt.ThermodynamicFriedmann TGLExt.SectorRouteComparison TGLExt.AuditThermodynamics TGLExt.ReviewThermodynamics`. Os três arquivos autorais foram copiados em bytes, sem objetos; mais auditor próprio com `#check`, `pp.universes` e `#print axioms`. Os três .oleans finais são byte a byte iguais aos autorais. **Quatro objetos novos; 113 objetos próprios anteriores preservados; total 117.** Fontes, traces, relatórios e pins protegidos B1/B2/B3 foram relidos e não mudaram.

Mathlib e oito pacotes auxiliares continuam o cache herdado pinado em B1/B2; não foram recompilados. Toolchain Lean 4.31.0 pinada no run. Nenhum build de projeto autoral no LEAN_PATH. Configuração Git segura limitada aos caminhos privados no ambiente do processo, sem alteração global. Nenhuma falha nesta execução Lake B4.

Ficha MD/JSON lida integralmente; 13 fornecedores conferidos por hash/linha. A ficha antecede as fontes nos metadados locais medidos; isso não equivale a selo externo de tempo. A comparação com a ORDEM 012, linhas 125–141, está no JSON. As buscas da ficha são históricas, não novas buscas exaustivas; locadores Python são propostas de consumidor, não integração revisada.

`AUDITORIA_B4.json` e fontes/streams dos negativos foram relidos: omitir Phi (`BadThermodynamicFactor`) e inverter o sinal beta·variância (`BadVarianceSign`) falham por **Type mismatch**, com imports funcionando. São execuções autorais lidas e pinadas, não execuções minhas adicionais. Seu mapa de 28 axiomas coincide com o próprio. A alegação de preservação dos 941 arquivos-base e um.py é [DECLARADO] no auditor autoral; não se refez inventário amplo.

## Pins e saídas

| Arquivo | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---|---|
| ThermodynamicFriedmann | `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3` | `2a7148b530748b2e551c1cc2b29b82c984959f11a55182a68610ce55ec563f57` |
| SectorRouteComparison | `b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4` | `87379c48027a183ead16fdc00f493a3bd3da3c3be18e1f8cd23c37250e6ae9ea` |
| AuditThermodynamics | `0c75ce3985df5faa7b1f2fdabec3bbdd936a6d200607d60d1219f28ad7f2a392` | `1c2dae4020a6ad36388c9755554dd13e97af8633e8edc9112efd188a2ee12952` |

- [Revisão JSON](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b4/REVIEW_B4_FINAL.json>) — `bfe87230a0dd92621bbaef7ab6d833c344eba8a2f080158cc9a95c968612000a`.
- [Compilação própria](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b4/compilation.json>) — `094361aefa7cfe355ee45c1dd4d82b3c0133b9baceb147a4b1f2442bce5f0854`.
- [Run rc0](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b4/independent_20260914_170247_181979/run.json>) — `b806fd028f1b71c5cfdc7d66998da1fa8101b0b64e34b64b2099a71bfa35cc1d`.
- [Snapshot](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b4/independent_20260914_170247_181979/snapshot.json>) — `47e8a535f643ab1a5f294474fc16e22d26575250602b6938513ffcf307e988d5`.
- [Ficha/contrato](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b4/independent_20260914_170247_181979/contract_and_fiche.json>) e [inspeção semântica](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b4/independent_20260914_170247_181979/semantic_inspection.json>).

## Alvos auditados

- `ChatgptAudit.FLRW.hubbleArea`
- `ChatgptAudit.FLRW.entropyFactor`
- `ChatgptAudit.FLRW.entropy_factor_pos`
- `ChatgptAudit.FLRW.hubble_area_derivative`
- `ChatgptAudit.FLRW.HubbleHorizonInput`
- `ChatgptAudit.FLRW.modified_clausius_coefficient`
- `ChatgptAudit.FLRW.tgl_second_friedmann_from_clausius`
- `ChatgptAudit.FLRW.radius_free_flux_consequence`
- `ChatgptAudit.FLRW.variable_entropy_derivative`
- `ChatgptAudit.FLRW.tgl_first_friedmann_from_primitive`
- `ChatgptAudit.FLRW.tgl_first_friedmann_constant_w`
- `ChatgptAudit.FLRW.variable_factor_first_equation_defect`
- `ChatgptAudit.FLRW.SectorFluid.secondMoment`
- `ChatgptAudit.FLRW.SectorFluid.sectorVariance`
- `ChatgptAudit.FLRW.SectorFluid.fluxFactor`
- `ChatgptAudit.FLRW.SectorFluid.corrected_enthalpy`
- `ChatgptAudit.FLRW.SectorFluid.centered_variance`
- `ChatgptAudit.FLRW.SectorFluid.sector_variance_nonneg`
- `ChatgptAudit.FLRW.SectorFluid.sector_variance_zero_iff`
- `ChatgptAudit.FLRW.the_two_routes_differ`
- `ChatgptAudit.FLRW.the_two_routes_equal_iff`
- `ChatgptAudit.FLRW.the_two_hubble_rates_differ`
- `ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure`
- `ChatgptAudit.FLRW.sector_clausius_matches_closed_rate`
- `ChatgptAudit.FLRW.common_w_flux_factor`
- `ChatgptAudit.FLRW.zero_flux_has_no_unique_factor`
- `ChatgptAudit.FLRW.matter_vacuum_variance`
- `ChatgptAudit.FLRW.nonzero_flux_support_does_not_characterize_equality`

**Encerrado o DEV B4 delimitado.** Sem pendência de recompilação ou análise destes 28 alvos. Integração, gate, B5/B6, escolha de rota, A1, fecho global, experimentos e atualização de memórias não integram este aceite. Nenhum arquivo autoral/canônico foi alterado.
