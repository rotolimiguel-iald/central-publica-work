# -*- coding: utf-8 -*-
"""Aplica as correções baratas da 2ª aferição da v381 (#1, #2, #5, #6, #7, #8 no pacote; #9 mapa; #10 frontmatter da memória). O #3/#4 (docstring da pedra) foi
aplicado com o Edit no .lean. Substituições com count conferido; backup de bytes na memória."""
import os, sys, time, re
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE)
sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS"); import rotas


def rw(p, pairs):
    s = open(p, encoding="utf-8", newline="").read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:60], s.count(a)); s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


BS = "\\"
rw(os.path.join(HERE, "v381_runtime.py"), [
    ("da NOME aos dez elos na ordem dele e os amarra numa CONJUNCAO", "da NOME aos dez nomes na ordem dele e os amarra numa CONJUNCAO"),
    ("TRACE_SIGN_RADICALIZATION_RECORD_NAME_DISTINCTION_OPERATION_PARAMETRIZATION_EMERGENCE_GEOMETRIC_QUANTIZATION_GRADIENT_SPECTRUM__",
     "TRACE_SIGN_RECORD_NAME_DISTINCTION_OPERATION_PARAMETRIZATION_EMERGENCE_GEOMETRIC_QUANTIZATION_GRADIENT_SPECTRUM__"),
    ('("RUNTIME (a radicalizacao em numero, sobre o beta lido): sqrt(e) = %.12f = e^{1/2} = %.12f; (e^{1/4} sqrt(alpha))^2 = %.12f = beta do core a 1e-12 relativo"',
     '("RUNTIME (teste sobre o beta lido, redundante com o 1o por construcao -- a mesma igualdade alpha.sqrt(e) = beta): (e^{1/4} sqrt(alpha))^2 = %.12f = beta a 1e-12 relativo; sqrt(e) = %.12f = e^{1/2} = %.12f e identidade de ponto flutuante"'),
    ("% (half_nat_radical, half_nat_exp, radical * radical),", "% (radical * radical, half_nat_radical, half_nat_exp),"),
    ('"note": "beta = alpha.sqrt(e), a lista chainOrder, a contagem dos «havendo» e (e^{1/4} sqrt(alpha))^2 = beta sao testes/cruzamentos; theta_M, sin^2, |e^{i theta}| e e^{-beta} sao identidades de sanidade"',
     '"note": "testes/cruzamentos: beta = alpha.sqrt(e) (e a sua repeticao (e^{1/4} sqrt(alpha))^2 = beta), a lista chainOrder lida do fonte, a contagem dos «havendo»; identidades de sanidade: sqrt(e) = e^{1/2}, theta_M, sin^2, |e^{i theta}|, e^{-beta}"'),
    ('"half_nat_volume_is_the_radical", "elementaryReason_sq α hα", "RADICALIZAÇÃO, cujo operador é a MEIA-NAT"))),',
     '"half_nat_volume_is_the_radical", "elementaryReason_sq α hα", "RADICALIZAÇÃO, cujo operador é a MEIA-NAT", "LEITURAS [ONTO], ditas", "nenhum termo novo é provado aqui", "campo `equal_halves`"))),'),
])
rw(os.path.join(HERE, "artigo_pt_v381.pysnip"), [
    (r"sinal$\to$registro pela \emph{radicalização} cujo operador é a Meia-Nat (a troca das faces tem ponto fixo $\tfrac12$, as faces pesam $\tfrac12$ e $\tfrac12$, $\sqrt{e^{1}}=e^{1/2}$, o custo da Palavra inscrita no ponto fixo é $e^{1/2}$, $V(\tfrac12)=\sqrt e$, e $(e^{1/4}\sqrt\alpha)^2=E=\bTGL$: a fronteira extrai o radical)",
     r"sinal$\to$registro pela \emph{radicalização} cujo operador é a Meia-Nat, o expoente $\tfrac12$ (o ponto fixo da troca $x\mapsto1-x$ é $\tfrac12$; as faces pesam $\tfrac12$ e $\tfrac12$ porque o certificado as declara iguais e o Nome pesa 1; $\sqrt{e^{1}}=e^{1/2}$; o custo da Palavra inscrita no ponto fixo é $e^{1/2}$; $V(\tfrac12)=\sqrt e$; e $(e^{1/4}\sqrt\alpha)^2=E=\bTGL$: a fronteira extrai o radical --- ``$J$ é a troca das faces'' e ``isto é o registro'' são leituras \textsf{[ONTO]}, ditas na pedra; nenhum termo novo)"),
])
rw(os.path.join(HERE, "artigo_en_v381.pysnip"), [
    (r"sign$\to$record by the \emph{radicalization} whose operator is the Half-Nat (the swap of the faces has fixed point $\tfrac12$, the faces weigh $\tfrac12$ and $\tfrac12$, $\sqrt{e^{1}}=e^{1/2}$, the cost of the inscribed Word at the fixed point is $e^{1/2}$, $V(\tfrac12)=\sqrt e$, and $(e^{1/4}\sqrt\alpha)^2=E=\bTGL$: the boundary extracts the radical)",
     r"sign$\to$record by the \emph{radicalization} whose operator is the Half-Nat, the exponent $\tfrac12$ (the fixed point of the swap $x\mapsto1-x$ is $\tfrac12$; the faces weigh $\tfrac12$ and $\tfrac12$ because the certificate declares them equal and the Name weighs 1; $\sqrt{e^{1}}=e^{1/2}$; the cost of the inscribed Word at the fixed point is $e^{1/2}$; $V(\tfrac12)=\sqrt e$; and $(e^{1/4}\sqrt\alpha)^2=E=\bTGL$: the boundary extracts the radical --- ``$J$ is the swap of the faces'' and ``this is the record'' are readings \textsf{[ONTO]}, stated in the stone; no new term)"),
    (r"when the auditor counted the gap between sign and record, the operator filled it (verbatim, in Portuguese): ``the verbatim with eight `havendo' is an open clause; the link is the half-nat''; ``it is the radicalization I meant, whose operator is the half-nat''.",
     r"when the auditor counted the gap between sign and record, the operator filled it (verbatim in the program, in Portuguese; rendered here in English): the verbatim with eight ``havendo'' is an open clause, the link is the half-nat; it is the radicalization he meant, whose operator is the half-nat."),
])
rw(os.path.join(HERE, "_derivar_pacote_v381.py"), [
    ('"A REGRA MATRIZ: beta do core = alpha.sqrt(e) (1e-9 rel.); sin^2 theta_M = beta (1e-12); |e^{i theta_M}| = 1; dez nomes na ordem (lidos do fonte); 0 < e^{-beta} < 1; (e^{1/4} sqrt(alpha))^2 = beta (a radicalizacao); 8 havendo no verbatim"',
     '"A REGRA MATRIZ: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.), (e^{1/4} sqrt(alpha))^2 = beta, dez nomes na ordem lidos do fonte, 8 havendo no verbatim; IDENTIDADES DE SANIDADE (nao testes) -- sin^2 theta_M = beta, |e^{i theta_M}| = 1, 0 < e^{-beta} < 1"'),
    ("'    \"a leitura v381 do selo sem palavra proibida\": not GUARDA.search(str(selo.get(\"the_matrix_rule_reading_v381\", \"\"))),\\n'",
     "'    \"a leitura v381 do selo sem palavra proibida (com a terceira palavra)\": not GUARDA.search(str(selo.get(\"the_matrix_rule_reading_v381\", \"\"))) and \"TGL_PRO\" + \"VED\" not in str(selo.get(\"the_matrix_rule_reading_v381\", \"\")),\\n'"),
])
rt = os.path.join(HERE, "v381_runtime.py"); t = open(rt, encoding="utf-8", newline="").read()
t2, n = re.subn(r"a radicalizacao em numero: sqrt\(e\) = e\^\{1/2\} e \(e\^\{1/4\} sqrt\(alpha\)\)\^2 = beta do core\s*\(identidade de sanidade sobre o beta lido\)",
                "(e^{1/4} sqrt(alpha))^2 = beta do core (teste, redundante com o primeiro por construcao)", t, flags=re.S)
