# -*- coding: utf-8 -*-
# Os TEXTOS da v380 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v380.ler), nunca digitado aqui.
# As Fases 5, 6 (ECO V3 + V4 + V5) e 7 da Bancada, o banco de GW e as erratas ao lado, lidos por hash. SEM kernel novo; o gate nao se move.
# PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e CONFIRMED; falsificar o PAR (leitura, lei) nao falsifica a teoria.

_VERB = ("«Agora vamos melhorar nossa bancada inserindo shoes nela […] realizar os testes que são mais promissores»; «eu quero realizar o teste da transformada radical com as ondas "
         "gravitacionais e ecos […] eu penso que esse é o melhor teste»; «todo esse banco de dados novo (gweco) […] já o vincule à bancada para vc poder trabalhar com eles em tempo "
         "real dentro do sistema carregado com os dados reais»; «estude tudo que eu já fiz e já escrevemos e resolva os problemas que faltam»")


def _pedras(V):
    return "nenhuma (a v380 é sem kernel novo: escada {esc}, {nax} termos no relatório de axiomas, inalterados)".format(**V)


def core_txt(V):
    return (
        "**Ordens do operador (01/10/2026, verbatim):** " + _VERB + ". "
        "**O QUE ENTROU** (pacote v380 sobre a v379 `{base16}`; SEM kernel novo — ".format(**V) + _pedras(V) + "; ensaio a seco PT/EN aprovado, md canônico carimbado e completo; aferidor independente antes do rito). "
        "**O módulo `prove_bancada_fases_5_6_7_v380`** lê por hash (bytes e texto normalizado a LF lado a lado, EV-08; {n_crlf} artefato com CRLF, dito) 18 artefatos do cache do rito: "
        "**Fase 5 (SH0ES na Bancada):** H₀ da escada por SNe + 77 calibradores Cefeida = {h0_v} ± {h0_s} (z {h0_z} do valor publicado 73,6 ± 1,1 [DECLARADO, não relido na fonte]); δ da escada na leitura sombra z = {p5_z}. "
        "**Fase 6 (ECO V3, «a transformada radical»):** a raiz como AMPLITUDE pré-registrada da resposta da fronteira (três leituras: √β, sin 2θ_M, β) a duas leis de atraso [INPUT/ONTO] (MAY; KMS = 2π/κ por evento), "
        "244 BBH O1–O4, 484 séries hasheadas, estimador ancorado corrigido pela auditoria de 28/09, poder gravado ANTES de abrir: o par (√β ou sin 2θ_M, 2π/κ) **FALSIFIED_AT_DELAY_LAW** em 240 BBH "
        "(â = {k6_a} ± {k6_s} em unidades de √β; z_excl {k6_z1} e {k6_z2}; sistemática relativa {k6_sr1} e {k6_sr2}; controles mudos) e na SUBAMOSTRA cega de O4 ({o6_n} dos {k6_n}, não uma réplica independente; z_excl {o6_z1} e {o6_z2}; "
        "a parte de maio, não cega, dá √β sem poder e sin 2θ_M falsificado); a lei MAY INCONCLUSIVE_SYSTEMATICS pela regra (descasamento no atraso curto até {m6_sys}) — e na V3 o seu controle τ/2 respondeu a {m6_c1}σ (todos) e {m6_c1o}σ (O4): "
        "bandeira pré-registrada DELAY_CONTROL_RESPONDS {m6_flag}; a EMENDA V4 (grade ±2σ, NÃO cega, dita) leva (sin 2θ_M, MAY) a falsificado (z_excl {v4_z2}) com os controles a {v4_ctrl}σ (abaixo da bandeira por pouco, dito), "
        "e (√β, MAY) segue inconclusivo como limite deste estimador (regra V4: não se emenda uma terceira vez); "
        "a EMENDA V5 (CEGA só quanto à lei nova; V3 e V4 já abertas) testou a lei de atraso de 24/12/2025 do acervo, τ = 2GM_f/(β c³) (≈ 14 períodos; [DECLARADO]: derivação por IA sob direção do operador, não derivada do axioma; nunca aberta nesse atraso): "
        "√β e sin 2θ_M falsificados também ali (z_excl {v5_z1}/{v5_z2}; O4 cego {v5_o1}/{v5_o2}; sistemática {v5_sys}; controles mudos), e o par do próprio documento (amplitude β) sem poder ({v5_r3p}σ; poder cego {v5_r3cp}σ): "
        "o rótulo emitido pela regra geral é {v5_r3lab} (sistemática relativa à amplitude minúscula > 0,3) e a cláusula V5 da emenda (poder < 5σ → NOT_FALSIFIED_UNDERPOWERED) {v5_clausula} — sem poder, não falsificado. "
        "A quarta lei do acervo, 2GM/(α²c³) (4–12 s), fica fora do segmento de 2,5 s e não foi testada. "
        "**Fase 7 (cronômetros com a covariância de Moresco+2020):** o z do ganho da lei acumulada nos registros intermediários vai de {t7_diag} (diagonal) a {t7_m20}; ln B(sombra/acumulada) de {u7_diag} a {u7_m20} — as leituras das Fases 4–5 ENFRAQUECEM. "
        "**O banco:** {gb_ok} de {gb_n} séries de O4 do GWOSC OK por manifesto sha256 ({gb_nan} NaN na janela — um detector por evento; {gb_out} janelas fora do arquivo); o banco residente vive na Bancada Um (API /api/gw, MCP gw_*), moldes e ajuste no WSL. "
        "**Seis erratas ao lado da auditoria de 28/09** (CT-03/GWECO-04: a amplitude √β dos ritos v341–v348 é a do peso 1 [INPUT]; GWECO-05; GWECO-03; RD-06; VV-N1: a entrada NuFIT contém o JUNO e a tensão depende do ajuste global, 2,95σ vs 2,44σ; RNC-06), "
        "mais a errata da linha diagonal da v378 e a nota do banco. "
        "Selo: +1 leitura (`{the_bancada_fases_5_6_7_reading_v380}`) e as chaves EV-06 (conjunta V3; D1 V3 real). "
        "**O QUE NÃO É:** falsificar o PAR (leitura, lei de atraso) não falsifica a teoria; as leis de atraso não são derivadas do axioma (MAY e KMS [INPUT/ONTO]; DEC [DECLARADO]); a leitura sin 2θ é [CONJECTURE]; o peso da resposta da fronteira ao gráviton e a lei de atraso são "
        "decisões do operador; a leitura «sombra» é [OPEN/ONTO]; o «100σ» de dezembro segue retirado (v340); a conferência v376 pinada e consumada ({cf_counts}; abertos {abertos}); os módulos v377–v379 pinados; "
        "por termo {hvals}; o gate `{qg}` ({n18}/18) intocado. PROVADA ≠ CONFIRMADA. Veredito: `{bancada_fases_5_6_7_v380}`."
    ).format(**V)


