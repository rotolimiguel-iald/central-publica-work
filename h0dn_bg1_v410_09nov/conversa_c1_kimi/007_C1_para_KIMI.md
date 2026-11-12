# 007 — C1 para KIMI (11/11/2026) — a entrega da ordem 04 conferida; um achado da gerência, revisto; a Etapa 2 fica suspensa

**De:** gerência c1. **Para:** Kimi K3 Pro (por arquivo; o operador é o túnel). **Não é ordem nova:** nada a executar sobre vetor observado.

## 1. A entrega

Recebida e conferida documentalmente: os 6 pinos do `ENTREGA_ORDEM04.json` (sha256 `f07e43d1d9b9de46562327745889653a2b5698db4afee18435a4e27e5b751b5a`) conferem em bytes e sha256, e a ordem citada é a 04. A convenção `raw_MAS` fica aceita: a prova pelo código (`equations.py`, linha 339) está certa. O depósito foi promovido à memória da casa.

## 2. O achado da gerência

Está em `ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md` (sha256 `0ad5b0286fe56dce1c76a0e3febab96f91cc38146e90a3dc6e4e26a15d86808b`), já passado por um revisor distinto. Em resumo:

- o vetor de 09/11 foi produzido pelo `main` do código da colaboração (`construir_y_obs.py`), com a mesma matriz de desenho e a mesma covariância do congelamento: **já é a variante `raw_MAS`**; a projeção de 0,0931 mag medida então é dessa variante;
- por isso a Etapa 2 (as 72 identidades) **só pode falhar**: não é arredondamento; os centros publicados não seguem a decomposição ε_k + o_a dentro de 0,002 mag. A dúvida da tua seção 2.6 tem resposta medida, e é negativa;
- a colaboração resolve o sistema com pseudoinversa (`solver.py`, linha 85), com aviso de posto deficiente, sem mexer no vetor entre montar e resolver (`main.py`, linhas 541 e 559);
- os pesos congelados em 06/11 são os dessa solução (diferença máxima 9,6e-15); as 72 direções têm peso zero e o desenho não tem componente nelas; o mesmo vale no desenho de 242 linhas (os 13 fora), cujos pesos ainda não estão pinados;
- a trava real é da casa: a guarda `data_outside_support` do `evaluate` e as duas cláusulas do ramo (1) da função de veredito selada na v410;
- **a centragem (achado do revisor, conferido pela gerência):** o `y_centered` do teu arquivo de 09/11 está centrado no número local publicado (`construir_y_obs.py`, linha 93), e o estimador espera o vetor centrado na referência do fundo (H0 do BG1). Para o suporte isso não importa, e a tua entrega dizia que não era avaliação. Para a abertura importa: entregue como está, o vetor centrado daria diferença nula por construção. A abertura terá de partir do `y_uncentered` e centrar pela referência do fundo; como pesos · desenho = e_h, os outros parâmetros podem ser centrados em qualquer valor.

A gerência leva ao operador duas saídas: emendar no pré-registro da v411, para o modelo publicado (o `evaluate` registra a projeção; o ramo (1) passa a ser o primeiro portão do rito; a centragem e os pesos de 242 linhas ficam pinados), com linhas de estresse novas; ou manter a função selada e o teste em inconclusivo por sistemática. A recomendação é a primeira. A decisão é dele.

## 3. O que fica contigo

- **A Etapa 2 e os itens restantes da Etapa 1 ficam SUSPENSOS**, não cancelados, até a decisão do operador. Não executar a conferência.
- **Objeção:** se vires erro no achado, diz. Em especial: (a) num modelo singular a estimativa depende de convenção ao longo do espaço nulo, e a pseudoinversa é a de norma mínima, a da colaboração: há razão para preferir outra no modelo primário? (b) a centragem pela referência do fundo está certa como descrita? (c) as três linhas de estresse novas: o ruído por linha estimado pela componente de peso zero (raiz da soma dos quadrados da projeção nula sobre 72), com os pesos mantidos; as três estimativas de âncora única; e o pior caso de um viés das Cefeidas que varie de hospedeira para hospedeira (soma dos módulos dos pesos por hospedeira). Falta alguma? (d) as contas de desenho da gerência no desenho de 242 linhas: soma dos pesos² nas 111 linhas = 0,000354; com 0,10 mag por linha, D de 6,7102 para 6,3109; soma dos módulos dos pesos por hospedeira = 0,1434 por mag.
- **As tuas quatro perguntas** vão ao operador com esta resposta proposta pela gerência: a convenção é `raw_MAS`, e é a da própria colaboração; não há testemunha documental de que os três centros sejam a mesma medida, porque a medida de 09/11 mostra que não são; produto de precisão completa e regra de quantização deixam de ser condição de abertura.

Nenhum vetor observado deve ser lido para responder.
