# PARTITURA MÍNIMA — coerência espectroscópica versus intensidade fotométrica

**Data:** 05/11/2026  
**Estatuto:** **[DECLARADO pelo Kimi]**, até derivação da ponte astrofísica, decisão do operador e conferência da gerência.  
**Estado:** `OPEN_DERIVATION_REQUIRED` · `NO_DATA_OPENED` · `NO_TGL_LIKELIHOOD_EVALUATED`.  
**Escopo:** forma matemática da rota, nulo rival, estatística e derivações pendentes. Nenhuma abertura de DESI/Euclid, nenhum ajuste, nenhuma execução de natureza e nenhum novo veredito.

---

## 1. A pergunta correta

**Não** perguntar: “como a TGL corrige a fotometria para a espectroscopia?”

Perguntar:

> **Existe uma previsão TGL, sem parâmetro ajustado, para a coerência de um campo ou de uma linha, enquanto a intensidade integrada permanece preservada, que se separe do rival por pelo menos 5σ em duas determinações independentes?**

A rota é fisicamente admissível porque defasagem pode reduzir coerências sem reduzir populações. Ela **ainda não é um teste TGL pronto**, porque a amplitude e a dependência com redshift não foram derivadas.

A identificação de K com fator de fluxo ou de deslocamento espectral continua fora da derivação atual: sob H1, populações de momento, energia e direção são preservadas. [DERIVACAO_RE_02nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Crota_RE_dualidade_02nov%5CDERIVACAO_RE_02nov.md&line=22&text=Sob%20H1%20%5BDERIVED%5D%3A%20popula%C3%A7%C3%B5es%20em%20momento%20n%C3%A3o%20mudam%2C%20logo%20n%C3%BAmero%2C%20energia%20e%20dire%C3%A7%C3%A3o%20do%20f%C3%B3ton%20se%20conservam. "citation")

---

## 2. O que já está demonstrado: coerência fora da diagonal, total preservado

Para um canal de defasagem na base de \(K\), escreva

\[
\rho_{ij}(T)=D_{ij}(T)\rho_{ij}(0),
\qquad
D_{ij}(T)=e^{-\Gamma_{ij}T},
\qquad
\Gamma_{ii}=0 .
\]

Na forma de salto hermitiano citada na rota R–E,

\[
\Gamma_{ij}=\frac{\beta}{2}
\left(\sqrt{k_i}-\sqrt{k_j}\right)^2 .
\]

Essa taxa pertence à coerência entre os setores \(i,j\), não à perda da diagonal. [DERIVACAO_RE_02nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Crota_RE_dualidade_02nov%5CDERIVACAO_RE_02nov.md&line=18&text=com%20%CE%93_ij%20%3D%20%C2%BD%CE%B2(%E2%88%9Ak_i%20%E2%88%92%20%E2%88%9Ak_j)%C2%B2. "citation")

Como \(D_{ii}=e^0=1\),

\[
p_i(T)=\rho_{ii}(T)=\rho_{ii}(0)=p_i(0),
\qquad
\operatorname{Tr}\rho(T)=\operatorname{Tr}\rho(0).
\]

Portanto, coerências \(i\neq j\) podem decair enquanto populações e traço permanecem preservados. `dephase_preserves_trace` e `the_trace_is_not_erasable` são resultados algébricos dessa forma, não uma nova observação astrofísica. [TheTraceIsNotErasable](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CTheTraceIsNotErasable.lean&text=%28dephase%20g%20t%20x%29.trace%20%3D%20x.trace "citation")

**Estatuto:** [REAL na forma algébrica]. A identificação desses elementos com coerência óptica astrofísica concreta permanece **[OPEN]**.

### O que `survivingWeight` não autoriza concluir

Em D1a,

\[
N(z)=\ln(1+z),\qquad
w(\beta,z)=e^{-\beta N(z)}=(1+z)^{-\beta}.
\]

