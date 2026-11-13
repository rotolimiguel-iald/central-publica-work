"""CU-F2: o scan da D181 (o MEU, cu_b1) sobre os textos do pos-rito: harness (todas as cadeias), PRONTO_POS_RITO (cadeias), rascunho do X, README projetado, handoff do ensaio."""
import json, os, re, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cu_b1.py"), encoding="utf-8").read()
cut = src.index("alvos = {}")
g = {"__name__": "cu_b1_defs"}
so = sys.stdout
sys.stdout = open(os.devnull, "w")
exec(compile(src[:cut], "cu_b1_defs", "exec"), g)
sys.stdout = so
varrer, strs, TOPO_WIN, V = g["varrer"], g["strs"], g["TOPO_WIN"], g["V"]
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace")
alvos = {
    "harness_textos_json": "\n".join(strs(json.load(open(os.path.join(V, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v411.json"), encoding="utf-8")))),
    "pronto_pos_rito_json": "\n".join(strs(json.load(open(os.path.join(V, "PRONTO_POS_RITO_v411.json"), encoding="utf-8")))),
    "rascunho_do_X": rd(os.path.join(V, "pos_rito", "CUSTODIA_v411_RASCUNHO.txt")),
    "readme_projetado": rd(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\README_PROJETADO_v411.md"),
    "handoff_de_ensaio": rd(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\HANDOFF_v411_CUSTODIA.md"),
    "harness_fechar_json": "\n".join(strs(json.load(open(os.path.join(V, "pos_rito", "HARNESS_FECHAR_SANDBOX_v411.json"), encoding="utf-8")))),
}
for k, t in alvos.items():
    r = varrer(k, t, "", None, TOPO_WIN)
    print("==", k, "chars", r["chars"], "| ocorrencias (inteiro/linha24):", len(r["ocorrencias"]), "| nomes:", len(r["nomes"]), "| janelas excedentes:", r["n_janelas_excedentes"], "(no topo:", sum(1 for j in r["janelas_excedentes"] if j["no_topo"]), ")")
    for o in r["ocorrencias"][:6]:
        print("   OCOR", {k2: o[k2] for k2 in ("fala", "tipo", "forma", "linha", "n_no_alvo", "sha16_agulha", "len")})
    for o in r["nomes"][:6]:
        print("   NOME", o)
    for j in r["janelas_excedentes"][:8]:
        print("   JANELA", j)
