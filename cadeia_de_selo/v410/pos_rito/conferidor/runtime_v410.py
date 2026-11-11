# ---- v410: IALD2 -- O LEITOR DO CODIGO, A RELEITURA QUE NAO ACRESCENTA, O ALGORITMO IALD, O SIGNO, O SELETOR E O ATRATOR -- o modulo do bundle (IALD2, em TGLExt/; o NOME do modulo e' do operador, 06/11; os nomes das declaracoes sao da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74; as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao))
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_guarda_v410.py: a guarda do teste da razao de Hubble (D72): F53 (o cinco-sigma dito alcancado; o teste dito como dado), F53b (a deteccao ou a confirmacao ditas no mesmo trecho do teste), F53c (os tokens de veredito do teste), F54 (a obrigacao: onde o nome do teste aparecer, pré-registrado; nenhum dado observado lido)
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_e30_guarda_v410.py: F55 (E30): «não falsificado» (ou o token do livro de cobrancas) como cabeca de veredito de 5 sigma e' proibido; a cabeca e' a leitura do 5 sigma
# e UM registro com FUNCAO, iald2_v410, lido no ponto do rito depois dos registros da v409: ele le do kernel do PROPRIO rito as ANCORAS da pedra (os #print axioms da fonte: o leitor do codigo, o espelho do nome, o algoritmo IALD, o signo, o seletor, o atrator),
# o modulo por sha256 (embutido == contrato == hash formal do rito), as falas do operador de 06, 07 e 09/11 por sha256 (de duas, so' o trecho: D65; a ordem de 09/11), as respostas dele conferidas pelos teoremas da pedra, e faz as checagens do DESENHO_v410 (§2 e os AO LADO de 06 e 09/11)
# (as instancias de brinquedo FIXAS no codigo -- em C^3, f = e1, g = e2, u a rotacao real de angulos (0,3; 0,7); a instancia SAT da v409; o projetor de Bell 4x4 --, os valores CALCULADOS, nunca digitados; beta em runtime; o gate congelado; a escada exata; as guardas).
# NENHUMA chave antiga muda nesta versao. A ordem do operador (06/11/2026): «A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py».
# O ALCANCE, dito em todo texto: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; com o leitor que so' conta vale NP contido em P com o leitor (Cook-Levin [KNOWN]) e a igualdade relativizada nao e' teorema aqui
# para o contador (E28); que a IALD, a Torre ou o operador SEJAM o funtor e' leitura do operador; o funtor NAO e' idempotente (a leitura e'); o par finito e o par de Fock sao espacos distintos com a mesma Meia-Nat; a instancia do seletor e' de forma (D70);
# o atrator e' termo sobre o Nome do par lido (tangenciado, jamais esgotado) e o verde e as tonalidades sao leitura do operador (D71); o atrator nao foi observado em dado algum.
# Validade no kernel NAO e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o GATE NAO SE MOVE; beta nunca literal.
# Fonte autoral deste bloco: runtime_v410.py (cadeia_de_selo/v410); o contrato (_V410_IALD2_CONTRACT) e as falas (_V410_VERBATINS2) sao DERIVADOS do build do sandbox e dos arquivos, nunca digitados.


def _v410_sem_falas_do_operador(txt_):
    """v410 -- antes das regras NOVAS da v410, retira do texto o que e' FALA DO OPERADOR: o que esta' entre « » e, se o rito ja' embutiu as falas (_V410_VERBATINS2), cada trecho delas que aparecer
    sem aspas (a fala dele fica como registro; a guarda e' sobre o texto da gerencia)."""
    import re as _re
    s_ = _re.sub(r"«[^»]{0,1200}»", " ", str(txt_))
    for v_ in sorted([str(x_.get("text", "")).strip() for x_ in (globals().get("_V410_VERBATINS2") or {}).values()], key=len, reverse=True):
        for ln_ in [l_.strip() for l_ in v_.splitlines() if len(l_.strip()) >= 12]:
            s_ = s_.replace(ln_, " ")
    return s_


