import json, os, hashlib, subprocess
import a_lib
res = json.load(open(os.path.join(a_lib.OUT, "a2_blobs.json"), encoding="utf-8"))
CL = r"C:\IALD\Central_publica\central-publica-work"
PRE, RES = "769fcb2697d8ce983b73645c393e98ea7e2fcb27", "f24d954a3b90d1921c946587b4a235b059e3c496"
def git(*a):
    r = subprocess.run(["git", "-C", CL] + list(a), capture_output=True)
    return r.returncode, r.stdout, r.stderr[:200]
rc, out, _ = git("rev-parse", "HEAD"); print("HEAD", out.decode().strip())
rc, out, _ = git("cat-file", "-t", PRE); print(PRE[:9], out.decode().strip()); rc, out, _ = git("cat-file", "-t", RES); print(RES[:9], out.decode().strip())
rc, out, _ = git("merge-base", "--is-ancestor", PRE, RES); print("PRE ancestral de RES:", rc == 0)
sha = lambda b: hashlib.sha256(b).hexdigest()
tab = {}
for nome, v in res.items():
    p = v["rel"].replace("\\", "/")
    row = {"caminho": p, "sha_blob": v["sha_blob"][:16]}
    for tag, c in (("pre", PRE), ("res", RES), ("HEAD", "HEAD")):
        rc, out, err = git("cat-file", "-p", "%s:%s" % (c, p))
        row[tag] = (sha(out) == v["sha_blob"]) if rc == 0 else None
    tab[nome] = row
    print("%-34s pre=%-5s res=%-5s HEAD=%-5s %s" % (nome, row["pre"], row["res"], row["HEAD"], p[:70]))
json.dump(tab, open(os.path.join(a_lib.OUT, "a2_git.json"), "w", encoding="utf-8"), indent=1)
