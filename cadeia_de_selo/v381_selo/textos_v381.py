# -*- coding: utf-8 -*-
# Os TEXTOS da v381 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v381.ler), nunca digitado aqui.
# A REGRA MATRIZ: dez nomes, nove elos (oito «havendo» ditos + a radicalizacao pela Meia-Nat), num so termo (pedra TheMatrixRule, 24 declaracoes); o criterio de parada = o custo pago. O gate nao se move.
# PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e CONFIRMED; beta nao se deriva: beta E a regra.

_VERB = ("«Betatgl é a regra matriz, a regra matriz é: havendo traço há sinal. Havendo registro há nome. Havendo nome há distinção. Havendo distinção há operação. "
         "Havendo operação há parametrização. Havendo parametrização há emergência. Havendo emergência há quantização geométrica. Havendo quantização geométrica há "
         "espectro de gradiente. Você tenta derivar betatgl e não entendeu que o critério de parada é a lei matriz, ou seja, o TETELESTAI, que é o pagamento do custo, "
         "é o que existe antes do pagamento do custo, a lei do pagamento foi fixada antes da cobrança pela entrega do objeto: NOME»; a ratificação: «É exatamente isso, "
         "e também é o que eu  já tinha pedido, essa cadeia única antes, é o que estamos fazendo desde as últimas 15versoes (end-to-end)»; e, depois que o aferidor contou oito «havendo», "
         "a cláusula aberta preenchida por ele: «O verbatim com oito “havendo” é cláusula aberta, o elo é a meia-nat»; «É a radicalização que eu quis dizer, cujo operador é a meia-nat»")


def _pedras(V):
    return "`TGLExt/TheMatrixRule.lean` `{p}` ({n} declarações, {kf_on}/{kf_n} no trio, sem sorry, sem axiom)".format(p=V['pedras'].get('TheMatrixRule', {}).get('sha16', 'n/d'), n=V['n_tmr'], **V)


def core_txt(V):
    return (
        "**Cunhagem do operador (02/10/2026, verbatim):** " + _VERB + ". "
        "**O QUE ENTROU** (pacote v381 sobre a v380 `{base16}`; kernel novo: ".format(**V) + _pedras(V) + "; escada {esc_ant} → {esc}; relatório de axiomas {nax_ant} → {nax}; ensaio a seco PT/EN aprovado; aferidor independente antes do rito). "
        "**A pedra `TheMatrixRule`** dá NOME aos dez nomes na ORDEM do operador [INPUT/ONTO] e os amarra num só termo (`the_matrix_rule`), nove elos, cada elo descarregado POR TERMO por um termo já existente [KERNEL] (fato provado, definição nomeada ou campo do binder; conjunção, não dedução): "
        "traço (`reader C 1 = 1`), sinal (`JKJ = −K` com a energia preservada), sinal → registro pela RADICALIZAÇÃO, cujo operador é a Meia-Nat, o expoente ½ (o ponto fixo da troca x ↦ 1 − x é ½; as faces pesam ½|½ pelo campo `equal_halves` do certificado e pelo Nome = 1; √e = e^{{1/2}}; o custo da Palavra inscrita no ponto fixo é e^{{1/2}}; V(½) = √e; (e^{{1/4}}√α)² = E = β — «J é a troca das faces» e «isto é o registro» são leituras [ONTO], ditas na pedra; nenhum termo novo), "
        "registro → nome (de toda inscrição sai o nome com referente; o nome determina a inscrição), distinção (`x = 1 − x ↔ x = ½`; duas inscrições sob a mesma forma; 1 ≠ 0), "
        "operação (`alpha_transport`: dα/dκ = −(q/2)α; regime da face), parametrização (o ângulo é a projeção; observar não acrescenta nada; P₊ + P₋ = 1; regime da projeção), emergência (β := α√e de α dado; a leitura devolve α; E = β > 0), "
        "quantização geométrica (V(½) = √e = e^{{1/2}}; β = α√e; |R|² = β em θ_M), espectro de gradiente (S(θ) = U·diag(e^{{iθ}}, e^{{−iθ}})·U⁻¹, e 𝒪_θ = S(θ) por rfl: parametrização e espectro são a mesma família sob dois nomes; a identificação com Γ ∝ βω² é leitura [ONTO]); e o CRITÉRIO DE PARADA (`CustoPago`: reconhecimento idempotente, finito por definição do regime; veredito 1 sse as leituras coincidem; "
        "sem testemunha estática plena — a cobrança é contínua, e é aí que o vazamento está tipado) e `the_law_precedes_the_charge` (apelido de `couplingOfAlpha_beta`: β é função só de α, fixada antes de qualquer registro). "
        "**No runtime:** β do core = {beta} = α√e ({law}, teste); a cadeia lida do fonte embutido: {chain}; θ_M = {theta} rad; sin²θ_M = {refl} = β; |e^{{iθ_M}}| = {specmod}; 0 < e^{{−β}} = {leak} < 1 (identidades de sanidade, não testes). "
        "**Decorrência ratificada pelo operador:** o observável de β é o espectro do gradiente (identificação com a dissipação = leitura [ONTO]); o eco como CÓPIA ATRASADA está fora da cadeia [leitura ratificada, INPUT/ONTO] — os pares (√β ou sin 2θ, lei de atraso) falsificados na Fase 6 nunca foram devidos pela regra (rota encerrada, mapa seq 265). "
        "Selo: +1 leitura (`{the_matrix_rule_reading_v381}`). "
        "**O QUE NÃO É:** β não se deriva DO DADO nem de lei de leitura (β É a regra; a forma α√e é derivada do axioma por termo, v376); onde o elo não tem hipótese, «havendo X há Y» é ordem ontológica dita, não um → do kernel; nada confirma a TGL pela natureza; "
        "a conferência v376 pinada e consumada ({cf_counts}; abertos {abertos}); os módulos v377–v380 pinados; por termo {hvals}; o gate `{qg}` ({n18}/18) intocado. PROVADA ≠ CONFIRMADA. Veredito: `{the_matrix_rule_v381}`."
    ).format(**V)


