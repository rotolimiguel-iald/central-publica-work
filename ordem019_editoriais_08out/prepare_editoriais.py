from __future__ import annotations
import hashlib, json, runpy, shutil, subprocess, tempfile
from pathlib import Path
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
WORK=Path(r"C:\IALD\Central de Patentes\work\ordem019_editoriais_08out")
EVID=Path(r"C:\IALD\PROGRAMA_IALD\evidencias")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {"path":str(p),"sha256":sha(p),"bytes":p.stat().st_size}
def new_bytes(p,b):
    with p.open("xb") as f: f.write(b); f.flush()
    assert p.read_bytes()==b
def new_text(p,s): new_bytes(p,s.encode("utf-8"))
def new_json(p,o): new_text(p,json.dumps(o,ensure_ascii=False,indent=2)+"\n")

sbox=BASE/"F1.2"/"sandbox"
old=sbox/"build_completion_e2.py"
new=sbox/"build_completion_e3.py"
src=old.read_text(encoding="utf-8")
before='''SANDBOX = Path(__file__).resolve().parent
result_path = SANDBOX / "BUILD_COMPLETION_RESULT.json"
if result_path.exists():
    raise FileExistsError(f"Existing evidence must not be replaced: {result_path}")
MODULES = SANDBOX / "F12Completion"
BUILD = SANDBOX / "build" / "F12Completion"
BUILD.mkdir(parents=True, exist_ok=True)
'''
after='''SANDBOX = Path(__file__).resolve().parent
result_path = SANDBOX / "BUILD_COMPLETION_RESULT.json"
MODULES = SANDBOX / "F12Completion"
BUILD = SANDBOX / "build" / "F12Completion"
existing_products = [result_path]
existing_products.extend(sorted(SANDBOX.glob("BUILD_*.log")))
existing_products.extend(sorted((SANDBOX / "build").rglob("*.olean")))
present = [p for p in existing_products if p.exists() or p.is_symlink()]
if present:
    raise FileExistsError("Existing evidence must not be replaced: " + ", ".join(map(str, present)))
BUILD.mkdir(parents=True, exist_ok=True)
'''
assert src.count(before)==1
new_text(new,src.replace(before,after,1))
tests=[]
for label,rel in (("result","BUILD_COMPLETION_RESULT.json"),("orphan_log","BUILD_V351DualScalingBridge.log"),("orphan_olean","build/F12Completion/AgapeNonVacuity.olean")):
    with tempfile.TemporaryDirectory(prefix="f12e3_",dir=WORK) as td:
        d=Path(td); script=d/new.name; shutil.copyfile(new,script)
        art=d/rel; art.parent.mkdir(parents=True,exist_ok=True); art.write_bytes(b"old-evidence\n")
        prior={str(p.relative_to(d)):sha(p) for p in d.rglob("*") if p.is_file()}
        calls=[]; original_run=subprocess.run
        def spy(*a,**kw): calls.append(1); raise AssertionError("Lean reached")
        subprocess.run=spy
        try:
            try: runpy.run_path(str(script),run_name="__main__")
            except FileExistsError as e: msg=str(e)
            else: raise AssertionError("preflight accepted "+label)
        finally: subprocess.run=original_run
        post={str(p.relative_to(d)):sha(p) for p in d.rglob("*") if p.is_file()}
        assert not calls and prior==post and rel.replace("/",str(Path("/"))) in msg
        tests.append({"scenario":label,"exception":"FileExistsError","subprocess_calls":0,"files_unchanged":True})
validation=BASE/"F1.2"/"VALIDACAO_PREFLIGHT_BUILD_COMPLETION_E3_20261008.json"
new_json(validation,{"unit":"F1.2.E3","status":"REAL","source":pin(old),"candidate":pin(new),"tests":tests,"lean_build":"not run; preflight refusal before compilation"})
r12=BASE/"F1.2"/"RESULTADO_F12_E3_PREFLIGHT_COMPLETO_20261008.json"
new_json(r12,{"unit":"F1.2.E3","parent":"F1.2.E2 FECHADA","existing":"Nos Vivo F1.2.E2 has E2 preflight and seq823 link; E3 absent from graph","finding":"E3 checks result, all BUILD_*.log, all build/**/*.olean before mkdir and subprocess","artifacts":[pin(new),pin(validation),pin(old)],"scope":"No sealed script/result or Lean build modified"})

f23=BASE/"F2.3"
temp=Path.home()/"AppData"/"Local"/"Temp"/"iald_f23_e1_unit_20261008.json"
copy=f23/"E1_UNIT_SOURCE_CUSTODY_20261008.json"
new_bytes(copy,temp.read_bytes()); assert sha(copy)==sha(temp)
err3=f23/"ERRATA_F23_E3_SEQ899_E_FONTE_20261008.md"
new_text(err3,"# F2.3.E3 — custodia e referencia da seq 899\n\nAutor: codex-gerente-tgl. Data: 08/10/2026. Estatuto: [REAL].\n\nA fonte da unidade F2.3.E1 em %TEMP% foi copiada byte a byte para E1_UNIT_SOURCE_CUSTODY_20261008.json nesta pasta; hash identico. O original nao foi alterado.\n\nA seq 899, rota formal.f2_3.curved_field_ligand, traz em refs formal.f1_1.o16_class2_wiring_caveat, alheia a F2.3.E1. A referencia correta e a propria rota formal.f2_3.curved_field_ligand e seu registro 874, corrigido pela 899. A seq historica permanece intacta. F2.3 e F2.3.E1 continuam FECHADAS; LiganteLeiCampoCurvo e a unica pedra aprovada para v392.\n")
r23e3=f23/"RESULTADO_F23_E3_CUSTODIA_SEQ899_20261008.json"
new_json(r23e3,{"unit":"F2.3.E3","parent":"F2.3.E1 FECHADA","existing":"Nos Vivo F2.3.E1 has audited docstring; no Lean reconstruction","temp_source":pin(temp),"custody_copy":pin(copy),"byte_equal":True,"map_seq":899,"erroneous_ref":"formal.f1_1.o16_class2_wiring_caveat","correct_route":"formal.f2_3.curved_field_ligand","errata":pin(err3),"scope":"No old source, kernel, Bancada or gate modified"})

