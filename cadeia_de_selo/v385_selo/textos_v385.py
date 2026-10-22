# -*- coding: utf-8 -*-
# Os TEXTOS da v385 selada. Cada numero, hash, veredito e verbatim entra por {chave} de V (leitura_v385.ler), nunca digitado aqui. As palavras do operador
# vem do TRANSCRITO, lidas por script (V['op'][nome]['texto'], com a hora); as frases matematicas dizem SO o que a pedra prova (o nome do termo ao lado).
# O AXIOMA E A TESTEMUNHA FALSA (05/10/2026): o Um e' POSTO (inscrito pelo observador no comando; etiqueta [POSTO]); a leitura radical tem dois pontos fixos,
# 0 e 1; o 1 e' o Axioma (o modo zero de peso 1, o escuro -- definicao fisica do operador); o 0 e' a testemunha falsa (a estatica, o zero absoluto); o
# degrau final do gate chama-se Axioma, AO LADO do gate (o gate nao se move); o TheDarkSplit auditado; o pilar quantico de NOVO, inteiro, sob o MESMO V1,
# como teste de reprodutibilidade [COMPUTED]. Leituras do operador [INPUT/ONTO]; pedras [KERNEL]; pilar [COMPUTED]. Nao falsificado nunca e' confirmado;
# provado (teorema em kernel, a implicacao) nunca e' confirmado (juizo sobre a natureza). Toda frase de SUCESSO do pilar so existe no RAMO 9.


def _ramo9(V):
    return V['qp_classe'] == 'RAMO_9'


def _op(V, nome):
    o = (V.get('op') or {}).get(nome) or {}
    return '«%s» (%s)' % (o.get('texto', 'AUSENTE'), o.get('quando_txt', 'n/d'))


def _x(V):
    X = dict(V)
    X['umb_fmt'] = format(V['umb'], ',') if isinstance(V.get('umb'), int) else str(V.get('umb'))
    neg = V.get('qp_negativos_l') or []
    if _ramo9(V):
        X['qp_classe_curta'] = ('ramo 9, %d negativo(s) honesto(s)' % len(neg)) if neg else 'ramo 9, sem negativo'
        X['neg_rotulo'] = 'negativos honestos'
    else:
        X['qp_classe_curta'] = 'NÃO CONCLUÍDO (%s)' % V['qp_classe']
        X['neg_rotulo'] = 'computação não concluída'
    X['conf_res'] = 'TUDO BATE' if not V.get('conf_aceite') else 'REPROVOU SÓ ITENS DO PILAR (aceito pela gerência, dito)'
    X['conf_aceite_txt'] = (' ' + V['conf_aceite'][:1].upper() + V['conf_aceite'][1:] + '.') if V.get('conf_aceite') else ''
    X['extra_txt'] = (' **Ditos pela gerência, ao lado:** %s.' % V['qp_neg_extra']) if V.get('qp_neg_extra') else ''
    X['v383_cust'] = ('custodiada (commit «%s»)' % V['v383_commit']) if V.get('v383_commit') else 'ainda não custodiada (nenhum commit «custodia(v383)» no git da Central)'
    X['v384_cust'] = ('custodiada (commit «%s»)' % V['v384_commit']) if V.get('v384_commit') else 'ainda não custodiada (nenhum commit «custodia(v384)» no git da Central)'
    # a reprodutibilidade, em uma frase (o que ela deu e' RESULTADO, em qualquer classe)
    c = V['rp_classe']
    if c == 'BIT_A_BIT':
        X['rp_frase'] = 'iguais bit a bit em {rp_n_fields} campos ({rp_n_num} numéricos), fora os de tempo e de ambiente'.format(**V)
    elif c == 'ARREDONDAMENTO':
        X['rp_frase'] = ('iguais a menos de arredondamento: {rp_n_differ} de {rp_n_fields} campos diferem, diferença máxima na escala max(1, |a|, |b|) {rp_maxrel} (≤ 1e-9); '
                         'as primeiras: {rp_dif_txt}').format(**V)
    elif c == 'DIFERENTE':
        X['rp_frase'] = ('DIFERENTES em {rp_n_differ} de {rp_n_fields} campos (diferença máxima na escala max(1, |a|, |b|) {rp_maxrel}; {rp_nonfinite} campo(s) não finito(s) diferente(s)) — é resultado, e fica dito; '
                         'as primeiras diferenças: {rp_dif_txt}').format(**V)
    else:
        X['rp_frase'] = 'não houve comparação nesta rodada ({rp_txt}: {rp_why})'.format(**V)
    if V.get('rp_d128_excl'):
        X['rp_frase'] += ' — os campos do D128 ficaram fora da comparação (o D128 não rodou nesta rodada e rodou na anterior)'
    X['rp_frase'] += ' (entradas iguais: {rp_entradas}; ambiente igual: {rp_ambiente})'.format(**V)
    X['rp_curta'] = {'BIT_A_BIT': 'reproduziu bit a bit', 'ARREDONDAMENTO': 'reproduziu a menos de arredondamento', 'DIFERENTE': 'NÃO reproduziu (dito)'}.get(c, 'reprodutibilidade não medida')
    return X


