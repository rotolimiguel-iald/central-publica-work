# Consulta — resolventes racionais e quadrados no gráfico do F original

2026-09-13T04:11:24.335312-03:00

[DERIVED — argumento matemático abaixo, ainda não formalizado nesta consulta.] A rota funciona para operador limitado auto-adjunto a e dispensa PVM. Adoto o índice n+1 sugerido pelo agente principal e sua identidade energética, combinada com o limite forte antítono de `PositiveResolvent`. A cota mais forte já presente em `DualResolvent` é uma alternativa, não uma dependência obrigatória. Não é necessário construir novas raízes ou identificar o limite em todo H como uma projeção.

[REAL — inspeção de fontes.] Nenhum Lean, monólito, teste autoral ou recorder foi executado. Não há novo certificado DEV nem auditoria de axiomas nesta consulta. Fontes lidas e hashes medidos em consulta_resolvente_racional_pins_20260913_041124_335312.json (SHA256 b8438b7dcaf58db5b429ca6ffc8e53cc37345ea708bf4b909386300f80815e19). A custódia mãe foi apenas pinada; pareceres e memórias permanecem intactos.

## 1. Lema genérico que reduz a obrigação

Seja H Hilbert complexo completo, a∈B(H), a*=a. Para n∈ℕ, ponha

    R_n = positiveResolvent (((n:ℝ)+1) • (a*a)) = (I+(n+1)a²)^−1.

Aqui a*a é composição de a consigo mesmo, não notação para adjunto vezes a; a auto-adjunticidade é a hipótese que dá a²≥0. Não é necessário a≥0, injetividade, gap, separabilidade nem D(a)=H como hipótese extra: a já é CLM limitado.

Os lemas existentes dão 0≤R_n≤I, antitonia e existência de CLM L com R_n v→Lv para todo v. Aplicar `vonNeumann_antitone_contraction_limit` a N=⊤ serve para o lema genérico; na aplicação pode-se usar o comutante concreto. A sequência ℕ é dirigida e não vazia, sem hipótese residual de convergência forte.

Como a comuta com I+(n+1)a², também comuta com sua inversa. A hipótese IsUnit necessária vem de `one_add_strictlyPositive`. Escrevendo r=R_n v, a equação da inversa e a contração ||R_n||≤1 dão

    ||r||²+(n+1)||ar||² = Re⟨r,v⟩ ≤ ||r|| ||v|| ≤ ||v||²,
    portanto (n+1)||R_n a v||² ≤ ||v||².               (E)

A igualdade quadrática usa a*=a e a convenção do produto interno complexo, sem descartar parte imaginária não justificada: Re⟨r,a²r⟩=||ar||². A cota ||R_n||≤1 decorre de 0≤R_n≤I; usar ||I||≤1 evita impor Nontrivial H. Se conveniente, o lema já existente `positiveResolvent_energy_bound`, com C=(n+1)a², melhora o lado direito de (E) para ||v||²/4. Essa constante ótima é desnecessária aqui.

Uma prova de limite adequada à biblioteca evita até raízes e divisão por n: fixe k>0. Para n≥k, (E) dá k||R_n av||²≤||v||². Passe ao limite forte já construído: k||Lav||²≤||v||² para todo k natural positivo. A propriedade arquimediana força Lav=0. Como ker L é fechado, L anula closure(Ran a). Logo

    x ∈ closure(Ran a)  ⇒  R_n x → 0.                 (R)

O índice n+1 é positivo desde o primeiro termo. Alternativamente (E) dá ||R_n av||≤||v||/√(n+1), e a cota uniforme ||R_n||≤1 estende a convergência por densidade. A primeira prova reaproveita diretamente o limite antítono existente, sem desenvolver um novo teorema de extensão por densidade. Também é válido obter aL=0 passando pela continuidade de a e depois La=0 pela comutação no limite; trabalhar diretamente com R_n av economiza essa última passagem.

