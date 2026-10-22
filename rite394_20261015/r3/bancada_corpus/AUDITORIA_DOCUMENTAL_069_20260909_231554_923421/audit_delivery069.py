"""Documentary read-only audit of delivery069; does not execute any audited program."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,re
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt")
BASE=ROOT/"REEXAME_SUFICIENCIA_069_20260909"
OUT=Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT) and OUT!=BASE
def pin(p):
    p=Path(p);b=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(Path(p).read_bytes())
def equal(a,b):return a["sha256"]==b["sha256"] and ("bytes" not in b or a["bytes"]==b["bytes"])
def new(p,b):
    assert p.parent==OUT and not p.exists()
    tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    os.replace(tmp,p);assert p.read_bytes()==b
    return pin(p)
mp=BASE/"MANIFESTO_ENTREGA_069.json";mpin=pin(mp);m=load(mp)
measured=[pin(x["path"])for x in m["files"]]
by_path={x["path"]:x for x in measured}
file_checks=[{"path":b["path"],"passed":equal(a,b)}for a,b in zip(measured,m["files"])]
snap=load(BASE/"ESTADO_CANONICO_069.json")
old=load(ROOT/"REEXAME_SUFICIENCIA_068_20260909/ESTADO_CANONICO_068.json")
previous=load(ROOT/"REEXAME_SUFICIENCIA_066_20260909/RESULTADO_INTEGRACAO_066.json")
result=load(BASE/"RESULTADO_ENTREGA_069.json")
canon=[x for x in measured if "/Artigo/"in x["path"]]
oldpins={x["path"]:x for x in old["pins"]}
um=next(x for x in canon if x["path"].endswith("/um.py"))
tree=ast.parse(Path(um["path"]).read_bytes())
node=next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=="_EMBEDDED_KERNEL_FILES"for t in n.targets))
emb=ast.literal_eval(node)
presence=[{"module":x["module"],"present":("TGLExt/"+x["module"]+".lean")in emb}for x in snap["modules"]]
seal=load(next(x["path"]for x in canon if x["path"].endswith("/um_absoluto_selo.json")))
cas={}
for c in result["cas"]:
    data=load(c["receipt"]["path"]);rows=list(data["checks"].values())if isinstance(data["checks"],dict)else data["checks"]
    cas[Path(c["receipt"]["path"]).name]={"receipt":pin(c["receipt"]["path"]),"expected":c["exact_controls"],"count":len(rows),"all_exact":all(x.get("passed")is True and x.get("residual")=="0"for x in rows),"status":data["status"],"expressions":data.get("expressions",{}),"rerun":False}
tunnel=Path(m["tunnel"]["path"])
links={}
for p in [BASE/"REEXAME_SUFICIENCIA.md",tunnel]:
    links[p.name]=re.findall(r"\]\(<(C:/[^>]+)>\)",p.read_text(encoding="utf-8"))
def source(src):
    if src=="snapshot069":return snap["pins"]
    if src=="historical_working_copy98":return previous["working_copy"]
    return load(ROOT/src)
def locate(obj,loc):
    assert loc.startswith("root")
    for field,index in re.findall(r"\.([^\.\[\]]+)|\[(\d+)\]",loc[4:]):
        obj=obj[field]if field else obj[int(index)]
    return obj
audit=[]
for row in m["checks"]:
    name=row["name"];kind,_,tail=name.partition(":")
    ok=None;scope="CURRENT_REEVALUATION";error=None
    try:
        if kind=="canonical_snapshot_status":ok=snap["status"]=="READ_ONLY_STABLE_SNAPSHOT"
        elif kind=="four_unchanged_from068":ok=len(canon)==4 and all(equal(x,oldpins[x["path"]])for x in canon)
        elif kind=="seal_hash_matches":ok=seal["sha256"]["um.py"]==um["sha256"]
        elif kind=="canonical_comparison_modules":ok=presence==snap["modules"] and len(presence)==98 and sum(x["present"]for x in presence)==77
        elif kind=="canonical_embedded_files":ok=len(emb)==snap["embedded_files"]==683
        elif kind in ("absolute_pin","pin"):
            src,loc=tail.rsplit(":",1);obj=locate(source(src),loc)
            ok=Path(obj["path"]).is_absolute()if kind=="absolute_pin"else equal(pin(obj["path"]),obj)
        elif kind=="pending_modules_unchanged":ok=snap["absent"]==previous["pending_canonical_modules"]==[x["module"]for x in presence if not x["present"]]
        elif kind=="directory":ok=(ROOT/tail).is_dir()
        elif kind=="cas_count":ok=cas[tail]["count"]==cas[tail]["expected"]
        elif kind=="cas_exact":ok=cas[tail]["all_exact"]
        elif kind=="cas_not_lean":ok="NOT_LEAN"in cas[tail]["status"]
        elif kind=="cas_total31":ok=sum(x["count"]for x in cas.values())==31
        elif kind in ("new_destination","new_tunnel_destination"):
            scope="HISTORICAL_PRE_WRITE_REPORTED_PASS_NOT_REPLAYABLE"
        elif kind in ("stable_pre_write","stable_final"):ok=equal(pin(tail),by_path[tail])
        elif kind=="link":
            doc,idx=tail.rsplit(":",1);p=links[doc][int(idx)]
            ok=p==row["detail"] and Path(p).is_file()
        else:raise ValueError("Unrecognized check:"+name)
    except Exception as ex:error=repr(ex);ok=False
    audit.append({"name":name,"reported_passed":row["passed"],"current_passed":ok,"scope":scope,"error":error})
extra=[]
def ck(n,b):extra.append({"name":n,"passed":bool(b)})
ck("105_unique_files",len(m["files"])==len(by_path)==105)
ck("all_file_bytes_match",all(x["passed"]for x in file_checks))
ck("566_reported_checks",m["checks_total"]==m["checks_passed"]==len(m["checks"])==566 and all(x["passed"]is True for x in m["checks"]))
ck("current_repeatable_checks",all(x["current_passed"]is True for x in audit if x["scope"]=="CURRENT_REEVALUATION"))
ck("six_historical_creation_preconditions",sum(x["scope"].startswith("HISTORICAL")for x in audit)==6)
ck("canonical_result_pin",equal(um,result["canonical"]))
ck("canonical_result_count",result["canonical_modules_present"]==77 and result["pending_canonical_modules"]==snap["absent"] and len(snap["absent"])==21)
ck("CAS31_no_new_Lean",m["exact_symbolic_controls"]==result["new_exact_symbolic_controls"]==31 and result["new_lean_modules"]==result["new_lean_compilations"]==0 and m["new_lean_compilation"]is False)
ck("result_C4_matches_receipt",result["one_loop_background"]["C4"].replace(" ","")==cas["VERIFICACAO_TRACOS_INVARIANTES.json"]["expressions"]["background_C4"].replace(" ",""))
ck("result_C4_total_derivatives",result["one_loop_background"]["includes_total_derivatives"]is True and result["one_loop_background"]["total_derivative_contribution"]=="5*x/4")
ck("limits_remain_open",m["goal_complete"]is False and result["goal_complete"]is False and result["canonical_gate_modified"]is False and result["nature_tests_run"]is False)
ck("tunnel_pin",equal(pin(tunnel),m["tunnel"]))
ck("105_unchanged_end",all(equal(pin(x["path"]),x)for x in measured))
ck("manifest_unchanged_end",equal(pin(mp),mpin))
bad=[x["name"]for x in audit if x["current_passed"]is False]+[x["name"]for x in extra if not x["passed"]]
status="PASS_DOCUMENTARY_069_WITH_EXPLICIT_HISTORICAL_SCOPE"if not bad else"FAIL_DOCUMENTARY_069"
report=f"""# Auditoria documental final — entrega 069

