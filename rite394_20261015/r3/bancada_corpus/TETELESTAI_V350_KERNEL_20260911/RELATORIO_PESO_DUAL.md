# Integral da ação dual: avanço e obrigações restantes

2026-09-11T22:49:55-03:00. [REAL — quatro módulos compilados na cópia isolada; escopo de revisão no parecer.]

O avanço é a construção de integrais fortes finitas e de sua avaliação positiva ampliada
na mesma representação regular. **Ainda não é o peso dual canônico nem o traço do core.**
Nenhuma flag de core, canto, H1/H2/H3 ou testemunha completa foi quitada por este incremento.

Para X positivo, foram construídos

    T_R(X)v = ∫[-R,R] θ_s(X)v ds,
    q_X(v) = (1/(2π)) ∫ℝ ofReal(Re⟨v,θ_s(X)v⟩) ds.

O primeiro integral é Bochner em vetores. Ele produz um operador limitado, com norma
≤ 2R‖X‖ para R≥0, e pertence à mesma álgebra de von Neumann dos integrandos. Não foi
pressuposta integração Bochner de θ_s(X) na norma de B(H).

[REAL — Lean] Positividade e monotonicidade dos cortes em R; permanência no mesmo core;
T_R(ι(a))=2Rι(a); aditividade de q em entradas positivas; invariância q_θr(X)=q_X;
igualdade da avaliação de T_R com integral escalar restrito; e, sem hipótese de finitude,

    q_X(v) = sup[n∈ℕ] (1/(2π))·ofReal(Re⟨v,T_n(X)v⟩).

Para todo v≠0, q_I(v)=∞. Logo esse limite não é um estado normalizado nem foi promovido
a supremo limitado em B(H). A expressão foi definida para toda entrada usando ofReal;
as leis de peso aqui verificadas têm explicitamente entradas positivas.

[INPUT — convenção implementada; DERIVED — compatibilidade de Fourier na nota]
A constante é (2π)⁻¹ para Lebesgue dt e caracteres exp(−ist). Ela não depende de R.
Seu valor foi escolhido segundo a medida dual da convenção adotada. O arquivo Lean
ainda não prova o teorema de Fourier que identifica essa medida dual.
[Fonte primária: Hiai, Teorema 10.13](https://arxiv.org/pdf/2004.02383#page=96).
[Pesquisa e derivação de sinais](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/DUAL_WEIGHT_CONSTRUCTION.md>).
Multiplicar τ por uma constante positiva preserva a lei de escala. A tabela anterior
de sinais em CONVENCOES_DO_TRACO.md fixava densidades compatíveis, não a constante.
Fixar adicionalmente τ(P)=1 é uma escolha que requer conferir a normalização usada.

## O que continua faltando para o traço

1. Construir o cone positivo ampliado e colocar o integral nele; identificar os pontos
   fixos da ação dual com a imagem da álgebra de base. A família finita não está em geral
   nessa imagem. As leis quadráticas em v e sua semicontinuidade ainda não foram formalizadas.
2. Exibir domínio finito denso, provando a identidade dos integrados e a semifinitude.
   A existência de cortes positivos não fornece esse domínio por si só.
3. Compor com o peso fiel normal da base e identificar seu grupo modular na mesma
   realização. Preservar um estado e normalizar uma álgebra não basta para essa identificação.
4. Construir o operador afiliado A com Λ_t=A^it e a perturbação
   τ=(φ̃)_{A⁻¹}; provar fidelidade, normalidade, semifinitude, propriedade tracial e
   τ∘θ_s=e⁻ˢτ. Essa é a rota publicada; tais etapas não foram quitadas em Lean aqui.

Depois vêm o canto dos Three Locks com 0<τ(P_F)<∞, H1/H2/H3 compatíveis, setor quântico
interagente e o contrato dependente consumido pelo gate. O contrato antigo de core ainda
precisa ser fortalecido: o contraexemplo de traço zero permanece válido e não passa Three Locks.
[Peças da torre já existentes e próximo passo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/ROTA_APOS_CORTES_DUAIS.md>).

## Evidência da integração

25 registros Lean integrados válidos; 48 controles Python
aprovados; 5922 declarações distintas no Audit, com axiomas
limitados a propext, Classical.choice e Quot.sound. Os controles novos verificam que
a integral ampliada não quite o traço e que a unidade infinita não quite o canto finito.

Base original SHA-256 `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`.
Cópia experimental SHA-256 `cb7b87f8f64a7bb0483767809d6712d1d381c6530c24d733de87473a5d2ba7b1`.

| Fonte integrada | SHA-256 lido do arquivo |
|---|---|
| StrongOperatorIntegral | `7ee0e23dc3319a72734ce420f540251f59a27561fa61221d6ab5f98b2989dfa7` |
| DualWeightCuts | `cad8c916c67f1329afbac42658d13e8930e065e8f6a69152d4c9caf93cedd91b` |
| DualWeightForm | `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4` |
| DualWeightExhaustion | `b09270078d8522f00acddd75b90a36f92b332330521aaec3253087414555c697` |

[Revisão independente e seus limites](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_WEIGHT_CUTS.md>).
A revisão das fontes e a integração pelo autor são evidências distintas; a abrangência
exata das recompilações independentes está no parecer. O incremento não recebe uma
declaração de revisão da execução integral: ela continua pendente.

Os arquivos originais não foram alterados. Logs das tentativas que falharam foram preservados.
A compilação é incremental com dependências verificadas; não houve execução integral do
monólito, transposição canônica ou publicação. O objetivo integral continua ativo.


## TETELESTAI_V350_DUAL_CLOSED_FORM_20260911 — 2026-09-11T23:24:34-03:00

[REAL — Lean em cópia] `DualQuadraticLaws` e `DualClosedForm` compilados e integrados:
homogeneidade e paralelogramo em ENNReal, semicontinuidade inferior por supremo dos
cortes, domínio finito construído como submódulo, subníveis fechados e invariância
unitária pelo comutante da mesma álgebra. D(q_I)={0} e D(q_0)=H. Não foi assumida
densidade universal de D(q_A). Semifinitude do peso exige trabalho sobre seu domínio
na álgebra, não essa densidade para cada forma.

27 registros Lean válidos, 50 controles aprovados,
5937 declarações distintas no Audit, axiomas no trio.
Base `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia `80d168b66d543803444f970aaebbc18030ceeeaaaaff6ec13b1ca42549f4c0c0`.
Corpo Python/gate inalterado em relação ao incremento anterior, conferido por AST.
[Relatório](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/RELATORIO_FORMA_DUAL_FECHADA.md>).
[Revisão independente e escopo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_CLOSED_FORM.md>).

[OPEN] Representação espectral/cone ampliado da base e pontos fixos; peso fiel normal
semifinito, afiliação do gerador/perturbação/traço, Three Locks, H1/H2/H3 físicos,
setor interagente/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
A construção de forma fechada não quita o traço. Não há novo selo ou transposição.
O objetivo integral segue ativo.
