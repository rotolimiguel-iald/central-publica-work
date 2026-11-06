# Derivação de \(\Omega\) e \(K\) — classificação geral do lock e no-go modular

**Data:** 05/11/2026  
**Estatuto:** **[DECLARADO pelo Kimi]**, com composição manual de teoremas do kernel e verificação algébrica; não é uma nova pedra Lean nem conferência da gerência.  
**Estado:** `LOCK_AND_MODULAR_K_NO_GO_FOR_ONE_PHOTON_PATH_MODEL` · `OPEN_NEW_PHYSICAL_CHANNEL` · `NO_DATA_OPENED` · `NO_VERDICT`.  
**Escopo:** decidir se o lock ou o Hamiltoniano modular pode fornecer \(k_A,k_B\) ao interferômetro mínimo sem inserir uma escolha manual de caminho.

---

## 1. Resultado

Para o modelo de um fóton com dois caminhos e salto hermitiano \(L=\sqrt\beta\sqrt K\), os candidatos físicos examinados não produzem o canal não trivial procurado:

1. **Lock do vácuo:** \(K=1-P_{\rm vac}\) é a identidade no setor de uma partícula; logo \(k_A=k_B=1\) e \(\Gamma_{AB}=0\).
2. **Hamiltoniano modular \(K=-\log\Delta\):** nenhum vetor não nulo de uma partícula é autovetor do boost com fase; portanto os estados de um fóton dos caminhos não podem ser autostados do \(K\) modular. Os números \(k_A,k_B\) exigidos pela prescrição não existem nesse setor.
3. **Lock com referência arbitrária:** a taxa é controlada por \(r=\|Q\Omega\|\), mas a preservação universal das populações dos caminhos exige que o lock seja diagonal na base dos caminhos. O caso \(\Gamma=\beta/2\) só ocorre quando \(\Omega\) é inteiramente um dos caminhos. Isso é uma escolha física adicional, não uma consequência do vácuo, do modular ou da tradução de Turing.
4. **Lock do próprio estado de entrada:** embora haja dois autovalores, o estado inicial é autostado de \(K\); logo não evolui e não perde coerência.
5. **Lock simétrico entre caminhos:** não preserva universalmente as populações dos caminhos e não produz a lei simples \(V(T)=V_0e^{-\Gamma T}\).

**Consequência:** a rota lock/modular está fechada **como fonte do modelo de defasagem de caminho de um fóton aqui definido**. Isso não falsifica a TGL nem exclui um novo canal físico fora desses operadores. O \(K\) escalar da lei de Hubble é outro homônimo e não preenche a lacuna.

---

## 2. Premissas do modelo

Os caminhos são estados ortonormais de um fóton,

\[
|A\rangle=|1_A,0_B\rangle,\qquad |B\rangle=|0_A,1_B\rangle,
\qquad S=\operatorname{span}\{A,B\}.
\]

A entrada é \(|\psi\rangle=a|A\rangle+b|B\rangle\), com \(|a|^2+|b|^2=1\). O salto candidato é

\[
L=\sqrt\beta\sqrt K,
\qquad K=K^\dagger\ge0,
\]

e, na base de autostados de \(K\),

\[
\rho_{ij}(T)=\rho_{ij}(0)e^{-\Gamma_{ij}T},
\qquad
\Gamma_{ij}=\frac\beta2(\sqrt{k_i}-\sqrt{k_j})^2.
\]

A prescrição é a usada na rota R–E; sua aplicação física à luz permanece uma hipótese nomeada. [DERIVACAO_RE_02nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Crota_RE_dualidade_02nov%5CDERIVACAO_RE_02nov.md&line=18&text=A%20fam%C3%ADlia%20do%20vazamento%20%C3%A9%20defasagem. "citation")

Para obter o interferômetro mínimo já derivado, exige-se adicionalmente:

- os caminhos são autostados de \(K\);
- as populações \(\rho_{AA}\) e \(\rho_{BB}\) são preservadas para toda entrada;
- apenas \(\rho_{AB}\) e \(\rho_{BA}\) decaem;
- o traço total permanece 1.

Essas condições não serão relaxadas silenciosamente: um canal que troca populações entre caminhos é outro modelo e exige outra partitura experimental.

