# Reexame após a v337 — interação geral limitada, Araki e atlas suave

09/09/2026. **[REAL — leitura]** O `um.py` canônico disponível nesta consulta continua sendo a v337: 9.860.115 bytes, SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303`. A nova bancada é um delta sobre essa base, ainda sujeito à incorporação pela sessão que mantém o programa. Este documento sucede as pendências da entrega 060; não reescreve o histórico.

**O caminho crítico diminuiu.** A existência do estado perturbado na classe construída deixa de ser uma falta matemática: há uma aplicação justificada de Araki, com normalização e identificação do cociclo. A transformação finita de Einstein agora alimenta um teorema efetivo de colagem entre cartas suavemente compatíveis. A construção quântica passou da família XX para uma classe local somável que admite termos não comutativos.

## O que foi pago

**[REAL — fontes e compilações da bancada] Interação local sem hipótese de comutação.** O contrato recebe V_j auto-adjunto, suporte no andar j+1 e Σ‖V_j‖ < ∞. A soma V pertence ao fator canônico; seu cociclo é construído como limite em norma dos cortes, com controle da cauda. Unitariedade, lei torcida, derivada em norma e dinâmica efetiva continuam demonstradas para qualquer `SiteProfile`. A testemunha X₀X₁ e Z₁Z₂ tem comutador −2iX₀Y₁Z₂ ≠ 0, e o cociclo do potencial total não é identicamente I. [Lote e recibos](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/MANIFESTO_INTERACAO_GERAL.json>).

**[REAL — unicidade formal] O potencial determina o cociclo.** Provaram-se V_c=V_d ⇔ u_c=u_d e, consequentemente, mesma dinâmica quando o potencial é o mesmo. A prova diferencia u·v*, usa o gerador anti-auto-adjunto e cancela a unidade. A decomposição em termos locais não acrescenta uma escolha à dinâmica resultante. Não se inverte a conclusão sobre dinâmicas: deslocamentos centrais podem ser invisíveis à conjugação. [Prova aplicada](<C:/IALD/Central de Patentes/Chatgpt/ESTADO_ARAKI_20260909/LocalInteractionUniqueness.lean>).

**[DERIVED + KNOWN] Estado fiel normal e identificação modular/KMS.** Para o par canônico (M,Ω), já cíclico e separante, e o mesmo V construído, a aplicação da perturbação limitada de Araki fornece

\[
\Phi_V=e^{(\log\Delta+V)/2}\Omega,\quad
Z_V=\|\Phi_V\|^2>0,\quad
\omega_V(A)=\langle\Phi_V,A\Phi_V\rangle/Z_V.
\]

A continuidade em norma da órbita de V permite aplicar a unicidade formal ao expansional da referência. Seu cociclo coincide com o limite construído; o cociclo do estado normalizado é Z_V^{−it}u_V(t). **[REAL]** A fase central foi formalizada: preserva a dinâmica e desloca o gerador para i(V−log Z_V·I). O domínio da exponencial e KMS vêm do resultado analítico importado, com os sinais conferidos, não de uma definição ou de mera invariância do estado. [Dedução completa](<C:/IALD/Central de Patentes/Chatgpt/ESTADO_ARAKI_20260909/DEDUCAO_ESTADO_PERTURBADO_ARAKI.md>) · [Revisão independente final](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_FINAL_ARAKI_20260909_170730_304080/PARECER_FINAL_ARAKI.md>) · [Araki, fonte primária](https://ems.press/journals/prims/articles/2638).

**[REAL — teorema global condicional] Colagem por transições suaves reais.** `SmoothRecordTransition` exige que a transição represente o mesmo ponto do espaço e que métrica e matéria sejam compatíveis no aberto. A transformação do tensor de Einstein é deduzida dessas condições; não é mais um campo independente do contrato novo. Em um espaço conexo coberto por cartas admissíveis, as equações locais produzem uma única constante Λ global, inclusive nos registros decodificados pelo caráter. [Teorema de colagem selecionada](<C:/IALD/Central de Patentes/Chatgpt/COLAGEM_SUAVE_REAL_20260909_164537_702751/SmoothSelectedAtlasGluing.lean:150>).

## Pendências atuais, com o alcance explícito

| Frente | O que permanece | Critério concreto para avançar |
|---|---|---|
| Seleção → registro geométrico | **[OPEN/INPUT]** Identificar o caráter completo do decodificador com a saída do seletor operatorial e com a leitura física pretendida. O caráter é construído a partir de registros geométricos admissíveis; sua inversa já recupera esses registros. | Dar o mapa entre os mesmos objetos, demonstrar sua compatibilidade com o reconhecimento e dizer quais correspondências entram como postulados. Se houver pretensão de recuperação operacional com dados medidos, fornecer também o alcance de precisão e estabilidade. |
| Estado/interação → matéria e área | **[OPEN/INPUT]** Instanciar T, conservação e a relação entre calor e área induzida das telas usando os mesmos dados selecionados/interagentes. O erro de área o(t²) continua hipótese do resultado geral. | Construir essas respostas e provar as hipóteses no domínio reivindicado, ou declará-las expressamente como leis de correspondência. Dimensão quatro, assinatura lorentziana, região–andar e tempo modular–tempo físico conservam seus estatutos. |
| Geometria global efetiva | **[OPEN/INPUT]** Fornecer o espaço, a cobertura e as transições suaves compatíveis para os registros efetivamente selecionados. | Instanciar `selected_connected_smooth_atlas_einstein`. A lei de transformação de Einstein e a propagação de Λ já são resultados utilizáveis. |
| Alcance quântico reivindicado | **[OPEN]** Ultrapassar, quando exigido pelo alcance físico, a soma global de normas finita; tratar interações extensivas/não limitadas, anomalias e a rota relativística/UV. | Construir o setor especificado e provar os controles correspondentes. O limite em número de sítios com V limitado não estabelece sozinho o limite ultravioleta de uma teoria de campos gravitacional. |
| Incorporação e formalização | **[OPEN — implementação]** Levar as novas folhas e a aplicação tipada de Araki ao programa e à sua rodada. **[OPEN — formalização interna]** O construtor analítico/KMS ainda não foi reproduzido integralmente em Lean. | Incorporar o delta com seus recibos e rotular a aplicação como DERIVED + KNOWN. Uma exigência de prova inteiramente interna ao kernel acrescentaria a tarefa de formalizar a análise importada; não é requisito para a aplicação matemática documentada. |

As hipóteses geométricas não constituem defeito de um teorema condicional. Elas delimitam a frase que esse teorema sustenta. O passo pendente é mostrar que o modelo físico pretendido fornece essas hipóteses, ou assumi-las abertamente e declarar a suficiência condicionada a elas.

O novo lote geométrico usa Levi-Civita sem torção. Não deve ser apresentado como uma extensão geral de Einstein–Cartan com matéria de spin apenas por homonímia com a ponte do artigo; o escopo de eventuais resultados canônicos de Cartan deve ser acompanhado separadamente.

## O que não deve voltar à lista por desatualização

**[REAL/INPUT, conforme a fonte]** JS positivo e auto-adjunto, a identificação da raiz no objeto formal construído, a resposta do operador sobre H3/tela fundada, a injetividade da leitura e a reconstrução angular já têm seus resultados. As versões v336–v337 acrescentam verificação por identidade e caracterizações por equivalência. A [v337](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheNameIsTheCharacterization.lean:77>) foi relida: essas equivalências identificam seus referentes matemáticos; não trazem, no mesmo enunciado, as hipóteses de área, matéria e transições suaves acima.

Os critérios capazes de contrariar a previsão já estão no programa, inclusive o mapa gerado em [um.py](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py:158368>). Não é necessário criá-los novamente. Este reexame não executou os ritos. A leitura documental anterior distingue canais `NOT_FALSIFIED_POWERED`, armados, aguardando revelação, não identificáveis e uma formulação retirada. [Lastro empírico efetivamente lido](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_FONTE_GERAL_20260909_133220_037525/LASTRO_EMPIRICO_LIDO.md>).

**[DERIVED — suficiência delimitada]** Há lastro suficiente para os enunciados formais demonstrados e para a aplicação matemática importada, sob suas hipóteses explícitas. Os canais empíricos sustentam os vereditos registrados no seu alcance. Nenhum desses pontos exige esperar todos os dados futuros; também não autoriza concluir que todo o alcance físico de gravidade quântica foi estabelecido. `NOT_FALSIFIED` continua distinto de `CONFIRMED`.

## Custódia deste reexame

As nove novas fontes têm recibos individuais PASS e revisão semântica independente. A aplicação Araki permanece separada do escopo formal do lote. A cópia integrada e a compilação conjunta são descritas no recibo consolidado que acompanha esta entrega; este texto não substitui esse recibo nem afirma execução do programa.

Nenhum `um.py` foi executado ou importado. Originais, Atlas, índice e memórias canônicas permanecem em leitura. O progresso está registrado em novos documentos da pasta Chatgpt e será apontado pela nova entrega no túnel.
