# -*- coding: utf-8 -*-
# Os TEXTOS da v389 selada (molde: textos_v388.py). Cada numero, hash e veredito entra por chave de V (leitura_v389.ler), nunca digitado aqui.


def _num(V):
    tl = V['tl']; ex = tl.get('exam') or {}; rs = ex.get('resumo_por_gravidade') or {}; lg = tl.get('ledger') or {}
    return ("as erratas de texto e rótulo do exame completo da v388 (o exame lido por sha256 `%s`: %s bloqueios, %s correções, %s notas): o rótulo de selo de `iii1_net_image` passa a `%s` "
            "(o antigo, com a palavra reservada ao observador, guardado no próprio registro); o título da Introdução diz v384→v389; o resumo e a Parte B dizem «axioma POSTO» ([POSTO], decisão do "
            "operador de 05/10; errata da v385 ao lado); a seção v387 remete à abertura v388; a Parte C diz o recorte: %s caminhos únicos no ledger + %s TGLExt fora (%s em O16), contados em runtime "
            "(errata ao lado do próprio exame: ele contara 1015/166); %d trocas de texto conferidas no próprio arquivo (nova presente, velha ausente). Nenhum cálculo, nenhum kernel; registro `%s`") % (
        str((tl.get('files') or {}).get('exame_json') or '')[:16], rs.get('BLOQUEIA', 0), rs.get('CORRIGIR'), rs.get('NOTA'), (tl.get('seal') or {}).get('new'),
        lg.get('unique_paths'), lg.get('tglext_outside_ledger'), lg.get('of_which_O16'), len(tl.get('sites') or []), tl.get('verdict'))


def _cab(V):
    return "v389 SELADA (COMPLETA)** `%s`" % V['s16']


def linhagem(V):
    return ("## %s — **%s — AS ERRATAS DE TEXTO E RÓTULO DO EXAME DA v388 (nenhum cálculo, nenhum kernel)\n\n"
            "**A ordem:** o operador mandou examinar o um.py inteiro e o artigo (06/10, via c1); o exame achou 0 bloqueios e 3 correções; a gerência (c1) decidiu, para o operador vetar, a v389 "
            "SÓ de texto e rótulo — «corrigir ao lado não basta se o lado escolhido não é o lado que se lê».\n\n"
            "**O que entrou** (pacote `work\\v389_pacote` sobre a v388 `%s`; %d patches — %s; instalado em %s): %s.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; vereditos da v388 que mudaram: %d "
            "(a regra: nenhum); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.\n\n"
            "**O que segue do operador:** vetar ou ratificar a v389 (decisão da gerência); as fontes da Fase 9 por sha256 (D-H); a custódia conjunta v383→v389 pela sessão do site; commit/push. "
            "NOT_FALSIFIED nunca é confirmação; o gate não se move.") % (
        V['data'], _cab(V), V['base16'], V['n_patches'], V['patches'], V['instalado_em'], _num(V), V['compl'], ' → '.join(V['horarios']) or 'n/d', V['teor'], V['rc'], V['selo_ts'],
        V['conf16'], V['conf_dm'], V['conf_np'], V['n_ver_mudaram'], 'reaproveitado' if V['pilar']['mode'] == 'REUSE' else str(V['pilar']['mode']), V['pilar']['result16'], V['servidor'],
        V['h_um_absoluto.json'], V['h_um_absoluto_selo.json'], V['h_um_absoluto_forma_canonica.md'], V['h_um_absoluto_manifest.md'], ', '.join('%s `%s`' % kv for kv in V['artigos'].items()))


