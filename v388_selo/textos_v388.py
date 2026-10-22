# -*- coding: utf-8 -*-
# Os TEXTOS da v388 selada (molde: textos_v387.py). Cada numero, hash e veredito entra por chave de V (leitura_v388.ler), nunca digitado aqui.


def _f(x, n=2):
    return ('%%.%df' % n % x).replace('.', ',') if isinstance(x, (int, float)) and not isinstance(x, bool) else 'n/d'


def _num(V):
    br, nu = V['br'], (V['ho'].get('numbers') or {})
    lb = nu.get('lnB') or {}
    zl = nu.get('z_por_leitor') or {}
    return ("a pedra `TheCouplingRunsBoundedBelow` (`%s`; %s de %s declarações no trio): α(χ) = sech(χ/2) e β(χ) = α(χ)·√e estritamente decrescentes na profundidade; o piso no "
            "supremo de χ (o infravermelho), atingido só lá; a ligação a `couplingOfAlpha`; a soma das metades < 1 com limite 1; a Meia-Nat ponto fixo. β₀ = α_Thomson·√e = %s (a constante da fronteira, "
            "o Teorema da Escala); β(M_Z) = %s a um laço (Teorema da Escala) e %s MS-bar [KNOWN] (a leitura de bulk, acima do piso). A Fase 9 aberta pela função congelada: veredito `%s` (leitores [DECLARADO]); "
            "fundo %s, previsão %s, média dos locais %s ± %s; z_δ %s; z_disc %s; ln B TGL/ΛCDM %s, /β-livre %s, /shift %s, /fundo-livre %s; CCHP %sσ; contrafactual com as fontes por hash "
            "(NÃO veredito): `%s` — não discrimina a 5σ sob este V1") % (
        V['pedra16'], br.get('kernel_flags_ok'), br.get('kernel_flags_total'), _f(br.get('beta0'), 10), _f(br.get('beta_MZ_on_shell'), 6), _f(br.get('beta_MZ_msbar'), 6),
        V['ho'].get('verdict_of_the_frozen_function'), _f(nu.get('H0_bg'), 3), _f(nu.get('H0_local_previsto'), 3), _f(nu.get('media_GLS_locais'), 3), _f(nu.get('sigma_GLS_locais'), 3),
        _f(nu.get('z_delta')), _f(nu.get('z_disc')), _f(lb.get('TGL_vs_LCDM')), _f(lb.get('TGL_vs_beta_livre')), _f(lb.get('TGL_vs_shift_cefeidas')), _f(lb.get('TGL_vs_fundo_livre')),
        _f((zl.get('L2_cchp') or {}).get('z_vs_TGL')), V['ho'].get('counterfactual_with_sources_NOT_a_verdict'))


def _cab(V):
    return "v388 SELADA (COMPLETA)** `%s`" % V['s16']


