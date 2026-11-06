# Candidatos naturais a \(k_A,k_B\) — coerência interferométrica e dicionário de Turing

**Data:** 05/11/2026  
**Estatuto:** **[DECLARADO pelo Kimi]**, até conferência da gerência.  
**Estado atualizado:** `LOCK_AND_MODULAR_K_NO_GO_FOR_ONE_PHOTON_PATH_MODEL` · `OPEN_NEW_PHYSICAL_CHANNEL` · `NO_DATA_OPENED` · `NO_VERDICT`.  
**Escopo:** procurar valores determinados por teoria, sem ajuste, para o canal de defasagem com intensidade preservada. Nenhum dado foi aberto e nenhum teste com a natureza foi executado.

---

## 1. Resultado executivo

Há um único par algébrico não trivial diretamente oferecido pelo lock mínimo:

\[
k_A=0,\qquad k_B=1
\quad\Longrightarrow\quad
\Gamma_{AB}=\frac{\beta}{2}(\sqrt{k_A}-\sqrt{k_B})^2
=\frac{\beta}{2}.
\]

O lock é

\[
\operatorname{lockDe}(\Omega)=1-P_\Omega,
\]

e o kernel prova que ele vale 0 em \(\Omega\) e 1 em todo vetor ortogonal a \(\Omega\). [PontoZeroDoPsion](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPontoZeroDoPsion.lean&text=theorem%20o_lock_tem_gap_um%20(%CE%A9%20%CF%87%20%3A%20F)%20(hort%20%3A%20%E2%9F%AA%CE%A9%2C%20%CF%87%E2%9F%AB_%E2%84%82%20%3D%200)%20%3A%20lockDe%20%CE%A9%20%CE%A9%20%3D%200%20%E2%88%A7%20lockDe%20%CE%A9%20%CF%87%20%3D%20%CF%87 "citation")

**Mas o lock do vácuo não fornece esse par aos dois caminhos de um fóton.** No interferômetro mínimo,

\[
|A\rangle=|1_A,0_B\rangle,\qquad |B\rangle=|0_A,1_B\rangle
\]

são estados do setor de uma partícula, ambos ortogonais ao vácuo \(\Omega\). Portanto, se \(K=1-P_\Omega\) é o lock do vácuo no espaço de Fock,

\[
K|A\rangle=|A\rangle,\qquad K|B\rangle=|B\rangle,
\qquad k_A=k_B=1,
\qquad \boxed{\Gamma_{AB}=0}.
\]

Esse é um resultado algébrico sob a identificação declarada, não uma falsificação da TGL nem de outros possíveis canais \(K\).

O par \(0/1\) só é recuperado por um lock cuja referência esteja alinhada a **um dos caminhos**, por exemplo \(\Omega\propto|A\rangle\). Isso é outro operador, com uma escolha física privilegiada de caminho; não se pode presumir essa identificação para obter o efeito desejado.

Assim:

- \(V(T)=V_0e^{-\beta T/2}\) é uma **previsão condicional** do modelo com lock alinhado a um caminho, na convenção de unidades em que \(\beta T\) é adimensional;
- o lock do vácuo prevê, para os dois caminhos de um fóton, **nenhum decaimento extra por esse mecanismo**;
- as pedras candidatas R1–R8 da tradução de Turing não determinam autovalores ópticos \(k_A,k_B\);
- ainda não há previsão TGL sem ajuste, classe A/B ou teste pronto.

---

## 2. O que a tradução de Turing R1–R8 acrescenta

As pedras R1–R8 são candidatas à v409, compiladas no sandbox da v408; o cabeçalho cumulativo de R8 não as apresenta como uma versão selada nova nem como teste com a natureza. [TraducaoTuringR8](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cpedras_candidatas_05nov%5CTraducaoTuringR8.lean&text=NOME%20PROVIS%C3%93RIO%20(o%20nome%20%C3%A9%20do%20operador)%3B%20compilada%20no%20sandbox%20da%20v408 "citation")