[REAL — leitura de bytes, AST e JSON] **{status}**. Não foi encontrada divergência material de custódia ou consistência.

Os **105 arquivos distintos** listados no manifesto foram relidos integralmente e conferem em tamanho e SHA-256. Os quatro canônicos também coincidem com os pins de068; sua leitura foi autorizada em modo elevado, sem execução. A AST e a tabela literal de um.py conferem 683 arquivos embutidos, 77 dos98 módulos de comparação presentes e21 pendentes. Esse conjunto de98 não é o total de módulos do programa.

O manifesto registra **566/566 controles aprovados**, e a contagem foi conferida. **560 condições atualmente repetíveis foram reavaliadas e passaram**, incluindo160 pares de controles de pins, estabilidade e links. As outras **seis** são condições históricas de inexistência dos destinos ANTES da escrita. O finalizador lido exige essas condições e escrita exclusiva; a auditoria registra seu PASS histórico, mas não finge testar inexistência depois de os arquivos terem sido criados. Não houve rerun do finalizador.

Os dois recibos CAS conferem **23+8=31 controles exatos**, todos aprovados e com resíduo zero. Nenhum CAS ou Lean foi reexecutado. O coeficiente estruturado C4=(7440x²+1616x−211)/96 confere com o recibo; o termo de divergência total5x/4 está mantido.

