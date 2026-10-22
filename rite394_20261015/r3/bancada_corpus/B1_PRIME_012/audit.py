from support import *
import re,subprocess,sys
K=ROOT/"kernel"
expected=json.loads((ROOT/"AUDIT_NAMES.json").read_text("utf-8"))
finished=sorted((ROOT/"attempts").glob("*/run.json"))
assert finished, "No completed builds"
last=finished[-1]; build=json.loads(last.read_text("utf-8"))
assert build["returncode"]==0, "Latest build failed"
log=(last.parent/"stdout.txt").read_text("utf-8")
allowed={"propext","Classical.choice","Quot.sound"}
found={}
for m in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log,re.S):
    name=re.sub(r"\.\{[^}]*\}","",m.group(1)); found[name]=[re.sub(r"\.\{[^}]*\}","",a.strip()) for a in m.group(2).split(",") if a.strip()]
for m in re.finditer(r"'([^']+)' does not depend on any axioms",log):
    found[re.sub(r"\.\{[^}]*\}","",m.group(1))]=[]
missing=sorted(set(expected)-found.keys())
unexpected={n:[a for a in found.get(n,[]) if a not in allowed] for n in expected}
unexpected={n:a for n,a in unexpected.items() if a}
assert not missing, f"Missing axiom prints {missing}"
assert not unexpected, f"Unexpected axioms {unexpected}"
source_checks=[]
for p in (ROOT/"sources").glob("*.lean"):
    q=K/"TGLExt"/p.name
    assert p.read_bytes()==q.read_bytes()
    s=p.read_text("utf-8")
    # Nested Lean block comments, line comments and quoted strings excluded.
    i=0;depth=0;out=[]
    while i<len(s):
        if s.startswith("/-",i):depth+=1;i+=2
        elif depth and s.startswith("-/",i):depth-=1;i+=2
        elif depth:i+=1
        elif s.startswith("--",i):i=s.find("\n",i) if "\n" in s[i:] else len(s)
        elif s[i]=='"':
            i+=1
            while i<len(s):
                if s[i]=='\\':i+=2
                elif s[i]=='"':i+=1;break
                else:i+=1
        else:out.append(s[i]);i+=1
    code="".join(out)
    bad=re.findall(r"\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b",code,re.M)
    assert not bad,(str(p),bad)
    source_checks.append(dict(path=str(q),sha256=digest(q),bytes=q.stat().st_size,forbidden_tokens=bad,local_sha256=digest(p)))
main_print=log.rsplit("theorem TGLExt.the_same_beta_reads_four_faces",1)[-1]
consumes=("the_same_beta_reads_three_faces" in main_print and "hEOM" in main_print)
assert consumes,"Main proof not printed or supplier not consumed"
controls_files=sorted((ROOT/"semantic_controls").glob("*/RESULTADOS.json"))
assert controls_files,"No negative controls"
controls=json.loads(controls_files[-1].read_text("utf-8"))
assert controls["all_semantic"] and all(r["semantic_type_rejection"] for r in controls["controls"])
assert all(r["proved_wall"] in found for r in controls["controls"])
cmd=[str(BIN/"lake.exe"),"env","python","-c","import os,json; print(json.dumps({k:os.environ.get(k) for k in ['LEAN_PATH','LEAN_SRC_PATH','PATH']}))"]
p=subprocess.run(cmd,cwd=K,env=clean_env(),capture_output=True)
atomic(ROOT/"LAKE_ENV.stdout.txt",p.stdout);atomic(ROOT/"LAKE_ENV.stderr.txt",p.stderr)
assert p.returncode==0
lakeenv=json.loads(p.stdout.decode("utf-8"))
paths=[]
for raw in (lakeenv.get("LEAN_PATH") or "").split(os.pathsep):
    if not raw:continue
    path=Path(raw);path=path if path.is_absolute() else K/path
    path=path.resolve()
    assert path.is_relative_to(ROOT) or path.is_relative_to(BIN.parent),str(path)
    paths.append(str(path))
package_revisions=[]
for row in json.loads((K/"lake-manifest.json").read_text("utf-8"))["packages"]:
    root=K/".lake"/"packages"/row["name"]
    assert (root/".git").is_dir(), "Package gitdir must be local"
    result=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],capture_output=True,env=clean_env())
    assert result.returncode==0,result.stderr.decode("utf-8",errors="replace")
    actual=result.stdout.decode().strip()
    assert actual==row["rev"], (row["name"],actual,row["rev"])
    package_revisions.append(dict(name=row["name"],expected_revision=row["rev"],actual_revision=actual,local_root=str(root)))
outputs=[]
for family in ['TGL','TGLExt']:
    for p in (K/".lake"/"build"/"lib"/"lean"/family).rglob('*.olean'):
        outputs.append(dict(path=str(p),sha256=digest(p),bytes=p.stat().st_size))
report=dict(status="AUTHOR_KERNEL_AND_SEMANTIC_CONTROLS_VERIFIED_PENDING_INDEPENDENT_REVIEW",time_utc=stamp(),allowed_axioms=sorted(allowed),expected_names=expected,axioms={n:found[n] for n in expected},missing=missing,unexpected=unexpected,all_axioms_subset_of_trio=not missing and not unexpected,main_consumes_existing_three_faces=consumes,build_record=str(last),build_record_sha256=digest(last),lean_version=build["lean_version"],sources=source_checks,negative_controls_path=str(controls_files[-1]),negative_controls_sha256=digest(controls_files[-1]),semantic_controls_count=len(controls["controls"]),lean_search_paths=paths,compiled_local_objects=outputs,compiled_local_objects_count=len(outputs),packages_rebuilt_from_sources=False,gate_changed=False,proposed_flag="ext_pb_same_beta_four_faces_kernel_proved",flag_installed=False)
report["compiled_companions"]=[dict(path=str(p),sha256=digest(p),bytes=p.stat().st_size) for p in (K/".lake/build/lib/lean").rglob("*") if p.is_file() and any(p.name.endswith(suf) for suf in [".olean.private",".olean.server",".ilean",".trace"])]
report["package_revisions"]=package_revisions
report["toolchain_executables"]=[dict(path=str(BIN/n),sha256=digest(BIN/n)) for n in ["lean.exe","lake.exe"]]
record(ROOT/"AUDITORIA_B1_PRIME.json",report)
atomic(ROOT/"AUDITORIA_B1_PRIME.md", "[REAL — auditoria AUTORAL; revisao independente pendente]\n\n"+f"Lean: {report['lean_version']}\n\n{len(expected)} nomes consultados; axiomas efetivamente lidos, todos subconjunto do trio permitido. {len(controls['controls'])} controles recusados por Type mismatch, com paredes provadas correspondentes.\n\n"+f"Build: {last}\nControles: {controls_files[-1]}\n\n"+"Prova principal impressa: consumo direto de the_same_beta_reads_three_faces e hEOM. Fontes próprias sem tokens proibidos. Cache Mathlib/pacotes copiado; objetos locais recompilados. Sem aceite final ou alteracao de gate.\n\n"+"\n".join(f"- {n}: {found[n]}" for n in expected)+"\n")
print(json.dumps({k:report[k] for k in ['status','semantic_controls_count','all_axioms_subset_of_trio','compiled_local_objects_count']},ensure_ascii=False))
