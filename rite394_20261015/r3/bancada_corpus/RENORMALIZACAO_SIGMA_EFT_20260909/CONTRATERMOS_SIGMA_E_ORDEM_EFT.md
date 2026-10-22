# Primeiro laço sigma e organização da teoria efetiva

[DERIVED — demonstração escrita; KNOWN — coeficiente universal do núcleo de calor] Esta nota calcula a divergência logarítmica do setor sigma quântico em uma métrica externa suave de dimensão quatro. Dá contra-termos explícitos e um exemplo que impede absorvê-los apenas nos parâmetros da ação de duas derivadas. Não é o determinante completo do sistema Einstein–sigma acoplado: os laços métricos, fantasmas e blocos mistos têm de ser calculados para esse outro enunciado.

O cálculo acrescenta uma obrigação concreta à passagem interagente da entrega 067. A adoção da ação permanece [INPUT/POSTULATE]; o resultado não é deduzido somente da normalização dos pesos.

## 1. Assinatura, campos e estatuto do cálculo

Trabalhe inicialmente em assinatura euclidiana, com g positiva, em quatro dimensões, e campo φ:M→S³ unitária. A ação do setor é

\[
S_\sigma=\frac c2\int_M\mu_g\,Q,\qquad
Q=g^{\mu\nu}\langle u_\mu,u_\nu\rangle,
\quad u_\mu=d\phi(\partial_\mu),\quad c>0.
\]

Defina W_{µν}=〈uµ,uν〉 e W²=W_{µν}W^{µν}. Aqui Q é um escalar de duas derivadas; W é o tensor de derivadas sigma. Não são as condicionais Q_a dos registros probabilísticos das outras notas. Tampouco este Sσ euclidiano escolhe uma continuação global do espaço-tempo cosmológico lorentziano.

Use perturbações tangentes ξ∈φ*TS³ e variação geodésica no alvo. O transporte covariante no alvo fornece

\[
\delta^2S_\sigma(\xi,\xi)
=c\int\mu_g\big(|D\xi|^2-\langle\xi,\mathcal E\xi\rangle\big),
\quad
\mathcal E\xi=\sum_\mu R^{S^3}(\xi,u_\mu)u^\mu.
\]

Com R(X,Y)Z=〈Z,Y〉X−〈Z,X〉Y na esfera, escreva

\[
U=\sum_\mu u_\mu\otimes u^\mu,\qquad
\boxed{\mathcal E=Q I_3-U,\quad P=-(D^2+\mathcal E).}
\]

A redefinição ξ_can=√c ξ remove o fator constante da Hessiana. Um fator constante de medida pode modificar termos locais de normalização ou escolhas de escala; não elimina o coeficiente quartico em derivadas calculado abaixo. O operador de curvatura do fibrado é

\[
\Omega_{\mu\nu}=u_\mu\otimes u_\nu-u_\nu\otimes u_\mu.
\]

Essas fórmulas são a Hessiana covariante do modelo sigma, com o vínculo da esfera tratado geometricamente. Não se usa a Hessiana de quatro componentes extrínsecos livres. O cálculo da divergência local admite fundo geral; o exemplo posterior também satisfaz a equação sigma.

## 2. Contração dos índices do alvo

O alvo tem dimensão tangente três. A ciclicidade do traço dá

\[
\operatorname{tr}U=Q,\qquad\operatorname{tr}U^2=W^2,
\]
\[
\boxed{\operatorname{tr}\mathcal E=2Q,\qquad
\operatorname{tr}\mathcal E^2=Q^2+W^2.}
\]

Para vetores v,w, ponha A=v⊗w−w⊗v. Então tr A²=2(〈v,w〉²−|v|²|w|²). Somando as direções da base,

\[
\boxed{\operatorname{tr}\Omega_{\mu\nu}\Omega^{\mu\nu}
=2(W^2-Q^2).}
\]

O sinal negativo possível do traço de Ω² decorre de Ω ser antissimétrica; não é uma probabilidade negativa. Essas identidades foram verificadas para jatos arbitrários de uma matriz real 3×4, além da derivação algébrica acima.

## 3. Coeficiente local de quatro derivadas

