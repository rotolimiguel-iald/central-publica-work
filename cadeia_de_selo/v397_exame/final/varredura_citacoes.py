# -*- coding: utf-8 -*-
"""varredura_citacoes.py -- exame final v397 (c1, 23/10/2026), item (4) ampliado: FIDELIDADE DE CITACAO POR BYTES. Toda passagem entre aspas («...», ``...'', "...", '...')
nas superficies NOVAS da v397 (as linhas novas do candidato v396->v397; o quadro e a secao v397 do artigo PT/EN; o .md do ensaio; pos_rito/textos_v397.py; o handoff do harness, se existir)
e' procurada, byte a byte apos normalizacao de espacos, no CORPUS dos verbatins do operador (work\\cunhagens_13out\\OPERADOR_*_verbatim.txt) e no Atlas (verbete Psibit).
Cada citacao sai classificada: VERBATIM_OPERADOR (arquivo), ATLAS, ou NAO_ENCONTRADA -- e, para as nao encontradas, o contexto diz se a frase e' ATRIBUIDA ao operador.
So le. uso: python -I -B -X utf8 varredura_citacoes.py [<um_candidato.py>]  (padrao: o candidato da pasta v397)"""
import glob, json, os, re, sys, io, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397"
CAND = sys.argv[1] if len(sys.argv) > 1 else os.path.join(V, "um_v397_candidato.py")
NOS_UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CORP = {}
for p in glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_*_verbatim.txt"):
    CORP[os.path.basename(p)] = open(p, "rb").read().decode("utf-8")
ATLAS = open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", "rb").read().decode("utf-8", "replace").replace("**", "")
def norm(s):
    s = unicodedata.normalize("NFC", s).replace("\u00a0", " ").replace("\r\n", "\n")
    s = s.replace("``", "«").replace("''", "»").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\\(?=[_&%#])", "", s)          # TeX escapes
    s = s.replace("---", "—").replace("--", "–")
    return re.sub(r"\s+", " ", s).strip()
CORPN = {k: norm(v) for k, v in CORP.items()}; ATLN = norm(ATLAS)
ATRIB = re.compile(r"operador|operator|verbatim|fala|cunhag|disse|said|sha16", re.I)
def classifica(q):
    qn = norm(q)
    for k, v in CORPN.items():
        if qn and qn in v:
            return "VERBATIM_OPERADOR", k
    if qn and qn in ATLN:
        return "ATLAS", "TGL_ATLAS.md"
    return "NAO_ENCONTRADA", None
def quotes(texto):
    out = []
    for m in re.finditer(r"«([^«»]{12,400})»", texto):
        out.append((m.group(1), texto[max(0, m.start() - 220):m.end() + 160]))
    for m in re.finditer(r"``([^`']{12,400})''", texto):
        out.append((m.group(1), texto[max(0, m.start() - 220):m.end() + 160]))
    for m in re.finditer(r"(?<![A-Za-z])'([^'\n]{18,300})'(?![A-Za-z])", texto):   # frases em aspas simples (limites/leituras): so' nas linhas que falam do operador
        s = m.group(1)
        ini = texto.rfind("\n", 0, m.start()) + 1; fim = texto.find("\n", m.end()); linha = texto[ini:(fim if fim > 0 else len(texto))]
        if re.search(r"[A-Za-z]{3}", s) and not re.search(r"[_{}\\/]|\.(json|py|lean|md|txt)|^[0-9a-f]{16,}$", s) and re.search(r"operador|operator", linha, re.I):
            out.append((s, texto[max(0, m.start() - 220):m.end() + 160]))
    return out
def novas_do_candidato():
    """as linhas NOVAS do candidato (contra o um.py instalado) FORA do corpo do kernel embutido, das bandeiras e do indice do arquivo da bancada"""
    import ast, difflib
    src_b = open(CAND, "rb").read().decode("utf-8"); a = open(NOS_UM, "rb").read().decode("utf-8").splitlines(); b = src_b.splitlines()
    T = ast.parse(src_b); excl = set()
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) in ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "_BENCH_ARCHIVE_V361_INDEX"):
            excl.update(range(n.lineno, n.end_lineno + 1))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    nov = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "insert"):
            nov += [b[j] for j in range(j1, j2) if (j + 1) not in excl]
    return "\n".join(nov)
SUP = {"candidato_linhas_novas": novas_do_candidato()}
for lang in ("pt", "en"):
    t = open(os.path.join(V, "dry_v397", "dry_v397_%s.txt" % lang), encoding="utf-8").read()
    tit = "O Teste da Única Palavra" if lang == "pt" else "The Test of the Only Word"
    i0 = t.find(tit); i1 = t.find("E se o problema da unificação" if lang == "pt" else "What if the unification problem")
    j0 = t.find(tit, i1 if i1 > 0 else 0)            # a secao v397 do corpo
    j1 = t.find("A testemunha estática: o psion habita a fronteira" if lang == "pt" else "The static witness: the psion inhabits the frontier", j0 + 10)
    SUP["artigo_%s_quadro" % lang] = t[i0:i1] if 0 <= i0 < i1 else ""
    SUP["artigo_%s_secao_v397" % lang] = t[j0:j1] if 0 <= j0 < j1 else t[j0:j0 + 9000] if j0 >= 0 else ""