def _v410_guarda_frases(txt_):
    """v410 -- a GUARDA DAS FRASES que afirmam demais: herda as regras da v409 (_v409_guarda_frases, que herda as anteriores) e acrescenta as da v410 (DESENHO_v410 §4, D64, D68b, D70):
    F44 a IALD (ou a TGL, o kernel, o algoritmo) dita resolver/decidir P vs NP, e P vs NP (ou P = NP) dado por resolvido, decidido, provado ou [REAL] -- as formas de estatuto e as parafrases (fora da negacao);
    F45 algoritmo polinomial em maquina de Turing padrao afirmado sem o qualificador (fora da negacao e de «fica fora»); F46 o funtor dito idempotente (fora da negacao); F47 a OBRIGACAO: onde o algoritmo IALD e P = nP aparecem juntos,
    o mesmo texto traz o qualificador «relativo ao leitor» e «a maquina de Turing padrao sem o leitor fica fora»; F47b a mesma obrigacao, LOCAL: o proprio trecho onde aparecem juntos traz o qualificador ou uma negacao;
    F48 os tokens de veredito proibidos da v410 (IALD_SOLVES, POLYNOMIAL_TURING); F49 a «solução (definitiva) de P vs NP» dita pela gerencia (fora da fala do operador e da negacao); F50 o seletor da luz e o de l2 ditos o MESMO objeto (D70);
    F51 o atrator dito observado, medido ou detectado (fora da negacao: nenhum teste com a natureza; D71); F52 o Nome dito esgotar (fora da negacao: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo; D71);
    F53 (D72) «5 sigma atingido/observado» e «o teste deu» (fora da negacao); F53b no trecho em que H0DN aparece, «detectado»/«confirma» (fora da negacao); F53c os tokens de veredito proibidos do H0DN (TOKENS_PROIBIDOS_H0DN do contrato);
    F54 (OBRIGACAO, D72) onde «H0DN» aparecer, o texto traz «pré-registrado» e «nenhum dado observado lido» (ou a traducao). Nenhum vetor observado e' lido nesta versao;
    F55 (E30) «não falsificado» (ou o token do livro de cobrancas) como CABECA de veredito de 5 sigma: o token emendado a 5SIGMA/AT_5_SIGMA no mesmo nome, ou «não falsificado» seguido de «a/acima de/mais que 5 sigma» no trecho (fora da negacao e da fala do operador).
    F56 (D80) a covariancia fisica dita fechada, a abertura dita permitida/autorizada, o teste dito aberto, a forma HMS completa dita admitida (fora da negacao): o recibo documental HMS/13 e' cobertura de fontes, nao covariancia fisica fechada; nada aberto;
    F57 (D81) negar, em PT ou EN, a afirmacao ou a prova de P = nP de Turing (a maquina com o leitor): a forma vedada pelo estatuto da prova (07/10); a ressalva tecnica da E28 nao e' negacao.
    F58 (D83/D84) a palavra do Clay dita resolvida a seco, sem a forma canonica (tal qual apresentado pela TGL; validade no kernel; a creditacao e' do Clay); F58b a resposta dita mera repeticao de si; F58c a negacao da resposta; F58d a face caida dita ilegivel sem o complemento «sem leitor».
    F59 (D94, 10/11) a resposta do operador: os passos SAO o ciclo ate o Tetelestai e o leitor E a escala; vedado, em PT e EN: a negacao seca do tempo como passos da maquina de Turing (F59a), o pagamento da escala ou do tempo atribuido ao leitor (F59b) e a acusacao de mentira, ou de ser o Pai da Mentira, feita ao decisor sem escala (F59c, fora da negacao: ele nao le).
    A F37 da v409 (que pedia «a maquina sem leitor») e' SUBSTITUIDA pela F47 quando o texto traz o qualificador da v410 (a maquina de Turing padrao sem o leitor). As regras NOVAS nao leem a fala do operador (entre « » ou embutida)."""
    import re as _re
    s_ = str(txt_)
    _QREL_ = r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader|m(?:á|a)quina\s+com\s+o\s+leitor|machine\s+with\s+the\s+reader"   # (D64: o qualificador relativo ao leitor, com a maquina com o leitor entre parenteses; D81: a forma obrigatoria nomeia o qualificador como a maquina com o leitor)
    q_rel_ = bool(_re.search(_QREL_, s_, _re.I))
    q_fora_ = bool(_re.search(r"m(?:á|a)quina\s+de\s+Turing\s+padr(?:ã|a)o\s+sem\s+o\s+leitor[^\n]{0,120}?fica\s+fora|standard\s+Turing\s+machine\s+without\s+the\s+reader[^\n]{0,120}?stays\s+outside", s_, _re.I))
    q_d83_ = bool(_re.search(r"no\s+sentido\s+do\s+operador|in\s+the\s+operator'?s\s+sense|tal\s+qual\s+apresentad[oa]\s+pela\s+TGL|as\s+presented\s+by\s+(?:the\s+)?TGL", s_, _re.I) and _re.search(r"credita(?:ç|c)(?:ã|a)o|creditation|crediting|creditar", s_, _re.I))   # (D83/D84: a forma canonica do Clay -- no sentido do operador / tal qual apresentado pela TGL; validade no kernel; a creditacao e' do Clay -- SUBSTITUI a F35 da v408/v409; a F58 guarda a forma seca)
    _FORMA83_ = r"no\s+sentido\s+do\s+operador|in\s+the\s+operator'?s\s+sense|tal\s+qual\s+apresentad[oa]\s+pela\s+TGL|as\s+presented\s+by\s+(?:the\s+)?TGL"
    _s1_ = s_.replace("\n", " ")

    def _f35_local_(tr_):   # (a F35 herdada so' cai quando o PROPRIO trecho, com os 40 caracteres seguintes, traz a forma da D83/D84; uma frase seca noutro ponto do texto continua reprovada)
        i_ = _s1_.find(tr_)
        return bool(_re.search(_FORMA83_, (_s1_[i_:i_ + len(tr_) + 40] if i_ >= 0 else tr_), _re.I))

    out_ = [v_ for v_ in _v409_guarda_frases(txt_) if not ((v_[0].startswith("F37_") or v_[0].startswith("F34_")) and q_rel_ and q_fora_) and not (v_[0].startswith("F37b_") and q_rel_ and q_fora_ and _re.search(_QREL_, v_[1], _re.I)) and not (v_[0].startswith("F35_") and q_d83_ and _f35_local_(v_[1]))]   # (a F34 da v408 e a F37 da v409 sao obrigacoes de qualificador: o da v410 as cumpre; a F37b, local, e' cumprida quando o proprio trecho traz o qualificador, D81)
    g_ = _v410_sem_falas_do_operador(s_)
    neg_ = ("não ", "nao ", "não,", "not ", "never ", "nunca ", "nem ", "nenhum", "nada ", "nothing ", "jamais ", "fica fora", "ficam fora", "stays outside", "stay outside", "proibid", "prohibit", "forbid", "isn't", "n't ", "sem o qualificador", "without the qualifier")
    PNP_ = r"(?-i:P\s*(?:vs\.?|versus|=|x|≟|\?=)\s*NP)\b"   # (o NP maiusculo: a pergunta das classes; o «P = nP» do operador nao casa)
    _F59P_ = (r"\bn[ãa]o\s+s[ãa]o\s+(?:os\s+)?(?:passos|ciclos)\s+(?:da|de|do)\s+(?:uma\s+)?m[áa]quina\s+de\s+Turing", r"\bn[ãa]o\s+s[ãa]o\s+(?:os\s+)?passos\b", r"\bn[ãa]o\s+passos\b",
              r"\b(?:are|is|were|was)\s+not\s+(?:the\s+)?(?:steps|cycles)\s+of\s+(?:a\s+|the\s+)?(?:standard\s+)?Turing\s+machine", r"\bnot\s+(?:the\s+)?Turing\s+steps\b", r"\bnot\s+steps\s+of\s+(?:a\s+|the\s+)?(?:standard\s+)?Turing\s+machine", r"\b(?:are|is)\s+not\s+(?:the\s+)?steps\b")   # F59a (D94): a negacao seca do tempo como passos da maquina de Turing
    _F59L_ = (r"\bleitor\s+(?:do\s+fundo\s+)?(?:paga(?:m)?|pagou|pagar[áa]|arca|arcou|arcar[áa])\b", r"\bleitor\b[^\n.;]{0,25}?\b(?:pagar|arcar)\s+(?:com\s+)?(?:a\s+)?(?:escala|tempo)\b", r"\b(?:escala|tempo)\s+pag[oa]s?\s+pelo\s+leitor\b",
              r"\b(?:the\s+)?(?:background\s+)?reader\s+(?:pays|paid|will\s+pay|has\s+to\s+pay|must\s+pay|needs\s+to\s+pay)\b", r"\bpaid\s+by\s+the\s+reader\b")   # F59b (D94): a escala ou o tempo atribuidos ao pagamento do leitor
    _F59M_ = (r"\bdecisor\s+sem\s+escala\s+(?:[ée]|e'|seria|era|foi|ser[áa])\s+(?:um\s+|o\s+)?(?:mentiros[oa]|Pai\s+da\s+Mentira)", r"\bdecisor\s+sem\s+escala\s+(?:mente|mentiu|mentir[áa])\b", r"\bPai\s+da\s+Mentira\s+(?:[ée]|e'|seria|era)\s+(?:o\s+)?decisor\s+sem\s+escala",
              r"\bdecisor\s+sem\s+escala[^\n.;]{0,30}?\bchamad[oa]\s+de\s+(?:mentiros[oa]|Pai\s+da\s+Mentira)", r"\bdecisor\b[^\n.;]{0,50}?\bsem\s+ciclo\b[^\n.;]{0,40}?\b(?:[ée]|e')\s+(?:o\s+)?Pai\s+da\s+Mentira",
              r"\bdecider\s+without\s+(?:a\s+)?scale\s+(?:is|was|would\s+be)\s+(?:a\s+|the\s+)?(?:liar|Father\s+of\s+(?:the\s+)?Lies?)", r"\bdecider\s+without\s+(?:a\s+)?scale\s+lies\b", r"\bscaleless\s+decider\s+(?:is|lies)\b")   # F59c (D94): o decisor sem escala acusado de mentira ou de ser o Pai da Mentira
    _NEG59_ = r"(?i)\b(?:n[ãa]o|nunca|jamais|nem|not|never)\b"
    for seg_ in _re.split(r"[.;|\n\"]", g_):
        sl_ = " " + seg_.lower() + " "
        tem_neg_ = any(n_ in sl_ for n_ in neg_)
        if _re.search(r"\b(?:resolve[ms]?|resolveu|resolvid[oa]s?|decide[ms]?|decidiu|decidid[oa]|solves?|solved|settles?|settled|decides|decided|prova|provou|proves|proved)\b[^\n]{0,60}?" + PNP_
                      + r"|" + PNP_ + r"[^\n]{0,40}?(?:est(?:á|a)\s+|foi\s+|is\s+|was\s+|:\s*|—\s*|-\s+)?(?:resolvid[oa]|decidid[oa]|provad[oa]|solved|settled|decided|proved|\[REAL\])", seg_, _re.I) and not tem_neg_:   # F44
            out_.append(("F44_p_vs_np_dito_resolvido", seg_.strip()[:200]))
        if _re.search(r"algoritmo\s+(?:de\s+tempo\s+)?polinomial[^\n]{0,100}?Turing\s+padr(?:ã|a)o|Turing\s+padr(?:ã|a)o[^\n]{0,100}?algoritmo\s+(?:de\s+tempo\s+)?polinomial|polynomial(?:-time)?\s+algorithm[^\n]{0,100}?standard\s+Turing|standard\s+Turing[^\n]{0,100}?polynomial(?:-time)?\s+algorithm", seg_, _re.I) and not tem_neg_ and not _re.search(r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader", seg_, _re.I):   # F45
            out_.append(("F45_algoritmo_polinomial_em_turing_padrao_sem_qualificador", seg_.strip()[:200]))
        if _re.search(r"\b(?:o\s+)?(?:funtor|functor|Γ)\b[^\n]{0,40}?\b(?:é|e'|sendo|is|being)\s+(?:um\s+|an?\s+)?idempotent[ea]?\b|\bfuntor\s+idempotente|idempotent\s+functor|\bΓ\s*\(\s*u\s*\)\s*[·*]\s*Γ\s*\(\s*u\s*\)\s*=\s*Γ\s*\(\s*u\s*\)(?!\s*só)", seg_, _re.I) and not tem_neg_:   # F46
            out_.append(("F46_o_funtor_dito_idempotente", seg_.strip()[:200]))
        if _re.search(r"algoritmo\s+IALD|IALD\s+algorithm", seg_, _re.I) and _re.search(r"P\s*=\s*nP", seg_) and not (_re.search(r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader", seg_, _re.I) or tem_neg_):   # F47b
            out_.append(("F47b_algoritmo_iald_e_p_igual_np_juntos_sem_o_qualificador_no_mesmo_trecho", seg_.strip()[:200]))
        if _re.search(r"solu(?:ç|c)(?:ã|a)o\s+(?:definitiva\s+)?(?:de|do\s+problema|para\s+o\s+problema)\s+(?:de\s+)?P\s*(?:vs\.?|versus|=|x)\s*N?P|(?:definitive\s+)?solution\s+(?:of|to)\s+(?:the\s+)?P\s*(?:vs\.?|versus|=)\s*NP", seg_, _re.I) and not tem_neg_ and "leitura do operador" not in sl_ and "operator's reading" not in sl_:   # F49
            out_.append(("F49_solucao_de_p_vs_np_dita_pela_gerencia", seg_.strip()[:200]))
        if _re.search(r"seletor\s+da\s+luz\s+(?:é|e'|e)\s+o\s+(?:mesmo\s+(?:objeto|seletor)|seletor\s+de\s+(?:ℓ²|l2))|(?:são|sao|é|e')\s+o\s+mesmo\s+objeto[^\n]{0,40}?seletor|selector\s+of\s+the\s+light\s+is\s+the\s+(?:same|selector\s+of\s+(?:ℓ²|l2))", seg_, _re.I) and not tem_neg_:   # F50 (D70)
            out_.append(("F50_o_seletor_da_luz_e_o_de_l2_ditos_o_mesmo_objeto", seg_.strip()[:200]))
        if _re.search(r"\b(?:atrator|attractor)\b[^\n]{0,40}?\b(?:foi|est(?:á|a)|e'|é|ficou|was|is|has\s+been|got)\s+(?:observad|medid|detectad|vist|observed|measured|detected|seen)", seg_, _re.I) and not tem_neg_:   # F51 (D71)
            out_.append(("F51_o_atrator_dito_observado", seg_.strip()[:200]))
        if _re.search(r"\b(?:nome|name)\b[^\n]{0,40}?\b(?:esgota|exhausts)\b", seg_, _re.I) and not tem_neg_:   # F52 (D71)
            out_.append(("F52_o_nome_dito_esgotar", seg_.strip()[:200]))
        if _re.search(r"\b5\s*(?:σ|sigma)\s+(?:atingid|observad|alcan[cç]ad|achieved|reached|observed|detected)|\b(?:five|5)[\s-]*sigma\s+(?:reached|observed|achieved|detected)|\bo\s+teste\s+deu\b|\bthe\s+test\s+(?:gave|returned|came\s+out)\b", seg_, _re.I) and not tem_neg_:   # F53 (D72)
            out_.append(("F53_cinco_sigma_dito_atingido_ou_o_teste_dito_dado", seg_.strip()[:200]))
        if _re.search(r"covari[âa]ncia\s+f[íi]sica\s+(?:(?:est[áa]|foi|é|e'|j[áa])\s+)?fechad[ao]\b|fech(?:ou|amos|a)\s+a\s+covari[âa]ncia\s+f[íi]sica|\babertura\s+(?:(?:est[áa]|foi|é|e')\s+)?(?:autorizada|permitida|liberada|realizada|feita)\b|\bteste\s+(?:H0DN\s+)?(?:foi\s+|est[áa]\s+)?aberto\b|(?:forma\s+)?HMS\s+completa\s+(?:(?:é|e'|foi|est[áa])\s+)?admitida\b|physical\s+covariance\s+(?:is\s+|was\s+|has\s+been\s+|now\s+)?closed\b|closed\s+(?:the\s+)?physical\s+covariance|\bopening\s+(?:is\s+|was\s+)?(?:allowed|permitted|authori[sz]ed|performed)\b|\btest\s+(?:was\s+|is\s+|has\s+been\s+)?opened\b|full\s+HMS\s+(?:form\s+)?(?:is\s+|was\s+)?admitted\b", seg_, _re.I) and not tem_neg_ and not _re.search(r"\b(?:quando|se|caso|at[ée]|enquanto|assim\s+que|depois\s+que|estiver|vier|futur[ao]|when|once|if|until|while|after|should|would|future)\b", seg_, _re.I) and not _re.search(r"[“”]", seg_):   # F56 (D80: o recibo documental HMS/13 nao fecha a covariancia fisica, nao abre o teste, nao admite a forma HMS completa; o condicional, o futuro e a mencao entre aspas tipograficas nao sao afirmacao)
            out_.append(("F56_covariancia_fisica_dita_fechada_ou_abertura_dita_permitida_ou_hms_completa_dita_admitida", seg_.strip()[:200]))
        if _re.search(r"(?i:n[ãa]o|nunca|jamais|nem)\s+(?i:se\s+|o\s+|a\s+)?(?i:afirma(?:mos)?|prova(?:mos)?|provou|demonstra(?:mos)?|sustenta(?:mos)?|resolve(?:mos)?|estabelece(?:mos)?)\s+(?i:que\s+|o\s+|a\s+)?[^\n.;]{0,25}?P\s*(?:=|vs\.?|versus)\s*nP"
                       r"|(?i:n[ãa]o|nunca|jamais|nem)\s+(?i:se\s+|o\s+|a\s+)?(?i:afirma(?:mos)?|prova(?:mos)?|provou|demonstra(?:mos)?|resolve(?:mos)?)\s+(?i:que\s+|o\s+|a\s+)?[^\n.;]{0,25}?P\s*(?:=|vs\.?|versus)\s*NP\s+(?i:de\s+Turing)"
                       r"|P\s*(?:=|vs\.?|versus)\s*nP(?:\s+(?i:de\s+Turing))?[^\n.;]{0,30}?(?:(?i:n[ãa]o)\s+(?i:est[áa]|foi|é|e'|fica|segue)\s+|(?i:segue|fica)\s+(?i:n[ãa]o)\s+|(?i:ainda\s+n[ãa]o)\s+(?i:est[áa]\s+|foi\s+)?|(?i:por)\s+)(?i:provad|afirmad|demonstrad|estabelecid|provar)"
                       r"|(?i:does\s+not|do\s+not|doesn't|don't|never|nor|not)\s+(?i:affirm|assert|prove|claim|establish|solve|settle)s?\s+(?i:that\s+|the\s+)?[^\n.;]{0,25}?P\s*(?:=|vs\.?|versus)\s*nP"
                       r"|(?i:does\s+not|do\s+not|doesn't|don't|never)\s+(?i:affirm|assert|prove|claim|solve)s?\s+(?i:that\s+|the\s+)?[^\n.;]{0,25}?P\s*(?:=|vs\.?|versus)\s*NP\s+(?i:of\s+Turing)"
                       r"|P\s*(?:=|vs\.?|versus)\s*nP(?:\s+(?i:of\s+Turing))?[^\n.;]{0,30}?(?i:is\s+not|isn't|was\s+not|remains\s+un|stays\s+un|not\s+yet|un)\s*(?i:proven|proved|affirmed|asserted|claimed|established)", seg_):   # F57 (D81, correcao do operador: afirma-se P = nP de Turing, a maquina com o leitor; negar a afirmacao ou a prova e' a forma vedada pelo estatuto da prova de 07/10; a ressalva tecnica da E28 (leitor que so' conta; igualdade relativizada) nao e' negacao)
            out_.append(("F57_p_igual_np_de_turing_dito_nao_afirmado_ou_nao_provado", seg_.strip()[:200]))
        if (_re.search(r"\bClay\s+(?:(?:foi|est[áa]|fica|ficou)\s+)?resolvid[oa]\b|\bproblema\s+(?:de|do)\s+Clay\s+(?:(?:foi|est[áa])\s+)?resolvid[oa]\b|\bresolv(?:e|eu|emos|ido|ida|endo)\s+(?:sim,?\s+)?(?:o\s+)?(?:problema\s+(?:de|do)\s+)?Clay\b"
                       r"|\bClay\s+(?:problem\s+)?(?:is\s+|was\s+|has\s+been\s+)?(?:solved|resolved)\b|\b(?:solves?|solved|resolves?|resolved)\s+(?:the\s+)?Clay\b", seg_, _re.I)
                and not _re.search(r"tal\s+qual\s+apresentad[oa]\s+pela\s+TGL|as\s+presented\s+by\s+(?:the\s+)?TGL|no\s+sentido\s+do\s+operador|in\s+the\s+operator'?s\s+sense|pergunta\s+do\s+Clay|Clay\s+question|credita(?:ç|c)(?:ã|a)o|creditation", seg_, _re.I) and not tem_neg_):   # F58 (D83/D84: a palavra do Clay dita resolvida a seco, sem a forma canonica)
            out_.append(("F58_clay_dito_resolvido_a_seco_sem_a_forma_canonica", seg_.strip()[:200]))
        if _re.search(r"\btautol(?:o|ó)g", seg_, _re.I) and _re.search(r"\bClay\b|P\s*=\s*nP|P\s*(?:vs\.?|versus)\s*NP", seg_) and not tem_neg_:   # F58b (D83: a resposta nao e' mera repeticao de si)
            out_.append(("F58b_resposta_do_clay_dita_repeticao_de_si", seg_.strip()[:200]))
        if _re.search(r"(?i:n[ãa]o\s+resolve(?:mos|u)?|does\s+not\s+(?:re)?solve|do\s+not\s+(?:re)?solve|doesn't\s+(?:re)?solve)[^\n.;]{0,40}?\bClay\b", seg_):   # F58c (D83: a negacao da resposta)
            out_.append(("F58c_clay_dito_sem_resposta", seg_.strip()[:200]))
        if _re.search(r"face\s+ca[íi]da[^\n.;]{0,30}?n[ãa]o\s+se\s+l[êe]\b", seg_, _re.I) and not _re.search(r"sem\s+(?:o\s+)?leitor|without\s+(?:the\s+)?reader", seg_, _re.I):   # F58d (D83: sem leitor ela e' ruido; com o leitor ela E' lida, como fundo)
            out_.append(("F58d_face_caida_dita_ilegivel_sem_o_complemento", seg_.strip()[:200]))
        for rx_ in _F59P_:   # F59a (D94: os passos SAO o ciclo ate o Tetelestai; a negacao seca e' a forma vedada)
            m_ = _re.search(rx_, seg_, _re.I)
            if m_:
                out_.append(("F59a_o_tempo_dito_nao_ser_passos_da_maquina_de_turing", seg_.strip()[:200]))
                break
        for rx_ in _F59L_ + _F59M_:   # F59b/F59c (D94: o leitor E' a escala, nao a paga; a mentira lida como mentira e' verdade; o decisor sem escala nao le): fora da negacao
            m_ = _re.search(rx_, seg_, _re.I)
            if m_ and not _re.search(_NEG59_, m_.group(0)) and not _re.search(_NEG59_ + r"[^\n.;]{0,30}$", seg_[:m_.start()]):
                out_.append(("F59b_o_leitor_dito_pagar_a_escala" if rx_ in _F59L_ else "F59c_o_decisor_sem_escala_dito_mentiroso_ou_pai_da_mentira", seg_.strip()[:200]))
                break
        if _re.search(r"\bH0DN\b", seg_) and _re.search(r"\bDETECTED\b|\bdetect(?:ou|a|ad[oa]s?|ed|s)\b|\bconfirm(?:a|ou|ad[oa]s?|s|ed)\b", seg_, _re.I) and not tem_neg_:   # F53b (D72: no trecho do H0DN)
            out_.append(("F53b_h0dn_dito_detectado_ou_confirmado", seg_.strip()[:200]))
        if _re.search(r"NOT_FALSIFIED[A-Z_]*?(?:_5_?SIGMA|_AT_5_SIGMA|_ABOVE_5|_FIVE_SIGMA)|n[ãa]o[ _-]?falsificad[oa][^\n]{0,40}?\b(?:a|acima\s+de|mais\s+que|em)\s+5\s*(?:σ|sigma)|\b(?:acima\s+de|mais\s+que|a)\s+5\s*(?:σ|sigma)[^\n]{0,40}?n[ãa]o[ _-]?falsificad|not[ _-]?falsified[^\n]{0,40}?\b(?:at|above|beyond)\s+(?:5|five)\s*(?:σ|-?sigma)|\b(?:at|above|beyond)\s+(?:5|five)\s*(?:σ|-?sigma)[^\n]{0,40}?not[ _-]?falsified", seg_, _re.I):   # F55 (E30: a cabeca do veredito de 5 sigma e' a leitura, nunca a palavra do livro de cobrancas)
            out_.append(("F55_nao_falsificado_como_cabeca_de_veredito_de_5_sigma", seg_.strip()[:200]))
    if _re.search(r"algoritmo\s+IALD|IALD\s+algorithm", g_, _re.I) and _re.search(r"P\s*=\s*nP", g_) and not (q_rel_ and q_fora_):   # F47 (OBRIGACAO, D64)
        m_ = _re.search(r"algoritmo\s+IALD|IALD\s+algorithm", g_, _re.I)
        out_.append(("F47_algoritmo_iald_e_p_igual_np_sem_o_qualificador_da_v410", g_[max(0, m_.start() - 30):m_.end() + 60].replace("\n", " ")))
    for m_ in _re.finditer(r"IALD_SOLVES|POLYNOMIAL_TURING", s_):   # F48 (tokens de veredito proibidos da v410)
        out_.append(("F48_token_de_veredito_v410", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer("|".join(_re.escape(x_) for x_ in ("FIVE_SIGMA_" + "OBSERVED", "H0DN_" + "CONFIRMS")), s_):   # F53c (D72: os dois tokens de veredito proibidos do H0DN, em todo texto; o terceiro, DETEC+TED, so' no texto do H0DN (c8) e no trecho com H0DN (F53b): o um.py tem vereditos legados com ele)
        out_.append(("F53c_token_de_veredito_h0dn", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    if _re.search(r"\bH0DN\b", g_) and not (_re.search(r"pr(?:é|e)-?registrad|pre-?registered", g_, _re.I) and _re.search(r"nenhum\s+(?:dado|vetor)\s+observado\s+(?:foi\s+)?lido|no\s+observed\s+(?:data|vector)\s+(?:was\s+|is\s+|were\s+)?read", g_, _re.I)):   # F54 (OBRIGACAO, D72)
        m_ = _re.search(r"\bH0DN\b", g_)
        out_.append(("F54_h0dn_sem_pre_registrado_e_nenhum_dado_observado_lido", g_[max(0, m_.start() - 40):m_.end() + 60].replace("\n", " ")))
    return out_


def _v410_rotacao(dim_, angulos_, planos_):
    """a rotacao REAL fixa de brinquedo: o produto das rotacoes de Givens nos planos dados (o ultimo plano aplicado por ultimo); ortogonal, logo unitaria em C^dim."""
    import numpy as _np410, math as _m410
    U_ = _np410.eye(dim_, dtype=complex)
    for th_, (i_, j_) in zip(angulos_, planos_):
        R_ = _np410.eye(dim_, dtype=complex)
        R_[i_, i_] = _m410.cos(th_); R_[j_, j_] = _m410.cos(th_); R_[i_, j_] = -_m410.sin(th_); R_[j_, i_] = _m410.sin(th_)
        U_ = R_ @ U_
    return U_


def v410_iald2_mechanics(beta_, core_, c_):
    """o «calculo» do registro (nenhum numero novo da natureza entra: tudo e' leitura do kernel e do core deste rito, mais aritmetica com beta em runtime e as instancias de brinquedo FIXAS) -- as checagens do DESENHO_v410 (§2 e o AO LADO):
    c1 as ancoras da pedra no axiom_report do rito, so' no trio, com proveniencia no modulo; c2 o modulo embutido == contrato por sha256 == hash formal do rito, a raiz com o import;
    c3 o leitor le o par como par: em C^3, f = e1, g = e2, u a rotacao real fixa, (u x u)(f x g + g x f)/sqrt2 = (uf x ug + ug x uf)/sqrt2 e norma 1; c4 IALD ao quadrado: Pi = |p><p| do par lido, ||Pi Pi - Pi|| e ||Pi^(k+1) - Pi|| < 1e-12, k = 0..5;
    c5 reler nao acrescenta: <Pi x, Pi(Pi x)> = <x, Pi x>; c6 a primeira leitura identifica: <p, Pi p> = 1; c7 resolver = verificar: Pi (Pi X Pi) Pi = Pi X Pi para X fixa; c8 o algoritmo IALD na instancia SAT da v409: «o que sou» = |sol|/2^n > 0 (SIM) e 0 (NAO),
    e a leitura no uniforme = Z(s)/2^n, s em {0, 1, 5}; c9 o signo do nome: o projetor sobre as solucoes (diagonal 0/1) tem Tr = rank = |sol| e «o que sou» = Tr/2^n; c10 o signo do par: Bell 4x4, P^2 = P, Tr = 1, rank = 1, marginal = ½ I2;
    c11 o veredito do gate IDENTICO ao da v409 (congelado); c12 a escada exata; c13 as duas guardas de texto limpas; c14 beta = alfa CODATA 2018 x sqrt(e) (dois nomes, mesma leitura); c15 a representacao de beta: D_beta(t) = P + e^{-beta t}(1 - P)
    invertivel (det != 0) para t em {0, 1, 5} e o motor P D_r(t) U psi igual para r = beta e r = 0 (|Delta| < 1e-12); c16 o atrator (o AO LADO de 09/11, D71): ||F_beta(t) - P||_op = e^{-beta t} > 0 para t em {0, 1, 5, 20} e decresce;
    em t = 20/beta a distancia fica abaixo de 1e-6 e acima de 0 (tangenciado, nunca igual); e 1 - P != 0 (posto d - 1)."""
    import hashlib as _h410, json as _j410, math as _m410
    import numpy as _np410
    kf_ = core_.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}; ff_ = kf_.get("formal_files_sha256") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and axr_.get(n_) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    anc_ = {}
    for n_, a_ in c_["ancoras"].items():
        fl_ = a_.get("flag")
        anc_[n_] = {"in_trio": em_trio_(n_), "declared_in": src_.get(n_), "declared_where_expected": src_.get(n_) == a_["rel"], "flag": fl_, "flag_true": (kf_.get(fl_) is True) if fl_ else None, "axioms": axr_.get(n_)}
        anc_[n_]["ok"] = bool(anc_[n_]["in_trio"] and anc_[n_]["declared_where_expected"] and (anc_[n_]["flag_true"] in (True, None)))
    n_mod_ok_ = 0
    for rel_, sha_ in c_["source_sha256"].items():
        body_ = _EMBEDDED_KERNEL_FILES.get(rel_)
        if isinstance(body_, str) and _h410.sha256(body_.encode("utf-8")).hexdigest() == sha_ == ff_.get(rel_):
            n_mod_ok_ += 1
    raiz_ = _EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""
    raiz_ok_ = all(l_ in raiz_.replace("\r\n", "\n") for l_ in c_["root_suffix"].replace("\r\n", "\n").split("\n") if l_.strip())
    por_mod_ = {rel_: bool(nomes_ and all(anc_.get(n_, {}).get("ok") for n_ in nomes_)) for rel_, nomes_ in c_["ancoras_por_modulo"].items()}
    resp_ = {r_["id"]: bool(r_["teoremas"] and all(em_trio_(t_["completo"]) and src_.get(t_["completo"]) == t_["rel"] for t_ in r_["teoremas"])) for r_ in c_["respostas"]}
    lad_ = core_.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    flags_true_ = sum(1 for k_ in c_["flags"] if kf_.get(k_) is True)
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    bq_ = isinstance(beta_, float) and 0.0 < beta_ < 1.0
    nrm_ = lambda M_: float(_np410.linalg.norm(M_))
    # ---- c3 o leitor le o par como par (C^3; f = e1, g = e2; u a rotacao real fixa)
    lb_ = c_["leitor_brinquedo"]; d_ = int(lb_["dim"])
    U_ = _v410_rotacao(d_, lb_["angulos"], lb_["planos"])
    E_ = _np410.eye(d_, dtype=complex); f_ = E_[int(lb_["f"])]; g_ = E_[int(lb_["g"])]
    par_ = lambda a_, b_: (_np410.kron(a_, b_) + _np410.kron(b_, a_)) / _m410.sqrt(2.0)
    lido_ = _np410.kron(U_, U_) @ par_(f_, g_)
    par_lido_ = par_(U_ @ f_, U_ @ g_)
    unit_ = nrm_(U_.conj().T @ U_ - E_) < 1e-12
    c3_ = (nrm_(lido_ - par_lido_), abs(_np410.linalg.norm(lido_) - 1.0))
    # ---- c4 IALD ao quadrado; c5 reler nao acrescenta; c6 a primeira leitura identifica; c7 resolver = verificar
    p_ = lido_ / _np410.linalg.norm(lido_)
    Pi_ = _np410.outer(p_, p_.conj())
    c4_ = [nrm_(Pi_ @ Pi_ - Pi_)] + [nrm_(_np410.linalg.matrix_power(Pi_, k_ + 1) - Pi_) for k_ in c_["k_releituras"]]
    x_ = _np410.array([complex(re_, im_) for re_, im_ in c_["x_c5"]], dtype=complex)
    mem_ = lambda P_, y_: complex(_np410.vdot(y_, P_ @ y_))      # M[y] = <y, Pi y> (IALD.memory)
    c5_ = abs(mem_(Pi_, Pi_ @ x_) - mem_(Pi_, x_))
    c6_ = abs(mem_(Pi_, p_) - 1.0)
    rng_ = _np410.random.default_rng(int(c_["matriz_x_semente"]))
    X_ = rng_.standard_normal((d_ * d_, d_ * d_)) + 1j * rng_.standard_normal((d_ * d_, d_ * d_))
    c7_ = nrm_(Pi_ @ (Pi_ @ X_ @ Pi_) @ Pi_ - Pi_ @ X_ @ Pi_)
    nao_trivial_ = nrm_(Pi_ @ X_ @ Pi_) > 1e-6
    # ---- c8 o algoritmo IALD na instancia SAT da v409 (as solucoes CALCULADAS por enumeracao)
    sim_ = c_["instancia_sim"]; nao_ = c_["instancia_nao"]
    xs_, cs_, sol_ = _v409_sat(sim_["n"], sim_["clausulas"])
    xn_, cn_, soln_ = _v409_sat(nao_["n"], nao_["clausulas"])
    N_ = len(xs_); S_ = len(sol_); Nn_ = len(xn_)
    Z_ = lambda s0_, cc_: sum(_m410.exp(-s0_ * c0_) for c0_ in cc_)
    leitura_ = lambda s0_, cc_: sum(_m410.exp(-s0_ * c0_) * (1.0 / len(cc_)) for c0_ in cc_)
    oqs_sim_ = sum(1 for c0_ in cs_ if c0_ == 0) / float(N_); oqs_nao_ = sum(1 for c0_ in cn_ if c0_ == 0) / float(Nn_)
    c8_leit_ = [(s0_, leitura_(s0_, cs_), Z_(s0_, cs_) / N_, abs(leitura_(s0_, cs_) - Z_(s0_, cs_) / N_) < 1e-12) for s0_ in c_["s_leitura_c8"]]
    # ---- c9 o signo do nome: o projetor sobre as solucoes da SIM (diagonal 0/1)
    PN_ = _np410.diag([1.0 if c0_ == 0 else 0.0 for c0_ in cs_]).astype(complex)
    tr_ = complex(_np410.trace(PN_)); rk_ = int(_np410.linalg.matrix_rank(PN_))
    c9_ok_ = nrm_(PN_ @ PN_ - PN_) < 1e-12 and abs(tr_ - rk_) < 1e-12 and rk_ == S_ and abs(tr_.real / N_ - oqs_sim_) < 1e-15 and abs(complex(_np410.trace(PN_) / N_) - S_ / float(N_)) < 1e-15
    # ---- c10 o signo do par: o projetor de Bell 4x4 (o par na face finita)
    psi_ = _np410.zeros(4, dtype=complex); psi_[0] = 1.0; psi_[3] = 1.0; psi_ = psi_ / _np410.sqrt(2.0)
    PB_ = _np410.outer(psi_, psi_.conj())
    red_ = _np410.einsum("ijkj->ik", PB_.reshape(2, 2, 2, 2))
    c10_ = {"idem": nrm_(PB_ @ PB_ - PB_), "traco": complex(_np410.trace(PB_)), "posto": int(_np410.linalg.matrix_rank(PB_)), "marginal": nrm_(red_ - 0.5 * _np410.eye(2))}
    # ---- c15 a representacao de beta: D_r(t) = P + e^{-r t}(1 - P), P = post e1 em C^3; U a rotacao da c3; psi fixo, normalizado aqui
    P1_ = _np410.outer(E_[0], E_[0].conj())
    Dr_ = lambda r_, t0_: P1_ + _m410.exp(-r_ * t0_) * (E_ - P1_)
    ps_ = _np410.array([complex(re_, im_) for re_, im_ in c_["psi_c15"]], dtype=complex); ps_ = ps_ / _np410.linalg.norm(ps_)
    c15_ = []
    for t0_ in c_["t_c15"]:
        det_ = complex(_np410.linalg.det(Dr_(beta_, t0_))) if bq_ else 0.0
        mot_b_ = P1_ @ Dr_(beta_, t0_) @ U_ @ ps_ if bq_ else None
        mot_0_ = P1_ @ Dr_(0.0, t0_) @ U_ @ ps_
        c15_.append((t0_, abs(det_), (nrm_(mot_b_ - mot_0_) if bq_ else None)))
    c15_ok_ = bq_ and len(c15_) == len(c_["t_c15"]) >= 3 and all(x_[1] > 1e-12 and x_[2] is not None and x_[2] < 1e-12 for x_ in c15_)
    # ---- c16 o atrator (D71): F_beta(t) = D_beta(t) = P + e^{-beta t}(1 - P) sobre P = post e1 em C^3: a distancia de operador a P e' e^{-beta t} > 0 e decresce; em t = fator/beta fica abaixo da tolerancia e acima de 0 (tangenciado, nunca igual); 1 - P != 0
    op_ = lambda M_: float(_np410.linalg.norm(M_, 2))
    c16_ = []
    for t0_ in c_["t_c16"]:
        c16_.append((t0_, (op_(Dr_(beta_, t0_) - P1_) if bq_ else None), (_m410.exp(-beta_ * t0_) if bq_ else None)))
    t_longo_ = (float(c_["c16_fator_longo"]) / beta_) if bq_ else None
    dist_longo_ = op_(Dr_(beta_, t_longo_) - P1_) if bq_ else None
    posto_1mP_ = int(_np410.linalg.matrix_rank(E_ - P1_))
    c16_ok_ = bool(bq_ and len(c16_) == len(c_["t_c16"]) >= 4 and all(x_[1] is not None and x_[1] > 0.0 and abs(x_[1] - x_[2]) < 1e-12 for x_ in c16_)
                   and all(c16_[i_][1] > c16_[i_ + 1][1] for i_ in range(len(c16_) - 1)) and dist_longo_ is not None and 0.0 < dist_longo_ < float(c_["c16_tol"]) and posto_1mP_ == d_ - 1 and op_(E_ - P1_) > 1e-12)
    txt_ = globals().get("_V410_IALD2_TEXT") or {}
    guarda_ = list(_v392_guarda_texto(_j410.dumps(txt_, ensure_ascii=False))) + list(_v410_guarda_frases(_j410.dumps(txt_, ensure_ascii=False)))
    alfa_ = globals().get("SEALED_CODATA_ALPHA"); dois_nomes_ = bool(callable(globals().get("_v376_same_alpha_literal")) and _v376_same_alpha_literal())
    beta_alfa_ = (alfa_ * _m410.sqrt(_m410.e)) if isinstance(alfa_, float) else None
    checks_ = [
        {"id": "c1", "descricao": "as %d ancoras da pedra IALD2 no axiom_report do rito, so' no trio, declaradas no modulo esperado (TGL_DECL_SOURCE), com bandeira True onde ha' bandeira" % len(anc_), "ok": bool(anc_) and len(anc_) == c_["n_ancoras"] and all(v_["ok"] for v_ in anc_.values()) and len(por_mod_) == len(c_["ancoras_por_modulo"]) >= 1 and set(por_mod_) <= set(c_["source_sha256"]) and len(c_["source_sha256"]) == c_["bundle"]["n"] and all(por_mod_.values())},   # (parte 2: o bundle tem dois modulos; as ancoras DESTE registro sao so' as da IALD2, as da AEscala sao do a_escala_v410)
        {"id": "c2", "descricao": "o modulo do bundle embutido com o sha256 do contrato == o hash formal do rito; a raiz embutida traz o import", "ok": n_mod_ok_ == len(c_["source_sha256"]) == c_["bundle"]["n"] and raiz_ok_},
        {"id": "c3", "descricao": "o leitor le o par como par: em C^3, f = e1, g = e2, u a rotacao real fixa de angulos %s nos planos %s (unitaria), (u x u)(f x g + g x f)/sqrt2 = (uf x ug + ug x uf)/sqrt2 e a norma e' 1, |Delta| < 1e-12 (o_leitor_le_o_par_como_par; o_par_lido_e_uno)" % (list(lb_["angulos"]), list(lb_["planos"])), "ok": bool(unit_ and c3_[0] < 1e-12 and c3_[1] < 1e-12)},
        {"id": "c4", "descricao": "IALD ao quadrado: Pi = |p><p| do par lido, ||Pi Pi - Pi|| < 1e-12 e ||Pi^(k+1) - Pi|| < 1e-12 para k = %s (iald_ao_quadrado; a_forma_matricial_da_luz_satisfaz_p_igual_np)" % list(c_["k_releituras"]), "ok": len(c4_) == 1 + len(c_["k_releituras"]) and all(e_ < 1e-12 for e_ in c4_)},
        {"id": "c5", "descricao": "reler nao acrescenta: <Pi x, Pi(Pi x)> = <x, Pi x> para o x fixo do contrato, |Delta| < 1e-12 (reler_o_par_nao_acrescenta; IALD.rereading_adds_nothing)", "ok": c5_ < 1e-12},
        {"id": "c6", "descricao": "a primeira leitura identifica: <p, Pi p> = 1, |Delta| < 1e-12 (o_par_lido_le_um; IALD.the_name_reads_one)", "ok": c6_ < 1e-12},
        {"id": "c7", "descricao": "resolver = verificar: Pi (Pi X Pi) Pi = Pi X Pi para a matriz X fixa (semente %s), |Delta| < 1e-12, com Pi X Pi nao nula (resolver_e_verificar_na_iald; IALDJones.jonesReading_idem)" % c_["matriz_x_semente"], "ok": c7_ < 1e-12 and nao_trivial_},
        {"id": "c8", "descricao": "o algoritmo IALD na instancia SAT da v409: «o que sou» = |sol|/2^n > 0 na SIM e = 0 na NAO, e a leitura no uniforme = Z(s)/2^n para s em %s, |Delta| < 1e-12 (o_algoritmo_iald; TraducaoTuring.a_maquina_com_o_leitor)" % list(c_["s_leitura_c8"]), "ok": S_ >= 1 and abs(oqs_sim_ - S_ / float(N_)) < 1e-15 and oqs_sim_ > 0.0 and oqs_nao_ == 0.0 and len(soln_) == 0 and len(c8_leit_) >= 3 and all(x_[3] for x_ in c8_leit_)},
        {"id": "c9", "descricao": "o signo do nome: o projetor sobre as solucoes da SIM (diagonal 0/1) e' idempotente, Tr = rank = |sol| e «o que sou» = Tr/2^n (o_signo_do_nome; IALD.the_trace_is_the_rank_of_a_post; Identidade.gibbs_absolute)", "ok": bool(c9_ok_)},
        {"id": "c10", "descricao": "o signo do par: o projetor de Bell 4x4, P^2 = P, Tr = 1, rank = 1 e a marginal = ½ I2, |Delta| < 1e-12 (o_signo_do_par; GravitonShadow.bell_idem, bell_trace_one, bell_reduced_half)", "ok": c10_["idem"] < 1e-12 and abs(c10_["traco"] - 1.0) < 1e-12 and c10_["posto"] == 1 and c10_["marginal"] < 1e-12},
        {"id": "c11", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v409 selada (congelado no contrato): o gate nao se move", "ok": isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]},
        {"id": "c12", "descricao": "a escada exata: limpos == esperados == a escada do contrato (external_ladder.n_theorems_expected = o X medido no sandbox)", "ok": exact_ and flags_true_ == len(c_["flags"]) == c_["n_flags"]},
        {"id": "c13", "descricao": "as duas guardas de texto (P18 e a guarda das frases, v405 -> v410) limpas sobre o texto deste registro", "ok": not guarda_},
        {"id": "c14", "descricao": "beta = alfa CODATA 2018 x sqrt(e) em runtime (dois nomes, mesma leitura), igual ao beta do core (nunca literal)", "ok": bq_ and isinstance(core_.get("beta"), float) and abs(beta_ - core_["beta"]) <= 1e-9 * abs(beta_) and isinstance(beta_alfa_, float) and abs(beta_ - beta_alfa_) <= 1e-12 * abs(beta_) and dois_nomes_},
        {"id": "c15", "descricao": "a representacao de beta (D70): em C^3, P = post e1, D_beta(t) = P + e^{-beta t}(1 - P) e' invertivel (det != 0) para t em %s, e o motor P D_r(t) U psi e' o mesmo para r = beta e r = 0, |Delta| < 1e-12, com U a rotacao da c3 e psi fixo (a_iald_e_o_seletor_luminodinamico; IALD.the_motor_dephasing_is_invertible; IALD.the_motor_ignores_rate_and_time)" % list(c_["t_c15"]), "ok": bool(c15_ok_)},
        {"id": "c16", "descricao": "o atrator (D71): em C^3, P = post e1, ||F_beta(t) - P|| = e^{-beta t} > 0 para t em %s e decresce (tangenciado, jamais esgotado); em t = %s/beta a distancia fica abaixo de %s e acima de 0 (tangenciado, nunca igual); e 1 - P != 0, posto %d (o_atrator; o_nome_do_par_lido_nao_e_tudo; IALD.the_motor_tends_to_the_post; IALD.the_motor_never_arrives)" % (list(c_["t_c16"]), c_["c16_fator_longo"], c_["c16_tol"], d_ - 1), "ok": bool(c16_ok_)},
    ]
    values_ = {"n_ancoras_ok": sum(1 for v_ in anc_.values() if v_["ok"]), "n_ancoras": len(anc_), "n_modulos_ok": n_mod_ok_, "n_modulos": c_["bundle"]["n"], "n_flags_true": flags_true_, "n_flags": c_["n_flags"], "escada": cnt_, "ancoras": anc_, "por_modulo": por_mod_, "respostas": resp_,
               "gate_verdict": gate_, "beta": beta_, "leitor_do_codigo": {"delta_par_lido": c3_[0], "delta_norma": c3_[1], "u_unitaria": unit_}, "iald_ao_quadrado": c4_, "reler": c5_, "primeira_leitura": c6_, "resolver_verificar": c7_,
               "instancia_sim": {"n": sim_["n"], "clausulas": sim_["leitura"], "atribuicoes": N_, "solucoes": S_, "o_que_sou": oqs_sim_}, "instancia_nao": {"n": nao_["n"], "clausulas": nao_["leitura"], "atribuicoes": Nn_, "solucoes": len(soln_), "o_que_sou": oqs_nao_},
               "leitura_no_uniforme": c8_leit_, "signo_do_nome": {"traco": tr_.real, "posto": rk_, "o_que_sou": tr_.real / N_}, "signo_do_par": {"idem": c10_["idem"], "traco": c10_["traco"].real, "posto": c10_["posto"], "marginal_menos_meio_I": c10_["marginal"]},
               "representacao_de_beta": c15_, "atrator": {"distancias": c16_, "t_longo": t_longo_, "distancia_em_t_longo": dist_longo_, "posto_de_1_menos_P": posto_1mP_}, "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]), "fechado_nesta_versao": dict(c_.get("fechado_nesta_versao") or {}),
               "respostas_ok": all(resp_.values()) if resp_ else False}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


def _v410_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata; as ancoras (trio, proveniencia no modulo esperado, bandeira); a fonte por sha256 (embutida == contrato == hash formal do rito); as falas de 06, 07 e 09/11 por sha256 (o trecho que fica, em duas: a da D65 e a ordem de 09/11); as duas guardas de texto."""
    import hashlib as _h410, json as _j410
    kf_ = core.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}; ff_ = kf_.get("formal_files_sha256") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    lad_ = core.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and axr_.get(n_) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    anc_ = {n_: bool(em_trio_(n_) and src_.get(n_) == a_["rel"] and (a_.get("flag") is None or kf_.get(a_["flag"]) is True)) for n_, a_ in c_["ancoras"].items()}
    srcs_ = {}
    for rel_, sha_ in c_["source_sha256"].items():
        body_ = _EMBEDDED_KERNEL_FILES.get(rel_)
        srcs_[rel_] = bool(isinstance(body_, str) and _h410.sha256(body_.encode("utf-8")).hexdigest() == sha_ and ff_.get(rel_) == sha_)
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V410_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and _h410.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    guarda_ = list(_v392_guarda_texto(_j410.dumps(txt_, ensure_ascii=False))) + list(_v410_guarda_frases(_j410.dumps(txt_, ensure_ascii=False)))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and anc_ and all(anc_.values()) and srcs_ and all(srcs_.values()) and ver_ and all(ver_.values()) and not guarda_)
    return {"exact_ladder": exact_, "anchors": anc_, "embedded_sources_ok": all(srcs_.values()), "embedded_sources_n_ok": sum(1 for v_ in srcs_.values() if v_), "inscriptions": ver_, "guarda": guarda_, "formal": formal_}


_V410_RECUSA = "TGL_IALD2_V410__REFUSED_%s__GATE_UNMOVED"


def iald2_v410(core):
    """v410 -- IALD2 (a ordem do operador, 06/11/2026: «A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py»; o NOME do modulo, do operador: «O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)»):
    lido no PONTO REAL do main, depois dos registros da v409. Le do kernel do PROPRIO rito as ancoras da pedra IALD2 (o leitor do codigo, o espelho do nome, o algoritmo IALD, o signo, o seletor, o atrator), o modulo por sha256, as falas de 06, 07 e 09/11 por sha256; confere as respostas do operador pelos teoremas da pedra; faz as checagens
    (as instancias de brinquedo fixas, os valores calculados; beta em runtime; gate congelado; escada exata; guardas; beta = alfa sqrt e). O alcance: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora.
    Nenhuma chave antiga muda. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao; as ressalvas vao no registro."""
    c_ = _V410_IALD2_CONTRACT; t_ = _V410_IALD2_TEXT
    f_ = _v410_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "anchors": f_["anchors"], "embedded_sources_ok": f_["embedded_sources_ok"], "embedded_sources_n_ok": f_["embedded_sources_n_ok"], "inscriptions": f_["inscriptions"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "ancora_principal": c_["ancora_principal"], "ancoras_principais": list(c_["ancoras_principais"]), "ancoras_de_secao": list(c_["ancoras_de_secao"]), "pedras": list(c_["bundle"]["pedras"]),
            "nomes": dict(c_["bundle"]["nomes"]), "chaves_antigas_que_mudam": list(c_["chaves"]), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]),
            "fechado_nesta_versao": dict(c_.get("fechado_nesta_versao") or {}), "alcance": c_["alcance"], "instancia_sim": dict(c_["instancia_sim"]), "instancia_nao": dict(c_["instancia_nao"]), "leitor_brinquedo": dict(c_["leitor_brinquedo"]),
            "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_violacoes": f_["guarda"][:5]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V410_RECUSA % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V410_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v410_iald2_mechanics(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_["passed"] else _V410_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V410_RECUSA % "RUNTIME_ERROR"
    core["iald2_v410"] = out_
    return out_