**Economia formal frente à rota CFC.** A versão acima usa a ordem dos inversos, o limite forte já disponível, uma identidade de produto interno e um argumento arquimediano. Evita construir g_ε por CFC, transportar fórmulas escalares entre espectros e provar a estimativa de supremo √ε/2. A pertença ao comutante ainda usa `positiveResolvent_mem`, cuja prova existente já tem sua infraestrutura CFC; trata-se de evitar CFC novo, não de eliminar suas dependências transitivas. Os resolventes racionais podem igualmente ser escritos com ε=1/(n+1), mas essa reparametrização não ajuda o alvo atual.

**Limites necessários.** Em ker a vale R_n x=x; portanto (R) não se estende a todo H sem hipótese adicional. Tampouco há convergência em norma de operador em geral: em ℓ², a e_k=k^−1 e_k (k≥1) é limitado, auto-adjunto e injetivo, mas ||R_n||=1 para cada n. Se a não fosse auto-adjunto, substituir a² por a* a mudaria o suporte relevante para closure(Ran a*); não reutilizar a conclusão com Ran a silenciosamente.

## 2. Aplicação à álgebra direita existente

Fixar H=ScalarGNSHilbert P, M=π(N), E=scalarPairedRightAlgebra P, j=scalarRightPairVector P e F=scalarTomitaAdjoint P original. Para a=a*∈E, v=j(a), duas pontes novas devem ser efetivamente formalizadas — são precisamente as anunciadas pelo principal:

1. Se T=T*∈M′ e Ta=aT, então Ta∈E é auto-adjunto e j(Ta)=Tv. Para provar, tomar o par de a com ambos os vetores iguais a v; as identidades são TaΛ(b)=Tπ(b)v=π(b)Tv e (Ta)*=Ta. A unicidade de vetor identifica j(Ta). T não precisa pertencer a E.
2. v∈closure(Ran a): para h>0, π(average_h)v=aΛ(average_h), enquanto π(average_h)v→v. Cada vetor à direita pertence a Ran a. Não se exige cota uniforme dos vetores Λ(average_h).

O resolvente R_n pertence a M′ por `positiveResolvent_mem`, é auto-adjunto positivo e comuta com a. Não se deve afirmar R_n∈E: E não é unital. A ponte 1 dá b_n=R_n a∈E e j(b_n)=R_n v. Defina dentro de E

    d_n = (n+1) a b_n,
    c_n = a d_n.

Como operadores limitados, a equação da inversa dá d_n=(n+1)a²R_n=I−R_n. Essa igualdade ambiente prova a pertinência de I−R_n em E via o produto já construído; não pressupõe I∈E. Todos a,b_n,d_n,c_n são auto-adjuntos e comutam entre si. Pela lei j(ab)=a j(b),

    j(c_n)=(n+1)a²R_n v=(I−R_n)v → v.

E, crucialmente, há a identidade algébrica exata

    c_n = ¼[(a+d_n)² − (a−d_n)²].                    (Q)

Os dois fatores a±d_n pertencem a E e são auto-adjuntos. Como F j(c_n)=j(c_n) e Fv=v, a aproximação ocorre também no gráfico original: (j(c_n),Fj(c_n))→(v,Fv). Nenhuma continuidade limitada de F foi usada.

## 3. Alcance exato de “quadrados graphdense”

Da identidade (Q), a **envoltória linear real** dos vetores j(b²), b=b*∈E, tem fecho igual a Fix F: primeiro aproxima cada j(a) auto-adjunto; depois usa `scalarRightSelfadjointVectors_closure`. Não é afirmação de densidade do cone de somas positivas de quadrados, nem de um único quadrado.

Se L_alg é a envoltória complexa, dentro de E, dos quadrados desses elementos auto-adjuntos, então

    closure { (j(c), j(c*)) : c∈L_alg } = graph F.     (G)

