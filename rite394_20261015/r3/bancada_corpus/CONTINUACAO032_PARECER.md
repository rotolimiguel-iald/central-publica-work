# Continuação 032 — comutação modular e igualdade de domínios

[REAL / INPUT / OPEN] 06/09/2026. Continuação espontânea da ordem 007. Os quatro módulos finais passaram em Lean, sem erros ou avisos, com as dependências de axiomas admitidas. A auditoria independente da gerência e a incorporação permanecem pendentes.

Para a família somável construída nas etapas 028–031, foi demonstrada a igualdade de operadores parciais fechados

Δ_{Ψ|Ω}=exp(L)Δ_ω, com D(Δ_{Ψ|Ω})=D(Δ_ω).

A igualdade inclui o domínio. Não é somente uma fórmula em vetores locais, uma definição de nome ou uma identidade formal de produtos. O operador do lado esquerdo continua sendo o fecho relativo e a composição S†S efetivamente construídos na 031.

## O que foi demonstrado

[REAL] A separação de frequências utiliza igualdade para todo s real. Se exp(isa)c=exp(isb)c e c não é zero, então a=b, por derivação em s=0 e cancelamento. O controle completo é c=0 ou a=b. A prova não extrai uma frequência única de amostragem em tempos discretos.

[REAL] Um vetor x com U_s x=exp(isr)x para todo s pertence ao domínio de Δ_ω e satisfaz Δ_ω x=exp(r)x. Para demonstrar isso, seus produtos internos com os autovetores locais são nulos ou têm a mesma frequência. Os testes são estendidos às matrizes de cada andar por somas finitas de unidades matriciais. O teorema anterior de gráfico fraco fornece então o domínio e o valor do operador não limitado.

[REAL] Para qualquer perfil admissível desta construção de torre, um operador B limitado e autoadjunto que comuta com todo U_s preserva D(Δ_ω) e comuta com Δ_ω nesse domínio. A hipótese de auto-adjunticidade de B é usada para transportar os testes de produto interno. Positividade e invertibilidade de B não são hipóteses desse lema. A prova não usa densidade simples para justificar a aplicação de um operador não limitado.

[REAL] A invariância σ_s(B)=B foi ligada explicitamente à comutação com U_s. Isso foi aplicado ao filtro R=exp(L/2), ao inverso V=exp(-L/2) e ao gerador L. No caso de V, sua invariância foi demonstrada pela exponencial e pela invariância de L.

[REAL] Como R e V preservam D(Δ_ω) e são inversos, Rx pertence ao domínio se e somente se x pertence. A descrição do domínio relativo da 031 torna-se, portanto, exatamente D(Δ_ω). Nesse domínio, RΔ_ωR=R²Δ_ω=exp(L)Δ_ω. A igualdade foi registrada como igualdade de LinearPMap, e positividade, fechamento e auto-adjunticidade do produto foram transportados do operador relativo já verificado.

[REAL] O controle t=0 recupera exatamente o operador de referência Δ_ω. Esse controle usa a identidade demonstrada L(0)=0, não um valor numérico inserido.

## Escopo

[INPUT] A aplicação a L, R, V e Δ relativo usa a referência de sítio (1/3,2/3), amplitudes 0≤b_n≤1/12 com soma finita e h(t)=t²/(1+t²). Trata-se da família SummableAmplitude efetivamente construída. O lema intermediário para B tem escopo em qualquer SiteProfile admissível da torre; isso não o torna um resultado aqui formalizado para toda álgebra de von Neumann.

[OPEN] A etapa estabelece comutação no domínio e identidade do produto. Não foi construída uma teoria genérica de cálculo funcional conjunto, nem foram identificadas as potências imaginárias do operador relativo. Não se pode definir essas potências como u_s U_s e usar a definição como prova da identificação desejada.

[KNOWN] Uma rota para identificar o cociclo é a especialização limitada de Pedersen–Takesaki: H=exp(L)=R² positivo e invertível no centralizador, ψ(A)=ω(RAR), e [Dψ:Dω]_s=H^{is}. A caracterização é apresentada em [Hiai, Teorema 9.4(2)](https://arxiv.org/pdf/2004.02383#page=84). Aqui ainda é necessário formalizar essa ponte ou uma caracterização equivalente. O cone natural é uma rota possível para certas identificações canônicas; não é um requisito obrigatório dessa via.

[OPEN] A identificação da esperança de L com entropia de Araki integral também conserva suas obrigações próprias. A igualdade já obtida com o limite das entropias relativas dos prefixos permanece o resultado da 030.

## Relação com geometria e com a ordem 007

A etapa 031 foi classificada como progresso efetivo e reconferida no início desta continuação: auditor somente leitura PASS, quatro módulos, 51 teoremas e 13 definições impressas, 753 hashes. A ordem 007 continua sendo a última recebida; esta entrega é espontânea e não substitui a entrega original dos seus alvos A, B e C.

[OPEN] A comutação demonstrada fortalece a base necessária para comparar a inscrição angular com grandezas geométricas. Ela não seleciona uma superfície, uma escala de comprimento, um mapa região-álgebra ou uma equação de estabilização. A operação angular pretendida pelo operador permanece em esclarecimento. Nenhuma escolha entre módulo, módulo ao quadrado e área de duas direções é assumida nesta etapa.

[OPEN] A reconstrução gravitacional geral e a prova ampla de gravidade quântica permanecem abertas. Igualdades modulares não são, por si, uma derivação da dinâmica gravitacional física.

## Revisão e custódia

Uma revisão adversarial independente, somente leitura, não identificou lacuna matemática nos quatro fontes: conferiu a extensão finita dos testes, o uso da auto-adjunticidade de B, a igualdade de domínios pelos dois inversos e a igualdade de LinearPMap. Essa revisão não é recompilação ou aprovação da gerência.

As tentativas rejeitadas permanecem no inventário. A primeira compilação de ModularDomainCommutation exigiu corrigir um transporte de pertinência ao domínio; a versão final usa diretamente a passagem de gráfico a domínio da biblioteca. A primeira compilação de RelativeModularProduct exigiu explicitar os dois operadores nos argumentos da extensionalidade, evitando que a igualdade de domínios determinasse incorretamente o segundo operador. Não houve alteração das afirmações matemáticas para obter a compilação.

O auditor calcula contagens e hashes dos bytes, exige logs limpos para os fontes finais, verifica toda a cobertura de axiomas e preserva os backups e as tentativas falhas. Contagens incluem lemas auxiliares e não medem uma porcentagem de conclusão física.

Toda escrita desta etapa está em Chatgpt. As etapas seladas, os originais, o kernel canônico, um.py, Atlas, memórias, selos e gates permanecem intocados pela bancada. A entrega e o manifesto são novos; a gerência mantém a auditoria e a incorporação.
