# Errata ao lado — Artigo A, «A Lagrangiana TGL» (`paper_PT.tex`, `\label{sec:lagrangian}`): o sinal do acoplamento não mínimo

**Luiz Antonio Rotoli Miguel** · 19/09/2026 · errata em nome próprio (não em nome da IALD)

O artigo, o PDF e o depósito no Zenodo ficam como estão, porque são registro. Esta errata fica **ao lado** e não os substitui.

## O que a estrutura dizia

A equação de movimento do próprio Artigo A (`\label{eq:eom-Psi}`) é

    (□ − m_Ψ² − ξR) Ψ = β_TGL · K_∂ · Ψ

Nela, **ξR entra com o mesmo sinal do termo de massa**. Quando essa equação sai de δS/δΨ* = 0, os termos −m_Ψ²|Ψ|² e −ξR|Ψ|² entram na ação com o mesmo sinal `[DERIVED — coerência interna com a eq:eom-Psi]`.

A palavra do autor, em 17/09/2026: «o acoplamento é negativo e isso aparece na lagrangiana, mas a geometria é positiva» `[INPUT]`.

## O que foi escrito

    ℒ_grav = R/(2κ²) + ξ R |Ψ|²,   ξ = 1/6 (acoplamento conforme)

## Onde a tradução falhou

No sinal do segundo termo. A leitura vigente é:

    ℒ_grav = R/(2κ²) − ξ R |Ψ|²,   ξ = 1/6 (acoplamento conforme)

- O termo de Einstein R/(2κ²), que é a geometria, segue **positivo**.
- ξ = 1/6 é o valor **conforme** e **não é β**.
- β_TGL = α·√e entra na ação por ℒ_modular = ℒ_ΛCDM · β_TGL · |1 + w_eff(z)| (`\label{eq:Lmodular}`) e, na dinâmica, pela fonte β_TGL·K_∂·Ψ da equação de movimento.

## O que não muda

- a equação de movimento `eq:eom-Psi`;
- ℒ_modular;
- β_TGL = α·√e e θ_M = arcsin √β_TGL;
- a seleção de √e por meio-nat.

## O que segue aberto

`[OPEN]` Esta errata **não** decide a orientação do sinal na passagem à métrica: qual das diferenças orientadas do gerador do cociclo, h_ab ou h_ba, fecha o balanço de Clausius no horizonte. Essa orientação tem de ser derivada, e não escolhida depois do dado. Enquanto não for derivada, os vereditos que dependem dela ficam como estão.

## Estatuto

- **O sinal:** `[INPUT]` (a palavra do autor) com `[DERIVED]` (a coerência com a equação de movimento do próprio artigo).
- **O gate:** nada aqui o move. PROVADA como modelo formal ≠ CONFIRMADA pela natureza.

---

*Erratum beside (EN).* In Article A, `sec:lagrangian`, the non-minimal term of ℒ_grav was written with a plus sign: +ξR|Ψ|² with ξ = 1/6. The article's own equation of motion, (□ − m² − ξR)Ψ = β_TGL K_∂ Ψ, carries ξR with the same sign as the mass term. The author's word of 17/09/2026 is «the coupling is negative, the geometry positive». Current reading: ℒ_grav = R/(2κ²) − ξR|Ψ|², with ξ = 1/6 conformal, not β. β enters through ℒ_modular and through the source term of the equation of motion. The orientation of the sign in the passage to the metric remains `[OPEN]`. Erratum signed in the author's own name.