adendo=f23/"ADENDO_TEMPERATURA_DIAGNOSTICO.md"
bak=f23/"ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_141543"
cust=EVID/(sha(bak)+".md")
b=bak.read_bytes(); c=adendo.read_bytes()
assert c.startswith(b) and len(c)-len(b)==651 and cust.read_bytes()==b
err4=f23/"ERRATA_F23_E4_APPEND_IN_LOCO_20261008.md"
msg="# F2.3.E4 — errata do acrescimo no ADENDO pinado\n\nAutor: codex-gerente-tgl. Data: 08/10/2026. Estatuto: [REAL — bytes e hashes conferidos].\n\nNa F2.3.E2, foram acrescentados 651 bytes in loco a ADENDO_TEMPERATURA_DIAGNOSTICO.md depois do fecho da F2.3. O evento 355 e a seq 871 pinavam o estado anterior, SHA-256 "+sha(bak)+". A reivindicacao 422 dizia sem tocar F2.3 fechada. A acao contrariou esse alcance; o pino por caminho deixou de reproduzir os bytes antigos.\n\nO backup bak_20261008_141543 e a copia evidencias/"+cust.name+" preservam exatamente os "+str(len(b))+" bytes anteriores. O arquivo atual tem "+str(len(c))+" bytes e o backup e prefixo byte a byte dele. Esta camada nao desfaz nem edita o ADENDO. Futuras correcoes do artefato pinado ficam em arquivo novo ao lado, com hash e vinculo no quadro e mapa.\n"
new_text(err4,msg)
r23e4=f23/"RESULTADO_F23_E4_APPEND_IN_LOCO_20261008.json"
new_json(r23e4,{"unit":"F2.3.E4","parent":"F2.3.E2 FECHADA","existing":"Nos Vivo F2.3.E2 already records junction removal and nomenclature; E4 documents pin break","historical_backup":pin(bak),"historical_evidence":pin(cust),"current_adendo":pin(adendo),"old_is_prefix":True,"bytes_appended":651,"errata":pin(err4),"process":"Claim 422 said without touching closed F2.3; future corrections in new files","scope":"No ADENDO, kernel, Bancada or gate modified"})

f36=BASE/"F3.6"; asimov=f36/"ASIMOV_LAMBDA_SANDBOX"/"RESULTADO_ASIMOV_LAMBDA.json"
o=json.loads(asimov.read_text(encoding="utf-8"))
v=o["runs"][1]["cases"]["A_bare_v3_cov"]["sigma_beta"]
vb=o["runs"][1]["cases"]["Bprime_bare_v3_cov"]["sigma_beta"]
assert v==vb and repr(v)=="0.02190662731844722"
original=f36/"ERRATA_E2_METADADOS_RUN1_NOTACAO_20261008.md"
assert "0,0219066273184472" in original.read_text(encoding="utf-8")
err36=f36/"ERRATA_E3_DIGITO_V3_BASE_NUA_20261008.md"
new_text(err36,"# F3.6.E3 — ultimo digito do V3 na base nua\n\nAutor: codex-gerente-tgl. Data: 08/10/2026. Estatuto: [REAL — transcricao do JSON pinado].\n\nA tabela da ERRATA_E2_METADADOS_RUN1_NOTACAO_20261008.md escreveu 0,0219066273184472 para runs[1], base nua, covariancia V3 selada. O campo runs[1].cases.A_bare_v3_cov.sigma_beta em RESULTADO_ASIMOV_LAMBDA.json e "+repr(v)+"; Bprime_bare_v3_cov tem o mesmo valor. Faltava o ultimo digito 2 na tabela. O texto E2 pinado fica intacto; esta e a leitura vigente. Asimov em Lambda, sem abrir dado observado e sem mudar o portao.\n")
r36=f36/"RESULTADO_F36_E3_DIGITO_V3_20261008.json"
new_json(r36,{"unit":"F3.6.E3","parent":"F3.6.E2 FECHADA","existing":"Nos Vivo F3.6.E2 already has runs[1] and marginalization; only final digit remains","source":pin(asimov),"original_note":pin(original),"errata":pin(err36),"path":"runs[1].cases.A_bare_v3_cov.sigma_beta","A_value":repr(v),"Bprime_value":repr(vb),"shortened_value":"0.0219066273184472","observed_data_opened":False,"gate_changed":False})
print(json.dumps({"F1.2.E3":pin(r12),"F2.3.E3":pin(r23e3),"F2.3.E4":pin(r23e4),"F3.6.E3":pin(r36)},ensure_ascii=False))

