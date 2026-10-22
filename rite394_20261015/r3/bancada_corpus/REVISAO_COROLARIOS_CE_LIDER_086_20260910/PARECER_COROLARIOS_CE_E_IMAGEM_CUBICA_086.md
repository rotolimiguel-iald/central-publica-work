# Parecer independente dos corolários CE e da imagem cúbica — 086

10/09/2026. Revisor: /root/prepare_integration_83. [DERIVED — revisão matemática escrita]. [REAL — pins e preservação documental medidos no recibo]. Sem CAS, Lean ou execução/importação de um.py.

**Parecer favorável no contrato explicitado; não identifiquei erro material.** A prova nova da raiz distingue corretamente três afirmações: H³ do complexo CE quadrático é zero; a classe de Pontryagin gera uma linha livre em H⁴ desse complexo; e a imagem dos grupos BRST truncados no alvo cúbico C₃ desaparece a partir de C₆. A terceira afirmação não anula os grupos BRST inteiros. A passagem à completação usa uma projeção de complexos, sem trocar cohomologia e limite inverso.

Li integralmente a [fonte dos corolários](<C:/IALD/Central de Patentes/Chatgpt/COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/COHOMOLOGIA_CE3_E_IMAGEM_CUBICA_ZERO_APOS_C6.md>) e seu [manifesto](<C:/IALD/Central de Patentes/Chatgpt/COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/MANIFESTO_COROLARIOS_CE_086.json>). Os antecedentes diretamente necessários foram confrontados com os pareceres indicados abaixo. A fonte examinada mede 11035 bytes; seu SHA-256 lido nesta emissão é 2a2c7d5a9d49dc00119ec33aa56f7c8197b748b65e270522199b884eea3bad38. O registro anexo contém todos os pins antes/depois.

## 1. A categoria precisa permanecer a mesma em cada seta

A referência é uma espaço-forma Lorentziana orientada de dimensão quatro, K>0 real FIXO e κ real não nulo, com sigma constante já projetado ao complexo métrico. Rher é uma álgebra real unital não nula, inerte e de ghost zero para esses operadores fixados. As peças são polinomiais de valência finita e têm finitos jatos por elemento. Não há tensores espectadores, coeficientes espaciais ativos ou inversos de dados dinâmicos.

Mcal é o quociente linear efetivo de invariantes de gauge pela imagem das EOM e de todos os seus prolongamentos; N₂=Rher⊗Sym²Mcal. Não se troca esse quociente por uma torre de Weyl formalmente livre. A invariância é sob a isotropia h=so(1,3), e o diferencial CE envolve a álgebra inteira de Killing g. Não é permitida uma aplicação de Whitehead a g com base apenas na finitude local sob h.

O complexo empregado inclui ghosts p de translação e M de isotropia. Ele não é somente o subcomplexo horizontal relativo. Essa distinção torna a forma normal084 indispensável: uma primitiva geral pode ter componentes verticais antes da eliminação.

A [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) e seu [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md>) identificam a diagonal H^q(A_(q+2),s₀) com C^q(g,N₂)^h, incluindo o diferencial induzido por s₁. Portanto a passagem ghost 3/E5 → ghost 4/E6 usada aqui tem a tipagem correta. As correções s₀ dos jatos completos não são apagadas antes de passar à cohomologia.

## 2. A forma normal produz H³ CE=0 com primitiva ainda natural

Conferi o uso da [eliminação084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>), já acompanhada de [revisão específica](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_ISOTROPIA_084_20260910/PARECER_ELIMINACAO_FINITA_E_CANAL_EULER_084.md>). Para Q de ghost três cuja diferencial é horizontal, ela dá

    Q = q_V + f_tr CS_tr + f_E CS_E + dR,
    f_tr, f_E ∈ N₂^g,       d q_V = (div₀ V)ν.

A hipótese admite dQ=0. As duas primitivas intermediárias verticais e R são finitas e h-invariantes; não se está importando uma primitiva coordenada para a categoria natural por mera escolha de palavras. O canal Euler tem dCS_E=K²ν, enquanto o canal de traço é fechado.

A [nulidade085](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>), com [revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515/PARECER_KT_LINEAR_E_INVARIANTES_085.md>), elimina os dois coeficientes: N₂^g=0. O setor m=0 não entra nesse enunciado; nele constantes e classes Cartan não são anuladas por085.