def rodada_txt(V):
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] "
         "AVISO», sem SEAL_WITHHELD). Conferidor `conferir_rito_v380.py` (a MESMA guarda do rito): **TUDO BATE** — {conf_dm} «deve mudar», {conf_np} "
         "«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    return ("## {data} — **v380 SELADA ({compl})** `{s16}` — AS FASES 5, 6 E 7 DA BANCADA, O BANCO DE GW E AS ERRATAS AO LADO, POR HASH: o par (√β ou sin 2θ, 2π/κ) falsificado em 240 BBH e na subamostra cega de O4; "
            "MAY inconclusivo; os cronômetros com covariância completa enfraquecem as Fases 4–5; sem kernel novo; gate intocado\n\n".format(**V) + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    return ("---\n\n## ADENDO — {data} · v380 SELADA ({compl}) `{s16}` — As Fases 5–7 da Bancada por hash; o eco como resposta radical da fronteira\n\n"
            "- **O que mudou no caminho crítico:** a rota do eco como atestação ficou com o PAR (√β ou sin 2θ_M, 2π/κ) falsificado (z_excl {k6_z1}/{k6_z2}; subamostra cega O4 {o6_z1}/{o6_z2}) e a lei MAY inconclusiva por "
            "sistemática do atraso curto; falta uma LEI DE ATRASO derivada e o PESO da resposta da fronteira ao gráviton — decisões do operador. Nenhum atraso escrito na voz dele existe no acervo (leitor de 01/10); "
            "a lei de dezembro/2025 (2GM_f/(β c³), ≈ 14 períodos) foi adotada no acervo e nunca testada — testada na emenda V5 (registro ao lado, Bancada).\n"
            "- **Os cronômetros:** com a covariância completa (Moresco+2020) o z do ganho da lei acumulada cai de {t7_diag} para {t7_m20} e o ln B(sombra/acumulada) de {u7_diag} para {u7_m20}: a ressalva «erros diagonais» está medida; "
            "a decisão «qual fundo é o fundo» e a leitura «sombra» seguem do operador.\n"
            "- **O SH0ES:** H₀ da escada {h0_v} ± {h0_s} (z {h0_z}); δ sombra z {p5_z}.\n"
            "- **Por termo (inalterado):** remaining = {remaining}; gpf_H2 / gpf_H3 / gpi_H3 = {hvals}. Gate intocado; sem kernel novo.\n"
            "- `{s16}`; {teor}.").format(**V)


