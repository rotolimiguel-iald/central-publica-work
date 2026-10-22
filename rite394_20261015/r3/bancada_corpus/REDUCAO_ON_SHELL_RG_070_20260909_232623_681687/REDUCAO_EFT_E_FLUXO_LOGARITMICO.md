# Redução on-shell de C4 e fluxo logarítmico dos operadores EFT

09/09/2026, arco 070. [DERIVED — prova algébrica escrita] [REAL — 16 controles simbólicos novos, todos PASS]. Nenhum dos 31 controles de operadores da entrega 069 foi reexecutado. Não houve Lean, execução/importação de um.py ou alteração de fontes existentes.

**Resultado.** O coeficiente acoplado de uma volta admite, módulo equações e divergências, o representante

\[
\boxed{\begin{aligned}
\mathcal C_4\simeq{}&\frac{43}{72}\mathcal E_4-\frac{11}{2}\Lambda^2
 +\Lambda\left(\frac23-\frac{11s}{4}\right)Q\\
&+\left(-\frac{13s^2}{16}+\frac{7s}{6}+\frac16\right)Q^2
 +\left(\frac{27s^2}{8}-s+\frac13\right)W^2,
\qquad s=\kappa c .
\end{aligned}}
\tag{1}
\]

Aqui E4 é a densidade escalar de Euler **sem** o fator 1/(32π²): E4=Riem²−4Ric²+R². A assinatura e os coeficientes são os da [nota acoplada 069](../CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553/COEFICIENTE_COMPLETO_UMA_VOLTA.md). A relação ≃ identifica funcionais locais que diferem pelo ideal das equações ou por divergências admissíveis; não afirma igualdade ponto a ponto após simplesmente apagar as últimas.

Para s=4, os coeficientes de Q² e W² são −49/6 e 151/3. Sua combinação FRW é 3A1+A2=155/6. O sinal e o fator do fluxo RG são fixados abaixo por uma relação explícita entre acoplamento bare e renormalizado; os valores finitos permanecem entradas. Uma passagem local formal de convenções Euclidiana/Lorentziana também é declarada, sem postular uma rotação global de Wick.

## 1. Entradas e escopo do quociente

[INPUT — ação e prescrição já adotadas] Usam-se a ação Einstein–sigma de duas derivadas, alvo S³ de curvatura seccional +1, s=κc, constantes Λ,κ,c, e o coeficiente diferencial de uma volta normalizado como na nota 069. A medida ultralocal, a fase conforme e os requisitos de bordo continuam com os contratos daquela nota. Se outra prescrição acrescentar uma densidade local de medida, seus coeficientes devem ser somados separadamente; não se supõe cancelamento por uma medida não calculada.

Escreva u=dφ, W_ab=〈u_a,u_b〉, Q=tr_g W e B_ab=D_a u_b. B é o Hessiano do mapa; o símbolo B_FRW usado adiante é outro objeto, uma combinação de acoplamentos. As equações de fundo são

\[
E_{ab}=G_{ab}+\Lambda g_{ab}-s(W_{ab}-g_{ab}Q/2)=0,
\qquad \tau=D^a u_a=0.
\tag{2}
\]

Divergências são identificadas apenas em funcionais com suporte e/ou condições de bordo apropriados. Num domínio cosmológico aberto, a corrente de bordo deve ser guardada se essas condições não forem dadas. Retém-se Euler em (1) para mostrar o coeficiente topológico; se o quociente também identifica Euler/Pontryagin, pode-se apagar esse gerador para a dinâmica local de bulk. Isso não apaga a contribuição topológica ao funcional global. Não aparece Pontryagin neste C4; essa ausência não é uma prova sobre anomalias de número fantasma um.

O conjunto {1,Q,Q²,W²,E4} é uma base conveniente de representantes para **a redução deste coeficiente**, na classe natural e na ordem de derivadas examinadas. Não se afirma aqui classificação completa de todos os operadores EFT ou de toda a cohomologia local. Não se impõe a relação especial W²=Q²/3 do FRW antes de terminar a redução geral.

## 2. Prova direta da redução

A identidade de Bochner na aplicação harmônica dá

\[
\tfrac12\Box Q=B^2+\operatorname{Ric}\!:\!W-Q^2+W^2.
\]

Ela transforma (4.2) de 069 na expressão (4.3), com os termos mistos B² e Ric:W eliminados. Substituir Riem²=E4+4Ric²−R² produz

