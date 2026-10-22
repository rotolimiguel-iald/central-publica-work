# -*- coding: utf-8 -*-
"""Verificacao independente da INTEGRIDADE do pre-registro (nao e ensaio de afirmacao nenhuma).
Rele os textos do operador e o um.py (busca de linha), resegmenta, e confere que PREREGISTRO.json/.md
dizem o que os bytes dizem. Somente leitura; imprime o resultado; sai com codigo 2 na primeira falha."""
import hashlib, json, math, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import segmentar  # noqa: E402

UMPY = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\um.py"
ok = []


def falha(m):
    print("FALHA VISIVEL:", m)
    sys.exit(2)


def sha(b):
    return hashlib.sha256(b).hexdigest()


js_b = open(os.path.join(AQUI, "PREREGISTRO.json"), "rb").read()
md_b = open(os.path.join(AQUI, "PREREGISTRO.md"), "rb").read()
for nome, b in (("json", js_b), ("md", md_b)):
    if b.startswith(b"\xef\xbb\xbf") or b"\r\n" in b or not b.endswith(b"\n"):
        falha(nome + ": BOM, CRLF ou sem LF final")
D = json.loads(js_b.decode("utf-8"))
md = md_b.decode("utf-8")
ok.append("json e md: UTF-8 sem BOM, LF, JSON valido")

# (a) verbatins
for c in ("V1", "V2", "V3", "V4"):
    b = open(segmentar.TEXTOS[c], "rb").read()
    h = sha(b)
    v = D["a_verbatins"][c]
    if v["sha256"] != h or v["bytes"] != len(b) or not v["confere"] or h[:16] != segmentar.SHA16_ORDEM[c]:
        falha("verbatim %s nao confere" % c)
    if h not in md:
        falha("sha256 de %s ausente no MD" % c)
b2 = open(segmentar.TEXTOS["V2"], "rb").read().split(b"\n")
tr = b"\n".join(b2[:33])
if sha(tr) != D["a_verbatins"]["V2"]["trilha"]["sha256"] or not b2[33].startswith("O que mais me fascina".encode("utf-8")):
    falha("trecho da trilha de V2")
ok.append("4 verbatins: sha256 e bytes conferem com os arquivos e com os sha16 da ordem; trecho V2 l.1-33 confere")

# (b) mapeamento: toda frase da trilha tem linha, marca e sha16 corretos
linhas = {r[0]: r for r in D["b_mapeamento"]["linhas"]}
marcas_ok = {"[INPUT da gerência]", "[ONTO]", "[MARCAÇÃO]"}
n_fora, n_dentro = 0, 0
v1norm = {}
for c in ("V1", "V2", "V3", "V4"):
    segs, h, n, fr = segmentar.segmentos(c)
    for s in segs:
        if s["escopo"] != "TRILHA_POSTO":
            n_fora += 1
            if s["id"] in linhas:
                falha("frase fora do escopo no mapeamento: " + s["id"])
            continue
        n_dentro += 1
        if c == "V1":
            v1norm[s["id"]] = segmentar.normalizar(s["texto"])
        r = linhas.get(s["id"])
        if r is None:
            falha("frase sem marca: " + s["id"])
        if r[3] not in marcas_ok:
            falha("marca invalida em " + s["id"])
        if r[2] != sha(s["texto"].encode("utf-8"))[:16]:
            falha("sha16 da frase " + s["id"])
        t = r[1]
        if t.startswith("="):
            par = t[1:]
            if c != "V2" or v1norm.get(par) != segmentar.normalizar(s["texto"]):
                falha("igualdade V2=V1 falsa em " + s["id"])
            if linhas[par][3] != r[3]:
                falha("marca herdada divergente em " + s["id"])
        elif r[3] == "[INPUT da gerência]" or s["tipo"] == "MARCACAO":
            if t != s["texto"]:
                falha("texto INPUT nao e verbatim em " + s["id"])
        else:
            pre = t[:-2] if t.endswith(" …") else t
            if not s["texto"].startswith(pre):
                falha("inicio ONTO nao e prefixo em " + s["id"])
if len(linhas) != n_dentro:
    falha("linhas a mais no mapeamento")
if n_fora != 23 or str(n_fora) not in D["b_fora_do_escopo"]:
    falha("contagem fora do escopo")
