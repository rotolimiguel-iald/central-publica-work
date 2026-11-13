"""CU-C6: B-03/B-08 a errata E44 PT e EN byte a byte contra o DESENHO; no candidato, no core, no artigo txt, no tex, no md e no texto extraido do PDF."""
import ast, json, os, re, sys, unicodedata, hashlib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
D = r"C:\t\k411c\dry_v411"
F = r"C:\t\k411c\falso_nos_v411"
OUT = r"C:\t\k411c\revisao_CU"
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
des = rd(os.path.join(V, "DESENHO_v411.md"))
m_pt = re.search(r"^- \*\*E44\*\* (.+)$", des, re.M)
m_en = re.search(r"^- \*\*E44 \(EN\)\*\* (.+)$", des, re.M)
E_PT, E_EN = m_pt.group(1).strip(), m_en.group(1).strip()
print("DESENHO E44 PT len", len(E_PT), "sha16", hashlib.sha256(E_PT.encode()).hexdigest()[:16], "| EN len", len(E_EN), "sha16", hashlib.sha256(E_EN.encode()).hexdigest()[:16])
R = {"desenho": {"pt_sha16": hashlib.sha256(E_PT.encode()).hexdigest()[:16], "en_sha16": hashlib.sha256(E_EN.encode()).hexdigest()[:16]}}
# candidato (AST)
src = open(os.path.join(V, "um_v411_candidato.py"), "rb").read().decode("utf-8")
t = ast.parse(src)
for n in t.body:
    if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "_V411_TEXTOS_DA_GERENCIA" for x in n.targets):
        d = ast.literal_eval(n.value)
        R["candidato_pt_igual"] = d["e44"]["pt"] == E_PT
        R["candidato_en_igual"] = d["e44"]["en"] == E_EN
        print("candidato _V411_TEXTOS_DA_GERENCIA e44 pt/en iguais ao DESENHO:", R["candidato_pt_igual"], R["candidato_en_igual"])
# core
core = json.load(open(os.path.join(D, "core_ensaio.json"), encoding="utf-8"))["core"]
r4 = core["h0dn_bg1_v411"]
e44 = [e for e in r4["erratas"] if e["id"] == "E44"][0]
R["core_erratas_pt"] = e44["texto"] == E_PT
R["core_erratas_en"] = e44["texto_en"] == E_EN
print("core h0dn_bg1_v411.erratas E44 texto/texto_en iguais:", R["core_erratas_pt"], R["core_erratas_en"], "| ids:", [e["id"] for e in r4["erratas"]])
cu = core["cunhagens_v411"]
print("cunhagens_v411.erratas ids:", [e.get("id") for e in cu.get("erratas", [])] if isinstance(cu.get("erratas"), list) else type(cu.get("erratas")))
# txt
for lang, nm, E in (("pt", "dry_v411_pt.txt", E_PT), ("en", "dry_v411_en.txt", E_EN)):
    tx = rd(os.path.join(D, nm))
    flat = re.sub(r"\s+", " ", tx)
    ef = re.sub(r"\s+", " ", E)
    i = flat.find(ef)
    print(lang, "txt: E44 inteiro (espacos normalizados) presente:", i >= 0, "| contagem:", flat.count(ef))
    R["txt_" + lang] = i >= 0
    # contexto: o paragrafo depois
    j = tx.find(E[:60])
    if j < 0:
        # a quebra de linha do txt pode cortar: acha pelo comeco normalizado
        j = 0
    paras = re.findall(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx)
    for k, p in enumerate(paras):
        pf = re.sub(r"\s+", " ", p)
        if pf.startswith("E44") or ef[:80] in pf:
            print("   paragrafo E44 e' o %d de %d; comeca com %r; termina igual ao DESENHO: %s; proximo paragrafo abre com: %r" % (k, len(paras), pf[:12], pf.rstrip().endswith(ef[-60:]), re.sub(r"\s+", " ", paras[k + 1])[:90]))
            print("   anterior abre com:", re.sub(r"\s+", " ", paras[k - 1])[:90])
            R["txt_%s_prefixo" % lang] = pf[:8]
            R["txt_%s_proximo" % lang] = re.sub(r"\s+", " ", paras[k + 1])[:60]
            break
