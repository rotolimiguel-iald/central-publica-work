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