---

## 3. Lock com referência arbitrária: solução em um único parâmetro

Seja \(\Omega\) normalizado e

\[
K_\Omega=1-P_\Omega=1-|\Omega\rangle\langle\Omega|.
\]

O kernel prova \(K_\Omega\Omega=0\) e \(K_\Omega\chi=\chi\) para todo \(\chi\perp\Omega\). [PontoZeroDoPsion](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPontoZeroDoPsion.lean&text=theorem%20o_lock_tem_gap_um%20(%CE%A9%20%CF%87%20%3A%20F)%20(hort%20%3A%20%E2%9F%AA%CE%A9%2C%20%CF%87%E2%9F%AB_%E2%84%82%20%3D%200)%20%3A%20lockDe%20%CE%A9%20%CE%A9%20%3D%200%20%E2%88%A7%20lockDe%20%CE%A9%20%CF%87%20%3D%20%CF%87 "citation")

Seja \(Q\) o projetor sobre \(S\). Escreva

\[
Q\Omega=\alpha A+\tau B,
\qquad
r^2:=\|Q\Omega\|^2=|\alpha|^2+|\tau|^2,
\qquad 0\le r\le1.
\]

A restrição ao espaço dos caminhos é

\[
K_S:=QK_\Omega Q
=I_S-|Q\Omega\rangle\langle Q\Omega|
=
\begin{pmatrix}
1-|\alpha|^2 & -\alpha\tau^*\\
-\alpha^*\tau & 1-|\tau|^2
\end{pmatrix}.
\]

### 3.1 Autovalores e taxa exata

Se \(r>0\), defina

\[
|e\rangle=\frac{Q\Omega}{r}=uA+vB,
\qquad
|o\rangle=-v^*A+u^*B.
\]

Nessa base ortonormal,

\[
K_S=(1-r^2)|e\rangle\langle e|+|o\rangle\langle o|.
\]

Logo,

\[
\boxed{k_e=1-r^2,\qquad k_o=1}
\]

e a taxa entre os dois modos do lock é

\[
\boxed{
\Gamma_{\rm lock}(r)
=\frac\beta2\left(\sqrt{1-r^2}-1\right)^2
=\frac\beta2\left(1-\sqrt{1-r^2}\right)^2.
}
\]

Os casos extremos são

\[
\Gamma_{\rm lock}(0)=0,
\qquad
\Gamma_{\rm lock}(1)=\frac\beta2.
\]

Para \(r\ll1\),

\[
\Gamma_{\rm lock}(r)=\frac\beta8r^4+O(r^6).
\]

Portanto, uma componente pequena da referência dentro do espaço dos caminhos produz apenas uma taxa de quarta ordem em \(r\). Este comportamento não pode ser substituído por \(\beta/2\) sem fixar \(r=1\).

### 3.2 A base dos caminhos e a preservação das populações

O elemento fora da diagonal de \(K_S\) é \(-\alpha\tau^*\). Para que a base dos caminhos seja uma base de autostados do lock, é necessário e suficiente que

\[
\boxed{\alpha\tau^*=0}.
\]

Há então somente estas possibilidades:

| Caso | Autovalores na base \(A,B\) | Taxa | Consequência |
|---|---|---|---|
| \(r=0\) | \(k_A=k_B=1\) | 0 | Nenhuma defasagem; inclui o lock do vácuo. |
| \(\tau=0,\ 0<r=|\alpha|\le1\) | \(k_A=1-r^2,\ k_B=1\) | \(\Gamma_{\rm lock}(r)\) | Preserva populações; \(\beta/2\) só se \(r=1\). |
| \(\alpha=0,\ 0<r=|\tau|\le1\) | \(k_A=1,\ k_B=1-r^2\) | \(\Gamma_{\rm lock}(r)\) | Mesma forma com os caminhos trocados. |

**Correção à classificação anterior:** \(Q\Omega\propto A\) não basta para \(k_A=0\). Se \(\Omega\) tiver componente fora de \(S\), então \(r<1\) e \(k_A=1-r^2>0\). O par exato \(0/1\) exige simultaneamente alinhamento e \(r=1\), isto é, \(\Omega=e^{i\varphi}A\) ou \(\Omega=e^{i\varphi}B\).

