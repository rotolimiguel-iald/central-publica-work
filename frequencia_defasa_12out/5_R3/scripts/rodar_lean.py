# -*- coding: utf-8 -*-
# Rodada 3 (5_R3) — compila UM arquivo .lean de um sandbox da rodada 3 com o toolchain COPIADO (5_R3\toolchain_v4.31.0) e
# LEAN_PATH apontando, SOMENTE LEITURA, para o .lake do tgl_kernel do Nos (+ <sandbox>\build, onde ficam os .olean
# gerados aqui). Nada e escrito fora de 5_R3. Mesmo metodo das rodadas 1 e 2 (3_KERNEL\rodada2\scripts\rodar_lean.py), com o
# sandbox como parametro. Uso:
#   rodar_lean.py <sandbox: sandbox|sandbox_r2> <arquivo relativo ao sandbox> <tag> [--olean <rel. a <sandbox>\build>]
#                 [--root <dir>]
# Grava 5_R3\logs\<tag>_SAIDA.txt e 5_R3\logs\<tag>_RECIBO.json (recusa sobrescrever um recibo existente).
import os, sys, subprocess, hashlib, json, time, datetime
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TC = os.path.join(R2, "toolchain_v4.31.0")
LEAN = os.path.join(TC, "bin", "lean.exe")
LOGS = os.path.join(R2, "logs")
K = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel\\.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    sbname, alvo, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    if sbname not in ("sandbox", "sandbox_r2"):
        raise SystemExit("FALHA VISIVEL: sandbox desconhecido: " + sbname)
    SB = os.path.join(R2, sbname)
    BUILD = os.path.join(SB, "build")
    paths = [BUILD, os.path.join(K, "build", "lib", "lean")] + \
        [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
    paths = [p for p in paths if os.path.isdir(p) or p == BUILD]
    LEAN_PATH = ";".join(paths)
    rec_path = os.path.join(LOGS, tag + "_RECIBO.json")
    if os.path.exists(rec_path):
        raise SystemExit("FALHA VISIVEL: recibo ja existe (nao sobrescrevo): " + rec_path)
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
        # raiz de pacote propria: o modulo da pedra se chama `TheUnitIsTheRank` (sem o prefixo TGLExt), para que o
        # build do sandbox NAO sombreie o pacote TGLExt do Nos na resolucao do LEAN_PATH (igual as rodadas 1 e 2).
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
        "alvo": alvo, "sandbox": SB, "tag": tag, "source_sha256": sha(sb), "source_bytes": len(sb), "inicio_utc": st,
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
    with open(rec_path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos",
                                              "ocorrencias_sorryAx", "olean_sha256")}, ensure_ascii=False))
    print(txt[:20000])


if __name__ == "__main__":
    main()
