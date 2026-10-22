# Parecer independente: classe par no BV–BRST clássico completo

10/09/2026. Revisor: /root/selected_geometry_design. [DERIVED — revisão matemática escrita da composição087]. [REAL — custódia documental separada].

**Não identifiquei erro material na composição examinada, no contrato fixado.** A nota constrói uma linha livre de Rher em H⁴ do diferencial BV–BRST CLÁSSICO completo por valência e distingue corretamente a exatidão do ciclo completo de Pontryagin de sua classe não nula no primeiro complexo CE. O argumento considera primitivas com antifields e detecta a não exatidão já em C₆. Não precisa de Mittag–Leffler.

Fonte lida integralmente: [Classe par em H⁴ BRST e Pontryagin exato](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md>). Pin desta versão, medido dos bytes: **14186 bytes; SHA-256 bd1a27316e99c33718e583f9442f8869bc3a234c63e3d20c74ee36abec43da5c**. Manifesto autoral: [MANIFESTO_CLASSE_PAR_BRST_087.json](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/MANIFESTO_CLASSE_PAR_BRST_087.json>).

Esta revisão trata a composição própria da raiz. A entrada N₂ é a [demonstração quadrática087 de Turing](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>), lida para conferir precisamente a independência de I₀ν e J₀ν usada. Sua revisão integral específica é uma etapa distinta, a cargo de Singer. Não reapresento a minha autoria da prova simbólica086 como uma aprovação independente: consumo o [parecer integral de Turing086](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md>) e os resultados antecedentes no alcance registrado.

## 1. Fechamento off-shell, sinais e normalização

As convenções sg=Lie_c g e scᵘ=cᵛ∂ᵥcᵘ são as da transgressão076. Se Ω_I=ρ_I dx⁰dx¹dx²dx³ é uma quatro-forma natural da métrica dinâmica, sua transformação ativa dá

    sρ_I=cᵘ∂ᵤρ_I+(∂ᵤcᵘ)ρ_I.

O uso da inversa e do volume de g é necessário. Não seria lícito manter somente vol₀ e substituir a lei de transformação ativa pelo caráter tensorial sob transformações simultâneas da referência.

Para G=c⁰c¹c²c³, a contribuição da posição μ no Leibniz ímpar tem sinal (−1)^μ. Somente ν=μ em scᵐ=cᵛ∂ᵥcᵐ sobrevive, porque todas as outras escolhas repetem um ghost de valor. Deslocar o ghost derivado pelos 3−μ fatores restantes produz (−1)^(3−μ). O produto dos sinais é −1 para as quatro posições. Portanto

    sG=−G∂ᵤcᵘ.

Como G é par, o termo de divergência de sρ_I cancela ρ_I sG. O termo (c·∂ρ_I)G contém cinco ghosts de valor em dimensão quatro e é zero. Isso verifica sA_I=0 sem EOM ou integração por partes. Derivadas de ghosts são ímpares, como exigido nesse cálculo.

O fator 1/4! da descrição por componentes antissimétricas é compatível com a escrita ordenada ν=√|det g₀| C⁰C¹C²C³. Esta última é a definição inequívoca usada para os coeficientes. Não se está avaliando uma forma alternada quatro vezes no mesmo vetor comutativo.

## 2. Valência seis e pertença ao domínio formal

W(g₀)=0 na espaço-forma, logo W(g₀+t h)=tW[1]+O(t²). As variações das inversas e do volume só alteram termos posteriores na densidade quadrática. Com c=tC, seguem

    A_I=t⁶ I₀ν+O(t⁷),   I₀=½W[1]².

A normalização é a usada na entrada N₂087 e na classificação086 de uma derivada, e não I082 sem seu fator dois. A₆ pertence a ghost quatro e valência seis; estes dois graus não são permutáveis.

Os coeficientes de g⁻¹ e vol_g são séries formais regulares junto à identidade. Em cada valência há finitíssimas parcelas e finitíssimos jatos; as contrações de Weyl dependem de derivadas da métrica até ordem dois. Não é necessária uma escolha de raiz real entre métricas afastadas ou uma ressoma a t numérico. A filtração é preservada porque a referência é on-shell e o diferencial mínimo não reduz valência.

Essa pertença é a da álgebra formal clássica declarada. Não prova, por si, escala por aridade, identidades de contato, normalizações de inserções ou admissibilidade causal Q2.

## 3. Imagem inteira da conexão e presença dos antifields

Conferi o uso da [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) e do [levantamento077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>). A sequência

    0 → (A₆,s₀) → C₆ → C₅ → 0

é uma sequência de complexos. Sua conexão δ leva um ciclo de C₅ à classe da componente E6 de s de um levantamento. Alterar essa componente do levantamento acrescenta uma fronteira s₀.

Ponha T=T_P,≤5. A imagem H³(C₅)→H³(C₃) é a linha Rher[α₃], e T realiza seu gerador. Para qualquer y∈H³(C₅), a escolha de λ com a mesma imagem implica y−λ[T]∈Kcal. Como δ(Kcal)=im d₁|E5 e δ[T]=[J₀ν] na normalização característica herdada, segue

    im δ = Rher[J₀ν] + im d₁|E5.

