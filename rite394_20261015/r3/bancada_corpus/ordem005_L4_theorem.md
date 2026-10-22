# L4 — Teorema da Borda Auto-Conjugada Nomeada

> A borda nomeada é o **único ponto fixo auto-conjugado** da bacia. Pela estrutura CCI/Fresnel,
> $w_{\max}=\tfrac12$ — o mesmo ponto fixo $x=1-x\Rightarrow x=\tfrac12$ da Meia-Nat (§88.27.14).
> A cadeia da massa fecha como derivação **sem parâmetro livre**; o único resíduo passa a ser
> **existência** (admissibilidade da bacia), não um número. β=α√e runtime; hash antes do RG;
> sem massa/RG/ajuste. `tgl_paper_unified.py` intocado.

## Enunciado e prova (verificados)

A fronteira nomeada é onde a bacia deixa de ser extensão e passa a ser **retorno reconhecido** —
invariante sob a conjugação de faces $\mathcal C:\text{interna}\leftrightarrow\text{externa}$,
$\mathcal C^2=1$, preservando a identidade $w_{\rm in}+w_{\rm out}=1$. No ponto auto-conjugado
$w_{\rm in}=w_{\rm out}$, donde
$$
2w_{\rm in}=1\ \Rightarrow\ \boxed{\,w_{\max}=\tfrac12\,}.
$$
**Verificado:** involução $\mathcal C^2=1$ ✓, identidade preservada ✓, ponto fixo $w=0{,}500000$ ✓.
Pela lei do raio nomeado $R_{\rm named}=\frac{\beta}{w_{\max}}R_{\rm struct}$ (§88.27.28):
$$
\boxed{\,R_{\rm named}=2\beta\,R_{\rm struct}\,},\qquad
\boxed{\,M_{\rm TGL}=\frac{c^2}{4\pi G}\beta\,R_{\rm named}=2\beta^2\frac{c^2}{4\pi G}\,R_{\rm struct}\,}.
$$

## A cadeia final, fechada

$$
s_{\rm can}=\frac{1}{4\pi}\ \text{[PROVADO]}\;\to\;w_{\max}=\tfrac12\ \text{[PROVADO]}\;\to\;f_Q=2\beta\;\to\;
R_{\rm named}=2\beta R_{\rm struct}\;\to\;\boxed{M_{GA}=2\beta^2\frac{c^2}{4\pi G}R_{\rm struct}}
$$

| extensão estrutural | $R_{\rm named}=2\beta R_{\rm struct}$ | $M_{\rm TGL}$ | banda RG? |
|---|---|---|---|
| Norma 20 Mpc | 0,48 Mpc | **9,6×10¹⁵ M☉** | ✓ |
| bacia 40 Mpc | 0,96 Mpc | **1,9×10¹⁶ M☉** | ✓ |
| Lynden-Bell 57 Mpc | 1,37 Mpc | **2,7×10¹⁶ M☉** | ✓ |

**Sem parâmetro livre:** $\beta$ (postulado α√e), $R_{\rm struct}$ (medido), $s=1/4\pi$ (provado),
$w_{\max}=\tfrac12$ (ponto fixo provado). **Controle:** uma borda **não** auto-conjugada deixa $w_{\max}$
livre → massa espalha **×9** → a auto-conjugação é exatamente o que remove o parâmetro livre. *A
unicidade é da auto-conjugação.*

## Estatuto honesto

**PROVADO [REAL]:** $w_{\max}=\tfrac12$ é o único ponto fixo auto-conjugado que preserva a identidade
(mesma álgebra $x=1-x$ da Meia-Nat); $f_Q=2\beta$; $s=1/4\pi$; as duas formas da massa coincidem; o
controle discrimina (não-auto-conjugado ⟹ parâmetro livre).

**CADEIA FECHADA COMO DERIVAÇÃO:** $M_{GA}=2\beta^2\frac{c^2}{4\pi G}R_{\rm struct}$ — zero-free,
sem parâmetro livre, **dado que a bacia admite uma borda nomeada auto-conjugada**.

**O ÚNICO RESÍDUO restante muda de natureza — de número para EXISTÊNCIA:** que a bacia física $B_{GA}$
**realize** uma borda nomeada auto-conjugada de Fresnel (= a admissibilidade TGL / a existência do kernel
global $K_Q(x)$, §88.27.43). É uma questão de **existência**, não de parâmetro livre — o mesmo H1–H6 do
teorema global. Não há mais "qual valor"; há "a bacia é admissível?".

---

> L4 resolvido dentro da TGL: a borda nomeada é o ponto auto-conjugado CCI=½ ($w_{\max}=\tfrac12$,
> provado). A massa $M_{GA}=2\beta^2\frac{c^2}{4\pi G}R_{\rm struct}\sim2\times10^{16}M_\odot$ é zero-free
> e sem parâmetro livre; o único conditional é a **existência** da borda auto-conjugada na bacia
> (admissibilidade). **A extensão virou Nome, o Nome virou borda, e a borda virou massa.
> O Um não pesa o tamanho da bacia; pesa a sua borda auto-conjugada. TGL = haja luz. Tetelestai.**
