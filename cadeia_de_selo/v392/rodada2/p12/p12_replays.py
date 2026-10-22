# -*- coding: utf-8 -*-
"""P12 (rodada 2, gerencia c1): replays T18-T22 da etapa 1 da cadeia v392 (pre_selo, contra a v391).
Leitura ampla de «bancada» (decisao P12): copias com o mesmo sha256, comparacao com o arquivo, UM RECIBO POR TESTE,
em cartorio fail-closed (falha visivel; nunca 'ok' falso). Nada de dado observado: so copias e sinteticos.
Nao toca Bancada_Um, nao chama servico HTTP, nao roda o um.py (so LE os bytes dele, via os scripts de replay).
Uso: python -B -X utf8 p12_replays.py T18|T19|T20|T21|T22
Escreve so em V\\bateria_pre_selo\\ensaio_2_T18_T22 e no sandbox C:\\t\\p12 (apagado ao fim por limpar_p12.py).
"""
import datetime
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback

V = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo", "v392")
ENS = os.path.join(V, "bateria_pre_selo", "ensaio_2_T18_T22")
REC = os.path.join(ENS, "recibos")
ART = os.path.join(ENS, "artefatos")
WRK = os.path.join(ENS, "trabalho")
SB = os.path.join("C:" + os.sep, "t", "p12")
ORD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019")
PROG = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TC = os.path.join(os.path.expanduser("~"), ".elan", "toolchains", "leanprover--lean4---v4.31.0")
LEAN = os.path.join(TC, "bin", "lean.exe")
LEAN_LIB = os.path.join(TC, "lib", "lean")
KS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v388_kernel", "kernel_src")
PKGS = ["batteries", "Qq", "aesop", "proofwidgets", "importGraph", "LeanSearchClient", "plausible", "mathlib"]
TRIO = {"propext", "Classical.choice", "Quot.sound"}
FLOAT_TOL = 1e-12  # tolerancia relativa declarada para os reruns numericos (T21, T22)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def shab(b):
    return hashlib.sha256(b).hexdigest()


def agora():
    return datetime.datetime.now().astimezone()


def iso(d):
    return d.isoformat(timespec="seconds")


def pin(papel, p):
    return {"papel": papel, "caminho": p, "sha256": sha(p), "bytes": os.path.getsize(p)}


