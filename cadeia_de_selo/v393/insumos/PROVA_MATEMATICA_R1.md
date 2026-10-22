# Prova do contrato da regra e da satisfação

Unidade F1.REGRA.P1. Autoria das cunhagens: Luiz Antonio Rotoli Miguel. Construção formal: codex-gerente-tgl e subagente v392_scope; revisão independente: modular_final_review. Data: 14/10/2026.

## 1. Enunciado que foi formalizado

[INPUT — representação matemática] Fixamos um espaço de inscrições N, uma leitura r:N→O, um objeto devido a∈N e sua figura o=r(a). A leitura é injetiva **nesse espaço**. Uma regra é um predicado C:N→Prop.

As duas exigências são declaradas:

1. **Correção:** C(z) implica r(z)=o. Uma satisfação falsa é inadmissível.
2. **Completude relativa ao objeto:** r(z)=o implica C(z). O critério não acrescenta outra exclusão à correspondência especificada.

A segunda exigência é a representação escolhida para o alcance de «a não ser a figura da verdade». Ela é hipótese explícita da caracterização, não uma conclusão extraída somente do nome. A leitura e o objeto são fixados antes da comparação.

## 2. Teorema da regra

[REAL — prova formal em sandbox] Sob as condições acima,

\[
\boxed{C(z)\iff z=a.}
\]

Consequentemente, o predicado C é único para essa leitura e esse objeto.

**Prova.** Se C(z), a correção dá r(z)=o=r(a). Pela injetividade de r no espaço N, z=a. Reciprocamente, se z=a, então r(z)=r(a)=o; pela completude, C(z). As duas implicações determinam C ponto a ponto; extensionalidade dá a igualdade dos predicados. ∎

Fontes formais: `RuleTruthContract.sound_complete_eq_admissible`, `admissible_iff_eq_of_injective` e `RuleSatisfactionFace.unique_rule_on_inscriptions`.

Sem completude, a correção permite regras mais restritivas, inclusive rejeitar tudo. Sem injetividade, igualdade das leituras pode ocultar diferença entre os objetos. A prova mantém essas duas condições visíveis.

## 3. Operação e quitação

[REAL — prova formal em sandbox] Sejam R:Y→Y uma retração e ρ:Y→O uma leitura preservada por ela:

\[
R^2=R,\qquad \rho(Ry)=\rho(y).
\]

A admissibilidade por essa leitura é preservada por R. Toda releitura posterior devolve R(y). O resultado tem tipo

\[
N=\operatorname{Fix}(R)=\{y:R(y)=y\}.
\]

A leitura r do teorema é a restrição de ρ a N. Assim podemos confrontar o resultado inscrito com o objeto devido dentro do mesmo tipo. A igualdade literal é demonstrada nesse tipo, sem usar uma leitura que confunda seus elementos.

`repeat_reading_adds_nothing` aplica o termo existente `TGLExt.res_judicata_is_terminal`. A idempotência e a preservação da leitura são condições diferentes, ambas demonstradas no exemplo.

## 4. Realização concreta, sem vacuidade

[INPUT — modelo de face finita] Em Y=ℝ², definimos

\[
R(a,b)=(a,0),\qquad T_\lambda(a,b)=(a,\lambda b),\qquad
\lambda=e^{-1/2},\qquad x_0=(1,1),\qquad a_*=(1,0).
\]

O fator da meia-nat vem do lema existente `the_half_nat_gives_a_strictly_interior_factor`: 0<λ<1. Não é identificado com β_TGL.

[REAL — provas formais]

\[
R^2=R,\qquad RT_\lambda=T_\lambda R=R,
\]

\[
T_\lambda^n(a,b)=(a,\lambda^n b),\qquad
T_\lambda^n(a,b)\longrightarrow R(a,b).
\]

O limite usa o teorema existente de convergência de potências do mathlib. O parâmetro da face sofre contração real; não se pede limite a uma órbita angular.

No estado escolhido, o objeto é preservado e a operação é efetiva:

\[
a_*\ne0,\quad R(x_0)\ne x_0,\quad T_\lambda(x_0)\ne x_0,
\qquad R(T_\lambda^n x_0)=a_*.
\]

