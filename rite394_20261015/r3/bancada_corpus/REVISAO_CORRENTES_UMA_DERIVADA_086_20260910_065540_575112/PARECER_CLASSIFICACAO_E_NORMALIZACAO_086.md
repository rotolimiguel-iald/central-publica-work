# Parecer independente: correntes W·∇W e sua divergência

10/09/2026. Revisor: selected_geometry_design. Investigação086. [DERIVED — revisão matemática escrita]. [REAL — somente os controles documentais enumerados no recibo]. Nenhum CAS, Lean ou programa canônico foi executado/importado.

**Parecer favorável, sem erro material identificado no alcance declarado.** Li integralmente a nota de Singer e seu manifesto, refiz a redução do primeiro jato, a multiplicidade dos dois vetores e as contas de normalização/avaliação abaixo. A prova específica não foi substituída pela demonstração geral086 de minha autoria: esta revisão verifica o argumento independente com uma derivada. Não solicito alteração da fonte congelada.

Fonte principal: [CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md](<C:/IALD/Central de Patentes/Chatgpt/CORRENTES_WEYL_UMA_DERIVADA_086_20260910/CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md>).

## 1. Normalização e categoria

A definição desta nota é I086=(1/2)W_abcd W^abcd. A fonte082 define I082=W_abcd W^abcd, conforme sua equação5. Portanto **I082=2I086**, enquanto J086=J082=(1/2)W·*W=tr(W∧W)/vol permanece igual. Um coeficiente A082 de grad I082 passa a 2A082 na base grad I086; isso não muda o módulo gerado ou qualquer exclusão. A nota escreve sua definição explicitamente, de modo que não há erro a corrigir; a igualdade entre nomes sem esse fator é que seria incorreta na integração.

Com *²=−1 e a estrela autoadjunta para a contração bilinear de duas-formas, (*W)·(*W)=−W·W. Logo a equação10 confere: W±·W±=I086∓iJ. Todas as identidades posteriores usam essa meia normalização. Em particular, W·∇W=∇I e W·∇(*W)=∇J.

O domínio é o quociente pelas EOM Einstein lineares e todos os prolongamentos, em espaço-forma orientado de dimensão quatro, K>0 real fixado, κ real não nulo fixado, sem tensores externos. Rher é unital real, não nula, de escalares constantes/inertes; não precisa ser reduzida nem domínio. Um coeficiente não pode ser escolhido separadamente para cada frequência de teste. Não se afirma resultado no fundo físico sigma φ=id.

## 2. Exaustão das contrações de uma derivada

Conferi a distinção entre fechamento s0 off-shell, que segue de W(g0)=0, e redução on-shell, que usa Cotton/Bianchi e div W=0. Essa distinção é mantida na fonte.

Na notação de SPINS da nota, W_C=(2,0)⊕(0,2), não os pesos inteiros 2j usados em outros arquivos. O primeiro jato tem limite superior (5/2,1/2)⊕(1/2,5/2): a contração da derivada com o Weyl espinorial é exatamente a parcela (3/2,1/2) eliminada pela equação divergência. Não se comutam duas derivadas nessa etapa; não há um termo K·W omitido da primeira decomposição.

O produto (2,0)⊗(5/2,1/2) contém (1/2,1/2) uma única vez; o conjugado fornece outra cópia. Os produtos cruzados têm um spin fixo 5/2 e não contêm vetor. A forma real Lorentziana troca as duas quiralidades: são dois parâmetros REAIS, não quatro. As contrações explícitas Ψ·χ=(1/2)∇(Ψ·Ψ) e sua conjugada identificam os candidatos com grad I, grad J.

Este limite superior vale mesmo se o quociente curvo tiver relações adicionais: módulos tensoriais finitos da isotropia são semissimples e tomar intertwiners é exato. As avaliações do §5 dão depois o limite inferior. Não há passagem ilegítima de mera contagem de representações a realizabilidade arbitrária de toda a torre.

Conferi também as equações11–12. Sym²W não contém os tipos do tensor de posto dois sem traço: na notação de spins, (1,1), (1,0) e (0,1). Assim W_acde W_b^cde e o tensor quadrático misto com estrela são proporcionais a g_ab; os traços fixam 1/4. Derivar e usar div W=0 dá os fatores 1/2 das duas últimas identidades11.

## 3. Primárias e derivada covariante

