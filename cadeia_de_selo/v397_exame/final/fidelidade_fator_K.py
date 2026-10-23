# -*- coding: utf-8 -*-
"""fidelidade_fator_K.py -- exame final v397 (c1, 23/10/2026), delta do candidato NOVO: fidelidade de citacao POR BYTES, depois da ratificacao do operador.
(1) as STRINGS NOVAS do candidato (constantes do AST que nao existem no um.py instalado -- assim os literais partidos em duas linhas voltam a ser uma frase), os textos do
pos-rito RENDERIZADOS contra o Nos do sandbox, o handoff do sandbox, o artigo PT/EN e o .md do ensaio: toda citacao «...» / ``...'' / "..." atribuida ao operador tem de ser
SUBSTRING dos bytes de um OPERADOR_*_verbatim.txt (ou da linha do Atlas); (2) cada ocorrencia da leitura do fator K tem de vir na FORMA ADMITIDA (ratificada pelo operador,
sha16 782c7e77 da ratificacao e f3e24a8c da fala); (3) nenhuma FORMA PROIBIDA («o operador disse X» com X fora dos bytes). So le; grava so' o JSON nesta pasta."""
import ast, glob, json, os, re, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397"
CAND = os.path.join(V, "um_v397_candidato.py"); NOS_UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2009", " ").replace("\xa0", " ")).strip()
CORP = {os.path.basename(p): norm(open(p, "rb").read().decode("utf-8")) for p in glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_*_verbatim.txt")}
ATL = norm(open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", "rb").read().decode("utf-8", "replace").replace("**", ""))
def strings(src):
    out = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Constant) and isinstance(n.value, str): out.add(n.value)
        elif isinstance(n, ast.JoinedStr):
            out.add("".join(v.value if isinstance(v, ast.Constant) else "{…}" for v in n.values))
    return out
cb = open(CAND, "rb").read().decode("utf-8"); nb = open(NOS_UM, "rb").read().decode("utf-8")
emb_txt = set()
for n in ast.parse(cb).body:   # o corpo do kernel embutido sai (nao e' texto da cadeia)
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) in ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "_BENCH_ARCHIVE_V361_INDEX"):
        emb_txt |= {x.value for x in ast.walk(n) if isinstance(x, ast.Constant) and isinstance(x.value, str)}
novas = sorted(strings(cb) - strings(nb) - emb_txt)
SUP = {"candidato_strings_novas": "\n\n".join(novas)}
tx = open(os.path.join(V, "pos_rito", "textos_v397.py"), "rb").read().decode("utf-8")
SUP["textos_v397_strings"] = "\n\n".join(sorted(strings(tx)))
for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_388", "*.txt"))):
    SUP["render_" + os.path.basename(p)[:-4]] = open(p, encoding="utf-8").read()
for nome, p in (("handoff_sb2_memory", os.path.join(H, "..", "sb2", "memory", "handoff-v397-custodia.md")), ("handoff_sb2_nos", os.path.join(H, "..", "sb2", "nos", "HANDOFF_v397_CUSTODIA.md")),
                ("artigo_pt", os.path.join(V, "dry_v397", "dry_v397_pt.txt")), ("artigo_en", os.path.join(V, "dry_v397", "dry_v397_en.txt")), ("artigo_pt_tex", os.path.join(V, "dry_v397", "dry_v397_pt.tex")),
                ("artigo_en_tex", os.path.join(V, "dry_v397", "dry_v397_en.tex")), ("md_ensaio", os.path.join(V, "dry_v397", "um_absoluto_forma_canonica.md"))):
    SUP[nome] = open(p, encoding="utf-8", errors="replace").read()
# nos textos herdados (o artigo e o .md trazem o acervo inteiro), so' os paragrafos da v397
for k in ("artigo_pt", "artigo_en", "artigo_pt_tex", "artigo_en_tex", "md_ensaio"):
    SUP[k] = "\n\n".join(p for p in re.split(r"\n\s*\n", SUP[k]) if re.search(r"v397|23/10/2026|Única Palavra|Only Word|fator K|factor \$?K|Token|token", p))
