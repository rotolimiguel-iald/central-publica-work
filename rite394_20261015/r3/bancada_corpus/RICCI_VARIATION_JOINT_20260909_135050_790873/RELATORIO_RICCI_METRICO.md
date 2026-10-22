# Ricci da métrica perturbada — primeira variação real

[REAL — compilado e auditado no alcance abaixo]

A entrega identifica a derivada temporal do Ricci canônico da família de Levi-Civita de g+t h com ricciVariation(Gamma, metricConnectionVariation g h). A função derivada é o próprio coordinateRicci(perturbedLeviCivita g h t), e não uma fórmula homônima introduzida como substituto.

O núcleo JointCurvatureVariation prova a troca temporal/espacial pelo teorema de Schwarz aplicado à regularidade conjunta. A aplicação MetricRicciVariation deriva essa regularidade para a conexão real: a inversa é suave pela fórmula adjunta/determinante, o jet espacial da métrica perturbada é calculado por linearidade, e a fórmula real de Levi-Civita combina esses fatores. Nenhuma hipótese hjet é fornecida ao teorema final.

## Hipóteses e domínio

U é um aberto de R⁴. As componentes de g e h são C∞ em U e cada g(x), x∈U, é inversível. Define-se W={(t,x) : x∈U e det(g(x)+t h(x))≠0}. A prova mostra que W é aberto e contém (0,x). Não exige um intervalo temporal uniforme válido para toda uma região não compacta. A derivada é local em t=0, para cada x∈U.

A primeira variação da conexão é identificada em todo U por unicidade da derivada. A igualdade local das conexões transporta seus jets espaciais reais antes da identificação de ricciVariation. Isso evita uma igualdade apenas pontual que não bastaria para diferenciar no espaço.

## Aplicação geométrica e alcance

O enunciado algébrico admite campos matriciais não simétricos. Para sua interpretação como Levi-Civita de uma família de métricas, especializar a g e h simétricos; compatibilidade e ausência de torção pertencem aos certificados canônicos já existentes. O teorema não produz a assinatura Lorentziana nem estende a construção a torção/spin.

Gamma(t) é a conexão de g+t h e não precisa ser afim. A igualdade de primeira ordem não identifica essa família com Gamma+t deltaGamma em ordens superiores.

[OPEN — próximo elo] Especializar h à derivada de Lie de g e provar a naturalidade métrica sob difeomorfismos em fundo curvo. A identidade pertinente para o Ricci é sua derivada de Lie, que não se anula em um fundo curvo arbitrário. Não se afirma uma Ward métrica completa, nem controle de anomalias quânticas, nem fechamento UV.

## Verificação e preservação

Compilação de folha em bancada nova, com artefatos locais PASS copiados byte a byte e dependências canônicas/Mathlib lidas. O recibo verifica hashes das fontes/cache e fronteira direta antes/depois. As dependências transitivas não foram todas recompiladas ou novamente hasheadas nesta folha. Nenhum um.py foi executado/importado, e nenhum original, Atlas ou memória foi alterado.

A revisão semântica independente de /root aprovou a cadeia do núcleo conjunto e da aplicação métrica. As correções posteriores restringiram-se à elaboração das provas: auditorias intercaladas, orçamento de elaboração, prova explícita de soma/produto e aplicações da API. Os enunciados foram preservados.

O primeiro build da aplicação terminou TIMEOUT; o segundo localizou uma busca automática lenta e duas chamadas de API incompatíveis, com falha visível. Todos os builds e backups permanecem preservados. O resultado aprovado é exclusivamente o recibo PASS final.

## Recibo final medido

- Fonte: [MetricRicciVariation.lean](C:/IALD/Central%20de%20Patentes/Chatgpt/RICCI_VARIATION_JOINT_20260909_135050_790873/MetricRicciVariation.lean): 8621 bytes; SHA-256 `881bec4d1d14c9f0117253b9a18c672eae960e43943e3847af96c6c6ba7c56c4`.
- Build: `BUILD_20260909_141308_862807`; 12 teoremas + 3 definições; 15 auditorias; dois exits 0; somente propext, Classical.choice e Quot.sound; zero avisos/erros.
- Núcleo conjunto preservado: `BUILD_20260909_135701_498129`; 10 teoremas + 4 outros termos. Suplemento total: 22 teoremas + 7 outros termos, sem somar novamente as dependências herdadas.
- Assinaturas das 15 declarações da aplicação comparadas por script com a primeira versão: inalteradas. Fonte de trabalho idêntica em bytes à fonte do build PASS.

## Localização dos elos

- `joint_matrix_inverse_smooth`: linha 51.
- `metric_nonsingular_domain_open`: linha 73.
- `perturbed_levi_civita_joint_smooth`: linha 109.
- `metric_time_derivative_eq_on`: linha 147.
- `ricci_variation_congr_on`: linha 163.
- `metric_ricci_first_variation`: linha 180.
