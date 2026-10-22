import os, re, hashlib, sys, json
sys.stdout.reconfigure(encoding="utf-8")
C = "C:" + os.sep
LEV = os.path.join(C, "IALD", "Central de Patentes", "work", "levantamento_chatgpt_19out", "LEVANTAMENTO_CHATGPT.md")
T = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019")
W = os.path.join(C, "IALD", "Central de Patentes", "work", "cunhagens_13out")
txt = open(LEV, encoding="utf-8").read()
sec = txt.split("### b.1")[1].split("### b.2")[0]
alvo = re.findall(r"`([0-9a-f]{16})`", sec)
sec2 = txt.split("### b.2")[1].split("Nota: o PENDENCIAS")[0]
alvo2 = re.findall(r"`([0-9a-f]{16})`", sec2)
print("b1", len(alvo), "b2", len(alvo2))
want = set(alvo) | set(alvo2)
found = {}
roots = [T, W]
cnt = 0
pat = re.compile(r"(verbatim|origem|operator|operador|OPERADOR|ORIGEM|VERBATIM)", re.I)
for root in roots:
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".lake", "orbital_rotation", "tgl_kernel", "__pycache__")]
        for f in fn:
            if not (f.lower().endswith((".txt", ".json", ".md"))):
                continue
            if not pat.search(f) and not pat.search(os.path.basename(dp)):
                continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 3_000_000:
                    continue
                b = open(p, "rb").read()
            except OSError:
                continue
            cnt += 1
            h = hashlib.sha256(b).hexdigest()
            if h[:16] in want:
                found.setdefault(h[:16], []).append(p)
print("arquivos lidos", cnt)
for s in alvo + alvo2:
    print(s, "ACHADO" if s in found else "----", (found.get(s) or [""])[0][len(T):][:140])
json.dump({"b1": alvo, "b2": alvo2, "achados": found}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cunhagens_achadas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