Esse é um peso escalar do registro, definido sobre \(N(z)\). Não é, sem hipótese adicional, fração de fótons sobreviventes, atenuação de intensidade ou largura de linha. [TheFlowLawD1a](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CTheFlowLawD1a.lean&text=def%20register%20(z%20%3A%20%E2%84%9D)%20%3A%20%E2%84%9D%20%3A%3D%20Real.log%20(1%20%2B%20z) "citation")

---

## 3. A face espectral: difusão de fase e perfil Lorentziano

Considere um campo de amplitude constante,

\[
E(t)=\sqrt{I_0}\,e^{-i\omega_0t+i\phi(t)},
\]

com incrementos de fase gaussianos, estacionários e de média nula. Se

\[
\left\langle[\phi(t+\tau)-\phi(t)]^2\right\rangle
=2\gamma|\tau|,
\]

a função característica gaussiana fornece

\[
\left\langle e^{i[\phi(t+\tau)-\phi(t)]}\right\rangle
=e^{-\gamma|\tau|}.
\]

Logo,

\[
\boxed{
g_1(\tau)=
\frac{\langle E^*(t)E(t+\tau)\rangle}
{\langle |E(t)|^2\rangle}
=e^{-i\omega_0\tau}e^{-\gamma|\tau|}
}
\]

e o envelope da coerência decai como \(e^{-\gamma|\tau|}\).

Com \(\Omega=\omega-\omega_0\), a transformada é

\[
L_\omega(\Omega)
=\frac{1}{2\pi}\int_{-\infty}^{\infty}
e^{i\Omega\tau}e^{-\gamma|\tau|}\,d\tau
=\frac{1}{\pi}\frac{\gamma}{\Omega^2+\gamma^2}.
\]

Essa densidade é normalizada:

\[
\int_{-\infty}^{\infty}L_\omega(\Omega)\,d\omega=1.
\]

Portanto, se \(I(\omega)=I_{\rm tot}L_\omega(\omega-\omega_0)\), então

\[
\int I(\omega)\,d\omega=I_{\rm tot}.
\]

A difusão de fase **redistribui a linha sem retirar intensidade integrada**.

### Largura e fatores de \(2\pi\)

A meia altura ocorre em \(\Omega=\pm\gamma\). Assim,

\[
\boxed{\Delta\omega_{\rm FWHM}=2\gamma\ \mathrm{rad/s}.}
\]

Como \(\omega=2\pi\nu\), a densidade ganha o Jacobiano \(2\pi\), e

\[
\boxed{\Delta\nu_{\rm FWHM}=\frac{\gamma}{\pi}\ \mathrm{Hz}.}
\]

O kernel é simétrico: não desloca o centroide em valor principal simétrico, nem numa banda finita simétrica. A Lorentziana não possui primeiro momento absoluto; portanto, a afirmação sobre o centroide deve usar uma dessas duas convenções, não uma integral ingênua sobre toda a reta.

**Estatuto:** [KNOWN como consequência de difusão estacionária de fase]. A identificação de \(\gamma\) com o \(\Gamma_{ij}\) da propagação **não foi derivada**.

---

## 4. Por que \(\Gamma_{ij}\neq\gamma\) automaticamente

\[
\Gamma_{ij}:\quad
\rho_{ij}\mapsto e^{-\Gamma_{ij}T}\rho_{ij}
\]

é a taxa de defasagem entre dois setores da matriz densidade, associada ao tempo de propagação \(T\);

\[
\gamma:\quad
g_1(\tau)\propto e^{-\gamma|\tau|}
\]

é a taxa de decaimento da autocorrelação temporal de um campo e de uma linha, associada ao atraso de coerência \(\tau\).

Ter ambas em \(\mathrm{s}^{-1}\) não estabelece igualdade. Para identificá-las, seria necessário demonstrar que:

