# -*- coding: utf-8 -*-
# Os TEXTOS da v384 selada. Cada numero, hash, veredito e verbatim entra por {chave} de V (leitura_v384.ler), nunca digitado aqui.
# O PILAR QUANTICO NA GPU [COMPUTED]: o sistema aberto GKLS da teoria (H_LD + cinco saltos de Lindblad) calculado em paralelo com o kernel e os ritos,
# sob o pre-registro V1 ratificado pelo operador e congelado ANTES do calculo; registro proprio AO LADO do gate; o gate NAO se move; o kernel e' o da v383.
# Os textos nao afirmam mais do que os numeros: o que a GPU deu entra com a classe lida da arvore congelada (ramo 9 com os negativos honestos, ou
# computacao nao concluida, com a causa tirada do token); toda frase de SUCESSO (o T3 recupera, o N1 falhou como exigido, a identidade conferida, o arquivo
# do pilar = o resultado) so existe no RAMO 9 (e a identidade, so com IDENTITIES_HOLD no veredito); nao falsificado nunca e' confirmado; nada de «QG confirmada».

# a parafrase da gerencia das ordens do V1, por NUMERO da ordem; so usada se as ordens do V1 forem exatamente estas (senao: «o verbatim esta no V1»)
_PARAF = {1: 'a prova quântica, com matrizes, na GPU enquanto o um.py roda',
          2: 'o mundo quântico da TGL inteiro na GPU — os saltos, o dephasing, o sistema aberto — em paralelo com o kernel e os ritos cosmológicos',
          3: 'a introdução e a nota do artigo sobre o que a GPU calcula e como',
          4: 'os cinco saltos de Lindblad, o servidor parado durante o rito e o tempo que o teste robusto pedir',
          5: 'o rito robusto com a ferramenta de reaproveitamento, e a versão final sempre completa'}


def _ramo9(V):
    return V['qp_classe'] == 'RAMO_9'


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
    X['t1_frase'] = (('o estimador cego recupera a lei injetada sem ruído (%s)' % V['t1_rec']) if (_ramo9(V) and 'T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND' in V['qp_v'])
                     else ('o T1 não recupera a lei injetada sem ruído em todas as dimensões (%s)' % V['t1_rec']) if _ramo9(V)
                     else 'o T1 não tem resultado válido nesta rodada')
    X['v383_cust'] = ('custodiada (commit «%s» lido do git da Central)' % V['v383_commit']) if V.get('v383_commit') else 'ainda não custodiada pelo que o git da Central registra (nenhum commit «custodia(v383)»)'
    X['qp_beta_hex_txt'] = V.get('qp_beta_hex') or 'n/d'
    X['extra_txt'] = (' **Ditos pela gerência, ao lado:** %s.' % V['qp_neg_extra']) if V.get('qp_neg_extra') else ''
    X['resumo_txt'] = (' O resumo dos números: %s.' % V['resumo_fonte']) if V.get('resumo_ausente') and _ramo9(V) else ''
    return X


def _ordens(V):
    ns = V.get('pr_ordens_ns') or []
    par = (('; '.join('(%d) %s' % (n, _PARAF[n]) for n in ns) + ' — paráfrase da gerência; o verbatim está no V1')
           if ns and sorted(ns) == sorted(_PARAF) else 'o verbatim está no V1')
    return ("**A ordem e a ratificação (verbatim no pré-registro):** as {pr_n_ordens} ordens do operador ({pr_n_trechos} trechos verbatim) de {pr_ordens_datas} ("
            + par + ") e a RATIFICAÇÃO ({pr_quando_txt}): «{pr_verbatim}» — escolha `{pr_escolha}` [INPUT]. ").format(**V)


