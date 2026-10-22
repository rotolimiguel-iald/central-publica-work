# Parecer independente dos primeiros truncamentos BRST — 077

10/09/2026. [DERIVED — revisão matemática escrita]. **Parecer favorável ao conjunto da nota com o adendo obrigatório de sinal.** Foi detectada uma incompatibilidade na atribuição Hamiltoniana da equação(3) original; o autor a corrigiu em arquivo separado, sem reescrever a fonte. Não encontrei outro erro material nas contagens e nos mapas examinados.

Li integralmente [S0_KILLING_E_PRIMEIRA_TRANSICAO.md](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>), seu manifesto e o [ADENDO_SINAL_KOSZUL_TATE_077.md](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>), também com manifesto. Pins lidos antes da gravação:
- nota: 16971 bytes, SHA-256 d97945de866937f2b8b141bab33a8f0647b54f2e951a7ccb6b3448064e17ea52;
- adendo: 5559 bytes, SHA-256 e85b3f29db7dc2c80d28bda6de75e2498e504e7ee3b1ef0f265afb6aff2b6112.

O recibo separa custódia documental de demonstração escrita. Não houve CAS/Lean, execução/importação de um.py ou inclusão desta revisão na entrega076.

## 1. Correção efetiva do complexo linear

Para o quadrático escrito S₂=½⟨u,H₀u⟩+⟨u*,R₀c⟩, com a fonte ímpar à esquerda, a convenção de069 e do levantamento Killing076 dá

\[
 s_0u=R_0c,\qquad s_0c=0,\qquad
 s_0u^*=+H_0u,\qquad s_0c^*=+R_0^\dagger u^*.
\]

