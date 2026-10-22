# Registro finito de resposta quadrática
[REAL — compilação medida; DERIVED — reconstrução algébrica; INPUT — lei de resposta quando se quer interpretar todos os argumentos]

O módulo preserva a interface do registro do root. Um registro contém dez números reais, nas direções e₀,e₁,e₂,e₃,e₀+e₁,e₀+e₂,e₀+e₃,e₁+e₂,e₁+e₃,e₂+e₃. Para q(d)=dᵀAd com A simétrico, as quatro primeiras amostras recuperam Aᵢᵢ, e as outras seis recuperam Aᵢⱼ=(q(eᵢ+eⱼ)−q(eᵢ)−q(eⱼ))/2.

O lema novo quadratic_response_samples (linha 33) reutiliza tensorQuad_components do kernel canônico. Ele calcula uma única vez os dez coeficientes, evitando expandir repetidamente somas matriciais.

decode_quadratic_response (linha 71) prova que decodificar as amostras da forma quadrática de um tensor simétrico devolve o próprio tensor. sample_decoded_response (linha 117) prova a volta para qualquer registro de dez números reais. decoded_response_symmetric (linha 28) certifica a simetria do resultado. A injetividade e a equivalência de igualdade entre registros e tensores simétricos seguem desses dois retornos (linhas 143–155).

finite_response_reconstructs_given_tensor (linha 157) e reconstructed_quadratic_matches_all_directions (linha 163) conservam explicitamente a hipótese q(d)=tensorQuad A d em todas as direções. Dez valores de uma função arbitrária não provam, por si, que ela é quadrática fora dos pontos amostrados.

## Alcance

As amostras são coeficientes reais exatos, sem hipótese de positividade, assinatura Lorentziana ou não degenerescência. O decoder sempre produz um tensor simétrico; essas propriedades adicionais dependem de certificados próprios. As direções não recebem restrições causais ou de pertença a um cone nulo; o registro não é uma leitura apenas do cone nulo.

O módulo é uma equivalência algébrica em um referencial conhecido. Não contém preparação microscópica, postulado de medição, lei gravitacional, confirmação empírica ou fechamento quântico. Sua composição com a resposta unitária geral deve demonstrar que as amostras pertencem à mesma lei de resposta e fornecer a métrica quando a conversão por reversão de traço a exigir.

## Correção e custódia

As definições do root e seus enunciados foram preservados. Acrescentou-se o lema de dez coeficientes; corrigiu-se o congrArg para aplicar sampleResponse após tensorQuad. As provas dos retornos agora reduzem explicitamente os componentes antes de aplicar aritmética, pois a simplificação automática anterior deixava aplicações opacas de vetores Fin 10.

Cada edição teve backup imediato em bytes, seguido de arquivo temporário verificado e substituição. Todas as builds anteriores permanecem. Nenhum original canônico ou um.py foi alterado, executado ou importado. A compilação nova usa dependências TGLExt/Mathlib preexistentes, com hashes antes/depois das fontes e binários diretamente importados; não recompila nem mede toda a árvore transitiva.

A revisão semântica favorável do root examinou os mesmos enunciados e o novo lema antes da última correção dos passos de prova. Os resultados medidos e hashes estão no manifesto e no BUILD_RESULT.json indicado nele.

[REAL — medição final]

Build: BUILD_20260909_133559_200106/BUILD_RESULT.json. PASS_COMPILED_SCOPE; 10 teoremas + 4 outros termos = 14 auditorias, dois exits 0, zero warnings. Fonte 6495 bytes; SHA-256 cd7fcb5e26e37eeb6da8fee725ef0973673adbe58072b325e0c5da9447d28767.