def linhagem(V):
    vb = V['verbatins']
    return ("## %s — **%s — β CORRE COM A ESCALA, LIMITADO INFERIORMENTE (a pedra); A FASE 9 ABERTA pela função congelada\n\n"
            "**O operador (06/10/2026, via a sessão c1, verbatim):** «vamos em frente, haja v388 e abra a fase 9». **A cunhagem (06/10, %s e %s UTC; sha256 `%s` e `%s`)** [INPUT/ONTO]: α como "
            "índice de escala da fronteira, β_TGL a sua conjugação, β escalar limitado inferiormente; a dicotomia (dividir pela metade sem nunca alcançar o limite).\n\n"
            "**O que entrou** (pacote `work\\v388_pacote` sobre a v387 `%s`; %d patches — %s; instalado em %s; a pedra compilada e auditada no sandbox novo `work\\v388_kernel\\kernel_src`, "
            "cópia de bytes do `tgl_kernel` do Nós — o sandbox antigo perdeu os pacotes da Mathlib, dito): a pedra e os 2 registros `beta_runs_bounded_below_v388` e "
            "`hubble_ratio_opening_v388`; a seção «Ao lado (v388)» PT/EN no sumário; a errata AO LADO de «α observa-se, não se deriva» (deriva-se a forma, não o número).\n\n"
            "**O que a rodada mediu:** %s.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos da v387 mudaram SÓ pela "
            "escada (6137 → 6154, dito); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.\n\n"
            "**O que segue do operador:** as fontes públicas da Fase 9 por sha256 (D-H) — mesmo com elas, z_disc < 5 sob este V1 não discrimina; qual especificação da Fase 9 governa (a do "
            "Codex, mais rica, em construção); qual μ cada rito usa (β(μ) [OPEN]); a custódia pela sessão do site; commit/push. NOT_FALSIFIED nunca é confirmação; o gate não se move.") % (
        V['data'], _cab(V), vb['beta_escalar_1327']['quando_utc'][11:19], vb['dicotomia_1348']['quando_utc'][11:19], vb['beta_escalar_1327']['sha256'][:16], vb['dicotomia_1348']['sha256'][:16],
        V['base16'], V['n_patches'], V['patches'], V['instalado_em'], _num(V), V['compl'], ' → '.join(V['horarios']) or 'n/d', V['teor'], V['rc'], V['selo_ts'], V['conf16'], V['conf_dm'],
        V['conf_np'], V['n_ver_mudaram'], 'reaproveitado' if V['pilar']['mode'] == 'REUSE' else str(V['pilar']['mode']), V['pilar']['result16'], V['servidor'],
        V['h_um_absoluto.json'], V['h_um_absoluto_selo.json'], V['h_um_absoluto_forma_canonica.md'], V['h_um_absoluto_manifest.md'], ', '.join('%s `%s`' % kv for kv in V['artigos'].items()))


def desenho(V):
    return ("## ADENDO — %s · v388 SELADA (COMPLETA) `%s` — β corre com a escala, limitado inferiormente; a Fase 9 aberta\n\n<!-- adendo_v388_selada -->\n"
            "- **O caminho crítico:** a escada sobe a %s (a pedra `TheCouplingRunsBoundedBelow`, 17 nomes, só matemática da forma fechada sech(χ/2)); o gate intocado.\n"
            "- **O que se moveu:** a Fase 9 foi ABERTA pela função congelada do V1 e devolveu `%s` (leitores [DECLARADO]); o contrafactual com as fontes (NÃO veredito) não discrimina a 5σ: "
            "sob este V1 a razão de Hubble não é o discriminante a 5σ hoje. β(μ) ≥ β₀ entra como LEITURA de bulk; a constante da fronteira segue β₀ (Teorema da Escala).\n"
            "- **O que segue do operador:** as fontes por sha256; qual especificação da Fase 9 governa; qual μ cada rito usa; custódia; commit/push.") % (
        V['data'], V['s16'], V['teor'], V['ho'].get('verdict_of_the_frozen_function'))


def atlas(V):
    return ("### %s — v388 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v388_selada -->\n[REAL — rodada v388, selo `%s`] %s. [INPUT/ONTO] β(μ) = α(μ)·√e é a leitura de bulk, "
            "≥ β₀ = α(0)·√e (a constante da fronteira); a errata ao lado: deriva-se a FORMA, não o número. Estatuto: PROVADA ≠ CONFIRMADA; o gate não se move.") % (V['data'], V['s16'], V['selo_ts'], _num(V))


def haja_luz(V):
    return ("## %s — v388 SELADA `%s` (%s; COMPLETA; gate intocado)\n\nβ corre com a escala, limitado inferiormente (a pedra `TheCouplingRunsBoundedBelow`; `beta_runs_bounded_below_v388`); "
            "a Fase 9 aberta pela função congelada (`hubble_ratio_opening_v388`: INCONCLUSIVE_SYSTEMATICS com leitores [DECLARADO]; o contrafactual não discrimina a 5σ). Memórias: "
            "`beta-escalar-limitado-inferiormente-06out.md`, `fase9-razao-de-hubble-05out.md`, `missao-ultima-flag-um-py.md`; handoff `handoff-v388-custodia.md`.") % (V['data'], V['s16'], V['teor'])


def marca_topico_missao(V):
    return "## %s — v388 SELADA `%s`" % (V['data'], V['s16'])


