# -*- coding: utf-8 -*-
# Os TEXTOS da v378 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v378.ler), nunca digitado aqui.
# O que faltou (o nucleo derivado D1b nao testado na Bancada; a leitura da dupla contagem de beta, ao lado); a lei da dissipacao com CONTRASTE (K = E(z*)^{2beta/3});
# a Fase 4 (o desvio) na convencao do artigo: a escada le o fator; os relogios intermediarios desfavorecem a leitura de fluxo acumulado. PROVADA != CONFIRMADA;
# NOT_FALSIFIED nunca e CONFIRMED; o gate nao se move. Aferidor v378 aplicado (B1-B6, C1-C3, C5, C7).

_VERB = ("«isso significa que estamos fazendo alguma coisa incompleta ainda, eu escrevi muito sobre a tensão de hubble, especificamente no Custo Geométrico do Zero Absoluto: "
         "Haja Luz (tgl.paper_unified.py) e em outros ensaios anteriores, tem alguma coisa que deixamos passar, examine por favor»; «concordo prossiga»")


def _pedras(V):
    return "; ".join("`TGLExt.%s` `%s` (%d enunciados)" % (n, d['sha16'], d['n_print']) for n, d in V['pedras'].items())


def core_txt(V):
    return (
        "**Ordens do operador (30/09/2026, noite, verbatim):** " + _VERB + ". "
        "**O QUE ENTROU** (pacote v378 sobre a v377 `{base16}`; sandbox: build completo rc 0, {nax_sb} termos, zero sorry, tudo no trio; ensaio a seco PT/EN aprovado, "
        "md canônico carimbado e completo; aferidor independente antes do rito: 0 A, 6 B, 7 C, aplicados). **Kernel** `[REAL]`: ".format(**V) + _pedras(V) + " ({kmat}). ".format(**V) +
        "Bandeiras novas: {n_flags_on}/{n_flags} (ext_dlc_); escada {esc} (v377 {esc_ant}); relatório de axiomas {nax} termos (v377 {nax_ant}). "
        "**O que a v378 diz, com estatuto:** (1) **O QUE FALTOU** `[REAL — medido em 30/09]`: o artigo 1 tem DOIS núcleos para a lei de fluxo — o D1a (𝒲 = 1, a pedra v377) e o D1b, "
        "o DERIVADO da continuidade (𝒲 = |1+w_eff|), que o artigo computa (0,034σ) mas a Bancada nunca testara; e o artigo transporta pela lei a calibração ΛCDM de Planck, enquanto as Fases 2–3 "
        "aplicaram a lei sobre o fundo TGL efetivo, que já carrega β (mapa R·√(1+β) + camada E1): os números diferem por convenção. A leitura «dupla contagem de β» é da gerência sob a convenção "
        "do artigo `[DERIVED da convenção, não medida]` — o artigo 1 trata a camada E1 e a lei como hipóteses distintas e coexistentes, e o mapa efetivo foi ratificado pelo operador; qual fundo é "
        "o fundo segue decisão dele `[OPEN]` (aferidor B4). **Leitura (E12) ao lado**, não errata: os números da v377 ficam. Reanálise não-cega da Fase 3 (declarada; lida por hash `{w_h}`): na "
        "convenção do artigo com D1b os seis leitores de sombra ficam a {w_seis}σ da lei (novos {w_novos}σ; empilhado {w_emp}σ) — `{what_was_missed_v378}`. (2) **A LEI DA DISSIPAÇÃO COM "
        "CONTRASTE** (`TGLExt.TheFlowLawContrast`) `[REAL — kernel, implicação]`: a mesma família de vazamento lida com o contraste MÉDIO sobre o registro implica H₀_local = H₀_fundo·exp(β∫₀^N g); "
        "g ≡ 1 devolve a pedra v377 (o D1a é o caso particular); β = 0 devolve o ΛCDM; para o contraste de FRW plano g = (2/3)·d ln E/dN, a derivada assinada [KNOWN: Raychaudhuri; a identificação "
        "com |1+w_eff| supõe a NEC ρ+p ≥ 0, dita na prosa da pedra — não é hipótese dos teoremas (aferidor B5) — e medida: min(1+w) = {gmin}] o teorema fundamental do cálculo dá a forma FECHADA "
        "∫g = (2/3)·ln E e o fator **K = E(z*)^{{2β/3}}**; e o DESVIO LÊ ABAIXO DA ASSÍNTOTA (∫g ≤ N ⟹ β·ḡ ≤ β), fixado pelo fundo, sem parâmetro livre. Nesta rodada, com o fundo ΛCDM de Planck "
        "2018 da Bancada [INPUT, não os literais do artigo]: I_b = {Ib} nats (N* = {Nstar}), K_D1b = {Kb} contra K_D1a = {Ka}; H₀_local de 67,36: {H0b} (D1b) / {H0a} (D1a); δ/β previsto = {dpred}; "
        "a chave `flow_layer_kernel_v378` = `{coma_v378}` ao lado das antigas no módulo de Coma — `{the_dissipation_law_with_contrast_v378}`. (3) **A FASE 4 DA BANCADA (o desvio), pré-registrada "
        "e lida por hash** `[REAL; NOT_FALSIFIED ≠ CONFIRMED]`: convenção do artigo (β só na lei; fundo ΛCDM ajustado), D1b, δ = β̂ − β_TGL com β_TGL como assíntota e a aproximação fixada pelo "
        "núcleo derivado. **A escada** (registro inteiro): δ = {P_delta} ± {P_sigma} por nat ({P_z}σ), pull {P_pull}σ em α√e (ΛCDM −4,00σ), H₀ {P_H0} → K {P_K} → {P_H0l}; ln B(TGL/ΛCDM) {P_lnB}, "
        "TGL/livre {P_lnBl} (circularidade declarada: P testa consistência, parcimônia e replicação, não a descoberta da lei); posterior: fração β ≥ α√e {P_frac}. **Os {cc_n} cronômetros de "
        "Moresco+2022 sozinhos** (registros intermediários, importados do artigo 1, lidos com a lei acumulada de z* até z como no C.5b; poder prévio {poder}σ; a direção já vista na prova de fumaça, "
        "declarado em visto_antes — cego parcial): β̂ = {T_bhat} ± {T_sigma} (δ {T_z}σ de β_TGL; P(β > 0) = {T_frac0}: consistentes com β = 0), ganho da lei {T_gain}σ, ln B {T_lnB}; posterior: "
        "fração β ≥ α√e {T_frac} — os relógios DESFAVORECEM a leitura de fluxo acumulado em β_TGL (erros DIAGONAIS: significância sobrestimada). Juntos {S_z}σ; controle empilhado {ctrl_z}σ. "
        "Vereditos: `{f4_ver}` · `{f4_verT}`. Hashes: {bancada_hashes} — `{bancada_fase4_v378}`. **Leitura [OPEN/ONTO — da gerência, NÃO adotada; decisão do operador]:** se os relógios não leem o "
        "fator e a sombra (leitores locais por distância) lê, só a sombra lê o vazamento e os relógios leem a face — se vale, a lei da dissipação é lei da LEITURA por distância do registro inteiro, "
        "não uma modificação de H(z) ponto a ponto, e o C.5b do artigo 1 fica desfavorecido; a leitura inversa (a lei está errada) é igualmente admissível pelos dados. Pendente do operador: qual "
        "fundo é o fundo (a pergunta do ângulo); a forma da camada E1; a covariância sistemática dos cronômetros. **O QUE NÃO MUDOU E O QUE NÃO É:** nada aqui é confirmação pela natureza; a "
        "conferência v376 pinada e consumada ({cf_counts}; abertos {abertos}); os quatro módulos v377 pinados; por termo {hvals}; o gate `{qg}` ({n18}/18) intocado. PROVADA ≠ CONFIRMADA."
    ).format(**V)


