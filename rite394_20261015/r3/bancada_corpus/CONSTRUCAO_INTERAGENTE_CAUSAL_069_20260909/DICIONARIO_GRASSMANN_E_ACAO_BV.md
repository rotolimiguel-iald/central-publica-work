# Dicionário de operadores para campos Grassmann e ação BV livre

09/09/2026. [DERIVED — demonstração escrita]. Adendo novo à construção BRST 068; nenhuma fonte anterior foi alterada. O objetivo é fornecer a apresentação de campos e anticampos usada na construção causal das interações, conservando os operadores e o estado físico já obtidos.

## 1. Duas apresentações, com o pareamento explicitado

A [nota 068](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md>) usa o operador formalmente autoadjunto L de Wrochna–Zahn, com blocos ghost simétricos Q. Essa apresentação usa campos complexos e pareamentos sesquilineares. Ela não deve ser inserida, sem dicionário, como a Hessiana bilinear de uma ação com duas variáveis Grassmann reais: tal Hessiana é antissimétrica no setor ímpar.

As convenções de campos carregados e de graduação constam de [Wrochna–Zahn, §§3.1–3.2](https://arxiv.org/html/1407.8079v2). Para a convenção bilinear graduada de ações e Green, o contrato pertinente é [Fröb, §2, equações (1)–(6)](https://arxiv.org/pdf/1803.10235). Aqui construímos o dicionário diretamente.

Na ordem \(x=(u,b,c,\bar c)\), ponha
\[
J=\operatorname{diag}(1_V,1_W,1_W,-1_W),\qquad
P_{\rm gr}=LJ=
\begin{pmatrix}
\mathcal H&C^*&0&0\\
C&-\ell^{-1}&0&0\\
0&0&0&-Q\\
0&0&Q&0
\end{pmatrix}.
\tag{1}
\]
O símbolo J nesta nota é apenas essa matriz de conversão dos slots; não é identificado com o J modular ou com o vocabulário ontológico da TGL.

Com derivadas esquerda/direita para as variáveis ímpares, (1) é a Hessiana da ação
\[
S_0^{\rm gf}=\tfrac12\langle u,\mathcal Hu\rangle
+\langle b,Cu\rangle-\frac1{2\ell}\langle b,b\rangle
+\langle\bar c,Qc\rangle.
\tag{2}
\]
De fato \(\frac12[-cQ\bar c+\bar cQc]=\bar cQc\), por integração por partes e anticomutação. Em componentes, \(P_{AB}=(-1)^{p_Ap_B}P_{BA}^{\mathrm t}\), onde t transpõe também os índices de fibra e as derivadas. Os setores físicos são idênticos aos de 068. Não estamos afirmando que multiplicação de um único slot por J seja uma congruência de mudança de base de uma forma bilinear; é a apresentação graduada definida por (2).

## 2. Green, covariâncias reais e orientação

Como \(J^2=1\), os inversos exatos são
\[
G_{\rm gr}^{\rm ret/adv}=J G_L^{\rm ret/adv},\qquad
G_{\rm gr}^{F}=J G_L^F.
\tag{3}
\]
As duas inversões seguem de \((LJ)(JG_L)=1\) e \((JG_L)(LJ)=1\). Suporte causal e frente de onda são preservados. Em particular o bloco ghost é
\[
G_{{\rm gr},\rm ghost}=
\begin{pmatrix}0&G_Q\\-G_Q&0\end{pmatrix}.
\tag{4}
\]

Para usar variáveis reais, podemos escolher os pares de covariâncias de D e Q com \(W^-=(W^+)^{\mathrm t}\). Essa escolha não precisa ser presumida da mera hermiticidade. Como os operadores e C,K são reais, aplique, se necessário,
\[
\widehat W^+=\tfrac12(W^++\overline{W^-}),\qquad
\widehat W^-=\tfrac12(W^-+\overline{W^+}).
\tag{5}
\]
Cada parcela satisfaz as equações; as Ward são preservadas por realidade. Com \(W^+-W^-=i\hbar E\) e E real, a diferença em (5) continua \(i\hbar E\). A conjugação troca as orientações microlocais, de modo que os dois termos de cada média têm a orientação correta. Hermiticidade e \(\widehat W^-=\overline{\widehat W^+}\) dão a transposição desejada. O bloco físico 067 já é o par real de campos construído pelos modos; por isso (5) não muda sua restrição positiva.

Use esses pares na fórmula matricial 068 e defina
\[
\mathcal W^+=J\Lambda_L^+,\qquad \mathcal W^-=J\Lambda_L^-.
\tag{6}
\]
Então \(\mathcal W^-=(\mathcal W^+)^{\mathrm t}\). No bloco ghost,
\[
\mathcal W^+_{c\bar c}=W_Q^+,\quad
\mathcal W^+_{\bar c c}=-W_Q^+,\quad
\mathcal W^-_{c\bar c}=-W_Q^-,\quad
\mathcal W^-_{\bar c c}=W_Q^-.
\]
Portanto a soma no anticomutador ghost é \(i\hbar E_{{\rm gr},\rm ghost}\), enquanto a diferença no comutador bosônico é \(i\hbar E_{{\rm gr},B}\). Isso verifica a reciprocidade graduada em componentes, além da inversão abstrata.

Uma involução compatível é \(u^*=u\), \(b^*=b\), \(c^*=c\), \(\bar c^*=-\bar c\), com reversão da ordem dos fatores. Ela torna \(\bar cQc\) real. O antighost não é o conjugado do ghost. Outra convenção pode usar antighost hermitiano e um fator i explícito; não se misturam os dois contratos.

O inverso Feynman (3) conserva o contato \(\ell^2 C G_D^F C^*=\ell I\). A entrada b–b continua zero porque o complemento de Schur subtrai exatamente \(\ell I\). Nada nessa conversão elimina contatos por conveniência.

## 3. Diferencial livre e anticampos

Na apresentação (2), fixe
\[
s_0u=Kc,\qquad s_0c=0,\qquad s_0\bar c=-b,\qquad s_0b=0.
\tag{7}
\]
No nível das componentes, a matriz é \(J\gamma J\); o sinal do antighost acompanha a apresentação da ação. A nilpotência é imediata. A variação da parte bosônica é \(\langle b,CKc\rangle\), pois \(\mathcal HK=0\); a da parte ghost é \(-\langle b,Qc\rangle\). Elas se cancelam por \(CK=Q\). Logo \(s_0S_0^{\rm gf}=0\).

Introduza anticampos \(u^\ddagger,b^\ddagger,c^\ddagger,\bar c^\ddagger\) de paridade oposta e número fantasma \(-1-\mathrm{gh}(x)\). Eles são fontes externas; suas contrações são zero. Com o antibracket canônico escolhido para gerar (7),
\[
S_0^{\rm BV}=S_0^{\rm gf}
+\langle u^\ddagger,Kc\rangle-\langle\bar c^\ddagger,b\rangle
\tag{8}
\]
satisfaz \((S_0^{\rm BV},S_0^{\rm BV})=0\): os termos sem anticampos são a invariância acabada de demonstrar e os termos com anticampos são a nilpotência de (7). O diferencial nos anticampos é então fixado pela mesma ação e fornece a parte Koszul–Tate livre.

A compatibilidade das contrações com (7) pode ser vista diretamente em entradas mistas. Por exemplo, a variação da contração u–barc é \(K W_Q^+-K W_Q^+=0\); a de barc–u é \(-W_Q^+K^*+W_Q^+K^*=0\). Os demais casos seguem de \(QW_Q^+=0\), das Ward e da regra graduada. Assim o diferencial livre se estende à álgebra livre, não apenas aos geradores lineares. Nas ordenações locais de Wick, a representação do diferencial acompanha o isomorfismo de mudança suave de ordenação.

## 4. Gauge fixado não linear que reproduz exatamente esses dados

[INPUT] A ação física é a Einstein–sigma de 067. No espaço completo dos campos use o gauge de difeomorfismos \(sg=\mathcal L_cg\), \(s\phi=\mathcal L_c\phi\), \(sc=c^\mu\partial_\mu c\), \(s\bar c=-b\), \(sb=0\), com o sinal do antibracket ajustado a essa convenção. A nilpotência é a identidade de Jacobi graduada.

Com o C de fundo linear em h, a férmion de gauge
\[
\Psi=-\langle\bar c,Ch-b/(2\ell)\rangle
\]
produz
\[
s\Psi=\langle b,Ch\rangle-\frac1{2\ell}\langle b,b\rangle
+\langle\bar c,C(sh)\rangle.
\tag{9}
\]
Sua parte quadrática é precisamente (2). A interação ghost inclui \(\bar c C\mathcal L_ch\). A matéria participa das equações e dos termos com anticampos; ela não precisa ser artificialmente inserida em C para obter o acoplamento já existente na Hessiana D.

Como C é linear de fundo, b não aparece nos vértices de interação sem anticampos. Ele não gera novos laços propagantes. Inserções de b continuam definidas pelas entradas mistas e pelos contatos de (3); não se confunde sua eliminação gaussiana com nilpotência off-shell de um BRST reduzido sem anticampos.

[DERIVED] Este adendo fornece a tradução efetiva da construção 068 para a ação BV graduada necessária em Q2. [OPEN] Não calcula a anomalia interagente nem a remove. Nenhum Lean, um.py ou CAS foi executado para produzir esta demonstração.
