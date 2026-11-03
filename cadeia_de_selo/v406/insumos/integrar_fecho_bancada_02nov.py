# -*- coding: utf-8 -*-
"""R3 formal do fechamento (02/11/2026, gerência c1): integrar no SANDBOX (cópia do kernel v405, C:\\t\\k405c\\final) os módulos da
bancada que habitam `physicalFockCertificate` (F1.FECHO_20261015, recibo de 16/10), recompilando-os do FONTE, em ordem de dependência,
em paralelo, com manifesto por hash e log por módulo. Fail-closed: hash divergente, conflito com o kernel ou erro de compilação
param o ramo e ficam visíveis. Nada toca o kernel do Nós, o um.py, a bancada (só leitura) ou o gate.

Entrada: o RECIBO da bancada (lista `dependencies` com caminho+sha256 de cada .lean compilado).
Saída: <LOGDIR>/MANIFEST.json, SUMMARY.json, <modulo>.log, CHECK_axioms.txt, DONE.txt
"""
import ctypes, datetime, hashlib, json, os, re, subprocess, sys, threading, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
RECEIPT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\orbital_rotation\attempts\20261016T210640_174717Z\RECEIPT.json")
SANDBOX = Path(r"C:\t\k405c\final")
SRC = SANDBOX / "TGLExt" / "F1Fecho394"
LIB = SANDBOX / ".lake" / "build" / "lib" / "lean" / "TGLExt" / "F1Fecho394"
LAKE = Path(r"C:\Users\rotol\.elan\bin\lake.exe")
LOGDIR = Path(r"C:\IALD\Central de Patentes\work\fechamento_02nov") / ("integracao_R3_" + TS)
LOGDIR.mkdir(parents=True, exist_ok=True)
LOG = LOGDIR / "DRIVER.log"
PREFIX = "TGLExt.F1Fecho394."
ROOT_MODULE = "CanonicalFockModularCoreInputR1"
lock = threading.Lock()