| Rodada | Conteúdo demonstrado | O que não entrega ao interferômetro |
|---|---|---|
| **R1 — codificação e parede** | Uma instância vira operador diagonal do custo \(c:X\to\mathbb N\); núcleo não nulo iff resposta SIM; leitura verifica o certificado; grau polinomial na entrada; bits como oitavas; peso uniforme da solução \(|sol|/|X|\); fluxo não amplia esse peso; seleção custa \(\log(2^n/s)\le n\ln2\). | \(c(x)\) é custo computacional, não autovalor óptico; o fluxo não é um canal de defasagem do fóton. |
| **R2 — modo seleção** | Seleção como projeção renormalizada no Nome; decaimento renormalizado converge à seleção; custo linear nas oitavas em nats; \(t=n\ln2/(\beta g)\) linear nos bits. | O enunciado de máquina de Turing permanece fora; nenhum par de caminhos ópticos é selecionado como setor 0/1. |
| **R3 — trava no Nome** | A trava é gerada pelo custo, fatora cláusula a cláusula e converge à seleção, com perda linear nas oitavas. | A trava atenua amplitudes computacionais e renormaliza; não é derivada como salto GKLS sobre coerência óptica. |
| **R4 — fita e partição** | A fita é lida como Hamiltoniano oculto; \(Z(s)=\sum_xe^{-sc(x)}\); a regra gera a trava e \(Z\) conta soluções no limite. | Calcular \(Z\) não é gratuito: é #P-completo em geral, e decidir seu limite \(\ge1\) contém SAT; nenhum \(k_A,k_B\) óptico resulta. |
| **R5 — \(Z\) como modo leitor** | \(Z\) soma pixels; no uniforme a leitura é \(Z/|X|\); o canto escalariza na mesma forma do psíon. | A própria pedra diz «mesma forma, não ponte»: o \(\Omega\) uniforme computacional não é identificado ao psíon de Fock. |
| **R6 — fita sem escala** | Sem escala não há medida; o tempo cria a medida e separa solução de não-solução. | Não fixa uma escala óptica nem uma base de propagação. |
| **R7 — pai da mentira** | Sem escala, mentira e verdade leem igual; só o tempo as separa. | Não fornece dois setores físicos do interferômetro. |
| **R8 — identidade performada** | A leitura começa em «eu sou», não cresce ao decair, não desce abaixo do conteúdo e converge a «o que sou». | A monotonicidade da leitura não determina taxa nem autovalores de um canal óptico. |

A síntese R1–R8 e a separação explícita entre codificação, seleção, trava, partição e leitura estão no cabeçalho cumulativo da pedra. [TraducaoTuringR8](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cpedras_candidatas_05nov%5CTraducaoTuringR8.lean&text=Mesma%20forma%2C%20n%C3%A3o%20ponte%3A%20o%20%CE%A9%20do%20%60PsionCanto%60%20%C3%A9%20o%20ps%C3%ADon%20da%20luz%20na%20face%20de%20Fock%3B%20aqui%20%CE%A9%20%C3%A9%20o%20uniforme%20sobre%20as%20atribui%C3%A7%C3%B5es. "citation")

**Consequência:** a v409 candidata fornece objetos algébricos novos, mas nenhuma ponte nova entre esses objetos e os dois caminhos do Mach–Zehnder.

---

## 3. Classificação geral do lock no espaço de dois caminhos — corrigida por \(r\)

**Correção ao lado, 05/11/2026:** a versão anterior desta seção tratou \(Q\Omega\propto A\) como suficiente para o par exato \(0/1\). Isso só vale se \(\Omega\) estiver inteiramente no espaço dos caminhos. A classificação completa usa \(r=\|Q\Omega\|\) e está demonstrada em [DERIVACAO_OMEGA_K_LOCK_NO_GO_05nov](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/DERIVACAO_OMEGA_K_LOCK_NO_GO_05nov.md).

Seja

\[
S=\operatorname{span}\{|A\rangle,|B\rangle\},\qquad
\langle A|B\rangle=0,
\]

e seja \(Q\) o projetor sobre \(S\). Para \(\|\Omega\|=1\), escreva

\[
Q\Omega=\alpha A+\tau B,
\qquad
r^2=|\alpha|^2+|\tau|^2,
\qquad 0\le r\le1.
\]

Então

