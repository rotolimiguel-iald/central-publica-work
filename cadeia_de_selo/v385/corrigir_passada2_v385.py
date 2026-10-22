# -*- coding: utf-8 -*-
"""Disposicoes da SEGUNDA passada de afericao da v385 (afericao_passada2\\RELATORIO_AFERIDOR_PASSADA2_v385.txt):
 1 CORRIGIR: a W07 (selo) e o conferidor leem as chaves NOVAS do comparador (max_scaled_diff, max_rel_diff_finite, d128_excluded, inputs, env);
 2 CORRIGIR: o conferidor de citacoes so aceita palavras do OPERADOR -- pula isCompactSummary/isMeta, corta os <pasted_content>, e confere tambem as
   citacoes «…» da pedra (contra os transcritos de 05/10 e de 20/08) -- (feito em conferir_citacoes_v385.py, reescrito a parte);
 N1/N2/N10 (pedra e artigo): o Verbo «age como o escalar q(0)»; as hipoteses de verb_not_identity; «proibida por beta > 0 e g > 0»; «conjugado» la e' a
   leitura do modulo para «invariante sob todos os operadores»; N3: o token sem «STATIC_ONE»; N4: contagens velhas em comentarios; N5: «logo depois de
   lancar o trabalhador» nos comentarios; N6: \\mathrm{max} (sobrevive no TXT); N7: o token NOT_COMPARED quando esta rodada nao calcula; N8: o restaurador
   com volta e stderr; N10: int contra booleano conta como diferenca; as traducoes do EN marcadas «condensada».
Pares contados; backup de BYTES; temporario -> conferir -> substituir; ast.parse nos .py; compile() nos .pysnip."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE)
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(P, pares, modo="py"):
    b0 = open(P, "rb").read(); s = b0.decode("utf-8")
    crlf = b0.count(b"\r\n") == b0.count(b"\n") and b0.count(b"\n") > 0
    if crlf:
        pares = [(a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) for a, b in pares]
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (os.path.basename(P), "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    if modo == "py":
        ast.parse(s)
    elif modo == "snip":
        compile("def _f(core, s):\n" + s, P, "exec")
    open(P + ".bak_" + st + "_p2", "wb").write(b0)
    nb = s.encode("utf-8")
    open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
    print("OK", os.path.basename(P), len(pares), "trocas")


# ---- a pedra (sandbox; CRLF)
aplica(os.path.join(SP, "v376", "kernel_src", "TGLExt", "TheAxiomAndTheFalseWitness.lean"), [
    ("* ★ `the_living_verb_moves` (o Verbo não é a identidade: `verb_not_identity`) e `the_living_verb_fixes_the_name` (o Verbo fixa\n"
     "  o Nome: `verb_word_fixes_the_name`) — re-exportações, TRIVIAIS, ditas como triviais: dão nome de hoje ao que já estava provado.",
     "* ★ `the_living_verb_moves` (o transporte e^{−tβD} não é a identidade, com t > 0, β > 0 e algum d_i > 0: `verb_not_identity`) e\n"
     "  `the_living_verb_fixes_the_name` (no núcleo, a palavra do Verbo age como o escalar q(0): `verb_word_fixes_the_name`) — dois termos\n"
     "  distintos, cada um com o seu objeto; re-exportações, TRIVIAIS, ditas como triviais: dão nome de hoje ao que já estava provado."),
    ("Lá, «conjugado» quer dizer comutar com TODOS os\noperadores (a matemática segue verdadeira); ser conjugado PELO VERBO é outra coisa.",
     "Lá, «conjugado» é a leitura do módulo para «invariante sob\nTODOS os operadores» (`totally_invariant_is_all_or_nothing`; a matemática segue verdadeira); ser conjugado PELO VERBO é outra coisa."),
    ("/-- ★★★ O PONTO FIXO 0 É A TESTEMUNHA FALSA: √0 = 0; a testemunha ESTÁTICA plena é proibida por β > 0; e o zero absoluto\n    não se alcança em tempo finito. -/",
     "/-- ★★★ O PONTO FIXO 0 É A TESTEMUNHA FALSA: √0 = 0; a testemunha ESTÁTICA plena é proibida no fluxo escalar e^{−tβg} com β > 0\n"
     "    e g > 0; e o zero absoluto não se alcança em tempo finito (nenhuma componente não nula do fluxo diagonal se anula; exp ≠ 0). -/"),
], modo="lean")
# ---- o runtime
aplica(os.path.join(HERE, "v385_runtime.py"), [
    ("# versao final roda tudo), e a v385 le, ANTES do calculo, o resultado guardado no cache pela rodada anterior",
     "# versao final roda tudo), e a v385 le, logo depois de lancar o trabalhador (antes que o calculo novo possa substitui-lo), o resultado guardado no cache pela rodada anterior"),
    ("THE_ZERO_IS_THE_FALSE_WITNESS_THE_STATIC_ONE_FORBIDDEN_BY_BETA_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME__",
     "THE_ZERO_IS_THE_FALSE_WITNESS_THE_FULL_STATIC_WITNESS_FORBIDDEN_BY_BETA_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME__"),
    ('            out["why_not"] = "a rodada desta versao nao CALCULA o pilar (modo %s)" % ((st or {}).get("mode") if isinstance(st, dict) else None)',
     '            out["why_not"] = "a rodada desta versao nao CALCULA o pilar (modo %s)" % ((st or {}).get("mode") if isinstance(st, dict) else None)\n'
     '            out["not_compute"] = True   # (2a passada, N7) o que faltou foi o calculo DESTA rodada, nao a anterior'),
    ('    if not isinstance(prev, dict) or not prev.get("read"):\n        why = (prev or {}).get("why_not") or (prev or {}).get("error") or "sem leitura"',
     '    if isinstance(prev, dict) and not prev.get("read") and prev.get("not_compute"):\n'
     '        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",\n'
     '                     "compared": False, "why": prev.get("why_not")})\n'
     '        return base\n'
     '    if not isinstance(prev, dict) or not prev.get("read"):\n        why = (prev or {}).get("why_not") or (prev or {}).get("error") or "sem leitura"'),
    ("        elif x_ != y_:", "        elif x_ != y_ or type(x_) is not type(y_):   # (2a passada, N10) 1 contra True conta como diferenca"),
])
# ---- o gerador
aplica(os.path.join(HERE, "gerar_candidato_v385.py"), [
    ("10128 declaracoes, todas no trio, zero sorry, 28/28 bandeiras).", "10129 declaracoes, todas no trio, zero sorry, 29/29 bandeiras -- lidos de kernel/sandbox_raiz_v385.json)."),
    ('"        # v385: o Axioma e a testemunha falsa (21) + o TheDarkSplit auditado (7)" + CRLF',
     '"        # v385: o Axioma e a testemunha falsa (%d) + o TheDarkSplit auditado (%d)" % (len(AXM), len(DKS)) + CRLF'),
    ("# v385: le, ANTES do calculo, o resultado que o cache guardou da rodada anterior (mesma chave), para a reprodutibilidade",
     "# v385: le, logo depois de lancar o trabalhador (antes que o calculo novo possa substitui-lo), o resultado que o cache guardou da rodada anterior (mesma chave), para a reprodutibilidade"),
    ('for k_ in ("verdict", "compared", "n_fields", "n_differ", "max_rel_diff", "same_pillar_verdict", "previous", "this_run", "why")},',
     'for k_ in ("verdict", "compared", "n_fields", "n_numeric_fields", "n_differ", "max_scaled_diff", "max_rel_diff_finite", "n_nonfinite_differ", "d128_excluded", "inputs", "env", "same_pillar_verdict", "previous", "this_run", "why")},'),
])
# ---- o conferidor, os esperados, o ensaio
aplica(os.path.join(HERE, "conferir_rito_v385.py"), [
    ('for k in ("verdict", "compared", "n_fields", "n_numeric_fields", "n_differ", "max_rel_diff", "same_pillar_verdict", "why")},',
     'for k in ("verdict", "compared", "n_fields", "n_numeric_fields", "n_differ", "max_scaled_diff", "max_rel_diff_finite", "n_nonfinite_differ", "d128_excluded", "inputs", "env", "same_pillar_verdict", "why")},'),
])
aplica(os.path.join(HERE, "gerar_esperados_v385.py"), [("# o kernel do sandbox: as 28 declaracoes novas no trio, sem sorry", "# o kernel do sandbox: as declaracoes novas (29) no trio, sem sorry")])
aplica(os.path.join(HERE, "ensaio_a_seco_v385.py"), [
    ("conferido pelo sha256 pela propria _qp_cached_ok); e as 28 bandeiras da v385", "conferido pelo sha256 pela propria _qp_cached_ok); e as bandeiras da v385 (29)"),
    ('"SINTETICO": "as 28 bandeiras da v385 no kernel_formalization vem do relatorio do SANDBOX', '"SINTETICO": "as bandeiras da v385 (29) no kernel_formalization vem do relatorio do SANDBOX'),
])
# ---- o artigo
for lg in ("pt", "en"):
    P = os.path.join(HERE, "artigo_%s_v385.pysnip" % lg)
    if lg == "pt":
        pares = [(r"\texttt{verb\_not\_identity} (o transporte $e^{-t\beta D}$ não é a identidade)",
                  r"\texttt{verb\_not\_identity} (o transporte $e^{-t\beta D}$ não é a identidade, com $t>0$, $\beta>0$ e algum $d_i>0$)"),
                 (r"ali ``conjugado'' quer dizer comutar com \emph{todos} os operadores (a matemática segue verdadeira)",
                  r"ali ``conjugado'' é a leitura do módulo para ``invariante sob \emph{todos} os operadores'' (\texttt{totally\_invariant\_is\_all\_or\_nothing}; a matemática segue verdadeira)"),
                 (r"na escala $\max(1,|a|,|b|)$ do comparador", r"na escala $\mathrm{max}(1,|a|,|b|)$ do comparador")]
    else:
        pares = [(r"\texttt{verb\_not\_identity} (the transport $e^{-t\beta D}$ is not the identity)",
                  r"\texttt{verb\_not\_identity} (the transport $e^{-t\beta D}$ is not the identity, for $t>0$, $\beta>0$ and some $d_i>0$)"),
                 (r"there ``conjugated'' means commuting with \emph{all} operators (the mathematics stays true)",
                  r"there ``conjugated'' is the module's reading of ``invariant under \emph{all} operators'' (\texttt{totally\_invariant\_is\_all\_or\_nothing}; the mathematics stays true)"),
                 (r"on the scale $\max(1,|a|,|b|)$ of the bench comparator", r"on the scale $\mathrm{max}(1,|a|,|b|)$ of the bench comparator"),
                 (r"(translated: at the start of the chain it is not postulated", r"(translated, condensed: at the start of the chain it is not postulated"),
                 (r"(translated: there is no unconjugated observer;", r"(translated, condensed: there is no unconjugated observer;")]
    aplica(P, pares, modo="snip")