1. a coerência \(\rho_{ij}\) é precisamente a coerência óptica que determina \(g_1\);
2. \(T\) e \(\tau\) são o mesmo parâmetro dinâmico, incluindo as transformações de tempo e frequência pelo redshift;
3. o emissor, os modos e o acoplamento ao meio fazem a taxa microscópica da propagação coincidir com a taxa de difusão de fase da linha;
4. fatores de 2, relaxação populacional e resposta instrumental foram separados.

Nenhum desses passos decorre apenas dos teoremas atuais.

---

## 5. A ponte astrofísica ainda necessária

Antes de qualquer dado, a derivação deve fornecer quatro peças:

1. **Definição operacional de \(D(z,\tau)\).** Dizer se é atenuação de \(\rho_{ij}\), coerência mútua entre modos ou \(g_1\) de uma linha; fixar modos, base, normalização e se \(\tau\) é tempo do emissor ou do detector.
2. **Lei de caminho.** Derivar \(T(z)\), ou justificar por que o parâmetro do semigrupo é \(N(z)=\ln(1+z)\), incluindo as transformações de tempo e frequência pelo redshift. D1a fornece \(N(z)\), não uma trajetória óptica completa.
3. **Mapa microscópico sem parâmetro livre.** Derivar \(\Gamma_{ij}(z)\) e, se houver alargamento, \(\gamma(z)\) a partir de \(K\), β, modos e acoplamento, sem postular \(\Gamma_{ij}=\gamma\).
4. **Regra de composição.** Demonstrar como emissão e propagação atuam sobre o mesmo campo. Somente sob independência e multiplicatividade demonstradas se poderia escrever
   \[
   D(z,\tau)=e^{-\Gamma_{ij}T(z)}e^{-\gamma(z)|\tau|}.
   \]
   Essa fatoração é hipótese adicional, não resultado atual.

**Parede medida:** falta a ponte \(K,\beta,\text{modos},\text{trajeto}\mapsto D(z,\tau)\). Não se escolhe amplitude ou cromaticidade pelo ajuste.

---

## 6. Observáveis e nulo rival

### Contraste principal

Para cada réplica \(a\), defina um vetor de coerência calibrado:

\[
\mathbf y_a=
\left(\Re g^{(1)},\Im g^{(1)},V,P_1,\ldots,P_m\right)_a,
\]

com PSF, máscara, seleção e pesos tratados igualmente nos dados e nos nulos. Componentes correlacionados não contam como detecções independentes.

Os coeficientes de perfil são definidos por

\[
P_{a,j}=\int dr\,w_j(r)\,
\Re\!\left[e^{-i\phi_T(r)}g_a^{(1)}(r)\right],
\]

com \(w_j\), \(\phi_T\), suporte de integração e binagem congelados antes do unblinding.

Para dois canais de intensidades \(I_1,I_2\),

\[
V=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}
=\frac{2\sqrt{I_1I_2}}{I_1+I_2}|g^{(1)}|.
\]

A igualdade \(V=|g^{(1)}|\) vale somente para intensidades iguais. O nulo de visibilidade não deve ser fixado automaticamente em zero: ruído e retificação podem gerar viés positivo.

### Controle de intensidade

Use, por exemplo, \(Q_I=\ln(I/I_0)\) ou uma amplitude insensível à fase, medida nos mesmos objetos e estratos de magnitude, S/N, PSF e redshift. Os dois modelos devem conter a mesma forma funcional de controle de intensidade/seleção:

\[
\boldsymbol\mu_M(X)=B_Mq(X)+\boldsymbol\mu_{M,\mathrm{coh}}(X),
\qquad M\in\{T,N\}.
\]

Se a TGL prevê dependência com \(I\), ela pertence a \(\boldsymbol\mu_T(I)\), e não pode ser removida post hoc.

### Nulo rival

O nulo \(N\) deve preservar máscara, intensidades, seleção, erros de redshift, PSF e ruído, destruindo ou alterando somente a relação de fase. Um rival forte pode incluir defasagem instrumental ou convencional não nula; fixar trivialmente zero não é suficiente.

