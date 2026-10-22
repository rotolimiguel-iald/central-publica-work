# Revisão própria do coeficiente sigma em métrica externa

09/09/2026. Leitura da nota `CONTRATERMOS_SIGMA_E_ORDEM_EFT.md` da frente complementar. Esta é uma análise matemática desta sessão; não é aprovação atribuída ao operador ou a outra sessão. Nenhuma compilação ou execução CAS foi repetida.

**[DERIVED]** Para o operador euclidiano P=−(D²+E), E=QI₃−U, as identidades trU=Q e trU²=W² dão trE=2Q e trE²=Q²+W². Para Ω_{μν}=u_μ⊗u_ν−u_ν⊗u_μ, contrair o quadrado dá trΩ_{μν}Ω^{μν}=2(W²−Q²), com esse sinal porque Ω é antissimétrico. Substituir na expressão universal de [Vassilevich, equação (4.28)](https://arxiv.org/html/hep-th/0306138v3) produz

\[
\frac12\operatorname{tr}E^2+\frac1{12}\operatorname{tr}\Omega^2
=\frac13Q^2+\frac23W^2,\qquad
\frac16R\operatorname{tr}E=\frac13RQ.
\]

O traço da identidade vale três, logo os termos puramente métricos recebem 1/120. As derivadas totais são □Q/3 e □R/10. Assim a expressão B₄ da nota lida está consistente com a convenção P=−(D²+E). O sinal do termo misto RQ não seria o mesmo se se trocasse a definição de E sem trocar a fórmula universal.

Na representação Γ₁=−ħ/2∫_{ρ⁻²}^∞dt K(t)/t, a integração de t⁰ no coeficiente do calor, entre ρ⁻² e uma escala finita μ⁻², dá ln(ρ²/μ²). O fator global −ħ/[2(4π)²] da parcela logarítmica está correto nessa convenção. Isso não afirma que a integral infravermelha exista quando P tenha espectro não positivo; a nota faz a separação necessária.

**[DERIVED] Controle independente do exemplo.** No toro plano, φ_k=(cos kx,sin kx,0,0), k inteiro, é suave e harmônico. O vetor tangente e₁=(−sin kx,cos kx,0,0) tem derivada −kφ_k normal ao alvo; portanto sua derivada covariante tangente é zero. Os dois vetores transversais constantes também são paralelos. Nesse referencial global a conexão puxada é trivial, E=diag(0,k²,k²) e o traço do calor local possui fator 1+2 exp(tk²). O coeficiente de t² é k⁴, confirmando B₄ sem depender da contração geral.

Um termo constante e a renormalização da cinética fornecem A+Bk², que não iguala k⁴ para todos os inteiros: k=0,1 fixa A=0,B=1 e k=2 dá diferença 12. Como os mapas são on-shell e o toro não tem bordo, termos proporcionais à equação sigma e divergências totais não desfazem o exemplo por integração. A conclusão de não fechamento na ação original é, assim, válida no setor sigma com métrica externa.

As ressalvas da nota são essenciais: redefinição de uma métrica dinâmica, laços gravitacionais, ghosts e blocos mistos não são testados por esse exemplo. Não se calculou o coeficiente completo da teoria acoplada. O contra-termo covariante de ghost zero não é automaticamente uma anomalia de ghost um. A contagem D=4L−2I+Σd_v=2+2L+Σ(d_v−2) segue da identidade topológica do grafo conectado; é um grau superficial, não a prova de que todo coeficiente permitido é não nulo.

**Limite desta revisão.** As contas acima conferem os sinais, fatores e o exemplo de não absorção. A afirmação variacional sobre o mapa probabilístico livre na seção 6 da nota lida depende do adendo de imersão/inverso à direita da frente 067; ela não foi rederivada nesta revisão. Sua distinção entre transporte clássico e equivalência de medidas quânticas é necessária. O recibo CAS associado é apenas lido e medido no manifesto desta pasta; a presente análise não declara ter executado aquele script.
