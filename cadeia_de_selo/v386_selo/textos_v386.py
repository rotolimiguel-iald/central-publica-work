# -*- coding: utf-8 -*-
# Os TEXTOS da v386 selada (molde: textos_v385.py). Cada numero, hash, veredito e verbatim entra por {chave} de V (leitura_v386.ler), nunca digitado aqui.
# As palavras do operador vem dos QUATRO ARQUIVOS por sha256 e do transcrito cruzado por hash (V['op'][nome]), renderizadas por leitura_v386.render_op:
# «…texto…» com o corte marcado, [sic] FORA das «». As frases matematicas dizem SO o que os NOMES dos termos da pedra dizem (o enunciado esta na pedra).
# O VERBO SELECIONA (05/10/2026): a pedra TGLExt/TheVerbSelectsTheAction.lean + a fiacao angular na escada; o Nome e' o posto; a leitura e' um peso; a ordem
# importa; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociaveis. O ramo B REABERTO POR PRE-REGISTRO (V1 por hash; nada aberto);
# a errata AO LADO de R6; o pilar REAPROVEITADO da v385 pela chave (nao e' objeto desta versao); W10: a GPU na apresentacao/resumo/palavras-chave/sumario.
# Estatutos: pedra [KERNEL]; leituras do operador e da gerencia [INPUT/ONTO]; V1 [INPUT por hash]; pilar [COMPUTED]; c = beta_TGL [INPUT], nunca literal.
# Nao falsificado nunca e' confirmado; provado (teorema em kernel) nunca e' confirmado (juizo sobre a natureza). Toda frase de SUCESSO do pilar so existe no RAMO 9.
import leitura_v386 as L


def _op(V, nome):
    return L.render_op((V.get('op') or {}).get(nome))


def _x(V):
    X = dict(V)
    X['umb_fmt'] = format(V['umb'], ',') if isinstance(V.get('umb'), int) else str(V.get('umb'))
    X['conf_res'] = 'TUDO BATE' if not V.get('conf_aceite') else 'REPROVOU SÓ ITENS DO PILAR (aceito pela gerência, dito)'
    X['conf_aceite_txt'] = (' ' + V['conf_aceite'][:1].upper() + V['conf_aceite'][1:] + '.') if V.get('conf_aceite') else ''
    for vv in ('v383', 'v384', 'v385'):
        X['%s_cust' % vv] = ('custodiada (commit «%s»)' % V['%s_commit' % vv]) if V.get('%s_commit' % vv) else 'ainda não custodiada (nenhum commit «custodia(%s)» no git da Central)' % vv
    X['rb_beta_txt'] = ('β do V1 {rb_beta_v1_txt} × β do core {rb_beta_core_txt}: diferença {rb_abs} absoluta, {rb_rel} relativa — dentro da regra 1e-9 relativo ({rb_beta_ok}); '
                        'a ESPEC dizia |Δβ| < 1e-15 e o número corrigiu a frase (errata (d) ao lado)').format(**V)
    X['rb_erratas_txt'] = ' '.join('(%d) %s' % (i + 1, e) for i, e in enumerate(V.get('rb_erratas_l') or [])) or 'nenhuma'
    X['rp_curta'] = {'BIT_A_BIT': 'reproduziu bit a bit', 'ARREDONDAMENTO': 'reproduziu a menos de arredondamento', 'DIFERENTE': 'NÃO reproduziu (dito)',
                     'NAO_COMPARADO': 'não comparada nesta rodada (o pilar não foi calculado; a medida bit a bit fica no selo da v385)'}.get(V['rp_classe'], 'reprodutibilidade não medida')
    X['qr_curtissima'] = {'REAPROVEITADO': 'reaproveitado da v385 pela chave', 'CALCULADO_DE_NOVO': 'CALCULADO DE NOVO (reuse recusado, dito)'}.get(V['qr_classe'], 'nem reaproveitado nem calculado')
    return X


