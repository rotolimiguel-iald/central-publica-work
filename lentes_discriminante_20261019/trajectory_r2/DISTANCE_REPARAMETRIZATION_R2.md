# Distâncias de fundo: reparametrização e alcance — R2

19/10/2026. F8.LENTES_5SIGMA_20261019, claim1009, referência própria SESSION_REFERENCE.json confirmada na revisão2. [DERIVED] Análise da função efetivamente escrita; não é revisão da totalidade da cosmologia TGL e não é veredito observado. A fonte foi lida como texto, **não importada nem executada**. Autor: subagente codex da coordenação. Não foi feita nova campanha numérica.

## 1. O que a fonte implementa

`C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` SHA256 `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd`:

- 3299–3302: H_LCDM²=H0²[Ωm a⁻³+Ωr a⁻⁴+ΩΛ], sem curvatura.
- 3283–3296 e3358–3371: w_eff=(Ωr a⁻⁴/3−ΩΛ)/(Ωm a⁻³+Ωr a⁻⁴+ΩΛ), e H_TGL²=H_LCDM²[1+β|1+w_eff|].
- 3315–3322: a motivação da resposta fala em βXi+O(β²), mas a função devolve somente βXi. A equivalência abaixo é exata para **esse modelo implementado**, não para correções de ordem superior desconhecidas.
- 3266–3280 e3349–3355: Ωr é calculada de H0, T_CMB e N_eff; ΩΛ=1−Ωm−Ωr.
- 3374–3404: χ(z)=∫₀ᶻc/H_TGL dz, D_L=(1+z)χ e D_A=χ/(1+z).
- 198–202: β é calculada como ALPHA_FINE_CODATA_2018·√e. Não é avaliada numericamente nesta nota, nem substituída por literal.

Hipóteses da redução: a>0, Ωm,Ωr≥0, E²=Ωm a⁻³+Ωr a⁻⁴+ΩΛ>0, fora das guardas numéricas de denominador pequeno, β constante e coeficientes finais positivos. Então 1+w_eff=(Ωm a⁻³+(4/3)Ωr a⁻⁴)/E²≥0. O módulo não troca o sinal nesse domínio. Multiplicando explicitamente,

**H_TGL²=H0²[(1+β)Ωm a⁻³+(1+4β/3)Ωr a⁻⁴+ΩΛ].**

Essa é uma identidade do fundo homogêneo escolhido. Não abrange um w(a) adicional/phantom, β correndo com época, neutrinos massivos com transição de estado, curvatura, correções superiores ou a lei fotônica local α₂RFF.

## 2. Equivalência exata quando os coeficientes são livres

Escreva Cm=(1+β)Ωm, Cr=(1+4β/3)Ωr, CL=ΩΛ e S=Cm+Cr+CL>0. Defina

H0'=H0√S; Ωm'=Cm/S; Ωr'=Cr/S; ΩΛ'=CL/S.

Então Ωm'+Ωr'+ΩΛ'=1 e, para todo a no domínio,

H_GR²(a;H0',Ω') = H0'²(Ωm'a⁻³+Ωr'a⁻⁴+ΩΛ') = H_TGL²(a;H0,Ω).

Com H>0, a igualdade é de H, não apenas dos quadrados. Para Ωm+Ωr+ΩΛ=1, S=1+βΩm+(4β/3)Ωr. A prova é a igualdade separada dos três coeficientes de a⁻³,a⁻⁴,1. Essas funções são linearmente independentes em qualquer intervalo aberto de a; assim a igualdade do fundo inteiro exige justamente a correspondência dos coeficientes.

Para β fixo com fatores positivos, o mapa também tem inversa na família positiva livre: dado Ω' plano, seja C=Ωm'/(1+β)+Ωr'/(1+4β/3)+ΩΛ'. Então S=1/C, Ωm=SΩm'/(1+β), Ωr=SΩr'/(1+4β/3), ΩΛ=SΩΛ', H0=H0'/√S. Portanto é uma mudança de parâmetros bijetiva nesse domínio, não apenas uma aproximação em β.

### Fecho H(0)

No código, com fecho **nu** Ωm+Ωr+ΩΛ=1, vale H_TGL(0)=H0√S, em geral diferente do argumento chamado H0. O Hubble de hoje da função é H*=H0√S. Com β>0 e matéria/radiação positivas, exigir simultaneamente H_TGL(0)=H0 e o fecho nu é incompatível, exceto no limite sem matéria nem radiação.

Há três descrições distintas, que não devem ser misturadas:

1. **Função original:** H0 é a escala nua; H*=H0√S é o valor físico presente. A reparametrização acima descreve essa função sem mudá-la.
2. **Renomear por H*:** substituir H0=H*/√S na fórmula original, acompanhando todas as dependências de Ωr(H0), é mudança de coordenadas da mesma família.
3. **Dividir a função por √S mantendo os mesmos argumentos numéricos:** H_closed=H_raw/√S tem H_closed(0)=H0 e densidades efetivas Ω'=C/S, mas altera as distâncias daquela escolha original de parâmetros. É outro fechamento/modelo até explicitar a equivalência parametrizada e os priors.

Alternativamente impor Cm+Cr+CL=1 com H0 físico muda o fecho dos coeficientes nus. Não corrigimos o código nem escolhemos um desses contratos nesta nota.

