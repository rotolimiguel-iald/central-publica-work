# Dicionário com o controle CE exato da raiz

10/09/2026. [DERIVED — comparação algébrica escrita]. Adendo novo à [construção de Pontryagin até C5](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>), preservada. O [recibo CE da raiz](<C:/IALD/Central de Patentes/Chatgpt/ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/RESULTADO_CE_EXATO_077.json>) foi lido, não reexecutado.

O recibo registra as três assinaturas, dimensões invariantes 0/4/3 nos graus 2/3/4, posto três e núcleo unidimensional do primeiro diferencial, com linha do Cartan. Esta é evidência aritmética finita produzida pela raiz; não equivale a uma auditoria aqui do código inteiro ou do BRST de jatos. A construção sem antifields da nota principal independe da precisão separada do sinal KT077.

Para comparar representantes e não só dimensões, use precisamente a convenção registrada: X_ab[a,b]=ε_a, X_ab[b,a]=−ε_b e dθ_k=−Σ_(i<j) f_ij^k θ_iθ_j. Ponha

\[
\Theta=\sum_{a<b}\theta_{ab}X_{ab},\qquad d\Theta=-\Theta^2.
\tag{D1}
\]

Separando os índices tangentes 0,…,3 e o normal 4, a matriz tem a forma

\[
\Theta=\begin{pmatrix}M&u\\-\varepsilon_4u^\flat&0\end{pmatrix},
\qquad u^a=\varepsilon_a\theta_{a4},
\quad g_{ab}=\varepsilon_a\delta_{ab}.
\tag{D2}
\]

Para a normalização |K|=1, escolha K=ε4 e p=u. Assim a componente tangente de (D1) é dM=−M²+Kpp♭ e dp=−Mp, na convenção da nota principal. Para |K| distinto de um, u=√|K| p e ε4=sign(K) dão o mesmo dicionário após a reescala do setor de translações. Essa mudança de geradores não exige nem introduz uma raiz de K negativo.

Expandir o cubo de (D2) e usar a ciclicidade graduada dá

\[
\operatorname{tr}(\Theta^3)
=\operatorname{tr}(M^3)-3\operatorname{tr}(M Kpp^\flat).
\tag{D3}
\]

Por outro lado, defina a forma de Cartan na convenção do recibo por

\[
\mathscr C=\sum_{i<j<k}
\operatorname{tr}(X_i[X_j,X_k])\theta_i\theta_j\theta_k.
\]

As seis permutações de cada produto no traço do cubo de Θ dão três vezes esse coeficiente. Logo

\[
\boxed{\alpha_3=\operatorname{tr}(M Kpp^\flat)
-\tfrac13\operatorname{tr}(M^3)
=-\tfrac13\operatorname{tr}(\Theta^3)=-\mathscr C.}
\tag{D4}
\]

Isso fixa o sinal global na convenção CE da raiz. No controle espacial θ12θ13θ23, correspondente aos índices 4/5/7 da lista basis_pairs do recibo, Cartan tem coeficiente +2 nas três assinaturas registradas. A expressão (D4) tem coeficiente −2. A mudança m_ab=∇_[a C_b] para M_ab=−m_ab já foi explicitada na nota principal; ela não pode ser omitida numa comparação de componentes.

[DERIVED] O líder de Pontryagin é a negativa da cúbica de Cartan registrada, portanto gera a mesma linha sobrevivente. Isso complementa o controle de não nulidade da nota principal e a construção até C5; não modifica seus limites em valência seis e nas ordens posteriores.

[REAL — documental] Pins do recibo, do seu script e das duas fontes próprias foram medidos antes/depois, sem importar ou executar o script CE. O manifesto deste adendo não substitui o manifesto anterior. Zero novos CAS, Lean ou um.py; nenhuma aprovação por outro revisor atribuída.


## Precisões de leitura e da convenção KT

A reescala por √|K| em (D2) é somente um dicionário para o controle finito da álgebra de Killing com K fixo e não nulo. Ela não é usada na fórmula natural original α3=K m_ab p^ap^b+⅓tr(m³), que não contém divisão por K e permanece regular quando K varia. Não se introduz por esse controle uma categoria universal que permita coeficientes singulares em K.

A vírgula de separação na equação (7) da nota principal é apenas tipográfica. O primeiro coeficiente possível deve ser lido como o PRODUTO

\[
(A_P)_{[6]}=\rho_{[2]}[h,h]\,C^0C^1C^2C^3.
\tag{D5}
\]

ρ[2][h,h] é o coeficiente quadrático da densidade tr(W[1]∧W[1]); não é um argumento adicional do ghost nem uma operação de vírgula. Nada é alterado na fonte congelada.

O [adendo do sinal Koszul–Tate077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>) já corrige o sinal para s0u*=+H0u e conserva s0c*=+R0†u*. Foi lido integralmente para esta ponte. A construção de Pontryagin usa expressões sem antifields e somente sg/sc; seus líderes e suas correções até C5 não mudam com a correção. Isso não autoriza usar a convenção antiga em outros cálculos com antifields.

O primeiro script de emissão do dicionário havia sido criado, mas não executado, quando a raiz solicitou estas precisões. Foi conservado intacto. Este novo script lê somente sua string literal NOTE por AST/literal_eval e emite o adendo completo por escrita exclusiva. Nenhum código daquele rascunho ou do controle CE é executado/importado.