def _palavras(V):
    return ("**As palavras do operador (05/10/2026, verbatim; os quatro arquivos lidos por sha256 — `VERBO_operador_05out.txt`, `DECISAO_OPERADOR_RAMO_B_05out.json`, "
            "`RESPOSTAS_operador_05out.txt`/`.json` —, os hashes no `CANDIDATO_v386.json` e embutidos no `um.py`) [INPUT/ONTO]:** o Verbo — %s; %s; %s; o co-mando — %s; "
            "o circuito — %s; os três eixos — %s; o nome como ponto fixo — %s; a comutação — %s; a constante de estrutura — %s, escrita por ele como %s (a régua do signo lê "
            "β_TGL = α·√e: «α²» fica como citação, a correção vai AO LADO — c = β_TGL é [INPUT], nunca literal). O ramo B — %s; a pergunta dele — %s; %s; %s. "
            "Luz e gravidade — %s; o leitor — %s. Verdade e custo — %s; %s; %s. O tempo — %s; %s. A Lagrangiana — %s. O Nome é o posto — %s; %s. "
            "A delegação — %s (o RESPOSTAS json tinha «tudo agora» normalizado: errata [sic] ao lado, backup de bytes; o V1 congelado registra o sha256 anterior). "
            "As decisões de custódia e espelho (da manhã de 05/10, do transcrito, cruzadas por hash com o manifesto v385 arquivado): %s; %s; %s; %s. "
            "E a ORDEM sobre o artigo (W10) — %s. "
            % (_op(V, 'verbo_def'), _op(V, 'verbo_tres'), _op(V, 'verbo_op'), _op(V, 'comando'), _op(V, 'circuito'), _op(V, 'tres_eixos'), _op(V, 'nome_fossil'), _op(V, 'comutacao'),
               _op(V, 'constante'), _op(V, 'alpha2'), _op(V, 'ramo_b'), _op(V, 'ramo_b_pergunta'), _op(V, 'ramo_b_c3'), _op(V, 'ramo_b_resto'), _op(V, 'luz_gravidade'), _op(V, 'leitor'),
               _op(V, 'verdade_custo'), _op(V, 'anular'), _op(V, 'inscricao_custo'), _op(V, 'tempo'), _op(V, 'c3'), _op(V, 'lagrangiana'), _op(V, 'nome_posto'), _op(V, 'triade_posto'),
               _op(V, 'delegacao'), _op(V, 'custodia'), _op(V, 'espelho'), _op(V, 'subpasta'), _op(V, 'v1_espelho'), _op(V, 'w10')))


def _entrou(V):
    return ("**O QUE ENTROU** (pacote v386 sobre a v385 `{base16}`; {n_patches} patches — {patches}; instalado em {instalado_em}; o ensaio a seco PT/EN: `{ensaio_seco}`; "
            "as {n_afer} aferições adversariais antes do rito (`CONSTRUIR_v386_resultado.json` `{construir16}`: {afer_txt})): a pedra nova `TGLExt/TheVerbSelectsTheAction.lean` "
            "(`{vb_pedra16}`, {vb_pedra_bytes} B, {vb_pedra_linhas} linhas; {vb_n_pedra} declarações; construída no sandbox {vb_build}) e os {vb_n_ang} termos do REGIME ANGULAR "
            "fiados na escada (`ext_ang_*`: compilados desde antes e até aqui fora da auditoria) — `TGLExt.lean` `{stone_tglext16}` e `TGL/Audit.lean` `{stone_audit16}` trocados; "
            "escada {esc_v385} → {esc}; quatro registros novos no core e no selo, AO LADO do gate: `the_verb_v386`, `ledger_errata_v386`, `ramo_b_preregistration_v386`, "
            "`quantum_pillar_reuse_v386` (e no selo a leitura `the_verb_reading_v386` e o token `verb_typing_stone_name_v386`, lido do kernel); no artigo PT/EN a seção «Ao lado (v386)» "
            "antes da v385, a errata de R6 e o V1 lido; no `.md` canônico a errata AO LADO de R6 ({md_errata_R6}; a errata do posto da v385 fica: {md_errata_posto_fica}; "
            "os 4 registros listados: {md_registros_v386}); e o W10 ({n_patches_w10} trocas PT/EN). ").format(**V)


