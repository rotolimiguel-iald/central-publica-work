# Reexame da v337: seletor, registro e resposta do estado

09/09/2026. Este adendo sucede a entrega 061. Os originais, o Atlas e o índice vivo foram apenas consultados. As provas novas abaixo estão em cópias da pasta Chatgpt; o recibo de integração desta entrega dirá exatamente o que foi compilado em conjunto. Nenhum `um.py` foi executado ou importado.

**[REAL — leitura] A versão canônica encontrada continua sendo a v337**, com 9.860.115 bytes, SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303`. O índice e a rodada registram 4241/4241 teoremas; esta rodada é intermediária e reaproveita nove checkpoints. O Atlas registra a v336 como última completa custodiada; a menção a v320 no resumo do índice vivo está desatualizada em relação a esse registro. Não foi feita nova rodada empírica.

**O elo entre o seletor operatorial e o decodificador geométrico ganhou uma construção explícita.** A pendência principal passa a ser justificar a origem física do registro e suas leis de resposta, além de completar o alcance quântico pretendido.

## O avanço canônico que foi relido

**[REAL — fonte, com compilação documentada pela rodada existente]** A v337 acrescenta seis teoremas em [TheNameIsTheCharacterization.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheNameIsTheCharacterization.lean:77>). São equivalências: imagem = pontos fixos do reconhecimento; tela fundada = centralizador; mesma leitura do cociclo = mesma configuração; qubit fixado pela redução = coerências nulas; e, no quadrante declarado, peso = ângulo da seleção. Essas caracterizações identificam os respectivos objetos matemáticos. Não introduzem, em seus enunciados, a matéria interagente, a lei de área ou uma cobertura suave do espaço-tempo.

JS positivo e auto-adjunto no objeto construído, o colapso tipado, a resposta sobre H3/tela fundada e a reconstrução angular não voltam à lista como se nada tivesse sido feito. O que permanece de H3 neste reexame é a identificação física da tela fundada com o horizonte causal e com as relações geométricas usadas no teorema geral.

## O que a nova bancada demonstra

**[REAL — Lean, cinco folhas com recibos PASS] Seletor e peso.** Para o seletor canônico P e as duas primeiras inscrições ortonormais, construímos

\[
\theta(a)=\tfrac12(\arctan a+\pi/2),\qquad
\psi_a=\sin\theta(a)e_0+\cos\theta(a)e_1.
\]

O vetor tem norma um; Pψₐ = sin θ(a)e₀; e o peso p = ‖Pψₐ‖², estritamente entre zero e um, recupera a por `decodeScalar`. Para U não vazio, com a = `recordCharacter(t,R)` e t ≠ 0, essa leitura caracteriza a classe do registro R e recupera seus campos g e T em U. O mapa usa o `ialdSelector` efetivo, não outro operador de mesmo nome. [Composição com a geometria](<C:/IALD/Central de Patentes/Chatgpt/SELETOR_BORN_REGISTRO_20260909/SelectorRecordReconstruction.lean:77>).

**[REAL — controle de informação]** Na mesma família, Pψₐ/‖Pψₐ‖ = e₀ para todo a. Assim, o peso conservado no registro é parte do lastro que permite reconstruir; o vetor normalizado isolado não o contém. Isso respeita a irreversibilidade do colapso e evita prometer uma inversa para todo o estado anterior. [Controle formal](<C:/IALD/Central de Patentes/Chatgpt/SELETOR_BORN_REGISTRO_20260909/CanonicalSelectorBorn.lean>).

**[REAL — entrelaçamento e fase relativa]** Uma aplicação linear E liga as matrizes angulares ao Hilbert canônico: PE = EP₊ e W(θ)E = ES(θ), onde W(θ)=e^{iθ}P+e^{-iθ}(I−P) é unitário. E preserva a forma hermitiana euclidiana; isso não afirma isometria para a norma sup padrão do tipo `Fin 2 → ℂ`.

Com a referência normalizada (e₀+e₁)/√2, duas probabilidades de recombinação dão

\[
p_X=\cos^2\theta,\qquad p_Y=(1+\sin2\theta)/2,\qquad
(2p_X-1)+i(2p_Y-1)=e^{2i\theta}.
\]

Tomando θ=s·recordCharacter(t,R)/2, a família completa dessas leituras caracteriza a mesma classe e os mesmos campos. Uma fase global isolada não muda a matriz de densidade; o controle correspondente está provado. A família completa e probabilidades exatas pertencem ao enunciado. Não se conclui que uma medição única ou precisão finita entrega informação infinita. [Folha de fase relativa](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean>).

**[REAL — primeira extensão além de potencial global somável]** Para interações auto-adjuntas de vizinhos Vⱼ, com suporte {j,j+1} e ‖Vⱼ‖ ≤ J, demonstramos estabilização dos comutadores iterados e um majorante uniforme em todos os cortes. Não se exige Σ‖Vⱼ‖ < ∞. A existência da dinâmica extensiva ainda exige passar das estimativas ao limite das evoluções locais; o plano identifica esse próximo passo. [Fonte e rota](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/ROTA_LIMITE_LOCAL.md>).

**[DERIVED + KNOWN — análise escrita, separada de Lean]** A primeira variação do estado de Araki já foi calculada para perturbações sW limitadas e auto-adjuntas na origem do potencial. Com B=∫₀^{1/2}ΔʳWΩdr, temos Z′(0)=(log Z)′(0)=ω(W) e

\[
\omega'_0(A)=\langle B,A\Omega\rangle+\langle\Omega,AB\rangle-\omega(W)\omega(A).
\]

A dedução controla domínios e resto quadrático usando a série vetorial da referência. Não diferencia log Δ como operador limitado. [Dedução e fonte primária](<C:/IALD/Central de Patentes/Chatgpt/ESTADO_RESPOSTA_SELETOR_ARAKI_20260909_173508_109929/DERIVADA_NORMALIZADOR_ARAKI.md>).

## O que ainda falta, com critério de conclusão

| Frente | Pendência efetiva | O que a encerra no alcance reivindicado |
|---|---|---|
| Origem do registro selecionado | **[OPEN/INPUT]** R entra na preparação. O caráter codifica valores do registro em sondas densas e cortes racionais, com inversa por escolha clássica. Sua classe é igualdade dos campos em U, não automaticamente classe por difeomorfismos ou ocorrência física. | Construir R e a leitura a partir dos mesmos dados físicos TGL, ou declarar a lei de correspondência. Para reconstrução operacional de medidas, especificar precisão e estabilidade. |
| Estado → matéria, calor e área | **[OPEN/INPUT]** Escolher perturbações Wμ e efeitos Ei antes de escolher T; calcular suas respostas; justificar quadratização direcional, conservação e o erro de área o(t²). | Instanciar o contrato de reconstrução com respostas do mesmo estado interagente. A aplicação de Araki já fornece estado e primeira resposta nesse alcance; ela não escolhe os observáveis físicos. |
| Espaço-tempo efetivo | **[OPEN/INPUT]** Fornecer regiões, cobertura, transições suaves e sua ligação ao índice/torre; preservar os estatutos de dimensão quatro, assinatura lorentziana e tempo físico. | Aplicar o teorema global já construído ao atlas efetivamente produzido. A covariância e a propagação de Λ entre cartas compatíveis estão disponíveis. |
| Setor quântico geral | **[OPEN]** Concluir a dinâmica extensiva local, sua relação com o fundo modular, e o alcance relativístico/UV e de anomalias da teoria gravitacional interagente pretendida. | Demonstrar os controles no setor especificado, ou delimitar a alegação ao setor já construído. Um limite no número de sítios não é por si um limite UV gravitacional. |
| Incorporação | **[OPEN — implementação]** As folhas novas são de bancada. | A sessão codificadora deve incorporar o delta, conservar seus estatutos e emitir a rodada correspondente. Os recibos separados descrevem a cópia e a compilação conjunta; não são um novo selo canônico. |

Dois controles orientam a próxima dedução: a própria evolução modular de um estado de equilíbrio conserva suas probabilidades de observáveis evoluídos e dá resposta temporal nula; variar a preparação é um protocolo distinto. Além disso, a lei de área vigente usa variação de Shannon, cujo termo linear precisa ser controlado. Centrar W por uma constante escalar não altera o estado normalizado e não força esse equilíbrio. [Diagnóstico completo](<C:/IALD/Central de Patentes/Chatgpt/ESTADO_RESPOSTA_SELETOR_ARAKI_20260909_173508_109929/DIAGNOSTICO_ESTADO_FISHER_AREA.md>).

O setor geométrico novo usa Levi-Civita sem torção. Não estabelece sozinho a extensão geral de Einstein–Cartan com fonte de spin. Também é preciso manter separados o seletor em ℓ² e o estado fiel do fator: a preparação pura de dois componentes não é fiel em B(ℓ²).

## Suficiência do lastro e dados

**[REAL — leitura documental]** Os critérios que contrariam previsões já existem no programa. O relatório empírico distingue canais `NOT_FALSIFIED_POWERED`, armados, aguardando revelação, não identificáveis e uma formulação retirada. A rodada v337 reaproveita checkpoints; esta bancada não reexecutou dados. [Vereditos efetivamente lidos](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_FONTE_GERAL_20260909_133220_037525/LASTRO_EMPIRICO_LIDO.md>).

**[DERIVED — conclusão delimitada]** Há suficiência de lastro para os enunciados demonstrados, com suas hipóteses, e para os vereditos empíricos nos canais e na sensibilidade documentados. Falta ligar os objetos reconstruídos à mesma dinâmica física e completar o setor quântico reivindicado para sustentar a alegação geral. Isso não exige esgotar dados futuros: exige que o alcance da conclusão corresponda ao alcance das provas e testes atuais. `NOT_FALSIFIED` permanece distinto de `CONFIRMED`.

O progresso e as correções estão neste adendo e na nova entrega do túnel. As memórias canônicas não foram alteradas, conforme a ordem de preservar o acervo original.