## 3. Todas as distâncias de lente de fundo coincidem no mapa livre

Admitindo a mesma geometria FLRW plana, mesma constante c, mesmos redshifts e propagação de fundo usada na fonte, H_GR(z)=H_TGL(z) implica χ_GR(z)=χ_TGL(z). Logo são idênticos D_l, D_s e D_ls=[χ(z_s)−χ(z_l)]/(1+z_s), bem como

D_Δt=(1+z_l)D_lD_s/D_ls, D_L, D_A e razões dessas distâncias.

Consequentemente, **nenhuma quantidade de lentes e de redshifts identifica β por essas distâncias apenas quando os três coeficientes de expansão estão livres**. Não é só uma absorção de H0: também se reparametrizam as frações de matéria/radiação/Λ. A mesma massa física/projeção e lei de lente, nas mesmas distâncias, produzem o mesmo setor geométrico de lente; efeitos locais adicionais de propagação ou uma relação dinâmica diferente não estão incluídos nessa conclusão.

Isso não prova equivalência de crescimento de estruturas, recombinação, espectro CMB, física do som, BBN ou toda a teoria. Um BAO não é apenas D_V: a régua r_d tem de ser prevista/medida com seu próprio contrato. A igualdade de H sozinha não transporta essas leis.

## 4. A ressalva material: a radiação default da fonte NÃO está livre

A função `omega_radiation_today` fixa a densidade física de radiação

ωr ≡ h²Ωr = 2,473·10⁻⁵ (T_CMB/2,7255 K)⁴ [1+A N_eff],
A=(7/8)(4/11)^(4/3), h=H0/(100 km s⁻¹ Mpc⁻¹).

Os números desta linha são os coeficientes da fonte, não novas medidas. Sob o mapa livre, h'²Ωr'=(1+4β/3)h²Ωr=(1+4β/3)ωr. Portanto um ΛCDM que mantenha **os mesmos T_CMB e N_eff**, usando a mesma função de radiação, não contém em geral o ponto reparametrizado. A alegação de equivalência exata das duas implementações default seria falsa para βΩr≠0.

Com T_CMB fixo mas N_eff livre, o coeficiente pode ser reproduzido por

N_eff'=[(1+4β/3)(1+A N_eff)−1]/A.

Com N_eff fixo mas T_CMB livre: T_CMB'=T_CMB(1+4β/3)^(1/4). São correspondências algébricas da radiação de fundo, não permissões para ignorar medições externas nem prova de equivalência do CMB/BBN. O mapa também exige ωm'=(1+β)ωm; uma determinação independente da densidade física de matéria pode restringi-lo.

Se os coeficientes material e constante forem casados mas a radiação física for mantida fixa no GR, o termo residual exato é

H_TGL²−H_GR² = H0²(4β/3)Ωr a⁻⁴,

onde H0,Ωr do lado direito são os parâmetros nus da TGL, e o GR foi definido pelo casamento dos outros dois coeficientes. Se também se exigir H_GR(0)=H_TGL(0), os três casamentos não podem continuar simultaneamente: o residual é redistribuído entre coeficientes. Não extrapolar a expressão de um ajuste específico para outro.

Nos baixos redshifts, a contribuição de radiação é pequena no regime usual, mas não a arredondamos a zero nem calculamos significância. O limite Ωr=0 recupera degenerescência **exata** matéria+Λ por H0 e Ωm livres. Um residual não nulo com radiação fixada não demonstra poder de cinco sigma, nem identifica uma assinatura local de lente.

## 5. Priors e dado discriminante

| Comparação | Resultado de identificabilidade do fundo |
|---|---|
| H0,Ωm,Ωr livres, flat closure; mesmas leis geométricas | Reparametrização exata; distâncias sozinhas não identificam β |
| Sem radiação, H0 e Ωm livres | Exatamente equivalente a ΛCDM de matéria+Λ |
| Fonte default, T_CMB/N_eff fixos externos, H0/Ωm livres | O mapa exato sai da família; falta quantificar o residual após ajuste e a precisão admissível |
| Ωm/Ωr ou H0 fixados aos mesmos números por convenção | Diferença condicional a essas fixações; não é teste com nuisances livres |
| Priors realmente independentes sobre H*, densidades físicas, T_CMB/N_eff | Podem quebrar a liberdade; propagar origem, covariância e transformação H0↔H* |
| Priors extraídos de dados já ajustados assumindo GR | Não são independência automática; é necessário reavaliar a likelihood sob cada lei |
| Assinatura fotônica local ou polarizada adicional | Não é absorvida por esta prova sobre H; exige lei própria e teste de identificabilidade R2 |

Em famílias equivalentes, um contraste de evidências bayesianas causado apenas por priors não transformados não é uma nova diferença de predição: acompanhar o Jacobiano e a interpretação física dos priors. A assinatura útil poderá ser a combinação com observáveis físicos independentes ou a lei local de propagação; não a simples comparação de distâncias com os mesmos parâmetros nus fixados. A análise não escolhe q_TGL e não faz nenhum composto observado.

**Conclusão:** a lei escrita permite a reparametrização exata do fundo ampliado e de todas as suas distâncias de lente. A implementação default carrega uma restrição adicional de radiação que precisa ser mantida explícita. Fecho, parâmetros físicos e priors decidem qual comparação está sendo feita; só depois cabe calcular poder.
