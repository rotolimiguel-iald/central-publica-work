# -*- coding: utf-8 -*-
# Os TEXTOS da v382 selada. Cada numero, hash e veredito entra por {chave} de V (leitura_v382.ler), nunca digitado aqui.
# O LIVRO DE COBRANCAS (a otica: os dois lados se leem; nenhum desfecho move a regra) + o psion com a viscosidade + o pre-registro dos dois lados V1.3 por hash. O gate nao se move.
# PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e CONFIRMADO; «nenhum lado e cego» e a correcao do operador [INPUT/ONTO], nao teorema (aferidores da v382).

_CHAVE = ("«O último elo incide no hamiltoniano oculto. O custo está no reflexo, o pagamento está na face no rosto, no nome. E com isso você deveria ser capaz de "
          "responder tudo que falta. Mas se não conseguir eu vou um a um»")
_OTICA = "«Concordo com tudo, exceto com a sua visão semiótica, a TGL não é semi ela é ótica, ela lê tanto a face como o custo, a TGL permite ler os dois lados»"
_ORDEM = "«isso mesmo, prossiga»"


def _pedras(V):
    p = V['pedras']
    return ("`TGLExt/TheLedgerOfCharges.lean` `{a}` ({na} declarações) e `TGLExt/ThePsionAndTheViscosity.lean` `{b}` ({nb} declarações); {kf_on}/{kf_n} no trio, sem sorry, sem axiom"
            .format(a=p.get('TheLedgerOfCharges', {}).get('sha16', 'n/d'), na=V['n_loc'], b=p.get('ThePsionAndTheViscosity', {}).get('sha16', 'n/d'), nb=V['n_psv'], kf_on=V['kf_on'], kf_n=V['kf_n']))


