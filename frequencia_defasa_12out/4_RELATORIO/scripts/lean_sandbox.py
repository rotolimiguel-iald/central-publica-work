# -*- coding: utf-8 -*-
# Sandbox Lean do REDATOR da F1.FREQUENCIA (so dentro de 4_RELATORIO\L). Metodo das auditorias anteriores:
#   copiar  : copia (so leitura na origem) o toolchain v4.31.0 do elan para L\tc (bin + lib\lean\{Init,Std,Lean,Lake}*)
#   rodar   : compila UM arquivo de L com o toolchain copiado e LEAN_PATH (so leitura) para o .lake do tgl_kernel do Nos
#             (+ L\build, onde fica o .olean gerado aqui); recibo e saida em 4_RELATORIO\lean_logs
#   apagar  : apaga toolchain, build, .lake e caches copiados (prefixo \\?\ para caminhos longos)
# Nada e escrito fora de 4_RELATORIO. Uso: lean_sandbox.py copiar | rodar <alvo> <tag> [--olean N] [--root D] | apagar
import os, sys, shutil, subprocess, hashlib, json, time, datetime

REL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # 4_RELATORIO
SB = os.path.join(REL, "L")
TC = os.path.join(SB, "tc")
BUILD = os.path.join(SB, "build")
LOGS = os.path.join(REL, "lean_logs")
ORIG_TC = os.path.expanduser("~") + "\\.elan\\toolchains\\leanprover--lean4---v4.31.0"
MODS = ("Init", "Std", "Lean", "Lake")
K = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel\\.lake"


def L(p):
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def sha(b):
    return hashlib.sha256(b).hexdigest()


def copiar():
    t0 = time.time()
    dest = L(TC)
    if os.path.exists(dest):
        raise SystemExit("FALHA VISIVEL: L\\tc ja existe")
    os.makedirs(dest)
    shutil.copytree(L(os.path.join(ORIG_TC, "bin")), os.path.join(dest, "bin"))
    lib_o = L(os.path.join(ORIG_TC, "lib", "lean"))
    lib_d = os.path.join(dest, "lib", "lean")
    os.makedirs(lib_d)
    n = 0
    for fn in sorted(os.listdir(lib_o)):
        if fn.split(".")[0] not in MODS:
            continue
        p = os.path.join(lib_o, fn)
        if os.path.isdir(p):
            shutil.copytree(p, os.path.join(lib_d, fn))
        else:
            shutil.copy2(p, os.path.join(lib_d, fn))
        n += 1
    tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, dns, fns in os.walk(dest) for f in fns)
    print(json.dumps({"copiado_de": ORIG_TC, "copiado_para": dest, "entradas_lib": n, "bytes": tot,
                      "segundos": round(time.time() - t0, 1)}, ensure_ascii=False))


def rodar(argv):
    alvo, tag = argv[0], argv[1]
    olean = os.path.join(BUILD, argv[argv.index("--olean") + 1]) if "--olean" in argv else None
    pk = sorted(os.listdir(os.path.join(K, "packages")))
    paths = [BUILD, os.path.join(K, "build", "lib", "lean")] + \
            [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in pk]
    paths = [p for p in paths if os.path.isdir(p) or p == BUILD]
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    src = open(os.path.join(SB, alvo), "rb").read()
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH", "LAKE", "LAKE_HOME"):
        env.pop(k, None)
    cmd = [os.path.join(TC, "bin", "lean.exe")]
    if "--root" in argv:
        cmd += ["--root=" + argv[argv.index("--root") + 1]]
    if olean:
        cmd += ["-o", olean]
    cmd += [alvo]
    t0 = time.time()
    ini = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
    dt = time.time() - t0
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    for nome in (tag + "_SAIDA.txt", tag + "_RECIBO.json"):
        if os.path.exists(os.path.join(LOGS, nome)):
            raise SystemExit("FALHA VISIVEL: %s ja existe (nao sobrescrevo)" % nome)
    open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb").write(saida)
    txt = saida.decode("utf-8", errors="replace")
    rec = {"alvo": alvo, "tag": tag, "source_sha256": sha(src), "source_bytes": len(src), "inicio_utc": ini,
           "segundos": round(dt, 2), "exit_code": r.returncode, "saida_sha256": sha(saida),
           "n_erros": txt.count(": error"), "n_avisos": txt.count(": warning"),
           "ocorrencias_sorryAx": txt.count("sorryAx"), "declaration_uses_sorry": txt.count("declaration uses 'sorry'"),
           "comando": cmd, "cwd": SB, "LEAN_PATH": env["LEAN_PATH"]}
    if olean and os.path.exists(olean):
        ob = open(olean, "rb").read()
        rec["olean_bytes"] = len(ob)
        rec["olean_sha256"] = sha(ob)
    open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos", "ocorrencias_sorryAx",
                                              "saida_sha256", "olean_bytes", "olean_sha256")}, ensure_ascii=False))
    print(txt[:4000])


def apagar():
    out = {}
    for sub in ("tc", "build"):
        raiz = L(os.path.join(SB, sub))
        if os.path.exists(raiz):
            shutil.rmtree(raiz)
        out[sub] = {"existe_depois": os.path.exists(raiz)}
    for dp, dns, fns in os.walk(L(SB)):
        for d in list(dns):
            if d in (".lake", "__pycache__", ".cache"):
                shutil.rmtree(os.path.join(dp, d))
                out.setdefault("caches_apagados", []).append(os.path.join(dp, d))
    restos = [os.path.join(dp, f) for dp, dns, fns in os.walk(L(REL)) for f in fns
              if f.endswith((".ilean", ".olean.private", ".olean.server", ".ir", ".c", ".hash", ".trace"))
              or (f.endswith(".olean") and "olean_candidata" not in dp)]
    out["artefatos_de_build_restantes_fora_de_olean_candidata"] = restos
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "copiar":
        copiar()
    elif cmd == "rodar":
        rodar(sys.argv[2:])
    elif cmd == "apagar":
        apagar()
    else:
        raise SystemExit("uso: copiar | rodar <alvo> <tag> [--olean N] [--root D] | apagar")