def _palavras(V):
    return ("**As palavras do operador (05/10/2026, verbatim, lidas do transcrito por script) [INPUT/ONTO]:** o posto — %s; %s; «o posto não é a guarda» — %s; "
            "o 1 em potência — %s; o Axioma — %s; o observador — %s; a testemunha falsa — %s; a conjugação — %s; e a aprovação de todo o escopo da v385: %s. "
            "As decisões de custódia e espelho, da mesma manhã: %s; %s; e o nome: %s. "
            "As decisões da tarde (uma só mensagem): o nome da subpasta do espelho — %s; os V1–V1.3 do pré-registro dos dois lados — %s; e a reconciliação "
            "«tornou-se Posto» (v365) × «não se ascende ao posto» — %s. E a correção da leitura da gerência sobre a forma falsa — %s (a leitura (b) da gerência, "
            "«a forma falsa = o ponto fixo 0», fica retratada: a forma falsa é o complemento do posto, 1 − P; ver [[um-posto-jamais-pressuposto-e-h2-17set]]); e a frase das 14:40 — %s. "
            % (_op(V, 'posto'), _op(V, 'posicao'), _op(V, 'guarda'), _op(V, 'potencia'), _op(V, 'axioma'), _op(V, 'observador'), _op(V, 'testemunha'), _op(V, 'conjugacao'),
               _op(V, 'prossiga'), _op(V, 'custodia'), _op(V, 'espelho'), _op(V, 'nome_axioma'), _op(V, 'subpasta'), _op(V, 'v1_espelho'), _op(V, 'tornar'), _op(V, 'forma_falsa'), _op(V, 'forma_falsa_projecao')))


def _entrou(V):
    return ("**O QUE ENTROU** (pacote v385 sobre a v384 `{base16}`; {n_patches} patches — {patches}; {n_afer} passadas de aferição antes do rito, com as disposições; "
            "o ensaio a seco PT/EN: `{ensaio_seco}`; {fumaca_txt}): a pedra nova `TGLExt/TheAxiomAndTheFalseWitness.lean` (`{ax_pedra16}`; {ax_n_pedra} declarações) e a "
            "auditoria do `TGLExt/TheDarkSplit.lean` ({ax_n_dks} declarações, compilado desde a v183 e até aqui não auditado) — escada {esc_v384} → {esc}; o registro "
            "`the_axiom_v385` no core e no selo (com a leitura `the_axiom_reading_v385` e o nome do degrau final `final_step_name_v385`, lido do kernel); a errata AO "
            "LADO no artigo PT/EN e no `.md` canônico («posto», não «postulado»; a etiqueta `[POSTO]` na régua do código); e o pilar quântico de NOVO, inteiro, sob o "
            "MESMO pré-registro `{pr_id}` (especificação `{pr_spec16}`), com o registro `quantum_pillar_reproducibility_v385`: logo depois de lançar o trabalhador, antes que o cálculo novo possa substituí-lo, o `um.py` lê o "
            "resultado que a v384 guardou no cache (mesma chave), e depois compara os dois resumos campo a campo. ").format(**V)