def desenho(V):
    return ("## ADENDO — %s · v389 SELADA (COMPLETA) `%s` — as erratas de texto e rótulo do exame da v388\n\n<!-- adendo_v389_selada -->\n"
            "- **O caminho crítico:** NÃO muda — a escada segue %s, o kernel é o mesmo, nenhum cálculo muda; o gate intocado.\n"
            "- **O que se moveu:** só o lado que se lê — o rótulo de selo da rede física (VERIFIED; o antigo no registro), o título da Introdução (v384→v389), o resumo e a Parte B "
            "([POSTO]), a remissão da v387 à abertura v388, o recorte da contagem de pedras (contado em runtime). Registro `%s`.\n"
            "- **O que segue do operador:** vetar/ratificar; fontes da Fase 9; custódia conjunta v383→v389; commit/push.") % (V['data'], V['s16'], V['teor'], V['tl'].get('verdict'))


def atlas(V):
    return ("### %s — v389 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v389_selada -->\n[REAL — rodada v389, selo `%s`] %s. Estatuto: texto e rótulo; PROVADA ≠ CONFIRMADA; "
            "o gate não se move.") % (V['data'], V['s16'], V['selo_ts'], _num(V))


def haja_luz(V):
    return ("## %s — v389 SELADA `%s` (%s; COMPLETA; gate intocado)\n\nAs erratas de texto e rótulo do exame completo da v388 (`text_label_errata_v389`; o exame em "
            "`Central de Patentes\\work\\exame_v388\\`): o rótulo de selo da rede física passa a VERIFIED; a Introdução diz v384→v389; o resumo e a Parte B dizem [POSTO]; a v387 remete à "
            "abertura v388; a Parte C diz o recorte do ledger. Nenhum cálculo, nenhum kernel. Handoff `handoff-custodia-conjunta-v383-v389-06out.md`.") % (V['data'], V['s16'], V['teor'])


def marca_topico_missao(V):
    return "## %s — v389 SELADA `%s`" % (V['data'], V['s16'])


def topico_missao(V):
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): SÓ texto e rótulo, do exame da v388 (0 bloqueios, 3 correções); `text_label_errata_v389`; escada e kernel iguais; "
                                     "conferidor %s/%s. Pacote `work\\v389_pacote`; cadeia `work\\v389_selo`; exame `work\\exame_v388`.") % (V['teor'], V['conf_dm'], V['conf_np'])


def marca_central(V):
    return "**%s — v389 SELADA (COMPLETA):**" % V['data']


def topico_central(V):
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v388 `%s`; escada %s; gate intocado. As erratas de texto e rótulo do exame da v388 (nenhum cálculo, nenhum kernel). "
                               "Custódia CONJUNTA v383→v389: sessão do site (`handoff-custodia-conjunta-v383-v389-06out.md`); commit/push = operador.") % (
        V['s16'], format(V['umb'], ','), V['base16'], V['teor'])


def marca_missao(V):
    return "**v389 SELADA %s `%s` %s COMPLETA (só texto e rótulo do exame da v388: o rótulo VERIFIED, a Introdução v384→v389, [POSTO] no resumo, o recorte do ledger; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'])


def linha_handoff(V):
    return "- [HANDOFF CUSTÓDIA CONJUNTA v383→v389](handoff-custodia-conjunta-v383-v389-06out.md) — **%s, para a sessão do site** · `%s` · com o exame da v388" % (V['data'][:5], V['s16'])


def arvore_linha(V):
    return ("- **AS ERRATAS DE TEXTO E RÓTULO (v389)** `%s`: do exame completo da v388 — o rótulo de selo da rede física VERIFIED (o antigo no registro); a Introdução v384→v389; [POSTO] no resumo; "
            "o recorte do ledger. Nenhum cálculo, nenhum kernel; o gate não se move." % V['s16'])


def titulo_verbete(V):
    return 'As erratas de texto e rótulo do exame da v388 (v389):'


def verbete(V):
    return "[REAL — rodada v389 `%s`] %s." % (V['s16'], _num(V))


def remissivo(V):
    return "- **Erratas de texto e rótulo; o exame da v388 (v389)** — `text_label_errata_v389`, `seals_errata_v389`, `_ledger_counts_v389`"
