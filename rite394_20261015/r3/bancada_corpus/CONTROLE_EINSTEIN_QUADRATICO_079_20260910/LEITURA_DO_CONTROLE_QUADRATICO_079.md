# Leitura do controle quadrático079

10/09/2026. [REAL — 12 controles matriciais simbólicos exatos]. O cálculo foi executado uma vez com Python3.14 e SymPy1.14.0 já copiados em Chatgpt. Nenhum um.py foi importado ou executado, nenhuma instalação original foi modificada e não houve Lean.

O script deriva Γ0, Γ1 e Γ2=−(g0⁻¹h)Γ1, constrói Ricci em cada ordem pela soma de todos os produtos Γ_mΓ_(n−m) e inclui as variações da métrica inversa na curvatura escalar. F2 é o coeficiente de ε² em G(g0+εh)+Λ(g0+εh), não a segunda derivada sem dividir por dois.

Para f(z) arbitrária, o resultado é diagonal:
F2_00=−k²f²/4+f f''+3(f')²/4−2f f'/z;
F2_11=F2_22=−3k²f²/4−f f''−(f')²/4+2f f'/z;
F2_33=−(k²f²+(f')²)/4+2f f'/z.

As demais componentes são zero. As expressões são pares em k como funções, antes de impor a EDO. O controle inclui a fonte densitizada e com índices elevados, com as parcelas que multiplicam F1; também é par em k. Esse objeto é registrado sem o prefator da ação, cuja normalização não precisa ser escolhida para testar paridade.

No ponto do certificado, f=0, f'=1, f''=2/z, τ=0, F2=diag(3/4,−1/4,−1/4,−1/4) e Ric2=diag(0,1/2,1/2,1/2). A equação quadrática não é zero, embora a perturbação resolva a equação linear. O funcional ímpar elimina sua contribuição por comparação, não por chamá-la de nula.

Os 12 controles incluem inversa até segunda ordem, equação do fundo, transformação da perturbação, simetrias e paridade de F2/fonte densitizada e dois valores pontuais. A fonte documental foi medida ANTES do cálculo e depois dele nesta execução; os bytes permaneceram iguais. Isso corrige o alcance de custódia temporal no novo procedimento sem alterar nem reescrever o recibo078, cujo intervalo mais curto continua explicitado.

O recibo não enumera infinitos jatos nem decide δ(K). O argumento de todos os jatos e a aplicação ao BRST estão na nota escrita separada, sujeita à revisão independente. Os 122 controles da078 não são recontados aqui.