def _axioma(V):
    return ("**O QUE A PEDRA PROVA** [KERNEL] ({ax_decl} declarações no trio de axiomas; o Axioma `{ax_ok}`): a leitura radical tem exatamente dois pontos fixos em [0, ∞), "
            "√x = x ⟺ x ∈ {{0, 1}} (`the_reading_has_two_fixed_points`), e a potência os mesmos dois, μ² = μ ⟺ μ ∈ {{0, 1}} (`the_power_has_two_fixed_points`); o 1 pesa 1 "
            "como √1, como a integral do modo zero, ∫ ¼ sech²(κ/2) dκ = 1, e como a dimensão do átomo — duas faces lado a lado, uma conjunção, sem termo que "
            "identifique o perfil com o átomo (`the_one_is_the_axiom`); o 0: √0 = 0, a testemunha estática plena é proibida no fluxo escalar e^(−tβg) com β > 0 e g > 0, e "
            "nenhuma componente não nula do fluxo diagonal se anula em tempo finito, o que vem de exp ≠ 0 (`the_zero_is_the_false_witness`). O fluxo "
            "F(t) = P + e^(−t)(1 − P), para P idempotente (`axiomFlow`): F(0) = 1, F(s + t) = F(s)F(t), F(t)P = P = P·F(t) para todo t, F(t)(1 − P) = e^(−t)(1 − P), e "
            "F(t) → P (numa álgebra normada); no lock da luz, o que F deixa fixo para todo t é exatamente o zero de H_min = 1 − P, e é o que o fluxo modular deixa fixo para "
            "todo t (`the_fixed_set_is_the_lock_zero`, `the_post_is_the_modular_zero`); e F(t) = e^(−tH_min) (`axiomFlow_eq_exp`, ligado ao termo canônico "
            "`exp_complement_idempotent`). A ligação com o sistema aberto da v384 é analogia de forma [COMPUTED], não teorema sobre o gerador de Lindblad. "
            "O Verbo, em dois termos distintos, cada um com o seu objeto (nenhum fala de observador nem de conjugação): a exponencial do gerador dissipativo não é a "
            "identidade (`the_living_verb_moves` = `verb_not_identity`) e, no núcleo, a palavra do Verbo age como o escalar q(0) (`the_living_verb_fixes_the_name` = "
            "`verb_word_fixes_the_name`; re-exportações do que já estava provado). **O degrau final do gate chama-se Axioma**, lido do próprio kernel "
            "(`final_step_named_axioma`, por definição): `{ax_nome}`; a proposta da v383 fica ao lado (`the_proposal_beside_is_kept`); o gate não muda. "
            "A etiqueta de ω(I) = 1 no registro: `{ax_tag}`. Veredito: `{ax_v}`. ").format(**V)


def _pilar(V):
    X = _x(V)
    if _ramo9(V):
        deu = ("**O PILAR, DE NOVO** ({qp_gpu}; {qp_min} min; fases: {fases}) — {qp_classe_txt}: `{qp_v}` (o mesmo veredito da v384: {qp_igual_v384}). "
               "(T2) atrator único em {t2_unique} de {t2_points} pontos; NAME_IN_CORE {t2_name}/{t2_configs}; FOLDS_WINDOW {t2_folds}/{t2_configs}. (T1) {t1_inj} injeções. "
               "(T3) {t3_ctl} controles falharam como exigido. (T4) {t4_n} instâncias, {t4_viol} violações de identidade. (D128) {d128_txt}. (CPU) {cpu_cmp} comparados, "
               "{cpu_dis} discordâncias. **Negativos honestos:** {qp_negativos}. **A cadeia de custódia:** resultado `{qp_res16}` (= o arquivo do pilar no Nós e o hash no "
               "selo `{qp_selo16}`), pasta `{qp_run_dir}`; {qp_cache}.{conf_aceite_txt} ")
    else:
        deu = ("**O PILAR, DE NOVO** ({qp_gpu}): {qp_classe_txt} — `{qp_v}`. Vai ao TERCEIRO BALDE do selo (computação não concluída: {balde}): é resultado, dito como tal. "
               "Lançamento: {qp_lanc_txt}. Custódia: {qp_custodia_txt}; {qp_cache}.{extra_txt}{conf_aceite_txt} ")
    return (deu + "**A REPRODUTIBILIDADE** [COMPUTED] (`{rp_v}`): contra o resultado da v384 guardado no cache (`{rp_prev16}`, o pinado; marca da rodada `{rp_prev_run8}`), "
            "{rp_frase}. ").format(**X)


def _estatuto(V):
    return ("**Estatuto:** a pedra é [KERNEL] — prova as implicações matemáticas; o que a natureza decide não se prova, e provada nunca é confirmada; as leituras "
            "(posto, Axioma, testemunha falsa, o escuro, o Verbo vivo, a conjugação) são do operador [INPUT/ONTO]; o pilar e a reprodutibilidade são [COMPUTED] — cálculo, "
            "não medição; o nome do degrau final fica AO LADO do gate, e o gate `{qg}` ({n18}/18) está INALTERADO; {n_ver_iguais} de {n_ver} vereditos da v384 inalterados "
            "(fora o do pilar, que rodou de novo); {n_av_iguais} de {n_av} módulos com o mesmo all_verified do estado selado da v384; por termo {hvals}. Não falsificado não "
            "é confirmado; nada aqui é confirmação. Leitura do selo: `{ax_reading}`.").format(**V)