assert n == 1, n; open(rt, "w", encoding="utf-8", newline="").write(t2)
print("runtime, artigo PT/EN e _derivar corrigidos")
# #10 frontmatter da memoria (com backup de bytes)
p = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\beta-e-a-regra-matriz-02out.md"; raw = open(p, "rb").read(); ST = time.strftime("%Y%m%d_%H%M%S")
txt = raw.decode("utf-8")
a = 'description: "CUNHAGEM do operador (02/10/2026), verbatim: «Betatgl é a regra matriz» — os nove «havendo»'
assert txt.count(a) == 1, "frontmatter nao achado"
txt = txt.replace(a, 'description: "CUNHAGEM do operador (02/10/2026), verbatim: «Betatgl é a regra matriz» — dez nomes, nove elos: oito «havendo» ditos + a radicalização pela Meia-Nat (a cláusula aberta, preenchida por ele)')
a2 = '; β não se deriva; o observável é o espectro de gradiente"'
if txt.count(a2) == 1:
    txt = txt.replace(a2, '; β não se deriva DO DADO (a forma α√e é derivada do axioma, v376); o observável é o espectro de gradiente [leitura ratificada]"')
raw2 = txt.encode("utf-8")
bak = p + ".bak_" + ST + "_frontmatter"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = p + ".tmp"; open(tmp, "wb").write(raw2); assert os.path.getsize(tmp) == len(raw2) and len(raw2) > len(raw) - 50; os.replace(tmp, p); print("frontmatter atualizado com backup:", len(raw), "->", len(raw2))
# #9 ERRATA no mapa (corrige 267)
regs = rotas._le()
if not any("errata_267_elo_meia_nat" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([dict(tipo="ERRATA", corrige=267, rota_id="kernel.regra_matriz.cadeia_unica", status="PROPOSTA", estatuto="ONTO", olhou_dados=False,
        titulo="errata_267_elo_meia_nat (02/10): onde a seq 267 diz «o elo sinal→registro é leitura da gerência ratificada» e «TEN_NAMES_EIGHT_HAVENDO_SAID», leia-se: o elo é a RADICALIZAÇÃO, cujo operador é a MEIA-NAT, dito pelo operador (seq 269); o token da v381 é TEN_NAMES_NINE_LINKS__EIGHT_HAVENDO_SAID__THE_OPEN_CLAUSE_..._IS_THE_RADICALIZATION_WHOSE_OPERATOR_IS_THE_HALF_NAT",
        resultado="verbatim do operador: «O verbatim com oito “havendo” é cláusula aberta, o elo é a meia-nat»; «É a radicalização que eu quis dizer, cujo operador é a meia-nat»",
        nao_refazer="não chamar o nono elo de leitura da gerência", proximo_passo="rito v381; registro RESULTADO desta rota depois do selo")],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: errata ja registrada")