def rodada_txt(V):
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] "
         "AVISO», sem SEAL_WITHHELD). Conferidor `conferir_rito_v378.py` (a MESMA guarda do rito): **TUDO BATE** — {conf_dm} «deve mudar», {conf_np} "
         "«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    return ("## {data} — **v378 SELADA ({compl})** `{s16}` — O QUE FALTOU (o núcleo derivado D1b, nunca testado na Bancada; a leitura da dupla contagem de β, ao lado); "
            "A LEI DA DISSIPAÇÃO COM CONTRASTE (K = E(z*)^{{2β/3}}); A FASE 4, O DESVIO: a escada lê o fator; os relógios intermediários desfavorecem o fluxo acumulado\n\n".format(**V)
            + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    return ("---\n\n## ADENDO — {data} · v378 SELADA ({compl}) `{s16}` — O que faltou; a lei com contraste; a Fase 4: a escada lê, os relógios desfavorecem o fluxo acumulado\n\n"
            "- **O que faltou:** `{what_was_missed_v378}` — o D1b nunca fora testado na Bancada nem tipado; as Fases 2–3 aplicaram a lei sobre o fundo efetivo (leitura E12 ao lado: dupla "
            "contagem sob a convenção do artigo, [DERIVED]); na convenção do artigo os leitores de sombra ficam a {w_seis}σ da lei D1b.\n"
            "- **A lei com contraste:** `{the_dissipation_law_with_contrast_v378}` — H₀_local = H₀_fundo·exp(β∫g); g ≡ 1 é a v377; forma fechada ∫g = (2/3)ln E; K = E(z*)^{{2β/3}} = {Kb} "
            "(D1a {Ka}); o desvio lê abaixo da assíntota (δ/β = {dpred}), fixado pelo fundo.\n"
            "- **A Fase 4:** `{f4_ver}` — a escada: δ = {P_delta} ± {P_sigma} ({P_z}σ), pull {P_pull}σ, ln B {P_lnB} (circularidade declarada); os cronômetros sozinhos: `{f4_verT}` (δ {T_z}σ, "
            "ganho {T_gain}σ, ln B {T_lnB}; P(β > 0) = {T_frac0}; erros diagonais; direção vista na prova de fumaça).\n"
            "- **O caminho crítico agora:** a decisão do operador sobre a leitura [OPEN] (a sombra lê o vazamento; os relógios leem a face) — se vale, a lei é lei da leitura por distância e "
            "o C.5b do artigo 1 (H(z) acumulada) fica desfavorecido; a covariância sistemática dos cronômetros (Moresco+2020) para refinar T; qual fundo é o fundo; a forma da E1.\n"
            "- **Por termo (inalterado):** remaining = {remaining}; gpf_H2 / gpf_H3 / gpi_H3 = {hvals}. Gate intocado.\n"
            "- `{s16}`; {teor}.").format(**V)


