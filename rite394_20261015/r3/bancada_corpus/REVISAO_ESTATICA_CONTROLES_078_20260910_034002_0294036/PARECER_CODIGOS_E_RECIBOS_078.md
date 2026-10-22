# Revisão estática dos controles Einstein e Weyl078

10/09/2026. Autor: /root/finish_gibbs_realization. [DERIVED — análise independente dos códigos] [REAL — leitura dos recibos, contagens e pins]. Não executei nem importei os dois scripts, SymPy, Lean ou um.py. Todas as escritas desta revisão são novas e ficam em Chatgpt.

**Conclusão.** Não identifiquei erro material na implementação dos dois controles dentro do alcance declarado. Os códigos calculam, respectivamente, a Ricci e sua variação a partir das conexões e o traço de Weyl∧Weyl a partir de segundos jatos. Os recibos contêm 105 e 17 asserções verdadeiras, com nomes distintos dentro de cada lista, e seus pins de fonte coincidem com os códigos lidos. Os 122 registros não substituem a demonstração do mapa BRST ou a classificação de todas as classes.

Fontes examinadas integralmente:

- [Código Einstein linearizado](<C:/IALD/Central de Patentes/Chatgpt/compute_linear_einstein078_new.py>) e [recibo Einstein](<C:/IALD/Central de Patentes/Chatgpt/CONTROLE_EINSTEIN_LINEARIZADO_078_20260910/RESULTADO_EINSTEIN_LINEARIZADO_078.json>).
- [Código Weyl pontual](<C:/IALD/Central de Patentes/Chatgpt/compute_weyl_point078_new.py>) e [recibo Weyl](<C:/IALD/Central de Patentes/Chatgpt/CONTROLE_WEYL_PONTUAL_078_20260910/RESULTADO_WEYL_PONTUAL_078.json>).
- [Certificado matemático A₆](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>) e meu [parecer escrito independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RESIDUO_PONTRYAGIN_078_20260910_033403_7284198/PARECER_CERTIFICADO_A6_078.md>), preservados.

## 1. Código Einstein: cálculo efetivo da variação

O script fixa coords=[τ,x,y,z], η=diag(1,−1,−1,−1), g0=(ℓ/z)²η e h=(ℓ/z)²γ. A derivada do inverso é implementada por gi1=−gi0*h*gi0. Essa é a primeira variação de g⁻¹, não uma aproximação que mantenha o inverso congelado.

G0 usa a fórmula de Levi-Civita com o inverso de fundo. G1 soma os dois termos necessários: gi1 multiplicado por derivadas de g0 e gi0 multiplicado por derivadas de h. Como d1 deriva h inteiro, conserva as derivadas do fator a², além das derivadas de f. Essa parte não usa a fórmula conforme de Ricci empregada na prova escrita.

Ric0 é a contração primeira–terceira de ∂Γ+ΓΓ na convenção declarada. Ric1 contém a derivada das duas parcelas ∂Γ e as quatro parcelas de primeira variação dos dois produtos ΓΓ. Os índices internos são contraídos na mesma ordem da fonte. Não encontrei omissão de gi1, fator conforme ou uma das parcelas cruzadas.

O tensor res é calculado como Ric1−Λh. O tensor expected, com ODE/2 no bloco xy, é produzido separadamente e comparado com res componente a componente; res não é definido pelo resultado esperado. O script mantém f(z) simbólico arbitrário nessa comparação. Assim o cálculo verifica que o resíduo inteiro é proporcional à EDO, antes de escolher suas soluções.

Os demais controles correspondem às afirmações listadas: traço e divergência planos de γ; duas soluções elementares da EDO; Wronskiano k³z²; derivadas de Lie completas das quatro Killing; valores delas em p. A contagem recomposta é 16+16+1+4+2+1+64+1=105.

z é declarado real no sistema simbólico, e as fórmulas racionais envolvem 1/z. A interpretação geométrica do recibo restringe z>0, portanto não usa a expressão em seu polo. k é real não nulo; ℓ e z0 são positivos. Não há amostragem numérica que substitua as identidades simbólicas.

O código não calcula a mistura sigma explicitamente nem todos os prolongamentos infinitos. No fundo φ0 constante, a anulação dessa mistura e o prolongamento das identidades de funções são passos da prova escrita e do parecer anterior. O limite do recibo conserva essa distinção.

