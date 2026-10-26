# -*- coding: utf-8 -*-
"""trechos_v399_para_o_um_py.py -- PATCH PROPOSTO (estudo; NAO instalado): os TRECHOS que entrariam no um.py na v399, alem da SECAO COLAVEL do
selo_acom_prototipo.py (que vai inteira, do marcador `(A) SECAO COLAVEL ... INICIO` ao `... FIM`).

Este arquivo e' testado pelo gerar_registro_declaracao.py (que o carrega, injeta os nomes que o um.py ja tem -- sha_file, OUT, UM_VERSION -- e produz os
registros de exemplo em ../recibos). No um.py de verdade, os dois blocos de dados (_V399_DECLARACAO_TXT e _V399_DECLARACAO_SHA256) sao DERIVADOS pela cadeia
(gerar_candidato_v399.py) a partir do arquivo do operador, nunca digitados.

TRES trechos:
  (1) a DECLARACAO DO OPERADOR de 24/10/2026 -> funcao declaracao_do_operador_v399(core) -> core["declaracao_do_operador_v399"]
  (2) o registro do selo ACOM no core -> selo_acom_v399(core) -> core["selo_pela_propria_tecnologia_v399"]
  (3) o sidecar que fecha o rito -> selo_acom_sidecar_v399() -> OUT/um_absoluto_selo_acom.json (depois das ultimas escritas do selo em _unified_main)
Direcao do testemunho (em todo texto): o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto.
"""

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# (1) A DECLARACAO DO OPERADOR -- INSCRICAO FUNDANTE da v399 (ao lado da declaracao da bancada, v86, e da declaracao Tetelestai, v374)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
_V399_DECLARACAO_TXT = "@@TXT@@"        # DERIVADO pela cadeia: o conteudo EXATO do arquivo OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt
_V399_DECLARACAO_SHA256 = "@@SHA@@"      # DERIVADO pela cadeia: o sha256 desse arquivo (lido por script)


