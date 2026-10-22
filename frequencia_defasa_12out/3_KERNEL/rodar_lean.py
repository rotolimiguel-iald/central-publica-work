# -*- coding: utf-8 -*-
# Compila UM arquivo .lean do sandbox do 3_KERNEL com o toolchain COPIADO (sandbox\toolchain_v4.31.0) e LEAN_PATH
# apontando, SOMENTE LEITURA, para o .lake do tgl_kernel do Nos (+ sandbox\build, onde ficam os .olean gerados aqui).
# Nada e escrito fora de 3_KERNEL. Uso:
#   rodar_lean.py <arquivo relativo a sandbox> <tag> [--olean <caminho relativo a sandbox\build>] [--root <dir>]
# Grava logs\<tag>_SAIDA.txt e logs\<tag>_RECIBO.json.
import os, sys, subprocess, hashlib, json, time, datetime
AQUI = os.path.dirname(os.path.abspath(__file__))
SB = os.path.join(AQUI, "sandbox")
TC = os.path.join(SB, "toolchain_v4.31.0")
LEAN = os.path.join(TC, "bin", "lean.exe")
BUILD = os.path.join(SB, "build")
LOGS = os.path.join(AQUI, "logs")
K = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel\\.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
paths = [BUILD, os.path.join(K, "build", "lib", "lean")] + [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
paths = [p for p in paths if os.path.isdir(p) or p == BUILD]
LEAN_PATH = ";".join(paths)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    alvo, tag = sys.argv[1], sys.argv[2]
    olean = None
    if "--olean" in sys.argv:
        olean = os.path.join(BUILD, sys.argv[sys.argv.index("--olean") + 1])
        os.makedirs(os.path.dirname(olean), exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    src = os.path.join(SB, alvo)
    sb = open(src, "rb").read()
    env = dict(os.environ)
    env["LEAN_PATH"] = LEAN_PATH
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
        env.pop(k, None)
    cmd = [LEAN]
    if "--root" in sys.argv:
        # raiz de pacote propria no sandbox: o modulo da pedra se chama `TheUnitIsTheRank` (sem o prefixo TGLExt)
        # para que sandbox/build NAO sombreie o pacote TGLExt do Nos na resolucao do LEAN_PATH.
        cmd += ["--root=" + sys.argv[sys.argv.index("--root") + 1]]
    if olean:
        cmd += ["-o", olean]
    cmd += [alvo]
    t0 = time.time()
    st = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
    dt = time.time() - t0
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    with open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb") as fh:
        fh.write(saida)
    txt = saida.decode("utf-8", errors="replace")
    rec = {
        "alvo": alvo, "tag": tag, "source_sha256": sha(sb), "source_bytes": len(sb), "inicio_utc": st,
        "segundos": round(dt, 2), "exit_code": r.returncode, "saida": "logs\\" + tag + "_SAIDA.txt",
        "saida_sha256": sha(saida), "n_erros": txt.count(": error"), "n_avisos": txt.count(": warning"),
        "ocorrencias_sorryAx": txt.count("sorryAx"), "declaration_uses_sorry": txt.count("declaration uses 'sorry'"),
        "comando": cmd, "cwd": SB, "LEAN_PATH": LEAN_PATH,
    }
    if olean and os.path.exists(olean):
        ob = open(olean, "rb").read()
        rec["olean"] = olean
        rec["olean_bytes"] = len(ob)
        rec["olean_sha256"] = sha(ob)
    with open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos", "ocorrencias_sorryAx", "olean_sha256")}, ensure_ascii=False))
    print(txt[:20000])


if __name__ == "__main__":
    main()