\[
QK_\Omega Q=
\begin{pmatrix}
1-|\alpha|^2&-\alpha\tau^*\\
-\alpha^*\tau&1-|\tau|^2
\end{pmatrix}.
\]

Na base paralela e ortogonal a \(Q\Omega\), os autovalores são

\[
\boxed{k_e=1-r^2,\qquad k_o=1},
\]

e a taxa entre esses modos é

\[
\boxed{
\Gamma_{\rm lock}(r)=\frac\beta2(1-\sqrt{1-r^2})^2.
}
\]

Para que a base dos caminhos seja também a base de autostados do lock, é necessário e suficiente que \(\alpha\tau^*=0\). Restam somente:

| Caso | \(k_A,k_B\) | Taxa |
|---|---:|---|
| \(r=0\), incluindo o lock do vácuo | \(1,1\) | 0 |
| \(\tau=0,\ 0<r=|\alpha|\le1\) | \(1-r^2,1\) | \(\Gamma_{\rm lock}(r)\) |
| \(\alpha=0,\ 0<r=|\tau|\le1\) | \(1,1-r^2\) | \(\Gamma_{\rm lock}(r)\) |

O par exato \(0/1\) e \(\Gamma=\beta/2\) exigem **alinhamento e \(r=1\)**, isto é, \(\Omega=e^{i\varphi}A\) ou \(\Omega=e^{i\varphi}B\). Se \(0<r<1\), o lock pode ser diagonal nos caminhos, mas a taxa é menor; para \(r\ll1\), \(\Gamma_{\rm lock}=\beta r^4/8+O(r^6)\).

Se \(\alpha\tau^*\ne0\), os caminhos não são autostados do lock. A coerência \(\rho_{AB}\) não segue em geral uma única exponencial e as populações podem mudar. O lock do próprio estado não evolui; o lock simétrico não preserva universalmente as populações dos caminhos.

---

## 4. Tabela de candidatos e objetos que não podem ser reutilizados

| Objeto candidato | Valores que realmente fornece | Pode determinar \(\Gamma\) agora? | Estatuto |
|---|---|---|---|
| **Lock abstrato \(1-P_\Omega\)** | Autovalores 0 e 1; \(0/1\) exige \(A\) e \(B\) nos dois setores. | Só condicionalmente: \(\Gamma=\beta/2\). | **[REAL] álgebra; [INPUT/ONTO] identificação óptica.** |
| **Lock do vácuo de Fock** | Nos dois estados de um fóton dos caminhos: \(k_A=k_B=1\). | Sim, mas o resultado é \(\Gamma=0\), não um sinal. | **[REAL] consequência da identificação declarada; não exclui outro \(K\).** |
| **Lock referido a um caminho** | \(0/1\) ou \(1/0\). | \(\Gamma=\beta/2\), mas falta derivar a referência e o canal. | **[INPUT/ONTO]**; não pode ser escolhido pelo efeito. |
| **Projetor de um caminho ou ocupação de um braço** | \(P_A\) ou \(n_A\) distingue \((1,0)\) de \((0,1)\), dando \(1/0\). | Produz formalmente \(\beta/2\), mas é um modelo fenomenológico de «qual caminho», não uma derivação TGL. | **[DECLARADO]** como modelo possível; portador físico e ligação a \(K\) abertos. |
| **Custo de instância \(c(x)\)** | Inteiros \(0,1,2,\ldots\); em SAT, 0 identifica solução e valores positivos contam cláusulas violadas. | Não. Nem todo caso é binário e não há embedding óptico derivado. | **[REAL] computacional; [ONTO] se lido como óptica.** |
| **Seleção/trava de R2–R3** | Projeção, pesos e decaimentos parametrizados por \(c(x)\). | Não. Não são autovalores de um \(K\) óptico nem um canal fotônico derivado. | **[REAL] no modelo computacional; ponte aberta.** |
| **Partição \(Z\) e peso \(Z/|X|\)** | Peso de leitura, não gap nem autovalor de caminho. | Não. | **Homônimos recusados.** |
| **`ClasseP` / `ClasseNP`** | Classes de problemas/leituras. | Não são setores \(k\). | **Uso como autovalor seria inválido.** |
| **Ângulo de Miguel** | No estado angular, \(\langle\operatorname{lock}\rangle=\sin^2\theta\); no ângulo de Miguel, \(\langle\operatorname{lock}\rangle=\beta\). | Não se pode pôr \(k=\beta\) como se fosse autovalor. | **[REAL] valor esperado, não gap.** [PontoZeroDoPsion](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPontoZeroDoPsion.lean&text=NO%20%C3%82NGULO%20DE%20MIGUEL%20O%20LOCK%20L%C3%8A%20%CE%B2%3A%20o%20valor%20esperado%2C%20n%C3%A3o%20o%20gap. "citation") |

