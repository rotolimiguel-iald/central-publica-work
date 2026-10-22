# Revisão independente do elo Jacobi → coeficiente de calor acoplado

09/09/2026. [DERIVED — revisão escrita própria]. Fonte revisada: `CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553/COEFICIENTE_COMPLETO_UMA_VOLTA.md`. Resultado: **não encontrei erro material** na extração de ω e E, nas contrações apresentadas ou nos pesos 1/2 bosônico e −1 fantasma, dentro do escopo on-shell e da normalização diferencial especificados.

A revisão compara a fonte com a Hessiana Jacobi 066 e recompõe as identidades tensorais por escrito. Não reexecuta os controles CAS, não calcula a medida completa, não extrapola a Hessiana off-shell e não reabre o resultado de não absorção, objeto de parecer separado.

## 1. Comparação direta com a Hessiana anteriormente derivada

Use s=κc, W_μν=<u_μ,u_ν>, Q=tr W, B_μν=D_μu_ν, τ=tr B=0 e Ric=Λg+sW. A nota 066 dá

\[
 D_{hh}=\frac1{2\kappa}\{-\tfrac12\Box I_{\rm tr}+\mathcal L_R+\Lambda-\kappa\delta T\},
\qquad
 D_{\xi\bullet}=-c\{(D^2+QI-U)\xi-B:h-u\cdot C(h)\}.
\]

Normalizar por B_fibra=diag(−I_tr/(4κ),−cI₃) multiplica o primeiro bloco por −2I_tr. Para conferir a simplificação algébrica, a parte métrica de ordem zero **antes** desse fator é

\[
 A_h=\frac s2(W\cdot h+h\cdot W)-\mathcal Rh+rac\Lambda2g\,\mathrm{tr}(h),
 \qquad \mathrm{tr}(A_h)=\Lambda\mathrm{tr}(h).
\]

Portanto −2I_tr A_h=2ℛh−s(W·h+h·W), exatamente V₀,hh da fonte. Na parte derivativa em ξ, I_tr[A(ξ)−g<u,Dξ>]=A(ξ), porque tr A=2<u,Dξ>. A mistura normalizada é +2sA(ξ).

No outro sentido, a mistura é

\[
 -u^\nu\nabla^\mu h_{\mu\nu}+\frac12u^\rho\nabla_\rho\mathrm{tr}(h)-B:h.
\]

Essas duas expressões são precisamente 2ω^ρ∇_ρ com

\[
 (\omega_\rho\xi)_{\mu\nu}=s(g_{\mu\rho}<u_\nu,\xi>+g_{\nu\rho}<u_\mu,\xi>),
 \qquad
 \omega_\rho h=-\tfrac12u^\nu h_{\rho\nu}+\tfrac14u_\rho\mathrm{tr}(h).
\]

Logo nenhum termo de calibre C(h) foi eliminado antecipadamente. A conexão efetiva do operador completo não é a conexão direta de três campos escalares independentes.

## 2. Contração de ω e potencial normal E

Refazendo as composições em dimensão quatro, obtenho

\[
 (\nabla\cdot\omega)_{h\xi}=2sB,\quad
 (\nabla\cdot\omega)_{\xi h}=-B:h/2,
\]
\[
 (\omega^2)_{hh}=-\tfrac s2(\mathcal S_W-\mathcal T_W),\quad
 (\omega^2)_{\xi\xi}=-2sU,
\]

onde S_Wh=W·h+h·W e T_Wh=W tr h. O último fator resulta de −5sU/2+sU/2; o 5 vem de quatro dimensões mais o segundo índice simétrico. Em ∇·ω_ξh, o termo τ tr h/4 desaparece somente pela hipótese on-shell.

Subtrair essas parcelas de V₀ fornece

\[
 E_{hh}=2\mathcal R-\tfrac s2(\mathcal S_W+\mathcal T_W),\quad
 E_{h\xi}=-2sB,\quad E_{\xi h}=-B/2,\quad
 E_{\xi\xi}=QI+(2s-1)U.
\]