Se \(\alpha\tau^*\ne0\), o lock ainda tem a taxa \(\Gamma_{\rm lock}(r)\) em **sua própria base**, mas essa base não é a dos caminhos. Não se pode atribuir essa taxa diretamente a \(\rho_{AB}\).

---

## 4. Dinâmica exata na base dos caminhos

Para \(r>0\), escreva a entrada na base do lock:

\[
c:=\langle e|\psi\rangle=u^*a+v^*b,
\qquad
d:=\langle o|\psi\rangle=-va+ub.
\]

A evolução é exatamente

\[
\rho_{ee}(T)=|c|^2,
\qquad
\rho_{oo}(T)=|d|^2,
\qquad
\rho_{eo}(T)=e^{-\Gamma_{\rm lock}(r)T}cd^*.
\]

O traço é preservado. Contudo, ao retornar à base dos caminhos,

\[
\boxed{
\rho_{AB}(T)
=uv(|c|^2-|d|^2)
+e^{-\Gamma_{\rm lock}(r)T}
\left(|u|^2cd^*-|v|^2c^*d\right).
}
\]

Em geral:

- \(\rho_{AB}\) **não** é simplesmente \(\rho_{AB}(0)e^{-\Gamma T}\);
- pode restar coerência residual \(uv(|c|^2-|d|^2)\);
- as populações \(\rho_{AA}\) e \(\rho_{BB}\) podem variar;
- a visibilidade não precisa obedecer \(V=V_0e^{-\Gamma T}\).

A solução foi comparada numericamente com a diagonalização completa do operador e com o dissipador de um único salto hermitiano. Todos os seis casos passaram, com erro máximo de fórmula abaixo de \(10^{-10}\) nos testes. [VERIFICACAO_LOCK_GERAL](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/VERIFICACAO_LOCK_GERAL.json), gerado por [verificar_lock_geral](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/verificar_lock_geral.py).

---

## 5. Três no-gos físicos do lock

### 5.1 Vácuo: \(r=0\)

O vácuo é ortogonal a todo estado do setor de uma partícula. Assim, para \(\Omega=\Omega_{\rm vac}\),

\[
Q\Omega=0,
\qquad K_S=I_S,
\qquad k_A=k_B=1,
\qquad \boxed{\Gamma_{AB}=0}.
\]

Não há decaimento de \(\rho_{AB}\), mudança de população ou perda de visibilidade por esse mecanismo.

### 5.2 Lock do próprio estado: nenhuma evolução

Se \(\Omega=\psi\), então \(r=1\), \(c=1\) e \(d=0\). O estado inicial é o modo zero do lock:

\[
K_\Omega|\psi\rangle=0.
\]

Apesar de \(\Gamma_{\rm lock}(1)=\beta/2\) entre os **dois modos do lock**, não existe coerência inicial entre eles:

\[
\rho(0)=|\Omega\rangle\langle\Omega|
\quad\Longrightarrow\quad
\boxed{\rho(T)=\rho(0)}.
\]

Identificar a referência do lock ao estado do fóton, portanto, não gera decoerência.

### 5.3 Lock simétrico: troca populações de caminho

Para

\[
\Omega=\frac{A+B}{\sqrt2},
\qquad
K_S=\frac12
\begin{pmatrix}
1&-1\\
-1&1
\end{pmatrix},
\]

o lock é diagonal na base \(|+\rangle,|-\rangle\), não na base \(A,B\). Para a entrada inicial \(|\psi\rangle=|A\rangle\), a coerência entre \(|+\rangle\) e \(|-\rangle\) decai e, quando \(\Gamma T\to\infty\),

\[
\rho(T)\longrightarrow
\frac12\left(|+\rangle\langle+|+|-\rangle\langle-|\right)
=\frac{I_S}{2}.
\]

Logo,

\[
\rho_{AA}:1\longrightarrow\frac12,
\qquad
\rho_{BB}:0\longrightarrow\frac12.
\]

O traço total é preservado, mas as populações dos caminhos não. Portanto, uma referência simétrica não realiza o canal de defasagem de caminho exigido. A verificação numérica obteve esse comportamento sem nenhum dado externo.