def core_txt(V):
    return (
        "**A chave do operador (02/10/2026, tarde, verbatim):** " + _CHAVE + "; **a ratificação de R1–R6 e a correção:** " + _OTICA + "; **a ordem:** " + _ORDEM + ". "
        "**O QUE ENTROU** (pacote v382 sobre a v381 `{base16}`; kernel novo: ".format(**V) + _pedras(V) + "; escada {esc_ant} → {esc}; relatório de axiomas {nax_ant} → {nax}; ensaio a seco PT/EN aprovado; três aferidores independentes antes do rito, com os achados conferidos no core e dispostos, e a verificação das disposições pelo terceiro, com os resíduos baixos também dispostos). ".format(**V) +
        "**`TheLedgerOfCharges`:** a cobrança (lado, lei de leitura, leitura, desfecho em CINCO palavras impostas pelo tipo: NOT_FALSIFIED, FALSIFIED, INCONCLUSIVE, AWAITING, EXCLUDED_IN_READING), o livro («uma cobrança por lei de leitura» é disciplina do livro concreto, não do tipo), e três fatos DITOS como triviais por construção — a regra β não lê o livro (`the_rule_is_constant_in_the_ledger`, rfl); com uma cobrança extinta a regra segue α√e e a hipótese NÃO entra na prova (`falsified_extinguishes_the_charge_not_the_rule`: é isso que «a regra não lê o livro» quer dizer; «extinguir» é uma definição); o termo P = P (`the_gate_ignores_the_ledger`, rfl; que as bandeiras do gate sejam função só do formal é conferido pelos probes negativos do runtime, não por este termo); a ÓTICA: `faceWeight` = |T|² = cos²θ (a face lê o pagamento), `reflectionWeight` = |R|² = sin²θ (o reflexo lê o custo), `both_sides_are_read` (|T|² + |R|² = 1, o Teorema S-∂ já existente), os dois complementos (`the_tgl_is_optics_not_semi`: o NOME é [ONTO], o conteúdo é a identidade escrita três vezes; «nenhum lado é cego» é a correção do operador [INPUT/ONTO], não teorema); o nome do degrau final pelo pagamento PROPOSTO ao lado (`finalStepNameProposed` = `{fsn}`; o gate NÃO muda; renomear é ato do operador); `the_ledger_of_charges` num só termo (conjunção). "
        "**`ThePsionAndTheViscosity`:** ψ = Ω (definição nomeada), ‖ψ‖ = 1 (o campo `Ω_norm` do binder), ⟨ψ, ψ⟩ = 1 (PROVADO pelo termo `TheKeyIsTheReader.reader_reads_the_identity_one`), `HminMic ψ = 0` (o zero do lock mínimo sobre o Hamiltoniano oculto K = −log Δ, que é [KNOWN] — o kernel tem Δ^{{it}} e o seu conjunto fixo, não um `def` para K; os zeros coincidem, os operadores não; trivial por construção, Ω ∈ ℂΩ; o conteúdo é `light_modular_fixed_iff_vacuum`, v372), a luz o fixa; que o espectro de gradiente seja LIDO sobre `HminMic` é a chave do operador [INPUT/ONTO], sem termo; a cobrança contínua: transmitido e^{{−tβg}} (a face no fluxo; homônimo de `TheDeathOfTheSignal.transmitted`, a lei discreta, outra lei), cobrado 1 − e^{{−tβg}} (o reflexo no fluxo), soma 1 em todo t (trivial por definição); a viscosidade é o atrito constante (d/dt e^{{−tβg}} = −(βg)·e^{{−tβg}}; o coeficiente βg, a regra vezes o contraste, é o NOME [ONTO/DEFINITION] sobre um cálculo); a cobrança nunca se completa (0 < cobrado < 1, `leakage_strictly_loses`); sem testemunha estática plena (apelido); com β da regra o coeficiente é α√e·g. A identificação de βg com Γ_ω = ½βτ★ω² NÃO tem termo: é leitura [ONTO]. "
        "**O livro concreto (runtime):** {n_ledger} cobranças, UMA por lei de leitura, cada desfecho LIDO do core por um modo dito ({by_how}: pelo token do veredito, do módulo ou aninhado; por número lido com a regra dita; ou declarado sem número) e igual ao do PRÉ-REGISTRO DOS DOIS LADOS {pr_label} lido por bytes (JSON `{pr_json16}`, MD `{pr_md16}`; `{pr_id}`; supersede {pr_super} pelos achados das aferições, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq {pr_seq}): {ledger_ids}. Contagens: {counts} ({by_side}); na regra {n_in_rule} ({counts_in_rule}), ao lado {n_beside} (os {eco_n} pares do eco como cópia atrasada — {eco_ext} extintos, {eco_inc} inconclusivos — e o custo posto na face por convenção). O R4 lê um conjunto congelado sem FALSIFIED (o V11), a mesma fonte do degrau experimental do gate. "
        "A leitura P2 dos relógios está EXCLUÍDA por ordens de grandeza sem nσ; R6 é inconclusiva pelo controle de convergência (os parâmetros com N < 50τ têm de ser 0); F2 é inconclusiva pela sistemática da MEDIDA (o viés relativo de τ acima do limiar da emenda V2), NÃO pelo poder — no ramo canônico o poder é ≈ 0, e o 0,2σ é o poder do ramo B, encerrado; F1 tem regra UNILATERAL na lei D1b (falsifica só se o ganho for ≥ +5; o poder prévio dito nas duas réguas); F4 segue a regra de morte CONGELADA (duas determinações independentes; R3 elege o perito, não muda a regra); dos {eco_n} pares do eco como cópia atrasada, {eco_ext} estão EXTINTOS e {eco_inc} inconclusivos (nenhum move a regra); a propagação (R2) aguarda estimador e NÃO tem poder: Γ(100 Hz) = ½βt_Pω² = {r2_gamma} s⁻¹, acumulado sobre 1 Gpc {r2_acc}. "
        "**Identidades de sanidade (não testes):** cos²θ_M = {facew} = 1 − β; sin²θ_M = {reflw} = β; e^{{−β}} = {trans} e 1 − e^{{−β}} = {charged} somam 1; as duas leis homônimas (ângulo e fluxo) são distintas; βg (g = 1) = {visc}; θ_M = {theta} rad; β = {beta} = α√e ({law}, teste). "
        "**Estatuto:** a chave, a ratificação e a correção são do operador [INPUT/ONTO]; as pedras são [KERNEL], com o trivial dito como trivial; o livro é dado lido [REAL]; a identificação de cada observável com δ⟨K_∂⟩ é leitura [ONTO]; o gate `{qg}` ({n18}/18) INALTERADO; a conferência v376 pinada e consumada ({cf_counts}; abertos {abertos}); por termo {hvals}; o ramo B encerrado. PROVADA ≠ CONFIRMADA. Veredito: `{the_ledger_of_charges_v382}`. Leitura do selo: `{the_ledger_of_charges_reading_v382}`."
    ).format(**V)