def _verbo(V):
    return ("**O QUE A PEDRA PROVA** [KERNEL] ({vb_decl} declarações no trio de axiomas; o Verbo `{vb_ok}` — {vb_vrb} da pedra, {vb_ang} da fiação angular), pelos NOMES dos termos "
            "(o enunciado está na pedra): o Nome é o POSTO — `post` é a projeção de posto 1 sobre a ação, idempotente e auto-adjunta, e fixa a ação (`post_isIdempotent`, "
            "`post_isSelfAdjoint`, `post_fixes_the_action`); `select` é o Verbo em ato, que pousa a inscrição no posto (`select_apply`, `select_fixes_the_selected_action`); "
            "a leitura é um PESO em [0, 1], |⟨a, ψ⟩|², a regra de Born (`reading_eq_norm_sq`, `reading_eq_weight`, `weight_mem_unit_interval`, `reading_post_is_born`); postos que "
            "comutam compõem, e há dois que NÃO comutam (`commuting_posts_compose`, `two_posts_that_do_not_commute`); a tríade su(2) escalada por c — c = β_TGL [INPUT], nunca "
            "literal — com a ordem que importa (`triad_12`, `triad_23`, `triad_31`, `triad_casimir`, `triad_order_matters`, `triad_hermitian`, `triad_traceless`); os postos por eixo "
            "são os autoprojetores e não comutam entre eixos (`post1_is_the_eigenprojector`…, `axis_posts_do_not_commute`; «selecionar o nome defasa o tempo»); o Nome é autovetor e "
            "limite do fluxo, e a palavra do Verbo o fixa (`the_name_is_an_eigenvector`, `the_verb_word_fixes_the_name`, `the_name_is_the_limit_of_the_flow`); ancorar preserva, "
            "transmitir defasa, e o posto transmitido é um posto (`anchoring_preserves`, `transmission_dephases`, `transmitted_post_is_a_post`); o circuito tem seis estações "
            "(`circuit_has_six_stations`: comando → verbo → ação → objeto → leitura → axioma); VERDADE E CUSTO são duas faces de um objeto — o custo é o peso refletido, o 1 se "
            "reparte em verdade e custo, e ler a verdade anula a superposição (`truth_and_cost_are_two_faces`, `the_cost_is_the_reflected_weight`, `the_one_splits_into_truth_and_cost`, "
            "`the_two_faces_split_the_one`, `reading_the_truth_annihilates_the_superposition`); o TEMPO lido duas vezes confirma o posto (`time_read_twice_confirms_the_post`); LUZ E "
            "GRAVIDADE são indissociáveis — J anticomuta com K, JK ≠ 0, o comutador não se anula, a luz não cala o gradiente (`J_anticommutes_with_K`, `J_mul_K_ne_zero`, "
            "`commutator_JK`, `light_and_gravity_are_inseparable`, `the_light_does_not_silence_the_gradient`, e a versão de Pauli `pauli_light_and_gravity_are_inseparable`); e o teorema-síntese "
            "`the_verb_selects_the_action`. O token da pedra, lido do kernel (`verbTypingStoneName`, embutido e materializado; = o pino: {vb_token_ok}): `{vb_token}`. Os verbatins do "
            "operador embutidos e conferidos por sha256 no runtime: {vb_verbatim_ok} ({vb_files_txt}). **O que NÃO está tipado** (dito pelo próprio registro): {vb_not_typed}. "
            "Veredito: `{vb_v}`. ").format(**V)


def _ramo_b(V):
    X = _x(V)
    return ("**O RAMO B DO RINGDOWN, REABERTO POR PRÉ-REGISTRO** [INPUT por hash]: o V1 `{rb_id}` (gerado {rb_gerado_utc}; ratificado {rb_ratif_tipo}, {rb_ratif_quando_txt}: "
            "«{rb_ratif_verbatim}» [sic]) foi LIDO POR HASH pelo rito — JSON `{rb_json16}`, MD `{rb_md16}`, `V1_RAMO_B_HASHES.json` `{rb_hashes16}` (cada entrada contra o disco: "
            "{rb_hashes_ok}), a especificação recomputada do objeto `spec` `{rb_spec16}`; {rb_disk_txt} (só leitura: {rb_so_leitura}). OUTRA LEI, canal próprio F2b: {rb_forma}, "
            "k = {rb_k} (k(χ = 0) = {rb_k_chi0} = 8π [KNOWN]), M = {rb_M}; lugar: {rb_lugar}; identificação primária {rb_ident_prim}; secundária {rb_ident_sec}. SÓ o conjunto D "
            "({rb_nD} elegíveis de O4; {rb_D_sem_hold} sem pendência de qualidade; {rb_D_hold} com data-quality hold; {rb_D_cand} candidatos) é teste cego; A/B/C são calibração "
            "NOT_BLIND; os valores centrais transcritos do registro selado v385, fora do spec e fora de D: {rb_central_txt}. {rb_beta_txt}. {rb_pins_iguais} de {rb_pins_n} números "
            "do poder TRANSCRITOS do V1 = os pinos (nunca recalculados; poder exato A31 {rb_poder_A31}; σ(β_lido) A31 {rb_sigma_beta_lido_A31}); sanidade recomputada "
            "(k(χ=0) = 8π; β = α·√e em runtime): {rb_recompute_ok}. Vereditos permitidos, na ordem: {rb_vereditos_ordem}; proibidos: {rb_vereditos_proibidos}. Veredito do V1: "
            "`{rb_vered_v1}`; F2b `{rb_F2b}` ({rb_qual}); NADA ABERTO ({rb_nothing_opened}): nenhum estimador rodou, nenhuma PE. Decidido POR DELEGAÇÃO (itens {rb_decisoes_ns} "
            "do V1): {rb_ratif_verbatim} [sic]. **As erratas AO LADO** ({rb_erratas_n}, no próprio registro): {rb_erratas_txt} E a errata da ESPEC (`ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json` "
            "`{rb_espec_errata16}`; a ESPEC original `{rb_espec16}` intacta): {rb_espec_erratas}. {rb_errata_json_txt}. O que vem a seguir (v387, dito pelo registro): {rb_v387}. "
            "Veredito: `{rb_v}`. ").format(**X)