\[
\begin{aligned}
\mathcal C_4={}&\frac{43}{72}\mathcal E_4+\frac{15}{8}\operatorname{Ric}^2
 -\frac{13}{16}R^2+\frac16RQ\\
&+\left(s+\frac16\right)Q^2
 +\left(\frac32s^2-s+\frac13\right)W^2
 -\frac16\Box R+\frac16\Box Q.
\end{aligned}
\tag{3}
\]

Pelas equações (2),

\[
\operatorname{Ric}=\Lambda g+sW,\quad R=4\Lambda+sQ,
\quad \operatorname{Ric}^2=4\Lambda^2+2\Lambda sQ+s^2W^2.
\tag{4}
\]

A parcela constante de (3) é (15/8)4Λ²−(13/16)16Λ²=−11Λ²/2. A parcela ΛQ é [15s/4−13s/2+2/3]ΛQ. Os termos Q² e W² dão os dois polinômios de (1). As derivadas restantes são

\[
-\frac16\Box R+\frac16\Box Q=\frac{1-s}{6}\Box Q.
\tag{5}
\]

Portanto, nas soluções, a igualdade ponto a ponto completa é C4=C_red+(1−s)□Q/6, onde C_red é o lado direito de (1). A equivalência de funcionais segue sob o contrato de divergências da seção 1.

## 3. Certificado explícito no ideal e representante por redefinição

[DERIVED] Pode-se exibir o resto algébrico inteiro, sem usar apenas uma substituição verbal “on-shell”. **C42_poly** denota o polinômio tensorial escrito em (4.2) de 069, estendido como expressão a jatos arbitrários. Essa extensão escolhida não é alegada como o coeficiente da verdadeira Hessiana off-shell, que contém termos adicionais de equações de fundo não calculados em 069.

Ponha e=tr_g E. As identidades algébricas, válidas fora das soluções, são

\[
R=4\Lambda+sQ-e,\qquad
\operatorname{Ric}=\Lambda g+sW+E-\tfrac12eg,
\]
\[
\operatorname{Ric}^2=4\Lambda^2+2\Lambda sQ+s^2W^2
 +2sW:E-(2\Lambda+sQ)e+E:E.
\tag{6}
\]

A identidade completa de Bochner acrescenta 〈u^a,D_aτ〉 ao lado direito da primeira fórmula da seção 2. Além disso,

\[
\langle u^a,D_a\tau\rangle
=\nabla_a\langle u^a,\tau\rangle-\langle\tau,\tau\rangle.
\]

Resulta o certificado exato

\[
\boxed{\mathcal C_{42,\mathrm{poly}}
 =\mathcal C_{\mathrm{red}}+\nabla_a J^a+E^{ab}M_{ab}
 +\frac{s}{6}\langle\tau,\tau\rangle,}
\tag{7}
\]
\[
\begin{aligned}
M_{ab}={}&\frac{15s}{4}W_{ab}
 +\left[\frac{11\Lambda}{4}-\left(\frac s4+\frac16\right)Q\right]g_{ab}
 +\frac{15}{8}E_{ab}-\frac{13}{16}e g_{ab},\\
J^a={}&\frac{1-s}{6}\nabla^aQ+\frac16\nabla^a e
 -\frac s6\langle u^a,\tau\rangle.
\end{aligned}
\tag{8}
\]

Tudo é local, natural e polinomial nos jatos diferenciados; não se invertem dy ou curvaturas. Esse certificado foi conferido simbolicamente após as identidades tensorais exibidas, com s e Λ livres.

A ligação variacional é explícita. Nas convenções físicas anteriores,

\[
\delta S=\int\mu_g\left(\frac1{2\kappa}E^{ab}\delta g_{ab}
 -c\langle\tau,\delta\phi\rangle\right)+\text{bordo}.
\]

Para um parâmetro formal χ de ordem ℏ, as redefinições

\[
\delta g_{ab}=2\kappa\chi M_{ab},\qquad
\delta\phi=-\frac{\chi s}{6c}\tau
\tag{9}
\]

geram χ(E:M+s|τ|²/6) na ação. A mudança do mapa é tangente e pode ser realizada por Exp_φ. Assim um funcional S+χ C42_poly é reescrito, até O(χ²) e bordo, como S nos campos redefinidos mais χ C_red. O sinal inverso é usado se a intenção for acrescentar em vez de retirar o resto. Não se reivindica uma transformação não perturbativa invertível global.

(7)–(9) escolhem um representante; **não determinam a parte off-shell omitida do coeficiente original**, nem o dicionário físico dos campos após redefinição. Inclusive M pode ser não nulo em uma solução clássica. Logo não se deduz uma backreaction off-shell única de C4 on-shell.

## 4. Coeficientes logarítmicos e RG: convenção Euclidiana explícita

Defina K=ℏ/(4π)². A convenção diferencial de 069 é

