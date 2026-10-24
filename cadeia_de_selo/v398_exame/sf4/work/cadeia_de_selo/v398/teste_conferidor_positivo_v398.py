# -*- coding: utf-8 -*-
"""teste_conferidor_positivo_v398.py -- exercita o caminho POSITIVO do conferidor (conferir_rito_v398.py, o arquivo REAL, apontado por V398_NOS) SEM instalar nada e SEM tocar o Nos: monta um Nos FALSO em v398\\falso_nos
a partir da pasta do ensaio a seco (dry_v398: o um.py candidato, o kernel materializado COM os residuais, o core e o selo que o ensaio computou, o artigo, o sumario e o .md). E' uma EMULACAO: o core e o selo vem do ensaio
(nao do rito), e o selo ganha da v397 as chaves que o main poe depois do literal (fail_closed_selftest, rite_checkpoints, not_sealed_this_run). Um 'TUDO BATE' aqui diz que as expressoes do conferidor concordam com os ESPERADOS
e com o que o ensaio mediu; nao substitui o conferidor depois do rito real. Molde: teste_conferidor_positivo_v397.py (cadeia v397). uso: python -I -B -X utf8 teste_conferidor_positivo_v398.py"""
import hashlib, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
DRY = os.path.join(HERE, "dry_v398"); FN = os.path.join(HERE, "falso_nos")
sha = lambda b: hashlib.sha256(b).hexdigest()
if os.path.isdir(FN):
    shutil.rmtree(FN)
os.makedirs(FN)
um = open(os.path.join(DRY, "um.py"), "rb").read()
open(os.path.join(FN, "um.py"), "wb").write(um)
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(FN, "tgl_kernel"))
cj = json.load(open(os.path.join(DRY, "core_ensaio.json"), encoding="utf-8"))
json.dump({"core": cj["core"], "verdict": cj["verdict"]}, open(os.path.join(FN, "um_absoluto.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
selo0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto_selo.json"), encoding="utf-8"))
selo = dict(selo0); selo.update(json.load(open(os.path.join(DRY, "selo_ensaio.json"), encoding="utf-8")))
selo["sha256"] = dict(selo0.get("sha256") or {}); selo["sha256"]["um.py"] = sha(um)
json.dump(selo, open(os.path.join(FN, "um_absoluto_selo.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
for l in ("pt", "en"):
    for ext in ("txt", "toc"):
        shutil.copyfile(os.path.join(DRY, "dry_v398_%s.%s" % (l, ext)), os.path.join(FN, "um_absoluto_%s.%s" % (l, ext)))
for n in ("um_absoluto_forma_canonica.md", "um_absoluto_manifest.md"):
    shutil.copyfile(os.path.join(DRY, n), os.path.join(FN, n))
env = dict(os.environ, V398_NOS=FN)
r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_rito_v398.py"), "_POSITIVO_FALSO_NOS"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
print(r.stdout[-6000:]); print(r.stderr[-1500:])
sys.exit(r.returncode)
