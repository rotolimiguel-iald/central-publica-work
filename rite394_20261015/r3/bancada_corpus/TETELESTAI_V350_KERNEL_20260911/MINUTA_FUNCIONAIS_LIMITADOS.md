# Funcionais limitados dominados pelo peso escalar

{date}. [REAL — Lean compilado na cópia, revisão independente delimitada]

Para o mesmo core N, o mesmo peso ν e a mesma normalização c=(2π)⁻¹,
os cortes duais C_R são mapas complexo-lineares contínuos de operadores.
O funcional ψ_R(A)=c⟨η,C_R(A)η⟩ é complexo-linear limitado para todo R.
Para R≥0 é positivo: sua avaliação num operador positivo é real e
não negativa, não apenas uma parte real de sinal não negativo.

No cone positivo de N, Re ψ_R≤ν para R≥0. Nos raios naturais,
ν(A)=sup_n Re ψ_n(A), com as avaliações finitas incluídas em ENNReal.
O supremo pode ser infinito. Não se afirma ψ_n(1)=1 ou fidelidade de
cada corte. A normalização de Haar permanece a já fixada no peso.

Foi provado o critério de convergência monótona para essas avaliações:
se A_i é rede positiva crescente, dirigida e não vazia em N, com
supremo interno B, então Re ψ_R(A_i)→Re ψ_R(B). A prova constrói
o limite forte na mesma N antes de aplicar a continuidade dos cortes.
Não recebe convergência forte como hipótese final. A convergência
vale para R arbitrário; a positividade do funcional requer R≥0.
Não se construiu uma nova interface predual nem uma equivalência
Lean geral entre esse critério e todas as definições de normalidade.

[REAL — evidência da integração] Três módulos/{target_count} alvos novos,
{build_count} registros Lean válidos (incluem dependências herdadas),
{controls} controles, {audit_count} declarações distintas Audit e
{embedded_count} arquivos embutidos. Os axiomas dos alvos pertencem ao
trio `propext`, `Classical.choice`, `Quot.sound`. As recompilações
próprias do revisor e a inspeção da integração têm escopos diferentes,
descritos no [parecer](<{review_path}>).

Base `{base_sha}`; cópia `{working_sha}`. Só o conteúdo Lean embutido
muda nesta etapa: a AST Python restante é igual à custódia precedente.
O gate legado e as seis flags maiores continuam inalterados. O controle
novo exige as declarações e impede sua leitura como Tomita/KMS/traço.
O original não foi importado ou executado; não houve runtime integral.

[OPEN] Falta provar a fechabilidade do gráfico de Tomita deste peso:
(0,y)∈fecho(G)⇒y=0. Domínio escalar máximo, operador fechado, dados
modulares/KMS e traço canônico com escala dual permanecem abertos.
Também faltam as interfaces gerais necessárias, Three Locks/H1,
identificação geométrica H2, aplicação correta de H3, setor quântico
interagente e certificado completo efetivamente consumido pelo gate.

Os dois módulos posteriores de mapas GNS de corte são desenvolvimento
separado, sem revisão ou integração neste parecer. Eles não entram
nas contagens acima nem fornecem, por si, a prova de fechabilidade.
