# Continuação045 — revisão A3: esperança aperiódica
06/09/2026. Somente leitura e esta nota nova. Nenhuma compilação ou novo teorema Lean nesta revisão.

## Conclusão e estatuto

[DERIVED] Há uma rota concreta para construir ExpectationInput P para qualquer SiteProfile, sem assumir período comum e sem importar sua própria conclusão. Ela reaproveita periodAverage e a ação direita da torre. A parede é uma sequência identificada de provas de limite e levantamento limitado, não uma ausência do teorema ergódico médio no mathlib.

[REAL — fontes locais lidos] O mathlib instalado contém o teorema ergódico médio de von Neumann para UMA contração Hilbert, além de uma API para empacotar limites pontuais uniformemente limitados de operadores. Nenhum desses resultados, isoladamente, entrega uma esperança condicional normal completamente positiva sobre a álgebra.

[OPEN — implementação ainda necessária] Não foi produzido nesta nota aperiodicExpectationInput nem validado um binário novo. A rota abaixo não deve ser anunciada como dívida formal já paga.

## 1. Contrato canônico conferido

O arquivo canônico [TheOathOnTheTower.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheOathOnTheTower.lean:344>) tem exatamente:

```lean
structure ExpectationInput where
  E : (TowerHilbert P →L[ℂ] TowerHilbert P) →
      (TowerHilbert P →L[ℂ] TowerHilbert P)
  into : ∀ A ∈ theFactorObject P, E A ∈ omegaCentralizer P
  fixes : ∀ A ∈ omegaCentralizer P, E A = A
  ortho : ∀ A ∈ theFactorObject P, ∀ B ∈ omegaCentralizer P,
    omegaState P (star B * (A - E A)) = 0
```

Não há campos de linearidade, norma, positividade completa ou normalidade. Os valores de E fora de M não são restringidos. Uma construção pode definir E=0 fora de M; propriedades de esperança devem então ser enunciadas para sua RESTRIÇÃO a M, não para toda B(H).

[REAL — fonte lido] [TheImportedExpectation.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheImportedExpectation.lean>) declara TakesakiInput.expectation : Nonempty (ExpectationInput P). O teorema the_expectation_exists_by_import extrai esse campo; usá-lo como existência independente seria circular. O mesmo arquivo distingue expressamente omegaState_seqWOT de normalidade σ-fraca plena: a primeira é uma consequência sequencial, não uma equivalência formal já estabelecida.

## 2. APIs efetivamente disponíveis

| Fonte lida | Resultado disponível | Limite do resultado |
|---|---|---|
| [MeanErgodic.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/MeanErgodic.lean:89>) | ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection, para f : E →L[𝕜] E, ‖f‖≤1, espaço Hilbert completo | Projeta nos fixos de um operador f, não automaticamente nos fixos de todo um grupo real |
| [Operator/Completeness.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Completeness.lean:62>) | ContinuousLinearMap.ofTendstoOfBoundedRange: uma família de operadores com imagem limitada e limite pontual em todos os vetores determina um operador linear contínuo | É necessário provar previamente o limite em TODOS os vetores; convergência apenas em Ω não é seu argumento |
| [InnerProductSpace/WeakOperatorTopology.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/WeakOperatorTopology.lean>) | ContinuousLinearMapWOT.tendsto_iff_forall_inner_apply_tendsto e continuidade do adjunto em WOT | Caracterização topológica, não teorema de existência do limite ou de normalidade da esperança |
| [CompletelyPositiveMap.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/CompletelyPositiveMap.lean:50>) | Estrutura CompletelyPositiveMap e classe correspondente; positividade por amplificações matriciais | Ainda requer construir o mapa e provar suas amplificações positivas com as instâncias apropriadas |
| [PeriodAverageOperator.lean](</C:/IALD/Central de Patentes/Chatgpt/PeriodAverageOperator.lean>) | periodAverage, period_average_operator, period_average_mem_factor | Todos valem para QUALQUER T>0; não exigem LocalPhasePeriod |
| [ExpectationProjection.lean](</C:/IALD/Central de Patentes/Chatgpt/ExpectationProjection.lean>) | project_flow_commutes, expectation_flow_commutes, expectation_omega_limit | Permitem controlar cada corte e recuperar a ação em Ω |
| [RightMult.lean](</C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/RightMult.lean:443>) | rTowerPi_omega N y = tof N y no completamento; factor_comm_rTowerPi hA y | A órbita direita local de Ω contém o pré-Hilbert denso; fornece o levantamento forte proposto abaixo |
| [TracialCentralizerExpectation.lean](</C:/IALD/Central de Patentes/Chatgpt/TracialCentralizerExpectation.lean>) | centralizer_from_expectations | Se B∈M e todos os towerExpectation N B pertencem ao centralizador, então B pertence |
| [PeriodicCentralizerExpectation.lean](</C:/IALD/Central de Patentes/Chatgpt/PeriodicCentralizerExpectation.lean>) | period_average_fixes, period_average_ortho e construção periodicExpectationInput | A periodicidade entra na identidade period_average_prefix usada nessas provas; não se pode apagar a hipótese sem substituí-la |