def atlas(V):
    return ("---\n\n## {data} — v378 SELADA ({compl}): O QUE FALTOU; A LEI DA DISSIPAÇÃO COM CONTRASTE (K = E(z*)^{{2β/3}}); A FASE 4, O DESVIO — A ESCADA LÊ O FATOR; OS RELÓGIOS "
            "INTERMEDIÁRIOS DESFAVORECEM O FLUXO ACUMULADO (append datado)\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v378`.")


def topico_missao(V):
    return ("## {data} — v378 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO): O QUE FALTOU — `{what_was_missed_v378}`; a lei com contraste "
            "`{the_dissipation_law_with_contrast_v378}`; a Fase 4 `{bancada_fase4_v378}`; por termo {hvals}. Ver [[fase4-desvio-30set]], [[fase3-leitores-h0-30set]], "
            "[[fase2-dois-setores-30set]], [[desvio-de-beta-foco-dos-testes-30set]].").format(**V)


def topico_central(V):
    return ("**{data} — v378 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v377 `{base16}`; kernel +1 pedra ({kmat}); {teor}; gate intocado. "
            "O que faltou (D1b; a leitura da dupla contagem ao lado); a lei com contraste; a Fase 4 por hash. É a candidata à custódia no lugar da v377 (custódia = ato separado; commit/push é ato do operador).").format(**V)