**Nulo operacional para a defasagem de fase:** fases/pares embaralhados ou simulação equivalente, com a mesma intensidade e resposta instrumental. O modelo TGL deve receber \(D_T\) e ser propagado pelo mesmo modelo de instrumento, máscara, seleção e estimador usado no nulo, mas sem o embaralhamento destrutivo de fases/pares, que pertence somente à construção do nulo.

Photo-z e spec-z, sozinhos, não medem coerência: servem para emparelhamento, estratificação e covariância, não fornecem \(g^{(1)}\), visibilidade ou perfil de fase.

---

## 7. Estatística e o que significa 5σ

Fixe um contraste escalar \(\theta_a=\mathbf a^T\mathbf y_a\). Sejam:

- \(\widehat\theta_a\): centro medido;
- \(\mu_{T,a}\): previsão TGL, ainda por derivar;
- \(\mu_{N,a}\): centro do nulo rival;
- \(\sigma_{\mathrm{eff},a}^2=\mathbf a^TC_{\mathrm{eff},a}\mathbf a\).

### Compatibilidade de cada modelo com o centro

\[
z_{T|d,a}=\frac{\mu_{T,a}-\widehat\theta_a}{\sigma_{\mathrm{eff},a}},
\qquad
z_{N|d,a}=\frac{\mu_{N,a}-\widehat\theta_a}{\sigma_{\mathrm{eff},a}} .
\]

Um valor grande de \(|z_{T|d}|\) exclui aquela previsão numérica dentro do modelo de erros; um valor pequeno indica compatibilidade, não detecção.

### Separação entre TGL e nulo

\[
\Delta_{TN,a}=\mu_{T,a}-\mu_{N,a},
\qquad
S_{TN,a}=\frac{|\Delta_{TN,a}|}{\sigma_{\mathrm{eff},a}} .
\]

Para separação de 5σ:

\[
\boxed{
\sigma_{\mathrm{eff},a}\leq
\frac{|\mu_{T,a}-\mu_{N,a}|}{5}
}
\]

Isso mede **poder**, não detecção. Para uma discriminação observada, o nulo deve ser excluído a 5σ e a previsão TGL deve permanecer compatível, com duas réplicas independentes.

No caso multivariado,

\[
S_{TN}^2=\Delta_{TN}^{T}C_{\mathrm{eff}}^{-1}\Delta_{TN},
\]

com limiar calibrado para dimensionalidade, trials e look-elsewhere. Não converter automaticamente \(\sqrt{\chi^2}\) em z unidimensional.

### Covariância efetiva

\[
C_{\mathrm{eff},a}
=C_{\mathrm{stat},a}
+\sum_kJ_{a,k}\Sigma_{a,k}J_{a,k}^{T}
+C_{\mathrm{modelo},a},
\]

\[
C_{\mathrm{eff}}^{(D,E)}=
\begin{pmatrix}
C_{\mathrm{eff},D}&C_{DE}\\
C_{ED}&C_{\mathrm{eff},E}
\end{pmatrix},
\qquad C_{ED}=C_{DE}^{T}.
\]

Inclui ruído de medida, variância amostral, calibração, PSF, seleção, redshift e marginalização de nuisances. Covariâncias entre nuisances dentro de cada réplica entram uma única vez em \(\Sigma_{a,k}\); \(C_{DE}\) entra somente nos blocos fora da diagonal, nunca novamente dentro de \(C_{\mathrm{eff},a}\). Não somar novamente um sistemático já incluído em simulações end-to-end.

### Duas independências

1. **Dados efetivamente independentes:** instrumentos, fótons, ruído e amostras independentes. Objetos compartilhados exigem \(C_{DE}\neq0\) ou subamostras de objetos disjuntas; calibração ou zero-points compartilhados continuam exigindo covariância cruzada mesmo com objetos disjuntos.
2. **Replicação analítica independente:** reduções cegadas e independentes, com previsões e código de decisão congelados. Testa robustez, mas não multiplica significância quando os dados são os mesmos.

