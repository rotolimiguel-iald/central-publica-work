import json, sys
core = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json", encoding="utf-8"))
def walk(o, path, want, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if any(w.lower() in k.lower() for w in want):
                acc.append((path + "/" + k, v))
            walk(v, path + "/" + k, want, acc)
    elif isinstance(o, list):
        for i, v in enumerate(o[:50]):
            walk(v, f"{path}[{i}]", want, acc)
want = sys.argv[1].split(",")
acc = []
walk(core, "", want, acc)
for p, v in acc[:40]:
    s = json.dumps(v, ensure_ascii=False)
    print(p, "=>", s[:int(sys.argv[2]) if len(sys.argv) > 2 else 600])
    print()
