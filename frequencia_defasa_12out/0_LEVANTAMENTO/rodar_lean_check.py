# -*- coding: utf-8 -*-
# Roda as duas sondas Lean do levantamento com o toolchain COPIADO para o sandbox e LEAN_PATH apontando
# (somente leitura) para o .lake do tgl_kernel do Nos. Nao escreve .olean (sem -o). Grava saidas e recibo em lean_check/.
import os, sys, subprocess, hashlib, json, time, datetime
AQUI = os.path.dirname(os.path.abspath(__file__))
TC = os.path.join(AQUI, "sandbox", "toolchain_v4.31.0")
LEAN = os.path.join(TC, "bin", "lean.exe")
K = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel\\.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
paths = [os.path.join(K, "build", "lib", "lean")] + [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
paths = [p for p in paths if os.path.isdir(p)]
LEAN_PATH = ";".join(paths)
OUT = os.path.join(AQUI, "lean_check")
alvos = sys.argv[1:] or ["LevantamentoF1FrequenciaCheck.lean", "LevantamentoF1FrequenciaMathlibProbe.lean"]
env = dict(os.environ)
env["LEAN_PATH"] = LEAN_PATH
for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN"):
    env.pop(k, None)
ver = subprocess.run([LEAN, "--version"], capture_output=True, text=True, env=env)
recibos = []
for a in alvos:
    src = os.path.join(OUT, a)
    sb = open(src, "rb").read()
    t0 = time.time()
    st = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run([LEAN, src], capture_output=True, env=env, cwd=OUT)
    dt = time.time() - t0
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    nome_saida = a.replace(".lean", "_SAIDA.txt")
    with open(os.path.join(OUT, nome_saida), "wb") as fh:
        fh.write(saida)
    txt = saida.decode("utf-8", errors="replace")
    n_ax = txt.count("depends on axioms")
    trio = txt.count("depends on axioms: [propext, Classical.choice, Quot.sound]")
    outros = [ln for ln in txt.splitlines() if "depends on axioms" in ln and "[propext, Classical.choice, Quot.sound]" not in ln]
    sorry = txt.count("sorryAx")
    rec = {"alvo": a, "source_sha256": hashlib.sha256(sb).hexdigest(), "inicio_utc": st, "segundos": round(dt, 2),
           "exit_code": r.returncode, "saida": nome_saida, "saida_sha256": hashlib.sha256(saida).hexdigest(),
           "n_print_axioms": n_ax, "n_no_trio": trio, "linhas_fora_do_trio": outros, "ocorrencias_sorryAx": sorry,
           "n_erros": txt.count(": error"), "comando": [LEAN, src]}
    recibos.append(rec)
    print(json.dumps({k: rec[k] for k in ("alvo", "exit_code", "segundos", "n_print_axioms", "n_no_trio", "ocorrencias_sorryAx", "n_erros")}, ensure_ascii=False))
recibo = {"toolchain": ver.stdout.strip(), "toolchain_copiado_de": "~/.elan/toolchains/leanprover--lean4---v4.31.0 (bin + lib/lean/{Init,Std,Lean,Lake})",
          "lean_exe": LEAN, "LEAN_PATH": LEAN_PATH, "sem_saida_olean": True, "recibos": recibos}
with open(os.path.join(OUT, "RECIBO_LEAN_CHECK.json"), "w", encoding="utf-8") as fh:
    json.dump(recibo, fh, ensure_ascii=False, indent=1)
