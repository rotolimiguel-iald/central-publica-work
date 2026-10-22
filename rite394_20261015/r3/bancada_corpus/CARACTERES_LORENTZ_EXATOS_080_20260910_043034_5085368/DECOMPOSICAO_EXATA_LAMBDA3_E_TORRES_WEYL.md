# Caráter exato de Λ³Wg e sua sobreposição com os tipos de Weyl

10/09/2026, investigação080, separada da entrega079. [REAL — aritmética inteira executada em Python puro]. [DERIVED — interpretação dos caracteres finitos]. Nenhum SymPy, Lean, um.py ou fonte externa executado/importado; nenhum arquivo079 ou original alterado.

**Resultado.** Com pesos inteiros iguais a 2j para sl2(C)×sl2(C), a decomposição calculada é

\[
\begin{aligned}
\Lambda^3W_g\cong{}&(4,0)\oplus(0,4)\oplus(2,0)\oplus(0,2)
\oplus4(0,0)\oplus4(2,2)\\
&\oplus(3,3)\oplus2(3,1)\oplus2(1,3)\oplus4(1,1).
\end{aligned}
\tag{1}
\]

A dimensão é 120. A comparação com os tipos (4+r,r) e (r,4+r), r inteiro não negativo, encontra somente r=0, com multiplicidade um para cada quiralidade COMPLEXA. O cálculo não identifica qualquer torre de jatos físicos com esses tipos e não classifica H³(s0) de valência quatro.

## 1. Entradas e construção sem tabela de decomposição

[INPUT] O problema finito é o módulo

\[
W_g=V\oplus\Lambda^2V=(1,1)\oplus(2,0)\oplus(0,2).
\tag{2}
\]

O módulo (a,b) tem pesos (a−2i,b−2j), com 0≤i≤a e 0≤j≤b, cada qual uma vez. Isso fixa as dez entradas da base de pesos de Wg:

\[
(1,1),(1,-1),(-1,1),(-1,-1),
(2,0),(0,0),(-2,0),(0,2),(0,0),(0,-2).
\tag{3}
\]

Os dois vetores de peso (0,0) são DISTINTOS. Um cálculo que primeiro eliminasse a multiplicidade do zero perderia parte da potência exterior.

O [script executado](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/compute_lorentz_characters080.py>) enumera todas as escolhas de três ÍNDICES distintos da lista (3), soma seus pesos e acumula as multiplicidades em inteiros. Há exatamente binom(10,3)=120 escolhas. A proposta manual da raiz só entra no script DEPOIS de a decomposição ser calculada, como comparação separada; não determina o resultado da enumeração ou da redução.

Equivalentemente, se x,y denotam as variáveis do caráter do toro, χΛ3 é o coeficiente de t³ do produto COMPLETO

\[
\left[\prod_{\epsilon,\delta=\pm1}(1+t x^\epsilon y^\delta)\right]
(1+tx^2)(1+t)(1+tx^{-2})
(1+ty^2)(1+t)(1+ty^{-2}).
\]

Há dez fatores lineares em t, incluindo duas cópias de (1+t). O parâmetro t nesta identidade é somente o contador da potência exterior, não uma identificação com o parâmetro de Rees do complexo BRST.

## 2. Verificação independente por Newton e extração dos maiores pesos

Se χ=χWg e ψmχ substitui (x,y) por (x^m,y^m), a identidade simétrica de grau três dá

\[
\boxed{6\chi_{\Lambda^3W_g}
=\chi^3-3\chi\,\psi_2\chi+2\psi_3\chi.}
\tag{4}
\]

Ela pode ser vista sem tabela: em χ³, triplas de índices distintos aparecem seis vezes; as repetições de dois índices são canceladas por −3χψ2χ; as três ocorrências de um mesmo índice ficam com coeficiente 1−3+2=0. O script calcula convoluções de caracteres, verifica divisibilidade inteira por seis em cada peso e confronta o resultado com a enumeração exterior. Os dois métodos coincidiram em TODOS os coeficientes.

Para decompor o caráter calculado, o algoritmo toma o peso lexicograficamente máximo restante, subtrai sua multiplicidade vezes o caráter retangular do módulo de maior peso correspondente e repete. Todos os maiores pesos encontrados são dominantes e todos os restos permanecem não negativos. A reconstrução final soma os caracteres dos módulos obtidos e reproduz exatamente o caráter inicial.

