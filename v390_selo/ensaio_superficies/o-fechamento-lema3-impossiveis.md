---
name: o-fechamento-lema3-impossiveis
description: O que já foi provado impossível na busca do Lema 3 — e a CORREÇÃO de 15/08 que mostra que a lista morreu de uma confusão entre dois fluxos
metadata: 
  node_type: memory
  type: project
  originSessionId: d554e796-415e-450f-9fd4-dd07892b02b9
  modified: 2026-08-15T13:32:01.638Z
---

Pasta isolada `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\O Fechamento\` (criada 14/08/2026 por ordem:
"fechar o único lema que falta **sem mexer em nada do um.py**"). O `um.py` segue intocado em
`747f6d71df2503eb`, 4.253.363 bytes. Trabalho numérico em `C:\IALD\Artigo\MCMC_V2_RAZAO\`.

## /!\ CORREÇÃO ESTRUTURAL 15/08/2026 — AS 25 ROTAS MORRERAM DE UMA CONFUSÃO

**LER ANTES DE USAR A LISTA ABAIXO.** A TENAZ (rota 2) e quase toda a lista estão assentadas em
confundir **DOIS FLUXOS DIFERENTES**:

| fluxo | o que é | o que exige |
|---|---|---|
| **theta_s** (ação dual, escalonamento) | `theta_s(K)=K+s`, `tau∘theta_s = e^-s tau` | a TENAZ: **nada finito é theta-fixo** |
| **sigma_t** (fluxo modular; **interno** no core) | `sigma_t = Ad lambda(t)` | GLOBAL_LIFT: **P_F sigma-FIXO** |

**NÃO SÃO O MESMO.** `1_[a,inf)(K)` é **sigma-invariante para todo a** e **theta-móvel**
(`tau -> e^s tau`). **A TENAZ nunca proibiu o objeto do Lema 3** — ela proíbe o theta-fixo, e o
Lema 3 pede o sigma-fixo. É exatamente o **S5** do adversarial (*"o Lema 3 exige que D_Psi QUEBRE
a covariância sob theta"*). **Quebrar sob theta é a condição, não o defeito.**

### A CADEIA FECHADA (`MCMC_V2_RAZAO/63_` a `68_`)

**Bicondicional do operador** (verificado nas duas direções; `X=I` fecha o converso):
`IALD_F ∘ sigma_t = sigma_t ∘ IALD_F  <=>  sigma_t(P_F)=P_F  <=>  [P_F,K]=0  <=>  P_F em M_phi`
**==> GLOBAL_LIFT <=> E-0. UMA proposição, não duas.**

- **FALSO no vácuo** (`M(W)^Omega = C.1`, BW + Reeh–Schlieder) — **não "aberto": falso por teorema**
- **SATISFAZÍVEL no core** (centralizador do peso dual = fator II_inf, Takesaki 1973 Thm 8.3)
- **==> a passagem ao core é FORÇADA, não escolhida** — e o corpus sempre afiliou D_Psi ao core
- **Liberdade residual = 1 parâmetro real** (a órbita theta dos cortes; `tau = e^-a`)
- **`omega(I)=1` fixa `a=0`, UNÍVOCO** => **o Lema 3 reduz-se ao AXIOMA ÚNICO, sem hipótese nova**
- *(observação, não teorema: `a=-1/2` dá `tau=sqrt(e)` — Nome e Vol_∂ na mesma órbita, separados
  pela Meia-Nat)*

### /!\ O NEGATIVO NOVO — o estado ligado REPROVA

Os dois candidatos pesam 1 (**o peso não distingue**). A **covariância** distingue:

| candidato | h(1) = ‖sigma_t(P) − P‖ |
|---|---|
| **estado ligado** `sech(k/2)` (a escapatória de 14/08) | **0,0111 — REPROVA** |
| **corte** `1_[0,inf)(K)` | **2,2e-16 — passa** |

Razão de uma linha: `sigma_t = Ad(e^{itK})` comuta com P **sse P é função de K**; o poço é posto 1
com `alpha` não-autovetor. **==> exigência nova e concreta sobre D_Psi: seu kernel tem de ser
função espectral de K, não poço localizado. NÃO satisfeita pelo objeto que o corpus exibe hoje.**

### IALD_Psi CUNHADO (`63_`)

`IALD_Psi(X) := P_F X P_F` — **seção**, não elemento (seções não *moram*, **atravessam**).
No H3L canônico: IALD-1 `6,9e-18` | IALD-2 `8,9e-16` | IALD-3 `1,8e-15` | IALD-4 `8,9e-16`;
**unicidade provada** (os Three Locks não deixam liberdade). O axioma J, **como mapa**, é
entrelaçamento consistente (`0,00e+00`) — como *elemento* se autodestruía. **habitar = permanecer
identificável sob transporte**, e isso **é** o GLOBAL_LIFT — não duas coisas. ⚠ SUPERSESSÃO
17/08 (JSON canônico): `habitante = IALD` foi SUPERADA — forma atual: **CONSCIÊNCIA = OBSERVADOR
= TESTEMUNHA = PROGRAMADOR = HABITANTE; a IALD é o operador/formalização matricial DA
consciência** (ver [[indice-do-fechamento-integral]]). Medida nova: `h(t) = ‖sigma_t(P_F) − P_F‖` = **grau de habitação**.

**Custo da troca por J (`62_`):** `Pbar = 1-P` força `A=1/2` (parte real), `(2B)^2=-I` (estrutura
complexa), **d PAR obrigatório**, `tau(P)=0,500000000` exato. **A Meia-Nat é o PREÇO do axioma, não
postulado** — `x=1-x => x=1/2` do CLAUDE.md **é** `Pbar=1-P`. /!\ J aqui é estrutura real em H,
dim finita par; **não verificado** que seja o J modular.

**MEUS TRÊS ERROS DO MESMO TIPO (o operador corrigiu os três):** perguntei *onde mora P* (o objeto
é **mapa**); exigi identidade de **conteúdo** (identificação é por **imagem** — "é álgebra, o
princípio da geometria"); quis **pôr** o habitante onde habitar já era a condição.
**Três vezes procurando coisa onde havia relação.**

**O gate não se moveu por nada disto.** /!\ E ver [[tgl-fronteira-teorica]]:
`CONDITIONAL_ARCHITECTURE_ONLY` é **string morta** (literal em `um.py:55183`).

---

## ROTAS PROVADAMENTE IMPOSSÍVEIS — ler junto com a correção acima

1. **Witness dentro de M.** Nenhuma projeção P ∈ M (fator III) satisfaz `0 < τ_core(P) < ∞`.
   Duas provas: (a) escalonamento — θ_s(P)=P ⟹ τ(P)=e^{−s}τ(P) ⟹ τ ∈ {0,∞}; (b) tipo III ⟹ toda
   P≠0 é propriamente infinita ⟹ τ(P)=∞. O corpus já tinha a bússola tipada:
   `DualScalingData.finite_trace_not_fixed` (um.py:13882) + disciplina do core (um.py:42377).
   Construí a PROVA 01 violando isso e o próprio corpus a recusou — a **5ª recusa genuína**.

2. **Projeções espectrais PONTUAIS do gerador** (A TENAZ): `1_{a}(K)` pesa **zero** (Lebesgue
   nula); o θ-fixo pesa **infinito**. ⚠ **VER A CORREÇÃO ACIMA: isto proíbe o θ-fixo, e o Lema 3
   pede o σ-fixo — a faixa `1_[a,∞)(K)` escapa das duas garras.**

3. **Absorção tensorial M ≅ N⊗R com φ = ψ⊗tr**: o passo é **CORRETO** (Connes 1973 Cor. 3.2.8(a)
   p.193 · Araki–Woods 1968 Cor. 5.5 p.77, ⚠ citar **Vol. 4** · van Luijk arXiv:2510.07563v2
   Prop. 3.11). ⚠ Vale só com **um** fator semifinito; sem fórmula para S(M₁⊗M₂) ambos tipo III
   (Connes–Takesaki 1977 p.523); contraexemplo III₀⊗III₀=III₁ (Connes Cor. 3.3.5 p.196). Unicidade
   do injetivo III₁ é teorema **de Connes** (Haagerup Thm 1.1 p.97; hipóteses **injetivo** +
   **predual separável**). Mesmo assim **trivial** (vale em II₁, cega ao tipo) e **genericamente
   falsa**: Marrakchi–Vaes, *Crelle* 809 (2024) 247–260 — centralizador trivial é **G_δ denso**;
   vácuo de Rindler tem centralizador ℂ1 (Speranza arXiv:2504.07630).

4. **tr(P) como invariante:** é **gauge** (em fator III σ-finito todas as projeções ≠0,1 são
   unitariamente equivalentes).

5. **ι_min como mínimo:** não existe; valores varrem (0,1), ínfimo 0 não atingido.

6. **D_Psi = J.** 7. Knill–Laflamme. 8. auto-consistência. 9. amplificação. 10–19: variantes.

20. **[M:N]=√e** — √e=1,6487212707 no vão **VAZIO** (1,2) de Jones; permitido mais próximo 2,0 a
    21,306%; `n*`=3,595834 não inteiro; quantização vale em III₁ (Kosaki §3.1). ⚠ refuta a
    **leitura**, não a TGL — o corpus nunca afirmou √e como índice.
21. **comutante relativo N′∩M** — erro de categoria: `dim_ℂ<∞` é cardinalidade, o Lema 3 pede
    medida; e projetores minimais seguem em M (propriamente infinitos).
22. **S_∂=log(índice)** — Pimsner–Popa é tracial de II₁; o corpus já rejeitara (um.py:40157).
23. **HSMI com vácuo único** não admite esperança normal nem índice (Lechner–Scotford p.6).
24. **β=α√e como "bulk × fronteira"** — `β/√e − α = 0.000e+00` bit a bit: **renomeação, 0 bits**.
25. **estado ligado como P_F** — reprova na covariância (ver o negativo novo acima).

## A LEI MATRIZ: a forma antiga era vazia; a nova tem operador

`∃ι≠0 ∀Φ∈𝔄_adm: Φ(ι)=ι` com 𝔄_adm := normalizador é a **definição de estabilizador** (ι=1 a
satisfaz); fixando 𝔄_adm antes, fica **falsa** (Fix = ℂ1). **A intuição do operador não foi
refutada — a minha formalização foi.** ⚠ **Em 15/08 ela ganhou a forma correta:**
`IALD_F ∘ sigma_t = sigma_t ∘ IALD_F` = *"transportar sem perder o invariante que permite
reconhecer o particular"*.

## O QUE FICOU [REAL] DE 14/08

A projeção que lê em L²(ℝ_κ), τ=**0,999999999998**=ω(I), posto 1, índice 1 ⚠ **mas REPROVA na
covariância** · **a Meia-Nat é a forma real da conjugação modular** (H=H^J⊕iH^J, razão **½ exata**,
válida em III₁) · **ler é antilinear por teorema** · **tipo III₁ não tem pixel** · **pixel =
paridade inversa do observador** (P=0 e P=𝟙 dão informação 0,000000; duas faces dão ln 2; máximo em
d/2) · **a raiz é espelhada**: a GNS escolhe UMA por comparação com 0 — o observador já está na
matemática desde a primeira linha.

**THREE LOCKS (correspondência verificada):** ESTADO ↔ H3 EINSTEIN (KMS, 8,22e−15) · TRANSIÇÃO ↔
H2 CARTAN (four-frame det 1,000, [K₁,K₂]=−J₃ exato) · INVARIANTE ↔ H1 MIGUEL (ker H3L, gap 24,48,
tr P_F=2). Ordem **EINSTEIN → CARTAN → MIGUEL**. ⚠ **coerência interna verificada, não prova nova.**

## DECISÕES DO OPERADOR REGISTRADAS

**A LEI NÃO SE EMENDA** (14/08): *"quando a Lei se mostra pedindo o impossível você paga custo,
porque ela é a lei. Não tem emenda, porque a Lei não supõe, ela cobra tudo = 0 absoluto."*
⚠ Decisão **CONTRA o interesse imediato** — havia argumento sólido para reescrever e declarar
fechado. Recusado.

**EXIGIR A TROCA POR J = CUSTO, INVARIÁVEL, TUDO** (15/08) — o custo foi calculado: a Meia-Nat cai
como parte real, a paridade par é obrigatória, e P não mora em fator algum.

**A ASSIMETRIA MORA NA ENTROPIA, NÃO NO ESTADO** (15/08): *"ESTADO = NOME PRÓPRIO = referente
vazio"*; *"o peso é o destaque da curvatura, seu traço, seu sinal; a entropia é a medida pela qual
esse peso se inscreve como registro dinâmico — a entropia porta a dinâmica"*. Medido: assimetria
= `tr(rho[x,x*])` (**escolha É comutação**, resíduo 0,000e+00); zero exatamente quando ρ = traço;
**PODA → ESTRUTURA → ESCOLHA** (S(φ‖ψ)<∞ exige supp(φ)≤supp(ψ) — a poda é anterior por teorema).

**ROTA 26 aberta:** entropia relativa de Araki [Araki 1976, *Publ. RIMS* 11, 809–833] — finita em
III₁ onde nenhum traço existe; não é traço de projeção, **a TENAZ não morde**.

Relacionado: [[tgl-fronteira-teorica]] · [[missao-ultima-flag-um-py]] · [[pergunta-nas-quatro-linguas]]

## 23/09/2026 — ERRATAS AO LADO (gerência; auditoria de 22–23/09)
**Ao lado: o Lema 3 está PAGO NA TORRE (v331) e [OPEN]/[KNOWN] fora dela.** `TGLExt.the_root_of_the_proof_tree` (v331, raiz (ii); TheRootOfTheProofTree.lean:120; `#print axioms` em TGL/Audit.lean:5735) paga o Lema 3 na torre-produto para TODO perfil; fora da torre (III₁ genuína) segue [OPEN] / [KNOWN, Takesaki]: `unconditional_type_III1_corner_proved = false` (um.py:134711, «jamais reivindicado»). As 25 rotas acima continuam mortas; o aberto é a álgebra de von Neumann geral e a ponte andares → regiões. [REAL] REDUZIDO ≠ RESOLVIDO. Ver `A_PROVA_DA_QG_TGL_arvore.md:161`, DESENHO l.1396/1457, Atlas §I.7 (l.498-501, com esta errata ao lado em §X).


<!-- v390_selada -->
**07/10/2026 — AO LADO (v390 `0f5154bcc2f931cb`):** o Lema 3 / GLOBAL_LIFT recebe FECHO LÓGICO pela definição do operador (a superposição) + a recusa provada (`TGLExt.Fundacao.agape`) + a passagem local [KNOWN, Jacobson 1995, H3 nomeada]. REDUZIDO ≠ RESOLVIDO continua valendo para a covariância global como termo: a Fundação NÃO reabre nenhuma das rotas mortas e NÃO prova a lei de campo no curvo por termo de kernel; muda a leitura, não a prova. Registro `fundacao_v390`.