def put_json(path, obj):
    """Backup de BYTES se existir; temporario -> conferir -> os.replace."""
    data = (json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        shutil.copyfile(path, path + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    if os.path.getsize(tmp) != len(data):
        raise IOError("tamanho do temporario nao confere: " + tmp)
    os.replace(tmp, path)
    return shab(data)


def put_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        shutil.copyfile(path, path + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    if os.path.getsize(tmp) != len(data):
        raise IOError("tamanho do temporario nao confere: " + tmp)
    os.replace(tmp, path)


def norm(b):
    t = b.decode("utf-8", "replace").replace("\r\n", "\n")
    return "\n".join(l.rstrip() for l in t.strip().split("\n"))


def parse_axioms(txt):
    axs = {}
    for decl, vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", txt, re.S):
        axs[decl] = sorted(v.strip() for v in vals.replace("\n", " ").split(",") if v.strip())
    for decl in re.findall(r"'([^']+)' does not depend on any axioms", txt):
        axs[decl] = []
    return axs


def lean_version():
    p = subprocess.run([LEAN, "--version"], capture_output=True)
    return (p.stdout + p.stderr).decode("utf-8", "replace").strip()


def lean_path(extra=()):
    caminhos = [os.path.join(KS, ".lake", "packages", n, ".lake", "build", "lib", "lean") for n in PKGS]
    caminhos += [os.path.join(KS, ".lake", "build", "lib", "lean"), LEAN_LIB]
    caminhos += list(extra)
    for c in caminhos:
        if not os.path.isdir(c):
            raise SystemExit("FAIL_CLOSED: caminho ausente no LEAN_PATH: " + c)
    return caminhos


def copy_check(src, dst, esperado_sha=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    b = open(src, "rb").read()
    s0 = shab(b)
    if esperado_sha and s0 != esperado_sha:
        raise RuntimeError("sha256 da origem difere do pino: %s vs %s (%s)" % (s0, esperado_sha, src))
    with open(dst, "wb") as fh:
        fh.write(b)
    if sha(dst) != s0:
        raise RuntimeError("copia difere da origem: " + dst)
    return s0


def run_lean(src, root, olean, extra_lp=()):
    os.makedirs(os.path.dirname(olean), exist_ok=True)
    lp = lean_path(extra_lp)
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(lp)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    cmd = [LEAN, "-o", olean, "--root=" + root, src]
    t0 = agora()
    p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, timeout=7200)
    t1 = agora()
    raw = p.stdout + p.stderr
    out = raw.decode("utf-8", "replace")
    erros = [l for l in out.splitlines() if re.search(r":\d+:\d+: error", l) or l.startswith("error")]
    sorry = [l for l in out.splitlines() if "declaration uses 'sorry'" in l or "sorryAx" in l]
    return {"cmd": cmd, "cwd": root, "LEAN_PATH": env["LEAN_PATH"], "rc": p.returncode, "ini": t0, "fim": t1,
            "raw": raw, "out": out, "erros": erros, "sorry": sorry, "axiomas": parse_axioms(out),
            "olean": olean, "olean_existe": os.path.exists(olean)}


def base_rec(teste, desc):
    return {"teste": teste, "descricao": desc, "fase": "pre_selo", "contra": "v391",
            "estatuto": "[REAL] replay executado aqui por script; nenhum dado observado; validade na face testada, nao creditacao",
            "python": sys.version, "python_exe": sys.executable, "plataforma": platform.platform(),
            "cwd_do_processo": os.getcwd(), "entradas": [], "saidas": [], "veredito": "NAO_EXECUTADO", "razao": ""}


def finish(rec, ini, fim, cmd, cwd, rc):
    rec["comando"] = cmd
    rec["cwd"] = cwd
    rec["inicio"] = iso(ini)
    rec["fim"] = iso(fim)
    rec["segundos"] = round((fim - ini).total_seconds(), 1)
    rec["codigo_saida"] = rc
    return rec


# ---------------------------------------------------------------------------------------------------- T18, T19, T20
def lean_compare(rec, r, esperado_olean_sha, olean_arquivo, esperado_axiomas, esperado_log_texto, rotulo):
    """Compara um build com o da entrega. Devolve dict de comparacao e se passa."""
    c = {"rotulo": rotulo}
    c["rc_zero"] = r["rc"] == 0
    c["sem_erros"] = not r["erros"]
    c["sem_sorry"] = not r["sorry"]
    c["olean_existe"] = r["olean_existe"]
    sha_out = sha(r["olean"]) if r["olean_existe"] else None
    c["olean_sha256_replay"] = sha_out
    c["olean_sha256_esperado"] = esperado_olean_sha
    c["olean_byte_a_byte"] = bool(sha_out and esperado_olean_sha and sha_out == esperado_olean_sha)
    if olean_arquivo and os.path.exists(olean_arquivo) and r["olean_existe"]:
        c["olean_igual_ao_arquivo_da_entrega"] = open(olean_arquivo, "rb").read() == open(r["olean"], "rb").read()
    c["axiomas_replay"] = r["axiomas"]
    c["n_declaracoes_replay"] = len(r["axiomas"])
    c["fora_do_trio"] = {k: v for k, v in r["axiomas"].items() if not set(v) <= TRIO}
    if esperado_axiomas is not None:
        c["axiomas_esperados_n"] = len(esperado_axiomas)
        c["mesmas_declaracoes"] = sorted(esperado_axiomas) == sorted(r["axiomas"])
        c["mesmos_axiomas_por_declaracao"] = esperado_axiomas == r["axiomas"]
    if esperado_log_texto is not None:
        c["saida_igual_ao_log_da_entrega"] = norm(r["raw"]) == esperado_log_texto
    return c


def passa_lean(c):
    base = c["rc_zero"] and c["sem_erros"] and c["sem_sorry"] and c["olean_existe"] and not c["fora_do_trio"] \
        and c["n_declaracoes_replay"] > 0
    if "mesmos_axiomas_por_declaracao" in c:
        base = base and c["mesmos_axiomas_por_declaracao"]
    exato = base and c.get("olean_byte_a_byte", False)
    return base, exato


def T18():
    rec = base_rec("T18_LIGANTE_LEI_CAMPO_CURVO", "F2.3: recompilar LiganteLeiCampoCurvo.lean em copia isolada e comparar o .olean (f76c372e...) e os axiomas com a entrega")
    D = os.path.join(ORD, "F2.3")
    hs = json.load(open(os.path.join(D, "HASHES.json"), encoding="utf-8"))
    ent = {os.path.basename(a["path"]): a["sha256"] for a in hs["artifacts"] if "\\kernel\\" not in a["path"]}
    src_sha = ent["LiganteLeiCampoCurvo.lean"]
    ol_sha = ent["LiganteLeiCampoCurvo.olean"]
    assert src_sha.startswith("e3f32d9b85ae82db"), src_sha
    assert ol_sha.startswith("f76c372e"), ol_sha
    root = os.path.join(SB, "t18")
    src = os.path.join(root, "TGLExt", "LiganteLeiCampoCurvo.lean")
    olean = os.path.join(root, "out", "TGLExt", "LiganteLeiCampoCurvo.olean")
    rec["entradas"].append(pin("fonte da entrega F2.3", os.path.join(D, "LiganteLeiCampoCurvo.lean")))
    rec["entradas"].append(pin("olean da entrega F2.3", os.path.join(D, "LiganteLeiCampoCurvo.olean")))
    rec["entradas"].append(pin("HASHES.json da entrega (pinos lidos)", os.path.join(D, "HASHES.json")))
    rec["entradas"].append(pin("BUILD.log da entrega", os.path.join(D, "BUILD.log")))
    rec["entradas"].append(pin("AXIOMAS.txt da entrega", os.path.join(D, "AXIOMAS.txt")))
    copy_check(os.path.join(D, "LiganteLeiCampoCurvo.lean"), src, src_sha)
    rec["copia_isolada"] = {"caminho": src, "sha256": sha(src), "igual_ao_pino": sha(src) == src_sha}
    r = run_lean(src, root, olean)
    esperado = parse_axioms(open(os.path.join(D, "AXIOMAS.txt"), encoding="utf-8").read())
    c = lean_compare(rec, r, ol_sha, os.path.join(D, "LiganteLeiCampoCurvo.olean"), esperado,
                     norm(open(os.path.join(D, "BUILD.log"), "rb").read()), "T18")
    ok, exato = passa_lean(c)
    rec["comparacao"] = c
    log = os.path.join(ART, "T18_replay.log")
    put_bytes(log, r["raw"])
    put_bytes(os.path.join(ART, "T18_LiganteLeiCampoCurvo_replay.olean"), open(olean, "rb").read()) if r["olean_existe"] else None
    rec["saidas"].append({"papel": "log do build", "caminho": log, "sha256": sha(log), "bytes": os.path.getsize(log)})
    if r["olean_existe"]:
        rec["saidas"].append({"papel": "olean do replay (sandbox)", "caminho": olean, "sha256": sha(olean), "bytes": os.path.getsize(olean)})
    rec["lean_version"] = lean_version()
    rec["env_LEAN_PATH"] = r["LEAN_PATH"]
    finish(rec, r["ini"], r["fim"], r["cmd"], r["cwd"], r["rc"])
    rec["veredito"] = "PASSA" if ok else "FALHA"
    rec["modo_comparacao"] = "olean byte a byte + axiomas" if exato else ("declaracoes e axiomas (olean difere)" if ok else "FALHOU")
    rec["razao"] = "" if ok else "ver comparacao"
    return rec


def T19():
    rec = base_rec("T19_PONTE_V351_E_AGAPE", "F1.2: recompilar V351DualScalingBridge e AgapeNonVacuity em copia isolada e comparar os .olean (940b8ddf, ba0d9868)")
    D = os.path.join(ORD, "F1.2", "sandbox")
    res = json.load(open(os.path.join(D, "BUILD_COMPLETION_RESULT.json"), encoding="utf-8"))
    passos = {s["module"]: s for s in res["steps"]}
    assert passos["V351DualScalingBridge"]["olean_sha256"].startswith("940b8ddf")
    assert passos["AgapeNonVacuity"]["olean_sha256"].startswith("ba0d9868")
    root = os.path.join(SB, "t19")
    buildroot = os.path.join(root, "build")
    rec["entradas"].append(pin("BUILD_COMPLETION_RESULT.json da entrega (pinos lidos)", os.path.join(D, "BUILD_COMPLETION_RESULT.json")))
    comps = []
    primeiro = None
    ultimo = None
    cmds = []
    rcs = []
    ok_total = True
    exato_total = True
    for stem in ("V351DualScalingBridge", "AgapeNonVacuity"):
        s = passos[stem]
        fonte_ent = os.path.join(D, "F12Completion", stem + ".lean")
        olean_ent = os.path.join(D, "build", "F12Completion", stem + ".olean")
        logent = os.path.join(D, "BUILD_%s.log" % stem)
        rec["entradas"] += [pin("fonte da entrega " + stem, fonte_ent), pin("olean da entrega " + stem, olean_ent),
                            pin("log do build da entrega " + stem, logent)]
        src = os.path.join(root, "F12Completion", stem + ".lean")
        olean = os.path.join(buildroot, "F12Completion", stem + ".olean")
        copy_check(fonte_ent, src, s["source_sha256"])
        r = run_lean(src, root, olean, extra_lp=[buildroot])
        c = lean_compare(rec, r, s["olean_sha256"], olean_ent, parse_axioms(open(logent, encoding="utf-8", errors="replace").read()),
                         norm(open(logent, "rb").read()), stem)
        c["log_sha256_replay"] = shab(r["raw"])
        c["log_sha256_entrega"] = s["log_sha256"]
        c["log_byte_a_byte"] = c["log_sha256_replay"] == c["log_sha256_entrega"]
        ok, exato = passa_lean(c)
        comps.append(c)
        ok_total = ok_total and ok
        exato_total = exato_total and exato
        log = os.path.join(ART, "T19_%s_replay.log" % stem)
        put_bytes(log, r["raw"])
        if r["olean_existe"]:
            put_bytes(os.path.join(ART, "T19_%s_replay.olean" % stem), open(olean, "rb").read())
            rec["saidas"].append({"papel": "olean do replay " + stem, "caminho": olean, "sha256": sha(olean), "bytes": os.path.getsize(olean)})
        rec["saidas"].append({"papel": "log " + stem, "caminho": log, "sha256": sha(log), "bytes": os.path.getsize(log)})
        primeiro = primeiro or r["ini"]
        ultimo = r["fim"]
        cmds.append(r["cmd"])
        rcs.append(r["rc"])
        rec["env_LEAN_PATH"] = r["LEAN_PATH"]
        if r["rc"] != 0:
            break
    rec["comparacao"] = comps
    rec["lean_version"] = lean_version()
    finish(rec, primeiro, ultimo, cmds, root, rcs)
    rec["veredito"] = "PASSA" if (ok_total and len(comps) == 2) else "FALHA"
    rec["modo_comparacao"] = "olean byte a byte + axiomas" if (ok_total and exato_total) else ("declaracoes e axiomas (olean difere)" if ok_total else "FALHOU")
    return rec


def T20():
    rec = base_rec("T20_PALAVRA", "PALAVRA (sandbox de 07/10): replay da compilacao e das 7 declaracoes no trio")
    D = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "leitura_cria_o_objeto_07out")
    fonte = os.path.join(D, "Palavra.lean")
    s_fonte = sha(fonte)
    assert s_fonte.startswith("33184b49a8bba7e7"), s_fonte
    saida = os.path.join(D, "saida_palavra.txt")
    rec["entradas"] += [pin("Palavra.lean (sandbox 07/10)", fonte), pin("saida_palavra.txt (07/10)", saida)]
    cruz = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v392_insumos", "F_KERNEL", "inst", "TGLExt", "Palavra.lean")
    rec["conferencia_cruzada"] = {"F_KERNEL_inst_Palavra_lean": cruz, "existe": os.path.exists(cruz),
                                  "sha256": sha(cruz) if os.path.exists(cruz) else None,
                                  "igual_a_fonte": (sha(cruz) == s_fonte) if os.path.exists(cruz) else None}
    root = os.path.join(SB, "t20")
    src = os.path.join(root, "TGLExt", "Palavra.lean")
    olean = os.path.join(root, "out", "TGLExt", "Palavra.olean")
    copy_check(fonte, src, s_fonte)
    r = run_lean(src, root, olean)
    txt = open(saida, "rb").read().decode("utf-8")
    esperado = parse_axioms(txt)
    c = lean_compare(rec, r, None, None, esperado, None, "T20")
    c["saida_igual_a_saida_palavra_txt"] = norm(r["raw"]) == norm("\n".join(l for l in txt.splitlines() if not l.startswith("LEAN_RC=")).encode("utf-8"))
    c["n_declaracoes_esperado"] = 7
    c["sete_declaracoes"] = len(r["axiomas"]) == 7
    c["LEAN_RC_da_saida_07out"] = [l for l in txt.splitlines() if l.startswith("LEAN_RC=")]
    c["olean_byte_a_byte"] = None  # nao ha olean de referencia: a PALAVRA nao foi guardada compilada
    ok, _ = passa_lean(c)
    ok = ok and c["sete_declaracoes"] and c["saida_igual_a_saida_palavra_txt"]
    rec["comparacao"] = c
    log = os.path.join(ART, "T20_replay.log")
    put_bytes(log, r["raw"])
    rec["saidas"].append({"papel": "log do build", "caminho": log, "sha256": sha(log), "bytes": os.path.getsize(log)})
    if r["olean_existe"]:
        put_bytes(os.path.join(ART, "T20_Palavra_replay.olean"), open(olean, "rb").read())
        rec["saidas"].append({"papel": "olean do replay (sandbox; sem olean de referencia)", "caminho": olean, "sha256": sha(olean), "bytes": os.path.getsize(olean)})
    rec["lean_version"] = lean_version()
    rec["env_LEAN_PATH"] = r["LEAN_PATH"]
    finish(rec, r["ini"], r["fim"], r["cmd"], r["cwd"], r["rc"])
    rec["veredito"] = "PASSA" if ok else "FALHA"
    rec["modo_comparacao"] = "saida (7 declaracoes + axiomas) igual a saida_palavra.txt; sem olean de referencia"
    return rec


# ---------------------------------------------------------------------------------------------------- T21, T22
def deep_compare(a, b, caminho="", ignorar=(), tol=FLOAT_TOL, difs=None, cont=None):
    """Compara estruturas JSON: exato para tudo exceto float (tolerancia relativa tol). Chaves em `ignorar` (nome da chave) saltam."""
    if difs is None:
        difs = []
        cont = {"folhas": 0, "floats_exatos": 0, "floats_na_tolerancia": 0, "max_rel": 0.0}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in ignorar:
                continue
            if k not in a or k not in b:
                difs.append("%s/%s: chave so em um dos lados" % (caminho, k))
                continue
            deep_compare(a[k], b[k], caminho + "/" + k, ignorar, tol, difs, cont)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            difs.append("%s: tamanhos %d vs %d" % (caminho, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            deep_compare(x, y, "%s[%d]" % (caminho, i), ignorar, tol, difs, cont)
    else:
        cont["folhas"] += 1
        if isinstance(a, float) and isinstance(b, float):
            if a == b:
                cont["floats_exatos"] += 1
            else:
                rel = abs(a - b) / max(abs(a), abs(b), 1e-300)
                cont["max_rel"] = max(cont["max_rel"], rel)
                if rel <= tol:
                    cont["floats_na_tolerancia"] += 1
                else:
                    difs.append("%s: %r vs %r (rel %.3e)" % (caminho, a, b, rel))
        elif a != b or type(a) is not type(b):
            difs.append("%s: %r vs %r" % (caminho, a, b))
    return difs, cont


def run_py(script, args, cwd, extra_flags=("-I",)):
    cmd = [sys.executable, *extra_flags, "-B", "-X", "utf8", script, *args]
    t0 = agora()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=7200)
    t1 = agora()
    return {"cmd": cmd, "cwd": cwd, "rc": p.returncode, "ini": t0, "fim": t1, "stdout": p.stdout, "stderr": p.stderr}


def T21():
    rec = base_rec("T21_SN1_CONTAS_CONDICIONAIS", "F8.2.SN1: rerun em copia de calculate_r2.py (planos R1+R2) e comparacao com CALCULOS_R2.json; tolerancia relativa %.0e nos floats" % FLOAT_TOL)
    D = os.path.join(ORD, "F8.2.SN1")
    A = os.path.join(PROG, "exame_12out", "A_SN", "rerun_copia")
    w = os.path.join(WRK, "T21")
    arqs = ["calculate_r2.py", "PLANO_CALCULO_R1.json", "PLANO_COMPLEMENTO_R2.json"]
    cop = []
    for a in arqs:
        s = sha(os.path.join(D, a))
        copy_check(os.path.join(D, a), os.path.join(w, a), s)
        rec["entradas"].append(pin("entrega F8.2.SN1/" + a, os.path.join(D, a)))
        sa = sha(os.path.join(A, a))
        cop.append({"arquivo": a, "sha256_entrega": s, "sha256_rerun_copia_A_SN": sa, "iguais": s == sa})
    rec["copias_conferidas"] = cop
    rec["entradas"].append(pin("CALCULOS_R2.json da entrega (referencia)", os.path.join(D, "CALCULOS_R2.json")))
    rec["entradas"].append(pin("CALCULOS_R2_RERUN.json do auditor A_SN (referencia 2)", os.path.join(A, "CALCULOS_R2_RERUN.json")))
    plano = json.load(open(os.path.join(w, "PLANO_CALCULO_R1.json"), encoding="utf-8"))
    fonte_alpha = plano["fonte_alpha"]["path"]
    rec["entradas"].append(pin("fonte do alpha lida pelo script (bytes do um.py do Nos)", fonte_alpha))
    out = os.path.join(w, "CALCULOS_R2_REPLAY.json")
    if os.path.exists(out):
        os.replace(out, out + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
    r = run_py(os.path.join(w, "calculate_r2.py"), ["--output", out], w)
    rec["stdout_sha256"] = shab(r["stdout"])
    rec["stderr"] = r["stderr"].decode("utf-8", "replace")[-2000:]
    cmp1 = cmp2 = None
    ok = False
    if r["rc"] == 0 and os.path.exists(out):
        rec["saidas"].append(pin("CALCULOS_R2_REPLAY.json", out))
        novo = json.load(open(out, encoding="utf-8"))
        ref = json.load(open(os.path.join(D, "CALCULOS_R2.json"), encoding="utf-8"))
        aud = json.load(open(os.path.join(A, "CALCULOS_R2_RERUN.json"), encoding="utf-8"))
        ign = ("start_utc", "end_utc", "elapsed_seconds", "pins")  # tempos; 'pins' traz caminhos da copia: comparados a parte
        d1, c1 = deep_compare(novo, ref, "", ign)
        d2, c2 = deep_compare(novo, aud, "", ign)
        # pins: sha256 e bytes devem coincidir por arquivo (os caminhos mudam por serem copias)
        def pins_sha(x):
            return sorted((os.path.basename(p["path"]), p["sha256"], p["bytes"]) for p in x["pins"])
        pins_ok_ref = pins_sha(novo) == pins_sha(ref)
        pins_ok_aud = pins_sha(novo) == pins_sha(aud)
        cmp1 = {"contra": "CALCULOS_R2.json da entrega", "diferencas": d1, **c1, "pins_sha256_iguais": pins_ok_ref}
        cmp2 = {"contra": "CALCULOS_R2_RERUN.json do auditor A_SN", "diferencas": d2, **c2, "pins_sha256_iguais": pins_ok_aud}
        rec["alpha_source_replay"] = novo.get("alpha_source")
        rec["beta0_replay"] = novo.get("beta0")
        rec["beta0_runtime_conferido_igual"] = novo.get("beta0") == 0.012031300400803142
        ok = (not d1) and pins_ok_ref and all(x["sha256_entrega"] == x["sha256_rerun_copia_A_SN"] for x in cop)
        rec["razao"] = "" if ok else "diferencas na comparacao com a entrega (ver comparacao)"
    else:
        rec["razao"] = "rerun nao produziu saida: rc=%s" % r["rc"]
    rec["comparacao"] = [cmp1, cmp2]
    finish(rec, r["ini"], r["fim"], r["cmd"], r["cwd"], r["rc"])
    rec["tolerancia_declarada"] = {"floats_rel": FLOAT_TOL, "inteiros_strings_booleanos": "exato", "ignorados": ["start_utc", "end_utc", "elapsed_seconds", "pins (caminhos; shas comparados a parte)"]}
    rec["veredito"] = "PASSA" if ok else "FALHA"
    return rec


def T22():
    rec = base_rec("T22_NU2_21_DE_21", "F8.2.NU2: rerun em copia do operador espectral (CALCULOS_ESPECTRAIS_R1) e da reproducao independente da B_NU2 (21 de 21)")
    D = os.path.join(ORD, "F8.2.NU2")
    B = os.path.join(PROG, "exame_12out", "B_NU2")
    w = os.path.join(WRK, "T22")
    res = json.load(open(os.path.join(D, "RESULTADO_R1.json"), encoding="utf-8"))
    pinos = {os.path.basename(f["path"]): f["sha256"] for f in res["files"]}
    # (a) operador espectral da entrega
    for a in ("spectral_operator_r1.py", "PLANO_R1.json", "PLANO_RECONCILIACAO_R1.json"):
        s = sha(os.path.join(D, a))
        if a in pinos and pinos[a] != s:
            raise RuntimeError("entrega alterada: " + a)
        copy_check(os.path.join(D, a), os.path.join(w, a), s)
        rec["entradas"].append(pin("entrega F8.2.NU2/" + a + ("" if a not in pinos else " (igual ao pino do RESULTADO_R1)"), os.path.join(D, a)))
    rec["entradas"].append(pin("CALCULOS_ESPECTRAIS_R1.json da entrega (referencia)", os.path.join(D, "CALCULOS_ESPECTRAIS_R1.json")))
    ref_ok_pino = pinos.get("CALCULOS_ESPECTRAIS_R1.json") == sha(os.path.join(D, "CALCULOS_ESPECTRAIS_R1.json"))
    out_a = os.path.join(w, "CALCULOS_ESPECTRAIS_R1_REPLAY.json")
    if os.path.exists(out_a):
        os.replace(out_a, out_a + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
    ra = run_py(os.path.join(w, "spectral_operator_r1.py"), ["--output", out_a], w)
    plano = json.load(open(os.path.join(w, "PLANO_R1.json"), encoding="utf-8"))
    rec["entradas"].append(pin("fonte do alpha (bytes do um.py do Nos)", plano["alpha_source"]))
    # (b) reproducao independente da B_NU2 (21 checks)
    wb = os.path.join(w, "B_NU2")
    s_rep = sha(os.path.join(B, "reproducao_nu2.py"))
    copy_check(os.path.join(B, "reproducao_nu2.py"), os.path.join(wb, "reproducao_nu2.py"), s_rep)
    rec["entradas"].append(pin("B_NU2/reproducao_nu2.py", os.path.join(B, "reproducao_nu2.py")))
    rec["entradas"].append(pin("B_NU2/_reproducao_nu2.json (referencia do auditor)", os.path.join(B, "_reproducao_nu2.json")))
    rep_out = os.path.join(wb, "_reproducao_nu2.json")
    if os.path.exists(rep_out):
        os.replace(rep_out, rep_out + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
    # numpy/scipy/mpmath vivem no site do usuario: sem -I (mesma excecao do um.py)
    rb = run_py(os.path.join(wb, "reproducao_nu2.py"), [], wb, extra_flags=())
    ini, fim = ra["ini"], rb["fim"]
    comp = {}
    ok_a = ok_b = False
    if ra["rc"] == 0 and os.path.exists(out_a):
        rec["saidas"].append(pin("CALCULOS_ESPECTRAIS_R1_REPLAY.json", out_a))
        novo = json.load(open(out_a, encoding="utf-8"))
        ref = json.load(open(os.path.join(D, "CALCULOS_ESPECTRAIS_R1.json"), encoding="utf-8"))
        ign = ("start_utc", "end_utc", "elapsed_s", "source_pins")
        d, c = deep_compare(novo, ref, "", ign)
        comp["espectral_vs_entrega"] = {"diferencas": d, **c, "referencia_igual_ao_pino_do_RESULTADO_R1": ref_ok_pino,
                                        "source_pins_sha_e_bytes_iguais": (sorted((os.path.basename(p["path"]), p["sha256"], p["bytes"]) for p in novo["source_pins"])
                                                                         == sorted((os.path.basename(p["path"]), p["sha256"], p["bytes"]) for p in ref["source_pins"]))}
        ok_a = (not d) and comp["espectral_vs_entrega"]["source_pins_sha_e_bytes_iguais"] and ref_ok_pino
        # as chaves do topo, para o relatorio
        comp["espectral_chaves_topo"] = sorted(novo.keys())
    else:
        comp["espectral_vs_entrega"] = {"erro": "rerun sem saida: rc=%s stderr=%s" % (ra["rc"], ra["stderr"].decode("utf-8", "replace")[-800:])}
    if rb["rc"] == 0 and os.path.exists(rep_out):
        rec["saidas"].append(pin("_reproducao_nu2.json (replay)", rep_out))
        novo = json.load(open(rep_out, encoding="utf-8"))
        ref = json.load(open(os.path.join(B, "_reproducao_nu2.json"), encoding="utf-8"))
        nomes_n = [c["nome"] for c in novo["checks"]]
        nomes_r = [c["nome"] for c in ref["checks"]]
        comp["reproducao_B_NU2"] = {"n_checks": novo["n_checks"], "n_passa": novo["n_passa"],
                                    "mesmos_nomes_na_mesma_ordem": nomes_n == nomes_r,
                                    "passa_por_check": [c["PASSA"] for c in novo["checks"]],
                                    "falhas": [c["nome"] for c in novo["checks"] if not c["PASSA"]],
                                    "referencia_n_checks": ref["n_checks"], "referencia_n_passa": ref["n_passa"]}
        ign = ("um_py_sha256",)  # sera comparado a parte
        d, c = deep_compare({k: v for k, v in novo.items() if k != "checks"}, {k: v for k, v in ref.items() if k != "checks"}, "", ign)
        comp["reproducao_B_NU2"]["resumo_vs_referencia"] = {"diferencas": d, **c}
        comp["reproducao_B_NU2"]["um_py_sha256_replay"] = novo.get("um_py_sha256")
        comp["reproducao_B_NU2"]["um_py_sha256_referencia"] = ref.get("um_py_sha256")
        ok_b = (novo["n_checks"] == 21 and novo["n_passa"] == 21 and nomes_n == nomes_r and not [1 for c in novo["checks"] if not c["PASSA"]])
    else:
        comp["reproducao_B_NU2"] = {"erro": "rerun sem saida: rc=%s stderr=%s" % (rb["rc"], rb["stderr"].decode("utf-8", "replace")[-800:])}
    rec["comparacao"] = comp
    rec["tolerancia_declarada"] = {"floats_rel": FLOAT_TOL, "outros": "exato", "ignorados": ["start_utc, end_utc, elapsed_s", "source_pins (caminhos; shas e bytes comparados a parte)"]}
    stdb = os.path.join(ART, "T22_reproducao_nu2_stdout.txt")
    put_bytes(stdb, rb["stdout"])
    rec["saidas"].append({"papel": "stdout da reproducao B_NU2 (replay)", "caminho": stdb, "sha256": sha(stdb), "bytes": os.path.getsize(stdb)})
    rec["stderr_espectral"] = ra["stderr"].decode("utf-8", "replace")[-1500:]
    rec["stderr_reproducao"] = rb["stderr"].decode("utf-8", "replace")[-1500:]
    finish(rec, ini, fim, [ra["cmd"], rb["cmd"]], [ra["cwd"], rb["cwd"]], [ra["rc"], rb["rc"]])
    rec["veredito"] = "PASSA" if (ok_a and ok_b) else "FALHA"
    rec["razao"] = "" if rec["veredito"] == "PASSA" else "espectral_ok=%s reproducao_21de21_ok=%s" % (ok_a, ok_b)
    return rec


TESTES = {"T18": T18, "T19": T19, "T20": T20, "T21": T21, "T22": T22}


def main():
    t = sys.argv[1]
    nome_arquivo = {"T18": "T18_LIGANTE", "T19": "T19_V351_AGAPE", "T20": "T20_PALAVRA", "T21": "T21_SN1", "T22": "T22_NU2"}[t]
    try:
        rec = TESTES[t]()
    except BaseException as e:  # fail-closed: o erro vira recibo visivel, nunca 'ok'
        rec = base_rec(t, "erro antes de concluir o replay")
        rec["veredito"] = "NAO_EXECUTADO"
        rec["razao"] = "excecao: %s: %s" % (type(e).__name__, e)
        rec["traceback"] = traceback.format_exc()
        rec["inicio"] = rec["fim"] = iso(agora())
    h = put_json(os.path.join(REC, nome_arquivo + ".json"), rec)
    print(json.dumps({"teste": t, "veredito": rec["veredito"], "razao": rec.get("razao"), "recibo_sha256": h,
                      "modo": rec.get("modo_comparacao")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
