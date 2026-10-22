# -*- coding: utf-8 -*-
"""aferir_citacoes_v386.py -- AFERIDOR ADVERSARIAL (lente: texto e citacoes), independente do conferidor do pacote.
Confere cada citacao do operador contra os TRES ARQUIVOS-FONTE (nao contra o transcrito):
  VERBO_operador_05out.txt (sha16 5973d79a49995c4c), RESPOSTAS_operador_05out.txt (b49b0d9e60ee4646),
  ramo_b/DECISAO_OPERADOR_RAMO_B_05out.json (a5d548235522c112 -> campo "verbatim").
Niveis: EXATO (so espacos normalizados) > CASEFOLD (maiusculas) > NAO_ACHADA. Os «…» cortam em pedacos NA ORDEM, na MESMA fonte.
Superficies: artigo PT/EN (``…''), runtime («…»), bloco v386 do Audit.lean («…»), pedra («…», 4+ palavras), V1.md («…», 4+ palavras),
errata W08 do md («…»), pinos (textos embutidos byte a byte), ESPEC/_V386_R6_ERRATA.texto_R6 (verbatim interno), V1.json (campos verbatim).
Tambem: o EN marca a traducao; §6 vazia nao preenchida; alpha^2 fora de citacao marcada; regex de vereditos proibidos; 'tudo agora' x 'agroa'.
So leitura fora desta pasta. Saida: AFERICAO_CITACOES_v386.json nesta pasta."""
import io, os, re, json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.dirname(HERE)
PK = os.path.join(V6, "pacote")
BANC = r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out"

def rd(p): return io.open(p, encoding="utf-8").read()
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

SRC = {
    "VERBO_16:53": os.path.join(V6, "VERBO_operador_05out.txt"),
    "RESPOSTAS_18:29": os.path.join(V6, "RESPOSTAS_operador_05out.txt"),
    "DECISAO_17:11": os.path.join(V6, "ramo_b", "DECISAO_OPERADOR_RAMO_B_05out.json"),
}
EXP = {"VERBO_16:53": "5973d79a49995c4c", "RESPOSTAS_18:29": "b49b0d9e60ee4646", "DECISAO_17:11": "a5d548235522c112"}
fontes = {}
for k, p in SRC.items():
    s = sha(p)
    assert s[:16] == EXP[k], (k, s)
    t = rd(p)
    if k == "DECISAO_17:11":
        t = json.loads(t)["verbatim"]
    fontes[k] = t
R = {"fontes": {k: {"sha256": sha(p), "bytes": os.path.getsize(p)} for k, p in SRC.items()}, "citacoes": {}, "resumo": {}}

def ws(t): return re.sub(r"\s+", " ", t).strip()
def delatex(t):
    t = re.sub(r"\\texttt\{([^}]*)\}", r"\1", t)
    t = re.sub(r"`([^`']*)'", r'"\1"', t)           # `x' -> "x" (convencao LaTeX; dito como tipografia)
    return t

def acha(q):
    """pedacos separados por «…» na ordem, na mesma fonte. Devolve (nivel, fonte)."""
    partes = [ws(p) for p in re.split(r"…|\.\.\.", q) if ws(p)]
    for nivel, f_ in (("EXATO", lambda s: s), ("CASEFOLD", lambda s: s.casefold())):
        for k, t in fontes.items():
            tt = f_(ws(t)); i = 0; ok = True
            for p in partes:
                j = tt.find(f_(p), i)
                if j < 0: ok = False; break
                i = j + len(p)
            if ok: return nivel, k
    return "NAO_ACHADA", None

def registra(sup, q, onde, extra=None):
    nivel, fonte = acha(q)
    d = {"superficie": sup, "onde": onde, "citacao": ws(q)[:220], "nivel": nivel, "fonte": fonte}
    if extra: d.update(extra)
    R["citacoes"].setdefault(sup, []).append(d)
    return nivel

NAO_SAO_DO_OPERADOR = {"o ramo B segue ENCERRADO", "O pilar rodou de novo, inteiro", "a natureza decidiu", "nature has decided", "decidido por delegação",
                       "o que falta eu responder?", "translated, condensed", "translated"}

# 1) artigo PT/EN: ``…''
for lg in ("pt", "en"):
    p = os.path.join(PK, "artigo_%s_v386.pysnip" % lg); t = rd(p)
    for m in re.finditer(r"``(.*?)''", t, flags=re.S):
        q = m.group(1)
        if q in NAO_SAO_DO_OPERADOR: continue
        ln = t[:m.start()].count("\n") + 1
        registra("artigo_%s" % lg, delatex(q), "artigo_%s_v386.pysnip:L%d" % (lg, ln),
                 {"latex_quote_substituida": bool(re.search(r"`[^`']*'", q))})