A derivada direita do termo u*R₀c em u* é −R₀c, enquanto a derivada em u é H₀u. Variar c e integrar por partes já deixa a variação à direita e dá +R₀†u*. A verificação é a da [convenção explícita Killing076, seção2](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/LEVANTAMENTO_BRST_CORRENTES_KILLING_076.md>) e dos sinais nos geradores da [equação140 de Fröb](https://arxiv.org/pdf/1803.10235v3).

Portanto o sinal −H₀u da nota original não era o daquela ação na convenção citada. O adendo reconhece e corrige precisamente isso. O mapa u* antigo↦−u* corrigido e c* antigo↦−c* corrigido, fixando u,c, entrelaça os dois complexos LINEARES. Não é apresentado como transformação canônica que preserve simultaneamente ação e antibracket, nem como transporte já provado do diferencial não linear inteiro.

Conferi também R₀c=(2∇̄_(μc_ν),c·dφ₀) e o adjunto densitizado R₀†(π,p)=−2∇̄·π+p·dφ₀. H₀R₀=R₀†H₀=0 no fundo on-shell garante a nilpotência corrigida. Nenhuma inversa de H₀ ou propriedade normalmente hiperbólica do operador sem gauge é utilizada.

## 2. Quociente de Killing e dependência da referência

No espaço linear de jatos, as únicas fronteiras de ghost1 são os prolongamentos de R₀c provenientes dos campos de ghost0. Os graus dos antifields impedem novas fronteiras lineares nesse grau. Por isso W=V_c/span(jatos de R₀c) está corretamente identificado; seu dual formal satisfaz a equação de Killing e v·dφ₀=0 com todos os prolongamentos.

Conferi a anulação de W na região genérica indicada, condicionada à prolongabilidade estacionária já citada em070. As quatro covariáveis independentes dφ₀¹,dφ₀²,dφ₀³,dQ₀ forçam v(p)=0. A derivada da equação material força a imagem de ∇v a caber no núcleo unidimensional de dφ₀. Como g₀∇v é antissimétrica, seu posto é par; posto≤1 implica zero. A identidade de prolongamento de Killing determina então todos os jatos restantes. Não se divide pelo determinante para fabricar um coeficiente universal. A construção e a prolongabilidade dos jatos estacionários de070 são entradas desta passagem, não uma nova auditoria integral de KT aqui.

Para φ₀ constante e curvatura seccional K=Λ/3≠0, a matéria não impõe relação linear no ghost. Os valores p=c e m=∇̄_[a c_b] somam quatro mais seis dados; a identidade de Killing determina os derivados seguintes. A realização da quádrica ambiente produz dez soluções independentes, de modo que dim W=10, não só uma cota superior. Sob a isotropia Lorentz, W≅V⊕Λ²V (ou o dual identificado pela métrica).

Isto é estabilizador de uma referência, não reducibilidade universal. O salto entre as duas fibras não contradiz a ausência de parâmetro universal070. Também não constrói uma representação Hadamard/BRST física na referência simétrica: o teste aqui é do complexo mínimo LOCAL de jatos.

## 3. Contagens invariantes 0,4,3

Recalculei as decomposições com V_C=(½,½) e H_C=Λ²V_C=(1,0)⊕(0,1). Temos

\[
 \Lambda^2H=(1,0)\oplus(0,1)\oplus(1,1),\quad
 \Lambda^3H=2(0,0)\oplus2(1,1).
\]

Na decomposição de Λ^q(V⊕H), os únicos escalares relevantes são:

| q | Origem dos escalares | Dimensão |
|---|---|---:|
| 2 | nenhuma | 0 |
| 3 | dois em Λ²V⊗H e dois em Λ³H | 4 |
| 4 | um em Λ⁴V e dois em Λ²V⊗Λ²H | 3 |

A orientação de espaço-tempo é necessária aos representantes com ε; exigir também reflexões mudaria a categoria. O alvo não fornece índices Lorentz adicionais na referência constante. A contagem é na fibra com Λ e φ₀ fixados; multiplicidades funcionais de coeficientes de referência não são indevidamente contadas como novas dimensões nessa fibra.

As duas cúbicas de m e os emparelhamentos mpp e εmpp são representáveis por expressões naturais. Multiplicar os dois últimos por Λ≠0 iguala o peso de engenharia, sem alterar a dimensão ou introduzir inverso de um gradiente. Não se confundem esses geradores da álgebra de Killing com ghosts Lorentz independentes do modelo métrico.

## 4. C₃, C₄ e a condição exata de levantamento

Em ghost3/valência≤3 existem só cúbicas de ghosts. As fronteiras vêm de duas espécies: s(c²) e s₀(u c²). A segunda impõe o ideal R₀c; a primeira desce ao CE da álgebra de Killing. Qualquer elemento finito do ideal tem preimagem finita nos jatos de u. Tomar invariantes após esse quociente é permitido pelos tipos Lorentz finitos.

Como (Λ²W)^G=0, o denominador CE natural nesse primeiro quociente é zero. Segue dim H³(C₃)=4.

Um levantamento para C₄ acrescenta um termo u c³. Seu diferencial linear pode cancelar exatamente a parcela no ideal R₀c, e nenhuma outra espécie de correção cabe nesses graus. Logo a condição é d_CEα=0 em Λ⁴W, tanto necessária quanto suficiente. A suficiência não é uma hipótese escondida: vem da preimagem finita no ideal e da projeção no tipo trivial, que conserva a igualdade.

A complexificação da álgebra de Killing é so(5,C), com geradores CE primitivos de graus3 e7. Conferi essa importação finita em [BBH1995, seção7.1 e Apêndice B](https://arxiv.org/pdf/hep-th/9505173v2). Assim H³_CE tem dimensão1. A isotropia age trivialmente por Cartan e tomar invariantes é exato; como não há fronteira invariante de grau2, o núcleo de d_CE no espaço invariante de grau3 tem dimensão1.

Portanto a imagem de H³(C₄)→H³(C₃) tem dimensão1. O mapa de grau3 para grau4 tem posto4−1=3 e preenche os três invariantes de Λ⁴W. Como C₄⁴ tem só quatro ghosts e as fronteiras são s(c³) e s₀(u c³), segue H⁴(C₄)=0 na mesma fibra/categoria.

A correção de sinal KT não altera nada nesses passos: um antifield físico de ghost−1 exige três ghosts para chegar a ghost2, valência total4, e quatro para chegar a ghost3, valência5. O antifield de ghost exige ainda mais. Assim os segmentos usados no cálculo não empregam H₀ nem o sinal corrigido. Isso não autoriza ignorá-los nas próximas valências.

Os controles85 e126 também conferem como dimensões COORDENADAS nessa fibra: rank d₂=45−10=35 e rank d₃=120−(35+1)=84. Não são os grupos naturais principais, nem dimensões de um espaço acrescido de funções arbitrárias de x como coeficientes independentes.

## 5. A conclusão universal é uma obstrução de levantamento regular

Os quatro polinômios em p=c e m=∇̄_[a c_b], com contrações por g₀/ε e Λ, existem antes da especialização da referência. Por sc quadrático e sB₀=0, são ciclos universais em C₃. Sua restrição ao teste dá a base de quatro classes já calculada.

A restrição à referência on-shell preserva o diferencial mínimo e a valência. Se as quatro classes universais levantassem regularmente, suas imagens também levantariam no teste, contradizendo a imagem de dimensão1. De fato, o subespaço de combinações constantes desses quatro controles que admite levantamento universal tem dimensão no máximo1.

A prova não necessita que toda classe da fibra se estenda universalmente: os quatro representantes usados foram explicitamente estendidos. Tampouco identifica a cohomologia universal com a fibra. É essencial manter a cláusula da fonte: categoria regular que ADMITE esse teste local. Uma classe definida apenas onde dφ₀ tem determinado posto, ou uma família quântica restrita por outras hipóteses, requer sua própria comparação; não se a inclui por nome.

## 6. Limites e resultado da revisão

[DERIVED] O conjunto nota+adendo paga a formulação correta de s₀, o salto do quociente de Killing, as dimensões naturais0/4/3, as contagens H³(C₃)=4, imagem desde C₄ de dimensão1 e H⁴(C₄)=0 na referência declarada, além da obstrução à sobrejetividade universal na classe regular que contém o teste.

[OPEN] A falha de uma transição inicial não implica lim¹≠0. Há uma precisão ainda mais forte nesse alvo FIXO: as imagens H³(C_M)→H³(C₃) formam uma cadeia decrescente de subespaços de um espaço de dimensão4 e, portanto, estabilizam eventualmente. Isso não demonstra estabilização para todos os N. Corte por valência não é corte na ordem dos jatos, e os demais grupos das truncagens não foram provados finitos.

O núcleo CE de dimensão1 não foi levantado a todas as ordens; nenhuma classe sobrevivente do BRST completo é extraída disso. Permanecem cohomologia completada, canais com coeficientes, anomalia, corrente/carga interagentes, QME e UV. Não se afirmou anomalia não nula nem falsificação da teoria.

[REAL — documental] A fonte original conserva sua errata registrada, e o adendo corrige ao lado. Para consumir o resultado é necessário transportar ambos. Os pins dos manifestos foram comparados a bytes relidos e as entradas foram preservadas durante a gravação deste parecer. A revisão não modifica076, não recaptura canônicos e não executa/importa um.py, Lean ou CAS.