Para um ciclo Q, resta Q=q_V+dR e (div₀V)ν=0. Multiplicar por ν é injetivo no módulo horizontal; no setor h-invariante, o coeficiente correspondente é o submódulo h-invariante de N₂. A nilpotência dos ghosts não cria um anulador de um coeficiente que não contém esses ghosts.

A [prova simbólica086](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>) e seu [parecer independente integral](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md>) dão injetividade da divergência neste espaço de vetores, não apenas inexistência de uma solução específica div V=J_W. Logo V=0 e Q=dR. A primitiva requerida já está na forma normal; não se necessita de uma escolha uniforme na ordem de jatos.

Assim H³ CE quadrático é zero. Em termos de d₁, o denominador correto é im[d₁:H²(A₄,s₀)→H³(A₅,s₀)]. Não é H³(s) inteiro, e tampouco o gate H3 de reconstrução do programa.

## 3. A comparação de graus é efetiva e resiste a nilpotentes

O símbolo086 usa a filtração pela SOMA das ordens nos dois fatores lineares. A estriteza das EOM e a injeção graduada no quociente plano entrelaçam a derivada principal. Não se usa a máxima ordem de apenas um fator nem uma suposta liberdade de toda a torre curva.

Para V≠0, seu maior grau efetivo é d≥5 e o termo principal de div₀V é não nulo no grau d+1. O alvo J_W tem símbolo não nulo no grau quatro. Os comutadores de conexão e K multiplicam ou produzem termos inferiores; não cancelam o símbolo efetivo selecionado. A finitude é essencial para a existência desse maior grau.

A extensão escalar é rigorosa também quando Rher tem divisores de zero ou nilpotentes. Se j é o símbolo real não nulo de J_W, a inclusão Rj→gr₄(Sym²Mcal) é cindível como aplicação de espaços vetoriais reais. Após tensorizar, λ⊗j=0 implica λ=0. De modo análogo, tensorizar os mapas reais injetivos da divergência mantém a injetividade. Não foi usado um ponto real de Spec Rher, que poderia apagar nilpotentes.

Se λ[J_Wν]=0, a forma normal e N₂^g=0 exigem div₀V=λJ_W. Para λ≠0, o segundo membro ainda tem grau efetivo quatro. Se V≠0, o primeiro tem grau pelo menos seis; se V=0, é zero. A contradição mostra λ=0.

Isto prova uma injeção Rher→H⁴ CE. Não prova que H⁴ CE tenha posto um nem que toda classe de ghost quatro seja proporcional a esse representante. K continua fixado como real não nulo; a prova não localiza silenciosamente um anel universal em K.

## 4. A conexão dos truncamentos foi usada na classe correta

A [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) e seu [parecer](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_TRANSFERENCIA_DELTA_080_20260910_045028_826573/PARECER_TRANSFERENCIA_DELTA_E5_080.md>) foram relidos para conferir a igualdade de imagens, que é mais forte que um teste de candidatos:

    Kcal = ker[H³(C₅) → H³(C₃)],
    δ(Kcal) = im[d₁:H³(A₅,s₀) → H⁴(A₆,s₀)].

A sequência 0→(A₆,s₀)→C₆→C₅→0 é exata em cochains por truncamento. O diferencial no núcleo é s₀ porque os s_j com j>0 passam de E6. A conexão δ é, portanto, bem definida e não é confundida com d₁ em todo H³(C₅).

A remoção das componentes baixas de uma classe em Kcal usa fronteiras já existentes no complexo natural finito. A injetividade de d₁ em E4 permite escrever b₄=s₀v₄ e trocar b₄+b₅ por z₅=b₅−s₁v₄ em C₅. Em C₆, o termo s₂v₄ não some: a diferença entre resíduos é −s₀(s₂v₄), pelo coeficiente E6 de s²=0. Por isso a conexão preserva a classe, e não necessariamente o representante. A inclusão q de ciclos de E5 é sobrejetiva sobre Kcal e δq=d₁; não se exige que q seja injetiva.

O resíduo da transgressão escolhida é (sT≤5)₆=A₆−s₀α₆. Usar [A₆], como faz a fonte086, é exatamente a passagem legítima para a conexão. Na diagonal quadrática, [A₆] corresponde a J_Wν. Seu fechamento CE vem da invariância orientada de J_Wν e da ausência de uma quinta translação independente em dimensão quatro.

## 5. O argumento decide todos os líderes cúbicos desse teste