---

## 5. Correção de estado: o certificado físico existe, a ponte óptica não

O comentário antigo de `PontoZeroDoPsion` diz que a identificação de `HminMic` com o lock é condicional a um `FockCertificate` não habitado. Esse comentário convive no arquivo com o estado mais recente da cadeia: a v408 contém o `physicalFockCertificate` da v406, e `PontoDeContradicao` prova que seu espaço é o Fock concreto e seu \(\Omega\) é o vácuo, sem hipótese. [PontoDeContradicao](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPontoDeContradicao.lean&text=theorem%20o_habitante_e_o_fock_concreto%20%3A%0A%20%20%20%20physicalFockCertificate.F%20%3D%20F1Rede.BosonicFock.F%20%E2%88%A7%20physicalFockCertificate.%CE%A9%20%3D%20vacuum "citation")

A face física do psíon no habitante também é declarada como incondicional na v406. [PsionCanto](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPsionCanto.lean&text=tudo%20isto%20no%20%60physicalFockCertificate%60%20(F1Fecho394%2C%20v406)%2C%20SEM%20hip%C3%B3tese. "citation")

**Correção operacional:** a lacuna desta rota não deve mais ser formulada como «o kernel não habita nenhum certificado de Fock». A lacuna atual é demonstrar que o \(K\) da defasagem óptica é esse lock — ou outro operador especificado — e obter seus autovalores nos estados dos caminhos.

Além disso, `PontoDeContradicao` separa explicitamente o lock \(1-P_\Omega\) do Hamiltoniano modular \(K=-\log\Delta\): eles coincidem em ter \(\Omega\) como modo zero, mas não são provados ser o mesmo operador; a identificação foi podada. [PontoDeContradicao](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPontoDeContradicao.lean&text=o%20lock%20%601%20%E2%88%92%20P%60%20e%20o%20Hamiltoniano%20modular%20%60K%20%3D%20%E2%88%92log%20%CE%94%60%20(o%20gerador%20de%20%60lightOp%60)%20s%C3%A3o%20OBJETOS%20DISTINTOS%20que%20coincidem%20em%20ter%20%CE%A9%20como%20modo%20zero. "citation")

Portanto, nem `HminMic`, nem o lock, nem o Hamiltoniano modular podem ser intercambiados apenas pelo nome \(K\).

---

## 6. A fórmula condicional e suas unidades

A prescrição herdada da rota R–E é

\[
L=\sqrt\beta\,\sqrt K,
\qquad
\Gamma_{ij}=\frac{\beta}{2}(\sqrt{k_i}-\sqrt{k_j})^2.
\]

Ela pertence a uma família de defasagem; a hipótese de aplicação à luz é nomeada, não um portador físico derivado. [DERIVACAO_RE_02nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Crota_RE_dualidade_02nov%5CDERIVACAO_RE_02nov.md&line=18&text=A%20fam%C3%ADlia%20do%20vazamento%20%C3%A9%20defasagem. "citation")

Se, **por hipótese física ainda a derivar**, os caminhos realizam \(k_A=0,k_B=1\) e o mesmo salto atua durante \(T\), então

\[
\boxed{\Gamma_{AB}=\frac{\beta}{2}},
\qquad
\boxed{V(T)=V_0e^{-\beta T/2}},
\qquad
q:=-\ln(V/V_0)=\frac{\beta T}{2}.
\]

### Condição dimensional obrigatória

O expoente deve ser adimensional. Se \(k_A,k_B\) são adimensionais e \(\beta\) é o acoplamento adimensional canônico, \(\beta/2\) **não é automaticamente uma taxa em \(\mathrm{s}^{-1}\)**. É necessário pelo menos um dos seguintes itens, derivado e não escolhido por conveniência:

