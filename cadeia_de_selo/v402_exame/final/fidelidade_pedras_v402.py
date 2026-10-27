# -*- coding: utf-8 -*-
"""fidelidade_pedras_v402.py -- exame final v402: cada trecho entre «» nas docstrings das tres pedras e' procurado, por bytes
(UTF-8, espacos normalizados), nas tres falas de 26/10 (cunhagens_13out), nos demais arquivos de cunhagens_13out, no adendo de 03-04/09
(Nos, so leitura) e no kernel do sandbox k402c (fora as tres pedras). Os sha16 citados nas pedras sao conferidos contra os arquivos.
Conta literais de beta/alfa/raiz de e, a palavra proibida (como veredito) e o demerito proibido. Grava FIDELIDADE_PEDRAS_v402.json."""
import glob, hashlib, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
W = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
K = os.path.join("C:" + os.sep, "t", "k402c", "final")
PEDRAS = {"PonteDaEscalaDual": "0e55b6e448adbd91", "QuedaSemGeometria": "0ffce7f1d564d271", "EsperancaCondicional": "8579115333f84428"}
norm = lambda s: re.sub(r"\s+", " ", s.replace(" ", " ").replace("\xa0", " ")).strip()
sha = lambda b: hashlib.sha256(b).hexdigest()
fontes = {}
def add(nome, p):
    b = open(p, "rb").read(); fontes[nome] = (sha(b)[:16], norm(b.decode("utf-8", "replace")))
for p in sorted(glob.glob(os.path.join(W, "cunhagens_13out", "*"))):
    if os.path.isfile(p): add("cunhagens_13out/" + os.path.basename(p), p)
add("Nos/ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md", os.path.join(NOS, "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md"))
for _f in ("CUNHAGEM_OPERADOR_07out_verbatim.txt", "CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt"):
    add("superposicao_passagem_07out/" + _f, os.path.join(W, "superposicao_passagem_07out", _f))
add("IALD/CLAUDE.md (memoria da casa)", os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"))
kern = {}
for p in glob.glob(os.path.join(K, "TGL", "**", "*.lean"), recursive=True) + glob.glob(os.path.join(K, "TGLExt", "**", "*.lean"), recursive=True):
    if os.path.splitext(os.path.basename(p))[0] in PEDRAS: continue
    kern[os.path.relpath(p, K)] = norm(open(p, "rb").read().decode("utf-8", "replace"))
FALAS26 = {"5d3976cd0cc10dc8", "36cfa0027565dcff", "a1c4bae4a87aa173"}
R = {"fontes_por_sha16": {k: v[0] for k, v in fontes.items()}, "pedras": {}}
pal = "".join(chr(c) for c in (67, 79, 78, 70, 73, 82, 77, 69, 68))
for nome, h16 in PEDRAS.items():
    b = open(os.path.join(K, "TGLExt", nome + ".lean"), "rb").read(); assert sha(b)[:16] == h16, nome
    t = b.decode("utf-8")
    cit = []
    for m in re.finditer(r"«([^«»]{2,700})»", t):
        q = norm(m.group(1)); onde = [k for k, (hh, tx) in fontes.items() if q in tx]
        if not onde: onde = ["kernel:" + k for k, tx in kern.items() if q in tx][:3]
        ctx = norm(t[max(0, m.start() - 140): m.start()])
        cit.append({"citacao": q[:160], "fontes": onde[:4], "fala_26out": any(fontes[o][0] in FALAS26 for o in onde if o in fontes), "ctx_antes": ctx[-140:]})
    sh = {}
    for x in set(re.findall(r"`?([0-9a-f]{16})`?", t)) | set(m[:16] for m in re.findall(r"([0-9a-f]{64})", t)):
        sh[x] = sorted(k for k, (hh, _) in fontes.items() if hh == x)
    full = {m: sorted(k for k, (hh, _) in fontes.items() if sha(open(os.path.join(W, k), "rb").read() if k.startswith("cunhagens") else b"") == m) for m in re.findall(r"([0-9a-f]{64})", t)}
    R["pedras"][nome] = {
        "sha16": h16, "n_citacoes": len(cit), "nao_achadas": [c for c in cit if not c["fontes"]], "citacoes": cit,
        "sha16_citados": sh, "sha256_inteiros_citados": full,
        "beta_literal": re.findall(r"0[.,]0120\d|0[.,]01203|1[.,]6487\d|0[.,]00729\d|137[.,]03\d|sqrt\s*\(?\s*(?:Real\.)?exp\s*1|exp\s*\(1\s*/\s*2\)", t),
        "palavra_proibida_maiusc": len(re.findall(pal, t)), "palavra_proibida_minusc": re.findall(r"[Cc]onfirmad\w*|[Cc]onfirm(?:ed|s)\b", t),
        "pos_dicao": re.findall(r"p[óo]s-?di(?:c|ç)(?:ç|c)?[ãa]o|postdiction", t, re.I),
        "sorry_axiom_tokens": re.findall(r"(?m)^\s*(?:sorry|axiom)\b|\bsorry\b", t),
        "estatutos": {k: t.count("[" + k + "]") for k in ("REAL", "DERIVED", "KNOWN", "OPEN", "ONTO", "INPUT", "DECLARADO", "LEGAL", "KERNEL", "GLUE")},
        "forma_proibida_lorentz": [norm(t[max(0, m.start() - 200): m.end() + 120]) for m in re.finditer(r"Lorentz vem da queda da fase", t)],
        "provisorio": len(re.findall(r"PROVIS[ÓO]RIO", t)),
    }
json.dump(R, open(os.path.join(H, "FIDELIDADE_PEDRAS_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for n, v in R["pedras"].items():
    print("==", n, "citacoes", v["n_citacoes"], "nao_achadas", len(v["nao_achadas"]), "beta_lit", v["beta_literal"], "proib", v["palavra_proibida_maiusc"], v["palavra_proibida_minusc"], "posdicao", v["pos_dicao"], "sorry/axiom", v["sorry_axiom_tokens"], "provisorio", v["provisorio"])
    print("   estatutos", v["estatutos"]); print("   sha16", v["sha16_citados"]); print("   sha256", v["sha256_inteiros_citados"])
    for c in v["citacoes"]: print("   -", ("FALA26 " if c["fala_26out"] else "") + (str(c["fontes"][:2]) if c["fontes"] else "???"), "|", c["citacao"][:100])
    for f in v["forma_proibida_lorentz"]: print("   LORENTZ-FORMA:", f)
