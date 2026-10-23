# -*- coding: utf-8 -*-
"""CONFERÊNCIA FINAL INDEPENDENTE da custódia v396 (22/10/2026, sessão a7; molde: a da v395). O cético mecânico: refaz do zero, sem importar nada da
esteira de custódia, as afirmações que a custódia faz. Só leitura (rede: GET no raw do GitHub e no site). Fail-closed: cada item ok/FALHA.
 1. o selo do Nós: um.py v396 = o pino; o um.py do Nós, do espelho e do cofre têm os mesmos bytes;
 2. o cofre um_unificado_v396: cada artefato que o selo lista e que está no cofre bate com o sha256 do selo;
 3. o cofre tgl_kernel_v396: cada arquivo formal do manifesto de prova bate (1425); nenhuma declaração fora do trio;
 4. o GitHub (raw) serve o um.py e o selo com os bytes do pino; o README raw traz o pino;
 5. o site no ar: o index traz «v396 · <pin16>» e o read-brief/llms citam o pino;
 6. os dois repositórios: HEAD = origin/main, árvore sem mudança rastreada pendente nos caminhos da custódia."""
import hashlib, json, subprocess, sys, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TB = Path(r"C:\IALD\Artigo\the_boundary")
ESP = TB / "Um (absoluto) \u2014 Grande Atrator"
CEN = Path(r"C:\IALD\Central de Patentes")
V, KV = CEN / "vault" / "originals_copy" / "um_unificado_v396", CEN / "vault" / "originals_copy" / "tgl_kernel_v396"
RAW = "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/"
SITE = "https://teoriadagravitacaoluminodinamica.com/"
R = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def item(nome, ok, det=""):
    R.append((nome, bool(ok), det))
    print("%-6s %s %s" % ("ok" if ok else "FALHA", nome, det))


def get(url):
    rq = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "conferencia-final-v396"})
    with urllib.request.urlopen(rq, timeout=180) as r:
        return r.read()


selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
pin = selo["sha256"]["um.py"]
p16 = pin[:16]
b_nos, b_esp, b_cof = (NOS / "um.py").read_bytes(), (ESP / "um.py").read_bytes(), (V / "um.py").read_bytes()
item("1 selo do Nós = v396 e o pino", selo.get("um_version") == "v396" and sha(b_nos) == pin, p16)
item("1 um.py igual no Nós, no espelho e no cofre", sha(b_esp) == pin and sha(b_cof) == pin, "%d bytes" % len(b_nos))
lis = selo["sha256"]
no_cofre = [n for n in lis if (V / n).is_file()]
div = [n for n in no_cofre if sha((V / n).read_bytes()) != lis[n]]
item("2 cofre v396: artefatos do selo presentes conferem", no_cofre and not div, "%d conferidos, %d divergentes, %d do selo fora do cofre" % (len(no_cofre), len(div), len(lis) - len(no_cofre)))
pm = json.loads((KV / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
ff = pm["formal_files_sha256"]
kdiv = [r for r, h in ff.items() if not (KV / r).is_file() or sha((KV / r).read_bytes()) != h]
fora = [k for k, v in pm["axiom_report"].items() if any(x not in ("propext", "Classical.choice", "Quot.sound") for x in (v or []))]
item("3 cofre do kernel: arquivos formais conferem", len(ff) == 1425 and not kdiv, "%d formais, %d divergentes/ausentes" % (len(ff), len(kdiv)))
item("3 axiom_report no trio", len(pm["axiom_report"]) == 29228 and not fora, "%d declarações, %d fora" % (len(pm["axiom_report"]), len(fora)))
from urllib.parse import quote
A3 = "Um (absoluto) \u2014 Grande Atrator/"
try:
    gu = get(RAW + quote(A3 + "um.py"))
    gs = get(RAW + quote(A3 + "um_absoluto_selo.json"))
    gr = get(RAW + "README.md").decode("utf-8", "replace")
    item("4 GitHub raw: um.py = pino", sha(gu) == pin, "%d bytes" % len(gu))
    item("4 GitHub raw: selo = o selo do Nós", sha(gs) == sha((NOS / "um_absoluto_selo.json").read_bytes()))
    item("4 GitHub raw: README traz o pino", p16 in gr)
except Exception as e:  # noqa: BLE001
    item("4 GitHub raw", False, repr(e)[:160])
try:
    si = get(SITE).decode("utf-8", "replace")
    sb = get(SITE + "read-brief.md").decode("utf-8", "replace")
    sl = get(SITE + "llms.txt").decode("utf-8", "replace")
    item("5 site no ar: index com «v396 · pin16»", ("v396 \u00b7 " + p16) in si)
    item("5 site no ar: read-brief e llms citam o pino", p16 in sb and p16 in sl)
except Exception as e:  # noqa: BLE001
    item("5 site no ar", False, repr(e)[:160])


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo)] + list(a), capture_output=True, text=True).stdout.strip()


for nome, repo, caminhos in (("espelho", TB, ["."]),
                             ("Central", CEN, ["vault/originals_copy/um_unificado_v396", "vault/originals_copy/tgl_kernel_v396", "fronteira_tgl",
                                               "patents/_formula_completa", "memory/TGL_ATLAS.md"])):
    h, o = git(repo, "rev-parse", "HEAD"), git(repo, "rev-parse", "origin/main")
    pend = git(repo, "status", "--porcelain", "--untracked-files=no", "--", *caminhos)
    item("6 %s: HEAD = origin/main e nada pendente na custódia" % nome, h == o and not pend, "%s %s" % (h[:8], ("| pendente: " + pend[:120]) if pend else ""))
n_ok = sum(1 for _, ok, _ in R if ok)
print("\nCONFERÊNCIA FINAL: %d/%d ok" % (n_ok, len(R)))
out = CEN / "work" / "custodia_v396_22out" / "CONFERENCIA_FINAL_v396.json"
out.write_text(json.dumps({"itens": [{"item": n, "ok": ok, "detalhe": d} for n, ok, d in R], "ok": n_ok, "total": len(R), "pin": pin},
                          ensure_ascii=False, indent=1), encoding="utf-8")
sys.exit(0 if n_ok == len(R) else 1)