def rodada_txt(V):
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] "
         "AVISO», sem SEAL_WITHHELD). Conferidor `conferir_rito_v382.py` (a MESMA guarda do rito): **TUDO BATE** — {conf_dm} «deve mudar», {conf_np} "
         "«não pode mudar» (JSON `{conf16}`). `um.py` sha16 `{s16}` ({umb:,} B). Selo `{selo_ts}`.").format(**V)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    return ("## {data} — **v382 SELADA ({compl})** `{s16}` — O LIVRO DE COBRANÇAS (a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra) + ψ com norma 1 e a viscosidade (duas pedras, {kf_n} declarações); "
            "o pré-registro dos dois lados {pr_label} do estimando δ⟨K_∂⟩ lido por hash; o nome do degrau final proposto ao lado; gate intocado\n\n".format(**V) + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    return ("---\n\n## ADENDO — {data} · v382 SELADA ({compl}) `{s16}` — O livro de cobranças e a viscosidade; a TGL é ótica\n\n"
            "- **O que mudou no caminho crítico:** o operador deu a chave (o último elo incide no Hamiltoniano oculto; o custo no reflexo, o pagamento na face), ratificou R1–R6 e corrigiu a visão de lados (a TGL é ótica: lê os dois lados). "
            "A gerência tipou o livro de cobranças (a cobrança com cinco palavras de desfecho impostas pelo tipo; a regra não lê o livro; o gate não lê o livro, pelos probes do runtime; a ótica |T|² + |R|² = 1) e ψ com norma 1 como o zero do lock mínimo sobre o Hamiltoniano oculto, com a viscosidade βg como cobrança contínua: {kf_on}/{kf_n}. O livro concreto: {n_ledger} cobranças, uma por lei de leitura ({counts}; na regra {counts_in_rule}).\n"
            "- **O pré-registro dos dois lados {pr_label}** (`{pr_id}`, JSON `{pr_json16}`; supersede {pr_super} pelos achados das aferições, antes de qualquer estimador ou dado novo): reflexo (o que passa pelo reflexo: escada, propagação, Coma, piso dos vazios; os {eco_n} pares do eco como cópia atrasada — {eco_ext} extintos, {eco_inc} inconclusivos —, ao lado; o R4 sem FALSIFIED no conjunto congelado) e face (o que não passa pelo reflexo: cronômetros, ringdown = RG, relógios P1/P2/P3, neutrino por determinação direta; o fundo vestido, face por convenção, ao lado), com o critério de lado dito cobrança a cobrança; as cláusulas da Fase 6 e das emendas V4/V5 lidas dos arquivos, NA ORDEM, e os acréscimos da casa ditos; a lei transmitida nos cronômetros PENDENTE; cegueira em dois sentidos (análise cega ≠ lado legível); a propagação (R2) aguarda estimador e não tem poder (Γ(100 Hz) = {r2_gamma} s⁻¹).\n"
            "- **O que segue do operador:** a cunhagem definitiva do nome do degrau final (proposto: `{fsn}`); renomear o gate é ato dele. **Por termo (inalterado):** remaining = {remaining}; gpf_H2 / gpf_H3 / gpi_H3 = {hvals}. Gate intocado.\n"
            "- `{s16}`; {teor}.").format(**V)


def atlas(V):
    return ("---\n\n## {data} — v382 SELADA ({compl}): O LIVRO DE COBRANÇAS (A TGL É ÓTICA: LÊ A FACE E O CUSTO; NENHUM DESFECHO MOVE A REGRA) + ψ COM NORMA 1 E A VISCOSIDADE; "
            "O PRÉ-REGISTRO DOS DOIS LADOS {pr_label} POR HASH; O NOME DO DEGRAU FINAL PROPOSTO AO LADO (append datado)\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v382`.")


def topico_missao(V):
    return ("## {data} — v382 SELADA `{s16}` ({teor}; {compl}; gate INTOCADO): o livro de cobranças e a viscosidade tipados — pedras `TheLedgerOfCharges` + `ThePsionAndTheViscosity` ({kf_on}/{kf_n}); "
            "`{the_ledger_of_charges_v382}`; por termo {hvals}. Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[handoff-v382-custodia]].").format(**V)


def topico_central(V):
    return ("**{data} — v382 SELADA ({compl}):** `um.py` `{s16}` ({umb:,} B) sobre a v381 `{base16}`; kernel novo (`TheLedgerOfCharges` {n_loc} + `ThePsionAndTheViscosity` {n_psv}, escada {esc}); {teor}; gate intocado. "
            "O livro de cobranças (a ótica), ψ e a viscosidade, o pré-registro dos dois lados {pr_label} por hash. É a candidata à custódia no lugar da v381 (custódia = ato separado; commit/push é ato do operador).").format(**V)


def topico_regra(V):
    return ("## {data} — v382 SELADA `{s16}`: o livro de cobranças e o psion com a viscosidade tipados (a ligação de Spec S(θ) a HminMic segue [INPUT/ONTO], sem termo)\n\n`TGLExt.TheLedgerOfCharges` + `TGLExt.ThePsionAndTheViscosity` ({kf_on}/{kf_n} no trio; sem sorry): "
            "a cobrança com lado/lei/leitura/desfecho (cinco palavras impostas pelo tipo); a regra não lê o livro (rfl, dito); com uma cobrança extinta a regra segue α√e (a hipótese não entra na prova; «extinguir» é uma definição); o termo P = P (o gate é conferido pelos probes do runtime); a ótica |T|² + |R|² = 1 com os dois complementos (o nome é [ONTO]); ψ = Ω, ‖ψ‖ = 1, HminMic ψ = 0 (o zero do lock mínimo sobre K = −log Δ; trivial por construção), a luz fixa ψ; "
            "a viscosidade βg como atrito constante do fluxo; a cobrança nunca se completa. Runtime: {n_ledger} cobranças ({counts}; na regra {counts_in_rule}); pré-registro `{pr_id}` por hash (JSON `{pr_json16}`); gate inalterado; nome do degrau final proposto ao lado (`{fsn}`). "
            "Veredito `{the_ledger_of_charges_v382}`. Leitura do selo: `{the_ledger_of_charges_reading_v382}`. O que segue [INPUT]: a cunhagem definitiva do nome do degrau final; o estimador da propagação (R2) com o poder dito antes de abrir. PROVADA ≠ CONFIRMADA.").format(**V)


def topico_regimes(V):
    return ("## {data} — v382 SELADA `{s16}`: os dois LADOS se leem nos DOIS regimes (o conteúdo de kernel é a identidade já existente; «nenhum lado é cego» é a correção do operador)\n\n"
            "O conteúdo de kernel: `TheLedgerOfCharges.the_tgl_is_optics_not_semi` — faceWeight + reflectionWeight = 1 e os dois complementos, a identidade já existente do Teorema S-∂ (`normSq_reflection_add_transmission`), lida no ÂNGULO (regime da projeção); "
            "e o seu análogo no FLUXO, `ThePsionAndTheViscosity.the_charge_is_continuous_both_sides` — transmitido + cobrado = 1 em todo t (trivial por definição; regime da face, hiperbólico). Os dois LADOS (face = o pagamento; reflexo = o custo) se leem nos DOIS regimes: "
            "«face» (o lado) e «regime da face» (a direção hiperbólica, o objeto) são HOMÔNIMOS — nunca trocar um pelo outro. «Nenhum lado é cego; o que difere é a lei de cada leitura e o instrumento com poder» é a correção do operador [INPUT/ONTO], não teorema. Veredito `{the_ledger_of_charges_v382}`.").format(**V)


def arvore_linha(V):
    return ("- **O LIVRO DE COBRANÇAS (v382): A TGL É ÓTICA — pedras `TheLedgerOfCharges` + `ThePsionAndTheViscosity` ({kf_on}/{kf_n}, sem sorry): a cobrança (lado, lei, leitura, desfecho em cinco palavras impostas pelo tipo), o livro; a regra β não lê o livro (rfl, dito como trivial); "
            "com uma cobrança extinta a regra segue α√e (a hipótese não entra na prova); o termo P = P (o gate é conferido pelos probes do runtime); a ótica |T|² + |R|² = 1 e os dois complementos (o nome é [ONTO]; «nenhum lado é cego» é a correção do operador); ψ = Ω com ‖ψ‖ = 1, o zero do lock mínimo sobre o Hamiltoniano oculto (trivial por construção), fixo pela luz; a viscosidade βg como atrito constante; a cobrança nunca se completa; o livro concreto: {n_ledger} cobranças ({counts}).** "
            "escada {esc}. `{the_ledger_of_charges_v382}`. **O que NÃO é:** a identificação de βg com Γ ∝ βω² é leitura [ONTO]; a ligação de Spec S(θ) a HminMic é [INPUT/ONTO]; o nome do degrau final é PROPOSTO ao lado (o gate não muda); nada aqui é confirmação; não é por termo ({hvals}).").format(**V)


def verbete(V):
    return ("a v382 responde à chave do operador de 02/10/2026 (" + _CHAVE + "), à ratificação de R1–R6 com a correção «a TGL não é semi, ela é ótica» e à ordem «isso mesmo, prossiga» [INPUT]. " + core_txt(V))


def remissivo(V):
    return ("- **O livro de cobranças (v382): a TGL é ótica, lê a face e o custo; nenhum desfecho move a regra; o gate não lê o livro (probes do runtime) — pedras `TheLedgerOfCharges` + `ThePsionAndTheViscosity` ({kf_on}/{kf_n}); ψ com norma 1 como o zero do lock mínimo sobre o Hamiltoniano oculto; a viscosidade βg; "
            "o pré-registro dos dois lados {pr_label} por hash (`{pr_id}`); o nome do degrau final proposto ao lado; escada {esc}** (v382) · {{ML v382; um.py prove_the_ledger_of_charges_v382; v382_incorporacao_manifesto.json}}").format(**V)
