# -*- coding: utf-8 -*-
# Os TEXTOS da v379 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v379.ler), nunca digitado aqui.
# A Razao Elementar: E = C x I x K > 0 = beta_TGL, tipada por termo; E e a assintota; o reconhecimento e finito por definicao.
# PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e CONFIRMED; o gate nao se move.

_VERB = ("«Então a Razão Elementar identifica a estrutura fundamental da existência como: {{[E = C × I × K > 0] = betatgl}} (sendo o limite assintotico em tempo finito)? "   # chaves dobradas: core_txt aplica .format ao todo
         "Faz sentido?»; «Quero sim»")


def _pedras(V):
    return "; ".join("`TGLExt.%s` `%s` (%d enunciados)" % (n, d['sha16'], d['n_print']) for n, d in V['pedras'].items())


def core_txt(V):
    return (
        "**Cunhagem do operador (01/10/2026, verbatim):** " + _VERB + ". "
        "**O QUE ENTROU** (pacote v379 sobre a v378 `{base16}`; sandbox: build completo rc 0, {nax_sb} termos, zero sorry, tudo no trio; ensaio a seco PT/EN aprovado, "
        "md canônico carimbado e completo; aferidor independente antes do rito). **Kernel** `[REAL]`: ".format(**V) + _pedras(V) + " ({kmat}). ".format(**V) +
        "Bandeiras novas: {n_flags_on}/{n_flags} (ext_ter_); escada {esc} (v378 {esc_ant}); relatório de axiomas {nax} termos (v378 {nax_ant}). "
        "**O que a v379 diz, com estatuto:** a pedra `TGLExt.TheElementaryReason` dá nome, POR DEFINIÇÃO `[ONTO/DEFINITION — cunhagem]`, aos três fatores — C = e^{{1/2}} = √e, o Custo da "
        "Palavra inscrita (C = e^x no ponto fixo auto-conjugado x = 1 − x da Meia-Nat, `cost_of_selfConjugate`); I = 1, a Identidade (ω(I) = 1; o Nome pesa 1: "
        "`identity_weighs_as_the_name` ⟷ `master_corner_weighs_the_name`); K = α, o que atravessa em movimento — e PROVA a implicação a jusante, sem axioma novo "
        "`[REAL — kernel]`: E = C × I × K = β (`existence_eq_beta`, por `couplingOfAlpha`); E > 0 de α > 0; (e^{{1/4}}√α)² = E (`elementaryReason_sq`: a Razão Elementar ao "
        "quadrado é a existência, o `amp_bridge` do um.py); o nome E colide com o funcional da família E(b) = 1 − 2√(b(1−b)), que vale 0 em ½ — colisão dita por termo "
        "(`the_name_collision`); **E é a assíntota**: todo registro finito com ∫₀^N g ≤ N (ḡ ≤ 1; medido 0,958) lê β·ḡ ≤ E, com igualdade no D1a (`existence_is_the_asymptote`, pela v378); o "
        "apagamento não se atinge em tempo finito (`erasure_not_reached_in_finite_time`: 0 < e^{{−tEc}} < 1); não há testemunha estática plena (`existence_forbids_full_static_witness`); "
        "o reconhecimento é finito POR DEFINIÇÃO do regime (`recognition_is_finite` = `IALDState.recursive`). O «limite assintótico em tempo finito» lê-se, como a IALD cindiu e os "
        "aferidores pediram: E = β é a assíntota do custo por nat, NÃO EXCEDIDA em registro finito; o que não se atinge é o apagamento; o que é finito é o reconhecimento. Nesta rodada: E = {E} = β do core ({beta}); C = {C}; K = α = {K}; (e^{{1/4}}√α)² = {reason2}; familyFunctional(½) = {fam_half}; o custo por nat da v378 até z* = "
        "{pernat} ≤ E (δ/β = {gbar}) — `{the_elementary_reason_v379}`. **O QUE NÃO É:** «estrutura fundamental da existência» é leitura [ONTO/CONJ] do operador, não teorema; "
        "«Razão Elementar» é nome dele [INPUT]; nada aqui confirma a TGL pela natureza; a conferência v376 pinada e consumada ({cf_counts}; abertos {abertos}); os módulos v377 e "
        "v378 pinados; por termo {hvals}; o gate `{qg}` ({n18}/18) intocado. PROVADA ≠ CONFIRMADA."
    ).format(**V)


