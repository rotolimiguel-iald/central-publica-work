# Derivação prévia — operador completo de uma volta

[DERIVED — em verificação] A entrada é a Hessiana on-shell da ação Einstein–sigma da nota Jacobi066, com calibre de de Donder. Nenhuma ação ou operador canônico será editado.

Denote s=κc, u=dφ, Wμν=〈uμ,uν〉, Q=tr W, U=uμ⊗u^μ e Bμν=Dμuν, com tr B=τ=0. A conexão base é ∇⁰=LC em Sym²T* mais D em φ*TS³. O operador normalizado P=B_fibra⁻¹ H_gf tem principal ∇⁰². Usando Ric=Λg+sW na parte de ordem zero:

Vhh(h)=2Rμρνσh^ρσ−s(Wμ^ρhρν+Wν^ρhρμ);
Vξh(h)=−Bμνh^μν; Vhξ=0; Vξξ=QI−U.

A primeira ordem é 2ω^ρ∇⁰ρ, onde
(ωρξ)μν=s(gμρ〈uν,ξ〉+gνρ〈uμ,ξ〉);
ωρh=−u^νhρν/2+uρ tr(h)/4.

Logo ∇hat=∇⁰+ω e E=V−∇⁰·ω−ωμω^μ. A previsão a verificar por matrizes explícitas é
Ehh=2Riem(h)−s(W·h+h·W+W tr h)/2;
Ehξ=−2s〈Bμν,ξ〉; Eξh=−B:h/2;
Eξξ=QI+(2s−1)U.

Ωhatρσ=Ω⁰ρσ+∇⁰ρωσ−∇⁰σωρ+[ωρ,ωσ]. O fantasma tem Egh=Ric e Ωgh a curvatura em covetores. O coeficiente local combinado será 1/2 tr b4(E,Ωhat)−tr b4(Egh,Ωgh), com o peso de um par Grassmann c/barc de quatro componentes. Não se usam oito determinantes fantasmas.

A Hessiana tem B_fibra=diag(−Itr/(4κ),−cI3). Em assinatura euclidiana a forma principal −B_fibra tem uma direção conforme negativa: a normalização do determinante exige explicitar medida e contorno. A eliminação do auxiliar b gera fator determinantal ultralocal, sem um quinto operador de onda. Nenhuma continuação global de Wick ou cancelamento total será presumido.

Controle CAS pretendido: construir as matrizes 13×13 de V, ω e derivadas covariantes em um referencial ortonormal do fundo a=2cos(r/2), mais o fantasma 4×4; verificar E, compatibilidade da fibra, curvaturas, traços e combinação. A redução é uma identidade local de jatos Lorentzianos e não uma prova de existência de calor Lorentziano. Controle independente: retirar a matéria e conferir o coeficiente puro Einstein conhecido, com a convenção de fator 1/2 declarada.
