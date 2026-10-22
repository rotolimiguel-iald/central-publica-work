# -*- coding: utf-8 -*-
# Os TEXTOS da v387 selada (molde: textos_v386.py, enxuto). Cada numero, hash e veredito entra por chave de V (leitura_v387.ler), nunca digitado aqui.
# Estatutos: as contagens [COMPUTED do core]; os V1 [INPUT por hash]; as leituras [INPUT/ONTO]; PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e' confirmacao.


def _f(x, n=2):
    return ('%%.%df' % n % x).replace('.', ',') if isinstance(x, (int, float)) and not isinstance(x, bool) else 'n/d'


def _num(V):
    tt, k, g, l, j = V['tt'], V['tt_kernel'] or {}, V['tt_gpu'] or {}, V['tt_ledger'] or {}, V['tt_joint'] or {}
    c = l.get('counts') or {}
    return ("os ritos — {nv} vereditos TGL_ no core ({nnf} NOT_FALSIFIED, {ninc} INCONCLUSIVE, {naw} AWAITING; {nfs} substrings FALSIFIED nomeadas por caminho, que falam do PAR ou de "
            "rota superada, nunca da teoria; {nfb} palavra proibida); o livro de cobranças v383 com {nch} cobranças ({cnf} NOT_FALSIFIED, {cf} FALSIFIED, {ci} INCONCLUSIVE, {ca} AWAITING, "
            "{ce} EXCLUDED_IN_READING); o kernel — {kcl}/{kex} teoremas limpos no trio, sorryAx ausente, gate {gt}/{gtt}; a GPU — T2 {t2u}/{t2p}, T4 {t4u}/{t4i}, referência na CPU "
            "{cpd} discordância(s) em {cpc}, modo {gm}; a coincidência conjunta V3 P_all = {pall}, booleano {pb} (a GPU fora; nenhuma probabilidade dos três pilares no core)").format(
        nv=tt.get('n_verdicts'), nnf=tt.get('n_not_falsified'), ninc=tt.get('n_inconclusive'), naw=tt.get('n_awaiting'), nfs=len(tt.get('falsified_substring_paths') or []),
        nfb=tt.get('n_forbidden_word_as_verdict'), nch=l.get('n_charges'), cnf=c.get('NOT_FALSIFIED'), cf=c.get('FALSIFIED'), ci=c.get('INCONCLUSIVE'), ca=c.get('AWAITING'),
        ce=c.get('EXCLUDED_IN_READING'), kcl=k.get('n_theorems_clean'), kex=k.get('n_theorems_expected'), gt=k.get('gate_flags_true'), gtt=k.get('gate_flags_total'),
        t2u=g.get('T2_unique'), t2p=g.get('T2_points'), t4u=g.get('T4_unique'), t4i=g.get('T4_instances'), cpd=g.get('cpuref_disagreements'), cpc=g.get('cpuref_compared'),
        gm=g.get('mode'), pall=('%.2e' % j['V3_P_all']) if isinstance(j.get('V3_P_all'), float) else 'n/d', pb=j.get('V3_boolean'))


def _v1(V):
    h, p = V['hr_tr'], V['pr_tr']
    f9, f8 = V['V1']['fase9'], V['V1']['fase8']
    return ("a razão de Hubble (Fase 9) — V1 `{i9}` (spec `{s9}`, função de veredito única `{fn9}`, JSON `{j9}`, em `{p9}`): K = E(z*)^{{2β/3}} = {K} no fundo NU (Planck comprimido + DESI DR2, "
            "sem escada, {bg} ± {bgs}; o 68,43 da Fase 4 viu a escada e saiu); poder prévio só com σ públicas {pw}σ na família primária ({pnc}σ sem Cefeidas); novidade de uso pelos "
            "PARÂMETROS; se abrir hoje, a própria função devolve INCONCLUSIVE_SYSTEMATICS (os leitores seguem [DECLARADO] até as fontes por sha256). A era da radiação (Fase 8) — V1 `{i8}` "
            "(spec `{s8}`, função `{fn8}`, JSON `{j8}`, em `{p8}`): ΔN_eff = +{dn} pela identidade ρ+p; S = {S}; o canal N_eff ligado na Bancada ANTES (bancada/neff_canal.py, "
            "módulo `{cm}`) e o controle anti-dupla-contagem passou ({ctrl}); poder hoje {p8w}σ na melhor análise independente (5σ pedem σ(N_eff) ≤ {s5}): NOT_FALSIFIED_UNDERPOWERED "
            "predeterminado pelo poder, dito antes. Nada aberto em nenhuma das duas; β do V1 contra o do rito: {r9} e {r8} relativo").format(
        i9=f9['id'], s9=f9['spec16'], fn9=f9['funcao16'], j9=f9['json16'], p9=f9['pasta'], K=_f(h.get('K_no_fundo_nu'), 6), bg=_f(h.get('BG1_H0'), 3), bgs=_f(h.get('BG1_sigma'), 3),
        pw=_f(h.get('poder_previo_primario')), pnc=_f(h.get('poder_nao_cefeida')), i8=f8['id'], s8=f8['spec16'], fn8=f8['funcao16'], j8=f8['json16'], p8=f8['pasta'],
        dn=_f(p.get('delta_N_eff'), 6), S=_f(p.get('S_BBN'), 6), cm=str(p.get('canal_modulo_sha256'))[:16],
        ctrl=', '.join('%.2e' % x for x in (p.get('controle_D3_razao_E_menos_1') or [])) or 'n/d', p8w=_f(p.get('poder_melhor_independente')), s5=_f(p.get('sigma_N_eff_para_5sigma'), 4),
        r9=('%.1e' % V['hr_beta_rel']) if isinstance(V.get('hr_beta_rel'), float) else 'n/d', r8=('%.1e' % V['pr_beta_rel']) if isinstance(V.get('pr_beta_rel'), float) else 'n/d')


