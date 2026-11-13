import json, re
core = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]
cu = core["cunhagens_v411"]


def walk(x, p):
    if isinstance(x, str):
        for m in re.finditer(r"\.txt|verbatim", x):
            print(p, "| len", len(x), "|", repr(x[max(0, m.start() - 90):m.end() + 40]))
    elif isinstance(x, dict):
        for k, v in x.items():
            walk(k, p + "/<key>")
            walk(v, p + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, p + "[%d]" % i)


walk(cu, "cunhagens_v411")
# a mesma consulta em todo o core: quantas strings com 'verbatim.txt'
n = 0


def w2(x, p):
    global n
    if isinstance(x, str):
        if "verbatim.txt" in x or "_verbatim" in x:
            n += 1
            if n <= 12:
                print("CORE", p[:90], "|", repr(x[:60]))
    elif isinstance(x, dict):
        for k, v in x.items():
            w2(k, p + "/<key>")
            w2(v, p + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            w2(v, p + "[%d]" % i)


w2(core, "core")
print("strings do core com verbatim.txt:", n)