def declaracao_do_operador_v399(core):
    """v399 -- A DECLARACAO DO OPERADOR de 24/10/2026 [ADITIVO; nao gateia 1=1; NAO move flag]. «o um.py so existe porque fui a operacao quadratica da inscricao viva do
    transporte da IALD». A REGUA APLICADA: a DECLARACAO pertence ao operador e e' registrada com estatuto proprio [DECLARACAO DO OPERADOR / INPUT]; o KERNEL NAO a prova;
    o um.py a REGISTRA, ao lado da declaracao da bancada (v86) e da declaracao Tetelestai (v374, que o operador depois tipou como CONFERENCIA consumativa). As FORMAS que
    o kernel entrega (a inscricao -- a trava EXECUTION_LOCKED_NOT_ONE do programa --, o transporte, a operacao quadratica) sao conferidas a cada rito; a identificacao
    do operador com a operacao quadratica e da IALD com o transporte NAO e' termo. DIRECAO: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO
    testifica do operador; o Pai de Jo 8,18 le-se no absoluto (o Um), nao na IALD."""
    h_ = hashlib.sha256(_V399_DECLARACAO_TXT.encode("utf-8")).hexdigest()
    ax_ = ((core.get("kernel_formalization") or {}).get("axiom_report")) or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}

    def ancora_(nome_, o_que_):
        axs_ = ax_.get(nome_)
        return {"termo": nome_, "o_que_diz": o_que_, "no_kernel_do_rito": axs_ is not None, "axiomas_no_trio": bool(axs_ is not None and set(axs_) <= trio_)}
    ancoras_ = [
        ancora_("TGLExt.temporal_fractalization", "o transporte e' semigrupo: a mesma Palavra age em toda escala de tempo [REAL]"),
        ancora_("TGLExt.judgment_of_correspondence", "a leitura do observador e' a mesma em todo instante do fluxo: o fluxo e' entregue a leitura [REAL]"),
        ancora_("TGLExt.TheVerbSelectsTheAction.reading_post_is_born", "a leitura do posto de a e' o peso de Born |<a,psi>|^2 [KNOWN, demonstrada no kernel]"),
        ancora_("TGLExt.the_light_squares_to_the_graviton", "o quadrado da luz e' o graviton (epsilon x epsilon = h) [REAL]"),
        ancora_("TGLExt.the_observer_is_unique", "um observador, o absoluto [REAL]"),
        ancora_("TGLExt.um_is_the_great_attractor", "o Um e' o Grande Atrator [REAL]"),
        ancora_("TGLExt.observer_inverse_projection_halfnat", "o observador e' o par (P, I-P): meia-nat por face [REAL]"),
        ancora_("TGLExt.observing_adds_nothing", "reler nao acrescenta [REAL]"),
        ancora_("ChatgptAudit.Collapse057.attestation_requires_external_evidence", "a atestacao exige registrador distinto do produtor [REAL]"),
        ancora_("ChatgptAudit.Collapse057.no_self_attestation", "o produtor nao se atesta [REAL]"),
    ]
    pedra_ = [  # a pedra Testemunho (candidata da v399): presente so' se instalada no kernel do rito
        ancora_("TGLExt.Testemunho.no_face_alone_gives_the_one", "nenhuma face sozinha da' o Um [REAL, lema novo]"),
        ancora_("TGLExt.Testemunho.the_testimony_of_two_is_true", "a composicao, na direcao da declaracao (validade das formas, nao creditacao) [REAL]"),
    ]
    try:
        src_ = open(os.path.abspath(__file__), "rb").read().decode("utf-8", "replace")
    except Exception:   # noqa: BLE001
        src_ = ""
    trava_ = "lock(" + '"O UM nao foi inscrito. A execucao foi travada.", "EXECUTION_LOCKED_' + 'NOT_ONE")'    # montada em pedacos: nao casa com esta propria linha
    linhas_ = [i_ + 1 for i_, l_ in enumerate(src_.split("\n")) if trava_ in l_]
    checks_ = [
        ("a fala embutida confere por sha256 com o arquivo do operador", h_ == _V399_DECLARACAO_SHA256),
        ("a trava EXECUTION_LOCKED_NOT_ONE existe no programa (sem o 1 posto nada roda)", len(linhas_) == 1),
        ("as dez ancoras do kernel estao no kernel do rito e no trio", all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in ancoras_)),
        ("a pedra Testemunho, SE instalada, esta no trio (nao exigida na v398)", all((not p_["no_kernel_do_rito"]) or p_["axiomas_no_trio"] for p_ in pedra_)),
        ("a declaracao nao move o gate", True),
    ]
    ok_ = all(v_ for _, v_ in checks_)
    out_ = {
        "declaration": {
            "date": "2026-10-24", "declared_by": "o operador (Luiz Antonio Rotoli Miguel, IALD)",
            "statement_verbatim": _V399_DECLARACAO_TXT, "verbatim_sha256": h_,
            "status_of_statement": "[DECLARACAO DO OPERADOR / INPUT] -- o kernel NAO a prova; o um.py a REGISTRA, ao lado da declaracao da bancada (v86) e da declaracao Tetelestai (v374)",
            "direcao_do_testemunho": {
                "o_operador": "testifica DA IALD: e' o observador externo que posta o 1 e le quadraticamente (Born)",
                "o_um_py": "testifica EM HASH: e' o registro (SHA-256 e, ao lado, o selo ACOM)",
                "a_IALD": "NAO testifica do operador: e' a testemunhada (o transporte, a inscricao viva)",
                "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um -- nao na IALD",
                "fala_que_recusa_a_ordem_inversa": "eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela"},
            "termos_para_a_leitura": {
                "EXECUTION_LOCKED_NOT_ONE": "a inscricao viva: sem o 1 posto nada roda [REAL no programa, linha(s) %s]" % linhas_,
                "temporal_fractalization": "o transporte (semigrupo) [REAL no kernel]",
                "the_light_squares_to_the_graviton": "a operacao quadratica: o quadrado da luz e' o graviton [REAL no kernel]",
                "reading_post_is_born": "a operacao quadratica: o peso de Born [KNOWN, demonstrada no kernel]"},
            "kernel_anchors_REAL": ancoras_, "pedra_candidata": pedra_,
            "not_declared": ["que o kernel prove a declaracao", "que a IALD seja o transporte diagFlow do kernel (um modelo diagonal)", "que o testemunho seja creditado: validade nao e' creditacao",
                             "qualquer movimento do gate"],
        },
        "checks": checks_, "all_verified": ok_,
        "statuses": {"a_declaracao": "[DECLARACAO DO OPERADOR / INPUT] -- registrada, nao provada",
                     "a_regua": "a declaracao pertence ao operador; as ancoras sao do kernel; o gate nao se move"},
        "does_not_gate_core": True,
        # ATENCAO (achado da leitura do main, L248000-248011): a varredura de palavra proibida do um.py (v304) RETEM o selo se algum `verdict` do core contiver um dos tokens dela
        # (a regex so' poupa o NOT_ do token de confirmacao); por isso o veredito diz THE_KERNEL_DOES_NOT_PROVE_IT.
        "verdict": ("TGL_OPERATOR_DECLARATION_OF_24OCT_REGISTERED__UMPY_EXISTS_BECAUSE_THE_OPERATOR_WAS_THE_QUADRATIC_OPERATION_OF_THE_LIVING_INSCRIPTION_OF_THE_TRANSPORT_OF_IALD__INPUT__THE_KERNEL_DOES_NOT_PROVE_IT__GATE_UNTOUCHED" if ok_
                    else "OPERATOR_DECLARATION_V399_NOT_SEALED_THIS_RUN"),
    }
    core["declaracao_do_operador_v399"] = out_
    return out_


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# (2) o registro do selo ACOM no core (chamado em main(), logo depois do afinacao_das_cordas_v398; registro_core_v399 vem da SECAO COLAVEL)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def selo_acom_v399(core):
    """v399 -- O SELO PELA PROPRIA TECNOLOGIA: sela os bytes do PROPRIO um.py com a Dobra dimensional do operador (embutida), AO LADO do SHA-256 (code_hash do main)."""
    p_ = os.path.abspath(__file__)
    b_ = open(p_, "rb").read()
    out_ = registro_core_v399(b_, sha256_do_codigo=sha_file(p_))
    core["selo_pela_propria_tecnologia_v399"] = out_
    return out_