[KNOWN] Para P=−(D²+E) em dimensão quatro, sem contribuição de bordo, a expansão do traço de calor tem a forma K(t)∼(4πt)⁻²∫µ tr(I+t b₂+t² b₄+…). A fórmula universal e suas convenções são as equações (2.2), (2.6), (4.27) e (4.28) de [Vassilevich](https://arxiv.org/html/hep-th/0306138v3). A convenção dá curvatura escalar positiva à esfera. A divergência logarítmica da ação a um laço é determinada por esse coeficiente. A referência distingue esse cálculo euclidiano de uma construção global lorentziana em sua seção 2.3.

Escrevendo B₄ já com o traço no alvo, a fórmula usada é

\[
B_4=\operatorname{tr}\left[
\frac16D^2\mathcal E+\frac16R\mathcal E+\frac12\mathcal E^2
+\frac1{12}\Omega_{\mu\nu}\Omega^{\mu\nu}
+\frac{I_3}{360}(12\Box R+5R^2-2|\mathrm{Ric}|^2+2|\mathrm{Riem}|^2)
\right].
\]

Substituir os traços calculados dá o resultado específico do modelo:

\[
\boxed{\begin{aligned}
B_4={}&\frac13Q^2+\frac23W^2+\frac13RQ\\
&+\frac1{120}\left(5R^2-2|\mathrm{Ric}|^2+2|\mathrm{Riem}|^2\right)
+\frac13\Box Q+\frac1{10}\Box R.
\end{aligned}}
\tag{3.1}
\]

Em variedade fechada, os dois termos de divergência integram a zero. Em região com bordo ou funções de acoplamento variáveis, só podem ser retirados depois de contabilizar os termos correspondentes. Não se afirma que (3.1) inclua os coeficientes de bordo do núcleo de calor.

Para fixar o fator global sem misturar convenções de polos, introduza um corte de tempo próprio ρ⁻², com ρ uma escala UV distinta da constante cosmológica Λ. Defina

\[
\Gamma_1=-\frac{\hbar}{2}\int_{\rho^{-2}}^{\infty}\frac{dt}{t}\,K(t).
\]

A parcela logarítmica divergente é

\[
\boxed{\Gamma_{1,\log}
=-\frac{\hbar}{2(4\pi)^2}\ln\frac{\rho^2}{\mu^2}
\int_M\mu_g B_4.}
\tag{3.2}
\]

Assim, nesta convenção euclidiana, o contra-termo que cancela a divergência é a expressão oposta. O cálculo usa somente o limite t→0; se P possuir autovalores negativos ou zero, o infravermelho deve ser regulado separadamente. Somar uma massa positiva a P permite fazer isso em um exemplo compacto. As parcelas de maior grau em dφ em (3.1) não são removidas por esse regulador.

Os termos Q², W² e RQ são covariantes sob difeomorfismos e invariantes sob as isometrias do alvo. A presença de uma divergência covariante não é, por si, uma anomalia de calibre: ela pode ser subtraída por termos da mesma simetria. A possibilidade de manter todas as identidades quânticas no sistema acoplado é uma obrigação distinta, tratada pela análise BV.

## 4. Um fundo exato mostra por que os termos novos não podem ser omitidos

Considere um toro plano T⁴, com a primeira coordenada x de período 2π e métrica externa fixa. Para k inteiro, escolha

\[
\phi_k(x)=(\cos kx,\sin kx,0,0).
\]

Temos φ²=1, Q=k², W²=k⁴ e tensão sigma

\[
\tau=\partial_x^2\phi_k+Q\phi_k=0.
\]

O referencial tangente e₁=(−sin kx,cos kx,0,0), e₂=(0,0,1,0), e₃=(0,0,0,1) é global e paralelo para a conexão puxada. Nele,

\[
\Omega=0,\qquad\mathcal E=\operatorname{diag}(0,k^2,k^2),
\qquad P=-\partial^2I_3-\mathcal E.
\]

O traço de calor local é, até termos de imagens do toro exponencialmente pequenos em t,

\[
K(t;x,x)=(4\pi t)^{-2}\left(1+2e^{tk^2}\right),
\]

e seu coeficiente de t² dentro do parêntese é k⁴. Isso confere (3.1) diretamente, sem depender apenas da contração geral. Esse operador não é apresentado como um vácuo estável: o exemplo testa a divergência UV local, e autovalores baixos negativos são uma questão infravermelha separada.

O funcional clássico sigma nesse conjunto de fundos vale c k² Vol(T⁴)/2. Um deslocamento de termo constante e de c produziria A+B k². Nenhuma escolha de A,B constante em k reproduz k⁴ para todos os inteiros: k=0 força A=0, k=1 força B=1, e k=2 dá 4 em vez de 16. A discrepância é 12.

Além disso, todo contra-termo proporcional à equação sigma e toda divergência total integra a zero nesses fundos. Logo o termo quartico não pode ser removido dessa família apenas por redefinição local do campo sigma proporcional à sua equação. **O setor sigma em métrica externa não fecha sob renormalização usando somente o termo constante e a ação de duas derivadas.** Precisa dos termos novos, já em um laço.

O qualificativo “métrica externa” é essencial. Se a métrica for quantizada, redefinições métricas e diagramas mistos devem ser incluídos no problema completo. O cálculo acima não prova um valor para o coeficiente total gravitacional, nem exclui cancelamentos que exigiriam demonstração própria. Também não é uma refutação observacional da TGL: identifica uma obrigação matemática da ação interagente adotada.

## 5. Organização por ordem na teoria efetiva

[DERIVED — contagem de potência] Após normalização canônica local dos campos e fixação de calibre de ordem dois, cada propagador principal cai como p⁻². Para um grafo conectado em quatro dimensões, com L laços, I linhas internas e vértices de d_v derivadas, o grau superficial de momento é

\[
\mathcal D=4L-2I+\sum_v d_v.
\]

Usar L=I−V+1 fornece

\[
\boxed{\mathcal D=2+2L+\sum_v(d_v-2).}
\tag{5.1}
\]

Se todos os vértices vêm dos termos de duas derivadas, as ordens são quatro em um laço, seis em dois laços, e assim por diante. Inserções de potenciais ou parâmetros de massa contam com sua ordem correspondente; a constante cosmológica pode ser contada como ordem dois na expansão de baixa curvatura. Curvatura e derivadas de fundo entram nos invariantes locais com essa mesma graduação. Identidades e cancelamentos podem reduzir divergências; (5.1) é uma contagem superficial e não prova que todo operador permitido tenha coeficiente não nulo.

Uma ação efetiva deve admitir a torre

\[
S_{\mathrm{EFT}}=S_2+\sum_i c_{4,i}(\mu)\int\mu_g\,\mathcal O_{4,i}
+\sum_i c_{6,i}(\mu)\int\mu_g\,\mathcal O_{6,i}+\cdots.
\]

O cálculo de (3.1) dá explicitamente contribuições a alguns c₄. Suas partes finitas exigem condições de renormalização ou informação de uma teoria mais fundamental; o coeficiente divergente não as fixa sozinho. A organização efetiva permite tratar ordens finitas sem afirmar convergência da torre. O papel dessa separação em gravidade é desenvolvido por [Donoghue, seções 2–3](https://arxiv.org/html/gr-qc/9405057v1).

Ao fixar a ordem em derivadas, número de campos externos e simetrias, há um problema de subtração finito naquela ordem. Sem impor isometria do alvo, funções arbitrárias do campo podem aparecer como acoplamentos e essa afirmação precisa ser refinada; o modelo desta nota usa o alvo homogêneo S³ e sua simetria O(4). A existência de produtos renormalizados com todas as identidades BRST não decorre da contagem: exige o contrato analítico e cohomológico correspondente.

Os operadores de mais derivadas são inserções perturbativas da expansão efetiva. Tratá-los como uma ação exata nova e inverter seu operador de ordem superior pode introduzir polos e graus de liberdade adicionais; essa outra teoria não é construída pela expansão formal. Tampouco a positividade do estado livre de 067 demonstra, por si, positividade não perturbativa da teoria interagente.

## 6. Como esses termos permanecem ligados aos mesmos dados

No representante probabilístico livre com Φ(P)=(g[P],φ[P]), cada funcional covariante acima pode ser puxado:

\[
S_{\mathrm{EFT},P}=S_{\mathrm{EFT}}\circ\Phi.
\]

O argumento AR=Id e a injetividade de A* do adendo 067 não dependem de a ação ambiente ter apenas duas derivadas. Para uma ação local truncada, integração por partes fornece

\[
E_P=A^*E_X,\qquad A^*E_X=0\iff E_X=0
\]

no interior, usando o mesmo inverso à direita e as mesmas condições de suporte. Portanto os novos contra-termos podem ser expressos pelos dados e continuam variacionalmente equivalentes ao modelo ambiente correspondente na classe livre. A ordem diferencial do operador E_X muda; as condições de Cauchy e o tratamento perturbativo dessa ordem não são substituídos pela identidade funcional.

A igualdade acima é clássica/formal por ordem. **Ela não demonstra equivalência entre integrais funcionais quantizadas em P e em X.** Uma transformação que depende de derivadas e possui fibras redundantes exige controle de medida, determinantes e gauge dessas fibras. O transporte simplético linear de 067 é suficiente para seu estado linear, mas não paga esse jacobiano funcional interagente. Se a teoria quântica for definida diretamente pela álgebra ambiente e seus observáveis puxados, isso deve ser declarado como definição; não é uma quantização independente de todas as probabilidades finas.

## 7. Resultado que a sessão codificadora pode incorporar

- [DERIVED + KNOWN] Coeficiente sigma B₄ de (3.1), com o estatuto de métrica externa euclidiana e os termos de bordo explicitados.
- [DERIVED] Teste do círculo geodésico no toro, demonstrando a necessidade de termos de quatro derivadas no setor sigma externo.
- [DERIVED] Contagem de potência (5.1), organização efetiva e transporte funcional dos operadores aos mesmos dados na classe livre.
- [REAL — controle simbólico] Treze identidades exatas conferidas no recibo associado; nenhuma compilação Lean foi realizada.
- [OPEN] Determinante completo métrica–sigma–ghost, anomalias quânticas do contrato adotado, medida interagente em probabilidades, condições finitas de renormalização e conclusão UV da teoria reivindicada.

Nenhum `um.py`, original ou nota congelada foi alterado ou executado. A escolha de uma descrição efetiva não encerra o objetivo de altas energias; estabelece uma etapa concreta para chegar a ele com os termos necessários presentes.
