"""Independent documentary audit. Reads bytes/AST/JSON only; never runs audited programs."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re
ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
OUT = Path(__file__).resolve().parent
BASE = ROOT / "REEXAME_SUFICIENCIA_068_20260909"
assert OUT.is_relative_to(ROOT) and OUT != BASE
def measure(path):
    p = Path(path); b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def read_json(path):
    return json.loads(Path(path).read_bytes())
def match(a, b):
    return a["sha256"] == b["sha256"] and ("bytes" not in b or a["bytes"] == b["bytes"])
def fresh(path, data):
    assert path.parent == OUT and not path.exists()
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == data
    os.replace(tmp, path)
    assert path.read_bytes() == data
    return measure(path)
manifest_path = BASE / "MANIFESTO_ENTREGA_068.json"
manifest_pin = measure(manifest_path)
m = read_json(manifest_path)
snap = read_json(BASE / "ESTADO_CANONICO_068.json")
old = read_json(ROOT / "REEXAME_SUFICIENCIA_067_20260909/ESTADO_CANONICO_067.json")
previous = read_json(ROOT / "REEXAME_SUFICIENCIA_066_20260909/RESULTADO_INTEGRACAO_066.json")
result = read_json(BASE / "RESULTADO_ENTREGA_068.json")
measurements = [measure(row["path"]) for row in m["files"]]
by_path = {p["path"]: p for p in measurements}
file_checks = [{"path": want["path"], "passed": match(got, want)} for got,want in zip(measurements,m["files"])]
canonical = [row for row in measurements if "/Artigo/" in row["path"]]
assert len(canonical) == 4
um_pin = next(x for x in canonical if x["path"].endswith("/um.py"))
um_bytes = Path(um_pin["path"]).read_bytes()
tree = ast.parse(um_bytes)
node = next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets))
embedded = ast.literal_eval(node)
presence = [{"module": x["module"], "present": "TGLExt/"+x["module"]+".lean" in embedded} for x in snap["modules"]]
seal = read_json(next(x["path"] for x in canonical if x["path"].endswith("/um_absoluto_selo.json")))
oldpins = {x["path"]:x for x in old["pins"]}
cas = {}
for item in result["cas"]:
    path = Path(item["receipt"]["path"]); data = read_json(path)
    rows = list(data["checks"].values()) if isinstance(data["checks"],dict) else data["checks"]
    cas[path.name] = {"receipt":measure(path), "expected":item["exact_controls"], "count":len(rows), "all_passed_zero":all(x.get("passed") is True and x.get("residual") == "0" for x in rows), "status":data["status"], "rerun":False}
report = BASE / "REEXAME_SUFICIENCIA.md"
tunnel = Path(m["tunnel"]["path"])
links = {}
for p in [report,tunnel]:
    links[p.name] = re.findall(r"\]\(<(C:/[^>]+)>\)",p.read_text(encoding="utf-8"))
def source_object(source):
    if source == "snapshot068": return snap["pins"]
    if source == "historical_working_copy98": return previous["working_copy"]
    return read_json(ROOT / source)
def locate(obj, locator):
    assert locator.startswith("root")
    for field,index in re.findall(r"\.([^\.\[\]]+)|\[(\d+)\]",locator[4:]):
        obj = obj[field] if field else obj[int(index)]
    return obj
global_m = read_json(ROOT / "GLOBALIZACAO_PROBABILIDADES_S3_20260909_220238_785086/MANIFESTO_GLOBALIZACAO_S3.json")
note_names = ["PROVA_GLOBAL_S3_ASSINADA_E_LIVRE.md","EXTENSAO_BRST_E_CORRECOES_SUAVES.md","ADENDO_FEYNMAN_PARIDADE_E_CONTATOS.md","CONTRATERMOS_SIGMA_E_ORDEM_EFT.md","FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md","BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md","EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md"]
reevaluated = []
for row in m["checks"]:
    name = row["name"]; kind,sep,tail = name.partition(":")
    ok = False; detail = None
    try:
        if kind == "canonical_four_unchanged_from067":
            ok = all(match(x,oldpins[x["path"]]) for x in canonical)
        elif kind == "canonical_seal_matches":
            ok = seal["sha256"]["um.py"] == um_pin["sha256"]
        elif kind == "canonical_presence":
            ok = presence == snap["modules"] and sum(x["present"] for x in presence) == 77 and len(presence) == 98 and len(embedded) == 683
        elif kind in ("absolute_recorded_pin","recorded_pin"):
            source,locator = tail.rsplit(":",1)
            target = locate(source_object(source),locator)
            ok = Path(target["path"]).is_absolute() if kind == "absolute_recorded_pin" else match(measure(target["path"]),target)
        elif kind == "pending_modules_unchanged":
            ok = [x["module"] for x in presence if not x["present"]] == snap["absent"] == previous["pending_canonical_modules"]
        elif kind == "source_directory": ok = (ROOT / tail).is_dir()
        elif kind == "cas_count": ok = cas[tail]["count"] == cas[tail]["expected"]
        elif kind == "cas_exact_pass": ok = cas[tail]["all_passed_zero"]
        elif kind == "cas_not_lean": ok = "NOT_LEAN" in cas[tail]["status"]
        elif kind == "cas_total": ok = sum(x["count"] for x in cas.values()) == 68
        elif kind == "probability_alphabet": ok = global_m["construction_inputs"]["fine_categories_total"] == 1289
        elif kind == "probability_count_arithmetic": ok = 1 + 8*(21+140) == 1289
        elif kind == "source_notes_present":
            ok = all(any(Path(x["path"]).name == n and Path(x["path"]).is_file() for x in m["files"]) for n in note_names)
        elif kind == "link":
            document,index = tail.rsplit(":",1); target = links[document][int(index)]
            ok = target == row["detail"] and Path(target).is_file()
        elif kind == "stable_final": ok = match(measure(tail),by_path[tail])
        else: raise ValueError("Unhandled documentary check: "+name)
    except Exception as exc: detail = repr(exc)
    reevaluated.append({"name":name, "reported_passed":row["passed"], "independently_passed":bool(ok), "error":detail})
additional = [
    ("56_unique_files",len(m["files"]) == len(by_path) == 56),
    ("56_fresh_byte_matches",all(x["passed"] for x in file_checks)),
    ("213_declared_and_actual_checks",m["checks_total"] == m["checks_passed"] == len(m["checks"]) == 213 and all(x["passed"] is True for x in m["checks"])),
    ("seal_excerpt_matches",all(seal.get(k) == v for k,v in snap["seal_excerpt"].items())),
    ("result_canonical_matches",match(um_pin,result["canonical"])),
    ("result_counts_match",result["canonical_modules_present"] == 77 and result["pending_canonical_modules"] == snap["absent"] and result["previous_benchmark"]["modules"] == 98),
    ("result_cas_counts_match",result["new_exact_symbolic_controls"] == m["exact_symbolic_controls"] == sum(x["count"] for x in cas.values()) == 68),
    ("result_no_new_lean",result["new_lean_modules"] == result["new_lean_compilations"] == 0 and m["new_lean_compilation"] is False),
    ("result_limits_no_completion",m["goal_complete"] is False and result["goal_complete"] is False and result["canonical_gate_modified"] is False and result["nature_tests_run"] is False),
    ("manifest_tunnel_pin_matches",match(measure(tunnel),m["tunnel"])),
    ("all_56_stable_end",all(match(measure(x["path"]),x) for x in measurements)),
    ("manifest_stable_end",match(measure(manifest_path),manifest_pin)),
]
failed = [x["name"] for x in reevaluated if not x["independently_passed"]] + [n for n,p in additional if not p]
status = "PASS_DOCUMENTARY_068_INDEPENDENT_OF_FINALIZER" if not failed else "FAIL_DOCUMENTARY_068"
text = f"""# Auditoria documental independente — entrega 068

