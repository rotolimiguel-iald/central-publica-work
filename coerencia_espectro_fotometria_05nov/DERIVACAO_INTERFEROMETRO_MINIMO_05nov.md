# DERIVAÇÃO — interferômetro mínimo com intensidade e fase no mesmo sistema

**Data:** 05/11/2026  
**Estatuto:** **[DECLARADO pelo Kimi]**, até identificação física do canal e conferência da gerência.  
**Estado:** `OPEN_K_BASIS_AND_CHANNEL_DERIVATION` · `NO_DATA_OPENED` · `NO_VERDICT`.  
**Objeto:** Mach–Zehnder de um fóton com defasagem de caminho, recombinação balanceada e intensidade total preservada.

---

## 1. Estado de entrada e o canal

Defina os dois caminhos como estados de um fóton:

\[
|A\rangle:=|1_A,0_B\rangle,\qquad
|B\rangle:=|0_A,1_B\rangle .
\]

A entrada é

\[
|\psi\rangle=a|A\rangle+b|B\rangle,
\qquad N:=|a|^2+|b|^2>0 .
\]

Na base \(\{|A\rangle,|B\rangle\}\),

\[
\rho(0)=|\psi\rangle\langle\psi|=
\begin{pmatrix}
|a|^2 & ab^*\\
a^*b & |b|^2
\end{pmatrix}.
\]

A defasagem atua **somente fora da diagonal**:

\[
\rho_{AB}(T)=e^{-\Gamma T}\rho_{AB}(0),\qquad
\rho_{BA}(T)=e^{-\Gamma T}\rho_{BA}(0),
\]

com

\[
\rho_{AA}(T)=|a|^2,\qquad
\rho_{BB}(T)=|b|^2 .
\]

Portanto,

\[
\rho(T)=
\begin{pmatrix}
|a|^2 & e^{-\Gamma T}ab^*\\
e^{-\Gamma T}a^*b & |b|^2
\end{pmatrix}.
\]

A taxa candidata, na forma de salto hermitiano usada em R–E, é

\[
\Gamma\equiv\Gamma_{AB}
=\frac{\beta}{2}\left(\sqrt{k_A}-\sqrt{k_B}\right)^2 .
\]

Ela pertence à coerência entre os caminhos, não à perda de população. [DERIVACAO_RE_02nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Crota_RE_dualidade_02nov%5CDERIVACAO_RE_02nov.md&line=18&text=com%20%CE%93_ij%20%3D%20%C2%BD%CE%B2(%E2%88%9Ak_i%20%E2%88%92%20%E2%88%9Ak_j)%C2%B2. "citation")

A forma preserva o traço, coerentemente com `dephase_preserves_trace`. [TheTraceIsNotErasable](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CTheTraceIsNotErasable.lean&text=%28dephase%20g%20t%20x%29.trace%20%3D%20x.trace "citation")

---

## 2. Recombinação e intensidades

Use os projetores de detecção

\[
|\pm_\phi\rangle=\frac{|A\rangle\pm e^{i\phi}|B\rangle}{\sqrt2},
\qquad
I_\pm=\langle\pm_\phi|\rho(T)|\pm_\phi\rangle .
\]

A aplicação direta da matriz fornece

\[
\boxed{
I_\pm(\phi,T)=\frac{|a|^2+|b|^2}{2}
\pm e^{-\Gamma T}|ab|\cos\!\big(\arg(ab^*)+\phi\big).
}
\]

Se \(\phi\) já for a fase relativa total na recombinação, basta usar \(\phi\) no cosseno. A fase inicial e a fase do recombinador entram somadas nesta convenção.

A intensidade total é

\[
\boxed{
I_++I_-=|a|^2+|b|^2=N,
}
\]

independente de \(\Gamma\), \(T\) e \(\phi\). O canal reduz as franjas, não o fóton nem a intensidade total do par de detectores.

---

## 3. Visibilidade derivada

Ao varrer a fase, os extremos de qualquer saída são

\[
I_{\max}=\frac N2+e^{-\Gamma T}|ab|,
\qquad
I_{\min}=\frac N2-e^{-\Gamma T}|ab|.
\]

Logo,

\[
\boxed{
V(T)=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}
=\frac{2|ab|}{|a|^2+|b|^2}e^{-\Gamma T}
=V_0e^{-\Gamma T},
\qquad
V_0=\frac{2|ab|}{|a|^2+|b|^2}.
}
\]

Como \(2|ab|\le |a|^2+|b|^2\), \(V_0\le1\), com igualdade quando \(|a|=|b|\).

Numa fase fixa,

\[
\frac{I_+-I_-}{I_++I_-}
=V_0e^{-\Gamma T}\cos\!\big(\arg(ab^*)+\phi\big).
\]

A fase desloca as franjas; a defasagem reduz seu envelope. Não são o mesmo efeito.

### Caso balanceado

Para \(a=b=1/\sqrt2\), temos \(N=1\), \(|ab|=1/2\) e \(V_0=1\):

\[
\boxed{
I_\pm=\frac12\left(1\pm e^{-\Gamma T}\cos\phi\right),
\qquad I_++I_-=1,
\qquad V(T)=e^{-\Gamma T}.
}
\]

