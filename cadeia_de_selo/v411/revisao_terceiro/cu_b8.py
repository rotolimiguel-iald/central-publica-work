"""CU-B8: os nomes GERENCIA_1xnov_* (textos da gerencia a que o operador respondeu; D181 manda citar por data e sha256): onde aparecem nos alvos renderizados e no core."""
import json, os, re
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace")
pat = re.compile(r"GERENCIA_1[0-2]nov[A-Za-z0-9_\u00c0-\u00ff]*")
alvos = {"pt_txt": r"C:\t\k411c\dry_v411\dry_v411_pt.txt", "en_txt": r"C:\t\k411c\dry_v411\dry_v411_en.txt", "pt_tex": r"C:\t\k411c\dry_v411\dry_v411_pt.tex", "en_tex": r"C:\t\k411c\dry_v411\dry_v411_en.tex",
         "forma_canonica": r"C:\t\k411c\falso_nos_v411\um_absoluto_forma_canonica.md", "manifesto": r"C:\t\k411c\falso_nos_v411\um_absoluto_manifest.md", "stdout": r"C:\t\k411c\falso_nos_v411\rodada_v411_stdout.txt"}
for k, p in alvos.items():
    print(k, len(pat.findall(rd(p))))
core = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]


def walk(x, p):
    if isinstance(x, str):
        for m in pat.finditer(x):
            print("CORE", p[:100], "| ctx len", len(x), "| nome sha-prefix:", m.group(0)[:30])
    elif isinstance(x, dict):
        for k, v in x.items():
            walk(k, p + "/<key>")
            walk(v, p + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, p + "[%d]" % i)


walk(core, "core")
