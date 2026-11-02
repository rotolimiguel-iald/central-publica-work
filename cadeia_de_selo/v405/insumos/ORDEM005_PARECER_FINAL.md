[REAL — aritmética e controles] A conta da v98 foi reproduzida. [DERIVED condicional] A forma de massa permanece algébrica sob hipóteses de fonte e borda. [OPEN] Realização física e teste quantitativo dos quatro domínios.

## A. O que foi medido e o que a v98 realmente apontou

O log contemporâneo de 16/07, copiado em ordem005_run_v98_stdout.txt, linhas 626–635, registra a tabela abaixo. O §178 de CLAUDE.md preserva o mandato de investigar/corrigir. O rito corrente contém os mesmos seis pares; sua árvore sintática é idêntica à versão associada ao resultado selado lido.

| Estrutura da tabela histórica | R (Mpc) | Massa da forma (M☉) | Âncora histórica (M☉) | Razão |
|---|---:|---:|---:|---:|
| Via Láctea | 0,1 | 4,81323×10¹³ | 1×10¹² | 48,1323 |
| Grupo Local | 1,5 | 7,21985×10¹⁴ | 5×10¹² | 144,3970 |
| Coma | 3 | 1,44397×10¹⁵ | 1,2×10¹⁵ | 1,20331 |
| Norma | 2 | 9,62647×10¹⁴ | 1×10¹⁵ | 0,962647 |
| Bacia GA | 57 | 2,74354×10¹⁶ | 5,4×10¹⁶ | 0,508063 |
| Laniakea | 80 | 3,85059×10¹⁶ | 1×10¹⁷ | 0,385059 |

São inputs históricos atribuídos às referências do rito, não massas revalidadas contra novos artigos. As incertezas e definições homogêneas de abertura não estão fornecidas. Os fatores medem o diagnóstico aritmético histórico; não são significâncias de falsificação observacional universal.

Com as constantes seladas, M/R=4,8132327361×10¹⁴ M☉/Mpc e √(GM/R)=1438,942166 km/s. O GA passa a janela larga, como já passava na v98. A discrepância de ordens vinha da extrapolação ao ramo galáctico, não de erro de multiplicação no GA.

R=57 Mpc vem do arredondamento de 40 h⁻¹ Mpc com h=0,7. Usar 57,142857… dá 2,7504187063×10¹⁶ M☉: mudança de apenas ~0,25%. Isso não remove fatores 48 e 144. Não há σ_R selado nesse bloco. G é constante medida; não é exata por definição do SI. Os valores selados de conversão foram preservados na recomputação, sem substituí-los por dados novos.

## B. O fator 2β² e a condição que falta

A derivação em ORDEM005_DERIVACOES.md identifica três passos diferentes: simetria das faces → w=1/2; lei de leitura radial → R_named=(β/w)R_struct; ponte de fonte → M=(c²/4πG)β R_named. A multiplicação produz 2β² e está verificada em Lean. A condição de realização da bacia já aparece no próprio L4_SELF_CONJUGATE_BOUNDARY_THEOREM.md; não foi inventada por esta auditoria.

A positividade de JS e a construção modular da torre não selecionam, sozinhas, uma métrica, um raio de bacia ou o gradiente de potencial requerido. A prova algébrica condicional não substitui essa identificação física. Gauss fornece M=R²Φ′/G; a normalização Φ′ requerida precisa ser derivada na ponte. O ensaio de perfil w(r)∝r^p mostra por que auto-conjugação sem lei radial não fixa o raio.

Há um controle adicional simples: mantendo M∝β²R/w e 0<w≤1, abandonar apenas w=1/2 permite reduzir a massa por no máximo um fator 2. Para corrigir as duas primeiras linhas por esse expediente seriam necessários w≈24,07 e w≈72,20, incompatíveis com pesos normalizados. Alternativamente, escolher R a partir da massa exigiria ~0,00208 Mpc e ~0,01039 Mpc; isso seria ajuste inverso, não predição geométrica independente. Esses controles não excluem uma condição de admissibilidade derivada que retire tais estruturas do domínio de aplicação; exigem que ela seja estabelecida sem olhar a massa.

## C. As três saídas, sem decisão em nome do operador

1. **Reinstauração limpa como lei física de fonte — não demonstrada nesta entrega.** A aritmética correta e o acerto na janela não bastam. Para essa saída, é preciso provar a ponte de fonte, a admissibilidade e a lei radial na bacia identificada independentemente. Se isso for obtido, a reinstauração pode citar os teoremas e seu domínio exato, mantendo a tabela v98 ao lado.
2. **Defeito persistente na extrapolação universal — reproduzido.** Os fatores 48,1323 e 144,3970 permanecem com os inputs históricos. A v98 não demonstrou com essa tabela, sem barras nem aberturas homogêneas, uma rejeição estatística de toda formulação restrita ao GA. Tampouco há um erro aritmético local que, corrigido, apague a tabela.
3. **Forma condicional no domínio admissível — sustentada como enunciado, realização física aberta.** Pode-se preservar explicitamente M=2β²(c²/4πG)R como consequência da ponte de fonte e da borda nomeada, sem apresentá-la como lei física já estabelecida. Uma restrição apenas nominal a aglomerados escolhidos porque a massa coincide seria seleção posterior; a admissibilidade precisa de critério independente.