A busca incluiu esses arquivos, as pastas Dynamics/Analysis pertinentes e buscas dirigidas por topologias, médias e mapas positivos. Ela não demonstra inexistência de outros lemas no acervo. Em particular, o resultado de compacidade pontual em Operator/Completeness exige ProperSpace no contradomínio; não pode ser aplicado diretamente ao Hilbert infinito como se sua bola normada fosse compacta.

## 3. Cuidado com discretizar o grupo modular

[DERIVED] Aplicar o teorema ergódico médio a U(1) entrega Fix U(1). Um grupo U(t)=exp(2πit) sobre ℂ tem U(1)=I, embora o subespaço fixo para todos os t seja zero. Logo a igualdade entre os dois espaços precisa de prova.

Uma alternativa geral seria usar uma contração média de U(1),U(-1),U(√2),U(-√2), provar que seus fixos são a interseção dos fixos desses operadores e usar densidade do subgrupo gerado por1,√2 mais continuidade forte. Esses passos não foram identificados como uma composição já pronta nesta revisão. Para a torre concreta, a rota de fases finitas abaixo aproveita melhor o código existente e evita essa discretização.

## 4. Rota concreta recomendada, sem período comum

Escreva T_n=n+1 e C_n(A)=periodAverage P T_n (por positividade) A.

### 4.1 Primeiro lema novo: Cesàro de uma fase real

[DERIVED; prova Lean nova] Para cada r∈ℝ:

```
T⁻¹ ∫₀ᵀ modularPhase(t,r) dt → if r=0 then 1 else 0,   T→+∞.
```

Se r=0, a igualdade é exata. Se r≠0, a integral é (exp(irT)−1)/(ir), e a norma da média é no máximo2/(|r|T). O arquivo PeriodAveragePrefix já usa integral_exp_mul_complex e a identificação da fase com a exponencial. Seu integral_modularPhase atual usa uma igualdade de período; o novo lema deve substituí-la por este limite, sem supor essa igualdade.

Por finitude de chainIdx N, obter o limite matricial das médias de flowLevel em cada N para specExpect (towerW P N), preservando todos os blocos de pesos iguais. Não substituir specExpect por diagonalização simples: degenerescências locais continuam possíveis no perfil aperiódico.

### 4.2 Segundo lema novo: convergência no GNS

[DERIVED; prova Lean nova] Definir a média vetorial T⁻¹∫₀ᵀ U(t)v dt e provar a cota de contração ‖média(v)‖≤‖v‖. Em vetores locais, o limite anterior é o pinching. A densidade towerPre_denseRange e a cota uniforme tornam as médias uma sequência de Cauchy para qualquer v; a completude dá o limite.

Para v=AΩ, a igualdade U(-t)Ω=Ω identifica essa média com C_n(A)Ω. Não basta a cota ‖C_n(A)‖≤‖A‖ para aproximar AΩ por vetores locais: usa-se explicitamente a cota de contração da média VETORIAL.

### 4.3 Parede tipada do levantamento limitado

O seguinte é um ALVO NOVO, não um lema existente com esse nome:

```lean
-- Esquema de assinatura; não compilado nesta revisão.
bounded_omega_limit_lift
  (P : SiteProfile)
  (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
  (bound : ℝ) (hbound : 0 ≤ bound)
  (hmem : ∀ n, C n ∈ theFactorObject P)
  (hnorm : ∀ n, ‖C n‖ ≤ bound)
  (z : TowerHilbert P)
  (hz : Tendsto (fun n => C n (hOmega P)) atTop (𝓝 z)) :
  ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
    B ∈ theFactorObject P ∧ ‖B‖ ≤ bound ∧
    B (hOmega P)=z ∧
    ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v))
```

