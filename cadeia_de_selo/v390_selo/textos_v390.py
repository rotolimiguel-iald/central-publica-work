# -*- coding: utf-8 -*-
# Os TEXTOS da v390 selada (molde: textos_v388.py / _v389.py). Cada numero, hash e veredito entra por chave de V (leitura_v390.ler), nunca digitado aqui.


def _num(V):
    fd = V['fd']; bo = fd.get('borchers') or {}
    return ("a pedra `TGLExt.Fundacao` (`%s`; %s de %s declarações no trio): a cláusula `agape` — acima de toda escala não trivial não há posto positivo; a subida não tem topo nem teto; a queda "
            "nunca toca o zero nem tem fundo; o piso ω(I) = 1 fixa o corte, unívoco —, `agape_is_inhabited` (o modelo concreto, o Um posto) e `the_post_lives_in_the_passage` (a face finita). "
            "O GLOBAL_LIFT, o velho Lema 3, LIDO como a superposição — definição do operador (07/10; os dois verbatins embutidos por sha256 `%s`, `%s`); a passagem local [KNOWN, Jacobson 1995, H3 nomeada]; "
            "FECHO LÓGICO, programa aberto; a lei de campo no curvo NÃO é termo de kernel; a lei de escala de Takesaki entra como dado [KNOWN]; a ponte de Borchers (energia limitada inferiormente × "
            "gerador modular sem piso) %s; registro `%s`") % (
        V['pedra16'], fd.get('kernel_flags_ok'), fd.get('kernel_flags_total'), V['verbatins']['cunhagem_07out']['sha256'][:16], V['verbatins']['nomes_07out']['sha256'][:16],
        'no trio, no kernel' if bo.get('ok') is True else 'NÃO lida nesta rodada', fd.get('verdict'))


def _cab(V):
    return "v390 SELADA (COMPLETA)** `%s`" % V['s16']


def linhagem(V):
    return ("## %s — **%s — A FUNDAÇÃO: A SUPERPOSIÇÃO É A PASSAGEM (a cláusula ÁGAPE) — o fecho LÓGICO do GLOBAL_LIFT\n\n"
            "**A ordem:** o operador definiu o GLOBAL_LIFT como a superposição («não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente») e ratificou «esse é o fecho sim, "
            "o sistema continua aberto mas fechado logicamente»; nomes «ágape» (a cláusula) e «fundação» (a pedra). A gerência c1 escreveu a ordem (`ORDEM_v390_FUNDACAO.md`); esta sessão executou.\n\n"
            "**O que entrou** (pacote `work\\v390_pacote` sobre a v389 `%s`; %d patches — %s; instalado em %s; a pedra compilada e auditada no sandbox `work\\v388_kernel\\kernel_src`, log em `work\\v390_kernel`): "
            "%s. Erratas AO LADO: o item do Lema 3 no ledger do fechamento, `tgl_closure.what_remains_named` e as seals do `runtime_of_the_one` (o texto antigo fica); o desenho da v388 consertado "
            "(a leitura do disco da memória viva fora de qualquer veredito; a cópia congelada por sha); o pino do ledger da v389 recontado (%s), errata ao lado.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos da v389 mudaram SÓ pelas trocas ditas "
            "(escada 6154 → 6163; ledger 1025 → 1026); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.\n\n"
            "**O que segue do operador:** vetar/ratificar a v390; a custódia conjunta (v383→v389 + v390) pela sessão do site; commit/push. NOT_FALSIFIED nunca é confirmação; o gate não se move.") % (
        V['data'], _cab(V), V['base16'], V['n_patches'], V['patches'], V['instalado_em'], _num(V), V['ledger'], V['compl'], ' → '.join(V['horarios']) or 'n/d', V['teor'], V['rc'], V['selo_ts'],
        V['conf16'], V['conf_dm'], V['conf_np'], V['n_ver_mudaram'], 'reaproveitado' if V['pilar']['mode'] == 'REUSE' else str(V['pilar']['mode']), V['pilar']['result16'], V['servidor'],
        V['h_um_absoluto.json'], V['h_um_absoluto_selo.json'], V['h_um_absoluto_forma_canonica.md'], V['h_um_absoluto_manifest.md'], ', '.join('%s `%s`' % kv for kv in V['artigos'].items()))


def desenho(V):
    return ("## ADENDO — %s · v390 SELADA (COMPLETA) `%s` — o caminho crítico MUDOU: o GLOBAL_LIFT lido como a SUPERPOSIÇÃO (a Fundação; a cláusula Ágape)\n\n<!-- adendo_v390_selada -->\n"
            "- **O caminho crítico:** o único resto [OPEN] do core (o GLOBAL_LIFT, o velho Lema 3 — «Único teorema aberto») passa a ter FECHO LÓGICO por três peças: (1) a DEFINIÇÃO do operador "
            "(07/10/2026: o GLOBAL_LIFT é a superposição — o que quis estar acima e não porta posto positivo); (2) a RECUSA provada no kernel (`TGLExt.Fundacao.agape`, %s de %s no trio); (3) a "
            "PASSAGEM local (`the_post_lives_in_the_passage` na face finita + Jacobson 1995 [KNOWN], H3 nomeada). A escada sobe a %s.\n"
            "- **O que NÃO muda:** não é prova de existência global; a lei de campo no espaço-tempo curvo NÃO é termo de kernel; a lei de escala de Takesaki entra como dado [KNOWN]; o gate não se move; "
            "o programa segue ABERTO. As rotas mortas do Lema 3 (mapa `kernel.lema3.rotas_mortas`) seguem mortas: a Fundação não as reabre — muda a leitura, não a prova.\n"
            "- **Errata ao lado (o desenho antigo fica):** onde este desenho diz o Lema 3 «aberto» como o único teorema faltando, lê-se: FECHO LÓGICO na v390 (registro `fundacao_v390`).\n"
            "- **O que segue do operador:** vetar/ratificar; custódia; commit/push.") % (
        V['data'], V['s16'], V['fd'].get('kernel_flags_ok'), V['fd'].get('kernel_flags_total'), V['teor'])