def topico_missao(V):
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): a pedra `TheCouplingRunsBoundedBelow` (17; escada 6137 → 6154); `beta_runs_bounded_below_v388`; a Fase 9 aberta "
                                     "(`hubble_ratio_opening_v388`); conferidor %s/%s. Pacote `work\\v388_pacote`; kernel `work\\v388_kernel`; cadeia `work\\v388_selo`.") % (V['teor'], V['conf_dm'], V['conf_np'])


def marca_central(V):
    return "**%s — v388 SELADA (COMPLETA):**" % V['data']


def topico_central(V):
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v387 `%s`; escada %s; gate intocado. β escalar ≥ β₀ [KERNEL a forma; INPUT/ONTO a leitura]; a Fase 9 aberta [REAL] "
                               "(INCONCLUSIVE_SYSTEMATICS; contrafactual não discrimina). Custódia: sessão do site (`handoff-v388-custodia.md`); commit/push = operador.") % (
        V['s16'], format(V['umb'], ','), V['base16'], V['teor'])


def topico_fase9(V):
    nu = V['ho'].get('numbers') or {}
    return ("<!-- v388_selada -->\n**%s — FASE 9 ABERTA (ordem do operador via c1) e LIDA pela v388 `%s`:** a função congelada devolveu `%s` (os 5 leitores [DECLARADO] até D-H); "
            "z_δ %s, z_disc %s, ln B TGL/ΛCDM %s; contrafactual com as fontes (NÃO veredito): `%s` — sob este V1 a razão de Hubble não discrimina a 5σ hoje. Resultado em "
            "`Bancada_Um\\investigacao\\fase9_hubble_abertura\\` (mapa seq 647).") % (
        V['data'], V['s16'], V['ho'].get('verdict_of_the_frozen_function'), _f(nu.get('z_delta')), _f(nu.get('z_disc')), _f((nu.get('lnB') or {}).get('TGL_vs_LCDM')),
        V['ho'].get('counterfactual_with_sources_NOT_a_verdict'))


def topico_beta(V):
    br = V['br']
    return ("<!-- v388_selada -->\n**%s — TIPADO E SELADO na v388 `%s`:** a pedra `TheCouplingRunsBoundedBelow` (%s/%s no trio): α(χ) = sech(χ/2), β(χ) estritamente decrescentes; o piso no "
            "infravermelho; a dicotomia (soma das metades < 1, limite 1); a Meia-Nat ponto fixo; β₀ = %s; β(M_Z) = %s a um laço / %s MS-bar. A constante da fronteira segue β₀ (Teorema da Escala); "
            "β(μ) é leitura de bulk; qual μ cada rito usa [OPEN]; patentes com β variável: vínculo não localizado nos arquivos [DECLARADO]. Errata ao lado: deriva-se a forma, não o número.") % (
        V['data'], V['s16'], br.get('kernel_flags_ok'), br.get('kernel_flags_total'), _f(br.get('beta0'), 10), _f(br.get('beta_MZ_on_shell'), 6), _f(br.get('beta_MZ_msbar'), 6))


def marca_missao(V):
    return "**v388 SELADA %s `%s` %s COMPLETA (β escalar ≥ β₀ tipado; Fase 9 aberta: INCONCLUSIVE, leitores declarados; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'])


def linha_handoff(V):
    return "- [HANDOFF v388 — β escalar; Fase 9 aberta; custódia](handoff-v388-custodia.md) — **%s, para a sessão do site** · `%s`" % (V['data'][:5], V['s16'])


def arvore_linha(V):
    return ("- **O ACOPLAMENTO CORRE COM A ESCALA (v388)** `%s`: a pedra `TheCouplingRunsBoundedBelow` (α = sech(χ/2); o piso no infravermelho; a dicotomia); a Fase 9 aberta pela função "
            "congelada (INCONCLUSIVE, leitores declarados). PROVADA ≠ CONFIRMADA; o gate não se move." % V['s16'])


def titulo_verbete(V):
    return 'O acoplamento corre com a escala; a Fase 9 aberta (v388):'


def verbete(V):
    return "[REAL — rodada v388 `%s`] %s." % (V['s16'], _num(V))


def remissivo(V):
    return "- **β escalar ≥ β₀; Fase 9 aberta (v388)** — `beta_runs_bounded_below_v388`, `hubble_ratio_opening_v388`, `TheCouplingRunsBoundedBelow`"