def _entrou(V):
    return ("**O QUE ENTROU** (pacote v384 sobre a v383 `{base16}`; {n_patches} patches — {patches}; kernel: {kernel_decl}; {n_afer} passadas de aferição antes do rito, com as disposições; "
            "a fumaça {fumaca_txt}; o ensaio a seco PT/EN: `{ensaio_seco}`): o `um.py` lança, logo depois da inscrição do Um, um trabalhador de GPU embutido nele byte a byte (`pilar_quantico_worker.py`, `{pr_worker16}`) "
            "que calcula o sistema quântico aberto GKLS da teoria — o hamiltoniano luminodinâmico H_LD e os cinco saltos de Lindblad, entre eles a anti-coerência L_anti = √β_TGL·√K (a lei-raiz), "
            "com β do core em hexadecimal, nunca literal —; antes do artigo, espera, confere o sha256, REDERIVA o veredito pela mesma árvore congelada e registra no core (`quantum_pillar_v384`), "
            "no selo (registro próprio AO LADO do gate + a leitura `the_quantum_pillar_reading_v384`) e no artigo (a introdução e a nota da GPU) — e, se o pilar não concluir, no terceiro balde "
            "da custódia de sentido (`computacao_nao_concluida`). **O pré-registro** `{pr_id}` (pasta permanente da Bancada; JSON `{pr_json16}`, MD `{pr_md16}`, especificação `{pr_spec16}`; {pr_ev} evidências "
            "conferidas por sha256; somente leitura: {pr_so_leitura_txt}; conferência independente do congelamento: {pr_conf}; orçamento {pr_orc_min} min, {pr_orc_margem} com a margem), "
            "congelado ANTES de qualquer cálculo dos testes. ").format(**V)


def _deu(V):
    X = _x(V)
    if _ramo9(V):
        return ("**O QUE A GPU DEU** ({qp_gpu}; {qp_min} min do começo ao fim do trabalhador; fases: {fases}) — {qp_classe_txt}: "
                "(T2) a forma na escala: {t2_points} pontos da grade em {t2_configs} configurações (d, n_c); atrator único em {t2_unique} (ambíguos {t2_amb}, degenerados {t2_deg}, erros {t2_err}); "
                "NAME_IN_CORE (ao menos um ponto de atrator único com peso ≥ ½ no núcleo Π) em {t2_name} de {t2_configs}; FOLDS_WINDOW (as dobras na janela pré-registrada: quase-pureza do atrator) "
                "em {t2_folds} de {t2_configs}; menor gap relativo {t2_gapmin}; identidades conferidas {t2_ids}; |sin²θ_M − β| = {t2_sin2}. "
                "(T1) o instrumento, às cegas: {t1_inj} injeções ({t1_por_d}); {t1_frase}; com ruído, a fração com {t1_ruido_crit} — a estatística que o V1 fixou para RELATAR, "
                "sem limiar de decisão (curva de resolução): {t1_ruido}. "
                "(T3) os controles que têm de falhar: {t3_ctl} falharam como exigido; a identidade unital (I/d estacionário) em {t3_n2}; o N3: {t3_n3}. "
                "(T4) o estresse: {t4_n} instâncias, atrator único em {t4_u}, {t4_viol} violações de identidade, as seis identidades conferidas em {t4_all} ({t4_rot} com rotação de Haar). "
                "(D128) {d128_txt}. (CPU) a referência independente (numpy/LAPACK, processo à parte) leu {cpu_read} pontos, comparou {cpu_cmp} ({cpu_near} perto do limiar, não comparados), "
                "{cpu_dis} discordâncias, maior diferença {cpu_maxdiff}. O motor E1–E8: {eng}.{resumo_txt} "
                "**O veredito do pilar**, rederivado pela mesma árvore ({qp_rederiv}): `{qp_v}`. **Negativos honestos desta rodada:** {qp_negativos}. "
                "**A cadeia de custódia:** resultado `{qp_res16}` (= o arquivo do pilar no Nós e o seu hash no selo `{qp_selo16}`), details `{qp_det16}`, cpuref `{qp_cpu16}`, pasta `{qp_run_dir}`, "
                "marca da rodada `{qp_run_id8}`, chave `{qp_key_txt}`; {qp_cache}.{conf_aceite_txt} ").format(**X)
    return ("**O QUE A GPU DEU** ({qp_gpu}): {qp_classe_txt} — `{qp_v}`. O pilar vai ao TERCEIRO BALDE do selo (computação não concluída: {balde}): não é dívida formal da teoria nem "
            "recusa de dado; é resultado, dito como tal. Lançamento: {qp_lanc_txt}. Custódia: {qp_custodia_txt}; {qp_cache}.{extra_txt}{conf_aceite_txt} ").format(**X)


