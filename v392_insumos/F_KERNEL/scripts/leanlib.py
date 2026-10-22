# -*- coding: utf-8 -*-
"""Biblioteca do sandbox F_KERNEL (exame de 12/10/2026, frente kernel da v392). [2a execucao: os arquivos da 1a
foram apagados por um erro meu na limpeza (Remove-Item sobre -Include ignorado); os scripts foram reescritos iguais]

Roda o lean.exe v4.31.0 COPIADO para o sandbox (F_KERNEL\\tc), com LEAN_PATH so-leitura apontando para os .olean
do kernel do Nos e dos pacotes (mathlib etc.), ou para a sobreposicao ov (copia verificada + candidatas). Nada e
escrito fora de F_KERNEL: o lean so le .olean; a saida (-o) vai sempre para pastas dentro de F_KERNEL.
Logs gravados em modo 'xb' (nada se sobrescreve).
"""
import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone

F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\F_KERNEL
# copia do toolchain elan v4.31.0 em F_KERNEL\tc (nome curto: na 1a execucao, F_KERNEL\toolchain\leanprover--lean4---v4.31.0
# passava de 260 caracteres e o lean nao abria Std\Tactic\BVDecide\...\RotateRight.olean)
LEAN = os.path.join(F, "tc", "bin", "lean.exe")
TOOL_LIB = os.path.join(F, "tc", "lib", "lean")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
PKGROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\tgl_kernel\.lake\packages"  # alvo da juncao Nos\tgl_kernel\.lake\packages
PKGS = ["batteries", "Qq", "aesop", "proofwidgets", "importGraph", "LeanSearchClient", "plausible", "mathlib"]
TRIO = {"propext", "Classical.choice", "Quot.sound"}
PROIBIDOS = (r"(?<![\w#.])(sorry|admit|axiom|unsafe|implemented_by|extern|opaque|run_cmd|run_tac|#eval|#exit|"
             r"native_decide|ofReduceBool|skipKernelTC|macro_rules|elab_rules|macro|elab|syntax|debug\.\w+|trust\w*)(?![\w])")


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def base_lean_path(kernel_lib=None):
    # kernel_lib: None = os .olean do Nos no lugar (so leitura); ou a SOBREPOSICAO ov (copia verificada + candidatas),
    # porque o lean resolve a raiz TGLExt na PRIMEIRA pasta do LEAN_PATH que a contem (medido; ver demo_resolucao_raiz.py)
    caminhos = [kernel_lib or os.path.join(NOS, ".lake", "build", "lib", "lean")]
    caminhos += [os.path.join(PKGROOT, n, ".lake", "build", "lib", "lean") for n in PKGS]
    caminhos += [TOOL_LIB]
    for c in caminhos:
        if not os.path.isdir(c):
            raise SystemExit("FAIL_CLOSED: caminho ausente no LEAN_PATH: " + c)
    return caminhos


def strip_comments(texto):
    # remove comentarios de bloco aninhados /- ... -/ e de linha -- ...; strings ficam (varredura mais estrita)
    out, i, depth, n = [], 0, 0, len(texto)
    while i < n:
        if texto.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth > 0 and texto.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth > 0:
            i += 1
            continue
        if texto.startswith("--", i):
            j = texto.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(texto[i])
        i += 1
    return "".join(out)


def scan_tokens(path):
    texto = open(path, "rb").read().decode("utf-8")
    sem = strip_comments(texto)
    return sorted(set(re.findall(PROIBIDOS, sem)))


def parse_out(out):
    axs = {}
    for decl, vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", out, re.S):
        axs[decl] = [v.strip() for v in vals.replace("\n", " ").split(",") if v.strip()]
    for decl in re.findall(r"'([^']+)' does not depend on any axioms", out):
        axs[decl] = []
    linhas = out.splitlines()
    erros = [l for l in linhas if re.search(r":\d+:\d+: error", l) or l.startswith("error")]
    avisos = [l for l in linhas if re.search(r":\d+:\d+: warning", l)]
    sorry = [l for l in linhas if "declaration uses 'sorry'" in l or "sorryAx" in l]
    fora = {k: v for k, v in axs.items() if not set(v) <= TRIO}
    return {"axiomas": axs, "n_axiomas": len(axs), "fora_do_trio": fora, "erros": erros, "avisos": avisos,
            "n_avisos": len(avisos), "sorry": sorry}


def run_lean(nome, fonte, root, olean, logdir, extra_paths=(), timeout=5400, use_root_flag=True, kernel_lib=None):
    os.makedirs(logdir, exist_ok=True)
    if olean:
        os.makedirs(os.path.dirname(olean), exist_ok=True)
    caminhos = base_lean_path(kernel_lib) + [p for p in extra_paths]
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(caminhos)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    cmd = [LEAN]
    if use_root_flag:
        cmd.append("--root=" + root)
    if olean:
        cmd += ["-o", olean]
    cmd.append(fonte)
    t0 = time.time()
    quando = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, timeout=timeout)
    dt = time.time() - t0
    raw = p.stdout + p.stderr
    k = 1
    while os.path.exists(os.path.join(logdir, "%s_r%d.log" % (nome, k))):
        k += 1
    log = os.path.join(logdir, "%s_r%d.log" % (nome, k))
    with open(log, "xb") as fh:
        fh.write(raw)
    out = raw.decode("utf-8", "replace")
    res = {"nome": nome, "quando_utc": quando, "cmd": cmd, "cwd": root, "LEAN_PATH": env["LEAN_PATH"],
           "rc": p.returncode, "segundos": round(dt, 1), "fonte": fonte, "fonte_sha256": sha(fonte),
           "fonte_bytes": os.path.getsize(fonte), "log": log, "log_sha256": sha(log)}
    res.update(parse_out(out))
    if olean and os.path.exists(olean):
        res["olean"] = olean
        res["olean_sha256"] = sha(olean)
    res["tokens_proibidos_na_fonte"] = scan_tokens(fonte)
    res["ok"] = bool(p.returncode == 0 and not res["erros"] and not res["sorry"] and not res["fora_do_trio"])
    return res


def dump(obj, path):
    k = 1
    base, ext = os.path.splitext(path)
    alvo = path
    while os.path.exists(alvo):
        k += 1
        alvo = "%s_r%d%s" % (base, k, ext)
    with open(alvo, "xb") as fh:
        fh.write((json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return alvo