Esses são todos os blocos de (2.4). O produto G_B E é simétrico e G_Bω é antissimétrico na forma de fibra indicada: por exemplo, os dois blocos mistos de G_BE são cB/2, pois I_tr B=B quando τ=0. Esse controle verifica os sinais relativos sem transformar a forma indefinida em uma norma positiva.

## 3. Traços de E e E²

No espaço dos tensores simétricos de posto dois, tr ℛ=−R/2, tr ℛ²=3 Riem²/4 e tr(S_W+T_W)=6Q. Os traços cruzados tr ℛS_W=−Ric·W e tr ℛT_W=+Ric·W cancelam.

Uma conferência explícita da parte quadrática é

\[
 \mathrm{tr}\mathcal S_W^2=6W^2+Q^2,\quad
 \mathrm{tr}\mathcal S_W\mathcal T_W=2W^2,\quad
 \mathrm{tr}\mathcal T_W^2=Q^2.
\]

Assim tr(S_W+T_W)²=10W²+2Q² e

\[
 \mathrm{tr}E_{hh}^2=3\mathrm{Riem}^2+\frac{5s^2}{2}W^2+\frac{s^2}{2}Q^2.
\]

O bloco sigma acrescenta (1+4s)Q²+(2s−1)²W²; os dois produtos mistos somam 2sB². Recuperam-se exatamente

\[
 \mathrm{tr}_{13}E=-R+(2-s)Q,
\]
\[
 \mathrm{tr}_{13}E^2=3\mathrm{Riem}^2+left(\frac{s^2}{2}+4s+1\right)Q^2
 +\left(\frac{13s^2}{2}-4s+1\right)W^2+2sB^2.
\]

Não há sinais de norma extras no traço de endomorfismos. A assinatura já está nas contrações geométricas.

## 4. Curvatura efetiva: conferência dos termos que podem mudar C₄

O comutador das misturas fornece [ω_ρ,ω_σ]_ξξ=s(u_ρ⊗u_σ−u_σ⊗u_ρ). Somando a curvatura da conexão do alvo, o bloco sigma é (1+s)A_ρσ. A diferença ∇_ρω_σ−∇_σω_ρ produz exatamente os blocos em B exibidos na fonte; o termo de traço no bloco ξh desaparece pela simetria B_ρσ=B_σρ.

Para verificar o bloco métrico C_ρσ=[ω_ρ,ω_σ]_hh, diagonalize W em uma base Riemanniana e fixe um par a<b. A ação relevante nas componentes é

\[
 (Ch)_{aa}=-sw_a h_{ab},\quad (Ch)_{bb}=sw_bh_{ab},
\]
\[
 (Ch)_{ab}=\frac s4\left[(w_a+w_b)(h_{aa}-h_{bb})
 +(w_b-w_a)\sum_{c\ne a,b}h_{cc}\right],
\]
\[
 (Ch)_{ac}=-\frac s2w_c h_{bc},\quad
 (Ch)_{bc}=\frac s2w_c h_{ac}\quad(c\ne a,b).
\]

Daí, por traço de pequenos blocos,

\[
 \mathrm{tr}C_{ab}^2=-\frac{s^2}{2}\{(w_a+w_b)^2+\sum_{c\ne a,b}w_c^2\}
 =-\frac{s^2}{2}(W^2+2w_aw_b).
\]

Somar pares ordenados dá −s²(5W²+Q²). O traço cruzado seleciona apenas a curvatura seccional K_ab=R_abab e vale sK_ab(Q+w_a+w_b) por par; o fator cruzado 2 e a soma ordenada dão 2sRQ+4s Ric·W.

Também conferi o termo misto de Ω² por componente de alvo de B. Se P_ab é o bloco ξ→h e N_ab o bloco h→ξ, então

\[
 N_{ab}P_{ab}=-\frac s2\{(B^2)_{aa}+(B^2)_{bb}+2B_{ab}^2-2B_{aa}B_{bb}\}.
\]

Os dois blocos diagonais de Ω² e os pares ordenados produzem

\[
 -2s(4B^2-|\mathrm{tr}B|^2)=-8sB^2
\]