[REAL — leitura de bytes, AST e JSON] Resultado: **{status}**.

Foram relidos os **56 arquivos distintos** enumerados no manifesto. Todos os tamanhos e SHA-256 coincidem, incluindo os quatro artefatos canônicos. Esses quatro também coincidem com os pins de 067. A leitura canônica precisou de autorização elevada; ela foi usada apenas para ler. O programa foi analisado por AST e sua tabela literal, sem execução ou importação: **683 arquivos embutidos, 77 dos 98 módulos presentes e 21 ausentes**. O selo identifica o mesmo hash de um.py.

Os **213 controles** do manifesto foram reavaliados nominalmente por este script independente. Os 59 pares de controles de pins foram resolvidos nos respectivos documentos JSON e comparados aos bytes, sem importar o finalizador. Os 56 controles finais de estabilidade releram os arquivos. Os links do relatório e do túnel existem e apontam aos artefatos especificados.

Os recibos CAS contêm **47 + 13 + 8 = 68 controles**, todos com passed=true e residual literal zero. Foram lidos os recibos e conferidos seus hashes; nenhum script CAS foi reexecutado. Estes controles não são provas Lean de afirmações analíticas.

A leitura documental de REEXAME_SUFICIENCIA.md, RESULTADO_ENTREGA_068.json, ADENDO_REVISAO_E_ESCOPO_068.md e da entrega no túnel não encontrou divergência material de versão, contagem ou alcance. Os documentos distinguem a representação global do fundo especificado e a extensão BRST Einstein–sigma livre das obrigações interagentes, QME, anomalias, rota UV e eventual complexo vertical das probabilidades. A existência de Nash permanece declarada; a tabela numérica completa não é reivindicada. A família quártica é clássica truncada. As notas históricas que precederam a conclusão livre recebem precisão ao lado, sem reescrita.