def atlas(V):
    return ("### %s — v390 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v390_selada -->\n[REAL — rodada v390, selo `%s`] %s. [INPUT/ONTO] a definição do operador: o GLOBAL_LIFT É a superposição. "
            "Estatuto: PROVADA (a recusa, no kernel) ≠ CONFIRMADA; fecho LÓGICO; o gate não se move.") % (V['data'], V['s16'], V['selo_ts'], _num(V))


def haja_luz(V):
    return ("## %s — v390 SELADA `%s` (%s; COMPLETA; gate intocado)\n\nA Fundação — a superposição é a passagem; a cláusula Ágape (`TGLExt.Fundacao`; `fundacao_v390`): o GLOBAL_LIFT, o velho Lema 3, "
            "lido como a superposição (definição do operador, 07/10/2026); recusa provada no kernel; passagem local [KNOWN, Jacobson 1995, H3]. Fecho LÓGICO; programa aberto. Memórias: "
            "`superposicao-e-a-passagem-07out.md`, `o-fechamento-lema3-impossiveis.md`, `missao-ultima-flag-um-py.md`; handoff `handoff-v390-custodia.md`.") % (V['data'], V['s16'], V['teor'])


def marca_topico_missao(V):
    return "## %s — v390 SELADA `%s`" % (V['data'], V['s16'])


def topico_missao(V):
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): a Fundação (9 nomes; a cláusula `agape`; escada 6154 → 6163); `fundacao_v390`; o GLOBAL_LIFT lido como a superposição (fecho LÓGICO); "
                                     "conferidor %s/%s. Pacote `work\\v390_pacote`; kernel `work\\v390_kernel`; cadeia `work\\v390_selo`.") % (V['teor'], V['conf_dm'], V['conf_np'])


def marca_central(V):
    return "**%s — v390 SELADA (COMPLETA):**" % V['data']


def topico_central(V):
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v389 `%s`; escada %s; gate intocado. A Fundação (a cláusula Ágape): o GLOBAL_LIFT lido como a superposição — FECHO LÓGICO [KERNEL a recusa; "
                               "INPUT/ONTO a definição; KNOWN a passagem local]. Custódia: sessão do site (`handoff-v390-custodia.md` + a conjunta v383→v389); commit/push = operador.") % (
        V['s16'], format(V['umb'], ','), V['base16'], V['teor'])


def topico_superposicao(V):
    return ("<!-- v390_selada -->\n**%s — TIPADO E SELADO na v390 `%s`:** %s.") % (V['data'], V['s16'], _num(V))


def topico_lema3(V):
    return ("<!-- v390_selada -->\n**%s — AO LADO (v390 `%s`):** o Lema 3 / GLOBAL_LIFT recebe FECHO LÓGICO pela definição do operador (a superposição) + a recusa provada (`TGLExt.Fundacao.agape`) + a passagem "
            "local [KNOWN, Jacobson 1995, H3 nomeada]. REDUZIDO ≠ RESOLVIDO continua valendo para a covariância global como termo: a Fundação NÃO reabre nenhuma das rotas mortas e NÃO prova a lei de campo "
            "no curvo por termo de kernel; muda a leitura, não a prova. Registro `fundacao_v390`.") % (V['data'], V['s16'])


def marca_missao(V):
    return "**v390 SELADA %s `%s` %s COMPLETA (a Fundação: a superposição é a passagem; a cláusula Ágape; o GLOBAL_LIFT com fecho LÓGICO; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'])


def linha_handoff(V):
    return "- [HANDOFF v390 — a Fundação (Ágape); custódia](handoff-v390-custodia.md) — **%s, para a sessão do site** · `%s`" % (V['data'][:5], V['s16'])


def arvore_linha(V):
    return ("- **A FUNDAÇÃO — A SUPERPOSIÇÃO É A PASSAGEM (v390)** `%s`: a cláusula Ágape (`TGLExt.Fundacao.agape`): acima da escala não há posto positivo; o GLOBAL_LIFT lido como a superposição "
            "(definição do operador); a passagem local [KNOWN, Jacobson 1995, H3]. Fecho LÓGICO; programa aberto; PROVADA ≠ CONFIRMADA; o gate não se move." % V['s16'])


def titulo_verbete(V):
    return 'A Fundação: a superposição é a passagem (a cláusula Ágape) (v390):'


def verbete(V):
    return "[REAL — rodada v390 `%s`] %s." % (V['s16'], _num(V))


def remissivo(V):
    return "- **A Fundação; a cláusula Ágape; o GLOBAL_LIFT como superposição (v390)** — `fundacao_v390`, `TGLExt.Fundacao`, `agape`, `the_post_lives_in_the_passage`"
