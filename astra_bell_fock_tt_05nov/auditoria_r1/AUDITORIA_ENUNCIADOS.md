# Conferência independente de BellEspelhamentoR1

**[REAL] Escopo formal.** Os índices são os quatro pares de bits e as matrizes têm coeficientes complexos. A leitura abaixo confronta os tipos e as hipóteses dos enunciados com a álgebra de matrizes. O recibo JSON associa cada nome à linha inicial na fonte, aos axiomas impressos pelo compilador e ao SHA-256 do log integral. As dependências do ambiente v408 já estavam compiladas.

Escrevo (P=|Φ⁺⟩⟨Φ⁺|, R=|Φ⁻⟩⟨Φ⁻|, Q=I-P, X=|Φ⁺⟩⟨Φ⁻|). Na tabela, (c,s,u,v) são reais, (n) é natural, (ρ_n) é a família explícita `bellAfter` e (η=2uv).

| Declaração | Identidade e significado conferidos |
|---|---|
| `bellR_idem` | (R²=R). A definição por produto exterior do vetor normalizado fornece a autoadjunção. |
| `bellP_bellR` | (PR=0). O estado Φ⁻ está no complemento do canto Φ⁺. |
| `bellR_bellP` | (RP=0). A nulidade está provada na ordem contrária. |
| `bellP_bellX` | (PX=X). A imagem da coerência é o raio Φ⁺. |
| `bellX_bellP` | (XP=0). A coerência anula o raio Φ⁺ quando ele atua pela direita. |
| `bellX_bellR` | (XR=X). O domínio sustentando essa coerência é o raio Φ⁻. |
| `bellQ_idem` | (Q²=Q). A identidade usa a idempotência do projetor canônico. |
| `bellP_bellQ` | (PQ=0). A decomposição complementar é usada na ordem escrita. |
| `bellQ_bellP` | (QP=0). Vale a segunda ordem. |
| `bellInputDensity_eq_corner` | (ρ=|cΦ⁺-isΦ⁻⟩⟨cΦ⁺-isΦ⁻|) para quaisquer (c,s). A expansão tem (+icsX-icsX†). Seu traço vale (c²+s²). |
| `bellInput_PQ` | (PρQ=icsX) para quaisquer (c,s). O sinal positivo vem da conjugação do coeficiente de Φ⁻ no bra. |
| `bellAfter_zero` | (ρ₀=ρ). O valor de potência de expoente zero é 1 também para (η=0). |
| `bellAfter_succ` | (ℰ(ρₙ)=ρₙ₊₁) sob (u²+v²=1). É recursão desta família. O canal em toda matriz também pode ser analisado pela decomposição em quatro blocos. |
| `bellAfter_detectors` | Para (c²+s²=1), os traços são ((1±2ηⁿcs)/2). D₊ corresponde ao ket com (-i), D₋ ao ket com (+i). O enunciado isolado admite quaisquer (u,v), logo requer vínculo adicional para interpretar os traços como probabilidades de iteração do canal. |
| `mirror_complete` | (M₀²+M₁²=I) sob (u²+v²=1). As Kraus da definição são autoadjuntas porque os pesos são reais e (P,Q) são projetores ortogonais. Assim a soma é a completeza de Kraus. A preservação de traço geral e a positividade completa se deduzem matematicamente. |
| `mirror0Inv_mul_mirror0` | (M₀⁻¹M₀=I) para (uv≠0). A condição é implementada por duas hipóteses de não anulação. |
| `mirror0_mul_mirror0Inv` | (M₀M₀⁻¹=I) sob as mesmas hipóteses. |
| `mirror_branch_reconstruct` | Reconstrói uma matriz arbitrária a partir da saída **subnormalizada** (M₀ρM₀) por congruência com a inversa. Uma implementação heraldada requer escalar a inversa a uma contração e contabilizar o sucesso. |
| `bellInput_marginals` | Ambos os traços parciais do input puro normalizado valem (I₂/2). A fase relativa imaginária e os coeficientes reais são parte do preparo. O enunciado mede o instante de entrada. |
| `bellInput_unprepared_PQ` | (PρQ=0) quando o preparo é ((c,s)=(1,0)). O par fica no raio Φ⁺. |
| `bellInput_full_transfer_PQ` | (PρQ=0) quando ((c,s)=(0,1)). O par fica no raio Φ⁻. |
| `bellAfter_balanced_detectors` | Em (c=s=1/√2) os traços são ((1±ηⁿ)/2). Vale a distinção entre expressão algébrica para quaisquer (u,v) e canal normalizado. |
| `the_bell_mirror_visibility` | Conjuga a recursão e os dois traços com as duas normalizações explícitas. Dá o contraste assinado (I₊-I₋=2ηⁿcs) na fase fixa dos detectores. Uma visibilidade por varredura envolve recorrer aos demais analisadores e tomar máximo, mínimo e módulo. |

**[DERIVED] Verificações de interpretação.** Em Lean, os vetores auxiliares `detectorPlusVec` e `detectorMinusVec` têm norma √2. O fator ½ aparece no operador de detecção e dá exatamente os dois projetores normalizados do handoff. Sua soma é (P+R). O complemento (I-P-R) fecha a medição no espaço de dimensão quatro. Para (c=s=1/√2, n=0), D₊ tem probabilidade 1 e D₋ tem probabilidade zero, fixando o sinal positivo da saída na convenção matemática do modelo.

**[DERIVED] Inversa seletiva.** Dado o resultado 0, o filtro físico (K=tM₀⁻¹) satisfaz (K†K≤I) se (|t|≤min(|u|,|v|)). Para entrada com traço 1, o sucesso **conjunto** de obter 0 e revertê-lo vale (|t|²). A probabilidade de reversão **condicional** ao resultado 0 vale (|t|²/Tr(M₀ρM₀)), quando o denominador é positivo. A operação complementar correspondente ao insucesso completa o instrumento. A inversa matricial da pedra tem alcance algébrico mais amplo que uma operação determinística.

**[OPEN] Identificação empírica.** O parâmetro (η) está livre na família antes da identificação proposta com β. A pedra não contém tempo físico, geometria que conte (n), nenhum ajuste de lock, conversão de fase óptica em rotação espacial, nem termo ligando essas Kraus à propagação de um par físico. Uma recompilação bem-sucedida resolve a auditoria dessa fonte.
