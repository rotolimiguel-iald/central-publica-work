# Admissibilidade dos contratermos e covariância de fundo

09/09/2026, continuidade 070. [DERIVED — precisões e demonstrações escritas]. A classe usada no certificado de igualdade fraca não deve ser imposta indiscriminadamente à primitiva de uma anomalia. Esta nota distingue os dois problemas e fornece operações explícitas que preservam condições pertinentes, sem declarar Q3 satisfeito.

## 1. Três exigências distintas

Uma identidade característica como `Euler≈d beta` testa uma primitiva beta tensorial natural do campo completo, sem conexão de referência adicional. Essa restrição é parte essencial do teste C0 de 068–069. Permitir uma forma de Chern–Simons não tensorial mudaria esse teste.

Uma renormalização que cancela a quebra de gauge exige `a=sB+dD`. O contratermo B não deve ser obrigado, antes da construção, a ser invariável pelo mesmo gauge que a quebra viola. Na construção causal com fundo externo, a condição apropriada é naturalidade sob transporte **simultâneo dos dados de fundo e dos campos**, além das condições de suporte, realidade e ordem local. O BRST quântico mantém o fundo fixo e atua nos campos dinâmicos. As duas operações são diferentes.

[DERIVED] Para ver a diferença sem analogia, tome uma 4-forma B(g,phi) sem antifields, covariante sob difeomorfismos dos campos completos e sem outro dado externo. Sob o BRST de difeomorfismos, `sB=Lie_C B`. A identidade de Cartan em dimensão quatro dá

\[
sB=d\,\iota_C B\quad\text{módulo a convenção de sinais graduados}.
\]

Logo sB é zero no quociente módulo d. Esse subespaço, sozinho, não remove uma quebra que tenha classe de forma não nula módulo d antes da variação. A afirmação não exclui contratermos com antifields nem aqueles dependentes do fundo, e não afirma que uma quebra específica seja não removível.

O coeficiente de calor C4 é uma densidade de ghost zero, e seus representantes covariantes não têm o mesmo papel de uma primitiva B de ghost zero cuja variação cancela uma inserção de ghost um. Não confundir classificação de operadores invariantes com classificação de todas as renormalizações admissíveis.

## 2. Exemplo tensorial explícito usando duas conexões

Considere duas conexões A e Abar no mesmo fibrado, com curvaturas F e Fbar, e uma forma bilinear invariante denotada por tr. Ponha a=A−Abar e A_t=Abar+t a. A diferença a é tensorial sob transformações simultâneas das duas conexões. Como

\[
F_t=\bar F+t\bar D a+t^2a\wedge a,
\]

defina

\[
T_3(A,\bar A)=2\int_0^1\mathrm{tr}(a\wedge F_t)\,dt
=\mathrm{tr}\left(2a\wedge\bar F+a\wedge\bar D a+\frac23a^3\right).
\tag{1}
\]

Todos os termos são locais de ordem finita e se transformam tensorialmente sob transporte simultâneo. Pela identidade de Bianchi D_t F_t=0 e pela invariância do pareamento,

\[
\frac{d}{dt}\mathrm{tr}(F_t^2)
=2\mathrm{tr}(D_t a\wedge F_t)
=2d\,\mathrm{tr}(a\wedge F_t).
\]

Integrar essa identidade prova

\[
dT_3=\mathrm{tr}(F^2)-\mathrm{tr}(\bar F^2).
\tag{2}
\]

[KNOWN — referência primária] A transgressão entre duas conexões, sua relação com as formas de Chern–Simons e a invariância **simultânea** são apresentadas em [Mora–Olea–Troncoso–Zanelli, §2, (2.1)–(2.4)](https://arxiv.org/pdf/hep-th/0601081). Aqui usamos somente a identidade local (1)–(2), não os resultados de gravidade AdS ou termodinâmica desse artigo.

Se alpha é uma 1-forma suave no alvo, então `phi*alpha∧T3` é uma 4-forma local covariante nos dois conjuntos de dados. Sob gauge quântico que transforma A e mantém Abar fixo, T3 não está obrigado a ser invariável. Isso mostra concretamente como uma densidade natural de fundo pode ter variação quântica não trivial. A conexão externa e sua curvatura continuam declaradas; elas não desapareceram da identidade (2).

**Limite:** construir T3 não demonstra que uma anomalia específica seja a variação desse contratermo. Para tal conclusão, é preciso comparar os representantes e seus termos de descida, incluindo os termos de fundo. Tampouco (2) fornece uma primitiva tensorial de tr(F²) sem o termo de fundo. O teste C0 anterior permanece inalterado.

## 3. Preservação de simetrias rígidas compactas

[DERIVED — lema condicional útil] Suponha que uma classe admissível de formas locais seja estável pela ação de um grupo compacto G, que s e d comutem com essa ação e que uma anomalia a seja G-invariante. Se existem primitivas admissíveis B,D com a=sB+dD, então existem primitivas G-invariantes, desde que a classe seja estável pela média de Haar:

\[
\bar B=\int_G g\cdot B\,d\mu(g),\qquad
\bar D=\int_G g\cdot D\,d\mu(g),\qquad
a=s\bar B+d\bar D.
\tag{3}
\]

Para campos globais no alvo S³, a ação rígida O(4) transporta suavemente os jatos e preserva a ação Einstein–sigma. A média não aumenta a ordem de jato nem o suporte espaço-temporal. Em grau perturbativo fixado, os jatos e tensores de fibras têm ordem finita; a média de seus coeficientes suaves permanece suave. Assim essa operação é admissível no espaço global suave natural pertinente. Uma primitiva definida só numa carta do alvo ainda precisa ser globalizada antes de aplicar a média do grupo inteiro; não se integra uma expressão fora do seu domínio.

O lema não resolve a existência de B,D e não usa média sobre o grupo não compacto de Lorentz ou sobre difeomorfismos. Para uma condição de realidade, uma projeção antilinear análoga só é legítima depois de verificar sua compatibilidade com s,d e com as convenções graduadas do dicionário BV. A presença de uma ação clássica real não substitui essa conferência no complexo gauge-fixado.

## 4. Consequência para o trabalho de Q3

O espaço de primitivas deve ser o mesmo permitido pela construção causal de Q2. Deve admitir transformações canônicas locais, termos com antifields quando necessários e dependência natural nos dados de fundo declarados. Uma eventual exigência adicional de independência de fundo deve ser provada separadamente; não pode ser obtida apenas renomeando covariância simultânea.

A análise do alvo S³ pode eliminar candidatos por grau ou exatidão de formas de alvo. Se uma etapa usar Chern–Simons, deve dizer se a conclusão vive na álgebra local usual, numa apresentação de fundo por transgressão ou no subcomplexo estritamente invariante. A passagem entre essas classes é trabalho matemático, não troca de nomenclatura.

[OPEN] Ainda é necessário mostrar que toda quebra produzida no modelo pertence ao setor cohomológico controlado e possui primitiva com os requisitos de Q2. As operações desta nota fornecem comparações e preservações úteis, não uma declaração de ausência de anomalias.

Somente arquivo novo em Chatgpt; zero CAS, Lean, execução de um.py, alteração de originais ou mudança de gate.