ok.append("mapeamento: %d frases da trilha, todas marcadas (sha16 conferido, INPUT verbatim, ONTO prefixo, V2=V1 conferido); %d fora do escopo (F1.TEMPO)" % (n_dentro, n_fora))

# (c) afirmacoes
ids_af = {a["id"] for a in D["c_afirmacoes"]}
esperados_ok = ("PASSA", "FALHA", "CITADO", "CITADO_REAL", "NAO_TESTAVEL", "ABERTO")
n_partes = 0
for a in D["c_afirmacoes"]:
    for k in ("id", "titulo", "frases", "estatuto", "partes", "controles", "nao_afirma"):
        if k not in a:
            falha("afirmacao %s sem %s" % (a.get("id"), k))
    for p in a["partes"]:
        n_partes += 1
        if len(p) != 7 or not p[6].split(" (")[0] in esperados_ok:
            falha("parte mal formada: %r" % p[:1])
        if p[1] not in md or p[0] not in md:
            falha("parte %s ausente do MD" % p[0])
for r in D["b_mapeamento"]["linhas"]:
    for af in r[5]:
        if af not in ids_af:
            falha("mapeamento cita afirmacao inexistente: " + af)
for req in ("P1", "P2", "P3", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "O1", "O2"):
    if req not in ids_af:
        falha("afirmacao minima ausente: " + req)
falhas_esp = sorted(p[0] for a in D["c_afirmacoes"] for p in a["partes"] if p[6].startswith("FALHA"))
if falhas_esp != ["B5.e(ii)", "B9.a", "B9.a'"]:
    falha("FALHAs pre-registradas inesperadas: %r" % falhas_esp)
for a in D["c_afirmacoes"]:
    if a["id"] in ("O1", "O2") and any(p[6] == "PASSA" for p in a["partes"]):
        falha("ONTO/OPEN com PASSA")
ok.append("%d afirmacoes, %d partes, 7 campos cada, esperado em %s; FALHAs pre-registradas = %s; O1/O2 sem PASSA" % (len(ids_af), n_partes, "/".join(esperados_ok), falhas_esp))
for sec in ("## (a)", "## (b)", "## (c)", "## (d)", "## (e)", "## (f)"):
    if sec not in md:
        falha("MD sem secao " + sec)
for k in ("a_verbatins", "b_mapeamento", "c_afirmacoes", "d_controles", "d_sondas_de_vacuidade", "e_pedra", "f_regra_de_decisao"):
    if k not in D:
        falha("JSON sem " + k)
if len(D["d_controles"]["lista"]) != 14:
    falha("controles")
ok.append("secoes (a)-(f) presentes no JSON e no MD; 14 controles")

# beta: releitura independente dos bytes do um.py
alphas = []
with open(UMPY, "rb") as fh:
    for ln in fh:
        m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", ln.rstrip(b"\r\n"))
        if m:
            alphas.append(m.group(1).decode())
if len(alphas) != 1:
    falha("alpha nao unico")
beta = float(alphas[0]) * math.sqrt(math.e)
if repr(beta) != D["beta_runtime"]["beta_float64"] or repr(math.asin(math.sqrt(beta))) != D["beta_runtime"]["theta_M"]:
    falha("beta/thetaM divergem do runtime relido")
ok.append("beta relido dos bytes: %s; thetaM %s" % (repr(beta), D["beta_runtime"]["theta_M"]))

# guardas de vocabulario e de literal
txt = js_b.decode("utf-8") + md
for pr in ("CONFIRMED", "CONFIRMADA", "não provou", "nao provou", "pós-dição", "pos-dicao"):
    if pr in txt:
        falha("palavra proibida: " + pr)
for f in ("gerar_preregistro.py", "segmentar.py", "verificar_preregistro.py"):
    src = open(os.path.join(AQUI, f), "rb").read().decode("utf-8")
    lits = re.findall(r"0\.0120313\d*", src)
    if f == "gerar_preregistro.py" and lits != [D["beta_runtime"]["beta_float64"]]:
        falha("literal de beta fora da conferencia em " + f)
    if f != "gerar_preregistro.py" and lits:
        falha("literal de beta em " + f)
ok.append("sem a palavra proibida; beta literal so na constante de conferencia do gerador")
for linha in ok:
    print("OK", linha)
print("VERIFICACAO_DE_INTEGRIDADE_PASSOU", sha(js_b), sha(md_b))