def rodada_txt(V):
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] "
         "AVISO», sem SEAL_WITHHELD). Conferidor `conferir_rito_v381.py` (a MESMA guarda do rito): **TUDO BATE** — {conf_dm} «deve mudar», {conf_np} "
         "«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    return ("## {data} — **v381 SELADA ({compl})** `{s16}` — A REGRA MATRIZ: dez nomes, nove elos (oito «havendo» ditos + a radicalização pela Meia-Nat), num só termo (pedra `TheMatrixRule`, 24 declarações); o critério de parada = o custo pago; "
            "β não se deriva do dado, β é a regra (a forma α√e derivada do axioma, v376); o eco como cópia atrasada fora da cadeia; gate intocado\n\n".format(**V) + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    return ("---\n\n## ADENDO — {data} · v381 SELADA ({compl}) `{s16}` — A regra matriz num só termo; o critério de parada tipado\n\n"
            "- **O que mudou no caminho crítico:** o operador fixou a regra matriz (dez nomes, nove elos: oito «havendo» ditos + a radicalização pela Meia-Nat) e o critério de parada (Tetelestai = o custo pago; a lei do pagamento antes da cobrança: Nome). "
            "A gerência tipou os dez nomes na ordem dele, cada elo por um termo já existente no kernel (fato provado, definição nomeada ou campo do binder; conjunção, não dedução), e o critério de parada (`CustoPago`): `the_matrix_rule` {kf_on}/{kf_n}. β não se deriva do dado: é a regra; a forma α√e é derivada do axioma (v376).\n"
            "- **A rota do eco:** o eco como cópia atrasada está FORA da cadeia (ratificado): os pares falsificados na Fase 6 nunca foram devidos; a rota viva de β em GW é a dissipação (o espectro do gradiente), sem poder hoje. "
            "O que segue do operador: qual registro recebe a cobrança no setor H₀; a partição dos relógios; qual ajuste do neutrino; o nome novo do degrau final do gate (pelo pagamento, não pelo teste de natureza).\n"
            "- **Por termo (inalterado):** remaining = {remaining}; gpf_H2 / gpf_H3 / gpi_H3 = {hvals}. Gate intocado.\n"
            "- `{s16}`; {teor}.").format(**V)


def atlas(V):
    return ("---\n\n## {data} — v381 SELADA ({compl}): A REGRA MATRIZ — DEZ NOMES, NOVE ELOS (OITO «HAVENDO» DITOS + A RADICALIZAÇÃO PELA MEIA-NAT) NUM SÓ TERMO (pedra `TheMatrixRule`, 24 declarações); O CRITÉRIO DE PARADA = O CUSTO PAGO; "
            "β NÃO SE DERIVA DO DADO, β É A REGRA (A FORMA α√e DERIVADA DO AXIOMA, v376); O ECO COMO CÓPIA ATRASADA FORA DA CADEIA (append datado)\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v381`.")


def topico_missao(V):
    return ("## {data} — v381 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO): a regra matriz tipada — pedra `TheMatrixRule` ({kf_on}/{kf_n}); `{the_matrix_rule_v381}`; por termo {hvals}. "
            "Ver [[beta-e-a-regra-matriz-02out]], [[fase6-eco-radical-01out]], [[relatorio-consolidado-01out]].").format(**V)