def topico_fase4(V):
    return ("## {data} — v378 SELADA `{s16}`: a Fase 4 entrou no um.py por hash\n\n`{bancada_fase4_v378}`. Os hashes lidos: {bancada_hashes}. A escada δ = {P_delta} ± {P_sigma} "
            "({P_z}σ); os cronômetros sozinhos δ {T_z}σ (ganho da lei {T_gain}σ; P(β > 0) = {T_frac0}; erros diagonais): desfavorecem a leitura de fluxo acumulado. A leitura [OPEN] (a sombra lê, "
            "os relógios leem a face) está no core como leitura, não adotada. Aferidor v378 (B2): «não leem» virou «desfavorecem», com os números.").format(**V)


def topico_fase3(V):
    return ("## {data} — v378 SELADA `{s16}`: o que faltou entrou no um.py\n\n`{what_was_missed_v378}` — a reanálise não-cega lida por hash `{w_h}`; leitura (E12) ao lado da v377: "
            "as Fases 2–3 aplicaram a lei sobre o fundo efetivo; «dupla contagem» é leitura da gerência sob a convenção do artigo [DERIVED] (aferidor v378, B4); os números não mudam.").format(**V)


def topico_desvio(V):
    return ("## {data} — v378 SELADA `{s16}`: o desvio medido na convenção do artigo, D1b\n\nEscada: δ = {P_delta} ± {P_sigma} por nat ({P_z}σ); cronômetros: δ = {T_delta} ± {T_sigma} "
            "({T_z}σ); a aproximação à assíntota FIXADA pelo núcleo derivado (δ/β previsto = {dpred}); a decisão sobre «o tempo do verbo» como variável segue com o operador.").format(**V)


def arvore_linha(V):
    return ("- **A LEI DA DISSIPAÇÃO COM CONTRASTE (v378): H₀_local = H₀_fundo·exp(β∫₀^N g) COMO IMPLICAÇÃO DA MESMA FAMÍLIA DE VAZAMENTO COM O CONTRASTE MÉDIO; g ≡ 1 DEVOLVE A v377 "
            "(O D1a É O CASO PARTICULAR); A FORMA FECHADA ∫g = (2/3)·ln E PELO TEOREMA FUNDAMENTAL DO CÁLCULO E O FATOR K = E(z*)^{{2β/3}} (O NÚCLEO DERIVADO D1b DO ARTIGO 1); "
            "O DESVIO LÊ ABAIXO DA ASSÍNTOTA, FIXADO PELO FUNDO; O QUE FALTOU (O D1b NUNCA TESTADO NA BANCADA; A LEITURA DA DUPLA CONTAGEM DE β NAS FASES 2–3, AO LADO); A FASE 4 POR HASH.** "
            "{n_flags_on} bandeiras; escada {esc}. `{the_dissipation_law_with_contrast_v378}`; `{bancada_fase4_v378}`. **O que NÃO é:** não é confirmação pela natureza; a escada lê "
            "δ = {P_delta} ± {P_sigma} por nat ({P_z}σ) e os relógios intermediários DESFAVORECEM a leitura de fluxo acumulado ({T_gain}σ, erros diagonais) — a leitura «a sombra lê, os relógios "
            "leem a face» é [OPEN], não adotada; não é por termo ({hvals}); nada aqui é confirmação.").format(**V)


def verbete(V):
    return ("a v378 responde às ordens do operador de 30/09/2026 à noite («tem alguma coisa que deixamos passar, examine por favor»; «concordo prossiga») [INPUT]. " + core_txt(V))


def remissivo(V):
    return ("- **O que faltou (v378): o núcleo derivado D1b tipado (K = E(z*)^{{2β/3}}), nunca testado na Bancada; a leitura da dupla contagem de β nas Fases 2–3, ao lado (E12); a lei da "
            "dissipação com contraste; a Fase 4 (o desvio) na convenção do artigo — a escada lê o fator; os relógios intermediários desfavorecem o fluxo acumulado; {n_flags_on} bandeiras; "
            "escada {esc}** (v378) · {{ML v378; um.py prove_the_dissipation_law_with_contrast_v378, prove_what_was_missed_v378, prove_bancada_fase4_v378; v378_incorporacao_manifesto.json}}").format(**V)