# 1b) EN: cada citacao PT tem marca de traducao logo depois?
t = rd(os.path.join(PK, "artigo_en_v386.pysnip")); en_marks = []
for m in re.finditer(r"``(.*?)''", t, flags=re.S):
    q = m.group(1); tail = t[m.end():m.end() + 160]
    marcado = bool(re.search(r"\((translated|the |branch |read twice|every )|---\s*the ", tail)) or q in NAO_SAO_DO_OPERADOR
    en_marks.append({"citacao": ws(q)[:80], "marcada": marcado, "cauda": ws(tail)[:70]})
R["en_marca_traducao"] = en_marks

# 2) runtime «…» (juntando as quebras de comentario)
rt = rd(os.path.join(PK, "v386_runtime.py")); rt2 = re.sub(r"\n#\s*", " ", rt)
for m in re.finditer(r"«(.*?)»", rt2, flags=re.S):
    q = ws(m.group(1))
    if len(q.split()) < 4 or q in NAO_SAO_DO_OPERADOR or q.startswith("decidido por"): continue
    registra("runtime", q, "v386_runtime.py (comentario/docstring)")

# 3) bloco v386 do Audit.lean
au = rd(os.path.join(V6, "kernel", "AUDIT_BLOCO_v386.lean"))
for m in re.finditer(r"«(.*?)»", au, flags=re.S):
    q = ws(m.group(1))
    if len(q.split()) < 4: continue
    registra("audit_bloco", q, "AUDIT_BLOCO_v386.lean (comentario datado)")

# 4) pedra (DEPOIS)
pd = rd(os.path.join(V6, "kernel", "TheVerbSelectsTheAction.lean.DEPOIS_v386"))
FORMULAS_LATEX = {"𝒱 = |a⟩⟨a|": r"\mathcal{V} = |a\rangle \langle a|", "ℛ(𝒱) = 𝒱 (ponto fixo)": r"\mathcal{R}(\mathcal{V}) = \mathcal{V} \quad \text{(ponto fixo)}",
                  "Nome = lim_{t→∞} 𝒱(t)": r"\text{Nome} = \lim_{t \to \infty} \mathcal{V}(t)", "NOME = lim_{t→∞} 𝒱(t)": r"\text{Nome} = \lim_{t \to \infty} \mathcal{V}(t)",
                  "sequência 𝒱ⁿ(a), n → ∞": r"\mathcal{V}^n(a) \to \mathcal{N}, \quad n \to \infty", "𝒱(t) = U 𝒱(0) U*": r"\mathcal{V}(t) = e^{-iHt/\hbar} \, \mathcal{V}(0) \, e^{iHt/\hbar}"}
for m in re.finditer(r"«(.*?)»", pd, flags=re.S):
    q = ws(m.group(1)); ln = pd[:m.start()].count("\n") + 1
    if len(q.split()) < 4 or q.startswith("decidido por"): continue
    nivel = registra("pedra", q, "TheVerbSelectsTheAction.lean:L%d" % ln)
    if nivel == "NAO_ACHADA":
        # tenta: prosa + formula pela tabela (o LaTeX do operador renderizado em Unicode)
        d = R["citacoes"]["pedra"][-1]
        parts = [p.strip() for p in re.split(r"…", q)]
        okp = True; obs = []
        for p in parts:
            if not p: continue
            if ":" in p and p.split(":", 1)[1].strip() in FORMULAS_LATEX:
                prosa, form = p.split(":", 1); form = form.strip()
                a = acha(prosa)[0] != "NAO_ACHADA"; b = ws(FORMULAS_LATEX[form]) in ws(fontes["VERBO_16:53"])
                okp = okp and a and b; obs.append("prosa:%s formula_latex:%s" % (a, b))
            elif p in FORMULAS_LATEX:
                b = ws(FORMULAS_LATEX[p]) in ws(fontes["VERBO_16:53"]); okp = okp and b; obs.append("formula_latex:%s" % b)
            else:
                a = acha(p)[0]; okp = okp and a != "NAO_ACHADA"; obs.append("pedaco:%s" % a)
        d["nivel"] = "FORMULA_RENDERIZADA_OK" if okp else "NAO_ACHADA"; d["obs"] = "; ".join(obs)