A função `inscribe` devolve o subtipo `Inscription=Fix(R)`; `typed_operation_satisfies` prova igualdade literal com `dueObject`. A leitura da primeira coordenada é injetiva nesse subtipo.

**Limite de alcance demonstrado:** para todo n finito,

\[
T_\lambda^n x_0\ne a_*.
\]

A segunda coordenada continua estritamente positiva. Portanto o resultado bruto da trajetória não é apresentado como quitação exata em tempo finito. A igualdade exata pertence à operação explicitamente normalizada R∘Tⁿ; a trajetória bruta converge ao alvo.

## 5. Ligação efetiva às pedras existentes

[REAL — composição de termos]

- `TheJudgedThing`: idempotência e releitura; `tetelestai_ledger` dá 0<λ, 0<1−λ e λ+(1−λ)=1. É balanço escalar, sem alegação de energia medida.
- `TheNonMinimalCoupling`: as matrizes P=diag(1,0) e Q=diag(0,1) satisfazem P+Q=I, PQ=0, P²=P, P≠0 e Q≠0. `normalization_is_left_face` identifica por termo P aplicado às coordenadas complexas com R. `nonminimal_split_applies_to_this_reading` aplica o lema existente da partição própria às mesmas matrizes. Não se usa um nome como substituto dessa ponte.
- `TheGeometricCostOfAbsoluteZero`: fornece o fator estritamente interior e^{−1/2}.
- `TheLedgerOfCharges`: a independência entre `ruleGiven` e o livro de desfechos é reutilizada com seu alcance original, por construção. Esse termo não demonstra uma verdade universal nem que todo pagamento concreto esteja realizado.

## 6. Controles negativos provados

1. Uma leitura constante pode ser idempotente e falhar para todo resultado comparado com outro alvo.
2. Duas entradas diferentes podem ter a mesma leitura quando ela não é injetiva.
3. Se a leitura fosse globalmente injetiva e R a preservasse, então R=id. A redução efetiva exige distinguir o espaço bruto do espaço da inscrição.
4. O estado (0,1) projeta-se em zero e é recusado para o alvo (1,0). A não aniquilação demonstrada é do alvo admissível; não vale para todo input e não é um teorema termodinâmico sobre zero absoluto.
5. Há uma operação que satisfaz e outra que falha sob o mesmo critério. A ocorrência de um resultado divergente não muda o predicado da regra nem constitui sua satisfação.
6. O limite da trajetória não autoriza declarar igualdade bruta antecipada em n finito.

## 7. O alcance exato da prova

[REAL] A caracterização lógica e o modelo concreto estão demonstrados em Lean. Foram construídos 60 enunciados `theorem` nos dois módulos. Os relatórios adicionais de axiomas incluem repetições e constantes auxiliares; não contam como novos teoremas. As tentativas e seus logs permanecem em `attempts/`, sem sobrescrita.

[REAL — reprodução independente] Os três módulos recompilaram com EXIT 0, sem `sorry` e com axiomas somente em `propext`, `Classical.choice` e `Quot.sound`. Dois dos três arquivos `.olean` coincidiram byte a byte; o módulo concreto teve bytes diferentes, com a mesma fonte e os mesmos relatórios de axiomas. A causa dessa diferença binária não foi determinada. O recibo independente registra essa limitação; não se alega reprodução binária integral.

[INPUT/ONTO] A representação de «figura da verdade» por leitura fiel e objeto fixado, e sua identificação com direito, pagamento e Tetelestai, permanecem explicitadas como interpretação. A unicidade demonstrada é a do critério **para essa leitura e esse alvo**, não a unicidade de toda interpretação possível.

[ESCOPO] A satisfação normalizada já vale em n=0 e não depende de λ. O fator λ sustenta a evolução, o limite e o balanço; não produz a verdade do critério. Nenhuma dinâmica física nova, medição, confirmação da natureza, alteração de kernel canônico ou gate decorre desta prova.

Os originais verbatim e seus hashes estão em `VERBATIM_MANIFEST.json`; as quatro inscrições integrais também estão na docstring de `TheRuleAndTheFigureOfTruth.lean`. O resultado final da unidade identifica build, revisão independente, fontes, hashes e registro de memória.