\[
\Gamma^{E}_{1,\log}=-K\log\frac{\rho^2}{\mu^2}
 \int\mu_g\,\mathcal C_4.
\tag{10}
\]

Essa normalização deriva do coeficiente local de calor e da expressão por tempo próprio; a fórmula universal e a diferença entre calor Euclidiano e coeficientes locais Lorentzianos estão em [Vassilevich, §§2.1–2.3 e equação (4.28)](https://arxiv.org/html/hep-th/0306138v3). Aqui (10) fixa a convenção, sem pressupor um determinante global no nosso espaço-tempo.

Escolha acoplamentos Euclidianos g_i^E multiplicando diretamente os operadores da tabela. Ao retirar o polo logarítmico por um contratermo de sinal oposto a (10), defina

\[
g_{i,B}^E=g_i^E(\mu)+K A_i\log\frac{\rho^2}{\mu^2}.
\tag{11}
\]

A independência do bare em relação a μ dá, na primeira ordem em ℏ,

\[
\boxed{\mu\frac{d g_i^E}{d\mu}=2K A_i+O(\hbar^2).}
\tag{12}
\]

| Operador multiplicado por g_i^E | Coeficiente A_i |
|---|---|
| 1 | −11Λ_E²/2 |
| Q_E | Λ_E(2/3−11s/4) |
| Q_E² | A1=−13s²/16+7s/6+1/6 |
| W_E² | A2=27s²/8−s+1/3 |
| E4_E, não normalizada | 43/72 |
| Pontryagin | 0 neste coeficiente |

Por isso g_i^E(μ)=g_i^E(μ0)+2K A_i log(μ/μ0)+O(ℏ²), tratando os parâmetros dentro de A_i no nível de árvore. Sua própria evolução altera esse resultado somente na ordem seguinte. Se a derivada escolhida for em log μ², o coeficiente é K A_i, sem o fator 2. Os g_i(μ0) são parâmetros finitos independentes da determinação do logaritmo.

Esses são fluxos dimensionais no representante escolhido. Não incluem termos de escala canônica que apareceriam ao tornar acoplamentos adimensionais. Tampouco são uma separação única dos fluxos de κ,c,Λ: no quociente on-shell, R=4Λ+sQ, de modo que um coeficiente de R pode ser redistribuído entre os de 1 e Q e uma redefinição da métrica. Fixar separadamente a normalização de Einstein é uma escolha adicional de esquema/campos. Não se infere β_κ única da tabela.

## 5. Conversão local formal para os b_i Lorentzianos da fonte FRW

[INPUT — convenção de continuação de coeficientes, explicitada aqui] Para relacionar a tabela anterior aos coeficientes da [fonte quartica](../RENORMALIZACAO_SIGMA_EFT_20260909/FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md), adote formalmente

\[
t_L=-i\tau_E,\quad g_L^{W}=-g_E,\quad
S_E=-iS_L^{W}.
\tag{13}
\]

O sobrescrito W indica apenas a regra local de continuação. Não se afirma que o fundo Lorentziano completo possua essa seção Euclidiana global, nem que φ ou estados suaves arbitrários admitam continuação analítica global.

Nessa regra, Q_L^W=−Q_E, R_L^W=−R_E, (W_L²)^W=W_E² e (E4_L)^W=E4_E. O jacobiano temporal em μ_L é −i; portanto L_E=−L_L^W. A ação de duas derivadas mantém c_E=c_L e κ_E=κ_L, enquanto Λ_E=−Λ_L. A mesma relação segue de continuar Ric_L=Λ_L g_L+sW para Ric_E=−Λ_L g_E+sW.

Para o setor quartico, se a ação Lorentziana contém +b1 Q_L²+b2 W_L², os coeficientes Euclidianos satisfazem

\[
g_{Q^2}^E=-b_1,\qquad g_{W^2}^E=-b_2.
\tag{14}
\]

Assim, **nessa convenção**, (12) equivale a

\[
\boxed{\mu\frac{db_1}{d\mu}=-2K A_1,\qquad
\mu\frac{db_2}{d\mu}=-2K A_2.}
\tag{15}
\]

Equivalentemente, o bare Lorentziano é b_i,B=b_i(μ)−K A_i log(ρ²/μ²). A mudança de sinal não vem de substituir uma assinatura dentro da fórmula C4 e esquecer a ação: ela inclui (13). Ao usar outra convenção de ação, assinatura ou identificação de coeficientes, (11)–(12) continuam sendo a tabela Euclidiana definida e a conversão deve ser refeita. Não se igualam silenciosamente b_i e g_i^E.

## 6. Consequência FRW e valores que continuam livres

Para φ=id em g=dr²−a²γ, Q=−3x e W²=3x², com x=a⁻². Portanto

\[
A_1Q^2+A_2W^2=3A_Bx^2,\qquad
\boxed{A_B=3A_1+A_2=\frac{15s^2}{16}+\frac{5s}{2}+\frac56.}
\tag{16}
\]

Em s=4,

\[
A_1=-\frac{49}{6},\quad A_2=\frac{151}{3},\quad
A_B=\frac{155}{6},\qquad 3A_B=\frac{155}{2}.
\]

Para o fundo original Λ=3/4, E4=3/2−12x e □Q=−3x/2. Substituir em (1) e acrescentar (5) recupera exatamente

\[
\mathcal C_4=\frac{7440x^2+1616x-211}{96}.
\]

**Precisão sobre divergências:** depois da troca de Bochner e da redução, (5) vale 3x/4 nesse fundo. Os 5x/4 de 069 eram a parcela explicitamente divergente na expressão (4.2), antes dessa integração por partes. A transformação também desloca parte dos demais termos para a corrente; as duas densidades totais C4 coincidem. Não se deve comparar somente as parcelas divergentes de representantes diferentes e declarar erro no coeficiente.

Se B_FRW=3b1+b2 na ação Lorentziana escolhida, (15) fornece

\[
\boxed{\mu\frac{dB_{\rm FRW}}{d\mu}=-2K A_B
=-\frac{155}{3}K\quad(s=4),}
\tag{17}
\]

\[
B_{\rm FRW}(\mu)=B_{\rm FRW}(\mu_0)
-\frac{155}{3}K\log\frac{\mu}{\mu_0}+O(\hbar^2).
\]

O valor finito B_FRW(μ0), inclusive seu sinal, continua livre até se fixar uma condição de renormalização. A positividade de A_B para s>0 não fixa o sinal desse valor finito. O coeficiente A1 negativo em s=4 também não é uma instabilidade física por si: trata-se de uma direção de fluxo no espaço de contratermos.

[DERIVED, condicionado ao representante Lorentziano] Na ação truncada que contém apenas esses quarticos além dos termos de árvore, a fonte local já derivada é ρ4=−3B_FRW/a⁴ e p4=ρ4/3. Mantendo a geometria de fundo fixa ao diferenciar o acoplamento, (17) dá

\[
\mu\partial_\mu\rho_4=155K/a^4,\qquad
\mu\partial_\mu p_4=\frac{155K}{3a^4}\quad(s=4).
\tag{18}
\]

Isso é a variação da **parcela local escolhida**, não uma previsão de energia quântica total dependente de μ. Na grandeza física renormalizada, a dependência explícita dos laços e outras parcelas deve cancelar a dependência dos acoplamentos. O resultado não fixa um sinal de energia de vácuo.

Também não se impõe μ=μ(r), μ=a⁻¹ ou qualquer outra escala espacial/temporal nesta dedução. Tratar acoplamentos como funções do espaço-tempo altera a variação e a identidade de conservação e exige um procedimento de melhoria RG próprio. A escala μ de (11) não é a coordenada r.

## 7. O que esta redução não determina

A família a_B²=2+2√(1−κB_FRW) cos(r−r0), já construída para uma ação truncada específica, permanece uma solução dessa ação no domínio indicado na nota anterior. A redução de C4 não a promove a solução semiclassica única: coeficientes finitos, redefinições dos campos, renormalizações dos termos de duas derivadas, funcionais não locais e estado contribuem na mesma ordem relevante. As relações κc=4 e Λ=3/4 são valores do fundo de árvore, não identidades RG provadas em toda escala.

Euler é topológico em quatro dimensões apenas com o contrato global/de bordo pertinente; eliminá-lo das equações de bulk não determina sua fase no funcional. A presente conta não calcula H¹(s|d), não remove a anomalia BRST, não produz um estado interagente e não decide uma rota UV. O símbolo β_RG, quando usado para μd/dμ, é distinto do parâmetro β_TGL do atlas.

[REAL] VERIFICACAO_REDUCAO_RG.json registra 16 identidades exatas novas em SymPy 1.14.0: Bochner no polinômio de entrada, redução Euler/Einstein, certificado do resto no ideal e na divergência, coeficientes e combinação FRW, recuperação de C4 e sinais RG definidos por (11)/(15). São controles algébricos sobre as identidades especificadas, não uma nova compilação dos tensores, da Hessiana ou da teoria de campos. Fonte, script e recibo são pinados no manifesto; os arquivos de entrada foram conferidos antes e depois e permaneceram idênticos.
