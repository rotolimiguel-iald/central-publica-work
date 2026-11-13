"""CU-B4: quadro sem o item da fala do autor; linha da v411 no stdout; docstring; core cunhagens_v411; veredito; decisoes e erratas."""
import ast, hashlib, json, os, re, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sha256 = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace")
R = {}
alv = {"pt_tex": (r"C:\t\k411c\dry_v411\dry_v411_pt.tex", "um_absoluto_pt.tex"), "pt_txt": (r"C:\t\k411c\dry_v411\dry_v411_pt.txt", "um_absoluto_pt.txt"),
       "en_tex": (r"C:\t\k411c\dry_v411\dry_v411_en.tex", "um_absoluto_en.tex"), "en_txt": (r"C:\t\k411c\dry_v411\dry_v411_en.txt", "um_absoluto_en.txt"),
       "forma_canonica_md": (r"C:\t\k411c\falso_nos_v411\um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), "manifesto_md": (r"C:\t\k411c\falso_nos_v411\um_absoluto_manifest.md", "um_absoluto_manifest.md")}
rot = ["A fala do autor", "The author's words", "The author\u2019s words", "fala_do_autor_para_o_quadro", "FALA_DO_AUTOR", "testemunho do autor", "the author's test"]
for k, (a, b) in alv.items():
    ta, tb = rd(a), rd(os.path.join(NOS, b))
    R["rotulos_" + k] = {r: (ta.count(r), tb.count(r)) for r in rot}
    print("rotulos (novo, v410):", k, R["rotulos_" + k])
# o quadro novo: titulo
for k in ("pt_txt", "en_txt"):
    ta = rd(alv[k][0])
    i = ta.find("H0DN")
    print(k, "H0DN primeira ocorrencia na posicao", i)
# linha da v411 na saida do rito
so = rd(r"C:\t\k411c\falso_nos_v411\rodada_v411_stdout.txt")
linhas = [l for l in so.splitlines() if "v411" in l and "H0DN" in l]
print("stdout: linhas com v411 e H0DN:", len(linhas))
for l in linhas:
    print("   len", len(l), "sha16", hashlib.sha256(l.encode()).hexdigest()[:16], "| aspas angulares:", ("\u00ab" in l or "\u00bb" in l), "| 'citada por data e sha16':", "citada por data e sha16" in l,
          "| sha16 citado:", re.findall(r"sha16 ([0-9a-f]{16})", l), "| 'nao transcrita':", "nao transcrita" in l)
cand = rd(os.path.join(V, "um_v411_candidato.py"))
# docstring do h0dn_bg1_v411
t = ast.parse(cand)
for n in t.body:
    if isinstance(n, ast.FunctionDef) and n.name == "h0dn_bg1_v411":
        ds = ast.get_docstring(n, clean=False)
        i = ds.find("a ordem do operador")
        print("docstring h0dn_bg1_v411:", len(ds), "| trecho da citacao (primeiros 170 chars a partir de 'a ordem do operador'):", ds[i:i + 170])
        print("   aspas angulares no docstring:", ("\u00ab" in ds or "\u00bb" in ds), "| marcador __SHA16 residual:", "__SHA16" in ds)
# core
core = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]
cu = core["cunhagens_v411"]
print("cunhagens_v411 keys:", list(cu.keys()))
vb = cu["verbatim"]
print("verbatim: n", len(vb), "| tipos", {type(v).__name__ for v in vb.values()})
chaves = sorted({k for v in vb.values() for k in v})
print("campos dos itens:", chaves)
print("citado_por_sha256 todos True:", all(v.get("citado_por_sha256") is True for v in vb.values()), "| texto_transcrito todos False:", all(v.get("texto_transcrito") is False for v in vb.values()))
VC = json.load(open(os.path.join(V, "VERBATIM_CONGELADO_v411.json"), encoding="utf-8"))
sh_arq = {}
for r in VC["registro"]:
    sh_arq[sha256(open(r["arquivo"], "rb").read())] = r["papel"]
sh_core = {v["sha256"]: v for v in vb.values()}
print("os 11 sha256 do core == os 11 sha256 dos arquivos lidos agora:", set(sh_core) == set(sh_arq), len(sh_core), len(sh_arq))
print("chave == v411_cun_ + sha16 do sha256:", all(k == "v411_cun_" + v["sha256"][:16] for k, v in vb.items()))
print("quando por item:", sorted({v["quando"] for v in vb.values()}), "| autor:", sorted({v["autor"] for v in vb.values()}))
print("papel do core == papel da lista da casa:", all(v["papel"] == sh_arq[v["sha256"]] for v in vb.values()))
js = json.dumps(cu, ensure_ascii=False)
print("cunhagens_v411: 'OPERADOR_' ocorrencias:", js.count("OPERADOR_"), "| '.txt':", js.count(".txt"), "| 'verbatim.txt':", js.count("verbatim"), "| 'trecho':", js.count('"trecho"'), "| 'texto':", len(re.findall(r'"texto"\s*:', js)))
ex = cu.get("extras", {})
print("extras keys:", list(ex.keys()))
print("extras.falas_citadas n:", len(ex.get("falas_citadas", [])), "| campos:", sorted({k for v in ex.get("falas_citadas", []) for k in v}), "| n_falas:", ex.get("n_falas"), "| autores keys:", sorted(ex.get("autores", {}).keys())[:2])
print("verdict:", cu.get("verdict", "")[:400])
print("all_verified:", cu.get("all_verified"))
# veredito do registro h0dn
r4 = core["h0dn_bg1_v411"]
print("h0dn veredito tem ORDERS... :", [m for m in ("OPERATOR_ORDERS", "CITED_BY_DATE_AND_SHA256", "NOT_TRANSCRIBED", "EMBEDDED_VERBATIM") if m in cu.get("verdict", "")])
print("decisoes (n):", len(r4["decisoes"]), sorted(r4["decisoes"].keys()), "| erratas:", [e["id"] for e in r4["erratas"]])
print("spec: decisoes/erratas em cunhagens extras:", len(ex.get("decisoes", {})), ex.get("erratas_ids"))
print("h0dn falas (contrato) campos:", sorted({k for f in r4.get("falas", [])[:1] for k in f}) if "falas" in r4 else "sem chave falas no registro")
print("h0dn keys com 'fala':", [k for k in r4 if "fala" in k])