def log(msg):
    line = datetime.datetime.now().strftime("%H:%M:%S") + " " + msg
    with lock:
        print(line, flush=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def ram_gb() -> float:
    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    m = MS(); m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullTotalPhys / 2**30

# ---------- 1. o manifesto da bancada, conferido por hash
rec = json.loads(RECEIPT.read_text(encoding="utf-8"))
assert rec.get("exit_code") == 0, rec.get("exit_code")
fontes = {}
for x in rec["dependencies"]:
    p = Path(x["path"])
    if p.suffix.lower() != ".lean":
        continue
    h = sha(p)
    assert h == x["sha256"], ("hash divergente", p)
    fontes[p.stem] = {"path": str(p), "sha256": h}
# a própria raiz compilada no recibo
raiz = Path(rec["source"]["path"]); assert raiz.stem == ROOT_MODULE
assert sha(raiz) == rec["source"]["sha256"]
fontes[ROOT_MODULE] = {"path": str(raiz), "sha256": rec["source"]["sha256"]}
names = set(fontes)
# os nomes do KERNEL vêm do Nós (só leitura), não do sandbox: o sandbox já pode conter os novos gravados numa rodada anterior
KERNEL_NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\F1Fecho394")
kernel_names = {f.stem for f in KERNEL_NOS.glob("*.lean")}
def mesmo_conteudo(a: str, b: str) -> bool:
    """igualdade a menos de linhas em branco e espaços finais (a 1ª rodada marcou 149 «conflitos» que eram uma linha em branco)."""
    la = [l.rstrip() for l in a.splitlines() if l.strip()]
    lb = [l.rstrip() for l in b.splitlines() if l.strip()]
    return la == lb
log(f"recibo ok: {len(fontes)} fontes conferidas por hash; kernel F1Fecho394 tem {len(kernel_names)} módulos; RAM {ram_gb():.0f} GB; cpus {os.cpu_count()}")

IMPORT_RE = re.compile(r"^import\s+(\S+)\s*$")
def normaliza(text: str):
    """reescreve imports planos para o prefixo do kernel e remove linhas #eval (instrumentação); devolve (texto, imports, n_eval)."""
    out, imps, n_eval = [], [], 0
    em_eval = False  # bloco `#eval … do` multilinha: pula também as linhas indentadas/vazias que o continuam (lição da 1ª rodada)
    for line in text.splitlines():
        if em_eval:
            if line.strip() == "" or line[:1].isspace():
                continue
            em_eval = False
        m = IMPORT_RE.match(line)
        if m:
            tok = m.group(1)
            if tok.startswith(PREFIX):
                base = tok[len(PREFIX):]
            elif tok in names or tok in kernel_names:
                base = tok; tok = PREFIX + tok
            else:
                base = None
            if base is not None:
                imps.append(base)
            out.append("import " + tok); continue
        if line.lstrip().startswith("#eval"):
            n_eval += 1; em_eval = True; continue
        out.append(line)
    return "\n".join(out) + "\n", imps, n_eval

# ---------- 2. classificar: idêntico ao kernel / conflito / novo
manifest = {}
novos = {}
for name, info in sorted(fontes.items()):
    text = Path(info["path"]).read_text(encoding="utf-8")
    norm, imps, n_eval = normaliza(text)
    entry = {"fonte": info["path"], "sha256_fonte": info["sha256"], "imports_f1fecho": imps, "n_eval_removidos": n_eval}
    if name in kernel_names:
        ktext = (SRC / (name + ".lean")).read_text(encoding="utf-8")
        knorm, _, _ = normaliza(ktext)
        if mesmo_conteudo(knorm, norm):
            entry.update(status="kernel_identico", olean=str(LIB / (name + ".olean")), olean_existe=(LIB / (name + ".olean")).exists())
        else:
            entry.update(status="CONFLITO_com_kernel", olean=str(LIB / (name + ".olean")))
            log(f"CONFLITO: {name} difere do kernel; o kernel prevalece no sandbox (não sobrescrito)")
    else:
        dest = SRC / (name + ".lean")
        if dest.exists() and mesmo_conteudo(dest.read_text(encoding="utf-8"), norm):
            entry.update(status="novo_ja_gravado")
        else:
            assert not dest.exists() or dest.read_text(encoding="utf-8").startswith(norm[:0]) , name
            tmp = dest.with_suffix(".lean.tmp")
            tmp.write_text(norm, encoding="utf-8"); os.replace(tmp, dest)
            entry.update(status="novo_gravado")
        entry["sha256_gravado"] = sha(dest)
        novos[name] = imps
    manifest[name] = entry
n_id = sum(1 for e in manifest.values() if e["status"] == "kernel_identico")
n_conf = sum(1 for e in manifest.values() if e["status"] == "CONFLITO_com_kernel")
log(f"classificação: {n_id} idênticos ao kernel, {n_conf} conflitos, {len(novos)} novos gravados no sandbox")
(LOGDIR / "MANIFEST_pre.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- 3. ordem de dependência entre os novos (imports para módulos já no kernel não bloqueiam)
pend = {n: {d for d in imps if d in novos} for n, imps in novos.items()}
done, failed, blocked = {}, {}, {}
J = 3 if ram_gb() < 40 else 6
# ambiente do lake lido UMA vez (o `lake env` por módulo, em paralelo, derrubou os lean com STATUS_CONTROL_C_EXIT na 1ª rodada)
_env = subprocess.run([str(LAKE), "env", sys.executable, "-c", "import os,json;print(json.dumps({k:os.environ[k] for k in ('LEAN_PATH','PATH','LEAN_SYSROOT','LEAN') if k in os.environ}))"],
                      cwd=str(SANDBOX), capture_output=True, stdin=subprocess.DEVNULL,
                      creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)  # sem console: sem janela na tela do operador
_envd = json.loads(_env.stdout.decode("utf-8", "replace").strip().splitlines()[-1])
ENV = dict(os.environ); ENV.update(_envd)
LEAN_EXE = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
assert LEAN_EXE.exists(), LEAN_EXE
tc = (SANDBOX / "lean-toolchain").read_text(encoding="utf-8").strip()
assert "4.31.0" in tc, tc
log(f"paralelismo {J}; toolchain {tc}; LEAN_PATH com {len(_envd.get('LEAN_PATH','').split(os.pathsep))} entradas")
# retomada: o que já tem .olean mais novo que a fonte conta como compilado
for n in list(pend):
    o = LIB / (n + ".olean"); s = SRC / (n + ".lean")
    if o.exists() and o.stat().st_mtime > s.stat().st_mtime:
        done[n] = {"rc": 0, "segundos": 0.0, "olean_sha256": sha(o), "retomado": True}
        del pend[n]
for n, d in pend.items():
    d.difference_update(done)
log(f"retomados {len(done)}; a compilar {len(pend)}")

def compila(name):
    src = SRC / (name + ".lean"); olean = LIB / (name + ".olean"); ilean = LIB / (name + ".ilean")
    cmd = [str(LEAN_EXE), "-R", str(SANDBOX), "-o", str(olean), "-i", str(ilean), str(src)]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(SANDBOX), capture_output=True, env=ENV, stdin=subprocess.DEVNULL,
                       creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)
    dt = time.time() - t0
    out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
    (LOGDIR / (name + ".log")).write_text(out, encoding="utf-8")
    sorry = ("sorryAx" in out) or ("declaration uses 'sorry'" in out)
    return name, r.returncode, dt, sorry, (sha(olean) if olean.exists() else None), out.lower().count("error")

inicio = time.time()
with ThreadPoolExecutor(max_workers=J) as ex:
    futs = {}
    while pend or futs:
        prontos = [n for n, d in pend.items() if not d and n not in futs]
        for n in prontos:
            futs[ex.submit(compila, n)] = n
            del pend[n]
        if not futs:
            # o que resta está bloqueado por falha
            for n in list(pend):
                blocked[n] = sorted(pend[n]); del pend[n]
            break
        for f in as_completed(list(futs)):
            name, rc, dt, sorry, oh, nerr = f.result(); del futs[f]
            if rc == 0 and not sorry:
                done[name] = {"rc": rc, "segundos": round(dt, 1), "olean_sha256": oh}
                for d in pend.values(): d.discard(name)
                log(f"ok  {name} ({dt:.0f}s) restam {len(pend)} pendentes")
            else:
                failed[name] = {"rc": rc, "segundos": round(dt, 1), "sorry": sorry, "erros": nerr}
                log(f"FALHA {name} rc={rc} sorry={sorry} erros={nerr}")
                # dependentes ficam bloqueados
                for n2, d in list(pend.items()):
                    if name in d:
                        blocked[n2] = sorted(d); del pend[n2]
            break  # volta a submeter os que ficaram prontos

for name in done: manifest[name].update(status="novo_compilado", **done[name])
for name in failed: manifest[name].update(status="FALHA_compilacao", **failed[name])
for name in blocked: manifest[name].update(status="BLOQUEADO_por_falha", bloqueado_por=blocked[name])

# ---------- 4. a conferência: axiomas do certificado físico e do habitante dos 21 campos
check = SANDBOX / "_check_fecho_02nov.lean"
check.write_text("import TGLExt.F1Fecho394." + ROOT_MODULE + "\n"
                 "#print axioms F1Fecho.CanonicalFockModularCoreInputR1.modularCoreInput\n"
                 "#print axioms F1Fecho.CanonicalFockModularCoreInputR1.physicalModularCoreInput\n"
                 "#print axioms F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate\n"
                 "#print axioms F1Fecho.CanonicalFockModularCoreInputR1.physical_trace\n", encoding="utf-8")
axioms_out = ""
if ROOT_MODULE in done:
    r = subprocess.run([str(LEAN_EXE), "-R", str(SANDBOX), str(check)], cwd=str(SANDBOX), capture_output=True, env=ENV, stdin=subprocess.DEVNULL,
                       creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)
    axioms_out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace") + f"\nrc {r.returncode}\n"
    (LOGDIR / "CHECK_axioms.txt").write_text(axioms_out, encoding="utf-8")
    log("conferência de axiomas: " + axioms_out.replace("\n", " ")[:400])
else:
    log("raiz NÃO compilada: sem conferência de axiomas")

summary = {"ts": TS, "recibo": str(RECEIPT), "recibo_sha256": sha(RECEIPT), "sandbox": str(SANDBOX), "fontes": len(fontes),
           "kernel_identicos": n_id, "conflitos": n_conf, "novos": len(novos), "compilados": len(done), "falhas": len(failed), "bloqueados": len(blocked),
           "segundos_total": round(time.time() - inicio, 1), "paralelismo": J, "raiz_compilada": ROOT_MODULE in done,
           "axiomas_trio_no_certificado": ("physicalFockCertificate' depends on axioms: [propext, Classical.choice, Quot.sound]" in " ".join(axioms_out.split())),
           "falhas_lista": sorted(failed), "bloqueados_lista": sorted(blocked), "conflitos_lista": sorted(n for n, e in manifest.items() if e["status"] == "CONFLITO_com_kernel")}
(LOGDIR / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
(LOGDIR / "SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
(LOGDIR / "DONE.txt").write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")
log("FIM " + json.dumps(summary, ensure_ascii=False))