A leitura direta de [Vasiliev, hep-th/9611024v2, §9, equações87–91](https://arxiv.org/pdf/hep-th/9611024) confirma a organização do primeiro jato por cinco índices de uma quiralidade e um da outra. As equações seguintes exibem termos de curvatura em ordens superiores. O uso da fonte na nota fica corretamente limitado a esse primeiro jato; não herda automaticamente sua convenção para λ² nem uma classificação não linear.

Li também [Torre, gr-qc/9508005, equação8 e parágrafos adjacentes](https://arxiv.org/pdf/gr-qc/9508005). A parametrização ali discutida é Ricci-flat. Singer a identifica como linguagem de jatos e não a usa para trocar o K positivo por zero. Essa ressalva é necessária e foi preservada.

A identidade □bar W=6KW foi cotejada com a derivação083, equações10–12: cada índice covariante recebe −R; as duas contrações de comutadores dão −3KW e a equação tem o sinal global negativo. Portanto sobra +6KW. A derivada atua em TODOS os slots, não apenas no índice interno da conexão.

Com a métrica, o volume e a estrela paralelos, Leibniz fornece corretamente □I=12KI+2I1 e □J=12KJ+2J1, para I1=(1/2)∇W·∇W e a definição dual correspondente. O termo de primeira derivada não pode ser apagado para substituir □J por 12KJ.

## 4. As avaliações que pagam a independência

Refiz as contas escritas, sem CAS. A família TT satisfaz a equação diferencial na vizinhança; por isso os funcionais anulam EOM e TODOS os seus prolongamentos.

O fator da contração é Wtilde²=16(E²−B²), logo I=8a^−4(E²−B²). O fator conformal a^−4 está correto: W covariante físico=a²Wtilde, e a contração tem quatro inversas da métrica.

Para k=0, p=f'=(z/z0)², B=0 e E=−p/(2z). Segue I=2z^6/(ell^4 z0^4), J=0 em toda a vizinhança. O operador escalar é □F=(z²/ell²)(−F''+2F'/z). Portanto □I=−18I/ell² antes de especializar e, em z0=ell,

- I'=12/z0³;
- □I=−36/z0⁴.

Para k=1/z0, os perfis083 dão J'=−24/z0³ e □J=56/z0⁴. Assim, A grad I+B grad J=0 implica primeiro A=0 em k=0 e depois B=0 em k=1/z0; a mesma sequência funciona para A□I+B□J=0.

Todos os fatores cancelados são reais não nulos e, portanto, unidades em qualquer Rher permitido. Nenhuma avaliação numérica de nilpotentes foi usada. Isso prova que os dois vetores e as duas divergências são independentes no quociente, não apenas em um modelo tensorial sem relações.

## 5. Exclusão de J e do canal Euler invariante

A paridade em k foi usada legitimamente: I e □I são pares, J e □J ímpares. A simetria helicoidal garante independência temporal do escalar na vizinhança; não se tomou a fórmula em τ=0 como se sua derivada temporal fosse conhecida sem prova. A reflexão serve para comparar soluções na orientação fixada; não altera o coeficiente Rher.

A parte ímpar de J=A□I+B□J exige J=B□J. Em k=1/z0, J=−4/z0² e □J=56/z0⁴, impondo B=−z0²/14. Em k=2/z0, J=−8/z0² e □J=−224/z0⁴, impondo B=z0²/28. São incompatíveis por uma unidade real.

A extensão com K²f também confere sem pressupor N^g=0. A invariância sob TODA a álgebra de Killing implica ∇bar f=0 pela ação das transvecções. Após derivar em z e tomar a parte ímpar, restam as mesmas condições084:

- em k=1/z0: −24/z0³=(144/z0⁵)B;
- em k=2/z0: −24/z0³=(−3168/z0⁵)B.

Subtrair fornece (3312/z0⁵)B=0, logo B=0 e contradição. Cotejei os coeficientes com 16k^5−656k³/z0²+784k/z0⁴. K=ell^−2 fica constante DURANTE a diferenciação; só depois se põe ell=z0. Isso não deriva incorretamente K como função da coordenada.

## 6. Alcance do parecer e custódia

[DERIVED] O argumento específico prova a classificação das contrações W·∇W, sua imagem livre de divergência e a exclusão de J mesmo com qualquer coeficiente Euler invariante admissível. Não depende da nulidade N^g085 nem da minha prova geral por símbolos086. A exclusão geral086 é antecedente distinto e não é reaprovada por esta revisão.

A remissão à forma normal084, de minha autoria, foi consumida como resultado já existente; não atribuo a este parecer uma revisão independente nova dessa mesma prova. O mesmo cuidado vale para o histórico de revisões. O exame atual é da nota de Singer.

A fonte não afirma todas as ordens, naturalidade de primitivas causais, QME, anomalia efetiva, fechamento do fundo físico sigma ou UV. Seu trecho OPEN sobre derivadas superiores delimita a própria nota, sem contrariar um suplemento independente que tenha sido concluído depois. Nenhuma investigação087 foi acrescentada.

[REAL — documental] O recibo mede fonte, manifesto, oito dependências declaradas, emissor e a fonte082 da normalização. O emissor foi somente medido, nunca executado. Os hashes foram lidos dos bytes, comparados com os pins do manifesto e relidos ao término; os links locais da fonte foram conferidos.

Uma tentativa auxiliar de imprimir trechos falhou por codificação cp1252 no stdout; foi repetida com stdout UTF-8 e completou. Não houve escrita de fonte ou execução matemática nessa tentativa. Ela é registrada como falha de apresentação resolvida, não como leitura bem-sucedida presumida.

Nenhum original, arquivo congelado, Atlas, memória canônica, selo ou gate foi alterado. Este novo parecer não altera o estado declarado no manifesto histórico da fonte; registra ao lado a revisão específica concluída.
