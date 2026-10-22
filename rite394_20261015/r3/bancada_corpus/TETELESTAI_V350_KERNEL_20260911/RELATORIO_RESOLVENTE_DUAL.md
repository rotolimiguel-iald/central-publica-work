# Resolvente dos cortes duais e domínio finito

2026-09-12T00:25:03-03:00. [REAL — Lean incremental em cópia; revisão independente delimitada.]

Foi construído o limite forte R dos inversos (I+C_n)⁻¹ dos cortes normalizados
efetivos C_n=(2π)⁻¹∫_[-n,n] θ_s(A)ds. Para A positivo no core regular já construído,
R pertence à mesma álgebra, satisfaz 0≤R≤I e é o ínfimo dessa família no ambiente
de operadores limitados. Não se presume uma cota inferior estritamente positiva.

## Ligação que foi provada

Para cada vetor v da representação original:

    q_A(Rv) ≤ ‖v‖²/4 < ∞; portanto Ran R ⊆ D(q_A).

A cota vale para a integral dual efetiva, não para uma forma definida a posteriori
com o nome q. O fator (2π)⁻¹ é o mesmo dos cortes e da integral. Sua identificação
como normalização de Haar dual via Fourier continua na pendência já registrada.

O caso A=I dá R=0, pois D(q_I)={0}. O caso A=0 dá R=I. Os resolventes finitos
são injetivos; a prova não transfere essa propriedade indevidamente ao limite.
Isso conserva a parte infinita da forma, em vez de apagá-la por uma hipótese de
domínio denso universal.

## Passos da prova

1. Positividade de C garante que I+C é uma unidade estritamente positiva. Sua
   inversa é positiva, menor ou igual a I e inverte a ordem entre C e D.
2. O cálculo direto dos comutantes mostra que o inverso permanece na álgebra.
   A família I-(I+C_n)⁻¹ é crescente, positiva e limitada. O teorema de convergência
   monótona já existente produz seu limite forte; o fechamento WOT o mantém na
   mesma álgebra. Subtrair esse limite de I produz R e a propriedade de ínfimo.
   O lema abstrato aceita índices preordenados, dirigidos e não vazios; a aplicação
   aos cortes usa os intervalos inteiros de exaustão.
3. A equação (I+C_n)r_n=v implica
   Re⟨r_n,C_n r_n⟩=Re⟨r_n,v⟩-‖r_n‖²≤‖v‖²/4 por Cauchy–Schwarz.
   Para m≤n, o corte C_m tem energia menor que C_n. Fixando m e passando ao limite
   forte de r_n, a continuidade da forma limitada de C_m preserva a cota.
4. Tomar o supremo em m recupera exatamente q_A(Rv), pelo lema de exaustão.
   Não se trocam limites de duas variáveis nem se subtraem valores infinitos.

## O que ainda falta no caminho do gate

[OPEN] A inclusão Ran R⊆D(q_A) ainda não é a representação espectral da forma.
É necessário provar a identificação variacional/espectral completa, incluindo
o suporte correto (por exemplo ker R=D(q_A)⊥), a igualdade da forma com o operador
não limitado e os domínios correspondentes. Não foi construído ainda um operador
não limitado auto-adjunto representando q_A, nem uma medida espectral nova.

[Rota variacional](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/ROTA_VARIACIONAL_DO_RESOLVENTE.md>):
argumento de trabalho [DERIVED], ainda não formalizado nem revisado independentemente,
para a etapa seguinte. Não faz parte da evidência compilada desta entrega.

[OPEN] Depois: cone ampliado da base/pontos fixos; domínio e semifinitude do peso
operadorial; estado modular da base; gerador afiliado, perturbação e traço canônico
fiel normal semifinito com escala dual; Three Locks no mesmo modelo; H1/H2/H3 físicos
compatíveis; setor interagente/BRST/QME/anomalias/UV; contrato dependente ampliado;
runtime integral. Nenhuma das seis flags abertas foi quitada por este incremento.

O gate principal da v350 não lê essas flags de fronteira. Além de cumprir as provas,
é necessário fazer a decisão consumir o contrato compatível que as reúne. A subdecisão
experimental existente continua apenas com o alcance modular anteriormente provado.

## Evidência

19 alvos novos impressos no auditor; 33 registros Lean
integrados válidos; 54 controles Python aprovados;
5981 declarações distintas no Audit com axiomas no trio.
735 arquivos embutidos. Compilação incremental e auditoria
de hashes; a execução integral do monólito continua pendente.

| Módulo integrado | SHA-256 lido |
|---|---|
| PositiveResolvent | `28a29b66c00b67f696a8a8f27dfc8e19dc28de0f16c96ec64e299a9b6143ebd1` |
| DualResolvent | `ee5ee31d1788cde0420e74d571e86ddddb86cb9ed5d7744eec74999a682fbcd2` |

Base SHA-256 `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`.
Cópia SHA-256 `74d56693da1d66981c85b98d587cc355986fbbea09432a3dc2009374aa9c1df6`.

[Parecer independente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_RESOLVENT.md>). O parecer delimita o que recompilou
e o que conferiu por inspeção da integração do autor. As falhas históricas de elaboração
foram preservadas, fora da evidência aceita. O controle adicional verifica que limite
forte e domínio finito não sejam promovidos a certificado de peso, traço ou Three Locks.

Corpo Python/gate igual por AST ao estrato anterior; original preservado por hash.
Objetivo integral ativo. Não houve novo selo, transposição canônica ou confirmação física.


## TETELESTAI_V350_DUAL_SUPPORT_OPERATOR_20260912 — 2026-09-12T01:00:45-03:00

[REAL — Lean em cópia] `DualVariational`, `DualFormSupport`, `ResolventGraph`
e `DualSupportOperator`: F_v(Rv)≤F_v(w), ker R=D(q_A)⊥,
closure(Ran R)=closure(D(q_A)); restrição R_K injetiva no suporte construído;
operador positivo auto-adjunto T, com domínio denso em K e (I+T)⁻¹=R_K.
O teorema existencial final constrói R e T a partir de A≥0 do mesmo core.
O suporte da forma não é o projetor Three Locks. Não há hipótese de
injetividade global, densidade universal ou auto-adjunção pronta.

37 registros Lean, 55 controles,
6006 declarações distintas no Audit, axiomas no trio.
Base `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia `74424b54d411b248074a971135391fd1b3f2add9c270b9e829d35c20eb2aeb9b`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/RELATORIO_SUPORTE_E_OPERADOR_DUAL.md>).
[Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_SUPPORT_OPERATOR.md>).

[OPEN] Igualdade da forma com a raiz quadrada de T e domínios correspondentes;
cone ampliado da base/pontos fixos; peso semifinito, estado modular, gerador
afiliado, perturbação e traço; Three Locks, H1/H2/H3, interações/BRST/QME/
anomalias/UV, contrato ampliado e runtime integral. As seis flags abertas
continuam falsas. Objetivo integral ativo; sem confirmação física.

Adendo à rota variacional: as etapas 1–3 antes DERIVED agora têm os teoremas
compilados descritos acima. A etapa 4, representação completa da forma,
permanece OPEN. O registro anterior é histórico e foi preservado.

[REAL — compilação local, fora da integração e da revisão desta etapa]
`DualEnergyOnResolvent.lean` já compilou a identidade de energia em Ran R;
integração, revisão e ligação aos domínios completos continuam pendentes.
[Checkpoint do próximo trabalho](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/next_energy_checkpoint.json>).