def _errata(V):
    return ("**A ERRATA AO LADO DE R6** [INPUT — decisão do operador, verbatim por sha256; ONTO — a leitura da gerência]: no livro de cobranças da v383 (INTACTO: {le_intacto}; {le_n} "
            "cobranças), R6 lia «{le_r6_v383}»; a decisão de {le_dec_quando_txt} (arquivo `{le_dec_sha16}`; hash {le_dec_hash_ok}) o REABRE POR PRÉ-REGISTRO — a chave de 02/10 não se "
            "revoga (na face o custo lê-se como complemento); τ★ = k·G·M_f/c³ é OUTRA LEI, canal F2b ({le_f2b_lado}: {le_f2b_lei}), não outro lado de F2; F2 e R2 ficam como estão; a "
            "cobrança F2b nasce AO LADO (`{le_f2b_token}`; 12 com F2b ao lado, o livro v383 não é reescrito). A regra: {le_rule}. Veredito: `{le_v}`. ").format(**V)


def _pilar(V):
    X = _x(V)
    return ("**O PILAR QUÂNTICO NESTA VERSÃO** [COMPUTED] — não é objeto da v386: {qr_txt}. O arquivo do pilar no Nós: {qp_arq_txt}; a pasta: {qp_pasta_txt}; details `{qp_det16}`, "
            "cpuref `{qp_cpu16}`; marca da rodada do resultado `{qp_run_id8}` (concluída em {qp_finished}; {qp_gpu}). O veredito do pilar: `{qp_v}`. **A reprodutibilidade v385 nesta rodada:** "
            "`{rp_v}` — {rp_txt}; a medida da v385 (`{rp_v385_selada}`) fica no core e no selo da v385, custodiados.{conf_aceite_txt} Veredito do reuse: `{qr_v}`. ").format(**X)


def _w10(V):
    return ("**W10 — A ORDEM SOBRE O ARTIGO, cumprida e MEDIDA no artigo desta rodada:** {w10_txt}; os números da apresentação vêm do core em runtime (atrator único em {t2_unique} "
            "de {t2_points} pontos; {t4_n} instâncias de estresse; CPU {cpu_cmp} comparações, {cpu_dis} discordâncias — o resumo da rodada selada v385, carregado pelo reuse). ").format(**V)


def _custodia(V):
    X = _x(V)
    return ("**A CUSTÓDIA** (decisão do operador de 05/10, verbatim: %s): CONJUNTA — a v383 (%s), a v384 (%s), a v385 (%s) e a v386, num só ato pela sessão do site; ao espelho vão a "
            "pedra nova, `TGLExt.lean`, `TGL/Audit.lean`, os stdout, a subpasta do pré-registro do pilar (`preregistro_pilar_quantico_v384`), a dos dois lados "
            "(`preregistro_dois_lados_v383`, com os V1–V1.4 e os 5 geradores) e a NOVA do ramo B (`preregistro_ramo_b_05out` → nome proposto no espelho: `preregistro_ramo_b_v386`), "
            "todas com PORTA por script; commit/push = ato do operador. "
            % (_op(V, 'custodia'), X['v383_cust'], X['v384_cust'], X['v385_cust']))