As duas inclusões estão justificadas. Não se usa injetividade da aplicação H³(A₅,s₀)→Kcal, nem uma cisão de H³(C₅). O termo s₂v₄ da mudança de representante080 só desaparece no truncamento C₅; em C₆ ele reaparece na correção permitida, sem mudar δ. Essa precisão impede uma perda de termos de valência seis.

A fonte080 faz essa redução no complexo mínimo com antifields. Portanto a fórmula da imagem não se limita a primitivas sem antifields. A própria densidade A_I é antifield-free, mas essa propriedade do representante não foi usada para restringir indevidamente suas possíveis fronteiras.

## 4. Independência CE e detector em C₆

Se λA_I=sB em C₆, então B mod C₅ é um ciclo e δ[B mod C₅]=λ[I₀ν]. Pela fórmula da imagem, λ[I₀ν]−μ[J₀ν]=d₁z para algum μ e z. A comparação082 identifica essa igualdade com uma relação entre I₀ν e J₀ν na cohomologia CE quadrática.

A entrada087 fornece duas classes independentes sobre Rher. Para esta composição basta essa independência: a exaustão adicional de H⁴ CE não é necessária. Sua justificativa na entrada usa os dois símbolos quirais independentes e a impossibilidade de uma divergência de ordem finita produzir um escalar quadrático de grau principal quatro. O mecanismo é compatível com a prova simbólica086 já revista por terceiro e com a eliminação da isotropia. Nenhuma avaliação numérica é usada para separar coeficientes nilpotentes.

Logo λ=μ=0, e Rher→H⁴(C₆,s), λ↦λ[A_I], é injetivo. Trata-se de uma linha livre, não de uma afirmação de que o grupo inteiro tenha posto um. O argumento distingue H(s₀), a cohomologia de d₁ e a cohomologia do truncamento: a conexão entre C₆ e C₅ é exatamente o elo que permite a conclusão no último espaço.

## 5. Truncamentos posteriores e a série formal

O MESMO ciclo A_I fornece uma classe em cada C_N, N≥6. Se um múltiplo fosse fronteira em qualquer deles, a projeção de complexos a C₆ contrariaria a injeção já provada. A mesma lógica vale para uma fronteira formal em Ĉ: seu truncamento em C₆ seria uma fronteira.

Isso estabelece a linha livre em H⁴(C_N,s) para N≥6 e em H⁴(Ĉ,s), sem intercambiar cohomologia com limite inverso. Não se afirma H⁴(Ĉ)=lim H⁴(C_N), lim¹=0, exaustividade dos grupos ou uma cota uniforme de ordem dos jatos de todas as primitivas. Cada primitiva formal admitida teria um truncamento finito que já é impossível.

## 6. Pontryagin e precisão aditiva sobre o operador

A [transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>) e seu [parecer específico](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_TRANSGRESSAO_BRST_076_20260910/PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md>) conservam k=S(∇c)S⁻¹−(sS)S⁻¹. Com Ω=sk+k²,

    T_P=tr(kΩ)−⅓tr(k³),   sT_P=A_P.

O termo sS e os sinais graduados estão preservados. A primitiva começa em valência três; o ciclo A_P começa em valência seis. Por isso a não nulidade de J₀ν no CE de m=2 não contradiz a exatidão de A_P no complexo completo. A ligação de valências inferiores está contabilizada pela conexão δ, em vez de ser apagada numa identificação com a diagonal CE.

**Precisão aditiva de terminologia:** nesta nota, “s completo” significa o diferencial BV–BRST CLÁSSICO s₀+s₁+s₂+⋯, com todas as valências do teste formal. Não é um operador quântico renormalizado, uma carga interagente já construída ou uma solução de QME. Essa precisão não altera o enunciado matemático congelado; explicita o alcance já compatível com suas ressalvas.

O resultado usa a referência espaço-forma com sigma constante projetado, dimensão quatro, orientação e coeficientes herdados inertes. Não transporta classes automaticamente ao fundo sigma físico não constante, a espectadores, a uma categoria de jatos infinitos por coeficiente ou a K variável. Também não trata o critério horizontal com coeficientes em H⁴(s) como já resolvido, nem converte ghost quatro em anomalia física de ghost um.

## 7. Custódia e alcance desta revisão

[DERIVED] Parecer favorável à composição, sem erro material identificado no escopo acima. As revisões da entrada quadrática087 e dos antecedentes conservam autoria e alcance próprios. Não aprovo independentemente minha prova086 por esta emissão, nem atribuo a Singer uma revisão que ainda não tenha sido efetivamente publicada e consumida.

[REAL — documental] O recibo mede a fonte, o manifesto autoral e seus pins, confere links e registra preservação de bytes antes/depois. Arquivos apenas pinados são distinguidos das leituras matemáticas. O script próprio emite somente texto novo e hashes; não executa fontes matemáticas, CAS, Lean ou um.py, nem recaptura canônicos. Os números de checks são documentais, não uma contagem de demonstrações formais.

[OPEN — fora do parecer] A classificação completa do BRST, os outros grupos e diferenciais, admissibilidade causal, operadores quânticos renormalizados, QME, UV e reconstrução geral dos mesmos dados selecionados. Nenhum gate ou veredito físico é movido por esta revisão.
