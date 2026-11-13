# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] o QUADRO do topo e a SECAO da v411 no artigo (PT/EN) e no .md (DESENHO_v411 5.1 a e 5.2): os NUMEROS sao LIDOS do core deste rito
# (core["h0dn_bg1_v411"], o recalculo do resultado da abertura), nunca digitados; os textos fixos sao conectivos da gerencia; as sete ressalvas sao as da secao 8 do pre-registro embutido, lidas pelo registro; o que o teste
# nao decide e' o resumo da gerencia no DESENHO (secao 4). Em todo bloco onde o primario aparece estao as quatro obrigacoes (o modelo publicado, as Cefeidas livres com o numero, validade nao creditacao, retrodicao e nao cego).


def _v411_n(x_, k_=2, lang_="pt", tex_=True):
    """numero formatado (virgula em PT; {,} no LaTeX PT); n/d se nao for numero."""
    if not isinstance(x_, (int, float)) or x_ != x_:
        return r"\text{n/d}" if tex_ else "n/d"
    s_ = ("%%.%df" % k_) % float(x_)
    if s_.startswith("-"):
        s_ = ("-" if tex_ else "−") + s_[1:]
    return s_.replace(".", "{,}" if tex_ else ",") if lang_ == "pt" else s_


def _v411_p(x_, lang_="pt", tex_=True):
    """p unilateral em notacao cientifica (mantissa com 1 casa)."""
    if not isinstance(x_, float) or not x_ > 0:
        return r"\text{n/d}" if tex_ else "n/d"
    import math as _m
    e_ = int(_m.floor(_m.log10(x_))); m_ = x_ / 10 ** e_
    mm_ = ("%.1f" % m_).replace(".", "{,}" if tex_ else ",") if lang_ == "pt" else "%.1f" % m_
    return (mm_ + r"\times10^{" + str(e_) + "}") if tex_ else (mm_ + "×10^" + str(e_))


def _v411_tt(s_):
    return "n/d" if s_ is None else str(s_).replace("\\", "").replace("_", r"\_\allowbreak{}").replace("&", r"\&").replace("%", r"\%")


def _v411_tex_unicode(s_):
    """o titulo e os textos lidos do DESENHO trazem unicode: no LaTeX vao como macro (licao da v408: beta como \\beta)."""
    return (str(s_).replace("×", r"$\times$").replace("·", r"$\cdot$").replace("β", r"$\beta$").replace("α", r"$\alpha$").replace("σ", r"$\sigma$").replace("τ", r"$\tau$").replace("%", r"\%"))


def _v411_atomos(r_, lang_="pt", tex_=True):
    r_ = r_ or {}; v_ = r_.get("values") or {}; pr_ = v_.get("primario") or {}; cl_ = v_.get("cefeidas_livres") or {}; km_ = v_.get("lei_em_km_s_Mpc") or {}; at_ = v_.get("atos") or {}
    N = lambda x_, k_=2: _v411_n(x_, k_, lang_, tex_)
    est_ = v_.get("estresse") or {}; ti_ = est_.get("i_tau_por_linha") or {}; an_ = (est_.get("ii_ancora_unica") or {}).get("ancoras") or {}; iii_ = est_.get("iii_vies_por_hospedeira") or {}
    c11_ = (v_.get("a_emenda_as_claras") or {}).get("a") or {}
    return {"sealed": r_.get("all_verified") is True, "zn": N(pr_.get("z_null")), "zk": N(pr_.get("z_tgl")), "D": N(pr_.get("D")), "p": _v411_p(pr_.get("p_unilateral"), lang_, tex_), "ramo": pr_.get("ramo"),
            "cab": pr_.get("cabeca_do_teste"), "out": pr_.get("outcome"), "zn_cl": N(cl_.get("z_null")), "zk_cl": N(cl_.get("z_tgl")), "D_cl": N(cl_.get("D")), "ramo_cl": cl_.get("ramo"), "cab_cl": cl_.get("cabeca"),
            "H0_bg": N(km_.get("H0_fundo")), "H0_K": N(km_.get("previsao_de_K_para_o_local")), "H0_pr": N(km_.get("lido_primario")), "H0_cl": N(km_.get("lido_cefeidas_livres")), "H0_pub": N(km_.get("publicado_pela_colaboracao")),
            "sig_pub": N(km_.get("desvio_publicado")), "K": N(v_.get("K"), 6), "logK": N(v_.get("log10K"), 6), "atos": at_, "ressalvas": list(v_.get("ressalvas_secao8") or []), "verdict": r_.get("verdict"),
            "tau": N(ti_.get("tau_hat"), 4), "zn_tau": N((ti_.get("z_null") or [None])[0]), "zn_tau_cl": N((ti_.get("z_null") or [None, None])[1]),
            "anc": {a_: N(((an_.get(a_) or {}).get("z_null") or [None])[0]) for a_ in ("N4258", "LMC", "MW")},
            "b": {b_: (N(((iii_.get(b_) or {}).get("z_null_min") or [None])[0]), N(((iii_.get(b_) or {}).get("z_null_max") or [None])[0])) for b_ in ("b_0.02", "b_0.05")},
            "agregados": list(v_.get("esperado_pelos_agregados") or []), "regra_antiga": (c11_.get("as_duas_clausulas") or [None, None, None]), "nao_decide": list(r_.get("o_que_o_teste_nao_decide") or []),
            "h_resultado": ((r_.get("insumos_pinados") or {}).get("RESULTADO_DA_ABERTURA_V411.json") or {}).get("sha256"), "n_checks": len(((r_.get("mechanics") or {}).get("checks") or [])),
            "n_ok": sum(1 for c_ in ((r_.get("mechanics") or {}).get("checks") or []) if c_.get("ok"))}


def _v411_hora(s_):
    return (str(s_)[:19].replace("T", " ") + " UTC") if s_ else "n/d"