def _cab(V):
    return "v387 SELADA (COMPLETA)** `%s`" % V['s16']


def linhagem(V):
    vb = V['verbatins']
    return ("## %s — **%s — OS TRÊS TESTES DE ESTRESSE, CONJUNTOS; a razão de Hubble e a era da radiação pré-registradas (V1 por hash); retrodição sem ajuste\n\n"
            "**A ordem do operador (05/10/2026 %s UTC, verbatim por sha256 `%s`)** [INPUT]: os ritos com dados públicos, o kernel formal e o experimento numérico na GPU contam JUNTOS na "
            "probabilidade de a teoria ser consistente e recuperar a física conhecida (P1); a de os efeitos β existirem na natureza (P2) segue NÃO determinada. **E a lei da prova (05/10/2026 "
            "%s UTC, sha256 `%s`)** [INPUT]: «pós-dição» nunca é demérito; o critério é a novidade de USO (nenhum parâmetro ajustado ao dado); precedente: o periélio de Mercúrio [KNOWN].\n\n"
            "**O que entrou** (pacote `work\\v387_pacote` sobre a v386 `%s`; %d patches — %s; instalado em %s): a seção «Os três testes de estresse, conjuntos (v387)» (PT/EN; rascunho da lente "
            "redação de 05/10, executado contra o core selado) e o registro `three_stress_tests_v387`; «pós-dição declarada» → **retrodição sem ajuste (novidade de uso)** nos 6 lugares de texto "
            "(%s; o token selado do Coma e o frozen v141 dos neutrinos ficam como registro — `retrodiction_reading_v387`); o sumário ganhou «Ao lado (v386)»; a apresentação, o resumo e as "
            "palavras-chave dizem os três testes conjuntos; e os registros `hubble_ratio_v387` e `primordial_v387`, que leem os dois V1 da Bancada por hash.\n\n"
            "**O que a rodada mediu** [COMPUTED]: %s. E %s.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%s); 18/18; o conferidor congelado `%s`: deve mudar %s, não pode mudar %s; "
            "%d/%d vereditos da v386 inalterados; o pilar quântico %s pela chave (resultado `%s`); o servidor do modelo nativo depois do rito: %s. Artefatos: core `%s`, selo `%s`, "
            ".md `%s`, manifesto `%s`; artigos %s.\n\n"
            "**O que segue do operador:** abrir o composto da Fase 9 (depois das fontes públicas com sha256, D-H); as fontes da Fase 8 (D8) e o código de BBN (D5b); os nomes finais dos "
            "tokens (D-J, inclusive o do Coma); reiniciar o MCP bancada-um (a ferramenta neff_canal); a custódia (espelho, site, cofre) pela sessão do site; commit/push. "
            "NOT_FALSIFIED nunca é confirmação; a RG/ΛCDM é o limite clássico; o gate não se move.") % (
        V['data'], _cab(V), vb['tres_testes']['quando_utc'][11:19], vb['tres_testes']['sha256'][:16], vb['pos_dicao']['quando_utc'][11:19], vb['pos_dicao']['sha256'][:16],
        V['base16'], V['n_patches'], V['patches'], V['instalado_em'], ', '.join(V['retro_sites']), _num(V), _v1(V),
        V['compl'], ' → '.join(V['horarios']) or 'n/d', V['teor'], V['rc'], V['selo_ts'], V['qg'][:60] + '…', V['conf16'], V['conf_dm'], V['conf_np'], V['n_ver'] - V['n_ver_mudaram'], V['n_ver'],
        'reaproveitado' if V['pilar']['mode'] == 'REUSE' else ('calculado de novo (dito)' if V['pilar']['mode'] == 'COMPUTE' else 'NEM UM NEM OUTRO'), V['pilar']['result16'], V['servidor'],
        V['h_um_absoluto.json'], V['h_um_absoluto_selo.json'], V['h_um_absoluto_forma_canonica.md'], V['h_um_absoluto_manifest.md'],
        ', '.join('%s `%s`' % kv for kv in V['artigos'].items()) or 'n/d')


