# Calibração das oito fontes por preparações unitárias canônicas
[REAL — Lean] 17 teoremas e9 definições/abreviações;26 termos auditados, módulo e importador exit0, sem avisos, só o trio padrão. O módulo foi compilado contra SignedCovectorCoverage e GeneralMetricEinstein previamente aprovados e congelados; suas fontes locais coincidem com as fontes cacheadas e os binários usados foram medidos antes/depois.

Os dois eixos são canônicos e normalizados. Com u=3/5,v=4/5:
κ+ = coherentCoupling(−3/5,4/5,u,v)>0;
κ− = coherentCoupling(0,1,u,v)<0.
Usamos oito pesos λ=1/8 e escalas r+=√(8/κ+), r−=√(8/(−κ−)).
Foi verificado λκ±r±²=±1. Assim as probabilidades de mistura são positivas, embora a fonte efetiva tenha quatro sinais negativos. Nenhum sinal foi transferido para uma probabilidade.

Aplicando esses fatores aos covetores p_i e m_i da polarização de traceReverse_g(T), a fonte calibrada é exatamente T para qualquer matriz simétrica T e métrica com inversa. As escalas são constantes: a suavidade dos covetores acompanha a de g,T, sem raiz de coeficiente variável.

[INPUT/OPEN] Trata-se de representação de uma fonte T fornecida. A conservação total de T pode ser transportada pela igualdade; conservação e energia por setor não são consequências da calibração. A adoção física de setores efetivos assinados exige explicitação. A lei de área e a reconstrução gravitacional permanecem no contrato apropriado.

A composição com JointUnitaryPreparation usa16 resultados (8 rótulos ×2 componentes). Como λ,u,v são fixos, sua base diagonal é a mesma para todas as fontes: T entra nos covetores, frequências, Hamiltonianos e resposta por direção. Uma seleção isolada do peso de base não contém esse T arbitrário. O registro necessário inclui a preparação/resposta que se pretende reconstruir.

Revisão independente: review_new_angular_chain conferiu fonte/recibo e a calibração λκr²; a realização conjunta tem pasta e recibo próprios. Tentativas falhas e backups em bytes preservados. Nenhum um.py foi executado ou importado.