1. declarar que \(T\) é o parâmetro adimensional do canal, não segundos;
2. fornecer a escala que converte esse parâmetro em tempo físico;
3. derivar uma taxa física adicional. A tradução R2 usa a combinação \(\beta g\) em \(t=n\ln2/(\beta g)\), mas isso não autoriza importar \(g\) ao interferômetro sem demonstrar que é o mesmo gerador e a mesma taxa.

Por isso, \(\Gamma=\beta/2\) deve ser lida inicialmente **na convenção adimensional da prescrição**. Uma taxa de laboratório exigiria fechar essa calibração. Em particular, \(V(L)=V_0e^{-\beta L/(2c)}\) só é dimensionalmente válida se a convenção usada atribuir a \(\beta/c\) a unidade correta; não se deve apresentar essa expressão como previsão física antes dessa etapa.

---

## 7. Requisito estatístico condicional de 5σ

Esta seção calcula apenas o **poder necessário caso o canal e suas unidades sejam fechados**. Não escolhe instrumento, dados ou redshift.

Para \(x=\Gamma T\), com modelos e visibilidade instrumental \(V_0\) conhecidos,

\[
V_N=V_0,
\qquad
V_T=V_0e^{-x},
\qquad
\Delta_V=V_0(1-e^{-x}).
\]

Uma separação de 5σ entre as duas previsões requer

\[
\boxed{\sigma_{\Delta V}\le\frac{V_0}{5}(1-e^{-x})}.
\]

Na variável logarítmica \(q=-\ln(V/V_0)\),

\[
q_N=0,\qquad q_T=x,
\qquad
\boxed{\sigma_q\le\frac{x}{5}}.
\]

Para o candidato condicional \(x=\beta T/2\),

\[
\boxed{\sigma_q\le\frac{\beta T}{10}},
\qquad
\boxed{\sigma_{\Delta V}\le\frac{V_0}{5}(1-e^{-\beta T/2})},
\]

e, para \(x\ll1\),

\[
\sigma_{\Delta V}\lesssim\frac{V_0\beta T}{10}.
\]

Essas desigualdades não eliminam covariância de calibração nem sistemáticas de \(V_0\). Uma discriminação operacional continuaria a exigir nulo excluído a pelo menos 5σ em duas réplicas independentes, previsão TGL compatível e covariância/trials congelados antes da abertura.

No caso do **lock do vácuo**, \(x=0\) para os caminhos de um fóton, logo \(\Delta_V=0\): esse ramo não oferece separação entre TGL e nulo por visibilidade, qualquer que seja a precisão idealizada.

As fórmulas gerais do interferômetro e a condição de 5σ já foram verificadas no modelo mínimo; isso não verifica sua identificação física com \(K\). [DERIVACAO_INTERFEROMETRO_MINIMO_05nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccoerencia_espectro_fotometria_05nov%5CDERIVACAO_INTERFEROMETRO_MINIMO_05nov.md&line=120&text=V(T)%3D%5Cfrac%7BI_%7B%5Cmax%7D-I_%7B%5Cmin%7D%7D%7BI_%7B%5Cmax%7D%2BI_%7B%5Cmin%7D%7D "citation")

---

## 8. Cosmologia e espectro: duas pontes que continuam separadas

Se o canal vier a atuar continuamente na propagação cosmológica, o tempo é o lookback time