A [revisão077 da primeira transição](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_PRIMEIROS_TRUNCAMENTOS_077_20260910_031524_472175/PARECER_TRUNCAMENTOS_E_SINAL_077.md>) consome a fonte junto com sua errata KT. Ela dá H³(C₃)=Rher⁴ e uma única linha na imagem desde C₄. A correção efetiva é s₀h*=+H₀h; não se transporta o sinal histórico errado para a identidade não linear. As contas líderes não empregam antifields nesses graus, mas a transferência posterior continua tratando suas fronteiras.

O ciclo T≤5 e seu [parecer independente da raiz077](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_077_20260910/PARECER_PONTRYAGIN_E_C5_077.md>) mostram que a linha alcança C₅. O líder α₃=tr(M Kpp♭)−tr(M³)/3 tem uma componente real −2xyz na restrição indicada. Esse coeficiente é unidade após extensão escalar real; portanto gera a linha inteira, não somente um ideal próprio de Rher. A imagem C₅→C₃ é Rher[α₃] pela fatorização através de C₄. Nada disso afirma que H³(C₅) inteiro seja unidimensional.

Se x∈H³(C₆), escreva y para sua imagem em H³(C₅). Sua imagem em C₃ é λ[α₃] e y−λ[T≤5]∈Kcal. A exatidão fornece

    0 = δy = λ[A₆] + δ(y−λ[T≤5]).

A transferência080 transforma a última parcela em uma imagem de d₁. Logo λ[A₆] é zero depois de tomar a cohomologia CE, com sinal irrelevante para a pertença à imagem. A injeção do §3 força λ=0. Esse passo usa TODA a liberdade Kcal, incluindo classes com antifields antes da redução, e não apenas a transgressão ou os detectores TT antigos.

Os três outros líderes já não alcançavam C₄; a linha restante alcançava C₅ e agora não alcança C₆. É correto dizer que a imagem em C₃ é zero desde C₆ nesta categoria. O resultado não diz que classes cujo primeiro termo está acima de E3 sejam exatas.

## 6. Completação: functorialidade suficiente, sem hipótese ML

Para todo N≥6, C_N→C₃ se fatora por C₆. O mesmo vale para a projeção do complexo completado por valência Ĉ→C₃. Aplicar H³ a essas composições basta para concluir imagem zero.

Não se intercambia H³ com lim, não se computa lim¹ e não se demonstra Mittag-Leffler para todos os outros alvos. A completação só é a previamente definida: cada coeficiente de valência conserva ordem finita de jatos. Um espaço ampliado que admita infinitas derivadas no coeficiente E5 ou E6 não está coberto pelo argumento de maior grau086.

## 7. Autoria dos antecedentes e limite desta revisão

A autoria desta revisão dos novos corolários é minha. Tenho autoria anterior no levantamento Pontryagin077, no certificado078 e na identificação082; isso não é uma aprovação independente desses antecedentes. O levantamento077 é consumido com o parecer da raiz077, e a identificação082 com o parecer independente de /root/finish_gibbs_realization. A igualdade de resíduos078 usada na composição é a identidade formal da transgressão já conferida; a presente conclusão de não exatidão CE usa a prova086 independente, sem depender de autovalidar meu detector antigo.

A emissão confere os pins diretos do manifesto086 e os arquivos efetivamente relacionados nesta revisão. Não reaudita recursivamente todos os arquivos, custódias ou execuções antigas. O helper histórico foi somente medido para confronto do pin; não foi executado nem apresentado como aprovado por esta revisão.

[DERIVED] A pergunta sobre outra correção que preserve o líder cúbico e permita alcançar C₆ foi resolvida negativamente NO CONTRATO FIXADO. Não precisa permanecer aberta nesse contrato. H³ CE quadrático também foi determinado.

[OPEN — fora do alcance] BRST total e suas classes de valência inicial maior, complexo físico com sigma não constante, admissibilidade Q2, anomalia quântica efetivamente calculada de ghost um, QME, UV, categorias com espectadores ou infinitos jatos, reconstrução geral pelos mesmos dados selecionados. A fase, o ramo e o H3 interno do programa não são invalidados por homonímia. Não há afirmação de gravidade quântica resolvida ou de integração destes corolários no canônico.

[REAL — documental] Somente arquivos novos desta pasta foram escritos. A fonte, seu manifesto, os antecedentes pinados e o helper histórico foram preservados antes/depois da emissão. Os controles do recibo são documentais; nenhuma nova execução matemática, CAS, Lean ou um.py ocorreu.