QRX = [r"«([^«»]{3,400})»", r"``([^`']{3,400})''", r"“([^“”]{3,400})”"]
ATRIB = re.compile(r"operador|operator|verbatim|fala d|his saying|nas palavras|in his", re.I)
PROIB = re.compile(r"(o operador|the operator)\s+(disse|falou|escreveu|said|wrote|stated)\b", re.I)
KRX = re.compile(r"fator\s*\$?K|factor\s*\$?K", re.I)
R = {"candidato_sha16": hashlib.sha256(cb.encode("utf-8")).hexdigest()[:16], "corpus_n": len(CORP), "n_strings_novas_candidato": len(novas), "superficies": {}, "nao_verbatim_atribuidas": [], "forma_proibida": [], "fator_K": []}
for nome, t in SUP.items():
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    n_q = n_v = 0
    for p in paras:
        pn = norm(p)
        for rx in QRX:
            for m in re.finditer(rx, p):
                q = norm(m.group(1))
                if not re.search(r"[A-Za-zÀ-ú]{3}", q) or "{…}" in q:
                    continue
                n_q += 1
                if any(q in c for c in CORP.values()) or q in ATL:
                    n_v += 1; continue
                ctx = pn[max(0, pn.find(q) - 260): pn.find(q) + len(q) + 160]
                if ATRIB.search(ctx):
                    R["nao_verbatim_atribuidas"].append({"superficie": nome, "citacao": q[:200], "contexto": ctx[:460]})
        for m in PROIB.finditer(pn):
            R["forma_proibida"].append({"superficie": nome, "trecho": pn[max(0, m.start() - 120): m.end() + 200]})
        for m in KRX.finditer(pn):
            ctx = pn[max(0, m.start() - 400): m.end() + 500]
            R["fator_K"].append({"superficie": nome, "ratificada": bool(re.search(r"ratific|RATIFIC", ctx)), "sha_782c7e77": "782c7e77" in ctx, "sha_f3e24a8c": "f3e24a8c" in ctx,
                                 "composicao_dita": bool(re.search(r"composi[cç][aã]o|COMPOSICAO|composition", ctx, re.I)), "trecho": pn[max(0, m.start() - 200): m.end() + 160]})
    R["superficies"][nome] = {"paragrafos": len(paras), "citacoes": n_q, "verbatim_ou_atlas": n_v}
fk = R["fator_K"]
R["fator_K_resumo"] = {"ocorrencias": len(fk), "forma_admitida_completa": sum(1 for x in fk if x["ratificada"] and x["sha_782c7e77"] and x["sha_f3e24a8c"]),
                       "sem_forma_completa": [{"superficie": x["superficie"], "ratificada": x["ratificada"], "782c": x["sha_782c7e77"], "f3e2": x["sha_f3e24a8c"], "trecho": x["trecho"][:330]} for x in fk if not (x["ratificada"] and x["sha_782c7e77"] and x["sha_f3e24a8c"])]}
json.dump(R, open(os.path.join(H, "FIDELIDADE_FATOR_K_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("candidato_sha16", "corpus_n", "n_strings_novas_candidato")}, ensure_ascii=False))
print("superficies:", json.dumps(R["superficies"], ensure_ascii=False)[:2500])
print("FORMA PROIBIDA:", len(R["forma_proibida"]), json.dumps(R["forma_proibida"], ensure_ascii=False)[:1500])
print("NAO VERBATIM ATRIBUIDAS:", len(R["nao_verbatim_atribuidas"]))
for x in R["nao_verbatim_atribuidas"]: print("  -", x["superficie"], "|", x["citacao"][:160], "| CTX:", x["contexto"][:360])
print("FATOR K:", json.dumps({k: v for k, v in R["fator_K_resumo"].items() if k != "sem_forma_completa"}, ensure_ascii=False))
for x in R["fator_K_resumo"]["sem_forma_completa"]: print("  K-", x["superficie"], "| ratif", x["ratificada"], "782c", x["782c"], "f3e2", x["f3e2"], "|", x["trecho"][:330])