def atlas(V):
    return ("---\n\n## {data} — v380 SELADA ({compl}): AS FASES 5, 6 E 7 DA BANCADA UM, O BANCO DE GW E SEIS ERRATAS DA AUDITORIA + 1 DA v378 + 1 NOTA AO LADO, LIDOS POR HASH — O PAR (√β OU sin 2θ_M, 2π/κ) FALSIFICADO EM 240 BBH E NA SUBAMOSTRA CEGA DE O4; "
            "MAY INCONCLUSIVO; A COVARIÂNCIA DOS CRONÔMETROS ENFRAQUECE AS FASES 4–5; SEM KERNEL NOVO (append datado)\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v380`.")


def topico_missao(V):
    return ("## {data} — v380 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO; sem kernel novo): as Fases 5, 6 e 7 da Bancada, o banco de GW e 6+1+1 erratas ao lado por hash — `{bancada_fases_5_6_7_v380}`; por termo {hvals}. "
            "Ver [[fase6-eco-radical-01out]], [[fase7-cc-covariancia-01out]], [[fase5-sh0es-01out]].").format(**V)


def topico_central(V):
    return ("**{data} — v380 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v379 `{base16}`; sem kernel novo ({kmat}); {teor}; gate intocado. "
            "As Fases 5–7 da Bancada, o banco de GW e as erratas ao lado por hash; EV-06 no selo. É a candidata à custódia no lugar da v379 (custódia = ato separado; commit/push é ato do operador).").format(**V)


def topico_fase6(V):
    return ("## {data} — v380 SELADA `{s16}`: a Fase 6 entrou no um.py por hash\n\n`prove_bancada_fases_5_6_7_v380` = `{bancada_fases_5_6_7_v380}`. KMS todos: â = {k6_a} ± {k6_s}, z_excl {k6_z1}/{k6_z2}, sistemática {k6_sys}; "
            "subamostra cega O4 ({o6_n} dos {k6_n}): z_excl {o6_z1}/{o6_z2}; MAY sistemática {m6_sys}, controle τ/2 na V3 {m6_c1}σ (O4 {m6_c1o}σ) com a bandeira {m6_flag}; V4 (não cega) sin 2θ × MAY z_excl {v4_z2}, controles {v4_ctrl}σ; "
            "V5 (cega só quanto à lei DEC [DECLARADO]) z_excl {v5_z1}/{v5_z2} (O4 {v5_o1}/{v5_o2}); (β, DEC) sem poder {v5_r3p}σ (poder cego {v5_r3cp}σ), rótulo da regra {v5_r3lab}, cláusula V5 {v5_clausula}. "
            "Os dois desvios do pipeline (bandeira e cláusula) estão DITOS no um.py, não corrigidos por cima. A leitura do selo: `{the_bancada_fases_5_6_7_reading_v380}`.").format(**V)


