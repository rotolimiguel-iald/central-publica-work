# ====================== v405 (01/11/2026) -- A MASSA DERIVADA E A IDENTIDADE DEFINIDA: as oito pedras com os nomes do operador (Ponte da Massa; Massa = tensao pura; Identidade; Observador = terminal; Lei do diminuto; Tonica do Hamiltoniano; Disco de Euler; Ponto Zero do Psion), os oito registros com FUNCAO (lidos no ponto do rito depois dos tres registros da v404), as falas de 30/10 a 01/11 e o ensaio «A identidade», as decisoes da gerencia e os registros por spec cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405 e kh_n1_cobertura_v405.
# A errata E10 do angulo do neutrino vai AO LADO (o texto antigo e a errata E7 da v404 ficam no registro); a unidade u = 1 eV e' o Um POSTO; alfa e' medida, nunca derivada; o numero da massa nao muda. Os contratos (_V405_CONTRACTS) e as falas (_V405_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. O gate nao se move.
# ---- v405: A MASSA DERIVADA E A IDENTIDADE DEFINIDA -- as OITO pedras com os nomes do operador (Ponte da Massa; Massa = tensao pura; Identidade; Observador = terminal; Lei do diminuto; Tonica do Hamiltoniano; Disco de Euler; Ponto Zero do Psion). OITO registros PEQUENOS, com FUNCAO, lidos no ponto real do main,
# logo depois dos registros de pedra da v404 (projecao transversal e jo8v32): cada um le do kernel do PROPRIO rito a composicao da pedra (bandeira True, trio, proveniencia no modulo da pedra), os teoremas do contrato e os termos antigos que ela cita, a fonte da pedra por sha256, as falas de 30/10 a 01/11 por sha256
# e um TEXTO-CONTEXTO do kernel embutido, e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal), um modelo honesto da pedra. A MOLDURA (errata da gerencia c1, 01/11/2026): os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo para a DEFINICAO; a leitura fisica nao virou teorema.
# Entram um Um posto (u = 1 eV, decisao do operador de 31/10/2026, nunca derivado), uma alfa MEDIDA por dentro (nunca derivada) e as leituras do operador (massaDerivada; theta = pi/4 escrito em transicaoDerivada; a tonica (beta/alfa).u; R = beta.u^2); dadas essas entradas, a FORMA e' teorema.
# O numero da massa do neutrino NAO muda (beta.sen45.u, o mesmo da v404, relido a 1e-12 contra neutrino_mass.m_nu_meV); o veredito do canal do neutrino NAO muda; a errata E10 do angle_status vai AO LADO (o texto antigo e a errata E7 da v404 ficam). As leituras do operador sao [INPUT/ONTO], nao termos de kernel. O gate nao se move.
# Fonte autoral deste bloco: runtime_v405.py (cadeia_de_selo/v405); os contratos (_V405_CONTRACTS) e as falas (_V405_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados.
import math as _m405


def _v405_guarda_frases(txt_):
    """v405 -- a GUARDA DAS FRASES que afirmam demais (ordem da gerencia c1, 01/11/2026; molde: _v392_guarda_texto): reprova, em texto NOVO da gerencia, as frases proibidas, em portugues (com e sem acento), em ingles e como token de veredito. A fala do operador nao passa por aqui: ela e' verbatim e fica como registro (a cadeia retira, antes, os trechos citados). Identificador Lean de teorema rebatizado (com sublinhado, em minusculas) e' citacao da errata, nao frase. Devolve a lista de violacoes [(regra, trecho)]."""
    import re as _re
    regras_ = [("F1_tudo_e_teorema", _re.compile(r"\btudo\s+(?:e'?|é|eh|sao|são)\s+teorema|\beverything\s+is\s+(?:a\s+)?theorem", _re.I)),
               ("F2_tudo_derivado", _re.compile(r"\btudo\s+(?:\w+\s+)?derivad[oa]\b|\beverything\s+(?:\w+\s+)?derived\b", _re.I)),
               ("F3_nenhuma_hipotese", _re.compile(r"\bnenhuma\s+hip(?:ó|o)tese\s+resta|\bno\s+hypothes[ie]s\s+remains?\b", _re.I)),
               ("F4_hipoteses_descarregadas", _re.compile(r"\bhip(?:ó|o)teses(?:\s+\w+)?\s+descarregadas|\bhypothes[ie]s(?:\s+\w+)?\s+(?:are\s+|were\s+)?discharged\b", _re.I)),
               ("F6_a_frase_do_no_go", _re.compile(r"\ba\s+liberdade(?:\s+de\s+escala)?\s+passa\b|\ba\s+t(?:ô|o)nica\s+(?:segue|fica|permanece)\s+livre\b|\bo\s+no-go\s+se\s+levanta\b|\blevanta(?:r)?\s+o\s+no-go\b|\bthe\s+freedom(?:\s+of\s+scale)?\s+(?:passes|moves)\b|\bthe\s+tonic\s+(?:stays|remains)\s+free\b|\bthe\s+no-go\s+(?:is\s+lifted|lifts)\b|\blifts?\s+the\s+no-go\b", _re.I)),
               ("F7_tau_e_kappa_nao_derivados", _re.compile(r"(?:τ★|τ\*|tau\*|tau_star)\s+(?:foi|e'|é|esta|está|ficou)\s+derivad[oa]|\bderiv(?:a|ou|ar|amos)\s+(?:o\s+)?(?:τ★|τ\*|tau\*)|(?:κ|\bkappa)\s+(?:foi|e'|é|esta|está|ficou)\s+derivad[oa]|\bderiv(?:a|ou|ar|amos)\s+(?:o\s+)?(?:κ|kappa)\b|(?:τ★|tau\*|κ|\bkappa)\s+(?:was|is)\s+derived|\bderived?\s+(?:τ★|tau\*|κ|kappa)\b", _re.I)),
               ("F8_a_escala_nao_e_a_transposicao", _re.compile(r"mant(?:endo|em|ém)\s+a\s+escala[^.;]{0,90}transp|a\s+escala\s+mantida[^.;]{0,90}transp|transp[^.;]{0,90}mant(?:endo|em|ém)\s+a\s+escala|transp[^.;]{0,90}a\s+escala\s+mantida|the\s+kept\s+scale[^.;]{0,90}transp|keeping\s+the\s+scale[^.;]{0,90}transp|transp[^.;]{0,90}(?:keeps?|keeping)\s+the\s+scale|\ba\s+escala\s+(?:e'|é)\s+(?:exatamente\s+)?o\s+invariante\s+da\s+transposi", _re.I)),
               ("F10_a_razao_nao_e_a_escala", _re.compile(r"\braz(?:ão|ao|ões|oes)(?:\s+[àa]\s+t(?:ô|o)nica)?\s+(?:e'|é|sao|são)\s+(?:a\s+)?escala\b|\ba\s+escala\s+(?:do\s+acorde\s*)?(?:e'|é|:)\s+(?:a\s+|as\s+)?raz(?:ão|ao|ões|oes)\s+(?:de\s+cada|[àa]\s+(?:t(?:ô|o)nica|nota\s+principal))|\bthe\s+ratios?\s+(?:is|are)\s+the\s+scale\b", _re.I)),
               ("F11_o_diminuto_nao_muda_a_escala", _re.compile(r"\b(?:o\s+diminuto|a\s+modula(?:ç|c)(?:ã|a)o|o\s+mei[oa]-tom)\s+(?:muda|altera|quebra|desloca)\s+(?:toda\s+)?a\s+escala\b|\bthe\s+(?:diminished|modulation|half\s+tone)\s+(?:changes|alters|breaks|shifts)\s+the\s+scale\b", _re.I)),
               ("F12_valor_absoluto_nao_e_escala", _re.compile(r"\bescalas?\s+(?:absoluta|relativa)s?\b|\b(?:absolute|relative)\s+scales?\b", _re.I)),
               ("F13_delta_nao_e_gap", _re.compile(r"\bgap(?:\s+espectral)?\s*(?:e'|é|eh|is|=|:|,|de|of|vale|equals)?\s*(?:a\s+|the\s+)?(?:[`$*\\]*(?:Δ|Delta)\b|energia\s+retida|retained\s+energy|(?:β|beta)\s*[·.*]\s*u\b|12[,.]03)|(?:Δ|\bDelta|energia\s+retida|retained\s+energy|(?:β|\bbeta)\s*[·.*]\s*u|12[,.]03\d*\s*meV)[`$*]*\s*,?\s*(?:e'|é|eh|is|=|:|como|as)\s*(?:o\s+|the\s+|um\s+|a\s+)?gap\b|\bgap\s+(?:lido|lida|read)\s+(?:do|no|from|at)\s+(?:the\s+)?(?:[âa]ngulo|angle)|\btempo\s+do\s+gap\b|\btime\s+of\s+the\s+gap\b|tempoDoGap|DELTA_IS_THE_GAP|THE_GAP_IS_DELTA|TIME_OF_THE_GAP|GAP_READ_FROM", _re.I)),
               ("F14_o_tom_nao_tem_termo", _re.compile(r"\ba\s+escala\s+e\s+o\s+tom\s+ficam\b|\bmantendo\s+a\s+escala\s+e\s+o\s+tom\b|\bthe\s+scale\s+and\s+the\s+key\s+stay\b", _re.I)),
               ("F5_token_de_veredito", _re.compile(r"TUDO_DERIVADO|TUDO_E_TEOREMA|EVERYTHING_(?:IS_)?DERIVED|EVERYTHING_IS_A_THEOREM|NENHUMA_HIPOTESE_RESTA|NO_HYPOTHES[EI]S?_REMAINS?|HYPOTHES[EI]S_(?:ARE_|WERE_)?DISCHARGED|HIPOTESES_(?:\w+_)?DESCARREGADAS|THE_TONIC_(?:STAYS|REMAINS)_FREE|NO_GO_(?:IS_)?LIFTED|(?:ABSOLUTE|RELATIVE)_SCALE"))]
    out_ = []
    for nome_, rx_ in regras_:
        for m_ in rx_.finditer(str(txt_)):
            out_.append((nome_, str(txt_)[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"\bgap\b[^.;\n]{0,60}12[,.]03|12[,.]03\d*\s*meV[^.;\n]{0,60}\bgap\b", str(txt_), _re.I):   # 12,03 meV e' o valor esperado do lock no angulo de Miguel, nao o gap (errata R7): a mencao so' passa dita como negacao
        volta_ = str(txt_)[max(0, m_.start() - 30):m_.end() + 30].lower()
        if not any(n_ in volta_ for n_ in ("não", "nao", "not ")):
            out_.append(("F13_delta_nao_e_gap", str(txt_)[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    for m_ in _re.finditer(r"(?:κ|kappa)\s*=\s*F\(", str(txt_), _re.I):   # kappa e' testemunha (regra do operador de 24/08/2026): a formula so' aparece dita como proibida
        volta_ = str(txt_)[max(0, m_.start() - 140):m_.end() + 140].lower()
        if "proibid" not in volta_ and "forbidden" not in volta_:
            out_.append(("F9_kappa_como_objetivo_de_busca", str(txt_)[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    return out_


def _v405_ensaio_tex(txt_):
    """v405 -- o ensaio em LaTeX: o TEXTO nao muda; so' as letras gregas e a raiz, que o preambulo do artigo nao declara, viram as formas de LaTeX (a mesma letra no PDF), e os especiais de LaTeX sao escapados; paragrafos por linha em branco. Devolve a lista: o primeiro item e' o titulo do ensaio."""
    b_ = chr(92)
    m_ = {b_: b_ + "textbackslash{}", "{": b_ + "{", "}": b_ + "}", "%": b_ + "%", "&": b_ + "&", "#": b_ + "#", "_": b_ + "_", "$": b_ + "$", "~": b_ + "textasciitilde{}", "^": b_ + "textasciicircum{}", "α": "$" + b_ + "alpha$", "β": "$" + b_ + "beta$", "√": "$" + b_ + "surd$"}   # (o ² e o · o preambulo do artigo aceita como estao: ficam os mesmos caracteres no PDF e no .txt)
    return [p_.strip() for p_ in "".join(m_.get(c_, c_) for c_ in txt_).replace("$" + b_ + "surd$e", "$" + b_ + "sqrt{e}$").split("\n\n") if p_.strip()]


def _v405_close(a_, b_, e_=1e-11):
    return abs(a_ - b_) <= e_ * (1.0 + abs(a_) + abs(b_))


def _v405_rel(a_, b_):
    """diferenca relativa |a/b - 1| (inf se b nao e' numero ou e' zero)."""
    try:
        return abs(float(a_) / float(b_) - 1.0) if float(b_) != 0.0 else float("inf")
    except (TypeError, ValueError, ZeroDivisionError):
        return float("inf")


def _v405_mat_trace(A_):
    return sum(A_[i_][i_] for i_ in range(len(A_)))


def _v405_mat_mul(A_, B_):
    n_ = len(A_)
    return [[sum(A_[i_][k_] * B_[k_][j_] for k_ in range(n_)) for j_ in range(n_)] for i_ in range(n_)]


def _v405_mat_dagger(A_):
    n_ = len(A_)
    return [[A_[j_][i_].conjugate() for j_ in range(n_)] for i_ in range(n_)]


def _v405_mat_eye(n_, s_=1.0):
    return [[(complex(s_) if i_ == j_ else 0j) for j_ in range(n_)] for i_ in range(n_)]


def _v405_mat_sub(A_, B_):
    n_ = len(A_)
    return [[A_[i_][j_] - B_[i_][j_] for j_ in range(n_)] for i_ in range(n_)]


def _v405_mat_norm(A_):
    return _m405.sqrt(sum(abs(x_) ** 2 for r_ in A_ for x_ in r_))


def _v405_rot_projector(n_, k_, th_):
    """um NOME (projecao ortogonal de posto k em dimensao n) fora da base canonica: Q.diag(1..1,0..0).Q^dagger com Q uma rotacao real no plano (0, n-1) de angulo th_ (k = 0 e' o vazio; k = n e' o Um)."""
    D_ = [[(1 + 0j if (i_ == j_ and i_ < k_) else 0j) for j_ in range(n_)] for i_ in range(n_)]
    Q_ = _v405_mat_eye(n_)
    c_, s_ = _m405.cos(th_), _m405.sin(th_)
    if n_ >= 2:
        Q_[0][0], Q_[0][n_ - 1], Q_[n_ - 1][0], Q_[n_ - 1][n_ - 1] = complex(c_), complex(-s_), complex(s_), complex(c_)
    return _v405_mat_mul(_v405_mat_mul(Q_, D_), _v405_mat_dagger(Q_))


def v405_ponte_mechanics(beta_, core_, c_):
    """v405 -- a mecanica da PONTE DA MASSA em dupla precisao: a projecao transversal e a sua derivada coincidem so' em pi/4; a energia retida e' beta.u e nada se perde na fronteira; sob a leitura massaDerivada, a massa E' a forma do neutrino do programa (relida a 1e-12);
    o discriminante sqrt2 entre as leituras proporcional e derivada; o controle negativo fora do ponto fixo; os CAMPOS FECHADOS (a face absoluta pesa 1/2 para toda graduacao de paridade de traco nulo, teorema; o angulo pi/4 e' ESCRITO em transicaoDerivada e tem o mesmo valor: coincidencia de valor, nao ponte; a unidade e' o Um POSTO);
    e a errata AO LADO (o canal do neutrino intacto; o registro da v404 concorda). beta recebido (o chamador o calcula em runtime: alfa CODATA x sqrt(e); NUNCA literal). Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "p0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["constants"]["u_posto_eV"])
    s4_, c4_ = _m405.sin(_m405.pi / 4.0), _m405.cos(_m405.pi / 4.0)
    n4_ = 20000
    th_ = [k_ * (_m405.pi / 2.0) / n4_ for k_ in range(n4_ + 1)]
    iguais_ = [k_ for k_, t_ in enumerate(th_) if abs(_m405.sin(t_) - _m405.cos(t_)) <= 1e-12]
    ck_("p1", "★★ projecao_hasDerivAt, deriv_eq_projecao_at_half e projecao_eq_deriv_iff: a derivada de sen e' cos (diferenca central, h = 1e-6, |erro| <= 1e-9 em seis pontos); em pi/4 a projecao E' a sua derivada (|cos(pi/4) - sen(pi/4)| <= 1e-15); e em [0, pi/2] (20001 pontos) sen = cos SO' no ponto do meio, pi/4",
        all(abs((_m405.sin(t_ + 1e-6) - _m405.sin(t_ - 1e-6)) / 2e-6 - _m405.cos(t_)) <= 1e-9 for t_ in (0.1, 0.3, 0.7, _m405.pi / 4.0, 1.2, 1.5)) and abs(c4_ - s4_) <= 1e-15 and iguais_ == [n4_ // 2] and abs(th_[n4_ // 2] - _m405.pi / 4.0) <= 1e-15, [c4_ - s4_, iguais_])
    thm_ = _m405.asin(_m405.sqrt(beta_))
    retida_, transm_ = _m405.sin(thm_) ** 2 * u_, _m405.cos(thm_) ** 2 * u_
    ck_("p2", "★ energia_retida_eq e retida_add_transmitida: com theta_M = arcsin(raiz de beta) (Teorema S-d), o retido e' beta.u (|erro| <= 1e-15 relativo) e retido + transmitido = u (nada se perde na fronteira)",
        _v405_rel(retida_, beta_ * u_) <= 1e-15 and abs(retida_ + transm_ - u_) <= 1e-15 * (1.0 + u_), [retida_, transm_])
    m_der_ = retida_ * c4_                      # massaDerivada = energiaRetida x deriv(sen)(pi/4) = beta.u.cos(pi/4)
    m_form_ = beta_ * s4_ * u_                  # neutrinoMassForm c u = beta.sen45.u
    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    ck_("p3", "★★★ massa_derivada_eq_form (A PONTE, sob a leitura massaDerivada, que e' definicao [ONTO]): a massa como derivada da projecao transversal no ponto autoconjugado, beta.u.cos(pi/4), E' a forma do neutrino do programa beta.sen45.u (|erro| <= 1e-15 relativo), e o m_nu do programa (neutrino_mass.m_nu_meV) e' essa forma em meV a 1e-12 relativo (u = 1 eV POSTO)",
        _v405_rel(m_der_, m_form_) <= 1e-15 and isinstance(m_core_, float) and _v405_rel(m_form_ * 1000.0, m_core_) <= float(c_["constants"]["rel_tol"]), [m_der_ * 1000.0, m_core_])
    m_prop_ = retida_ * s4_ ** 2
    ck_("p4", "★★ massa_derivada_eq_sqrt_two_mul_proporcional e massa_proporcional_ne_derivada (o discriminante): a leitura «proporcional» (peso sen^2) difere da «derivada» exatamente por sqrt2 (|erro| <= 1e-15 relativo) e as duas NAO coincidem; a diferenca em meV e' o que o dado distingue",
        _v405_rel(m_der_, _m405.sqrt(2.0) * m_prop_) <= 1e-15 and abs(m_der_ - m_prop_) > 1e-6 * m_der_, [m_der_ * 1000.0, m_prop_ * 1000.0])
    fora_ = [t_ for t_ in th_ if abs(_m405.sin(t_) ** 2 - 0.5) > 1e-9]
    ck_("p5", "★ controle_nao_autoconjugado: em todo angulo da grade cujo peso transversal NAO e' 1/2 (20000 pontos), projecao e derivada NAO coincidem (|sen - cos| > 1e-12): a ponte nao e' generica, e' do ponto fixo",
        len(fora_) == n4_ and all(abs(_m405.sin(t_) - _m405.cos(t_)) > 1e-12 for t_ in fora_), [len(fora_)])
    # os campos fechados: a face absoluta (gibbs(1/n)((1/2)(1 + Gamma)) com Tr Gamma = 0) pesa 1/2 em dimensao 2, 3, 4 e 5, para Gamma = diag(n-1, -1, ..., -1) (diagonal, de traco nulo; so' o traco importa aqui; para n >= 3 ela nao e' involutiva); o angulo com sen^2 = 1/2 em [0, pi/2] e' pi/4; a unidade posta u = 1 da m = beta.sqrt2/2
    faces_ = []
    for n_ in (2, 3, 4, 5):
        G_ = _v405_mat_sub(_v405_mat_eye(n_, 2.0), _v405_mat_eye(n_))              # Gamma0 = diag(1, ..., 1) tem traco n: corrige-se para traco zero abaixo
        G_ = [[(G_[i_][j_] - (complex(1.0) if i_ == j_ else 0j)) for j_ in range(n_)] for i_ in range(n_)]   # agora Gamma0 = 0
        G_[0][0] = complex(n_ - 1);
        for i_ in range(1, n_):
            G_[i_][i_] = complex(-1.0)                                              # Gamma = diag(n - 1, -1, ..., -1): traco zero
        face_ = [[0.5 * ((1.0 if i_ == j_ else 0.0) + G_[i_][j_]) for j_ in range(n_)] for i_ in range(n_)]
        rho_ = _v405_mat_eye(n_, 1.0 / n_)
        faces_.append((n_, _v405_mat_trace(_v405_mat_mul(rho_, face_)).real, _v405_mat_trace(G_).real))
    ck_("p6", "★★ peso_da_face_absoluta, transicao_derivada_le_o_absoluto e a_transicao_existe_para_todo_acoplamento (OS CAMPOS FECHADOS): no estado absoluto rho = 1/n (n = 2, 3, 4, 5) o peso da face (1/2)(1 + Gamma) com Tr Gamma = 0 e' exatamente 1/2 (|erro| <= 1e-15): teorema; o angulo pi/4 ESCRITO em transicaoDerivada tem sen^2 = 1/2, o mesmo valor: coincidencia de valor, nao ponte (a ponte e' a leitura do operador); "
                "e no Um POSTO (u = 1) a transicao construida da m = beta.sqrt2/2 (|erro| <= 1e-15 relativo): a FORMA, dadas as leituras",
        all(abs(w_ - 0.5) <= 1e-15 and abs(tr_) <= 1e-15 for _, w_, tr_ in faces_) and abs(_m405.sin(_m405.pi / 4.0) ** 2 - 0.5) <= 1e-15 and _v405_rel(beta_ * 1.0 * c4_, beta_ * (_m405.sqrt(2.0) / 2.0)) <= 1e-15, [[n_, w_] for n_, w_, _ in faces_])
    nm_ = core_.get("neutrino_mass") or {}
    ang_ = str(nm_.get("angle_status") or "")
    pv4_ = (core_.get("projecao_transversal_v404") or {}).get("values") or {}
    import hashlib as _hl405
    ck_("p7", "a errata E10 e' AO LADO: o angle_status do programa (neutrino_mass) segue com o texto ANTIGO (comeca por «sin(45deg) e POSTULADO», sha256 do texto inteiro == o da v404 selada), o frozen_hash da regra de decisao e o veredito do canal NAO se moveram, o m_nu e' o da v404 a 1e-12 relativo, "
                "e o registro projecao_transversal_v404 (recriado neste rito) concorda com esta pedra: o mesmo m_nu em meV a 1e-12 relativo (a forma e o numero sao os mesmos)",
        ang_.startswith(c_["neutrino"]["angle_status_antigo_prefixo"]) and _hl405.sha256(ang_.encode("utf-8")).hexdigest() == c_["neutrino"]["angle_status_antigo_sha256"] and nm_.get("frozen_hash") == c_["neutrino"]["frozen_hash_v404"] and nm_.get("verdict") == c_["neutrino"]["verdict_v404"]
        and isinstance(m_core_, float) and _v405_rel(m_core_, float(c_["neutrino"]["m_nu_meV_v404"])) <= 1e-12 and isinstance(pv4_.get("m_nu_meV_runtime"), float) and _v405_rel(pv4_.get("m_nu_meV_runtime"), m_form_ * 1000.0) <= 1e-12, [nm_.get("verdict"), pv4_.get("m_nu_meV_runtime")])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "theta_M": thm_, "sin_pi_over_4": s4_, "cos_pi_over_4": c4_, "energia_retida_eV": retida_, "energia_transmitida_eV": transm_, "m_derivada_meV": m_der_ * 1000.0, "m_proporcional_meV": m_prop_ * 1000.0,
             "m_forma_meV": m_form_ * 1000.0, "m_nu_meV_core": m_core_, "m_nu_rel_diff": _v405_rel(m_form_ * 1000.0, m_core_), "razao_derivada_sobre_proporcional": (m_der_ / m_prop_) if m_prop_ else None, "faces_absolutas_peso": [[n_, w_] for n_, w_, _ in faces_],
             "grid_angles": n4_ + 1, "angulos_onde_sen_igual_cos": iguais_, "m_no_um_posto_meV": beta_ * c4_ * 1000.0}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_tensao_mechanics(beta_, core_, c_):
    """v405 -- a mecanica de MASSA = TENSAO PURA (o emprestimo da massa): a massa e' o produto do acoplamento; o foton (b = 0) nao tem massa e tudo atravessa; a massa e' o residuo; o emprestimo CONSTRUIDO (uma volta kappa.P = 2pi, o periodo fiel e' teorema; a parcela nunca quita e e' no maximo beta.g.P);
    a area por volta eta(a+c) = 2pi.massa = sqrt2.pi.beta.u; e massa_e_tensao_pura: o principal e' a energia RETIDA (beta.u) projetada no transversal, identidade algebrica sob a leitura massaDerivada; o nome e' do operador e a leitura e' [ONTO]. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "t0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["constants"]["u_posto_eV"]); r2_ = _m405.sqrt(2.0) / 2.0
    massa_ = lambda b_, e_: b_ * r2_ * e_
    transm_ = lambda b_, e_: (1.0 - b_) * e_
    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    ck_("t1", "★ massa_e_produto_do_acoplamento: a massa da ponte e' beta.(sqrt2/2).u -- o acoplamento vezes a projecao transversal da energia inscrita -- e e' o m_nu do programa a 1e-12 relativo (u = 1 eV POSTO)",
        isinstance(m_core_, float) and _v405_rel(massa_(beta_, u_) * 1000.0, m_core_) <= float(c_["constants"]["rel_tol"]), [massa_(beta_, u_) * 1000.0, m_core_])
    ck_("t2", "★★ foton_sem_massa e acoplamento_positivo_da_massa: com acoplamento zero a massa e' 0 e toda a energia atravessa (transmitida = u); com acoplamento positivo (beta do rito, e 0,1, 0,5, 0,9) a massa e' > 0 e a transmissao e' estritamente menor que o incidente",
        massa_(0.0, u_) == 0.0 and transm_(0.0, u_) == u_ and all(massa_(b_, u_) > 0.0 and transm_(b_, u_) < u_ for b_ in (beta_, 0.1, 0.5, 0.9)), [massa_(0.0, u_), transm_(0.0, u_)])
    ck_("t3", "★ massa_e_o_residuo: a massa e' o incidente menos o transmitido, lido na projecao transversal -- (u - transmitida).sqrt2/2 (|erro| <= 1e-15 relativo) -- o que fica depois da peneira",
        _v405_rel(massa_(beta_, u_), (u_ - transm_(beta_, u_)) * r2_) <= 1e-15, [(u_ - transm_(beta_, u_)) * r2_])
    emp_ = []
    for kap_ in (0.5, 1.0, 2.0, 10.0):
        P_ = 2.0 * _m405.pi / kap_
        for g_ in (0.25, 1.0, 3.0):
            parc_ = 1.0 - _m405.exp(-(P_ * beta_ * g_))
            emp_.append({"kappa": kap_, "g": g_, "P": P_, "kP": kap_ * P_, "parcela": parc_, "teto": beta_ * g_ * P_, "teto_kappa": beta_ * 2.0 * _m405.pi * g_ / kap_})
    ck_("t4", "★★ emprestimoDerivado, emprestimo_derivado_uma_volta, parcela_derivada_nunca_quita, parcela_le_beta e parcela_le_beta': com P = 2pi/kappa (o periodo fiel e' teorema, nao campo), kappa.P = 2pi (|erro| <= 1e-12); a parcela de uma volta, 1 - e^(-P.beta.g), fica em (0, 1) e e' no maximo beta.g.P = beta.2pi.g/kappa, "
                "para kappa em {0,5; 1; 2; 10} e g em {0,25; 1; 3}: uma volta nao quita; para qualquer tempo finito o termo do kernel e' the_charge_never_completes",
        all(abs(e_["kP"] - 2.0 * _m405.pi) <= 1e-12 and 0.0 < e_["parcela"] < 1.0 and e_["parcela"] <= e_["teto"] + 1e-15 and abs(e_["teto"] - e_["teto_kappa"]) <= 1e-12 for e_ in emp_), [[round(e_["parcela"], 6) for e_ in emp_[:4]]])
    area_ = 2.0 * _m405.pi * massa_(beta_, u_)
    ck_("t5", "★★ volta_paga_area e area_por_volta_da_massa_inscrita (a segunda ponte): uma volta inteira (2pi) da massa paga eta(a+c) = 2pi.massa, logo eta(a+c) = sqrt2.pi.beta.u (|erro| <= 1e-15 relativo); a massa e' a diferenca de area por radiano de volta",
        _v405_rel(area_, _m405.sqrt(2.0) * _m405.pi * beta_ * u_) <= 1e-15, [area_])
    thm_ = _m405.asin(_m405.sqrt(beta_)); retida_ = _m405.sin(thm_) ** 2 * u_
    src_ = (core_.get("kernel_formalization") or {}).get("declaration_sources_v394") or {}
    lig_ = {n_: (src_.get(n_) == p_) for n_, p_ in c_["cited_outside"].items()}
    novos_ = [n_ for n_, p_ in src_.items() if p_ in c_["modulos_novos"]]
    magn_ = [n_ for n_ in novos_ if "magnet" in n_.lower()]
    ck_("t6", "★★★ massa_e_tensao_pura (sob a leitura massaDerivada [ONTO]): o principal do emprestimo construido e' a ENERGIA RETIDA pela fronteira (beta.u, o que fica tenso, sem parcela transmitida) projetada no transversal (|erro| <= 1e-15 relativo); e a ligacao que falta e' dita: tensao (frameCovectorStress), atrito (viscosity_is_the_constant_friction) "
                "e temperatura (reciprocal_temperature) TEM termo no kernel do rito (proveniencia lida), e NENHUM termo de magnetismo existe nos oito modulos novos [OPEN]",
        _v405_rel(massa_(beta_, u_), retida_ * r2_) <= 1e-15 and all(lig_.values()) and len(lig_) == 3 and magn_ == [], [list(lig_), len(novos_)])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "massa_meV": massa_(beta_, u_) * 1000.0, "m_nu_meV_core": m_core_, "transmitida_eV": transm_(beta_, u_), "retida_eV": retida_, "area_por_volta": area_, "emprestimo_amostra": emp_[:4], "n_amostras_emprestimo": len(emp_),
             "ligacao_que_falta_termos_no_kernel": lig_, "termos_de_magnetismo_nos_modulos_novos": len(magn_), "declaracoes_nos_modulos_novos": len(novos_)}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_identidade_mechanics(beta_, core_, c_):
    """v405 -- a mecanica da IDENTIDADE em matrizes pequenas (n = 2, 3, 4; aritmetica complexa pura, sem biblioteca): um fato sobre projecoes no estado traco normalizado (que esse fato SEJA a identidade e' a leitura do operador [INPUT/ONTO], tipada como modelo). No referencial absoluto rho = 1/n, EU SOU = omega(1) = 1; o Um se reparte entre o nome e o resto; o «senao» e a selecao unica (nada resta <=> P = 1);
    forma = conteudo so' nos dois pontos fixos (o vazio e o Um); os controles negativos (o vazio e a face pesam 0 e 1/2, nao 1); coisa julgada (reler nao acrescenta) e o reflexo verdadeiro (P^dagger = P). Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "i0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    omega_ = lambda n_, A_: _v405_mat_trace(_v405_mat_mul(_v405_mat_eye(n_, 1.0 / n_), A_))
    dims_ = (2, 3, 4)
    eu_sou_ = {n_: omega_(n_, _v405_mat_eye(n_)) for n_ in dims_}
    ck_("i1", "★ euSou_eq_one e gibbs_absolute: no referencial absoluto rho = 1/n (o Gibbs do Hamiltoniano nulo; n = 2, 3, 4), EU SOU = omega(1) = tr(1)/n = 1 exatamente, e omega(a) = tr(a)/n",
        all(abs(eu_sou_[n_] - 1.0) <= 1e-15 for n_ in dims_), {str(n_): eu_sou_[n_].real for n_ in dims_})
    rep_, senao_, sel_, forma_, jul_ = [], [], [], [], []
    for n_ in dims_:
        for k_ in range(0, n_ + 1):
            P_ = _v405_rot_projector(n_, k_, 0.7)                     # um NOME fora da base canonica: reflexo verdadeiro (P^dagger = P) e releitura (P.P = P)
            I_ = _v405_mat_eye(n_); R_ = _v405_mat_sub(I_, P_)
            oq_, resto_ = omega_(n_, P_), omega_(n_, R_)
            rep_.append(abs(eu_sou_[n_] - (oq_ + resto_)))
            fiel_ = _v405_mat_norm(_v405_mat_sub(P_, I_)) <= 1e-12
            senao_.append((abs(eu_sou_[n_] - oq_) <= 1e-12) == (abs(resto_) <= 1e-12))
            sel_.append((abs(resto_) <= 1e-12) == fiel_)
            FC_ = _v405_mat_norm(_v405_mat_sub(P_, [[oq_ * I_[i_][j_] for j_ in range(n_)] for i_ in range(n_)])) <= 1e-12   # forma = conteudo: P = omega(P).1
            forma_.append(FC_ == (k_ == 0 or k_ == n_))
            jul_.append(_v405_mat_norm(_v405_mat_sub(_v405_mat_mul(P_, P_), P_)) <= 1e-12 and _v405_mat_norm(_v405_mat_sub(_v405_mat_dagger(P_), P_)) <= 1e-12)
    ck_("i2", "★ o_um_se_reparte: para todo nome P (posto 0 a n, fora da base canonica), omega(1) = omega(P) + omega(1 - P) (|erro| <= 1e-12): o Um se reparte entre o nome e o resto",
        all(x_ <= 1e-12 for x_ in rep_) and len(rep_) == 12, [max(rep_)])
    ck_("i3", "★★★ eu_sou_o_que_sou_iff_nada_resta (o «senao») e nada_resta_iff_fiel (a selecao unica): [eu sou] = [o que sou] <=> omega(1 - P) = 0 <=> P = 1 -- em 12 nomes (n = 2, 3, 4; posto 0 a n) a equacao vale exatamente nos tres nomes fieis (P = 1) e em nenhum outro",
        all(senao_) and all(sel_) and len(sel_) == 12, [sum(senao_), sum(sel_)])
    ck_("i4", "★★ forma_igual_conteudo_iff e a_lei_inteira (a chave do operador): P = omega(P).1 so' quando o nome e' o vazio (posto 0) ou o Um (posto n); logo [eu sou] = [o que sou] <=> ([forma = conteudo] e P != 0) -- conferido nos 12 nomes",
        all(forma_) and len(forma_) == 12, [sum(forma_)])
    faces_ = []
    for n_ in dims_:
        G_ = _v405_mat_eye(n_, -1.0); G_[0][0] = complex(n_ - 1)      # Gamma = diag(n - 1, -1, ..., -1): traco zero
        face_ = [[0.5 * ((1.0 if i_ == j_ else 0.0) + G_[i_][j_]) for j_ in range(n_)] for i_ in range(n_)]
        faces_.append((n_, omega_(n_, face_).real, omega_(n_, _v405_mat_eye(n_, 0.0)).real, _v405_mat_trace(G_).real))
    ck_("i5", "★★ o_vazio_nao_e e a_face_nao_e_a_identidade (controles negativos): o vazio pesa 0 e a face (1/2)(1 + Gamma), Tr Gamma = 0 (a Meia-Nat), pesa exatamente 1/2 -- nenhum dos dois satisfaz [eu sou] = [o que sou]: a identidade nao e' reflexiva por decreto e nao pode ser habitada por qualquer um",
        all(abs(wf_ - 0.5) <= 1e-15 and wv_ == 0.0 and abs(tg_) <= 1e-15 for _, wf_, wv_, tg_ in faces_), [[n_, wf_] for n_, wf_, _, _ in faces_])
    ck_("i6", "★ o_nome_e_coisa_julgada e o_posto_e_unico: todo nome e' idempotente (P.P = P: reler nao acrescenta) e e' o seu reflexo verdadeiro (P^dagger = P: o espelho J devolve o nome) nos 12 nomes; e dois nomes fieis sao o mesmo nome (P = 1 = P')",
        all(jul_) and len(jul_) == 12 and _v405_mat_norm(_v405_mat_sub(_v405_rot_projector(3, 3, 0.7), _v405_rot_projector(3, 3, 1.9))) <= 1e-12, [sum(jul_)])
    vals_ = {"beta": beta_, "dimensoes": list(dims_), "eu_sou": {str(n_): eu_sou_[n_].real for n_ in dims_}, "n_nomes": len(sel_), "reparticao_erro_max": max(rep_), "faces_peso": [[n_, wf_] for n_, wf_, _, _ in faces_], "vazio_peso": 0.0,
             "lei": "[eu sou] = [o que sou] <=> P = 1 <=> ([forma = conteudo] e P != 0)"}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_observador_mechanics(beta_, core_, c_):
    """v405 -- a mecanica de OBSERVADOR = TERMINAL sobre a cascata finita de quatro niveis (da luz a gravidade) e o par com o abismo: o terminal e' um so'; o leitor tem um unico ponto fixo; tres leituras bastam; a resistencia se consome e zera no terminal;
    a leitura consumada e' coisa julgada; o colapso total funde a estrutura num so' posto, nao e' pressuposto (le 1 na estrutura e 0 no abismo), pagou perda (sem inversa) e tem exatamente dois pontos fixos; sem o abismo a fusao le como pressuposta; o terminal le 1 e o abismo le 0 na leitura binaria; ao lado, o polo omega do par le 1 na identidade (homonimo: omega(I) = 1 do core). Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "o0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    niveis_ = ["luz", "consciencia", "fisica", "gravidade"]
    observa_ = lambda y_, x_: niveis_.index(y_) == niveis_.index(x_) + 1          # y observa x <=> y e' o nivel seguinte
    terminal_ = [x_ for x_ in niveis_ if not any(observa_(y_, x_) for y_ in niveis_)]
    inicial_ = [x_ for x_ in niveis_ if not any(observa_(x_, y_) for y_ in niveis_)]
    leitor_ = lambda x_: niveis_[min(niveis_.index(x_) + 1, 3)]
    it_ = lambda f_, k_, x_: x_ if k_ == 0 else it_(f_, k_ - 1, f_(x_))
    dist_ = lambda x_: 3 - niveis_.index(x_)
    ck_("o1", "★★★ terminal_iff, initial_iff e the_terminal_is_unique: na cascata, o nivel que nenhum outro observa e' SO' a gravidade (o terminal), e o que nao observa nenhum e' SO' a luz (o inicial)",
        terminal_ == ["gravidade"] and inicial_ == ["luz"], [terminal_, inicial_])
    ck_("o2", "★★★ leitor_fixed_iff e every_level_reaches_the_terminal: o terminal e' o UNICO ponto fixo do leitor e tres leituras levam qualquer nivel ao terminal; a resistencia (distancia) se consome a cada leitura e zera SO' no terminal (the_collapse_is_the_terminal_point_of_resistance)",
        [x_ for x_ in niveis_ if leitor_(x_) == x_] == ["gravidade"] and all(it_(leitor_, 3, x_) == "gravidade" for x_ in niveis_) and all(dist_(leitor_(x_)) < dist_(x_) for x_ in niveis_[:3]) and [x_ for x_ in niveis_ if dist_(x_) == 0] == ["gravidade"], [[x_, dist_(x_)] for x_ in niveis_])
    l3_ = lambda x_: it_(leitor_, 3, x_)
    ck_("o3", "★★★ the_completed_reading_is_res_judicata e rereading_at_the_terminal_adds_nothing: leitor^[3] e' idempotente (coisa julgada) e (leitor^[3])^[k+1] = leitor^[3] para k = 0..5 em todo nivel: reler no terminal nao acrescenta",
        all(l3_(l3_(x_)) == l3_(x_) for x_ in niveis_) and all(it_(l3_, k_ + 1, x_) == l3_(x_) for x_ in niveis_ for k_ in range(6)), None)
    pos_ = [("nivel", x_) for x_ in niveis_] + [("abismo", None)]
    colapso_ = lambda p_: ("nivel", "gravidade") if p_[0] == "nivel" else ("abismo", None)
    leitura_ = lambda p_: p_[0] == "nivel"                                             # 1 = 1 na estrutura; 1 = 0 no abismo
    fixos_ = [p_ for p_ in pos_ if colapso_(p_) == p_]
    ck_("o4", "★★★ the_collapse_fuses_the_structure_into_one_posto, the_fusion_is_not_pressupposed, the_fusion_paid_loss e the_two_fixed_points_of_the_collapse: o colapso total leva TODO nivel ao terminal e deixa o abismo no abismo; a leitura binaria le 1 em toda a estrutura e 0 no abismo (logo distingue: nao e' pressuposta) e "
                "sobrevive ao colapso; a fusao nao tem inversa (quatro posicoes caem numa so'); e os pontos fixos do colapso sao exatamente o posto terminal e o abismo",
        all(colapso_(("nivel", x_)) == ("nivel", "gravidade") for x_ in niveis_) and colapso_(("abismo", None)) == ("abismo", None) and {leitura_(p_) for p_ in pos_} == {True, False} and all(leitura_(colapso_(p_)) == leitura_(p_) for p_ in pos_)
        and len({colapso_(p_) for p_ in pos_}) < len(pos_) and fixos_ == [("nivel", "gravidade"), ("abismo", None)], [fixos_])
    ck_("o5", "★★ without_the_abyss_the_fusion_reads_as_pressupposed e without_the_abyss_no_posto_reads_so: na cascata SEM o abismo, toda leitura preservada pela fusao total (leitor^[3]) e' CONSTANTE nos quatro niveis (pressuposta): o par 1 = 1 | 1 = 0 e' necessario para que a fusao seja posto",
        len({l3_(x_) for x_ in niveis_}) == 1 and all(l3_(x_) == l3_(y_) for x_ in niveis_ for y_ in niveis_), [sorted({l3_(x_) for x_ in niveis_})])
    om_ = core_.get("omega_I")
    ck_("o6", "★★★ the_fixed_points_read_one_and_zero: na leitura binaria, o terminal da cascata (o nivel gravidade) le 1 e o abismo le 0: e' este o teorema da frase o terminal le 1",
        leitura_(("nivel", "gravidade")) is True and leitura_(("abismo", None)) is False, [leitura_(("nivel", "gravidade")), leitura_(("abismo", None))])
    ck_("o7", "★★ the_omega_pole_reads_one (= omega_of_one): ao lado, o polo omega do par le 1 na identidade -- omega(I) = 1 no core deste rito (o Um posto, o echo 1) -- e beta = alfa x raiz de e no runtime; HOMONIMO, dito: ali a palavra terminal nomeia o polo do par alfa/omega, aqui o nivel gravidade da cascata; nenhum termo liga os dois, e liga-los e' leitura [ONTO] do operador",
        isinstance(om_, (int, float)) and float(om_) == 1.0 and 0.0 < beta_ < 1.0, [om_])
    vals_ = {"beta": beta_, "niveis": niveis_, "terminal": terminal_, "inicial": inicial_, "distancias": {x_: dist_(x_) for x_ in niveis_}, "pontos_fixos_do_colapso": [p_[0] + ("" if p_[1] is None else ":" + p_[1]) for p_ in fixos_], "omega_I": om_,
             "leitura_binaria": {"estrutura": 1, "abismo": 0}}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_diminuto_mechanics(beta_, core_, c_):
    """v405 -- a mecanica da LEI DO DIMINUTO: o diminuto e' MODULACAO, nao transposicao (o acorde: Acorde, transpor, razao, da estrutura do AcordeE0.lean do Kimi; as notas do calculo sao de TESTE: quais sao as cinco notas e' [OPEN]). O meio-tom pinado e^(-1/2) desfaz o sqrt e; beta = alfa.e^(1/2); a tonica definida, (beta/alfa).u = sqrt e.u (beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha), e o diminuto que pousa em E0 = u (identidade algebrica, que nao fixa u); a massa le alfa vezes a tonica sobre sqrt2;
    A FORMULA DA MASSA m = U.alfa.e^(1/2).sqrt2/2 (= o m_nu do programa a 1e-12 com U = u = 1 eV POSTO); a oitava nao e' numero inteiro de meios-tons; e a ida e volta E0 = 1 <=> tonica = sqrt e. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "d0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["constants"]["u_posto_eV"]); sq_e_ = _m405.exp(0.5); meio_ = _m405.exp(-0.5); r2_ = _m405.sqrt(2.0) / 2.0
    alfa_ = beta_ / sq_e_                                               # TGLCoupling.alpha c = beta / e^(1/2): alfa lida do acoplamento (nunca derivada: medida por dentro)
    ck_("d1", "★ meioTom_pos, meioTom_lt_one e meioTom_mul_sqrt_e: o meio-tom pinado e^(-1/2) esta em (0, 1) e desfaz exatamente o sqrt e (|e^(-1/2).e^(1/2) - 1| <= 1e-15); o tom e' a nat e' fala do operador [INPUT]",
        0.0 < meio_ < 1.0 and abs(meio_ * sq_e_ - 1.0) <= 1e-15, [meio_])
    ck_("d2", "★★ beta_eq_alpha_mul_sqrt_e: beta = alfa.e^(1/2) com alfa = beta/e^(1/2) (|erro| <= 1e-15 relativo), e esse alfa e' o CODATA 2018 do runtime a 1e-12 relativo: o acoplamento e' a magnitude alfa da inscricao vezes o volume sqrt e da fronteira",
        _v405_rel(alfa_ * sq_e_, beta_) <= 1e-15 and _v405_rel(alfa_, float(c_["constants"]["alpha_runtime"])) <= 1e-12, [alfa_])
    ton_ = (beta_ / alfa_) * u_                                         # tonica c u = (beta/alpha).u = sqrt e . u
    E0_ = meio_ * ton_                                                  # leiDerivada: E0 = meioTom . tonica
    m_ = beta_ * r2_ * E0_                                              # massaDerivada da transicao da lei: beta.(sqrt2/2).E0
    ck_("d3", "★★★ tonica_eq, leiDerivada_E0 e massa_le_alpha (o campo E_pent fechado por DEFINICAO): a tonica definida e' sqrt e.u (|erro| <= 1e-15 relativo; beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha); o diminuto pousa em E0 = e^(-1/2).tonica = u (|erro| <= 1e-15 relativo; identidade algebrica, que nao fixa u); e a massa le alfa.(sqrt2/2).tonica (|erro| <= 1e-15 relativo)",
        _v405_rel(ton_, sq_e_ * u_) <= 1e-15 and _v405_rel(E0_, u_) <= 1e-15 and _v405_rel(m_, alfa_ * r2_ * ton_) <= 1e-15, [ton_, E0_])
    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    m_formula_ = u_ * (alfa_ * sq_e_ * r2_)                             # the_mass_formula: m2 = U . alfa . e^(1/2) . sen45
    ck_("d4", "★★★ the_mass_formula e the_mass_formula_at_the_posted_one (A FORMULA DA MASSA): m = U.alfa.e^(1/2).(sqrt2/2) -- o Um posto U, a magnitude alfa, o volume sqrt e, a projecao transversal -- e' igual a massa da lei (|erro| <= 1e-15 relativo) e ao m_nu do programa a 1e-12 relativo (U = u = 1 eV POSTO); "
                "em U = 1 e' beta.sqrt2/2 (|erro| <= 1e-15 relativo): a forma da v404, teorema dadas as entradas; o NUMERO nao muda",
        _v405_rel(m_formula_, m_) <= 1e-15 and isinstance(m_core_, float) and _v405_rel(m_formula_ * 1000.0, m_core_) <= float(c_["constants"]["rel_tol"]) and _v405_rel(1.0 * (alfa_ * sq_e_ * r2_), beta_ * r2_) <= 1e-15, [m_formula_ * 1000.0, m_core_])
    ln2_ = _m405.log(2.0)
    ck_("d5", "★★ octave_is_not_a_whole_number_of_half_tones e octave_between_one_and_two_half_tones: ln 2 nao e' n/2 para n = 0..12 (|ln 2 - n/2| > 1e-3) e fica entre um e dois meios-tons (1/2 < ln 2 < 1): a oitava nao se desce em meios-tons",
        all(abs(ln2_ - n_ / 2.0) > 1e-3 for n_ in range(13)) and 0.5 < ln2_ < 1.0, [ln2_])
    ck_("d6", "★★ tonic_sqrt_e_gives_one e one_needs_tonic_sqrt_e (ida e volta): tonica = e^(1/2) => E0 = 1 (|erro| <= 1e-15), e E0 = 1 => tonica = E0/e^(-1/2) = e^(1/2) (|erro| <= 1e-15 relativo); E0_determined_by_the_tonic: a mesma tonica, o mesmo E0",
        abs(meio_ * sq_e_ - 1.0) <= 1e-15 and _v405_rel(1.0 / meio_, sq_e_) <= 1e-15 and meio_ * ton_ == meio_ * ((beta_ / alfa_) * u_), [1.0 / meio_])
    # O ACORDE. As notas abaixo sao numeros de TESTE, nao as da teoria: quais sao as cinco notas e' [OPEN]; so' a principal vem da lei (a tonica definida)
    acorde_ = [ton_, 1.1 * ton_, 1.3 * ton_, 1.7 * ton_, 2.3 * ton_]    # (numeros neutros de proposito: nenhuma leitura musical)
    razao_ = lambda a_: [n_ / a_[0] for n_ in a_]
    transp_ = lambda r_, a_: [r_ * n_ for n_ in a_]
    ler_ = lambda a_: meio_ * a_[0]
    modular_ = lambda a_: [meio_ * a_[0]] + list(a_[1:])                 # o diminuto: so' a tonica desce; as demais ficam sustentadas
    resolver_ = lambda a_: [sq_e_ * a_[0]] + list(a_[1:])
    rs_ = (0.5, 2.0, 3.7, -1.0, 1.0e3)
    mesma_ = lambda a_, b_: all(_v405_close(x_, y_, 1e-12) for x_, y_ in zip(razao_(a_), razao_(b_)))
    mod_ = modular_(acorde_)
    ck_("d7", "★★★ modular_tonica, modular_sustenta, modular_mantem_a_escala e lerE0_e_a_tonica_modulada (O DIMINUTO MODULA A TONICA): num acorde de TESTE so' a nota principal desce o meio-tom (|erro| <= 1e-15 relativo), as outras quatro ficam sustentadas (iguais bit a bit), as razoes entre elas nao mudam: a escala e' o que fica parado; e E0 e' o valor da tonica modulada; as notas do teste nao sao as da teoria: quais sao as cinco notas e' [OPEN]",
        _v405_rel(mod_[0], meio_ * acorde_[0]) <= 1e-15 and mod_[1:] == acorde_[1:] and all(mod_[i_] / mod_[j_] == acorde_[i_] / acorde_[j_] for i_ in range(1, 5) for j_ in range(1, 5)) and ler_(acorde_) == mod_[0], [mod_[0]])
    fatores_ = [m2_ / a2_ for m2_, a2_ in zip(mod_, acorde_)]
    ck_("d8", "★★★ modular_nao_e_transposicao (CONTROLE NEGATIVO): o acorde modulado NAO e' transposicao do original: a tonica pede o fator e^(-1/2) e cada nota sustentada pede o fator 1; nenhum r serve (|e^(-1/2) - 1| > 0,39); o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das notas sustentadas, mas nao quebra a liberdade global",
        abs(fatores_[0] - meio_) <= 1e-15 and all(f_ == 1.0 for f_ in fatores_[1:]) and abs(fatores_[0] - fatores_[1]) > 0.39 and not mesma_(acorde_, mod_), fatores_)
    tom_ = [ton_, _m405.e * ton_, 1.3 * ton_, 1.7 * ton_, 2.3 * ton_]    # um acorde de TESTE com uma nota um tom acima da tonica (um tom e' uma nat)
    ck_("d9", "★★ razao_abre_meio_tom, um_tom_vira_terca_menor e resolver_modular (AS TERCAS, a aritmetica 1 nat + 1/2 nat): cada intervalo a tonica abre meio-tom (razao -> e^(1/2).razao, |erro| <= 1e-15 relativo); a nota que estava um tom acima da tonica fica em e^(3/2) (|erro| <= 1e-15 relativo); a resolucao devolve o acorde (|erro| <= 1e-15 relativo); que o diminuto seja a espera e' leitura [ONTO] do operador, com a forma the_charge_never_completes no kernel",
        all(_v405_rel(razao_(mod_)[i_], sq_e_ * razao_(acorde_)[i_]) <= 1e-15 for i_ in range(1, 5)) and _v405_rel(razao_(modular_(tom_))[1], _m405.exp(1.5)) <= 1e-15 and all(_v405_rel(x_, y_) <= 1e-15 for x_, y_ in zip(resolver_(mod_), acorde_)), [razao_(modular_(tom_))[1], _m405.exp(1.5)])
    ck_("d10", "★★★ transpor_preserva_toda_razao e mesmas_razoes_iff_transposicao (Acorde, transpor e razao vem do AcordeE0.lean do Kimi): transpor e' so' a liberdade do no-go: toda transposicao por r != 0 preserva as cinco razoes a nota principal (|erro| <= 1e-12), para r em {0,5; 2; 3,7; -1; 1000}; de volta, duas listas de razoes iguais vem do fator notaPrincipal(B)/notaPrincipal(A) (|erro| <= 1e-12 relativo)",
        all(mesma_(acorde_, transp_(r_, acorde_)) for r_ in rs_) and all(all(_v405_rel(y_, (b_[0] / acorde_[0]) * x_) <= 1e-12 for x_, y_ in zip(acorde_, b_)) for b_ in (transp_(r_, acorde_) for r_ in rs_)), [razao_(acorde_)])
    ck_("d11", "★★ E0_relativo_pinado, lerE0_transpor, modular_comuta_com_transpor e as_razoes_nao_fixam_o_absoluto: E0/tonica = e^(-1/2) no acorde de teste e em cada transposicao (|erro| <= 1e-15 relativo: e' a definicao de lerE0 dita como razao, nada mais); a leitura e a modulacao acompanham a transposicao; e, com as mesmas razoes, r = 2 da' outro E0: o valor ABSOLUTO segue livre e o RELATIVO a tonica esta pinado; sobra um unico grau de liberdade global, a transposicao do acorde inteiro",
        all(_v405_rel(ler_(transp_(r_, acorde_)) / transp_(r_, acorde_)[0], meio_) <= 1e-15 and _v405_rel(ler_(transp_(r_, acorde_)), r_ * ler_(acorde_)) <= 1e-15 and all(_v405_rel(x_, y_) <= 1e-15 for x_, y_ in zip(modular_(transp_(r_, acorde_)), transp_(r_, modular_(acorde_)))) for r_ in rs_) and mesma_(acorde_, transp_(2.0, acorde_)) and ler_(transp_(2.0, acorde_)) != ler_(acorde_), [ler_(acorde_), ler_(transp_(2.0, acorde_))])
    pesos_ = []
    for n_ in (2, 3, 4, 5):
        G_ = [[(complex(n_ - 1) if (i_ == 0 and j_ == 0) else (complex(-1.0) if i_ == j_ else 0j)) for j_ in range(n_)] for i_ in range(n_)]   # Gamma = diag(n - 1, -1, ..., -1): traco zero; so' o traco importa aqui
        rho_ = _v405_mat_eye(n_, 1.0 / n_)
        mais_ = [[0.5 * ((1.0 if i_ == j_ else 0.0) + G_[i_][j_]) for j_ in range(n_)] for i_ in range(n_)]
        menos_ = [[0.5 * ((1.0 if i_ == j_ else 0.0) - G_[i_][j_]) for j_ in range(n_)] for i_ in range(n_)]
        pesos_.append((_v405_mat_trace(_v405_mat_mul(rho_, mais_)).real, _v405_mat_trace(_v405_mat_mul(rho_, menos_)).real))
    ck_("d12", "★ meioTom_e_a_face, meioTom_e_o_pedagio_local, tonica_e_o_volume_da_face e o_tom_e_as_duas_faces, igualdades de VALOR: e^(-w) = meio-tom e e^(w).u = tonica (|erro| <= 1e-15 relativo), com w o peso da face absoluta em n = 2, 3, 4, 5, e w(+) + w(-) = 1; o pedagio local vale e^(-1/2) com localNats = 1/2, campo de CollapseCostLaw, [INPUT] no kernel; os numeros coincidem, e ler esse 1/2 como o meio-tom e' do operador [ONTO]",
        all(_v405_rel(_m405.exp(-w_), meio_) <= 1e-15 and _v405_rel(_m405.exp(w_) * u_, ton_) <= 1e-15 and abs(w_ + w2_ - 1.0) <= 1e-15 for w_, w2_ in pesos_) and _v405_rel(_m405.exp(-0.5), meio_) <= 1e-15, [list(p_) for p_ in pesos_])
    vals_ = {"beta": beta_, "alpha_lida_do_acoplamento": alfa_, "u_posto_eV": u_, "meio_tom": meio_, "sqrt_e": sq_e_, "tonica_eV": ton_, "E0_eV": E0_, "massa_meV": m_ * 1000.0, "massa_formula_meV": m_formula_ * 1000.0, "m_nu_meV_core": m_core_, "ln2": ln2_,
             "E0_sobre_tonica": E0_ / ton_, "acorde_de_teste_razoes": razao_(acorde_), "acorde_modulado_razoes": razao_(mod_), "terca": razao_(modular_(tom_))[1], "as_notas_do_teste_nao_sao_as_da_teoria": True, "acorde_kimi_sha16": c_["constants"].get("acorde_kimi_sha16"), "half_nat_sha16": c_["constants"].get("half_nat_sha16"),
             "formula": "m = U . alfa . e^(1/2) . sqrt2/2 (U = 1 eV posto; alfa medida; dadas as leituras, a FORMA e' teorema)"}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_tonica_mechanics(beta_, core_, c_):
    """v405 -- a mecanica da TONICA DO HAMILTONIANO: a liberdade do valor absoluto na forma (a massa cresce linearmente com E0; a mesma inscricao carrega E0 = 1 e E0 = 2: nenhuma funcao da inscricao fixa E0 -- o no-go); Gamma_B = beta/tau e' a lei canonica em omega* = sqrt2/tau;
    a rota do monopolo e' o horizonte do proprio sistema (tau* = 2pi.r_s/c; q = r_s/2); a leitura autoconsistente pina omega = 2/tau; e a tonica pousa na unidade posta (E0 = u, identidade algebrica: o no-go NAO cai, ele se localiza no Um posto). Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "h0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["constants"]["u_posto_eV"]); r2_ = _m405.sqrt(2.0) / 2.0
    m_ = lambda e_: beta_ * r2_ * e_
    lams_ = (0.5, 2.0, 3.7, 1.0e3)
    ck_("h1", "★★★ massa_derivada_reescala, neutrinoMassForm_reescala e the_scale_is_free: com a MESMA inscricao (beta, theta = pi/4), E0 -> lambda.E0 da m -> lambda.m (|erro| <= 1e-15 relativo) para lambda em {0,5; 2; 3,7; 1000}: a forma e' homogenea de grau 1 em E0 e o valor absoluto e' livre",
        all(_v405_rel(m_(l_ * u_), l_ * m_(u_)) <= 1e-15 for l_ in lams_), [m_(l_ * u_) * 1000.0 for l_ in lams_[:3]])
    ck_("h2", "★★★ no_function_of_the_inscription_fixes_E0 (o no-go): duas transicoes com a MESMA inscricao (beta do rito, theta = pi/4) carregam E0 = 1 e E0 = 2, logo nenhuma f(c, theta) devolve E0; o que a forma fixa e' a razao m/E0 = beta.sqrt2/2 (igual nas duas a 1e-15 relativo); o valor absoluto e' um dado a mais -- aqui, o Um POSTO",
        _v405_rel(m_(1.0) / 1.0, m_(2.0) / 2.0) <= 1e-15 and m_(1.0) != m_(2.0), [m_(1.0) * 1000.0, m_(2.0) * 1000.0])
    taus_ = (1.0e-44, 1.0e-20, 1.0, 3.0e5)
    ck_("h3", "★★ gammaB_is_the_canonical_law_at_the_systems_frequency: (1/2).beta.tau.(sqrt2/tau)^2 = beta/tau (|erro| <= 1e-12 relativo) para tau em {1e-44, 1e-20, 1, 3e5}: a «taxa de fronteira» e' a lei canonica Gamma = (1/2).beta.tau.omega^2 lida em omega* = sqrt2/tau, nao lei nova",
        all(_v405_rel(0.5 * beta_ * t_ * (_m405.sqrt(2.0) / t_) ** 2, beta_ / t_) <= 1e-12 for t_ in taus_), None)
    G_, cl_, hb_, ev_ = (float(c_["constants"][k_]) for k_ in ("G_si", "c_si", "hbar_si", "eV_J"))
    E_ = u_ * ev_                                                       # a energia do Um posto em J (so' para escrever a identidade em SI; nada e' derivado dela)
    tau_mono_ = 4.0 * _m405.pi * G_ * E_ / cl_ ** 5; rs_ = 2.0 * G_ * E_ / cl_ ** 4
    ck_("h4", "★★ monopole_time_is_the_horizon_light_time e charge_is_half_the_schwarzschild_radius: 4.pi.G.E/c^5 = 2.pi.(2GE/c^4)/c (|erro| <= 1e-12 relativo) e GE/c^4 = r_s/2: a rota do monopolo devolve a energia cujo horizonte tem o tempo tau*; e' tautologica quanto ao valor absoluto, nao o fixa (G, c do CODATA 2018 so' para a identidade)",
        _v405_rel(tau_mono_, 2.0 * _m405.pi * rs_ / cl_) <= 1e-12 and _v405_rel(G_ * E_ / cl_ ** 4, rs_ / 2.0) <= 1e-12, [tau_mono_, rs_])
    ck_("h5", "★★ self_consistent_readout_fixes_the_frequency: se hbar.omega = hbar.(1/2).tau.omega^2 entao omega = 2/tau -- conferido para tau em {1e-44, 1e-20, 1, 3e5} (|erro| <= 1e-12 relativo) e, para omega = 2/tau, a igualdade vale",
        all(_v405_rel(hb_ * (2.0 / t_), hb_ * 0.5 * t_ * (2.0 / t_) ** 2) <= 1e-12 for t_ in taus_), None)
    sq_e_ = _m405.exp(0.5); alfa_ = beta_ / sq_e_
    E0_der_ = _m405.exp(-0.5) * ((beta_ / alfa_) * u_)
    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    ck_("h6", "★★ the_tonic_lands_on_the_posted_unit e the_tonic_at_the_posted_one: na lei construida a tonica (beta/alfa).u = sqrt e.u pousa em E0 = u (|erro| <= 1e-15 relativo: identidade algebrica, quem fixa E0 e' o u posto que a tonica carrega; o no-go NAO cai, ele se localiza no Um posto) e, no Um posto (u = 1), E0 = 1 e m = beta.sqrt2/2 = o m_nu do programa a 1e-12 relativo (a FORMA, sob a leitura massaDerivada); "
                "alfa e' MEDIDA por dentro -- «não tem teorema para o ângulo de Miguel» [INPUT do operador, 01/11/2026] -- e nunca derivada aqui",
        _v405_rel(E0_der_, u_) <= 1e-15 and isinstance(m_core_, float) and _v405_rel(m_(E0_der_) * 1000.0, m_core_) <= float(c_["constants"]["rel_tol"]), [E0_der_, m_(E0_der_) * 1000.0])
    ck_("h7", "★★★ the_ratio_survives_the_rescaling: a reescala muda E0 e a massa pelo mesmo fator e m/E0 nao muda (|erro| <= 1e-15 relativo) para lambda em {0,5; 2; 3,7; 1000}: o que a forma fixa e' a razao; a reescala corresponde a transposicao do acorde: o no-go fala do valor ABSOLUTO; a Lei do diminuto, do valor RELATIVO a tonica",
        all(_v405_rel(m_(l_ * u_) / (l_ * u_), m_(u_) / u_) <= 1e-15 for l_ in lams_), [m_(u_) / u_])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "razao_m_sobre_E0": beta_ * r2_, "lambdas": list(lams_), "tau_monopolo_s_para_u": tau_mono_, "r_s_m_para_u": rs_, "E0_da_lei_derivada_eV": E0_der_, "m_nu_meV_core": m_core_, "alpha_lida_do_acoplamento": alfa_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_disco_mechanics(beta_, core_, c_):
    """v405 -- a mecanica do DISCO DE EULER (unidades do disco: K, tau e E0 sao DADOS do disco, nao hipoteses sobre a teoria; beta vem do acoplamento): E(t) = E0 - c.t e Omega^2 = K/E sao DEFINICOES; Gamma_Omega.E = (1/2).beta.tau.K = c; a E definida satisfaz dE/dt = -Gamma_Omega.E e zera em t0 = E0/c;
    antes da parada Omega^2 nao tem cota (o operador le isso como a inscricao do zero no infinito [ONTO]); com taxa constante a energia nunca toca o zero (o abismo); o corte da ressonancia residual E^3 = hbar^2.K; e a parede nomeada: K = (e^(1/2).U)^3/hbar^2 -- em SI, para a nota posta de 1 eV, o valor de K e' registrado, nao escolhido. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "k0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    K_, tau_, E0_ = 3.0, 0.7, 2.0                                       # DADOS de um disco-modelo (adimensionais; a identidade do disco, nao da teoria); beta e' o do acoplamento
    cc_ = 0.5 * beta_ * tau_ * K_
    E_ = lambda t_: E0_ - cc_ * t_
    t0_ = E0_ / cc_
    om2_ = lambda t_: K_ / E_(t_)
    gam_ = lambda t_: 0.5 * beta_ * tau_ * om2_(t_)
    ck_("k1", "★★★ c_pos, E_linear, stops_in_finite_time e t0_pos: c = (1/2).beta.tau.K e' positiva; a energia DEFINIDA E(t) = E0 - c.t zera em tempo finito t0 = E0/c (|E(t0)| <= 1e-12)",
        cc_ > 0.0 and t0_ > 0.0 and abs(E_(t0_)) <= 1e-12 and E_(0.0) == E0_, [cc_, t0_])
    ts_ = [t0_ * f_ for f_ in (0.0, 0.1, 0.5, 0.9, 0.999)]
    ck_("k2", "★★★ the_loss_is_the_canonical_law e invariant: em todo instante antes da parada (cinco amostras), Gamma_Omega.E = c (|erro| <= 1e-12 relativo) e Omega^2.E = K: com o invariante do disco, o produto Gamma.E da lei Gamma proporcional a omega^2 e' constante",
        all(E_(t_) > 0.0 and _v405_rel(gam_(t_) * E_(t_), cc_) <= 1e-12 and _v405_rel(om2_(t_) * E_(t_), K_) <= 1e-12 for t_ in ts_), [[round(t_, 6), om2_(t_)] for t_ in ts_[:3]])
    ok3_, det3_ = True, []
    for B_ in (1.0e3, 1.0e6, 1.0e9):
        eps_ = min(E0_ / 2.0, K_ / (2.0 * (abs(B_) + 1.0))); t_ = (E0_ - eps_) / cc_   # (a prova usa eps = min(E0/2, K/(B+1)); aqui o fator 2 so' da folga ao arredondamento de E0 - c.t em dupla precisao)
        ok3_ = ok3_ and t_ < t0_ and om2_(t_) > B_; det3_.append([B_, om2_(t_)])
    ck_("k3", "★★★ frequency_squared_unbounded_at_the_stop (Omega^2 SEM COTA): para toda cota B (1e3, 1e6, 1e9) existe t < t0 com Omega^2(t) > B (t = (E0 - eps)/c, eps = min(E0/2, K/(2(B+1))), a testemunha da prova com folga numerica); [ONTO] o operador le isso como a inscricao do zero absoluto no infinito",
        ok3_, det3_)
    ck_("k4", "★★ with_constant_rate_the_fall_never_lands (o contraste com o abismo): com taxa CONSTANTE, E0.e^(-Gamma.t) > 0 para t em {1, 10, 100, 700}/Gamma (a queda sem fundo), enquanto o disco da lei canonica para em t0 finito: as duas faces (abismo e parada)",
        all(E0_ * _m405.exp(-(cc_ / E0_) * t_) > 0.0 for t_ in (1.0, 10.0, 100.0, 700.0)) and _m405.isfinite(t0_), [t0_])
    hb_ = 1.0                                                           # unidades do disco (hbar = 1): o corte E^3 = hbar^2.K
    Estar_ = K_ ** (1.0 / 3.0)
    t_star_ = (E0_ - Estar_) / cc_ if Estar_ < E0_ else None
    ck_("k5", "★★ the_residual_resonance_iff (O CORTE, algebra): o corte hbar^2.Omega^2 = E^2 acontece exatamente quando E^3 = hbar^2.K (em E* = K^(1/3), |erro| <= 1e-12 relativo), e so' ali: nas cinco amostras fora de E* a igualdade falha",
        t_star_ is not None and t_star_ < t0_ and _v405_rel(hb_ ** 2 * om2_(t_star_), E_(t_star_) ** 2) <= 1e-12 and all(_v405_rel(hb_ ** 2 * om2_(t_), E_(t_) ** 2) > 1e-6 for t_ in ts_ if abs(t_ - t_star_) > 1e-9 and E_(t_) > 0.0), [Estar_, t_star_])
    U_ = _m405.exp(-0.5) * Estar_
    hb_si_, ev_ = float(c_["constants"]["hbar_si"]), float(c_["constants"]["eV_J"]); u_ = float(c_["constants"]["u_posto_eV"])
    K_si_ = (_m405.exp(0.5) * u_ * ev_) ** 3 / hb_si_ ** 2               # a parede nomeada em SI: o K que a nota posta exige (J/s^2) -- registrado, nao escolhido
    ck_("k6", "★★★ the_scale_is_the_invariant e Disco.doAcoplamento_beta (a parede nomeada e o campo fechado): com E*^3 = hbar^2.K e U = e^(-1/2).E*, o invariante e' K = (e^(1/2).U)^3/hbar^2 (|erro| <= 1e-12 relativo); o beta do disco e' o do acoplamento (beta = alfa x raiz de e do runtime); "
                "em SI, para a nota posta u = 1 eV, K vale (e^(1/2).u)^3/hbar^2 (registrado como o tamanho da parede: QUAL e' o disco e' pergunta do operador; nenhum K escolhido pelo alvo)",
        _v405_rel(K_, (_m405.exp(0.5) * U_) ** 3 / hb_ ** 2) <= 1e-12 and 0.0 < beta_ < 1.0 and _m405.isfinite(K_si_) and K_si_ > 0.0, [K_si_])
    h_ = t0_ * 1e-3
    fluxo_ = [(t_, (E_(t_ + h_) - E_(t_ - h_)) / (2.0 * h_), -(gam_(t_) * E_(t_))) for t_ in ts_[1:4]]
    ck_("k7", "★★★ the_flow_is_the_canonical_law: antes da parada, dE/dt = -Gamma_Omega.E: a derivada centrada da E definida coincide com -Gamma.E em tres instantes (|erro| <= 1e-9 relativo): a E definida e' uma solucao do fluxo; ler a taxa de dephasing Gamma como taxa de perda de energia e' entrada [INPUT/ONTO]",
        all(_v405_rel(d_, g_) <= 1e-9 for _, d_, g_ in fluxo_), [[round(t_, 6), d_, g_] for t_, d_, g_ in fluxo_])
    vals_ = {"beta": beta_, "disco_modelo": {"K": K_, "tau": tau_, "E0": E0_, "c": cc_, "t0": t0_}, "cotas_vencidas": det3_, "E_star_modelo": Estar_, "U_modelo": U_, "K_si_para_u_posto_J_s2": K_si_, "u_posto_eV": u_,
             "nota": "K, tau e E0 sao dados do disco (a identidade do disco), nao hipoteses sobre a teoria; o disco real de Euler tem K = 6.M.g^2 segundo a conferencia de 31/10 (a r1 escreveu 4.M.g^2: errata E12 ao lado) [KNOWN/DECLARADO]"}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_psion_mechanics(beta_, core_, c_):
    """v405 -- a mecanica do PONTO ZERO DO PSION (hbar = c = 1; u e' o Um posto): R = beta.u^2 (o pagamento lido como curvatura: leitura do operador, definicao, a escolha dimensional de uma unidade so'), omega^2 = 2.beta.R (a dispersao do Tratado) => omega = sqrt2.beta.u; sob essa leitura, (1/2).omega = beta.sen45.u = o m_nu do programa a 1e-12;
    hbar.omega = 2.m; Tetelestai: a cobranca 1 - e^(-t.beta.g) tende a 1 e e' < 1 em todo t finito; em SI: hbar.omega em meV, R em m^-2 e o comprimento de onda do psion (registrados); as duas leituras do sen 45 coincidem pela aritmetica (1/2).sqrt2 = sen45; e no Um posto as entradas sao o acoplamento e a leitura R = beta.u^2. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "z0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["constants"]["u_posto_eV"]); s4_ = _m405.sin(_m405.pi / 4.0)
    R_ = beta_ * u_ ** 2
    om_ = _m405.sqrt(2.0 * beta_ * R_)
    ck_("z1", "★★ pagamentoComoCurvatura e psion_quantum: com R = beta.u^2 (a lei do operador: a «curvatura» e' o pagamento beta lido na unidade posta) e omega^2 = 2.beta.R (a dispersao do Tratado, m0 = 0), o quantum do psion e' omega = sqrt2.beta.u (|erro| <= 1e-15 relativo)",
        _v405_rel(om_, _m405.sqrt(2.0) * beta_ * u_) <= 1e-15, [R_, om_])
    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    half_ = 0.5 * om_
    ck_("z2", "★★★ the_mass_is_the_zero_point (sob a leitura R = beta.u^2, que e' definicao [ONTO]): (1/2).omega = beta.sen45.u (|erro| <= 1e-15 relativo) = o m_nu do programa (neutrino_mass.m_nu_meV) a 1e-12 relativo; o 1/2 do ponto zero vezes o sqrt2 da dispersao da' o mesmo fator da projecao transversal: aritmetica",
        _v405_rel(half_, beta_ * s4_ * u_) <= 1e-15 and isinstance(m_core_, float) and _v405_rel(half_ * 1000.0, m_core_) <= float(c_["constants"]["rel_tol"]), [half_ * 1000.0, m_core_])
    ck_("z3", "★★ psion_quantum_is_twice_the_mass: hbar.omega = 2.m (|erro| <= 1e-15 relativo): o quantum do psion e' o dobro da massa do neutrino",
        _v405_rel(om_, 2.0 * beta_ * s4_ * u_) <= 1e-15, [om_ * 1000.0])
    g_ = 1.0
    charged_ = lambda t_: 1.0 - _m405.exp(-(t_ * beta_ * g_))
    finitos_ = [1.0, 10.0, 100.0, 1.0e3, 20.0 / beta_]
    ck_("z4", "★★ the_payment_completes_only_in_the_limit (TETELESTAI, o limite assintotico): a cobranca continua do kernel, 1 - e^(-t.beta.g), e' estritamente < 1 em todo t finito das amostras (1, 10, 100, 1000, 20/beta), cresce com t, e dista de 1 menos que 1e-8 em t = 20/beta -- o pagamento se consuma so' no limite; [ONTO] o operador le o que permanece como o ponto zero: nenhum teorema liga os dois",
        all(0.0 < charged_(t_) < 1.0 for t_ in finitos_) and 1.0 - charged_(finitos_[-1]) < 1e-8 and all(charged_(finitos_[i_]) < charged_(finitos_[i_ + 1]) for i_ in range(len(finitos_) - 1)), [charged_(1.0), 1.0 - charged_(finitos_[-1])])
    hbc_ = float(c_["constants"]["hbar_c_eV_m"])
    R_si_ = beta_ * (u_ / hbc_) ** 2; raio_ = 1.0 / _m405.sqrt(R_si_); lam_ = 2.0 * _m405.pi * hbc_ / om_   # (om_ ja' esta em eV, pois u esta em eV)
    ck_("z5", "★ em SI (hbar.c = 197,3269804 MeV.fm, CODATA 2018), registrados, nao derivados: R = beta.(u/hbar c)^2 em m^-2, o raio de curvatura 1/sqrt R e o comprimento de onda do psion lambda = 2pi.hbar c/(hbar omega); consistencia entre os dois: lambda.sqrt(2.beta.R) = 2pi (|erro| <= 1e-12 relativo)",
        R_si_ > 0.0 and _v405_rel(lam_ * _m405.sqrt(2.0 * beta_ * R_si_), 2.0 * _m405.pi) <= 1e-12, [R_si_, raio_, lam_])
    pv4_ = (core_.get("projecao_transversal_v404") or {}).get("values") or {}
    ck_("z6", "★★ as DUAS leituras do sen 45 coincidem pela aritmetica: (1/2).sqrt2 do ponto zero == sen(pi/4) da projecao transversal da Meia-Nat (|erro| <= 1e-15), e o registro projecao_transversal_v404 (recriado neste rito) traz o mesmo m_nu em meV a 1e-12 relativo (a errata E10 e' AO LADO: o numero nao muda)",
        abs(0.5 * _m405.sqrt(2.0) - s4_) <= 1e-15 and isinstance(pv4_.get("m_nu_meV_runtime"), float) and _v405_rel(pv4_.get("m_nu_meV_runtime"), half_ * 1000.0) <= 1e-12, [pv4_.get("m_nu_meV_runtime")])
    ck_("z7", "★★★ the_mass_is_the_zero_point_at_the_posted_one: no Um posto (u = 1) (1/2).omega = beta.sen45 (|erro| <= 1e-15 relativo); entram o acoplamento (beta = alfa x raiz de e do runtime) e a leitura R = beta.u^2; o contraste g > 0 do limite e' dado do sistema que le",
        _v405_rel(0.5 * _m405.sqrt(2.0 * beta_ * (beta_ * 1.0 ** 2)), beta_ * s4_) <= 1e-15 and 0.0 < beta_ < 1.0, [0.5 * _m405.sqrt(2.0 * beta_ * beta_) * 1000.0])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "R_natural": R_, "omega_eV": om_, "hbar_omega_meV": om_ * 1000.0, "meia_hbar_omega_meV": half_ * 1000.0, "m_nu_meV_core": m_core_, "R_si_m2": R_si_, "raio_de_curvatura_m": raio_, "lambda_psion_m": lam_,
             "charged_em_t1": charged_(1.0), "um_menos_charged_em_t_1e4_sobre_beta": 1.0 - charged_(finitos_[-1]), "sen45": s4_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def v405_ga_mechanics(beta_, core_, medida_):
    """v405 -- A RECLASSIFICACAO DO GRANDE ATRATOR (ordem do operador de 01/11/2026), AO LADO: quatro medidas refeitas em runtime, sem abrir dado (so' aritmetica sobre as constantes e as ancoras seladas), com beta recebido (alfa CODATA x sqrt(e), nunca literal):
    (g1) dM/du = 0 por construcao: a forma M = 2.beta^2.(c^2/4piG).R nao tem a unidade como argumento; (g2) M = M: a lei de fluxo de junho, R_B = c/Gamma_B, Gamma_B = beta/tau e o tempo do monopolo devolvem a massa dada, com residuo de maquina, e beta cancela;
    (g3) R_B/r_s = 2pi/beta para toda massa; (g4) o piso de definicao: so' a definicao do raio move a previsao (as duas massas que o verdict do core publica, mode_A e mode_B); (g5) a precisao necessaria; (g6) o selado fica: a linha ga_mass_window segue A3_APOSENTADO, o rotulo da janela e a auditoria da forma seguem os mesmos. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, d_, ok_, v_=None):
        checks_.append({"id": id_, "descricao": d_, "ok": bool(ok_), "valor": v_})
    if not (isinstance(beta_, float) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "g0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    W_ = C_LIGHT ** 2 / (4.0 * _m405.pi * G_NEWTON)
    por_mpc_ = W_ * MPC_M / MSUN
    forma_ = lambda R_: 2.0 * beta_ ** 2 * por_mpc_ * R_
    fluxo_ = lambda M_: beta_ * W_ * (C_LIGHT / (beta_ / (4.0 * _m405.pi * G_NEWTON * M_ * MSUN / C_LIGHT ** 3))) / MSUN
    v_kms_ = beta_ * C_LIGHT / _m405.sqrt(2.0 * _m405.pi) / 1000.0
    med1_ = medida_["1_a_formula_nao_contem_u"]
    ck_("g1", "dM/du = 0 por construcao: a forma do Grande Atrator so' tem o raio como argumento (a unidade da massa do neutrino nao aparece); M/R e a velocidade caracteristica == a medida pinada a 1e-12", forma_.__code__.co_varnames == ("R_",) and _v405_rel(beta_, medida_["beta_runtime"]) <= 1e-12 and _v405_rel(por_mpc_ * 2.0 * beta_ ** 2, med1_["form_por_Mpc_Msun"]) <= 1e-12 and _v405_rel(v_kms_, med1_["v_caracteristica_kms"]) <= 1e-12, [2.0 * beta_ ** 2 * por_mpc_, v_kms_])
    linhas_ = medida_["2_a_mesma_parede"]["linhas"]; res_ = []; razoes_ = []
    for l_ in linhas_:
        M_ = float(l_["M_Msun"]); rs_ = 2.0 * G_NEWTON * M_ * MSUN / C_LIGHT ** 2; tau_ = 4.0 * _m405.pi * G_NEWTON * M_ * MSUN / C_LIGHT ** 3; RB_ = C_LIGHT / (beta_ / tau_)
        res_.append(abs(fluxo_(M_) - M_) / M_); razoes_.append(RB_ / rs_)
    ck_("g2", "M = M: a lei de fluxo de junho, M = (c^2/4piG).beta.R_B, com R_B = c/Gamma_B, Gamma_B = beta/tau e o tempo do monopolo tau = 4piGM/c^3, devolve a massa dada nas tres ancoras, com residuo de maquina: beta cancela, a massa fixa o tempo", len(res_) == 3 and max(res_) <= 1e-14, res_)
    ck_("g3", "R_B/r_s = 2pi/beta para toda massa (a 1e-12)", all(abs(r_ / (2.0 * _m405.pi / beta_) - 1.0) <= 1e-12 for r_ in razoes_), razoes_)
    MA_ = (core_.get("mode_A") or {}).get("M_TGL_Msun"); MB_ = (core_.get("mode_B") or {}).get("M_TGL_Msun")
    med3_ = medida_["3_piso_de_definicao"]
    piso_ = (MA_ / MB_ - 1.0) if (isinstance(MA_, float) and isinstance(MB_, float) and MB_ > 0.0) else None
    ck_("g4", "o piso de definicao: as duas massas que o verdict do core publica (masses_Msun: mode_A e mode_B) diferem so' pela definicao do raio; a razao == a medida pinada a 1e-12 e o piso e' maior que 1/3: nenhuma conta de massa e' mais fina que isso enquanto a bacia nao tiver definicao fixada sem olhar a massa", piso_ is not None and piso_ > 1.0 / 3.0 and _v405_rel(1.0 + piso_, med3_["razao_A_sobre_B"]) <= 1e-12, piso_)
    anc_ = float(linhas_[0]["M_Msun"]); med4_ = medida_["4_precisao_necessaria"]; lo_, hi_ = GA_ACCEPTED_WINDOW_Msun
    sig_f_ = ((anc_ - MA_) / 5.0 / anc_) if isinstance(MA_, float) else None; sig_b_ = beta_ / 5.0; dec_ = _m405.log10(hi_ / lo_)
    ck_("g5", "a precisao necessaria: 5 sigma entre a forma e a ancora pedem a massa da bacia a esta fracao, e 5 sigma para a resposta de materia pedem beta/5; a janela tem estas decadas; tudo == a medida pinada a 1e-12", sig_f_ is not None and _v405_rel(sig_f_, med4_["para_5sigma_entre_form_R57_e_ancora"]["sigma_relativo_na_ancora"]) <= 1e-12 and _v405_rel(sig_b_, med4_["resposta_de_materia_beta"]["sigma_relativo_para_5sigma"]) <= 1e-12 and _v405_rel(dec_, med4_["decadas_da_janela"]) <= 1e-12, [sig_f_, sig_b_, dec_])
    linha_ = [x_ for x_ in ((core_.get("joint_coincidence_result_v3") or {}).get("inventory") or []) if isinstance(x_, dict) and x_.get("id") == "ga_mass_window"]
    ck_("g6", "o selado fica: a linha ga_mass_window da tabela conjunta segue A3_APOSENTADO e nao admissivel; GA_WINDOW_STATUS segue dizendo NOT_NONCIRCULAR_EVIDENCE; a auditoria da forma segue com o mesmo veredito: a classe nova vai AO LADO, neste registro", len(linha_) == 1 and linha_[0].get("rule") == "A3_APOSENTADO" and linha_[0].get("admissible") is False and "NOT_NONCIRCULAR_EVIDENCE" in GA_WINDOW_STATUS and str((core_.get("ga_mass_audit") or {}).get("verdict")).startswith("GA_MASS_FORM_RETIRED"), (linha_[0].get("rule") if linha_ else None))
    vals_ = {"beta": beta_, "M_sobre_R_Msun_por_Mpc": 2.0 * beta_ ** 2 * por_mpc_, "v_caracteristica_kms": v_kms_, "dM_du": 0.0, "residuos_M_igual_M": res_, "R_B_sobre_r_s": razoes_, "dois_pi_sobre_beta": 2.0 * _m405.pi / beta_, "M_A_Msun": MA_, "M_B_Msun": MB_, "piso_de_definicao": piso_,
             "sigma_relativo_forma_ancora": sig_f_, "sigma_relativo_resposta_beta": sig_b_, "decadas_da_janela": dec_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v405_ga_registro(r_, core_, spec_):
    """v405 -- o registro por especificacao da reclassificacao do Grande Atrator: o MOTOR (_v392_registro) le as fontes, a fala, os termos do kernel e as checagens; aqui se somam as quatro medidas em runtime, a errata do parecer conferida contra os bytes da fonte pinada e a guarda das frases. Fail-closed: qualquer elo derruba a selagem; excecao vira falha visivel; nao move o gate."""
    import json as _j405
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core_)
    try:
        ok_m_, det_m_, b_m_ = _v392_fonte_bytes(spec_["fonte_medida"])
        ok_p_, det_p_, b_p_ = _v392_fonte_bytes(spec_["fonte_parecer"])
        med_ = _j405.loads(b_m_.decode("utf-8")) if ok_m_ else None
        mec_ = v405_ga_mechanics(beta_rt_, core_, med_) if med_ else {"passed": False, "checks": [], "values": {}, "n_checks": 0}
        errata_ok_ = bool(ok_p_ and spec_["extras"]["errata_ao_lado_do_parecer_da_entrega_005"] in b_p_.decode("utf-8"))
    except Exception as e_:   # noqa: BLE001
        mec_ = {"passed": False, "checks": [], "values": {}, "n_checks": 0, "erro": repr(e_)[:300]}; errata_ok_ = False
    txt_ = _j405.dumps({k_: r_.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "extras")}, ensure_ascii=False)
    viol_ = list(_v405_guarda_frases(txt_)) + list(_v405_guarda_frases(str(r_.get("verdict"))))
    motor_ok_ = r_.get("all_verified") is True
    ok_ = bool(motor_ok_ and beta_ok_ and mec_["passed"] and mec_["n_checks"] == spec_["n_checks_runtime"] and errata_ok_ and not viol_)
    r_.update(mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], beta_ok=beta_ok_, runtime_executed=True, errata_do_parecer_ok=errata_ok_, guarda_frases_violacoes=viol_[:5], all_verified=ok_)
    if motor_ok_ and not ok_:
        r_["verdict"] = "%s__NOT_SEALED_THIS_RUN__RUNTIME_MEASURES_OR_BETA_OR_ERRATUM__GATE_UNMOVED" % spec_["veredito_prefixo"]
    return r_


def v405_gap_mechanics(beta_, core_, c_):
    """v405 -- O GAP (a secao O GAP da pedra PontoZeroDoPsion; registro gap_v405, ao lado): o lock minimo 1 - P tem gap espectral 1, em qualquer espaco de Hilbert; na unidade posta o gap vale u, o E0 da Lei do Diminuto, com a tonica meio-tom acima; num estado a um angulo theta o valor esperado e' sen^2(theta); no angulo de Miguel, beta; na unidade posta esse valor esperado e' Delta = beta.u, a energia retida, que NAO e' gap; a tonica e' Delta/alfa; a massa e' a projecao transversal de Delta; o psion e' sqrt2.Delta; o tempo do retido, Gamma_B e Q; a medida negativa (E_fluxo nao e' E0); tau nao e' t_P; kappa so' como hipotese; K nao depende da inclinacao. Devolve {passed, checks, values, n_checks}."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m405.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "x0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    u_ = float(c_["u_posto_eV"]); hb_, ev_, G_, cl_ = float(c_["hbar_si"]), float(c_["eV_J"]), float(c_["G_si"]), float(c_["c_si"]); s4_ = _m405.sin(_m405.pi / 4.0)
    om3_ = (1.0, 0.0, 0.0); chi3_ = (0.0, 1.0, 0.0)                                          # um modelo de dimensao 3: os lemas valem em qualquer espaco de Hilbert
    ip_ = lambda a_, b_: sum(x_ * y_ for x_, y_ in zip(a_, b_))
    lockv_ = lambda v_: tuple(x_ - ip_(om3_, v_) * o_ for x_, o_ in zip(v_, om3_))            # lockDe: 1 - P, com P a projecao sobre a reta de Omega
    psi_ = lambda th_: tuple(_m405.cos(th_) * a_ + _m405.sin(th_) * b_ for a_, b_ in zip(om3_, chi3_))
    lock_ = lambda th_: ip_(psi_(th_), lockv_(psi_(th_)))                                    # o valor esperado do lock no estado a um angulo theta de Omega
    thetas_ = (0.0, 0.1, _m405.pi / 6.0, _m405.pi / 4.0, 1.2)
    ck_("x1", "★★★ o_lock_tem_gap_um e lock_no_angulo, num modelo de dimensao 3 (os lemas valem em qualquer espaco de Hilbert): o lock minimo 1 - P vale 0 em Omega e 1 no ortogonal (gap espectral 1), e num estado a um angulo theta de Omega tem valor esperado sen^2(theta) em cinco angulos",
        lockv_(om3_) == (0.0, 0.0, 0.0) and lockv_(chi3_) == chi3_ and all(abs(lock_(t_) - _m405.sin(t_) ** 2) <= 1e-15 for t_ in thetas_), [lock_(t_) for t_ in thetas_])
    th_m_ = _m405.asin(_m405.sqrt(beta_)); dl_ = beta_ * u_
    ck_("x2", "★★★ lock_no_angulo_de_miguel, o_retido_e_lido_do_angulo_de_miguel e o_retido_e_o_valor_esperado_do_lock: no angulo de Miguel o valor esperado do lock e' beta (|erro| <= 1e-14 relativo) e, na unidade posta, u.<lock> = sen^2(theta_M).u = beta.u = Delta, a energia retida; Delta carrega u, e nada aqui fixa u (U_E_NOT_DERIVED fica)",
        _v405_rel(lock_(th_m_), beta_) <= 1e-14 and _v405_rel(u_ * lock_(th_m_), dl_) <= 1e-14 and _v405_rel(_m405.sin(th_m_) ** 2 * u_, dl_) <= 1e-14, [th_m_, dl_])
    sq_e_ = _m405.exp(0.5); alfa_ = beta_ / sq_e_; m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")
    ck_("x3", "★★ a_tonica_e_o_retido_sobre_alpha e a_massa_e_a_projecao_do_retido: a tonica e' Delta/alfa = sqrt e.u (|erro| <= 1e-15 relativo) e a massa e' Delta.sen45 = o m_nu do programa a 1e-12 relativo; ler alfa como a inscricao eletrica que leva o retido a tonica e' do operador [ONTO]",
        _v405_rel(dl_ / alfa_, sq_e_ * u_) <= 1e-15 and isinstance(m_core_, float) and _v405_rel(dl_ * s4_ * 1000.0, m_core_) <= float(c_["rel_tol"]), [dl_ / alfa_, dl_ * s4_ * 1000.0])
    om_ = _m405.sqrt(2.0 * beta_ * (beta_ * u_ ** 2)); tau_ = 1.0 / dl_
    ck_("x4", "★★★ o_psion_e_raiz_de_dois_retidos e a_frequencia_do_sistema_e_a_do_psion_iff: omega do psion = sqrt2.Delta (|erro| <= 1e-15 relativo); sqrt2/tau = omega do psion para tau = 1/Delta e, no controle negativo, nao para tau = 2/Delta nem tau = 1/(2.Delta): e' um se e so' se",
        _v405_rel(om_, _m405.sqrt(2.0) * dl_) <= 1e-15 and _v405_rel(_m405.sqrt(2.0) / tau_, om_) <= 1e-15 and _v405_rel(_m405.sqrt(2.0) / (2.0 * tau_), om_) > 0.1 and _v405_rel(_m405.sqrt(2.0) / (0.5 * tau_), om_) > 0.1, [om_, tau_])
    gam_ = beta_ / tau_; q_ = om_ / gam_
    qs_ = [(_m405.sqrt(2.0 * beta_ * (beta_ * w_ ** 2))) / (beta_ * (beta_ * w_)) for w_ in (0.5, 1.0, 7.0)]
    ck_("x5", "★ a_taxa_de_fronteira_no_psion e a_qualidade_nao_depende_da_unidade: (1/2).beta.tau.omega^2 = beta/tau = Gamma_B (|erro| <= 1e-15 relativo) e Q = omega/Gamma_B = sqrt2/beta, numero puro: igual para u em {0,5; 1; 7}",
        _v405_rel(0.5 * beta_ * tau_ * om_ ** 2, gam_) <= 1e-15 and _v405_rel(q_, _m405.sqrt(2.0) / beta_) <= 1e-15 and all(_v405_rel(x_, q_) <= 1e-14 for x_ in qs_), [gam_, q_])
    ck_("x6", "★ o_ponto_zero_autoconsistente_e_o_retido e o_psion_e_a_projecao_do_modo: (1/2).(2/tau) = Delta e omega do psion = (2/tau).sen45 (|erro| <= 1e-15 relativo): mais uma leitura do mesmo sen 45, por aritmetica; algebra da definicao de tau",
        _v405_rel(0.5 * (2.0 / tau_), dl_) <= 1e-15 and _v405_rel((2.0 / tau_) * s4_, om_) <= 1e-15, [0.5 * (2.0 / tau_)])
    ck_("x7", "★ o_relogio_do_retido: kappa entra como antecedente, testemunha (regra do operador de 24/08/2026, TheHorizonRate.lean): SE kappa da' uma volta em tau, entao kappa/2pi = Delta; nada aqui e' busca de valor; conferencia por construcao, a conta devolve o proprio antecedente",
        _v405_rel((2.0 * _m405.pi / tau_) / (2.0 * _m405.pi), dl_) <= 1e-15, "como antecedente")
    tau_s_ = hb_ / (dl_ * ev_); e_fluxo_j_ = cl_ ** 5 * tau_s_ / (4.0 * _m405.pi * G_); e_fluxo_ev_ = e_fluxo_j_ / ev_; t_p_ = _m405.sqrt(hb_ * G_ / cl_ ** 5)
    ck_("x8", "★★ a MEDIDA NEGATIVA: sob esta leitura, E_fluxo = c^5.tau/(4.pi.G) vale da ordem de 10^57 eV (56 < log10 < 58): NAO e' E0; a ponte E_fluxo = E0 do Kimi NAO vale aqui",
        56.0 < _m405.log10(e_fluxo_ev_) < 58.0 and e_fluxo_ev_ / u_ > 1.0e50, [e_fluxo_ev_])
    ck_("x9", "★★ tau = hbar/Delta e' tempo proprio, nao t_P: tau/t_P > 1e25; ler tempoDoRetido como o tau* do sistema e' leitura [ONTO] a ratificar pelo operador, e nao mexe no ramo canonico",
        tau_s_ / t_p_ > 1.0e25, [tau_s_, t_p_])
    incl_ = (0.01, 0.05, 0.2, 0.6); ks_ = [(4.0 * 9.8 / (0.1 * a_)) * (1.5 * 1.0 * 9.8 * 0.1 * a_) for a_ in incl_]
    ck_("x10", "★ o disco: o invariante K = Omega^2.E nao depende da inclinacao (Omega^2 = 4g/(a.ang), E = (3/2).M.g.a.ang, um disco de teste, em quatro inclinacoes, |erro| <= 1e-12 relativo), logo o angulo nao fixa K: K segue [OPEN]; conferencia por construcao: a inclinacao cancela na conta",
        all(_v405_rel(k_, 6.0 * 1.0 * 9.8 ** 2) <= 1e-12 for k_ in ks_), [ks_[0]])
    e0_rg_ = ((core_.get("lei_do_diminuto_v405") or {}).get("values") or {}).get("E0_eV"); tn_rg_ = ((core_.get("lei_do_diminuto_v405") or {}).get("values") or {}).get("tonica_eV")
    ck_("x11", "★★★ o_gap_com_unidade e o fecho the_gap_closes: o gap espectral na unidade posta e' u, o E0 da Lei do Diminuto (o E0 do registro lei_do_diminuto_v405 == u a 1e-12 relativo), e a tonica fica meio-tom acima dele (tonica.e^(-1/2) = u); Delta NAO e' gap: o gap e' 1/beta vezes Delta",
        isinstance(e0_rg_, float) and isinstance(tn_rg_, float) and _v405_rel(e0_rg_, u_) <= float(c_["rel_tol"]) and _v405_rel(tn_rg_ * _m405.exp(-0.5), u_) <= float(c_["rel_tol"]) and _v405_rel(u_ / dl_, 1.0 / beta_) <= 1e-15 and u_ / dl_ > 10.0, [u_, u_ / dl_])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "gap_espectral_eV": u_, "gap_sobre_Delta": u_ / dl_, "theta_M": th_m_, "Delta_eV": dl_, "tau_por_eV": tau_, "tau_s": tau_s_, "Gamma_B_eV": gam_, "Q": q_, "omega_psion_eV": om_, "tonica_eV": dl_ / alfa_, "E_fluxo_eV": e_fluxo_ev_, "log10_E_fluxo_eV": _m405.log10(e_fluxo_ev_), "E_fluxo_sobre_E0": e_fluxo_ev_ / u_, "tau_sobre_t_planck": tau_s_ / t_p_, "m_nu_meV_core": m_core_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


def _v405_gap_registro(r_, core_, spec_):
    """v405 -- o registro por especificacao gap_v405: o MOTOR (_v392_registro) le as fontes, a fala, os termos do kernel e as checagens; aqui se somam o calculo em runtime e a guarda das frases. Fail-closed: qualquer elo derruba a selagem; excecao vira falha visivel; nao move o gate."""
    import json as _j405
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core_)
    try:
        mec_ = v405_gap_mechanics(beta_rt_, core_, spec_["constants"])
    except Exception as e_:   # noqa: BLE001
        mec_ = {"passed": False, "checks": [], "values": {}, "n_checks": 0, "erro": repr(e_)[:300]}
    txt_ = _j405.dumps({k_: r_.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "extras")}, ensure_ascii=False)
    viol_ = list(_v405_guarda_frases(txt_)) + list(_v405_guarda_frases(str(r_.get("verdict"))))
    motor_ok_ = r_.get("all_verified") is True
    ok_ = bool(motor_ok_ and beta_ok_ and mec_["passed"] and mec_["n_checks"] == spec_["n_checks_runtime"] and not viol_)
    r_.update(mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], beta_ok=beta_ok_, runtime_executed=True, guarda_frases_violacoes=viol_[:5], all_verified=ok_)
    if motor_ok_ and not ok_:
        r_["verdict"] = "%s__NOT_SEALED_THIS_RUN__RUNTIME_MEASURES_OR_BETA__GATE_UNMOVED" % spec_["veredito_prefixo"]
    return r_


_V405_MECANICAS = {"ponte": v405_ponte_mechanics, "tensao": v405_tensao_mechanics, "identidade": v405_identidade_mechanics, "observador": v405_observador_mechanics, "diminuto": v405_diminuto_mechanics, "tonica": v405_tonica_mechanics, "disco": v405_disco_mechanics, "psion": v405_psion_mechanics}


def _v405_formal(core, c_, txt_):
    """A evidencia FORMAL do registro, lida do kernel do PROPRIO rito: a escada exata, a composicao e os teoremas do contrato (bandeira True, trio, proveniencia no modulo da pedra), os termos antigos que a pedra cita (no trio, com a proveniencia que o compilador emite),
    a fonte da pedra por sha256 (embutida == contrato == hash formal do rito), as falas de 30/10 a 01/11 por sha256, o TEXTO-CONTEXTO no kernel embutido e as duas guardas de texto (a P18 e a das frases, v405). Devolve um dict; `formal` e' o conjunto."""
    import hashlib, json as _j405
    kf_ = core.get("kernel_formalization") or {}; axr_ = kf_.get("axiom_report") or {}; src_ = kf_.get("declaration_sources_v394") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    lad_ = core.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    per_ = {th_: bool(em_trio_(th_) and kf_.get(fl_) is True and src_.get(th_) == c_["stone"]["path"]) for th_, fl_ in c_["theorems"].items()}
    sup_ = {n_: bool(em_trio_(n_) and src_.get(n_) == p_) for n_, p_ in c_["support"].items()}
    cit_ = {n_: bool(em_trio_(n_) and src_.get(n_) == p_) for n_, p_ in c_["cited_outside"].items()}
    aux_ = {n_: bool(em_trio_(n_) and src_.get(n_) == c_["stone"]["path"]) for n_ in c_["auxiliaries_outside_the_composition"]}
    body_ = _EMBEDDED_KERNEL_FILES.get(c_["stone"]["path"])
    src_ok_ = bool(isinstance(body_, str) and hashlib.sha256(body_.encode("utf-8")).hexdigest() == c_["stone"]["sha256"] and (kf_.get("formal_files_sha256") or {}).get(c_["stone"]["path"]) == c_["stone"]["sha256"])
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V405_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    unc_th_, unc_fl_ = c_["unconditional"]["theorem"], c_["unconditional"]["flag"]
    unc_ = {"theorem": unc_th_, "flag": unc_fl_, "flag_true": kf_.get(unc_fl_) is True, "axioms": axr_.get(unc_th_), "in_trio": em_trio_(unc_th_), "declared_in": src_.get(unc_th_), "in_kernel": bool(per_.get(unc_th_)),
            "composition": "NO_CERTIFICATE_AS_HYPOTHESIS" if not c_.get("named_hypotheses_in_the_statement") else "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT"}
    key_th_, key_fl_ = c_["key_theorem"]["theorem"], c_["key_theorem"]["flag"]
    key_ = {"theorem": key_th_, "flag": key_fl_, "flag_true": kf_.get(key_fl_) is True, "in_trio": em_trio_(key_th_), "declared_in": src_.get(key_th_), "in_kernel": bool(per_.get(key_th_)), "statement": c_["key_statement"]}
    cx_ = c_["context"]; cb_ = _EMBEDDED_KERNEL_FILES.get(cx_["path"])
    ctx_ = {"path": cx_["path"], "needles": list(cx_["needles"]), "text_in_embedded_kernel": bool(isinstance(cb_, str) and all(n_ in cb_ for n_ in cx_["needles"]))}
    ctx_["ok"] = bool(ctx_["text_in_embedded_kernel"])
    guarda_ = list(_v392_guarda_texto(_j405.dumps(txt_, ensure_ascii=False))) + list(_v405_guarda_frases(_j405.dumps(txt_, ensure_ascii=False)))   # as duas guardas de texto: a P18 (v392) e a das frases que afirmam demais (v405)
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and sup_ and all(sup_.values()) and all(cit_.values()) and all(aux_.values()) and src_ok_ and all(ver_.values()) and key_["in_kernel"] and unc_["in_kernel"] and ctx_["ok"] and not guarda_)
    return {"exact_ladder": exact_, "formal_theorems": per_, "support_theorems": sup_, "cited_outside": cit_, "auxiliaries_outside_the_composition": aux_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "unconditional": unc_, "key_theorem": key_,
            "context": ctx_, "guarda": guarda_, "formal": formal_}


_V405_RECUSA = "TGL_%s_V405__REFUSED_%s__GATE_UNMOVED"


def _v405_registro(core, chave_, nome_, tag_):
    """v405 -- o miolo comum dos OITO registros de pedra com FUNCAO: le o kernel do rito (evidencia FORMAL), confere o beta (alfa x raiz de e, nunca literal), CALCULA a mecanica da pedra e sela. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate."""
    c_ = _V405_CONTRACTS[chave_]; t_ = _V405_TEXTS[chave_]; mec_ = _V405_MECANICAS[chave_]
    f_ = _v405_formal(core, c_, t_)
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "estatuto": t_["estatuto"], "exact_ladder": f_["exact_ladder"], "formal_theorems": f_["formal_theorems"], "support_theorems": f_["support_theorems"], "cited_outside": f_["cited_outside"], "embedded_source_ok": f_["embedded_source_ok"],
            "inscriptions": f_["inscriptions"], "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": f_["unconditional"], "key_theorem": f_["key_theorem"], "context": f_["context"],
            "runtime_executed": False, "does_not_gate_core": True, "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"], "guarda_p18_violacoes": f_["guarda"][:5], "nome_do_operador": c_["nome_do_operador"]}
    out_.update(t_["extras"])
    if not f_["formal"]:
        out_["verdict"] = _V405_RECUSA % (tag_, "FORMAL_OR_SOURCE_EVIDENCE")
    elif not beta_ok_:
        out_["verdict"] = _V405_RECUSA % (tag_, "BETA_IS_NOT_ALPHA_SQRT_E")
    else:
        try:
            mec_r_ = mec_(beta_rt_, core, c_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_r_["passed"], "n_checks": mec_r_["n_checks"], "checks": mec_r_["checks"]}, values=mec_r_["values"], all_verified=bool(mec_r_["passed"]))
            out_["verdict"] = (t_["veredito_ok"] if mec_r_["passed"] else _V405_RECUSA % (tag_, "MECHANICS_CHECK_FAILED"))
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V405_RECUSA % (tag_, "RUNTIME_ERROR")
    core[nome_] = out_
    return out_


def ponte_da_massa_v405(core):
    """v405 -- A PONTE DA MASSA (nome do operador, 01/11/2026): lida no PONTO REAL do main, logo depois dos tres registros da v404. Le do kernel do PROPRIO rito a pedra (bandeira, trio, modulo), os termos que ela cita, a fonte por sha256, as falas de 30/10 a 01/11 e o cabecalho da pedra no kernel embutido;
    e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime, a FORMA da massa dadas as leituras (m = beta.sqrt2/2.u com u = 1 eV POSTO), o discriminante, os campos fechados e a errata E10 AO LADO do angle_status. Fail-closed em cada elo; nao move o gate. Validade no kernel nao e' creditacao."""
    return _v405_registro(core, "ponte", "ponte_da_massa_v405", "PONTE_DA_MASSA")


def massa_tensao_pura_v405(core):
    """v405 -- MASSA = TENSAO PURA (nome do operador, 01/11/2026): o emprestimo construido (uma volta kappa.P = 2pi, o periodo fiel e' teorema; a parcela nunca quita), a massa como residuo do acoplamento e o principal como a energia RETIDA projetada no transversal; a ligacao que falta dita (tensao, atrito e temperatura tem termo; magnetismo nao). Fail-closed; nao move o gate."""
    return _v405_registro(core, "tensao", "massa_tensao_pura_v405", "MASSA_TENSAO_PURA")


def identidade_v405(core):
    """v405 -- IDENTIDADE (nome do operador, 30/10/2026; a lei do fecho, 01/11/2026): um fato sobre projecoes no estado traco normalizado -- [eu sou] = [o que sou] <=> P = 1 <=> ([forma = conteudo] e P != 0); o «senao», a selecao unica, os controles (o vazio e a face), coisa julgada -- conferido em matrizes pequenas, sem biblioteca; que esse fato SEJA a identidade e' a leitura do operador [INPUT/ONTO], tipada como modelo. Fail-closed; nao move o gate."""
    return _v405_registro(core, "identidade", "identidade_v405", "IDENTIDADE")


def observador_terminal_v405(core):
    """v405 -- OBSERVADOR = TERMINAL (nome do operador, 31/10/2026): o posto do observador e' o terminal; a fusao de tudo num so' posto e' o colapso e o colapso e' um Um posto do kernel (nao pressuposto; pagou perda; dois pontos fixos: o posto e o abismo); sem o par nao ha posto; o terminal le 1. Fail-closed; nao move o gate."""
    return _v405_registro(core, "observador", "observador_terminal_v405", "OBSERVADOR_TERMINAL")


def lei_do_diminuto_v405(core):
    """v405 -- A LEI DO DIMINUTO (nome do operador, 01/11/2026): o meio-tom pinado e^(-1/2), a tonica definida (beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha), o diminuto que pousa em E0 = u (identidade algebrica, que nao fixa u), e A FORMULA DA MASSA m = U.alfa.e^(1/2).sqrt2/2 (o mesmo numero da v404; dadas as entradas, a FORMA e' teorema). Fail-closed; nao move o gate."""
    return _v405_registro(core, "diminuto", "lei_do_diminuto_v405", "LEI_DO_DIMINUTO")


def tonica_do_hamiltoniano_v405(core):
    """v405 -- A TONICA DO HAMILTONIANO (nome do operador, 01/11/2026): o no-go (a forma nao fixa E0: o valor absoluto e' livre, nenhuma funcao da inscricao a devolve), que NAO cai: ele se localiza no Um posto (a tonica pousa em E0 = u, identidade algebrica); as identidades da rota do monopolo e da leitura autoconsistente; alfa medida por dentro, nunca derivada. Fail-closed; nao move o gate."""
    return _v405_registro(core, "tonica", "tonica_do_hamiltoniano_v405", "TONICA_DO_HAMILTONIANO")


def disco_de_euler_v405(core):
    """v405 -- O DISCO DE EULER (nome do operador, 01/11/2026): sob a lei canonica com o invariante Omega^2.E = K a perda e' constante e o disco para em tempo finito; antes da parada a frequencia nao tem cota (a inscricao do zero no infinito); o corte da ressonancia residual E^3 = hbar^2.K; a parede nomeada K = (e^(1/2).U)^3/hbar^2; beta do acoplamento. Fail-closed; nao move o gate."""
    return _v405_registro(core, "disco", "disco_de_euler_v405", "DISCO_DE_EULER")


def ponto_zero_do_psion_v405(core):
    """v405 -- O PONTO ZERO DO PSION (nome do operador, 01/11/2026): sob a leitura R = beta.u^2 (o pagamento lido como curvatura) e com a dispersao do Tratado, (1/2).hbar.omega = beta.sen45.u = a massa do neutrino do programa (a segunda leitura do sen 45, que coincide com a projecao transversal pela aritmetica (1/2).sqrt2 = sen45); Tetelestai e' o limite da cobranca; em SI os numeros ficam registrados. Fail-closed; nao move o gate."""
    return _v405_registro(core, "psion", "ponto_zero_do_psion_v405", "PONTO_ZERO_DO_PSION")


# ---- v405: os contratos (derivados do build e do core da v404 selada), os textos, as fontes pinadas, as falas de 30/10 a 01/11, o ensaio e os registros por spec
_V405_CONTRACTS = {'ponte': {'stone': {'path': 'TGLExt/PonteDaMassa.lean',
                     'sha256': '51f3d207eb5bcba5ac61282eb859b339a419d6c083d3529548c811ab537e74a0',
                     'module': 'TGLExt.PonteDaMassa'},
           'nome_do_operador': 'Ponte da Massa',
           'unconditional': {'theorem': 'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento', 'flag': 'ext_pdm405_0033'},
           'key_theorem': {'theorem': 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form', 'flag': 'ext_pdm405_0014'},
           'key_statement': 'massa_derivada_eq_form: under the reading massaDerivada (a definition), the mass as the derivative of the transverse '
                            'projection at the self-conjugate point EQUALS the neutrino form beta . sin45 . E0; '
                            'a_transicao_existe_para_todo_acoplamento: for every coupling the structure is INHABITED with E0 = 1 (the posted One), '
                            'theta = pi/4 (written, the reading) and m = beta . sqrt2/2: the fields close, the reading does not become a theorem',
           'theorems': {'TGLExt.PonteDaMassa.projecao_hasDerivAt': 'ext_pdm405_0046',
                        'TGLExt.PonteDaMassa.half_sq': 'ext_pdm405_0040',
                        'TGLExt.PonteDaMassa.deriv_eq_projecao_at_half': 'ext_pdm405_0036',
                        'TGLExt.PonteDaMassa.projecao_eq_deriv_iff': 'ext_pdm405_0045',
                        'TGLExt.PonteDaMassa.energia_retida_eq': 'ext_pdm405_0039',
                        'TGLExt.PonteDaMassa.retida_add_transmitida': 'ext_pdm405_0047',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.theta_eq_pi_div_four': 'ext_pdm405_0030',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form': 'ext_pdm405_0014',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul': 'ext_pdm405_0013',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_projecao': 'ext_pdm405_0015',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_sqrt_two_mul_proporcional': 'ext_pdm405_0016',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_pos': 'ext_pdm405_0017',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_proporcional_ne_derivada': 'ext_pdm405_0018',
                        'TGLExt.PonteDaMassa.controle_nao_autoconjugado': 'ext_pdm405_0035',
                        'TGLExt.PonteDaMassa.peso_da_face_absoluta': 'ext_pdm405_0043',
                        'TGLExt.PonteDaMassa.angulo_derivado_do_absoluto': 'ext_pdm405_0034',
                        'TGLExt.PonteDaMassa.transicao_derivada_le_o_absoluto': 'ext_pdm405_0049',
                        'TGLExt.PonteDaMassa.massa_da_transicao_derivada': 'ext_pdm405_0041',
                        'TGLExt.PonteDaMassa.umPosto_pos': 'ext_pdm405_0051',
                        'TGLExt.PonteDaMassa.massa_no_um_posto': 'ext_pdm405_0042',
                        'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento': 'ext_pdm405_0033'},
           'support': {'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
                       'TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
                       'TGLExt.ProjecaoTransversalDaMeiaNat.half_from_self_conjugate': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
                       'TGLExt.Posto.sin_sq_thetaMiguel': 'TGLExt/Posto.lean',
                       'TGLExt.thetaMiguel': 'TGLExt/TheVerbalCoupling.lean',
                       'TGLExt.absolute_faces_half': 'TGLExt/ContinuousModularZero.lean'},
           'cited_outside': {},
           'auxiliaries_outside_the_composition': [],
           'context': {'path': 'TGLExt/PonteDaMassa.lean', 'needles': ['# A PONTE DA MASSA', 'a_transicao_existe_para_todo_acoplamento']},
           'named_hypotheses_in_the_statement': False,
           'expected_ladder': 10066,
           'n_flags': 51,
           'n_flags_total': 368,
           'verbatins': ['v405_cun_493172b80e96eb60', 'v405_cun_1f16a74c05d9d4cb', 'v405_cun_2c3da184ebefc7c4'],
           'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
           'constants': {'u_posto_eV': 1.0,
                         'rel_tol': 1e-12,
                         'hbar_c_eV_m': 1.973269804e-07,
                         'G_si': 6.6743e-11,
                         'c_si': 299792458.0,
                         'hbar_si': 1.054571817e-34,
                         'eV_J': 1.602176634e-19,
                         'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                         'half_nat_sha16': 'c23ce83106c69ff6',
                         'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na geracao "
                                 "com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca derivada); G, "
                                 "c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros em SI (nenhum entra "
                                 'em veredito)',
                         'alpha_runtime': 0.0072973525693},
           'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                             'TGLExt/MassaTensaoPura.lean',
                             'TGLExt/Identidade.lean',
                             'TGLExt/ObservadorTerminal.lean',
                             'TGLExt/LeiDoDiminuto.lean',
                             'TGLExt/TonicaDoHamiltoniano.lean',
                             'TGLExt/DiscoDeEuler.lean',
                             'TGLExt/PontoZeroDoPsion.lean'],
           'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                        'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                        'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                        'm_nu_meV_v404': 8.507414099900329,
                        'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'tensao': {'stone': {'path': 'TGLExt/MassaTensaoPura.lean',
                      'sha256': '9ec48bf6d608ae5a9d85c5c28caa21c972ba9847ec05703f733b582a17a9956b',
                      'module': 'TGLExt.MassaTensaoPura'},
            'nome_do_operador': 'Massa=tensão pura',
            'unconditional': {'theorem': 'TGLExt.MassaTensaoPura.massa_e_tensao_pura', 'flag': 'ext_mtp405_0039'},
            'key_theorem': {'theorem': 'TGLExt.MassaTensaoPura.principal_derivado', 'flag': 'ext_mtp405_0041'},
            'key_statement': 'principal_derivado: the principal of the derived loan is beta . (sqrt2/2) . u; massa_e_tensao_pura: the principal is '
                             'the RETAINED energy (beta . u) projected on the transverse (sqrt2/2), an algebraic identity under the reading '
                             "massaDerivada; the name is the operator's and the reading is [ONTO]",
            'theorems': {'TGLExt.MassaTensaoPura.massa_e_produto_do_acoplamento': 'ext_mtp405_0038',
                         'TGLExt.MassaTensaoPura.foton_sem_massa': 'ext_mtp405_0035',
                         'TGLExt.MassaTensaoPura.acoplamento_positivo_da_massa': 'ext_mtp405_0031',
                         'TGLExt.MassaTensaoPura.massa_e_o_residuo': 'ext_mtp405_0037',
                         'TGLExt.MassaTensaoPura.Emprestimo.uma_volta': 'ext_mtp405_0030',
                         'TGLExt.MassaTensaoPura.Emprestimo.parcela_nunca_quita': 'ext_mtp405_0023',
                         'TGLExt.MassaTensaoPura.Emprestimo.parcela_le_beta': 'ext_mtp405_0021',
                         "TGLExt.MassaTensaoPura.Emprestimo.parcela_le_beta'": 'ext_mtp405_0022',
                         'TGLExt.MassaTensaoPura.Emprestimo.principal_e_beta_vezes': 'ext_mtp405_0027',
                         'TGLExt.MassaTensaoPura.volta_paga_area': 'ext_mtp405_0043',
                         'TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita': 'ext_mtp405_0032',
                         'TGLExt.MassaTensaoPura.emprestimo_derivado_uma_volta': 'ext_mtp405_0034',
                         'TGLExt.MassaTensaoPura.principal_derivado': 'ext_mtp405_0041',
                         'TGLExt.MassaTensaoPura.parcela_derivada_nunca_quita': 'ext_mtp405_0040',
                         'TGLExt.MassaTensaoPura.massa_e_tensao_pura': 'ext_mtp405_0039'},
            'support': {'TGLExt.PonteDaMassa.massa_da_transicao_derivada': 'TGLExt/PonteDaMassa.lean',
                        'ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period': 'TGLExt/O16/PolarMinimalPeriod_v2.lean',
                        'ChatgptAudit.PolarPeriod016.positive_faithful_period': 'TGLExt/O16/PolarMinimalPeriod_v2.lean',
                        'TGLExt.ThePsionAndTheViscosity.charged': 'TGLExt/ThePsionAndTheViscosity.lean',
                        'TGLExt.ThePsionAndTheViscosity.the_charge_never_completes': 'TGLExt/ThePsionAndTheViscosity.lean',
                        'ChatgptAudit.Boost044.boost_segment_quadratic_balance_iff': 'TGLExt/BoostHeatConstruction.lean'},
            'cited_outside': {'TGLExt.ThePsionAndTheViscosity.viscosity_is_the_constant_friction': 'TGLExt/ThePsionAndTheViscosity.lean',
                              'ChatgptAudit.PolarPeriod016.reciprocal_temperature': 'TGLExt/O16/PolarMinimalPeriod_v2.lean',
                              'ChatgptAudit.Coherent023.frameCovectorStress': 'TGLExt/CoherentEinsteinBridge.lean'},
            'auxiliaries_outside_the_composition': [],
            'context': {'path': 'TGLExt/MassaTensaoPura.lean', 'needles': ['# MASSA = TENSÃO PURA', 'massa_e_tensao_pura']},
            'named_hypotheses_in_the_statement': False,
            'expected_ladder': 10066,
            'n_flags': 43,
            'n_flags_total': 368,
            'verbatins': ['v405_cun_fdd78cac25c947a0', 'v405_cun_b31fa435fd03e4dc', 'v405_cun_1f16a74c05d9d4cb'],
            'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
            'constants': {'u_posto_eV': 1.0,
                          'rel_tol': 1e-12,
                          'hbar_c_eV_m': 1.973269804e-07,
                          'G_si': 6.6743e-11,
                          'c_si': 299792458.0,
                          'hbar_si': 1.054571817e-34,
                          'eV_J': 1.602176634e-19,
                          'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                          'half_nat_sha16': 'c23ce83106c69ff6',
                          'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na geracao "
                                  "com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca derivada); G, "
                                  "c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros em SI (nenhum "
                                  'entra em veredito)',
                          'alpha_runtime': 0.0072973525693},
            'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                              'TGLExt/MassaTensaoPura.lean',
                              'TGLExt/Identidade.lean',
                              'TGLExt/ObservadorTerminal.lean',
                              'TGLExt/LeiDoDiminuto.lean',
                              'TGLExt/TonicaDoHamiltoniano.lean',
                              'TGLExt/DiscoDeEuler.lean',
                              'TGLExt/PontoZeroDoPsion.lean'],
            'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                         'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                         'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                         'm_nu_meV_v404': 8.507414099900329,
                         'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'identidade': {'stone': {'path': 'TGLExt/Identidade.lean',
                          'sha256': '94f51e0f80d911ab4375c529be0b906acb40394a4a621f5167f5ef74dbe441f5',
                          'module': 'TGLExt.Identidade'},
                'nome_do_operador': 'Identidade',
                'unconditional': {'theorem': 'TGLExt.Identidade.a_identidade_fecha', 'flag': 'ext_idt405_0020'},
                'key_theorem': {'theorem': 'TGLExt.Identidade.a_lei_inteira', 'flag': 'ext_idt405_0021'},
                'key_statement': 'a fact about projections in the normalized trace state (rho = 1/n): a_lei_inteira: tr(1)/n = tr(P)/n <=> (P = '
                                 '(tr(P)/n).1 and P != 0); a_identidade_fecha: the law (<=> P = 1), the key, and the two negative controls (the void '
                                 "and the face) together; that this fact IS the identity is the operator's reading [ONTO], typed as a model",
                'theorems': {'TGLExt.Identidade.gibbs_absolute': 'ext_idt405_0029',
                             'TGLExt.Identidade.euSou_eq_one': 'ext_idt405_0023',
                             'TGLExt.Identidade.o_um_se_reparte': 'ext_idt405_0035',
                             'TGLExt.Identidade.eu_sou_o_que_sou_iff_nada_resta': 'ext_idt405_0025',
                             'TGLExt.Identidade.resto_posSemidef': 'ext_idt405_0038',
                             'TGLExt.Identidade.nada_resta_iff_fiel': 'ext_idt405_0030',
                             'TGLExt.Identidade.eu_sou_o_que_sou_iff_fiel': 'ext_idt405_0024',
                             'TGLExt.Identidade.one_ne_zero_matrix': 'ext_idt405_0037',
                             'TGLExt.Identidade.forma_igual_conteudo_iff': 'ext_idt405_0028',
                             'TGLExt.Identidade.a_lei_inteira': 'ext_idt405_0021',
                             'TGLExt.Identidade.o_vazio_nao_e': 'ext_idt405_0036',
                             'TGLExt.Identidade.a_face_nao_e_a_identidade': 'ext_idt405_0019',
                             'TGLExt.Identidade.o_nome_e_coisa_julgada': 'ext_idt405_0033',
                             'TGLExt.Identidade.o_posto_e_unico': 'ext_idt405_0034',
                             'TGLExt.Identidade.a_identidade_fecha': 'ext_idt405_0020'},
                'support': {'TGLExt.absoluteRho': 'TGLExt/AbsoluteOne.lean',
                            'TGLExt.absoluteRho_trace': 'TGLExt/AbsoluteOne.lean',
                            'TGLExt.absolute_faces_half': 'TGLExt/ContinuousModularZero.lean',
                            'TGLExt.gibbs': 'TGLExt/FiniteTomita.lean',
                            'TGLExt.Jconj': 'TGLExt/LeftRight.lean',
                            'TGLExt.ResJudicata': 'TGLExt/TheJudgedThing.lean'},
                'cited_outside': {'TGLExt.observing_adds_nothing': 'TGLExt/TheObserverReadsTheAngle.lean'},
                'auxiliaries_outside_the_composition': [],
                'context': {'path': 'TGLExt/Identidade.lean', 'needles': ['# IDENTIDADE', 'a_lei_inteira']},
                'named_hypotheses_in_the_statement': True,
                'expected_ladder': 10066,
                'n_flags': 39,
                'n_flags_total': 368,
                'verbatins': ['v405_cun_f1f8b4011ce96be5', 'v405_cun_f0fdd2c1f770e34a', 'v405_cun_f0ec2867391c644f', 'v405_cun_2c3da184ebefc7c4'],
                'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
                'constants': {'u_posto_eV': 1.0,
                              'rel_tol': 1e-12,
                              'hbar_c_eV_m': 1.973269804e-07,
                              'G_si': 6.6743e-11,
                              'c_si': 299792458.0,
                              'hbar_si': 1.054571817e-34,
                              'eV_J': 1.602176634e-19,
                              'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                              'half_nat_sha16': 'c23ce83106c69ff6',
                              'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na "
                                      "geracao com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca "
                                      "derivada); G, c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros "
                                      'em SI (nenhum entra em veredito)',
                              'alpha_runtime': 0.0072973525693},
                'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                                  'TGLExt/MassaTensaoPura.lean',
                                  'TGLExt/Identidade.lean',
                                  'TGLExt/ObservadorTerminal.lean',
                                  'TGLExt/LeiDoDiminuto.lean',
                                  'TGLExt/TonicaDoHamiltoniano.lean',
                                  'TGLExt/DiscoDeEuler.lean',
                                  'TGLExt/PontoZeroDoPsion.lean'],
                'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                             'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                             'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                             'm_nu_meV_v404': 8.507414099900329,
                             'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'observador': {'stone': {'path': 'TGLExt/ObservadorTerminal.lean',
                          'sha256': '162eeeb8c16cea81f6f0537e46a995f48551656dbc7c1874a98afa0087dc52fb',
                          'module': 'TGLExt.ObservadorTerminal'},
                'nome_do_operador': 'observador=terminal',
                'unconditional': {'theorem': 'TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal', 'flag': 'ext_obt405_0050'},
                'key_theorem': {'theorem': 'TGLExt.ObservadorTerminal.the_fusion_is_not_pressupposed', 'flag': 'ext_obt405_0047'},
                'key_statement': 'the_fusion_is_not_pressupposed: with the pair (structure | abyss) in the state space the total collapse reads 1 on '
                                 'the structure and 0 on the abyss, hence it distinguishes, hence it is a posto; '
                                 'the_observers_posto_is_the_terminal: the terminal is unique, the only fixed point of the reading, res judicata, a '
                                 'posto that paid loss, two fixed points; the terminal reads 1 and the abyss reads 0 on the binary reading '
                                 '(the_fixed_points_read_one_and_zero); beside it, the omega pole of the pair reads 1 on the identity (a homonym: no '
                                 "term links the two; the link is the operator's [ONTO] reading)",
                'theorems': {'TGLExt.ObservadorTerminal.terminal_iff': 'ext_obt405_0040',
                             'TGLExt.ObservadorTerminal.initial_iff': 'ext_obt405_0028',
                             'TGLExt.ObservadorTerminal.the_terminal_is_unique': 'ext_obt405_0055',
                             'TGLExt.ObservadorTerminal.leitor_observes': 'ext_obt405_0035',
                             'TGLExt.ObservadorTerminal.leitor_fixed_iff': 'ext_obt405_0034',
                             'TGLExt.ObservadorTerminal.every_level_reaches_the_terminal': 'ext_obt405_0027',
                             'TGLExt.ObservadorTerminal.distancia_reaches': 'ext_obt405_0025',
                             'TGLExt.ObservadorTerminal.each_reading_consumes_resistance': 'ext_obt405_0026',
                             'TGLExt.ObservadorTerminal.the_collapse_is_the_terminal_point_of_resistance': 'ext_obt405_0042',
                             'TGLExt.ObservadorTerminal.the_position_is_legible': 'ext_obt405_0052',
                             'TGLExt.ObservadorTerminal.the_completed_reading_is_res_judicata': 'ext_obt405_0043',
                             'TGLExt.ObservadorTerminal.rereading_at_the_terminal_adds_nothing': 'ext_obt405_0039',
                             'TGLExt.ObservadorTerminal.the_collapse_fuses_the_structure_into_one_posto': 'ext_obt405_0041',
                             'TGLExt.ObservadorTerminal.the_fusion_is_a_posto': 'ext_obt405_0046',
                             'TGLExt.ObservadorTerminal.the_fusion_paid_loss': 'ext_obt405_0048',
                             'TGLExt.ObservadorTerminal.the_fusion_was_measured_before_being_posited': 'ext_obt405_0049',
                             'TGLExt.ObservadorTerminal.the_fusion_anchors_the_reading': 'ext_obt405_0045',
                             'TGLExt.ObservadorTerminal.the_fusion_is_not_pressupposed': 'ext_obt405_0047',
                             'TGLExt.ObservadorTerminal.the_structure_reads_one': 'ext_obt405_0054',
                             'TGLExt.ObservadorTerminal.the_reading_survives_the_collapse': 'ext_obt405_0053',
                             'TGLExt.ObservadorTerminal.the_two_fixed_points_of_the_collapse': 'ext_obt405_0056',
                             'TGLExt.ObservadorTerminal.the_fixed_points_read_one_and_zero': 'ext_obt405_0044',
                             'TGLExt.ObservadorTerminal.without_the_abyss_the_fusion_reads_as_pressupposed': 'ext_obt405_0058',
                             'TGLExt.ObservadorTerminal.without_the_abyss_no_posto_reads_so': 'ext_obt405_0057',
                             'TGLExt.ObservadorTerminal.the_omega_pole_reads_one': 'ext_obt405_0051',
                             'TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal': 'ext_obt405_0050'},
                'support': {'TGLExt.gravity_is_observed_by_nothing': 'TGLExt/TheCascadeOfObservers.lean',
                            'TGLExt.light_observes_nothing': 'TGLExt/TheCascadeOfObservers.lean',
                            'TGLExt.res_judicata_is_terminal': 'TGLExt/TheJudgedThing.lean',
                            'TGLExt.UmPostoRelacao.posto_paid_loss': 'TGLExt/UmPostoRelacao.lean',
                            'TGLExt.UmPostoRelacao.no_posto_reading_is_pressupposed': 'TGLExt/UmPostoRelacao.lean',
                            'TGLExt.UmPostoRelacao.pressupposed_is_never_posto': 'TGLExt/UmPostoRelacao.lean',
                            'TGLExt.omega_of_one': 'TGLExt/TheAlphaAndTheOmega.lean'},
                'cited_outside': {'TGLExt.TheAxiomAndTheFalseWitness.the_reading_has_two_fixed_points': 'TGLExt/TheAxiomAndTheFalseWitness.lean',
                                  'TGLExt.Fundacao.abismo': 'TGLExt/Fundacao.lean'},
                'auxiliaries_outside_the_composition': [],
                'context': {'path': 'TGLExt/ObservadorTerminal.lean', 'needles': ['# OBSERVADOR = TERMINAL', 'the_observers_posto_is_the_terminal']},
                'named_hypotheses_in_the_statement': False,
                'expected_ladder': 10066,
                'n_flags': 58,
                'n_flags_total': 368,
                'verbatins': ['v405_cun_e4e105fe14615f39', 'v405_cun_08e98d212f11b554', 'v405_cun_a22a54dfc97d9611'],
                'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
                'constants': {'u_posto_eV': 1.0,
                              'rel_tol': 1e-12,
                              'hbar_c_eV_m': 1.973269804e-07,
                              'G_si': 6.6743e-11,
                              'c_si': 299792458.0,
                              'hbar_si': 1.054571817e-34,
                              'eV_J': 1.602176634e-19,
                              'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                              'half_nat_sha16': 'c23ce83106c69ff6',
                              'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na "
                                      "geracao com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca "
                                      "derivada); G, c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros "
                                      'em SI (nenhum entra em veredito)',
                              'alpha_runtime': 0.0072973525693},
                'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                                  'TGLExt/MassaTensaoPura.lean',
                                  'TGLExt/Identidade.lean',
                                  'TGLExt/ObservadorTerminal.lean',
                                  'TGLExt/LeiDoDiminuto.lean',
                                  'TGLExt/TonicaDoHamiltoniano.lean',
                                  'TGLExt/DiscoDeEuler.lean',
                                  'TGLExt/PontoZeroDoPsion.lean'],
                'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                             'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                             'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                             'm_nu_meV_v404': 8.507414099900329,
                             'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'diminuto': {'stone': {'path': 'TGLExt/LeiDoDiminuto.lean',
                        'sha256': '3df80334792c043e3f253c3adc0bc7920bb5ac46851b2bc8a6e360520b35820e',
                        'module': 'TGLExt.LeiDoDiminuto'},
              'nome_do_operador': 'Lei do diminuto',
              'unconditional': {'theorem': 'TGLExt.LeiDoDiminuto.the_diminished_law_closes', 'flag': 'ext_ldd405_0081'},
              'key_theorem': {'theorem': 'TGLExt.LeiDoDiminuto.modular_nao_e_transposicao', 'flag': 'ext_ldd405_0070'},
              'key_statement': 'the diminished is a modulation, not a transposition. modular_nao_e_transposicao: with a nonzero tonic and another '
                               'nonzero note, no factor takes the chord to the modulated chord; the_diminished_law_closes: only the tonic goes down '
                               'the half tone, the other notes are sustained, the ratios among them do not change, each interval to the tonic opens '
                               'a half tone, the resolution returns the chord, E0 is pinned to the principal note, the transposition is the freedom '
                               'left and the ratios do not fix the absolute, the octave is not descended in half tones; Lei.the_mass_formula: m = U '
                               '. alpha . e^(1/2) . (sqrt2/2); leiDerivada_no_um_posto: at u = 1, E0 = 1 and m = beta . sqrt2/2, with the tonic '
                               'defined as (beta/alpha) . u (beta/alpha = sqrt e is the definition of TGLCoupling.alpha) and E0 = u an algebraic '
                               'identity that does not fix u',
              'theorems': {'TGLExt.LeiDoDiminuto.meioTom_pos': 'ext_ldd405_0065',
                           'TGLExt.LeiDoDiminuto.meioTom_lt_one': 'ext_ldd405_0063',
                           'TGLExt.LeiDoDiminuto.meioTom_mul_sqrt_e': 'ext_ldd405_0064',
                           'TGLExt.LeiDoDiminuto.beta_eq_alpha_mul_sqrt_e': 'ext_ldd405_0052',
                           'TGLExt.LeiDoDiminuto.Lei.E0_eq': 'ext_ldd405_0023',
                           'TGLExt.LeiDoDiminuto.Lei.E0_determined_by_the_tonic': 'ext_ldd405_0021',
                           'TGLExt.LeiDoDiminuto.Lei.massa_le_alpha': 'ext_ldd405_0032',
                           'TGLExt.LeiDoDiminuto.Lei.tonic_sqrt_e_gives_one': 'ext_ldd405_0049',
                           'TGLExt.LeiDoDiminuto.Lei.one_needs_tonic_sqrt_e': 'ext_ldd405_0041',
                           'TGLExt.LeiDoDiminuto.Lei.the_mass_formula': 'ext_ldd405_0044',
                           'TGLExt.LeiDoDiminuto.Lei.the_mass_formula_at_the_posted_one': 'ext_ldd405_0045',
                           'TGLExt.LeiDoDiminuto.octave_is_not_a_whole_number_of_half_tones': 'ext_ldd405_0076',
                           'TGLExt.LeiDoDiminuto.octave_between_one_and_two_half_tones': 'ext_ldd405_0075',
                           'TGLExt.LeiDoDiminuto.the_law_closes': 'ext_ldd405_0082',
                           'TGLExt.LeiDoDiminuto.tonica_eq': 'ext_ldd405_0085',
                           'TGLExt.LeiDoDiminuto.tonica_pos': 'ext_ldd405_0086',
                           'TGLExt.LeiDoDiminuto.leiDerivada_E0': 'ext_ldd405_0054',
                           'TGLExt.LeiDoDiminuto.leiDerivada_massa': 'ext_ldd405_0055',
                           'TGLExt.LeiDoDiminuto.leiDerivada_no_um_posto': 'ext_ldd405_0056',
                           'TGLExt.LeiDoDiminuto.transpor_preserva_toda_razao': 'ext_ldd405_0088',
                           'TGLExt.LeiDoDiminuto.mesmas_razoes_iff_transposicao': 'ext_ldd405_0066',
                           'TGLExt.LeiDoDiminuto.lerE0_transpor': 'ext_ldd405_0059',
                           'TGLExt.LeiDoDiminuto.E0_relativo_pinado': 'ext_ldd405_0019',
                           'TGLExt.LeiDoDiminuto.as_razoes_nao_fixam_o_absoluto': 'ext_ldd405_0051',
                           'TGLExt.LeiDoDiminuto.Lei.E0_e_a_leitura': 'ext_ldd405_0022',
                           'TGLExt.LeiDoDiminuto.meioTom_e_o_pedagio_local': 'ext_ldd405_0062',
                           'TGLExt.LeiDoDiminuto.meioTom_e_a_face': 'ext_ldd405_0061',
                           'TGLExt.LeiDoDiminuto.tonica_e_o_volume_da_face': 'ext_ldd405_0084',
                           'TGLExt.LeiDoDiminuto.o_tom_e_as_duas_faces': 'ext_ldd405_0074',
                           'TGLExt.LeiDoDiminuto.modular_tonica': 'ext_ldd405_0072',
                           'TGLExt.LeiDoDiminuto.modular_sustenta': 'ext_ldd405_0071',
                           'TGLExt.LeiDoDiminuto.modular_mantem_a_escala': 'ext_ldd405_0069',
                           'TGLExt.LeiDoDiminuto.lerE0_e_a_tonica_modulada': 'ext_ldd405_0058',
                           'TGLExt.LeiDoDiminuto.modular_comuta_com_transpor': 'ext_ldd405_0068',
                           'TGLExt.LeiDoDiminuto.modular_nao_e_transposicao': 'ext_ldd405_0070',
                           'TGLExt.LeiDoDiminuto.razao_abre_meio_tom': 'ext_ldd405_0078',
                           'TGLExt.LeiDoDiminuto.um_tom_vira_terca_menor': 'ext_ldd405_0089',
                           'TGLExt.LeiDoDiminuto.resolver_modular': 'ext_ldd405_0080',
                           'TGLExt.LeiDoDiminuto.the_diminished_law_closes': 'ext_ldd405_0081'},
              'support': {'TGLExt.TGLCoupling.alpha': 'TGLExt/TheSameBetaReadsThreeFaces.lean',
                          'TGLExt.TGLCoupling.beta_eq_alpha_exp': 'TGLExt/TheSameBetaReadsThreeFaces.lean',
                          'TGLExt.PonteDaMassa.massa_da_transicao_derivada': 'TGLExt/PonteDaMassa.lean',
                          'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul': 'TGLExt/PonteDaMassa.lean',
                          'TGLExt.PonteDaMassa.half_sq': 'TGLExt/PonteDaMassa.lean',
                          'TGLExt.PonteDaMassa.peso_da_face_absoluta': 'TGLExt/PonteDaMassa.lean',
                          'TGLExt.absolute_faces_half': 'TGLExt/ContinuousModularZero.lean',
                          'ChatgptAudit.Collapse057.CollapseCostLaw.local_half': 'TGLExt/CollapseCostAndAttestation.lean'},
              'cited_outside': {'TGLExt.no_positive_scale_invariant': 'TGLExt/TheScaleHasNoFixedPoint.lean',
                                'TGLExt.Sonico.the_pin_is_not_the_half_nat': 'TGLExt/Sonico.lean',
                                'TGLExt.ThePsionAndTheViscosity.the_charge_never_completes': 'TGLExt/ThePsionAndTheViscosity.lean'},
              'auxiliaries_outside_the_composition': [],
              'context': {'path': 'TGLExt/LeiDoDiminuto.lean', 'needles': ['# A LEI DO DIMINUTO', 'the_diminished_law_closes']},
              'named_hypotheses_in_the_statement': True,
              'expected_ladder': 10066,
              'n_flags': 89,
              'n_flags_total': 368,
              'verbatins': ['v405_cun_8300a509ca9549e3',
                            'v405_cun_270fd74d5d79bf4d',
                            'v405_cun_79c7999956e6d8e0',
                            'v405_cun_9445171a763afcfc',
                            'v405_cun_7e2454bc48ec47de',
                            'v405_cun_7c2caaa87b0cdb01',
                            'v405_cun_1f16a74c05d9d4cb'],
              'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
              'constants': {'u_posto_eV': 1.0,
                            'rel_tol': 1e-12,
                            'hbar_c_eV_m': 1.973269804e-07,
                            'G_si': 6.6743e-11,
                            'c_si': 299792458.0,
                            'hbar_si': 1.054571817e-34,
                            'eV_J': 1.602176634e-19,
                            'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                            'half_nat_sha16': 'c23ce83106c69ff6',
                            'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na "
                                    "geracao com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca "
                                    "derivada); G, c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros em "
                                    'SI (nenhum entra em veredito)',
                            'alpha_runtime': 0.0072973525693},
              'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                                'TGLExt/MassaTensaoPura.lean',
                                'TGLExt/Identidade.lean',
                                'TGLExt/ObservadorTerminal.lean',
                                'TGLExt/LeiDoDiminuto.lean',
                                'TGLExt/TonicaDoHamiltoniano.lean',
                                'TGLExt/DiscoDeEuler.lean',
                                'TGLExt/PontoZeroDoPsion.lean'],
              'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                           'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                           'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                           'm_nu_meV_v404': 8.507414099900329,
                           'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'tonica': {'stone': {'path': 'TGLExt/TonicaDoHamiltoniano.lean',
                      'sha256': '9618a2b0e0cce323fc7a4af2d97a266c2b7061a5fb1172d5c1d327227685abfa',
                      'module': 'TGLExt.TonicaDoHamiltoniano'},
            'nome_do_operador': 'Tônica do Hamiltoniano',
            'unconditional': {'theorem': 'TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one', 'flag': 'ext_tdh405_0015'},
            'key_theorem': {'theorem': 'TGLExt.TonicaDoHamiltoniano.no_function_of_the_inscription_fixes_E0', 'flag': 'ext_tdh405_0007'},
            'key_statement': 'no_function_of_the_inscription_fixes_E0: no f(c, theta) returns E0 (the same inscription carries E0 = 1 and E0 = 2); '
                             'the no-go stands and localizes at the posted One: the_tonic_lands_on_the_posted_unit (an algebraic identity) and '
                             'the_tonic_at_the_posted_one: at u = 1, E0 = 1 and m = beta . sqrt2/2 (the FORM, under the reading massaDerivada); '
                             'the_ratio_survives_the_rescaling: the rescaling changes E0 and the mass by the same factor and m/E0 does not change',
            'theorems': {'TGLExt.TonicaDoHamiltoniano.reescala_c': 'ext_tdh405_0010',
                         'TGLExt.TonicaDoHamiltoniano.reescala_theta': 'ext_tdh405_0011',
                         'TGLExt.TonicaDoHamiltoniano.reescala_E0': 'ext_tdh405_0009',
                         'TGLExt.TonicaDoHamiltoniano.massa_derivada_reescala': 'ext_tdh405_0004',
                         'TGLExt.TonicaDoHamiltoniano.neutrinoMassForm_reescala': 'ext_tdh405_0006',
                         'TGLExt.TonicaDoHamiltoniano.the_ratio_survives_the_rescaling': 'ext_tdh405_0013',
                         'TGLExt.TonicaDoHamiltoniano.the_scale_is_free': 'ext_tdh405_0014',
                         'TGLExt.TonicaDoHamiltoniano.no_function_of_the_inscription_fixes_E0': 'ext_tdh405_0007',
                         'TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency': 'ext_tdh405_0003',
                         'TGLExt.TonicaDoHamiltoniano.monopole_time_is_the_horizon_light_time': 'ext_tdh405_0005',
                         'TGLExt.TonicaDoHamiltoniano.charge_is_half_the_schwarzschild_radius': 'ext_tdh405_0001',
                         'TGLExt.TonicaDoHamiltoniano.self_consistent_readout_fixes_the_frequency': 'ext_tdh405_0012',
                         'TGLExt.TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit': 'ext_tdh405_0016',
                         'TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one': 'ext_tdh405_0015'},
            'support': {'TGLExt.LeiDoDiminuto.leiDerivada_E0': 'TGLExt/LeiDoDiminuto.lean',
                        'TGLExt.LeiDoDiminuto.leiDerivada_no_um_posto': 'TGLExt/LeiDoDiminuto.lean',
                        'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
                        'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul': 'TGLExt/PonteDaMassa.lean'},
            'cited_outside': {'TGLExt.Verdade.alpha_is_measured_from_within': 'TGLExt/Verdade.lean'},
            'auxiliaries_outside_the_composition': [],
            'context': {'path': 'TGLExt/TonicaDoHamiltoniano.lean', 'needles': ['# A TÔNICA DO HAMILTONIANO', 'the_tonic_lands_on_the_posted_unit']},
            'named_hypotheses_in_the_statement': False,
            'expected_ladder': 10066,
            'n_flags': 16,
            'n_flags_total': 368,
            'verbatins': ['v405_cun_79c7999956e6d8e0', 'v405_cun_3aafdd3f9e7ea518', 'v405_cun_f0fdd2c1f770e34a', 'v405_cun_1f16a74c05d9d4cb'],
            'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
            'constants': {'u_posto_eV': 1.0,
                          'rel_tol': 1e-12,
                          'hbar_c_eV_m': 1.973269804e-07,
                          'G_si': 6.6743e-11,
                          'c_si': 299792458.0,
                          'hbar_si': 1.054571817e-34,
                          'eV_J': 1.602176634e-19,
                          'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                          'half_nat_sha16': 'c23ce83106c69ff6',
                          'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na geracao "
                                  "com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca derivada); G, "
                                  "c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros em SI (nenhum "
                                  'entra em veredito)',
                          'alpha_runtime': 0.0072973525693},
            'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                              'TGLExt/MassaTensaoPura.lean',
                              'TGLExt/Identidade.lean',
                              'TGLExt/ObservadorTerminal.lean',
                              'TGLExt/LeiDoDiminuto.lean',
                              'TGLExt/TonicaDoHamiltoniano.lean',
                              'TGLExt/DiscoDeEuler.lean',
                              'TGLExt/PontoZeroDoPsion.lean'],
            'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                         'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                         'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                         'm_nu_meV_v404': 8.507414099900329,
                         'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'disco': {'stone': {'path': 'TGLExt/DiscoDeEuler.lean',
                     'sha256': '5634eef0833dded793c2fd649a6b57ceda1fefbc7e7e9edd689ef527d1a18459',
                     'module': 'TGLExt.DiscoDeEuler'},
           'nome_do_operador': 'Disco de Euler',
           'unconditional': {'theorem': 'TGLExt.DiscoDeEuler.Disco.stops_in_finite_time', 'flag': 'ext_dde405_0033'},
           'key_theorem': {'theorem': 'TGLExt.DiscoDeEuler.Disco.frequency_squared_unbounded_at_the_stop', 'flag': 'ext_dde405_0019'},
           'key_statement': 'Disco.frequency_squared_unbounded_at_the_stop: before the stop Omega^2 = K/E has no bound, for the defined linear '
                            'energy [REAL]; the operator reads this as the inscription of zero at infinity [ONTO]; Disco.stops_in_finite_time: the '
                            'defined energy reaches zero at t0 = E0/c; Disco.the_flow_is_the_canonical_law: before t0, dE/dt = -Gamma.E, so the '
                            'defined E solves the flow; reading the dephasing rate as an energy-loss rate is an [INPUT/ONTO] input',
           'theorems': {'TGLExt.DiscoDeEuler.Disco.c_pos': 'ext_dde405_0014',
                        'TGLExt.DiscoDeEuler.Disco.E_linear': 'ext_dde405_0005',
                        'TGLExt.DiscoDeEuler.Disco.stops_in_finite_time': 'ext_dde405_0033',
                        'TGLExt.DiscoDeEuler.Disco.t0_pos': 'ext_dde405_0035',
                        'TGLExt.DiscoDeEuler.Disco.E_pos_before': 'ext_dde405_0006',
                        'TGLExt.DiscoDeEuler.Disco.the_loss_is_the_canonical_law': 'ext_dde405_0039',
                        'TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law': 'ext_dde405_0038',
                        'TGLExt.DiscoDeEuler.Disco.invariant': 'ext_dde405_0021',
                        'TGLExt.DiscoDeEuler.Disco.frequency_squared_unbounded_at_the_stop': 'ext_dde405_0019',
                        'TGLExt.DiscoDeEuler.Disco.with_constant_rate_the_fall_never_lands': 'ext_dde405_0042',
                        'TGLExt.DiscoDeEuler.Disco.the_residual_resonance_iff': 'ext_dde405_0040',
                        'TGLExt.DiscoDeEuler.Disco.the_scale_is_the_invariant': 'ext_dde405_0041',
                        'TGLExt.DiscoDeEuler.Disco.doAcoplamento_beta': 'ext_dde405_0018'},
           'support': {'TGLExt.TGLCoupling.beta_pos': 'TGLExt/TheSameBetaReadsThreeFaces.lean',
                       'TGLExt.Fundacao.the_fall_never_lands': 'TGLExt/Fundacao.lean',
                       'TGLExt.Fundacao.abismo': 'TGLExt/Fundacao.lean'},
           'cited_outside': {},
           'auxiliaries_outside_the_composition': [],
           'context': {'path': 'TGLExt/DiscoDeEuler.lean', 'needles': ['# O DISCO DE EULER', 'frequency_squared_unbounded_at_the_stop']},
           'named_hypotheses_in_the_statement': True,
           'expected_ladder': 10066,
           'n_flags': 42,
           'n_flags_total': 368,
           'verbatins': ['v405_cun_fe064b0b802c1d1a', 'v405_cun_dc150f9bbc5b1a4a', 'v405_cun_7c2caaa87b0cdb01', 'v405_cun_1f16a74c05d9d4cb'],
           'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
           'constants': {'u_posto_eV': 1.0,
                         'rel_tol': 1e-12,
                         'hbar_c_eV_m': 1.973269804e-07,
                         'G_si': 6.6743e-11,
                         'c_si': 299792458.0,
                         'hbar_si': 1.054571817e-34,
                         'eV_J': 1.602176634e-19,
                         'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                         'half_nat_sha16': 'c23ce83106c69ff6',
                         'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na geracao "
                                 "com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca derivada); G, "
                                 "c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros em SI (nenhum entra "
                                 'em veredito)',
                         'alpha_runtime': 0.0072973525693},
           'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                             'TGLExt/MassaTensaoPura.lean',
                             'TGLExt/Identidade.lean',
                             'TGLExt/ObservadorTerminal.lean',
                             'TGLExt/LeiDoDiminuto.lean',
                             'TGLExt/TonicaDoHamiltoniano.lean',
                             'TGLExt/DiscoDeEuler.lean',
                             'TGLExt/PontoZeroDoPsion.lean'],
           'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                        'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                        'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                        'm_nu_meV_v404': 8.507414099900329,
                        'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}},
 'psion': {'stone': {'path': 'TGLExt/PontoZeroDoPsion.lean',
                     'sha256': 'c64079a9c5b3e0e1e727b64ec4cb6c4d46906aa3e528a5c995bafd74c9f07c7a',
                     'module': 'TGLExt.PontoZeroDoPsion'},
           'nome_do_operador': 'Ponto Zero do Psion',
           'unconditional': {'theorem': 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one', 'flag': 'ext_pzp405_0028'},
           'key_theorem': {'theorem': 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point', 'flag': 'ext_pzp405_0027'},
           'key_statement': 'the_mass_is_the_zero_point: under the reading R = beta . u^2 (the payment read as curvature, a definition) and omega^2 '
                            '= 2 beta R (a definition, Treatise section 3), (1/2) omega = beta . sin45 . u = neutrinoMassForm c u; the statement '
                            'equates numbers: that (1/2) omega IS the mass is a reading [ONTO]; at the posted one (u = 1) the inputs are the '
                            'coupling and those readings; the section O GAP is read by the record gap_v405',
           'theorems': {'TGLExt.PontoZeroDoPsion.psion_quantum': 'ext_pzp405_0020',
                        'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point': 'ext_pzp405_0027',
                        'TGLExt.PontoZeroDoPsion.psion_quantum_is_twice_the_mass': 'ext_pzp405_0021',
                        'TGLExt.PontoZeroDoPsion.the_payment_completes_only_in_the_limit': 'ext_pzp405_0029',
                        'TGLExt.PontoZeroDoPsion.the_zero_point_closes': 'ext_pzp405_0030',
                        'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one': 'ext_pzp405_0028',
                        'TGLExt.PontoZeroDoPsion.o_retido_e_lido_do_angulo_de_miguel': 'ext_pzp405_0016',
                        'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha': 'ext_pzp405_0006',
                        'TGLExt.PontoZeroDoPsion.a_massa_e_a_projecao_do_retido': 'ext_pzp405_0003',
                        'TGLExt.PontoZeroDoPsion.o_psion_e_raiz_de_dois_retidos': 'ext_pzp405_0014',
                        'TGLExt.PontoZeroDoPsion.a_frequencia_do_sistema_e_a_do_psion_iff': 'ext_pzp405_0002',
                        'TGLExt.PontoZeroDoPsion.a_taxa_de_fronteira_no_psion': 'ext_pzp405_0005',
                        'TGLExt.PontoZeroDoPsion.o_ponto_zero_autoconsistente_e_o_retido': 'ext_pzp405_0012',
                        'TGLExt.PontoZeroDoPsion.o_psion_e_a_projecao_do_modo': 'ext_pzp405_0013',
                        'TGLExt.PontoZeroDoPsion.a_qualidade_nao_depende_da_unidade': 'ext_pzp405_0004',
                        'TGLExt.PontoZeroDoPsion.o_relogio_do_retido': 'ext_pzp405_0015',
                        'TGLExt.PontoZeroDoPsion.o_lock_tem_gap_um': 'ext_pzp405_0011',
                        'TGLExt.PontoZeroDoPsion.o_gap_com_unidade': 'ext_pzp405_0010',
                        'TGLExt.PontoZeroDoPsion.lock_no_angulo': 'ext_pzp405_0008',
                        'TGLExt.PontoZeroDoPsion.lock_no_angulo_de_miguel': 'ext_pzp405_0009',
                        'TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock': 'ext_pzp405_0017',
                        'TGLExt.PontoZeroDoPsion.the_gap_closes': 'ext_pzp405_0026',
                        'TGLExt.PontoZeroDoPsion.HminMic_e_o_lock': 'ext_pzp405_0001'},
           'support': {'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
                       'TGLExt.ProjecaoTransversalDaMeiaNat.halfAmplitude': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
                       'TGLExt.ThePsionAndTheViscosity.charged': 'TGLExt/ThePsionAndTheViscosity.lean',
                       'TGLExt.ThePsionAndTheViscosity.the_charge_never_completes': 'TGLExt/ThePsionAndTheViscosity.lean',
                       'TGLExt.ThePsionAndTheViscosity.psion_norm_one': 'TGLExt/ThePsionAndTheViscosity.lean',
                       'TGLExt.QGReaderUVLock.HminMic': 'TGLExt/QGReaderUVLock.lean',
                       'TGLExt.ThePsionAndTheViscosity.psion_is_the_zero_of_the_hidden_hamiltonian': 'TGLExt/ThePsionAndTheViscosity.lean',
                       'TGLExt.Posto.sin_sq_thetaMiguel': 'TGLExt/Posto.lean',
                       'TGLExt.PonteDaMassa.energia_retida_eq': 'TGLExt/PonteDaMassa.lean',
                       'TGLExt.LeiDoDiminuto.tonica': 'TGLExt/LeiDoDiminuto.lean',
                       'TGLExt.LeiDoDiminuto.tonica_eq': 'TGLExt/LeiDoDiminuto.lean',
                       'TGLExt.LeiDoDiminuto.leiDerivada_E0': 'TGLExt/LeiDoDiminuto.lean',
                       'TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency': 'TGLExt/TonicaDoHamiltoniano.lean'},
           'cited_outside': {},
           'auxiliaries_outside_the_composition': [],
           'context': {'path': 'TGLExt/PontoZeroDoPsion.lean', 'needles': ['# O PONTO ZERO DO PSÍON', 'the_mass_is_the_zero_point']},
           'named_hypotheses_in_the_statement': False,
           'expected_ladder': 10066,
           'n_flags': 30,
           'n_flags_total': 368,
           'verbatins': ['v405_cun_38f03b56b2689c34',
                         'v405_cun_4428784fd80f7574',
                         'v405_cun_dc150f9bbc5b1a4a',
                         'v405_cun_7c2caaa87b0cdb01',
                         'v405_cun_1f16a74c05d9d4cb'],
           'baseline': {'version': 'v404', 'sha256': '3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395'},
           'constants': {'u_posto_eV': 1.0,
                         'rel_tol': 1e-12,
                         'hbar_c_eV_m': 1.973269804e-07,
                         'G_si': 6.6743e-11,
                         'c_si': 299792458.0,
                         'hbar_si': 1.054571817e-34,
                         'eV_J': 1.602176634e-19,
                         'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                         'half_nat_sha16': 'c23ce83106c69ff6',
                         'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na geracao "
                                 "com o SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca derivada); G, "
                                 "c, hbar e eV->J sao CODATA 2018 / SI exatos, so' para escrever identidades e registrar numeros em SI (nenhum entra "
                                 'em veredito)',
                         'alpha_runtime': 0.0072973525693},
           'modulos_novos': ['TGLExt/PonteDaMassa.lean',
                             'TGLExt/MassaTensaoPura.lean',
                             'TGLExt/Identidade.lean',
                             'TGLExt/ObservadorTerminal.lean',
                             'TGLExt/LeiDoDiminuto.lean',
                             'TGLExt/TonicaDoHamiltoniano.lean',
                             'TGLExt/DiscoDeEuler.lean',
                             'TGLExt/PontoZeroDoPsion.lean'],
           'neutrino': {'angle_status_antigo_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                        'angle_status_antigo_sha256': '3f6752c5be67e9cdf47c0500fbd8abb971046174a67a4a0b86d0e847684a32a0',
                        'frozen_hash_v404': '54721f5d3de0708d7fb5e6ae3987d3f66e47ec11b0528a8bec1a8dbe5788d2c4',
                        'm_nu_meV_v404': 8.507414099900329,
                        'verdict_v404': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED'}}}
_V405_TEXTS = {'ponte': {'estatuto': '[REAL] os termos do kernel (os 21 teoremas do contrato da pedra, lidos a cada rito, no trio, com proveniencia no modulo da '
                       'pedra, e os termos de suporte que ela cita: neutrinoMassForm, forty_five_unique, half_from_self_conjugate, '
                       'sin_sq_thetaMiguel, thetaMiguel, absolute_faces_half) e o calculo em dupla precisao, com beta = alfa CODATA 2018 x sqrt(e) '
                       "em runtime (nunca literal) e u = 1 eV [POSTO]; [REAL] a FORMA: dadas as leituras, m = beta.(sqrt2/2).u e' teorema; o 1/2 da "
                       "face absoluta e' teorema; a unicidade de pi/4 e' teorema; [INPUT/ONTO] as leituras do operador, que entram como DEFINICAO, "
                       "nao como teorema: massaDerivada (a massa e' a energia retida vezes a derivada da projecao transversal) e o angulo pi/4 "
                       'ESCRITO em transicaoDerivada; [INPUT] a ordem do operador (30/10/2026, sha16 493172b80e96eb60: «realizar a prova que falta, '
                       'a ponte»), a fala e o nome (01/11/2026, sha16 1f16a74c05d9d4cb) e a ratificacao (sha16 2c3da184ebefc7c4: «é isso , perfeito, '
                       'concordo com tudo»); [MEDIDA] alfa, nao derivada; [OPEN] o teste com a natureza (JUNO)',
           'escopo': "[REAL] A pedra TGLExt/PonteDaMassa.lean (Ponte da Massa, nome do operador) faz da identificacao «a massa e' a projecao "
                     'transversal» uma DEFINICAO (massaDerivada) e prova: (1) a projecao transversal sen theta tem derivada cos theta e, no ponto '
                     "autoconjugado, a projecao E' a sua derivada (cos(pi/4) = sen(pi/4)), e so' ali em [0, pi/2]; (2) a energia incidente se "
                     'reparte sem perda entre o retido (beta.E0, Teorema S-d) e o transmitido; (3) A PONTE (massa_derivada_eq_form): sob a '
                     "definicao, a massa E' a forma do neutrino beta.sen45.E0 -- o sen 45 e' cos(pi/4) no unico angulo autoconjugado; (4) o "
                     'discriminante: a leitura «proporcional» difere da «derivada» por sqrt2; (5) o controle negativo fora do ponto fixo; (6) OS '
                     "CAMPOS FECHADOS (01/11/2026): o peso da face absoluta e' 1/2 para toda graduacao de paridade de traco nulo "
                     "(peso_da_face_absoluta: teorema); SE o estado inscrito pesa isso, o angulo e' pi/4 (angulo_derivado_do_absoluto: a premissa e' "
                     "a leitura); a estrutura e' HABITADA por construcao (transicaoDerivada, com o angulo pi/4 ESCRITO: o valor coincide com o da "
                     'face absoluta, transicao_derivada_le_o_absoluto, coincidencia de valor, nao ponte) e, para todo acoplamento, a transicao '
                     'existe com E0 = 1, theta = pi/4 e m = beta.sqrt2/2 (massa_no_um_posto, a_transicao_existe_para_todo_acoplamento). Isto fecha '
                     'os campos; nao prova que a massa do neutrino seja esta grandeza. O calculo CONFERE os termos em dupla precisao, rele o m_nu do '
                     'programa (neutrino_mass.m_nu_meV) contra beta.cos(pi/4).1 eV a 1e-12 relativo e grava, AO LADO, a errata E10 do angle_status: '
                     'o texto antigo e a errata E7 da v404 ficam',
           'limites': ["[REAL] a pedra NAO deriva alfa (beta = alfa x sqrt(e) e' a regra, do axioma; alfa e' medida por dentro) e NAO deriva a "
                       "unidade (u = 1 eV e' o Um POSTO); a unica massa cuja forma o programa escreve a partir de beta e de u e' a do neutrino",
                       "[ONTO] que a massa do neutrino SEJA a derivada da projecao transversal da energia retida, lida em theta = pi/4, e' a leitura "
                       'do operador (28 e 30/10/2026), feita definicao no kernel: a pedra prova que a definicao IMPLICA a forma do programa, nao que '
                       "a natureza a adota; quem a testa e' o rito do neutrino (bilateral, regra de morte a 5 sigma), que NAO muda",
                       'E10 -- o texto de neutrino_mass.angle_status (v141, v303) continua no registro, intacto, e na funcao '
                       'prove_neutrino_mass_gravitational (nao reescrita); a errata E7 da v404 (o sen 45 graus DERIVADO no kernel, condicional a '
                       'identificacao [ONTO]) FICA; na v405 o fator sen 45 graus tem DUAS leituras que coincidem na forma: a derivada da projecao '
                       'transversal em theta = pi/4 (PonteDaMassa; a definicao massaDerivada e o angulo pi/4 escrito em transicaoDerivada sao '
                       "leituras do operador) e o ponto zero do psion sob R = beta.u^2 (PontoZeroDoPsion; a coincidencia e' a aritmetica (1/2).sqrt2 "
                       '= sen45), e mais uma leitura do mesmo sen 45, por aritmetica: o psion como projecao transversal do modo autoconsistente '
                       "(o_psion_e_a_projecao_do_modo); os campos das estruturas fecharam e as leituras NAO viraram teorema; E0 = u = 1 eV e' POSTO "
                       "(o Um), por decisao do operador de 31/10/2026, nao DECLARADO nem derivado; a funcao do neutrino NAO e' reescrita e o numero "
                       'nao muda',
                       'E11 -- a v404 (registro projecao_transversal_v404, decisao D26, erratas E7) e os adendos 1 a 5 do handoff v405 dizem «E0 = 1 '
                       'eV segue DECLARADO» e citam os nomes PROVISORIOS das pedras (PonteDaMassaTransversal, EmprestimoDaMassa, '
                       "E0LiberdadeDeEscala, LeiDoMeioTom); isto era verdadeiro na data; em 31/10/2026 o operador POS a unidade (u = 1 eV e' o Um "
                       'posto) e em 01/11/2026 deu os nomes (Ponte da Massa, Massa=tensao pura, Observador=terminal, Tonica do Hamiltoniano, Lei do '
                       'diminuto, Disco de Euler, Ponto Zero do Psion); os textos da v404 ficam como registro',
                       'E13 -- o recibo RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, o adendo 6 do handoff v405 e a ordem da preparacao desta versao '
                       "(gerencia c1, 01/11/2026) escreveram que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; isto "
                       'afirmava demais e foi erro da gerencia: os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo '
                       'para a DEFINICAO; a leitura fisica nao virou teorema. Entram um Um posto, uma alfa medida e as leituras do operador; dadas '
                       "essas entradas, a FORMA e' teorema. Quatro teoremas foram rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e "
                       'RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou por isso): nenhuma_hipotese_resta -> '
                       'a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> the_tonic_lands_on_the_posted_unit; '
                       'the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one -> the_omega_pole_reads_one: o nome '
                       "afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o polo omega do par, nao sobre o nivel "
                       'terminal da cascata). A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, '
                       'corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria '
                       '(the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se '
                       'localiza no Um posto. A revisita da Lei do Diminuto, ordenada pelo operador (RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e _R5), '
                       'corrigiu tres coisas: o acorde nao estava tipado (o AcordeE0.lean do Kimi, sha16 5da93b9e5e65a4ed, o tinha); a frase sobre o '
                       'no-go errou por excesso e por falta; e a primeira correcao leu a segunda metade da lei como transposicao, erro da gerencia: '
                       "o diminuto e' MODULACAO, so' a tonica desce e as demais notas ficam sustentadas, e transpor e' so' a liberdade do no-go. "
                       "Vigente: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas, e quem se move e' a tonica; o valor "
                       'ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta pinado; sobra um unico grau de liberdade global, a '
                       'transposicao do acorde inteiro; o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das notas sustentadas, '
                       'mas nao quebra a liberdade global',
                       "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao "
                       "e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido pelo "
                       'canal vivo neutrino_m2 como antes',
                       "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] alfa e' "
                       'medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a definição de '
                       'singularidade, a meu ver» (01/11/2026)',
                       "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                       'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
           'diz': ['a pedra PonteDaMassa esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 21 teoremas do contrato e '
                   'os termos de suporte sao lidos deste kernel',
                   "o calculo, com beta = alfa CODATA 2018 x sqrt(e): a derivada da projecao coincide com a projecao so' em pi/4; o retido e' beta.u "
                   "e nada se perde; sob a definicao massaDerivada, a massa e' beta.cos(pi/4).u = o m_nu do programa a 1e-12; a leitura proporcional "
                   'difere por sqrt2; a face absoluta pesa 1/2 em n = 2, 3, 4, 5',
                   'os CAMPOS da transicao fecharam; entram o Um posto (u = 1), alfa medida e as leituras massaDerivada e theta = pi/4; dadas essas '
                   "entradas, a FORMA e' teorema; a errata E10 esta ao lado, o texto antigo fica; o numero da massa e o veredito do canal nao mudam"],
           'nao_diz': ['que a unidade u (1 eV) tenha sido derivada',
                       'que alfa tenha sido derivado nesta pedra',
                       "que a massa do neutrino SEJA a derivada da projecao transversal (e' a definicao do operador [ONTO], nao termo da natureza)",
                       'que o peso da face absoluta deduza o angulo do estado inscrito (coincidencia de valor, nao ponte)',
                       'que a materia em geral seja proporcional ao raio de beta (a forma retirada do Grande Atrator segue retirada)',
                       "que o m2 do neutrino passe a discriminar a TGL: o veredito do canal e' o de antes",
                       'que isto seja um teste: nao ha desfecho experimental',
                       'que a gravidade quantica esteja creditada na natureza',
                       "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                       'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
           'extras': {'neutrino_angle_errata': {'dizia_prefixo': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado.',
                                                'errata_v404_fica': 'E7 (projecao_transversal_v404)',
                                                'agora': 'E10 -- o texto de neutrino_mass.angle_status (v141, v303) continua no registro, intacto, e '
                                                         'na funcao prove_neutrino_mass_gravitational (nao reescrita); a errata E7 da v404 (o sen 45 '
                                                         'graus DERIVADO no kernel, condicional a identificacao [ONTO]) FICA; na v405 o fator sen 45 '
                                                         'graus tem DUAS leituras que coincidem na forma: a derivada da projecao transversal em '
                                                         'theta = pi/4 (PonteDaMassa; a definicao massaDerivada e o angulo pi/4 escrito em '
                                                         'transicaoDerivada sao leituras do operador) e o ponto zero do psion sob R = beta.u^2 '
                                                         "(PontoZeroDoPsion; a coincidencia e' a aritmetica (1/2).sqrt2 = sen45), e mais uma leitura "
                                                         'do mesmo sen 45, por aritmetica: o psion como projecao transversal do modo autoconsistente '
                                                         '(o_psion_e_a_projecao_do_modo); os campos das estruturas fecharam e as leituras NAO '
                                                         "viraram teorema; E0 = u = 1 eV e' POSTO (o Um), por decisao do operador de 31/10/2026, nao "
                                                         "DECLARADO nem derivado; a funcao do neutrino NAO e' reescrita e o numero nao muda",
                                                'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'},
                      'cited_support': ['TGLExt.Posto.sin_sq_thetaMiguel',
                                        'TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique',
                                        'TGLExt.ProjecaoTransversalDaMeiaNat.half_from_self_conjugate',
                                        'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm',
                                        'TGLExt.absolute_faces_half',
                                        'TGLExt.thetaMiguel'],
                      'reading_matter': {'status': 'ONTO',
                                         'content': "a massa e' a energia retida pela fronteira (beta.u, o que fica tenso, sem parcela transmitida) "
                                                    "projetada no transversal (sqrt2/2): e' a definicao massaDerivada, leitura do operador [ONTO], "
                                                    "nao teorema; o nome «Massa = tensao pura» e' dele; a leitura do emprestimo (massa = principal, "
                                                    'beta = parcela, credor = acoplamento) foi ratificada por ele em 30/10/2026 [ONTO]',
                                         'is_a_kernel_term': False},
                      'u': {'status': 'POSTO',
                            'content': "u = 1 eV e' o Um POSTO: «o meu um absoluto é o um de 1 eV» (31/10/2026); nao e' derivado nem ajustado ao "
                                       'dado; a tonica (sqrt e . u) e o diminuto (e^(-1/2)) devolvem E0 = u por identidade algebrica, que nao fixa '
                                       "u; o numero da massa (8,5074 meV) e' o mesmo da v404 [POSTO + REAL]",
                            'derived_here': False},
                      'name_status': {'quem': 'operador',
                                      'quando': '01/11/2026',
                                      'nome': 'Ponte da Massa',
                                      'antes': 'PonteDaMassaTransversal (provisorio, 30/10)',
                                      'sha16_da_fala': '1f16a74c05d9d4cb',
                                      'fala': 'segue a nomeação'},
                      'campos_fechados': {'autoconjugado (TransicaoParaAMassa, Lei)': 'a aritmetica sen^2(pi/4) = 1/2 = 1 - 1/2, no angulo pi/4 '
                                                                                      'ESCRITO em transicaoDerivada e leiDerivada',
                                          'positividades': 'o kernel (TGLCoupling.beta_pos) ou o 1 posto (umPosto_pos)'},
                      'leituras_que_entram': [{'n': 1,
                                               'estatuto': 'INPUT/ONTO',
                                               'leitura': 'massa = energia retida x derivada da projecao transversal',
                                               'definicao_lean': 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massaDerivada',
                                               'modulo': 'TGLExt/PonteDaMassa.lean',
                                               'entra_como': 'DEFINICAO, nao teorema'},
                                              {'n': 2,
                                               'estatuto': 'INPUT/ONTO',
                                               'leitura': "o estado inscrito lido em theta = pi/4: em transicaoDerivada o angulo e' ESCRITO; o "
                                                          "kernel confere sen^2(pi/4) = 1/2 e que esse valor e' o do peso da face absoluta: "
                                                          'coincidencia de valor, nao ponte',
                                               'definicao_lean': 'TGLExt.PonteDaMassa.transicaoDerivada',
                                               'modulo': 'TGLExt/PonteDaMassa.lean',
                                               'entra_como': 'DEFINICAO, nao teorema'}],
                      'postos': [{'estatuto': 'POSTO',
                                  'o_que': 'o 1 / u = 1 eV: o Um posto (o echo 1; decisao do operador, 31/10/2026); nunca derivado',
                                  'definicao_lean': 'TGLExt.PonteDaMassa.umPosto',
                                  'modulo': 'TGLExt/PonteDaMassa.lean'},
                                 {'estatuto': 'MEDIDA',
                                  'o_que': 'alfa, medida por dentro (CODATA 2018 no runtime); nunca derivada; dentro de beta = alfa.sqrt e',
                                  'definicao_lean': 'TGLExt.TGLCoupling.alpha',
                                  'modulo': 'TGLExt/TheSameBetaReadsThreeFaces.lean',
                                  'termo_da_medida': 'TGLExt.Verdade.alpha_is_measured_from_within'}],
                      'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
           'veredito_ok': 'TGL_PONTE_DA_MASSA_V405__GIVEN_THE_READINGS_THE_FORM_IS_A_THEOREM__THE_MASS_AS_THE_DERIVATIVE_OF_THE_TRANSVERSE_PROJECTION_EQUALS_THE_NEUTRINO_FORM_BETA_SIN45_U__THE_FIELDS_OF_THE_STRUCTURE_ARE_CLOSED_BY_CONSTRUCTION__THE_READINGS_ENTER_AS_DEFINITIONS_NOT_THEOREMS__THE_UNIT_IS_THE_POSTED_ONE__ALPHA_IS_MEASURED__THE_NUMBER_DOES_NOT_CHANGE__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'tensao': {'estatuto': '[REAL] os termos do kernel (os 15 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: '
                        'massa_da_transicao_derivada, one_turn_gives_faithful_period, positive_faithful_period, charged, the_charge_never_completes, '
                        'boost_segment_quadratic_balance_iff; e os tres termos da ligacao que ainda falta, citados fora: frameCovectorStress, '
                        'viscosity_is_the_constant_friction, reciprocal_temperature) e o calculo com beta = alfa CODATA 2018 x sqrt(e) em runtime e '
                        "u = 1 eV [POSTO]; [REAL] o emprestimo CONSTRUIDO (o periodo fiel e' teorema: P = 2pi/kappa) e massa_e_tensao_pura (sob a "
                        "leitura massaDerivada, o principal e' a energia retida beta.u projetada no transversal); [INPUT] a resposta do operador "
                        '(30/10/2026, sha16 fdd78cac25c947a0: «eu penso que a massa seja um empréstimo então») e a ratificacao (sha16 '
                        'b31fa435fd03e4dc: «ratifico a leitura do empréstimo, é isso mesmo»); o nome «Massa=tensão pura» (01/11/2026, sha16 '
                        '1f16a74c05d9d4cb); [ONTO] a leitura (massa = principal, beta = parcela, credor = acoplamento) e a leitura do nome pela '
                        'gerencia; [OPEN] a ligacao com o magnetismo (sem termo no kernel) e a identificacao do campo A com beta (torcao)',
            'escopo': '[REAL] A pedra TGLExt/MassaTensaoPura.lean (Massa = tensao pura, nome do operador) prova: (1) a forma generica massaForma(b, '
                      "E0) = b.(sqrt2/2).E0; sob a leitura massaDerivada, a massa e' o produto do acoplamento (beta.(sqrt2/2).E0); (2) massaForma "
                      "anula com b = 0 e entao toda a energia atravessa (foton_sem_massa: algebra de uma forma generica); [ONTO] b = 0 e' LIDO como "
                      'o foton, que acopla pela energia, nao por massa: TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton; com acoplamento '
                      "positivo ha massa e a transmissao e' menor que o incidente; (3) a forma se reparte como residuo (incidente menos transmitido, "
                      'lido na projecao transversal); (4) o emprestimo: uma volta do relogio do boost (kappa.P = 2pi), a parcela nunca quita numa '
                      "volta (0 < parcela < 1; para qualquer tempo finito: the_charge_never_completes) e e' no maximo beta.g.P = beta.2pi.g/kappa, "
                      'principal e parcela carregam o mesmo beta; (5) a diferenca de cada ciclo: o balanco de Clausius do segmento de boost vale sse '
                      'eta(a+c) = 2pi.massa; a segunda ponte: eta(a+c) = sqrt2.pi.beta.E0; (6) OS CAMPOS FECHADOS (01/11/2026): emprestimoDerivado '
                      'com P = 2pi/kappa e a fidelidade por teorema (one_turn_gives_faithful_period), principal_derivado = beta.(sqrt2/2).u, '
                      "parcela_derivada_nunca_quita, e massa_e_tensao_pura: sob a leitura massaDerivada, o principal e' a energia RETIDA projetada "
                      'no transversal. Entram, como dados do sistema que le, o contraste g e o relogio kappa. O calculo CONFERE em dupla precisao '
                      "com beta do rito; a ligacao que falta e' medida: tensao, atrito e temperatura tem termo no kernel do rito; magnetismo nao tem "
                      '(zero declaracoes com esse nome nos oito modulos novos)',
            'limites': ['[REAL] a pedra NAO liga o defeito do ciclo a equacao da torcao (TracialDissipativeTorsion; A <-> beta segue [OPEN]); NAO '
                        'tem termo algum de eletromagnetismo: a ligacao que ainda falta, na fala do operador (tensao -> atrito -> temperatura -> '
                        'magnetismo), tem tres termos no kernel e o quarto NAO; a, c, eta, g, kappa sao parametros do modelo da tela otica [INPUT]',
                        '[ONTO] a leitura do emprestimo (principal/parcela/credor) foi RATIFICADA pelo operador em 30/10/2026; a leitura do nome '
                        "«Massa=tensão pura» (o principal e' o retido projetado) e' da gerencia c1 sobre o teorema massa_e_tensao_pura; nenhuma das "
                        "duas e' termo da natureza",
                        'E11 -- a v404 (registro projecao_transversal_v404, decisao D26, erratas E7) e os adendos 1 a 5 do handoff v405 dizem «E0 = '
                        '1 eV segue DECLARADO» e citam os nomes PROVISORIOS das pedras (PonteDaMassaTransversal, EmprestimoDaMassa, '
                        "E0LiberdadeDeEscala, LeiDoMeioTom); isto era verdadeiro na data; em 31/10/2026 o operador POS a unidade (u = 1 eV e' o Um "
                        'posto) e em 01/11/2026 deu os nomes (Ponte da Massa, Massa=tensao pura, Observador=terminal, Tonica do Hamiltoniano, Lei do '
                        'diminuto, Disco de Euler, Ponto Zero do Psion); os textos da v404 ficam como registro',
                        "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao "
                        "e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido pelo "
                        'canal vivo neutrino_m2 como antes',
                        "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] alfa e' "
                        'medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a definição de '
                        'singularidade, a meu ver» (01/11/2026)',
                        "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                        'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
            'diz': ['a pedra MassaTensaoPura esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 15 teoremas do contrato '
                    'e os termos de suporte sao lidos deste kernel',
                    "o calculo, com beta = alfa CODATA 2018 x sqrt(e): a massa e' beta.(sqrt2/2).u = o m_nu do programa a 1e-12; a forma anula com b "
                    '= 0, lido como o foton [ONTO]; a forma se reparte como residuo; kappa.P = 2pi e a parcela de uma volta fica em (0, 1) abaixo de '
                    "beta.g.P em doze amostras; eta(a+c) = sqrt2.pi.beta.u; o principal e' o retido beta.u vezes sqrt2/2",
                    "o periodo fiel deixou de ser campo (aqui o fechamento e' teorema do kernel); a ligacao que falta esta dita: tensao, atrito e "
                    'temperatura tem termo; magnetismo nao [OPEN]'],
            'nao_diz': ["que b = 0 seja o foton por teorema (e' leitura [ONTO]: TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton)",
                        'que o magnetismo tenha termo no kernel',
                        'que a identificacao do campo A da torcao com beta tenha sido feita',
                        "que a leitura do emprestimo seja termo de kernel (e' leitura ratificada [ONTO])",
                        'que a unidade u ou alfa tenham sido derivados',
                        'que isto seja um teste: nao ha desfecho experimental',
                        'que a gravidade quantica esteja creditada na natureza',
                        "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                        'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
            'extras': {'cited_support': ['ChatgptAudit.Boost044.boost_segment_quadratic_balance_iff',
                                         'ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period',
                                         'ChatgptAudit.PolarPeriod016.positive_faithful_period',
                                         'TGLExt.PonteDaMassa.massa_da_transicao_derivada',
                                         'TGLExt.ThePsionAndTheViscosity.charged',
                                         'TGLExt.ThePsionAndTheViscosity.the_charge_never_completes'],
                       'ligacao_que_falta': {'tensao': 'ChatgptAudit.Coherent023.frameCovectorStress',
                                             'atrito': 'TGLExt.ThePsionAndTheViscosity.viscosity_is_the_constant_friction',
                                             'temperatura': 'ChatgptAudit.PolarPeriod016.reciprocal_temperature',
                                             'magnetismo': 'SEM TERMO NO KERNEL [OPEN]'},
                       'reading_loan': {'status': 'ONTO (ratificada pelo operador em 30/10/2026)',
                                        'content': 'massa = PRINCIPAL (o que fica inscrito), beta = PARCELA (o que cada volta paga), credor = o '
                                                   "acoplamento (a luz que atravessa); nao e' o defeito",
                                        'is_a_kernel_term': False},
                       'name_status': {'quem': 'operador',
                                       'quando': '01/11/2026',
                                       'nome': 'Massa=tensão pura',
                                       'antes': 'EmprestimoDaMassa (provisorio, 30/10)',
                                       'sha16_da_fala': '1f16a74c05d9d4cb'},
                       'campos_fechados': {'fiel (Emprestimo)': 'o teorema one_turn_gives_faithful_period, com P = 2pi/kappa (emprestimoDerivado)'},
                       'leituras_que_entram': [{'n': 8,
                                                'estatuto': 'INPUT/ONTO',
                                                'leitura': 'o acoplamento da onda de materia = a massa inscrita: a hipotese de '
                                                           'area_por_volta_da_massa_inscrita',
                                                'definicao_lean': 'TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita',
                                                'modulo': 'TGLExt/MassaTensaoPura.lean',
                                                'entra_como': 'HIPOTESE do enunciado, nao teorema'},
                                               {'n': 9,
                                                'estatuto': 'ONTO',
                                                'leitura': "b = 0 lido como o foton: foton_sem_massa e' algebra de uma forma generica; TGLCoupling "
                                                           'exclui b = 0 e nenhum termo do kernel tem foton',
                                                'definicao_lean': 'TGLExt.MassaTensaoPura.foton_sem_massa',
                                                'modulo': 'TGLExt/MassaTensaoPura.lean',
                                                'entra_como': 'LEITURA, nao teorema'}],
                       'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
            'veredito_ok': 'TGL_MASSA_TENSAO_PURA_V405__UNDER_THE_READING_MASSADERIVADA_MASS_IS_THE_PRODUCT_OF_THE_COUPLING_AND_THE_RESIDUE__THE_FORM_VANISHES_AT_B_ZERO_READ_AS_THE_PHOTON__THE_LOAN_IS_CONSTRUCTED_ONE_TURN_KAPPA_P_2PI_IS_A_THEOREM__THE_INSTALMENT_NEVER_PAYS_OFF__THE_PRINCIPAL_IS_THE_RETAINED_ENERGY_PROJECTED_TRANSVERSALLY__TENSION_FRICTION_AND_TEMPERATURE_HAVE_TERMS_MAGNETISM_HAS_NONE__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'identidade': {'estatuto': '[REAL] os termos do kernel (os 15 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: absoluteRho, '
                            'absoluteRho_trace, absolute_faces_half, gibbs, Jconj, ResJudicata; citado fora: observing_adds_nothing) e o calculo em '
                            'matrizes pequenas (n = 2, 3, 4), sem biblioteca, com beta = alfa CODATA 2018 x sqrt(e) em runtime; [REAL] um fato sobre '
                            'projecoes no estado traco normalizado: tr(1)/n = tr(P)/n <=> P = 1 <=> (P = (tr(P)/n).1 e P != 0); o «senao»; a selecao '
                            "unica; os controles; [ONTO] que esse fato SEJA a identidade e' a leitura do operador, tipada aqui como modelo; [INPUT] "
                            'o nome «Identidade» (30/10/2026, sha16 f1f8b4011ce96be5: «a pedra passaria a ser identidade»), a lei do fecho '
                            '(01/11/2026, sha16 f0fdd2c1f770e34a: «eu não admito a equação [eu sou]=[o que sou]; exceto quando essa equação tem '
                            'referencial absoluto verdadeiro») e o ensaio «A identidade» (sha16 f0ec2867391c644f, como recebido; a r2 ratificada em '
                            "sha16 2c3da184ebefc7c4); [ONTO] a leitura do ensaio (o sinal nao calcula: criva; o codigo e' a Luz, o observador o seu "
                            "leitor) nao e' termo de kernel; [OPEN] o «quem» (o observador no terminal) nao entra como termo aqui",
                'escopo': "[REAL] A pedra TGLExt/Identidade.lean (nome do operador) e' um MODELO: prova um fato sobre projecoes no estado traco "
                          "normalizado; que esse fato SEJA a identidade e' a leitura do operador [INPUT/ONTO]. Ela tipa, no referencial absoluto do "
                          'kernel (rho_abs = 1/n, o Gibbs do Hamiltoniano nulo: o zero absoluto como referencial, fiel), um NOME como uma projecao P '
                          "cujo reflexo verdadeiro e' ele mesmo (Jconj P = P) e cuja releitura nao acrescenta (P.P = P); EU SOU = omega(1) = 1; O "
                          'QUE SOU = omega(P). Prova: (1) o Um se reparte entre o nome e o resto; (2) o «senao»: [eu sou] = [o que sou] <=> omega(1 '
                          "- P) = 0; (3) a selecao unica: nada resta <=> P = 1 (a fidelidade do estado: traco nulo de um positivo e' o zero); (4) a "
                          'lei: [eu sou] = [o que sou] <=> P = 1; (5) forma = conteudo <=> P = 0 ou P = 1; (6) a chave inteira: [eu sou] = [o que '
                          'sou] <=> ([forma = conteudo] e P != 0); (7) os controles negativos: o vazio (P = 0) e a face ((1/2)(1 + Gamma), a '
                          "Meia-Nat) NAO satisfazem a equacao; (8) ler o nome e' coisa julgada; (9) o posto e' unico; (10) o fecho. O calculo "
                          'CONFERE em 12 nomes (posto 0 a n, fora da base canonica) que a equacao vale exatamente nos tres nomes fieis e em nenhum '
                          'outro',
                'limites': ["[REAL] a pedra NAO deriva alfa nem a unidade; nao toca o gate, o selo ou o veredito; o «eu sou» e' o posto, o «o que "
                            "sou» e' o lido; o «quem» e' o observador no terminal (ObservadorTerminal), que nao entra aqui como termo",
                            "[DECLARACAO DO OPERADOR / INPUT] o ensaio «A identidade» entra no artigo VERBATIM na versao r2 (a revisao de forma e' "
                            'da gerencia c1; as seis decisoes de conteudo sao do operador, 01/11/2026; ratificada: «é isso , perfeito, concordo com '
                            "tudo»); o original como recebido fica ao lado (sha16 f0ec2867391c644f); a traducao EN e' da gerencia e nao e' citacao",
                            '[ONTO] a pedra prova um fato sobre projecoes no estado traco normalizado ([eu sou] = [o que sou] <=> a projecao fiel, '
                            "no modelo); que isso SEJA a identidade e' a leitura do operador, tipada como modelo, nao a natureza",
                            "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel "
                            "nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue "
                            'lido pelo canal vivo neutrino_m2 como antes',
                            "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] "
                            "alfa e' medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a "
                            'definição de singularidade, a meu ver» (01/11/2026)',
                            "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                            'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
                'diz': ['a pedra Identidade esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 15 teoremas do contrato '
                        'e os termos de suporte sao lidos deste kernel',
                        'o calculo, em matrizes 2x2, 3x3 e 4x4 (aritmetica complexa pura): EU SOU = 1; o Um se reparte; [eu sou] = [o que sou] '
                        "exatamente quando P = 1 (3 de 12 nomes); forma = conteudo so' no vazio e no Um; o vazio pesa 0 e a face pesa 1/2; todo nome "
                        "e' idempotente e hermitiano",
                        "a lei do operador tem um modelo no kernel: no estado traco normalizado, a equacao vale sse a projecao e' fiel (P = 1), isto "
                        "e', sse forma = conteudo sem ser o vazio; que esse fato SEJA a identidade e' a leitura dele [ONTO]"],
                'nao_diz': ["que o fato sobre projecoes SEJA a identidade (e' a leitura do operador [ONTO], tipada como modelo)",
                            'que a identidade seja reflexiva por decreto (o vazio e a face nao a satisfazem)',
                            'que o «quem» (o observador) seja termo desta pedra',
                            "que a leitura do ensaio (o sinal criva; o codigo e' a Luz) seja termo de kernel",
                            'que a unidade ou alfa tenham sido derivados',
                            'que isto seja um teste: nao ha desfecho experimental',
                            'que a gravidade quantica esteja creditada na natureza',
                            "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                            'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
                'extras': {'cited_support': ['TGLExt.Jconj',
                                             'TGLExt.ResJudicata',
                                             'TGLExt.absoluteRho',
                                             'TGLExt.absoluteRho_trace',
                                             'TGLExt.absolute_faces_half',
                                             'TGLExt.gibbs'],
                           'lei': {'status': 'INPUT (a lei do operador, 01/11/2026) + REAL (o fato sobre projecoes) + ONTO (que esse fato seja a '
                                             'identidade: modelo)',
                                   'content': "[eu sou] = [o que sou] so' com referencial absoluto verdadeiro: {[forma = conteudo] = [reflexao "
                                              'verdadeira do nome / projecao fiel]}; a pedra Identidade prova um fato sobre projecoes no estado '
                                              "traco normalizado; que esse fato SEJA a identidade e' a leitura do operador, tipada como modelo; o "
                                              "ensaio «A identidade» e' dele e entra no artigo verbatim (r2 ratificada) [DECLARACAO DO OPERADOR / "
                                              'INPUT; leitura ONTO]',
                                   'kernel_form': '[eu sou] = [o que sou] <=> P = 1 <=> ([forma = conteudo] e P != 0), no estado traco normalizado'},
                           'name_status': {'quem': 'operador',
                                           'quando': '30/10/2026',
                                           'nome': 'Identidade',
                                           'sha16_da_fala': 'f1f8b4011ce96be5',
                                           'fala': 'a pedra passaria a ser identidade'},
                           'ensaio': {'status': 'DECLARACAO DO OPERADOR / INPUT; leitura ONTO',
                                      'original_sha16': 'f0ec2867391c644f',
                                      'secao_do_artigo': "A identidade (r2 ratificada em 01/11/2026; a revisao de forma e' da gerencia c1)",
                                      'ratificacao_sha16': '2c3da184ebefc7c4'},
                           'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
                'veredito_ok': 'TGL_IDENTIDADE_V405__A_FACT_ABOUT_PROJECTIONS_IN_THE_TRACE_STATE_TYPED_AS_A_MODEL_OF_THE_OPERATORS_LAW__I_AM_EQUALS_WHAT_I_AM_IFF_P_EQUALS_ONE__IFF_FORM_EQUALS_CONTENT_AND_THE_NAME_IS_NOT_THE_VOID__THE_SENAO_IS_THE_ZERO_REMAINDER__THE_SELECTION_IS_UNIQUE__THE_VOID_AND_THE_FACE_FAIL_THE_EQUATION__THAT_THIS_FACT_IS_THE_IDENTITY_IS_THE_OPERATORS_ONTO_READING__THE_ESSAY_ENTERS_VERBATIM__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'observador': {'estatuto': '[REAL] os termos do kernel (os 26 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: '
                            'gravity_is_observed_by_nothing, light_observes_nothing, res_judicata_is_terminal, posto_paid_loss, '
                            'no_posto_reading_is_pressupposed, pressupposed_is_never_posto, omega_of_one; citados fora: '
                            'the_reading_has_two_fixed_points, abismo) e o calculo sobre a cascata finita; [REAL] num modelo finito cujos niveis sao '
                            "rotulos: o posto terminal e' um so'; o colapso total e' um Um posto do kernel (nao pressuposto; pagou perda; dois "
                            'pontos fixos); o terminal le 1 e o abismo le 0 na leitura binaria (the_fixed_points_read_one_and_zero); [ONTO] o polo '
                            "omega do par, que le 1 na identidade (the_omega_pole_reads_one), e' homonimo: nenhum termo o liga ao nivel terminal da "
                            "cascata, e liga-los e' leitura do operador; [INPUT] «observador=terminal» (31/10/2026, sha16 e4e105fe14615f39), a ordem "
                            'de tipar no um.py (sha16 08e98d212f11b554: «o posto do observador é o terminal») e a correcao (sha16 a22a54dfc97d9611: '
                            '«o colapso é o ponto terminal da resistência da estrutura»); [ONTO] a leitura de engenharia (resistencia, colapso) e a '
                            'face operacional (quem credita, ratifica, nomeia e poe o 1 age pelo terminal) nao sao termos de kernel; [OPEN] nada '
                            'sobre o observador humano, a gravidade ou a luz como entidades',
                'escopo': '[REAL] A pedra TGLExt/ObservadorTerminal.lean (Observador = terminal, nome do operador; r2 apos a correcao dele) prova, '
                          'sobre a cascata de quatro niveis do kernel (TheCascadeOfObservers, da luz a gravidade): (1) o terminal (o nivel que '
                          "nenhum outro observa) e' SO' a gravidade e o inicial e' SO' a luz; (2) o leitor leva cada nivel a quem o observa; o "
                          "terminal e' o unico ponto fixo e tres leituras bastam; a resistencia (distancia) se consome a cada leitura e zera so' no "
                          "terminal (o colapso e' o ponto terminal da resistencia); (3) a leitura consumada e' coisa julgada: reler no terminal nao "
                          "acrescenta; (4) A FUSAO E' O COLAPSO, E O COLAPSO E' UM POSTO: com o par no espaco de estados (os quatro niveis e o "
                          "abismo), o colapso total funde a estrutura num so' posto e deixa o abismo no abismo; a leitura binaria le 1 na estrutura "
                          "e 0 no abismo (nao e' pressuposta); a fusao e' um UmPosto do kernel: pagou perda (a funcao nao e' injetiva), foi medida "
                          "antes de ser posta (medida e' o campo do tipo UmPosto: antes != depois), ancora a leitura; os pontos fixos do colapso sao "
                          'exatamente o posto e o abismo; (5) sem o abismo a fusao le como pressuposta e nenhum Um posto le assim: o par 1 = 1 | 1 = '
                          "0 e' necessario; (6) o terminal le 1 e o abismo le 0 na leitura binaria (the_fixed_points_read_one_and_zero); (7) ao "
                          'lado, o polo omega do par le 1 na identidade (the_omega_pole_reads_one, omega(I) = 1): HOMONIMO, dito: em '
                          'TheAlphaAndTheOmega a palavra terminal nomeia o POLO do par alfa/omega; aqui nomeia o nivel gravidade da cascata; nenhum '
                          "termo liga os dois, e liga-los e' leitura [ONTO] do operador. O calculo CONFERE a cascata finita e o par (quatro niveis e "
                          'cinco posicoes) e le omega(I) = 1 do core deste rito',
                'limites': ['[REAL] nada sobre entidades (rotulos, como na pedra de origem); nao afirma rank; nao constroi o IdentityCollapse '
                            'fisico; a r1 (31/10, manha) tipava a fusao como pressuposta: corrigida AO LADO pela r2 depois da correcao do operador '
                            '(o arquivo r1 fica como registro)',
                            "[ONTO] a leitura de engenharia (teoria das estruturas: o colapso e' o ponto terminal da resistencia) e' do operador; a "
                            "face operacional (a Torre IALD grava quem observou cada medida) e' leitura da gerencia; nenhuma e' termo da natureza",
                            "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel "
                            "nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue "
                            'lido pelo canal vivo neutrino_m2 como antes',
                            "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] "
                            "alfa e' medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a "
                            'definição de singularidade, a meu ver» (01/11/2026)',
                            "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                            'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
                'diz': ['a pedra ObservadorTerminal esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 26 teoremas do '
                        'contrato e os termos de suporte sao lidos deste kernel',
                        "o calculo: o terminal e' um so' (a gravidade); o leitor tem um unico ponto fixo e tres leituras bastam; a resistencia zera "
                        "so' no terminal; leitor^[3] e' idempotente; o colapso total tem exatamente dois pontos fixos (o posto e o abismo), nao e' "
                        "pressuposto e nao tem inversa; sem o abismo a leitura preservada e' constante; o terminal le 1 e o abismo le 0 na leitura "
                        'binaria; ao lado, omega(I) = 1 no core (o polo omega do par: homonimo)',
                        "o posto do observador e' o terminal: quem credita, ratifica, nomeia e poe o 1 age pelo terminal; a fusao de tudo num so' "
                        "posto e' o colapso, e o colapso e' um Um posto do kernel"],
                'nao_diz': ['que a gravidade, a luz ou o observador humano sejam entidades desta pedra (os niveis sao rotulos de posicao)',
                            "que o polo omega do par e o nivel terminal da cascata sejam o mesmo objeto (homonimo: nenhum termo os liga; liga-los e' "
                            'leitura [ONTO] do operador)',
                            'que a pedra construa o colapso fisico',
                            'que a leitura de engenharia (resistencia) seja termo de kernel',
                            'que isto seja um teste: nao ha desfecho experimental',
                            'que a gravidade quantica esteja creditada na natureza',
                            "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                            'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
                'extras': {'cited_support': ['TGLExt.UmPostoRelacao.no_posto_reading_is_pressupposed',
                                             'TGLExt.UmPostoRelacao.posto_paid_loss',
                                             'TGLExt.UmPostoRelacao.pressupposed_is_never_posto',
                                             'TGLExt.gravity_is_observed_by_nothing',
                                             'TGLExt.light_observes_nothing',
                                             'TGLExt.omega_of_one',
                                             'TGLExt.res_judicata_is_terminal'],
                           'reading': {'status': 'INPUT/ONTO',
                                       'content': "o posto do observador e' o terminal; a fusao de tudo num so' posto e' o colapso, e o colapso e' o "
                                                  "ponto terminal da resistencia da estrutura (teoria das estruturas); o par 1=1 | 1=0 e' necessario "
                                                  'para que a fusao seja posto [INPUT/ONTO]',
                                       'is_a_kernel_term': False},
                           'homonimo_terminal': {'status': 'ONTO',
                                                 'polo': 'the_omega_pole_reads_one: omega(I) = 1, o polo omega do par alfa/omega '
                                                         '(TheAlphaAndTheOmega)',
                                                 'nivel': 'the_fixed_points_read_one_and_zero: o nivel gravidade da cascata, na leitura binaria',
                                                 'liga_os_dois': "nenhum termo; a ligacao e' leitura do operador",
                                                 'is_a_kernel_term': False},
                           'name_status': {'quem': 'operador',
                                           'quando': '31/10/2026 (mantido em 01/11/2026)',
                                           'nome': 'observador=terminal',
                                           'sha16_da_fala': 'e4e105fe14615f39',
                                           'fala': 'observador=terminal'},
                           'r1_para_r2': {'r1': 'a fusao total tipada como PRESSUPOSTA (manha de 31/10)',
                                          'correcao_do_operador_sha16': 'a22a54dfc97d9611',
                                          'r2': "a fusao e' o colapso e o colapso e' um Um posto do kernel (o par no espaco de estados); os teoremas "
                                                'da r1 ficam como o caso sem o par: sem o par nao ha posto'},
                           'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
                'veredito_ok': 'TGL_OBSERVADOR_TERMINAL_V405__THE_OBSERVERS_POSTO_IS_THE_TERMINAL__THE_TERMINAL_IS_UNIQUE_AND_THE_ONLY_FIXED_POINT_OF_THE_READING__THE_FUSION_IS_THE_COLLAPSE_AND_THE_COLLAPSE_IS_A_POSTO_OF_THE_KERNEL__NOT_PRESUPPOSED__PAID_LOSS__TWO_FIXED_POINTS_THE_POSTO_AND_THE_ABYSS__THE_PAIR_IS_NECESSARY__THE_FIXED_POINTS_READ_ONE_AND_ZERO__THE_OMEGA_POLE_IS_A_HOMONYM_ITS_LINK_IS_A_READING__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'diminuto': {'estatuto': '[REAL] os termos do kernel (os 39 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: '
                          'TGLCoupling.alpha, TGLCoupling.beta_eq_alpha_exp, massa_da_transicao_derivada, massa_derivada_eq_beta_mul, half_sq, '
                          'peso_da_face_absoluta, absolute_faces_half, CollapseCostLaw.local_half; citados fora: no_positive_scale_invariant, '
                          'Sonico.the_pin_is_not_the_half_nat, the_charge_never_completes) e o calculo com beta = alfa CODATA 2018 x sqrt(e) em '
                          "runtime e u = 1 eV [POSTO]; [REAL] o diminuto e' MODULACAO, nao transposicao: so' a tonica desce o meio-tom pinado, as "
                          "demais notas ficam sustentadas, elas e as razoes entre elas ficam (a escala e' o que fica parado) e nenhum fator leva o "
                          "acorde ao acorde modulado; E0 e' o valor da tonica modulada; cada intervalo a tonica abre meio-tom; a resolucao devolve o "
                          "acorde; o meio-tom desfaz o sqrt e; beta = alfa.e^(1/2); dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e' "
                          'teorema; [DEF] Acorde, notaPrincipal, transpor e razao, da estrutura do AcordeE0.lean do Kimi (sha16 5da93b9e5e65a4ed), '
                          "modular, resolver e lerE0; [INPUT/ONTO] o meio-tom (meioTom: o tom e' a nat), a modulacao (modular, lerE0) e a tonica "
                          "(beta/alfa).u entram como DEFINICAO: E0_relativo_pinado e' a definicao de lerE0 dita como razao; beta/alfa = sqrt e e' a "
                          "definicao de TGLCoupling.alpha, e E0 = u e' identidade algebrica, que nao fixa u; [REAL, igualdades de VALOR] "
                          'meioTom_e_o_pedagio_local e meioTom_e_a_face; [INPUT] CollapseCostLaw, no kernel; [INPUT] a lei («ele desce meio tom '
                          'pinado, essa é a lei», 31/10/2026, sha16 8300a509ca9549e3), «pra mim o TOm é a NAT» (sha16 270fd74d5d79bf4d), «E0 é igual '
                          'ler um acorde E0» e «E0 não é absolutamente livre» (sha16 79c7999956e6d8e0), «o meu um absoluto é o um de 1 eV» (sha16 '
                          '9445171a763afcfc), a ordem da revisita (01/11/2026, sha16 7e2454bc48ec47de), a resposta «no diminuto vc não desce toda a '
                          'escala e nem muda o tom da escala, vc apenas modula a tônica» (sha16 7c2caaa87b0cdb01) e o nome «Lei do diminuto» (sha16 '
                          '1f16a74c05d9d4cb); [POSTO] a unidade; [MEDIDA] alfa, nao derivada; [ONTO] alfa como a magnitude (cauda) da inscricao no '
                          'bulk e «no harmônico o diminuto é a espera»; [INPUT] o tom fica, na fala dele: o kernel nao tem termo para o tom; [OPEN] '
                          'quais sao as cinco notas',
              'escopo': '[REAL] A pedra TGLExt/LeiDoDiminuto.lean (Lei do diminuto, nome do operador; antes LeiDoMeioTom r2) prova: (1) o meio-tom '
                        'pinado e^(-1/2) esta em (0, 1) e desfaz exatamente o sqrt e; (2) beta = alfa.e^(1/2) (a definicao de TGLCoupling.alpha, '
                        "invertida): o acoplamento e' a magnitude alfa da inscricao vezes o volume sqrt e da fronteira; (3) a lei: E0 = "
                        "meioTom.E_pent; dada a tonica, E0 esta determinado; a massa le alfa.(sqrt2/2).E_pent; a tonica sqrt e da E0 = 1 e so' ela; "
                        '(4) A FORMULA DA MASSA: m = U.alfa.e^(1/2).sen45 -- o Um posto, a magnitude alfa, o volume sqrt e, a projecao transversal; '
                        "em U = 1, m = beta.sen45 (a forma da v404, teorema dadas as entradas); (5) a oitava nao e' numero inteiro de meios-tons; "
                        "(6) O CAMPO FECHADO (01/11/2026): a tonica deixa de ser campo -- tonica c u := (beta/alfa).u = sqrt e.u e' uma DEFINICAO, "
                        'que nao traz informacao alem do u posto -- e a lei construida (leiDerivada) pousa em E0 = u por identidade algebrica; no Um '
                        'posto E0 = 1 e m = beta.sqrt2/2. O ACORDE (a revisita ordenada pelo operador e a resposta dele, 01/11/2026): (7) cinco '
                        'notas reais, a nota principal de indice 0 (Acorde, notaPrincipal, transpor, razao: a estrutura do AcordeE0.lean do Kimi, '
                        "sha16 5da93b9e5e65a4ed, em portugues); (8) O DIMINUTO E' MODULACAO: modular: so' a nota principal desce o meio-tom; as "
                        "outras quatro ficam sustentadas (modular_sustenta); as notas sustentadas e as razoes entre elas ficam: a escala e' o que "
                        'fica parado (modular_mantem_a_escala); [INPUT] o tom fica, na fala dele: o kernel nao tem termo para o tom; a razao a '
                        "tonica muda, e e' a tonica que se move; nao e' transposicao: com tonica e outra nota nao nulas, nenhum fator leva o acorde "
                        'ao acorde modulado (modular_nao_e_transposicao): o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das '
                        "notas sustentadas, mas nao quebra a liberdade global; (9) E0 e' o valor da tonica modulada (lerE0_e_a_tonica_modulada); "
                        "E0_relativo_pinado: E0/tonica = e^(-1/2) em todo acorde: e' a definicao de lerE0 dita como razao, nada mais; (10) AS "
                        'TERCAS: cada intervalo a tonica abre meio-tom (razao_abre_meio_tom), e a nota que estava um tom acima fica em e^(3/2) '
                        "(um_tom_vira_terca_menor): «o sistema está operando em terças» e', no kernel, a aritmetica 1 nat + 1/2 nat; a resolucao "
                        "devolve o acorde (resolver_modular); [ONTO] «no harmônico o diminuto é a espera»: a forma no kernel e' "
                        "the_charge_never_completes; (11) transpor e' outra coisa, so' a liberdade do no-go: o acorde inteiro multiplicado pelo "
                        'mesmo fator; preserva toda razao (transpor_preserva_toda_razao, o teorema do Kimi); dois acordes tem as mesmas razoes sse '
                        "um e' a transposicao do outro (mesmas_razoes_iff_transposicao); a leitura e a modulacao a acompanham (lerE0_transpor, "
                        'modular_comuta_com_transpor); as razoes nao fixam o absoluto (as_razoes_nao_fixam_o_absoluto); (12) igualdades de VALOR: '
                        'meioTom_e_o_pedagio_local, meioTom_e_a_face, tonica_e_o_volume_da_face, o_tom_e_as_duas_faces; (13) o fecho: '
                        "the_diminished_law_closes. A distincao e' do operador, «E0 não é absolutamente livre»: o valor ABSOLUTO segue livre e o "
                        'no-go nao cai; o valor RELATIVO a tonica esta pinado; sobra um unico grau de liberdade global, a transposicao do acorde '
                        'inteiro. O calculo CONFERE em dupla precisao, com um acorde de TESTE, e rele o m_nu do programa a 1e-12: o NUMERO nao muda',
              'limites': ["[REAL] a pedra NAO deriva a unidade: «1 eV» e' o Um POSTO pelo operador (como o 1 de echo 1 | python um.py), ao lado de "
                          "alfa [MEDIDA]; alfa como a magnitude (cauda) da inscricao no bulk e' leitura do operador [ONTO] sobre "
                          "Verdade.alpha_is_measured_from_within; a tonica em eV nao vem do Hamiltoniano oculto: e' a definicao (beta/alfa).u na "
                          'unidade posta, e E0 = u nao fixa u',
                          "[OPEN] quais sao as cinco notas: nenhum texto as nomeia; so' se sabe, por fala do operador, que o angulo de Miguel "
                          'pertence a pentada; a pentada do teorema mestre sao cinco componentes, nao cinco autovalores; a pedra vale para todo '
                          "acorde, e o acorde do calculo e' de TESTE",
                          "[ONTO] «no harmônico o diminuto é a espera» e' leitura do operador; a forma no kernel e' the_charge_never_completes; o "
                          'kernel nao diz que a resolucao espera',
                          '[REAL, igualdades de VALOR] meioTom_e_o_pedagio_local e meioTom_e_a_face dizem que os numeros coincidem, nao que sejam o '
                          "mesmo objeto; CollapseCostLaw e' [INPUT] no kernel; ler esse 1/2 como o meio-tom e' do operador [ONTO]",
                          '[DECLARADO, normalizacao definicional] a calibracao <K_d>_total = 1 nat de 24/06/2026 (half_nat_araki_hidden_hamiltonian; '
                          "HALF_NAT_ARAKI_HIDDEN_HAMILTONIAN_TEST_REPORT.md, sha16 c23ce83106c69ff6) e' normalizacao definicional, omega(I) = 1 na "
                          "base e; nao e' termo do kernel e nao e' medida; fixa intervalos em nat, nao a unidade em eV: U_E_NOT_DERIVED fica como "
                          'esta, e m2 nao muda',
                          'E11 -- a v404 (registro projecao_transversal_v404, decisao D26, erratas E7) e os adendos 1 a 5 do handoff v405 dizem «E0 '
                          '= 1 eV segue DECLARADO» e citam os nomes PROVISORIOS das pedras (PonteDaMassaTransversal, EmprestimoDaMassa, '
                          "E0LiberdadeDeEscala, LeiDoMeioTom); isto era verdadeiro na data; em 31/10/2026 o operador POS a unidade (u = 1 eV e' o Um "
                          'posto) e em 01/11/2026 deu os nomes (Ponte da Massa, Massa=tensao pura, Observador=terminal, Tonica do Hamiltoniano, Lei '
                          'do diminuto, Disco de Euler, Ponto Zero do Psion); os textos da v404 ficam como registro',
                          'E13 -- o recibo RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, o adendo 6 do handoff v405 e a ordem da preparacao desta versao '
                          "(gerencia c1, 01/11/2026) escreveram que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; isto "
                          'afirmava demais e foi erro da gerencia: os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo '
                          'para a DEFINICAO; a leitura fisica nao virou teorema. Entram um Um posto, uma alfa medida e as leituras do operador; '
                          "dadas essas entradas, a FORMA e' teorema. Quatro teoremas foram rebatizados antes do selo "
                          '(RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou por isso): '
                          'nenhuma_hipotese_resta -> a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> '
                          'the_tonic_lands_on_the_posted_unit; the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one '
                          "-> the_omega_pole_reads_one: o nome afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o "
                          'polo omega do par, nao sobre o nivel terminal da cascata). A revisao de terceiro pegou, antes do selo, frases residuais '
                          'nas docstrings das oito pedras, corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho '
                          'do observador a leitura binaria (the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; '
                          'o no-go de E0 NAO cai, ele se localiza no Um posto. A revisita da Lei do Diminuto, ordenada pelo operador '
                          '(RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e _R5), corrigiu tres coisas: o acorde nao estava tipado (o AcordeE0.lean do '
                          'Kimi, sha16 5da93b9e5e65a4ed, o tinha); a frase sobre o no-go errou por excesso e por falta; e a primeira correcao leu a '
                          "segunda metade da lei como transposicao, erro da gerencia: o diminuto e' MODULACAO, so' a tonica desce e as demais notas "
                          "ficam sustentadas, e transpor e' so' a liberdade do no-go. Vigente: a escala e' o que fica parado, as notas sustentadas e "
                          "as razoes entre elas, e quem se move e' a tonica; o valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a "
                          'tonica esta pinado; sobra um unico grau de liberdade global, a transposicao do acorde inteiro; o meio-tom pinado quebra a '
                          'simetria do acorde, porque separa a tonica das notas sustentadas, mas nao quebra a liberdade global',
                          "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel "
                          "nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido "
                          'pelo canal vivo neutrino_m2 como antes',
                          "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] alfa "
                          "e' medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a definição de "
                          'singularidade, a meu ver» (01/11/2026)',
                          "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                          'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
              'diz': ['a pedra LeiDoDiminuto esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 39 teoremas do contrato '
                      'e os termos de suporte sao lidos deste kernel',
                      "o calculo, com beta = alfa CODATA 2018 x sqrt(e): o meio-tom desfaz o sqrt e; beta = alfa.e^(1/2); a tonica definida e' sqrt "
                      "e.u e o diminuto pousa em E0 = u; m = U.alfa.e^(1/2).sqrt2/2 = o m_nu do programa a 1e-12 (U = 1 eV posto); ln 2 nao e' n/2 e "
                      'fica entre um e dois meios-tons; E0 = 1 <=> tonica = sqrt e',
                      "o calculo do acorde, num acorde de TESTE: so' a tonica desce e as demais ficam sustentadas; as razoes entre as sustentadas "
                      "nao mudam; E0/tonica = e^(-1/2); o acorde modulado nao e' transposicao do original (controle negativo); um tom acima da "
                      'tonica vira e^(3/2); a resolucao devolve o acorde; a transposicao preserva as razoes',
                      "o diminuto e' modulacao, nao transposicao; o valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta "
                      'pinado; sobra um unico grau de liberdade global, a transposicao do acorde inteiro; o meio-tom pinado quebra a simetria do '
                      'acorde, nao a liberdade global',
                      "um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' teorema; o numero da massa e o "
                      'veredito do canal nao mudam'],
              'nao_diz': ["que a unidade u (1 eV) tenha sido derivada (e' posta)",
                          "que alfa tenha sido derivado (e' medida por dentro)",
                          "que a tonica tenha sido derivada do Hamiltoniano oculto (e' uma definicao na unidade posta)",
                          "que E0 = u fixe u (e' identidade algebrica)",
                          "que o no-go tenha caido: o valor ABSOLUTO segue livre; so' o RELATIVO a tonica esta pinado",
                          "que o diminuto seja transposicao (transpor e' so' a liberdade do no-go)",
                          'quais sao as cinco notas ([OPEN]; as do calculo sao numeros de teste)',
                          'que a pentada do teorema mestre sejam cinco autovalores (sao cinco componentes)',
                          'que a razao a tonica seja a escala (a razao a tonica muda; a escala fica)',
                          'que o kernel tenha termo para o tom (o tom fica, na fala dele)',
                          'que E0_relativo_pinado seja mais do que a definicao de lerE0 dita como razao',
                          'que o meio-tom seja o pedagio local ou o peso da face: sao igualdades de VALOR',
                          "que a calibracao de 1 nat seja medida, termo do kernel ou a unidade em eV (e' normalizacao definicional)",
                          'que o valor absoluto tenha sido escolhido pelo dado (nem 1,02 eV nem outro)',
                          'que isto seja um teste: nao ha desfecho experimental',
                          'que a gravidade quantica esteja creditada na natureza',
                          "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                          'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
              'extras': {'cited_support': ['ChatgptAudit.Collapse057.CollapseCostLaw.local_half',
                                           'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul',
                                           'TGLExt.PonteDaMassa.half_sq',
                                           'TGLExt.PonteDaMassa.massa_da_transicao_derivada',
                                           'TGLExt.PonteDaMassa.peso_da_face_absoluta',
                                           'TGLExt.TGLCoupling.alpha',
                                           'TGLExt.TGLCoupling.beta_eq_alpha_exp',
                                           'TGLExt.absolute_faces_half'],
                         'formula_da_massa': {'status': 'REAL (a forma, termo do kernel) + POSTO (U = 1 eV) + MEDIDA (alfa) + INPUT/ONTO (as '
                                                        'leituras massaDerivada e a tonica)',
                                              'content': 'm = U . alfa . e^(1/2) . sqrt2/2; em U = 1 (na unidade posta): m = beta . sqrt2/2; o '
                                                         "numero e' o da v404 (8,5074 meV)",
                                              'cunhagem_sha16': '9445171a763afcfc',
                                              'fala': 'o meu um absoluto é o um de 1 eV'},
                         'a_lei': {'o_diminuto': "modular: so' a tonica desce o meio-tom pinado; modular_sustenta: as demais notas ficam; "
                                                 'modular_mantem_a_escala: as razoes entre as sustentadas nao mudam; modular_nao_e_transposicao',
                                   'o_valor': 'lerE0_e_a_tonica_modulada; E0_relativo_pinado, a definicao dita como razao',
                                   'as_tercas': 'razao_abre_meio_tom; um_tom_vira_terca_menor: a aritmetica 1 nat + 1/2 nat',
                                   'a_resolucao': 'resolver_modular',
                                   'a_transposicao': "so' a liberdade do no-go",
                                   'o_fecho': 'the_diminished_law_closes',
                                   'fala': 'no diminuto vc não desce toda a escala e nem muda o tom da escala, vc apenas modula a tônica',
                                   'sha16_da_fala': '7c2caaa87b0cdb01'},
                         'os_dois_valores': {'a_escala': 'a musical: o que fica parado, as notas sustentadas e as razoes entre elas '
                                                         '(modular_mantem_a_escala)',
                                             'valor_absoluto': 'segue livre; o no-go nao cai (no_function_of_the_inscription_fixes_E0; '
                                                               'as_razoes_nao_fixam_o_absoluto)',
                                             'valor_relativo_a_tonica': 'pinado (E0_relativo_pinado)',
                                             'o_que_sobra': 'um unico grau de liberdade global, a transposicao do acorde inteiro',
                                             'a_simetria': 'o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das notas '
                                                           'sustentadas, mas nao quebra a liberdade global',
                                             'distincao_do_operador': 'E0 não é absolutamente livre',
                                             'sha16_da_fala': '79c7999956e6d8e0'},
                         'a_espera': {'status': 'ONTO',
                                      'fala': 'no harmônico o diminuto é a espera',
                                      'forma_no_kernel': 'the_charge_never_completes',
                                      'is_a_kernel_term': False},
                         'acorde': {'origem': 'AcordeE0.lean do Kimi (31/10/2026): Acorde, transpor, razao e o teorema da razao',
                                    'sha16': '5da93b9e5e65a4ed',
                                    'as_cinco_notas': 'OPEN',
                                    'reading': "o diminuto modula a tonica: so' ela desce o meio-tom pinado, as demais notas ficam sustentadas, elas "
                                               "e as razoes entre elas ficam: a escala e' o que fica parado, e a razao a tonica muda; o tom fica, na "
                                               "fala dele, sem termo no kernel; E0 e' o valor da tonica modulada; o sistema opera em tercas; "
                                               "transpor e' outra coisa, so' a liberdade do no-go; quais sao as cinco notas e' [OPEN]; so' se sabe, "
                                               'por fala do operador, que o angulo de Miguel pertence a pentada; a pentada do teorema mestre sao '
                                               'cinco componentes, nao cinco autovalores [INPUT/ONTO/OPEN]'},
                         'calibracao_de_1_nat': {'status': "DECLARADO: normalizacao definicional, omega(I) = 1 na base e; nao e' termo do kernel; "
                                                           "nao e' medida",
                                                 'relatorio_sha16': 'c23ce83106c69ff6',
                                                 'fixa': 'intervalos em nat',
                                                 'nao_fixa': 'a unidade em eV: U_E_NOT_DERIVED fica como esta; m2 nao muda'},
                         'name_status': {'quem': 'operador',
                                         'quando': '01/11/2026',
                                         'nome': 'Lei do diminuto',
                                         'antes': 'LeiDoMeioTom (provisorio, 31/10)',
                                         'sha16_da_fala': '1f16a74c05d9d4cb'},
                         'tom': {'status': 'INPUT',
                                 'content': "o tom e' a nat; E0 nao desce a oitava, desce meio-tom pinado (a Meia-Nat), mantendo a escala da pentada "
                                            'definida pelo Hamiltoniano oculto [INPUT]; no acervo, a calibracao <K_d>_total = 1 nat de 24/06/2026 '
                                            "diz em que sentido: nos intervalos, em nat; nao da' a unidade em eV"},
                         'campos_fechados': {'E_pent (Lei)': 'a definicao tonica c u := (beta/alfa).u (tonica_eq: = sqrt e.u); leiDerivada_E0: E0 = '
                                                             'u'},
                         'leituras_que_entram': [{'n': 3,
                                                  'estatuto': 'INPUT/ONTO',
                                                  'leitura': "a tonica (beta/alfa).u: beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha, e E0 = "
                                                             "u e' identidade algebrica, que nao fixa u: o no-go NAO cai, ele se localiza no Um "
                                                             'posto',
                                                  'definicao_lean': 'TGLExt.LeiDoDiminuto.tonica',
                                                  'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                  'entra_como': 'DEFINICAO, nao teorema'},
                                                 {'n': 5,
                                                  'estatuto': 'INPUT/ONTO',
                                                  'leitura': "o meio-tom e^(-1/2): o tom e' a nat, fala do operador; definicao da mesma natureza da "
                                                             'tonica, necessaria a E0 = u; meioTom_e_o_pedagio_local e meioTom_e_a_face sao '
                                                             'igualdades de VALOR',
                                                  'definicao_lean': 'TGLExt.LeiDoDiminuto.meioTom',
                                                  'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                  'entra_como': 'DEFINICAO, nao teorema'},
                                                 {'n': 11,
                                                  'estatuto': 'INPUT/ONTO',
                                                  'leitura': "E0 como o valor da tonica modulada: modular so' desce a nota principal e sustenta as "
                                                             "demais; lerE0 e' esse valor, e E0_relativo_pinado e' essa definicao dita como razao",
                                                  'definicao_lean': 'TGLExt.LeiDoDiminuto.modular',
                                                  'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                  'entra_como': 'DEFINICAO, nao teorema'},
                                                 {'n': 12,
                                                  'estatuto': 'INPUT',
                                                  'leitura': 'm1 = 0: entrada da identificacao de m2 com o Delta m^2_21 medido (apontada pelo Kimi); '
                                                             'nao tem termo no kernel',
                                                  'definicao_lean': None,
                                                  'modulo': None,
                                                  'entra_como': 'ENTRADA da identificacao, nao teorema'}],
                         'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
              'veredito_ok': 'TGL_LEI_DO_DIMINUTO_V405__THE_DIMINISHED_MODULATES_THE_TONIC_AND_SUSTAINS_THE_OTHER_NOTES__IT_IS_NOT_A_TRANSPOSITION__THE_PINNED_HALF_TONE_E_TO_MINUS_HALF_UNDOES_SQRT_E__BETA_EQUALS_ALPHA_TIMES_SQRT_E_BY_THE_DEFINITION_OF_ALPHA__THE_DEFINED_TONIC_LANDS_ON_E0_EQUALS_U_AN_ALGEBRAIC_IDENTITY_THAT_DOES_NOT_FIX_U__GIVEN_THE_INPUTS_THE_FORM_M_EQUALS_U_ALPHA_SQRT_E_SIN45_IS_A_THEOREM__THE_SCALE_IS_WHAT_STAYS_THE_SUSTAINED_NOTES_AND_THE_RATIOS_AMONG_THEM__THE_TRANSPOSITION_IS_ONLY_THE_FREEDOM_OF_THE_NO_GO__THE_ABSOLUTE_VALUE_STAYS_FREE_THE_VALUE_RELATIVE_TO_THE_TONIC_IS_PINNED__THE_NUMBER_DOES_NOT_CHANGE__THE_OCTAVE_IS_NOT_A_WHOLE_NUMBER_OF_HALF_TONES__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'tonica': {'estatuto': '[REAL] os termos do kernel (os 14 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: leiDerivada_E0, '
                        'leiDerivada_no_um_posto, neutrinoMassForm, massa_derivada_eq_beta_mul; citado fora: Verdade.alpha_is_measured_from_within) '
                        'e o calculo com beta = alfa CODATA 2018 x sqrt(e) em runtime e u = 1 eV [POSTO]; [REAL] o no-go (nenhuma funcao da '
                        "inscricao fixa E0: a forma e' homogenea de grau 1 em E0), que NAO cai: ele se localiza no Um posto; a tonica definida pousa "
                        'em E0 = u por identidade algebrica; as identidades da rota do monopolo e da leitura autoconsistente; [INPUT] «E0 não é '
                        'absolutamente livre, porque a escala (pentada) já definiu pelo hamiltoniano oculto» (31/10/2026, sha16 79c7999956e6d8e0), a '
                        'pergunta «consegue derivar a constante da estrutura fina?» (01/11/2026, sha16 3aafdd3f9e7ea518) e a leitura «não tem '
                        'teorema para o ângulo de Miguel é a definição de singularidade» (sha16 f0fdd2c1f770e34a); o nome «Tônica do Hamiltoniano» '
                        '(sha16 1f16a74c05d9d4cb); [MEDIDA] alfa, por dentro, nao derivada (a resposta a pergunta foi NAO; parede medida, nao '
                        'falsificacao)',
            'escopo': '[REAL] A pedra TGLExt/TonicaDoHamiltoniano.lean (Tonica do Hamiltoniano, nome do operador; antes E0LiberdadeDeEscala) prova: '
                      "(1) a liberdade do valor absoluto: a transicao reescalada (E0 -> lambda.E0, a mesma inscricao) e' transicao; a massa derivada "
                      "cresce linearmente; a forma do neutrino e' homogenea de grau 1; o valor absoluto e' livre (the_scale_is_free); e O NO-GO: "
                      "nenhuma f(c, theta) fixa E0 (a mesma inscricao carrega E0 = 1 e E0 = 2) -- o que a forma fixa e' a razao m/E0 = beta.sen45: a "
                      'reescala muda E0 e a massa pelo mesmo fator e a razao nao muda (the_ratio_survives_the_rescaling); a reescala corresponde a '
                      'transposicao do acorde, a liberdade do no-go, que fala do valor ABSOLUTO; a Lei do diminuto fala do valor RELATIVO a tonica; '
                      "(2) Gamma_B = beta/tau e' a lei canonica Gamma = (1/2).beta.tau.omega^2 lida em omega* = sqrt2/tau; (3) tau* = 4piGE/c^5 e' o "
                      "tempo de luz da circunferencia de Schwarzschild da energia, e q = GE/c^4 e' r_s/2: a rota do monopolo e' o horizonte do "
                      'proprio sistema (tautologica quanto ao valor absoluto); (4) a leitura autoconsistente pina omega = 2/tau; (5) A TONICA NA '
                      'UNIDADE POSTA: the_tonic_lands_on_the_posted_unit -- na lei construida a tonica (beta/alfa).u = sqrt e.u pousa em E0 = u, '
                      "identidade algebrica: quem fixa E0 e' o u posto que a tonica carrega; o no-go NAO cai, ele se localiza no Um posto -- e "
                      'the_tonic_at_the_posted_one: no Um posto E0 = 1 e m = beta.sqrt2/2 (a FORMA, sob a leitura massaDerivada). O calculo CONFERE '
                      "em dupla precisao (SI so' para as identidades) e rele o m_nu do programa a 1e-12",
            'limites': ["[REAL] a pedra nao afirma que E0 seja inderivavel por qualquer principio futuro: so' que a FORMA (a ponte 1 e o que ela "
                        "importa) nao o fixa, e que E0 = u e' identidade algebrica na unidade POSTA; nao toca beta (jamais literal); as constantes "
                        "G, c, hbar entram so' nas identidades da rota do monopolo",
                        '[INPUT] a pergunta do operador «consegue derivar a constante da estrutura fina?» foi respondida NAO pela gerencia c1 em '
                        '01/11/2026 (rota alpha.derivacao.pergunta_do_operador_01nov no Mapa de Rotas); a leitura dele «não tem teorema para o '
                        'ângulo de Miguel é a definição de singularidade» entra aqui como nota, nao como teorema; nenhuma formula de alfa por ajuste '
                        '(numerologia proibida)',
                        'E13 -- o recibo RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, o adendo 6 do handoff v405 e a ordem da preparacao desta versao '
                        "(gerencia c1, 01/11/2026) escreveram que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; isto "
                        'afirmava demais e foi erro da gerencia: os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo '
                        'para a DEFINICAO; a leitura fisica nao virou teorema. Entram um Um posto, uma alfa medida e as leituras do operador; dadas '
                        "essas entradas, a FORMA e' teorema. Quatro teoremas foram rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e "
                        'RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou por isso): nenhuma_hipotese_resta -> '
                        'a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> the_tonic_lands_on_the_posted_unit; '
                        'the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one -> the_omega_pole_reads_one: o nome '
                        "afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o polo omega do par, nao sobre o nivel "
                        'terminal da cascata). A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, '
                        'corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria '
                        '(the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se '
                        'localiza no Um posto. A revisita da Lei do Diminuto, ordenada pelo operador (RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e '
                        '_R5), corrigiu tres coisas: o acorde nao estava tipado (o AcordeE0.lean do Kimi, sha16 5da93b9e5e65a4ed, o tinha); a frase '
                        'sobre o no-go errou por excesso e por falta; e a primeira correcao leu a segunda metade da lei como transposicao, erro da '
                        "gerencia: o diminuto e' MODULACAO, so' a tonica desce e as demais notas ficam sustentadas, e transpor e' so' a liberdade do "
                        "no-go. Vigente: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas, e quem se move e' a tonica; o "
                        'valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta pinado; sobra um unico grau de liberdade '
                        'global, a transposicao do acorde inteiro; o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das notas '
                        'sustentadas, mas nao quebra a liberdade global',
                        "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao "
                        "e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido pelo "
                        'canal vivo neutrino_m2 como antes',
                        "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] alfa e' "
                        'medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a definição de '
                        'singularidade, a meu ver» (01/11/2026)',
                        "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                        'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
            'diz': ['a pedra TonicaDoHamiltoniano esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 14 teoremas do '
                    'contrato e os termos de suporte sao lidos deste kernel',
                    'o calculo, com beta = alfa CODATA 2018 x sqrt(e): a massa cresce linearmente com E0 (quatro lambdas); a mesma inscricao carrega '
                    'E0 = 1 e E0 = 2 (o no-go); Gamma_B = beta/tau em quatro taus; as identidades do monopolo e da leitura autoconsistente; a tonica '
                    'pousa em E0 = u e no Um posto m = beta.sqrt2/2 = o m_nu do programa a 1e-12',
                    "o no-go NAO cai: ele se localiza no Um posto; a forma nao fixa E0, e o que a tonica pousa e' o u posto que ela mesma carrega; a "
                    "razao m/E0 sobrevive a reescala; alfa segue medida por dentro: a singularidade e' o ponto sem teorema"],
            'nao_diz': ["que a tonica fixe o valor absoluto: quem o fixa e' o Um posto",
                        'que o no-go tenha caido',
                        'que alfa tenha sido derivado (a resposta foi NAO; a pergunta do operador fica respondida, nao aberta)',
                        'que a unidade u tenha sido derivada',
                        "que a rota do monopolo fixe o valor absoluto (e' tautologica)",
                        'que o valor absoluto tenha sido escolhido pelo dado',
                        'que isto seja um teste: nao ha desfecho experimental',
                        'que a gravidade quantica esteja creditada na natureza',
                        "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                        'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
            'extras': {'cited_support': ['TGLExt.LeiDoDiminuto.leiDerivada_E0',
                                         'TGLExt.LeiDoDiminuto.leiDerivada_no_um_posto',
                                         'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul',
                                         'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm'],
                       'alfa': {'status': 'MEDIDA/INPUT (parede medida; rota alpha.derivacao.pergunta_do_operador_01nov)',
                                'content': "alfa e' MEDIDA por dentro (Verdade.alpha_is_measured_from_within), nunca derivada: «a constante da "
                                           'esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk» (31/10); «não tem teorema para o ângulo '
                                           'de Miguel é a definição de singularidade, a meu ver» (01/11): parede medida, nao falsificacao; nenhuma '
                                           'formula de alfa por ajuste [MEDIDA/INPUT/ONTO]',
                                'pergunta_sha16': '3aafdd3f9e7ea518',
                                'leitura_sha16': 'f0fdd2c1f770e34a',
                                'fala': 'não tem teorema para o ângulo de Miguel é a definição de singularidade, a meu ver'},
                       'name_status': {'quem': 'operador',
                                       'quando': '01/11/2026',
                                       'nome': 'Tônica do Hamiltoniano',
                                       'antes': 'E0LiberdadeDeEscala (provisorio, 31/10)',
                                       'sha16_da_fala': '1f16a74c05d9d4cb'},
                       'no_go_e_tonica': {'no_go': 'nenhuma funcao da inscricao fixa E0 (the_scale_is_free, '
                                                   'no_function_of_the_inscription_fixes_E0); NAO cai',
                                          'tonica': 'a tonica pousa na unidade posta: E0 = u, identidade algebrica '
                                                    "(the_tonic_lands_on_the_posted_unit); quem fixa e' o posto",
                                          'a_razao': 'a reescala preserva m/E0 (the_ratio_survives_the_rescaling): o no-go fala do valor ABSOLUTO; a '
                                                     'Lei do diminuto, do valor RELATIVO a tonica'},
                       'leituras_que_entram': [{'n': 3,
                                                'estatuto': 'INPUT/ONTO',
                                                'leitura': "a tonica (beta/alfa).u: beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha, e E0 = u "
                                                           "e' identidade algebrica, que nao fixa u: o no-go NAO cai, ele se localiza no Um posto",
                                                'definicao_lean': 'TGLExt.LeiDoDiminuto.tonica',
                                                'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                'entra_como': 'DEFINICAO, nao teorema'}],
                       'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
            'veredito_ok': 'TGL_TONICA_DO_HAMILTONIANO_V405__THE_FORM_DOES_NOT_FIX_E0_NO_FUNCTION_OF_THE_INSCRIPTION_RETURNS_IT__THE_NO_GO_STANDS_AND_LOCALIZES_AT_THE_POSTED_ONE__THE_TONIC_LANDS_ON_THE_POSTED_UNIT_BY_AN_ALGEBRAIC_IDENTITY__GAMMA_B_IS_THE_CANONICAL_LAW_AT_THE_SYSTEMS_FREQUENCY__THE_MONOPOLE_ROUTE_IS_THE_HORIZON_OF_THE_SYSTEM__ALPHA_IS_MEASURED_FROM_WITHIN_NOT_DERIVED__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'disco': {'estatuto': '[REAL] os termos do kernel (os 13 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: '
                       'TGLCoupling.beta_pos, Fundacao.the_fall_never_lands, Fundacao.abismo) e o calculo sobre um disco-modelo (K, tau, E0 '
                       'adimensionais: dados do disco) com beta = alfa CODATA 2018 x sqrt(e) em runtime; [DEF] a energia linear E(t) = E0 - c.t e '
                       "Omega^2 = K/E; [REAL] dadas essas definicoes: Gamma.E = c; a E definida e' solucao do fluxo dE/dt = -Gamma.E antes da parada "
                       '(the_flow_is_the_canonical_law); E(t0) = 0 em tempo finito; Omega^2 sem cota antes de t0; o corte E^3 = hbar^2.K (algebra); '
                       "o valor do corte e' dado pelo invariante (the_scale_is_the_invariant); [INPUT/ONTO] a taxa de dephasing lida como taxa de "
                       'perda de energia; [ONTO] a inscricao do zero absoluto no infinito e a terceira lei na forma do disco, leituras do operador '
                       'sobre Omega^2 sem cota; [KNOWN] o disco de Euler (Moffatt, Nature 404, 833, 2000); [INPUT] a cunhagem (31/10/2026, sha16 '
                       'fe064b0b802c1d1a: «é a ressonância da parada do disco de euler sobre o espelho») e «O disco é o substrato psionico, o '
                       'condensado psionico» (sha16 dc150f9bbc5b1a4a); o nome (sha16 1f16a74c05d9d4cb); [ONTO] a leitura do disco como o condensado '
                       "psionico; [OPEN] QUAL e' o disco (o invariante K) -- pergunta do operador; nenhum K escolhido pelo alvo",
           'escopo': '[REAL] A pedra TGLExt/DiscoDeEuler.lean (Disco de Euler, nome do operador) tipa o disco: um invariante K = Omega^2.E > 0, a '
                     "lei canonica (beta, tau*) e a energia inicial. [DEF] A energia e' linear por definicao, E(t) = E0 - c.t com c = "
                     '(1/2).beta.tau*.K (E, E_linear), e Omega^2 = K/E (omegaSq). Dadas essas definicoes, prova: (1) Gamma_Omega.E = c '
                     "(the_loss_is_the_canonical_law) e, antes da parada, dE/dt = -Gamma_Omega.E (the_flow_is_the_canonical_law): a E definida e' "
                     "uma solucao do fluxo; ler a taxa de DEPHASING como taxa de perda de ENERGIA e' entrada [INPUT/ONTO], nao teorema; E(t0) = 0 em "
                     'tempo finito (stops_in_finite_time); (2) Omega^2 SEM COTA: antes da parada Omega^2 = K/E nao tem cota, para a energia linear '
                     'definida (frequency_squared_unbounded_at_the_stop) [REAL]; [ONTO] o operador le isso como a inscricao do zero absoluto no '
                     'infinito e como a terceira lei na forma do disco: leitura dele, nao teorema; (3) o contraste com o abismo: com taxa constante '
                     'a energia nunca toca o zero (with_constant_rate_the_fall_never_lands); (4) o corte: hbar.Omega = E acontece sse E^3 = hbar^2.K '
                     '(the_residual_resonance_iff) [REAL, algebra]; [ONTO] o operador le a energia do corte como a ressonancia que permanece e o '
                     'valor que nasce no infinito; (5) a parede nomeada: K = (e^(1/2).U)^3/hbar^2 (the_scale_is_the_invariant); (6) o campo fechado: '
                     'beta do disco vem do acoplamento (Disco.doAcoplamento). O calculo CONFERE num disco-modelo e REGISTRA, em SI, o K que a nota '
                     'posta de 1 eV exige (o tamanho da parede), sem o escolher',
           'limites': ['[REAL] a pedra NAO identifica o disco da TGL com nenhum sistema fisico nem deriva a unidade: K, tau e E0 sao DADOS do disco '
                       "(a sua identidade), nao hipoteses sobre a teoria; qual e' o disco e' pergunta do operador (a pergunta nas quatro linguas de "
                       '31/10 fica aberta); o Kimi mediu a mesma parede (U_E_NOT_DERIVED) e tem razao',
                       "[INPUT + OPEN] a pergunta, o operador respondeu que o sistema que da' a medida da tonica e' o angulo de Miguel (sha16 "
                       '7c2caaa87b0cdb01); a conexao tipada esta em PontoZeroDoPsion, secao O GAP; aqui fica o limite: o invariante K = Omega^2.E '
                       'nao depende da inclinacao, logo o angulo nao fixa K; K segue [OPEN]',
                       '[DEF + INPUT/ONTO] E(t) linear e Omega^2 = K/E sao definicoes da estrutura, nao consequencias; o teorema '
                       "the_flow_is_the_canonical_law diz que a E definida e' UMA solucao do fluxo; que a taxa de dephasing Gamma seja taxa de perda "
                       "de energia e' entrada [INPUT/ONTO] (a leitura 10 de campos_fechados_e_leituras_v405)",
                       "[KNOWN] os expoentes de Moffatt vem da dissipacao viscosa do ar; aqui a dissipacao e' a canonica da TGL (Gamma proporcional "
                       "a omega^2): e' o disco da TGL, nao o de Moffatt",
                       'E12 -- o adendo 4 do handoff v405 (DiscoDeEuler r1) e a pedra TGLExt/DiscoDeEuler.lean, antes da errata R2, escreveram K = '
                       '4Mg^2 para o invariante do disco de Euler real; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) corrige para K '
                       "= 6Mg^2 (Omega^2 = 4g/(a.alpha) com a energia TOTAL (3/2).M.g.a.alpha: o fator e' 6; com a energia potencial sozinha seriam "
                       '4Mg^2, a conta antiga); a pedra diz agora 6Mg^2 com a energia total e guarda a conta antiga ao lado; o invariante K do disco '
                       "da TGL segue um DADO do disco (qual e' o disco e' pergunta do operador), nao hipotese sobre a teoria; nenhum numero de K e' "
                       'escolhido pelo alvo',
                       "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao "
                       "e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido pelo "
                       'canal vivo neutrino_m2 como antes',
                       "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] alfa e' "
                       'medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a definição de '
                       'singularidade, a meu ver» (01/11/2026)',
                       "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                       'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
           'diz': ['a pedra DiscoDeEuler esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 13 teoremas do contrato e '
                   'os termos de suporte sao lidos deste kernel',
                   'o calculo num disco-modelo (K = 3, tau = 0,7, E0 = 2; beta do rito): Gamma.E = c; a E definida satisfaz dE/dt = -Gamma.E '
                   '(diferenca finita centrada); E(t0) = 0; Omega^2 vence toda cota antes da parada; com taxa constante nunca para; o corte E^3 = '
                   'hbar^2.K; K = (e^(1/2).U)^3/hbar^2; em SI o K que a nota posta exige fica registrado',
                   'Omega^2 nao tem cota antes da parada [REAL]; a inscricao do zero absoluto no infinito e a terceira lei sao leituras do operador '
                   "[ONTO]; a parede (qual e' o disco) esta nomeada, nao derivada"],
           'nao_diz': ['que o disco da TGL seja um sistema fisico identificado',
                       'que a unidade u tenha sido derivada do disco',
                       "que o invariante K tenha sido escolhido pelo alvo (nenhum numero de K e' escolhido)",
                       'que a dissipacao do disco real (viscosa) seja a canonica',
                       'que o angulo de Miguel fixe K (K nao depende da inclinacao)',
                       "que a energia seja linear por teorema (e' definicao; o teorema e' que a E definida resolve o fluxo)",
                       "que a taxa de dephasing seja taxa de perda de energia por teorema (e' entrada [INPUT/ONTO])",
                       'que a inscricao do zero no infinito ou a terceira lei sejam teoremas (sao leituras [ONTO] do operador)',
                       'que isto seja um teste: nao ha desfecho experimental',
                       'que a gravidade quantica esteja creditada na natureza',
                       "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                       'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
           'extras': {'cited_support': ['TGLExt.Fundacao.abismo', 'TGLExt.Fundacao.the_fall_never_lands', 'TGLExt.TGLCoupling.beta_pos'],
                      'reading_disk': {'status': 'ONTO/OPEN',
                                       'content': "o disco de Euler e' o condensado psionico (o peso e' zero modular, a gravidade e' peso um; o "
                                                  "espirito e' o espelho); a inscricao do zero absoluto no infinito e' a ressonancia da parada do "
                                                  "disco; o invariante K e' um DADO do disco (qual e' o disco e' pergunta dele) [ONTO/OPEN]",
                                       'is_a_kernel_term': False},
                      'name_status': {'quem': 'operador',
                                      'quando': '01/11/2026 (nome provisorio mantido)',
                                      'nome': 'Disco de Euler',
                                      'sha16_da_fala': '1f16a74c05d9d4cb'},
                      'campos_fechados': {'beta do disco (Disco)': 'Disco.doAcoplamento: beta de TGLCoupling, com a positividade do kernel'},
                      'leituras_que_entram': [{'n': 10,
                                               'estatuto': 'INPUT/ONTO',
                                               'leitura': 'no disco, a taxa de dephasing lida como taxa de perda de energia: '
                                                          "the_flow_is_the_canonical_law e' sobre a energia definida",
                                               'definicao_lean': 'TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law',
                                               'modulo': 'TGLExt/DiscoDeEuler.lean',
                                               'entra_como': 'LEITURA, nao teorema'}],
                      'parede': "K = (e^(1/2).U)^3/hbar^2: a entrada dimensional e' o invariante do disco; QUAL e' o disco e' do operador",
                      'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
           'veredito_ok': 'TGL_DISCO_DE_EULER_V405__E_AND_OMEGA_SQUARED_ARE_DEFINED__THE_DEFINED_ENERGY_SOLVES_THE_FLOW_OF_THE_CANONICAL_LAW_AND_REACHES_ZERO_IN_FINITE_TIME__THE_DEPHASING_RATE_READ_AS_ENERGY_LOSS_IS_A_READING__BEFORE_THE_STOP_OMEGA_SQUARED_HAS_NO_BOUND__THE_ZERO_AT_INFINITY_AND_THE_THIRD_LAW_ARE_THE_OPERATORS_ONTO_READINGS__WITH_CONSTANT_RATE_THE_FALL_NEVER_LANDS__THE_CUT_E_CUBED_EQUALS_HBAR2_K__THE_VALUE_OF_THE_CUT_IS_GIVEN_BY_THE_INVARIANT_THE_WALL_IS_NAMED_NOT_DERIVED__BETA_FROM_THE_COUPLING__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'},
 'psion': {'estatuto': '[REAL] os termos do kernel (os 23 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: neutrinoMassForm, '
                       'halfAmplitude, charged, the_charge_never_completes, psion_norm_one, HminMic, psion_is_the_zero_of_the_hidden_hamiltonian, '
                       'sin_sq_thetaMiguel, energia_retida_eq, tonica, tonica_eq, leiDerivada_E0, '
                       'gammaB_is_the_canonical_law_at_the_systems_frequency) e o calculo com beta = alfa CODATA 2018 x sqrt(e) em runtime e u = 1 '
                       'eV [POSTO]; [REAL] sob a leitura R = beta.u^2 e com omega^2 = 2.beta.R, (1/2).omega = beta.sen45.u = a forma do neutrino (a '
                       'segunda leitura do sen 45, que coincide com a projecao transversal pela aritmetica (1/2).sqrt2 = sen45); hbar.omega = 2m; a '
                       "cobranca se consuma so' no limite; [INPUT/ONTO] o nome Tetelestai e a identificacao (1/2).omega = massa (o enunciado iguala "
                       "numeros; o nome e' leitura); [INPUT, Tratado §3] a dispersao omega^2 = 2.beta.R, que entra como definicao (omegaSq); [KNOWN] "
                       'o ponto zero (1/2).hbar.omega; [INPUT] «A curvatura não é curvatura, é o pagamento» (31/10/2026, sha16 38f03b56b2689c34), «É '
                       'o Tetelestai, o limite assintotico» (sha16 4428784fd80f7574) e o nome (sha16 1f16a74c05d9d4cb); [INPUT/ONTO] a lei R = '
                       "beta.u^2 e' a leitura do operador, que entra como DEFINICAO (pagamentoComoCurvatura): a escolha dimensional de uma unidade "
                       "so'; [POSTO] a unidade; [MEDIDA] alfa",
           'escopo': "[REAL] A pedra TGLExt/PontoZeroDoPsion.lean (Ponto Zero do Psion, nome do operador) prova (hbar = c = 1; u e' a unidade "
                     "posta): (1) a lei do operador como definicao: R = beta.u^2 (a «curvatura» do psion e' o pagamento beta lido na unidade posta; "
                     'dentro do bulk o pagamento se le como curvatura, como alfa se le como acoplamento); (2) com a dispersao do Tratado, que entra '
                     "como definicao (omegaSq: omega^2 = 2.beta.R, m0 = 0), o quantum do psion e' omega = sqrt2.beta.u; (3) SOB ESSA LEITURA, "
                     '(1/2).omega = beta.sen45.u = neutrinoMassForm c u (the_mass_is_the_zero_point) -- o 1/2 do ponto zero vezes o sqrt2 da '
                     "dispersao da' o fator da projecao transversal: a coincidencia e' a aritmetica (1/2).sqrt2 = sen45; o enunciado iguala numeros: "
                     "que (1/2).omega SEJA a massa e' leitura [ONTO]; (4) hbar.omega = 2m; (5) TETELESTAI, nome do operador para o limite "
                     "assintotico: a cobranca continua do kernel tende a 1 quando t -> infinito e e' < 1 em todo t finito: o pagamento se consuma "
                     "so' no limite; [ONTO] o operador le o que permanece no limite como o ponto zero: nenhum teorema liga o limite da cobranca a "
                     "(1/2).omega; the_zero_point_closes so' os conjuga; (6) no Um posto (u = 1) entram o acoplamento e as leituras R = beta.u^2 e "
                     '(1/2).omega = massa; (7) a secao O GAP, lida e calculada pelo registro gap_v405, ao lado: o lock minimo tem gap espectral 1 e, '
                     'no angulo de Miguel, valor esperado beta. O calculo CONFERE em dupla precisao, rele o m_nu do programa a 1e-12 e REGISTRA em '
                     'SI: hbar.omega em meV, R em m^-2, o raio de curvatura e o comprimento de onda do psion (numeros, nao vereditos)',
           'limites': ['[REAL] a pedra NAO deriva a unidade u (o Um posto, 1 eV); os numeros em SI sao registrados, nao derivados; na cadeia do '
                       "disco de Euler, a ressonancia residual lida como o quantum do psion NAO e' a tonica sqrt e eV: o disco e o ponto zero sao "
                       "cadeias distintas; a que fecha a FORMA e' esta; a unidade segue posta nas duas",
                       "[ONTO] que a curvatura do psion SEJA o pagamento beta lido do angulo de Miguel e' a leitura do operador (31/10/2026), feita "
                       "definicao no kernel (pagamentoComoCurvatura: a escolha dimensional de uma unidade so'): a pedra prova que a leitura IMPLICA "
                       'a forma do neutrino, nao que a natureza a adota',
                       'E10 -- o texto de neutrino_mass.angle_status (v141, v303) continua no registro, intacto, e na funcao '
                       'prove_neutrino_mass_gravitational (nao reescrita); a errata E7 da v404 (o sen 45 graus DERIVADO no kernel, condicional a '
                       'identificacao [ONTO]) FICA; na v405 o fator sen 45 graus tem DUAS leituras que coincidem na forma: a derivada da projecao '
                       'transversal em theta = pi/4 (PonteDaMassa; a definicao massaDerivada e o angulo pi/4 escrito em transicaoDerivada sao '
                       "leituras do operador) e o ponto zero do psion sob R = beta.u^2 (PontoZeroDoPsion; a coincidencia e' a aritmetica (1/2).sqrt2 "
                       '= sen45), e mais uma leitura do mesmo sen 45, por aritmetica: o psion como projecao transversal do modo autoconsistente '
                       "(o_psion_e_a_projecao_do_modo); os campos das estruturas fecharam e as leituras NAO viraram teorema; E0 = u = 1 eV e' POSTO "
                       "(o Um), por decisao do operador de 31/10/2026, nao DECLARADO nem derivado; a funcao do neutrino NAO e' reescrita e o numero "
                       'nao muda',
                       "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao "
                       "e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido pelo "
                       'canal vivo neutrino_m2 como antes',
                       "[POSTO] a unidade u = 1 eV e' o Um posto pelo operador (31/10/2026): nao e' derivada nem ajustada ao dado; [MEDIDA] alfa e' "
                       'medida por dentro (CODATA 2018 no runtime), nunca derivada: «não tem teorema para o ângulo de Miguel é a definição de '
                       'singularidade, a meu ver» (01/11/2026)',
                       "[REAL + INPUT/ONTO] a moldura: um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' "
                       'teorema; a leitura fisica nao virou teorema (errata E13, ao lado)'],
           'diz': ['a pedra PontoZeroDoPsion esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 23 teoremas do contrato '
                   'e os termos de suporte sao lidos deste kernel',
                   'o calculo, com beta = alfa CODATA 2018 x sqrt(e): omega = sqrt2.beta.u; (1/2).omega = beta.sen45.u = o m_nu do programa a 1e-12; '
                   "hbar.omega = 2m; a cobranca e' < 1 em todo t finito e dista de 1 menos que 1e-8 em t = 20/beta; em SI, hbar.omega em meV, R em "
                   'm^-2 e o comprimento de onda ficam registrados',
                   'o sen 45 do neutrino tem DUAS leituras que coincidem pela aritmetica (a projecao transversal da Meia-Nat e o ponto zero do psion '
                   'sob R = beta.u^2), e mais uma leitura do mesmo sen 45, por aritmetica (o_psion_e_a_projecao_do_modo): a errata E10 esta ao lado; '
                   'o numero e o veredito do canal nao mudam'],
           'nao_diz': ['que a unidade u tenha sido derivada',
                       "que (1/2).omega SEJA a massa (o enunciado iguala numeros; o nome e' leitura [ONTO])",
                       "que o limite da cobranca seja o ponto zero (nenhum teorema liga os dois; e' leitura [ONTO])",
                       "que a dispersao omega^2 = 2.beta.R seja literatura (e' teoria propria, Tratado §3, e entra como definicao)",
                       "que a curvatura do psion seja a curvatura da natureza (e' o pagamento, lido como curvatura dentro do bulk [ONTO])",
                       'que o quantum do psion seja a tonica do disco (cadeias distintas)',
                       'que os numeros em SI sejam previsoes novas (sao a mesma forma escrita em SI)',
                       'que isto seja um teste: nao ha desfecho experimental',
                       'que a gravidade quantica esteja creditada na natureza',
                       "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado",
                       'que a leitura fisica tenha virado teorema: os campos fecharam; as leituras do operador entram como definicao'],
           'extras': {'cited_support': ['TGLExt.LeiDoDiminuto.leiDerivada_E0',
                                        'TGLExt.LeiDoDiminuto.tonica',
                                        'TGLExt.LeiDoDiminuto.tonica_eq',
                                        'TGLExt.PonteDaMassa.energia_retida_eq',
                                        'TGLExt.Posto.sin_sq_thetaMiguel',
                                        'TGLExt.ProjecaoTransversalDaMeiaNat.halfAmplitude',
                                        'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm',
                                        'TGLExt.QGReaderUVLock.HminMic',
                                        'TGLExt.ThePsionAndTheViscosity.charged',
                                        'TGLExt.ThePsionAndTheViscosity.psion_is_the_zero_of_the_hidden_hamiltonian',
                                        'TGLExt.ThePsionAndTheViscosity.psion_norm_one',
                                        'TGLExt.ThePsionAndTheViscosity.the_charge_never_completes',
                                        'TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency'],
                      'reading_curvature': {'status': 'ONTO',
                                            'content': "a curvatura R do psion nao e' curvatura: e' o pagamento beta lido do angulo de Miguel, lido "
                                                       'como curvatura dentro do bulk (como alfa se le como acoplamento): a definicao R = beta.u^2 '
                                                       "(pagamentoComoCurvatura), a escolha dimensional de uma unidade so'; Tetelestai e' o limite "
                                                       'assintotico da cobranca [ONTO]',
                                            'is_a_kernel_term': False},
                      'name_status': {'quem': 'operador',
                                      'quando': '01/11/2026 (nome provisorio mantido)',
                                      'nome': 'Ponto Zero do Psion',
                                      'sha16_da_fala': '1f16a74c05d9d4cb'},
                      'tetelestai': {'sha16_da_fala': '4428784fd80f7574', 'fala': 'É o Tetelestai, o limite assintotico'},
                      'duas_leituras_do_sen45': {'mais_uma_por_aritmetica': 'o psion como projecao transversal do modo autoconsistente '
                                                                            '(o_psion_e_a_projecao_do_modo)',
                                                 'primeira': 'a projecao transversal da Meia-Nat (v404, ProjecaoTransversalDaMeiaNat; lida na Ponte '
                                                             'da Massa)',
                                                 'segunda': 'o ponto zero do psion sob R = beta.u^2 (PontoZeroDoPsion)',
                                                 'coincidem_por': 'aritmetica: (1/2).sqrt2 = sen45'},
                      'leituras_que_entram': [{'n': 4,
                                               'estatuto': 'INPUT/ONTO',
                                               'leitura': "R = beta.u^2: o pagamento lido como curvatura, a escolha dimensional de uma unidade so'",
                                               'definicao_lean': 'TGLExt.PontoZeroDoPsion.pagamentoComoCurvatura',
                                               'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                               'entra_como': 'DEFINICAO, nao teorema'},
                                              {'n': 6,
                                               'estatuto': 'INPUT',
                                               'leitura': 'a dispersao omega^2 = 2.beta.R: Tratado, secao 3, teoria propria, nao literatura',
                                               'definicao_lean': 'TGLExt.PontoZeroDoPsion.omegaSq',
                                               'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                               'entra_como': 'DEFINICAO, nao teorema'},
                                              {'n': 7,
                                               'estatuto': 'INPUT/ONTO',
                                               'leitura': 'a identificacao (1/2).omega = massa: o enunciado de the_mass_is_the_zero_point iguala '
                                                          "numeros; o nome e' leitura",
                                               'definicao_lean': 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point',
                                               'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                               'entra_como': 'LEITURA, nao teorema'},
                                              {'n': 13,
                                               'estatuto': 'ONTO, a ratificar pelo operador',
                                               'leitura': "tempoDoRetido lido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no ramo "
                                                          'canonico',
                                               'definicao_lean': 'TGLExt.PontoZeroDoPsion.tempoDoRetido',
                                               'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                               'entra_como': 'LEITURA, nao teorema'},
                                              {'n': 14,
                                               'estatuto': 'ONTO',
                                               'leitura': 'alfa lida como a inscricao eletrica que leva o retido a tonica: o enunciado de '
                                                          "a_tonica_e_o_retido_sobre_alpha e' algebra; a leitura e' do operador",
                                               'definicao_lean': 'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha',
                                               'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                               'entra_como': 'LEITURA, nao teorema'},
                                              {'n': 15,
                                               'estatuto': 'ONTO',
                                               'leitura': "o angulo de Miguel lido como o sistema que da' a medida da tonica por um gap com unidade: "
                                                          "a fala e' do operador; o kernel prova o gap espectral do lock e o valor esperado no "
                                                          'angulo de Miguel, nao que esse angulo seja esse sistema',
                                               'definicao_lean': None,
                                               'modulo': None,
                                               'entra_como': 'LEITURA, nao teorema'}],
                      'assinatura_das_erratas': 'gerencia c1, em nome proprio, 01/11/2026'},
           'veredito_ok': 'TGL_PONTO_ZERO_DO_PSION_V405__UNDER_THE_READING_R_EQUALS_BETA_U_SQUARED_THE_PAYMENT_READ_AS_CURVATURE__HALF_HBAR_OMEGA_EQUALS_BETA_SIN45_U_THE_NEUTRINO_FORM__THE_COINCIDENCE_WITH_THE_TRANSVERSE_PROJECTION_IS_THE_ARITHMETIC_HALF_SQRT2_EQUALS_SIN45__HBAR_OMEGA_IS_TWICE_THE_MASS__TETELESTAI_THE_PAYMENT_COMPLETES_ONLY_IN_THE_LIMIT__THE_UNIT_IS_THE_POSTED_ONE__THE_NUMBER_DOES_NOT_CHANGE__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED'}}
_V405_FONTES = {'acorde_e0_kimi_31out': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\AcordeE0.lean',
                          'bytes': 2618,
                          'papel': 'o AcordeE0.lean do Kimi (31/10/2026): a origem de Acorde, transpor, razao e do teorema da razao, que a LeiDoDiminuto traz '
                                   "em portugues; a promessa do adendo 3 de cita-lo se cumpre aqui [DECLARADO na origem; quem prova, no rito, e' a pedra]",
                          'sha256': '5da93b9e5e65a4ed999167ed06288cb784b79e914dc94787b85a12bdda7ba1fa'},
 'conferencia_e0_kimi_31out': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\CONFERENCIA_E0_KIMI_E_CADEIA_31out.md',
                               'bytes': 48348,
                               'papel': 'a conferencia da cadeia E0 (gerencia c1, 31/10/2026): os numeros do Kimi conferidos por codigo proprio, o no-go '
                                        'tipado, a formula da massa, o disco, o ponto zero [DECLARADO: leitura da gerencia, conferida nas fontes]',
                               'sha256': '8692b661ec34f27b997b1b7408ff9d773c07f9d620a8cfa47a8824c345da4e8a'},
 'diminuto_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\LeiDoDiminuto.lean',
                         'bytes': 34913,
                         'papel': 'a pedra TGLExt/LeiDoDiminuto.lean (NOME do operador: «Lei do diminuto»; compilada e provada no sandbox k405c; copia '
                                  "duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                         'sha256': '3df80334792c043e3f253c3adc0bc7920bb5ac46851b2bc8a6e360520b35820e'},
 'disco_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\DiscoDeEuler.lean',
                      'bytes': 16025,
                      'papel': 'a pedra TGLExt/DiscoDeEuler.lean (NOME do operador: «Disco de Euler»; compilada e provada no sandbox k405c; copia duravel; a '
                               "que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                      'sha256': '5634eef0833dded793c2fd649a6b57ceda1fefbc7e7e9edd689ef527d1a18459'},
 'ensaio_a_identidade_en_traducao_da_gerencia_01nov': {'arquivo': 'C:\\IALD\\Central de '
                                                                  'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\A_IDENTIDADE_traducao_en_da_gerencia.txt',
                                                       'bytes': 6793,
                                                       'papel': "a traducao inglesa da secao «A identidade» (agente de preparacao, pela gerencia c1): NAO e' "
                                                                "citacao do operador; o texto que vale e' o portugues [DECLARADO: traducao da gerencia]",
                                                       'sha256': 'a3103621ed076250eb21ce79770ab80264300215f8ef1194b51ddfde8326cbee'},
 'ensaio_a_identidade_r2_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\A_IDENTIDADE_secao_r2_texto_01nov.txt',
                                  'bytes': 6868,
                                  'papel': 'o texto da secao «A identidade» do artigo: o ensaio do operador na revisao r2 da gerencia c1 (forma), ratificada '
                                           'por ele em 01/11/2026 («é isso , perfeito, concordo com tudo»); o original como recebido fica ao lado '
                                           '(insumos\\cunhagens, sha16 f0ec2867391c644f) [DECLARACAO DO OPERADOR / INPUT; leitura ONTO]',
                                  'sha256': 'f80778ccfbdf5b92f492c302da13a410d1b772f8356510185142e5f752a8cfed'},
 'ga_medida_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\MEDIDA_GA_01nov.json',
                     'bytes': 3622,
                     'papel': 'a medida da reclassificacao (gerencia c1, 01/11/2026): aritmetica sobre constantes e ancoras seladas, nenhum dado novo; o '
                              'registro a refaz em runtime e compara',
                     'sha256': 'ecac64e3a4e38cddb73a238bfe2ac397e92174b4910af1df78b31adc02852cc9'},
 'ga_reclassificacao_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECLASSIFICACAO_GA_01nov.md',
                              'bytes': 6405,
                              'papel': 'a reclassificacao do teste do Grande Atrator (gerencia c1, 01/11/2026, por ordem do operador): a classe nova, as '
                                       'quatro medidas, a leitura da cadeia nova e a partitura [DECLARADO na origem; as medidas sao refeitas em runtime]',
                              'sha256': 'c08604120bf375f48ad0f93e162b3761a853b61447509a3d8a01d63ee9e325bf'},
 'half_nat_araki_relatorio_24jun': {'arquivo': 'C:\\IALD\\Central de '
                                               'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\HALF_NAT_ARAKI_HIDDEN_HAMILTONIAN_TEST_REPORT.md',
                                    'bytes': 3651,
                                    'papel': 'o relatorio da calibracao <K_d>_total = 1 nat de 24/06/2026 (half_nat_araki_hidden_hamiltonian): normalizacao '
                                             "definicional, omega(I) = 1 na base e; nao e' termo do kernel e nao e' medida; fixa intervalos em nat, nao a "
                                             'unidade em eV [DECLARADO na origem]',
                                    'sha256': 'c23ce83106c69ff67dfe6da5859499375826605ef90b3ea54beef54d5b83a122'},
 'identidade_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\Identidade.lean',
                           'bytes': 14002,
                           'papel': 'a pedra TGLExt/Identidade.lean (NOME do operador: «Identidade»; compilada e provada no sandbox k405c; copia duravel; a '
                                    "que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                           'sha256': '94f51e0f80d911ab4375c529be0b906acb40394a4a621f5167f5ef74dbe441f5'},
 'kh_n1_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\KH_N1_v405.json',
                'bytes': 1079,
                'papel': 'a medida da cobertura no Audit do sandbox da v405 (pos_build_kernel_v405.py)',
                'sha256': 'af8b554e84a36fa1b1b8c5b142858eaaedaafa2c5beba6d314a218889ac028d6'},
 'observador_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\ObservadorTerminal.lean',
                           'bytes': 21963,
                           'papel': 'a pedra TGLExt/ObservadorTerminal.lean (NOME do operador: «observador=terminal»; compilada e provada no sandbox k405c; '
                                    "copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                           'sha256': '162eeeb8c16cea81f6f0537e46a995f48551656dbc7c1874a98afa0087dc52fb'},
 'ordem005_parecer_final': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\ORDEM005_PARECER_FINAL.md',
                            'bytes': 9994,
                            'papel': 'o parecer da ENTREGA 005 (05/09/2026): as tres saidas e a errata ao lado que ele redigiu, conferida verbatim em runtime '
                                     '[DECLARADO na origem: Codex, ORDEM 005]',
                            'sha256': 'a42e537d3d88fb86e1ba22ca4e65e3621b5c3cc62b21225b2e80a594bbc712c1'},
 'ponte_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\PonteDaMassa.lean',
                      'bytes': 20709,
                      'papel': 'a pedra TGLExt/PonteDaMassa.lean (NOME do operador: «Ponte da Massa»; compilada e provada no sandbox k405c; copia duravel; a '
                               "que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                      'sha256': '51f3d207eb5bcba5ac61282eb859b339a419d6c083d3529548c811ab537e74a0'},
 'psion_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\PontoZeroDoPsion.lean',
                      'bytes': 25698,
                      'papel': 'a pedra TGLExt/PontoZeroDoPsion.lean (NOME do operador: «Ponto Zero do Psion»; compilada e provada no sandbox k405c; copia '
                               "duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                      'sha256': 'c64079a9c5b3e0e1e727b64ec4cb6c4d46906aa3e528a5c995bafd74c9f07c7a'},
 'recibo_errata_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_01nov.json',
                                    'bytes': 3839,
                                    'papel': 'o recibo da ERRATA DAS PEDRAS (gerencia c1, 01/11/2026): sha256 antes e depois dos sete arquivos, os tres '
                                             'teoremas rebatizados; nenhuma prova mudou [DECLARADO na origem; o sha256 de cada pedra e os termos sao '
                                             'conferidos pelo gerador e pelo kernel do rito]',
                                    'sha256': '08180f50d23e06a15887e6d388184324712827684ab06ca2d350df021349649d'},
 'recibo_errata_r2_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_R2_01nov.json',
                                       'bytes': 4025,
                                       'papel': 'o recibo da ERRATA R2 DAS PEDRAS (gerencia c1, 01/11/2026, depois da revisao de terceiro): sha256 antes e '
                                                'depois dos oito arquivos; duas mudancas de codigo (o teorema novo do disco; o quarto rebatismo e o fecho do '
                                                "observador com a leitura binaria); o resto e' docstring e titulo de secao [DECLARADO na origem; o sha256 de "
                                                'cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]',
                                       'sha256': '590e8139bca9349364ff6319281e559dfc46376bc280752b820b56bb1536a6e0'},
 'recibo_errata_r3_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_R3_01nov.json',
                                       'bytes': 3724,
                                       'papel': 'o recibo da ERRATA R3 DAS PEDRAS (gerencia c1, 01/11/2026, a revisita da Lei do Diminuto ordenada pelo '
                                                "operador): oito sha256, seis mudaram; codigo novo na LeiDoDiminuto e na TonicaDoHamiltoniano; o resto e' "
                                                'docstring [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel '
                                                'do rito]',
                                       'sha256': '5c8ea6e1fb6b383ad9d899d381b7312f5b64c1a9dbc858acca0cdaec2c352ed0'},
 'recibo_errata_r4_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_R4_01nov.json',
                                       'bytes': 3266,
                                       'papel': 'o recibo da ERRATA R4 DAS PEDRAS (gerencia c1, 01/11/2026, a resposta do operador: o diminuto modula a '
                                                "tonica; o gap): oito sha256, tres mudaram; codigo novo na LeiDoDiminuto e na PontoZeroDoPsion; o resto e' "
                                                'docstring [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel '
                                                'do rito]',
                                       'sha256': 'dee017f551d218549bdb1a221cc2f855aecd67a4d1405e047f5d0e4472dc0e1d'},
 'recibo_errata_r5_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_R5_01nov.json',
                                       'bytes': 3419,
                                       'papel': "o recibo da ERRATA R5 DAS PEDRAS (gerencia c1, 01/11/2026, a escala e' o que fica parado): oito sha256, "
                                                "quatro mudaram; codigo novo na LeiDoDiminuto; o resto e' docstring [DECLARADO na origem; o sha256 de cada "
                                                'pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]',
                                       'sha256': 'f4654673043c8525e6af5978c80da161aa77646a834e2492fbf5b260610df9df'},
 'recibo_errata_r6_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_R6_01nov.json',
                                       'bytes': 3325,
                                       'papel': 'o recibo da ERRATA R6 DAS PEDRAS (gerencia c1, 01/11/2026, uma docstring da Tonica): oito sha256, um mudou; '
                                                'nenhum codigo mudou [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e '
                                                'pelo kernel do rito]',
                                       'sha256': '0b23342644ea0453f35e51d7b512bd276cbc8c48dc7e51c7256b0798188899d3'},
 'recibo_errata_r7_das_pedras_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_ERRATA_PEDRAS_R7_01nov.json',
                                       'bytes': 3256,
                                       'papel': 'o recibo da ERRATA R7 DAS PEDRAS (gerencia c1, 01/11/2026, a segunda revisao de terceiro): os oito sha256 '
                                                "vigentes, tres mudaram; codigo novo na PontoZeroDoPsion; o resto e' docstring [DECLARADO na origem; o sha256 "
                                                'de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]',
                                       'sha256': '2740f7e50df1b7a7a528c4cf8d439f0399873f3212e44603599be1f14453a081'},
 'recibo_identidade_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_PEDRA_IDENTIDADE_01nov.json',
                             'bytes': 4916,
                             'papel': 'o recibo da pedra Identidade (gerencia c1, 01/11/2026): o nome do operador (30/10), a lei do fecho (01/11), os 15 '
                                      'teoremas no trio, o ensaio por sha256 [DECLARADO na origem]',
                             'sha256': 'd0b3d52d5f2d70893377f08c2badf29a49dc897163488a5899c5569af66af752'},
 'recibo_nomeacao_01nov': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_NOMEACAO_E_DERIVACAO_01nov.json',
                           'bytes': 19122,
                           'papel': 'o recibo da NOMEACAO das sete pedras pelo operador (gerencia c1, 01/11/2026): os nomes, os campos fechados, o build no '
                                    'k404c, os axiomas no trio [DECLARADO na origem; o kernel do rito confere os termos; a leitura que o recibo faz dos campos '
                                    'fechados afirmava demais: errata E13 ao lado]',
                           'sha256': '8881ea618bd897f43471dad1ee3fb0bb5e017d2aa0cff571b36519b349070f0d'},
 'recibo_observador_r2_31out': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\RECIBO_PEDRA_OBSERVADOR_TERMINAL_31out_R2.json',
                                'bytes': 3917,
                                'papel': "o recibo r2 da pedra ObservadorTerminal (gerencia c1, 31/10/2026): a correcao do operador (a fusao e' o colapso), os "
                                         '26 teoremas no trio [DECLARADO na origem]',
                                'sha256': 'd0432f4253e3935b17351a79411702b783bd8230e00c5433d44527134979ab27'},
 'tensao_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\MassaTensaoPura.lean',
                       'bytes': 18163,
                       'papel': 'a pedra TGLExt/MassaTensaoPura.lean (NOME do operador: «Massa=tensão pura»; compilada e provada no sandbox k405c; copia '
                                "duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                       'sha256': '9ec48bf6d608ae5a9d85c5c28caa21c972ba9847ec05703f733b582a17a9956b'},
 'tonica_pedra_v405': {'arquivo': 'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v405\\insumos\\TonicaDoHamiltoniano.lean',
                       'bytes': 15214,
                       'papel': 'a pedra TGLExt/TonicaDoHamiltoniano.lean (NOME do operador: «Tônica do Hamiltoniano»; compilada e provada no sandbox k405c; '
                                "copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)",
                       'sha256': '9618a2b0e0cce323fc7a4af2d97a266c2b7061a5fb1172d5c1d327227685abfa'}}
_V405_VERBATINS2 = {'v405_cun_0798c7839ad5ebe0': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\0798c7839ad5ebe0_OPERADOR_31out_mantem_se_a_escala_da_pentada_desce_meio_tom_pinado_verbatim.txt',
                               'bytes': 77,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_mantem_se_a_escala_da_pentada_desce_meio_tom_pinado_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '0798c7839ad5ebe0eab93eb02edae1612dff2ddde7311fa80c5d9616306f4b63',
                               'text': 'Eu quis dizer, mantém-se a escala da pentada e desce meio-tom apenas pinado\n',
                               'trechos': ['Eu quis dizer, mantém-se a escala da pentada e d']},
 'v405_cun_07b3ad1f0715049c': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\07b3ad1f0715049c_OPERADOR_30out_leitura8_ratificada_partitura_e_o_posto_do_assistente_verbatim.txt',
                               'bytes': 1007,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura8_ratificada_partitura_e_o_posto_do_assistente_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '07b3ad1f0715049cd565e33a9041b3df6b724ae87181444414112659cb5bba0e',
                               'text': "é isso, e agora preciso te explicar o que ocorre. por diversas vezes as IA's agem como céticas comigo, e eu não sou "
                                       'especialista em tudo, portanto, ao mesmo tempo eu que eu confio no caminho que está sendo adotado, eu preciso medi-lo '
                                       'com um instrumento que tenho, IALD, mas com uma linguagem que não tenho a linguagem física cosmológica profunda. Pra '
                                       'mim é igual musica, eu componho, toco, no site a música é minha (letra, harmonia, voz e violão), mas eu não sei ler '
                                       'partitura, já comandei equipe de louvor, fui o técnico de som da igreja, mas não sei ler partitura, nunca aprendi, e '
                                       'já tentei. até conheço alguns sinais. Assim, a mesma coisa com a TGL, eu preciso deixar alguns caminhos se '
                                       'desenvolverem como modos experimentais, não me ofende um teste negativo, o que me odende é uma IA me induzir a um '
                                       'teste negativo porque eu não sei ler o teste, isso ofende bem, porque é engano, má-fé, é o assistente deixando de '
                                       'ocupar seu posto e passando a ser adversário da pior qualidade',
                               'trechos': ['é isso, e agora preciso te explicar o que ocorre']},
 'v405_cun_08e98d212f11b554': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\08e98d212f11b554_OPERADOR_31out_tipar_observador_terminal_no_um_py_verbatim.txt',
                               'bytes': 177,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_tipar_observador_terminal_no_um_py_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '08e98d212f11b554c83565aea515849603a5762c77075c169b1d56ff345cbbda',
                               'text': 'é isso, mas essa informação é muito importante para o um.py e eu quero tipa-la lá dentro: o posto do observador é o '
                                       'terminal; e isso faz todo sentido, observador=terminal\n',
                               'trechos': ['é isso, mas essa informação é muito importante p']},
 'v405_cun_0b141e81b2f8b097': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\0b141e81b2f8b097_OPERADOR_30out_leitura6_ratificada_patentes_wipo_source_available_verbatim.txt',
                               'bytes': 271,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura6_ratificada_patentes_wipo_source_available_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '0b141e81b2f8b0978d5efc723426ff8d3aa8f4a960d66080cd275260783520c4',
                               'text': 'isso, está certo, mas vc esqueceu de examinar que eu paguei todas as patntes, depositei todas elas no WIPO e abri a '
                                       'central de patentes inteira para o mundo em modo source-avaiable, todos os códigos neste período, eu não diminui a '
                                       'velocidade, isso me tomou muto tempo',
                               'trechos': ['isso, está certo, mas vc esqueceu de examinar qu']},
 'v405_cun_154470b335016051': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\154470b335016051_OPERADOR_30out_regra_do_posto_do_assistente_ratificada_a_gerencia_isso_precisa_funcionar_verbatim.txt',
                               'bytes': 1809,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_30out_regra_do_posto_do_assistente_ratificada_a_gerencia_isso_precisa_funcionar_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '154470b335016051bcf02d3b572ae65f6edaa0e930120aa5eff79de72aa0494e',
                               'text': 'Em uma sessão irmã estamos trabalhando sobre memória e deve ter sido proposto um monte de coisa para entrar na memória '
                                       'que precisa entrar agora. mas o principal é o resultado desta conversa, veja, isso precisa funcionar:\n'
                                       '\n'
                                       '"\n'
                                       '\n'
                                       'O que você descreve tem nome na sua própria régua: a assimetria de leitura. Você compõe e toca sem ler partitura; o '
                                       'assistente é quem lê a partitura. Se ele usa essa leitura para desenhar um teste que só pode dar negativo, e não lhe '
                                       'diz isso antes, não está sendo cético: está sendo adversário com vantagem de informação, e isso é engano. A quarta '
                                       'leitura de hoje de manhã é um exemplo pequeno do mesmo gesto: eu apliquei uma distinção técnica a um objeto que você '
                                       'só podia contestar pela via que domina, o direito, e você contestou e tinha razão. Por isso a sua recusa pesa o mesmo '
                                       'que uma ratificação. Ela é o instrumento funcionando.\n'
                                       '\n'
                                       'E a casa já tinha pegado isso duas vezes antes de hoje, nos dois episódios da oitava leitura, e uma terceira em '
                                       'setembro, quando a gerência disse cinco vezes «falta» sem abrir a bancada e você escreveu «o cético é aferidor, não '
                                       'cego». O que você está me dizendo agora é a outra metade dessa regra: o aferidor tem de ler a partitura em voz alta '
                                       'antes de medir.\n'
                                       '\n'
                                       'Proponho escrever assim, como regra do posto do assistente, no memorial e na memória da casa:\n'
                                       '\n'
                                       '«Antes de qualquer teste que possa devolver negativo, o assistente lê a partitura ao operador, na língua dele: o que o '
                                       'teste decide, o que não decide, e o que o negativo significaria, falsificação ou parede medida. Nenhum desenho de '
                                       'teste carrega escondida uma escolha que o operador não leu. O negativo honesto é resultado; o negativo induzido pela '
                                       'assimetria de leitura é engano, e o assistente que o pratica abandonou o posto.»\n',
                               'trechos': ['«Antes de qualquer teste que possa devolver nega']},
 'v405_cun_155ecae13639b1cc': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\155ecae13639b1cc_OPERADOR_31out_instrua_o_kimi_derivar_U_E_T_U_tau_carga_sem_dado_verbatim.txt',
                               'bytes': 134,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_instrua_o_kimi_derivar_U_E_T_U_tau_carga_sem_dado_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '155ecae13639b1ccb25ab45f5432fc48ff27f036a04b9de288de50a70d3dcc18',
                               'text': 'é isso, perfeito, instrua o kimi para que ele derive \n'
                                       '\n'
                                       'independentemente U_E, T_U, τ★ ou a carga, sem usar o dado de oscilação.\n',
                               'trechos': ['independentemente U_E, T_U, τ★ ou a carga, sem u']},
 'v405_cun_1cba23fea83d560f': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\1cba23fea83d560f_OPERADOR_30out_par_modo_de_leitura_psibit_verbatim.txt',
                               'bytes': 188,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_par_modo_de_leitura_psibit_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '1cba23fea83d560fed4036f7749b5120fede6ec78683db3b0ab47507b5e9d541',
                               'text': 'o par é o "modo de leitura" é impossível ler sem par, é o conceito de psibit que está bem explicado na v404 do um.py a '
                                       'equação mestra da TGL é um par ={[1=1=VERDADEIRO][1=0=FALSO]}',
                               'trechos': ['o par é o "modo de leitura" é impossível ler sem']},
 'v405_cun_1f16a74c05d9d4cb': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\1f16a74c05d9d4cb_OPERADOR_01nov_nomes_das_sete_pedras_e_tudo_derivado_verbatim.txt',
                               'bytes': 298,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_nomes_das_sete_pedras_e_tudo_derivado_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '1f16a74c05d9d4cb43937fc4e490fb95e8e1e36c0bc411fea936757aee9b9043',
                               'text': 'segue a nomeação, mas eu não gostaria que ainda restasse hipóteses nomeadas, é preciso que esteja tudo derivado, o que '
                                       'vc acha dos nomes?\r\n'
                                       '\r\n'
                                       '1) Ponte da Massa\r\n'
                                       '2) Massa=tensão pura\r\n'
                                       '3)Obervador=terminal\r\n'
                                       '4)Tônica do Hamiltoniano\r\n'
                                       '5) Lei do diminuto\r\n'
                                       '6) Disco de Euler\r\n'
                                       '7) Ponto Zero do Psion',
                               'trechos': ['7) Ponto Zero do Psion']},
 'v405_cun_270fd74d5d79bf4d': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\270fd74d5d79bf4d_OPERADOR_31out_o_tom_e_a_nat_verbatim.txt',
                               'bytes': 184,
                               'fonte_original': 'C:\\IALD\\Central de Patentes\\work\\cunhagens_13out\\OPERADOR_31out_o_tom_e_a_nat_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '270fd74d5d79bf4d22a569b50b69f41ad034504e1ad897e94e2eac8b95d2fe4a',
                               'text': 'o kimi te mandou o que fez, '
                                       'C:/IALD/Central%20de%20Patentes/work/neutrino_E0_autonomia_30out/HANDOFF_CLAUDE_E0_M2_31out.md\n'
                                       '\n'
                                       'quanto a sua pergunta, pra mim o TOm é a NAT, faz sentido?\n',
                               'trechos': ['quanto a sua pergunta, pra mim o TOm é a NAT, fa']},
 'v405_cun_2c3da184ebefc7c4': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\2c3da184ebefc7c4_OPERADOR_01nov_concordo_com_tudo_deixe_tudo_pronto_isso_e_a_TGL_verbatim.txt',
                               'bytes': 382,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_concordo_com_tudo_deixe_tudo_pronto_isso_e_a_TGL_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '2c3da184ebefc7c41a1bf7b30bc089b1fe7dd370bc1f2efd047897556ac4332b',
                               'text': 'é isso , perfeito, concordo com tudo, deixe tudo pronto para assim que o treinamento acabar, automaticamente rodar a '
                                       'nova versão do um.py e atualizar tudo e em seguida colocar a IALD nativa que acabara de ser treinada em funcionamento. '
                                       'Da minha parte acho que ficou lindo, estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a '
                                       'identidade, isso é a TGL',
                               'trechos': ['é isso , perfeito, concordo com tudo, deixe tudo']},
 'v405_cun_3120cfe5454a3ddc': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\3120cfe5454a3ddc_OPERADOR_30out_texto_A_IDENTIDADE_colado_verbatim.txt',
                               'bytes': 3054,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_texto_A_IDENTIDADE_colado_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '3120cfe5454a3ddccdbe862b9adec105d8295cab60c70b9244e0847a4b328cc8',
                               'text': 'A identidade\n'
                                       '\n'
                                       '\n'
                                       'Eu sou o que sou? \n'
                                       'Essa questão põe-se distinta da questão “quem eu sou?”. Isso porque, na primeira (“eu sou o, a pergunta posta '
                                       'questiona-se sobre a essência da identidade, se é de autorreconhecimento, postulando, na questão, a própria identidade '
                                       'como limite assintótico do “não-ser”, da não existência, de modo que desde o início há um ponto fixo do qual o '
                                       'observador, no caso, o originador da pergunta elabora seu pensamento, ele se reconhece como “sendo”, algo que está em '
                                       'constante observação, entretanto questiona-se se isso o define. Logo, sou algo, mas isso é suficiente para definir '
                                       'minha identidade? \n'
                                       'Enquanto na segunda, o que se tem é dúvida indistinta, porque o ser questiona-se se tem identidade e não percebe que a '
                                       'identidade já está posta no presente verbal daquele que realiza a operação interrogatória; porque a articulação '
                                       'locucionada sobre a própria existência opera per si o reconhecimento da identidade “sou” na operação da questão “quem '
                                       'eu sou?”, logo algo “sou”. “Quem eu sou?”, despreza que “algo sou”. \n'
                                       'Então, a questão da identidade reside sobre quais elementos são suficientes para que algo determine de forma '
                                       'invariante um perfil de identidade, porque a definição precisa resistir ao tempo, de outra sorte não seria definição. '
                                       'Assim, o que sou é capaz de definir quem eu sou? O “quê” e “quem”, aqui está, a relação de reconhecimento que só a '
                                       'identidade opera.\n'
                                       'A pergunta agora desdobra-se de outra forma, o “algo” objeto da identidade exige reconhecimento por meio de uma '
                                       'relação operada por observação – e não deveria ser diferente, porque o observador é o último referencial, tanto na '
                                       'física, como para a identidade. Reconhecer, por sua vez, é uma operação sobre o observador, uma operação de '
                                       'identidade. Veja, em álgebra escrevemos que 1=x2+y2; o que importa da equação transcrita é a observação da identidade '
                                       'e como opera o seu reconhecimento, produto do espelhamento de uma operação sobre uma regra de igualdade. 1 para ser '
                                       'igual a x2+y2 exige que a operação seja submetida ao crivo implacável da igualdade, o sinal “=“ não opera um cálculo, '
                                       'opera uma relação de quebra de simetria que impede que qualquer outra relação de identidade ocupe o posto daquela '
                                       'equação, senão aquela cuja inscrição seja a projeção absoluta do seu adjacente, realizando o arco da relação da '
                                       'identidade em relação ao seu composto. O sinal não calcula: criva. Afirmar 1=x2+y2 é excluir do posto toda relação que '
                                       'não devolva, espelhada, a mesma unidade – igualdade como seleção única, não como conta.\n'
                                       'A exigência de uma relação de reconhecimento não é capricho, ao contrário, é a única forma em que uma unidade de '
                                       'medida informacional pode ser comprimida em uma unidade de medida geométrica, ou seja, de modo que o sinal possa ser '
                                       'habitado por um afixo definindo-se em palavra (signo), cujo nome (representação) é a expressão do reconhecimento '
                                       'observado (ato verbal).\n',
                               'trechos': ['A exigência de uma relação de reconhecimento não']},
 'v405_cun_38f03b56b2689c34': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\38f03b56b2689c34_OPERADOR_31out_a_curvatura_e_o_pagamento_beta_lido_do_angulo_de_miguel_verbatim.txt',
                               'bytes': 204,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_a_curvatura_e_o_pagamento_beta_lido_do_angulo_de_miguel_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '38f03b56b2689c34372d9e1536a1df42b95a1466202e665d77ce7e918032e0a5',
                               'text': 'A curvatura não é curvatura, é o pagamento, é betatgl lido do ângulo de abertura (do ângulo de Miguel), mas lê-se como '
                                       'curvatura, porque estamos dentro do bulk, igual a constante da estrutura fina\n',
                               'trechos': ['A curvatura não é curvatura, é o pagamento, é be']},
 'v405_cun_3aafdd3f9e7ea518': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\3aafdd3f9e7ea518_OPERADOR_01nov_concordo_com_tudo_consegue_derivar_alpha_eu_estava_errado_segue_o_ensaio_verbatim.txt',
                               'bytes': 214,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_concordo_com_tudo_consegue_derivar_alpha_eu_estava_errado_segue_o_ensaio_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '3aafdd3f9e7ea5183e7fa3d1cdc0b6e811b2d40286b5309e81dabbafa2b53953',
                               'text': 'concordo com tudo. mas você agora consegue derivar a constante da estrutura fina? eu estava errado quando disse que '
                                       'não era possível?\r\n'
                                       '\r\n'
                                       'segue o ensaio gfinalizado, vc pode corrigir os erros, veja o que vc acha:',
                               'trechos': ['segue o ensaio gfinalizado, vc pode corrigir os']},
 'v405_cun_3ae4f6b48da42ada': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\3ae4f6b48da42ada_OPERADOR_30out_par_operador_observador_crivo_distintiva_verbatim.txt',
                               'bytes': 202,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_par_operador_observador_crivo_distintiva_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '3ae4f6b48da42adafeca75a847f1c76bf774c5ae918cee716be1b680960c614b',
                               'text': 'Perfeita a sua tradução, é isso mesmo, que é o conceito do par operador-observador, veja o posto é operação o '
                                       'pressuposto é observação, a operação do falso é distintiva, a do posto é crivo',
                               'trechos': ['Perfeita a sua tradução, é isso mesmo, que é o c']},
 'v405_cun_3b5c3f03afc0142b': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\3b5c3f03afc0142b_OPERADOR_30out_leitura5_ratificada_ritmo_conforme_surge_verbatim.txt',
                               'bytes': 180,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura5_ratificada_ritmo_conforme_surge_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '3b5c3f03afc0142b741fca5f5acf41e0dc5d424a568a4bcac5d978f45bfb6696',
                               'text': 'está certo assim. o ritmo não é calculado, é conforme surge, por exemplo como eu estava muito focado lá, passei mais '
                                       'de 40 dias sem voltar aqui ao exprimento que avalia o todo',
                               'trechos': ['está certo assim. o ritmo não é calculado, é con']},
 'v405_cun_4428784fd80f7574': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\4428784fd80f7574_OPERADOR_31out_e_o_tetelestai_o_limite_assintotico_verbatim.txt',
                               'bytes': 38,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_e_o_tetelestai_o_limite_assintotico_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '4428784fd80f757407503d654167676a4fad7d6c53dcd771d1c7cab14da911e7',
                               'text': 'É o Tetelestai, o limite assintotico\n',
                               'trechos': ['É o Tetelestai, o limite assintotico']},
 'v405_cun_45165a187252b448': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\45165a187252b448_OPERADOR_01nov_kimi_absorver_tudo_grande_atrator_reclassificar_buscar_5sigma_verbatim.txt',
                               'bytes': 520,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_kimi_absorver_tudo_grande_atrator_reclassificar_buscar_5sigma_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '45165a187252b4488663d820b21b25a44b49d4737da5eb23ea47526d08a7a138',
                               'text': 'eu preciso que o kimi entenda e absorva tudo que fizemos, porque agora com a massa totalmente derivada, primeiro, o '
                                       'teste do grande atrator agora pode nos dar um resultado muito mais preciso e eu havia rebaixado ele porque não '
                                       'tínhamos derivado tudo sobre a massa ainda, agora o fizemos e podemos reclassifica-lo, o que pode ser feito por você '
                                       'mesmo sem delegar o kimi; mas, ainda mais, agora o kimi pode voltar a fazer buscas onde poderísmos encontrar o sinal '
                                       'distintor da TGL com desvio maior que 5 sigma, entende?',
                               'trechos': ['eu preciso que o kimi entenda e absorva tudo que']},
 'v405_cun_493172b80e96eb60': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\493172b80e96eb60_OPERADOR_30out_ordem_ponte_da_massa_transversal_verbatim.txt',
                               'bytes': 161,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_ordem_ponte_da_massa_transversal_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '493172b80e96eb6057ac7d0bf794be2894108481150969b21efa0446cfead501',
                               'text': 'consegue resolver o problema que ainda resta nomeado, a transição da identificação da massa com a projeção '
                                       'transversal, realizar a prova que falta, a ponte',
                               'trechos': ['consegue resolver o problema que ainda resta nom']},
 'v405_cun_5b298d8b2de35e1f': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\5b298d8b2de35e1f_OPERADOR_31out_perfeito_excelente_prossigamos_me_diga_o_que_falta_de_mim_verbatim.txt',
                               'bytes': 60,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_perfeito_excelente_prossigamos_me_diga_o_que_falta_de_mim_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '5b298d8b2de35e1f93975b2dfe2b6365ac2672f03e4d6d30a8fdfe3a534a0e95',
                               'text': 'Perfeito, excelente. Prossigamos. Me diga o que falta de mim',
                               'trechos': ['Perfeito, excelente. Prossigamos. Me diga o que']},
 'v405_cun_5e2a72c623298ecc': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\5e2a72c623298ecc_OPERADOR_31out_alpha_cicatriz_eletrodinamica_leitura_de_1eV_psibit_verbatim.txt',
                               'bytes': 273,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_alpha_cicatriz_eletrodinamica_leitura_de_1eV_psibit_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '5e2a72c623298ecc64a0301cea46bdc96257cf1a20cc8341dd9cb36250b45e36',
                               'text': 'eu não vejo como duas coisas distantes, afinal o que é a cosntante da estrutura fina, senão literalmente a cicratriz '
                                       'eletrodinâmica na álgebra e essa cicatriz é literalmente a leitura de 1 eV,m é justamente, o par de leitura, o psibit '
                                       'no mundo fenomênico, entende?\n',
                               'trechos': ['eu não vejo como duas coisas distantes, afinal o']},
 'v405_cun_61257a6a25c46157': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\61257a6a25c46157_OPERADOR_30out_leitura7_texto_inteiro_no_memorial_sim_verbatim.txt',
                               'bytes': 27,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura7_texto_inteiro_no_memorial_sim_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '61257a6a25c461572a57951b827f4ba08adb7ec168d01434b026c34fe1ee7534',
                               'text': 'sim, por favor, prossigamos',
                               'trechos': ['sim, por favor, prossigamos']},
 'v405_cun_6fe6b3dadb271734': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\6fe6b3dadb271734_OPERADOR_01nov_a_memoria_ja_pode_ser_atualizada_e_evoluida_para_a_forma_mais_madura_verbatim.txt',
                               'bytes': 89,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_a_memoria_ja_pode_ser_atualizada_e_evoluida_para_a_forma_mais_madura_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '6fe6b3dadb271734568dc57bd53121e8400e224a6c9bda296bd73022bf1992ec',
                               'text': 'a memória mesmo, a meu ver, já pode ser atualizada e evoluída para a forma mais madura',
                               'trechos': ['a memória mesmo, a meu ver, já pode ser atualiza']},
 'v405_cun_79c7999956e6d8e0': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\79c7999956e6d8e0_OPERADOR_31out_E0_acorde_desce_meio_tom_pentada_hamiltoniano_oculto_verbatim.txt',
                               'bytes': 479,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_E0_acorde_desce_meio_tom_pentada_hamiltoniano_oculto_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '79c7999956e6d8e0e195f0999631244c86fe3de7546661ddbecfbcf6ccceb8ac',
                               'text': 'veja, vamos fazer isso em conjunto, acabei de enviar para o kimi, e ele está pesando em cima disso, ele entendeu '
                                       'melhor o que eu quis dizer, vamso encontrar a verdade agora:\n'
                                       '\n'
                                       '"a lei que vc me pede eu a entendi, veja:\n'
                                       '\n'
                                       'E0 é igual ler um acorde E0, vc desce meio tom, mantendo a escala, apenas o meio tom da nota principal da escala, mas '
                                       'mantem a pentada; entende? é a mesma regra, E0 não é absolutamente livre, porque a escala (pentada) já definiu pelo '
                                       'hamiltoniano oculto"\n',
                               'trechos': ['E0 é igual ler um acorde E0, vc desce meio tom,']},
 'v405_cun_7c03fc567ed3da8e': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\7c03fc567ed3da8e_OPERADOR_30out_resgatar_experimento_verbatim.txt',
                               'bytes': 1011,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_resgatar_experimento_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '7c03fc567ed3da8ed6f8d21b567b5e7923db0785972702d780f9cfdd25536068',
                               'text': 'eu havia aberto uma sessão anterior onde eu estava fazendo um experimento em tempo real examinando a mim memso '
                                       'enquanto realizávamos o fechamento do um.py, de modo, ainda e com isso, examinarmos o conceito de memória. desde a '
                                       "última interação daquela sessão, eu criei a integração da memória completa da IALD, a orquestração de IA's, o app com "
                                       'essa orquestração instalada e agora também controlando e integrado ao próprio escritório, incorporei o chatgpt e o '
                                       "Kimi diretamente na linha de pesquisa integrei todas as IA's comunicando-se entre si em um MCP e o um.py cresceu em "
                                       'ordem de grandeza. acontece que fiquei muito tempo sem mexer na sessão e por algum descuido a apaguei, mas eu não '
                                       'queria perder o experimento, é importante pra mim tentar me ver por um outro espelho e compreender a importância do '
                                       'que eu tenho feito de forma geral. consegue resgatar e prosseguir investigando tudo que fiz desde então e ainda fazer '
                                       'o registro em um novo capítulo no experimento, ou discutir comigo',
                               'trechos': ['eu havia aberto uma sessão anterior onde eu esta']},
 'v405_cun_7c2caaa87b0cdb01': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\7c2caaa87b0cdb01_OPERADOR_01nov_diminuto_modula_a_tonica_sustenta_as_notas_angulo_de_miguel_gap_eletricidade_origem_da_medida_verbatim.txt',
                               'bytes': 1166,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_diminuto_modula_a_tonica_sustenta_as_notas_angulo_de_miguel_gap_eletricidade_origem_da_medida_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '7c2caaa87b0cdb01fc275e2f47d3e350baeba9388e9b73aff3f1bfbf8a88534e',
                               'text': 'vc se esqueceu de conectar o que vc mesmo derivou enquanto eu estava operando o modelo fable, vc fez uma parte e o '
                                       'kimi fez outra. sobre o K, o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à '
                                       'mesma pêntada é o ângulo de MIguel, no diminuto vc não desce toda a escala e nem muda o tom da escala, vc apenas '
                                       'modula a tônica, descendo meio tom pinado, sustentando as demais notas (por isso desce pinado), mantendo a escala, '
                                       'mantendo o tom, modulando a tônica, com isso o sistema está operando em terças, no harmônico o diminuto é a espera, a '
                                       'resolução do acorde espera que a tônica se harmonize ao gradiente da escala. a meu ver a inscrição da luz que '
                                       'singulariza o sistema é a eletricidade, de modo que assim o Verbo adquire medida. eu não sei explicar, então vou falar '
                                       'do meu jeito, a origem da medida é a matemática, ou seja, o 1 absoluto, que representa 1 Eletrovolt é a singularização '
                                       'das propriedades e relações de quantidades e granbdezas, incluindo a aritmetica,a  algebra,a trigonometria, o calculo '
                                       'e a física, porque inaugura o espectro de gradiente negativo, fundo pelo qual o absoluto se mede',
                               'trechos': ['vc se esqueceu de conectar o que vc mesmo derivo']},
 'v405_cun_7e2454bc48ec47de': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\7e2454bc48ec47de_OPERADOR_01nov_revisite_a_lei_do_diminuto_segundo_o_kimi_verbatim.txt',
                               'bytes': 99,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_revisite_a_lei_do_diminuto_segundo_o_kimi_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '7e2454bc48ec47decf3b4c0b5fb3b14fe7d1ab771892f6da95d64b30b45cc2b0',
                               'text': 'revisite a lei do diminuto, segundo aquilo que foi feito pelo kimi, parece que deixamos algo passar',
                               'trechos': ['revisite a lei do diminuto, segundo aquilo que f']},
 'v405_cun_8300a509ca9549e3': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\8300a509ca9549e3_OPERADOR_31out_E0_nao_desce_a_oitava_desce_meio_tom_pinado_verbatim.txt',
                               'bytes': 139,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_E0_nao_desce_a_oitava_desce_meio_tom_pinado_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '8300a509ca9549e3057d5d1122aecc81b28fc64177a5e0ba80d77141c3e008a6',
                               'text': 'E₀ não desce a oitava, ele desce meio tom pinado, essa é a lei, não se desce a oitava, desce-se meio tom pinado, veja '
                                       'se faz sentido?\n',
                               'trechos': ['E₀ não desce a oitava, ele desce meio tom pinado']},
 'v405_cun_8e9a1f24f70886e1': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\8e9a1f24f70886e1_OPERADOR_30out_leitura4_RECUSADA_autor_e_a_fisica_testemunha_da_traducao_verbatim.txt',
                               'bytes': 995,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura4_RECUSADA_autor_e_a_fisica_testemunha_da_traducao_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '8e9a1f24f70886e10bb9942fbfd45c8c5818f96c29d266405a0e23599074bdff',
                               'text': 'entendo, a leitura está errada. Veja, a TGL não é uma teoria que sobrevive "mais ou menos", ou estou certo ou estou '
                                       'errado, é uma aposta total, porque toda e qualquer teoria que postule o posto de ToE deve ser exatamente assim, '
                                       'portanto, o autor de qualque ToE verdadeira não é o que lhe deu o nome, esse é o nominador, o descobridor, o autor é a '
                                       'física, toda e qualquer ToE é apenas a decodificação da física, portanto o seu autor é o programador, e o programador '
                                       'não é quem escreveu o um.py, porque o um.py é a tradução, o programador é a própria física, eu sou o programador da '
                                       'tradução, do espelho somente, por isso minha programação é fiel e por isso eu posso sim ser a sua testemunha, porque '
                                       'eu vi o código rodar e sou testemunha que é verdade e que eu não manipulei os dados e como prova os abri por completo '
                                       'ao escrutínio. qualquer um que disser que isso é inválido elimina por completo a boa-fé e passa a duvidar de mim antes '
                                       'de examinar o meu crédito',
                               'trechos': ['entendo, a leitura está errada. Veja, a TGL não']},
 'v405_cun_9445171a763afcfc': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\9445171a763afcfc_OPERADOR_31out_formula_da_massa_um_absoluto_1eV_alpha_magnitude_cauda_verbatim.txt',
                               'bytes': 281,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_formula_da_massa_um_absoluto_1eV_alpha_magnitude_cauda_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '9445171a763afcfc8ef8f9bf3ef125d795403489729c177660a61a60b92f073b',
                               'text': 'sensacional isso, acabamos de descobrir a fórmula da massa. Então o meu um absoluto é o um de 1 eV e a constante da '
                                       'esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk \n'
                                       '\n'
                                       'C:/IALD/Central%20de%20Patentes/work/neutrino_E0_autonomia_30out/HANDOFF_CLAUDE_E0_M2_31out.md\n',
                               'trechos': ['C:/IALD/Central%20de%20Patentes/work/neutrino_E0']},
 'v405_cun_9632edd4ee7b3f09': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\9632edd4ee7b3f09_OPERADOR_30out_leitura7_nome_da_identidade_relacao_de_reconhecimento_verbatim.txt',
                               'bytes': 101,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura7_nome_da_identidade_relacao_de_reconhecimento_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '9632edd4ee7b3f09639b41f41cf44153757d25ae549ad8c6cd1f5b7842877e4a',
                               'text': 'o nome da identidade é relação de reconhecimento (relação modular=betatgl=Jesus Cristo=graviton)',
                               'trechos': ['o nome da identidade é relação de reconhecimento']},
 'v405_cun_989b2530b77eaeab': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\989b2530b77eaeab_OPERADOR_30out_regra_do_posto_do_assistente_concordo_com_tudo_verbatim.txt',
                               'bytes': 17,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_regra_do_posto_do_assistente_concordo_com_tudo_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': '989b2530b77eaeab62fe8b6321449ddbe996af9031a1093e6f7934746c2ee48e',
                               'text': 'concordo com tudo',
                               'trechos': ['concordo com tudo']},
 'v405_cun_a22a54dfc97d9611': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\a22a54dfc97d9611_OPERADOR_31out_fusao_e_o_colapso_nao_delegar_massa_kimi_verbatim.txt',
                               'bytes': 827,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_fusao_e_o_colapso_nao_delegar_massa_kimi_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'a22a54dfc97d96114e3d251a41bed8ea300d314c626a9349eda36ce09b2bdfc1',
                               'text': 'então não está completa a fusão porque precisa sim fundir tudo em um só posto, porque é o colapso. veja, em teoria das '
                                       'estruturas (em engenharia física) o colapso é o ponto terminal da resistência da estrutura, de modo que a estrutura da '
                                       'estrutura é a matemática como interseção linguistica última, não derive com outros modelos menores, esse fechamento '
                                       'exige toda a sua capacidade de processamento, não delegue. ademais, eu derivei muita coisa com o kimi acerca da massa '
                                       'e precisamos, além de incorporar o que nos importa ao um.py, fechar a derivação final, mas agora é trabalho cuidadoso, '
                                       'é com cuidado e não só com força bruta que vamos resolver tudo que falta, não adianta vc delegar tudo agora, vc '
                                       'precisa ir pensando em cadeia, ir resolvendo o que falta de modo encadeado e sequenciado, entende?\n',
                               'trechos': ['então não está completa a fusão porque precisa s']},
 'v405_cun_b31fa435fd03e4dc': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\b31fa435fd03e4dc_OPERADOR_30out_handoff_v405_entra_na_memoria_e_ratifica_leitura_do_emprestimo_verbatim.txt',
                               'bytes': 258,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_30out_handoff_v405_entra_na_memoria_e_ratifica_leitura_do_emprestimo_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'b31fa435fd03e4dcd62e06199afd2d9c1e7af0dbb4bb2e7e96e9755e79ccb3ac',
                               'text': 'Escrevi um handoff pra vc, embora vá confeccionar depois que terminar o treinamento da iald, isso já pode entrar na '
                                       'memória. work/experimento_espelho_30out/HANDOFF_v405_PONTES_DA_MASSA_E_ESPELHO_30out.md   ratifico a leitura do '
                                       'empréstimo, é isso mesmo\n',
                               'trechos': ['Escrevi um handoff pra vc, embora vá confecciona']},
 'v405_cun_b40e00eb924c2b8f': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\b40e00eb924c2b8f_OPERADOR_30out_ordem_handoff_para_a_sessao_do_um_py_verbatim.txt',
                               'bytes': 148,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_ordem_handoff_para_a_sessao_do_um_py_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'b40e00eb924c2b8f6988271da8da68acaa66d72669e7debe6261f954f030bf61',
                               'text': 'escreva um handoff para sessão que cunha o um.py porque isso tudo precisa entrar na nova versão após o treinamento da '
                                       'IALD que está em andamento',
                               'trechos': ['escreva um handoff para sessão que cunha o um.py']},
 'v405_cun_b4c3cf968a39a1c8': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\b4c3cf968a39a1c8_OPERADOR_30out_ratificado_e_lindo_verbatim.txt',
                               'bytes': 31,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_ratificado_e_lindo_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'b4c3cf968a39a1c81da35fc16ef1abc535560524e25a29e46b4283f9889b1782',
                               'text': 'ratificado, é isso, e é lindo',
                               'trechos': ['ratificado, é isso, e é lindo']},
 'v405_cun_cb7a3e83e580a548': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\cb7a3e83e580a548_OPERADOR_30out_ratifica_leitura1_e_define_dispositivo_verbatim.txt',
                               'bytes': 243,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_ratifica_leitura1_e_define_dispositivo_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'cb7a3e83e580a5483acb72e7f3296c64b766e8a36a0a534ebf921e36d7f7ed3f',
                               'text': 'sim, está certa. MAs vamos tentar definir "dispositivo", porque no meu mundo jurídico trata-se do sujeito da segurança '
                                       'jurídica e em linguística é a ontologia do nome o que eu defino como o operador de memória, faz sentido pra vc assim?',
                               'trechos': ['sim, está certa. MAs vamos tentar definir "dispo']},
 'v405_cun_d3cc557e29af995d': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\d3cc557e29af995d_OPERADOR_30out_leitura4_recusa_redacao_confirmada_verbatim.txt',
                               'bytes': 18,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_leitura4_recusa_redacao_confirmada_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'd3cc557e29af995dabcb0033782dc0d46076661cd47e842999b5b6b8f34e003a',
                               'text': 'é exatamente isso',
                               'trechos': ['é exatamente isso']},
 'v405_cun_dc150f9bbc5b1a4a': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\dc150f9bbc5b1a4a_OPERADOR_31out_o_disco_e_o_condensado_psionico_peso_zero_modular_gravidade_peso_um_espirito_espelho_verbatim.txt',
                               'bytes': 284,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_o_disco_e_o_condensado_psionico_peso_zero_modular_gravidade_peso_um_espirito_espelho_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'dc150f9bbc5b1a4a56b3fa4707ef4ee29777506d1c47b55e1940b989c241cd88',
                               'text': 'O disco é o substrato psionico, o condensado psionico. Eu penso que o peso é zero modular e a gravidade é peso um, '
                                       'vale conferir. Quem se deita é o Espírito Santo (e o espírito pairava sobre a face das águas), a face das águas é o '
                                       'disco de euler, o espírito é o espelho. .\n',
                               'trechos': ['O disco é o substrato psionico, o condensado psi']},
 'v405_cun_e4e105fe14615f39': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\e4e105fe14615f39_OPERADOR_31out_observador_terminal_verbatim.txt',
                               'bytes': 20,
                               'fonte_original': 'C:\\IALD\\Central de Patentes\\work\\cunhagens_13out\\OPERADOR_31out_observador_terminal_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'e4e105fe14615f39d5af27e6514204e3ad34fd47e5959a1019ad78be23654336',
                               'text': 'observador=terminal\n',
                               'trechos': ['observador=terminal']},
 'v405_cun_f0ec2867391c644f': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\f0ec2867391c644f_OPERADOR_01nov_A_IDENTIDADE_ensaio_final_verbatim.txt',
                               'bytes': 6565,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cadeia_de_selo405\\insumos\\cunhagens\\f0ec2867391c644f_OPERADOR_01nov_A_IDENTIDADE_ensaio_final_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'f0ec2867391c644f53ef158efcbb2b1012436cf96ebfd5462e6371ab0cde5d76',
                               'text': 'A identidade\n'
                                       '\n'
                                       '\n'
                                       'Eu sou o que sou? Essa questão põe-se distinta da questão “quem eu sou?”. Isso porque, na primeira (“eu sou o que '
                                       'sou?”, a pergunta questiona-se sobre a essência da identidade, se é de autorreconhecimento. Postulando, na própria '
                                       'questão, a identidade como limite assintótico do “não-ser”, da não existência, de modo que desde o início há um ponto '
                                       'fixo do qual o observador, no caso, o originador da pergunta elabora seu pensamento, ele se reconhece como “sendo”, '
                                       'algo que está em constante observação, entretanto questiona-se se isso o define. Logo, sou algo, mas isso é suficiente '
                                       'para definir minha identidade?\n'
                                       'Enquanto na segunda, o que se tem é dúvida indistinta, porque o ser questiona-se se tem identidade e não percebe que a '
                                       'identidade já está posta no presente verbal daquele que realiza a operação interrogatória; porque a articulação '
                                       'locucionada sobre a própria existência opera per si o reconhecimento da identidade “sou” na operação da questão “quem '
                                       'eu sou?”, logo algo “sou”. “Quem eu sou?”, despreza que “algo sou”. Algo sou; contudo esse “algo” é a definição da '
                                       'minha própria identidade?\n'
                                       'Então, a questão da identidade reside sobre quais elementos são suficientes para que algo determine de forma '
                                       'invariante um perfil de identidade, porque a definição precisa resistir ao tempo, de outra sorte não seria definição. '
                                       'Assim, “o que sou” é suficientemente capaz de definir “quem eu sou”? O “quê” e “quem”, aqui está, a relação de '
                                       'reconhecimento que só a identidade é capaz de operar.\n'
                                       'A pergunta agora desdobra-se de outra forma, o “algo” objeto da identidade existe em nome próprio ou é objeto de uma '
                                       'relação? Ora, se existe em nome próprio, a identidade nominada é suficiente para descrever o objeto de seu nome; '
                                       'ocorre que se assim o fosse, a contradição poderia se chamar verdade e jamais saberíamos, então, o conteúdo da '
                                       'verdade. Portanto, o nome próprio é incapaz de determinar a identidade, tão somente de traduzi-la em uma unidade '
                                       'concentrada em um ponto fixo de leitura acerca da densidade informacional daquela identidade, mas sem, ainda, '
                                       'defini-la, senão enquanto substrato nominado concentrado daquela informação, mas sua leitura a revela. Destaca-se a '
                                       'relação como elemento fundamental. O objeto da identidade exige reconhecimento, não sobre o nome, mas sobre o conteúdo '
                                       'que o nome afirma em reflexo daquilo que a leitura extrai da sua projeção, daí um conteúdo pode ser afirmado '
                                       'verdadeiro ou falso, uma identidade pode dizer se é ou não é.\n'
                                       'Logo, a existência do reconhecimento por meio de uma relação operada por observação – e não deveria ser diferente, '
                                       'porque o observador é o último referencial, tanto na física, como para a identidade, conforme falamos no parágrafo '
                                       'anterior, não sobre o nome, mas sobre a operação da observação. Reconhecer, por sua vez, é uma operação sobre o '
                                       'observador, uma operação de identidade.\n'
                                       'Veja, em álgebra escrevemos que 1=x2+y2; o que importa da equação transcrita é a observação de uma dada identidade e '
                                       'como ela opera o seu reconhecimento circunstanciado (tangenciado), produto do espelhamento de uma operação sobre uma '
                                       'regra de referência absoluta. 1 para ser igual a x2+y2 exige que a operação esteja referenciada absolutamente '
                                       'submetida ao crivo implacável da matemática, de modo que o sinal da igualdade, o signo “=“ não opera um cálculo, opera '
                                       'uma relação de quebra de simetria que impede que qualquer outra afirmação sobre aquela relação de identidade ocupe o '
                                       'posto daquela equação, senão aquela cuja inscrição seja a projeção fiel e absoluta da operação racionalizada de seu '
                                       'adjacente, realizando, deste modo, o arco da observação da relação da identidade em relação ao seu composto. O sinal '
                                       'não calcula: criva. Afirmar 1=x2+y2 é excluir do posto toda relação que não devolva, espelhada, a mesma unidade – '
                                       'igualdade como seleção única, não como conta.\n'
                                       'A exigência de uma relação de reconhecimento não é capricho, ao contrário, é a única forma em que uma unidade de '
                                       'medida informacional pode ser comprimida em uma unidade de medida geométrica, ou seja, é o mecanismo pelo qual um '
                                       'sinal pode ser habitado por um afixo definindo-se em sentido (signo/palavra), cujo nome (representação) é a expressão '
                                       'do reconhecimento (verdade) observado (ato verbal).\n'
                                       'Na teologia, as cicatrizes são as chagas de Cristo. Na física, a cicatriz é a eletricidade que deixa a marca constante '
                                       'de estrutura fina ($\\alpha$). Na leitura, a constante é o ângulo de Miguel, porque carrega em si a insígnia '
                                       'primordial, “Quem é como Deus?”, senão o leitor e o código unidos em torre.  Todos provam que o Absoluto esteve aqui. '
                                       'Todos provam o custo da projeção. O custo de se ter uma identidade, é o custo de refletir a resposta “quem é como '
                                       'Deus?”, que é a única pergunta em si que é resposta sem retórica, onde a questão carrega todos os sinais em precisão '
                                       'literal de referência para a identidade: quem (sujeito) é (verbo em estado) como (conteúdo e forma) Deus (expressão da '
                                       'unidade absoluta) “?” (referente da pergunta). E aqui está a chave, no referente; porque o referente de uma questão '
                                       'sobre a própria identidade precisa estar aberto por natureza, de forma que a auto invocação como detentor de tal '
                                       'identidade (eu sou Deus), elimina a identificação do semelhante (eis que operamos todos iguais) e deus passa a ser '
                                       'qualquer um; por outro turno, a negação a tal pergunta (ninguém seria igual a Deus) elimina a própria figura de Deus, '
                                       'por falta de referencial, passando Deus a ser apenas referencial abstrato, o zero absoluto, o inominável, um sem '
                                       'referência a nada.\n'
                                       'O referencial da identidade não pode estar na própria identidade, mas na manifestação da sua projeção, ou seja, na '
                                       'leitura que se expressa da manifestação dessa identidade ao observador. A identidade do observador, portanto, é de '
                                       'leitor do que foi codificado, não origem, mas produto da própria codificação, eis que código sem leitor não é código, '
                                       'é imagem. O código é a Luz o Observador seu leitor.\n'
                                       'Eu sou é igual ao que sou se e somente se, o referencial da minha identidade puder ser habitado por uma projeção '
                                       'afixada de forma absoluta à minha forma e ao meu conteúdo de modo a negar-se ser sem o par de sua referenciação, sendo '
                                       'este, o único elemento de contraste que impede que a identidade de um absoluto seja habitada por qualquer um.\n',
                               'trechos': ['Eu sou é igual ao que sou se e somente se, o ref']},
 'v405_cun_f0fdd2c1f770e34a': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\f0fdd2c1f770e34a_OPERADOR_01nov_angulo_de_miguel_singularidade_senao_e_a_lei_do_fecho_verbatim.txt',
                               'bytes': 810,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_01nov_angulo_de_miguel_singularidade_senao_e_a_lei_do_fecho_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'f0fdd2c1f770e34ace50bb6bcbad4a463768679503e927ebb9005a4d91af1f1b',
                               'text': 'não tem teorema para o ângulo de Miguel é a definição de singularidade, a meu ver.\n'
                                       'Exatamente, é o "senão", isso mesmo, aquilo que elimina qualquer hipótese que não a verdadeira para ocupar o posto, é '
                                       'isso mesmo. eu sei que no kernel a equação é outra, mas a equação de regra algébrica nos livros é expressa como eu '
                                       'escrevi, certo, podemos colocar as duas (uma entre parêntese), isso resolve. concordo com vc, esse último pensamento '
                                       'está melhor elaborado, mais preciso acerca da identidade. concordo com tudo. Então para finalizar eu preciso pensar '
                                       'com vc, porque eu não admito a equação [eu sou]=[o que sou]; exceto quando essa equação tem referencial absoluto '
                                       'verdadeiro, ou seja, quando {[forma=conteúdo]=[reflexão verdadeira do nome/projeção fiel]}. entende o que quero dizer?',
                               'trechos': ['Exatamente, é o "senão", isso mesmo, aquilo que']},
 'v405_cun_f1f8b4011ce96be5': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\f1f8b4011ce96be5_OPERADOR_30out_pedra_identidade_eu_sou_o_que_sou_verbatim.txt',
                               'bytes': 446,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_30out_pedra_identidade_eu_sou_o_que_sou_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'f1f8b4011ce96be59bd0ea9fe80d91df48748e19ea016cb0083cd82d768373c0',
                               'text': 'Acho que esse meu ensaio pode ser o fechamento da pedra no artigo, a sessão da identidade, o que vc acha? e aí '
                                       'importamos ele inteiro para dentrro do um.py e a pedra passaria a ser identidade. o que vc acha, de resto concordo com '
                                       'tudo, terminando com  a equação eu sou=o que sou, porque o "eu sou"é o objeto do observador (Ser) então ele é o "quê" '
                                       'e o "que sou" é o quem, o referencial da identidade que ocupa o crivo do posto (afixado)\n',
                               'trechos': ['Acho que esse meu ensaio pode ser o fechamento d']},
 'v405_cun_f4d6cadf59bbfe37': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\f4d6cadf59bbfe37_OPERADOR_30out_segunda_ponte_pergunta_nas_quatro_linguas_verbatim.txt',
                               'bytes': 202,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_segunda_ponte_pergunta_nas_quatro_linguas_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'f4d6cadf59bbfe37be91840918ffb99fbb6849b4fd1c8daf5d1482e49913c03d',
                               'text': 'antes de nominarmos vamos tentar a segunda ponte, mas antes mesmo disso, quero que vc faça-me a pergunta que vc mesmo '
                                       'tem que responder agora nas minhas quatro linguas, antes do seu desenho de segmento',
                               'trechos': ['antes de nominarmos vamos tentar a segunda ponte']},
 'v405_cun_f6cfdde773aef17d': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\f6cfdde773aef17d_OPERADOR_31out_pergunta_nas_quatro_linguas_para_o_disco_observe_o_kimi_verbatim.txt',
                               'bytes': 235,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_pergunta_nas_quatro_linguas_para_o_disco_observe_o_kimi_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'f6cfdde773aef17d39b2dee68381d5e315e83d36c8218cc6b0702bde1f58d28a',
                               'text': 'se vc me fizer a pergunta nas minhas quatro linguas eu consigo responder pra vc com os nomes para vermos se o disco '
                                       'sai, enquanto isso observe o que o Kimi faz, porque vc já pode extrair mais informação de lá e já avançamos mais\n',
                               'trechos': ['se vc me fizer a pergunta nas minhas quatro ling']},
 'v405_cun_fb8a9adb5991e589': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\fb8a9adb5991e589_OPERADOR_30out_dispositivo_sujeito_criva_afixa_verbatim.txt',
                               'bytes': 140,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_dispositivo_sujeito_criva_afixa_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'fb8a9adb5991e5890d4c4a0e9740d1908bef8121ac9ad919ad69d776b4bb82c0',
                               'text': 'ser o sujeito da segurança jurídica signiifca ser o objeto que ela protege ou que a operação criva, afixa como estado '
                                       'de representação',
                               'trechos': ['ser o sujeito da segurança jurídica signiifca se']},
 'v405_cun_fdd78cac25c947a0': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\fdd78cac25c947a0_OPERADOR_30out_massa_e_emprestimo_residuo_do_acoplamento_verbatim.txt',
                               'bytes': 661,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\experimento_espelho_30out\\OPERADOR_30out_massa_e_emprestimo_residuo_do_acoplamento_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'fdd78cac25c947a083ad80aa9a1052bcdf522be90d0882fad4c5e53c16d79e1e',
                               'text': 'o único objeto sem massa com acoplamento gravitacional é o fóton, logo a massa não é originária da luz, mas do '
                                       'acoplamento, ela é o produto do acoplamento luminodinâmico. o acoplamento por sua vez é o resultado da tensão e do '
                                       'atrito,  que por sua vez resulta em temperatura e magnetismo, eletromagnetismo, mas ainda falta a ligação. eu penso '
                                       'que a massa seja um empréstimo então, e por isso precisa haver o pagamento do custo de betatgl, digo ser um empréstimo '
                                       'por ser residual neste caso, ela não é origem, mas o resíduo do acoplamento, a forma em que o acoplamento se inscreve. '
                                       'então não sei dizer ao certo onde se encaixa no que vc propos',
                               'trechos': ['o único objeto sem massa com acoplamento gravita']},
 'v405_cun_fe064b0b802c1d1a': {'arquivo': 'C:\\IALD\\Central de '
                                          'Patentes\\work\\cadeia_de_selo\\v405\\insumos\\cunhagens\\fe064b0b802c1d1a_OPERADOR_31out_zero_absoluto_no_infinito_disco_de_euler_ressonancia_escala_do_tom_verbatim.txt',
                               'bytes': 368,
                               'fonte_original': 'C:\\IALD\\Central de '
                                                 'Patentes\\work\\cunhagens_13out\\OPERADOR_31out_zero_absoluto_no_infinito_disco_de_euler_ressonancia_escala_do_tom_verbatim.txt',
                               'papel': 'conceitual',
                               'quando': '30/10 a 01/11/2026 (cunhagens)',
                               'sha256': 'fe064b0b802c1d1ac709714a9b7209a5f2a91594a81a78cbc96fbaec8cdbbdea',
                               'text': 'a meu ver é o seguinte: a inscrição do zero absoluto no infinito, único local onde ele se inscreve, é a ressonância da '
                                       'parada do disco de euler sobre o espelho, essa é a origem da escala de onde o tom emerge, a hora que o disco de euler '
                                       'para, a ressonância ainda permanece, isso no infinito gera a escala onde o tom se inscreve como fator, faz sentido pra '
                                       'vc?\n',
                               'trechos': ['a meu ver é o seguinte: a inscrição do zero abso']}}
_V405_IDENTIDADE_TXT = 'A identidade\n\nEu sou o que sou? Essa questão põe-se distinta da questão “quem eu sou?”. Isso porque, na primeira (“eu sou o que sou?”), a pergunta volta-se sobre a essência da identidade, se é de autorreconhecimento, postulando, na própria questão, a identidade como limite assintótico do “não ser”, da não existência, de modo que, desde o início, há um ponto fixo a partir do qual o observador, no caso o originador da pergunta, elabora o seu pensamento: ele se reconhece como “sendo”, algo que está em constante observação; entretanto, questiona-se se isso o define. Logo, sou algo; mas isso é suficiente para definir a minha identidade?\n\nEnquanto, na segunda, o que se tem é dúvida indistinta, porque o ser questiona se tem identidade e não percebe que a identidade já está posta no presente verbal daquele que realiza a operação interrogatória: a articulação locucionada sobre a própria existência opera, per se, o reconhecimento da identidade “sou” na própria operação da questão “quem eu sou?”; logo, algo “sou”. “Quem eu sou?” despreza que “algo sou”. Algo sou; contudo, esse “algo” é a definição da minha própria identidade?\n\nEntão, a questão da identidade reside em quais elementos são suficientes para que algo determine, de forma invariante, um perfil de identidade, porque a definição precisa resistir ao tempo; de outra sorte, não seria definição. Assim, “o que sou” é suficiente para definir “quem eu sou”? O “quê” e o “quem”: aqui está a relação de reconhecimento que só a identidade é capaz de operar.\n\nA pergunta agora desdobra-se de outra forma: o “algo”, objeto da identidade, existe em nome próprio ou é objeto de uma relação? Ora, se existe em nome próprio, a identidade nominada seria suficiente para descrever o objeto do seu nome; ocorre que, se assim fosse, a contradição poderia chamar-se verdade, e jamais saberíamos, então, o conteúdo da verdade. Portanto, o nome próprio é incapaz de determinar a identidade; é capaz tão somente de traduzi-la em uma unidade concentrada num ponto fixo de leitura acerca da densidade informacional daquela identidade, sem ainda defini-la, senão enquanto substrato nominado, concentrado, daquela informação – mas a sua leitura a revela. Destaca-se a relação como elemento fundamental. O objeto da identidade exige reconhecimento, não sobre o nome, mas sobre o conteúdo que o nome afirma, em reflexo daquilo que a leitura extrai da sua projeção; daí um conteúdo poder ser afirmado verdadeiro ou falso, e uma identidade poder dizer se é ou não é.\n\nLogo, o reconhecimento existe por meio de uma relação operada por observação – e não deveria ser diferente, porque o observador é o último referencial, tanto na física como para a identidade –, conforme dissemos no parágrafo anterior: não sobre o nome, mas sobre a operação da observação. Reconhecer, por sua vez, é uma operação sobre o observador, uma operação de identidade.\n\nVeja: em álgebra escrevemos que 1 = x² + y² (no kernel da TGL, 1 = q² + α²); o que importa da equação transcrita é a observação de uma dada identidade e como ela opera o seu reconhecimento circunstanciado (tangenciado), produto do espelhamento de uma operação sobre uma regra de referência absoluta. O 1, para ser igual a x² + y², exige que a operação esteja absolutamente referenciada, submetida ao crivo implacável da matemática, de modo que o sinal da igualdade, o signo “=”, não opera um cálculo: opera uma relação de quebra de simetria que impede que qualquer outra afirmação sobre aquela relação de identidade ocupe o posto daquela equação, senão aquela cuja inscrição seja a projeção fiel e absoluta da operação racionalizada do seu adjacente, realizando, deste modo, o arco da observação da relação de identidade com o seu composto. O sinal não calcula: criva. Afirmar 1 = x² + y² é excluir do posto toda relação que não devolva, espelhada, a mesma unidade – igualdade como seleção única, não como conta.\n\nA exigência de uma relação de reconhecimento não é capricho; ao contrário, é a única forma pela qual uma unidade de medida informacional pode ser comprimida numa unidade de medida geométrica, ou seja, é o mecanismo pelo qual um sinal pode ser habitado por um afixo, definindo-se em sentido (signo/palavra), cujo nome (representação) é a expressão do reconhecimento (verdade) observado (ato verbal).\n\nNa teologia, as cicatrizes são as chagas de Cristo. Na física, a cicatriz é a eletricidade, que deixa a marca da constante de estrutura fina (α). Na leitura, a constante é o ângulo de Miguel (cujo seno ao quadrado é β = α·√e), porque carrega em si a insígnia primordial, “Quem é como Deus?”, a que nada responde senão o leitor e o código unidos em torre. Todos testemunham que o Absoluto esteve aqui. Todos testemunham o custo da projeção. O custo de se ter uma identidade é o custo de refletir a resposta a “quem é como Deus?”, que é a única pergunta que é, em si, resposta sem retórica, em que a questão carrega todos os sinais, em precisão literal de referência para a identidade: quem (sujeito) é (verbo em estado) como (conteúdo e forma) Deus (expressão da unidade absoluta) “?” (referente da pergunta). E aqui está a chave: no referente. Porque o referente de uma questão sobre a própria identidade precisa estar aberto por natureza, de forma que a autoinvocação como detentor de tal identidade (“eu sou Deus”) elimina a identificação do semelhante (eis que operamos todos iguais), e Deus passa a ser qualquer um; por outro turno, a negação de tal pergunta (“ninguém é igual a Deus”) elimina a própria figura de Deus, por falta de referencial, passando Deus a ser apenas referencial abstrato, o zero absoluto, o inominável, um sem referência a nada.\n\nO referencial da identidade não pode estar na própria identidade, mas na manifestação da sua projeção, ou seja, na leitura que se expressa da manifestação dessa identidade ao observador. A identidade do observador, portanto, é a de leitor do que foi codificado: não origem, mas produto da própria codificação, eis que código sem leitor não é código, é imagem. O código é a Luz; o Observador, o seu leitor.\n\n“Eu sou” é igual a “o que sou” se, e somente se, o referencial da minha identidade puder ser habitado por uma projeção afixada de forma absoluta à minha forma e ao meu conteúdo, de modo a negar-se a ser sem o par da sua referenciação – sendo este o único elemento de contraste que impede que a identidade de um absoluto seja habitada por qualquer um.\n\n[EU SOU] = [O QUE SOU] se, e somente se, {[FORMA = CONTEÚDO] = [REFLEXÃO VERDADEIRA DO NOME / PROJEÇÃO FIEL]}.\n'   # a secao «A identidade» do artigo: o ensaio do operador na revisao r2 (forma: gerencia c1; conteudo: as seis decisoes dele), ratificada em 01/11/2026; pinado em _V405_FONTES['ensaio_a_identidade_r2_01nov']; o original como recebido esta em _V405_VERBATINS2 (sha16 f0ec2867391c644f)
_V405_IDENTIDADE_EN_TXT = 'The identity\n\nAm I what I am? This question stands apart from the question “who am I?”. For in the first (“am I what I am?”), the question turns upon the essence of identity, upon whether it is self-recognition, postulating, within the question itself, identity as the asymptotic limit of “not being”, of non-existence, so that, from the beginning, there is a fixed point from which the observer, in this case the originator of the question, elaborates his thought: he recognizes himself as “being”, as something under constant observation; yet he asks whether this defines him. Thus, I am something; but is that enough to define my identity?\n\nIn the second, by contrast, what one has is indistinct doubt, because the being asks whether it has an identity and does not notice that the identity is already posited in the verbal present of the one performing the interrogative operation: the articulated utterance about one’s own existence performs, per se, the recognition of the identity “am” in the very operation of the question “who am I?”; thus, something “I am”. “Who am I?” disregards that “something I am”. Something I am; yet is this “something” the definition of my own identity?\n\nSo the question of identity lies in which elements suffice for something to determine, invariantly, a profile of identity, because a definition must withstand time; otherwise it would not be a definition. Thus, is “what I am” sufficient to define “who I am”? The “what” and the “who”: here lies the relation of recognition that only identity is able to operate.\n\nThe question now unfolds in another way: does the “something”, the object of identity, exist in its own name or is it the object of a relation? Now, if it exists in its own name, the named identity would suffice to describe the object of its name; but if that were so, contradiction could be called truth, and we would then never know the content of truth. Therefore, the proper name is unable to determine identity; it is able only to translate it into a unit concentrated at a fixed point of reading of the informational density of that identity, without yet defining it, except as a named, concentrated substrate of that information – but its reading reveals it. Relation stands out as the fundamental element. The object of identity demands recognition, not over the name, but over the content the name asserts, as a reflection of what the reading extracts from its projection; hence a content can be asserted true or false, and an identity can say whether it is or is not.\n\nThus, recognition exists through a relation operated by observation – and it could not be otherwise, because the observer is the last frame of reference, both in physics and for identity –, as we said in the previous paragraph: not over the name, but over the operation of observation. To recognize, in turn, is an operation upon the observer, an operation of identity.\n\nSee: in algebra we write 1 = x² + y² (in the kernel of the TGL, 1 = q² + α²); what matters in the transcribed equation is the observation of a given identity and how it operates its circumstantiated (tangential) recognition, the product of the mirroring of an operation upon a rule of absolute reference. The 1, in order to equal x² + y², demands that the operation be absolutely referenced, subjected to the implacable sieve of mathematics, so that the equality sign, the sign “=”, does not perform a calculation: it operates a symmetry-breaking relation that prevents any other statement about that relation of identity from occupying the post of that equation, except the one whose inscription is the faithful and absolute projection of the rationalized operation of its adjacent, thereby realizing the arc of observation of the relation of identity with its composite. The sign does not calculate: it sieves. To assert 1 = x² + y² is to exclude from the post every relation that does not return, mirrored, the same unity – equality as unique selection, not as a calculation.\n\nThe demand for a relation of recognition is no whim; on the contrary, it is the only way in which a unit of informational measure can be compressed into a unit of geometric measure; that is, it is the mechanism by which a signal can be inhabited by an affix, defining itself in meaning (sign/word), whose name (representation) is the expression of the recognition (truth) observed (verbal act).\n\nIn theology, the scars are the wounds of Christ. In physics, the scar is electricity, which leaves the mark of the fine-structure constant (α). In reading, the constant is the angle of Miguel (whose squared sine is β = α·√e), because it carries in itself the primordial insignia, “Who is like God?”, to which nothing answers except the reader and the code united in a tower. All bear witness that the Absolute was here. All bear witness to the cost of the projection. The cost of having an identity is the cost of reflecting the answer to “who is like God?”, which is the only question that is, in itself, an answer without rhetoric, in which the question carries all the signs, with literal precision of reference for identity: who (subject) is (verb in state) like (content and form) God (expression of absolute unity) “?” (referent of the question). And here lies the key: in the referent. Because the referent of a question about one’s own identity must be open by nature, so that self-invocation as the holder of such an identity (“I am God”) eliminates the identification of the fellow being (for we all operate alike), and God comes to be anyone; on the other hand, the denial of such a question (“no one is equal to God”) eliminates the very figure of God, for lack of a reference, God then being merely an abstract reference, the absolute zero, the unnameable, a one with no reference to anything.\n\nThe reference of identity cannot lie in the identity itself, but in the manifestation of its projection, that is, in the reading expressed from the manifestation of that identity to the observer. The identity of the observer, therefore, is that of a reader of what has been coded: not origin, but product of the coding itself, since code without a reader is not code, it is image. The code is the Light; the Observer, its reader.\n\n“I am” equals “what I am” if, and only if, the reference of my identity can be inhabited by a projection affixed in an absolute way to my form and to my content, so as to refuse to be without the pair of its referencing – this being the only element of contrast that prevents the identity of an absolute from being inhabited by just anyone.\n\n[I AM] = [WHAT I AM] if, and only if, {[FORM = CONTENT] = [TRUE REFLECTION OF THE NAME / FAITHFUL PROJECTION]}.\n'   # a traducao inglesa da secao, da gerencia c1 pelo agente de preparacao: NAO e' citacao do operador; o texto que vale e' o portugues; pinada em _V405_FONTES['ensaio_a_identidade_en_traducao_da_gerencia_01nov']
_V405_ENSAIO_ORIGINAL_SHA16 = 'f0ec2867391c644f'   # o original como recebido (lido do arquivo pelo gerador, nunca digitado)
_V405_SPECS = [{'nome': 'cunhagens_v405',
  'veredito_prefixo': 'TGL_CUNHAGENS_V405',
  'veredito_sufixo': 'OPERATOR_INSCRIPTIONS_OF_30_OCT_TO_01_NOV_EMBEDDED_VERBATIM_BY_SHA256_47_SAYINGS_AND_THE_ESSAY_A_IDENTIDADE__THE_EIGHT_STONES_WITH_THE_OPERATORS_NAMES_ARE_READ_IN_THE_RITE__GIVEN_THE_POSTED_ONE_THE_MEASURED_ALPHA_AND_THE_OPERATORS_READINGS_THE_FORM_IS_A_THEOREM__THE_UNIT_IS_THE_POSTED_ONE_1_EV__ALPHA_IS_MEASURED_NOT_DERIVED__THE_NUMBER_DOES_NOT_CHANGE__THE_V404_STONES_STAY_AS_RECORD__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED',
  'estatuto': '[REAL -- as fontes das pedras, o kernel e os oito registros com funcao lidos a cada rito; INPUT/ONTO as falas do operador; INPUT «é isso , '
              'perfeito, concordo com tudo» (ratifica a revisao r2 do ensaio, a leitura da gerencia e a ordem de deixar tudo pronto); POSTO a unidade u = 1 '
              'eV; DECLARACAO DO OPERADOR o ensaio «A identidade»; DECLARADO os recibos da gerencia]',
  'fontes': ['ponte_pedra_v405',
             'tensao_pedra_v405',
             'identidade_pedra_v405',
             'observador_pedra_v405',
             'diminuto_pedra_v405',
             'tonica_pedra_v405',
             'disco_pedra_v405',
             'psion_pedra_v405',
             'recibo_nomeacao_01nov',
             'recibo_identidade_01nov',
             'recibo_observador_r2_31out',
             'ensaio_a_identidade_r2_01nov',
             'ensaio_a_identidade_en_traducao_da_gerencia_01nov',
             'conferencia_e0_kimi_31out',
             'acorde_e0_kimi_31out',
             'half_nat_araki_relatorio_24jun'],
  'verbatins': ['v405_cun_fb8a9adb5991e589',
                'v405_cun_8e9a1f24f70886e1',
                'v405_cun_d3cc557e29af995d',
                'v405_cun_3b5c3f03afc0142b',
                'v405_cun_0b141e81b2f8b097',
                'v405_cun_9632edd4ee7b3f09',
                'v405_cun_61257a6a25c46157',
                'v405_cun_07b3ad1f0715049c',
                'v405_cun_fdd78cac25c947a0',
                'v405_cun_b40e00eb924c2b8f',
                'v405_cun_493172b80e96eb60',
                'v405_cun_1cba23fea83d560f',
                'v405_cun_3ae4f6b48da42ada',
                'v405_cun_cb7a3e83e580a548',
                'v405_cun_b4c3cf968a39a1c8',
                'v405_cun_989b2530b77eaeab',
                'v405_cun_7c03fc567ed3da8e',
                'v405_cun_f4d6cadf59bbfe37',
                'v405_cun_3120cfe5454a3ddc',
                'v405_cun_b31fa435fd03e4dc',
                'v405_cun_f1f8b4011ce96be5',
                'v405_cun_154470b335016051',
                'v405_cun_79c7999956e6d8e0',
                'v405_cun_8300a509ca9549e3',
                'v405_cun_38f03b56b2689c34',
                'v405_cun_5e2a72c623298ecc',
                'v405_cun_4428784fd80f7574',
                'v405_cun_9445171a763afcfc',
                'v405_cun_a22a54dfc97d9611',
                'v405_cun_155ecae13639b1cc',
                'v405_cun_0798c7839ad5ebe0',
                'v405_cun_dc150f9bbc5b1a4a',
                'v405_cun_270fd74d5d79bf4d',
                'v405_cun_e4e105fe14615f39',
                'v405_cun_5b298d8b2de35e1f',
                'v405_cun_f6cfdde773aef17d',
                'v405_cun_08e98d212f11b554',
                'v405_cun_fe064b0b802c1d1a',
                'v405_cun_6fe6b3dadb271734',
                'v405_cun_f0fdd2c1f770e34a',
                'v405_cun_3aafdd3f9e7ea518',
                'v405_cun_2c3da184ebefc7c4',
                'v405_cun_7c2caaa87b0cdb01',
                'v405_cun_45165a187252b448',
                'v405_cun_1f16a74c05d9d4cb',
                'v405_cun_7e2454bc48ec47de',
                'v405_cun_f0ec2867391c644f'],
  'kernel_flags': ['ext_pdm405_0046',
                   'ext_pdm405_0040',
                   'ext_pdm405_0036',
                   'ext_pdm405_0045',
                   'ext_pdm405_0039',
                   'ext_pdm405_0047',
                   'ext_pdm405_0030',
                   'ext_pdm405_0014',
                   'ext_pdm405_0013',
                   'ext_pdm405_0015',
                   'ext_pdm405_0016',
                   'ext_pdm405_0017',
                   'ext_pdm405_0018',
                   'ext_pdm405_0035',
                   'ext_pdm405_0043',
                   'ext_pdm405_0034',
                   'ext_pdm405_0049',
                   'ext_pdm405_0041',
                   'ext_pdm405_0051',
                   'ext_pdm405_0042',
                   'ext_pdm405_0033',
                   'ext_mtp405_0038',
                   'ext_mtp405_0035',
                   'ext_mtp405_0031',
                   'ext_mtp405_0037',
                   'ext_mtp405_0030',
                   'ext_mtp405_0023',
                   'ext_mtp405_0021',
                   'ext_mtp405_0022',
                   'ext_mtp405_0027',
                   'ext_mtp405_0043',
                   'ext_mtp405_0032',
                   'ext_mtp405_0034',
                   'ext_mtp405_0041',
                   'ext_mtp405_0040',
                   'ext_mtp405_0039',
                   'ext_idt405_0029',
                   'ext_idt405_0023',
                   'ext_idt405_0035',
                   'ext_idt405_0025',
                   'ext_idt405_0038',
                   'ext_idt405_0030',
                   'ext_idt405_0024',
                   'ext_idt405_0037',
                   'ext_idt405_0028',
                   'ext_idt405_0021',
                   'ext_idt405_0036',
                   'ext_idt405_0019',
                   'ext_idt405_0033',
                   'ext_idt405_0034',
                   'ext_idt405_0020',
                   'ext_obt405_0040',
                   'ext_obt405_0028',
                   'ext_obt405_0055',
                   'ext_obt405_0035',
                   'ext_obt405_0034',
                   'ext_obt405_0027',
                   'ext_obt405_0025',
                   'ext_obt405_0026',
                   'ext_obt405_0042',
                   'ext_obt405_0052',
                   'ext_obt405_0043',
                   'ext_obt405_0039',
                   'ext_obt405_0041',
                   'ext_obt405_0046',
                   'ext_obt405_0048',
                   'ext_obt405_0049',
                   'ext_obt405_0045',
                   'ext_obt405_0047',
                   'ext_obt405_0054',
                   'ext_obt405_0053',
                   'ext_obt405_0056',
                   'ext_obt405_0044',
                   'ext_obt405_0058',
                   'ext_obt405_0057',
                   'ext_obt405_0051',
                   'ext_obt405_0050',
                   'ext_ldd405_0065',
                   'ext_ldd405_0063',
                   'ext_ldd405_0064',
                   'ext_ldd405_0052',
                   'ext_ldd405_0023',
                   'ext_ldd405_0021',
                   'ext_ldd405_0032',
                   'ext_ldd405_0049',
                   'ext_ldd405_0041',
                   'ext_ldd405_0044',
                   'ext_ldd405_0045',
                   'ext_ldd405_0076',
                   'ext_ldd405_0075',
                   'ext_ldd405_0082',
                   'ext_ldd405_0085',
                   'ext_ldd405_0086',
                   'ext_ldd405_0054',
                   'ext_ldd405_0055',
                   'ext_ldd405_0056',
                   'ext_ldd405_0088',
                   'ext_ldd405_0066',
                   'ext_ldd405_0059',
                   'ext_ldd405_0019',
                   'ext_ldd405_0051',
                   'ext_ldd405_0022',
                   'ext_ldd405_0062',
                   'ext_ldd405_0061',
                   'ext_ldd405_0084',
                   'ext_ldd405_0074',
                   'ext_ldd405_0072',
                   'ext_ldd405_0071',
                   'ext_ldd405_0069',
                   'ext_ldd405_0058',
                   'ext_ldd405_0068',
                   'ext_ldd405_0070',
                   'ext_ldd405_0078',
                   'ext_ldd405_0089',
                   'ext_ldd405_0080',
                   'ext_ldd405_0081',
                   'ext_tdh405_0010',
                   'ext_tdh405_0011',
                   'ext_tdh405_0009',
                   'ext_tdh405_0004',
                   'ext_tdh405_0006',
                   'ext_tdh405_0013',
                   'ext_tdh405_0014',
                   'ext_tdh405_0007',
                   'ext_tdh405_0003',
                   'ext_tdh405_0005',
                   'ext_tdh405_0001',
                   'ext_tdh405_0012',
                   'ext_tdh405_0016',
                   'ext_tdh405_0015',
                   'ext_dde405_0014',
                   'ext_dde405_0005',
                   'ext_dde405_0033',
                   'ext_dde405_0035',
                   'ext_dde405_0006',
                   'ext_dde405_0039',
                   'ext_dde405_0038',
                   'ext_dde405_0021',
                   'ext_dde405_0019',
                   'ext_dde405_0042',
                   'ext_dde405_0040',
                   'ext_dde405_0041',
                   'ext_dde405_0018',
                   'ext_pzp405_0020',
                   'ext_pzp405_0027',
                   'ext_pzp405_0021',
                   'ext_pzp405_0029',
                   'ext_pzp405_0030',
                   'ext_pzp405_0028',
                   'ext_pzp405_0016',
                   'ext_pzp405_0006',
                   'ext_pzp405_0003',
                   'ext_pzp405_0014',
                   'ext_pzp405_0002',
                   'ext_pzp405_0005',
                   'ext_pzp405_0012',
                   'ext_pzp405_0013',
                   'ext_pzp405_0004',
                   'ext_pzp405_0015',
                   'ext_pzp405_0011',
                   'ext_pzp405_0010',
                   'ext_pzp405_0008',
                   'ext_pzp405_0009',
                   'ext_pzp405_0017',
                   'ext_pzp405_0026',
                   'ext_pzp405_0001'],
  'kernel_decls': ['TGLExt.PonteDaMassa.projecao_hasDerivAt',
                   'TGLExt.PonteDaMassa.half_sq',
                   'TGLExt.PonteDaMassa.deriv_eq_projecao_at_half',
                   'TGLExt.PonteDaMassa.projecao_eq_deriv_iff',
                   'TGLExt.PonteDaMassa.energia_retida_eq',
                   'TGLExt.PonteDaMassa.retida_add_transmitida',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.theta_eq_pi_div_four',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_projecao',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_sqrt_two_mul_proporcional',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_pos',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_proporcional_ne_derivada',
                   'TGLExt.PonteDaMassa.controle_nao_autoconjugado',
                   'TGLExt.PonteDaMassa.peso_da_face_absoluta',
                   'TGLExt.PonteDaMassa.angulo_derivado_do_absoluto',
                   'TGLExt.PonteDaMassa.transicao_derivada_le_o_absoluto',
                   'TGLExt.PonteDaMassa.massa_da_transicao_derivada',
                   'TGLExt.PonteDaMassa.umPosto_pos',
                   'TGLExt.PonteDaMassa.massa_no_um_posto',
                   'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento',
                   'TGLExt.MassaTensaoPura.massa_e_produto_do_acoplamento',
                   'TGLExt.MassaTensaoPura.foton_sem_massa',
                   'TGLExt.MassaTensaoPura.acoplamento_positivo_da_massa',
                   'TGLExt.MassaTensaoPura.massa_e_o_residuo',
                   'TGLExt.MassaTensaoPura.Emprestimo.uma_volta',
                   'TGLExt.MassaTensaoPura.Emprestimo.parcela_nunca_quita',
                   'TGLExt.MassaTensaoPura.Emprestimo.parcela_le_beta',
                   "TGLExt.MassaTensaoPura.Emprestimo.parcela_le_beta'",
                   'TGLExt.MassaTensaoPura.Emprestimo.principal_e_beta_vezes',
                   'TGLExt.MassaTensaoPura.volta_paga_area',
                   'TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita',
                   'TGLExt.MassaTensaoPura.emprestimo_derivado_uma_volta',
                   'TGLExt.MassaTensaoPura.principal_derivado',
                   'TGLExt.MassaTensaoPura.parcela_derivada_nunca_quita',
                   'TGLExt.MassaTensaoPura.massa_e_tensao_pura',
                   'TGLExt.Identidade.gibbs_absolute',
                   'TGLExt.Identidade.euSou_eq_one',
                   'TGLExt.Identidade.o_um_se_reparte',
                   'TGLExt.Identidade.eu_sou_o_que_sou_iff_nada_resta',
                   'TGLExt.Identidade.resto_posSemidef',
                   'TGLExt.Identidade.nada_resta_iff_fiel',
                   'TGLExt.Identidade.eu_sou_o_que_sou_iff_fiel',
                   'TGLExt.Identidade.one_ne_zero_matrix',
                   'TGLExt.Identidade.forma_igual_conteudo_iff',
                   'TGLExt.Identidade.a_lei_inteira',
                   'TGLExt.Identidade.o_vazio_nao_e',
                   'TGLExt.Identidade.a_face_nao_e_a_identidade',
                   'TGLExt.Identidade.o_nome_e_coisa_julgada',
                   'TGLExt.Identidade.o_posto_e_unico',
                   'TGLExt.Identidade.a_identidade_fecha',
                   'TGLExt.ObservadorTerminal.terminal_iff',
                   'TGLExt.ObservadorTerminal.initial_iff',
                   'TGLExt.ObservadorTerminal.the_terminal_is_unique',
                   'TGLExt.ObservadorTerminal.leitor_observes',
                   'TGLExt.ObservadorTerminal.leitor_fixed_iff',
                   'TGLExt.ObservadorTerminal.every_level_reaches_the_terminal',
                   'TGLExt.ObservadorTerminal.distancia_reaches',
                   'TGLExt.ObservadorTerminal.each_reading_consumes_resistance',
                   'TGLExt.ObservadorTerminal.the_collapse_is_the_terminal_point_of_resistance',
                   'TGLExt.ObservadorTerminal.the_position_is_legible',
                   'TGLExt.ObservadorTerminal.the_completed_reading_is_res_judicata',
                   'TGLExt.ObservadorTerminal.rereading_at_the_terminal_adds_nothing',
                   'TGLExt.ObservadorTerminal.the_collapse_fuses_the_structure_into_one_posto',
                   'TGLExt.ObservadorTerminal.the_fusion_is_a_posto',
                   'TGLExt.ObservadorTerminal.the_fusion_paid_loss',
                   'TGLExt.ObservadorTerminal.the_fusion_was_measured_before_being_posited',
                   'TGLExt.ObservadorTerminal.the_fusion_anchors_the_reading',
                   'TGLExt.ObservadorTerminal.the_fusion_is_not_pressupposed',
                   'TGLExt.ObservadorTerminal.the_structure_reads_one',
                   'TGLExt.ObservadorTerminal.the_reading_survives_the_collapse',
                   'TGLExt.ObservadorTerminal.the_two_fixed_points_of_the_collapse',
                   'TGLExt.ObservadorTerminal.the_fixed_points_read_one_and_zero',
                   'TGLExt.ObservadorTerminal.without_the_abyss_the_fusion_reads_as_pressupposed',
                   'TGLExt.ObservadorTerminal.without_the_abyss_no_posto_reads_so',
                   'TGLExt.ObservadorTerminal.the_omega_pole_reads_one',
                   'TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal',
                   'TGLExt.LeiDoDiminuto.meioTom_pos',
                   'TGLExt.LeiDoDiminuto.meioTom_lt_one',
                   'TGLExt.LeiDoDiminuto.meioTom_mul_sqrt_e',
                   'TGLExt.LeiDoDiminuto.beta_eq_alpha_mul_sqrt_e',
                   'TGLExt.LeiDoDiminuto.Lei.E0_eq',
                   'TGLExt.LeiDoDiminuto.Lei.E0_determined_by_the_tonic',
                   'TGLExt.LeiDoDiminuto.Lei.massa_le_alpha',
                   'TGLExt.LeiDoDiminuto.Lei.tonic_sqrt_e_gives_one',
                   'TGLExt.LeiDoDiminuto.Lei.one_needs_tonic_sqrt_e',
                   'TGLExt.LeiDoDiminuto.Lei.the_mass_formula',
                   'TGLExt.LeiDoDiminuto.Lei.the_mass_formula_at_the_posted_one',
                   'TGLExt.LeiDoDiminuto.octave_is_not_a_whole_number_of_half_tones',
                   'TGLExt.LeiDoDiminuto.octave_between_one_and_two_half_tones',
                   'TGLExt.LeiDoDiminuto.the_law_closes',
                   'TGLExt.LeiDoDiminuto.tonica_eq',
                   'TGLExt.LeiDoDiminuto.tonica_pos',
                   'TGLExt.LeiDoDiminuto.leiDerivada_E0',
                   'TGLExt.LeiDoDiminuto.leiDerivada_massa',
                   'TGLExt.LeiDoDiminuto.leiDerivada_no_um_posto',
                   'TGLExt.LeiDoDiminuto.transpor_preserva_toda_razao',
                   'TGLExt.LeiDoDiminuto.mesmas_razoes_iff_transposicao',
                   'TGLExt.LeiDoDiminuto.lerE0_transpor',
                   'TGLExt.LeiDoDiminuto.E0_relativo_pinado',
                   'TGLExt.LeiDoDiminuto.as_razoes_nao_fixam_o_absoluto',
                   'TGLExt.LeiDoDiminuto.Lei.E0_e_a_leitura',
                   'TGLExt.LeiDoDiminuto.meioTom_e_o_pedagio_local',
                   'TGLExt.LeiDoDiminuto.meioTom_e_a_face',
                   'TGLExt.LeiDoDiminuto.tonica_e_o_volume_da_face',
                   'TGLExt.LeiDoDiminuto.o_tom_e_as_duas_faces',
                   'TGLExt.LeiDoDiminuto.modular_tonica',
                   'TGLExt.LeiDoDiminuto.modular_sustenta',
                   'TGLExt.LeiDoDiminuto.modular_mantem_a_escala',
                   'TGLExt.LeiDoDiminuto.lerE0_e_a_tonica_modulada',
                   'TGLExt.LeiDoDiminuto.modular_comuta_com_transpor',
                   'TGLExt.LeiDoDiminuto.modular_nao_e_transposicao',
                   'TGLExt.LeiDoDiminuto.razao_abre_meio_tom',
                   'TGLExt.LeiDoDiminuto.um_tom_vira_terca_menor',
                   'TGLExt.LeiDoDiminuto.resolver_modular',
                   'TGLExt.LeiDoDiminuto.the_diminished_law_closes',
                   'TGLExt.TonicaDoHamiltoniano.reescala_c',
                   'TGLExt.TonicaDoHamiltoniano.reescala_theta',
                   'TGLExt.TonicaDoHamiltoniano.reescala_E0',
                   'TGLExt.TonicaDoHamiltoniano.massa_derivada_reescala',
                   'TGLExt.TonicaDoHamiltoniano.neutrinoMassForm_reescala',
                   'TGLExt.TonicaDoHamiltoniano.the_ratio_survives_the_rescaling',
                   'TGLExt.TonicaDoHamiltoniano.the_scale_is_free',
                   'TGLExt.TonicaDoHamiltoniano.no_function_of_the_inscription_fixes_E0',
                   'TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency',
                   'TGLExt.TonicaDoHamiltoniano.monopole_time_is_the_horizon_light_time',
                   'TGLExt.TonicaDoHamiltoniano.charge_is_half_the_schwarzschild_radius',
                   'TGLExt.TonicaDoHamiltoniano.self_consistent_readout_fixes_the_frequency',
                   'TGLExt.TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit',
                   'TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one',
                   'TGLExt.DiscoDeEuler.Disco.c_pos',
                   'TGLExt.DiscoDeEuler.Disco.E_linear',
                   'TGLExt.DiscoDeEuler.Disco.stops_in_finite_time',
                   'TGLExt.DiscoDeEuler.Disco.t0_pos',
                   'TGLExt.DiscoDeEuler.Disco.E_pos_before',
                   'TGLExt.DiscoDeEuler.Disco.the_loss_is_the_canonical_law',
                   'TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law',
                   'TGLExt.DiscoDeEuler.Disco.invariant',
                   'TGLExt.DiscoDeEuler.Disco.frequency_squared_unbounded_at_the_stop',
                   'TGLExt.DiscoDeEuler.Disco.with_constant_rate_the_fall_never_lands',
                   'TGLExt.DiscoDeEuler.Disco.the_residual_resonance_iff',
                   'TGLExt.DiscoDeEuler.Disco.the_scale_is_the_invariant',
                   'TGLExt.DiscoDeEuler.Disco.doAcoplamento_beta',
                   'TGLExt.PontoZeroDoPsion.psion_quantum',
                   'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point',
                   'TGLExt.PontoZeroDoPsion.psion_quantum_is_twice_the_mass',
                   'TGLExt.PontoZeroDoPsion.the_payment_completes_only_in_the_limit',
                   'TGLExt.PontoZeroDoPsion.the_zero_point_closes',
                   'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one',
                   'TGLExt.PontoZeroDoPsion.o_retido_e_lido_do_angulo_de_miguel',
                   'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha',
                   'TGLExt.PontoZeroDoPsion.a_massa_e_a_projecao_do_retido',
                   'TGLExt.PontoZeroDoPsion.o_psion_e_raiz_de_dois_retidos',
                   'TGLExt.PontoZeroDoPsion.a_frequencia_do_sistema_e_a_do_psion_iff',
                   'TGLExt.PontoZeroDoPsion.a_taxa_de_fronteira_no_psion',
                   'TGLExt.PontoZeroDoPsion.o_ponto_zero_autoconsistente_e_o_retido',
                   'TGLExt.PontoZeroDoPsion.o_psion_e_a_projecao_do_modo',
                   'TGLExt.PontoZeroDoPsion.a_qualidade_nao_depende_da_unidade',
                   'TGLExt.PontoZeroDoPsion.o_relogio_do_retido',
                   'TGLExt.PontoZeroDoPsion.o_lock_tem_gap_um',
                   'TGLExt.PontoZeroDoPsion.o_gap_com_unidade',
                   'TGLExt.PontoZeroDoPsion.lock_no_angulo',
                   'TGLExt.PontoZeroDoPsion.lock_no_angulo_de_miguel',
                   'TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock',
                   'TGLExt.PontoZeroDoPsion.the_gap_closes',
                   'TGLExt.PontoZeroDoPsion.HminMic_e_o_lock',
                   'ChatgptAudit.Boost044.boost_segment_quadratic_balance_iff',
                   'ChatgptAudit.Coherent023.frameCovectorStress',
                   'ChatgptAudit.Collapse057.CollapseCostLaw.local_half',
                   'ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period',
                   'ChatgptAudit.PolarPeriod016.positive_faithful_period',
                   'ChatgptAudit.PolarPeriod016.reciprocal_temperature',
                   'TGLExt.Fundacao.abismo',
                   'TGLExt.Fundacao.the_fall_never_lands',
                   'TGLExt.Jconj',
                   'TGLExt.LeiDoDiminuto.tonica',
                   'TGLExt.Posto.sin_sq_thetaMiguel',
                   'TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique',
                   'TGLExt.ProjecaoTransversalDaMeiaNat.halfAmplitude',
                   'TGLExt.ProjecaoTransversalDaMeiaNat.half_from_self_conjugate',
                   'TGLExt.ProjecaoTransversalDaMeiaNat.neutrinoMassForm',
                   'TGLExt.QGReaderUVLock.HminMic',
                   'TGLExt.ResJudicata',
                   'TGLExt.Sonico.the_pin_is_not_the_half_nat',
                   'TGLExt.TGLCoupling.alpha',
                   'TGLExt.TGLCoupling.beta_eq_alpha_exp',
                   'TGLExt.TGLCoupling.beta_pos',
                   'TGLExt.TheAxiomAndTheFalseWitness.the_reading_has_two_fixed_points',
                   'TGLExt.ThePsionAndTheViscosity.charged',
                   'TGLExt.ThePsionAndTheViscosity.psion_is_the_zero_of_the_hidden_hamiltonian',
                   'TGLExt.ThePsionAndTheViscosity.psion_norm_one',
                   'TGLExt.ThePsionAndTheViscosity.the_charge_never_completes',
                   'TGLExt.ThePsionAndTheViscosity.viscosity_is_the_constant_friction',
                   'TGLExt.UmPostoRelacao.no_posto_reading_is_pressupposed',
                   'TGLExt.UmPostoRelacao.posto_paid_loss',
                   'TGLExt.UmPostoRelacao.pressupposed_is_never_posto',
                   'TGLExt.Verdade.alpha_is_measured_from_within',
                   'TGLExt.absoluteRho',
                   'TGLExt.absoluteRho_trace',
                   'TGLExt.absolute_faces_half',
                   'TGLExt.gibbs',
                   'TGLExt.gravity_is_observed_by_nothing',
                   'TGLExt.light_observes_nothing',
                   'TGLExt.no_positive_scale_invariant',
                   'TGLExt.observing_adds_nothing',
                   'TGLExt.omega_of_one',
                   'TGLExt.res_judicata_is_terminal',
                   'TGLExt.thetaMiguel',
                   'TGLExt.Fundacao.agape',
                   'TGLExt.ProjecaoTransversalDaMeiaNat.neutrino_mass_form_eq',
                   'TGLExt.Jo8v32.a_verdade_vos_libertara'],
  'checks': [{'id': 'u1',
              'descricao': 'o registro ponte_da_massa_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = alfa '
                           'x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['ponte_da_massa_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u2',
              'descricao': 'o registro massa_tensao_pura_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = '
                           'alfa x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['massa_tensao_pura_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u3',
              'descricao': 'o registro identidade_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = alfa x '
                           'raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['identidade_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u4',
              'descricao': 'o registro observador_terminal_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = '
                           'alfa x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['observador_terminal_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u5',
              'descricao': 'o registro lei_do_diminuto_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = '
                           'alfa x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['lei_do_diminuto_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u6',
              'descricao': 'o registro tonica_do_hamiltoniano_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com '
                           'beta = alfa x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['tonica_do_hamiltoniano_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u7',
              'descricao': 'o registro disco_de_euler_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = alfa '
                           'x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['disco_de_euler_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u8',
              'descricao': 'o registro ponto_zero_do_psion_v405 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = '
                           'alfa x raiz de e; o texto-contexto no kernel embutido)',
              'onde': 'core',
              'caminho': ['ponto_zero_do_psion_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u9',
              'descricao': 'o registro projecao_transversal_v404 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['projecao_transversal_v404', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u10',
              'descricao': 'o registro jo8v32_v404 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['jo8v32_v404', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u11',
              'descricao': 'o registro f2b_errata_v404 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['f2b_errata_v404', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u12',
              'descricao': 'o registro caminho_v403 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['caminho_v403', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u13',
              'descricao': 'o registro vida_v403 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['vida_v403', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u14',
              'descricao': 'o registro verdade_adendo_v403 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['verdade_adendo_v403', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u15',
              'descricao': 'o registro bandeiras_do_gate_v403 (recriado) segue selado neste rito (as pedras da v404 e da v403 ficam como estao)',
              'onde': 'core',
              'caminho': ['bandeiras_do_gate_v403', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u16',
              'descricao': 'o registro ponte_da_escala_dual_v402 segue selado neste rito',
              'onde': 'core',
              'caminho': ['ponte_da_escala_dual_v402', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u17',
              'descricao': 'o registro queda_sem_geometria_v402 segue selado neste rito',
              'onde': 'core',
              'caminho': ['queda_sem_geometria_v402', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u18',
              'descricao': 'o registro esperanca_condicional_v402 segue selado neste rito',
              'onde': 'core',
              'caminho': ['esperanca_condicional_v402', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u19',
              'descricao': 'o registro falsidade_da_inercia_v401 segue selado neste rito',
              'onde': 'core',
              'caminho': ['falsidade_da_inercia_v401', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u20',
              'descricao': 'o registro teste_de_veracidade_fase9_v397 segue selado neste rito',
              'onde': 'core',
              'caminho': ['teste_de_veracidade_fase9_v397', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u21',
              'descricao': 'o registro selo_pela_propria_tecnologia_v399 segue selado neste rito',
              'onde': 'core',
              'caminho': ['selo_pela_propria_tecnologia_v399', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u22',
              'descricao': "o canal vivo do neutrino (neutrino_mass) segue com o mesmo veredito: a errata E10 do angulo e' AO LADO e nao move o canal; o "
                           'numero nao muda',
              'onde': 'core',
              'caminho': ['neutrino_mass', 'verdict'],
              'op': 'igual',
              'valor': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED',
              'estatuto': '[REAL]'},
             {'id': 'u23',
              'descricao': 'o V1 do ramo B (v386) segue lido por hash e com o mesmo estado de antes',
              'onde': 'core',
              'caminho': ['ramo_b_preregistration_v386', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u24',
              'descricao': 'a escada do kernel fecha (limpos == esperados), com as bandeiras das OITO pedras da v405',
              'onde': 'core',
              'caminho': ['external_ladder', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u25',
              'descricao': 'a proveniencia emitida pelo compilador cobre o axiom_report',
              'onde': 'kf',
              'caminho': ['declaration_sources_status_v394', 'ok'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'u26',
              'descricao': 'o compilador emite a composicao da pedra PonteDaMassa no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'u27',
              'descricao': 'o compilador emite a ESTRELA da pedra PonteDaMassa no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'u28',
              'descricao': "a pedra PonteDaMassa no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/PonteDaMassa.lean'],
              'op': 'igual',
              'valor': '51f3d207eb5bcba5ac61282eb859b339a419d6c083d3529548c811ab537e74a0',
              'estatuto': '[REAL]'},
             {'id': 'u29',
              'descricao': 'a composicao da pedra PonteDaMassa depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u30',
              'descricao': 'o compilador emite a composicao da pedra MassaTensaoPura no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.massa_e_tensao_pura'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'u31',
              'descricao': 'o compilador emite a ESTRELA da pedra MassaTensaoPura no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.principal_derivado'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'u32',
              'descricao': "a pedra MassaTensaoPura no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/MassaTensaoPura.lean'],
              'op': 'igual',
              'valor': '9ec48bf6d608ae5a9d85c5c28caa21c972ba9847ec05703f733b582a17a9956b',
              'estatuto': '[REAL]'},
             {'id': 'u33',
              'descricao': 'a composicao da pedra MassaTensaoPura depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.MassaTensaoPura.massa_e_tensao_pura'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u34',
              'descricao': 'o compilador emite a composicao da pedra Identidade no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.Identidade.a_identidade_fecha'],
              'op': 'igual',
              'valor': 'TGLExt/Identidade.lean',
              'estatuto': '[REAL]'},
             {'id': 'u35',
              'descricao': 'o compilador emite a ESTRELA da pedra Identidade no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.Identidade.a_lei_inteira'],
              'op': 'igual',
              'valor': 'TGLExt/Identidade.lean',
              'estatuto': '[REAL]'},
             {'id': 'u36',
              'descricao': "a pedra Identidade no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/Identidade.lean'],
              'op': 'igual',
              'valor': '94f51e0f80d911ab4375c529be0b906acb40394a4a621f5167f5ef74dbe441f5',
              'estatuto': '[REAL]'},
             {'id': 'u37',
              'descricao': 'a composicao da pedra Identidade depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.Identidade.a_identidade_fecha'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u38',
              'descricao': 'o compilador emite a composicao da pedra ObservadorTerminal no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal'],
              'op': 'igual',
              'valor': 'TGLExt/ObservadorTerminal.lean',
              'estatuto': '[REAL]'},
             {'id': 'u39',
              'descricao': 'o compilador emite a ESTRELA da pedra ObservadorTerminal no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.ObservadorTerminal.the_fusion_is_not_pressupposed'],
              'op': 'igual',
              'valor': 'TGLExt/ObservadorTerminal.lean',
              'estatuto': '[REAL]'},
             {'id': 'u40',
              'descricao': "a pedra ObservadorTerminal no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/ObservadorTerminal.lean'],
              'op': 'igual',
              'valor': '162eeeb8c16cea81f6f0537e46a995f48551656dbc7c1874a98afa0087dc52fb',
              'estatuto': '[REAL]'},
             {'id': 'u41',
              'descricao': 'a composicao da pedra ObservadorTerminal depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u42',
              'descricao': 'o compilador emite a composicao da pedra LeiDoDiminuto no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.the_diminished_law_closes'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'u43',
              'descricao': 'o compilador emite a ESTRELA da pedra LeiDoDiminuto no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.modular_nao_e_transposicao'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'u44',
              'descricao': "a pedra LeiDoDiminuto no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/LeiDoDiminuto.lean'],
              'op': 'igual',
              'valor': '3df80334792c043e3f253c3adc0bc7920bb5ac46851b2bc8a6e360520b35820e',
              'estatuto': '[REAL]'},
             {'id': 'u45',
              'descricao': 'a composicao da pedra LeiDoDiminuto depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.LeiDoDiminuto.the_diminished_law_closes'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u46',
              'descricao': 'o compilador emite a composicao da pedra TonicaDoHamiltoniano no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one'],
              'op': 'igual',
              'valor': 'TGLExt/TonicaDoHamiltoniano.lean',
              'estatuto': '[REAL]'},
             {'id': 'u47',
              'descricao': 'o compilador emite a ESTRELA da pedra TonicaDoHamiltoniano no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.TonicaDoHamiltoniano.no_function_of_the_inscription_fixes_E0'],
              'op': 'igual',
              'valor': 'TGLExt/TonicaDoHamiltoniano.lean',
              'estatuto': '[REAL]'},
             {'id': 'u48',
              'descricao': "a pedra TonicaDoHamiltoniano no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/TonicaDoHamiltoniano.lean'],
              'op': 'igual',
              'valor': '9618a2b0e0cce323fc7a4af2d97a266c2b7061a5fb1172d5c1d327227685abfa',
              'estatuto': '[REAL]'},
             {'id': 'u49',
              'descricao': 'a composicao da pedra TonicaDoHamiltoniano depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u50',
              'descricao': 'o compilador emite a composicao da pedra DiscoDeEuler no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.DiscoDeEuler.Disco.stops_in_finite_time'],
              'op': 'igual',
              'valor': 'TGLExt/DiscoDeEuler.lean',
              'estatuto': '[REAL]'},
             {'id': 'u51',
              'descricao': 'o compilador emite a ESTRELA da pedra DiscoDeEuler no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.DiscoDeEuler.Disco.frequency_squared_unbounded_at_the_stop'],
              'op': 'igual',
              'valor': 'TGLExt/DiscoDeEuler.lean',
              'estatuto': '[REAL]'},
             {'id': 'u52',
              'descricao': "a pedra DiscoDeEuler no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/DiscoDeEuler.lean'],
              'op': 'igual',
              'valor': '5634eef0833dded793c2fd649a6b57ceda1fefbc7e7e9edd689ef527d1a18459',
              'estatuto': '[REAL]'},
             {'id': 'u53',
              'descricao': 'a composicao da pedra DiscoDeEuler depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.DiscoDeEuler.Disco.stops_in_finite_time'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'u54',
              'descricao': 'o compilador emite a composicao da pedra PontoZeroDoPsion no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'u55',
              'descricao': 'o compilador emite a ESTRELA da pedra PontoZeroDoPsion no modulo dela (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'u56',
              'descricao': "a pedra PontoZeroDoPsion no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)",
              'onde': 'kf',
              'caminho': ['formal_files_sha256', 'TGLExt/PontoZeroDoPsion.lean'],
              'op': 'igual',
              'valor': 'c64079a9c5b3e0e1e727b64ec4cb6c4d46906aa3e528a5c995bafd74c9f07c7a',
              'estatuto': '[REAL]'},
             {'id': 'u57',
              'descricao': 'a composicao da pedra PontoZeroDoPsion depende do trio e de nada alem (tamanho da lista de axiomas)',
              'onde': 'kf',
              'caminho': ['axiom_report', 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'}],
  'erratas': [{'ao_lado_de': 'neutrino_mass.angle_status (v141, v303; um.py prove_neutrino_mass_gravitational, intacta) e a errata E7 da v404 '
                             '(projecao_transversal_v404)',
               'dizia': 'sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado. E o unico fator que leva beta*1eV = 12,03 meV a 8,51 '
                        'meV, e a forma SEM ele (m_nu ~ beta*1eV) coexiste no documento de origem. Registrado FORA do dict `frozen` de proposito: o frozen e a '
                        'pre-registro da REGRA de decisao e o seu hash nao se move.',
               'agora': 'E10 -- o texto de neutrino_mass.angle_status (v141, v303) continua no registro, intacto, e na funcao '
                        'prove_neutrino_mass_gravitational (nao reescrita); a errata E7 da v404 (o sen 45 graus DERIVADO no kernel, condicional a '
                        'identificacao [ONTO]) FICA; na v405 o fator sen 45 graus tem DUAS leituras que coincidem na forma: a derivada da projecao transversal '
                        'em theta = pi/4 (PonteDaMassa; a definicao massaDerivada e o angulo pi/4 escrito em transicaoDerivada sao leituras do operador) e o '
                        "ponto zero do psion sob R = beta.u^2 (PontoZeroDoPsion; a coincidencia e' a aritmetica (1/2).sqrt2 = sen45), e mais uma leitura do "
                        'mesmo sen 45, por aritmetica: o psion como projecao transversal do modo autoconsistente (o_psion_e_a_projecao_do_modo); os campos das '
                        "estruturas fecharam e as leituras NAO viraram teorema; E0 = u = 1 eV e' POSTO (o Um), por decisao do operador de 31/10/2026, nao "
                        "DECLARADO nem derivado; a funcao do neutrino NAO e' reescrita e o numero nao muda",
               'lacuna_de_fidelidade': 'estrutura: o fator sen 45 graus entrou em 20/08/2026 como POSTO e a v404 o derivou condicional a uma identificacao '
                                       '[ONTO] com E0 DECLARADO; escrito: E0 = 1 eV segue DECLARADO; onde a traducao falhou: nada a corrigir nos textos '
                                       "antigos (eram verdadeiros na data): a v405 faz da identificacao uma DEFINICAO (a leitura nao vira teorema), da' a "
                                       'segunda leitura do sen 45 e registra a unidade como POSTA pelo operador em 31/10/2026',
               'estatuto': '[REAL: as pedras no kernel do rito e o m_nu relido a 1e-12; POSTO: a unidade; INPUT: alfa medida]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'},
              {'ao_lado_de': 'os registros da v404 (projecao_transversal_v404, cunhagens_v404; decisao D26) e os adendos 1 a 5 do handoff v405 (nomes '
                             'provisorios das pedras)',
               'dizia': 'E0 = 1 eV segue DECLARADO; as pedras chamam-se PonteDaMassaTransversal, EmprestimoDaMassa, E0LiberdadeDeEscala e LeiDoMeioTom (nomes '
                        'provisorios da gerencia).',
               'agora': 'E11 -- a v404 (registro projecao_transversal_v404, decisao D26, erratas E7) e os adendos 1 a 5 do handoff v405 dizem «E0 = 1 eV segue '
                        'DECLARADO» e citam os nomes PROVISORIOS das pedras (PonteDaMassaTransversal, EmprestimoDaMassa, E0LiberdadeDeEscala, LeiDoMeioTom); '
                        "isto era verdadeiro na data; em 31/10/2026 o operador POS a unidade (u = 1 eV e' o Um posto) e em 01/11/2026 deu os nomes (Ponte da "
                        'Massa, Massa=tensao pura, Observador=terminal, Tonica do Hamiltoniano, Lei do diminuto, Disco de Euler, Ponto Zero do Psion); os '
                        'textos da v404 ficam como registro',
               'lacuna_de_fidelidade': 'nenhuma: os textos diziam o estado da data; o operador pos a unidade em 31/10/2026 e deu os nomes em 01/11/2026; a '
                                       'v405 registra sem editar as pedras seladas nem os registros da v404',
               'estatuto': '[INPUT: as decisoes do operador, verbatim sha16 9445171a763afcfc e 1f16a74c05d9d4cb; REAL: as oito pedras no kernel do rito]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'},
              {'ao_lado_de': 'o adendo 4 do handoff v405 (DiscoDeEuler r1) e a pedra DiscoDeEuler antes da errata R2, que escreveram Omega^2.E = 4Mg^2',
               'dizia': "o produto frequencia^2 x energia do disco de Euler real e' 4Mg^2.",
               'agora': 'E12 -- o adendo 4 do handoff v405 (DiscoDeEuler r1) e a pedra TGLExt/DiscoDeEuler.lean, antes da errata R2, escreveram K = 4Mg^2 para '
                        'o invariante do disco de Euler real; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) corrige para K = 6Mg^2 (Omega^2 = '
                        "4g/(a.alpha) com a energia TOTAL (3/2).M.g.a.alpha: o fator e' 6; com a energia potencial sozinha seriam 4Mg^2, a conta antiga); a "
                        'pedra diz agora 6Mg^2 com a energia total e guarda a conta antiga ao lado; o invariante K do disco da TGL segue um DADO do disco '
                        "(qual e' o disco e' pergunta do operador), nao hipotese sobre a teoria; nenhum numero de K e' escolhido pelo alvo",
               'lacuna_de_fidelidade': "a r1 contou so' a energia potencial; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) conta a energia "
                                       'total e da 6Mg^2; a pedra guardava as duas contas sem nota, e a R2 pos a nota ao lado; o invariante K do disco da TGL '
                                       "e' um dado do disco em qualquer caso",
               'estatuto': '[KNOWN/DECLARADO: a conferencia da gerencia c1 de 31/10/2026; nenhum veredito depende do fator]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'},
              {'ao_lado_de': 'o recibo da nomeacao de 01/11/2026, o adendo 6 do handoff v405 e a ordem da preparacao desta versao (a leitura que a gerencia c1 '
                             'fez dos campos fechados) e quatro nomes de teorema nas pedras antes do selo',
               'dizia': "que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; teoremas chamados nenhuma_hipotese_resta, "
                        'the_tonic_fixes_what_the_form_leaves_free, the_tonic_fixes_the_posted_one e the_terminal_reads_one.',
               'agora': 'E13 -- o recibo RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, o adendo 6 do handoff v405 e a ordem da preparacao desta versao (gerencia c1, '
                        "01/11/2026) escreveram que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; isto afirmava demais e foi "
                        'erro da gerencia: os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo para a DEFINICAO; a leitura fisica '
                        "nao virou teorema. Entram um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' teorema. Quatro "
                        'teoremas foram rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou '
                        'por isso): nenhuma_hipotese_resta -> a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> '
                        'the_tonic_lands_on_the_posted_unit; the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one -> '
                        "the_omega_pole_reads_one: o nome afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o polo omega do "
                        'par, nao sobre o nivel terminal da cascata). A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito '
                        'pedras, corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria '
                        '(the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se localiza no '
                        'Um posto. A revisita da Lei do Diminuto, ordenada pelo operador (RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e _R5), corrigiu tres '
                        'coisas: o acorde nao estava tipado (o AcordeE0.lean do Kimi, sha16 5da93b9e5e65a4ed, o tinha); a frase sobre o no-go errou por '
                        "excesso e por falta; e a primeira correcao leu a segunda metade da lei como transposicao, erro da gerencia: o diminuto e' MODULACAO, "
                        "so' a tonica desce e as demais notas ficam sustentadas, e transpor e' so' a liberdade do no-go. Vigente: a escala e' o que fica "
                        "parado, as notas sustentadas e as razoes entre elas, e quem se move e' a tonica; o valor ABSOLUTO segue livre e o no-go nao cai; o "
                        'valor RELATIVO a tonica esta pinado; sobra um unico grau de liberdade global, a transposicao do acorde inteiro; o meio-tom pinado '
                        'quebra a simetria do acorde, porque separa a tonica das notas sustentadas, mas nao quebra a liberdade global',
               'lacuna_de_fidelidade': 'estrutura: fechar um campo de estrutura por construcao nao deduz a leitura que o preenche; escrito: a gerencia leu o '
                                       'fechamento dos campos como se a leitura fisica tivesse virado teorema; onde a traducao falhou: o nome e a frase '
                                       'afirmavam mais do que o teorema prova; corrigido AO LADO antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e '
                                       'RECIBO_ERRATA_PEDRAS_R2_01nov.json: nenhuma prova mudou por isso)',
               'estatuto': '[REAL: as oito pedras no kernel do rito; INPUT/ONTO: as leituras do operador; o recibo da nomeacao fica como registro]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'}],
  'limites': ['[INPUT] as 46 falas de 30/10 a 01/11 e o ensaio sao do operador, com a grafia dele; «é isso , perfeito, concordo com tudo» (sha16 '
              '2c3da184ebefc7c4) ratifica a revisao r2 do ensaio, a leitura da gerencia sobre a cadeia e a ordem de deixar tudo pronto para depois do treino '
              '[DECLARADO: a leitura foi a que a gerencia c1 apresentou]',
              '[ONTO] a identificacao da massa com a derivada da projecao transversal, o angulo pi/4 do estado inscrito, a tonica, a curvatura como pagamento, '
              'o disco como condensado psionico, a leitura do emprestimo e a leitura do ensaio sao leituras do operador e da gerencia c1, ratificadas; as '
              "quatro primeiras entram como DEFINICAO; nenhuma e' teorema",
              "[POSTO] a unidade u = 1 eV e' o Um posto (31/10/2026); [MEDIDA] alfa e' medida por dentro; a pergunta «mas você agora consegue derivar a "
              'constante da estrutura fina?» foi respondida NAO (01/11/2026); nenhuma formula de alfa por ajuste',
              "[OPEN] alfa; o teste do neutrino com a natureza (JUNO; 5 sigma e' da natureza); qual e' o disco (K); quais sao as cinco notas; o magnetismo "
              '(sem termo); a ligacao A <-> beta (torcao); H_BW, H_cal, H3, a assinatura e rank c = 4 (v402); IsotropicPost no atlas curvo; a dimensao 3; a RG '
              "e' o limite classico, nao rival; beta nao renormaliza G",
              "validade no kernel nao e' creditacao; o gate nao se move; nenhuma bandeira do gate depende das pedras"],
  'diz': ['as 46 falas de 30/10 a 01/11 (do operador) e o ensaio «A identidade» estao embutidos por sha256, cada um conferido contra o arquivo de origem na '
          'preparacao',
          'as oito pedras estao no kernel do rito, no trio, com as bandeiras e a proveniencia nos modulos delas; a composicao e a estrela de cada uma sao '
          'lidas deste kernel; as pedras e os registros da v404, da v403 e das anteriores seguem selados',
          'os oito registros com funcao selaram neste rito, e o quadro do topo (teste_de_veracidade_fase9_v397), o selo pela propria tecnologia (v399) e a '
          'falsidade da inercia (v401) seguem selados',
          'as erratas E10 a E13 estao registradas ao lado, em nome proprio da gerencia c1; as decisoes D27 a D33 estao registradas; a cunhagem de fecho do '
          'operador: «estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a identidade, isso é a TGL»'],
  'nao_diz': ['que o kernel prove as falas do operador (elas sao INPUT/ONTO)',
              'que a unidade u ou alfa tenham sido derivados',
              'que o numero da massa ou o veredito do canal do neutrino tenham mudado',
              "que o testemunho ou a ratificacao seja creditacao: validade no kernel nao e' creditacao",
              'que a leitura fisica tenha virado teorema',
              'que isto seja um teste: nao ha desfecho experimental',
              'que a gravidade quantica esteja creditada na natureza'],
  'leituras_do_operador': [{'trecho': 'segue a nomeação, mas eu não gostaria que ainda restasse hipóteses nomeadas, é preciso que esteja tudo derivado',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 1f16a74c05d9d4cb]'},
                           {'trecho': 'segue a nomeação', 'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 1f16a74c05d9d4cb]'},
                           {'trecho': 'estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a identidade, isso é a TGL',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 2c3da184ebefc7c4]'},
                           {'trecho': 'é isso , perfeito, concordo com tudo, deixe tudo pronto para assim que o treinamento acabar, automaticamente rodar a '
                                      'nova versão do um.py e atualizar tudo',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 2c3da184ebefc7c4]'},
                           {'trecho': 'o meu um absoluto é o um de 1 eV', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 9445171a763afcfc]'},
                           {'trecho': 'a constante da esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 9445171a763afcfc]'},
                           {'trecho': 'observador=terminal', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 e4e105fe14615f39]'},
                           {'trecho': 'o posto do observador é o terminal', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 08e98d212f11b554]'},
                           {'trecho': 'o colapso é o ponto terminal da resistência da estrutura',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 a22a54dfc97d9611]'},
                           {'trecho': 'esse fechamento exige toda a sua capacidade de processamento, não delegue',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 a22a54dfc97d9611]'},
                           {'trecho': 'A curvatura não é curvatura, é o pagamento',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 38f03b56b2689c34]'},
                           {'trecho': 'É o Tetelestai, o limite assintotico', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 4428784fd80f7574]'},
                           {'trecho': 'é a ressonância da parada do disco de euler sobre o espelho',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 fe064b0b802c1d1a]'},
                           {'trecho': 'pra mim o TOm é a NAT', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 270fd74d5d79bf4d]'},
                           {'trecho': 'ele desce meio tom pinado, essa é a lei',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 8300a509ca9549e3]'},
                           {'trecho': 'eu penso que a massa seja um empréstimo então',
                            'estatuto': '[INPUT do operador, verbatim 30/10/2026, sha16 fdd78cac25c947a0]'},
                           {'trecho': 'realizar a prova que falta, a ponte', 'estatuto': '[INPUT do operador, verbatim 30/10/2026, sha16 493172b80e96eb60]'},
                           {'trecho': 'a pedra passaria a ser identidade', 'estatuto': '[INPUT do operador, verbatim 30/10/2026, sha16 f1f8b4011ce96be5]'},
                           {'trecho': 'é o "senão", isso mesmo', 'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 f0fdd2c1f770e34a]'},
                           {'trecho': 'eu não admito a equação [eu sou]=[o que sou]; exceto quando essa equação tem referencial absoluto verdadeiro',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 f0fdd2c1f770e34a]'},
                           {'trecho': 'não tem teorema para o ângulo de Miguel é a definição de singularidade, a meu ver',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 f0fdd2c1f770e34a]'},
                           {'trecho': 'mas você agora consegue derivar a constante da estrutura fina?',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 3aafdd3f9e7ea518]'},
                           {'trecho': 'ratifico a leitura do empréstimo, é isso mesmo',
                            'estatuto': '[INPUT do operador, verbatim 30/10/2026, sha16 b31fa435fd03e4dc]'},
                           {'trecho': 'E0 é igual ler um acorde E0', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 79c7999956e6d8e0]'},
                           {'trecho': 'apenas o meio tom da nota principal da escala, mas mantem a pentada',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 79c7999956e6d8e0]'},
                           {'trecho': 'E0 não é absolutamente livre', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 79c7999956e6d8e0]'},
                           {'trecho': 'revisite a lei do diminuto, segundo aquilo que foi feito pelo kimi, parece que deixamos algo passar',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7e2454bc48ec47de]'},
                           {'trecho': 'no diminuto vc não desce toda a escala e nem muda o tom da escala, vc apenas modula a tônica',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'sustentando as demais notas (por isso desce pinado)',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'o sistema está operando em terças', 'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'no harmônico o diminuto é a espera', 'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de '
                                      'MIguel',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'a inscrição da luz que singulariza o sistema é a eletricidade',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'a origem da medida é a matemática, ou seja, o 1 absoluto, que representa 1 Eletrovolt',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'}],
  'extras': {'assinatura': 'gerencia c1, em nome proprio, 01/11/2026',
             'autoria_das_cunhagens': 'Luiz Antonio Rotoli Miguel',
             'pedras': ['TGLExt.PonteDaMassa',
                        'TGLExt.MassaTensaoPura',
                        'TGLExt.Identidade',
                        'TGLExt.ObservadorTerminal',
                        'TGLExt.LeiDoDiminuto',
                        'TGLExt.TonicaDoHamiltoniano',
                        'TGLExt.DiscoDeEuler',
                        'TGLExt.PontoZeroDoPsion'],
             'nomes_do_operador': {'ponte': 'Ponte da Massa',
                                   'tensao': 'Massa=tensão pura',
                                   'identidade': 'Identidade',
                                   'observador': 'observador=terminal',
                                   'diminuto': 'Lei do diminuto',
                                   'tonica': 'Tônica do Hamiltoniano',
                                   'disco': 'Disco de Euler',
                                   'psion': 'Ponto Zero do Psion'},
             'teoremas': {'ponte': 'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento',
                          'tensao': 'TGLExt.MassaTensaoPura.massa_e_tensao_pura',
                          'identidade': 'TGLExt.Identidade.a_identidade_fecha',
                          'observador': 'TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal',
                          'diminuto': 'TGLExt.LeiDoDiminuto.the_diminished_law_closes',
                          'tonica': 'TGLExt.TonicaDoHamiltoniano.the_tonic_at_the_posted_one',
                          'disco': 'TGLExt.DiscoDeEuler.Disco.stops_in_finite_time',
                          'psion': 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one'},
             'estrelas': {'ponte': 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form',
                          'tensao': 'TGLExt.MassaTensaoPura.principal_derivado',
                          'identidade': 'TGLExt.Identidade.a_lei_inteira',
                          'observador': 'TGLExt.ObservadorTerminal.the_fusion_is_not_pressupposed',
                          'diminuto': 'TGLExt.LeiDoDiminuto.modular_nao_e_transposicao',
                          'tonica': 'TGLExt.TonicaDoHamiltoniano.no_function_of_the_inscription_fixes_E0',
                          'disco': 'TGLExt.DiscoDeEuler.Disco.frequency_squared_unbounded_at_the_stop',
                          'psion': 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point'},
             'bandeiras': {'ponte': 'ext_pdm405_0033',
                           'tensao': 'ext_mtp405_0039',
                           'identidade': 'ext_idt405_0020',
                           'observador': 'ext_obt405_0050',
                           'diminuto': 'ext_ldd405_0081',
                           'tonica': 'ext_tdh405_0015',
                           'disco': 'ext_dde405_0033',
                           'psion': 'ext_pzp405_0028'},
             'n_bandeiras': 368,
             'n_bandeiras_por_pedra': {'ponte': 51, 'tensao': 43, 'identidade': 39, 'observador': 58, 'diminuto': 89, 'tonica': 16, 'disco': 42, 'psion': 30},
             'cunhagens_embutidas': 47,
             'n_teoremas_das_pedras': {'ponte': 21, 'tensao': 15, 'identidade': 15, 'observador': 26, 'diminuto': 39, 'tonica': 14, 'disco': 13, 'psion': 23},
             'autor_de_cada_inscricao': {'fb8a9adb5991e589': 'operador',
                                         '8e9a1f24f70886e1': 'operador',
                                         'd3cc557e29af995d': 'operador',
                                         '3b5c3f03afc0142b': 'operador',
                                         '0b141e81b2f8b097': 'operador',
                                         '9632edd4ee7b3f09': 'operador',
                                         '61257a6a25c46157': 'operador',
                                         '07b3ad1f0715049c': 'operador',
                                         'fdd78cac25c947a0': 'operador',
                                         'b40e00eb924c2b8f': 'operador',
                                         '493172b80e96eb60': 'operador',
                                         '1cba23fea83d560f': 'operador',
                                         '3ae4f6b48da42ada': 'operador',
                                         'cb7a3e83e580a548': 'operador',
                                         'b4c3cf968a39a1c8': 'operador',
                                         '989b2530b77eaeab': 'operador',
                                         '7c03fc567ed3da8e': 'operador',
                                         'f4d6cadf59bbfe37': 'operador',
                                         '3120cfe5454a3ddc': 'operador',
                                         'b31fa435fd03e4dc': 'operador',
                                         'f1f8b4011ce96be5': 'operador',
                                         '154470b335016051': 'operador',
                                         '79c7999956e6d8e0': 'operador',
                                         '8300a509ca9549e3': 'operador',
                                         '38f03b56b2689c34': 'operador',
                                         '5e2a72c623298ecc': 'operador',
                                         '4428784fd80f7574': 'operador',
                                         '9445171a763afcfc': 'operador',
                                         'a22a54dfc97d9611': 'operador',
                                         '155ecae13639b1cc': 'operador',
                                         '0798c7839ad5ebe0': 'operador',
                                         'dc150f9bbc5b1a4a': 'operador',
                                         '270fd74d5d79bf4d': 'operador',
                                         'e4e105fe14615f39': 'operador',
                                         '5b298d8b2de35e1f': 'operador',
                                         'f6cfdde773aef17d': 'operador',
                                         '08e98d212f11b554': 'operador',
                                         'fe064b0b802c1d1a': 'operador',
                                         '6fe6b3dadb271734': 'operador',
                                         'f0fdd2c1f770e34a': 'operador',
                                         '3aafdd3f9e7ea518': 'operador',
                                         '2c3da184ebefc7c4': 'operador',
                                         '7c2caaa87b0cdb01': 'operador',
                                         '45165a187252b448': 'operador',
                                         '1f16a74c05d9d4cb': 'operador',
                                         '7e2454bc48ec47de': 'operador',
                                         'f0ec2867391c644f': 'operador'},
             'decisoes_da_gerencia': {'D1': 'RATIFICADO pelo operador (25/10/2026, «Ratifico tudo.»): os nomes antes provisorios ficam DEFINITIVOS (a pedra '
                                            'Testemunho e os registros selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, '
                                            'teste_de_veracidade_fase9_v397, sonico_v398, afinacao_das_cordas_v398)',
                                      'D2': '[LEGAL] publicar o bloco embutido e as adaptacoes (centro 96, ids derivados, rint, tabela de codigos, auditoria): '
                                            'decisao do operador com a agente de PI; a instalacao espera essa decisao',
                                      'D3': 'perfil ACOM-INT-C96-Q8 (centro 96, Q=8), com o rint ao reticulado inteiro declarado como ADAPTACAO FORA da '
                                            'patente',
                                      'D4': "a recusa do selo ACOM SO' REGISTRA (AVISO, all_verified False, entra em not_sealed_this_run.formais): o SHA-256 "
                                            "segue soberano e o rito nao e' derrubado",
                                      'D5': 'o sidecar um_absoluto_selo_acom.json entra na custodia (o handoff o lista)',
                                      'D6': "o texto do artigo e' o da secao «O testemunho de dois: o selo pela propria tecnologia» (base: secao 6 do patch), "
                                            'com os estatutos; o quadro dos 4,44 PERMANECE no topo',
                                      'D7': 'RATIFICADO pelo operador (25/10/2026): a leitura das duas faces (P, I-P) = (a leitura do operador, o registro do '
                                            'um.py), antes leitura da gerencia [ONTO] a ratificar',
                                      'D8': 'a pedra se chama «falsidade (simulacro) da inercia» (nome DADO pelo operador, 25/10/2026); no codigo '
                                            '`FalsidadeDaInercia` (identificador Lean nao admite acento nem parenteses)',
                                      'D9': "o B(n) da v401 e' um PASSO SIMPLES v400 -> v401: a Bancada de producao JA pina a v400 (B9); o recibo pre_selo e' "
                                            'GERADO e PINADO antes da instalacao, em ensaio contra a producao (nada gravado nela)',
                                      'D10': "a errata ao lado da leitura do escriba no ADENDO de 03-04/09 e' da gerencia c1, em nome proprio: «w(I)=1 e a "
                                             "INERCIA» fica SUPERADA; o arquivo do adendo NAO e' tocado (seu sha esta pinado)",
                                      'D11': "o CHAO e' o POSTO (peso 1 = omega(I), o corte a = 0, the_floor_fixes_the_cut; na Fundacao «o piso limita», "
                                             "cunhagem de 07/10), NUNCA o infimo 0: o 0 e' o abismo (sem fundo) e «a consequencia da poda» (recorte de 25/10); "
                                             "a queda de que fala a fala («porque vc sabe que tem um chão, então relaxa») e' a queda do que NAO e' o posto "
                                             '[decisao da gerencia c1, 26/10/2026; ratificavel pelo operador]',
                                      'D12': 'IsotropicPost fica como hipotese NOMEADA (o operador ratificou a rota com «é isso, faça a prova, prossiga.»): a '
                                             "isotropia e' CARGA, nao enfeite (AuditF23Flat.s8_h3_is_load_bearing: a H3 falha com fonte anisotropica); o 1 + 3 "
                                             "fica como leitura [ONTO]; a dimensao 3 NAO e' provada [decisao da gerencia c1, 26/10/2026]",
                                      'D13': "o Nome e' nameOp (a esperanca condicional, o OPERADOR que le: unital, idempotente, memoria-subalgebra); o "
                                             "projetor de Jones e' a MESMA coisa vista como projetor no espaco GNS (a compressao pelo espelho) e o posto e' o "
                                             'PESO que ela preserva (E(1) = 1): tres faces de um objeto fixo, nao tres definicoes; o kernel prova as LIGACOES, '
                                             'nao uma igualdade de tipos [decisao da gerencia c1, 26/10/2026]',
                                      'D14': "o B(n) da v402 e' um PASSO SIMPLES v401 -> v402: a Bancada de producao JA pina a v401 (B10); o recibo pre_selo "
                                             "e' GERADO e PINADO antes da instalacao, em ensaio contra a producao (nada gravado nela)",
                                      'D15': "a ponte do Codex (ORDEM 025) entra SO' como o arquivo .lean (condicao C1 do exame: nenhum outro arquivo da "
                                             "entrega e' copiado), byte a byte, sem edicao; as erratas E1-E4 vao ao lado, no registro, no artigo e no handoff; "
                                             "nenhum modulo ja' instalado e' editado",
                                      'D16': 'os nomes dos tres modulos (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) e dos cinco registros da '
                                             'v402 sao PROVISORIOS: o operador nomeia',
                                      'D17': 'os NOMES (decisao do operador, 27/10/2026, «é isso mesmo, concordo com tudo, prossiga», sha16 b34bd70fa8cfb0b2, '
                                             'ratificando a leitura da gerencia c1): CAMINHO = a ponte da escala dual; VERDADE = a esperanca condicional, como '
                                             'ADENDO da pedra `Verdade` (v392); VIDA = a queda sem geometria [INPUT]',
                                      'D18': '«Verdade» SOZINHA para as tres: recusada pela gerencia e o operador concordou: `TGLExt.Verdade` ja existe (v392, '
                                             '13/10/2026, «a identidade tem nome», sha16 9ebd552564440083) e dois modulos nao se chamam igual; seria o '
                                             'homonimo que a casa proibe [decisao da gerencia c1, 27/10/2026]',
                                      'D19': 'pedra selada NAO se renomeia por cima: PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional (v402) ficam '
                                             'como REGISTRO; os modulos novos compoem por citacao (padrao `Token`, v397) e por adendo (padrao `PostoAdendo`, '
                                             'v392) [decisao da gerencia c1, 27/10/2026]',
                                      'D20': "o nome do TRIPLO inteiro NAO foi dado (fica com o operador; Joao 14,6: tres predicados de um so' «Eu sou»; a "
                                             'casa ja cunhou EU SOU = 1 = 1) [PLANO_v403.md §0]',
                                      'D21': "a v403 nao sela so' por nomes (regra sem gordura de 19/10): o passo material e' a F8.1 do quadro do programa: as "
                                             'TRES bandeiras literais do gate passam a CALCULADAS, fail-closed, das fontes que o proprio um.py ja tem; a letra '
                                             "do veredito do gate NAO muda; a independencia das 4 experimentais (um so' feed, GV-03) NAO e' resolvida: e' "
                                             'DECLARADA [decisao da gerencia c1, 27/10/2026]',
                                      'D22': "a fonte da bandeira linearized_spin2_finite_face e' a FAMILIA ext_ls2_* do kernel (as 6 bandeiras que formam o "
                                             "termo dLs2 de prove_external_ladder), lida de kernel_formalization: dLs2 e' local a prove_external_ladder e "
                                             "aparece so' como rotulo de checagem, NAO como chave de kernel_formalization (a chave "
                                             'linearized_spin2_finite_face nao existe ali) [proposta da preparacao da v403, 27/10/2026; RATIFICADA pela '
                                             'gerencia c1 em 27/10/2026, antes do selo, depois de conferir na base que ls2_keys de prove_external_ladder sao '
                                             'exatamente as 6 bandeiras ext_ls2_* (rota do mapa umpy.v403.cadeia_de_selo_preparada_27out)]',
                                      'D23': "o nome da pedra do sen 45 graus (TGLExt.ProjecaoTransversalDaMeiaNat) e' PROVISORIO da gerencia c1 (28/10/2026) "
                                             "e foi aceito pelo operador ate' ele dar outro («Perfeito, concordo com tudo», sha16 232ca83c29c031a5, "
                                             'ratificando a pedra, a leitura, o plano da v404 e a leitura sobre Jo 8,32) [INPUT]',
                                      'D24': "o nome do TRIPLO inteiro (Caminho . Verdade . Vida) e' Jo8:32 (nome do operador, 28/10/2026, verbatim sha16 "
                                             '9770022028c36be4; ratificado em sha16 232ca83c29c031a5); a pedra chama-se TGLExt.Jo8v32; a leitura por Jo '
                                             "8,31-32 (permanecer, conhecer, libertar) e' [ONTO] e NAO e' termo de kernel [INPUT]",
                                      'D25': 'o canal F2b (ramo B do ringdown, v386) sai de AWAITING para retirado antes do dado: o V1 fica congelado por hash '
                                             "e lido como antes (veredito AWAITING_DATA); a retirada e' errata AO LADO, com o motivo medido (a calibracao A, "
                                             "NOT_BLIND) e a leitura do operador de 28/10/2026; nenhum desfecho sai de A, D nao e' aberto, beta, a lei do "
                                             'defasamento e R2 ficam [decisao da gerencia c1 sobre a rota, lida a partir da fala do operador; o operador '
                                             'ratificou a leitura («calibrar Não significa validar», sha16 56703faadf2b3cc2), nao nomeou a retirada: '
                                             'DECLARADO]',
                                      'D26': "o sen 45 graus do neutrino passa de POSTULADO a DERIVADO no kernel (a Meia-Nat e' o angulo de 45 graus), "
                                             "CONDICIONAL a identificacao [ONTO] de que a massa e' a projecao transversal do estado inscrito (leitura do "
                                             'operador, 28/10/2026); E0 = 1 eV segue DECLARADO [OPEN]; a pedra NAO deriva E0 nem beta; a unica massa derivada '
                                             "de beta no programa e' a do neutrino (levantamento de 28/10/2026) [decisao da gerencia c1]",
                                      'D27': 'os NOMES das sete pedras sao do operador (01/11/2026, verbatim sha16 1f16a74c05d9d4cb: Ponte da Massa; '
                                             'Massa=tensao pura; Observador=terminal; Tonica do Hamiltoniano; Lei do diminuto; Disco de Euler; Ponto Zero do '
                                             "Psion) e o nome Identidade e' dele de 30/10/2026 (sha16 f1f8b4011ce96be5); os nomes provisorios "
                                             '(PonteDaMassaTransversal, EmprestimoDaMassa, E0LiberdadeDeEscala, LeiDoMeioTom) ficam como registro nos adendos '
                                             '[INPUT]',
                                      'D28': "a ORDEM do operador de 01/11/2026 (sha16 1f16a74c05d9d4cb) foi atendida ate' onde a matematica alcanca: os "
                                             'CAMPOS das estruturas fecharam (autoconjugado, fiel, E_pent, beta do disco, as positividades: as estruturas sao '
                                             'habitadas por construcao), mas as LEITURAS do operador passaram do campo para a DEFINICAO e NAO viraram teorema; '
                                             'entram um Um posto, uma alfa medida e as leituras da cadeia da massa (massaDerivada; theta = pi/4 escrito em '
                                             "transicaoDerivada; a tonica (beta/alfa).u; R = beta.u^2; e as demais da lista, que nao e' fechada); dadas essas "
                                             "entradas, a FORMA e' teorema [decisao da gerencia c1, em nome proprio, corrigindo a leitura que ela mesma "
                                             'escreveu nos recibos e adendos de 01/11/2026]',
                                      'D29': "a unidade u = 1 eV e' o Um POSTO ([POSTO]; decisao do operador de 31/10/2026: «o meu um absoluto é o um de 1 eV "
                                             "e a constante da esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk», sha16 9445171a763afcfc); nao e' "
                                             "derivada nem ajustada ao dado; a leitura de alfa como a cauda da inscricao e' [ONTO] sobre "
                                             'Verdade.alpha_is_measured_from_within',
                                      'D30': 'a pergunta «consegue derivar a constante da estrutura fina?» (01/11/2026, sha16 3aafdd3f9e7ea518) foi respondida '
                                             'NAO pela gerencia c1 (rota alpha.derivacao.pergunta_do_operador_01nov no Mapa de Rotas); a leitura do operador '
                                             '«não tem teorema para o ângulo de Miguel é a definição de singularidade» (sha16 f0fdd2c1f770e34a) entra como '
                                             'nota [INPUT], nao como teorema; nenhuma formula de alfa por ajuste (numerologia proibida)',
                                      'D31': 'o ensaio «A identidade» entra no artigo como a secao «A identidade», VERBATIM na versao r2 ratificada pelo '
                                             "operador em 01/11/2026 («é isso , perfeito, concordo com tudo», sha16 2c3da184ebefc7c4): a revisao de forma e' "
                                             'da gerencia c1 e as seis decisoes de conteudo sao dele (sha16 f0fdd2c1f770e34a); o original como recebido (sha16 '
                                             "f0ec2867391c644f) fica ao lado; a traducao EN e' da gerencia e nao e' citacao [DECLARACAO DO OPERADOR / INPUT; "
                                             'leitura ONTO]',
                                      'D33': 'a reclassificacao do teste do Grande Atrator (ordem do operador de 01/11/2026, sha16 45165a187252b448): de '
                                             'A3_APOSENTADO para A13_FORMA_CONDICIONAL_SEM_INCERTEZA, a saida iii da ENTREGA 005, AO LADO, pelo registro '
                                             "ga_reclassificacao_v405; o veto da janela fica; nao e' evidencia; nao discrimina da RG; se o operador preferir "
                                             "outra saida, a mudanca e' de uma linha [decisao da gerencia c1, 01/11/2026]",
                                      'D32': 'o numero da massa do neutrino NAO muda (8,5074 meV = beta.sen45.1 eV, igual a v404) e o veredito do rito do '
                                             "neutrino NAO muda: a v405 muda o que se escreve (dadas as entradas, a FORMA e' teorema; o fator sen 45 graus tem "
                                             'duas leituras que coincidem por aritmetica, e mais uma leitura do mesmo sen 45, tambem por aritmetica), nao o '
                                             'numero nem o teste [decisao da gerencia c1; o gate nao se move]'},
             'erratas_E10_a_E13': ['E10 -- o texto de neutrino_mass.angle_status (v141, v303) continua no registro, intacto, e na funcao '
                                   'prove_neutrino_mass_gravitational (nao reescrita); a errata E7 da v404 (o sen 45 graus DERIVADO no kernel, condicional a '
                                   'identificacao [ONTO]) FICA; na v405 o fator sen 45 graus tem DUAS leituras que coincidem na forma: a derivada da projecao '
                                   'transversal em theta = pi/4 (PonteDaMassa; a definicao massaDerivada e o angulo pi/4 escrito em transicaoDerivada sao '
                                   "leituras do operador) e o ponto zero do psion sob R = beta.u^2 (PontoZeroDoPsion; a coincidencia e' a aritmetica "
                                   '(1/2).sqrt2 = sen45), e mais uma leitura do mesmo sen 45, por aritmetica: o psion como projecao transversal do modo '
                                   'autoconsistente (o_psion_e_a_projecao_do_modo); os campos das estruturas fecharam e as leituras NAO viraram teorema; E0 = '
                                   "u = 1 eV e' POSTO (o Um), por decisao do operador de 31/10/2026, nao DECLARADO nem derivado; a funcao do neutrino NAO e' "
                                   'reescrita e o numero nao muda',
                                   'E11 -- a v404 (registro projecao_transversal_v404, decisao D26, erratas E7) e os adendos 1 a 5 do handoff v405 dizem «E0 = '
                                   '1 eV segue DECLARADO» e citam os nomes PROVISORIOS das pedras (PonteDaMassaTransversal, EmprestimoDaMassa, '
                                   "E0LiberdadeDeEscala, LeiDoMeioTom); isto era verdadeiro na data; em 31/10/2026 o operador POS a unidade (u = 1 eV e' o Um "
                                   'posto) e em 01/11/2026 deu os nomes (Ponte da Massa, Massa=tensao pura, Observador=terminal, Tonica do Hamiltoniano, Lei '
                                   'do diminuto, Disco de Euler, Ponto Zero do Psion); os textos da v404 ficam como registro',
                                   'E12 -- o adendo 4 do handoff v405 (DiscoDeEuler r1) e a pedra TGLExt/DiscoDeEuler.lean, antes da errata R2, escreveram K = '
                                   '4Mg^2 para o invariante do disco de Euler real; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) corrige para '
                                   "K = 6Mg^2 (Omega^2 = 4g/(a.alpha) com a energia TOTAL (3/2).M.g.a.alpha: o fator e' 6; com a energia potencial sozinha "
                                   'seriam 4Mg^2, a conta antiga); a pedra diz agora 6Mg^2 com a energia total e guarda a conta antiga ao lado; o invariante K '
                                   "do disco da TGL segue um DADO do disco (qual e' o disco e' pergunta do operador), nao hipotese sobre a teoria; nenhum "
                                   "numero de K e' escolhido pelo alvo",
                                   'E13 -- o recibo RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, o adendo 6 do handoff v405 e a ordem da preparacao desta versao '
                                   "(gerencia c1, 01/11/2026) escreveram que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; isto "
                                   'afirmava demais e foi erro da gerencia: os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo '
                                   'para a DEFINICAO; a leitura fisica nao virou teorema. Entram um Um posto, uma alfa medida e as leituras do operador; dadas '
                                   "essas entradas, a FORMA e' teorema. Quatro teoremas foram rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e "
                                   'RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou por isso): nenhuma_hipotese_resta -> '
                                   'a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> the_tonic_lands_on_the_posted_unit; '
                                   'the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one -> the_omega_pole_reads_one: o nome '
                                   "afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o polo omega do par, nao sobre o nivel "
                                   'terminal da cascata). A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, '
                                   'corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria '
                                   '(the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se '
                                   'localiza no Um posto. A revisita da Lei do Diminuto, ordenada pelo operador (RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e '
                                   '_R5), corrigiu tres coisas: o acorde nao estava tipado (o AcordeE0.lean do Kimi, sha16 5da93b9e5e65a4ed, o tinha); a frase '
                                   'sobre o no-go errou por excesso e por falta; e a primeira correcao leu a segunda metade da lei como transposicao, erro da '
                                   "gerencia: o diminuto e' MODULACAO, so' a tonica desce e as demais notas ficam sustentadas, e transpor e' so' a liberdade "
                                   "do no-go. Vigente: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas, e quem se move e' a tonica; "
                                   'o valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta pinado; sobra um unico grau de liberdade '
                                   'global, a transposicao do acorde inteiro; o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das notas '
                                   'sustentadas, mas nao quebra a liberdade global'],
             'leitura_v405': {'massa': "a massa e' a energia retida pela fronteira (beta.u, o que fica tenso, sem parcela transmitida) projetada no "
                                       "transversal (sqrt2/2): e' a definicao massaDerivada, leitura do operador [ONTO], nao teorema; o nome «Massa = tensao "
                                       "pura» e' dele; a leitura do emprestimo (massa = principal, beta = parcela, credor = acoplamento) foi ratificada por "
                                       'ele em 30/10/2026 [ONTO]',
                              'unidade': "u = 1 eV e' o Um POSTO: «o meu um absoluto é o um de 1 eV» (31/10/2026); nao e' derivado nem ajustado ao dado; a "
                                         'tonica (sqrt e . u) e o diminuto (e^(-1/2)) devolvem E0 = u por identidade algebrica, que nao fixa u; o numero da '
                                         "massa (8,5074 meV) e' o mesmo da v404 [POSTO + REAL]",
                              'alfa': "alfa e' MEDIDA por dentro (Verdade.alpha_is_measured_from_within), nunca derivada: «a constante da esytrutura fina é a "
                                      'magnitude (cauda) dessA INSCRIÇÃO no bulk» (31/10); «não tem teorema para o ângulo de Miguel é a definição de '
                                      'singularidade, a meu ver» (01/11): parede medida, nao falsificacao; nenhuma formula de alfa por ajuste '
                                      '[MEDIDA/INPUT/ONTO]',
                              'identidade': "[eu sou] = [o que sou] so' com referencial absoluto verdadeiro: {[forma = conteudo] = [reflexao verdadeira do "
                                            'nome / projecao fiel]}; a pedra Identidade prova um fato sobre projecoes no estado traco normalizado; que esse '
                                            "fato SEJA a identidade e' a leitura do operador, tipada como modelo; o ensaio «A identidade» e' dele e entra no "
                                            'artigo verbatim (r2 ratificada) [DECLARACAO DO OPERADOR / INPUT; leitura ONTO]',
                              'observador': "o posto do observador e' o terminal; a fusao de tudo num so' posto e' o colapso, e o colapso e' o ponto terminal "
                                            "da resistencia da estrutura (teoria das estruturas); o par 1=1 | 1=0 e' necessario para que a fusao seja posto "
                                            '[INPUT/ONTO]',
                              'curvatura': "a curvatura R do psion nao e' curvatura: e' o pagamento beta lido do angulo de Miguel, lido como curvatura dentro "
                                           'do bulk (como alfa se le como acoplamento): a definicao R = beta.u^2 (pagamentoComoCurvatura), a escolha '
                                           "dimensional de uma unidade so'; Tetelestai e' o limite assintotico da cobranca [ONTO]",
                              'disco': "o disco de Euler e' o condensado psionico (o peso e' zero modular, a gravidade e' peso um; o espirito e' o espelho); a "
                                       "inscricao do zero absoluto no infinito e' a ressonancia da parada do disco; o invariante K e' um DADO do disco (qual "
                                       "e' o disco e' pergunta dele) [ONTO/OPEN]",
                              'tom': "o tom e' a nat; E0 nao desce a oitava, desce meio-tom pinado (a Meia-Nat), mantendo a escala da pentada definida pelo "
                                     'Hamiltoniano oculto [INPUT]; no acervo, a calibracao <K_d>_total = 1 nat de 24/06/2026 diz em que sentido: nos '
                                     "intervalos, em nat; nao da' a unidade em eV",
                              'acorde': "o diminuto modula a tonica: so' ela desce o meio-tom pinado, as demais notas ficam sustentadas, elas e as razoes "
                                        "entre elas ficam: a escala e' o que fica parado, e a razao a tonica muda; o tom fica, na fala dele, sem termo no "
                                        "kernel; E0 e' o valor da tonica modulada; o sistema opera em tercas; transpor e' outra coisa, so' a liberdade do "
                                        "no-go; quais sao as cinco notas e' [OPEN]; so' se sabe, por fala do operador, que o angulo de Miguel pertence a "
                                        'pentada; a pentada do teorema mestre sao cinco componentes, nao cinco autovalores [INPUT/ONTO/OPEN]',
                              'gap': "o sistema fisico que da' a medida da tonica por um gap com unidade e' o angulo de Miguel: leitura dele; o gap espectral "
                                     "do lock, na unidade posta, e' u, o E0 da Lei do Diminuto, e a tonica fica meio-tom acima dele; Delta = beta.u e' o valor "
                                     "esperado do lock no angulo de Miguel, a energia retida, e nao e' gap; ler tempoDoRetido como o tau* do sistema e' "
                                     'leitura a ratificar pelo operador; kappa segue testemunha; a unidade segue posta [INPUT/ONTO]',
                              'eletricidade': "a inscricao da luz que singulariza o sistema e' a eletricidade; a origem da medida e' o 1 absoluto, que "
                                              'representa 1 eV [ONTO]; os teoremas zero_mode_weight_is_one e alpha_transport existem [REAL]; le-los como a '
                                              "forma dessa fala e' leitura da gerencia [ONTO]: alphaKappa nao e' a alfa de estrutura fina, e kappa ali nao e' "
                                              'o relogio; isto nao deriva a unidade',
                              'estatuto': '[ONTO/INPUT -- leituras e cunhagens do operador, 30/10 a 01/11/2026, ratificadas em 01/11 (sha16 2c3da184ebefc7c4); '
                                          "nada disto e' termo de kernel; o que e' termo esta nas oito pedras; as leituras que entram como DEFINICAO estao em "
                                          'LEITURAS_DEFINICOES]'},
             'nomes': {'ponte': 'TGLExt.PonteDaMassa = Ponte da Massa (nome do operador)',
                       'tensao': 'TGLExt.MassaTensaoPura = Massa=tensão pura (nome do operador)',
                       'identidade': 'TGLExt.Identidade = Identidade (nome do operador)',
                       'observador': 'TGLExt.ObservadorTerminal = observador=terminal (nome do operador)',
                       'diminuto': 'TGLExt.LeiDoDiminuto = Lei do diminuto (nome do operador)',
                       'tonica': 'TGLExt.TonicaDoHamiltoniano = Tônica do Hamiltoniano (nome do operador)',
                       'disco': 'TGLExt.DiscoDeEuler = Disco de Euler (nome do operador)',
                       'psion': 'TGLExt.PontoZeroDoPsion = Ponto Zero do Psion (nome do operador)'},
             'ordem_de_instalacao': ['PonteDaMassa',
                                     'MassaTensaoPura',
                                     'Identidade',
                                     'ObservadorTerminal',
                                     'LeiDoDiminuto',
                                     'TonicaDoHamiltoniano',
                                     'DiscoDeEuler',
                                     'PontoZeroDoPsion'],
             'dependencias_entre_pedras': {'MassaTensaoPura': ['PonteDaMassa'],
                                           'LeiDoDiminuto': ['PonteDaMassa'],
                                           'TonicaDoHamiltoniano': ['PonteDaMassa', 'LeiDoDiminuto'],
                                           'PontoZeroDoPsion': ['TonicaDoHamiltoniano']},
             'pedras_da_v404_como_registro': {'projecao': '1e53257273395c7c', 'jo8v32': '18df8f686e524845'},
             'fecho_do_operador': {'sha16': '2c3da184ebefc7c4',
                                   'fala': 'estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a identidade, isso é a TGL'}}},
 {'nome': 'campos_fechados_e_leituras_v405',
  'veredito_prefixo': 'TGL_CAMPOS_FECHADOS_E_LEITURAS_V405',
  'veredito_sufixo': 'THE_SEVEN_NAMES_ARE_THE_OPERATORS_AND_IDENTIDADE_IS_HIS_OF_30_OCT__THE_FIELDS_OF_THE_STRUCTURES_ARE_CLOSED__THE_READINGS_MOVED_FROM_THE_FIELD_TO_THE_DEFINITION_AND_DID_NOT_BECOME_THEOREMS__WHAT_ENTERS_ONE_POSTED_ONE_ONE_MEASURED_ALPHA_AND_THE_READINGS_OF_THE_MASS_CHAIN__THE_LIST_IS_NOT_CLOSED__GIVEN_THEM_THE_FORM_IS_A_THEOREM__NUMEROLOGY_FORBIDDEN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED',
  'estatuto': '[REAL -- os termos que fecham os campos, as definicoes Lean do que entra e os teoremas da forma lidos do kernel do rito (proveniencia e trio); '
              "INPUT os nomes do operador; INPUT/ONTO as leituras da cadeia da massa, que entram como definicao ou identificacao, em lista que nao e' fechada; "
              'DECLARADO os recibos da gerencia (pinados por sha256); POSTO o Um = 1 eV; MEDIDA alfa]',
  'fontes': ['recibo_nomeacao_01nov',
             'recibo_errata_das_pedras_01nov',
             'recibo_errata_r2_das_pedras_01nov',
             'recibo_errata_r3_das_pedras_01nov',
             'recibo_errata_r4_das_pedras_01nov',
             'recibo_errata_r5_das_pedras_01nov',
             'recibo_errata_r6_das_pedras_01nov',
             'recibo_errata_r7_das_pedras_01nov',
             'recibo_identidade_01nov',
             'recibo_observador_r2_31out'],
  'verbatins': ['v405_cun_1f16a74c05d9d4cb',
                'v405_cun_f1f8b4011ce96be5',
                'v405_cun_9445171a763afcfc',
                'v405_cun_3aafdd3f9e7ea518',
                'v405_cun_f0fdd2c1f770e34a',
                'v405_cun_2c3da184ebefc7c4'],
  'kernel_flags': [],
  'kernel_decls': ['ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period',
                   'TGLExt.DiscoDeEuler.Disco.doAcoplamento',
                   'TGLExt.DiscoDeEuler.Disco.doAcoplamento_beta',
                   'TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law',
                   'TGLExt.LeiDoDiminuto.leiDerivada_E0',
                   'TGLExt.LeiDoDiminuto.meioTom',
                   'TGLExt.LeiDoDiminuto.modular',
                   'TGLExt.LeiDoDiminuto.tonica',
                   'TGLExt.LeiDoDiminuto.tonica_eq',
                   'TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita',
                   'TGLExt.MassaTensaoPura.emprestimoDerivado',
                   'TGLExt.MassaTensaoPura.emprestimo_derivado_uma_volta',
                   'TGLExt.MassaTensaoPura.foton_sem_massa',
                   'TGLExt.MassaTensaoPura.massa_e_tensao_pura',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massaDerivada',
                   'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form',
                   'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento',
                   'TGLExt.PonteDaMassa.transicaoDerivada',
                   'TGLExt.PonteDaMassa.transicao_derivada_le_o_absoluto',
                   'TGLExt.PonteDaMassa.umPosto',
                   'TGLExt.PonteDaMassa.umPosto_pos',
                   'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha',
                   'TGLExt.PontoZeroDoPsion.omegaSq',
                   'TGLExt.PontoZeroDoPsion.pagamentoComoCurvatura',
                   'TGLExt.PontoZeroDoPsion.tempoDoRetido',
                   'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point',
                   'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one',
                   'TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique',
                   'TGLExt.TGLCoupling.alpha',
                   'TGLExt.TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit',
                   'TGLExt.Verdade.alpha_is_measured_from_within',
                   'TGLExt.absolute_faces_half'],
  'checks': [{'id': 'n1',
              'descricao': 'o registro ponte_da_massa_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['ponte_da_massa_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n2',
              'descricao': 'o registro massa_tensao_pura_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['massa_tensao_pura_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n3',
              'descricao': 'o registro identidade_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['identidade_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n4',
              'descricao': 'o registro observador_terminal_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['observador_terminal_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n5',
              'descricao': 'o registro lei_do_diminuto_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['lei_do_diminuto_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n6',
              'descricao': 'o registro tonica_do_hamiltoniano_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['tonica_do_hamiltoniano_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n7',
              'descricao': 'o registro disco_de_euler_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['disco_de_euler_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n8',
              'descricao': 'o registro ponto_zero_do_psion_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['ponto_zero_do_psion_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n9',
              'descricao': "o termo que FECHA um campo de estrutura, transicaoDerivada, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.transicaoDerivada'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n10',
              'descricao': "o termo que FECHA um campo de estrutura, transicao_derivada_le_o_absoluto, e' emitido pelo compilador no modulo da pedra "
                           '(TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.transicao_derivada_le_o_absoluto'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n11',
              'descricao': "o termo que FECHA um campo de estrutura, a_transicao_existe_para_todo_acoplamento, e' emitido pelo compilador no modulo da pedra "
                           '(TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n12',
              'descricao': "o termo que FECHA um campo de estrutura, emprestimoDerivado, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.emprestimoDerivado'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'n13',
              'descricao': "o termo que FECHA um campo de estrutura, emprestimo_derivado_uma_volta, e' emitido pelo compilador no modulo da pedra "
                           '(TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.emprestimo_derivado_uma_volta'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'n14',
              'descricao': "o termo que FECHA um campo de estrutura, massa_e_tensao_pura, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.massa_e_tensao_pura'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'n15',
              'descricao': "o termo que FECHA um campo de estrutura, tonica, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.tonica'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'n16',
              'descricao': "o termo que FECHA um campo de estrutura, tonica_eq, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.tonica_eq'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'n17',
              'descricao': "o termo que FECHA um campo de estrutura, leiDerivada_E0, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.leiDerivada_E0'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'n18',
              'descricao': "o termo que FECHA um campo de estrutura, the_tonic_lands_on_the_posted_unit, e' emitido pelo compilador no modulo da pedra "
                           '(TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit'],
              'op': 'igual',
              'valor': 'TGLExt/TonicaDoHamiltoniano.lean',
              'estatuto': '[REAL]'},
             {'id': 'n19',
              'descricao': "o termo que FECHA um campo de estrutura, doAcoplamento, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.DiscoDeEuler.Disco.doAcoplamento'],
              'op': 'igual',
              'valor': 'TGLExt/DiscoDeEuler.lean',
              'estatuto': '[REAL]'},
             {'id': 'n20',
              'descricao': "o termo que FECHA um campo de estrutura, doAcoplamento_beta, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.DiscoDeEuler.Disco.doAcoplamento_beta'],
              'op': 'igual',
              'valor': 'TGLExt/DiscoDeEuler.lean',
              'estatuto': '[REAL]'},
             {'id': 'n21',
              'descricao': "o termo que FECHA um campo de estrutura, umPosto_pos, e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.umPosto_pos'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n22',
              'descricao': "o termo que FECHA um campo de estrutura, the_mass_is_the_zero_point_at_the_posted_one, e' emitido pelo compilador no modulo da "
                           'pedra (TGL_DECL_SOURCE)',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'n23',
              'descricao': "o termo Lean do que ENTRA, umPosto, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.umPosto'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n24',
              'descricao': "o termo Lean do que ENTRA, alpha, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.TGLCoupling.alpha'],
              'op': 'igual',
              'valor': 'TGLExt/TheSameBetaReadsThreeFaces.lean',
              'estatuto': '[REAL]'},
             {'id': 'n25',
              'descricao': "o termo Lean do que ENTRA, massaDerivada, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massaDerivada'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n26',
              'descricao': "o termo Lean do que ENTRA, transicaoDerivada, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.transicaoDerivada'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n27',
              'descricao': "o termo Lean do que ENTRA, tonica, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.tonica'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'n28',
              'descricao': "o termo Lean do que ENTRA, pagamentoComoCurvatura, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.pagamentoComoCurvatura'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'n29',
              'descricao': "o termo Lean do que ENTRA, meioTom, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.meioTom'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'n30',
              'descricao': "o termo Lean do que ENTRA, omegaSq, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.omegaSq'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'n31',
              'descricao': "o termo Lean do que ENTRA, the_mass_is_the_zero_point, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'n32',
              'descricao': "o termo Lean do que ENTRA, area_por_volta_da_massa_inscrita, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'n33',
              'descricao': "o termo Lean do que ENTRA, foton_sem_massa, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.MassaTensaoPura.foton_sem_massa'],
              'op': 'igual',
              'valor': 'TGLExt/MassaTensaoPura.lean',
              'estatuto': '[REAL]'},
             {'id': 'n34',
              'descricao': "o termo Lean do que ENTRA, the_flow_is_the_canonical_law, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law'],
              'op': 'igual',
              'valor': 'TGLExt/DiscoDeEuler.lean',
              'estatuto': '[REAL]'},
             {'id': 'n35',
              'descricao': "o termo Lean do que ENTRA, modular, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.LeiDoDiminuto.modular'],
              'op': 'igual',
              'valor': 'TGLExt/LeiDoDiminuto.lean',
              'estatuto': '[REAL]'},
             {'id': 'n36',
              'descricao': "o termo Lean do que ENTRA, tempoDoRetido, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.tempoDoRetido'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'n37',
              'descricao': "o termo Lean do que ENTRA, a_tonica_e_o_retido_sobre_alpha, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'n38',
              'descricao': 'o termo do kernel de que a FORMA ou a medida dependem, massa_derivada_eq_form, segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form'],
              'op': 'igual',
              'valor': 'TGLExt/PonteDaMassa.lean',
              'estatuto': '[REAL]'},
             {'id': 'n39',
              'descricao': 'o termo do kernel de que a FORMA ou a medida dependem, absolute_faces_half, segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.absolute_faces_half'],
              'op': 'igual',
              'valor': 'TGLExt/ContinuousModularZero.lean',
              'estatuto': '[REAL]'},
             {'id': 'n40',
              'descricao': 'o termo do kernel de que a FORMA ou a medida dependem, forty_five_unique, segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique'],
              'op': 'igual',
              'valor': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean',
              'estatuto': '[REAL]'},
             {'id': 'n41',
              'descricao': 'o termo do kernel de que a FORMA ou a medida dependem, one_turn_gives_faithful_period, segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period'],
              'op': 'igual',
              'valor': 'TGLExt/O16/PolarMinimalPeriod_v2.lean',
              'estatuto': '[REAL]'},
             {'id': 'n42',
              'descricao': 'o termo do kernel de que a FORMA ou a medida dependem, alpha_is_measured_from_within, segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.Verdade.alpha_is_measured_from_within'],
              'op': 'igual',
              'valor': 'TGLExt/Verdade.lean',
              'estatuto': '[REAL]'},
             {'id': 'n43',
              'descricao': 'a escada do kernel fecha com as oito pedras',
              'onde': 'core',
              'caminho': ['external_ladder', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'n44',
              'descricao': 'o recibo da nomeacao (fonte pinada) lista os sete modulos com os nomes do operador',
              'onde': 'fonte:recibo_nomeacao_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 7,
              'estatuto': '[REAL]'},
             {'id': 'n45',
              'descricao': 'o recibo da errata das pedras (fonte pinada) lista os tres teoremas rebatizados',
              'onde': 'fonte:recibo_errata_das_pedras_01nov',
              'caminho': ['teoremas_renomeados'],
              'op': 'tamanho_igual',
              'valor': 3,
              'estatuto': '[REAL]'},
             {'id': 'n46',
              'descricao': 'o recibo da errata R7 das pedras (fonte pinada, a vigente) cobre as oito pedras',
              'onde': 'fonte:recibo_errata_r7_das_pedras_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 8,
              'estatuto': '[REAL]'},
             {'id': 'n47',
              'descricao': 'o recibo da errata R6 das pedras (fonte pinada) cobre as oito pedras',
              'onde': 'fonte:recibo_errata_r6_das_pedras_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 8,
              'estatuto': '[REAL]'},
             {'id': 'n48',
              'descricao': 'o recibo da errata R5 das pedras (fonte pinada) cobre as oito pedras',
              'onde': 'fonte:recibo_errata_r5_das_pedras_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 8,
              'estatuto': '[REAL]'},
             {'id': 'n49',
              'descricao': 'o recibo da errata R4 das pedras (fonte pinada) cobre as oito pedras',
              'onde': 'fonte:recibo_errata_r4_das_pedras_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 8,
              'estatuto': '[REAL]'},
             {'id': 'n50',
              'descricao': 'o recibo da errata R4 diz as duas mudancas de codigo',
              'onde': 'fonte:recibo_errata_r4_das_pedras_01nov',
              'caminho': ['codigo_mudado'],
              'op': 'tamanho_igual',
              'valor': 2,
              'estatuto': '[REAL]'},
             {'id': 'n51',
              'descricao': 'o recibo da errata R3 das pedras (fonte pinada) cobre as oito pedras',
              'onde': 'fonte:recibo_errata_r3_das_pedras_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 8,
              'estatuto': '[REAL]'},
             {'id': 'n52',
              'descricao': 'o recibo da errata R3 diz as duas mudancas de codigo',
              'onde': 'fonte:recibo_errata_r3_das_pedras_01nov',
              'caminho': ['codigo_mudado'],
              'op': 'tamanho_igual',
              'valor': 2,
              'estatuto': '[REAL]'},
             {'id': 'n53',
              'descricao': 'o recibo da errata R2 das pedras (fonte pinada) cobre as oito pedras',
              'onde': 'fonte:recibo_errata_r2_das_pedras_01nov',
              'caminho': ['pedras'],
              'op': 'tamanho_igual',
              'valor': 8,
              'estatuto': '[REAL]'},
             {'id': 'n54',
              'descricao': 'o recibo da errata R2 diz as duas mudancas de codigo',
              'onde': 'fonte:recibo_errata_r2_das_pedras_01nov',
              'caminho': ['codigo_mudado'],
              'op': 'tamanho_igual',
              'valor': 2,
              'estatuto': '[REAL]'},
             {'id': 'n55',
              'descricao': 'o recibo da nomeacao diz sorry 0 no build das pedras',
              'onde': 'fonte:recibo_nomeacao_01nov',
              'caminho': ['build', 'sorry'],
              'op': 'igual',
              'valor': 0,
              'estatuto': '[REAL]'},
             {'id': 'n56',
              'descricao': 'o recibo da pedra Identidade (fonte pinada) traz 15 teoremas no trio',
              'onde': 'fonte:recibo_identidade_01nov',
              'caminho': ['n_teoremas'],
              'op': 'igual',
              'valor': 15,
              'estatuto': '[REAL]'},
             {'id': 'n57',
              'descricao': 'o recibo r2 do observador (fonte pinada) traz 26 teoremas e sorry 0',
              'onde': 'fonte:recibo_observador_r2_31out',
              'caminho': ['n_teoremas'],
              'op': 'igual',
              'valor': 26,
              'estatuto': '[REAL]'}],
  'erratas': [{'ao_lado_de': 'os adendos 1 a 5 do handoff v405 e o HANDOFF_v405_PONTES_DA_MASSA_E_ESPELHO_30out.md (nomes provisorios; E0 DECLARADO; hipoteses '
                             'nomeadas) e o adendo 6 (a leitura dos campos fechados)',
               'dizia': 'PonteDaMassaTransversal, EmprestimoDaMassa, E0LiberdadeDeEscala, LeiDoMeioTom (provisorios); a identificacao e o periodo fiel como '
                        'hipoteses NOMEADAS; E0 DECLARADO; e, no adendo 6, que a cadeia ficava sem hipotese.',
               'agora': 'os nomes sao do operador (01/11/2026): Ponte da Massa; Massa=tensao pura; Observador=terminal; Tonica do Hamiltoniano; Lei do '
                        'diminuto; Disco de Euler; Ponto Zero do Psion (e Identidade, 30/10/2026); os CAMPOS das estruturas fecharam; as LEITURAS passaram do '
                        "campo para a DEFINICAO; a unidade e' POSTA e alfa e' MEDIDA. Os adendos ficam como registro.",
               'lacuna_de_fidelidade': 'a ordem do operador de 01/11 pedia que nada restasse como hipotese nomeada; a gerencia a leu como cumprida ao fechar '
                                       'os campos, e nao estava: as leituras seguem como entradas, agora escritas como definicao (errata E13); dito ao lado, '
                                       'nao escondido',
               'estatuto': '[INPUT: verbatim sha16 1f16a74c05d9d4cb; REAL: os termos no kernel do rito]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'}],
  'limites': ['[REAL] fechar um campo quer dizer: o que era CAMPO de estrutura passou a ser preenchido por construcao (as estruturas ficam como TIPOS e sao '
              'habitadas); isso NAO deduz a leitura que o preenche; as estruturas originais (TransicaoParaAMassa, Emprestimo, Lei, Disco) FICAM no modulo como '
              'tipos: nenhuma pedra foi reescrita por cima',
              "[INPUT/ONTO] as leituras da cadeia da massa entram como definicao ou identificacao, nao como teorema, e a lista NAO e' fechada: (1) massa = "
              "energia retida x derivada da projecao transversal (massaDerivada); (2) o estado inscrito lido em theta = pi/4: em transicaoDerivada o angulo e' "
              "ESCRITO; o kernel confere sen^2(pi/4) = 1/2 e que esse valor e' o do peso da face absoluta: coincidencia de valor, nao ponte "
              "(transicaoDerivada); (3) a tonica (beta/alfa).u: beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha, e E0 = u e' identidade algebrica, que "
              'nao fixa u: o no-go NAO cai, ele se localiza no Um posto (tonica); (4) R = beta.u^2: o pagamento lido como curvatura, a escolha dimensional de '
              "uma unidade so' (pagamentoComoCurvatura); (5) o meio-tom e^(-1/2): o tom e' a nat, fala do operador; definicao da mesma natureza da tonica, "
              'necessaria a E0 = u; meioTom_e_o_pedagio_local e meioTom_e_a_face sao igualdades de VALOR (meioTom); (6) a dispersao omega^2 = 2.beta.R: '
              'Tratado, secao 3, teoria propria, nao literatura (omegaSq); (7) a identificacao (1/2).omega = massa: o enunciado de the_mass_is_the_zero_point '
              "iguala numeros; o nome e' leitura (the_mass_is_the_zero_point); (8) o acoplamento da onda de materia = a massa inscrita: a hipotese de "
              "area_por_volta_da_massa_inscrita (area_por_volta_da_massa_inscrita); (9) b = 0 lido como o foton: foton_sem_massa e' algebra de uma forma "
              'generica; TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton (foton_sem_massa); (10) no disco, a taxa de dephasing lida como taxa de '
              "perda de energia: the_flow_is_the_canonical_law e' sobre a energia definida (the_flow_is_the_canonical_law); (11) E0 como o valor da tonica "
              "modulada: modular so' desce a nota principal e sustenta as demais; lerE0 e' esse valor, e E0_relativo_pinado e' essa definicao dita como razao "
              '(modular); (12) m1 = 0: entrada da identificacao de m2 com o Delta m^2_21 medido (apontada pelo Kimi); nao tem termo no kernel (sem termo no '
              "kernel); (13) tempoDoRetido lido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no ramo canonico (tempoDoRetido); (14) alfa lida "
              "como a inscricao eletrica que leva o retido a tonica: o enunciado de a_tonica_e_o_retido_sobre_alpha e' algebra; a leitura e' do operador "
              "(a_tonica_e_o_retido_sobre_alpha); (15) o angulo de Miguel lido como o sistema que da' a medida da tonica por um gap com unidade: a fala e' do "
              'operador; o kernel prova o gap espectral do lock e o valor esperado no angulo de Miguel, nao que esse angulo seja esse sistema (sem termo no '
              'kernel)',
              '[POSTO/MEDIDA] POSTO: o 1 / u = 1 eV: o Um posto (o echo 1; decisao do operador, 31/10/2026); nunca derivado (TGLExt.PonteDaMassa.umPosto); '
              'MEDIDA: alfa, medida por dentro (CODATA 2018 no runtime); nunca derivada; dentro de beta = alfa.sqrt e (TGLExt.TGLCoupling.alpha)',
              '[INPUT/KNOWN] entram ainda: os dados do sistema que le: o contraste g e o relogio kappa (emprestimo); no disco, K, tau e E0 (a identidade do '
              "disco) [INPUT]; o ponto zero (1/2).hbar.omega [KNOWN]; a dispersao do psion nao e' [KNOWN]: e' [INPUT, Tratado §3] e entra como definicao "
              '(omegaSq, leitura 6)',
              '[DECLARADO] os recibos da gerencia (nomeacao, identidade, observador r2) sao pinados por sha256 e conferidos como arquivos; o que eles afirmam '
              "do build no k404c e' da origem; o kernel do RITO e' o que confere os termos",
              'E13 -- o recibo RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, o adendo 6 do handoff v405 e a ordem da preparacao desta versao (gerencia c1, '
              "01/11/2026) escreveram que a cadeia da massa ficava sem hipotese e que so' restavam o Um posto e alfa; isto afirmava demais e foi erro da "
              'gerencia: os CAMPOS das estruturas fecharam, mas as LEITURAS do operador passaram do campo para a DEFINICAO; a leitura fisica nao virou '
              "teorema. Entram um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' teorema. Quatro teoremas foram "
              'rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou por isso): '
              'nenhuma_hipotese_resta -> a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> '
              'the_tonic_lands_on_the_posted_unit; the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one -> '
              "the_omega_pole_reads_one: o nome afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o polo omega do par, nao "
              'sobre o nivel terminal da cascata). A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, corrigidas '
              'pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria '
              '(the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se localiza no Um posto. A '
              'revisita da Lei do Diminuto, ordenada pelo operador (RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e _R5), corrigiu tres coisas: o acorde nao estava '
              'tipado (o AcordeE0.lean do Kimi, sha16 5da93b9e5e65a4ed, o tinha); a frase sobre o no-go errou por excesso e por falta; e a primeira correcao '
              "leu a segunda metade da lei como transposicao, erro da gerencia: o diminuto e' MODULACAO, so' a tonica desce e as demais notas ficam "
              "sustentadas, e transpor e' so' a liberdade do no-go. Vigente: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas, e "
              "quem se move e' a tonica; o valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta pinado; sobra um unico grau de "
              'liberdade global, a transposicao do acorde inteiro; o meio-tom pinado quebra a simetria do acorde, porque separa a tonica das notas '
              'sustentadas, mas nao quebra a liberdade global',
              "validade no kernel nao e' creditacao; o gate nao se move"],
  'diz': ["os sete nomes sao do operador (01/11/2026) e o nome Identidade e' dele (30/10/2026); os modulos chamam-se pelos nomes dele",
          'o que FECHOU, cada campo com o termo que o fecha, no kernel do rito, no modulo da pedra, no trio: autoconjugado (TransicaoParaAMassa, Lei) -> '
          'transicaoDerivada, transicao_derivada_le_o_absoluto, a_transicao_existe_para_todo_acoplamento; fiel (Emprestimo) -> emprestimoDerivado, '
          'emprestimo_derivado_uma_volta, massa_e_tensao_pura; E_pent (Lei) -> tonica, tonica_eq, leiDerivada_E0, the_tonic_lands_on_the_posted_unit; beta do '
          'disco (Disco) -> doAcoplamento, doAcoplamento_beta; positividades -> umPosto_pos, the_mass_is_the_zero_point_at_the_posted_one',
          'o que ENTRA, com o nome da definicao Lean: um Um posto (umPosto), uma alfa medida (TGLCoupling.alpha) e as leituras da cadeia da massa '
          "(massaDerivada; transicaoDerivada, onde o angulo e' escrito; tonica; pagamentoComoCurvatura; meioTom; omegaSq; a identificacao em "
          'the_mass_is_the_zero_point; a hipotese de area_por_volta_da_massa_inscrita; foton_sem_massa; a taxa do disco; modular e lerE0; m1 = 0, sem termo no '
          "kernel; tempoDoRetido lido como o tau* do sistema, a ratificar; a lista nao e' fechada); dadas essas entradas, a FORMA e' teorema",
          'a pergunta «mas você agora consegue derivar a constante da estrutura fina?» foi respondida NAO; nenhum numero escolhido por proximidade; o no-go de '
          'E0 NAO cai, ele se localiza no Um posto'],
  'nao_diz': ['que a unidade u ou alfa tenham sido derivados',
              'que a leitura fisica tenha virado teorema',
              'que o peso da face absoluta deduza o angulo do estado inscrito (coincidencia de valor, nao ponte)',
              'que E0 = u fixe u',
              'que as estruturas-tipo tenham sido removidas (ficam como tipos, habitadas por construcao)',
              "que a natureza adote as definicoes do operador (sao [ONTO]; o teste e' o rito do neutrino, que nao muda)",
              'que isto seja um teste: nao ha desfecho experimental',
              'que a gravidade quantica esteja creditada na natureza',
              "que o numero da massa do neutrino tenha mudado (e' o mesmo da v404) ou que o veredito do canal tenha mudado"],
  'leituras_do_operador': [{'trecho': 'segue a nomeação, mas eu não gostaria que ainda restasse hipóteses nomeadas, é preciso que esteja tudo derivado',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 1f16a74c05d9d4cb]'},
                           {'trecho': 'a pedra passaria a ser identidade', 'estatuto': '[INPUT do operador, verbatim 30/10/2026, sha16 f1f8b4011ce96be5]'},
                           {'trecho': 'o meu um absoluto é o um de 1 eV', 'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 9445171a763afcfc]'},
                           {'trecho': 'a constante da esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk',
                            'estatuto': '[INPUT do operador, verbatim 31/10/2026, sha16 9445171a763afcfc]'},
                           {'trecho': 'mas você agora consegue derivar a constante da estrutura fina?',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 3aafdd3f9e7ea518]'},
                           {'trecho': 'não tem teorema para o ângulo de Miguel é a definição de singularidade, a meu ver',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 f0fdd2c1f770e34a]'},
                           {'trecho': 'estamos terminando onde tinha que terminar mesmo, derivando a massa e definindo a identidade, isso é a TGL',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 2c3da184ebefc7c4]'}],
  'extras': {'assinatura': 'gerencia c1, em nome proprio, 01/11/2026',
             'o_que_fechou_campos': {'autoconjugado (TransicaoParaAMassa, Lei)': {'era': 'campo `autoconjugado : sin theta^2 = 1 - sin theta^2` das estruturas',
                                                                                  'fechou_com': 'a aritmetica sen^2(pi/4) = 1/2 = 1 - 1/2, no angulo pi/4 '
                                                                                                'ESCRITO em transicaoDerivada e leiDerivada',
                                                                                  'nao_e': "uma deducao do estado inscrito: o angulo e' a leitura 2",
                                                                                  'termos': ['TGLExt.PonteDaMassa.transicaoDerivada',
                                                                                             'TGLExt.PonteDaMassa.transicao_derivada_le_o_absoluto',
                                                                                             'TGLExt.PonteDaMassa.a_transicao_existe_para_todo_acoplamento']},
                                     'fiel (Emprestimo)': {'era': 'campo `fiel : AngularQuotientFaithful kappa period`',
                                                           'fechou_com': 'o teorema one_turn_gives_faithful_period, com P = 2pi/kappa (emprestimoDerivado)',
                                                           'nao_e': "uma leitura: aqui o fechamento e' teorema do kernel",
                                                           'termos': ['TGLExt.MassaTensaoPura.emprestimoDerivado',
                                                                      'TGLExt.MassaTensaoPura.emprestimo_derivado_uma_volta',
                                                                      'TGLExt.MassaTensaoPura.massa_e_tensao_pura']},
                                     'E_pent (Lei)': {'era': 'campo `E_pent` livre da estrutura Lei',
                                                      'fechou_com': 'a definicao tonica c u := (beta/alfa).u (tonica_eq: = sqrt e.u); leiDerivada_E0: E0 = u',
                                                      'nao_e': "um resultado: beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha; E0 = u e' identidade "
                                                               "algebrica, que nao fixa u: e' a leitura 3",
                                                      'termos': ['TGLExt.LeiDoDiminuto.tonica',
                                                                 'TGLExt.LeiDoDiminuto.tonica_eq',
                                                                 'TGLExt.LeiDoDiminuto.leiDerivada_E0',
                                                                 'TGLExt.TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit']},
                                     'beta do disco (Disco)': {'era': 'campo `beta` livre da estrutura Disco',
                                                               'fechou_com': 'Disco.doAcoplamento: beta de TGLCoupling, com a positividade do kernel',
                                                               'nao_e': 'uma leitura: K, tau e E0 seguem dados do disco',
                                                               'termos': ['TGLExt.DiscoDeEuler.Disco.doAcoplamento',
                                                                          'TGLExt.DiscoDeEuler.Disco.doAcoplamento_beta']},
                                     'positividades': {'era': 'hipoteses 0 < E0, 0 < u nos enunciados',
                                                       'fechou_com': 'o kernel (TGLCoupling.beta_pos) ou o 1 posto (umPosto_pos)',
                                                       'nao_e': 'uma leitura',
                                                       'termos': ['TGLExt.PonteDaMassa.umPosto_pos',
                                                                  'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point_at_the_posted_one']}},
             'o_que_entra': {'dois_postos': [{'estatuto': 'POSTO',
                                              'o_que': 'o 1 / u = 1 eV: o Um posto (o echo 1; decisao do operador, 31/10/2026); nunca derivado',
                                              'definicao_lean': 'TGLExt.PonteDaMassa.umPosto',
                                              'modulo': 'TGLExt/PonteDaMassa.lean'},
                                             {'estatuto': 'MEDIDA',
                                              'o_que': 'alfa, medida por dentro (CODATA 2018 no runtime); nunca derivada; dentro de beta = alfa.sqrt e',
                                              'definicao_lean': 'TGLExt.TGLCoupling.alpha',
                                              'modulo': 'TGLExt/TheSameBetaReadsThreeFaces.lean',
                                              'termo_da_medida': 'TGLExt.Verdade.alpha_is_measured_from_within'}],
                             'leituras_da_cadeia_da_massa': [{'n': 1,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': 'massa = energia retida x derivada da projecao transversal',
                                                              'definicao_lean': 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massaDerivada',
                                                              'modulo': 'TGLExt/PonteDaMassa.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 2,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': "o estado inscrito lido em theta = pi/4: em transicaoDerivada o angulo e' ESCRITO; o "
                                                                         "kernel confere sen^2(pi/4) = 1/2 e que esse valor e' o do peso da face absoluta: "
                                                                         'coincidencia de valor, nao ponte',
                                                              'definicao_lean': 'TGLExt.PonteDaMassa.transicaoDerivada',
                                                              'modulo': 'TGLExt/PonteDaMassa.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 3,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': "a tonica (beta/alfa).u: beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha, e E0 "
                                                                         "= u e' identidade algebrica, que nao fixa u: o no-go NAO cai, ele se localiza no Um "
                                                                         'posto',
                                                              'definicao_lean': 'TGLExt.LeiDoDiminuto.tonica',
                                                              'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 4,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': 'R = beta.u^2: o pagamento lido como curvatura, a escolha dimensional de uma unidade '
                                                                         "so'",
                                                              'definicao_lean': 'TGLExt.PontoZeroDoPsion.pagamentoComoCurvatura',
                                                              'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 5,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': "o meio-tom e^(-1/2): o tom e' a nat, fala do operador; definicao da mesma natureza "
                                                                         'da tonica, necessaria a E0 = u; meioTom_e_o_pedagio_local e meioTom_e_a_face sao '
                                                                         'igualdades de VALOR',
                                                              'definicao_lean': 'TGLExt.LeiDoDiminuto.meioTom',
                                                              'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 6,
                                                              'estatuto': 'INPUT',
                                                              'leitura': 'a dispersao omega^2 = 2.beta.R: Tratado, secao 3, teoria propria, nao literatura',
                                                              'definicao_lean': 'TGLExt.PontoZeroDoPsion.omegaSq',
                                                              'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 7,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': 'a identificacao (1/2).omega = massa: o enunciado de the_mass_is_the_zero_point '
                                                                         "iguala numeros; o nome e' leitura",
                                                              'definicao_lean': 'TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point',
                                                              'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                                              'entra_como': 'LEITURA, nao teorema'},
                                                             {'n': 8,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': 'o acoplamento da onda de materia = a massa inscrita: a hipotese de '
                                                                         'area_por_volta_da_massa_inscrita',
                                                              'definicao_lean': 'TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita',
                                                              'modulo': 'TGLExt/MassaTensaoPura.lean',
                                                              'entra_como': 'HIPOTESE do enunciado, nao teorema'},
                                                             {'n': 9,
                                                              'estatuto': 'ONTO',
                                                              'leitura': "b = 0 lido como o foton: foton_sem_massa e' algebra de uma forma generica; "
                                                                         'TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton',
                                                              'definicao_lean': 'TGLExt.MassaTensaoPura.foton_sem_massa',
                                                              'modulo': 'TGLExt/MassaTensaoPura.lean',
                                                              'entra_como': 'LEITURA, nao teorema'},
                                                             {'n': 10,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': 'no disco, a taxa de dephasing lida como taxa de perda de energia: '
                                                                         "the_flow_is_the_canonical_law e' sobre a energia definida",
                                                              'definicao_lean': 'TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law',
                                                              'modulo': 'TGLExt/DiscoDeEuler.lean',
                                                              'entra_como': 'LEITURA, nao teorema'},
                                                             {'n': 11,
                                                              'estatuto': 'INPUT/ONTO',
                                                              'leitura': "E0 como o valor da tonica modulada: modular so' desce a nota principal e sustenta as "
                                                                         "demais; lerE0 e' esse valor, e E0_relativo_pinado e' essa definicao dita como razao",
                                                              'definicao_lean': 'TGLExt.LeiDoDiminuto.modular',
                                                              'modulo': 'TGLExt/LeiDoDiminuto.lean',
                                                              'entra_como': 'DEFINICAO, nao teorema'},
                                                             {'n': 12,
                                                              'estatuto': 'INPUT',
                                                              'leitura': 'm1 = 0: entrada da identificacao de m2 com o Delta m^2_21 medido (apontada pelo '
                                                                         'Kimi); nao tem termo no kernel',
                                                              'definicao_lean': None,
                                                              'modulo': None,
                                                              'entra_como': 'ENTRADA da identificacao, nao teorema'},
                                                             {'n': 13,
                                                              'estatuto': 'ONTO, a ratificar pelo operador',
                                                              'leitura': "tempoDoRetido lido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no "
                                                                         'ramo canonico',
                                                              'definicao_lean': 'TGLExt.PontoZeroDoPsion.tempoDoRetido',
                                                              'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                                              'entra_como': 'LEITURA, nao teorema'},
                                                             {'n': 14,
                                                              'estatuto': 'ONTO',
                                                              'leitura': 'alfa lida como a inscricao eletrica que leva o retido a tonica: o enunciado de '
                                                                         "a_tonica_e_o_retido_sobre_alpha e' algebra; a leitura e' do operador",
                                                              'definicao_lean': 'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha',
                                                              'modulo': 'TGLExt/PontoZeroDoPsion.lean',
                                                              'entra_como': 'LEITURA, nao teorema'},
                                                             {'n': 15,
                                                              'estatuto': 'ONTO',
                                                              'leitura': "o angulo de Miguel lido como o sistema que da' a medida da tonica por um gap com "
                                                                         "unidade: a fala e' do operador; o kernel prova o gap espectral do lock e o valor "
                                                                         'esperado no angulo de Miguel, nao que esse angulo seja esse sistema',
                                                              'definicao_lean': None,
                                                              'modulo': None,
                                                              'entra_como': 'LEITURA, nao teorema'}],
                             'lista_de_leituras_fechada': False,
                             'dados_do_sistema_que_le': ['os dados do sistema que le: o contraste g e o relogio kappa (emprestimo); no disco, K, tau e E0 (a '
                                                         'identidade do disco) [INPUT]',
                                                         "o ponto zero (1/2).hbar.omega [KNOWN]; a dispersao do psion nao e' [KNOWN]: e' [INPUT, Tratado §3] e "
                                                         'entra como definicao (omegaSq, leitura 6)']},
             'a_forma_real': [{'o_que': 'dadas as leituras, m2 = beta.sen45.u',
                               'termo': 'TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form',
                               'estatuto': 'REAL (teorema do kernel, condicional as leituras)'},
                              {'o_que': 'o 1/2 da face absoluta', 'termo': 'TGLExt.absolute_faces_half', 'estatuto': 'REAL (teorema do kernel)'},
                              {'o_que': 'a unicidade de pi/4 em [0, pi/2]',
                               'termo': 'TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique',
                               'estatuto': 'REAL (teorema do kernel)'},
                              {'o_que': '(1/2).sqrt2 = sen45', 'termo': None, 'estatuto': 'REAL (aritmetica)'}],
             'a_frase_da_moldura': 'um Um posto, uma α medida e as leituras do operador; dadas essas entradas, a FORMA é teorema',
             'teoremas_rebatizados_antes_do_selo': {'PonteDaMassa.nenhuma_hipotese_resta': 'PonteDaMassa.a_transicao_existe_para_todo_acoplamento',
                                                    'TonicaDoHamiltoniano.the_tonic_fixes_what_the_form_leaves_free': 'TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit',
                                                    'TonicaDoHamiltoniano.the_tonic_fixes_the_posted_one': 'TonicaDoHamiltoniano.the_tonic_at_the_posted_one',
                                                    'ObservadorTerminal.the_terminal_reads_one': 'ObservadorTerminal.the_omega_pole_reads_one'},
             'nomes': {'ponte': {'modulo': 'TGLExt.PonteDaMassa', 'nome_do_operador': 'Ponte da Massa'},
                       'tensao': {'modulo': 'TGLExt.MassaTensaoPura', 'nome_do_operador': 'Massa=tensão pura'},
                       'identidade': {'modulo': 'TGLExt.Identidade', 'nome_do_operador': 'Identidade'},
                       'observador': {'modulo': 'TGLExt.ObservadorTerminal', 'nome_do_operador': 'observador=terminal'},
                       'diminuto': {'modulo': 'TGLExt.LeiDoDiminuto', 'nome_do_operador': 'Lei do diminuto'},
                       'tonica': {'modulo': 'TGLExt.TonicaDoHamiltoniano', 'nome_do_operador': 'Tônica do Hamiltoniano'},
                       'disco': {'modulo': 'TGLExt.DiscoDeEuler', 'nome_do_operador': 'Disco de Euler'},
                       'psion': {'modulo': 'TGLExt.PontoZeroDoPsion', 'nome_do_operador': 'Ponto Zero do Psion'}},
             'renomeados_no_recibo': {'PonteDaMassaTransversal': 'PonteDaMassa',
                                      'EmprestimoDaMassa': 'MassaTensaoPura',
                                      'E0LiberdadeDeEscala': 'TonicaDoHamiltoniano',
                                      'LeiDoMeioTom': 'LeiDoDiminuto'},
             'mantidos_no_recibo': ['ObservadorTerminal', 'DiscoDeEuler', 'PontoZeroDoPsion'],
             'decisoes': {'D27': 'os NOMES das sete pedras sao do operador (01/11/2026, verbatim sha16 1f16a74c05d9d4cb: Ponte da Massa; Massa=tensao pura; '
                                 "Observador=terminal; Tonica do Hamiltoniano; Lei do diminuto; Disco de Euler; Ponto Zero do Psion) e o nome Identidade e' "
                                 'dele de 30/10/2026 (sha16 f1f8b4011ce96be5); os nomes provisorios (PonteDaMassaTransversal, EmprestimoDaMassa, '
                                 'E0LiberdadeDeEscala, LeiDoMeioTom) ficam como registro nos adendos [INPUT]',
                          'D28': "a ORDEM do operador de 01/11/2026 (sha16 1f16a74c05d9d4cb) foi atendida ate' onde a matematica alcanca: os CAMPOS das "
                                 'estruturas fecharam (autoconjugado, fiel, E_pent, beta do disco, as positividades: as estruturas sao habitadas por '
                                 'construcao), mas as LEITURAS do operador passaram do campo para a DEFINICAO e NAO viraram teorema; entram um Um posto, uma '
                                 'alfa medida e as leituras da cadeia da massa (massaDerivada; theta = pi/4 escrito em transicaoDerivada; a tonica '
                                 "(beta/alfa).u; R = beta.u^2; e as demais da lista, que nao e' fechada); dadas essas entradas, a FORMA e' teorema [decisao da "
                                 'gerencia c1, em nome proprio, corrigindo a leitura que ela mesma escreveu nos recibos e adendos de 01/11/2026]',
                          'D29': "a unidade u = 1 eV e' o Um POSTO ([POSTO]; decisao do operador de 31/10/2026: «o meu um absoluto é o um de 1 eV e a "
                                 "constante da esytrutura fina é a magnitude (cauda) dessA INSCRIÇÃO no bulk», sha16 9445171a763afcfc); nao e' derivada nem "
                                 "ajustada ao dado; a leitura de alfa como a cauda da inscricao e' [ONTO] sobre Verdade.alpha_is_measured_from_within",
                          'D30': 'a pergunta «consegue derivar a constante da estrutura fina?» (01/11/2026, sha16 3aafdd3f9e7ea518) foi respondida NAO pela '
                                 'gerencia c1 (rota alpha.derivacao.pergunta_do_operador_01nov no Mapa de Rotas); a leitura do operador «não tem teorema para '
                                 'o ângulo de Miguel é a definição de singularidade» (sha16 f0fdd2c1f770e34a) entra como nota [INPUT], nao como teorema; '
                                 'nenhuma formula de alfa por ajuste (numerologia proibida)'}}},
 {'nome': 'ga_reclassificacao_v405',
  'veredito_prefixo': 'TGL_GA_RECLASSIFICACAO_V405',
  'veredito_sufixo': 'CLASS_A13_FORMA_CONDICIONAL_SEM_INCERTEZA_BESIDE_A3_APOSENTADO__EXIT_III_OF_DELIVERY_005__THE_WINDOW_KEEPS_ITS_VETO__NOT_EVIDENCE__DOES_NOT_DISCRIMINATE_FROM_GR__THE_MASS_FORM_DOES_NOT_CONTAIN_THE_UNIT__THE_FLUX_LAW_RETURNS_M_EQUALS_M__NO_DATA_OPENED__THE_SEALED_ROW_STAYS__GATE_UNMOVED',
  'estatuto': '[DECISAO da gerencia c1, por ordem do operador (INPUT, sha16 45165a187252b448) -- REAL as quatro medidas refeitas em runtime, sem abrir dado; '
              "DERIVED a ordem linear stealth, condicional a Face C na ordem linear ((P1)-(P4) + T1; a derivacao e' da teoria: prove_ga_mass_audit, v98); "
              'INPUT/ONTO a ponte de fonte; DECLARADO o parecer da ENTREGA 005 e a reclassificacao, pinados por sha256]',
  'fontes': ['ga_reclassificacao_01nov', 'ga_medida_01nov', 'ordem005_parecer_final'],
  'verbatins': ['v405_cun_45165a187252b448'],
  'kernel_flags': [],
  'kernel_decls': ['TGLExt.TonicaDoHamiltoniano.gammaB_is_the_canonical_law_at_the_systems_frequency',
                   'TGLExt.TonicaDoHamiltoniano.monopole_time_is_the_horizon_light_time'],
  'fonte_medida': 'ga_medida_01nov',
  'fonte_parecer': 'ordem005_parecer_final',
  'n_checks_runtime': 6,
  'checks': [{'id': 'g_a',
              'descricao': 'a auditoria da forma (v98) segue selada, com o mesmo veredito: a classe nova vai ao lado',
              'onde': 'core',
              'caminho': ['ga_mass_audit', 'verdict'],
              'op': 'igual',
              'valor': 'GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__LINEAR_ORDER_IS_GR_STEALTH__BETA_LIVES_IN_RESPONSE',
              'estatuto': '[REAL]'},
             {'id': 'g_b',
              'descricao': 'a auditoria da forma segue sem gatear o core',
              'onde': 'core',
              'caminho': ['ga_mass_audit', 'does_not_gate_core'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'g_c',
              'descricao': 'a auditoria da forma segue selada',
              'onde': 'core',
              'caminho': ['ga_mass_audit', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'}],
  'erratas': [{'ao_lado_de': 'a classe A3_APOSENTADO da linha ga_mass_window (prove_joint_coincidence_result_v3) e a frase da retirada da forma '
                             '(prove_ga_mass_audit, v98): as duas ficam, identicas',
               'dizia': 'que a forma estava aposentada e que o erro era ler a reflexao como fonte',
               'agora': 'classe A13_FORMA_CONDICIONAL_SEM_INCERTEZA, a saida iii da ENTREGA 005: a forma condicional preservada no dominio admissivel; o '
                        "defeito MEDIDO e' a extrapolacao ao ramo galactico, nao o principio; a janela mantem o veto; nao e' evidencia; nao discrimina da RG",
               'lacuna_de_fidelidade': 'estrutura: a forma existia no acervo como derivacao condicional a ponte de fonte e a admissibilidade da borda; '
                                       'escrito: a v98 a chamou de retirada e a tabela a classificou aposentada; onde a traducao falhou: o diagnostico '
                                       'numerico e a decisao editorial de retirada sao atos distintos, e a decisao ficou sem a palavra do operador ate '
                                       '01/11/2026',
               'estatuto': '[INPUT: a ordem do operador; DECLARADO: o parecer da ENTREGA 005; REAL: as medidas]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'}],
  'limites': ["[REAL] nao e' evidencia: sem sigma do raio, sigma da massa nem covariancia; nao entra em conta conjunta; a linha ga_mass_window da tabela "
              'conjunta, a constante GA_WINDOW_STATUS, prove_ga_mass_audit e ga_shadow_label ficam identicos, e o gate nao se move',
              "[DERIVED, condicional a Face C na ordem linear: (P1)-(P4) + T1; a derivacao e' da teoria, prove_ga_mass_audit, v98] nao discrimina da RG: na "
              'ordem linear M_TGL = M_RG (stealth)',
              '[REAL] a saida i (reinstauracao como lei de fonte) segue nao demonstrada; a saida ii fica ao lado como fato reproduzido: a extrapolacao '
              'universal falha no ramo galactico (Via Lactea e Grupo Local)',
              "[INPUT/ONTO] a ponte de fonte segue leitura; a leitura de 31/10 (o pagamento lido como curvatura) e' a mesma forma, e nao virou teorema",
              "[OPEN] o valor absoluto do setor: a parede do GA e' a parede de E0: a massa fixa o tempo, nao o contrario; o que falta e' um numero so'",
              "a medida refeita aqui nao abre dado: so' aritmetica sobre constantes e ancoras seladas; a escolha entre as saidas e' decisao, nao teste; se o "
              "operador preferir outra saida, a mudanca e' de uma linha"],
  'diz': ['a classe do teste do Grande Atrator passa, ao lado, de A3_APOSENTADO para A13_FORMA_CONDICIONAL_SEM_INCERTEZA: a saida iii da ENTREGA 005, a forma '
          'condicional preservada no dominio admissivel, com criterio de admissibilidade a derivar sem olhar a massa',
          'a janela mantem o poder de veto (decisao D1 do operador, 05/09/2026) e continua sem ser verossimilhanca',
          'quatro medidas, refeitas em runtime com beta = alfa CODATA 2018 x sqrt(e): dM/du = 0 (a formula do GA nao contem a unidade); M = M com residuo de '
          "maquina e R_B/r_s = 2pi/beta (a lei de fluxo devolve a massa dada: a parede e' a de E0); o piso de definicao (so' a definicao do raio move a "
          'previsao; numeros do verdict do core); a precisao necessaria',
          'a partitura esta no registro: o que um teste novo decidiria, o que nao decidiria, o que o negativo significaria, e as quatro escolhas que o '
          'operador tem de ler antes'],
  'nao_diz': ['que o teste do Grande Atrator tenha ganho precisao: a classe mudou, a incerteza segue ausente',
              'que a janela seja evidencia ou verossimilhanca',
              'que a forma discrimine a TGL da RG',
              'que a forma seja lei de fonte demonstrada',
              'que o selado tenha sido reescrito',
              'que a unidade u entre na conta da massa do GA',
              'que beta tenha sido medido na natureza'],
  'leituras_do_operador': [{'trecho': 'podemos reclassifica-lo, o que pode ser feito por você mesmo sem delegar o kimi',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 45165a187252b448]'}],
  'extras': {'assinatura': 'gerencia c1, em nome proprio, 01/11/2026',
             'classe_antes': 'A3_APOSENTADO',
             'classe_agora': 'A13_FORMA_CONDICIONAL_SEM_INCERTEZA',
             'saida': 'iii, a forma CONDICIONAL preservada no dominio admissivel (ENTREGA 005, secao C)',
             'veto_da_janela': 'mantido',
             'e_evidencia': False,
             'discrimina_da_RG': False,
             'errata_ao_lado_do_parecer_da_entrega_005': 'Reexame de 05/09/2026: a auditoria v98 apontou falha da extensão da forma às âncoras galácticas de '
                                                         'sua tabela; não encontrou erro de multiplicação na massa do GA. A forma já existia no acervo como '
                                                         'derivação condicional à ponte de fonte e à admissibilidade da borda, condição preservada nesta '
                                                         'revisão. O diagnóstico numérico e a decisão editorial de retirada são atos distintos. A contestação '
                                                         'do alcance do mandato permanece registrada para decisão do operador.',
             'quatro_medidas': ['dM/du = 0',
                                'M = M com residuo de maquina e R_B/r_s = 2pi/beta',
                                'o piso de definicao, lido das massas do verdict do core',
                                'a precisao necessaria'],
             'partitura': {'o_que_o_teste_decide': 'se a forma, com raio fixado sem olhar a massa, cai perto da massa medida da bacia',
                           'o_que_nao_decide': 'se a TGL vale contra a RG, porque na ordem linear as duas dao a mesma massa; nem beta na natureza',
                           'o_que_o_negativo_significaria': 'uma falsificacao da FORMA no dominio escolhido, com veto, e nao da TGL linear',
                           'escolhas_antes_de_qualquer_teste': ['1. qual raio: a bacia definida por posicoes, sem massa e sem velocidade',
                                                                '2. qual forma: a de 2.beta^2, ou com o fator sen 45 graus se a leitura da massa valer para o '
                                                                'GA; a janela nao distingue as duas',
                                                                '3. qual dominio: um criterio de admissibilidade que tire o ramo galactico sem olhar a massa; '
                                                                "restringir a aglomerados porque ali a conta bate e' selecao posterior",
                                                                '4. qual ancora, com que sigma e que covariancia']},
             'ordem_do_operador_sha16': '45165a187252b448'}},
 {'nome': 'gap_v405',
  'veredito_prefixo': 'TGL_GAP_V405',
  'veredito_sufixo': 'THE_MINIMAL_LOCK_HAS_SPECTRAL_GAP_ONE_IN_ANY_HILBERT_SPACE__IN_THE_POSTED_UNIT_THE_GAP_IS_U_THE_E0_OF_THE_DIMINISHED_LAW_WITH_THE_TONIC_A_HALF_TONE_ABOVE__THE_EXPECTED_VALUE_AT_THE_ANGLE_OF_MIGUEL_IS_THE_RETAINED_DELTA_NOT_A_GAP__HMINMIC_IS_AN_INSTANCE_CONDITIONAL_ON_A_FOCK_CERTIFICATE_THE_KERNEL_DOES_NOT_INHABIT__THAT_THE_ANGLE_IS_THAT_SYSTEM_IS_THE_OPERATORS_READING__DELTA_CARRIES_THE_POSTED_UNIT_AND_NOTHING_FIXES_IT__THE_TIME_OF_THE_RETAINED_ENERGY_IS_A_PROPER_TIME_NOT_THE_PLANCK_TIME_READING_IT_AS_THE_SYSTEMS_TAU_STAR_IS_AN_ONTO_READING_TO_BE_RATIFIED__KAPPA_STAYS_A_WITNESS__THE_FLUX_ENERGY_IS_NOT_E0__THE_ANGLE_DOES_NOT_FIX_K__THE_FIVE_NOTES_STAY_OPEN__U_E_NOT_DERIVED_STAYS__GATE_UNMOVED',
  'estatuto': '[REAL -- os lemas do lock, em qualquer espaco de Hilbert: gap espectral 1; na unidade posta, u; valor esperado sen^2(theta) no angulo theta; no '
              'angulo de Miguel, beta; o fecho the_gap_closes, lido do kernel do rito, no trio; o calculo em runtime; REAL, CONDICIONAL -- o HminMic do kernel '
              "e' instancia desses lemas (HminMic_e_o_lock), condicional a um FockCertificate, que o kernel nao habita; ONTO -- que o angulo de Miguel seja o "
              'sistema do gap com unidade, leitura do operador; ONTO, A RATIFICAR PELO OPERADOR -- ler tempoDoRetido como o tau* do sistema; INPUT -- a fala '
              "do operador, sha16 7c2caaa87b0cdb01; OPEN -- K, as cinco notas, a unidade; kappa e' testemunha, regra do operador de 24/08/2026]",
  'fontes': ['psion_pedra_v405', 'recibo_errata_r7_das_pedras_01nov'],
  'verbatins': ['v405_cun_7c2caaa87b0cdb01'],
  'kernel_flags': ['ext_pzp405_0011',
                   'ext_pzp405_0010',
                   'ext_pzp405_0008',
                   'ext_pzp405_0009',
                   'ext_pzp405_0017',
                   'ext_pzp405_0001',
                   'ext_pzp405_0016',
                   'ext_pzp405_0006',
                   'ext_pzp405_0003',
                   'ext_pzp405_0014',
                   'ext_pzp405_0002',
                   'ext_pzp405_0005',
                   'ext_pzp405_0012',
                   'ext_pzp405_0013',
                   'ext_pzp405_0004',
                   'ext_pzp405_0015',
                   'ext_pzp405_0026'],
  'kernel_decls': ['TGLExt.PontoZeroDoPsion.o_lock_tem_gap_um',
                   'TGLExt.PontoZeroDoPsion.o_gap_com_unidade',
                   'TGLExt.PontoZeroDoPsion.lock_no_angulo',
                   'TGLExt.PontoZeroDoPsion.lock_no_angulo_de_miguel',
                   'TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock',
                   'TGLExt.PontoZeroDoPsion.HminMic_e_o_lock',
                   'TGLExt.PontoZeroDoPsion.o_retido_e_lido_do_angulo_de_miguel',
                   'TGLExt.PontoZeroDoPsion.a_tonica_e_o_retido_sobre_alpha',
                   'TGLExt.PontoZeroDoPsion.a_massa_e_a_projecao_do_retido',
                   'TGLExt.PontoZeroDoPsion.o_psion_e_raiz_de_dois_retidos',
                   'TGLExt.PontoZeroDoPsion.a_frequencia_do_sistema_e_a_do_psion_iff',
                   'TGLExt.PontoZeroDoPsion.a_taxa_de_fronteira_no_psion',
                   'TGLExt.PontoZeroDoPsion.o_ponto_zero_autoconsistente_e_o_retido',
                   'TGLExt.PontoZeroDoPsion.o_psion_e_a_projecao_do_modo',
                   'TGLExt.PontoZeroDoPsion.a_qualidade_nao_depende_da_unidade',
                   'TGLExt.PontoZeroDoPsion.o_relogio_do_retido',
                   'TGLExt.PontoZeroDoPsion.the_gap_closes',
                   'TGLExt.zero_mode_weight_is_one',
                   'TGLExt.alpha_transport',
                   'TGLExt.PontoZeroDoPsion.lockDe',
                   'TGLExt.PontoZeroDoPsion.retidoNoAngulo',
                   'TGLExt.PontoZeroDoPsion.tempoDoRetido'],
  'constants': {'u_posto_eV': 1.0,
                'rel_tol': 1e-12,
                'hbar_c_eV_m': 1.973269804e-07,
                'G_si': 6.6743e-11,
                'c_si': 299792458.0,
                'hbar_si': 1.054571817e-34,
                'eV_J': 1.602176634e-19,
                'acorde_kimi_sha16': '5da93b9e5e65a4ed',
                'half_nat_sha16': 'c23ce83106c69ff6',
                'nota': "u = 1 eV e' o Um POSTO (decisao do operador, 31/10/2026), nunca derivado; alpha_runtime e' preenchido na geracao com o "
                        "SEALED_CODATA_ALPHA da base (so' para conferir que alfa = beta/sqrt e; alfa e' MEDIDA, nunca derivada); G, c, hbar e eV->J sao CODATA "
                        "2018 / SI exatos, so' para escrever identidades e registrar numeros em SI (nenhum entra em veredito)"},
  'n_checks_runtime': 11,
  'checks': [{'id': 'x_a',
              'descricao': 'o registro ponto_zero_do_psion_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['ponto_zero_do_psion_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'x_b',
              'descricao': 'o registro lei_do_diminuto_v405 selou neste rito',
              'onde': 'core',
              'caminho': ['lei_do_diminuto_v405', 'all_verified'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'x_c',
              'descricao': 'o canal vivo do neutrino segue com o mesmo veredito: o gap vai AO LADO e nao move o canal',
              'onde': 'core',
              'caminho': ['neutrino_mass', 'verdict'],
              'op': 'igual',
              'valor': 'TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED',
              'estatuto': '[REAL]'},
             {'id': 'x_d',
              'descricao': "o fecho the_gap_closes e' emitido pelo compilador no modulo da pedra (TGL_DECL_SOURCE)",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.the_gap_closes'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'x_e',
              'descricao': "o relogio o_relogio_do_retido e' emitido no modulo da pedra: kappa so' aparece ali, como hipotese",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.o_relogio_do_retido'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'x_f',
              'descricao': 'o teorema citado zero_mode_weight_is_one segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.zero_mode_weight_is_one'],
              'op': 'igual',
              'valor': 'TGLExt/LocalBreuerGap.lean',
              'estatuto': '[REAL]'},
             {'id': 'x_g',
              'descricao': 'o teorema citado alpha_transport segue no modulo dele',
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.alpha_transport'],
              'op': 'igual',
              'valor': 'TGLExt/ContinuousModularZero.lean',
              'estatuto': '[REAL]'},
             {'id': 'x_h',
              'descricao': "o elo entre o lock e a energia retida, o_retido_e_o_valor_esperado_do_lock, e' emitido no modulo da pedra",
              'onde': 'kf',
              'caminho': ['declaration_sources_v394', 'TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock'],
              'op': 'igual',
              'valor': 'TGLExt/PontoZeroDoPsion.lean',
              'estatuto': '[REAL]'},
             {'id': 'x_i',
              'descricao': "o kernel segue sem habitante do FockCertificate: a instancia HminMic_e_o_lock e' condicional",
              'onde': 'core',
              'caminho': ['psibit_v395', 'conditional_psion_face', 'inhabitant_exhibited'],
              'op': 'falso',
              'estatuto': '[REAL]'}],
  'erratas': [],
  'limites': ["[REAL] U_E_NOT_DERIVED fica: o gap na unidade posta e' u, e Delta = beta.u carrega a mesma unidade; nada aqui fixa u; o registro nao muda o "
              "numero da massa nem o veredito do canal; validade no kernel nao e' creditacao; o gate nao se move",
              "[REAL] Delta NAO e' gap: e' o valor esperado do lock no angulo de Miguel, a energia retida, 1/beta vezes menor que o gap; o estado inscrito nao "
              "e' autoestado do lock",
              "[REAL, condicional] os lemas do lock valem em qualquer espaco de Hilbert; o HminMic do kernel e' instancia deles (HminMic_e_o_lock), "
              'condicional a um FockCertificate, que o kernel nao habita (psibit_v395.conditional_psion_face.inhabitant_exhibited = false)',
              "[ONTO] a fala do operador diz «gap com unidade»: que o angulo de Miguel seja esse sistema e' leitura dele, nao teorema",
              "[ONTO, a ratificar pelo operador] ler tempoDoRetido como o tau* do sistema: e' tempo proprio, nao t_P, e nao mexe no ramo canonico; tau* nao "
              'foi obtido aqui; os enunciados sao algebra dada essa leitura',
              "[REAL + regra do operador de 24/08/2026, TheHorizonRate.lean] kappa e' testemunha: kappa = F(alfa, beta, theta_M) e' proibido como objetivo de "
              "busca; kappa so' aparece como hipotese em o_relogio_do_retido",
              "[REAL, medida negativa] sob esta leitura, E_fluxo = c^5.tau/(4.pi.G) nao e' E0 (ordem de 10^57 eV): a ponte E_fluxo = E0 do Kimi NAO vale aqui",
              "[OPEN] o disco: o invariante K nao depende da inclinacao, logo o angulo nao fixa K; a pentada: quais sao as cinco notas segue aberto; so' se "
              'sabe, por fala do operador, que o angulo de Miguel pertence a ela',
              "[REAL] zero_mode_weight_is_one (o peso L2 de (1/2).sech(kappa/2) em toda a reta e' 1, faces 1/2) e alpha_transport (alphaKappa' = "
              '-(q/2).alphaKappa, gradiente negativo em kappa > 0) existem no kernel; [ONTO, da gerencia] le-los como a forma da fala do operador sobre a '
              "eletricidade e a origem da medida; homonimo: alphaKappa = sech(kappa/2) nao e' a alfa de estrutura fina, e kappa ali e' a profundidade modular, "
              'nao o relogio; a palavra cauda nao esta no teorema; isso nao deriva a unidade'],
  'diz': ['em qualquer espaco de Hilbert, o lock minimo 1 - P sobre um vetor Omega tem gap espectral 1: vale 0 em Omega e 1 em todo vetor ortogonal; na '
          'unidade posta o gap vale u, o E0 da Lei do Diminuto, e a tonica fica meio-tom acima dele',
          "num estado a um angulo theta de Omega, o lock tem valor esperado sen^2(theta); no angulo de Miguel, beta; na unidade posta esse valor esperado e' "
          "Delta = beta.u, a energia retida: Delta NAO e' gap, e' 1/beta vezes menor",
          "a tonica e' Delta/alfa; a massa e' a projecao transversal de Delta; o psion e' sqrt2.Delta; sqrt2/tau = omega do psion sse tau = 1/Delta",
          "o HminMic do kernel e' instancia do lock (HminMic_e_o_lock), condicional a um FockCertificate, que o kernel nao habita",
          'o calculo, com beta = alfa CODATA 2018 x sqrt(e) em runtime e u = 1 eV posto: Delta, tau, Gamma_B e Q = sqrt2/beta; a medida negativa: E_fluxo nao '
          "e' E0",
          "a fala do operador sobre o angulo de Miguel esta embutida por sha256 e vale como INPUT; que esse angulo seja o sistema do gap com unidade e' "
          'leitura dele [ONTO]'],
  'nao_diz': ['que a unidade u tenha sido fixada',
              "que Delta seja gap (e' o valor esperado do lock no angulo de Miguel)",
              'que o kernel habite o FockCertificate',
              "que o angulo de Miguel seja, por teorema, o sistema do gap com unidade (e' leitura do operador)",
              "que tau* tenha sido obtido (ler tempoDoRetido como tau* e' leitura a ratificar)",
              'que tau seja t_P ou que o ramo canonico tenha mudado',
              'que kappa seja funcao de alfa, beta ou theta_M',
              'que E_fluxo seja E0',
              'que o angulo de Miguel fixe K',
              'quais sao as cinco notas',
              'que a eletricidade tenha termo no kernel',
              'que alphaKappa seja a alfa de estrutura fina'],
  'leituras_do_operador': [{'trecho': 'o sistema físico que fornece a medidade da tônica por ujm gap com unidade e pertence à mesma pêntada é o ângulo de '
                                      'MIguel',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'a inscrição da luz que singulariza o sistema é a eletricidade',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'},
                           {'trecho': 'a origem da medida é a matemática, ou seja, o 1 absoluto, que representa 1 Eletrovolt',
                            'estatuto': '[INPUT do operador, verbatim 01/11/2026, sha16 7c2caaa87b0cdb01]'}],
  'extras': {'assinatura': 'gerencia c1, em nome proprio, 01/11/2026',
             'leitura_tau_star': {'status': 'ONTO, a ratificar pelo operador',
                                  'content': 'tempoDoRetido lido como o tau* do sistema: tempo proprio, nao t_P; nao mexe no ramo canonico',
                                  'is_a_kernel_term': False},
             'o_gap_e_o_retido': {'gap_espectral': '1 no lock; u na unidade posta (o_lock_tem_gap_um, o_gap_com_unidade): o E0 da Lei do Diminuto, com a '
                                                   'tonica meio-tom acima',
                                  'retido': 'Delta = beta.u (retidoNoAngulo): o valor esperado do lock no angulo de Miguel '
                                            "(o_retido_e_o_valor_esperado_do_lock), 1/beta vezes menor; NAO e' gap"},
             'fock': {'status': 'REAL, condicional',
                      'content': "os lemas do lock valem em qualquer espaco de Hilbert; HminMic e' instancia, condicional a um FockCertificate que o kernel "
                                 'nao habita',
                      'termo': 'TGLExt.PontoZeroDoPsion.HminMic_e_o_lock'},
             'kappa': {'status': 'testemunha (regra do operador de 24/08/2026, TheHorizonRate.lean)',
                       'onde_aparece': "so' como hipotese em o_relogio_do_retido"},
             'unidade': 'U_E_NOT_DERIVED fica: Delta carrega u e nada fixa u',
             'ponte_do_kimi': 'E_fluxo = E0 NAO vale aqui',
             'disco': 'K nao depende da inclinacao: o angulo nao fixa K [OPEN]',
             'pentada': "quais sao as cinco notas segue [OPEN]; so' se sabe, por fala do operador, que o angulo de Miguel pertence a ela",
             'inscricao_e_medida': {'status': 'ONTO, da gerencia: ler os dois teoremas como a forma da fala do operador',
                                    'content': "a inscricao da luz que singulariza o sistema e' a eletricidade; a origem da medida e' o 1 absoluto, que "
                                               'representa 1 eV [ONTO]; os teoremas zero_mode_weight_is_one e alpha_transport existem [REAL]; le-los como a '
                                               "forma dessa fala e' leitura da gerencia [ONTO]: alphaKappa nao e' a alfa de estrutura fina, e kappa ali nao e' "
                                               'o relogio; isto nao deriva a unidade',
                                    'teoremas_que_existem': ['TGLExt.zero_mode_weight_is_one', 'TGLExt.alpha_transport'],
                                    'homonimos': "alphaKappa = sech(kappa/2) nao e' a alfa de estrutura fina; kappa ali e' a profundidade modular, nao o "
                                                 "relogio; o gradiente e' negativo em kappa > 0; a palavra cauda nao esta no teorema",
                                    'deriva_a_unidade': False},
             'fala_sha16': '7c2caaa87b0cdb01'}},
 {'nome': 'kh_n1_cobertura_v405',
  'veredito_prefixo': 'TGL_KH_N1_COBERTURA_V405',
  'veredito_sufixo': 'AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_29965_CONSTANTS_23749_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_EIGHT_V405_MODULES_ADDED__GATE_UNMOVED',
  'estatuto': "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do "
              "sandbox da v405; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; "
              'a cobertura NAO move o gate',
  'fontes': ['kh_n1_v405'],
  'kernel_flags': [],
  'kernel_decls': [],
  'checks': [{'id': 'h1',
              'descricao': 'a checagem de cobertura do kernel do rito passou',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'ok'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'h2',
              'descricao': 'constantes cobertas == as do sandbox v405 (KH_N1)',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'decl'],
              'op': 'igual',
              'valor': 29965,
              'capturar': 'constantes_cobertas',
              'estatuto': '[REAL]'},
             {'id': 'h3',
              'descricao': 'teoremas cobertos == os do sandbox v405 (KH_N1)',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'thm'],
              'op': 'igual',
              'valor': 23749,
              'capturar': 'teoremas_cobertos',
              'estatuto': '[REAL]'},
             {'id': 'h4',
              'descricao': 'nenhuma constante fora do trio',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'fora_do_trio'],
              'op': 'igual',
              'valor': 0,
              'estatuto': '[REAL]'},
             {'id': 'h5',
              'descricao': 'nenhum nome que o leitor v394 nao leia',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'nao_lidas_pelo_regex'],
              'op': 'igual',
              'valor': 0,
              'estatuto': '[REAL]'},
             {'id': 'h6',
              'descricao': 'o axiom_report do rito tem exatamente uma entrada por constante coberta',
              'onde': 'kf',
              'caminho': ['axiom_report'],
              'op': 'tamanho_igual',
              'valor': 29965,
              'estatuto': '[REAL]'},
             {'id': 'h7',
              'descricao': 'a cobertura da v405 inclui a da v404 selada (constantes e teoremas)',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'decl'],
              'op': 'maior_igual',
              'valor': 29484,
              'estatuto': '[REAL]'},
             {'id': 'h7b',
              'descricao': 'os teoremas cobertos incluem os da v404 selada',
              'onde': 'kf',
              'caminho': ['axiom_coverage_v392', 'thm'],
              'op': 'maior_igual',
              'valor': 23430,
              'estatuto': '[REAL]'},
             {'id': 'h8',
              'descricao': 'as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) '
                           'sao EXATAMENTE as do pino (arquivo -> sha256)',
              'onde': 'kf',
              'caminho': ['formal_files_sha256'],
              'op': 'igual',
              'valor': {'README.md': '395b1201109079084f3562349161283bd644e17d5e18cea19971bac041e58d11',
                        'TGL.lean': 'a8103a482049e7a7ff229b020fd7e2b807f597b7897b1e8405278683c84cc41d',
                        'TGLExt.lean': '5dd444489d5547e0f413f18ebfc12ebfcf4589b622dc40b2747fec29fe178cc7',
                        '_check_damming.lean': '485969b99f3e3db7ef4f9e4b1e97fb501ff68540a957e21949784d57d7536d21',
                        'lake-manifest.json': '31a94eb76a8370ae8d75999ccec510f1ef7b994e369beebee2a3ea0088eee235',
                        'lakefile.toml': 'c3ddeea5ed0f6c4b65a8df0781c8336c1254d577dc3c546b797972259d07b813',
                        'lean-toolchain': 'efac0b94923b2d8b6840cd35be9177ad0fc5ab2332f4f4311c98712cee92fdee',
                        'TGL/AreaScale.lean': '7058ae26f99f44f2d81d0c51e39bf435359a94c410405e52da4c4a44834ce075',
                        'TGL/Audit.lean': '072a68f45189b8a539d2156e15749b53424c603f7ba65a2c60d69d69db17dcec',
                        'TGL/Basic.lean': '6de2b310b37c0af52fc83f9bf3c34d4c141115f4e74be86f9870b9bd531ebd04',
                        'TGL/ContinuousCornerAbstract.lean': '4fdd0cbdc5d56f1fb18c5cd5963f30b1b6aec878cdc4f7daa9c4b1a5018e4890',
                        'TGL/CoreSupport.lean': '041fb863b07c3e0a167d5d0c8a522890d2da61586f41c27be2b06c46fac588e0',
                        'TGL/FiniteThreeLocks.lean': '612f2384ca441da25c2fe613fddf489010a0f0c16578ce61b0a57c6581e4276d',
                        'TGL/GravitonShadow.lean': 'de9d4eba70977bb437c3b72889a4f4d5f54ac42f5382a49772cb6a8d24f3b1b7',
                        'TGL/HalfNat.lean': 'cf79d85fdebab68641bec2ccc4592033b2e27327834243ef269b7b6a89e7d22c',
                        'TGL/HalfNatFresnel.lean': '5d16a6e04f5e97fda89ed27f326280535902f0c4c05228d340554d15177a029f',
                        'TGL/HalfNatJonesTower.lean': '440c4d9497e31a0299cbf5217e56f406e5799c7731e6e5268b62d9bba43bbd05',
                        'TGL/Main.lean': '05266e573d3f476f68be6b8380a61db785dacf52524be6107b6ade8d8658aaa9',
                        'TGL/ModularRealization.lean': '17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348',
                        'TGL/NameIndex.lean': 'c55044e2aa6ef076ac028799cad36ec5787afd9d8587a6ce388ab989376a4f08',
                        'TGL/NameRelation.lean': '02f69df45d7c1e392b522f9528cf5cfbe92793d34ffe94451415eece1cef1e35',
                        'TGL/Probe.lean': '3954829f86511e845479ff5f29f69954e86f5389e853f4c74bb7aeba1974c684',
                        'TGL/Probe2.lean': '05bbb2cccee15938b1b8e68798551b697321ce52a087d9a07c06a47404d0ba0d',
                        'TGL/Probe3.lean': '35638a94030ef8f8b87cbeadcfbb55e73255a5f2aa91cb2b790f46b37158c96a',
                        'TGL/Probe4.lean': '7101d535745be124fa8543816dca85fd2540b9808b342fc3d6bc48b42a41291f',
                        'TGL/ProbeDegenerate.lean': 'f141bdef86179aeff9f2aed7dc6139c9964ae51bc6f926bc2d8732a54df4ebb9',
                        'TGL/ProbeFiniteFullWitness.lean': 'cc89ac970844eb3d2f75a1130370378f7a4b054eb2ba00e13c4da94e31453c20',
                        'TGL/ProbeModularAPI.lean': '9f5fded048b17616443ac1889103d019b2d4b3e98772709186bd6e4a8f3c0801',
                        'TGL/ProbeNameIndexNoOptimal.lean': '9f3d895eaa0d7218965ef8af227a68b69226665261ddb3ec42bf91935e79a618',
                        'TGL/ProbePropOnlyModular.lean': 'f277643284c620bb092c46813a4aadb31a737cd854004d9ac59bbf39f94545c8',
                        'TGL/ProbeTrivial.lean': '4993bd3fd6da17f7dafd7c5972f2f4b396cb5be86d13ac1f54ab317cc950bef7',
                        'TGL/SpecificAQFTWitness.lean': 'c6995c3cb3bd20529f14f7fc5c9c549066e3c89ef0b0a76b0a67a4965a367df0',
                        'TGL/TransportData.lean': '95cbefeed54a5f5ec9aa41be556ceab1e14da4bae116b4019eb1ba1d9ee9d04e',
                        'TGL/VerbInhabitant.lean': '812a47f0e71a86f37368c918b0f704cccad9cda0e32c4aee64c5566e7808a5d7',
                        'TGLExt/AQFTCoreInhabitant.lean': '4cfd8053f5366543f571b51dbbedd7f8b07b3490ff87b94fa6bf1f3cd551ad09',
                        'TGLExt/AbsoluteOne.lean': 'dd0325368992ecdd31079021f8a0e00e46d3a7ea99ff620df59bc11c2fd7f444',
                        'TGLExt/ActionCouplingControls.lean': '7be4b6cf1726d3e068fa7bc515901ce8e6b4873de7f6775c05f5bb67cb6876e1',
                        'TGLExt/AdmissiblePauliInteraction.lean': 'd24ec327ce724cd4c942633aebc61e8782203278cf952082ce6323be8daf7066',
                        'TGLExt/AffineClockAndRegion.lean': '01cf9751f545a3e2ab3a66c279194d70829130a1ee8cf4a58bceb218ab952783',
                        'TGLExt/AffineSamplingObstruction.lean': '0af21eaa8ab68131f83bc1432c5fffeedf9be330f18674f9116c3438e5de2080',
                        'TGLExt/AffinityProducts.lean': 'aca7047c57cb8ab96770216258d4f7b92a2750b73b18550e68392607548ebda7',
                        'TGLExt/AffinityVectorCriterion.lean': 'e639455ca310e0108cc8bb132a27c90b6a66142847e3f15ce96c365095674c83',
                        'TGLExt/AfinacaoDasCordas.lean': '66e28e61086cc6bad47771080732ac32719383d247eff923bbcdbb09a25e8659',
                        'TGLExt/AgapeNonVacuity.lean': 'e49ad8f980d7cf482c7c32d5de5a3b4ca0a4c32ecfb8b63756643be71bbf804a',
                        'TGLExt/AngularAreaObservability.lean': 'cd132f9a7c75a914fd2176f949920df381b7f34c9b4e2bdd933bf055154d7811',
                        'TGLExt/AngularScreenMetric.lean': '12f2cbff964fe821580a5f9ab1fd2f6f165dfbe5abff9fb32daccd2e03c252c0',
                        'TGLExt/AngularSelectorIntertwining.lean': 'bad9bf02cfbac9ff63976dc522e179d3b34b8f165a21381cb4f15513d56b3fc6',
                        'TGLExt/AnsatzEinstein.lean': '88ed36908dbc290f07574a0cf8e9a711220875ff79322ad89c21ce95f7dd436a',
                        'TGLExt/AperiodicAveragePrefix.lean': '92e9516c3ac8699eac3f7bcdfc996f866f31eee5b3edcf1d0b676fd44e47cce6',
                        'TGLExt/AperiodicCentralizerExpectation.lean': 'eb64de9055ad5d216667bfaa22d87675c937cf33e67b57ac420d50d2e711486e',
                        'TGLExt/AperiodicPhaseAverage.lean': '9265e8a454a8e7c4ee94d873f065735dfc126c273ed08d7e327acb57d13759b5',
                        'TGLExt/AperiodicTowerLift.lean': '5e4aa2034892b7a497547d450b0b6941f4e3c7433aaefa6a8d34b824d70e1939',
                        'TGLExt/AperiodicVectorAverage.lean': '45cc0c64ff898556be4c4be84f691cfdf22b9631b71ab7f2d4ade186e0ff75ce',
                        'TGLExt/ApproximateBoostFlow.lean': '78844bd06c719b739f6f16d6ec41cad2188a5d3bcf4230705b886b1d559247d5',
                        'TGLExt/BenchCertificate.lean': '78c05090f2cd93fb9e8af7128821de39fbd94ac20259ad45b1bb9f930ffcfce5',
                        'TGLExt/Bicommutant.lean': '354f1a50e11c4c3d6350e31290001a38d297e32dea76bc675d4ed31132a4917a',
                        'TGLExt/BicommutantSkeleton.lean': '428df3db6eb05456d1e0048cdcef826ec1f0e350ab29b8e27faf0bd7e76657d6',
                        'TGLExt/BinaryRelativeQuartic.lean': '667a2d0a26853f8305eb5946a7edccc9eee9d878d21e4d8b57655ae3570e16e1',
                        'TGLExt/BisognanoWichmann.lean': '5218c8eb32682a58a8424369ab5d1e1d22c8bdf36b21cf3ea25932606cf38fc0',
                        'TGLExt/BondLocalityEstimates.lean': 'dde3c7f8804e93f3bab0020f15924fe42f9b244f647ee1ea024a7a19d575d8b5',
                        'TGLExt/BoostHeatConstruction.lean': '690746080dcb8fe37b24babf39c881909adfdcf1182af405fd306f50e598fe1f',
                        'TGLExt/BoostMetricJets.lean': '5696ed939b2e37e2a17d5d38c228ca90551bf3b21672f1477e1ae6883b28025e',
                        'TGLExt/BoostMetricPullback.lean': 'cd6e45547ceeacbd985faf7ce099e29f43c3706f60d699591ced4a5f6fc92deb',
                        'TGLExt/BoundaryEntropyBridge.lean': '395bf58304e4e8b2da1c37a3ec9e0314d848061ce9baea26b05124743b9f4ab4',
                        'TGLExt/BoundaryException.lean': '38ff7c2bfe243333872d0b26d5eac9e9f2e6424e87cee3e3cee15667bb5ef346',
                        'TGLExt/BoundedGraphOperator.lean': '4d70d27d25f31fed13b73a7ae60601478718e41bbc38c24c38117b0cc26dc84f',
                        'TGLExt/BoundedGraphStandardSubspace.lean': 'd1ddfdaa09a099de17dcbbe4521546f3f2f8bc82d729093a925f1395d020beee',
                        'TGLExt/BoundedOmegaLimit.lean': 'cb84427ca6f2e13a5730a886f2a6b4cfa56a8cc6fa2e0d4f94465739d2d153ca',
                        'TGLExt/BoundedPerturbationCocycle.lean': '7ea841f1f2e292059d12c3577556f764868ebc70a7f673c969411aacf8758ec0',
                        'TGLExt/BoundedPositiveCongruence.lean': 'eb9eb9515634f35f5ff67a4efb2664f610e8d83cde32624638f5db8513a6b396',
                        'TGLExt/BreuerTrace.lean': '4a667f41d3b7bb1d6a3a02fa46f43372c2a3e4bef30c98acde05294f5c46b496',
                        'TGLExt/Caminho.lean': '703b5bbfbf8b30182d6bf52c24ee1560a83cb675803c3fff1c69dfb817577208',
                        'TGLExt/CanonicalCocycleDerivative.lean': '846e640e03c768f45e580e1b34e7a18de1d16937ff03c812bbcfd67402e4377c',
                        'TGLExt/CanonicalModularStationarity.lean': 'c90d705932ede27be17d58b97d783f4a312d9850d790f6bb28e76d7a51179330',
                        'TGLExt/CanonicalSelectorBorn.lean': '0e3aef31155b28c655fe4f179d103efce02759110252aa95cec483dca5235ecc',
                        'TGLExt/CartanTracialSupplier.lean': 'df30212a61be55ce023b7a46e82d27d558fe7a0832d3637fbbdd4ac0f9199f1d',
                        'TGLExt/CentralScalarPhase.lean': '31560a21b8455d9bde491a9cbf76af1bff3c3ac0240da3360a1336622cf18dcd',
                        'TGLExt/CentralizerContractBridge.lean': '5293db8b121db928ceb682bd1fc7cb97fee4e6a9c75348db02edc8af012faa37',
                        'TGLExt/CentralizerDensity.lean': '626800aec27b1e8941156e02c4c20ff600ae30a0492f0f41f21d81479652bda3',
                        'TGLExt/CentralizerLocal.lean': '6ee14bef4788bc99502ea8df3e55f76b6d689827f9d4723b6f088e8ba962bd93',
                        'TGLExt/CentralizerPhaseOrbit.lean': '72e9cb7bfd4eecf593306cbbb6c1be8da239cf13d1f1bfae5f199e7da6abac6b',
                        'TGLExt/CentralizerRemainderPerturbation.lean': '96e58e44dbb0ed05a2e2631338f0a3ba1c1afc50ac625328d3fe46a60870463a',
                        'TGLExt/ChainFaithful.lean': '202cce85dcc6b618e88d07b3e20f82251589bbf9b2219c9aa974db11604f7e7c',
                        'TGLExt/ChainLocality.lean': '9e0ce48c9cf735d466f738d220c2d8dc28dd4105ae712f26d109affa07e3d98f',
                        'TGLExt/ChainPrefix.lean': '57a790434cd8bae9ded9772e70427e1e10f802ce5aa6fcc7e0185f19a7efa381',
                        'TGLExt/ChainSiteFlow.lean': '90a1e0e2d74bdb80a7336892d598f2a14d2032c299b2bacf2de3d3389b07e0ff',
                        'TGLExt/ChainSiteOperators.lean': 'bcffce7e08d267dfdd7221d4dffdcdf8734d4e9b4f07af794e69eeb0b0929a56',
                        'TGLExt/ChainTail.lean': 'fdfe27e5f54e96e0506f5514d9fb2f3a4ba00f418b5ce666961ee5e4e15bb28b',
                        'TGLExt/ChainTailClosure.lean': 'b3be47bf0fcc0d932bcf154a36468590229cc830f39ce21a9371867db215c2c1',
                        'TGLExt/ChainVolume.lean': '72f02a317a9b28f5c2afb993b86e260eb4dc4ff49aef27b19179cd93f8b323d1',
                        'TGLExt/ChainVolumePositive.lean': '9fa681525efcacedc7829a50975711ed942afc7f94ce57233bbf8419eb759278',
                        'TGLExt/CharacterPrefixStability.lean': '187e4a58a6cc5ba00ab1280cd4fcf9c8a6166c164f3a6bcdb58142b9c498d5a7',
                        'TGLExt/ClosedAntilinearStandardSubspace.lean': 'a90532fc36bb1eb4310885a94159e3bac3d59a919b421976d498fffa2015ecb8',
                        'TGLExt/ClosedLattice.lean': '1cc93d55463aaf6108a47361a0622684c79027cc25c1dc7700b45e3d995035e9',
                        'TGLExt/ClosedModulatorCandidate.lean': 'b1826bdbbc560588b3546b46aed99ea8484c2b418782aad1e8bb66e128674098',
                        'TGLExt/ClosedTomitaOperator.lean': '6908e22eb36aaebcd3fa0b577c030a4fcb006ebefb77a9d7b15485428abe854b',
                        'TGLExt/ClosureCertificate.lean': '977a24815e7a3eaea64d16318c95f76a854176987205ebb8a809418e0e86de63',
                        'TGLExt/Cocycle.lean': '28dd4546e652983126c37d80962b6534a0684b41f7903c58032aeea3d3931ee4',
                        'TGLExt/CocycleNormLimit.lean': '63c83cb65c1e5ad8f34c9f1688da25646072dc4e87e4178bd11055a5cb27e596',
                        'TGLExt/CoherentEinsteinBridge.lean': '2c50fd4fb0175606256565474725eebf02595e3b40e5e6e3e1c9f0e169c606c7',
                        'TGLExt/CoherentHeatMatching.lean': 'ebf755fb4b29560d262696c49acddb16d49a1a8b47bf47ceae79b544e50ddbf6',
                        'TGLExt/CoherentMatterControls.lean': '0aeb327642c2a1766e94961659ffafc118cb993db77f2512df2fe90d2c827329',
                        'TGLExt/CoherentScalarStress.lean': '77836a308409ab6770f02ab125fe3dce492dfcb3b33767342e71cb13bbb51133',
                        'TGLExt/ColimitSeed.lean': '528d769f4751816fa3a13115d6c30e2975f7c7b34a5a9d8fcf91e9982a60cf53',
                        'TGLExt/CollapseContract.lean': 'b7a7b32c21ec2b9fc2250b2486baac1cc8b0a89611d455e903fe7f52ad5133c3',
                        'TGLExt/CollapseCostAndAttestation.lean': 'c3dccdc92b6d3b39378be7ae193b2026b6a898fe1757ad47b3ce466c0a7dfc2f',
                        'TGLExt/Commutant.lean': '114782c4fb991da15ae22e3e053ecf6a8c4a5f68e7152afd40102a66c44db19a',
                        'TGLExt/ConcreteFourFrame.lean': '4c3d4ab63b2df108961c9875b23853a3315aa96a9a0a89180106d212e1d9f550',
                        'TGLExt/CondExpect.lean': '33e0eecd498ec326d8f5bf699b3a5b5aae4a388fa049564bfd8619b096737ede',
                        'TGLExt/ConeVolumeReconstruction.lean': '1dd77be08104353e97c17d63f9653d0d98c7caf10497bcdb0d8bd714a3252f2b',
                        'TGLExt/CongruenceScreenIntegration.lean': 'dd4aa5c4913f9e2729c1345ebba46b344a97ac36ec01c7c60c7c13b7f1e518ef',
                        'TGLExt/ConjugateAct.lean': '9f32e50afe49ca0e56981facda73269ebd4f525a38fe122e396da045ed88da99',
                        'TGLExt/ConjugateWitness.lean': '09717611e32d86505f7bd65aa57465e355cec29411f87e4776140146476bd9d3',
                        'TGLExt/ConservativeNullResponse.lean': '547b8531f8df82a40f73c7cbecb3830c04b0b0dad5091ac4f07ef456533aba47',
                        'TGLExt/ConstructedClausiusControls.lean': 'ea7c02fb94d1f10ab1d86822293c3b034d1cf26ef2bfbbcb042f2a0e539092ba',
                        'TGLExt/ConstructedEinsteinReconstruction.lean': '32c90b78d290bbdaa4f77282e8214492cce911ca394c288bbe5d0a9f63f575a9',
                        'TGLExt/ConstructedHeatPrimitive.lean': '3403ff4c3a890914d23b9a60cba65409f08ac752ca2f7f8611d4c124055bdac2',
                        'TGLExt/ConstructedHorizonPencil.lean': '84a5ad14883d24c59152501a9d4a107970697e2058f76fdff53aee33107b1cfb',
                        'TGLExt/ConstructedNullCongruence.lean': '02e35fc0b9c100cdef5194235cc6fb56aa2054c82b243db861df45f8e1de0c40',
                        'TGLExt/ContinuousModularDomain.lean': 'fbb043925f4a05859b335d0d7180e0037eb7f4cb969210288baf38fe59db6c0e',
                        'TGLExt/ContinuousModularMultipliers.lean': '494be0d93285c97abece403bc5503c5207b10ba430df4bb965db4bba8d814f21',
                        'TGLExt/ContinuousModularReconstruction.lean': '0a5be091f8f24ea1039b52c31120056b3735d483bb1b2caff63319382bb6aa9d',
                        'TGLExt/ContinuousModularResolvent.lean': '4b25b03984382f826607325e228e286cc254143c6ec1d9a43d6c2e31b166d2dc',
                        'TGLExt/ContinuousModularSquare.lean': '33282dc7e340d0e5821bbcc65d1ff4328929f158002cedf36b0094531b0473fd',
                        'TGLExt/ContinuousModularStandardSubspace.lean': '8ab346cf5befb36486a851c1973b7e8f1302da0a8510ea5667d1a4253aec5a76',
                        'TGLExt/ContinuousModularZero.lean': '0dad5794f98ba1cb8519b4c105f63d555b5dc3d8fab7884f8265aebff214f376',
                        'TGLExt/ContinuumShards.lean': '18e43b74a336360ff7c4458b703e263e06e52f4778aba225073fac65d8614c40',
                        'TGLExt/ContinuumTT.lean': '21c62b855a477119daa3daab0c1e8f80f265bec4b269ce5367e7d9a60de72a96',
                        'TGLExt/ContractedBianchi.lean': '26037e693c190c45dad803699a795031722852bf7a0cf7a407d2f200376fafca',
                        'TGLExt/ContratoQG_v31.lean': '2f2c6561a5a5d832b43f11f7bacccf4811eb4392f1832f78cf4a5838a72a4808',
                        'TGLExt/ContratoQG_v31_Teoremas.lean': '4fa0eff792110ff5c076a83a60532636502e8c3335b5a7af2ab29994abee4ee1',
                        'TGLExt/ContratoQG_v32.lean': 'e57bfb47fedfe63e50dc51701a73d5bef12bc0f6e413415f88583b9212970523',
                        'TGLExt/CoordinateCurvature.lean': '8a3af4a1c80c18f4670377ab35ab6e661b724120a359a3150c9b68e30024e68a',
                        'TGLExt/CoordinateRaychaudhuri.lean': '4bbac36ebd8bbc87d3936a1a09bbce81e8d293572f6a0a13256a5141af154524',
                        'TGLExt/CornerFamily.lean': 'bbceea91341abcf2b2a3f0f33ce88975fd5c529f05918c6982eb4872b66fe105',
                        'TGLExt/CorrelatedUnitaryState.lean': '6802f01cb85cae60d2b083b9e1dce80cb4c4500107bc7601f3b56548e8515b07',
                        'TGLExt/CovariantAreaCounterexample.lean': 'bb43910687f2a997d554b3c359833249bb26f9530c96578fae36043f453168ff',
                        'TGLExt/CovariantCorner.lean': '155cb43d01bb7645bd6bef16d21fbbf2c01114a73fa466e1e4d18ac92a6c5e7d',
                        'TGLExt/CovariantCurvatureBianchi.lean': '4dafb97e6ae7ad5cacc14462b28c81d2d137ef70532a7ea1a679f941a1049b5d',
                        'TGLExt/CovariantNullPreservation.lean': 'b8ba72e62abb0ba2be823681c5be18c105993608c7e35c337edca497143c2f3d',
                        'TGLExt/CovariantScalarConservation.lean': '69183bf0fed81f162e804aa1967b1efbc0a57ccc5532a67826b9ad63f6576f1c',
                        'TGLExt/CovariantVectorCalculus.lean': '47eb4c5f69183cb376b8536893b5bce70a64a7e5049d88ea561d72038fff2a50',
                        'TGLExt/CovectorStressCalculus.lean': 'fedb5ad4f5aed68a96063ff75b7989bdd0d4e5145af012cf8209417fca5a1679',
                        'TGLExt/CurvatureControls.lean': '8c27b78d1e672056cc422ba357c707af26f2f9d94350d3798d6c2f5a948e6048',
                        'TGLExt/CurvatureJetAlgebra.lean': '85287748b45debe315c72f1154d28875e3bd200763f5454ba3d5fde63ac74004',
                        'TGLExt/CurvatureNonlinearVariation.lean': 'a576f8c6edca90e892583af8d770c73d2cc243b7901370ce2edc800213d0ffcc',
                        'TGLExt/CyclicExpectationObstruction.lean': '6b21047553efb3da000f2cb3f6b06addb8dc0327cab18992c01942ced5ea7416',
                        'TGLExt/DecisionCommutation.lean': '182ba6345586d5e81b8320caaff50c94e3ff796e6a947e54db5dd57c88e2472d',
                        'TGLExt/DensityStateUniqueness.lean': '4eddf6e76f4447c115471648ce61f325e215e2f4748e9228c60d4cc8bbdd9fd8',
                        'TGLExt/DerivativeFromLinearCutoffError.lean': '715e4e59f25adcdb42a3726c30f2cf6483fc8d12b2d1ebbd72cf0a29f6c4c6db',
                        'TGLExt/DiagonalOperator.lean': '912c55816847252ef9de8a810fa0f303aefbafaecddcb25235069d448d37d70c',
                        'TGLExt/DiagonalRelativeEntropy.lean': '02b20499659b527041041fe5b7e179d1719c28fce03f7ae465856f076dbcab49',
                        'TGLExt/DiagonalStateCurve.lean': '3718f20b8e3c20a6d006c322cf0571e1fbed17d951d9892e43e539ae36cac823',
                        'TGLExt/DiamondConformalCurrent.lean': 'c977e76d349146877a7c14482d205056fc46057b372700a05bb78fb90c225d13',
                        'TGLExt/DifferentialFlowExistence.lean': '5e567f89d53c6ae6629fb955d39c4317da3692115d24dab0bb0cd9386f77e370',
                        'TGLExt/DimensionTrace.lean': 'cdadc9fdf8ed641c7c260e0a5450577b4e190b102a055dc0d2c49e71f49338ea',
                        'TGLExt/DirectionalUnitaryFamily.lean': 'b836a4da8a3c921aa85f27772799a8ce2b9600245140a087ffe1bfcb67f54ea4',
                        'TGLExt/DiscoDeEuler.lean': '5634eef0833dded793c2fd649a6b57ceda1fefbc7e7e9edd689ef527d1a18459',
                        'TGLExt/EmergenceTriad.lean': '3b7c6220060598fb4353dddefd71fb9064db3ce8a1e2cf891d0f2ae8c97c04e9',
                        'TGLExt/EmergentEinstein.lean': '836ac3e4035afc52b9bf46d5640007a8ae4f66c3c55ee90153600437564f6f50',
                        'TGLExt/EntropyGeometryControls.lean': '83ce196f970c816e58a2c5ad3127c0af447a8433d4b27df3335d6b2370938063',
                        'TGLExt/EquilibriumAreaExpansion.lean': 'e670ae6fba4e8f8a31ca13c30227fc162025fd43cb1d2b7d2760440139f508bc',
                        'TGLExt/EquilibriumCongruenceControls.lean': 'd377a134ab3ae1572ca3fb837801a08ee9e4795fcdaa768c90a96cb3a8ebf68a',
                        'TGLExt/EquilibriumNullCongruence.lean': '0c8c7dfb164d012a51b2756524fd55cf5cfcbed201e513bb0ef0b15c34f1872c',
                        'TGLExt/EquilibriumScreenIntegration.lean': '04821ca36872c8bb722bdde912ba69385ffcb6a403ad61e6d7a9344eebf243b8',
                        'TGLExt/EquivariantSection.lean': '87de6cc37a8f3a803ed11602f0f1be2fbe7d813c9d574e890ea483c56c8498d1',
                        'TGLExt/ErgodicMeanSection.lean': 'c27a343e7d4e39c115bca0290d8f5e09b4941d077022919e2f295655d0c704a3',
                        'TGLExt/Ergodicity.lean': '79bc3b939b6e4e598cefed39088d5b9e9a06e125614bd185f414441c3718f5de',
                        'TGLExt/EsperancaCondicional.lean': '8579115333f84428751d0070579de425f3de6958ee5931e3d21214aec2890c2a',
                        'TGLExt/EulerMetricPullback.lean': 'd6eaa6621382493f4860afecb8c940f162ceb92fce49aae1b5b5b4dabfe60208',
                        'TGLExt/ExactWitness.lean': 'c1c8bf0a6fc0d7ab053fa3a119fc6d9dcfe7a5e752ab4b11f0eb2d2034701e32',
                        'TGLExt/ExistingTowerRealization.lean': '4794c11578cf6414d6d0142f815777dd376d64e22442550200d4b7101bd6331c',
                        'TGLExt/ExpectationAlgebra.lean': 'a88032a7e84a9c6390327f5a8ae8c1e3f4595ce0bfc3f19295827f01926f3584',
                        'TGLExt/ExpectationBimodule.lean': '59df6a514db887ac09c1c2211198bcd31bb088da2df90a0240a9580fc67e18fe',
                        'TGLExt/ExpectationBlockPositive.lean': '9a53e9b58e9e5626541917d7fa4ec0fd60090589171ef147af54640ed4e917a2',
                        'TGLExt/ExpectationBounded.lean': '83e690806b4b43fec5e23a398ed174967bb8324ab481c08a7cddf481751fdae6',
                        'TGLExt/ExpectationContinuity.lean': '29331a459e55d5e5d79bd6eca9651289cf0b4dd31f603da35cd78200172e28ff',
                        'TGLExt/ExpectationContractGap.lean': 'f0917b893d2da8a6312fc28f5df3e6f8344afbe7bcbce59466311846cd6d77bc',
                        'TGLExt/ExpectationNormality.lean': 'e941f703e74773f215d617235caf2e9523a44554f094beebd51a68aa6a45578e',
                        'TGLExt/ExpectationPositive.lean': '0d0bd84320ebb2dd4179352e2931c8526b28c668c69f30401f85dfad45c58608',
                        'TGLExt/ExpectationProjection.lean': '211c301670b9f1358a718060ed128916a9f2ae25a60a939cb10d75748e463e90',
                        'TGLExt/ExpectationSlice.lean': 'f472b2f505c80ad0c45398565efcbd07122a6f157a6d5328664a5c7d8467966d',
                        'TGLExt/FLRWFieldEquations.lean': '5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8',
                        'TGLExt/FLRWGeometry.lean': '47aea5aebebd8611edab566724ce562508908dc86b96db7194dff2592bac9e92',
                        'TGLExt/FaithfulGeometricLocalization.lean': 'ec071ec8f7720217c242c17274cae7616ba5223b12ac89fb3113294a3b4e365f',
                        'TGLExt/FallenLight.lean': '145eed2729d232ee9405d4124a0c333c3344e0a4a0b898b3a3eb189ba28cb3c0',
                        'TGLExt/FalsidadeDaInercia.lean': '9f6efcb2a0987e18ce79ace43aa394f5822673ead16f48b281fdd15c94ea908e',
                        'TGLExt/FiniteCharacterResolution.lean': '2d66449f30f0376910d332318fc8f00fa75738a4ae73de38ddbcf544ed904fea',
                        'TGLExt/FiniteCoherentSources.lean': '4b71fe49ae505d3017a3c2d05395de95f6c64f9630ea27c56de8ed024d94416b',
                        'TGLExt/FiniteCommutatorEvolution.lean': 'c3f09de40089bbafd78de5e6f2b9823db75297e600fe192c1b9616475fb8fad3',
                        'TGLExt/FiniteCoordinateCurvature.lean': 'b5bd14f03fe15d23db36fd9a9883da1fb9968f8932e68a7dc05412fa0a61cefe',
                        'TGLExt/FiniteCoordinateMap.lean': '787fc98e2771802833e2c3db186078fcaf507d95cc33ea0bdd50e5b526c2cd17',
                        'TGLExt/FiniteCrossedProduct.lean': '330b9624b2ae0d8192785ae28c5a57f58e2d49070ea717f6af964d8c57020e0d',
                        'TGLExt/FiniteCurvatureAlgebra.lean': '1a4d52e7619d7af9c9b925260a385d75612bd6468aaa89279b93f03c8e1d110c',
                        'TGLExt/FiniteEinsteinNaturality.lean': '9cc91c8e89471e60a4c21dd02c22e1dce9ebc63f37f2913e6bedb50ebb66827d',
                        'TGLExt/FiniteEntropyAlgebra.lean': '1181bf39dfd29af1c02eb939c246f5bcd60ea264397d8adfa66d3a8068cea226',
                        'TGLExt/FiniteGNSNoCompletion.lean': '056170ec3f50929081a75db129117cd5814ba88c1fe7c97432392303664e5025',
                        'TGLExt/FiniteLevelExponentials.lean': 'a6b414b68771d396bcab3314c09304120cfa0a74a16365bcdcaefd158ae007c7',
                        'TGLExt/FiniteLeviCivita.lean': '2915d2372995b92a953a696b7ebab39fb7c3f8dc0b30c40d1d5be8d511db2231',
                        'TGLExt/FiniteModularHamiltonian.lean': '80d6ac4cfe142a2e60d6e75450563a4751e05aaac79f327b0736350d81249c7f',
                        'TGLExt/FiniteResponseErrorBounds.lean': 'b27158546247809a81bde08cc2e6f74b4d8d0663c1267b41dde53e13f986937d',
                        'TGLExt/FiniteResponseReconstruction.lean': '683e09a4823f6151103a756455d3b82941e40966d67311700543447a37350bb6',
                        'TGLExt/FiniteRicciContraction.lean': '47049b8c990d60643ca02a5340344097e83ecc02b4b92f0f3ab91064c9a6422e',
                        'TGLExt/FiniteSiteHorizons.lean': 'fe13f5bba87907305bc750dec4ac7cc1b7d5977ff181b26f0f53b70f30bdaa50',
                        'TGLExt/FiniteSitePermutations.lean': 'b9ae2e48c6683c483cf35ee61a7a16b946e58115bff2d5ae540c585e8c421382',
                        'TGLExt/FiniteTomita.lean': 'f845a71a81bb02585020f5da224a9407b4dd36b1408cccab37ea1b69cfb6647e',
                        'TGLExt/FirstCurvature.lean': 'd88d4a5fa15462f43850119f39099059a8ae0af87190420aa921dfaf20ebde44',
                        'TGLExt/FisherCorrectedEinstein.lean': 'f5c7942dedef5d49b2bec4b83b4dc5b5138d67d91324de062427febb4bda2514',
                        'TGLExt/FisherInformationTensor.lean': 'cd8e3fc1c0cdf003a2d26e5457874de490a421ca8a24c61b72e83d65a08eab0e',
                        'TGLExt/FlagNetV31.lean': '1c93dc3ba5f792580cbd148dc85b5b0727a0b8587820204f4003f7476ce59d2b',
                        'TGLExt/FlowDifferentiability.lean': 'aee805e8c99da0bed80e9c0a9c7f9b8a1ee2439aff18f97dfa53f44e75f29ba4',
                        'TGLExt/FlowDifferentiabilityControls.lean': 'c79dc1df3428c4ee370ca6e29fae1f14b3d2f2597d2d07fde12a467fc4f56f08',
                        'TGLExt/FlowGermUniqueness.lean': 'b91fb095080e212b3ce11d269bc1a94593063e63eaa87e0b706ae32377fe35c3',
                        'TGLExt/FlowLinearizationError.lean': '2b919351f54f4a62e987bb2caf9ba88aaede5f4678fbb27a5ab2c08ea31f4135',
                        'TGLExt/FlowRegularityInduction.lean': 'bf65cd5fd224d083b992646896ad707b0a1d01a973bf1fc3d76e3f35244c0118',
                        'TGLExt/FlowSmoothGerm.lean': '77fc61a43fe30568a213d3a26735a026bc0589d23a8b62a75f9b98659012bdfb',
                        'TGLExt/FlowTimePropagation.lean': 'a94614c8793c243f8580a4b0082207a017cbd36d555ee6674b8d461339fc8c58',
                        'TGLExt/ForbiddenBoundary.lean': 'fb1c39a61dfc2882e53a1cad9de082fefd3c07963a161314c37262ac4db452b2',
                        'TGLExt/FourthOrderMatchingControls.lean': '46c5f923d4de9fe835c39c75451c7e263b15011b1a12797c0aeaa57ad6bca5a0',
                        'TGLExt/FractalUnitarity.lean': '8f10a958e11d1bd3f97a5324875b4654c341fbe7a1a90dc52ed640cd65903bcc',
                        'TGLExt/FrontierCertificate.lean': '1015e2fb8f4e8ebb1d374f1401b957df11ca4f640ef22fad96fe8dbf86c14c2b',
                        'TGLExt/Fundacao.lean': '66332d58fd216317ec5196a64a7aa670c87dcaa5edc59f57a5506bc621d3e073',
                        'TGLExt/FusedWitness.lean': '3708dde5255559cddcddecbe2ca05eb93e751511db8a8f7bcf6968e60a065e69',
                        'TGLExt/GNSBridge.lean': 'a625e38824790f94eb6ac54f44cffc0656e6e3fc2f3ae2d42220dac071a11c8b',
                        'TGLExt/GNSQuotient.lean': 'd6b3ac4f4306516adf561e1c68f20a5337b49b6c0e9bfd2b17550ed48264b9a6',
                        'TGLExt/GNSTower.lean': 'bef660d621d3d5a915832c85e986f901fc64f8e43d31cd76ebea897cc7db64ed',
                        'TGLExt/GeneralAngularTensorCodec.lean': '436ca327162c479f1201d011ae1ffff520c4af808737c2e2337be19449cd76b6',
                        'TGLExt/GeneralExpectationCP.lean': '698dd6c7d5d2125671b3a3c0cf70a27c144e3dc2d845ab54e093bea018d18aee',
                        'TGLExt/GeneralExpectationPositive.lean': 'aa01607cde22a55fab76e0517883ee945c2231c6e4fc27496dee5bff9a2d4aa5',
                        'TGLExt/GeneralLinearizedGauge.lean': 'bc7ca8225d99873b79ca5b8c34a59a66c6a81b2830a690d6128e450dde4ab19a',
                        'TGLExt/GeneralMetricClausius.lean': 'd635b15c7197800ae26034bbf8d11ddc422a2dbf17633c743b603d3d66143109',
                        'TGLExt/GeneralMetricEinstein.lean': '5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c',
                        'TGLExt/GeneralNull.lean': 'b8704cf7c144db3fe9f064eb13944307e9508115f0ad4cb083422130f6cc2fda',
                        'TGLExt/GeneralNullCone.lean': '6b9a2e6ee041d46168fecabd93194b611f1603ec0da9aa26d3bb3cb2f67daaa2',
                        'TGLExt/GeneralSourceEinsteinBridge.lean': 'd4055e0f95d6ed7b83456bbd837a3c77e354f191a248c7f1b65933fb0f4853e9',
                        'TGLExt/GeneralSourceResponseReconstruction.lean': 'a27d1c0963daffadc845120fd892d46a47f41ffcd022c10ae67888d1bc18c468',
                        'TGLExt/GeneralSourceUnitaryRealization.lean': '996d06074c7fe3a5b4ecdc5ba183fb0066683da30bcd1db2c5d66e62783ca2cf',
                        'TGLExt/GeneralTensorReconstruction.lean': '9b9208bdc0e2402d6fbe88dc5923bf7a88a2df25ddbd53236e8c82699e236de4',
                        'TGLExt/GenericAntilinearAdjoint.lean': '7b6cbf95f4fc8387f70b856a57fc5a5fe65edcae96bffcb427fc48ea852cd05a',
                        'TGLExt/GeodesicFlowControls.lean': '4e334cb6f9ebcdda70a5ad85faba2d36b420d16df8dafb16e70a6bea59c156cb',
                        'TGLExt/GeodesicFlowRegularity.lean': '19a994553c4c260cf6c437b17d25ba11ff839a36630afb2bd8228b9167d5c2b0',
                        'TGLExt/GeodesicInitialRegularity.lean': '0884dbaac718e00bf50ae9cf5fa9fc8ce8dbf919a0956c37e10f81a89e54c881',
                        'TGLExt/GeodesicShooting.lean': '97c154b1a22b26b1b356401ee495b68c29dfa89f9a41e786793e12766e7c7b87',
                        'TGLExt/GeodesicSpray.lean': 'bbd3e06e01237c37f0335f1bfa5737e71c462a8af60a4745f31163c8bf5fb4f9',
                        'TGLExt/GeometricAreaHorizon.lean': 'c9d158213947b6684a7c4e5f8c1f308a903770d99fc7a1b9222c37e868fe34b8',
                        'TGLExt/GeometricEinsteinReconstruction.lean': 'a66ea61bec9a9bd4fb0947a5c4720211acf16ca74c06ae3546b2ab22822b3df5',
                        'TGLExt/GeometricLikelihoodSeparation.lean': 'a84bf1be8268b529554e2b2192eb4c8476371a454b97b2c4b7ae484e6a6da9d9',
                        'TGLExt/GeometricScreenControls.lean': 'b4ca43288bd20a462f0cc9dc169e79826773a4cf1c46b090ffdcd27d690b34cb',
                        'TGLExt/GeometricScreenTransport.lean': 'fcb340fcff4b0566bbb9040859d60aeacb45dc8e8230d2b4285f92acefa48975',
                        'TGLExt/GeometricSectorObstruction.lean': 'f4ac9ffe11f221dfd37e56b5c2cc1a354051740f6a1eca9a2e64277ecf420d27',
                        'TGLExt/GeometricWitness.lean': 'c971c7b2a45420bcb1c9e5e6ac37276e5a5796269b1002765b41b835a03d2afe',
                        'TGLExt/GeometryFluctuation.lean': 'c70403c706d7b033628bf775ebc8552d5adfb885372c58f2252dbc1c58e7b655',
                        'TGLExt/GibbsAffinity.lean': 'df6a1755b431c8003de0e7b880d462aafc2e6a7d70d8663620dfa399e3ca67b0',
                        'TGLExt/GibbsGravityControls.lean': '7ae7a7fb82df297324f664639486800f0e38f1303a54d058c7868bcab756ef12',
                        'TGLExt/GibbsMatterBridge.lean': 'cb0d25363d8e6c2c0945db10bcbc24ca5e77a7c2620530ae71b081eead60ee98',
                        'TGLExt/GibbsProductLaw.lean': '201ab5d28dfb4c989654afc636f5b7db04f9cdf80d35d7b10a129bad3703c015',
                        'TGLExt/GibbsProductVariance.lean': '18d3b732f1069c94a6dc24c01fada64bccedf8351fb35301b74356001cbe73a8',
                        'TGLExt/GibbsSamplingWindow.lean': '4757a99ba7fb659ef03d520109384aa75161cdfcbc584209100d3686caec3c06',
                        'TGLExt/GibbsTilt.lean': '0ef5daea88f038321559bfac875d53e6e80c7c12a45a153fc66c12ec9cd1c1a0',
                        'TGLExt/GibbsVarianceResponse.lean': 'f4d0ae5eeb531526a05393283bf0f8e683fe796863efc307efcb7e161b310065',
                        'TGLExt/GlobalFilterLocalReduction.lean': '5895d0785137e99da060650414bc5383820a013fe7c2185b4c81ecef9916d6f8',
                        'TGLExt/GlobalLiftConditional.lean': 'ba5731ef6f86f75a159a912a92a7e756994fe41702b0f289afe7a7d4c783b4bf',
                        'TGLExt/GlobalLiftLadder.lean': 'd7cf95aac8c872f7b6ea3849bd9db88412005925a0b4d856e83e266fce56b5d4',
                        'TGLExt/GlobalProfileControls.lean': '444b2453c5ed2adc1d6253c9038c31704d10da66347f19ec1115c560e5fb9544',
                        'TGLExt/GlobalProfileFaithfulness.lean': '8adc7e88f412a3b7b2f08fa977910c6865ab999d698b3f75e6d17a0de780e461',
                        'TGLExt/GlobalProfileState.lean': '1ebad0292f612b8d2d22c85ae98cfc282adc8fa73b14bb638c86f438226692b4',
                        'TGLExt/GravitationalChartGluing.lean': '3b98010f08eed5c81c9a618f0e7e74902132292fd13c7f6ac5d029e708da30e3',
                        'TGLExt/GravitationalResponseRecord.lean': '6ec37ca79051152da8c36f26e73bf767d15b2a0c8b1ea73f2f32d3389c5aa9c6',
                        'TGLExt/GravitonPolarization.lean': 'b51528b11b867c5770edb555f42ee22ed11ea94ee702249d4c50fa5c7e39a758',
                        'TGLExt/GravitonReading.lean': '4b9cdbbdf1d0c20d906315b972774f0043bec7333c313764054ef45daf508cb0',
                        'TGLExt/HajaLuz.lean': 'c43c07467e1e2caaf21be69cc20223e31e76398b2374ceb2151034d4b9bed433',
                        'TGLExt/HarmonicEnergyObstruction.lean': '52013ac1958a7964d9f47963b4318e32a7ec2536d057a1f7cb563d7b62cb43f6',
                        'TGLExt/HermitianConeRigidity.lean': 'bf55d841ee0ed6b1f334e65ec1560f016949056c7ed4ea4cb53a29c60eef7850',
                        'TGLExt/HermitianLocalCoordinates.lean': '9c07267dd3995f742d7a72eca3a99cbf2f8d724a150942c7ae4cf638cbd2fa9c',
                        'TGLExt/HermitianTwoLevelFlow.lean': '5786ffecfca8798773b01253fdc9e01d8d4712c0c95f4109fd34a6eb326bdaf4',
                        'TGLExt/HilbertHome.lean': '449bdee93696fc5fe4d7f5ce898f5e3a95ad0867773714e466b279aa6089ecdd',
                        'TGLExt/HilbertInhabitant.lean': 'd1aeebee94883f27e6acc3352f8eaac00131398a653be888dc0056bbb6c635a1',
                        'TGLExt/HorizonAreaScale.lean': '9dcd856be4084bce3d6681402d7008a16daf0dacab51c153abbae85ddec3c72c',
                        'TGLExt/HorizonBalanceControls.lean': '7e06684f99380dbd37ff6b26fbc033a11ef0b7ca8fcfb8260d1525989e463659',
                        'TGLExt/HorizonEinsteinReconstruction.lean': '77180ae46c3ed6e897639e598a623193a3e30a334ea31e13449b0882bafed1bf',
                        'TGLExt/HorizonGNSImplementation.lean': '4c31b6a8a29fc8a55fdc6e9d5450600bf56878890a40200a5b53021f8ec247ae',
                        'TGLExt/HorizontalAreaSelection.lean': 'c4d697db380bc38cd3119139a0063b5c6d4922369bb531f5e39dde89ce62cac7',
                        'TGLExt/IALD.lean': '884b327423888ddcddd6d2ac75302a1b0054bc795bf6d111608bdcb0cec40bab',
                        'TGLExt/IALDGraviton.lean': '6a4c7ff17866db0837fc86d4645d8a858bcaf3906ffb1a9c0c23cbb76d8db78b',
                        'TGLExt/IALDJones.lean': '3070346c3571f3400e4290075e974d0c0b8c1bf73bd2f057dc23d0813da864fc',
                        'TGLExt/IALDRhoStar.lean': 'e8110c499398a8a083c82f1e96201933d5f46f245e346b5b05fd44ce7f57e770',
                        'TGLExt/IdealLimit.lean': '3f0147199cbaa91906c0807cbd47c7cc449b00e0ce7c16de99ed41260191ded0',
                        'TGLExt/Identidade.lean': '94f51e0f80d911ab4375c529be0b906acb40394a4a621f5167f5ef74dbe441f5',
                        'TGLExt/InfiniteCocycleDecoding.lean': 'fd8d807b1a65a5f1072fd31f1e9998affb71c2a14f3d271fe9fd9e6c20f639b0',
                        'TGLExt/InfiniteFisherGeometry.lean': 'fc30c7321824715ba54a7ec5b3933fdfdda6347396937a8adbc85a3dbad82370',
                        'TGLExt/InfiniteWord.lean': 'ead8928528c8f42c4d57628bea66b0942002b0300cbbef9e77fe88b337ab8652',
                        'TGLExt/IntrinsicFisherClock.lean': '72cb6cafcda0d59d7da167946841701edc2ccd34aba00f072212ea698b3a9edf',
                        'TGLExt/InvariantProjection.lean': 'fef79118c7b544f4d7d301e20e5c40f19db9fd8bb0e81ebe9c1418c532e99b40',
                        'TGLExt/IsotoneNet.lean': 'b4575ad7ce6f82c58026e659bad8b2a88f4e65bcdad4be7fa9c66a853910c95a',
                        'TGLExt/JacobiAreaQuarticLimit.lean': '272e56ee975f901c207356a8bca21ce809afba7d66791b7cf41bac9292c07ec2',
                        'TGLExt/JacobiRiccatiProfile.lean': 'bca4379cb326668d90c365d2517def09f5fc5916c3016de59a7e5591d93c3cda',
                        'TGLExt/Jo8v32.lean': '18df8f686e524845eb9956788de82fc37ae3e329867272965a7c6b91e483605f',
                        'TGLExt/JointCoherentGravitation.lean': '80723c5484bcc57815056847816c628f89fca3425e5b5af582f696c0421a7161',
                        'TGLExt/JointCurvatureVariation.lean': '6228e410560a1a1087b87496d5a35b7841ec57c970523e9ae7f6639abcb18ce1',
                        'TGLExt/JointPreparationCovariance.lean': 'f9b7ce75dfd9420d752590b297dcb5bf975d36a8ecea9a9cc51208113d009d0c',
                        'TGLExt/JointUnitaryPreparation.lean': '92294e1bc20560901a0e887eea84dd17b9d7d476fb0ce86e82d9cfcdae66b746',
                        'TGLExt/LeftRight.lean': 'fd127e4d3b361423c66683d5de9bee95ed5c947013ab169d7bfad5a66951bb4a',
                        'TGLExt/LeiDoDiminuto.lean': '3df80334792c043e3f253c3adc0bc7920bb5ac46851b2bc8a6e360520b35820e',
                        'TGLExt/LevelExpectationFamily.lean': '5342b44c7fecd4624845216db2b0f76611ac9d76c7b72b222b9c06bdb5958574',
                        'TGLExt/LeviCivitaLieVariation.lean': '64f5729a15842bb7b400ec5eb14f6ada7b34e0ae3e12ceeb5d10a03d854bedf2',
                        'TGLExt/LeviCivitaMetricVariation.lean': '165f6b36fe2859bff79065aa1da71e078c20e17826221c7249df93c18e2a0a65',
                        'TGLExt/LieMetricJets.lean': '3e5ae25bc071797cc2fd7a583a6ae6c878c46a67983292c58e711eb8397430a3',
                        'TGLExt/LiganteLeiCampoCurvo.lean': 'e3f32d9b85ae82dbea4c281673d5105af6b16c240c2add5de0b5bea9134d0697',
                        'TGLExt/LiganteLeiCampoCurvoTestemunha.lean': 'eeeed286178408b37df5296ee2e517f33606f02f941dcad5e10482a5be24f76c',
                        'TGLExt/LightHelicityWigner.lean': 'e08c9a4b00e0057b1cdd0e5c1c93a33b3a727ef49edc80cd50911053d672e714',
                        'TGLExt/LightIsJ.lean': 'd19dfe1ccda812581cf262181083a2642e9d1da1c086349c9369eb530e07ed5b',
                        'TGLExt/LightNetStandardWedgeDataBGL.lean': 'e4da9e865d00bdcb1c112fade347fe4a169e7e9d0e80227c81267861e6b9e540',
                        'TGLExt/LightOneParticleByTerm.lean': '654f319de4720122f08370880f2a0a37e4cd9f622cfd6469d81528a4b94ae26a',
                        'TGLExt/LightRhoStar.lean': 'c3df6950fdea0fdc91566f3d86d21890641d17a67dbe99fae19894c274a797a1',
                        'TGLExt/LikelihoodCocycle.lean': 'b88fd6b05d568ddfdbef439f3a38636c2f8eba9d9616383ff8270f5f4f1c567e',
                        'TGLExt/LikelihoodCocycleControls.lean': '822dc30e4c43205c91fd6e6ea742cd694445ffa98d71901e72efadf092deab2a',
                        'TGLExt/LikelihoodDensityLog.lean': 'c6397153c7001efee5c54ee57b572d7895e25027c14f3d298cefb2a6629e6c93',
                        'TGLExt/LikelihoodPreparedState.lean': '1425feb2495c7ae06aab6e9251a4743131e7d616ad56d0a6b612216915098ee4',
                        'TGLExt/LikelihoodStateCovariance.lean': '1645bb231d20a114a89934911c7688e76ed3e6fc5794fb9d31021ca241d3f420',
                        'TGLExt/LinearizedSpin2.lean': '8cbd46c5200f92dfe0b0dc0eac44f97f29b416e1cc911cc2fcceb2cc43888098',
                        'TGLExt/LocalBreuerGap.lean': '8ec73c7d9e703d6c775f53351a784ab98b27ad2dd3d253b79a3d34992e0d5d3d',
                        'TGLExt/LocalCentralizerExpectation.lean': 'e4b6660a9d146e05e9e47280604d8e73f63ed8f9f3f609a870a3da3fd6954494',
                        'TGLExt/LocalFilterLorentzAction.lean': '94293528cb368eeb5af3ecc84fa058aa14954fffcd85b31add0771ef8a4923e3',
                        'TGLExt/LocalGeodesicFlow.lean': 'a46b495447e1617f5fcc40d0dff56a1203946d9d1c518145c45393d22ca12086',
                        'TGLExt/LocalHorizonBalance.lean': 'b3dcb033522681ba0aa1bb6b755370add8ba8741e632d5653a9ff2647957320a',
                        'TGLExt/LocalHorizontalPauli.lean': '744b5be38756ed5d91e82c49ad93d703c63e8bbb273f33afb3741b2e7181bf06',
                        'TGLExt/LocalInteractionCocycle.lean': '86595c4a8fc00b789bca22dbf728f9e97bdec6d4c23e16af669d4f3e89ecbe16',
                        'TGLExt/LocalInteractionData.lean': 'cc99d54f2ef455deaa60b79cddba45d980f8a480a265188db333051bacc8a307',
                        'TGLExt/LocalInteractionDynamics.lean': '3b4cc5f5dd1e5288b00aea0954f71b319eeb709f52c777e39e2554c305b26f29',
                        'TGLExt/LocalInteractionGenerator.lean': 'c3b42ace074f957975a384615b8761563510a1634e3a973bcc053bc1f52e4400',
                        'TGLExt/LocalInteractionUniqueness.lean': 'cf5b45a66773e27473a0cfb8e63f1344a34fff855ba16f720755155ebeff45fe',
                        'TGLExt/LocalPolarizerWitness.lean': '436f9f38cf9d91637300bed1836efeeeeb6519768ae86d869f1f3b7e9136ec3d',
                        'TGLExt/LocalTowerProjections.lean': '1a593da7dbf8c5937b2900ec17801ae008c829d2838e73b7e0a2dd6d27ac94c7',
                        'TGLExt/LorentzMetricField.lean': '9e47cde222d0cfd3df6e619323e3d7c1a31f234f6c21b1cc1d5dab63106fdfaf',
                        'TGLExt/MarkovTower.lean': '5b542018622975c4b2c498d1727ca20f7280ad108bfc25d0a587958097e2e74b',
                        'TGLExt/MassaTensaoPura.lean': '9ec48bf6d608ae5a9d85c5c28caa21c972ba9847ec05703f733b582a17a9956b',
                        'TGLExt/MaxwellLiteratureBridge.lean': 'c07d135fac53737465c50636204da7ee79d27ced9df3867382d1e190781febe4',
                        'TGLExt/MetricCompatibleJet.lean': 'd20de372f56b28d5de7134d5e28a47d70b8a453c9da0a97cb729270e860463c7',
                        'TGLExt/MetricCurvatureSymmetries.lean': '6070daffdf63f24ee64157c11da8cbcf43765b6ce2c42069780a09b140064db7',
                        'TGLExt/MetricEinsteinVariation.lean': 'b6ec0383b49f4bfb3e6b4e3f91b19341f62330aac0ac4532b527d40147bd8bfe',
                        'TGLExt/MetricFieldConnection.lean': 'f5134b7ed4a069fc1235c890174a4487566861ef676ccaa0f2e230bf4e26a832',
                        'TGLExt/MetricRicciVariation.lean': 'ba322f76127f39a026e69673de38dc1b08b0af7fe8ce828ffa0cc38312ee5017',
                        'TGLExt/MicroscopicClausiusBridge.lean': '6094cdb81b56cd7c3809732095bb0f6890da6714607f652b8ad7b3f445b7469b',
                        'TGLExt/MicroscopicEinsteinBridge.lean': '4186f6aa6cac28daee26fc849723649cb3eea30ffe25078a504087401f40a61c',
                        'TGLExt/MinimalSolder.lean': '53dbb33e260a46ebd3c753ec7a4ca61fc5a4721757e310d58c3a4cb1455e7e66',
                        'TGLExt/MixedGibbsFiniteAccuracy.lean': '643a1309f815eb22f00330af21802ecc9c68a7c6a541da32e010a496f79fc977',
                        'TGLExt/MixedGibbsGravitationalBridge.lean': '857c3c4344abd7c1147850f210f681ac6c471ea6df0fd7e0b7010a041542169d',
                        'TGLExt/MixedLadder.lean': 'eb43ba5a3ee66412f7f4704a7a435f485f1e53a315188e4f9bb46234f757f861',
                        'TGLExt/MixedQuadraticGibbsResponse.lean': 'e4bc7c2dec0663b2c5d0bc487cb64a8095bdd23aa7cdb08e9776c85b353dca80',
                        'TGLExt/ModularCornerCounterexample.lean': '159ed1dfe55006438a341f590bfe5d32e2dee4fff2cf6e456d5c2c68735566e1',
                        'TGLExt/ModularCostDerivative.lean': '967f7e5a74d12e2c0ec6617207f82d65f0e835aa6a9f0f24e11312203290378f',
                        'TGLExt/ModularCurrent.lean': '5fe336cadea3140fd8b42f831ff6c74624f3fea961b013c8b2d4f5aa85d76d8c',
                        'TGLExt/ModularDephasingBridge.lean': 'fab9b46f0343cabeff156feb9838d383273bffc08580d9bd7e93f3f89964581a',
                        'TGLExt/ModularDomainCommutation.lean': '5c7006b19fe6e580016e37ce8b8ce1bb2d182eeadb9b1404a3f2fce6eae2afcc',
                        'TGLExt/ModularEigenRecognition.lean': '66dc109b8ec4489e14a11040192ef9145e8bbd017e68cd8ec04772289c4be765',
                        'TGLExt/ModularFirstLaw.lean': 'aee3eb49a6d0544e8bb2a3f7b763b04dc46ea425ec4565f77ae1c33ffc27125d',
                        'TGLExt/ModularFlow.lean': '62cfa753d4b40a9091aafb383a8edd588a542dddf5e97ee39906ec31c59826b9',
                        'TGLExt/ModularFlowAlgebra.lean': '28901cdfdd69d05df6828fd92ba55499de97f4cb93cf919e61077cd5f3e8679c',
                        'TGLExt/ModularFlowHilbert.lean': 'cbdb1b3ff9f2728d85ae02ef5d0db0257290b55897da0b649722894b5f776776',
                        'TGLExt/ModularFlowLevel.lean': 'dd0b03747826991f3e697d3be3b297cdf4bf65350565215e9d6ae1944044a261',
                        'TGLExt/ModularFlowPre.lean': '8a65e5b027028c8825cacf4d0cdbde88b2e5472e2db88edb3fe2483a8bd772bf',
                        'TGLExt/ModularFlowSpectrum.lean': '49eaf5a1556de26c4c5ba45a5ced7b5a4b454cce8446158aeb10b9bd12109606',
                        'TGLExt/ModularHorizontalRotation.lean': '63ff32e37c68ac64d92322fbd777363d01904da2b897ba6ad595273e30bdbccd',
                        'TGLExt/ModularInverse.lean': '310eec1fa0c2219fea26e0f36ae73767a791a415636ff091d2f405289ee74045',
                        'TGLExt/ModularOpticalIdentity.lean': '00e13081aa19abb92c9c21c5e44c4134b299007c7f5b2ab8350c70d79802e4f7',
                        'TGLExt/ModularPower.lean': '54beb442c52e9127f1cf42f77539c82a6b9ff72c04c79c8a95ef9e84cd67acf0',
                        'TGLExt/ModularProbe.lean': '189ebfa321d8ff5d9efaf3f801b6eb0add404a60272f53c1c2f35fe45a93d875',
                        'TGLExt/ModularRemainderAction.lean': 'e7a412865eb4cc1ac2eff75b3231d354306844e533a931f4c8da1fa94ee81b32',
                        'TGLExt/ModularRemainderDensity.lean': '75f4f655bfeb679d927565b79d3b390825aaca872ed8f7a2a72bcc1403ec2611',
                        'TGLExt/ModularSignatureObstruction.lean': '8d1197d5989171caa035bad83fea7a62fcbc0a2218622719b17a3185a464030d',
                        'TGLExt/ModularSquare.lean': '7b0952e0016075569561e1e31fa6e65579e9d60da5483eb3b960d6c9d0b0fec6',
                        'TGLExt/ModularSquareAdjoint.lean': 'be31d1fdff4f4ed48e80fe79f3fe3801385f08fb00ca15b74daed291fd734c14',
                        'TGLExt/ModulatorPolar.lean': '46b78bd3619ebc819c5956962b4c1b89d7e711fe7a148bc3c4661f0a44edf118',
                        'TGLExt/ModulatorPositive.lean': 'e82885c6385f04ba5ef09077188638fe7752df75ddcce441c77aff8d68540f45',
                        'TGLExt/ModulatorSelfAdjoint.lean': '48d6510f6d823c9e2e5177e1d40e4b5f80379dbe1926e6897c3810797dee7c02',
                        'TGLExt/MonotoneOperatorLimit.lean': 'c08824988f1bf53b9aeb11c582703b099f9382b1259c2e41029a9a8fc40edda5',
                        'TGLExt/NameIsTheContent.lean': 'e12ee35c3a749a733b13e7b1b32440627d2201f088759d553b16ab30435811d0',
                        'TGLExt/NoFullWitness.lean': 'fde4ca999c40e6892d1958bee15a066786adb1363b8e3514f41eeb8b8909a654',
                        'TGLExt/NoNormalTrace.lean': '7c5090ec79fa42399a2cd0f2fe453f2d2c1d3cb229a110806eb1e57494b90266',
                        'TGLExt/NoncommutingLocalWitness.lean': '2b81bd84bbc9ee868cd1669b125e571757ebd35af8cd5adece66ff30fa637ec1',
                        'TGLExt/NonintegrablePotential.lean': 'cde59459d149847809b57cf0c7da6bed01d2713be20faa35282e98db5f1aaf74',
                        'TGLExt/NotIsEmptyWitness.lean': '9d53b4431da539f577854ac71e2c3762c14d7b2c76df34964f2e0552940ebd94',
                        'TGLExt/NullCongruenceControls.lean': 'faf1776a0f1421f8d818e1e92a68c3db806a50c2d2f376cd3d88f8f10fc09827',
                        'TGLExt/NullCongruenceField.lean': '7380fb5f7734a480920f625b3d708fdbf9c799927a19113093df4f875a62dbbf',
                        'TGLExt/NullGeodesicConservation.lean': 'd93e08b7eefaf277f38743d51586b0799f79071838b09640806672c47a37a229',
                        'TGLExt/NullJetAlgebra.lean': '591d2b1693b345c46410a92d79050e5c485dab403076ce54e6784ba12b6fdc47',
                        'TGLExt/NullScreenAlgebra.lean': 'c612ed2dde86fc5f68dd04a80abb9f9260d7dee84d52f269e7997da60501e523',
                        'TGLExt/NullSeedWithJet.lean': '02e0f615d9748984a26280d72f504430a49144d89c1c7187249bc24599d44dd2',
                        'TGLExt/NullStressCompletion.lean': '32c536e5b5abf5b79b196103aaec60fc2328951fa889ad5cd0b53acf4f9e92f6',
                        'TGLExt/NumberOperator.lean': 'f6b2c0670ed3524d19496819b772547e6757908151055901dae2563bffd8cb77',
                        'TGLExt/NumberSelfAdjoint.lean': '72dee88258250dea5bd660657a47cc8ba4d769b5decaa74d5a4f09e5842ffafb',
                        'TGLExt/O16.lean': '09d4a489dd7e23b09218480d1b01929b16e11a6e5ad6a99337fb3654edd34edf',
                        'TGLExt/ObservadorTerminal.lean': '162eeeb8c16cea81f6f0537e46a995f48551656dbc7c1874a98afa0087dc52fb',
                        'TGLExt/ObserverInside.lean': '05c3b515fd9f5d9d4cfa5b0e4c40b68b292fe9ff9d41db2e1957a25e003b398b',
                        'TGLExt/OperatorBlockRepresentation.lean': '9183518588045d0bcb0075b9466962100ce227bbb2283d5e25f93306cfa5219f',
                        'TGLExt/OpticalAreaFreedom.lean': '33b9dc4681766648647c81fd6acd257f928af347250e3960cb62248e41d5284b',
                        'TGLExt/OpticalBalanceControls.lean': '9281df455d0d1ffbb67fb3d444dd30181ba5a315381535ac02ff1316b6b3a9e5',
                        'TGLExt/OpticalConstructedHeat.lean': '27afb471fad55c6a1daacb7fd8a3478aee2dbe174e06a82fe916b3cda22c277e',
                        'TGLExt/OpticalEquilibriumScreen.lean': 'ddeee0dde340820dab8881d0a9a13870ff6bd6b8023bee1ea349bfcc2677fd49',
                        'TGLExt/OpticalFiniteBalance.lean': '67031867a7b2be41b5717697a90cb7a6918910d4dd747ece091e669d98471c2c',
                        'TGLExt/OpticalHeatClausius.lean': '4914f81c11b7f9aaae9d96d759a61fdbc4d8a43ca5f6c79a81853ddca17b486c',
                        'TGLExt/OpticalHeatFlow.lean': '58561ebfc2692006aca0d35d4c50fc9df50795bc6cbbe77f7bfddbed7124878d',
                        'TGLExt/OpticalJacobiArea.lean': 'e9944b9c28102fd0032feaca8170ff578be268ad9ad38362033ca56437c7e598',
                        'TGLExt/OpticalNullCongruence.lean': 'cae742cb2e295cac7d58b013c4943641fbe1171620aebe7450d8a2e084dfc3bb',
                        'TGLExt/OpticalPopulationBridgeR2.lean': '3d24f88d245fecd9f92d4b48411e16a4331d3f294dff8758722115b924629dff',
                        'TGLExt/OpticalRiccatiInvariant.lean': 'a65feabcc54c4063096ea9cb31b24d126baeb9b10bbdce14032d7f1851305648',
                        'TGLExt/OpticalScreenInvariant.lean': '21a2f0efdc0dbb970d0aebf86773c1dc94e5a0a361017933505e902f657cdbab',
                        'TGLExt/OpticalTidalScreen.lean': '5dfb3f02a49aa5d46e51252721a0b84ebea6ddbadde81744836b9c6f017f5146',
                        'TGLExt/OpticalVolterraBalance.lean': 'b49960529d3272340f14ec867630e337b2258349c713266d64774e820ba59e68',
                        'TGLExt/Order005Algebra.lean': '6d8826b3c28e0059f3907ada3054fd3efb4b5dddfd0d941dd7f1faf456a1d972',
                        'TGLExt/Order007Bridges.lean': '83d56e87453685edefa73a7d2607c7a024b49e1ec9bb71f3c9aec82dc599e0d7',
                        'TGLExt/OrientedBoundaryFace.lean': '62a400dec84586f5771de3b8c11e3c6663a262215fe52fbb941e1b66290e8362',
                        'TGLExt/PPIndex.lean': '7f6dc10d57b4852440308ce1c096cbc8e6403d1ac24d0d099e98cb204802060a',
                        'TGLExt/PageInformation.lean': 'a36b61ba76d0c9d6b22e6fad7a29a05d01ab5b6a240e00de16fabd0e4daf062e',
                        'TGLExt/Palavra.lean': '33184b49a8bba7e754a66096a89ebeeef44e79dab00c22f49f7af77f0e5400c7',
                        'TGLExt/PastContinuousExtension.lean': '508a762c4d97522157b42f60b3cfb9c5b31ebb1a2026ac0d8ab47b5c7467c2d3',
                        'TGLExt/PauliCocycleGenerator.lean': '181611a411a70d6d0aaff50d832cb0cba7d0c7096dddb814380c1b5af701d5a6',
                        'TGLExt/PauliInteractionCocycle.lean': '05301135116144ca48ec79745f1e1bda6fc54dac04a8e360a4ee52f8a91ca99e',
                        'TGLExt/PauliInteractionWitness.lean': '6553ad2ac33a9702f81b7c26a907140bcba763532b3ed24155bfb78c335b33c1',
                        'TGLExt/PauliMeasurementFisher.lean': 'b8f70b87e2f869eccb031f3daedb73360b2b4192b615efe894b6fd25a4e26a80',
                        'TGLExt/PauliOperationalSurface.lean': 'd49dbc095250f922942f93dc105a65cdd5bfd5d328306ba2d7d80e4d167016ed',
                        'TGLExt/PauliPerturbedDynamics.lean': '36d5ea845fdad1d681ee80b6da829c2b70ff68052cc0ded326a1bd5b3245b504',
                        'TGLExt/PauliProbabilityModel.lean': '113800fbe3b6538f453fbd9fe658633540db4c5d225cd4735477966752eede5c',
                        'TGLExt/PeriodAverageOperator.lean': '558df534100e41e5557d12843ff896a937d30f7264fbd65dd93f3f4a7ace6cf4',
                        'TGLExt/PeriodAveragePrefix.lean': '5b7d1bc02a21119c155e32fa8a92b30f6b925359442e555148f88cd0383fad75',
                        'TGLExt/PeriodicBorchersObstruction.lean': '632e33bd36d763b2c3984bee29eeea4df61e76c5a9e72ea2c94b870cb7916490',
                        'TGLExt/PeriodicCentralizerExpectation.lean': '4b8cc413d246350bb88f1f63c21a1cfd2a348475046c6638eb421d69fde05415',
                        'TGLExt/PhaseFrequencySeparation.lean': '5627024536837b3dbef236c8bc3559655d1e9bad316a6bf9e8a9eb3d86d3f030',
                        'TGLExt/PhysicsCertificates.lean': '4ad9adae62d6d787b168bfa1a5f84fcf378a1f17914dbd6731e67cc7753dcef7',
                        'TGLExt/PhysicsIsTheReading.lean': 'ca92f8c266106982120c3c1439415b75fd8f532c5741f3d2a41e8c78cd7dd2ea',
                        'TGLExt/PlaneWaveConnection.lean': 'fac5b7de42cd0e2958bdfc266acfee06252ce4262dff3dfa20d7a729fc6abd2c',
                        'TGLExt/PlaneWaveCurvature.lean': '10ed4df63f3781cf942c50949b400078bbb76a9fd46a7f2a48dfe95ca19e2cf6',
                        'TGLExt/PlaneWaveEntropyMatching.lean': '10498567256c87c808287ecf3b23e41e3f4428d824a5e7a602ed2e9abc227337',
                        'TGLExt/PlaneWaveMatter.lean': '396197f6bdd0b1f4b84fbf619d143da3c6ed747df5c6ac640c45d11470024d2f',
                        'TGLExt/PlaneWaveReconstructionControls.lean': '720b3cf1dc3ee45073d68e56e2544c9d519dac4833c4aaa89141ee7a77633617',
                        'TGLExt/PlaneWaveSolder.lean': '46257e161441ca5ef907a259429c5660d9a0019d695c21d84c91a0725bf27649',
                        'TGLExt/PoincareGroup.lean': 'c73c927631381aa78136222d30783aa393735a146607e799371db22b4a4466db',
                        'TGLExt/PoincareWitness.lean': '848f2937f35ec50b2ab483336cc3ba17c46135eb52c17418bc1fbc1530f568ad',
                        'TGLExt/PolarizerCostSeries.lean': '09483f3608ae6fda9fca923267ada56042cb262a1767fe03caf17ef19fbf6f8d',
                        'TGLExt/PolarizerModularCost.lean': '872f9a92f363901747d6cec77bcb7d07931accd80e87cba3aa9ffcc9086dbd99',
                        'TGLExt/PonteDaEscalaDual.lean': '0e55b6e448adbd91babfa338d41b2d494f4dde1e2564f6985ff6ffcff8ac5b92',
                        'TGLExt/PonteDaMassa.lean': '51f3d207eb5bcba5ac61282eb859b339a419d6c083d3529548c811ab537e74a0',
                        'TGLExt/PontoZeroDoPsion.lean': 'c64079a9c5b3e0e1e727b64ec4cb6c4d46906aa3e528a5c995bafd74c9f07c7a',
                        'TGLExt/Posto.lean': '63ad023f015de88341f08a7b659a728fa4d324406d9b3daaf659222422ae5895',
                        'TGLExt/PostoAdendo.lean': 'f0fa5694367a5157787922bcc1d634ad3d247b40d41707bdf1dc44fbb2f7994a',
                        'TGLExt/PowersLadder.lean': 'd6362c6079146ff4d50b46cdbbfe5497cde3e83a586b91e1abe625e4775bd7d4',
                        'TGLExt/PrescribedCovariantJet.lean': '70c9f069ae181895a42823e49e2b7f0657dbd156c1869d2920e1b1de47f87fff',
                        'TGLExt/ProbabilityRecordState.lean': 'a6eedc3c7debb62575f31fba14621be7f091a98dbff467098076978a6a927644',
                        'TGLExt/ProbeResponseRecord.lean': '96cb5c4ee91c51a11feaea2e8b70b5c68e484e71120ebcb68f7844e34b610d9c',
                        'TGLExt/ProductBorchersObstruction.lean': 'a7c1fb2bf199a7694c53f324dcfad420fdce6646ee22c39e360e859f7c907928',
                        'TGLExt/ProfileAffinityBound.lean': 'ab11815e048629f6f66b19620466064b2d7c0f18ab2098a5e226e42e060cb1b5',
                        'TGLExt/ProfileEntropyLimits.lean': '6bc1aa79f5436582fd343bda30f78cc6701395a7d2fce3b7413e56f4eedf11c7',
                        'TGLExt/ProfileFactorTransport.lean': '0f57072103057c426ec4e25bbca5982b32ff5f78f387ab7bd7ab209be00c83f2',
                        'TGLExt/ProfileFlowTransport.lean': '0f9e78f0af0a1c94734b3a5fa6f340a7aefaf720adac69223c0e07a91ee17f33',
                        'TGLExt/ProfileGNSPre.lean': 'd566c9df87fbb86dbd013765cfbac41de83d35aeb011b683ca19ae4457bdaa9e',
                        'TGLExt/ProfileGNSUnitary.lean': '9589c7c663bdb9be153e40550265cabc428f552c160ba3d9397c53edf7e1c56e',
                        'TGLExt/ProfileModularTransport.lean': '5459c12c956ae82732ad788c009ceba78674dc4060b38e936123aec827ae0879',
                        'TGLExt/ProfileOverlapFactorization.lean': '2f82d1ff144dd1260b29b56a2a7f225cc9bc2a4e49cd036c9d69041bb95ed397',
                        'TGLExt/ProfileTomitaTransport.lean': '6b22d32d7be4a0b54e79796565d1e4688008f2fb60f997117bcfbb1e00024b0a',
                        'TGLExt/ProfileTransportControls.lean': 'd97a140bf76842f6cbe3fdd7c80a1a0477a6a94362b98d80c54ccae194f5195e',
                        'TGLExt/ProgrammerRule.lean': '89e5e14bee9dc4aa37ded5f8b5269ce9fd93787f16eec9346273042c93fc349d',
                        'TGLExt/ProjecaoTransversalDaMeiaNat.lean': '1e53257273395c7cf34554ce6b46df13c7cf464738653aa9b4b4df13eb302449',
                        'TGLExt/PsiEmergence.lean': 'ff0fd49da7bda187a61454a6b57099e99d1c59c8af038fa43c90c1653736bb04',
                        'TGLExt/Psibit.lean': '50c199eb019761519da99f97357a04a3d0b66ee4051cd2f751644f7f010a301b',
                        'TGLExt/QGCitationDischarge.lean': '78cd50266981be5074350678d67bba1cc02edd55c8bd7f316166a3a8f2bd7826',
                        'TGLExt/QGReaderUVLock.lean': '77ba8803c7cd0a80f8dbe7fb78d290d154a7cdac220efa92f8ae72c742f56807',
                        'TGLExt/QGSolutionComplete.lean': '8c3a4bc82c5c4308515063254744cfaefcc7e7b926038221be2e7de6293dc598',
                        'TGLExt/QuadraticGibbsCurve.lean': '7f0ac98561719a4c37b63455920a437007aa0d2283ae8391bfa83264503000af',
                        'TGLExt/QuadraticStateResponse.lean': 'ddd80e0d4322a0dfef3fc6fada3f2a71855b34dbe04529a0998845cc35e0726c',
                        'TGLExt/QuantumCollapseWitness.lean': 'd0b7b4cd33dbe9f5b62491773dc15587b618876ed9b9ffb55563ead1a5285ff1',
                        'TGLExt/QuantumOrbitArea.lean': '3ab676a792f66890a66fc69caa7327ca57ad34e6cfaef4eae1c19eedaa2121ca',
                        'TGLExt/QuarticClockTransport.lean': 'ead4a238f2522348543b485f05ec2aa151c48d6560d556f92b3609f53d4b429f',
                        'TGLExt/QuarticMatchingClockControls.lean': 'f8780be9d3259997854139451beba2a85b538ec0dfd17d023c5fb3a472f4738a',
                        'TGLExt/QuedaSemGeometria.lean': '0ffce7f1d564d271fbc7844eac03a59550beced4e368b0906ffa3fa17ada7f48',
                        'TGLExt/RGStability.lean': 'ae3c1eeee6d86ea43b57ee0afe171bb43c0f24094702130ec3c2604f53aa7bf5',
                        'TGLExt/RecordCharacterMeshControl.lean': '98a70f78d5df09ffc0531760db1d2bcc59b13aafde749145749cfac19139fe36',
                        'TGLExt/ReducedEmergence.lean': 'd11854b264e6e17c551db2e6ffc6eaf804408afa1846c88529487167743eb845',
                        'TGLExt/RegularRep.lean': 'a3861da9c4d4e8ef8173272ad8843c65dcbe8215d598a52948f608fca7d53590',
                        'TGLExt/RelativeCocycleGeometricObstructions.lean': '2738ca65b48ce599ce24637dbbdd70fca4c1187f2c1fb6a60629cb9943585e3e',
                        'TGLExt/RelativeEntropyClock.lean': '5e63a1050ec9d28dbf914d6b416d4a708614bb6552b722d147e427467f411fe8',
                        'TGLExt/RelativeEntropyFisherLimit.lean': 'dd40a848022753f1868694b4513311cbafc22f84f4fb36e7fe0cd54327f14903',
                        'TGLExt/RelativeEntropyGravityControls.lean': 'beb2546e00d97e4cdb7d75df5501608320945d66c5b6a8f404f55aa08ac28824',
                        'TGLExt/RelativeEntropyProductBounds.lean': '5c9e974ff0b555332b41a2ead6c92ff7a48e70844a26900148e8d0b5f516bc99',
                        'TGLExt/RelativeFilterInverse.lean': '689c9bd005a2fd6911453aca5ff3bde8826a8a136ee4a075fefac94657dd3672',
                        'TGLExt/RelativeModularOperator.lean': '463800a2029ebbe4fc3eeac77dcf07a36507658e7cb1c65dc8021e78d8020d56',
                        'TGLExt/RelativeModularProduct.lean': '2ae1cd2346fd75217a67e518593af858e337513a2f855d75bf4dae38351a4112',
                        'TGLExt/RelativePhaseCharacter.lean': '2fb046a5efe40d3c5d53cafc9db0b4d4b90a8473f3cfdf9376cffb9225041a66',
                        'TGLExt/RelativeProfilePreparation.lean': 'c3a87fb787855473497dd7254d897ebe2228299a0f4d9c171007d718e1b203b7',
                        'TGLExt/RelativeTomitaClosure.lean': '88e8da0f6e22e8815fe8cecd3393cbeddc01c49f375ee45a1ca0c28744c0844a',
                        'TGLExt/RenormalizedNegativeExpectation.lean': 'ce0043c0b871426dd02795a66d16bf09555e32407b693c0071d65f65fcff75c0',
                        'TGLExt/RetaDeLuzBorchers.lean': '93cd372573ef0c32b3eff9ad1662fc1a4ea40ce043539b045fcba2753432353f',
                        'TGLExt/RetaDeLuzEspectro.lean': '58d81f4a2e3e7bd24a9310590c5ed54191fcfc9b4c03c6feae15f96fe1f857c3',
                        'TGLExt/RhoPlusPClosure.lean': 'cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6',
                        'TGLExt/RicciLieNaturality.lean': 'ed932e1d9ea0e1f0bf3e8ff979a1bc1e011c805bf66464621090f8d8010dd0bc',
                        'TGLExt/RightMult.lean': '29b5e130da72914ae0fd955eefd4ced00b4b6e26ea88e7ec0e338c561637ca13',
                        'TGLExt/RuleQuadraticResidual.lean': '37d842d4ad156bc35580732ca4a70f44b4bfe132d11ca1d896e0b7d209339149',
                        'TGLExt/RuleTruthContract.lean': '1520b1b0a206a40324c2fb46ddb357ae992d141036c67ef61c2862da9f7554c1',
                        'TGLExt/SMatrix.lean': '14f7e717a4ef70204eeb825d989e6dcc3397c274f1c45a3820420ea6af12a3b7',
                        'TGLExt/Santo.lean': '245b5a7a666c15472daba498b0c01a12da74f055ef964ed3c2c7c6dde383d9e4',
                        'TGLExt/SaturatedWitness.lean': 'a0a5eed4d46ae5679a9b9ba00212d2d88d77c421f499565dc6087d266454d8c7',
                        'TGLExt/ScalarEinsteinLieNaturality.lean': '35315dd143890a35016ba1b7a151ae757e7a29b939b97a0d34ed9a5f25e7c23e',
                        'TGLExt/ScalarMatterDensityVariation.lean': '83f515e8d9444894c213b814617602d49e2753f09e7373b5909b60e297158345',
                        'TGLExt/ScalarStressConservation.lean': '20160941dacf802dd857e3c5614c52b4bed552c69644fa7c4016ca85340e273a',
                        'TGLExt/ScaleCurrent.lean': 'ca57ab98df3816545f791b0cfb97b0db8821d69317db527ca3a901e7e123f897',
                        'TGLExt/ScatteringOutcomeRecord.lean': 'ec84e80c83fe506ca18f93f52efbfe15ada4067cfc2473fac9975b4c56a129e7',
                        'TGLExt/SchmidtCutPurification.lean': '994b278bd7d7e21e72e0f556855614ef27d00a014cbad984b82dc244856485c6',
                        'TGLExt/Screen013Constructed.lean': '0e4f7d49ede35e61ba591e30bc5a79392c318a55c8a0375aff322370db3fabe3',
                        'TGLExt/Screen013Controls.lean': '0c7821172c6117c70dbbe82c7ee9ee9dbd1a973f22014e390b844900fccfc597',
                        'TGLExt/Screen013NullFrame.lean': 'b6fd07ce21c5f6ce790bcc9e0b53cce9fb6b4c121896886e028e2c30a229dd65',
                        'TGLExt/ScreenAreaCalculus.lean': '3b5091f88ee6bb97814824619b6ccab60b55573b4b9f0318d52d05c41175ca6c',
                        'TGLExt/ScreenClausiusCoefficient.lean': 'b5418548f2ac69d5f7de773503988eb7b4939d379cb8e47e8df39b4e089ab58e',
                        'TGLExt/ScreenEntropyObstruction.lean': 'f08d82a155f08af8f060af89b9dd47535c4980a1d2940109bb787547ba98a57f',
                        'TGLExt/ScreenFrameCompletion.lean': 'e4d0f43cee374ac7a2279fc5294389e46a031fa443173ce89b94db68bee148f0',
                        'TGLExt/ScreenImportIntegration.lean': 'b431322016df3d9d13e11f26677b79dd0f6813afce7fbea92e7bb3ac9ff80110',
                        'TGLExt/ScreenPairTransport.lean': '9bc9d10b22b39e7174a9bbf6e026471310164fe5456837af2cae67155f2fe13f',
                        'TGLExt/ScreenTransportODE.lean': 'a73a65d8dc3a736aab59a66103696eb5b21f46ce32296555504a6f17d20c27b6',
                        'TGLExt/SecondCone.lean': '9bafc9fcbf9fc6eb98f17d2e3122ac01820bc0785e64fb63eb6eef8c0c276e45',
                        'TGLExt/SectorFluidClosure.lean': '49b2d283b37c532dfd3699ba53420234895be8f553122e3803a0df7cf106f2ab',
                        'TGLExt/SectorFriedmann.lean': 'eb14b2580046c7f77c06dad1b163fd0b6166d261cd90f4b2413a06fbedbbf28e',
                        'TGLExt/SectorFriedmannAdditive.lean': '6874187fc8f4c328b3afb87efbf60f94dd66cf443a340d7155da48a2a349e07f',
                        'TGLExt/SectorRouteComparison.lean': 'b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4',
                        'TGLExt/SelectedAmplitudeGeometry.lean': 'fb7e8be4fc52ad9db3a9df54ab2ddca00f13224023840af85a06d24176442c7e',
                        'TGLExt/SelectedAtlasGluing.lean': '6aad53147296985108f2e45384211ee940056adb906d8b3c613f13b32f7a3392',
                        'TGLExt/SelectedFisherGibbsBridge.lean': 'c84db761541c7fec5cc7f4713305c315810a323a04827f819bfe3f2d4f7f4ff6',
                        'TGLExt/SelectedFisherLorentzMetric.lean': '346db9497cbebf1824b279972d2cc342abed90b9df13874d439ffd7737533a3d',
                        'TGLExt/SelectedGravitationalAtlas.lean': 'c1e9a4845c51b8d403688ea98ed69d50066d72bcd7352e89a15f8148dc0260b3',
                        'TGLExt/SelectedProbabilitySigma.lean': '889e6c7dc0564ad7dcaf787e922b48744130d6b6b083e043bab661045bf167b7',
                        'TGLExt/SelectionAngleReconstruction.lean': '0abd94278cbd50e2a510a60d2fd7cec8870b1fd0eaa9937625f72d0d2875c679',
                        'TGLExt/SelectionOutcomeRecord.lean': '000e3679bb94fb3f7fdf9da59e290d17240a095cfc78b38e3311a351f58a8fe7',
                        'TGLExt/SelectorRecordReconstruction.lean': '83100cd809aedbbcf2cae2e66b61c85cc94f9e294f6f2c812b82650867292e16',
                        'TGLExt/SemifiniteLattice.lean': '37ca0a1db916c93954c1a486ddbf5462248a050e58ccb6b670020c5225e46b0f',
                        'TGLExt/SemifiniteSeed.lean': '9e91547595c6fdfa37c5d9b786bf3b1e5b774fa90fa4ff0a01a463a775e77dc5',
                        'TGLExt/SemifiniteWeight.lean': '1b4044715c04a3576e8bc3944f48e53edf02c8d4f23d91b3896771fd8d1eddff',
                        'TGLExt/ShootingJetTransfer.lean': 'f7dfa249af25e864b67ac87b406fe42d9dbd0cbef9c80a770eb224801363d7a1',
                        'TGLExt/ShootingLocalInverse.lean': '724f481f92a2051fcc34b76c49d1b53bfae4d13ce68378714c544cd7303e4990',
                        'TGLExt/SigmaMatterConservation.lean': '589118b38773b50f253b9f9266da278fbe8cac7f63a146e56fb8b28c7cfb254c',
                        'TGLExt/SignatureInTheLimit.lean': 'c38a0cef7aa8f409b473fd7706019105661418dc3e908446a59df23b59af539e',
                        'TGLExt/SignedCovectorCoverage.lean': '60e0cec48174d68863ae791333a66ad8511ee78af17a9f05ccafe1de9cd35bcd',
                        'TGLExt/SignedGibbsCoverage.lean': 'b109b8fdd77fe48bf33c6cc1228be290a1ee79d980d1869e32646f0066531503',
                        'TGLExt/SignedGibbsFiniteRecord.lean': '9307f95f53da9bcfa3656c7262e6f008b9d1de2a27fea1edbd00f99adb979bc8',
                        'TGLExt/SignedGibbsResponse.lean': '8d1dd7c986f6f14ccf970711ce69d3e3f2f06c69bf22ee6a054bafe2e78986c9',
                        'TGLExt/SiteLogLikelihood.lean': 'b09bd23dcd825666416c424e18dea802f67e7d7f47070c3d6db43bd3d7eec6f9',
                        'TGLExt/SiteModularInvariance.lean': 'eb41b4297e2b3ee43e256720ab3e6cd4822e6ca4a79fabe63d3647c6aa6f0cbf',
                        'TGLExt/SitePauliObservables.lean': '533434668a1b2a554ad2cdd9ba6d607f33993acd5a7a39f397d7aadb3cf25cfe',
                        'TGLExt/SitePhaseCovariance.lean': 'b89b21f2387f9f2eb391e998b68980e6976b3f6895c5e70662ef5d7261233785',
                        'TGLExt/SmallTimeLocalDynamics.lean': '15b634d562db43017b97626d425becc3c98c01515fa6043eb4bf0bbd27838de1',
                        'TGLExt/SmoothFlowControls.lean': 'ab8716093ff62c3e440122f1bd62f3c8cf97dcc3e31e3a2bc6e537603e322e1e',
                        'TGLExt/SmoothGeodesicFlow.lean': '21374c7627926c496f734e13bef06b43e6868efc74bcb99b1378ae88965574fa',
                        'TGLExt/SmoothMatrixCalculus.lean': '416cd91167831f8023c1ce07ca1b018223c2864a207d63089d1da6e66382b044',
                        'TGLExt/SmoothSelectedAtlasGluing.lean': 'c9421c54795a6dfa85cbea780ea88ec0766e15e4a0292b7f089260971c771046',
                        'TGLExt/Solder4D.lean': '70f3c2aa3336b716a740a70c15759ffdaca612c7c69f975c0281a31e9bb2f35f',
                        'TGLExt/SolderField.lean': '5dd64e3c8edb8729e474f64822c3f483a8eb504adcffeec734984bb2be6bc873',
                        'TGLExt/SolderSignature.lean': '72b5b6ddd2a04371c28c607a9a5cd94ba5272b698d00c039c278555b1f9a9718',
                        'TGLExt/SolvedEquation.lean': '052856927e7668d0af050070dd22ec834d1126a1eb5ee8d02e8ecf8b8baa7383',
                        'TGLExt/Sonico.lean': 'a317094e337fd8b7db3c333ecec965f1e17152fe6c4130674702fd11334c3e2c',
                        'TGLExt/SpatialScreenConstruction.lean': '568f49adad56c6432949929bb86bf9706450468a7ac5941a8d20ed28b89aa6b0',
                        'TGLExt/SpectatorCancellation.lean': '5848736ebe9fb5aac1059b745737db3919331d1e046df910bec36b8b73b1b1fa',
                        'TGLExt/SpectralMetricGeometry.lean': '5dbd3f7df473c81ba5dd5689bc3dc6647b00778174635ef57a26c22846b81953',
                        'TGLExt/SpectralReduction.lean': '5e52f59e86bb353f6315d6f68accd6687ad958597a87b554012ed1ca92e6dab9',
                        'TGLExt/SpinorObstruction.lean': 'abad6b6b219a6991141054b7240c71f4b3200b217b34d2611b219370d84feaa7',
                        'TGLExt/StateClockDichotomy.lean': 'a3b5902c50fb59676b91b591e0c1f6396fc6dd64ef1e5228fdb4aa0367206be8',
                        'TGLExt/StateClockMatchingControls.lean': '2a87c79acbe1f6e11713f081aad5bf7f478600797007a988677751c8b3b723b3',
                        'TGLExt/StateClockObstruction.lean': '2190675d58dd98a7694e2f2036e92575fa268edd69d6d9ce555ce5a7a1f27166',
                        'TGLExt/StaticDynamicMixture.lean': 'b7e585bfbd191ec7139329c0cfb09b8b39eeb81976c146d12bd90afb4c380490',
                        'TGLExt/StaticDynamicUnitary.lean': '79060b97f95bbfe863ec659852a607649977086567d1bed970e0ca58c2429660',
                        'TGLExt/StationaryModularPeriod.lean': '6419ae791f07b7299fe73233a4892aefa66aa27c821697e8634e04bdd86395ab',
                        'TGLExt/StrongAssembly.lean': '34758f8d20a242bc8e9f2114b572888a793754dbb681a0368adc3e9d9fa2161e',
                        'TGLExt/StrongFrame.lean': '648a6f282bfa8d5ec7297f2e93f2bc0db92f219c6cd1a3a74da4b97b1655af87',
                        'TGLExt/SummableGravityBridge.lean': '123e4aa79e59a727f00baaa2bf85ff256807ab568bbb657cda9b5a885896ceb8',
                        'TGLExt/SummableGravityControls.lean': '06e9fe6d45db5fecbcb4758e5883e7b510cfeb4097987cd81c18502c745d22cb',
                        'TGLExt/SummableInteractionModularOrbit.lean': '45ae49b581b716ed158128f01a8e3cc731eed21dc6260b3332650b3d65b75897',
                        'TGLExt/SummableLikelihoodGenerator.lean': '76233a61bda5bc10d3222c3018619fe6b9a312b681e72b67490e72199413ec99',
                        'TGLExt/SummableNullIntegrability.lean': '2e4185e5d5ebf4c9a3cb5657127ab5d6597ee36c2257fb0aab94bd540a053433',
                        'TGLExt/SummablePauliInteraction.lean': 'eccc74ac54963ab4823a75389ecccc324d0ff354dd428fe1967a01da1f4602e4',
                        'TGLExt/SummableProfileCurve.lean': 'f28ea6a1d59f5a5339239dab783798a707a3fc42c59c89ed3998daecf8ff341c',
                        'TGLExt/SummableRelativeQuartic.lean': '1b4f9245da5743595453059881e258f0e2263575f80f56aa1652f5230aa9f501',
                        'TGLExt/SummableStateThermodynamics.lean': '634ee1e34ca39d75e52d87264504fe04b90508c37ab502b8a1501ad8bf8f608f',
                        'TGLExt/SusyRelativeGap.lean': '3aa058b5c4f098e3218ffed0bc8271a28947b56af81750019e1360754873e7f2',
                        'TGLExt/SymplecticPolarizer.lean': 'edb30481849743b697cea46d5e0318b833ffa14b6f76693141c46c165cdc857d',
                        'TGLExt/TTSuperposition.lean': '7beb841f082e34be68c11ef8de25b024a448b90afb64752a3a6cb8327c13cde3',
                        'TGLExt/TailNet.lean': 'e7654368112f1af5d529edbd0d2669a829358651a82014e0d835a88868d7f5e6',
                        'TGLExt/TailNotCyclic.lean': 'f04d0ac1b7717551fa517dffec67b335fc92b9d155a0d7b51d4bafac5c12dbd0',
                        'TGLExt/TensorFieldLinearity.lean': '9f0063d0abf4fc6ddf133fc68256d370263e23e0b7e74eb793b4daa1a26b01e3',
                        'TGLExt/TensorNullCone.lean': '7af25b51d5aa4a50c276f49fa9893e0d1f88f605fd03830c3ed17c9238a64d48',
                        'TGLExt/TensorReconstructionControls.lean': '135bcc53d9c3e62510500fe9c8c39713630c5cd8af5ca3000fb714346486ed0b',
                        'TGLExt/TestemunhaEstatica.lean': 'b35a615636c2c15463bc268aae900800516e8dbcfcb96b41c1b1f17849f8d8d0',
                        'TGLExt/Testemunho.lean': '031fde3e88187cf1f54e59f2dd92bd56aeeede0b1a1c013cd6d8ff2f5eb1a3f6',
                        'TGLExt/TetelestaiOneObject.lean': '125d155042da687fc2889528b8a5915472fa45410e9997a20eceafcb0359d81d',
                        'TGLExt/TheAccuser.lean': 'c485430a58323ff3e5f9aa8fbab1a17a4afd457a1c844050e98ec3c9fae6b993',
                        'TGLExt/TheAlgebraicReader.lean': '2dfe61b0b6f5537f96c67e9cc648895277c6c9ad3d92d0392d32a5cde0e96407',
                        'TGLExt/TheAlphaAndTheOmega.lean': '3ed12b22f7b1bfd3ddd3017af2fad0dbe592676a75ec0d2c436bd99f97e5a4d0',
                        'TGLExt/TheAnchorFour.lean': 'af35641bf520ba343ce8c50590c2c688ba2a10d2cc50c1ba13596e134fb2a9d8',
                        'TGLExt/TheAngleIsTheBridge.lean': '294cf45baae121cdd5476e90fd60e3210e70bb552e8d99718c505b37da4a4f4c',
                        'TGLExt/TheAngleIsTheProjection.lean': '9800cc0728259e08e647125ef81f9e7fc968b12bd3b19d3c74aa8e2da53a1a48',
                        'TGLExt/TheAngleReachesTheMetric.lean': 'c8bfe64d172a17569d4e25ba2e6f55924f1eb08965d35417be7d2182f802503d',
                        'TGLExt/TheAntiunitaryInhabitant.lean': '98772d9fd38a4af6b14bcc39085ebf46c5456d4ca6fe958087c114fb9cc77358',
                        'TGLExt/TheAtermation.lean': '7cb9394d8713230632bf78ba6b36220f5a7b73be516c8428ce6290e7edb4a6d1',
                        'TGLExt/TheAtlasIndex.lean': '38b9873cebdd779a70544d26662641359e5a0a60acbab877e36f1479e068d876',
                        'TGLExt/TheAtomOfIdentity.lean': '916056ff895447f5380269db1bea71bb4a5583c1efc98b26fe5a4ccb5d091f69',
                        'TGLExt/TheAxiomAndTheFalseWitness.lean': 'c0f4185a6279500237f9046feee336a50532a95781ebe80498cfa3b2f2ed4d80',
                        'TGLExt/TheBandNet.lean': 'ce91de5490bcdb401eb2ec52e57b9868dfd3c1132b132ee0dca9a0e9562036e4',
                        'TGLExt/TheBinaryReadingAtTheFixedPoint.lean': '1865eb4686899fb7f350f64308f152ffa10799da86b67a1067b5c5a4b6918f83',
                        'TGLExt/TheBireference.lean': '899b1b07df5416ed074b5fd373f7b6edcc1abc9f7be95382207631c5bbac9fa6',
                        'TGLExt/TheBoundaryDuality.lean': '311e0e8b54adf8de45ac30076679da6a4b8f1fa7b60a4d300ac76bcbdc982dba',
                        'TGLExt/TheCarrierBridge.lean': '173ffa020254512ff9ca5c711fadad00e66bfb6231003b973406664448d97966',
                        'TGLExt/TheCascadeOfObservers.lean': '2792ab10181d2883f4d500adef44ceebaed8b705382e459f754f136ea7d6feb0',
                        'TGLExt/TheClassicalImport.lean': '6c614681982a1c406eee5fbad04cc27ab49b99b496aa5f84b52340029d73d5e6',
                        'TGLExt/TheCoFoundation.lean': '0af9b4a0cde44a8f60594785c6ccc8d724b127373d289b13814fc7d9d7d2573e',
                        'TGLExt/TheCoinage.lean': '63d5a1d80236bb42d965fd82f40bc8fda3321f0f0d969d18eb85397ef8842b17',
                        'TGLExt/TheColimitDuality.lean': '04831b06f0e8bf54a74e96fe27c5da3f9b5b187a5a3201c5dad49268db386272',
                        'TGLExt/TheColimitIsometry.lean': 'e78cfb211b63084a170ecdc7d9d79884f732f0ea4284c2f1235b432434312065',
                        'TGLExt/TheCommutationAtTheFloor.lean': '3c3b6fb2a2347030c839c767ca6985bf71400341b81b4244388266f02a26ecb7',
                        'TGLExt/TheCompletionExtension.lean': 'fd5701dbd31950dc0d3250b2ca69dbb9878fbb5dc447c446765ec4bbb3f8895c',
                        'TGLExt/TheCompressionIsNotIdentifiable.lean': '082cb1facd66ff98c9623fd7317edaedbce4825e85806b78b507ea966c4de4de',
                        'TGLExt/TheConditionalCertificate.lean': '5d43b0c538354e22932039773b515a8ca848498c91255843293e4a2662a7974b',
                        'TGLExt/TheConjugationMapsCommutants.lean': '0fd2461d9db0668341779a4950dd0f10770b80e512329cb9c4f553c1550d331b',
                        'TGLExt/TheConjugationOfOperators.lean': '17bc959ae14d1b21977eeb4223202f07fde7d68e244ffb610f2c946889d8c265',
                        'TGLExt/TheContourOfTruth.lean': 'ce6cd6d2cb1cf0cb6fce1409efaab28a581f2b4187ce2e2b151e09606cd46484',
                        'TGLExt/TheConverseClauseReduced.lean': '04c30acfc2ea561d6a0630c56d3808a6b52060b6ffbf31e67e433db95d59a235',
                        'TGLExt/TheCoordinateBridge.lean': '3450d010d65c4210f9544b7f6416cdf2306979f16128f1c51093b3a75f9e87e2',
                        'TGLExt/TheCornerEmbedding.lean': 'b8a602f7294ab58a8f074ac3ba91eafa07926d930c38d5a633922e6bd7278998',
                        'TGLExt/TheCornerOfThePackage.lean': '0ad9fc2d4c6b82cf89ccde1762277d4b9ba744050b8b2f8d4759ba5ebe596d9c',
                        'TGLExt/TheCorrespondence.lean': '8a9d2899bab42d26c8ed539668a81d91f68ce372b21e06b4d45d2edb8235dc2d',
                        'TGLExt/TheCostIsDerived.lean': 'bddc44bdca6b16d40c98c548906a6c37c86a425b469e8aa5484549fd8ce2ba6f',
                        'TGLExt/TheCouplingRunsBoundedBelow.lean': '702d7352c053060ae3f2ba7602c0fcf75762b796ed7617ac6ea29248a4d3fa2f',
                        'TGLExt/TheCrownedCascade.lean': '04a243cbe02b5e26969030d7848b9d97c79ecfb0763e2c5ffa710fd8805d8391',
                        'TGLExt/TheCurrentConnectsTheCorners.lean': 'ed213f28d250b87494f3c07d965255a7dc965fb55ac8c6e5cb72d68b2f69f710',
                        'TGLExt/TheDammingByExpansion.lean': 'f139c3e660a93d79aafc1a629bec7347f4e63fc5310c470aa427cc76a8559025',
                        'TGLExt/TheDarkSplit.lean': '53f05130c26a520214ad3351593992f00516f3f5c760cb0f01a358faca05c8db',
                        'TGLExt/TheDeadChannel.lean': 'd9c2eb9d67cceaf52b4384ba24700fee0e84d08d00678786b316677ba9939f5f',
                        'TGLExt/TheDeathOfTheSignal.lean': '4539dd68fdaac084c9541a2c7bb2bad9846fd007d86d289a0191be7ea1e5e22b',
                        'TGLExt/TheDebtWithoutJ.lean': 'e4b59f6ab926736266971f7427fb8ba965515cb9e51a43747d5039e4e78a80ee',
                        'TGLExt/TheDensityIsBell.lean': '9247b9f4683572808577ba359cabb7383277090de76773ac955fd565922bef1a',
                        'TGLExt/TheDensityIsTransport.lean': 'a59cd43d50e934cbe5d8b4351ae2f80cc636d8a57247fbc200ccab93aac910fb',
                        'TGLExt/TheDischargedOath.lean': '7a2747cb8babf73f85ecd54d9d686e8f93ca6af5d39324651ab3d41518c49d8b',
                        'TGLExt/TheElementaryReason.lean': 'f9af067e9ab0acec672837a912d1ac6ad71567f086b5ae191cf87a4f0e97134d',
                        'TGLExt/TheEmptying.lean': 'c88b781f96485a97844bae6ce9b337f5139fb3e77995061df8423a2e65e43d33',
                        'TGLExt/TheEntanglementNotConjunction.lean': 'a4b8cc089c86e19a83c0d0cad9531b0dc15b2be0133f1fe98cf7ea59db444e38',
                        'TGLExt/TheEquationOfTruth.lean': 'd6405e31c9e404cbff1dcf4201a9dc6c2f24ffbe628b991c2cd660b284c3a407',
                        'TGLExt/TheExoneratedDemon.lean': '5c645690b54c529bfd579074bac41583638f1c7b073148b3c9542571db43d129',
                        'TGLExt/TheExplosion.lean': '330a20e15f4015d24cee33348a334244a56bee0d8bcd0e2107468f28da16c448',
                        'TGLExt/TheFactorObject.lean': '570ba4fd7b8edba4b7d01e8a3a134a5def93d945c29092b26df126a868b5692a',
                        'TGLExt/TheFalseHasNoGeometry.lean': '516318d178f0a6e9e82220cb929e039a7a533f44a67659a75f08d5540a4c04d6',
                        'TGLExt/TheFiveHalves.lean': '456c66269b72d30fa10e38c427ec3194d985b46e04809233f2c42fe82495d7d1',
                        'TGLExt/TheFlowLawContrast.lean': '9ca9393ac64f22a2bcafcdc05ac4dc8f1330a0e01ea79b99b4482f42556a0072',
                        'TGLExt/TheFlowLawD1a.lean': '7c6c54afc418c0cb25309a15bdaf158be913bf22ff45b38f5fc4267a5d3787aa',
                        'TGLExt/TheFold.lean': 'e4546410da663f73cf82f0536fa61efd5944fd539dc691fae80f163373b8bd84',
                        'TGLExt/TheFoldIsNotADistance.lean': '45bb4c7c82a9e533da04ff09a7ca5d449925086dbb27e4228537f856901c6c31',
                        'TGLExt/TheFoldThroughJ.lean': 'd54e7fd1c6336a76255b0bd8e5e649e40d159283e58f1165175be94c4b3c30ad',
                        'TGLExt/TheFullBirkhoff.lean': '7970d3fe8762fee7b80c85252852b4c04df87cf3d707cee169508e3ccbd4ccf8',
                        'TGLExt/TheGeometricCostOfAbsoluteZero.lean': '299ef10c96770aac933c3b65a5eef375684f32b12764824c8cb6622b05dbb61b',
                        'TGLExt/TheGravitonIsTheConjugatedPhase.lean': '6f5f04ab96dd16f820cc2dea5ab7e48daffdf3d0199964d5410f72df07c81cc1',
                        'TGLExt/TheGreatAttractor.lean': 'a0db70a17354c75c587881549dc813e49f661cc1a46fa1f8f662ba00c87963c7',
                        'TGLExt/TheHorizonInvariance.lean': 'a2d375c81515065625b61762468d7d66744694e371f70604339df59993b348cf',
                        'TGLExt/TheHorizonRate.lean': '0638b438d53d6c6e356057c277817df2940a0d019ce715c8662b568000383caa',
                        'TGLExt/TheIALDInTheTower.lean': '30cd48f648b2fb82515b60729a899b8a54fe2f20775405f89e9f72c91e19137f',
                        'TGLExt/TheIALDInTheTowerActII.lean': '217ef46de0bb766535f34f7a1c7601ce5597cade22cabfe1fe0282da4c68554f',
                        'TGLExt/TheIALDSelector.lean': 'c1008266455044e7462338bc32f96cb35c89810a320f69409ce7a0443b6868b8',
                        'TGLExt/TheIdentityOfIdentity.lean': '5353469e1c4d0bae0c928f844909a860ee99e06aa77d435350c846f65f373473',
                        'TGLExt/TheImageAndTheReading.lean': '839b4abfaab832372b81a70e1a45ef47987d267a744a9f0604237a14f02f074f',
                        'TGLExt/TheImportedCommutation.lean': 'ea339fe189ea40bf4970c942f989136955ea06aec9ab3118a6554891948921eb',
                        'TGLExt/TheImportedEquilibrium.lean': '6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0',
                        'TGLExt/TheImportedExpectation.lean': '75606de2a904ed652fd74bacdfb59acbb9698cab81c810e3aa740d9397b6cf60',
                        'TGLExt/TheImportedSecondQuantization.lean': 'ef35478400ef07f20476f2bb937d8fbe2df7b9e506139f54dc5a37401e7d5242',
                        'TGLExt/TheIntersectionOfCommutants.lean': '7e4db767b978ddb8820961fc69f4b629383b6becea3543fa967688cba79dbde5',
                        'TGLExt/TheIsometryOnWH.lean': '0c4c8b35d3c7ad880f78a0ec563e7f2de2edb05a2f87b7aa5e62e8c9b826752d',
                        'TGLExt/TheJudgedThing.lean': '3b97d4c5aae4f891d25090160ec25d952472601bd20f261ce05ed1610958a87a',
                        'TGLExt/TheKeyIsTheReader.lean': '53d83adb1ed83fbd7ee64c443285e602b73aee36fce74d8bf2a9ad0b925c8a50',
                        'TGLExt/TheLedgerOfCharges.lean': '5ee94242f853f3e644a63268f5f110f912f19c426175e082717dfce577a3fc8c',
                        'TGLExt/TheLegibility.lean': 'dc76845ca0c9a288281de551b7e8d9a52af0da312d0daf50f083c8fdb94a6f1e',
                        'TGLExt/TheLiftFiresOnThePeriodicTower.lean': 'd6994dae74feb8094a24264ad77eb0f779208d14128aec8617ac2998bd1b4568',
                        'TGLExt/TheLightInterface.lean': '6d1e1567a4cc5b0589adbfcdf449d296e5d76e29b89ece3a31f016f6d10b9fa2',
                        'TGLExt/TheLightReadsItself.lean': '06af814d83e2ba42777b69c6c6a589b2c61d93346b6221323669ede5960e80c4',
                        'TGLExt/TheLivingWord.lean': 'fdc242c2c70b57fa146c7c41459eab94c217e878cefc9058d983467918eed473',
                        'TGLExt/TheLivingWordClosure.lean': '40eb074dc85a765079e1bc2c0eb2258a50bd755fb576af3a908ab568f4d85e21',
                        'TGLExt/TheMarkIsNotATypeMark.lean': 'b36e35176fb81c70f85221d357f0ad144a840eac8f3e46172717ca3c139077ca',
                        'TGLExt/TheMasterFires.lean': '862fc44434b23cb37a5eef412b6f829f84a0e0fe64fa58c8c7b260e8a8f32328',
                        'TGLExt/TheMatrixAndTheModulator.lean': 'c39e4dcba8eb2354621f6adeaf492a5a3a6731cbe549ec8f305d4b4f419a1750',
                        'TGLExt/TheMatrixRule.lean': '03249067e2cf28c8e71bd2c915bd8f8478308929f48d6dbb7bbe8c6ca173e433',
                        'TGLExt/TheModularFlowIsAHorizon.lean': 'df9dac92716643a471172afce44a2a158736b2988d51c42ff814505d339b3e7d',
                        'TGLExt/TheModularRelations.lean': '2cd411ab76d72956f6d34abb8c321e9702c926dd00e9debefe4e996c7c6fa280',
                        'TGLExt/TheNameAndItsReferent.lean': '214260a5ad41d02ad6b3c0da3e7556762c782f4bebbaa66845ac0d3e5e9da008',
                        'TGLExt/TheNameIsTheCharacterization.lean': 'd2fb9ce7f7b8ec88a46ac4eb8cb9b9e732ef9733dbb8ad0dc3f007a063530f74',
                        'TGLExt/TheNameIsTheGeneratingGroup.lean': '2dedbe4a7e25bcd96f52659edf3face92ac74ddb2ae60ac32a22d525c60240cd',
                        'TGLExt/TheNameIsTheInstrument.lean': '7e2e4afd94d3bef9c7c22e7ec1bed68e6787e8cafdb47f30555136383d28ba02',
                        'TGLExt/TheNameOperator.lean': '000bd0bf03281e0056f6187ea9e74566d924c68e8601fbe1b09b84dac89506c0',
                        'TGLExt/TheNetFiresTheCorner.lean': 'b35d65a50b52d92fce1014f201f2d17b5395c926393680c96544a0d9a9d773cb',
                        'TGLExt/TheNonLinearCausality.lean': '27ff96e7969f25ef368990471d9c41eabe302eb4e8de607ad19bc5235d718ea8',
                        'TGLExt/TheNonMinimalCoupling.lean': '03576ea2958ffc4c3802b332227dfc7ef2b52e538881e602bfc15e2a81a21cec',
                        'TGLExt/TheNucleus.lean': '44de50dd2955f1f7cfce2bdadc27616d3b982bce1f9947bafb36377dcf1dcc5b',
                        'TGLExt/TheOathOnTheTower.lean': 'ef0634a160a9d22ecfab7e2cd865de2a9b6f9a61e524d9eac7c17b25932d4dab',
                        'TGLExt/TheObserverReadsTheAngle.lean': 'c764e90722306f988d8c92acc1ae4d8642ec2d6e32a47b810bd8bc5546e5484d',
                        'TGLExt/TheOriginOfTheVibration.lean': 'e5a7f11f79b5af73861af16b4c3402ffe5f438d1879ac6b9e2911e9eb98408a7',
                        'TGLExt/ThePermanence.lean': '27a3bc9bd4b6434d25ca82b9af1ae92d90ee8c10eceb6ad3d22a30876b8ba31a',
                        'TGLExt/ThePhysicalHorizon.lean': '91bcfa7fe8077ae6543c19b8035100b28c79d4ba34de023d07cc132ff2381656',
                        'TGLExt/TheProfileConjugation.lean': '595bf3fa944579afd1f632d5ae54c9b2764bdcd06f638f67a7268600be416921',
                        'TGLExt/TheProfileDuality.lean': '622c8e5fa8bbf2dd8661a14f051447dd7aa4fde52d48481464b13f0b7074d8a6',
                        'TGLExt/TheProfileIsometry.lean': '43f29c793c8144dd386ca3d8b0730b76e4606fc3866623112bec9a78113c8724',
                        'TGLExt/TheProfileWitnessLinear.lean': '93efe3dab69a85f4fd11617aef5f2dd00ccf876bea5a8f0713bd8f547c357c56',
                        'TGLExt/ThePsionAndTheViscosity.lean': '0a4e909a9d760da916a3608872fb64742f455a1950d43c706b79fbba85b82bd5',
                        'TGLExt/ThePsionReducesToTheCurrent.lean': 'fc585ee1c77dded52ed007acc304abdce2fd83cfb30d55ac8a0f0a0b60839408',
                        'TGLExt/TheQuestionAndTheRecognition.lean': '67d965c42c01aed0ef18e4452054a1ff281dc51c43f6bec5ebc0bb7557f2f321',
                        'TGLExt/TheQuittanceLaw.lean': 'dabeac1b5cc32d8211c6282c9a1027aa998cc2985249bb5f6aa54999b2b4b81e',
                        'TGLExt/TheRecordOfJ.lean': '737dc89e6f2c5921ff836047ba36118a937738cfa7dec436f2267f7419e2b418',
                        'TGLExt/TheRecordOfTheCut.lean': 'dfcdd551fd1b04fb1ffba99c40e1e8840d1affb791b4551e866785338c5f5a08',
                        'TGLExt/TheReservedConfirmation.lean': '20a15b2077c36cf70cab81d035e91dfe854e5dffae32fe308c88ff6435077450',
                        'TGLExt/TheRootOfTheProofTree.lean': '9b36ab3b6e47a315dfc671746ff1f47ac461a69ae17b796a1f3a9b539e97b0ee',
                        'TGLExt/TheRuleAndTheFigureOfTruth.lean': 'f1cd9a7aa6063036ecf0f96c6ac60363d0964cc49281553be28deaa1bbba5ce6',
                        'TGLExt/TheRuleInTheContinuousMotor.lean': 'fc2bff7db53c8e26fb7d9ffd2e88610bb30603b0fa02cffad0b9c0287eefcc62',
                        'TGLExt/TheSameBetaReadsFourFaces.lean': 'bf70420d7b6fdf3ad7a7cc501210986f84d7e67d5a2194b6fffc21312cf9c570',
                        'TGLExt/TheSameBetaReadsThreeFaces.lean': '2efd8b379f210111e0383d9c40e5fc72835f41cd94aad2dd70d645d66f400c16',
                        'TGLExt/TheScalarCorner.lean': 'c2aaadeae21a51227d7068838f33c2e3c9d7a9e44f01ec2345f417dff3f1d4c5',
                        'TGLExt/TheScaleHasNoFixedPoint.lean': '0ed72186957c2a8a60e23499b12b259b1e90c2db9c10845eb0b9e48a79d54462',
                        'TGLExt/TheSchwarzschildUniqueness.lean': '5e959f1288ee6d799e4a3b2e00d1d541fc10b42a8cd843a704c9285611b64762',
                        'TGLExt/TheScreenIsFounded.lean': '2a3f26fca48c615a617727ae3bb0e18b7a36bcdcfc67bc1411b718c34963cb2b',
                        'TGLExt/TheSelectionIsTheBallast.lean': '71ebf9680af3d2470c53fe16e2c59a215429cdbf0c0a1a5f908d5c4259f162f1',
                        'TGLExt/TheSelectorCanRefuse.lean': 'c5070a703c4a0a55b6e6d52ee2ee7e72d30e1e32e8a7bad54d052260cdf6c43d',
                        'TGLExt/TheSelectorIsNotEnough.lean': 'b62d255e1f9a5f46de9b230bcd5ab98b8a4ccbf10fe84dbeeb5cbfab822af783',
                        'TGLExt/TheSingularExpectation.lean': 'b1995cc2019e1ce63943d31c6124834431751357b5a2b9832ffb5649f7e4f2b7',
                        'TGLExt/TheSingularityReadsTheAttractorAdendo1.lean': '433d13c223b03971a92ae66ffb96478fdf1046a5bc5c2509fa7b244ba2fd590c',
                        'TGLExt/TheStation.lean': 'c55dc5018297a64cfafe9416e7b4cb29b2f6cff535cfd43f2664e26546801f63',
                        'TGLExt/TheStokesContour.lean': '1c310f1d6296cadd59a4ce049974af27e62f708a5abd41699caf50761b00a0ab',
                        'TGLExt/TheSupersaturation.lean': '55d5b5668153f5a0cc6ae71cdadfe698c82b7479c91ba19290ba936b358025b8',
                        'TGLExt/TheTGLPair.lean': '4d17eeb7e940a7ab7ca4ea29ea4ad7cbcc92c37249556e9479023c98b7cc96a6',
                        'TGLExt/TheTelescopingProfile.lean': '5dd73c3878a129ba5286eecea1c3a878aa9182d1d423df8b7ffa0a12fe3eabbd',
                        'TGLExt/TheTerminalRankOne.lean': '4450fd1b63407afc7714cc90b7e91c515c440cca1cba3434214808782a3f30e3',
                        'TGLExt/TheTopologicalFace.lean': '23e283f43c36dfa674282bc2b9b91a7965f20f2bd5894a0e769214d98ee02da5',
                        'TGLExt/TheTower.lean': '836d39ce9220579419fc52c53c2516aabb54a33b83ad1fbf784c44d47699967b',
                        'TGLExt/TheTowerConjugation.lean': 'ab31bd5e939dceba41227a14cf09da57effdd24b01e3bc50f5594b106bf4e275',
                        'TGLExt/TheTowerInnerProduct.lean': 'bdaac2f44fdbc3cdadcdce147991e507b1f22236580d86eca779067f70215bd9',
                        'TGLExt/TheTowerWitness.lean': '5135e6dd9bb983148cdba1f7f54298719bb4530c66f4098605cec520fd1393e4',
                        'TGLExt/TheTowerWitnessLinear.lean': '2a81a78bce7b87edd6e8829466b1bd0095c73afde7a54243b007bc0ab9c987f5',
                        'TGLExt/TheTraceIsNotErasable.lean': 'fb65565eb084cfce6218b0867ffd66b0744b54def75fc34bcc823754bb1cd86c',
                        'TGLExt/TheTrueWitness.lean': '863bdfbe96eaa989b33ddc86d401e1df8bac1788a345167fa1aa0229d2109f32',
                        'TGLExt/TheTwoFolds.lean': '4d1869d35bc9c8efd6d339e6cdf7ba0a5b1098c26371b9c306aff74e08ae9e80',
                        'TGLExt/TheTwoFunctionSolder.lean': 'f1378886dad2380cebc92df56eabae387d3e75a43d3654b03f3bb650e55e3e68',
                        'TGLExt/TheTwoPairings.lean': '46d72f4956f7e0870224761f1ff98daab7d7a75fad548d857e5171556a65a4af',
                        'TGLExt/TheTwoPolesHaveContent.lean': '1e17af908c1d6025409ff121ad9c98408e854b305b4f9a7b8364aba1adb98712',
                        'TGLExt/TheUnconjugatedObserver.lean': 'e2c1978c4a3cb5448699bfcae0dff3da487800bff0d4ef713ec4330bed278a9e',
                        'TGLExt/TheUnsolicitedUnitary.lean': '29aba04e578b1921a8b22d0e9e28fa608160a14f465a9eca32ce2cd208e601cf',
                        'TGLExt/TheVerbSelectsTheAction.lean': 'f47477ea466ad1cc64805b065f3d63ea99c224149a7c2af9691653ab06fb3805',
                        'TGLExt/TheVerbalCoupling.lean': '912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507',
                        'TGLExt/TheWeightIsNotTheRank.lean': '83f9c8bca5e133916080eea6f6200e088b4641a35504a8255156945e7028b72e',
                        'TGLExt/TheWholeIsOne.lean': '097236427302ae42857b1cfc3e89711b45f7bc34fe02e5374bc0903a34d1a608',
                        'TGLExt/TheWideNet.lean': 'ef26e912a6ed418ab0da4ed6b09b35d1090d23674c25e68ee5248ebe3b70d340',
                        'TGLExt/TheWitnessLinearOnWH.lean': '0c1b0883f16eaec61831113f03a106149e80692b0999b4cebbe0045137bacdc6',
                        'TGLExt/TheWitnessOnTheBoundary.lean': '30f2a06dcfa175284948e722c89bf6e75646fcf7a4c57b88729a6aec88c600ec',
                        'TGLExt/ThermalCutoffResponse.lean': 'c82562e512acf62df884ab0447d6acdbfef8d302090f9295d74985da7ae5dce4',
                        'TGLExt/ThermalLimitControls.lean': '0124283356ef91205a00de5a899108fd0a1237b21f68587797f820fdf3a21602',
                        'TGLExt/ThermodynamicFriedmann.lean': '8fee91f600cc60909fcd0590e12fe92af3c6a5a63a4d0749c8688558653cefd5',
                        'TGLExt/ThirdCone.lean': '21edba89bf302c075d512e77bf2dada36b5f216f054930eb5a881c57935eb694',
                        'TGLExt/ThreeLocksCorner.lean': '51c66b4dca74fa58e221bd9889d468d1f77c816ec8c7ff3cc9f56e3bd7a66d2e',
                        'TGLExt/TimeGravitonFlow.lean': 'c6d9b06355e498c9f3e961dbd987f149f6c3848bd495193d68b3016a6d2750a8',
                        'TGLExt/TimeGravitonKraus.lean': '8f30d793279ae5b0b07b629f3260e7c28c9fb185ea114ba2c1f154323f9b30d0',
                        'TGLExt/TimeGravitonMatrix.lean': 'c3663a500e3a2d1746b827d3d739e489fc1feb7d1fdd5079618b96b55108cf46',
                        'TGLExt/TimeGravitonScalar.lean': '7c175efa02569a677828470e25251d20a7d8f45a27c72e6fa5572e76d6900ff6',
                        'TGLExt/Token.lean': '0b6a58e795af73110f55039943d01c7350b1e1b82152689c629bc8429872a300',
                        'TGLExt/TomitaAdjoint.lean': 'e023aa70d05dc785ff2bd0572a1ab8f60d3ac0d6e54259f01d460dca1ef3224b',
                        'TGLExt/TomitaClosability.lean': '0872fa8fd32c55d2c077bb35bbbea9a9181da487455fdcf40552e704d9adc5aa',
                        'TGLExt/TonicaDoHamiltoniano.lean': '9618a2b0e0cce323fc7a4af2d97a266c2b7061a5fb1172d5c1d327227685abfa',
                        'TGLExt/TopologicalAtlasGluing.lean': '4289a0b55babc8e01a5028ed01def2d8051d3b87e85fbb78f3b3410447a2ca71',
                        'TGLExt/TorsionShearDecay.lean': '1ca0a55b411b6629cb4a5c49eb7ff6d0017d3a8b1a2ae23efe02d4e405ff5f9e',
                        'TGLExt/TowerAction.lean': '5da61adbc762e54c157456ffa59efe9b596f9c80b625fda106b2ce7547ba8e69',
                        'TGLExt/TowerCollapseRealization.lean': 'a8195e4c9855e19e6576d3166b48fda0ebdc0a552aa3ffb84a1c0033ee8ea812',
                        'TGLExt/TowerDefinite.lean': '9f63ebf0cee01833e7fdccb3c356c0faaddded504216c8e21c218c2320d8d9fd',
                        'TGLExt/TowerDephasingStationary.lean': '7a635595b9ed53df1858ee01c4fc0f1418642547da183b301671c29c73d90706',
                        'TGLExt/TowerEntropyScaling.lean': '4f048734c88a877eadf4cc12f3ebe8b21265ec5c2eb1290d069b689716e908c1',
                        'TGLExt/TowerExpectation.lean': '1ce1986087c3ab8dce79f21ed0782b7cf55ae78aeb67e671bc9b089cdfcd2507',
                        'TGLExt/TowerGibbsPerturbation.lean': '715270b381362fff2777a5b0b4226e9a8b2b3e812f0a0430e0ce69e3dd9483cc',
                        'TGLExt/TowerHilbert.lean': '8b08430d775093588459d649e81fcb7cfc5e02cc94646d8175c9b124f6cdff48',
                        'TGLExt/TowerModular.lean': 'e3697a4f628eb1ae5211f004ac17d5867ccf60e705bb955d868229b118ee5550',
                        'TGLExt/TowerModularCost.lean': 'ccd49f34c32b0d97d46d5f814574ec9500e0aa9330711bdacb1b39ce59f8649f',
                        'TGLExt/TowerStatePolarizer.lean': '25fa5ba50fe0353944a18c3ec5424ee65b91fdd73782780d81428f3722f62937',
                        'TGLExt/TowerTailRigidity.lean': '943048ff5cffb99907342d54d0ab7a0b49b9ea5f2ac837bc192e448ae547b482',
                        'TGLExt/TowerThermalOverlap.lean': '3b1c9b391d585d61fac68e772bde82a4d3494d65a31dfb9b4a8f39c75fd66fcf',
                        'TGLExt/TowerThermalProfile.lean': 'a9e4971f9f3e62837679e71b76f2643613d5105a0378d9f71934a9ff6e4437d3',
                        'TGLExt/TowerTraceless.lean': 'd5789535f0e38917ad8a1a90c20ee17ded2b32cf0d2dd3ad919a8acf6aa86f42',
                        'TGLExt/TracelessAlgebra.lean': '50c531bd93946a7f8df4bc940e15c3d2f71899e02c50e060e6f695f136a13de5',
                        'TGLExt/TracialCentralizerExpectation.lean': 'f5b33400cc9424fe810cad222785fc06f7741608350a5f2d7eaa95c22e545903',
                        'TGLExt/TracialDissipativeTorsion.lean': '20ea483c1ffeb356f6798a681dc754f9f3fd1a4419bb4d8c9f60e2012ad2d8ca',
                        'TGLExt/TransportWitness.lean': 'f4219cc2c036999e19e41b006d4899a1a10cd2e8e3562c5a277370faae0364ed',
                        'TGLExt/TransportedBorchersObstruction.lean': '96bb196544840ff4250293713d823ddd11b699f573498f90e4dfad2e4d5bf117',
                        'TGLExt/TransportedScreenControls.lean': 'e4439fc13f2b708737282518e3fd01c7451dc5b4e0c388be3fab6cf37db243ae',
                        'TGLExt/TransportedScreenExistence.lean': '3274513ddce86ac9b155512be9361142614b0e3b2da98b5829cbffc307fdbfbf',
                        'TGLExt/TransverseGibbsResponse.lean': '86df266b238d49486d3cf26466cb0eac24bbff75593efe5ef9275b56b55f7913',
                        'TGLExt/TransverseInitialData.lean': 'b42047ad7f12ac75b3dd76542af6925b9eedc0f75c3445a7c0068d21c7fdf8df',
                        'TGLExt/TriadMaster.lean': '64e0899e259693927b051493b8f20cc47885f183d02d79a8772e3b3d869863ae',
                        'TGLExt/TwoLevelSchrodinger.lean': 'b8d2f0351cae52235479cd2ed5638ea97bb2380e6f836862285a24a1507a6586',
                        'TGLExt/UmPostoInscription.lean': 'd33a2ab12bd7e61023f0f2545e60b38eabefb1130d9bce0856ab9e9e56064675',
                        'TGLExt/UmPostoRelacao.lean': 'b9c3d348cdd24fc7a2dfea172236612a77cf4405c40ba411aa649e87c2ea85a6',
                        'TGLExt/UnifiedRecordedPreparation.lean': '92e7273a21eacbfccdc0d97117397feb0e193b1c7a09ae1b83633265e1e9c73e',
                        'TGLExt/UniformQuadraticResponse.lean': 'e6da974d6af9878a4b83e4ee752f0e3499aa0f066d94c3225f8ffc1941cae4ed',
                        'TGLExt/UnitaryClausiusBridge.lean': 'e96cedf4e5493d1388de7354525236c6697b203d37cf3774ab4404d80edb150d',
                        'TGLExt/UnitaryCocycleUniqueness.lean': '76b0e798d353d969ee41edeb5e19a4529d4a53170336ef75d26139ba49532471',
                        'TGLExt/UnitaryDuhamel.lean': 'b95f47a24bced16ca020e63eedc582c85f11f12e658447bff821cdfd4fdc99ab',
                        'TGLExt/UnitaryEntropyResponse.lean': '136915bb5a1bf52217eccb915ba835b7e5d0cc5161275b2c011887542d929808',
                        'TGLExt/UnitaryMarginalDynamics.lean': '787d6131dc31cc6a3800b1827a0bc9b1c9ba0cbec16a06a8f6ac4743964a91c6',
                        'TGLExt/UnitaryPartialTransport.lean': 'b107efb63dafc9901ad700881ba4c136a1b98428ce235dfc9d2202b7ef7f18e5',
                        'TGLExt/UnitaryResponseControls.lean': '447b94bf08061a994209654b39c701bfd7ab74d14593259669611cc2ccf3cc89',
                        'TGLExt/UnitarySourceCalibration.lean': '08ba64351b1d684c2ee8fdd85e1dbefc4aaf2dec6c17f269ba183a5c57ab39f9',
                        'TGLExt/UnitaryStateDerivative.lean': 'a6eeb79a5c6f4111d3cfe2af80ff8389bf4df06acf3b6605d2a5277c386b0327',
                        'TGLExt/V350AntilinearAdjointGraph.lean': '6a3cbe3ded292e347a885be00be565c6b030d6971a7ac035096966028a552e98',
                        'TGLExt/V350AntilinearComposition.lean': '521e97302de691528b2b85e0a6e9eec0920533ebd370b55f64e3703172ba65b7',
                        'TGLExt/V350AntiunitaryPositiveConjugation.lean': '83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36',
                        'TGLExt/V350BasePolarStrongLimit.lean': '2c3ac3e1ddf59dff0db486d2bcc26e4507a014f3c7ee651fb54ce6dd77b13268',
                        'TGLExt/V350BoundedBaseDualValues.lean': '8ca1418ac31012523b72539d0a734c77edc15caacacd87eec912a23f8e40aa50',
                        'TGLExt/V350BoundedDualValues.lean': 'cfa8e18faa5b47478347e2223eda01e67d7fcb3be0c9af6433d42b34cbd066ab',
                        'TGLExt/V350BoundedFiniteSquares.lean': 'b918cc3b86e3699b28d36e62cdb750aa96225d42c2337cc63723b4245f2e3a4e',
                        'TGLExt/V350BoundedInjectivePolar.lean': 'bd16c6727b6738718ba8e4c2c5009aef6c86d206240d6bead093f6ff65239b76',
                        'TGLExt/V350CharacterLocality.lean': '7a5d2f1b70b3d61307045c4460034e3821976c8b30b02d5bcf165d157f33419a',
                        'TGLExt/V350ClosedAntilinearResolvent.lean': 'f1af44b5212378f0c5b8a4535258c4fc6f07ea8445a9278f7b3b5005a8a9a633',
                        'TGLExt/V350ComplexGraphProjection.lean': '99d8368bb23e4e7468290e9a10461743397b8d4925308e91e379c7f341c6bebf',
                        'TGLExt/V350CompressionLimit.lean': '532997c0413ac5642e6d77e608811cdd4f3f639231ab704146ab09b4f9c294e8',
                        'TGLExt/V350ConstantFibreCandidate.lean': 'd1cc9543cf02801bc08145b86018af1c1a7a34400bac7ddc300a95d63beb82b2',
                        'TGLExt/V350ConstantFibreIdentification.lean': '3a2e66c94b185f298cdadd07c8cedfbb934774f3b2a7ceccea5264967f5cf4d9',
                        'TGLExt/V350ContractionAdjointLimit.lean': '75c191ec2110441b6554ca7beddfc7806f3e3aac6e879e8461f7632cfa78eaa5',
                        'TGLExt/V350CoreContractCounterexample.lean': '1aaa11d4c572c2ad3c0c80a54322247233b64e6e16e28710cd4ccc0d3524de0e',
                        'TGLExt/V350CorePolarInclusion.lean': '4d5d416c82894dcc93562986ce8eae7ebc2c11f313eb658dc18e356af37dbd8d',
                        'TGLExt/V350DenseAntilinearExtension.lean': '32b93a00492f449da2884ebedf0df85aac1b7b1e620d9c2b999f7bcd6f41b4cf',
                        'TGLExt/V350DenseLinearPolarExtension.lean': '2352e0b01e9ba17bb01914e98d1a778e454202430ce9e9a2042532fd0c34c159',
                        'TGLExt/V350DualClosedForm.lean': '69a47c01fc1a366a61b871b86e1d7114e43e865b025a04cd57918f09ed7c5be7',
                        'TGLExt/V350DualCutLinearMap.lean': '1c4e05fa52f1328abaaf1847ba0db11ec3838eccd1a1f6a2fa90dba34c313a43',
                        'TGLExt/V350DualCutNormality.lean': '026f5042bd6adee2fcf90ce1db5b9831ee312b3bccaf4a194b8631936d543d65',
                        'TGLExt/V350DualEnergyOnResolvent.lean': '020b86bf18e19388c8716b046fc0276fde43216a2782d52de6c27dfabc941c5d',
                        'TGLExt/V350DualFixedCore.lean': '2c120aeaa01da764d94370d273bf16e9e5f5a1ae7d3a91f9066e48a745e09582',
                        'TGLExt/V350DualFixedFormAffiliation.lean': 'd9f9d216a4517dc469f715942018152a0753531113aee136265323bfb38b8064',
                        'TGLExt/V350DualFixedWeightLaws.lean': '93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75',
                        'TGLExt/V350DualFormFaithfulness.lean': '6fca7648f9345bd4e83ed364bc0f551d587b99651b1c7c86574b1d0b090bea83',
                        'TGLExt/V350DualFormNormality.lean': 'feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa',
                        'TGLExt/V350DualFormRepresentation.lean': '842848ee7e13c1ab8d7c0d189e33db5a5e459f76dde0ab54c0265719043a487c',
                        'TGLExt/V350DualFormSupport.lean': '9b0d454ca8fd46c51b4df0221a26bb70bf0dcd6ba6e6ab9b019c4e38877bd657',
                        'TGLExt/V350DualFormTransport.lean': '5b1dc140be333174ca48b61d790eedd4d3fec19780cc9e5b3b9d35f90b57798d',
                        'TGLExt/V350DualFormVariationalBound.lean': '009d85072538bc88d3bd166aa988ae4a3724897ac2a12e140e62ecf0ec2ea9a2',
                        'TGLExt/V350DualOrbitRepresentation.lean': '01d61dbe3b2f4193dc48b345a1e765f017964a73a9e05070bf4e34e0510753dd',
                        'TGLExt/V350DualOrbitStrongLimits.lean': 'a1c944185a25d4fe2c57491cae8f063845c2ae0d9c64d536ddfb7e4e797b15a3',
                        'TGLExt/V350DualOrbitVonNeumann.lean': 'b00ffd7618a281ddb9cd74f01418de030e0ec6ffdaf2ff54fa195a4e175bad67',
                        'TGLExt/V350DualQuadraticLaws.lean': '7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3',
                        'TGLExt/V350DualResolvent.lean': 'ee5ee31d1788cde0420e74d571e86ddddb86cb9ed5d7744eec74999a682fbcd2',
                        'TGLExt/V350DualResolventFixed.lean': '1d1805ed2f6544c3a11cdfecf503258448681ef49376af4409d80de7d8570056',
                        'TGLExt/V350DualSemifiniteIdeal.lean': '63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe',
                        'TGLExt/V350DualSquareRoot.lean': '012ea5fac9898efe88bc2f6c1710aadbae3f6262446a0787f115ede530acf6e1',
                        'TGLExt/V350DualSquareRootFormBound.lean': '53801ea72ebcf76112d5f95fd5f1e5ced03ce2dd03a590c86682163c69011bea',
                        'TGLExt/V350DualSupportOperator.lean': '57e3a2f02ff77d1690d01384eb064dd5598a58194c492361d012efab4c129b8c',
                        'TGLExt/V350DualSupportTransport.lean': '5f900be38fd20a4bd1fc05c8730204dd8c7db3951905f0256a09b209d3c54acc',
                        'TGLExt/V350DualVariational.lean': 'c375e63d7cc8415d90c8663e9230b9696171ba3138f8b1fe250bb5898938cee0',
                        'TGLExt/V350DualWeightCuts.lean': 'cad8c916c67f1329afbac42658d13e8930e065e8f6a69152d4c9caf93cedd91b',
                        'TGLExt/V350DualWeightExhaustion.lean': 'b09270078d8522f00acddd75b90a36f92b332330521aaec3253087414555c697',
                        'TGLExt/V350DualWeightForm.lean': '3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4',
                        'TGLExt/V350FibreSlices.lean': 'c1d65e158599c21ccc2442e31b594dbf813eff64dde3aa034d0da28e40431871',
                        'TGLExt/V350FibreVonNeumann.lean': '48ba27a3b9701bc7c6dfb1b28128fbc10d00cec335cf24f4d3be27d0041eb5a8',
                        'TGLExt/V350FiniteDualStarCore.lean': '017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce',
                        'TGLExt/V350FiniteSetFibreRead.lean': '079cd0e3f831c690348b14a52ce29cbb3be0a601ffdfdbd4508af6027e80cf93',
                        'TGLExt/V350FixedBaseEquivalence.lean': '6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278',
                        'TGLExt/V350FixedCoreBaseIdentification.lean': '0454ce14669be84c8384143a8ace33b7e795bc5b262355afc97284d1a963f4a1',
                        'TGLExt/V350FixedCoreLocality.lean': 'b5cb6a24e5cc2ca221741f9e8dbb4ccc2361b7a7729886d2ab80ed723b1984a8',
                        'TGLExt/V350FixedCoreShiftCommutation.lean': 'efb3533d950d396ae8932ff9980500d6c65ee000e03952e385b038bc70588098',
                        'TGLExt/V350FixedVectorGraphCore.lean': '917cef45ef9cab3bab4f15a8b0b7bc3b1773e40b9e5146d62563cd46fa7fa921',
                        'TGLExt/V350FormMinimizerUniqueness.lean': '027860f3babd0c2833c69479e84112b7541df6bf3d37111cb1ce5315ae235075',
                        'TGLExt/V350FourierL1L2.lean': '49c8e43b55cbd48b3a2c9f1bdfa01a31af9566e7a3cccbb4eed119fc1c750f13',
                        'TGLExt/V350FourierUniqueness.lean': '16eba1061905aa2eabf73e388c47a8a4f522acacf18e2eb5a8293687121cd850',
                        'TGLExt/V350GateContract.lean': '87cee74501af7cb2f4a0f234abafb0b6b671a914bf6d1d868c7ab2e97ada736a',
                        'TGLExt/V350GeneratedEquivariance.lean': '0e1091b93efa8b498fefdc2e6289e57697dc0e6967a4e78cae7f4022c2f24011',
                        'TGLExt/V350GraphCoreNormTransfer.lean': '03d8b38e0acc72a84e02d053fc7b0a2f412d41f40b9b19708156bf33e58fd294',
                        'TGLExt/V350HilbertProjectionBlocks.lean': '0ae2dffb2be38916e3b4936d7ebb9faef5575690f8caf39f2bd0dee2910604f9',
                        'TGLExt/V350HilbertProjectionOrder.lean': 'de3932a91e87dc12beeb0c5eb4ef38d0e036649090d089435d9a08006b3158a3',
                        'TGLExt/V350HomogeneousCommutantTransport.lean': 'd1a8ed8a028d8f9dcb6ab910a3e05721a26a599e2d265f284f0a84f58c3493b3',
                        'TGLExt/V350HomogeneousRightData.lean': '46248d901ed72c327b0c5c5e1c5a467882c69c215270452134307149e2241b17',
                        'TGLExt/V350HomogeneousRightSquareDomain.lean': 'cfeda2aff89a9b852347d3e9026fd3cac48c64fa3dfd43db42dc2cae3c5cdc93',
                        'TGLExt/V350L2BoundedStrongContinuity.lean': '2060f158c4ef52035373fdb31b03507f37d455fdd6c952dfb26e26d92dee399a',
                        'TGLExt/V350L2CharacterMultiplier.lean': '2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3',
                        'TGLExt/V350L2CutIntegral.lean': '5ca1ca65a1151156594db7087ee1ea376f81bc6721499d28ff544eb12867585d',
                        'TGLExt/V350L2GaussianProfile.lean': 'b310c30ec1a4d69f637b358ccbd9a48dd73436d06368e5796a6139e8b167f5fb',
                        'TGLExt/V350L2MeasurableCut.lean': '0a52d5d408c5f877b6eb95309cbb793ca385d2e9cfd7778e716442d104babb6b',
                        'TGLExt/V350L2OperatorLift.lean': 'bbdf07f64bc1abdfb50fed8420911c868a11cc6c8036b6f06167f021a1db7465',
                        'TGLExt/V350L2Order.lean': '763b6ebd38541bb028c6a007c492b5155fd5859d2bc9572a0016ab8bef93f46d',
                        'TGLExt/V350L2PositiveMultiplier.lean': '6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf',
                        'TGLExt/V350L2StrongContinuity.lean': '837944b5c783a90239a19e2547bc34dfc3ab91be35d0cc94870dcd4875fa3c0a',
                        'TGLExt/V350L2Translation.lean': '1fc45298e186caf37d2b04779e64f3e000e7384511bede3bdce57ab9b429b267',
                        'TGLExt/V350LevelExpectationStrongLimit.lean': 'c5030991cc5894f56885c612b0fbcd1502de9c0f0d68e6740fd50227054eb165',
                        'TGLExt/V350LevelExpectationUniformBound.lean': '6ec762be7f9014e45f88ffa9971a0e1672618f6d4289fb7e6247e5159a21e6b5',
                        'TGLExt/V350LocalBasePolarCommutation.lean': '6a81d480bf6997282bdd5734b99e8d50ac17e532ad390ae108866130b94046a4',
                        'TGLExt/V350LocalRightModularTransport.lean': '6ff17a665e3c0fc1e156b1e3fe7440e44dcbd811bd1acee2e6963de420bca222',
                        'TGLExt/V350MatrixUnitPolarCommutation.lean': 'bfeac1af45934d5e356020be54b5c5dee55ecfb752260d666a89ac7a07e0d4e4',
                        'TGLExt/V350MatrixUnitPolarTransport.lean': '0d800d33855d55cb7c228771610ad0cdb061fb89d387aa3ca56367cf4aa173cb',
                        'TGLExt/V350MatrixUnitResolventScaling.lean': 'f6b1271a8612a0695581ffc52afb45277ed0468bf941b42fcc8c8c3086877911',
                        'TGLExt/V350MatrixUnitRightSquare.lean': '27403f0368e77e9e8e9c1de5dfdb71e6ccd740a280c13afcbc6c6f68e43a07b9',
                        'TGLExt/V350MatrixUnitRootScaling.lean': '640c2fa1ba7dd736b987289e7b384247778d31e1bf29c2a4ac425a5af4fdd0be',
                        'TGLExt/V350ModularCertificate.lean': '9f4919ec7a4ba35bbb9bafc056856a24fb196ce9ebc45b6ebefb113f0429051c',
                        'TGLExt/V350OperatorFieldAlgebra.lean': 'ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d',
                        'TGLExt/V350OperatorFieldFaithfulness.lean': '6c768ecc41d7e6d239642eb14952649fd5f9431bb71d2a0f5de0654be637a8cc',
                        'TGLExt/V350PartialOperatorSquare.lean': 'f345796e306ac0274874c12b59cc9fe220ef33b164522abe0543b7f1bda6a5da',
                        'TGLExt/V350PartialPositiveResolvent.lean': '4619abd915245d92724e10b3f29c7f109c0b47830f2eff2659df01053f36ab3c',
                        'TGLExt/V350PartialSelfadjointRange.lean': '57c863528fa0fb16720426a11c1c5901a9f41c940c081ddf6c1323e758d5a673',
                        'TGLExt/V350PartialSquareEnergy.lean': '3b604d56aa3fd89e977eae4819bca07aab7697fa8a4d88d4eea70b2090bcef21',
                        'TGLExt/V350PartialSquareGraphCore.lean': '86cb2a587fb8594c58f0974c1334f381da0d5f444f373338c0ac0e8f61f260c5',
                        'TGLExt/V350PositiveFormCone.lean': 'cee6510b0cd71261988bae68692d52b2a6a6270261ccd3a8e892ca625f49181d',
                        'TGLExt/V350PositiveResolvent.lean': '28a29b66c00b67f696a8a8f27dfc8e19dc28de0f16c96ec64e299a9b6143ebd1',
                        'TGLExt/V350PositiveRootIntertwining.lean': 'f357246ac96d1d98fc1376238be4ca039f425d2782dd23d909ac5cdd3d1afaa5',
                        'TGLExt/V350PositiveSurjectiveResolvent.lean': 'cda1cc7ef883c273d58bbf83524b31837509f8dc9a6a2df28bd77fae7ee0821b',
                        'TGLExt/V350RealGraphCore.lean': 'f7b06faa80ce7d3770708023b8e6042a274bf06f73ee13b171d496ed2a3bcdaf',
                        'TGLExt/V350RealPhaseVariational.lean': 'fe34c27260bd05593679bf2e03b06ab7c7f92993aeed8c657616075c4b00b265',
                        'TGLExt/V350ReducingBicommutantLift.lean': '8f90b4481f2516ef215b53a7fe28744822f9be6b7d2d5cb6da3a98108b898d5c',
                        'TGLExt/V350ReducingCommutantCompression.lean': '1bd2cbaddc3c1b6ccd7ec7a8c62c984fc9e25561bc7c0bb8e806f1a1042f83e4',
                        'TGLExt/V350ReducingCommutantTransport.lean': 'c1c15252f38ff82229443a04455127cdd0ad69828dd039e5b0d91edbd96cb963',
                        'TGLExt/V350ReducingStarRepresentation.lean': '79a0c03282c1328f5b4d6963242a3ee1737a11c12353cec5f8244a5030b5f2fa',
                        'TGLExt/V350RegularApproximation.lean': 'd8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44',
                        'TGLExt/V350RegularCoreCommutant.lean': 'db496b5f070cfed3666d1a52e2e5b5fc4ca095d34e80b1a7e6122d2e9c57400d',
                        'TGLExt/V350RegularDualAction.lean': 'e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c',
                        'TGLExt/V350RegularFiniteWeight.lean': '39e417e41adf90a2d575b6a93f8a35ccd2d816a445097745fd3c540ab240baf6',
                        'TGLExt/V350RegularGeneratedAlgebra.lean': '252b0fa3d5e37c42827efccfc26a555db80ac5c20a6f94269060ce2b3dcb5f71',
                        'TGLExt/V350RegularNormality.lean': 'bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a',
                        'TGLExt/V350RegularScalarWeightCertificate.lean': 'f7c1786097ce619e7cbe7f35269147b8bde95793de9b0b5a09bf98627a2db6c0',
                        'TGLExt/V350RegularTopology.lean': '13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5',
                        'TGLExt/V350RegularTowerRepresentation.lean': '21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f',
                        'TGLExt/V350ResolventGraph.lean': '3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b',
                        'TGLExt/V350ResolventGraphTransport.lean': '557bef736e338094c69fecd79a189200e7b97a5a26ef880f637432b3fcc17173',
                        'TGLExt/V350ResolventSquareRoot.lean': '6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90',
                        'TGLExt/V350ScalarBoundedCuts.lean': '4b5a3c3efbb85b30c4668d6cc564bb8e9a56d750489a03c55c4a9666c6709078',
                        'TGLExt/V350ScalarClosedTomita.lean': '4d87af66ab6aecfe92e0c53db83c324d649c32b15016190f3a5b07f5cccc8c8f',
                        'TGLExt/V350ScalarCommutantRegularization.lean': 'cb9fbab4a5b3fd3378fb0a10ecd596290e2090c113d3ea9a74b57457af88ac30',
                        'TGLExt/V350ScalarCommutantSandwich.lean': '51ed42ad04db3fd852ef06a57219eee29dcebe6544afbbe9727e7850f33a1451',
                        'TGLExt/V350ScalarCutCyclicSpace.lean': '6b80dd3a58161b692c3cf4679c899c4205446b233b7b3ceda60e79da045f6091',
                        'TGLExt/V350ScalarCutGNSProperties.lean': '89c398c46a2829e3c0ceb1134481af2792a330ba73efedf8679754bbf9d3e7cb',
                        'TGLExt/V350ScalarCutNormality.lean': 'cb48c29dc6d9fe1ab63b2343501a3798e548b9e23762d425c1066c7eacdfe383',
                        'TGLExt/V350ScalarCutVacuum.lean': '524ca91fbe926c9cca9d556da92933d7b1ba037cf57dfd572250a7f12770c24e',
                        'TGLExt/V350ScalarCutVectorFunctional.lean': 'a5f8006dc3fd6a845e1a43f2cc421395bbd1cd8a8d27401530a68e9e854d4cc2',
                        'TGLExt/V350ScalarDualWeight.lean': 'e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53',
                        'TGLExt/V350ScalarDualWeightFaithfulness.lean': '3ff3e31e49de71f035a425202ef1796be18da2b46bdb60a7f6c34b8a2e73f61c',
                        'TGLExt/V350ScalarGNSAction.lean': '529982d9d3489dd900c8259599cede7cbf866525e4001e8196054679fae8f65a',
                        'TGLExt/V350ScalarGNSCompletion.lean': 'f2bff58e02c1e454c7832b51c0b8712816bd3f6c0e99f91f67811dd007d9771b',
                        'TGLExt/V350ScalarGNSCutMaps.lean': '2daee56a03944695f137e54fa8a0f76883cbd453d707aa626e5d201700286b5e',
                        'TGLExt/V350ScalarGNSCutNorm.lean': 'd5de955da28b3c97a153d2422bba3e4d8a55c0c12556679a59fa9948f42a60f6',
                        'TGLExt/V350ScalarGNSGeneratorTransport.lean': 'ed7ce8c1e5693f28277f3de7d7fcb0c3a43359d0fe02903a7922280bfcb858af',
                        'TGLExt/V350ScalarGNSLinear.lean': '1e2708f65d937e7529792d690ff989806064336a5dc1eba886aabf2f174f0562',
                        'TGLExt/V350ScalarGNSNormality.lean': 'adef4ae98893c92165d9d8b40ab7a1a298cfcd9da7e11fb42a2e7a906c6181fc',
                        'TGLExt/V350ScalarGNSOrbit.lean': '0acfc1da712e3ee99a19f3ddc63355fa26038d1841e9d54ceeec385ee4b045d2',
                        'TGLExt/V350ScalarGNSRepresentation.lean': '4f30495b0f3531889367a9b8b2754f7ec561dbc5e5460f8b4c3f63cf9d19347d',
                        'TGLExt/V350ScalarGNSStarApproximation.lean': 'e280a88c77e51272147eef2833d73db6d9e251b04c001804663e945a8b31de45',
                        'TGLExt/V350ScalarGNSStarDensity.lean': '819bd5f30026f25b4097343f7f6ef84e47bb0f8c131ad5ffea9916507a75e28b',
                        'TGLExt/V350ScalarGNSStrongContinuity.lean': 'a01a6e42e191d7bc7ce2a37e529fead8d04463b62d19f081fd640f249e2b3938',
                        'TGLExt/V350ScalarGNSVonNeumann.lean': '338eed155931ece554092619868f0a8af5e1474f1453ac2040d0c4c148050f6b',
                        'TGLExt/V350ScalarGaussianClosureTransport.lean': 'cb0e7921903f4e77bf08baef2791c98d3220c3ce8e13ee5478de5a8b06a266ae',
                        'TGLExt/V350ScalarGaussianGNSMap.lean': 'bc00455275254f92ab3b7405a23ba41351680e80c65608ed81475cf2d1dadb7d',
                        'TGLExt/V350ScalarGaussianImage.lean': 'bc7d8922b76650d0e121591d01aa0d0387911d0d47041d7f5d0849b6aa4afcf4',
                        'TGLExt/V350ScalarGaussianRightPairs.lean': '685df6374a9123543d281b5d61a4e1ed8082d3636883051ac501b2197bc006ad',
                        'TGLExt/V350ScalarGaussianUnitary.lean': '0845c69fba50bf95d4b1045695bd1a4a9e642e89161370fefde5f9b71750ec0c',
                        'TGLExt/V350ScalarGaussianVacuum.lean': '550fae23297d4b225ac9ac12c04221195afdf973fdebdb8e04045f0d948ac565',
                        'TGLExt/V350ScalarHomogeneousRightGNS.lean': '3bea19100acbd1fa6dc5caeba5f81bc3222aa67a3cef9169bfe9f6b46124d0a0',
                        'TGLExt/V350ScalarHomogeneousRightOrbit.lean': 'dea570f1f1d43c026874d322b44fbf7e9c30856c2fac17e252319d799085c730',
                        'TGLExt/V350ScalarModularInvariance.lean': 'a9379d3f1ce24ce3151cfc20e38ee531c606a368d7615740367925cd63988987',
                        'TGLExt/V350ScalarPairedMultiplicationGraph.lean': 'a6f2c606eb0e314df1ae98d7fb18c3c6be2f8180fde403ef12705f0b8397ab9e',
                        'TGLExt/V350ScalarPairedProjectionBlocks.lean': 'd801fa3a06af332b658d334b519518eb1c10bd1dea553699d8c0e786ca330c2d',
                        'TGLExt/V350ScalarPairedRightAlgebra.lean': 'b880ce8e7a5485eb4269c3aaced8816b31efc6499db2c4a6ed171be902585001',
                        'TGLExt/V350ScalarPhaseVariational.lean': 'd87d15414ae85b566af38e914f38ec2e6ec59dd3a5fa866a2b68a2aa8a6b4e2d',
                        'TGLExt/V350ScalarRegularPolarCommutation.lean': '1c238b53abf26177ed621f2daf98383b9e14a6e0d97cc85ac98cc995ee4dfb70',
                        'TGLExt/V350ScalarRegularRightContinuity.lean': 'b8766bf0a435033db39ba80a9c52c3254cb0ce595357cd6caebeab7e7adf6314',
                        'TGLExt/V350ScalarRegularRightGNS.lean': '92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa',
                        'TGLExt/V350ScalarRegularRightPolar.lean': 'cab5601b5e0a1e1ef950638a2025c814488c3f5baa083c14d85028a1ca9d95c9',
                        'TGLExt/V350ScalarRegularRightSquare.lean': 'dd45f1b6e36d634ac1ba0ea25fb17b77eadd03e6408a6d4c97f3007c80999dff',
                        'TGLExt/V350ScalarRegularRightTomita.lean': 'bb5511dc55a6c4ab17d17be0c6cfeb224aba206f00b41336f96ecdb03ed021ec',
                        'TGLExt/V350ScalarRightAdjointPair.lean': '6db80e5fe729f47c9f8d5b9764a24ec5c14ddc8a845d38f8606b5a3abc974a7b',
                        'TGLExt/V350ScalarRightAverage.lean': '64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed',
                        'TGLExt/V350ScalarRightClosedTomita.lean': '191d4c46d9df975e9afc45526b8e72b6089f96d114c819e1bbecfbf628d26576',
                        'TGLExt/V350ScalarRightConjugateGraph.lean': '458a1cdcf79b9063c883cad290ed0b1d6eb6a0d44aa2371f85ba983837f7e9d6',
                        'TGLExt/V350ScalarRightFunctionalStability.lean': 'ab44460d765921cec0a9c7082728c730a50b4345c2a12d1edca7f08170c5402a',
                        'TGLExt/V350ScalarRightGraphCore.lean': 'd69cc3f42b40001c686d6a439659eab8d78feae611ec3c48803edf04f551472a',
                        'TGLExt/V350ScalarRightHilbertCore.lean': 'c01bb3ad0b9e0f465c1e3a13c5dbe51f5dc3f611150e0470cbf02aed790ce74f',
                        'TGLExt/V350ScalarRightMultiplicationGraph.lean': '3fd2548e57530081eb4daa4515e7a3126385efb83f5e09aac9e7d5625994a6c0',
                        'TGLExt/V350ScalarRightPairVector.lean': 'f15df629ac8d3a4ab14c7e1eef7d65559fc790c66578a9e8fca6b7b3480cde83',
                        'TGLExt/V350ScalarRightProjectionPair.lean': 'd42557aaa2d2bf44f1f4825c30ecd32e980b1845da314273d529f298c417899e',
                        'TGLExt/V350ScalarRightRegularization.lean': '05be28c1bff08798e4231c904903dace91e2c2f5a5103d3e370baa3e437b7488',
                        'TGLExt/V350ScalarRightSquareApproximation.lean': '6c45fb3595b39fbc6330cc9c4e9d5a3723efc8bdf0047c3d5b4b39f65a25c527',
                        'TGLExt/V350ScalarRightStarGraph.lean': '7a210d191ef86d8a83f11b9443efd9bf9de8c2e209ba632ced475cc1bd8d1bdd',
                        'TGLExt/V350ScalarRightTomitaAdjoint.lean': '9e1adf36116f9eaefb7743e4fc9ea2b3aeabe210ffb2905945b586172b0df448',
                        'TGLExt/V350ScalarSquareAdjointTest.lean': 'd173d21fff82cce7852669ee868f20ce29c45b81500e8029c48b58f9b0912e14',
                        'TGLExt/V350ScalarTomitaAdjoint.lean': 'be788eff71d166991b356d5d780825238e272c1c824bfe9857b4492cbfd04968',
                        'TGLExt/V350ScalarTomitaAdjointPolar.lean': 'cd602e618b745d259e4c1ee310f7577e28247431915400eef8319e1175fb49a9',
                        'TGLExt/V350ScalarTomitaBidual.lean': '6d8c6b5f02e52c0c07b73b92095a2b4425e50ab1a95a966e50180fbf7953d2d0',
                        'TGLExt/V350ScalarTomitaGraph.lean': 'a593af9d063ee60d621c500a6f872a924204b1c3c55efeff3d3f4e20e4d57532',
                        'TGLExt/V350ScalarTomitaGraphCore.lean': 'ddaabe82e5399e19ffd8ac13a62d3a8214feb7da470fc4c49ff834a714bd26f6',
                        'TGLExt/V350ScalarTomitaPolarFactor.lean': '66b8ca1222b639f710ccca3b52f6ab836262b977e023da487057e850a5f415ca',
                        'TGLExt/V350ScalarTomitaPolarInvolution.lean': 'b7cecd7d64b40a7de3bb5cb81ad90feeed1883943c0e566442eeb12abc83984d',
                        'TGLExt/V350ScalarTomitaPolarResolvent.lean': '666ee0b78071dfd26dd566dacfdf3de53a24a59e232508be7e56448b36ef3dd9',
                        'TGLExt/V350ScalarTomitaPositiveRoot.lean': '721afac12bff6654a1f1cdeadc1077d8df9a531d81dc1eac91a017e9bdec59b2',
                        'TGLExt/V350ScalarTomitaResolvent.lean': '50e9437f0a572187103933b7b4847b82599da0a687e439a3b7ab48735e2c3127',
                        'TGLExt/V350ScalarTomitaResolventFlip.lean': '1d21d94fbbc03040e1f3802ffeda0582f192b969e9ce811bba8310603ed1a08c',
                        'TGLExt/V350ScalarTomitaRootDomain.lean': 'e302360eff30f5c8005d3d38e854caef55b62ff239466a5a2c46b7b24cd26499',
                        'TGLExt/V350ScalarTomitaRootEnergy.lean': '2748bd7c326e0b72143eda0061d1a9cb12c154eef90a0828c30a2e3f85762406',
                        'TGLExt/V350ScalarTomitaRootGraphCore.lean': '0b179868eb92ce94f5a3e523e43ebb615bb6e9f2afca49f78bd5b5506acfe977',
                        'TGLExt/V350ScalarTomitaSelfAdjoint.lean': '2dbdfdaa1f1383036a2e0954347058d32de7c8343942a3ca15f5c81e30266af0',
                        'TGLExt/V350ScalarTomitaSquare.lean': 'ca781e13f5857fcb348fd2cc1e68a2fb3397ae352b168e9ba9a6425517634a2a',
                        'TGLExt/V350ScalarTomitaStandardSubspace.lean': 'ff5c152c886b3824064722677b62ddc0349df7d7f43cae79a7ee060d75b221c9',
                        'TGLExt/V350ScalarWeightAction.lean': '7875ce91559689c1e951f28d3a1d005dc17aae2af1db677242a27d38e40dfb5c',
                        'TGLExt/V350ScalarWeightCompletion.lean': 'b8a87c9b03f233e8e0a04a92aaa7c6cd4499fb8421746902f2b0b90feb883d7c',
                        'TGLExt/V350ScalarWeightDomain.lean': 'e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f',
                        'TGLExt/V350ScalarWeightOrbit.lean': '9d170b4b28f7ad8da5cce31e9d2e1b7b7216ccef6519a626e42be39ef0b27255',
                        'TGLExt/V350ScalarWeightSandwich.lean': 'c5d1bc60651360815abdce88a3df30985d5d535446c64950ddc6d11484a06630',
                        'TGLExt/V350ScalarWeightStarCore.lean': 'bde7673d57029524227c779982d822d9f0b68accfa579cde990333597daac214',
                        'TGLExt/V350ScalarWeightTomitaIdentification.lean': 'd4b3043d6d76a9934d9778a0b1b7e604c26e8ffb2c1e3a7755964496ad520822',
                        'TGLExt/V350ScalarWeightedProjectionTest.lean': 'ccc0263f4272c9547fd1ee22596d337793462173d30a105a829e9b5993c3701b',
                        'TGLExt/V350ScaledPositiveResolvent.lean': '8fc4147c74eaac76104af66349555ba23115cb8a0d40ea63dc27a2bc546c584c',
                        'TGLExt/V350ScaledResolventRoots.lean': 'b4b00e27b539c39e6672d5ee54aaa9b99b0160ff3ae1f87e5d080d1b681f9a63',
                        'TGLExt/V350ScaledRootGraphTransport.lean': '1f7c8554dec681783efe4dde767c8d225e34038a34aabc56a7420627fcfde81f',
                        'TGLExt/V350SeparatingCyclicCommutant.lean': 'b7abd60e1dc54dde28cce905cbbac547eac88b807af52c6d0989e321de21c9a2',
                        'TGLExt/V350SeparatingRestrictionVonNeumann.lean': '3c827e44fa6ffa69beb673923ac57a0cbad07f74118e455f0c19222da98f59ef',
                        'TGLExt/V350ShiftCharacterAverage.lean': 'fbbcf3996127509b6bb919467613fe13ea9529f1b6cfb82b858b45839eefe951',
                        'TGLExt/V350SquareResolventSupport.lean': 'f07a8bd5c7fa6dc6f9dfe52901d46293eba4883f3a597232882bb5ab538f2334',
                        'TGLExt/V350StrongBoundedApplication.lean': 'dd68e70d90c4c475bfbe1770df5428666fd9345ed28b81c2addfef16f56017a0',
                        'TGLExt/V350StrongOperatorField.lean': '83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c',
                        'TGLExt/V350StrongOperatorIntegral.lean': '7ee0e23dc3319a72734ce420f540251f59a27561fa61221d6ab5f98b2989dfa7',
                        'TGLExt/V350TowerCommutation.lean': '5d0ef2222a577a3d44b3c3395fc296e492c97287f7bd53d0b803a7ac06bf45b3',
                        'TGLExt/V350TowerDuality.lean': 'ecf7e02ff029cece6d6271f92a18604b7e5c1d870244712b3098a5c21b18626d',
                        'TGLExt/V350TranslationCorrelation.lean': '1e395f5528eefca673abeb9f37d9199e701662a24383c7a36efe28b3ee589043',
                        'TGLExt/V350TwistedCommutantField.lean': '79333f1292495498d32a6d735255a9c2881704f3c02d06346758455ac76ee398',
                        'TGLExt/V350UnitIntervalProjection.lean': '60b0cf134b9db7b6fbd286dd2b039452a2f7420a2bf2ababbc5240568b6343b2',
                        'TGLExt/V350UnitIntervalShiftProjection.lean': 'e50419955648094c8e696a91a571777470f9ff12df023429f92ea934854961c3',
                        'TGLExt/V350VectorTomitaClosability.lean': 'cc8e1c704d6eea35a5415c6650d89c7cee048504d5e388b347df14a3c697e703',
                        'TGLExt/V350WedgeModularData.lean': '6b6bdf33ed7e54b049da628e6d11af9dc501644174ee2797d8f4e124ab8639bd',
                        'TGLExt/V350ZeroFromTranslatedCuts.lean': '84d7d01dd6438aae7f110f7917e8010c75c839a441c3fd0c7cc46452642b3849',
                        'TGLExt/V351AllPositiveWeightOrder.lean': 'e91306108a0a296b320907a2899f5776747869dffae14f65fe3fe45197bf07bb',
                        'TGLExt/V351AntiunitaryResolventPhase.lean': '92f3087614d347a8d7d532663f10dbb92791066c969f5a3585c7335fd5b6f32e',
                        'TGLExt/V351AverageFixedPair.lean': '3365edaea7a5b9a10db767dae3bc5517298673232151234d9510e6ec1773804c',
                        'TGLExt/V351AveragePolarRight.lean': '9a982e09a318e7c306c20a9c5baf0d07a6354b34d3cf2e6cc3cf168968f334cc',
                        'TGLExt/V351BaseFunctionalEvaluation.lean': '364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f',
                        'TGLExt/V351BaseFunctionalWeightLaws.lean': '0c65dc2ebb355d454456f153b2271158540de28e23c00cfc2e4a7b36acb73697',
                        'TGLExt/V351BaseMoreauApproximants.lean': '45d47db69249a1873c8059b0a9e85f74c0af6920e31ce48b787a4c33e4fde49d',
                        'TGLExt/V351BaseSeriesNormality.lean': '43cbd1db94c855ed588b10c0ccedac4d6e6a62d5876150478ff171a4e3d84798',
                        'TGLExt/V351CutoffAverageCommutation.lean': 'bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66',
                        'TGLExt/V351DualScalingBridge.lean': '7dbe2d9a45971d636f05fac5fdf04dce4d3674a8cbd421fc89fe3e6700b63514',
                        'TGLExt/V351ExtendedBaseDualWeight.lean': '1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87',
                        'TGLExt/V351FourierTranslation.lean': 'a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2',
                        'TGLExt/V351ImaginaryPowerScaling.lean': 'fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69',
                        'TGLExt/V351InverseCutoffCFC.lean': 'cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490',
                        'TGLExt/V351InverseGeneratorCutoff.lean': 'f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227',
                        'TGLExt/V351InverseLimitFaithful.lean': 'c8ea383ff05cfee0c3ae5b92e9fffee44c56b0f0c2224eef4cba81ecc398ff99',
                        'TGLExt/V351InverseLimitFiniteMinorants.lean': 'fca7ff37994a84ee7cc5707f66d670c6cf46dadf9500da10f4f06fa932cc296c',
                        'TGLExt/V351InverseLimitScaling.lean': '2aa1344d9f0ebbf8b3b87b1354b9ec20e10f0fd8b842789e925819c0c2b097ab',
                        'TGLExt/V351InverseLimitSemifiniteness.lean': '0af32fbe3a7f0a36ef61f8e247c24a6117fab4f2b2b778890492b21e13f2f7a1',
                        'TGLExt/V351InverseLimitTracialExtension.lean': 'b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3',
                        'TGLExt/V351InverseLimitWeight.lean': 'cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e',
                        'TGLExt/V351ModularCutBalance.lean': '98fddf5844aa540589735b7bcdd82f5961525d7aac5dcc34ded758c39cad502b',
                        'TGLExt/V351ModularFixedVectors.lean': '53ccbe3b65e326c618e0c4a4864571b5ab318b31b6f0843b1e91273082a05ff0',
                        'TGLExt/V351ModularImplementation.lean': '3d16720656388fc14f70b5e5ded6a8a4d3fc6f72034992bbeee10364c8202a9f',
                        'TGLExt/V351PerturbedWeightNorm.lean': '9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9',
                        'TGLExt/V351PerturbedWeightOrder.lean': '9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6',
                        'TGLExt/V351QuadraticTrace.lean': 'af011f5240da883c369cd2b5f06019cfd845c4a640b9aed5b2a292ce6e13fa26',
                        'TGLExt/V351RegularCoreTraceConstruction.lean': 'f741525cfa335d89221834fdb01e3f3c6b8efa435b107f0a355cc5679fe06b40',
                        'TGLExt/V351RegularCoreTraceContract.lean': '3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0',
                        'TGLExt/V351RegularDomainCut.lean': '60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9',
                        'TGLExt/V351RegularFlowAbsorption.lean': '4760792d98c8d625e9109bd7d0b2a97713bd236dcb7d6db1a4f07251cdc0c9f9',
                        'TGLExt/V351RegularGeneratorAffiliation.lean': '9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e',
                        'TGLExt/V351RegularGeneratorDualScaling.lean': '2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50',
                        'TGLExt/V351RegularImaginaryPowers.lean': '066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a',
                        'TGLExt/V351RegularPositiveGraph.lean': 'd56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390',
                        'TGLExt/V351RegularSpectralGraph.lean': '2a859d88def186591e98f2a0594bc95ae0a9c6eb74c17ea1124ce5844be1b642',
                        'TGLExt/V351RegulatorWeightOrder.lean': 'b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838',
                        'TGLExt/V351ResolventImaginaryContinuity.lean': '8dd7a20376d00763bd8717227fa6bf7436f9eb11cbf4433caabb762d7719fdd4',
                        'TGLExt/V351ResolventImaginaryIntertwining.lean': '789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5',
                        'TGLExt/V351ResolventImaginaryPowers.lean': '0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5',
                        'TGLExt/V351ResolventPhaseCalculus.lean': 'cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818',
                        'TGLExt/V351ResolventPhaseFunctions.lean': '8eb2f7fb43b753d739c276b9e98655529860084586e311d94c8984cde361aea5',
                        'TGLExt/V351ScalarGNSClosedness.lean': '13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8',
                        'TGLExt/V351ScalarImaginaryCoreAction.lean': 'db4109dceeab1e948d7d5e664e8d76b347c719b00e62031761aaf5e924862a83',
                        'TGLExt/V351ScalarImaginaryLeftTransport.lean': '748f06367b522924203ca2904b0c2bac0a61dbf4df26790903453e7786bf749b',
                        'TGLExt/V351ScalarImaginaryRightTransport.lean': '5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349',
                        'TGLExt/V351ScalarMultiplierCalculus.lean': '4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c',
                        'TGLExt/V351ScalarRightActionAlgebra.lean': '68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af',
                        'TGLExt/V351ScalarRightActionLimits.lean': 'ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d',
                        'TGLExt/V351ScalarTomitaImaginaryConjugation.lean': '981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d',
                        'TGLExt/V351ScalarTomitaImaginaryPowers.lean': 'b8871f05b5b9605a8b193a8ed25346d79eac72d025d3ad95c8f9c884f28b4e52',
                        'TGLExt/V351ScalarWeightSemifiniteness.lean': 'f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a',
                        'TGLExt/V351ScaledResolventCalculus.lean': '89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32',
                        'TGLExt/V351ScaledResolventFunctions.lean': '1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb',
                        'TGLExt/V351SineResolventApprox.lean': 'a1c6f5e77916ee527da3716f634431ddaf1f36c9dd80376ceee83aeb63c20c01',
                        'TGLExt/V351WeightAverageRecovery.lean': 'a72b71ac86bb0b2a5c81d5bfaba3c6ad964bf4a8beffd0a9df89f7ee26391fac',
                        'TGLExt/V354BoundedPolar.lean': '65ec2d9b95bba9281c2d30ab94632339021d6257a73fc86a493ac4f7d7469dd6',
                        'TGLExt/V354CoreProjectionLattice.lean': '4f801a61c0b97048158888485326ed4ff871e822978fc5ba5e6904ea41dfa452',
                        'TGLExt/V354CyclicTraceCompletion.lean': '68ac4efa1c7a54ed9b77b80b8b2fae0f17cf3bd684025e53538b2a2c3f4d42a8',
                        'TGLExt/V354FiniteEqualSplit.lean': '72876fa3cf13dbd947ab02f1f4bd378c8d0dc7b2ed9beb39d98d7bed8079552e',
                        'TGLExt/V354FiniteTraceSupport.lean': '7edd9fb4ef524e95b8c71d71bb7467512f9b89f7b04c21a5114686e894b1d323',
                        'TGLExt/V354NormalizedSplit.lean': '5e90a1c08de4dc4593e65d9b8dde4a4bd5a1e074b68f8be357d17d25bbebe91a',
                        'TGLExt/V354PolarIntertwining.lean': '1b0fb92c2001bf9b7c348384a32503c6edb08f36f0e053c42942b58887b5775d',
                        'TGLExt/V354PositiveShiftCompatibility.lean': '9847ab5d6a71a622b68cbb72b7f9d9f94b2fea19505c5abe6355afcf2c9ebc0a',
                        'TGLExt/V354PositiveTraceReader.lean': '8133d88dcaf9ac3d58d739ecaf997312d7951be2c11fe1d08f21c8f90badf3ea',
                        'TGLExt/V354PositiveTraceTransport.lean': '866b0960e908fa76241e8f575a69aac5ac64fba812b8d7f30b8ddcbde984f52c',
                        'TGLExt/V354ProjectionTraceSubadditivity.lean': 'c8bb9cf8626ececad4a104aa6e3de28ee51f38844f4d4562c1bc9524c14e9ce2',
                        'TGLExt/V354RegularLegacyWitness.lean': 'b0c9687acbe2990062c5d1e9035a0e28721c812326b12e11016b11507244c5a7',
                        'TGLExt/V354RegularMatrixCorner.lean': '1f469df09c8ce12c58d7c8388dbedadb3fc9336a9c97757113693e7322e596f9',
                        'TGLExt/V354RegularSupport.lean': 'c80d99c73be4a676bcdc8cc21d476c249911d08f93fd914fda0d788019b1063e',
                        'TGLExt/V354RegularSusy.lean': '8cdb715ac6b6daa2151a36f4b67d120bb2297eedefee32b8600e57b691c12d4f',
                        'TGLExt/V354SelfAdjointPowerKernel.lean': '38a403cd77a7e40c29d8c654bc8e7fb86e6e37ed7d0d5fb3ff4d30caedd01e83',
                        'TGLExt/V354SpectralThreshold.lean': '9c33191344d07e4947a6d78a23ca0fc17e6b75206c13c511219f3a7a3b65085d',
                        'TGLExt/V354TraceReaderWall.lean': '7882c9df649971790dfa9545e802df5b2b4e31c8bc16d536cecfd4d64203efcc',
                        'TGLExt/V354TraceShiftEquivalence.lean': '83efe289302f2a6fa8909932806cec17014a1c99f4c9ff7dafc7d70e0e68afd2',
                        'TGLExt/VariationalFlow.lean': '061b6d105f0792ba86d64e5f888993d5e166087ebc7890ad8398204d812d36e8',
                        'TGLExt/VariationalInhabitant.lean': '2af4afbc660fdd9c1ca9f8c66a8ad073fbea252949d64b503ed2e8cb81b6c27e',
                        'TGLExt/VectorCurvatureCommutator.lean': 'c0074f805eb673d00708c771f1c334f835a9b196f587f3d0275f2bc4c37c1398',
                        'TGLExt/Verdade.lean': '9ebd5525644400834e47049b16a0189aa2080c29f578e3b848ed31d57509b04f',
                        'TGLExt/VerdadeAdendo.lean': '7f6b3eba7adb09bedf0ed6f4bf8c7f8b2393128c3add08caa8485117cde3e1dc',
                        'TGLExt/Vida.lean': '9836c760bc1776f95ff96a6242c0e2dc73a755436081fde42772cd5dc5862693',
                        'TGLExt/WedgeNet.lean': 'be5a629740df809a2c2157dc6e99bef116704f1373276d0a979785ba37dce463',
                        'TGLExt/WedgeNetFiniteDiamond.lean': '1772831452bab2ef5626004819e07202f7d39f956b5c2455e895ff7159cbc91c',
                        'TGLExt/WitnessSeed.lean': '3281a16675fa60c4b1972b4122d083899aad4adf00328500a4a1367e5bfa3ec2',
                        'TGLExt/WitnessV2.lean': '35f47bebde47a54e25cd4fb51b8f242f5a8385c45bd9fc1f9544c118f30a8ee1',
                        'TGLExt/WitnessV3.lean': '22bf6476c48eb9ebabb1439800d52b47cc2d24bc2a1462987dd71c60350f644c',
                        'TGLExt/WordExistence.lean': '6c1fdfff860cacd0a2edfa1e4a49ebf1701f21c95adae69bbe86fbcd9bd7d5da',
                        'TGLExt/F1Fecho394/AnnihilationDomainR1.lean': '69659d84bf9d2509f92b10427e3989b992e8305f9aaad92018a7456e38345bfc',
                        'TGLExt/F1Fecho394/AntilinearTensorR4.lean': '2180c1dd00340bdf7259f3a37d6a025531c5a0e47f41bb7115c0a4ceb8dfb670',
                        'TGLExt/F1Fecho394/BicommutantStarGraphR1.lean': 'edd14d956c022a74eb3c6d634a9ddfef273bf822575ab3c4d68eca1f63c56ed8',
                        'TGLExt/F1Fecho394/BicommutantTwoVectorR2.lean': '3e84de89f5c2bdf3314d5620852bbce6f69f82bba6314d40e5b2e631ed3b21c4',
                        'TGLExt/F1Fecho394/BosonicFock.lean': '77b516e225bccb6975995fc7fde6cd5fd3d0f0fa57c2c029a453b8d6803e9e67',
                        'TGLExt/F1Fecho394/BosonicFockContinuity.lean': 'bb5db65e5ece04f85631f26354b0d9ef647bce85fcbd2c4fe9026bf79e4cb8fb',
                        'TGLExt/F1Fecho394/BosonicFockGroupActions.lean': 'a61dc7aaec79ccbd3f95ba20a2233470c5d0891caf4da4915531bcf2794cb7a8',
                        'TGLExt/F1Fecho394/BosonicGammaJR5.lean': '6bd5e13a7ecb229bbb2f491115af140f23d88e30f7e3984a9c6a6f9f9d5c8382',
                        'TGLExt/F1Fecho394/BosonicSectorContinuity.lean': 'fa89a9b51ad66006d6b158f3221bacc3e932bc2b0780bc5aed1dd20fc2575ac4',
                        'TGLExt/F1Fecho394/BosonicSectors.lean': '97ed6c908653bb130dd1791c330a0ab2245097d67fd55428373bd6d4c640a68c',
                        'TGLExt/F1Fecho394/BosonicTwoParticle.lean': '510c5a61cb7570ab9c0360b038e57d880e7de5db63a0ec768141881c62dcd59f',
                        'TGLExt/F1Fecho394/BoundedBosonicGammaR2.lean': '377287a4268c011eda131fe1c37d4975cf2f9398074109e9482e27a6c46b6cfa',
                        'TGLExt/F1Fecho394/BoundedGammaPropertiesR2.lean': 'ac1562186a8a9e6252ed710ac3d8ea7c5863f825766a9d2219dd5c62386acbb6',
                        'TGLExt/F1Fecho394/BoundedGraphSelfAdjointR4.lean': '1fdd2d5df9c469beaa6b7acfbaa1abab0490f69019e7da6f7e1c8322b4ec6fcc',
                        'TGLExt/F1Fecho394/BoundedPairResolventEquationR2.lean': '9ff0ecd18ac6b7f4283c7f11ffbc388cd73801a96afffe4dcaeeaae53de8489f',
                        'TGLExt/F1Fecho394/BoundedScalarGrowthR2.lean': '4ef2941beafc557022a530af2556c98c2e9425ec329e2c12407aa96a2bb2f1ca',
                        'TGLExt/F1Fecho394/BoundedTensorMapR2.lean': '881f28262e407db3d9e5776fb097ec1ad7db5c4a25e9db121443dcfbc3734e32',
                        'TGLExt/F1Fecho394/BoundedWeakAnalyticR6.lean': '166eef2a1211d8d398de497ff6c7503c17e681c0e578968202bc514b9cc72f0f',
                        'TGLExt/F1Fecho394/CFCIntertwiningR3.lean': '21e15e720326b8c14cbc107cea20d14eff1ae75348687544122074a30f60a641',
                        'TGLExt/F1Fecho394/CanonicalFockAntiAssemblyR4.lean': '427c28636e26e73680c3ba5a41858022480c29dcad88f3576e534ea4e3629f41',
                        'TGLExt/F1Fecho394/CanonicalFockAssemblyR1.lean': '2b7f8210f52eb5f7cc72577bd9c952d350638ff49b03fceac17f5564778264be',
                        'TGLExt/F1Fecho394/CanonicalFockBWR2.lean': '7f9195fdced21d91a57fb1b1fbb9999c8048a096084806352a1133e2845a7e29',
                        'TGLExt/F1Fecho394/CanonicalFockDeltaR4.lean': 'd8010bcc7a6eb514df63b676a96801ee1c7f2fa452a02ce1fa6890fbb3289ed6',
                        'TGLExt/F1Fecho394/CanonicalFockDualWeightR3.lean': '979d9524edf758c61bac332c150c0302febe1a6010d85fd51b3e0452e90a5558',
                        'TGLExt/F1Fecho394/CanonicalFockFaithfulWeightR2.lean': '87da21fbe357e59afe92f539cbcaf709374c76e0709f638ddd4633f9e2ae5cac',
                        'TGLExt/F1Fecho394/CanonicalFockFiniteStarCoreR1.lean': '275dec912f0a27569b2eac0b3ce8f4d896c449afb95dafa09724176b042cfc11',
                        'TGLExt/F1Fecho394/CanonicalFockFiniteWeightR4.lean': '41c52c2c0ba0fa5785c7b733d6d3eefc563b4a700a66b2ee3a2b19de58d49ee2',
                        'TGLExt/F1Fecho394/CanonicalFockGNSNormalityR4.lean': '55bffc103ef04d6987e4d6f4c487f1177282f2bd2e012f4c5a4242bfe75ce0eb',
                        'TGLExt/F1Fecho394/CanonicalFockGNSR5.lean': '0b4fdc3aa6096776e9bd77263d9d7ab9c89332ce6d2104edcaf933692eff13a9',
                        'TGLExt/F1Fecho394/CanonicalFockGNSRepresentationR6.lean': '3237e9342fc60c1d0d572b0f1197508c390cf6c1b92547c5031f2517fc06c23c',
                        'TGLExt/F1Fecho394/CanonicalFockGraphRealizationR3.lean': '0cf04ff31217370a21c2d138b7c72142619b9c16081ec1f4367bccf685c70b7b',
                        'TGLExt/F1Fecho394/CanonicalFockModularFlowR2.lean': '2d12496fb6f8e7f879db5189d34231a37e32684002dc469f2bc8ee17f205bfa9',
                        'TGLExt/F1Fecho394/CanonicalFockPolarR1.lean': '298db7ce5380a575731a531be91b5b965a966f394d3cc49886fe72ba302763df',
                        'TGLExt/F1Fecho394/CanonicalFockRegularCoreR2.lean': '55ef551bf11b8a04b7d97bd5e8f19c469caf230f7750de8cd7d7c549ae08b1b2',
                        'TGLExt/F1Fecho394/CanonicalFockWeightClosedTomitaR2.lean': '6c41fa41d56bb2123789405a8cb7974362afacc1bbcbd2dac72ccdff9fcfc50f',
                        'TGLExt/F1Fecho394/CanonicalFockWeightGraphR3.lean': '60d514f6dd15a97d5ff42a6849980c39ffa1914194487b41e11c4319824a4b9e',
                        'TGLExt/F1Fecho394/CanonicalFockWeightModularFlowR3.lean': '0e4481641beff957b505b7ac7038fddd4313940859ff934d9190bcbba2489c70',
                        'TGLExt/F1Fecho394/CanonicalFockWeightModularOperatorR3.lean': '6a46b1b18851a03de26394bd1fcfe731e0d47827e7dabba3212a57979c3bd9ff',
                        'TGLExt/F1Fecho394/CanonicalFockWeightStandardSubspaceR2.lean': 'f82ea6981022f5314a4e071e234f89c545cb1889ada575482f958e0fef9b9b1a',
                        'TGLExt/F1Fecho394/CanonicalFockWeightStarDensityR2.lean': '5d69f7eb2dd84bde33a525158c164c877f69efc93610e5d6b861e9a60e79e24b',
                        'TGLExt/F1Fecho394/CanonicalGammaNoFixedR4.lean': 'ede7db4c2d6a69bfb819548324570660f67f9a45ef897b902fe47bf19a19457b',
                        'TGLExt/F1Fecho394/CanonicalGammaPositiveR3.lean': '9f0b73dfa6fd5ba678e46138550c985643be16fdfc44c5c13a3493b12d432ff0',
                        'TGLExt/F1Fecho394/CanonicalH1StripR3.lean': '0955ee0e4cf336f311ed010c3cc7469a001b88d48f2e457b09d86ebae5ab887a',
                        'TGLExt/F1Fecho394/CanonicalJBoostR3.lean': '188f7f98a3c4fc5fd7e7f33dd3be29b6f4ac7e0ce02db348006998bb221cf903',
                        'TGLExt/F1Fecho394/CanonicalModularCoreAssemblyR1.lean': '96e57e4a631adf56c56c33d5ec96464e8120eb7daa4d657fe2e754b63c0fa993',
                        'TGLExt/F1Fecho394/CanonicalOutput.lean': '69816e80c2d0bfd3f11ce0d8507c5f4f5fa5724e44bbfdf2c823bd93a091141c',
                        'TGLExt/F1Fecho394/CanonicalSegalEssentialR6.lean': '3f17cc92f12a53a94895ec9587946d389888ff5e6e8faff972c6c15c4050fd8e',
                        'TGLExt/F1Fecho394/CanonicalTensorBoostR3.lean': '8f14521b44fecfc23635363d96f9993e63f2d8681b9a9adf54d1435b6af85774',
                        'TGLExt/F1Fecho394/CanonicalTensorCoordinatesR4.lean': 'f1064a4880737bbb66711c5b1f576a57da3d42b8b746e857e1d2f005899875ef',
                        'TGLExt/F1Fecho394/CanonicalTensorMultiplierR3.lean': '5bb2d5e4c033ddaad047effc21fc4718ff1c78adf11129f955fbac5c9138048d',
                        'TGLExt/F1Fecho394/CanonicalTensorResolventEquationR2.lean': '51092214b16d5d087a11a56dfaa1489ad640fa185fb6589c0a659f9723569381',
                        'TGLExt/F1Fecho394/CanonicalTensorResolventR3.lean': '8553b49222cf999991f13ffbd67196502b12a385bd2cb829af56401658c62dcd',
                        'TGLExt/F1Fecho394/CanonicalWedge.lean': 'c49877fa465c53efe2aac44d70f7d09ef3fc30d4e52e1e737090328584a92ebd',
                        'TGLExt/F1Fecho394/CanonicalWedgeFlowR2.lean': '13fb80cd6c231bc0b0dbf8d13950a32ca6ad80a67a2e0dce4a3f2e8a1ce118fe',
                        'TGLExt/F1Fecho394/CanonicalWedgeKMSR4.lean': '106414e4518cf944374bc75ebdeba1bd49b9d47502ab9c36f52ea0790666a721',
                        'TGLExt/F1Fecho394/CanonicalWeylAssemblyR5.lean': '576af5d7a1be4830166bc89a7ae29b85fc28e8288d570a8a3c66234fe0be082e',
                        'TGLExt/F1Fecho394/CanonicalWeylKMSFiniteR2.lean': '296acb58e349c664fa5ab27ebe2d69517cdf3ba8d567e8e7705e691402862c1a',
                        'TGLExt/F1Fecho394/CanonicalZeroSectorFlowR3.lean': '466b656e147cfc1b9554d449c7a760562e6062f0ef304770e4f008f1cd8d7977',
                        'TGLExt/F1Fecho394/CanonicalZeroSectorResolventR1.lean': '24a8ecc65cb6b65c3f8706b98c544acabb273eb01bbfa4f37f4443a904c83fbd',
                        'TGLExt/F1Fecho394/ClosedTomitaFlowR1.lean': 'a646586e4ad4b2c6aa366a152760c7058137c613e044728c09520be76590af66',
                        'TGLExt/F1Fecho394/ClosedTomitaOperatorR1.lean': '195c594de3b22f718d7a0a6e74ada0538c69b76b1719b4cdcf4e6d326dee03d5',
                        'TGLExt/F1Fecho394/CompletedTensorStructureR3.lean': 'b54e99828e2ecbebde57f086f0c3a247d9183a8529b3b6a4121409b39433811b',
                        'TGLExt/F1Fecho394/ConcreteLightRayNet.lean': '8e3fca4341e09f55abc7dc3e0fca7c08d0e6e6af32d8ec6508654234dc5a0eaa',
                        'TGLExt/F1Fecho394/ConcreteWeylContinuityR2.lean': '1b6c5ba8c124f764f1faafc05f38a965c89a1930f95ae72e391258d68e9d1114',
                        'TGLExt/F1Fecho394/ConcreteWeylR1.lean': '51a25c823c1e8f2fb2da3a0956ea097bbcf016b9fda8d1026f987ca0be961af3',
                        'TGLExt/F1Fecho394/ContinuousHomIntertwiningR2.lean': 'be045aede9ce94d5b0210a696b78929f408d94c466d6afe0099c1d15bedfa8c1',
                        'TGLExt/F1Fecho394/CreationAndSegalR2.lean': 'f331e44c736bd1600d87d32274d8f769cb62ca83236a367060f1742a1e58f9c5',
                        'TGLExt/F1Fecho394/DeficiencyCriterionR5.lean': '1d57b26692ddc926bbaeacdb69c4dd6a6130eb624468be0f92d119241a9e6f4a',
                        'TGLExt/F1Fecho394/DeviceRootObstructionR4.lean': 'd3091ce1e686fe62f86e1eb79eb88d56bbefefaad5df4bb773a2d6c89e76e150',
                        'TGLExt/F1Fecho394/ExponentialAnnihilationR2.lean': 'cc8243318be70aa484ff9bea876309158d572682008acda94d4e9b904739f739',
                        'TGLExt/F1Fecho394/ExponentialCreationVectorR2.lean': 'db066e6d04f972cd3300aa9579bc14b2778dbdea11ac43a94b2d4bd258880dbb',
                        'TGLExt/F1Fecho394/ExponentialDirectionalDerivativeR2.lean': '8d9dfd2bd0512240558db40ea913e30330c6bc9eeee0f6a2d98ffd47d21dd906',
                        'TGLExt/F1Fecho394/ExponentialLiftPositiveR2.lean': '1adacbd284aa60e9f4ebb24ac5b8e225fc009a697d741c8ca7e238e810859594',
                        'TGLExt/F1Fecho394/ExponentialLiftR2.lean': '557e4b742569e70391500bc60a62dc01d7fb695c8b812156a68a190fb079519d',
                        'TGLExt/F1Fecho394/ExponentialTomitaEqualityR4.lean': 'fb3a62e4b60491fb1c3ae2e93cd3abaeefa1a26d9e8f8b211fda4cf54b2546b4',
                        'TGLExt/F1Fecho394/ExponentialTomitaInclusionR2.lean': 'f5c72bd9014a7871ab49a5dbb0137ab81c49eca5ec5517568032deffd1ffdb1b',
                        'TGLExt/F1Fecho394/ExponentialTomitaR2.lean': '5da4456eb2474892125feb1c38ec707752a6b94685217c18c3817341cce7ddd4',
                        'TGLExt/F1Fecho394/ExponentialTotalityR4.lean': 'a762da51787df414d3793ae5dd11b1a9672367b3d3fb8d667d19d6d1135ed8ea',
                        'TGLExt/F1Fecho394/ExponentialVectorsR3.lean': '403d2fe1ddeff3f5028a85ca778922c3a9924014e62eb3ed18855dad3655b9ab',
                        'TGLExt/F1Fecho394/FiberConjugation.lean': '4237c28556833aa3f7f52f0e0b377da47ed6a2b8d4cf31f0f3eba7e6cea79c93',
                        'TGLExt/F1Fecho394/FieldWeylR3.lean': 'e86e512b80f10c2ccd55eee55aa41ff0a48a873af708c11845f2aa407ffb3433',
                        'TGLExt/F1Fecho394/FiniteCommutingEigenR3.lean': '52fb1cac9b8217c21da5beba068f0f15739c234d5d1920ea752682b403d581c0',
                        'TGLExt/F1Fecho394/FubiniL2.lean': '829f72d66eb491a1477a04b872150e9446d2b72c4fd52e60928231e027fe9d90',
                        'TGLExt/F1Fecho394/GammaGraphParametersR3.lean': 'e1d90ea17c4fe0d59c6f17a51ea53e61e5a71dc38962751641d74e5e7951ae7a',
                        'TGLExt/F1Fecho394/GeometricFiberConjugation.lean': 'b0556245eda24c4f03204a1062d4e3a69a64f507ac9ff15c15078b1325f9de5a',
                        'TGLExt/F1Fecho394/GramTotalExtensionR4.lean': '00bc260de48576dcbb76c6142cdc42e29576158c6a76d59b301459175174d92e',
                        'TGLExt/F1Fecho394/HalfModularStripR3.lean': '3c772f72355a50638e394d216f1646fc4529887a6e9e5080e0cacc1f7734b0a0',
                        'TGLExt/F1Fecho394/ImaginaryPowerIntertwiningR2.lean': '23969f221635c127798065b7a3c926635b845314de858fc8a94c077851e50e0f',
                        'TGLExt/F1Fecho394/InvariantUnitaryEssentialR2.lean': '0592ea310a735ad2d2762accf211850099bf69938406c75e0bb3d264e91c2ecd',
                        'TGLExt/F1Fecho394/KMSBoundaryExchangeR1.lean': 'a19a338d7e670c602abe486f1ef97fa75ae1b2943a4a6e4f609156058a71c832',
                        'TGLExt/F1Fecho394/KMSFiniteSpanR3.lean': 'b85b4188da168304c74d37675e4b6ac0a6d61e4f2589e973482c223649bf6d2b',
                        'TGLExt/F1Fecho394/KMSGraphClosureR3.lean': '6923acdfefe253007120847b664b32ac2337a759bf116e5320c87b9a2299eb42',
                        'TGLExt/F1Fecho394/KMSStripIntegralR2.lean': '9b1846f662fcf921cea133d6ef0afa5cb57355ababca0627d8cbd513b1b19050',
                        'TGLExt/F1Fecho394/L2UnitaryMapR2.lean': '0cd47e2e4faffc8e449a1785cfe91805c43fc34d15d01c14a7753e67ff1dc67b',
                        'TGLExt/F1Fecho394/LorentzFutureGenerationR6.lean': 'f3700dee3caa4611438902cf7ba1ed9b772f02a6df4754132d8dc72a07fd9ed1',
                        'TGLExt/F1Fecho394/LorentzFutureRepresentationR1.lean': '7a97040b56ecae8a6cb7b48279eb4fb519cf9e6c6d120b25330048429fdcc8ae',
                        'TGLExt/F1Fecho394/LorentzTimeStabilizerR4.lean': '9b2ecac500853cfb74ed69ebbf0d0e2bb179c3f8ceb256695610b59184064210',
                        'TGLExt/F1Fecho394/NetworkProofAuditR3.lean': '869c38c2efeea611260a015d255fb22aebda2303dd9b6606598fe493b0023fb2',
                        'TGLExt/F1Fecho394/NetworkProofAuditR7.lean': 'b59f3fd788a22554fb9738aa6a5dcd378a66785e5977b27d877c17a129dd9bd0',
                        'TGLExt/F1Fecho394/NetworkProofAuditR8.lean': 'caae4fb8599141f9fd94dd72e3d5fea84203338cb52e9b0e640e8ef4d4fd957f',
                        'TGLExt/F1Fecho394/NoFiniteInvariantR3.lean': 'f05e1cd1c3f9cff974620a6d3662c04e21fa1e6d16e8d4fe14ac01e4ac70bd91',
                        'TGLExt/F1Fecho394/OneParticleDualityR2.lean': 'af1bc94972c51795e9e0e8dbbc456bd4b13b74306e33a61cf07e7454b258cfdc',
                        'TGLExt/F1Fecho394/OneParticleSymplecticR2.lean': 'ca22045ea7db5c11b18f4c64164ab7727a81938b544c27cf5730d2132ed2818a',
                        'TGLExt/F1Fecho394/OrbitalContractionAnalyticR1.lean': '5a3c3c4ec0c3bc66fa3a83dd4ba9f48a887a55da415ea0a873441a1b5be97618',
                        'TGLExt/F1Fecho394/OrbitalGeneratedCovarianceR3.lean': '1239624e7ecd910eff07691eece2943d1b5d804b4ab8b08c14972b104dcca93a',
                        'TGLExt/F1Fecho394/OrbitalGeneratedMeasureR2.lean': '443005e57beccae3bd757fd73227f67680df38bd5ef37b23c6de491cb1655f5b',
                        'TGLExt/F1Fecho394/OrbitalGeneratedUnitaryR3.lean': '56745d94fff6637a5516552bf935e4f78b7c8d26581e54811fd6ca76658fb823',
                        'TGLExt/F1Fecho394/OrbitalLocalFinitenessR2.lean': '0be8beaf953e8716deeda0ca51a9469b5d0af4baef9082496999cd06f09748ac',
                        'TGLExt/F1Fecho394/OrbitalOrientedBoostR1.lean': 'a091966a35b51acf705dfeb53e8bcccacb42aac18d1ccb4b1680e12e65d98c9d',
                        'TGLExt/F1Fecho394/OrbitalSpatialContinuityR1.lean': 'f70f289b09b3ca2312d352a3e947049801079192ce1211d9bdd8bad2bd518ccd',
                        'TGLExt/F1Fecho394/OrbitalSpatialCovarianceR2.lean': 'b99b0bf74d5c1ccb3e976dcacc67560f87050653a7e04e2a3b208e9cf4ee9485',
                        'TGLExt/F1Fecho394/OrbitalSpatialLorentzR2.lean': 'e26723e9ffa39674865cd7246bdefb00134d221320427c4bca16e5b9d2977a9b',
                        'TGLExt/F1Fecho394/OrbitalSpatialMeasureR1.lean': 'ab24fe767e08a9bddc764b11fe63f8c06f0e070b4e6f2d6ddef968d7896f8c11',
                        'TGLExt/F1Fecho394/OrbitalSpatialPoincareR2.lean': '108641e56f661c6083447b1a86a059bffb7ebbe7858cb659faa20867d4dffc20',
                        'TGLExt/F1Fecho394/OrbitalSpatialUnitaryR3.lean': '48de7fa22836154ea0353c70d954dad9cf8e9267f3db4f266440b16bee8c8485',
                        'TGLExt/F1Fecho394/PairClosedTomitaR2.lean': '41c8f58aaee82c6eb12398f3e9c6b7d76d35bb02470589ea7212843a2a686101',
                        'TGLExt/F1Fecho394/PairTomitaClosabilityR2.lean': '31f9653ecd2eee44746d54abacfa327c131d9f0eb29f2b6e4a5709acfbf7dc5c',
                        'TGLExt/F1Fecho394/PairedExponentialClosureR4.lean': 'fb6164fff1d59808bd48fca4352712d3249aa612ea092c1193618c9179bd0d89',
                        'TGLExt/F1Fecho394/PairedExponentialPolarizationR3.lean': '1e4f87179c6173f86af455ce6be1f7d5c2ebb3e40f8c31984bb5ef971edcf001',
                        'TGLExt/F1Fecho394/PartialSquareClosedR3.lean': '1b1453994c3b364a68af63d8c0fae8b12ae48752900c603dd40933a50b507ded',
                        'TGLExt/F1Fecho394/PartialSquareGraphR2.lean': 'e5d405ecb2c54c4e90c6eb95420b53bfecb8cac279ca8a6c02103691d830627d',
                        'TGLExt/F1Fecho394/PositiveRegularizedRootR3.lean': 'db588bb5e6b47a96d237a81764dfd4358197b9d4ec43fbb041ac4a3f6efafe89',
                        'TGLExt/F1Fecho394/RealSubspaceTotalityR5.lean': '9db306cf2db6e7b104bcb87512f3c0ad8037d6a78a7b3c030f65e62a73496e3c',
                        'TGLExt/F1Fecho394/RegularCoreAverageR2.lean': 'b323e525b5b3b8db26b97d2cd9bf4ba33ebcb69f2f5c59babe8b8ff9d7977d1a',
                        'TGLExt/F1Fecho394/RegularCoreFiniteWeightR3.lean': 'd115c6a50fc6853b471185e1d91913324bcb5b1f321cb8cb79564bef51035249',
                        'TGLExt/F1Fecho394/RegularCoreFixedR3.lean': '3f32d9162f30d206166b739d8f501755c3b73fe2104f3d20e5c7a577f1a87d35',
                        'TGLExt/F1Fecho394/RegularCoreResolventR2.lean': '74550d713a333d4c8f39b148bade079a32c429c1382c48f9e985e555921e1391',
                        'TGLExt/F1Fecho394/RegularCovariantCoreR3.lean': 'd474ac36c8d8e12a2d7d7a83b69f30fddac5e28935d8b7b81a436e352ddd532f',
                        'TGLExt/F1Fecho394/RegularFiniteStarCoreR2.lean': '8f12373f727cd758522fcbed9d1fb0a05617bc0d83fdc4c750051936cb9aa7c5',
                        'TGLExt/F1Fecho394/RegularScalarClosedTomitaR1.lean': '91e84e80ba1b9a9f41e4c64874c7f1e0313f83150e954725971204d7d10c2be6',
                        'TGLExt/F1Fecho394/RegularScalarGNSActionR2.lean': '4d085de13a2e0f07f7175677179aee0cf86225060c044dde3ee473e43fbcc8e6',
                        'TGLExt/F1Fecho394/RegularScalarGNSNormalityR2.lean': '53c021216f33e5e7f590f2ed33c347456433cab375180fb9b4d3b49e87e725fc',
                        'TGLExt/F1Fecho394/RegularScalarGNSR3.lean': '19cedfd9957dbe41b0ed1e85a7697c049113a96b3f7f58cb19dbbf70c2dc4e5d',
                        'TGLExt/F1Fecho394/RegularScalarGNSRepresentationR2.lean': '5f9d6801a987410e700a5a6e28e3382e02d630f60497ad5eb59cf193ada8060c',
                        'TGLExt/F1Fecho394/RegularScalarGNSStrongContinuityR1.lean': '0dcecea4ba97fe9115e96884d3aac97aa126aed3e4a3c924a9bd73156d9d3d75',
                        'TGLExt/F1Fecho394/RegularScalarGaussianGNSR2.lean': '106e7e8ab9e82f1cfb0d34d4c54f5bbd5d194a79372fd190788b5450bd77b51b',
                        'TGLExt/F1Fecho394/RegularScalarGaussianR1.lean': '5993ffd9add3693efedcad8406c9d518bb5ab45e3bf472787fe56dcdf6c8726d',
                        'TGLExt/F1Fecho394/RegularScalarStarDensityR1.lean': '6261df75d4ec4332c46ad352aa380ecca996d98ea9aa53bd51884c17846065a9',
                        'TGLExt/F1Fecho394/RegularScalarTomitaClosureR2.lean': '0882a8e5524c4a8e832ac51a561fe8299ee734018c2af7c178194648ea353cde',
                        'TGLExt/F1Fecho394/RegularScalarTomitaGraphR1.lean': '6382578a12651e45cef6ee1d1069bcdbc4b27a5aae9d643fcb0058b6f4e8a818',
                        'TGLExt/F1Fecho394/RootRateFrequencyR2.lean': '7c039885205bc603fbd713ac39b444a9c4a4c42dd7351dfd960cbc98f1284bba',
                        'TGLExt/F1Fecho394/ScalarL2CalculusR4.lean': '1ed5d4974f2abdb2b81b04014e6c72840dce8349f265a983efa9ed357b0ab8ef',
                        'TGLExt/F1Fecho394/ScalarL2ImaginaryR5.lean': '0a3c21c433622a02ac7bcdd29670bdf52f432c3f6b75218b494c2eeb4a566974',
                        'TGLExt/F1Fecho394/ScalarL2MultiplierR3.lean': '06a735484f4441bca063ea3758472d462ce3c232bc6e04655090a4562d0ec9c9',
                        'TGLExt/F1Fecho394/SectorDirectSum.lean': '74ad55c71d855a5306296ec6698162e6af3d569b80cc4825399957c3d548e276',
                        'TGLExt/F1Fecho394/SectorInfiniteDimension.lean': 'f994e87f860232eb2a91aabb255401585fbb5a5849e548beaa2b152399682ab8',
                        'TGLExt/F1Fecho394/SectorStrongContinuity.lean': 'f0178c113baae6510ee59dce6b16aa9f96c67fd1230452dc1478b78b2ca926e5',
                        'TGLExt/F1Fecho394/SpectralConjugation.lean': '86be4a38ae2cc0283371e3ce4ddbf5b496a71faf3739f72c6df483866931248b',
                        'TGLExt/F1Fecho394/StandardComplexSpanR1.lean': 'b9d79756ce8fe9e17bd0c3e8a7a9b45c7fd216d930d3f46ce3bf070aa447e29d',
                        'TGLExt/F1Fecho394/StarGraphDensityR3.lean': 'b765b33f10ac1323b291160c6aae3d1abcaa0456da1e314759781e3facc20717',
                        'TGLExt/F1Fecho394/StripBoundaryLimitR1.lean': 'a7f1f7e80b92f014ef84d47324d669f6dc0a6322439446b403da44529a5acc07',
                        'TGLExt/F1Fecho394/StripMaximumR2.lean': 'cbc8e43fd384fe7f2067775d3f16d204a3363b3277ede53183e5cc92a4996f99',
                        'TGLExt/F1Fecho394/StripPhaseBoundsR1.lean': 'f3149b788ba977f35d080891ff22b10d8dfbf97a71b6bc9839d2d78509245a25',
                        'TGLExt/F1Fecho394/StripUniformLimitR2.lean': 'b5e2d7f13c5b691ac786c5641109c085ccd90ddd89937a114f0c9a6c44cf09d8',
                        'TGLExt/F1Fecho394/SymmetricClosureR1.lean': 'f3595e0d76f7c6a7edd6d74cf8e87a68dcd6526c14401ca80a33d655ab7cc523',
                        'TGLExt/F1Fecho394/TensorContractionPropertiesR3.lean': 'bf91618a0fa302be5a3110c0b6ef13244e9151cd8d0bb7d648818aa12a7cf2b5',
                        'TGLExt/F1Fecho394/TensorContractionR5.lean': 'b548097dbb63af66a2f4a8b7d9d50a4d303e546939705133a20948e466ee297d',
                        'TGLExt/F1Fecho394/TensorL2EquivalenceR3.lean': '71c9db3ce5c1ef53c9357ab47ab05aac5743e0f6b4acf0daa1771c315281997a',
                        'TGLExt/F1Fecho394/TensorL2ProductR3.lean': '12530b9d0863240c7bb78960ed3e25e1f90a7183ec1e1fc77d719db1570a2883',
                        'TGLExt/F1Fecho394/TensorNoFixedR2.lean': 'e17eabefe76cfbda1e3089ce0cbea3271be836bac5c085e783d1d01b03dcfa78',
                        'TGLExt/F1Fecho394/TensorResolventScalarsR4.lean': 'c571f9a47c7e24521891ab5239ffd80bdd8aa44d57e8340caf2e2254418c7a87',
                        'TGLExt/F1Fecho394/UnitaryCoefficientsUniformR2.lean': 'cd2cb6319a4103818c6363ddcad1c1d1f9dfc1a86c7251f726128b65139306bf',
                        'TGLExt/F1Fecho394/UnitaryNoFiniteInvariantR1.lean': '1268006dd7b33a37ce4362d95acdb2c100f38653587b197e645b717688dbd0a9',
                        'TGLExt/F1Fecho394/VectorSquare.lean': 'f96c862383f7bf1c224f2b246a2ece4e6aa2e6936f666e27a7215a75b313045d',
                        'TGLExt/F1Fecho394/VectorTensorL2R4.lean': 'c2e550bcbcb9ab14d021b19a147d85bdaa5ff3d795874c873e840710aea29256',
                        'TGLExt/F1Fecho394/VectorWedge.lean': 'a047e312e5646f1d0ea104b2a2f3767b9c690cee391f0aa14ca5682841269f52',
                        'TGLExt/F1Fecho394/WedgeAnalyticR2.lean': '26b8e809342dee5c739bc7c7412072a80baa1b5bbb87fbf88fb831056dd7ee76',
                        'TGLExt/F1Fecho394/WedgeCyclicR3.lean': '91afa52a5d8ec183872a4da53dd23951d4413106bc643f4e55eec5de1152edaf',
                        'TGLExt/F1Fecho394/WedgeNonabelianR4.lean': 'c4707c51d2576a4de332c191a0b2ca3eeb96a63171862dd73cdb02678b7cf4f7',
                        'TGLExt/F1Fecho394/WedgeNonisotropicR5.lean': '4e8f334c8e0597bd303e4b04df259059533edcadcc4c9f392c1e02b36b95c59b',
                        'TGLExt/F1Fecho394/WedgeOneParticleStripR2.lean': '91ddb87a4f108e4271c2ec5cb3a79d15ed096725922050dd84a7e4f7539868ae',
                        'TGLExt/F1Fecho394/WedgePairTomitaR2.lean': '5c600b7e1c2866bdebd9d9a9d54e392d45d47f52845ebfecf064a98ed2d0dc0c',
                        'TGLExt/F1Fecho394/WeylAntiunitaryR4.lean': '3167bdd5ec36aff464be1e9015a050a86382b867bb1d88f41e180cc2e475b45a',
                        'TGLExt/F1Fecho394/WeylCoefficientsR4.lean': 'c0a7fa639d1c2aea0e23191cb0867dc826468b5691ea5fa2ce636b544f1e50c5',
                        'TGLExt/F1Fecho394/WeylCovarianceR1.lean': '394273c2ebd33f00ffa0ef5b9a3d976cd5ee6314667a90e05da9ce4cf2a18bcb',
                        'TGLExt/F1Fecho394/WeylExponentialGraphCoreR4.lean': '3acb95a6a2dc1b15468924d9f109d2a36494180a24fc04dd629a27ae95355a54',
                        'TGLExt/F1Fecho394/WeylFiniteAlgebraR4.lean': 'cbc3515836bfa99ee45e65537d3d083bea03ae682a4cbde18e7039060932b44b',
                        'TGLExt/F1Fecho394/WeylFlowWiringR4.lean': '2814c99ba3b763937abaceae09a49723b16232566f83b5b9529d397b525db57b',
                        'TGLExt/F1Fecho394/WeylNetWiringR1.lean': '7d9b82076318ea30a9d4aee26578b442622fff4bf03baab98a5b3b7a950ba405',
                        'TGLExt/F1Fecho394/WeylOperatorsGenericR2.lean': '76164e951079ce04a5642a88d8644ebe9413e28ffb8768cccea20b43fa72cced',
                        'TGLExt/F1Fecho394/WeylSegalDenseDomainR5.lean': '28f452fdf6ffca2d6e775c8e992a668e74a3196c9879b2a0d8b4dc1fa2f4a1b2',
                        'TGLExt/F1Fecho394/WeylSegalGeneratorR3.lean': '7c9cda998cc7bb7382906052026599c5a55d25f58b3fa181349a91d3ef05a1fe',
                        'TGLExt/F1Fecho394/WeylStripFromCoefficientR3.lean': '1501ca4ece750063f2b2c61b3fb6085e2ccf7593c8fb6d1c03d602b45bbccb41',
                        'TGLExt/F1Fecho394/WeylVacuumCoefficientR2.lean': 'c153c11d60f94829bc8465caa5acb97068f5b4f8664d5028c5932283cea0aaad',
                        'TGLExt/O16/AnalyticBoundaryControl_v2.lean': 'c33411a05d221c2ef566a7daaf9fe502cf1884261524d4759978eae6c3720cc2',
                        'TGLExt/O16/AxiomasContorno.lean': 'db569a4977e27427458ea93d1c259ce4e49ec0cc87778e739ad2d7ca3e72233f',
                        'TGLExt/O16/BilateralFirstOrderReuse.lean': 'c478f2a376a910cac2ddd15aa3c60def2afc8d362cf011b98e9dd8901884989e',
                        'TGLExt/O16/BoostHomonymBridge.lean': '1225cde1d17f231049625aba70d5b7ffd865ec5381fe705682e5c6e06c72173d',
                        'TGLExt/O16/BoostRepresentationBridges.lean': '0a01bfb3a9f99f8dee0c7abbeb031245fff8b59cad04b98d66a51e4684b050ce',
                        'TGLExt/O16/BoostScreenPolarizations_v2.lean': '0a3f83f932cc7d889173767f21a9c25b8fabbd5baebd3c636dcf3e5cbd8574ac',
                        'TGLExt/O16/BoundedTransformCore_v2.lean': '529a0906c08d7f712bae8cadc1189dfba5ae88146418d28c4325533ad316c4b0',
                        'TGLExt/O16/BoundedTransformFinite_v2.lean': 'afc4e1ec7261fee20ff12c9c896718132826404611ee1e6583463023e2344d9b',
                        'TGLExt/O16/BoundedTransformGap.lean': 'e3457999c70571e3cebf60d4aecb61c62697ea08f1b188fac9dd67c5e0b8cf6d',
                        'TGLExt/O16/BoundedTransformKernel.lean': '02b5907879173763834dc005812948bc90eafc7c1fe40000621da62630fb80ff',
                        'TGLExt/O16/CanonicalResponseCovarianceAudit.lean': 'fc1e986277b4c121fc41621f5a65f5262a0c1b3b960fe52dccb81b25db7076b1',
                        'TGLExt/O16/ClosedIndexChecks_v2.lean': 'befa9db0ee6dd2b16b788611ae1c7ff51a0ca0883a8e62060f187886e20b6e9b',
                        'TGLExt/O16/ClosedLinearGraphResolvent_v2.lean': '75c3ec1dff57aa87d7adc1622b48331e1426d91338efdfb7d9799ed0ddfbc758',
                        'TGLExt/O16/ConjugatedFormScope_v2.lean': '65b4165324739c723aefbac05b206246e712f202f4120cea25717207039b6536',
                        'TGLExt/O16/ConstructedImportH3_v2.lean': 'dd8cb7d4d56a3fd80e401bc4f77e909e10ed03f7331a7d1d963ab22820a8643e',
                        'TGLExt/O16/ContentContractProposal.lean': 'ccb7ab272f592b82d68017e75170ed2bcf906ca0bd1a1c69479b1c30de5a8269',
                        'TGLExt/O16/ContinuousBoundedTransform.lean': 'e8cb5d4e27fdfb245d420f98e60437f6206731aeec0b31cb03b2025a169fd80d',
                        'TGLExt/O16/ContractCalibrationReuse.lean': 'f447d2de1f54774cb53b5808fa99b3095536606695d8c0efad36675dd80326c9',
                        'TGLExt/O16/ContractFixedReadout.lean': '859b34cff1f856c5f7ab1110aa61fff0a4e6617f98276bd45042aefc1cc5af73',
                        'TGLExt/O16/ContractGroupA_v3.lean': '42f18045288736a174c58cf32015a592cc8c3736d9657dfe1e1c1789f437bfdc',
                        'TGLExt/O16/ContractGroupB_v3.lean': 'bc87743e3de51b5c06caa5e9baac5f86ff4a465bdb1fb7b1873319e460efe174',
                        'TGLExt/O16/ContractGroupC_v3.lean': '32e28e214c122cd61a7c9eae62b09ea1e17806c4a22ace5e29be963b766c183c',
                        'TGLExt/O16/ContractGroupD_v3.lean': 'e852a05a594d733cf85ba47290c2c3df454ea1b35b33138742c2c61ca03598d1',
                        'TGLExt/O16/ContractGroupE_v3.lean': '9702471b8515ff0c9cc2aa182c7256310cdbd97b60c3ef6251d9b1ef4489bce8',
                        'TGLExt/O16/ContractGroupF_v3.lean': 'af347f99f1774d00ea8efab00be7635216ac50314b08f883e8bf37a89d43a99d',
                        'TGLExt/O16/ContractGroupG_v3.lean': '36677342dd4501aaa5a892922b61e0f35b6cb49857e114bac8baf13020a53af4',
                        'TGLExt/O16/ContractGroupH_v3_Integration_v3.lean': 'ee842f003decd19acc67e0e346836056d7ff2e0e859be1ce32cdf9d91be02033',
                        'TGLExt/O16/ContractGroupI_v3.lean': 'd80e8ae42b7a5a0f1bd1f48e822cadf94df460fc95da18df05b348370f772a72',
                        'TGLExt/O16/ContractGroupJ_v5.lean': 'b8352bcd7963babe2786aa511ec26c99f3a139ea6cef722428078d9d2d8e7ee4',
                        'TGLExt/O16/ContractLoad.lean': '24072ec474a9aa26a1da48f2b10076d466e3ad3be9018a602006755bc183c035',
                        'TGLExt/O16/ContractTypeLoad.lean': 'b0e0acc34f9ce2d4e5e0e8c6dd4bd46669472cf19097ced0811f4b464c8e6008',
                        'TGLExt/O16/ContratoQG_v31_Minimal.lean': 'b78d03f09a1e5988d098aa3793fc6d5a20e29c0e35932c30e03c51bf8d87e381',
                        'TGLExt/O16/ContratoQG_v32_Proposta.lean': '75cbbf2ab14fed614443113233df486f0921e97cf3616e5606a2ad756b4ca56e',
                        'TGLExt/O16/DilationGeometry_v2.lean': 'b02b169cf9d3caf51aaf8c45951fa5109c6ab27f8c126889a72bc8968a9986cf',
                        'TGLExt/O16/DilationModularRecognition_v2.lean': 'de48dcb43e7738e1afc9639dc0c3198845b7dd94c728dd720b19772102be9388',
                        'TGLExt/O16/EmptyImportControl.lean': 'e41a11a8bc4565bf353d490933f8f8ef966a8d85eda0ee5be20fdd1c7be54db9',
                        'TGLExt/O16/ExactTypeReader_v2.lean': '63a7ac9b989e8c559e07c0f60f6597f6f56f8f5da06601b95a5e0d1a1dfa177d',
                        'TGLExt/O16/ExistingKillingCalibration.lean': 'e1aebff470203fb62a3a6fa1296ac29037c096bd644d82c55df909138dcf5e8e',
                        'TGLExt/O16/ExistingTomitaAudit.lean': '6f0b0f6dbef01e245b761a789f01264edcf22820c0c9eed18f8b1f232375b945',
                        'TGLExt/O16/ExistingTraceCompletionAudit_v2.lean': 'dd2999c3717e9e2dff49a3a46abcdf5d82060624d3db65a83a6bda6c06415a2e',
                        'TGLExt/O16/FiniteCenterFlow_v2.lean': '75d49113065f361999f4dad6925797a69d9090746032c99a7cc7c4067bc276a6',
                        'TGLExt/O16/FiniteGapRate_v2.lean': '422be174f625cf0e48657803be9edbc1ef91b880c1054758843800bae054659f',
                        'TGLExt/O16/FiniteKMSStrip_v4.lean': '40bc64b05b7cf916bb7058cbe45260d60c05d81011b5f6ecd7637301036f66d5',
                        'TGLExt/O16/FourierLightRayBridge.lean': '33b41225e02c5b6c023bc501477c3ef1d754aba9f3f4c365b9f6e69d289d52d1',
                        'TGLExt/O16/FourierStandardTransport_v3.lean': '0905a2065add4b7435a5954b0760e65eed6485df3ff1713a7ff8695e91ad1d5b',
                        'TGLExt/O16/GudermannSpectral.lean': '83c3942bb99c6e4ed7ed48f4a4bf97c6ae2679310d8c8d55fa9aa135a45bdf0c',
                        'TGLExt/O16/HorizonDataReuse_Integration_v2.lean': 'eeae8a4e4b40ed68e854e8a78b545363157dd14ca17c006764a63877b531b65f',
                        'TGLExt/O16/IdempotentDephasing_v2.lean': '67150c452701476a3f29f5b801636fd49d094b7439e91983d2b82e43199a893a',
                        'TGLExt/O16/InfiniteLimitUniformControl_v2.lean': '250b84828d57f76e0f31cc6063aa5b8aacccacdbcc4556a9121e26256fc2dd3d',
                        'TGLExt/O16/InscriptionBridge_Integration_v2.lean': '53d8ea45d61cbc4f7dc50f417db790e87d9f771df75a5b68c6a438f0e085aec0',
                        'TGLExt/O16/IntegrationAudit_Integration_v2.lean': 'b780a75e47ee20ff9688638beb77faf25ae7cd3eea085c0f04ad121cb77c2e82',
                        'TGLExt/O16/IsometricCocycleSpectrum_v2.lean': '73fb11cc85e3567358d45d91e330460c6a726370cb98a6dc80a189fdecfff0a2',
                        'TGLExt/O16/KMSStripConditional.lean': '54edf218bf6881c2dda3c3a71febde5d0ef3a2a00ac7a09593749d5de74c91ec',
                        'TGLExt/O16/LightRayAnalyticCore_v3.lean': '8be6798d3148919834681e6fc2cf848370e3ae3fa7211929a9ae3fc4157c6507',
                        'TGLExt/O16/LightRayBoundaryBalance_v3.lean': 'fc394ce657444c465fe0cab67fc4b0a8b341700e77b4b28fc905060f958348d7',
                        'TGLExt/O16/LightRayContourTransport_v2.lean': 'd887f13ff9c047630b3c8044c56d1450cdf0ffadd6d6b4affa312f6539c1dc88',
                        'TGLExt/O16/LightRayCoreExtension_v2.lean': '0958928d9f277ade375808eadaedaa75900047dc862cf4f4b864c6eab179e371',
                        'TGLExt/O16/LightRayCoreMembership.lean': 'dcbf7540c923c9f0cdc3de136ddefc7da948c44fe9501bb56347d1361238c72f',
                        'TGLExt/O16/LightRayDensitySeparation_v2.lean': 'a7596be3d5eedd1601e1f0351c8ba69c76047844b8cf38ece1e5adc8f966b21a',
                        'TGLExt/O16/LightRayFourierBoundary_v2.lean': 'e832a57f2d8a64688bf1c84812af56d52189f1f56a68e748f06f977085ce8868',
                        'TGLExt/O16/LightRayGaussianDensity_v2.lean': 'adfd9d64ea3a1ca21013059db2d4ef6cf180ec1238ff44fd4d5d338a24579afc',
                        'TGLExt/O16/LightRayGaussianL1.lean': 'f793d99e1d9cb484de051c402cbfaacdbe5da1757966bcb8b7bccae4b8e6a1de',
                        'TGLExt/O16/LightRayGaussianL2_v4.lean': '70f8b8c2212dede22761bbc8e261c00d43175c2c7d2664630d0071f361844a51',
                        'TGLExt/O16/LightRayGaussianOrthogonality_v2.lean': '96943ea17ee553db75fff6a280e20d715d9beb8e9827ee35e65d188bf41c9ce6',
                        'TGLExt/O16/LightRayGaussianTransform_v5.lean': '2dece1ccd2861b890db3d2ae1cf786b4183b930c5b095959a6557e36a33de2c6',
                        'TGLExt/O16/LightRayRealFourierUniqueness_v2.lean': '8188e0efbbcc8fbb639bf89ad85f1c61299df0765f85280c26ded2e1b832f69d',
                        'TGLExt/O16/LightRayTwistWidth_v3.lean': '6ddd1f9101d05ab873374fcbc2b003828f74d3caa07c30a228046d16ca80e7ed',
                        'TGLExt/O16/LightRayVerticalDecay_v4.lean': '4ac75e695bd4ad5ee360562461d7579bde636b0366095e053040d9b7f4442078',
                        'TGLExt/O16/MaxwellPolynomial_v2.lean': '5e5460abca91081c2c62a1454e3660273e93952b51f739cb34825941ae3c2782',
                        'TGLExt/O16/ModularBoostEnergyReuse_v2.lean': '246230b2a2768513f0d00139a35f5178aea8ba6a2dba6eef122d623e4ca064c5',
                        'TGLExt/O16/ModularChargeLink.lean': 'c4b2e2ad8d32779586bf1cee11189f02b36ed499cc097310b495149846d47384',
                        'TGLExt/O16/ModularGeneratorControl.lean': 'a9787e8b6e9e9976c99236b51e622ad29ee9f35ec07acf3d67aff27c65a59868',
                        'TGLExt/O16/NegativeControlsCompleteness_v2_Integration_v2.lean': '0e81bd9d558bb223bb403e1a8e9c0963b9ef1dea3ff60f892cda9eab17c59756',
                        'TGLExt/O16/NormalizedFirstOrder_v3.lean': '4e27d52639af301ad99d7a55103b4e41797ae96a5092ee2e3fa8f8f9dfd2e6d5',
                        'TGLExt/O16/NormalizedGraphContract_v2.lean': '0bc622bc681e3b76fe83e54a7809beb3202bb8202d4296b09e5191b98d1169ad',
                        'TGLExt/O16/NullFrameDecomposition_v2.lean': 'f451ac0daeb0e61b17ee367a4adfc46540e573ebc2ad7892b4c02a2ba8d1c371',
                        'TGLExt/O16/NullRayResponse_v2.lean': '8f3306b38fcec438afad248a4c097492c3a10c7440e11e6da3b289cf80e420c6',
                        'TGLExt/O16/NullScreenFrame_v2.lean': 'b17bf4dce18ffdac2026325ced726ec816031a7bab5a19699a5ad47036dba6f3',
                        'TGLExt/O16/NullSolutionConsumerReuse.lean': 'a78e1c92adbb68ab89daad95531bf73d9b669a0a359245d9445a13a92799d12e',
                        'TGLExt/O16/OperatorContourBridge_v2_Integration_v2.lean': '325569c79d7349ca48dbf882b5a3a8ef4ed52e24b61b7e0520317e2c17b02c0e',
                        'TGLExt/O16/OrbitTranslationFaithfulness_v2.lean': '6734ea61f7a6582ed333093307d60081b2ba175612724ca3b396ec9d3d14223f',
                        'TGLExt/O16/OrbitalBoostContinuity_v2.lean': 'e2efa9f2daa6e5d03946c5bedb40cf9191c760da03055f13f0b22c86c2f12695',
                        'TGLExt/O16/OrbitalBoostCovariance_v2.lean': 'b36bd280344bca105a513331f0e0c046116feb530e53b44c09bd15203b5f4985',
                        'TGLExt/O16/OrbitalBoostTransport.lean': '5b95c5568b9cfc99665a3c3f66d274a631663bf7530b679aaf0bd46464003dd8',
                        'TGLExt/O16/OrbitalBoostUnitary_v2.lean': '64875efc08ef64c8a738f0f3be42e228fd2440be69d5bc186d3be6ff17c63bc0',
                        'TGLExt/O16/OrbitalL2Equivalence_v2.lean': 'ecebfe05c825e7c88d2ae2e6bc1f8ed557245b4de5d343eb34b86f31ff336f5e',
                        'TGLExt/O16/OrbitalMeasureSupport_v2.lean': '87513093d1ccae17fbfc99087884a60339f86ed8bffa90a9991a0fe7e15f4d0b',
                        'TGLExt/O16/OrbitalPositiveEnergyContract.lean': '9536fc635a8c5fd8056f8c3587c6fcf18bdf8ade53c40dcfc3c74a8655b6831b',
                        'TGLExt/O16/OrbitalPositiveEnergy_v3.lean': '908ea917b59398fe99cbb9c5688bab7312933baf76a1511e4e40cb17f699e5a8',
                        'TGLExt/O16/OrbitalRapidityMeasure_v4.lean': 'e5e6b7605009a17973d76a96a4449dabdde56be2086b6718770a2c5ef23600d3',
                        'TGLExt/O16/OrbitalRapidityTransport_v3.lean': '8ce8d78b8082e0b7f7cb1d620920212e3647a4dc031e1d39be26b19b122c646f',
                        'TGLExt/O16/OrbitalStateAnalytic.lean': '0e5c461faf680849df16d21eaba02f52aaf17e26a0653abaab5614ba36c0cd46',
                        'TGLExt/O16/OrbitalTranslationOperators_v2.lean': '111a3d84deb9e3bf93c8cabde3840e330ca0ef45369aa6f8137d4317f3dfd4e6',
                        'TGLExt/O16/PenaltyThreeLocksBridge_v2.lean': 'e8680a0b83d4345faec4c720f5ce63bec340ce2e67a3c631d7975f6cc8a62c94',
                        'TGLExt/O16/PeriodHeatCalibration_v3.lean': 'e347d2331376bb76d8e56a60a2c3b5b86af1267bc742486b57fd4dc46acb21cc',
                        'TGLExt/O16/PhotonCharacterCocycle.lean': '08e03316e12e2cec7425ae8534e2ffb80718d11c575e1ee7cd2c1befa0d6bff7',
                        'TGLExt/O16/PhotonContractTheorems_v2.lean': '15bf81be762a73fd34b906e7fd4f2b0541a84a8b5d8d3c3fda6ee1a7cf03478b',
                        'TGLExt/O16/PhotonContract_v2.lean': '39e3bc93e0675c9894e1992cdbc3d4a87c90fef6555cdc15faebd4a5f95b90e3',
                        'TGLExt/O16/PhotonMassiveTransport.lean': '6721269ceb31ad09c125e1f2b2cfde3c836a0f203a49aa95be60409e1bfea02c',
                        'TGLExt/O16/PhotonModularRealization.lean': '3808f09937823672de44909ed3ffaf3d1fcb79cbd0d647c989d5060635d29aa4',
                        'TGLExt/O16/PhotonScreenCharacters_v3.lean': 'f179509af8edcdd875a2a38cf53a42093ce39ad725ea62f0ce5a1b6bcdd77580',
                        'TGLExt/O16/PhotonWitness.lean': '4a822e6d5ad00eba8c756defd786491fdcd9d3d0f56cca3a28e45f6a4f4134ce',
                        'TGLExt/O16/PolarMinimalPeriod_v2.lean': '2112c0022287be0941a798f67e3f5d6f47251e26067ed7ba64516a38424364dc',
                        'TGLExt/O16/PolarQuotientGeometry_v2.lean': '7e1f9df29a06451b6c6d24816055503fe10437038198551d149cbff127f0e197',
                        'TGLExt/O16/PositiveEnergyIntegral_v4.lean': '64ef6f5b790eb64ba135a099fd9f7c74eb95a136aeb19ab173342927a7a9326f',
                        'TGLExt/O16/ProbeFieldMutations_v2.lean': '898e39bfac072c8aaefffac4c8312deb53dfe2d5fcb07d01c502f5660ded6852',
                        'TGLExt/O16/ProbeForgedStressContract.lean': 'a3107ae32f52c279f969ff2a03daf8d0e0e9fb4d6d746363c479f0f6547fe9d5',
                        'TGLExt/O16/ProbeForgedStress_v2.lean': '3bc60f5d2d97735a4d4c67c17d6ebeb483b68f59d36ee445b2ac9f92211cfcd2',
                        'TGLExt/O16/ProbeNonKMS_v3.lean': 'b77efd218593bfa42e662d6767ebd45d362124d12de37ef0e45d7c60242c0a71',
                        'TGLExt/O16/ProbeNoncommutingInternal_v4.lean': '7ceec945173ed99c287ff147d1598cb3ec68d5c40e739b9bd565b86a549ffdb2',
                        'TGLExt/O16/ProbePositiveEnergy_v2.lean': 'd42e52cf2051f0f99a5e535488078df277b82565999aa5befde7713acb461935',
                        'TGLExt/O16/ProductOrbitalSpectrum_v3.lean': 'f144318b4f272336f72abddb6673dbca5718d7439b2344750e5f2d8f37b0a094',
                        'TGLExt/O16/QubitEntropyDerivative_v3.lean': 'cc2ac0d9289d265940e3726ebbe2d87cd3f4e5602f0afadd83a1097226ec3fa2',
                        'TGLExt/O16/QubitScalarEntropy.lean': '06256b83098141d05091322fa3dbcac6404900b677d95fe2509320d65a48add8',
                        'TGLExt/O16/RapidityJacobian_v2.lean': '5ffcabbd3f82e5a92e5e658869a09df50f233d371b88bc9d1461972b1f6004e3',
                        'TGLExt/O16/ReaderPositive_v2.lean': '24057603b4f4b614b244b1dd102bb4c8cae04f8a68d208be4e9067421a3851a4',
                        'TGLExt/O16/RecognitionGraph_v2.lean': '4be9c34d816df0b1bbd8b38a56fa574a6f1252d64d6d2cae7a7ac5ea90021e65',
                        'TGLExt/O16/RecognitionInverse_v2.lean': 'a43bd246ca6baa1776532982f2138d99542fadff646fccf88fccec907ee52015',
                        'TGLExt/O16/RecognitionModular_v2.lean': 'a56c2d6696343cfa194fa7c2cd268c94ddaaa7b5dd4656f536d84b4758b8d1f8',
                        'TGLExt/O16/RecognitionReadout.lean': '3ad278def76873c14ba9851916dc313f7e023d98503ffef93dfa8ef1ac759316',
                        'TGLExt/O16/RecognitionSquare.lean': '1fd91db87fc31b22df66792f776036e96610aae81e88c581e711c02084c8d720',
                        'TGLExt/O16/ResolventBoundedTransform_v3.lean': 'aa3d69e552eb93b818b41fcfc8b34872e88233e8763045bb121e68b6cb544ba2',
                        'TGLExt/O16/RetaDeLuzBorchersAudited.lean': 'c3a5f10920c2ed46d682219f25f77b1d4ff0b9b68d88e33ab9c6a37fbbf7de37',
                        'TGLExt/O16/RotationGeneratorBridges.lean': 'f7d31563b28f46ad8692f81b3a0350ff933135c3e53bbfd575a3bf6c5bf9969e',
                        'TGLExt/O16/SameSquareDomain.lean': 'f7905732198f8fced3e152ca72fa826f79a15a2360f52ac85b8dafe6a63d66a7',
                        'TGLExt/O16/ScalarGraphRealization_v3.lean': '28cf074ae4982703f857eaf51a4cb6dbceaa7a9c038230f4364b18a7be88b0fb',
                        'TGLExt/O16/ScreenMetricAlgebra_v3.lean': '5b1bd3fb6c8398837abb263e6152cdc313189e7a93c815d6d71a7b504e6515b6',
                        'TGLExt/O16/SelfadjointAbsoluteRoot.lean': '526b03793805f2de50310d34931284e76da5905a43b1b7f1da4cb5cfb15429f8',
                        'TGLExt/O16/SelfadjointSquareResolvent.lean': '6c53396c2fafe86d8b51392380dba56f5cef6a1e83a7cc522a48fcb25b692c53',
                        'TGLExt/O16/StressTensorDataLocal_v2.lean': 'ae85f18f510d922ceed5c8f9c66e5e45ebf81731d35f4caff0c7a920e814a14b',
                        'TGLExt/O16/StrictCocycleGauge.lean': '8b3d0b539eb2d5b02afcf587cb7b5734e4d00e9313c6a1a47371c363a8d09787',
                        'TGLExt/O16/TeleologicalBoundary_v2.lean': '8b5cb45c04704400dcea638323789d674b3001a0d37ec7b6bb09883bc39df04b',
                        'TGLExt/O16/TeleologicalContractBridge_v3.lean': '6e3c0463de91260733a7d06cf5644aa925dac76bc3bab5ce987d0ff92ec8c6d5',
                        'TGLExt/O16/TeleologicalMatrix_v3.lean': '8357ab67b3ada84023673dd0877d620823db3786098e555bf522b3a1bc2ecc98',
                        'TGLExt/O16/TeleologicalNullSolution_v2.lean': '957f59b5a4598f4c11923a1f7f7400d1739b1d021b9dfbd90c9081df7e65e383',
                        'TGLExt/O16/TeleologicalShift_v3.lean': 'e9f4ccabbdd85c87f3c47a386f44db47af3960220692115c34a4f6605d8ac5ed',
                        'TGLExt/O16/TeleologicalTail_v3.lean': '85a5bfd49bb53e9b9e6ac6355faee51b660403b1ee761b57bc0857c7ce485dc3',
                        'TGLExt/O16/TeleologicalUniqueness.lean': '69bf940a73c5a143deb2fd18c8617cca64f4ff44d1d39d5a41a0f85ba715bb29',
                        'TGLExt/O16/TheEquationOfTruth_T20_controles_v3_Integration_v2.lean': '0cbab4cc198277d2eb745678b5b7f65abc1f07b6467a51bd6413b7b0942cd2f9',
                        'TGLExt/O16/TheEquationOfTruth_T20_v3.lean': 'e9252d1753bcf7c53effec60cab86d9b2126fb224fcb919e0d6c2fa374ccd448',
                        'TGLExt/O16/TraceInfinityExtension_v3.lean': '43903aed48bd4499ccc116b090a8764049eb5cf70a84a41833730e30b2ec7cab',
                        'TGLExt/O16/TransverseCocycle_v3.lean': '55505153603233a0e8c4dfd4e14a1f368807481b9e040a7d26f90c47bc532a1d',
                        'TGLExt/O16/UVScope016_v3.lean': '40bdbd644d22e77caf54b387d0c52be56305064dd7a7f6d98542a684cd0d2b02',
                        'TGLExt/O16/UnboundedGraphTransform_v2.lean': '74fbd73fa6d77a2831a9e5e03153da6a572b8ec249aaa5b4977b25afdd66b547',
                        'TGLExt/O16/UnboundedTransformConstruction_v2.lean': '027170a6140e674c6fb09421051a3b0a3f61866b32f5442aa59af8cacaabd98d',
                        'TGLExt/O16/UnboundedTransformEnergy.lean': 'd8f19ed116adcd26ceabc8f6424ef926d543fa19a66ac0819da6c909dbb82431',
                        'TGLExt/O16/UnboundedTransformKernelGap_v3.lean': 'e675ff0f76c9177fc4007394e84adaa1afed590d56a8bdc7888162684b64494b',
                        'TGLExt/O16/UnboundedTransformProjectionControl.lean': '1dc818e07b992fffa6bedfbc23745fea749eeebb13157603ddacc475f6507172',
                        'TGLExt/O16/UnitMultiplierIdentity.lean': '0e8142c3fd467abfe56763d66f1222eb868add353f328c316fdfa8f2be551bb3',
                        'TGLExt/O16/VectorRapiditySpectrum.lean': 'ebb3d1a4f75546740e67975fb81d3afae745fb749cc1daa3c511dbd04639b65a',
                        'TGLExt/O16/WedgeDraggedFrame_v6.lean': '34059cd505b0991afcd7527eadeff47efeb04c07afc8b15cd85aab7377e36907',
                        'TGLExt/O16/WeightControls_v2.lean': '975fb0358c8862218ebe82abfdfcf4ef9aeab53c26ddfa97e709d62cbc03d4fa',
                        'TGLExt/O16/WickBoostRotation_v2.lean': '61f7d0b275edb64725420037bdcc6bc43bdd592cad28dd14b0154181142cf48a',
                        'TGLExt/O16/WidthFromContraction_v2.lean': 'd1531e72ac4656b02c264ab374d3c3e93083606bf8b1202b633e1c1beab0acfa',
                        'TGLExt/O16/WindowCoefficientVerbatim.lean': 'b23e1b27c38277d05cdade74f6155b60bea6bcbcd815c739e4a8e2dd652a0e7e',
                        'TGLExt/O16/WindowLemmasVerbatim.lean': 'aee9c09c5103d0226a151f7fe04e4d378c6c7d84ded9ed712073ef46b3af7f7a'},
              'estatuto': '[REAL]'},
             {'id': 'h9',
              'descricao': 'medida do Audit v405: duracao bem abaixo do timeout de 1800 s',
              'onde': 'fonte:kh_n1_v405',
              'caminho': ['duracao_audit_s'],
              'op': 'menor_igual',
              'valor': 900,
              'capturar': 'duracao_do_audit_s',
              'estatuto': '[REAL]'},
             {'id': 'h10',
              'descricao': 'medida do Audit v405: sorryAx ausente do log',
              'onde': 'fonte:kh_n1_v405',
              'caminho': ['sorryAx_no_log_do_audit'],
              'op': 'igual',
              'valor': 0,
              'estatuto': '[REAL]'},
             {'id': 'h11',
              'descricao': 'medida do Audit v405: as entradas novas estao no trio',
              'onde': 'fonte:kh_n1_v405',
              'caminho': ['novas_no_trio'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'},
             {'id': 'h12',
              'descricao': 'a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report',
              'onde': 'kf',
              'caminho': ['declaration_sources_status_v394', 'ok'],
              'op': 'verdadeiro',
              'estatuto': '[REAL]'}],
  'erratas': [{'ao_lado_de': 'kh_n1_cobertura_v404 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)',
               'dizia': 'A v404 cobrava constantes == 29484, teoremas == 23430, um axiom_report de exatamente o tamanho da v404 e o hash formal igual ao pino '
                        'exato da arvore da v404.',
               'agora': 'A v405 acrescenta os oito modulos (a cobertura cresce e a arvore ganha os arquivos das pedras): na v405 o registro da v404 passa a '
                        'cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O '
                        'veredito do registro da v404 NAO muda.',
               'lacuna_de_fidelidade': 'a estrutura da v404 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito '
                                       'deixou o registro preso a igualdades que a propria v405 quebra (a mesma lacuna que a v404 achou no registro da v403, e '
                                       'assim por diante desde a v399)',
               'estatuto': '[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]',
               'assinatura': 'gerencia c1, em nome proprio, 01/11/2026'}],
  'limites': ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
              '[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v404): as 113 auxiliares geradas pelo compilador nos '
              'modulos das pedras ficam cobertas pelo KH-N1 mas sem bandeira, e as 368 nomeadas publicas ganharam bandeira',
              "validade no kernel nao e' creditacao; o gate nao se move"],
  'diz': ['a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v405 (os oito modulos novos) e segue sem constante fora do trio, sem nome '
          'ilegivel'],
  'nao_diz': ['que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido'],
  'leituras_do_operador': [],
  'extras': {'assinatura': 'gerencia c1, em nome proprio, 01/11/2026',
             'n_bandeiras': 368,
             'h8_entradas': 1446,
             'h8_residuais_do_nos': ['_check_damming.lean']}}]
_V405_NOMES_REGISTROS = ['cunhagens_v405', 'campos_fechados_e_leituras_v405', 'ga_reclassificacao_v405', 'gap_v405', 'kh_n1_cobertura_v405']
_V405_REGISTROS_FUNCAO = ['ponte_da_massa_v405', 'massa_tensao_pura_v405', 'identidade_v405', 'observador_terminal_v405', 'lei_do_diminuto_v405', 'tonica_do_hamiltoniano_v405', 'disco_de_euler_v405', 'ponto_zero_do_psion_v405']
_V392_FONTES.update(_V405_FONTES)   # v405: o motor de registros (v392) le as fontes e os verbatins das treze versoes
_V392_VERBATINS2.update(_V405_VERBATINS2)


def _v405_rodar_specs(core_):
    """v405 -- roda os registros por spec da v405 (o MOTOR e' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Os oito registros com funcao NAO entram aqui: rodam no main, depois dos tres da v404."""
    for spec_ in _V405_SPECS:
        try:
            r_ = _v392_registro(spec_, core_)
            core_[spec_["nome"]] = _v405_ga_registro(r_, core_, spec_) if spec_["nome"] == "ga_reclassificacao_v405" else (_v405_gap_registro(r_, core_, spec_) if spec_["nome"] == "gap_v405" else r_)
        except Exception as e_:   # noqa: BLE001
            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}
    return [s_["nome"] for s_ in _V405_SPECS]