# 5) V1.md «…» (4+ palavras) -- classificado: do operador 05/10 (3 fontes) ou OUTRA_FONTE (nao auditavel aqui)
v1md = rd(os.path.join(BANC, "PREREGISTRO_RAMO_B_RINGDOWN_V1.md"))
for m in re.finditer(r"«(.*?)»", v1md, flags=re.S):
    q = ws(m.group(1)); ln = v1md[:m.start()].count("\n") + 1
    if len(q.split()) < 4: continue
    registra("V1_md", q, "PREREGISTRO_RAMO_B_RINGDOWN_V1.md:L%d" % ln)

# 6) errata W08 do md (no gerador e no md do ensaio)
g = rd(os.path.join(PK, "gerar_candidato_v386.py"))
i = g.find("W08_md_errata_R6"); w08 = g[i:i + 2500]
for m in re.finditer(r"«(.*?)»", w08, flags=re.S):
    q = ws(m.group(1))
    if len(q.split()) < 4: continue
    registra("md_errata_W08", q, "gerar_candidato_v386.py (patch W08)")
md = rd(os.path.join(PK, "dry_v386", "um_absoluto_forma_canonica.md"))
R["md_ensaio"] = {"errata_v385_posto_presente": "**Errata ao lado (v385, 05/10/2026, o operador):** o Um não é postulado — é **posto**" in md,
                  "errata_v386_R6_presente": "**Errata ao lado (v386, 05/10/2026, o operador):**" in md,
                  "ordem_v385_antes_v386": md.find("Errata ao lado (v385") < md.find("Errata ao lado (v386"),
                  "versao_carimbo": "**Versão v386**" in md}

# 7) pinos: textos embutidos == arquivos (bytes) ; R6 errata interna; 'tudo agora'
ns = {}; exec(compile(rd(os.path.join(PK, "v386_pins.py")), "v386_pins.py", "exec"), ns)
V = ns["_V386_OPERATOR_VERBATIM"]; pins_ok = {}
for k, f in V["files"].items():
    b = f["text"].encode("utf-8"); disk = open(f["path"], "rb").read()
    pins_ok[k] = {"sha256_embutido_ok": hashlib.sha256(b).hexdigest() == f["sha256"], "igual_ao_disco": disk == b, "bytes": len(b), "quando_utc": f["quando_utc"]}
R["pinos_textos_embutidos"] = pins_ok
r6 = ns["_V386_R6_ERRATA"]
inner = re.search(r"«(.*?)»", r6["texto_R6"], flags=re.S).group(1)
R["errata_R6"] = {"verbatim_interno_igual_DECISAO": ws(inner) == ws(fontes["DECISAO_17:11"]), "quando_utc": r6["quando_utc"],
                  "R6_v383_corrections_beside_termina_em_ENCERRADO": r6["R6_v383_corrections_beside"].endswith("o ramo B segue ENCERRADO"),
                  "delegacao_verbatim": r6.get("delegacao_verbatim"), "delegacao_verbatim_na_fonte": (r6.get("delegacao_verbatim") or "") in fontes["RESPOSTAS_18:29"]}
R["delegation_pins"] = {"texto": V.get("delegation"), "na_fonte": (V.get("delegation") or "") in fontes["RESPOSTAS_18:29"]}
# 'tudo agora' (nao verbatim) x 'tudo agroa' (verbatim) em cada superficie
sup = {"RESPOSTAS_json(leituras_da_gerencia)": rd(os.path.join(V6, "RESPOSTAS_operador_05out.json")), "v386_pins.py": rd(os.path.join(PK, "v386_pins.py")),
       "v386_runtime.py": rt, "artigo_pt": rd(os.path.join(PK, "artigo_pt_v386.pysnip")), "artigo_en": rd(os.path.join(PK, "artigo_en_v386.pysnip")),
       "V1_md": v1md, "V1_json": rd(os.path.join(BANC, "PREREGISTRO_RAMO_B_RINGDOWN_V1.json")), "pedra": pd, "audit_bloco": au,
       "ESPEC": rd(os.path.join(V6, "ramo_b", "ESPEC_RUNTIME_RAMO_B_v386.json")), "md_ensaio": md}
R["tudo_agora_vs_agroa"] = {k: {"tudo agora": t.count("tudo agora"), "tudo agroa": t.count("tudo agroa")} for k, t in sup.items()}