Para verificar a passagem, escreva x=u+i v em D(F), com u,v∈Fix F, e aproxime u,v separadamente por combinações reais de quadrados. Os pares aproximantes são (u_n+i v_n,u_n−i v_n), não (u_n+i v_n,u_n+i v_n). O gráfico de F é real-linear, não complexo-linear; esta conjugação dos coeficientes é essencial. A inclusão oposta em (G) vem da propriedade existente de j e do fechamento de F.

F†=S não é necessário para (R), (Q) ou (G). Será necessário depois, se o objetivo for estender um pareamento de teste nos quadrados e concluir pertinência ao domínio do S original. O principal informou rc0 desse novo módulo; não li nem auditei a fonte nova nesta consulta. Esta consulta não prova o pareamento ponderado, a estimativa de multiplicador, a inclusão inversa dos comutantes, KMS, traço ou qualquer flag.

## 4. Interfaces exatas e sequência sugerida

Todas abaixo foram localizadas nas fontes atuais, no namespace TGLV350.Regular salvo indicação:

| Interface existente | Arquivo/linha | Uso |
|---|---|---|
| `positiveResolvent`, inversas, positividade, cota por I, antitonia | `kernel/TGLV350/PositiveResolvent.lean:16` | R_n positivo e antítono |
| `positiveResolvent_mem` | `kernel/TGLV350/PositiveResolvent.lean:51` | R_n no comutante concreto |
| `vonNeumann_antitone_contraction_limit` | `kernel/TGLV350/PositiveResolvent.lean:73` | existência do limite CLM L |
| `positiveResolvent_energy_bound` | `kernel/TGLV350/DualResolvent.lean:75` | alternativa com constante 1/4, genérico em H apesar do nome do módulo |
| `ring_inverse_commutes_of_unit` | `kernel/TGLV350/ScaledPositiveResolvent.lean:47` | comutação aR_n=R_na; IsUnit explícita |
| `scalarGNSAverage_tendsto` | `kernel/TGLV350/ScalarRightAdjointPair.lean:34` | suporte de j(a), restringindo h→0 a h>0 |
| `scalarRightPairVector_of_pair`, `scalarRightPairVector_mul` | `kernel/TGLV350/ScalarRightPairVector.lean:67` e `:79` | identificar vetores e produtos |
| `scalarRightPairVector_original_adjoint` | `kernel/TGLV350/ScalarRightPairVector.lean:89` | gráfico do mesmo F |
| `scalarRightSelfadjointVectors_closure` | `kernel/TGLV350/ScalarRightGraphCore.lean:43` | fechar a densidade real |
| `scalarRightPairGraph_closure_eq_original` | `kernel/TGLV350/ScalarRightGraphCore.lean:60` | referência do gráfico já construído |

`bounded_application_tendsto`, em `StrongBoundedApplication.lean`, não é, sozinho, um lema de extensão da convergência a partir de um subconjunto denso: já recebe convergência sobre o vetor fixo. Não é necessário para a prova acima.

Próximos enunciados concretos, ainda propostos: (i) comutação e (E) para R_n; (ii) (R), por limite antítono e núcleo fechado; (iii) estabilidade de pares e suporte de j(a), sem campos adicionais; (iv) construção explícita b_n,d_n,c_n e (Q); (v) densidade real dos quadrados e (G). A cadeia reduz a obrigação a lemas limitados e álgebra elementar, sem importar uma hipótese de graph-core dos quadrados.

**Diagnóstico:** não identifiquei obstáculo matemático nesta rota com as hipóteses acima. A conclusão sobre quadrados permanece [DERIVED], pendente das novas provas Lean; a inspeção desta consulta não aceita fontes futuras nem modifica o estatuto do pacote custodiado.


Errata de referência (20260913_041151_564852): `positiveResolvent_energy_bound` é declarado na linha **74** de `kernel/TGLV350/DualResolvent.lean`; a linha 75 indicada na tabela é a continuação do enunciado. A referência foi conferida por busca literal após a emissão. Argumento e pins inalterados.