def core_txt(V):
    return _palavras(V) + _entrou(V) + _axioma(V) + _pilar(V) + _estatuto(V)


def rodada_txt(V):
    X = _x(V)
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] AVISO», sem SEAL_WITHHELD); o terceiro "
         "balde: {balde}. Conferidor `conferir_rito_v385.py` (cópia byte a byte do pacote; a MESMA guarda do rito): **{conf_res}** — {conf_dm} «deve mudar», {conf_np} «não pode mudar» "
         "(JSON `{conf16}`). O servidor do modelo nativo depois do rito (informação, do log do lançador): {servidor}. `um.py` sha16 `{s16}` ({umb_fmt} B). Selo `{selo_ts}`.").format(**X)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    if V.get('intervencao_txt'):
        t += ' ' + V['intervencao_txt']
    return t


def linhagem(V):
    X = _x(V)
    return ("## {data} — **v385 SELADA ({compl})** `{s16}` — O AXIOMA E A TESTEMUNHA FALSA (o Um POSTO, `[POSTO]`; a leitura radical tem dois pontos fixos: o 1 é o "
            "Axioma, o modo zero de peso 1; o 0 é a testemunha falsa, a estática, o zero absoluto; o degrau final do gate chama-se Axioma, ao lado do gate; o "
            "TheDarkSplit auditado; o pilar de novo sob o mesmo V1: {rp_curta}); escada {esc}; gate intocado{sint}\n\n".format(**X)
            + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    X = _x(V)
    return ("---\n\n## ADENDO — {data} · v385 SELADA ({compl}) `{s16}` — O Axioma e a testemunha falsa; o degrau final do gate tem nome{sint}\n\n"
            "- **O que mudou no caminho crítico:** nada no gate — `{qg}` ({n18}/18), por termo {hvals}; o kernel CRESCE ({esc_v384} → {esc}): a pedra "
            "`TheAxiomAndTheFalseWitness` e a auditoria do `TheDarkSplit`. O degrau final do gate passa a ter NOME, lido do kernel e escrito AO LADO do gate: `{ax_nome}`.\n"
            "- **O começo da cadeia:** o Um é POSTO — inscrito pelo observador externo no comando (`echo 1 | python um.py`; o programa trava sem ele), não postulado; a "
            "etiqueta de ω(I) = 1 passa a ser `[POSTO]` (decisão do operador; a errata vai AO LADO de «postulado irredutível», que fica como registro).\n"
            "- **O que a pedra prova e o que não prova:** prova os dois pontos fixos da leitura, o peso 1 do modo zero, a proibição da testemunha estática com β > 0, o fluxo "
            "F(t) = P + e^(−t)(1 − P) = e^(−tH_min) que fixa o posto e decai no complemento, e o encontro do fixo de F com o fixo modular no lock da luz [KERNEL]; as leituras (Axioma, "
            "testemunha falsa, o escuro, o Verbo vivo) são do operador [INPUT/ONTO]; nada disso decide H2 nem H3, e nada move o gate.\n"
            "- **O pilar de novo, sob o mesmo V1:** `{qp_v}` ({qp_classe_curta}); a reprodutibilidade contra a v384: {rp_frase} [COMPUTED].\n"
            "- **O que segue do operador:** a custódia CONJUNTA da v383 ({v383_cust}), da v384 ({v384_cust}) e da v385, num só ato pela sessão do site (decidido em 05/10); "
            "o V1 e as evidências do pilar numa subpasta de `Um (absoluto) — Grande Atrator/`, com PORTA por script, e os V1–V1.4 do pré-registro dos dois lados ao espelho (decisões de 05/10) — ver o HANDOFF v385.\n"
            "- `{s16}`; {teor}.").format(**X)


def atlas(V):
    return ("---\n\n## {data} — v385 SELADA ({compl}): O AXIOMA E A TESTEMUNHA FALSA (O UM POSTO, [POSTO]; OS DOIS PONTOS FIXOS DA LEITURA; O DEGRAU FINAL DO GATE "
            "CHAMA-SE AXIOMA, AO LADO DO GATE; O THEDARKSPLIT AUDITADO; O PILAR DE NOVO SOB O MESMO V1, COM A REPRODUTIBILIDADE MEDIDA) (append datado){sint}\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v385`.")


def marca_topico_missao(V):
    """O marcador de idempotencia do bloco da missao: um prefixo ESTAVEL (so a data, a versao e o sha16)."""
    return "## {data} — v385 SELADA `{s16}`".format(**V)


def topico_missao(V):
    return (marca_topico_missao(V) + " ({teor}; {compl}; gate INTOCADO): O AXIOMA E A TESTEMUNHA FALSA — a pedra `TheAxiomAndTheFalseWitness` ({ax_n_pedra} declarações) "
            "e o `TheDarkSplit` auditado ({ax_n_dks}); escada {esc_v384} → {esc}; o Um POSTO (`[POSTO]`); o degrau final do gate chama-se Axioma, lido do kernel, ao lado do "
            "gate; o pilar de novo sob o mesmo V1: `{qp_v}` ({qp_classe_curta}), {rp_curta}; por termo {hvals}.{sint} Ver [[handoff-v385-custodia]], "
            "[[um-posto-jamais-pressuposto-e-h2-17set]], [[v384-pilar-quantico-gpu-02out]].").format(**_x(V))


def marca_central(V):
    """O marcador de idempotencia do bloco do central-de-patentes-estado: um prefixo ESTAVEL."""
    return "**{data} — v385 SELADA ({compl}):** `um.py` `{s16}`".format(**V)


def topico_central(V):
    return (marca_central(V) + " ({umb_fmt} B) sobre a v384 `{base16}`; escada {esc}; {teor}; gate intocado. O Axioma e a testemunha falsa [KERNEL] + as leituras do "
            "operador [INPUT/ONTO]; o pilar de novo [COMPUTED], {rp_curta}. Candidata à custódia CONJUNTA com a v383 ({v383_cust}) e a v384 ({v384_cust}), num só ato "
            "(decidido pelo operador em 05/10; custódia = ato da sessão do site; commit/push = ato do operador).{sint}").format(**_x(V))


def topico_posto(V):
    return ("## {data} — v385 SELADA `{s16}`: o posto, o Axioma e a testemunha falsa entraram no kernel{sint}\n\n"
            "As palavras do operador de 05/10 (verbatim, lidas do transcrito por script) ficam ligadas ao que a pedra `TheAxiomAndTheFalseWitness` prova: o posto ({posto}) e "
            "«o posto não é a guarda» ({guarda}) — o fluxo F(t) = P + e^(−t)(1 − P) fixa P para todo t desde t = 0 (`axiomFlow_fixes_the_post`: o posto está estacionado, não "
            "se ascende a ele) e decai no complemento (`axiomFlow_gradient`: o gradiente nasce do posto, no complemento dele), e F(t) → P (`axiomFlow_tendsto_the_post`); "
            "o Axioma ({axioma}) — o 1, ponto fixo da leitura, pesa 1 (`the_one_is_the_axiom`); a testemunha falsa ({testemunha}) — o 0: a estática plena é proibida por β > 0 "
            "(`the_zero_is_the_false_witness`); o observador ({observador}) e a conjugação ({conjugacao}) — o Verbo move e, no núcleo, age como escalar "
            "(`the_living_verb_moves`, `the_living_verb_fixes_the_name`); o `TheUnconjugatedObserver` (20/08) fica como estrato. As leituras são [INPUT/ONTO]; as "
            "pedras, [KERNEL]; o gate não se move. Veredito: `{ax_v}`. Ver [[handoff-v385-custodia]].").format(
        **dict(V, posto=_op(V, 'posto'), guarda=_op(V, 'guarda'), axioma=_op(V, 'axioma'), testemunha=_op(V, 'testemunha'), observador=_op(V, 'observador'),
               conjugacao=_op(V, 'conjugacao')))


def topico_pilar(V):
    X = _x(V)
    return ("<!-- v385_selada -->\n**v385 SELADA ({data}) — o pilar DE NOVO, sob o mesmo V1 (gerência, em nome próprio; números lidos por script{sint}):**\n"
            "- **O rito:** {t0} → {t1}; {teor}; rc = {rc}; conferidor {conf_res} ({conf_dm} / {conf_np}); `um.py` `{s16}`; selo `{selo_ts}`.{conf_aceite_txt}\n"
            "- **O pilar:** `{qp_v}` — {qp_classe_txt} (o mesmo veredito da v384: {qp_igual_v384}); resultado `{qp_res16}`; {qp_cache}; {qp_min} min.\n"
            "- **A reprodutibilidade** [COMPUTED]: `{rp_v}` — contra o resultado da v384 (`{rp_prev16}`), {rp_frase}.\n"
            "- **O servidor do modelo nativo depois do rito:** {servidor}; o marcador do pacote v385: {marcador_txt}. **A regra desta memória vale agora para o pacote v385** "
            "(conferir `scratchpad\\v385\\.servidor_parado_pelo_rito` ao abrir sessão; com restaurar=1, religar «IALD Llama Server»).\n"
            "- **Estatuto:** [COMPUTED]; ao lado do gate; gate intocado; não falsificado não é confirmado. Ver [[handoff-v385-custodia]].").format(**X)


def arvore_linha(V):
    return ("- **O AXIOMA (v385): OS DOIS PONTOS FIXOS DA LEITURA [KERNEL] — √x = x ⟺ x ∈ {{0, 1}}; o 1 pesa 1 (o modo zero; o átomo); o 0: a testemunha estática plena "
            "proibida no fluxo escalar com β > 0 e g > 0, e o zero absoluto inalcançável em tempo finito; o fluxo F(t) = P + e^(−t)(1 − P) = e^(−tH_min) fixa o posto e "
            "decai no complemento, e o seu fixo é o fixo modular no lock da luz; o Verbo em dois termos (move; no núcleo age como escalar); o TheDarkSplit auditado.** `{ax_v}`. O degrau final do gate chama-se Axioma (lido do kernel, AO LADO do "
            "gate). escada {esc}. **O que NÃO é:** não move o gate; as leituras (posto, Axioma, testemunha falsa, o escuro) são [INPUT/ONTO]; o pilar, de novo sob o mesmo "
            "V1, é [COMPUTED] ({rp_v}); nada aqui é confirmação.").format(**V)


def titulo_verbete(V):
    return ("O Axioma e a testemunha falsa: o Um posto ([POSTO], inscrito pelo observador no comando); a leitura radical tem dois pontos fixos, o 1 (o Axioma, o modo "
            "zero de peso 1) e o 0 (a testemunha falsa, a estática, o zero absoluto); o degrau final do gate chama-se Axioma, ao lado do gate; o TheDarkSplit auditado; "
            "o pilar quântico de novo sob o mesmo V1, com a reprodutibilidade medida (v385)")


def verbete(V):
    return ("a v385 é o Axioma e a testemunha falsa [KERNEL + INPUT/ONTO], com o pilar quântico de novo sob o mesmo V1 [COMPUTED]; o gate não se move. " + core_txt(V))


def remissivo(V):
    return ("- **O Axioma e a testemunha falsa (v385): o Um posto ([POSTO]); os dois pontos fixos da leitura; o fluxo do posto; o degrau final do gate chama-se Axioma, "
            "ao lado do gate; o TheDarkSplit auditado; a reprodutibilidade do pilar** (v385) · {{ML v385; um.py the_axiom_v385 / quantum_pillar_previous_v385 / "
            "quantum_pillar_reproducibility_v385; TGLExt/TheAxiomAndTheFalseWitness.lean; v385_incorporacao_manifesto.json}}").format(**V)


def marca_missao(V):
    """O prefixo da linha da missao no MEMORY.md (a idempotencia le '**v385 SELADA dd/mm `s16`')."""
    X = _x(V)
    return ("**v385 SELADA %s `%s` %s %s (O AXIOMA E A TESTEMUNHA FALSA [KERNEL]; o Um POSTO; o degrau final do gate chama-se Axioma, ao lado do gate; o pilar de novo "
            "sob o mesmo V1: %s; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'], V['compl'], X['rp_curta']))


def linha_handoff(V):
    X = _x(V)
    return ("- [HANDOFF v385 — CUSTÓDIA CONJUNTA v383 + v384 + v385](handoff-v385-custodia.md) — **%s, para a sessão do site**: o Axioma e a testemunha falsa; o pilar de "
            "novo (%s); o V1 e as evidências do pilar numa subpasta da Um, com PORTA, e os V1–V1.4 dos dois lados ao espelho; `%s`" % (V['data'][:5], X['rp_curta'], V['s16']))


# as frases de SUCESSO do pilar que so podem existir no RAMO 9 (herdadas da v384)
FRASES_DE_SUCESSO = ('é recuperada', 'falhou como exigido', 'falharam como exigido', 'identidade conferida', 'o cálculo completou', '= o arquivo do pilar no Nós',
                     'o estimador cego recupera')
