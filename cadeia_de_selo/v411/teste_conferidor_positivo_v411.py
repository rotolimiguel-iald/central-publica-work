# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] do molde v410/teste_conferidor_positivo_v410.py: o dry do ensaio e o falso Nos FORA de work\ (DL.DRY_DIR, DL.FALSO_NOS_DIR: C:\t\k411c, ou a pasta do ensaio do topo proposto), o manifesto por DL.MANIFESTO_ARQ, o ESPERADOS por DL.saida, V411_NOS; o corpo da v410 serve (o conferidor e' o arquivo real)
"""teste_conferidor_positivo_v411.py -- exercita o caminho POSITIVO do conferidor (conferir_rito_v411.py, o arquivo REAL, apontado por V411_NOS) SEM instalar nada e SEM tocar o Nos: monta um Nos FALSO em DL.FALSO_NOS_DIR (fora de work\\)
a partir da pasta do ensaio a seco (DL.DRY_DIR: o um.py candidato -- ou, com V411_ENSAIO_TOPO_PROPOSTO=1, o ARTEFATO DE ENSAIO do topo proposto, que NAO e' candidato --, o kernel materializado COM os residuais, o core e o selo que o
ensaio computou, o artigo, o sumario e o .md). E' uma EMULACAO: o core e o selo vem do ensaio (nao do rito), e o selo ganha da v410 as chaves que o main poe depois do literal (fail_closed_selftest, rite_checkpoints, not_sealed_this_run).
O SIDECAR um_absoluto_selo_acom.json e' gerado AQUI pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, importada de uma copia de bytes do dry) sobre o core e o selo FINAIS do Nos falso, e o rodada_v411_stdout.txt e' sintetizado
do stdout do fluxo do ensaio mais a linha de fechamento do sidecar. Um 'TUDO BATE' aqui diz que as expressoes do conferidor (o registro h0dn_bg1_v411 e os specs da v411; os quatro registros com funcao da v410 e os anteriores herdados;
a secao, o quadro, o topo, o .md, o selo e o stdout da v411; nenhum modulo novo; nenhuma chave antiga muda) concordam com os ESPERADOS e com o que o ensaio mediu; nao substitui o conferidor depois do rito real.
FAIL-CLOSED: exige ensaio_a_seco_v411.json (TUDO PASSOU, deste artefato), ESPERADOS_v411.json e a pasta do dry; sem eles PARA com a mensagem do que falta (nunca 'ok' falso).
uso: python -B -X utf8 teste_conferidor_positivo_v411.py   (SEM -I: importa o um.py do dry, que precisa do numpy do usuario)"""
import ast, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
DRY = DL.DRY_DIR; FN = DL.FALSO_NOS_DIR
assert os.path.normcase(DL.WK) not in os.path.normcase(os.path.abspath(FN)), "o falso Nos tem de ficar FORA de work\\ (D135)"
_CAND = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8"))
for _p_ in (DL.saida("ensaio_a_seco_v411.json"), DL.saida("ESPERADOS_v411.json")):
    assert os.path.exists(_p_), "FAIL-CLOSED: falta %s (o ensaio a seco, e depois gerar_esperados_v411.py, tem de rodar antes deste teste)" % _p_
assert os.path.isdir(DRY), "FAIL-CLOSED: falta a pasta do dry (%s; e' escrita pelo ensaio a seco)" % DRY
_ens0 = json.load(open(DL.saida("ensaio_a_seco_v411.json"), encoding="utf-8"))
assert _ens0.get("veredito") == "TUDO PASSOU" and _ens0.get("sha16") == _CAND["sha16"], ("FAIL-CLOSED: o ensaio nao e' deste artefato ou nao passou", _ens0.get("veredito"), _ens0.get("sha16"), _CAND["sha16"])
sha = lambda b: hashlib.sha256(b).hexdigest()
if os.path.isdir(FN):
    shutil.rmtree(FN)
os.makedirs(FN)
um = open(os.path.join(DRY, "um.py"), "rb").read()
assert sha(um)[:16] == _CAND["sha16"], "o um.py do dry nao e' o do manifesto"
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
    for ext in ("txt", "toc", "tex"):   # (R1, C-02: o .tex do artigo tambem vai ao Nos falso)
        shutil.copyfile(os.path.join(DRY, "dry_v411_%s.%s" % (l, ext)), os.path.join(FN, "um_absoluto_%s.%s" % (l, ext)))
    if os.path.exists(os.path.join(DRY, "dry_v411_%s.pdf" % l)):
        shutil.copyfile(os.path.join(DRY, "dry_v411_%s.pdf" % l), os.path.join(FN, "um_absoluto_%s.pdf" % l))
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
ens = json.load(open(DL.saida("ensaio_a_seco_v411.json"), encoding="utf-8"))
open(os.path.join(FN, "rodada_v411_stdout.txt"), "w", encoding="utf-8").write("\n".join(ens["mainflow"]["stdout"]) + "\n" + _linha_sidecar + "RITO_RC=0\n")
json.dump(dict({"contrato": "FALSO_NOS_v411", "de": DRY, "emulado": ["core e selo do ensaio a seco (nao do rito)", "o stdout do rito (sintetizado do fluxo do ensaio + a linha do sidecar)", "o sidecar (a funcao do proprio artefato)"], "um_py_sha16": sha(um)[:16]}, **DL.MARCA_ENSAIO),
          open(os.path.join(DL.RODADA_PAI, "FALSO_NOS_v411.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # (ao lado do falso Nos, nao dentro: o Nos falso tem so' o que o rito escreve)
import datetime   # noqa: E402
# (R1, C-02) os horarios do rito do Nos falso: o inicio 10 minutos antes (os PDF copiados agora sao posteriores a ele); o arquivo fica no Nos falso, fora de work\
open(os.path.join(FN, "rito_horarios_v411.txt"), "w", encoding="utf-8").write((datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime("%H:%M:%S") + "\n" + datetime.datetime.now().strftime("%H:%M:%S") + "\n")
env = dict(os.environ, V411_NOS=FN, V411_RITO_HORARIOS=os.path.join(FN, "rito_horarios_v411.txt"))
r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "conferir_rito_v411.py"), "_POSITIVO_FALSO_NOS"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
print(r.stdout[-7000:]); print(r.stderr[-1500:])
sys.exit(r.returncode)