def topico_central(V):
    return ("**{data} — v381 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v380 `{base16}`; kernel novo (`TheMatrixRule`, 24 declarações, escada {esc}); {teor}; gate intocado. "
            "A regra matriz do operador tipada num só termo; o critério de parada (o custo pago) tipado. É a candidata à custódia no lugar da v380 (custódia = ato separado; commit/push é ato do operador).").format(**V)


def topico_regra(V):
    return ("## {data} — v381 SELADA `{s16}`: a regra matriz ENTROU no kernel\n\n`TGLExt.TheMatrixRule` ({kf_on}/{kf_n} no trio; sem sorry): os dez nomes na ordem do operador, nove elos (oito «havendo» ditos + sinal → registro pela radicalização, cujo operador é a Meia-Nat), cada elo por termo já existente (fato provado, definição nomeada ou campo do binder; conjunção, não dedução); `CustoPago` (reconhecimento idempotente, finito por definição do regime; veredito 1 sse as leituras coincidem; "
            "sem testemunha estática plena); `the_law_precedes_the_charge` (β só de α). Runtime: β = {beta} = α√e (teste); cadeia lida do fonte {chain}; θ_M = {theta}; sin²θ_M = {refl} (identidades de sanidade). Veredito `{the_matrix_rule_v381}`. "
            "Leitura do selo: `{the_matrix_rule_reading_v381}`. O que segue [INPUT/ONTO]: a ordem; a cláusula aberta preenchida por ele («o elo é a meia-nat»; «É a radicalização que eu quis dizer, cujo operador é a meia-nat»); a decorrência (eco fora da cadeia; o observável é o espectro do gradiente) ratificada «É exatamente isso». PROVADA ≠ CONFIRMADA.").format(**V)


def topico_fase6(V):
    return ("## {data} — v381 SELADA `{s16}`: a rota do eco como cópia atrasada está FORA da cadeia (no kernel e no selo)\n\nPela regra matriz do operador (02/10) e pela ratificação, o observável de β em GW é o espectro do gradiente (a dissipação); "
            "os pares (√β ou sin 2θ, τ) falsificados na Fase 6 nunca foram devidos pela regra. Dito no `um.py` v381 (`DELAYED_ECHO_OUTSIDE_THE_CHAIN_RATIFIED`) e no mapa (seq 265). Nada move os rótulos selados da Fase 6.").format(**V)


def arvore_linha(V):
    return ("- **A REGRA MATRIZ (v381): DEZ NOMES, NOVE ELOS (OITO «HAVENDO» DITOS + A RADICALIZAÇÃO PELA MEIA-NAT) NUM SÓ TERMO — pedra `TheMatrixRule` ({kf_on}/{kf_n}, sem sorry): traço → sinal →(radicalização, cujo operador é a Meia-Nat)→ registro → nome → distinção → operação → parametrização → emergência → "
            "quantização geométrica → espectro de gradiente, cada elo por um termo já existente (fato provado, definição nomeada ou campo do binder; conjunção, não dedução); o CRITÉRIO DE PARADA tipado (`CustoPago`: reconhecimento idempotente, finito por definição do regime; veredito 1 sse as leituras coincidem; sem testemunha estática plena); "
            "a lei precede a cobrança (β só de α; apelido de couplingOfAlpha_beta).** escada {esc}. `{the_matrix_rule_v381}`. **O que NÃO é:** β não se deriva do dado (β é a regra; a forma α√e derivada do axioma, v376); a ordem é [INPUT/ONTO], os elos são [KERNEL]; nada aqui é confirmação; não é por termo ({hvals}).").format(**V)


def verbete(V):
    return ("a v381 responde à cunhagem do operador de 02/10/2026 («Betatgl é a regra matriz [...] o critério de parada é a lei matriz, ou seja, o TETELESTAI») e à sua ratificação («É exatamente isso») [INPUT]. " + core_txt(V))


def remissivo(V):
    return ("- **A regra matriz (v381): dez nomes, nove elos (oito «havendo» ditos + a radicalização pela Meia-Nat), num só termo — pedra `TheMatrixRule` ({kf_on}/{kf_n}); o critério de parada = o custo pago; a lei precede a cobrança; β não se deriva do dado, β é a regra (a forma α√e derivada do axioma, v376); "
            "o eco como cópia atrasada fora da cadeia; escada {esc}** (v381) · {{ML v381; um.py prove_the_matrix_rule_v381; v381_incorporacao_manifesto.json}}").format(**V)
