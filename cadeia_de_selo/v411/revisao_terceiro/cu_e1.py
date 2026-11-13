"""CU-E1: para cada um dos 29 arquivos com backup *_r1fix: sha16 do backup e do arquivo de hoje, contagem de linhas +/-; e a guarda de nao-transcricao: linhas com nome de fala ou agulha sao omitidas na impressao (nunca gravo texto de fala).
uso: python cu_e1.py            -> tabela
     python cu_e1.py <arquivo>  -> diff -U0 (abreviado) so' desse arquivo, no terminal"""
import difflib, glob, hashlib, os, re, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
bks = sorted(glob.glob(os.path.join(V, "**", "*r1fix*"), recursive=True))
bks = [b for b in bks if os.sep + "revisao_terceiro" + os.sep not in b]
pares = []
for b in bks:
    orig = re.sub(r"\.bak_\d{8}_\d{6}_r1fix$", "", b)
    pares.append((os.path.relpath(orig, V).replace("\\", "/"), b, orig))
if len(sys.argv) == 1:
    print("n pares:", len(pares))
    for rel, b, o in pares:
        a = open(b, "rb").read().decode("utf-8", "replace").splitlines()
        c = open(o, "rb").read().decode("utf-8", "replace").splitlines()
        sm = difflib.SequenceMatcher(None, a, c, autojunk=False) if len(a) + len(c) < 8000 else None
        if sm is None:
            sa, sc = set(a), set(c)
            rem = sum(1 for x in a if x not in sc)
            add = sum(1 for x in c if x not in sa)
        else:
            rem = add = 0
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op in ("replace", "delete"):
                    rem += i2 - i1
                if op in ("replace", "insert"):
                    add += j2 - j1
        print("%-46s bak %s -> hoje %s | linhas removidas/alteradas %4d | acrescentadas %4d | tam %d -> %d" % (rel, sha16(b), sha16(o), rem, add, os.path.getsize(b), os.path.getsize(o)))
else:
    alvo = sys.argv[1]
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 240
    for rel, b, o in pares:
        if rel == alvo:
            a = open(b, "rb").read().decode("utf-8", "replace").splitlines()
            c = open(o, "rb").read().decode("utf-8", "replace").splitlines()
            omit = 0
            for ln in difflib.unified_diff(a, c, lineterm="", n=0):
                if ln.startswith(("---", "+++")):
                    continue
                if "OPERADOR_" in ln:
                    omit += 1
                    print(ln[:1], "[linha com nome de fala omitida; sha16 %s]" % hashlib.sha256(ln.encode()).hexdigest()[:10])
                    continue
                print(ln if len(ln) <= lim else ln[:lim] + " ...[+%d]" % (len(ln) - lim))
            print("(omitidas por nome de fala: %d)" % omit)
