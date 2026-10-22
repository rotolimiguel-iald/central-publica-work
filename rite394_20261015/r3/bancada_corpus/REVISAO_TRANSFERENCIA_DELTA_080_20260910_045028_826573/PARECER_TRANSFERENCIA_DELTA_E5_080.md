# Parecer independente: transferência de δ(K) para d1 em E5

10/09/2026. Revisor /root/selected_geometry_design. Frente080. Revisão matemática de prova algébrica escrita, sem CAS, Lean, execução/importação de um.py ou alteração de fontes.

**Parecer favorável no alcance declarado; não identifiquei erro material.** Li integralmente [IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) e seu manifesto. A fonte mede 7491 bytes, SHA-256 1cdc1e78f345f8674d7bc617466e261870d3b20c39281b91a794cd28a0d70d90, obtidos dos bytes nesta revisão.

A igualdade δ(K)=im(d1 em E5) segue da remoção E4 já revisada, sem afirmar a injetividade de q ou conhecer a imagem de d1. O critério −[A6]∈im d1 é necessário e suficiente somente para o levantamento C5→C6 com o mesmo líder cohomológico em C3.

## 1. Sequência exata e domínio

As hipóteses s=Σsj, com sj aumentando valência em j≥0, garantem a estabilidade de F^n. Em C6, o núcleo da projeção para C5 é A6 e seu diferencial é s0. Isso fornece a sequência exata de complexos(3). A sobrejetividade usada é a de cochains por truncamento, não a de cohomologias.

As ordens finitas dos jatos são preservadas neste argumento: cada escolha envolve número finito de componentes de valência e aplicações dos sj necessários nessa ordem. Uma fronteira em C3 ou A4 já significa a existência de primitiva dentro do mesmo complexo natural, com seus coeficientes e finitude. Não se transforma uma primitiva meramente coordenada em natural por declaração.

A injetividade de d1 em E4 é consumida exatamente na categoria da geração080: espaço-forma Lorentziano fixado, dimensão quatro, orientação, K>0, κ≠0, matéria constante projetada e apenas escalares herdados inertes. A transferência não amplia essa categoria.

## 2. Remoção do líder e surjeção q

Para [b]∈K, a imagem em C3 é exata. Escolher e levantar sua primitiva, e subtrair sa, elimina as componentes até E3 sem mudar a classe em C5. Resta b4+b5. As componentes da equação de ciclo são s0b4=0 e s0b5+s1b4=0.

A segunda implica d1[b4]=0; a injetividade080 dá b4=s0v4. Subtrair sv4 em C5 deixa z5=b5−s1v4 e
s0z5=s0b5+s1s0v4=0.
A escolha não precisa ser canônica, uniforme na classe ou uma cisão linear.

A inclusão de A5 em C5 envia ciclos de s0 a ciclos de s, pois os demais termos ficam acima de E5. Se z5=s0v5, então z5=sv5 em C5. Assim q está bem definida em cohomologia. Sua imagem está em K e a remoção acima prova a sobrejetividade sobre K.

A fonte não confunde essa sobrejeção com injetividade: uma fronteira que começa abaixo de E5 pode identificar classes distintas de H³(A5,s0).

## 3. Conferência explícita do termo s2v4

Esse é o ponto de maior risco no levantamento seguinte. Depois de retirar componentes até E3, o resíduo E6 do representante b4+b5 sem termo E6 é
r6=s2b4+s1b5.

Substituindo b4=s0v4 e b5=z5+s1v4, obtém-se
r6=s1z5+(s2s0+s1²)v4
   =s1z5−s0(s2v4),
pela identidade s0s2+s1²+s2s0=0.

Portanto a alteração do resíduo é uma fronteira de s0, e não um termo que se possa apagar como zero. Em C6, subtrair o sv4 completo deixa z5−s2v4; escolher z5 como outro levantamento muda a componente E6 por s2v4 e conserva a classe da conexão. Isso confirma a precisão do §2 da fonte e fornece a fórmula explícita do sinal.

## 4. Identidade das imagens e critério de levantamento

Para um ciclo z5, o levantamento sem componente E6 satisfaz
δq[z5]=[(sz5)6]=[s1z5]=d1[z5].
Como im q=K, segue δ(K)=im d1. Não é preciso conhecer ker q, nem supor que q possua seção.

A classe particular T≤5 tem δ[T≤5]=[A6]. Todas as classes com a mesma imagem em H³(C3) são sua translação por K. A exatidão da sequência longa implica que alguma delas levanta a C6 se e somente se −[A6] pertence a δ(K), agora identificada com im d1.

Conferi também a construção em representantes. Se r6+s1z5=s0a6, então T≤5+z5−a6 é fechado em C6. Os termos sja6 com j≥1 estão acima de E6; o sinal menos cancela precisamente o resíduo escrito. Naturalidade e finitude de a6 são parte da igualdade de classes em H⁴(A6,s0), não um acréscimo não demonstrado.

## 5. Detector e limites

Lk anula fronteiras de s0 e por isso define ℓk sobre H⁴(A6,s0). Mudar z5 por s0v5 altera s1z5 por −s0s1v5, sem alterar ℓk d1. Logo a condição ℓk d1[z5]=+4k/z0 é bem definida. Ela é necessária para o cancelamento, mas não suficiente para igualdade das classes inteiras.

As espécies E5/ghost3 são h²C³ e h*C⁴, incluindo seus jatos. O detector079 anula a contribuição direta da segunda espécie; isso não prova seu fechamento isolado ou permite retirá-la de uma classe mista. A fonte mantém essa distinção.

Não são conclusões: o cálculo de H³(A5), a imagem efetiva de d1, o cancelamento de [A6], o levantamento a C7 ou a todas as ordens, Mittag-Leffler, convergência, QME, UV ou admissibilidade causal. A investigação081 permanece fora da entrega080.

[REAL — documental] Os pins e links foram conferidos, com fontes preservadas antes/depois. A contagem no recibo anexo é de verificações documentais e não de novos teoremas ou execuções aritméticas.
