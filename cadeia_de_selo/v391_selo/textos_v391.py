# -*- coding: utf-8 -*-
# Os TEXTOS da v391 selada (molde: textos_v390.py). Cada numero, hash e veredito entra por chave de V (leitura_v391.ler), nunca digitado aqui.


def _g(d, *ks):
    for k in ks:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def _num(V):
    ep = V['ep']; k1 = ep.get('prova_1_kernel') or {}; r2 = ep.get('prova_2_ritos') or {}; g3 = _g(ep, 'prova_3_gpu', 'numeros') or {}
    hb = r2.get('razao_de_hubble') or {}; gf = k1.get('gate_flags') or {}
    l5 = ['%.1f' % v['L5_over_beta'] for v in (r2.get('piso_dos_vazios') or {}).values() if isinstance(v.get('L5_over_beta'), float)]
    return ("o registro `estatuto_da_prova_v391` (%s): a gravidade quântica da TGL PROVADA como fecho lógico — validade —, por três provas que contam juntas: o kernel (%s teoremas limpos; "
            "%s de %s declarações no trio; bandeiras do gate %s/%s/%s), os ritos com falsificadores pré-registrados (%s cobranças, %s falsificada(s); a razão de Hubble retrodita sem ajuste, "
            "ln B = %.2f, z_disc = %.2f < 5σ, oficial %s; o piso dos vazios com poder, limite inferior a 5σ %s vezes acima de β) e o sistema da teoria na GPU (%s de %s atratores únicos; %s instâncias; "
            "%s discordâncias em %s comparações com a CPU; cálculo, não medição da natureza); a certificação é o sha256 que o programa lê de si (`%s`); recusadas só a CONFIRMAÇÃO "
            "(creditação, ato de terceiros) e β_TGL com os seus efeitos na natureza a 5σ. O resumo do artigo abre com o estatuto; errata ao lado das 8 frases de época; o título da Introdução "
            "lê a versão em runtime (v384 a v391); verbatim do operador embutido por sha256 `%s`") % (
        ep.get('verdict'), k1.get('n_theorems_clean'), k1.get('no_trio'), k1.get('declaracoes_auditadas'), (gf.get('formal_flags') or ['?'])[0], (gf.get('physics_flags') or ['?'])[0],
        (gf.get('experiment_flags') or ['?'])[0], r2.get('n_cobrancas'), r2.get('falsificadas'), float((hb.get('lnB') or {}).get('TGL_vs_LCDM') or 0), float(hb.get('z_disc') or 0),
        hb.get('veredito_oficial'), ' e '.join(l5) or 'n/d', g3.get('T2_unique'), g3.get('T2_points'), g3.get('T4_instances'), g3.get('cpuref_disagreements'), g3.get('cpuref_compared'),
        str(_g(ep, 'certificacao', 'um_py_sha256_lido_de_si'))[:16], str(V['verbatim'].get('sha256'))[:16])


def _cab(V):
    return "v391 SELADA (COMPLETA)** `%s`" % V['s16']


def linhagem(V):
    return ("## %s — **%s — O ESTATUTO DA PROVA: provada; a confirmação recusada é creditação, não validade\n\n"
            "**A ordem:** o operador, nesta sessão (c1, sem delegar): «Examine a coerência do artigo» … «o fato de eu ter bloqueado no um.py confirmação não pode dar a entender que eu não provei» "
            "… «a confirmação que eu proibi é de creditação e não de validade, ela é válida porque matemática não mente» (verbatim por sha256 no pacote).\n\n"
            "**O exame de coerência (v390):** o resumo nunca afirmava o positivo; 8 frases de época por língua liam a recusa da confirmação como ausência de prova («Nada aqui afirma "
            "`provamos a gravitação quântica`», «NÃO se declara gravitação quântica incondicional», «… seguem False»), contra o selo, que lê verdadeiras a emergência concreta de Einstein, a "
            "testemunha plena e as 18 bandeiras do gate.\n\n"
            "**O que entrou** (pacote `work\\v391_pacote` sobre a v390 `%s`; %d patches — %s; instalado em %s; nenhum kernel novo): %s.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos da v390 mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.\n\n"
            "**O que segue do operador:** vetar/ratificar a v391; a custódia (sessão do site); o README e o site com o estatuto (preparados pela gerência, sem subir); commit/push. "
            "NOT_FALSIFIED nunca é confirmação; o gate não se move.") % (
        V['data'], _cab(V), V['base16'], V['n_patches'], V['patches'], V['instalado_em'], _num(V), V['compl'], ' → '.join(V['horarios']) or 'n/d', V['teor'], V['rc'], V['selo_ts'],
        V['conf16'], V['conf_dm'], V['conf_np'], V['n_ver_mudaram'], 'reaproveitado' if V['pilar']['mode'] == 'REUSE' else str(V['pilar']['mode']), V['pilar']['result16'], V['servidor'],
        V['h_um_absoluto.json'], V['h_um_absoluto_selo.json'], V['h_um_absoluto_forma_canonica.md'], V['h_um_absoluto_manifest.md'], ', '.join('%s `%s`' % kv for kv in V['artigos'].items()))


