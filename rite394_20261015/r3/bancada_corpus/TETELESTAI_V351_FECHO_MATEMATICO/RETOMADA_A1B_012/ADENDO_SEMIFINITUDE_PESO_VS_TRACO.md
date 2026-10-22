[DERIVED — correção de roteiro, com revisão escrita independente; sem novo teorema Lean]

# Semifinitude do peso e semifinitude do traço

2026-09-14T19:05:57.798346-03:00

O requisito por minorantes positivos pertence ao futuro traço τ. Não deve ser cobrado como propriedade geral do peso dual ν. A fonte existente já fornece a semifinitude usual deste peso: `TGLV351.scalarWeight_square_finite_wot_closure`, em `V351ScalarWeightSemifiniteness.lean`, é a densidade WOT do domínio quadrado-finito no mesmo core. A consulta não recompila esse fornecedor nem cria outro objeto.

[KNOWN] Hiai, *Concise lectures on selected topics of von Neumann algebras*, §7.1, Definição 7.1, p.63, usa a densidade fraca do ideal quadrado-finito para a semifinitude de pesos. A definição não exige minorantes finitos abaixo de todo positivo. [Fonte primária](https://arxiv.org/pdf/2004.02383#page=63).

[DERIVED — prova escrita, não Lean] Em B(ℓ²(N≥1)), seja φ(A)=Σ n²⟨eₙ,Aeₙ⟩ para A≥0. É um peso fiel normal: somas finitas de funcionais vetoriais positivos são normais, os supremos comutam, e φ(A)=0 implica A¹ᐟ²eₙ=0 para toda a base. Para p_N a projeção coordenada finita e x limitado, φ((xp_N)*(xp_N))=Σ_(n≤N) n²‖xeₙ‖²<∞. Como xp_N→x fortemente, o ideal quadrado-finito é denso.

Escolha ξₙ=c/n, com c>0 normalizando ‖ξ‖=1. Então φ(Pξ)=∞. Todo 0≤B≤Pξ é bPξ, 0≤b≤1: a positividade anula B¹ᐟ² em ξ⊥. Só b=0 tem peso finito. Portanto sup{φ(B):0≤B≤Pξ, φ(B)<∞}=0≠φ(Pξ). Isto refuta a ponte geral para pesos, não a existência do traço nem uma propriedade de uma projeção específica do core construído.

Para um traço normal semifinito τ, tome projeções e_i↑1 com τ(e_i)<∞. Para A≥0 limitado, B_i=A¹ᐟ²e_iA¹ᐟ²≤A e B_i↑A. A tracialidade dá τ(B_i)=τ(e_iAe_i)≤‖A‖τ(e_i)<∞; a normalidade fornece τ(A)=sup_i τ(B_i). Assim o campo `RegularCoreTraceData.semifinite` continua exigido e pode ser pago usando tracialidade. Não removemos nem enfraquecemos esse contrato.

A revisão independente escrita em `revisao_core/CONSULTA_SEMIFINITUDE_PESO_VS_TRACO.md` aceita o argumento. Ela não é uma compilação ou construção de τ. Nenhum relatório selado, contrato ou memória canônica foi modificado. A menção anterior a `scalarWeightLeftIdeal_wotDense` era um nome aproximado incorreto; o fornecedor exato é o acima.

[OPEN] Identificação das potências do gerador regular, afiliação, escala dual e perturbação para o traço. A correção retira uma exigência falsa sobre ν, sem dispensar as obrigações de τ.

## Custódia lida nesta gravação

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean` — 2181 bytes — SHA256 `f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceContract.lean` — 5624 bytes — SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\CONSULTA_SEMIFINITUDE_PESO_VS_TRACO.md` — 3689 bytes — SHA256 `556c0ca442b97549d961961e9035c4dc74f1c4c2797a4af2edcbab0bdf152ee0`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\CONSULTA_SEMIFINITUDE_PESO_VS_TRACO.json` — 1170 bytes — SHA256 `8ace201782aa9ea8b5dff1b2e6160c53eb6faafbcc36c27c1f008846d1784db6`.