Essa eliminação é legítima porque, num módulo finito de sl2×sl2, um peso máximo lexicográfico é anulado pelos dois operadores de levantamento: qualquer levantamento produziria peso lexicograficamente maior. A completa redutibilidade finita permite retirar as cópias do módulo desse maior peso. A reconstrução exata constitui ainda uma identidade de caracteres verificável independentemente da implementação da retirada; os caracteres irredutíveis são linearmente independentes pelos seus maiores pesos.

## 3. Resultado por tipo e dimensão

O [recibo inteiro](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json>) contém o caráter completo, todos os passos de retirada e os controles. A tabela extraída é:

| Maior peso (a,b) | Multiplicidade | Dimensão de (a,b) | Contribuição |
|---|---:|---:|---:|
| (0,0) | 4 | 1 | 4 |
| (0,2) | 1 | 3 | 3 |
| (0,4) | 1 | 5 | 5 |
| (1,1) | 4 | 4 | 16 |
| (1,3) | 2 | 8 | 16 |
| (2,0) | 1 | 3 | 3 |
| (2,2) | 4 | 9 | 36 |
| (3,1) | 2 | 8 | 16 |
| (3,3) | 1 | 16 | 16 |
| (4,0) | 1 | 5 | 5 |
| Total | | | 120 |

A soma usa dim(a,b)=(a+1)(b+1). As reflexões independentes dos dois sistemas de pesos e a troca das duas quiralidades preservam o caráter calculado; esses controles também passaram.

Em notação por spins, por exemplo, (4,0) significa (jL,jR)=(2,0), e (3,1) significa (3/2,1/2). O cálculo não troca essas duas convenções durante a comparação.

## 4. Comparação com TODAS as ordens r das torres propostas

[INPUT para esta comparação] Considere as famílias de tipos

\[
\mathcal W_r^+=(4+r,r),\qquad
\mathcal W_r^-=(r,4+r),\qquad r\ge0.
\tag{5}
\]

O maior primeiro peso do caráter exterior é 4 e o maior segundo peso também é 4. Isso é medido a partir de (3), não inferido de um corte arbitrário em r. Se r≥1, o maior peso de W_r^+ teria primeira coordenada pelo menos 5, e o de W_r^- teria segunda coordenada pelo menos 5. Nenhum pode ocorrer. Logo

\[
\operatorname{mult}_{\Lambda^3W_g}(4+r,r)
=\operatorname{mult}_{\Lambda^3W_g}(r,4+r)
=\begin{cases}1,&r=0,\\0,&r\ge1.\end{cases}
\tag{6}
\]

A conclusão sobre r≥1 cobre toda a família infinita por uma desigualdade de pesos; o script não se limita a testar algumas ordens pequenas. Como os módulos finitos irredutíveis de sl2 são autoduais, o mesmo número é a dimensão do espaço de emparelhamentos invariantes de cada tipo (5) com Λ³Wg, no problema PURAMENTE REPRESENTACIONAL. Isso não transforma automaticamente um emparelhamento de módulos em uma classe natural de jatos.

## 5. O contrato que este recibo NÃO paga

Não foram demonstrados neste diretório: a exatidão do complexo de Calabi, a fatorização de operadores de gauge, a identificação do quociente on-shell de jatos de Einstein com uma soma dos tipos (5), a eliminação triangular de derivados, a passagem a invariantes naturais com coeficientes herdados ou uma comparação entre esse módulo finito e o complexo BRST.

Essas são entradas separadas para qualquer inferência sobre H³(s0)E4. O resultado (6) é utilizável DEPOIS de demonstrar que os jatos relevantes fornecem somente essas torres, no domínio e no anel corretos. Não confirma por si a afirmação de que W[1]CCm e seu dual geram todas as classes, nem promove a exclusão específica079 a uma exclusão de todos os levantamentos.

As duas quiralidades em (6) são os tipos complexos da álgebra Lorentz complexificada. Nenhuma decomposição em dois espaços reais independentes de Weyl foi presumida. A eventual passagem aos dois representantes reais P e P* requer a estrutura real e a comparação de campos já tratadas em outra frente.

[REAL] Uma execução do script, somente biblioteca padrão, registra 15 controles exatos. Não se contam verificações documentais posteriores como novos controles aritméticos. O manifesto mede o script, o recibo e esta nota, sem modificar os arquivos de cálculo. [OPEN] Nenhuma conclusão sobre δ(𝒦), estabilização cohomológica, QME ou UV é extraída deste cálculo080.
