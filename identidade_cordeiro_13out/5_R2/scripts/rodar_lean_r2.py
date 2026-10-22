# -*- coding: utf-8 -*-
"""Compila UM .lean no sandbox C:/t/id2/src com o toolchain v4.31.0 COPIADO para C:/t/id2/toolchain.
LEAN_PATH: o .lake do Nos (build/lib/lean + pacotes), SO LEITURA; com --ov, C:/t/id2/ov vem na frente (sobreposicao:
copia dos .olean do TGLExt do Nos + as pedras compiladas aqui, para arquivos que IMPORTAM a pedra).
Com --olean, -o grava SO em C:/t/id2/out. Logs em 5_R2/logs. Uso: rodar_lean_r2.py <rel em src> <tag> [--olean] [--ov]"""
import os, sys, subprocess, hashlib, json, time, datetime, re
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(R2, "logs")
SB = "C:/t/id2"
SRC = SB + "/src"
LEAN = SB + "/toolchain/bin/lean.exe"
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def main():
    alvo, tag = sys.argv[1], sys.argv[2]
    paths = [K + "/build/lib/lean"] + [K + "/packages/" + p + "/.lake/build/lib/lean" for p in PK]
    if "--ov" in sys.argv[3:]:
        paths = [SB + "/ov"] + paths
    paths = [p for p in paths if os.path.isdir(p)]
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
        env.pop(k, None)
    cmd = [LEAN]
    out_olean = None
    if "--olean" in sys.argv[3:]:
        out_olean = SB + "/out/" + alvo[:-5] + ".olean"
        os.makedirs(os.path.dirname(out_olean), exist_ok=True)
        cmd += ["--root=" + SRC, "-o", out_olean]
    cmd.append(alvo)
    src_bytes = open(SRC + "/" + alvo, "rb").read()
    st = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SRC)
    dt = time.time() - t0
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    os.makedirs(LOGS, exist_ok=True)
    open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb").write(saida)
    txt = saida.decode("utf-8", errors="replace")
    axs = {}
    for decl, vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", txt, re.S):
        axs[decl] = [v.strip() for v in vals.replace("\n", " ").split(",") if v.strip()]
    for decl in re.findall(r"'([^']+)' does not depend on any axioms", txt):
        axs[decl] = []
    fora = {k: v for k, v in axs.items() if not set(v) <= TRIO}
    rec = {"alvo": alvo, "tag": tag, "source_sha256": hashlib.sha256(src_bytes).hexdigest(),
           "source_bytes": len(src_bytes), "inicio_utc": st, "segundos": round(dt, 2), "exit_code": r.returncode,
           "saida_sha256": hashlib.sha256(saida).hexdigest(), "n_erros": len(re.findall(r":\d+:\d+: error", txt)),
           "n_avisos": len(re.findall(r":\d+:\d+: warning", txt)),
           "declaration_uses_sorry_crase": txt.count("declaration uses `sorry`"),
           "declaration_uses_sorry_aspas": txt.count("declaration uses 'sorry'"),
           "sorryAx_no_texto": txt.count("sorryAx"),
           "n_print_axioms": len(axs), "fora_do_trio": fora, "lean": LEAN, "LEAN_PATH": paths, "comando": cmd}
    if out_olean and os.path.exists(out_olean):
        rec["olean"] = out_olean
        rec["olean_sha256"] = sha(out_olean)
        rec["olean_bytes"] = os.path.getsize(out_olean)
    json.dump(rec, open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos",
                                              "declaration_uses_sorry_crase", "sorryAx_no_texto", "n_print_axioms",
                                              "fora_do_trio", "olean_sha256")}))
    print(txt[:15000])


if __name__ == "__main__":
    main()
