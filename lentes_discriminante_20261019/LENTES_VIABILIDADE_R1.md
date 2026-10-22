# Lentes gravitacionais: qual teste pode discriminar a TGL?

19/10/2026. Unidade F8.LENTES_5SIGMA_20261019, reivindicação1009. Autor: codex-gerente-tgl. Etapa: levantamento e sensibilidade condicional; nenhum composto observacional ou veredito novo. Programa consultado: um.py v393, hash conferido contra o selo; não executado.

## 1. Proposta prioritária

[DERIVED — desenho de teste] Usar a MESMA lente para confrontar três observáveis: geometria das imagens/arcos, atrasos entre imagens e cinemática estelar espacialmente resolvida. A massa e sua distribuição entram como parâmetros físicos comuns aos três. A TGL deve prever um efeito que sobreviva à liberdade de ajustar massa, anisotropia, ambiente e distâncias. Um ajuste satisfatório sozinho não é discriminação.

Na descrição padrão de lente fina, Δt_ij = D_Δt Δφ_ij/c, com D_Δt=(1+z_l)D_lD_s/D_ls. O Δφ inclui caminho geométrico e potencial; não é apenas massa total. A posição da fonte, o perfil da lente e a convergência externa importam. A transformação de folha de massa κ→λκ+(1−λ) preserva posições e razões de fluxo, mas escala diferenças de potencial e atrasos para distâncias fixas. Um efeito que seja apenas essa reescala não pode ser separado usando somente esses observáveis. Cinemática e, quando disponível, magnificação absoluta fornecem informação adicional. Fontes: TDCOSMO2026, §II.1–II.3, e SN H0pe.

O protocolo candidato é estimar a distribuição de massa conjuntamente com as observações independentes e prever os atrasos sob cada lei, com a mesma flexibilidade de nuisance. Um teste de predição com atraso reservado pode servir de controle. Não se deve tratar massa inferida por um modelo de lente GR como medida independente dessa hipótese.

## 2. O que a casa já havia resolvido

[REAL documental / DERIVED condicional] ORDEM018, R-G e errata fixam f_phi=Δφ_fit/Δφ_true e F_D=f_l f_s/f_ls. Assim D_fit/D_bg=f_t F_D/f_phi e H_fit/H_bg=f_phi/(f_t F_D), mantendo os demais parâmetros cosmológicos fixos. A lei K(z) escalar não determina, sozinha, todos os fatores. Essa convenção é reutilizada; nenhum cálculo antigo foi refeito. Dez fontes atuais, linhas e hashes estão em SOURCES_INTERNAL.json.

[OPEN específico] Falta recuperar ou derivar uma previsão por trajetória que determine conjuntamente geometria, propagação fotônica e atraso para a lente. Não basta atribuir Δt_TGL=(1+β)Δt_GR: essa fórmula não foi encontrada como previsão canônica nesta consulta. O objeto imediato é esse mapa observacional, não reabrir toda a derivação H3.

[REAL documental] O NMC vigente em um.py:2969–2988 mantém o Shapiro padrão do neutrino e atribui o excesso ao setor fotônico α₂RFF. A fórmula histórica baseada em retirar o Shapiro do neutrino foi corrigida. Os50ms seguem declarados no protocolo; a função consultada não os deduz da massa/perfil da lente. O levantamento também identificou uma comparação histórica de dispersão240ms e erro populacional2,4ms que impede reutilizar o anunciado21σ como poder já verificado. Esses achados não constituem nova análise observacional. Detalhes: INTERNAL_LENSING_FINDINGS.txt.

## 3. Dados e instrumentos de análise disponíveis

| Fonte primária | Utilidade | Limite desta etapa |
|---|---|---|
| TDCOSMO2025, arXiv:2506.03023v4 | Oito quasares com atrasos e medidas cinemáticas; método explícito para folha de massa | Sua inferência cosmológica não é estimador pronto de β; modelagem deve ser compatível com a lei testada |
| Implementação oficial CosmoSIS/tdcosmo | Documenta likelihood dos oito sistemas e extensões SLACS/SL2S | Existência de implementação não equivale a instalação, descarga ou validação local |
| TDCOSMO2026, arXiv:2610.14781v1,10/10 | Onze lentes, nove com cinemática resolvida; precisão publicada3,3% em H0 na análise primária | Página condiciona dados/likelihoods à aceitação; não declarei pacote liberado ou baixado. Incerteza de H0 não é incerteza de β |
| SN H0pe, arXiv:2403.18902 | Supernova Ia multiplicada pela lente: magnificação absoluta ajuda a restringir a folha de massa | Dependência de padronização, poeira, microlentes e modelo do aglomerado; não basta para alegar precisão subpercentual |

