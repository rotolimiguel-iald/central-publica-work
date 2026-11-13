# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] do molde v410/reverter_v410.py para uma versao SEM modulo novo: a lista do instalador e' VAZIA (nada vai a quarentena; a asserta exige a lista vazia == ESPERADOS.bundle_sha256); o um.py volta a v410 (sha16 lido de v410\ESPERADOS_v410.json); NAO executado na preparacao
"""reverter_v411.py -- REVERSAO da instalacao v411 (ato da gerencia c1; usar so' se o rito falhar; NAO executado na preparacao). Le o ULTIMO APLICADO_AO_CANONICO_*.json desta pasta (o carimbo dos backups; nada digitado), guarda o estado
falho como registro, restaura os 10 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, o sidecar um_absoluto_selo_acom.json, o manifesto do kernel tgl_kernel_proof_manifest.json, TGLExt.lean, TGL/Audit.lean). A v411 NAO tem
modulo novo: a lista que o instalador gravou e' VAZIA (conferida contra ESPERADOS.bundle_sha256, vazio): nada vai a QUARENTENA (a pasta quarentena_bundle_<ts> e' criada vazia, como registro). Confere ao fim que o um.py voltou a ser a v410
selada (o sha16 e' LIDO de ESPERADOS_v410.json do pacote anterior, nunca digitado). Fail-closed: backup ausente => para sem tocar o que resta. NAO restaura, como no molde: os .tex e os .pdf que o rito reescreve no Nos ficam como o rito
os deixou, e o .lake do kernel nao e' limpo; a proxima rodada os regenera. Recusa -O e o modo de ensaio, como o instalar. Molde: reverter_v410.py."""
import datetime, glob, hashlib, json, os, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
if os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1":
    raise SystemExit("RECUSO: o MODO DE ENSAIO do topo proposto nao instala nem reverte nada")

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CAD = os.path.dirname(os.path.abspath(__file__))
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ap_p = sorted(glob.glob(os.path.join(CAD, "APLICADO_AO_CANONICO_*.json")))
assert ap_p, "nenhum APLICADO_AO_CANONICO_*.json: nada instalado por instalar_v411.py"
AP = json.load(open(ap_p[-1], encoding="utf-8")); TS = AP["ts"]
T2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# --- tudo o que decide a reversao e' LIDO ANTES de qualquer escrita (fail-closed): ESPERADOS_v411, a lista dos modulos novos (vazia) e a ancora do hash da v410 selada
esp = json.load(open(os.path.join(CAD, "ESPERADOS_v411.json"), encoding="utf-8"))
_aplic = AP.get("modulos_novos_v411") or {}
_lista = list(_aplic.get("lista") or []) or list(esp.get("bundle_sha256") or [])
assert len(_lista) == len(set(_lista)) == len(esp["bundle_sha256"]) == esp["kernel"]["modulos_novos"] == 0 and set(_lista) == set(esp["bundle_sha256"]) and all(x_.startswith("TGLExt/") and x_.count("/") == 1 and x_.endswith(".lean") for x_ in _lista), ("a lista dos modulos novos da v411 tem de ser VAZIA (== ESPERADOS.bundle_sha256): a v411 nao tem modulo novo", len(_lista))
try:
    ANCORA = json.load(open(os.path.join(os.path.dirname(CAD), "v410", "ESPERADOS_v410.json"), encoding="utf-8"))["candidato_sha16"]   # o sha16 do um.py da v410 selada, lido do pacote anterior
except (OSError, ValueError, KeyError):
    ANCORA = None
alvos = list(AP["backups"].keys())
assert sorted(alvos) == sorted(["um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",
                                os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")]), alvos
for a in alvos:   # fail-closed: todos os backups existem e batem com o que o instalador gravou, ANTES de qualquer escrita
    b = AP["backups"][a]["backup"]; assert os.path.exists(b) and sh(b)[:16] == AP["backups"][a]["sha16"], ("backup ausente ou alterado", b)
rec = {"ts": T2, "backups": TS, "aplicado": os.path.basename(ap_p[-1]), "guardado": [], "restaurado": [], "quarentena": []}
reg = os.path.join(CAD, "tentativa_v411_rito_falhou_" + T2)
os.makedirs(reg)
for a in alvos + ["rodada_v411_stdout.txt"]:
    p = os.path.join(NOS, a)
    if os.path.exists(p):
        d = os.path.join(reg, a.replace(os.sep, "__")); shutil.copyfile(p, d)
        rec["guardado"].append({"arquivo": a, "sha16": sh(d)[:16], "bytes": os.path.getsize(d)})
for a in alvos:
    p = os.path.join(NOS, a); b = AP["backups"][a]["backup"]
    data = open(b, "rb").read(); tmp = p + ".tmp_reverter"
    open(tmp, "wb").write(data)
    assert os.path.getsize(tmp) == len(data) and sh(tmp) == hashlib.sha256(data).hexdigest()
    os.replace(tmp, p)
    rec["restaurado"].append({"arquivo": a, "sha16": sh(p)[:16]})
qd = os.path.join(CAD, "quarentena_bundle_" + T2)
os.makedirs(qd)
rec["quarentena_fonte"] = "APLICADO_AO_CANONICO.modulos_novos_v411.lista (vazia)" if "lista" in _aplic else "ESPERADOS.bundle_sha256 (vazio)"
for nome in _lista:   # (vazia na v411: nenhum modulo novo; o laco fica, como no molde, para a forma ser a mesma)
    p = os.path.join(NOS, "tgl_kernel", *nome.split("/"))
    if os.path.isfile(p):
        d_ = os.path.join(qd, *nome.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True)
        shutil.move(p, d_); rec["quarentena"].append(nome)
umsha = sh(os.path.join(NOS, "um.py"))[:16]
rec["um_py_sha16"] = umsha
rec["ancora_v410"] = {"fonte": "v410/ESPERADOS_v410.json[candidato_sha16]", "sha16": ANCORA}
rec["ok"] = umsha == esp["origem_sha16"] and (ANCORA is None or umsha == ANCORA)
json.dump(rec, open(os.path.join(CAD, "RECIBO_REVERSAO_" + T2 + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg, "nao_restaura": "os .tex e os .pdf que o rito reescreve e o .lake do kernel"}, ensure_ascii=False))
sys.exit(0 if rec["ok"] else 1)