Se \(\Gamma>0\) e \(T\to\infty\), então \(I_\pm\to1/2\) e \(V\to0\): desaparece a interferência, não o fóton.

**Verificação:** as fórmulas foram testadas em cinco configurações, incluindo fases complexas e amplitudes desiguais. Todos os testes passaram. [VERIFICACAO_INTERFEROMETRO](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/VERIFICACAO_INTERFEROMETRO.json), gerado por [verificar_interferometro](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/verificar_interferometro.py).

---

## 4. O que é teorema do modelo e o que continua leitura

### [REAL — consequências do canal definido]

- atenuação dos elementos \(\rho_{AB}\) e \(\rho_{BA}\) por \(e^{-\Gamma T}\);
- invariância das diagonais e do traço;
- fórmulas de \(I_\pm\), da soma e de \(V(T)=V_0e^{-\Gamma T}\);
- ausência de perda na intensidade total;
- condição \(k_A\neq k_B\) para \(\Gamma\neq0\).

### [INPUT/ONTO — identificações ainda não derivadas]

- que os caminhos \(|A\rangle,|B\rangle\) sejam autostados de \(K\), com autovalores \(k_A,k_B\);
- que o salto \(L=\sqrt\beta\sqrt K\) represente um canal físico efetivo sobre o fóton, com intensidade β e duração \(T\);
- que \(T=L/c\) seja o tempo de atuação desse canal;
- a hipótese H1: a luz sofre o vazamento na base de \(K\), e \(K\) comuta com o momento do fóton. [DERIVACAO_RE_02nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Crota_RE_dualidade_02nov%5CDERIVACAO_RE_02nov.md&line=20&text=a%20luz%20sofre%20esse%20vazamento%20na%20base%20de%20K%2C%20e%20K%20comuta%20com%20o%20momento%20do%20f%C3%B3ton. "citation")

Se a base de \(K\) não coincidir com a base dos caminhos, é necessário transformar o superoperador; a prescrição simples usada aqui deixa de estar justificada.

Para \(\beta>0\) e \(T>0\),

\[
\Gamma_{AB}>0
\quad\Longleftrightarrow\quad
k_A\neq k_B .
\]

Se \(k_A=k_B\), o ambiente não distingue os caminhos e a coerência relativa não é atenuada por esse canal.

---

## 5. Tempo de atuação: laboratório e cosmologia

### Laboratório

Se o canal atua continuamente ao longo de um comprimento \(L\), com taxa constante,

\[
T=\frac{L}{c},
\qquad
\Gamma T=\frac{\beta L}{2c}
\left(\sqrt{k_A}-\sqrt{k_B}\right)^2 .
\]

Portanto,

\[
\boxed{
V(L)=V_0\exp\!\left[
-\frac{\beta L}{2c}
\left(\sqrt{k_A}-\sqrt{k_B}\right)^2
\right].
}
\]

O \(L\) correto é o comprimento sobre o qual o **canal físico realmente atua**, não automaticamente o comprimento geométrico total do interferômetro. Se a taxa variar ao longo do trajeto,

\[
V=V_0\exp\!\left[-\int_0^T\Gamma(t)\,dt\right].
\]

Em um meio, usa-se o atraso de grupo apropriado, não simplesmente o comprimento dividido pela velocidade de fase.

### Cosmologia

Se o canal atua continuamente durante a propagação, o tempo cosmológico usual é o **lookback time**:

