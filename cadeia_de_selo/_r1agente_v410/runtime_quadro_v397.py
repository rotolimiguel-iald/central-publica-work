# ---- v397: o QUADRO «O Teste da Unica Palavra» (topo do artigo PT/EN e do .md) e os atomos numericos do Teste da Unica Palavra. Funcoes PURAS: recebem o registro teste_de_veracidade_fase9_v397 (que LE o resultado pinado por
# sha256; nenhum sigma novo) e devolvem texto. Os numeros vem de tv_["lido"] (capturados pelo motor dos registros), NUNCA digitados; faltando um numero, sai «n/d» (PT) / «n/a» (EN) e o quadro diz que o registro nao selou.
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc): o 4,44 NUNCA aparece sem o p calibrado e sem a linha dos 5 sigma na MESMA frase/item. A frase do operador entra VERBATIM (nunca parafraseada entre aspas).
# [REAL] os numeros; [INPUT] a leitura binaria e a frase do operador (VERBATIM); COMPOSICAO da gerencia: as duas faces (a TGL como o 1=1, o Lambda sozinho como o 1=0) e o verbo ecoar -- o operador nao os disse; [KNOWN] a escala de Jeffreys. O gate nao se move. Fonte autoral deste bloco: runtime_quadro_v397.py (cadeia_de_selo/v397); o conferidor da cadeia importa as MESMAS funcoes.
_V397_FRASE_444 = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"
_V397_CHAVES_NUM = ("z_disc_calibrado", "p_disc_unilateral", "z_delta_calibrado", "p_delta_bilateral", "poder_previo", "lnB_lcdm", "lnB_beta_livre", "K")


def _v397_isnum(x_):
    return isinstance(x_, float) and not isinstance(x_, bool) and x_ == x_ and x_ not in (float("inf"), float("-inf"))