def _estatuto(V):
    return ("**Estatuto:** o pilar é [COMPUTED] — cálculo do sistema da teoria, não medição da natureza; registro próprio AO LADO do gate, e o gate `{qg}` ({n18}/18) está INALTERADO; o kernel é o "
            "MESMO da v383 (escada {esc}; nenhuma pedra nova; {n_ver_iguais} de {n_ver} vereditos da v383 inalterados; {n_av_iguais} de {n_av} módulos com o mesmo all_verified do estado selado "
            "da v383; por termo {hvals}); as identidades (o zero do espectro, CP, traço, Spohn, "
            "o não-retorno, a parte unital) só falham se o motor errar, e a hierarquia das dobras é matemática, não teste; o T1 testa o instrumento (em aritmética exata a separação da lei é "
            "estrutural), não a natureza; «o Nome como matriz» (Π; CCI = Tr Πρ_ss) é leitura [ONTO]; as ordens e a ratificação são do operador [INPUT]. Não falsificado não é confirmado; "
            "nada aqui é confirmação. Leitura do selo: `{qp_reading}`.").format(**V)


def core_txt(V):
    return _ordens(V) + _entrou(V) + _deu(V) + _estatuto(V)


def rodada_txt(V):
    X = _x(V)
    t = ("Rodada {compl} ({ckpt}) {t0} → {t1} ({tsrc}): **{teor}**; rc = {rc} ({rcsrc}); `{selftest}`; stdout limpo (sem Traceback, sem «[selo] AVISO», sem SEAL_WITHHELD); o terceiro "
         "balde: {balde}. Conferidor `conferir_rito_v384.py` (cópia byte a byte do pacote; a MESMA guarda do rito): **{conf_res}** — {conf_dm} «deve mudar», {conf_np} «não pode mudar» "
         "(JSON `{conf16}`). O servidor do modelo nativo depois do rito (informação, do log do lançador): {servidor}. `um.py` sha16 `{s16}` ({umb_fmt} B). Selo `{selo_ts}`.").format(**X)
    if V.get('tentativas'):
        t += " Tentativas anteriores preservadas ao lado: %s." % ", ".join("`%s`" % x for x in V['tentativas'])
    return t


def linhagem(V):
    X = _x(V)
    return ("## {data} — **v384 SELADA ({compl})** `{s16}` — O PILAR QUÂNTICO NA GPU ([COMPUTED]: o sistema aberto H_LD + os cinco saltos de Lindblad, em paralelo com o kernel e os ritos; "
            "o pré-registro `{pr_id}` ratificado pelo operador, `{pr_escolha}`, por hash; o pilar: {qp_classe_curta}); kernel = o da v383; gate intocado{sint}\n\n".format(**X)
            + core_txt(V) + "\n\n" + rodada_txt(V))


def desenho(V):
    X = _x(V)
    deu = ("- **O que a GPU deu:** `{qp_v}` — {qp_classe_txt}; negativos honestos: {qp_negativos}.\n" if _ramo9(V)
           else "- **O que a GPU deu:** `{qp_v}` — {qp_classe_txt}" + ("; ditos pela gerência, ao lado: {qp_neg_extra}" if V.get('qp_neg_extra') else "") + ".\n")
    return ("---\n\n## ADENDO — {data} · v384 SELADA ({compl}) `{s16}` — O pilar quântico na GPU, ao lado do gate{sint}\n\n"
            "- **O que mudou no caminho crítico:** nada no caminho formal — o kernel é o MESMO da v383 (escada {esc}) e o gate `{qg}` ({n18}/18) não se move; por termo (inalterado): "
            "remaining = {remaining}; gpf_H2 / gpf_H3 / gpi_H3 = {hvals}. Ao lado do gate entra um registro próprio, [COMPUTED]: o sistema quântico aberto da teoria (H_LD + cinco saltos de "
            "Lindblad), calculado na GPU na mesma rodada, sob o pré-registro `{pr_id}` (especificação `{pr_spec16}`), ratificado pelo operador ({pr_quando_txt}; `{pr_escolha}`).\n"
            + deu +
            "- **O que o pilar é e não é:** cálculo da face matricial do mesmo sistema (a leitura é [ONTO]), não medição; não decide H2 nem H3; nenhum número dele entra no gate; "
            "não falsificado não é confirmado.\n"
            "- **O que segue do operador:** a custódia (a v383 — {v383_cust} — agora ou junto com a v384; os V1–V1.3 do pré-registro dos dois lados; o que espelhar do pré-registro do pilar e "
            "das suas evidências) — ver o HANDOFF v384.\n"
            "- `{s16}`; {teor}.").format(**X)