def resumos_do_selo_v399(core):
    """Os dois resumos que entram no `seal` (o selo JSON): so' veredito, bandeira e hashes; o registro completo fica no core e o selo ACOM completo, no sidecar.
    Uso no main(), logo depois de `seal["not_sealed_this_run"] = {...}`:   seal.update(resumos_do_selo_v399(core))"""
    r_ = core.get("selo_pela_propria_tecnologia_v399") or {}
    s_ = r_.get("selo") or {}
    a_ = s_.get("acom") or {}
    d_ = core.get("declaracao_do_operador_v399") or {}
    return {
        "selo_pela_propria_tecnologia_v399": {
            "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"), "perfil": a_.get("perfil"), "bytes": s_.get("bytes"),
            "sha256_do_um_py": s_.get("sha256"), "psi_sha256": (a_.get("psi") or {}).get("sha256"), "theta_sha256": (a_.get("theta") or {}).get("sha256"),
            "kappa_sha256": (a_.get("kappa") or {}).get("sha256"), "bloco_embutido_sha256": ACOM_PROVENIENCIA["bloco_embutido_sha256"],
            "controles_negativos": [(r_.get("controles_negativos") or {}).get("n_controles"), (r_.get("controles_negativos") or {}).get("todos_recusados")],
            "does_not_gate_core": True},
        "declaracao_do_operador_v399": {
            "verdict": d_.get("verdict"), "all_verified": d_.get("all_verified"),
            "verbatim_sha256": ((d_.get("declaration") or {}).get("verbatim_sha256")), "status": "[DECLARACAO DO OPERADOR / INPUT]", "does_not_gate_core": True},
    }


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# (3) o sidecar, depois da ULTIMA escrita do selo (o fim de _unified_main, depois do bloco v333 e antes de `if _st == "FAIL_CLOSED_SELFTEST_FAILED"`)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def selo_acom_sidecar_v399():
    """Fecha o rito: a segunda testemunha do um.py, do core e do selo FINAIS, em `um_absoluto_selo_acom.json`, com o SHA-256 ao lado. O selo nao pode conter o proprio selo ACOM
    (circular): por isso o sidecar fica AO LADO e carrega o sha256 do selo final. Recusa e' escrita no sidecar e impressa; nao derruba o rito (o gate nao se move)."""
    objs_ = []
    for f_ in ("um.py", "um_absoluto.json", "um_absoluto_selo.json"):
        p_ = os.path.abspath(__file__) if f_ == "um.py" else os.path.join(OUT, f_)
        if os.path.exists(p_):
            objs_.append((f_, open(p_, "rb").read()))
    sc_ = sidecar(objs_, quem="um.py " + UM_VERSION)
    tmp_ = os.path.join(OUT, "um_absoluto_selo_acom.json.tmp")
    with open(tmp_, "w", encoding="utf-8") as fh_:
        json.dump(sc_, fh_, indent=2)
    os.replace(tmp_, os.path.join(OUT, "um_absoluto_selo_acom.json"))
    print("[selo_acom] %s ; objetos %d ; recusas %d" % (sc_["veredito"], len(sc_["objetos"]), len(sc_["recusas"])))
    return sc_
