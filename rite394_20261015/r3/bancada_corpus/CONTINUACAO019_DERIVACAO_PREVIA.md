[DERIVED / INPUT / OPEN] CONTINUAÇÃO 019 — primeiro jato de equilíbrio da congruência nula

06/09/2026. Derivação anterior ao código Lean desta etapa. O turno 018 foi progresso: seu auditor acaba de reconferir 553 hashes, sete módulos limpos, 37 teoremas e uma definição impressa. O túnel ainda contém somente as ordens gerenciais 001–007. O objetivo amplo continua ativo e não alcançado.

## Alvo e motivação

Fortalecer local_levi_civita_null_congruence de 018 para construir V com covariantVectorGradient Γ V p=0, além de suavidade, nulidade, não anulação e geodesicidade local. Essa é a hipótese equilibrium_gradient dos objetos de horizonte já existentes. Não deve ser simplesmente recebida como INPUT no resultado final.

## Derivação

1. Fixar p e v nulo não nulo. Definir o mapa linear J(h)=−∑ᵢ hᵢ Γᵢ(p)v e o campo afim R(x)=v+J(x−p). Então R(p)=v e ∇R(p)=0, por cálculo direto das derivadas.

2. Seja q(x)=g(x)(R(x),R(x)). A compatibilidade métrica dá ∂ᵢq(p)=2g(p)(v,∇ᵢR(p))=0. Portanto q(p)=0 e Dq(p)=0. Isso usa a derivada efetiva e a suavidade, não a convenção de fderiv para funções não diferenciáveis.

3. Construir uma direção nula companheira n₀ de v no ponto p usando o referencial nulo normalizado de 013, com g(p)(v,n₀)=−1. Transportá-la pela solda: n(x)=B(x)A(p)n₀. Ela é suave, nula e assume n₀ no ponto p.

4. No aberto onde d(x)=2g(x)(R(x),n(x)) não se anula, definir
   W(x)=R(x)−[q(x)/d(x)] n(x).
   Como n é nulo, a expansão bilinear dá g(W,W)=q−2(q/d)g(R,n)=0. Como q(p)=Dq(p)=0 e d(p)≠0, a correção tem valor e primeira derivada zero no ponto. Assim W(p)=v e DW(p)=J; logo ∇W(p)=0. Abertura e vizinhança do domínio precisam ser provadas.

5. Aplicar a construção de shooting de 018 a W no aberto restringido. Como DX(0)=I, a inversa tem derivada I em p. Para a velocidade,
   DY(0)h=DW(p)(Πh)+ℓ(h)·sprayAcceleration Γ p v.
   O jato prescrito dá DW(p)v=−Γ(p)(v,v), portanto DY(0)h=DW(p)h. Para V=Y∘X⁻¹ resulta DV(p)=DW(p), V(p)=v e ∇V(p)=0.

6. Reunir o campo construído com a tela transportada. A expansão inicial e o termo quadrático do gradiente devem zerar por cálculo. Se a interface permitir, construir o objeto geométrico de lápis de horizonte e sua expansão local, conservando explícitos coeficientes e hipóteses físicas.

## Controles e limites

Controles em solda identidade e no fundo conformal curvo. O controle de 018 com expansão não zero não será apagado: ele mostra que equilíbrio exige esta escolha adicional de jato. Se algum elo não fechar, registrar o enunciado e a parede exata.

A dimensão, assinatura, solda e inversa suaves continuam INPUT. O jato zero no ponto não implica campo paralelo num aberto, nem curvatura zero. Não paga integrabilidade de uma hipersuperfície nula, horizonte imerso, área integrada, região–álgebra, entropia–área microscópica, unidade/coefficientes físicos, calor/Clausius/H3, ponte modular ou globalização.

Todas as escritas exclusivamente em Chatgpt. Fontes entregues, um.py, kernel canônico, Atlas, memórias, selos e gate intocados. Revisões próprias preservam backup de bytes; tentativas falhas não são apagadas. Auditoria independente da gerência permanece separada.