quando τ=0. Acrescentar a curvatura base métrica −6Riem² e a contribuição sigma 2(1+s)²(W²−Q²) recupera (3.6) integralmente. A diagonalização é só uma demonstração de identidade polinomial tensorial em assinatura Riemanniana; a continuação algébrica não exige diagonalizar um W Lorentziano real arbitrário.

## 5. Fantasmas e coeficiente universal

Da nota 066, CK=□+Ric em covetores, de modo que E_gh=Ric, tr E_gh=R, tr E_gh²=Ric² e tr Ω_gh²=−Riem². Não se usou K* K no lugar de CK.

[KNOWN] Conferi a fórmula interior b₄ para L=−(∇̂²+E) em [Vassilevich, equação (4.28)](https://arxiv.org/html/hep-th/0306138v3). Seus pesos são E²/2, Ω²/12, RE/6, □E/6 e (12□R+5R²−2Ric²+2Riem²)I/360, depois de separar o fator (4πt)⁻².

[DERIVED] A integral quadrática formal de treze campos reais bosônicos dá +ħ Tr log L_B/2. Um par independente (c,bar c) de quatro componentes Grassmann com ação bar c Qc dá det Q, logo −ħ Tr log L_gh. A matriz graduada 8×8 não representa dois pares independentes: contar −2 seria duplicar os fantasmas. O auxiliar b já eliminado tem operador algébrico de multiplicação e não acrescenta um quinto operador de onda. Portanto os pesos 1/2 e −1 usados na fonte estão corretos nessa normalização.

Como controle da soma, o peso líquido do termo universal proporcional à identidade é 13/2−4=5/2. As parcelas combinam assim:

| Invariante | Coeficiente recomposto |
|---|---:|
| Riem² | 3/4−1/4+1/12+1/72=43/72 |
| Ric² | −1/2−1/72=−37/72 |
| R² | −1/12−1/6+5/144=−31/144 |
| RQ | (2−s)/12+s/12=1/6 |
| Ric·W | s/6 |
| Q² | s²/8+s+1/4−s²/8−s/6−1/12=(5s+1)/6 |
| W² | 13s²/8−s+1/4−s²/8+s/6+1/12=(9s²−5s+2)/6 |
| B² | s/2−s/3=s/6 |
| □R | −1/12−1/6+1/12=−1/6 |
| □Q | (2−s)/12 |

Logo (4.2) confere termo a termo. Usar B²=□Q/2−Ric·W+Q²−W² cancela Ric·W e dá (4.3), inclusive o coeficiente final □Q/6.

## 6. Avaliação do coeficiente e limites preservados

Com s=4 e os invariantes do fundo, a soma fornece tr E=18x−3, tr E²=588x²−24x+9/2 e tr Ω²=−300x²−84x−9. A combinação final dos dois b₄ apresentados pode ser conferida no denominador comum 480:

\[
 \frac12b_{4,B}-b_{4,gh}
 =\frac{(62160-24960)x^2+(-4240+12320)x+(377-1432)}{480}
 =\frac{7440x^2+1616x-211}{96}.
\]

A parcela de divergência total é −□R/6−□Q/6=5x/4, e sua subtração formal muda 1616 para 1496, sem alterar a parcela x². Não a descartei como integral de bordo nula num domínio aberto.

O controle puramente gravitacional também confere ao retirar o bloco sigma inteiro: C₄=53 Riem²/90−29R²/80 no fundo Einstein. Apenas pôr u=0 mantendo os três campos sigma soma três escalares minimais; não é o mesmo teste.

O alcance matemático permanece o coeficiente local **diferencial** on-shell do calibre e da parametrização adotados. Não foi construída uma medida completa, um determinante Lorentziano global, a rotação global de Wick, o tratamento de todos os zero-modos ou uma extensão off-shell da Hessiana. A fonte conserva essas distinções; a direção conforme negativa e os fatores ultralocais não foram contados como cancelamentos não calculados de C₄. A análise não implica QME interagente nem completude UV.

[REAL] Os pins e a leitura do recibo atual estão no manifesto. [DERIVED] As comparações e contrações deste parecer são próprias e escritas. Não executei CAS, Lean, um.py nem o script de calor; nenhuma fonte foi alterada. Não atribuo aprovação ao operador ou a outro agente.