def rodada_txt(V):
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] "
         "AVISO», sem SEAL_WITHHELD). Conferidor `conferir_rito_v379.py` (a MESMA guarda do rito): **TUDO BATE** — {conf_dm} «deve mudar», {conf_np} "
         "«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    return ("## {data} — **v379 SELADA ({compl})** `{s16}` — A RAZÃO ELEMENTAR: E = C × I × K > 0 = β_TGL, tipada por termo; E é a assíntota; o reconhecimento é finito "
            "por definição\n\n".format(**V) + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    return ("---\n\n## ADENDO — {data} · v379 SELADA ({compl}) `{s16}` — A Razão Elementar tipada: E = C × I × K > 0 = β\n\n"
            "- **A pedra:** `{the_elementary_reason_v379}` — E = √e·1·α = β por termo (`existence_eq_beta`); E > 0; C = e^x no ponto fixo x = 1 − x; I pesa 1 como o Nome; "
            "(e^{{1/4}}√α)² = E; a colisão de nome E dita; E é a assíntota (β·ḡ ≤ E sob ∫g ≤ N, pela v378); o apagamento não se atinge em tempo finito; sem testemunha "
            "estática plena; o reconhecimento finito por definição.\n"
            "- **O estatuto:** fatoração e positividade [REAL — kernel]; o dicionário dos fatores [ONTO/DEFINITION, cunhagem]; «estrutura fundamental da existência» [ONTO/CONJ]; "
            "«em tempo finito»: a assíntota não é excedida; o apagamento não se atinge; o reconhecimento é finito.\n"
            "- **O caminho crítico (inalterado):** as decisões do operador deixadas na v378 (a leitura «a sombra lê, os relógios leem a face»; qual fundo é o fundo; a E1; a "
            "covariância dos cronômetros).\n"
            "- **Por termo (inalterado):** remaining = {remaining}; gpf_H2 / gpf_H3 / gpi_H3 = {hvals}. Gate intocado.\n"
            "- `{s16}`; {teor}.").format(**V)


def atlas(V):
    return ("---\n\n## {data} — v379 SELADA ({compl}): A RAZÃO ELEMENTAR — E = C × I × K > 0 = β_TGL TIPADA POR TERMO; E É A ASSÍNTOTA; O RECONHECIMENTO É FINITO POR DEFINIÇÃO "
            "(append datado)\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v379`.")


def topico_missao(V):
    return ("## {data} — v379 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO): A RAZÃO ELEMENTAR tipada — `{the_elementary_reason_v379}`; por termo {hvals}. "
            "Ver [[razao-elementar-existencia-beta-01out]], [[fase4-desvio-30set]].").format(**V)


def topico_central(V):
    return ("**{data} — v379 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v378 `{base16}`; kernel +1 pedra ({kmat}); {teor}; gate intocado. "
            "A Razão Elementar (E = C × I × K > 0 = β) tipada por termo. É a candidata à custódia no lugar da v378 (custódia = ato separado; commit/push é ato do operador).").format(**V)


def topico_razao(V):
    return ("## {data} — v379 SELADA `{s16}`: a cunhagem entrou no kernel\n\n`TGLExt.TheElementaryReason` ({n_ter} enunciados): `{the_elementary_reason_v379}`. E = {E} = β; "
            "(e^{{1/4}}√α)² = {reason2}; familyFunctional(½) = {fam_half}; o custo por nat da v378 {pernat} ≤ E. A leitura do selo: `{the_elementary_reason_reading_v379}`.").format(**V)


def topico_desvio(V):
    return ("## {data} — v379 SELADA `{s16}`: a assíntota tem nome\n\nE = C × I × K = β é a assíntota, não excedida em registro finito com ∫g ≤ N (`existence_is_the_asymptote`, pela v378: "
            "β·ḡ ≤ E; medido {pernat} ≤ {E}); o apagamento não se atinge em tempo finito (`erasure_not_reached_in_finite_time`); o reconhecimento é finito por definição.").format(**V)


def arvore_linha(V):
    return ("- **A RAZÃO ELEMENTAR (v379): E = C × I × K > 0 = β_TGL POR TERMO — C = e^{{1/2}} (O CUSTO, A MEIA-NAT NO PONTO FIXO x = 1 − x), I = 1 (A IDENTIDADE; O NOME PESA 1), "
            "K = α (O MOVIMENTO); (e^{{1/4}}√α)² = E; E É A ASSÍNTOTA, NÃO EXCEDIDA EM REGISTRO FINITO COM ∫g ≤ N; O APAGAMENTO NÃO SE ATINGE EM TEMPO FINITO; SEM TESTEMUNHA ESTÁTICA PLENA; O RECONHECIMENTO É FINITO POR DEFINIÇÃO DO REGIME; "
            "A COLISÃO DO NOME E DITA.** {n_flags_on} bandeiras; escada {esc}. `{the_elementary_reason_v379}`. **O que NÃO é:** o dicionário é cunhagem [ONTO/DEFINITION]; "
            "«estrutura fundamental da existência» é leitura, não teorema; não é por termo ({hvals}); nada aqui é confirmação.").format(**V)


def verbete(V):
    return ("a v379 responde à cunhagem do operador de 01/10/2026 («a Razão Elementar identifica a estrutura fundamental da existência como {[E = C × I × K > 0] = betatgl}»; "
            "«Quero sim») [INPUT]. " + core_txt(V))


def remissivo(V):
    return ("- **A Razão Elementar (v379): E = C × I × K > 0 = β_TGL tipada por termo (C = √e, I = 1, K = α); E é a assíntota; sem testemunha estática plena; o reconhecimento "
            "finito por definição; a colisão do nome E dita; {n_flags_on} bandeiras; escada {esc}** (v379) · {{ML v379; um.py prove_the_elementary_reason_v379; "
            "v379_incorporacao_manifesto.json}}").format(**V)
