# Continuação050 — adjunto antilinear, composição e operador modular
[DERIVED — derivação prévia; nenhum resultado050 compilado nesta emissão]
Data UTC: 2026-09-07T02:43:09.036270+00:00

## Ponto de partida verificado
O auditor padrão049 foi executado em leitura neste turno e retornou PASS: 85 teoremas, 23 definições, 108 prints e sete etapas. A origem matemática atual é o modelo concreto de Lebesgue L² construído ali, não uma representação física derivada da torre. A meta ampla permanece OPEN.

## Dívida escolhida
049 prova S_c=J T_c e T_c positivo auto-adjunto. Isso não basta, por simples nomeação, para afirmar Δ=S†S e T=Δ^(1/2). Este lote construirá o adjunto antilinear maximal, o domínio efetivo da composição e a igualdade com o multiplicador de peso exp(-2cξ).

## Adjunto
Para T linear parcial auto-adjunto e J antiunitária involutiva, S=JT tem adjunto antilinear A=TJ, de domínio {y:Jy∈D(T)}. A convenção é ⟨Sx,y⟩=⟨Ay,x⟩. Mostrar a identidade e sua maximalidade: todo par (y,z) que satisfaz o pareamento entra no domínio e tem Ay=z. A maximalidade usa o adjunto linear já construído pelo Mathlib, cuja densidade está provada; não apenas simetria ou renomeação de um candidato.

## Quadrado e composição
O domínio de T_c² é {f∈D(T_c):T_cf∈D(T_c)}. Ele não é D(T_c) por decreto. Mostrar a equivalência global, para todo f∈H, com MemLp(exp(-2cξ)f). A inclusão D(T_(2c))⊂D(T_c) segue de |exp(-cξ)f|≤|f|+|exp(-2cξ)f|. Provar igualdade de operadores parciais T_c²=T_(2c), incluindo domínio.

A composição S_c† S_c tem exatamente esse mesmo domínio porque J S_c=T_c. Assim Δ_c:=S_c† S_c coincide com T_(2c), que é positivo auto-adjunto pela família049. A forma quadrática deve dar ⟨f,Δ_cf⟩=||S_cf||² no domínio de Δ.

## Raiz: não esconder a próxima hipótese
A conclusão de que T_c é uma raiz positiva auto-adjunta de Δ_c será provada pela igualdade de quadrados. A identificação com a raiz canônica Δ_c^(1/2) requer conferir a existência/uniquidade ou a realização explícita do cálculo funcional para multiplicadores. Essa exigência está em revisão independente: uma igualdade pontual de pesos não será apresentada como teorema geral de raízes não limitadas.

## Limites que permanecem
[OPEN] Cálculo funcional do fluxo Δ^it, ação geométrica/Hardy, inclusão semilateral, rede de álgebras e estado, seleção física de L²/Lebesgue/c, ligação com a torre, área e H3. Não se substitui a meta ampla pela construção deste modelo; o passo paga uma ligação matemática necessária já nomeada como pendente na049.

## Custódia
Novos arquivos050 somente em Chatgpt. Fontes049 e selos anteriores somente leitura; os seis fontes049 poderão ser copiados por bytes e recompilados como baseline, com pins lidos do manifesto049. Derivações antes do código, backups exatos antes de revisões, compilação limpa conjunta e revisão independente. Nenhuma escrita em um.py, Atlas, índice, kernel ou gate.
