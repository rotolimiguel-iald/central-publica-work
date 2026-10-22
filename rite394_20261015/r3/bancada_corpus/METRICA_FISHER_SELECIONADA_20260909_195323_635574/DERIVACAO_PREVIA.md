# Derivação prévia: Fisher selecionado e leitura lorentziana

[DERIVED — plano da prova, ainda não compilado]

Dados de entrada: aberto U em R^4; probabilidades P_i suaves, estritamente positivas e normalizadas; o diferencial conjunto é injetivo; um rótulo selecionado j tem dP_j não nulo em U. Nenhuma métrica é recebida.

F = soma_i (dP_i tensor dP_i)/P_i é positivo definido pelo posto. Ponha c = dP_j, a = c^T F^(-1)c > 0, g = (2/a)c tensor c - F. A inversa proposta é (2/a)(F^(-1)c) tensor (F^(-1)c) - F^(-1). Sua multiplicação cancela os termos de posto um. A assinatura (+---) é derivada de uma base ortonormal para F adaptada a F^(-1)c/sqrt(a), ou de uma fatoração positiva e reflexão ortogonal explícita. Essa base só testemunha a conclusão; não entra no protocolo. A expressão de g usa apenas derivadas de P, inversa matricial e divisão por a>0, logo é suave. Só então encodeLorentzRecord serve de adaptador aos consumidores já compilados.

[INPUT] A dimensão quatro, a lei de leitura assinada, o protocolo P, o posto e a escolha de relógio não são produzidos pela álgebra de Fisher. Uma troca descontínua de rótulos não preserva automaticamente suavidade. A construção não afirma que toda métrica de Lorentz seja atingida.

[DERIVED — controles]
Quatro Bernoulli independentes com canais fixos dão F = soma_a dy_a^2, y_a=2 arcsin sqrt(p_a). Distinguir y_0 produz g=dy_0^2-soma_{a>0}dy_a^2: localmente plana. Não usaremos isso como testemunha de curvatura geral.

Uma distribuição categórica com cinco resultados tem P_0=q, P_a=(1-q)Q_a, soma Q_a=1. Seu Fisher é dq^2/[q(1-q)]+(1-q)F_Q. Escolher c=dq produz g=dq^2/[q(1-q)]-(1-q)F_Q. No interior do simplex de dimensão quatro, o posto é quatro. Nas coordenadas angulares r=2 arcsin sqrt(q), e Q no octante positivo da esfera unitária S^3, g=dr^2-4 cos^2(r/2) h_S3. O fator a(r)=2 cos(r/2) satisfaz a''/a=-1/4; a curvatura mista não é zero. Esta testemunha é derivação escrita, não prova Lean salvo teorema posterior explicitamente compilado.

[OPEN] Não se deduz o matching de área: amostragem afim de um P geral tem derivada entrópica de primeira ordem não nula; telas de equilíbrio têm A'(0)=0. A construção métrica não elimina a obrigação de área nem identifica esta leitura com um protocolo físico observado. Positividade diagonal também não torna uma preparação vetorial pura fiel na álgebra matricial completa.