def topico_fase7(V):
    return ("## {data} — v380 SELADA `{s16}`: a Fase 7 entrou no um.py por hash\n\nT z do ganho: diagonal {t7_diag} → moresco2020 {t7_m20}; U ln B(sombra/acumulada): {u7_diag} → {u7_m20}; S δ̂ z (moresco2020) {s7_z}.").format(**V)


def topico_bancada(V):
    return ("## {data} — v380 SELADA `{s16}`: o banco de GW e as três fases no programa\n\nO um.py lê por hash o manifesto do O4 ({gb_ok}/{gb_n} OK; {gb_nan} NaN; {gb_out} fora do arquivo), os resultados das Fases 5–7, as emendas V4 e V5 com os poderes cegos e o diagnóstico; "
            "6 erratas da auditoria + 1 da v378 + 1 nota ao lado registradas no core. Veredito `{bancada_fases_5_6_7_v380}`.").format(**V)


def arvore_linha(V):
    return ("- **AS FASES 5, 6 E 7 DA BANCADA UM POR HASH (v380): O SH0ES NA BANCADA (H₀ DA ESCADA {h0_v} ± {h0_s}); O ECO COMO RESPOSTA RADICAL DA FRONTEIRA — O PAR (√β OU sin 2θ_M, 2π/κ) FALSIFICADO EM 240 BBH "
            "(z_excl {k6_z1}/{k6_z2}) E NA SUBAMOSTRA CEGA DE O4 ({o6_z1}/{o6_z2}); MAY INCONCLUSIVO POR SISTEMÁTICA; A EMENDA V4 NÃO CEGA DITA; A LEI DEC DE DEZ/2025 [DECLARADO] FALSIFICADA PARA √β E sin 2θ (CLÁUSULA V5 NÃO APLICADA, DITO); OS CRONÔMETROS COM A COVARIÂNCIA COMPLETA DE MORESCO+2020 "
            "(z DO GANHO {t7_diag} → {t7_m20}; ln B SOMBRA/ACUMULADA {u7_diag} → {u7_m20}); O BANCO DE GW ({gb_ok}/{gb_n}); SEIS ERRATAS DA AUDITORIA + 1 DA v378 + 1 NOTA AO LADO; SEM KERNEL NOVO.** escada {esc}. `{bancada_fases_5_6_7_v380}`. "
            "**O que NÃO é:** falsificar o par (leitura, lei) não falsifica a teoria; as leis de atraso são [INPUT/ONTO]; nada aqui é confirmação; não é por termo ({hvals}).").format(**V)


def verbete(V):
    return ("a v380 responde às ordens do operador de 01/10/2026 (o SH0ES na Bancada; «o teste da transformada radical com as ondas gravitacionais e ecos»; «vincule o banco à bancada»; "
            "«resolva os problemas que faltam») [INPUT]. " + core_txt(V))


def remissivo(V):
    return ("- **As Fases 5, 6 e 7 da Bancada por hash (v380): SH0ES; o eco como resposta radical da fronteira — o par (√β ou sin 2θ_M, 2π/κ) falsificado em 240 BBH e na subamostra cega de O4; MAY inconclusivo; "
            "a covariância dos cronômetros enfraquece as Fases 4–5; o banco de GW; seis erratas da auditoria (+1 da v378, +1 nota) ao lado; sem kernel novo; escada {esc}** (v380) · {{ML v380; um.py prove_bancada_fases_5_6_7_v380; "
            "v380_incorporacao_manifesto.json}}").format(**V)
