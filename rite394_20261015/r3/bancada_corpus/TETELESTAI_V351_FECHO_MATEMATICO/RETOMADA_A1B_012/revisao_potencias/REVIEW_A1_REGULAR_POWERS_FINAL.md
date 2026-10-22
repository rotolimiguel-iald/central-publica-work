# Revisão independente — potências do gerador regular existente

2026-09-14T19:58:07.113285-03:00

**A1_REGULAR_POWERS_REVIEW_ACCEPTED__AFFILIATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 4 declarações (4 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] A fonte inteira e a ficha foram confrontadas com resolventImaginaryPower, seu lema de amortecimento e seu transporte por entrelaçamento, já reproduzidos. O delta contém quatro teoremas e nenhuma definição: não substitui o grupo de potências por uma definição igual a regularUnitary.

[REAL] O cálculo log((1−sigmoid a)/sigmoid a)=−a dá a fase de sinal negativo. Com a convenção characterPhase(s,ξ)=exp(−i s ξ), modularPhase(t,−2πξ) é precisamente characterPhase(2πt,ξ). O controle de tempo oposto testa essa distinção.

[REAL] sigmoidMultiplier_imaginaryPower exige explicitamente T igual ao multiplicador, positividade, T≤1 e injetividade de T e 1−T. No teorema final essas condições são provadas para o multiplicador e para regularSpectralResolvent; hT é descarregada por rfl. A igualdade é primeiro estabelecida na imagem densa do amortecimento T(1−T), usando CFC pontual e somente eventos AE finitos, e estendida pela continuidade dos operadores limitados. Não se inverte o amortecimento como operador limitado.

[REAL] V=W·Fourier⁻¹ é a coordenada existente. Fourier/shift e W·shift·W*=regularUnitary dão V·character=regularUnitary·V. O entrelaçamento R·V=V·M e resolventImaginaryPower_intertwines transportam as potências para o mesmo R. O resultado final vale para todo SiteProfile, t e vetor, sem antecedente adicional de identificação.

[REAL] regularPositiveGenerator continua sendo o grafo resolvente de R=(1+h)⁻¹, com identificação exponencial já aceita separadamente. Neste sentido preciso, o teorema identifica as potências construídas por esse resolvente com a família regular inteira. Não identifica h com o operador modular do peso, nem troca a ação esquerda regular por um implementador GNS por homonímia.

[REAL] Execução própria rc0 em 37.91 s. 644 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularImaginaryPowers | `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a` | `392ec0633d892ed00901a5b5ac2d6c4b6e1a10a8d5093fb324b9622dd3182cc2` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Aceite separado dos quatro teoremas, herdando explicitamente as provas anteriores do resolvente e de seu grupo. Afiliação, escala dual e traço não são conclusões deste delta; nenhuma promoção de gate ou alteração de memória. O negativo autoral de t→−t é apenas relido com pins e diagnóstico de elaboração; não há alegação de nova execução desse controle pelo revisor.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\independent_20260914_195640_056744\run.json>) — SHA256 `afa1bfdaeaf2023814a956139fad94bca032a4ee7554e4ac872334a5b3c8f0ee`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\compilation.json>) — SHA256 `e9c33584fa841df8e817c7e68f2f87634f2f52eaf5a99bbaa70af7d037c4d98d`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\independent_20260914_195640_056744\type_axiom_audit.json>) — SHA256 `e3d7adb5ac13798a5449ae7d85e29a3f1743db57047993d6ec07189e280363e6`.
