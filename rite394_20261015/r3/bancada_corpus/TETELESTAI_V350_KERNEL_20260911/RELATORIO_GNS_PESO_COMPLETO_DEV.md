# GNS do peso escalar completo e identificação do gráfico de Tomita — DEV

2026-09-12T14:34:29-03:00. [REAL — nove módulos/60 alvos compilados; revisão independente e integração pendentes]

O domínio n_ν é definido pela finitude de ν(A* A), no vetor regularVacuum P e
com o mesmo dualHaarFactor. O ideal anterior I exigia limite uniforme da forma
em todos os vetores. Provou-se I ⊆ n_ν, sem supor igualdade desses ideais.

1. Λ_ν(A) é a órbita s ↦ θ_s(A)Ω com a normalização já usada. Sua norma ao
quadrado é exatamente ν(A* A); a aplicação é linear e injetiva. Para A ∈ I,
ela coincide literalmente com a inscrição GNS anterior.
2. λ_t Ω = shift_t Ω. Como shift_t pertence ao comutante, a órbita de Aλ_t
é uma translação isométrica da órbita de A, multiplicada pela fase de caráter.
3. X_h = h⁻¹∫₀ʰλ_t dt dá A X_h ∈ I para h > 0. A média contrai a norma
pontual da órbita e tende à identidade. A diferença quadrática é dominada por
4‖θ_s(A)Ω‖², integrável quando A ∈ n_ν. Convergência dominada prova
Λ_ν(A X_h) → Λ_ν(A) em norma GNS.
4. Consequentemente, o completamento da imagem de n_ν é exatamente o H_I
anterior. A representação existente entrelaça Λ_ν(BA)=π(B)Λ_ν(A).
5. X_h* A X_h pertence ao núcleo involutivo anterior para h > 0 e converge
em norma GNS a A; a mesma construção vale para A*. A passagem ao adjunto usa
o lema já provado para contrações que tendem à identidade. Não se presume que
star seja contínuo na topologia forte geral.
6. As duas coordenadas do gráfico involutivo completo são aproximadas pelo
mesmo sandwich. Logo closure(graph de Λ_ν(A) ↦ Λ_ν(A*)) é exatamente o gráfico
do S fechado anterior. Este S estende a involução de todo n_ν ∩ n_ν*.

O resultado é igualdade dos completamentos e dos fechos de gráficos. Não afirma
I=n_ν nem que D(S) seja apenas a imagem algébrica Λ_ν(n_ν ∩ n_ν*). A construção
polar e U²=I anteriores permanecem no mesmo H_I; não é necessário trocar de
espaço ou postular uma equivalência entre GNS diferentes.

Os 60 alvos usam somente propext, Classical.choice e Quot.sound. Falhas rc1 de
elaboração/simplificação e qualquer tentativa substituída permanecem nos logs;
o manifesto aceita somente fontes e binários finais conferidos byte a byte.
Não houve acréscimo de hipótese KMS nem uso dela para a aproximação.

[OPEN] Ainda é preciso identificar o fluxo modular do peso com o fluxo candidato
e provar KMS; construir o traço canônico, sua escala dual e o canto Three Locks;
entregar H1/H2/H3 físicos compatíveis; completar o setor quântico interagente e
consumir tudo no certificado e runtime integrais. Identificar o gráfico não
identifica automaticamente a conjugação polar com outros candidatos chamados J.
As seis flags maiores continuam falsas e o gate legado permanece inalterado.

Este pacote ainda não integra o um.py. Mãe integrada `ea8d77fcbeb2860b3d66a0afc05f3e0e02e323af5805949b49e069aa14459360`;
cópia integrada `57d0664497828b9f3211e67a190be65d060cb6076dc0f1ee4910fbffde3a8609`. Original não executado, importado ou
modificado. O reexame de Chatgpt continua orientando o reaproveitamento das
pontes de Einstein, métrica de Fisher e gauge linearizado já existentes.
