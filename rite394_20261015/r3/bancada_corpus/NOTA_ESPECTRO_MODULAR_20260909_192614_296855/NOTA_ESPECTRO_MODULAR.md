# Espectro modular: correção de alcance necessária no artigo

[REAL — leitura] As versões do parágrafo em um.py, linhas 146392 (EN) e 146394 (PT), afirmam que o espectro modular é puramente contínuo e, por isso, não há autovetor ou instante estacionário. O contexto trata do tipo III₁, exterioridade modular e fluxo de pesos. Não há restrição explícita a Ω⊥, ao complemento do centralizador ou a estados não estacionários. A frase seguinte reconhece o centralizador como setor fixo, mas não qualifica a afirmação de ausência de autovetores.

## Testemunhas canônicas

1. ModularPower.lean:49, modularFlow_fixes_omega: para todo SiteProfile P e t real, modularFlow P t (hOmega P) = hOmega P. TowerHilbert.lean:53, hOmega_norm, prova ‖Ω‖=1. ModularPower.lean:27/30 define e caracteriza a potência imaginária modular construída. Logo há um vetor estacionário não nulo explícito na mesma torre.

2. ModularFlowSpectrum.lean:66, delta_eigenvector: os vetores locais E_ij da torre pertencem ao domínio de Δ e satisfazem Δξ_ij=λ_ijξ_ij, com λ_ij=towerW(i)/towerW(j)>0. A linha 74, modularFlow_eigenvector, prova Δ^{it}ξ_ij=exp(it logλ_ij)ξ_ij. A linha 98, localEigenvectors_total, prova que seu span é denso em TowerHilbert P. A construção possui uma família total de autovetores, não apenas Ω.

3. Mesmo excluir somente Ω não resolve a inexistência de vetores estacionários: ξ_j=(P_j−p_jI)Ω é ortogonal a Ω (SitePhaseCovariance.lean:90), tem norma ao quadrado p_j(1−p_j)>0 (:132/:137) e é não nulo (:141). [DERIVED] P_j é diagonal no sítio, portanto sua ação modular é fixa; junto à invariância de Ω, isso fornece Δ^{it}ξ_j=ξ_j. Esta composição é explicação escrita, não teorema novo compilado nesta nota.

## Diagnóstico

[DERIVED] A inferência é falsa no alcance em que foi escrita. Continuidade forte de t↦Δ^{it}, espectro total como conjunto, natureza pontual/contínua da medida espectral, exterioridade e periodicidade do fluxo de pesos são propriedades distintas.

Uma família total de autovetores pode coexistir com um espectro topológico dado pelo fecho de autovalores densos. Isso não torna a medida espectral puramente contínua. Um automorfismo exterior não precisa mover cada vetor ou elemento; um grupo global não periódico pode ter vetores fixos e modos próprios.

Redação segura proposta: “A exterioridade e a ausência de período global não implicam ausência de modos estacionários. Na torre produto canônica, Ω é fixo e os vetores locais formam uma família total de autovetores modulares. Deve-se distinguir o espectro total do operador, seu espectro pontual e os invariantes do fator.”

A identidade geral conhecida ΔΩ=Ω na representação padrão também contradiz a ausência universal de autovetores; as testemunhas principais desta nota são, porém, os enunciados concretos já existentes no kernel.

## Limites

É uma inconsistência matemática/editorial localizada entre a narrativa e seus próprios objetos formais. Não é refutação da TGL inteira, não altera critérios falsificadores, não reabre teoremas corretos e não move gate. As outras afirmações sobre corrida de α, fluxo de pesos e exterioridade universal não foram auditadas aqui.

Nenhum original foi modificado. um.py foi apenas lido como bytes/texto, nunca executado ou importado. Não houve recompilação nesta subtarefa. Os hashes medidos estão no manifesto; os enunciados citados não são apresentados como nova auditoria Lean.