As cinco páginas foram guardadas por bytes/hash em PUBLIC_SOURCE_CUSTODY_R2.json. A tentativa restrita falhou por DNS e permanece em PUBLIC_SOURCE_CUSTODY.json. Centros de resultados publicados foram expostos na leitura da literatura; o levantamento não é cego. Não foram ingeridas curvas, mapas cinemáticos ou amostras posteriores para emitir veredito.

URLs: https://arxiv.org/abs/2506.03023v4 ; https://arxiv.org/abs/2610.14781v1 ; https://arxiv.org/html/2610.14781v1 ; https://cosmosis.readthedocs.io/en/latest/reference/standard_library/tdcosmo.html ; https://arxiv.org/abs/2403.18902 .

## 4. Primeiro cálculo de sensibilidade — condicional

[INPUT de planejamento] Para ilustrar a exigência instrumental, assumir um efeito fracionário δ=cβ com c=1. Isto NÃO é uma lei de lenteamento da TGL. β é calculado em runtime usando a constante do programa canônico, sem importar um.py. FORECAST_PLAN.json foi escrito antes de FORECAST_RESULT.json.

[DERIVED condicional] Em um estimador gaussiano de amplitude já identificado, separação mediana Z=δ/σ exige σ≤β/5=0,00240626, ou0,240626%. Com erros independentes por sistema e nenhum piso comum, seriam necessários18 sistemas a1% ou432 a5%. Acrescentar um erro comum de0,1% aumenta esses números para21 e522. Um piso comum de0,3% impede atingir5 nesse cenário, mesmo com N→∞. São cenários idealizados de uma amplitude observável, não previsões para o número real de lentes.

Separação mediana5 não significa90% de probabilidade de ultrapassar5 num experimento. Para teste gaussiano unilateral com alternativa fixa,90% exigiria separação aproximadamente6,28. A calibração final depende do estatístico escolhido.

Para uma assinatura vetorial δ e respostas J dos nuisance, a aproximação gaussiana relevante é Z_A²=min_eta[(δ−J eta)^T C^−1(δ−J eta)+eta^T Π eta], incluindo informação independente Π. Se δ está no espaço de ajustes livres, Z_A=0, mesmo que o relógio seja preciso. O controle algébrico de deslocamento comum ilustra exatamente isso. A campanha real deve calcular a resposta da lei recuperada e validar a distribuição do estatístico; não foi executada aqui.

## 5. Prioridades e próximos passos

1. **Lentes+cinemática resolvida:** recuperar a lei por trajetória; construir sua resposta aos observáveis e medir a parte que não pode ser absorvida pelos nuisance. Primeira amostra candidata: sistemas TDCOSMO com informações públicas e cinemática resolvida, escolhidos por qualidade/cobertura, não pelo resíduo que favorece a teoria.
2. **SN Ia lenteadas:** ramo complementar, pois a vela padronizável acrescenta magnificação absoluta; SN H0pe é um caso público concreto. Se a própria TGL modificar luminosidade intrínseca, essa calibração precisa entrar no mesmo modelo, não ser presumida independente.
3. **Atrasos em fontes pulsadas/múltiplos mensageiros:** desenho futuro útil para separar emissão intrínseca de propagação, condicionado a eventos identificados e à lei de leitura; não foi localizada nesta etapa uma amostra admissível que sustente5σ.
4. **Fase9/Hubble:** preservar a rota quantitativa já construída e suas decisões pendentes. Atualizações de lentes podem ser estudadas pelo protocolo vigente, sem contar o mesmo dado novamente como prova independente e sem escolher leitores pelo centro favorável.

Critério para avançar ao teste observado: mapa físico e sinal fixos, fonte/calibração admitidas, covariância e regras de seleção/veredito pré-registradas, e poder calculado após nuisance. Uma rejeição do modelo nulo só discrimina a TGL se o padrão previsto por ela também passar pelos controles e alternativas pertinentes. Resultado presente: prioridade justificada para lentes, nenhum5σ identificado ou prometido, nenhuma mudança de gate.