# tex
for lang, nm, E in (("pt", "dry_v411_pt.tex", E_PT), ("en", "dry_v411_en.tex", E_EN)):
    tx = rd(os.path.join(D, nm))
    m = re.search(r"\\textbf\{E44\} (.+?)(?:\n\n|\Z)", tx, re.S)
    p = m.group(1)
    back = p
    for a, b in ((r"\%", "%"), (r"$\beta$", "\u03b2"), (r"$\sigma$", "\u03c3"), (r"$\times$", "\u00d7"), (r"\_", "_"), ("\\textquotedblleft{}", "\u201c"), ("\\textquotedblright{}", "\u201d"), (r"\&", "&"), (r"\#", "#")):
        back = back.replace(a, b)
    back2 = re.sub(r"\s+", " ", back).strip()
    ok = back2 == re.sub(r"\s+", " ", E)
    print(lang, "tex: E44 igual ao DESENHO apos desfazer o escape (%, beta, sigma, times, _):", ok, "| len", len(back2), len(E))
    R["tex_" + lang] = ok
    if not ok:
        import difflib
        sm = difflib.SequenceMatcher(None, back2, re.sub(r"\s+", " ", E), autojunk=False)
        for op in sm.get_opcodes():
            if op[0] != "equal":
                print("   dif", op[0], repr(back2[op[1]:op[2]])[:80], "->", repr(re.sub(r"\s+", " ", E)[op[3]:op[4]])[:80])
    # o que vem depois do paragrafo
    rest = tx[m.end():m.end() + 160].replace("\n", " ")
    print("   depois do paragrafo E44 (tex):", rest[:140])
    # o sinal de porcentagem escapado
    print("   % nao escapado dentro do paragrafo:", len(re.findall(r"(?<!\\)%", p)))
# md
md = rd(os.path.join(F, "um_absoluto_forma_canonica.md"))
for lang, E in (("pt", E_PT),):
    k = md.find("**E44** ")
    seg = md[k:k + len(E) + 20] if k >= 0 else ""
    R["md_pt"] = (k >= 0 and E in md)
    print("md: E44 PT presente inteiro na linha da forma canonica:", R["md_pt"], "| posicao", k)
    if k >= 0:
        ls = md.rfind("\n", 0, k) + 1
        print("   a linha comeca com:", md[ls:ls + 60].replace("\n", " "))
# PDF -> texto
import fitz
for lang, E in (("pt", E_PT), ("en", E_EN)):
    pdf = os.path.join(D, "dry_v411_%s.pdf" % lang)
    doc = fitz.open(pdf)
    txt = "".join(pg.get_text() for pg in doc)
    open(os.path.join(OUT, "pdf_%s.txt" % lang), "w", encoding="utf-8").write(txt)
    def squash(s):
        s = unicodedata.normalize("NFKC", s).replace("\u00ad", "")
        s = re.sub(r"-\s*\n\s*", "", s)
        return re.sub(r"\s+", "", s)
    sf, ef = squash(txt), squash(E)
    print(lang, "PDF: paginas", len(doc), "| E44 inteiro (sem espacos/hifenizacao) presente:", ef in sf, "| contagem:", sf.count(ef))
    R["pdf_" + lang] = ef in sf
    if ef not in sf:
        # maior prefixo e ultima frase
        lo = 0
        for L in range(20, len(ef), 20):
            if ef[:L] in sf:
                lo = L
            else:
                break
        print("   maior prefixo achado:", lo, "de", len(ef), "| ultimos 60 achados:", ef[-60:] in sf)
json.dump(R, open(os.path.join(OUT, "c6_e44.json"), "w"), indent=1)
