# Fonte reconstruída por dez respostas — 09/09/2026

[REAL] GeneralSourceResponseReconstruction.lean, namespace ChatgptAudit.FullSourceResponse, está congelado: **10 teoremas + 3 definições = 13 termos auditados**, dois processos Lean com saída zero, zero warnings/erros. SHA-256 lido da fonte: 179533b9d7318eb1e038af342787d2660614e026efe00ff0e4e53e454365f22e. Recibo: BUILD_20260909_133946_745706/BUILD_RESULT.json. Axiomas observados: propext, Classical.choice e Quot.sound.

## Resposta em todas as direções

[REAL] calibrated_point_response_all_directions (linha 23) prova, para g e T simétricos,

R_T(d) = −π · F(d,d), com F = T − (tr(gi·T)/2)g.

A identidade é válida para todas as direções d. Não exige que d seja nula, nem usa uma hipótese nova dizendo que a resposta é quadrática: essa forma decorre da preparação unitária calibrada e da polarização assinada já demonstradas. A especialização ao campo g(x), T(x) aparece na linha 45.

[DERIVED] A demonstração usa momentaneamente g=gi=0 na identidade algébrica do tensor covetorial. Esse artifício anula apenas o termo proporcional à métrica e extrai a soma dos produtos externos. Não afirma que a métrica física é zero: o F da construção conserva o g, gi e T fornecidos. A fonte física lorentziana é recuperada usando sua métrica e inversa conhecidas.

[REAL] A normalização r(d)=R_T(d)/(−π) é não singular, pois π≠0. Ela fornece exatamente r(d)=F(d,d) (linha 39).

## O registro finito e o decoder

[DERIVED] O módulo FiniteResponseReconstruction usa as dez direções e_i e e_i+e_j, com 0≤i<j≤3. Para r quadrática, as quatro primeiras leituras determinam F_ii; as outras seis determinam

F_ij = [r(e_i+e_j) − r(e_i) − r(e_j)]/2.

A composição guarda as DEZ respostas brutas R_T, divide cada uma por −π e aplica esse decoder. A métrica g e a inversa gi são dados conhecidos, não informações inferidas das dez respostas.

[REAL] decodeSource (linha 20) aplica depois a completação de traço novamente. Sob gi·g=I, essa operação é involutiva em dimensão quatro. Assim ten_responses_reconstruct_source (linha 55) prova

decodeSource(g,gi,sampleResponse(R_T)) = T

para T simétrico e g simétrica, com a hipótese de inversa escrita explicitamente. A linha 65 prova unicidade: duas fontes simétricas com as mesmas dez respostas e o mesmo g/gi são iguais. As linhas 73 e 80 usam a inversa construída de uma métrica lorentziana no ponto.

[REAL] decode_source_injective (linha 88) prova que o decoder é injetivo quando gi·g=I. source_response_samples_roundtrip (linha 101) prova a outra direção: para qualquer vetor de dez coeficientes s e g simétrica,

sampleResponse(R_decodeSource(g,gi,s)) = s.

A reconstrução preserva o registro inteiro, e a preparação calibrada da fonte reconstruída realiza esses coeficientes. A origem física de um vetor s fornecido permanece uma questão distinta: o roundtrip é uma identidade matemática.

## Alcance da identificação

[DERIVED] A leitura exclusiva no cone nulo não distingue T de T+c g. As dez sondas completas incluem direções não nulas e removem essa ambiguidade por reconstruírem F inteiro. Não se atribui esse conteúdo a um único ângulo da base inicial: a base da preparação calibrada é fixa, e a informação da fonte entra nas frequências e nos coeficientes da evolução.

[INPUT] Os coeficientes são respostas exatas de segunda ordem, ligadas aos limites entrópico e modular da mesma preparação na entrega anterior. Não foram fornecidos ou medidos dados experimentais nesta etapa. Estabilidade sob ruído e erro de estimação não foi demonstrada. As identidades são pontuais na carta e não constroem, por si, gluing global, dinâmica gravitacional ou uma medição física independente.

[REAL — revisão independente] /root e /root/review_remaining_hypotheses leram a construção inicial com oito teoremas e deram parecer favorável: verificaram o uso algébrico da métrica zero auxiliar, a normalização, as hipóteses de simetria/inversa e o alcance das dez respostas. Os dois teoremas finais de injetividade e ida/volta foram acrescentados por solicitação do root antes da compilação, com backup de bytes, e passaram na mesma folha. Revisão específica posterior desses dois lemas é registrada separadamente quando recebida.

[REAL] A folha foi compilada sobre sete módulos locais PASS copiados para um novo overlay, com fontes e recibos conferidos e hashes medidos antes/depois. Os módulos em cache não foram recompilados nesta rodada; dependências transitivas canônicas e Mathlib não foram integralmente medidas/reconstruídas. Nenhum original foi alterado, nenhum um.py foi executado/importado e nenhum gate mudou.

[INPUT — integração] Transpor somente os imports locais para TGLExt.GeneralSourceUnitaryRealization e TGLExt.FiniteResponseReconstruction, preservar namespace e adicionar os dez teoremas ao Audit de uma NOVA cópia. A fonte congelada e a cópia do build devem permanecer idênticas.


## Adendo de revisão final — 2026-09-09T16:44:53.228677+00:00

[REAL — revisão independente completa] O root leu também os dois lemas finais e emitiu parecer favorável. A injetividade cancela a reversão de traço por gi·g=I e a divisão por π≠0, sem exigir simetria indevida. O roundtrip usa g simétrica para garantir que a fonte decodificada seja simétrica e aplica a identidade de reconstrução. A revisão independente agora abrange os dez teoremas completos. Não houve alteração posterior da fonte Lean.