**No-go de simetria:** uma referência não trivial invariante ou anti-invariante sob \(A\leftrightarrowB\) tem \(|u|=|v|\) e \(uv\ne0\); logo não é diagonal na base dos caminhos. O canal universal que preserva as populações de todos os estados de entrada exige quebrar essa simetria ou usar outro operador.

---

## 6. No-go do Hamiltoniano modular no setor de uma partícula

A cadeia da luz identifica o fluxo modular com a segunda quantização do boost:

\[
\Delta^{it}=\Gamma\!\left(B0(-2\pi t)\right).
\]

Essa é a definição usada para o conjunto fixo modular e o \(K=-\log\Delta\) da luz. [QGReaderUVLock](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CQGReaderUVLock.lean&text=o%20conjunto%20fixo%20do%20fluxo%20modular%20%CE%94%5E%7Bit%7D%20%3D%20%CE%93(B0(%E2%88%922%CF%80t))%20%E2%80%94%20o%20n%C3%BAcleo%20do%20Hamiltoniano "citation")

No espaço de uma partícula, a segunda quantização reduz-se ao próprio \(B0\). O kernel contém o teorema

\[
\left(\forall s,\ \exists c_s,\ |c_s|=1\ \wedge\ B0(s)f=c_s f\right)
\Longrightarrow f=0.
\]

Ou seja, nenhum vetor não nulo de uma partícula é autovetor do boost com fase. [TheImportedSecondQuantization](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CTheImportedSecondQuantization.lean&text=theorem%20B0_no_eigen%20(f%20%3A%20H1)%20(h%20%3A%20%E2%88%80%20s%20%3A%20%E2%84%9D%2C%20%E2%88%83%20c%20%3A%20%E2%84%82%2C%20%E2%80%96c%E2%80%96%20%3D%201%20%E2%88%A7%20B0%20s%20f%20%3D%20c%20%E2%80%A2%20f)%20%3A%20f%20%3D%200 "citation")

Se um estado de um fóton \(f\) fosse autostado do Hamiltoniano modular,

\[
Kf=kf,
\]

o cálculo funcional auto-adjunto daria, no domínio apropriado,

\[
\Delta^{it}f=e^{-ikt}f,
\]

que é exatamente um autovetor do boost com fase, proibido pelo teorema. A conclusão vale para qualquer \(k\in\mathbb R\).

Portanto,

\[
\boxed{
\text{nenhum }A\text{ ou }B\text{ não nulo de uma partícula é autostado do }K\text{ modular}.
}
\]

Isso não afirma ausência de autovetores com fase em todos os setores de muitas partículas; o próprio acervo ressalva essa distinção. O no-go aqui é específico ao setor de **uma partícula**, que é o do interferômetro definido. [OUmInscrito](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5COUmInscrito.lean&text=Autovetores%20com%20fase%20(%60%CE%93(B0%20s)%20%CF%88%20%3D%20c(s)%20%E2%80%A2%20%CF%88%60%2C%20%60%E2%80%96c(s)%E2%80%96%20%3D%201%60)%20nos%20setores%20de%20n%20%E2%89%A5%201%20particulas%20NAO%20sao%20excluidos%20por%20este%20termo%3B "citation")

A consequência para esta rota é direta: o \(K\) modular não fornece \(k_A,k_B\) escalares aos caminhos de um fóton. Usá-lo exigiria outro setor, outra dinâmica ou uma transformação fora da prescrição de autostados.

---

## 7. Os demais homônimos não abrem uma saída

