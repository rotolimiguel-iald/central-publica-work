# -*- coding: utf-8 -*-
"""Os trechos do artigo PT/EN da v383, a partir dos da v382 (trocas exatas, cada uma conferida): o titulo; a DECISAO DO OPERADOR verbatim; o livro de ONZE; o
pre-registro V1.4; o «ao lado» so com o R6; e uma frase com as NOVE ROTAS do eco FORA do livro (estado, numeros e motivo, lidos do core e do V1.4)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(os.path.dirname(HERE), "v382")

# as rotas, renderizadas em LaTeX seguro (a amplitude e a lei pelo NOME lido do V1.4; as formulas das leis sao as das fontes, escritas em LaTeX)
ROTAS_PT = (r'''    _er2 = _r2.get("echo_routes_outside_the_ledger") or {}; _ro2 = _er2.get("routes") or []
    _amp2 = {"√β": r"$\sqrt{\bTGL}$", "sin 2θ": r"$\sin 2\theta_M$", "β": r"$\bTGL$"}
    _lei2 = {"KMS": r"KMS, $2\pi/\kappa$", "DEC": r"dezembro, $2GM_f/(\bTGL c^3)$", "MAY": r"maio, $(2GM_f/c^3)\ln(1/\bTGL)$"}
    _st2 = {"EXCLUDED_BY_DATA": "excluída pelos dados", "INCONCLUSIVE": "inconclusiva"}
    _nr2 = lambda r_: (r_.get("numbers_read") or {})
    _rn2 = lambda r_: ((r", $z_{\rm excl}=" + _f2(_nr2(r_).get("z_excl"), 2) + "$" + ((r", subamostra cega do O4 (não independente) $" + _f2(_nr2(r_).get("z_excl_o4_cego"), 2) + "$") if _nr2(r_).get("z_excl_o4_cego") is not None else "")) if _nr2(r_).get("z_excl") is not None else ((r", sistemática relativa " + _f2(_nr2(r_).get("sist_rel"), 2)) if _nr2(r_).get("sist_rel") is not None else ""))
    _rotas2 = "; ".join(r"%s: %s com %s, %s%s" % (_tt2(r_.get("id")), _amp2.get(str((r_.get("amplitude_from_preregistration") or {}).get("leitura")), "n/d"), _lei2.get(str((r_.get("delay_law_from_preregistration") or {}).get("nome")), "n/d"), _st2.get(r_.get("state"), "n/d"), _rn2(r_)) for r_ in _ro2)
''')
ROTAS_EN = (r'''    _er2 = _r2.get("echo_routes_outside_the_ledger") or {}; _ro2 = _er2.get("routes") or []
    _amp2 = {"√β": r"$\sqrt{\bTGL}$", "sin 2θ": r"$\sin 2\theta_M$", "β": r"$\bTGL$"}
    _lei2 = {"KMS": r"KMS, $2\pi/\kappa$", "DEC": r"December, $2GM_f/(\bTGL c^3)$", "MAY": r"May, $(2GM_f/c^3)\ln(1/\bTGL)$"}
    _st2 = {"EXCLUDED_BY_DATA": "excluded by the data", "INCONCLUSIVE": "inconclusive"}
    _nr2 = lambda r_: (r_.get("numbers_read") or {})
    _rn2 = lambda r_: ((r", $z_{\rm excl}=" + _f2(_nr2(r_).get("z_excl"), 2) + "$" + ((r", blind O4 subsample (not independent) $" + _f2(_nr2(r_).get("z_excl_o4_cego"), 2) + "$") if _nr2(r_).get("z_excl_o4_cego") is not None else "")) if _nr2(r_).get("z_excl") is not None else ((r", relative systematic " + _f2(_nr2(r_).get("sist_rel"), 2)) if _nr2(r_).get("sist_rel") is not None else ""))
    _rotas2 = "; ".join(r"%s: %s with %s, %s%s" % (_tt2(r_.get("id")), _amp2.get(str((r_.get("amplitude_from_preregistration") or {}).get("leitura")), "n/a"), _lei2.get(str((r_.get("delay_law_from_preregistration") or {}).get("nome")), "n/a"), _st2.get(r_.get("state"), "n/a"), _rn2(r_)) for r_ in _ro2)
''')

PT = [
    ("    # v382 (02/10/2026, tarde), a chave do operador:", "    # v383 (02/10/2026, noite) -- a DECISAO do operador «prefiro a primeira opção»: os nove pares do eco FORA do livro (rotas examinadas); base v381. Herdado da v382: a chave do operador:"),
    ('core.get("the_ledger_of_charges_v382")', 'core.get("the_ledger_of_charges_v383")'),
    ('    s.append(r"\\paragraph*{Ao lado (v382) --- O livro de cobranças e a viscosidade: a TGL é ótica, lê a face e o custo; nenhum desfecho move a regra; o pré-registro dos dois lados.} "',
     ROTAS_PT + '    s.append(r"\\paragraph*{Ao lado (v383) --- O livro de cobranças e a viscosidade: a TGL é ótica, lê a face e o custo; nenhum desfecho move a regra; o pré-registro dos dois lados; o eco como cópia atrasada fora do livro.} "'),
    ("a TGL permite ler os dois lados''. \"",
     "a TGL permite ler os dois lados''. Depois, o operador decidiu (02/10/2026, noite, verbatim no programa: ``prefiro a primeira opção''): os nove pares do eco como cópia atrasada não são cobranças da teoria e saem do livro, como rotas examinadas, com os números e o motivo de cada uma; a v382, que os trazia no livro ao lado, foi selada só no Nós e não é custodiada; esta versão parte da v381. \""),
    ('e igual ao do pré-registro dos dois lados V1.3, lido por bytes (JSON \\texttt{" + _sh2("json") + r"}, MD \\texttt{" + _sh2("md") + r"}; publicado na Bancada; supersede o V1.2, o V1.1 e o V1 pelos achados das aferições, antes de qualquer estimador ou dado novo): "',
     'e igual ao do pré-registro dos dois lados V1.4, lido por bytes (JSON \\texttt{" + _sh2("json") + r"}, MD \\texttt{" + _sh2("md") + r"}; publicado na Bancada; supersede o V1.3 pela decisão do operador, e os anteriores pelos achados das aferições, antes de qualquer estimador ou dado novo): "'),
    ('''r"), ao lado " + str(_r2.get("n_beside", "n/d")) + r" (os " + str((_r2.get("delayed_echo_pairs") or {}).get("n", "n/d")) + r" pares do eco como cópia atrasada --- " + str((_r2.get("delayed_echo_pairs") or {}).get("extinguished", "n/d")) + r" extintos, " + str((_r2.get("delayed_echo_pairs") or {}).get("inconclusive", "n/d")) + r" inconclusivos --- e o custo posto na face por convenção). O R4 lê''',
     '''r"), ao lado " + str(_r2.get("n_beside", "n/d")) + r" (o custo posto na face por convenção). Fora do livro, as " + str(_er2.get("n", "n/d")) + r" rotas examinadas do eco como cópia atrasada, que não são cobranças da teoria (o estado de cada uma é lido do rótulo da Fase 6 no core e conferido contra o V1.4): " + _rotas2 + r". O motivo, lido das fontes: a amplitude do eco igual a $|\\mathcal R|$ é leitura \\textsf{[ONTO]}, e a amplitude $\\sin 2\\theta_M$ é \\textsf{[CONJECTURE]}; a lei KMS toma a largura $2\\pi/\\kappa$ de uma faixa em tempo imaginário como atraso real (auditoria de 28/09, GWECO-05); a lei de dezembro é \\textsf{[DECLARADO]}, derivada por IA, não do axioma; as três leis de atraso nomeiam a massa do remanescente, e a leitura R6 ratificada diz que isso põe o custo na face; a v381 já pôs o eco como cópia atrasada fora da cadeia, e fica a definição do operador de 16/09, o eco como resposta da fronteira. O R4 lê'''),
    (r'(r"; nenhum \texttt{FALSIFIED} na regra" if not _cr2.get("FALSIFIED") else "")', r'(r"; nenhum \texttt{FALSIFIED} no livro" if not _ct2.get("FALSIFIED") else "")'),
]
EN = [
    ("    # v382 (02/10/2026, afternoon), the operator's key:", "    # v383 (02/10/2026, evening) -- the operator's DECISION «prefiro a primeira opção»: the nine echo pairs OUTSIDE the ledger (examined routes); base v381. Inherited from v382: the operator's key:"),
    ('core.get("the_ledger_of_charges_v382")', 'core.get("the_ledger_of_charges_v383")'),
    ('    s.append(r"\\paragraph*{Beside (v382) --- The ledger of charges and the viscosity: the TGL is optics, it reads the face and the cost; no outcome moves the rule; the pre-registration of both sides.} "',
     ROTAS_EN + '    s.append(r"\\paragraph*{Beside (v383) --- The ledger of charges and the viscosity: the TGL is optics, it reads the face and the cost; no outcome moves the rule; the pre-registration of both sides; the echo as a delayed copy outside the ledger.} "'),
    ("it allows reading both sides. \"",
     "it allows reading both sides. Then the operator decided (02/10/2026, evening, verbatim in the program, in Portuguese: ``prefiro a primeira opção'', I prefer the first option): the nine pairs of the echo as a delayed copy are not charges of the theory and leave the ledger, as examined routes, with the numbers and the reason for each; v382, which carried them in the ledger beside, was sealed only in the canonical folder and is not custodied; this version starts from v381. \""),
    ('and equal to the one in the pre-registration of both sides V1.3, read by bytes (JSON \\texttt{" + _sh2("json") + r"}, MD \\texttt{" + _sh2("md") + r"}; published on the Bench; it supersedes V1.2, V1.1 and V1 by the audits\' findings, before any new estimator or data): "',
     'and equal to the one in the pre-registration of both sides V1.4, read by bytes (JSON \\texttt{" + _sh2("json") + r"}, MD \\texttt{" + _sh2("md") + r"}; published on the Bench; it supersedes V1.3 by the operator\'s decision, and the earlier ones by the audits\' findings, before any new estimator or data): "'),
    ('''r"), beside " + str(_r2.get("n_beside", "n/a")) + r" (the " + str((_r2.get("delayed_echo_pairs") or {}).get("n", "n/a")) + r" pairs of the echo as a delayed copy --- " + str((_r2.get("delayed_echo_pairs") or {}).get("extinguished", "n/a")) + r" extinguished, " + str((_r2.get("delayed_echo_pairs") or {}).get("inconclusive", "n/a")) + r" inconclusive --- and the cost placed on the face by convention). R4 reads''',
     '''r"), beside " + str(_r2.get("n_beside", "n/a")) + r" (the cost placed on the face by convention). Outside the ledger, the " + str(_er2.get("n", "n/a")) + r" examined routes of the echo as a delayed copy, which are not charges of the theory (the state of each is read from the Phase 6 label in the core and checked against V1.4): " + _rotas2 + r". The reason, read from the sources: the echo's amplitude equal to $|\\mathcal R|$ is a reading \\textsf{[ONTO]}, and the amplitude $\\sin 2\\theta_M$ is \\textsf{[CONJECTURE]}; the KMS law takes the width $2\\pi/\\kappa$ of a strip in imaginary time as a real delay (audit of 28/09, GWECO-05); the December law is \\textsf{[DECLARADO]}, derived by an AI, not from the axiom; the three delay laws name the remnant's mass, and the ratified reading R6 says that this puts the cost on the face; v381 already put the echo as a delayed copy outside the chain, and the operator's definition of 16/09, the echo as the boundary's response, stays. R4 reads'''),
    (r'(r"; no \texttt{FALSIFIED} in the rule" if not _cr2.get("FALSIFIED") else "")', r'(r"; no \texttt{FALSIFIED} in the ledger" if not _ct2.get("FALSIFIED") else "")'),
]
for nome, reps in (("pt", PT), ("en", EN)):
    s = open(os.path.join(V2, "artigo_%s_v382.pysnip" % nome), encoding="utf-8", newline="").read()
    for a, b in reps:
        assert s.count(a) == 1, (nome, s.count(a), a[:100]); s = s.replace(a, b)
    assert "delayed_echo_pairs" not in s and "the_ledger_of_charges_v382" not in s and "dos dois lados V1.3" not in s and "both sides V1.3" not in s
    out = os.path.join(HERE, "artigo_%s_v383.pysnip" % nome)
    assert not os.path.exists(out)
    open(out, "w", encoding="utf-8", newline="").write(s); print("ok", out, len(s.encode("utf-8")))