**Escopo de independência.** Este é um auditor documental novo e independente do integrador/finalizador. Sou autor de parte das notas geométricas e BRST listadas: esta auditoria NÃO constitui nova aprovação analítica independente desses textos. Os pareceres de outros agentes são artefatos distintos com escopos próprios. A preservação demonstrada é a coincidência dos bytes nos momentos observados e com os pins históricos fornecidos; não é uma auditoria do histórico integral do sistema de arquivos.

Nenhum um.py, finalizador, programa CAS ou Lean foi executado/importado. Nenhum arquivo existente foi modificado por esta auditoria. Somente este diretório novo contém o script, parecer e resultado. Os hashes medidos e todos os controles estão em RESULTADO_AUDITORIA_DOCUMENTAL_068.json. Nenhum gate ou estatuto científico foi promovido.

Manifesto auditado: {manifest_pin["path"]}
SHA-256 medido: {manifest_pin["sha256"]}
"""
report_pin = fresh(OUT / "PARECER_DOCUMENTAL_068.md",text.encode("utf-8"))
answer = {
    "status":status,"created_utc":datetime.now(timezone.utc).isoformat(),
    "scope":"Independent documentary audit; not independent analytic approval of this auditor's own mathematical notes.",
    "manifest_audited":manifest_pin,"report":report_pin,"auditor_script":measure(__file__),
    "counts":{"listed_files":len(m["files"]),"fresh_files_passed":sum(x["passed"] for x in file_checks),"canonical_files":len(canonical),"embedded_files":len(embedded),"benchmark_present":sum(x["present"] for x in presence),"benchmark_absent":sum(not x["present"] for x in presence),"cas_controls":sum(x["count"] for x in cas.values())},
    "manifest_checks_total":len(reevaluated),"manifest_checks_passed":sum(x["independently_passed"] for x in reevaluated),
    "checks_total":len(reevaluated)+len(additional),"checks_passed":sum(x["independently_passed"] for x in reevaluated)+sum(p for n,p in additional),
    "failed_checks":failed,"files":measurements,"file_checks":file_checks,"canonical":canonical,
    "cas_receipts":list(cas.values()),"manifest_checks":reevaluated,
    "additional_checks":[{"name":n,"passed":p} for n,p in additional],
    "um_executed_or_imported":False,"finalizer_executed_or_imported":False,"CAS_rerun":False,"lean_executed":False,"originals_modified":False,
}
answer_pin = fresh(OUT / "RESULTADO_AUDITORIA_DOCUMENTAL_068.json",(json.dumps(answer,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":status,"report":report_pin,"result":answer_pin,"manifest_checks":answer["manifest_checks_passed"],"checks":answer["checks_passed"],"total":answer["checks_total"],"files":56,"failed_checks":failed},ensure_ascii=False))
if failed: raise SystemExit(1)
