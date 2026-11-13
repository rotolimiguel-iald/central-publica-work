"""CU-C9: (7) caracteres especiais do TeX nos textos novos; nenhum texto novo cortado no PDF (a ultima frase de cada paragrafo novo presente no texto extraido)."""
import os, re, unicodedata, json
D = r"C:\t\k411c\dry_v411"
OUT = r"C:\t\k411c\revisao_CU"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
PAR = re.compile(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*")
R = {}


def especiais(p):
    """acha especiais NAO escapados, fora de math ($...$) e fora de comandos conhecidos."""
    q = re.sub(r"\$[^$]*\$", " ", p)          # tira math
    achados = {}
    for nome, rx in (("%", r"(?<!\\)%"), ("&", r"(?<!\\)&"), ("#", r"(?<!\\)#"), ("_", r"(?<!\\)_"), ("^", r"(?<!\\)\^"), ("~", r"(?<!\\)~")):
        n = len(re.findall(rx, q))
        if n:
            achados[nome] = n
    # chaves balanceadas
    nivel = 0
    ok = True
    for ch in re.sub(r"\\[{}]", "", p):
        if ch == "{":
            nivel += 1
        elif ch == "}":
            nivel -= 1
            if nivel < 0:
                ok = False
    if nivel != 0:
        ok = False
    if not ok:
        achados["chaves_desbalanceadas"] = nivel
    # numero impar de cifroes (math aberto)
    if len(re.findall(r"(?<!\\)\$", p)) % 2:
        achados["cifrao_impar"] = 1
    return achados


def alnum(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[\W_]+", "", s).lower()


pdf = {l: alnum(open(os.path.join(OUT, "pdf_%s.txt" % l), encoding="utf-8").read()) for l in ("pt", "en")}
for lang in ("pt", "en"):
    tn = rd(os.path.join(D, "dry_v411_%s.tex" % lang))
    tv = rd(os.path.join(NOS, "um_absoluto_%s.tex" % lang))
    pv = {m.group(0) for m in PAR.finditer(tv)}
    novos = [m for m in PAR.finditer(tn) if m.group(0) not in pv and len(m.group(0)) < 60000]
    esp = []
    cortes = []
    for m in novos:
        p = m.group(0)
        e = especiais(p)
        if e:
            esp.append((m.start(), e, p[:60].replace("\n", " ")))
        # ultima frase: sem math, sem comandos
        q = p
        q = re.sub(r"\\(?:begin|end)\{[^}]*\}", " ", q)
        q = re.sub(r"\\(?:vspace|hspace)\*?\{[^}]*\}", " ", q)
        q = re.sub(r"\\\\(?:\[[^\]]*\])?", " ", q)
        q = re.sub(r"\$[^$]*\$", "\x00", q)
        q = q.split("\x00")[-1]
        q = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", q)
        q = q.replace("{", " ").replace("}", " ").replace("\\", " ")
        a = alnum(q)
        if len(a) >= 30:
            tail = a[-30:]
            if tail not in pdf[lang]:
                cortes.append((m.start(), len(p), p[:60].replace("\n", " "), p[-50:].replace("\n", " ")))
    R[lang] = {"novos_ou_alterados": len(novos), "com_especial_nao_escapado": len(esp), "cauda_ausente_no_pdf": len(cortes)}
    print("==", lang, R[lang])
    for x in esp[:10]:
        print("   ESPECIAL", x)
    for x in cortes[:10]:
        print("   CAUDA NAO ACHADA NO PDF", x)
json.dump(R, open(os.path.join(OUT, "c9_tex.json"), "w"), indent=1)