def _v411_quadro_tex(r_, lang_, titulo_pt_):
    """O quadro H0DN x BG1 (lista de linhas para s.append), ACIMA do quadro “O Teste da Unica Palavra”. lang_ = 'pt' | 'en'."""
    a_ = _v411_atomos(r_, lang_); at_ = a_["atos"]; tt_ = _v411_tt
    sel_pt_ = r"\noindent\textbf{Nesta rodada o registro do H0DN v411 NÃO selou: o que segue é o enunciado, não um selo.}\par\smallskip" if not a_["sealed"] else r"\noindent{\scriptsize Aberto uma única vez em 12/11/2026, depois do commit público do pré-registro; recalculado neste rito.}\par\smallskip"
    sel_en_ = r"\noindent\textbf{This round the v411 H0DN record did NOT seal: what follows is the statement, not a seal.}\par\smallskip" if not a_["sealed"] else r"\noindent{\scriptsize Opened only once, on 12 Nov 2026, after the public commit of the pre-registration; recomputed in this rite.}\par\smallskip"
    ress_ = "".join(r"\item[%d.] %s" % (i_ + 1, _v411_tex_unicode(x_)) for i_, x_ in enumerate(a_["ressalvas"]))
    if not ress_:   # (v411, achado do ensaio a seco: sem o registro, a lista ficava vazia e o pdflatex parava) um item que diz que as ressalvas nao foram lidas nesta rodada
        ress_ = (r"\item (nesta rodada o registro não selou: as sete ressalvas não foram lidas do texto embutido)" if lang_ == "pt" else r"\item (this round the record did not seal: the seven reservations were not read from the embedded text)")
    if lang_ == "pt":
        nd_ = "; ".join(_v411_tex_unicode(x_) for x_ in a_["nao_decide"])
        return [r"\begin{center}\fbox{\parbox{0.93\textwidth}{\small",
                r"\noindent\textbf{" + _v411_tex_unicode(titulo_pt_) + r"}\par\smallskip", sel_pt_,
                r"\begin{enumerate}\setlength{\itemsep}{1pt}",
                r"\item \textbf{As duas linhas, juntas.} O primário, sob o modelo de erros publicado: $Z$ contra o nulo $=" + a_["zn"] + r"$ ($p$ unilateral $" + a_["p"] + r"$), $Z$ contra $K=" + a_["zk"] + r"$, $D$ de desenho $=" + a_["D"]
                + r"$, ramo (" + str(a_["ramo"]) + r"); a cabeça do teste, exata: \texttt{" + tt_(a_["cab"]) + r"}. Ao lado, no mesmo item, as Cefeidas livres: $Z$ contra o nulo $=" + a_["zn_cl"] + r"$, $Z$ contra $K=" + a_["zk_cl"]
                + r"$, $D=" + a_["D_cl"] + r"$, ramo (" + str(a_["ramo_cl"]) + r"), abaixo de 5. Retrodição sem ajuste, com emenda posterior à guarda; o teste não é cego; provado é validade, não creditação; o gate não se move.",
                r"\item \textbf{A lei, em km/s/Mpc.} O fundo BG1 lê $H_0=" + a_["H0_bg"] + r"$; a lei $K=E(z_\star)^{2\beta/3}$, com $\beta=\alpha\sqrt e$ em runtime e nenhum parâmetro ajustado, prevê $" + a_["H0_K"] + r"$ para o local ($K=" + a_["K"]
                + r"$); o dado lê $" + a_["H0_pr"] + r"$ no primário e $" + a_["H0_cl"] + r"$ com as Cefeidas livres; a colaboração publica $" + a_["H0_pub"] + r"\pm" + a_["sig_pub"] + r"$ para a rede completa.",
                r"\item \textbf{Os atos.} O pré-registro foi publicado no commit \texttt{" + tt_((at_.get("commit_do_pre_registro") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_pre_registro_utc")) + r"); a abertura começou "
                + _v411_hora(at_.get("inicio_da_abertura_utc")) + r", uma única vez; o resultado foi publicado no commit \texttt{" + tt_((at_.get("commit_do_resultado") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_resultado_utc")) + r").",
                r"\item \textbf{As sete ressalvas} (da seção 8 do pré-registro, lidas do texto embutido): \begin{itemize}\setlength{\itemsep}{0pt}" + ress_ + r"\end{itemize}",
                r"\item \textbf{O que o teste não decide:} " + nd_ + r".",
                r"\item \textbf{Origem.} Recalculado neste rito a partir dos bytes embutidos (o código publicado antes da abertura, executado como foi pinado) e conferido contra o resultado da abertura (sha256 \texttt{" + tt_(a_["h_resultado"])
                + r"}); " + str(a_["n_ok"]) + r" de " + str(a_["n_checks"]) + r" checagens. Linha de máquina: \texttt{" + tt_(a_["verdict"]) + r"}.",
                r"\end{enumerate}", r"}}\end{center}\vspace{4pt}"]
    nd_ = "; ".join(_v411_tex_unicode(x_) for x_ in _V411_NAO_DECIDE_EN)
    return [r"\begin{center}\fbox{\parbox{0.93\textwidth}{\small",
            r"\noindent\textbf{The Hubble ratio, H0DN $\times$ BG1: the test opened on 12 Nov 2026} \textsf{[REAL in the numbers $\cdot$ operator INPUT: the verdict head (09/11) and the amendment (11/11)]}\par\smallskip", sel_en_,
            r"\begin{enumerate}\setlength{\itemsep}{1pt}",
            r"\item \textbf{The two lines, together.} The primary, under the published error model: $Z$ against the null $=" + a_["zn"] + r"$ (one-sided $p$ $" + a_["p"] + r"$), $Z$ against $K=" + a_["zk"] + r"$, design $D=" + a_["D"]
            + r"$, branch (" + str(a_["ramo"]) + r"); the test head, exact: \texttt{" + tt_(a_["cab"]) + r"}. Beside it, in the same item, the free Cepheids: $Z$ against the null $=" + a_["zn_cl"] + r"$, $Z$ against $K=" + a_["zk_cl"]
            + r"$, $D=" + a_["D_cl"] + r"$, branch (" + str(a_["ramo_cl"]) + r"), below 5. A retrodiction without fit, with an amendment made after the guard; the test is not blind; proved is validity, not creditation; the gate does not move.",
            r"\item \textbf{The law, in km/s/Mpc.} The BG1 background reads $H_0=" + a_["H0_bg"] + r"$; the law $K=E(z_\star)^{2\beta/3}$, with $\beta=\alpha\sqrt e$ at runtime and no fitted parameter, predicts $" + a_["H0_K"] + r"$ for the local value ($K=" + a_["K"]
            + r"$); the data read $" + a_["H0_pr"] + r"$ in the primary and $" + a_["H0_cl"] + r"$ with free Cepheids; the collaboration publishes $" + a_["H0_pub"] + r"\pm" + a_["sig_pub"] + r"$ for the full network.",
            r"\item \textbf{The acts.} The pre-registration was published in commit \texttt{" + tt_((at_.get("commit_do_pre_registro") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_pre_registro_utc")) + r"); the opening began "
            + _v411_hora(at_.get("inicio_da_abertura_utc")) + r", once; the result was published in commit \texttt{" + tt_((at_.get("commit_do_resultado") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_resultado_utc")) + r").",
            r"\item \textbf{The seven reservations} (section 8 of the pre-registration, read from the embedded text, in Portuguese): \begin{itemize}\setlength{\itemsep}{0pt}" + ress_ + r"\end{itemize}",
            r"\item \textbf{What the test does not decide:} " + nd_ + r".",
            r"\item \textbf{Origin.} Recomputed in this rite from the embedded bytes (the code published before the opening, run as pinned) and checked against the opening result (sha256 \texttt{" + tt_(a_["h_resultado"])
            + r"}); " + str(a_["n_ok"]) + r" of " + str(a_["n_checks"]) + r" checks. Machine line: \texttt{" + tt_(a_["verdict"]) + r"}.",
            r"\end{enumerate}", r"}}\end{center}\vspace{4pt}"]


_V411_NAO_DECIDE_EN = ["the creditation", "the specificity (the Z against the null measures the Hubble tension; what belongs to the law K is the size, the Z against K)", "whether the published error budget is right",
                       "the independence between local and background", "it is not independent evidence from Phases 4, 5 and 9"]


def _v411_remissao_tex(lang_):
    if lang_ == "pt":
        return r"\noindent{\small O quadro acima, “O Teste da Única Palavra” (23/10/2026), fica como registro; o teste da razão de Hubble aberto em 12/11/2026 está no quadro H0DN $\times$ BG1, logo acima dele.}\par\vspace{4pt}"
    return r"\noindent{\small The box above, ``The Test of the Only Word'' (23/10/2026), stays as record; the Hubble-ratio test opened on 12 Nov 2026 is in the H0DN $\times$ BG1 box just above it.}\par\vspace{4pt}"


def _v411_quadro_md(r_, titulo_pt_):
    """O quadro em Markdown (PT), para o topo do .md canonico (antes do quadro da v397) e para o paragrafo pronto do README."""
    a_ = _v411_atomos(r_, "pt", False); at_ = a_["atos"]
    L_ = ["> **" + titulo_pt_ + "**" + ("" if a_["sealed"] else " — **nesta rodada o registro do H0DN v411 NÃO selou: o que segue é o enunciado, não um selo.**"), ">",
          "> - **As duas linhas, juntas.** O primário, sob o modelo de erros publicado: Z contra o nulo = %s (p unilateral %s), Z contra K = %s, D de desenho = %s, ramo (%s); a cabeça do teste, exata: `%s`. Ao lado, no mesmo item, as Cefeidas livres: Z contra o nulo = %s, Z contra K = %s, D = %s, ramo (%s), abaixo de 5. Retrodição sem ajuste, com emenda posterior à guarda; o teste não é cego; provado é validade, não creditação; o gate não se move."
          % (a_["zn"], a_["p"], a_["zk"], a_["D"], a_["ramo"], a_["cab"], a_["zn_cl"], a_["zk_cl"], a_["D_cl"], a_["ramo_cl"]),
          "> - **A lei, em km/s/Mpc.** O fundo BG1 lê H0 = %s; a lei K = E(z*)^(2β/3), com β = α√e em runtime e nenhum parâmetro ajustado, prevê %s para o local (K = %s); o dado lê %s no primário e %s com as Cefeidas livres; a colaboração publica %s ± %s para a rede completa."
          % (a_["H0_bg"], a_["H0_K"], a_["K"], a_["H0_pr"], a_["H0_cl"], a_["H0_pub"], a_["sig_pub"]),
          "> - **Os atos.** Pré-registro no commit `%s` (push %s); abertura em %s, uma única vez; resultado no commit `%s` (push %s)." % ((at_.get("commit_do_pre_registro") or "")[:12], _v411_hora(at_.get("push_do_pre_registro_utc")),
                                                                                                                                  _v411_hora(at_.get("inicio_da_abertura_utc")), (at_.get("commit_do_resultado") or "")[:12], _v411_hora(at_.get("push_do_resultado_utc"))),
          "> - **As sete ressalvas** (seção 8 do pré-registro): " + " ".join("(%d) %s" % (i_ + 1, x_) for i_, x_ in enumerate(a_["ressalvas"])),
          "> - **O que o teste não decide:** " + "; ".join(a_["nao_decide"]) + ".",
          "> - **Origem.** Recalculado neste rito a partir dos bytes embutidos e conferido contra o resultado da abertura (sha256 `%s`); %s de %s checagens. Linha de máquina: `%s`." % (a_["h_resultado"], a_["n_ok"], a_["n_checks"], a_["verdict"]), ""]
    return L_


def _v411_fecho_blocos(a_, lang_):
    """(B-01 da revisao de terceiro) o FECHO dos blocos que trazem o Z do primario (os estresses e o esperado pelos agregados): texto da gerencia, lido do DESENHO (_V411_TEXTOS_DA_GERENCIA); o marcador e' o Z das Cefeidas livres contra o nulo, lido do core no formato do topo."""
    t_ = _V411_TEXTOS_DA_GERENCIA["fecho_blocos"][lang_]
    mk_ = "⟨Z das Cefeidas livres⟩" if lang_ == "pt" else "⟨Z of the free Cepheids⟩"
    if mk_ not in t_:
        raise ValueError("o fecho dos blocos nao traz o marcador do Z das Cefeidas livres: PARAR")
    return " " + _v411_tex_misto(t_.replace(mk_, "$" + a_["zn_cl"] + "$"))


def _v411_rotulo_agregado(chave_, lang_):
    """(B-09) o rotulo da linha do esperado pelos agregados: o da gerencia (lido do DESENHO); chave desconhecida cai no proprio nome."""
    r_ = (_V411_TEXTOS_DA_GERENCIA["rotulos_agregados"][lang_]).get(chave_)
    return _v411_tex_unicode(r_) if r_ else _v411_tt(chave_)


def _v411_errata_e44_tex(lang_):
    """(B-03/B-08) a errata E44 da gerencia c1 (texto lido do DESENHO), como paragrafo no fim da secao nova."""
    return r"\textbf{E44} " + _v411_tex_misto(_V411_TEXTOS_DA_GERENCIA["e44"][lang_])


def _v411_secao_tex(core_, lang_, titulo_):
    """A SECAO da v411 (5.2): montada do core selado e do pre-registro embutido (as ressalvas lidas pelo registro); antes da secao da v410."""
    r_ = core_.get("h0dn_bg1_v411") or {}; a_ = _v411_atomos(r_, lang_); at_ = a_["atos"]; tt_ = _v411_tt; ra_ = a_["regra_antiga"]
    ag_ = a_["agregados"]; N = lambda x_: _v411_n(x_, 2, lang_)
    if lang_ == "pt":
        agt_ = "; ".join(r"%s: esperado $%s$, observado $%s$" % (_v411_rotulo_agregado(x_.get("linha"), "pt"), N(x_.get("z_nulo_esperado")), N(x_.get("z_nulo_observado"))) for x_ in ag_)
        L_ = [r"\section*{" + _v411_tex_unicode(titulo_) + r"}", r"\addcontentsline{toc}{section}{" + _v411_tex_unicode(titulo_) + r"}",
              (r"\textbf{Nesta rodada o registro \texttt{h0dn\_bg1\_v411} NÃO selou: o que segue é o enunciado, não um selo.} " if not a_["sealed"] else "")
              + r"\textbf{A lei e a pergunta.} Nulo: $H_{\rm local}/H_{\rm fundo}=1$ (o $\Lambda$CDM). Alternativa: $K=E(z_\star)^{2\beta/3}$, com $\beta=\alpha\sqrt e$ em runtime e zero parâmetro livre ($K=" + a_["K"] + r"$, $\log_{10}K=" + a_["logK"]
              + r"$, recomputados neste rito). A pergunta: o número local da rede H0DN, lido contra o fundo BG1, cabe na razão 1 ou na razão $K$?",
              r"\textbf{O que a v410 tinha pré-registrado e por que não abriu.} A v410 pré-registrou a função de veredito e não leu dado observado; a ordem do operador era não abrir sem poder discriminante, e o vetor publicado não cabia no suporte da covariância publicada. "
              r"Com os mesmos números lidos agora, a função congelada da v410 (a do \texttt{um.py}) devolve o ramo (" + str(ra_[2]) + r"): \texttt{" + tt_(ra_[0]) + r"} --- o desfecho que a regra antiga daria, dito às claras.",
              r"\textbf{O achado do suporte e a emenda.} A tabela de erros publicada declara variância zero em 72 direções, que tocam 111 linhas (37 hospedeiras nas três âncoras); a colaboração resolve por pseudoinversa, e os pesos congelados em 06/11 são os dela e dão peso zero a essa componente. "
              r"Em 11/11 o operador emendou a regra (D162): o ramo (1) deixou de recusar o vetor fora do suporte e passou a ser o portão 1 (a reprodução do número local publicado e a impressão digital). O literal novo só difere do antigo pela marca da emenda, e os ramos 2 a 6 são os mesmos (conferido neste rito). "
              r"É emenda posterior à guarda, e o teste não é cego.",
              r"\textbf{O desenho ratificado (D159).} O primário é o modelo de erros publicado, com os 13 calibradores extras fora ($D$ de desenho $=" + a_["D"] + r"$); a linha das Cefeidas livres vai ao lado, sempre ($D=" + a_["D_cl"]
              + r"$); o portão é de 90\,\% de poder de desenho no modelo publicado, com as linhas de estresse ao lado.",
              r"\textbf{A publicação antes da abertura.} O pré-registro foi publicado no commit \texttt{" + tt_((at_.get("commit_do_pre_registro") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_pre_registro_utc")) + r"); a abertura começou "
              + _v411_hora(at_.get("inicio_da_abertura_utc")) + r", uma única vez; o resultado foi publicado no commit \texttt{" + tt_((at_.get("commit_do_resultado") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_resultado_utc")) + r").",
              r"\textbf{O resultado (as duas linhas juntas).} No primário, sob o modelo de erros publicado, $Z$ contra o nulo $=" + a_["zn"] + r"$ ($p$ unilateral $" + a_["p"] + r"$) e $Z$ contra $K=" + a_["zk"] + r"$, ramo (" + str(a_["ramo"])
              + r"); ao lado, no mesmo item, com as Cefeidas livres, $Z$ contra o nulo $=" + a_["zn_cl"] + r"$ e $Z$ contra $K=" + a_["zk_cl"] + r"$, ramo (" + str(a_["ramo_cl"]) + r"), abaixo de 5. Em km/s/Mpc: o fundo $" + a_["H0_bg"] + r"$, a previsão da lei $" + a_["H0_K"]
              + r"$, o lido $" + a_["H0_pr"] + r"$ e $" + a_["H0_cl"] + r"$. Retrodição sem ajuste; o teste não é cego; provado é validade, não creditação; o gate não se move.",
              r"\textbf{Os estresses (não mudam o veredito).} (i) Ruído por linha nas 111 linhas, com $\tau$ estimado do próprio vetor ($\hat\tau=" + a_["tau"] + r"$ mag, pós-observação): $Z$ contra o nulo $" + a_["zn_tau"] + r"$ e $" + a_["zn_tau_cl"]
              + r"$. (ii) Âncora única: N4258 $" + a_["anc"]["N4258"] + r"$, LMC $" + a_["anc"]["LMC"] + r"$, MW $" + a_["anc"]["MW"] + r"$. (iii) Viés das Cefeidas variando por hospedeira, $B=0{,}02$ mag: $Z$ entre $" + a_["b"]["b_0.02"][0] + r"$ e $" + a_["b"]["b_0.02"][1]
              + r"$; $B=0{,}05$ mag: entre $" + a_["b"]["b_0.05"][0] + r"$ e $" + a_["b"]["b_0.05"][1] + r"$." + _v411_fecho_blocos(a_, "pt"),
              r"\textbf{O esperado pelos agregados, ao lado do observado ($Z$ contra o nulo).} " + agt_ + r". É relato, não portão: o rito conferiu a conta." + _v411_fecho_blocos(a_, "pt"),
              r"\textbf{O que o teste não decide.} " + "; ".join(_v411_tex_unicode(x_) for x_ in a_["nao_decide"]) + r".",
              r"\textbf{As sete ressalvas.} " + " ".join(r"(%d) %s" % (i_ + 1, _v411_tex_unicode(x_)) for i_, x_ in enumerate(a_["ressalvas"])),
              r"\textbf{As tentativas anteriores.} A lei $K$ já foi confrontada com a razão de Hubble neste programa (Fase 4, Fase 5 e Fase 9 V2); os dados locais deste teste se sobrepõem aos daquelas, e ele não é evidência independente delas; as tentativas ficam contadas no Mapa de Rotas.",
              _v411_errata_e44_tex("pt")]
        return L_
    agt_ = "; ".join(r"%s: expected $%s$, observed $%s$" % (_v411_rotulo_agregado(x_.get("linha"), "en"), N(x_.get("z_nulo_esperado")), N(x_.get("z_nulo_observado"))) for x_ in ag_)
    return [r"\section*{" + _v411_tex_unicode(titulo_) + r"}", r"\addcontentsline{toc}{section}{" + _v411_tex_unicode(titulo_) + r"}",
            (r"\textbf{This round the record \texttt{h0dn\_bg1\_v411} did NOT seal: what follows is the statement, not a seal.} " if not a_["sealed"] else "")
            + r"\textbf{The law and the question.} Null: $H_{\rm local}/H_{\rm background}=1$ ($\Lambda$CDM). Alternative: $K=E(z_\star)^{2\beta/3}$, with $\beta=\alpha\sqrt e$ at runtime and zero free parameters ($K=" + a_["K"] + r"$, $\log_{10}K=" + a_["logK"]
            + r"$, recomputed in this rite). The question: does the local number of the H0DN network, read against the BG1 background, fit ratio 1 or ratio $K$?",
            r"\textbf{What v410 had pre-registered and why it did not open.} v410 pre-registered the verdict function and read no observed data; the operator's order was not to open without discriminating power, and the published vector did not fit the support of the published covariance. "
            r"With the same numbers read now, the frozen v410 function (the one in \texttt{um.py}) returns branch (" + str(ra_[2]) + r"): \texttt{" + tt_(ra_[0]) + r"} --- the outcome the old rule would give, stated openly.",
            r"\textbf{The support finding and the amendment.} The published error table declares zero variance in 72 directions, touching 111 rows (37 hosts in the three anchors); the collaboration resolves it by pseudo-inverse, and the weights frozen on 6 Nov are its (the collaboration's) and give zero weight to that component. "
            r"On 11 Nov the operator amended the rule (D162): branch (1) no longer refuses the vector outside the support and became gate 1 (the reproduction of the published local number and the fingerprint). The new literal differs from the old only by the amendment mark, and branches 2 to 6 are the same (checked in this rite). "
            r"It is an amendment made after the guard, and the test is not blind.",
            r"\textbf{The ratified design (D159).} The primary is the published error model, with the 13 extra calibrators out (design $D=" + a_["D"] + r"$); the free-Cepheid line goes beside it, always ($D=" + a_["D_cl"]
            + r"$); the gate is 90\,\% design power in the published model, with the stress lines beside.",
            r"\textbf{Publication before the opening.} The pre-registration was published in commit \texttt{" + tt_((at_.get("commit_do_pre_registro") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_pre_registro_utc")) + r"); the opening began "
            + _v411_hora(at_.get("inicio_da_abertura_utc")) + r", once; the result was published in commit \texttt{" + tt_((at_.get("commit_do_resultado") or "")[:12]) + r"} (push " + _v411_hora(at_.get("push_do_resultado_utc")) + r").",
            r"\textbf{The result (the two lines together).} In the primary, under the published error model, $Z$ against the null $=" + a_["zn"] + r"$ (one-sided $p$ $" + a_["p"] + r"$) and $Z$ against $K=" + a_["zk"] + r"$, branch (" + str(a_["ramo"])
            + r"); beside it, in the same item, with free Cepheids, $Z$ against the null $=" + a_["zn_cl"] + r"$ and $Z$ against $K=" + a_["zk_cl"] + r"$, branch (" + str(a_["ramo_cl"]) + r"), below 5. In km/s/Mpc: the background $" + a_["H0_bg"] + r"$, the law's prediction $" + a_["H0_K"]
            + r"$, the reading $" + a_["H0_pr"] + r"$ and $" + a_["H0_cl"] + r"$. A retrodiction without fit; the test is not blind; proved is validity, not creditation; the gate does not move.",
            r"\textbf{The stresses (they do not change the verdict).} (i) Row noise in the 111 rows, with $\tau$ estimated from the vector itself ($\hat\tau=" + a_["tau"] + r"$ mag, post-observation): $Z$ against the null $" + a_["zn_tau"] + r"$ and $" + a_["zn_tau_cl"]
            + r"$. (ii) Single anchor: N4258 $" + a_["anc"]["N4258"] + r"$, LMC $" + a_["anc"]["LMC"] + r"$, MW $" + a_["anc"]["MW"] + r"$. (iii) Cepheid bias varying by host, $B=0.02$ mag: $Z$ between $" + a_["b"]["b_0.02"][0] + r"$ and $" + a_["b"]["b_0.02"][1]
            + r"$; $B=0.05$ mag: between $" + a_["b"]["b_0.05"][0] + r"$ and $" + a_["b"]["b_0.05"][1] + r"$." + _v411_fecho_blocos(a_, "en"),
            r"\textbf{What the public aggregates predict, beside the observed ($Z$ against the null).} " + agt_ + r". It is a report, not a gate: the rite checked the arithmetic." + _v411_fecho_blocos(a_, "en"),
            r"\textbf{What the test does not decide.} " + "; ".join(_v411_tex_unicode(x_) for x_ in _V411_NAO_DECIDE_EN) + r".",
            r"\textbf{The seven reservations} (section 8 of the pre-registration, in Portuguese). " + " ".join(r"(%d) %s" % (i_ + 1, _v411_tex_unicode(x_)) for i_, x_ in enumerate(a_["ressalvas"])),
            r"\textbf{The earlier attempts.} The law $K$ has already been confronted with the Hubble ratio in this programme (Phase 4, Phase 5 and Phase 9 V2); the local data of this test overlap with theirs, and it is not independent evidence from them; the attempts are counted in the Route Map.",
            _v411_errata_e44_tex("en")]


def _v411_linha_md(r_):
    """A linha do .md canonico (antes das linhas da v410): as duas linhas juntas, com as quatro obrigacoes; numeros do core."""
    a_ = _v411_atomos(r_, "pt", False)
    if not a_["sealed"]:
        return "o registro `h0dn_bg1_v411` NÃO selou nesta rodada: o que segue é o enunciado, não um selo; o teste H0DN × BG1 foi aberto uma vez em 12/11/2026, depois do commit público do pré-registro; o gate não se move."
    return ("o teste pré-registrado da razão de Hubble local/fundo (rede H0DN contra o fundo BG1) foi aberto uma vez em 12/11/2026, depois do commit público do pré-registro, e o resultado é RECALCULADO neste rito dos bytes embutidos: "
            "sob o modelo de erros publicado, o primário fica a %s contra o nulo e %s contra K (ramo %s); ao lado, no mesmo item, as Cefeidas livres leem %s (ramo %s), abaixo de 5; retrodição sem ajuste, com emenda posterior à guarda; "
            "o teste não é cego; provado é validade, não creditação; as sete ressalvas vão no quadro do topo; o gate não se move. **E44** " % (a_["zn"], a_["zk"], a_["ramo"], a_["zn_cl"], a_["ramo_cl"]) + _V411_TEXTOS_DA_GERENCIA["e44"]["pt"])


_V411_MARCADORES = {"pt": {"⟨Z contra K⟩": ("primario", "z_tgl"), "⟨Z contra o nulo⟩": ("primario", "z_null"), "⟨Z das Cefeidas livres⟩": ("cefeidas_livres", "z_null"), "⟨n⟩": ("primario", "n")},
                    "en": {"⟨Z against K⟩": ("primario", "z_tgl"), "⟨Z against the null⟩": ("primario", "z_null"), "⟨Z of the free Cepheids⟩": ("cefeidas_livres", "z_null"), "⟨n⟩": ("primario", "n")}}


def _v411_tex_misto(s_):
    """converte unicode para LaTeX dentro e fora do modo matematico (o texto ratificado traz $...$ com beta, alfa e raiz; fora do modo vira $\beta$ etc.)."""
    fora_ = {"β": r"$\beta$", "α": r"$\alpha$", "σ": r"$\sigma$", "Λ": r"$\Lambda$", "δ": r"$\delta$", "√": r"$\surd$", "×": r"$\times$", "−": r"$-$", "%": r"\%", "_": r"\_"}   # (v411: o Λ do ΛCDM e o sublinhado de veredito de maquina no modo texto, achados do ensaio a seco)
    dentro_ = {"β": r"\beta ", "α": r"\alpha ", "σ": r"\sigma ", "Λ": r"\Lambda ", "δ": r"\delta ", "√e": r"\sqrt e", "√": r"\sqrt ", "×": r"\times ", "−": "-"}
    out_, mat_ = [], False
    i_ = 0
    while i_ < len(s_):
        ch_ = s_[i_]
        if ch_ == "$":
            mat_ = not mat_; out_.append(ch_); i_ += 1; continue
        tab_ = dentro_ if mat_ else fora_
        if mat_ and s_[i_:i_ + 2] == "√e":
            out_.append(dentro_["√e"]); i_ += 2; continue
        out_.append(tab_.get(ch_, ch_)); i_ += 1
    return "".join(out_)


def _v411_topo_texto(core_, lang_, tex_=True):
    """O texto RATIFICADO do topo (TOPO_RATIFICADO_v411.json, a fonte unica; D172, D173), com os marcadores preenchidos na EMISSAO a partir da chave do core que a tabela `marcadores` do arquivo da' (doze: o H0DN, o livro de
    cobrancas e a Fase 9 V2). Marcador com fonte AUSENTE no core => o topo nao diz o resultado e diz por que (visivel; fork C, 12/11); numero nao finito ou nao numerico, ou marcador que sobre no texto = PARAR (ValueError). O acrescimo e' fail-closed: a frase de que nenhuma cobranca foi falsificada so' sai se as
    falsificadas forem zero no core do rito e a soma das categorias mais as falsificadas for o numero de cobrancas; o H0DN nao entra no livro. Se o registro nao selou, devolve a frase de que nao selou."""
    import math as _m
    r_ = core_.get("h0dn_bg1_v411") or {}
    if r_.get("all_verified") is not True:
        return (r"\textbf{O registro do teste H0DN $\times$ BG1 (v411) NÃO selou nesta rodada: o resultado não é dito aqui.} " if lang_ == "pt" else r"\textbf{The H0DN $\times$ BG1 test record (v411) did NOT seal this round: the result is not stated here.} ") if tex_ else ""
    t_ = str(_V411_TOPO[lang_])
    tab_ = _V411_TOPO.get("marcadores") or {}
    if not tab_:
        raise ValueError("a tabela de marcadores do topo ratificado nao esta' embutida: PARAR")
    lv_ = _V411_TOPO.get("livro") or {}
    pr2_ = core_
    for k_ in lv_.get("caminho") or ["?"]:
        pr2_ = pr2_.get(k_) if isinstance(pr2_, dict) else None
    if any(f_ in t_ for f_ in lv_.get("frases_" + lang_) or []):   # (fail-closed do acrescimo: D173)
        led_ = (pr2_ or {}).get("ledger") if isinstance(pr2_, dict) else None
        if not isinstance(led_, dict) or not isinstance((pr2_ or {}).get("n_cobrancas"), int) or (pr2_ or {}).get("falsificadas") != 0 or led_.get("FALSIFIED", 0) != 0 \
                or sum(int(led_.get(c_) or 0) for c_ in lv_["categorias"]) + int(led_.get("FALSIFIED") or 0) != int(pr2_["n_cobrancas"]):
            raise ValueError("o livro de cobrancas do rito nao sustenta a frase de que nenhuma foi falsificada (falsificadas != 0 ou a soma das categorias != as cobrancas): PARAR")
    for mk_pt_, d_ in tab_.items():
        mk_ = mk_pt_ if lang_ == "pt" else d_["en"]
        if mk_ not in t_:
            continue
        x_ = core_
        for k_ in d_["caminho"]:
            x_ = x_.get(k_) if isinstance(x_, dict) else None
        if x_ is None:   # (fonte AUSENTE: um registro nao gravou nesta rodada) o topo NAO diz o resultado e diz por que, visivel, sem derrubar o artigo (o padrao de quando o registro do H0DN nao sela)
            return ((r"\textbf{O texto do topo não é dito nesta rodada: a fonte de um marcador (\texttt{%s}) não está no core.} " if lang_ == "pt" else r"\textbf{The top text is not stated this round: the source of a marker (\texttt{%s}) is not in the core.} ")
                    % _v411_tt(".".join(d_["caminho"]))) if tex_ else ""
        if isinstance(x_, bool) or not isinstance(x_, (int, float)) or x_ != x_ or x_ in (float("inf"), float("-inf")):   # (valor PRESENTE mas nao numerico ou nao finito: PARAR)
            raise ValueError("marcador do topo sem fonte resolvida no core (%s <- %s): PARAR" % (mk_, ".".join(d_["caminho"])))
        if d_["inteiro_de"]:
            rep_ = str(int(_m.floor(float(x_))))
        elif d_["inteiro"]:
            if float(x_) != int(x_):
                raise ValueError("marcador inteiro com valor nao inteiro (%s): PARAR" % mk_)
            rep_ = str(int(x_))
        else:
            rep_ = "%.*f" % (int(d_["casas"]), float(x_))
            if d_["com_sinal"] and float(x_) > 0:
                rep_ = "+" + rep_
            rep_ = (rep_.replace(".", ",") if lang_ == "pt" else rep_).replace("-", "−")
        t_ = t_.replace(mk_, rep_)
    if "⟨" in t_ or "⟩" in t_:
        raise ValueError("marcador do topo nao preenchido (sobrou no texto): PARAR")
    return (_v411_tex_misto(t_) + " ") if tex_ else t_


def _v411_efeitos_tex(core_, lang_, onde_="apresentacao"):
    """A troca da frase sobre os efeitos de beta (DESENHO 5.1 b): so' se o registro selou; senao fica a frase antiga, dita."""
    r_ = core_.get("h0dn_bg1_v411") or {}
    if r_.get("all_verified") is not True:
        return (r"a probabilidade de os efeitos $\beta$ existirem na natureza segue indeterminada (o registro do H0DN v411 não selou nesta rodada)" if lang_ == "pt" else r"the probability that the $\beta$ effects exist in nature remains undetermined (the v411 H0DN record did not seal this round)")
    if onde_ == "metodo":   # (aditivo da gerencia c1, 12/11) no paragrafo “O metodo” a frase leva as quatro obrigacoes da F67 no mesmo bloco
        z_ = _v411_n(((r_.get("values") or {}).get("cefeidas_livres") or {}).get("z_null"), 2, lang_)
        if lang_ == "pt":
            return (r"os efeitos de $\beta$ na natureza foram lidos acima de $5\sigma$ num canal, a razão de Hubble, sob o modelo de erros publicado (ao lado, no mesmo item, as Cefeidas livres dão $" + z_ + r"\sigma$, abaixo de 5; "
                    r"retrodição sem ajuste, com emenda posterior à guarda, teste não cego; provado é validade, não creditação); nos demais canais nenhum discrimina a RG à sensibilidade disponível")
        return (r"the effects of $\beta$ in nature were read above $5\sigma$ in one channel, the Hubble ratio, under the published error model (beside it, in the same item, the free Cepheids give $" + z_ + r"\sigma$, below 5; "
                r"a retrodiction without fit, with an amendment made after the guard, the test not blind; proved is validity, not creditation); in the other channels none discriminates GR at the available sensitivity")
    if lang_ == "pt":
        return r"os efeitos de $\beta$ na natureza foram lidos acima de $5\sigma$ num canal, a razão de Hubble, sob o modelo de erros publicado; nos demais canais nenhum discrimina a RG à sensibilidade disponível"
    return r"the effects of $\beta$ in nature were read above $5\sigma$ in one channel, the Hubble ratio, under the published error model; in the other channels none discriminates GR at the available sensitivity"


def _v411_p2_ao_lado_tex(core_, lang_):
    """(aditivo da gerencia c1, 12/11) a frase AO LADO do P2 na secao dos tres testes de estresse (v387): o texto selado da v387 fica (P2 nao determinada, registro); a leitura nova do P2 vai ao lado, com as quatro
    obrigacoes da F67 no mesmo bloco e o rotulo do campo novo do registro (p2_ao_lado_da_v387). So' se o registro selou; senao, dito."""
    r_ = core_.get("h0dn_bg1_v411") or {}; p2_ = r_.get("p2_ao_lado_da_v387") or {}
    if r_.get("all_verified") is not True or not p2_:
        return (r"\textbf{(v411, ao lado)} O registro do teste H0DN $\times$ BG1 não selou nesta rodada: o P2 segue como o registro selado da v387 o diz." if lang_ == "pt"
                else r"\textbf{(v411, beside)} The H0DN $\times$ BG1 test record did not seal this round: P2 stays as the sealed v387 record says.")
    z_ = _v411_n(((r_.get("values") or {}).get("cefeidas_livres") or {}).get("z_null"), 2, lang_)
    if lang_ == "pt":
        return (r"\textbf{(v411, ao lado do $P_2$)} Os efeitos de $\beta$ na natureza foram lidos acima de $5\sigma$ num canal, a razão de Hubble (H0DN $\times$ BG1), sob o modelo de erros publicado; ao lado, no mesmo item, "
                r"as Cefeidas livres dão $" + z_ + r"\sigma$, abaixo de 5; é retrodição sem ajuste, com emenda posterior à guarda, e o teste não é cego; provado é validade, não creditação; nos demais canais nenhum discrimina a RG "
                r"à sensibilidade disponível. O rótulo selado da v387 (\texttt{" + _v411_tt(p2_.get("rotulo_selado_da_v387")) + r"}) fica como registro; esta leitura vai ao lado (\texttt{" + _v411_tt(p2_.get("rotulo")) + r"}"
                + (r", rótulo provisório, em proposta" if p2_.get("rotulo_e_proposta") else "") + r").")
    return (r"\textbf{(v411, beside $P_2$)} The effects of $\beta$ in nature were read above $5\sigma$ in one channel, the Hubble ratio (H0DN $\times$ BG1), under the published error model; beside it, in the same item, "
            r"the free Cepheids give $" + z_ + r"\sigma$, below 5; it is a retrodiction without fit, with an amendment made after the guard, and the test is not blind; proved is validity, not creditation; in the other channels none "
            r"discriminates GR at the available sensitivity. The sealed v387 label (\texttt{" + _v411_tt(p2_.get("rotulo_selado_da_v387")) + r"}) stays as record; this reading goes beside it (\texttt{" + _v411_tt(p2_.get("rotulo")) + r"}"
            + (r", provisional label, under proposal" if p2_.get("rotulo_e_proposta") else "") + r").")


def _v411_estatuto_tex(core_, lang_):
    """A frase AO LADO do “estatuto da prova (v391)” e do item do “coracao” (DESENHO 5.1 c), so' se o registro selou."""
    r_ = core_.get("h0dn_bg1_v411") or {}
    if r_.get("all_verified") is not True:
        return r"\textbf{(v411, ao lado)} O registro do teste H0DN $\times$ BG1 não selou nesta rodada." if lang_ == "pt" else r"\textbf{(v411, beside)} The H0DN $\times$ BG1 test record did not seal this round."
    if lang_ == "pt":
        return r"\textbf{(v411, ao lado)} " + _v411_tex_misto(_V411_ESTATUTO_AO_LADO_PT) + " " + _v411_tex_misto(_V411_TEXTOS_DA_GERENCIA["fecho_estatuto"]["pt"])   # (B-04) o fecho da gerencia
    return (r"\textbf{(v411, beside)} The link that was waiting for an instrument, $\beta_{TGL}$ in nature at $5\sigma$, was read on 12 Nov 2026 in the H0DN $\times$ BG1 test: closed at this sensitivity, under the published error model "
            r"(the free Cepheids stay below 5; more sensitive data may revise). What the programme keeps refusing is the creditation, which belongs to whoever observes from outside. " + _v411_tex_misto(_V411_TEXTOS_DA_GERENCIA["fecho_estatuto"]["en"]))   # (B-04) o fecho da gerencia
