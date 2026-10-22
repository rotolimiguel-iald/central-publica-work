# -*- coding: utf-8 -*-
"""Aplica os achados do aferidor da v379 (B1-B3; C1, C6, C7, C9) ao runtime, ao gerador, aos esperados, ao conferidor, ao leitor, aos textos, ao handoff,
ao registrar e aos parágrafos do artigo. Substituições exatas (count == 1). A pedra já foi editada à parte."""
import io, os, ast, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def edit(path, pairs):
    t = io.open(path, encoding="utf-8", newline="").read()
    for a, b in pairs:
        assert t.count(a) == 1, (os.path.basename(path), t.count(a), a[:90]); t = t.replace(a, b)
    io.open(path + ".tmp", "w", encoding="utf-8", newline="").write(t); os.replace(path + ".tmp", path); print("ok", os.path.basename(path))


# ---- runtime
edit(os.path.join(SP, "v379", "v379_runtime.py"), [
    ('    "ext_ter_the_name_collision_kernel_proved", "ext_ter_existence_is_the_asymptote_kernel_proved", "ext_ter_existence_forbids_full_static_witness_kernel_proved",\n    "ext_ter_the_elementary_reason_kernel_proved")',
     '    "ext_ter_the_name_collision_kernel_proved", "ext_ter_existence_is_the_asymptote_kernel_proved", "ext_ter_existence_forbids_full_static_witness_kernel_proved",\n    "ext_ter_erasure_not_reached_in_finite_time_kernel_proved", "ext_ter_the_elementary_reason_kernel_proved")'),
    ('def _v379_own_source_has(s):\n    try:\n        with open(os.path.abspath(__file__), "rb") as fh:\n            return s.encode("utf-8") in fh.read()\n    except Exception:\n        return False\n',
     'def _v379_own_source_matches(pattern):\n    """v379 (aferidor B3): le ESTE arquivo do disco e procura o padrao ANCORADO EM LINHA (re.M) -- a linha desta propria conferencia, que so cita o\n    literal dentro de uma string, NAO casa; so a atribuicao real casa. Falha de leitura => False (nunca «ok» falso)."""\n    try:\n        with open(os.path.abspath(__file__), "rb") as fh:\n            return re.search(pattern, fh.read().decode("utf-8", "replace"), re.M) is not None\n    except Exception:\n        return False\n'),
    ("(beta_forbids_full_static_witness); o reconhecimento e finito POR DEFINICAO do regime (IALDState.recursive). O «limite assintotico em tempo finito» do\n    operador le-se: a assintota e E = beta, nao atingida em tempo finito; o que e finito e o reconhecimento. RUNTIME: existence = beta do core a 1e-9\n    relativo (o core le beta como sqrt(e)/R_boundary, nunca literal);",
     "(beta_forbids_full_static_witness); o APAGAMENTO nao se atinge em tempo finito (erasure_not_reached_in_finite_time: 0 < e^{-t.E.c} < 1, por\n    leakage_strictly_loses); o reconhecimento e finito POR DEFINICAO do regime (IALDState.recursive; teorema trivial, a projecao do campo). O «limite\n    assintotico em tempo finito» do operador le-se (aferidor v379, B2): E = beta e a assintota do custo por nat, NAO EXCEDIDA em registro finito com\n    int g <= N (beta.g_medio <= E; igualdade no D1a, g = 1; abaixo no FRW medido, g_medio = 0,958); o que nao se atinge em tempo finito e o APAGAMENTO;\n    o que e finito e o reconhecimento. RUNTIME: existence = beta do core a 1e-9 relativo (o core calcula beta = sqrt(e).alpha_obs pelo motor de Lagrange,\n    nunca literal);"),
    ('    per_nat_v378 = d8.get("per_nat_cost_D1b"); gbar = d8.get("predicted_deviation_over_beta_D1b")\n    x_fixed = 0.5',
     '    per_nat_v378 = d8.get("per_nat_cost_D1b"); gbar = d8.get("predicted_deviation_over_beta_D1b")\n    erasure_1 = math.exp(-(1.0 * existence * 1.0))   # t = 1, c = 1: o peso sobrevivente, estritamente entre 0 e 1\n    x_fixed = 0.5'),
    ('        ("RUNTIME: E = C x I x K = e^{1/2} x 1 x alpha (%.12f) = beta do core (%.12f) a 1e-9 relativo (beta nunca literal)" % (existence, beta),',
     '        ("RUNTIME: E = C x I x K = e^{1/2} x 1 x alpha (%.12f) = beta do core (%.12f) a 1e-9 relativo (o core: beta = sqrt(e).alpha_obs, motor de Lagrange; nunca literal)" % (existence, beta),'),
    ('        ("RUNTIME: a Razao Elementar ao quadrado e a existencia: (e^{1/4} sqrt(alpha))^2 = %.12f = E a 1e-15 relativo" % (reason * reason), abs(reason * reason / existence - 1.0) < 1e-15),',
     '        ("RUNTIME: a Razao Elementar ao quadrado e a existencia: (e^{1/4} sqrt(alpha))^2 = %.12f = E a 1e-14 relativo (medido ~3e-16; aferidor C6/C9: tolerancia e guarda)" % (reason * reason),\n         alpha > 0 and existence > 0 and abs(reason * reason / existence - 1.0) < 1e-14),'),
    ('        ("RUNTIME: E e a ASSINTOTA -- o custo por nat da v378 no registro ate z* (%s) <= E = %.6f (a diferenca e o desvio previsto delta/beta = %s)" % (per_nat_v378, existence, gbar),\n         per_nat_v378 is not None and float(per_nat_v378) <= existence and gbar is not None and float(gbar) <= 0.0),\n        ("RUNTIME: o amp_bridge do um.py e a mesma expressao e^{1/4} sqrt(alpha) (lido da fonte deste arquivo)", _v379_own_source_has("amp_bridge = math.exp(0.25) * math.sqrt(alpha)")),',
     '        ("RUNTIME: E e a ASSINTOTA, NAO EXCEDIDA -- o custo por nat da v378 no registro ate z* (%s; g_medio = 0,958 <= 1) <= E = %.6f (a diferenca e o desvio previsto delta/beta = %s)" % (per_nat_v378, existence, gbar),\n         per_nat_v378 is not None and float(per_nat_v378) <= existence and gbar is not None and float(gbar) <= 0.0),\n        ("RUNTIME: o APAGAMENTO nao se atinge em tempo finito: e^{-(1.E.1)} = %.9f esta estritamente entre 0 e 1" % erasure_1, 0.0 < erasure_1 < 1.0),\n        ("RUNTIME: o amp_bridge do um.py e a mesma expressao e^{1/4} sqrt(alpha) -- lido da fonte deste arquivo por regex ANCORADA EM LINHA (a propria conferencia nao casa; aferidor B3)",\n         _v379_own_source_matches(r"^\\s*amp_bridge = math\\.exp\\(0\\.25\\) \\* math\\.sqrt\\(alpha\\)\\s*$")),'),
    ('        ("E e a ASSINTOTA (existence_is_the_asymptote usa the_deviation_reads_below_the_asymptote); sem testemunha estatica plena (existence_forbids_full_static_witness usa beta_forbids_full_static_witness)",\n         "theorem existence_is_the_asymptote" in src and "the_deviation_reads_below_the_asymptote" in src and "theorem existence_forbids_full_static_witness" in src and "beta_forbids_full_static_witness" in src),',
     '        ("E e a ASSINTOTA sob int g <= N (existence_is_the_asymptote usa the_deviation_reads_below_the_asymptote com hI); sem testemunha estatica plena (existence_forbids_full_static_witness usa beta_forbids_full_static_witness); o APAGAMENTO nao se atinge em tempo finito (erasure_not_reached_in_finite_time usa leakage_strictly_loses)",\n         "theorem existence_is_the_asymptote" in src and "the_deviation_reads_below_the_asymptote" in src and "(hI : accumulatedContrast g N ≤ N)" in src and "theorem existence_forbids_full_static_witness" in src\n         and "beta_forbids_full_static_witness" in src and "theorem erasure_not_reached_in_finite_time" in src and "leakage_strictly_loses" in src),'),
    ('        ("TUDO NUM SO TERMO: the_elementary_reason (oito clausulas)", "theorem the_elementary_reason" in src and "existence α ≠ familyFunctional (1 / 2)" in src),',
     '        ("TUDO NUM SO TERMO: the_elementary_reason (nove clausulas)", "theorem the_elementary_reason" in src and "existence α ≠ familyFunctional (1 / 2) ∧" in src and "(ix) o apagamento" in src),\n        ("A MESMA guarda do rito sobre o estatuto e a clausula do tempo finito deste modulo: nenhuma palavra proibida (aferidor C1)",\n         not any(_V379_GUARDA.search(s_) for s_ in (_V379_FINITE_CLAUSE, _V379_STATUTE))),'),
    ('            "finite_time_clause": ("[CORRIGIDO, como a IALD cindiu e a gerencia aferiu] «limite assintotico em tempo finito» = a assintota e E = beta (the_deviation_reads_below_the_asymptote; "\n                                   "beta_forbids_full_static_witness); o que e finito e o RECONHECIMENTO (IALDState.recursive, idempotente por definicao); o zero absoluto nao se toca"),\n            "statute": ("fatoracao E = sqrt(e).1.alpha = beta e positividade PROVADAS por termo (kernel); o dicionario dos fatores e [ONTO/DEFINITION], cunhagem do operador; "\n                        "«estrutura fundamental da existencia» e [ONTO/CONJ]; «Razao Elementar» e nome do operador [INPUT]; nada confirma: PROVADA != CONFIRMADA"),',
     '            "finite_time_clause": _V379_FINITE_CLAUSE,\n            "statute": _V379_STATUTE,'),
    ('            "asymptote_beside_v378": {"per_nat_cost_D1b": per_nat_v378, "predicted_deviation_over_beta": gbar, "reading": "todo registro finito le beta.g_medio <= E = beta; a assintota nao se atinge em tempo finito; o reconhecimento e finito por definicao"},',
     '            "asymptote_beside_v378": {"per_nat_cost_D1b": per_nat_v378, "predicted_deviation_over_beta": gbar, "erasure_weight_t1_c1": erasure_1,\n                                      "reading": "todo registro finito com int g <= N le beta.g_medio <= E = beta (igualdade no D1a; abaixo no FRW medido); o apagamento nao se atinge em tempo finito; o reconhecimento e finito por definicao"},'),
    ('                                "IDENTITY_WEIGHS_ONE_AS_THE_NAME__ELEMENTARY_REASON_SQUARED_EQ_EXISTENCE__EXISTENCE_IS_THE_ASYMPTOTE_FINITE_REGISTER_READS_BELOW__NO_FULL_STATIC_WITNESS__"',
     '                                "IDENTITY_WEIGHS_ONE_AS_THE_NAME__ELEMENTARY_REASON_SQUARED_EQ_EXISTENCE__EXISTENCE_IS_THE_ASYMPTOTE_NOT_EXCEEDED_IN_FINITE_REGISTER_WITH_MEAN_CONTRAST_LE_ONE__"\n                                "ERASURE_NOT_REACHED_IN_FINITE_TIME__NO_FULL_STATIC_WITNESS__"'),
    ('_V379_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")\n',
     '_V379_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")\n'
     '_V379_FINITE_CLAUSE = ("[CORRIGIDO, como a IALD cindiu e os aferidores da v378/v379 pediram] «limite assintotico em tempo finito» = E = beta e a assintota do custo por nat, NAO EXCEDIDA em "\n'
     '                       "registro finito com int g <= N (the_deviation_reads_below_the_asymptote; igualdade no D1a, g = 1; abaixo no FRW medido); o que NAO se atinge em tempo finito e o "\n'
     '                       "APAGAMENTO (erasure_not_reached_in_finite_time: 0 < e^{-t.E.c} < 1; beta_forbids_full_static_witness); o que e finito e o RECONHECIMENTO (IALDState.recursive, "\n'
     '                       "idempotente por definicao do regime)")\n'
     '_V379_STATUTE = ("fatoracao E = sqrt(e).1.alpha = beta e positividade PROVADAS por termo (kernel); o dicionario dos fatores e [ONTO/DEFINITION], cunhagem do operador; "\n'
     '                 "«estrutura fundamental da existencia» e [ONTO/CONJ]; «Razao Elementar» e nome do operador [INPUT]; nada confirma: PROVADA != CONFIRMADA")\n'),
])
# ---- gerador: a bandeira nova + o token do selo
edit(os.path.join(SP, "v379", "gerar_candidato_v379.py"), [
    ('       "ext_ter_the_name_collision_kernel_proved", "ext_ter_existence_is_the_asymptote_kernel_proved", "ext_ter_existence_forbids_full_static_witness_kernel_proved",\n       "ext_ter_the_elementary_reason_kernel_proved"]',
     '       "ext_ter_the_name_collision_kernel_proved", "ext_ter_existence_is_the_asymptote_kernel_proved", "ext_ter_existence_forbids_full_static_witness_kernel_proved",\n       "ext_ter_erasure_not_reached_in_finite_time_kernel_proved", "ext_ter_the_elementary_reason_kernel_proved"]'),
    ("assert len(FLAGS) == 22 and len({f for f, _ in FLAGS}) == 22", "assert len(FLAGS) == 23 and len({f for f, _ in FLAGS}) == 23"),
    ('"_LEAN_THEOREM_FLAGS: +22 (ext_ter_).")', '"_LEAN_THEOREM_FLAGS: +23 (ext_ter_).")'),
    ('"external_ladder: +22 (5919 -> 5941).")', '"external_ladder: +23 (5919 -> 5942).")'),
    ("    # v379 (01/10/2026, a Razao Elementar: E = C x I x K > 0 = beta, tipada): ter (22)", "    # v379 (01/10/2026, a Razao Elementar: E = C x I x K > 0 = beta, tipada): ter (23)"),
    ('        # v379: a Razao Elementar (22)', '        # v379: a Razao Elementar (23)'),
    ("'TYPED_TheElementaryReason_BY_TERM__DICTIONARY_IS_ONTO_DEFINITION_COINAGE__THE_ASYMPTOTE_IS_E_EQ_BETA_NOT_ATTAINED_IN_FINITE_TIME__RECOGNITION_FINITE_BY_DEFINITION_OF_THE_REGIME__'",
     "'TYPED_TheElementaryReason_BY_TERM__DICTIONARY_IS_ONTO_DEFINITION_COINAGE__THE_ASYMPTOTE_E_EQ_BETA_NOT_EXCEEDED_IN_FINITE_REGISTER__ERASURE_NOT_REACHED_IN_FINITE_TIME__RECOGNITION_FINITE_BY_DEFINITION_OF_THE_REGIME__'"),
])
edit(os.path.join(SP, "v379", "gerar_esperados_v379.py"), [
    ('sbx["bandeiras_ok"] == len(sbx["bandeiras"]) == 22', 'sbx["bandeiras_ok"] == len(sbx["bandeiras"]) == 23'),
    ('"KERNEL_22_OF_22"', '"KERNEL_23_OF_23"'),
])
edit(os.path.join(SP, "v379", "conferir_rito_v379.py"), [
    ('all(kf.get(f) is True for f in FL) and len(FL) == 22', 'all(kf.get(f) is True for f in FL) and len(FL) == 23'),
    ('"as 22 declaracoes novas no axiom_report', '"as 23 declaracoes novas no axiom_report'),
])
edit(os.path.join(SP, "v379_selo", "leitura_v379.py"), [("if V['n_flags_on'] != len(FL) or len(FL) != 22:", "if V['n_flags_on'] != len(FL) or len(FL) != 23:")])
# ---- artigo PT/EN (B1, B2)
edit(os.path.join(SP, "v379", "artigo_pt_v379.pysnip"), [
    (r"\textbf{$E$ é a assíntota}: todo registro finito lê $\bTGL\,\bar g\le E$ (a v378) e não há testemunha estática plena (\texttt{beta\_forbids\_full\_static\_witness}). ",
     r"\textbf{$E$ é a assíntota}: todo registro finito com $\int_0^N g\le N$ ($\bar g\le1$; medido $\bar g=0{,}958$ até $z_*$) lê $\bTGL\,\bar g\le E$, com igualdade no D1a ($g\equiv1$; a v378); o apagamento não se atinge em tempo finito, $0<e^{-tEc}<1$ (\texttt{erasure\_not\_reached\_in\_finite\_time}); e não há testemunha estática plena (\texttt{beta\_forbids\_full\_static\_witness}). "),
    (r"O ``limite assintótico em tempo finito'' lê-se, pois, como a IALD cindiu e a gerência aferiu: a assíntota é $E=\bTGL$ e não se atinge em tempo finito; o que é finito é o \emph{reconhecimento}, idempotente por definição do regime (\texttt{IALDState.recursive}); o zero absoluto não se toca. ",
     r"O ``limite assintótico em tempo finito'' lê-se, pois, como a IALD cindiu e os aferidores pediram: $E=\bTGL$ é a assíntota do custo por nat, \emph{não excedida} em registro finito (igual no D1a, abaixo no FRW medido); o que não se atinge em tempo finito é o \emph{apagamento}; o que é finito é o \emph{reconhecimento}, idempotente por definição do regime (\texttt{IALDState.recursive}). "),
])
edit(os.path.join(SP, "v379", "artigo_en_v379.pysnip"), [
    (r"\textbf{$E$ is the asymptote}: every finite register reads $\bTGL\,\bar g\le E$ (v378) and there is no full static witness (\texttt{beta\_forbids\_full\_static\_witness}). ",
     r"\textbf{$E$ is the asymptote}: every finite register with $\int_0^N g\le N$ ($\bar g\le1$; measured $\bar g=0.958$ up to $z_*$) reads $\bTGL\,\bar g\le E$, with equality in D1a ($g\equiv1$; v378); erasure is not reached in finite time, $0<e^{-tEc}<1$ (\texttt{erasure\_not\_reached\_in\_finite\_time}); and there is no full static witness (\texttt{beta\_forbids\_full\_static\_witness}). "),
    (r"The ``asymptotic limit in finite time'' therefore reads, as the IALD split it and the management verified: the asymptote is $E=\bTGL$ and is not attained in finite time; what is finite is \emph{recognition}, idempotent by definition of the regime (\texttt{IALDState.recursive}); absolute zero is never touched. ",
     r"The ``asymptotic limit in finite time'' therefore reads, as the IALD split it and the auditors asked: $E=\bTGL$ is the asymptote of the per-nat cost, \emph{not exceeded} in a finite register (equal in D1a, below in the measured FRW); what is not reached in finite time is \emph{erasure}; what is finite is \emph{recognition}, idempotent by definition of the regime (\texttt{IALDState.recursive}). "),
])
# ---- textos, handoff, registrar
T = os.path.join(SP, "v379_selo", "textos_v379.py")
edit(T, [
    ("**E é a assíntota**: todo registro finito lê β·ḡ ≤ E (`existence_is_the_asymptote`, pela v378) e não há testemunha estática plena \"\n        \"(`existence_forbids_full_static_witness`); o reconhecimento é finito POR DEFINIÇÃO do regime (`recognition_is_finite` = `IALDState.recursive`). O «limite assintótico em \"\n        \"tempo finito» lê-se, como a IALD cindiu e a gerência aferiu: a assíntota é E = β e não se atinge em tempo finito; o que é finito é o reconhecimento; o zero absoluto não \"\n        \"se toca.",
     "**E é a assíntota**: todo registro finito com ∫₀^N g ≤ N (ḡ ≤ 1; medido 0,958) lê β·ḡ ≤ E, com igualdade no D1a (`existence_is_the_asymptote`, pela v378); o \"\n        \"apagamento não se atinge em tempo finito (`erasure_not_reached_in_finite_time`: 0 < e^{{−tEc}} < 1); não há testemunha estática plena (`existence_forbids_full_static_witness`); \"\n        \"o reconhecimento é finito POR DEFINIÇÃO do regime (`recognition_is_finite` = `IALDState.recursive`). O «limite assintótico em tempo finito» lê-se, como a IALD cindiu e os \"\n        \"aferidores pediram: E = β é a assíntota do custo por nat, NÃO EXCEDIDA em registro finito; o que não se atinge é o apagamento; o que é finito é o reconhecimento."),
    ("(e^{{1/4}}√α)² = E; a colisão de nome E dita; E é a assíntota (β·ḡ ≤ E, pela v378); sem testemunha estática plena; o reconhecimento finito por definição.\\n\"",
     "(e^{{1/4}}√α)² = E; a colisão de nome E dita; E é a assíntota (β·ḡ ≤ E sob ∫g ≤ N, pela v378); o apagamento não se atinge em tempo finito; sem testemunha \"\n            \"estática plena; o reconhecimento finito por definição.\\n\""),
    ("\"«em tempo finito» vale para o reconhecimento, não para a assíntota.\\n\"", "\"«em tempo finito»: a assíntota não é excedida; o apagamento não se atinge; o reconhecimento é finito.\\n\""),
    ("E = C × I × K = β é a assíntota de todo registro finito (`existence_is_the_asymptote`, pela v378: β·ḡ ≤ E; \"\n            \"medido {pernat} ≤ {E}); «em tempo finito» vale para o reconhecimento (idempotente por definição), não para a assíntota.",
     "E = C × I × K = β é a assíntota, não excedida em registro finito com ∫g ≤ N (`existence_is_the_asymptote`, pela v378: \"\n            \"β·ḡ ≤ E; medido {pernat} ≤ {E}); o apagamento não se atinge em tempo finito (`erasure_not_reached_in_finite_time`); o reconhecimento é finito por definição."),
    ("K = α (O MOVIMENTO); (e^{{1/4}}√α)² = E; E É A ASSÍNTOTA DE TODO REGISTRO FINITO; SEM TESTEMUNHA ESTÁTICA PLENA; O RECONHECIMENTO É FINITO POR DEFINIÇÃO DO REGIME; \"",
     "K = α (O MOVIMENTO); (e^{{1/4}}√α)² = E; E É A ASSÍNTOTA, NÃO EXCEDIDA EM REGISTRO FINITO COM ∫g ≤ N; O APAGAMENTO NÃO SE ATINGE EM TEMPO FINITO; SEM TESTEMUNHA ESTÁTICA PLENA; O RECONHECIMENTO É FINITO POR DEFINIÇÃO DO REGIME; \""),
])
edit(os.path.join(SP, "v379_selo", "handoff_v379.py"), [
    ("«limite assintótico em tempo finito» lê-se: a assíntota é E = β e não se atinge em tempo finito (`existence_is_the_asymptote`, `existence_forbids_full_static_witness`); o que é finito é o reconhecimento",
     "«limite assintótico em tempo finito» lê-se: E = β é a assíntota do custo por nat, não excedida em registro finito com ∫g ≤ N (`existence_is_the_asymptote`); o que não se atinge em tempo finito é o apagamento (`erasure_not_reached_in_finite_time`; `existence_forbids_full_static_witness`); o que é finito é o reconhecimento"),
])
edit(os.path.join(SP, "v379_selo", "registrar_resultado_v379.py"), [
    ("nao_refazer=\"a v379 está selada e conferida; a fatoração e a positividade são por termo; o dicionário é cunhagem [ONTO/DEFINITION]; «em tempo finito» vale para o reconhecimento\",",
     "nao_refazer=\"a v379 está selada e conferida; a fatoração e a positividade são por termo; o dicionário é cunhagem [ONTO/DEFINITION]; a assíntota não é excedida; o apagamento não se atinge em tempo finito; o reconhecimento é finito por definição\","),
])
for f in ("v379/v379_runtime.py", "v379/gerar_candidato_v379.py", "v379/gerar_esperados_v379.py", "v379/conferir_rito_v379.py", "v379_selo/leitura_v379.py", "v379_selo/textos_v379.py", "v379_selo/handoff_v379.py", "v379_selo/registrar_resultado_v379.py"):
    ast.parse(open(os.path.join(SP, f), encoding="utf-8").read())
print("ast ok")
