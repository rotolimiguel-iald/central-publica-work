# Interação local somável: resultado e alcance
[REAL — Lean compilado e revisão semântica independente favorável] 09/09/2026.

Foram construídos três módulos novos: 58 teoremas e 12 outras declarações, 70 termos auditados. Os dois primeiros compilaram juntos em build limpo; a interface tipada compilou importando cópias dos binários PASS com hashes conferidos. Os cinco processos Lean desses dois recibos terminaram com exit0, sem warnings; axiomas somente propext, Classical.choice e Quot.sound. O root leu as três fontes e aprovou seu alcance. Fontes congeladas.

## O objeto construído

No Hilbert e no fator canônicos da torre, B_j=X_jX_(j+1) é auto-adjunto, tem quadrado I e norma no máximo1. Para coeficientes reais com Σ|c_j| finito:

V_N=Σ_(j<N)c_jB_j,  V=Σ_jc_jB_j,
‖V−V_N‖≤Σ_(j≥N)|c_j| →0,
‖V_N‖≤Σ_j|c_j|,  ‖V‖≤Σ_j|c_j|.

Essas conclusões decorrem dos operadores e das somas efetivos. V não é um campo abstrato que assume “completamento quântico”.

- SummablePauliInteraction.lean:111 prova a convergência dos prefixos;:127 o bound do limite;:146 o erro de corte;:153 o desaparecimento da cauda;:165 o bound uniforme.
- PauliInteractionWitness.lean:43 prova que B_j está fora do centralizador se P.w j≠1/2. O teste usa A=Y_jX_(j+1): BA=iZ_j, AB=−iZ_j; suas expectativas diferem.
- PauliInteractionWitness.lean:133 e:166 provam [[B_j,Z_j],Z_(j+1)]=−4Y_jY_(j+1)≠0. O não zero é deduzido do quadrado I do produto YY e da norma1 do vetor hOmega.
- A mesma fonte:180–217 constrói c_j=1 quando j=0 e0 nos demais sítios, prova a somabilidade e V=X0X1. Esse V concreto carrega ambas as testemunhas.

## Interface e ressalvas essenciais

AdmissiblePauliInteraction.lean:12 exige SummableCouplingData: valores mais prova de somabilidade absoluta. certifiedInteraction:16 e certifiedPrefix:19 recebem esse dado, e os teoremas:34–52 entregam convergência, bounds e cauda. singleBondData:22 possui certificado construído e os teoremas:58–69 conservam as testemunhas físicas do modelo no alcance declarado.

A soma infinita de Mathlib é uma função total: fora da somabilidade, seu valor padrão não certifica convergência. Por isso os teoremas incondicionais de auto-adjunticidade/pertencimento do núcleo não devem ser usados isoladamente como interface física; a entrada certificada elimina essa ambiguidade de uso.

Os vínculos XX comutam entre si. O resultado demonstra acoplamento entre sítios e, sob a condição do perfil, exclusão do centralizador. Não afirma uma família de vínculos mutuamente não comutantes. A exclusão do centralizador não é afirmada no caso tracial; a testemunha do duplo comutador continua válida.

## Próximo teorema

[OPEN] Construir o cociclo da perturbação da dinâmica modular e sua estimativa de Duhamel uniforme no fundo, para transportar a remoção do corte do potencial à dinâmica. No caso finito, o candidato é exp(it(H+V))exp(−itH), com hipóteses hermitianas, e depois u'_N=i u_N α_t(V_N). A família de potenciais desta entrega fornece o dado real V_N necessário; o cociclo ainda não foi construído neste lote.

[KNOWN — referência examinada pelo root, não formalizada aqui] REFERENCIA_MODULAR_IMPORTADA.md registra a rota de Araki para relacionar perturbação e estado modular. Nenhum estado perturbado ou identificação de seu grupo foi introduzido como campo pressuposto nos novos tipos.

[INPUT/OPEN] Perfil, sítios, couplings e somabilidade são entradas declaradas. Relação com regiões físicas, tensor de matéria, métrica e relógio físico necessita sua própria composição. O controle ℓ¹ é de interação limitada nesta classe, não UV relativista, renormalização completa ou ausência de anomalias.

## Revalidação e custódia

O mapa anterior da rota está em MAPA_MODULAR_UV.md e a dedução prévia permanece intacta. O JSON de entrega registra bytes, hashes e mtime medidos do programa/índice e de todas as ordens PARA_CHATGPT; nenhuma ordem posterior à010 foi localizada na conferência. O programa permaneceu no v337 lido; a cópia28 continua baseada no snapshot v336. O índice atual declara uma rodada intermediária com9ritos reaproveitados; seu campo de última rodada completa custodiada não apaga a rodada v336 anteriormente documentada.

A correção de navegação foi comunicada ao root: ContinuousModularReconstruction.lean:155 já prova a raiz positiva auto-adjunta com quadrado/domínio; essa conclusão formal não deve ser reaberta pela frase histórica do índice. Identificação do fluxo físico é outra questão.

Falhas anteriores e backups de bytes permanecem na pasta. Nenhum um.py foi executado/importado; nenhum original, fonte congelada anterior ou gate foi alterado. A entrega ainda não foi integrada ao programa.
