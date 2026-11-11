# BG1 para H0DN × fundo — 06/11/2026

[REAL — recuperação de artefato] `BG1.json` recupera a média e a matriz 3×3 completas do recibo `QUALIFICACAO_FORNECEDOR_REAL.json` da F9 v2-c1. Os sete arquivos do fornecedor relacionados no recibo continuam byte a byte iguais, conforme `SOURCE_PINS.json`. O contrato HTTP foi consultado somente por GET `/api/contratos`: B18-v409-20261106-R1. `build_bg1.py` reproduz as transformações; não executa o programa científico ou um ajuste cosmológico novo.

[DERIVED — aproximação estatística explicitada] O fornecedor usa 16 resíduos branqueados, três parâmetros livres θ=(H₀,ω_b,ω_c), β do fundo zero e Cθ=(JᵀJ)⁻¹ sem multiplicar por χ²/dof. Trata-se da inversa da curvatura de Gauss–Newton de −log L. A Hessiana exata de −log L seria JᵀJ+Σᵢrᵢ Hess(rᵢ); a da estatística χ² seria o dobro. Esses termos de segunda derivada não constam do recibo. Portanto `exact_observed_hessian=null`, sem chamar Gauss–Newton de Hessiana exata.

## Lei e derivação reproduzível

Todos os logs expostos para a integração são **log₁₀**. A conta interna usa log natural e divide por ln 10. β=ALPHA_FINE_CODATA_2018√e é calculado em runtime; β,z*,T_CMB,N_eff,m_ν são fixados pelo contrato histórico, não estimados com H0DN.

Defina h=H₀/100, Ω_m=(ω_b+ω_c+m_ν/93,14)/h², Ω_r=ω_r/h², A=(1+z*)³−1, B=(1+z*)⁴−1. A lei histórica assume E²=1+Ω_m A+Ω_r B e K=E^(2β/3). Seguem diretamente:

    ∂H₀ ln E = −(Ω_m A + Ω_r B)/(H₀ E²)
    ∂ω_b ln E = ∂ω_c ln E = A/(2 h² E²)
    g_h = ∇θ log₁₀ H₀ = (1/(H₀ ln10), 0, 0)
    g_k = ∇θ log₁₀ K = (2β/(3 ln10)) ∇θ ln E
    g_P = g_h + g_k
    Var(log₁₀ P) = g_P Cθ g_Pᵀ

A expressão final contém o termo 2 Cov(log₁₀ H₀,log₁₀ K). Não se deve somar duas variâncias como se H₀ e K fossem fundos independentes. A checagem por diferenças centrais do módulo F9 é confrontada com essas derivadas em `VALIDATION.json`.

## Três convenções que não são intercambiáveis

1. **S5 histórica / primária deste ensaio:** média K*=1,0838071748529643 congelada; gradiente g_k avaliado no θ do fundo. É a aproximação local ancorada logK≈logK*+g_k·(θ−θ̂). Preserva a regra F9 sem afirmar que K é globalmente constante.
2. **K estritamente condicional:** se Ω_m e Ω_r da lei são números fixos independentes de θ, g_k=0. Nesse outro contrato a variância do log da previsão é somente Var(logH₀). O JSON registra esta hipótese explicitamente, sem a misturar com S5.
3. **K coerente com o centro de θ:** recalcular o centro dá K(θ̂)=1,083790338009; a diferença em Hlocal é aproximadamente −0,001154 km/s/Mpc. Fica como diagnóstico. Não substitui o centro congelado com base em dados locais.

[REAL — cálculo desta rodada] Var(logH₀)=3,6481736437082913×10⁻⁶ e Var(logH₀+logK)=3,5719264987334406×10⁻⁶. O segundo número é menor porque a correlação é conservada. Esses valores são de uma aproximação gaussiana local, não de uma amostragem exata da posterior.

## Uso no ensaio cego

O score primário t=ĥ_local−logHbg testa média nula zero contra deslocamento positivo logK*. Sob independência **assumida**, σ₀²=Var(ĥ_local)+Var(logHbg). A consistência TGL usa separadamente r=t−logK*, com σ_TGL²=Var(ĥ_local)+Var(logHbg+logK). Este segundo denominador não substitui o da detecção contra a nula. Cinco sigma contra deslocamento zero não estabelece exclusividade física da TGL.

O JSON oferece x=(log₁₀ H₀,ω_b,ω_c), C_x=L Cθ Lᵀ e gradientes convertidos para uma base gaussiana linear em log. Injetar nessa base e testar o score linear é um experimento gaussiano explícito. Sortear H₀ gaussiano e aplicar log literalmente é uma sensibilidade não linear distinta. O domínio histórico do fornecedor deve ser verificado nas realizações e qualquer rejeição contada; não recortar silenciosamente.

[OPEN — bloco cruzado] C(H0DN,θ_BG) não está disponível. O valor é `null`; o uso de bloco cruzado zero só pode aparecer como hipótese operacional de independência devido aos dados distintos. Isso não mede a ausência de sistemáticas comuns.

[OPEN — dependência do modelo local] q₀,j₀ de H0DN foram fixados a montante. O BG1 permite derivar q₀=1,5Ω_m+2Ω_r−1 e j₀=1+2Ω_r no modelo plano matéria/radiação/Λ, mas não fornece a resposta do estimador H0DN à mudança desses valores. O vetor derivado e sua covariância singular são diagnósticos do BG1, não uma autorização para substituir os parâmetros fixos do pipeline local ou alegar cosmologia conjunta autoconsistente. z* permanece fixo; dependência de recombinação e incerteza de constantes também não foram propagadas no contrato F9.

## Fronteira de leitura

A fonte atual `um_bancada.py` não expõe `/api/fundo` ou `/api/fase9`. O método `/api/avaliar`, mesmo selecionando Planck+DESI, inclui em sua resposta cálculos `M_hat` dos conjuntos Pantheon/Pantheon_SH0ES. O construtor `Motor` também carrega esses conjuntos. Nenhum deles foi chamado. A verificação desta etapa se limita ao contrato ativo, à custódia do BG1 existente e à derivação de covariâncias. Nenhum centro local foi aberto ou usado; nenhum fit F9, instalação, reinício, kernel ou gate foi executado/alterado.