## 2. Código Weyl: jatos, contrações e produtos exteriores

setd insere os jatos γ11,zz=u, γ22,zz=−u e γ12,τz=v, com simetria tanto nos índices métricos quanto nos índices de derivação. Todos os outros segundos jatos são zero. Isso coincide com os jatos relevantes da solução no ponto escolhido; primeiras derivadas não são necessárias ao Riemann linearizado em η.

A expressão R(a,b,c,d) tem os quatro termos e o fator exato 1/2 da curvatura linearizada. Ric contrai os índices primeiro e terceiro com a assinatura; o escalar é a contração de Ric. P=(Ric−Rη/6)/2 é precisamente o Schouten em quatro dimensões. W subtrai o produto métrico–Schouten com os quatro sinais pertinentes.

As 16 asserções de traço conferem a contração de Weyl. A última asserção compara o produto exterior calculado a −2uv. Não se infere que essas 17 verificações sejam 17 teoremas independentes sobre um Riemann arbitrário; são asserções do controle pontual especificado.

No produto exterior, os pares (c,d) e (e,f) são enumerados com c<d e e<f. Os coeficientes de uma 2-forma ½W_cd dx^c∧dx^d já são W_cd nesses pares ordenados, logo não cabe um fator 1/4 extra. As tuplas com índices repetidos são descartadas; a paridade do número de inversões fornece exatamente o sinal da orientação 0123. A soma em a,b, com os dois fatores de assinatura, é tr(W^a_b∧W^b_a). Portanto os pares matriciais e os fatores de 2 são contados corretamente.

O resultado −2uv, com u=2/z0 e v=k, dá −4k/z0, em acordo com os quatro produtos de formas conferidos manualmente no parecer anterior. A substituição u=2/z0,v=k aparece como descrição no recibo; sua aritmética é imediata e foi conferida aqui. O script pontual não calcula a EDO, as Killing ou o mapa de todos os jatos, e seu campo limits o diz expressamente.

## 3. Recibos e precisão de custódia

Li os dois JSON e contei suas listas, sem executar seus códigos. São 105/105 e 17/17 entradas com passed=true; os campos checks_total coincidem com as contagens, e não há repetição de nomes dentro de cada recibo. As duas referências source têm tamanho e SHA-256 iguais aos códigos atuais, medidos nesta revisão.

Os dois scripts criam diretórios de saída novos com exist_ok=False, gravam um temporário com abertura exclusiva, verificam seus bytes e o renomeiam. As falhas nas asserções impedem a emissão normal de um recibo PASS. Não encontrei no código leitura/importação de um.py ou execução de arquivos do acervo. A revisão não reproduz o ambiente SymPy: a versão1.14.0 é a versão registrada pelo recibo Einstein, não uma importação feita aqui.

Há uma precisão de custódia no código Einstein: a variável before dos inputs é preenchida **depois** dos cálculos simbólicos, imediatamente antes da construção do recibo. Sua comparação com a segunda leitura prova igualdade nesse intervalo de emissão; não prova, por si, estabilidade da nota durante todo o tempo desde o início do cálculo. O código não usa o conteúdo da nota como entrada do cálculo simbólico, mas a referencia documentalmente. Os pins atuais coincidem com o recibo. Essa limitação não é uma falha de Einstein, Weyl ou da prova escrita.

Nesta revisão, as seis fontes foram medidas antes e depois da escrita do parecer. O manifesto registra a igualdade, as contagens documentais e os pins reais. Isso não autentica uma transcrição completa do processo de execução, nem amplia o que cada recibo efetivamente mede.

## 4. Alcance final

[DERIVED] A implementação estática é consistente com as identidades que pretende verificar, e fornece um caminho de cálculo de Ricci independente da fórmula conforme da prova escrita. [REAL] Os recibos e os códigos lidos têm contagens e pins compatíveis, sem rerun.

O certificado de não-exatidão continua dependendo da solução em uma vizinhança, da avaliação do BRST linear mínimo e do argumento de obstrução da classe específica de C₅. Esses passos constam da nota matemática e foram revisados separadamente. Os controles não eliminam outras escolhas com o mesmo líder cúbico, não calculam lim¹/ML do modelo e não constituem QME, prova Lean ou fechamento UV. A entrega077 e todos os originais permanecem intactos.