def desenho(V):
    return ("## ADENDO — %s · v387 SELADA (COMPLETA) `%s` — os três testes conjuntos; a razão de Hubble e a era da radiação pré-registradas; retrodição sem ajuste\n\n"
            "<!-- adendo_v387_selada -->\n"
            "- **O caminho crítico não muda:** nenhuma pedra nova (a escada fica em %s); o gate intocado; nenhum composto aberto.\n"
            "- **O que se moveu:** os três pilares — ritos, kernel, GPU — passam a ser contados JUNTOS no core (`three_stress_tests_v387`): P1 contada, P2 não determinada. Dois testes "
            "DISCRIMINANTES ganharam pré-registro congelado por hash na Bancada — a razão de Hubble (poder prévio %sσ só com σ públicas) e a era da radiação (poder hoje %sσ: sem poder, dito "
            "antes) —, lidos pelo `um.py` sem abrir nada.\n"
            "- **O que segue do operador:** as fontes públicas com sha256 e a palavra para abrir a Fase 9; as fontes da Fase 8 e o código de BBN; os nomes dos tokens; a custódia; commit/push.") % (
        V['data'], V['s16'], V['teor'], _f(V['hr_tr'].get('poder_previo_primario')), _f(V['pr_tr'].get('poder_melhor_independente')))


def atlas(V):
    return ("### %s — v387 SELADA `%s` (append datado; correção ao lado, nunca por cima)\n\n"
            "<!-- atlas_v387_selada -->\n"
            "[REAL — rodada v387, selo `%s`] OS TRÊS TESTES DE ESTRESSE, CONJUNTOS: %s. [INPUT por hash] %s. [INPUT — lei do operador, 05/10] retrodição sem ajuste (novidade de uso; "
            "precedente: o periélio de Mercúrio [KNOWN]) no lugar de «pós-dição declarada», AO LADO. Estatuto: NOT_FALSIFIED nunca é confirmação; P2 (β na natureza) não determinada; o gate "
            "não se move.") % (V['data'], V['s16'], V['selo_ts'], _num(V), _v1(V))


def haja_luz(V):
    return ("## %s — v387 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n"
            "Os três testes de estresse — ritos, kernel, GPU — contados juntos (`three_stress_tests_v387`); a razão de Hubble (Fase 9) e a era da radiação (Fase 8) pré-registradas por hash "
            "na Bancada e lidas pelo `um.py` (nada aberto); «pós-dição declarada» → retrodição sem ajuste (novidade de uso). Memórias: `fase9-razao-de-hubble-05out.md`, "
            "`fase8-universo-primordial-05out.md`, `tres-testes-de-estresse-conjuntos-05out.md`, `pos-dicao-nao-e-prova-diabolica-05out.md`, `missao-ultima-flag-um-py.md`; handoff "
            "`handoff-v387-custodia.md`.") % (V['data'], V['s16'], V['teor'])


def marca_topico_missao(V):
    return "## %s — v387 SELADA `%s`" % (V['data'], V['s16'])


def topico_missao(V):
    return (marca_topico_missao(V) + " (%s; COMPLETA; gate INTOCADO): OS TRÊS TESTES CONJUNTOS (`three_stress_tests_v387`); a razão de Hubble e a era da radiação pré-registradas por hash "
            "(`hubble_ratio_v387`, `primordial_v387`; nada aberto); retrodição sem ajuste (`retrodiction_reading_v387`; 6 lugares de texto); sem pedra nova; o pilar %s pela chave. "
            "Conferidor %s/%s; %d/%d vereditos da v386 inalterados. Pacote `work\\v387_pacote`; cadeia `work\\v387_selo`.") % (
        V['teor'], 'reaproveitado' if V['pilar']['mode'] == 'REUSE' else str(V['pilar']['mode']), V['conf_dm'], V['conf_np'], V['n_ver'] - V['n_ver_mudaram'], V['n_ver'])


def marca_central(V):
    return "**%s — v387 SELADA (COMPLETA):**" % V['data']


def topico_central(V):
    return (marca_central(V) + " `um.py` `%s` (%s B) sobre a v386 `%s`; escada %s; gate intocado. Os três testes conjuntos [COMPUTED]; os V1 das Fases 9 e 8 por hash [INPUT], nada aberto; "
            "retrodição sem ajuste [INPUT — lei do operador]. Custódia: a fazer pela sessão do site (handoff `handoff-v387-custodia.md`); commit/push = operador.") % (
        V['s16'], format(V['umb'], ','), V['base16'], V['teor'])