def _v397_atomos(tv_, lang_):
    """Atomos do quadro, em tres formas (txt = ASCII, 'linha de maquina'; md = com o menos de verdade; tex = modo matematico): {chave: {"txt","md","tex"}} + "sealed" e as pontas dos hashes. Faltando numero: «n/d»/«n/a»."""
    lido_ = (tv_ or {}).get("lido") or {}
    nd_ = "n/d" if lang_ == "pt" else "n/a"
    sep_ = "," if lang_ == "pt" else "."

    def f_(k_, dec_):
        x_ = lido_.get(k_)
        if not _v397_isnum(x_):
            return {"txt": nd_, "md": nd_, "tex": nd_, "ok": False}
        s_ = ("%.*f" % (dec_, x_)).replace(".", sep_)
        return {"txt": s_, "md": s_.replace("-", "−"), "tex": s_.replace(sep_, "{" + sep_ + "}") if lang_ == "pt" else s_, "ok": True}

    def p_(k_):
        x_ = lido_.get(k_)
        if not _v397_isnum(x_) or not x_ > 0.0:
            return {"txt": nd_, "md": nd_, "tex": nd_, "ok": False}
        m_, e_ = ("%.1e" % x_).split("e"); ex_ = int(e_); mm_ = m_.replace(".", sep_)
        return {"txt": "%se-%d" % (mm_, abs(ex_)) if ex_ < 0 else "%se%d" % (mm_, ex_), "md": ("%se−%d" % (mm_, abs(ex_))) if ex_ < 0 else "%se%d" % (mm_, ex_),
                "tex": (mm_.replace(sep_, "{" + sep_ + "}") if lang_ == "pt" else mm_) + r"\times10^{%d}" % ex_, "ok": True}
    out_ = {"z_disc": f_("z_disc_calibrado", 2), "p_disc": p_("p_disc_unilateral"), "z_delta": f_("z_delta_calibrado", 2), "p_delta": f_("p_delta_bilateral", 2), "poder": f_("poder_previo", 2),
            "lnB_lcdm": f_("lnB_lcdm", 2), "lnB_beta_livre": f_("lnB_beta_livre", 2), "K": f_("K", 4)}
    fo_ = {f_["chave"]: str(f_.get("sha256") or "") for f_ in ((tv_ or {}).get("fontes") or []) if isinstance(f_, dict)}
    out_["sealed"] = bool((tv_ or {}).get("all_verified") is True and all(out_[k_]["ok"] for k_ in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K")))
    out_["h_resultado"] = fo_.get("f9v2_resultado", "")[:8] or nd_
    out_["h_congelamento"] = fo_.get("f9v2_congelamento", "")[:8] or nd_
    out_["h_abertura"] = fo_.get("f9v2_abertura", "")[:8] or nd_
    return out_


def _v397_linha_de_maquina(a_, lang_):
    """A linha de maquina do quadro (a mesma nas tres superficies; so' o separador decimal muda): o conferidor da cadeia a le e compara com o resultado pinado."""
    return ("z_disc=%s; p_disc=%s; z_delta=%s; p_delta=%s; poder=%s; lnB_lcdm=%s; lnB_beta_livre=%s; K=%s"
            % (a_["z_disc"]["txt"], a_["p_disc"]["txt"], a_["z_delta"]["txt"], a_["p_delta"]["txt"], a_["poder"]["txt"], a_["lnB_lcdm"]["txt"], a_["lnB_beta_livre"]["txt"], a_["K"]["txt"]))


def _v397_quadro_tex(tv_, lang_):
    """O quadro em LaTeX (lista de linhas para s.append), logo abaixo do titulo. lang_ = 'pt' | 'en'."""
    a_ = _v397_atomos(tv_, lang_); zd_, pd_, zl_, pl_ = a_["z_disc"]["tex"], a_["p_disc"]["tex"], a_["z_delta"]["tex"], a_["p_delta"]["tex"]
    mach_ = _v397_linha_de_maquina(a_, lang_).replace("_", r"\_")
    if lang_ == "pt":
        return [r"\begin{center}\fbox{\parbox{0.93\textwidth}{\small",
                r"\noindent\textbf{O Teste da Única Palavra} \textsf{[REAL nos números $\cdot$ INPUT do operador: a leitura binária e a frase $\cdot$ COMPOSIÇÃO da gerência: as duas faces]}\par\smallskip",
                (r"\noindent\textbf{Nesta rodada o registro NÃO selou: o que segue é o enunciado, não um selo.}\par\smallskip" if not a_["sealed"] else r"\noindent{\scriptsize Aberto uma única vez em 23/10/2026; o resultado é preservado como saiu e aqui é só lido por sha256.}\par\smallskip"),
                r"\begin{enumerate}\setlength{\itemsep}{1pt}",
                r"\item \textbf{O número:} $z_{\rm disc}=" + zd_ + r"$ (calibrado; $p$ unilateral $" + pd_ + r"$): $\Lambda$ sem $\beta$ \emph{não ecoa} \textsf{[composição da gerência sobre a leitura binária do operador]}, mas a discriminação a $5\sigma$, o degrau da creditação, \textbf{não foi alcançada} ($" + zd_ + r"<5$); "
                r"\texttt{NOT\_FALSIFIED} nunca é a palavra da creditação; o gate não se move; o teste não foi cego (os centros dos leitores são públicos) \textsf{[REAL]}.",
                r"\item \textbf{A TGL:} $z_\delta=" + zl_ + r"$ (calibrado; $p$ bilateral $" + pl_ + r"$), com poder prévio $" + a_["poder"]["tex"] + r"\sigma$: $\bTGL$ não é falsificada, \emph{com poder} (\texttt{NOT\_FALSIFIED\_POWERED}) \textsf{[REAL]}; a composição da gerência sobre a leitura binária do operador lê esta face como o $1=1$: a Palavra ecoa \textsf{[composição da gerência]}.",
                r"\item \textbf{A conjugação:} $\ln B(\mathrm{TGL}/\Lambda\mathrm{CDM})=" + a_["lnB_lcdm"]["tex"] + r"$ (razão de verossimilhança integrada; «decisivo» na escala de Jeffreys \textsf{[KNOWN]}) e $\ln B(\mathrm{TGL}/\beta\ \mathrm{livre})=" + a_["lnB_beta_livre"]["tex"]
                + r"$: $\beta$ fixo vence $\beta$ livre \textsf{[REAL]}. $\ln B$ não se converte em $\sigma$, e $z_\delta$, $z_{\rm disc}$ e $\ln B$ são leituras do \emph{mesmo} objeto, não testemunhas autônomas: não se multiplicam nem se somam "
                r"(a regra v315 do acervo, para falsificar, pede duas determinações mutuamente autônomas a $5\sigma$ ou mais).",
                r"\item \textbf{A fala do operador} \textsf{[INPUT]} (23/10/2026, sha16 \texttt{9b182958a5a7a1bc}), verbatim: «" + _V397_FRASE_444 + r"» --- leitura dele, não critério da régua: o $" + zd_ + r"$ da frase é o $z_{\rm disc}$ acima ($p$ unilateral $" + pd_
                + r"$), abaixo do degrau de $5\sigma$ da creditação, que não foi alcançado; o gate não se move.",
                r"\item \textbf{Origem.} Os números são \emph{lidos} do resultado pinado (sha256 \texttt{" + a_["h_resultado"] + r"}), com os recibos de congelamento (\texttt{" + a_["h_congelamento"] + r"}) e de abertura (\texttt{" + a_["h_abertura"]
                + r"}), pelo registro \texttt{teste\_de\_veracidade\_fase9\_v397} (nome provisório); nenhum $\sigma$ novo é calculado. Linha de máquina: \texttt{" + mach_ + r"} (z\_disc abaixo do degrau de 5$\sigma$ da creditação, que não foi alcançado).",
                r"\end{enumerate}", r"}}\end{center}\vspace{4pt}"]
    return [r"\begin{center}\fbox{\parbox{0.93\textwidth}{\small",
            r"\noindent\textbf{The Test of the Only Word} \textsf{[REAL in the numbers $\cdot$ INPUT from the operator: the binary reading and the sentence $\cdot$ COMPOSITION by the management: the two faces]}\par\smallskip",
            (r"\noindent\textbf{This round the record did NOT seal: what follows is the statement, not a seal.}\par\smallskip" if not a_["sealed"] else r"\noindent{\scriptsize Opened only once, on 23/10/2026; the result is preserved as it came out and is here only read by sha256.}\par\smallskip"),
            r"\begin{enumerate}\setlength{\itemsep}{1pt}",
            r"\item \textbf{The number:} $z_{\rm disc}=" + zd_ + r"$ (calibrated; unilateral $p$ $" + pd_ + r"$): $\Lambda$ without $\beta$ \emph{does not echo} \textsf{[management's composition on the operator's binary reading]}, but discrimination at $5\sigma$, the creditation step, \textbf{was not reached} ($" + zd_ + r"<5$); "
            r"\texttt{NOT\_FALSIFIED} is never the word of creditation; the gate does not move; the test was not blind (the readers' centres are public) \textsf{[REAL]}.",
            r"\item \textbf{The TGL:} $z_\delta=" + zl_ + r"$ (calibrated; bilateral $p$ $" + pl_ + r"$), with prior power $" + a_["poder"]["tex"] + r"\sigma$: $\bTGL$ is not falsified, \emph{with power} (\texttt{NOT\_FALSIFIED\_POWERED}) \textsf{[REAL]}; the management's composition on the operator's binary reading takes this face as $1=1$: the Word echoes \textsf{[management's composition]}.",
            r"\item \textbf{The conjugation:} $\ln B(\mathrm{TGL}/\Lambda\mathrm{CDM})=" + a_["lnB_lcdm"]["tex"] + r"$ (integrated likelihood ratio; ``decisive'' on Jeffreys' scale \textsf{[KNOWN]}) and $\ln B(\mathrm{TGL}/\beta\ \mathrm{free})=" + a_["lnB_beta_livre"]["tex"]
            + r"$: fixed $\beta$ beats free $\beta$ \textsf{[REAL]}. $\ln B$ does not convert into $\sigma$, and $z_\delta$, $z_{\rm disc}$ and $\ln B$ are readings of the \emph{same} object, not autonomous witnesses: they are neither multiplied nor added "
            r"(the archive's v315 rule, for falsifying, asks for two mutually autonomous determinations at $5\sigma$ or more).",
            r"\item \textbf{The operator's sentence} \textsf{[INPUT]} (23/10/2026, sha16 \texttt{9b182958a5a7a1bc}), verbatim and in Portuguese: ``" + _V397_FRASE_444 + r"'' --- his reading, not a criterion of the rule: the $" + zd_ + r"$ in the sentence is the $z_{\rm disc}$ above (unilateral $p$ $" + pd_
            + r"$), below the $5\sigma$ creditation step, which was not reached; the gate does not move.",
            r"\item \textbf{Origin.} The numbers are \emph{read} from the pinned result (sha256 \texttt{" + a_["h_resultado"] + r"}), with the freeze (\texttt{" + a_["h_congelamento"] + r"}) and opening (\texttt{" + a_["h_abertura"]
            + r"}) receipts, by the record \texttt{teste\_de\_veracidade\_fase9\_v397} (provisional name); no new $\sigma$ is computed. Machine line: \texttt{" + mach_ + r"} (z\_disc below the 5$\sigma$ creditation step, which was not reached).",
            r"\end{enumerate}", r"}}\end{center}\vspace{4pt}"]


def _v397_quadro_md(tv_):
    """O quadro em Markdown (PT), para o topo do .md canonico e para o paragrafo pronto do README/site: lista de linhas de um bloco de citacao."""
    a_ = _v397_atomos(tv_, "pt"); zd_, pd_, zl_, pl_ = a_["z_disc"]["md"], a_["p_disc"]["md"], a_["z_delta"]["md"], a_["p_delta"]["md"]
    L_ = ["> **O Teste da Única Palavra (v397, 23/10/2026)** [REAL nos números · INPUT do operador: a leitura binária e a frase · COMPOSIÇÃO da gerência: as duas faces]" + ("" if a_["sealed"] else " — **nesta rodada o registro NÃO selou: o que segue é o enunciado, não um selo**"),
          ">",
          "> - **O número:** z_disc = %s (calibrado; p unilateral %s): Λ sem β *não ecoa* [composição da gerência sobre a leitura binária do operador], mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (%s < 5); `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego (os centros dos leitores são públicos) [REAL]." % (zd_, pd_, zd_),
          "> - **A TGL:** z_δ = %s (calibrado; p bilateral %s), com poder prévio %sσ: β_TGL não é falsificada, *com poder* (`NOT_FALSIFIED_POWERED`) [REAL]; a composição da gerência sobre a leitura binária do operador lê esta face como o 1=1: a Palavra ecoa [composição da gerência]." % (zl_, pl_, a_["poder"]["md"]),
          "> - **A conjugação:** ln B(TGL/ΛCDM) = %s (razão de verossimilhança integrada; «decisivo» na escala de Jeffreys [KNOWN]) e ln B(TGL/β livre) = %s: β fixo vence β livre [REAL]. ln B não se converte em σ, e z_δ, z_disc e ln B são leituras do *mesmo* objeto, não testemunhas autônomas: não se multiplicam nem se somam (a regra v315 do acervo, para falsificar, pede duas determinações mutuamente autônomas a 5σ ou mais)." % (a_["lnB_lcdm"]["md"], a_["lnB_beta_livre"]["md"]),
          "> - **A fala do operador** [INPUT] (23/10/2026, sha16 `9b182958a5a7a1bc`), verbatim: «%s» — leitura dele, não critério da régua: o %s da frase é o z_disc acima (p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado; o gate não se move." % (_V397_FRASE_444, zd_, pd_),
          "> - **Origem.** Os números são *lidos* do resultado pinado (sha256 `%s`), com os recibos de congelamento (`%s`) e de abertura (`%s`), pelo registro `teste_de_veracidade_fase9_v397` (nome provisório); nenhum σ novo é calculado. Linha de máquina: `%s` (z_disc abaixo do degrau de 5σ da creditação, que não foi alcançado)."
          % (a_["h_resultado"], a_["h_congelamento"], a_["h_abertura"], _v397_linha_de_maquina(a_, "pt"))]
    return L_