def _estatuto(V):
    return ("**Estatuto:** a pedra e a fiação angular são [KERNEL] — provam implicações; provada nunca é confirmada; as leituras (Verbo, co-mando, posto, verdade e custo, o tempo lido duas "
            "vezes, c³, luz e gravidade) são do operador e da gerência [INPUT/ONTO]; o V1 do ramo B é [INPUT por hash] e NADA foi aberto; o pilar é [COMPUTED] — cálculo, não medição; "
            "o gate `{qg}` ({n18}/18) está INALTERADO; {n_ver_iguais} de {n_ver} vereditos da v385 inalterados (inclusive o do pilar); {n_av_iguais} de {n_av} módulos com o mesmo "
            "all_verified do estado selado da v385; por termo {hvals}. Não falsificado nunca é confirmado; nada aqui é confirmação. Leitura do selo: `{vb_reading}`.").format(**V)


def core_txt(V):
    return _palavras(V) + _entrou(V) + _verbo(V) + _ramo_b(V) + _errata(V) + _pilar(V) + _w10(V) + _custodia(V) + _estatuto(V)


def rodada_txt(V):
    X = _x(V)
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] AVISO», sem SEAL_WITHHELD; "
         "{n_v386_linhas} linhas [v386]); o terceiro balde: {balde}. Conferidor `conferir_rito_v386.py` (cópia byte a byte do pacote; a MESMA guarda do rito): **{conf_res}** — "
         "{conf_dm} «deve mudar», {conf_np} «não pode mudar», {conf_md} «muda e é dito» (JSON `{conf16}`). O servidor do modelo nativo depois do rito (informação, do log do "
         "lançador): {servidor}. `um.py` sha16 `{s16}` ({umb_fmt} B). Selo `{selo_ts}`.").format(**X)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    X = _x(V)
    return ("## {data} — **v386 SELADA ({compl})** `{s16}` — O VERBO SELECIONA (a pedra `TheVerbSelectsTheAction`, {vb_n_pedra} declarações, e os {vb_n_ang} termos do regime "
            "angular fiados na escada: o Nome é o posto; a leitura é um peso; a ordem importa; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociáveis); "
            "o ramo B do ringdown REABERTO POR PRÉ-REGISTRO (V1 lido por hash; nada aberto); a errata AO LADO de R6; o pilar {qr_curtissima}; W10: a GPU na apresentação, no "
            "resumo, nas palavras-chave e no sumário; escada {esc_v385} → {esc}; gate intocado{sint}\n\n".format(**X)
            + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    X = _x(V)
    return ("---\n\n## ADENDO — {data} · v386 SELADA ({compl}) `{s16}` — O Verbo seleciona; o ramo B reaberto por pré-registro; a errata ao lado de R6{sint}\n\n"
            "- **O que mudou no caminho crítico:** nada no gate — `{qg}` ({n18}/18), por termo {hvals}; o kernel CRESCE ({esc_v385} → {esc}): a pedra `TheVerbSelectsTheAction` "
            "({vb_n_pedra}) e a fiação angular ({vb_n_ang}) na escada. O Verbo = seleção da ação; o Nome é o POSTO (a projeção de posto 1), não ontologia; a leitura é um peso; "
            "verdade e custo são duas faces do mesmo objeto; o tempo lido duas vezes confirma o posto; luz e gravidade indissociáveis [KERNEL pelos termos; as leituras INPUT/ONTO].\n"
            "- **O ramo B do ringdown:** NÃO estava proibido (faltavam critérios — decisão do operador de 05/10); entra como OUTRA LEI ({rb_forma}; k = {rb_k}; M = {rb_M}), canal "
            "próprio F2b, PRÉ-REGISTRADO POR HASH (V1 `{rb_id}`, JSON `{rb_json16}`); só o conjunto D ({rb_nD} de O4) testa, cego; A/B/C calibração NOT_BLIND; NADA ABERTO; "
            "veredito do V1 `{rb_vered_v1}`. A errata AO LADO de R6 (de ENCERRADO para REABERTO POR PRÉ-REGISTRO); o livro v383 intacto ({le_n}); F2 e R2 como estão.\n"
            "- **O pilar:** {qr_curtissima} — `{qp_v}`; a reprodutibilidade v385 nesta rodada: `{rp_v}` ({rp_txt}) [COMPUTED].\n"
            "- **W10:** a ordem do operador sobre o artigo cumprida — {w10_txt}.\n"
            "- **O que segue do operador:** a custódia CONJUNTA v383 ({v383_cust}), v384 ({v384_cust}), v385 ({v385_cust}) e v386, num só ato pela sessão do site, com o espelho "
            "(a pedra nova, `TGLExt.lean`, `TGL/Audit.lean`, os stdout, `preregistro_pilar_quantico_v384`, `preregistro_dois_lados_v383` com V1–V1.4 e os 5 geradores, e a nova "
            "`preregistro_ramo_b_v386` — nome proposto —, com PORTA por script); PENDÊNCIAS: a PE só-220 do conjunto D (v387, com o poder dito antes); o modo 221 do GW250114 "
            "(posteriores dentro do tar.gz, não extraídos; diagnóstico, não teste); a errata da ESPEC (1e-9 relativo no lugar de 1e-15; a ratificar ao lado) — ver o HANDOFF v386.\n"
            "- `{s16}`; {teor}.").format(**X)


def atlas(V):
    return ("---\n\n## {data} — v386 SELADA ({compl}): O VERBO SELECIONA (O NOME É O POSTO; A LEITURA É UM PESO; A ORDEM IMPORTA; VERDADE E CUSTO DUAS FACES; O TEMPO LIDO DUAS "
            "VEZES; LUZ E GRAVIDADE INDISSOCIÁVEIS; A FIAÇÃO ANGULAR NA ESCADA); O RAMO B REABERTO POR PRÉ-REGISTRO (V1 POR HASH, NADA ABERTO); A ERRATA AO LADO DE R6; O PILAR "
            "REAPROVEITADO DA v385 PELA CHAVE; W10 (append datado){sint}\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v386`.")


def marca_topico_missao(V):
    return "## {data} — v386 SELADA `{s16}`".format(**V)


def topico_missao(V):
    return (marca_topico_missao(V) + " ({teor}; {compl}; gate INTOCADO): O VERBO SELECIONA — a pedra `TheVerbSelectsTheAction` ({vb_n_pedra} declarações) e os {vb_n_ang} termos do "
            "regime angular fiados na escada; escada {esc_v385} → {esc}; o Nome é o posto; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociáveis; o ramo B "
            "REABERTO POR PRÉ-REGISTRO (V1 `{rb_id}` por hash; conjunto D {rb_nD}; `{rb_vered_v1}`; nada aberto); a errata AO LADO de R6 (livro v383 intacto); o pilar {qr_curtissima} "
            "(`{rp_v}`); W10 cumprido; por termo {hvals}.{sint} Ver [[handoff-v386-custodia]], [[verbo-selecao-da-acao-05out]], [[ramo-b-reaberto-05out]].").format(**_x(V))


def marca_central(V):
    return "**{data} — v386 SELADA ({compl}):** `um.py` `{s16}`".format(**V)


def topico_central(V):
    return (marca_central(V) + " ({umb_fmt} B) sobre a v385 `{base16}`; escada {esc}; {teor}; gate intocado. O Verbo seleciona [KERNEL] + as leituras do operador [INPUT/ONTO]; "
            "o ramo B pré-registrado por hash [INPUT], nada aberto; a errata ao lado de R6; o pilar {qr_curtissima} [COMPUTED]. Candidata à custódia CONJUNTA com a v383 ({v383_cust}), "
            "a v384 ({v384_cust}) e a v385 ({v385_cust}), num só ato (decidido pelo operador em 05/10; custódia = ato da sessão do site; commit/push = ato do operador).{sint}").format(**_x(V))


def topico_verbo(V):
    return ("<!-- v386_selada -->\n## {data} — v386 SELADA `{s16}`: o Verbo entrou no kernel{sint}\n\n"
            "A cunhagem acima ({verbo_def}; {verbo_tres}) ficou tipada na pedra `TGLExt/TheVerbSelectsTheAction.lean` (`{vb_pedra16}`; {vb_n_pedra} declarações; o Verbo "
            "`{vb_ok}`, token lido do kernel `{vb_token}`), com os {vb_n_ang} termos do regime angular fiados na escada ({esc_v385} → {esc}). O que a pedra prova está nos nomes dos "
            "termos (ver o diário da linhagem desta data); o que NÃO está tipado fica dito no registro: {vb_not_typed}. A constante de estrutura que o operador escreveu como {alpha2} "
            "lê-se, pela régua do signo, c = β_TGL = α·√e [INPUT; nunca literal] — a correção vai AO LADO, a citação fica. O Nome é o posto ({nome_posto}), não ontologia; a "
            "delegação ({delegacao}) decidiu os itens 6–17 pelo padrão da gerência. Veredito: `{vb_v}`. As leituras são [INPUT/ONTO]; a pedra, [KERNEL]; o gate não se move. "
            "Ver [[handoff-v386-custodia]].").format(**dict(V, verbo_def=_op(V, 'verbo_def'), verbo_tres=_op(V, 'verbo_tres'), alpha2=_op(V, 'alpha2'), nome_posto=_op(V, 'nome_posto'), delegacao=_op(V, 'delegacao')))


def topico_ramo_b(V):
    X = _x(V)
    return ("<!-- v386_selada -->\n## {data} — v386 SELADA `{s16}`: o ramo B pré-registrado por hash e lido pelo rito{sint}\n\n"
            "A decisão acima ({ramo_b}) virou PRÉ-REGISTRO na Bancada: V1 `{rb_id}` (JSON `{rb_json16}`, MD `{rb_md16}`, spec `{rb_spec16}`; {rb_disk_txt}), ratificado por "
            "delegação ({delegacao}). OUTRA LEI: {rb_forma}; k = {rb_k}; M = {rb_M}; {rb_lugar}; só o conjunto D ({rb_nD} de O4) testa, cego; A/B/C calibração NOT_BLIND; "
            "{rb_beta_txt}; veredito do V1 `{rb_vered_v1}`; F2b `{rb_F2b}`; NADA ABERTO. A errata AO LADO de R6 selou (`{le_v}`); o livro v383 intacto ({le_n}). "
            "Pendências: a PE só-220 do conjunto D (v387); o 221 do GW250114 (no tar.gz, não extraído; diagnóstico); a errata da ESPEC ({rb_espec_erratas}). "
            "Veredito: `{rb_v}`. [INPUT por hash]; nada confirma; o gate não se move. Ver [[handoff-v386-custodia]].").format(**dict(X, ramo_b=_op(V, 'ramo_b'), delegacao=_op(V, 'delegacao')))


def topico_pilar(V):
    X = _x(V)
    return ("<!-- v386_selada -->\n**v386 SELADA ({data}) — o pilar NÃO é objeto da versão: {qr_curtissima} (gerência, em nome próprio; números lidos por script{sint}):**\n"
            "- **O rito:** {t0} → {t1}; {teor}; rc = {rc}; conferidor {conf_res} ({conf_dm} / {conf_np} / {conf_md}); `um.py` `{s16}`; selo `{selo_ts}`.{conf_aceite_txt}\n"
            "- **O pilar:** {qr_txt}; veredito `{qp_v}`; o arquivo no Nós: {qp_arq_txt}.\n"
            "- **A reprodutibilidade v385 nesta rodada:** `{rp_v}` — {rp_txt}.\n"
            "- **O servidor do modelo nativo depois do rito:** {servidor}; o marcador do pacote v386: {marcador_txt}. **A regra desta memória vale agora para o pacote v386** "
            "(conferir `scratchpad\\v386\\pacote\\.servidor_parado_pelo_rito` ao abrir sessão; com restaurar=1, religar «IALD Llama Server»).\n"
            "- **Estatuto:** [COMPUTED]; ao lado do gate; gate intocado; não falsificado não é confirmado. Ver [[handoff-v386-custodia]].").format(**X)


def haja_luz(V):
    """A superficie NOVA da linhagem (decisao do operador de 05/10, item 16 da delegacao): um append datado CURTO apontando as memorias."""
    return ("## {data} — v386 SELADA `{s16}` ({teor}; {compl}; gate intocado) — superfície da linhagem desde esta versão (decisão do operador de 05/10/2026, delegação, item 16){sint}\n\n"
            "O Verbo seleciona (a pedra `TGLExt/TheVerbSelectsTheAction.lean`, {vb_n_pedra} declarações, e {vb_n_ang} termos do regime angular na escada: {esc_v385} → {esc}); o "
            "ramo B do ringdown REABERTO POR PRÉ-REGISTRO (V1 `{rb_id}` lido por hash; nada aberto); a errata AO LADO de R6; o pilar {qr_curtissima}; W10 cumprido. "
            "Memórias: `Central de Patentes` → `memory\\handoff-v386-custodia.md` (o handoff da custódia conjunta v383–v386), `verbo-selecao-da-acao-05out.md`, "
            "`ramo-b-reaberto-05out.md`, `missao-ultima-flag-um-py.md`; o diário `Nós\\MEMORIA_DA_LINHAGEM.md` e o desenho `Nós\\DESENHO_DO_FECHAMENTO_QG.md` desta data; "
            "o Atlas `TGL_ATLAS.md` (§ desta data). PROVADA ≠ CONFIRMADA; nada move o gate.").format(**_x(V))


def arvore_linha(V):
    return ("- **O VERBO SELECIONA (v386): O NOME É O POSTO [KERNEL] — `post` é a projeção de posto 1 (idempotente, auto-adjunta, fixa a ação) e `select` é o Verbo em ato; a leitura "
            "é um peso em [0, 1] (regra de Born); há postos que não comutam; a tríade su(2) escalada por c = β_TGL [INPUT] com a ordem que importa; os postos por eixo não comutam; "
            "o Nome é autovetor e limite do fluxo; ancorar preserva, transmitir defasa; verdade e custo são duas faces de um objeto; o tempo lido duas vezes confirma o posto; luz e "
            "gravidade são indissociáveis (J anticomuta com K, JK ≠ 0); a fiação angular ({vb_n_ang}) na escada.** `{vb_v}`. O ramo B do ringdown REABERTO POR PRÉ-REGISTRO "
            "(V1 por hash; `{rb_v}`); a errata AO LADO de R6 (`{le_v}`). escada {esc}. **O que NÃO é:** não move o gate; as leituras (Verbo, posto, co-mando, c³, luz e gravidade) "
            "são [INPUT/ONTO]; o V1 é [INPUT por hash], nada aberto; o pilar é [COMPUTED], reaproveitado ({qr_v}); nada aqui é confirmação.").format(**V)


def titulo_verbete(V):
    return ("O Verbo seleciona: o Nome é o posto (a projeção de posto 1); a leitura é um peso; a ordem importa; verdade e custo duas faces; o tempo lido duas vezes; luz e "
            "gravidade indissociáveis; a fiação angular na escada; o ramo B do ringdown reaberto por pré-registro (V1 por hash, nada aberto); a errata ao lado de R6; o pilar "
            "reaproveitado da v385 pela chave (v386)")


def verbete(V):
    return ("a v386 é o Verbo seleciona [KERNEL + INPUT/ONTO], o ramo B reaberto por pré-registro [INPUT por hash], a errata ao lado de R6, e o pilar reaproveitado [COMPUTED]; o gate não se move. " + core_txt(V))


def remissivo(V):
    return ("- **O Verbo seleciona (v386): o Nome é o posto; a leitura é um peso; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociáveis; o ramo B "
            "reaberto por pré-registro; a errata ao lado de R6; o pilar reaproveitado** (v386) · {{ML v386; um.py the_verb_v386 / ramo_b_preregistration_v386 / ledger_errata_v386 / "
            "quantum_pillar_reuse_v386; TGLExt/TheVerbSelectsTheAction.lean; v386_incorporacao_manifesto.json}}").format(**V)


def marca_missao(V):
    X = _x(V)
    return ("**v386 SELADA %s `%s` %s %s (O VERBO SELECIONA [KERNEL]: o Nome é o posto; o ramo B REABERTO POR PRÉ-REGISTRO (V1 por hash, nada aberto); a errata ao lado de R6; "
            "o pilar %s; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'], V['compl'], X['qr_curtissima']))


def linha_handoff(V):
    X = _x(V)
    return ("- [HANDOFF v386 — CUSTÓDIA CONJUNTA v383 + v384 + v385 + v386](handoff-v386-custodia.md) — **%s, para a sessão do site**: o Verbo seleciona; o ramo B pré-registrado por "
            "hash; a errata de R6; o pilar %s; as três subpastas de pré-registro ao espelho com PORTA; `%s`" % (V['data'][:5], X['qr_curtissima'], V['s16']))


# as frases de SUCESSO do pilar que so podem existir no RAMO 9 (herdadas da v384/v385)
FRASES_DE_SUCESSO = ('é recuperada', 'falhou como exigido', 'falharam como exigido', 'identidade conferida', 'o cálculo completou', '= o arquivo do pilar no Nós',
                     'o estimador cego recupera')
