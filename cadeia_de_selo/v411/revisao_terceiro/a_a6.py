"""A6: as 11 falas embutidas == os arquivos OPERADOR_*.txt (bytes), autoria; os 6(8) textos da gerencia so' por sha256; nenhuma fala FORA entrou; guarda de material privado; kimi."""
import hashlib, json, os, re, glob
import a_lib
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_VERBATINS2", "_V411_FONTES"])
VB, FT = ns["_V411_VERBATINS2"], ns["_V411_FONTES"]
V = a_lib.V
CG = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
sha = lambda b: hashlib.sha256(b).hexdigest()
cong = json.load(open(os.path.join(V, "VERBATIM_CONGELADO_v411.json"), encoding="utf-8"))
print("congelado: n", cong["n"], "| registro", len(cong["registro"]), "| chaves", list(cong.keys()))
print("VERBATINS2 n:", len(VB), "| chaves:", list(VB.keys())[:3], "...")
lista = {os.path.basename(r["arquivo"]): r for r in cong["registro"]}
ok_total = True
for k, v in VB.items():
    nome = os.path.basename(v["fonte_original"])
    p = os.path.join(CG, nome)
    b = open(p, "rb").read()
    txt = b.decode("utf-8")
    cp = os.path.join(V, "insumos", "cunhagens", nome)
    cpok = os.path.exists(cp) and open(cp, "rb").read() == b
    row = {"id_ok": k == "v411_cun_" + sha(b)[:16], "sha_ok": v["sha256"] == sha(b), "bytes_ok": v["bytes"] == len(b), "text_eq_arquivo": v["text"] == txt, "text_eq_strip": v["text"] == txt.strip(), "autor": v["autor"],
           "na_lista_congelada": nome in lista and lista[nome]["sha256"] == sha(b) and lista[nome]["autor"] == "operador", "copia_do_insumo_igual": cpok, "embutido": v.get("texto_embutido"), "ntrechos": len(v.get("trechos") or []),
           "trechos_em_text": all(t in v["text"] for t in v.get("trechos") or [])}
    ok = all(x for kk, x in row.items() if kk in ("id_ok", "sha_ok", "bytes_ok", "na_lista_congelada", "copia_do_insumo_igual", "trechos_em_text")) and row["autor"] == "operador" and (row["text_eq_arquivo"] or row["text_eq_strip"])
    ok_total &= ok
    print("%-100s ok=%s %s" % (nome[:100], ok, {kk: x for kk, x in row.items() if x is not True}))
print("11 falas todas ok:", ok_total and len(VB) == 11 and len(cong["registro"]) == 11)
print("falas da lista congelada nao embutidas:", [n for n in lista if not any(os.path.basename(v["fonte_original"]) == n for v in VB.values())])
# as FORA: todas as OPERADOR_11nov*/12nov* (e as demais datas?) que NAO estao na lista: texto/nome/sha no candidato?
cand = open(a_lib.CAND, "rb").read().decode("utf-8")
fora = [p for p in glob.glob(os.path.join(CG, "OPERADOR_1[12]nov*.txt")) if os.path.basename(p) not in lista]
print("candidatas FORA (11 e 12/11 nao listadas):", len(fora))
for p in fora:
    b = open(p, "rb").read(); t = b.decode("utf-8").strip()
    nome = os.path.basename(p)
    em_texto = (t in cand) if len(t) >= 15 else None
    # trechos de 40 chars (inicio, meio, fim)
    ex = [t[:40], t[len(t) // 2 - 20:len(t) // 2 + 20], t[-40:]] if len(t) > 80 else [t]
    em_trechos = [e in cand for e in ex]
    print("  FORA %-95s texto_inteiro_no_candidato=%s trechos=%s nome_no_candidato=%s sha16_no_candidato=%s" % (nome[:95], em_texto, em_trechos, nome in cand, sha(b)[:16] in cand))
# os textos da gerencia: so' sha; o texto nao esta embutido
ger = sorted(glob.glob(os.path.join(CG, "GERENCIA_1[12]nov*.json")))
print("GERENCIA_*:", len(ger))
for p in ger:
    b = open(p, "rb").read(); nome = os.path.basename(p)
    d = json.loads(b.decode("utf-8"))
    campos = [str(v) for v in d.values() if isinstance(v, str) and len(v) > 60]
    emb = any(c[:50] in cand for c in campos)
    print("  GER %-100s sha16=%s sha16_no_cand=%s nome_no_cand=%s texto_no_cand=%s" % (nome[:100], sha(b)[:16], sha(b)[:16] in cand, nome in cand, emb))
json.dump({"ok_total": bool(ok_total)}, open(os.path.join(a_lib.OUT, "a6.json"), "w"))