- **`HminMic`:** é \(1-P_\Omega\), não o \(K\) modular; sua identificação com o \(H_{\min}\) abstrato do programa também permanece separada. [QGCitationDischarge](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CQGCitationDischarge.lean&text=%60HminMic%20%3A%3D%201%20%E2%88%92%20P_%CE%A9%60%20(v372)%20%C3%A9%20um%20HOM%C3%94NIMO%20do%20H_min%20do%20programa "citation")
- **\(K\) da razão de Hubble:** `OIgual.K` é um número \((E_b/E_a)^{2\beta/3}\), não um operador sobre os caminhos; a própria pedra separa esse homônimo do \(K\) modular. [OIgual](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5COIgual.lean&text=Tr%C3%AAs%20hom%C3%B4nimos%3A%20este%20K%20%C3%A9%20a%20raz%C3%A3o%20de%20Hubble%3B%20o%20K%20modular%20%C3%A9%20outro%20objeto "citation")
- **Chave da guarda:** restaura a coerência por \(e^{+tG}\) quando o registro é conhecido; não é um canal físico de propagação e não determina \(K\). [AChaveDaGuarda](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CAChaveDaGuarda.lean&text=Que%20o%20custo%20de%20um%20par%20seja%20o%20da%20lei%20de%20Hubble%20e%20HIPOTESE%20nomeada%20(%60hform%60).%20Ler%20a%20chave%20como%20K%20e%20leitura%20%5BONTO%5D. "citation")
- **Custo de instância e trava de Turing:** operam no espaço de atribuições e não fornecem autostados ópticos nem o salto fotônico.
- **Projetor de caminho:** \(K=P_A\) ou \(K=P_B\) daria o par \(0/1\), mas nenhuma das pedras examinadas o deriva como ambiente TGL. É um modelo fenomenológico de «qual caminho», não uma previsão sem ajuste.

---

## 8. O que ficou demonstrado e o que não ficou

### [REAL — dentro das premissas declaradas]

- fórmula de \(K_S\) para referência arbitrária;
- autovalores \(1-r^2,1\);
- taxa \(\Gamma_{\rm lock}(r)=\frac\beta2(1-\sqrt{1-r^2})^2\);
- condição \(\alpha\tau^*=0\) para a base dos caminhos ser a base do lock;
- classificação dos canais que preservam universalmente as populações dos caminhos;
- \(\Gamma=0\) para o lock do vácuo;
- ausência de evolução para o lock do próprio estado;
- mudança de populações para o lock simétrico genérico;
- ausência de autostados modulares não nulos no setor de uma partícula, por composição do cálculo funcional com `B0_no_eigen`.

### [INPUT/ONTO — continua não derivado]

- que algum lock deva representar o ambiente do interferômetro;
- que uma referência possa ser escolhida como um dos caminhos sem destruir a simetria física;
- que um novo operador, fora do lock e do modular, produza defasagem óptica;
- que o parâmetro \(T\) seja tempo físico e qual escala converte \(\beta\) em taxa;
- qualquer ligação entre essa coerência de caminho e \(g^{(1)}\) espectral.

### O que este resultado não significa

- não é falsificação da TGL;
- não é prova de que toda defasagem fotônica seja impossível;
- não exclui modelos de muitas partículas, ambientes com memória, saltos múltiplos ou canais que mudem populações;
- não produz veredito experimental nem move o gate.

---

## 9. Pergunta física que realmente falta

A pergunta deixou de ser «qual é o autovalor do lock?». A matemática já respondeu essa parte.

A pergunta restante é:

> **Qual mecanismo físico, distinto do lock do vácuo e do gerador modular, distingue os dois caminhos de um fóton, preserva suas populações e gera um salto hermitiano com autovalores determinados?**

Sem uma resposta derivada, \(K=P_A\), \(\Omega=A\) ou \(k_A=0,k_B=1\) são entradas fenomenológicas. Com elas, a fórmula \(V=V_0e^{-\beta T/2}\) é correta como modelo, mas não é uma previsão autônoma da teoria.

---

## 10. Estado final

**[DECLARADO pelo Kimi]:** os dois candidatos físicos explícitos disponíveis na cadeia examinada não alimentam o interferômetro mínimo:

\[
\boxed{\text{lock do vácuo: }\Gamma=0},
\qquad
\boxed{\text{modular: não há autostados }A,B\text{ de uma partícula}}.
\]

O lock arbitrário só chega a \(\beta/2\) com preservação universal das populações quando a referência é inteiramente um dos caminhos. Nenhuma das fontes examinadas deriva essa escolha.

**Estado:** `LOCK_AND_MODULAR_K_NO_GO_FOR_ONE_PHOTON_PATH_MODEL` e `OPEN_NEW_PHYSICAL_CHANNEL`. A próxima etapa científica legítima é procurar um mecanismo fora desses dois operadores ou modificar explicitamente o modelo físico; não é prosseguir para dados com \(\beta/2\) como se fosse previsto.
