[DERIVED / INPUT / OPEN] CONTINUAÇÃO 018 — seção transversal e congruência nula local

06/09/2026. Derivação anterior ao código Lean. O turno 017 foi progresso: custódia reconferida nesta sessão, 536 hashes, seis módulos limpos, 18 teoremas e uma definição impressa. Permanecem somente as ordens gerenciais 001–007. O objetivo amplo segue ativo e não alcançado.

## Alvo

Dados um aberto U, uma solda suave invertível A com inverso B, p∈U e v≠0 nulo para g(p)=A(p)ᵀηA(p), construir um aberto N contendo p e um campo V suave nele, com V(p)=v, V≠0, g(V,V)=0 e ∇_V V=0. O fluxo suave de 017 fornece a evolução. Nenhum campo espacial geodésico será recebido como hipótese no teorema final.

## Derivação anterior à implementação

1. Definir W(x)=B(x)A(p)v. Então W(p)=v e A(x)W(x)=A(p)v. Logo g(x)(W,W)=g(p)(v,v)=0. A inversibilidade garante W≠0 e a suavidade de B garante a suavidade de W.

2. Escolher uma forma linear contínua ℓ com ℓ(v)=1, usando uma coordenada não nula de v. Definir Π=I−v⊗ℓ. Assim Πv=0 e Πz+ℓ(z)v=z. Os dados iniciais são (p+Πz,W(p+Πz)) e o tempo é ℓ(z). A seção inicial está no hiperplano ℓ(x−p)=0. O parâmetro z∈ℝ⁴ reúne três direções transversais e uma temporal.

3. Aplicar o fluxo geodésico a esses dados e tempos, com projeções X(z) e Y(z). Há um aberto D contendo 0 onde os argumentos pertencem ao domínio do fluxo e as duas projeções são suaves. X(0)=p, Y(0)=v e DX(0)h=Πh+ℓ(h)v=h, pela derivada do fluxo demonstrada em 016. Portanto DX(0)=I.

4. Aplicar o teorema da função inversa. Restringir a carta a um aberto contido em D onde DX continua invertível. A abertura dos operadores invertíveis e a continuidade de DX pagam a restrição. A inversa deve ser C∞ em todo o alvo da carta, não apenas no ponto p.

5. Definir V(x)=Y(X⁻¹(x)) no alvo. Suavidade, nulidade, não anulação e V(p)=v são transportadas. As identidades Π(z+s v)=Πz e ℓ(z+s v)=ℓz+s mostram que s↦X(z+s v) segue a geodésica com dados iniciais fixos. Sua tangente é Y(z), e a derivada da velocidade é −Γ(Y,Y). A igualdade local V∘X=Y, junto à unicidade de derivadas, deve provar vectorAcceleration Γ V=0.

6. Instanciar o construtor de tela transportada de 014 com o campo V produzido. A condição de equilíbrio no primeiro jato permanece separada: expansão e cisalhamento nulos não decorrem da mera geodesicidade.

## Critérios, controles e limites

Construir ℓ e provar ℓ(v)=1; provar o transporte nulo W; provar DX(0)=I; construir a inversa C∞ num aberto; demonstrar aceleração covariante nula; reunir as peças sem receber V como INPUT. Controles plano e curvo devem distinguir essas propriedades das condições adicionais de equilíbrio.

Cada ponte recebe enunciado, log e #print axioms. Se uma obrigação não fechar, sua parede será explicitada. Assinatura, dimensão e solda permanecem INPUT. Continuam distintas as obrigações de primeiro jato de equilíbrio, horizonte imerso e área integrada, ponte região–álgebra e entropia–área, coeficiente físico, calor/Clausius/H3, ponte modular e globalização. O resultado local pretendido não é uma prova geral de gravidade quântica.

Escritas exclusivamente em Chatgpt. Revisões próprias com backup de bytes e temporário verificado. Entregas anteriores, um.py, kernel canônico, Atlas, memórias, selos e gate intocados. Nenhum dado observacional. Auditoria independente a cargo da gerência.

O primeiro helper de revisão teve uma quebra de linha ausente e foi recusado pelo Python antes de executar a escrita. O fonte defeituoso foi conservado em backup de bytes e a sintaxe corrigida antes da criação deste documento.
