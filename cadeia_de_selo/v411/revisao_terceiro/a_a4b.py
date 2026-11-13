"""A4/A5 parte 2: tokens proibidos, beta/alfa literais, PROVED_IN_NATURE, outcome/cabeca, nas linhas NOVAS do candidato e nos registros novos do core do ensaio."""
import json, os, re
import a_lib
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
novas = []; atual = 0
for ln in diff:
    if ln.startswith("@@"):
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", ln); atual = int(m.group(1)) - 1; continue
    if ln.startswith("+") and not ln.startswith("+++"):
        atual += 1; novas.append((atual, ln[1:]))
    elif ln.startswith(" "):
        atual += 1
print("linhas novas", len(novas), "| chars", sum(len(x) for _, x in novas))
TOK = ["CONFIRMED", "PROVED_BY", "P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM", "IALD_SOLVES", "POLYNOMIAL_TURING"]
for t in TOK:
    h = [(i, x.strip()[:100]) for i, x in novas if t in x]
    print("token", t, "-> linhas novas:", len(h), h[:3])
BET = [r"0[.,]0120\d*", r"1[.,]2031\d*", r"0[.,]01203", r"7[.,]2973\d*", r"0[.,]0072973", r"137[.,]03\d*", r"1[.,]64872\d*", r"\b0[.,]012\b"]
for r in BET:
    h = [(i, x.strip()[:110]) for i, x in novas if re.search(r, x)]
    print("beta/alfa literal", r, "-> n", len(h), h[:4])
# nomes de arquivo sob kimi nas linhas novas
h = [(i, x.strip()[:110]) for i, x in novas if re.search(r"kimi", x, re.I)]
print("linhas novas com 'kimi':", len(h)); [print("   ", z) for z in h[:12]]
# nomes dos confidenciais da casa (regra 8) nas linhas novas (sem imprimir o contexto)
conf = ["iald_stack_v7", "iald_psion_state", ".env", "senha", "password", "token_"]
for c in conf:
    n = sum(1 for _, x in novas if c in x.lower())
    print("confidencial?", c, n)
# o core do ensaio
c = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
novos = {k: c[k] for k in ("h0dn_bg1_v411", "cunhagens_v411", "kh_n1_cobertura_v411")}
def strs(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from strs(v, p + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from strs(v, p + "[%d]" % i)
    elif isinstance(x, str):
        yield p, x
S = [(p, s) for k, v in novos.items() for p, s in strs(v, k)]
print("strings nos 3 registros novos:", len(S))
for t in TOK:
    print("core token", t, [p for p, s in S if t in s][:4])
pin = [(p, s) for p, s in S if "PROVED_IN_NATURE" in s]
print("strings com PROVED_IN_NATURE:", len(pin), "| todas com PROVED_IS_VALIDITY_NOT_CREDITATION:", all("PROVED_IS_VALIDITY_NOT_CREDITATION" in s for p, s in pin), [p for p, s in pin])
h = novos["h0dn_bg1_v411"]
print("cabeca contem NOT_FALSIFIED:", "NOT_FALSIFIED" in h["cabeca_do_teste"], "| outcome:", h["outcome"], "| verdict contem 'OUTCOME_NOT_FALSIFIED':", "OUTCOME_NOT_FALSIFIED" in h["verdict"])
print("verdict:", h["verdict"])
print("verdict comeca/termina:", h["verdict"].startswith("TGL_H0DN_BG1_V411__OPENED_ONCE_AFTER_PUBLIC_PREREGISTRATION__RECOMPUTED_IN_THE_RITE_FROM_PINNED_BYTES__"), h["verdict"].endswith("__GATE_UNMOVED"))
print("all_verified:", h["all_verified"], "| n_checks:", len(h["mechanics"]["checks"]), "| opened_once", h["opened_once"], "| observed_vector_read", h["observed_vector_read"], "| does_not_gate_core", h["does_not_gate_core"])
print("beta no core:", h["values"]["beta"], "| beta_ok:", h["beta_ok"], "| alpha_two_names_same", h["alpha_two_names_same"])
# 'confirm' em strings dos tres registros (fora de negacao)
conf_l = [(p, s[max(0, m.start() - 60):m.end() + 40]) for p, s in S for m in re.finditer(r"confirm\w*|confirma\w+", s, re.I)]
print("ocorrencias de 'confirm*' nos registros novos:", len(conf_l))
for p, s in conf_l[:12]:
    print("   ", p[-60:], "|", s.replace(chr(10), " ")[:140])