Não se somam \(z\)'s de \(g^{(1)}\), visibilidade, perfil, photo-z e spec-z dos mesmos objetos.

---

## 8. Vereditos fail-closed

| situação | veredito |
|---|---|
| Falta previsão numérica, observável fase-sensível, covariância ou duas independências | `NOT_TESTABLE` |
| Nulo falha, controle de intensidade explica o efeito ou réplicas divergem sem solução | `INCONCLUSIVE_SYSTEMATICS` |
| Efeito não nulo, mas TGL e rival continuam compatíveis | `GENERIC_DEPHASING_NOT_DISCRIMINANT` |
| TGL compatível, porém \(|z_{N|d}|<5\) ou \(S_{TN}<5\) | `TGL_COMPATIBLE_RIVAL_NOT_EXCLUDED` |
| Previsão TGL afastada do centro no limiar congelado, com nulo e controles válidos | `TGL_VARIANT_EXCLUDED` |
| TGL e nulo ambos excluídos | `INCONCLUSIVE_SYSTEMATICS` |
| Em ambas as réplicas: controles válidos, TGL não excluída, rival excluído a pelo menos 5σ, com limiares e trials pré-registrados | `TGL_RIVAL_DISCRIMINATION_REPLICATED` |

O último veredito vale somente para a comparação fechada entre os modelos testados; não é creditação universal da teoria.

**Distinção obrigatória:** rejeitar “alguma defasagem” é diferente de discriminar a TGL. A segunda exige sinal, magnitude, escala e perfil previstos antes da abertura, com replicação independente.

---

## 9. Dados: candidatos futuros, ainda não abertos

- **DESI-COSMOS × COSMOS2020:** possível emparelhamento fotométrico/espectroscópio, mas photo-z × spec-z, sozinho, não testa coerência.
- **Euclid Q1 PHZ × spec-z:** possível réplica fotométrica, desde que os produtos permitam construir um observável fase-sensível com covariância espacial e de zero-points.
- **DES-Dovekie:** útil para distâncias somente depois de derivar \(\mu_{\rm TGL}(z)\), não para testar coerência por mera associação com photo-z.
- **Interferometria laboratorial:** candidata preferencial para validar primeiro a ponte entre defasagem e \(g^{(1)}\), com intensidade de controle e sistema totalmente especificado.

Nenhum desses conjuntos deve ser aberto antes de uma previsão numérica congelada e da prova de que seus produtos realmente medem fase/coerência.

---

## 10. Folha de derivação antes da decisão do operador

- [ ] **Objeto de \(D\):** \(\rho_{ij}\), coerência entre modos ou \(g_1\) de uma linha: __________
- [ ] **Modos e base:** __________
- [ ] **Lei de caminho \(T(z)\) ou justificativa para \(N(z)=\ln(1+z)\):** __________
- [ ] **Mapa sem ajuste \(\Gamma_{ij}(z)\) e/ou \(\gamma(z)\):** __________
- [ ] **Regra emissão × propagação:** __________
- [ ] **Nulo rival operacional:** __________
- [ ] **Previsão numérica \(\mu_T\):** __________
- [ ] **Centro do nulo \(\mu_N\):** __________
- [ ] **Contraste e limiares:** __________
- [ ] **Duas independências e covariância \(C_{DE}\):** __________
- [ ] **E3, somente depois de tudo congelado e do runner hasheado:** __________

---

**Resultado [DECLARADO pelo Kimi]:** a rota de coerência com intensidade preservada é fisicamente coerente e matematicamente bem definida. A TGL fornece a defasagem e a preservação da diagonal; a difusão estacionária de fase fornece o perfil Lorentziano normalizado. O elo astrofísico entre esses objetos ainda não foi derivado. Portanto, não há previsão sem ajuste, σ de 5σ ou teste pronto. A próxima derivação necessária é o mapa \(K,\beta,\text{modos},\text{trajeto}\mapsto D(z,\tau)\), antes de qualquer dado.
