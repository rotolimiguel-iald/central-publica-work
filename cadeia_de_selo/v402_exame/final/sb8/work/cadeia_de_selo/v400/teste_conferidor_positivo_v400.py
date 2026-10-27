# -*- coding: utf-8 -*-
"""teste_conferidor_positivo_v400.py -- exercita o caminho POSITIVO do conferidor (conferir_rito_v400.py, o arquivo REAL, apontado por V400_NOS) SEM instalar nada e SEM tocar o Nos: monta um Nos FALSO em v400\\falso_nos
a partir da pasta do ensaio a seco (dry_v400: o um.py candidato, o kernel materializado COM os residuais, o core e o selo que o ensaio computou, o artigo, o sumario e o .md). E' uma EMULACAO: o core e o selo vem do ensaio
(nao do rito), e o selo ganha da v399 as chaves que o main poe depois do literal (fail_closed_selftest, rite_checkpoints, not_sealed_this_run). O SIDECAR um_absoluto_selo_acom.json (a ultima coisa que o um.py escreve) e' gerado AQUI
pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, importada de uma copia de bytes do dry) sobre o core e o selo FINAIS do Nos falso, e o rodada_v400_stdout.txt e' sintetizado do stdout do fluxo do ensaio mais a linha de
fechamento do sidecar. Um 'TUDO BATE' aqui diz que as expressoes do conferidor (inclusive os 14 itens C1-C14 e o round trip do um.py) concordam com os ESPERADOS e com o que o ensaio mediu; nao substitui o conferidor depois do
rito real. Molde: teste_conferidor_positivo_v399.py (cadeia v399). uso: python -I -B -X utf8 teste_conferidor_positivo_v400.py"""
import hashlib, importlib.util, io, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
DRY = os.path.join(HERE, "dry_v400"); FN = os.path.join(HERE, "falso_nos")
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
        shutil.copyfile(os.path.join(DRY, "dry_v400_%s.%s" % (l, ext)), os.path.join(FN, "um_absoluto_%s.%s" % (l, ext)))
for n in ("um_absoluto_forma_canonica.md", "um_absoluto_manifest.md"):
    shutil.copyfile(os.path.join(DRY, n), os.path.join(FN, n))
# o SIDECAR: a funcao do PROPRIO candidato (uma copia de bytes do dry; __file__ = dry\um.py, igual ao um.py do Nos falso) sobre o core e o selo FINAIS do Nos falso
spec = importlib.util.spec_from_file_location("um_sidecar_emulacao", os.path.join(DRY, "um.py")); umm = importlib.util.module_from_spec(spec)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    spec.loader.exec_module(umm); umm.OUT = FN
    sys.stdout = _buf = io.StringIO()
    umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf.getvalue()
finally:
    sys.stdout = _o; sys.stdout.reconfigure(encoding="utf-8")
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v400.json"), encoding="utf-8"))
open(os.path.join(FN, "rodada_v400_stdout.txt"), "w", encoding="utf-8").write("\n".join(ens["mainflow"]["stdout"]) + "\n" + _linha_sidecar + "RITO_RC=0\n")
env = dict(os.environ, V400_NOS=FN)
r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "conferir_rito_v400.py"), "_POSITIVO_FALSO_NOS"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
print(r.stdout[-7000:]); print(r.stderr[-1500:])
sys.exit(r.returncode)