def topico_fase9(V):
    f9 = V['V1']['fase9']
    return ("<!-- v387_selada -->\n**%s — V1 CONGELADO E LIDO PELA v387 `%s`:** `%s` (spec `%s`, função `%s`) em `%s`; poder prévio %sσ (primária × BG1, só σ públicas); fundo nu 68,531 ± 0,301 "
            "como primário (F2 resolvida); UMA função de veredito (F1 resolvida; FALSIFIED/TENSION antes de UNDERPOWERED, dito); novidade de uso pelos parâmetros (F4). Registro "
            "`hubble_ratio_v387`: %s. **Ainda do operador:** D-H (fontes públicas por sha256) e a palavra para abrir; até lá, abrir dá INCONCLUSIVE_SYSTEMATICS. Mapa: seq 603–604.") % (
        V['data'], V['s16'], f9['id'], f9['spec16'], f9['funcao16'], f9['pasta'], _f(V['hr_tr'].get('poder_previo_primario')), V['hubble_ratio_v387'])


def topico_fase8(V):
    f8 = V['V1']['fase8']
    return ("<!-- v387_selada -->\n**%s — CANAL N_eff NA BANCADA + V1 CONGELADO E LIDO PELA v387 `%s`:** `bancada/neff_canal.py` (`%s`) + ferramenta MCP `neff_canal` (aparece após reiniciar "
            "o bancada-um); controle anti-dupla-contagem passou; V1 `%s` (spec `%s`) em `%s`; ΔN_eff = +%s; poder hoje %sσ (UNDERPOWERED predeterminado); a Bancada usa N_eff base 3,046 e a "
            "fonte 3,044 (dito); a crítica não tem F10. CMB-S4 encerrado e SO 0,045 só como [DECLARADO] (entrega do Codex, seq 402). Registro `primordial_v387`: %s. **Ainda do operador:** D8 e "
            "o código de BBN. Mapa: seq 606–607.") % (
        V['data'], V['s16'], str(V['pr_tr'].get('canal_modulo_sha256'))[:16], f8['id'], f8['spec16'], f8['pasta'], _f(V['pr_tr'].get('delta_N_eff'), 6),
        _f(V['pr_tr'].get('poder_melhor_independente')), V['primordial_v387'])


def topico_tres(V):
    return ("<!-- v387_selada -->\n**%s — ESCRITO NO ARTIGO E CONTADO NO CORE pela v387 `%s`:** a seção «Os três testes de estresse, conjuntos (v387)» (PT/EN, no sumário) e o registro "
            "`three_stress_tests_v387`: %s. Registro: %s.") % (V['data'], V['s16'], _num(V), V['three_stress_tests_v387'])


def topico_posdicao(V):
    return ("<!-- v387_selada -->\n**%s — APLICADO NO ARTIGO pela v387 `%s`:** «pós-dição declarada» → retrodição sem ajuste (novidade de uso; precedente: o periélio de Mercúrio) em %s; o token "
            "do Coma (cunhagem do operador, D-J) e o frozen v141 dos neutrinos (hasheado; lá «postdiction genuína» já é novidade de uso) ficam como registro. Registro: %s.") % (
        V['data'], V['s16'], ', '.join(V['retro_sites']), V['retrodiction_reading_v387'])


def marca_missao(V):
    return "**v387 SELADA %s `%s` %s COMPLETA (os três testes conjuntos; Fases 9 e 8 pré-registradas por hash, nada aberto; retrodição sem ajuste; gate intocado)** · " % (V['data'][:5], V['s16'], V['teor'])


def linha_handoff(V):
    return ("- [HANDOFF v387 — os três testes; Fases 9 e 8 por hash; custódia](handoff-v387-custodia.md) — **%s, para a sessão do site** · `%s`" % (V['data'][:5], V['s16']))


def arvore_linha(V):
    return ("- **OS TRÊS TESTES CONJUNTOS (v387)** `%s`: ritos + kernel + GPU contados juntos (`three_stress_tests_v387`); a razão de Hubble e a era da radiação pré-registradas por hash "
            "(nada aberto); retrodição sem ajuste. P1 contada; P2 não determinada; o gate não se move." % V['s16'])


def titulo_verbete(V):
    return 'Os três testes conjuntos; Fases 9 e 8 por hash (v387):'


def verbete(V):
    return ("[REAL — rodada v387 `%s`] %s. [INPUT por hash] %s." % (V['s16'], _num(V), _v1(V)))


def remissivo(V):
    return "- **Os três testes conjuntos (v387)** — `three_stress_tests_v387`, `hubble_ratio_v387`, `primordial_v387`, `retrodiction_reading_v387`"