Proposta de errata AO LADO, sem aplicá-la: “Reexame de 05/09/2026: a auditoria v98 apontou falha da extensão da forma às âncoras galácticas de sua tabela; não encontrou erro de multiplicação na massa do GA. A forma já existia no acervo como derivação condicional à ponte de fonte e à admissibilidade da borda, condição preservada nesta revisão. O diagnóstico numérico e a decisão editorial de retirada são atos distintos. A contestação do alcance do mandato permanece registrada para decisão do operador.”

Só o operador decide o alcance da correção histórica, a manutenção/reclassificação editorial e eventual autorização para a gerência alterar o programa. A bancada não reverte a v98 nem o veto GA ratificado.

## D. Quatro domínios: os números disponíveis e sua aptidão

| Domínio | Conteúdo do resultado selado lido | Uso quantitativo nesta proposta |
|---|---|---|
| Neutrino | JUNO: Δm²₂₁=(7,50±0,12)×10⁻⁵ eV², m₂=8,660254±0,069282 meV; NuFIT: 8,677557±0,057620 meV. Predição: 8,507414 meV. | Candidata: UMA determinação autônoma, após congelar a aproximação gaussiana e as normalizações. Não somar JUNO e global pós-JUNO. |
| Coma por fluxo | D_L=101,902786 Mpc; σ_stat=1,018377 e σ_sys=0,975713 Mpc; controle sem fluxo=110,849771 Mpc. comparison=null, referência não revelada nessa rodada. | Falta comparação primária e barras completas dos inputs. FP inversa 111,8±1,8 é controle, não árbitro substituto. |
| GA | 2,74354×10¹⁶ M☉ contra âncora 5,4×10¹⁶; janela [10¹⁵,10¹⁷]. | Sem σ_R, σ_M e covariância; lei condicional. Janela não é likelihood. |
| Piso | SDSS/V11: r_c=0,126929±0,013628, L5=0,058791; NOT_FALSIFIED_POWERED. DESI/V4.1: 0,188941±0,016661. | Densidade de núcleo com limite unilateral; não é medição de β. Não entra como igualdade gaussiana. |

O registro de 6,2σ é SNR=6,1866635 do perfil de shear na versão V1. Na mesma saída: χ²/dof do B-mode=12,3714, sistemáticas reprovadas, Fisher de separação do piso=0, r* sem restrição entre 0 e 0,3. O número de detecção bruta é preservado; não recebe estatuto de medição limpa de piso não nulo ou de β. O resultado de densidade independente é outro objeto e outro rito. A leitura ontológica de não nulidade não entra como termo de likelihood.

## E. Correlações e defeitos da fiação a comunicar

- JUNO/global: o rótulo indep=True em ambos não prova independência. O fonte pede duas determinações independentes ≥5σ, mas vd0 muda para FALSIFIED usando apenas tensao_atual global. Se esse veredito alimentar o veto expandido, corrigir primeiro a implementação da exigência de duas determinações; esta bancada não aplicou a correção.
- GA/Coma/piso: cosmologia de referência, H₀, calibração de distâncias e algoritmos podem gerar ancestrais comuns; inserir covariância ou condicionar explicitamente. Distintos fenômenos não garantem independência estatística. Coma inversa usa a mesma lei massa–raio do GA e não deve ser contada adicionalmente como outro teste independente de fonte.
- As réplicas de vazios compartilham objetos e pipeline. Surveys distintos podem ter volume cósmico comum e a mesma cosmologia. Não multiplicar suas evidências como réplicas totalmente independentes por decreto.
- β usa α externa, sem ajuste a esses domínios. A escala neutrino 1 eV, m₁=0, cosmologia de Coma, admissibilidade GA e relação de traçadores são hipóteses/inputs. Se algum for ajustado aos mesmos dados, o número de parâmetros deixa de ser 0 versus 1.
- BBN circular, CMB de proveniência reprovada e r_d cosmológico congelado constam de prove_evidence_audit. Esses resultados antigos não serão reciclados como quatro estimativas independentes e precisas de β.

## F. O rito proposto e o resultado desta bancada

JOINT_CONTOUR_V1_PREREG_DRAFT.md especifica hipóteses, seleção, covariância, transformação, AIC, falsificador bilateral Q_A, α, poder, veto, hash e parada. O código joint_contour_v1.py implementa o modelo gaussiano de constante comum. A derivação explica por que ΔAIC=2−G e por que a vantagem máxima de A é 2. Isso afia o argumento de parcimônia, limitando seu alcance em vez de inflá-lo.

Os controles sintéticos incluem A correto, B deslocado positivo e negativo, média correta com resíduos opostos, correlação, baixo poder e recusas. AIC e falsificação têm funções distintas: no caso de resíduos opostos A pode ganhar em AIC e ambos os modelos continuarem inadequados. O teste Q_A detecta esse caso.

O estado de QUATRO domínios é JOINT_CONTOUR_INCONCLUSIVE. Nenhuma estatística conjunta dos dados reais foi calculada: o rascunho não foi ratificado e os quatro contratos de entrada ainda não estão satisfeitos. Isso não é falsificação da TGL, nem atestado de concordância multidomínio. É a recusa correta de uma combinação sem verossimilhança e covariância estabelecidas.

Só o operador decide se congela a proposta, qual roster e quais dados prospectivos autoriza, mantendo explícitas as condições pendentes. Um hash do rascunho não substitui essa decisão. A gerência audita e incorpora; nenhum arquivo canônico foi alterado.