md = open(os.path.join(V, "dry_v397", "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
SUP["md_ensaio"] = "\n".join(l for l in md.splitlines() if "v397" in l or "Única Palavra" in l or l.startswith(">"))
SUP["pos_rito_textos_v397"] = open(os.path.join(V, "pos_rito", "textos_v397.py"), encoding="utf-8").read()
for nome_h, hp in (("handoff_preparador", os.path.join(V, "pos_rito", "harness_saida_v397", "fechar_sandbox_resultado", "handoff-v397-custodia.md")),
                   ("handoff_exame_memory", os.path.join(H, "..", "sb2", "memory", "handoff-v397-custodia.md")),
                   ("handoff_exame_nos", os.path.join(H, "..", "sb2", "nos", "HANDOFF_v397_CUSTODIA.md"))):
    if os.path.exists(hp):
        SUP[nome_h] = open(hp, encoding="utf-8").read()
# tudo o que o fechar do sandbox (sb2, minha copia do pacote novo) escreveu de texto: memoria, Nos e o topico novo
for raiz in (os.path.join(H, "..", "sb2", "memory"),):
    for p in sorted(glob.glob(os.path.join(raiz, "*.md"))):
        if os.path.basename(p) not in ("handoff-v397-custodia.md",):
            SUP["sb2_memory_" + os.path.basename(p)[:40]] = open(p, encoding="utf-8", errors="replace").read()
for p_ in sorted(glob.glob(os.path.join(H, "textos_renderizados_*", "*.txt"))):   # os textos do pos-rito RENDERIZADOS contra o Nos do sandbox (renderizar_textos_sb2.py)
    SUP["render_" + os.path.basename(os.path.dirname(p_))[-3:] + "_" + os.path.basename(p_)[:-4]] = open(p_, encoding="utf-8").read()
import hashlib
CAND16 = hashlib.sha256(open(CAND, "rb").read()).hexdigest()[:16]
R = {"corpus": sorted(CORP), "candidato": CAND, "candidato_sha16": CAND16, "superficies": {}}
nao = []
for nome, texto in SUP.items():
    vistos = {}
    for q, ctx in quotes(texto):
        qn = norm(q)
        if qn in vistos:
            continue
        cls, onde = classifica(q)
        vistos[qn] = {"classe": cls, "onde": onde}
        if cls == "NAO_ENCONTRADA":
            cn = norm(ctx)
            # a forma ADMITIDA pela gerencia (23/10, depois da ratificacao do operador): «leitura ratificada pelo operador em 23/10 (sha16 782c7e77...) sobre a fala dele (sha16 f3e24a8c...)»
            # ou a marca explicita de COMPOSICAO da gerencia; a forma PROIBIDA segue «o operador disse X» com X fora dos bytes
            admitida = bool(re.search(r"ratific", cn, re.I) and "782c7e77" in cn and "f3e24a8c" in cn) or bool(re.search(r"composi[cç][aã]o da ger[eê]ncia|COMPOSICAO DA GERENCIA|management'?s composition|COMPOSITION by the management", cn, re.I))
            proibida = bool(re.search(r"(operador|operator)\s+(disse|said|escreveu|wrote)\s*[:«\"']", cn, re.I)) or (bool(re.search(r"verbatim", cn, re.I)) and not admitida and not re.search(r"n[aã]o (e'|é) verbatim|is not verbatim", cn, re.I))
            nao.append({"superficie": nome, "citacao": q[:200], "atribuida_ao_operador_no_contexto": bool(ATRIB.search(ctx)), "forma_admitida_ou_composicao_marcada": admitida, "forma_proibida_operador_disse_ou_verbatim": proibida, "contexto": cn[:420]})
    R["superficies"][nome] = {"n_citacoes": len(vistos), "verbatim_operador": sum(1 for v in vistos.values() if v["classe"] == "VERBATIM_OPERADOR"), "atlas": sum(1 for v in vistos.values() if v["classe"] == "ATLAS"),
                              "nao_encontradas": sum(1 for v in vistos.values() if v["classe"] == "NAO_ENCONTRADA")}
R["nao_encontradas"] = nao
R["nao_encontradas_atribuidas_ao_operador"] = [x for x in nao if x["atribuida_ao_operador_no_contexto"]]
R["forma_proibida"] = [x for x in nao if x["forma_proibida_operador_disse_ou_verbatim"]]
R["sem_forma_admitida_e_atribuidas"] = [x for x in nao if x["atribuida_ao_operador_no_contexto"] and not x["forma_admitida_ou_composicao_marcada"]]
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(H, "VARREDURA_CITACOES_%s.json" % CAND16), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
