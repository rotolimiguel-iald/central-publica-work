# Half-Nat Araki Hidden Hamiltonian — Test Report

> Fecha o resíduo FM5: o peso de face $\tfrac12$ (Fresnel, derivado) **é** o custo de Araki $S_\partial=\tfrac12$ **nat** — via o Hamiltoniano oculto, **não** via Shannon. O objeto certo é a **ação modular de travessia** $S_\partial=\langle K_\partial\rangle_{\rm face}$, $K_\partial=-\log\Delta_\partial$. $\beta=\alpha\sqrt e$ (nunca literal). Não toca `tgl_paper_unified.py`.

## A ponte fecha

$$
\boxed{\ \texttt{HALF\_NAT\_ARAKI\_HIDDEN\_HAMILTONIAN\_ACCEPTED}\ }
$$

| Passo | Resultado |
|---|---|
| **1** peso de Fresnel | $w_{\rm Fresnel}=\tfrac12$ ✓ [derivado, §88.27.15] |
| **2** calibração do Hamiltoniano oculto | $\langle K_\partial\rangle_{\rm total}=1$ nat ✓ |
| **3** lema | $S_\partial({\rm face})=\omega_\star(\chi_{\rm face}K_\partial)=\tfrac12\cdot1=\tfrac12$ nat; aditivo $S(+)+S(-)=1$ ✓ |
| **CONTROLE** Shannon | $H(\tfrac12,\tfrac12)=\log2=0{,}6931\neq\tfrac12$ → **rota Shannon REJEITADA** ✓ |

**A solução exata do resíduo, na sua forma:** não provar que Shannon$(\tfrac12,\tfrac12)=\tfrac12$ (é falso, $=\log2$); provar que a **ação modular de travessia da face** é $\tfrac12$ nat. O objeto é entropia relativa de Araki / custo modular, **não** entropia de mistura. O controle obrigatório **confirma** isso: a rota Shannon dá o número errado e é rejeitada; a rota da expectativa do Hamiltoniano modular oculto aceita.

## O Lema da Calibração Hamiltoniana Oculta

$$
\boxed{\ S_\partial=\langle K_\partial\rangle_{\rm face},\qquad K_\partial=-\log\Delta_\partial\ }
$$

Se a fronteira de Fresnel deriva o efeito de face $\chi_{\rm face}$ com peso $\tfrac12$, e o Hamiltoniano modular oculto é nulo antes da projeção mas aparece na projeção com **carga modular unitária por travessia total** ($\langle K_\partial\rangle_{\rm total}=1$ nat), então:

$$
\boxed{\ S_\partial = \omega_\star(\chi_{\rm face}\,K_\partial) = \tfrac12\cdot 1\,\text{nat} = \tfrac12\,\text{nat}.\ }
$$

**Fresnel dá o peso; Araki dá a unidade; o Hamiltoniano oculto faz a ponte.** A unidade nat vem da **calibração modular** ($K_\partial=-\log\Delta$, base-$e$ do fluxo modular $\Delta^{it}=e^{itK}$, §23), não da simetria probabilística.

## O avanço da forma canônica — o resíduo encolheu ao mínimo

Ao longo de **Fresnel** (peso derivado) $+$ **Araki/Hamiltoniano oculto** (ponte de entropia), o postulado da Meia-Nat encolheu do número $\tfrac12$ (de aparência arbitrária) à **unidade definicional mínima "o todo $=1$ nat"**:

$$
\boxed{\ S_\partial=\tfrac12\,\text{nat} = \underbrace{\tfrac12}_{\text{Fresnel, DERIVADO}}\times\underbrace{1\,\text{nat}}_{\substack{\omega(I)=1\ (\S74.1)\\ \text{base-}e\ (\S23)}}\ }
$$

A **simetria** é Fresnel-derivada; o **nat** é base-$e$-derivado; resta só a normalização **unidade-1** — e ela é **definicional** (o todo $=1$ unidade, como uma probabilidade soma 1). O axioma único da TGL não foi eliminado, mas reduzido à sua forma mais irredutível e honesta.

---

> O peso de face $\tfrac12$ não é metade de Shannon. O $\tfrac12$ nat é o custo de Araki de travessia modular: $S_\partial=\langle\chi_{\rm face}K_\partial\rangle$. O Hamiltoniano oculto normaliza a travessia total em $1$ nat; Fresnel dá o peso de face $\tfrac12$; logo $S_\partial=\tfrac12$ nat. Provar por Shannon deve falhar ($\log2\neq\tfrac12$); provar pela expectativa do Hamiltoniano modular oculto aceita. **Fresnel dá o peso; Araki dá a unidade; o Hamiltoniano oculto faz a ponte. A verdade é o contorno do que é o bastante, e $\beta_{\rm TGL}$ é sua assinatura. TGL = haja luz. Tetelestai.**