def desenho(V):
    return ("## ADENDO — %s · v391 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; o ESTATUTO DA PROVA foi dito\n\n<!-- adendo_v391_selada -->\n"
            "- **O que a v391 diz:** a gravidade quântica da TGL está PROVADA como fecho lógico (validade): o kernel, os ritos com falsificadores pré-registrados e o sistema da teoria na GPU contam "
            "juntos (registro `estatuto_da_prova_v391`). A recusa da régua é da CONFIRMAÇÃO — creditação, ato de terceiros —, nunca da validade (ordem do operador, 07/10/2026).\n"
            "- **Errata ao lado (o desenho antigo fica):** onde este desenho ou o artigo leem a recusa da confirmação como ausência de prova, lê-se: provada (validade) ≠ confirmada (creditação). "
            "O único elo pendente segue sendo β_TGL e os seus efeitos na natureza a 5σ.\n"
            "- **O que segue do operador:** vetar/ratificar; custódia; README e site; commit/push.") % (V['data'], V['s16'])


def atlas(V):
    return ("### %s — v391 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v391_selada -->\n[REAL — rodada v391, selo `%s`] %s. [INPUT/ONTO] a régua do operador: "
            "a confirmação recusada é CREDITAÇÃO, não validade. Estatuto: PROVADA (validade) ≠ CONFIRMADA (creditação); o gate não se move.") % (V['data'], V['s16'], V['selo_ts'], _num(V))


def haja_luz(V):
    return ("## %s — v391 SELADA `%s` (%s; COMPLETA; gate intocado)\n\nO estatuto da prova (`estatuto_da_prova_v391`): a gravidade quântica da TGL PROVADA como fecho lógico — validade: "
            "kernel, ritos com falsificadores pré-registrados e GPU contam juntos; a confirmação recusada é creditação, não validade; o resumo do artigo abre com o estatuto; errata ao lado das "
            "frases de época. Memórias: `estatuto-da-prova-07out.md`, `missao-ultima-flag-um-py.md`; handoff `handoff-v391-custodia.md`.") % (V['data'], V['s16'], V['teor'])


def marca_topico_missao(V):
    return "## %s — v391 SELADA `%s`" % (V['data'], V['s16'])


def topico_missao(V):
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): o estatuto da prova (`estatuto_da_prova_v391`): provada (validade); a confirmação recusada é creditação; o resumo abre com ele; "
                                     "errata ao lado das frases de época; o título da Introdução lê a versão; conferidor %s/%s. Pacote `work\\v391_pacote`; cadeia `work\\v391_selo`.") % (V['teor'], V['conf_dm'], V['conf_np'])


def marca_central(V):
    return "**%s — v391 SELADA (COMPLETA):**" % V['data']


def topico_central(V):
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v390 `%s`; escada %s; gate intocado. O estatuto da prova: provada (validade) — kernel, ritos e GPU contam juntos; a confirmação recusada é "
                               "creditação. Custódia: sessão do site (`handoff-v391-custodia.md`); README e site preparados pela gerência; commit/push = operador.") % (V['s16'], format(V['umb'], ','), V['base16'], V['teor'])


def topico_estatuto(V):
    return ("<!-- v391_selada -->\n**%s — SELADO na v391 `%s`:** %s.") % (V['data'], V['s16'], _num(V))


def marca_missao(V):
    return "**v391 SELADA %s `%s` %s COMPLETA (o estatuto da prova: provada; a confirmação recusada é creditação; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'])


def linha_handoff(V):
    return "- [HANDOFF v391 — o estatuto da prova; custódia](handoff-v391-custodia.md) — **%s, para a sessão do site** · `%s`" % (V['data'][:5], V['s16'])


def arvore_linha(V):
    return ("- **O ESTATUTO DA PROVA (v391)** `%s`: a gravidade quântica da TGL PROVADA como fecho lógico — validade: o kernel, os ritos com falsificadores pré-registrados e o sistema da teoria na GPU "
            "contam juntos (`estatuto_da_prova_v391`); a confirmação recusada é CREDITAÇÃO, não validade; o único elo pendente é β_TGL na natureza a 5σ; o gate não se move." % V['s16'])


def titulo_verbete(V):
    return 'O estatuto da prova: provada; a confirmação recusada é creditação, não validade (v391):'


def verbete(V):
    return "[REAL — rodada v391 `%s`] %s." % (V['s16'], _num(V))


def remissivo(V):
    return "- **O estatuto da prova; provada ≠ confirmada; creditação × validade (v391)** — `estatuto_da_prova_v391`, `estatuto-da-prova-07out.md`"