def atlas(V):
    return ("---\n\n## {data} — v384 SELADA ({compl}): O PILAR QUÂNTICO NA GPU ([COMPUTED]; O SISTEMA ABERTO H_LD + CINCO SALTOS DE LINDBLAD EM PARALELO COM O KERNEL E OS RITOS; "
            "O PRÉ-REGISTRO V1 RATIFICADO PELO OPERADOR, {pr_escolha}, POR HASH; REGISTRO PRÓPRIO AO LADO DO GATE; KERNEL = O DA v383) (append datado){sint}\n\n"
            "`um.py` `{s16}` · {teor} · {compl} · ".format(**V) + core_txt(V) + " " + rodada_txt(V) + " Ver o verbete gerado por `atlas_indice.py v384`.")


def marca_topico_missao(V):
    """O marcador de idempotencia do bloco da missao: um prefixo ESTAVEL (so a data, a versao e o sha16)."""
    return "## {data} — v384 SELADA `{s16}`".format(**V)


def topico_missao(V):
    return (marca_topico_missao(V) + " ({teor}; {compl}; gate INTOCADO): o pilar quântico na GPU [COMPUTED] — o sistema aberto H_LD + cinco saltos de Lindblad em paralelo com o kernel "
            "e os ritos, sob o pré-registro `{pr_id}` ratificado (`{pr_escolha}`); kernel = o da v383 (nenhuma pedra nova); o pilar: `{qp_v}` ({qp_classe_curta}); {neg_rotulo}: {qp_negativos}; "
            "por termo {hvals}.{sint} Ver [[v384-pilar-quantico-gpu-02out]], [[handoff-v384-custodia]], [[handoff-v383-custodia]].").format(**_x(V))


def marca_central(V):
    """O marcador de idempotencia do bloco do central-de-patentes-estado: um prefixo ESTAVEL (nunca o bloco inteiro, que traz a custodia lida do git ao vivo)."""
    return "**{data} — v384 SELADA ({compl}):** `um.py` `{s16}`".format(**V)


def topico_central(V):
    return (marca_central(V) + " ({umb_fmt} B) sobre a v383 `{base16}`; kernel = o da v383 (escada {esc}); {teor}; gate intocado. O pilar quântico na GPU "
            "[COMPUTED], ao lado do gate: {qp_classe_curta}; pré-registro `{pr_id}` por hash (JSON `{pr_json16}`). Candidata à custódia — com a v383 ({v383_cust}) agora ou depois: "
            "decisão do operador (custódia = ato separado; commit/push é ato do operador).{sint}").format(**_x(V))