# 8) §6 vazia nao preenchida; alpha^2; regex proibido
rx_a2 = re.compile(r"α²|α\^2|alpha\^2|alpha²|\\alpha\^\{?2|alpha ao quadrado|quadrado de \$?\\?alpha|square of \$?\\?alpha", re.I)
rx_forb = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
R["secao6_vazia"] = {k: bool(re.search(r"genealogia como tríade|O seu nome é a tríade realizada", t)) for k, t in sup.items()}
R["alpha2"] = {}; R["regex_proibido"] = {}
for k, t in sup.items():
    hits = []
    for m in rx_a2.finditer(t):
        ctx = ws(t[max(0, m.start() - 110):m.end() + 60])
        hits.append({"linha": t[:m.start()].count("\n") + 1, "contexto": ctx,
                     "marcado_como_erro_de_signo": bool(re.search(r"nunca|NUNCA|never|régua do signo|regua do signo|sign ruler|escreve a constante como|proibido", ctx)),
                     "dentro_de_texto_embutido_do_operador": k == "v386_pins.py" and "mathcal" in ctx})
    R["alpha2"][k] = hits
    R["regex_proibido"][k] = [{"linha": t[:m.start()].count("\n") + 1, "contexto": ws(t[max(0, m.start() - 90):m.end() + 40])} for m in rx_forb.finditer(t)]

# 9) V1.json campos verbatim
J = json.loads(sup["V1_json"])
R["V1_json"] = {
    "ratificacao.verbatim == delegacao": J["ratificacao"]["verbatim"] == "o resto vc consegue responder tudo agroa",
    "ratificacao.verbatim_inteiro_sha256_txt == sha(RESPOSTAS.txt)": J["ratificacao"]["verbatim_inteiro_sha256_txt"] == R["fontes"]["RESPOSTAS_18:29"]["sha256"],
    "ratificacao.reabertura.verbatim == DECISAO.verbatim": ws(J["ratificacao"]["reabertura"]["verbatim"]) == ws(fontes["DECISAO_17:11"]),
    "ratificacao.reabertura.sha256 == sha(DECISAO)": J["ratificacao"]["reabertura"]["sha256"] == R["fontes"]["DECISAO_17:11"]["sha256"],
    "a_ponte_do_tempo.verbatim_operador_18_29_37 na fonte (EXATO)": ws(J["a_ponte_do_tempo"]["verbatim_operador_18_29_37"]) in ws(fontes["RESPOSTAS_18:29"]),
    "a_ponte_do_tempo.verbatim_luz_gravidade na fonte (EXATO)": ws(J["a_ponte_do_tempo"].get("verbatim_luz_gravidade") or "@@") in ws(fontes["RESPOSTAS_18:29"]),
    "leitura_da_gerencia_da_delegacao cita 'tudo agora' (NAO verbatim)": "tudo agora" in J["ratificacao"]["leitura_da_gerencia_da_delegacao"],
}

# resumo
for sup_, lst in R["citacoes"].items():
    c = {}
    for d in lst: c[d["nivel"]] = c.get(d["nivel"], 0) + 1
    R["resumo"][sup_] = c
R["en_todas_marcadas"] = all(e["marcada"] for e in en_marks)
out = os.path.join(HERE, "AFERICAO_CITACOES_v386.json")
tmp = out + ".tmp"
io.open(tmp, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1))
assert os.path.getsize(tmp) > 2000; os.replace(tmp, out)
print(json.dumps({"resumo": R["resumo"], "en_todas_marcadas": R["en_todas_marcadas"], "pinos": pins_ok, "errata_R6": R["errata_R6"], "delegation_pins": R["delegation_pins"],
                  "tudo_agora_vs_agroa": R["tudo_agora_vs_agroa"], "secao6_vazia": R["secao6_vazia"], "V1_json": R["V1_json"], "md_ensaio": R["md_ensaio"],
                  "alpha2_n": {k: len(v) for k, v in R["alpha2"].items()}, "regex_proibido_n": {k: len(v) for k, v in R["regex_proibido"].items()}}, ensure_ascii=False, indent=1))
print("\n=== NAO EXATAS ===")
for sup_, lst in R["citacoes"].items():
    for d in lst:
        if d["nivel"] != "EXATO":
            print("[%s] %s | %s | %s%s" % (d["nivel"], sup_, d["onde"], d["citacao"][:150], (" | " + d.get("obs", "")) if d.get("obs") else ""))
print("\n=== EN nao marcadas ===", [e for e in en_marks if not e["marcada"]])
print("sha256 deste script:", hashlib.sha256(open(__file__, "rb").read()).hexdigest())
