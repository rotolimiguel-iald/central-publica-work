# -*- coding: utf-8 -*-
"""teste_conferidor_positivo.py -- DELTA 19/10: exercita o caminho POSITIVO do conferidor (conferir_rito_v394.py) SEM instalar nada e SEM tocar o Nos: monta um Nos FALSO em delta_19out\\falso_nos a partir da pasta do ensaio a seco
(dry_v394_d19: o um.py candidato, o kernel materializado COM os residuais, o core e o selo que o ensaio computou, o artigo, o sumario e o .md) e roda uma COPIA do conferidor apontada para ele (so' trocam: a pasta do Nos, a pasta
dos ESPERADOS e o arquivo de saida). E' uma EMULACAO: o core e o selo vem do ensaio (nao do rito), e o selo ganha de v393 as chaves que o main poe depois do literal (fail_closed_selftest, rite_checkpoints, not_sealed_this_run).
Um 'TUDO BATE' aqui diz que as expressoes novas do conferidor concordam com os ESPERADOS e com o que o ensaio mediu; nao substitui o conferidor depois do rito real.
uso: python -I -B -X utf8 teste_conferidor_positivo.py"""
import hashlib, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
DRY = os.path.join(V, "dry_v394" + DL.ROT); FN = os.path.join(HERE, "falso_nos")
sha = lambda b: hashlib.sha256(b).hexdigest()
if os.path.isdir(FN):
    shutil.rmtree(FN)
os.makedirs(FN)
um = open(os.path.join(DRY, "um.py"), "rb").read()
open(os.path.join(FN, "um.py"), "wb").write(um)
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(FN, "tgl_kernel"))
cj = json.load(open(os.path.join(DRY, "core_ensaio.json"), encoding="utf-8"))
json.dump({"core": cj["core"], "verdict": cj["verdict"]}, open(os.path.join(FN, "um_absoluto.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
selo0 = json.load(open(os.path.join(V, "base_v393", "um_absoluto_selo.json"), encoding="utf-8"))
selo = dict(selo0); selo.update(json.load(open(os.path.join(DRY, "selo_ensaio.json"), encoding="utf-8")))
selo["sha256"] = dict(selo0.get("sha256") or {}); selo["sha256"]["um.py"] = sha(um)
json.dump(selo, open(os.path.join(FN, "um_absoluto_selo.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
for l in ("pt", "en"):
    for ext in ("txt", "toc"):
        shutil.copyfile(os.path.join(DRY, "dry_v394_%s.%s" % (l, ext)), os.path.join(FN, "um_absoluto_%s.%s" % (l, ext)))
for n in ("um_absoluto_forma_canonica.md", "um_absoluto_manifest.md"):
    shutil.copyfile(os.path.join(DRY, n), os.path.join(FN, n))
src = open(os.path.join(V, "conferir_rito_v394.py"), "rb").read().decode("utf-8")
def sub(old, new):
    global src
    assert src.count(old) == 1, (old[:80], src.count(old)); src = src.replace(old, new)
sub("HERE = os.path.dirname(os.path.abspath(__file__))\n", "HERE = %r\n" % V)
sub('NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")', "NOS = %r; NK = os.path.join(NOS, \"tgl_kernel\")" % FN)
sub('p = os.path.join(HERE, "conferencia_rito_v394%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))', "p = os.path.join(%r, \"conferencia_POSITIVO_FALSO_NOS.json\")" % HERE)
cp = os.path.join(HERE, "conferir_rito_positivo_copia.py"); open(cp, "wb").write(src.encode("utf-8"))
r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", cp], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-6000:]); print(r.stderr[-1500:])
sys.exit(r.returncode)