Foram lidos RESULTADO_ENTREGA_069.json, REEXAME_SUFICIENCIA.md, MEMORIA_DE_TRABALHO_069.md, DESENHO_DO_FECHAMENTO_ADENDO_069.md e o túnel. As superfícies concordam: Q2 fornece produtos temporais e álgebra auxiliar formal com anomalia consistente; isso não fornece QME satisfeita. C0/KT no espaço indicado não é H1 relativo completo. Os31 controles CAS não são teoremas Lean. A incorporação77/98 com21 pendentes, a medida normalizada, o alcance local on-shell e as constantes de C4 estão preservados. O dado histórico da auditoria068 aparece como histórico.

Esta é auditoria documental independente do finalizador. Sou autor da nota de calor: NÃO atribuo a esta auditoria uma revisão matemática independente dessa nota. Os pareceres matemáticos existentes têm autores e escopos próprios; não foram substituídos por esta conferência de hashes.

A preservação demonstrada é a igualdade dos bytes com os pins e entre as leituras desta auditoria. Ela não representa monitoramento integral do histórico do computador. Nenhum arquivo existente foi modificado; somente este diretório novo recebeu auditor, parecer e recibo. Nenhum um.py, finalizador, CAS ou Lean foi executado/importado. Nenhum gate ou estatuto científico foi promovido.

Manifesto auditado: {mpin["path"]}
SHA-256 medido: {mpin["sha256"]}
"""
rp=new(OUT/"PARECER_DOCUMENTAL_069.md",report.encode("utf-8"))
answer={"status":status,"created_utc":datetime.now(timezone.utc).isoformat(),"manifest_audited":mpin,"report":rp,"auditor":pin(__file__),
"counts":{"listed_files":105,"canonical_files":len(canon),"manifest_reported_total":len(audit),"manifest_reported_passed":sum(x["reported_passed"]for x in audit),"repeatable_checks":sum(x["scope"]=="CURRENT_REEVALUATION"for x in audit),"repeatable_checks_passed":sum(x["current_passed"]is True for x in audit),"historical_creation_checks":sum(x["scope"].startswith("HISTORICAL")for x in audit),"cas_controls":31,"extra_checks":len(extra),"extra_passed":sum(x["passed"]for x in extra)},
"failed_checks":bad,"files":measured,"file_checks":file_checks,"manifest_checks":audit,"extra_checks":extra,"cas":list(cas.values()),
"limitations":["The six historical creation preconditions are reported as historical, not replayed.","Documentary independence from finalizer does not make this an independent mathematical review of this auditor's authored heat note.","CAS and Lean were not rerun."],
"originals_modified":False,"manifest_modified":False,"um_executed_or_imported":False,"finalizer_executed_or_imported":False,"CAS_rerun":False,"lean_executed":False}
ap=new(OUT/"RESULTADO_AUDITORIA_DOCUMENTAL_069.json",(json.dumps(answer,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":status,"report":rp,"result":ap,"counts":answer["counts"],"failed_checks":bad},ensure_ascii=False))
if bad:raise SystemExit(1)