Justificação construtiva: em v=rTowerPi y Ω, a comutação dá C_n v=rTowerPi y(C_nΩ), que converge. Esses v contêm todos os vetores locais pelo rTowerPi_omega. A cota uniforme estende a propriedade de Cauchy a qualquer vetor; a completude produz um limite pontual. Então ofTendstoOfBoundedRange empacota B. Passar as relações de comutação ao limite forte põe B no bicomutante que DEFINE theFactorObject. A cota passa ao limite. A separância garante unicidade de B pelo valor BΩ.

Portanto não se está identificando arbitrariamente um vetor Hilbert com um operador limitado: são as médias limitadas em M e a ação direita densa que justificam essa identificação.

### 4.4 Fechar exatamente os três campos do contrato

[DERIVED; provas Lean novas] O limite das médias em cada corte deve dar:

```
towerExpectation P N (E A)
  = towerPi P (specExpect (towerW P N) (expectationMatrix P N A)),  A∈M.
```

A igualdade segue comparando ações em Ω: expectation_omega identifica a esquerda com levelProject; a continuidade deste e o limite finito identificam o limite; factor_eq_of_omega fecha a igualdade de operadores.

Depois:
1. into: pinching_into_global_centralizer em cada corte e centralizer_from_expectations.
2. fixes: pinching_fixes_global_local, expectation_of_centralizer_is_centralizer e expectation_omega_limit; a prova periódica já exibe o argumento.
3. ortho: pinching_global_ortho em cada corte, depois limite do produto interno por expectation_omega_limit; novamente é o argumento da prova periódica, agora usando a nova identidade prefixal.

A escolha de E em M vem do levantamento único. Fora de M pode-se usar zero. Nenhum TakesakiInput.expectation é pressuposto em nenhum desses passos.

## 5. Propriedades adicionais: normalidade e positividade completa

[KNOWN — existência matemática] O teorema de Takesaki estabelece a existência de projeção normal fiel de norma1 preservando o peso quando a subálgebra é modularmente invariante e a restrição do peso é semifinita. Para um estado fiel normal, a restrição ao centralizador é finita; o centralizador é fixo pelo grupo modular. Assim a existência não depende de periodicidade. Fonte primária: Masamichi Takesaki, “Conditional expectations in von Neumann algebras”, JFA9(3),306–321(1972), [DOI editorial](https://doi.org/10.1016/0022-1236(72)90004-3). O resumo editorial foi recuperado pela busca; a abertura direta da página retornou403. Não foi lido o artigo integral nesta revisão.

[DERIVED — obrigações além do registro mínimo] Para a RESTRIÇÃO E:M→M da construção:
- Linearidade, unidade, preservação do adjunto e preservação de ω devem ser provadas passando as correspondentes identidades das médias ao limite; idempotência vem de into+fixes.
- Positividade completa exige, para cada tamanho matricial, que a amplificação das médias preserve positividade e que essa positividade passe ao limite de operadores em Hⁿ. A estrutura CompletelyPositiveMap existe, mas sua instanciação para este E não foi feita.
- Normalidade não decorre apenas da frase “limite de mapas normais”. Uma prova disponível em matemática é: para A_i↑A positivos, positividade dá E(A_i)↑B≤E(A); preservação de um estado fiel NORMAL dá ω(E(A)−B)=ω(A)−sup_iω(A_i)=0; fidelidade implica B=E(A). Isso requer formalizar os supremos monotônicos na álgebra e a normalidade plena do estado, além de suas hipóteses de limitação. omegaState_seqWOT, isoladamente, não substitui essas obrigações.

[OPEN] A formalização dessas propriedades adicionais deve ser registrada separadamente da obtenção de ExpectationInput. A projeção Hilbert é uma etapa da construção, não um certificado automático de normalidade/CP.

## Próximo alvo delimitado

Pagar primeiro o limite escalar Cesàro e sua versão flowLevel, sem LocalPhasePeriod. Em seguida, desenvolver bounded_omega_limit_lift com RightMult e a cota já existente. Esse caminho ataca diretamente o habitante geral do contrato; não exige acrescentar postulado físico, nem confundir centralizador com diagonal ou com toda a álgebra. Esta nota não inicia código046 e não altera o lote045.
