# Esperanças dos andares — demonstração anterior à formalização

[DERIVED] Construção matemática para a torre produto fiel. O estatuto [REAL — Lean] será atribuído separadamente, por teorema compilado na entrega 001. Data: 05/09/2026.

## Hipóteses e objetos

1. [INPUT] `P : SiteProfile`, com 0 < P.w(n) < 1. O andar N contém os primeiros N+1 sítios de dimensão 2; A_N = M_{2^(N+1)}(C), incluído por a ↦ a ⊗ 1.
2. [DERIVED] ρ_N é diagonal com pesos `towerW P N`, positivos e de soma 1. ω_N(a)=Tr(ρ_N a). As inclusões preservam os estados.
3. [REAL — etapas anteriores] H é o completamento GNS, M=π(∪A_N)'', Ω é cíclico e separante. H_N=A_N Ω é finito dimensional; p_N é sua projeção ortogonal, e p_N → 1 fortemente.

## Fórmula finita e extensão correta

Para K≥N, escreva A_K=A_N⊗A_(N,K], com estado complementar de matriz diagonal ρ_(N,K]. Defina

    E_N^K(x)_(i,j) = Σ_r w_(N,K](r) x_((i,r),(j,r)).

Os pesos do complemento somam 1. Logo E_N^K(a⊗b)=a ω_(N,K](b). Inserir uma identidade no último sítio não muda a soma: as fatias são compatíveis. Para a,b∈A_N,

    E_N^K((a⊗1)x(b⊗1)) = a E_N^K(x) b.

Cada compressão x↦V_r* x V_r, V_r(v)=v⊗e_r, é completamente positiva, porque sua amplificação envia uma matriz positiva X a (1⊗V_r)*X(1⊗V_r). A combinação com pesos positivos é completamente positiva e unital. Em particular é positiva e contrativa em norma de operador.

**Cuidado topológico:** completar a união em norma de operador produz a álgebra C* quase local, não automaticamente o bicomutante M. Completar vetores em norma GNS produz H, não M. Para chegar a TODO M usamos a construção seguinte, sem confundir esses completamentos.

O mapa i_N:a↦aΩ é um isomorfismo linear A_N→H_N: injetividade vem da positividade estrita dos pesos; sobrejetividade é a definição de H_N. Para x∈M defina

    E_N(x) = π(i_N^(-1)(p_N xΩ)).                     (1)

Na verdade (1) define um mapa linear limitado em B(H): avaliação em Ω é limitada, p_N é limitado e i_N^(-1), seguido de π, tem domínio finito dimensional. A propriedade de positividade abaixo é afirmada na restrição a M. Não se confunde limitação dessa extensão com contrato de esperança em B(H).

## Prova das propriedades no bicomutante

As ações à esquerda L_a e à direita R_b do andar N preservam H_N. Seus adjuntos também: L_a*=L_a*, R_b*=R_(ρ_N b* ρ_N^-1). Assim H_N é redutor para ambas e p_N comuta com elas. Todo x∈M comuta com R_b.

Da definição, E_N(x)Ω=p_N xΩ. Para b∈A_N:

    E_N(x)bΩ = R_b p_N xΩ = p_N R_b xΩ = p_N x bΩ.

Portanto a restrição de E_N(x) a H_N é a compressão p_N x|H_N. Esta identidade prova:

* imagem em M_N=π(A_N), por construção;
* restrição E_N(a)=a e idempotência, pois p_N fixa H_N e Ω é separante;
* ω(E_N(x))=ω(x), pois Ω∈H_N;
* bimodularidade: E_N(a x b)Ω=p_N a x bΩ=a p_N x bΩ=a E_N(x)bΩ; ambos os operadores estão em M, logo separância dá igualdade;
* positividade completa: a compressão em H_N, e em H_N^k para cada k, é positiva; a representação fiel de A_N em H_N reflete positividade, inclusive matricial. Assim E_N|M é completamente positiva e unital. Sua norma é 1;
* normalidade: cada coordenada de i_N^-1(p_N xΩ) é uma combinação finita de funcionais vetoriais x↦⟨v,xΩ⟩. São ultrafracamente contínuos e a imagem é finito dimensional;
* fidelidade: E_N(x)=0, x≥0, implica ω(x)=0; a fidelidade de ω implica x=0.

Para a comutação modular, U_t H_N=H_N e U_t Ω=Ω já foram construídos. Logo U_t p_N=p_N U_t. Portanto σ_t(E_N(x))Ω=U_t p_N xΩ=p_N U_t xΩ=E_N(σ_t(x))Ω, e separância conclui.

Para a cadeia, H_M⊂H_N quando M≤N. Projeções ortogonais aninhadas satisfazem p_M p_N=p_N p_M=p_min(M,N). Aplicando a (1) e usando separância, E_M E_N=E_min(M,N). Da mesma forma E_N(x)Ω→xΩ.

A fórmula finita inicial é identificada com (1) pelo teste contra cada aΩ: ω_K(a* x)=ω_N(a* E_N^K(x)). Estes testes determinam p_N xΩ e a matriz, portanto não há escolha adicional de esperança.

## Contrato importado: diferença exata

[REAL — leitura do fonte] `TGLExt.ExpectationInput` exige `into : E(x) ∈ omegaCentralizer P` e `fixes` sobre TODO esse centralizador. O destino NÃO é M_N.

[DERIVED] M_N não está em geral contido no centralizador: em um sítio de peso p≠1/2, a=e_01 e b=e_10 satisfazem ω(ab)=p e ω(ba)=1-p. Como E_N(a)=a, E_N não pode ter o campo `into` exigido. Mesmo para o perfil tracial, o centralizador é M inteiro e E_N não fixa os sítios posteriores. Logo nenhuma troca de nome resolve o contrato.

[OPEN — formalização adicional] Uma esperança sobre M_ω requer outro procedimento, por exemplo projeção/ média ergódica do fluxo com prova de que a imagem é o centralizador, além da ponte entre a definição livre de fluxo e pontos fixos. Esta ordem permite registrar precisamente essa distância; não se postula `TakesakiInput`.

[KNOWN] Contexto externo: [Takesaki, Conditional expectations in von Neumann algebras (1972)](https://www.sciencedirect.com/science/article/pii/0022123672900043). A construção acima é específica do produto e não usa a conclusão do teorema como hipótese.