\[
T(z)=\int_0^z\frac{dz'}{(1+z')H(z')},
\]

não uma integral com numerador \(1+z'\). A dilatação detector–fonte obedece

\[
d\tau_{\rm det}=(1+z)d\tau_{\rm src},
\]

e, sozinha, não reduz a visibilidade em atrasos equivalentes. [DERIVACAO_INTERFEROMETRO_MINIMO_05nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccoerencia_espectro_fotometria_05nov%5CDERIVACAO_INTERFEROMETRO_MINIMO_05nov.md&line=226&text=T(z)%3D%5Cint_0%5Ez%5Cfrac%7Bdz'%7D%7B(1%2Bz')H(z')%7D "citation")

A coerência entre caminhos também não é automaticamente a função \(g^{(1)}\) de uma linha espectral. Uma eventual difusão de fase temporal,

\[
g_1(\tau)=e^{-i\omega_0\tau}e^{-\gamma|\tau|},
\]

produz uma Lorentziana normalizada sem perda de intensidade integrada, mas sua \(\gamma\) não é automaticamente a taxa de propagação \(\Gamma_{AB}\). Igualá-las exige uma dinâmica e uma convenção comuns demonstradas.

Nenhuma correção fotometria–espectroscopia ou desvio photo-z–spec-z segue do canal até aqui: populações e intensidade total permanecem preservadas.

---

## 9. Provas ainda necessárias

- [ ] **Escolher o operador físico sem homônimos:** lock, `HminMic`, Hamiltoniano modular e \(K\) de R–E são objetos a relacionar por teoremas, não por nome.
- [ ] **Se o candidato for o lock:** derivar a referência \(\Omega\) física e sua projeção \(Q\Omega\) no espaço dos caminhos.
- [ ] **Obter os autovalores:** demonstrar \(K|A\rangle=k_A|A\rangle\) e \(K|B\rangle=k_B|B\rangle\). Para o lock do vácuo, a conta já dá \(1,1\); não se pode substituir por \(0,1\).
- [ ] **Se \(Q\Omega=0\):** aceitar \(\Gamma=0\) nesse ramo e procurar outro portador, sem reintroduzir \(\beta/2\).
- [ ] **Se \(Q\Omega\) for alinhado a um caminho:** derivar fisicamente essa seleção e sua simetria; não assumi-la pelo sinal desejado.
- [ ] **Se o lock não for diagonal nos caminhos:** transformar o superoperador para a base de \(K\) e refazer a evolução da matriz de densidade.
- [ ] **Derivar o canal:** mostrar que \(L=\sqrt\beta\sqrt K\) atua sobre o fóton durante \(T\), preservando traço e populações, em vez de apenas reproduzir uma forma algébrica.
- [ ] **Fechar unidades e escala:** definir o caráter adimensional de \(T\) ou derivar a taxa física e a conversão para segundos/comprimento.
- [ ] **Separar coerência de caminho e \(g^{(1)}\):** só depois discutir perfil espectral.
- [ ] **Só então congelar previsão e nulo:** calibração de \(V_0\), covariância, duas independências e requisito de 5σ; nenhum dado antes disso.

---

## 10. Veredito técnico desta etapa — atualizado após a derivação geral

**[DECLARADO pelo Kimi]:** o lock mínimo oferece formalmente os autovalores \(0/1\), mas a classificação completa e a conferência do modular fecharam os candidatos físicos disponíveis para o modelo de um fóton:

1. o **lock do vácuo**, disponível no habitante físico de Fock da cadeia v406–v408, atribui \(1,1\) aos dois estados de um fóton e portanto \(\Gamma=0\);
2. o resultado positivo \(\beta/2\), com populações dos caminhos universalmente preservadas, exige \(r=1\) e referência inteiramente alinhada a um caminho — uma entrada física não derivada;
3. o lock do próprio estado não evolui, e o lock simétrico pode trocar populações entre os caminhos;
4. o **Hamiltoniano modular** não possui autostados não nulos no setor de uma partícula, por `B0_no_eigen`; portanto não fornece \(k_A,k_B\) aos caminhos;
5. a tradução de Turing R1–R8 não supre um novo operador óptico;
6. falta ainda fechar a dimensão da taxa e o tempo de atuação para qualquer novo canal.

A derivação completa, a solução para referência arbitrária e a verificação dos seis casos estão em [DERIVACAO_OMEGA_K_LOCK_NO_GO_05nov](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/DERIVACAO_OMEGA_K_LOCK_NO_GO_05nov.md).

**Estado final atualizado:** `LOCK_AND_MODULAR_K_NO_GO_FOR_ONE_PHOTON_PATH_MODEL` · `OPEN_NEW_PHYSICAL_CHANNEL`. Não há previsão TGL sem ajuste nem teste pronto. A próxima derivação legítima deve procurar um mecanismo fora do lock do vácuo e do gerador modular, ou modificar explicitamente o modelo físico.