\[
\boxed{
T(z)=\int_0^z\frac{dz'}{(1+z')H(z')},
\qquad
\frac{dT}{dz}=\frac{1}{(1+z)H(z)}>0 .
}
\]

Ele vem de \(a=1/(1+z)\) e \(dt=dz/[(1+z)H(z)]\), em módulo, integrado ao longo do trajeto. \(H\) deve ser convertido para \(\mathrm{s}^{-1}\) antes do cálculo.

Não se insere outro fator \(1+z\) nesse integrando. A prescrição alternativa \(\int(1+z')/H(z')dz'\) **não é o lookback time** e não deve ser usada sem uma nova derivação física explícita.

### Detector versus fonte

Para um intervalo emitido por uma fonte em redshift \(z\),

\[
d\tau_{\rm det}=(1+z)d\tau_{\rm src}.
\]

Para a função de coerência,

\[
\boxed{
g^{(1)}_{\rm det}(\tau_{\rm det})
=g^{(1)}_{\rm src}\!\left(\frac{\tau_{\rm det}}{1+z}\right).
}
\]

Se a fonte tem difusão de fase com taxa \(\gamma\), a largura Lorentziana na frequência ordinária transforma como

\[
\Delta\nu_{\rm det}=\frac{\Delta\nu_{\rm src}}{1+z},
\qquad
\gamma_{\rm det}=\frac{\gamma_{\rm src}}{1+z}.
\]

**A dilatação temporal, sozinha, não reduz a visibilidade**: em atrasos equivalentes, \(|g^{(1)}|\) é o mesmo. Ela também não identifica \(\gamma\) à taxa de propagação \(\Gamma\).

---

## 6. O que este modelo não demonstra

1. **Não produz alargamento espectral automaticamente.** O canal atua sobre coerência de caminho; nenhuma dinâmica sobre frequências foi introduzida. Só haveria perfil espectral se fosse demonstrada adicionalmente a identificação entre essa coerência e \(g^{(1)}\) de um campo estacionário.
2. **Não corrige fotometria.** A soma das saídas é constante; não há fator de atenuação de fluxo.
3. **Não produz desvio photo-z–spec-z.** Posições de linhas e populações de momento permanecem invariantes sob H1.
4. **Não prova \(\eta=1\) nem \(\eta\neq1\).** A ligação cosmológica depende de uma ponte física adicional, não apenas da recombinação.
5. **Não identifica \(\Gamma=\gamma\).** Essa igualdade exige que a visibilidade seja medida em função do mesmo atraso da coerência, com envelope exponencial e sem outra atenuação escondida em \(V_0\).

Se \(\gamma\) for taxa de decaimento de intensidade/população, a coerência pode decair com \(\gamma/2\), não com \(\gamma\); se \(\gamma\) for apenas o FWHM em Hz, então \(\Gamma=\pi\gamma\) sob a convenção de difusão de fase. As convenções não podem ser misturadas.

---

## 7. A previsão condicional e o requisito de 5σ

Defina \(x=\Gamma T\). O nulo de ausência do decaimento extra e a previsão TGL são

\[
V_N=V_0,
\qquad
V_T=V_0e^{-x}.
\]

A separação prevista é

\[
\boxed{
\Delta_V=V_N-V_T=V_0(1-e^{-x})
\simeq V_0x\quad (x\ll1).
}
\]

Para uma única medida com modelos e \(V_0\) conhecidos, a separação de 5σ exige

\[
\boxed{
\sigma_{\Delta V}\leq
\frac{V_0}{5}(1-e^{-x}).
}
\]

Para duas medidas independentes, \(\sigma_{\Delta V}=\sqrt{\sigma_{V,T}^2+\sigma_{V,N}^2}\).

### Convenção logarítmica que evita a dependência em \(V_0\)

Defina

\[
q=-\ln(V/V_0).
\]

Então

\[
q_T=x,
\qquad q_N=0,
\qquad
\boxed{\sigma_q\leq\frac{x}{5}.}
\]

Essa forma pressupõe que \(V_0\) tenha sido corretamente calibrado; não elimina a covariância de calibração.

### Compatibilidade de cada modelo com o dado

\[
z_{T|d}=\frac{V_T-\widehat V}{\sigma_{\mathrm{eff}}},
\qquad
z_{N|d}=\frac{V_N-\widehat V}{\sigma_{\mathrm{eff}}}.
\]

Para discriminar TGL do nulo em duas réplicas independentes:

- o nulo deve ser excluído a pelo menos 5σ em cada réplica;
- a previsão TGL deve permanecer compatível;
- covariância, trials e independência devem ter sido congelados antes da abertura.

Se o resultado for \(q\simeq0\), o limite unilateral de 5σ em \(q\) fornece

\[
\boxed{
\Gamma<\frac{5\sigma_q}{T(z)}.
}
\]

Isso é um limite experimental sobre \(\Gamma\), não sua derivação teórica nem uma detecção do nulo.

**Se \(x=\Gamma T\) for conhecido exatamente**, a previsão \(V/V_0=e^{-x}\) é falsificável e as incertezas acima são requisitos de poder, não ajustes. **Se \(\Gamma\) não foi derivado**, existe apenas um modelo fenomenológico com parâmetro livre; ajustá-lo não produz previsão absoluta nem redshift de descoberta.

---

## 8. Derivações ainda obrigatórias antes de E3

- [ ] **Base de \(K\):** demonstrar que os caminhos são autostados e obter \(k_A,k_B\), sem escolhê-los pelo alvo: __________
- [ ] **Canal físico:** demonstrar o salto e o setor de atuação: __________
- [ ] **Tempo de atuação:** \(L/c\), atraso de grupo ou \(T(z)\), com unidades: __________
- [ ] **Previsão exata \(x=\Gamma T\):** __________
- [ ] **Relação entre visibilidade e \(g^{(1)}\), se usada:** __________
- [ ] **Nulo operacional e calibração de \(V_0\):** __________
- [ ] **Duas independências e covariância completa:** __________
- [ ] **Runner hasheado e palavra E3 do operador:** __________

**Classe atual:** `OPEN_K_BASIS_AND_CHANNEL_DERIVATION`. Não há previsão numérica sem ajuste, σ de 5σ ou teste pronto.

---

**Resultado [DECLARADO pelo Kimi]:** no modelo mínimo de Mach–Zehnder, a defasagem produz exatamente \(V(T)=V_0e^{-\Gamma T}\), com intensidade total preservada. A fórmula é uma ponte concreta entre coerência e visibilidade, mas sua identificação com um canal TGL físico permanece [INPUT/ONTO]. A próxima derivação necessária é obter \(k_A,k_B\) e o canal, sem escolhê-los pelo resultado desejado.
