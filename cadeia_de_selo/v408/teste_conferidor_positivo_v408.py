# -*- coding: utf-8 -*-
"""teste_conferidor_positivo_v408.py -- exercita o caminho POSITIVO do conferidor (conferir_rito_v408.py, o arquivo REAL, apontado por V408_NOS) SEM instalar nada e SEM tocar o Nos: monta um Nos FALSO em v408\\falso_nos
a partir da pasta do ensaio a seco (dry_v408: o um.py candidato, o kernel materializado COM os residuais, o core e o selo que o ensaio computou, o artigo, o sumario e o .md). E' uma EMULACAO: o core e o selo vem do ensaio
(nao do rito), e o selo ganha da v407 as chaves que o main poe depois do literal (fail_closed_selftest, rite_checkpoints, not_sealed_this_run). O SIDECAR um_absoluto_selo_acom.json (a ultima coisa que o um.py escreve) e' gerado AQUI
pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, importada de uma copia de bytes do dry) sobre o core e o selo FINAIS do Nos falso, e o rodada_v408_stdout.txt e' sintetizado do stdout do fluxo do ensaio mais a linha de
fechamento do sidecar. Um 'TUDO BATE' aqui diz que as expressoes do conferidor (inclusive os itens C1-C16 do selo pela propria tecnologia, o round trip do um.py e, na v408, o registro tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados,
as 41 ancoras e os 4 modulos do bundle; nenhuma chave antiga muda) concordam com os ESPERADOS e com o que o ensaio mediu; nao substitui o conferidor depois do rito real.
FAIL-CLOSED: exige ensaio_a_seco_v408.json (TUDO PASSOU, deste candidato), ESPERADOS_v408.json e a pasta dry_v408; sem eles PARA com a mensagem do que falta (nunca 'ok' falso).
Molde: teste_conferidor_positivo_v407.py (cadeia v407), adaptado em 04/11/2026 a v408 (claude-construtor-v408). uso: python -B -X utf8 teste_conferidor_positivo_v408.py   (SEM -I: importa o um.py do dry, que precisa do numpy do usuario)"""
import ast, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v408 as DL  # noqa: E402
DRY = os.path.join(HERE, "dry_v408"); FN = os.path.join(HERE, "falso_nos")
_CAND = json.load(open(os.path.join(HERE, "CANDIDATO_v408.json"), encoding="utf-8"))
for _n_ in ("ensaio_a_seco_v408.json", "ESPERADOS_v408.json"):
    assert os.path.exists(os.path.join(HERE, _n_)), "FAIL-CLOSED: falta %s (o ensaio a seco, e depois gerar_esperados_v408.py, tem de rodar antes deste teste)" % _n_
assert os.path.isdir(DRY), "FAIL-CLOSED: falta a pasta dry_v408 (e' escrita pelo ensaio a seco)"
_ens0 = json.load(open(os.path.join(HERE, "ensaio_a_seco_v408.json"), encoding="utf-8"))
assert _ens0.get("veredito") == "TUDO PASSOU" and _ens0.get("sha16") == _CAND["sha16"], ("FAIL-CLOSED: o ensaio nao e' deste candidato ou nao passou", _ens0.get("veredito"), _ens0.get("sha16"), _CAND["sha16"])
sha = lambda b: hashlib.sha256(b).hexdigest()
if os.path.isdir(FN):
    shutil.rmtree(FN)
os.makedirs(FN)
um = open(os.path.join(DRY, "um.py"), "rb").read()
open(os.path.join(FN, "um.py"), "wb").write(um)
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(FN, "tgl_kernel"))
cj = json.load(open(os.path.join(DRY, "core_ensaio.json"), encoding="utf-8"))
_gw = re.search(r"^GA_WINDOW_STATUS = \((.*?)\)\r?$", um.decode("utf-8"), re.S | re.M); assert _gw, "a constante GA_WINDOW_STATUS nao esta no candidato"
json.dump({"core": cj["core"], "verdict": cj["verdict"], "ga_window_status": ast.literal_eval("(" + _gw.group(1) + ")")}, open(os.path.join(FN, "um_absoluto.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
selo0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto_selo.json"), encoding="utf-8"))
selo = dict(selo0); selo.update(json.load(open(os.path.join(DRY, "selo_ensaio.json"), encoding="utf-8")))
selo["sha256"] = dict(selo0.get("sha256") or {}); selo["sha256"]["um.py"] = sha(um)
json.dump(selo, open(os.path.join(FN, "um_absoluto_selo.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
for l in ("pt", "en"):
    for ext in ("txt", "toc"):
        shutil.copyfile(os.path.join(DRY, "dry_v408_%s.%s" % (l, ext)), os.path.join(FN, "um_absoluto_%s.%s" % (l, ext)))
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
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v408.json"), encoding="utf-8"))
open(os.path.join(FN, "rodada_v408_stdout.txt"), "w", encoding="utf-8").write("\n".join(ens["mainflow"]["stdout"]) + "\n" + _linha_sidecar + "RITO_RC=0\n")
env = dict(os.environ, V408_NOS=FN)
r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "conferir_rito_v408.py"), "_POSITIVO_FALSO_NOS"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
print(r.stdout[-7000:]); print(r.stderr[-1500:])
sys.exit(r.returncode)
