# Lentes: o que sobrevive ao ajuste — resultado R2

19/10/2026, em nome de codex-gerente-tgl. Unidade F8.LENTES_5SIGMA_20261019. [DERIVED — ações recuperadas e controles sintéticos; nenhum veredito observado].

## Resposta operacional

Recuperamos duas ações fotônicas escritas, uma distância angular implementada e a correção vigente da massa linear. Calculamos a propagação do operador Ricci tensorial e a absorção dos efeitos por parâmetros de massa/distância. **Ainda não há um sinal discriminante observado de5σ. Os ramos quantitativamente examinados não sustentam esse objetivo nas condições testadas.** Isso não é uma exclusão da TGL inteira nem um levantamento exaustivo de todo o acervo.

| Ramo realmente escrito | Resultado calculado | Consequência para o teste |
|---|---|---|
| α₂R_abF^{ac}F^b_c/M_P², com α₂=β | Atraso extra proporcional à diferença de colunas de matéria; zero no exterior Schwarzschild Ricci-flat; controle ΔΣ=10kg/m²,z_l=0,5 dá2,93473×10⁻¹⁰⁵s | Normalização de Planck torna o efeito local impraticável nesse regime; não deriva50ms |
| Escalar RF², prefator regular | Mesmo cone nulo no limite principal da óptica geométrica | Não produz automaticamente atraso geométrico extra; transporte de amplitude/efeitos de onda são questões distintas |
| Fundo H_TGL²=H_LCDM²(1+β|1+w_eff|), coeficientes livres | Reparametrização exata de H0,Ωm,Ωr,ΩΛ; todas as distâncias coincidem | Distâncias sozinhas não identificamβ nessa família |
| Mesmo fundo, radiação física fixada pelo default | Controle de cinco distâncias, perfilando H0 eΩm, deixa residual máximo2,011125×10⁻⁸ | Residual não zero, mas muito abaixo de precisão percentual no controle; não é previsão de significância em uma amostra real |
| Duas imagens axiais + um atraso, potencial ponto-massa com perturbação radial | Família exata ajusta massa, fonte e distância preservando esses observáveis | Acertar o atraso pelo ajuste de massa não é, sozinho, discriminação |

## O novo cálculo de distância, delimitado

BACKGROUND_PLAN_R2.json foi gravado antes da execução. Os cinco pares (z_l,z_s) são (0,2;1), (0,3;1,5), (0,5;2), (0,7;2,5), (0,9;3); **sintéticos**, escolhidos para cobrir um intervalo, sem ajuste a lentes observadas. H0 nu=70 eΩm nu=0,3 são entradas desse controle, não estimativas da natureza. T_CMB eN_eff foram lidos do Custo; β foi calculado em runtime do um.py, sem importá-lo.

A integração usa a mesma geometria plana e D_Δt=χ_lχ_s/(χ_s−χ_l). O modelo GR ajusta H0 eΩm simultaneamente, mantendo a mesma densidade física de radiação. O mapa de equivalência com radiação livre foi conferido como controle separado. A integração128/256 pontos difere no máximo1,33×10⁻¹⁵ em fração, abaixo do residual medido. A otimização convergiu dentro dos limites declarados.

Resultados sintéticos:

- Máximo |D_GR,ajustado/D_TGL−1|: **2,011125×10⁻⁸**.
- Norma de separação dos cinco valores, com erros independentes de1% em cada distância: **3,03426×10⁻⁶**. É uma norma Asimov da comparação escolhida, não um p-valor observado.
- Para essa mesma norma alcançar5, o erro fracional igual em cada distância teria de ser aproximadamente **6,07×10⁻⁹**, sob a covariância ideal declarada. Não inclui modelagem de massa, convergência externa ou anisotropia. Não é uma proposta de precisão instrumental realizável.

Nota de nomenclatura do JSON: `ideal_common_fractional_sigma_for_norm5` significa um **mesmo valor de erro em cinco medições independentes**, conforme o plano; não significa um erro sistemático comum correlacionado. A projeção com radiação livre dá degenerescência exata. A fonte default fixa radiação e, por isso, mantém o pequeno residual. Uma informação externa real sobre matéria/Hubble pode restringir o ajuste e mudar a comparação; não foi acrescentada para elevar a norma.

## O que falta para uma rota empírica viável

1. **Confrontar a lei de leitura acumulada D1b com as distâncias angular e lente–fonte.** A ORDEM018 já provou que K(z) isolado não determina f_t,F_D,f_φ; a função angular recuperada pertence ao fundo local e não pode ser substituída silenciosamente por K*/k(z). É a diferença entre esses consumidores que precisa de resolução documental/matemática, não uma nova pergunta abstrata sobre identidade.
2. **Uma assinatura que permaneça após os ajustes permitidos.** Massa dinâmica independente e ambiente, ou um padrão adicional derivado de raios, podem restringir as degenerescências. A correção atual do um.py estabelece M_TGL^linear=M_RG sob suas hipóteses e não autoriza multiplicar G ou massa porβ. Não localizamos nos recortes consultados outro slip de lente com amplitude fixada.
3. **Só então uma likelihood conjunta com fontes custodiadas e função de veredito pré-fixada.** A previsão deve usar a mesma massa/anisotropia/distâncias nos observáveis associados. A amplitude não será escolhida para produzir5σ; a busca pode concluir que um canal não tem poder.

O caminho útil em lentes continua sendo atraso + imagens + cinemática, desde que a teoria forneça uma diferença identificável entre essas leituras. Esta etapa evita gastar a análise em uma alteração que desapareça por mudança de parâmetros. A meta empírica segue aberta; não foi substituída por confirmação formal ou pela existência de um parâmetroβ.

## Evidência e revisão

TRAJECTORY_DERIVATION_R2.md expõe a variação e a integral; IDENTIFIABILITY_R2.md traz23 controles racionais; DISTANCE_REPARAMETRIZATION_R2.md prova o mapa de parâmetros e sua ressalva de radiação. SOURCE_ACTION_R2.md/ALT_LENS_LAW_R2.md trazem fontes e linhas. RICCI_CALCULATION_RESULT_R2_1.json e BACKGROUND_RESULT_R2.json contêm os números e pins. REVIEW_R2.json registra a revisão independente da primeira camada; o controle numérico de distância tem revisão separada em REVIEW_BACKGROUND_R2.json quando emitida. Não se afirma que esta redação do resumo foi ela própria reexecutada ou aceita pela gerência.

Os originais, kernel, um.py e Bancada foram apenas consultados ou preservados; nenhum dado observado foi composto, nenhum provedor chamado e nenhum gate alterado. O primeiro erro mecânico de comparação SymPy foi preservado e corrigido em arquivo novo. Uma âncora de constante no recibo aponta a linha anterior por whitespace do regex; o valor e seus bytes foram conferidos, sem impacto no cálculo.
