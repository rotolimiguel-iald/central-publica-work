# Continuação 036 — área óptica e liberdade radiativa
06/09/2026. [REAL / DERIVED / INPUT / OPEN] Continuação espontânea da ordem007; procedimento008. A meta ampla de gravidade quântica permanece OPEN.

## A pergunta sobre L e a inscrição angular
A distinção proposta pelo operador entre gerador e leitura quadrática é matematicamente útil. Para u=exp(iθ), |u|²=1. Para diferença de fases, |u−1|²=4sin²(θ/2). Uma fase escalar global também deixa ||P exp(iθ)Ω||² constante. Para uma família de unitários operadores U(θ), uma leitura ||P U(θ)Ω||² pode variar quando a ação e os observáveis a distinguem; a órbita centralizadora da034 não altera as leituras fixas em M. Essas operações são distintas. A030 já formalizou a quadratura (u−I)*(u−I), sua positividade, leitura e limite modular; a034 demonstrou a invariância das leituras fixas na órbita centralizadora; a035 construiu uma família diferente com área de Fisher medida.

Na bancada L=log H é a densidade relativa em forma logarítmica. Sua identificação com L_phi usado no Atlas continua sem ponte tipada. “Cauda/poço”, “ponto onde a luz dobra” e “fluxo de estabilização” são leituras ONTO/CONJECTURE enquanto não recebem definições e teoremas correspondentes. Retorno periódico e convergência estabilizadora são propriedades diferentes.

Uma métrica de probabilidades não identifica, por si só, a área geométrica de um feixe. Por isso esta etapa trabalha diretamente na geometria curva029, cuja conexão já foi identificada com a Levi-Civita do frame. O alvo é explicar qual dado óptico continua livre apesar do mesmo casamento entrópico inicial.

## O modelo e o feixe escolhidos
[INPUT] Mantêm-se a carta (t,x,y,z), assinatura (+---) e família029:
g=eta+H k⊗k, H=a x²+c y², k=(1,0,0,1).
Fixam-se a geodésica central γ(τ)=(τ/2,0,0,τ/2), direção d=(1/2,0,0,1/2), normalização k(d)=1, tela inicial e_x,e_y e derivada inicial zero. É o feixe inicialmente colimado; um feixe de vértice tem dados iniciais e ordens de área diferentes.

[REAL — Lean, nesta família] O módulo OpticalTidalScreen liga a curva à equação geodésica da conexão real; prova que a conexão se anula na curva, que d é nulo e que a tela tem Gram lorentziano −I. A matriz óptica é definida por
K_ij = −g(e_i,R(e_j,d)d).
Na convenção R_ij=∂iΓ_j−∂jΓ_i+[Γ_i,Γ_j], obtém-se K=diag(a,c) e tr K=Ric(d,d)=a+c.

Algumas identidades algébricas valem para todo ponto x; sua interpretação como tela nula aqui está garantida na curva central. Não se afirma que a direção constante seja nula fora dessa curva.

## Área induzida e derivadas
[REAL — Lean, nesta família] A equação transversal de Jacobi é f_a''+a f_a=0, f_a(0)=1, f_a'(0)=0; análoga para f_c. O módulo escalar recebe HasDerivAt reais na ODE, obtém as derivadas do produto e fornece a solução explícita cos(sqrt(a)τ) quando a≥0.

Os campos transversais são f_a e_x e f_c e_y. A métrica positiva da tela usa −g, portanto sua Gram é diag(f_a²,f_c²). A área induzida relativa à área inicial1 é |f_a f_c|. A positividade local do produto permite transportar para a área geométrica induzida as derivadas do produto orientado perto deτ=0. A interpretação é de área transversal dos campos de Jacobi, infinitesimal em relação às separações iniciais.

[REAL — derivadas reais verificadas]
A(0)=1; A'(0)=0; A''(0)=−(a+c); A'''(0)=0;
A''''(0)=a²+6ac+c².

Ao parametrizar a=r/2+s,c=r/2−s:
A''(0)=−r,
A''''(0)/24=r²/12−s²/6.
Na família explícita de cossenos, |s|<r/2 garante a,c>0. Essa subfamília já basta para comparar áreas distintas com o mesmo r.

O lote prova derivadas reais até quarta ordem. Não contém um teorema de Taylor com resto. [DERIVED — cálculo analítico] A solução explícita também fornece
A(τ)=1−rτ²/2+(r²/12−s²/6)τ⁴+O(τ⁶)
perto de0; não atribuir a prova do resto ao Lean sem enunciado correspondente.

