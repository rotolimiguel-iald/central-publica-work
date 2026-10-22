# Controle de expectativa renormalizada negativa — entrega

[REAL — Lean] RenormalizedNegativeExpectation passou: 15 teoremas, 5 definições, 20 auditorias de axiomas, dois processos com exit 0 e zero warnings. As dependências axiomáticas das declarações auditadas estão contidas em propext, Classical.choice e Quot.sound. Namespace: ChatgptAudit.RenormalizedExpectation.

[Fonte congelada](<C:/IALD/Central de Patentes/Chatgpt/EXPECTATIVA_RENORMALIZADA_20260909_205808_979024/RenormalizedNegativeExpectation.lean>): 6.795 bytes; SHA-256 dad879cc61883be717ac47b94b9955f3e8ec65e788de9f8453f8d73d2f81b81c.
[Recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/EXPECTATIVA_RENORMALIZADA_20260909_205808_979024/BUILD_20260909_210306_180323/BUILD_RESULT.json>): biblioteca transposta 93 aprovada, fronteira medida e preservada. O escopo é compilação da nova folha e de seu importador, não reconstrução integral das dependências canônicas/Mathlib.

## Resultado matricial

[REAL — Lean] O vetor ψ=(2√2/3,−1/3) é tratado em EuclideanSpace C (Fin 2), com norma igual a um. A densidade complexa ρ=ψψ† é PosSemidef e tem traço um. Suas probabilidades diagonais são 8/9 e 1/9.

Para a matriz Hermitiana O=[[0,√2],[√2,4]], o kernel verifica Tr(ρO)=−4/9 e Tr(ρ(O+I))=5/9. Além disso, O+I=B†B para B=[[1,√2],[0,√3]], de modo que a matriz deslocada é positiva semidefinida. Não se afirma que o observável O seja positivo.

A norma, a densidade positiva, a Hermiticidade e as expectativas usam tipos complexos reais da biblioteca, sem premissas que assumam os valores das expectativas. A instância ComplexOrder fornece a ordem parcial adequada ao certificado matricial; não ordena os complexos como uma reta.

## Restrição da família positiva

[REAL — Lean] unsigned_gibbs_null_nonnegative deriva T(v,v)≥0 para a soma finita covetorial em uma direção g-nula quando os pesos são não negativos e k_j>0, de modo que c_j=k_j/(πcosh²k_j)>0. unsigned_gibbs_excludes_negative_value prova que esse valor não pode ser −4/9.

unsigned_gibbs_record_null_nonnegative aplica o mesmo resultado ao recordSource do gibbsRecord existente. A identidade utilizada é a soma de quadrados T(v,v)=Σ_j weight_j c_j (w_j(v))². Não há alteração nos sinais da fonte anterior, nem novo coeficiente negativo disfarçado.

[DERIVED — interpretação] A positividade de um estado não obriga todos os seus observáveis a terem expectativa positiva. Por outro lado, a parametrização covetorial Gibbs com coeficientes positivos restringe a fonte à condição nula não negativa. Se uma aplicação quiser representar respostas renormalizadas negativas, precisará justificar a identificação observável e a ampliação da família. Esta folha não prova que O seja a componente nula de um stress de QFT, nem que uma cinética negativa seja física.

## Identificação externa ao Lean

[DERIVED — escrito] A nota [IDENTIFICACAO_FOCK_ESCRITA.md](<C:/IALD/Central de Patentes/Chatgpt/EXPECTATIVA_RENORMALIZADA_20260909_205808_979024/IDENTIFICACAO_FOCK_ESCRITA.md>) demonstra no domínio de suporte finito do oscilador que a compressão de :(a+a†)²: à base |0>,|2> é O. A inclusão do vetor é isométrica e preserva sua expectativa. A restrição de a+a† à saída |1>,|3> tem matriz B, explicando O+I=B†B.

A nota distingue compressão do quadrado e quadrado da compressão: E†(a+a†)E=0 nesse subespaço de paridade par, mas E†(a+a†)²E=O+I. Nenhuma relação CCR de dimensão finita é postulada.

[KNOWN — contexto, não premissa da prova matricial] [C. J. Fewster, Lectures on quantum energy inequalities](https://arxiv.org/abs/1208.5399) trata expectativas renormalizadas negativas e restrições para médias em QFT. O artigo foi consultado apenas com consulta genérica; nenhum conteúdo privado foi enviado.

[OPEN] Não formalizamos Fock/QFT completo nesta folha, não identificamos automaticamente esse observável com a energia gravitacional da TGL e não concluímos falsificação ou confirmação da teoria. A densidade é pura de posto um; não se declara fiel ou invertível em M₂(C).

## Preservação

[REAL — operação local] Todos os arquivos desta entrega nasceram em pasta nova Chatgpt. As duas correções locais receberam backups imediatos em bytes e substituição por arquivo temporário verificado; as tentativas de build foram preservadas. Fonte congelada após o PASS. Nenhum um.py foi executado ou importado e nenhum original, memória canônica ou módulo congelado anterior foi alterado.

Este relatório registra análise do autor da folha e medições locais; não atribui aprovação independente a terceiros.
