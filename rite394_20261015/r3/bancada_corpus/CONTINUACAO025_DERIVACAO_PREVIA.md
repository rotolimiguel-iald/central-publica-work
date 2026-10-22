[DERIVED / INPUT / OPEN] CONTINUAÇÃO 025 — consistência térmica, limite dos andares e escala da resposta

06/09/2026. Derivação registrada antes do código. A etapa anterior é PROGRESSO: o auditor 024 foi reexecutado e conferiu 684 hashes, sete módulos, 85 teoremas e três definições impressas. O túnel continua com ordens 001–007. A árvore canônica e o Atlas mantêm H3 como INPUT; a bancada não modifica essa árvore nem o gate. O objetivo amplo continua aberto.

A questão crítica é remover a ambiguidade sobre o andar finito em 024. O dado de entrada continua sendo um perfil produto P. Nenhuma temperatura física, relação de área ou estado não-produto será inventado.

1. Produto e consistência. Para pesos positivos p,q, K_{p⊗q}=K_p+K_q. Logo Z_{p⊗q}(s)=Z_p(s)Z_q(s) e r_{p⊗q}(s)=r_p(s)⊗r_q(s). Construir um SiteProfile P_s com primeiro peso de cada sítio r_{siteW(P.w n)}(s,0). A positividade e a soma um dão P_s.w n∈(0,1). Provar towerW(P_s,N)=r_{towerW(P,N)}(s) para todo N. Com isso, as restrições locais são compatíveis entre andares, e a construção canônica aplicada a P_s fornece uma representação global própria. Não se identificam automaticamente H(P_s) e H(P).

2. Variância. Para produtos normalizados independentes, μ e V somam. Provar V_N=Σ_{n≤N} V_site(n), em particular V_N=(N+1)V_site para perfil constante. A aditividade de entropia finita já existe em TowerEntropyScaling e será reutilizada, não contada como descoberta nova. O resultado novo sobre a resposta de 024 implica κ_N=V_N/π e coeficiente -ℓ²V_N: em perfil estacionário não tracial, o acoplamento escolhido cresce sem limite quando o andar cresce, se mantidos os demais parâmetros.

3. Sobreposição e a parede de Hilbert. Definir c(p,r)=Σ_i sqrt(p_i)sqrt(r_i), com 0<c≤1 e c=1 exatamente quando p=r. Provar multiplicatividade sob produtos. Para r=r_p(s), s≠0 e p não tracial, c<1: a identidade de log dos pesos mostra que r=p forçaria s(K_i-K_j)=0. Os vetores de 024 satisfazem <Ω,Ψ_N(s)>=produto das afinidades dos sítios. Para perfil constante, isso vale c^(N+1) e tende a zero.

O alvo mais forte desta parte é calcular a distância entre vetores consecutivos no mesmo H(P): ||Ψ_{N+1}(s)-Ψ_N(s)||²=2(1-c_site). Se c_site<1, a sequência não tem limite em norma. Isso refuta o limite em norma da preparação específica; isoladamente não prova disjunção de todas as representações nem inexistência de qualquer estado normal com as marginais. A distinção precisa permanecer no relatório.

4. Escala explícita e limites. Examinar a escolha ℓ_N=ℓ/sqrt(N+1), equivalente a s_N=(ℓt)²/(N+1). Para cada N, o coeficiente de segunda ordem passa a -ℓ²V_site. A normalização é INPUT, não seleção física. Provar também que s_N→0 para t fixo e que, em qualquer andar observado fixo, a família converge ao estado original; o caráter extensivo da resposta não deve ser apresentado como uma nova variação local que sobreviva sem escala.

Não permutar limites N→∞ e t→0 sem prova. A formulação mínima exata deve dizer qual limite é tomado primeiro; qualquer limite uniforme adicional exige demonstração própria.

5. Integração e controles. Instanciar perfil tracial (família constante, V=0) e não tracial fiel (V>0, afinidade estrita). Ligar a resposta reescalada ao tensor com κ_site=V_site/π e reutilizar o controle plano de 024: conservar e corresponder ao calor não produz a hipótese de área. A dependência do corte, a mudança de representação e a lei de área permanecem obstáculos distintos.

Fontes: a literatura de Kakutani/Bures/Promislow trata equivalência e estados produtos infinitos por afinidades. Será usada como orientação, com hipóteses indicadas, jamais como axioma Lean. Não anunciar o teorema completo de normalidade/disjunção se somente a sobreposição e a não convergência da sequência escolhida forem formalizadas.

Escrita apenas em Chatgpt. Originais, um.py, kernel canônico, Atlas, memórias, diários, gate e entregas anteriores intocados. Backups dos bytes antes de revisar fontes próprios não selados; nenhuma edição durante compilação; todos os erros/avisos rejeitados preservados. Toda conclusão formal viaja com enunciado, hipóteses, axiomas e hashes medidos. Incorporação e auditoria independente cabem à gerência.
