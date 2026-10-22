# -*- coding: utf-8 -*-
"""Compila UM .lean do sandbox curto C:/t/mo2/src com o lean v4.31.0 COPIADO para C:/t/mo2/toolchain (sem lake).
LEAN_PATH: PRIMEIRO a sobreposicao C:/t/mo2/ov (copia verificada dos .olean do kernel do Nos + candidatas compiladas
aqui), depois os pacotes do .lake do Nos, SO LEITURA. -o so dentro do sandbox. Logs em 6_R2_CORRECOES/logs.
Com --olean grava C:/t/mo2/ov/TGLExt/<Modulo>.olean (recusa sobrescrever).
Uso: rodar_lean.py <fonte relativa a src> <tag> [--olean]"""
import os, sys, subprocess, hashlib, json, time, datetime, re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = "C:/t/mo2"
SRC = SB + "/src"
OV = SB + "/ov"
LOGS = os.path.join(AQUI, "logs")
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
    olean = "--olean" in sys.argv[3:]
    paths = [OV] + [K + "/packages/" + p + "/.lake/build/lib/lean" for p in PK]
    paths = [p for p in paths if os.path.isdir(p)]
    if not os.path.isdir(OV) or not os.path.isfile(LEAN):
        print("FALHA VISIVEL: sandbox incompleto"); sys.exit(2)
    src = SRC + "/" + alvo
    sb = open(src, "rb").read()
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(p.replace("/", chr(92)) for p in paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
        env.pop(k, None)
    cmd = [LEAN]
    out_olean = None
    if olean:
        assert alvo.startswith("TGLExt/") and alvo.endswith(".lean")
        out_olean = OV + "/TGLExt/" + os.path.basename(alvo)[:-5] + ".olean"
        if os.path.exists(out_olean):
            print("FALHA VISIVEL: .olean ja existe: " + out_olean); sys.exit(2)
        cmd += ["--root=" + SRC, "-o", out_olean]
    cmd.append(alvo)
    t0 = time.time()
    st = datetime.datetime.now(datetime.timezone.utc).isoformat()
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
    rec = {"alvo": alvo, "tag": tag, "source_sha256": hashlib.sha256(sb).hexdigest(), "source_bytes": len(sb),
           "inicio_utc": st, "segundos": round(dt, 2), "exit_code": r.returncode,
           "saida_sha256": hashlib.sha256(saida).hexdigest(), "n_erros": len(re.findall(r":\d+:\d+: error", txt)),
           "n_avisos": len(re.findall(r":\d+:\d+: warning", txt)),
           "declaration_uses_sorry": txt.count("declaration uses 'sorry'") + txt.count("sorryAx"),
           "n_print_axioms": len(axs), "fora_do_trio": fora, "axiomas": axs,
           "lean": LEAN, "lean_sha256": sha(LEAN), "LEAN_PATH": paths, "comando": cmd}
    if out_olean and os.path.exists(out_olean):
        rec["olean"] = out_olean
        rec["olean_sha256"] = sha(out_olean)
        rec["olean_bytes"] = os.path.getsize(out_olean)
    elif out_olean:
        rec["olean"] = None
    json.dump(rec, open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos",
                                              "declaration_uses_sorry", "n_print_axioms", "olean_sha256")}))
    print(txt[:14000])
    sys.exit(0 if r.returncode == 0 else 1)


if __name__ == "__main__":
    main()