## A diferença independe de girar os eixos
[REAL — Lean, nesta família] Para T=K−(tr K/2)I, define-se tr(TᵀT). A mudança ortonormal K→QᵀKQ, QᵀQ=QQᵀ=I, conserva essa quantidade. Em nossa família:
tr(TᵀT)=(a−c)²/2=2s².
Isso é anisotropia de maré, não o cisalhamento inicial do feixe, que foi escolhido zero. Direção e escala afim continuam fixadas.

Com s² diferente, a segunda derivada de área permanece igual e a quarta muda. Trocar apenas s por −s permuta os eixos; não é o controle de distinção usado aqui. A área sozinha não identifica orientação ou sinal da polarização.

As identidades geométricas verificadas incluem A''(0)=−Ric(d,d) e A''''(0)=2(tr K)²−2tr(TᵀT). Ambas usam a mesma conexão e a mesma área induzida; a quarta ordem contém a anisotropia que a segunda ordem não determina.

## O que isso acrescenta à dívida de reconstrução
[REAL — alcance da029, sujeito aos seus enunciados selados] Com η≠0, o casamento entrópico fixa a soma a+c=2πκ/η, κ=log(2)B/π. A subfamília explícita por cossenos tratada nesta etapa exige r=a+c>0. A mesma família de estados e a mesma fonte deixam s livre. A029 distinguia componentes de curvatura no referencial escolhido. A036 acrescenta uma quantidade invariante por mudança de base ortonormal da tela e a resposta de área em quarta ordem.

O resultado não seleciona a geometria a partir de L. Ele identifica com mais precisão o que falta: dados que determinem a evolução óptica completa, incluindo a anisotropia radiativa e as condições de contorno. Também faltam a seleção geral da métrica/assinatura e a correspondência física entre o parâmetro dos estados e o parâmetro afim. A igualdade de segunda ordem, por si só, não elimina esses dados.

[DERIVED, não formalizado neste lote] Uma realização por família exata de geodésicas nulas é
X(τ,ξ,ζ)=(τ/2+v,f_aξ,f_cζ,τ/2−v),
v=(f_af_a'ξ²+f_cf_c'ζ²)/2.
Sua tela tem área |f_af_c| dξdζ. Essa expressão esclarece a interpretação geométrica, mas não será contada como construção formal de família de geodésicas sem o respectivo enunciado.

## Fontes e custódia
[KNOWN] Propagadores de Jacobi com posição inicial I e derivada inicial zero, e a relação entre equações transversais e coordenadas de Rosen: Harte–Drivas, Caustics and wave propagation in curved spacetimes, Phys. Rev. D85 (2012), equações2.16–2.19,3.1–3.2,3.22–3.25, [texto integral](https://arxiv.org/pdf/1202.0540). Os sinais desta etapa foram conferidos diretamente na conexão029; não se transporta convenção de Riemann apenas pelo nome.

[REAL] Instâncias nomeadas; todos os teoremas, definições e a estrutura com axiomas impressos; compilação serial em diretório inédito e importação conjunta. Fontes e binários externos à bancada são somente leitura. Os oleans e as fontes locais da fronteira geométrica estão fixados pelos manifestos029/032/033/034 e não são recompilados. Fontes individuais TGL/TGLExt sem pin histórico são lidas e hashadas agora para descobrir imports, sem demonstrar a proveniência fonte→olean. A dependência transitiva externa inteira de mathlib/toolchain não é reconstituída. Falhas e backups desta sessão são preservados.

Todos os novos arquivos ficam em Chatgpt. Nenhum original, um.py, gate, kernel canônico, Atlas ou memória foi editado. Incorporação canônica e respectiva auditoria da gerência não são reclamadas.

## Verificação final do lote

[REAL] 4 módulos, 87 teoremas, 26 definições incluindo uma estrutura; 113 declarações com axiomas impressos. Zero instâncias anônimas; o lote não declara instâncias. As cinco etapas (quatro módulos e Imports036All) terminaram com exit0, zero erros/avisos/sorryAx, cobertura exata e fontes/inputs estáveis. Os axiomas impressos pertencem a propext, Classical.choice e Quot.sound.

Diretório de compilação medido no marcador: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO036_CLEAN_20260906_170002_192324.

Os fracassos preparatórios e seus logs foram preservados. Incluem recusa de dependência sem pin, erros/avisos corrigidos e recusa por alteração de um fonte do lote durante uma tentativa; nenhum desses resultados foi tratado como aprovação. O lote final foi integralmente refeito em diretório inédito. A revisão independente dos enunciados foi favorável; incorporação e auditoria da gerência canônica continuam pendentes.

[REAL — revisão técnica independente nesta sessão] O revisor executou inspect_build() somente em leitura: exit0. Conferiu separadamente os cinco logs, 113 impressões de axiomas, igualdade de bytes nas quatro cópias e estabilidade dos inputs. Isso não constitui aprovação gerencial ou incorporação canônica.