def topico_regra(V):
    X = _x(V)
    t3 = ("No T1, {t1_frase}; no T3, a lei linear injetada é recuperada e a lei-raiz rejeitada ({t3_n3})" if _ramo9(V)
          else "O T1 e o T3 não têm resultado válido nesta rodada (`{qp_v}`)")
    ident = ("sin²θ_M = β é identidade conferida (|sin²θ_M − β| = {t2_sin2}), não teste" if (_ramo9(V) and '__IDENTITIES_HOLD__' in V['qp_v'])
             else "sin²θ_M = β é identidade, não teste — nesta rodada ela não foi conferida como válida")
    return ("## {data} — v384 SELADA `{s16}`: o pilar quântico USA β, não o deriva{sint}\n\n"
            "O trabalhador da GPU recebe β do core em hexadecimal (`{qp_beta_hex_txt}`; bit a bit o do core: {qp_beta_txt}), pelo mesmo motor do `um.py` (a forma de Lagrange; o CODATA só "
            "valida) — nunca literal. O que ele testa é a FORMA da lei, não o valor: a anti-coerência L_anti = √β·√K (a lei-raiz). " + t3 + "; " + ident + ". "
            "Nada disso deriva o VALOR de β sem α, e nada disso move a regra. "
            "Pilar: `{qp_v}` [COMPUTED]; não falsificado não é confirmado.").format(**X)


def topico_regimes(V):
    n1 = (" — e o N1 falhou como exigido em {t3_n1}" if _ramo9(V) else " — o N1 não tem resultado válido nesta rodada")
    return ("## {data} — v384 SELADA `{s16}`: o pilar quântico não acrescenta kernel nem leitura de regime{sint}\n\n"
            "Dois fatos dele tocam a régua dos dois regimes, ditos sem encadear homônimo: (i) o controle N1 do T3 (o dephasing sozinho) apoia-se no que o kernel já prova — o dephasing "
            "preserva toda a diagonal (`ModularDephasingBridge.spectral_preserves_every_diagonal`) e, na face de dois níveis, os pontos fixos do semigrupo são exatamente os que a esperança "
            "diagonal fixa (`IALDRhoStar.tgl_fix_iff`) —; a NÃO unicidade do atrator em dimensão d sai de uma contagem elementar (a dimensão do núcleo, d + n_c(n_c − 1), no pré-registro), "
            "não de teorema do kernel" + n1 + "; (ii) o atrator ρ_ss é um LIMITE (t → ∞ do semigrupo do sistema aberto) e o CCI = Tr Πρ_ss é uma LEITURA desse limite pelo projetor do núcleo. "
            "A gerência NÃO identifica aqui esse limite com a direção hiperbólica de SL(2,ℝ) nem a leitura com o regime compacto: seria encadear homônimo; fica [OPEN]. Pilar: `{qp_v}`.").format(**V)


def topico_suspensao(V):
    return ("## {data} — v384 SELADA `{s16}`: a v382 continua só no Nós; a v384 parte da v383{sint}\n\n"
            "A v384 foi instalada sobre a v383 `{base16}` (não sobre a v382). A sessão do site não custodia a v382 (decisão do operador já registrada nesta memória). A v383: {v383_cust}; se ela vai agora ou junto com a "
            "v384 é decisão do operador [a decidir]. Ver [[handoff-v384-custodia]].").format(**_x(V))


def topico_pilar(V):
    X = _x(V)
    if _ramo9(V):
        deu = ("- **O pilar:** `{qp_v}` — {qp_classe_txt}. (T2) atrator único em {t2_unique} de {t2_points} pontos; NAME_IN_CORE {t2_name}/{t2_configs}; FOLDS_WINDOW {t2_folds}/{t2_configs}. "
               "(T1) {t1_inj} injeções; {t1_frase}; com ruído ({t1_ruido_crit}), relatado: {t1_ruido}. (T3) {t3_ctl} controles falharam como exigido. (T4) {t4_n} instâncias; {t4_viol} violações. "
               "(D128) {d128_txt}. (CPU) {cpu_cmp} comparados, {cpu_dis} discordâncias. Tempo do trabalhador: {qp_min} min (orçamento pré-registrado {pr_orc_min}; {pr_orc_margem} com a margem).{resumo_txt}\n"
               "- **Negativos honestos:** {qp_negativos}. **Cache:** {qp_cache}.\n")
    else:
        deu = ("- **O pilar:** `{qp_v}` — {qp_classe_txt}. Lançamento: {qp_lanc_txt}. Custódia: {qp_custodia_txt}. Orçamento pré-registrado {pr_orc_min} min ({pr_orc_margem} com a margem).\n"
               "- **Computação não concluída** (o terceiro balde do selo: {balde}).{extra_txt} **Cache:** {qp_cache}.\n")
    return ("<!-- v384_selada -->\n**v384 SELADA ({data}) — gerência, em nome próprio; números lidos por script{sint}:**\n"
            "- **O rito:** {t0} → {t1}; {teor}; rc = {rc}; conferidor {conf_res} ({conf_dm} / {conf_np}); `um.py` `{s16}`; selo `{selo_ts}`.{conf_aceite_txt}\n"
            + deu +
            "- **O servidor do modelo nativo depois do rito:** {servidor}; o marcador do pacote: {marcador_txt}.\n"
            "- **Estatuto:** [COMPUTED]; ao lado do gate; gate intocado; não falsificado não é confirmado. Ver [[handoff-v384-custodia]].").format(**X)


