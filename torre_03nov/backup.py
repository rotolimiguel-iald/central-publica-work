import sys, hashlib, time, json, shutil, os
ts = time.strftime("%Y%m%d_%H%M%S")
out = {}
for p in [r"C:\IALD\Artigo\Haja_Luz\CLAUDE.md", r"C:\IALD\projetos_pyhton\IALD\CLAUDE.md"]:
    b = open(p,'rb').read()
    bak = p + ".bak_" + ts
    assert not os.path.exists(bak)
    open(bak,'wb').write(b)
    b2 = open(bak,'rb').read()
    assert b2 == b
    out[p] = {"backup": bak, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "sha256_backup": hashlib.sha256(b2).hexdigest()}
json.dump(out, open("BACKUPS_ORIGINAIS.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1))