def arvore_linha(V):
    return ("- **O PILAR QUÂNTICO (v384): O SISTEMA ABERTO DA TEORIA NA GPU, AO LADO DO GATE [COMPUTED] — H_LD + cinco saltos de Lindblad (L_anti = √β·√K, a lei-raiz), calculados em paralelo "
            "com o kernel e os ritos sob o pré-registro `{pr_id}` (especificação `{pr_spec16}`, ratificado pelo operador: `{pr_escolha}`); quatro testes congelados (T1 o instrumento às cegas; "
            "T2 a forma na escala; T3 os controles que têm de falhar; T4 o estresse) + D128 + a referência na CPU.** `{qp_v}`. kernel = o da v383 (escada {esc}). **O que NÃO é:** não é "
            "medição da natureza; não é teorema de kernel; não move o gate; a hierarquia das dobras é matemática; o T1 testa o instrumento; {neg_rotulo}: {qp_negativos}; nada aqui é "
            "confirmação.").format(**_x(V))


def verbete(V):
    # o verbete: uma frase de abertura propria (sem repetir as ordens, que o core_txt ja diz) + o core_txt
    return ("a v384 é o pilar quântico na GPU [COMPUTED], registrado ao lado do gate, sobre o kernel da v383. " + core_txt(V))


def remissivo(V):
    return ("- **O pilar quântico (v384): o sistema aberto H_LD + cinco saltos de Lindblad na GPU, em paralelo com o kernel e os ritos [COMPUTED]; o pré-registro `{pr_id}` ratificado "
            "(`{pr_escolha}`) por hash; registro próprio ao lado do gate; o terceiro balde da custódia de sentido; kernel = o da v383 (escada {esc})** (v384) · "
            "{{ML v384; um.py quantum_pillar_start_v384 / quantum_pillar_finish_v384; v384_incorporacao_manifesto.json}}").format(**V)


def marca_missao(V):
    """O prefixo da linha da missao no MEMORY.md (a idempotencia le '**v384 SELADA dd/mm `s16`')."""
    X = _x(V)
    return ("**v384 SELADA %s `%s` %s %s (O PILAR QUÂNTICO na GPU [COMPUTED], ao lado do gate: %s; o pré-registro V1 ratificado (%s) por hash; kernel = o da v383; gate intocado)** · "
            % (V['data'][:5], V['s16'], V['teor'], V['compl'], X['qp_classe_curta'], V['pr_escolha']))


def linha_handoff(V):
    X = _x(V)
    return ("- [HANDOFF v384 — O PILAR QUÂNTICO na GPU; custódia](handoff-v384-custodia.md) — **%s, para a sessão do site**: o pilar [COMPUTED] ao lado do gate (%s); o pré-registro V1 "
            "e as evidências da Bancada; a pasta da rodada; decisões pendentes do operador; `%s`" % (V['data'][:5], X['qp_classe_curta'], V['s16']))


# as frases de SUCESSO que so podem existir no RAMO 9 (testar_formatos_v384.py e ensaio_guardas_v384.py as procuram fora dele)
FRASES_DE_SUCESSO = ('é recuperada', 'falhou como exigido', 'falharam como exigido', 'identidade conferida', 'o cálculo completou', '= o arquivo do pilar no Nós',
                     'o estimador cego recupera')
